"""Behavior checks for bounded evidence requests on one native thread."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import eval_inquiry as e
from test_eval_inquiry import ModelFreeHost


class DialogueTests(unittest.TestCase):
    def test_only_requested_record_is_returned_and_final_ends_access(self):
        dialogue = e.Dialogue.parse({'records': {'a': 'visible evidence', 'b': 'hidden evidence'}, 'max_requests': 2})
        self.assertEqual(dialogue.reply('READ a'), 'visible evidence')
        self.assertIsNone(dialogue.reply('Use the safe route.'))
        with self.assertRaises(e.DialogueError):
            dialogue.reply('READ b')

    def test_unknown_record_and_exhausted_budget_are_invalid_trials(self):
        for request in ('READ missing', 'READ a\nREAD b'):
            with self.subTest(request=request), self.assertRaises(e.DialogueError):
                e.Dialogue.parse({'records': {'a': 'x'}, 'max_requests': 1}).reply(request)
        dialogue = e.Dialogue.parse({'records': {'a': 'x'}, 'max_requests': 1})
        dialogue.reply('READ a')
        with self.assertRaises(e.DialogueError):
            dialogue.reply('READ a')

    def test_changed_dialogue_module_invalidates_canary(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'common.json'
            frozen = {'suite_hashes': {}, 'skill_hashes': {}}
            context = {'system': {}, 'requirements': {}, 'layers': [], 'actual_developer_sha256': 'b' * 64, 'actual_user_prefix_sha256': 'e' * 64}
            path.write_text(json.dumps({'schema_version': 1, 'canary_cross_arm_verified': True, 'context': context, 'runner_sha256': e.digest(Path(e.__file__)), 'dialogue_runner_sha256': '0' * 64, **frozen}))
            with self.assertRaises(e.RunnerError) as caught:
                e.read_common_context(path, {'common_context_sha256': e.digest(path)}, frozen)
            self.assertEqual(caught.exception.code, 'context_runner_mismatch')

    def test_actual_turns_keep_one_thread_and_preserve_query_and_final(self):
        self.run_dialogue_case(False)

    def test_second_turn_timeout_preserves_first_output_and_cleans_up(self):
        self.run_dialogue_case(True)

    def test_malformed_queries_preserve_response_but_cannot_be_scored(self):
        for response in ('READ', 'READ	ledger', 'read ledger'):
            with self.subTest(response=response):
                self.run_dialogue_case(False, response)

    def run_dialogue_case(self, timeout, malformed=None):
        dispatched = []
        class DialogueHost(ModelFreeHost):
            def call(self, method, params, deadline=None):
                if method != 'turn/start':
                    return super().call(method, params, deadline)
                self.dispatched = True
                dispatched.append(params)
                if timeout and len(dispatched) == 2:
                    raise TimeoutError('second turn failed')
                text = (malformed or 'READ ledger') if len(dispatched) == 1 else 'Choose B because delivered ledger says so.'
                self.capture.messages.append(text)
                self.capture.unknown_messages.append(f'unknown-{len(dispatched)}')
                self.capture.completion = 'completed'
                self.capture.output_seen = True
                self.capture.delivered_user_text = (['<environment_context>\n</environment_context>'] if len(dispatched) == 1 else []) + [params['input'][0]['text']]
                self.capture.delivered_developer_text = ['fixture context']
                return {'turn': {'id': f'turn-{len(dispatched)}'}}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            auth = root / 'auth.json'
            auth.write_bytes(b'fake credential')
            folder = root / 'trial'
            dialogue = e.Dialogue.parse({'records': {'ledger': 'B verified', 'secret': 'ORACLE MUST STAY HIDDEN'}, 'max_requests': 2})
            with patch.object(e, 'Host', DialogueHost), patch.object(e, 'verified_shared_context', return_value=('developer', {})):
                report = e.run_trial(Path(sys.executable), auth, root, {'id': 'D', 'prompt': 'Decide'}, 'baseline', folder, {}, {}, dialogue=dialogue)
            if malformed:
                self.assertEqual(report['status'], 'error')
                self.assertEqual(report['error_contract_code'], 'dialogue_invalid')
                self.assertEqual(len(dispatched), 1)
                self.assertEqual((folder / 'final.txt').read_text(), malformed)
                self.assertTrue(report['output_seen'])
                self.assertTrue(report['process_stopped'])
                self.assertTrue(report['copied_auth_root_removed'])
                return
            self.assertEqual(report['status'], 'error' if timeout else 'completed')
            self.assertEqual([p['threadId'] for p in dispatched], ['model-free-thread'] * 2)
            self.assertEqual(dispatched[1]['input'], [{'type': 'text', 'text': 'B verified'}])
            self.assertNotIn('ORACLE', json.dumps(dispatched))
            self.assertEqual((folder / 'turn-01-final.txt').read_text(), 'READ ledger')
            self.assertEqual((folder / 'final.txt').read_text(), 'READ ledger' if timeout else 'Choose B because delivered ledger says so.')
            self.assertTrue(report['output_seen'])
            self.assertTrue(report['turn_dispatched'])
            if not timeout:
                self.assertTrue(report['dialogue_delivery_verified'])
                self.assertEqual(report['turn_id'], 'turn-2')
                trace = json.loads((folder / 'dialogue-transcript.json').read_text())
                self.assertEqual([item['turn_id'] for item in trace], ['turn-1', 'turn-2'])
                self.assertEqual(json.loads((folder / 'unknown-phase-messages-private.json').read_text()), [{'turn': 1, 'messages': ['unknown-1']}, {'turn': 2, 'messages': ['unknown-2']}])
            self.assertTrue(report['process_stopped'])
            self.assertTrue(report['copied_auth_root_removed'])


if __name__ == '__main__':
    unittest.main()
