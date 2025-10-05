# Installation Guide

## Prerequisites

- **macOS or Linux** (Windows users: use WSL or Git Bash)
- [Claude Code CLI](https://www.anthropic.com/claude-code) - this fork supports Claude Code only
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads) (optional, can use `--no-git` flag)

> **Note**: This is a Claude Code-only, bash-only fork of spec-kit optimized for solo developers on Unix-like systems.

## Installation

### Initialize a New Project

The easiest way to get started is to initialize a new project:

```bash
uvx --from git+https://github.com/anagri/spec-kit.git speclaude init <PROJECT_NAME>
```

Or initialize in the current directory:

```bash
uvx --from git+https://github.com/anagri/spec-kit.git speclaude init .
# or use the --here flag
uvx --from git+https://github.com/anagri/spec-kit.git speclaude init --here
```

### Optional Flags

#### Skip git initialization

If you don't want git initialization:

```bash
uvx --from git+https://github.com/anagri/spec-kit.git speclaude init <project_name> --no-git
```

#### Ignore Agent Tools Check

If you prefer to get the templates without checking for Claude Code CLI:

```bash
uvx --from git+https://github.com/anagri/spec-kit.git speclaude init <project_name> --ignore-agent-tools
```

#### Force initialization in non-empty directory

```bash
uvx --from git+https://github.com/anagri/spec-kit.git speclaude init --here --force
```

## Verification

After initialization, you should see the following structure:

```
your-project/
├── .claude/
│   └── commands/          # Slash commands (/specify, /plan, /tasks, etc.)
├── .specify/
│   ├── scripts/bash/      # Automation scripts (.sh files only)
│   ├── templates/         # Template files
│   └── memory/           # Constitution and state
└── specs/                # Feature specifications go here
```

The following slash commands are now available in Claude Code:

- `/constitution` - Create/update project constitution
- `/specify` - Create feature specifications
- `/clarify` - Ask clarification questions for specs
- `/plan` - Generate implementation plans
- `/tasks` - Break down into actionable tasks
- `/analyze` - Cross-artifact consistency check
- `/implement` - Execute tasks

## Troubleshooting

### Claude Code CLI not found

Ensure Claude Code CLI is installed and in your PATH:

```bash
which claude
# Should output: /Users/<you>/.claude/local/claude (after migrate-installer)
# or: /opt/homebrew/bin/claude (before migrate-installer)
```

If not installed, follow the [Claude Code installation instructions](https://www.anthropic.com/claude-code).

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```

### Scripts not executable

If bash scripts aren't executable on Linux/macOS:

```bash
chmod +x .specify/scripts/bash/*.sh
```

### Template download fails

If template download fails, check your internet connection and GitHub access. You can also try with a GitHub token:

```bash
export GITHUB_TOKEN=your_token
uvx --from git+https://github.com/anagri/spec-kit.git speclaude init <project_name>
```

## Next Steps

- Read the [Quick Start Guide](quickstart.md) to begin using spec-kit
- Review [Local Development Guide](local-development.md) if you want to contribute to spec-kit itself
- Consult `docs/PHILOSOPHY.md` to understand the architectural philosophy of this fork
