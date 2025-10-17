# Commands: Clarification and Analysis

**Purpose**: Guide to enhancement commands that resolve ambiguities and validate consistency
**Target Audience**: Developers refining specifications before implementation
**Related Files**:

- [Commands: Core](04-commands-core.md) - Main workflow commands
- [Templates](06-templates.md) - [NEEDS CLARIFICATION] marker system
- [AI Patterns](09-ai-patterns.md) - How Claude processes clarifications
- [Workflows](10-workflows.md) - When to use clarification commands
  **Keywords**: /clarify, /analyze, /clarify-constitution, ambiguity resolution, validation

---

## Overview

Clarification and analysis commands enhance specification quality by:

- **Resolving ambiguities** through targeted interactive questions
- **Validating consistency** across artifacts (spec, plan, tasks)
- **Detecting coverage gaps** before implementation starts
- **Enforcing constitutional principles** throughout the workflow

All three commands are **optional but recommended** to catch issues early and prevent costly rework during implementation.

---

## Command: /clarify

### Purpose

Interactive ambiguity resolution for feature specifications through targeted questions (maximum 5 per session).

### When to Use

**Workflow Position**: After `/specify`, before `/plan`

**Use Cases**:

- Initial spec contains vague requirements ("fast", "scalable", "secure")
- `[NEEDS CLARIFICATION]` markers exist in spec
- Non-functional requirements lack measurable criteria
- Edge cases underspecified
- Terminology inconsistencies detected

**Skip If**: Specification is complete with measurable outcomes and no ambiguity markers.

---

### Inputs and Prerequisites

**Required**:

- `specs/###-feature-name/spec.md` with potential ambiguities

**Optional Context**:

- `.specify/memory/constitution.md` for principle alignment
- Previous clarification sessions metadata

**Detection Mechanism**: Automatically scans spec for:

- Vague adjectives without metrics
- `[NEEDS CLARIFICATION]` markers
- Missing acceptance criteria
- Undefined entities or behaviors
- Terminology variations

---

### The 10 Taxonomy Categories

Clarification questions are systematically generated across these categories:

#### 1. Functional Requirements Scope

**Detects**: Missing capabilities, unclear feature boundaries
**Example Question**: "Should users be able to edit sent messages?"

#### 2. Data Model Structure

**Detects**: Undefined entities, missing relationships, unclear types
**Example Question**: "What fields should the User entity contain (email, username, display name)?"

#### 3. Access Control & Permissions

**Detects**: Authorization gaps, role ambiguities
**Example Question**: "Who can delete messages: only sender, room admin, or any user?"

#### 4. Interaction & UX Flow

**Detects**: Undefined navigation, missing UI states
**Example Question**: "What happens when a user sends a message while offline?"

#### 5. Non-Functional Quality Attributes

**Detects**: Vague performance/security/reliability requirements
**Example Question**: "What is the expected message delivery latency target?"

#### 6. Integration & External Dependencies

**Detects**: Undefined external services, unclear protocols
**Example Question**: "Should the system integrate with existing authentication (OAuth) or use local accounts?"

#### 7. Edge Cases & Failure Handling

**Detects**: Missing error scenarios, undefined recovery behavior
**Example Question**: "What happens if message storage is full?"

#### 8. Constraints & Tradeoffs

**Detects**: Conflicting requirements, missing limits
**Example Question**: "What is the maximum message length (characters or bytes)?"

#### 9. Terminology & Consistency

**Detects**: Same concept with multiple names
**Example Question**: "Should we use 'Room', 'Channel', or 'Conversation' consistently?"

#### 10. Completion Signals / Misc Placeholders

**Detects**: TODO markers, placeholder text, unresolved notes
**Example Question**: "What format should timestamps use (ISO8601, Unix epoch, or relative)?"

---

### Interactive Process Flow

**Step 1: Analysis Phase**

```
Claude:
  Loading spec.md...
  ✓ Parsed 12 requirements
  ✓ Detected 8 potential ambiguities

  Prioritizing across 10 taxonomy categories...
  ✓ Generated 5 clarification questions

  Starting interactive session (max 5 questions)...
```

**Step 2: Sequential Questions** (one at a time)

```
Claude:
  Q1 [Category: Non-Functional Quality Attributes]
  What is the expected message delivery latency target?

  | Option | Description |
  |--------|-------------|
  | A      | < 100ms (real-time chat) |
  | B      | < 1s (near real-time) |
  | C      | < 5s (delayed messaging) |

User: A

Claude: ✓ Integrated into NFR-001: "Message delivery < 100ms p95 latency"
        ✓ Updated spec.md (saved)
```

```
Claude:
  Q2 [Category: Data Model Structure]
  How long should message history be retained?
  Format: Short answer (≤5 words)

User: 30 days

Claude: ✓ Integrated into FR-007: "Retain messages for 30 days"
        ✓ Updated spec.md (saved)
```

```
Claude:
  Q3 [Category: Edge Cases & Failure Handling]
  What happens if a user sends a message while offline?

  | Option | Description |
  |--------|-------------|
  | A      | Queue locally, send when reconnected |
  | B      | Show error immediately |
  | C      | Not supported (must be online) |

User: A

Claude: ✓ Added Edge Case EC-003: "Offline message queuing with retry"
        ✓ Updated spec.md (saved)
```

**Step 3: Early Termination** (optional)

```
User: done

Claude: Clarification session ended early.
        - 3/5 questions answered
        - 3 sections updated
        - 2 questions deferred
```

**Step 4: Completion Summary**

```
Claude:
  Clarification Session Complete!

  Coverage Report:
  | Category | Status | Questions | Resolved |
  |----------|--------|-----------|----------|
  | Functional Requirements | ✓ Clear | 0 | — |
  | Data Model | ✓ Resolved | 1 | Yes |
  | Access Control | Deferred | 0 | — |
  | Interaction & UX | ✓ Clear | 0 | — |
  | Non-Functional | ✓ Resolved | 1 | Yes |
  | Integration | ✓ Clear | 0 | — |
  | Edge Cases | ✓ Resolved | 1 | Yes |
  | Constraints | Deferred | 1 | No |
  | Terminology | ✓ Clear | 0 | — |
  | Completion Signals | ✓ Clear | 0 | — |

  Summary:
  - 5 questions answered
  - 5 spec sections updated
  - Coverage: 8/10 categories clear or resolved
  - 2 categories deferred (low impact)

  Recommendation: Proceed to /plan
```

---

### Outputs

**Updated spec.md**:

- Integrated clarifications into appropriate sections
- New measurable criteria added
- Edge cases documented
- Terminology normalized

**New Section Added**:

```markdown
## Clarifications

### Session 2025-10-17

**Questions Answered**: 5
**Categories Covered**: Non-Functional, Data Model, Edge Cases, Constraints, Terminology

Q1: Message delivery latency target
A1: < 100ms p95 latency → Integrated into NFR-001

Q2: Message history retention
A2: 30 days → Integrated into FR-007

[... additional Q&A pairs ...]
```

**Coverage Summary Table**:
Shows which taxonomy categories have been resolved vs outstanding.

**Recommendation**:

- "Proceed to /plan" if critical ambiguities resolved
- "Re-run /clarify" if high-impact gaps remain

---

### Key Features

**Maximum 5 Questions**: Prevents analysis paralysis, focuses on highest-impact ambiguities

**Incremental Integration**: Saves spec after each answer to prevent context loss

**Interactive Not Batch**: One question at a time for better user engagement

**Taxonomy-Driven**: Systematic coverage across 10 ambiguity categories ensures comprehensive resolution

**Atomic Updates**: Each answer immediately modifies spec and saves (referentially transparent)

**Early Termination**: User can type "done" to skip remaining questions

---

## Command: /analyze

### Purpose

Non-destructive cross-artifact consistency analysis to catch issues before implementation begins.

### When to Use

**Workflow Position**: After `/tasks`, before `/implement`

**Use Cases**:

- Validate requirements mapped to tasks
- Detect conflicting specifications
- Check constitutional principle compliance
- Identify coverage gaps early
- Verify terminology consistency

**Skip If**: Small feature with <10 tasks and high confidence in artifact alignment.

---

### Inputs and Prerequisites

**Required**:

- `spec.md` with requirements and user stories
- `plan.md` with architecture and tech stack
- `tasks.md` with task breakdown

**Optional**:

- `.specify/memory/constitution.md` for principle validation

---

### Detection Passes (6 Categories)

#### A. Duplication Detection

**Finds**: Near-duplicate requirements, redundant user stories

**Example**:

```
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| D1 | Duplication | HIGH | spec.md:L120-134, L145-152 | Two similar requirements for file upload |
```

**Recommendation**: "Merge into single FR with clear scope"

---

#### B. Ambiguity Detection

**Finds**: Vague adjectives (fast, scalable, secure) without metrics, unresolved placeholders

**Example**:

```
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| A1 | Ambiguity | HIGH | spec.md:L89 | "Fast response time" lacks metric |
```

**Recommendation**: "Specify latency target (e.g., <200ms p95)"

---

#### C. Underspecification

**Finds**: Requirements with verbs but missing outcomes, user stories without acceptance criteria, tasks referencing undefined files

**Example**:

```
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| U1 | Underspecification | MEDIUM | tasks.md T012 | Task references 'MessageQueue' undefined in plan |
```

**Recommendation**: "Add MessageQueue to data-model.md or clarify as external"

---

#### D. Constitution Alignment

**Finds**: Violations of MUST principles, missing mandated sections

**Example**:

```
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| CA1 | Constitution | CRITICAL | plan.md Phase 2 | Violates Test-First (Principle III) - implementation tasks before contract tests |
```

**Recommendation**: "Reorder tasks to ensure contract tests (T005) before implementation (T010)"

---

#### E. Coverage Gaps

**Finds**: Requirements with zero tasks, tasks with no mapped requirement/story, NFRs not reflected

**Example**:

```
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| C1 | Coverage | CRITICAL | spec.md FR-008 | Message encryption requirement has zero tasks |
```

**Recommendation**: "Add Task T021: Implement message encryption (addresses FR-008)"

---

#### F. Inconsistency

**Finds**: Terminology drift, data entities in plan absent in spec, task ordering contradictions, conflicting requirements

**Example**:

```
| ID | Category | Severity | Location(s) | Summary |
|----|----------|----------|-------------|---------|
| F1 | Inconsistency | MEDIUM | spec.md vs plan.md | Spec says "User" entity, plan says "Account" |
```

**Recommendation**: "Normalize terminology to 'User' across both artifacts"

---

### Severity Assignment Rules

**CRITICAL**:

- Violates constitution MUST principles
- Missing core artifact
- Zero coverage blocking baseline functionality

**HIGH**:

- Duplicate/conflicting requirements
- Ambiguous security/performance criteria
- Untestable acceptance criterion

**MEDIUM**:

- Terminology drift
- Missing NFR task coverage
- Underspecified edge case

**LOW**:

- Style/wording improvements
- Minor redundancy

---

### Analysis Report Format

```markdown
### Specification Analysis Report

| ID  | Category      | Severity | Location(s)                | Summary                                       | Recommendation                            |
| --- | ------------- | -------- | -------------------------- | --------------------------------------------- | ----------------------------------------- |
| D1  | Duplication   | HIGH     | spec.md:L120-134, L145-152 | Two similar requirements for file upload      | Merge into single FR with clear scope     |
| A1  | Ambiguity     | HIGH     | spec.md:L89                | "Fast response time" lacks metric             | Specify latency target (e.g., <200ms p95) |
| C1  | Coverage      | CRITICAL | spec.md FR-008             | Message encryption requirement has zero tasks | Add task for encryption implementation    |
| F1  | Inconsistency | MEDIUM   | spec.md vs plan.md         | Spec says "User" entity, plan says "Account"  | Normalize terminology to "User"           |

#### Coverage Summary

| Requirement Key       | Has Task? | Task IDs   | Notes                |
| --------------------- | --------- | ---------- | -------------------- |
| user-can-send-message | ✓         | T010, T015 | Covered              |
| message-encryption    | ✗         | —          | **Missing coverage** |
| real-time-delivery    | ✓         | T012, T014 | Covered              |

#### Constitution Alignment Issues

- **CRITICAL**: Plan violates Test-First principle (Principle III) - implementation tasks before contract tests

#### Metrics

- Total Requirements: 25
- Total Tasks: 20
- Coverage: 84% (21/25 requirements have ≥1 task)
- Ambiguity Count: 3
- Duplication Count: 2
- Critical Issues: 2

### Next Actions

- **CRITICAL issues exist**: Resolve before `/implement`
- Add Task T021: Implement message encryption (addresses FR-008)
- Reorder tasks to ensure contract tests before implementation
- Run `/plan` to normalize terminology drift

Would you like me to suggest concrete remediation edits for the top 5 issues?
```

---

### Outputs

**Structured Markdown Report**:

- Findings table with severity-sorted issues
- Coverage summary with unmapped requirements/tasks
- Constitution alignment validation results
- Metrics (totals, percentages, issue counts)

**Next Actions Section**:

- Explicit prioritization (CRITICAL first)
- Concrete remediation steps
- Command recommendations

**Interactive Offer**:

- Asks before suggesting edits (never modifies automatically)

---

### Key Features

**Strictly Read-Only**: Never modifies files - analysis only

**Deterministic**: Re-running without changes produces consistent IDs/counts

**Constitution Authority**: Treats constitution MUST principles as non-negotiable

**Limits Findings to 50**: Aggregates remainder to prevent overwhelming output

**Asks Before Remediation**: Offers to suggest fixes but never applies automatically

---

## Command: /clarify-constitution

### Purpose

Resolve `[NEEDS CLARIFICATION]` markers in constitution through targeted questions.

### When to Use

**Workflow Position**: After `/constitution` if markers exist

**Use Cases**:

- Constitution contains ambiguous principles
- Team has not defined critical governance rules
- Project-specific constraints need documentation
- Technology preferences unclear

**Skip If**: Constitution has no `[NEEDS CLARIFICATION]` markers.

---

### Inputs and Prerequisites

**Required**:

- `.specify/memory/constitution.md` with `[NEEDS CLARIFICATION]` markers

**Metadata**:

- Session counter: `<!-- Clarification Sessions: N -->`

---

### Process Flow

**Step 1: Parse Constitution**

```
Claude:
  Loading constitution...
  ✓ Parsed 5 principles
  ✓ Found 3 [NEEDS CLARIFICATION] markers

  Generating targeted questions...
```

**Step 2: Sequential Interactive Loop** (same as `/clarify`)

- Maximum 5 questions per session
- One question at a time
- User answers or types "done"
- Immediate integration into constitution
- Save after each answer

**Step 3: Update Metadata**

```markdown
<!-- Clarification Sessions: 3 -->
<!-- Last Session: 2025-10-17 -->
```

**Step 4: Remove Resolved Markers**

- `[NEEDS CLARIFICATION]` removed where answers provided
- Remaining markers stay for future sessions

---

### Example Session

```
User: /clarify-constitution

Claude:
  Q1 [Principle II: CLI Interface]
  Should CLI commands accept JSON input for automation?

  | Option | Description |
  |--------|-------------|
  | A      | Yes, all commands support --json flag |
  | B      | Only read commands (no write) |
  | C      | No, interactive only |

User: A

Claude: ✓ Updated Principle II: "All commands MUST support --json flag"
        ✓ Removed [NEEDS CLARIFICATION] marker
        ✓ Saved constitution
```

---

### Outputs

**Updated constitution.md**:

- Resolved markers integrated into principle sections
- `[NEEDS CLARIFICATION]` removed where answered
- Incremented session counter

**Coverage Report**:

```
Clarification Session Complete!
- 3 questions answered
- 3 principles updated
- 3 markers resolved
- 0 markers outstanding

Constitution is now complete. Proceed to /specify.
```

---

### Key Features

**Constitution-Specific**: Focuses on governance principles rather than feature requirements

**Same Interactive Flow**: Maximum 5 questions, one at a time, incremental saves

**Session Tracking**: Metadata shows clarification history

**Marker Management**: Automatically removes resolved markers, preserves outstanding ones

---

## Cross-References

### Related Ambiguity Resolution Patterns

- **[Templates](06-templates.md)**: `[NEEDS CLARIFICATION]` marker syntax and usage
- **[AI Patterns](09-ai-patterns.md)**: How Claude generates and prioritizes questions
- **[Workflows](10-workflows.md)**: When to run clarification vs analysis

### Related Validation Mechanisms

- **[Commands: Core](04-commands-core.md)**: `/plan` constitutional gates
- **[Templates](06-templates.md)**: Coverage tracking templates
- **[Workflows](10-workflows.md)**: Quality gates and checkpoints

### Related Context Management

- **[Context Files](07-context-files.md)**: How constitution principles propagate
- **[Scripts](08-scripts.md)**: `check-prerequisites.sh` validation logic

---

**Navigation**: [← Commands: Core](04-commands-core.md) | [Templates →](06-templates.md)

---

## Keywords

clarification, ambiguity resolution, validation, consistency analysis, /clarify, /analyze, /clarify-constitution, taxonomy categories, interactive questions, coverage gaps, constitutional compliance, duplication detection, terminology normalization, specification refinement, quality gates
