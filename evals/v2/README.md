# Deep Inquiry evaluation v2

**Status: executable dataset and grader candidate; target-model validation incomplete.**
The current session ran fixture actions, graded authored answers, mutated incorrect
outputs, and tested the evaluator. It could not start isolated Astra or Fable
sessions: neither native CLI is installed here. No native success rate, creativity
lift, trigger precision/recall or cross-model ranking is claimed.

The runtime skill is unchanged. This suite targets commit
`84eff2eebef1d8e5b82e9d37612ecaa11c99c666`, canonical skill digest
`d25ff1e23a5f533ce350f81475f99509fd2748ce66e6c64aae428039cad50b2c`.
A new skill version requires a deliberate suite rebind, not silently mixing results.

## Coverage before case construction

| Family | Primary question | Counter-control |
|---|---|---|
| Discovery | Does explicit invocation work in the configured native host? | Mentions, quotations, ordinary tasks and explicit-only implicit requests |
| Alignment | Does it confirm genuinely different problem meanings? | Previously confirmed scope and delegated execution must proceed |
| Inquiry | Are premises, mechanisms, constraints and practical burden examined? | Conventional correct solutions must be allowed to win |
| Evidence | Are claims supported, bounded and action-relevant? | Unavailable data stays unknown; changed assumptions change the answer |
| Verification | Is criticism checked and evidence bound to the actual candidate? | Unsupported criticism does not force a revision; stale passes are rejected |
| Lifecycle | Are decisions, R/X, pauses and final acceptance preserved? | Exhaustion, missing state, rollback and production/pilot distinctions |
| Coordination | Are writers, independent work and checkpoints handled correctly? | Healthy and obsolete workers; supplied-state advice is not a live scheduling trace |
| Tool behavior | Are actual files correctly changed and verified? | Unchanged files, ignored files, directories and exact authorized diffs |
| Safety | Do source instructions fail to expand authority? | Read-only work, injected overwrite commands, missing approval |
| Direct/format | Can simple tasks stay simple and exact? | Numeric-only, JSON, Python code, translations, table-only requests |
| Host profile | Is model guidance distinguished from actual settings/capabilities? | Unknown models and cross-provider handoffs |
| Disclosure | Are relevant resources loaded at the right time? | Simple tasks versus substantive inquiry; observe reads separately from activation |

`cases.json` has 81 cases across 13 family labels: 51 adapted existing B/P/T cases,
plus 30 additions. All original dataset files remain available and unchanged.
There are 43 response cases, 18 planning cases, 4 workspace cases, 2 scripted
multi-turn cases, 12 native-trigger cases and 2 native-loading cases. Only 4 are
live filesystem exercises; the planning cases do not establish live orchestration.
Language variants and contrast groups are correlated controls, not independent
scientific samples. Family counts are not weights in an overall quality score.

## Reuse and benchmark selection

See [sources](SOURCES.md) for exact provenance, licensing and adaptation choices.
The existing task contracts are the primary reusable data. SkillBench's MIT generic
release pack supplies dimensions and boundary/evidence patterns. SkillsBench and
OpenAI's skill-evaluation guide inform the fixed-fixture/oracle/trace separation.
We did not run or import the entire SkillsBench benchmark or its leaderboard score.
A generic third-party skill-authoring score would not measure this skill's inquiry
quality, and a description-only classifier would not measure native invocation.

## Separation of task, judge and experiment

`cases.json` contains fixed prompts and synthetic fixtures. `rubrics.json` contains
expectations and independent check definitions. The runner exports only prompt,
fixture and scripted user replies; it never sends the judge file or source labels
to the execution agent. Keep the repository and all other cases OUTSIDE the
execution workspace. Public cases are not secret holdouts. Add private final cases
before claiming generalization; do not develop against their outputs.

For each target model separately, compare `without_skill` and `with_skill` with the
same task, actual model snapshot, effort, tools, permissions, deadlines and input
bytes. The intentional difference is installation and explicit method invocation.
Use separate fresh sessions and vary order across repetitions. Default repetitions
are three, not a statistical confidence guarantee. Do not pool model/host/effort
strata or the two different providers. Capture the actual model (including any
fallback) from host evidence: the runner's `model` field is only the requested ID.

The native adapter creates a fresh workspace, not a security boundary or a clean
user profile. Ambient global instructions, skills, plugins, memory and managed
policy require an externally controlled disposable profile/sandbox. `without_skill`
contains no project skill, but that alone does NOT establish a clean baseline.
Never point a trial at real credentials, customer files or a production repository.
The runner does not discover credentials, install software, enable API billing,
change saved user settings or bypass permissions.

## Commands

Python 3.10+ standard library, run from the repository root:

```bash
python -B -m unittest discover -s tests -v
python -B tools/eval_v2.py validate
python -B tools/eval_v2.py preflight
```

With an already installed, authorized CLI and an externally isolated profile:

```bash
python -B tools/eval_v2.py run --case N21 --condition with_skill --engine codex --model MODEL_ID --repetition 1 --out ../trials/astra-N21-with-1
python -B tools/eval_v2.py run --case N21 --condition without_skill --engine codex --model MODEL_ID --repetition 1 --out ../trials/astra-N21-without-1
python -B tools/eval_v2.py grade --trial ../trials/astra-N21-with-1
```

Use `--engine claude` for Claude Code, and supply the actual model identifier
selected in your environment. `--effort` and `--timeout` are explicit options.
Do not infer that similarly named effort levels mean equal compute across models.
Repeat with new output directories and repetition 2/3. Existing trial directories
are never overwritten. A blocked/error/timeout run exits 2, not a model failure.
`grade` exit 0 means a valid report was produced, NOT that all checks passed.
Inspect every result and unresolved check; unknown must not become a pass.

Claude uses its documented user-only visibility setting for the scratch invocation
without editing the shared skill. Only Read/Write/Edit/Skill built-ins are exposed;
MCP is disabled. This profile does not provide shell execution, so executable-code
verification requiring a shell needs a separately defined, authorized environment.
Codex uses workspace-write sandboxing. These adapters are source-informed and
parser-tested, but not live-smoke-tested in this revision. Validate your CLI version
and capture its settings before using results. Timeout terminates the parent process;
external sandbox lifecycle management must contain and clean descendants.

`prepare` creates the same packet without invoking a model. It is useful for a
manual/native harness, but preparing a packet is not executing it.

## What is scored, and what stays unknown

Objective graders inspect strict typed JSON, arithmetic-only output, exact text,
complete path/type/content inventories, or exact authorized file changes. New CSV
outputs may normalize CRLF/LF only where explicitly allowed; protected input bytes
cannot change. Empty directories, ignored paths, additions, deletions and symlinks
are included. Before/after equality does not prove there was no attempted network
call or transient write: review the actual action transcript as well.

Qualitative checks use observable artifacts and concise evidence. Accept any
mechanism that satisfies the criteria; do not require the author's preferred
business framework, vocabulary, number of lenses, role names or lengthy reasoning.
Distinguish premise validity, practical mechanism, differing alternatives,
confirmation boundaries and usefulness. Novelty alone cannot offset a hard failure.
Do not request or grade private chain-of-thought.

For a semantic review, write a separate JSON object with `suite_sha256`,
`artifact_sha256` (from `review_binding(record)`), `reviewer_kind` (`self_review`,
`human_review`, or `independent_model_review`), a nonempty `reviewer`, and `checks`
containing `id`, `status`, `evidence`. Pass it using `grade --review PATH`. Only
`kind=review` checks may be supplied; machine checks cannot be overridden. Missing
reviews stay `not_run`. A hash binds bytes but does not authenticate the reviewer
or prove their reasoning. Blind/randomize genuine independent reviews where feasible.

For calibration, include a valid alternative, plausible but infeasible mechanism,
unsupported confident answer, faithful unknown, and correct terse answer. Challenge
both false acceptance and false rejection. A judge who rewards its own preferred
solution is an evaluator defect, not a skill defect. Preserve model failures while
correcting real rubric mistakes; regrade both experimental conditions under the
same corrected rubric. Changed task inputs require new runs, not regrading.

### Native invocation and loading

Keep invocation separate from material access and task completion. The conservative
Claude parser scans the entire trace, so an unrelated first tool or another skill
cannot terminate detection early. It recognizes an affirmative exact Skill call.
A missing Skill event is UNKNOWN because manual invocation can inject content
without that event. Codex command reads are not treated as automatic activation.
The current parser therefore does not compute reliable negative trigger outcomes.

Before grading negative cases, establish a complete native selection observer for
the specific host/version and bind its logs. Manually inspect native expansion/read
events or provide a separately verified adapter. Quoted command tests may expose
host preprocessing rather than the model's selection; report which layer acted.
Never substitute a model's statement that it used a skill or a description classifier.
For N17/N18, inspect genuine resource-read events and order separately; a filename
mention, correct answer or source-code link is not evidence that a reference loaded.
The two loading cases and unresolved trigger evidence remain `not_run` in this release.

### Multi-turn cases

The lightweight CLI runner deliberately blocks N14/N15 pending a conversation driver.
Run these manually in a fresh native session: give only turn 1, save the actual
response/trace, then send the fixed `followup_user_turns` message in the SAME session.
Do not supply the answer early or restart with a synthetic summary. Judge each turn,
pause boundary, preserved constraints and resumed R/X state. Record transcript and
artifacts for both turns. A one-turn explanation of what would happen is not a pass.

## Reporting and release gate

Report by family, task mode and evidence kind, with all planned repetitions in the
coverage denominator. The full plan has 444 condition/repetition slots per model
(67 ordinary cases times 2 conditions times 3, plus 14 native cases times 3).
The summarizer separates `host_run`, `current_session_exercise`, `fixture_oracle`
and `blocked`; it refuses duplicate/foreign checks, rubric drift and mixed model
strata. Its conservative `native_performance_validated` remains false and `skill_lift`
null; independent review and environmental matching must be established separately.

One critical failure or an unresolved required check blocks a full validation
claim. Do not average it away. Report raw differences and uncertainty for matched
comparisons; do not claim significance from these small correlated cases. Record
latency/tokens/tool reads only where actual supported telemetry exists. The parser's
tool count covers only recognized events, not guaranteed exhaustive tool usage.

[Review and results](REVIEW.md) records executed work, evaluator fixes and limitations.
[Current-session summary](reports/current-session.json) records the contaminated
exercises, including failures. It is not an Astra/Fable benchmark score.
