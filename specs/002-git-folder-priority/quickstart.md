# Quick Start: Monorepo Support with .specify Priority

This guide shows how to use spec-kit in monorepo environments where multiple independent projects share a single git repository.

## What Changed

**Before** (v0.x): Repository root detected by `.git` folder first
**After** (v1.x): Repository root detected by `.specify` folder first, `.git` as fallback

**Why**: Enables multiple spec-kit projects in a single git repository (monorepo workflow)

---

## Scenario 1: Multiple Projects in Single Git Repository

### Directory Structure
```
workspace/
├── .git/                       # Shared git repository
│
├── project-a/                  # Independent project A
│   ├── .specify/               # ← Project A root (detected first)
│   │   ├── templates/
│   │   ├── scripts/
│   │   └── memory/
│   │       └── constitution.md
│   ├── specs/
│   │   └── 001-feature-a/
│   └── src/
│
└── project-b/                  # Independent project B
    ├── .specify/               # ← Project B root (detected first)
    │   ├── templates/
    │   ├── scripts/
    │   └── memory/
    │       └── constitution.md
    ├── specs/
    │   └── 001-feature-b/
    └── src/
```

### Setup Instructions

**1. Initialize workspace as git repository**
```bash
cd workspace
git init
```

**2. Initialize project-a with spec-kit**
```bash
cd project-a
speclaude init .
# Creates .specify/ folder in project-a/
```

**3. Initialize project-b with spec-kit**
```bash
cd ../project-b
speclaude init .
# Creates .specify/ folder in project-b/ (independent from project-a)
```

**4. Verify independent operation**
```bash
# From project-a/
cd ../project-a/src
/specify "user authentication"
# Creates specs/001-user-authentication/ in project-a/

# From project-b/
cd ../../project-b/src
/specify "payment processing"
# Creates specs/001-payment-processing/ in project-b/
```

### How It Works

When you run a spec-kit command from `workspace/project-a/src/`:

1. **Traverse upward** from current directory (`workspace/project-a/src/`)
2. **Check `workspace/project-a/src/.specify`** → Not found
3. **Check `workspace/project-a/src/.git`** → Not found
4. **Move up** to `workspace/project-a/`
5. **Check `workspace/project-a/.specify`** → **Found!** ✓
6. **Stop immediately** - Return `workspace/project-a/` as repository root
7. **Do NOT continue** to check parent `workspace/.git`

**Result**: Each project maintains its own specs/ directory, constitution, and workflows independently.

---

## Scenario 2: Nested Submodules with Independent Specs

### Directory Structure
```
main-project/
├── .specify/                   # Main project root
├── specs/
│   └── 001-core-feature/
│
└── submodule/
    ├── .specify/               # Submodule root (independent)
    └── specs/
        └── 001-submodule-feature/
```

### Behavior

**From main-project/src/**:
```bash
/specify "core feature"
# Repository root: main-project/
# Creates: main-project/specs/001-core-feature/
```

**From main-project/submodule/src/**:
```bash
/specify "submodule feature"
# Repository root: main-project/submodule/  ← Closest .specify
# Creates: main-project/submodule/specs/001-submodule-feature/
```

**Why**: The traversal finds the **closest parent** `.specify` folder, allowing nested independent spec-kit projects.

---

## Scenario 3: Respecting Git Boundaries

### Directory Structure
```
workspace/
├── .specify/                   # ⚠ Workspace-level spec-kit (NOT used by repo/)
│
└── repo/
    ├── .git/                   # Git repository boundary
    ├── project/
    │   └── src/                # Current directory
    └── specs/
```

### Behavior

**From workspace/repo/project/src/**:
```bash
/specify "feature"
# Repository root: workspace/repo/  ← Stops at .git
# Creates: workspace/repo/specs/001-feature/
# Does NOT escape to workspace/.specify
```

**Why Git Boundary Matters**:
- Git repository is a logical project boundary
- Even if a parent directory has `.specify`, don't escape the git repo
- Prevents unintended mixing of git-tracked and parent-level spec-kit projects

**Edge Case Explained** (from spec.md line 88-89):
> When traversing upward finds `.git` folder (with no `.specify` at that level), but `.specify` exists at a higher parent directory, the system should stop at the directory containing `.git` and return that as project root. Once any project marker (`.git` or `.specify`) is found, traversal stops.

---

## Scenario 4: Traditional Single Project (Backward Compatible)

### Directory Structure
```
project/
├── .git/                       # Git root
├── .specify/                   # Spec-kit root (same level)
├── specs/
│   └── 001-feature/
└── src/
```

### Behavior

**From project/src/**:
```bash
/specify "feature"
# Repository root: project/  ← Both .specify and .git at same level
# Creates: project/specs/001-feature/
```

**Backward Compatibility**: ✓
- Both `.specify` and `.git` at the same level → returns that directory
- Priority doesn't matter when both markers are co-located
- Existing single-project repos work exactly as before

---

## Scenario 5: No-Git Repository (--no-git)

### Directory Structure
```
project/
├── .specify/                   # Spec-kit root (no .git)
├── specs/
│   └── 001-feature/
└── src/
```

### Behavior

**From project/src/**:
```bash
/specify "feature"
# Repository root: project/  ← .specify found, .git not needed
# Creates: project/specs/001-feature/
```

**Backward Compatibility**: ✓
- No `.git` folder present → `.specify` is the only marker
- Priority change doesn't affect (no `.git` to check)
- `--no-git` workflow continues to work

---

## Migration Guide

### Do I Need to Migrate?

**NO migration needed** if you have:
- ✅ Traditional single project (`.git` and `.specify` at same level)
- ✅ No-git repository (only `.specify`)
- ✅ Git-only repository (no `.specify` yet)

**Monorepo users**: Just initialize `.specify` in subdirectories as shown in Scenario 1.

### Creating a Monorepo

**Starting from scratch**:
```bash
mkdir workspace && cd workspace
git init

mkdir project-a && cd project-a
speclaude init .

cd ../
mkdir project-b && cd project-b
speclaude init .
```

**Migrating existing projects**:
```bash
# Existing git repo with project-a/ and project-b/ subdirectories
cd workspace  # (already has .git/)

cd project-a
speclaude init .  # Creates .specify/ in project-a/

cd ../project-b
speclaude init .  # Creates .specify/ in project-b/
```

---

## Troubleshooting

### Commands Create Specs in Wrong Location

**Symptom**: Running `/specify` from `project-a/` creates specs in parent directory

**Cause**: No `.specify` folder in `project-a/`, falls back to parent marker

**Solution**:
```bash
cd project-a
speclaude init .  # Ensure .specify/ exists here
/specify "feature"  # Now creates project-a/specs/001-feature/
```

---

### Want to Check Which Root is Detected

**Test repository root detection**:
```bash
# From your current directory
.specify/scripts/bash/common.sh

# Or in a script:
source .specify/scripts/bash/common.sh
get_repo_root
# Outputs: /absolute/path/to/detected/root
```

**Expected behavior**:
- ✓ Finds closest parent `.specify/` folder
- ✓ Falls back to closest parent `.git/` folder if no `.specify`
- ✓ Stops at first marker found (doesn't continue to higher parents)

---

### Multiple .specify Folders - Which One is Used?

**Rule**: Closest parent `.specify` to your current directory wins

**Example**:
```
/project/
├── .specify/                   # Outer
└── submodule/
    ├── .specify/               # Inner ← Used from submodule/src/
    └── src/
```

**From `/project/submodule/src/`**:
- Detected root: `/project/submodule/` (inner `.specify`)

**From `/project/src/`**:
- Detected root: `/project/` (outer `.specify`)

---

## Best Practices

### Monorepo Organization

1. **One .specify per independent project**
   - Each project gets its own constitution, templates, scripts
   - Projects can evolve independently

2. **Shared git repository**
   - Single `.git` at workspace root
   - All projects versioned together

3. **Independent specs directories**
   - `project-a/specs/` for project A features
   - `project-b/specs/` for project B features
   - No cross-contamination

### When to Use Monorepo

✅ **Use monorepo when**:
- Multiple related services/apps in one codebase
- Shared dependencies, coordinated releases
- Want atomic commits across projects

❌ **Don't use monorepo when**:
- Projects are completely independent
- Different teams, different workflows
- Better suited for separate repositories

### Initializing New Projects

**Template for consistent setup**:
```bash
# 1. Create project directory
mkdir -p workspace/new-project
cd workspace/new-project

# 2. Initialize spec-kit
speclaude init .

# 3. Create constitution
/constitution "Describe your project and principles..."

# 4. Start first feature
/specify "first feature description..."
```

---

## Summary

| Scenario | .specify Location | .git Location | Detected Root | Notes |
|----------|-------------------|---------------|---------------|-------|
| **Monorepo** | `project-a/.specify` | `workspace/.git` | `project-a/` | `.specify` found first ✓ |
| **Nested** | `project/.specify`<br>`project/sub/.specify` | N/A | Closest parent | Finds nearest `.specify` |
| **Git boundary** | `workspace/.specify` | `repo/.git` | `repo/` | Stops at `.git`, doesn't escape |
| **Single project** | `project/.specify` | `project/.git` | `project/` | Both at same level ✓ |
| **No-git** | `project/.specify` | None | `project/` | Works without git ✓ |

**Key Principle**: `.specify` folder is the **primary** project marker, `.git` is the **fallback** marker. The system stops at the **first marker found** during upward traversal.
