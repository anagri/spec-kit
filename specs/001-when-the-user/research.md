# Research: Constitution Command Clarification Flow

**Feature**: 001-when-the-user | **Date**: 2025-10-05

## Internal Documentation Consulted

### docs/PHILOSOPHY.md
- **Layer 2 (Templates)**: Templates are executable specifications with YAML frontmatter, execution flows, and validation gates
- **Template Constraints Guide Claude**: `[NEEDS CLARIFICATION]` markers prevent guessing, force explicit uncertainty
- **Separation of Concerns**: Each template handles one responsibility (constitution vs spec clarification)
- **Extension Pattern**: New slash commands follow: frontmatter → execution flow → validation → output
- **Constitutional Gates**: Templates enforce principles through checklist validation

### docs/quickstart.md
- **Clarification Workflow**: `/clarify` runs after `/specify` to refine specs before planning
- **Interactive Pattern**: Ask targeted questions, update document incrementally
- **CLI Tool Pattern**: For tools like spec-kit, use `template-contracts.md` instead of `data-model.md`

### CLAUDE.md
- **Slash Commands Location**: `.claude/commands/*.md` for Claude Code
- **Template Placeholders**: `$ARGUMENTS` for user input, `{SCRIPT}` for bash paths
- **Dogfooding Rules**: SOURCE templates in `templates/commands/` → INSTALLED in `.claude/commands/`
- **No Script Changes**: Templates-only feature, reuse existing path resolution

### Existing specs/
- Only one spec exists (this feature), no similar patterns to reference

## Research Findings

### 1. Clarification Pattern (from /clarify command)

**Decision**: Reuse `/clarify` command structure for `/clarify-constitution`

**Rationale**:
- Proven interactive question-answer workflow
- Sequential questioning with max 5 questions
- Multiple choice or short answer formats
- Incremental document updates with session tracking
- Strong precedent in codebase

**Key Pattern Elements**:
```markdown
1. Run prerequisite script to get paths (check-prerequisites.sh --json --paths-only)
2. Load document, scan for ambiguities using taxonomy
3. Generate prioritized question queue (max 5)
4. Sequential questioning loop:
   - Present ONE question at a time
   - Validate answer
   - Integrate immediately into document
   - Save after each update
5. Report completion with coverage summary
```

**Alternatives Considered**:
- Batch questions (all at once): Rejected - overwhelming, less iterative
- AI-driven completion: Rejected - violates NFR-001 (no hallucination)
- Required fields form: Rejected - too rigid, doesn't handle varying project needs

### 2. Constitution-Specific Question Categories

**Decision**: Define constitution-specific taxonomy separate from spec taxonomy

**Rationale**:
- Constitutions have different structure than specs (principles vs requirements)
- Need to ask about: architectural principles, tech constraints, workflow, governance
- Spec clarification taxonomy focuses on: functional scope, data model, UX, NFRs

**Constitution Question Categories**:
1. **Architectural Principles** (core development philosophy)
   - Test-first vs code-first
   - Library minimalism vs rich ecosystem
   - Monolith vs microservices
   - CLI-only vs UI support

2. **Technology Constraints** (hard technical choices)
   - Language/version
   - Framework preferences
   - Platform targets (mobile, web, desktop, server)
   - Database technology

3. **Development Workflow** (team/process decisions)
   - Solo vs team development
   - Branching strategy (trunk-based, git-flow, feature branches)
   - Release cadence
   - Deployment approach

4. **Governance Policies** (meta-process)
   - Amendment process (who can change constitution)
   - Compliance review frequency
   - Version semantics
   - Documentation requirements

**Alternatives Considered**:
- Reuse spec taxonomy: Rejected - doesn't map to constitutional structure
- Single "principles" category: Rejected - too broad, misses critical governance aspects
- External template: Rejected - constitution is project-specific, not industry-standard

### 3. [NEEDS CLARIFICATION] Marker Handling

**Decision**: Constitution template generates with markers, `/clarify-constitution` removes them

**Rationale**:
- Explicit uncertainty principle from PHILOSOPHY.md
- Prevents hallucination (NFR-001)
- Clear visual indicator of incomplete sections
- Matches existing pattern in specs

**Implementation Approach**:
```markdown
/constitution "minimal input"
→ Generates constitution with:
  Principle I: [NEEDS CLARIFICATION]
  Principle II: [NEEDS CLARIFICATION]
  Technology: [NEEDS CLARIFICATION]
  ...

/clarify-constitution
→ Detects markers
→ Asks questions about each marked section
→ Replaces markers with user-provided content
```

**Alternatives Considered**:
- Generate nothing until complete: Rejected - no starting point for clarification
- Generate "best guess" with footnotes: Rejected - still hallucination, users might miss footnotes
- Use TODO comments: Rejected - less visible than `[NEEDS CLARIFICATION]`

### 4. Iteration Limits

**Decision**: Soft limit of 3 clarification rounds with warning

**Rationale** (from clarification answer in spec):
- Prevents infinite loops
- Allows flexibility for complex projects
- Warning educates user about typical completion
- Respects user override for edge cases

**Implementation**:
- Track clarification session count in constitution metadata
- After 3rd session: "Warning: Multiple clarification rounds detected. Consider direct file editing if AI misunderstands."
- No hard block - user can continue

**Alternatives Considered**:
- Hard limit: Rejected - too restrictive, blocks legitimate complexity
- No limit: Rejected - could lead to poor UX with endless loops
- Per-section limits: Rejected - adds complexity, unclear benefit

### 5. Separation of /clarify vs /clarify-constitution

**Decision**: Separate commands (FR-004)

**Rationale**:
- Different document structures (spec vs constitution)
- Different question taxonomies
- Avoids conditional logic in single command
- Clear user mental model (spec clarification vs constitution clarification)
- Simpler template maintenance

**Implementation**:
- `/clarify` → operates on `specs/###-feature/spec.md`
- `/clarify-constitution` → operates on `.specify/memory/constitution.md`
- Shared pattern, different execution contexts

**Alternatives Considered**:
- Single `/clarify` with mode parameter: Rejected - complex template logic, unclear to users
- Auto-detect document type: Rejected - implicit behavior, error-prone
- Merged into `/constitution`: Rejected - violates single responsibility, creates monolithic template

### 6. User Disagreement Handling

**Decision**: Allow manual file editing as escape hatch (FR-011)

**Rationale** (from clarification answer in spec):
- AI interpretation isn't perfect
- Users should have final control
- Direct editing faster than rephrasing repeatedly
- Markdown files are human-readable/editable

**Implementation**:
- In clarification loop: If user says "AI doesn't understand"
- Response: "You can directly edit `.specify/memory/constitution.md` to make changes. The file is plain markdown."
- No validation on manual edits (trust user)

**Alternatives Considered**:
- Force AI understanding: Rejected - wastes time, frustrates users
- Guided editing mode: Rejected - over-engineering, plain editing works fine
- Lock file during clarification: Rejected - prevents escape hatch

## Summary

**All Technical Context items resolved**: ✓

**Key Decisions**:
1. Reuse `/clarify` pattern for interactive clarification workflow
2. Define constitution-specific question taxonomy (4 categories)
3. Use `[NEEDS CLARIFICATION]` markers in generated constitutions
4. Implement soft limit (3 rounds) with warning, no hard block
5. Keep `/clarify` and `/clarify-constitution` as separate commands
6. Support manual file editing as escape hatch for AI miscommunication

**Internal Docs Referenced**:
- docs/PHILOSOPHY.md: Layer 2 template patterns, explicit uncertainty principle
- CLAUDE.md: Slash command structure, dogfooding workflow
- .claude/commands/clarify.md: Full clarification execution flow
- .claude/commands/constitution.md: Constitution generation pattern

**No external research needed** - all patterns and decisions derived from existing codebase architecture and constitutional principles.
