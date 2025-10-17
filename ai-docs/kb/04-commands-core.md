# Commands: Core Workflow

**Purpose**: Detailed reference for the 5 core commands that form the main SDD workflow
**Target Audience**: Developers using spec-kit for feature development
**Related Files**:

- [Commands: Clarify](05-commands-clarify.md) - Enhancement commands
- [Architecture](03-architecture.md) - How commands integrate with layers
- [Templates](06-templates.md) - Template mechanics used by commands
- [Workflows](10-workflows.md) - End-to-end command usage
  **Keywords**: /constitution, /specify, /plan, /tasks, /implement, workflow commands

---

## Overview

Spec-kit provides 5 **required** commands that form a complete SDD (Specification-Driven Development) workflow. Each command operates at a distinct phase, with strict separation of concerns to prevent premature decisions and maintain referential transparency.

```
Required Sequence:
/constitution → /specify → /plan → /tasks → /implement

Enhancement Points:
/constitution → [/clarify-constitution] → /specify → [/clarify] → /plan → /tasks → [/analyze] → /implement
```

**Phase Separation Enforcement**:

- `/specify` creates `spec.md` with **NO technical decisions**
- `/plan` adds `plan.md`, `data-model.md`, `contracts/` with **NO task breakdown**
- `/tasks` creates `tasks.md` **without executing implementation**
- `/implement` executes tasks **following TDD order**

Breaking this separation collapses the model. Each phase builds on the previous but remains **referentially transparent**—same inputs produce same outputs.

---

## 1. `/constitution` - Project Governance Setup

### Purpose

Create or update the project constitution from interactive or provided principle inputs.

### When to Use

- **Once per project** at the start
- When project principles change (version bump triggers template sync)

### Inputs

- User-provided principles (via `$ARGUMENTS` or conversation)
- Existing `.specify/memory/constitution.md` template
- Repository context (README, docs)

### Execution Process

```
1. Load constitution template with [PLACEHOLDER] tokens
2. Collect/derive values from user input or repo context
3. Mark ambiguous sections with [NEEDS CLARIFICATION]
4. Track version changes (MAJOR/MINOR/PATCH semantic versioning)
5. Update dependent templates (plan-template.md, spec-template.md, etc.)
6. Generate Sync Impact Report
```

### Outputs

- `.specify/memory/constitution.md` with filled placeholders
- Session metadata: `<!-- Clarification Sessions: 0 -->` if markers exist
- Sync Impact Report (as HTML comment)
- Suggested next command: `/clarify-constitution` or `/specify`

### Key Features

#### Semantic Versioning for Constitution

Treat principles as code with MAJOR/MINOR/PATCH rules:

- **MAJOR**: New non-negotiable principle (e.g., adding mandatory security review)
- **MINOR**: New SHOULD principle (e.g., adding recommended linting)
- **PATCH**: Clarification/wording improvement

#### Consistency Propagation

Automatically updates dependent templates when constitution changes:

- `plan-template.md`: Constitution Check gates updated to match principles
- `spec-template.md`: Constraints section updated
- `tasks-template.md`: Task ordering rules updated

#### Explicit Uncertainty

Never guesses—always marks `[NEEDS CLARIFICATION]` for:

- Ambiguous technology constraints
- Unclear quality gates
- Undefined team workflows

### Claude Code Integration Pattern

```
User: /constitution "Library-first architecture; CLI interfaces; TDD mandatory"
  ↓
Claude:
  1. Parses user input for principles
  2. Fills constitution template
  3. Validates no guessing occurred
  4. Updates plan-template.md gates to match principles
  5. Writes constitution file
  6. Reports: "Constitution v1.0.0 created, ready for /specify"
```

### Example Output Structure

```markdown
# Project Constitution

## Principle I: Library-First Architecture

**Mandate**: Every feature MUST begin as a standalone library
**Rationale**: Enables reusability, testing isolation, clear boundaries
**Enforcement**: Constitution Check gate in /plan verifies library boundaries

## Principle II: CLI Interfaces

**Mandate**: All libraries MUST expose CLI interfaces for automation
**Rationale**: Scriptability, CI/CD integration, headless workflows
**Enforcement**: plan.md validates text input/output protocol

## Principle III: Test-Driven Development (NON-NEGOTIABLE)

**Mandate**: Contract tests MUST be written and approved before implementation
**Rationale**: Prevents rework, ensures testability, validates design
**Enforcement**: /tasks generates test tasks before implementation tasks

---

<!-- Constitution Version: 1.0.0 -->
<!-- Clarification Sessions: 0 -->
```

### Cross-References

- [Templates](06-templates.md) - Constitution template structure
- [Workflows](10-workflows.md) - Multi-feature constitution reuse
- [Commands: Clarify](05-commands-clarify.md) - `/clarify-constitution` command

---

## 2. `/specify` - Feature Specification Generation

### Purpose

Create structured feature specification from natural language description.

### When to Use

- **Once per feature** to define requirements
- Before any technical planning or design

### Inputs

- User's feature description (via `$ARGUMENTS`)
- `.specify/templates/spec-template.md`
- Current feature numbering state

### Execution Process

```
1. Run `create-new-feature.sh --json "$ARGUMENTS"` **once**
2. Parse JSON for FEATURE_ID, SPEC_FILE, FEATURE_NUM
3. Load spec template
4. Extract key concepts from description (actors, actions, data, constraints)
5. Mark unclear aspects with [NEEDS CLARIFICATION]
6. Fill sections: User Scenarios, Functional Requirements, Key Entities
7. Run Review Checklist (no implementation details, testable requirements)
8. Write specification to SPEC_FILE
```

### Outputs

- `specs/###-feature-name/spec.md` with structured specification
- Feature directory created (no git branch in solo dev workflow)
- `SPECIFY_FEATURE` environment variable set for subsequent commands

### Key Features

#### Sequential Feature Numbering

Automatic numbering (001, 002, 003...) prevents conflicts:

- Tracked in `.specify/memory/next-feature.txt`
- Incremented atomically by `create-new-feature.sh`
- No manual intervention required

#### No Branch Creation

Solo developer workflow:

- Single main branch
- Feature directories organize work
- Git commits mark feature completion

#### Ambiguity Markers

Forces explicit uncertainty:

- `[NEEDS CLARIFICATION: latency target?]` for missing metrics
- `[NEEDS CLARIFICATION: authentication method?]` for unclear security
- Prevents false assumptions

#### Template-Driven Structure

Ensures completeness:

- User Scenarios (who, what, why)
- Functional Requirements (MUST/SHOULD statements)
- Non-Functional Requirements (performance, security, scalability)
- Key Entities (domain model concepts)
- Edge Cases & Error Scenarios

### Example Flow

```bash
User: /specify "Real-time chat system with message history"

Claude executes:
  1. Runs: create-new-feature.sh --json "Real-time chat system with message history"
  2. Receives: {"FEATURE_ID":"003-real-time-chat","SPEC_FILE":"...","FEATURE_NUM":"003"}
  3. Creates specs/003-real-time-chat/spec.md with:
     - User Stories: "Users can send messages in real-time"
     - FR-001: System MUST deliver messages within [NEEDS CLARIFICATION: latency target?]
     - FR-002: System MUST persist message history
     - FR-003: System MUST support [NEEDS CLARIFICATION: how many concurrent users?]
     - Key Entities: Message (text, timestamp, sender), Room (participants)
  4. Reports: "Feature 003-real-time-chat created, 2 clarifications needed"
```

### Specification Structure

```markdown
# Feature Specification: Real-Time Chat

## User Scenarios

**Primary Actor**: Chat User
**Goal**: Send and receive messages in real-time

**Scenario 1: Send Message**

- User joins a chat room
- User types a message
- User sends the message
- Message appears instantly for all room participants

**Scenario 2: View History**

- User opens a chat room
- System displays recent message history
- User can scroll to load older messages

## Functional Requirements

### Core Features

- **FR-001**: System MUST deliver messages to all room participants within [NEEDS CLARIFICATION: latency target?]
- **FR-002**: System MUST persist message history for [NEEDS CLARIFICATION: retention period?]
- **FR-003**: System MUST support [NEEDS CLARIFICATION: concurrent user count?]
- **FR-004**: Users MUST be able to join/leave rooms dynamically

### Data Management

- **FR-005**: Each message MUST include text, timestamp, sender ID
- **FR-006**: System MUST prevent message loss during network interruptions

## Non-Functional Requirements

- **NFR-001**: Message delivery latency [NEEDS CLARIFICATION: target?]
- **NFR-002**: System availability [NEEDS CLARIFICATION: uptime requirement?]

## Key Entities

- **Message**: text (string), timestamp (datetime), sender_id (UUID), room_id (UUID)
- **Room**: room_id (UUID), participants (User[]), created_at (datetime)
- **User**: user_id (UUID), username (string)

## Edge Cases

- Network interruption during message send
- User leaves room while message in transit
- Message history exceeds [NEEDS CLARIFICATION: pagination limit?]
```

### Cross-References

- [Templates](06-templates.md) - Spec template structure
- [Commands: Clarify](05-commands-clarify.md) - `/clarify` for ambiguity resolution
- [Workflows](10-workflows.md) - Specify-clarify-plan cycle

---

## 3. `/plan` - Implementation Planning with Constitution Gates

### Purpose

Execute implementation planning workflow to generate design artifacts.

### When to Use

- After `/specify` (optionally after `/clarify`)
- Before task breakdown
- When specification is sufficiently clear

### Inputs

- Feature specification from `specs/###-feature-name/spec.md`
- Constitution at `.specify/memory/constitution.md`
- Technical context from `$ARGUMENTS` (language, dependencies, platform)

### Execution Process

```
Execution Flow:
1. Run setup-plan.sh --json → Parse FEATURE_SPEC, IMPL_PLAN, FEATURE_DIR
2. Check for Clarifications section in spec
   → If missing with ambiguities: PAUSE, recommend /clarify
3. Read and analyze feature specification
4. Read constitution for requirements
5. Fill Technical Context from arguments
6. Evaluate Constitution Check gates
   → If violations: Document in Complexity Tracking OR ERROR
7. Execute Phase 0: Research
   → Generate research.md with tech stack decisions
8. Execute Phase 1: Design & Contracts
   → Generate data-model.md, contracts/, quickstart.md
   → Run update-agent-context.sh to update CLAUDE.md
9. Re-evaluate Constitution Check (post-design validation)
   → If new violations: Refactor design, return to Phase 1
10. Describe Phase 2 task generation approach (DO NOT create tasks.md)
11. STOP - Ready for /tasks command
```

### Outputs

- `plan.md` with implementation strategy
- `research.md` with technology decisions and rationale
- `data-model.md` with entities, fields, relationships
- `contracts/` directory with API specifications (OpenAPI/GraphQL)
- `quickstart.md` with integration test scenarios
- Updated `.claude/CLAUDE.md` with project context

### Key Features

#### Constitutional Gates Enforced Twice

**Pre-Research Gate**: Before Phase 0

- Validates specification against constitution
- Blocks if MUST principles violated
- Documents acceptable violations in Complexity Tracking

**Post-Design Gate**: After Phase 1

- Validates design against constitution
- Catches new violations introduced during design
- Forces refactoring if needed

#### Complexity Tracking Table

Forces justification for violations:

```markdown
## Complexity Tracking

| Principle Violation                     | Justification                             | Mitigation                        | Accepted?  |
| --------------------------------------- | ----------------------------------------- | --------------------------------- | ---------- |
| Skipping library boundary (Principle I) | WebSocket requires tight FastAPI coupling | Extract protocol layer in Phase 2 | ✓ Deferred |
```

#### Incremental CLAUDE.md Updates

Preserves manual additions between markers:

```markdown
<!-- BEGIN AUTOGENERATED CONTEXT -->

# Feature Context: Real-Time Chat

[Generated content]

<!-- END AUTOGENERATED CONTEXT -->

[User's manual additions preserved]
```

#### STOP Before Task Generation

Phase separation is strict:

- `/plan` describes task approach but does NOT create `tasks.md`
- `/tasks` command generates executable task list
- Prevents interleaving planning and execution

### Constitution Check Example

```markdown
## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Library-First Gate (Principle I)

- [ ] Feature begins as standalone library?
- [ ] Clear library boundaries defined?

### CLI Interface Gate (Principle II)

- [ ] Text input/output protocol specified?
- [ ] JSON format support planned?

### Test-First Gate (Principle III - NON-NEGOTIABLE)

- [ ] Contract tests written before implementation?
- [ ] Tests validated and approved?

**Result**: PASS - Continue to Phase 0
[If FAIL with violations: Document in Complexity Tracking or ERROR]
```

### Technical Context Filling

```markdown
## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, asyncio, websockets
**Storage**: PostgreSQL 15 with asyncpg
**Testing**: pytest, httpx, pytest-asyncio
**Target Platform**: Linux server (Docker)
**Performance Goals**: 1000 req/s sustained, <100ms message delivery
**Constraints**: <200ms p95 latency for HTTP endpoints
**Scale/Scope**: 10k concurrent WebSocket connections
```

### Phase 0: Research Example

`research.md`:

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

### Database Schema

**Decision**: PostgreSQL with JSONB for message metadata
**Rationale**:

- Strong consistency for user/room data
- JSONB allows flexible message attributes without schema changes
- Excellent async support via asyncpg
  **Alternatives Considered**:
- MongoDB: Less mature async drivers, eventual consistency risks
- DynamoDB: Lock-in, cost unpredictability
```

### Phase 1: Design Artifacts

`data-model.md`:

```markdown
# Data Model: Real-Time Chat

## Entities

### User

**Fields**:

- `user_id`: UUID (PK)
- `username`: VARCHAR(50) (UNIQUE, NOT NULL)
- `created_at`: TIMESTAMP (NOT NULL)

**Relationships**:

- One-to-Many with Message (sender)
- Many-to-Many with Room (participants)

### Room

**Fields**:

- `room_id`: UUID (PK)
- `name`: VARCHAR(100) (NOT NULL)
- `created_at`: TIMESTAMP (NOT NULL)

**Relationships**:

- Many-to-Many with User (participants)
- One-to-Many with Message

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
```

`contracts/messages.yaml`:

```yaml
openapi: 3.0.0
info:
  title: Messages API
  version: 1.0.0

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
                room_id:
                  type: string
                  format: uuid
                text:
                  type: string
                  maxLength: 5000
      responses:
        "201":
          description: Message created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Message"
        "400":
          description: Invalid request
```

### Cross-References

- [Templates](06-templates.md) - Plan template structure
- [Constitution](02-constitution.md) - Constitution gates
- [Workflows](10-workflows.md) - Plan-tasks-implement cycle

---

## 4. `/tasks` - Task Breakdown Generation

### Purpose

Generate actionable, dependency-ordered tasks from design artifacts.

### When to Use

- After `/plan` completes successfully
- Before `/implement` execution
- Optionally after `/analyze` for validation

### Inputs

- `plan.md` (required)
- `data-model.md` (if exists)
- `contracts/` (if exists)
- `research.md` (if exists)
- `quickstart.md` (if exists)

### Execution Process

```
1. Run `check-prerequisites.sh --json` for FEATURE_DIR and AVAILABLE_DOCS
2. Load all available design documents
3. Use `.specify/templates/tasks-template.md` as base
4. Generate tasks following rules:
   - Each contract file → contract test task marked [P] (parallel-safe)
   - Each entity in data-model → model creation task marked [P]
   - Each endpoint → implementation task (sequential if shared files)
   - Each user story → integration test marked [P]
   - Different files = can be parallel [P]
   - Same file = sequential (no [P])

5. Order tasks by dependencies:
   - Setup before everything
   - Tests before implementation (TDD)
   - Models before services
   - Services before endpoints
   - Core before integration
   - Everything before polish

6. Include parallel execution examples with Task agent commands
```

### Outputs

- `tasks.md` with numbered tasks (T001, T002, ...)
- Clear file paths for each task
- Dependency notes
- Parallel execution guidance

### Task Generation Rules

| Input                           | Generated Task                                    | Parallel?  | Ordering               |
| ------------------------------- | ------------------------------------------------- | ---------- | ---------------------- |
| `contracts/messages.yaml`       | `T001: Write contract test for messages endpoint` | `[P]`      | Setup phase            |
| `data-model.md: Message entity` | `T002: Create Message model`                      | `[P]`      | Core phase             |
| `contracts/rooms.yaml`          | `T003: Write contract test for rooms endpoint`    | `[P]`      | Setup phase            |
| User story: "Send message"      | `T010: Integration test for message sending`      | `[P]`      | Integration            |
| Endpoint: POST /messages        | `T015: Implement POST /messages`                  | (no `[P]`) | Core (depends on T002) |

### Example tasks.md Structure

````markdown
# Tasks: Real-Time Chat

## Setup Phase (T001-T005)

- [ ] T001: Initialize FastAPI project structure
  - Files: `pyproject.toml`, `src/main.py`, `tests/`
- [ ] T002: Configure PostgreSQL connection
  - Files: `src/db.py`
- [ ] T003: Set up pytest with async support
  - Files: `pyproject.toml`, `tests/conftest.py`
- [ ] T004: Configure linting (ruff, mypy)
  - Files: `pyproject.toml`, `.ruff.toml`
- [ ] T005: Write contract test for messages endpoint [P]
  - Files: `tests/contract/test_messages.py`
  - Contract: `contracts/messages.yaml`

## Core Phase (T006-T015)

- [ ] T006: Create Message model [P]
  - Files: `src/models/message.py`
  - Schema: `data-model.md: Message entity`
- [ ] T007: Create Room model [P]
  - Files: `src/models/room.py`
  - Schema: `data-model.md: Room entity`
- [ ] T008: Implement MessageService
  - Files: `src/services/message_service.py`
  - Depends on: T006
- [ ] T009: Implement RoomService
  - Files: `src/services/room_service.py`
  - Depends on: T007
- [ ] T010: Implement POST /messages endpoint
  - Files: `src/api/messages.py`
  - Depends on: T008, T005 (test exists)
- [ ] T011: Implement GET /messages endpoint
  - Files: `src/api/messages.py`
  - Depends on: T008
- [ ] T012: Implement WebSocket connection handler
  - Files: `src/websocket/connection.py`
  - Depends on: T009
- [ ] T013: Integration test for message sending [P]
  - Files: `tests/integration/test_message_sending.py`
  - Scenario: `quickstart.md: Send Message`
- [ ] T014: Integration test for real-time delivery [P]
  - Files: `tests/integration/test_real_time.py`
  - Scenario: `quickstart.md: Real-time Delivery`
- [ ] T015: Integration test for history retrieval [P]
  - Files: `tests/integration/test_history.py`
  - Scenario: `quickstart.md: View History`

## Polish Phase (T016-T020)

- [ ] T016: Unit tests for MessageService [P]
  - Files: `tests/unit/test_message_service.py`
- [ ] T017: Unit tests for RoomService [P]
  - Files: `tests/unit/test_room_service.py`
- [ ] T018: Performance test for 1000 req/s target
  - Files: `tests/performance/test_load.py`
- [ ] T019: Add API documentation
  - Files: `docs/api.md`
- [ ] T020: Write deployment guide
  - Files: `docs/deployment.md`

## Parallel Execution Examples

```bash
# Run all contract tests in parallel
Task T005 & Task T013 & Task T014 & Task T015

# Run all model creation in parallel
Task T006 & Task T007

# Run all unit tests in parallel
Task T016 & Task T017
```
````

```

### Key Features

#### TDD Ordering Enforced
Tests always before implementation:
- Contract tests (T005) before endpoint implementation (T010)
- Integration tests (T013-T015) created in Core phase
- Unit tests (T016-T017) in Polish phase

#### Explicit Parallelization
`[P]` marks independent tasks:
- Different files → can run in parallel
- Same file → must be sequential
- Different test files → always parallel

#### Specific File Paths
Each task knows exactly what files to create/modify:
- `src/models/message.py` not just "create model"
- `tests/contract/test_messages.py` not just "write test"

#### Immediately Executable
LLM can complete tasks without additional context:
- Contract reference: `contracts/messages.yaml`
- Schema reference: `data-model.md: Message entity`
- Scenario reference: `quickstart.md: Send Message`

### Cross-References
- [Templates](06-templates.md) - Tasks template structure
- [Workflows](10-workflows.md) - Task execution patterns
- [Commands: Analyze](05-commands-clarify.md) - `/analyze` for validation

---

## 5. `/implement` - Task Execution

### Purpose
Execute implementation plan by processing all tasks in `tasks.md`.

### When to Use
- After `/tasks` completes successfully
- Optionally after `/analyze` validates consistency
- When ready to write code

### Inputs
- `tasks.md` (required)
- `plan.md` (required)
- `data-model.md`, `contracts/`, `research.md`, `quickstart.md` (if exist)

### Execution Process

```

1. Run `check-prerequisites.sh --json --require-tasks --include-tasks`
2. Load implementation context from all available docs
3. Parse `tasks.md` structure:
   - Extract task phases (Setup, Tests, Core, Integration, Polish)
   - Identify dependencies (sequential vs parallel)
   - Extract task details (ID, description, file paths, [P] markers)

4. Execute phase-by-phase:
   - Setup first: Initialize project, dependencies, configuration
   - Tests before code: Execute test tasks before implementation tasks (TDD)
   - Respect dependencies: Sequential tasks in order, parallel tasks [P] can run together
   - File-based coordination: Tasks affecting same files run sequentially

5. Progress tracking:
   - Report progress after each completed task
   - Halt if non-parallel task fails
   - For parallel tasks, continue with successful, report failures
   - Mark completed tasks with [X] in tasks.md

6. Completion validation:
   - Verify all tasks completed
   - Check implementation matches specification
   - Validate tests pass
   - Confirm technical plan followed

```

### Outputs
- Implemented code matching specifications
- Updated `tasks.md` with `[X]` for completed tasks
- Test execution results
- Final status summary

### Key Features

#### TDD Enforcement
Test tasks execute before implementation tasks:
- T005 (contract test) completes before T010 (endpoint)
- Tests fail initially (no implementation)
- Implementation makes tests pass

#### Atomic Task Updates
Marks `[X]` after each task completion:
- Prevents context loss on interruption
- Shows exact progress state
- Enables resumption from last completed task

#### Halt on Failure
Non-parallel task failures stop execution for diagnosis:
- Setup failure → stop immediately (nothing will work)
- Core task failure → stop, fix, resume
- Prevents cascading errors

#### Parallel Task Resilience
Continue with successful parallel tasks:
- T006 and T007 run together (different files)
- If T006 fails, T007 completes
- Report failure, continue with dependent tasks that don't need T006

### Example Execution

```

User: /implement

Claude:
Loading context...
✓ Loaded plan.md
✓ Loaded tasks.md (20 tasks)
✓ Loaded data-model.md
✓ Loaded contracts/ (2 files)

Starting Setup Phase (T001-T005)...

[T001] Initialize FastAPI project structure
✓ Created pyproject.toml
✓ Created src/main.py
✓ Created tests/
→ Marked [X] in tasks.md

[T002] Configure PostgreSQL connection
✓ Created src/db.py with async connection pool
✓ Added environment variable handling
→ Marked [X] in tasks.md

[T003] Set up pytest with async support
✓ Added pytest-asyncio to pyproject.toml
✓ Created tests/conftest.py with async fixtures
→ Marked [X] in tasks.md

[T004] Configure linting (ruff, mypy)
✓ Added ruff and mypy to dev dependencies
✓ Created .ruff.toml with settings
→ Marked [X] in tasks.md

[Running T005 in parallel - contract test]
[T005] Write contract test for messages endpoint
✓ Created tests/contract/test_messages.py
✓ Test fails as expected (no implementation yet)
→ Marked [X] in tasks.md

Setup Phase Complete (5/5 tasks)

Starting Core Phase (T006-T015)...

[Running T006, T007 in parallel - models]
[T006] Create Message model
✓ Created src/models/message.py with SQLAlchemy model
✓ Added fields: message_id, room_id, sender_id, text, metadata, created_at
✓ Contract tests now discover Message model
→ Marked [X] in tasks.md

[T007] Create Room model
✓ Created src/models/room.py with SQLAlchemy model
✓ Added fields: room_id, name, created_at
✓ Added relationship to User (participants)
→ Marked [X] in tasks.md

[T008] Implement MessageService
✓ Created src/services/message_service.py
✓ Methods: create_message, get_messages, get_room_history
✓ Integration with Message model
→ Marked [X] in tasks.md

[T009] Implement RoomService
✓ Created src/services/room_service.py
✓ Methods: create_room, get_room, add_participant
✓ Integration with Room model
→ Marked [X] in tasks.md

[T010] Implement POST /messages endpoint
✓ Created src/api/messages.py
✓ POST /messages endpoint implementation
✓ Contract test T005 now passes!
→ Marked [X] in tasks.md

[T011] Implement GET /messages endpoint
✓ Added GET /messages to src/api/messages.py
✓ Returns room history with pagination
→ Marked [X] in tasks.md

[T012] Implement WebSocket connection handler
✓ Created src/websocket/connection.py
✓ WebSocket connection management
✓ Redis pub/sub integration for message routing
→ Marked [X] in tasks.md

[Running T013, T014, T015 in parallel - integration tests]
[T013] Integration test for message sending
[T014] Integration test for real-time delivery
[T015] Integration test for history retrieval
✓ All integration tests created and passing
→ Marked [X] for T013, T014, T015 in tasks.md

Core Phase Complete (10/10 tasks)

Starting Polish Phase (T016-T020)...

[Running T016, T017 in parallel - unit tests]
[T016] Unit tests for MessageService
[T017] Unit tests for RoomService
✓ All unit tests created and passing
→ Marked [X] for T016, T017 in tasks.md

[T018] Performance test for 1000 req/s target
✓ Created tests/performance/test_load.py
✓ Performance test passes: 1200 req/s achieved
→ Marked [X] in tasks.md

[T019] Add API documentation
✓ Created docs/api.md with endpoint reference
→ Marked [X] in tasks.md

[T020] Write deployment guide
✓ Created docs/deployment.md with Docker setup
→ Marked [X] in tasks.md

Polish Phase Complete (5/5 tasks)

Implementation Complete!
✓ 20/20 tasks completed
✓ All tests passing (contract, integration, unit, performance)
✓ Matches specification (specs/003-real-time-chat/spec.md)
✓ Follows technical plan (specs/003-real-time-chat/plan.md)

Summary:

- Setup: 5 tasks
- Core: 10 tasks
- Polish: 5 tasks
- Total execution time: ~15 minutes
- Test coverage: 95%
- Performance: 1200 req/s (target: 1000 req/s)

```

### Cross-References
- [Workflows](10-workflows.md) - Complete implement workflow
- [Templates](06-templates.md) - Task execution patterns
- [Testing](08-testing.md) - TDD practices

---

## Command Dependency Graph

```

/constitution [required, once per project]
│
├─> /clarify-constitution [optional, if markers exist]
│
↓
/specify [required, per feature]
│
├─> /clarify [optional but recommended]
│
↓
/plan [required, per feature]
↓
/tasks [required, per feature]
│
├─> /analyze [optional but recommended]
│
↓
/implement [required, per feature]

```

**Command Categories**:
- **Required Core**: `/constitution`, `/specify`, `/plan`, `/tasks`, `/implement`
- **Optional Enhancement**: `/clarify-constitution`, `/clarify`, `/analyze`

**Phase Boundaries**:
1. **Constitution → Specify**: Project governance established before features
2. **Specify → Plan**: Requirements clear before technical decisions
3. **Plan → Tasks**: Design complete before task breakdown
4. **Tasks → Implement**: Plan validated before execution

**Enhancement Insertion Points**:
- After `/constitution`: Use `/clarify-constitution` to resolve principle ambiguities
- After `/specify`: Use `/clarify` to resolve requirement ambiguities
- After `/tasks`: Use `/analyze` to validate artifact consistency

---

## Cross-References

### Related Command Concepts
- **Sequential execution**: Each command builds on previous outputs
- **Referential transparency**: Same inputs produce same outputs
- **Phase separation**: No premature decisions (spec → plan → tasks → implement)
- **Constitutional authority**: Constitution gates enforce principles

### Template Integration
- [Templates](06-templates.md) - How templates constrain command outputs
- Constitution template drives `/constitution` structure
- Spec template drives `/specify` structure
- Plan template drives `/plan` structure
- Tasks template drives `/tasks` structure

### Workflow Patterns
- [Workflows](10-workflows.md) - End-to-end usage examples
- Single-feature workflow: constitution → specify → clarify → plan → tasks → analyze → implement
- Multi-feature workflow: Reuse constitution across features
- Iterative refinement: Use clarify commands to improve quality

**Navigation**: [← Architecture](03-architecture.md) | [Commands: Clarify →](05-commands-clarify.md)

---

## Keywords
constitution, governance, principles, feature specification, requirements, functional requirements, user stories, implementation planning, technical design, data model, API contracts, task breakdown, TDD, test-driven development, task execution, dependency ordering, parallel execution, constitutional gates, phase separation, referential transparency
```
