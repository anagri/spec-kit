# Page 10: /implement - Code Generation

**What This Command Does**: Executes the implementation plan by processing all tasks defined in `tasks.md`, following Test-Driven Development (TDD) discipline and respecting task dependencies to generate working code from specifications.

---

## When to Use This Command

Run `/implement` after you have:

- ✅ Completed `/tasks` successfully (tasks.md exists)
- ✅ Optionally validated consistency with `/analyze`
- ✅ Reviewed the task breakdown and confirmed it matches your requirements
- ✅ Ensured all prerequisites are in place (dependencies, environment setup)

**Do NOT run `/implement` if**:

- ❌ You haven't run `/tasks` yet (no task breakdown exists)
- ❌ Tasks.md has unresolved errors or inconsistencies
- ❌ You need to change requirements (update spec.md first, regenerate tasks)

---

## What This Command Requires

### Required Files

- **tasks.md** - Complete task breakdown with phases, dependencies, file paths
- **plan.md** - Technical implementation strategy, architecture, tech stack
- **spec.md** - Original feature specification with requirements

### Optional Files (Used If Available)

- **data-model.md** - Entity definitions, relationships, database schema
- **contracts/** - API specifications (OpenAPI, GraphQL, etc.)
- **research.md** - Technology decisions, trade-offs, constraints
- **quickstart.md** - Integration test scenarios

---

## What You'll See During Execution

### 1. Prerequisite Check

```
Running script: check-prerequisites.sh --json --require-tasks --include-tasks
✓ All prerequisites satisfied
```

**What's happening**: Validates that all required files exist and the feature context is properly configured.

### 2. Loading Implementation Context

```
Loading implementation context...
✓ Loaded tasks.md (38 tasks)
✓ Loaded plan.md (tech stack: Python 3.11, FastAPI, PostgreSQL, Redis)
✓ Loaded data-model.md (3 entities, 12 fields)
✓ Loaded contracts/ (2 files: websocket-events.yaml, rest-endpoints.yaml)
✓ Loaded research.md (technology decisions)
✓ Loaded quickstart.md (5 integration scenarios)
```

**What's happening**: Claude reads all available design artifacts to build complete context for implementation.

### 3. Parsing Task Structure

```
Parsing tasks.md structure...
✓ Task phases extracted: Setup, Test, Core, Integration, Polish
✓ Dependencies identified: 20 sequential, 18 parallel [P]
✓ Parallel markers [P] detected: 18 tasks
✓ File paths extracted per task: 38 file mappings
```

**What's happening**: Analyzes task dependencies, identifies which tasks can run in parallel, and creates execution plan.

---

## Phase-by-Phase Execution

### Setup Phase (T001-T005)

**Purpose**: Initialize project structure, dependencies, configuration

```
Starting Setup Phase (T001-T005)...

[T001] Initialize FastAPI project structure
Creating pyproject.toml...
Creating src/chat/ directory structure...
Creating tests/ directory...
✓ Project structure created
→ Marked [X] in tasks.md

[T002] Configure PostgreSQL connection
Creating src/chat/db.py...
✓ Async connection pool configured
→ Marked [X] in tasks.md

[T003] Configure Redis connection
Creating src/chat/cache.py...
✓ Redis client configured with Pub/Sub support
→ Marked [X] in tasks.md

[T004] Set up pytest with async support
Creating pytest configuration...
Adding pytest-asyncio to dependencies...
✓ Test framework configured
→ Marked [X] in tasks.md

[T005] Configure linting (ruff, mypy)
Creating ruff.toml, mypy.ini...
✓ Linting configured
→ Marked [X] in tasks.md

Setup Phase Complete (5/5 tasks)
```

**Key Behaviors**:

- Tasks run sequentially (no [P] markers in Setup)
- Each task completion immediately marked with `[X]` in tasks.md
- Failure in Setup halts execution (nothing will work without proper setup)

### Test Phase (T006-T015)

**Purpose**: Write contract and integration tests BEFORE implementation (TDD enforcement)

```
Starting Test Phase (T006-T015)...

[Running T006, T007, T008 in parallel - contract tests]

[T006] Write contract test for POST /rooms endpoint [P]
✓ Created tests/contract/test_rooms.py
✓ Test fails as expected (no implementation yet)
→ Marked [X] in tasks.md

[T007] Write contract test for WebSocket /ws endpoint [P]
✓ Created tests/contract/test_websocket.py
✓ Test fails as expected (no implementation yet)
→ Marked [X] in tasks.md

[T008] Write contract test for GET /messages endpoint [P]
✓ Created tests/contract/test_messages.py
✓ Test fails as expected (no implementation yet)
→ Marked [X] in tasks.md

[Running T009, T010 in parallel - integration tests]

[T009] Integration test for message sending [P]
✓ Created tests/integration/test_message_sending.py
✓ Test written based on quickstart.md scenario
→ Marked [X] in tasks.md

[T010] Integration test for real-time delivery [P]
✓ Created tests/integration/test_real_time.py
✓ Test written based on quickstart.md scenario
→ Marked [X] in tasks.md

Test Phase Complete (10/10 tasks)
```

**Key Behaviors**:

- **TDD Enforced**: Tests written before any implementation code
- **Parallel Execution**: Tasks with [P] markers run concurrently (different files)
- **Expected Failures**: Contract tests fail initially (no implementation exists yet)
- **Scenario-Based**: Integration tests derived from quickstart.md user scenarios

### Core Phase (T016-T030)

**Purpose**: Implement models, services, endpoints to make tests pass

```
Starting Core Phase (T016-T030)...

[Running T016, T017 in parallel - models]

[T016] Create Message model [P]
✓ Created src/models/message.py with SQLAlchemy model
✓ Added fields: message_id, room_id, sender_id, text, metadata, created_at
✓ Contract tests now discover Message model
→ Marked [X] in tasks.md

[T017] Create Room model [P]
✓ Created src/models/room.py with SQLAlchemy model
✓ Added fields: room_id, name, created_at
✓ Added relationship to User (participants)
→ Marked [X] in tasks.md

[T018] Implement MessageService
✓ Created src/services/message_service.py
✓ Methods: create_message, get_messages, get_room_history
✓ Integration with Message model
→ Marked [X] in tasks.md

[T019] Implement RoomService
✓ Created src/services/room_service.py
✓ Methods: create_room, get_room, add_participant
✓ Integration with Room model
→ Marked [X] in tasks.md

[T020] Implement POST /messages endpoint
✓ Created src/api/messages.py
✓ POST /messages endpoint implementation
✓ Contract test T008 now passes!
→ Marked [X] in tasks.md

[T021] Implement GET /messages endpoint
✓ Added GET /messages to src/api/messages.py
✓ Returns room history with pagination
→ Marked [X] in tasks.md

[T022] Implement WebSocket connection handler
✓ Created src/websocket/connection.py
✓ WebSocket connection management
✓ Redis pub/sub integration for message routing
✓ Contract test T007 now passes!
→ Marked [X] in tasks.md

Core Phase Complete (15/15 tasks)
✓ Contract tests passing: 3/3
✓ Integration tests passing: 2/2
```

**Key Behaviors**:

- **Dependency Respect**: T018 (MessageService) waits for T016+T017 (models) to complete
- **Tests Turn Green**: Implementation makes previously failing contract tests pass
- **File-Based Coordination**: Tasks on same file run sequentially (T020, T021 both modify `src/api/messages.py`)
- **Parallel When Safe**: T016, T017 run concurrently (different files, no shared state)

### Integration Phase (T031-T035)

**Purpose**: Wire up database, middleware, external services, authentication

```
Starting Integration Phase (T031-T035)...

[T031] Database migrations for schema
✓ Created migrations/001_initial_schema.sql
✓ Tables: users, rooms, messages, room_participants
→ Marked [X] in tasks.md

[T032] Redis Pub/Sub setup for message routing
✓ Updated src/chat/cache.py with pub/sub channels
✓ Added message broadcast logic
→ Marked [X] in tasks.md

[T033] Authentication middleware
✓ Created src/middleware/auth.py
✓ JWT token validation
✓ User context injection
→ Marked [X] in tasks.md

[T034] Logging and monitoring
✓ Created src/utils/logging.py
✓ Structured logging with JSON format
✓ Request/response timing
→ Marked [X] in tasks.md

[T035] Health check endpoint
✓ Created src/api/health.py
✓ GET /health endpoint (database + Redis checks)
→ Marked [X] in tasks.md

Integration Phase Complete (5/5 tasks)
```

**Key Behaviors**:

- **Sequential Execution**: Integration tasks often depend on each other
- **External Dependencies**: Database, Redis, authentication services wired up
- **Production Readiness**: Logging, monitoring, health checks added

### Polish Phase (T036-T040)

**Purpose**: Unit tests, performance validation, documentation

```
Starting Polish Phase (T036-T040)...

[Running T036, T037 in parallel - unit tests]

[T036] Unit tests for MessageService [P]
✓ Created tests/unit/test_message_service.py
✓ All methods covered with mocked dependencies
→ Marked [X] in tasks.md

[T037] Unit tests for RoomService [P]
✓ Created tests/unit/test_room_service.py
✓ All methods covered with mocked dependencies
→ Marked [X] in tasks.md

[T038] Performance test for 1000 req/s target
Creating tests/performance/test_load.py...
Running performance test...
✓ Achieved 1200 req/s sustained (20% above target)
✓ Latency: 95ms p95 (target: <100ms)
→ Marked [X] in tasks.md

[T039] Performance test for graceful degradation [P]
Creating tests/performance/test_degradation.py...
Running degradation test...
✓ Service remains operational under 3x load
✓ Error responses returned when capacity exceeded
→ Marked [X] in tasks.md

[T040] API documentation
✓ Created docs/api.md with endpoint reference
✓ Added usage examples
→ Marked [X] in tasks.md

Polish Phase Complete (5/5 tasks)
```

**Key Behaviors**:

- **Unit Tests**: Added after integration tests (comprehensive coverage)
- **Performance Validation**: Tests verify non-functional requirements from spec.md
- **Documentation**: API reference generated from contracts and implementation

---

## All Possible Outcomes

### 1. Full Success

```
Implementation Complete!
✓ 38/38 tasks completed
✓ All tests passing (125 tests, 0 failures)
✓ Performance targets met

Final validation:
- Message delivery: 95ms p95 latency (target <100ms) ✓
- Throughput: 1200 req/s sustained (target 1000 req/s) ✓
- Test coverage: 94%
- All contract tests passing
- All integration tests passing

Summary:
- Setup: 5 tasks
- Test: 10 tasks
- Core: 15 tasks
- Integration: 5 tasks
- Polish: 5 tasks
- Total execution time: ~15 minutes

Feature complete at specs/003-real-time-chat/

Ready for deployment!
```

**Next Steps**: Review implementation, manually run tests, commit changes to git.

### 2. Partial Success

```
Implementation Partial!
✓ 32/38 tasks completed
✗ 6 tasks failed (all in parallel batch T036-T039)

Successful tasks:
- Setup: 5/5 ✓
- Test: 10/10 ✓
- Core: 15/15 ✓
- Integration: 5/5 ✓
- Polish: 2/6 (4 failures)

Failed tasks:
- T036: Unit test for MessageService [P] - Import error (missing mock library)
- T037: Unit test for RoomService [P] - Import error (missing mock library)
- T038: Performance test - Load generator timeout
- T039: Performance degradation test - Redis connection failure

✓ All contract tests passing
✓ All integration tests passing
⚠ Unit tests incomplete (missing pytest-mock dependency)
⚠ Performance tests inconclusive

Recommendation:
1. Add pytest-mock to dependencies (pyproject.toml)
2. Fix Redis configuration for load testing
3. Re-run /implement (will resume from first incomplete task)
```

**Next Steps**: Fix reported issues, re-run `/implement` to complete remaining tasks.

### 3. Halt (Critical Failure)

```
Implementation Halted!
✓ 12/38 tasks completed
✗ CRITICAL FAILURE at T013 (sequential task)

Completed phases:
- Setup: 5/5 ✓
- Test: 7/10 (halted)

Failed task:
[T013] Implement MessageService
✗ Import error: SQLAlchemy model Message not found
✗ File: src/services/message_service.py

Error context:
- T012 (Create Message model) marked [X] but file missing
- Possible cause: File creation succeeded but content empty
- Blocking: T014, T015, T020, T021 (all depend on MessageService)

Suggested fix:
1. Check src/models/message.py exists and contains Message class
2. If missing, manually create or re-run T012
3. Re-run /implement (will resume from T013)

Implementation stopped to prevent cascading failures.
```

**Next Steps**: Fix the blocking issue (T012), then re-run `/implement` to resume from T013.

### 4. Resume After Fix

```
Resuming implementation...
Scanning tasks.md for completion markers [X]...
✓ Found 32 completed tasks (T001-T032)
✗ Found 6 incomplete tasks (T033-T038)

Resuming from first incomplete task: T033

[T033] Authentication middleware
Creating src/middleware/auth.py...
✓ JWT token validation implemented
→ Marked [X] in tasks.md

[Continues with T034-T038...]

Implementation Complete!
✓ 38/38 tasks completed (6 resumed from previous run)
```

**Key Behavior**: Uses `[X]` markers in tasks.md to determine where to resume, skips already-completed tasks.

---

## Error Handling

### Sequential Task Failure → HALT

```
[T015] Implement POST /messages endpoint
✗ ERROR: MessageService import failed
✗ File: src/api/messages.py

HALT: Sequential task failed. Execution stopped.

Reason: T015 is not marked [P], indicating downstream tasks depend on it.
Continuing would cause cascading failures.

Action: Fix T015, then re-run /implement to resume.
```

**Why**: Sequential tasks are critical dependencies. Failure blocks downstream work.

### Parallel Task Failure → CONTINUE

```
[Running T036, T037, T038 in parallel - unit tests]

[T036] Unit tests for MessageService [P]
✗ ERROR: pytest-mock not installed

[T037] Unit tests for RoomService [P]
✓ Created tests/unit/test_room_service.py
→ Marked [X] in tasks.md

[T038] Performance test [P]
✓ Created tests/performance/test_load.py
→ Marked [X] in tasks.md

Parallel batch complete: 2/3 succeeded, 1 failed
✗ T036 failed (can be fixed and re-run independently)
✓ T037, T038 completed successfully
```

**Why**: Parallel tasks are independent. One failure doesn't block others from completing.

---

## Follow-up Actions

After `/implement` completes:

1. **Review Implementation Files**

   ```bash
   # Check generated files match expected structure
   tree src/ tests/

   # Review key implementation files
   cat src/api/messages.py
   cat src/models/message.py
   ```

2. **Run Tests Manually**

   ```bash
   # Verify contract tests pass
   pytest tests/contract/

   # Verify integration tests pass
   pytest tests/integration/

   # Verify unit tests pass
   pytest tests/unit/

   # Run performance tests
   pytest tests/performance/
   ```

3. **Fix Any Failures**

   - Check error messages from test output
   - Update implementation files as needed
   - Re-run `/implement` to regenerate (if major changes needed)
   - Or manually fix and re-test (if minor tweaks)

4. **Commit Changes to Git** (User Manual Action)

   ```bash
   # Review changes
   git status
   git diff

   # Commit implementation
   git add specs/003-real-time-chat/ src/ tests/
   git commit -m "Implement real-time chat feature (specs/003)"
   ```

5. **Deploy or Continue Development**
   - If all tests pass and performance targets met: Deploy to staging/production
   - If additional features needed: Start new `/specify` cycle
   - If requirements change: Update spec.md, regenerate with `/plan` → `/tasks` → `/implement`

---

## Best Practices

### During Execution

- ✅ **Monitor progress**: Watch phase completion messages to track advancement
- ✅ **Don't interrupt during phase**: Let each phase complete atomically (Setup, Test, Core, Integration, Polish)
- ✅ **Note parallel failures**: Parallel task failures don't block others, but should be reviewed after phase completes
- ✅ **Expect test failures initially**: Contract/integration tests written before implementation (TDD) will fail until Core phase completes

### After Failure

- ✅ **Fix sequential failures immediately**: These block all downstream tasks
- ✅ **Review parallel failures after phase**: May not block progress, but indicate issues to address
- ✅ **Check tasks.md for [X] markers**: Shows exactly which tasks completed successfully
- ✅ **Re-run `/implement` after fixes**: Automatically resumes from first incomplete task

### Validation

- ✅ **Verify tests pass**: Run pytest manually to confirm all contract, integration, and unit tests succeed
- ✅ **Check performance targets**: Ensure non-functional requirements from spec.md are met
- ✅ **Review generated code**: Spot-check implementation files for quality and correctness
- ✅ **Run linting/type checking**: Ensure code quality standards met (if configured in Setup phase)

---

## Why This Command Is Important

1. **Generates Working Code from Specifications**
   - Translates design artifacts (plan.md, data-model.md, contracts/) into executable code
   - Ensures implementation matches original requirements from spec.md

2. **Enforces TDD Discipline**
   - Tests written before implementation (Test Phase before Core Phase)
   - Contract tests validate API compliance
   - Integration tests verify user scenarios
   - Unit tests ensure component-level correctness

3. **Follows Dependency Order**
   - Setup before any code written
   - Models before services (services depend on models)
   - Services before endpoints (endpoints depend on services)
   - Core before integration (integration depends on working core)

4. **Enables Resumption After Interruption**
   - Atomic `[X]` marking in tasks.md after each task completion
   - Re-running `/implement` resumes from last incomplete task
   - No redundant work or lost progress

5. **Provides Real-Time Progress Visibility**
   - Phase-by-phase execution shows current stage
   - Task-by-task completion shows exact progress
   - Parallel execution indicators show concurrent work
   - Clear error messages with recovery suggestions

---

## Execution Flow Details

### 1. Setup First

**Why**: Initialize project structure, dependencies, configuration before writing any code.

**Tasks**: Project structure, database connection, test framework, linting configuration.

**Failure Impact**: HALT (nothing will work without proper setup).

### 2. Tests Before Code (TDD)

**Why**: Write tests that define expected behavior, then implement to make tests pass.

**Flow**:

1. Write contract test (expects endpoint to return 201 with specific schema)
2. Test fails (endpoint doesn't exist yet)
3. Implement endpoint in Core phase
4. Test passes (endpoint matches contract)

**Benefit**: Ensures testability, prevents rework, validates design early.

### 3. Respect Dependencies

**Example**:

- T016: Create Message model [P]
- T017: Create Room model [P]
- T018: Implement MessageService (depends on T016, T017)

**Execution**:

1. T016 and T017 run in parallel (independent, different files)
2. T018 waits for both to complete (mentions Message and Room models)
3. Only starts after T016 [X] and T017 [X] marked

**Why**: Prevents import errors, ensures code dependencies met before use.

### 4. File-Based Coordination

**Rule**: Tasks affecting the same file run sequentially.

**Example**:

- T020: Implement POST /messages (file: src/api/messages.py)
- T021: Implement GET /messages (file: src/api/messages.py)

**Execution**: T021 waits for T020 (both modify same file).

**Why**: Prevents merge conflicts, ensures file consistency.

### 5. Parallel Execution

**Rule**: Tasks with [P] marker can run concurrently when independent.

**Example**:

- T036: Unit test for MessageService [P] (file: tests/unit/test_message_service.py)
- T037: Unit test for RoomService [P] (file: tests/unit/test_room_service.py)

**Execution**: Run simultaneously (different files, no shared dependencies).

**Benefit**: Reduces total execution time, maximizes Claude's efficiency.

---

## Progress Tracking

### Atomic [X] Updates

**After each task completion**:

```markdown
## Core Phase

- [X] T016: Create Message model [P]
- [X] T017: Create Room model [P]
- [ ] T018: Implement MessageService
```

**Benefits**:

1. **Resumption**: Re-running `/implement` skips T016, T017, resumes at T018
2. **Visibility**: User sees exact progress state at any moment
3. **Rollback**: Can manually un-mark [X] to re-run specific tasks if needed

### Real-Time Progress Messages

```
[T016] Create Message model [P]
Creating src/models/message.py...
Adding fields from data-model.md...
✓ Model created with 6 fields
→ Marked [X] in tasks.md

Progress: 16/38 tasks completed (42%)
```

**User Experience**: Continuous feedback showing current task, actions taken, completion status.

---

## References

**Related Commands**:

- [Page 8: /tasks](08-tasks-command.md) - Generates the task breakdown that /implement executes
- [Page 6: /plan](06-plan-command.md) - Creates design artifacts (plan.md, contracts/) used during implementation

**Related Knowledge Base Articles**:

- [Commands: Core Workflow](../kb/04-commands-core.md) - Detailed `/implement` reference (lines 762-981)
- [Workflows](../kb/10-workflows.md) - End-to-end implementation examples (lines 489-590)
- [AI Patterns](../kb/09-ai-patterns.md) - Parallel execution awareness, error handling patterns

**Related User Guide Pages**:

- [Page 9: /analyze](09-analyze-command.md) - Optional pre-implementation validation
- [Page 11: Best Practices](11-best-practices.md) - Implementation quality guidelines

---

**Navigation**: [← Page 9: /analyze](09-analyze-command.md) | [Page 11: Best Practices →](11-best-practices.md)
