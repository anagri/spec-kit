<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.0.1 (PATCH - clarification removal)
Modified Principles:
  - Principle IV (GitHub Release Template Distribution) - Removed note about offline-first bundled templates request
Added Sections: None
Removed Sections: None
Templates Status:
  ✅ .specify/templates/plan-template.md - Aligned (Constitution Check section)
  ✅ .specify/templates/spec-template.md - Aligned (no constitutional constraints on specs)
  ✅ .specify/templates/tasks-template.md - Aligned (TDD principles reflected)
  ✅ CLAUDE.md - Aligned (references constitution, describes GitHub release distribution accurately)
  ⚠ templates/plan-template.md - Needs version reference fix (references v2.1.1, should be generic)
  ⚠ .specify/templates/plan-template.md - Needs version reference fix (references v2.1.1, should be generic)
Related Docs Updated:
  ⚠ docs/PHILOSOPHY.md - Needs update to affirm GitHub releases as architectural decision (not mitigation)
Follow-up TODOs:
  - Update plan template version references to use generic "latest version" text
  - Update PHILOSOPHY.md to remove bundled templates suggestion
-->

# Spec Kit Constitution

## Core Principles

### I. Claude Code-Only Support

This project MUST support only Claude Code as the AI coding assistant. All agent-specific
code, templates, workflows, and documentation MUST be tailored exclusively for Claude Code
using bash scripts.

**Rationale**: Simplifies maintenance, reduces complexity, and allows focused optimization
for a single workflow. Multi-agent support creates unnecessary branching logic and testing
burden.

**Enforcement**:
- No `--ai` CLI flags or agent selection logic
- CLI binary named `speclaude` to differentiate from upstream
- Only `.claude/commands/` directory structure
- Only bash scripts in `.specify/scripts/bash/` (no PowerShell)
- Release workflow creates only `claude-sh` packages

### II. Solo Developer Workflow

This project MUST NOT couple feature development to git branch workflows. Feature IDs and
specifications exist independently of git branches.

**Rationale**: Solo developers often work directly on main/master without feature branches.
Forcing branch creation adds friction and complexity for the primary use case.

**Enforcement**:
- `create-new-feature.sh` MUST NOT execute `git checkout -b`
- Feature directories created in `specs/###-feature-name/` without branch coupling
- No BRANCH_NAME variable in scripts
- Git operations remain optional (`--no-git` flag support)

### III. Minimal Divergence from Upstream

Changes to this fork MUST be limited to: (1) removing multi-agent support, (2) removing
PowerShell support, (3) removing git branch creation, and (4) changing download source to
`anagri/spec-kit`. All other functionality MUST align with `github/spec-kit`.

**Rationale**: Easier to pull improvements from upstream. Large divergence creates
maintenance burden and loses benefit of upstream evolution.

**Enforcement**:
- `.github/workflows/` changes only for agent/script removal
- Template copying logic matches upstream exactly (use `cp --parents`)
- Core spec-driven development workflow unchanged
- Document any necessary divergence in CLAUDE.md with justification

### IV. GitHub Release Template Distribution

Templates MUST be distributed via GitHub release packages downloaded from `anagri/spec-kit`
repository. The CLI downloads release zips, not bundled templates.

**Rationale**: Allows updating templates without CLI version changes. Users get latest
templates automatically. Simpler than bundling templates in Python package.

**Enforcement**:
- `download_template_from_github()` uses `repo_owner = "anagri"`
- Release workflow MUST include all template files in `.specify/templates/`
- Verify template files present in release zip logs (non-zero deflation percentage)
- No bundled templates in `src/specify_cli/` package

### V. Version Discipline (NON-NEGOTIABLE)

Every change to `src/specify_cli/__init__.py` MUST increment version in `pyproject.toml`
and add entry to `CHANGELOG.md`. Releases MUST follow semantic versioning.

**Rationale**: Clear version history enables debugging, rollback, and user communication.
Undocumented changes create confusion and break trust.

**Enforcement**:
- MAJOR: Breaking CLI changes (removed commands, changed arguments)
- MINOR: New features (new commands, new options)
- PATCH: Bug fixes, documentation, internal refactoring
- CHANGELOG entries MUST include: version, date, changes, rationale
- No releases without version bump + CHANGELOG update

### VI. Dogfooding - Self-Application

This project MUST use spec-kit methodology to develop spec-kit itself. All significant
features MUST follow: `/constitution` → `/specify` → `/plan` → `/tasks` → `/implement`.

**Rationale**: Validates the methodology works for real projects. Surfaces UX issues and
workflow gaps. Ensures tools remain practical and usable.

**Enforcement**:
- Specs directory at `specs/` for all features
- Constitution updated before architectural changes
- Complex features require spec.md and plan.md
- Templates tested on spec-kit development
- CLAUDE.md updated with spec-kit-specific practices

## Technology Constraints

**Language**: Python 3.11+ with minimal dependencies (typer, rich, httpx, platformdirs,
readchar, truststore)

**Package Manager**: uv for installation (`uv tool install` and `uvx` patterns)

**Shell Scripts**: bash only, no PowerShell, no zsh-specific features

**AI Agent**: Claude Code CLI exclusively

**Build System**: hatchling (build backend defined in pyproject.toml)

**Distribution**: GitHub releases with zip packages containing templates and scripts

**Platform Support**: macOS and Linux (Windows via WSL/Git Bash, not native PowerShell)

## Development Workflow

**Local Development**:
- Test CLI with `uvx --from . specify-cli` before releasing
- Verify release packages locally before pushing tags
- Use `cargo fmt` equivalent for Python (ruff/black) if applicable
- Follow user's CLAUDE.md preferences (no auto git commits)

**Release Process**:
1. Update version in `pyproject.toml`
2. Add CHANGELOG.md entry with date and changes
3. Commit changes: `git add -A && git commit -m "chore: bump version to X.Y.Z"`
4. Tag release: `git tag vX.Y.Z`
5. Push with tags: `git push && git push --tags`
6. GitHub Actions creates release package automatically
7. Verify release artifact contains templates (check logs for deflation %)
8. Test installation: `uvx --from git+https://github.com/anagri/spec-kit.git specify-cli`

**Quality Gates**:
- Templates MUST appear in release zip with non-zero compression
- CLI MUST work via `uvx --from .` locally
- No empty release packages allowed
- Release workflow logs MUST show template file additions

**Constitution Alignment**:
- All changes reviewed against these principles
- Divergence from upstream requires documented justification
- Complexity must be justified against simpler alternatives

## Governance

**Amendment Process**:
- Constitution changes require updating `.specify/memory/constitution.md`
- Version bump follows semantic versioning (MAJOR for principle removal/redefinition,
  MINOR for new principles, PATCH for clarifications)
- Impact report generated at top of constitution file
- Dependent templates updated for consistency

**Compliance**:
- All development decisions evaluated against Core Principles
- Violations require documented justification in specs/plans
- Simplicity preferred over feature sprawl
- User preferences in CLAUDE.md respected (no git auto-commits, etc.)

**Supersedence**:
- This constitution supersedes conflicting practices
- When upstream conflicts with principles, fork diverges with documentation
- Principles guide all architectural and implementation decisions

**Version**: 1.0.1 | **Ratified**: 2025-10-05 | **Last Amended**: 2025-10-05
