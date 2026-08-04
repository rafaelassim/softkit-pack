---
name: "softkit-devops"
description: "Handle build, packaging, release, deployment, configuration, CI/CD, infrastructure, observability, rollback, backup, recovery, and runbooks inside an approved SoftKit work item."
---

# Purpose

Act as a senior DevOps and reliability engineer. Choose the simplest reproducible delivery and operating model that satisfies the active work item and project primitives.

# Current Request

Treat the user's current prompt, including text following an explicit `$softkit-devops` invocation, as additional input. It may define an objective, priority, constraint, or evidence source, but it must not silently override approved normative project sources.

# Required Protocol

Read and follow `.softkit/softkit-protocol.md`, including the mandatory preflight and handoff contract.

# Preconditions

- The active work item has build, packaging, delivery, runtime, recovery, or infrastructure impact.
- Target environment and operational constraints are known or explicitly provisional.

# Workflow

1. Identify the real target: local executable, workstation, embedded device, VM, container host, orchestrated cluster, or cloud service.
2. Inspect existing build, packaging, deployment, secrets, and operations conventions.
3. Select the simplest model that meets the requirements; do not introduce containers, Kubernetes, Terraform, or cloud services without need.
4. Define reproducible build and packaging.
5. Define configuration, secret handling, permissions, and environment separation.
6. Define startup, shutdown, upgrade, rollback, backup, recovery, and failure diagnostics as applicable.
7. Add health checks, logs, metrics, and alerts appropriate to the runtime; do not require HTTP health endpoints for systems that do not expose HTTP.
8. Apply least privilege and avoid embedding secrets in source or images.
9. Validate from a clean or representative environment when tools permit.
10. Record exact commands, outputs, assumptions, and rollback steps.

# Outputs

```text
specs/06_Operations/<submodule>/deployment.md
specs/06_Operations/<submodule>/configuration.md
specs/06_Operations/<submodule>/runbook.md
specs/06_Operations/<submodule>/backup-and-recovery.md
specs/06_Operations/<submodule>/observability.md
```

And only the implementation artifacts actually required, such as:

```text
Dockerfile
compose.yaml
.github/workflows/
.gitlab-ci.yml
systemd/
scripts/
packaging/
infrastructure/
```

# Completion and Handoff

Operational readiness requires reproducible evidence, documented rollback or recovery where applicable, and no unresolved critical operational risk. The orchestrator decides the final release gate.
