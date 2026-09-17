# Deep Inquiry

An instruction-only Agent Skill for investigating problems beyond familiar answers, without silently changing the user's objective. It extends an existing user-aligned, evidence-driven revision workflow rather than replacing it with a creativity checklist.

**Status:** implemented candidate. Repository checks validate structure and test the checker; they do not establish model behavior, creativity gains or production reliability. Host evaluations are defined but have not been run.

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

Install a project copy for Codex:

```bash
npx skills@latest add idnotbe/deep-inquiry --skill deep-inquiry --agent codex --copy
```

Add `--global` for user-wide installation. This command requires the CLI's Node/npm and repository-access prerequisites. Review third-party installer code and permissions before running it. The command follows the CLI's documented syntax; installation was not executed in the development session.

Alternatively copy the complete [skill directory](.agents/skills/deep-inquiry/SKILL.md)'s containing folder to the host's supported skills directory. Do not copy SKILL.md alone: its relative resources are required. For project-local Codex use `.agents/skills/deep-inquiry/`.

Invoke explicitly:

```text
$deep-inquiry Investigate this problem, confirm ambiguous framing with me, and develop the simplest defensible solution: ...
```

Codex metadata disables implicit invocation to avoid a broad reasoning method activating for unrelated tasks. Other hosts may interpret or ignore host-specific metadata differently; their behavior needs separate testing. Repository creation does not install a ChatGPT web plugin or start background agents.

## Structure

Runtime: [SKILL.md](.agents/skills/deep-inquiry/SKILL.md), six conditional references, one work-record template, host metadata and a license notice. No runtime scripts, API keys, database, MCP dependency or autonomous scheduler.

[Design and preservation](docs/design.md) explains the source-to-module mapping. [Evaluation instructions](evals/README.md) distinguish static checks from host observations. [Sources](docs/sources.md) identifies guide versions and private baseline digests. [Implementation review](docs/validation.md) records scope and remaining checks.

## Development

Python 3.10+; standard library only. From the repository root:

```bash
python -B -m unittest discover -s tests -v
python -B tools/check_repository.py
```

The deliberately narrow checker rejects broken local paths, orphaned resources, invalid project metadata and malformed evaluation definitions. It does not parse arbitrary YAML/Markdown, execute skills, score creativity or prove prompt-injection resistance. Empty observations stay empty; a successful static check never becomes a host pass.

Keep task data, local model outputs and evaluation observations outside the installed bundle and outside committed files. The public examples are synthetic; supplied private conversations are not redistributed.

## License

[MIT](LICENSE). The same notice accompanies the installed skill.
