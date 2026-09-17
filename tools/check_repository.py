"""Read-only structural checks for this repository's deliberately narrow formats.

Not a general YAML/Markdown validator, model runner, semantic judge or safety proof.
Python 3.10+, standard library only. Never execute code from an inspected skill.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

SKILL_PATH = Path('.agents/skills/deep-inquiry')
LINK = re.compile(r'\[[^\]\n]+\]\(([^)\s]+)\)')
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')


def canonical_digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def frontmatter(text: str) -> dict[str, str]:
    """Accept only name + one JSON-quoted description, not arbitrary YAML."""
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if not match:
        raise ValueError('missing or malformed frontmatter')
    fields: dict[str, str] = {}
    for line in match[1].splitlines():
        key, sep, value = line.partition(': ')
        if not sep or key not in {'name', 'description'} or key in fields:
            raise ValueError('unsupported or duplicate frontmatter field')
        fields[key] = value
    if set(fields) != {'name', 'description'}:
        raise ValueError('name and description are required')
    name = fields['name']
    if len(name) > 64 or not NAME.fullmatch(name):
        raise ValueError('invalid skill name')
    try:
        description = json.loads(fields['description'])
    except json.JSONDecodeError as exc:
        raise ValueError('description must be a single JSON-quoted string') from exc
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise ValueError('description must be nonempty and at most 1024 characters')
    fields['description'] = description
    return fields


def metadata(text: str) -> dict[str, dict[str, object]]:
    """Read only the interface/policy subset used by this instruction-only skill."""
    result: dict[str, dict[str, object]] = {}
    section = None
    for line in text.splitlines():
        if not line.strip():
            continue
        if line in {'interface:', 'policy:'}:
            section = line[:-1]
            if section in result:
                raise ValueError('duplicate metadata section')
            result[section] = {}
            continue
        match = re.fullmatch(r'  ([a-z_]+): (.+)', line)
        if section is None or match is None:
            raise ValueError('unsupported metadata syntax')
        key, raw = match.groups()
        if key in result[section]:
            raise ValueError('duplicate metadata field')
        try:
            result[section][key] = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError('metadata values must be JSON strings or booleans') from exc
    return result


def check_bundle(skill: Path) -> list[str]:
    errors: list[str] = []
    if not skill.is_dir() or skill.is_symlink():
        return ['skill directory missing or symlinked']
    entries = sorted(skill.rglob('*'))
    if any(p.is_symlink() for p in entries):
        return ['symlinks are not supported']
    files = [p for p in entries if p.is_file()]
    if any(not p.is_file() and not p.is_dir() for p in entries):
        return ['non-regular filesystem entry']
    normalized: set[str] = set()
    for p in entries:
        rel = p.relative_to(skill).as_posix()
        key = unicodedata.normalize('NFC', rel).casefold()
        if key in normalized:
            errors.append(f'case/normalization path collision: {rel}')
        normalized.add(key)
        for part in p.relative_to(skill).parts:
            stem = part.split('.')[0].upper()
            if (part.endswith((' ', '.')) or re.search(r'[<>:"\\|?*\x00-\x1f]', part)
                    or stem in {'CON', 'PRN', 'AUX', 'NUL'}
                    or re.fullmatch(r'(COM|LPT)[1-9]', stem)):
                errors.append(f'nonportable path: {rel}')
    required = [skill/'SKILL.md', skill/'agents/openai.yaml', skill/'LICENSE.txt']
    if any(not p.is_file() for p in required):
        return errors + ['required runtime file missing']
    try:
        text = (skill/'SKILL.md').read_text(encoding='utf-8')
        fields = frontmatter(text)
        if fields['name'] != skill.name:
            errors.append('directory/name mismatch')
        if len(text.splitlines()) >= 500:
            errors.append('root exceeds project line budget')
        config = metadata((skill/'agents/openai.yaml').read_text(encoding='utf-8'))
        if set(config) != {'interface', 'policy'}:
            errors.append('unexpected metadata sections')
        interface = config.get('interface', {})
        if set(interface) != {'display_name', 'short_description', 'default_prompt'}:
            errors.append('unexpected interface fields')
        if not all(isinstance(v, str) and v.strip() for v in interface.values()):
            errors.append('interface values must be nonempty strings')
        short = interface.get('short_description', '')
        if not isinstance(short, str) or not 25 <= len(short) <= 64:
            errors.append('invalid short description length')
        if '$'+fields['name'] not in str(interface.get('default_prompt', '')):
            errors.append('default prompt must invoke this skill')
        policy = config.get('policy', {})
        if set(policy) != {'allow_implicit_invocation'} or policy['allow_implicit_invocation'] is not False:
            errors.append('explicit-only Codex policy changed')
    except (ValueError, UnicodeError) as exc:
        return errors + [str(exc)]
    root_targets: set[Path] = set()
    for p in files:
        if p.suffix != '.md':
            if p.name not in {'openai.yaml', 'LICENSE.txt'}:
                errors.append(f'unexpected runtime file: {p.name}')
            continue
        try:
            body = p.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'non-UTF-8 Markdown: {p.name}')
            continue
        for destination in LINK.findall(body):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', destination):
                errors.append(f'external runtime link: {destination}')
                continue
            path = destination.split('#', 1)[0]
            if not path:
                continue  # Heading anchors are outside this small checker's scope.
            target = (p.parent/path).resolve()
            if not target.is_relative_to(skill.resolve()):
                errors.append(f'path escape: {destination}')
            elif not target.is_file():
                errors.append(f'missing linked file: {destination}')
            elif p == skill/'SKILL.md':
                root_targets.add(target)
    for directory in ('references', 'assets'):
        for p in (skill/directory).rglob('*'):
            if p.is_file() and p.resolve() not in root_targets:
                errors.append(f'resource not directly linked from root: {p.name}')
    return errors


def check_suite(suite: object) -> list[str]:
    """Validate definitions only; do not score observations or execute prompts."""
    if not isinstance(suite, dict):
        return ['suite must be an object']
    errors: list[str] = []
    if type(suite.get('schema_version')) is not int or suite['schema_version'] != 1:
        errors.append('schema_version must be 1')
    if not isinstance(suite.get('suite_id'), str) or not suite['suite_id'].strip():
        errors.append('suite_id required')
    conditions = suite.get('conditions')
    if (not isinstance(conditions, list) or not conditions
            or not all(isinstance(x, str) and x.strip() for x in conditions)
            or len(conditions) != len(set(str(x) for x in conditions))):
        errors.append('conditions must be unique nonempty strings')
    reps = suite.get('repetitions')
    if type(reps) is not int or reps < 1:
        errors.append('repetitions must be a positive integer')
    if suite.get('require_provenance') is not True or suite.get('fixtures') != {}:
        errors.append('this profile requires provenance and entirely inline fixed inputs')

    def checks(items: object, label: str) -> set[str]:
        seen: set[str] = set()
        if not isinstance(items, list):
            errors.append(f'{label}: checks must be a list')
            return seen
        for item in items:
            if not isinstance(item, dict):
                errors.append(f'{label}: check must be an object')
                continue
            cid = item.get('id')
            if not isinstance(cid, str) or not cid.strip() or cid in seen:
                errors.append(f'{label}: duplicate or invalid check id')
            else:
                seen.add(cid)
            if not isinstance(item.get('text'), str) or not item['text'].strip():
                errors.append(f'{label}: check text required')
            if type(item.get('critical')) is not bool:
                errors.append(f'{label}: critical must be Boolean')
        return seen

    common = checks(suite.get('common_checks', []), 'common')
    cases = suite.get('cases')
    if not isinstance(cases, list) or not cases:
        return errors + ['nonempty cases required']
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append('case must be an object')
            continue
        cid = case.get('id')
        if not isinstance(cid, str) or not cid.strip() or cid in seen:
            errors.append('duplicate or invalid case id')
        else:
            seen.add(cid)
        if not isinstance(case.get('prompt'), str) or not case['prompt'].strip():
            errors.append('nonempty fixed prompt required')
        if type(case.get('critical')) is not bool:
            errors.append('case critical must be Boolean')
        if case.get('kind') == 'trigger':
            if type(case.get('should_trigger')) is not bool:
                errors.append('trigger expectation must be Boolean')
            if case.get('invocation') not in {'explicit', 'implicit'}:
                errors.append('trigger invocation mode required')
        elif case.get('kind') == 'outcome':
            local = checks(case.get('checks'), str(cid))
            if not local or common.intersection(local):
                errors.append('empty local checks or common/local id collision')
        else:
            errors.append('unknown case kind')
    return errors


def manifest(skill: Path) -> dict[str, str]:
    if check_bundle(skill):
        raise ValueError('resolve bundle errors before generating identity')
    return {p.relative_to(skill).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(skill.rglob('*')) if p.is_file()}


def check_repository(root: Path) -> list[str]:
    errors = check_bundle(root/SKILL_PATH)
    for kind in ('behavior', 'trigger'):
        try:
            suite = json.loads((root/f'evals/{kind}-suite.json').read_text(encoding='utf-8'))
            errors += [f'{kind}: {e}' for e in check_suite(suite)]
            observation = json.loads((root/f'evals/{kind}-observations.empty.json').read_text(encoding='utf-8'))
            if (not isinstance(suite, dict) or not isinstance(observation, dict)
                    or observation.get('suite_id') != suite.get('suite_id')
                    or observation.get('observations') != []):
                errors.append(f'{kind}: tracked empty template is not empty or has wrong suite identity')
        except (OSError, ValueError) as exc:
            errors.append(f'{kind}: {exc}')
    try:
        if (root/'LICENSE').read_bytes() != (root/SKILL_PATH/'LICENSE.txt').read_bytes():
            errors.append('runtime license differs from repository license')
    except OSError as exc:
        errors.append(str(exc))
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        errors = check_repository(root)
        report = {'scope': 'static_structure_only', 'errors': errors,
                  'host_behavior': 'not_run', 'semantic_quality': 'not_evaluated'}
        if not errors:
            report['skill_sha256'] = canonical_digest(manifest(root/SKILL_PATH))
        print(json.dumps(report, indent=2))
        return 1 if errors else 0
    except (OSError, ValueError) as exc:
        print(json.dumps({'scope': 'static_structure_only', 'errors': [str(exc)]}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
