#!/usr/bin/env python3
"""Create the next stable SoftKit work item from the canonical template."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re


def find_root(start: Path) -> Path:
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".softkit" / "templates" / "work-item.template.yaml").is_file():
            return candidate
    raise SystemExit("SoftKit root not found")


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def next_id(work_dir: Path) -> str:
    maximum = 0
    for path in work_dir.glob("WI-*.yaml"):
        match = re.match(r"WI-(\d+)", path.stem)
        if match:
            maximum = max(maximum, int(match.group(1)))
    return f"WI-{maximum + 1:03d}"


def replace_line(text: str, key: str, value: str, indent: int = 0) -> str:
    prefix = " " * indent
    pattern = rf"(?m)^{re.escape(prefix + key)}:\s*.*$"
    return re.sub(pattern, prefix + key + ": " + value, text, count=1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--title", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--origin-type", choices=("change-request", "roadmap", "defect", "user-request"), default="user-request")
    parser.add_argument("--origin-id", default="")
    parser.add_argument("--priority", choices=("critical", "high", "medium", "low"), default="medium")
    args = parser.parse_args()

    root = find_root(Path(args.root))
    work_dir = root / "specs" / "00_Project_Control" / "work-items"
    work_dir.mkdir(parents=True, exist_ok=True)
    wi_id = next_id(work_dir)

    template = root / ".softkit" / "templates" / "work-item.template.yaml"
    text = template.read_text()
    text = replace_line(text, "id", wi_id)
    text = replace_line(text, "title", yaml_string(args.title))
    text = replace_line(text, "type", args.origin_type, 2)
    text = replace_line(text, "id", yaml_string(args.origin_id), 2)
    text = replace_line(text, "priority", args.priority)
    text = replace_line(text, "objective", yaml_string(args.objective))

    target = work_dir / f"{wi_id}.yaml"
    target.write_text(text)
    print(target.relative_to(root))


if __name__ == "__main__":
    main()
