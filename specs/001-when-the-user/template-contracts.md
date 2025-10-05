# Template Contracts: Constitution Clarification Flow

**Feature**: 001-when-the-user | **Date**: 2025-10-05

## Overview

This document defines the structure and contracts for the new `/clarify-constitution` command template and modifications to the existing `/constitution` template.

## Template File Contracts

### 1. /clarify-constitution Command Template

**File**: `templates/commands/clarify-constitution.md`

**Structure**:
```yaml
---
description: "Identify underspecified areas in the constitution by asking targeted clarification questions and encoding answers back into the constitution."
---

[Execution flow markdown]
```

**Required Sections**:
1. **YAML Frontmatter**
   - `description`: Single-line command description (< 100 chars)

2. **User Input Handling**
   - `$ARGUMENTS` placeholder for optional user context
   - Note about considering user input before execution

3. **Execution Flow** (numbered steps):
   - Step 1: Path resolution (call `check-prerequisites.sh --json --paths-only`)
   - Step 2: Load constitution and scan for `[NEEDS CLARIFICATION]` markers
   - Step 3: Generate prioritized question queue (max 5 questions)
   - Step 4: Sequential questioning loop (ONE question at a time)
   - Step 5: Integration after each answer
   - Step 6: Validation
   - Step 7: Write updated constitution
   - Step 8: Report completion

4. **Question Taxonomy** (constitution-specific):
   - Architectural Principles
   - Technology Constraints
   - Development Workflow
   - Governance Policies

5. **Question Format Specifications**:
   - Multiple choice: 2-5 options in markdown table
   - Short answer: ≤5 words constraint
   - One question at a time (never batch)

6. **Integration Rules**:
   - Create `## Clarifications` section if missing
   - Create `### Session YYYY-MM-DD` subsection for today
   - Append `- Q: <question> → A: <answer>` bullets
   - Replace `[NEEDS CLARIFICATION]` with concrete content
   - Save after each integration

7. **Iteration Tracking**:
   - Session count metadata in constitution
   - Soft limit: 3 rounds
   - Warning after threshold
   - No hard block

8. **Behavior Rules**:
   - Max 5 questions per session
   - Respect user "stop"/"done" signals
   - Support manual file editing escape hatch

**Input**: None (operates on `.specify/memory/constitution.md`)

**Output**: Updated constitution with clarifications integrated

### 2. /constitution Command Template Modifications

**File**: `templates/commands/constitution.md`

**Changes Required**:

1. **Step 2 (Placeholder Collection)** - Add clarification flow:
```markdown
2. Collect/derive values for placeholders:
   - If user input supplies value, use it
   - If placeholder has sufficient context, infer from repo
   - If neither: Mark section with [NEEDS CLARIFICATION]
   - Inform user that /clarify-constitution can be run to provide details
```

2. **Step 3 (Draft Constitution)** - Handle markers:
```markdown
3. Draft the updated constitution content:
   - Replace placeholders with concrete text OR [NEEDS CLARIFICATION]
   - Sections marked with [NEEDS CLARIFICATION] indicate missing user input
   - Preserve heading hierarchy
```

3. **Step 7 (Write Constitution)** - Add informational output:
```markdown
7. Write completed constitution to `.specify/memory/constitution.md`
   - If [NEEDS CLARIFICATION] markers present, inform user to run:
     /clarify-constitution
```

4. **Step 8 (Summary)** - Include marker count:
```markdown
8. Output final summary:
   - New version and bump rationale
   - Count of [NEEDS CLARIFICATION] markers (if any)
   - Next command: /clarify-constitution (if markers present) OR /specify
```

**Backward Compatibility**: ✓ (existing behavior preserved, new markers are additive)

### 3. Constitution File Structure Contract

**File**: `.specify/memory/constitution.md`

**New Elements**:

1. **Clarification Markers**:
```markdown
### I. Principle Name
[NEEDS CLARIFICATION]

**Rationale**: [NEEDS CLARIFICATION]
```

2. **Clarifications Section** (added by /clarify-constitution):
```markdown
## Clarifications

### Session 2025-10-05
- Q: What is the primary architectural principle? → A: Test-first development
- Q: What branching strategy do you use? → A: Trunk-based (direct on main)
```

3. **Session Metadata** (for iteration tracking):
```markdown
<!-- Clarification Sessions: 2 -->
```

**Validation Rules**:
- `[NEEDS CLARIFICATION]` only in content sections (not headings)
- Session dates in ISO format (YYYY-MM-DD)
- Q&A bullets follow format: `- Q: <text> → A: <text>`
- Session count ≥ 0

## Command Argument Contracts

### /clarify-constitution

**Syntax**: `/clarify-constitution [context]`

**Arguments**:
- `context` (optional): Additional context for question prioritization

**Examples**:
```bash
/clarify-constitution                          # Standard clarification
/clarify-constitution "focus on tech stack"    # Prioritize technology questions
```

**Exit Codes** (conceptual for scripting):
- 0: Success (all critical clarifications resolved)
- 1: User cancelled ("stop" signal)
- 2: File not found (no constitution exists)

### /constitution (modified)

**Syntax**: `/constitution [principles]`

**Behavior Change**:
- Previously: Generate complete constitution (with potential hallucination)
- Now: Generate constitution with `[NEEDS CLARIFICATION]` for missing info
- Suggests `/clarify-constitution` if markers present

**Backward Compatible**: ✓ (comprehensive input still generates complete constitution)

## JSON Output Contracts

### check-prerequisites.sh --json --paths-only

**Output** (used by /clarify-constitution):
```json
{
  "CONSTITUTION_FILE": "/path/to/.specify/memory/constitution.md"
}
```

**Fields**:
- `CONSTITUTION_FILE` (string): Absolute path to constitution
- Other fields optional (feature-specific paths not needed)

**Error Output**:
```json
{
  "error": "Constitution file not found",
  "suggestion": "Run /constitution first"
}
```

## Interaction Flow Contracts

### Minimal Input Flow (Scenario 1)

```
User: /constitution "Python web app"
      ↓
AI: Analyzes input (insufficient details)
      ↓
Output: Constitution generated with:
  - Tech Stack: Python [NEEDS CLARIFICATION: version, framework]
  - Workflow: [NEEDS CLARIFICATION]
  - Governance: [NEEDS CLARIFICATION]

  "This constitution has 3 sections needing clarification.
   Run /clarify-constitution to provide details."
```

### Clarification Flow (Scenario 2)

```
User: /clarify-constitution
      ↓
AI: Scans constitution → finds 3 [NEEDS CLARIFICATION] markers
      ↓
AI: "I found 3 areas needing clarification. Let's start:"
      ↓
AI: "Q1: What Python version and framework?"
    | Option | Description |
    | Python 3.11 + FastAPI | Modern async framework |
    | Python 3.11 + Django | Full-featured web framework |
    | Short | Provide different answer (≤5 words) |
      ↓
User: "A"
      ↓
AI: Updates constitution:
    - Removes [NEEDS CLARIFICATION] from Tech Stack
    - Adds "Python 3.11 + FastAPI"
    - Adds to Clarifications/Session
    - Saves file
      ↓
AI: "Q2: What is your development workflow?"
    [continues until 5 questions or user stops]
      ↓
AI: "Clarification complete. 3 questions answered.
     Constitution updated at .specify/memory/constitution.md"
```

### Iteration Warning Flow

```
User: /clarify-constitution (4th time)
      ↓
AI: Detects session count = 3
      ↓
AI: "⚠ Warning: This is your 4th clarification session.
     If the AI continues to misunderstand, consider editing
     .specify/memory/constitution.md directly."
      ↓
[Proceeds with normal clarification]
```

### Manual Edit Escape Flow

```
User: "The AI doesn't understand my workflow"
      ↓
AI: "You can directly edit `.specify/memory/constitution.md`
     to specify your workflow. The file is plain Markdown.
     Just replace [NEEDS CLARIFICATION] with your text."
      ↓
[User edits file manually]
      ↓
User: /clarify-constitution (later)
      ↓
AI: Detects no [NEEDS CLARIFICATION] in manually edited section
      ↓
AI: Focuses questions on remaining unclear sections
```

## File Structure Contract

### Directory Layout

```
templates/commands/
├── clarify-constitution.md    # NEW
├── constitution.md            # MODIFIED
└── [existing commands...]

.specify/memory/
└── constitution.md            # MODIFIED (supports markers)

specs/001-when-the-user/
├── template-contracts.md      # THIS FILE
├── contracts/                 # Implementation contracts
│   ├── clarify-constitution-command.md
│   ├── constitution-template.md
│   └── clarification-workflow.md
└── [other docs...]
```

## Validation Contracts

### Template Validation

**Checklist for /clarify-constitution template**:
- [ ] YAML frontmatter with description
- [ ] $ARGUMENTS placeholder handled
- [ ] 8-step execution flow present
- [ ] Constitution-specific question taxonomy defined
- [ ] Question format specifications (table for multiple choice)
- [ ] Max 5 questions enforced
- [ ] Sequential questioning (one at a time)
- [ ] Integration after each answer
- [ ] Session tracking logic
- [ ] Soft limit warning (3 rounds)
- [ ] Manual editing escape hatch mentioned

**Checklist for /constitution modifications**:
- [ ] Step 2: Add [NEEDS CLARIFICATION] marker logic
- [ ] Step 3: Preserve markers in draft
- [ ] Step 7: Detect markers, suggest /clarify-constitution
- [ ] Step 8: Include marker count in summary
- [ ] Backward compatible (comprehensive input still works)

### Constitution File Validation

**Valid Constitution with Markers**:
```markdown
## Core Principles

### I. Test-First Development
All features MUST have tests written before implementation.

### II. Technology Stack
**Language**: [NEEDS CLARIFICATION]
**Framework**: [NEEDS CLARIFICATION]

## Clarifications

### Session 2025-10-05
- Q: What is the primary architectural principle? → A: Test-first

<!-- Clarification Sessions: 1 -->
```

**Invalid Examples**:
```markdown
# Invalid: Marker in heading
### II. [NEEDS CLARIFICATION]  ❌

# Invalid: Wrong Q&A format
- Question: What version? Answer: Python 3.11  ❌

# Invalid: Wrong date format
### Session 10/05/2025  ❌
```

## Contract Tests Required

1. **test_clarify_constitution_output.sh**:
   - Verify JSON input parsing
   - Check marker detection logic
   - Validate question generation (max 5)
   - Test integration updates constitution
   - Confirm session tracking works

2. **test_constitution_markers.sh**:
   - Verify [NEEDS CLARIFICATION] syntax
   - Check marker placement rules (not in headings)
   - Test marker removal on clarification
   - Validate preservation of manual edits

3. **test_constitution_workflow.sh**:
   - Scenario 1: Minimal input → markers present
   - Scenario 2: Clarification → markers removed
   - Scenario 3: Soft limit warning displayed
   - Scenario 4: Comprehensive input → no markers

## Summary

**New Templates**: 1 (`clarify-constitution.md`)
**Modified Templates**: 1 (`constitution.md`)
**New Constitution Features**: Clarification markers, session tracking, Q&A history
**Backward Compatibility**: ✓ (all existing functionality preserved)
**Constitutional Compliance**: ✓ (Claude-only, bash-only, no git coupling)
