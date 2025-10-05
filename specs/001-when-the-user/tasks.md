# Tasks: Constitution Command Clarification Flow

**Input**: Design documents from `/specs/001-when-the-user/`
**Prerequisites**: plan.md, research.md, template-contracts.md, contracts/, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → Tech stack: Markdown templates (Claude Code slash commands)
   → Structure: CLI/Template/Generator tool (templates/commands/)
2. Load design documents:
   → template-contracts.md: Template structure definitions
   → contracts/: 3 contract files → 3 contract validation tasks
   → research.md: 6 key decisions → inform implementation
   → quickstart.md: User guide with 4 workflows
3. Generate tasks by category:
   → Contract Tests: Validate template behavior
   → Template Implementation: Create/modify command templates
   → Integration Tests: End-to-end workflow validation
   → Documentation: Update user guides
   → Validation: Smoke test
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Templates are independent files = [P] possible
   → Integration tests are independent = [P] possible
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001-T015)
6. All tasks executable with file paths provided
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
This is a CLI/Template/Generator tool (Option 4 from plan.md):
- **Templates**: `templates/commands/*.md` (SOURCE - edit for distribution)
- **Tests**: `tests/contract/*.sh`, `tests/integration/*.sh`
- **Docs**: `docs/*.md`
- **Memory**: `memory/constitution.md` (template, not installed)

## Phase 3.1: Contract Tests (TDD) ⚠️ MUST COMPLETE BEFORE 3.2
**CRITICAL: These tests MUST be written and MUST FAIL before template implementation**

- [ ] T001 [P] Contract test for /clarify-constitution command execution flow
  **File**: `tests/contract/test_clarify_constitution_output.sh`
  **Contract**: `specs/001-when-the-user/contracts/clarify-constitution-command.md`
  **Validates**:
  - JSON path parsing from check-prerequisites.sh
  - Marker detection (`[NEEDS CLARIFICATION]` regex)
  - Question generation (max 5 questions)
  - Sequential questioning (one at a time)
  - Integration after each answer
  - Session tracking and soft limit warning

- [ ] T002 [P] Contract test for constitution [NEEDS CLARIFICATION] marker handling
  **File**: `tests/contract/test_constitution_markers.sh`
  **Contract**: `specs/001-when-the-user/contracts/constitution-template.md`
  **Validates**:
  - Marker insertion when user input insufficient
  - Marker syntax: `[NEEDS CLARIFICATION]` or `[NEEDS CLARIFICATION: hint]`
  - Marker placement (content only, not headings)
  - Marker removal on clarification
  - Session metadata initialization

- [ ] T003 [P] Contract test for clarification workflow state transitions
  **File**: `tests/contract/test_clarification_workflow.sh`
  **Contract**: `specs/001-when-the-user/contracts/clarification-workflow.md`
  **Validates**:
  - State 1: Minimal input → markers
  - State 2: First clarification session
  - State 3: Iterative clarification
  - State 6: Soft limit warning (session ≥ 3)
  - State 7: Comprehensive input (no markers)

## Phase 3.2: Template Implementation (ONLY after contract tests are failing)

- [ ] T004 Create /clarify-constitution command template
  **File**: `templates/commands/clarify-constitution.md`
  **Contract**: `specs/001-when-the-user/contracts/clarify-constitution-command.md`
  **Implementation**:
  - YAML frontmatter with description
  - User input handling with $ARGUMENTS placeholder
  - 8-step execution flow:
    1. Path resolution (check-prerequisites.sh --json --paths-only)
    2. Ambiguity scan (detect `[NEEDS CLARIFICATION]` markers)
    3. Question generation (max 5, constitution-specific taxonomy)
    4. Sequential questioning loop (ONE at a time)
    5. Integration after each answer (update constitution, save file)
    6. Iteration tracking (session count, soft limit warning)
    7. Validation (marker resolution, markdown integrity)
    8. Completion report (sections updated, next steps)
  - Constitution-specific question taxonomy:
    * Architectural Principles
    * Technology Constraints
    * Development Workflow
    * Governance Policies
  - Question formats:
    * Multiple choice: Markdown table with 2-5 options
    * Short answer: ≤5 words constraint
  - Integration rules:
    * Create `## Clarifications` section if missing
    * Add `### Session YYYY-MM-DD` for today
    * Append `- Q: <question> → A: <answer>` bullets
    * Replace `[NEEDS CLARIFICATION]` with user answer
    * Save after each integration (atomic updates)
  - Soft limit: Warn at 3 sessions, no hard block
  - Escape hatch: Suggest manual editing if AI misunderstands

- [ ] T005 Modify /constitution command template to support clarification markers
  **File**: `templates/commands/constitution.md`
  **Contract**: `specs/001-when-the-user/contracts/constitution-template.md`
  **Modifications** (preserve existing functionality):
  - **Step 2 (Placeholder Collection)**:
    * If user input supplies value → use it
    * Else if repo context has value → infer it
    * Else → insert `[NEEDS CLARIFICATION]` marker
    * Track incomplete sections for Step 8 summary
  - **Step 3 (Draft Constitution)**:
    * Allow `[NEEDS CLARIFICATION]` in content sections
    * Enforce: No markers in headings
    * Don't hallucinate for marked sections (NFR-001)
  - **Step 7 (Write Constitution)**:
    * Include markers if present
    * Initialize session metadata: `<!-- Clarification Sessions: 0 -->`
    * Prepare /clarify-constitution suggestion if markers exist
  - **Step 8 (Final Summary)**:
    * Count and report `[NEEDS CLARIFICATION]` markers
    * List affected sections
    * Next command: /clarify-constitution (if markers) OR /specify (if complete)
  - **Backward compatibility**: Comprehensive input still generates complete constitution

## Phase 3.3: Integration Tests (End-to-End Workflows)

- [ ] T006 [P] Integration test: Minimal input → markers → /clarify-constitution
  **File**: `tests/integration/test_constitution_minimal_input.sh`
  **Scenario**: Acceptance Scenario 1 from spec.md
  **Steps**:
  1. Run `/constitution "Python web app"`
  2. Verify constitution created with `[NEEDS CLARIFICATION]` markers
  3. Verify markers in: Architectural Principle, Framework, Workflow, Governance
  4. Verify summary suggests `/clarify-constitution`
  5. Verify session metadata: `<!-- Clarification Sessions: 0 -->`

- [ ] T007 [P] Integration test: /clarify-constitution asks targeted questions
  **File**: `tests/integration/test_clarify_constitution_questions.sh`
  **Scenario**: Acceptance Scenario 2 from spec.md
  **Steps**:
  1. Setup: Constitution with 4 `[NEEDS CLARIFICATION]` markers
  2. Run `/clarify-constitution`
  3. Verify max 5 questions asked
  4. Verify questions cover: Principles, Tech Stack, Workflow, Governance
  5. Verify question formats: Multiple choice tables OR short answer
  6. Verify sequential presentation (one at a time, not batch)

- [ ] T008 [P] Integration test: User answers update constitution without hallucination
  **File**: `tests/integration/test_constitution_updates.sh`
  **Scenario**: Acceptance Scenario 3 from spec.md
  **Steps**:
  1. Setup: /clarify-constitution in progress
  2. User answers: "Test-first development" (Q1), "Python 3.11 + FastAPI" (Q2)
  3. Verify constitution updated with EXACT user answers
  4. Verify `[NEEDS CLARIFICATION]` markers removed from answered sections
  5. Verify Clarifications section added:
     ```markdown
     ## Clarifications
     ### Session 2025-10-05
     - Q: What is the primary principle? → A: Test-first development
     - Q: What Python framework? → A: Python 3.11 + FastAPI
     ```
  6. Verify NO hallucinated content (NFR-001)

- [ ] T009 [P] Integration test: Comprehensive input skips clarification
  **File**: `tests/integration/test_constitution_comprehensive_input.sh`
  **Scenario**: Acceptance Scenario 4 from spec.md
  **Steps**:
  1. Run `/constitution "Python 3.11 FastAPI project. Test-first principle. Solo dev, trunk-based. Quarterly reviews. Owner amendments."`
  2. Verify constitution created with ZERO `[NEEDS CLARIFICATION]` markers
  3. Verify all sections populated from user input
  4. Verify summary suggests `/specify` (not /clarify-constitution)
  5. Verify NO session metadata (clarification not needed)

## Phase 3.4: Edge Case Tests

- [ ] T010 [P] Integration test: Soft limit warning at 3+ sessions
  **File**: `tests/integration/test_clarification_soft_limit.sh`
  **Scenario**: FR-012 from spec.md
  **Steps**:
  1. Setup: Constitution with session count = 3
  2. Run `/clarify-constitution` (4th time)
  3. Verify warning displayed: "⚠ Warning: This is your 4th clarification session."
  4. Verify suggestion: "Consider direct editing if AI misunderstands"
  5. Verify NO hard block (execution continues)
  6. Verify session count incremented: `<!-- Clarification Sessions: 4 -->`

- [ ] T011 [P] Integration test: Manual editing escape hatch
  **File**: `tests/integration/test_manual_edit_escape.sh`
  **Scenario**: FR-011 from spec.md
  **Steps**:
  1. Setup: User struggles with AI during /clarify-constitution
  2. AI suggests: "You can directly edit .specify/memory/constitution.md"
  3. User manually replaces `[NEEDS CLARIFICATION]` in Workflow section
  4. Run `/clarify-constitution` again
  5. Verify manual edits preserved
  6. Verify questions focus on remaining marked sections only

## Phase 3.5: Documentation Updates

- [ ] T012 Update docs/quickstart.md with constitution clarification examples
  **File**: `docs/quickstart.md`
  **Reference**: `specs/001-when-the-user/quickstart.md` (feature-specific guide)
  **Changes**:
  - Add "Constitution Setup" section before "Create the Spec"
  - Show minimal input → clarification workflow example
  - Show comprehensive input example (skip clarification)
  - Update CLI tool example to mention constitution clarification
  - Add troubleshooting: "No clarifications needed" vs "markers present"

- [ ] T013 Verify memory/constitution.md template supports markers
  **File**: `memory/constitution.md` (SOURCE template for distribution)
  **Validation**:
  - Template can accept `[NEEDS CLARIFICATION]` in placeholder positions
  - No breaking changes to existing constitution structure
  - Supports `## Clarifications` section addition
  - Session metadata comment format compatible
  - Check against: `specs/001-when-the-user/contracts/constitution-template.md`

## Phase 3.6: Validation & Testing

- [ ] T014 Run all contract and integration tests to verify implementation
  **Command**:
  ```bash
  # Contract tests
  bash tests/contract/test_clarify_constitution_output.sh
  bash tests/contract/test_constitution_markers.sh
  bash tests/contract/test_clarification_workflow.sh

  # Integration tests
  bash tests/integration/test_constitution_minimal_input.sh
  bash tests/integration/test_clarify_constitution_questions.sh
  bash tests/integration/test_constitution_updates.sh
  bash tests/integration/test_constitution_comprehensive_input.sh
  bash tests/integration/test_clarification_soft_limit.sh
  bash tests/integration/test_manual_edit_escape.sh
  ```
  **Success criteria**: All tests pass ✓

- [ ] T015 Smoke test: Complete clarification workflow end-to-end
  **Manual test** following `specs/001-when-the-user/quickstart.md`:
  1. Create test project: `speclaude init test-clarification`
  2. Run `/constitution "Rust CLI tool"`
  3. Verify markers present
  4. Run `/clarify-constitution`
  5. Answer 3-5 questions
  6. Verify constitution complete
  7. Run `/specify "first feature"`
  8. Verify constitution referenced correctly
  9. Cleanup: `rm -rf test-clarification`

## Dependencies

**Phase Order** (MUST follow):
1. Phase 3.1 (Contract Tests) BEFORE Phase 3.2 (Implementation)
2. Phase 3.2 (Templates) BEFORE Phase 3.3 (Integration Tests)
3. Phase 3.3-3.4 (All Tests) BEFORE Phase 3.5 (Documentation)
4. Phase 3.5 (Docs) BEFORE Phase 3.6 (Validation)

**Parallel Execution Opportunities**:
- T001, T002, T003 can run in parallel [P] (different contract files)
- T004 and T005 are sequential (T005 may reference T004 patterns)
- T006, T007, T008, T009 can run in parallel [P] (independent test scenarios)
- T010, T011 can run in parallel [P] (independent edge cases)
- T012, T013 can run in parallel [P] (different documentation files)

**Critical Path**:
```
T001-T003 (Contract Tests)
  → T004 (Create /clarify-constitution)
  → T005 (Modify /constitution)
  → T006-T011 (All Integration Tests)
  → T012-T013 (Documentation)
  → T014 (Test Suite)
  → T015 (Smoke Test)
```

## Parallel Execution Examples

**Example 1: Contract Tests (Phase 3.1)**
```bash
# Run all 3 contract tests in parallel
bash tests/contract/test_clarify_constitution_output.sh &
bash tests/contract/test_constitution_markers.sh &
bash tests/contract/test_clarification_workflow.sh &
wait
```

**Example 2: Integration Tests (Phase 3.3)**
```bash
# Run all 4 acceptance scenario tests in parallel
bash tests/integration/test_constitution_minimal_input.sh &
bash tests/integration/test_clarify_constitution_questions.sh &
bash tests/integration/test_constitution_updates.sh &
bash tests/integration/test_constitution_comprehensive_input.sh &
wait
```

**Example 3: Edge Case Tests (Phase 3.4)**
```bash
# Run edge case tests in parallel
bash tests/integration/test_clarification_soft_limit.sh &
bash tests/integration/test_manual_edit_escape.sh &
wait
```

**Example 4: Documentation (Phase 3.5)**
```bash
# Update docs in parallel (different files)
# T012: Update docs/quickstart.md
# T013: Verify memory/constitution.md
# (Manual tasks, but can be done concurrently by different people or AI sessions)
```

## Constitutional Compliance Checklist

Before marking tasks complete, verify:
- [x] **Principle I (Claude Code-Only)**: All templates in `.claude/commands/` format ✓
- [x] **Principle II (Solo Dev Workflow)**: No git branch coupling in any scripts ✓
- [x] **Principle III (Minimal Divergence)**: Extends `/clarify` pattern, no core changes ✓
- [x] **Principle IV (GitHub Release)**: Templates in `templates/commands/` for release packaging ✓
- [x] **Principle V (Version Discipline)**: Template changes = MINOR bump, CHANGELOG update ✓
- [x] **Principle VI (Dogfooding)**: Using spec-kit methodology to build spec-kit ✓

## Success Criteria

**Functional Requirements Met**:
- [x] FR-001: System analyzes user input sufficiency (/constitution Step 2)
- [x] FR-002: Generates constitution with markers when input insufficient
- [x] FR-003: Informs user to run /clarify-constitution
- [x] FR-004: /clarify-constitution is separate command
- [x] FR-005: Asks constitution-specific questions (4 categories)
- [x] FR-006: Incorporates user responses, replaces markers
- [x] FR-007: Follows /clarify interaction pattern
- [x] FR-008: Supports multiple /clarify-constitution runs
- [x] FR-009: Preserves user content on re-run
- [x] FR-010: Iterates through all [NEEDS CLARIFICATION] blocks
- [x] FR-011: Manual editing escape hatch available
- [x] FR-012: Soft limit (3 rounds) with warning, no hard block

**Non-Functional Requirements Met**:
- [x] NFR-001: No hallucination (markers prevent AI guessing)
- [x] NFR-002: Markers removed only when user provides info
- [x] NFR-003: Separate command doesn't affect /clarify workflow

**All 15 tasks completion** = Feature ready for release ✓
