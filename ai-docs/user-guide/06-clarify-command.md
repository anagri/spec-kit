# Page 06: /clarify - Specification Clarification

**Status**: Stable
**Command**: `/clarify`
**Workflow Position**: After `/specify`, before `/plan` (optional but highly recommended)
**Related Pages**: [05: /specify Command](05-specify-command.md) | [07: /plan Command](07-plan-command.md)

---

## Overview

The `/clarify` command resolves ambiguities in your feature specification through an interactive question-and-answer session. After running `/specify`, your spec may contain `[NEEDS CLARIFICATION]` markers or vague requirements. This command identifies those gaps, asks up to 5 targeted questions, and integrates your answers directly into the specification.

**Key Benefits**:
- Reduces rework during implementation by resolving ambiguities upfront
- Forces explicit decisions on critical architectural choices (auth, data, scale)
- Provides measurable criteria instead of vague adjectives ("fast", "secure")
- Saves spec after each answer to prevent context loss

---

## When to Use

### Recommended Situations

Use `/clarify` after `/specify` and before `/plan` when:

- Your spec contains `[NEEDS CLARIFICATION]` markers
- Requirements use vague adjectives without metrics ("fast", "scalable", "secure")
- Non-functional requirements lack measurable targets
- Edge cases are underspecified or missing
- Terminology is inconsistent across the spec
- You want to ensure planning starts with complete requirements

### Skip If

- Specification is already complete with measurable outcomes
- All requirements are testable and unambiguous
- You're doing an exploratory spike and want to iterate quickly
- Feature is trivial with obvious requirements (e.g., "add a constant to config")

**Warning**: Skipping `/clarify` when ambiguities exist increases rework risk during `/plan` and `/implement`.

---

## How It Works

### Step 1: Ambiguity Scan

When you run `/clarify` (no arguments needed), Claude:

1. Loads your `spec.md`
2. Scans for ambiguities across 10 taxonomy categories
3. Generates up to 5 prioritized questions based on impact
4. Presents questions one at a time (never in batch)

### Step 2: Interactive Question Loop

For each question, Claude:

- Presents **ONE question at a time** (sequential, not batch)
- Provides answer format:
  - **Multiple choice table** with 2-5 options, OR
  - **Short answer** (5 words maximum)
- Waits for your response
- Integrates answer immediately into the relevant spec section
- **Saves spec.md** after each integration (atomic updates)
- Proceeds to next question (or stops if you say "done")

### Step 3: Coverage Report

After the session (5 questions answered OR early termination), Claude provides:

- Number of questions answered
- Sections updated with line references
- Coverage summary table showing taxonomy category status
- Recommendation: proceed to `/plan` or re-run `/clarify`

---

## The 10 Taxonomy Categories

Claude systematically scans your spec across these categories to identify ambiguities:

### 1. Functional Scope & Behavior

**Detects**: Missing capabilities, unclear feature boundaries, undefined user roles

**Example Question**:
```
Should users be able to edit sent messages?

| Option | Description |
|--------|-------------|
| A      | Yes, within 5 minutes of sending |
| B      | Yes, unlimited edit history |
| C      | No, messages are immutable |
```

---

### 2. Domain & Data Model

**Detects**: Undefined entities, missing relationships, unclear types, data volume assumptions

**Example Question**:
```
How long should message history be retained?
Format: Short answer (≤5 words)

User Answer: "30 days then archive"
```

---

### 3. Interaction & UX Flow

**Detects**: Undefined navigation, missing UI states (loading, error, empty), unclear user journeys

**Example Question**:
```
What happens when a user sends a message while offline?

| Option | Description |
|--------|-------------|
| A      | Queue locally, send when reconnected |
| B      | Show error immediately |
| C      | Not supported (must be online) |
```

---

### 4. Non-Functional Quality Attributes

**Detects**: Vague performance/scalability/reliability/security requirements lacking metrics

**Example Question**:
```
What is the expected message delivery latency target?

| Option | Description |
|--------|-------------|
| A      | < 100ms (real-time chat experience) |
| B      | < 1s (near real-time, slight delay acceptable) |
| C      | < 5s (delayed messaging, not real-time) |
```

**Impact**: High. This category often has the biggest influence on architecture and implementation.

---

### 5. Integration & External Dependencies

**Detects**: Undefined external services, unclear protocols, missing failure modes

**Example Question**:
```
What authentication method should be used?

| Option | Description |
|--------|-------------|
| A      | Email/password with JWT tokens |
| B      | OAuth2 (Google, GitHub) |
| C      | Single Sign-On (SSO) via SAML |
```

---

### 6. Edge Cases & Failure Handling

**Detects**: Missing error scenarios, undefined recovery behavior, unclear rate limiting

**Example Question**:
```
What happens if message storage is full?
Format: Short answer (≤5 words)

User Answer: "Reject new messages gracefully"
```

---

### 7. Constraints & Tradeoffs

**Detects**: Conflicting requirements, missing limits, undefined resource constraints

**Example Question**:
```
What is the maximum message length?

| Option | Description |
|--------|-------------|
| A      | 280 characters (Twitter-style) |
| B      | 2000 characters (Slack-style) |
| C      | 65536 characters (unlimited) |
```

---

### 8. Terminology & Consistency

**Detects**: Same concept with multiple names, conflicting glossary terms

**Example Question**:
```
Should we use "Room", "Channel", or "Conversation" consistently?
Format: Short answer (≤5 words)

User Answer: "Room"
```

**Action**: Claude normalizes terminology across entire spec after this answer.

---

### 9. Completion Signals

**Detects**: TODO markers, placeholder text, untestable acceptance criteria

**Example Question**:
```
What format should timestamps use?

| Option | Description |
|--------|-------------|
| A      | ISO8601 (2025-10-17T14:23:00Z) |
| B      | Unix epoch (milliseconds since 1970) |
| C      | Relative (2 hours ago, 3 days ago) |
```

---

### 10. Misc / Placeholders

**Detects**: Unresolved decisions, ambiguous adjectives lacking quantification

**Example Question**:
```
Define "scalable" for this feature.
Format: Short answer (≤5 words)

User Answer: "1000 concurrent users"
```

---

## Example Interaction

Here's a complete example showing the interactive flow:

### Running the Command

```
User: /clarify
```

### Claude's Analysis Phase

```
Claude:
  Loading spec.md...
  ✓ Parsed 12 requirements
  ✓ Detected 8 potential ambiguities

  Prioritizing across 10 taxonomy categories...
  ✓ Generated 5 clarification questions

  Starting interactive session (max 5 questions)...
```

### Question 1: Multiple Choice Table

```
Claude:
  Q1 [Category: Non-Functional Quality Attributes]
  What is the expected message delivery latency target?

  | Option | Description |
  |--------|-------------|
  | A      | < 100ms (real-time chat experience) |
  | B      | < 1s (near real-time, slight delay acceptable) |
  | C      | < 5s (delayed messaging, not real-time) |

User: A

Claude:
  ✓ Integrated into FR-001: "System MUST deliver messages with <100ms p95 latency"
  ✓ Updated spec.md (saved)
```

### Question 2: Short Answer

```
Claude:
  Q2 [Category: Data Model Structure]
  How long should message history be retained?
  Format: Short answer (≤5 words)

User: 30 days then archive

Claude:
  ✓ Integrated into FR-003: "Messages retained for 30 days, then archived"
  ✓ Updated spec.md (saved)
```

### Question 3: Another Multiple Choice

```
Claude:
  Q3 [Category: Integration & External Dependencies]
  What authentication method should be used?

  | Option | Description |
  |--------|-------------|
  | A      | Email/password with JWT tokens |
  | B      | OAuth2 (Google, GitHub) |
  | C      | Single Sign-On (SSO) via SAML |

User: B

Claude:
  ✓ Integrated into FR-006: "Authentication via OAuth2 (Google, GitHub providers)"
  ✓ Updated spec.md (saved)
```

### Early Termination (Optional)

```
User: done

Claude:
  Clarification session ended early.
  - 3/5 questions answered
  - 3 sections updated
  - 2 questions deferred
```

### Completion Summary

```
Claude:
  Clarification Session Complete!

  Coverage Report:
  | Category                 | Status      | Questions | Resolved |
  |--------------------------|-------------|-----------|----------|
  | Functional Requirements  | ✓ Clear     | 0         | —        |
  | Data Model               | ✓ Resolved  | 1         | Yes      |
  | Access Control           | Deferred    | 0         | —        |
  | Interaction & UX         | ✓ Clear     | 0         | —        |
  | Non-Functional           | ✓ Resolved  | 1         | Yes      |
  | Integration              | ✓ Resolved  | 1         | Yes      |
  | Edge Cases               | ✓ Clear     | 0         | —        |
  | Constraints              | Deferred    | 1         | No       |
  | Terminology              | ✓ Clear     | 0         | —        |
  | Completion Signals       | ✓ Clear     | 0         | —        |

  Summary:
  - 3 questions answered
  - 3 spec sections updated
  - Coverage: 7/10 categories clear or resolved
  - 3 categories deferred (low impact)

  Recommendation: Proceed to /plan
```

---

## Spec.md Changes

After clarification, Claude adds a new section to your spec:

```markdown
## Clarifications

### Session 2025-10-17

- Q: Message delivery latency target → A: < 100ms p95 latency
- Q: Message history retention → A: 30 days then archive
- Q: Authentication method → A: OAuth2 (Google, GitHub providers)
```

And updates relevant sections with specific criteria:

**Before**:
```markdown
- FR-001: System MUST deliver messages quickly
```

**After**:
```markdown
- FR-001: System MUST deliver messages with <100ms p95 latency
```

---

## Key Features

### Maximum 5 Questions Rule

To prevent analysis paralysis, `/clarify` asks at most 5 questions per session. Questions are prioritized by:

- **Impact**: Does the answer materially affect architecture, data modeling, or testing?
- **Uncertainty**: How ambiguous is the current requirement?
- **Category Coverage**: Attempt to cover highest-impact categories first

If more than 5 ambiguities exist, Claude selects the top 5 by (Impact × Uncertainty) heuristic.

### Incremental Integration (Atomic Updates)

Each answer is:

1. Integrated into the most appropriate spec section
2. **Saved immediately** to `spec.md`
3. Reported to user with line reference

This prevents context loss if the session is interrupted and ensures transparency.

### Interactive, Not Batch

Questions are presented **one at a time**, not all at once. This:

- Improves user engagement
- Allows early termination ("done" command)
- Prevents overwhelming the user with too many decisions at once

### Taxonomy-Driven Systematic Coverage

By scanning across 10 predefined categories, `/clarify` ensures comprehensive ambiguity detection rather than ad-hoc questioning.

---

## All Possible Outcomes

### Outcome 1: All Clarified

```
Claude:
  - 5 questions answered
  - 5 sections updated
  - Coverage: 10/10 categories resolved
  - No outstanding ambiguities

  Recommendation: Proceed to /plan
```

**Next Action**: `/plan`

---

### Outcome 2: Partial Clarification

```
Claude:
  - 3 questions answered
  - 3 sections updated
  - Coverage: 7/10 categories resolved
  - 3 categories deferred (low impact)

  Recommendation: Proceed to /plan (deferred items unlikely to block implementation)
```

**Next Action**: `/plan` (acceptable to proceed with low-impact gaps)

---

### Outcome 3: Early Termination

```
User: done

Claude:
  Clarification session ended early.
  - 2/5 questions answered
  - 2 sections updated
  - 3 questions not asked

  Recommendation: Re-run /clarify or proceed to /plan with caution
```

**Next Action**: Either `/clarify` again (to answer remaining questions) or `/plan` (accepting risk)

---

### Outcome 4: No Ambiguities Detected

```
Claude:
  Loading spec.md...
  ✓ Performed ambiguity scan

  No critical ambiguities detected worth formal clarification.
  All requirements appear testable and measurable.

  Recommendation: Proceed to /plan
```

**Next Action**: `/plan`

---

### Outcome 5: Error - Missing Spec

```
Claude:
  Error: Missing prerequisite file spec.md
  Run /specify first to create specification.
```

**Next Action**: `/specify`

---

## Best Practices

### 1. Answer All 5 Questions (Don't Terminate Early)

**Why**: Clarifications are high-leverage. Answering 5 questions takes ~5 minutes but can save hours of rework during implementation.

**Avoid**: Typing "done" after 2 questions unless you're certain remaining questions are low-impact.

---

### 2. Provide Metrics, Not Adjectives

**Good Answers**:
- "< 100ms p95 latency"
- "1000 concurrent users"
- "30 days retention"
- "5 retry attempts with exponential backoff"

**Bad Answers**:
- "fast"
- "scalable"
- "reasonable"
- "as needed"

**Why**: Measurable criteria enable testable requirements and clear success criteria.

---

### 3. Resolve Auth/Data/Scale Early (High-Impact Categories)

Categories 2, 4, and 5 (Data Model, Non-Functional, Integration) typically have the biggest architectural impact. Prioritize answering questions in these categories.

**Example High-Impact Questions**:
- Authentication method (OAuth2 vs email/password)
- Message retention policy (affects storage design)
- Latency targets (affects WebSocket vs polling decision)

---

### 4. Be Specific About Integrations

**Good Answer**: "OAuth2 with Google and GitHub providers"
**Bad Answer**: "Social login"

**Why**: Specificity enables Claude to generate accurate contracts and integration tests during `/plan`.

---

### 5. If You Don't Know, Say So

If you genuinely don't know the answer, respond with:

```
User: I need to research this first

Claude: Understood. Marking this as deferred.
```

You can re-run `/clarify` after research or proceed to `/plan` and update spec manually.

---

## Importance in the Workflow

### Reduces Rework Risk

**Without /clarify**:
```
/specify → /plan (guesses latency target) → /tasks → /implement
[Later: User realizes latency target was wrong]
→ Must regenerate plan and tasks
```

**With /clarify**:
```
/specify → /clarify (explicitly sets latency target) → /plan → /tasks → /implement
[No rework needed]
```

---

### Enforces Explicit Decisions

`[NEEDS CLARIFICATION]` markers prevent Claude from hallucinating details during `/plan`. Instead of guessing "probably OAuth2", Claude waits for your explicit decision.

---

### Enables Better Planning

When `/plan` receives a spec with measurable criteria:
- Architecture decisions are more informed (WebSocket vs polling based on latency)
- Contract tests can be generated with specific assertions (<100ms)
- Task estimates are more accurate

---

## Common Issues

### Issue 1: Early Termination Leaving Critical Gaps

**Symptom**: You type "done" after 2 questions, but Question 3 was about authentication method (high-impact).

**Fix**: Re-run `/clarify` to answer remaining questions, or manually update spec.md with authentication details.

**Prevention**: Answer all 5 questions unless you're certain remaining ones are low-impact.

---

### Issue 2: Vague Answers Requiring Re-Clarification

**Symptom**:
```
Claude: What is the expected latency target?
User: Fast

Claude: Can you be more specific? (e.g., <100ms, <1s, <5s)
```

**Fix**: Provide measurable criteria (see Best Practice 2).

**Prevention**: Use numbers with units (ms, req/s, GB, days) whenever possible.

---

### Issue 3: Skipping /clarify Entirely

**Symptom**: You run `/specify` → `/plan` directly, and `/plan` creates architecture based on assumptions.

**Risk**: Assumptions may be wrong, requiring plan regeneration.

**Fix**: If you notice assumptions during `/plan`, stop and run `/clarify` to resolve them, then re-run `/plan`.

**Prevention**: Always run `/clarify` when spec contains `[NEEDS CLARIFICATION]` markers.

---

## Command Reference

### Syntax

```
/clarify
```

**No arguments required** - Claude automatically loads `spec.md` from current feature directory.

### Prerequisites

- `specs/###-feature-name/spec.md` must exist (created by `/specify`)

### Outputs

- **Updated `spec.md`**: Integrated clarifications in relevant sections
- **New Section**: `## Clarifications` with session timestamp and Q&A log
- **Coverage Report**: Taxonomy category status table

### Environment Variables

None. Context is automatically detected via `check-prerequisites.sh`.

---

## Follow-Up Actions

After `/clarify`, you typically proceed to:

```
/plan "Tech stack and architecture details"
```

If critical gaps remain after clarification, consider:

- **Re-running `/clarify`**: To answer deferred questions
- **Manually editing `spec.md`**: To add missing details
- **Proceeding with `/plan`**: If gaps are low-impact and won't block implementation

---

## References

- **Template Source**: `templates/commands/clarify.md` (execution flow pseudocode)
- **Related KB Articles**:
  - [KB 05: Commands - Clarification](../kb/05-commands-clarify.md) - Technical implementation details
  - [KB 09: AI Patterns](../kb/09-ai-patterns.md) - How Claude processes clarifications
  - [KB 10: Workflows](../kb/10-workflows.md) - Real-world examples with /clarify
- **Related User Guide Pages**:
  - [05: /specify Command](05-specify-command.md) - Creating the initial spec
  - [07: /plan Command](07-plan-command.md) - Using clarified spec for planning

---

**Next**: [Page 07: /plan Command](07-plan-command.md)
**Previous**: [Page 05: /specify Command](05-specify-command.md)
**Index**: [User Guide Index](00-index.md)
