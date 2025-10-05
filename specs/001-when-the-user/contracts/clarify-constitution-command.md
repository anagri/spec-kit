# Contract: /clarify-constitution Command

**Version**: 1.0.0
**Type**: Slash Command Template
**File**: `templates/commands/clarify-constitution.md`

## Command Interface

### Syntax
```
/clarify-constitution [context]
```

### Arguments
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `context` | string | No | Additional context for question prioritization (e.g., "focus on tech stack") |

### Examples
```bash
/clarify-constitution
/clarify-constitution "prioritize workflow questions"
/clarify-constitution "focus on governance"
```

## Input/Output Contract

### Input
- **Constitution File**: `.specify/memory/constitution.md` (must exist)
- **User Responses**: Interactive answers during execution
- **Optional Context**: `$ARGUMENTS` from command invocation

### Output
- **Updated Constitution**: Same file with `[NEEDS CLARIFICATION]` markers replaced
- **Clarifications Section**: Added/updated with Q&A session log
- **Console Report**: Summary of questions asked, sections updated, next steps

## Execution Flow Contract

### Step 1: Path Resolution
**Action**: Run bash script to get constitution path
```bash
.specify/scripts/bash/check-prerequisites.sh --json --paths-only
```

**Expected JSON Output**:
```json
{
  "CONSTITUTION_FILE": "/absolute/path/to/.specify/memory/constitution.md"
}
```

**Error Handling**:
- If file not found → Error: "Constitution not found. Run /constitution first."
- If JSON parse fails → Error: "Invalid script output"

### Step 2: Ambiguity Scan
**Action**: Load constitution and scan for `[NEEDS CLARIFICATION]` markers

**Detection Pattern**:
```regex
\[NEEDS CLARIFICATION[^\]]*\]
```

**Taxonomy** (constitution-specific categories):
1. **Architectural Principles** (core development philosophy)
2. **Technology Constraints** (languages, frameworks, platforms)
3. **Development Workflow** (team structure, branching, releases)
4. **Governance Policies** (amendment process, compliance)

**Output**: Internal coverage map with status (Clear/Partial/Missing) per category

### Step 3: Question Generation
**Action**: Create prioritized question queue

**Constraints**:
- Maximum 5 questions total per session
- Each question must be answerable with:
  - Multiple choice (2-5 options), OR
  - Short answer (≤5 words)
- Only include high-impact questions
- Balance across taxonomy categories

**Prioritization Formula**: `Impact × Uncertainty`
- High Impact: Blocks architecture, data modeling, compliance
- High Uncertainty: `[NEEDS CLARIFICATION]` present or contradictory info

### Step 4: Sequential Questioning Loop
**Action**: Present questions one at a time, integrate answers incrementally

**Question Format (Multiple Choice)**:
```markdown
Q: <question text>

| Option | Description |
|--------|-------------|
| A | <option A description> |
| B | <option B description> |
| C | <option C description> |
| Short | Provide different answer (≤5 words) |
```

**Question Format (Short Answer)**:
```markdown
Q: <question text>

Format: Short answer (≤5 words)
```

**Interaction Rules**:
- Present ONE question at a time (never batch)
- Wait for user response
- Validate response (matches option or ≤5 words)
- If ambiguous, request clarification (doesn't count as new question)
- Once satisfactory, integrate and save
- Move to next question or stop

**Stop Conditions**:
- 5 questions asked
- User signals completion ("done", "stop", "good", "no more")
- All critical ambiguities resolved (remaining questions become unnecessary)

### Step 5: Integration
**Action**: Update constitution after EACH accepted answer

**Constitution Structure Changes**:

1. **Add Clarifications Section** (if missing):
```markdown
## Clarifications

### Session 2025-10-05
```

2. **Append Q&A Bullet**:
```markdown
- Q: What is your branching strategy? → A: Trunk-based, direct on main
```

3. **Replace [NEEDS CLARIFICATION] Marker**:
```markdown
# Before
**Workflow**: [NEEDS CLARIFICATION]

# After
**Workflow**: Trunk-based development, direct commits to main
```

4. **Save File** (atomic overwrite after each integration)

**Preservation Rules**:
- Keep heading hierarchy intact
- Preserve manual additions
- Replace contradictory statements (don't duplicate)
- Maintain markdown formatting

### Step 6: Iteration Tracking
**Action**: Track session count for soft limit warning

**Metadata Format** (HTML comment at top of constitution):
```html
<!-- Clarification Sessions: 3 -->
```

**Soft Limit Logic**:
```
IF session_count >= 3:
  WARN "⚠ Warning: Multiple clarification rounds detected.
        Consider direct file editing if AI misunderstands."
CONTINUE (no hard block)
```

### Step 7: Validation
**Action**: Verify constitution integrity after updates

**Checks**:
- [ ] Exactly one Q&A bullet per accepted answer
- [ ] Total questions asked ≤ 5
- [ ] Updated sections have no lingering `[NEEDS CLARIFICATION]` that answer resolved
- [ ] No contradictory earlier statements remain
- [ ] Markdown structure valid
- [ ] Terminology consistent across sections

### Step 8: Completion Report
**Action**: Output summary to user

**Format**:
```markdown
Clarification complete. <N> questions answered.

Sections updated:
- Architectural Principles
- Technology Constraints

Constitution updated at: .specify/memory/constitution.md

Coverage Summary:
| Category | Status |
|----------|--------|
| Architectural Principles | Resolved |
| Technology Constraints | Resolved |
| Development Workflow | Deferred |
| Governance Policies | Clear |

Next command: /specify (to start first feature)
```

**Status Definitions**:
- **Resolved**: Was Partial/Missing, now addressed
- **Clear**: Already sufficient from start
- **Deferred**: Low impact or better suited for later
- **Outstanding**: Still Partial/Missing but question quota reached

## Error Handling

### Constitution Not Found
```
Error: Constitution file not found at .specify/memory/constitution.md

Suggested action: Run /constitution first to create the constitution.
```

### No Markers Detected
```
No [NEEDS CLARIFICATION] markers found in constitution.

The constitution appears complete. If you need to make changes, you can:
1. Directly edit .specify/memory/constitution.md
2. Run /constitution again to regenerate
```

### User Cancellation
```
User stopped clarification at question 2 of 5.

Constitution partially updated (2 questions answered).
Run /clarify-constitution again to continue.
```

### Invalid Response
```
Invalid response. Please choose:
- A valid option letter (A/B/C)
- A short answer (≤5 words)
```

## Behavioral Contracts

### Interactive Behavior
- **One Question at a Time**: Never present multiple questions simultaneously
- **Validate Before Proceeding**: Ensure answer is valid before integration
- **Save After Each Answer**: Minimize risk of context loss
- **Respect Stop Signals**: Honor user's "done"/"stop" immediately

### Escape Hatch
**When User Struggles with AI Understanding**:
```
AI: "It seems there's miscommunication. You can directly edit
     .specify/memory/constitution.md to specify your preferences.
     The file is plain Markdown. Just replace [NEEDS CLARIFICATION]
     with your text."
```

**Manual Edit Support**:
- No file locking during clarification
- Manual edits preserved in next /clarify-constitution run
- No validation on manual content (trust user)

### Iteration Limits
- **Soft Limit**: 3 sessions (warning only)
- **Hard Limit**: None (user can continue indefinitely)
- **Rationale**: Balance guidance with flexibility

## Testing Contracts

### Unit Tests (Template Validation)
```bash
# Test: Marker detection
Given: Constitution with 3 [NEEDS CLARIFICATION] markers
When: /clarify-constitution runs
Then: Detects all 3 markers correctly

# Test: Question limit
Given: 10 potential questions
When: Question generation runs
Then: Queue contains exactly 5 questions

# Test: Sequential questioning
Given: User answers question 1
When: Integration completes
Then: Question 2 presented (not batch)

# Test: Soft limit warning
Given: Session count = 3
When: /clarify-constitution runs 4th time
Then: Warning displayed, execution continues
```

### Integration Tests (End-to-End)
```bash
# Test: Minimal input → clarification → completion
1. /constitution "Python app" (generates markers)
2. /clarify-constitution (answers 3 questions)
3. Verify: Markers replaced, Clarifications section added, file saved

# Test: User stop signal
1. /clarify-constitution
2. User responds "stop" at question 2
3. Verify: 2 answers integrated, session ended gracefully

# Test: Manual edit escape
1. /clarify-constitution
2. User says "AI doesn't understand"
3. Verify: Escape hatch message displayed
4. User edits file manually
5. /clarify-constitution (next session)
6. Verify: Manual edits preserved, remaining markers clarified
```

## Success Criteria

**Functional**:
- [x] Detects all `[NEEDS CLARIFICATION]` markers
- [x] Asks max 5 questions per session
- [x] Presents questions sequentially (one at a time)
- [x] Integrates answers immediately after each response
- [x] Saves file after each integration
- [x] Tracks session count and warns at soft limit
- [x] Supports manual file editing escape hatch

**Non-Functional**:
- [x] No hallucination (NFR-001): Only user-provided content replaces markers
- [x] Preserves manual edits (NFR-002): Markers removed only when user provides info
- [x] Separate from /clarify (NFR-003): Distinct command, doesn't affect spec workflow

**User Experience**:
- Response time <2s per question
- Clear question presentation (markdown table for options)
- Informative completion summary
- Helpful error messages with suggested actions
