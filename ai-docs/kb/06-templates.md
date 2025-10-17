# Template System and Constraint Mechanisms

**Purpose**: Explains how templates constrain LLM output to produce architecturally consistent results
**Target Audience**: Developers understanding AI behavior constraints
**Related Files**:

- [AI Patterns](09-ai-patterns.md) - How Claude processes templates
- [Commands: Core](04-commands-core.md) - Commands using templates
- [Architecture](03-architecture.md) - Template engine layer
- [Philosophy](02-philosophy.md) - Constraint-driven generation principle

**Keywords**: templates as constraints, execution flows, [NEEDS CLARIFICATION], placeholder system

---

## Overview

The genius of spec-kit lies in treating templates as **reduction functions** that constrain the vast output space of LLMs into architecturally consistent results.

## Templates as Constraint Functions

### Mathematical Model

```
Unconstrained LLM: Output space = 10^n (hallucination-prone)
                         ↓
          Apply template with execution flow
                         ↓
    Constrained outputs = 10^3 (valid)
                         ↓
           Apply constitutional gates
                         ↓
    Acceptable outputs = 10^1 (enforced)
```

Templates transform probabilistic text generation into deterministic architectural workflows by constraining decision space at every step.

---

## Seven Template Constraint Mechanisms

### 1. Preventing Premature Implementation Details

**Spec Template Constraint**:

```markdown
## ⚡ Quick Guidelines

- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
```

**Effect**: Forces LLM to maintain proper abstraction levels. When an LLM might naturally jump to "implement using React with Redux," the template keeps it focused on "users need real-time updates."

**Why This Matters**: Specifications remain stable even as implementation technologies change.

### 2. Forcing Explicit Uncertainty Markers

**Both Spec and Plan Templates**:

```markdown
When creating this spec from a user prompt:

1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question]
2. **Don't guess**: If the prompt doesn't specify something, mark it
```

**Example Output**:

```markdown
- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION:
  auth method not specified - email/password, SSO, OAuth?]
```

**Effect**: Prevents common LLM behavior of making plausible but potentially incorrect assumptions.

**Why This Matters**: Explicit uncertainty prevents downstream rework when assumptions prove wrong.

### 3. Structured Thinking Through Checklists

**Template Checklists as "Unit Tests"**:

```markdown
### Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
```

**Effect**: Forces LLM to self-review systematically, catching gaps that might otherwise slip through.

**Why This Matters**: Provides a quality assurance framework embedded in the template.

### 4. Constitutional Compliance Through Gates

**Plan Template Gates**:

```markdown
### Phase -1: Pre-Implementation Gates

#### Simplicity Gate (Article VII)

- [ ] Using ≤3 projects?
- [ ] No future-proofing?

#### Anti-Abstraction Gate (Article VIII)

- [ ] Using framework directly?
- [ ] Single model representation?
```

**Effect**: Prevents over-engineering by making LLM explicitly justify complexity.

**If Gate Fails**: Document in Complexity Tracking table with rationale:

```markdown
| Violation   | Why Needed                | Simpler Alternative Rejected                |
| ----------- | ------------------------- | ------------------------------------------- |
| 4th project | Performance critical path | 3 projects created bottleneck in benchmarks |
```

**Why This Matters**: Creates accountability for architectural decisions.

### 5. Hierarchical Detail Management

**Template Instruction**:

```markdown
**IMPORTANT**: This implementation plan should remain high-level and readable.
Any code samples, detailed algorithms, or extensive technical specifications
must be placed in the appropriate `implementation-details/` file
```

**Effect**: Prevents specifications from becoming unreadable code dumps. LLM learns to maintain appropriate detail levels.

**Why This Matters**: Main documents stay navigable; complexity extracted to separate files.

### 6. Test-First Thinking

**Plan Template File Creation Order**:

```markdown
### File Creation Order

1. Create `contracts/` with API specifications
2. Create test files in order: contract → integration → e2e → unit
3. Create source files to make tests pass
```

**Effect**: Ensures LLM thinks about testability and contracts before implementation.

**Why This Matters**: Leads to more robust, verifiable specifications.

### 7. Preventing Speculative Features

**Template Validation**:

```markdown
- [ ] No speculative or "might need" features
- [ ] All phases have clear prerequisites and deliverables
```

**Effect**: Stops LLM from adding "nice to have" features that complicate implementation.

**Why This Matters**: Every feature must trace back to concrete user story with clear acceptance criteria.

---

## Execution Flow as Pseudocode

Templates contain **executable instructions** for Claude:

```markdown
## Execution Flow (main)
```

1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)

```

```

This isn't documentation—it's **instructions for Claude to execute**. Claude follows this pseudocode step-by-step, reporting progress in the "Execution Status" checklist.

---

## Placeholder System

Four types of placeholders control information flow:

| Placeholder Type      | Example                                    | When Filled                        | Purpose                |
| --------------------- | ------------------------------------------ | ---------------------------------- | ---------------------- |
| Template variables    | `[FEATURE]`, `[DATE]`                      | During command execution by Claude | Dynamic content        |
| Uncertainty markers   | `[NEEDS CLARIFICATION: specific question]` | User clarification via `/clarify`  | Prevent hallucination  |
| Script interpolation  | `{SCRIPT}`, `$ARGUMENTS`                   | Runtime by command invocation      | Script execution paths |
| Environment variables | `${SPECIFY_FEATURE}`                       | Bash script execution              | Context passing        |

### Critical Rule: Never Guess

`[NEEDS CLARIFICATION]` markers are **never guessed**. If information is missing, Claude must mark it explicitly.

**Example Workflow**:

1. User: `/specify add user authentication`
2. Claude creates spec with: `[NEEDS CLARIFICATION: auth method not specified]`
3. User runs: `/clarify` → sees question
4. User provides: `use email/password with password reset`
5. Claude updates spec with concrete requirement

This prevents the most common LLM failure mode: hallucinating plausible but incorrect details.

---

## How Constraints Prevent Hallucination

### Problem: Unconstrained Generation

Without templates, LLMs operate in maximum entropy mode:

- Fill every ambiguity with "reasonable" assumptions
- Add features based on common patterns
- Jump to implementation details prematurely
- Mix abstraction levels inconsistently

### Solution: Constraint Layering

**Layer 1: Template Structure**

- Fixed sections enforce information architecture
- Checklists create systematic review points
- Examples demonstrate correct patterns

**Layer 2: Explicit Instructions**

- "Mark ambiguities, don't guess"
- "Focus on WHAT, not HOW"
- "No speculative features"

**Layer 3: Constitutional Gates**

- Simplicity gate: justify complexity
- Anti-abstraction gate: justify layers
- Testability gate: define success criteria

**Layer 4: Execution Flow**

- Step-by-step pseudocode
- Error conditions for invalid states
- Success criteria for completion

**Result**: Output space reduced from infinite probabilistic text to finite set of valid architectural documents.

---

## Cross-References

**How templates are processed**: [AI Patterns](09-ai-patterns.md)
**Commands using templates**: [Commands: Core](04-commands-core.md)
**Template engine design**: [Architecture](03-architecture.md)
**Why constraints work**: [Philosophy](02-philosophy.md)
**Clarification workflow**: [Commands: Clarify](05-commands-clarify.md)

**Navigation**: [← Commands: Clarify](05-commands-clarify.md) | [Bash Automation →](07-bash-automation.md)

---

## Keywords

templates as constraints, reduction functions, execution flows, [NEEDS CLARIFICATION], placeholder system, uncertainty markers, constitutional gates, checklist-driven validation, hallucination prevention, constraint layering, test-first thinking, abstraction levels, hierarchical detail management
