# Spec Kit User Guide

**Version**: 1.0.0
**Last Updated**: 2025-10-17
**Project**: anagri/spec-kit (Claude Code Edition)
**Repository**: https://github.com/anagri/spec-kit

---

## Purpose

This user guide provides comprehensive documentation of Spec Kit from the **functional user perspective**. It documents:

- What users SEE (terminal output, file changes, progress indicators)
- What users DO (command invocations, inputs, decisions)
- What users GET (outcomes, artifacts, next steps)
- When and why to use each command
- Best practices for optimal results
- Troubleshooting for common issues

**Primary Audience**: AI coding assistants (Claude Code) using Spec Kit as a knowledge base for helping users with specification-driven development.

**Secondary Audience**: Developers learning Spec Kit workflows and command sequences.

---

## Navigation Guide

### For First-Time Users

**Start here if you're new to Spec Kit:**

1. **[Introduction & Getting Started](01-introduction.md)** - Installation, project setup, first feature journey
2. **[Command Flow & Decision Tree](02-command-flow.md)** - Understanding the 8-command workflow
3. **[Workflow Patterns](11-workflow-patterns.md)** - Choosing the right workflow variation

### Command Reference (In Workflow Order)

**Follow this sequence for your first feature:**

1. **[/constitution](03-constitution-command.md)** - Define project governance principles (once per project)
2. **[/clarify-constitution](04-clarify-constitution-command.md)** - Resolve governance ambiguities (optional)
3. **[/specify](05-specify-command.md)** - Create feature specification from natural language
4. **[/clarify](06-clarify-command.md)** - Resolve specification ambiguities (recommended)
5. **[/plan](07-plan-command.md)** - Generate implementation plan with constitutional validation
6. **[/tasks](08-tasks-command.md)** - Break down plan into actionable tasks with dependencies
7. **[/analyze](09-analyze-command.md)** - Validate consistency across artifacts (recommended)
8. **[/implement](10-implement-command.md)** - Execute tasks to generate working code

### Workflow & Troubleshooting

- **[Workflow Patterns & Best Practices](11-workflow-patterns.md)** - Workflow variations, best practices by phase, time estimates
- **[Troubleshooting & Error Recovery](12-troubleshooting.md)** - Common errors, recovery strategies, debugging tips

---

## Quick Reference Tables

### Command Summary

| Command | Purpose | Input Required | Time | Optional? |
|---------|---------|----------------|------|-----------|
| `/constitution` | Create project governance | Principles (4-6 recommended) | 30 min | Required (once) |
| `/clarify-constitution` | Resolve governance gaps | Interactive Q&A (max 5) | 5-15 min | If markers exist |
| `/specify` | Generate feature spec | Natural language description | 15-30 min | Required (per feature) |
| `/clarify` | Resolve spec ambiguities | Interactive Q&A (max 5) | 15-30 min | Recommended |
| `/plan` | Create implementation plan | Tech stack description | 1-2 hrs | Required (per feature) |
| `/tasks` | Generate task breakdown | None (reads from plan) | 15-30 min | Required (per feature) |
| `/analyze` | Validate consistency | None (reads all artifacts) | 10-15 min | Recommended |
| `/implement` | Execute implementation | None (reads tasks) | 2-8 hrs | Required (per feature) |

### Workflow Variations

| Workflow | Commands | Time | Risk | When to Use |
|----------|----------|------|------|-------------|
| **Minimal** | 5 core commands (skip clarify/analyze) | 2-4 hrs | Higher | Simple features, clear requirements |
| **Recommended** | 7 commands (include clarify/analyze) | 4-10 hrs | Lower | Complex features, production code |
| **Iterative** | Loop specify→clarify→plan until stable | 4-7 hrs | Medium | Exploratory features, emerging requirements |
| **Design-Only** | Stop after /tasks (no /implement) | 2-4 hrs | N/A | Estimation, feasibility analysis |

### Command Prerequisites

| Command | Requires | Creates | Next Command |
|---------|----------|---------|--------------|
| `/constitution` | .specify/ folder | constitution.md | /clarify-constitution or /specify |
| `/clarify-constitution` | constitution.md with markers | Updated constitution.md | /specify |
| `/specify` | None | spec.md | /clarify or /plan |
| `/clarify` | spec.md | Updated spec.md | /plan |
| `/plan` | spec.md, constitution.md | plan.md, research.md, data-model.md, contracts/, quickstart.md | /tasks |
| `/tasks` | plan.md | tasks.md | /analyze or /implement |
| `/analyze` | spec.md, plan.md, tasks.md | Analysis report | /implement |
| `/implement` | tasks.md, all artifacts | Working code | Review, test, commit |

---

## Reading Paths

### Quick Start (30-45 minutes)

**Goal**: Understand Spec Kit basics and run your first feature

1. [Introduction & Getting Started](01-introduction.md) - Installation and overview
2. [Command Flow & Decision Tree](02-command-flow.md) - Workflow understanding
3. [/specify Command](05-specify-command.md) - Start your first feature

### Implementation Path (2-3 hours)

**Goal**: Learn all commands and best practices

1. [Introduction & Getting Started](01-introduction.md)
2. [Command Flow & Decision Tree](02-command-flow.md)
3. [/constitution](03-constitution-command.md) → [/specify](05-specify-command.md) → [/clarify](06-clarify-command.md)
4. [/plan](07-plan-command.md) → [/tasks](08-tasks-command.md) → [/analyze](09-analyze-command.md) → [/implement](10-implement-command.md)
5. [Workflow Patterns](11-workflow-patterns.md)

### Deep Understanding (4-5 hours)

**Goal**: Master Spec Kit workflows and troubleshooting

Read all pages in sequence 01-12, then explore:
- [Knowledge Base](../kb/README.md) for technical details
- [PHILOSOPHY.md](../../docs/PHILOSOPHY.md) for architectural rationale

### Topic-Specific Reading

**By Problem**:
- Command errors → [Troubleshooting](12-troubleshooting.md)
- Choosing workflow → [Workflow Patterns](11-workflow-patterns.md)
- Understanding command sequence → [Command Flow](02-command-flow.md)

**By Phase**:
- Project setup → [Introduction](01-introduction.md), [/constitution](03-constitution-command.md)
- Requirements → [/specify](05-specify-command.md), [/clarify](06-clarify-command.md)
- Design → [/plan](07-plan-command.md)
- Execution → [/tasks](08-tasks-command.md), [/implement](10-implement-command.md)
- Quality → [/analyze](09-analyze-command.md), [Best Practices](11-workflow-patterns.md)

---

## Document Organization

Each page follows a consistent structure:

```markdown
# [Page Title]

## Overview / Purpose

## When to Use / Prerequisites

## What You'll See / User Action

## All Possible Outcomes

## Follow-up Actions

## Best Practices

## Common Issues / Troubleshooting

## Importance / Why It Matters

---

## References

**Sources Consulted**: [List of files with line numbers]
**Related Pages**: [Cross-references to other user guide pages]
```

### Page Lengths and Content Density

| Page | Size | Focus |
|------|------|-------|
| 01-introduction.md | ~770 lines | Project setup, first feature journey |
| 02-command-flow.md | ~650 lines | Workflow sequencing, decision trees |
| 03-constitution-command.md | ~580 lines | Governance setup, principles |
| 04-clarify-constitution-command.md | ~520 lines | Interactive governance clarification |
| 05-specify-command.md | ~560 lines | Feature specification creation |
| 06-clarify-command.md | ~750 lines | Interactive specification clarification |
| 07-plan-command.md | ~710 lines | Implementation planning, constitutional gates |
| 08-tasks-command.md | ~620 lines | Task breakdown with TDD enforcement |
| 09-analyze-command.md | ~950 lines | Consistency validation, 6 detection passes |
| 10-implement-command.md | ~680 lines | Code generation, phase execution |
| 11-workflow-patterns.md | ~580 lines | Workflow variations, best practices |
| 12-troubleshooting.md | ~650 lines | Error recovery, debugging |

**Total**: ~8,020 lines across 12 focused documents

---

## Key Concepts Quick Lookup

### Command Workflow

- **Required Core**: /constitution, /specify, /plan, /tasks, /implement
- **Enhancement**: /clarify-constitution, /clarify, /analyze
- **Sequence**: Must follow prerequisites (e.g., /plan requires /specify)

### Decision Points

1. **After /constitution**: Run /clarify-constitution if `[NEEDS CLARIFICATION]` markers exist
2. **After /specify**: Run /clarify if specification has ambiguities (highly recommended)
3. **After /tasks**: Run /analyze to validate consistency before /implement (recommended)

### Phase Separation

- **Constitution Phase**: Governance principles (WHAT principles govern architecture)
- **Specification Phase**: Requirements (WHAT users need, no tech stack)
- **Planning Phase**: Architecture (HOW to implement, tech decisions)
- **Task Phase**: Execution plan (WHEN to do each step, dependencies)
- **Implementation Phase**: Code generation (DO the work, TDD enforced)

### Key Features

- **[NEEDS CLARIFICATION] Markers**: Explicit uncertainty instead of hallucination
- **Constitutional Gates**: Pre-research and post-design validation in /plan
- **TDD Enforcement**: Tests written before implementation in /implement
- **Parallel Execution**: [P] markers enable concurrent task execution
- **Atomic Progress**: [X] markers in tasks.md enable resumption after interruption
- **State Management**: SPECIFY_FEATURE environment variable for feature switching

---

## Relationship to Knowledge Base

This **User Guide** complements the **[Knowledge Base](../kb/README.md)** with different focus:

| User Guide | Knowledge Base |
|------------|----------------|
| **Functional perspective** (what users see/do) | **Technical perspective** (how it works internally) |
| Command usage, inputs, outputs | Architecture, templates, scripts, implementation |
| Best practices, troubleshooting | Design patterns, AI integration, philosophy |
| Workflow sequences, decision trees | Constitutional enforcement, bash automation |
| **Primary audience**: Users and AI assistants helping users | **Primary audience**: Developers extending/modifying Spec Kit |

**Use User Guide when**:
- Learning how to use Spec Kit commands
- Understanding workflow sequences
- Troubleshooting command errors
- Choosing the right workflow variation

**Use Knowledge Base when**:
- Understanding Spec Kit's architecture
- Learning about template mechanics
- Extending Spec Kit with custom commands
- Understanding philosophical design decisions

---

## Usage Notes for AI Assistants

When helping users with Spec Kit:

1. **Start with user guide** for command usage, workflows, troubleshooting
2. **Reference knowledge base** for technical details, architecture, implementation
3. **Check prerequisites** before suggesting commands (see Command Prerequisites table)
4. **Recommend enhancements** (/clarify, /analyze) for complex features
5. **Point to troubleshooting** when users encounter errors
6. **Explain outcomes** using "All Possible Outcomes" sections from command pages
7. **Ground recommendations** in best practices from workflow patterns page

### Common User Questions

| Question | Point to |
|----------|----------|
| "How do I start?" | [01-introduction.md](01-introduction.md) |
| "What commands do I run?" | [02-command-flow.md](02-command-flow.md) |
| "Why did /plan fail?" | [07-plan-command.md](07-plan-command.md) then [12-troubleshooting.md](12-troubleshooting.md) |
| "Should I run /clarify?" | [06-clarify-command.md](06-clarify-command.md) |
| "What workflow should I use?" | [11-workflow-patterns.md](11-workflow-patterns.md) |
| "How do I fix this error?" | [12-troubleshooting.md](12-troubleshooting.md) |

---

## Document Stats

- **Total Pages**: 12
- **Total Lines**: ~8,020
- **Total Words**: ~80,000
- **Coverage**: All 8 commands + workflows + troubleshooting
- **Sources Referenced**: 50+ files (templates, scripts, knowledge base articles)
- **Examples Included**: 100+ (terminal outputs, error messages, resolutions)
- **Best Practices**: 50+ (distributed across command pages)

---

## Version History

### v1.0.0 (2025-10-17)

**Initial Release**:
- 12-page comprehensive user guide
- Complete command reference (8 commands)
- Workflow patterns and best practices
- Troubleshooting and error recovery
- Grounded in source files with line-level references
- Optimized for AI assistant consumption

---

## Future Enhancements

Planned additions to user guide:

1. **Real-World Examples**: Complete feature implementations (chat, payment, search)
2. **Video Walkthroughs**: Screencast references for visual learners
3. **Cheat Sheets**: One-page quick reference for each command
4. **Team Workflows**: Extended collaboration patterns for larger teams
5. **Integration Examples**: CI/CD, GitHub Actions, deployment pipelines

---

## Feedback and Contributions

This user guide is part of the spec-kit project. For issues or improvements:

- **Repository**: https://github.com/anagri/spec-kit
- **Issues**: https://github.com/anagri/spec-kit/issues
- **Documentation**: Located in `ai-docs/user-guide/`

---

**Navigation**: [Start Reading →](01-introduction.md) | [Knowledge Base →](../kb/README.md)
