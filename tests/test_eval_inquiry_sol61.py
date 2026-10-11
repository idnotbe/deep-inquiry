import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import eval_inquiry as original
from tools import eval_inquiry_sol61 as prospective
from test_eval_inquiry import ModelFreeHost


class ProspectiveRunnerTests(unittest.TestCase):
    def test_expired_deadline_does_not_dispatch(self):
        for runner in (original, prospective):
            for now in (10, 11):
                with self.subTest(runner=runner.__name__, now=now):
                    host = runner.Host.__new__(runner.Host)
                    host.number, host.dispatched = 0, False
                    host.stdin = io.StringIO()
                    with patch.object(runner.time, 'monotonic', return_value=now):
                        with self.assertRaisesRegex(TimeoutError, 'app-server deadline'):
                            host.call('turn/start', {}, 10)
                    self.assertEqual(host.stdin.getvalue(), '')
                    self.assertEqual(host.number, 0)
                    self.assertFalse(host.dispatched)

    def test_each_runner_accepts_only_its_requested_model(self):
        with tempfile.TemporaryDirectory() as temp:
            suite = Path(temp)
            for name in ('cases.json', 'rubrics.json', 'protocol.json'):
                (suite / name).write_bytes((original.ROOT / 'evals/v3' / name).read_bytes())
            protocol = original.load(suite / 'protocol.json')
            for model, accepted, rejected in (
                ('gpt-6-sol', original, prospective),
                ('gpt-6.1-sol', prospective, original),
            ):
                with self.subTest(model=model):
                    protocol['model']['requested'] = model
                    original.save(suite / 'protocol.json', protocol)
                    accepted.validate_suite(suite)
                    with self.assertRaises(rejected.RunnerError):
                        rejected.validate_suite(suite)

    def test_model_configuration_and_both_dialogue_turns(self):
        for runner, model in ((original, 'gpt-6-sol'), (prospective, 'gpt-6.1-sol')):
            with self.subTest(model=model), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                auth = root / 'auth.json'
                auth.write_bytes(b'fake credential')
                requests = []
                process = Mock(stdin=io.StringIO(), stdout=io.StringIO())
                with patch.object(runner.subprocess, 'Popen', return_value=process) as popen, patch.object(runner.threading, 'Thread'):
                    runner.Host(Path(sys.executable), root, root, root, runner.Capture())
                self.assertIn(f'model="{model}"', popen.call_args.args[0])

                class ModelHost(ModelFreeHost):
                    def call(self, method, params, deadline=None):
                        requests.append((method, params))
                        if method == 'config/read':
                            return {'config': {'model': model, 'model_reasoning_effort': 'medium'}, 'layers': []}
                        if method == 'thread/start':
                            return {'model': model, 'reasoningEffort': 'medium', 'instructionSources': [], 'sandbox': {'type': 'readOnly', 'networkAccess': False}, 'approvalPolicy': 'never', 'thread': {'id': 'model-free-thread'}}
                        if method != 'turn/start':
                            return super().call(method, params, deadline)
                        self.dispatched = True
                        count = sum(method == 'turn/start' for method, _ in requests)
                        self.capture.messages.append('READ ledger' if count == 1 else 'Choose B.')
                        self.capture.completion = 'completed'
                        self.capture.output_seen = True
                        self.capture.delivered_user_text = (['<environment_context>\n</environment_context>'] if count == 1 else []) + [params['input'][0]['text']]
                        self.capture.delivered_developer_text = ['fixture context']
                        return {'turn': {'id': f'turn-{count}'}}

                dialogue = runner.Dialogue.parse({'records': {'ledger': 'B verified'}, 'max_requests': 2})
                with patch.object(runner, 'Host', ModelHost), patch.object(runner, 'verified_shared_context', return_value=('developer', {})):
                    report = runner.run_trial(Path(sys.executable), auth, root, {'id': 'D', 'prompt': 'Decide'}, 'baseline', root / 'trial', {}, {}, dialogue=dialogue)
                self.assertEqual(report['status'], 'completed', report.get('error_message', report.get('error_contract_code')))
                starts = [params for method, params in requests if method == 'thread/start']
                turns = [params for method, params in requests if method == 'turn/start']
                self.assertEqual([p['model'] for p in starts], [model])
                self.assertEqual([p['model'] for p in turns], [model, model])
                self.assertEqual([p['effort'] for p in turns], ['medium', 'medium'])
                self.assertEqual(turns[1]['input'], [{'type': 'text', 'text': 'B verified'}])


if __name__ == '__main__':
    unittest.main()
