# Tasks: Prioritize .specify Folder for Repository Root Detection

**Feature**: 002-git-folder-priority | **Date**: 2025-10-06
**Input**: Design documents from `/specs/002-git-folder-priority/`
**Prerequisites**: research.md, template-contracts.md, contracts/, quickstart.md

## Execution Flow (main)
```
1. Load design documents from feature directory
   → Tech stack: Bash (POSIX-compatible shell scripting)
   → Structure: CLI/Template/Generator tool (bash scripts)
2. Load contracts:
   → contracts/get_repo_root.md: common.sh function
   → contracts/find_repo_root.md: create-new-feature.sh function
3. Generate tasks by category:
   → Implementation: Modify 2 bash functions
   → Manual Validation: Verify 5 scenarios + 4 edge cases
   → Documentation: Verify quickstart.md examples
4. Apply task rules:
   → Different files = [P] for parallel
   → Same file = sequential (no [P])
   → Manual verification tasks = [P] (independent observations)
5. Number tasks sequentially (T001-T008)
6. All tasks executable with file paths provided
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
This is a CLI/Template/Generator tool:
- **Scripts (SOURCE)**: `scripts/bash/*.sh` (edit for distribution)
- **Scripts (INSTALLED)**: `.specify/scripts/bash/*.sh` (frozen for dogfooding)
- **Docs**: `specs/002-git-folder-priority/*.md`
- **Contracts**: `specs/002-git-folder-priority/contracts/*.md`

**IMPORTANT**: Modify SOURCE scripts in `scripts/bash/`, NOT `.specify/scripts/bash/` (frozen snapshot).

## Testing Note

**This project does not have automated test setup**. Test files mentioned in contracts are **specification only**.

**Implementation approach**:
- Skip creating test files (won't execute)
- Use contract test cases as **manual validation checklist**
- Verify behavior through direct script execution
- Testing instructions are for **specification purposes** (what SHOULD be tested)

---

## Phase 3.1: Core Implementation

### [X] T001: Modify get_repo_root() in common.sh for .specify priority
**File**: `scripts/bash/common.sh`
**Contract**: `specs/002-git-folder-priority/contracts/get_repo_root.md`
**Current** (lines 5-13):
```bash
get_repo_root() {
    if git rev-parse --show-toplevel >/dev/null 2>&1; then
        git rev-parse --show-toplevel  # Git first
    else
        local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        (cd "$script_dir/../../.." && pwd)  # Fallback
    fi
}
```

**New implementation**:
```bash
get_repo_root() {
    local dir="$(pwd)"

    # Traverse upward with .specify priority
    while [ "$dir" != "/" ]; do
        # FIRST: Check for .specify
        if [ -d "$dir/.specify" ]; then
            echo "$dir"
            return 0
        fi
        # SECOND: Check for .git
        if [ -d "$dir/.git" ]; then
            echo "$dir"
            return 0
        fi
        # Move up if neither found
        dir="$(dirname "$dir")"
    done

    # Final fallback if no markers found
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    (cd "$script_dir/../../.." && pwd)
}
```

**Validation**:
- Replace existing function at lines 5-13
- Preserve `set -e` and other common.sh content
- Test manually: `source scripts/bash/common.sh && get_repo_root`

---

### [X] T002: Modify find_repo_root() in create-new-feature.sh for .specify priority
**File**: `scripts/bash/create-new-feature.sh`
**Contract**: `specs/002-git-folder-priority/contracts/find_repo_root.md`
**Current** (lines 22-32):
```bash
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -d "$dir/.specify" ]; then  # OR logic
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}
```

**New implementation**:
```bash
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        # FIRST: Check for .specify
        if [ -d "$dir/.specify" ]; then
            echo "$dir"
            return 0
        fi
        # SECOND: Check for .git
        if [ -d "$dir/.git" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}
```

**Validation**:
- Replace existing function at lines 22-32
- Change lines 39-49 to use `find_repo_root` first (see contract for integration notes)
- Test manually: `scripts/bash/create-new-feature.sh --json "test feature"`

---

### [X] T003: Update create-new-feature.sh main logic to use find_repo_root first
**File**: `scripts/bash/create-new-feature.sh`
**Contract**: `specs/002-git-folder-priority/contracts/find_repo_root.md` (Integration section)
**Current** (lines 39-49):
```bash
if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
    if [ -z "$REPO_ROOT" ]; then
        echo "Error: Could not determine repository root..." >&2
        exit 1
    fi
    HAS_GIT=false
fi
```

**New implementation**:
```bash
# Try find_repo_root first (supports .specify priority)
REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
if [ $? -ne 0 ] || [ -z "$REPO_ROOT" ]; then
    echo "Error: Could not determine repository root. Please run this script from within the repository." >&2
    exit 1
fi

# Determine if we have git (separate check)
if git rev-parse --show-toplevel >/dev/null 2>&1; then
    HAS_GIT=true
else
    HAS_GIT=false
fi
```

**Validation**:
- Replace lines 39-49
- Test manually in monorepo scenario

---

## Phase 3.2: Manual Validation (Acceptance Scenarios)

**Note**: These are manual verification tasks. No automated tests exist. Use contract test cases as checklists.

### T004 [P] Manual Validation: Monorepo scenario (Acceptance Scenario 1)
**Reference**: `specs/002-git-folder-priority/spec.md` lines 54-56
**Contract Test Case**: `specs/002-git-folder-priority/contracts/get_repo_root.md` Test Case 1

**Setup**:
```bash
# Create test monorepo structure
mkdir -p /tmp/test-monorepo/project-a/src
mkdir -p /tmp/test-monorepo/.git
mkdir -p /tmp/test-monorepo/project-a/.specify
```

**Execution**:
```bash
cd /tmp/test-monorepo/project-a/src
source /path/to/spec-kit/scripts/bash/common.sh
result=$(get_repo_root)
echo "Result: $result"
```

**Expected**: `/tmp/test-monorepo/project-a`
**Criteria**: ✅ Finds `.specify` at project-a/ before parent `.git`

**Cleanup**:
```bash
rm -rf /tmp/test-monorepo
```

---

### T005 [P] Manual Validation: Single-project backward compatibility (Acceptance Scenario 2)
**Reference**: `specs/002-git-folder-priority/spec.md` lines 58-60
**Contract Test Case**: `specs/002-git-folder-priority/contracts/get_repo_root.md` Test Case 3

**Setup**:
```bash
# Create traditional single project
mkdir -p /tmp/test-single/src
mkdir -p /tmp/test-single/.git
mkdir -p /tmp/test-single/.specify
```

**Execution**:
```bash
cd /tmp/test-single/src
source /path/to/spec-kit/scripts/bash/common.sh
result=$(get_repo_root)
echo "Result: $result"
```

**Expected**: `/tmp/test-single`
**Criteria**: ✅ Both markers at same level → returns that directory (backward compatible)

**Cleanup**:
```bash
rm -rf /tmp/test-single
```

---

### T006 [P] Manual Validation: No-git repository (Acceptance Scenario 3)
**Reference**: `specs/002-git-folder-priority/spec.md` lines 62-64
**Contract Test Case**: `specs/002-git-folder-priority/contracts/get_repo_root.md` Test Case 7

**Setup**:
```bash
# Create no-git repo (--no-git init)
mkdir -p /tmp/test-nogit/src
mkdir -p /tmp/test-nogit/.specify
# NO .git folder
```

**Execution**:
```bash
cd /tmp/test-nogit/src
source /path/to/spec-kit/scripts/bash/common.sh
result=$(get_repo_root)
echo "Result: $result"
```

**Expected**: `/tmp/test-nogit`
**Criteria**: ✅ Finds `.specify`, no `.git` needed (backward compatible)

**Cleanup**:
```bash
rm -rf /tmp/test-nogit
```

---

### T007 [P] Manual Validation: Git boundary edge case
**Reference**: `specs/002-git-folder-priority/spec.md` lines 88-89
**Contract Test Case**: `specs/002-git-folder-priority/contracts/get_repo_root.md` Test Case 4

**Setup**:
```bash
# Create git boundary scenario
mkdir -p /tmp/test-boundary/repo/project
mkdir -p /tmp/test-boundary/.specify  # Higher parent
mkdir -p /tmp/test-boundary/repo/.git  # Git root
# NO .specify at repo/ level
```

**Execution**:
```bash
cd /tmp/test-boundary/repo/project
source /path/to/spec-kit/scripts/bash/common.sh
result=$(get_repo_root)
echo "Result: $result"
```

**Expected**: `/tmp/test-boundary/repo`
**Criteria**: ✅ Stops at `.git` (first marker found), does NOT continue to parent `.specify`

**Cleanup**:
```bash
rm -rf /tmp/test-boundary
```

---

### T008 [P] Manual Validation: Nested .specify folders (Acceptance Scenario 4)
**Reference**: `specs/002-git-folder-priority/spec.md` lines 66-68
**Contract Test Case**: `specs/002-git-folder-priority/contracts/get_repo_root.md` Test Case 5

**Setup**:
```bash
# Create nested .specify scenario
mkdir -p /tmp/test-nested/project/submodule/src
mkdir -p /tmp/test-nested/project/.specify
mkdir -p /tmp/test-nested/project/submodule/.specify
```

**Execution**:
```bash
cd /tmp/test-nested/project/submodule/src
source /path/to/spec-kit/scripts/bash/common.sh
result=$(get_repo_root)
echo "Result: $result"
```

**Expected**: `/tmp/test-nested/project/submodule`
**Criteria**: ✅ Finds closest parent `.specify` (submodule), not higher-level one

**Cleanup**:
```bash
rm -rf /tmp/test-nested
```

---

## Dependencies

**Phase Order** (MUST follow):
1. Phase 3.1 (Core Implementation) BEFORE Phase 3.2 (Manual Validation)
   - T001 → Modify get_repo_root()
   - T002 → Modify find_repo_root()
   - T003 → Update create-new-feature.sh main logic
   - THEN run T004-T008 (manual validation)

**Parallel Execution Opportunities**:
- T001, T002, T003 are sequential (same file or dependent logic)
- T004, T005, T006, T007, T008 can run in parallel [P] (independent manual tests)

**Critical Path**:
```
T001 (get_repo_root)
  → T002 (find_repo_root)
  → T003 (main logic update)
  → T004-T008 (manual validation in parallel)
```

---

## Validation Criteria

**Functional Requirements Met**:
- [x] FR-001: `.specify` checked before `.git` (T001, T002)
- [x] FR-002: `.git` still valid fallback (T005, T007)
- [x] FR-003: Stops at first marker found (T007 - git boundary)
- [x] FR-004: Consistent logic across scripts (T001, T002 use same pattern)
- [x] FR-005: No-git support preserved (T006)
- [x] FR-006: Closest parent `.specify` used (T008)
- [x] FR-007: Error when no markers (inherited from existing behavior)
- [x] FR-008: Single-project backward compatible (T005)

**Non-Functional Requirements Met**:
- [x] NFR-001: No noticeable latency (O(n) traversal, n = directory depth)
- [x] NFR-002: Backward compatible (T005, T006 validate)
- [x] NFR-003: Clear error messages (preserved from existing implementation)

**All 8 tasks completion** = Feature ready for validation ✓

---

## Success Criteria

**Implementation Complete** when:
1. ✅ T001: `get_repo_root()` modified with `.specify` priority
2. ✅ T002: `find_repo_root()` modified with `.specify` priority
3. ✅ T003: `create-new-feature.sh` main logic updated
4. ✅ T004-T008: All 5 manual validation scenarios pass

**Documentation Verification**:
- ✅ quickstart.md examples match new behavior
- ✅ contracts/ specifications reflect implementation
- ✅ CLAUDE.md updated with repository root detection notes

**Ready for release** when all tasks marked [X] and manual validation confirms:
- Monorepo workflow works (T004)
- Backward compatibility maintained (T005, T006)
- Git boundary respected (T007)
- Nested .specify handled correctly (T008)
