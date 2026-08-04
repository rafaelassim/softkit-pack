# SoftKit Repository Instructions

All paths below are relative to the repository root.

## Default workflow

- For project initialization, continuation, substantial changes, prioritization, or status, use `$softkit-orchestrator` first.
- Read `.softkit/softkit-protocol.md` before creating or changing SoftKit-managed artifacts.
- Read `softkit-input/project-primitives.md` before planning or implementing project changes.
- Do not perform substantial implementation outside an active, approved work item in `specs/00_Project_Control/work-items/`.
- Specialist skills are explicit stages. Do not bypass the orchestrator unless the user explicitly invokes a specialist and an approved work item already assigns that stage.
- Treat `.softkit/templates/` as executable schemas, not optional examples.
- Do not silently contradict normative premises, enlarge scope, add major dependencies, change public interfaces, or claim unexecuted tests passed.

## Control files

- Global state: `specs/00_Project_Control/project-state.yaml`
- Work items: `specs/00_Project_Control/work-items/`
- Incoming changes: `softkit-input/changes/inbox/`
- Project primitives: `softkit-input/project-primitives.md`

## Codex usage

- Explicitly invoke the coordinator with `$softkit-orchestrator`.
- Use `/skills` to inspect available skills in Codex CLI or the IDE extension.
