"""Test validator behavior and actual bundle structure, not LLM reasoning."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.check_repository import (SKILL_PATH, canonical_digest, check_bundle,
                                   check_repository, check_suite, frontmatter,
                                   manifest, metadata)


class FrontmatterTests(unittest.TestCase):
    def test_actual_metadata(self):
        value = frontmatter((ROOT/SKILL_PATH/'SKILL.md').read_text(encoding='utf-8'))
        self.assertEqual(value['name'], 'deep-inquiry')

    def test_invalid_frontmatter(self):
        invalid = [
            'name: x\n',
            '---\nname: x\n---\n',
            '---\nname: x\nname: y\ndescription: "ok"\n---\n',
            '---\nname: x\ndescription: ""\n---\n',
            '---\nname: Bad_Name\ndescription: "ok"\n---\n',
            '---\nname: x\ndescription: false\n---\n',
            '---\nname: x\ndescription: [x]\n---\n',
            '---\nname: x\ndescription: "ok"\nextra: no\n---\n',
            '---\nname: '+('a'*65)+'\ndescription: "ok"\n---\n',
        ]
        for text in invalid:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    frontmatter(text)

    def test_metadata_duplicates_rejected(self):
        for text in ['interface:\ninterface:\n', 'interface:\n  display_name: "A"\n  display_name: "B"\n']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                metadata(text)


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.skill = Path(self.temp.name)/'deep-inquiry'
        shutil.copytree(ROOT/SKILL_PATH, self.skill)

    def tearDown(self):
        self.temp.cleanup()

    def append_root(self, text):
        with (self.skill/'SKILL.md').open('a', encoding='utf-8') as file:
            file.write(text)

    def test_real_bundle(self):
        self.assertEqual(check_bundle(self.skill), [])

    def test_missing_required_file(self):
        (self.skill/'SKILL.md').unlink()
        self.assertTrue(check_bundle(self.skill))

    def test_missing_reference(self):
        (self.skill/'references/inquiry-methods.md').unlink()
        self.assertTrue(any('missing linked' in e for e in check_bundle(self.skill)))

    def test_orphan_reference(self):
        (self.skill/'references/orphan.md').write_text('Orphan', encoding='utf-8')
        self.assertTrue(any('not directly linked' in e for e in check_bundle(self.skill)))

    def test_directory_link_not_sufficient(self):
        self.append_root('\n[everything](references)\n')
        self.assertTrue(any('missing linked file' in e for e in check_bundle(self.skill)))

    def test_path_escape(self):
        outside = self.skill.parent/'outside.md'
        outside.write_text('Do not read', encoding='utf-8')
        self.append_root('\n[outside](../outside.md)\n')
        self.assertTrue(any('path escape' in e for e in check_bundle(self.skill)))

    def test_external_runtime_dependency(self):
        self.append_root('\n[remote](https://example.invalid/rules.md)\n')
        self.assertTrue(any('external runtime link' in e for e in check_bundle(self.skill)))

    def test_symlink(self):
        try:
            (self.skill/'references/alias.md').symlink_to(self.skill/'SKILL.md')
        except OSError as exc:
            self.skipTest(f'Host does not permit symlink creation: {exc}')
        self.assertTrue(any('symlink' in e for e in check_bundle(self.skill)))

    def test_reserved_filename(self):
        # Windows itself rejects this name; the portable check is exercised on other hosts.
        if sys.platform == 'win32':
            self.skipTest('Windows prevents fixture creation')
        (self.skill/'references/CON.md').write_text('x', encoding='utf-8')
        self.assertTrue(any('nonportable path' in e for e in check_bundle(self.skill)))

    def test_unexpected_runtime_code(self):
        (self.skill/'extra.py').write_text('raise RuntimeError("never execute")', encoding='utf-8')
        self.assertTrue(any('unexpected runtime file' in e for e in check_bundle(self.skill)))

    def test_policy_regression(self):
        p = self.skill/'agents/openai.yaml'
        p.write_text(p.read_text(encoding='utf-8').replace('false','true'), encoding='utf-8')
        self.assertTrue(any('explicit-only' in e for e in check_bundle(self.skill)))

    def test_wrong_default_prompt(self):
        p = self.skill/'agents/openai.yaml'
        p.write_text(p.read_text(encoding='utf-8').replace('$deep-inquiry','$other'), encoding='utf-8')
        self.assertTrue(any('default prompt' in e for e in check_bundle(self.skill)))

    def test_content_identity_changes(self):
        before = canonical_digest(manifest(self.skill))
        p = self.skill/'references/alignment.md'
        p.write_text(p.read_text(encoding='utf-8')+'\nAdditional rule.\n', encoding='utf-8')
        self.assertNotEqual(before, canonical_digest(manifest(self.skill)))

    def test_checker_is_read_only(self):
        def snapshot():
            return {p.relative_to(self.skill).as_posix():
                    ('file', hashlib.sha256(p.read_bytes()).hexdigest()) if p.is_file() else ('directory', '')
                    for p in self.skill.rglob('*')}
        before = snapshot()
        check_bundle(self.skill)
        manifest(self.skill)
        self.assertEqual(snapshot(), before)


class SuiteTests(unittest.TestCase):
    def setUp(self):
        self.suite = json.loads((ROOT/'evals/behavior-suite.json').read_text(encoding='utf-8'))

    def test_actual_suites(self):
        for path in (ROOT/'evals').glob('*-suite.json'):
            with self.subTest(path=path):
                self.assertEqual(check_suite(json.loads(path.read_text(encoding='utf-8'))), [])

    def test_duplicate_case(self):
        self.suite['cases'].append(copy.deepcopy(self.suite['cases'][0]))
        self.assertTrue(any('case id' in e for e in check_suite(self.suite)))

    def test_global_check_collision(self):
        self.suite['cases'][0]['checks'][0]['id'] = self.suite['common_checks'][0]['id']
        self.assertTrue(any('collision' in e for e in check_suite(self.suite)))

    def test_duplicate_local_check(self):
        case = self.suite['cases'][0]
        case['checks'].append(copy.deepcopy(case['checks'][0]))
        self.assertTrue(check_suite(self.suite))

    def test_boolean_repetitions_rejected(self):
        self.suite['repetitions'] = True
        self.assertTrue(check_suite(self.suite))

    def test_bad_expectation_type(self):
        suite = json.loads((ROOT/'evals/trigger-suite.json').read_text(encoding='utf-8'))
        suite['cases'][0]['should_trigger'] = 'false'
        self.assertTrue(check_suite(suite))

    def test_unknown_kind(self):
        self.suite['cases'][0]['kind'] = 'simulation'
        self.assertTrue(check_suite(self.suite))

    def test_empty_check(self):
        self.suite['cases'][0]['checks'][0]['text'] = ''
        self.assertTrue(check_suite(self.suite))

    def test_nonobjects_rejected(self):
        for item in [None, [], True, 3]:
            with self.subTest(item=item):
                self.assertTrue(check_suite(item))

    def test_empty_templates_are_not_observations(self):
        for path in (ROOT/'evals').glob('*.empty.json'):
            record = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(record['observations'], [])
            self.assertEqual(record['metadata']['skill_version'], '')

    def test_canonical_digest(self):
        self.assertEqual(canonical_digest({'a':1,'b':2}), canonical_digest({'b':2,'a':1}))
        self.assertNotEqual(canonical_digest({'a':1}), canonical_digest({'a':2}))


class RepositoryTests(unittest.TestCase):
    def test_repository(self):
        self.assertEqual(check_repository(ROOT), [])

    def test_nonobject_repository_json_returns_diagnostic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)/'repo'
            shutil.copytree(ROOT, root)
            for name in ('behavior-suite.json', 'behavior-observations.empty.json'):
                path = root/'evals'/name
                original = path.read_bytes()
                for value in ([], None, True):
                    with self.subTest(name=name, value=value):
                        path.write_text(json.dumps(value), encoding='utf-8')
                        self.assertTrue(check_repository(root))
                path.write_bytes(original)

    def test_cli_does_not_claim_behavior(self):
        run = subprocess.run([sys.executable,'-B',str(ROOT/'tools/check_repository.py')],
                             capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 0, run.stdout+run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result['scope'], 'static_structure_only')
        self.assertEqual(result['host_behavior'], 'not_run')
        self.assertEqual(result['semantic_quality'], 'not_evaluated')


if __name__ == '__main__':
    unittest.main()
