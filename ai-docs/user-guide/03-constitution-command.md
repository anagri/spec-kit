# Page 03: /constitution - Project Governance

**Part of**: Spec Kit User Guide
**Audience**: Users setting up project governance
**Related Pages**: [02-specify-command.md](02-specify-command.md) (next step), [Quick Start](01-quick-start.md) (workflow context)

---

## Overview

The `/constitution` command creates your project's governance document - a living contract that defines architectural principles, technology constraints, and quality gates. Think of it as a "type system for architecture" that enforces rules before implementation begins.

**When to Run**: Once per project, at the very start (before any features)

**Why It Matters**: The constitution establishes guardrails that protect architectural decisions throughout development. Every feature's implementation plan will be validated against these principles via constitutional gates.

---

## What It Does

### User Action

```bash
/constitution "principle 1; principle 2; principle 3; ..."
```

You provide 4-8 architectural principles in natural language. The command:

1. Loads the constitution template from `.specify/memory/constitution.md`
2. Identifies all placeholder tokens (`[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`, etc.)
3. Fills placeholders with concrete values from your input or repository context
4. Marks ambiguous sections with `[NEEDS CLARIFICATION]` if information is missing
5. Assigns a semantic version (starts at v1.0.0 for new constitutions)
6. Updates dependent templates (plan-template.md, spec-template.md, tasks-template.md)
7. Writes the completed constitution back to `.specify/memory/constitution.md`

### Input Required

Provide **4-8 project principles** as semicolon-separated text. Each principle should capture:

- **Architectural rules** (e.g., "Library-first architecture - every feature starts as standalone library")
- **Technology constraints** (e.g., "Python 3.11+ only; FastAPI for APIs; PostgreSQL for persistence")
- **Quality gates** (e.g., "TDD mandatory - contract tests written and approved before implementation")
- **Process requirements** (e.g., "CLI interfaces required for all libraries to enable automation")

**Examples**:

```bash
# Minimal (4 principles)
/constitution "Library-first architecture; CLI interfaces mandatory; Test-driven development; Python 3.11+ only"

# Comprehensive (6 principles)
/constitution "Library-first: features start as standalone libraries; CLI interfaces: text I/O protocol for automation; TDD mandatory: contract tests before implementation; Observability: structured logging required; Versioning: semantic versioning for breaking changes; Simplicity: YAGNI principles enforced"

# Interactive (no arguments - Claude will ask questions)
/constitution
```

---

## Execution Process

### Step-by-Step Flow

```
1. Load constitution template
   ↓
2. Parse user input for principles
   ↓
3. For each placeholder:
   - Use provided value if available
   - Infer from repo context (README, docs) if possible
   - Mark [NEEDS CLARIFICATION: hint] if ambiguous
   ↓
4. Assign semantic version
   - v1.0.0 for new constitutions
   - Increment by MAJOR/MINOR/PATCH rules for updates
   ↓
5. Update dependent templates
   - plan-template.md: Constitutional gates
   - spec-template.md: Constraints section
   - tasks-template.md: Task ordering rules
   ↓
6. Write constitution file with metadata
   ↓
7. Report completion status
```

### What You'll See

**Terminal Output Example** (Success Complete):

```
Constitution created at .specify/memory/constitution.md

Version: 1.0.0 (new constitution)

✓ All sections complete
✓ 6 principles defined
✓ Dependent templates updated

Next command: /specify

Suggested commit message:
docs: create project constitution v1.0.0

The constitution will enforce these principles via gates during /plan.
```

**Terminal Output Example** (Success Partial):

```
Constitution created at .specify/memory/constitution.md

Version: 1.0.0 (new constitution)

⚠ Incomplete Sections (3):
- Performance targets (Principle IV)
- Technology stack version constraints
- Governance amendment procedure

Next command: /clarify-constitution

The clarification command will ask targeted questions to complete these sections
without making assumptions.
```

---

## All Possible Outcomes

### 1. Success Complete

**Condition**: All placeholders filled, no ambiguities detected

**Result**:
- Constitution file created with version 1.0.0
- All principle sections populated with concrete rules
- Governance section includes ratification date (today)
- Session metadata: `<!-- Clarification Sessions: 0 -->`

**Next Step**: `/specify` to start defining your first feature

**Example Constitution Structure**:

```markdown
# TaskFlow Project Constitution

## Core Principles

### I. Library-First Architecture

Every feature MUST begin as a standalone library with:
- Clear boundaries and single responsibility
- Independent testability without external dependencies
- Self-contained documentation

**Rationale**: Enables reusability, testing isolation, and clear architectural boundaries.
**Enforcement**: Constitution Check gate in /plan verifies library boundaries before Phase 0.

### II. CLI Interfaces

All libraries MUST expose CLI interfaces with:
- Text input/output protocol (stdin/args → stdout, errors → stderr)
- JSON format support for machine parsing
- Human-readable output for manual usage

**Rationale**: Enables scriptability, CI/CD integration, and headless workflows.
**Enforcement**: plan.md validates text I/O protocol in Technical Context section.

### III. Test-Driven Development (NON-NEGOTIABLE)

Contract tests MUST be written and approved before implementation:
- Tests written first → User approves → Tests fail → Then implement
- Red-Green-Refactor cycle strictly enforced
- No implementation without passing contract tests

**Rationale**: Prevents rework, ensures testability, validates design before coding.
**Enforcement**: /tasks generates test tasks before implementation tasks; /implement executes tests first.

### IV. Observability

All components MUST include:
- Structured logging with consistent format (JSON Lines)
- Error context propagation via traceback IDs
- Performance metrics for critical paths (<100ms p95 latency)

**Rationale**: Debuggability in production, performance monitoring, incident response.
**Enforcement**: plan.md includes logging strategy; tasks.md includes observability tasks.

### V. Versioning and Breaking Changes

Semantic versioning (MAJOR.MINOR.PATCH) required for all libraries:
- MAJOR: Breaking changes (removed/changed API contracts)
- MINOR: New features (backward compatible additions)
- PATCH: Bug fixes, internal refactoring

**Rationale**: Clear communication of impact, safe dependency management.
**Enforcement**: CHANGELOG.md required; breaking changes documented in migration guide.

### VI. Simplicity (YAGNI)

Features start with simplest implementation that meets requirements:
- No speculative generalization
- Justify each abstraction layer
- Refactor only when duplication causes maintenance burden

**Rationale**: Faster delivery, easier maintenance, lower cognitive load.
**Enforcement**: Complexity Tracking table in plan.md documents each abstraction with justification.

## Governance

**Amendment Procedure**: Constitution changes require version bump, CHANGELOG entry, and approval.

**Compliance Review**: All /plan outputs must pass Constitution Check gates. Violations require:
1. Documentation in Complexity Tracking table
2. Justification for why simpler approach won't work
3. Mitigation plan for accepted complexity

**Version**: 1.0.0 | **Ratified**: 2025-10-17 | **Last Amended**: 2025-10-17
<!-- Clarification Sessions: 0 -->
```

---

### 2. Success Partial (with Markers)

**Condition**: Some placeholders lack sufficient information

**Result**:
- Constitution file created with version 1.0.0
- Completed sections filled with concrete rules
- Ambiguous sections marked with `[NEEDS CLARIFICATION: specific question]`
- Session metadata: `<!-- Clarification Sessions: 0 -->`

**Next Step**: `/clarify-constitution` to resolve markers interactively

**Example Markers**:

```markdown
### IV. Performance Standards

System MUST meet performance targets:
- Response latency: [NEEDS CLARIFICATION: target p95 latency?]
- Throughput: [NEEDS CLARIFICATION: requests per second?]
- Concurrent users: [NEEDS CLARIFICATION: expected scale?]

**Rationale**: [NEEDS CLARIFICATION: business justification for performance requirements?]
**Enforcement**: Performance tests validate targets before deployment.
```

**Why Markers Are Good**: They prevent Claude from hallucinating requirements (e.g., assuming "100ms latency" when you actually need "10ms" for real-time systems).

---

### 3. Error: Invalid Template Path

**Condition**: `.specify/memory/constitution.md` template not found

**Result**:
```
ERROR: Constitution template not found at .specify/memory/constitution.md

Did you run 'speclaude init' to set up the project?

Suggested action:
cd /path/to/project
speclaude init --here
```

**Fix**: Run `speclaude init --here` to download templates from GitHub releases

---

### 4. Error: Placeholder Resolution Failure

**Condition**: Template contains malformed placeholders (e.g., `[UNCLOSED_BRACKET`)

**Result**:
```
ERROR: Failed to parse constitution template

Malformed placeholder at line 23: [UNCLOSED_BRACKET

Suggested action:
Verify .specify/memory/constitution.md is not corrupted.
Re-run 'speclaude init --force' to restore original template.
```

**Fix**: Restore template with `speclaude init --force` or manually fix malformed syntax

---

## Semantic Versioning Rules

The constitution itself is versioned using semantic versioning to communicate impact of governance changes.

### Version Bump Decision Tree

```
Did principle semantics change?
├─ No  → PATCH (wording clarity, typo fixes)
└─ Yes
   ├─ Backward compatible? (old features still valid)
   │  └─ Yes → MINOR (new principle added, expanded guidance)
   └─ No → MAJOR (principle removed or redefined)
```

### Version Examples

**MAJOR (1.0.0 → 2.0.0)**: Breaking governance changes
- Remove NON-NEGOTIABLE Test-First principle (now optional)
- Change Principle I from "Library-first" to "Monolith-first"
- Redefine "Simplicity" to allow speculative abstractions

**MINOR (1.0.0 → 1.1.0)**: New principle or expanded guidance
- Add Principle VII: Security Review Gate
- Expand Principle IV with specific observability requirements
- Add new Governance section: Compliance Review Process

**PATCH (1.0.0 → 1.0.1)**: Clarifications without semantic change
- Fix typo in Principle III description
- Add examples to Simplicity enforcement section
- Clarify "standalone library" definition

### Why Version the Constitution?

Principles are **executable constraints** that affect system behavior. Changing principles changes how features are validated during `/plan`. Versioning communicates impact:

- **v1.0.0 → v2.0.0**: Features developed under v1.0.0 may violate v2.0.0 principles
- **v1.0.0 → v1.1.0**: New principles added; old features remain valid
- **v1.0.0 → v1.0.1**: Pure clarification; no behavioral change

---

## Follow-up Actions

### If Markers Exist

**Run**: `/clarify-constitution` to resolve ambiguities interactively

**What Happens**:
1. Claude identifies all `[NEEDS CLARIFICATION]` markers
2. Asks up to 5 targeted questions (one at a time)
3. Integrates your answers directly into constitution sections
4. Increments clarification session counter
5. Reports completion when all markers resolved

**Example Session**:

```
Question 1 of 3: Performance Targets

What is the target p95 response latency for API endpoints?

A) <50ms (real-time requirements)
B) <100ms (standard web application)
C) <500ms (batch processing acceptable)
D) Other (please specify)

Your answer: B

✓ Updated Principle IV with "System MUST meet <100ms p95 latency for API endpoints"

Question 2 of 3: Throughput...
```

---

### If Complete (No Markers)

**Run**: `/specify "<feature description>"` to start your first feature

**What Happens**:
1. Feature specification created in `specs/001-feature-name/spec.md`
2. Specification validated against constitution constraints
3. Ambiguities marked with `[NEEDS CLARIFICATION]` in spec
4. Ready for `/clarify` (optional) or `/plan` (next required step)

---

## Best Practices

### 1. Define 4-6 Principles (Not Too Few/Many)

**Too Few (<4)**:
- Insufficient architectural guidance
- Constitutional gates too permissive
- Teams drift in different directions

**Too Many (>8)**:
- Analysis paralysis during /plan
- High maintenance burden (every principle needs enforcement)
- Developers bypass gates to make progress

**Sweet Spot (4-6)**:
- Cover critical architectural decisions
- Manageable enforcement overhead
- Clear communication of priorities

---

### 2. Mix MUST (Non-Negotiable) and SHOULD (Recommended)

**MUST Principles**: Violations block progress unless justified

```markdown
### III. Test-Driven Development (NON-NEGOTIABLE)

Contract tests MUST be written and approved before implementation.

**Enforcement**: /plan will ERROR if tests are not planned before implementation tasks.
```

**SHOULD Principles**: Violations require justification but don't block

```markdown
### VI. Simplicity

Features SHOULD start with simplest implementation meeting requirements.

**Enforcement**: Complexity Tracking table documents abstractions with justification.
```

**Guidance**:
- Use MUST for critical constraints (security, testing, architecture)
- Use SHOULD for quality improvements (observability, performance, style)
- Limit NON-NEGOTIABLE to 1-2 principles (highest priority)

---

### 3. Avoid Vague Language

**Bad Examples** (unmeasurable):
- "System must be fast"
- "Code should be maintainable"
- "Performance must be good"

**Good Examples** (measurable criteria):
- "System MUST respond within <100ms p95 latency for API endpoints"
- "Code coverage MUST exceed 80% for core business logic"
- "Throughput MUST support 1000 req/s sustained load"

**Pattern**: Replace adjectives with metrics
- Fast → <Xms latency
- Maintainable → <Y cyclomatic complexity
- Scalable → Z concurrent users supported

---

### 4. Include Enforcement Mechanism

Every principle needs a validation method:

```markdown
### Principle: CLI Interfaces Mandatory

**Enforcement**:
1. plan.md validates text I/O protocol in Technical Context section
2. contracts/ must include CLI contract specifications
3. tasks.md generates CLI integration tests
4. /implement executes CLI contract tests before implementation
```

**Enforcement Types**:
- **Template Gates**: Constitutional Check in /plan template validates principles
- **Task Generation**: /tasks creates enforcement tasks (e.g., performance tests)
- **Test Execution**: /implement runs validation tests (e.g., contract tests)
- **Manual Review**: Code review checklist verifies compliance

---

### 5. Document Rationale

Explain **why** each principle exists:

```markdown
### II. Solo Developer Workflow

**Rationale**:
- Solo developers work directly on main (no merge conflicts)
- Branch creation adds ceremony without team coordination benefit
- Faster iteration without branch switching overhead

**Trade-off Accepted**: No true isolation for experimenting with breaking changes. Users can create branches manually if needed.
```

**Benefits**:
- Future maintainers understand context
- Principle amendments consider original intent
- Trade-offs are explicit (not forgotten)

---

## Common Issues

### Issue 1: Too Many Principles (>8)

**Symptom**: Constitutional gates take 10+ minutes, developers complain about process

**Fix**:
1. Merge related principles (e.g., "Testing" + "TDD" → single "Test-First" principle)
2. Demote SHOULD principles to team guidelines (not constitution)
3. Focus on architectural constraints, not style preferences

**Example Consolidation**:

Before (10 principles):
```
I. Library-First
II. CLI Interfaces
III. TDD
IV. Unit Tests
V. Integration Tests
VI. Contract Tests
VII. Observability
VIII. Logging
IX. Metrics
X. Versioning
```

After (5 principles):
```
I. Library-First Architecture
II. CLI Interfaces
III. Test-First Development (TDD + contract/integration/unit tests)
IV. Observability (logging + metrics + tracing)
V. Versioning and Breaking Changes
```

---

### Issue 2: Principles Without Measurable Criteria

**Symptom**: Constitutional gates pass even when principles are violated (subjective interpretation)

**Fix**: Add acceptance criteria to each principle

**Before** (unmeasurable):
```markdown
### Simplicity

Code should be simple and maintainable.
```

**After** (measurable):
```markdown
### Simplicity (YAGNI)

Features start with simplest implementation:
- Max 3 abstraction layers for any feature
- Cyclomatic complexity <10 per function
- Zero unused code (detected by coverage tools)
- Each abstraction justified in Complexity Tracking table

**Enforcement**: /plan Complexity Tracking table documents each layer with justification.
```

---

### Issue 3: No Enforcement Mechanism

**Symptom**: Constitution exists but is never checked (aspirational document)

**Fix**: Wire principles into template gates

**Before** (aspirational):
```markdown
### Security

All APIs should be secure.
```

**After** (enforced):
```markdown
### Security

All APIs MUST include:
- Authentication: JWT tokens with expiration
- Authorization: Role-based access control (RBAC)
- Input validation: Schema validation for all requests
- Rate limiting: Max 100 req/min per user

**Enforcement**:
1. plan.md Security section documents auth/authz approach
2. contracts/ include security schemas (JWT claims, RBAC roles)
3. tasks.md generates security test tasks
4. /implement executes security contract tests before API implementation
```

**Template Integration**: Update `plan-template.md` with Security Gate:

```markdown
## Constitution Check

### Security Gate (Principle IV)
- [ ] Authentication mechanism specified? (JWT/OAuth/API keys)
- [ ] Authorization model defined? (RBAC/ABAC/ACL)
- [ ] Input validation approach documented?
- [ ] Rate limiting strategy planned?

**Result**: PASS/FAIL with justification
```

---

### Issue 4: Conflicting Principles

**Symptom**: Principle I requires X, Principle III requires NOT X (impossible to pass gates)

**Example Conflict**:
```markdown
### I. Library-First
Every feature MUST start as standalone library (no external dependencies).

### III. Reusability
All features MUST reuse existing shared libraries to avoid duplication.
```

**Fix**: Resolve conflict with priority order or clarification

**Option 1: Priority Order**:
```markdown
### I. Library-First (Priority 1)
Features start as standalone libraries...

### III. Reusability (Priority 2)
After initial implementation, refactor to reuse shared libraries if:
- Duplication exceeds 3 features
- Shared library has stable contract (v1.0.0+)
```

**Option 2: Clarification**:
```markdown
### I. Library-First
Every feature starts as standalone library with:
- Clear boundaries (single responsibility)
- Minimal external dependencies (only infrastructure: DB, cache, queue)
- Testability without full system setup

**Note**: Infrastructure dependencies (PostgreSQL, Redis) are permitted. Feature dependencies (other domain libraries) require justification.
```

---

## Importance

### Why Constitution Matters

The constitution is not documentation - it's an **executable constraint system** enforced at runtime.

**Without Constitution**:
- Every feature makes ad-hoc architectural decisions
- Inconsistent patterns across codebase (REST + GraphQL + gRPC mixed randomly)
- No mechanism to prevent complexity creep
- Refactoring becomes high-risk (no guardrails)

**With Constitution**:
- Architectural decisions codified once, enforced automatically
- Consistent patterns (every library has CLI, every API has auth)
- Complexity requires explicit justification (Complexity Tracking table)
- Refactoring safe (constitution ensures new design aligns with principles)

---

### Constitutional Gates in Action

During `/plan`, Claude evaluates your design against constitution principles:

```markdown
## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Library-First Gate (Principle I)
- [✓] Feature begins as standalone library
- [✓] Clear boundaries defined (Message + Room entities)

### CLI Interface Gate (Principle II)
- [✓] Text I/O protocol specified (JSON Lines)
- [✓] Supports both machine parsing and human-readable output

### Test-First Gate (Principle III - NON-NEGOTIABLE)
- [✓] Contract tests planned before implementation (tasks.md: T005, T013-T015)
- [✓] Red-Green-Refactor cycle enforced (tests fail initially)

### Observability Gate (Principle IV)
- [✗] VIOLATION: No structured logging strategy documented

**Resolution**: Documented in Complexity Tracking table (see below)

**Result**: PASS (with documented exception)
```

**Complexity Tracking Table** (violation justification):

```markdown
| Violation | Why Needed | Simpler Alternative Rejected Because | Accepted? |
|-----------|------------|--------------------------------------|-----------|
| Missing structured logging (Principle IV) | MVP focuses on core chat functionality; logging deferred to Phase 2 | Adding logging now adds 5 tasks and 2 days | ✓ Deferred to next sprint |
```

---

### Impact on Development Workflow

```
Feature Specification (spec.md)
         ↓
Implementation Plan (plan.md)
         ↓
    [Constitution Check Gate]  ← Validates principles
         ↓
   PASS → Continue to Phase 0
   FAIL → Document in Complexity Tracking OR refactor design
         ↓
Task Breakdown (tasks.md)
         ↓
Implementation (code)
```

**Key Benefit**: Architectural violations caught **before implementation**, not during code review.

---

## References

### Source Files

- **Command Implementation**: `templates/commands/constitution.md` (lines 1-116)
  - Execution flow: lines 13-76
  - Placeholder resolution rules: lines 19-29
  - Sync impact report format: lines 50-56
  - Validation requirements: lines 58-62

- **Constitution Template**: `memory/constitution.md` (lines 1-50)
  - Placeholder tokens: lines 1, 6, 12, 18, 24 (`[PRINCIPLE_X_NAME]`)
  - Section structure: lines 4-30 (Core Principles)
  - Governance section: lines 43-46
  - Version metadata: line 49

- **Constitutional Enforcement**: `ai-docs/kb/08-constitution.md` (lines 29-63, 403-480)
  - Constitution as type system: lines 29-63
  - Constitutional gates in templates: lines 403-457
  - Version semantics: lines 482-516

- **Command Reference**: `ai-docs/kb/04-commands-core.md` (lines 37-146)
  - Purpose and workflow: lines 37-48
  - Execution process: lines 55-64
  - Key features: lines 73-97
  - Example output structure: lines 113-140

### Related Commands

- **Next Step (if markers)**: [/clarify-constitution](04-clarify-constitution-command.md) - Resolve governance ambiguities
- **Next Step (if complete)**: [/specify](02-specify-command.md) - Create first feature specification
- **Constitutional Enforcement**: Constitutional gates validated during `/plan` command

### Template Dependencies

Files updated by `/constitution` command:

1. `.specify/memory/constitution.md` - Primary output (governance document)
2. `.specify/templates/plan-template.md` - Constitutional Check gates updated to match principles
3. `.specify/templates/spec-template.md` - Constraints section updated with principle references
4. `.specify/templates/tasks-template.md` - Task ordering rules updated to enforce principles (e.g., test-first)

---

## Example: Real-Time Chat Constitution

**User Input**:

```bash
/constitution "Library-first architecture: features as standalone libraries; CLI interfaces: text I/O for automation; TDD mandatory: contract tests before code; FastAPI + PostgreSQL + Redis stack; Performance: <100ms p95 latency, 1000 req/s; Simplicity: YAGNI enforced"
```

**Generated Constitution** (abbreviated):

```markdown
# Real-Time Chat System Constitution

## Core Principles

### I. Library-First Architecture

Every feature MUST begin as standalone library with clear boundaries, independent testability, and self-contained documentation.

**Rationale**: Enables reusability, testing isolation, clear architectural boundaries.
**Enforcement**: Constitution Check gate in /plan verifies library boundaries before Phase 0.

### II. CLI Interfaces

All libraries MUST expose text I/O protocol: stdin/args → stdout (JSON + human-readable), errors → stderr.

**Rationale**: Scriptability, CI/CD integration, headless workflows.
**Enforcement**: plan.md validates text I/O protocol in Technical Context section.

### III. Test-Driven Development (NON-NEGOTIABLE)

Contract tests written and approved → Tests fail → Implement → Tests pass.

**Rationale**: Prevents rework, ensures testability, validates design.
**Enforcement**: /tasks generates test tasks before implementation; /implement executes tests first.

### IV. Technology Stack

- **Language**: Python 3.11+
- **Web Framework**: FastAPI (async/await)
- **Database**: PostgreSQL 15+ (asyncpg driver)
- **Cache/Queue**: Redis 7+ (Pub/Sub for message routing)

**Rationale**: Proven production stack, excellent async support, strong ecosystem.
**Enforcement**: plan.md Technical Context section validates stack choices.

### V. Performance Standards

System MUST meet:
- **Latency**: <100ms p95 for API endpoints
- **Throughput**: 1000 req/s sustained load
- **Concurrency**: 10k WebSocket connections

**Rationale**: Real-time chat requires low latency and high concurrency.
**Enforcement**: tasks.md includes performance test task; /implement validates targets.

### VI. Simplicity (YAGNI)

Features start with simplest implementation. Each abstraction layer justified in Complexity Tracking table.

**Rationale**: Faster delivery, easier maintenance, lower cognitive load.
**Enforcement**: plan.md Complexity Tracking documents abstractions with rationale.

## Governance

**Amendment Procedure**: Version bump + CHANGELOG entry required for principle changes.

**Compliance Review**: /plan Constitution Check gates validate all principles. Violations require justification.

**Version**: 1.0.0 | **Ratified**: 2025-10-17 | **Last Amended**: 2025-10-17
<!-- Clarification Sessions: 0 -->
```

**Next Command**: `/specify "Real-time chat with message history and room management"`

---

**Navigation**: [← Quick Start](01-quick-start.md) | [/specify Command →](02-specify-command.md)
