# Plan: Simplify Spec-Kit for Claude Code on macOS Only

## Overview
Strip out multi-agent support, Windows compatibility, and branch creation to create a streamlined Claude Code-only version for macOS.

## Core Changes

### 1. Python CLI Simplification (`src/specify_cli/__init__.py`)
- **Remove multi-agent support**: Delete AI_CHOICES for all agents except Claude
- **Remove script type selection**: Hardcode to bash ('sh'), remove PowerShell option
- **Simplify init command**: Remove AI/script selection prompts, default to Claude + bash
- **Remove agent tool checks**: Keep only Claude CLI check, remove checks for Gemini, Cursor, Qwen, opencode, Codex, Windsurf, Amazon Q, etc.
- **Simplify check command**: Only check for git and Claude Code CLI
- **Remove Windows logic**: Strip all Windows-specific code paths (`os.name == "nt"` checks)
- **Clean up UI**: Remove unnecessary selection panels and options

### 2. Remove Branch Creation Logic
- **`scripts/bash/create-new-feature.sh`**: Remove git branch creation (lines 74-78), keep feature directory creation
- **`scripts/bash/common.sh`**: Simplify `check_feature_branch()` to not enforce branch naming
- **`templates/commands/specify.md`**: Update instructions to reflect no branch creation

### 3. Delete Windows Support Files
- **Remove entire directory**: `scripts/powershell/` (all .ps1 files)
- **Update templates**: Remove PowerShell script references from command templates

### 4. Simplify Scripts
- **`scripts/bash/update-agent-context.sh`**: Remove support for all agents except Claude
- **`scripts/bash/common.sh`**: Simplify to remove multi-agent and branch validation logic
- **Keep**: `check-prerequisites.sh`, `setup-plan.sh` (with updates)

### 5. Update Documentation
- **README.md**: Remove supported agents table, Windows instructions, multi-agent examples
- **CLAUDE.md/AGENTS.md**: Remove agent integration guide, focus on Claude-only usage
- **Remove references to**: Script type selection, agent selection, branch creation workflow

### 6. Simplify Build/Release (Optional)
- **`.github/workflows/scripts/create-release-packages.sh`**: Simplify to only build `claude-sh` packages
- **`.github/workflows/scripts/create-github-release.sh`**: Update to only release Claude packages
- **Or remove entirely** if not needed for your fork

### 7. Update Project Metadata
- **`pyproject.toml`**: Update description to reflect Claude-only, macOS-only focus
- **Version bump**: Increment version to mark this as a custom fork

## Files to Delete
- `scripts/powershell/` (entire directory)
- References to other agents in templates and docs

## Files to Modify
- `src/specify_cli/__init__.py` (major simplification)
- `scripts/bash/create-new-feature.sh` (remove branch creation)
- `scripts/bash/common.sh` (simplify)
- `scripts/bash/update-agent-context.sh` (Claude-only)
- `templates/commands/specify.md` (update instructions)
- `README.md` (major updates)
- `CLAUDE.md` (simplify)
- `pyproject.toml` (metadata update)

## Result
A streamlined spec-kit that:
✅ Only supports Claude Code
✅ Only supports macOS (bash scripts)
✅ No branch creation on `/specify`
✅ Works with `uvx --from git+https://github.com/anagri/spec-kit.git specify init <PROJECT_NAME>`
✅ Much simpler codebase, easier to maintain and customize

## Implementation Phases

### Phase 1: Python CLI Simplification
- Modify `src/specify_cli/__init__.py`
- Remove multi-agent support
- Hardcode to Claude + bash
- Remove Windows-specific code
- Test: `uvx --from . specify init test-project`

### Phase 2: Remove Branch Creation
- Modify `scripts/bash/create-new-feature.sh`
- Modify `scripts/bash/common.sh`
- Update `templates/commands/specify.md`
- Test: Run `/specify` command

### Phase 3: Delete Windows Support
- Delete `scripts/powershell/` directory
- Update command templates
- Test: Verify no broken references

### Phase 4: Update Documentation
- Update `README.md`
- Update `CLAUDE.md`
- Update `pyproject.toml`
- Test: Review documentation accuracy

### Phase 5: Clean Up Build/Release (Optional)
- Simplify GitHub workflows
- Or remove if not needed

---

## Baseline Test Results ✅

**Date**: 2025-10-04
**Test Location**: `/Users/amir36/Documents/workspace/src/github.com/anagri/baseline-project`

### Test Command
```bash
cd baseline-project
uvx --from /Users/amir36/Documents/workspace/src/github.com/anagri/spec-kit specify init . --ai claude --script sh --force
```

### Results
✅ **SUCCESS** - All components installed correctly:
- `.claude/commands/` - 7 slash commands (analyze, clarify, constitution, implement, plan, specify, tasks)
- `.specify/scripts/bash/` - 5 executable bash scripts
- `.specify/memory/` - Memory directory created
- `.specify/templates/` - Template directory created
- All scripts have correct executable permissions

### Test Strategy for Each Phase
After each phase, run:
```bash
# Clean up previous test
rm -rf /Users/amir36/Documents/workspace/src/github.com/anagri/test-phase-N

# Create fresh test directory
mkdir -p /Users/amir36/Documents/workspace/src/github.com/anagri/test-phase-N
cd /Users/amir36/Documents/workspace/src/github.com/anagri/test-phase-N
git init

# Test installation
uvx --from /Users/amir36/Documents/workspace/src/github.com/anagri/spec-kit specify init . --force
```

---

## Phase 1A: Hardcode Defaults - ✅ COMPLETED

**Date**: 2025-10-04

### Changes Made
- `src/specify_cli/__init__.py` line 876-877: Default to `"claude"` instead of interactive prompt
- `src/specify_cli/__init__.py` line 934-935: Default to `"sh"` instead of OS detection/prompt

### Code Changes
```python
# AI selection (line 876-877)
else:
    # Default to Claude Code
    selected_ai = "claude"

# Script type selection (line 934-935)
else:
    # Default to bash/sh
    selected_script = "sh"
```

### Testing Results
✅ **Test 1**: No flags - defaults to claude + sh
```bash
specify init test-phase-1a --ignore-agent-tools
# Result: SUCCESS - Selected AI: claude, Script: sh
```

✅ **Test 2**: Explicit flags still work
```bash
specify init test-phase-1b --ai claude --script sh --ignore-agent-tools
# Result: SUCCESS - Flags respected
```

### Important Note
- For testing, use: `uv pip install -e .` to install in editable mode
- Then use `specify` command directly (picks up live changes)
- `uvx` caches packages, so not ideal for iterative development

### What Still Works
- ✅ `--ai` flag still functional (can override default)
- ✅ `--script` flag still functional (can override default)
- ✅ All other agents still work if explicitly specified
- ✅ No breaking changes, just removed interactive prompts

---

## Phase 1B: Remove Unused Options - NEXT
