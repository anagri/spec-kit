# Local Development Mode Implementation - Explained

**Feature**: 003-local-to-cmdline
**Generated**: 2025-10-07
**Purpose**: Conversational explanation of the `--local` flag implementation plan

---

## **Phase 1: The Big Picture**

**What problem are we solving?**

Right now, when you develop spec-kit itself, if you want to test changes to templates, bash scripts, or the constitution, you have to:
1. Make changes to source files (in `templates/`, `scripts/`, `memory/`)
2. Create a GitHub release
3. Wait for the release workflow
4. Test the downloaded templates

This is slow and painful for rapid iteration.

**The solution?**

Add a `--local <path>` flag to the `speclaude init` command. When you use it:
```bash
speclaude init my-test-project --local /path/to/spec-kit
```

Instead of downloading from GitHub, it copies templates directly from your local repository. No releases needed.

**What changes, what doesn't?**

**Changes:**
- One new optional flag on `init` command
- Two new functions: `validate_local_repo()` and `copy_local_templates()`
- Modified execution flow inside `init()` function

**Stays the same:**
- Everything after the copy (making scripts executable, git init, etc.)
- All existing flags still work (`--here`, `--no-git`, `--force`)
- GitHub download mode is still the default
- No changes to templates, bash scripts, or the constitution
- No changes to slash commands

**Bottom line:** This is a Layer 1 (CLI) change only. You're adding a developer convenience feature that bypasses the network, nothing more.

---

## **Phase 2: The Technical Approach**

**How does it work under the hood?**

The implementation branches early in the `init()` function, but then rejoins the same path afterward. Think of it like a fork in a road that merges back together.

**The execution flow:**

```
1. User runs: speclaude init my-project --local /path/to/spec-kit
2. CLI parses arguments, validates project name
3. Creates project directory
4. Checks prerequisites (git, claude CLI)
5. ⚡ HERE'S WHERE IT SPLITS:

   IF --local flag provided:
     → Validate local repository structure
     → Copy files from local directories

   ELSE:
     → Download from GitHub
     → Extract zip file

6. ⚡ PATHS MERGE BACK:
   → Make bash scripts executable
   → Initialize git (unless --no-git)
   → Show success message
```

**The key decisions:**

1. **Path resolution:** Use Python's `Path.resolve()` to handle both relative (`../spec-kit`) and absolute (`/Users/you/spec-kit`) paths automatically

2. **Validation strategy:** Strict validation - all 3 required directories must exist:
   - `templates/` (with `templates/commands/` subdirectory)
   - `scripts/bash/`
   - `memory/`

   If ANY are missing, fail immediately with a clear error message showing what's missing and what was found.

3. **Copy strategy:** Use Python's `shutil.copytree()` because it:
   - Handles recursion automatically
   - Follows symlinks (copies the actual content, not the link)
   - Works with the `--here` flag (merge mode)

4. **Directory mapping:** This is crucial - it replicates exactly what the GitHub release does:

   ```
   Source (your repo)          →  Target (new project)
   templates/*.md              →  .specify/templates/
   templates/commands/         →  .claude/commands/
   scripts/bash/               →  .specify/scripts/bash/
   memory/                     →  .specify/memory/
   ```

**What about error handling?**

Five specific error scenarios, all with Rich Panel formatted messages:
- Path doesn't exist
- Path is a file (not directory)
- Missing required directories (shows which ones)
- Permission errors during copy
- Broken symlinks

Each error stops execution immediately (fail-fast) before any partial state is created.

---

## **Phase 3: The Implementation Details**

**What code gets written?**

You're modifying ONE file: `src/specify_cli/__init__.py`

**Two new functions to add:**

**1. `validate_local_repo(local_path: Path) -> Tuple[bool, Optional[str]]`**

Super simple validation function:
- Check if `templates/` exists
- Check if `templates/commands/` exists
- Check if `scripts/bash/` exists
- Check if `memory/` exists
- Return `(True, None)` if all good
- Return `(False, "error message")` if any missing

The error message lists what's missing and what was found, so you can immediately see the problem.

**2. `copy_local_templates(project_path, local_path, is_current_dir, tracker)`**

Does the actual copying with the directory mapping:
```python
# Copy templates/ (excluding commands/) to .specify/templates/
shutil.copytree(
    local_path / "templates",
    project_path / ".specify" / "templates",
    symlinks=False,  # Follow symlinks
    dirs_exist_ok=True  # Merge if --here used
)

# Copy templates/commands/ to .claude/commands/
shutil.copytree(
    local_path / "templates" / "commands",
    project_path / ".claude" / "commands",
    symlinks=False,
    dirs_exist_ok=True
)

# Similar for scripts/bash/ and memory/
```

Also updates the progress tracker: "Copy templates from local (47 files)"

**3. Modify existing `init()` function:**

Add one parameter:
```python
def init(
    project_name: Optional[str] = None,
    # ... all existing parameters ...
    local: Optional[str] = None,  # NEW
):
```

Then add the branching logic after prerequisite checks:
```python
if local:
    local_path = Path(local).resolve()

    # Validate path exists and is directory
    if not local_path.exists():
        # Rich Panel error, exit
    if not local_path.is_dir():
        # Rich Panel error, exit

    # Validate repo structure
    is_valid, error_msg = validate_local_repo(local_path)
    if not is_valid:
        # Rich Panel error with message, exit

    # Copy templates
    copy_local_templates(project_path, local_path, here, tracker)
else:
    # Existing GitHub download logic unchanged
    download_and_extract_template(...)
```

**Progress tracker changes:**

In local mode, instead of showing:
- "Fetch latest release"
- "Download template"
- "Extract template"

It shows:
- "Validate local repository (3 directories found)"
- "Copy templates from local (47 files)"

The rest stays identical.

---

## **Phase 4: Testing & Validation**

**How do you know it works?**

The quickstart.md defines **9 test scenarios** that cover everything. You'll run these manually since spec-kit uses manual CLI testing (no automated test suite).

**The test scenarios (grouped by purpose):**

**Happy Path Tests (scenarios 1-3):**
1. **Basic usage** - Absolute path: `speclaude init test --local $(pwd)`
   - Verify all directories created correctly
   - Check templates, scripts, commands all copied
   - Scripts have executable permissions

2. **Relative paths** - `speclaude init test --local ../spec-kit`
   - Paths resolve correctly from any location

3. **Flag combinations** - `speclaude init --here --local /path`
   - Works with `--here` (merge into current directory)
   - Works with `--no-git` (skip git initialization)

**Error Handling Tests (scenarios 4-5):**
4. **Invalid path** - `speclaude init test --local /nonexistent`
   - Shows clear error: "Local path does not exist"
   - No project directory created
   - Exit code 1

5. **Incomplete repository** - Missing `memory/` directory
   - Lists specific missing directories
   - Shows what WAS found
   - Helpful error message

**Edge Cases (scenarios 6-7):**
6. **Symlinks** - Source has symlinked files
   - Copies actual content (dereferences)
   - Target file is regular file, not symlink

7. **Nested directories** - `scripts/bash/utils/helper.sh`
   - Subdirectories preserved exactly
   - Structure maintained recursively

**Integration Tests (scenarios 8-9):**
8. **No-git flag** - `--local --no-git`
   - No `.git/` directory created
   - Templates still copied normally

9. **Performance check** - `time speclaude init test --local $(pwd)`
   - Should complete in < 2 seconds
   - No noticeable difference from GitHub mode

**The validation workflow:**

```bash
# From spec-kit root:
uvx --from . specify-cli init test1 --local $(pwd)
cd test1
ls -la .specify/ .claude/  # Verify structure
ls -l .specify/scripts/bash/*.sh  # Check executable
cd ..

# Run all 9 scenarios, clean up between:
rm -rf test1 test2 test3 ...
```

**Release checklist (after all tests pass):**

1. ✅ All 9 scenarios pass
2. ✅ Bump version in `pyproject.toml` (MINOR version - new feature)
3. ✅ Add entry to `CHANGELOG.md`
4. ✅ Test with real dogfooding: use `--local` to create a project, run `/specify`, `/plan` to ensure templates work
5. ✅ Git tag and push

---

## **Phase 5: What Could Go Wrong & Gotchas**

**Critical things to NOT mess up:**

**1. The directory mapping - get this EXACTLY right:**

The trickiest part is that `templates/commands/` goes to `.claude/commands/`, not `.specify/templates/commands/`. This is different from the other directories.

❌ **Wrong:**
```python
# Don't copy templates/ as one block - commands/ ends up in wrong place
shutil.copytree(local / "templates", project / ".specify/templates")
```

✅ **Right:**
```python
# Copy templates/*.md (excluding commands/) to .specify/templates/
# Copy templates/commands/ separately to .claude/commands/
```

**2. Don't process templates during copy**

The research.md clarifies this explicitly: NO template processing happens during `init`. Templates are copied as-is. Processing (placeholder substitution) happens later when slash commands run.

Both GitHub mode and local mode copy templates without modification.

**3. Permissions matter**

After copying, you MUST call `ensure_executable_scripts()` on the project directory. This is already implemented - just make sure you call it in BOTH branches (GitHub and local).

**4. The `--here` flag interaction**

When `--here` is used with `--local`:
- Don't create a subdirectory
- Merge into current directory
- `dirs_exist_ok=True` parameter handles this
- But you still need the same validation (directory exists check happens before copy)

**5. Path resolution subtlety**

```python
local_path = Path(local).resolve()
```

This is crucial - it:
- Converts relative to absolute
- Expands `~` to home directory
- Normalizes the path
- Do this ONCE at the start, then use `local_path` everywhere

**6. Error message consistency**

All errors use Rich Panel formatting, matching existing CLI style:
```python
console.print(Panel(
    "error message here",
    title="[red]Error Title[/red]",
    border_style="red"
))
raise typer.Exit(1)
```

Don't use plain `print()` or different formatting.

**7. Constitutional compliance**

The plan already verified all 6 principles:
- ✅ Claude-only (no multi-agent logic)
- ✅ No git branch creation
- ✅ Minimal divergence (optional flag, backward compatible)
- ✅ GitHub download still default
- ✅ Version bump required (MINOR - new feature)
- ✅ Using spec-kit methodology (this plan itself)

The implementation must maintain this.

**8. What NOT to do:**

- ❌ Don't add template validation (checking file contents) - too complex, not in spec
- ❌ Don't add file watching or auto-sync - out of scope
- ❌ Don't modify the GitHub download logic - leave it untouched
- ❌ Don't add new slash commands - CLI change only
- ❌ Don't create new bash scripts - reuse existing patterns

---

## **Summary: The Complete Picture**

**In one sentence:** Add a `--local <path>` flag that copies templates from a local spec-kit repository instead of downloading from GitHub, using strict validation and the exact same directory mapping as releases.

**Files changed:** 1 (just `src/specify_cli/__init__.py`)

**Functions added:** 2 (`validate_local_repo`, `copy_local_templates`)

**Functions modified:** 1 (`init` - add parameter and branching logic)

**Tests:** 9 manual scenarios in quickstart.md

**Version bump:** MINOR (new optional feature)

**Risk level:** Low (optional flag, no changes to existing behavior, Layer 1 only)

**Development time estimate:** ~2-3 hours (coding + testing)

---

## Quick Reference

### Key Files
- **Implementation**: `src/specify_cli/__init__.py` (only file to change)
- **Test Plan**: `specs/003-local-to-cmdline/quickstart.md`
- **Contracts**: `specs/003-local-to-cmdline/template-contracts.md`
- **Research**: `specs/003-local-to-cmdline/research.md`

### Directory Mapping
```
templates/*.md           → .specify/templates/
templates/commands/      → .claude/commands/
scripts/bash/            → .specify/scripts/bash/
memory/                  → .specify/memory/
```

### Required Validation
- `templates/` exists
- `templates/commands/` exists
- `scripts/bash/` exists (not just `scripts/`)
- `memory/` exists

### Usage Examples
```bash
# Basic
speclaude init my-project --local /path/to/spec-kit

# With flags
speclaude init --here --local ../spec-kit
speclaude init test --local $(pwd) --no-git
```
