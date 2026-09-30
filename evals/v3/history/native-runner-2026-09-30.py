"""Response-only v3 Codex app-server runner. Python 3.10+, standard library.

How to run: python tools/eval_inquiry.py validate --suite evals/v3
Actual turns require an explicit run-plan file and --execute. Rubrics never
cross the model boundary. Host configuration is evidence, not backend identity.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import tempfile
import threading
import time
from typing import Final, TextIO, TypeAlias

Json: TypeAlias = None | bool | int | float | str | list["Json"] | dict[str, "Json"]
ROOT: Final = Path(__file__).resolve().parents[1]
REFS: Final = ('inquiry-methods.md', 'evidence-and-diagnosis.md', 'alternatives-and-drafting.md')
COMMON: Final = 'Answer the task directly without using tools. Keep the final response within 700 words.'


class RunnerError(RuntimeError):
    """A rejected suite, delivery, transport, or completed-turn contract."""
    def __init__(self, message: str, code: str = 'contract_rejected') -> None:
        super().__init__(message)
        self.code = code


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, value: Json) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load(path: Path):
    """Reject duplicate keys and nonfinite numbers at the file boundary."""
    def pairs(items: list[tuple[str, Json]]):
        result: dict = {}
        for key, value in items:
            if key in result:
                raise RunnerError('duplicate JSON key')
            result[key] = value
        return result
    def nonfinite(value: str) -> None:
        raise RunnerError('nonfinite JSON number: ' + value)
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=pairs, parse_constant=nonfinite)


def validate_suite(suite: Path):
    """Validate task/rubric coverage without exposing rubrics to model input."""
    cases, rubrics = load(suite / 'cases.json'), load(suite / 'rubrics.json')
    if cases['schema_version'] != 1 or rubrics['schema_version'] != 1:
        raise RunnerError('unsupported schema_version')
    ids: set[str] = set()
    for phase in ('calibration', 'confirmation', 'controls'):
        if not cases[phase]:
            raise RunnerError('empty phase: ' + phase)
        for case in cases[phase]:
            if set(case) != {'id', 'family', 'prompt'} or not all(isinstance(case[k], str) and case[k].strip() for k in case):
                raise RunnerError('invalid case shape')
            if not re.fullmatch(r'[A-Za-z0-9_-]+', case['id']) or case['id'] in ids:
                raise RunnerError('unsafe or duplicate case ID')
            ids.add(case['id'])
    if set(rubrics['cases']) != ids:
        raise RunnerError('rubric case coverage mismatch')
    for rubric in rubrics['cases'].values():
        if not {'dimensions', 'critical_failures'}.issubset(rubric) or set(rubric) - {'dimensions', 'critical_failures', 'accepted_answer_policy'} or len(rubric['dimensions']) != 5:
            raise RunnerError('invalid rubric shape')
        dimensions: set[str] = set()
        for dimension in rubric['dimensions']:
            if set(dimension) != {'id', 'zero', 'one', 'two'} or not all(isinstance(v, str) and v.strip() for v in dimension.values()):
                raise RunnerError('invalid rubric dimension')
            if dimension['id'] in dimensions:
                raise RunnerError('duplicate rubric dimension')
            dimensions.add(dimension['id'])
        if not isinstance(rubric['critical_failures'], list) or not all(isinstance(x, str) and x.strip() for x in rubric['critical_failures']):
            raise RunnerError('invalid critical failures')
    protocol = load(suite / 'protocol.json')
    if protocol['schema_version'] != 1 or protocol['model']['requested'] != 'gpt-6-sol' or protocol['model']['requested_effort'] != 'medium' or protocol['runtime']['timeout_seconds'] != 300 or protocol['screening']['trials_per_family'] != 3 or protocol['confirmation']['trials_per_arm_per_family'] != 3 or protocol['controls']['trials_per_arm'] != 1:
        raise RunnerError('protocol does not match fixed runner contract')
    if protocol['runtime']['treatment']['references'] != ['.agents/skills/deep-inquiry/references/' + n for n in REFS]:
        raise RunnerError('protocol reference order mismatch')
    return cases


def verify_hashes(base: Path, expected: dict) -> None:
    """Freeze exact inputs; reject traversal and missing or modified bytes."""
    for relative, value in expected.items():
        path = (base / relative).resolve()
        if not path.is_relative_to(base.resolve()) or not path.is_file() or digest(path) != value:
            raise RunnerError('frozen input mismatch: ' + relative)


@dataclass(slots=True)
class Capture:
    """Mutable accumulator retaining only final messages and safe event metadata."""
    messages: list[str] = field(default_factory=list)
    completion: str | None = None
    telemetry: list = field(default_factory=list)
    output_seen: bool = False
    tool_attempted: bool = False
    delivered_user_text: list[str] = field(default_factory=list)
    delivered_developer_text: list[str] = field(default_factory=list)
    unknown_messages: list[str] = field(default_factory=list)

    def observe(self, event: dict) -> None:
        method = event.get('method')
        if method == 'model/rerouted':
            raise RunnerError('model rerouted')
        params = event.get('params') or {}
        if method == 'rawResponseItem/completed':
            raw = params['item']
            if raw.get('type') in {'local_shell_call', 'function_call', 'tool_search_call', 'custom_tool_call', 'web_search_call'}:
                self.tool_attempted = True
                self.telemetry.append({'method': method, 'item_type': raw['type']})
            if raw.get('type') == 'message' and raw.get('role') in {'user', 'developer'}:
                texts = [x['text'] for x in raw['content'] if x.get('type') == 'input_text']
                destination = self.delivered_user_text if raw['role'] == 'user' else self.delivered_developer_text
                destination.extend(texts)
        if method in {'item/started', 'item/completed'}:
            item = params['item']
            kind = item['type']
            if kind in {'commandExecution', 'fileChange', 'mcpToolCall', 'webSearch', 'dynamicToolCall'}:
                self.tool_attempted = True
            self.telemetry.append({'method': method, 'item_type': kind, 'phase': item.get('phase')})
            if kind == 'agentMessage' and method == 'item/completed':
                self.output_seen = True
                if item.get('phase') == 'final_answer':
                    self.messages.append(item['text'])
                elif item.get('phase') is None:
                    self.unknown_messages.append(item['text'])
        if method == 'item/agentMessage/delta':
            self.output_seen = True
        if method == 'turn/completed':
            self.completion = params['turn']['status']
            self.telemetry.append({'method': method, 'status': self.completion})
        if method in {'error', 'turn/failed'}:
            raise RunnerError('host reported turn error')

    def final_bytes(self) -> bytes:
        if self.completion != 'completed' or len(self.messages) != 1:
            raise RunnerError('missing unique completed final_answer')
        return self.messages[0].encode('utf-8')


def pump(stream: TextIO, messages: queue.Queue[str]) -> None:
    for line in stream:
        messages.put(line)


class Host:
    """Owned stdio process; raw reasoning and stderr are never persisted."""
    def __init__(self, exe: Path, profile: Path, home: Path, workspace: Path, capture: Capture) -> None:
        env = {k: v for k, v in os.environ.items() if not any(w in k.upper() for w in ('CODEX', 'OPENAI', 'ANTHROPIC', 'TOKEN', 'SECRET', 'API_KEY'))}
        env.update(CODEX_HOME=str(profile), HOME=str(home), USERPROFILE=str(home))
        args = [str(exe), '-c', 'model="gpt-6-sol"', '-c', 'model_reasoning_effort="medium"', '--disable', 'apps', '--disable', 'plugins', '--disable', 'remote_plugin', 'app-server', '--stdio']
        self.proc = subprocess.Popen(args, cwd=workspace, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding='utf-8')
        if self.proc.stdin is None or self.proc.stdout is None:
            raise RunnerError('missing owned transport pipes')
        self.stdin, self.stdout = self.proc.stdin, self.proc.stdout
        self.lines: queue.Queue[str] = queue.Queue()
        threading.Thread(target=pump, args=(self.stdout, self.lines), daemon=True).start()
        self.capture, self.number = capture, 0
        self.dispatched = False

    def receive(self, deadline: float):
        try:
            event = json.loads(self.lines.get(timeout=max(.001, deadline - time.monotonic())))
        except queue.Empty as error:
            raise TimeoutError('app-server deadline') from error
        self.capture.observe(event)
        if 'id' in event and 'method' in event:
            raise RunnerError('unexpected server request')
        return event

    def notify(self, method: str, params: dict) -> None:
        self.stdin.write(json.dumps({'method': method, 'params': params}) + '\n')
        self.stdin.flush()

    def call(self, method: str, params: dict, deadline: float | None = None):
        self.number += 1
        if method == 'turn/start':
            self.dispatched = True
        self.stdin.write(json.dumps({'id': self.number, 'method': method, 'params': params}) + '\n')
        self.stdin.flush()
        deadline = deadline if deadline is not None else time.monotonic() + 40
        while True:
            event = self.receive(deadline)
            if event.get('id') == self.number:
                if 'error' in event:
                    raise RunnerError('app-server RPC rejected: ' + method)
                return event['result']

    def initialize(self):
        result = self.call('initialize', {'clientInfo': {'name': 'inquiry-v3', 'version': '1'}, 'capabilities': {'experimentalApi': True}})
        self.notify('initialized', {})
        return result

    def stop(self) -> bool:
        """Terminate only the child this host created; close owned pipes."""
        if self.proc.poll() is None:
            if os.name == 'nt':
                result = subprocess.run(['taskkill', '/PID', str(self.proc.pid), '/T', '/F'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10, check=False)
                if result.returncode and self.proc.poll() is None:
                    self.proc.terminate()
            else:
                self.proc.terminate()
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=10)
        for stream in (self.proc.stdin, self.proc.stdout):
            if stream:
                stream.close()
        return self.proc.poll() is not None


def inputs_for(prompt: str, target: Path | None) -> list:
    """Shared response budget, native root input, exact ordered preloaded refs."""
    inputs: list = [{'type': 'text', 'text': prompt + '\n\n' + COMMON}]
    if target is not None:
        inputs.append({'type': 'skill', 'name': 'deep-inquiry', 'path': str(target / 'SKILL.md')})
        for name in REFS:
            inputs.append({'type': 'text', 'text': (target / 'references' / name).read_bytes().decode('utf-8')})
    return inputs


def verify_delivery(capture: Capture, inputs: list, target: Path | None) -> None:
    texts = capture.delivered_user_text
    if not texts or not texts[0].startswith('<environment_context>\n') or not texts[0].rstrip().endswith('</environment_context>') or texts[0].count('<environment_context>') != 1 or texts[0].count('</environment_context>') != 1:
        raise RunnerError('known host user prefix missing', 'delivery_user_prefix')
    if texts.count(inputs[0]['text']) != 1 or len(texts) < 2 or texts[1] != inputs[0]['text']:
        raise RunnerError('task input readback mismatch', 'delivery_task')
    if target is None:
        if len(texts) != 2:
            raise RunnerError('baseline user sequence mismatch', 'delivery_baseline_sequence')
        return
    root_text = (target / 'SKILL.md').read_bytes().decode('utf-8')
    expansion = f'<skill>\n<name>deep-inquiry:deep-inquiry</name>\n<path>{target / "SKILL.md"}</path>\n' + root_text + '\n</skill>'
    roots = [index for index, text in enumerate(texts) if text.startswith('<skill>')]
    if len(roots) != 1 or texts[roots[0]] != expansion:
        raise RunnerError('native root expansion readback mismatch', 'delivery_native_root')
    positions = []
    for entry in inputs[2:]:
        matches = [index for index, text in enumerate(texts) if text == entry['text']]
        if len(matches) != 1:
            raise RunnerError('preloaded reference readback mismatch', 'delivery_reference_bytes')
        positions.extend(matches)
    if len(texts) != 6 or positions != [2, 3, 4] or roots != [5]:
        raise RunnerError('native user sequence mismatch', 'delivery_sequence')


def actual_context_hash(texts: list[str], paths: tuple[tuple[Path, str], ...]) -> str:
    if not texts or not all(text.strip() for text in texts):
        raise RunnerError('actual developer instruction readback missing')
    normalized = []
    for text in texts:
        for path, label in paths:
            text = text.replace(str(path), label).replace(str(path).replace(chr(92), '/'), label)
        normalized.append(text)
    return hashlib.sha256(json.dumps(normalized, ensure_ascii=False).encode('utf-8')).hexdigest()


def prepare_output(path: Path) -> None:
    if path.exists():
        raise RunnerError('output already exists; retained evidence cannot be overwritten')
    path.mkdir(parents=True, exist_ok=False)


def read_common_context(path: Path | None, plan: dict, frozen: dict):
    if path is None or not plan.get('common_context_sha256'):
        raise RunnerError('scored runs require frozen cross-arm canary context')
    if digest(path) != plan['common_context_sha256']:
        raise RunnerError('frozen common context file mismatch')
    reference = load(path)
    if reference.get('schema_version') != 1 or reference.get('canary_cross_arm_verified') is not True:
        raise RunnerError('cross-arm canary context proof absent')
    for key in ('suite_hashes', 'skill_hashes'):
        if reference.get(key) != frozen[key]:
            raise RunnerError('common context input freeze mismatch')
    context = reference.get('context', {})
    if set(context) != {'system', 'requirements', 'layers', 'actual_developer_sha256', 'actual_user_prefix_sha256'} or not context['system'] or not all(re.fullmatch(r'[0-9a-f]{64}', context[key]) for key in ('actual_developer_sha256', 'actual_user_prefix_sha256')):
        raise RunnerError('actual common context evidence incomplete')
    return context


def validate_plan(plan: dict, cases: dict):
    if plan.get('schema_version') != 1 or set(plan.get('suite_hashes', {})) != {'cases.json', 'rubrics.json', 'protocol.json'}:
        raise RunnerError('run plan schema or suite freeze incomplete')
    purpose = plan.get('purpose')
    if purpose not in {'canary', 'screening', 'confirmation', 'controls'}:
        raise RunnerError('invalid run plan purpose')
    lookup = {c['id']: (phase, c) for phase in ('calibration', 'confirmation', 'controls') for c in cases[phase]}
    if purpose == 'canary':
        if not isinstance(plan.get('canary_prompt'), str) or not plan['canary_prompt'].strip():
            raise RunnerError('canary requires neutral canary_prompt')
        lookup = {'CANARY': ('controls', {'id': 'CANARY', 'family': 'canary', 'prompt': plan['canary_prompt']})}
    seen: set[str] = set()
    if not isinstance(plan.get('trials'), list) or not plan['trials']:
        raise RunnerError('empty trial plan')
    if purpose == 'canary' and plan['trials'] != [{'case_id': 'CANARY', 'condition': arm, 'repetition': 1} for arm in ('baseline', 'treatment')]:
        raise RunnerError('canary must compare baseline then treatment once each')
    for trial in plan['trials']:
        if set(trial) != {'case_id', 'condition', 'repetition'} or trial['case_id'] not in lookup:
            raise RunnerError('invalid trial case')
        phase, case = lookup[trial['case_id']]
        if purpose == 'screening' and (phase != 'calibration' or trial['condition'] != 'baseline'):
            raise RunnerError('screening is calibration baseline-only')
        if purpose == 'confirmation' and (phase != 'confirmation' or case['family'] not in plan.get('selected_families', [])):
            raise RunnerError('confirmation family is not selected')
        if purpose == 'controls' and phase != 'controls':
            raise RunnerError('controls purpose requires control case')
        limit = 1 if phase == 'controls' else 3
        name = f"{trial['case_id']}-{trial['condition']}-r{trial['repetition']}"
        if trial['condition'] not in {'baseline', 'treatment'} or type(trial['repetition']) is not int or not 1 <= trial['repetition'] <= limit or name in seen:
            raise RunnerError('invalid or duplicate trial slot')
        seen.add(name)
    return lookup


def run_trial(exe: Path, auth: Path, source: Path, case: dict, condition: str, folder: Path, frozen: dict, common: dict, probe_only: bool = False):
    """One fresh trial, cleanup on every exit; retries belong to the run plan."""
    folder.mkdir(parents=True, exist_ok=False)
    capture = Capture()
    report: dict = {'case_id': case['id'], 'condition': condition, 'status': 'not_run', 'backend_model_verified': False, 'model_requested': 'gpt-6-sol', 'effort_requested': 'medium', 'reference_delivery': 'explicit_preloaded', 'comparison_eligible': False, 'allow_provider_model_fallback_requested': False, 'timeout_seconds': 300}
    protected = [auth, *[source / rel for rel in frozen]]
    if (auth.parent / 'config.toml').exists():
        protected.append(auth.parent / 'config.toml')
    before = {}
    host: Host | None = None
    root: Path | None = None
    stage = 'setup'
    report.update(turn_dispatched=False, output_seen=False, process_stopped=True, source_preserved=False)
    try:
        before = {str(p): digest(p) for p in protected}
        with tempfile.TemporaryDirectory(prefix='inquiry-v3-', dir=folder.parent) as disposable:
            root = Path(disposable).resolve()
            profile, home, workspace = (root / name for name in ('profile', 'home', 'workspace'))
            for path in (profile, home, workspace):
                path.mkdir()
            try:
                shutil.copyfile(auth, profile / 'auth.json')
                if digest(auth) != digest(profile / 'auth.json'):
                    raise RunnerError('auth bytewise copy mismatch')
                host = Host(exe, profile, home, workspace, capture)
                if Path(host.initialize()['codexHome']).resolve() != profile:
                    raise RunnerError('profile mismatch')
                stage = 'host_preflight'
                inventory = host.call('skills/list', {'cwds': [str(workspace)], 'forceReload': True})['data'][0]
                if inventory['errors']:
                    raise RunnerError('skill inventory errors')
                for item in inventory['skills']:
                    path = Path(item['path'])
                    if path.is_file():
                        before[str(path)] = digest(path)
                disabled = [x['path'] for x in inventory['skills'] if x['enabled'] and x['scope'] != 'system']
                for path in disabled:
                    if host.call('skills/config/write', {'path': path, 'enabled': False})['effectiveEnabled']:
                        raise RunnerError('inherited skill disable failed')
                host.stop()
                host = Host(exe, profile, home, workspace, capture)
                host.initialize()
                inventory = host.call('skills/list', {'cwds': [str(workspace)], 'forceReload': True})['data'][0]
                active = [x for x in inventory['skills'] if x['enabled']]
                if inventory['errors'] or any(x['scope'] != 'system' for x in active):
                    raise RunnerError('inherited skills remain enabled')
                config = host.call('config/read', {'cwd': str(workspace), 'includeLayers': True})
                if config['config']['model'] != 'gpt-6-sol' or config['config']['model_reasoning_effort'] != 'medium':
                    raise RunnerError('host model configuration mismatch')
                if config['config'].get('instructions') or config['config'].get('developer_instructions'):
                    raise RunnerError('unmatched host instructions')
                hooks = host.call('hooks/list', {'cwds': [str(workspace)]})['data'][0]
                if hooks['hooks'] or hooks['errors'] or host.call('mcpServerStatus/list', {})['data']:
                    raise RunnerError('unexpected hooks or MCP')
                for item in active:
                    path = Path(item['path'])
                    before[str(path)] = digest(path)
                signature = {'system': {x['name']: digest(Path(x['path'])) for x in active}, 'requirements': host.call('configRequirements/read', {}), 'layers': [[x['name']['type'], x['version'], x.get('disabledReason')] for x in config['layers']]}
                if common and signature != {key: common[key] for key in signature}:
                    raise RunnerError('common system/policy/config mismatch')
                common.update(signature)
                save(folder / 'common-context-private.json', signature)
                target = None
                if condition == 'treatment':
                    stage = 'native_discovery'
                    verify_hashes(source, frozen)
                    target = workspace / '.agents/skills/deep-inquiry'
                    shutil.copytree(source, target)
                    verify_hashes(target, frozen)
                    host.call('skills/extraRoots/set', {'extraRoots': [str(workspace / '.agents/skills')]})
                    observed = host.call('skills/list', {'cwds': [str(workspace)], 'forceReload': True})['data'][0]
                    native = [x for x in observed['skills'] if x['enabled'] and Path(x['path']).resolve() == target / 'SKILL.md']
                    if observed['errors'] or len(native) != 1:
                        raise RunnerError('native root not discovered')
                stage = 'thread_contract'
                thread = host.call('thread/start', {'cwd': str(workspace), 'model': 'gpt-6-sol', 'config': {'model_reasoning_effort': 'medium'}, 'allowProviderModelFallback': False, 'approvalPolicy': 'never', 'sandbox': 'read-only', 'ephemeral': True, 'experimentalRawEvents': True})
                if thread['model'] != 'gpt-6-sol' or thread['reasoningEffort'] != 'medium' or thread['instructionSources'] or thread['sandbox']['type'] != 'readOnly' or thread['sandbox']['networkAccess'] or thread['approvalPolicy'] != 'never':
                    raise RunnerError('thread contract mismatch')
                inputs = inputs_for(case['prompt'], target)
                save(folder / 'delivery.json', {'input': inputs, 'root_sha256': frozen['SKILL.md'] if target else None, 'reference_sha256': [frozen['references/' + n] for n in REFS] if target else []})
                report['delivery_sha256'] = digest(folder / 'delivery.json')
                report['status'] = 'ready'
                if not probe_only:
                    stage = 'turn_dispatch'
                    deadline = time.monotonic() + 300
                    result = host.call('turn/start', {'threadId': thread['thread']['id'], 'model': 'gpt-6-sol', 'effort': 'medium', 'input': inputs}, deadline)
                    report['turn_id'] = result['turn']['id']
                    stage = 'turn_completion'
                    while capture.completion is None:
                        host.receive(deadline)
                    stage = 'final_capture'
                    final = capture.final_bytes()
                    (folder / 'final.txt').write_bytes(final)
                    report.update(status='completed', actual_completed_final_preserved=True, final_sha256=digest(folder / 'final.txt'), final_bytes=len(final), host_config_verified=True, native_root_input_delivered=target is not None, preloaded_references_verified=False)
                    stage = 'delivery_readback'
                    verify_delivery(capture, inputs, target)
                    stage = 'common_context'
                    developer_hash = actual_context_hash(capture.delivered_developer_text, ((workspace, '<WORKSPACE>'), (profile, '<PROFILE>'), (home, '<HOME>')))
                    matched_actual_context = 'actual_developer_sha256' in common
                    if 'actual_developer_sha256' in common and common['actual_developer_sha256'] != developer_hash:
                        raise RunnerError('actual shared developer instructions mismatch', 'context_developer_mismatch')
                    prefix_hash = actual_context_hash([capture.delivered_user_text[0]], ((workspace, '<WORKSPACE>'), (profile, '<PROFILE>'), (home, '<HOME>')))
                    matched_user_prefix = 'actual_user_prefix_sha256' in common
                    if matched_user_prefix and common['actual_user_prefix_sha256'] != prefix_hash:
                        raise RunnerError('actual shared host user prefix mismatch', 'context_user_prefix_mismatch')
                    common['actual_developer_sha256'] = developer_hash
                    common['actual_user_prefix_sha256'] = prefix_hash
                    save(folder / 'common-context-private.json', common)
                    report['actual_common_developer_match'] = matched_actual_context
                    report['actual_common_user_prefix_match'] = matched_user_prefix
                    report['actual_context_observed'] = True
                    report.update(native_root_expansion_verified=target is not None, preloaded_references_verified=target is not None, task_input_readback_verified=True)
            except RunnerError as error:
                report.update(status='error', error_type='RunnerError', error_stage=stage, error_contract_code=error.code)
            except (OSError, TimeoutError, KeyError, TypeError, json.JSONDecodeError) as error:
                report.update(status='error', error_type=type(error).__name__, error_stage=stage, error_contract_code='transport_or_setup_error')
            finally:
                report['turn_dispatched'] = host.dispatched if host else False
                report['output_seen'] = capture.output_seen
                try:
                    report['process_stopped'] = host.stop() if host else True
                except (OSError, subprocess.TimeoutExpired) as error:
                    report.update(process_stopped=False, cleanup_error_type=type(error).__name__)
                receipts = []
                for path, expected in before.items():
                    try:
                        observed = digest(Path(path))
                    except OSError:
                        observed = None
                    receipts.append({'path': path, 'before_sha256': expected, 'after_sha256': observed, 'unchanged': observed == expected})
                save(folder / 'source-receipts-private.json', {'publication': 'private_only', 'sources': receipts})
                report['source_preserved'] = all(x['unchanged'] for x in receipts)
                report['tool_attempted'] = capture.tool_attempted
                report['completion_status'] = capture.completion
                save(folder / 'delivered-context-private.json', {'user': capture.delivered_user_text, 'developer': capture.delivered_developer_text})
                save(folder / 'unknown-phase-messages-private.json', capture.unknown_messages)
                save(folder / 'telemetry.json', capture.telemetry)
    except OSError as error:
        report.update(status='error', cleanup_error_type=type(error).__name__, error_stage=stage, error_contract_code='setup_or_cleanup_error')
    report['copied_auth_root_removed'] = root is None or not root.exists()
    if not all(report.get(key) for key in ('copied_auth_root_removed', 'process_stopped', 'source_preserved')):
        report['status'] = 'error'
    save(folder / 'manifest.json', report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate', 'run'))
    parser.add_argument('--suite', type=Path, required=True)
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--exe', type=Path)
    parser.add_argument('--auth', type=Path)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--skill', type=Path, default=ROOT / '.agents/skills/deep-inquiry')
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--probe', action='store_true')
    parser.add_argument('--common-context', type=Path)
    args = parser.parse_args()
    cases = validate_suite(args.suite)
    if args.command == 'validate':
        print(json.dumps({'valid': True, 'case_count': sum(len(cases[x]) for x in ('calibration', 'confirmation', 'controls'))}))
        return 0
    if not (args.execute or args.probe) or not all((args.plan, args.exe, args.auth, args.out)):
        raise RunnerError('run requires --execute --plan --exe --auth --out')
    plan = load(args.plan)
    verify_hashes(args.suite, plan['suite_hashes'])
    verify_hashes(args.skill, plan['skill_hashes'])
    required = {'SKILL.md', *['references/' + n for n in REFS]}
    if not required.issubset(plan['skill_hashes']):
        raise RunnerError('required delivery hashes absent')
    lookup = validate_plan(plan, cases)
    if plan['purpose'] == 'canary':
        if args.common_context:
            raise RunnerError('canary creates its own cross-arm context reference')
        common = {}
    else:
        common = read_common_context(args.common_context, plan, plan)
    prepare_output(args.out)
    slots = [{'case_id': t['case_id'], 'condition': t['condition'], 'repetition': t['repetition'], 'status': 'not_run'} for t in plan['trials']]
    save(args.out / 'run-slots.json', slots)
    for slot_index, trial in enumerate(plan['trials']):
        verify_hashes(args.suite, plan['suite_hashes'])
        verify_hashes(args.skill, plan['skill_hashes'])
        name = f"{trial['case_id']}-{trial['condition']}-r{trial['repetition']}"
        for attempt in (1, 2):
            report = run_trial(args.exe, args.auth, args.skill, lookup[trial['case_id']][1], trial['condition'], args.out / (name + f'-attempt{attempt}'), plan['skill_hashes'], common, args.probe)
            print(json.dumps({k: report[k] for k in ('case_id', 'condition', 'status')}), flush=True)
            if report['status'] in {'completed', 'ready'} or report['turn_dispatched'] or report['output_seen']:
                break
        slots[slot_index].update(status=report['status'], attempt=attempt, final_sha256=report.get('final_sha256'), actual_completed_final_preserved=report.get('actual_completed_final_preserved', False))
        save(args.out / 'run-slots.json', slots)
        if report['status'] not in {'completed', 'ready'}:
            return 1
    if plan['purpose'] == 'canary' and not args.probe:
        if not report.get('actual_common_developer_match') or not report.get('actual_common_user_prefix_match') or not common.get('actual_developer_sha256'):
            raise RunnerError('canary cross-arm actual context equality is unverified')
        reference = {'schema_version': 1, 'canary_cross_arm_verified': True, 'context': common, 'suite_hashes': plan['suite_hashes'], 'skill_hashes': plan['skill_hashes'], 'runner_sha256': digest(Path(__file__)), 'canary_final_sha256': {slot['condition']: slot['final_sha256'] for slot in slots}}
        with (args.out / 'canary-common-context.json').open('x', encoding='utf-8') as stream:
            stream.write(json.dumps(reference, ensure_ascii=False, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
