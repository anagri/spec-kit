# Research: Prioritize .specify Folder for Repository Root Detection

**Feature**: 002-git-folder-priority | **Date**: 2025-10-06

## Internal Documentation Consulted

### docs/PHILOSOPHY.md
- **Layer 3 (Scripts)**: Bash scripts handle state automation and file system boundaries
- **Boundary Detection**: Scripts use `.git` OR `.specify` markers to find repository root
- **Solo Dev Optimization**: No git branch coupling in repository root logic
- **State Automation Pattern**: Scripts communicate via JSON, maintain idempotent behavior
- **Extension Pattern**: Modify existing functions rather than add new ones (KISS principle)

### docs/quickstart.md
- **Monorepo Scenario** (line 212-218): Shows multiple projects in single git repository
- **CLI Tool Pattern** (line 177-201): CLI projects use template-contracts.md not data-model.md
- **Constitutional Requirement** (line 209): Must consult docs/ folder during research phase

### CLAUDE.md
- **Bash Script Ecosystem** (line 37-55): Overview of all scripts and their responsibilities
- **Common.sh Functions** (line 4-13): `get_repo_root()` is central to all scripts
- **Create-new-feature.sh** (line 21-32): `find_repo_root()` used for marker detection
- **Script Conventions**: `set -e` for fail-fast, `--json` for tool integration
- **Dogfooding Rules** (line 245-265): SOURCE scripts in `scripts/bash/` packaged to `.specify/scripts/bash/`

### Existing specs/001-when-the-user
- **Research Pattern**: Consult internal docs first, document decisions, reference alternatives
- **Contract-First Design**: Define function contracts before implementation
- **TDD Workflow**: Contract tests must fail before implementation

## Research Findings

### 1. Repository Root Detection Strategy

**Decision**: Invert priority in existing traversal functions

**Rationale**:
- Two functions handle repo root detection:
  - `get_repo_root()` in common.sh (lines 5-13) - used by all scripts
  - `find_repo_root()` in create-new-feature.sh (lines 22-32) - local to that script
- Current logic: Check git first, then fall back
- Required logic: Check `.specify` first, then `.git`, then fall back
- Both functions traverse upward until marker found
- Modification maintains backward compatibility

**Implementation Approach**:
```bash
# Current: common.sh get_repo_root()
if git rev-parse --show-toplevel >/dev/null 2>&1; then
    git rev-parse --show-toplevel
else
    # Fall back to script location
fi

# New: Priority traversal
1. Start from current directory
2. Check for .specify at this level → if found, return and STOP
3. Check for .git at this level → if found, return and STOP
4. Move to parent directory, repeat
5. If reach filesystem root: Fall back to script location
```

**Alternatives Considered**:
- **Double-pass traversal**: Search all `.specify` upward, then all `.git` upward
  - Rejected: Performance penalty (2x traversal), violates edge case requirement
  - Edge case (spec line 88-89): Must stop at first marker found to respect git boundaries
- **New dedicated function**: Create `get_monorepo_root()` alongside `get_repo_root()`
  - Rejected: Duplicates traversal logic, requires calling code changes, harder to maintain
- **Environment variable override**: `SPECIFY_PRIORITY=.specify` to control behavior
  - Rejected: Implicit behavior, configuration complexity, error-prone

**Internal Docs Consulted**: CLAUDE.md lines 4-13, 21-32, docs/PHILOSOPHY.md Layer 3

### 2. Project Type Determination

**Decision**: CLI/Template/Generator tool (Option 4) → use template-contracts.md

**Rationale**:
- Feature modifies bash scripts (Layer 3), not data models
- Bash functions are interfaces/contracts, not database entities
- Follows pattern from docs/quickstart.md line 192 (CLI tool example)
- Plan-template.md line 181 specifies template-contracts.md for CLI/template features

**Contract Structure**:
```markdown
## Contract: function_name()
**Location**: file path
**Purpose**: brief description
**Input**: parameters
**Output**: stdout/stderr
**Exit Code**: success/failure codes
**Behavior**: numbered steps
```

**Alternatives Considered**:
- **data-model.md**: Rejected - no database entities or state models
- **API contracts**: Rejected - bash functions, not HTTP endpoints
- **Inline documentation**: Rejected - need separate testable contracts

**Internal Docs Consulted**: docs/quickstart.md line 192, plan-template.md line 181

### 3. Git Boundary Edge Case Handling

**Decision**: Stop at first marker found (either `.specify` or `.git`)

**Rationale** (from spec line 88-89):
- When traversing upward, once any marker is found, return that directory immediately
- Do NOT continue searching parent directories for a different marker type
- Prevents escaping git repository boundaries
- Example scenario:
  ```
  /workspace/.specify         ← Higher parent
  /workspace/repo/.git        ← Git root (STOP HERE)
  /workspace/repo/project/    ← Current directory
  ```
  - From `project/`: Find `.git` first (at repo/), return `repo/`, STOP
  - Do NOT continue to find `.specify` at `workspace/`

**Implementation Logic**:
```bash
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        # Priority check at EACH level before moving up
        if [ -d "$dir/.specify" ]; then
            echo "$dir"
            return 0  # STOP HERE
        fi
        if [ -d "$dir/.git" ]; then
            echo "$dir"
            return 0  # STOP HERE
        fi
        dir="$(dirname "$dir")"  # Move up only if neither found
    done
    return 1
}
```

**Alternatives Considered**:
- **Continue search after `.git`**: Rejected - violates git boundary requirement
- **Prefer parent `.specify` over child `.git`**: Rejected - breaks isolation, unexpected behavior
- **Configurable boundary**: Rejected - adds complexity, unclear benefit

**Internal Docs Consulted**: specs/002-git-folder-priority/spec.md lines 88-89

### 4. Backward Compatibility Preservation

**Decision**: Maintain all existing behaviors for current use cases

**Rationale**:
- **Single-project repos** (`.git` and `.specify` at same level): No behavior change
- **No-git repos** (`--no-git` init, only `.specify`): Priority change doesn't affect (no `.git` exists)
- **Git-only repos** (no `.specify`): Falls back to `.git` as before
- **Performance**: Single upward traversal, no additional overhead

**Test Coverage** (from spec acceptance scenarios):
1. Monorepo: `.specify` in subdirectories → finds closest `.specify` ✓
2. Single-project: Same level markers → finds root (priority doesn't matter) ✓
3. No-git: Only `.specify` → finds `.specify` ✓
4. Nested `.specify`: Multiple levels → finds closest parent ✓
5. Git boundary: `.git` found first → stops, respects boundary ✓

**Alternatives Considered**:
- **Version flag**: `--v2-priority` for new behavior - Rejected: fragmentation, migration burden
- **Migration script**: Automatic conversion - Rejected: unnecessary, no breaking changes
- **Deprecation period**: Warn before switching - Rejected: no user-facing changes

**Internal Docs Consulted**: specs/002-git-folder-priority/spec.md lines 53-89

### 5. Function Modification Scope

**Decision**: Modify 2 functions in 2 files only

**Rationale**:
- **common.sh**: `get_repo_root()` used by:
  - `get_current_feature()` (line 24)
  - `get_feature_paths()` (line 75)
  - Sourced by: check-prerequisites.sh, setup-plan.sh, update-agent-context.sh
- **create-new-feature.sh**: `find_repo_root()` used locally (line 43)
- Both functions implement same priority logic independently
- No other functions require changes (inheritance via common.sh)

**Impact Analysis**:
- ✅ check-prerequisites.sh: Inherits change via `get_repo_root()` → supports monorepo
- ✅ setup-plan.sh: Inherits change via `get_repo_root()` → supports monorepo
- ✅ update-agent-context.sh: Inherits change via `get_repo_root()` → supports monorepo
- ✅ create-new-feature.sh: Direct modification of `find_repo_root()` → supports monorepo
- ✅ All scripts gain monorepo support automatically

**Alternatives Considered**:
- **Centralize in common.sh only**: Rejected - create-new-feature.sh has independent implementation by design
- **Modify all 5 scripts**: Rejected - only 2 contain traversal logic, others inherit
- **New shared library**: Rejected - over-engineering for 2 function changes

**Internal Docs Consulted**: CLAUDE.md lines 37-55, grep analysis of function usage

### 6. Testing Strategy

**Decision**: Contract tests for functions, integration tests for scenarios

**Rationale**:
- **Contract Tests** (Phase 3.1 in tasks):
  - `test_get_repo_root.sh`: Validates common.sh function behavior
  - `test_find_repo_root.sh`: Validates create-new-feature.sh function behavior
  - Must be written and must fail before implementation (TDD gate)
- **Integration Tests** (Phase 3.3 in tasks):
  - 5 acceptance scenarios from spec
  - 4 edge cases from spec
  - End-to-end workflow validation

**Test Pattern** (from specs/001 contract tests):
```bash
#!/usr/bin/env bash
set -euo pipefail

# Test Setup
TEST_NAME="test_get_repo_root"
FAILURES=0

# Test Case
test_specify_priority() {
    local test_dir=$(mktemp -d)
    mkdir -p "$test_dir/project/.specify"
    mkdir -p "$test_dir/.git"

    cd "$test_dir/project"
    result=$(get_repo_root)

    if [[ "$result" == "$test_dir/project" ]]; then
        pass "Finds .specify before .git in parent"
    else
        fail "Should prioritize .specify over parent .git"
    fi

    rm -rf "$test_dir"
}

# Run tests
test_specify_priority
[[ $FAILURES -eq 0 ]] && exit 0 || exit 1
```

**Alternatives Considered**:
- **Unit tests only**: Rejected - need end-to-end scenario validation
- **Manual testing**: Rejected - not repeatable, no regression detection
- **Python/bats framework**: Rejected - adds dependencies, bash scripts suffice

**Internal Docs Consulted**: specs/001-when-the-user/tasks.md lines 42-75 (contract test pattern)

## Summary

**All Technical Context items resolved**: ✓

**Key Decisions**:
1. **Invert priority** in existing `get_repo_root()` and `find_repo_root()` functions
2. **Use template-contracts.md** (not data-model.md) for bash function contracts
3. **Stop at first marker found** to respect git boundaries (edge case requirement)
4. **Maintain backward compatibility** for all existing use cases
5. **Modify 2 functions in 2 files** only (common.sh and create-new-feature.sh)
6. **TDD approach** with contract tests before implementation

**Internal Docs Referenced**:
- docs/PHILOSOPHY.md: Layer 3 script patterns, state automation via bash
- docs/quickstart.md: Monorepo scenario example, CLI tool pattern
- CLAUDE.md: Bash script ecosystem, function responsibilities
- specs/001-when-the-user/: Contract test pattern, research structure
- specs/002-git-folder-priority/spec.md: Edge cases, acceptance scenarios

**No external research needed** - all patterns and decisions derived from existing codebase architecture, constitutional principles, and specification requirements.
