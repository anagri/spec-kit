# Technical Architecture: The 4-Layer Model

**Purpose**: Details the 4-layer separation model implementing specification-driven development
**Target Audience**: Tech experts familiar with agile/TDD, new to AI-assisted SDD
**Related Files**:

- [Overview](01-overview.md) - High-level architecture summary
- [Commands: Core](04-commands-core.md) - How commands use the architecture
- [Bash Automation](07-bash-automation.md) - Layer 3 script details
- [Constitution](08-constitution.md) - Layer 4 governance
  **Keywords**: 4-layer model, CLI orchestrator, template engine, state automation, constitutional enforcement

---

## Overview

Spec-kit's architecture embodies a strict separation of concerns through four distinct layers, each with clear responsibilities and communication contracts. This layered approach creates a structured environment that constrains LLM behavior while maintaining flexibility.

```
Layer 4: Constitutional Enforcement (constitution.md)
         │ Validates architectural principles
         ↓
Layer 3: State Automation (bash/*.sh)
         │ Handles filesystem state, JSON contracts
         ↓
Layer 2: Template Engine (templates/*.md)
         │ Executable specifications with validation gates
         ↓
Layer 1: CLI Orchestrator (__init__.py)
         │ Bootstrap and distribution
```

---

## Layer 1: CLI Orchestrator

**Location**: `src/specify_cli/__init__.py` (1221 lines, single file)
**Technology**: Python 3.11+ with Typer (CLI) and Rich (UI)
**Purpose**: Bootstrap projects with Claude Code templates from GitHub releases

### Core Responsibilities

#### 1. Project Initialization

```python
def init(project_name, here, force, local, github_token):
    # Download spec-kit-template-claude-sh-{version}.zip from anagri/spec-kit releases
    # Extract to project directory with nested directory flattening
    # chmod +x on all .sh files (POSIX only)
    # Initialize git repo (optional)
```

The initialization process:

1. Downloads versioned template ZIP from GitHub releases
2. Extracts to target directory with directory flattening
3. Makes all `.sh` files executable (POSIX systems only)
4. Optionally initializes git repository
5. Reports success with Rich-formatted output

#### 2. Prerequisite Validation

```python
def check():
    # Validates git availability
    # Special handling for claude CLI at ~/.claude/local/claude (post-migration)
    # Reports tool status
```

The check command validates:

- Git installation and version
- Claude Code CLI availability (checks `~/.claude/local/claude` post-migration path)
- Tool versions and compatibility
- Provides clear status reporting with Rich formatting

#### 3. Template Distribution

The CLI handles template distribution with specific design choices:

- **Source**: Downloads from `anagri/spec-kit` releases (fork-specific, not `github/spec-kit`)
- **Authentication**: Handles GitHub token authentication to avoid rate limiting
- **Security**: Supports SSL/TLS with truststore for secure downloads
- **Offline Mode**: Provides `--local` flag for offline development workflows

### Solo Developer Optimizations

The fork eliminates multi-agent abstractions through hardcoded constants:

```python
# Hardcoded constants - no multi-agent abstraction
AI_AGENT = "claude"
SCRIPT_TYPE = "sh"
repo_owner = "anagri"  # Fork-specific download source
```

**Impact**: This eliminates approximately 200 lines of conditional logic compared to upstream multi-agent support. The simplification makes the codebase more maintainable for solo developers while removing complexity that would never be used.

### Key Functions

- **`download_template_from_github()`**: Fetches versioned zip archive, handles authentication and rate limiting, manages SSL/TLS certificates
- **`ensure_executable_scripts()`**: Recursively sets `chmod +x` on all `.sh` files in the project directory (POSIX systems only)
- **`StepTracker` class**: Rich-based progress UI with circular indicators (●/○) for visual feedback during initialization

### Design Philosophy

Layer 1 is deliberately minimal:

- **Single responsibility**: Bootstrap and distribute templates
- **No business logic**: Delegates all specification work to templates and scripts
- **Solo-optimized**: Hardcoded choices eliminate configuration complexity
- **Distribution-focused**: Treats templates as versioned artifacts from GitHub releases

---

## Layer 2: Template Engine

**Location**: `.specify/templates/*.md`, `.claude/commands/*.md`
**Purpose**: Executable specifications that guide Claude Code behavior through structured flows

Templates are **not passive documents**—they are executable instructions that constrain and direct LLM behavior through structured flows, validation gates, and explicit uncertainty markers.

### Template Components

#### 1. YAML Frontmatter (Metadata)

```yaml
---
description: "Generate feature specification"
scripts:
  sh: scripts/bash/create-new-feature.sh --json
---
```

Frontmatter provides:

- Human-readable description for command discovery
- Script invocation syntax with platform-specific paths
- Metadata for Claude Code command system integration

#### 2. Execution Flow Pseudocode (Instructions for Claude)

```markdown
## Execution Flow (main)
```

1. Run {SCRIPT} from repo root
2. Parse JSON for FEATURE_DIR, SPEC_FILE
3. Load prerequisite files
4. Fill template sections
5. Validate gates
6. Write output
7. Return status

```

```

The execution flow:

- Uses **pseudocode**, not natural language descriptions
- References `{SCRIPT}` from frontmatter for runtime interpolation
- Defines clear steps with numbered sequence
- Specifies exact file operations (load, parse, write)
- Enforces validation before output

#### 3. Validation Gates (Constitutional Enforcement)

```markdown
## Constitution Check

- [ ] Claude Code-Only: No multi-agent logic?
- [ ] Solo Workflow: No branch coupling?
- [ ] Bash-Only: Unix scripts only?
```

Gates act as runtime checks:

- Checkboxes force explicit validation (Claude must mark each)
- Each item maps to specific constitutional principle
- Prevents accidental violations through inattention
- Creates audit trail in generated artifacts

#### 4. Placeholder System

Templates use three types of placeholders:

**Static Placeholders** (filled by Claude during execution):

```markdown
[FEATURE]: Feature name from user input
[DATE]: Current date in ISO format
[VERSION]: Version number from context
```

**Uncertainty Markers** (prevent hallucination):

```markdown
[NEEDS CLARIFICATION]: Explicit uncertainty indicator
```

**Runtime Interpolation** (from command invocation):

```markdown
{SCRIPT}: Script path from frontmatter
$ARGUMENTS: Command-line arguments passed to slash command
```

### How Templates Constrain LLM Behavior

Templates act as **reduction functions** on the LLM output space:

```
Unconstrained Claude: 10^n possible outputs (hallucination-prone)
              ↓ [Template with execution flow]
              10^3 valid outputs (constrained)
              ↓ [Constitutional gates]
              10^1 acceptable outputs (enforced)
```

### Constraint Mechanisms

#### 1. Preventing Premature Implementation

Spec templates explicitly forbid technology stack decisions, forcing focus on requirements and behavior.

#### 2. Forcing Explicit Uncertainty

`[NEEDS CLARIFICATION]` markers prevent Claude from guessing when information is missing. The template makes uncertainty visible and actionable.

#### 3. Structured Thinking

Checklists act as "unit tests" for specifications—each checkbox is a validation criterion that must be satisfied.

#### 4. Constitutional Compliance

Gates enforce architectural principles at generation time, preventing violations before artifacts are created.

#### 5. Hierarchical Detail

Main documents stay readable with high-level summaries. Complex details are extracted to subdirectories (`examples/`, `alternatives/`, `context/`).

#### 6. Test-First Thinking

Templates enforce TDD by design—test cases are required sections, not optional additions.

### Template Execution Model

```
User invokes: /new-feature "user authentication"
      ↓
Claude Code loads: .claude/commands/new-feature.md
      ↓
Frontmatter parsed: scripts.sh → create-new-feature.sh
      ↓
Claude executes script: JSON output with FEATURE_DIR, SPEC_FILE
      ↓
Template flow executed: Load prerequisites → Fill sections → Validate gates
      ↓
Artifact written: specs/003-user-authentication/spec.md
      ↓
Status returned: Success with file paths
```

---

## Layer 3: State Automation

**Location**: `.specify/scripts/bash/*.sh`
**Purpose**: Handle filesystem state, path resolution, and optional git operations

Scripts form the stateful layer that handles:

- Directory creation and file operations
- Path resolution (project root, feature directories)
- JSON contract output for Claude
- Optional git operations (commit, status)

### Key Scripts

| Script                    | LOC | Purpose                    | Key Feature                                          |
| ------------------------- | --- | -------------------------- | ---------------------------------------------------- |
| `common.sh`               | 115 | Shared utilities           | `.specify` priority over `.git` for monorepo support |
| `create-new-feature.sh`   | 100 | Feature directory creation | **No branch creation** (solo dev)                    |
| `update-agent-context.sh` | 623 | CLAUDE.md updates          | Incremental updates preserving manual additions      |
| `setup-plan.sh`           | 60  | Plan template setup        | JSON output contract                                 |
| `check-prerequisites.sh`  | 165 | Tool validation            | Enumerates available docs                            |

### Solo Developer Workflow Model

The fork makes a **critical design change** in feature creation:

```bash
# create-new-feature.sh (line 82-84)
# Original upstream: git checkout -b "$BRANCH_NAME"
# This fork: NO branch creation

FEATURE_DIR="$SPECS_DIR/$FEATURE_ID"
mkdir -p "$FEATURE_DIR"
# Feature directory created WITHOUT git branch coupling
```

#### Why No Branches?

1. **Solo developer pattern**: No parallel work by multiple people requiring branch isolation
2. **Simpler mental model**: Feature = directory, not branch. One less abstraction to track.
3. **Faster iteration**: No branch switching, no merge conflicts with yourself
4. **Git optional**: Features work even in `--no-git` repositories

#### Environment Variable Pattern

Since features aren't tied to git branches, the `SPECIFY_FEATURE` environment variable tracks current feature context:

```bash
export SPECIFY_FEATURE=003-feature-name
```

Scripts check this variable first, then fall back to finding the latest feature directory:

```bash
get_current_feature() {
    # First check SPECIFY_FEATURE env var
    if [[ -n "${SPECIFY_FEATURE:-}" ]]; then
        echo "$SPECIFY_FEATURE"
        return
    fi
    # Fallback: Find latest feature directory
    find "$SPECS_DIR" -maxdepth 1 -type d | sort | tail -1
}
```

This provides:

- **Explicit context**: Developer controls which feature is active
- **Fallback behavior**: Defaults to latest feature when not set
- **No branch coupling**: Works independently of git state

### JSON Communication Contract

Scripts implement a **critical design decision**: Output **only JSON** to stdout, errors to stderr.

```bash
# create-new-feature.sh output
{"FEATURE_ID":"003-feature-name","SPEC_FILE":"/path/to/spec.md","FEATURE_NUM":"003"}
```

This creates clean state isolation:

- **Scripts**: Change filesystem state (mkdir, cp, chmod)
- **Claude**: Parse JSON, perform pure transformations, write new artifacts
- **No race conditions**: Clear input/output contract prevents state corruption

**Example Contract**:

```json
{
  "FEATURE_ID": "003-user-authentication",
  "SPEC_FILE": "/Users/dev/project/specs/003-user-authentication/spec.md",
  "FEATURE_NUM": "003",
  "FEATURE_DIR": "/Users/dev/project/specs/003-user-authentication"
}
```

Claude parses this JSON and uses the paths without filesystem operations during template filling.

### Monorepo Support

The `common.sh:get_repo_root()` function implements priority-based root detection:

```bash
# Priority order for repository root detection
while [ "$dir" != "/" ]; do
    if [ -d "$dir/.specify" ]; then echo "$dir"; return 0; fi  # Priority 1
    if [ -d "$dir/.git" ]; then echo "$dir"; return 0; fi      # Priority 2
    dir="$(dirname "$dir")"
done
```

This enables multiple independent spec-kit projects in a single git repository:

```
my-monorepo/                    # Root git repository
├── .git/
├── project-a/
│   ├── .specify/              # First spec-kit project (detected as root)
│   └── specs/
└── project-b/
    ├── .specify/              # Second spec-kit project (detected as root)
    └── specs/
```

**Design Impact**:

- `.specify` marker takes priority over `.git`
- Each project maintains independent feature numbering
- Scripts operate within their project boundary
- No cross-project contamination

---

## Layer 4: Constitutional Enforcement

**Location**: `.specify/memory/constitution.md`
**Purpose**: Runtime validation of fork-specific architectural principles

The constitution isn't documentation—it's a **type system for architectures**. Violations are "type errors" that must be fixed or justified.

### The Six Fork-Specific Principles

| Principle                              | Description                                                  | Enforcement Method                          |
| -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------- |
| I. Claude Code-Only Support            | No multi-agent logic, only `.claude/commands/`               | Template gates + hardcoded CLI constants    |
| II. Solo Developer Workflow            | No git branch coupling, use `SPECIFY_FEATURE` env var        | Script modifications + template validation  |
| III. Minimal Divergence from Upstream  | Only remove multi-agent/PowerShell/branches                  | Code review + CHANGELOG documentation       |
| IV. GitHub Release Distribution        | Templates from `anagri/spec-kit` releases                    | CI/CD workflow + download source hardcoding |
| V. Version Discipline (NON-NEGOTIABLE) | Every `__init__.py` change requires version bump + CHANGELOG | Manual process + constitution reminder      |
| VI. Dogfooding                         | Use spec-kit to develop spec-kit                             | Dual file structure (SOURCE vs INSTALLED)   |

### Constitutional Enforcement Flow

```
1. Template-Level Gates (plan-template.md):
   │
   ├─> Constitution Check section with checkboxes
   │   - [ ] Claude Code-Only (Principle I)
   │   - [ ] Solo Workflow (Principle II)
   │   - [ ] Bash-Only (Principle I)
   │
2. Claude Reasoning Loop:
   │
   ├─> Load constitution → Extract MUST/SHOULD statements
   ├─> Generate checklist for current plan
   ├─> Evaluate: PASS/FAIL/JUSTIFY
   │
3. Complexity Tracking Table:
   │
   └─> If FAIL → Document rationale OR refactor
       │
       | Violation | Why Needed | Simpler Alternative Rejected |
       |-----------|------------|------------------------------|
```

### Type System Analogy

Constitutional principles act like a type system:

| Type System      | Constitution                            |
| ---------------- | --------------------------------------- |
| Type declaration | Principle statement (MUST/SHOULD)       |
| Type checking    | Gate validation in templates            |
| Type error       | Constitutional violation                |
| Compiler         | Claude's reasoning loop                 |
| Cast/suppress    | Justified exception in complexity table |

**Example Violation**:

```markdown
## Constitution Check

- [ ] Claude Code-Only: No multi-agent logic?
      ❌ VIOLATION: Added if/else for Claude vs Aider

## Complexity Tracking

| Violation               | Why Needed                     | Simpler Alternative Rejected                      |
| ----------------------- | ------------------------------ | ------------------------------------------------- |
| Multi-agent conditional | Support upstream compatibility | Fork-only approach rejected (maintain merge path) |
```

The violation must be:

1. **Detected**: Gate marked as failed
2. **Documented**: Rationale in complexity table
3. **Justified**: Alternative approaches evaluated

### Enforcement Mechanisms

#### 1. Template-Level (Compile-Time)

Gates in templates force explicit validation before artifact generation.

#### 2. Runtime (Claude Reasoning)

Claude loads constitution and validates each generated plan/spec against principles.

#### 3. Manual (Code Review)

Human reviewer checks CHANGELOG entries reference constitutional compliance.

#### 4. Structural (Hardcoded Constants)

CLI constants prevent multi-agent code paths from executing.

---

## Cross-References

**Related Architecture Concepts**:

- [Philosophy: Specification-First Development](02-philosophy.md) - Why this architecture exists
- [Commands: Core](04-commands-core.md) - How commands traverse all 4 layers
- [Bash Automation](07-bash-automation.md) - Deep dive into Layer 3 scripts
- [Constitution](08-constitution.md) - Complete Layer 4 principles

**Integration Points**:

- [Dogfooding: SOURCE vs INSTALLED](06-dogfooding.md) - How the project uses its own architecture
- [Commands: Supporting](05-commands-supporting.md) - Template patterns across commands

---

**Navigation**: [← Philosophy](02-philosophy.md) | [Commands: Core →](04-commands-core.md)

---

## Keywords

4-layer model, separation of concerns, CLI orchestrator, template engine, executable specifications, state automation, bash scripts, JSON contracts, constitutional enforcement, type system analogy, validation gates, solo developer workflow, monorepo support, constraint mechanisms, LLM output reduction, placeholder system, execution flow pseudocode, YAML frontmatter, static placeholders, uncertainty markers, runtime interpolation
