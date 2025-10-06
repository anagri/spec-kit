# Contract: get_repo_root()

**Function**: `get_repo_root()`
**File**: `.specify/scripts/bash/common.sh`
**Lines**: 5-13 (current), will be modified
**Version**: 2.0 (priority-based traversal)

## Purpose

Find the repository root directory by traversing upward from the current working directory, prioritizing `.specify` folder over `.git` folder to support monorepo workflows.

## Interface

### Input
- **None** (implicit: uses current working directory from shell context)
- **Requires**: Read access to parent directories

### Output
- **stdout**: Absolute path to repository root (e.g., `/Users/name/project`)
- **stderr**: None (silent operation)

### Exit Code
- **Always 0** (never fails, guaranteed to return a path via fallback)

### Side Effects
- None (read-only file system operations)
- No state modification
- No external process spawning (pure bash)

## Behavior

### Priority Traversal Algorithm

```
FUNCTION get_repo_root():
    SET dir = current_working_directory()

    WHILE dir != filesystem_root:
        # Priority 1: Check for .specify
        IF directory_exists(dir + "/.specify"):
            RETURN dir
            EXIT  # STOP - do not continue traversal

        # Priority 2: Check for .git
        IF directory_exists(dir + "/.git"):
            RETURN dir
            EXIT  # STOP - do not continue traversal

        # Neither found - move up
        SET dir = parent_directory(dir)
    END WHILE

    # Fallback: No markers found
    SET script_dir = directory_of_this_script()
    SET fallback_root = resolve_path(script_dir + "/../../..")
    RETURN fallback_root
END FUNCTION
```

### Step-by-Step Execution

1. **Initialize**: `dir = $(pwd)` (current working directory)

2. **Traversal Loop**: While `dir != "/"`
   - **Step 2a**: Check if `$dir/.specify` exists
     - **If YES**: Echo `$dir`, return 0, **STOP**
   - **Step 2b**: Check if `$dir/.git` exists
     - **If YES**: Echo `$dir`, return 0, **STOP**
   - **Step 2c**: Neither found - set `dir=$(dirname "$dir")`, continue loop

3. **Fallback**: If loop reaches filesystem root `/`
   - Calculate: `script_dir = <directory of common.sh>`
   - Return: `$script_dir/../../..` (3 levels up from script location)
   - This assumes structure: `repo_root/.specify/scripts/bash/common.sh`

## Test Cases

### Test Case 1: .specify Priority (Monorepo)
**Setup**:
```
/workspace/
├── .git/                    # Git root
└── project-a/
    ├── .specify/            # Project root
    └── src/                 # Current directory
```

**Execution**:
```bash
cd /workspace/project-a/src
result=$(get_repo_root)
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
└── src/                     # Current directory (no .specify anywhere)
```

**Execution**:
```bash
cd /project/src
result=$(get_repo_root)
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
├── .git/                    # Git root
├── .specify/                # Project root (same level)
└── src/                     # Current directory
```

**Execution**:
```bash
cd /project/src
result=$(get_repo_root)
```

**Expected**:
- Output: `/project`
- Exit code: 0
- Rationale: Both markers at same level, return that directory (either check succeeds)

---

### Test Case 4: Git Boundary (Stop at First Marker)
**Setup**:
```
/workspace/
├── .specify/                # Higher parent
└── repo/
    ├── .git/                # Git root
    └── project/             # Current directory
```

**Execution**:
```bash
cd /workspace/repo/project
result=$(get_repo_root)
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
├── .specify/                # Outer project root
└── submodule/
    ├── .specify/            # Submodule root
    └── src/                 # Current directory
```

**Execution**:
```bash
cd /project/submodule/src
result=$(get_repo_root)
```

**Expected**:
- Output: `/project/submodule`
- Exit code: 0
- Rationale: Closest parent `.specify` found at `/project/submodule`

---

### Test Case 6: Fallback (No Markers)
**Setup**:
```
/tmp/
└── random-dir/              # Current directory (no .specify or .git anywhere)
```

**Execution**:
```bash
# Assume common.sh is at /opt/spec-kit/.specify/scripts/bash/common.sh
cd /tmp/random-dir
result=$(get_repo_root)
```

**Expected**:
- Output: `/opt/spec-kit` (script_dir/../../..)
- Exit code: 0
- Rationale: No markers found, fall back to script location

---

### Test Case 7: No-Git Repository
**Setup**:
```
/project/
├── .specify/                # Project root (no .git)
└── src/                     # Current directory
```

**Execution**:
```bash
cd /project/src
result=$(get_repo_root)
```

**Expected**:
- Output: `/project`
- Exit code: 0
- Rationale: `.specify` found, `.git` not needed

---

## Edge Cases

| Scenario | Current Directory | Expected Output | Rationale |
|----------|-------------------|-----------------|-----------|
| Symlink to .specify | `/link/src` → `/real/project/src`<br>`.specify` at `/real/project/.specify` | `/real/project` | Follows symlinks via `pwd` resolution |
| Hidden parent .specify | `/project/.hidden/.specify`<br>Current: `/project/.hidden/src` | `/project/.hidden` | Directory check works on hidden folders |
| Permission denied on parent | `/restricted/` (no read)<br>Current: `/restricted/project/` | Undefined (bash test fails) | Caller's responsibility to handle |
| Filesystem root as current | `cd /` | `<script_location>/../..` (fallback) | No markers at `/`, uses fallback |

---

## Dependencies

### Required Commands
- `pwd` - Get current working directory (POSIX)
- `dirname` - Get parent directory path (POSIX)
- `test -d` - Check if directory exists (POSIX)
- `cd` - Change directory for path resolution (POSIX)

### Assumptions
- Shell: Bash or POSIX-compatible shell
- File system: Case-sensitive (Unix-like)
- Permissions: Read access to parent directories during traversal
- Structure: Script located at `<repo>/.specify/scripts/bash/common.sh` for fallback

---

## Backward Compatibility

### Preserved Behaviors
- ✅ Single-project repos (`.git` + `.specify` at same level) → same result
- ✅ No-git repos (`--no-git` init, only `.specify`) → same result (no `.git` to check)
- ✅ Git-only repos (no `.specify`) → falls back to `.git`
- ✅ Always succeeds (never fails, has fallback)

### New Behaviors
- ✅ Monorepo support: Finds `.specify` in subdirectories before parent `.git`
- ✅ Nested `.specify`: Finds closest parent `.specify`
- ✅ Git boundary: Stops at `.git` even if parent has `.specify`

### Breaking Changes
- **None** - All existing use cases continue to work

---

## Performance

### Complexity
- **Time**: O(n) where n = directory depth from current to marker or root
- **Space**: O(1) - single directory variable, no recursion
- **Best case**: O(1) - `.specify` in current directory
- **Worst case**: O(n) - no markers, traverse to `/`, use fallback

### Benchmarks
- Typical depth: 3-10 directories (project structure)
- Monorepo depth: 5-15 directories
- Target: <10ms for 10 levels (NFR-001 from spec)
- Implementation: Pure bash, no subprocesses → fast

### Optimization Notes
- Early termination: Returns on first marker found
- No external commands: Avoids `git rev-parse` subprocess overhead
- Directory checks: Native bash `test -d` (fast)

---

## Implementation Checklist

- [ ] Remove `git rev-parse` check (old priority logic)
- [ ] Add upward traversal loop with `.specify` priority
- [ ] Implement fallback to script location
- [ ] Preserve exit code 0 guarantee
- [ ] Test all 7 test cases above
- [ ] Verify backward compatibility (3 preserved behaviors)
- [ ] Benchmark performance (<10ms for 10 levels)
