---
name: entry
description: Create chronologically organized documentation entries
argument-hint: "[create|init|install-skill] [args...]"
allowed-tools: Bash(entry *), Bash(./entry *), Bash(uvx *entry*), Read, Write
---

You are creating documentation entries using the `entry` CLI tool. Entries are organized as `entries/YYYY/MM/DD/<filename>.md`.

## Why Use This Tool

**Do not create entry files directly with Write or Bash.** Use this CLI instead.

LLMs have no internal sense of temporal ordering. You cannot distinguish between a claim made in January 2025 and one made in February 2026, or tell that a later entry supersedes an earlier one. This was a central finding from a year-long multi-agent research program: without externally imposed time structure, CLAUDE.md files went stale, agents operated on outdated beliefs, and contradictions accumulated undetected.

The `entries/YYYY/MM/DD/` directory structure solves this — the filesystem encodes time that the model cannot track internally. Every entry gets a date from its path, creating an auditable trail of when ideas appeared, when problems were identified, and whether resolutions were genuine or cosmetic. This tool enforces that structure automatically so you don't have to construct it manually (and get it wrong).

It also prevents practical problems observed in the same program:

1. **Filenames with spaces.** Agents naturally generate filenames like `Meeting Notes.md` which break shell commands. This tool auto-slugifies titles to kebab-case (`meeting-notes.md`).
2. **Structural drift.** Without enforcement, agents invented extra nesting levels, embedded redundant timestamps in filenames (`250126_082445_TrMic.md`), and fragmented single entries across multiple files. 90+ malformed directories accumulated before the pattern was corrected. This tool enforces one flat file per entry with a consistent template.

## How to Run

Try these in order until one works:
1. `entry $ARGUMENTS` (if installed via uv/pip)
2. `./entry $ARGUMENTS` (if in the repo directory)
3. `uvx --from git+https://github.com/benthomasson/entry entry $ARGUMENTS` (fallback)

## Subcommand Behavior

### `create <filename> [title] [--content BODY] [--edit]`
Creates a new entry at `entries/YYYY/MM/DD/<filename>.md` with a standard template. If no title is given, one is generated from the filename (kebab-case to Title Case).

Convert natural language to CLI arguments:
- `/entry meeting notes from auth discussion` → `entry create "Meeting Notes from Auth Discussion"`
- `/entry retrospective on Q4 deployment` → `entry create "Retrospective on Q4 Deployment"`
- `/entry quick note about caching bug` → `entry create "Caching Bug Note"`

When the filename contains spaces, it is treated as a title and the kebab-case filename is derived automatically. So `entry create "My Finding Title"` creates `my-finding-title.md` with title "My Finding Title".

#### Single-step creation with `--content-file` (preferred for AI agents)

Use `--content-file` / `-f` to create an entry from a file. The tool adds the header (title, date, time) automatically — the file should contain just the body:

```bash
# 1. Write body to a temp file (using the Write tool — no bash quoting issues)
# 2. Create the entry from that file
entry create "My Finding" --content-file /tmp/entry-body.md
```

**This is the preferred pattern for AI agents.** Content with `$`, `()`, backticks, and LaTeX math breaks bash heredocs and `--content` strings. Writing to a temp file via the Write tool avoids all quoting issues.

#### `--content` for simple inline content

For short content without special characters, `--content` / `-c` works inline:

```bash
entry create "My Finding" --content "## Overview

Found something interesting."
```

Use `-c -` to read from stdin:

```bash
echo "Piped content." | entry create "My Finding" -c -
```

Rules:
- **Use `--content-file` / `-f` when content has math, LaTeX, or special characters** — write a temp file with the Write tool first, then pass the path
- Use `--content` / `-c` only for short, simple content without `$`, `()`, or backticks
- Prefer passing a title with spaces — the tool slugifies it automatically
- Use `--edit` / `-e` only if the user says they want to edit it interactively

### `init`
Run `entry init` to create the `entries/` directory. Use this when setting up a new repository for entry tracking.

### `install-skill`
Run `entry install-skill` to install this skill file to `.claude/skills/entry/SKILL.md`. Use `--skill-dir` to override the target directory.

## After Any Command

- If the entry was created, confirm the path
- Keep responses concise — the tool output speaks for itself
