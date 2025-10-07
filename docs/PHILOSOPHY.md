# Spec Kit Philosophy: The Claude Code Edition

## Fork Philosophy: Constraint as Optimization

This fork (`anagri/spec-kit`) embodies a deliberate philosophical choice: **trading generality for simplicity**. While the upstream `github/spec-kit` supports multiple AI agents, cross-platform scripts, and team-based branching workflows, this fork optimizes for a single, focused use case:

**Solo developers using Claude Code on Unix-like systems.**

This isn't a limitation—it's an optimization strategy. By constraining the solution space, we:

- **Eliminate complexity** that serves multi-agent abstraction
- **Reduce maintenance burden** of dual-scripting (bash + PowerShell)
- **Simplify workflows** by removing branch-management overhead
- **Focus innovation** on making Claude Code integration exceptional

The result is a leaner, faster, more maintainable tool that does one thing exceptionally well rather than many things adequately.

## Core Philosophy

Spec Kit embodies **specification as executable contract**, not documentation. Three foundational premises:

### 1. Inversion of Authority

Code serves specifications, not vice versa. The spec is the source of truth; implementation is disposable output. This inverts decades of software development practice where code was king and specs were scaffolding.

### 2. Constraint-Driven Generation

LLMs are powerful but undisciplined. Templates act as **compiler directives** that constrain output space to valid architectural choices. Without structure, LLMs produce plausible but architecturally inconsistent code. Templates transform them from creative writers into disciplined specification engineers.

### 3. Separation of Concerns Through Phases

Requirements (what) → Architecture (how) → Tasks (steps) are **hard boundaries**. Mixing them produces hallucination and drift. This separation is not workflow preference—it's architectural necessity:

- **Spec phase**: Users can change their mind without technical debt (no code written)
- **Plan phase**: Tech stack can pivot without rewriting requirements
- **Tasks phase**: Execution order can regenerate without changing design

Breaking this separation collapses the entire model.

## Architectural Layers

```
┌─────────────────────────────────────────┐
│   Layer 1: CLI Orchestrator             │  ← User Entry Point
│   (specify-cli: Python + Typer)         │     [Claude Code hardcoded]
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│   Layer 2: Template Engine              │  ← Transformation Logic
│   (Markdown with execution flows)       │     [Agent-agnostic]
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│   Layer 3: State Automation             │  ← Filesystem/Git
│   (Bash scripts only)                   │     [No branch creation]
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│   Layer 4: Constitutional Enforcement   │  ← Runtime Validation
│   (Six principles + gates)              │
└─────────────────────────────────────────┘
```

### Layer 1: CLI Orchestrator

**Location**: `src/specify_cli/__init__.py`

**Purpose**: Bootstrap projects with Claude Code templates from `anagri/spec-kit` releases.

**Key Design Decisions**:

```python
# Hardcoded constants (no multi-agent abstraction)
AI_AGENT = "claude"
SCRIPT_TYPE = "sh"
repo_owner = "anagri"  # Fork-specific download source
```

**Core Functions**:

- `init()`: Downloads `spec-kit-template-claude-sh-{version}.zip` from GitHub releases, extracts to project
- `check()`: Validates prerequisites (git, claude CLI at `~/.claude/local/claude`)
- `download_template_from_github()`: Fetches versioned zip from `anagri/spec-kit`, handles auth/rate limiting
- `ensure_executable_scripts()`: Sets `chmod +x` on `.sh` files recursively (POSIX only)

**How It Works**:

```python
# Simplified bootstrap flow
1. Parse CLI args (project name, --here, --force)
2. Validate prerequisites (git, claude)
3. Fetch latest release from github.com/anagri/spec-kit/releases
4. Download spec-kit-template-claude-sh-{version}.zip
5. Extract with nested directory flattening
6. chmod +x on all .sh files
7. Initialize git repo (optional)
8. Display next steps
```

**Solo Developer Optimization**:

No agent selection UI, no script-type branching, no cross-platform checks. The CLI knows exactly what it's installing: Claude Code templates with bash scripts. This eliminates ~200 lines of conditional logic from upstream.

**Modification Pattern**:

- **Change bootstrap behavior**: Modify `init()` function, respect `--here` and `--force` flags
- **Custom template source**: Override `download_template_from_github()` repo/owner constants
- **Add validation**: Extend `check()` with new prerequisite checks

**Principle Preservation**:

- Never modify templates during installation (downloaded as-is from releases)
- Respect `.claude/` directory convention
- Maintain JSON communication contract with scripts

### Layer 2: Template Engine

**Location**: `.specify/templates/*.md`, `.specify/templates/commands/*.md`

**Purpose**: Executable specifications that guide Claude Code behavior through structured flows.

**Key Templates**:

- `spec-template.md`: Requirements phase (no technical decisions)
- `plan-template.md`: Architecture phase (tech stack + research)
- `tasks-template.md`: Task decomposition (executable steps)
- `agent-file-template.md`: Template for `CLAUDE.md` generation
- `commands/*.md`: Slash command implementations (7 commands)

**How Templates Work**:

Templates are **not passive documents**. They contain:

**1. YAML Frontmatter** (metadata + script references):

```yaml
description: "Generate feature specification"
scripts:
  sh: scripts/bash/create-new-feature.sh --json
```

**2. Execution Flow Pseudocode** (instructions for Claude):

```markdown
1. Run {SCRIPT} from repo root
2. Parse JSON for FEATURE_DIR, SPEC_FILE
3. Load prerequisite files
4. Fill template sections
5. Validate gates
6. Write output
7. Return status
```

**3. Validation Gates** (constitutional enforcement):

```markdown
## Constitution Check
- [ ] Claude Code-Only: No multi-agent logic?
- [ ] Solo Workflow: No branch coupling?
- [ ] Bash-Only: Unix scripts only?
```

**4. Placeholder System**:

- `[FEATURE]`, `[DATE]` → filled by Claude
- `[NEEDS CLARIFICATION]` → explicit uncertainty marker
- `{SCRIPT}`, `$ARGUMENTS` → runtime interpolation

**Template Constraints Guide Claude Behavior**:

- **Preventing premature implementation**: Spec template forbids tech stack decisions
- **Forcing explicit uncertainty**: `[NEEDS CLARIFICATION]` markers prevent guessing
- **Structured thinking**: Checklists act as unit tests for specifications
- **Constitutional compliance**: Gates enforce architectural principles
- **Hierarchical detail**: Main docs stay readable, complexity extracted to subdirs
- **Test-first thinking**: Templates enforce TDD by design

**Modification Pattern**:

- **Add validation gate**: Insert checkbox in Constitution Check section
- **Change section structure**: Update execution flow that fills that section
- **Add new artifact**: Update Phase 1 to generate it, reference in Phase 2
- **Custom output format**: Override template entirely, preserve execution flow structure

**Principle Preservation**:

- Maintain separation: `spec.md` has NO tech stack, `plan.md` has NO requirements duplication
- Keep execution flows sequential (no parallel steps)
- Always mark ambiguities (never let Claude guess)
- Update Progress Tracking as template executes

### Layer 3: State Automation

**Location**: `.specify/scripts/bash/*.sh`

**Purpose**: Handle filesystem state, path resolution, and optional git operations without branch creation.

**Key Scripts** (bash only):

- `common.sh`: Path discovery, git detection, feature resolution
- `create-new-feature.sh`: Feature directory scaffolding (**no branch creation**)
- `setup-plan.sh`: Plan template copying
- `check-prerequisites.sh`: Validation, available docs enumeration
- `update-agent-context.sh`: Incremental `CLAUDE.md` updates

**Solo Developer Workflow** (Critical Design Change):

```bash
# create-new-feature.sh (line 74)
# Original upstream: git checkout -b "$BRANCH_NAME"
# This fork: NO branch creation

FEATURE_DIR="$SPECS_DIR/$FEATURE_ID"
mkdir -p "$FEATURE_DIR"
# Feature directory created WITHOUT git branch coupling
```

**How It Works** (`create-new-feature.sh` as example):

```bash
# Input: Feature description from $@
# Output: JSON with FEATURE_ID, SPEC_FILE, FEATURE_NUM

1. Find repo root (git rev-parse OR search for .specify/)
2. Scan specs/ for highest number (001, 002, ...)
3. Increment: NEXT=$((HIGHEST + 1))
4. Slugify description → feature ID (001-feature-name)
5. mkdir -p specs/{feature-id}/  # No git branch
6. cp template → specs/{feature-id}/spec.md
7. echo JSON to stdout
```

**Environment Variable Pattern**:

Since features aren't tied to git branches, scripts use `SPECIFY_FEATURE` environment variable to track current feature context. This allows:

- Working directly on `main` branch
- Multiple features in progress without branch switching
- Simpler mental model for solo developers

**Critical Design Decision**: Scripts output **only JSON** to stdout, errors to stderr. This creates a clean contract with Claude.

**Modification Pattern**:

- **Add filesystem operation**: Extend `common.sh`, use `find_repo_root()` for paths
- **Support non-git workflows**: Check `$SPECIFY_FEATURE` env var first
- **Custom directory structure**: Override `get_feature_dir()` in `common.sh`
- **Add validation**: Extend `check-prerequisites.sh`, update JSON output

**Principle Preservation**:

- Always output parseable JSON (even on error)
- Never write to files Claude expects to read (separation of concerns)
- Support both git and non-git repos (check `HAS_GIT` flag)
- No branch creation (respect solo developer workflow)

### Layer 4: Constitutional Enforcement

**Location**: `.specify/memory/constitution.md`

**Purpose**: Runtime validation of the six fork-specific architectural principles.

**The Six Principles**:

1. **Claude Code-Only Support**: No multi-agent logic, only `.claude/commands/`
2. **Solo Developer Workflow**: No git branch coupling, use `SPECIFY_FEATURE` env var
3. **Minimal Divergence from Upstream**: Only remove multi-agent/PowerShell/branches
4. **GitHub Release Distribution**: Templates from `anagri/spec-kit` releases
5. **Version Discipline**: Every `__init__.py` change requires version bump + CHANGELOG
6. **Dogfooding**: Use spec-kit to develop spec-kit

**How Constitutional Enforcement Works**:

**1. Template-Level Gates** (in `plan-template.md`):

```markdown
## Constitution Check
*GATE: Must pass before Phase 0 research*

- [ ] Claude Code-Only (Principle I): No agent selection logic?
- [ ] Solo Workflow (Principle II): No branch creation in scripts?
- [ ] Bash-Only (Principle I): Unix scripts only?
- [ ] Minimal Divergence (Principle III): Core workflow unchanged?
```

**2. Claude Reasoning Loop**:

```
Load constitution → Extract MUST/SHOULD statements
Generate checklist for current plan
Evaluate: PASS/FAIL/JUSTIFY
If FAIL → Document in Complexity Tracking OR refactor
```

**3. Complexity Tracking Table**:

```markdown
| Violation | Why Needed | Simpler Alternative Rejected |
|-----------|------------|------------------------------|
| 4th dependency | Performance critical | Vanilla impl 10x slower |
```

**4. Version Enforcement** (Principle V):

- MAJOR: Breaking changes (remove commands, change args)
- MINOR: New features (new commands, new flags)
- PATCH: Bug fixes, docs, refactoring

Every `src/specify_cli/__init__.py` change **must** update `pyproject.toml` and `CHANGELOG.md`.

**Modification Pattern**:

- **Add principle**: Use `/constitution` command, update plan template gates
- **Change gate logic**: Modify plan-template.md Constitution Check section
- **Enforce in other phases**: Add gates to spec/tasks templates
- **Custom validation**: Create `validate-constitution.sh`, call from template

**Principle Preservation**:

- Constitution is **non-negotiable during implementation** (compiler error, not guideline)
- Violations must be documented with rationale (accountability)
- Re-check after design phase (architecture might introduce violations)
- Sync dependent templates when constitution changes

## Solo Developer Workflow Model

Unlike upstream's branch-based team workflow, this fork uses a **direct-on-main** pattern optimized for solo developers:

### Traditional Team Workflow (Upstream):

```bash
/specify "Feature X"
→ Creates branch: 003-feature-x
→ Creates specs/003-feature-x/spec.md
→ Work happens in isolated branch
→ Merge via PR when complete
```

### Solo Developer Workflow (This Fork):

```bash
/specify "Feature X"
→ Creates specs/003-feature-x/ (no branch)
→ All work on main branch
→ SPECIFY_FEATURE=003-feature-x env var for context
→ Commit when ready (manual, per user preference)
```

### Why This Design?

**1. Reduced Friction**: Solo developers rarely need branch isolation. Creating/switching branches adds ceremony without benefit.

**2. Simpler Mental Model**: One branch (`main`), multiple feature directories. Current work tracked by directory, not git branch.

**3. Faster Iteration**: No `git checkout`, no branch naming, no merge conflicts with yourself.

**4. Respects User Preferences**: User's CLAUDE.md specifies "no auto git commits"—this workflow respects that by decoupling features from git entirely.

### Environment Variable Pattern:

```bash
# Set current feature context
export SPECIFY_FEATURE=003-feature-x

# Scripts detect current feature
current_feature="${SPECIFY_FEATURE:-$(get_current_branch)}"

# Works with or without git branches
```

This allows gradual adoption: start without branches, add them later if needed.

## Layer Interaction Model

### Example: `/specify` Command (No-Branch Workflow)

```
User: /specify "Build real-time chat"
         ↓
Claude parses command from .claude/commands/specify.md
         ↓
Layer 2 (Template): Loads spec-template.md execution flow
         ↓
Layer 3 (Script): create-new-feature.sh --json "real-time chat"
         ↓
Script logic:
  - Scans specs/ → finds 002 is highest
  - Next ID: 003
  - Slugify: "real-time-chat"
  - Creates: specs/003-real-time-chat/ (NO git branch)
         ↓
JSON output: {"FEATURE_ID":"003-real-time-chat","SPEC_FILE":"..."}
         ↓
Layer 2: Fill spec-template.md placeholders
         ↓
Layer 4: Validate against constitution (implicit check)
         ↓
Write: specs/003-real-time-chat/spec.md
         ↓
Return: "Feature 003-real-time-chat created at specs/003-real-time-chat/"
```

**Key difference from upstream**: No `git checkout -b 003-real-time-chat`. Directory structure provides isolation without git branch coupling.

### Example: `/plan` Command (Constitution Enforcement)

```
User: /plan "Use WebSockets + Redis + PostgreSQL"
         ↓
Layer 2 (Template): plan.md loads from .claude/commands/plan.md
         ↓
Layer 3 (Script): setup-plan.sh --json
         ↓
JSON: {"FEATURE_SPEC":"...","IMPL_PLAN":"...","FEATURE_DIR":"..."}
         ↓
Layer 2: Load specs/003-real-time-chat/spec.md
         ↓
Layer 4: Evaluate Constitution Check gates
  - [ ] Claude Code-Only? ✓ (no agent logic)
  - [ ] Solo Workflow? ✓ (no branch references)
  - [ ] Bash-Only? ✓ (no PowerShell scripts)
         ↓
Layer 2: Execute Phase 0 (research.md for WebSocket/Redis/PostgreSQL)
         ↓
Layer 2: Execute Phase 1 (contracts/, data-model.md)
         ↓
Layer 3 (Script): update-agent-context.sh claude
  - Parses plan.md for tech stack
  - Updates CLAUDE.md with language/framework/database info
         ↓
Layer 4: Re-evaluate gates (post-design validation)
         ↓
Write: specs/003-real-time-chat/plan.md
Return: "Plan complete at specs/003-real-time-chat/plan.md"
```

**Key Insight**: Layers communicate through **immutable JSON contracts**. Scripts never read Claude-generated content; Claude never executes git commands. This prevents state corruption.

## Extension Patterns for Claude Code

### Pattern 1: Add New Slash Command

**Valid** (respects architecture):

```markdown
# .specify/templates/commands/benchmark.md
---
description: "Run performance benchmarks against plan targets"
scripts:
  sh: scripts/bash/get-feature-context.sh --json
---

**Execution Flow**:
1. Run {SCRIPT} to get FEATURE_DIR and current feature info
2. Load plan.md to extract performance targets from Non-Functional Requirements
3. Execute benchmark suite appropriate to tech stack
4. Compare results against targets
5. Report PASS/FAIL with details
6. Suggest plan updates if targets unrealistic
```

**Invalid** (breaks principles):

```markdown
# DON'T DO THIS
1. Run `pytest benchmarks/` directly  # ← No script, no JSON contract
2. Assume 100ms latency target  # ← Should come from plan.md NFRs
3. Hardcode tech stack assumptions  # ← Should detect from plan
```

### Pattern 2: Modify Constitution

**Valid** (proper amendment):

```bash
# Use /constitution command to amend
/constitution "Add principle: All CLI operations <100ms on small repos"

# This updates constitution.md, then update plan-template.md:
```

```markdown
### Performance-First Gate (Principle VII)
- [ ] All CLI commands profiled with `time` command?
- [ ] Progress indicators for >1s operations?
- [ ] Lazy loading for expensive operations?
```

**Invalid** (no enforcement):

```markdown
# DON'T DO THIS in constitution.md
### VII. Performance-First
All operations should be fast.
# ← Vague, not measurable, no template enforcement
```

### Pattern 3: Custom Artifact Generation

**Valid** (script + template integration):

```bash
# 1. Add script: scripts/bash/generate-openapi.sh
#!/bin/bash
set -e

FEATURE_DIR=$(get_feature_dir)
CONTRACTS_DIR="$FEATURE_DIR/contracts"

# Merge YAML contracts into single OpenAPI spec
cat > "$FEATURE_DIR/openapi.yaml" <<EOF
openapi: 3.0.0
...
EOF

echo '{"OPENAPI_FILE":"'$FEATURE_DIR/openapi.yaml'"}'
```

```markdown
# 2. Reference in plan-template.md Phase 1:
6. Generate OpenAPI specification
   - Run: {SCRIPT:scripts/bash/generate-openapi.sh}
   - Parse JSON output for OPENAPI_FILE path
   - Validate OpenAPI spec against contracts/
   - Output: $FEATURE_DIR/openapi.yaml
```

**Invalid** (Claude generates directly):

```markdown
# DON'T DO THIS
6. Create openapi.yaml with all REST endpoints
   # ← Claude will hallucinate endpoints instead of deriving from contracts/
```

### Pattern 4: Template Customization (Manual Addition Markers)

Templates support custom sections via markers:

```markdown
# In agent-file-template.md (generates CLAUDE.md)

## Technology Stack
<!-- BEGIN MANUAL TECH STACK -->
[Language]: [Detected from plan.md]
[Framework]: [Detected from plan.md]
<!-- END MANUAL TECH STACK -->

<!-- BEGIN MANUAL ADDITIONS -->
# User can add custom sections here
# They won't be overwritten by update-agent-context.sh
<!-- END MANUAL ADDITIONS -->
```

This allows users to add project-specific guidance while keeping auto-generated sections current.

## Critical Insights

### Insight 1: Templates Are Constraint Functions

The genius of Spec Kit is treating templates as **reduction functions** on LLM output space:

```
Unconstrained Claude: 10^n possible outputs (hallucination prone)
              ↓
Template with execution flow: 10^3 valid outputs (constrained)
              ↓
Constitutional gates: 10^1 acceptable outputs (enforced)
```

Templates contain pseudocode execution flows—they're **instructions for Claude to execute**, not suggestions. This transforms Claude from a creative writer into a disciplined specification engineer.

### Insight 2: Phase Separation Is Load-Bearing

Spec → Plan → Tasks separation is **architectural necessity**, not workflow preference:

- **Spec phase**: Change requirements without technical debt (no code exists)
- **Plan phase**: Pivot tech stack without rewriting requirements
- **Tasks phase**: Regenerate execution order without changing design

Breaking this (e.g., putting tech stack in `spec.md`) collapses the model. Each phase builds on the previous, but they remain **referentially transparent**—same inputs produce same outputs.

### Insight 3: JSON as State Boundary

Scripts output JSON not for aesthetics, but for **state isolation**:

```bash
# What script does:
mkdir -p specs/003-feature/  # ← Changes filesystem state
echo '{"FEATURE_DIR":"specs/003-feature"}'  # ← Communicates change

# What Claude does:
Parse JSON  # ← Learns new state
Load spec-template.md  # ← Pure transformation (no side effects)
Write spec.md  # ← New artifact
```

If Claude executed `mkdir` directly, you'd get race conditions, permission errors, and state corruption. JSON creates a **read-only view of side effects**.

### Insight 4: Constitution as Type System

The constitution isn't documentation—it's a **type system for architectures**:

```
Type error: "Solo Workflow principle violated"
  Expected: No git branch creation in scripts
  Actual: create-new-feature.sh contains 'git checkout -b'

Fix: Remove branch creation (line 74)
     OR justify in Complexity Tracking table
```

This is why constitution has version semantics (1.0.0) like software. Principles are executable constraints, not guidelines.

### Insight 5: The Constraint Paradox

This fork is **most extensible through constraint**:

- **Upstream**: Supports 4 agents, 2 script types, 3 workflows → complex extension surface
- **This fork**: Supports 1 agent, 1 script type, 1 workflow → simple extension surface

By removing generality, we make it **easier to extend** within the constrained space. Adding a Claude Code slash command is trivial. Adding multi-agent support would be architectural upheaval.

**Extension is easier when the foundation is stable and singular.**

## Fork-Specific Design Decisions

### Why Claude Code-Only?

**Technical Reasoning**:

1. **Slash command integration**: Claude Code's `.claude/commands/*.md` pattern is first-class
2. **JSON communication**: Claude excels at parsing script JSON output
3. **Template execution**: Claude follows execution flow pseudocode reliably
4. **Constitution enforcement**: Claude's reasoning handles complex gate evaluation

**Maintenance Reasoning**:

1. **No agent abstraction layer**: Eliminates conditional logic for agent detection
2. **Single template set**: No need to test against multiple agent behaviors
3. **Focused optimization**: Can use Claude-specific features without compatibility concerns

**User Reasoning**:

Solo developers use one tool. Supporting multiple agents optimizes for a use case that doesn't exist in this fork's target audience.

### Why Bash-Only?

**Technical Reasoning**:

1. **POSIX ubiquity**: macOS and Linux (and WSL) have bash by default
2. **Simpler permissions**: `chmod +x *.sh` works universally on target platforms
3. **Git integration**: Bash and git have identical command syntax on all platforms

**Maintenance Reasoning**:

1. **Half the code**: No dual bash/PowerShell implementation
2. **Half the testing**: No cross-platform script validation
3. **Easier upstream merge**: Copy bash scripts, ignore PowerShell changes

**User Reasoning**:

Target users are on Unix-like systems. Windows users serious about development use WSL/Git Bash anyway. Native PowerShell support serves a minority at high cost.

### Why No Git Branches?

**Technical Reasoning**:

1. **Solo developer pattern**: No parallel work by multiple people
2. **Simpler mental model**: Feature = directory, not branch
3. **Faster iteration**: No branch switching, no merge conflicts
4. **Git optional**: Features work even in `--no-git` repos

**Maintenance Reasoning**:

1. **Less git logic**: No branch name validation, no checkout error handling
2. **Fewer edge cases**: No detached HEAD, no merge conflict scenarios
3. **Simpler JSON**: No BRANCH_NAME in script output

**User Reasoning**:

Solo developers often work directly on `main`. Creating feature branches adds ceremony without benefit. If they want branches, they can create them manually—the tool doesn't prevent it, just doesn't require it.

### Why anagri/spec-kit Distribution?

**Fork Independence**:

1. **Upstream can change**: `github/spec-kit` might add multi-agent features this fork rejects
2. **Release autonomy**: Can cut releases without upstream coordination
3. **Template divergence**: Can modify templates for Claude-specific optimizations

**User Clarity**:

1. **Explicit fork**: `speclaude` command + `anagri/spec-kit` source makes fork obvious
2. **Version independence**: Fork versions don't conflict with upstream
3. **Contribution clarity**: Users know which repo to file issues against

## Alignment with Upstream

### What Stays the Same (Core Methodology)

1. **Spec-driven workflow**: Spec → Plan → Tasks → Implement (unchanged)
2. **Template structure**: Same sections, same execution flows
3. **Constitutional enforcement**: Gates in plan template (adapted gates)
4. **JSON contracts**: Scripts output JSON, Claude parses it
5. **Release distribution**: GitHub releases with zip packages
6. **Dogfooding**: Use spec-kit to develop spec-kit

**These are the load-bearing elements.** Changes here would break the methodology.

### What Diverges (Optimization Constraints)

1. **Agent support**: Upstream supports multiple, fork only Claude Code
2. **Script platform**: Upstream supports bash + PowerShell, fork only bash
3. **Git workflow**: Upstream creates branches, fork creates directories
4. **Download source**: Upstream from `github/spec-kit`, fork from `anagri/spec-kit`
5. **Template count**: Upstream has agent variants, fork has single set
6. **CLI flags**: Upstream has `--ai` and `--script`, fork hardcodes constants

**These are the simplification decisions.** They reduce complexity without changing core methodology.

### Merge Strategy for Upstream Improvements

When upstream `github/spec-kit` releases improvements:

**✅ Safe to merge**:

- Template content changes (spec/plan/tasks wording improvements)
- Constitutional principles (adapt to fork's six principles)
- Documentation improvements (adapt agent references to Claude)
- Bug fixes in Python CLI logic (usually portable)

**⚠️ Requires adaptation**:

- Script changes (copy bash, ignore PowerShell)
- Agent-specific logic (extract Claude-relevant parts)
- Workflow changes (evaluate against solo-dev model)
- Release workflow (adapt for single package generation)

**❌ Do not merge**:

- Multi-agent abstraction layers
- PowerShell script additions
- Git branch coupling logic
- Cross-agent template multiplexing

**Merge Process**:

1. Review upstream commit diffs
2. Check against constitution (Principle III: Minimal Divergence)
3. Extract Claude + bash relevant changes
4. Test locally: `uvx --from . specify-cli init test-proj`
5. Update CHANGELOG.md with upstream attribution
6. Document divergence in CLAUDE.md if necessary

## Architecture Criticisms & Limitations

### Fork-Specific Limitations

**1. Single Agent Lock-In**

- **Limitation**: Can't switch to Gemini/GPT-4 without architectural changes
- **Mitigation**: Constitution principle allows this—it's intentional, not oversight
- **When it matters**: If Claude Code quality degrades or pricing changes
- **Fix if needed**: Fork can re-add agent abstraction, but loses simplicity benefit

**2. Bash-Only Platform Constraint**

- **Limitation**: Windows users must use WSL or Git Bash
- **Mitigation**: Most developers have these; native PowerShell is edge case
- **When it matters**: Enterprise Windows-only environments
- **Fix if needed**: Users can contribute PowerShell ports, fork won't maintain them

**3. No Branch Isolation**

- **Limitation**: Can't work on parallel features in true isolation
- **Mitigation**: Feature directories provide logical isolation
- **When it matters**: Experimenting with breaking changes across features
- **Fix if needed**: Users can create branches manually; tool doesn't prevent it

**4. GitHub Release Dependency**

- **Design Decision**: Templates distributed via GitHub releases (architectural choice per Constitution Principle IV)
- **Trade-off**: Offline installation requires pre-downloaded zip vs. always getting latest templates
- **When it matters**: Air-gapped or firewalled environments
- **Alternative approach**: Pre-download release zip for offline use; bundling in package would sacrifice template updateability

### Shared Upstream Limitations

**1. Template Verbosity**

- **Issue**: Each template is 100-200 lines, high token cost per command
- **Impact**: Slower Claude responses, higher API costs
- **Potential fix**: Create "lite" templates without examples
- **Upstream status**: Acknowledged, no solution yet

**2. No Incremental Planning**

- **Issue**: `/plan` is atomic—can't update just one section
- **Impact**: Small changes require full plan regeneration
- **Potential fix**: Add `/plan --update <section>` command
- **Fork consideration**: Could implement Claude-specific incremental updates

**3. Single Constitution Per Project**

- **Issue**: Can't have feature-specific principles
- **Impact**: All features must follow same architectural rules
- **Potential fix**: Support `.specify/memory/constitutions/{feature-id}.md`
- **Fork consideration**: Simpler to enforce uniform principles across features

**4. No Rollback Mechanism**

- **Issue**: If `/implement` fails halfway, manual recovery needed
- **Impact**: Time lost undoing partial changes
- **Potential fix**: Transaction log + `/rollback` command
- **Fork consideration**: Could track changes in `.specify/history/`

## Summary: The Optimized Specification Compiler

Think of this fork as a **specification compiler optimized for a single target architecture**:

```
Source Language: Natural language requirements (universal)
              ↓
Compiler Frontend: spec.md → plan.md → tasks.md (universal)
              ↓
Optimizer: Constitutional gates (fork-specific: 6 principles)
              ↓
Code Generator: Claude Code (fork-specific: single agent)
              ↓
Runtime: Bash scripts (fork-specific: POSIX only)
              ↓
Output: Implementation (universal: working code)
```

**Upstream** is like `gcc`: supports multiple architectures (x86, ARM, MIPS), multiple platforms (Linux, Windows, macOS), multiple languages (C, C++, Objective-C). Powerful, but complex.

**This fork** is like a specialized compiler: targets only one architecture (Claude Code), one platform (POSIX), one workflow (solo dev). Less general, but **optimized for that single use case**.

The layers exist to **preserve referential transparency**—each transformation is deterministic given the same inputs. The constitution provides **static analysis** to catch "type errors" before compilation. The templates are **compiler passes** that transform specifications through intermediate representations to executable code.

Extend it by:

- **Adding compiler passes**: New slash commands (templates)
- **Adding optimizations**: Better templates, smarter scripts
- **Adding type rules**: New constitutional principles

Break it by:

- **Mixing compilation stages**: Tech stack in spec.md, requirements in plan.md
- **Introducing side effects**: Claude executing git/mkdir directly
- **Violating type constraints**: Ignoring constitutional gates

**The philosophy: Specifications are programs. This fork compiles them optimally for Claude Code on Unix.**
