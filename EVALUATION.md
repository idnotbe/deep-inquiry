# Evaluate deep-inquiry

The current evaluation entry point is [evaluation v2](evals/v2/README.md).
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
No runtime skill file was changed for the evaluation.

**Do not interpret evaluator test passes as native model performance.**
The current session ran 21 rubric-visible exercises and actual synthetic file
operations, not isolated Astra/Fable evaluations. Two format failures are retained.
Both native CLI preflights were blocked by missing executables. Native discovery,
loading, multi-turn behavior and clean-profile matched model comparisons remain
unverified. The dataset/grader is a candidate pending that host validation.
