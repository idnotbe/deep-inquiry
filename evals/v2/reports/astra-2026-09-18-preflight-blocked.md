# Astra-only evaluation attempt: blocked before model execution

Date: 2026-09-18 (Asia/Seoul).
Status: **blocked; effectiveness unresolved; zero target-model executions**.
This is an execution-environment record, not an evaluation result or a v2 trial record.

## Scope and source identity

The requested comparison was Astra 6 `without_skill` versus Astra 6 `with_skill`
in genuinely separate execution contexts. Fable was explicitly excluded and was
not executed. The coordinating ChatGPT session is not counted as an experimental
execution context.

The repository main commit inspected through the GitHub connection was
`453aff2dd9d2849d4841eb9a37611d9cd5089f4b`.
The v2 README reports 81 cases and targets runtime commit
`84eff2eebef1d8e5b82e9d37612ecaa11c99c666`, with skill digest
`d25ff1e23a5f533ce350f81475f99509fd2748ce66e6c64aae428039cad50b2c`.
That digest was read from the repository, not independently recomputed here.
No suite rebind, runtime edit, case change, grader change, or replacement harness
was made for this attempt.

Repository metadata, the tree, the v2 README, runner source excerpts, and the CI
workflow were inspected. Full case/rubric/skill inspection and final identity
verification were not completed: the execution feasibility gate failed first.
No representative subset was selected and no outcome-dependent sampling occurred.

## Actual execution accounting

| Activity | Count or status |
|---|---|
| Astra `without_skill` model executions | 0 |
| Astra `with_skill` model executions | 0 |
| Matched pairs | 0 |
| Fable model executions | 0; excluded by request |
| Model outputs captured | 0 |
| Independent qualitative grades | 0 |
| Objective behavioral checks on model outputs | 0 |
| Evaluator/unit tests executed locally in this attempt | 0 |
| Current-session answers substituted for trials | 0 |
| Performance, regressions, and effect size | Not measured |

A missing executable or failed environment probe is not a failed model trial.
All pass rates, win/tie/loss rates, clarification rates, format-violation rates,
and effect sizes are undefined, not zero. Existing historical apparatus tests
and any repository CI checks must remain separate from these model-run counts.

## Observed blockers

These observations came from actual environment probes. Credential values were
not read, printed, or committed.

1. `codex` was not on PATH. Attempting `codex --version` raised
   `FileNotFoundError`; no model process started. The usual
   `~/.codex/auth.json` file was absent.
2. `OPENAI_API_KEY`, `CODEX_API_KEY`, `OPENAI_BASE_URL`,
   `AZURE_OPENAI_API_KEY`, and `AZURE_OPENAI_ENDPOINT` were not set.
   An attempted `from openai import OpenAI` failed with
   `ImportError: cannot import name 'OpenAI' from 'openai' (unknown location)`.
   Package-name discoverability did not establish a usable SDK. No API request
   was sent and no new API billing or credentials were provisioned.
3. Resolving `api.openai.com` from the execution container failed with
   `gaierror: [Errno -3] Temporary failure in name resolution`.
   A public Git clone separately failed because `github.com` could not be
   resolved. GitHub connector reads nevertheless worked; connector access is
   not evidence that the execution container has network access.
4. No callable isolated-model/session-spawn tool was available to the coordinator.
   Plugin discovery returned an uninstalled OpenAI Developers integration, not
   a verified, connected Astra execution service. No plugin was installed and
   no unverified plugin capability was counted as available.

These are observations about this execution environment, not claims that Astra
or Codex is unavailable generally or on the user's own computer. Installing a
CLI alone would not establish authentication, model access, clean profiles,
network access, or matched execution conditions.

## Evaluation integrity and limitations

Having Astra coordinate this task does not create two isolated Astra contexts.
The current conversation already contains evaluation instructions and repository
material. Writing both answers here and labeling them with/without the skill
would not remove that context, establish native loading, or provide independent
model execution. No such answers were generated or graded.

No evidence supports improvement, degradation, equivalence, task-family effects,
trigger precision, reference-loading behavior, or state-preservation behavior.
No runtime-skill defect or evaluator-validity defect was inferred from the host
blockers. There was no first real run to adversarially review, and no claim is
made that the requested post-run P0/P1 review or full verification was completed.

A self-check of this report rejected three misleading interpretations: counting
preflight failures as model failures, treating SDK module detection as working
inference access, and treating an uninstalled plugin listing as a functioning
executor. This report self-check is not independent grading of model behavior.

## Required execution boundary

Resume only in an environment that can actually launch authorized independent
Astra sessions, for example an authenticated Codex runner with controlled
per-trial profiles/workspaces. Confirm the actual model snapshot, host, effort,
tools, permissions, and budget in both conditions; keep rubrics, other cases,
and previous outputs outside execution contexts. Use the existing v2 suite and
runner, with independent evidence-based grading. Native loading/trigger and
multi-turn capabilities still require the host evidence described in the
[v2 README](../README.md).

The immediate missing capability is **callable isolated Astra execution**, not
another model and not another set of simulated answers. Effectiveness remains
unresolved until that capability is available and matched trials actually run.
