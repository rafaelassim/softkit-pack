# This toolkit aims to make the programming interaction easier.

```text
Sure, all toolkits do that, but this one gets you hands-on with the requirements before a single line of code is written.
Understand your problems and your desired outcome.
Every change is documented.
Every decision-making step remains accessible.
```

These tools will probe you to fully elicit your needs; this isn't just a game of Q&A.

## Be careful: this project is still under development.

# SoftKit Pack for Codex

SoftKit is a repository-local workflow pack for long-running software projects. The orchestrator reads project primitives and change inputs, proposes the next cycle for user approval, and coordinates specialist stages through persistent work items and gates.

## Codex-compatible layout

```text
AGENTS.md
.agents/
└── skills/
    ├── softkit-orchestrator/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── scripts/
    ├── softkit-interrogator/
    ├── softkit-philosopher/
    ├── softkit-architect/
    ├── softkit-coder/
    ├── softkit-qa/
    ├── softkit-reviewer/
    └── softkit-devops/
.softkit/
├── softkit-protocol.md
└── templates/
```

Codex discovers repository skills under `.agents/skills`. Every skill is a directory containing `SKILL.md`. The orchestrator allows implicit invocation; specialist skills disable implicit invocation and remain available through explicit `$skill-name` mentions.

## Install in a new repository

Copy the complete contents of this pack into the repository root, preserving hidden directories:

```bash
cp -a softkit-pack-codex/. /path/to/project/
```

Create or edit the initial premises:

```text
softkit-input/project-primitives.md
softkit-input/premises/pseudocode/
softkit-input/premises/examples/
softkit-input/premises/references/
softkit-input/changes/inbox/
```

You may let the orchestrator create the initial draft and control directories:

```text
$softkit-orchestrator initialize this project
```

When terminal execution is available, it may run:

```bash
python3 .agents/skills/softkit-orchestrator/scripts/bootstrap_softkit.py --project-name "Project Name"
python3 .agents/skills/softkit-orchestrator/scripts/scan_sources.py
```

The generated `project-primitives.md` remains `draft` until you approve it.

## Toml

For Integration we had a .toml of the project created.

## Continue a project

From the repository root, start Codex and invoke:

```text
$softkit-orchestrator continue the project and propose the next cycle
```

In Codex CLI or the IDE extension, `/skills` lists the available skills.

## Main rules

- `AGENTS.md` provides concise instructions that Codex reads at session start.
- `.softkit/softkit-protocol.md` is the single detailed protocol.
- `.softkit/templates/` is the single template directory.
- All managed paths are repository-relative.
- Substantial work requires an approved work item.
- The orchestrator proposes the workflow; the user approves or adjusts it.
- Approval by cycle is the default for long projects.
- Specialist stages do not implicitly activate from ordinary prompts.
- Implementation is not considered verified until required validation passes.

## Validate the pack

```bash
python3 .agents/skills/softkit-orchestrator/scripts/validate_softkit.py
```

 🔴 Progress

 [██░░░░░░░░] 20%

 🔴 Testing
 
 [██░░░░░░░░] 30%

TODO:
Test in different scenarios, loop for final validation.