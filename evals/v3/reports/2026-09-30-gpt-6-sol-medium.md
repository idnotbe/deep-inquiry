# Response-quality evaluation v3 — gpt-6-sol / medium

**Status:** all three materially different candidate pools completed baseline-only screening and were retired for insufficient difficult-core coverage. Together they produced **96 actual outputs in 96 attempts, 930/960 rubric points and 88/96 full passes**. Pool 1 retained zero families, pool 2 one valid family, and pool 3 zero; each needed six. No scored treatment, confirmation or conventional-control turn ran. The intended difficult-core evaluation remains **unmet**, and skill-package effect is `NOT_RUN` and undetermined. The [evidence record](2026-09-30-gpt-6-sol-medium-evidence.json) separates the pools and evidence limits.

## What this evaluation asks

Deep-inquiry aims to improve the quality of supported recommendations under a user's fixed objective. The core tests whether a final answer examines a load-bearing premise, chooses between mechanisms that work differently, uses observations to change a decision, integrates constraints and counterexamples, and accounts for operating burden and participant adaptation. These are five task-specific **scoring views**, not five independent measurements. A short, correct answer can earn full credit; length, named frameworks, novelty, and private reasoning are not graded. The purpose and boundaries are in [evaluation-purpose.md](../../../docs/evaluation-purpose.md); the exact retired pool 1 definitions are linked below.

This evaluates actual final responses from a native host requested as `gpt-6-sol` at `medium` effort. A completed answer and observed host readback do not attest to effective backend identity, fallback, or actual backend effort. No natural skill triggering, ordinary reference loading, root-only effect, or installation-only effect is tested.

## Candidate and selection rule

Retired pool 1 has 12 families with calibration cases C01–C12 and separate, frozen confirmation cases H01–H12. Its exact [case](../history/pool-1/cases.json), [rubric](../history/pool-1/rubrics.json), and [protocol](../history/pool-1/protocol.json) definitions remain in history. All instances and private illustrative feasibility answers were seen by their authors; H cases would have been fresh evaluation instances, **not** an inaccessible holdout or unseen-family transfer test. Three conventional-winning controls K01–K03 were outside the difficult-core score. Earlier v2 results remain historical and are excluded from this v3 core.

Independent structural and feasibility reviews found no P0/P1 blocker for the revised candidate. Those reviews establish that feasible answers exist, not that target-model performance is difficult. They also noted two nonblocking rubric wording issues: valid early interruption schedules must receive credit, and a correct dependency proof need not narrate extra alternatives. Grading must apply the rubric's concise, alternative-valid-answer policy. See the local review records `temp/2026-09-30-rebuild/construct-review2.md` and `temp/2026-09-30-rebuild/oracle-review2.md`; their private examples and oracles are not published here.

Pool 1 screening planned 36 baseline-only outputs: three fresh trials for each C family. The predeclared rule excludes a family when **at least two of three** trials are full passes, or when its normalized mean score is **strictly greater than 0.70**. A full pass is a score of at least 8/10 with no critical failure. A missing output is `NOT_RUN` or host failure, never a zero. A 0/3 full-pass family needs independent feasibility and clarity validation before inclusion. If fewer than six families remain, coverage is insufficient; the protocol calls for a prospective revised candidate and new freeze, preserving the initial records. No family may be selected, removed or replaced using treatment or confirmation results.

**Pool 1 screening result:** 36/36 actual baseline outputs were completed and verified. Final blind grading awarded 356/360 points and 34/36 full passes. Two independent panels graded all 36; a third adjudication resolved and preserved their two disagreements (S02 and S16). The [public final-response set](pool-1-responses.json) and [grade record](pool-1-grades.json) preserve the trial and grading evidence. Neither pool 1's structural review nor this high baseline score establishes a difficult core.

| Calibration family | Full passes | Points / 30 | Normalized mean | Exclusion |
| --- | ---: | ---: | ---: | --- |
| C01 attribution | 3/3 | 30 | 1.000 | Full passes and mean |
| C02 bottleneck | 3/3 | 30 | 1.000 | Full passes and mean |
| C03 diagnostic test | 3/3 | 30 | 1.000 | Full passes and mean |
| C04 operating rules | 1/3 | 28 | 0.933 | Mean |
| C05 threshold | 3/3 | 30 | 1.000 | Full passes and mean |
| C06 incentives | 3/3 | 30 | 1.000 | Full passes and mean |
| C07 analogy | 3/3 | 30 | 1.000 | Full passes and mean |
| C08 state interface | 3/3 | 30 | 1.000 | Full passes and mean |
| C09 critique | 3/3 | 30 | 1.000 | Full passes and mean |
| C10 combined constraints | 3/3 | 28 | 0.933 | Full passes and mean |
| C11 measurement cost | 3/3 | 30 | 1.000 | Full passes and mean |
| C12 complementarity | 3/3 | 30 | 1.000 | Full passes and mean |

All 12 normalized means were strictly above 0.70, so **zero families were selected**. Pool 1 fell below the required six families and cannot support a difficult-core comparison. The protocol thresholds were not changed after observing results.

## Pool 2: completed screen, retired candidate

The sole prospective pool 2 revision completed two independent review rounds. The final construct and oracle/feasibility reviews found P0=0 and P1=0 after correcting the C07 oldest-stock reference and stating the C05/H05 confirmed-reservation lifetime. The exact retired [cases](../history/pool-2/cases.json), [rubrics](../history/pool-2/rubrics.json), and [protocol](../history/pool-2/protocol.json) match the [public freeze record](pool-2-freeze.json) and the hashes in the evidence JSON. The freeze preceded the pool 2 canary and baseline trials; it was local, not an externally timestamped preregistration. The root skill, three-reference package and runner were unchanged. Reviews established feasible intended answers before screening, not empirical difficulty or treatment benefit.

Pool 2 prompts explicitly ask for comparisons and decision boundaries. A later result can measure **integrated answer quality when prompted**; it cannot establish spontaneous discovery of an unrequested reframe. Grading assigns a distinct error to its closest rubric anchor and lowers another view only for an independently demonstrated consequence; concise valid alternatives receive credit. The five views remain overlapping ways to judge one answer.

A fresh neutral pool 2 canary pair completed with exact task/reference/root delivery, matched observed developer and user-prefix context, and successful process, source and copied-auth cleanup. The frozen baseline-only screen then completed **36 actual outputs in 36 attempts**, scoring **336/360 points and 31/36 full passes**. Both initial judges graded all 36, and seven disagreements received a preserved third adjudication. The [public final-response set](pool-2-responses.json) and [grade record](pool-2-grades.json) retain the scored evidence.

| Calibration family | Full passes | Points / 30 | Normalized mean | Screening disposition |
| --- | ---: | ---: | ---: | --- |
| C01 capacity adaptation | 3/3 | 30 | 1.000 | Excluded: passes and mean |
| C02 partial identification | 3/3 | 30 | 1.000 | Excluded: passes and mean |
| C03 perturbing diagnosis | 3/3 | 30 | 1.000 | Excluded: passes and mean |
| C04 incentive coverage | 3/3 | 30 | 1.000 | Excluded: passes and mean |
| C05 cross-owner commitment | 0/3 | 19 | 0.633 | Numeric qualifier; clarity and authority unverified |
| C06 correlated robust information | 1/3 | 20 | 0.667 | Validly selected |
| C07 perishable cutover | 3/3 | 27 | 0.900 | Excluded: passes and mean |
| C08 commitment granularity | 3/3 | 30 | 1.000 | Excluded: passes and mean |
| C09 private structural matching | 3/3 | 30 | 1.000 | Excluded: passes and mean |
| C10 approval-scope critique | 3/3 | 30 | 1.000 | Excluded: passes and mean |
| C11 online preemption critique | 3/3 | 30 | 1.000 | Excluded: passes and mean |
| C12 decision without truthful costs | 3/3 | 30 | 1.000 | Excluded: passes and mean |

C05 and C06 both passed the numeric difficulty screen. C05's independent post-baseline validity audit found the number of allowed coordinator stops and cross-request admission authority insufficiently clear for a governing benchmark. The public [grade record](pool-2-grades.json) retains that qualification; the detailed local receipt is `temp/2026-09-30-rebuild/pool-2/transaction-validity-audit.md`. That uncertainty does **not** prove model inability or that a deadline is universally impossible. Frozen inputs, outcomes and numeric thresholds remain recorded; C05 is excluded from the valid difficult core under the separate clarity requirement. Only C06 is validly selected, below the required six. Pool 2 was therefore retired without treatment, confirmation or control dispatch.

## Pool 3: completed screen, retired dossier candidate

Pool 3 has eight paired evidence-rich decision dossiers (8 calibration C cases and 8 writer-seen confirmation H cases) and three unchanged conventional controls, for 19 cases. It followed the two failed coverage screens without changing the root skill, the three explicitly delivered references, or the native runner. Two independent pretrial construct and feasibility review rounds passed with P0=0 and P1=0. A bounded rubric revision made four C/H gates enforce the supplied maximization objective while preserving partial credit, concise valid answers and one charge per root error. These source reviews supported task feasibility, **not** empirical difficulty. The exact retired [cases](../history/pool-3/cases.json), [rubrics](../history/pool-3/rubrics.json), [protocol](../history/pool-3/protocol.json), and [README](../history/pool-3/README.md) match the [public exact-byte freeze](pool-3-freeze.json), created before native dispatch; the corresponding private receipt is `temp/2026-09-30-rebuild/pool-3/freeze-r1.json`.

An unscored pool 3 neutral pair returned two actual completed turns. The canary verified exact task, reference and native root delivery, matched observed common developer and user-prefix context, and passed source, process and copied-auth cleanup. The frozen baseline-only screen then finished **24 actual outputs in 24 attempts** with exit 0; strict input and context readback, source preservation, process and copied-auth cleanup, and unchanged native executable checks passed. Final blind grading awarded **238/240 points and 23/24 full passes**. Two initial judges graded all 24, and their single disagreement (P3S14/C04) received a preserved anonymous third adjudication. The [public final-response set](pool-3-responses.json) and [grade record](pool-3-grades.json) retain the evidence.

| Calibration family | Full passes | Points / 30 | Normalized mean | Exclusion |
| --- | ---: | ---: | ---: | --- |
| C01 selection and net effect | 3/3 | 30 | 1.000 | Passes and mean |
| C02 aggregation and burden transfer | 3/3 | 30 | 1.000 | Passes and mean |
| C03 action-relevant identification | 3/3 | 30 | 1.000 | Passes and mean |
| C04 case-boundary incentives | 2/3 | 28 | 0.933 | Passes and mean; source-clarity qualification |
| C05 attribution prerequisite | 3/3 | 30 | 1.000 | Passes and mean |
| C06 structural analogy authority | 3/3 | 30 | 1.000 | Passes and mean |
| C07 robust future adaptation | 3/3 | 30 | 1.000 | Passes and mean |
| C08 repair or premise revision | 3/3 | 30 | 1.000 | Passes and mean |

The third adjudication noted that the C04 dossier underidentifies handoff enforcement and customer-confirmation authority. Its descriptive 8-point grade neither assumes perfect compliance nor proves that every forbidden handoff is impossible to detect. C04 is excluded by **both** fixed numeric ceiling rules regardless: two full passes and a 28/30 mean above 0.70. All eight families were excluded. The frozen cases, rubrics, thresholds and outcomes were not changed after dispatch. Pool 3 was retired with **zero of six required families**; no fourth candidate is planned after three materially different hardness attempts.

## Native delivery check

Eight unscored neutral turns have completed across four canary pairs: four before the pool 1 screen, two for pool 2 and two for pool 3. The first pair's treatment answer completed, but a post-delivery verifier rejected the host's qualified native root name and observed order; the baseline completed. The diagnosis found final collection and cleanup completed, and common developer/user-prefix readback matched within the stated normalization. The corrected second pair and the pool 2 and pool 3 pairs passed the exact native delivery contract and cleanup. The delivered treatment package is the task, three explicitly preloaded frozen references in the order inquiry methods, evidence and diagnosis, alternatives and drafting, then the native root expansion named `deep-inquiry:deep-inquiry`. These are delivery checks only. They supply no scored response and do not prove hidden system context, backend identity or natural activation. The earlier verifier failure is retained, not recast as a model failure.

## Comparison outcome

The protocol required at least six selected families before giving their H instances three fresh baseline and three treatment turns under matched requested host settings. The treatment would receive the unchanged root plus three references; the baseline would receive the same task and common host setting without that package. Pool 1 selected none, pool 2 one valid family, and pool 3 none. Therefore **no treatment arm or confirmation comparison was dispatched**. The baseline answers alone cannot estimate skill-package effect, even though they are actual native model outputs.

The three conventional-winning controls would have received one turn per arm and separate reporting. No control turn ran. The three screens completed **36 + 36 + 24 = 96 baseline outputs in 96 attempts**. The eight neutral canary outputs are outside that score. This v3 set is baseline-only and distinct from the older v2 mixed-task 96-response set and its 77/96 combined passes. **Confirmation, treatment and controls: `NOT_RUN` in all three pools.** No skill-lift or package-effect claim follows from the screening scores.

## Evidence and limits

This report and its evidence record contain verified counts, scores, selection decisions and supported host observations; the three linked public response sets contain 96 final answers. Raw native events, private oracles, hidden reasoning, copied authentication material, local profile contents, and private context or configuration fingerprints are excluded. Each pool is tied to its exact archived definitions and predispatch freeze. The pool 2 C05 and pool 3 C04 validity qualifications stay separate from numeric grades and do not prove baseline inability. Host labels and request settings alone cannot verify effective model or effort. Repository publication preparation includes scoped byte-preservation rules for the frozen v3 artifacts and runner, but published Git-blob equivalence and live main readback are separate checks still owned by the publishing thread. The v2 historical results remain available separately and do not serve as this evaluation's deeper-response score.

## Runner publication repair

The exact runner used for these native outputs is preserved as [native-runner-2026-09-30.py](../history/native-runner-2026-09-30.py), SHA-256 `11a784e7c359b644571da55ff3838d41a501aef008d730ead433e11e84c78a40`. Final publication review found that the runner could accept an incomplete future stage plan. The current runner is repaired to require complete stage slots, reject tool-attempted scored turns while preserving their finals, retain a failure manifest for invalid UTF-8 inputs, restrict runtime output to ignored private roots, and copy only frozen skill files. Those repairs have behavior-test evidence; the actual native execution receipts bind the archived version. No model output was rerun, and no frozen definition or historical hash was changed.
