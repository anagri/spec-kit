# Template Contracts: Local Development Mode

**Feature**: 003-local-to-cmdline
**Date**: 2025-10-07
**Purpose**: Define CLI interface contracts and directory structure requirements

## CLI Interface Contract

### Command Signature
```bash
speclaude init <project-name> [OPTIONS]
speclaude init . [OPTIONS]
speclaude init --here [OPTIONS]
```

### New Flag: `--local`
```
--local TEXT    Path to local spec-kit repository (for template development)
```

**Type**: Optional path argument (string)
**Default**: None (uses GitHub download mode)
**Validation**:
- Must be a valid filesystem path
- Can be relative or absolute
- Must point to a directory (not a file)
- Directory must contain required subdirectories (see Directory Structure Contract)

**Behavior**:
- When NOT provided: Uses existing GitHub download flow
- When provided: Skips GitHub API/download, copies from local filesystem

**Compatibility**:
- Works with `--here` flag (initialize in current directory)
- Works with `--no-git` flag (skip git initialization)
- Works with `--force` flag (skip confirmation prompts)
- Works with `--ignore-agent-tools` flag (skip Claude CLI check)

### Examples
```bash
# Absolute path
speclaude init my-project --local /Users/dev/spec-kit

# Relative path
speclaude init my-project --local ../spec-kit

# With --here (current directory)
speclaude init --here --local ~/projects/spec-kit

# With --no-git
speclaude init test-proj --local ./spec-kit --no-git

# With --force (skip directory exists prompt)
speclaude init --here --local ../spec-kit --force
```

---

## Directory Structure Contract

### Local Repository Requirements

**Contract**: When `--local <path>` is provided, the path MUST point to a directory with this structure:

```
<local-path>/
├── templates/              # REQUIRED
│   ├── spec-template.md
│   ├── plan-template.md
│   ├── tasks-template.md
│   ├── agent-file-template.md
│   └── commands/          # REQUIRED subdirectory
│       ├── specify.md
│       ├── plan.md
│       ├── tasks.md
│       ├── implement.md
│       ├── clarify.md
│       ├── analyze.md
│       └── constitution.md
├── scripts/               # REQUIRED
│   └── bash/              # REQUIRED subdirectory
│       ├── common.sh
│       ├── create-new-feature.sh
│       ├── setup-plan.sh
│       ├── check-prerequisites.sh
│       └── update-agent-context.sh
└── memory/                # REQUIRED
    └── constitution.md
```

**Validation Rules**:
1. All three top-level directories MUST exist: `templates/`, `scripts/`, `memory/`
2. `templates/commands/` subdirectory MUST exist
3. `scripts/bash/` subdirectory MUST exist
4. Files within directories are NOT validated (flexible content)
5. Additional files/directories are allowed (ignored)
6. Symbolic links are followed (dereferenced to target content)

**Failure Behavior**:
If ANY required directory is missing:
```
ERROR: Invalid spec-kit repository structure

Missing directories:
  - templates/
  - scripts/bash/

Required structure:
  <path>/templates/
  <path>/scripts/bash/
  <path>/memory/

Ensure you're pointing to the root of a spec-kit repository.
```

### Target Project Structure

**Contract**: After successful initialization, target project MUST have:

```
<project-path>/
├── .specify/
│   ├── templates/              # Copied from <local>/templates/ (excluding commands/)
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   ├── tasks-template.md
│   │   └── agent-file-template.md
│   ├── scripts/
│   │   └── bash/              # Copied from <local>/scripts/bash/ (recursive)
│   │       ├── common.sh
│   │       ├── create-new-feature.sh
│   │       ├── setup-plan.sh
│   │       ├── check-prerequisites.sh
│   │       └── update-agent-context.sh
│   └── memory/                # Copied from <local>/memory/ (recursive)
│       └── constitution.md
└── .claude/
    └── commands/              # Copied from <local>/templates/commands/ (recursive)
        ├── specify.md
        ├── plan.md
        ├── tasks.md
        ├── implement.md
        ├── clarify.md
        ├── analyze.md
        └── constitution.md
```

**Mapping Rules**:
| Source (local repo) | Destination (project) | Mode |
|---------------------|----------------------|------|
| `templates/*.md` (exclude commands/) | `.specify/templates/*.md` | Recursive copy |
| `templates/commands/` | `.claude/commands/` | Recursive copy |
| `scripts/bash/` | `.specify/scripts/bash/` | Recursive copy |
| `memory/` | `.specify/memory/` | Recursive copy |

**Permissions**:
- All `.sh` files MUST have executable permission (`chmod +x`) after copy
- Applies recursively to all subdirectories in `scripts/bash/`

---

## File Copy Contract

### Copy Behavior

**Spec**: `shutil.copytree()` with specific parameters

**Parameters**:
- `symlinks=False`: Follow symlinks, copy target content
- `dirs_exist_ok=True`: Merge with existing directories (for `--here` mode)
- Preserve file metadata (timestamps, permissions where applicable)

**Recursive Copy**:
- ALL subdirectories copied with full structure
- Example: `scripts/bash/utils/helper.sh` → `.specify/scripts/bash/utils/helper.sh`

**Symlink Resolution**:
- If source file is a symlink: Copy the target file's contents
- Symlink is NOT preserved in target
- Broken symlinks result in copy error (fail fast)

**Overwrite Behavior**:
- When `--here` AND directory not empty: Merge/overwrite (requires `--force` or confirmation)
- When project directory doesn't exist: Create and copy
- When project directory exists (not `--here`): Error before copy

---

## Error Handling Contract

### Error Scenarios and Messages

#### 1. Path Does Not Exist
```python
# Input: --local /invalid/path
# Output:
ERROR: Local path '/invalid/path' does not exist

Provide a valid path to a spec-kit repository.
```

#### 2. Path Is Not a Directory
```python
# Input: --local /path/to/file.txt
# Output:
ERROR: Local path '/path/to/file.txt' is not a directory

The --local flag requires a directory containing a spec-kit repository.
```

#### 3. Missing Required Directories
```python
# Input: --local /path/to/incomplete-repo
# Output:
ERROR: Invalid spec-kit repository structure

Missing required directories:
  ✗ templates/commands/
  ✗ memory/

Found:
  ✓ templates/
  ✓ scripts/bash/

Required structure:
  templates/
  templates/commands/
  scripts/bash/
  memory/

Ensure you're pointing to the root of a spec-kit repository.
```

#### 4. Permission Error During Copy
```python
# Input: --local /read-only/repo
# Output:
ERROR: Permission denied copying templates

Details: [Errno 13] Permission denied: '/read-only/repo/templates/spec-template.md'

Ensure you have read access to the local repository.
```

#### 5. Broken Symlink
```python
# Input: --local /repo/with/broken-link
# Output:
ERROR: Cannot copy broken symlink

File: templates/broken-link.md
Target: /nonexistent/file.md (does not exist)

Fix or remove broken symlinks in the source repository.
```

---

## Progress Tracker Contract

### Local Mode Progress Steps

**Format**: Uses existing `StepTracker` class with custom messages

**Steps** (displayed during `--local` execution):

```
Initialize Specify Project
  ● Check required tools (ok)
  ● AI assistant (claude)
  ● Script type (sh)
  ● Validate local repository (3 directories found)
  ● Copy templates from local (47 files)
  ● Ensure scripts executable (5 updated)
  ● Initialize git repository (initialized)
  ● Finalize (project ready)
```

**Key Differences from GitHub Mode**:
| Step | GitHub Mode | Local Mode |
|------|-------------|------------|
| Step 4 | Fetch latest release | Validate local repository |
| Step 5 | Download template | Copy templates from local |
| Step 6 | Extract template | Ensure scripts executable |

**Implementation**:
```python
if local:
    tracker.add("validate", "Validate local repository")
    tracker.start("validate")
    # ... validation logic ...
    tracker.complete("validate", "3 directories found")

    tracker.add("copy", "Copy templates from local")
    tracker.start("copy")
    # ... copy logic ...
    tracker.complete("copy", f"{file_count} files")
else:
    tracker.add("fetch", "Fetch latest release")
    # ... existing GitHub logic ...
```

---

## Test Contract

### Contract Test Requirements

**Purpose**: Validate CLI behavior without implementation

**Test File**: `tests/contract/test_local_flag_contract.py`

**Test Cases** (TDD - write before implementation):

```python
def test_local_flag_accepts_path_argument():
    """Contract: --local flag accepts a path string"""
    # GIVEN: CLI with --local flag
    # WHEN: Invoked with path argument
    # THEN: Path is parsed and stored
    assert True  # Will fail until implemented

def test_local_path_validation_requires_templates_dir():
    """Contract: Local path must contain templates/ directory"""
    # GIVEN: Path without templates/ directory
    # WHEN: Validation runs
    # THEN: Error raised with specific message
    assert True  # Will fail until implemented

def test_local_path_validation_requires_scripts_bash_dir():
    """Contract: Local path must contain scripts/bash/ directory"""
    assert True  # Will fail until implemented

def test_local_path_validation_requires_memory_dir():
    """Contract: Local path must contain memory/ directory"""
    assert True  # Will fail until implemented

def test_local_path_resolves_relative_paths():
    """Contract: Relative paths resolved from CWD"""
    assert True  # Will fail until implemented

def test_local_path_resolves_absolute_paths():
    """Contract: Absolute paths used as-is"""
    assert True  # Will fail until implemented

def test_local_mode_creates_specify_directory():
    """Contract: Target must have .specify/ directory"""
    assert True  # Will fail until implemented

def test_local_mode_creates_claude_commands_directory():
    """Contract: Target must have .claude/commands/ directory"""
    assert True  # Will fail until implemented

def test_local_mode_copies_templates_recursively():
    """Contract: Subdirectories preserved in copy"""
    assert True  # Will fail until implemented

def test_local_mode_follows_symlinks():
    """Contract: Symlinks dereferenced to target content"""
    assert True  # Will fail until implemented

def test_local_mode_sets_executable_permissions():
    """Contract: Bash scripts have +x permission after copy"""
    assert True  # Will fail until implemented

def test_local_mode_works_with_here_flag():
    """Contract: --local compatible with --here"""
    assert True  # Will fail until implemented

def test_local_mode_works_with_no_git_flag():
    """Contract: --local compatible with --no-git"""
    assert True  # Will fail until implemented
```

---

## Non-Functional Contracts

### Performance
- Local copy operation: < 1 second for typical repository (~50-100 files)
- Path validation: < 50ms (3 directory existence checks)
- No network requests when `--local` provided (0 HTTP calls)

### Compatibility
- Python 3.11+ (existing requirement)
- POSIX systems (macOS, Linux, WSL)
- Works with all existing `init` flags

### Reliability
- Atomic operation: Either full success or rollback (no partial state)
- Fail-fast on validation errors (before any copy operations)
- Clear error messages for all failure modes

---

## Summary

**CLI Contract**: Add `--local <path>` optional flag to `init` command
**Directory Contract**: Validate 3 required directories in source, map to 4 target locations
**Copy Contract**: Recursive copy with symlink dereferencing, preserve structure
**Error Contract**: 5 specific error scenarios with formatted messages
**Progress Contract**: Reuse `StepTracker` with local-specific step labels
**Test Contract**: 13 contract tests (TDD - all fail initially)

**Validation**: All contracts testable without implementation (TDD ready)
