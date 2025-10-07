# Feature Specification: Local Development Mode for Template Distribution

**Feature ID**: `003-to-command-line`
**Created**: 2025-10-07
**Status**: Draft
**Input**: User description: "to command line, add a flag --local <path> That takes in the path to the local spec-kit repo, and then instead of downloading the artifacts from the `GitHub` releases, it looks into the folders in the repo instead. note that the source folder changes, if downloading from releases, we have .claude/commands from releases, but have templates/commands in the repo, .specify/memory,scripts,templates in releases but these folders are on top in repo"

## Execution Flow (main)
```
1. Parse user description from Input
   → Feature adds local development mode via --local flag
2. Extract key concepts from description
   → Actors: CLI users, developers
   → Actions: Initialize project from local repo
   → Data: File paths, template sources
   → Constraints: Path mapping (source vs release structure)
3. For each unclear aspect:
   → [RESOLVED] Path structure differences documented in input
4. Fill User Scenarios & Testing section
   → Primary: Developer testing template changes without release
5. Generate Functional Requirements
   → All requirements testable via CLI invocations
6. Identify Key Entities
   → Path mappings, source locations
7. Run Review Checklist
   → No tech details leaked, focused on user needs
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

---

## Clarifications

### Session 2025-10-07
- Q: When validating the local path, if only some required directories exist (e.g., templates/ and scripts/ present, but memory/ missing), what should the system do? → A: Fail validation entirely - all three directories must exist
- Q: When copying from scripts/bash/, should the system copy only files directly in that directory, or also include subdirectories and their contents recursively? → A: Recursive copy - all subdirectories and files
- Q: If the local repository contains symbolic links in template/script directories, what should the system do? → A: Follow symlinks - copy target file contents

---

## User Scenarios & Testing

### Primary User Story
As a **spec-kit developer**, when I make changes to templates, scripts, or memory files, I need to test those changes in a real project initialization **without creating a GitHub release**, so I can validate my changes work correctly before publishing.

Currently, developers must create releases to test template changes, which is slow and pollutes the release history with test versions.

### Acceptance Scenarios

1. **Given** I have a local spec-kit repository with modified templates, **When** I run `speclaude init my-project --local /path/to/spec-kit`, **Then** the project should initialize using templates from my local repository instead of downloading from GitHub

2. **Given** I have modified a bash script in `scripts/bash/`, **When** I initialize with `--local`, **Then** the initialized project should contain my modified script in `.specify/scripts/bash/`

3. **Given** I have modified a slash command template in `templates/commands/`, **When** I initialize with `--local`, **Then** the initialized project should contain my modified command in `.claude/commands/`

4. **Given** I provide an invalid local path, **When** I run `speclaude init --local /invalid/path`, **Then** the CLI should show a clear error message explaining the path doesn't exist or isn't a valid spec-kit repository

7. **Given** the local repository has a subdirectory under `scripts/bash/utils/`, **When** I initialize with `--local`, **Then** the initialized project should contain `.specify/scripts/bash/utils/` with all files preserved

8. **Given** the local repository has a symlinked file in `templates/`, **When** I initialize with `--local`, **Then** the symlink target contents should be copied (not the symlink itself)

5. **Given** I use `--local` flag, **When** initialization completes, **Then** no network requests should be made to GitHub (no download, no API calls)

6. **Given** I use both `--local` and existing project path, **When** I run `speclaude init existing-dir --local /path/to/spec-kit`, **Then** the behavior should match current rules (error if directory exists, unless using `--here` with confirmation)

### Edge Cases

- What happens when the local repository is missing required directories (templates/, scripts/, memory/)?
  → System MUST fail validation and show clear error listing which directories are missing

- What happens when local path is relative vs absolute?
  → System should support both, resolving relative paths from current working directory

- What happens when using `--local` with `--here` or `--no-git` flags?
  → All flags should work together normally; --local only affects source of templates

- What happens when local repository has uncommitted changes?
  → System should use whatever files exist, regardless of git status (developer testing scenario)

- What happens when the local repository contains symbolic links?
  → System MUST follow symlinks and copy the target file contents (symlinks are dereferenced)

- What happens when copying subdirectories from scripts/bash/?
  → System MUST copy all subdirectories recursively, maintaining directory structure

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept a new `--local` flag with a path argument on the `init` command

- **FR-002**: System MUST validate that the provided local path exists and is accessible

- **FR-003**: System MUST validate that the local path contains ALL three required directories: `templates/`, `scripts/`, and `memory/`. Validation MUST fail if any directory is missing

- **FR-004**: When `--local` is provided, system MUST skip GitHub release API calls entirely

- **FR-005**: When `--local` is provided, system MUST skip template download from GitHub

- **FR-006**: System MUST copy template files from `<local-path>/templates/` (excluding commands/) to `.specify/templates/` in the target project, including all subdirectories recursively

- **FR-007**: System MUST copy bash scripts from `<local-path>/scripts/bash/` to `.specify/scripts/bash/` in the target project, including all subdirectories and their contents recursively

- **FR-008**: System MUST copy memory files from `<local-path>/memory/` to `.specify/memory/` in the target project, including all subdirectories recursively

- **FR-009**: System MUST copy slash command templates from `<local-path>/templates/commands/` to `.claude/commands/` in the target project, including all subdirectories recursively

- **FR-010**: System MUST apply the same template processing (placeholder substitution, path rewriting) when using local templates as when using downloaded templates

- **FR-011**: System MUST resolve relative paths in `--local` argument relative to the current working directory

- **FR-012**: System MUST accept absolute paths in `--local` argument

- **FR-013**: System MUST display clear error messages when local path is invalid or incomplete

- **FR-014**: System MUST continue to support all existing flags (`--here`, `--no-git`, `--force`, `--ignore-agent-tools`, etc.) when using `--local`

- **FR-015**: System MUST set executable permissions on copied bash scripts when using `--local` (same as release mode)

- **FR-017**: When copying files, system MUST follow symbolic links and copy the target file contents (symlinks are resolved, not preserved)

- **FR-016**: Progress tracker MUST show "Using local templates" instead of "Downloading from GitHub" when `--local` is active

### Key Entities

- **Local Repository Path**: The file system location of a spec-kit repository containing source templates, scripts, and memory files
  - Attributes: absolute or relative path
  - Validation: Must exist, must be directory, must contain expected subdirectories

- **Source Directory Mapping**: The relationship between repository source structure and release structure
  - Repository structure: `templates/`, `scripts/bash/`, `memory/`, `templates/commands/`
  - Release structure: `.specify/templates/`, `.specify/scripts/bash/`, `.specify/memory/`, `.claude/commands/`
  - Mapping rules:
    - `templates/*.md` → `.specify/templates/*.md` (exclude commands/)
    - `templates/commands/*.md` → `.claude/commands/*.md`
    - `scripts/bash/*.sh` → `.specify/scripts/bash/*.sh`
    - `memory/*` → `.specify/memory/*`

- **Template Source**: Abstraction representing where templates come from
  - Types: "GitHub Release" (default) or "Local Repository" (with --local flag)
  - Behavior changes based on type (download vs copy)

---

## Review & Acceptance Checklist

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

---

## Execution Status

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked (none - input was comprehensive)
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [x] Review checklist passed

---
