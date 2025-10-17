# Page 08: /tasks - Task Breakdown

**Purpose**: Comprehensive guide to the `/tasks` command from the user's functional perspective

**Related Pages**:
- [Page 06: /plan Command](06-plan-command.md) - Prerequisites for task generation
- [Page 09: /analyze Command](09-analyze-command.md) - Optional validation before implementation
- [Page 10: /implement Command](10-implement-command.md) - Task execution
- [Page 04: Feature Workflow](04-feature-workflow.md) - Complete workflow context

---

## Overview

The `/tasks` command transforms your implementation plan into an actionable, dependency-ordered task list. It reads all design artifacts (plan.md, data-model.md, contracts/, research.md, quickstart.md) and generates a comprehensive tasks.md file with numbered tasks organized into five phases.

**Position in Workflow**: Required after `/plan`, before `/implement`

```
/constitution → /specify → /clarify → /plan → /tasks → /analyze → /implement
                                              ↑ You are here
```

---

## User Action

Running the command requires **no arguments**:

```
/tasks
```

The command automatically:
- Reads from all available design documents
- Applies task generation rules
- Creates tasks.md in your feature directory

---

## Input Required

**None** - The command reads from:

| Artifact | Required? | Purpose |
|----------|-----------|---------|
| `plan.md` | ✓ Yes | Tech stack, libraries, architecture |
| `data-model.md` | If exists | Entities generate model creation tasks |
| `contracts/` | If exists | Each file generates contract test task |
| `research.md` | If exists | Technical decisions inform setup tasks |
| `quickstart.md` | If exists | User stories generate integration tests |

**Note**: Not all projects have all documents. For example:
- CLI tools might not have contracts/
- Simple libraries might not need data-model.md
- Tasks are generated based on what's available

---

## What You'll See

### 1. Script Execution

```
Running script: check-prerequisites.sh --json
✓ Available docs: spec.md, plan.md, data-model.md, contracts/, quickstart.md
```

Claude validates that the required artifacts exist before proceeding.

### 2. Loading Design Documents

```
Loading design documents...
✓ Loaded plan.md (tech stack: Python 3.11, FastAPI, PostgreSQL, Redis)
✓ Loaded data-model.md (3 entities)
✓ Loaded contracts/ (2 files, 10 endpoints/events)
✓ Loaded quickstart.md (5 scenarios)
```

### 3. Task Generation Rules Applied

The command follows systematic rules to generate tasks:

| Input | Generated Task | Parallel? | Phase |
|-------|----------------|-----------|-------|
| `contracts/messages.yaml` | Contract test for messages endpoint | [P] | Test |
| `data-model.md: Message entity` | Create Message model | [P] | Core |
| `contracts/rooms.yaml` | Contract test for rooms endpoint | [P] | Test |
| User story: "Send message" | Integration test for message sending | [P] | Core |
| Endpoint: POST /messages | Implement POST /messages | No [P] | Core |

**Parallelization Rules**:
- **Different files** = Can be parallel [P]
- **Same file** = Sequential (no [P])
- **Different test files** = Always parallel

### 4. Task Ordering by Dependencies

```
Generating tasks...

Setup Phase: 5 tasks
- Project structure, dependencies, configuration

Test Phase: 10 tasks (8 marked [P])
- Contract tests for all endpoints/events
- Integration tests for user scenarios

Core Phase: 12 tasks
- Models for 3 entities [P]
- Services for business logic
- WebSocket handlers
- REST endpoints

Integration Phase: 5 tasks
- Database migrations
- Redis Pub/Sub setup
- Authentication middleware

Polish Phase: 5 tasks (4 marked [P])
- Unit tests
- Performance testing
- Documentation
```

### 5. Tasks.md Generated

```
Tasks complete at specs/001-real-time-chat/tasks.md
Total: 37 tasks (18 marked parallel-safe)
Estimated execution time: 8-12 hours

Next command: /analyze (optional) or /implement
```

---

## The 5 Task Phases

### Phase 1: Setup (T001-T005)

**Purpose**: Initialize project structure and configuration

**Typical Tasks**:
- [ ] T001: Create project structure per implementation plan
  - Files: `pyproject.toml`, `src/`, `tests/`
- [ ] T002: Initialize [language] project with [framework] dependencies
  - Files: `requirements.txt` or `package.json`
- [ ] T003 [P]: Configure linting and formatting tools
  - Files: `.ruff.toml`, `.eslintrc.json`
- [ ] T004 [P]: Set up testing framework
  - Files: `pytest.ini`, `tests/conftest.py`
- [ ] T005: Create environment configuration
  - Files: `.env.example`, `config.py`

**Ordering Rule**: Setup before everything (project must exist)

### Phase 2: Tests First (T006-T015) - TDD Enforcement

**Purpose**: Write tests that fail before implementation

**CRITICAL**: These tests MUST be written and MUST FAIL before ANY implementation

**Typical Tasks**:
- [ ] T006 [P]: Contract test POST /api/users
  - Files: `tests/contract/test_users_post.py`
  - Contract: `contracts/users.yaml`
- [ ] T007 [P]: Contract test GET /api/users/{id}
  - Files: `tests/contract/test_users_get.py`
  - Contract: `contracts/users.yaml`
- [ ] T008 [P]: Integration test user registration
  - Files: `tests/integration/test_registration.py`
  - Scenario: `quickstart.md: User Registration`
- [ ] T009 [P]: Integration test auth flow
  - Files: `tests/integration/test_auth.py`
  - Scenario: `quickstart.md: Authentication`

**Task Generation Rules**:
1. **From Contracts**: Each contract file → contract test task [P]
2. **From User Stories**: Each story → integration test [P]
3. **All tests are parallel-safe**: Different test files can run concurrently

**Ordering Rule**: Tests before implementation (TDD)

### Phase 3: Core Implementation (T016-T030)

**Purpose**: Implement models, services, and endpoints

**Typical Tasks**:
- [ ] T016 [P]: User model
  - Files: `src/models/user.py`
  - Schema: `data-model.md: User entity`
- [ ] T017 [P]: Message model
  - Files: `src/models/message.py`
  - Schema: `data-model.md: Message entity`
- [ ] T018: UserService CRUD operations
  - Files: `src/services/user_service.py`
  - Depends on: T016
- [ ] T019: MessageService business logic
  - Files: `src/services/message_service.py`
  - Depends on: T017
- [ ] T020: POST /api/users endpoint
  - Files: `src/api/users.py`
  - Depends on: T018, T006 (test exists)
- [ ] T021: GET /api/users/{id} endpoint
  - Files: `src/api/users.py`
  - Depends on: T018, T007 (test exists)
- [ ] T022: Input validation middleware
  - Files: `src/middleware/validation.py`
- [ ] T023: Error handling and logging
  - Files: `src/middleware/error_handler.py`

**Task Generation Rules**:
1. **From Data Model**: Each entity → model creation task [P]
2. **From Contracts**: Each endpoint → implementation task (sequential if shared files)
3. **Dependencies**: Models before services, services before endpoints

**Ordering Rule**: Models → Services → Endpoints

### Phase 4: Integration (T031-T035)

**Purpose**: Connect core components to external systems

**Typical Tasks**:
- [ ] T031: Connect UserService to database
  - Files: `src/services/user_service.py` (update)
  - Depends on: T016, T018
- [ ] T032: Auth middleware
  - Files: `src/middleware/auth.py`
- [ ] T033: Request/response logging
  - Files: `src/middleware/logging.py`
- [ ] T034: CORS and security headers
  - Files: `src/middleware/security.py`
- [ ] T035: Database migrations
  - Files: `migrations/001_initial_schema.sql`

**Ordering Rule**: Core before integration (core features before connections)

### Phase 5: Polish (T036-T040)

**Purpose**: Final quality assurance and documentation

**Typical Tasks**:
- [ ] T036 [P]: Unit tests for validation
  - Files: `tests/unit/test_validation.py`
- [ ] T037 [P]: Unit tests for UserService
  - Files: `tests/unit/test_user_service.py`
- [ ] T038: Performance tests (<200ms p95 latency)
  - Files: `tests/performance/test_load.py`
- [ ] T039 [P]: Update API documentation
  - Files: `docs/api.md`
- [ ] T040: Remove code duplication
  - Files: Various (refactoring)

**Ordering Rule**: Everything before polish (polish assumes working code)

---

## Task Numbering and Structure

Each task follows this format:

```markdown
- [ ] T001: Task description with specific action
  - Files: `exact/path/to/file.py`
  - [Optional] Schema: `data-model.md: Entity name`
  - [Optional] Contract: `contracts/file.yaml`
  - [Optional] Scenario: `quickstart.md: Scenario name`
  - [Optional] Depends on: T005, T006
```

**Key Elements**:
- **Numbered**: T001, T002, T003... (sequential)
- **Actionable**: Specific enough for LLM to execute
- **File Paths**: Exact files to create/modify
- **References**: Links to design artifacts
- **Dependencies**: Explicit blocking relationships

---

## Parallel Execution Markers

### What is [P]?

The `[P]` marker indicates a task can run **concurrently** with other `[P]` tasks in the same phase.

**Rules for Parallel-Safe Tasks**:
1. Different files (no conflicts)
2. No shared state
3. No dependencies on each other
4. Common examples: contract tests, integration tests, model creation, unit tests

### Example Parallel Execution

```markdown
## Parallel Example

```bash
# Launch T006-T009 together (all are contract/integration tests):
Task: "Contract test POST /api/users in tests/contract/test_users_post.py"
Task: "Contract test GET /api/users/{id} in tests/contract/test_users_get.py"
Task: "Integration test registration in tests/integration/test_registration.py"
Task: "Integration test auth in tests/integration/test_auth.py"
```
```

**Benefits**:
- Faster execution (4 tests in parallel vs sequential)
- Better resource utilization
- Clear parallelization strategy for `/implement`

---

## Dependency Graph

Tasks are ordered by dependencies:

```
Setup Tasks (T001-T005)
    ↓
Test Tasks (T006-T015) [Many parallel]
    ↓
Model Tasks (T016-T017) [Parallel]
    ↓
Service Tasks (T018-T019) [Depends on models]
    ↓
Endpoint Tasks (T020-T023) [Depends on services and tests]
    ↓
Integration Tasks (T031-T035) [Depends on core]
    ↓
Polish Tasks (T036-T040) [Many parallel]
```

**Dependency Notes**:
- Tests (T006-T015) before implementation (T016-T030)
- T016 blocks T018 (UserService needs User model)
- T018 blocks T020 (POST /users needs UserService)
- T020 requires T006 (contract test exists)
- Implementation before polish (T036-T040)

---

## All Possible Outcomes

### Success: Ready for Next Step

```
Tasks complete at specs/001-real-time-chat/tasks.md
Total: 37 tasks (18 marked parallel-safe)
Estimated execution time: 8-12 hours

Next command: /analyze (optional) or /implement
```

**What You Get**:
- `tasks.md` with 20-50 tasks (typical range)
- Clear dependencies noted
- Parallel markers [P] applied
- Exact file paths for each task

**Next Actions**:
- **Recommended**: Run `/analyze` to validate consistency
- **Alternative**: Run `/implement` directly (faster but higher risk)

### Error: Missing Prerequisites

```
Error: Missing prerequisite file plan.md
Run /plan first to create implementation plan.
```

**Resolution**: Run `/plan` before `/tasks`

### Error: Invalid Artifacts

```
Error: plan.md is malformed (missing Technical Context section)
Check plan.md structure and regenerate if needed.
```

**Resolution**:
1. Open `specs/###-feature-name/plan.md`
2. Verify all required sections exist
3. If corrupted, regenerate with `/plan`

---

## Best Practices

### Review Task Count

| Task Count | Interpretation | Action |
|------------|----------------|--------|
| < 15 tasks | Underspecified feature | Consider adding more detail to plan.md |
| 20-50 tasks | Normal complexity | Proceed with confidence |
| > 50 tasks | Overspecified or too large | Consider breaking into multiple features |

### Verify TDD Ordering

**Check**: Are tests before implementation?

```markdown
✓ Good:
- T006 [P]: Contract test POST /users
- T010: Implement POST /users endpoint

✗ Bad:
- T006: Implement POST /users endpoint
- T010 [P]: Contract test POST /users
```

**Why**: TDD requires tests written first, fail initially, then pass after implementation.

### Check Parallel Markers

**Check**: Do [P] tasks truly have no dependencies?

```markdown
✓ Good:
- T016 [P]: User model in src/models/user.py
- T017 [P]: Message model in src/models/message.py
(Different files, no dependencies)

✗ Bad:
- T018 [P]: UserService in src/services/user_service.py
- T019 [P]: Update UserService with auth in src/services/user_service.py
(Same file - would conflict!)
```

### Validate File Paths

**Check**: Does each task specify exact files?

```markdown
✓ Good:
- T016: Create User model in src/models/user.py

✗ Bad:
- T016: Create User model
(No file path - too vague)
```

---

## Example: Real-Time Chat Tasks

### Complete tasks.md Structure

```markdown
# Tasks: Real-Time Chat

**Input**: Design documents from `/specs/001-real-time-chat/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Phase 1: Setup

- [ ] T001: Create project structure per implementation plan
  - Files: `pyproject.toml`, `src/chat/`, `tests/`
- [ ] T002: Initialize FastAPI project with dependencies
  - Files: `pyproject.toml` (add fastapi, asyncpg, redis)
- [ ] T003 [P]: Configure linting and formatting tools
  - Files: `.ruff.toml`, `mypy.ini`
- [ ] T004 [P]: Set up pytest with async support
  - Files: `pytest.ini`, `tests/conftest.py`
- [ ] T005: Create environment configuration
  - Files: `.env.example`, `src/chat/config.py`

## Phase 2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE PHASE 3

**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

- [ ] T006 [P]: Contract test POST /rooms
  - Files: `tests/contract/test_rooms_post.py`
  - Contract: `contracts/rooms.yaml`
- [ ] T007 [P]: Contract test WebSocket /ws
  - Files: `tests/contract/test_websocket.py`
  - Contract: `contracts/websocket.yaml`
- [ ] T008 [P]: Contract test GET /messages
  - Files: `tests/contract/test_messages_get.py`
  - Contract: `contracts/messages.yaml`
- [ ] T009 [P]: Integration test: Send Message scenario
  - Files: `tests/integration/test_send_message.py`
  - Scenario: `quickstart.md: Send Message`
- [ ] T010 [P]: Integration test: Real-time Delivery scenario
  - Files: `tests/integration/test_real_time_delivery.py`
  - Scenario: `quickstart.md: Real-time Delivery`
- [ ] T011 [P]: Integration test: View History scenario
  - Files: `tests/integration/test_view_history.py`
  - Scenario: `quickstart.md: View History`

## Phase 3: Core Implementation (ONLY after tests are failing)

- [ ] T012 [P]: Message model
  - Files: `src/chat/models/message.py`
  - Schema: `data-model.md: Message entity`
- [ ] T013 [P]: Room model
  - Files: `src/chat/models/room.py`
  - Schema: `data-model.md: Room entity`
- [ ] T014 [P]: User model
  - Files: `src/chat/models/user.py`
  - Schema: `data-model.md: User entity`
- [ ] T015: MessageService CRUD operations
  - Files: `src/chat/services/message_service.py`
  - Depends on: T012
- [ ] T016: RoomService business logic
  - Files: `src/chat/services/room_service.py`
  - Depends on: T013
- [ ] T017: POST /rooms endpoint
  - Files: `src/chat/api/rooms.py`
  - Depends on: T016, T006 (test exists)
- [ ] T018: GET /messages endpoint
  - Files: `src/chat/api/messages.py`
  - Depends on: T015, T008 (test exists)
- [ ] T019: WebSocket connection handler
  - Files: `src/chat/websocket/connection.py`
  - Depends on: T015, T016
- [ ] T020: WebSocket message routing
  - Files: `src/chat/websocket/router.py`
  - Depends on: T019, T007 (test exists)

## Phase 4: Integration

- [ ] T021: Connect MessageService to PostgreSQL
  - Files: `src/chat/services/message_service.py` (update)
  - Depends on: T012, T015
- [ ] T022: Redis Pub/Sub for message routing
  - Files: `src/chat/cache.py`, `src/chat/websocket/router.py` (update)
  - Depends on: T020
- [ ] T023: Auth middleware
  - Files: `src/chat/middleware/auth.py`
- [ ] T024: Request/response logging
  - Files: `src/chat/middleware/logging.py`

## Phase 5: Polish

- [ ] T025 [P]: Unit tests for MessageService
  - Files: `tests/unit/test_message_service.py`
- [ ] T026 [P]: Unit tests for RoomService
  - Files: `tests/unit/test_room_service.py`
- [ ] T027: Performance test for 1000 req/s target
  - Files: `tests/performance/test_load.py`
- [ ] T028 [P]: Update API documentation
  - Files: `docs/api.md`
- [ ] T029: Run manual-testing.md scenarios
  - Files: Various (validation)

## Dependencies

- Tests (T006-T011) before implementation (T012-T020)
- T012 blocks T015 (MessageService needs Message model)
- T013 blocks T016 (RoomService needs Room model)
- T015 blocks T018 (GET /messages needs MessageService)
- T016 blocks T017 (POST /rooms needs RoomService)
- T019 blocks T020 (Router needs connection handler)
- Implementation before polish (T025-T029)

## Parallel Execution Examples

```bash
# Launch all contract tests together (T006-T008):
Task: "Contract test POST /rooms in tests/contract/test_rooms_post.py"
Task: "Contract test WebSocket /ws in tests/contract/test_websocket.py"
Task: "Contract test GET /messages in tests/contract/test_messages_get.py"

# Launch all integration tests together (T009-T011):
Task: "Integration test Send Message in tests/integration/test_send_message.py"
Task: "Integration test Real-time Delivery in tests/integration/test_real_time_delivery.py"
Task: "Integration test View History in tests/integration/test_view_history.py"

# Launch all model creation together (T012-T014):
Task: "Create Message model in src/chat/models/message.py"
Task: "Create Room model in src/chat/models/room.py"
Task: "Create User model in src/chat/models/user.py"

# Launch all unit tests together (T025-T026):
Task: "Unit tests for MessageService in tests/unit/test_message_service.py"
Task: "Unit tests for RoomService in tests/unit/test_room_service.py"
```

## Notes

- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts
```

---

## Task Ordering Rules (Summary)

The task generation follows these ordering principles:

1. **Setup before everything**: Project must exist
2. **Tests before implementation**: TDD (test → code)
3. **Models before services**: Services depend on models
4. **Services before endpoints**: Endpoints call services
5. **Core before integration**: Core features before connections
6. **Everything before polish**: Polish assumes working code

**Visualization**:

```
Setup (1) → Tests (2) → Models (3) → Services (4) → Endpoints (5) → Integration (6) → Polish (7)
    ↓          ↓           ↓             ↓              ↓               ↓              ↓
  T001-T005  T006-T015   T016-T017    T018-T019      T020-T023       T024-T028     T029-T033
```

---

## Why This Matters

### Creates Executable Roadmap

- **Before `/tasks`**: Abstract plan ("use FastAPI, PostgreSQL")
- **After `/tasks`**: Concrete steps ("Create Message model in src/models/message.py")

### Enables Parallel Work

- **Without [P] markers**: Sequential execution only (slow)
- **With [P] markers**: Parallel execution where safe (faster)

### Enforces TDD Discipline

- **Without task ordering**: Developer might implement before testing
- **With task ordering**: Tests written first, fail initially, then pass

### Provides Progress Tracking

- **During `/implement`**: Tasks marked [X] one by one
- **On interruption**: Clear resume point
- **For estimation**: Task count → time estimate

---

## References

### Related Commands

- [Page 06: /plan Command](06-plan-command.md) - Creates design artifacts that /tasks reads
- [Page 09: /analyze Command](09-analyze-command.md) - Validates task completeness
- [Page 10: /implement Command](10-implement-command.md) - Executes tasks

### Knowledge Base

- `ai-docs/kb/04-commands-core.md` (lines 586-760) - Task command details
- `ai-docs/kb/10-workflows.md` (lines 310-375) - Task generation examples

### Source Files

- `templates/commands/tasks.md` - Command implementation
- `templates/tasks-template.md` - Task template structure
- `scripts/bash/check-prerequisites.sh` - Prerequisite validation

---

## Keywords

task breakdown, task generation, TDD ordering, dependency ordering, parallel execution, [P] markers, task numbering, task phases, test-first, implementation planning, actionable tasks, file paths, task dependencies, setup phase, test phase, core phase, integration phase, polish phase, task validation
