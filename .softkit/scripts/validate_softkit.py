#!/usr/bin/env python3
"""Validate a repository-local SoftKit installation and skill packaging."""
from __future__ import annotations
import argparse
from pathlib import Path
import re

SKILLS = (
    "softkit-orchestrator", "softkit-interrogator", "softkit-philosopher",
    "softkit-architect", "softkit-coder", "softkit-qa",
    "softkit-reviewer", "softkit-devops",
)
TEMPLATES = (
    "project-primitives.template.md", "project-state.template.yaml",
    "work-item.template.yaml", "change-request.template.md", "module-schema.toml",
)


def validate_project(root: Path, errors: list[str]) -> None:
    try:
        import yaml
        import tomllib
    except ImportError:
        errors.append("project validation requires Python 3.11+ and PyYAML; pack checks need neither")
        return

    def read_yaml(path: Path):
        try:
            return yaml.safe_load(path.read_text())
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"cannot read YAML {path.relative_to(root)}: {exc}")
            return None

    def structure(value, template, label):
        if isinstance(template, dict):
            if not isinstance(value, dict):
                errors.append(f"expected mapping: {label}")
                return
            for key, expected in template.items():
                if key not in value:
                    errors.append(f"missing key: {label}.{key}")
                else:
                    structure(value[key], expected, f"{label}.{key}")
        elif template is not None and type(value) is not type(template):
            errors.append(f"wrong type: {label}")

    def managed(path, template_name):
        value = read_yaml(path)
        template = read_yaml(root / ".softkit/templates" / template_name)
        if value is not None and isinstance(template, dict):
            structure(value, template, str(path.relative_to(root)))
            if isinstance(value, dict):
                for key in ("schema_version", "generated_from"):
                    if value.get(key) != template.get(key):
                        errors.append(f"unexpected {key}: {path.relative_to(root)}")
        return value

    try:
        manifest = tomllib.loads((root / "module.toml").read_text())
        if manifest.get("schema_version") != 1 or manifest.get("manifest", {}).get("kind") != "softkit-modules":
            errors.append("invalid module.toml schema or manifest kind")
        if not isinstance(manifest.get("modules"), list):
            errors.append("module.toml must declare a modules array (may be empty during discovery)")
    except (OSError, ValueError, AttributeError) as exc:
        errors.append(f"invalid module.toml: {exc}")

    primitives = root / "softkit-input/project-primitives.md"
    if not primitives.is_file():
        errors.append("missing: softkit-input/project-primitives.md")
    control = root / "specs/00_Project_Control"
    state = managed(control / "project-state.yaml", "project-state.template.yaml")
    items = {}
    for path in sorted((control / "work-items").glob("WI-*.yaml")):
        wi = managed(path, "work-item.template.yaml")
        if not isinstance(wi, dict):
            continue
        if wi.get("id") != path.stem:
            errors.append(f"work item ID differs from filename: {path.name}")
        items[path.stem] = wi
        workflow = wi.get("workflow")
        if not isinstance(workflow, dict):
            continue
        document = workflow.get("document")
        if workflow.get("status") == "approved" and not document:
            errors.append(f"approved workflow requires document: {path.name}")
        if document and isinstance(document, str):
            target = (root / document).resolve()
            if Path(document).is_absolute() or not target.is_relative_to(root) or not target.is_file():
                errors.append(f"missing or non-local workflow document: {path.name}")
    if isinstance(state, dict) and isinstance(state.get("active_work_items"), list):
        for wi_id in state["active_work_items"]:
            if not isinstance(wi_id, str) or wi_id not in items:
                errors.append(f"active work item not found: {wi_id}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--mode", choices=("pack", "project"), default="pack")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    required = [
        root / "AGENTS.md",
        root / ".softkit" / "softkit-protocol.md",
    ]
    required += [root / ".softkit" / "templates" / x for x in TEMPLATES]
    required += [root / ".softkit/scripts" / name for name in ("bootstrap_softkit.py", "create_work_item.py", "scan_sources.py", "validate_softkit.py")]
    for name in SKILLS:
        required += [
            root / ".agents" / "skills" / name / "SKILL.md",
            root / ".agents" / "skills" / name / "agents" / "openai.yaml",
        ]
    for path in required:
        if not path.is_file():
            errors.append(f"missing: {path.relative_to(root)}")

    for name in SKILLS:
        path = root / ".agents" / "skills" / name / "SKILL.md"
        if not path.is_file():
            continue
        text = path.read_text()
        if not text.startswith("---\n") or "\nname:" not in text or "\ndescription:" not in text:
            errors.append(f"invalid frontmatter: {path.relative_to(root)}")
        if "$ARGUMENTS" in text:
            errors.append(f"unsupported $ARGUMENTS placeholder: {path.relative_to(root)}")
        if re.search(r"`/(?:\.softkit|softkit-input|specs)/", text):
            errors.append(f"absolute managed path: {path.relative_to(root)}")

    if args.mode == "project":
        validate_project(root, errors)

    if errors:
        print("SoftKit validation failed:")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print(f"SoftKit {args.mode} validation passed (structural checks only)")


if __name__ == "__main__":
    main()
