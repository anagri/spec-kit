# Quickstart: Testing Local Development Mode

**Feature**: 003-local-to-cmdline
**Purpose**: Validate `--local` flag works as specified
**Time**: ~5 minutes

## Prerequisites

- Local clone of spec-kit repository
- Python 3.11+ with uv installed
- Terminal access

## Test Scenario 1: Happy Path (Valid Local Repository)

### Setup
```bash
# Ensure you're in spec-kit root
cd /path/to/spec-kit

# Verify source directories exist
ls -la templates/ scripts/bash/ memory/
```

### Execute
```bash
# Test with absolute path
uvx --from . specify-cli init test-local-absolute --local $(pwd)

# Verify project created
cd test-local-absolute
ls -la .specify/ .claude/
```

### Expected Result
```
✓ Project directory created: test-local-absolute/
✓ Directory structure:
  - .specify/templates/ (contains *.md files)
  - .specify/scripts/bash/ (contains *.sh files, executable)
  - .specify/memory/constitution.md
  - .claude/commands/ (contains *.md files)
✓ No network requests made (no GitHub API calls)
✓ Progress tracker showed "Copy templates from local" step
```

### Validation
```bash
# Check templates copied
ls .specify/templates/
# Expected: spec-template.md, plan-template.md, tasks-template.md, agent-file-template.md

# Check commands copied
ls .claude/commands/
# Expected: specify.md, plan.md, tasks.md, implement.md, clarify.md, analyze.md, constitution.md

# Check scripts executable
ls -l .specify/scripts/bash/*.sh
# Expected: All .sh files have 'x' permission

# Check memory copied
ls .specify/memory/
# Expected: constitution.md
```

---

## Test Scenario 2: Relative Path Support

### Setup
```bash
# Create test directory outside spec-kit
cd /tmp
mkdir relpath-test && cd relpath-test
```

### Execute
```bash
# Use relative path to spec-kit
uvx --from /path/to/spec-kit specify-cli init test-relative --local ../../../path/to/spec-kit
```

### Expected Result
```
✓ Relative path resolved correctly
✓ Same directory structure as Scenario 1
✓ No errors about path not found
```

---

## Test Scenario 3: --here Flag Combination

### Setup
```bash
# Create empty directory
mkdir -p /tmp/here-test
cd /tmp/here-test
```

### Execute
```bash
# Initialize in current directory
uvx --from /path/to/spec-kit specify-cli init --here --local /path/to/spec-kit
```

### Expected Result
```
✓ Templates merged into current directory
✓ .specify/ and .claude/ created in /tmp/here-test/
✓ No subdirectory created
```

---

## Test Scenario 4: Invalid Path (Error Handling)

### Execute
```bash
# Non-existent path
uvx --from . specify-cli init test-error --local /nonexistent/path
```

### Expected Result
```
ERROR: Local path '/nonexistent/path' does not exist

Provide a valid path to a spec-kit repository.

✓ Clear error message shown
✓ No project directory created
✓ Exit code 1
```

---

## Test Scenario 5: Incomplete Repository (Missing Directories)

### Setup
```bash
# Create incomplete repository
mkdir -p /tmp/incomplete-repo/templates
mkdir -p /tmp/incomplete-repo/scripts
# Missing: scripts/bash/, memory/
```

### Execute
```bash
uvx --from . specify-cli init test-incomplete --local /tmp/incomplete-repo
```

### Expected Result
```
ERROR: Invalid spec-kit repository structure

Missing required directories:
  ✗ scripts/bash/
  ✗ memory/

Found:
  ✓ templates/

✓ Error lists specific missing directories
✓ No project created
✓ Exit code 1
```

---

## Test Scenario 6: Symlink Resolution

### Setup
```bash
cd /tmp
mkdir -p symlink-test/templates/commands
echo "# Test Template" > symlink-test/templates/real-file.md
ln -s real-file.md symlink-test/templates/link-file.md

# Complete the structure
mkdir -p symlink-test/scripts/bash
mkdir -p symlink-test/memory
```

### Execute
```bash
uvx --from . specify-cli init test-symlink --local /tmp/symlink-test
```

### Expected Result
```
✓ Symlink followed (copied target content)
✓ test-symlink/.specify/templates/link-file.md contains "# Test Template"
✓ link-file.md is a regular file, not a symlink
```

### Validation
```bash
cd test-symlink
ls -l .specify/templates/link-file.md
# Expected: Regular file (not symlink), readable content
cat .specify/templates/link-file.md
# Expected: "# Test Template"
```

---

## Test Scenario 7: Recursive Subdirectory Copying

### Setup
```bash
# Create nested structure
mkdir -p /tmp/nested-repo/templates/commands/subdir
mkdir -p /tmp/nested-repo/scripts/bash/utils
mkdir -p /tmp/nested-repo/memory

echo "# Nested" > /tmp/nested-repo/scripts/bash/utils/helper.sh
```

### Execute
```bash
uvx --from . specify-cli init test-nested --local /tmp/nested-repo
```

### Expected Result
```
✓ Subdirectories preserved
✓ test-nested/.specify/scripts/bash/utils/helper.sh exists
✓ Directory structure maintained
```

### Validation
```bash
ls -R test-nested/.specify/scripts/bash/
# Expected: utils/ subdirectory with helper.sh
```

---

## Test Scenario 8: Works with --no-git Flag

### Execute
```bash
uvx --from . specify-cli init test-nogit --local $(pwd) --no-git
```

### Expected Result
```
✓ Project created without git initialization
✓ No .git/ directory
✓ All templates copied normally
```

### Validation
```bash
cd test-nogit
ls -la .git
# Expected: ls: .git: No such file or directory
```

---

## Test Scenario 9: Performance Check

### Execute
```bash
time uvx --from . specify-cli init test-perf --local $(pwd)
```

### Expected Result
```
✓ Completion time < 2 seconds
✓ No noticeable delay compared to GitHub mode
✓ Progress tracker updates smoothly
```

---

## Cleanup

```bash
# Remove test projects
rm -rf test-local-absolute test-relative test-symlink test-nested test-nogit test-perf
rm -rf /tmp/here-test /tmp/incomplete-repo /tmp/symlink-test /tmp/nested-repo
```

---

## Success Criteria

All test scenarios pass:
- [x] Scenario 1: Valid local repository initialization
- [x] Scenario 2: Relative paths resolved correctly
- [x] Scenario 3: --here flag compatibility
- [x] Scenario 4: Clear error for invalid path
- [x] Scenario 5: Validation of incomplete repository
- [x] Scenario 6: Symlinks dereferenced properly
- [x] Scenario 7: Recursive copying preserves structure
- [x] Scenario 8: --no-git flag compatibility
- [x] Scenario 9: Performance acceptable (<2s)

**Definition of Done**: All 9 scenarios pass without errors, demonstrating FR-001 through FR-017 compliance.

---

## Troubleshooting

### "Module not found" Error
```bash
# Ensure you're running from spec-kit root
cd /path/to/spec-kit
uvx --from . specify-cli init test --local $(pwd)
```

### "Permission denied" on Scripts
```bash
# Check scripts are executable after copy
ls -l .specify/scripts/bash/*.sh
# If not executable, implementation has bug in ensure_executable_scripts() call
```

### Project Directory Already Exists
```bash
# Use unique names or clean up between tests
rm -rf test-* before re-running
```
