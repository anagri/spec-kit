# Spec-Kit Overview

**Purpose**: High-level introduction to spec-kit's core concepts, key characteristics, and navigation guidance.

**Target Audience**: Tech experts familiar with agile and TDD, new to AI-assisted specification-driven development.

**Related Files**:

- [Philosophy](02-philosophy.md) - Deep dive into SDD paradigm
- [Architecture](03-architecture.md) - Technical implementation details
- [Commands](04-commands-core.md) - Workflow execution

**Keywords**: spec-kit, SDD, specifications as code, Claude Code, AI coding assistants, template-driven development

---

## What is Spec-Kit?

Spec-kit is a sophisticated toolkit that fundamentally inverts the traditional software development paradigm by making **specifications the executable source of truth** rather than documentation artifacts.

Forked from `github/spec-kit` and optimized specifically for solo developers using Claude Code on Unix-like systems, it embodies a complete methodology for Specification-Driven Development (SDD) with AI coding assistants.

**Project Repository**: https://github.com/anagri/spec-kit

---

## Key Characteristics

| Aspect             | Description                                                                    |
| ------------------ | ------------------------------------------------------------------------------ |
| **Paradigm**       | Specifications generate code, not vice versa                                   |
| **Target**         | Solo developers using Claude Code (macOS, Linux, WSL)                          |
| **Architecture**   | 4-layer separation model (CLI → Templates → Scripts → Constitution)            |
| **Workflow**       | 8-command sequence enforcing phase discipline                                  |
| **Philosophy**     | Constraint-driven generation through templates as compiler directives          |
| **Implementation** | Python CLI + Markdown templates + Bash automation + Constitutional enforcement |

---

## Core Innovation

The toolkit treats AI coding assistants (specifically Claude Code) not as creative code generators but as **disciplined specification engineers**.

Through carefully crafted templates with embedded execution flows, it constrains the vast output space of LLMs to produce:

- **Architecturally consistent** implementations
- **Testable** specifications
- **Maintainable** codebases
- **Predictable** outcomes

### The Constraint Mechanism

```
Unconstrained LLM: 10^n possible outputs (hallucination-prone)
         ↓
Apply template with execution flow
         ↓
Constrained outputs: 10^3 (valid)
         ↓
Apply constitutional gates
         ↓
Acceptable outputs: 10^1 (enforced)
```

---

## Quick Architecture Overview

Spec-kit uses a strict **4-layer separation model**:

### Layer 1: CLI Orchestrator

- **Technology**: Python 3.11+ with Typer and Rich
- **Purpose**: Bootstrap projects with templates from GitHub releases
- **Location**: `src/specify_cli/__init__.py`
- **Commands**: `speclaude init`, `speclaude check`

### Layer 2: Template Engine

- **Technology**: Markdown files with YAML frontmatter
- **Purpose**: Executable specifications that guide Claude Code
- **Location**: `.specify/templates/`, `.claude/commands/`
- **Key Feature**: Execution flow pseudocode for deterministic AI behavior

### Layer 3: State Automation

- **Technology**: Bash scripts with JSON output
- **Purpose**: Filesystem operations and state management
- **Location**: `.specify/scripts/bash/`
- **Key Feature**: JSON communication contracts for stateless AI interaction

### Layer 4: Constitutional Enforcement

- **Technology**: Markdown governance document
- **Purpose**: Runtime validation of architectural principles
- **Location**: `.specify/memory/constitution.md`
- **Key Feature**: Gates that enforce design constraints

**Deep dive**: [Architecture](03-architecture.md)

---

## 8-Command Workflow

Spec-kit enforces phase discipline through 8 slash commands:

```
/constitution [required, once per project]
     │
     ├─> /clarify-constitution [optional, if markers exist]
     │
     ↓
/specify [required, per feature]
     │
     ├─> /clarify [optional but recommended]
     │
     ↓
/plan [required, per feature]
     ↓
/tasks [required, per feature]
     │
     ├─> /analyze [optional but recommended]
     │
     ↓
/implement [required, per feature]
```

### Core Commands

| Command           | Purpose                                              | Output                                    |
| ----------------- | ---------------------------------------------------- | ----------------------------------------- |
| **/constitution** | Create project governance principles                 | `.specify/memory/constitution.md`         |
| **/specify**      | Generate feature specification from natural language | `specs/###-feature-name/spec.md`          |
| **/plan**         | Create implementation plan with tech stack decisions | `plan.md`, `research.md`, `data-model.md` |
| **/tasks**        | Break down plan into actionable tasks                | `tasks.md` with dependencies              |
| **/implement**    | Execute tasks to generate code                       | Working implementation                    |

### Enhancement Commands

| Command                   | Purpose                             | When to Use                            |
| ------------------------- | ----------------------------------- | -------------------------------------- |
| **/clarify**              | Resolve specification ambiguities   | After `/specify`, before `/plan`       |
| **/analyze**              | Validate cross-artifact consistency | After `/tasks`, before `/implement`    |
| **/clarify-constitution** | Resolve governance ambiguities      | After `/constitution` if markers exist |

**Detailed reference**: [Commands: Core](04-commands-core.md), [Commands: Clarify](05-commands-clarify.md)

---

## Key Concepts at a Glance

### Power Inversion

Traditional development: **Code is truth, specs are documentation**
Spec-kit approach: **Specs are truth, code is generated artifact**

Result: Specifications don't drift; code is regenerated when specs evolve.

**Learn more**: [Philosophy](02-philosophy.md)

### Templates as Constraints

Templates are not passive documentation—they are **executable instructions** containing:

- YAML frontmatter (metadata)
- Execution flow pseudocode (step-by-step instructions for Claude)
- Validation gates (constitutional enforcement)
- Placeholder system (`[NEEDS CLARIFICATION]` markers)

**Learn more**: [Templates](06-templates.md)

### [NEEDS CLARIFICATION] Markers

Instead of guessing missing information, Claude explicitly marks uncertainties:

```markdown
- FR-006: System MUST authenticate users via [NEEDS CLARIFICATION: auth method - email/password, SSO, OAuth?]
```

This prevents hallucination and forces explicit decision-making before implementation.

**Learn more**: [AI Patterns](09-ai-patterns.md)

### Constitutional Gates

Before each phase, Claude validates compliance with project principles:

```markdown
### Library-First Gate (Principle I)

- [ ] Feature begins as standalone library?
- [ ] Clear library boundaries defined?
```

Violations must be justified in a Complexity Tracking table or the design must be refactored.

**Learn more**: [Constitution](08-constitution.md)

### Solo Developer Workflow

Unlike upstream `github/spec-kit`, this fork optimizes for solo developers:

- **No git branch creation** (work directly on main)
- **Environment variable context** (`SPECIFY_FEATURE`)
- **Monorepo support** (`.specify` priority over `.git`)
- **Simplified automation** (no multi-agent logic)

**Learn more**: [Architecture](03-architecture.md), [Bash Automation](07-bash-automation.md)

---

## What Makes Spec-Kit Different?

### Compared to Traditional Development

| Traditional                          | Spec-Kit                                |
| ------------------------------------ | --------------------------------------- |
| Specs drift from code over time      | Specs generate code; no drift possible  |
| Documentation is an afterthought     | Specifications are the primary artifact |
| Code reviews focus on implementation | Reviews focus on specification quality  |
| Refactoring risks breaking behavior  | Regenerate from updated specs           |
| Testing validates implementation     | Testing validates specifications        |

**Detailed comparison**: [Insights](11-insights.md)

### Compared to Other AI Tools

| Other AI Tools                                | Spec-Kit                                 |
| --------------------------------------------- | ---------------------------------------- |
| Unconstrained generation (hallucination risk) | Template-constrained generation          |
| No architectural enforcement                  | Constitutional gates enforce principles  |
| Ad-hoc workflows                              | Structured 8-command sequence            |
| Implementation-first                          | Specification-first                      |
| Opaque AI decisions                           | Explicit `[NEEDS CLARIFICATION]` markers |

---

## Quick Start Guide

### For First-Time Readers

**Minimal path** (30 minutes):

1. Read this overview
2. Read [Philosophy](02-philosophy.md) - understand the paradigm shift
3. Read [Workflows](10-workflows.md) - see practical examples

**Implementation path** (2-3 hours):

1. This overview
2. [Architecture](03-architecture.md) - technical details
3. [Commands: Core](04-commands-core.md) - main workflow
4. [Templates](06-templates.md) - constraint mechanisms
5. [Bash Automation](07-bash-automation.md) - script details

**Deep understanding** (4-5 hours):
Read all documents in sequence 01-11.

### For Specific Topics

Use the [README](README.md) **Quick Lookup by Concept** section.

---

## When to Use Spec-Kit

### Ideal Use Cases

✅ **Solo developers** working on new features or projects
✅ **AI-assisted development** with Claude Code as primary tool
✅ **Specification-first workflows** where clarity upfront saves time
✅ **Iterative refinement** of complex requirements
✅ **Architectural consistency** across multiple features
✅ **Test-driven development** with contract-first approach

### Not Ideal For

❌ **Large teams** with parallel development (fork optimized for solo devs)
❌ **Non-Claude AI tools** (fork hardcoded for Claude Code)
❌ **Windows-first environments** (bash scripts require Unix-like systems)
❌ **Quick prototypes** where specs are overkill
❌ **Legacy codebases** without spec-first culture

---

## File Locations Reference

Once spec-kit is installed in a project:

```
project-root/
├── .specify/                        # Installed templates & scripts
│   ├── templates/
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   └── tasks-template.md
│   ├── scripts/bash/
│   │   ├── common.sh
│   │   ├── create-new-feature.sh
│   │   ├── check-prerequisites.sh
│   │   └── update-agent-context.sh
│   └── memory/
│       └── constitution.md          # Project governance
│
├── .claude/                         # Claude Code integration
│   ├── commands/                    # Slash commands
│   │   ├── constitution.md
│   │   ├── specify.md
│   │   ├── clarify.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── implement.md
│   │   ├── analyze.md
│   │   └── clarify-constitution.md
│   └── CLAUDE.md                    # AI context (auto-updated)
│
└── specs/                           # Feature specifications
    ├── 001-feature-name/
    │   ├── spec.md                  # Requirements
    │   ├── plan.md                  # Implementation plan
    │   ├── tasks.md                 # Task breakdown
    │   ├── research.md              # Tech decisions
    │   ├── data-model.md            # Entities
    │   ├── quickstart.md            # Integration tests
    │   └── contracts/               # API specs
    ├── 002-another-feature/
    └── ...
```

**Deep dive**: [Architecture](03-architecture.md), [Bash Automation](07-bash-automation.md)

---

## Example: End-to-End Workflow

### User Goal

Build a real-time chat feature with message history.

### Spec-Kit Workflow

```bash
# 1. Define project principles (once per project)
/constitution "Library-first architecture, CLI interfaces, TDD mandatory"
# → Creates .specify/memory/constitution.md

# 2. Specify the feature (natural language)
/specify "Real-time chat system with message history"
# → Creates specs/003-real-time-chat/spec.md
# → Marks ambiguities: [NEEDS CLARIFICATION: latency target?]

# 3. Clarify ambiguities (interactive)
/clarify
# → Q1: "What is expected message delivery latency?"
# → User: "< 100ms p95"
# → Updates spec.md with concrete requirement

# 4. Plan implementation (with tech context)
/plan "Python 3.11, FastAPI, PostgreSQL, 10k concurrent users"
# → Creates plan.md, research.md, data-model.md, contracts/
# → Validates constitutional gates (Library-First, Test-First)

# 5. Generate tasks
/tasks
# → Creates tasks.md with dependencies
# → T001: Contract tests [P] (parallel-safe)
# → T002: Create Message model [P]
# → T010: Implement POST /messages (sequential)

# 6. Analyze consistency (optional)
/analyze
# → Validates requirements have task coverage
# → Checks constitution compliance
# → Reports gaps or conflicts

# 7. Implement
/implement
# → Executes tasks in dependency order
# → Tests before implementation (TDD)
# → Marks tasks complete in tasks.md
```

**Full workflow details**: [Workflows](10-workflows.md)

---

## Next Steps

### To Understand Philosophy

→ [Philosophy](02-philosophy.md) - Why specifications as truth matters

### To Learn Architecture

→ [Architecture](03-architecture.md) - How the 4 layers work together

### To Use Commands

→ [Commands: Core](04-commands-core.md) - Main workflow commands
→ [Commands: Clarify](05-commands-clarify.md) - Enhancement commands

### To See Examples

→ [Workflows](10-workflows.md) - Practical end-to-end scenarios

---

## Cross-References

**Related Concepts**:

- Paradigm shift: [Philosophy](02-philosophy.md)
- System design: [Architecture](03-architecture.md)
- Command workflows: [Commands: Core](04-commands-core.md)
- Template mechanics: [Templates](06-templates.md)
- Script automation: [Bash Automation](07-bash-automation.md)
- Governance: [Constitution](08-constitution.md)
- AI integration: [AI Patterns](09-ai-patterns.md)
- Practical usage: [Workflows](10-workflows.md)
- Design analysis: [Insights](11-insights.md)

**Navigation**: [← README](README.md) | [Philosophy →](02-philosophy.md)

---

## Keywords

- **Primary**: spec-kit, Specification-Driven Development, SDD, Claude Code, AI coding assistants
- **Architecture**: 4-layer model, CLI orchestrator, template engine, state automation, constitutional enforcement
- **Workflow**: 8 commands, /specify, /plan, /tasks, /implement, phase discipline
- **Mechanisms**: Templates as constraints, [NEEDS CLARIFICATION] markers, constitutional gates, JSON contracts
- **Features**: Solo developer workflow, monorepo support, dogfooding, power inversion
- **Technical**: Python CLI, Markdown templates, Bash automation, YAML frontmatter, execution flows
