# Evaluate deep-inquiry

The [response-quality evaluation design v3](evals/v3/README.md) assesses the
[inquiry capabilities](docs/evaluation-purpose.md) through baseline-only
difficulty screening followed by separate frozen confirmation instances.
Its task-specific scoring views assess supported recommendations, mechanisms,
constraints and decision-relevant evidence, rather than response length or
checklist wording. Run `python -B tools/eval_inquiry.py validate --suite evals/v3`
to validate definitions; this command does not execute or score a model.

All three screening pools were retired for insufficient valid difficult-family
coverage. No difficult core is active and no scored skill comparison ran.

The [current response-quality report](evals/v3/reports/2026-09-30-gpt-6-sol-medium.md)
records actual screening, exclusions and any completed comparison separately.

The v2 accounts below remain historical and regression evidence outside the
v3 core score.

The frozen evaluation v2 dataset and grader are documented in
[evaluation v2](evals/v2/README.md). Its session account is historical.
It reuses all 51 existing B/P/T case IDs and adds 30 cases, fixed filesystem
fixtures, typed output graders, conservative native trace parsing and 51 evaluator
regression tests. The legacy `evals/README.md` and original suites describe the
previous planning-only package; they are preserved unchanged for provenance.

```bash
python -B -m unittest discover -s tests -v
python -B tools/eval_v2.py validate
python -B tools/eval_v2.py preflight
```

Read [sources](evals/v2/SOURCES.md), [review findings](evals/v2/REVIEW.md), and
[actual exercise results](evals/v2/reports/current-session.json).
No runtime skill file was changed for that earlier 21-exercise session.

Historical mixed-task report: [requested gpt-6-sol / medium diagnostic](evals/v2/reports/2026-09-30-gpt-6-sol-medium.md) (96 original responses, 77/96 descriptive semantic outcome passes, plus a separate six-response skill-revision diagnostic whose candidate was reverted; comparative skill effect unverified). The 21-exercise account below records the earlier evaluation session.

**Do not interpret evaluator test passes as native model performance.**
That earlier session ran 21 rubric-visible exercises and actual synthetic file
operations, not isolated Astra/Fable evaluations. Two format failures are retained.
At that time, both native CLI preflights were blocked by missing executables. Native discovery,
loading, multi-turn behavior and clean-profile matched model comparisons remained
unverified. The dataset/grader is a candidate pending comparative host validation.
