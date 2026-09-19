# Deep Inquiry

An instruction-only Agent Skill for investigating problems beyond familiar answers, without silently changing the user's objective. It extends an existing user-aligned, evidence-driven revision workflow rather than replacing it with a creativity checklist.

**Distribution:** standalone skill and skills-only plugin for Claude and ChatGPT/Codex, using one canonical bundle. See [installation and distribution](INSTALL.md) for both marketplaces, Windows/Linux, updates and verification boundaries.

**Primary targets:** GPT-6 Astra and Claude Fable 5.1. Shared reasoning rules remain portable; conditional model emphasis does not switch models or effort.

**Status:** guidance-informed candidate. Repository checks validate structure and test the checker; they do not establish model behavior, creativity gains or production reliability. Host evaluations are defined but have not been run.

## What it does

- Confirm materially different problem interpretations before dependent research or design.
- Challenge whether a supposedly necessary intermediate step is needed, identifiable, observable and economical; explore different mechanisms rather than renamed frameworks.
- Use bounded analogies, changed representations, concrete transactions and stakeholder adaptation to expose weak assumptions. Allow a simple conventional answer to win.
- Preserve one contract, current candidate and issue register; apply bounded revisions and evidence-based acceptance.
- Apply Correctness First, KISS, YAGNI, High Cohesion/Low Coupling, Explicit over Implicit, Single Source of Truth, Minimal Diff and Test Behavior.

## Install and invoke

Inspect the available skill with the third-party skills CLI:

```bash
npx skills@latest add idnotbe/deep-inquiry --list
```

Install a project copy for Codex and Claude Code:

```bash
npx skills@latest add idnotbe/deep-inquiry --skill deep-inquiry --agent codex claude-code --copy
```

Add `--global` for user-wide installation. This command requires the CLI's Node/npm and repository-access prerequisites. Review third-party installer code and permissions before running it. Inspect the exact-commit distribution CI report for executed installation checks; installer success is not model-effectiveness evidence.

Alternatively copy the complete [skill directory](.agents/skills/deep-inquiry/SKILL.md)'s containing folder to the host's supported skills directory. Do not copy SKILL.md alone: its relative resources are required. For project-local Codex use `.agents/skills/deep-inquiry/`.

Invoke explicitly:

```text
$deep-inquiry Investigate this problem, confirm ambiguous framing with me, and develop the simplest defensible solution: ...
```

Codex metadata disables implicit invocation to avoid a broad reasoning method activating for unrelated tasks. Other hosts may interpret or ignore host-specific metadata differently; their behavior needs separate testing. Repository creation does not install a ChatGPT web plugin or start background agents.

## Astra and Fable use

Select the model in your existing host, then explicitly invoke the skill. Keep your current effective effort as a comparison baseline; do not assume maximum effort or the same effort label across providers is best. The [model tuning notes](docs/model-tuning.md) record official sources, preserved boundaries and unexecuted model checks.

For Claude Code, copy the complete bundle to `.claude/skills/deep-inquiry/` and invoke `/deep-inquiry`. Its current settings support `"skillOverrides": {"deep-inquiry": "user-invocable-only"}` for a personal/project skill without changing the shared SKILL.md. Merge this entry into existing settings; do not replace other settings. Codex's `openai.yaml` does not enforce Claude invocation policy. Host availability and installed versions must be checked; no host installation is performed by this repository.

## Structure

Runtime: [SKILL.md](.agents/skills/deep-inquiry/SKILL.md), seven conditional references, one work-record template, host metadata and a license notice. No runtime scripts, API keys, database, MCP dependency or autonomous scheduler.

[Design and preservation](docs/design.md) explains the source-to-module mapping. [Evaluation instructions](evals/README.md) distinguish static checks from host observations. [Sources](docs/sources.md) identifies guide versions and private baseline digests. [Implementation review](docs/validation.md) records scope and remaining checks.

## Development

Python 3.10+; standard library only. From the repository root:

```bash
python -B -m unittest discover -s tests -v
python -B tools/check_repository.py
python -B tools/distribution.py
```

The deliberately narrow checker rejects broken local paths, orphaned resources, invalid project metadata and malformed evaluation definitions. It does not parse arbitrary YAML/Markdown, execute skills, score creativity or prove prompt-injection resistance. Empty observations stay empty; a successful static check never becomes a host pass. The [model-specific suite](evals/model-suite.json) is checked by `tests/test_model_profile.py`; it is not a model runner.

Keep task data, local model outputs and evaluation observations outside the installed bundle and outside committed files. The public examples are synthetic; supplied private conversations are not redistributed.

## License

[MIT](LICENSE). The same notice accompanies the installed skill.
