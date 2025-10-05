# Contract: Constitution Template with Clarification Support

**Version**: 2.0.0 (adds clarification marker support)
**Type**: Command Template Modification
**File**: `templates/commands/constitution.md`

## Change Summary

**Baseline**: Existing `/constitution` command (v1.x)
**New Feature**: Support for `[NEEDS CLARIFICATION]` markers when user input is insufficient
**Backward Compatibility**: ✓ (comprehensive input still generates complete constitution)

## Modified Execution Flow

### Step 2: Placeholder Collection (MODIFIED)

**Original Behavior**:
```markdown
2. Collect/derive values for placeholders:
   - If user input supplies value, use it
   - Otherwise infer from repo context (README, docs, prior versions)
   - For governance dates: use today or ask
```

**New Behavior**:
```markdown
2. Collect/derive values for placeholders:
   - If user input supplies value, use it
   - If placeholder has sufficient context from repo, infer
   - If neither: Mark section with [NEEDS CLARIFICATION]
   - Track which sections are marked (for Step 8 summary)
```

**Decision Logic**:
```
FOR EACH placeholder:
  IF $ARGUMENTS contains explicit value:
    USE user-provided value
  ELSE IF README/docs/existing constitution has clear value:
    INFER from repo context
  ELSE:
    INSERT "[NEEDS CLARIFICATION]" marker
    ADD to incomplete_sections list
```

**Examples**:

**Scenario 1: Comprehensive Input**
```
User: /constitution "This project uses Python 3.11 with FastAPI. Solo developer, trunk-based workflow. Test-first development principle."

Result:
- Language: Python 3.11 ✓
- Framework: FastAPI ✓
- Workflow: Trunk-based ✓
- Principle: Test-first ✓
- [NO MARKERS - complete constitution generated]
```

**Scenario 2: Minimal Input**
```
User: /constitution "Python web app"

Result:
- Language: Python [NEEDS CLARIFICATION: version]
- Framework: [NEEDS CLARIFICATION: FastAPI vs Django vs Flask]
- Workflow: [NEEDS CLARIFICATION]
- Principle: [NEEDS CLARIFICATION]
- [4 markers - suggests /clarify-constitution]
```

**Scenario 3: Partial Input**
```
User: /constitution "Python 3.11 project, test-first principle"

Result:
- Language: Python 3.11 ✓
- Framework: [NEEDS CLARIFICATION]
- Workflow: [NEEDS CLARIFICATION]
- Principle: Test-first ✓
- [2 markers - suggests /clarify-constitution]
```

### Step 3: Draft Constitution (MODIFIED)

**Original Behavior**:
```markdown
3. Draft updated constitution:
   - Replace every placeholder with concrete text
   - No bracketed tokens left (except intentional template slots)
   - Justify any remaining placeholders
```

**New Behavior**:
```markdown
3. Draft updated constitution:
   - Replace placeholders with concrete text OR [NEEDS CLARIFICATION]
   - Markers indicate missing user input (not AI guesses)
   - Preserve heading hierarchy
   - Don't hallucinate content for marked sections
```

**Marker Placement Rules**:
```markdown
✓ Valid Placements:
- **Language**: [NEEDS CLARIFICATION: Python version]
- **Rationale**: [NEEDS CLARIFICATION]
- List item: - [NEEDS CLARIFICATION: specify principle]

✗ Invalid Placements:
- ### [NEEDS CLARIFICATION]  (not in headings)
- ## Principle [NEEDS CLARIFICATION]  (not in headings)
```

**Content Rules**:
- **No speculation**: Don't write "probably uses..." or "likely requires..."
- **No partial guesses**: Either complete value or full `[NEEDS CLARIFICATION]`
- **Marker specificity**: Include hint in brackets when helpful
  - Good: `[NEEDS CLARIFICATION: FastAPI vs Django vs Flask]`
  - Okay: `[NEEDS CLARIFICATION]`
  - Bad: `[NEEDS CLARIFICATION: framework (pick one)]` (too prescriptive)

### Step 7: Write Constitution (MODIFIED)

**Original Behavior**:
```markdown
7. Write completed constitution to `.specify/memory/constitution.md`
```

**New Behavior**:
```markdown
7. Write constitution to `.specify/memory/constitution.md`
   - Include [NEEDS CLARIFICATION] markers if present
   - Initialize session metadata: <!-- Clarification Sessions: 0 -->
   - If markers exist, prepare /clarify-constitution suggestion for Step 8
```

**File Structure with Markers**:
```markdown
<!--
SYNC IMPACT REPORT
[standard sync report content]
-->

<!-- Clarification Sessions: 0 -->

# Project Constitution

## Core Principles

### I. [Principle Name from user OR "Architectural Principle"]
[NEEDS CLARIFICATION: Describe the core architectural principle]

**Rationale**: [NEEDS CLARIFICATION]

### II. Technology Stack
**Language**: Python [NEEDS CLARIFICATION: version]
**Framework**: [NEEDS CLARIFICATION: FastAPI vs Django vs Flask]

## Technology Constraints
[NEEDS CLARIFICATION: Specify technical constraints]

## Development Workflow
[NEEDS CLARIFICATION: Solo vs team, branching strategy, release process]

## Governance
**Amendment Process**: [NEEDS CLARIFICATION]
**Compliance**: [NEEDS CLARIFICATION]

**Version**: 1.0.0 | **Ratified**: 2025-10-05 | **Last Amended**: 2025-10-05
```

### Step 8: Final Summary (MODIFIED)

**Original Behavior**:
```markdown
8. Output final summary:
   - New version and bump rationale
   - Files flagged for manual follow-up
   - Suggested commit message
```

**New Behavior**:
```markdown
8. Output final summary:
   - New version and bump rationale
   - Count of [NEEDS CLARIFICATION] markers (if any)
   - Files flagged for manual follow-up
   - Next command:
     * /clarify-constitution (if markers present)
     * /specify (if constitution complete)
   - Suggested commit message
```

**Output Format with Markers**:
```markdown
Constitution created at .specify/memory/constitution.md

Version: 1.0.0 (new constitution)

⚠ Incomplete Sections (4):
- Architectural Principle (Principle I)
- Framework (Technology Stack)
- Development Workflow
- Governance policies

This constitution has 4 sections needing clarification.

Next command: /clarify-constitution

The clarification command will ask targeted questions to complete these sections
without making assumptions.

---

Suggested commit message:
docs: create constitution v1.0.0 (needs clarification)
```

**Output Format without Markers** (comprehensive input):
```markdown
Constitution created at .specify/memory/constitution.md

Version: 1.0.0 (new constitution)

✓ All sections complete

Next command: /specify

---

Suggested commit message:
docs: create constitution v1.0.0 (Python 3.11, FastAPI, test-first)
```

## Marker Contract

### Syntax
```
[NEEDS CLARIFICATION]
[NEEDS CLARIFICATION: <optional hint>]
```

### Semantic Meaning
- **User Input Missing**: Placeholder cannot be filled from $ARGUMENTS or repo context
- **No AI Guess**: Marker prevents hallucination (NFR-001)
- **Clarification Target**: Section requires `/clarify-constitution` to resolve

### Detection Pattern (for /clarify-constitution)
```regex
\[NEEDS CLARIFICATION(?::\s*([^\]]+))?\]
```

**Capture Groups**:
- Group 0: Full marker text
- Group 1: Optional hint text (for question context)

### Lifecycle

1. **Creation** (`/constitution` with insufficient input):
```markdown
**Language**: [NEEDS CLARIFICATION: Python version]
```

2. **Detection** (`/clarify-constitution`):
```
Detected marker in "Technology Stack > Language"
Hint: "Python version"
```

3. **Question Generation**:
```
Q: What Python version does this project use?
| Option | Description |
| Python 3.11 | Current stable, modern syntax |
| Python 3.10 | Stable, widely supported |
| Short | Specify different version (≤5 words) |
```

4. **Replacement** (after user answers "A"):
```markdown
**Language**: Python 3.11
```

5. **History** (in Clarifications section):
```markdown
### Session 2025-10-05
- Q: What Python version does this project use? → A: Python 3.11
```

## Backward Compatibility

### Existing Behavior Preserved

**Test Case 1: Comprehensive Input** (existing users)
```
User: /constitution "Detailed multi-paragraph description with all principles, tech stack, workflow, governance"

Expected: Complete constitution, zero markers (SAME AS BEFORE)
```

**Test Case 2: Repo Context Inference** (existing users)
```
Given: README.md contains "Built with Rust 1.75"
User: /constitution "Systems programming project"

Expected: Infers Rust 1.75 from README (SAME AS BEFORE)
```

**Test Case 3: Governance Dates** (existing users)
```
User: /constitution "..."

Expected: Uses today for RATIFICATION_DATE, asks if unknown (SAME AS BEFORE)
```

### New Behavior (Additive)

**Test Case 4: Minimal Input** (new feature)
```
User: /constitution "Python app"

Expected: Constitution with [NEEDS CLARIFICATION] markers (NEW)
```

**Test Case 5: Clarification Flow** (new feature)
```
User: /constitution "minimal" → /clarify-constitution

Expected: Interactive Q&A to complete constitution (NEW)
```

## Template Change Diff

### constitution.md - Step 2 Changes

```diff
  2. Collect/derive values for placeholders:
     - If user input (conversation) supplies a value, use it.
-    - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
+    - If placeholder has sufficient context from repo context (README, docs, prior versions), infer.
+    - If neither user input nor repo context provides value: Mark section with [NEEDS CLARIFICATION].
+    - Track which sections are marked incomplete (for summary in Step 8).
     - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
```

### constitution.md - Step 3 Changes

```diff
  3. Draft the updated constitution content:
-    - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
+    - Replace every placeholder with concrete text OR [NEEDS CLARIFICATION] marker.
+    - Sections marked with [NEEDS CLARIFICATION] indicate missing user input (not AI speculation).
     - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
+    - Do NOT hallucinate or guess content for marked sections (violates NFR-001).
```

### constitution.md - Step 7 Changes

```diff
  7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).
+    - If [NEEDS CLARIFICATION] markers are present:
+      * Initialize session metadata: <!-- Clarification Sessions: 0 -->
+      * Prepare suggestion for /clarify-constitution in Step 8
```

### constitution.md - Step 8 Changes

```diff
  8. Output a final summary to the user with:
     - New version and bump rationale.
+    - Count of [NEEDS CLARIFICATION] markers (if any) with affected sections listed.
     - Any files flagged for manual follow-up.
+    - Next command:
+      * /clarify-constitution (if markers present)
+      * /specify (if constitution complete)
     - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).
```

## Testing Contracts

### Regression Tests (Backward Compatibility)
```bash
# Test: Comprehensive input still works
Given: /constitution with detailed multi-paragraph input
When: Constitution generated
Then: Zero [NEEDS CLARIFICATION] markers
And: All sections complete
And: Behavior matches v1.x

# Test: Repo inference still works
Given: README.md contains "Built with TypeScript 5.0"
When: /constitution "web application"
Then: Infers TypeScript 5.0 from README
And: No marker for language/version

# Test: Date handling unchanged
Given: /constitution "new project"
When: Governance dates processed
Then: Uses today for ratification
And: Asks for amendment date if unknown
And: Behavior matches v1.x
```

### New Feature Tests
```bash
# Test: Minimal input generates markers
Given: /constitution "Python app"
When: Step 2 placeholder collection runs
Then: Insufficient data for framework, workflow, governance
When: Step 3 draft runs
Then: [NEEDS CLARIFICATION] markers inserted
When: Step 8 summary runs
Then: Reports 3+ markers, suggests /clarify-constitution

# Test: Marker placement validation
Given: Constitution draft with markers
Then: No markers in headings (### [NEEDS CLARIFICATION] ✗)
And: Markers only in content sections
And: Optional hints properly formatted

# Test: Session metadata initialization
Given: Constitution with markers
When: File written (Step 7)
Then: Contains <!-- Clarification Sessions: 0 -->
And: Ready for /clarify-constitution
```

## Migration Path

### For Existing Projects (Already Have Constitution)

**Scenario**: Project has complete constitution from v1.x

**Action**: No migration needed
- Existing constitutions don't have markers
- `/constitution` regeneration optional
- `/clarify-constitution` detects no markers → reports "Constitution complete"

### For New Projects (After This Update)

**Scenario**: User runs `/constitution` for first time

**Flow**:
1. `/constitution "minimal description"`
2. Constitution created with markers
3. User runs `/clarify-constitution`
4. Interactive Q&A completes constitution
5. `/specify` starts feature development

### For Iterative Constitution Updates

**Scenario**: User wants to amend existing complete constitution

**Flow**:
1. User manually adds `[NEEDS CLARIFICATION]` to sections needing update
2. `/clarify-constitution` detects markers
3. Asks questions about marked sections only
4. Updates constitution, increments session count

**Alternative**:
1. User directly edits constitution (no markers)
2. Manual updates preferred for minor amendments

## Success Criteria

**Functional**:
- [x] Detects insufficient user input in Step 2
- [x] Inserts `[NEEDS CLARIFICATION]` markers instead of guessing
- [x] Counts markers and reports to user in Step 8
- [x] Suggests `/clarify-constitution` when markers present
- [x] Suggests `/specify` when constitution complete
- [x] Preserves all v1.x behavior for comprehensive input

**Non-Functional**:
- [x] No hallucination (NFR-001): Markers replace guesses
- [x] Backward compatible: v1.x inputs produce same output
- [x] Clear user guidance: Reports marker count and next steps
