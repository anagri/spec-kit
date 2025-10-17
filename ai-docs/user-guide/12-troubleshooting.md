# Troubleshooting & Error Recovery

**Purpose**: Document common errors and recovery strategies from user's perspective
**Target Audience**: Developers encountering issues during spec-kit workflows
**Related Guides**:
- [Getting Started](01-getting-started.md) - Installation and setup
- [Core Workflow](02-core-workflow.md) - Command sequence
- [Advanced Workflows](05-advanced-workflows.md) - Complex scenarios

---

## Common Errors by Command

### /constitution Errors

#### Error: Invalid template
**Message**: "Cannot load `.specify/memory/constitution.md`"
**Cause**: `.specify/` folder missing or corrupted
**Resolution**:
```bash
# Re-initialize spec-kit in the project
speclaude init --here --force

# Verify installation
ls -la .specify/memory/constitution.md
```

#### Error: Too many principles
**Message**: User created >10 principles
**Cause**: Over-specification, principles become hard to enforce
**Resolution**:
- Consolidate related principles into single governing rules
- Limit to 4-6 core principles
- Use MUST only for non-negotiable constraints
- Move guidelines to README.md or docs/ instead

**Best Practice**:
```markdown
❌ Too many principles:
- I. Use Python 3.11
- II. Use FastAPI
- III. Use PostgreSQL
- IV. Use Redis
- V. Use pytest
- VI. Use ruff
...

✅ Consolidated principles:
- I. Technology Stack (Python 3.11, FastAPI, PostgreSQL, Redis)
- II. Test-First Development (pytest, TDD mandatory)
- III. Code Quality (ruff linting, type hints required)
```

#### Issue: [NEEDS CLARIFICATION] markers remain
**Message**: Constitution created with incomplete sections
**Cause**: Insufficient initial input to fill all placeholders
**Resolution**:
```bash
# Run clarification command to resolve markers
/clarify-constitution

# Or manually edit constitution.md to replace markers
# Then update version metadata
```

---

### /specify Errors

#### Error: "No feature description provided"
**Message**: "Usage: create-new-feature.sh [--json] <feature_description>"
**Cause**: Empty `/specify` command
**Resolution**:
```bash
# Provide feature description as argument
/specify "your feature description here"

# Example
/specify "Add user authentication via OAuth2"
```

#### Error: Script execution failed
**Message**: "ERROR: specs/ directory not found" or "create-new-feature.sh --json failed"
**Cause**:
- Permissions issue with bash scripts
- `.specify/` folder missing
- Repo root detection failed

**Resolution**:
```bash
# 1. Verify .specify/ exists
ls -la .specify/scripts/bash/

# 2. Fix script permissions
chmod +x .specify/scripts/bash/*.sh

# 3. Test script directly
.specify/scripts/bash/create-new-feature.sh --json "test feature"

# 4. If repo root detection fails, check for .specify/ or .git/
pwd
ls -la .specify/ || ls -la .git/
```

#### Error: Feature ID collision
**Message**: Directory `specs/003-feature-name` already exists
**Cause**: Manual creation of specs/###-* directory conflicts with auto-numbering
**Resolution**:
- Let script assign IDs automatically
- Don't create feature directories manually
- If collision occurs, delete manual directory and re-run /specify
```bash
# Remove conflicting directory
rm -rf specs/003-conflicting-name

# Re-run specify command
/specify "actual feature description"
```

---

### /clarify Errors

#### Error: "Missing prerequisite file spec.md"
**Message**: "Run /specify first to create specification"
**Cause**: `/clarify` run before `/specify`
**Resolution**:
```bash
# Follow correct sequence
/specify "feature description"
# Then run clarify
/clarify
```

#### Warning: No questions generated
**Message**: "No critical ambiguities detected in specification"
**Cause**:
- Spec already complete and unambiguous (rare)
- Spec too vague to analyze (no concrete requirements)

**Resolution**:
- **If spec is actually complete**: Proceed to `/plan`
- **If spec is vague**: Review spec.md manually, add specific details:
  ```markdown
  ❌ Vague: "System should be fast"
  ✅ Specific: "System MUST deliver messages within <100ms p95 latency"

  ❌ Vague: "Support many users"
  ✅ Specific: "System MUST support 10,000 concurrent connections"
  ```
- Re-run `/specify` with more detailed description if needed

#### Issue: Early termination
**Symptom**: User types "done" after 2 questions, but 3 questions remain unanswered
**Consequence**: Some ambiguities unresolved, specification gaps remain
**Resolution**:
- **Option A**: Re-run `/clarify` to address remaining gaps
  ```bash
  /clarify
  # Answer remaining questions this time
  ```
- **Option B**: Accept risk and proceed to `/plan`
  - Document assumptions in plan.md
  - Be prepared for implementation changes if assumptions incorrect

---

### /plan Errors

#### Error: "Missing prerequisite file spec.md"
**Message**: "Run /specify first to create specification"
**Cause**: `/plan` run before `/specify`
**Resolution**:
```bash
# Follow correct sequence
/specify "feature description"
/plan "tech stack details"
```

#### Error: Constitution Check FAIL
**Message**: "Constitution Check: FAIL (X/6 gates) - Principle Y violated"
**Cause**: Plan violates a MUST principle from constitution

**Example Violation**:
```
Constitution Check: FAIL (5/6 gates)
✗ Anti-Abstraction Gate: Violates Principle VI "No wrapper abstractions"

Plan proposes creating ORM wrapper around SQLAlchemy.
This adds unnecessary abstraction layer.
```

**Resolution Options**:

**Option A - Refactor plan to comply** (preferred):
```bash
# Update plan approach to use framework directly
/plan "Use SQLAlchemy models directly, no wrapper layer"
```

**Option B - Document exception in Complexity Tracking**:
```markdown
## Complexity Tracking

| Principle Violation | Justification | Mitigation | Accepted? |
|---------------------|---------------|------------|-----------|
| Anti-Abstraction (Principle VI) | Legacy codebase requires wrapper for gradual migration | Extract wrapper in Phase 3 after migration complete | ✓ Deferred |
```

**Option C - Update constitution** (requires team discussion):
```bash
# If principle is too strict for project needs
/constitution "update Principle VI to allow minimal wrappers for legacy integration"
```

#### Warning: "Spec missing clarifications section"
**Message**: "PAUSE - Run /clarify first to reduce rework"
**Cause**: `/clarify` skipped when ambiguities detected in spec.md
**Resolution**:
```bash
# Run clarification before planning
/clarify
# Answer questions to resolve ambiguities
# Then re-run plan
/plan "tech stack details"
```

#### Error: Script execution failed
**Message**: "setup-plan.sh --json failed"
**Cause**: FEATURE_DIR detection failed or script permissions issue
**Resolution**:
```bash
# 1. Verify feature directory exists
ls -la specs/

# 2. Check SPECIFY_FEATURE env var
echo $SPECIFY_FEATURE

# 3. If not set, script uses highest-numbered directory
ls -la specs/ | grep -E '^[0-9]{3}-'

# 4. Verify repo root detection
.specify/scripts/bash/common.sh
```

---

### /tasks Errors

#### Error: "Missing plan.md"
**Message**: "Run /plan first to create implementation plan"
**Cause**: `/tasks` run before `/plan`
**Resolution**:
```bash
# Follow correct sequence
/specify "feature description"
/plan "tech stack"
/tasks
```

#### Warning: No contracts/ directory
**Message**: "contracts/ not found, skipping contract test tasks"
**Cause**: Feature doesn't need API contracts (e.g., CLI tool, library)
**Resolution**:
- This is normal for non-API features
- Tasks will be generated without contract tests
- Focus on integration tests from quickstart.md instead

#### Issue: Too many tasks (>50)
**Symptom**: tasks.md contains 60+ granular tasks
**Cause**: Over-specification in plan.md, too much implementation detail
**Resolution**:
```bash
# Review plan.md, consolidate related design elements
# Example: Merge 10 endpoint tasks into 3 service-level tasks
# Then regenerate tasks
/tasks

# Or manually edit tasks.md to consolidate:
# - [ ] T010-T019: Implement user service endpoints (consolidate 10 tasks)
```

#### Issue: Too few tasks (<15)
**Symptom**: tasks.md contains only 8 tasks for complex feature
**Cause**: Under-specification in plan.md, missing implementation details
**Resolution**:
```bash
# Add missing design artifacts to plan phase
# - Update data-model.md with all entities
# - Create contracts/ for all endpoints
# - Add quickstart.md integration scenarios
# Then regenerate tasks
/tasks
```

---

### /analyze Errors

#### Error: "Missing tasks.md"
**Message**: "Run /tasks first to generate task breakdown"
**Cause**: `/analyze` run before `/tasks`
**Resolution**:
```bash
# Follow correct sequence
/specify "feature"
/plan "tech stack"
/tasks
/analyze
```

#### CRITICAL: Coverage gaps
**Message**: "E1: FR-008 has zero associated tasks"
**Cause**: Requirement exists in spec.md but no task implements it
**Resolution**:

**Option A - Add task manually**:
```markdown
# Edit tasks.md, add new task
- [ ] T39: Implement graceful degradation under load
  - Files: src/middleware/rate_limit.py
  - Requirement: FR-008
  - Test: tests/performance/test_degradation.py
```

**Option B - Regenerate tasks after updating plan**:
```bash
# Update plan.md to include missing design elements
# Add to research.md: Rate limiting strategy
# Add to contracts/: Rate limit headers
# Then regenerate
/tasks
/analyze  # Verify coverage improved
```

#### CRITICAL: Constitution violation
**Message**: "D1: Plan violates Principle III (TDD Mandatory)"
**Cause**: tasks.md has implementation tasks before test tasks
**Resolution**:

**Option A - Reorder tasks in tasks.md**:
```markdown
# Move test tasks before implementation
## Core Phase
- [ ] T010: Write contract test for POST /users [P]
- [ ] T011: Write integration test for user creation [P]
- [ ] T012: Implement POST /users endpoint  # After tests
```

**Option B - Regenerate tasks**:
```bash
# The /tasks command enforces TDD by default
# Regenerating should fix ordering
/tasks
```

---

### /implement Errors

#### Error: "Missing tasks.md"
**Message**: "Run /tasks first to generate task breakdown"
**Cause**: `/implement` run before `/tasks`
**Resolution**:
```bash
# Follow correct sequence
/specify → /plan → /tasks → /implement
```

#### Halt: Sequential task failed
**Symptom**:
```
[T002] Configure database connection
ERROR: PostgreSQL not installed
Implementation halted
```
**Consequence**: Downstream tasks blocked, implementation cannot continue
**Resolution**:
```bash
# 1. Fix the error (install PostgreSQL)
brew install postgresql@15  # macOS
sudo apt install postgresql-15  # Ubuntu

# 2. Mark task incomplete in tasks.md
# Change [X] to [ ] for T002

# 3. Re-run /implement (resumes from T002)
/implement
```

#### Warning: Parallel task failed
**Symptom**:
```
[T006, T007, T008 parallel execution]
✓ T006: Create Message model - Success
✗ T007: Create Room model - ERROR: Import failed
✓ T008: Create User model - Success
```
**Consequence**: Implementation continues with T006/T008, T007 failure reported
**Resolution**:
```bash
# 1. Review T007 error after phase completion
# 2. Fix error (e.g., add missing import)
# 3. Mark T007 incomplete: [ ] instead of [X]
# 4. Re-run /implement (only runs incomplete tasks)
/implement
```

#### Error: Tests failing
**Symptom**:
```
[T006] Contract test for POST /messages
✓ Created tests/contract/test_messages.py
✓ Test fails as expected (no implementation)

[T010] Implement POST /messages endpoint
✓ Created src/api/messages.py
✗ Contract test still failing
ERROR: Response missing 'message_id' field
```
**Cause**: Implementation doesn't match contract specification
**Resolution**:
```bash
# 1. Review contracts/messages.yaml for required fields
cat specs/003-chat/contracts/messages.yaml

# 2. Fix implementation to match contract
# Add missing 'message_id' field to response

# 3. Re-run test manually to verify
pytest tests/contract/test_messages.py

# 4. Continue implementation
/implement
```

---

## Recovery Strategies

### Command Sequence Errors

**Problem**: Ran `/plan` before `/specify`
**Symptom**: "Missing prerequisite file spec.md"
**Solution**:
```bash
# Follow the correct sequence
/constitution  # Once per project
/specify "feature description"
/clarify       # Optional but recommended
/plan "tech stack"
/tasks
/analyze       # Optional but recommended
/implement
```

**Verification**: Check prerequisite files exist before running command
```bash
# Before /plan
ls specs/###-feature-name/spec.md

# Before /tasks
ls specs/###-feature-name/plan.md

# Before /implement
ls specs/###-feature-name/tasks.md
```

---

### Constitution Gate Failures

**Problem**: Plan violates constitutional principle
**Symptom**: "Constitution Check: FAIL (X/6 gates)"

**Solutions**:

**1. Refactor design to comply** (preferred):
```bash
# Identify violation
# "Anti-Abstraction Gate: FAIL - Creating ORM wrapper"

# Update plan to comply
/plan "Use SQLAlchemy models directly, no wrapper layer"

# Verify compliance
# Constitution Check: PASS (6/6 gates)
```

**2. Document exception in Complexity Tracking table**:
```markdown
## Complexity Tracking

| Principle Violation | Justification | Mitigation | Accepted? |
|---------------------|---------------|------------|-----------|
| Wrapper abstraction (VI) | Legacy system requires gradual migration | Remove wrapper in Phase 3 | ✓ Deferred |
```

**3. Update constitution if principle too strict**:
```bash
# Requires team discussion and explicit decision
/constitution "Revise Principle VI: Allow minimal wrappers for legacy integration only"
```

**Prevention**: Provide clear tech context in `/plan` argument
```bash
# Good: Specific tech stack that aligns with constitution
/plan "Use FastAPI WebSockets directly, PostgreSQL with asyncpg, Redis Pub/Sub"

# Bad: Vague approach that may conflict
/plan "Create abstraction layer for messaging"
```

---

### Coverage Gaps in /analyze

**Problem**: Requirements with zero tasks
**Symptom**: "/analyze reports CRITICAL: FR-X has zero coverage"

**Solutions**:

**1. Regenerate /tasks after updating plan.md**:
```bash
# Add missing design elements to plan.md
# - Update research.md with FR-X approach
# - Add to data-model.md if entity needed
# - Create contract in contracts/ if API needed
# Then regenerate
/tasks
/analyze  # Verify coverage improved
```

**2. Manually add task to tasks.md**:
```markdown
## Integration Phase
- [ ] T38: Implement graceful degradation (FR-008)
  - Files: src/middleware/circuit_breaker.py
  - Test: tests/integration/test_degradation.py
  - Requirement: FR-008 from spec.md
```

**3. Remove requirement from spec.md if not needed**:
```bash
# If FR-X was added by mistake or out of scope
# Update spec.md to remove or mark as deferred
# Then re-run analysis
/analyze
```

**Prevention**: Run `/analyze` before `/implement` to catch gaps early
```bash
# Recommended workflow
/tasks
/analyze  # Validation checkpoint
# Fix any issues found
/implement
```

---

### Implementation Failures

**Problem**: Task execution error during /implement
**Symptom**: "ERROR: Failed to create file" or "ERROR: Test failed"

**Solutions**:

**1. Fix error immediately**:
```bash
# Install missing dependency
pip install missing-package

# Fix code error
# Edit file to correct issue

# Re-run implementation
/implement  # Resumes from first incomplete task
```

**2. Mark task incomplete and debug**:
```bash
# 1. Mark task incomplete in tasks.md
# Change: [X] T010: Implement endpoint
# To:     [ ] T010: Implement endpoint

# 2. Debug the issue
pytest tests/unit/test_feature.py -v

# 3. Fix and re-run
/implement
```

**3. Skip problematic task temporarily**:
```bash
# Mark as complete to skip: [X] T010
# Add TODO comment: "# TODO: Fix T010 import error"
# Continue with other tasks
/implement

# Return later to fix T010
# Mark incomplete: [ ] T010
/implement  # Runs only T010
```

**Prevention**: Run `/analyze` before `/implement` to catch issues early
```bash
/tasks
/analyze  # Check for constitution violations, coverage gaps
# Fix issues before implementation
/implement
```

---

## State Management

### SPECIFY_FEATURE Environment Variable

**Purpose**: Override which feature commands operate on
**Default**: Highest-numbered feature in specs/
**Usage**:
```bash
# Set explicit feature context
export SPECIFY_FEATURE=002-user-auth

# Verify current feature
echo $SPECIFY_FEATURE

# Run commands on specific feature
/plan "tech stack"
/tasks
/implement

# Clear to return to default behavior
unset SPECIFY_FEATURE
```

**Example Use Cases**:
```bash
# Work on older feature while newer feature exists
export SPECIFY_FEATURE=002-old-feature
/plan "updated tech stack"

# Test feature in isolation
export SPECIFY_FEATURE=001-test-feature
/implement

# CI/CD automation
export SPECIFY_FEATURE=${FEATURE_FROM_ENV}
/tasks
```

---

### Feature Switching

**Scenario**: Multiple features in progress, need to switch between them
**Method**:
```bash
# Switch to feature 002
export SPECIFY_FEATURE=002-authentication
/plan "OAuth2 with JWT tokens"
/tasks
/implement

# Switch to feature 003
export SPECIFY_FEATURE=003-notifications
/plan "WebSocket push notifications"
/tasks
/implement

# Return to latest feature (default behavior)
unset SPECIFY_FEATURE
/plan "latest feature tech stack"
```

**Verification**:
```bash
# Check which feature is active
echo $SPECIFY_FEATURE

# List all features
ls -d specs/*/

# View current feature details
cat specs/$SPECIFY_FEATURE/spec.md
```

---

### Resume Implementation After Interruption

**Scenario**: `/implement` interrupted mid-execution (timeout, error, manual stop)
**Method**:
```markdown
# tasks.md tracks completion with [X] markers
## Core Phase
- [X] T001: Initialize project
- [X] T002: Configure database
- [ ] T003: Create models     ← Interruption here
- [ ] T004: Implement services
- [ ] T005: Add endpoints
```

**Recovery**:
```bash
# Re-run /implement
/implement

# Automatically resumes from first [ ] (incomplete) task
# In this case: T003
# No need to re-run T001, T002 (already [X])
```

**Manual Resume**:
```bash
# If need to re-run specific task, mark incomplete
# Change [X] to [ ] for that task
# Then re-run
/implement
```

---

### Reset Feature State

**Scenario**: Want to start feature development over from scratch
**Method**:
```bash
# 1. Delete feature directory
rm -rf specs/003-feature-name/

# 2. Re-run /specify
/specify "feature description"

# 3. Follow full workflow again
/clarify
/plan "tech stack"
/tasks
/implement
```

**Partial Reset** (keep spec, regenerate plan):
```bash
# Keep spec.md, delete other artifacts
cd specs/003-feature-name/
rm plan.md research.md data-model.md tasks.md
rm -rf contracts/

# Regenerate from spec
/plan "new tech approach"
/tasks
/implement
```

---

## Debugging Tips

### Check Script Outputs

**Scripts output JSON to stdout, errors to stderr**:
```bash
# Run script directly to see output
.specify/scripts/bash/create-new-feature.sh --json "test feature"

# Expected output (stdout):
{"FEATURE_ID":"001-test-feature","SPEC_FILE":"/path/to/specs/001-test-feature/spec.md","FEATURE_NUM":"001"}

# Error output (stderr):
ERROR: specs/ directory not found
```

**Verify JSON is parseable**:
```bash
# Test JSON parsing
echo '{"FEATURE_ID":"001-test"}' | jq .

# If jq not installed
echo '{"FEATURE_ID":"001-test"}' | python3 -m json.tool
```

---

### Verify File Paths

**Commands expect absolute paths, scripts provide them**:
```bash
# Check paths in JSON outputs
.specify/scripts/bash/check-prerequisites.sh --json | jq .

# Expected output
{
  "FEATURE_DIR": "/Users/dev/myproject/specs/003-feature",
  "AVAILABLE_DOCS": ["spec.md", "plan.md"],
  "REPO_ROOT": "/Users/dev/myproject"
}
```

**Verify repo root detection**:
```bash
# Test root detection priority
cd your-project/
pwd
ls -la .specify/  # Priority 1: .specify marker
ls -la .git/      # Priority 2: .git marker

# If both exist, .specify takes priority (monorepo support)
```

---

### Validate Bash Script Permissions

**Scripts must be executable**:
```bash
# Check permissions
ls -l .specify/scripts/bash/*.sh

# Expected output (note x flags):
-rwxr-xr-x  create-new-feature.sh
-rwxr-xr-x  setup-plan.sh
-rwxr-xr-x  check-prerequisites.sh
-rwxr-xr-x  common.sh

# Fix permissions if needed
chmod +x .specify/scripts/bash/*.sh
```

**Test script directly**:
```bash
# Run script to verify execution
.specify/scripts/bash/create-new-feature.sh --json "test feature"

# If permission denied
bash .specify/scripts/bash/create-new-feature.sh --json "test feature"
```

---

### Check Constitutional Compliance

**Load constitution and verify principles**:
```bash
# View constitution
cat .specify/memory/constitution.md

# Identify MUST principles (non-negotiable)
grep "MUST" .specify/memory/constitution.md

# Compare plan against principles manually
cat specs/003-feature/plan.md
```

**Look for Complexity Tracking table in plan.md**:
```markdown
## Complexity Tracking

| Principle Violation | Justification | Mitigation | Accepted? |
|---------------------|---------------|------------|-----------|
| (empty = no violations) | | | |
```

**If violations documented**:
```bash
# Review justification
# Verify mitigation strategy exists
# Check if accepted as deferred
```

---

## References

**Related Documentation**:
- [Getting Started](01-getting-started.md) - Installation and verification steps
- [Core Workflow](02-core-workflow.md) - Command sequence and prerequisites
- [Constitution Guide](04-constitution.md) - Understanding principles and gates
- [Advanced Workflows](05-advanced-workflows.md) - Complex scenarios and recovery
- [FAQ](11-faq.md) - Frequently asked questions

**Technical References**:
- [Bash Automation](../kb/07-bash-automation.md) - Script behaviors and JSON contracts
- [Commands: Core](../kb/04-commands-core.md) - Command error handling details
- [Commands: Clarify](../kb/05-commands-clarify.md) - Enhancement command behaviors

**File Paths** (for debugging):
- Constitution: `.specify/memory/constitution.md`
- Templates: `.specify/templates/*.md`
- Scripts: `.specify/scripts/bash/*.sh`
- Commands: `.claude/commands/*.md`
- Features: `specs/###-feature-name/`

---

## Keywords

troubleshooting, error recovery, debugging, common errors, constitution gates, coverage gaps, task failures, command sequence, state management, SPECIFY_FEATURE, feature switching, implementation resume, script debugging, permission errors, JSON parsing, file paths, constitutional compliance
