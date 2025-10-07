# Research: Local Development Mode Implementation

**Feature**: 003-local-to-cmdline
**Date**: 2025-10-07
**Purpose**: Research technical decisions for `--local <path>` flag implementation

## Internal Documentation Consulted

### docs/PHILOSOPHY.md (Layer 1: CLI Orchestrator)
**Section**: Layer 1: CLI Orchestrator (lines 64-115)

**Key Findings**:
- CLI is in `src/specify_cli/__init__.py` - single Python file
- Core functions: `init()`, `check()`, `download_template_from_github()`, `ensure_executable_scripts()`
- Hardcoded constants: `AI_AGENT = "claude"`, `SCRIPT_TYPE = "sh"`, `repo_owner = "anagri"`
- Bootstrap flow: Parse args → Validate prerequisites → Fetch release → Download zip → Extract → chmod +x → Init git

**Modification Pattern** (lines 104-109):
> - **Change bootstrap behavior**: Modify `init()` function, respect `--here` and `--force` flags
> - **Custom template source**: Override `download_template_from_github()` repo/owner constants
> - **Add validation**: Extend `check()` with new prerequisite checks

**Principle Preservation** (lines 111-114):
> - Never modify templates during installation (downloaded as-is from releases)
> - Respect `.claude/` directory convention
> - Maintain JSON communication contract with scripts

**Conclusion**: `--local` flag should be added as a parameter to `init()`, create alternate code path that skips `download_template_from_github()` and uses local file copy instead.

### docs/PHILOSOPHY.md (Layer Interaction Model)
**Section**: Example: `/specify` Command (No-Branch Workflow) (lines 377-403)

**Key Insight**:
> **Key Insight**: Layers communicate through **immutable JSON contracts**. Scripts never read Claude-generated content; Claude never executes git commands. This prevents state corruption.

**Application**: Local template copying must maintain same separation - CLI handles filesystem operations, produces same directory structure as GitHub download mode.

### CLAUDE.md (Architecture Overview)
**Section**: Core Components → CLI Entry Point (lines 16-35)

**Key Findings**:
- Single Python file: `src/specify_cli/__init__.py`
- Uses Typer for CLI, Rich for terminal UI
- Special handling for Claude CLI at `~/.claude/local/claude`
- Template distribution from `anagri/spec-kit` GitHub releases

**Section**: Template Distribution System (lines 37-48)

**Path Mapping Discovery**:
```
SOURCE REPO              RELEASE ZIP             INSTALLED
templates/            →  .specify/templates/  →  project/.specify/templates/
templates/commands/   →  .claude/commands/    →  project/.claude/commands/
scripts/bash/         →  .specify/scripts/bash/ → project/.specify/scripts/bash/
memory/               →  .specify/memory/     →  project/.specify/memory/
```

**Conclusion**: Local mode must replicate this exact mapping.

### Existing Specs Pattern Analysis
**File**: `specs/002-git-folder-priority/` (consulted for similar filesystem feature)

**Pattern Observed**:
- Spec focuses on WHAT (behavior), not HOW (implementation)
- Plan includes research.md with architecture consultation
- Implementation constrained by constitutional principles

**Application**: Follow same pattern for `--local` feature.

---

## Technical Decisions

### Decision 1: Path Validation Strategy
**Chosen**: Strict validation requiring all three directories (templates/, scripts/, memory/)

**Rationale**:
- Spec clarification Q1 answer: "Fail validation entirely - all three directories must exist"
- Prevents partial initialization that could cause confusing errors
- Clear error message guides users to fix repository structure

**Alternatives Considered**:
- Partial copy (copy only what exists) - REJECTED: Could hide missing directories, cause runtime failures
- Warn and continue - REJECTED: Creates ambiguous state, violates fail-fast principle

**Internal Docs Consulted**: docs/PHILOSOPHY.md Layer 1 validation patterns

---

### Decision 2: Recursive Copy Strategy
**Chosen**: Recursive directory traversal using `shutil.copytree()` with `dirs_exist_ok=True`

**Rationale**:
- Spec clarification Q2 answer: "Recursive copy - all subdirectories and files"
- Python's `shutil.copytree()` handles directory trees efficiently
- `dirs_exist_ok=True` supports `--here` mode (merge with existing directory)
- Maintains directory structure automatically

**Alternatives Considered**:
- Flat copy only - REJECTED: Spec requires subdirectory preservation
- Manual recursion with `os.walk()` - REJECTED: Reinvents built-in functionality
- `cp -r` via subprocess - REJECTED: Platform-specific, harder error handling

**Internal Docs Consulted**: Python pathlib/shutil documentation (standard library)

---

### Decision 3: Symlink Handling
**Chosen**: Follow symlinks (dereference) using `shutil.copytree(symlinks=False)`

**Rationale**:
- Spec clarification Q3 answer: "Follow symlinks - copy target file contents"
- Default `symlinks=False` parameter in `shutil.copytree()` dereferences symlinks
- Ensures copied files are complete and independent of source repository
- Prevents broken symlinks in target project

**Alternatives Considered**:
- Preserve symlinks (`symlinks=True`) - REJECTED: Could create broken links if targets outside repo
- Skip symlinks - REJECTED: Would silently omit files
- Error on symlinks - REJECTED: Unnecessary friction for common development pattern

**Internal Docs Consulted**: Python shutil documentation

---

### Decision 4: Integration with Existing Code Flow
**Chosen**: Branch at beginning of `init()`, share post-copy logic

**Code Structure**:
```python
def init(..., local: str = None):
    # ... existing validation ...

    if local:
        # NEW: Local mode path
        local_path = Path(local).resolve()
        validate_local_repo(local_path)  # Check directories exist
        copy_local_templates(project_path, local_path, here, tracker)
    else:
        # EXISTING: GitHub download mode
        download_and_extract_template(project_path, ...)

    # SHARED: Post-copy operations
    ensure_executable_scripts(project_path, tracker)
    # ... git init, display next steps ...
```

**Rationale**:
- Minimizes code duplication (shared post-copy logic)
- Clear separation of concerns (local vs remote)
- Reuses existing `ensure_executable_scripts()`, git init, progress tracking
- Respects philosophy principle: "Never modify templates during installation"

**Alternatives Considered**:
- Separate function chain - REJECTED: Duplicates post-copy logic
- Modify `download_and_extract_template()` - REJECTED: Conflates download and copy concerns

**Internal Docs Consulted**: docs/PHILOSOPHY.md Layer 1 modification pattern

---

### Decision 5: Progress Tracker Integration
**Chosen**: Reuse existing `StepTracker` class with local-specific messages

**Implementation**:
```python
if local:
    tracker.add("validate", "Validate local repository")
    tracker.start("validate")
    # validation logic
    tracker.complete("validate", "3 directories found")

    tracker.add("copy", "Copy templates from local repo")
    tracker.start("copy")
    # copy logic
    tracker.complete("copy", f"{file_count} files")
else:
    tracker.add("fetch", "Fetch latest release")
    # ... existing logic ...
```

**Rationale**:
- Consistent user experience (same progress display format)
- Spec requirement FR-016: "Progress tracker MUST show 'Using local templates' instead of 'Downloading from GitHub'"
- Reuses existing `StepTracker` infrastructure

**Alternatives Considered**:
- Silent copy - REJECTED: No user feedback for potentially slow operation
- Print statements - REJECTED: Inconsistent with existing Rich-based UI

**Internal Docs Consulted**: src/specify_cli/__init__.py lines 87-172 (StepTracker implementation)

---

### Decision 6: Error Handling Strategy
**Chosen**: Fail fast with descriptive Rich Panel error messages

**Pattern** (matching existing code):
```python
if not local_path.exists():
    console.print(Panel(
        f"Local path '[cyan]{local_path}[/cyan]' does not exist\n"
        "Provide a valid path to a spec-kit repository.",
        title="[red]Invalid Local Path[/red]",
        border_style="red"
    ))
    raise typer.Exit(1)
```

**Rationale**:
- Consistent with existing error handling (see init() directory conflict handling)
- Spec requirement FR-013: "System MUST display clear error messages when local path is invalid or incomplete"
- Rich Panel provides visual hierarchy and readability

**Alternatives Considered**:
- Simple print statements - REJECTED: Less visual impact
- Exceptions without user-friendly formatting - REJECTED: Poor UX
- Warning and continue - REJECTED: Violates fail-fast principle

**Internal Docs Consulted**: src/specify_cli/__init__.py lines 806-816 (existing error pattern)

---

### Decision 7: Path Resolution Strategy
**Chosen**: Resolve relative paths using `Path(local).resolve()` from current working directory

**Implementation**:
```python
local_path = Path(local).resolve()  # Handles both relative and absolute
```

**Rationale**:
- Spec requirements FR-011 (relative paths) and FR-012 (absolute paths)
- Python's `Path.resolve()` handles both cases automatically
- Converts to absolute path for consistent downstream processing
- Works correctly with `~` expansion

**Alternatives Considered**:
- Manual relative path handling - REJECTED: Error-prone, reinvents pathlib
- Only support absolute paths - REJECTED: Violates spec requirement FR-011
- `os.path.abspath()` - REJECTED: Older API, pathlib is preferred

**Internal Docs Consulted**: Python pathlib documentation

---

### Decision 8: Template Processing Application
**Chosen**: NO template processing in local mode (copy as-is)

**Rationale**:
- docs/PHILOSOPHY.md principle: "Never modify templates during installation (downloaded as-is from releases)"
- Templates are copied to `.specify/templates/` and `.claude/commands/` WITHOUT modification
- Template processing (placeholder substitution) happens when slash commands are executed, not during init
- GitHub download mode doesn't process templates either - they're extracted as-is from zip

**Spec Requirement FR-010 Clarification**:
> "System MUST apply the same template processing (placeholder substitution, path rewriting) when using local templates as when using downloaded templates"

**Interpretation**: Both modes copy templates without processing. The spec means "treat local templates identically to downloaded templates" (no processing in either case during init).

**Alternatives Considered**:
- Process templates during copy - REJECTED: Violates philosophy, not done in GitHub mode
- Different handling for local vs remote - REJECTED: Violates spec requirement FR-010

**Internal Docs Consulted**:
- docs/PHILOSOPHY.md lines 111-114 (principle preservation)
- .github/workflows/scripts/create-release-packages.sh (template processing happens during release creation, not installation)

---

## Summary

**All Technical Context Items Resolved**: ✓

| Item | Status | Decision |
|------|--------|----------|
| Path validation | ✓ Resolved | Strict (all 3 directories required) |
| Recursive copy | ✓ Resolved | `shutil.copytree()` with recursion |
| Symlink handling | ✓ Resolved | Follow symlinks (`symlinks=False`) |
| Code integration | ✓ Resolved | Branch early, share post-copy logic |
| Progress tracking | ✓ Resolved | Reuse `StepTracker` with local messages |
| Error messages | ✓ Resolved | Rich Panel format (existing pattern) |
| Path resolution | ✓ Resolved | `Path.resolve()` for both relative/absolute |
| Template processing | ✓ Resolved | No processing (copy as-is, matches GitHub mode) |

**Primary Sources**:
1. docs/PHILOSOPHY.md (Layer 1 modification patterns, principles)
2. CLAUDE.md (path mappings, architecture)
3. src/specify_cli/__init__.py (existing code patterns)
4. Spec clarifications (Q1-Q3 answers)

**External Sources**: None required (all decisions made from internal documentation)

**Ready for Phase 1**: Yes - all unknowns resolved, architecture understood, implementation approach defined.
