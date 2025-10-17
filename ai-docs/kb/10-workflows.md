# User Workflows and Practical Examples

**Purpose**: Comprehensive practical guide showing end-to-end workflows with real examples
**Target Audience**: Developers using spec-kit for actual feature development
**Related Files**:

- [Commands: Core](04-commands-core.md) - Command reference
- [Commands: Clarify](05-commands-clarify.md) - Enhancement commands
- [Overview](01-overview.md) - Quick workflow summary
- [AI Patterns](09-ai-patterns.md) - AI interaction patterns

**Keywords**: end-to-end workflows, practical examples, real-world usage, feature development, workflow patterns, team collaboration

---

## 1. Complete End-to-End Workflow

This section demonstrates a complete feature development lifecycle using a real-time chat system as the example.

### 1.1 Scenario Overview

**Feature**: Building a real-time chat feature from scratch
**Components**: WebSocket messaging, message history, user presence tracking
**Tech Stack**: Python 3.11, FastAPI, PostgreSQL, Redis
**Estimated Time**: 8-12 hours of implementation (following TDD)

---

### 1.2 Step 1: Project Initialization (One-Time Setup)

```bash
# Install spec-kit CLI
uv tool install specify-cli

# Initialize project
speclaude init my-chat-app
cd my-chat-app

# Verify installation
ls -la .specify/templates/    # Should have 4 .md files
ls -la .specify/scripts/bash/ # Should have 5 .sh files
ls -la .claude/commands/      # Should have 8 .md files
```

**Outcome**: Project structure created with templates, scripts, and Claude commands ready.

---

### 1.3 Step 2: Define Project Constitution

**Command**:

```
/constitution "Library-first architecture; CLI interfaces for all features; TDD mandatory; Integration testing with real databases; Maximum 3 projects; No wrapper abstractions"
```

**Claude Response**:

```
Loading constitution template...
Filling principles...

Constitution created at .specify/memory/constitution.md
Version: 1.0.0 (new constitution)

Principles defined:
- I. Library-First (every feature starts as standalone library)
- II. CLI Interface (text in/out, JSON support)
- III. Test-First (NON-NEGOTIABLE: TDD mandatory)
- IV. Integration Testing (real databases, no mocks)
- V. Simplicity (maximum 3 projects)
- VI. Anti-Abstraction (use framework directly)

✓ All sections complete

Next command: /specify
```

**Key Outcomes**:

- Six constitutional principles established
- Principles will gate all future design decisions
- Constitution version tracked (enables evolution)

---

### 1.4 Step 3: Create Feature Specification

**Command**:

```
/specify "Real-time chat system with message history and user presence"
```

**Claude Response**:

```
Running script: create-new-feature.sh --json "Real-time chat system with message history and user presence"
✓ Received: {"FEATURE_ID":"001-real-time-chat","SPEC_FILE":"...","FEATURE_NUM":"001"}

Creating specification...

Feature 001-real-time-chat created at specs/001-real-time-chat/spec.md

Sections completed:
- User Scenarios: 2 primary flows defined
- Functional Requirements: 8 requirements (4 with clarification markers)
- Key Entities: Message, Room, User

⚠ Clarifications needed (4):
- FR-001: Message delivery latency target
- FR-003: Message retention policy
- FR-006: User authentication method
- FR-007: Presence update frequency

Next command: /clarify
```

**Artifacts Generated**:

- `specs/001-real-time-chat/spec.md` with 8 functional requirements
- 4 requirements flagged for clarification
- Feature ID assigned: 001

**Key Insights**:

- Specification automatically identifies ambiguities
- Clarification markers (⚠) highlight gaps early
- Feature numbering enables tracking

---

### 1.5 Step 4: Resolve Ambiguities

**Command**:

```
/clarify
```

**Interaction Flow**:

```
Claude:
  Loading spec.md...
  Performing ambiguity scan across 10 categories...
  Generated 5 prioritized questions

  Question 1 of 5:
  What is the expected message delivery latency target?

  | Option | Description |
  |--------|-------------|
  | A      | < 100ms (real-time chat experience) |
  | B      | < 1s (near real-time, slight delay acceptable) |
  | C      | < 5s (delayed messaging, not real-time) |

User: A

Claude:
  ✓ Integrated into FR-001: "System MUST deliver messages with <100ms p95 latency"

  Question 2 of 5:
  How long should message history be retained?
  Format: Short answer (≤5 words)

User: 30 days then archive

Claude:
  ✓ Integrated into FR-003: "Messages retained for 30 days, then archived"

  Question 3 of 5:
  What authentication method should be used?

  | Option | Description |
  |--------|-------------|
  | A      | Email/password with JWT tokens |
  | B      | OAuth2 (Google, GitHub) |
  | C      | Single Sign-On (SSO) via SAML |

User: B

Claude:
  ✓ Integrated into FR-006: "Authentication via OAuth2 (Google, GitHub providers)"

  Question 4 of 5:
  How frequently should user presence be updated?
  Format: Short answer (≤5 words)

User: Every 30 seconds

Claude:
  ✓ Integrated into FR-007: "Presence updates every 30 seconds"

  Question 5 of 5:
  What should happen to messages when a user is offline?

  | Option | Description |
  |--------|-------------|
  | A      | Queue and deliver when user comes online |
  | B      | Drop messages, no queuing |
  | C      | Send push notifications |

User: A

Claude:
  ✓ Integrated into FR-005: "Queue messages for offline users, deliver on reconnect"

  Clarification complete!
  - 5 questions answered
  - 5 sections updated (Functional Requirements, Edge Cases)
  - Coverage: 9/10 categories resolved
  - 1 category deferred (Compliance - not applicable)

  Updated spec at specs/001-real-time-chat/spec.md

  Next command: /plan
```

**Key Outcomes**:

- 5 questions answered (mix of multiple-choice and short-answer)
- All answers directly integrated into spec.md
- Ambiguities reduced from 4 to 0
- 9/10 clarification categories resolved

---

### 1.6 Step 5: Create Implementation Plan

**Command**:

```
/plan "Use WebSocket for real-time messaging, PostgreSQL for message persistence, Redis for presence tracking"
```

**Claude Response**:

```
Running script: setup-plan.sh --json
✓ Received feature paths

Loading spec.md...
Loading constitution...

Filling Technical Context...
**Language**: Python 3.11
**Dependencies**: FastAPI, WebSockets, asyncpg, redis
**Storage**: PostgreSQL 15, Redis 7
**Testing**: pytest, httpx

Evaluating Constitution Check...
✓ Library-First Gate: Feature starts as library
✓ CLI Interface Gate: Chat CLI planned
✓ Test-First Gate: Contract tests before implementation
✓ Integration Testing Gate: Real PostgreSQL/Redis in tests
✓ Simplicity Gate: Single project structure
✓ Anti-Abstraction Gate: Using FastAPI WebSockets directly

Constitution Check: PASS (6/6 gates)

Executing Phase 0: Research...
Researching WebSocket best practices...
Researching PostgreSQL schema design...
Researching Redis Pub/Sub patterns...
✓ Created research.md

Executing Phase 1: Design & Contracts...
✓ Created data-model.md (Message, Room, User entities)
✓ Created contracts/websocket-events.yaml
✓ Created contracts/rest-endpoints.yaml
✓ Created quickstart.md (5 test scenarios)

Running: update-agent-context.sh claude
✓ Updated .claude/CLAUDE.md with tech stack

Re-evaluating Constitution Check (post-design)...
✓ All gates still pass

Describing Phase 2 task generation approach...
(Tasks will be generated by /tasks command)

Plan complete at specs/001-real-time-chat/plan.md

Artifacts generated:
- plan.md (implementation strategy)
- research.md (technology decisions)
- data-model.md (3 entities, 12 fields)
- contracts/websocket-events.yaml (4 events)
- contracts/rest-endpoints.yaml (6 endpoints)
- quickstart.md (5 integration scenarios)

Next command: /tasks
```

**Artifacts Generated**:

1. `plan.md` - Implementation phases and strategy
2. `research.md` - Technology research and justifications
3. `data-model.md` - Entity definitions (Message, Room, User)
4. `contracts/websocket-events.yaml` - 4 WebSocket events
5. `contracts/rest-endpoints.yaml` - 6 REST endpoints
6. `quickstart.md` - 5 integration test scenarios

**Constitution Check**:

- 6/6 gates passed
- Constitution enforced at both pre-design and post-design stages
- Principle violations caught early

---

### 1.7 Step 6: Generate Task Breakdown

**Command**:

```
/tasks
```

**Claude Response**:

```
Running script: check-prerequisites.sh --json
✓ Available docs: spec.md, plan.md, data-model.md, contracts/, quickstart.md

Loading design documents...
✓ Loaded plan.md (tech stack: Python 3.11, FastAPI, PostgreSQL, Redis)
✓ Loaded data-model.md (3 entities)
✓ Loaded contracts/ (2 files, 10 endpoints/events)
✓ Loaded quickstart.md (5 scenarios)

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

Tasks complete at specs/001-real-time-chat/tasks.md
Total: 37 tasks (18 marked parallel-safe)
Estimated execution time: 8-12 hours

Next command: /analyze (optional) or /implement
```

**Task Breakdown**:

- **Setup**: 5 tasks (project structure, dependencies)
- **Test**: 10 tasks (8 parallel-safe)
- **Core**: 12 tasks (implementation)
- **Integration**: 5 tasks (database, Redis, auth)
- **Polish**: 5 tasks (4 parallel-safe)

**Total**: 37 tasks, 18 marked `[P]` for parallel execution

---

### 1.8 Step 7: Validate Consistency

**Command**:

```
/analyze
```

**Claude Response**:

```
Running script: check-prerequisites.sh --json --require-tasks --include-tasks
✓ All required files present

Loading artifacts...
✓ Loaded spec.md (8 functional requirements, 3 entities, 4 user stories)
✓ Loaded plan.md (6 phases, 10 contracts)
✓ Loaded tasks.md (37 tasks)
✓ Loaded constitution (6 principles)

Building semantic models...
✓ Requirements inventory (8 requirements)
✓ User story mapping (4 stories)
✓ Task coverage mapping (37 tasks → requirements)

Running detection passes...

A. Duplication Detection: ✓ No duplicates found
B. Ambiguity Detection: ✓ All clarifications resolved
C. Underspecification: ✓ All requirements have measurable criteria
D. Constitution Alignment: ✓ No principle violations
E. Coverage Gaps: ⚠ 1 issue found
F. Inconsistency: ✓ No terminology drift

### Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| E1 | Coverage | MEDIUM | spec.md FR-008 | "Graceful degradation under load" requirement has no associated performance test task | Add Task T38: Performance test for graceful degradation |

#### Coverage Summary
| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| message-delivery-latency | ✓ | T022, T035 | Covered |
| message-persistence | ✓ | T008, T015 | Covered |
| user-authentication | ✓ | T025 | Covered |
| presence-tracking | ✓ | T026, T027 | Covered |
| offline-message-queue | ✓ | T028 | Covered |
| real-time-updates | ✓ | T022, T029 | Covered |
| message-history-retrieval | ✓ | T030 | Covered |
| graceful-degradation | ✗ | — | **Missing coverage** |

#### Constitution Alignment
✓ All principles satisfied

#### Metrics
- Total Requirements: 8
- Total Tasks: 37
- Coverage: 87.5% (7/8 requirements have ≥1 task)
- Ambiguity Count: 0
- Duplication Count: 0
- Critical Issues: 0
- High Issues: 0
- Medium Issues: 1

### Next Actions
- Add Task T38 to address missing coverage for FR-008
- Otherwise ready to proceed to /implement

Would you like me to suggest a concrete task description for T38?
```

**Remediation Flow**:

```
User: Yes, add T38

Claude:
  Suggested Task T38:

  **T38: Performance test for graceful degradation under load [P]**
  - File: tests/performance/test_degradation.py
  - Description: Simulate increasing load (1000 → 5000 concurrent connections) and verify:
    * Message delivery continues (may slow but not fail)
    * New connections accepted with exponential backoff
    * Error responses returned when capacity exceeded
    * No service crashes
  - Prerequisites: T035 (baseline performance test) complete
  - Success criteria: Service remains operational under 3x target load

  Shall I add this to tasks.md?

User: Yes

Claude:
  ✓ Added T38 to tasks.md (Polish Phase)
  ✓ Updated coverage: 8/8 requirements now have tasks

  Analysis complete with remediation!
  - Coverage: 100%
  - Ready for /implement
```

**Key Outcomes**:

- 1 coverage gap identified (FR-008 had no test task)
- Remediation suggested and applied
- Coverage improved from 87.5% to 100%
- All 6 analysis passes completed

---

### 1.9 Step 8: Execute Implementation

**Command**:

```
/implement
```

**Claude Response** (abbreviated):

```
Running script: check-prerequisites.sh --json --require-tasks --include-tasks
✓ All prerequisites satisfied

Loading implementation context...
✓ Loaded tasks.md (38 tasks)
✓ Loaded plan.md
✓ Loaded data-model.md
✓ Loaded contracts/

Starting Setup Phase (T001-T005)...

[T001] Initialize FastAPI project structure
Creating pyproject.toml...
Creating src/chat/ directory structure...
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
Installing pytest-asyncio...
✓ Test framework configured
→ Marked [X] in tasks.md

[T005] Configure linting (ruff, mypy)
Creating ruff.toml, mypy.ini...
✓ Linting configured
→ Marked [X] in tasks.md

Setup Phase Complete (5/5 tasks)

Starting Test Phase (T006-T015)...
[Running T006, T007, T008 in parallel - contract tests]

[T006] Write contract test for POST /rooms endpoint [P]
✓ Created tests/contract/test_rooms.py
✓ Test fails as expected (no implementation)
→ Marked [X] in tasks.md

[T007] Write contract test for WebSocket /ws endpoint [P]
✓ Created tests/contract/test_websocket.py
✓ Test fails as expected (no implementation)
→ Marked [X] in tasks.md

[T008] Write contract test for GET /messages endpoint [P]
✓ Created tests/contract/test_messages.py
✓ Test fails as expected (no implementation)
→ Marked [X] in tasks.md

[... continues through all 38 tasks ...]

Starting Polish Phase (T034-T038)...

[T035] Performance test for 1000 req/s target
Creating tests/performance/test_load.py...
Running performance test...
✓ Achieved 1200 req/s sustained (20% above target)
→ Marked [X] in tasks.md

[T038] Performance test for graceful degradation under load [P]
Creating tests/performance/test_degradation.py...
Running degradation test...
✓ Service remains operational under 3x load
→ Marked [X] in tasks.md

Implementation Complete!
✓ 38/38 tasks completed
✓ All tests passing (125 tests, 0 failures)
✓ Performance targets met
✓ Constitution principles followed

Final validation:
- Message delivery: <95ms p95 latency (target <100ms) ✓
- Throughput: 1200 req/s sustained (target 1000 req/s) ✓
- Test coverage: 94%
- All contract tests passing
- All integration tests passing

Feature complete at specs/001-real-time-chat/

Ready for deployment!
```

**Implementation Highlights**:

- 38 tasks executed sequentially (with parallel batches)
- TDD followed: tests written before implementation
- Tasks automatically marked `[X]` in tasks.md
- Performance targets exceeded (1200 req/s vs 1000 target)
- Constitution principles enforced throughout

---

## 2. Workflow Variations

### 2.1 Minimal Workflow (Skip Optional Commands)

**Sequence**:

```
/constitution → /specify → /plan → /tasks → /implement
```

**Characteristics**:

- **Time**: 2-4 hours (depending on feature complexity)
- **Risk**: Higher (ambiguities not resolved, consistency not validated)
- **When to Use**: Simple features with clear requirements
- **Trade-off**: Faster start, but may require backtracking

**Example Scenario**: Adding a simple "like" button to existing feature where requirements are obvious.

---

### 2.2 Recommended Workflow (Include Optional Commands)

**Sequence**:

```
/constitution → /specify → /clarify → /plan → /tasks → /analyze → /implement
```

**Characteristics**:

- **Time**: 3-6 hours (extra 30-60 minutes for clarify/analyze)
- **Risk**: Lower (ambiguities resolved early, consistency validated)
- **When to Use**: Complex features or team environments
- **Trade-off**: More upfront time, fewer mid-implementation surprises

**Example Scenario**: Building the real-time chat feature (as demonstrated above).

---

### 2.3 Iterative Refinement Workflow

**Initial Pass**:

```
/constitution → /specify → /clarify → /plan
[User reviews plan]
[User realizes requirements incomplete]
```

**Refinement Loop**:

```
/specify [update description] → /clarify [new questions] → /plan [regenerate]
```

**Final Execution**:

```
/tasks → /analyze → /implement
```

**When to Use**: Exploratory features where requirements emerge through design.

**Example**:

```
Initial: /specify "User dashboard with analytics"
Review: Realizes needs to specify which metrics
Refinement: /specify "User dashboard showing login frequency, feature usage, and error rates over last 30 days"
Continue: /plan → /tasks → /implement
```

---

## 3. Team Collaboration Patterns

While spec-kit is optimized for solo developers, it supports team workflows through structured artifacts.

### 3.1 Pattern 1: Spec Review Gate

**Developer Workflow**:

```
1. /specify "Feature description"
2. /clarify (resolve ambiguities)
3. Commit spec.md to git
4. Request review from product manager
```

**PM Review**:

```
- Reads specs/XXX-feature/spec.md
- Validates functional requirements
- Adds comments or updates spec.md directly
- Approves via pull request review
```

**Developer Continues**:

```
5. /plan (after approval)
6. /tasks
7. /implement
```

**Benefits**:

- Product alignment before implementation
- Spec.md serves as shared contract
- Reduces wasted implementation effort

---

### 3.2 Pattern 2: Shared Constitution

**Team Lead Setup**:

```
1. /constitution "Team-wide principles"
2. Commits .specify/memory/constitution.md to repository
3. All developers clone repository with shared constitution
```

**Effect**:

- Consistent architectural principles across team
- Constitutional gates enforce team standards automatically
- Changes to constitution require team discussion (via PR)

**Example Constitution for Team**:

```
"Microservices architecture; REST APIs only; PostgreSQL for persistence;
Redis for caching; Docker deployment; 80% test coverage minimum;
OpenAPI spec for all endpoints"
```

---

### 3.3 Pattern 3: Parallel Feature Development

**Developer A**:

```
/specify "Feature A" → Creates specs/001-feature-a/
```

**Developer B**:

```
/specify "Feature B" → Creates specs/002-feature-b/
```

**Both Work in Parallel**:

- No git branch conflicts (both on main, if desired)
- Feature directories isolated (`specs/001-*` vs `specs/002-*`)
- Can merge implementations independently
- Shared constitution ensures consistency

**Merge Strategy**:

- Each developer commits their `specs/` directory
- Implementation code in separate modules
- No conflicts in spec-kit artifacts

---

## 4. Troubleshooting Scenarios

### 4.1 Scenario: Missing Prerequisites

**Symptom**:

```
User: /plan

Claude:
  Error: Missing prerequisite file spec.md
  Run /specify first to create specification.
```

**Resolution**:

```
User: /specify "Feature description"
[Then retry /plan]
```

**Root Cause**: Commands have prerequisites enforced by `check-prerequisites.sh`.

---

### 4.2 Scenario: Constitution Gate Failure

**Symptom**:

```
User: /plan "Create ORM wrapper around SQLAlchemy"

Claude:
  Constitution Check: FAIL (1/6 gates)
  ✗ Anti-Abstraction Gate: Violates principle "No wrapper abstractions"

  Recommendation: Use SQLAlchemy directly instead of creating wrapper.
  Update plan to remove abstraction layer.
```

**Resolution**:

```
User: /plan "Use SQLAlchemy directly for database operations"

Claude:
  Constitution Check: PASS (6/6 gates)
  [Continues with planning...]
```

**Root Cause**: Plan violated constitutional principle VI (Anti-Abstraction).

---

### 4.3 Scenario: Coverage Gap in /analyze

**Symptom**:

```
User: /analyze

Claude:
  Coverage Gaps: ⚠ 2 issues found
  - FR-005: No task covers "offline message queue"
  - FR-008: No task covers "graceful degradation"
```

**Resolution**:

```
User: Add missing tasks

Claude:
  Suggested tasks:
  T39: Implement offline message queue
  T40: Test graceful degradation under load

  Shall I add these to tasks.md?

User: Yes

Claude:
  ✓ Added T39, T40
  ✓ Coverage: 100%
```

**Root Cause**: `/tasks` generated incomplete task list; `/analyze` caught gap.

---

## 5. Common Command Sequences

### 5.1 Quick Feature (No Clarification Needed)

```
/specify "Simple feature with clear requirements"
/plan "Straightforward tech approach"
/tasks
/implement
```

**Use Case**: Adding a simple endpoint or utility function.

---

### 5.2 Complex Feature (Full Workflow)

```
/constitution "Project principles" (if not already created)
/specify "Complex feature description"
/clarify (answer 3-5 questions)
/plan "Tech approach with architecture details"
/tasks
/analyze (validate consistency)
/implement
```

**Use Case**: Real-time chat system, payment integration, search feature.

---

### 5.3 Design-Only Workflow

```
/specify "Feature description"
/clarify
/plan
/tasks
[Stop - review tasks before implementing]
```

**Use Case**: Estimation, feasibility analysis, or planning spike.

---

### 5.4 Refinement After Feedback

```
[Already ran /specify, /clarify, /plan]
[Received feedback from stakeholder]

/specify "Updated feature description incorporating feedback"
/plan "Revised tech approach"
/tasks (regenerate task list)
/implement
```

**Use Case**: Requirements changed after initial design.

---

## Cross-References

**Related Documentation**:

- [Commands: Core](04-commands-core.md) - Detailed command syntax and parameters
- [Commands: Clarify](05-commands-clarify.md) - Ambiguity resolution mechanics
- [Overview](01-overview.md) - High-level workflow summary
- [AI Patterns](09-ai-patterns.md) - AI interaction strategies used in workflows
- [Script Pipeline](07-script-pipeline.md) - Bash scripts powering command execution
- [Insights](11-insights.md) - Design decisions behind workflow structure

**Navigation**: [← AI Patterns](09-ai-patterns.md) | [Insights →](11-insights.md)

---

## Keywords

workflow sequences, end-to-end examples, feature development, real-time chat, step-by-step, command execution, artifact generation, team collaboration, iterative refinement, troubleshooting, coverage gaps, constitution gates, TDD workflow, parallel development, spec review, shared standards
