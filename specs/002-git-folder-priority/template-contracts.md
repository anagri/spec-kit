# Template Contracts: Repository Root Detection Functions

**Feature**: 002-git-folder-priority | **Date**: 2025-10-06

This document defines the contracts for bash functions that detect repository root with `.specify` folder priority for monorepo support.

---

## Contract: get_repo_root()

**Location**: `.specify/scripts/bash/common.sh`
**Purpose**: Find repository root directory with `.specify` folder taking priority over `.git` folder
**Used By**: All scripts that source common.sh (check-prerequisites.sh, setup-plan.sh, update-agent-context.sh)

### Interface

**Input**: None (uses current working directory from shell context)
**Output**: Absolute path to repository root (stdout)
**Exit Code**: Always 0 (never fails, has fallback)
**Side Effects**: None (read-only file system operations)

### Behavior Specification

1. **Start from current working directory**
2. **Traverse upward** through parent directories until marker found or root reached
3. **At each directory level**, check in priority order:
   - **First**: Check if `.specify/` folder exists
     - If yes: Return this directory as repository root, **STOP**
   - **Second**: Check if `.git/` folder exists
     - If yes: Return this directory as repository root, **STOP**
   - **Neither found**: Move to parent directory, repeat from step 3
4. **If filesystem root (/) reached** without finding any marker:
   - Fall back to script location: `<script_dir>/../../..`
   - Return that path (always succeeds)

### Priority Rules

- `.specify` folder has **highest priority**
- `.git` folder is **secondary fallback**
- Script location is **final fallback** (for non-git, non-specify environments)
- **First marker wins**: Stop immediately when first marker found at any level

### Edge Cases

| Scenario | Behavior |
|----------|----------|
| Both `.specify` and `.git` at same level | Return that directory (both markers present, priority doesn't matter) |
| `.specify` in subdirectory, `.git` in parent | Return subdirectory with `.specify` (closer to current directory) |
| `.git` in subdirectory, `.specify` in parent | Return subdirectory with `.git` (first marker found, stop traversal) |
| No `.specify`, no `.git` anywhere | Return script location fallback |
| Multiple `.specify` in nested directories | Return closest parent `.specify` to current directory |

### Example Scenarios

**Scenario 1: Monorepo with subdirectory projects**
```
/workspace/
├── .git/                    # Git root
├── project-a/
│   ├── .specify/            # Project A root ← Found first from project-a/src/
│   └── src/
└── project-b/
    ├── .specify/            # Project B root ← Found first from project-b/src/
    └── src/

Current directory: /workspace/project-a/src/
Result: /workspace/project-a
```

**Scenario 2: Git boundary respect**
```
/workspace/
├── .specify/                # Higher parent
└── repo/
    ├── .git/                # Git root ← Found first, STOP here
    └── project/             # Current directory

Current directory: /workspace/repo/project/
Result: /workspace/repo (NOT /workspace)
Rationale: First marker (.git) found during upward traversal, stop immediately
```

**Scenario 3: Traditional single project**
```
/project/
├── .git/                    # Git root
├── .specify/                # Project root (same level)
└── src/

Current directory: /project/src/
Result: /project
Rationale: Both markers at same level, return that directory
```

---

## Contract: find_repo_root()

**Location**: `.specify/scripts/bash/create-new-feature.sh`
**Purpose**: Find repository root from specified starting directory (standalone function, not sourced)
**Used By**: create-new-feature.sh internally

### Interface

**Input**: `$1` = Starting directory path (absolute or relative)
**Output**: Absolute path to repository root (stdout)
**Exit Code**:
- `0` = Repository root found successfully
- `1` = No repository markers found (error)
**Side Effects**: None (read-only file system operations)

### Behavior Specification

1. **Start from provided directory** (`$1` parameter)
2. **Traverse upward** through parent directories until marker found or root reached
3. **At each directory level**, check in priority order:
   - **First**: Check if `.specify/` folder exists
     - If yes: Echo this directory path, exit with code 0, **STOP**
   - **Second**: Check if `.git/` folder exists
     - If yes: Echo this directory path, exit with code 0, **STOP**
   - **Neither found**: Move to parent directory, repeat from step 3
4. **If filesystem root (/) reached** without finding any marker:
   - Exit with code 1 (error, no repository found)

### Priority Rules

- `.specify` folder has **highest priority**
- `.git` folder is **secondary fallback**
- **No final fallback**: Returns error if no markers found (stricter than get_repo_root)
- **First marker wins**: Stop immediately when first marker found at any level

### Differences from get_repo_root()

| Aspect | get_repo_root() | find_repo_root() |
|--------|-----------------|------------------|
| Input | Current directory (implicit) | Starting directory (parameter) |
| Fallback | Script location (always succeeds) | None (can fail with exit 1) |
| Used by | Multiple scripts via sourcing | create-new-feature.sh only |
| Error handling | Never fails (has fallback) | Fails if no markers found |

### Edge Cases

| Scenario | Behavior |
|----------|----------|
| Both `.specify` and `.git` at same level | Return that directory, exit 0 |
| `.specify` in subdirectory, `.git` in parent | Return subdirectory with `.specify`, exit 0 |
| `.git` in subdirectory, `.specify` in parent | Return subdirectory with `.git`, exit 0 (stop at first marker) |
| No `.specify`, no `.git` anywhere | Exit 1 (error) |
| Starting directory doesn't exist | Undefined behavior (caller's responsibility to validate) |

### Example Scenarios

**Scenario 1: Monorepo - find project-specific root**
```
/workspace/
├── .git/                    # Git root
├── project-a/
│   ├── .specify/            # Project A root ← Found first
│   └── src/
└── project-b/
    └── src/

Input: /workspace/project-a/src
Output: /workspace/project-a
Exit code: 0
```

**Scenario 2: Git boundary - stop at first marker**
```
/workspace/
├── .specify/                # Higher parent (NOT reached)
└── repo/
    ├── .git/                # Git root ← Found first, STOP
    └── project/

Input: /workspace/repo/project
Output: /workspace/repo
Exit code: 0
Rationale: .git found during traversal, stop immediately (don't continue to parent .specify)
```

**Scenario 3: No markers - error**
```
/tmp/
└── random-dir/

Input: /tmp/random-dir
Output: (empty)
Exit code: 1
Error: No repository markers found
```

---

## Implementation Notes

### Current vs New Logic

**Current implementation** (common.sh:5-13):
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

**New implementation** (priority traversal):
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

**Current implementation** (create-new-feature.sh:22-32):
```bash
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -d "$dir/.specify" ]; then  # OR logic, .git checked first
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}
```

**New implementation** (priority logic):
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

### Key Changes

1. **Separate checks** instead of OR condition: `if [ -d ".specify" ]; then ... fi; if [ -d ".git" ]; then ... fi`
2. **Order matters**: `.specify` checked before `.git` at each level
3. **Stop on first match**: `return` immediately when marker found
4. **Backward compatible**: Existing scenarios continue to work (no `.specify` → falls back to `.git`)

---

## Validation Criteria

**Contract tests must verify**:
1. `.specify` found when present (priority)
2. `.git` found when `.specify` absent (fallback)
3. Closest parent `.specify` in nested scenarios
4. Git boundary respected (stop at first marker)
5. Error handling for no markers (find_repo_root only)
6. Fallback to script location (get_repo_root only)

**Integration tests must verify**:
1. Monorepo workflow (Acceptance Scenario 1)
2. Single-project backward compatibility (Acceptance Scenario 2)
3. No-git repo support (Acceptance Scenario 3)
4. Nested `.specify` folders (Acceptance Scenario 4)
5. Git boundary edge case (Edge Case from spec line 88-89)

---

## Dependencies

- **Unix utilities**: `dirname`, `pwd`, `cd`, `test` (POSIX-compliant)
- **File system**: Read access to parent directories during traversal
- **No git dependency**: Functions work without git installed (`.specify` check is file system only)

---

## Performance Considerations

- **Single traversal**: O(n) where n = directory depth from current to root
- **Early termination**: Stops at first marker (best case: O(1), worst case: O(n))
- **No external commands**: Pure bash, no `git` subprocess (faster)
- **Expected depth**: Typical projects 3-10 levels, monorepos 5-15 levels
- **Performance requirement** (from spec NFR-001): No noticeable latency (<10ms for 10 levels)
