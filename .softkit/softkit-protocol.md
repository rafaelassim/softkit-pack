# SoftKit Project Protocol

All paths in this protocol are relative to the repository root.

## 0. Codex Packaging and Entry Point

- Repository skills live under `.agents/skills/<skill-name>/SKILL.md`.
- `$softkit-orchestrator` is the normal explicit entry point.
- Only `softkit-orchestrator` may be invoked implicitly. Specialist skills require explicit invocation or an approved orchestrator stage.
- `AGENTS.md` supplies the minimal always-on repository guidance; this protocol supplies the detailed SoftKit workflow.
- `.softkit/` is the only support directory. Do not create a parallel `protocol/` or second template directory.

## 1. Canonical Protocol and Templates

```text
.softkit/
├── softkit-protocol.md
└── templates/
    ├── project-primitives.template.md
    ├── project-state.template.yaml
    ├── work-item.template.yaml
    ├── change-request.template.md
    └── module-schema.toml
```

Every SoftKit skill must read `.softkit/softkit-protocol.md`. The orchestrator must read the applicable canonical template before creating or repairing a managed artifact.

Template rules:

- If `specs/00_Project_Control/project-state.yaml` is missing, read `.softkit/templates/project-state.template.yaml`, copy its complete structure, and populate known values.
- Before creating `specs/00_Project_Control/work-items/WI-XXX.yaml`, read `.softkit/templates/work-item.template.yaml`, copy its complete structure, allocate the next stable ID, and populate approved data.
- If `softkit-input/project-primitives.md` is missing, read `.softkit/templates/project-primitives.template.md` and create or propose a draft. It remains `draft` until the user approves it.
- When normalizing an inbox change, read `.softkit/templates/change-request.template.md`; preserve the original and create a structured derivative.
- When `module.toml` is missing, read `.softkit/templates/module-schema.toml`, create the root manifest from repository evidence, and remove example-only entries that do not describe the project. An empty `modules = []` registry is valid while discovery is pending; the bootstrap helper must not invent module types or paths.
- When a managed artifact exists, add missing structural keys conservatively; never replace confirmed values or silently migrate semantics.
- Preserve `schema_version` and `generated_from` in YAML-managed artifacts.
- If the protocol or a required template is missing, stop and report an incomplete installation.

Bootstrap installs the package from its script location into the exact destination (positional path or `--root`, default cwd). Validate source completeness and destination conflicts before copying; preserve existing project data and never copy the source project history. Installation conflicts require explicit reconciliation.

When command execution is available, prefer the deterministic scripts in `.softkit/scripts/` for bootstrap, work-item allocation, source indexing, and structural validation.

## 2. Canonical Project Paths

```text
softkit-input/
├── project-primitives.md
├── premises/
│   ├── pseudocode/
│   ├── examples/
│   └── references/
└── changes/
    ├── inbox/
    ├── accepted/
    ├── applied/
    ├── rejected/
    └── archived/

specs/
├── 00_Project_Control/
│   ├── project-state.yaml
│   ├── source-index.yaml
│   ├── traceability.md
│   ├── workflows/
│   ├── work-items/
│   └── change-impact/
├── 01_Project_Policy/
├── 02_Requirements/
├── 03_Architecture/
├── 04_Implementation/
├── 05_Validation/
└── 06_Operations/
```

If the repository already uses an equivalent documented structure, preserve it and record the mapping in `project-state.yaml`. Do not create parallel structures silently.

## 3. Mandatory Preflight

Before specialized work:

1. Read `softkit-input/project-primitives.md`.
2. Recursively inspect relevant files under `softkit-input/premises/`.
3. Read `specs/00_Project_Control/project-state.yaml`.
4. Read the active work item under `specs/00_Project_Control/work-items/`.
5. Read the approved workflow at `workflow.document` in the work item. If an older work item lacks this field, link the existing approved plan without inventing approval; reconcile any disagreement before execution.
6. Read every source document linked by the work item.
7. Inspect existing target artifacts and implementation.
8. Reconcile recorded state with actual files.
9. Stop and record a blocker when an action contradicts a normative source or exceeds approved boundaries.

If no active approved work item exists, specialist skills must not invent one. Return control to `$softkit-orchestrator`.

## 4. Source Authority

Use this precedence unless an approved project rule overrides it:

1. Approved change request that explicitly supersedes earlier rules.
2. `project-primitives.md`.
3. Normative premises.
4. Approved ADRs and policies.
5. Approved requirements and use cases.
6. Approved architecture and interface contracts.
7. Preferred examples.
8. Informative examples and pseudocode.
9. Existing implementation as evidence of current behavior.
10. Agent assumptions.

Never treat an inbox change as approved. Never let an example silently override a normative rule.

Recommended authority values:

```text
normative | preferred | informative | historical | deprecated
```

## 5. Artifact States

```text
missing | draft | needs-input | ready-for-review | approved
implemented | verified | blocked | superseded | rejected
```

`implemented` is not the same as `verified`.

## 6. Work Items

Every substantial action belongs to a work item recording objective, origin, affected submodules, sources, requirements, architecture, approved workflow, current gate, approval boundaries, stop conditions, evidence, and blockers.

The external workflow document is the canonical approved plan. The work item stores execution status, gates and evidence; its `workflow.steps` summarizes the plan. Keep that summary consistent with the document.

Do not expand scope silently. Record unrelated discoveries as follow-up proposals; allocate a new work item after the required workflow approval.

## 7. Workflow Proposal and Approval

The orchestrator proposes; the user approves, adjusts, defers, or rejects.

For long projects use two planning horizons:

- a high-level roadmap;
- a detailed workflow only for the next cycle or work item.

Approval modes:

- `supervised`: approval before each specialist stage;
- `cycle`: one approval for the proposed cycle; default for long projects;
- `autonomous-limited`: low-risk work continues within explicit boundaries.

Explicit user approval for the same scope remains sufficient; do not ask again merely to reproduce it in a control artifact. Draft primitives are context, not approved constraints. Bounded maintenance explicitly authorized by the user can proceed while inferred project-wide primitives remain draft.

An approved workflow remains valid across sessions until completed, superseded, blocked, or materially changed.

## 8. Mandatory Stop Conditions

Stop and return to the user before:

- contradicting a normative primitive;
- changing the primary language, framework, public API, protocol, or persistent schema outside approved boundaries;
- adding a major dependency not previously approved;
- destructive migration or irreversible action;
- material scope, cost, risk, or operational expansion;
- accepting unresolved safety or security risk;
- modifying another approved work item;
- continuing after validation evidence invalidates the plan.

## 9. Persistence

After meaningful work:

1. update the work item;
2. update `project-state.yaml`;
3. update traceability when relationships changed;
4. record created or modified artifacts;
5. record actual commands and evidence;
6. preserve IDs and never renumber confirmed artifacts;
7. record one explicit next step or blocker.

Never claim that a build, test, deployment, migration, or command succeeded unless it was executed and inspected.

## 10. Handoff Contract

```markdown
## SoftKit Handoff

**Work Item:** WI-XXX
**Stage:** <stage>
**Result:** completed | partial | blocked
**Artifacts Changed:** ...
**Evidence:** ...
**Open Issues:** ...
**Recommended Next Skill:** ...
**Next Gate:** ...
**User Decision Required:** none | <decision>
```

The orchestrator evaluates handoffs and updates execution state. Specialist skills do not mark the whole work item complete.

QA and review must record the executor and relationship to implementation. A different skill stage in the same agent is self-validation or self-review, not independent evidence. When the approved workflow requires independence, use a separate permitted executor that did not implement the change; if unavailable, record the gate as blocked. Otherwise same-executor checks are allowed with that limitation disclosed. Do not spawn agents unless delegation is authorized.

The Architect owns architectural decisions and ADRs. The Philosopher owns engineering policies and refers architectural decisions to the orchestrator for an Architect stage; it may supply policy constraints and alternatives but does not author the architectural decision.

## 11. Universal Guardrails

- Prefer the smallest complete change.
- Ask only when missing information materially changes the result or makes work unsafe.
- Record non-blocking assumptions explicitly.
- Preserve backward compatibility unless an approved source changes it.
- Do not invent APIs, schemas, files, commands, dependencies, or test results.
- Do not perform unrelated refactoring.
- Keep generated documentation concise and traceable.
