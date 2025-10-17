# Page 07: /plan - Implementation Planning

**Purpose**: Transform feature requirements into technical design with architectural validation
**Phase**: Planning (bridges Specification → Execution)
**Prerequisites**: Feature specification created via `/specify`
**Output**: 6 design artifacts + constitutional validation

---

## Overview

The `/plan` command is the **architectural gateway** between requirements and implementation. It transforms your feature specification into a complete technical design while enforcing your project's constitutional principles through dual validation gates.

**Core Function**: Generate implementation strategy, technology decisions, data models, API contracts, and test scenarios—all validated against your project constitution before proceeding to task generation.

**Why This Matters**: Planning catches architectural violations early (cheap to fix) before they become implementation debt (expensive to fix). Constitutional gates ensure every feature aligns with your project principles.

---

## Command Usage

### Basic Syntax

```
/plan "tech stack description"
```

### Arguments

**Tech Stack Description** (optional but recommended):
Provide language, framework, database, and scale targets to guide research phase.

**Examples**:
```
/plan "Python 3.11, FastAPI, PostgreSQL, 10k concurrent users"
/plan "TypeScript, React 18, Node.js 20, MongoDB, serverless"
/plan "Rust 1.75, Axum, SQLite, embedded system"
/plan "Go 1.21, Gin, Redis, 1M requests/day"
```

**No Arguments**:
```
/plan
```
Claude will infer tech stack from existing codebase or ask clarifying questions.

---

## Execution Flow

### Phase 0: Pre-Research Setup

```
1. Run setup-plan.sh --json
   → Receives: FEATURE_SPEC, IMPL_PLAN, FEATURE_DIR paths

2. Load feature specification (spec.md)
   → Parse requirements, entities, user stories

3. Clarification Check (Quality Gate)
   → Verify spec.md contains "## Clarifications" section
   → If missing + ambiguities detected:
     WARNING: "Run /clarify first to reduce rework"
   → User can override: "proceed without clarification"

4. Load constitution (.specify/memory/constitution.md)
   → Parse principles, gates, enforcement rules

5. Fill Technical Context
   → From arguments: "Python 3.11, FastAPI, PostgreSQL"
   → From spec: Performance targets, constraints
   → Result: Structured tech requirements
```

**Terminal Output Example**:
```
Running script: setup-plan.sh --json
✓ Received feature paths

Loading spec.md...
✓ 8 functional requirements
✓ 3 key entities
✓ 2 user scenarios

⚠ CLARIFICATION CHECK:
  Spec missing "## Clarifications" section
  Detected ambiguous requirements:
    - FR-003: "fast delivery" (no latency target)
    - FR-006: "scalable architecture" (no scale metrics)

  Recommendation: Run /clarify first to resolve ambiguities
  Continue anyway? (increases rework risk)

User: proceed

Loading constitution...
✓ 6 principles loaded
```

---

### Phase 1: Constitutional Gates (Pre-Research)

**6 Gates Evaluated Before Phase 0 Begins**:

```
Constitution Check (Pre-Research Gate)
--------------------------------------
Evaluating against 6 principles...

✓ Library-First Gate (Principle I)
  - Feature starts as standalone library? YES
  - Clear library boundaries defined? YES

✓ CLI Interface Gate (Principle II)
  - Text input/output protocol? YES
  - JSON format support planned? YES

✓ Test-First Gate (Principle III - NON-NEGOTIABLE)
  - Contract tests before implementation? YES
  - Tests validated and approved? PENDING (will validate in /tasks)

✓ Integration Testing Gate (Principle IV)
  - Real database in tests (no mocks)? YES
  - End-to-end scenarios defined? YES

✓ Simplicity Gate (Principle V)
  - Maximum 3 projects respected? YES (single project)
  - No unnecessary abstractions? YES

✓ Anti-Abstraction Gate (Principle VI)
  - Using framework directly? YES
  - No wrapper classes planned? YES

Constitution Check: PASS (6/6 gates)
→ Proceeding to Phase 0: Research
```

**Gate Failure Example**:
```
✗ Anti-Abstraction Gate (Principle VI)
  - No wrapper abstractions? FAIL
  Detected: Plan includes "DatabaseWrapper class wrapping SQLAlchemy"

ERROR: Constitution violation detected
  Principle: VI. Anti-Abstraction (no wrapper abstractions)
  Violation: Creating DatabaseWrapper class

Recommendation:
  1. Use SQLAlchemy directly in services
  2. OR document in Complexity Tracking table:
     - Why wrapper needed (specific problem)
     - Simpler alternatives rejected (why direct usage insufficient)

Would you like to:
  A) Revise plan to remove abstraction
  B) Document justification in Complexity Tracking
```

**User Response to Gate Failure**:
```
User: A - remove abstraction

Claude: Revising plan...
✓ Removed DatabaseWrapper class
✓ Updated to use SQLAlchemy directly in services
✓ Re-evaluating Constitution Check...
✓ PASS (6/6 gates)
→ Proceeding to Phase 0: Research
```

---

### Phase 2: Research (Phase 0)

```
Phase 0: Research & Technology Decisions
-----------------------------------------
Analyzing Technical Context...

Researching: WebSocket libraries for Python
✓ Compared: websockets, FastAPI WebSocket, Socket.IO
✓ Decision: FastAPI WebSocket (native integration)

Researching: PostgreSQL schema design for chat
✓ Compared: JSONB vs relational for messages
✓ Decision: Hybrid (relational + JSONB metadata)

Researching: Redis Pub/Sub vs message queues
✓ Compared: Redis, RabbitMQ, Kafka
✓ Decision: Redis Pub/Sub (scale target: 10k users)

Created: research.md
  - 3 technology decisions with rationale
  - 6 alternatives considered and rejected
  - Trade-offs documented
```

**Generated Artifact**: `research.md`

```markdown
# Research: Real-Time Chat

## Technology Decisions

### WebSocket Library
**Decision**: Use FastAPI WebSocket support + Starlette
**Rationale**:
- Native integration with existing FastAPI setup
- Well-documented, production-ready
- Supports async/await patterns
**Alternatives Considered**:
- Socket.IO: Additional dependency, overkill for requirements
- Raw websockets library: Lower-level, more boilerplate

### Message Queue
**Decision**: Redis Pub/Sub
**Rationale**:
- Simple, fast, sufficient for 10k concurrent users
- Supports horizontal scaling with Redis Cluster
- Low latency (<10ms) for message routing
**Alternatives Considered**:
- RabbitMQ: More complex setup, unnecessary for scale
- Kafka: Overkill for message volume, adds operational overhead
```

---

### Phase 3: Design & Contracts (Phase 1)

```
Phase 1: Design & Contracts Generation
---------------------------------------
Extracting entities from spec.md...
✓ Created data-model.md
  - 3 entities: Message, Room, User
  - 12 fields with types and constraints
  - 4 relationships
  - 2 indexes for performance

Generating API contracts from requirements...
✓ Created contracts/websocket-events.yaml
  - 4 events: message.send, message.receive, user.join, user.leave
✓ Created contracts/rest-endpoints.yaml
  - 6 endpoints: POST /rooms, GET /rooms, POST /messages, GET /messages/:id, etc.

Extracting test scenarios from user stories...
✓ Created quickstart.md
  - 5 integration test scenarios
  - Step-by-step validation flows

Running: update-agent-context.sh claude
✓ Updated CLAUDE.md with tech stack
  - Added: Python 3.11, FastAPI, PostgreSQL, Redis
  - Added: Recent changes (plan.md generated)
```

**Generated Artifacts** (5 files):

1. **data-model.md** - Entity definitions
```markdown
# Data Model: Real-Time Chat

## Entities

### Message
**Fields**:
- `message_id`: UUID (PK)
- `room_id`: UUID (FK → Room)
- `sender_id`: UUID (FK → User)
- `text`: TEXT (NOT NULL)
- `metadata`: JSONB (default '{}')
- `created_at`: TIMESTAMP (NOT NULL)

**Indexes**:
- `idx_room_created`: (room_id, created_at DESC) for history queries

**Relationships**:
- Many-to-One with Room
- Many-to-One with User (sender)
```

2. **contracts/websocket-events.yaml** - WebSocket event specs
```yaml
events:
  message.send:
    payload:
      room_id: uuid
      text: string (max 5000)
    response:
      message_id: uuid
      timestamp: datetime

  message.receive:
    payload:
      message_id: uuid
      room_id: uuid
      sender_id: uuid
      text: string
      timestamp: datetime
```

3. **contracts/rest-endpoints.yaml** - REST API specs
```yaml
openapi: 3.0.0
paths:
  /messages:
    post:
      summary: Send a message
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [room_id, text]
              properties:
                room_id: {type: string, format: uuid}
                text: {type: string, maxLength: 5000}
      responses:
        "201":
          description: Message created
```

4. **quickstart.md** - Integration test scenarios
```markdown
# Quickstart: Real-Time Chat

## Scenario 1: Send Message
1. User authenticates via OAuth2
2. User joins room "general"
3. User sends message "Hello world"
4. Verify: Message delivered to all room participants within <100ms
5. Verify: Message persisted in database

## Scenario 2: Real-Time Delivery
1. User A and User B join room "test"
2. User A sends message
3. Verify: User B receives message via WebSocket within <100ms
4. Verify: Message appears in User B's message history
```

5. **CLAUDE.md** (updated) - Project context
```markdown
<!-- BEGIN AUTOGENERATED CONTEXT -->
# Feature Context: Real-Time Chat (001-real-time-chat)

**Tech Stack**:
- Language: Python 3.11
- Framework: FastAPI
- Database: PostgreSQL 15
- Cache: Redis 7
- Testing: pytest, httpx

**Recent Changes**:
- 2025-10-17: Generated implementation plan (plan.md)
- Performance target: <100ms message delivery
- Scale target: 10k concurrent users
<!-- END AUTOGENERATED CONTEXT -->
```

---

### Phase 4: Constitutional Gates (Post-Design)

**Re-Validation After Phase 1**:

```
Constitution Check (Post-Design Gate)
-------------------------------------
Re-evaluating against 6 principles after design...

✓ Library-First Gate (Principle I)
  - Library boundaries maintained? YES
  - src/chat/ is standalone module? YES

✓ CLI Interface Gate (Principle II)
  - CLI interface designed? YES
  - JSON input/output protocol? YES

✓ Test-First Gate (Principle III)
  - Contract tests planned? YES
  - Tests reference contracts/? YES

✓ Integration Testing Gate (Principle IV)
  - Real PostgreSQL/Redis in tests? YES
  - No mocks for external dependencies? YES

✓ Simplicity Gate (Principle V)
  - Single project structure? YES
  - Avoided 4th project? YES

✓ Anti-Abstraction Gate (Principle VI)
  - Using FastAPI directly? YES
  - No new wrapper classes? YES

Constitution Check: PASS (6/6 gates)
→ Ready for Phase 2 description
```

**New Violation Introduced During Design**:
```
✗ Simplicity Gate (Principle V)
  - Maximum 3 projects respected? FAIL
  Detected: Phase 1 design includes 4th project "chat-admin"

ERROR: New constitutional violation introduced in design
  Before Phase 1: 3 projects (passed gate)
  After Phase 1: 4 projects (violation)

Recommendation:
  1. Refactor: Merge "chat-admin" into main "chat" project
  2. OR justify in Complexity Tracking table

Action required: Refactor design to pass gate OR document exception
```

---

### Phase 5: Task Generation Approach (Phase 2 Description)

**IMPORTANT**: `/plan` command **DOES NOT** create `tasks.md`. It only **describes** the approach.

```
Phase 2: Task Planning Approach (Description Only)
---------------------------------------------------
The /tasks command will generate tasks using this strategy:

Task Generation Rules:
- Each contract → contract test task [P]
- Each entity → model creation task [P]
- Each endpoint → implementation task (sequential if shared files)
- Each user story → integration test [P]

Ordering Strategy:
- TDD order: Tests before implementation
- Dependency order: Models → Services → Endpoints
- Mark [P] for parallel execution (independent files)

Estimated Output: 35-40 numbered tasks in tasks.md

NOTE: This is a description. Run /tasks to generate actual tasks.md
```

---

### Phase 6: Completion Report

```
Plan complete at specs/001-real-time-chat/plan.md

Artifacts Generated:
1. plan.md - Implementation strategy (this file)
2. research.md - Technology decisions with rationale
3. data-model.md - 3 entities, 12 fields, 4 relationships
4. contracts/websocket-events.yaml - 4 WebSocket events
5. contracts/rest-endpoints.yaml - 6 REST endpoints
6. quickstart.md - 5 integration test scenarios
7. CLAUDE.md (updated) - Tech stack context added

Constitutional Validation:
✓ Pre-Research Gate: PASS (6/6)
✓ Post-Design Gate: PASS (6/6)
✓ No complexity deviations

Progress Tracking:
✓ Phase 0: Research complete
✓ Phase 1: Design complete
✓ Phase 2: Task approach described
- Phase 3: Tasks pending (/tasks command)
- Phase 4: Implementation pending (/implement command)

Next Command: /tasks
```

---

## All Possible Outcomes

### 1. Success (Ideal Path)

```
✓ Spec loaded successfully
✓ Constitution gates passed (6/6) pre-research
✓ Research completed (research.md)
✓ Design completed (5 artifacts)
✓ Constitution gates passed (6/6) post-design
✓ Task approach described
→ Next: /tasks
```

**Artifacts**: `plan.md` + `research.md` + `data-model.md` + `contracts/` + `quickstart.md` + updated `CLAUDE.md`

---

### 2. Gate Failure (Pre-Research)

```
✗ Constitution gate failed before research
  Violation: Creating wrapper abstraction (Principle VI)

ERROR: Cannot proceed to Phase 0
  Recommendation: Simplify approach to pass gate
  OR: Document in Complexity Tracking table

Action: Revise plan OR justify exception
```

**Resolution**:
- **Option A**: Revise technical approach, re-run `/plan`
- **Option B**: Add justification to Complexity Tracking table:

```markdown
## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Repository pattern abstraction | Need to swap PostgreSQL → DynamoDB later | Direct SQLAlchemy insufficient for multi-backend |
```

---

### 3. Gate Failure (Post-Design)

```
Constitution Check (Pre-Research): PASS
[Phase 0 completes]
[Phase 1 completes]

Constitution Check (Post-Design): FAIL
✗ Simplicity Gate: 4 projects detected (max 3 allowed)

ERROR: Design introduced new violation
  Before Phase 1: 3 projects
  After Phase 1: 4 projects (chat-admin added)

Action: Refactor Phase 1 design OR document in Complexity Tracking
```

**Resolution**:
- Merge `chat-admin` into main `chat` project
- Re-run Phase 1 design generation
- Re-validate constitution gates
- Continue to Phase 2

---

### 4. Clarification Warning (Non-Blocking)

```
⚠ CLARIFICATION WARNING:
  Spec missing "## Clarifications" section
  Ambiguous requirements detected:
    - FR-001: "fast delivery" (no latency SLA)
    - FR-006: "scalable" (no scale target)

  Recommendation: Run /clarify first
  Continue anyway? (y/n)

User: y

⚠ Proceeding without clarification (increased rework risk)
[Continues with planning...]
```

**Impact**: Higher risk of mid-implementation rework when ambiguities surface.

---

### 5. Missing Prerequisites

```
ERROR: Missing prerequisite file

  Expected: specs/001-feature/spec.md
  Not found: Specification does not exist

Action: Run /specify first to create feature specification
```

**Resolution**:
```
/specify "feature description"
[Then retry /plan]
```

---

## Follow-Up Actions

After `/plan` completes successfully:

### Immediate Next Step
```
/tasks
```
Generate actionable task breakdown from design artifacts.

### Optional Validation (Recommended)
```
/analyze
```
Run consistency checks before proceeding to `/tasks`. Catches:
- Missing test coverage for requirements
- Inconsistent terminology across artifacts
- Constitution alignment issues

### Review Artifacts
```
# Review generated design
cat specs/001-feature/plan.md
cat specs/001-feature/research.md
cat specs/001-feature/data-model.md
cat specs/001-feature/contracts/*.yaml
cat specs/001-feature/quickstart.md
```

---

## Best Practices

### 1. Provide Tech Context as Argument

**Good**:
```
/plan "Python 3.11, FastAPI, PostgreSQL 15, Redis 7, 10k concurrent users, <100ms p95 latency"
```

**Why**: Helps research phase focus on relevant technologies, generates more specific decisions.

**Avoid**:
```
/plan
```
Claude will ask clarifying questions, adding back-and-forth overhead.

---

### 2. Run /clarify Before /plan

**Workflow**:
```
/specify → /clarify → /plan
```

**Why**: Clarifications answered upfront reduce rework when technical decisions depend on requirements details.

**Example Issue Avoided**:
```
# Without /clarify:
Research phase: "Should we use WebSocket or polling?"
Claude guesses: "WebSocket (assuming real-time requirement)"
User later: "Actually, 5-second delay is fine (polling sufficient)"
Result: Wasted research time

# With /clarify:
/clarify asks: "What's the acceptable message delay?"
User answers: "5 seconds"
Research phase: "Use polling (simpler for 5s requirement)"
Result: Correct decision upfront
```

---

### 3. Let Constitutional Gates Catch Violations Early

**Why**: Fixing violations in planning phase is **10x cheaper** than in implementation.

**Cost Comparison**:
```
Planning Phase:
- Violation detected: 5 minutes
- Fix: Revise plan.md (10 minutes)
- Total: 15 minutes

Implementation Phase:
- Violation detected: After 3 hours of coding
- Fix: Refactor code + tests + update plan (2 hours)
- Total: 5 hours (20x more expensive)
```

**Strategy**: Don't bypass gates. If gate fails, either:
- Simplify design to pass gate
- Document compelling justification in Complexity Tracking

---

### 4. Review Complexity Tracking Table

If gates fail and you document exceptions:

```markdown
## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 4th project (violates Simplicity) | Admin UI requires separate deployment | Combining with main app couples release cycles |
```

**Review Checklist**:
- [ ] Is simpler alternative **genuinely** insufficient?
- [ ] Is violation **temporary** (tech debt to resolve)?
- [ ] Have you consulted team/stakeholders?
- [ ] Is trade-off **documented** for future maintainers?

---

### 5. Don't Skip Phase 0 Research

**Why Research Matters**:
- Documents **why** technologies chosen (not just **what**)
- Captures alternatives considered and rejected
- Provides future maintainers with decision context
- Prevents "why did we use X?" questions months later

**Bad Practice**:
```
/plan "Use FastAPI because it's fast"
[Skip research, jump to design]
```

**Good Practice**:
```
/plan "Python 3.11, async/await required, 1000 req/s target"
[Research phase compares: FastAPI vs Flask vs Starlette]
[Documents: FastAPI chosen for native async + OpenAPI support]
```

---

## Complexity Tracking Table Format

When constitutional gates fail and you need to document exceptions:

```markdown
## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [Principle violated] | [Business justification] | [Proof simpler approach insufficient] |
```

**Example Entries**:

```markdown
| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Repository pattern (violates Anti-Abstraction) | Must support PostgreSQL + DynamoDB backends | Direct SQLAlchemy insufficient for multi-backend |
| 4th project (violates Simplicity) | Admin UI requires separate deployment schedule | Combining with main app couples release cycles |
| Skip contract tests (violates Test-First) | External API has no contract definition | Cannot write contract test for undefined external API |
```

**Important**: Each entry must have **specific, measurable justification**. Avoid vague reasons like "better architecture" or "more flexible."

---

## Constitutional Gates Reference

### 6 Gates Evaluated (Twice)

1. **Library-First Gate** (Principle I)
   - Feature starts as standalone library?
   - Clear library boundaries defined?

2. **CLI Interface Gate** (Principle II)
   - Text input/output protocol specified?
   - JSON format support planned?

3. **Test-First Gate** (Principle III - NON-NEGOTIABLE)
   - Contract tests written before implementation?
   - Tests validated and approved?

4. **Integration Testing Gate** (Principle IV)
   - Real databases in tests (no mocks)?
   - End-to-end scenarios defined?

5. **Simplicity Gate** (Principle V)
   - Maximum 3 projects respected?
   - No unnecessary abstractions?

6. **Anti-Abstraction Gate** (Principle VI)
   - Using framework directly?
   - No wrapper classes planned?

**Evaluation Points**:
- **Pre-Research**: Before Phase 0 begins (blocks research if failed)
- **Post-Design**: After Phase 1 completes (catches new violations from detailed design)

---

## Artifacts Generated (6 Total)

| File | Purpose | Size | Content |
|------|---------|------|---------|
| `plan.md` | Implementation strategy | 200-400 lines | Phases 0-2, constitution check, progress tracking |
| `research.md` | Technology decisions | 100-200 lines | 3-5 decisions with rationale + alternatives |
| `data-model.md` | Entity definitions | 50-150 lines | Entities, fields, relationships, indexes |
| `contracts/*.yaml` | API specifications | 100-300 lines | REST endpoints, WebSocket events, GraphQL schemas |
| `quickstart.md` | Integration scenarios | 50-100 lines | 5-8 test scenarios with step-by-step flows |
| `CLAUDE.md` | Updated project context | Incremental | Tech stack added to autogenerated section |

**Total Output**: ~500-1150 lines of design documentation

---

## Common Issues

### Issue: "Spec Missing Clarifications Section"

**Symptom**:
```
⚠ Clarification check failed
  Spec.md missing "## Clarifications" section
  Recommendation: Run /clarify first
```

**Resolution**:
```
# Option 1: Run /clarify
/clarify
[Answer 3-5 questions]
/plan "tech stack"

# Option 2: Proceed anyway (not recommended)
User: "proceed without clarification"
Claude: [Continues with warning]
```

---

### Issue: Gate Failure Due to Ambiguous Requirements

**Symptom**:
```
✗ Simplicity Gate: Cannot determine project count
  Spec says "scalable architecture" but unclear if multi-project needed
```

**Resolution**: Run `/clarify` to resolve ambiguity, then re-run `/plan`.

---

### Issue: CLAUDE.md Update Fails

**Symptom**:
```
ERROR: update-agent-context.sh failed
  Could not write to CLAUDE.md
```

**Resolution**:
```bash
# Check file permissions
chmod 644 .claude/CLAUDE.md

# Verify script is executable
chmod +x .specify/scripts/bash/update-agent-context.sh

# Re-run plan
/plan "tech stack"
```

---

## References

### Related Commands
- [/specify](06-specify-command.md) - Create feature specification (prerequisite)
- [/clarify](08-clarify-command.md) - Resolve ambiguities before planning (recommended)
- [/tasks](09-tasks-command.md) - Generate task breakdown (next step)
- [/analyze](10-analyze-command.md) - Validate consistency (optional)

### Related Concepts
- [Constitution](../kb/08-constitution.md) - Six principles enforced by gates
- [Templates](../kb/06-templates.md) - Plan template structure
- [Workflows](../kb/10-workflows.md) - End-to-end planning examples
- [Architecture](../kb/03-architecture.md) - Layer 2 template execution

### Implementation Details
- Template: `.specify/templates/plan-template.md`
- Script: `.specify/scripts/bash/setup-plan.sh`
- Command: `.claude/commands/plan.md`

---

**Navigation**: [← /clarify Command](08-clarify-command.md) | [/tasks Command →](09-tasks-command.md)
