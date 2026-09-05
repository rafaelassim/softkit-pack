#!/usr/bin/env python3
"""Initialize the repository-local SoftKit control structure from canonical templates."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil

REQUIRED_TEMPLATES = (
    "project-primitives.template.md",
    "project-state.template.yaml",
    "work-item.template.yaml",
    "change-request.template.md",
    "module-schema.toml",
)


def find_root(start: Path) -> Path:
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".softkit" / "softkit-protocol.md").is_file():
            return candidate
    raise SystemExit("SoftKit root not found: .softkit/softkit-protocol.md is missing")


def replace_yaml_scalar(text: str, key: str, value: str, indent: int) -> str:
    pattern = rf"(?m)^{{indent}}{re.escape(key)}:\s*.*$".replace("{indent}", " " * indent)
    replacement = " " * indent + f'{key}: "{value.replace(chr(34), chr(92)+chr(34))}"'
    return re.sub(pattern, replacement, text, count=1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--project-name")
    args = parser.parse_args()

    root = find_root(Path(args.root))
    templates = root / ".softkit" / "templates"
    missing = [name for name in REQUIRED_TEMPLATES if not (templates / name).is_file()]
    if missing:
        raise SystemExit("Incomplete SoftKit installation; missing templates: " + ", ".join(missing))

    project_name = args.project_name or root.name
    today = datetime.now().date().isoformat()
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    manifest = root / "module.toml"
    if not manifest.exists():
        module_name = re.sub(r"[^a-z0-9]+", "_", project_name.lower()).strip("_")
        text = f'''schema_version = 1

[manifest]
kind = "softkit-modules"

[defaults]
language = ""
runtime = ""
tests_root = "tests"

[[modules]]
id = "MOD001"
name = "{module_name}"
description = "Root project module."
kind = "library"
path = "."
package = ""
entry_point = ""
lifecycle = "active"

[modules.responsibility]
summary = "Root project module."
provides = []
excludes = []

[modules.paths]
source = "src"
tests = "tests"
examples = "examples"
resources = ""
generated = ""

[modules.specifications]
requirements = "specs/02_Requirements"
architecture = "specs/03_Architecture"
implementation = "specs/04_Implementation"
validation = "specs/05_Validation"
operations = "specs/06_Operations"

[modules.runtime]
language = ""
version = ""
framework = ""
package_manifest = ""

[modules.ownership]
architecture = "softkit-architect"
implementation = "softkit-coder"
validation = "softkit-qa"
review = "softkit-reviewer"
operations = "softkit-devops"
'''
        manifest.write_text(text)
        print(f"created: {manifest.relative_to(root)}")

    for rel in (
        "softkit-input/premises/pseudocode",
        "softkit-input/premises/examples",
        "softkit-input/premises/references",
        "softkit-input/changes/inbox",
        "softkit-input/changes/accepted",
        "softkit-input/changes/applied",
        "softkit-input/changes/rejected",
        "softkit-input/changes/archived",
        "specs/00_Project_Control/work-items",
        "specs/00_Project_Control/workflows",
        "specs/00_Project_Control/change-impact",
        "specs/01_Project_Policy",
        "specs/02_Requirements",
        "specs/03_Architecture",
        "specs/04_Implementation",
        "specs/05_Validation",
        "specs/06_Operations",
    ):
        (root / rel).mkdir(parents=True, exist_ok=True)

    primitives = root / "softkit-input" / "project-primitives.md"
    if not primitives.exists():
        text = (templates / "project-primitives.template.md").read_text()
        text = text.replace("project: <project-name>", f'project: "{project_name}"')
        text = text.replace("updated: YYYY-MM-DD", f"updated: {today}")
        # A generated primitives file is a draft until the user approves it.
        text = text.replace("status: approved", "status: draft", 1)
        primitives.write_text(text)
        print(f"created draft: {primitives.relative_to(root)}")

    state = root / "specs" / "00_Project_Control" / "project-state.yaml"
    if not state.exists():
        text = (templates / "project-state.template.yaml").read_text()
        text = replace_yaml_scalar(text, "name", project_name, 2)
        text = re.sub(r"(?m)^last_reconciled:\s*.*$", f'last_reconciled: "{now}"', text, count=1)
        state.write_text(text)
        print(f"created: {state.relative_to(root)}")

    print("SoftKit bootstrap complete")


if __name__ == "__main__":
    main()
