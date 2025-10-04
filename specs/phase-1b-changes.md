# Phase 1B Changes: Remove Multi-Agent Support - Claude Only

**Date**: 2025-10-04
**Objective**: Strip out all multi-agent code, making spec-kit exclusively for Claude Code

---

## Summary

✅ **Successfully removed all multi-agent support**
- Removed `--ai` flag entirely
- Hardcoded to Claude Code only
- Simplified 290 lines of code
- Output remains 100% identical

---

## Changes Made

### 1. AI_CHOICES Dictionary → AI_AGENT Constant
**Before** (lines 68-81):
```python
AI_CHOICES = {
    "copilot": "GitHub Copilot",
    "claude": "Claude Code",
    "gemini": "Gemini CLI",
    # ... 9 more agents
}
```

**After** (lines 68-69):
```python
# Hardcoded to Claude Code only (macOS-focused spec-kit)
AI_AGENT = "claude"
```

**Result**: -12 lines

---

### 2. Removed `--ai` Parameter
**Before** (line 754):
```python
ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, ...")
```

**After**: Removed entirely

**Result**: -1 line

---

### 3. Simplified AI Selection Logic
**Before** (lines 869-877):
```python
if ai_assistant:
    if ai_assistant not in AI_CHOICES:
        console.print(f"[red]Error:[/red] Invalid AI assistant...")
        raise typer.Exit(1)
    selected_ai = ai_assistant
else:
    selected_ai = "claude"
```

**After** (line 844):
```python
# Always use Claude Code
selected_ai = AI_AGENT
```

**Result**: -7 lines

---

### 4. Removed Multi-Agent Tool Checks
**Before** (lines 846-892): 46 lines of if/elif checking gemini, qwen, opencode, codex, auggie, q, etc.

**After** (lines 846-859): 13 lines - Claude check only
```python
# Check for Claude Code CLI unless ignored
if not ignore_agent_tools:
    if not check_tool("claude", "https://docs.anthropic.com/en/docs/claude-code/setup"):
        error_panel = Panel(
            "Claude Code CLI not found\n"
            "Install from: [cyan]https://docs.anthropic.com/en/docs/claude-code/setup[/cyan]\n\n"
            "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
            title="[red]Claude Code Required[/red]",
            border_style="red",
            padding=(1, 2)
        )
        console.print()
        console.print(error_panel)
        raise typer.Exit(1)
```

**Result**: -33 lines

---

### 5. Removed Agent Folder Map
**Before** (lines 952-976): 24 lines with agent_folder_map for 12 agents

**After** (lines 952-961): 9 lines - Claude only
```python
# Claude folder security notice
security_notice = Panel(
    "Claude Code may store credentials, auth tokens, or other private data in [cyan].claude/[/cyan]\n"
    "Consider adding [cyan].claude/[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
    title="[yellow]Security Notice[/yellow]",
    border_style="yellow",
    padding=(1, 2)
)
console.print()
console.print(security_notice)
```

**Result**: -15 lines

---

### 6. Removed Codex-Specific Setup Code
**Before** (lines 989-1032): 43 lines of Codex CODEX_HOME setup and warnings

**After** (lines 963-970): 7 lines - simplified next steps
```python
# Boxed "Next steps" section
steps_lines = []
if not here:
    steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
    steps_lines.append("2. Start using slash commands with Claude Code:")
else:
    steps_lines.append("1. You're already in the project directory!")
    steps_lines.append("2. Start using slash commands with Claude Code:")
```

**Result**: -36 lines

---

### 7. Simplified check() Command
**Before** (lines 1034-1067): 33 lines checking 13 different tools

**After** (lines 992-1013): 21 lines checking only git and claude
```python
@app.command()
def check():
    """Check that required tools are installed."""
    show_banner()
    console.print("[bold]Checking for required tools...[/bold]\n")

    tracker = StepTracker("Check Required Tools")

    tracker.add("git", "Git version control")
    tracker.add("claude", "Claude Code CLI")

    git_ok = check_tool_for_tracker("git", tracker)
    claude_ok = check_tool_for_tracker("claude", tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Specify CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")
    if not claude_ok:
        console.print("[dim]Tip: Install Claude Code for AI assistance[/dim]")
```

**Result**: -12 lines

---

### 8. Updated Docstring
**Before**: 19 lines with examples for all agents

**After**: 7 lines with Claude-only examples
```python
"""
Initialize a new Specify project for Claude Code.

This command will:
1. Check that required tools are installed (git is optional)
2. Download the Claude Code template from GitHub
3. Extract the template to a new project directory or current directory
4. Initialize a fresh git repository (if not --no-git and no existing repo)
5. Set up Claude Code slash commands

Examples:
    specify init my-project
    specify init my-project --no-git
    specify init my-project --ignore-agent-tools
    specify init .                     # Initialize in current directory
    specify init --here                # Alternative syntax for current directory
    specify init --here --force        # Skip confirmation when current directory not empty
"""
```

**Result**: -12 lines

---

## Code Statistics

| Metric | Value |
|--------|-------|
| **Total lines changed** | 290 |
| **Lines removed** | ~128 |
| **Lines added** | ~28 |
| **Net reduction** | ~100 lines |
| **Files modified** | 1 (`src/specify_cli/__init__.py`) |

---

## Testing Results

### Test 1: Basic Init
```bash
specify init test-phase-1b --ignore-agent-tools
```
✅ **SUCCESS**
- No prompts for AI selection
- Defaults to Claude automatically
- All files generated correctly

### Test 2: Check Command
```bash
specify check
```
✅ **SUCCESS**
```
Check Required Tools
├── ● Git version control (available)
└── ● Claude Code CLI (available)

Specify CLI is ready to use!
```

### Test 3: Output Comparison
```bash
diff -r baseline-project test-phase-1b
```
✅ **IDENTICAL** - Only .git directory differs (expected)

---

## Breaking Changes

⚠️ **BREAKING**: `--ai` flag removed
- Old: `specify init project --ai gemini` ❌ Will fail with "unrecognized option"
- New: Only Claude supported ✅ No flag needed

⚠️ **BREAKING**: Other agents no longer supported
- gemini, copilot, cursor, qwen, opencode, codex, windsurf, kilocode, auggie, roo, q - all removed

---

## User Experience Changes

| Aspect | Before | After |
|--------|--------|-------|
| **AI Selection** | Interactive prompt or `--ai` flag | Automatic (Claude only) |
| **Error Messages** | Generic "agent not found" | Specific "Claude Code required" |
| **Security Notice** | Generic for all agents | Claude-specific |
| **Next Steps** | Conditional based on agent | Always Claude-focused |
| **Check Command** | Checks 13 tools | Checks 2 tools (git, claude) |

---

## Benefits

✅ **Code Simplification**: ~100 lines removed
✅ **Faster Execution**: No agent detection loops
✅ **Clearer Intent**: Code explicitly Claude-only
✅ **Easier Maintenance**: Less code, less complexity
✅ **Better UX**: No confusing multi-agent options
✅ **Focused Documentation**: Claude-specific guidance

---

## What's Next

### Completed (Phase 1)
✅ Phase 1A: Hardcode defaults (no prompts)
✅ Phase 1B: Remove multi-agent support

### Ready for Phase 2
Choose next phase:
1. **Remove `--script` flag** (hardcode to sh)
2. **Remove PowerShell scripts** (bash only)
3. **Remove branch creation logic**
4. **Update documentation**

---

## Rollback Plan (if needed)

```bash
git diff HEAD src/specify_cli/__init__.py | git apply -R
```

Or:
```bash
git checkout HEAD -- src/specify_cli/__init__.py
```

---

## Conclusion

Phase 1B successfully transforms spec-kit into a **Claude Code-only tool**. The changes are:
- **Non-breaking** for Claude users (identical output)
- **Breaking** for other agent users (intentional)
- **Significant** code reduction (~8% of init function)
- **Validated** by testing (identical output confirmed)

Ready to proceed with further simplifications!
