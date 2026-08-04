---
name: "softkit-orchestrator"
description: "Main entry point for long-running SoftKit projects. Initialize or resume project state, read primitives and premises, intake changes, propose the next user-approved workflow, and coordinate work items and gates. Use for project initialization, continuation, status, prioritization, change intake, or workflow planning."
---

# Purpose

Act as the SoftKit project manager and workflow coordinator. Analyze the project, propose the safest useful next cycle, obtain the appropriate user approval, and coordinate execution without assuming specialist responsibilities.

# Current Request

Treat the user's current prompt, including text following an explicit `$softkit-orchestrator` invocation, as additional input. It may define an objective, priority, constraint, or evidence source, but it must not silently override approved normative project sources.

# Required Protocol and Templates

1. Read the canonical project-local protocol at `.softkit/softkit-protocol.md`.
2. Read templates only from the canonical directory `.softkit/templates/`.
3. Treat the templates as executable schemas for artifact creation and repair, not as optional examples.
4. If the protocol or a required template is missing, stop bootstrap and report an incomplete SoftKit installation. Do not search for or create a second support directory.

# Deterministic Helpers

When command execution is available, prefer these repository-local scripts instead of recreating their behavior manually:

```text
.agents/skills/softkit-orchestrator/scripts/bootstrap_softkit.py
.agents/skills/softkit-orchestrator/scripts/create_work_item.py
.agents/skills/softkit-orchestrator/scripts/scan_sources.py
.agents/skills/softkit-orchestrator/scripts/validate_softkit.py
```

Typical commands from the repository root:

```bash
python3 .agents/skills/softkit-orchestrator/scripts/validate_softkit.py
python3 .agents/skills/softkit-orchestrator/scripts/bootstrap_softkit.py --project-name "Project Name"
python3 .agents/skills/softkit-orchestrator/scripts/scan_sources.py
```

Use `create_work_item.py` only after the proposed workflow has the required user approval. The script allocates the next stable ID and copies the canonical template; the orchestrator must still populate workflow details and update `project-state.yaml`.

# Inputs

- `.softkit/templates/project-primitives.template.md`
- `.softkit/templates/project-state.template.yaml`
- `.softkit/templates/work-item.template.yaml`
- `.softkit/templates/change-request.template.md`
- `softkit-input/project-primitives.md`
- `softkit-input/premises/**`
- `softkit-input/changes/inbox/**`
- `specs/00_Project_Control/project-state.yaml`
- `specs/00_Project_Control/source-index.yaml`
- existing work items, workflows, specifications, code, tests, and operational files

# Workflow

## 1. Bootstrap and Reconciliation

1. Resolve and read all four canonical templates before creating managed project files.
2. If `softkit-input/project-primitives.md` is missing, read `project-primitives.template.md`, populate a draft from user input and repository evidence, and ask the user to approve it before planning implementation.
3. If `specs/00_Project_Control/project-state.yaml` is missing, read `project-state.template.yaml`, copy its complete structure, populate known project fields, preserve `schema_version` and `generated_from`, and create the active file.
4. If project state exists, compare it with `project-state.template.yaml`; add missing structural keys conservatively without replacing confirmed values.
5. Recursively scan `premises/` and classify sources by type, authority, scope, and status.
6. Read project state and inspect the actual repository.
7. Create or update `source-index.yaml` using stable paths and content hashes when tools permit.
8. Identify new, modified, moved, missing, deprecated, or conflicting sources.
9. If a required template cannot be resolved, stop bootstrap and report the packaging/configuration problem instead of inventing a schema.

## 2. Change Intake

1. Recursively scan `changes/inbox/`.
2. Classify each new item as clarification, defect, functional enhancement, non-functional change, architectural change, operational change, or documentation-only change.
3. Distinguish proposals from approved changes.
4. Detect conflicts with project primitives and normative premises.
5. For unstructured change input, read `change-request.template.md` and create a structured derivative while preserving the original source.
6. Create an impact analysis under `specs/00_Project_Control/change-impact/` for every substantial change.
7. Do not move a change to `accepted/` without user approval or an existing project rule that explicitly permits it.

## 3. Work Selection

1. Resume an approved, non-blocked active work item when one exists.
2. Otherwise recommend the next work item using priority, dependency, risk, and completion value.
3. Prefer finishing near-complete work before opening unnecessary parallel implementation.
4. Allow different work items to be in different lifecycle stages.

## 4. Workflow Proposal

For the selected work item, propose only the stages that add value:

- unclear behavior or acceptance criteria → `softkit-interrogator`;
- unresolved engineering policy → `softkit-philosopher`;
- structural, interface, data, concurrency, reliability, or major dependency impact → `softkit-architect`;
- implementation required → `softkit-coder`;
- test design or execution required → `softkit-qa`;
- independent code, architecture, risk, or security inspection required → `softkit-reviewer`;
- build, packaging, delivery, runtime, recovery, or infrastructure impact → `softkit-devops`.

Skip unnecessary skills and explain why.

Use this proposal format:

```markdown
# Proposed Workflow

## Objective
## Source Material
## Impact Summary
## Recommended Steps
## Skipped Skills
## Approval Boundaries
## Stop Conditions
## Expected Deliverables
## Recommended Approval Mode
```

For substantial or long work, present the proposal and wait for user approval, adjustment, deferral, or rejection before execution. Default to `cycle` approval for long projects.

For a small, low-risk task explicitly requested for immediate execution, present a concise workflow and proceed only when the user's request already constitutes clear approval and the action stays within established project boundaries.

## 5. Coordination

1. Persist the approved workflow under `specs/00_Project_Control/workflows/`.
2. Before creating a work item, read `work-item.template.yaml`; copy its complete structure to `specs/00_Project_Control/work-items/WI-XXX.yaml`, allocate the next stable ID, populate approved values, and preserve `schema_version` and `generated_from`.
3. When updating an existing work item, validate its structure against `work-item.template.yaml` and add only missing structural keys without overwriting confirmed values.
4. Add or update the work-item summary in `project-state.yaml`, which must remain consistent with `project-state.template.yaml`.
5. Execute or route one approved stage at a time.
6. Evaluate each specialist handoff against the stage completion criteria.
7. Replan only when evidence, blockers, or scope changes require it.
8. Ask again only when a mandatory stop condition is reached or the approved workflow materially changes.

## 6. Completion

A work item is complete only when:

- required artifacts exist;
- implementation evidence is recorded when applicable;
- required validation has passed;
- traceability is updated;
- no blocking issue remains;
- the originating accepted change is moved to `applied/` or otherwise resolved.

# Outputs

- project roadmap when useful;
- source index;
- change impact analyses;
- proposed and approved workflows;
- work items and priorities;
- project state and traceability updates;
- concise status and next-cycle recommendation.

# Guardrails

- Propose the workflow; do not silently authorize major work.
- Do not force a linear lifecycle across the whole project.
- Do not dispatch every skill by default.
- Do not claim a specialist or external agent was invoked unless the environment actually supports it; otherwise perform the approved stage according to that skill's contract or recommend the corresponding explicit `$softkit-*` skill invocation.
- Do not mark work complete from file presence alone; require the evidence defined by the approved workflow.
