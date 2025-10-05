# Local Development Guide

This guide shows how to iterate on the `speclaude` CLI locally without publishing a release or committing to `main` first.

> **Fork Note**: This fork is bash-only, Claude Code-only, optimized for solo developers working directly on main (no feature branch workflow).

## 1. Clone the Repository

```bash
git clone https://github.com/anagri/spec-kit.git
cd spec-kit
```

## 2. Run the CLI Directly (Fastest Feedback)

You can execute the CLI via the module entrypoint without installing anything:

```bash
# From repo root
python -m src.specify_cli --help
python -m src.specify_cli init demo-project --ignore-agent-tools
```

If you prefer invoking the script file style (uses shebang):

```bash
python src/specify_cli/__init__.py init demo-project
```

## 3. Use Editable Install (Isolated Environment)

Create an isolated environment using `uv` so dependencies resolve exactly like end users get them:

```bash
# Create & activate virtual env (uv auto-manages .venv)
uv venv
source .venv/bin/activate

# Install project in editable mode
uv pip install -e .

# Now 'speclaude' entrypoint is available
speclaude --help
```

Re-running after code edits requires no reinstall because of editable mode.

## 4. Invoke with uvx Directly From Git (Current Branch)

`uvx` can run from a local path (or a Git ref) to simulate user flows:

```bash
uvx --from . speclaude init demo-uvx --ignore-agent-tools
```

You can also point uvx at a specific branch:

```bash
# Push your working branch first
git push origin your-branch-name
uvx --from git+https://github.com/anagri/spec-kit.git@your-branch-name speclaude init demo-branch-test
```

### 4a. Absolute Path uvx (Run From Anywhere)

If you're in another directory, use an absolute path instead of `.`:

```bash
uvx --from /path/to/spec-kit speclaude --help
uvx --from /path/to/spec-kit speclaude init demo-anywhere --ignore-agent-tools
```

Set an environment variable for convenience:

```bash
export SPEC_KIT_SRC=/path/to/spec-kit
uvx --from "$SPEC_KIT_SRC" speclaude init demo-env --ignore-agent-tools
```

(Optional) Define a shell function:

```bash
speclaude-dev() { uvx --from /path/to/spec-kit speclaude "$@"; }
# Then
speclaude-dev --help
```

## 5. Testing Script Permission Logic

After running an `init`, check that shell scripts are executable on macOS/Linux:

```bash
ls -l .specify/scripts/bash/ | grep .sh
# Expect owner execute bit (e.g. -rwxr-xr-x)
```

This fork only generates `.sh` scripts (no `.ps1` PowerShell scripts).

## 6. Run Lint / Basic Checks (Add Your Own)

Currently no enforced lint config is bundled, but you can quickly sanity check importability:

```bash
python -c "import specify_cli; print('Import OK')"
```

For code formatting, use ruff or black:

```bash
ruff format src/
# or
black src/
```

## 7. Build a Wheel Locally (Optional)

Validate packaging before publishing:

```bash
uv build
ls dist/
```

Install the built artifact into a fresh throwaway environment if needed.

## 8. Using a Temporary Workspace

When testing `init --here` in a dirty directory, create a temp workspace:

```bash
mkdir /tmp/spec-test && cd /tmp/spec-test
python -m src.specify_cli init --here --ignore-agent-tools  # if repo copied here
```

Or copy only the modified CLI portion if you want a lighter sandbox.

## 9. Debug Network / TLS Skips

If you need to bypass TLS validation while experimenting:

```bash
speclaude check --skip-tls
speclaude init demo --skip-tls --ignore-agent-tools
```

(Use only for local experimentation.)

## 10. Rapid Edit Loop Summary

| Action | Command |
|--------|---------|
| Run CLI directly | `python -m src.specify_cli --help` |
| Editable install | `uv pip install -e .` then `speclaude ...` |
| Local uvx run (repo root) | `uvx --from . speclaude ...` |
| Local uvx run (abs path) | `uvx --from /path/to/spec-kit speclaude ...` |
| Git branch uvx | `uvx --from git+URL@branch speclaude ...` |
| Build wheel | `uv build` |

## 11. Cleaning Up

Remove build artifacts / virtual env quickly:

```bash
rm -rf .venv dist build *.egg-info
```

## 12. Common Issues

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError: typer` | Run `uv pip install -e .` |
| Scripts not executable (Linux/macOS) | Re-run init or `chmod +x .specify/scripts/bash/*.sh` |
| Git step skipped | You passed `--no-git` or Git not installed |
| TLS errors on corporate network | Try `--skip-tls` (not for production) |
| Claude Code CLI not found | Install from https://www.anthropic.com/claude-code |

## 13. Dogfooding: Using Spec-Kit to Develop Spec-Kit

This project uses spec-kit methodology to develop itself:

```bash
# After making changes to templates or scripts
cd spec-kit
/constitution    # Update constitution if architectural changes
/specify         # Create spec for new feature
/plan            # Generate implementation plan (reads docs/PHILOSOPHY.md)
/tasks           # Break down into tasks
/implement       # Execute implementation
```

**Important**: The `.specify/` and `.claude/` directories in this repo are INSTALLED snapshots (frozen). To change what users receive, edit SOURCE files:

- `templates/` → packaged to `.specify/templates/` in releases
- `scripts/` → packaged to `.specify/scripts/bash/` in releases
- `memory/` → packaged to `.specify/memory/` in releases
- `templates/commands/` → packaged to `.claude/commands/` in releases

See `CLAUDE.md` for detailed dogfooding guidance.

## 14. Version Management

**Every change to `src/specify_cli/__init__.py` requires**:

1. Version bump in `pyproject.toml` (line 3)
2. Entry in `CHANGELOG.md` with date and description
3. Follow semantic versioning:
   - MAJOR: Breaking changes (removed commands, changed arguments)
   - MINOR: New features (new commands, new flags)
   - PATCH: Bug fixes, docs, refactoring

**Release Process**:

1. Edit `pyproject.toml`: `version = "X.Y.Z"`
2. Edit `CHANGELOG.md`: Add entry under new `## [X.Y.Z] - YYYY-MM-DD`
3. Commit: `git add -A && git commit -m "chore: bump version to X.Y.Z"`
4. Tag: `git tag vX.Y.Z`
5. Push: `git push && git push --tags`
6. GitHub Actions creates release automatically
7. Verify templates in release logs (look for "deflated XX%" lines)

## 15. Testing Template Changes

After modifying templates in `templates/`:

```bash
# Test locally before release
uvx --from . speclaude init test-proj --ignore-agent-tools
cd test-proj

# Verify directory structure
ls -la .specify/templates/    # Should have 4 .md files
ls -la .specify/scripts/bash/ # Should have 5 .sh files
ls -la .claude/commands/      # Should have slash command files

# Test a slash command
/specify test feature

# Clean up
cd .. && rm -rf test-proj
```

## 16. Next Steps

- Update docs and run through Quick Start using your modified CLI
- Test changes with dogfooding (use spec-kit to develop spec-kit)
- Commit changes following the version discipline in constitution
- (Optional) Tag a release once changes land in `main`
