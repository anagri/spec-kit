# Feature Specification: Prioritize .specify Folder for Repository Root Detection

**Feature ID**: `002-git-folder-priority`
**Created**: 2025-10-06
**Status**: Draft
**Input**: User description: "git folder priority for project root we want to remove the reorg the priority of Finding the project route using the .git folder we want to place more priority on finding the .specify folder insteadOf .git folder this helps to have multiple spec-it bootstrapping, especially for a mono-repo."

## Execution Flow (main)
```
1. Parse user description from Input
   → Extracted: Change repo root detection priority from .git to .specify
2. Extract key concepts from description
   → Actors: Developers using spec-kit in monorepos or multi-project environments
   → Actions: Detect repository root, initialize spec-kit in subdirectories
   → Data: File system markers (.specify, .git folders)
   → Constraints: Must maintain backward compatibility with existing repos
3. For each unclear aspect:
   → Behavior when both .specify and .git exist at different levels
   → Backward compatibility requirements
   → Non-git repo support preservation
4. Fill User Scenarios & Testing section
   → Monorepo scenario: Multiple .specify folders in single git repo
   → Single-project scenario: Traditional repo with one .specify
   → No-git scenario: Existing --no-git workflow
5. Generate Functional Requirements
   → Change priority order in repo root detection
   → Preserve fallback behavior
   → Maintain consistency across all bash scripts
6. Identify Key Entities
   → Repository root (file system location)
   → Project markers (.specify, .git folders)
7. Run Review Checklist
   → Implementation-agnostic specification
   → Testable requirements
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a developer working in a monorepo with multiple independent projects, I want to initialize spec-kit in a subdirectory and have it recognize that subdirectory as the project root (not the git repository root), so that each project can maintain its own specifications independently without interfering with other projects in the same repository.

### Acceptance Scenarios

1. **Given** a git repository with multiple subdirectories (monorepo structure),
   **When** I initialize spec-kit in subdirectory `project-a/` (creating `.specify` folder),
   **Then** all spec-kit commands run from `project-a/` or its subdirectories MUST resolve `project-a/` as the repository root, not the git root

2. **Given** a traditional single-project repository with both `.git` and `.specify` at the same location,
   **When** I run any spec-kit command,
   **Then** the system MUST detect the repository root correctly (no behavior change from current implementation)

3. **Given** a repository initialized with `--no-git` (only `.specify` folder exists),
   **When** I run any spec-kit command,
   **Then** the system MUST continue to work exactly as it does today (backward compatibility)

4. **Given** nested `.specify` folders (e.g., `project-a/.specify` and `project-a/submodule/.specify`),
   **When** I run a command from `project-a/submodule/`,
   **Then** the system MUST use the closest parent `.specify` folder (`project-a/submodule/.specify`), not the higher-level one

5. **Given** a subdirectory with `.specify` folder inside a git repository (where `.git` is at a higher level),
   **When** the system searches for repository root,
   **Then** it MUST find the `.specify` folder first, before checking for `.git`

### Edge Cases

- What happens when `.specify` folder exists but is empty or corrupted?
  → System should treat it as a valid marker for repository root (no validation of contents during root detection)

- What happens when neither `.specify` nor `.git` exists in any parent directory?
  → System should fail with clear error message (existing behavior, must be preserved)

- What happens when running commands from outside any `.specify` project but inside a git repo?
  → System should fall back to git root detection (current behavior for non-spec-kit projects)

- What happens when `.git` and `.specify` exist at different directory levels?
  → System should use the closest `.specify` folder, regardless of `.git` location

- What happens when traversing upward finds `.git` folder (with no `.specify` at that level), but `.specify` exists at a higher parent directory?
  → System should stop at the directory containing `.git` and return that as project root. Once any project marker (`.git` or `.specify`) is found, traversal stops - the system does not continue searching parent directories for a different marker type (this prevents escaping git repository boundaries)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST check for `.specify` folder in parent directory hierarchy BEFORE checking for `.git` folder when determining repository root

- **FR-002**: System MUST still use `.git` folder as a valid repository root marker when `.specify` folder is not found in the directory hierarchy

- **FR-003**: System MUST traverse parent directories from the current working directory upward, stopping at the first occurrence of either `.specify` or `.git` folder (with `.specify` taking priority)

- **FR-004**: All bash scripts in `.specify/scripts/bash/` MUST use the same prioritized repository root detection logic consistently

- **FR-005**: System MUST continue to support repositories initialized with `--no-git` option (no regression in non-git workflow)

- **FR-006**: When multiple `.specify` folders exist in nested directories, system MUST use the closest parent `.specify` folder to the current working directory

- **FR-007**: System MUST return an error when neither `.specify` nor `.git` markers are found in any parent directory up to filesystem root

- **FR-008**: The change in priority MUST NOT break existing single-project repositories where `.specify` and `.git` coexist at the same level

### Key Entities *(include if feature involves data)*

- **Repository Root**: The top-level directory of a spec-kit project, identified by the presence of a `.specify` folder (primary marker) or `.git` folder (fallback marker)

- **Project Marker**: A special folder (`.specify` or `.git`) that indicates a project boundary in the filesystem

- **Monorepo**: A single git repository containing multiple independent projects, each with its own `.specify` folder in separate subdirectories

### Non-Functional Requirements

- **NFR-001**: The repository root detection MUST NOT add noticeable latency to script execution (maintain current performance)

- **NFR-002**: The change MUST be backward compatible with existing spec-kit projects (no migration required)

- **NFR-003**: Error messages when repository root cannot be determined MUST be clear and actionable

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

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
  **Scope**: Change priority order in repository root detection logic; does NOT include changes to initialization logic, template distribution, or other CLI commands
- [x] Dependencies and assumptions identified
  **Dependencies**: Existing bash scripts in `.specify/scripts/bash/` use repository root detection
  **Assumptions**: `.specify` folder is a reliable marker for spec-kit project root

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked (0 remaining)
- [x] User scenarios defined (5 scenarios)
- [x] Requirements generated (8 functional + 3 non-functional)
- [x] Entities identified (3 key entities)
- [x] Review checklist passed

---
