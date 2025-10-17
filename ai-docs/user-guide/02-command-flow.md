# Command Flow & Decision Tree

**Purpose**: Visual guide to Spec Kit's command workflow with decision points and timing estimates
**Target Audience**: Users planning feature development workflows
**Related Pages**:
- [Getting Started](01-getting-started.md) - Installation and first steps
- [Command Reference](../kb/04-commands-core.md) - Detailed command documentation
- [Workflow Examples](../kb/10-workflows.md) - Complete end-to-end examples

---

## The 8-Command Workflow

Spec Kit enforces phase discipline through 8 slash commands organized into 2 categories:

**Core Commands (5)** - Required for complete workflow:
1. `/constitution` - Define project governance principles
2. `/specify` - Create feature specification
3. `/plan` - Generate implementation plan with design artifacts
4. `/tasks` - Break down plan into actionable tasks
5. `/implement` - Execute tasks to generate code

**Enhancement Commands (3)** - Optional but recommended:
- `/clarify-constitution` - Resolve governance ambiguities
- `/clarify` - Resolve specification ambiguities
- `/analyze` - Validate cross-artifact consistency

---

## Complete Command Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                      PROJECT INITIALIZATION                      │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                     ┌──────────────────┐
                     │  /constitution   │ [REQUIRED, once per project]
                     │  Define project  │ Time: 5-10 minutes
                     │   principles     │
                     └────────┬─────────┘
                              │
               ┌──────────────┴──────────────┐
               │  Has [NEEDS CLARIFICATION]? │
               └──────────────┬──────────────┘
                              │
                   ┌──────────┴──────────┐
                   │ YES                 │ NO
                   ▼                     ▼
    ┌──────────────────────────┐  [Continue to /specify]
    │ /clarify-constitution    │  [OPTIONAL]
    │ Resolve governance gaps  │  Time: 5-10 minutes
    │ Max 5 questions          │
    └──────────┬───────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FEATURE DEVELOPMENT                         │
└─────────────────────────────────────────────────────────────────┘
               │
               ▼
     ┌──────────────────┐
     │     /specify     │ [REQUIRED, per feature]
     │  Natural language│ Time: 10-15 minutes
     │  → Requirements  │
     └────────┬─────────┘
              │
┌─────────────┴─────────────┐
│ Has ambiguities/markers?  │
└─────────────┬─────────────┘
              │
    ┌─────────┴─────────┐
    │ YES               │ NO
    ▼                   ▼
┌──────────────────┐   [Continue to /plan]
│    /clarify      │   [OPTIONAL but RECOMMENDED]
│ Resolve spec gaps│   Time: 10-20 minutes
│ Max 5 questions  │   (5 min per question)
└────────┬─────────┘
         │
         ▼
  ┌──────────────────┐
  │      /plan       │ [REQUIRED]
  │ Tech stack +     │ Time: 15-30 minutes
  │ design artifacts │
  └────────┬─────────┘
           │
           │ [Constitutional gates validated 2x]
           │ [Outputs: plan.md, research.md, data-model.md, contracts/]
           │
           ▼
    ┌──────────────────┐
    │     /tasks       │ [REQUIRED]
    │ Task breakdown   │ Time: 10-20 minutes
    │ with dependencies│
    └────────┬─────────┘
             │
┌────────────┴────────────┐
│ Want consistency check? │
└────────────┬────────────┘
             │
   ┌─────────┴─────────┐
   │ YES               │ NO
   ▼                   ▼
┌────────────────┐   [Continue to /implement]
│   /analyze     │   [OPTIONAL but RECOMMENDED]
│ Coverage gaps, │   Time: 5-10 minutes
│ inconsistencies│
└───────┬────────┘
        │
        │ [Detects: duplication, ambiguity, coverage gaps, violations]
        │ [Read-only: no file modifications]
        │
        ▼
 ┌──────────────────┐
 │   /implement     │ [REQUIRED]
 │  Execute tasks   │ Time: 2-12 hours (feature-dependent)
 │  Generate code   │
 └──────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│                    FEATURE COMPLETE                              │
└──────────────────────────────────────────────────────────────────┘
```

---

## Required vs Optional Commands

### Core Commands (Required)

These 5 commands form the mandatory workflow path:

| Command | When | Output | Typical Time |
|---------|------|--------|--------------|
| `/constitution` | Once per project | `.specify/memory/constitution.md` | 5-10 min |
| `/specify` | Per feature | `specs/###-feature-name/spec.md` | 10-15 min |
| `/plan` | Per feature | `plan.md`, `research.md`, `data-model.md`, `contracts/` | 15-30 min |
| `/tasks` | Per feature | `tasks.md` (numbered tasks with dependencies) | 10-20 min |
| `/implement` | Per feature | Working code implementation | 2-12 hours |

**Total Minimal Time**: 2.5-13 hours per feature (specification to implementation)

### Enhancement Commands (Optional)

These 3 commands improve quality but can be skipped:

| Command | When | Benefit | Typical Time |
|---------|------|---------|--------------|
| `/clarify-constitution` | After `/constitution` if markers exist | Completes governance principles | 5-10 min |
| `/clarify` | After `/specify` before `/plan` | Resolves specification ambiguities | 10-20 min |
| `/analyze` | After `/tasks` before `/implement` | Catches consistency issues early | 5-10 min |

**Additional Time with Enhancements**: +20-40 minutes per feature

---

## Decision Points

### Decision 1: Run `/clarify-constitution`?

**Trigger**: After `/constitution` completes

```
IF constitution contains [NEEDS CLARIFICATION] markers
  THEN run /clarify-constitution
  - Resolves governance ambiguities
  - 5 questions max (multiple choice or short answer)
  - Time: 5-10 minutes

ELSE IF constitution has no markers
  THEN skip to /specify
  - Constitution is complete
  - Ready for feature development
```

**When to Skip**:
- No `[NEEDS CLARIFICATION]` markers present
- Constitution explicitly marked complete by `/constitution` command

**When to Run**:
- Constitution output shows "Incomplete Sections" warning
- Markers exist in Architectural Principles, Technology Stack, or Governance sections

---

### Decision 2: Run `/clarify`?

**Trigger**: After `/specify` completes

```
IF specification has ambiguities OR [NEEDS CLARIFICATION] markers
  AND feature is complex OR has NFRs
  THEN run /clarify (RECOMMENDED)
  - 5 questions max across 10 taxonomy categories
  - Time: 10-20 minutes (2-4 min per question)
  - Reduces downstream rework risk

ELSE IF requirements are simple AND well-understood
  THEN skip to /plan
  - Faster workflow
  - Higher risk of mid-implementation surprises
```

**When to Skip**:
- Simple, well-understood features (e.g., "Add a status field to existing model")
- No vague requirements ("fast", "scalable" without metrics)
- Solo developer confident in requirements

**When to Run**:
- Specification contains vague adjectives ("fast response time")
- Non-functional requirements lack metrics (latency, throughput, retention)
- Multiple `[NEEDS CLARIFICATION]` markers present
- Complex features with integration points

**Risk Trade-off**:
- Skip: Faster start (save 10-20 min), but may require backtracking during `/plan` or `/implement`
- Run: Slower start (invest 10-20 min), but clearer requirements reduce rework

---

### Decision 3: Run `/analyze`?

**Trigger**: After `/tasks` completes

```
IF feature is complex OR has 15+ tasks OR team environment
  THEN run /analyze (RECOMMENDED)
  - Detects coverage gaps, duplications, inconsistencies
  - Time: 5-10 minutes
  - Catches issues before expensive implementation phase

ELSE IF feature is simple AND <10 tasks AND high confidence
  THEN skip to /implement
  - Faster workflow for well-understood features
```

**When to Skip**:
- Simple features with <10 tasks
- Solo developer with high confidence in task breakdown
- Rapid prototyping scenarios

**When to Run**:
- Feature has 15+ tasks
- Multiple integration points
- Team environment (spec review required)
- Non-functional requirements (performance, security)
- First time using spec-kit (learn coverage validation)

**What /analyze Detects** (6 detection passes):
1. **Duplication**: Near-duplicate requirements
2. **Ambiguity**: Vague adjectives, unresolved placeholders
3. **Underspecification**: Requirements missing measurable outcomes
4. **Constitution Alignment**: Violations of MUST principles
5. **Coverage Gaps**: Requirements with zero tasks, tasks with no requirement
6. **Inconsistency**: Terminology drift, conflicting requirements

**Read-Only**: Never modifies files; only reports findings

---

## Workflow Variations

### Minimal Workflow (5 Commands)

**Path**: `/constitution` → `/specify` → `/plan` → `/tasks` → `/implement`

**Characteristics**:
- **Time**: 2-4 hours (simple features)
- **Risk**: Higher (ambiguities not resolved, consistency not validated)
- **Best For**:
  - Simple CRUD operations
  - Well-understood requirements
  - Solo developer with domain expertise
  - Rapid prototyping

**Example Use Case**: Adding a "status" field to an existing entity with basic filtering

---

### Recommended Workflow (7 Commands)

**Path**: `/constitution` → `/specify` → `/clarify` → `/plan` → `/tasks` → `/analyze` → `/implement`

**Characteristics**:
- **Time**: 3-6 hours (complex features)
- **Risk**: Lower (ambiguities resolved early, consistency validated)
- **Best For**:
  - Complex features with integration points
  - Features with NFRs (performance, security)
  - Team environments
  - Production-critical systems

**Example Use Case**: Building a real-time chat system with message history, presence tracking, and performance requirements

---

### Iterative Refinement Workflow

**Initial Exploration**:
```
/constitution → /specify → /clarify → /plan
[Review plan, realize requirements incomplete]
```

**Refinement Loop** (repeat as needed):
```
/specify [update description with new insights]
  ↓
/clarify [new questions emerge]
  ↓
/plan [regenerate with updated requirements]
  ↓
[Review again]
```

**Final Execution**:
```
/tasks → /analyze → /implement
```

**Characteristics**:
- **Time**: 4-8 hours (iterative discovery)
- **Best For**:
  - Exploratory features where requirements emerge through design
  - Novel domains with high uncertainty
  - Learning new technologies

**Example Use Case**: Designing a distributed tracing system for microservices (requirements clarify through research and planning iterations)

---

## Time Estimates

### Per Command (Typical)

| Phase | Command | Preparation | Execution | Review | Total |
|-------|---------|-------------|-----------|--------|-------|
| **Setup** | `/constitution` | 5 min | 3 min | 2 min | **10 min** |
| - | `/clarify-constitution` | - | 5-10 min | - | **5-10 min** |
| **Specify** | `/specify` | 5 min | 5 min | 5 min | **15 min** |
| - | `/clarify` | - | 10-20 min | - | **10-20 min** |
| **Design** | `/plan` | 5 min | 15-25 min | 5 min | **25-35 min** |
| **Tasks** | `/tasks` | - | 10-15 min | 5 min | **15-20 min** |
| - | `/analyze` | - | 5-10 min | - | **5-10 min** |
| **Implement** | `/implement` | - | 2-12 hours | - | **2-12 hours** |

**Notes**:
- Preparation: Reading previous artifacts, gathering context
- Execution: Claude processing command
- Review: User validation of output

### By Workflow Type

| Workflow | Commands | Spec-to-Code Time | Implementation Time | Total Time |
|----------|----------|-------------------|---------------------|------------|
| **Minimal** | 5 core | 60-80 min | 2-4 hours | **3-5 hours** |
| **Recommended** | 7 (with clarify/analyze) | 85-125 min | 2-4 hours | **3.5-6 hours** |
| **Iterative** | 7+ (with loops) | 120-180 min | 2-4 hours | **4-7 hours** |

**Feature Complexity Multipliers**:
- Simple (CRUD): 1x base time
- Moderate (API with 3-5 endpoints): 1.5x base time
- Complex (real-time system, integrations): 2-3x base time

---

## Prerequisites & Gates

### Command Prerequisites

Each command validates prerequisites before execution:

| Command | Requires | Validated By |
|---------|----------|--------------|
| `/constitution` | None (project init) | - |
| `/clarify-constitution` | Constitution with markers | Checks `.specify/memory/constitution.md` |
| `/specify` | Constitution complete | Reads constitution for context |
| `/clarify` | Specification exists | Checks `specs/###-name/spec.md` |
| `/plan` | Specification exists | `setup-plan.sh` validates spec.md |
| `/tasks` | Plan exists | `check-prerequisites.sh` validates plan.md |
| `/analyze` | Tasks exist | `check-prerequisites.sh --require-tasks` |
| `/implement` | Tasks exist | `check-prerequisites.sh --require-tasks` |

**Enforcement**: Bash scripts with `--json` output provide structured validation

---

### Constitutional Gates (in `/plan`)

The `/plan` command validates against constitution **twice**:

**Pre-Research Gate** (before Phase 0):
```markdown
## Constitution Check

_GATE: Must pass before Phase 0 research._

### Library-First Gate (Principle I)
- [ ] Feature begins as standalone library?
- [ ] Clear library boundaries defined?

[Additional gates for each principle...]

**Result**: PASS / FAIL
```

**Post-Design Gate** (after Phase 1):
```markdown
_GATE: Re-evaluate after Phase 1 design._

[Same checklist repeated]

**Result**: PASS / FAIL (with new violations caught)
```

**Failure Handling**:
- PASS: Continue to next phase
- FAIL: Document in Complexity Tracking table OR refactor design

**Complexity Tracking Example**:
```markdown
| Principle Violation | Justification | Mitigation | Accepted? |
|---------------------|---------------|------------|-----------|
| Skipping library boundary (Principle I) | WebSocket requires tight FastAPI coupling | Extract protocol layer in Phase 2 | ✓ Deferred |
```

---

## Phase Boundaries (Why Separation Matters)

Spec Kit enforces strict phase separation to prevent premature decisions:

### Phase 1: Specification (WHAT)
**Commands**: `/constitution`, `/specify`, `/clarify`

**Purpose**: Define requirements and constraints
**Constraints**:
- NO technical decisions (frameworks, databases)
- NO task breakdown
- NO implementation details

**Output**: `spec.md` with functional/non-functional requirements

**Boundary Rule**: Specifications describe WHAT the feature does, not HOW

---

### Phase 2: Design (HOW)
**Commands**: `/plan`

**Purpose**: Make technical decisions and generate design artifacts
**Constraints**:
- NO task generation (described but not created)
- NO implementation (design only)

**Outputs**:
- `plan.md` - Implementation strategy
- `research.md` - Technology decisions with rationale
- `data-model.md` - Entities, fields, relationships
- `contracts/` - API specifications (OpenAPI/GraphQL)
- `quickstart.md` - Integration test scenarios

**Boundary Rule**: Design specifies HOW the feature is built, not WHEN/WHO

---

### Phase 3: Task Breakdown (WHEN)
**Commands**: `/tasks`, `/analyze`

**Purpose**: Break design into executable tasks with dependencies
**Constraints**:
- NO implementation (tasks describe work, don't perform it)

**Output**: `tasks.md` with numbered tasks (T001-T0XX), dependencies, parallel markers

**Boundary Rule**: Tasks define execution order and dependencies, not actual implementation

---

### Phase 4: Implementation (DO)
**Commands**: `/implement`

**Purpose**: Execute tasks to generate code
**Constraints**:
- Follow TDD order (tests before implementation)
- Respect dependencies (sequential vs parallel)

**Output**: Working code matching specifications

**Boundary Rule**: Implementation follows task plan without deviating from design

---

### Why Strict Separation?

**Referential Transparency**: Same inputs produce same outputs at each phase
- Re-running `/plan` with same spec generates consistent design
- Re-running `/tasks` with same plan generates consistent task breakdown

**Prevents Premature Optimization**:
- Can't choose database in `/specify` (no technical context)
- Can't write code in `/plan` (design phase only)

**Enables Iteration**:
- Update spec → regenerate plan → regenerate tasks → regenerate code
- Each phase independent, no cross-contamination

**Reduces Cognitive Load**:
- Focus on one concern per phase (requirements, design, tasks, code)

---

## Decision Tree Summary

```
START: User wants to build a feature
  │
  ▼
[Q1] Is constitution complete?
  YES → Skip to [Q2]
  NO → Run /constitution
    ▼
    Is output complete?
      YES → Continue to [Q2]
      NO → Run /clarify-constitution
  │
  ▼
[Q2] Run /specify with feature description
  │
  ▼
[Q3] Are requirements clear and measurable?
  YES → Skip to [Q4]
  NO → Run /clarify (5 questions max)
    ▼
    Coverage report shows ≥80% resolved?
      YES → Continue to [Q4]
      NO → Run /clarify again OR proceed with risk
  │
  ▼
[Q4] Run /plan with tech stack
  │
  ▼
  Constitutional gates pass?
    NO → Refactor design OR justify in Complexity Tracking
    YES → Continue to [Q5]
  │
  ▼
[Q5] Run /tasks for task breakdown
  │
  ▼
[Q6] Is feature complex (≥15 tasks) OR team environment?
  YES → Run /analyze
    ▼
    Critical issues found?
      YES → Fix issues (add tasks, resolve conflicts)
      NO → Continue to [Q7]
  NO → Skip to [Q7]
  │
  ▼
[Q7] Run /implement
  │
  ▼
END: Feature complete (code + tests passing)
```

---

## References

### Source Files

**Command Documentation**:
- `ai-docs/kb/04-commands-core.md` - Core command reference (lines 1-1053)
  - `/constitution`: Lines 38-147
  - `/specify`: Lines 150-299
  - `/plan`: Lines 302-585
  - `/tasks`: Lines 587-759
  - `/implement`: Lines 762-981
  - Dependency graph: Lines 984-1023

- `ai-docs/kb/05-commands-clarify.md` - Enhancement commands (lines 1-682)
  - `/clarify`: Lines 28-285 (10 taxonomy categories, 5-question limit)
  - `/analyze`: Lines 287-525 (6 detection passes, read-only)
  - `/clarify-constitution`: Lines 527-651

**Workflow Examples**:
- `ai-docs/kb/10-workflows.md` - End-to-end scenarios (lines 1-941)
  - Complete workflow: Lines 16-599 (real-time chat example)
  - Workflow variations: Lines 602-674 (minimal, recommended, iterative)
  - Time estimates: Lines 605-639
  - Team collaboration: Lines 679-775

**Command Templates**:
- `templates/commands/constitution.md` - Constitution creation flow (lines 1-116)
- `templates/commands/specify.md` - Specification generation (lines 1-22)
- `templates/commands/clarify.md` - Interactive clarification (lines 1-159)
- `templates/commands/plan.md` - Implementation planning (lines 1-44)
- `templates/commands/tasks.md` - Task breakdown (lines 1-62)
- `templates/commands/analyze.md` - Consistency analysis (lines 1-102)
- `templates/commands/implement.md` - Task execution (lines 1-57)
- `templates/commands/clarify-constitution.md` - Constitution clarification (lines 1-184)

**Overview Context**:
- `ai-docs/kb/01-overview.md` - High-level workflow summary (lines 105-145)

### Key Insights

**Phase Separation** (from 04-commands-core.md:26-34):
- `/specify` creates spec.md with NO technical decisions
- `/plan` adds design artifacts with NO task breakdown
- `/tasks` creates tasks.md without executing implementation
- `/implement` executes tasks following TDD order

**Time Estimates** (from 10-workflows.md):
- Minimal workflow: 2-4 hours (5 commands)
- Recommended workflow: 3-6 hours (7 commands, +30-60 min for clarify/analyze)
- Iterative workflow: 4-8 hours (with spec-clarify-plan loops)

**Enhancement Commands** (from 05-commands-clarify.md):
- `/clarify`: Maximum 5 questions, 10 taxonomy categories, 10-20 min
- `/analyze`: Read-only validation, 6 detection passes, 5-10 min
- `/clarify-constitution`: Maximum 5 questions, 4 taxonomy categories, 5-10 min

**Constitutional Gates** (from 04-commands-core.md:356-367):
- Enforced twice: pre-research (before Phase 0) and post-design (after Phase 1)
- Failures require Complexity Tracking table with justification
- MUST principles are non-negotiable (refactor design or document exception)

---

**Navigation**: [← Getting Started](01-getting-started.md) | [Best Practices →](03-best-practices.md)
