# Contract: Constitution Clarification Workflow

**Version**: 1.0.0
**Type**: Interaction Flow
**Scope**: End-to-end user experience from minimal input to complete constitution

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Constitution Generation (Minimal Input)           │
│  Command: /constitution "Python app"                         │
│                                                              │
│  Input: Minimal user description                            │
│  Output: Constitution with [NEEDS CLARIFICATION] markers    │
│  Duration: <5 seconds                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: Iterative Clarification                           │
│  Command: /clarify-constitution                              │
│                                                              │
│  Input: User answers to targeted questions (max 5/session)  │
│  Output: Updated constitution, markers replaced             │
│  Duration: 30-120 seconds (5-8s per question)               │
│  Iterations: Typically 1-2 sessions, soft limit at 3        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: Feature Development                                │
│  Command: /specify                                           │
│                                                              │
│  Input: Complete constitution as governance context         │
│  Output: Feature specification                              │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Workflow States

### State 1: No Constitution Exists

**User Action**: `/constitution "minimal description"`

**System Behavior**:
1. Parse user input (Step 1-2 of constitution.md)
2. Attempt to fill placeholders from input + repo context
3. Insert `[NEEDS CLARIFICATION]` for missing values
4. Write constitution with markers
5. Report marker count and suggest `/clarify-constitution`

**Output Example**:
```
Constitution created at .specify/memory/constitution.md

Version: 1.0.0 (new constitution)

⚠ Incomplete Sections (4):
- Architectural Principle (Principle I)
- Framework (Technology Stack)
- Development Workflow
- Governance policies

Next command: /clarify-constitution
```

**File State**:
```markdown
<!-- Clarification Sessions: 0 -->

## Core Principles
### I. Architectural Principle
[NEEDS CLARIFICATION]

### II. Technology Stack
**Language**: Python [NEEDS CLARIFICATION: version]
**Framework**: [NEEDS CLARIFICATION: FastAPI vs Django]
...
```

**Transition**: User runs `/clarify-constitution` → State 2

---

### State 2: First Clarification Session

**User Action**: `/clarify-constitution`

**System Behavior**:
1. Load constitution, detect 4 `[NEEDS CLARIFICATION]` markers
2. Generate 5 prioritized questions across taxonomy
3. Present Question 1 (interactive)

**Interaction Flow**:

**Q1**: (Architectural Principles category)
```
What is the primary architectural principle for this project?

| Option | Description |
|--------|-------------|
| A | Test-first development (write tests before code) |
| B | Library-first (minimize custom code, use existing libraries) |
| C | Performance-first (optimize for speed/resource usage) |
| Short | Provide different principle (≤5 words) |
```

**User**: `A`

**System**:
- Validates answer
- Updates constitution:
  ```markdown
  ### I. Test-First Development
  All features MUST have tests written before implementation.
  ```
- Adds to Clarifications:
  ```markdown
  ## Clarifications
  ### Session 2025-10-05
  - Q: What is the primary architectural principle? → A: Test-first development
  ```
- Saves file
- Presents Q2

**Q2**: (Technology Constraints category)
```
What Python version and framework will you use?

| Option | Description |
|--------|-------------|
| A | Python 3.11 + FastAPI (modern async framework) |
| B | Python 3.11 + Django (full-featured framework) |
| C | Python 3.10 + Flask (lightweight framework) |
| Short | Specify different (≤5 words) |
```

**User**: `A`

**System**: (same integration process as Q1)

**Q3-Q5**: Continue for Workflow, Governance, etc.

**After 5 Questions**:
```
Clarification complete. 5 questions answered.

Sections updated:
- Architectural Principles (Principle I)
- Technology Constraints (version, framework)
- Development Workflow
- Governance (partially - 1 aspect covered)

Constitution updated at: .specify/memory/constitution.md

Coverage Summary:
| Category | Status |
|----------|--------|
| Architectural Principles | Resolved |
| Technology Constraints | Resolved |
| Development Workflow | Resolved |
| Governance Policies | Partial (2 aspects remaining) |

Remaining [NEEDS CLARIFICATION]: 2

Next command: /clarify-constitution (to complete Governance) or /specify (proceed with partial)
```

**File State**:
```markdown
<!-- Clarification Sessions: 1 -->

## Clarifications
### Session 2025-10-05
- Q: What is the primary architectural principle? → A: Test-first development
- Q: What Python version and framework? → A: Python 3.11 + FastAPI
- Q: What is your development workflow? → A: Solo dev, trunk-based
- Q: How often should constitution be reviewed? → A: Quarterly
- Q: Who can amend the constitution? → A: Project owner only

## Core Principles
### I. Test-First Development
All features MUST have tests written before implementation.

### II. Technology Stack
**Language**: Python 3.11
**Framework**: FastAPI

## Development Workflow
Solo developer workflow, trunk-based development (direct commits to main).

## Governance
**Review Frequency**: Quarterly
**Amendment Authority**: [NEEDS CLARIFICATION: process for amendments]
**Versioning**: [NEEDS CLARIFICATION: semantic versioning policy]
```

**Transition Options**:
- User runs `/clarify-constitution` again → State 3 (Second Session)
- User runs `/specify` → State 4 (Proceed with Partial Constitution)
- User edits file manually → State 5 (Manual Completion)

---

### State 3: Second Clarification Session (Iteration)

**User Action**: `/clarify-constitution` (2nd time)

**System Behavior**:
1. Load constitution, detect 2 remaining `[NEEDS CLARIFICATION]` markers
2. Generate 2 questions (only for missing sections)
3. Sequential Q&A as before

**Q1**:
```
What is the process for amending the constitution?

| Option | Description |
|--------|-------------|
| A | Requires approval from all team members |
| B | Project owner decides unilaterally |
| C | Consensus-based discussion then vote |
| Short | Describe process (≤5 words) |
```

**User**: `B`

**Q2**:
```
What versioning policy for constitution changes?

Format: Short answer (≤5 words)
```

**User**: `Semantic versioning`

**Completion**:
```
Clarification complete. 2 questions answered.

All sections now complete! ✓

Constitution updated at: .specify/memory/constitution.md

Next command: /specify (start feature development)
```

**File State**:
```markdown
<!-- Clarification Sessions: 2 -->

## Clarifications
### Session 2025-10-05
- Q: What is the primary architectural principle? → A: Test-first development
- Q: What Python version and framework? → A: Python 3.11 + FastAPI
- Q: What is your development workflow? → A: Solo dev, trunk-based
- Q: How often should constitution be reviewed? → A: Quarterly
- Q: Who can amend the constitution? → A: Project owner only
- Q: What is the process for amending? → A: Project owner decides
- Q: What versioning policy? → A: Semantic versioning

## Core Principles
[All sections complete - no markers]

## Governance
**Review Frequency**: Quarterly
**Amendment Process**: Project owner decides unilaterally
**Versioning**: Semantic versioning
```

**Transition**: User runs `/specify` → State 6 (Feature Development)

---

### State 4: Proceed with Partial Constitution (Optional)

**User Action**: `/specify` (while markers still exist)

**System Behavior**:
- Constitution loaded with 2 `[NEEDS CLARIFICATION]` markers
- Feature spec references constitution but notes incomplete sections
- Warning in spec template execution flow:
  ```
  WARN: Constitution has 2 incomplete sections (Governance)
  Consider completing with /clarify-constitution before planning
  ```

**Trade-off**:
- **Pro**: Faster start, can proceed with core principles defined
- **Con**: Governance gaps may surface during planning/implementation

**Valid Use Case**: Exploratory spikes where full governance isn't critical yet

---

### State 5: Manual File Editing (Escape Hatch)

**User Action**: Direct edit of `.specify/memory/constitution.md`

**Trigger**: AI misunderstands user's intent after multiple clarification attempts

**System Guidance** (during /clarify-constitution):
```
User: "The AI doesn't understand my workflow"

AI: "You can directly edit .specify/memory/constitution.md to specify
     your workflow. The file is plain Markdown. Just replace
     [NEEDS CLARIFICATION] with your text and save."
```

**User Edits**:
```markdown
# Before
**Workflow**: [NEEDS CLARIFICATION]

# After (manual edit)
**Workflow**: Custom hybrid approach - feature branches for complex work,
direct commits for hotfixes, code review via pair programming
```

**Next /clarify-constitution**:
- Detects manual edit (no marker in Workflow section)
- Preserves manual content
- Focuses questions on remaining marked sections

**File State**:
```markdown
<!-- Clarification Sessions: 2 -->

## Clarifications
### Session 2025-10-05
[Questions about other topics - Workflow not in Q&A list]

## Development Workflow
Custom hybrid approach - feature branches for complex work,
direct commits for hotfixes, code review via pair programming
[User's manual content preserved]
```

**Validation**: None (trust user's manual edits)

---

### State 6: Soft Limit Warning (3+ Sessions)

**User Action**: `/clarify-constitution` (4th time)

**System Behavior**:
1. Increment session count: `<!-- Clarification Sessions: 4 -->`
2. Detect `session_count >= 3`
3. Display warning before starting questions:

```
⚠ Warning: This is your 4th clarification session.

Multiple rounds may indicate:
- Complex project requirements (valid)
- AI misunderstanding your inputs (consider manual editing)

You can directly edit .specify/memory/constitution.md if the AI
continues to misinterpret your responses.

Continue with clarification? (yes/no)
```

**User**: `yes`

**System**: Proceed with normal clarification workflow (no hard block)

**Rationale** (from spec FR-012):
- Soft limit educates user about typical completion (1-2 sessions)
- Allows continuation for legitimately complex projects
- Suggests escape hatch without forcing it

---

### State 7: Comprehensive Input (No Clarification Needed)

**User Action**: `/constitution "detailed multi-paragraph description with all principles, tech stack, workflow, governance"`

**System Behavior**:
1. Parse comprehensive input
2. Fill all placeholders from user description
3. Zero `[NEEDS CLARIFICATION]` markers
4. Write complete constitution
5. Skip session metadata (no clarification needed)

**Output**:
```
Constitution created at .specify/memory/constitution.md

Version: 1.0.0 (new constitution)

✓ All sections complete

Next command: /specify

Suggested commit message:
docs: create constitution v1.0.0 (Python 3.11, FastAPI, test-first)
```

**File State**:
```markdown
# Project Constitution

## Core Principles
[All sections complete - no markers, no Clarifications section]

**Version**: 1.0.0 | **Ratified**: 2025-10-05
```

**Transition**: User runs `/specify` directly (skip clarification phase)

---

## State Transition Matrix

| From State | User Action | To State | Condition |
|------------|-------------|----------|-----------|
| None | `/constitution "minimal"` | State 1 | Insufficient input |
| None | `/constitution "comprehensive"` | State 7 | Complete input |
| State 1 | `/clarify-constitution` | State 2 | First session |
| State 2 | `/clarify-constitution` | State 3 | Markers remain |
| State 2 | `/specify` | State 4 | User proceeds with partial |
| State 2 | Manual edit | State 5 | AI misunderstanding |
| State 3 | `/clarify-constitution` (4th) | State 6 | Session count ≥ 3 |
| Any | `/clarify-constitution` | Complete | No markers detected |

## Timing Expectations

| Phase | Duration | Variation |
|-------|----------|-----------|
| Constitution generation | 2-5s | Depends on input length |
| Question generation | 1-2s | Per session start |
| User answer time | 5-30s | Per question (human speed) |
| Integration + save | <1s | Per answer |
| Full clarification session | 30-120s | 5 questions × (present + answer + integrate) |
| Typical complete flow | 1-3 min | 1-2 clarification sessions |
| Edge case (manual edit) | Variable | User editing time |

## Error Recovery

### Constitution File Deleted Mid-Workflow

**Scenario**: User deletes `.specify/memory/constitution.md` between sessions

**Detection**: `/clarify-constitution` runs path check (Step 1)

**Error**:
```
Error: Constitution file not found at .specify/memory/constitution.md

The file may have been deleted or moved.

Suggested action: Run /constitution again to recreate it.
```

**Recovery**: User runs `/constitution` to start over

### Corrupted Clarifications Section

**Scenario**: Manual edit breaks markdown structure

**Detection**: `/clarify-constitution` parses file (Step 2)

**Behavior**:
- Attempt to parse existing Q&A bullets
- If parse fails: Create new `### Session YYYY-MM-DD` subheading
- Continue with normal workflow (isolate new session from corrupted history)

**Rationale**: Graceful degradation, don't block user due to prior corruption

### Concurrent Edits (User + Command)

**Scenario**: User edits file while `/clarify-constitution` is running

**Prevention**: File saved after each answer integration (minimizes conflict window)

**If Conflict Occurs**:
- User's manual edits in non-marked sections: Preserved
- User's edits conflict with marker replacement: Last write wins (command overwrites)

**Mitigation**: Document in user guidance:
```
Don't edit constitution file while /clarify-constitution is running.
Wait for session to complete, then make manual edits if needed.
```

## Success Metrics

**Functional Goals**:
- [x] User can create complete constitution in 1-3 clarification sessions
- [x] No hallucination (user-provided content only)
- [x] Manual editing escape hatch available
- [x] Soft limit guides users without blocking

**User Experience Goals**:
- [x] Clear progress indication (questions N/5, sections updated)
- [x] Helpful error messages with recovery actions
- [x] Multiple valid paths to completion (interactive, manual, comprehensive input)

**Performance Goals**:
- [x] Constitution generation <5s
- [x] Question presentation <2s
- [x] Integration + save <1s per answer
- [x] Full workflow 1-3 minutes typical

## Validation Checklist

**Workflow Completeness**:
- [x] State 1: Minimal input → markers
- [x] State 2: First clarification session
- [x] State 3: Iterative clarification
- [x] State 4: Proceed with partial (optional path)
- [x] State 5: Manual editing escape
- [x] State 6: Soft limit warning
- [x] State 7: Comprehensive input (no clarification)

**Error Handling**:
- [x] File not found recovery
- [x] Corrupted sections graceful degradation
- [x] Concurrent edit mitigation

**User Guidance**:
- [x] Clear next steps at each state
- [x] Informative error messages
- [x] Escape hatch documentation
