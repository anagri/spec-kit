# Contract: find_repo_root()

**Function**: `find_repo_root()`
**File**: `.specify/scripts/bash/create-new-feature.sh`
**Lines**: 22-32 (current), will be modified
**Version**: 2.0 (priority-based traversal)

## Purpose

Find the repository root directory by traversing upward from a specified starting directory, prioritizing `.specify` folder over `.git` folder. Unlike `get_repo_root()`, this function can fail if no markers are found (stricter validation).

## Interface

### Input
- **Parameter 1**: `$1` = Starting directory path (absolute or relative)
- **Requires**: Read access to starting directory and its parents

### Output
- **stdout**: Absolute path to repository root (e.g., `/Users/name/project`)
- **stderr**: None (silent operation, error indicated by exit code)

### Exit Code
- **0** = Repository root found successfully
- **1** = No repository markers found (error)

### Side Effects
- None (read-only file system operations)
- No state modification
- No external process spawning (pure bash)

## Behavior

### Priority Traversal Algorithm

```
FUNCTION find_repo_root(starting_dir):
    SET dir = starting_dir

    WHILE dir != filesystem_root:
        # Priority 1: Check for .specify
        IF directory_exists(dir + "/.specify"):
            PRINT dir
            RETURN 0  # Success - STOP

        # Priority 2: Check for .git
        IF directory_exists(dir + "/.git"):
            PRINT dir
            RETURN 0  # Success - STOP

        # Neither found - move up
        SET dir = parent_directory(dir)
    END WHILE

    # No markers found - ERROR
    RETURN 1
END FUNCTION
```

### Step-by-Step Execution

1. **Initialize**: `dir="$1"` (starting directory parameter)

2. **Traversal Loop**: While `dir != "/"`
   - **Step 2a**: Check if `$dir/.specify` exists
     - **If YES**: Echo `$dir`, return 0, **STOP**
   - **Step 2b**: Check if `$dir/.git` exists
     - **If YES**: Echo `$dir`, return 0, **STOP**
   - **Step 2c**: Neither found - set `dir=$(dirname "$dir")`, continue loop

3. **Error Case**: If loop reaches filesystem root `/`
   - Return exit code 1 (no repository found)
   - No output on stdout

## Differences from get_repo_root()

| Aspect | get_repo_root() | find_repo_root() |
|--------|-----------------|------------------|
| **Input** | Current directory (implicit) | Starting directory (parameter $1) |
| **Fallback** | Script location (always succeeds) | None (fails with exit 1) |
| **Exit codes** | Always 0 | 0 = success, 1 = error |
| **Used by** | All scripts (via common.sh sourcing) | create-new-feature.sh only |
| **Error handling** | Never fails (has fallback) | Can fail if no markers found |
| **Use case** | General repo detection | Explicit marker validation |

## Test Cases

### Test Case 1: .specify Priority (Monorepo)
**Setup**:
```
/workspace/
├── .git/                    # Git root
└── project-a/
    ├── .specify/            # Project root
    └── src/
```

**Execution**:
```bash
result=$(find_repo_root "/workspace/project-a/src")
exit_code=$?
```

**Expected**:
- Output: `/workspace/project-a`
- Exit code: 0
- Rationale: `.specify` found at `/workspace/project-a`, returned before checking parent `.git`

---

### Test Case 2: Git Fallback (No .specify)
**Setup**:
```
/project/
├── .git/                    # Git root
└── src/
```

**Execution**:
```bash
result=$(find_repo_root "/project/src")
exit_code=$?
```

**Expected**:
- Output: `/project`
- Exit code: 0
- Rationale: No `.specify` found, falls back to `.git` at `/project`

---

### Test Case 3: Same Level Markers
**Setup**:
```
/project/
├── .git/
├── .specify/
└── src/
```

**Execution**:
```bash
result=$(find_repo_root "/project/src")
exit_code=$?
```

**Expected**:
- Output: `/project`
- Exit code: 0
- Rationale: Both markers at same level, `.specify` checked first (but both would return same directory)

---

### Test Case 4: Git Boundary (Stop at First Marker)
**Setup**:
```
/workspace/
├── .specify/                # Higher parent (NOT reached)
└── repo/
    ├── .git/                # Git root
    └── project/
```

**Execution**:
```bash
result=$(find_repo_root "/workspace/repo/project")
exit_code=$?
```

**Expected**:
- Output: `/workspace/repo`
- Exit code: 0
- Rationale: `.git` found at `/workspace/repo` during upward traversal, stop immediately (do NOT continue to parent `.specify`)

---

### Test Case 5: Nested .specify Folders
**Setup**:
```
/project/
├── .specify/                # Outer project
└── submodule/
    ├── .specify/            # Submodule (closest)
    └── src/
```

**Execution**:
```bash
result=$(find_repo_root "/project/submodule/src")
exit_code=$?
```

**Expected**:
- Output: `/project/submodule`
- Exit code: 0
- Rationale: Closest parent `.specify` at `/project/submodule`

---

### Test Case 6: No Markers - Error
**Setup**:
```
/tmp/
└── random-dir/
```

**Execution**:
```bash
result=$(find_repo_root "/tmp/random-dir")
exit_code=$?
```

**Expected**:
- Output: (empty string)
- Exit code: 1
- Rationale: No `.specify` or `.git` found, error returned

---

### Test Case 7: No-Git Repository
**Setup**:
```
/project/
├── .specify/                # Project root (no .git)
└── src/
```

**Execution**:
```bash
result=$(find_repo_root "/project/src")
exit_code=$?
```

**Expected**:
- Output: `/project`
- Exit code: 0
- Rationale: `.specify` found, `.git` not needed

---

### Test Case 8: Relative Path Input
**Setup**:
```
/workspace/project/.specify/
Current directory: /workspace/
```

**Execution**:
```bash
cd /workspace
result=$(find_repo_root "project")
exit_code=$?
```

**Expected**:
- Output: `/workspace/project`
- Exit code: 0
- Rationale: Relative path resolved, `.specify` found

---

## Edge Cases

| Scenario | Input | Expected Output | Exit Code | Rationale |
|----------|-------|-----------------|-----------|-----------|
| Symlink directory | `/link` → `/real/project` | `/real/project` | 0 | Follows symlinks, finds `.specify` |
| Non-existent directory | `/does/not/exist` | Undefined | Undefined | Caller's responsibility to validate |
| Filesystem root | `/` | (empty) | 1 | No markers at `/`, error |
| Empty input | `""` | Undefined | Undefined | Caller should validate non-empty |
| Absolute path | `/workspace/project/src` | (correct path) | 0 or 1 | Works as expected |
| Relative path | `../project/src` | (resolved path) | 0 or 1 | Resolves relative before traversal |

## Caller Responsibilities

The caller (create-new-feature.sh) must:
1. **Validate input**: Ensure `$1` is not empty
2. **Check directory exists**: Ensure starting directory is valid
3. **Handle errors**: Check exit code and handle `1` appropriately

**Example usage in create-new-feature.sh**:
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"

if [ $? -ne 0 ] || [ -z "$REPO_ROOT" ]; then
    echo "Error: Could not determine repository root." >&2
    exit 1
fi
```

---

## Dependencies

### Required Commands
- `dirname` - Get parent directory path (POSIX)
- `test -d` - Check if directory exists (POSIX)
- `echo` - Output result to stdout (POSIX)

### Assumptions
- Shell: Bash or POSIX-compatible shell
- File system: Case-sensitive (Unix-like)
- Permissions: Read access to starting directory and parents
- Input: Starting directory path is valid (caller's responsibility)

---

## Backward Compatibility

### Preserved Behaviors
- ✅ Single-project repos (`.git` + `.specify` at same level) → same result
- ✅ No-git repos (only `.specify`) → same result
- ✅ Git-only repos (no `.specify`) → falls back to `.git`
- ✅ Error when no markers → exit code 1 (preserved strictness)

### New Behaviors
- ✅ Monorepo support: Finds `.specify` in subdirectories before parent `.git`
- ✅ Nested `.specify`: Finds closest parent `.specify`
- ✅ Git boundary: Stops at `.git` even if parent has `.specify`

### Breaking Changes
- **None** - All existing use cases continue to work
- **Old behavior**: `if [ -d "$dir/.git" ] || [ -d "$dir/.specify" ]` (OR, either marker)
  - Problem: `.git` evaluated first in OR short-circuit, but both checked at same level
  - New behavior: Separate checks with explicit priority
  - Result: Same outcome for existing repos, new behavior for monorepos

---

## Performance

### Complexity
- **Time**: O(n) where n = directory depth from starting point to marker or root
- **Space**: O(1) - single directory variable, no recursion
- **Best case**: O(1) - `.specify` in starting directory
- **Worst case**: O(n) - no markers, traverse to `/`, return error

### Benchmarks
- Typical depth: 3-10 directories
- Monorepo depth: 5-15 directories
- Target: <10ms for 10 levels (NFR-001 from spec)
- Implementation: Pure bash, no subprocesses → fast

### Optimization Notes
- Early termination: Returns on first marker found
- No external commands: Native bash only
- Directory checks: `test -d` is fast (kernel-level)

---

## Implementation Checklist

- [ ] Change OR condition to separate priority checks
- [ ] Check `.specify` before `.git` at each level
- [ ] Maintain exit code behavior (0 = success, 1 = error)
- [ ] Test all 8 test cases above
- [ ] Verify backward compatibility
- [ ] Benchmark performance (<10ms for 10 levels)
- [ ] Ensure caller (create-new-feature.sh) handles exit codes correctly

---

## Integration with create-new-feature.sh

**Current usage** (lines 39-49):
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

**New usage** (priority-first):
```bash
# Try find_repo_root first (supports .specify priority)
REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
if [ $? -ne 0 ] || [ -z "$REPO_ROOT" ]; then
    echo "Error: Could not determine repository root. Please run this script from within the repository." >&2
    exit 1
fi

# Determine if we have git
if git rev-parse --show-toplevel >/dev/null 2>&1; then
    HAS_GIT=true
else
    HAS_GIT=false
fi
```

**Rationale for change**:
- Old: Uses `git rev-parse` first (`.git` priority), falls back to `find_repo_root`
- New: Uses `find_repo_root` first (`.specify` priority), git check is separate
- Benefit: Consistent priority across all detection methods
