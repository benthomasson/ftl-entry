"""Entry CLI — create chronologically organized documentation entries."""

import os
import re
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path


def _slugify(text: str) -> str:
    """Convert a title string to a kebab-case filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def cmd_create(args):
    now = datetime.now()
    entry_dir = Path.cwd() / "entries" / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")
    entry_dir.mkdir(parents=True, exist_ok=True)

    filename = args.filename
    title = args.title

    # If filename contains spaces, treat it as a title and derive the filename
    if " " in filename:
        title = title or filename
        filename = _slugify(filename)

    if not filename.endswith(".md"):
        filename += ".md"

    file_path = entry_dir / filename

    if file_path.exists():
        print(f"File already exists: {file_path}", file=sys.stderr)
        sys.exit(1)

    title = title or filename.removesuffix(".md").replace("-", " ").title()

    header = f"""# {title}

**Date:** {now.strftime('%Y-%m-%d')}
**Time:** {now.strftime('%H:%M')}

"""

    if args.content:
        if args.content == "-":
            body = sys.stdin.read()
        else:
            body = args.content
        template = header + body + "\n"
    else:
        template = header + """## Overview

## Details

## Next Steps

## Related

"""

    file_path.write_text(template)

    if not args.quiet:
        print(f"Created {file_path}")

    if args.edit:
        editor = os.environ.get("EDITOR", "nano")
        os.execlp(editor, editor, str(file_path))


def cmd_init(args):
    entries_dir = Path.cwd() / "entries"
    entries_dir.mkdir(exist_ok=True)
    if not args.quiet:
        print(f"Created {entries_dir}")


def cmd_install_skill(args):
    skill_source = Path(__file__).parent / "data" / "SKILL.md"
    if not skill_source.exists():
        print("Error: SKILL.md not found in package data", file=sys.stderr)
        sys.exit(1)

    target_dir = args.skill_dir / "entry"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "SKILL.md"

    shutil.copy2(skill_source, target)
    if not args.quiet:
        print(f"Installed {target}")


def main():
    parser = argparse.ArgumentParser(
        prog="entry",
        description="Create chronologically organized documentation entries",
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")

    sub = parser.add_subparsers(dest="command", required=True)

    # create
    create_p = sub.add_parser("create", help="Create a new entry")
    create_p.add_argument("filename", help="Entry filename (without .md)")
    create_p.add_argument("title", nargs="?", help="Entry title (default: auto from filename)")
    create_p.add_argument("--content", "-c", help="Entry body content (use '-' for stdin)")
    create_p.add_argument("--edit", "-e", action="store_true", help="Open in $EDITOR after creation")

    # init
    sub.add_parser("init", help="Create entries/ directory")

    # install-skill
    skill_p = sub.add_parser("install-skill", help="Install Claude Code skill to .claude/skills/entry/")
    skill_p.add_argument("--skill-dir", type=Path, default=Path(".claude/skills"),
                         help="Target skills directory (default: .claude/skills)")

    args = parser.parse_args()

    commands = {
        "create": cmd_create,
        "init": cmd_init,
        "install-skill": cmd_install_skill,
    }

    commands[args.command](args)
