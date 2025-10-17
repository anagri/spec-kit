# Bash Script Automation Ecosystem

**Purpose**: Details the bash script layer handling filesystem state and JSON communication
**Target Audience**: Developers understanding state management patterns
**Related Files**:

- [Architecture](03-architecture.md) - Layer 3 state automation
- [Commands: Core](04-commands-core.md) - How commands invoke scripts
- [Constitution](08-constitution.md) - Solo workflow principle
  **Keywords**: bash scripts, JSON contracts, monorepo support, solo workflow, state isolation

---

## Overview

The bash script layer handles **stateful filesystem operations** while maintaining **stateless communication** with Claude through JSON contracts. This separation ensures clean boundaries between AI-driven content generation and platform-specific state mutations.

---

## 1. Design Philosophy

### 1.1 State Isolation Model

```
┌─────────────────────────────────┐
│  Claude (Pure Transformations)  │
│  - Reads JSON                   │
│  - Generates content            │
│  - Writes artifacts             │
└────────────┬────────────────────┘
             │
             ▼ JSON (read-only view of state)
┌─────────────────────────────────┐
│  Bash Scripts (State Mutation)  │
│  - mkdir, cp, find              │
│  - Git operations (optional)    │
│  - Outputs JSON to stdout       │
└─────────────────────────────────┘
```

**Why This Separation?**

- **No race conditions**: Claude never executes filesystem operations directly
- **No permission errors**: Scripts handle platform-specific operations
- **Testability**: Scripts can be tested independently with JSON output validation
- **Portability**: Platform-specific logic isolated in bash layer

### 1.2 Communication Contract

**Bash → Claude**: JSON on stdout, errors on stderr

```bash
# Success case
{"FEATURE_ID":"003-user-auth","SPEC_FILE":"/path/to/specs/003-user-auth/spec.md"}

# Error case (stderr)
Error: specs/ directory not found
```

**Claude → Bash**: Command-line arguments

```bash
bash create-new-feature.sh --json "Add user authentication"
```

---

## 2. Common Utilities (`common.sh` - 115 lines)

### 2.1 Repository Root Detection

**Critical Feature**: `.specify` priority over `.git` for monorepo support

```bash
get_repo_root() {
    local dir="$(pwd)"
    while [ "$dir" != "/" ]; do
        # FIRST: Check for .specify (Priority 1)
        if [ -d "$dir/.specify" ]; then
            echo "$dir"
            return 0
        fi
        # SECOND: Check for .git (Priority 2)
        if [ -d "$dir/.git" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    # Final fallback to script location
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    (cd "$script_dir/../../.." && pwd)
}
```

**Monorepo Example**:

```
my-monorepo/                    # Root git repository
├── .git/
├── project-a/
│   ├── .specify/              # get_repo_root() returns /path/to/my-monorepo/project-a
│   └── specs/
└── project-b/
    ├── .specify/              # get_repo_root() returns /path/to/my-monorepo/project-b
    └── specs/
```

**Why**: Enables multiple independent spec-kit projects in a single git repository without interference. Each project can have its own feature numbering, agent context, and specification lifecycle.

### 2.2 Current Feature Detection

**No Git Branch Dependency**:

```bash
get_current_feature() {
    # First check SPECIFY_FEATURE environment variable
    if [[ -n "${SPECIFY_FEATURE:-}" ]]; then
        echo "$SPECIFY_FEATURE"
        return
    fi

    # Fallback: Find latest feature directory in specs/
    local specs_dir="$repo_root/specs"
    local latest_feature=""
    local highest=0

    for dir in "$specs_dir"/*; do
        if [[ -d "$dir" && "$dirname" =~ ^([0-9]{3})- ]]; then
            local number=${BASH_REMATCH[1]}
            number=$((10#$number))
            if [[ "$number" -gt "$highest" ]]; then
                highest=$number
                latest_feature=$dirname
            fi
        fi
    done

    echo "$latest_feature"
}
```

**Two-Tier Fallback**:

1. Check `SPECIFY_FEATURE` env var (explicit context)
2. Scan `specs/` for highest-numbered directory (implicit context)

**Why**: Supports solo dev workflow without requiring git branches or manual branch naming. Developers can work on features without additional ceremony.

### 2.3 Feature Path Resolution

```bash
get_feature_paths() {
    local repo_root=$(get_repo_root)
    local current_feature=$(get_current_feature)
    local feature_dir=$(get_feature_dir "$repo_root" "$current_feature")

    cat <<EOF
REPO_ROOT='$repo_root'
CURRENT_FEATURE='$current_feature'
HAS_GIT='$has_git_repo'
FEATURE_DIR='$feature_dir'
FEATURE_SPEC='$feature_dir/spec.md'
IMPL_PLAN='$feature_dir/plan.md'
TASKS='$feature_dir/tasks.md'
RESEARCH='$feature_dir/research.md'
DATA_MODEL='$feature_dir/data-model.md'
QUICKSTART='$feature_dir/quickstart.md'
CONTRACTS_DIR='$feature_dir/contracts'
EOF
}
```

**Single Source of Truth**: All scripts use this function for consistent path resolution. Changes to directory structure require updates in only one location.

---

## 3. Feature Creation (`create-new-feature.sh` - 100 lines)

### 3.1 Sequential Feature Numbering

```bash
HIGHEST=0
if [ -d "$SPECS_DIR" ]; then
    for dir in "$SPECS_DIR"/*; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
        number=$((10#$number))  # Force base-10 interpretation (handles leading zeros)
        if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
    done
fi

NEXT=$((HIGHEST + 1))
FEATURE_NUM=$(printf "%03d" "$NEXT")  # Format as 001, 002, 003...
```

**Why `10#$number`?**

Prevents bash from interpreting "008" as octal (which would fail). The `10#` prefix forces base-10 interpretation.

### 3.2 Feature ID Slugification

```bash
FEATURE_ID=$(echo "$FEATURE_DESCRIPTION" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9]/-/g' \
    | sed 's/-\+/-/g' \
    | sed 's/^-//' \
    | sed 's/-$//')

# Limit to first 3 words
WORDS=$(echo "$FEATURE_ID" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//')
FEATURE_ID="${FEATURE_NUM}-${WORDS}"
```

**Examples**:

- "Real-time chat system with message history" → `003-real-time-chat`
- "User authentication via OAuth2" → `004-user-authentication-via`
- "Add support for file uploads" → `005-add-support-for`

**Why 3 words?**

Balances readability with filesystem path length constraints. Three words provide sufficient context without creating unwieldy directory names.

### 3.3 No Branch Creation (Solo Dev Workflow)

```bash
# Feature directory (no branch creation - solo dev workflow)
FEATURE_DIR="$SPECS_DIR/$FEATURE_ID"
mkdir -p "$FEATURE_DIR"

# REMOVED from upstream:
# git checkout -b "$BRANCH_NAME"  # ← Line 74 in github/spec-kit
```

**Why Removed**:

Solo developers work directly on `main`. Creating branches adds ceremony without benefit. If branches are needed, users create them manually. This aligns with the constitution's solo developer workflow principle.

### 3.4 JSON Output Contract

```bash
if $JSON_MODE; then
    printf '{"FEATURE_ID":"%s","SPEC_FILE":"%s","FEATURE_NUM":"%s"}\n' \
        "$FEATURE_ID" "$SPEC_FILE" "$FEATURE_NUM"
else
    echo "FEATURE_ID: $FEATURE_ID"
    echo "SPEC_FILE: $SPEC_FILE"
    echo "FEATURE_NUM: $FEATURE_NUM"
fi
```

**Why JSON?**

- **Parseable**: Claude can reliably extract values with `json.loads()`
- **Structured**: Multiple values in single output
- **Error isolation**: Errors go to stderr, success data to stdout
- **Future-proof**: Additional fields can be added without breaking parsers

---

## 4. Agent Context Updates (`update-agent-context.sh` - 623 lines)

### 4.1 Purpose

Maintains `.claude/CLAUDE.md` with project-specific context by parsing `plan.md` for technology stack and updating specific sections while preserving manual additions.

### 4.2 Incremental Update Strategy

```bash
# Preserve manual additions between markers
<!-- BEGIN MANUAL TECH STACK -->
Language: Python 3.11
Framework: FastAPI
<!-- END MANUAL TECH STACK -->

<!-- BEGIN MANUAL ADDITIONS -->
# User can add custom sections here
# These won't be overwritten by update-agent-context.sh
<!-- END MANUAL ADDITIONS -->
```

**Update Process**:

1. Parse `plan.md` for: Language, Framework, Database, Architecture
2. Load existing `CLAUDE.md`
3. Update only sections between auto-generation markers
4. Preserve content between `BEGIN MANUAL` and `END MANUAL` markers
5. Write back to `CLAUDE.md`

**Why Incremental?**

- **O(1) operation**: Only updates changed sections
- **Preserves manual edits**: User customizations survive automatic updates
- **Token efficiency**: Keeps `CLAUDE.md` under 150 lines
- **Safe automation**: No risk of overwriting human-authored content

### 4.3 Technology Stack Extraction

```bash
# Parse plan.md for tech stack
LANGUAGE=$(grep "^\*\*Language/Version\*\*:" plan.md | sed 's/.*: //' | sed 's/ or.*//')
FRAMEWORK=$(grep "^\*\*Primary Dependencies\*\*:" plan.md | sed 's/.*: //' | cut -d',' -f1)
DATABASE=$(grep "^\*\*Storage\*\*:" plan.md | sed 's/.*: //')
```

**Effect**: `CLAUDE.md` automatically stays current with technical decisions from planning phase. Claude has accurate project context without manual intervention.

---

## 5. Prerequisites Checking (`check-prerequisites.sh` - 165 lines)

### 5.1 Multi-Mode Operation

```bash
# Flags
--json              # Output JSON format
--require-tasks     # ERROR if tasks.md missing
--include-tasks     # Include tasks content in output
--paths-only        # Minimal output (FEATURE_DIR, FEATURE_SPEC only)
```

**Why Multiple Modes?**

Different commands have different requirements:

- `/spec` needs only feature directory
- `/implement` requires tasks.md
- `/research` benefits from knowing all available docs

### 5.2 Available Docs Enumeration

```bash
AVAILABLE_DOCS='["spec.md"'
[ -f "$FEATURE_DIR/plan.md" ] && AVAILABLE_DOCS="$AVAILABLE_DOCS,\"plan.md\""
[ -f "$FEATURE_DIR/tasks.md" ] && AVAILABLE_DOCS="$AVAILABLE_DOCS,\"tasks.md\""
[ -f "$FEATURE_DIR/research.md" ] && AVAILABLE_DOCS="$AVAILABLE_DOCS,\"research.md\""
[ -f "$FEATURE_DIR/data-model.md" ] && AVAILABLE_DOCS="$AVAILABLE_DOCS,\"data-model.md\""
[ -d "$FEATURE_DIR/contracts" ] && AVAILABLE_DOCS="$AVAILABLE_DOCS,\"contracts/\""
AVAILABLE_DOCS="$AVAILABLE_DOCS]"
```

**Why Enumerate?**

Commands like `/tasks` and `/implement` need to know which design documents exist to tailor their behavior. For example:

- If `data-model.md` exists: Include database schema context
- If `contracts/` exists: Reference API contracts in implementation
- If `research.md` exists: Consider alternative approaches

### 5.3 JSON Output Structure

```json
{
  "FEATURE_DIR": "/path/to/specs/003-feature",
  "AVAILABLE_DOCS": ["spec.md", "plan.md", "data-model.md", "contracts/"],
  "REPO_ROOT": "/path/to/repo",
  "HAS_GIT": "true"
}
```

**Complete Example**:

```bash
$ bash check-prerequisites.sh --json --include-tasks

{
  "FEATURE_DIR": "/Users/dev/myproject/specs/003-user-auth",
  "AVAILABLE_DOCS": ["spec.md", "plan.md", "tasks.md"],
  "REPO_ROOT": "/Users/dev/myproject",
  "HAS_GIT": "true",
  "CURRENT_FEATURE": "003-user-auth",
  "TASKS_CONTENT": "### Core Implementation\n- [ ] Create User model..."
}
```

---

## 6. Script Architecture Patterns

### 6.1 Error Handling

```bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Explicit error messages to stderr
if [ ! -d "$SPECS_DIR" ]; then
    echo "Error: specs/ directory not found at $SPECS_DIR" >&2
    exit 1
fi
```

### 6.2 JSON vs Human Output

```bash
if $JSON_MODE; then
    printf '{"status":"success","data":%s}\n' "$JSON_DATA"
else
    echo "Feature created successfully!"
    echo "Location: $FEATURE_DIR"
fi
```

**Why Both?**

- JSON mode: Claude-to-script communication
- Human mode: Direct CLI usage during development

### 6.3 Environment Variable Expansion

```bash
# Support both explicit env var and command invocation
REPO_ROOT="${SPECIFY_REPO_ROOT:-$(get_repo_root)}"
FEATURE="${SPECIFY_FEATURE:-$(get_current_feature)}"
```

**Why**: Enables testing with synthetic environments and explicit context overrides.

---

## Cross-References

**Layer Relationships**:

- Scripts invoked by: [Commands: Core](04-commands-core.md) (Layer 2)
- Scripts manage state for: [Templates](06-templates.md) (Layer 2)
- Scripts implement: [Constitution](08-constitution.md) solo workflow

**Data Flow**:

- Input: Feature descriptions, command flags
- Processing: Filesystem operations, git queries
- Output: JSON with paths, state, enumerated documents

**Integration Points**:

- `/spec` command → `create-new-feature.sh` → JSON → template expansion
- `/implement` command → `check-prerequisites.sh --require-tasks` → validation
- All commands → `common.sh` functions → consistent path resolution

**Navigation**: [← Templates](06-templates.md) | [Constitution →](08-constitution.md)

---

## Keywords

bash automation, state management, JSON contracts, filesystem operations, monorepo support, feature numbering, path resolution, solo developer workflow, branch-free development, incremental updates, agent context maintenance, prerequisite validation, script composition, error handling patterns, environment variables, portable paths, CLAUDE.md automation, technology stack extraction, available document enumeration
