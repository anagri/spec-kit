"""
Function Signature Contracts for Local Development Mode

These signatures define the interface contracts for new functions
added to src/specify_cli/__init__.py for --local flag support.

CONTRACT TEST STATUS: All functions should fail tests until implemented (TDD)
"""

from pathlib import Path
from typing import Optional, Tuple
from rich.console import Console


def validate_local_repo(local_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Validate that a local path contains required spec-kit repository structure.

    CONTRACT:
    - Input: Resolved absolute Path object
    - Output: (is_valid: bool, error_message: Optional[str])
    - Checks: templates/, scripts/bash/, memory/ directories exist
    - Checks: templates/commands/ subdirectory exists
    - Returns: (True, None) if valid
    - Returns: (False, "error message") if invalid

    VALIDATION RULES:
    1. Path must exist (checked before calling)
    2. Path must be directory (checked before calling)
    3. Must contain: templates/
    4. Must contain: scripts/bash/ (not just scripts/)
    5. Must contain: memory/
    6. Must contain: templates/commands/
    7. Additional directories/files are allowed (ignored)

    ERROR MESSAGE FORMAT:
    ```
    Invalid spec-kit repository structure

    Missing required directories:
      ✗ templates/commands/
      ✗ memory/

    Found:
      ✓ templates/
      ✓ scripts/bash/
    ```

    EXAMPLES:
    >>> validate_local_repo(Path("/path/to/complete/repo"))
    (True, None)

    >>> validate_local_repo(Path("/path/to/incomplete/repo"))
    (False, "Invalid spec-kit repository structure\\n\\n...")

    TEST REQUIREMENT: Function must not exist yet (TDD)
    """
    raise NotImplementedError("TDD: Implement after tests written")


def copy_local_templates(
    project_path: Path,
    local_path: Path,
    is_current_dir: bool,
    tracker: Optional[object] = None,
) -> None:
    """
    Copy templates from local repository to project directory.

    CONTRACT:
    - Input: project_path (target), local_path (source), is_current_dir (--here flag), tracker (progress)
    - Output: None (side effect: files copied)
    - Behavior: Copies with directory structure mapping
    - Raises: OSError, PermissionError on copy failure

    PATH MAPPING:
    Source                          → Destination
    -------------------------------------------------------------
    local_path/templates/*.md       → project_path/.specify/templates/*.md
    (excludes commands/)

    local_path/templates/commands/  → project_path/.claude/commands/

    local_path/scripts/bash/        → project_path/.specify/scripts/bash/

    local_path/memory/              → project_path/.specify/memory/

    COPY BEHAVIOR:
    - Recursive: All subdirectories preserved
    - Symlinks: Followed (dereferenced), not preserved
    - Dirs exist: OK (merge for --here mode)
    - File count: Tracked and reported via tracker

    PROGRESS TRACKER UPDATES (if tracker provided):
    - tracker.add("copy", "Copy templates from local")
    - tracker.start("copy")
    - tracker.complete("copy", "{file_count} files")
    - tracker.error("copy", str(error)) on failure

    EXCEPTIONS:
    - OSError: File system errors during copy
    - PermissionError: Insufficient permissions
    - All exceptions propagate to caller (init handles error display)

    EXAMPLES:
    >>> copy_local_templates(
    ...     Path("/tmp/my-project"),
    ...     Path("/home/user/spec-kit"),
    ...     is_current_dir=False,
    ...     tracker=StepTracker("test")
    ... )
    # Side effect: Files copied, tracker updated

    TEST REQUIREMENT: Function must not exist yet (TDD)
    """
    raise NotImplementedError("TDD: Implement after tests written")


def init(
    project_name: Optional[str] = None,
    ignore_agent_tools: bool = False,
    no_git: bool = False,
    here: bool = False,
    force: bool = False,
    skip_tls: bool = False,
    debug: bool = False,
    github_token: Optional[str] = None,
    local: Optional[str] = None,  # NEW PARAMETER
) -> None:
    """
    Initialize a new Specify project (MODIFIED CONTRACT).

    NEW CONTRACT ADDITION:
    - Parameter: local (Optional[str]) - Path to local spec-kit repository
    - Default: None (uses GitHub download mode)
    - Behavior: When provided, skips GitHub download, copies from local path
    - Validation: Path resolved, validated, then copied

    EXECUTION FLOW WITH --local:
    1. Show banner
    2. Validate arguments (project_name/--here logic unchanged)
    3. Determine project_path
    4. Check prerequisites (git, claude CLI)
    5. >>> IF local:
           a. Resolve path: local_path = Path(local).resolve()
           b. Validate path exists and is directory (error if not)
           c. Validate repository structure: validate_local_repo(local_path)
           d. Copy templates: copy_local_templates(project_path, local_path, here, tracker)
       >>> ELSE:
           a. Download from GitHub (existing flow)
           b. Extract templates (existing flow)
    6. Ensure scripts executable (SHARED - both modes)
    7. Initialize git (SHARED - both modes)
    8. Display next steps (SHARED - both modes)

    ERROR HANDLING (--local specific):
    - Path not exist → Rich Panel error, Exit(1)
    - Path not directory → Rich Panel error, Exit(1)
    - Invalid repo structure → Rich Panel error (from validate_local_repo), Exit(1)
    - Copy failure → Rich Panel error (from copy_local_templates), Exit(1)

    COMPATIBILITY:
    - --local works with: --here, --no-git, --force, --ignore-agent-tools
    - --local ignored with: --skip-tls, --debug, --github-token (no network ops)

    EXISTING BEHAVIOR PRESERVED:
    - All current parameters unchanged
    - GitHub download mode unaffected when --local not provided
    - Post-copy logic (executable scripts, git init, display) identical

    TEST REQUIREMENT: Function signature change only (implementation tested separately)
    """
    raise NotImplementedError("TDD: Modify existing function signature")


# Contract test helper - expected directory structures
REQUIRED_SOURCE_DIRS = [
    "templates",
    "templates/commands",
    "scripts/bash",
    "memory",
]

TARGET_DIR_MAPPINGS = {
    "templates": ".specify/templates",
    "templates/commands": ".claude/commands",
    "scripts/bash": ".specify/scripts/bash",
    "memory": ".specify/memory",
}
