# Page 04: /clarify-constitution - Governance Clarification

**Purpose**: Resolve ambiguous governance principles before feature development
**When to Use**: After `/constitution` if `[NEEDS CLARIFICATION]` markers exist
**Time Estimate**: 5-15 minutes (maximum 5 questions)
**Next Command**: `/specify` (start feature development)

---

## What is /clarify-constitution?

The `/clarify-constitution` command resolves ambiguous governance principles in your project constitution through **interactive question-and-answer sessions**. Unlike `/clarify` which refines feature specifications, this command focuses on **project-wide architectural decisions** that affect all features.

**Key Characteristics**:
- **Optional but important**: Only needed when constitution contains `[NEEDS CLARIFICATION]` markers
- **Interactive not batch**: Asks one question at a time, saves immediately after each answer
- **Maximum 5 questions**: Prevents analysis paralysis, focuses on highest-impact ambiguities
- **Atomic saves**: Each answer integrated and saved before next question (prevents context loss)
- **Early termination**: Type "done", "stop", or "proceed" to skip remaining questions

---

## When to Use This Command

### Workflow Position

```
/constitution → [/clarify-constitution if markers exist] → /specify
```

**Run /clarify-constitution when**:
- You just ran `/constitution` and see: "⚠ Clarifications needed (3)"
- Constitution file contains `[NEEDS CLARIFICATION]` markers
- You want to prevent ambiguous governance from blocking future `/plan` gates

**Skip /clarify-constitution when**:
- No `[NEEDS CLARIFICATION]` markers found
- Constitution is complete with concrete principles
- You prefer to manually edit `.specify/memory/constitution.md` directly

---

## Why Governance Clarification Matters

Ambiguous constitutional principles cause problems downstream:

**Problem**: Constitution says "Use modern database" `[NEEDS CLARIFICATION]`
**Impact**: `/plan` gate fails because "modern" is vague - PostgreSQL? MongoDB? Redis?

**Problem**: Principle says "Test-first development" `[NEEDS CLARIFICATION: unit or integration?]`
**Impact**: Task ordering unclear - when to write which tests?

**Solution**: `/clarify-constitution` asks targeted questions to resolve ambiguities **before** they block feature development.

---

## Interactive Q&A Flow

### Step 1: Loading and Scanning

```
User: /clarify-constitution

Claude:
  Loading constitution from .specify/memory/constitution.md...
  ✓ Parsed 5 principles
  ✓ Found 3 [NEEDS CLARIFICATION] markers

  Scanning for ambiguities across 4 categories:
  - Architectural Principles: 1 marker
  - Technology Constraints: 1 marker
  - Development Workflow: 0 markers
  - Governance Policies: 1 marker

  Generating targeted questions (maximum 5)...
  ✓ Prioritized 3 questions by impact

  Starting interactive session...
```

**What Happens**:
- Constitution file loaded once at session start
- Automatic scan detects `[NEEDS CLARIFICATION]` markers
- Questions prioritized across 4 constitution-specific categories
- Maximum 5 questions per session (prevents fatigue)

---

### Step 2: Question 1 - Multiple Choice Format

```
Claude:
  Q1 [Category: Technology Constraints]
  Which database should be used for primary data storage?

  | Option | Description |
  |--------|-------------|
  | A      | PostgreSQL 15+ (relational, ACID guarantees) |
  | B      | MongoDB 6+ (document store, flexible schema) |
  | C      | Redis 7+ (in-memory, key-value) |
  | Short  | Provide a different short answer (≤5 words) |

User: A

Claude:
  ✓ Integrated into Principle II (Technology Constraints)
  ✓ Replaced marker with: "PostgreSQL 15+ for primary storage"
  ✓ Saved constitution

  [Moves to next question immediately]
```

**Key Features**:
- **Table format**: Clear presentation of 2-5 options
- **Descriptions**: Each option explains implications
- **Short answer option**: Available if predefined choices don't fit
- **Immediate integration**: Answer saved before moving to next question

---

### Step 3: Question 2 - Short Answer Format

```
Claude:
  Q2 [Category: Governance Policies]
  How often should the constitution be reviewed for updates?
  Format: Short answer (≤5 words)

User: Quarterly or major changes

Claude:
  ✓ Integrated into Principle VI (Amendment Process)
  ✓ Replaced marker with: "Review quarterly or on major project changes"
  ✓ Saved constitution

  [Moves to next question]
```

**Key Features**:
- **5-word limit**: Forces concise, concrete answers
- **No options**: Used when choices are too varied for multiple-choice
- **Specific constraint**: Prevents vague responses like "regularly" or "sometimes"

---

### Step 4: Question 3 - Architectural Principles

```
Claude:
  Q3 [Category: Architectural Principles]
  What is the primary architectural style for this project?

  | Option | Description |
  |--------|-------------|
  | A      | Library-first (every feature starts as standalone library) |
  | B      | Microservices (distributed services with API contracts) |
  | C      | Monolith (single deployable application) |

User: A

Claude:
  ✓ Integrated into Principle I (Core Architecture)
  ✓ Added rationale: "Enables reusability, testing isolation, clear boundaries"
  ✓ Added enforcement: "Constitution Check gate in /plan verifies library boundaries"
  ✓ Saved constitution

  Session complete! 3 questions answered.
```

**Key Features**:
- **Expanded integration**: Architecture principles get rationale and enforcement details
- **Session tracking**: Counts questions answered
- **Automatic marker removal**: `[NEEDS CLARIFICATION]` deleted where resolved

---

### Step 5: Early Termination (Optional)

```
Claude:
  Q4 [Category: Development Workflow]
  What branching strategy should be used?

  | Option | Description |
  |--------|-------------|
  | A      | Trunk-based (all work on main branch) |
  | B      | Feature branches (one branch per feature) |
  | C      | Git Flow (develop/release/hotfix branches) |

User: done

Claude:
  Clarification session ended early.
  - 3/5 questions answered
  - 3 sections updated
  - 2 questions deferred

  ⚠ Warning: 1 [NEEDS CLARIFICATION] marker remains in constitution.
  You can:
  1. Run /clarify-constitution again to resolve remaining markers
  2. Manually edit .specify/memory/constitution.md
  3. Proceed to /specify (markers may cause /plan gate failures)

  Recommendation: Complete all clarifications for smoothest workflow.
```

**Termination Keywords**:
- "done" - Stop asking more questions
- "stop" - Same as done
- "proceed" - Skip remaining questions
- "good" - Satisfied with current state
- "no more" - Explicit refusal to continue

**Effect**: Immediate session end with summary of what was and wasn't resolved.

---

## All Possible Outcomes

### Outcome 1: All Markers Resolved (Best Case)

```
Claude:
  Clarification complete. 5 questions answered.

  Sections updated:
  - Architectural Principles (Principle I)
  - Technology Constraints (Language, Database, Framework)
  - Development Workflow (Team size, Branching)
  - Governance Policies (Amendment process)

  Constitution updated at: .specify/memory/constitution.md

  Coverage Summary:
  | Category | Status |
  |----------|--------|
  | Architectural Principles | Resolved |
  | Technology Constraints | Resolved |
  | Development Workflow | Resolved |
  | Governance Policies | Resolved |

  Remaining [NEEDS CLARIFICATION]: 0

  Next command: /specify (start feature development)
```

**What This Means**:
- Constitution is complete with concrete principles
- No ambiguity remains to block future gates
- Safe to proceed to `/specify` immediately
- Constitution version unchanged (same v1.0.0) - clarifications don't bump version

---

### Outcome 2: Partial Resolution (Some Markers Remain)

```
Claude:
  Clarification session ended early. 3 questions answered.

  Sections updated:
  - Technology Constraints (Database)
  - Development Workflow (Branching)

  Constitution updated at: .specify/memory/constitution.md

  Coverage Summary:
  | Category | Status |
  |----------|--------|
  | Architectural Principles | Outstanding (1 marker remains) |
  | Technology Constraints | Resolved |
  | Development Workflow | Resolved |
  | Governance Policies | Outstanding (1 marker remains) |

  Remaining [NEEDS CLARIFICATION]: 2

  ⚠ Warning: Proceeding with unresolved markers may cause /plan gate failures.

  Next command:
  - /clarify-constitution (complete remaining clarifications)
  - Manual edit: .specify/memory/constitution.md
  - /specify (proceed with partial constitution - higher risk)
```

**What This Means**:
- Some principles still ambiguous
- Future `/plan` commands may fail gates or require Complexity Tracking justification
- Options: Continue clarification or accept risk

---

### Outcome 3: No Markers Found (Skip Scenario)

```
User: /clarify-constitution

Claude:
  Loading constitution from .specify/memory/constitution.md...
  ✓ Parsed 5 principles

  No [NEEDS CLARIFICATION] markers found in constitution.

  The constitution appears complete. If you need to make changes:
  1. Directly edit .specify/memory/constitution.md (plain Markdown)
  2. Run /constitution again to regenerate with new principles

  Next command: /specify (start feature development)
```

**What This Means**:
- Constitution already concrete (no ambiguities)
- Command exits immediately without asking questions
- Safe to proceed to `/specify`

---

## How Answers are Integrated

### Integration Process (Atomic)

For **each accepted answer**, Claude immediately:

1. **Creates Clarifications section** (if doesn't exist):
   ```markdown
   ## Clarifications

   ### Session 2025-10-17
   ```

2. **Records Q&A pair**:
   ```markdown
   - Q: Which database should be used for primary data storage?
   - A: PostgreSQL 15+ → Integrated into Principle II (Technology Constraints)
   ```

3. **Replaces marker** in principle section:
   ```markdown
   Before:
   **Database**: [NEEDS CLARIFICATION]

   After:
   **Database**: PostgreSQL 15+ for primary storage (ACID guarantees, mature async drivers)
   ```

4. **Saves constitution file** (atomic write - prevents loss on crash)

5. **Moves to next question**

**Why Atomic?**: Each save is independent. If session crashes after Q2, answers from Q1 and Q2 are preserved.

---

## Session Tracking and Soft Limit

### Session Counter

Constitution file tracks clarification history:

```markdown
<!-- Clarification Sessions: 0 -->
```

After each session:
```markdown
<!-- Clarification Sessions: 1 -->
<!-- Last Session: 2025-10-17 -->
```

### Soft Limit Warning (3+ Sessions)

```
Claude:
  ⚠ Warning: This is your 4th clarification session.

  Multiple rounds may indicate:
  - Complex project requirements (valid)
  - AI misunderstanding your inputs (consider manual editing)

  You can directly edit .specify/memory/constitution.md if the AI
  continues to misinterpret your responses.

  Continue with clarification? (yes/no)

User: no

Claude:
  Session cancelled.

  You can manually edit .specify/memory/constitution.md:
  1. Open file in text editor
  2. Replace [NEEDS CLARIFICATION] markers with your text
  3. Save file
  4. Run /specify to continue

  The constitution file is plain Markdown - no special syntax required.
```

**Why a Soft Limit?**:
- Prevents infinite loops of misunderstanding
- Offers manual editing escape hatch
- No hard limit - user can continue if needed

---

## 4 Constitution-Specific Categories

Questions are systematically generated across these areas:

### 1. Architectural Principles
**Detects**: Core development philosophy, principle rationale, conflict resolution
**Example Questions**:
- "What is the primary architectural style?" (Library-first, Microservices, Monolith)
- "How should principle conflicts be resolved?" (Simplicity wins, Performance wins, Security wins)

### 2. Technology Constraints
**Detects**: Language versions, frameworks, databases, build tools, platform targets
**Example Questions**:
- "Which database for primary storage?" (PostgreSQL, MongoDB, Redis)
- "What programming language version?" (Python 3.11, Node.js 20, Go 1.21)

### 3. Development Workflow
**Detects**: Team structure, branching strategy, code review, CI/CD, release cadence
**Example Questions**:
- "What branching strategy?" (Trunk-based, Feature branches, Git Flow)
- "How many developers on team?" (Solo, 2-5, 6-10)

### 4. Governance Policies
**Detects**: Constitution amendment process, review frequency, compliance validation
**Example Questions**:
- "How often review constitution?" (Quarterly, Yearly, On major changes)
- "Who can amend constitution?" (Any developer, Team lead, Consensus)

**Category Balance**: If multiple categories have markers, highest-impact category gets priority.

---

## Best Practices

### 1. Answer All Questions (Don't Terminate Early)

**Bad**:
```
User: [After Q2] done
```
**Result**: 3 markers remain, /plan gates may fail

**Good**:
```
User: [Answers all 5 questions]
```
**Result**: 0 markers remain, smooth workflow

---

### 2. Be Concrete Not Vague

**Bad Answers**:
- "Modern database" (still ambiguous)
- "Fast language" (not measurable)
- "Regular reviews" (not specific)

**Good Answers**:
- "PostgreSQL 15" (concrete version)
- "Python 3.11" (specific language)
- "Quarterly reviews" (measurable frequency)

---

### 3. Avoid "It Depends" Answers

**Bad**:
```
Q: Which database?
A: Depends on use case

Result: Marker remains, no clarity gained
```

**Good**:
```
Q: Which database?
A: PostgreSQL 15+ (primary), Redis (caching)

Result: Clear default with specific use cases
```

---

### 4. Use Short Answer When Options Don't Fit

```
Claude:
  Q: What CI/CD platform?
  | A | GitHub Actions |
  | B | GitLab CI |
  | C | Jenkins |
  | Short | Different answer (≤5 words) |

User: Short - Buildkite with Docker

Claude: ✓ Integrated: "Buildkite with Docker containers"
```

**When to Use Short**: Your answer isn't in the provided options, and you have a specific alternative.

---

## Common Issues and Solutions

### Issue 1: Early Termination Leaving Markers

**Symptom**:
```
User: [Terminates after Q2]
Warning: 3 markers remain
```

**Impact**: Future `/plan` gates fail with "ambiguous principle" errors

**Solution**:
```
Run /clarify-constitution again to complete remaining questions
OR
Manually edit .specify/memory/constitution.md
```

---

### Issue 2: Vague Answers Requiring Re-Clarification

**Symptom**:
```
Q: Which database?
A: Modern one

Claude:
  ⚠ Ambiguous answer. Please specify:
  | A | PostgreSQL |
  | B | MongoDB |
  | C | Redis |

User: A

Claude: ✓ Integrated
```

**Prevention**: Be specific on first answer (saves time).

---

### Issue 3: Multiple Sessions Without Progress

**Symptom**:
```
Claude:
  ⚠ This is your 4th clarification session.
  Multiple rounds may indicate AI misunderstanding.
  Continue? (yes/no)
```

**Solution**:
```
User: no

[Manually edit constitution file]
1. Open .specify/memory/constitution.md
2. Replace [NEEDS CLARIFICATION] with concrete text
3. Save file
```

**Why This Happens**: AI may misinterpret natural language answers. Manual editing bypasses interpretation.

---

## Example Session Walkthrough

### Complete 3-Question Session

```
User: /clarify-constitution

Claude:
  Loading constitution...
  ✓ Found 3 markers

  Q1 [Technology Constraints]
  Which programming language and version?
  Format: Short answer (≤5 words)

User: Python 3.11

Claude:
  ✓ Integrated into Principle II
  ✓ Saved constitution

  Q2 [Architectural Principles]
  Core development philosophy?

  | Option | Description |
  |--------|-------------|
  | A      | Test-first (TDD mandatory) |
  | B      | Speed-first (ship fast, test later) |
  | C      | Documentation-first (specs before code) |

User: A

Claude:
  ✓ Integrated into Principle I
  ✓ Added enforcement: "Contract tests before implementation"
  ✓ Saved constitution

  Q3 [Governance Policies]
  Constitution amendment process?

  | Option | Description |
  |--------|-------------|
  | A      | Any developer can propose, team consensus required |
  | B      | Team lead only |
  | C      | Open proposals, majority vote |

User: A

Claude:
  ✓ Integrated into Principle VI
  ✓ Saved constitution

  Session complete! 3 questions answered.

  Coverage Summary:
  | Category | Status |
  |----------|--------|
  | Architectural Principles | Resolved |
  | Technology Constraints | Resolved |
  | Development Workflow | Clear (no markers) |
  | Governance Policies | Resolved |

  Remaining [NEEDS CLARIFICATION]: 0

  Next command: /specify
```

**Session Metadata Added**:
```markdown
<!-- Clarification Sessions: 1 -->
<!-- Last Session: 2025-10-17 -->

## Clarifications

### Session 2025-10-17

- Q: Which programming language and version? → A: Python 3.11
- Q: Core development philosophy? → A: Test-first (TDD mandatory)
- Q: Constitution amendment process? → A: Any developer can propose, team consensus required
```

---

## Maximum 5 Questions Rule

**Why 5?**:
- Prevents analysis paralysis
- Forces prioritization of highest-impact ambiguities
- Keeps session under 15 minutes

**What if More Than 5 Markers?**:
- Claude prioritizes by (Impact × Uncertainty) heuristic
- Top 5 selected automatically
- Remaining markers can be resolved in second session or manually

**Example**:
```
7 markers found → 5 prioritized questions asked → 2 markers remain

Options:
1. Run /clarify-constitution again (max 5 more questions)
2. Manually edit remaining markers
3. Proceed with partial constitution (accept risk)
```

---

## Follow-up Actions

### If All Markers Resolved

```
Next: /specify "Feature description"
```

**Why Safe**: Constitution is complete, `/plan` gates will pass

---

### If Markers Remain

```
Option 1: /clarify-constitution (continue clarification)
Option 2: Manual edit .specify/memory/constitution.md
Option 3: /specify (proceed with risk - /plan may fail gates)
```

**Recommendation**: Complete all clarifications for smoothest workflow

---

### Manual Editing Escape Hatch

```bash
# Open constitution in text editor
vim .specify/memory/constitution.md

# Find marker
[NEEDS CLARIFICATION: database choice]

# Replace with concrete text
PostgreSQL 15+ for primary storage (ACID guarantees, mature async drivers)

# Save file
:wq
```

**When to Use**: AI repeatedly misunderstands your answers, or you prefer direct control

---

## What Constitution Version Unchanged Means

**Version NOT Bumped**: Clarifications don't change constitution version

```
Before: Constitution v1.0.0
After /clarify-constitution: Constitution v1.0.0 (same)
```

**Why?**: Clarifications don't change principles - they **complete** existing principles by replacing markers.

**Version DOES Bump**: Adding/removing principles via `/constitution`

```
/constitution (add new principle) → v1.1.0 (MINOR bump)
```

---

## References

- **[/constitution Command](03-constitution-command.md)**: Creates initial constitution with markers
- **[/specify Command](05-specify-command.md)**: Next step after constitution clarification
- **[Knowledge Base: Constitution](../kb/08-constitution.md)**: Technical details of constitutional enforcement
- **[Knowledge Base: Clarify Commands](../kb/05-commands-clarify.md)**: Deep dive into clarification mechanics
- **[Knowledge Base: Workflows](../kb/10-workflows.md)**: Example clarification sessions in full workflows

---

**Navigation**: [← Page 03: /constitution Command](03-constitution-command.md) | [Page 05: /specify Command →](05-specify-command.md)

---

## Quick Reference

**Command**: `/clarify-constitution` (no arguments)
**Prerequisites**: Constitution file exists with `[NEEDS CLARIFICATION]` markers
**Time**: 5-15 minutes
**Questions**: Maximum 5 per session
**Answer Formats**: Multiple choice (2-5 options) OR short answer (≤5 words)
**Termination**: Type "done", "stop", "proceed", "good", "no more"
**Saves**: Atomic after each answer (prevents loss on crash)
**Output**: Updated `.specify/memory/constitution.md` with markers replaced
**Next Command**: `/specify` (if 0 markers remain) or `/clarify-constitution` (if markers remain)
