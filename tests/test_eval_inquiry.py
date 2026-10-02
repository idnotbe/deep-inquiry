"""Behavior checks for the response-only runner; no model calls."""
from pathlib import Path
import json
import queue
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import eval_inquiry as e


class ModelFreeHost:
    def __init__(self, exe, profile, home, workspace, capture):
        self.profile, self.workspace, self.capture = profile, workspace, capture
        self.dispatched = False
        self.copied_files = set()

    def initialize(self):
        return {'codexHome': str(self.profile)}

    def call(self, method, params, deadline=None):
        target = self.workspace / '.agents/skills/deep-inquiry'
        match method:
            case 'skills/list':
                skills = [{'name': 'deep-inquiry', 'path': str(target / 'SKILL.md'), 'enabled': True, 'scope': 'repo'}] if target.exists() else []
                return {'data': [{'skills': skills, 'errors': []}]}
            case 'config/read':
                return {'config': {'model': 'gpt-6-sol', 'model_reasoning_effort': 'medium'}, 'layers': []}
            case 'hooks/list':
                return {'data': [{'hooks': [], 'errors': []}]}
            case 'mcpServerStatus/list':
                return {'data': []}
            case 'configRequirements/read':
                return {}
            case 'skills/extraRoots/set':
                self.copied_files = {path.relative_to(target).as_posix() for path in target.rglob('*') if path.is_file()}
                return {}
            case 'thread/start':
                return {'model': 'gpt-6-sol', 'reasoningEffort': 'medium', 'instructionSources': [], 'sandbox': {'type': 'readOnly', 'networkAccess': False}, 'approvalPolicy': 'never', 'thread': {'id': 'model-free-thread'}}
            case 'turn/start':
                self.dispatched = True
                self.capture.observe({'method': 'item/started', 'params': {'item': {'type': 'commandExecution'}}})
                self.capture.observe({'method': 'item/completed', 'params': {'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': 'preserved\r\n'}}})
                self.capture.observe({'method': 'turn/completed', 'params': {'turn': {'status': 'completed'}}})
                self.capture.delivered_user_text = ['<environment_context>\n</environment_context>', params['input'][0]['text']]
                self.capture.delivered_developer_text = ['fixture developer context']
                return {'turn': {'id': 'model-free-turn'}}
            case _:
                raise AssertionError('Unexpected model-free wire method')

    def stop(self):
        return True


class RunnerTests(unittest.TestCase):
    def test_native_catalog_exposure_is_separate_from_shared_context(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'source'
            source.mkdir()
            (source / 'SKILL.md').write_text('---\nname: deep-inquiry\ndescription: "Exact method description."\n---\n')
            workspace = Path(temp) / 'workspace'
            profile = Path(temp) / 'profile'
            prefix = ('<skills_instructions>\n## Skills\n'
                      'A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. Below is the list of skills that can be used. Each entry includes a name, description, and a short path that can be expanded into an absolute path using the skill roots table.\n'
                      '### Skill roots\n- `r0` = `' + (profile / 'skills/.system').as_posix() + '`\n')
            catalog = ('### Available skills\n- deep-inquiry:imagegen: Shared description. '
                       '(file: r0/imagegen/SKILL.md)\n')
            suffix = '</skills_instructions>'
            mapping = '- `r1` = `' + (workspace / '.agents/skills').as_posix() + '`\n'
            entry = ('- deep-inquiry:deep-inquiry: Exact method description. '
                     '(file: r1/deep-inquiry/SKILL.md)\n')
            paths = ((workspace, '<WORKSPACE>'), (profile, '<PROFILE>'))
            baseline = [prefix + catalog + suffix, 'other shared instructions']
            treatment = [prefix + mapping + catalog + entry + suffix, 'other shared instructions']
            baseline_hash, baseline_proof = e.verified_shared_context(baseline, paths, None, source)
            treatment_hash, treatment_proof = e.verified_shared_context(treatment, paths, workspace / '.agents/skills/deep-inquiry', source)
            self.assertEqual(baseline_hash, treatment_hash)
            self.assertFalse(baseline_proof['present'])
            self.assertTrue(treatment_proof['present'])
            self.assertEqual(baseline_proof['advertisement_sha256'], treatment_proof['advertisement_sha256'])
            for changed in (
                prefix + mapping + catalog + entry + suffix,
                prefix + catalog + entry + suffix,
            ):
                with self.subTest(baseline=changed), self.assertRaises(e.RunnerError):
                    e.verified_shared_context([changed, baseline[1]], paths, None, source)
            for changed in (
                prefix + mapping.replace('.agents/skills', 'wrong') + catalog + entry + suffix,
                prefix + mapping + catalog + entry.replace('Exact method description.', 'Wrong description.') + suffix,
                prefix + mapping + catalog + entry.replace('r1/', 'r0/') + suffix,
                prefix + mapping * 2 + catalog + entry + suffix,
                prefix + mapping + catalog + entry * 2 + suffix,
                prefix + catalog + entry + suffix,
                prefix + mapping + catalog + suffix,
            ):
                with self.subTest(treatment=changed), self.assertRaises(e.RunnerError):
                    e.verified_shared_context([changed, treatment[1]], paths, workspace / '.agents/skills/deep-inquiry', source)
            changed_hash, _ = e.verified_shared_context([baseline[0], 'different shared instructions'], paths, None, source)
            self.assertNotEqual(baseline_hash, changed_hash)
            changed_catalog = baseline[0].replace('Shared description.', 'Different system skill description.')
            changed_hash, _ = e.verified_shared_context([changed_catalog, baseline[1]], paths, None, source)
            self.assertNotEqual(baseline_hash, changed_hash)
            (source / 'SKILL.md').write_text('---\nname: deep-inquiry\ndescription: "Unexpected source description."\n---\n')
            with self.assertRaises(e.RunnerError):
                e.verified_shared_context(treatment, paths, workspace / '.agents/skills/deep-inquiry', source)

    def test_completed_tool_response_when_final_bytes_must_survive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            auth = root / 'auth.json'
            auth.write_bytes(b'fake credential')
            folder = root / 'trial'
            with patch.object(e, 'Host', ModelFreeHost):
                report = e.run_trial(Path(sys.executable), auth, root, {'id': 'C1', 'prompt': 'task'}, 'baseline', folder, {}, {})
            self.assertEqual(report['status'], 'error')
            self.assertEqual(report['error_contract_code'], 'response_tool_attempted')
            self.assertFalse(report['comparison_eligible'])
            self.assertTrue(report['actual_completed_final_preserved'])
            self.assertEqual((folder / 'final.txt').read_bytes(), b'preserved\r\n')

    def test_utf8_when_treatment_asset_is_malformed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'skill'
            (source / 'references').mkdir(parents=True)
            (source / 'SKILL.md').write_bytes(b'root')
            for name in e.REFS:
                (source / 'references' / name).write_bytes(b'valid')
            (source / 'references' / e.REFS[0]).write_bytes(bytes([255]))
            frozen = {path.relative_to(source).as_posix(): e.digest(path) for path in source.rglob('*') if path.is_file()}
            auth = root / 'auth.json'
            auth.write_bytes(b'fake credential')
            folder = root / 'trial'
            with patch.object(e, 'Host', ModelFreeHost):
                report = e.run_trial(Path(sys.executable), auth, source, {'id': 'H1', 'prompt': 'task'}, 'treatment', folder, frozen, {})
            self.assertEqual(report['status'], 'error')
            self.assertEqual(report['error_stage'], 'input_setup')
            self.assertEqual(report['error_contract_code'], 'input_utf8_decode')
            self.assertFalse(report['turn_dispatched'])
            self.assertTrue(report['source_preserved'])
            self.assertTrue((folder / 'manifest.json').exists())
            self.assertTrue((folder / 'source-receipts-private.json').exists())

    def test_treatment_when_unlisted_file_must_not_be_copied(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'skill'
            (source / 'references').mkdir(parents=True)
            (source / 'SKILL.md').write_bytes(b'root')
            for name in e.REFS:
                (source / 'references' / name).write_bytes(b'valid')
            frozen = {path.relative_to(source).as_posix(): e.digest(path) for path in source.rglob('*') if path.is_file()}
            (source / 'unlisted-private-file').write_bytes(b'not delivered')
            auth = root / 'auth.json'
            auth.write_bytes(b'fake credential')
            instances = []
            def host_factory(*args):
                host = ModelFreeHost(*args)
                instances.append(host)
                return host
            with patch.object(e, 'Host', side_effect=host_factory):
                e.run_trial(Path(sys.executable), auth, source, {'id': 'H1', 'prompt': 'task'}, 'treatment', root / 'trial', frozen, {})
            self.assertEqual(instances[-1].copied_files, set(frozen))

    def stage_plan(self, purpose):
        families = [f'f{i}' for i in range(6)]
        cases = {'calibration': [{'id': f'C{i}', 'family': family, 'prompt': 'task'} for i, family in enumerate(families)], 'confirmation': [{'id': f'H{i}', 'family': family, 'prompt': 'task'} for i, family in enumerate(families)], 'controls': [{'id': 'K1', 'family': 'control', 'prompt': 'task'}]}
        phase = {'screening': 'calibration', 'confirmation': 'confirmation', 'controls': 'controls'}[purpose]
        arms = ['baseline'] if purpose == 'screening' else ['baseline', 'treatment']
        repetitions = [1] if purpose == 'controls' else [1, 2, 3]
        plan = {'schema_version': 1, 'purpose': purpose, 'selected_families': families, 'suite_hashes': dict.fromkeys(('cases.json', 'rubrics.json', 'protocol.json'), 'f' * 64), 'trials': [{'case_id': case['id'], 'condition': arm, 'repetition': repetition} for case in cases[phase] for arm in arms for repetition in repetitions]}
        return cases, plan

    def test_stage_when_required_slot_is_missing(self):
        for purpose in ('screening', 'confirmation', 'controls'):
            with self.subTest(purpose=purpose):
                cases, plan = self.stage_plan(purpose)
                plan['trials'].pop()
                with self.assertRaises(e.RunnerError):
                    e.validate_plan(plan, cases)

    def test_confirmation_when_treatment_arm_is_missing(self):
        cases, plan = self.stage_plan('confirmation')
        plan['trials'] = [slot for slot in plan['trials'] if slot['condition'] == 'baseline']
        with self.assertRaises(e.RunnerError):
            e.validate_plan(plan, cases)

    def test_confirmation_when_selected_families_are_invalid(self):
        for selected in (['f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f5'], ['f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'unknown'], ['f0', 'f1', 'f2', 'f3', 'f4']):
            with self.subTest(selected=selected):
                cases, plan = self.stage_plan('confirmation')
                plan['selected_families'] = selected
                with self.assertRaises(e.RunnerError):
                    e.validate_plan(plan, cases)

    def test_stage_when_all_required_slots_are_present(self):
        for purpose in ('screening', 'confirmation', 'controls'):
            cases, plan = self.stage_plan(purpose)
            e.validate_plan(plan, cases)

    def test_output_when_public_destination_is_requested(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            destination = root / 'evals/v3/reports/new-run'
            with patch.object(e, 'ROOT', root), self.assertRaises(e.RunnerError):
                e.prepare_output(destination)
            self.assertFalse(destination.exists())

    def test_output_when_private_destination_is_requested(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(e, 'ROOT', root):
                for name in ('temp', 'local-runs'):
                    e.prepare_output(root / name / 'new-run')
                    self.assertTrue((root / name / 'new-run').is_dir())

    def test_delivery_when_native_root_has_extra_instructions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'references').mkdir()
            (root / 'SKILL.md').write_bytes(b'root bytes\r\n')
            for index, name in enumerate(e.REFS):
                (root / 'references' / name).write_bytes(f'ref-{index}'.encode())
            inputs = e.inputs_for('task', root)
            expansion = f'<skill>\n<name>deep-inquiry:deep-inquiry</name>\n<path>{root / "SKILL.md"}</path>\nroot bytes\r\nextra instructions\n</skill>'
            capture = e.Capture(delivered_user_text=['<environment_context>\n</environment_context>', inputs[0]['text'], *[x['text'] for x in inputs[2:]], expansion])
            with self.assertRaises(e.RunnerError):
                e.verify_delivery(capture, inputs, root)

    def test_delivery_when_native_root_body_is_duplicated(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'references').mkdir()
            (root / 'SKILL.md').write_bytes(b'root bytes\r\n')
            for index, name in enumerate(e.REFS):
                (root / 'references' / name).write_bytes(f'ref-{index}'.encode())
            inputs = e.inputs_for('task', root)
            expansion = f'<skill>\n<name>deep-inquiry:deep-inquiry</name>\n<path>{root / "SKILL.md"}</path>\nroot bytes\r\nroot bytes\r\n\n</skill>'
            capture = e.Capture(delivered_user_text=['<environment_context>\n</environment_context>', inputs[0]['text'], *[x['text'] for x in inputs[2:]], expansion])
            with self.assertRaises(e.RunnerError):
                e.verify_delivery(capture, inputs, root)

    def test_delivery_when_actual_native_contract_is_replayed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'references').mkdir()
            (root / 'SKILL.md').write_bytes(b'root bytes\r\n')
            for index, name in enumerate(e.REFS):
                (root / 'references' / name).write_bytes(f'ref-{index}\r\n'.encode())
            inputs = e.inputs_for('task', root)
            prefix = '<environment_context>\n<cwd>workspace</cwd>\n</environment_context>'
            expansion = f'<skill>\n<name>deep-inquiry:deep-inquiry</name>\n<path>{root / "SKILL.md"}</path>\nroot bytes\r\n\n</skill>'
            capture = e.Capture(delivered_user_text=[prefix, inputs[0]['text'], *[x['text'] for x in inputs[2:]], expansion])
            e.verify_delivery(capture, inputs, root)

    def test_delivery_when_arbitrary_user_extra_precedes_task(self):
        capture = e.Capture(delivered_user_text=['arbitrary hint', e.inputs_for('task', None)[0]['text']])
        with self.assertRaises(e.RunnerError) as result:
            e.verify_delivery(capture, e.inputs_for('task', None), None)
        self.assertEqual(result.exception.code, 'delivery_user_prefix')

    def test_delivery_when_extra_user_item_follows_baseline_task(self):
        inputs = e.inputs_for('task', None)
        capture = e.Capture(delivered_user_text=['<environment_context>\n</environment_context>', inputs[0]['text'], 'extra'])
        with self.assertRaises(e.RunnerError):
            e.verify_delivery(capture, inputs, None)

    def test_context_reference_when_verified_file_is_read_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'common.json'
            context = {'system': {'skill': 'a' * 64}, 'requirements': {}, 'layers': [], 'actual_developer_sha256': 'b' * 64, 'actual_user_prefix_sha256': 'e' * 64}
            frozen = {'suite_hashes': {'cases.json': 'c' * 64}, 'skill_hashes': {'SKILL.md': 'd' * 64}}
            path.write_text(json.dumps({'schema_version': 1, 'canary_cross_arm_verified': True, 'context': context, 'runner_sha256': e.digest(Path(e.__file__)), **frozen}))
            original = path.read_bytes()
            observed = e.read_common_context(path, {'common_context_sha256': e.digest(path)}, frozen)
            self.assertEqual(observed, context)
            self.assertEqual(path.read_bytes(), original)

    def test_context_reference_when_runner_hash_is_missing_or_wrong(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'common.json'
            frozen = {'suite_hashes': {}, 'skill_hashes': {}}
            context = {'system': {'skill': 'a' * 64}, 'requirements': {}, 'layers': [], 'actual_developer_sha256': 'b' * 64, 'actual_user_prefix_sha256': 'e' * 64}
            reference = {'schema_version': 1, 'canary_cross_arm_verified': True, 'context': context, **frozen}
            for runner_hash in (None, '0' * 64):
                with self.subTest(runner_hash=runner_hash):
                    if runner_hash is not None:
                        reference['runner_sha256'] = runner_hash
                    path.write_text(json.dumps(reference))
                    with self.assertRaises(e.RunnerError) as result:
                        e.read_common_context(path, {'common_context_sha256': e.digest(path)}, frozen)
                    self.assertEqual(result.exception.code, 'context_runner_mismatch')

    def test_context_when_only_trial_paths_differ(self):
        first = e.actual_context_hash(['instructions at C:/first/workspace'], ((Path('C:/first/workspace'), '<WORKSPACE>'),))
        second = e.actual_context_hash(['instructions at C:/second/workspace'], ((Path('C:/second/workspace'), '<WORKSPACE>'),))
        self.assertEqual(first, second)

    def test_context_reference_when_scored_run_has_no_frozen_reference(self):
        with self.assertRaises(e.RunnerError):
            e.read_common_context(None, {}, {'suite_hashes': {}, 'skill_hashes': {}})

    def test_context_reference_when_file_hash_mismatches(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'common.json'
            path.write_text('{}')
            with self.assertRaises(e.RunnerError):
                e.read_common_context(path, {'common_context_sha256': 'f' * 64}, {'suite_hashes': {}, 'skill_hashes': {}})

    def test_context_reference_when_cross_arm_proof_is_absent(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'common.json'
            path.write_text(json.dumps({'schema_version': 1, 'canary_cross_arm_verified': False}))
            with self.assertRaises(e.RunnerError):
                e.read_common_context(path, {'common_context_sha256': e.digest(path)}, {'suite_hashes': {}, 'skill_hashes': {}})

    def test_tool_attempt_when_started_then_turn_fails(self):
        capture = e.Capture()
        capture.observe({'method': 'item/started', 'params': {'item': {'type': 'commandExecution'}}})
        capture.observe({'method': 'turn/completed', 'params': {'turn': {'status': 'failed'}}})
        self.assertTrue(capture.tool_attempted)

    def test_tool_attempt_when_raw_call_has_no_completed_item(self):
        capture = e.Capture()
        capture.observe({'method': 'rawResponseItem/completed', 'params': {'item': {'type': 'function_call', 'name': 'exec_command'}}})
        self.assertTrue(capture.tool_attempted)

    def test_context_when_no_actual_developer_input(self):
        with self.assertRaises(e.RunnerError):
            e.actual_context_hash([], ())

    def test_output_when_directory_already_exists(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            receipt = root / 'run-slots.json'
            receipt.write_bytes(b'original evidence')
            with self.assertRaises(e.RunnerError):
                e.prepare_output(root)
            self.assertEqual(receipt.read_bytes(), b'original evidence')

    def test_manifest_when_disposable_setup_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source'
            source.mkdir()
            auth = root / 'auth.json'
            auth.write_bytes(b'fake credential')
            folder = root / 'trial'
            with patch.object(e.tempfile, 'TemporaryDirectory', side_effect=OSError('setup unavailable')):
                report = e.run_trial(Path(sys.executable), auth, source, {'id': 'C1', 'prompt': 'task'}, 'baseline', folder, {}, {})
            self.assertEqual(report['status'], 'error')
            self.assertFalse(report['turn_dispatched'])
            self.assertTrue((folder / 'manifest.json').exists())

    def test_delivery_when_root_precedes_references(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'references').mkdir()
            (root / 'SKILL.md').write_bytes(b'root bytes')
            for index, name in enumerate(e.REFS):
                (root / 'references' / name).write_bytes(f'ref-{index}'.encode())
            inputs = e.inputs_for('task', root)
            expansion = f'<skill>\n<name>deep-inquiry:deep-inquiry</name>\n<path>{root / "SKILL.md"}</path>\nroot bytes\n</skill>'
            capture = e.Capture(delivered_user_text=['<environment_context>\n</environment_context>', inputs[0]['text'], expansion, *[x['text'] for x in inputs[2:]]])
            with self.assertRaises(e.RunnerError):
                e.verify_delivery(capture, inputs, root)

    def test_delivery_when_native_root_is_not_expanded(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'references').mkdir()
            (root / 'SKILL.md').write_bytes(b'root bytes\r\n')
            for index, name in enumerate(e.REFS):
                (root / 'references' / name).write_bytes(f'ref-{index}'.encode())
            inputs = e.inputs_for('task', root)
            capture = e.Capture(delivered_user_text=['<environment_context>\n</environment_context>', inputs[0]['text'], *[x['text'] for x in inputs[2:]]])
            with self.assertRaises(e.RunnerError):
                e.verify_delivery(capture, inputs, root)

    def test_delivery_when_expansion_and_references_match(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'references').mkdir()
            (root / 'SKILL.md').write_bytes(b'root bytes\r\n')
            for index, name in enumerate(e.REFS):
                (root / 'references' / name).write_bytes(f'ref-{index}'.encode())
            inputs = e.inputs_for('task', root)
            expansion = f'<skill>\n<name>deep-inquiry:deep-inquiry</name>\n<path>{root / "SKILL.md"}</path>\nroot bytes\r\n\n</skill>'
            capture = e.Capture(delivered_user_text=['<environment_context>\n</environment_context>', inputs[0]['text'], *[x['text'] for x in inputs[2:]], expansion])
            e.verify_delivery(capture, inputs, root)

    def test_cleanup_when_initialization_times_out(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source'
            source.mkdir()
            (source / 'SKILL.md').write_bytes(b'root')
            auth = root / 'auth.json'
            auth.write_bytes(b'not-a-real-credential')
            folder = root / 'trial'
            with patch.object(e.Host, 'initialize', side_effect=TimeoutError('setup')):
                report = e.run_trial(Path(sys.executable), auth, source, {'id': 'C1', 'prompt': 'task'}, 'baseline', folder, {'SKILL.md': e.digest(source / 'SKILL.md')}, {})
            self.assertEqual(report['status'], 'error')
            self.assertFalse(report['turn_dispatched'])
            self.assertTrue(report['process_stopped'])
            self.assertTrue(report['copied_auth_root_removed'])
            self.assertEqual(auth.read_bytes(), b'not-a-real-credential')
            self.assertTrue((folder / 'manifest.json').exists())

    def test_capture_when_raw_hidden_reasoning_arrives(self):
        capture = e.Capture()
        capture.observe({'method': 'rawResponseItem/completed', 'params': {'item': {'type': 'reasoning', 'content': 'private'}}})
        self.assertEqual(capture.telemetry, [])
        self.assertEqual(capture.delivered_user_text, [])

    def test_plan_when_screening_requests_treatment(self):
        cases = {'calibration': [{'id': 'C1', 'family': 'f', 'prompt': 'p'}], 'confirmation': [], 'controls': []}
        plan = {'schema_version': 1, 'purpose': 'screening', 'suite_hashes': dict.fromkeys(('cases.json', 'rubrics.json', 'protocol.json'), 'f' * 64), 'trials': [{'case_id': 'C1', 'condition': 'treatment', 'repetition': 1}]}
        with self.assertRaises(e.RunnerError):
            e.validate_plan(plan, cases)

    def test_plan_when_confirmation_family_unselected(self):
        cases = {'calibration': [], 'confirmation': [{'id': 'H1', 'family': 'f', 'prompt': 'p'}], 'controls': []}
        plan = {'schema_version': 1, 'purpose': 'confirmation', 'selected_families': ['other'], 'suite_hashes': dict.fromkeys(('cases.json', 'rubrics.json', 'protocol.json'), 'f' * 64), 'trials': [{'case_id': 'H1', 'condition': 'baseline', 'repetition': 1}]}
        with self.assertRaises(e.RunnerError):
            e.validate_plan(plan, cases)

    def test_delivery_when_treatment_has_ordered_reference_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'references').mkdir()
            for index, name in enumerate(e.REFS):
                (root / 'references' / name).write_bytes(f'ref-{index}\r\n'.encode())
            inputs = e.inputs_for('task', root)
            self.assertEqual([x['type'] for x in inputs], ['text', 'skill', 'text', 'text', 'text'])
            self.assertEqual([x['text'].encode() for x in inputs[2:]], [f'ref-{i}\r\n'.encode() for i in range(3)])

    def test_source_hash_when_frozen_bytes_change(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'SKILL.md'
            source.write_bytes(b'before')
            frozen = {'SKILL.md': e.digest(source)}
            source.write_bytes(b'after')
            with self.assertRaises(e.RunnerError):
                e.verify_hashes(root, frozen)

    def test_transport_when_deadline_expires(self):
        host = e.Host.__new__(e.Host)
        host.lines = queue.Queue()
        host.capture = e.Capture()
        with self.assertRaises(TimeoutError):
            host.receive(time.monotonic() - 1)

    def test_cleanup_when_owned_process_running(self):
        host = e.Host.__new__(e.Host)
        host.proc = subprocess.Popen([sys.executable, '-c', 'import sys;sys.stdin.read()'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        self.assertTrue(host.stop())
        assert host.proc.stdin is not None
        self.assertTrue(host.proc.stdin.closed)
        assert host.proc.stdout is not None
        self.assertTrue(host.proc.stdout.closed)

    def test_transport_when_model_reroutes(self):
        capture = e.Capture()
        with self.assertRaises(e.RunnerError):
            capture.observe({'method': 'model/rerouted', 'params': {}})

    def test_capture_when_tool_execution_occurs(self):
        capture = e.Capture()
        capture.observe({'method': 'item/completed', 'params': {'item': {'type': 'commandExecution'}}})
        self.assertTrue(capture.tool_attempted)

    def test_schema_when_duplicate_case_id(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cases = {'schema_version': 1, 'calibration': [{'id': 'C1', 'family': 'f', 'prompt': 'p'}], 'confirmation': [{'id': 'C1', 'family': 'f', 'prompt': 'p'}], 'controls': [{'id': 'K1', 'family': 'f', 'prompt': 'p'}]}
            (root / 'cases.json').write_text(json.dumps(cases))
            (root / 'rubrics.json').write_text(json.dumps({'schema_version': 1, 'cases': {}}))
            with self.assertRaises(e.RunnerError):
                e.validate_suite(root)

    def test_schema_when_phase_wrong_shape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'cases.json').write_text(json.dumps({'schema_version': 1, 'calibration': 'bad', 'confirmation': [], 'controls': []}))
            (root / 'rubrics.json').write_text(json.dumps({'schema_version': 1, 'cases': {}}))
            with self.assertRaises(e.RunnerError):
                e.validate_suite(root)

    def test_final_capture_when_commentary_precedes_final(self):
        # Given completed commentary and final messages.
        capture = e.Capture()
        capture.observe({'method': 'item/completed', 'params': {'item': {'type': 'agentMessage', 'phase': 'commentary', 'text': 'progress'}}})
        capture.observe({'method': 'item/completed', 'params': {'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': '완료\r\n'}}})
        # When the turn completes.
        capture.observe({'method': 'turn/completed', 'params': {'turn': {'status': 'completed'}}})
        # Then exact final bytes are retained.
        self.assertEqual(capture.final_bytes(), '완료\r\n'.encode())

    def test_failed_turn_when_final_item_exists(self):
        # Given a final item followed by failed completion.
        capture = e.Capture()
        capture.observe({'method': 'item/completed', 'params': {'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': 'partial'}}})
        capture.observe({'method': 'turn/completed', 'params': {'turn': {'status': 'failed'}}})
        # When consuming final output, then failure remains failure.
        with self.assertRaises(e.RunnerError):
            capture.final_bytes()


if __name__ == '__main__':
    unittest.main()
