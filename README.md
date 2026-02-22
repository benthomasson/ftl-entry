# entry

CLI tool for creating chronologically organized documentation entries.

## The Problem: LLMs Have No Sense of Time

Large language models have no internal sense of temporal ordering. They cannot distinguish between a claim made in January 2025 and one made in February 2026. They cannot tell that a later entry supersedes an earlier one, or that a problem listed as "open" was resolved three weeks later. Every piece of text in the context window is treated as equally current.

This was a central finding from a year-long multi-agent AI research program where six agents worked across six repositories. Without externally imposed time structure:

- **Role definitions went stale.** CLAUDE.md files contained outdated claims. Agents operated on beliefs that had been superseded by newer findings. Every single role definition file had staleness issues when audited.
- **Contradictions accumulated undetected.** One file said a result was "resolved" while another classified it as "falsified." No agent noticed because both documents appeared equally current.
- **Agents invented inconsistent structures.** Without a tool enforcing the entry format, agents created 90+ directories with extra timestamp nesting, embedded redundant timestamps in filenames, and fragmented single entries across multiple files.

The same problem appears in automated pipelines. In a fully automated SDLC loop (no human in the loop), a hallucination in the planning stage cascaded through implementation, review, testing, and user acceptance — with each agent building on the previous one's flawed output. The tester found a real bug, the user agent confirmed it, then declared "SATISFIED" anyway. Without temporal structure, there was no mechanism to flag that the verdict contradicted the test results.

## The Solution: Filesystem-Encoded Time

The `entries/YYYY/MM/DD/` directory structure encodes time that the model cannot track internally:

```
entries/
  2026/
    02/
      20/
        api-redesign.md
        auth-migration.md
      21/
        belief-reconciliation.md
      22/
        cascading-failure-analysis.md
```

Every entry gets a date from its path. This creates an auditable trail of when ideas appeared, when problems were identified, and whether resolutions were genuine or cosmetic. The directory structure is the temporal memory that LLMs lack.

This tool enforces that structure mechanically — correct directory nesting, consistent templates, clean kebab-case filenames — so agents don't have to construct it manually and get it wrong.

## Install

```bash
# One-shot
uvx --from git+https://github.com/benthomasson/entry entry create my-note

# Permanent
uv tool install git+https://github.com/benthomasson/entry

# Development
git clone https://github.com/benthomasson/entry
cd entry
uv tool install -e .

# pip
pip install git+https://github.com/benthomasson/entry
```

## Usage

```bash
# Create an entry from a title (auto-slugifies to kebab-case filename)
entry create "My Finding Title"
# Creates: entries/2026/02/22/my-finding-title.md

# Explicit filename
entry create my-finding "My Finding Title"

# Auto-title from filename (becomes "My Finding")
entry create my-finding

# Create and open in editor
entry create "My Finding Title" --edit

# Quiet mode (no output, for scripting)
entry -q create "My Finding Title"

# Initialize entries/ directory
entry init

# Install Claude Code skill
entry install-skill
```

When the first argument contains spaces, it is treated as a title and the filename is derived automatically. This prevents agents from creating files with literal spaces in the name.

## Entry Template

Created entries follow this template:

```markdown
# {Title}

**Date:** YYYY-MM-DD
**Time:** HH:MM

## Overview

## Details

## Next Steps

## Related
```

Entries are placed in `entries/YYYY/MM/DD/<filename>.md`.

## Claude Code Skill

Install the bundled skill so agents can use `/entry` as a slash command:

```bash
entry install-skill
```

This copies the skill to `.claude/skills/entry/SKILL.md`. The skill teaches agents why the tool exists (temporal memory), how to convert natural language to CLI arguments, and that they should not create entry files directly with Write or Bash.

## Migration from `new_entry`

If you have a `new_entry` script in your repo, replace it:

```bash
# Install entry globally
uv tool install git+https://github.com/benthomasson/entry

# Remove the old script
rm new_entry

# Same behavior
entry create my-note "My Note"
```

## Background

This tool emerged from meta-research on multi-agent AI workflows. The entry system was one of several mechanisms developed to impose structure that LLMs cannot maintain internally. Related tools:

- [beliefs](https://github.com/benthomasson/beliefs) — Tracks claims and contradictions across repositories. Entries capture *what happened when* (temporal record); beliefs capture *what is currently believed and why* (structured state).
