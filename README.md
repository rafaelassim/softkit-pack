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
    │   └── scripts/  # compatibility wrappers
    ├── softkit-interrogator/
    ├── softkit-philosopher/
    ├── softkit-architect/
    ├── softkit-coder/
    ├── softkit-qa/
    ├── softkit-reviewer/
    └── softkit-devops/
.softkit/
├── softkit-protocol.md
├── scripts/          # canonical helpers
└── templates/
```

Codex discovers repository skills under `.agents/skills`. Every skill is a directory containing `SKILL.md`. The orchestrator allows implicit invocation; specialist skills disable implicit invocation and remain available through explicit `$skill-name` mentions.

## Install in a new repository

Run the bootstrap from this pack, providing the exact destination directory:

```bash
python3 .softkit/scripts/bootstrap_softkit.py /path/to/project --project-name "Project Name"
```

The destination is created if missing. The script installs the eight skills,
canonical tools, templates, protocol and AGENTS.md, then generates fresh project
control files. It does not copy this pack's Git history, work items or premises.
Existing project data is preserved. Identical installation files are reused;
conflicting files (including custom AGENTS.md) are reported before any copying.
Reconcile conflicts explicitly; this command is not a forced upgrade tool.

`--root /path/to/project` remains supported instead of the positional destination.
With neither option, the current directory is the exact destination. The source
package is located relative to the script, so invocation from another cwd works.

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
python3 .softkit/scripts/bootstrap_softkit.py --project-name "Project Name"
python3 .softkit/scripts/scan_sources.py
```

The generated `project-primitives.md` remains `draft` until you approve it.

## Toml

`module.toml` records discovered modules and integration contracts. Bootstrap creates
an empty module registry; the orchestrator populates it from repository evidence.
Unknown module types, source paths and interfaces must not be guessed.

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

Pack validation does not require an initialized consumer project.

```bash
python3 .softkit/scripts/validate_softkit.py
```

 🔴 Progress

 [██░░░░░░░░] 20%

 🔴 Testing
 
 [██░░░░░░░░] 30%

TODO:
Test in different scenarios, loop for final validation.

For an initialized project, also validate the manifest, state and work-item
structure (Python 3.11+ and PyYAML must be available):

```bash
python3 .softkit/scripts/validate_softkit.py --mode project
```

These checks do not certify user approval, semantic consistency or test success.
The approved plan lives at the work item's `workflow.document`; execution state
and evidence live in the work item. Same-executor QA/review is identified as such.


Create a work item interactively from the repository root:

```bash
python3 .softkit/scripts/create_work_item.py
```

With no arguments, a terminal is required. Title and objective are mandatory;
origin and priority offer defaults. Ctrl-C or EOF cancels without creating a file.
For automation, pass `--title` and `--objective`; incomplete arguments fail without
prompting. The old orchestrator script paths remain compatibility wrappers.


The interactive creator first selects `work-item` or `change-request`. Known options
use arrows and Enter on compatible POSIX terminals, or a numbered menu otherwise.
Press q in the arrow menu, Ctrl-C, or EOF to cancel.

To create a proposed change request directly:

```bash
python3 .softkit/scripts/create_work_item.py --artifact-type change-request --title "Change title" --objective "Requested behavior"
```

Change requests use the canonical Markdown template in `softkit-input/changes/inbox/`;
work items use YAML in `specs/00_Project_Control/work-items/`. `--origin-type` remains
work-item metadata. The default artifact type is `work-item` for existing automation.
CR IDs consider all change lifecycle folders. Creating a request does not approve it.
