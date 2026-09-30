# What deep-inquiry is intended to improve

Deep-inquiry is an instruction bundle for producing more defensible answers under
the user's confirmed objective. Its distinctive contribution is inquiry: testing
load-bearing premises, comparing mechanisms that actually work differently,
using evidence that changes a decision, and checking whether a recommendation
survives constraints, counterexamples, operating costs and participant adaptation.
It also preserves scope, authority and honest reporting while doing that work.

The source of this interpretation is the canonical [skill entry point](../.agents/skills/deep-inquiry/SKILL.md),
[inquiry methods](../.agents/skills/deep-inquiry/references/inquiry-methods.md),
[evidence and diagnosis](../.agents/skills/deep-inquiry/references/evidence-and-diagnosis.md),
and [alternatives and drafting](../.agents/skills/deep-inquiry/references/alternatives-and-drafting.md).
The [design record](design.md) distinguishes preserved adaptive-review rules from
the additional inquiry methods. These are design hypotheses, not guaranteed gains.

## Observable depth

Internal reasoning is not directly measured. The evaluation examines the final
answer's supported conclusions and the concrete reasoning needed to justify them.
A concise answer can receive full credit. Length, confident tone, named lenses,
unusual wording and private reasoning transcripts receive no credit.

| Intended capability | Evidence in a good answer |
| --- | --- |
| Inspect a premise | Shows exactly why a proposed prerequisite is necessary or unnecessary under the fixed goal, with a valid countercase. |
| Change the mechanism | Supplies feasible alternatives whose operating rules differ, rather than renaming the same dashboard or committee. |
| Make diagnosis useful | Identifies observations that distinguish plausible explanations and connects each result to a different permitted action. |
| Integrate constraints | Derives a bound, interaction or transaction that invalidates a superficially attractive answer and repairs the recommendation. |
| Converge fairly | Lets the conventional answer win when it is justified; changes the choice when a governing condition changes. |
| Account for ordinary operation | Identifies authority, inputs, exceptions, costs and adaptation without inventing cooperation or capabilities. |

A checklist can verify whether an answer asked a question or included a formula.
That alone does not establish any of the capabilities above. A quality rubric must
judge whether the question was decisive, the formula was correct and relevant,
and the resulting recommendation satisfies the actual problem.

## Why a new core evaluation is needed

Evaluation v2 mixes useful inquiry cases with direct arithmetic, translation,
formatting, lifecycle advice, loading checks and actual file operations. The
earlier Sol comparison had 32 distinct tasks and 96 responses: 37/48 baseline
passes and 40/48 treatment passes. Its 77/96 combined task-outcome passes describe
that mixed set, rather than measuring deeper response quality alone. The run was
marked `comparison_eligible=false`; these counts do not establish a skill effect.

The proposed v3 core uses self-contained response problems and task-specific
graded quality criteria. Actual baseline-only calibration must establish their
difficulty and remove ceiling items before treatment results are observed. Old v2 data and tests
remain historical and regression evidence; they are excluded from the new core
score. Conventional-winning countercontrols are reported separately so that
unnecessary reframing cannot earn an apparent gain.

The first two pools explicitly request comparisons and boundaries. They test
the quality of integrated answers to those requests, rather than proving that a
model spontaneously discovers an unrequested premise challenge or new framing.

As of 2026-09-30, the first v3 pool scored 356/360 with 34/36 full baseline passes
and retained zero families. The second scored 336/360 with 31/36 full passes;
only one family met both the difficulty and validity requirements. Another
numerical qualifier had unclear operating rules and cannot establish baseline
inability. Both pools were retired before scored treatment, confirmation or
control runs. The third used evidence-rich decision dossiers and scored 238/240
with 23/24 full passes, retaining zero families. Its contract-enforcement case
also has a qualified interpretation of available enforcement authority.
All three pools failed the six-family coverage requirement. No difficult core is
active, and its skill comparison has not been run. Further synthetic hardening
has stopped; a new direction needs evidence beyond these retired candidates.

Difficulty selection conditions the result on selected problems. Separate frozen
confirmation instances use fresh baseline and treatment runs; confirmation
outcomes cannot be used to remove inconvenient tasks. Those instances are known
to their authors and are not claimed to be an inaccessible or contamination-free
holdout. Task validity and feasible reference answers are reviewed before trials.

## Treatment and claim boundary

The earlier host blocked conditional reference reads. The v3 comparison explicitly
will deliver the unchanged skill entry point together with three frozen, relevant
references. The baseline will receive the same task and common host settings
without that package. This contrast measures the explicitly supplied instruction package. It does
not prove natural skill selection, ordinary progressive reference loading, an
installation-only effect, or the separate contribution of an individual module.

Codex host configuration is requested and checked as `gpt-6-sol` with `medium`
effort. Actual backend identity, fallback identity and effective backend effort
are reported only if observable; otherwise they remain unknown. A completed
model answer, a valid rubric, a structural repository test and a successful
installer are different kinds of evidence and are never substituted for one
another.
