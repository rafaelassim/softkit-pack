#!/usr/bin/env python3
"""Validate a repository-local SoftKit installation and skill packaging."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

SKILLS = (
    "softkit-orchestrator", "softkit-interrogator", "softkit-philosopher",
    "softkit-architect", "softkit-coder", "softkit-qa",
    "softkit-reviewer", "softkit-devops",
)
TEMPLATES = (
    "project-primitives.template.md", "project-state.template.yaml",
    "work-item.template.yaml", "change-request.template.md", "module-schema.toml",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    required = [
        root / "AGENTS.md",
        root / "module.toml",
        root / ".softkit" / "softkit-protocol.md",
    ]
    required += [root / ".softkit" / "templates" / x for x in TEMPLATES]
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

    if errors:
        print("SoftKit validation failed:")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print("SoftKit installation is structurally valid")


if __name__ == "__main__":
    main()
