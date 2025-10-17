# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About This Fork

This is `anagri/spec-kit`, a **Claude Code-only, bash-only, solo-developer fork** of `github/spec-kit`. The CLI is renamed to `speclaude` to differentiate from upstream.

**Key Divergences from Upstream**:
1. Only Claude Code support (no multi-agent logic)
2. Only bash scripts (no PowerShell)
3. No git branch creation for features (solo dev workflow)
4. Downloads templates from `anagri/spec-kit` instead of `github/spec-kit`

**Governance & Architecture Documentation**:
- `.specify/memory/constitution.md` - The six core principles (WHAT) - Version 1.1.0
  - I. Claude Code-Only Support
  - II. Solo Developer Workflow
  - III. Minimal Divergence from Upstream
  - IV. GitHub Release Template Distribution
  - V. Version Discipline (NON-NEGOTIABLE)
  - VI. Dogfooding - Self-Application
- `docs/PHILOSOPHY.md` - Architectural rationale and patterns (WHY & HOW)
- `CLAUDE.md` (this file) - Developer workflow and implementation (WHEN & WHERE)

> **For AI Assistants**:
> - **First time here?** Read `.specify/memory/constitution.md` first to understand the six governing principles.
> - **Making architectural decisions?** Consult `docs/PHILOSOPHY.md` for the four-layer model, design rationale, and extension patterns.
> - **Implementing features?** Use this file (CLAUDE.md) for build commands, testing procedures, and development workflows.
>
> The constitution defines WHAT must be followed. The philosophy explains WHY it's designed this way. This file shows WHEN and WHERE to apply them.

## Build and Development Commands

### Local Testing
```bash
# Test CLI without installing (use current working directory)
uvx --from . specify-cli

# Install locally for persistent testing
uv tool install .
speclaude init test-project

# Uninstall after testing
uv tool uninstall specify-cli
```

### Code Formatting
This is a Python project using hatchling as the build backend. If making significant changes:
```bash
# Use ruff or black for formatting if available
ruff format src/
# or
black src/
```

### Running the CLI
```bash
# Initialize a project (basic usage)
speclaude init my-project

# Initialize in current directory
speclaude init .
# or
speclaude init --here

# Check prerequisites
speclaude check

# Skip Claude Code CLI check (useful during development)
speclaude init test-project --ignore-agent-tools
```

## Architecture Overview

**📖 For Comprehensive Architectural Context**: This section provides implementation-focused guidance. For deep understanding of architectural philosophy, design decisions, and the "why" behind the structure, see [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md).

**Quick Architecture Summary**:
- **Layer 1 (CLI)**: Python orchestrator - hardcoded for Claude Code + bash
- **Layer 2 (Templates)**: Markdown execution flows - constrain Claude's output space
- **Layer 3 (Scripts)**: Bash state automation - no branch creation, JSON communication
- **Layer 4 (Constitution)**: Six principles - runtime validation via template gates

**When to Consult Philosophy**:
- 🏗️ **Making architectural changes**: Understand layer boundaries and constraints
- 🐛 **Debugging complex issues**: See how layers interact via JSON contracts
- 🔧 **Extending functionality**: Learn valid extension patterns vs. anti-patterns
- 🤔 **Questioning design decisions**: Read rationale for fork-specific choices

### Core Components

**1. CLI Entry Point (`src/specify_cli/__init__.py`)**
   - Single Python file containing entire CLI implementation
   - Uses Typer for CLI framework, Rich for terminal UI
   - Hardcoded constants: `AI_AGENT = "claude"`, `SCRIPT_TYPE = "sh"`
   - Special handling for Claude CLI after `migrate-installer` (checks `~/.claude/local/claude`)

**2. Template Distribution System**
   - Templates downloaded from GitHub releases at `anagri/spec-kit`
   - `download_template_from_github()` fetches latest release zip
   - Extracts to project directory with `.specify/` structure
   - See `download_and_extract_template()` for full extraction logic (src/specify_cli/__init__.py:537)

**3. Bash Script Ecosystem (`scripts/bash/`)**
   - `create-new-feature.sh`: Creates `specs/###-feature-name/` directory structure
     - Generates sequential feature IDs (001, 002, 003...)
     - Copies `spec-template.md` to new feature directory
     - **Does NOT create git branches** (solo dev workflow)
     - Sets `SPECIFY_FEATURE` environment variable
   - `update-agent-context.sh`: Maintains `CLAUDE.md` with project info
     - Parses `plan.md` for language/framework/database
     - Updates technology stack sections
     - Preserves manual additions between markers
   - `common.sh`: Shared functions for path resolution and git detection
   - `setup-plan.sh`: Sets up plan.md structure
   - `check-prerequisites.sh`: Validates required tools

**4. Template System (`.specify/templates/`)**
   - `spec-template.md`: Feature specification template
   - `plan-template.md`: Implementation plan template with constitution checks
   - `tasks-template.md`: Task breakdown template (TDD-focused)
   - `agent-file-template.md`: Template for `CLAUDE.md` generation
   - Templates use placeholders: `[FEATURE]`, `[DATE]`, `$ARGUMENTS`

**5. Claude Code Slash Commands (`.claude/commands/`)**
   - `/constitution`: Create/update `.specify/memory/constitution.md`
   - `/clarify-constitution`: Identify and resolve `[NEEDS CLARIFICATION]` markers in constitution (optional)
   - `/specify`: Generate feature spec in `specs/###-feature-name/spec.md`
   - `/clarify`: Ask clarification questions before planning (optional but recommended)
   - `/plan`: Create technical implementation plan
   - `/tasks`: Generate task breakdown from plan
   - `/analyze`: Cross-artifact consistency check (optional but recommended)
   - `/implement`: Execute tasks from tasks.md

   **Command Sequence**:
   - **Required**: `/constitution` → `/specify` → `/plan` → `/tasks` → `/implement`
   - **Optional but recommended**: Run `/clarify-constitution` after `/constitution` if markers exist, `/clarify` after `/specify` before `/plan`, `/analyze` after `/tasks` before `/implement`

   Commands are Markdown files with frontmatter and `$ARGUMENTS` placeholder

## Dogfooding - Self-Application

**Critical Context**: Spec-kit uses itself for development, creating two distinct file sets that serve different purposes.

**Dual File Structure**:

1. **SOURCE** (`templates/`, `memory/`, `scripts/`) - Edit these to change what users receive
2. **INSTALLED** (`.specify/`, `.claude/`) - Frozen snapshot from past install, used via `/specify`, `/plan`, etc.

**Critical Rules**:
- `.specify/` and `.claude/` are **frozen** - do NOT sync or update them when editing source
- To change distribution: Edit `memory/constitution.md`, `templates/`, `scripts/`
- To use spec-kit: Run `/constitution`, `/specify`, `/plan` (uses frozen `.specify/`, `.claude/`)
- Editing `templates/commands/plan.md` does NOT affect `/plan` command (uses `.claude/commands/plan.md`)

**Architecture Changes**: When making significant changes, consult:
- `.specify/memory/constitution.md` for runtime governance principles
- `docs/PHILOSOPHY.md` for layer boundaries and extension patterns
- `CLAUDE.md` (this file) for implementation details

**Example Workflow**:
```bash
# Developing a new feature for spec-kit itself
cd /path/to/spec-kit

# 1. Use INSTALLED templates to spec the feature
/specify "Add support for custom template variables"

# 2. This creates specs/003-custom-variables/ using .claude/commands/specify.md (INSTALLED)

# 3. Later, if implementing template changes:
#    - Edit templates/commands/specify.md (SOURCE)
#    - Test by running: speclaude init test-proj --local .
#    - DO NOT update .claude/commands/specify.md (INSTALLED) directly
```

### Key Workflows

**Release Workflow** (`.github/workflows/release.yml`):
1. Triggered on push to `main` for `templates/`, `scripts/`, `memory/` changes
2. Gets next semantic version from git tags
3. Creates release packages via `create-release-packages.sh`:
   - Copies templates to `.specify/templates/`
   - Uses `find ... -exec cp --parents ...` (GNU coreutils, Ubuntu only)
   - Creates zip: `spec-kit-template-claude-sh-vX.Y.Z.zip`
4. Generates release notes from commit history
5. Creates GitHub release with zip attachment

**Feature Development Flow**:
1. User runs `/specify <description>`
2. Script calls `create-new-feature.sh --json` to create directory
3. Feature created at `specs/###-feature-name/spec.md`
4. User runs `/plan <tech stack>`
5. Creates `plan.md`, `research.md`, `data-model.md`, `contracts/`
6. Script runs `update-agent-context.sh claude` to update `CLAUDE.md`
7. User runs `/tasks` to generate `tasks.md`
8. User runs `/implement` to execute tasks

### Critical Implementation Details

**Repository Root Detection Priority** (scripts/bash/common.sh:5-13, create-new-feature.sh:22-32):
```bash
# NEW: .specify folder has priority over .git for monorepo support
# Traverses upward checking .specify first, then .git, then fallback

get_repo_root() {
    local dir="$(pwd)"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.specify" ]; then echo "$dir"; return 0; fi  # Priority 1
        if [ -d "$dir/.git" ]; then echo "$dir"; return 0; fi      # Priority 2
        dir="$(dirname "$dir")"
    done
    # Fallback to script location
}
```
**Why**: Enables multiple independent spec-kit projects in a single git repository (monorepo workflow).
**Git Boundary**: Stops at first marker found - if `.git` is encountered first, doesn't continue to parent `.specify`.
**Backward Compatible**: Single-project repos work exactly as before.

**Monorepo Support Examples**:
```bash
# Example: Multiple spec-kit projects in a single git repository
my-monorepo/                    # Root git repository
├── .git/
├── project-a/
│   ├── .specify/              # First spec-kit project
│   └── specs/
└── project-b/
    ├── .specify/              # Second spec-kit project
    └── specs/

# Each project-a/ and project-b/ is detected independently
# cd project-a/ → finds .specify/ first (priority 1)
# cd project-b/ → finds .specify/ first (priority 1)
# Both can coexist in the same git repository

# Initialize monorepo setup
cd my-monorepo/project-a
speclaude init --here          # Creates .specify/ in project-a/
cd ../project-b
speclaude init --here          # Creates .specify/ in project-b/
```
See `specs/002-git-folder-priority/quickstart.md` for detailed monorepo setup examples and edge cases.

**Git Branch Removal** (scripts/bash/create-new-feature.sh:74):
```bash
# Feature directory (no branch creation - solo dev workflow)
FEATURE_DIR="$SPECS_DIR/$FEATURE_ID"
mkdir -p "$FEATURE_DIR"
```
Original upstream code had `git checkout -b "$BRANCH_NAME"` here - **removed** per constitution.

**Repo Download Source** (src/specify_cli/__init__.py:426):
```python
def download_template_from_github(...):
    repo_owner = "anagri"  # Changed from "github"
    repo_name = "spec-kit"
```

**Template Pre-processing** (one-time operation, completed):
```bash
# Templates were PRE-PROCESSED once for Claude Code + bash only
# Transformations applied:
# 1. Stripped YAML frontmatter to simple description-only format
# 2. Replaced {SCRIPT} with sh: variant from frontmatter
# 3. Replaced {ARGS} with $ARGUMENTS
# 4. Replaced __AGENT__ with claude
# 5. Rewrote paths: /memory/ → .specify/memory/, etc.
# 6. Skipped leading blank lines after frontmatter

# Script was: .github/workflows/scripts/preprocess-templates-claude-bash.sh
# (removed after one-time use - templates now stored in final form)
```
**Why Pre-process**: Simplifies release workflow and ensures `--local` flag produces identical output to GitHub releases. Templates are stored in their final processed form in the repository. The preprocessing script was run once and removed since templates are now in their final state.

**Template Copy Logic** (.github/workflows/scripts/create-release-packages.sh):
```bash
# SIMPLIFIED: Templates are already pre-processed, just copy as-is
if [[ -d templates ]]; then
  find templates -maxdepth 1 -type f -name "*.md" -exec cp {} "$SPEC_DIR/templates/" \;
fi

if [[ -d templates/commands ]]; then
  cp templates/commands/*.md "$CLAUDE_DIR/commands/" 2>/dev/null || true
fi
```
**Note**: Templates are now stored pre-processed in the repository. If you need to add new command templates, they should be created in their final form (following the pattern in existing `templates/commands/*.md` files).

**Constitution-Driven Development**:
- All architectural decisions must align with `.specify/memory/constitution.md`
- Plan template includes "Constitution Check" gate (plan-template.md:47-50)
- Violations require documented justification in plan's "Complexity Tracking" section

## Version Management (NON-NEGOTIABLE)

**Every change to `src/specify_cli/__init__.py` requires**:
1. Version bump in `pyproject.toml` (line 3)
2. Entry in `CHANGELOG.md` with date and description
3. Follow semantic versioning:
   - MAJOR: Breaking changes (removed commands, changed arguments)
   - MINOR: New features (new commands, new flags)
   - PATCH: Bug fixes, docs, refactoring

**Release Process**:
1. Edit `pyproject.toml`: `version = "X.Y.Z"`
2. Edit `CHANGELOG.md`: Add entry under new `## [X.Y.Z] - YYYY-MM-DD`
3. Commit: `git add -A && git commit -m "chore: bump version to X.Y.Z"`
4. Tag: `git tag vX.Y.Z`
5. Push: `git push && git push --tags`
6. GitHub Actions creates release automatically
7. Verify templates in release logs (look for "deflated XX%" lines)

## File Structure

**Dual Structure**: SOURCE (edit for distribution) + INSTALLED (frozen for dogfooding). See [Dogfooding - Self-Application](#dogfooding---self-application) section above.

```
# SOURCE - Edit these to change what users receive
├── src/specify_cli/__init__.py        # CLI implementation
├── scripts/bash/*.sh                  # Packaged → .specify/scripts/bash/
├── templates/*.md                     # Packaged → .specify/templates/
├── templates/commands/*.md            # Packaged → .claude/commands/
├── memory/constitution.md             # Packaged → .specify/memory/
├── .github/workflows/                 # Release automation
├── pyproject.toml                     # Version, dependencies
└── CLAUDE.md                          # This file

# INSTALLED - Frozen snapshot (do NOT sync with source during development)
├── .specify/                          # Installed templates, scripts, constitution
├── .claude/                           # Installed slash commands
└── specs/###-feature-name/            # Features developed using dogfooding
```

## Testing After Changes

**Before committing changes to `src/specify_cli/__init__.py`**:
```bash
# 1. Test locally
uvx --from . specify-cli init test-proj --ignore-agent-tools
cd test-proj

# 2. Verify directory structure
ls -la .specify/templates/    # Should have 4 .md files
ls -la .specify/scripts/bash/ # Should have 5 .sh files
ls -la .claude/commands/      # Should have 8 .md files (constitution, clarify-constitution, specify, clarify, plan, tasks, analyze, implement)

# 3. Test a script
.specify/scripts/bash/create-new-feature.sh --json "test feature"
# Should output: {"FEATURE_ID":"001-test-feature",...}

# 4. Clean up
cd .. && rm -rf test-proj
```

**Before creating a release**:
```bash
# Test release package creation locally
.github/workflows/scripts/create-release-packages.sh v0.0.99
ls -la .genreleases/
# Should see: spec-kit-template-claude-sh-v0.0.99.zip

# Extract and verify
cd /tmp && unzip -l ~/path/to/spec-kit/.genreleases/spec-kit-template-claude-sh-v0.0.99.zip
# Should show .specify/templates/ with 4 files
```

## Debug and Troubleshooting

### Common Issues and Solutions

**1. Templates not found after init**
```bash
# Verify extraction succeeded
ls -la .specify/templates/
ls -la .claude/commands/

# If empty, check for extraction errors in init output
# Common causes: Network issues, GitHub rate limiting, corrupt zip
```

**2. Template extraction verification**
```bash
# After running init, verify all expected files
tree .specify/ .claude/

# Expected structure:
# .specify/
# ├── memory/
# │   └── constitution.md (template)
# ├── scripts/
# │   └── bash/ (5 .sh files)
# └── templates/ (4 .md files)
# .claude/
# └── commands/ (8 .md files)
```

**3. Script permission errors**
```bash
# If scripts aren't executable, manually fix:
chmod +x .specify/scripts/bash/*.sh

# Verify:
ls -l .specify/scripts/bash/*.sh
# Should show -rwxr-xr-x permissions
```

**4. Slash commands not appearing in Claude Code**
```bash
# Verify .claude/commands/ directory exists and contains files
ls -la .claude/commands/

# If missing, re-run init with --force
speclaude init --here --force

# Restart Claude Code to pick up new commands
```

**5. GitHub rate limiting during download**
```bash
# Use GitHub token for higher rate limits
export GITHUB_TOKEN=ghp_your_token_here
speclaude init my-project

# Or use --github-token flag
speclaude init my-project --github-token ghp_your_token_here

# For offline/air-gapped environments
# 1. Download release zip manually from GitHub releases
# 2. Use --local flag to install from local repository
git clone https://github.com/anagri/spec-kit.git
speclaude init my-project --local /path/to/spec-kit
```

**6. Template processing debugging**
```bash
# Enable debug mode to see detailed extraction logs
speclaude init test-project --debug

# Check for nested directory flattening messages
# Templates are pre-processed - no runtime transformation occurs
```

**7. Monorepo root detection issues**
```bash
# Verify which directory is detected as root
cd your-project/
.specify/scripts/bash/common.sh  # Source this to test get_repo_root()

# Or check manually
pwd
# Should be at the directory containing .specify/ (highest priority)
```

**8. Constitution or template markers not resolving**
```bash
# Check for [NEEDS CLARIFICATION] markers
grep -r "NEEDS CLARIFICATION" .specify/memory/constitution.md

# Run /clarify-constitution to resolve them
# Or manually edit the constitution file
```

## Common Development Tasks

### Adding a New Slash Command Template
1. Create `templates/commands/newcommand.md` with frontmatter:
   ```markdown
   ---
   description: "What this command does"
   ---

   Command prompt here. Use $ARGUMENTS for user input.
   Reference {SCRIPT} for bash script paths.
   ```
2. Update `.github/workflows/scripts/create-release-packages.sh` if needed
3. Test with `uvx --from . specify-cli init test` and verify command appears

### Modifying Bash Scripts
- Always test with `bash -n script.sh` (syntax check) first
- Remember: These scripts support `--no-git` repos (use `find_repo_root()`)
- Test both with git and without: `git init` vs `rm -rf .git`
- Scripts use `set -e` - failures will exit immediately

### Changing Template Content
- Templates live in `templates/` (source)
- Copied to `.specify/templates/` during project init
- Changes require new release for users to get updates
- Test template rendering: Initialize project and check output files

## Alignment with Upstream

When pulling changes from `github/spec-kit`:
1. Check constitution for allowed divergence areas
2. Never change template copy logic in `create-release-packages.sh`
3. Avoid changes to core spec-driven workflow (spec → plan → tasks → implement)
4. Agent-specific code must stay Claude-only
5. PowerShell scripts should be ignored/deleted
6. Document any necessary divergence in this file

## Special Notes

- **📖 Architectural Philosophy**: See [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md) for:
  - Deep dive into the four-layer separation model
  - Constitutional enforcement patterns and gates
  - Fork-specific design rationale (why Claude-only, bash-only, no-branches)
  - Valid extension patterns for slash commands, scripts, and templates
  - Critical insights: templates as constraint functions, JSON as state boundary
- **Claude CLI Path**: After `claude migrate-installer`, binary moves to `~/.claude/local/claude`. The `check_tool()` function handles this (src/specify_cli/__init__.py:366-377).
- **Step Tracker**: Custom Rich-based UI component for progress display (src/specify_cli/__init__.py:87-172). Uses circles (●/○) without emojis.
- **Template Extraction**: Handles GitHub-style zips with nested directories. Flattens structure automatically (src/specify_cli/__init__.py:649-664).
- **Script Permissions**: `ensure_executable_scripts()` sets `+x` on all `.sh` files recursively (POSIX only, no-op on Windows).
- **Templates are Pre-Processed**: All templates in `templates/` directory are stored in their final processed form. No runtime transformation occurs during installation. This was a one-time operation to simplify the release workflow and ensure `--local` flag produces identical output to GitHub releases.
