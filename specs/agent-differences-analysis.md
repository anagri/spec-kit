# Agent Differences Analysis

**Purpose**: Understand exactly what changes when different AI agents are selected

---

## Overview

When you select a different AI agent with `--ai <agent>`, the **ONLY** things that change are:

1. **Directory location** where commands are placed
2. **File format** of the commands (Markdown vs TOML)
3. **Argument placeholder syntax** used in commands

**Everything else remains identical**: scripts, templates, memory, core functionality.

---

## What's Different Per Agent

### Directory Structure by Agent

| Agent | Command Directory | File Extension | Argument Format |
|-------|------------------|----------------|-----------------|
| **claude** | `.claude/commands/` | `.md` | `$ARGUMENTS` |
| **gemini** | `.gemini/commands/` | `.toml` | `{{args}}` |
| **copilot** | `.github/prompts/` | `.prompt.md` | `$ARGUMENTS` |
| **cursor** | `.cursor/commands/` | `.md` | `$ARGUMENTS` |
| **qwen** | `.qwen/commands/` | `.toml` | `{{args}}` |
| **opencode** | `.opencode/command/` | `.md` | `$ARGUMENTS` |
| **windsurf** | `.windsurf/workflows/` | `.md` | `$ARGUMENTS` |
| **codex** | `.codex/prompts/` | `.md` | `$ARGUMENTS` |
| **kilocode** | `.kilocode/workflows/` | `.md` | `$ARGUMENTS` |
| **auggie** | `.augment/commands/` | `.md` | `$ARGUMENTS` |
| **roo** | `.roo/commands/` | `.md` | `$ARGUMENTS` |
| **q** | `.amazonq/prompts/` | `.md` | `$ARGUMENTS` |

### Format Categories

**Markdown Format Agents** (most common):
- claude, copilot, cursor, opencode, windsurf, codex, kilocode, auggie, roo, q
- Use `.md` files with YAML frontmatter
- Argument placeholder: `$ARGUMENTS`

**TOML Format Agents** (Gemini, Qwen only):
- gemini, qwen
- Use `.toml` files with separate prompt section
- Argument placeholder: `{{args}}`

---

## Example: Same Command, Different Formats

### Claude Format (.claude/commands/specify.md)
```markdown
---
description: Create or update the feature specification from a natural language feature description.
---

User input:

$ARGUMENTS

Given that feature description, do this:

1. Run the script `.specify/scripts/bash/create-new-feature.sh --json "$ARGUMENTS"` from repo root...
```

### Gemini Format (.gemini/commands/specify.toml)
```toml
description = "Create or update the feature specification from a natural language feature description."

prompt = """
User input:

{{args}}

Given that feature description, do this:

1. Run the script `.specify/scripts/bash/create-new-feature.sh --json "{{args}}"` from repo root...
"""
```

### Key Differences
1. **Structure**: Markdown uses YAML frontmatter, TOML uses separate fields
2. **Arguments**: `$ARGUMENTS` vs `{{args}}`
3. **Content**: Identical logic, just different packaging

---

## What's IDENTICAL Across All Agents

### 1. Core Scripts (`.specify/scripts/bash/` or `.specify/scripts/powershell/`)
**Exactly the same for all agents:**
- `check-prerequisites.sh`
- `common.sh`
- `create-new-feature.sh`
- `setup-plan.sh`
- `update-agent-context.sh`

These scripts are the "engine" - they don't care which agent calls them.

### 2. Templates (`.specify/templates/`)
**Exactly the same for all agents:**
- `spec-template.md`
- `plan-template.md`
- `tasks-template.md`

These define the structure of your specs, plans, and tasks.

### 3. Memory (`.specify/memory/`)
**Exactly the same for all agents:**
- `constitution.md`

Project principles and guidelines.

### 4. Command Logic
**The actual instructions in commands are identical**, just formatted differently:
- Same 7 commands: constitution, specify, clarify, plan, tasks, analyze, implement
- Same workflow steps
- Same script references
- Same functionality

---

## Script Analysis: How Commands Are Generated

### Source: `.github/workflows/scripts/create-release-packages.sh`

The `build_variant()` function (lines 86-181) shows the ONLY differences:

```bash
case $agent in
  claude)
    mkdir -p "$base_dir/.claude/commands"
    generate_commands claude md "\$ARGUMENTS" "$base_dir/.claude/commands" "$script" ;;
  gemini)
    mkdir -p "$base_dir/.gemini/commands"
    generate_commands gemini toml "{{args}}" "$base_dir/.gemini/commands" "$script" ;;
  copilot)
    mkdir -p "$base_dir/.github/prompts"
    generate_commands copilot prompt.md "\$ARGUMENTS" "$base_dir/.github/prompts" "$script" ;;
  # ... etc for each agent
esac
```

### The `generate_commands()` Function (lines 40-84)

Takes the **same source templates** (`templates/commands/*.md`) and:

1. **Extracts** description from YAML frontmatter
2. **Replaces** `{SCRIPT}` with appropriate script path
3. **Replaces** `{ARGS}` with agent-specific format (`$ARGUMENTS` or `{{args}}`)
4. **Replaces** `__AGENT__` with agent name
5. **Formats** output as `.md` or `.toml` based on agent

**Key insight**: The source is identical, only the output format changes.

---

## Path Rewriting

The `rewrite_paths()` function (lines 33-38) ensures paths are consistent:

```bash
rewrite_paths() {
  sed -E \
    -e 's@(/?)memory/@.specify/memory/@g' \
    -e 's@(/?)scripts/@.specify/scripts/@g' \
    -e 's@(/?)templates/@.specify/templates/@g'
}
```

All agents reference the same paths: `.specify/scripts/`, `.specify/memory/`, etc.

---

## Script Type Differences (sh vs ps)

When `--script sh` vs `--script ps` is selected:

### Bash (sh)
- Copies `scripts/bash/*` → `.specify/scripts/bash/`
- Commands reference: `.specify/scripts/bash/create-new-feature.sh`

### PowerShell (ps)
- Copies `scripts/powershell/*` → `.specify/scripts/powershell/`
- Commands reference: `.specify/scripts/powershell/create-new-feature.ps1`

**The logic in both script types is identical**, just different shell syntax.

---

## Real-World Comparison

### Baseline (Claude + sh)
```
baseline-project/
├── .claude/commands/        # 7 .md files
├── .specify/
│   ├── memory/
│   ├── scripts/bash/        # 5 .sh files
│   └── templates/
```

### If Gemini + sh was selected
```
project/
├── .gemini/commands/        # 7 .toml files (different format)
├── .specify/
│   ├── memory/              # IDENTICAL
│   ├── scripts/bash/        # IDENTICAL (same 5 .sh files)
│   └── templates/           # IDENTICAL
```

### If Claude + ps was selected
```
project/
├── .claude/commands/        # 7 .md files (same as baseline)
├── .specify/
│   ├── memory/              # IDENTICAL
│   ├── scripts/powershell/  # DIFFERENT (.ps1 instead of .sh)
│   └── templates/           # IDENTICAL
```

---

## Implications for Simplification

### What We Can Remove (for Claude-only)

1. **Agent-specific code** (lines 139-178 in create-release-packages.sh):
   - Remove all cases except `claude)`
   - Hardcode directory to `.claude/commands/`
   - Hardcode format to `md`
   - Hardcode args to `$ARGUMENTS`

2. **Script type code** (lines 101-113):
   - Remove `ps)` case
   - Only copy `scripts/bash/`

3. **Validation code**:
   - Remove AI_CHOICES for all except claude
   - Remove SCRIPT_TYPE_CHOICES for all except sh

### What Stays the Same

✅ **All template content** - no changes needed
✅ **All scripts** - bash scripts work as-is
✅ **All memory** - constitution unchanged
✅ **Core logic** - generate_commands() simplified but same function

---

## Conclusion

**The agent selection is purely a packaging choice:**
- Same content
- Same functionality
- Same workflow
- Different wrapper

For a Claude-only, macOS-only version:
- Remove 11 agent cases, keep 1 (claude)
- Remove 1 script type, keep 1 (sh)
- **Result**: 90% code reduction with zero functional loss

The generated output is identical in function, just lives in a different directory with a different file extension.
