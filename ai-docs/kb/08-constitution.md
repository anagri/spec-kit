# Constitutional Enforcement and Governance

**Purpose**: Explains the constitutional system that enforces architectural principles at runtime
**Target Audience**: Developers understanding governance patterns
**Related Files**:

- [Architecture](03-architecture.md) - Layer 4 constitutional enforcement
- [Philosophy](02-philosophy.md) - Constitution as type system
- [Commands: Core](04-commands-core.md) - Constitutional gates in /plan
  **Keywords**: constitution, six principles, gates, enforcement, type system for architectures

---

## Table of Contents

1. [Constitution as Type System](#constitution-as-type-system)
2. [The Six Fork-Specific Principles](#the-six-fork-specific-principles)
   - [Principle I: Claude Code-Only Support](#principle-i-claude-code-only-support)
   - [Principle II: Solo Developer Workflow](#principle-ii-solo-developer-workflow)
   - [Principle III: Minimal Divergence from Upstream](#principle-iii-minimal-divergence-from-upstream)
   - [Principle IV: GitHub Release Distribution](#principle-iv-github-release-distribution)
   - [Principle V: Version Discipline (NON-NEGOTIABLE)](#principle-v-version-discipline-non-negotiable)
   - [Principle VI: Dogfooding - Self-Application](#principle-vi-dogfooding---self-application)
3. [Constitutional Gates in Templates](#constitutional-gates-in-templates)
4. [Version Semantics for Constitution](#version-semantics-for-constitution)

---

## Constitution as Type System

The constitution isn't documentation—it's a **type system for architectures**. Violations are treated as "type errors" that must be fixed or explicitly justified.

### Analogy to Programming

```
TypeScript:               Spec-Kit Constitution:
Type error: "Solo Workflow principle violated"
  Expected: No git branch creation in scripts
  Actual: create-new-feature.sh contains 'git checkout -b'

Fix: Remove branch creation (line 82)
     OR justify in Complexity Tracking table
```

### Core Concept

Just as TypeScript prevents runtime errors by catching type mismatches at compile time, the constitution prevents architectural drift by catching principle violations during planning.

**Enforcement Mechanism**:

- Principles are encoded as checkable constraints
- Claude evaluates designs against these constraints
- Violations must be justified or designs must be refactored
- No automatic bypass—explicit rationale required

**Benefits**:

- Prevents accidental complexity creep
- Forces intentional trade-off discussions
- Creates audit trail of architectural decisions
- Enables safe evolution with clear impact assessment

---

## The Six Fork-Specific Principles

These principles define the governance model for the `anagri/spec-kit` fork. Each principle has specific enforcement mechanisms and accepted trade-offs.

---

### Principle I: Claude Code-Only Support

**Statement**: Only support Claude Code as the AI agent; no multi-agent abstraction logic.

**Enforcement**:

- CLI: Hardcoded `AI_AGENT = "claude"` constant
- Templates: References to `.claude/commands/` only
- No agent detection or selection UI

**Code Examples**:

```python
# src/specify_cli/__init__.py
AI_AGENT = "claude"  # Hardcoded, not configurable

# Templates reference Claude Code directly
COMMAND_DIR = ".claude/commands"  # Not parameterized
```

**Rationale**: Solo developers use one tool. Supporting multiple agents optimizes for a use case that doesn't exist in this fork's target audience.

**Trade-off Accepted**: Cannot switch to Gemini/GPT-4 without architectural changes. This is intentional, not an oversight.

**Why This Matters**:

- Removes conditional logic for agent selection
- Simplifies template structure (no agent-specific variations)
- Reduces testing surface area (one agent, one path)
- Enables deep Claude Code integration without abstraction tax

**Violation Examples**:

- Adding `if agent == "cursor"` logic
- Creating agent detection in CLI
- Parameterizing `.claude/` path for other agents

---

### Principle II: Solo Developer Workflow

**Statement**: No git branch coupling; use `SPECIFY_FEATURE` environment variable for context.

**Enforcement**:

- `create-new-feature.sh`: No `git checkout -b` command (line 82 removed)
- `common.sh`: `get_current_feature()` checks env var first, then scans directories
- Templates: No references to branch names

**Code Examples**:

```bash
# common.sh - Feature detection order
get_current_feature() {
  # 1. Check environment variable (highest priority)
  if [ -n "$SPECIFY_FEATURE" ]; then
    echo "$SPECIFY_FEATURE"
    return
  fi

  # 2. Scan specs/ directories (fallback)
  # ... directory scanning logic ...
}

# create-new-feature.sh - No branch creation
# REMOVED: git checkout -b "feature/${feature_number}-${feature_slug}"
```

**Rationale**:

- Solo developers often work directly on `main`
- Creating branches adds ceremony without benefit
- Faster iteration without branch switching
- Git is optional, not required

**Trade-off Accepted**: No true isolation for experimenting with breaking changes across features. Users can create branches manually if needed.

**Why This Matters**:

- Reduces friction for rapid prototyping
- Supports git-less workflows (local experiments)
- Eliminates branch naming bikeshedding
- Allows parallel features via environment variable

**Violation Examples**:

- Adding `git checkout -b` to automation scripts
- Requiring git branch for feature identification
- Coupling feature lifecycle to git operations

---

### Principle III: Minimal Divergence from Upstream

**Statement**: Only diverge from `github/spec-kit` to remove multi-agent/PowerShell/branch logic.

**Enforcement**:

- CHANGELOG.md: Document every divergence with upstream attribution
- Code comments: Mark removed sections with rationale
- Merge strategy: Copy bash scripts, ignore PowerShell, adapt multi-agent templates

**Documentation Pattern**:

```markdown
# CHANGELOG.md

## [0.2.0] - 2024-08-15

### Divergence from upstream (github/spec-kit)

- Removed PowerShell scripts (Windows support dropped)
- Removed agent selection UI (Claude Code-only, Principle I)
- Removed git branch creation in create-new-feature.sh (Principle II)

### Upstream features adopted

- Phase-based workflow structure
- Constitutional governance model
- Complexity tracking tables
```

**Code Comment Pattern**:

```bash
# create-new-feature.sh
# UPSTREAM: github/spec-kit creates git branch here
# REMOVED: Solo workflow (Principle II) - no branch coupling
# Original line: git checkout -b "feature/${feature_number}-${feature_slug}"
```

**Rationale**: Enables pulling improvements from upstream while maintaining fork simplicity.

**Trade-off Accepted**: Some upstream features cannot be merged cleanly and require manual adaptation.

**Why This Matters**:

- Maintains compatibility with upstream workflow concepts
- Enables selective feature adoption
- Documents fork evolution for future maintainers
- Prevents accidental regression to removed complexity

**Violation Examples**:

- Adopting upstream features without documenting divergence
- Removing upstream attribution from code
- Adding features unrelated to fork's core purpose

---

### Principle IV: GitHub Release Distribution

**Statement**: Distribute templates via GitHub releases at `anagri/spec-kit`.

**Enforcement**:

- CLI: `repo_owner = "anagri"` hardcoded in `download_template_from_github()`
- CI/CD: `.github/workflows/release.yml` creates `spec-kit-template-claude-sh-{version}.zip`
- --local flag: Supports offline development with pre-downloaded releases

**Implementation**:

```python
# src/specify_cli/__init__.py
def download_template_from_github(version: str):
    repo_owner = "anagri"  # Fork-specific
    repo_name = "spec-kit"
    asset_name = f"spec-kit-template-claude-sh-{version}.zip"

    url = f"https://github.com/{repo_owner}/{repo_name}/releases/download/v{version}/{asset_name}"
    # ... download logic ...
```

```yaml
# .github/workflows/release.yml
- name: Create release asset
  run: |
    zip -r spec-kit-template-claude-sh-${{ github.ref_name }}.zip \
      templates/ scripts/ memory/
```

**Rationale**:

- Fork independence: Can cut releases without upstream coordination
- Version autonomy: Fork versions don't conflict with upstream
- Template divergence: Can optimize templates for Claude-specific features

**Trade-off Accepted**: Offline installation requires pre-downloaded zip vs. always getting latest templates.

**Why This Matters**:

- Decouples fork release cycle from upstream
- Enables rapid iteration on fork-specific features
- Supports air-gapped environments (--local flag)
- Clear artifact versioning (one asset per release)

**Violation Examples**:

- Fetching templates from upstream GitHub during init
- Mixing fork and upstream template versions
- Requiring network access without --local fallback

---

### Principle V: Version Discipline (NON-NEGOTIABLE)

**Statement**: Every change to `src/specify_cli/__init__.py` requires version bump in `pyproject.toml` and entry in `CHANGELOG.md`.

**Semantic Versioning Rules**:

- **MAJOR**: Breaking changes (removed commands, changed arguments)
- **MINOR**: New features (new commands, new flags)
- **PATCH**: Bug fixes, docs, refactoring

**Enforcement**:

- Manual process (no automation)
- Constitution reminder in CLAUDE.md
- Release process checklist

**Release Process**:

```bash
# 1. Edit pyproject.toml
version = "X.Y.Z"

# 2. Edit CHANGELOG.md
## [X.Y.Z] - YYYY-MM-DD
- Added/Changed/Fixed...

# 3. Commit and tag
git add -A && git commit -m "chore: bump version to X.Y.Z"
git tag vX.Y.Z

# 4. Push (GitHub Actions creates release automatically)
git push && git push --tags
```

**Version Decision Tree**:

```
Did CLI behavior change?
├─ No  → PATCH (docs, refactor only)
└─ Yes
   ├─ Backward compatible? (old usage still works)
   │  └─ Yes → MINOR (new flag, new command)
   └─ No → MAJOR (removed flag, changed output format)
```

**Rationale**: Users need predictable versioning to understand impact of updates.

**Trade-off Accepted**: Manual process prone to human error. No enforcement besides constitution reminder and peer review.

**Why This Matters**:

- Communicates impact without reading code
- Enables safe dependency pinning
- Creates release-by-release audit trail
- Prevents silent breaking changes

**Violation Examples**:

- Changing CLI without version bump
- Adding CHANGELOG entry without version bump
- Bumping version without CHANGELOG entry

---

### Principle VI: Dogfooding - Self-Application

**Statement**: Use spec-kit to develop spec-kit itself.

**Implementation**: Dual file structure

```
# SOURCE - Edit these to change what users receive
├── src/specify_cli/__init__.py        # CLI implementation
├── scripts/bash/*.sh                  # Packaged → .specify/scripts/bash/
├── templates/*.md                     # Packaged → .specify/templates/
├── templates/commands/*.md            # Packaged → .claude/commands/
├── memory/constitution.md             # Packaged → .specify/memory/

# INSTALLED - Frozen snapshot (do NOT sync with SOURCE during development)
├── .specify/                          # Installed templates, scripts, constitution
├── .claude/                           # Installed slash commands
└── specs/###-feature-name/            # Features developed using dogfooding
```

**Critical Rules**:

- `.specify/` and `.claude/` are **frozen**—do NOT update them when editing source
- To change distribution: Edit `memory/constitution.md`, `templates/`, `scripts/`
- To use spec-kit: Run `/constitution`, `/specify`, `/plan` (uses frozen `.specify/`, `.claude/`)
- Editing `templates/commands/plan.md` does NOT affect `/plan` command (uses `.claude/commands/plan.md`)

**Example Workflow**:

```bash
# Developing a new feature for spec-kit itself
cd /path/to/spec-kit

# 1. Use INSTALLED templates to spec the feature
/specify "Add support for custom template variables"

# 2. This creates specs/003-custom-variables/ using .claude/commands/specify.md (INSTALLED)

# 3. Later, if implementing template changes:
#    - Edit templates/commands/specify.md (SOURCE)
#    - Test by running: speclaude init test-proj --local .
#    - DO NOT update .claude/commands/specify.md (INSTALLED) directly
```

**Rationale**: Forces tool creators to experience the tool as users do, revealing usability issues.

**Trade-off Accepted**: Dual file structure is confusing initially. Clear documentation in CLAUDE.md mitigates this.

**Why This Matters**:

- Catches usability issues before users encounter them
- Validates workflow with real development
- Demonstrates best practices by example
- Ensures templates work as intended

**Violation Examples**:

- Editing `.claude/commands/` directly instead of `templates/commands/`
- Bypassing spec-kit workflow for spec-kit features
- Syncing SOURCE and INSTALLED during development

---

## Constitutional Gates in Templates

Constitutional gates are checkpoints embedded in the `/plan` template that force evaluation against principles before proceeding.

### Plan Template Constitution Check Section

```markdown
## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Claude Code-Only Gate (Principle I)

- [ ] No agent selection logic?
- [ ] Only .claude/commands/ references?

### Solo Workflow Gate (Principle II)

- [ ] No git branch creation in scripts?
- [ ] Using SPECIFY_FEATURE env var?

### Minimal Divergence Gate (Principle III)

- [ ] Core workflow unchanged from upstream?
- [ ] Divergences documented in CHANGELOG?

### GitHub Release Gate (Principle IV)

- [ ] Templates distributed via anagri/spec-kit releases?

### Version Discipline Gate (Principle V)

- [ ] Version bumped in pyproject.toml?
- [ ] CHANGELOG.md entry added?

### Dogfooding Gate (Principle VI)

- [ ] Using spec-kit to develop spec-kit features?
- [ ] SOURCE and INSTALLED separation maintained?
```

### Claude's Evaluation Process

```
1. Load constitution → Extract MUST/SHOULD statements
2. For current plan:
   - Generate checklist from principles
   - Evaluate each checkbox: PASS/FAIL
3. If FAIL:
   - Document in Complexity Tracking table
   - Provide rationale for exception
   - OR refactor design to pass gate
4. If no justification possible:
   - ERROR: "Simplify approach first"
```

### Complexity Tracking Table

When gates fail, violations must be documented:

```markdown
| Violation                                   | Why Needed                                      | Simpler Alternative Rejected Because                       |
| ------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------- |
| Git branch creation (violates Principle II) | Feature requires true isolation for A/B testing | Environment variable insufficient for parallel experiments |
```

**Table Usage**:

- **Violation**: Which principle is being violated
- **Why Needed**: Business justification for the violation
- **Simpler Alternative Rejected Because**: Proof that simpler approaches were considered

### Why Two Evaluations?

1. **Before Phase 0**: Catch violations early in design
2. **After Phase 1**: Re-validate after detailed design (architecture might introduce new violations)

**Rationale**: Architecture decisions made during detailed design can introduce violations not apparent in initial concept.

---

## Version Semantics for Constitution

The constitution itself has semantic versioning:

```markdown
**Version**: 1.0.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2025-07-16
```

### Version Bump Rules

- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

### Why Version the Constitution?

Principles are executable constraints. Changing principles changes system behavior. Versioning communicates impact:

- **v1.0.0 → v2.0.0**: Breaking change (e.g., removing Principle II allows branches)
- **v1.0.0 → v1.1.0**: New principle added (e.g., Principle VII: Performance targets)
- **v1.0.0 → v1.0.1**: Clarification (e.g., "Solo Workflow" definition refined)

**Effect**: Features developed under different constitution versions can coexist. Plans reference constitution version for traceability.

### Constitution Version Decision Tree

```
Did principle semantics change?
├─ No  → PATCH (wording clarity)
└─ Yes
   ├─ Backward compatible? (old features still valid)
   │  └─ Yes → MINOR (new principle added)
   └─ No → MAJOR (principle removed or redefined)
```

### Example Constitution Changes

**MAJOR (1.0.0 → 2.0.0)**:

- Remove Principle II (now allow branch creation)
- Change Principle I from "Claude Code-only" to "Claude/Cursor support"

**MINOR (1.0.0 → 1.1.0)**:

- Add Principle VII: Performance targets for CLI commands
- Expand Principle VI with testing requirements

**PATCH (1.0.0 → 1.0.1)**:

- Clarify "Solo Developer" definition
- Fix typos in Principle III rationale
- Add examples to enforcement sections

---

## Cross-References

**Related Architectural Concepts**:

- [Architecture Layer 4](03-architecture.md#layer-4-constitutional-enforcement) - Constitutional enforcement as architecture layer
- [Philosophy: Constitution as Type System](02-philosophy.md#constitution-as-type-system) - Philosophical foundation
- [/plan Command](04-commands-core.md#plan---create-implementation-plan) - Where gates are enforced

**Related Workflow Elements**:

- [Phase Structure](05-commands-phase.md) - How phases interact with gates
- [CLAUDE.md Integration](02-philosophy.md#claudemd-as-governance-document) - Constitution delivery mechanism

**Related Development Practices**:

- [Dogfooding Workflow](06-commands-support.md#dogfooding-workflow) - Self-application in practice
- [Version Discipline](04-commands-core.md#version-tracking) - Release process details

---

**Navigation**: [← Bash Automation](07-bash-automation.md) | [AI Patterns →](09-ai-patterns.md)

---

## Keywords

constitution, type system, six principles, Claude Code-only, solo workflow, minimal divergence, GitHub releases, version discipline, dogfooding, self-application, constitutional gates, complexity tracking, principle enforcement, governance model, semantic versioning, CLAUDE.md integration, architectural constraints, trade-off documentation, upstream compatibility, fork independence
