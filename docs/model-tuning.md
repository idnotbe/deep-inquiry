# Astra 6 and Fable 5.1 tuning

Reviewed: 2026-09-18 (Asia/Seoul). Baseline: `eb220b5c2e3fc071b62f9569d718ffee1adf069e`.
Status: official-guidance-informed revision, not a demonstrated model-performance improvement.

## Design decision

Keep one skill and one contract. A short conditional `references/model-adaptation.md` supplies model emphasis without duplicating the core or inventing a runtime adapter. The original six references remain; no API dependency, executable runtime code, model override, effort override or permission grant is added.

Alternatives considered: duplicating the complete skill per model risks divergent permission and revision policies; putting every model detail in the root loads irrelevant instructions; a common root plus one conditional profile preserves the existing progressive-disclosure design with a smaller maintenance surface. These are design judgments, not measured token or success-rate results.

## Research to change map

| Primary source | Relevant guidance | Revision and corresponding check |
|---|---|---|
| OpenAI Astra skills article [O1] | Short scoped discovery; conditional references; avoid rigid itineraries and redundant tests. | Shorter description, outcome-oriented route use, explicit reuse of the final frozen full run. P04/P05 distinguish valid reuse from stale evidence. |
| OpenAI model guide [O2] | Follow-through, instruction sensitivity, output style and explicit delegation boundaries. | Finish all authorized phases, while preserving the user's Q gate. P01/P02 contrast ambiguity with delegated completion. |
| Fable prompting guide [F1] | Search at low effort; targeted edits; progress, complete delivery, source handling and constraint-preserving compaction. | Evidence lookup rule, local-edit boundary, whole-task reporting, source example and handoff fields. P03/P06/P07/P08/P11. |
| Fable model changes [F2] | Model/runtime API behavior is distinct from prompt wording. | No claimed model switching or enabled capabilities. P09/P12. |
| Claude Code skills reference [C1] | Invocation and settings belong to the host. | Document Claude-specific explicit-invocation settings without changing shared frontmatter or other user settings. |

The user's framing-confirmation rule takes priority over generic recommendations to make assumptions and continue. We did not import claims that the user is absent, does not want updates, or has authorized unspecified action. The eight engineering principles, single-writer ownership, same-candidate verification and R/X limits remain in the root. `inquiry-methods.md` is unchanged: the optimization does not trade away premise exploration or mechanism diversity for brevity.

## Host setup, not skill magic

Select the actual model in the existing application. A requested guidance profile does not establish the running model's identity. Keep a working effort setting as the initial comparison; for a new Fable setup its documented default is `high` [F1]. Choose subsequent settings from matched task evaluations, not the word "deep" or an assumed equivalence between effort labels.

For a custom API harness, the verified identifiers are `gpt-6-astra` and `claude-fable-5-1` [O2, F2]. Astra tool workflows use the Responses API. Its current guide excludes `none` effort and legacy sampling parameters such as `temperature` and `top_p` [O2]. Do not add those parameters to make this skill more creative.

Fable's API history handling requires preserving its conversation prefix and returned blocks according to the provider protocol [F1, F2]. Let supported hosts manage compaction and reasoning state; a cross-provider handoff uses ordinary task-state text, not provider-specific opaque reasoning blocks. Fable progress-event display also needs client support [F1]. The skill's prose cannot activate API betas, make missing tools available or configure UI rendering.

For a personal/project Claude Code installation, use the complete bundle in `.claude/skills/deep-inquiry/` and `/deep-inquiry`. The current documented `skillOverrides` value `user-invocable-only` can enforce manual invocation without editing the shared frontmatter [C1]:

```json
{"skillOverrides": {"deep-inquiry": "user-invocable-only"}}
```

Merge only this entry into existing settings, or use `/skills` to set user-only visibility. This example is not an instruction to replace an existing settings file and does not apply to plugin-managed skills. Codex's existing `agents/openai.yaml` remains unchanged. No user installation or account settings were modified here.

## Evaluation protocol and limits

The original 33 behavior and six trigger definitions remain unchanged. `evals/model-suite.json` adds twelve fixed outcome cases; `tests/test_model_profile.py` checks their structure and resource integration, not model behavior. The model observation template stays empty. The repository CLI continues to cover the original suites; the additional unit tests cover this new suite.

For each target model separately, compare no-skill baseline, the immutable baseline skill and the current candidate. Supply the same domain-task prompt; select/activate the method outside it. Match model snapshot, host, actual effort, tools, permissions, inputs and budget. Do not compare one model's baseline against the other model's candidate. Keep check text away from the execution model. Use fresh sessions and repeat important cases; the public cases are not private held-out evidence.

The planning-only cases test advice about a supplied state, not actual tool orchestration. P04/P05 rely on supplied check records, so do not report them as agent-executed tests. Add separate live disposable fixtures before claiming tool sequencing, patch behavior, progress rendering, compaction or installation reliability. No such host runs were available during this revision.

Record suite/bundle digests, settings, observed outputs, attempted actions and coverage using the repository's evaluation protocol. Preserve failed and missing checks; never derive creativity, quality or triggering scores from word counts, lint success or empty observations. The source-based changes are hypotheses pending these experiments.

## Revision review

A focused author review caught two integration risks: a progress-update clause could grammatically appear to suppress the final answer for long tasks, and model tuning could be mistaken for runtime configuration. The final wording explicitly separates checkpoint updates from final delivery and separates profile selection from host settings. No independent model reviewer is claimed.

Local verification covers the hydrated runtime bundle and new static integration tests. The editing environment cannot resolve GitHub directly, so GitHub object/PR APIs are the publication transport. The sparse local checkout preserves the full baseline tree; unhydrated, unchanged files are not deletions. Full repository tests are run by the existing GitHub Actions workflow on the published candidate; refer to the actual PR run for that result rather than treating workflow configuration as evidence.

## Primary sources

- [O1] OpenAI, *Rethinking skills and prompts for GPT-6 Astra*, published 2026-09-11: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- [O2] OpenAI, *Model guidance*, Astra sections: https://developers.openai.com/api/docs/guides/latest-model
- [F1] Anthropic, *Prompting Claude Fable 5.1*: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- [F2] Anthropic, *What's new in Claude Fable 5.1*: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
- [C1] Anthropic, *Extend Claude with skills*: https://code.claude.com/docs/en/skills

Links record the researched guidance, not runtime dependencies. Model behavior may vary by host, effort, tools and task; these pages are not proof of improvement for this skill.
