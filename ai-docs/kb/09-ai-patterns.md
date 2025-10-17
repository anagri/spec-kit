# AI Interaction Patterns with Claude Code

**Purpose**: Explains how Claude Code processes templates and prevents hallucination through structured execution patterns
**Target Audience**: Developers understanding LLM behavior patterns and constraint-driven generation
**Related Files**:

- [Templates](06-templates.md) - Template constraint mechanisms
- [Workflows](10-workflows.md) - AI processing in action
- [Philosophy](02-philosophy.md) - Constraint-driven generation
  **Keywords**: templates as instructions, hallucination prevention, execution status, cascading context, constitutional reasoning, error handling

---

## Overview

Spec-kit templates aren't suggestions - they're executable instructions that Claude follows step-by-step. This document explains how Claude processes templates, maintains context, prevents hallucination, and handles errors through structured patterns.

**Key Patterns**:

1. **Templates as Instructions**: Pseudocode execution flows that Claude follows procedurally
2. **Hallucination Prevention**: Explicit markers that force clarification instead of guessing
3. **Structured Thinking**: Execution status checklists that show real-time progress
4. **Constitutional Reasoning**: Automated architectural validation gates
5. **Cascading Context**: Progressive context building across workflow stages
6. **Error Handling**: Explicit error conditions with recovery suggestions
7. **Parallel Execution**: Dependency-aware concurrent task execution

---

## 1. Templates as Instructions, Not Suggestions

### Critical Distinction

| Traditional Documentation         | Spec-Kit Templates                                                                                      |
| --------------------------------- | ------------------------------------------------------------------------------------------------------- |
| "Consider adding user stories"    | "4. Fill User Scenarios & Testing section → If no clear user flow: ERROR"                               |
| "Requirements should be testable" | "5. Generate Functional Requirements → Each requirement must be testable → Mark ambiguous requirements" |
| "Check for ambiguities"           | "3. For each unclear aspect: → Mark with [NEEDS CLARIFICATION: specific question]"                      |

### Execution Flow Format

Templates contain **pseudocode execution flows** that Claude follows step-by-step:

```markdown
## Execution Flow (main)

1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Insufficient description for user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify entities and relationships
   → Create Data Model section
7. Review against checklist
   → If any item fails: document in notes
8. Return: SUCCESS
```

### How Claude Processes Templates

**Processing Steps**:

1. **Reads execution flow**: Understands this is a procedure to execute, not guidelines
2. **Follows steps sequentially**: Processes step 1, then step 2, then step 3...
3. **Evaluates conditionals**: `If empty: ERROR` → checks condition, branches accordingly
4. **Reports progress**: Updates "Execution Status" checklist as each step completes
5. **Returns control**: `8. Return: SUCCESS` → signals completion to user

**Why This Works**: Claude's training includes following procedural instructions. Templates exploit this capability by providing clear, unambiguous execution paths.

**Example Processing**:

```
User: "Build a login system"

Claude (internal reasoning):
  Step 1: Parse user description → "login system" extracted
  Step 2: Key concepts → actors: users, actions: authenticate, data: credentials
  Step 3: Unclear aspects → auth method? password policy? session timeout?
  Step 3 action: Mark with [NEEDS CLARIFICATION: auth method not specified]
  Step 4: User scenarios → basic flow: user enters credentials, system validates
  Step 5: Generate requirements → FR-001: System MUST authenticate users...
  [continues through all steps]
  Step 8: Return SUCCESS
```

---

## 2. Preventing Hallucination Through Explicit Markers

### The Hallucination Problem

LLMs are trained to be helpful and fill in gaps. Given incomplete information, they generate plausible completions. For code generation, "plausible" often means "incorrect."

**Common hallucinations**:

- Assuming authentication methods (email/password vs OAuth vs SSO)
- Inventing password policies (length, complexity, rotation)
- Guessing session timeouts (30 min, 2 hours, 24 hours)
- Creating non-existent API endpoints or database schemas

### Spec-Kit's Solution: `[NEEDS CLARIFICATION]` Markers

**Template Instructions**:

```markdown
When creating this spec from a user prompt:

1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question]
2. **Don't guess**: If the prompt doesn't specify something, mark it
3. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
```

### Example: With vs Without Markers

**User prompt**: "Build a login system"

**Without markers** (hallucination-prone):

```markdown
- FR-001: System MUST authenticate users via email/password
- FR-002: Passwords MUST be hashed with bcrypt
- FR-003: Sessions MUST expire after 30 minutes
- FR-004: Failed login attempts MUST be rate-limited to 5 per minute
```

**With markers** (spec-kit approach):

```markdown
- FR-001: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- FR-002: Passwords MUST be hashed with [NEEDS CLARIFICATION: hashing algorithm preference - bcrypt, argon2, scrypt?]
- FR-003: Sessions MUST expire after [NEEDS CLARIFICATION: session timeout duration?]
- FR-004: Failed login attempts MUST be rate-limited to [NEEDS CLARIFICATION: rate limit threshold and window?]
```

### Effects of Marker-Driven Approach

**Benefits**:

- No assumptions made about critical security decisions
- All decisions explicit and documented
- User forced to clarify before implementation
- Prevents downstream rework from incorrect assumptions

**Validation Gate**:

```markdown
### Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] All requirements testable and unambiguous
```

If markers remain, Claude warns: "Spec has uncertainties, recommend `/clarify` before `/plan`"

---

## 3. Structured Thinking via Execution Status Checklists

### Real-Time Progress Tracking

Templates include **execution status checklists** that Claude updates as it works:

```markdown
## Execution Status

_Updated by main() during processing_

- [ ] User description parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked with [NEEDS CLARIFICATION]
- [ ] User scenarios defined
- [ ] Functional requirements generated
- [ ] Non-functional requirements identified
- [ ] Data entities extracted
- [ ] Review checklist passed
```

### Claude's Processing Pattern

**Execution Loop**:

1. Reads execution flow
2. Starts with first step: "Parse user description"
3. Completes step
4. **Updates checklist**: `- [X] User description parsed`
5. Proceeds to next step
6. Repeats until completion or error

**User Experience**: Sees real-time progress as checkboxes get marked during execution.

### Why This Pattern Works

**Accountability**: Claude can't skip steps - checklist shows exactly what's done

**Transparency**: User sees where Claude is in the process at any moment

**Error Recovery**: If Claude fails at step 4, user knows steps 1-3 succeeded and can debug from there

**Example Progress**:

```markdown
## Execution Status

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked with [NEEDS CLARIFICATION]
- [x] User scenarios defined
- [ ] Functional requirements generated ← Claude currently here
- [ ] Non-functional requirements identified
- [ ] Data entities extracted
- [ ] Review checklist passed
```

---

## 4. Constitutional Reasoning Loop

### Automated Architectural Validation

Templates include **constitutional gates** that trigger Claude's reasoning about architecture principles:

```markdown
## Constitution Check

_GATE: Must pass before Phase 0 research_

### Library-First Gate (Article I)

- [ ] Feature begins as standalone library?
- [ ] Clear library boundaries defined?
- [ ] CLI/API as thin wrapper over library?

### Test-First Gate (Article II)

- [ ] Test structure matches implementation structure?
- [ ] Integration tests planned before code?
```

### Claude's Constitutional Reasoning Process

**Step-by-Step Evaluation**:

1. **Load constitution**: Reads `.specify/memory/constitution.md`
2. **Extract relevant article**: "Article I: Every feature MUST begin as a standalone library"
3. **Analyze current plan**: Does plan start with library creation?
4. **Evaluate checkpoint**:
   - YES → `- [X] Feature begins as standalone library?`
   - NO → `- [ ] Feature begins as standalone library?` + document in Complexity Tracking

5. **If NO, decide on action**:
   - **Option A**: Refactor plan to pass gate (start with library)
   - **Option B**: Justify exception in Complexity Tracking table:
     ```markdown
     | Violation                 | Why Needed                                             | Simpler Alternative Rejected                       |
     | ------------------------- | ------------------------------------------------------ | -------------------------------------------------- |
     | Not starting with library | Feature is CLI-only tool, no library separation needed | Creating library would add unnecessary indirection |
     ```

6. **Report outcome**: "Constitution Check: 3/4 gates passed, 1 exception justified"

### Why Constitutional Reasoning Works

**Explicit Rules**: Constitution provides clear "IF condition THEN action" rules that Claude can evaluate

**Reasoning Capability**: Claude's language understanding handles complex conditional logic and trade-off analysis

**Forced Justification**: Complexity Tracking table prevents silent violations - every exception must be explained

**Example Reasoning**:

```
Claude (internal):
  Article I: "Every feature MUST begin as a standalone library"
  Current plan: Starts with CLI parser implementation
  Evaluation: Does NOT start with library
  Decision: Should I refactor or justify exception?
  Analysis: This is a CLI-only tool, library separation adds indirection
  Action: Document exception with justification
  Result: GATE PASSED (with documented exception)
```

---

## 5. Cascading Context Management

### Progressive Context Building

As the workflow progresses, Claude builds cumulative context across commands:

```
/specify:
  Inputs: User description
  Outputs: spec.md
  Context: Requirements, user stories

/plan:
  Inputs: spec.md + Technical context from user
  Outputs: plan.md, research.md, data-model.md, contracts/
  Context: Requirements + Tech stack + Architecture

/tasks:
  Inputs: plan.md, data-model.md, contracts/
  Outputs: tasks.md
  Context: Requirements + Architecture + Detailed design

/implement:
  Inputs: tasks.md, plan.md, data-model.md, contracts/
  Outputs: Code
  Context: Full workflow history
```

### How Context Cascading Works

**1. Artifact Dependencies**

Each command reads artifacts from previous commands:

```markdown
## Execution Flow (main)

1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Read constitution at `.specify/memory/constitution.md`
3. Fill Technical Context from user arguments
4. Load research findings from previous phase
   → Extract: libraries, patterns, constraints
```

**2. Prerequisite Checks**

Templates validate required context exists:

```markdown
BEFORE proceeding:

- Inspect FEATURE_SPEC for `## Clarifications` section
- If missing or clearly ambiguous areas remain: PAUSE
- Instruct user to run `/clarify` first
```

**3. Cross-Reference System**

Artifacts reference each other for consistency:

```markdown
## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Architecture

[Reference data-model.md entity relationships]

## Testing Strategy

[Reference spec.md user scenarios for integration test cases]
```

### Effect of Context Cascading

**Consistency**: Later commands inherit decisions from earlier stages

**No Re-Explanation**: Claude doesn't need requirements re-stated in `/tasks` - already in `spec.md`

**Validation**: Each stage validates previous stage's completeness before proceeding

**Example Context Flow**:

```
/specify → spec.md contains:
  - FR-001: System MUST support real-time messaging
  - User Scenario: User sends message, recipient sees it within 1 second

/plan → plan.md references spec.md:
  - Architecture Decision: Use WebSockets for real-time (from FR-001)
  - Test Strategy: Measure message delivery time (from user scenario)

/tasks → tasks.md references plan.md:
  - T008: Implement WebSocket connection (from architecture)
  - T015: Add latency measurement test (from test strategy)

/implement → Code references tasks.md:
  - Implements WebSocket handler (from T008)
  - Adds test with 1-second assertion (from T015)
```

---

## 6. Error Handling and Recovery

### Explicit Error Conditions

Templates include specific error handling for failure scenarios:

```markdown
## Execution Flow (main)

1. Run {SCRIPT} from repo root
   → If script fails: ERROR "Script execution failed: {stderr}"
2. Parse JSON for FEATURE_ID
   → If JSON invalid: ERROR "Failed to parse script output"
3. Load spec template from {PATH}
   → If not found: ERROR "Template missing at {path}"
4. Fill template sections
   → If required section empty: ERROR "Incomplete spec generation"
```

### Claude's Error Handling Behavior

**Error Detection and Response**:

1. **Detect error condition**: Step fails with ERROR trigger
2. **Report to user**: Display exact error message with context
3. **Suggest recovery**: Provide specific remediation steps
4. **STOP execution**: Does not proceed to next step with invalid state

**Example Error Flow**:

```
Claude executes: Load spec template from .specify/templates/spec-template.md
Template file missing
Claude detects: "If not found: ERROR"
Claude reports: "ERROR: Template missing at .specify/templates/spec-template.md"
Claude suggests: "Run `speclaude init --here` to reinstall templates"
Claude STOPS: Does not attempt step 4 without valid template
```

### Why Explicit Error Handling Matters

**Prevents Cascading Failures**: If step 2 fails, Claude doesn't attempt step 3 with invalid data

**Actionable Feedback**: User gets specific recovery instructions, not generic "something went wrong"

**State Preservation**: Execution status checklist shows exactly which steps succeeded before failure

**Example Recovery Scenario**:

```markdown
## Execution Status

- [x] User description parsed
- [x] Key concepts extracted
- [ ] Template loaded ← FAILED HERE
- [ ] Sections filled
- [ ] Review completed

ERROR: Template missing at .specify/templates/spec-template.md
RECOVERY: Run `speclaude init --here` to reinstall templates
```

---

## 7. Parallel Execution Awareness

### Dependency-Aware Task Execution

Templates mark parallel-safe operations to optimize execution:

```markdown
## Core Phase

- [ ] T006: Create Message model [P]
- [ ] T007: Create Room model [P]
- [ ] T008: Implement MessageService (depends on T006, T007)
- [ ] T009: Create WebSocket handler [P]
- [ ] T010: Integrate MessageService with WebSocket (depends on T008, T009)
```

### Claude's Interpretation of Markers

**`[P]` marker** = **Parallel-safe** (can run concurrently with other `[P]` tasks)

**No `[P]`** = **Sequential** (depends on previous tasks completing)

### Execution Strategy

**Claude's reasoning**:

```
Analyzing task dependencies:
  T006 [P]: No dependencies, can start immediately
  T007 [P]: No dependencies, can start immediately
  T008: Depends on T006, T007 (mentions Message model, Room model)
  T009 [P]: No dependencies, can start immediately
  T010: Depends on T008, T009 (integrates both components)

Execution plan:
  Phase 1 (parallel): T006, T007, T009
  Phase 2 (sequential): T008 (waits for T006, T007)
  Phase 3 (sequential): T010 (waits for T008, T009)
```

**Execution Flow**:

```
Claude:
  "I can execute T006, T007, and T009 in parallel since they operate on different files.
   T008 must wait for T006 and T007 to complete since MessageService depends on both models.
   T010 must wait for T008 and T009 since it integrates both components."

  [Executes T006, T007, T009 concurrently]
  ✓ T006 complete (Message model created)
  ✓ T007 complete (Room model created)
  ✓ T009 complete (WebSocket handler created)

  [Now executes T008]
  ✓ T008 complete (MessageService implemented)

  [Now executes T010]
  ✓ T010 complete (Integration finished)
```

### Why Parallel Execution Awareness Matters

**Performance**: Reduces total execution time by running independent tasks concurrently

**Safety**: Respects dependencies - never runs dependent tasks before prerequisites complete

**Clarity**: `[P]` marker explicitly communicates task independence to both Claude and users

---

## Cross-References

### Related Template Concepts

- [Templates](06-templates.md) - Detailed template structure and sections
- [Memory System](05-memory-system.md) - Constitution and artifact storage
- [Philosophy](02-philosophy.md) - Why constraint-driven generation works

### Related Workflow Patterns

- [Workflows](10-workflows.md) - Complete end-to-end execution examples
- [Commands](03-commands.md) - Individual command behaviors
- [Error Handling](07-error-handling.md) - Failure scenarios and recovery

### Related AI Concepts

- Constitutional AI principles applied to architecture
- Structured output generation with validation gates
- Context window management across multi-stage workflows
- Hallucination prevention through explicit uncertainty markers

**Navigation**: [← Constitution](08-constitution.md) | [Workflows →](10-workflows.md)

---

## Keywords

templates as instructions, hallucination prevention, execution status checklists, constitutional reasoning, cascading context, error handling, parallel execution, structured thinking, marker-driven clarification, prerequisite validation, dependency analysis, state preservation, progressive context building, execution flow, conditional logic, recovery strategies, concurrent task execution
