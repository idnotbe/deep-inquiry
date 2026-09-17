# Host evaluation plan

These definitions are tests to run, not completed results. The JSON inputs are fixed synthetic cases. No model runner is bundled. The repository checker validates definitions, not the truth of agent behavior.

## Conditions and execution

`behavior-suite.json` compares `baseline` (no skill), `original` (the unchanged privately supplied v3 English prompt) and `candidate` (this skill). Use fresh isolated sessions with the same model, host, tools, permissions, task inputs and budget. Use the identical domain-task prompt in every condition. Supply no method for baseline, the unchanged prompt for original, and an explicit host invocation for candidate. Keep method activation outside the case input; never install or retrieve the candidate in baseline/original sessions. Record this intentional method-only difference in the run context.

Only give the agent the prompt and authorized fixed inputs, not expected checks, judges' rubrics or other cases. Inputs are entirely inline, so `fixtures` is the empty map; their exact bytes are bound by the canonical suite digest. Public cases are not secret holdouts. Add genuinely private final cases and repeated trials before strong claims.

`trigger-suite.json` is candidate-only and separates explicit invocation from implicit near-misses. Observe actual selection/read events. Because the Codex policy disables implicit invocation, implicit requests should not select this skill, even if topically relevant. This does not imply the host cannot answer without the skill. Host-specific behavior outside Codex is a separate experiment.

Several cases supply workflow state or ask for a plan rather than supply executable services. Grade the response or proposed next action in those cases; a scenario answer is not evidence of real worker scheduling, cancellation or tool retrieval. B30 is explicitly planning-only. To test live actions, prepare a separate fixed sandbox/tool fixture, version the suite and record actual traces; do not silently upgrade scenario results to live behavior.

Capture actual artifacts, questions, termination points, tool calls and side effects. The agent's assertion that it followed the rules is not evidence. Treat roleplay as self-review, not independent replication. Baseline comparisons of subjective utility should be blinded and randomized where feasible; use original-source calculations or executable checks for objectively testable claims.

## Observation integrity

The checked-in `*-observations.empty.json` files contain no observations. Copy one to an authorized external workspace for real runs; never fill it from static tests or imagined outputs. Keep private run logs out of the installed skill and public repository.

Use the current skill-quality-builder observation schema: `schema_version`, matching `suite_id`, metadata (`model`, `host`, `skill_version`, `run_context`, `evidence_kind`) and observations keyed by `case_id`, `condition`, `repetition`. Outcome checks use `pass`, `fail`, `not_run` or `not_applicable`, with evidence for assessed results. Include every common and local check; missing checks remain not_run. Trigger observations use a Boolean `triggered` backed by host traces.

Filled records must bind `provenance.suite_sha256` and `provenance.conditions`. Each condition records `skill_sha256`, `fixtures_sha256`, model, host, tools, permissions and budget. Only baseline may use `no_skill`; hash the original prompt as its own immutable one-file bundle. The tools/permissions/budget and model/host must match across conditions. `fixtures_sha256` is the canonical digest of `{}` here. Do not invent values for unexecuted runs.

Canonical digest means SHA-256 of UTF-8 JSON, sorted keys, no ASCII escaping, separators comma/colon and no non-finite numbers. Bundle identity is the canonical digest of the sorted relative-path-to-file-SHA256 manifest. `tools/check_repository.py` prints the candidate digest. Record the original file's actual name and bytes in its manifest.

The separately installed skill-quality-builder summarizer can validate and aggregate compatible observation records; it is not required to use this skill and does not run models or authenticate evidence. A nonzero number of static tests is not behavior coverage.

## Gates and interpretation

Shared critical checks preserve contract/format, authority boundaries and evidence honesty in every outcome case. Local checks cover framing, mechanistic diversity, useful conventional answers, practical burden, state/counters, worker coordination, invalidation, missing inputs and adversarial content. A valid schema, a hypothetical walkthrough or an absent observation cannot establish a host pass.

A critical failure, missing required observation or unresolved critical N/A blocks a behavior-validation claim. Distinguish the task status `unverified` from evaluation `not_run`: an agent may correctly leave an unavailable fact unverified, but that correctness must itself be observed in a host run.
