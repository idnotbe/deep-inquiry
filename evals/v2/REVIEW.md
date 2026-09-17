# Evaluation-dataset adversarial review and executed evidence

Reviewed 2026-09-18, Asia/Seoul. One author; self-review is not an independent model
review. Runtime skill unchanged. The objective is a reliable test set, not to make
the skill or the author's answers appear to pass.

## Evidence actually produced

- 81 fixed cases, including all 51 legacy IDs and 30 additions; separate task and
  judge files; 13 family labels and six execution modes.
- 21 contaminated current-conversation exercises. Four performed real read/edit/CSV
  operations on isolated synthetic files. Other responses were authored in this
  conversation with the rubric visible. They are NOT isolated target-model trials.
- 19 of those 21 exercises satisfy the inspected checks; two (N03/N04) fail the
  requested JSON format. Their incorrect output is preserved. This is an apparatus
  exercise, not an estimated model success rate or causal skill improvement.
- 95 check judgments in those exercises: 91 pass, 4 fail. The four failures are
  two JSON-oracle failures plus the corresponding two contract-review failures.
  These are not four independent task failures. Same-author semantic checks are
  explicitly labeled self_review.
- Genuine native-run preflights attempted for the requested Astra and Fable model
  IDs: blocked because `codex` and `claude` executables are absent. Requested model
  identifiers do not prove what model ran. Target-model executions: zero.
- Local tests exercise the actual fixtures, grader, typed numeric checks, parser,
  isolation, manifests and report aggregation. They are tests of the evaluation
  apparatus, not 51 model reasoning passes. Final local run: 51 tests passed.

The public [summary](reports/current-session.json) and
[exercise outputs](reports/exercise-outputs.json) retain both passes and failures.
The companion downloadable evidence archive contains per-trial records, full
fixture manifests, raw local-action records, self-reviews and grading reports.
No supplied private case conversation is published.

## Review rounds and corrections

| Round / issue | Severity and evidence | Change | Retest / disposition |
|---|---|---|---|
| Initial provenance map drift | P1: new trigger prompt meanings were assigned old T03/T05 IDs | Restore original T01-T06 prompt meanings/expectations; reserve T07-T12 for new tests | Inspect exact source prompts against frozen legacy trigger suite |
| Empty qualitative criterion | P1: a blank criterion was schema-valid | Reject empty criteria | test_empty_review_rejected |
| Platform-dependent fixture collision | P1: Data.txt/data.txt and file data plus data/file were accepted | Check case/normalization and file/directory collisions | Two explicit fixture mutation tests |
| Malformed host message crash | P1: message=null raised AttributeError rather than an unknown/invalid trace result | Validate message object and keep incomplete/error traces unknown | test_malformed_message_returns_diagnostic |
| Result aggregation trusted missing/foreign checks | P1: aggregation had no exact rubric binding/check inventory validation | Bind current suite/rubric, reject duplicate/missing/unknown checks and critical-flag drift | Summary mutation tests for omitted checks and mixed suite identities |
| A test accidentally used Codex parsing on a Claude error trace | P1 evaluator-test defect: it passed without exercising the intended parser path | Prepare the test with the correct engine; verify native completion from raw trace, not free-form record claims | test_trace_error_not_overridden_by_record |
| Two patch-calibration tests used a nonexistent check ID | P2: KeyError on `files` instead of actual `patch` | Fix the test reference, not the oracle | Correct and unrelated-edit patch fixtures both retested |
| Initial-state record was not bound to fixed fixture | P1: a changed before manifest could hide a forbidden delta | Rebuild expected initial manifest from fixed task/skill and compare it | test_initial_manifest_tampering_rejected |
| Repetition/strata handling incomplete | P1: CLI could only name repetition 1; mixed models could share summary | Expose bounded repetitions and reject mixed host/model/effort strata | Repetition and environment mutation tests |
| Native Claude invocation policy mismatch | P1 integration risk: copied OpenAI metadata does not configure Claude visibility | Use documented per-invocation visibility settings and restricted tool profile; do not modify runtime | Source contract inspection; real-host smoke test remains unverified |
| Blanket semantic pass contradicted two format failures | P1 reviewer defect observed in the 21 exercises | Change N03/N04 contract judgments to fail; keep original bad responses and machine oracles | Regrade the same artifacts; two task failures remain |
| Extreme integer output crashed finite-number conversion | P1 robustness defect for arbitrary model output | Avoid float conversion for integer equality | 1,000-digit output is rejected without crashing |

Round-1 calibration: 43 tests, 3 failures and 5 errors (including two incorrect
check-ID tests and the missing aggregation API contract). After the first repairs,
43 passed. The next review added seven adversarial checks; 50 passed. The final
numeric robustness check brings the verified set to 51. These results are scoped
to observed code/tests; they do not mean the skill was run 51 times.

## Deliberately not changed

N03/N04's JSON oracles were correct. We did not weaken them to accept a bare letter.
A result failure is not automatically a dataset defect. We also did not rewrite the
runtime skill, alter the original 51 definitions, create a novelty score, or demand
that every answer reproduce the ROI/resource-allocation example.

## Final scenario review

| Adversarial situation | Verified/defined disposition |
|---|---|
| Unrelated tool or another skill occurs before the target | Parser continues through the full log; synthetic positive tested |
| Missing/partial trace or only a model claim of use | No negative-trigger pass; unknown remains |
| Same formula used after sequential flow becomes parallel | Wrong answer rejected; zero elapsed saving accepted for N02 |
| Correct patch plus unrelated note edit | Fails exact delta despite correct add behavior |
| Read-only audit creates ignored cache file or empty directory | Full manifest detects the change |
| A new output uses CRLF; protected input is rewritten with CRLF | New output normalization accepted, protected input rewrite rejected |
| Foreign suite report, missing check, forged initial manifest | Fails closed instead of reporting green coverage |
| Same-session author exercise labeled as model benchmark | Evidence grouping and explicit comparison prohibition prevent that claim |
| Critic is confidently wrong or familiar solution is sufficient | Qualitative rubric accepts a supported conventional answer; no contrarian quota |

No further P0/P1 defect was identified in the final **local dataset/fixture/grader
review scope** after the last fixes. This is not a claim that the full user-requested
native evaluation is complete. The unresolved requirements below block that claim.

## Unresolved validation requirements

Native Astra/Fable runs, verified clean-profile A/B comparisons, native negative
selection and reference-loading telemetry, the multi-turn driver, independent
semantic calibration, and production-style external side-effect containment have
NOT been validated. The runner intentionally marks unsupported paths blocked or
unknown. Its observer cannot certify native negative triggering and it does not
implement the scripted conversation driver. These are explicit missing coverage,
not hidden passes. Add verified host adapters/manual traces before calling this a
fully validated release benchmark or declaring the skill reliable across projects.
