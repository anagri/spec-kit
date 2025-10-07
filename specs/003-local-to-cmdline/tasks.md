# Tasks: Local Development Mode for Template Distribution

**Feature**: 003-local-to-cmdline
**Input**: Design documents from `/Users/amir36/Documents/workspace/src/github.com/anagri/spec-kit/specs/003-local-to-cmdline/`
**Prerequisites**: plan.md ✓, template-contracts.md ✓, contracts/function_signatures.py ✓, quickstart.md ✓

## Execution Flow (main)
```
1. Load plan.md → Tech stack: Python 3.11+, typer, rich, pathlib, shutil
2. Load design documents:
   → template-contracts.md: CLI interface, directory structure, file copy, error handling
   → contracts/function_signatures.py: validate_local_repo(), copy_local_templates(), init()
   → quickstart.md: 9 test scenarios (happy path, errors, edge cases)
3. Generate tasks by category:
   → Setup: None needed (existing project)
   → Tests: 13 contract tests (TDD - must fail first)
   → Core: 3 function implementations + 1 CLI integration
   → Integration: Progress tracker, error handling
   → Polish: 9 quickstart scenarios, version bump, CHANGELOG
4. Apply task rules:
   → Contract tests [P] - independent test files
   → validate_local_repo() and copy_local_templates() [P] - independent functions
   → init() modification depends on both functions above
   → Quickstart scenarios sequential (CLI operations)
5. Number tasks T001-T025
6. Return: SUCCESS (25 tasks ready for TDD execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **CLI Implementation**: `src/specify_cli/__init__.py` (single-file CLI)
- **Tests**: `tests/contract/` (TDD contract tests)
- **Manual Testing**: Follow `specs/003-local-to-cmdline/quickstart.md`

---

## Phase 3.1: Setup
*No setup tasks required - modifying existing CLI implementation*

---

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

### CLI Parameter Parsing Tests
- [ ] **T001** [P] Contract test: `--local` flag accepts path argument in `tests/contract/test_local_flag_parsing.py`
  - Assert `--local /path` stores path value
  - Assert `--local ../relative` resolves relative path
  - Assert `--local` without argument raises error

### Path Validation Tests
- [ ] **T002** [P] Contract test: Path existence validation in `tests/contract/test_path_validation.py`
  - Assert nonexistent path raises error with message "Local path '...' does not exist"
  - Assert file path (not directory) raises error "is not a directory"
  - Assert valid directory path passes

- [ ] **T003** [P] Contract test: Repository structure validation in `tests/contract/test_repo_structure.py`
  - Assert missing `templates/` raises error listing missing directories
  - Assert missing `scripts/bash/` raises error
  - Assert missing `memory/` raises error
  - Assert missing `templates/commands/` raises error
  - Assert all present returns (True, None)

### File Copy Behavior Tests
- [ ] **T004** [P] Contract test: Directory mapping in `tests/contract/test_directory_mapping.py`
  - Assert `templates/*.md` → `.specify/templates/*.md` (excluding commands/)
  - Assert `templates/commands/` → `.claude/commands/`
  - Assert `scripts/bash/` → `.specify/scripts/bash/`
  - Assert `memory/` → `.specify/memory/`

- [ ] **T005** [P] Contract test: Recursive copy in `tests/contract/test_recursive_copy.py`
  - Create nested structure: `scripts/bash/utils/helper.sh`
  - Assert subdirectories preserved: `.specify/scripts/bash/utils/helper.sh` exists
  - Assert file content identical

- [ ] **T006** [P] Contract test: Symlink dereferencing in `tests/contract/test_symlink_handling.py`
  - Create symlink: `templates/link.md` → `real.md`
  - Assert copied file is regular file (not symlink)
  - Assert content matches symlink target

- [ ] **T007** [P] Contract test: Executable permissions in `tests/contract/test_script_permissions.py`
  - Copy `scripts/bash/test.sh`
  - Assert `.specify/scripts/bash/test.sh` has executable permission (+x)
  - Assert applied recursively to subdirectories

### Error Handling Tests
- [ ] **T008** [P] Contract test: Path not exist error in `tests/contract/test_error_path_not_exist.py`
  - Run `init --local /nonexistent`
  - Assert error message: "Local path '/nonexistent' does not exist"
  - Assert Rich Panel format
  - Assert exit code 1

- [ ] **T009** [P] Contract test: Path not directory error in `tests/contract/test_error_not_directory.py`
  - Create file `/tmp/file.txt`
  - Run `init --local /tmp/file.txt`
  - Assert error message: "is not a directory"
  - Assert exit code 1

- [ ] **T010** [P] Contract test: Incomplete repo error in `tests/contract/test_error_incomplete_repo.py`
  - Create repo with only `templates/` directory
  - Run `init --local <path>`
  - Assert error lists "Missing required directories"
  - Assert shows found vs. missing directories
  - Assert exit code 1

### Integration Tests (Flag Combinations)
- [ ] **T011** [P] Contract test: `--local` with `--here` in `tests/contract/test_local_here_combination.py`
  - Run `init --here --local <path>` in existing directory
  - Assert `.specify/` and `.claude/` created in current directory
  - Assert no subdirectory created

- [ ] **T012** [P] Contract test: `--local` with `--no-git` in `tests/contract/test_local_nogit_combination.py`
  - Run `init test --local <path> --no-git`
  - Assert templates copied
  - Assert no `.git/` directory created

- [ ] **T013** [P] Contract test: `--local` with `--force` in `tests/contract/test_local_force_combination.py`
  - Create project directory manually
  - Run `init test --local <path> --force`
  - Assert no confirmation prompt
  - Assert templates copied (overwrite mode)

---

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Function Implementations
- [ ] **T014** [P] Implement `validate_local_repo()` in `src/specify_cli/__init__.py`
  - Input: Resolved absolute Path object
  - Output: (is_valid: bool, error_message: Optional[str])
  - Validation: Check `templates/`, `scripts/bash/`, `memory/`, `templates/commands/` exist
  - Error format: Rich Panel with missing vs. found directories
  - Make tests T002, T003, T010 pass

- [ ] **T015** [P] Implement `copy_local_templates()` in `src/specify_cli/__init__.py`
  - Input: project_path, local_path, is_current_dir, tracker
  - Behavior: Copy with path mapping per template-contracts.md
  - Use `shutil.copytree(symlinks=False, dirs_exist_ok=True)`
  - Update tracker: add("copy", "Copy templates from local"), start(), complete()
  - Make tests T004, T005, T006 pass

- [ ] **T016** Add `local` parameter to `init()` signature in `src/specify_cli/__init__.py`
  - Add parameter: `local: Optional[str] = None`
  - Add Typer option: `@click.option("--local", type=str, help="...")`
  - No implementation yet - just signature change
  - Make test T001 pass

### CLI Integration
- [ ] **T017** Integrate local mode branch in `init()` execution flow in `src/specify_cli/__init__.py`
  - After argument validation, before GitHub download
  - Branch logic:
    ```python
    if local:
        local_path = Path(local).resolve()
        if not local_path.exists():
            # Rich Panel error, Exit(1)
        if not local_path.is_dir():
            # Rich Panel error, Exit(1)
        is_valid, error = validate_local_repo(local_path)
        if not is_valid:
            # Rich Panel error (from validate_local_repo), Exit(1)
        copy_local_templates(project_path, local_path, here, tracker)
    else:
        # Existing GitHub download flow
    ```
  - Make tests T008, T009, T011, T012, T013 pass

---

## Phase 3.4: Integration

### Progress Tracker Updates
- [ ] **T018** Update progress tracker for local mode in `src/specify_cli/__init__.py`
  - Add step labels: "Validate local repository", "Copy templates from local"
  - Update `StepTracker` messages in local mode branch
  - Ensure progress display matches quickstart.md expected output
  - Make integration tests show correct progress messages

### Error Handling Polish
- [ ] **T019** Add Rich Panel error formatting for all local mode errors in `src/specify_cli/__init__.py`
  - Path not exist error (FR-013)
  - Path not directory error (FR-013)
  - Invalid repo structure error (from validate_local_repo)
  - Copy permission error (FR-014)
  - Broken symlink error (FR-015)
  - Use existing Panel pattern from init() directory conflict handling
  - Make test T008, T009, T010 pass with proper formatting

### Post-Copy Operations
- [ ] **T020** Ensure `ensure_executable_scripts()` called after local copy in `src/specify_cli/__init__.py`
  - Applies to both local and GitHub mode (shared post-copy logic)
  - Recursively sets +x on all `.sh` files in `.specify/scripts/bash/`
  - Make test T007 pass

---

## Phase 3.5: Polish & Validation

### Manual Testing (Sequential - CLI operations)
- [ ] **T021** Run quickstart.md Scenario 1: Valid local repository (happy path)
  - Test with absolute path: `uvx --from . specify-cli init test-local-absolute --local $(pwd)`
  - Verify all directories created
  - Verify file count matches source
  - Verify no network requests

- [ ] **T022** Run quickstart.md Scenario 2-3: Relative paths and `--here` flag
  - Scenario 2: Test relative path resolution
  - Scenario 3: Test `--here` flag (no subdirectory)
  - Verify behavior matches expectations

- [ ] **T023** Run quickstart.md Scenario 4-5: Error handling
  - Scenario 4: Invalid path error
  - Scenario 5: Incomplete repository error
  - Verify error messages match template-contracts.md format

- [ ] **T024** Run quickstart.md Scenario 6-9: Edge cases and performance
  - Scenario 6: Symlink resolution
  - Scenario 7: Recursive subdirectories
  - Scenario 8: `--no-git` compatibility
  - Scenario 9: Performance check (<2 seconds)

### Release Preparation
- [ ] **T025** Version bump and CHANGELOG in `pyproject.toml` and `CHANGELOG.md`
  - Bump version: MINOR (e.g., v0.2.0 → v0.3.0) - new feature flag
  - Add CHANGELOG entry:
    ```
    ## [X.Y.Z] - 2025-10-07
    ### Added
    - `--local <path>` flag for `init` command to support local template development
    - Local repository validation (requires templates/, scripts/bash/, memory/)
    - Path mapping from repository structure to installed structure
    - Symlink dereferencing during local copy
    ```
  - Test with `uvx --from . specify-cli init test --local $(pwd)`

---

## Dependencies

### Critical Path (TDD)
```
Tests (T001-T013) → Implementation (T014-T020) → Validation (T021-T025)
```

### Detailed Dependencies
- **T001-T013** (Tests): No dependencies - all [P] (parallel)
- **T014** `validate_local_repo()`: Blocked by T002, T003, T010 (tests must fail first)
- **T015** `copy_local_templates()`: Blocked by T004, T005, T006, T007 (tests must fail first)
- **T016** `init()` signature: Blocked by T001 (test must fail first)
- **T017** `init()` integration: Blocked by T014, T015, T016 (needs both functions + signature)
- **T018** Progress tracker: Blocked by T017 (needs local mode branch)
- **T019** Error handling: Blocked by T017 (needs local mode branch)
- **T020** Executable scripts: Blocked by T017 (needs copy flow complete)
- **T021-T024** Manual testing: Blocked by T020 (needs implementation complete)
- **T025** Version bump: Blocked by T024 (needs all tests passing)

### Parallelization Groups
```
GROUP 1 [P]: T001, T002, T003, T004, T005, T006, T007, T008, T009, T010, T011, T012, T013
  → All contract tests - independent files

GROUP 2 [P]: T014, T015
  → validate_local_repo() and copy_local_templates() - independent functions

GROUP 3: T016, T017, T018, T019, T020
  → Sequential - all modify same file (src/specify_cli/__init__.py)

GROUP 4: T021, T022, T023, T024
  → Sequential - manual CLI testing

GROUP 5: T025
  → Sequential - release preparation
```

---

## Parallel Execution Examples

### Launch All Contract Tests (Group 1)
```bash
# Run 13 test tasks in parallel (TDD - expect all to fail initially)
Task: "Contract test: --local flag accepts path argument in tests/contract/test_local_flag_parsing.py"
Task: "Contract test: Path existence validation in tests/contract/test_path_validation.py"
Task: "Contract test: Repository structure validation in tests/contract/test_repo_structure.py"
Task: "Contract test: Directory mapping in tests/contract/test_directory_mapping.py"
Task: "Contract test: Recursive copy in tests/contract/test_recursive_copy.py"
Task: "Contract test: Symlink dereferencing in tests/contract/test_symlink_handling.py"
Task: "Contract test: Executable permissions in tests/contract/test_script_permissions.py"
Task: "Contract test: Path not exist error in tests/contract/test_error_path_not_exist.py"
Task: "Contract test: Path not directory error in tests/contract/test_error_not_directory.py"
Task: "Contract test: Incomplete repo error in tests/contract/test_error_incomplete_repo.py"
Task: "Contract test: --local with --here in tests/contract/test_local_here_combination.py"
Task: "Contract test: --local with --no-git in tests/contract/test_local_nogit_combination.py"
Task: "Contract test: --local with --force in tests/contract/test_local_force_combination.py"
```

### Launch Core Function Implementations (Group 2)
```bash
# Run 2 implementation tasks in parallel (after tests fail)
Task: "Implement validate_local_repo() in src/specify_cli/__init__.py"
Task: "Implement copy_local_templates() in src/specify_cli/__init__.py"
```

---

## Notes

### TDD Workflow
1. **Phase 3.2** (T001-T013): Write all contract tests - EXPECT FAILURES
2. **Phase 3.3** (T014-T017): Implement functions to make tests pass
3. **Phase 3.4** (T018-T020): Polish integration and error handling
4. **Phase 3.5** (T021-T025): Manual validation and release prep

### File Modification Conflicts
- **Safe [P]**: All tests in `tests/contract/` - different files
- **Safe [P]**: T014, T015 - different functions in same file (no overlap)
- **Sequential**: T016-T020 - all modify `init()` function area
- **Sequential**: T021-T024 - manual CLI operations (state dependent)

### Key Technical Notes
- **Symlink handling**: `shutil.copytree(symlinks=False)` follows symlinks (dereferencing)
- **Path resolution**: `Path(local).resolve()` handles both relative and absolute paths
- **Permissions**: `ensure_executable_scripts()` already exists - reuse it
- **Error format**: Use Rich Panel matching existing pattern in `init()` (see src/specify_cli/__init__.py:806-816)
- **Progress tracker**: Use `StepTracker` class (see src/specify_cli/__init__.py:87-172)

---

## Validation Checklist
*GATE: Verify before marking Phase 3.5 complete*

- [ ] All contracts (template-contracts.md) have corresponding tests (T001-T013)
- [ ] All function signatures (contracts/function_signatures.py) implemented (T014-T017)
- [ ] All tests written before implementation (TDD - Phase 3.2 before 3.3)
- [ ] All [P] tasks truly independent (verified - different files or functions)
- [ ] Each task specifies exact file path (verified in task descriptions)
- [ ] No [P] task modifies same code area as another [P] task (verified - tests in separate files, functions non-overlapping)
- [ ] All 9 quickstart scenarios pass (T021-T024)
- [ ] Version bumped and CHANGELOG updated (T025)

---

## Task Count Summary
- **Setup**: 0 tasks (existing project)
- **Tests (TDD)**: 13 tasks (T001-T013) - all [P]
- **Implementation**: 7 tasks (T014-T020) - 2 [P], 5 sequential
- **Validation**: 4 tasks (T021-T024) - sequential
- **Release**: 1 task (T025)
- **Total**: 25 tasks

**Estimated Completion**:
- Group 1 (13 tests) [P]: 2-3 hours
- Group 2 (2 functions) [P]: 1-2 hours
- Group 3 (5 integration): 2-3 hours
- Group 4 (4 manual tests): 1 hour
- Group 5 (1 release): 30 minutes
- **Total**: ~7-10 hours

---

## Constitutional Compliance

**Alignment Check** (from plan.md):
- ✓ Layer 1 modification only (`src/specify_cli/__init__.py`)
- ✓ No template changes (templates/, scripts/, memory/ unchanged)
- ✓ No new scripts (reuses existing `ensure_executable_scripts()`)
- ✓ MINOR version bump (new optional feature flag)
- ✓ TDD approach (tests before implementation)
- ✓ Dogfooding methodology (using spec-kit to build spec-kit feature)

**Ready for Execution**: ✓ Yes - All 25 tasks defined, ordered, and dependency-mapped
