# Existing Bug: Path Doubling in Release Artifacts

**Status**: Known issue in upstream (v0.0.56) - Fixed by our preprocessing simplification
**Severity**: Low (LLMs auto-correct `.specify.specify/` as typo)
**Date Documented**: 2025-10-07

## Summary

Release artifacts from v0.0.56 onwards contain doubled paths like `.specify.specify/memory/` instead of `.specify/memory/`. This bug was introduced when source templates were updated to use `.specify/` paths without updating the release workflow's `rewrite_paths()` function.

## Root Cause Analysis

### Timeline of Events

1. **Before commit `2f043ef`** (working correctly):
   - Templates had relative paths: `/memory/`, `/scripts/`, `/templates/`
   - Release workflow's `rewrite_paths()` converted these to `.specify/memory/`, etc.
   - Result: Correct paths in release artifacts ✅

2. **At commit `2f043ef`** (Sep 18, 2025 - bug introduced):
   ```
   commit 2f043ef6826c2ca78c45d2af5b6e1b58c1b6ec21
   Author: Den Delimarsky 🌺 <53200638+localden@users.noreply.github.com>
   Date:   Thu Sep 18 22:13:38 2025 -0700

   Update constitution command
   ```
   - Templates updated to have `.specify/memory/` paths **in source**
   - Release workflow **NOT updated** - still applies `s@(/?)memory/@.specify/memory/@g`
   - **BUG**: `.specify/memory/` → `.specify.specify/memory/` ❌

3. **At tag `v0.0.56`** (Oct 2025):
   - Released with the bug
   - All command files have doubled paths in release artifacts ❌

4. **At commit `e350c27`** (Oct 4, 2025 - our fork refactor):
   ```
   commit e350c2758507e313ece47bb1ff0c3ae0046804a4
   Author: anagri <127566+anagri@users.noreply.github.com>
   Date:   Sat Oct 4 21:10:02 2025 +0530

   Refactor: Remove orphaned PowerShell scripts and simplify build scripts for Claude Code only
   ```
   - Simplified to Claude Code + bash only
   - Still kept `rewrite_paths()` and `generate_commands()` - bug persists ❌

### The Problematic `rewrite_paths()` Function

Located in `.github/workflows/scripts/create-release-packages.sh` (pre-simplification):

```bash
rewrite_paths() {
  sed -E \
    -e 's@(/?)memory/@.specify/memory/@g' \
    -e 's@(/?)scripts/@.specify/scripts/@g' \
    -e 's@(/?)templates/@.specify/templates/@g'
}
```

**Problem**: This replaces **any** occurrence of `memory/@`, `scripts/@`, `templates/@` with `.specify/` prefix, including patterns that already start with `.specify/`.

### Evidence from Git History

```bash
# v0.0.56 templates (before bug):
$ git show v0.0.56:templates/commands/constitution.md | grep memory/
You are updating the project constitution at `/memory/constitution.md`.
1. Load the existing constitution template at `/memory/constitution.md`.
7. Write the completed constitution back to `/memory/constitution.md` (overwrite).

# After commit 2f043ef (bug introduced):
$ git show 2f043ef:templates/commands/constitution.md | grep memory/
You are updating the project constitution at `.specify/memory/constitution.md`.
1. Load the existing constitution template at `.specify/memory/constitution.md`.
7. Write the constitution back to `.specify/memory/constitution.md` (overwrite).

# Current HEAD (still has .specify/ in source):
$ git show HEAD:templates/commands/constitution.md | grep "Constitution created at"
     Constitution created at .specify/memory/constitution.md
```

### Impact Assessment

**Affected Files**:
- `templates/commands/constitution.md` (lines referencing `.specify/memory/`)
- `templates/commands/clarify-constitution.md` (lines referencing `.specify/memory/`)
- All other command files with path references (minimal impact)

**Why Low Severity**:
1. LLMs interpret `.specify.specify/` as a typo and auto-correct to `.specify/`
2. Only affects example output text in command files (not functional paths)
3. Actual script execution uses correct paths from bash scripts

**Release Artifacts Affected**:
- v0.0.56 onwards (including v0.0.61 used in our testing)

## Our Fix

Our preprocessing simplification (spec 003-local-to-cmdline) **fixes this issue** by:

1. **Reverting to relative paths in source** (Git history shows this was original design):
   ```bash
   git show v0.0.56:templates/commands/constitution.md | grep "/memory/"
   # Shows: `/memory/constitution.md` (correct)
   ```

2. **Pre-processing templates once**:
   - Script: `.github/workflows/scripts/preprocess-templates-claude-bash.sh`
   - Applies transformations: `/memory/` → `.specify/memory/`
   - Uses backtick-bounded matching to avoid double-processing
   - Includes deduplication: `s@`.specify.specify/@`.specify/@g`

3. **Simplified release workflow**:
   - Removed runtime `rewrite_paths()` function
   - Just copies pre-processed templates as-is
   - No runtime transformations = no path doubling

### Verification

```bash
# Test comparison (after our fix):
$ diff /tmp/test-final/test-release/.claude/commands/constitution.md \
       /tmp/test-final/test-local/.claude/commands/constitution.md
79c79
<      Constitution created at .specify.specify/memory/constitution.md
---
>      Constitution created at .specify/memory/constitution.md
```

**Before our fix**: Release has `.specify.specify/` (doubled)
**After our fix**: Local has `.specify/` (correct)

## Resolution Strategy

**Decision**: Do NOT backport fix to upstream releases

**Rationale**:
1. Low impact - LLMs handle it gracefully
2. Our fork fixes it going forward
3. Upstream `github/spec-kit` would need similar refactor
4. Not worth the coordination effort for cosmetic issue

**Going Forward**:
- Our preprocessing simplification resolves the issue
- Future releases will have correct `.specify/` paths
- No action needed from users (LLMs auto-correct)

## References

- **Introduced**: Commit `2f043ef` (Sep 18, 2025)
- **First Affected Release**: v0.0.56
- **Fixed By**: Our preprocessing simplification (spec 003-local-to-cmdline)
- **Related Files**:
  - `.github/workflows/scripts/create-release-packages.sh`
  - `.github/workflows/scripts/preprocess-templates-claude-bash.sh`
  - `templates/commands/*.md` (all command files)
