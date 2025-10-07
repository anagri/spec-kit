
# Implementation Plan: Local Development Mode for Template Distribution

**Feature**: `003-local-to-cmdline` | **Date**: 2025-10-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/Users/amir36/Documents/workspace/src/github.com/anagri/spec-kit/specs/003-local-to-cmdline/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code, or `AGENTS.md` for all other agents).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Add `--local <path>` flag to `speclaude init` command to enable developers to test template changes from a local spec-kit repository without creating GitHub releases. The system will validate the local repository structure (requires all three directories: templates/, scripts/, memory/), copy files recursively with proper path mapping (source → installed structure), follow symlinks, and apply the same template processing as the GitHub download flow.

## Technical Context
**Language/Version**: Python 3.11+ (existing codebase)
**Primary Dependencies**: typer (CLI framework), rich (terminal UI), pathlib (filesystem operations), shutil (file copying)
**Storage**: Filesystem only (local repository directories, target project directories)
**Testing**: Manual CLI testing with `uvx --from . specify-cli init` (existing pattern)
**Target Platform**: macOS and Linux (bash-only platforms per constitution)
**Project Type**: CLI/Template/Generator tool (Option 4 structure)
**Performance Goals**: <1s for local file copy operations, O(n) where n=file count
**Constraints**: Must maintain identical behavior to GitHub download mode except for network operations; must respect existing `--here`, `--force`, `--no-git` flags
**Scale/Scope**: ~50-100 files per template repository, recursive directory traversal, symlink resolution

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Claude Code-Only Support
- [x] No multi-agent logic added? ✓ (CLI feature only, no agent-specific code)
- [x] Only bash scripts? ✓ (No new scripts required)
- [x] Only `.claude/commands/` structure? ✓ (No changes to slash commands)

### Principle II: Solo Developer Workflow
- [x] No git branch coupling? ✓ (Feature affects `init` command, not feature workflow)
- [x] No `git checkout -b` added? ✓ (No git logic changes)
- [x] Optional git operations? ✓ (Respects existing `--no-git` flag)

### Principle III: Minimal Divergence from Upstream
- [x] Core workflow unchanged? ✓ (Adds optional flag, doesn't modify existing behavior)
- [x] Template structures preserved? ✓ (No template changes)
- [x] Documented divergence if needed? N/A (No upstream equivalent feature to diverge from)

### Principle IV: GitHub Release Template Distribution
- [x] Default behavior unchanged? ✓ (GitHub download remains default)
- [x] Release packages unaffected? ✓ (No changes to release workflow)
- [ ] **POTENTIAL CONCERN**: `--local` bypasses GitHub download
  - **Justification**: This is intentional for development workflow; users explicitly opt-in with flag
  - **Mitigation**: Clear documentation that `--local` is for template development only

### Principle V: Version Discipline
- [x] Version bump required? ✓ (MINOR version - new feature flag)
- [x] CHANGELOG entry needed? ✓ (New `--local` flag)
- [x] Semantic versioning followed? ✓ (New optional feature = MINOR bump)

### Principle VI: Dogfooding - Self-Application
- [x] Using spec-kit methodology? ✓ (This plan)
- [x] Consult docs/PHILOSOPHY.md? ✓ (Layer 1 CLI modification pattern)
- [x] Aligned with four-layer model? ✓ (Layer 1 change only, no template/script changes)

**Initial Assessment**: PASS with one documented concern (Principle IV bypass is intentional)

**Post-Design Re-evaluation** (after Phase 1):

### Principle I: Claude Code-Only Support
- [x] No multi-agent logic added? ✓ (Implementation in src/specify_cli/__init__.py only)
- [x] Only bash scripts? ✓ (No new scripts, reuses existing validation patterns)
- [x] Only `.claude/commands/` structure? ✓ (No slash command changes)

### Principle II: Solo Developer Workflow
- [x] No git branch coupling? ✓ (No git logic modifications)
- [x] Feature directories independent? ✓ (Affects init only, not feature workflow)

### Principle III: Minimal Divergence from Upstream
- [x] Core workflow unchanged? ✓ (Optional flag, backward compatible)
- [x] Template copying preserved? ✓ (Replicates same path mappings as GitHub mode)
- [x] No upstream equivalent? ✓ (New feature, not divergence)

### Principle IV: GitHub Release Template Distribution
- [x] Default preserved? ✓ (GitHub remains default, --local is opt-in)
- [x] Template source changeable? ✓ (Documented in CLAUDE.md as valid use case)
- [x] Justification documented? ✓ (See research.md Decision 4, quickstart.md purpose statement)

### Principle V: Version Discipline
- [x] MINOR version bump? ✓ (New optional feature flag)
- [x] CHANGELOG entry? ✓ (Planned in tasks.md)
- [x] Semantic versioning? ✓ (v0.2.0 → v0.3.0 or similar)

### Principle VI: Dogfooding
- [x] Using spec-kit methodology? ✓ (This entire planning process)
- [x] Consulted docs/PHILOSOPHY.md? ✓ (See research.md - Layer 1 modification pattern)
- [x] Aligned with four layers? ✓ (Layer 1 CLI change only, no Layer 2/3/4 modifications)
- [x] Phase 1 artifacts conditional? ✓ (Used template-contracts.md, not data-model.md per CLI tool pattern)

**Final Assessment**: PASS - All principles satisfied, implementation stays within Layer 1 boundaries

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md                    # This file (/plan command output)
├── research.md                # Phase 0 output (/plan command)
├── data-model.md              # Phase 1 output (if feature has entities/storage)
├── template-contracts.md      # Phase 1 output (if feature is CLI/template/config)
├── quickstart.md              # Phase 1 output (/plan command)
├── contracts/                 # Phase 1 output (/plan command)
└── tasks.md                   # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
src/
└── specify_cli/
    └── __init__.py        # Single-file CLI implementation
                           # Contains: init(), check(), download_template_from_github()
                           # NEW: validate_local_repo(), copy_local_templates()

templates/                 # SOURCE (edit to distribute)
├── commands/*.md          # Slash command templates
├── spec-template.md
├── plan-template.md
└── tasks-template.md

scripts/
└── bash/                  # Bash automation scripts
    ├── common.sh
    ├── create-new-feature.sh
    └── setup-plan.sh

memory/
└── constitution.md        # Six fork principles

docs/
├── PHILOSOPHY.md          # Four-layer architecture explanation
├── quickstart.md
└── local-development.md

tests/
└── manual/                # Manual CLI testing workflow
    └── test-local-mode.sh # Test script for --local flag
```

**Structure Decision**: CLI/Template/Generator tool (Option 4). This feature modifies only `src/specify_cli/__init__.py` (Layer 1 in architecture). The `--local` flag enables copying from source directories (templates/, scripts/, memory/) to installed locations (.specify/, .claude/) without network operations. No changes to templates, scripts, or memory files required.

## Phase 0: Outline & Research
1. **Consult project documentation FIRST** (constitutional requirement):
   - Read docs/PHILOSOPHY.md for architectural patterns and layer boundaries
   - Read docs/ folder (quickstart.md, local-development.md, installation.md) for workflow context
   - Read CLAUDE.md for project-specific practices and constraints
   - Read existing specs/ for similar feature patterns
   - Only proceed to external research after exhausting internal sources

2. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

3. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

4. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]
   - Internal docs consulted: [list docs/ files and sections referenced]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

**IMPORTANT**: Phase 1 artifacts depend on feature type. Choose appropriate artifacts:

### For Features with Entities/Storage (web apps, mobile apps with databases):
1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

### For CLI/Template/Configuration Features (spec-kit, build tools, generators):
1. **Define template structures** → `template-contracts.md` (instead of data-model.md):
   - Template file formats (markdown, JSON, YAML)
   - Placeholder tokens and substitution rules
   - Directory structure contracts

2. **Generate file/interface contracts** → `/contracts/`:
   - Command-line interface contracts (arguments, outputs)
   - JSON communication schemas (between scripts/templates)
   - File structure contracts (directory layouts, naming conventions)

### Common to All Feature Types:
3. **Generate contract tests** from contracts:
   - One test file per contract
   - Assert schemas/formats/structure
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: (data-model.md OR template-contracts.md), /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
1. **Load base template**: `.specify/templates/tasks-template.md`
2. **Extract from Phase 1 artifacts**:
   - From `template-contracts.md`: CLI interface, directory structure, file copy, error handling contracts
   - From `contracts/function_signatures.py`: Function contracts for `validate_local_repo()`, `copy_local_templates()`, `init()` modification
   - From `quickstart.md`: 9 test scenarios covering all functional requirements

3. **Generate contract test tasks** (TDD - tests first):
   - Task group 1: CLI parameter parsing tests
   - Task group 2: Path validation tests (exists, is_directory, has_required_dirs)
   - Task group 3: File copy behavior tests (recursive, symlinks, permissions)
   - Task group 4: Error handling tests (5 error scenarios from template-contracts.md)
   - Task group 5: Integration tests (flag combinations: --here, --no-git, --force)

4. **Generate implementation tasks** (to make tests pass):
   - Task: Add `local` parameter to `init()` function signature
   - Task: Implement `validate_local_repo()` function
   - Task: Implement `copy_local_templates()` function with path mapping
   - Task: Integrate local mode branch in `init()` execution flow
   - Task: Update progress tracker messages for local mode
   - Task: Add error handling with Rich Panel formatting

5. **Generate validation tasks**:
   - Task: Run quickstart.md scenarios 1-9 manually
   - Task: Update pyproject.toml version (MINOR bump)
   - Task: Add CHANGELOG.md entry
   - Task: Test with `uvx --from . specify-cli init test --local $(pwd)`

**Ordering Strategy**:
- **Phase A: Contract tests** (write all tests first - TDD principle)
  - CLI parsing tests [P]
  - Validation tests [P]
  - Copy behavior tests [P]
  - Error handling tests [P]
  - Integration tests (depends on above)

- **Phase B: Implementation** (make tests pass)
  - `validate_local_repo()` implementation (independent)
  - `copy_local_templates()` implementation (independent)
  - `init()` modification (depends on above two)
  - Progress tracker integration (depends on init modification)
  - Error handling (depends on validation/copy functions)

- **Phase C: Validation & Release**
  - Manual quickstart scenarios (depends on implementation complete)
  - Version bump + CHANGELOG (depends on all tests passing)
  - Final smoke test (depends on version bump)

**Parallelization** (mark with [P]):
- All contract test tasks are parallel (independent test files)
- `validate_local_repo()` and `copy_local_templates()` can be implemented in parallel
- Error scenario tests can run in parallel

**Estimated Output**: 20-25 tasks
- ~13 contract test tasks (TDD)
- ~6 implementation tasks
- ~3 integration/validation tasks
- ~3 release preparation tasks

**Dependencies**:
- Template contracts define test assertions
- Function signatures define implementation interfaces
- Quickstart scenarios define integration test cases
- All tests written BEFORE implementation (strict TDD)

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command) - See research.md
- [x] Phase 1: Design complete (/plan command) - See template-contracts.md, contracts/, quickstart.md
- [x] Phase 2: Task planning complete (/plan command - describe approach only) - See above section
- [ ] Phase 3: Tasks generated (/tasks command) - NOT YET EXECUTED
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS (6/6 principles satisfied)
- [x] Post-Design Constitution Check: PASS (all principles re-verified after Phase 1)
- [x] All NEEDS CLARIFICATION resolved (Technical Context has no unknowns)
- [x] Complexity deviations documented (None - implementation follows standard patterns)

**Artifacts Generated**:
- [x] research.md (8 technical decisions with rationale)
- [x] template-contracts.md (CLI, directory structure, file copy, error handling contracts)
- [x] contracts/function_signatures.py (3 function contracts with TDD stubs)
- [x] quickstart.md (9 test scenarios validating FR-001 through FR-017)
- [x] CLAUDE.md updated (via update-agent-context.sh)

**Ready for /tasks Command**: ✓ Yes - All Phase 0 and Phase 1 artifacts complete

---
*Based on project constitution - See `.specify/memory/constitution.md` for current version*
