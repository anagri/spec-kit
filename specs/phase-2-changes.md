# Phase 2: Remove Branch Creation & Decouple from Git

**Date**: 2025-10-04
**Phase**: 2 - Remove Branch Creation, Decouple Feature ID from Git Branch
**Status**: ✅ Completed

## Overview

This phase removes automatic git branch creation and decouples the feature identifier from git branches, enabling a solo developer workflow where all work happens on the main branch. The `###-feature-name` pattern is retained as a directory naming convention, not a branch requirement.

## Problem Statement

**Before (Branch-Coupled)**:
- Feature identifier = Git branch name = Directory name (e.g., `001-create-taskify`)
- `/specify` automatically creates git branch AND feature directory
- All commands find features via git branch name → `specs/{branch}/`
- Assumes PR-based workflow (branch → merge to main)

**User Need (Branch-Free)**:
- Solo developer, commits directly to main
- Still needs feature organization (`specs/001-*/`, `specs/002-*/`)
- Still needs `###-feature-name` pattern
- NO automatic branch creation

**Solution**: Decouple feature identifier from git branches - it's just a directory naming scheme!

## Changes Made

### Phase 2A: Rename Variables (Internal Refactoring)

**Purpose**: Make variable names semantically correct (feature ID ≠ branch name)

#### scripts/bash/common.sh
- `get_current_branch()` → `get_current_feature()`
- `CURRENT_BRANCH` → `CURRENT_FEATURE`
- `check_feature_branch()` → `check_feature_id()`
- Updated `get_feature_paths()` to use `CURRENT_FEATURE`

#### scripts/bash/create-new-feature.sh
- `BRANCH_NAME` → `FEATURE_ID` (everywhere)
- JSON output: `{"FEATURE_ID":"..."}` instead of `{"BRANCH_NAME":"..."}`

#### scripts/bash/setup-plan.sh
- Uses `CURRENT_FEATURE` instead of `CURRENT_BRANCH`
- Calls `check_feature_id()` instead of `check_feature_branch()`
- JSON output: `{"FEATURE_ID":"..."}` instead of `{"BRANCH":"..."}`

#### scripts/bash/check-prerequisites.sh
- Uses `CURRENT_FEATURE` instead of `CURRENT_BRANCH`
- Calls `check_feature_id()` instead of `check_feature_branch()`
- JSON output: `{"FEATURE_ID":"..."}` instead of `{"BRANCH":"..."}`

#### scripts/bash/update-agent-context.sh
- All 7 occurrences of `CURRENT_BRANCH` → `CURRENT_FEATURE`
- Feature annotations now use feature ID instead of branch name

### Phase 2B: Remove Branch Logic

**Purpose**: Remove git branch creation and detection

#### scripts/bash/create-new-feature.sh
**Removed** (lines 74-78):
```bash
if [ "$HAS_GIT" = true ]; then
    git checkout -b "$FEATURE_ID"
else
    >&2 echo "[specify] Warning: Git repository not detected; skipped branch creation for $FEATURE_ID"
fi
```

**Replaced with**:
```bash
# Feature directory (no branch creation - solo dev workflow)
```

#### scripts/bash/common.sh
**get_current_feature() simplified** - removed git branch detection:

**Before**:
```bash
# First check SPECIFY_FEATURE env var
# Then check git branch name ← REMOVED
# Then find latest feature directory
# Final fallback: "main"
```

**After**:
```bash
# First check SPECIFY_FEATURE env var
# Find latest feature directory (no git dependency)
# Final fallback: "main"
```

**check_feature_id() simplified** - warning only, not blocking:

**Before**:
```bash
if [[ ! "$feature_id" =~ ^[0-9]{3}- ]]; then
    echo "ERROR: Not on a feature branch..." >&2
    return 1  # Blocking error
fi
```

**After**:
```bash
if [[ ! "$feature_id" =~ ^[0-9]{3}- ]]; then
    echo "[specify] Warning: Feature ID doesn't follow convention..." >&2
    # Non-blocking warning
fi
return 0  # Always succeeds
```

### Phase 2C: Update Templates

**Purpose**: Remove "branch" terminology, use "feature" terminology

#### templates/commands/specify.md
```diff
-1. Run the script `{SCRIPT}` from repo root and parse its JSON output for BRANCH_NAME and SPEC_FILE.
+1. Run the script `{SCRIPT}` from repo root and parse its JSON output for FEATURE_ID and SPEC_FILE.

-4. Report completion with branch name, spec file path, and readiness for the next phase.
+4. Report completion with feature ID, spec file path, and readiness for the next phase.

-Note: The script creates and checks out the new branch and initializes the spec file before writing.
+Note: The script creates the feature directory and initializes the spec file before writing.
```

#### templates/commands/plan.md
```diff
-1. Run `{SCRIPT}` from the repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH.
+1. Run `{SCRIPT}` from the repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, FEATURE_ID.

-6. Report results with branch name, file paths, and generated artifacts.
+6. Report results with feature ID, file paths, and generated artifacts.
```

#### templates/commands/clarify.md
```diff
-   - If JSON parsing fails, abort and instruct user to re-run `/specify` or verify feature branch environment.
+   - If JSON parsing fails, abort and instruct user to re-run `/specify` or verify feature environment.
```

#### templates/spec-template.md
```diff
-**Feature Branch**: `[###-feature-name]`
+**Feature ID**: `[###-feature-name]`
```

#### templates/plan-template.md
```diff
-**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
+**Feature**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
```

## Git Diff Statistics

```
 scripts/bash/check-prerequisites.sh  | 10 +++----
 scripts/bash/common.sh               | 56 ++++++++++++++----------------------
 scripts/bash/create-new-feature.sh   | 23 ++++++---------
 scripts/bash/setup-plan.sh           | 12 ++++----
 scripts/bash/update-agent-context.sh | 14 ++++-----
 templates/commands/clarify.md        |  2 +-
 templates/commands/plan.md           |  4 +--
 templates/commands/specify.md        |  6 ++--
 templates/plan-template.md           |  2 +-
 templates/spec-template.md           |  2 +-
 10 files changed, 57 insertions(+), 74 deletions(-)
```

**Total reduction**: 17 lines across 10 files

## Testing Results

### Phase 2A Test (Variable Rename)
```bash
$ cd /tmp/test-phase-2a-local
$ bash .../create-new-feature.sh --json "test feature"
{"FEATURE_ID":"001-test-feature","SPEC_FILE":"...","FEATURE_NUM":"001"}
Switched to a new branch '001-test-feature'  # Still creates branch (Phase 2A only)

$ bash .../setup-plan.sh --json
{"FEATURE_SPEC":"...","IMPL_PLAN":"...","SPECS_DIR":"...","FEATURE_ID":"001-test-feature","HAS_GIT":"true"}
✅ JSON outputs use FEATURE_ID instead of BRANCH/BRANCH_NAME

$ bash .../check-prerequisites.sh --json --paths-only
{"REPO_ROOT":"...","FEATURE_ID":"001-test-feature",...}
✅ All scripts work with renamed variables
```

### Phase 2B Test (Branch Removal)
```bash
$ cd /tmp/test-phase-2b
$ git branch  # Empty - no branches yet

$ bash .../create-new-feature.sh --json "test feature"
{"FEATURE_ID":"001-test-feature","SPEC_FILE":"...","FEATURE_NUM":"001"}
# No branch creation message!

$ git branch  # Still empty - no branch created
✅ No branch created

$ ls -la specs/
drwxr-xr-x  3 amir36  wheel   96 Oct  4 21:45 001-test-feature
✅ Feature directory created

$ bash .../setup-plan.sh --json
{"FEATURE_SPEC":"...","IMPL_PLAN":"...","SPECS_DIR":"...","FEATURE_ID":"001-test-feature","HAS_GIT":"true"}
✅ Feature detected without git branch (uses latest directory)
```

### Phase 2C Test (Template Updates)
Templates successfully updated to use FEATURE_ID and remove branch terminology.
All commands will instruct Claude to parse FEATURE_ID from JSON instead of BRANCH_NAME.

## New Workflow (Solo Developer)

### Before (Branch-Based)
```bash
/specify "create chat system"
→ Creates branch: 003-create-chat-system
→ Creates directory: specs/003-create-chat-system/
→ User must: git checkout main, git merge 003-create-chat-system (later)

/plan
→ Finds feature via: git branch name
```

### After (Branch-Free)
```bash
/specify "create chat system"
→ NO branch created
→ Creates directory: specs/003-create-chat-system/
→ User works on: main branch (or any branch they choose)

/plan
→ Finds feature via: latest directory in specs/
```

## Feature Detection Logic

### Before (Git-Dependent)
1. Check SPECIFY_FEATURE env var
2. Check git branch name ← **Removed**
3. Find latest feature directory
4. Fallback: "main"

### After (Git-Independent)
1. Check SPECIFY_FEATURE env var
2. Find latest feature directory
3. Fallback: "main"

**Key Insight**: Feature identifier is now completely independent of git state!

## Directory Structure (Unchanged)

```
specs/
├── 001-user-auth/           # Feature ID = directory name
│   ├── spec.md
│   ├── plan.md
│   └── tasks.md
├── 002-dashboard/
└── 003-create-chat-system/  # ← New feature (no branch needed)
    ├── spec.md
    ├── plan.md
    └── tasks.md
```

## Benefits for Solo Developers

✅ **No forced branching**: Work on main directly
✅ **Simpler workflow**: No branch management overhead
✅ **Same organization**: Features still organized by numbered directories
✅ **Less git noise**: No feature branches cluttering history
✅ **Flexible**: Can still create branches manually if desired

## Breaking Changes

**JSON API Changes**:
- `BRANCH_NAME` → `FEATURE_ID` (create-new-feature.sh)
- `BRANCH` → `FEATURE_ID` (setup-plan.sh, check-prerequisites.sh)
- `CURRENT_BRANCH` → `CURRENT_FEATURE` (internal only)

**Template Changes**:
- Commands now reference FEATURE_ID instead of BRANCH_NAME/BRANCH
- Help text updated to reflect branch-free workflow

**Behavioral Changes**:
- `/specify` no longer creates git branches
- Feature detection no longer uses git branch name
- check_feature_id() warns instead of errors

## Files Modified (10 files)

**Scripts (5)**:
1. `scripts/bash/common.sh` - Decoupled from git, renamed functions
2. `scripts/bash/create-new-feature.sh` - Removed branch creation
3. `scripts/bash/setup-plan.sh` - Use FEATURE_ID
4. `scripts/bash/check-prerequisites.sh` - Use FEATURE_ID
5. `scripts/bash/update-agent-context.sh` - Use CURRENT_FEATURE

**Templates (5)**:
6. `templates/commands/specify.md` - Parse FEATURE_ID, remove branch language
7. `templates/commands/plan.md` - Parse FEATURE_ID
8. `templates/commands/clarify.md` - Update error messages
9. `templates/spec-template.md` - "Feature ID" not "Feature Branch"
10. `templates/plan-template.md` - "Feature" not "Branch"

## Phase 2 Complete

**Phases Completed**:
- ✅ **2A**: Renamed variables for semantic clarity
- ✅ **2B**: Removed git branch creation and detection
- ✅ **2C**: Updated templates to use feature terminology

**Result**: Spec Kit now supports solo developer workflow with no forced branching, while maintaining the numbered feature directory organization pattern.

**Total Line Reduction**: -17 lines (simplified code, removed branching logic)

The system is now git-branch independent while preserving all feature organization capabilities!
