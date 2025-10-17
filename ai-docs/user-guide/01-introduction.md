# Introduction & Getting Started

Spec Kit is a toolkit for **Specification-Driven Development (SDD)** that inverts the traditional development paradigm. Instead of writing code and treating specifications as documentation artifacts, Spec Kit makes **specifications the executable source of truth** that directly generate working implementations through AI assistance.

This guide walks you through installation, project setup, and your first feature journey using Claude Code as your AI coding assistant.

---

## What is Spec Kit?

Spec Kit fundamentally changes how you build software by making specifications executable. In traditional development, code is king and specifications drift over time. With Spec Kit:

- **Specifications generate code**, not vice versa
- **Code becomes disposable** - regenerate it when specs evolve
- **Ambiguities are marked explicitly** with `[NEEDS CLARIFICATION]` to prevent AI hallucination
- **Constitutional gates enforce** architectural principles throughout development
- **8-command workflow** provides structured, phase-separated development

### Target Audience

Spec Kit is optimized for **solo developers** using **Claude Code** on **Unix-like systems** (macOS, Linux, WSL). It works best for:

- Specification-first workflows where clarity upfront saves time
- AI-assisted development with Claude Code as primary tool
- Projects requiring architectural consistency across features
- Test-driven development with contract-first approach

### Not Ideal For

Spec Kit has intentional constraints. It's **not designed** for:

- Large teams with parallel development (optimized for solo devs)
- Non-Claude AI tools (hardcoded for Claude Code)
- Windows-first environments without WSL/Git Bash
- Quick prototypes where specifications are overkill
- Legacy codebases without spec-first culture

---

## Installation

### Prerequisites

Before installing, ensure you have:

- **macOS** or **Linux** (Windows users: use WSL2 or Git Bash)
- **[Claude Code](https://www.anthropic.com/claude-code)** - AI coding assistant
- **[uv](https://docs.astral.sh/uv/)** - Python package manager
- **Python 3.11+**
- **Git** (optional - Spec Kit works in `--no-git` mode)

### Install Specify CLI

**Option 1: Persistent Installation (Recommended)**

Install once and use everywhere:

```bash
uv tool install specify-cli --from git+https://github.com/anagri/spec-kit.git
```

After installation, the `speclaude` command is available in your PATH:

```bash
speclaude init my-project
speclaude check
```

**Option 2: One-time Usage**

Run directly without installing:

```bash
uvx --from git+https://github.com/anagri/spec-kit.git specify-cli init my-project
```

**Verification**

Check that prerequisites are installed:

```bash
speclaude check
```

**Expected output:**
```
✓ git found (version 2.x.x)
✓ claude found (Claude Code CLI)
```

---

## Project Initialization

### Basic Initialization

Create a new project with Spec Kit structure:

```bash
speclaude init my-project
cd my-project
```

**What happens:**
1. Downloads templates from latest GitHub release (`anagri/spec-kit`)
2. Creates `.specify/` directory (templates, scripts, constitution template)
3. Creates `.claude/` directory (8 slash commands)
4. Creates `specs/` directory (for feature specifications)
5. Initializes git repository (unless `--no-git` flag used)
6. Sets executable permissions on bash scripts

### Initialize in Current Directory

Work in an existing directory:

```bash
# Using dot notation
speclaude init .

# Using --here flag
speclaude init --here

# Force merge into non-empty directory without confirmation
speclaude init . --force
```

### Common Options

| Option | Description |
|--------|-------------|
| `--ignore-agent-tools` | Skip Claude Code CLI check (useful during development) |
| `--no-git` | Skip git repository initialization |
| `--here` | Initialize in current directory |
| `--force` | Skip confirmation when directory has existing files |
| `--debug` | Enable detailed output for troubleshooting |
| `--github-token <token>` | GitHub token for API requests (or set `GITHUB_TOKEN` env var) |
| `--local <path>` | Use local spec-kit repository for template development |

---

## Project Structure After Init

After running `speclaude init`, your project has this structure:

```
my-project/
├── .specify/                        # Spec Kit installation
│   ├── memory/
│   │   └── constitution.md          # Template for project governance
│   ├── templates/
│   │   ├── spec-template.md         # Feature specification template
│   │   ├── plan-template.md         # Implementation plan template
│   │   ├── tasks-template.md        # Task breakdown template
│   │   └── agent-file-template.md   # CLAUDE.md template
│   └── scripts/bash/
│       ├── common.sh                # Shared utilities
│       ├── create-new-feature.sh    # Feature directory creation
│       ├── setup-plan.sh            # Plan phase setup
│       ├── update-agent-context.sh  # CLAUDE.md updates
│       └── check-prerequisites.sh   # Validates context
│
├── .claude/                         # Claude Code integration
│   └── commands/                    # Slash commands
│       ├── constitution.md          # /constitution command
│       ├── specify.md               # /specify command
│       ├── clarify.md               # /clarify command
│       ├── clarify-constitution.md  # /clarify-constitution command
│       ├── plan.md                  # /plan command
│       ├── tasks.md                 # /tasks command
│       ├── analyze.md               # /analyze command
│       └── implement.md             # /implement command
│
├── specs/                           # Feature specifications (created during workflow)
│   └── (empty initially)
│
└── .git/                            # Git repository (unless --no-git)
```

### Key Directories

**`.specify/`** - Core Spec Kit installation containing templates, scripts, and constitution template downloaded from GitHub releases. These files guide Claude Code through the workflow.

**`.claude/`** - Claude Code integration with 8 slash commands that become available in your Claude Code session. These commands orchestrate the spec-driven workflow.

**`specs/`** - Feature specifications created during development. Each feature gets a sequentially numbered directory (001-feature-name, 002-another-feature) containing spec.md, plan.md, tasks.md, and supporting artifacts.

---

## Your First Feature Journey

Spec Kit enforces an **8-command workflow** with strict phase separation to prevent premature decisions and ensure architectural consistency.

### Command Sequence Overview

```
/constitution [REQUIRED - once per project]
     │
     ├─> /clarify-constitution [optional, if [NEEDS CLARIFICATION] markers exist]
     │
     ↓
/specify [REQUIRED - per feature]
     │
     ├─> /clarify [optional but recommended]
     │
     ↓
/plan [REQUIRED - per feature]
     ↓
/tasks [REQUIRED - per feature]
     │
     ├─> /analyze [optional but recommended]
     │
     ↓
/implement [REQUIRED - per feature]
```

### Workflow Phases

#### Phase 0: Project Governance (Once Per Project)

**Command:** `/constitution`

**Purpose:** Establish project-wide principles that guide all development decisions.

**Example:**
```
/constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
```

**What happens:**
1. Claude creates `.specify/memory/constitution.md` with your governance principles
2. Applies semantic versioning (1.0.0 for new constitution)
3. May insert `[NEEDS CLARIFICATION]` markers for ambiguous areas
4. Reports completion with version number and next command

**Output example:**
```
Constitution created at .specify/memory/constitution.md

Version: 1.0.0 (new constitution)

⚠ Incomplete Sections (2):
- Testing strategy (Principle II)
- Deployment workflow (Governance)

Next command: /clarify-constitution
```

**If no clarifications needed:**
```
Constitution created at .specify/memory/constitution.md

Version: 1.0.0 (new constitution)

✓ All sections complete

Next command: /specify
```

---

#### Phase 1: Feature Specification

**Command:** `/specify <description>`

**Purpose:** Define **what** you want to build (requirements, user stories) without technical decisions.

**Example:**
```
/specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
```

**What happens:**
1. Runs `.specify/scripts/bash/create-new-feature.sh` to create feature directory
2. Generates sequential feature ID (001-photo-albums, 002-next-feature, etc.)
3. Creates `specs/001-photo-albums/spec.md` from template
4. Parses your description into structured sections:
   - User Stories (US-001, US-002, ...)
   - Functional Requirements (FR-001, FR-002, ...)
   - Non-Functional Requirements (NFR-001, NFR-002, ...)
   - Acceptance Criteria
5. Marks ambiguities with `[NEEDS CLARIFICATION: specific question]`

**Output example:**
```
Feature created: 001-photo-albums

Specification: /path/to/specs/001-photo-albums/spec.md

Generated:
- 8 user stories
- 12 functional requirements
- 4 non-functional requirements
- [NEEDS CLARIFICATION] markers: 3

Next command: /clarify (recommended) or /plan (if skipping clarification)
```

**Files created:**
```
specs/001-photo-albums/
└── spec.md
```

---

#### Phase 2: Clarification (Optional but Recommended)

**Command:** `/clarify`

**Purpose:** Resolve ambiguities before planning to reduce rework. Maximum 5 interactive questions.

**Example interaction:**
```
/clarify

Q1: What is the maximum file size supported for photo uploads?
> 10MB per photo

Q2: Which image formats should be supported?
> JPEG, PNG, HEIC

Q3: Should albums support sorting options beyond date?
> done

Clarifications integrated into spec.md

Updated sections:
- NFR-001: File size limit (10MB)
- FR-003: Supported formats (JPEG, PNG, HEIC)

Next command: /plan
```

**What happens:**
1. Claude analyzes spec.md for ambiguities using 10 taxonomy categories
2. Asks targeted questions one at a time
3. Integrates each answer directly into spec.md
4. Saves after each answer (atomic updates)
5. User can type "done" to exit early

**Files updated:**
```
specs/001-photo-albums/
└── spec.md  (Clarifications section added)
```

---

#### Phase 3: Technical Planning

**Command:** `/plan <tech stack details>`

**Purpose:** Create implementation plan with **how** technical decisions while validating constitutional principles.

**Example:**
```
/plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

**What happens:**
1. Runs `.specify/scripts/bash/setup-plan.sh` to prepare plan structure
2. **PRE-RESEARCH GATE:** Validates spec against constitution principles
3. Phase 0: Creates `research.md` with tech stack decisions
4. Phase 1: Creates `data-model.md`, `contracts/` (API specs), `quickstart.md`
5. **POST-DESIGN GATE:** Re-validates plan against constitution
6. If gate fails: Documents violations in Complexity Tracking table
7. Updates `CLAUDE.md` with tech stack context via `update-agent-context.sh`

**Output example:**
```
Plan created for feature 001-photo-albums

Files generated:
- plan.md (implementation strategy)
- research.md (tech stack: Vite, SQLite, vanilla JS)
- data-model.md (Album, Photo entities)
- contracts/api-spec.yaml (SQLite query interface)
- quickstart.md (integration test scenarios)

Constitutional gates: ✓ 6/6 passed

Next command: /tasks
```

**Files created:**
```
specs/001-photo-albums/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── api-spec.yaml
```

**If constitutional gate fails:**
```
⚠ Constitution Gate: FAIL (2 violations)

Violations:
- Principle I: "Library-First" - using inline SQLite instead of library abstraction
- Principle III: "Test-First" - missing contract test tasks

Complexity Tracking table created in plan.md

You must either:
1. Refactor plan to satisfy principles, OR
2. Document justification in Complexity Tracking table

STOP - Do not proceed to /tasks until gate passes or violations justified
```

---

#### Phase 4: Task Breakdown

**Command:** `/tasks`

**Purpose:** Generate actionable, dependency-ordered tasks from implementation plan.

**Example:**
```
/tasks

Task breakdown created: tasks.md

37 tasks across 5 phases:
- Setup (5 tasks) [P]
- Test (12 tasks) [P]
- Core (8 tasks) [sequential]
- Integration (7 tasks) [P]
- Polish (5 tasks) [P]

Parallel-safe tasks: 18 (marked with [P])
Sequential tasks: 19 (dependency-ordered)

Next command: /analyze (recommended) or /implement
```

**What happens:**
1. Reads `plan.md` and `data-model.md`
2. Generates numbered tasks (T001-T037)
3. Marks parallel-safe tasks with `[P]`
4. Orders tasks by dependencies
5. Enforces TDD: contract tests [P] before endpoint implementation
6. Each task has: description, file changes, test approach, dependencies

**Files created:**
```
specs/001-photo-albums/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── api-spec.yaml
└── tasks.md  (NEW)
```

**Task structure example:**
```markdown
## Setup Phase

- [ ] T001: Initialize Vite project structure [P]
- [ ] T002: Configure SQLite database connection [P]
- [ ] T003: Set up test framework (Vitest) [P]

## Test Phase (TDD)

- [ ] T004: Contract test: Album schema validation [P]
- [ ] T005: Contract test: Photo schema validation [P]
- [ ] T006: Unit test: Album CRUD operations [P]

## Core Phase

- [ ] T010: Implement Album model (depends: T004, T006)
- [ ] T011: Implement Photo model (depends: T005, T007)
- [ ] T012: Implement drag-and-drop UI (depends: T010, T011)
```

---

#### Phase 5: Analysis (Optional but Recommended)

**Command:** `/analyze`

**Purpose:** Validate cross-artifact consistency before implementation.

**Example:**
```
/analyze

Analysis complete: 6 detection passes

✓ Duplication: No near-duplicate requirements
✓ Ambiguity: No vague adjectives without metrics
✓ Underspecification: All requirements have acceptance criteria
✓ Constitution Alignment: 6/6 principles satisfied
✓ Coverage: All requirements mapped to tasks
✓ Inconsistency: No terminology drift

Coverage matrix:
FR-001 → T010, T012 ✓
FR-002 → T011 ✓
FR-003 → T013, T014 ✓
...

Next command: /implement
```

**What happens:**
1. Builds semantic model from spec.md, plan.md, tasks.md
2. Runs 6 detection passes (Duplication, Ambiguity, Underspecification, Constitution, Coverage, Inconsistency)
3. Reports findings by severity (CRITICAL, HIGH, MEDIUM, LOW)
4. Suggests remediation for gaps

**If gaps found:**
```
⚠ Analysis findings:

CRITICAL (1):
- FR-005: No tasks found covering "album deletion" requirement

HIGH (2):
- FR-008: Ambiguous "should be fast" without metrics
- NFR-002: Missing acceptance criteria for "responsive UI"

Suggested remediation:
1. Add task for FR-005 implementation
2. Clarify "fast" with specific latency target (e.g., <100ms)
3. Define responsive UI breakpoints in acceptance criteria

Fix issues before running /implement or document exceptions
```

---

#### Phase 6: Implementation

**Command:** `/implement`

**Purpose:** Execute all tasks in dependency order to generate working code.

**Example:**
```
/implement

Executing 37 tasks...

Phase 1: Setup (5 tasks) [parallel]
✓ T001: Initialize Vite project structure
✓ T002: Configure SQLite database connection
✓ T003: Set up test framework
✓ T004: Create .env.example
✓ T005: Set up ESLint/Prettier

Phase 2: Test (12 tasks) [parallel]
✓ T006: Contract test: Album schema
✓ T007: Contract test: Photo schema
...

Phase 3: Core (8 tasks) [sequential]
✓ T010: Implement Album model
✓ T011: Implement Photo model
  ✓ Tests pass (12/12)
✓ T012: Implement drag-and-drop UI
...

Phase 4: Integration (7 tasks)
...

Phase 5: Polish (5 tasks)
...

Implementation complete!

Files changed:
- 18 source files created
- 12 test files created
- 3 configuration files updated

Test results:
✓ 47 tests passed
✗ 0 tests failed

Next steps:
1. Run application: npm run dev
2. Review implementation
3. Test manually in browser
```

**What happens:**
1. Validates prerequisites (constitution, spec, plan, tasks exist)
2. Parses `tasks.md` for task list and dependencies
3. Executes tasks in phases:
   - Parallel-safe tasks run first within each phase
   - Sequential tasks wait for dependencies
4. Follows TDD approach: runs tests before implementation
5. Marks completed tasks with `[X]` in tasks.md
6. Halts on sequential task failure (continues for parallel failures)
7. Reports progress with file changes and test results

**Files updated:**
```
specs/001-photo-albums/
└── tasks.md  ([X] marks added to completed tasks)

(Application code created in project root)
src/
├── models/
│   ├── Album.js
│   └── Photo.js
├── ui/
│   ├── AlbumGrid.js
│   └── DragDrop.js
└── db/
    └── sqlite.js

tests/
├── Album.test.js
├── Photo.test.js
└── integration/
    └── album-flow.test.js
```

---

## When to Use Spec Kit

### Ideal Use Cases

Spec Kit works best when:

- **Solo developer projects** - Optimized workflow without team coordination overhead
- **Specification-heavy domains** - APIs, CLIs, data pipelines benefit from formal specs
- **Greenfield development** - Starting fresh with spec-first approach
- **AI-assisted workflows** - Claude Code as primary development tool
- **Architectural consistency required** - Constitutional gates enforce principles
- **Iterative refinement** - Evolving requirements through /clarify and plan updates

### Less Ideal Use Cases

Consider alternatives when:

- **Large teams** - Designed for solo developers, not parallel team workflows
- **Legacy codebases** - Spec-first culture hard to retrofit
- **Quick prototypes** - Specification overhead not justified for throwaways
- **GUI-heavy applications** - Visual design harder to specify textually
- **Performance-critical systems** - Generated code may need manual optimization
- **Windows-first environments** - Bash scripts require WSL/Git Bash

---

## Understanding the Workflow

### Phase Separation Discipline

Spec Kit enforces **hard boundaries** between phases to prevent common pitfalls:

| Phase | What You Define | What You DON'T Define |
|-------|-----------------|----------------------|
| **/specify** | Requirements, user stories, acceptance criteria | Tech stack, frameworks, implementation approach |
| **/plan** | Tech stack, architecture, data models, contracts | Task breakdown, line-by-line implementation |
| **/tasks** | Task order, dependencies, test approach | Actual code (no execution yet) |
| **/implement** | Execution order, TDD validation | New requirements (go back to /specify) |

**Why this matters:** Premature decisions reduce flexibility. Separating "what" from "how" from "when" enables better architecture and easier pivots.

### Constitutional Governance

The constitution (`.specify/memory/constitution.md`) acts as a **type system for architectures**:

- **Violations are "type errors"** requiring justification or refactoring
- **Gates enforce principles** before planning and after design
- **Semantic versioning** tracks governance changes (1.0.0 → 1.1.0 → 2.0.0)
- **Complexity Tracking** documents acceptable trade-offs

**Example principle:**
```markdown
### Principle I: Library-First

**Rule:** Features begin as standalone libraries before CLI/UI integration.

**Rationale:** Testability, reusability, decoupled architecture.

**Enforcement:** Constitutional gate rejects inline implementations.
```

**Gate validation:**
```markdown
### Library-First Gate (Principle I)

- [X] Feature begins as standalone library?
- [X] Clear library boundaries defined?
- [X] CLI/UI depends on library (not vice versa)?

Status: PASS
```

### JSON Communication Contracts

Bash scripts output **only JSON to stdout** (errors to stderr), creating clean state isolation:

**Example:**
```bash
.specify/scripts/bash/create-new-feature.sh --json "Real-time chat"
```

**Output:**
```json
{
  "FEATURE_ID": "003-real-time-chat",
  "SPEC_FILE": "/path/to/specs/003-real-time-chat/spec.md",
  "FEATURE_NUM": "003",
  "FEATURE_DIR": "/path/to/specs/003-real-time-chat"
}
```

Claude parses JSON reliably for next phase (no regex scraping terminal output).

---

## Command Reference Quick Lookup

| Command | Required? | When to Use | Output |
|---------|-----------|-------------|--------|
| `/constitution` | Yes (once) | Project start | `.specify/memory/constitution.md` |
| `/clarify-constitution` | No | After `/constitution` if `[NEEDS CLARIFICATION]` exists | Updated constitution |
| `/specify` | Yes (per feature) | Define feature requirements | `specs/###-name/spec.md` |
| `/clarify` | No (recommended) | After `/specify` before `/plan` | Updated spec.md with Clarifications section |
| `/plan` | Yes (per feature) | Technical design | plan.md, research.md, data-model.md, contracts/, quickstart.md |
| `/tasks` | Yes (per feature) | Task breakdown | tasks.md with T001-T0XX tasks |
| `/analyze` | No (recommended) | After `/tasks` before `/implement` | Validation report, coverage matrix |
| `/implement` | Yes (per feature) | Execute tasks | Working code, updated tasks.md with [X] marks |

---

## Common Workflows

### Minimal Workflow (5 commands)

```bash
/constitution "Library-first, TDD, simple designs"
/specify "Build a REST API for task management"
/plan "Python FastAPI, PostgreSQL, Docker"
/tasks
/implement
```

**Time:** 2-4 hours
**Risk:** Higher (no clarification or analysis gates)
**Use case:** Simple features, experienced users

---

### Recommended Workflow (7 commands)

```bash
/constitution "Library-first, TDD, simple designs"
/specify "Build a REST API for task management"
/clarify  # Interactive Q&A
/plan "Python FastAPI, PostgreSQL, Docker"
/tasks
/analyze  # Validation before implementation
/implement
```

**Time:** 3-6 hours
**Risk:** Lower (clarification reduces rework, analysis catches gaps)
**Use case:** Most features, recommended for new users

---

### Complete Workflow (8 commands)

```bash
/constitution "Library-first, TDD, simple designs"
/clarify-constitution  # If [NEEDS CLARIFICATION] markers exist
/specify "Build a REST API for task management"
/clarify
/plan "Python FastAPI, PostgreSQL, Docker"
/tasks
/analyze
/implement
```

**Time:** 3-7 hours
**Risk:** Lowest (all validation gates enabled)
**Use case:** Complex features, team-shared constitutions

---

## Troubleshooting Common Issues

### Issue: Slash commands not appearing in Claude Code

**Symptoms:**
- `/specify`, `/plan` commands not visible in Claude Code autocomplete

**Solution:**
```bash
# Verify .claude/commands/ directory exists with 8 files
ls -la .claude/commands/
# Should show: constitution.md, specify.md, clarify.md, clarify-constitution.md,
#              plan.md, tasks.md, analyze.md, implement.md

# If missing, re-run init with --force
speclaude init --here --force

# Restart Claude Code to pick up new commands
```

---

### Issue: Templates not found after init

**Symptoms:**
- Error: "Template not found at .specify/templates/spec-template.md"

**Solution:**
```bash
# Verify templates directory exists
ls -la .specify/templates/
# Should show: spec-template.md, plan-template.md, tasks-template.md, agent-file-template.md

# If empty, check for network issues during init
# Re-run with debug output
speclaude init --here --force --debug
```

---

### Issue: Script permission errors

**Symptoms:**
- Error: "Permission denied: .specify/scripts/bash/create-new-feature.sh"

**Solution:**
```bash
# Fix permissions manually
chmod +x .specify/scripts/bash/*.sh

# Verify executable bits set
ls -l .specify/scripts/bash/*.sh
# Should show: -rwxr-xr-x
```

---

### Issue: GitHub rate limiting during download

**Symptoms:**
- Error: "API rate limit exceeded" during `speclaude init`

**Solution:**
```bash
# Use GitHub token for higher rate limits
export GITHUB_TOKEN=ghp_your_token_here
speclaude init my-project

# Or provide token as flag
speclaude init my-project --github-token ghp_your_token_here

# For offline environments, use --local flag
git clone https://github.com/anagri/spec-kit.git
speclaude init my-project --local /path/to/spec-kit
```

---

## Next Steps

### Quick Start (30 minutes)

1. Install Spec Kit: `uv tool install specify-cli --from git+https://github.com/anagri/spec-kit.git`
2. Initialize project: `speclaude init my-first-project`
3. Read this introduction (you're here!)
4. Run minimal workflow with simple feature

### Learn the Workflow (2-3 hours)

1. Read full command documentation in knowledge base
2. Run recommended workflow (7 commands) with real feature
3. Understand constitutional gates and phase separation
4. Practice /clarify interactive questioning

### Deep Understanding (4-5 hours)

1. Study philosophy of Specification-Driven Development
2. Understand 4-layer architecture (CLI → Templates → Scripts → Constitution)
3. Learn constraint mechanisms and AI patterns
4. Review workflows and insights documentation

---

## References

**Sources Consulted**:

- **`/Users/amir36/Documents/workspace/src/github.com/anagri/spec-kit/ai-docs/kb/01-overview.md`**
  - Lines 17-24: Spec Kit definition and paradigm inversion
  - Lines 29-36: Key characteristics table (target, architecture, workflow)
  - Lines 40-63: Core innovation and constraint mechanism
  - Lines 67-98: 4-layer architecture quick overview
  - Lines 103-146: 8-command workflow sequence and command tables
  - Lines 265-283: When to use Spec Kit (ideal use cases and limitations)
  - Lines 288-328: File locations reference with complete structure
  - Lines 334-381: End-to-end workflow example

- **`/Users/amir36/Documents/workspace/src/github.com/anagri/spec-kit/CLAUDE.md`**
  - Lines 5-13: Fork divergences from upstream (Claude-only, bash-only, solo dev)
  - Lines 36-72: Local testing and running CLI commands
  - Lines 92-139: Core components (CLI, templates, bash scripts, Claude commands)
  - Lines 201-242: Monorepo support and repository root detection
  - Lines 245-258: Git branch removal rationale
  - Lines 336-365: Testing procedures after changes
  - Lines 369-461: Debug and troubleshooting common issues

- **`/Users/amir36/Documents/workspace/src/github.com/anagri/spec-kit/README.md`**
  - Lines 34-36: Spec-Driven Development definition
  - Lines 40-188: Installation options, slash commands, environment variables
  - Lines 193-226: Development phases and experimental goals
  - Lines 253-259: Prerequisites list
  - Lines 270-505: Detailed step-by-step process walkthrough

- **`/Users/amir36/Documents/workspace/src/github.com/anagri/spec-kit/templates/commands/constitution.md`**
  - Lines 1-10: Command description and user input handling
  - Lines 11-116: Constitution template workflow (placeholder filling, validation, sync)

- **`/Users/amir36/Documents/workspace/src/github.com/anagri/spec-kit/templates/commands/specify.md`**
  - Lines 1-22: Specify command structure and JSON parsing workflow

- **`/Users/amir36/Documents/workspace/src/github.com/anagri/spec-kit/templates/commands/plan.md`**
  - Lines 1-44: Plan command execution flow with constitutional gates
