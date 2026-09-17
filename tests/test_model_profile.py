"""Static model-profile integration checks, not model behavior evaluations."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.check_repository import SKILL_PATH, check_bundle, check_suite


class ModelProfileTests(unittest.TestCase):
    def test_model_suite_contract(self):
        suite = json.loads((ROOT / 'evals/model-suite.json').read_text(encoding='utf-8'))
        self.assertEqual(check_suite(suite), [])
        self.assertEqual(suite['conditions'], ['baseline', 'original', 'candidate'])
        self.assertEqual(len(suite['cases']), 12)
        self.assertTrue(all(c['kind'] == 'outcome' for c in suite['cases']))

    def test_empty_model_record_matches_suite(self):
        suite = json.loads((ROOT / 'evals/model-suite.json').read_text(encoding='utf-8'))
        record = json.loads((ROOT / 'evals/model-observations.empty.json').read_text())
        self.assertEqual(record['suite_id'], suite['suite_id'])
        self.assertEqual(record['schema_version'], suite['schema_version'])
        self.assertEqual(record['observations'], [])
        self.assertTrue(all(value == '' for value in record['metadata'].values()))

    def test_model_reference_is_structurally_integrated(self):
        self.assertEqual(check_bundle(ROOT / SKILL_PATH), [])
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'deep-inquiry'
            shutil.copytree(ROOT / SKILL_PATH, target)
            (target / 'references/model-adaptation.md').unlink()
            self.assertTrue(any('missing linked file' in e for e in check_bundle(target)))

    def test_malformed_new_suite_is_rejected(self):
        suite = json.loads((ROOT / 'evals/model-suite.json').read_text(encoding='utf-8'))
        broken = copy.deepcopy(suite)
        broken['cases'][0]['checks'] = []
        self.assertTrue(check_suite(broken))
        broken = copy.deepcopy(suite)
        broken['cases'][0]['checks'][0]['id'] = broken['common_checks'][0]['id']
        self.assertTrue(check_suite(broken))


if __name__ == '__main__':
    unittest.main()
