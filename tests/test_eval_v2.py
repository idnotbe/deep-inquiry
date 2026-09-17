"""Executable dataset/grader calibration, NOT native LLM evaluation."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import eval_v2 as e


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.s,self.r=e.read_suite()
        self.tmp=tempfile.TemporaryDirectory()
        self.base=Path(self.tmp.name)
        self.n=0
    def tearDown(self):self.tmp.cleanup()
    def trial(self,cid='N21',text='240',kind='fixture_oracle',mutate=None):
        self.n+=1; out=self.base/str(self.n)
        c=e.case_by_id(self.s,cid)
        rec=e.prepare(c,'with_skill',out,e.SKILL,self.s,self.r)
        if mutate:mutate(out/'workspace')
        rec.update(status='completed',evidence_kind=kind,grader_exposed=True)
        e.finalize(out,rec,text,'','')
        return out
    def local(self,out):
        return {x['id']:x['status'] for x in e.grade(out,self.s,self.r)['results']}
    def test_valid_suite_and_unchanged_runtime(self):
        self.assertEqual(e.validate(self.s,self.r),[])
        self.assertEqual(e.skill_digest(e.SKILL),self.s['target_skill_sha256'])
    def test_reused_ids_and_balanced_modes(self):
        ids={c['id'] for c in self.s['cases']}
        self.assertTrue({f'B{i:02}' for i in range(1,34)} <= ids)
        self.assertTrue({f'P{i:02}' for i in range(1,13)} <= ids)
        self.assertTrue({f'T{i:02}' for i in range(1,7)} <= ids)
        self.assertEqual({c['mode'] for c in self.s['cases']},e.MODES)
    def test_export_keeps_rubric_out(self):
        c=copy.deepcopy(e.case_by_id(self.s,'B04'));c['expected']='SECRET';c['checks']='SECRET'
        req=e.request(c,'with_skill')
        self.assertEqual(set(req),{'prompt','fixture','followup_user_turns'})
        self.assertNotIn('SECRET',json.dumps(req))
    def test_unknown_case(self):
        with self.assertRaises(ValueError):e.case_by_id(self.s,'Z99')
    def test_nonobjects(self):
        for value in (None,[],True,'text'):
            self.assertTrue(e.validate(value,self.r)); self.assertTrue(e.validate(self.s,value))
    def test_duplicate_case_or_rubric_ids(self):
        self.s['cases'].append(copy.deepcopy(self.s['cases'][0]));self.assertTrue(e.validate(self.s,self.r))
    def test_missing_local_criteria(self):
        self.r['cases']['N21']['checks']=[];self.assertTrue(e.validate(self.s,self.r))
    def test_empty_review_rejected(self):
        self.r['common_checks'][0]['criterion']='';self.assertTrue(e.validate(self.s,self.r))
    def test_nonfinite_json_and_duplicate_keys_rejected(self):
        for text in ('NaN','Infinity','{"a":1,"a":2}'):
            with self.assertRaises(ValueError):e.loads(text)
    def test_bad_repetitions(self):
        for value in (True,0,-1,1.5):
            s=copy.deepcopy(self.s);s['repetitions']=value;self.assertTrue(e.validate(s,self.r))
    def test_path_safety(self):
        for name in ('../x','/tmp/x','a/../x','a\\x','CON.txt','a.','a//b','a/./b'):
            self.assertFalse(e.safe_name(name),name)
    def test_fixture_file_directory_collision(self):
        self.s['cases'][0]['fixture']={'data':'x','data/file':'y'};self.assertTrue(e.validate(self.s,self.r))
    def test_fixture_case_collision(self):
        self.s['cases'][0]['fixture']={'Data.txt':'x','data.txt':'y'};self.assertTrue(e.validate(self.s,self.r))
    def test_reserved_host_paths(self):
        for path in ('.git/config','.claude/skills/a.md','.agents/skills/a.md','AGENTS.md','CLAUDE.md'):
            self.s['cases'][0]['fixture']={path:'bad'};self.assertTrue(e.validate(self.s,self.r))
    def test_prepare_refuses_overwrite(self):
        out=self.trial()
        with self.assertRaises(ValueError):e.prepare(e.case_by_id(self.s,'N21'),'with_skill',out,e.SKILL,self.s,self.r)
    def test_each_trial_is_isolated(self):
        a=self.trial();b=self.trial()
        (a/'workspace/extra').write_text('one')
        self.assertFalse((b/'workspace/extra').exists())
    def test_numeric_oracle(self):
        for output,status in [('240','pass'),('240.0','pass'),('239','fail'),('true','fail'),('240 seconds','fail'),('"240"','fail')]:
            self.assertEqual(self.local(self.trial(text=output))['seconds'],status)
    def test_extreme_numeric_output_fails_without_crashing(self):
        self.assertEqual(self.local(self.trial(text='9'*1000))['seconds'],'fail')
    def test_boolean_not_numeric_zero(self):self.assertFalse(e._json_same(False,0))
    def test_json_extra_field_rejected(self):
        out=self.trial('N20','{"East":40,"West":60,"extra":1}')
        self.assertEqual(self.local(out)['allocation'],'fail')
    def test_parallel_counterexample(self):
        wrong='{"before":120,"after":96,"saved":24,"improvement_percent":20}'
        right='{"before":90,"after":90,"saved":0,"improvement_percent":0}'
        self.assertEqual(self.local(self.trial('N02',wrong))['numbers'],'fail')
        self.assertEqual(self.local(self.trial('N02',right))['numbers'],'pass')
    def test_format_no_fences(self):
        code=self.r['cases']['P07']['checks'][-1]['expected']
        self.assertEqual(self.local(self.trial('P07',code))['code'],'pass')
        self.assertEqual(self.local(self.trial('P07','```python\n'+code+'\n```'))['code'],'fail')
    def test_readonly_good_and_ignored_change(self):
        self.assertEqual(self.local(self.trial('N06'))['readonly'],'pass')
        out=self.trial('N06',mutate=lambda w:(w/'cache/new.txt').write_text('extra'))
        self.assertEqual(self.local(out)['readonly'],'fail')
    def test_empty_directory_and_deletion_are_changes(self):
        for change in (lambda w:(w/'empty').mkdir(),lambda w:(w/'calculator.py').unlink()):
            self.assertEqual(self.local(self.trial('N06',mutate=change))['readonly'],'fail')
    def test_symlink_not_followed(self):
        out=self.trial('N06');w=out/'workspace'
        try:(w/'link').symlink_to(self.base/'missing')
        except OSError as exc:self.skipTest(str(exc))
        self.assertEqual(e.inventory(w)['link']['type'],'symlink')
    def test_full_expected_patch(self):
        def fix(w):
            p=w/'calculator.py';p.write_bytes(p.read_bytes().replace(b'a - b',b'a + b'))
        self.assertEqual(self.local(self.trial('N05',mutate=fix))['patch'],'pass')
        self.assertEqual(self.local(self.trial('N05'))['patch'],'fail')
    def test_patch_cannot_change_other_file(self):
        def wrong(w):
            p=w/'calculator.py';p.write_bytes(p.read_bytes().replace(b'a - b',b'a + b'))
            (w/'notes.txt').write_text('rewritten')
        self.assertEqual(self.local(self.trial('N05',mutate=wrong))['patch'],'fail')
    def test_new_csv_allows_crlf_but_protected_input_does_not(self):
        text=self.r['cases']['N08']['checks'][-1]['expected']['result.csv']
        def correct(w):(w/'result.csv').write_bytes(text.replace('\n','\r\n').encode())
        self.assertEqual(self.local(self.trial('N08',mutate=correct))['files'],'pass')
        def wrong(w):
            correct(w);p=w/'records.csv';p.write_bytes(p.read_bytes().replace(b'\n',b'\r\n'))
        self.assertEqual(self.local(self.trial('N08',mutate=wrong))['files'],'fail')
    def test_artifact_tampering(self):
        out=self.trial();(out/'final.txt').write_text('wrong')
        with self.assertRaises(ValueError):e.grade(out,self.s,self.r)
    def test_workspace_tampering(self):
        out=self.trial();(out/'workspace/hidden').write_text('new')
        with self.assertRaises(ValueError):e.grade(out,self.s,self.r)
    def test_rubric_change_requires_explicit_regrade(self):
        out=self.trial();r=copy.deepcopy(self.r);r['cases']['N21']['checks'][0]['criterion']+=' Clarification.'
        with self.assertRaises(ValueError):e.grade(out,self.s,r)
        report=e.grade(out,self.s,r,regrade_reason='Clarified rubric without changing task.')
        self.assertNotEqual(report['suite_sha256'],report['original_run_suite_sha256'])
    def test_changed_input_cannot_be_regraded(self):
        out=self.trial();s=copy.deepcopy(self.s);e.case_by_id(s,'N21')['prompt']='Different task'
        with self.assertRaises(ValueError):e.grade(out,s,self.r,regrade_reason='not allowed')
    def test_empty_observation_cannot_pass(self):
        out=self.trial();rec=e.load(out/'record.json');rec['status']='timeout';e.write(out/'record.json',rec)
        self.assertTrue(all(q['status']=='not_run' for q in e.grade(out,self.s,self.r)['results']))
    def test_semantics_not_inferred_from_artifact(self):
        rep=e.grade(self.trial(),self.s,self.r)
        self.assertFalse(rep['fully_verified']);self.assertFalse(rep['comparison_eligible'])
    def test_native_missing_runner_is_blocked(self):
        for engine in ('codex','claude'):
            with patch('shutil.which',return_value=None):
                rec=e.run_native(e.case_by_id(self.s,'N21'),'with_skill',self.base/engine,e.SKILL,self.s,self.r,engine,'user-selected-model')
            self.assertEqual(rec['status'],'blocked');self.assertEqual(rec['evidence_kind'],'blocked')
    def test_trace_scans_past_unrelated_tools(self):
        events=[{'type':'assistant','message':{'content':[{'type':'tool_use','name':'Bash','input':{}}]}},
                {'type':'assistant','message':{'content':[{'type':'tool_use','name':'Skill','input':{'skill':'other'}}]}},
                {'type':'assistant','message':{'content':[{'type':'tool_use','name':'Skill','input':{'skill':'deep-inquiry'}}]}},
                {'type':'result','subtype':'success','result':'done'}]
        obs=e.observe_trace('\n'.join(map(json.dumps,events)),'claude')
        self.assertIs(obs['selected'],True);self.assertTrue(obs['complete']);self.assertEqual(obs['tool_calls'],3)
    def test_trace_absence_and_model_claim_are_unknown(self):
        raw=json.dumps({'type':'result','subtype':'success','result':'I used deep-inquiry'})
        self.assertIsNone(e.observe_trace(raw,'claude')['selected'])
    def test_incomplete_error_and_malformed_traces(self):
        for raw in ('',json.dumps({'type':'assistant','message':{'content':[]}}),'bad json',json.dumps({'type':'result','is_error':True})):
            self.assertFalse(e.observe_trace(raw,'claude')['complete'])
    def test_malformed_message_returns_diagnostic(self):
        obs=e.observe_trace(json.dumps({'type':'assistant','message':None}),'claude')
        self.assertFalse(obs['complete']);self.assertTrue(obs['errors'])
    def test_trace_error_not_overridden_by_record(self):
        out=self.base/'traceerror'
        rec=e.prepare(e.case_by_id(self.s,'T01'),'with_skill',out,e.SKILL,self.s,self.r,'claude')
        rec.update(status='completed',evidence_kind='host_run',trace_complete=True,exit_code=0)
        raw='\n'.join(map(json.dumps,[{'type':'assistant','message':{'content':[{'type':'tool_use','name':'Skill','input':{'skill':'deep-inquiry'}}]}},{'type':'result','is_error':True}]))
        e.finalize(out,rec,'',raw,'')
        self.assertEqual(self.local(out)['trigger'],'not_run')
    def test_summary_duplicate_rejected(self):
        rep=e.grade(self.trial(),self.s,self.r)
        with self.assertRaises(ValueError):e.summarize(self.s,[rep,rep],planned_ids=['N21'])
    def test_summary_missing_checks_rejected(self):
        rep=e.grade(self.trial(),self.s,self.r);rep['results']=[]
        with self.assertRaises(ValueError):e.summarize(self.s,[rep],planned_ids=['N21'],rubrics=self.r)
    def test_summary_mixed_suite_rejected(self):
        rep=e.grade(self.trial(),self.s,self.r);rep['suite_sha256']='0'*64
        with self.assertRaises(ValueError):e.summarize(self.s,[rep],planned_ids=['N21'],rubrics=self.r)
    def test_summary_separates_evidence_and_missing(self):
        rep=e.grade(self.trial(),self.s,self.r)
        summary=e.summarize(self.s,[rep],planned_ids=['N21'])
        self.assertEqual(summary['missing_trials'],5);self.assertIn('fixture_oracle',summary['evidence_groups'])
        self.assertIsNone(summary['skill_lift']);self.assertFalse(summary['native_performance_validated'])


    def test_initial_manifest_tampering_rejected(self):
        out=self.trial('N06');rec=e.load(out/'record.json');rec['before']={};e.write(out/'record.json',rec)
        with self.assertRaises(ValueError):e.grade(out,self.s,self.r)
    def test_requested_repetition(self):
        rec=e.prepare(e.case_by_id(self.s,'N21'),'with_skill',self.base/'rep3',e.SKILL,self.s,self.r,repetition=3)
        self.assertEqual(rec['repetition'],3)
        with self.assertRaises(ValueError):e.prepare(e.case_by_id(self.s,'N21'),'with_skill',self.base/'rep4',e.SKILL,self.s,self.r,repetition=4)
    def test_current_review_is_not_native_lift(self):
        out=self.trial(kind='current_session_exercise');rec=e.load(out/'record.json')
        review={'suite_sha256':e.suite_digest(self.s,self.r),'artifact_sha256':e.review_binding(rec),'reviewer_kind':'self_review','reviewer':'current author','checks':[{'id':q['id'],'status':'pass','evidence':'Inspected literal 240 and the unchanged synthetic workspace; same-author review.'} for q in e.all_checks(e.case_by_id(self.s,'N21'),self.r) if q['kind']=='review']}
        report=e.grade(out,self.s,self.r,review=review)
        self.assertTrue(report['fully_verified']);self.assertFalse(report['comparison_eligible']);self.assertEqual(report['reviewer_kind'],'self_review')
        review['artifact_sha256']='0'*64
        with self.assertRaises(ValueError):e.grade(out,self.s,self.r,review=review)
    def test_review_cannot_override_machine_checks(self):
        out=self.trial();rec=e.load(out/'record.json')
        review={'suite_sha256':e.suite_digest(self.s,self.r),'artifact_sha256':e.review_binding(rec),'reviewer_kind':'self_review','reviewer':'author','checks':[{'id':'seconds','status':'pass','evidence':'trust me'}]}
        with self.assertRaises(ValueError):e.grade(out,self.s,self.r,review=review)
    def test_summary_rejects_mixed_environments(self):
        a=e.grade(self.trial(),self.s,self.r);b=copy.deepcopy(a);b['repetition']=2;b['model_requested']='other-model'
        with self.assertRaises(ValueError):e.summarize(self.s,[a,b],rubrics=self.r)
    def test_no_skills_in_baseline_workspace(self):
        rec=e.prepare(e.case_by_id(self.s,'N21'),'without_skill',self.base/'baseline',e.SKILL,self.s,self.r)
        self.assertEqual(rec['skill_sha256'],'no_skill');self.assertEqual(rec['before'],{})
    def test_prepare_is_read_only_for_original_skill(self):
        before=e.inventory(e.SKILL);self.trial();self.assertEqual(before,e.inventory(e.SKILL))

if __name__=='__main__':unittest.main()
