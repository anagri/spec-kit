
# Implementation Plan: [FEATURE]

**Feature**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

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
[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context
**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

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
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->
```
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]

# [REMOVE IF UNUSED] Option 4: CLI/Template/Generator tool (when templates/scripts/config detected)
templates/
├── commands/           # Slash command templates
└── *.md               # Template files with placeholders

scripts/
└── bash/              # Automation scripts (JSON communication)

memory/
└── *.md               # Configuration/state files

src/
└── [cli_name]/        # CLI implementation (if applicable)

docs/
├── PHILOSOPHY.md      # Architectural rationale
├── quickstart.md
└── *.md               # User documentation

tests/
├── contract/          # Template structure tests, JSON schema tests
└── integration/       # End-to-end CLI workflow tests
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

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

### Testing Note (Project-Specific Limitation)

**IMPORTANT**: This project does not have automated test setup, and test execution from CLI does not work.

**Implications for Phase 1 artifacts**:
- Contract test files in `tests/contract/*.sh` are **specification only** (won't be executed)
- Integration test files in `tests/integration/*.sh` are **documentation** (won't run)
- Test cases in `contracts/*.md` serve as **validation criteria** for manual verification

**Implementation approach**:
- Skip creating actual test files during /tasks
- Use contract test cases as **manual validation checklist**
- Verify behavior through direct script execution and observation
- Testing instructions in contracts/ are for **specification purposes** (what SHOULD be tested if tests existed)

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-30 numbered, ordered tasks in tasks.md

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
- [x] Phase 0: Research complete (/plan command) ✓ research.md created
- [x] Phase 1: Design complete (/plan command) ✓ template-contracts.md, contracts/, quickstart.md, CLAUDE.md updated
- [x] Phase 2: Task planning complete (/plan command - describe approach only) ✓ Approach documented below
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS (no violations - all 6 principles satisfied)
- [x] Post-Design Constitution Check: PASS (no new violations after Phase 1)
- [x] All NEEDS CLARIFICATION resolved (Technical Context complete)
- [x] Complexity deviations documented (none - no violations)

---
*Based on project constitution - See `.specify/memory/constitution.md` for current version*
