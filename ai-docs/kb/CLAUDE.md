# Spec-Kit Documentation Index

## Overview

This folder contains comprehensive documentation for spec-kit, a toolkit for Specification-Driven Development (SDD) using AI coding assistants. The documentation has been split into focused, manageable files optimized for AI context windows.

**Purpose**: This index provides AI assistants with a quick understanding of the documentation structure and contents without needing to load all files.

## Documentation Structure

- **Total Files**: 12 (README.md + 11 numbered documents)
- **Total Lines**: ~6,000 lines of documentation
- **Organization**: Progressive learning path from overview to implementation details
- **Optimization**: Each file sized for AI context windows (250-950 lines)

## File Summaries

### README.md (226 lines)

- Navigation guide with three learning paths: Quick Understanding (30 min), Implementation (2-3 hrs), Deep Understanding (4-5 hrs)
- Cross-reference matrix showing relationships between 11 documents organized by topic (Architecture, Commands, Templates, etc.)
- Quick lookup sections for architecture concepts, command reference, key mechanisms, and bash scripts with direct file links
- Document structure template showing consistent format: Purpose, Related Files, Keywords, Content, Cross-References
- Keywords index categorizing core concepts (SDD, Power Inversion), technical components (CLI, Templates), workflow commands, and AI patterns
- Future plans for migration to Claude Code marketplace-style plugins with component-based understanding
- Document stats showing 11 focused files (~3,280 lines) covering overview, philosophy, architecture, commands, templates, bash automation, constitution, AI patterns, workflows, and insights

### 01-overview.md (409 lines)

- Spec-kit inverts traditional development paradigm: specifications are executable source of truth that generate code (not documentation artifacts)
- 8-command workflow enforces phase discipline: /constitution → /specify → /clarify → /plan → /tasks → /analyze → /implement with constitutional gates at each phase
- 4-layer architecture: CLI Orchestrator (Python) → Template Engine (Markdown) → State Automation (Bash/JSON) → Constitutional Enforcement (governance document)
- Core innovation treats AI as disciplined specification engineer using templates with execution flows to constrain LLM output space from 10^n to 10^1 acceptable outputs
- Optimized for solo developers on Unix-like systems using Claude Code with [NEEDS CLARIFICATION] markers preventing hallucination and monorepo support
- Ideal for specification-first workflows with architectural consistency enforcement; not suitable for large teams, quick prototypes, or Windows-first environments
- File structure includes .specify/ (templates/scripts/memory), .claude/ (commands/CLAUDE.md), and specs/ (feature directories with spec.md/plan.md/tasks.md)

### 02-philosophy.md (380 lines)

- Power inversion paradigm: Specifications become executable source of truth that generate code (disposable artifacts), inverting traditional "code is truth, specs drift" model where specifications never drift because they generate current code
- Specifications as truth vs code as truth: Traditional flow is "Spec → Manual Translation → Code (truth) → Drift", spec-kit flow is "Specification (truth) → AI Generation → Code (disposable) → Evolve specification, regenerate code"
- Three enabling trends converged to make SDD practical: (1) AI capability threshold - GPT-4/Claude 3+ cross production-ready quality with 100k+ context windows, (2) Complexity growth - modern systems integrate 10+ microservices making manual alignment error-prone, (3) Accelerating change - continuous deployment and rapid pivots require systematic regeneration
- Executable specifications as lingua franca: Development activities map to specification operations (maintaining software = evolving specs, debugging = fixing specs that generate incorrect code, refactoring = restructuring specs), shifting team focus from implementation details (which library/framework) to intent focus (what problem, precise requirements, edge cases)
- Disposable code concept: Code is generated artifact that can be thrown away and regenerated (framework updates, architecture changes, performance optimization, dependency vulnerabilities), while specifications are permanent because they're written in natural language with no framework lock-in, express intent not implementation, validated by tests
- Constraint-driven generation principle: Templates constrain LLM output from 10^n possible hallucination-prone outputs to 10^1 acceptable enforced outputs through execution flow pseudocode, [NEEDS CLARIFICATION] placeholder system, constitutional gates, structured sections, and checklists
- Trade-offs and optimal use cases: Works best for greenfield projects with well-understood domains, solo/small teams, high change rate, AI-friendly tech stacks; challenging for legacy systems, novel domains, large distributed teams, performance-critical code; upfront specification cost pays off after >2 changes or >6 months lifespan

### 03-architecture.md (486 lines)

- **4-layer separation model**: Layer 1 CLI Orchestrator (Python 3.11+ with Typer/Rich, 1221 lines single file) bootstraps from GitHub releases → Layer 2 Template Engine (executable Markdown specs with YAML frontmatter, pseudocode flows, validation gates) constrains LLM behavior → Layer 3 State Automation (Bash scripts with JSON-only stdout contracts) handles filesystem state → Layer 4 Constitutional Enforcement (type system for architecture) validates fork-specific principles
- **Layer 1 solo developer optimizations**: Hardcoded constants (`AI_AGENT="claude"`, `SCRIPT_TYPE="sh"`, `repo_owner="anagri"`) eliminate ~200 lines of multi-agent conditional logic; downloads versioned templates from `anagri/spec-kit` releases with GitHub token authentication; `StepTracker` class provides Rich-based progress UI; delegates all business logic to templates/scripts
- **Layer 2 constraint mechanisms**: Templates reduce LLM output space from 10^n unconstrained outputs → 10^3 via execution flow → 10^1 via constitutional gates; uses three placeholder types (static `[FEATURE]`, uncertainty `[NEEDS CLARIFICATION]`, runtime `{SCRIPT}/$ARGUMENTS`); prevents premature implementation, forces explicit uncertainty, enforces test-first thinking through required checklist sections
- **Layer 3 JSON communication contract**: Scripts output **only JSON** to stdout (errors to stderr) creating clean state isolation between filesystem operations (mkdir/cp/chmod) and Claude's pure transformations; example contract `{"FEATURE_ID":"003-name","SPEC_FILE":"/path","FEATURE_NUM":"003","FEATURE_DIR":"/path"}` prevents race conditions through explicit input/output contracts
- **Layer 3 solo workflow model**: **No git branch creation** in `create-new-feature.sh` (line 82-84)—feature = directory not branch; `SPECIFY_FEATURE` environment variable tracks current context with fallback to latest feature directory; faster iteration without branch switching/merge conflicts; supports `--no-git` repositories
- **Monorepo support**: `common.sh:get_repo_root()` prioritizes `.specify` marker over `.git` enabling multiple independent spec-kit projects in single git repository; each project maintains independent feature numbering without cross-project contamination
- **Layer 4 constitutional enforcement**: Six fork-specific principles (Claude Code-Only, Solo Developer Workflow, Minimal Divergence, GitHub Release Distribution, Version Discipline NON-NEGOTIABLE, Dogfooding) enforced through template gates (compile-time), Claude reasoning (runtime), code review (manual), and hardcoded CLI constants (structural); violations treated as "type errors" requiring documentation in complexity tracking table with justification

### 04-commands-core.md (957 lines)

- Five core commands form strict sequential workflow: /constitution (project governance setup with semantic versioning and template propagation) → /specify (feature spec from natural language with ambiguity markers) → /plan (technical design with dual constitutional gates and STOP before task generation) → /tasks (dependency-ordered task breakdown with TDD enforcement) → /implement (phase-by-phase execution with atomic progress tracking)
- Command dependency graph enforces phase separation: Constitution (once per project, v1.0.0 semantic versioning) → Specify (per feature with sequential numbering 001-003) → Plan (pre-research AND post-design constitutional gates) → Tasks (immediate executability with [P] parallel markers) → Implement (TDD ordering with halt-on-failure for sequential tasks)
- Phase separation is strictly enforced to prevent premature decisions: /specify creates spec.md with NO technical decisions, /plan generates plan.md/data-model.md/contracts/ with NO task breakdown, /tasks produces tasks.md without executing implementation, /implement executes following TDD order (tests before code)
- Constitutional gates validate twice during /plan: pre-research gate blocks Phase 0 if MUST principles violated, post-design gate catches new violations after Phase 1 and forces refactoring, Complexity Tracking table documents acceptable violations with justification
- TDD ordering in /tasks enforced by rules: each contract file generates contract test task marked [P] before endpoint implementation, integration tests created in Core phase, unit tests deferred to Polish phase, tests always execute before implementation tasks in /implement
- JSON outputs from bash scripts provide structured data: create-new-feature.sh returns FEATURE_ID/SPEC_FILE/FEATURE_NUM for sequential numbering, setup-plan.sh returns FEATURE_SPEC/IMPL_PLAN/FEATURE_DIR for plan phase, check-prerequisites.sh validates context availability before tasks/implement
- File artifacts follow strict hierarchy: .specify/memory/constitution.md (project governance with version and clarification session tracking) → specs/###-feature-name/ (feature directory) → spec.md (requirements), plan.md/research.md/data-model.md/contracts/ (design), quickstart.md (integration scenarios), tasks.md (numbered T001-T020 with [P] markers and [X] completion tracking)

### 05-commands-clarify.md (620 lines)

- Three enhancement commands resolve ambiguities and validate consistency: /clarify (interactive specification refinement), /analyze (non-destructive cross-artifact validation), /clarify-constitution (governance principle resolution)
- 10 taxonomy categories systematically detect ambiguities: Functional Requirements Scope, Data Model Structure, Access Control, Interaction/UX Flow, Non-Functional Attributes, Integration/Dependencies, Edge Cases/Failure Handling, Constraints/Tradeoffs, Terminology/Consistency, Completion Signals/Placeholders
- /analyze performs 6 detection passes before implementation: Duplication (near-duplicate requirements), Ambiguity (vague adjectives without metrics), Underspecification (missing outcomes/criteria), Constitution Alignment (MUST principle violations), Coverage Gaps (requirements with zero tasks), Inconsistency (terminology drift/conflicting requirements)
- Maximum 5 questions rule prevents analysis paralysis with one-at-a-time interactive flow that saves spec after each answer (atomic updates, early termination via "done" command, incremental integration)
- Interactive resolution uses taxonomy-driven prioritization with multiple answer formats: multiple choice options with descriptions, short answer (5 words max), immediate integration into appropriate spec sections with line references
- Severity assignment for analysis findings: CRITICAL (constitution violations/zero coverage/missing core artifacts), HIGH (duplicate requirements/ambiguous security criteria/untestable acceptance), MEDIUM (terminology drift/missing NFR coverage/underspecified edge cases), LOW (style improvements/minor redundancy)
- /clarify workflow position after /specify before /plan; /analyze position after /tasks before /implement; /clarify-constitution position after /constitution if [NEEDS CLARIFICATION] markers exist

### 06-templates.md (258 lines)

- Templates as constraint/reduction functions: Transform unconstrained LLM output space (10^n hallucination-prone) → constrained valid outputs (10^3) → acceptable enforced outputs (10^1) through systematic constraint application
- Seven constraint mechanisms: (1) prevent premature implementation details via abstraction focus, (2) force explicit [NEEDS CLARIFICATION] uncertainty markers to prevent guessing, (3) structured thinking through checklist-based "unit tests", (4) constitutional compliance through pre-implementation gates (Simplicity/Anti-Abstraction with violation tracking), (5) hierarchical detail management separating high-level specs from implementation-details/ files, (6) test-first thinking with contract → test → source file creation order, (7) prevent speculative features via validation checklists
- Execution flow as pseudocode: Templates contain executable instructions for Claude with 8-step workflow (parse input → extract concepts → mark unclear aspects with [NEEDS CLARIFICATION] → fill scenarios → generate requirements → identify entities → run review checklist → return success/error), creating deterministic architectural workflows from probabilistic text generation
- Four placeholder types: Template variables ([FEATURE], [DATE]) filled by Claude during command execution, uncertainty markers ([NEEDS CLARIFICATION]) filled by user via /clarify, script interpolation ({SCRIPT}, $ARGUMENTS) filled at runtime by command invocation, environment variables (${SPECIFY_FEATURE}) filled during bash execution for context passing
- Preventing hallucination through constraint layering: Four-layer approach with (1) template structure enforcing information architecture/checklists/examples, (2) explicit instructions ("mark ambiguities don't guess", "WHAT not HOW"), (3) constitutional gates requiring complexity/abstraction justification, (4) execution flow with step-by-step pseudocode/error conditions/success criteria
- Critical "Never Guess" rule: [NEEDS CLARIFICATION] markers must never be guessed by Claude; workflow requires explicit user clarification via /clarify command, preventing most common LLM failure mode of hallucinating plausible but incorrect details
- Templates as quality assurance framework: Embedded self-review mechanisms including requirement completeness checks (no unresolved markers, testable requirements, measurable success criteria), detail level validation (separating high-level from technical specs), and constitutional compliance gates (justify each complexity/abstraction violation in tracking table with rejected alternatives)

### 07-bash-automation.md (445 lines)

- State isolation model separates Claude's pure transformations (read JSON, generate content) from bash scripts' state mutations (mkdir, cp, git ops), preventing race conditions and enabling independent testing with JSON contracts on stdout and errors on stderr
- JSON communication contracts enable structured bash-to-Claude data flow with parseable outputs ({"FEATURE_ID":"003-user-auth","SPEC_FILE":"/path/to/specs/003-user-auth/spec.md"}), supporting --json flag for machine parsing and human-readable fallback for direct CLI usage
- Solo developer workflow removes git branch creation ceremony (deleted upstream line 74: git checkout -b) with SPECIFY_FEATURE environment variable providing explicit context override, and fallback to scanning specs/ for highest-numbered directory as implicit context detection
- Monorepo support via .specify priority over .git in get_repo_root() enables multiple independent spec-kit projects in single git repository (project-a/.specify/ and project-b/.specify/ each get separate feature numbering and agent context without interference)
- common.sh utilities provide single source of truth for path resolution (get_repo_root, get_current_feature, get_feature_paths) with 10#$number forcing base-10 interpretation to prevent octal errors, and two-tier fallback (SPECIFY_FEATURE env var → highest-numbered directory scan)
- create-new-feature.sh implements sequential feature numbering with slugification (3-word limit: "Real-time chat system with message history" → 003-real-time-chat) and JSON output contract for structured data (FEATURE_ID, SPEC_FILE, FEATURE_NUM) enabling Claude to reliably parse results
- SPECIFY_FEATURE environment variable enables explicit context override for multi-feature work, testing with synthetic environments, and CI/CD automation, with fallback to filesystem scanning for implicit context in solo developer workflows where branches aren't needed

### 08-constitution.md (515 lines)

- Constitution functions as a type system for architectures where violations are treated as "type errors" requiring explicit justification or refactoring
- Six fork-specific principles enforce governance: I) Claude Code-only support (hardcoded, no multi-agent abstraction), II) Solo developer workflow (SPECIFY_FEATURE env var, no git branch coupling), III) Minimal divergence from upstream (document every fork change), IV) GitHub release distribution (anagri/spec-kit releases), V) Version discipline (NON-NEGOTIABLE: bump pyproject.toml + CHANGELOG.md for every CLI change), VI) Dogfooding (dual SOURCE/INSTALLED structure where .specify/ and .claude/ are frozen during development)
- Constitutional gates embedded in /plan template with two evaluation checkpoints (before Phase 0 research, after Phase 1 design) forcing PASS/FAIL evaluation against all six principles
- Complexity tracking table mandates documentation for gate failures: columns for Violation, Why Needed, and Simpler Alternative Rejected Because
- Constitution itself uses semantic versioning (MAJOR: principle removal/redefinition, MINOR: new principle added, PATCH: clarifications) enabling coexistence of features developed under different governance versions
- Enforcement mechanisms include hardcoded constants (AI_AGENT="claude"), removed code with rationale comments (git checkout -b removal), CLI parameter restrictions (repo_owner="anagri"), manual release process, and dogfooding dual-file structure preventing accidental SOURCE/INSTALLED synchronization
- Trade-offs explicitly accepted: cannot switch AI agents without architectural changes, no true isolation for breaking change experiments, manual version discipline prone to human error, dual file structure initially confusing, upstream features require manual adaptation

### 09-ai-patterns.md (523 lines)

- Templates are pseudocode execution flows that Claude follows step-by-step, not suggestions - contains IF-THEN conditionals, ERROR triggers, and explicit Return statements that constrain LLM output from infinite possibilities to deterministic outcomes
- Hallucination prevention via [NEEDS CLARIFICATION: specific question] markers forces Claude to mark ambiguities instead of guessing - prevents assuming auth methods/password policies/session timeouts and requires explicit user decisions before implementation
- Execution Status checklists provide real-time progress tracking where Claude updates checkboxes as each step completes, enabling accountability (can't skip steps), transparency (user sees current position), and error recovery (knows which steps succeeded before failure)
- Constitutional reasoning loop triggers automated architectural validation gates where Claude loads constitution, evaluates plan against principles (Library-First, Test-First), and either passes checkpoint or justifies exception in Complexity Tracking table with documented trade-off analysis
- Cascading context management builds progressive context across workflow stages - /specify outputs spec.md → /plan reads spec.md + outputs plan.md/research.md → /tasks reads both + outputs tasks.md → /implement reads all with prerequisite validation preventing execution without required artifacts
- Error handling uses explicit ERROR conditions at each step (script fails, JSON invalid, template missing) causing Claude to stop execution, report specific failure, suggest recovery action (e.g., "Run speclaude init --here"), and preserve execution status showing exactly where failure occurred
- Parallel execution awareness via [P] markers enables dependency-aware concurrent task execution where Claude analyzes task dependencies, identifies parallel-safe operations (different files/no shared state), executes independent tasks concurrently (Phase 1: T006/T007/T009), then runs sequential dependent tasks (Phase 2: T008 waits for T006+T007, Phase 3: T010 waits for T008+T009)

### 10-workflows.md (890 lines)

- Complete 8-step real-time chat example demonstrates full lifecycle: constitution (6 principles) → specify (8 requirements) → clarify (5 interactive Q&A) → plan (6 artifacts including contracts/data-model) → tasks (37 tasks, 18 parallel-safe) → analyze (coverage validation catches missing test) → implement (38 tasks with TDD, 1200 req/s achieved)
- Three workflow variations: Minimal (5 commands, 2-4 hrs, higher risk for simple features), Recommended (7 commands, 3-6 hrs, lower risk with clarify/analyze), Iterative Refinement (loop specify→clarify→plan until requirements stable, then continue)
- Team collaboration patterns: Spec Review Gate (commit spec.md for PM approval before implementation), Shared Constitution (team-wide principles in version control), Parallel Feature Development (isolated specs/001-\* directories, no branch conflicts, shared constitution ensures consistency)
- Troubleshooting scenarios with actual error messages and resolutions: Missing Prerequisites (enforce /specify before /plan), Constitution Gate Failure (catch "No wrapper abstractions" violations early), Coverage Gaps (/analyze detects missing tasks for requirements, suggests remediation)
- Command sequences for different use cases: Quick Feature (specify→plan→tasks→implement for simple endpoints), Complex Feature (full 7-command workflow for chat/payment/search), Design-Only (stop after /tasks for estimation), Refinement After Feedback (regenerate spec→plan→tasks with updated requirements)
- Each workflow step shows actual Claude responses with artifacts generated: /plan creates 6 files (plan.md, research.md, data-model.md, contracts/\*.yaml, quickstart.md), /tasks generates 37 tasks across 5 phases (Setup/Test/Core/Integration/Polish), /analyze builds semantic models and runs 6 detection passes with coverage matrix
- Real outputs demonstrate automation: constitution check shows 6/6 gates passed, clarify integrates 5 answers directly into spec.md sections, implement auto-marks [X] in tasks.md and reports performance targets (95ms p95 latency vs 100ms target, 1200 req/s vs 1000 target)

### 11-insights.md (383 lines)

- Ten key design strengths including paradigm inversion (specs as truth, not code), constraint-driven generation (templates as compiler directives reducing LLM output space), phase separation enforcement (Spec → Plan → Tasks as hard boundaries), and solo developer optimization (no git branches, Unix-only, ~200 LOC removed)
- Ten critical design insights treat templates as reduction functions (10^n → 10^1 output space), JSON as state boundary (read-only view of side effects), constitution as type system (executable constraints with version semantics), and constraint paradox (extension easier when foundation is stable and singular)
- Comparison with traditional development shows inversion of source of truth (code vs specifications), maintenance approach (edit code vs evolve specs), and ambiguity handling (developer assumptions vs [NEEDS CLARIFICATION] markers enforced by templates)
- Comparison with other AI tools (Copilot, Cursor, generators) highlights spec-kit as methodology enforced by tooling with strict phase separation, constitutional enforcement, and 8-command workflow vs ad-hoc prompts or single-shot generation
- Trade-offs and limitations include removed features (git branching, multi-agent, PowerShell) for solo dev optimization, known limitations (learning curve, token costs, regeneration overhead), and areas for improvement (incremental planning, transaction logs, lite templates)
- Ideal use cases are solo developer projects, specification-heavy domains (APIs/CLIs), greenfield development, and exploratory prototyping; less ideal for large teams, legacy codebases, GUI-heavy applications, and performance-critical systems
- Future directions maintain constraint as optimization principle with near-term evolution paths (incremental planning, feature-specific constitutions, multi-constitution support) while preserving single-agent, single-script-type, single-workflow focus

## Quick Reference

### Core Commands

- `/constitution` - Create project governance principles (once per project)
- `/specify` - Generate feature specification from natural language
- `/clarify` - Interactive ambiguity resolution (optional but recommended)
- `/plan` - Create implementation plan with tech stack decisions
- `/tasks` - Break down plan into actionable tasks
- `/analyze` - Validate cross-artifact consistency (optional but recommended)
- `/implement` - Execute tasks to generate code
- `/clarify-constitution` - Resolve governance ambiguities (if markers exist)

### Key Concepts

- **SDD (Specification-Driven Development)** - Specs as executable truth generating code
- **Power Inversion** - Code is disposable, specifications are permanent
- **[NEEDS CLARIFICATION]** - Explicit uncertainty markers preventing hallucination
- **Constitutional Gates** - Architectural validation checkpoints in /plan
- **Phase Separation** - Strict boundaries preventing premature decisions
- **Constraint Reduction** - Templates transform 10^n outputs to 10^1 acceptable
- **Solo Workflow** - No git branches, SPECIFY_FEATURE env var for context

## Usage Guide for AI Assistants

When answering questions about spec-kit:

1. **For overview questions**: Start with 01-overview.md summary, then reference specific sections
2. **For philosophy/paradigm questions**: Use 02-philosophy.md for power inversion and SDD concepts
3. **For technical implementation**: Reference 03-architecture.md (4-layer model) and relevant layer details
4. **For command usage**: Use 04-commands-core.md for main workflow, 05-commands-clarify.md for enhancements
5. **For template mechanics**: Reference 06-templates.md for constraint mechanisms
6. **For scripting details**: Use 07-bash-automation.md for JSON contracts and state management
7. **For governance questions**: Reference 08-constitution.md for principles and enforcement
8. **For AI behavior**: Use 09-ai-patterns.md for how Claude processes templates
9. **For practical examples**: Reference 10-workflows.md for end-to-end scenarios
10. **For comparisons/analysis**: Use 11-insights.md for trade-offs and design decisions

This index enables quick context loading without reading entire documentation files.
