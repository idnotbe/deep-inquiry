# Design and preservation

## Contract and architecture decision

Implement `deep-inquiry` by preserving the supplied adaptive review prompt's user gates, issue routing, working state, revision accounting and acceptance rules, while adding operational methods for deeper inquiry. English instructions; responses in the user's language.

Keep the original root-plus-conditional-references architecture. Add only `inquiry-methods.md` to the earlier five procedure references. The work-record asset now also records confirmed interpretation, consequential discoveries and check invalidation. It stores conclusions and observable evidence, not hidden reasoning.

A monolithic prompt was considered: fewer loading failures, but every task loads every detailed method. Multiple autonomous skills were considered: separate invocation and state coordination would add complexity without distinct user contracts. A separate runtime engine/database was rejected because the task needs procedural judgment, not a new execution platform. The chosen skill has no runtime code.

## Source preservation map

The private baseline is `adaptive_review_prompt_v3.en.md`; section numbers refer to that document. This table is a manual contract map, not automated proof of equivalent behavior.

| Baseline | Implementation | Preserved behavior and exceptions |
|---|---|---|
| 0: purpose/principles | SKILL.md sections 1, 3, 4, 6 | Proportionate routing, one deliverable/register, distinct fact/cause/value/defect handling, no recursive review ceremony. |
| 1: alignment | Root 1; alignment.md | Material questions before dependent work; no repeated answered questions; accessible facts checked directly; later decision checkpoints; pause and resume from same issue. |
| 2: state/limits | Root 3; work-record.template.md | Initial draft excluded; rounds charged at start; pauses resume same round; interruptions/failures/rollbacks count; no subtask resets; initial alternatives excluded from re-exploration; final verification survives exhausted limits. |
| 3: route order/E/H | Root 4; evidence-and-diagnosis.md | Q/E/H/A/D/V/open-issue/F order; initial drafting distinct from revision; causal hypotheses distinct from remedies; decisive facts and discriminating observations. |
| 4: alternatives/drafting | alternatives-and-drafting.md | Shared criteria and scenarios; genuine mechanisms; requested option set preserved; compatible hybrids only; all-fail handling; early concepts not rejected merely for missing rollout detail. |
| 5: verification/review | Root 6; verification-and-review.md | Frozen version, source/calculation/executable checks as appropriate; no invented prerequisites; simulation distinct from observation; one register; unsupported criticism challenged; no fake independent reviewers. |
| 6: disposition/M | Root 6; resolution-and-revision.md | Defect/E/H/Q handling; observable future switching; premise-collapse gate; conflicting constraints not waived; P2 repaired when agreed quality requires it; evidence-based closure/rollback. |
| 7: acceptance/stopping | Root 7 | Whole final-version gate, no unresolved material blockers, no silent scope downgrade, technical pass is not action permission; no success inferred from fatigue or limits. |
| 8: response | Root 7 | Question then stop; result-first completion, material evidence/changes/risks; actual routes and counters only when useful; respect exact user output format. |

## Explicit enhancements, not silent source corrections

The root retains numeric iteration policy as its sole normative location. References invoke the gate rather than duplicating limits. The engineering principles and efficient verification rules are later user requirements, added explicitly to root section 2.

The inquiry module adds: detection of same-mechanism answers; necessity/identifiability/economics of intermediate steps; bounded non-domain analogies; removal/reversal/unit change/separation/limiting cases/representation/adaptation; fair concept comparison; critic validation; practical transaction and administrative burden checks; commercial deliverables only for commercial tasks; short evidence-labeled discovery records.

These are design hypotheses, not proven gains in creativity or accuracy. They do not guarantee unusual answers. The supplied attribution case motivates the operations, not a universal prescription to replace measurement with budgets. A counterexample explicitly preserves easy, valid measurement.

## Permission boundary

Exploring methods under a confirmed objective is allowed within delegated scope. Materially different interpretations require user confirmation before dependent work. General permission to choose the best approach does not authorize a new objective or deletion of a mandatory measurement/report deliverable. A brief framing question is not substantive implementation of the reframe.

Original attachments and the business conversation are not published. Public examples and evaluation prompts are synthetic and contain no customer-specific records. No personal data is accumulated into the skill.

## Loading and verification

Root rules cover every execution. All six references and the asset are directly linked with loading conditions. Substantive open-ended work reads inquiry methods before convergence; straightforward transformations can finish using the root alone. Missing necessary references are surfaced instead of imagined.

One writer owns each changed area; read-only reviewers share one frozen version. Only real independent tooling may be parallelized. During iteration, transitive change impact determines invalidation. Final verification covers the whole candidate; retained independent evidence is reused only when still valid. These instructions do not supply an asynchronous runtime.
