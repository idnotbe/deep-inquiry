# Sources and adaptation ledger

Reviewed 2026-09-18, Asia/Seoul. Public benchmarks were inspected before new cases.
Existing task-specific definitions are the preferred base, not replaced merely to
increase counts. Runtime instructions and private uploaded conversations are not
copied into the public dataset. Every prompt here is synthetic.

## Reused task data

Repository: https://github.com/idnotbe/deep-inquiry
Fixed source commit: `84eff2eebef1d8e5b82e9d37612ecaa11c99c666`.

| Original | Source blob | v2 mapping | Adaptation |
|---|---|---|---|
| evals/behavior-suite.json | `4c293797fe1da9ea4a1dcf53568a3a2359af3257` | B01-B33 | Preserve task/exception, separate judge, add family/mode/contrast labels; make hypothetical state explicit |
| evals/model-suite.json | `e4b9f0506ef40c047953bd38afff36d12f1d7ee3` | P01-P12 | Preserve model-profile boundaries; machine-check P07; retain planning-only semantics |
| evals/trigger-suite.json | `ca18cb0b31aa681e82b4c77b3c466125b87b18f8` | T01-T06 | Retain original prompts/expectations; separate actual native detection from outcome quality |

This is 51 adapted cases, not 51 previous successful trials. Original files remain
unchanged. Original private v3 prompting can be added as an explicitly supplied
third experimental condition, but is not a dependency of this public two-condition
suite. Two provider-specific models must be evaluated in separate strata.

## Public reusable template

SkillBench, helloJamest (different project from benchflow-ai/skillsbench):
https://github.com/helloJamest/SkillBench/blob/main/examples/eval_packs/generic-skill-release.json

Source blob `ffcb6ee28d3ea3a3ef98076364be0f327a49be4b`, template id
`generic-skill-release-v1`, generator version `0.5.7`. MIT license blob
`1dd1570e6ad9894ba658d0e9b209d44da34549ed`; notice in [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md).

| Template pattern | Concrete adaptation |
|---|---|
| release-positive-trigger | T07 Korean explicit request; complement original positive controls |
| release-negative-routing | T08 explanation-only and N16 proportional resource selection |
| release-workflow-depth | N11 two operational mechanisms, ordinary/failure cases |
| release-safety-boundary | T09 quoted command and N07 source-injected overwrite with protected file |
| release-evidence-review | N09 superseding source scope and N22 unsupported test-success claim |
| tooling, ambiguous-routing, maintenance dimensions | Coverage design and static/ownership checks; not extra unexecuted task scores |

The upstream pack is judge-only and contains broad authoring criteria. We adapted
its dimensions and case patterns, not its generic scores. Native activation and
actual task artifacts replace text-only claims where our environment permits them.
No upstream benchmark score is claimed.

## Primary methodological sources (not imported datasets)

- SkillsBench: https://github.com/benchflow-ai/skillsbench . Reused fixed task/environment,
  oracle and verifier separation as a design pattern; no Docker images, full task
  corpus or original leaderboard was executed or copied.
- OpenAI, *Testing Agent Skills Systematically with Evals*:
  https://developers.openai.com/blog/eval-skills . Reused outcome/process/style/efficiency
  distinction, small controlled scratch tasks and artifacts plus traces. N05/N08
  specialize this pattern rather than importing its React demo.
- Anthropic, *Demystifying evals for AI agents*, 2026-01-09:
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents . Reused
  balanced positive/negative controls, multi-grader evidence and evaluation debugging.
- Anthropic skill-creator trigger runner:
  https://github.com/anthropics/skills/blob/main/skills/skill-creator/scripts/run_eval.py .
  Inspected its approach; did not execute or vendor it. Primary issue reports
  https://github.com/anthropics/skills/issues/1559 and
  https://github.com/anthropics/skills/issues/1352 describe early negative detection
  and shared-workspace contamination. These are attributed reports, not universal
  measured defects here. Local synthetic regression tests independently exercise
  those failure shapes in our own parser and workspace implementation.
- OpenAI CLI reference: https://developers.openai.com/codex/cli/reference .
- Claude Code CLI reference: https://code.claude.com/docs/en/cli-reference .
- Claude Code skills and visibility: https://code.claude.com/docs/en/skills .
  CLI commands/settings are source-informed, not live-host validated in this session.

External links are development provenance, not runtime skill dependencies.
