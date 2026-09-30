# Response-quality evaluation v3 candidate

This candidate tests defensible recommendations under supplied constraints. It has twelve dilemma families, each with one calibration instance (C01–C12) and a distinct confirmation instance (H01–H12), plus three conventional-winning controls (K01–K03). Every prompt is self-contained and requests at most 700 words; no external tools or facts are needed.

The round-one revision replaces supplied recipes with interacting timing, authority, cancellation, identity and capacity decisions. Quantitative probes require contingent policy choice after noisy/exact tests and include measurement fees and time; the last family now compares complementary shared investments with local purchases and a changed-downtime reversal. Arithmetic and feasibility are writer-checked, but empirical difficulty remains NOT_RUN until baseline screening.

The five task-specific dimensions each score 0, 1 or 2, for a total of ten. Full pass requires at least eight and no critical failure. Judge the final response only. Accept other feasible justified answers, including terse answers. Do not reward framework names, verbosity, novelty or unnecessary alternatives. Controls use the same five dimensions but stay outside the difficult-core result.

## Selection and confirmation

Freeze cases, rubrics, protocol, root skill and the three inquiry references after two independent review rounds, before any model output. The private illustrative feasibility answers are in `temp/2026-09-30-rebuild/oracles.json`; their author does not count as an independent validator.

Run three fresh baseline-only calibration trials per family. Exclude a family when at least two full-pass, or the normalized mean exceeds 0.70. A zero-pass family requires independent feasibility/clarity validation. Missing trials remain NOT_RUN and make selection incomplete; never count them as failures or replace them after dispatch.

If fewer than six families qualify, report insufficient difficult-core coverage. Revise one candidate prospectively from baseline evidence, review and freeze a new version while preserving all earlier screening records. A neutral delivery canary may run before selection; scored treatment may not. Freeze status belongs in a separate hashed runtime record, without mutating public frozen inputs after dispatch.

Run every selected family's frozen H instance three times in each arm, using a fresh baseline and matched native sessions. Preserve all outcomes and do not filter on confirmation performance. Both instance sets are writer-seen; “confirmation” describes their frozen evaluation role and does not mean an inaccessible holdout. Family structure transfers across splits; no unseen-family transfer claim is justified.

The controls change the governing condition so simple conventional action wins: verified contractual allocation, a true preparation bottleneck, and a decisive existing test. These remain reported even if easy. They are descriptive reversal checks, with changed scenario details.

## Treatment and runtime

Request `gpt-6-sol` at `medium` in the native host, with a 300-second timeout. The captured native order is task, preloaded frozen inquiry-methods, evidence-and-diagnosis, alternatives-and-drafting texts, then native root SKILL expansion named `deep-inquiry:deep-inquiry`. Verify that order, exact bytes, uniqueness, source path and hashes; host-provided context is outside the submitted input list. This measures the delivered instruction package, not installation, natural triggering or progressive loading. No rubric or oracle hints may enter either arm.

The maximum planned scored outputs are 114: 36 screening, up to 72 confirmation, and six controls. A neutral runtime canary is outside scoring and this budget. Only one preturn setup retry is permitted, and only when trace proves no model dispatch; no outcome reruns. Seed 20260930 fixes balanced arm order before dispatch.

Report per-family graded scores and full passes, selected/excluded counts, every missing outcome, controls separately and supported host identity/effort evidence. Baseline-selected difficulty limits generalization. Requested model labels do not prove effective backend identity.

## Candidate checks

Strict UTF-8 without BOM, parseable JSON, 27 unique case IDs, exact rubric/oracle coverage, five dimensions per case, and reference arithmetic/feasibility have been checked locally. Independent review and freeze are pending. No target-model trials have been run by this writer.
