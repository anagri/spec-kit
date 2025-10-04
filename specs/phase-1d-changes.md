# Phase 1D: Remove PowerShell Support - Orphaned Files

**Date**: 2025-10-04
**Phase**: 1D - Remove Orphaned PowerShell Scripts and Template References
**Status**: ✅ Completed

## Overview

This phase removes all PowerShell-related files and references that became orphaned after hardcoding script type to "sh" in Phase 1C. This includes:
1. The entire `scripts/powershell/` directory (5 script files)
2. PowerShell script references from 7 template files' YAML frontmatter

## Changes Made

### 1. Deleted Files

Removed the entire PowerShell scripts directory:

```
scripts/powershell/
├── check-prerequisites.ps1      (148 lines)
├── common.ps1                   (136 lines)
├── create-new-feature.ps1       (117 lines)
├── setup-plan.ps1               (61 lines)
└── update-agent-context.ps1     (433 lines)
```

**Total deleted**: 5 files, 895 lines of PowerShell code

### 2. Updated Template Files

Removed `ps:` line from YAML frontmatter in 7 template files:

#### templates/commands/specify.md
```diff
 ---
 description: Create or update the feature specification from a natural language feature description.
 scripts:
   sh: scripts/bash/create-new-feature.sh --json "{ARGS}"
-  ps: scripts/powershell/create-new-feature.ps1 -Json "{ARGS}"
 ---
```

#### templates/commands/plan.md
```diff
 ---
 description: Execute the implementation planning workflow using the plan template to generate design artifacts.
 scripts:
   sh: scripts/bash/setup-plan.sh --json
-  ps: scripts/powershell/setup-plan.ps1 -Json
 ---
```

#### templates/commands/clarify.md
```diff
 ---
 description: Identify underspecified areas in the current feature spec...
 scripts:
    sh: scripts/bash/check-prerequisites.sh --json --paths-only
-   ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
 ---
```

#### templates/commands/tasks.md
```diff
 ---
 description: Generate an actionable, dependency-ordered tasks.md...
 scripts:
   sh: scripts/bash/check-prerequisites.sh --json
-  ps: scripts/powershell/check-prerequisites.ps1 -Json
 ---
```

#### templates/commands/analyze.md
```diff
 ---
 description: Perform a non-destructive cross-artifact consistency and quality analysis...
 scripts:
   sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
-  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
 ---
```

#### templates/commands/implement.md
```diff
 ---
 description: Execute the implementation plan by processing and executing all tasks...
 scripts:
   sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
-  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
 ---
```

#### templates/plan-template.md
```diff
 ---
 description: "Implementation plan template for feature development"
 scripts:
   sh: scripts/bash/update-agent-context.sh __AGENT__
-  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
 ---
```

## Git Diff Statistics

```
 scripts/powershell/check-prerequisites.ps1  | 148 ----------
 scripts/powershell/common.ps1               | 136 ---------
 scripts/powershell/create-new-feature.ps1   | 117 --------
 scripts/powershell/setup-plan.ps1           |  61 ----
 scripts/powershell/update-agent-context.ps1 | 433 ----------------------------
 templates/commands/analyze.md               |   1 -
 templates/commands/clarify.md               |   1 -
 templates/commands/implement.md             |   1 -
 templates/commands/plan.md                  |   1 -
 templates/commands/specify.md               |   1 -
 templates/commands/tasks.md                 |   1 -
 templates/plan-template.md                  |   1 -
 12 files changed, 902 deletions(-)
```

**Total reduction**: 902 lines removed across 12 files

## Testing Results

### Test Execution
```bash
# Create test project
specify init test-phase-1d --ignore-agent-tools

# Test output
Using Claude Code with bash scripts
Initialize Specify Project
├── ● Check required tools (ok)
├── ● AI assistant (claude)
├── ● Script type (sh)
├── ● Create project directory (ok)
├── ● Download and extract template (ok)
├── ● Setup specify workspace (ok)
├── ● Copy bash scripts to .specify/scripts (ok)
├── ● Generate Claude Code commands (ok)
└── ● Copy memory files to .specify/memory (ok)

✨ Project initialized with:
   AI Assistant: Claude Code
   Script Type: bash
```

### Verification: No PowerShell References

```bash
$ grep -r "powershell\|\.ps1" test-phase-1d/.claude/commands/
# No output - PowerShell references successfully removed
```

### Comparison with Baseline

```bash
$ diff -r baseline-project test-phase-1d
Only in baseline-project: .git

# Output is identical - no functional changes
```

## Impact Analysis

### What Changed
- **Deleted**: 5 PowerShell script files (895 lines)
- **Updated**: 7 template files to remove `ps:` references (7 lines)
- **Total reduction**: 902 lines

### What Stayed the Same
- All generated project files remain identical to baseline
- No PowerShell references in generated `.claude/commands/` files
- All functionality preserved for bash/Claude Code users

### User Impact
- **Claude + macOS users**: No impact - identical output
- **Windows users**: No longer supported (intentional)
- **Other platforms**: No longer supported (intentional)

## Rationale

These files and references became orphaned in Phase 1C when we hardcoded `SCRIPT_TYPE = "sh"`. The PowerShell scripts were:
1. Never copied to projects anymore (copy logic removed in Phase 1C)
2. Never referenced in generated commands (ps: frontmatter never processed)
3. Impossible to select (--script parameter removed)

Removing them:
- Reduces codebase size by 902 lines
- Eliminates maintenance burden for unused code
- Makes the codebase clearer (no confusing dual-platform code)
- Aligns with the goal of Claude + macOS only

## Files Modified

```
scripts/powershell/                      [DELETED]
templates/commands/analyze.md            [-1 line]
templates/commands/clarify.md            [-1 line]
templates/commands/implement.md          [-1 line]
templates/commands/plan.md               [-1 line]
templates/commands/specify.md            [-1 line]
templates/commands/tasks.md              [-1 line]
templates/plan-template.md               [-1 line]
```

## Next Steps

**Optional Build Script Updates**:
- `.github/workflows/scripts/create-release-packages.sh` - Simplify to Claude+sh only
- `.github/workflows/scripts/create-github-release.sh` - Simplify to Claude+sh only

**Phase 2 Candidates**:
- Remove branch creation logic from /specify command
- Remove other agent support from build scripts
- Update README to reflect Claude-only focus

## Phase 1D Complete

✅ All Phase 1 objectives completed:
- **1A**: Hardcoded defaults (Claude + bash)
- **1B**: Removed multi-agent support
- **1C**: Removed PowerShell platform support
- **1D**: Removed orphaned files and references

**Total Phase 1 reduction**: ~1,024 lines of code removed, 5 files deleted

The codebase is now significantly simpler while maintaining identical functionality for Claude Code + macOS users.
