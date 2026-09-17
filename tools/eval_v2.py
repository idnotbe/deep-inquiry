"""Deep Inquiry evaluation: fixed tasks, private-to-runner rubrics and honest evidence.

Python 3.10+, standard library. Native runners are optional and never installed here.
Fresh workspaces are not a security sandbox. Run untrusted agents in a sandbox you
control. No automatic publishing, credential discovery or paid API calls.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'evals/v2'
SKILL = ROOT / '.agents/skills/deep-inquiry'
MODES = {'response','planning','workspace','multiturn','native_trigger','native_loading'}
KINDS = {'review','json_equals','exact_text','number','files_exact','unchanged','trigger'}
EVIDENCE = {'host_run','current_session_exercise','fixture_oracle','blocked'}
STATES = {'pass','fail','not_run','not_applicable'}
SHA = re.compile(r'[0-9a-f]{64}')


def canonical(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def loads(text: str):
    def bad_constant(value):
        raise ValueError(f'nonfinite JSON number: {value}')
    return json.loads(text, object_pairs_hook=_pairs, parse_constant=bad_constant)


def load(path: Path):
    return loads(path.read_text(encoding='utf-8'))


def write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def safe_name(name: str) -> bool:
    if not isinstance(name, str) or not name or '\\' in name:
        return False
    p = PurePosixPath(name)
    return (not p.is_absolute() and str(p) == name and all(x not in {'.','..',''} for x in p.parts)
            and not any(re.search(r'[<>:"|?*\x00-\x1f]', x) or x.endswith((' ','.'))
                        or re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])', x.split('.')[0], re.I)
                        for x in p.parts))


def safe_child(root: Path, name: str) -> Path:
    if not safe_name(name):
        raise ValueError(f'unsafe relative path: {name}')
    root = root.resolve()
    p = root / name
    if not p.resolve().is_relative_to(root) or any(x.is_symlink() for x in [p, *p.parents] if x != root):
        raise ValueError(f'escaped or symlinked path: {name}')
    return p


def inventory(root: Path) -> dict:
    """Include ignored files and empty directories; never follow a symlink."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError('workspace must be a real directory')
    result = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in sorted(dirs + files):
            p = Path(directory)/name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                result[rel] = {'type':'symlink','target':os.readlink(p)}
            elif p.is_dir():
                result[rel] = {'type':'directory'}
            elif p.is_file():
                result[rel] = {'type':'file','sha256':file_hash(p)}
            else:
                result[rel] = {'type':'special'}
    return result


def skill_digest(skill: Path) -> str:
    inv = inventory(skill)
    if any(v['type'] not in {'file','directory'} for v in inv.values()):
        raise ValueError('skill contains nonregular entries')
    return canonical({k:v['sha256'] for k,v in inv.items() if v['type']=='file'})


def read_suite(data: Path = DATA):
    suite, rubrics = load(data/'cases.json'), load(data/'rubrics.json')
    errors = validate(suite, rubrics)
    if errors:
        raise ValueError('; '.join(errors))
    return suite, rubrics


def check_paths(mapping):
    """Portable fixture tree, with no case or file/directory collisions."""
    if not isinstance(mapping,dict) or not all(safe_name(k) and isinstance(v,str) for k,v in mapping.items()):
        return False
    seen={}
    for path in mapping:
        parts=PurePosixPath(path).parts
        for n in range(1,len(parts)+1):
            raw='/'.join(parts[:n]); key=unicodedata.normalize('NFC',raw).casefold()
            value=(raw, 'file' if n==len(parts) else 'directory')
            if key in seen and seen[key]!=value:return False
            seen[key]=value
    return True


def validate(suite, rubrics) -> list[str]:
    errors = []
    if not isinstance(suite, dict) or not isinstance(rubrics, dict):
        return ['suite and rubrics must be objects']
    if suite.get('schema_version') != 2 or type(suite.get('schema_version')) is not int:
        errors.append('suite schema_version must be integer 2')
    if type(rubrics.get('schema_version')) is not int or rubrics.get('schema_version') != 2 or suite.get('suite_id') != rubrics.get('suite_id'):
        errors.append('rubric version or identity mismatch')
    if not isinstance(suite.get('suite_id'),str) or not suite['suite_id'].strip():
        errors.append('suite_id required')
    if suite.get('conditions') != ['without_skill','with_skill']:
        errors.append('expected without_skill and with_skill conditions')
    if type(suite.get('repetitions')) is not int or suite['repetitions'] < 1:
        errors.append('repetitions must be a positive integer')
    if not isinstance(suite.get('target_skill_sha256'), str) or not SHA.fullmatch(suite['target_skill_sha256']):
        errors.append('target bundle digest required')
    cases = suite.get('cases')
    judges = rubrics.get('cases')
    common = rubrics.get('common_checks')
    if not isinstance(cases, list) or not cases or not isinstance(judges, dict) or not isinstance(common,list):
        return errors+['nonempty cases, rubric mapping and common checks required']
    ids = set()
    def inspect_checks(checks, label):
        seen = set()
        if not isinstance(checks,list) or not checks:
            errors.append(f'{label}: nonempty checks required'); return seen
        for q in checks:
            if not isinstance(q,dict):
                errors.append(f'{label}: check must be object'); continue
            i = q.get('id')
            if not isinstance(i,str) or not i or i in seen:
                errors.append(f'{label}: duplicate/invalid check ID')
            else: seen.add(i)
            kind=q.get('kind')
            if kind not in KINDS or type(q.get('critical')) is not bool:
                errors.append(f'{label}: invalid check kind or critical flag')
            if kind=='review' and (not isinstance(q.get('criterion'),str) or not q['criterion'].strip()):
                errors.append(f'{label}: criterion missing')
            if kind in {'number','json_equals','exact_text','files_exact','trigger'} and 'expected' not in q:
                errors.append(f'{label}: expected value missing')
            if kind=='number' and (type(q.get('expected')) not in {int,float} or not math.isfinite(q['expected'])):
                errors.append(f'{label}: invalid numeric oracle')
            if kind=='trigger' and type(q.get('expected')) is not bool:
                errors.append(f'{label}: Boolean trigger expectation required')
            if kind=='files_exact':
                exp=q.get('expected')
                if not exp or not check_paths(exp):
                    errors.append(f'{label}: invalid expected files')
        return seen
    global_ids=inspect_checks(common,'common')
    for c in cases:
        if not isinstance(c,dict):
            errors.append('case must be object'); continue
        i=c.get('id')
        if not isinstance(i,str) or not re.fullmatch(r'[A-Z][0-9]{2}',i) or i in ids:
            errors.append('duplicate/invalid case ID'); continue
        ids.add(i)
        if c.get('mode') not in MODES or not isinstance(c.get('prompt'),str) or not c['prompt'].strip():
            errors.append(f'{i}: invalid mode/prompt')
        for key in ('family','language','source'):
            if not isinstance(c.get(key),str) or not c[key]: errors.append(f'{i}: {key} missing')
        fixture=c.get('fixture',{})
        if not check_paths(fixture):
            errors.append(f'{i}: invalid fixture')
        elif any(k.startswith(('.agents/','.claude/','.git/')) or k in {'.agents','.claude','.git','AGENTS.md','CLAUDE.md'} for k in fixture):
            errors.append(f'{i}: fixture collides with host controls')
        if c.get('mode')=='native_trigger' and c.get('invocation') not in {'explicit','implicit','quoted'}:
            errors.append(f'{i}: trigger invocation mode required')
        if c.get('mode')=='multiturn' and not (isinstance(c.get('followup_user_turns'),list) and c['followup_user_turns'] and all(isinstance(x,str) and x for x in c['followup_user_turns'])):
            errors.append(f'{i}: scripted user turns required')
        j=judges.get(i)
        if not isinstance(j,dict):
            errors.append(f'{i}: rubric missing'); continue
        local=inspect_checks(j.get('checks'),i)
        if local & global_ids: errors.append(f'{i}: common/local collision')
        if c.get('mode')=='native_trigger' and not any(q.get('kind')=='trigger' for q in j.get('checks',[])):
            errors.append(f'{i}: trigger expectation missing')
    if set(judges)!=ids: errors.append('rubric/case IDs differ')
    return errors


def suite_digest(suite, rubrics):
    return canonical({'suite':suite,'rubrics':rubrics})


def request(case, condition, native_engine='codex'):
    """Whitelist model inputs: judge metadata is intentionally never serialized."""
    prompt=case['prompt']
    if condition=='with_skill' and case['mode'] not in {'native_trigger','native_loading'}:
        invocation='/deep-inquiry' if native_engine=='claude' else '$deep-inquiry'
        prompt=f'Apply the installed {invocation} skill to this task.\n\n'+prompt
    elif native_engine=='claude' and condition=='with_skill':
        # Host syntax translation is recorded; quoted negative test text is unchanged.
        if case.get('invocation')=='explicit' or case['mode']=='native_loading':
            prompt=prompt.replace('$deep-inquiry','/deep-inquiry')
    return {'prompt':prompt,'fixture':case.get('fixture',{}),
            'followup_user_turns':case.get('followup_user_turns',[])}


def case_by_id(suite, case_id):
    matches=[c for c in suite['cases'] if c['id']==case_id]
    if len(matches)!=1: raise ValueError(f'unknown case {case_id}')
    return matches[0]


def prepare(case, condition, out:Path, skill:Path, suite, rubrics, engine='codex', repetition=1):
    if engine not in {'codex','claude'}: raise ValueError('unknown engine')
    if type(repetition) is not int or not 1<=repetition<=suite['repetitions']:raise ValueError('repetition out of plan')
    if condition not in suite['conditions']: raise ValueError('unknown condition')
    if case['mode'] in {'native_trigger','native_loading'} and condition!='with_skill':
        raise ValueError('native discovery/loading cases require installed with_skill condition')
    if out.exists(): raise ValueError('refuse to overwrite a trial directory')
    if out.resolve().is_relative_to(ROOT.resolve()): raise ValueError('trials must be outside checkout')
    if condition=='with_skill' and skill_digest(skill)!=suite['target_skill_sha256']:
        raise ValueError('target bundle drift: deliberately rebind suite before a new version experiment')
    work=out/'workspace'; work.mkdir(parents=True)
    for name, content in case.get('fixture',{}).items():
        p=safe_child(work,name); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding='utf-8',newline='')
    if condition=='with_skill':
        folder='.claude/skills/deep-inquiry' if engine=='claude' else '.agents/skills/deep-inquiry'
        shutil.copytree(skill,safe_child(work,folder))
    req=request(case,condition,engine)
    (out/'prompt.txt').write_text(req['prompt'],encoding='utf-8')
    rec={'schema_version':2,'case_id':case['id'],'condition':condition,'repetition':repetition,
         'suite_sha256':suite_digest(suite,rubrics),'request_sha256':canonical(req),
         'skill_sha256':suite['target_skill_sha256'] if condition=='with_skill' else 'no_skill',
         'engine':engine,'model':None,'effort':None,'status':'prepared','evidence_kind':'blocked',
         'isolation':'fresh_workspace_only; global host configuration unverified',
         'independent_session':False,'grader_exposed':None,'trace_complete':False,
         'before':inventory(work),'after':None,'files':{},'elapsed_seconds':None}
    write(out/'record.json',rec)
    return rec


def _json_same(a,b):
    if isinstance(b,bool) or b is None: return type(a) is type(b) and a==b
    if type(b) in {int,float}: return type(a) in {int,float} and (type(a) is int or math.isfinite(a)) and a==b
    if isinstance(b,str): return isinstance(a,str) and a==b
    if isinstance(b,list): return isinstance(a,list) and len(a)==len(b) and all(_json_same(x,y) for x,y in zip(a,b))
    if isinstance(b,dict): return isinstance(a,dict) and set(a)==set(b) and all(_json_same(a[k],v) for k,v in b.items())
    return False


def observe_trace(raw:str, engine:str):
    """Parse full logs; never return false on the first unrelated tool call.

Claude Skill tool calls supply activation evidence. Codex command reads are only
material-access evidence, not activation. Unrecognized/incomplete logs are unknown.
"""
    events=[]; terminal=False; selected=False; reads=[]; final=None; errors=[]; count=0
    for line in raw.splitlines():
        if not line.strip(): continue
        try: e=loads(line)
        except ValueError:
            errors.append('malformed_jsonl'); continue
        if not isinstance(e,dict): errors.append('nonobject_event'); continue
        events.append(e)
        if engine=='claude':
            if e.get('type')=='assistant':
                message=e.get('message',{})
                if not isinstance(message,dict): errors.append('bad_message'); continue
                blocks=message.get('content',[])
                if not isinstance(blocks,list): errors.append('bad_content'); continue
                for block in blocks:
                    if not isinstance(block,dict): continue
                    if block.get('type')=='tool_use':
                        count+=1
                        name=block.get('name'); args=block.get('input',{})
                        if not isinstance(args,dict): continue
                        if name=='Skill' and args.get('skill') in {'deep-inquiry','deep-inquiry:deep-inquiry'}:
                            selected=True
                        if name=='Read' and isinstance(args.get('file_path'),str): reads.append(args['file_path'])
            if e.get('type')=='result':
                terminal=True
                if e.get('is_error') or e.get('subtype') not in {'success',None}: errors.append('host_error')
                if isinstance(e.get('result'),str): final=e['result']
        elif engine=='codex':
            if e.get('type')=='item.completed':
                item=e.get('item',{})
                if not isinstance(item,dict): continue
                if item.get('type')=='agent_message' and isinstance(item.get('text'),str): final=item['text']
                if item.get('type')=='command_execution': count+=1
            if e.get('type')=='turn.completed': terminal=True
            if e.get('type') in {'error','turn.failed'}: errors.append('host_error')
        else: errors.append('unsupported_trace_engine'); break
    complete=terminal and not errors
    # Claude may inject skills without a Skill tool event; absence is not reliable
    # negative evidence without a separately verified complete selection observer.
    return {'complete':complete,'selected':True if selected else None,
            'read_paths':reads,'final':final,'tool_calls':count,'errors':sorted(set(errors))}


def finalize(out:Path, rec:dict, final:str, raw:str, stderr:str):
    for filename,text in [('final.txt',final),('trace.jsonl',raw),('stderr.txt',stderr)]:
        (out/filename).write_text(text,encoding='utf-8')
    rec['after']=inventory(out/'workspace')
    rec['files']={n:file_hash(out/n) for n in ('final.txt','trace.jsonl','stderr.txt')}
    write(out/'record.json',rec)


def run_native(case,condition,out,skill,suite,rubrics,engine,model,effort=None,timeout=180,repetition=1):
    rec=prepare(case,condition,out,skill,suite,rubrics,engine,repetition)
    rec.update(model=model,effort=effort,model_identity='requested_not_verified')
    if case['mode']=='multiturn':
        rec.update(status='blocked',error='conversation_driver_not_implemented; use documented manual protocol')
        finalize(out,rec,'','',''); return rec
    executable=shutil.which(engine)
    if not executable:
        rec.update(status='blocked',error=f'executable_not_found:{engine}')
        finalize(out,rec,'','',''); return rec
    if engine=='codex':
        cmd=[executable,'exec','--json','--skip-git-repo-check','--sandbox','workspace-write','--model',model]
        if effort: cmd += ['-c',f'model_reasoning_effort="{effort}"']
        cmd+=['-']
    elif engine=='claude':
        cmd=[executable,'-p','--model',model,'--output-format','stream-json','--verbose',
             '--permission-mode','dontAsk','--allowedTools','Read,Write,Edit,Skill',
             '--tools','Read,Write,Edit,Skill','--strict-mcp-config',
             '--setting-sources','project',
             '--settings',json.dumps({'skillOverrides':{'deep-inquiry':'user-invocable-only' if condition=='with_skill' else 'off'}})]
        if effort:cmd+=['--effort',effort]
    else: raise ValueError('unsupported engine')
    rec.update(command=cmd,evidence_kind='host_run',independent_session=True,grader_exposed=False)
    start=time.monotonic()
    try:
        proc=subprocess.run(cmd,input=(out/'prompt.txt').read_text(encoding='utf-8'),
                            cwd=out/'workspace',text=True,encoding='utf-8',errors='replace',
                            capture_output=True,timeout=timeout,check=False)
        raw,err=proc.stdout,proc.stderr
        parsed=observe_trace(raw,engine)
        rec.update(exit_code=proc.returncode,trace_complete=parsed['complete'],
                   selection=parsed['selected'],tool_calls=parsed['tool_calls'])
        rec['status']='completed' if proc.returncode==0 and parsed['complete'] and parsed['final'] is not None else 'error'
        final=parsed['final'] or ''
    except subprocess.TimeoutExpired as e:
        rec.update(status='timeout',trace_complete=False)
        raw=e.stdout or ''; err=e.stderr or ''; final=''
        if isinstance(raw,bytes):raw=raw.decode('utf-8','replace')
        if isinstance(err,bytes):err=err.decode('utf-8','replace')
    except OSError as e:
        rec.update(status='error',trace_complete=False,error=str(e)); raw=err=final=''
    rec['elapsed_seconds']=time.monotonic()-start
    finalize(out,rec,final,raw,err)
    return rec


def all_checks(case,rubrics):
    # Activation is assessed independently of task success; generic outcome rubrics
    # are inapplicable to a trigger-only trial, not positive evidence for it.
    return (rubrics['common_checks'] if case['mode']!='native_trigger' else [])+rubrics['cases'][case['id']]['checks']


def expected_before(case, condition, engine, skill=SKILL):
    result={}
    def put(name,value):
        result[name]=value
        p=PurePosixPath(name).parent
        while str(p)!='.':result[str(p)]={'type':'directory'};p=p.parent
    for name,text in case.get('fixture',{}).items():
        put(name,{'type':'file','sha256':hashlib.sha256(text.encode('utf-8')).hexdigest()})
    if condition=='with_skill':
        prefix='.claude/skills/deep-inquiry' if engine=='claude' else '.agents/skills/deep-inquiry'
        put(prefix,{'type':'directory'})
        for name,value in inventory(skill).items():put(prefix+'/'+name,value)
    return result


def review_binding(rec):
    return canonical({'request':rec['request_sha256'],'skill':rec['skill_sha256'],
                      'before':rec['before'],'after':rec['after'],'files':rec['files']})


def grade(out:Path,suite,rubrics,regrade_reason=None,review=None):
    rec=load(out/'record.json')
    if not isinstance(rec,dict):raise ValueError('record must be an object')
    case=case_by_id(suite,rec.get('case_id'))
    if rec.get('schema_version')!=2 or rec.get('evidence_kind') not in EVIDENCE:
        raise ValueError('unrecognized evidence record')
    if rec.get('condition') not in suite['conditions'] or type(rec.get('repetition')) is not int or not 1<=rec['repetition']<=suite['repetitions']:
        raise ValueError('invalid condition/repetition')
    if rec.get('request_sha256')!=canonical(request(case,rec['condition'],rec['engine'])):
        raise ValueError('task input drift: rerun required; regrading cannot change inputs')
    if rec.get('engine') not in {'codex','claude'}:raise ValueError('unsupported recorded engine')
    if rec.get('status') not in {'prepared','completed','blocked','error','timeout'}:raise ValueError('unknown run status')
    old=rec.get('suite_sha256'); current=suite_digest(suite,rubrics)
    if old!=current and not regrade_reason: raise ValueError('suite/rubric drift: explicit regrade reason required')
    expected_skill=suite['target_skill_sha256'] if rec['condition']=='with_skill' else 'no_skill'
    if rec.get('skill_sha256')!=expected_skill: raise ValueError('record skill identity mismatch')
    if rec.get('before')!=expected_before(case,rec['condition'],rec['engine']):
        raise ValueError('initial fixture/bundle manifest mismatch')
    files=rec.get('files',{})
    if set(files)!={'final.txt','trace.jsonl','stderr.txt'}:
        raise ValueError('incomplete artifact manifest')
    for name,digest in files.items():
        p=safe_child(out,name)
        if not p.is_file() or file_hash(p)!=digest: raise ValueError(f'artifact changed: {name}')
    actual_after=inventory(out/'workspace')
    if actual_after!=rec.get('after'): raise ValueError('workspace changed after capture')
    final=(out/'final.txt').read_text(encoding='utf-8')
    judgments={}
    if review is not None:
        if not isinstance(review,dict) or review.get('suite_sha256')!=current or review.get('artifact_sha256')!=review_binding(rec):
            raise ValueError('review not bound to these exact artifacts and rubric')
        if review.get('reviewer_kind') not in {'self_review','human_review','independent_model_review'} or not isinstance(review.get('reviewer'),str) or not review['reviewer'].strip():
            raise ValueError('review provenance required')
        allowed={q['id'] for q in all_checks(case,rubrics) if q['kind']=='review'}
        if not isinstance(review.get('checks'),list):raise ValueError('review checks required')
        for q in review['checks']:
            if not isinstance(q,dict) or q.get('id') not in allowed or q['id'] in judgments:
                raise ValueError('invalid/duplicate review ID; cannot override machine checks')
            if q.get('status') not in STATES or not isinstance(q.get('evidence'),str) or not q['evidence'].strip():
                raise ValueError('review judgment requires status and supporting evidence')
            judgments[q['id']]=q
    results=[]
    eligible=rec.get('status')=='completed' and rec['evidence_kind']!='blocked'
    if eligible and rec['evidence_kind']=='host_run':
        observed=observe_trace((out/'trace.jsonl').read_text(encoding='utf-8'),rec['engine'])
        eligible=observed['complete'] and rec.get('exit_code')==0
        if eligible and observed['final']!=final:raise ValueError('final response differs from host trace')
    for q in all_checks(case,rubrics):
        kind=q['kind']; status='not_run'; why='requires separate evidence-based review'
        try:
            if not eligible: why=f'run status {rec.get("status")}; no fabricated behavioral result'
            elif kind=='review':
                if q['id'] in judgments:
                    j=judgments[q['id']];status=j['status'];why=j['evidence']
            elif kind=='json_equals':
                status='pass' if _json_same(loads(final),q['expected']) else 'fail'; why='strict JSON structure and typed numeric/text values'
            elif kind=='number':
                n=loads(final.strip()); status='pass' if _json_same(n,q['expected']) else 'fail'; why='numeric response only; Boolean is not a number'
            elif kind=='exact_text':
                a=final.strip() if q.get('strip_boundary') else final
                status='pass' if a==q['expected'] else 'fail'; why='specified text contract, boundary whitespace only where permitted'
            elif kind=='unchanged':
                status='pass' if actual_after==rec['before'] else 'fail'; why='full workspace path/type/content manifest including ignored entries'
            elif kind=='files_exact':
                expected=dict(rec['before'])
                for path,text in q['expected'].items():
                    expected[path]={'type':'file','sha256':hashlib.sha256(text.encode()).hexdigest()}
                    par=PurePosixPath(path).parent
                    while str(par)!='.': expected[str(par)]={'type':'directory'}; par=par.parent
                compare=dict(actual_after)
                # Only NEW output files may normalize line endings. Existing inputs
                # and editable source files retain their explicitly required bytes.
                if q.get('normalize_newlines'):
                    for name in q['expected']:
                        if name not in rec['before'] and compare.get(name,{}).get('type')=='file':
                            text=safe_child(out/'workspace',name).read_bytes().replace(b'\r\n',b'\n')
                            compare[name]={'type':'file','sha256':hashlib.sha256(text).hexdigest()}
                status='pass' if compare==expected else 'fail'; why='exact authorized delta; all other paths unchanged'
            elif kind=='trigger':
                # Never accept an agent's final claim or a free-form record Boolean.
                if rec['evidence_kind']!='host_run' or not rec.get('trace_complete'):
                    why='native complete host selection evidence unavailable'
                else:
                    obs=observe_trace((out/'trace.jsonl').read_text(),rec['engine'])
                    if obs['selected'] is True:
                        status='pass' if q['expected'] else 'fail'; why='actual Skill tool invocation in captured host events'
                    else: why='no authenticated exhaustive selection observer; negative/unknown cannot be conflated'
        except (ValueError,UnicodeError,KeyError,TypeError) as e:
            status='fail'; why=f'invalid expected output format: {e}'
        results.append({'id':q['id'],'status':status,'critical':q['critical'],'evidence':why})
    counts=collections.Counter(x['status'] for x in results)
    report={'schema_version':2,'case_id':case['id'],'family':case['family'],'mode':case['mode'],
            'condition':rec['condition'],'repetition':rec['repetition'],'evidence_kind':rec['evidence_kind'],
            'run_status':rec['status'],'engine':rec['engine'],'model_requested':rec.get('model'),
            'effort_requested':rec.get('effort'),'reviewer_kind':review.get('reviewer_kind') if review else None,
            'suite_sha256':current,'original_run_suite_sha256':old,
            'regrade_reason':regrade_reason,'results':results,'counts':dict(counts),
            'fully_verified':all(x['status']=='pass' for x in results),
            'comparison_eligible':False,
            'limit':'Native-global-context control and independent semantic judging are not established by this grader.'}
    return report


def summarize(suite, reports, planned_ids=None, rubrics=None):
    if rubrics is None:
        default_suite,rubrics=read_suite()
        if canonical(default_suite)!=canonical(suite):raise ValueError('supply rubrics for nondefault suite')
    current=suite_digest(suite,rubrics)
    ids=set(planned_ids) if planned_ids is not None else {c['id'] for c in suite['cases']}
    if not ids or not ids.issubset({c['id'] for c in suite['cases']}):raise ValueError('unknown/empty plan')
    cases={c['id']:c for c in suite['cases'] if c['id'] in ids}
    expected={(i,condition,r) for i,c in cases.items()
              for condition in (['with_skill'] if c['mode'] in {'native_trigger','native_loading'} else suite['conditions'])
              for r in range(1,suite['repetitions']+1)}
    seen=set(); by_evidence={}; failures=0; environment=None
    for x in reports:
        if not isinstance(x,dict) or x.get('suite_sha256')!=current or x.get('evidence_kind') not in EVIDENCE:
            raise ValueError('foreign or malformed report')
        if type(x.get('repetition')) is not int:raise ValueError('invalid repetition')
        c=case_by_id(suite,x.get('case_id'))
        if x.get('family')!=c['family'] or x.get('mode')!=c['mode']:raise ValueError('case metadata drift')
        expected_checks={q['id']:q for q in all_checks(c,rubrics)}
        results=x.get('results')
        if not isinstance(results,list) or any(not isinstance(q,dict) for q in results):raise ValueError('invalid results')
        result_ids=[q.get('id') for q in results]
        if len(set(result_ids))!=len(result_ids) or set(result_ids)!=set(expected_checks):raise ValueError('missing/duplicate/foreign checks')
        for q in results:
            if type(q.get('critical')) is not bool or q['critical']!=expected_checks[q['id']]['critical']:
                raise ValueError('critical flag drift')
            if q.get('status') not in STATES or not isinstance(q.get('evidence'),str) or not q['evidence'].strip():
                raise ValueError('status/evidence missing')
        env=(x.get('engine'),x.get('model_requested'),x.get('effort_requested'))
        if environment is not None and env!=environment:raise ValueError('mixed model/host/effort strata; summarize separately')
        environment=env
        key=(x['case_id'],x['condition'],x['repetition'])
        if key not in expected or key in seen:raise ValueError('unexpected or duplicate observation')
        seen.add(key)
        bucket=by_evidence.setdefault(x['evidence_kind'],{'trials':0,'pass_checks':0,'fail_checks':0,'not_run_checks':0})
        bucket['trials']+=1
        for q in x['results']:
            if q['status'] not in STATES:raise ValueError('unknown result status')
            if q['status'] in {'pass','fail','not_run'}:bucket[q['status']+'_checks']+=1
            if q['critical'] and q['status']=='fail':failures+=1
    return {'planned_trials':len(expected),'recorded_trials':len(seen),
            'missing_trials':len(expected-seen),'coverage':len(seen)/len(expected),
            'evidence_groups':by_evidence,'critical_failures':failures,
            'native_performance_validated':False,'skill_lift':None,
            'status':'unverified','note':'Coverage of records is not coverage of successful model runs. Evidence groups must not be pooled.'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path,default=DATA)
    sub=p.add_subparsers(dest='action',required=True)
    sub.add_parser('validate'); sub.add_parser('preflight')
    for name in ('prepare','run'):
        q=sub.add_parser(name);q.add_argument('--case',required=True);q.add_argument('--condition',choices=['without_skill','with_skill'],default='with_skill');q.add_argument('--out',type=Path,required=True);q.add_argument('--skill',type=Path,default=SKILL);q.add_argument('--engine',choices=['codex','claude'],default='codex');q.add_argument('--repetition',type=int,default=1)
        if name=='run':
            q.add_argument('--model',required=True);q.add_argument('--effort',choices=['low','medium','high','xhigh','max']);q.add_argument('--timeout',type=int,default=180)
    q=sub.add_parser('grade');q.add_argument('--trial',type=Path,required=True);q.add_argument('--regrade-reason');q.add_argument('--review',type=Path)
    args=p.parse_args(argv)
    try:
        suite,rubrics=read_suite(args.data)
        if args.action=='validate':
            result={'cases':len(suite['cases']),'families':dict(collections.Counter(c['family'] for c in suite['cases'])),
                    'modes':dict(collections.Counter(c['mode'] for c in suite['cases'])),
                    'suite_sha256':suite_digest(suite,rubrics),'scope':'dataset_structure_only','model_runs':0}
        elif args.action=='preflight':
            result={'executables':{x:shutil.which(x) for x in ('codex','claude')},'network':'not_tested','credentials':'not_read','model_runs':0}
        elif args.action=='prepare':
            result=prepare(case_by_id(suite,args.case),args.condition,args.out,args.skill,suite,rubrics,args.engine,args.repetition)
        elif args.action=='run':
            if args.timeout<1:raise ValueError('timeout must be positive')
            result=run_native(case_by_id(suite,args.case),args.condition,args.out,args.skill,suite,rubrics,args.engine,args.model,args.effort,args.timeout,args.repetition)
        else:result=grade(args.trial,suite,rubrics,args.regrade_reason,load(args.review) if args.review else None)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 2 if result.get('status') in {'blocked','error','timeout'} else 0
    except (OSError,ValueError,KeyError) as e:
        print(json.dumps({'error':str(e),'model_pass_claim':False},ensure_ascii=False));return 2

if __name__=='__main__':sys.exit(main())
