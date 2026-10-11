"""Behavior checks for the response-only runner; no model calls."""
from pathlib import Path
import io
import json
import queue
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import Mock, call, patch

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


class DeadlineTests(unittest.TestCase):
    def test_receive_rejects_queued_final_when_deadline_reached(self):
        for now in (10.0, 11.0):
            with self.subTest(now=now):
                host = e.Host.__new__(e.Host)
                host.capture, host.lines = e.Capture(), queue.Queue()
                host.lines.put(json.dumps({'method': 'item/completed', 'params': {'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': 'synthetic'}}}))
                with patch.object(e.time, 'monotonic', return_value=now), patch.object(e.json, 'loads', wraps=e.json.loads) as decode, patch.object(e.Capture, 'observe', wraps=host.capture.observe) as observe:
                    with self.assertRaisesRegex(TimeoutError, '^app-server deadline$'):
                        host.receive(10.0)
                self.assertEqual(host.lines.qsize(), 1)
                decode.assert_not_called()
                observe.assert_not_called()
                self.assertEqual(host.capture.messages, [])

    def test_receive_rejects_final_when_queue_returns_at_or_after_deadline(self):
        for returned_at in (10.0, 11.0):
            with self.subTest(returned_at=returned_at):
                host = e.Host.__new__(e.Host)
                host.capture, host.lines = e.Capture(), queue.Queue()
                host.lines.put(json.dumps({'method': 'item/completed', 'params': {'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': 'synthetic'}}}))
                with patch.object(e.time, 'monotonic', side_effect=(9.0, returned_at)), patch.object(host.lines, 'get', wraps=host.lines.get) as dequeue, patch.object(e.json, 'loads', wraps=e.json.loads) as decode, patch.object(e.Capture, 'observe', wraps=host.capture.observe) as observe:
                    with self.assertRaisesRegex(TimeoutError, '^app-server deadline$'):
                        host.receive(10.0)
                dequeue.assert_called_once_with(timeout=1.0)
                self.assertTrue(host.lines.empty())
                decode.assert_not_called()
                observe.assert_not_called()
                self.assertEqual(host.capture.messages, [])

    def test_receive_accepts_in_time_final_with_actual_remaining_timeout(self):
        host = e.Host.__new__(e.Host)
        host.capture, host.lines = e.Capture(), queue.Queue()
        event = {'method': 'item/completed', 'params': {'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': 'synthetic'}}}
        host.lines.put(json.dumps(event))
        with patch.object(e.time, 'monotonic', side_effect=(9.9995, 9.9999)), patch.object(host.lines, 'get', wraps=host.lines.get) as dequeue:
            self.assertEqual(host.receive(10.0), event)
        dequeue.assert_called_once_with(timeout=10.0 - 9.9995)
        self.assertEqual(host.capture.messages, ['synthetic'])

    def test_receive_preserves_empty_queue_timeout_cause(self):
        host = e.Host.__new__(e.Host)
        host.capture, host.lines = e.Capture(), queue.Queue()
        empty = queue.Empty()
        with patch.object(e.time, 'monotonic', return_value=9.0), patch.object(host.lines, 'get', side_effect=empty):
            with self.assertRaisesRegex(TimeoutError, '^app-server deadline$') as result:
                host.receive(10.0)
        self.assertIs(result.exception.__cause__, empty)


class CleanupBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.host = e.Host.__new__(e.Host)
        self.host.proc = Mock(spec=subprocess.Popen, pid=123, stdin=Mock(spec=io.StringIO), stdout=Mock(spec=io.StringIO))
        self.host.proc.poll.return_value = None

    def test_cleanup_boundary_taskkill_timeout_or_nonzero_falls_back_to_owned_root(self):
        for timeout in (True, False):
            with self.subTest(timeout=timeout):
                self.host.proc.reset_mock()
                self.host.proc.poll.side_effect = (None, None, 0)
                with patch.object(e.os, 'name', 'nt'), patch.object(e.subprocess, 'run', side_effect=subprocess.TimeoutExpired('taskkill', 10) if timeout else None, return_value=subprocess.CompletedProcess([], 1)) as taskkill:
                    self.assertTrue(self.host.stop())
                taskkill.assert_called_once_with(['taskkill', '/PID', '123', '/T', '/F'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10, check=False)
                self.host.proc.terminate.assert_called_once_with()
                self.host.proc.wait.assert_called_once_with(timeout=10)
                self.host.proc.kill.assert_not_called()
                self.host.proc.stdin.close.assert_called_once_with()
                self.host.proc.stdout.close.assert_called_once_with()

    def test_cleanup_boundary_taskkill_timeout_rechecks_root_liveness(self):
        self.host.proc.poll.side_effect = (None, 0, 0)
        with patch.object(e.os, 'name', 'nt'), patch.object(e.subprocess, 'run', side_effect=subprocess.TimeoutExpired('taskkill', 10)):
            self.assertTrue(self.host.stop())
        self.host.proc.terminate.assert_not_called()
        self.host.proc.wait.assert_called_once_with(timeout=10)

    def test_cleanup_boundary_terminate_failure_propagates_and_closes_both_pipes(self):
        failure = OSError('synthetic terminate failure')
        self.host.proc.terminate.side_effect = failure
        with patch.object(e.os, 'name', 'nt'), patch.object(e.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1)):
            with self.assertRaises(OSError) as result:
                self.host.stop()
        self.assertIs(result.exception, failure)
        self.host.proc.stdin.close.assert_called_once_with()
        self.host.proc.stdout.close.assert_called_once_with()
        self.host.proc.wait.assert_not_called()

    def test_cleanup_boundary_wait_timeout_escalates_with_exact_bounded_waits(self):
        self.host.proc.poll.side_effect = (None, None, 0)
        self.host.proc.wait.side_effect = (subprocess.TimeoutExpired('synthetic child', 10), 0)
        with patch.object(e.os, 'name', 'nt'), patch.object(e.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1)):
            self.assertTrue(self.host.stop())
        self.assertEqual(self.host.proc.wait.call_args_list, [call(timeout=10), call(timeout=10)])
        self.assertEqual(self.host.proc.method_calls, [call.poll(), call.poll(), call.terminate(), call.wait(timeout=10), call.kill(), call.wait(timeout=10), call.stdin.close(), call.stdout.close(), call.poll()])

    def test_cleanup_boundary_final_wait_failure_propagates_and_closes_both_pipes(self):
        failure = subprocess.TimeoutExpired('synthetic child final wait', 10)
        self.host.proc.wait.side_effect = (subprocess.TimeoutExpired('synthetic child', 10), failure)
        with patch.object(e.os, 'name', 'nt'), patch.object(e.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1)):
            with self.assertRaises(subprocess.TimeoutExpired) as result:
                self.host.stop()
        self.assertIs(result.exception, failure)
        self.assertEqual(self.host.proc.wait.call_args_list, [call(timeout=10), call(timeout=10)])
        self.host.proc.kill.assert_called_once_with()
        self.host.proc.stdin.close.assert_called_once_with()
        self.host.proc.stdout.close.assert_called_once_with()

    def test_cleanup_boundary_first_close_failure_still_attempts_second_close(self):
        self.host.proc.poll.return_value = 0
        failure = OSError('synthetic first close failure')
        self.host.proc.stdin.close.side_effect = failure
        with self.assertRaises(OSError) as result:
            self.host.stop()
        self.assertIs(result.exception, failure)
        self.host.proc.stdout.close.assert_called_once_with()

    def test_cleanup_boundary_overlapping_failures_preserve_chained_context(self):
        terminate_failure = OSError('synthetic terminate failure')
        first_close_failure = ValueError('synthetic first close failure')
        second_close_failure = RuntimeError('synthetic second close failure')
        self.host.proc.terminate.side_effect = terminate_failure
        self.host.proc.stdin.close.side_effect = first_close_failure
        self.host.proc.stdout.close.side_effect = second_close_failure
        with patch.object(e.os, 'name', 'nt'), patch.object(e.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1)):
            with self.assertRaises(RuntimeError) as result:
                self.host.stop()
        self.assertIs(result.exception, second_close_failure)
        self.assertIs(result.exception.__context__, first_close_failure)
        self.assertIs(first_close_failure.__context__, terminate_failure)
        self.host.proc.stdin.close.assert_called_once_with()
        self.host.proc.stdout.close.assert_called_once_with()

    def test_cleanup_boundary_non_timeout_taskkill_error_propagates(self):
        failure = OSError('synthetic taskkill failure')
        with patch.object(e.os, 'name', 'nt'), patch.object(e.subprocess, 'run', side_effect=failure):
            with self.assertRaises(OSError) as result:
                self.host.stop()
        self.assertIs(result.exception, failure)
        self.host.proc.terminate.assert_not_called()
        self.host.proc.stdin.close.assert_called_once_with()
        self.host.proc.stdout.close.assert_called_once_with()


class NativeErrorTests(unittest.TestCase):
    def test_retryable_error_continues_same_capture_request_and_deadline(self):
        host = e.Host.__new__(e.Host)
        host.capture, host.number, host.dispatched = e.Capture(), 0, False
        host.stdin, host.lines = io.StringIO(), queue.Queue()
        events = [
            {'method': 'error', 'params': {'willRetry': True, 'error': {'codexErrorInfo': 'serverOverloaded'}}},
            {'id': 1, 'result': {'turn': {'id': 'fixture-turn'}}},
            {'method': 'item/completed', 'params': {'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': 'original\r\n'}}},
            {'method': 'turn/completed', 'params': {'turn': {'status': 'completed'}}},
        ]
        for event in events:
            host.lines.put(json.dumps(event))
        deadline = time.monotonic() + 5
        with patch.object(host, 'receive', wraps=host.receive) as receive:
            host.call('turn/start', {}, deadline)
            while host.capture.completion is None:
                host.receive(deadline)
        self.assertEqual(host.capture.final_bytes(), b'original\r\n')
        self.assertEqual(len(host.stdin.getvalue().splitlines()), 1)
        self.assertEqual(host.number, 1)
        self.assertTrue(all(call.args == (deadline,) for call in receive.call_args_list))
        self.assertEqual(host.capture.telemetry[0], {'method': 'error', 'will_retry': True, 'error_info': 'serverOverloaded'})

    def test_fatal_or_malformed_retry_flags_remain_rejected(self):
        for params in ({}, {'willRetry': False}, {'willRetry': None}, {'willRetry': 1}, {'willRetry': 'true'}, {'willRetry': []}):
            with self.subTest(params=params):
                capture = e.Capture()
                with self.assertRaises(e.RunnerError) as result:
                    capture.observe({'method': 'error', 'params': params})
                self.assertEqual(result.exception.code, 'host_error_notification')
                self.assertEqual(capture.telemetry[0]['error_info'], 'unknown')
                self.assertIs(capture.telemetry[0]['will_retry'], False if params.get('willRetry') is False else None)

    def test_failure_paths_have_fixed_codes_without_payload(self):
        for method, code in (('model/rerouted', 'model_rerouted'), ('turn/failed', 'host_turn_failed')):
            with self.subTest(method=method):
                capture = e.Capture()
                with self.assertRaises(e.RunnerError) as result:
                    capture.observe({'method': method, 'params': {'willRetry': True, 'message': 'SENTINEL', 'model': 'SENTINEL'}})
                self.assertEqual(result.exception.code, code)
                self.assertNotIn('SENTINEL', json.dumps(capture.telemetry) + str(result.exception))
                self.assertEqual(capture.telemetry[0]['method'], method)

    def test_unexpected_request_is_rejected_before_observation(self):
        host = e.Host.__new__(e.Host)
        host.capture, host.lines = e.Capture(), queue.Queue()
        for method in ('SENTINEL', 'item/completed'):
            with self.subTest(method=method):
                host.lines.put(json.dumps({'id': 'SENTINEL', 'method': method, 'params': {'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': 'SENTINEL'}}}))
                with self.assertRaises(e.RunnerError) as result:
                    host.receive(time.monotonic() + 5)
                self.assertEqual(result.exception.code, 'unexpected_server_request')
        self.assertEqual(host.capture.messages, [])
        self.assertEqual(host.capture.telemetry, [{'method': 'unexpected_server_request'}] * 2)

    def test_error_info_allowlist_does_not_retain_arbitrary_fields(self):
        units = ('contextWindowExceeded', 'sessionBudgetExceeded', 'usageLimitExceeded', 'rateLimitExceeded', 'flexUnavailable', 'serverOverloaded', 'cyberPolicy', 'misalignmentPolicyViolation', 'tooManyDenials', 'internalServerError', 'unauthorized', 'badRequest', 'threadRollbackFailed', 'sandboxError', 'other')
        for info in units:
            with self.subTest(info=info):
                capture = e.Capture()
                capture.observe({'method': 'error', 'params': {'willRetry': True, 'threadId': 'SENTINEL', 'error': {'codexErrorInfo': info, 'message': 'SENTINEL', 'additionalDetails': 'https://SENTINEL'}}})
                self.assertEqual(capture.telemetry, [{'method': 'error', 'will_retry': True, 'error_info': info}])

    def test_http_error_info_requires_strict_status_and_shape(self):
        for tag in ('httpConnectionFailed', 'responseStreamConnectionFailed', 'responseStreamDisconnected', 'responseTooManyFailedAttempts'):
            for status in (None, 100, 429, 599, True, False, 99, 600, 429.0, 'SENTINEL'):
                with self.subTest(tag=tag, status=status):
                    capture = e.Capture()
                    capture.observe({'method': 'error', 'params': {'willRetry': True, 'error': {'codexErrorInfo': {tag: {'httpStatusCode': status}}}}})
                    valid = status is None or type(status) is int and 100 <= status <= 599
                    expected = {'method': 'error', 'will_retry': True, 'error_info': tag if valid else 'unknown'}
                    if valid:
                        expected['http_status_code'] = status
                    self.assertEqual(capture.telemetry, [expected])

    def test_unknown_and_malformed_error_info_is_fixed_unknown(self):
        for info in ('SENTINEL', None, [], 1, {'SENTINEL': 'https://SENTINEL'}, {'httpConnectionFailed': {}}, {'httpConnectionFailed': {'httpStatusCode': 429, 'SENTINEL': 'SENTINEL'}}, {'other': {}}, {'httpConnectionFailed': {'httpStatusCode': 429}, 'SENTINEL': {}}, {'httpConnectionFailed': 'SENTINEL'}):
            with self.subTest(info=info):
                capture = e.Capture()
                capture.observe({'method': 'error', 'params': {'willRetry': True, 'error': {'codexErrorInfo': info, 'errorInfo': 'unauthorized', 'message': 'SENTINEL'}}})
                self.assertEqual(capture.telemetry, [{'method': 'error', 'will_retry': True, 'error_info': 'unknown'}])

    def test_failed_and_interrupted_completion_retains_only_safe_error(self):
        for status in ('failed', 'interrupted'):
            with self.subTest(status=status):
                capture = e.Capture()
                capture.observe({'method': 'error', 'params': {'willRetry': True}})
                capture.observe({'method': 'item/completed', 'params': {'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': 'partial'}}})
                capture.observe({'method': 'turn/completed', 'params': {'turn': {'status': status, 'id': 'SENTINEL', 'error': {'message': 'SENTINEL', 'codexErrorInfo': 'unauthorized'}}}})
                self.assertEqual(capture.telemetry[-1], {'method': 'turn/completed', 'status': status, 'error_info': 'unauthorized'})
                with self.assertRaises(e.RunnerError):
                    capture.final_bytes()


class RunnerTests(unittest.TestCase):
    def test_main_setup_retry_when_cleanup_guards_are_not_proven(self):
        # Given real frozen inputs and reports at the external run_trial seam.
        clean = {'status': 'error', 'turn_dispatched': False, 'output_seen': False,
                 'source_preserved': True, 'process_stopped': True, 'copied_auth_root_removed': True}
        ready = {**clean, 'status': 'ready'}
        stopped = (1, ['baseline-r1-attempt1'], ['error', 'not_run'], [1, None])
        scenarios = []
        for guard in ('source_preserved', 'process_stopped', 'copied_auth_root_removed'):
            for value in (False, None, 1, 1.0, 'true', 'unknown', [], {}):
                scenarios.append(({**clean, guard: value}, ready, stopped))
            missing = dict(clean)
            del missing[guard]
            scenarios.append((missing, ready, stopped))
        for flag in ('turn_dispatched', 'output_seen'):
            scenarios.append(({**clean, flag: True}, ready, stopped))
        scenarios.extend([
            (clean, ready, (0, ['baseline-r1-attempt1', 'baseline-r1-attempt2', 'treatment-r1-attempt1'], ['ready', 'ready'], [2, 1])),
            (clean, clean, (1, ['baseline-r1-attempt1', 'baseline-r1-attempt2'], ['error', 'not_run'], [2, None])),
            (ready, ready, (0, ['baseline-r1-attempt1', 'treatment-r1-attempt1'], ['ready', 'ready'], [1, 1])),
            ({**ready, 'status': 'completed'}, ready, (0, ['baseline-r1-attempt1', 'treatment-r1-attempt1'], ['completed', 'ready'], [1, 1])),
        ])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            suite, source = root / 'suite', root / 'skill'
            suite.mkdir()
            (source / 'references').mkdir(parents=True)
            cases = {'schema_version': 1, **{phase: [{'id': case_id, 'family': 'fixture', 'prompt': 'task'}]
                     for phase, case_id in (('calibration', 'C1'), ('confirmation', 'H1'), ('controls', 'K1'))}}
            rubric = {'dimensions': [{'id': str(i), 'zero': 'zero', 'one': 'one', 'two': 'two'} for i in range(5)], 'critical_failures': []}
            e.save(suite / 'cases.json', cases)
            e.save(suite / 'rubrics.json', {'schema_version': 1, 'cases': dict.fromkeys(('C1', 'H1', 'K1'), rubric)})
            e.save(suite / 'protocol.json', {'schema_version': 1,
                   'model': {'requested': 'gpt-6-sol', 'requested_effort': 'medium'},
                   'runtime': {'timeout_seconds': 300, 'treatment': {'references': ['.agents/skills/deep-inquiry/references/' + name for name in e.REFS]}},
                   'screening': {'trials_per_family': 3}, 'confirmation': {'trials_per_arm_per_family': 3}, 'controls': {'trials_per_arm': 1}})
            for relative in ('SKILL.md', *['references/' + name for name in e.REFS]):
                (source / relative).write_text('fixture', encoding='utf-8')
            plan = {'schema_version': 1, 'purpose': 'canary', 'canary_prompt': 'task',
                    'suite_hashes': {name: e.digest(suite / name) for name in ('cases.json', 'rubrics.json', 'protocol.json')},
                    'skill_hashes': {path.relative_to(source).as_posix(): e.digest(path) for path in source.rglob('*') if path.is_file()},
                    'trials': [{'case_id': 'CANARY', 'condition': arm, 'repetition': 1} for arm in ('baseline', 'treatment')]}
            e.save(root / 'plan.json', plan)
            for index, (first, second, expected) in enumerate(scenarios):
                with self.subTest(first=first, second=second):
                    out = root / 'temp' / str(index)
                    reports = [first, second, ready]
                    calls = []

                    def trial_report(exe, auth, skill, case, condition, folder, frozen, common, probe, dialogue):
                        report = {'case_id': case['id'], 'condition': condition, **reports[len(calls)]}
                        calls.append(folder.name.removeprefix('CANARY-'))
                        return report

                    argv = ['eval_inquiry', 'run', '--suite', str(suite), '--plan', str(root / 'plan.json'),
                            '--exe', str(root / 'unused-exe'), '--auth', str(root / 'unused-auth'),
                            '--skill', str(source), '--out', str(out), '--probe']
                    # When real main processes the reports without launching a host.
                    with patch.object(e, 'ROOT', root), patch.object(sys, 'argv', argv), patch.object(e, 'run_trial', side_effect=trial_report), patch('sys.stdout', new=io.StringIO()):
                        result = e.main()
                    # Then retries, stop status, remaining slots and order match.
                    slots = e.load(out / 'run-slots.json')
                    self.assertEqual([(slot['case_id'], slot['condition'], slot['repetition']) for slot in slots],
                                     [('CANARY', 'baseline', 1), ('CANARY', 'treatment', 1)])
                    observed = (result, calls, [slot['status'] for slot in slots], [slot.get('attempt') for slot in slots])
                    self.assertEqual(observed, expected)

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
            path.write_text(json.dumps({'schema_version': 1, 'canary_cross_arm_verified': True, 'context': context, 'runner_sha256': e.digest(Path(e.__file__)), 'dialogue_runner_sha256': e.digest(Path(e.__file__).with_name('inquiry_dialogue.py')), **frozen}))
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
