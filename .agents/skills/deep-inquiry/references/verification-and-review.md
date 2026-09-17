# Verification and integrated adversarial review

Read for nontrivial checks, scenarios, execution tests, dependency impact or counterexample review. Produce version-bound evidence and one issue register.

## Choose the method before judging

For facts, calculations, translations and summaries, compare with original sources, arithmetic and the contract; scenarios may add nothing. For code/rules/systems, run permitted tests of normal, boundary and error behavior. For strategies and workflows, test concrete scenarios and verify core facts separately. For ideas/design, inspect purpose, differentiation, audience, use conditions and constraints; imagined user reactions are not preference data.

For high-impact or difficult-to-reverse decisions, prioritize decisive evidence and necessary independent checks over more review rounds. If unavailable, disclose the missing basis and return to Q where permission or a user decision is needed.

Test observable behavior: resulting artifact, actual decision or question, stopping point, permissions and side effects. A Markdown keyword, lint score or statement of confidence cannot establish these outcomes. Match the exact requested output format in every applicable case, including empty results and errors.

## Construct useful scenarios

Specify starting conditions/inputs/events; resource/authority/time/data constraints; the candidate's defined response and expected result; pass/fail criteria; and the actual verification method or assumption-based label.

Before selection, use shared situations that distinguish mechanisms. After selection, cover relevant normal behavior, collapsed premises, candidate-specific weaknesses, important boundaries/interactions and previous successes. A missing approver with no substitute authority must not become a passing scenario by inventing a substitute.

Freeze the version under review. Apply scenarios to that version without patching separately for each reviewer or scenario. Collect findings. Use the root's result states and evidence distinctions. An obvious major defect can make later checks pointless; stop those checks without marking them passed.

## Review conclusions and criticism together

Review the original request, confirmed contract, frozen candidate, scenario outputs, sources, earlier findings and actual changes. Seek a falsifiable failure: lost constraint, unsupported causal claim, absent prerequisite, impossible handoff, incompatible component, regression or overstated verification.

Each finding needs the violated criterion, triggering conditions/counterexample/evidence, impact and closure check. Merge common causes and link their affected cases. Criticism itself must survive scrutiny; a generic "could fail" or reviewer preference is not a confirmed P0/P1. Use E for disputed facts and Q for user values. A different role prompt is not an independent reviewer.

## Efficient verification without stale passes

During iteration follow the root's change-impact policy. Record which earlier checks remain valid and why. Changes to shared assumptions, interfaces, test assertions, tools or acceptance criteria invalidate dependent evidence even when a tested file was not edited. When dependency impact is uncertain, broaden the affected set rather than silently preserving a pass.

Once stable, freeze one candidate identity and give the same version and criteria to independent full checks/reviews, parallel only when the environment supports it. Integrate findings through the single writer; do not let reviewers mutate their own variants. If a fix changes the candidate, invalidate affected work and rerun it. Do not repeatedly rerun unaffected expensive reviews merely for ritual.

Finish with one full verification of the final candidate: run the full required executable suite where available, inspect whole-contract coverage and confirm all retained evidence is still valid. Reuse valid independent review evidence rather than duplicating every review. Record candidate/input identity, checks, outcomes and uncovered requirements as a short verification receipt. A full run just completed on that frozen candidate satisfies the executable part of the final gate; close by checking coverage rather than rerunning identical checks. A later change invalidates this final gate and requires a new final verification. A successful packaging or lint run does not substitute for host behavior evaluation.
