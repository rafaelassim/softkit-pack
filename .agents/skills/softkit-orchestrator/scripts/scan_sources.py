#!/usr/bin/env python3
"""Build a deterministic source index for SoftKit inputs."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json


def find_root(start: Path) -> Path:
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".softkit" / "softkit-protocol.md").is_file():
            return candidate
    raise SystemExit("SoftKit root not found")


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def classify(path: Path, root: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "softkit-input/project-primitives.md":
        return "project-primitives"
    if "/changes/" in rel:
        return "change-input"
    if "/pseudocode/" in rel:
        return "pseudocode"
    if "/examples/" in rel:
        return "example"
    if "/references/" in rel:
        return "reference"
    return "premise"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = find_root(Path(args.root))

    inputs = root / "softkit-input"
    files = sorted(p for p in inputs.rglob("*") if p.is_file()) if inputs.exists() else []
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    lines = ["schema_version: 1", f"generated_at: {q(now)}", "sources:"]
    for path in files:
        data = path.read_bytes()
        stat = path.stat()
        rel = path.relative_to(root).as_posix()
        lines.extend([
            f"  - path: {q(rel)}",
            f"    type: {classify(path, root)}",
            f"    sha256: {q(sha256(data).hexdigest())}",
            f"    size: {stat.st_size}",
            f"    modified_ns: {stat.st_mtime_ns}",
        ])
    target = root / "specs" / "00_Project_Control" / "source-index.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n")
    print(target.relative_to(root))


if __name__ == "__main__":
    main()
