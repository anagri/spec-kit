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
- `.specify/memory/constitution.md` - The six core principles (WHAT)
- `docs/PHILOSOPHY.md` - Architectural rationale and patterns (WHY & HOW)
- `CLAUDE.md` (this file) - Developer workflow and implementation (WHEN & WHERE)

> **For AI Assistants**: When making architectural decisions or debugging complex issues, consult `docs/PHILOSOPHY.md` for the four-layer model, design rationale, and extension patterns. The philosophy document explains WHY the architecture is designed this way, not just WHAT it does.

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
   - `/specify`: Generate feature spec in `specs/###-feature-name/spec.md`
   - `/clarify`: Ask clarification questions before planning
   - `/plan`: Create technical implementation plan
   - `/tasks`: Generate task breakdown from plan
   - `/analyze`: Cross-artifact consistency check
   - `/implement`: Execute tasks from tasks.md
   - Commands are Markdown files with frontmatter and `$ARGUMENTS` placeholder

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

**Template Copy Logic** (.github/workflows/scripts/create-release-packages.sh):
```bash
# MUST match upstream exactly - uses GNU cp --parents
[[ -d templates ]] && {
  mkdir -p "$SPEC_DIR/templates";
  find templates -type f -not -path "templates/commands/*" -exec cp --parents {} "$SPEC_DIR"/ \; ;
  echo "Copied templates -> .specify/templates";
}
```
**Do not rewrite this logic** - it must stay aligned with upstream.

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

```
.
├── src/specify_cli/
│   └── __init__.py           # Entire CLI implementation (1013 lines)
├── scripts/bash/             # Feature and agent management scripts
│   ├── create-new-feature.sh # Creates specs/###-feature-name/
│   ├── update-agent-context.sh # Updates CLAUDE.md with project info
│   ├── common.sh             # Shared utility functions
│   ├── setup-plan.sh         # Sets up plan.md structure
│   └── check-prerequisites.sh # Tool validation
├── templates/                # Markdown templates for specs/plans/tasks
│   ├── spec-template.md
│   ├── plan-template.md
│   ├── tasks-template.md
│   └── agent-file-template.md
├── memory/                   # Project-wide memory (constitution)
│   └── constitution.md
├── .github/workflows/
│   ├── release.yml           # Auto-release on template changes
│   └── scripts/              # Release automation scripts
│       ├── create-release-packages.sh  # Creates zip files
│       ├── create-github-release.sh
│       └── get-next-version.sh
├── pyproject.toml            # Package config, version, dependencies
├── CHANGELOG.md              # Version history (required updates)
└── CLAUDE.md                 # This file
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
ls -la .claude/commands/      # Should have 7 .md files

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

## Dogfooding

This project uses spec-kit to develop spec-kit itself:
- Constitution at `.specify/memory/constitution.md`
- Features should go in `specs/###-feature-name/`
- Use slash commands: `/constitution`, `/specify`, `/plan`, `/tasks`, `/implement`
- Follow the same workflow we provide to users
