#!/usr/bin/env python3
"""Initialize the repository-local SoftKit control structure from canonical templates."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import json
import shutil

REQUIRED_TEMPLATES = (
    "project-primitives.template.md",
    "project-state.template.yaml",
    "work-item.template.yaml",
    "change-request.template.md",
    "module-schema.toml",
)


SKILLS = ("orchestrator", "interrogator", "philosopher", "architect", "coder", "qa", "reviewer", "devops")
SCRIPTS = ("bootstrap_softkit.py", "create_work_item.py", "scan_sources.py", "validate_softkit.py")


def install_package(source: Path, target: Path) -> None:
    required = [Path("AGENTS.md"), Path(".softkit/softkit-protocol.md")]
    required += [Path(".softkit/templates") / name for name in REQUIRED_TEMPLATES]
    required += [Path(".softkit/scripts") / name for name in SCRIPTS]
    for name in SKILLS:
        base = Path(".agents/skills") / ("softkit-" + name)
        required += [base / "SKILL.md", base / "agents/openai.yaml"]
    required += [Path(".agents/skills/softkit-orchestrator/scripts") / name for name in SCRIPTS]
    missing = [str(rel) for rel in required if not (source / rel).is_file()]
    if missing:
        raise SystemExit("Incomplete source installation: " + ", ".join(missing))
    files = set(required)
    for directory in [Path(".softkit/templates"), Path(".softkit/scripts")] + [
        Path(".agents/skills") / ("softkit-" + name) for name in SKILLS
    ]:
        files.update(p.relative_to(source) for p in (source / directory).rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    conflicts = []
    # Inspect every output path before creating directories or copying files.
    managed = [Path("module.toml"), Path("softkit-input/project-primitives.md"),
               Path("specs/00_Project_Control/project-state.yaml")]
    directories = [Path("softkit-input/premises") / x for x in ("pseudocode", "examples", "references")]
    directories += [Path("softkit-input/changes") / x for x in ("inbox", "accepted", "applied", "rejected", "archived")]
    directories += [Path("specs/00_Project_Control") / x for x in ("work-items", "workflows", "change-impact")]
    directories += [Path("specs") / x for x in ("01_Project_Policy", "02_Requirements", "03_Architecture", "04_Implementation", "05_Validation", "06_Operations")]
    for rel in sorted(files | set(managed) | set(directories)):
        dest = target / rel
        for parent in (dest.parent, *dest.parents):
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                conflicts.append(str(parent))
        if dest.is_symlink():
            conflicts.append(str(dest))
        elif dest.exists():
            if rel in directories:
                if not dest.is_dir():
                    conflicts.append(str(dest))
            elif not dest.is_file() or (rel in files and dest.read_bytes() != (source / rel).read_bytes()):
                conflicts.append(str(dest))
    if conflicts:
        raise SystemExit("Conflicts; no files copied. Reconcile explicitly: " + ", ".join(sorted(set(conflicts))))
    for rel in sorted(files):
        dest = target / rel
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / rel, dest)


def replace_yaml_scalar(text: str, key: str, value: str, indent: int) -> str:
    pattern = rf"(?m)^{{indent}}{re.escape(key)}:\s*.*$".replace("{indent}", " " * indent)
    replacement = " " * indent + key + ": " + json.dumps(value, ensure_ascii=False)
    return re.sub(pattern, lambda _: replacement, text, count=1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", nargs="?")
    parser.add_argument("--root")
    parser.add_argument("--project-name")
    args = parser.parse_args()

    if args.destination is not None and args.root is not None:
        parser.error("use destination or --root, not both")
    source = Path(__file__).resolve().parents[2]
    root = Path(args.destination or args.root or ".").expanduser().resolve()
    install_package(source, root)
    templates = root / ".softkit/templates"

    project_name = args.project_name or root.name
    today = datetime.now().date().isoformat()
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    manifest = root / "module.toml"
    if not manifest.exists():
        # Read the canonical schema, but never promote its examples to facts.
        (templates / "module-schema.toml").read_text()
        text = 'schema_version = 1\nmodules = []\n\n[manifest]\nkind = "softkit-modules"\n\n# Module discovery pending: register only evidence-backed modules and contracts.\n'
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
        text = text.replace("project: <project-name>", "project: " + json.dumps(project_name, ensure_ascii=False))
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
