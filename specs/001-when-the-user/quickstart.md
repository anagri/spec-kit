# Quick Start: Constitution Clarification Feature

**Feature**: 001-when-the-user | **For**: Developers using spec-kit

## What This Feature Does

Prevents hallucinated constitutions by requiring user clarification before generation. Instead of the AI guessing your project's principles, tech stack, and governance, it asks targeted questions to build an accurate constitution based on YOUR input.

## Prerequisites

- Spec-kit installed (`speclaude init` completed)
- Basic understanding of project constitutions

## Basic Usage (3 Steps)

### Step 1: Create Constitution with Minimal Input

```bash
/constitution "Python web application"
```

**What Happens**:
- AI analyzes your input (insufficient for complete constitution)
- Generates constitution with `[NEEDS CLARIFICATION]` markers
- Reports which sections need clarification

**Output**:
```
Constitution created at .specify/memory/constitution.md

⚠ Incomplete Sections (4):
- Architectural Principle
- Framework
- Development Workflow
- Governance policies

Next command: /clarify-constitution
```

### Step 2: Run Clarification

```bash
/clarify-constitution
```

**What Happens**:
- AI asks up to 5 targeted questions (one at a time)
- You answer each question (multiple choice or short answer)
- Constitution updates after each answer
- Sections with `[NEEDS CLARIFICATION]` get replaced with your answers

**Example Interaction**:
```
Q1: What is the primary architectural principle?

| Option | Description |
|--------|-------------|
| A | Test-first development |
| B | Library-first (minimal custom code) |
| C | Performance-first |
| Short | Your own principle (≤5 words) |

You: A

✓ Updated Principle I to "Test-First Development"

Q2: What Python framework?

| Option | Description |
|--------|-------------|
| A | FastAPI (modern async) |
| B | Django (full-featured) |
| C | Flask (lightweight) |
| Short | Different framework (≤5 words) |

You: A

✓ Updated Technology Stack
...
```

### Step 3: Start Feature Development

```bash
/specify "your first feature"
```

**What Happens**:
- Constitution now complete (no markers)
- Feature spec references accurate constitution
- Development follows YOUR stated principles

## Advanced Usage

### Multiple Clarification Sessions

If 5 questions aren't enough, run `/clarify-constitution` again:

```bash
/clarify-constitution  # First session: 5 questions
# ... some sections still incomplete

/clarify-constitution  # Second session: remaining questions
# ... constitution complete
```

**Soft Limit**: After 3 sessions, you'll see a warning suggesting manual editing if AI misunderstands.

### Direct Editing (Escape Hatch)

If AI doesn't understand your answer, edit the constitution file directly:

```bash
# Open in your editor
vim .specify/memory/constitution.md

# Find and replace [NEEDS CLARIFICATION]
**Workflow**: [NEEDS CLARIFICATION]
# Change to:
**Workflow**: Custom hybrid - feature branches for complex work, trunk-based for hotfixes
```

Next `/clarify-constitution` will skip sections you manually completed.

### Comprehensive Input (Skip Clarification)

Provide detailed description upfront to skip clarification:

```bash
/constitution "This is a Python 3.11 + FastAPI project. Test-first development principle - all features must have tests before code. Solo developer workflow with trunk-based development (direct commits to main). Quarterly constitution review. Project owner can amend constitution. Semantic versioning for constitution changes."
```

**Output**:
```
Constitution created at .specify/memory/constitution.md

✓ All sections complete

Next command: /specify
```

No clarification needed!

## Common Workflows

### Workflow 1: New Project (Minimal → Clarify → Develop)
```bash
speclaude init my-project
cd my-project
/constitution "Python microservice"
/clarify-constitution
# Answer 5 questions
/specify "User authentication API"
/plan "FastAPI + PostgreSQL + JWT"
/tasks
/implement
```

### Workflow 2: New Project (Comprehensive → Develop)
```bash
speclaude init my-project
cd my-project
/constitution "Python 3.11 FastAPI microservice. Test-first principle. Solo dev, trunk-based. Quarterly reviews. Owner-managed amendments."
/specify "User authentication API"
# Skip /clarify-constitution - not needed
```

### Workflow 3: Iterative Clarification
```bash
/constitution "Rust CLI tool"
/clarify-constitution
# Answer 3 questions, 2 sections still unclear
/clarify-constitution
# Answer 2 more questions, all complete
/specify "Command-line argument parser"
```

### Workflow 4: Manual Edit Recovery
```bash
/constitution "Node.js app"
/clarify-constitution
Q: What is your deployment strategy?
You: Kubernetes with Helm charts and GitOps
AI: "I don't have a multiple choice option for that."

# Escape to manual editing
vim .specify/memory/constitution.md
# Replace [NEEDS CLARIFICATION] in Deployment section

/clarify-constitution
# AI focuses on remaining sections, skips manually edited Deployment
```

## Understanding the Output

### Constitution with Markers
```markdown
## Core Principles

### I. Architectural Principle
[NEEDS CLARIFICATION]

### II. Technology Stack
**Language**: Python [NEEDS CLARIFICATION: version]
**Framework**: [NEEDS CLARIFICATION: FastAPI vs Django]
```

**Markers indicate**: AI needs YOUR input (won't guess)

### Constitution with Clarifications
```markdown
## Clarifications

### Session 2025-10-05
- Q: What is the primary architectural principle? → A: Test-first development
- Q: What Python framework? → A: FastAPI

## Core Principles

### I. Test-First Development
All features MUST have tests written before implementation.

### II. Technology Stack
**Language**: Python 3.11
**Framework**: FastAPI
```

**Clarifications section**: History of your answers (audit trail)

## Troubleshooting

### "Constitution not found" error

**Cause**: Ran `/clarify-constitution` before `/constitution`

**Fix**:
```bash
/constitution "your project description"
# Then run clarification
```

### "No clarifications needed" message

**Cause**: Constitution already complete (no `[NEEDS CLARIFICATION]` markers)

**Fix**: Constitution is done! Proceed to `/specify`

### AI keeps misunderstanding my answers

**Cause**: Complex or nuanced requirement doesn't fit predefined options

**Fix**:
```bash
# Option 1: Use "Short" answer option (≤5 words)
# Option 2: Manually edit constitution file
vim .specify/memory/constitution.md
```

### Soft limit warning appears

**Message**:
```
⚠ Warning: This is your 4th clarification session.
Consider direct editing if AI misunderstands.
```

**Meaning**: You've run `/clarify-constitution` 3+ times (unusual)

**Action**:
- If project is complex: Continue (no hard limit)
- If AI misunderstands: Use manual editing

## Testing Your Constitution

### Verify Completion

Check for markers:
```bash
grep "NEEDS CLARIFICATION" .specify/memory/constitution.md
# Empty output = complete
```

### Review Clarification History

Check Q&A log:
```bash
# View Clarifications section
sed -n '/## Clarifications/,/^## /p' .specify/memory/constitution.md
```

### Validate Structure

Ensure all required sections present:
```bash
grep "^## " .specify/memory/constitution.md
# Should show:
# ## Core Principles
# ## Technology Constraints (or similar)
# ## Development Workflow (or similar)
# ## Governance
```

## Next Steps

1. **Complete Constitution**: Ensure no `[NEEDS CLARIFICATION]` markers remain
2. **Review Principles**: Read `.specify/memory/constitution.md` to confirm accuracy
3. **Start Features**: Run `/specify` to create your first feature spec
4. **Dogfood**: Use spec-kit methodology to develop your project

## Related Commands

- `/constitution` - Create or update constitution
- `/clarify-constitution` - Answer questions to complete constitution
- `/specify` - Create feature specification (uses constitution as context)
- `/plan` - Generate technical implementation plan (validates against constitution)

## Key Takeaways

✓ **No Hallucination**: `[NEEDS CLARIFICATION]` prevents AI guesses
✓ **Interactive**: Max 5 questions per session, one at a time
✓ **Iterative**: Run clarification multiple times if needed
✓ **Flexible**: Manual editing escape hatch always available
✓ **Auditable**: Clarifications section logs all your answers
