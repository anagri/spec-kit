# Workflow Patterns and Best Practices

**Purpose**: Guide to workflow variations, best practices, and time estimates for effective Spec Kit usage

**Target Audience**: Developers planning feature development workflows

**Related Documentation**:
- [Feature Workflow](02-feature-workflow.md) - Basic workflow introduction
- [Troubleshooting Guide](10-troubleshooting.md) - Common issues and solutions
- [Commands Reference](../kb/04-commands-core.md) - Detailed command documentation

---

## Choosing Your Workflow

Use this decision tree to select the appropriate workflow variation:

```
Is this your first feature in the project?
├─ Yes → Start with Constitution Phase
└─ No → Skip to Specify Phase

How complex is your feature?
├─ Simple (clear requirements, < 15 tasks)
│  └─ Use Minimal Workflow (5 commands)
│
├─ Complex (ambiguous requirements, 20-50 tasks)
│  └─ Use Recommended Workflow (7 commands)
│
└─ Exploratory (requirements emerge through design)
   └─ Use Iterative Refinement Workflow

What is your goal?
├─ Working implementation → Run full workflow
├─ Estimation/planning only → Design-Only Workflow
└─ Refining existing spec → Refinement After Feedback
```

---

## Workflow Variations

### 1. Minimal Workflow (5 Commands)

**Sequence**:
```
/constitution → /specify → /plan → /tasks → /implement
```

**Time Estimate**: 2-4 hours (depending on feature complexity)

**Risk Level**: Higher
- Ambiguities not resolved before planning
- Consistency not validated before implementation
- May require backtracking to fix issues

**When to Use**:
- Simple features with clear requirements
- Experienced users familiar with the domain
- Time-constrained situations where you accept higher risk
- Features similar to previously implemented ones

**Example Scenario**:
Adding a simple REST endpoint to an existing API where all requirements are obvious:
```
/specify "Add GET /health endpoint returning service status and version"
/plan "Python FastAPI endpoint, no database, return JSON"
/tasks
/implement
```

**Trade-offs**:
- **Pros**: Faster start, fewer commands to run, quicker iteration
- **Cons**: Higher chance of mid-implementation surprises, potential rework

---

### 2. Recommended Workflow (7 Commands)

**Sequence**:
```
/constitution → /specify → /clarify → /plan → /tasks → /analyze → /implement
```

**Time Estimate**: 3-6 hours (extra 30-60 minutes for clarify/analyze)

**Risk Level**: Lower
- Ambiguities resolved early via /clarify
- Consistency validated before execution via /analyze
- Fewer surprises during implementation

**When to Use**:
- Complex features with multiple requirements
- Team environments where quality gates matter
- Production features requiring high reliability
- Features involving multiple integrations

**Example Scenario**:
Building a real-time chat system with message history, user presence, and offline queuing:
```
/specify "Real-time chat system with message history and user presence"
/clarify  # Resolves latency targets, retention policy, auth method
/plan "Python 3.11, FastAPI, PostgreSQL, Redis, 10k concurrent users"
/tasks
/analyze  # Validates coverage, consistency
/implement
```

**Trade-offs**:
- **Pros**: Higher quality, fewer mid-implementation issues, better coverage
- **Cons**: More upfront time, requires interactive Q&A sessions

---

### 3. Iterative Refinement Workflow

**Initial Pass**:
```
/constitution → /specify → /clarify → /plan
```

**Review Point**:
User reviews plan.md and realizes requirements are incomplete or incorrect.

**Refinement Loop** (repeat as needed):
```
/specify [updated description] → /clarify [new questions] → /plan [regenerate]
```

**Final Execution**:
```
/tasks → /analyze → /implement
```

**Time Estimate**: 4-8 hours (depends on iteration count)

**When to Use**:
- Exploratory features where requirements emerge through design
- Complex domains requiring multiple refinement cycles
- Learning projects where you discover constraints during planning
- Features with uncertain technical approaches

**Example**:
```
Initial: /specify "User dashboard with analytics"
Review: Realizes dashboard needs to specify which metrics
Refinement: /specify "User dashboard showing login frequency, feature usage,
                      and error rates over last 30 days with daily granularity"
Review: Realizes data retention policy unclear
Refinement: /clarify  # Answers data retention, aggregation strategy
Continue: /plan → /tasks → /analyze → /implement
```

**Trade-offs**:
- **Pros**: Requirements fully explored before implementation starts
- **Cons**: Longer upfront time, multiple regenerations

---

### 4. Design-Only Workflow

**Sequence**:
```
/constitution → /specify → /clarify → /plan → /tasks → STOP
```

**Purpose**: Estimation, feasibility analysis, planning spike

**Outcome**:
- Complete tasks.md with effort estimates
- Technical plan with architecture decisions
- No code generated

**Time Estimate**: 2-3 hours (stops before implementation)

**When to Use**:
- Pre-commitment analysis for stakeholders
- Budget estimation for client projects
- Feasibility studies
- Comparing multiple technical approaches

**Example**:
```
/specify "Real-time collaborative text editor with CRDT conflict resolution"
/clarify  # Understand scale, latency requirements
/plan "Yjs library, WebSocket transport, PostgreSQL persistence"
/tasks  # Generate task list
# Review tasks.md: 45 tasks estimated at 60-80 hours
# Decision: Too complex for current sprint, defer to next quarter
```

**Trade-offs**:
- **Pros**: Low cost for high-value planning information
- **Cons**: No working code, requires discipline to stop before implementing

---

### 5. Refinement After Feedback

**Initial Run** (full workflow once):
```
/constitution → /specify → /clarify → /plan → /tasks → /implement
```

**Receive Feedback**: Stakeholder reviews implementation, requests changes

**Refinement** (regenerate from updated spec):
```
/specify [updated with feedback] → /plan [revised] → /tasks [regenerated] → /implement
```

**Time Estimate**: 1-3 hours for refinement (depends on change scope)

**When to Use**:
- Requirements changed after initial implementation
- Stakeholder feedback received during review
- New edge cases discovered during testing
- Performance targets adjusted

**Example**:
```
Initial: Chat system with 30-day message retention
Feedback: "Legal requires 90 days, and we need audit logs"
Refinement:
  /specify "...message retention for 90 days, audit log for all operations..."
  /plan  # Regenerates with new retention, adds audit logging
  /tasks  # New tasks for audit infrastructure
  /implement  # Updates implementation
```

**Trade-offs**:
- **Pros**: Systematic handling of requirement changes
- **Cons**: Regeneration overhead, potential conflicts with manual edits

---

## Best Practices by Phase

### Constitution Phase

**Do**:
- Define 4-6 principles (not too few or too many)
- Mix MUST (non-negotiable) and SHOULD (recommended) directives
- Use concrete metrics: "< 100ms p95 latency" not "fast"
- Include enforcement mechanism for each principle
- Version your constitution (1.0.0, 1.1.0, 2.0.0)

**Don't**:
- Use vague language: "fast", "scalable", "secure"
- Create too many principles (reduces clarity)
- Forget to define what violations mean

**Example Good Principle**:
```markdown
## Principle III: Test-Driven Development (NON-NEGOTIABLE)

**Mandate**: Contract tests MUST be written and approved before implementation

**Rationale**: Prevents rework, ensures testability, validates design early

**Enforcement**:
- Constitutional gate in /plan verifies contract test tasks exist
- /tasks generates test tasks before implementation tasks
- /implement executes tests before code
```

**Example Poor Principle**:
```markdown
## Principle: Quality

**Mandate**: Code should be high quality

**Rationale**: Quality is important

**Enforcement**: Code review
```

---

### Specify Phase

**Do**:
- Be specific about scale: "10k concurrent users" not "many users"
- Focus on WHAT not HOW: Avoid tech stack, frameworks, libraries
- Mention user goals: "Users need to...", "Admins want to..."
- Include edge cases and error scenarios
- Specify measurable success criteria

**Don't**:
- Include technical implementation details
- Assume obvious requirements (state them explicitly)
- Use vague adjectives without metrics

**Example Good Specification**:
```
/specify "Real-time chat supporting 10k concurrent connections with message
          delivery under 100ms p95 latency. Users can send text messages up to
          5000 characters. Messages retained for 30 days then archived. Offline
          users receive queued messages on reconnect."
```

**Example Poor Specification**:
```
/specify "Fast chat system using WebSockets"  # Too vague, includes tech (WebSockets)
```

---

### Clarify Phase

**Do**:
- Answer all 5 questions (don't terminate early unless truly not applicable)
- Provide metrics not adjectives: "< 100ms p95" not "fast"
- Resolve high-impact categories first (auth, data, scale)
- Be specific: "OAuth2 with Google/GitHub" not "social login"
- Think about edge cases when answering

**Don't**:
- Skip questions to save time (costs more later)
- Give vague answers: "reasonable time" → be specific: "30 days"
- Ignore categories marked "high priority"

**Example Good Answers**:
```
Q: What is the expected message delivery latency target?
A: < 100ms p95 latency  # Specific metric

Q: How long should message history be retained?
A: 30 days then archive to cold storage  # Concrete policy

Q: What authentication method should be used?
A: OAuth2 with Google and GitHub providers  # Exact providers
```

**Example Poor Answers**:
```
Q: What is the expected message delivery latency target?
A: Fast  # Vague, unmeasurable

Q: How long should message history be retained?
A: A while  # Unclear policy
```

---

### Plan Phase

**Do**:
- Provide detailed tech context as argument
- Let constitution gates catch violations early
- Review Complexity Tracking table if exceptions needed
- Don't skip Phase 0 research (justifies tech decisions)
- Verify constitutional check passes twice (pre/post design)

**Don't**:
- Provide generic tech stack: "latest versions"
- Ignore constitutional gate failures
- Skip documenting complexity violations

**Example Good Plan Command**:
```
/plan "Python 3.11, FastAPI 0.104, PostgreSQL 15 with asyncpg, Redis 7 for
       pub/sub, pytest with async support. Target 10k concurrent WebSocket
       connections, < 100ms message delivery p95, 99.9% uptime."
```

**Example Poor Plan Command**:
```
/plan "Python and database"  # Too vague, no versions, no scale
```

---

### Tasks Phase

**Do**:
- Review task count: 20-50 normal, >50 over-specified, <15 under-specified
- Verify TDD ordering: Tests before implementation tasks
- Check parallel markers [P]: Independent tasks should have them
- Validate file paths: Each task specifies exact files
- Ensure phases follow dependency order (Setup → Test → Core → Integration → Polish)

**Don't**:
- Accept tasks without file paths
- Ignore missing test tasks
- Skip dependency validation

**Example Good Tasks Review**:
```
Setup Phase (T001-T005):
✓ T001: Initialize project structure
✓ T002: Configure database connection
✓ T003: Set up pytest with async support

Test Phase (T006-T010): [All marked P for parallel]
✓ T006: Write contract test for POST /messages [P]
✓ T007: Write contract test for WebSocket /ws [P]

Core Phase (T011-T020):
✓ T011: Create Message model [P]
✓ T012: Implement MessageService (depends on T011)
✓ T013: Implement POST /messages endpoint (depends on T012, T006)

Count: 37 tasks (normal range)
Parallel: 18 tasks marked [P] (good parallelization)
TDD: Contract tests (T006-T010) before implementation (T013+)
```

---

### Analyze Phase

**Do**:
- Always run before /implement (cheap to fix now, expensive later)
- Remediate CRITICAL issues immediately (blocks implementation)
- Consider HIGH issues (may cause confusion)
- Review MEDIUM issues (improves quality)
- Ignore LOW issues unless time permits

**Don't**:
- Skip this step to save time (false economy)
- Proceed with CRITICAL issues unresolved
- Ignore coverage gaps

**Example Good Analysis Response**:
```
| ID | Category | Severity | Summary |
|----|----------|----------|---------|
| C1 | Coverage | CRITICAL | FR-008 "Message encryption" has zero tasks |

Action: Add Task T38: Implement end-to-end encryption (addresses FR-008)
```

---

### Implement Phase

**Do**:
- Monitor progress during execution
- Don't interrupt during phase completion
- Fix sequential failures immediately (blocks downstream)
- Review parallel failures after phase completes
- Verify all tests pass before considering feature complete

**Don't**:
- Interrupt mid-phase (can leave inconsistent state)
- Ignore test failures
- Skip verification steps

---

## Common Patterns

### Single Feature Development

**Full Workflow**:
```
/constitution  # Once per project
/specify       # Feature requirements
/clarify       # Resolve ambiguities
/plan          # Technical design
/tasks         # Task breakdown
/analyze       # Validate consistency
/implement     # Execute implementation
```

**Time Estimate**: 4-8 hours total (including implementation)

**Result**: Working feature with tests, documentation

---

### Multiple Feature Development

**Constitution Once**:
```
/constitution "Shared principles for all features"
# Committed to version control
```

**Per Feature** (repeat for each):
```
/specify "Feature A description" → specs/001-feature-a/
/clarify
/plan
/tasks
/analyze
/implement

/specify "Feature B description" → specs/002-feature-b/
/clarify
/plan
/tasks
/analyze
/implement
```

**Benefits**:
- Shared constitution ensures consistency
- Independent feature directories prevent conflicts
- Sequential numbering tracks progress

---

### Team Collaboration Patterns

#### Pattern 1: Spec Review Gate

**Developer Workflow**:
```
1. /specify "Feature description"
2. /clarify (resolve ambiguities)
3. git add specs/###-feature/spec.md
4. git commit -m "spec: Add feature specification"
5. Create pull request for spec review
6. Request review from product manager
```

**PM Review**:
```
- Read specs/###-feature/spec.md
- Validate functional requirements align with product vision
- Add comments or suggest changes via PR review
- Approve PR when satisfied
```

**Developer Continues** (after approval):
```
7. /plan "Tech stack details"
8. /tasks
9. /analyze
10. /implement
```

**Benefits**:
- Product alignment before implementation starts
- spec.md serves as shared contract
- Reduces wasted implementation effort
- Clear approval checkpoint

---

#### Pattern 2: Shared Constitution

**Team Lead Setup**:
```
1. /constitution "Team-wide architectural principles"
2. git add .specify/memory/constitution.md
3. git commit -m "constitution: Define team standards"
4. git push origin main
```

**Effect**:
- All developers clone repository with shared constitution
- Constitutional gates enforce team standards automatically
- Changes to constitution require team discussion via PR

**Example Team Constitution**:
```
"Microservices architecture; REST APIs with OpenAPI specs; PostgreSQL for
 persistence; Redis for caching; Docker deployment; 80% test coverage minimum;
 All endpoints documented in OpenAPI 3.0"
```

**Benefits**:
- Consistent architectural decisions across team
- Automated enforcement reduces code review burden
- Principle changes explicitly versioned

---

#### Pattern 3: Parallel Feature Development

**Developer A**:
```
/specify "Feature A: User authentication" → specs/001-user-auth/
/plan "OAuth2 with JWT tokens"
/tasks
/implement
```

**Developer B** (simultaneously):
```
/specify "Feature B: File upload" → specs/002-file-upload/
/plan "S3 storage with presigned URLs"
/tasks
/implement
```

**Merge Strategy**:
- No conflicts in spec directories (001-* vs 002-*)
- Both work on main branch (no branch overhead)
- Shared constitution ensures consistency
- Implementation code in separate modules

**Benefits**:
- No git branch conflicts
- Parallel progress tracking
- Shared governance prevents architectural drift

---

## Time Estimates

### Per-Command Time Investment

| Command                 | Time Range  | Notes                                |
|-------------------------|-------------|--------------------------------------|
| /constitution           | 30 min      | One-time per project                 |
| /clarify-constitution   | 15-30 min   | Only if markers exist                |
| /specify                | 15-30 min   | Per feature                          |
| /clarify                | 15-30 min   | 5 questions, interactive             |
| /plan                   | 1-2 hours   | Includes research + design + contracts |
| /tasks                  | 15-30 min   | Generation + review                  |
| /analyze                | 10-15 min   | Validation + remediation             |
| /implement              | 2-8 hours   | Depends heavily on feature complexity |

### Total Workflow Time

**Minimal Workflow**: 2-4 hours
- Skip clarify and analyze
- Higher risk, potential rework

**Recommended Workflow**: 4-10 hours
- Include clarify and analyze
- Lower risk, better quality

**With Iterations**: 6-15 hours
- Multiple specify/clarify/plan cycles
- Highest quality, fully explored requirements

---

## Decision Matrix

Use this matrix to decide which workflow variation to use:

| Feature Characteristic | Minimal | Recommended | Iterative | Design-Only |
|------------------------|---------|-------------|-----------|-------------|
| Clear requirements     | ✓       | ✓           |           | ✓           |
| Ambiguous requirements |         | ✓           | ✓         | ✓           |
| Simple implementation  | ✓       | ✓           |           |             |
| Complex implementation |         | ✓           | ✓         | ✓           |
| Time-constrained       | ✓       |             |           | ✓           |
| Production feature     |         | ✓           | ✓         |             |
| Estimation needed      |         |             |           | ✓           |
| Exploratory            |         |             | ✓         | ✓           |

---

## References

**Related Documentation**:
- [Feature Workflow Guide](02-feature-workflow.md) - Step-by-step workflow introduction
- [Command Reference](../kb/04-commands-core.md) - Detailed command documentation
- [Troubleshooting Guide](10-troubleshooting.md) - Common issues and solutions
- [Practical Workflows](../kb/10-workflows.md) - End-to-end examples with actual outputs

**Knowledge Base**:
- [Commands: Clarify](../kb/05-commands-clarify.md) - Enhancement commands details
- [Templates](../kb/06-templates.md) - Template constraint mechanisms
- [Design Insights](../kb/11-insights.md) - Trade-offs and design decisions

---

## Keywords

workflow variations, best practices, time estimates, decision tree, minimal workflow, recommended workflow, iterative refinement, design-only workflow, team collaboration, spec review gate, shared constitution, parallel development, per-phase practices, common patterns, single feature, multiple features, decision matrix
