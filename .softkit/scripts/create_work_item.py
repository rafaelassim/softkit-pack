#!/usr/bin/env python3
"""Create the next stable SoftKit work item from the canonical template."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
import os
from datetime import date


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
    return re.sub(pattern, lambda _: prefix + key + ": " + value, text, count=1)


def select(label, choices, default):
    """Use curses arrows on capable POSIX terminals, numbered input elsewhere."""
    if os.name == "posix" and sys.stdout.isatty() and os.environ.get("TERM", "dumb") != "dumb":
        try:
            import curses
            def menu(screen):
                index = choices.index(default)
                screen.keypad(True)
                while True:
                    screen.erase()
                    screen.addstr(0, 0, label + " (arrows/Enter; q cancels)")
                    for row, choice in enumerate(choices, 1):
                        screen.addstr(row, 0, ("> " if row - 1 == index else "  ") + choice)
                    screen.refresh()
                    key = screen.getch()
                    if key == curses.KEY_UP:
                        index = (index - 1) % len(choices)
                    elif key == curses.KEY_DOWN:
                        index = (index + 1) % len(choices)
                    elif key in (10, 13, curses.KEY_ENTER):
                        return choices[index]
                    elif key in (3, 4, 27, ord("q")):
                        raise KeyboardInterrupt
            return curses.wrapper(menu)
        except ImportError:
            pass
        except curses.error:
            pass
    while True:
        print(label + ": " + ", ".join(f"{i}. {value}" for i, value in enumerate(choices, 1)))
        value = input(f"Selection [{choices.index(default) + 1}]: ").strip()
        if not value:
            return default
        if value.isdigit() and 1 <= int(value) <= len(choices):
            return choices[int(value) - 1]
        print("Invalid selection.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--artifact-type", choices=("work-item", "change-request"), default="work-item")
    parser.add_argument("--title", required=True)
    parser.add_argument("--objective", required=True, help="Work objective or requested change")
    parser.add_argument("--origin-type", choices=("change-request", "roadmap", "defect", "user-request"), default="user-request")
    parser.add_argument("--origin-id", default="")
    parser.add_argument("--priority", choices=("critical", "high", "medium", "low"), default="medium")
    if len(sys.argv) == 1:
        if not sys.stdin.isatty():
            parser.error("use --title and --objective without an interactive terminal")
        def ask(label, default=None):
            while True:
                value = input(label + ": ").strip()
                if value or default is not None:
                    return value or default
                print("Required field.")
        try:
            artifact = select("Artifact type", ("work-item", "change-request"), "work-item")
            title = ask("Title")
            objective = ask("Objective / Requested change")
            origin, origin_id = "user-request", ""
            if artifact == "work-item":
                origin = select("Origin type", ("change-request", "roadmap", "defect", "user-request"), "user-request")
                origin_id = ask("Origin ID", "")
            priority = select("Priority", ("critical", "high", "medium", "low"), "medium")
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled; no artifact created.", file=sys.stderr)
            raise SystemExit(130)
        args = parser.parse_args(["--artifact-type=" + artifact, "--title=" + title,
                                  "--objective=" + objective, "--origin-type=" + origin,
                                  "--origin-id=" + origin_id, "--priority=" + priority])
    else:
        args = parser.parse_args()
    if not args.title.strip() or not args.objective.strip():
        parser.error("title and objective must not be blank")

    root = find_root(Path(args.root))
    if args.artifact_type == "change-request":
        if args.origin_type != "user-request" or args.origin_id:
            parser.error("origin options apply only to work items")
        change_root = root / "softkit-input/changes"
        maximum = 0
        for path in change_root.rglob("CR-*.md"):
            match = re.match(r"CR-(\d+)(?:-|$)", path.stem)
            if match:
                maximum = max(maximum, int(match.group(1)))
        artifact_id = f"CR-{maximum + 1:03d}"
        text = (root / ".softkit/templates/change-request.template.md").read_text()
        text = replace_line(text, "id", artifact_id)
        text = replace_line(text, "title", yaml_string(args.title))
        text = replace_line(text, "priority", args.priority)
        text = replace_line(text, "submitted", date.today().isoformat())
        text = text.replace("# Requested Change", "# Requested Change\n\n" + args.objective, 1)
        target = change_root / "inbox" / f"{artifact_id}.md"
    else:
        work_dir = root / "specs/00_Project_Control/work-items"
        artifact_id = next_id(work_dir)
        text = (root / ".softkit/templates/work-item.template.yaml").read_text()
        text = replace_line(text, "id", artifact_id)
        text = replace_line(text, "title", yaml_string(args.title))
        text = replace_line(text, "type", args.origin_type, 2)
        text = replace_line(text, "id", yaml_string(args.origin_id), 2)
        text = replace_line(text, "priority", args.priority)
        text = replace_line(text, "objective", yaml_string(args.objective))
        target = work_dir / f"{artifact_id}.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x") as output:
        output.write(text)
    print(target.relative_to(root))


if __name__ == "__main__":
    main()
