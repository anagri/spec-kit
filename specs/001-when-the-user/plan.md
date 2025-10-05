
# Implementation Plan: Constitution Command Clarification Flow

**Feature**: `001-when-the-user` | **Date**: 2025-10-05 | **Spec**: [specs/001-when-the-user/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-when-the-user/spec.md`

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
Enhance the `/constitution` command to prevent hallucinated constitutions by requiring iterative clarification from users before generation. Introduce a new `/clarify-constitution` command that follows the same pattern as `/clarify` for specs, asking targeted questions about principles, tech stack, workflow, and governance before allowing final constitution generation.

## Technical Context
**Language/Version**: Markdown templates (Claude Code slash commands)
**Primary Dependencies**: Existing `/constitution` and `/clarify` command patterns, bash scripts for path resolution
**Storage**: File system (`.specify/memory/constitution.md`)
**Testing**: Manual validation via slash command execution, contract tests for JSON output, integration tests for workflow
**Target Platform**: Claude Code CLI on macOS/Linux (bash-only fork)
**Project Type**: CLI/Template/Generator tool (spec-kit itself)
**Performance Goals**: Interactive response time <2s for question generation, constitution generation <5s
**Constraints**: Must follow constitutional principles (Claude Code-only, bash-only, solo dev workflow), must not break existing `/constitution` or `/clarify` workflows
**Scale/Scope**: Single new command template + modifications to existing constitution template, ~100-150 lines of markdown template code

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Claude Code-Only Support
- [x] No multi-agent logic introduced (only templates for Claude Code `.claude/commands/`)
- [x] Only bash scripts used (no PowerShell)
- [x] Templates use Claude-specific patterns (execution flows, markdown structure)

### Principle II: Solo Developer Workflow
- [x] No git branch coupling (feature works independently of branches)
- [x] No branch creation in any new scripts
- [x] Works in `--no-git` environments

### Principle III: Minimal Divergence from Upstream
- [x] Core workflow unchanged (spec → plan → tasks → implement)
- [x] No changes to template copy logic or release workflow
- [x] Extends existing patterns (`/clarify` pattern reused for constitutions)
- [x] Divergence justified: New command for constitution-specific clarification (keeps spec and constitution flows separate per FR-004)

### Principle IV: GitHub Release Template Distribution
- [x] New command template will be distributed via `.specify/templates/commands/`
- [x] No bundled templates in Python package
- [x] Templates downloaded from `anagri/spec-kit` releases

### Principle V: Version Discipline
- [x] This is a MINOR version bump (new `/clarify-constitution` command)
- [x] Changes to templates will be packaged in next release
- [x] CHANGELOG.md will be updated after implementation

### Principle VI: Dogfooding - Self-Application
- [x] This feature developed using spec-kit methodology (constitution → specify → plan → tasks → implement)
- [x] Architectural decisions consulted docs/PHILOSOPHY.md (Layer 2: Templates)
- [x] Four-layer model respected (new template in Layer 2, no CLI changes in Layer 1)
- [x] Feature uses conditional artifacts (template-contracts.md instead of data-model.md per constitution v1.1.0)

## Project Structure

### Documentation (this feature)
```
specs/001-when-the-user/
├── plan.md                    # This file (/plan command output)
├── research.md                # Phase 0 output (/plan command)
├── template-contracts.md      # Phase 1 output (template structure definitions)
├── quickstart.md              # Phase 1 output (/plan command)
├── contracts/                 # Phase 1 output (/plan command)
│   ├── clarify-constitution-command.md     # /clarify-constitution command contract
│   ├── constitution-template.md            # Constitution template structure
│   └── clarification-workflow.md           # Interaction flow contract
└── tasks.md                   # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
templates/
├── commands/
│   ├── clarify-constitution.md       # NEW: Constitution clarification command
│   ├── constitution.md               # MODIFIED: Enhanced with clarification flow
│   ├── clarify.md                    # REFERENCE: Pattern to follow
│   └── [other commands...]
└── [other templates...]

.specify/memory/
└── constitution.md                   # MODIFIED: Support [NEEDS CLARIFICATION] markers

docs/
├── PHILOSOPHY.md                     # Reference for template design patterns
├── quickstart.md                     # May need example update
└── *.md

tests/
├── contract/
│   ├── test_clarify_constitution_output.sh      # Verify command follows contract
│   └── test_constitution_markers.sh             # Verify [NEEDS CLARIFICATION] handling
└── integration/
    ├── test_constitution_minimal_input.sh       # Scenario 1: minimal input flow
    ├── test_clarify_constitution_questions.sh   # Scenario 2: question generation
    └── test_constitution_comprehensive_input.sh # Scenario 4: comprehensive input
```

**Structure Decision**: CLI/Template/Generator tool structure (Option 4 from template). This feature modifies existing slash command templates and adds a new template following the established pattern in `.claude/commands/`. No new bash scripts needed (reuses existing path resolution from `check-prerequisites.sh`). Testing focuses on template contract validation and end-to-end workflow verification.

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
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (template-contracts.md, contracts/, quickstart.md)
- Each template contract → contract test task [P]
  - test_clarify_constitution_output.sh
  - test_constitution_markers.sh
  - test_constitution_workflow.sh
- Each template file → implementation task
  - Create /clarify-constitution command template
  - Modify /constitution command template
- Integration test scenarios from user stories (spec.md):
  - Scenario 1: Minimal input → markers
  - Scenario 2: Clarification questions
  - Scenario 3: Updates constitution
  - Scenario 4: Comprehensive input (no clarification)
- Documentation update tasks:
  - Update docs/quickstart.md with clarification example
  - Update constitution template if needed

**Ordering Strategy**:
- TDD order: Contract tests before template implementation
- Template tests before template creation
- Integration tests after templates complete
- Documentation updates last
- Mark [P] for parallel execution where files are independent

**Task Categories**:
1. **Contract Tests** (4 tasks) - Define expected behavior
2. **Template Implementation** (2 tasks) - Create/modify command templates
3. **Integration Tests** (4 tasks) - Validate end-to-end workflows
4. **Documentation** (2 tasks) - Update user guides
5. **Validation** (1 task) - Final smoke test

**Estimated Output**: 13-15 numbered, ordered tasks in tasks.md

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
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS (all 6 principles compliant)
- [x] Post-Design Constitution Check: PASS (no new violations)
- [x] All NEEDS CLARIFICATION resolved (research phase)
- [x] Complexity deviations documented (none - extends existing patterns)

---
*Based on project constitution - See `.specify/memory/constitution.md` for current version*
