# Page 09: /analyze - Consistency Validation

**Purpose**: Validate cross-artifact consistency before implementation begins

**Last Updated**: 2025-10-17

**Related Pages**:
- [Page 08: /tasks Command](08-tasks-command.md) - Generate tasks before analyzing
- [Page 10: /implement Command](10-implement-command.md) - Execute after validation
- [Page 06: /clarify Command](06-clarify-command.md) - Resolve ambiguities proactively
- [Page 03: /plan Command](03-plan-command.md) - Design artifacts analyzed

---

## Overview

The `/analyze` command performs a **non-destructive** cross-artifact consistency analysis across `spec.md`, `plan.md`, and `tasks.md` to catch issues before implementation begins. It is **optional but highly recommended** to run after `/tasks` and before `/implement` to identify:

- Requirements with zero task coverage
- Duplicate or conflicting specifications
- Ambiguous requirements without measurable criteria
- Constitution principle violations
- Terminology inconsistencies across artifacts
- Coverage gaps in non-functional requirements

**Key Principle**: The `/analyze` command is **strictly read-only**—it never modifies files. It provides a structured analysis report with severity-ranked issues and optionally offers remediation suggestions that require explicit user approval.

---

## When to Use

### Workflow Position

**After**: `/tasks` completes successfully (requires `tasks.md` to exist)
**Before**: `/implement` begins execution

```
Recommended Workflow:
/specify → /clarify → /plan → /tasks → /analyze → /implement
                                        ^^^^^^^^^^
                                        You are here
```

### Use Cases

**Run /analyze if**:
- Working on complex features with >10 tasks
- Multiple non-functional requirements (performance, security, scalability)
- Team environment where consistency is critical
- High-stakes features where rework is expensive
- Want to catch issues early (cheap to fix now, expensive during implementation)

**Skip /analyze if**:
- Simple feature with <10 tasks and high confidence
- Trivial changes (adding a single endpoint, utility function)
- Iterative prototyping where flexibility is more valuable than consistency
- Time-constrained scenarios (though this is risky)

---

## Prerequisites

### Required Files

The command validates that all required artifacts exist before proceeding:

```bash
# Script validation
.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks

# Required files (must exist):
specs/###-feature-name/spec.md       # Feature specification
specs/###-feature-name/plan.md       # Implementation plan
specs/###-feature-name/tasks.md      # Task breakdown
```

### Optional Context

```bash
.specify/memory/constitution.md      # For principle validation
specs/###-feature-name/data-model.md # For entity consistency checks
specs/###-feature-name/contracts/    # For contract-task mapping
```

**Error Handling**: If any required file is missing, the command aborts with an error message instructing the user to run the prerequisite command (e.g., "Run /tasks first to generate tasks.md").

---

## User Action

### Command Invocation

```
/analyze
```

**Arguments**: None (analyzes current feature context automatically)

### What User Sees

**Step 1: Script Execution**

```
Running script: check-prerequisites.sh --json --require-tasks --include-tasks
✓ All required files present
```

**Step 2: Artifact Loading**

```
Loading artifacts...
✓ Loaded spec.md (12 functional requirements, 4 non-functional requirements, 5 user stories)
✓ Loaded plan.md (6 phases, 3 entities, 8 contracts)
✓ Loaded tasks.md (42 tasks across 5 phases)
✓ Loaded constitution (6 principles)
```

**Step 3: Semantic Model Building**

```
Building semantic models...
✓ Requirements inventory (16 requirements with stable keys)
✓ User story mapping (5 stories)
✓ Task coverage mapping (42 tasks → requirements)
✓ Constitution rule set extraction (6 principles)
```

**Step 4: Detection Passes**

```
Running detection passes...

A. Duplication Detection: ✓ No duplicates found
B. Ambiguity Detection: ⚠ 2 issues found
C. Underspecification: ✓ All requirements have measurable criteria
D. Constitution Alignment: ⚠ 1 issue found
E. Coverage Gaps: ⚠ 3 issues found
F. Inconsistency: ⚠ 1 issue found
```

**Step 5: Structured Analysis Report** (see [Report Format](#analysis-report-format) section below)

**Step 6: Interactive Offer**

```
Would you like me to suggest concrete remediation edits for the top 5 issues?
(Note: I will not apply changes automatically—your approval required)
```

---

## The 6 Detection Passes

The `/analyze` command performs six systematic detection passes across all loaded artifacts. Each pass focuses on a specific category of issues.

### A. Duplication Detection

**Finds**: Near-duplicate requirements, redundant user stories, overlapping functional specifications

**Detection Logic**:
- Semantic similarity analysis between requirement texts
- Keyword overlap detection (>70% shared terms)
- Intent matching (same outcome with different wording)

**Example Issue**:

```markdown
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| D1 | Duplication | HIGH | spec.md:L120-134, L145-152 | Two similar requirements for file upload functionality |
```

**Recommendation**: "Merge into single FR-003: 'Users can upload files via drag-and-drop or file picker (max 10MB)'"

**Real-World Example**:
- FR-005: "User can upload file"
- FR-012: "System allows file uploads"
→ **Detection**: Same intent, different phrasing
→ **Remediation**: Merge into FR-005 with clearer scope

---

### B. Ambiguity Detection

**Finds**: Vague adjectives without measurable criteria, unresolved placeholders, missing metrics

**Detection Logic**:
- Pattern matching for ambiguous terms: "fast", "scalable", "secure", "intuitive", "robust", "reliable"
- Placeholder scanning: `TODO`, `TKTK`, `???`, `<placeholder>`, `[NEEDS CLARIFICATION]`
- Missing quantitative metrics for non-functional requirements

**Example Issue**:

```markdown
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| A1 | Ambiguity | HIGH | spec.md:L89 NFR-002 | "Fast response time" lacks measurable target |
```

**Recommendation**: "Specify latency target (e.g., <200ms p95 for REST endpoints, <100ms for WebSocket messages)"

**Real-World Examples**:
- NFR-001: "System must be fast" → No metric
  - **Fix**: "System MUST deliver messages with <100ms p95 latency"
- FR-008: "Secure authentication" → Undefined security model
  - **Fix**: "Authentication via OAuth2 (Google, GitHub) with JWT tokens (15-minute expiry)"
- NFR-003: "System should scale" → No capacity target
  - **Fix**: "System MUST support 10,000 concurrent WebSocket connections"

---

### C. Underspecification

**Finds**: Requirements with verbs but missing outcomes, user stories without acceptance criteria, tasks referencing undefined components

**Detection Logic**:
- Requirements missing measurable outcomes or success criteria
- User stories lacking "Given-When-Then" or acceptance criteria
- Tasks referencing files/components not defined in `plan.md` or `data-model.md`
- Edge cases mentioned without handling specifications

**Example Issue**:

```markdown
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| U1 | Underspecification | MEDIUM | tasks.md T012 | Task references 'MessageQueue' component undefined in plan |
```

**Recommendation**: "Add MessageQueue to data-model.md as external dependency or clarify as internal component"

**Real-World Examples**:
- FR-006: "User can login" → Missing auth method, session timeout, logout behavior
  - **Fix**: Add acceptance criteria: "Login via OAuth2, session expires after 15 minutes of inactivity, explicit logout clears session"
- T015: "Implement caching layer" → No cache store defined
  - **Fix**: Update plan.md to specify Redis as cache store, add to data-model.md
- User Story 3: "User receives notification" → No delivery mechanism specified
  - **Fix**: "User receives push notification via Firebase Cloud Messaging when message sent"

---

### D. Constitution Alignment

**Finds**: Violations of MUST principles, missing mandated sections, architectural mismatches

**Detection Logic**:
- Load `.specify/memory/constitution.md` for principle definitions
- Extract MUST/SHOULD normative statements
- Cross-reference against plan architecture and task ordering
- Validate required sections exist (e.g., Complexity Tracking table if violations documented)

**Example Issue**:

```markdown
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| CA1 | Constitution | CRITICAL | plan.md Phase 2, tasks.md T010-T015 | Violates Test-First (Principle III) - implementation tasks before contract tests |
```

**Recommendation**: "Reorder tasks to ensure contract tests (T005-T008) are completed before implementation (T010-T015). Move T005-T008 from Core Phase to Setup Phase."

**Real-World Examples**:
- **Principle I Violation**: Plan proposes ORM wrapper abstraction
  - Constitution: "No wrapper abstractions (Principle VI: Anti-Abstraction)"
  - **Fix**: Use SQLAlchemy directly, remove wrapper layer from plan
- **Principle III Violation**: Implementation tasks before test tasks
  - Constitution: "TDD mandatory (Principle III: Test-First - NON-NEGOTIABLE)"
  - **Fix**: Reorder tasks.md to place all contract tests before implementation
- **Principle V Violation**: Missing version bump for CLI changes
  - Constitution: "Version discipline (Principle V: NON-NEGOTIABLE)"
  - **Fix**: Update pyproject.toml version + CHANGELOG.md entry

---

### E. Coverage Gaps

**Finds**: Requirements with zero associated tasks, tasks with no mapped requirement/story, non-functional requirements not reflected in tasks

**Detection Logic**:
- Build requirement → task mapping via keyword matching and explicit IDs
- Identify orphaned requirements (no tasks reference them)
- Identify orphaned tasks (no requirement justifies them)
- Validate NFRs have corresponding test/implementation tasks

**Example Issue**:

```markdown
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| C1 | Coverage | CRITICAL | spec.md FR-008 | Message encryption requirement has zero associated tasks |
```

**Recommendation**: "Add Task T38: Implement end-to-end message encryption using libsodium (addresses FR-008)"

**Real-World Examples**:
- FR-008: "Graceful degradation under load" → Zero tasks
  - **Fix**: Add T39: "Performance test for graceful degradation (simulate 3x target load)"
- NFR-002: "99.9% uptime" → No monitoring/alerting tasks
  - **Fix**: Add T40: "Configure Prometheus metrics + Grafana dashboards", T41: "Set up PagerDuty alerts"
- T025: "Implement analytics dashboard" → No requirement mentions analytics
  - **Fix**: Either add FR-015 "Analytics dashboard for admin users" or remove T025 as out-of-scope

**Coverage Summary Table**:

```markdown
| Requirement Key       | Has Task? | Task IDs   | Notes                |
|-----------------------|-----------|------------|----------------------|
| user-can-send-message | ✓         | T010, T015 | Covered              |
| message-encryption    | ✗         | —          | **Missing coverage** |
| real-time-delivery    | ✓         | T012, T014 | Covered              |
| graceful-degradation  | ✗         | —          | **Missing coverage** |
| message-persistence   | ✓         | T008, T020 | Covered              |
```

---

### F. Inconsistency

**Finds**: Terminology drift, data entities in plan but not in spec (or vice versa), task ordering contradictions, conflicting requirements

**Detection Logic**:
- Extract entity names from `spec.md` and `data-model.md`, flag mismatches
- Identify same concept with multiple names (e.g., "User" vs "Account" vs "Profile")
- Detect conflicting requirements (e.g., one requires Next.js, another requires Vue)
- Check task ordering for logical contradictions (integration tasks before setup tasks without dependency notes)

**Example Issue**:

```markdown
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| F1 | Inconsistency | MEDIUM | spec.md vs data-model.md | Spec says "User" entity, data-model says "Account" |
```

**Recommendation**: "Normalize terminology to 'User' across both artifacts (update data-model.md line 15)"

**Real-World Examples**:
- Spec: "Message" entity, Plan: "ChatMessage" entity
  - **Fix**: Normalize to "Message" in data-model.md
- FR-003: "Use PostgreSQL for persistence", FR-007: "Use MongoDB for user data"
  - **Fix**: Resolve conflict—choose single database or justify polyglot persistence
- T018: "Deploy to production" appears before T015: "Run integration tests"
  - **Fix**: Reorder tasks or add dependency note: "T018 depends on T015 passing"

---

## Severity Assignment Rules

The `/analyze` command assigns severity levels to each detected issue based on impact and urgency.

### CRITICAL

**Definition**: Issues that **MUST** be resolved before `/implement` can proceed

**Criteria**:
- Violates constitution MUST principle (non-negotiable)
- Missing core artifact (spec.md, plan.md, tasks.md corrupted or incomplete)
- Zero coverage for requirement blocking baseline functionality (e.g., authentication, data persistence)
- Conflicting requirements preventing implementation (mutually exclusive choices)

**Examples**:
- CA1: TDD principle violated (implementation tasks before test tasks)
- C1: Message encryption requirement (FR-008) has zero tasks
- C2: Authentication requirement (FR-001) has zero implementation tasks

**Action Required**: Fix issues, regenerate affected artifacts, re-run `/analyze` before proceeding

---

### HIGH

**Definition**: Issues that **SHOULD** be resolved to prevent implementation confusion or rework

**Criteria**:
- Duplicate or conflicting requirements causing ambiguity
- Ambiguous security/performance criteria (e.g., "fast", "secure" without metrics)
- Untestable acceptance criteria (no measurable success condition)
- Significant terminology drift across artifacts

**Examples**:
- A1: "Fast response time" lacks measurable target (NFR-002)
- D1: Two similar requirements for file upload (FR-005, FR-012)
- F1: Terminology drift—"User" vs "Account" across spec and plan

**Action Recommended**: Resolve before `/implement` to improve implementation quality, but not strictly blocking

---

### MEDIUM

**Definition**: Issues that improve quality but don't block implementation

**Criteria**:
- Minor terminology drift (same concept, slightly different names)
- Missing task coverage for non-critical non-functional requirements
- Underspecified edge cases (mentioned but not fully detailed)
- Tasks referencing components not formally documented but implied

**Examples**:
- U1: Task references 'MessageQueue' undefined in plan (can be inferred)
- F2: "Message" vs "ChatMessage" terminology drift (context-clear)
- C3: Edge case "network interruption during send" lacks recovery specification

**Action Optional**: Consider fixing if time permits, safe to proceed with warnings

---

### LOW

**Definition**: Style/wording improvements, no functional impact

**Criteria**:
- Style/wording inconsistencies
- Minor redundancy that doesn't cause confusion
- Formatting issues in artifacts
- Missing optional sections (e.g., "Future Enhancements")

**Examples**:
- L1: Inconsistent bullet formatting in spec.md
- L2: Minor redundancy in user story descriptions
- L3: Missing "Future Considerations" section (optional)

**Action**: Ignore unless time permits cosmetic improvements

---

## Analysis Report Format

### Full Report Structure

```markdown
### Specification Analysis Report

Generated: 2025-10-17 14:30:00
Feature: 003-real-time-chat

---

#### Issues Summary

| ID  | Category      | Severity | Location(s)                | Summary                                       | Recommendation                            |
|-----|---------------|----------|----------------------------|-----------------------------------------------|-------------------------------------------|
| C1  | Coverage      | CRITICAL | spec.md FR-008             | Message encryption requirement has zero tasks | Add Task T38: Implement encryption        |
| CA1 | Constitution  | CRITICAL | plan.md Phase 2            | Violates Test-First (Principle III)           | Reorder tasks: tests before implementation|
| A1  | Ambiguity     | HIGH     | spec.md:L89 NFR-002        | "Fast response time" lacks metric             | Specify latency target (e.g., <200ms p95) |
| D1  | Duplication   | HIGH     | spec.md:L120-134, L145-152 | Two similar requirements for file upload      | Merge into single FR with clear scope     |
| F1  | Inconsistency | MEDIUM   | spec.md vs data-model.md   | Spec says "User" entity, plan says "Account"  | Normalize terminology to "User"           |
| U1  | Underspec     | MEDIUM   | tasks.md T012              | Task references undefined 'MessageQueue'      | Add to data-model or clarify as external  |
| L1  | Style         | LOW      | spec.md Functional Req     | Inconsistent bullet formatting                | Use consistent markdown formatting        |

---

#### Coverage Summary

| Requirement Key          | Has Task? | Task IDs      | Notes                    |
|--------------------------|-----------|---------------|--------------------------|
| user-can-send-message    | ✓         | T010, T015    | Covered                  |
| message-encryption       | ✗         | —             | **CRITICAL: Missing**    |
| real-time-delivery       | ✓         | T012, T014    | Covered                  |
| user-authentication      | ✓         | T025          | Covered                  |
| presence-tracking        | ✓         | T026, T027    | Covered                  |
| offline-message-queue    | ✓         | T028          | Covered                  |
| graceful-degradation     | ✗         | —             | **HIGH: Missing test**   |
| message-history-retrieval| ✓         | T030          | Covered                  |

**Coverage**: 75% (6/8 requirements have ≥1 task)

---

#### Constitution Alignment Issues

**CRITICAL: Test-First Principle Violation (Principle III)**

- **Location**: plan.md Phase 2, tasks.md T010-T015
- **Issue**: Implementation tasks (T010-T015) appear before contract test tasks (T005-T008)
- **Constitution Text**: "Contract tests MUST be written and approved before implementation"
- **Remediation**: Move T005-T008 from Core Phase to Setup Phase, ensure all tests complete before T010

**Status**: ✗ Constitution compliance failed (1 MUST violation)

---

#### Unmapped Tasks

Tasks with no clear requirement justification:

- **T037**: Performance optimization pass → No performance requirement in spec
  - **Recommendation**: Add NFR-005 "System MUST maintain <200ms p95 latency under 1000 req/s load"

---

#### Metrics

- **Total Requirements**: 8 functional + 4 non-functional = 12
- **Total Tasks**: 42 tasks across 5 phases
- **Coverage**: 75% (6/8 functional requirements have ≥1 task)
- **Ambiguity Count**: 1 (HIGH severity)
- **Duplication Count**: 1 (HIGH severity)
- **Critical Issues**: 2 (CA1 Constitution, C1 Coverage)
- **High Issues**: 2 (A1 Ambiguity, D1 Duplication)
- **Medium Issues**: 2 (F1 Inconsistency, U1 Underspec)
- **Low Issues**: 1 (L1 Style)

---

### Next Actions

**CRITICAL issues exist - Resolve before /implement**

1. **Fix CA1**: Reorder tasks.md to place contract tests (T005-T008) before implementation (T010-T015)
   - **Command**: Manually edit `tasks.md` or re-run `/tasks` with updated plan
2. **Fix C1**: Add Task T38 to implement message encryption (addresses FR-008)
   - **Command**: Append to `tasks.md` Core Phase
3. **Fix A1**: Update NFR-002 in `spec.md` with measurable latency target
   - **Command**: `/specify` with refinement or manual edit
4. **Fix D1**: Merge duplicate file upload requirements into single FR-003
   - **Command**: Manual edit of `spec.md`

**After remediation**:
- Re-run `/analyze` to verify coverage reaches 100%
- Proceed to `/implement` once all CRITICAL issues resolved

---

Would you like me to suggest concrete remediation edits for the top 4 issues?
```

---

## All Possible Outcomes

### Outcome 1: Zero Issues (Success)

**Report**:

```markdown
### Specification Analysis Report

Generated: 2025-10-17 14:30:00
Feature: 003-real-time-chat

---

✓ **All detection passes successful**

A. Duplication Detection: ✓ No duplicates found
B. Ambiguity Detection: ✓ All requirements have measurable criteria
C. Underspecification: ✓ All requirements complete with outcomes
D. Constitution Alignment: ✓ No principle violations
E. Coverage Gaps: ✓ All requirements mapped to tasks
F. Inconsistency: ✓ No terminology drift

#### Coverage Summary

Coverage: 100% (8/8 requirements have ≥1 task)

#### Metrics

- Total Requirements: 8
- Total Tasks: 42
- Coverage: 100%
- Issues: 0

---

### Next Actions

✓ **Analysis complete - Ready to proceed to /implement**

No issues detected. All requirements have task coverage, constitution principles satisfied, no ambiguities or inconsistencies.
```

---

### Outcome 2: LOW/MEDIUM Issues Only (Proceed with Warnings)

**Report** (abbreviated):

```markdown
### Specification Analysis Report

---

#### Issues Summary

| ID | Category | Severity | Summary |
|----|----------|----------|---------|
| F1 | Inconsistency | MEDIUM | Terminology drift "User" vs "Account" |
| L1 | Style | LOW | Inconsistent bullet formatting |

#### Metrics

- Critical Issues: 0
- High Issues: 0
- Medium Issues: 1
- Low Issues: 1

---

### Next Actions

✓ **Safe to proceed to /implement**

Consider addressing:
- F1: Normalize terminology to "User" across spec and plan
- L1: Optional formatting cleanup

These issues do not block implementation. Proceed when ready.
```

---

### Outcome 3: CRITICAL Issues (Blocked)

**Report** (abbreviated):

```markdown
### Specification Analysis Report

---

#### Issues Summary

| ID  | Category     | Severity | Summary |
|-----|--------------|----------|---------|
| CA1 | Constitution | CRITICAL | Test-First principle violated |
| C1  | Coverage     | CRITICAL | FR-008 has zero tasks |

#### Metrics

- Critical Issues: 2
- High Issues: 0

---

### Next Actions

✗ **CRITICAL issues must be resolved before /implement**

1. Fix CA1: Reorder tasks (tests before implementation)
2. Fix C1: Add Task T38 for message encryption

**Remediation Workflow**:
- Edit `tasks.md` to fix task ordering
- Re-run `/tasks` if regeneration needed
- Re-run `/analyze` to verify fixes
- Proceed to `/implement` after validation passes
```

---

### Outcome 4: Remediation Offered

**Interactive Flow**:

```
Claude: Analysis complete with 4 issues (2 CRITICAL, 2 HIGH).

Would you like me to suggest concrete remediation edits for the top 4 issues?

User: Yes

Claude:
**Suggested Remediation for CA1 (CRITICAL)**

Move the following tasks from Core Phase to Setup Phase in tasks.md:

```markdown
## Setup Phase (T001-T008)
...
- [ ] T005: Write contract test for POST /messages [P]
- [ ] T006: Write contract test for WebSocket /ws [P]
- [ ] T007: Write contract test for GET /rooms [P]
- [ ] T008: Write integration test for message sending [P]
```

**Suggested Remediation for C1 (CRITICAL)**

Add to Core Phase in tasks.md:

```markdown
- [ ] T38: Implement end-to-end message encryption [P]
  - Files: `src/crypto/encryption.py`
  - Description: Implement AES-256-GCM encryption for message text using libsodium
  - Prerequisites: T006 (Message model exists)
  - Success criteria: Messages encrypted at rest, decrypted on retrieval
  - Addresses: FR-008 (message encryption requirement)
```

Shall I apply these changes to tasks.md?

User: Yes

Claude: ✓ Applied remediation for CA1 and C1
        ✓ Updated tasks.md
        ✓ Re-running analysis to verify...

[... re-analysis shows 0 CRITICAL issues ...]

✓ Remediation successful - Ready for /implement
```

---

## Follow-up Actions

### If CRITICAL Issues Exist

**Workflow**:

```
1. Fix issues (manually or with Claude's remediation suggestions)
2. Re-run /tasks (if task regeneration needed)
3. Re-run /analyze (to verify fixes)
4. Proceed to /implement (once validation passes)
```

**Example**:

```bash
# After fixing constitution violation in plan.md
User: /tasks

# Regenerate tasks with corrected ordering
Claude: [generates tasks.md with tests before implementation]

User: /analyze

# Verify fixes
Claude: ✓ All CRITICAL issues resolved, ready for /implement
```

---

### If HIGH Issues Exist

**Decision Point**: Proceed with warnings or remediate first?

**Considerations**:
- **Remediate if**: High-stakes feature, team environment, ambiguity could cause confusion
- **Proceed if**: Solo developer, iterative prototyping, issues are minor and obvious

**Example**:

```
User: Should I fix A1 (ambiguous latency target) before implementing?

Claude: Recommended. "Fast response time" is ambiguous—implementation
        could misinterpret as <500ms when you expect <100ms. Clarify now
        to prevent rework.

User: /specify "Update NFR-002: System MUST deliver messages with <100ms p95 latency"
[... spec.md updated ...]

User: /analyze
[... A1 issue resolved ...]

User: /implement
```

---

### If MEDIUM Issues Only

**Safe to proceed** with optional cleanup:

```
User: /implement

[... during implementation, Claude notices F1 terminology drift ...]

Claude: Note: Using "User" terminology per spec (data-model says "Account"
        but spec takes precedence per /analyze recommendation F1)
```

---

### If LOW Issues Only

**Ignore and proceed**:

```
User: /implement

[No action needed for LOW issues unless time permits cosmetic fixes]
```

---

## Best Practices

### 1. Always Run Before /implement

**Rationale**: Catching issues during analysis is **cheap** (edit text files). Catching issues during implementation is **expensive** (rewrite code, regenerate tests).

**Cost Comparison**:
- **Analysis Phase**: 2-5 minutes to run `/analyze`, 5-15 minutes to fix issues
- **Implementation Phase**: 30-60 minutes to rewrite code, 15-30 minutes to regenerate tests, 10-20 minutes to re-run validation

**ROI**: ~10x time savings by catching issues early

---

### 2. Remediate CRITICAL Issues Immediately

**Non-Negotiable**: CRITICAL issues block implementation success.

**Examples**:
- Constitution violations → Code won't align with principles
- Zero coverage for core requirements → Feature incomplete
- Conflicting requirements → Implementation will fail

**Action**: Stop, fix, re-validate, then proceed.

---

### 3. Consider HIGH Issues

**Trade-off**: HIGH issues may cause implementation confusion but don't strictly block progress.

**Decision Factors**:
- **Solo developer**: Can proceed if confident about interpretation
- **Team environment**: Remediate to ensure shared understanding
- **High-stakes feature**: Remediate to prevent expensive rework
- **Iterative prototyping**: Proceed with warnings, fix if issues surface

---

### 4. Review MEDIUM Issues

**Benefit**: Improves quality without blocking implementation.

**When to Fix**:
- **Before implementing**: If terminology drift could cause confusion
- **During implementing**: If Claude flags inconsistency during code generation
- **After implementing**: If time permits polish pass

---

### 5. Ignore LOW Issues (Unless Time Permits)

**Focus**: LOW issues are cosmetic—no functional impact.

**Action**: Defer to polish phase or ignore entirely.

---

## Importance of /analyze

### Why Run This Command?

**1. Catches Spec-Plan-Tasks Misalignment**

Without `/analyze`:
- Spec says FR-008 "Message encryption" → Plan includes encryption library → Tasks have zero encryption tasks
- **Result**: Feature incomplete, discovered during implementation (expensive fix)

With `/analyze`:
- **Detection**: C1 Coverage Gap flagged immediately
- **Remediation**: Add T38 encryption task before implementing
- **Result**: Complete feature, no rework

---

**2. Prevents Implementation Rework**

**Scenario**: Ambiguous NFR-002 "Fast response time"
- Developer implements with <500ms latency target
- Product manager expected <100ms real-time chat experience
- **Rework**: Re-implement message delivery, re-run performance tests

**With /analyze**:
- **Detection**: A1 Ambiguity flagged
- **Remediation**: Clarify NFR-002 to "<100ms p95 latency"
- **Result**: Correct implementation first time

---

**3. Enforces Constitution Compliance**

**Scenario**: Plan violates Test-First principle
- Implementation tasks (T010-T015) before test tasks (T005-T008)
- Developer writes code without contract tests (TDD violated)
- **Result**: Tests written after code (defeats TDD purpose)

**With /analyze**:
- **Detection**: CA1 Constitution violation (CRITICAL)
- **Remediation**: Reorder tasks.md
- **Result**: TDD enforced, tests before implementation

---

**4. Improves Team Communication**

**Scenario**: Terminology drift—spec says "User", plan says "Account"
- Developer implements `Account` model
- Frontend team expects `User` API
- **Result**: API mismatch, integration issues

**With /analyze**:
- **Detection**: F1 Inconsistency (MEDIUM)
- **Remediation**: Normalize to "User"
- **Result**: Consistent terminology, no integration issues

---

## Examples

### Example 1: Zero Issues (Success)

**Feature**: Simple CRUD API with clear requirements

**Input**:

```
User: /analyze
```

**Output**:

```
Running script: check-prerequisites.sh --json --require-tasks --include-tasks
✓ All required files present

Loading artifacts...
✓ Loaded spec.md (5 requirements)
✓ Loaded plan.md (3 phases)
✓ Loaded tasks.md (15 tasks)

Building semantic models...
✓ Requirements inventory (5 requirements)
✓ Task coverage mapping (15 tasks → requirements)

Running detection passes...
A. Duplication Detection: ✓ No duplicates
B. Ambiguity Detection: ✓ All clear
C. Underspecification: ✓ Complete
D. Constitution Alignment: ✓ Compliant
E. Coverage Gaps: ✓ 100% coverage
F. Inconsistency: ✓ Consistent

### Specification Analysis Report

✓ **All detection passes successful**

#### Metrics
- Total Requirements: 5
- Total Tasks: 15
- Coverage: 100%
- Issues: 0

### Next Actions

✓ Ready to proceed to /implement
```

---

### Example 2: Coverage Gap Detected

**Feature**: Real-time chat with missing encryption task

**Input**:

```
User: /analyze
```

**Output** (abbreviated):

```
Running detection passes...
E. Coverage Gaps: ⚠ 1 issue found

### Specification Analysis Report

| ID | Category | Severity | Location | Summary |
|----|----------|----------|----------|---------|
| C1 | Coverage | CRITICAL | spec.md FR-008 | Message encryption has zero tasks |

#### Coverage Summary

| Requirement Key    | Has Task? | Task IDs   | Notes                |
|--------------------|-----------|------------|----------------------|
| message-encryption | ✗         | —          | **CRITICAL: Missing**|

### Next Actions

✗ CRITICAL issues - Resolve before /implement

1. Add Task T38: Implement message encryption (addresses FR-008)

Would you like me to suggest concrete remediation?

User: Yes

Claude: **Suggested Task T38**:

- [ ] T38: Implement end-to-end message encryption [P]
  - Files: `src/crypto/encryption.py`, `tests/unit/test_encryption.py`
  - Description: Implement AES-256-GCM encryption using libsodium
  - Prerequisites: T006 (Message model complete)
  - Success criteria: Messages encrypted at rest, decrypted on retrieval
  - Addresses: FR-008

Shall I add this to tasks.md?

User: Yes

Claude: ✓ Added T38 to tasks.md Core Phase
        ✓ Re-running analysis...
        ✓ Coverage: 100% (8/8 requirements)
        ✓ Ready for /implement
```

---

### Example 3: Constitution Violation

**Feature**: Architecture violates Test-First principle

**Output** (abbreviated):

```
### Specification Analysis Report

| ID  | Category     | Severity | Location | Summary |
|-----|--------------|----------|----------|---------|
| CA1 | Constitution | CRITICAL | tasks.md | Test-First principle violated |

#### Constitution Alignment Issues

**CRITICAL: Test-First Principle Violation (Principle III)**

- **Location**: tasks.md T010-T015 before T005-T008
- **Issue**: Implementation tasks before contract tests
- **Constitution Text**: "Contract tests MUST be written before implementation"

### Next Actions

✗ Fix CA1: Reorder tasks.md (tests before implementation)

**Remediation**: Move T005-T008 from Core Phase to Setup Phase

User: Apply fix

Claude: ✓ Reordered tasks.md
        ✓ Setup Phase now includes T001-T008 (tests)
        ✓ Core Phase starts at T009 (implementation)
        ✓ Re-running analysis...
        ✓ Constitution compliance: PASS
        ✓ Ready for /implement
```

---

## References

### Related Commands

- [Page 08: /tasks Command](08-tasks-command.md) - Generate task breakdown (prerequisite for /analyze)
- [Page 10: /implement Command](10-implement-command.md) - Execute implementation (after /analyze validates)
- [Page 06: /clarify Command](06-clarify-command.md) - Resolve ambiguities proactively before planning
- [Page 03: /plan Command](03-plan-command.md) - Create design artifacts analyzed by this command

### Related Concepts

- **Coverage Gaps**: [KB: Commands Core](../kb/04-commands-core.md) - Task generation rules ensure coverage
- **Constitutional Gates**: [KB: Constitution](../kb/08-constitution.md) - Principles enforced during analysis
- **Semantic Models**: [KB: AI Patterns](../kb/09-ai-patterns.md) - How Claude builds requirement → task mappings
- **Detection Passes**: [KB: Commands Clarify](../kb/05-commands-clarify.md) - Detailed pass algorithms

### Script Reference

- **check-prerequisites.sh**: [KB: Bash Automation](../kb/07-bash-automation.md) - Validates required files exist
- **JSON Contracts**: [KB: Architecture](../kb/03-architecture.md) - How scripts communicate structured data

### Workflow Position

- **Before /analyze**: [Workflow Diagram](../kb/10-workflows.md#recommended-workflow) - Shows full command sequence
- **After /analyze**: [Page 10: /implement](10-implement-command.md) - Next step after validation passes

---

**Navigation**: [← Page 08: /tasks](08-tasks-command.md) | [Page 10: /implement →](10-implement-command.md)

---

## Summary

The `/analyze` command is a **critical quality gate** that validates cross-artifact consistency before implementation begins. It performs six systematic detection passes (Duplication, Ambiguity, Underspecification, Constitution Alignment, Coverage Gaps, Inconsistency) and assigns severity levels (CRITICAL/HIGH/MEDIUM/LOW) to prioritize remediation.

**Key Benefits**:
- Catches spec-plan-tasks misalignment early (cheap to fix)
- Prevents implementation rework from ambiguous requirements
- Enforces constitutional principles automatically
- Improves team communication through terminology consistency

**When to Run**: Always after `/tasks`, before `/implement` (10x ROI on time savings)

**Next Steps**: If zero issues or LOW/MEDIUM only → proceed to [/implement](10-implement-command.md). If CRITICAL issues → remediate, re-run `/analyze`, then proceed.
