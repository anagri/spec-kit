# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About This Documentation Repository

This folder contains scraped Claude Code documentation from docs.claude.com. The documentation covers Claude Code CLI usage, configuration, features, and integrations.

**When working with Claude Code topics, refer to relevant files below for complete context.**

## Documentation File Index

Each file entry contains:
1. **Overview** - Human-readable description of what the file covers
2. **Details** - Comprehensive technical summary with specific commands, variables, and configuration details

### Core Documentation

**overview.md**
- Overview: High-level introduction to Claude Code architecture and fundamental concepts
- Details: CLI vs SDK distinction, dual execution modes (REPL vs headless -p), account system (claude.ai subscription vs Console API credits), three-tier settings (user/project/local)

**quickstart.md**
- Overview: Getting started guide with installation and first-time setup
- Details: Installation via npm/native binary, authentication dual paths, first session setup, `/login` for account switching

**setup.md**
- Overview: Detailed installation instructions and system requirements
- Details: Installation methods comparison, `claude migrate-installer` behavior (binary moves to `~/.claude/local/claude`), system requirements including Alpine Linux edge cases, auto-update mechanism

**claude-code.md**
- Overview: Main CLI reference with usage patterns and command-line flags
- Details: CLI flags deep dive: `--permission-mode`, `--add-dir`, `--agents` JSON, `--allowedTools`/`--disallowedTools`, `--resume` vs `--continue`, composability with Unix pipes

**cli-reference.md**
- Overview: Comprehensive reference of all CLI commands and options
- Details: Complete flag reference including non-obvious combinations: `--append-system-prompt` (headless only), `--permission-prompt-tool` for CI/CD, `--max-turns` for cost control

**index.md**
- Overview: Documentation index and navigation structure
- Details: Documentation navigation structure

### Configuration & Settings

**settings.md**
- Overview: Complete guide to Claude Code's hierarchical settings system and permissions
- Details: 5-layer hierarchy (enterprise managed → CLI args → local → project → user), settings merging behavior, `permissions.deny` replaces deprecated `ignorePatterns`, `apiKeyHelper` for dynamic credentials (5min TTL), `env` key for environment variables in settings.json

**model-config.md**
- Overview: Model selection, aliases, and configuration options
- Details: Model aliases with special behaviors: `opusplan` (Opus in plan mode → Sonnet execution), `[1m]` suffix for 1M context (Console/API only), `default` alias fallback behavior, `ANTHROPIC_DEFAULT_*_MODEL` must be full model names not aliases

**memory.md**
- Overview: CLAUDE.md file system for project and user memory management
- Details: Recursive CLAUDE.md discovery (cwd → root), import system with `@path/to/file` syntax (max 5 hops), subtree lazy loading, CLAUDE.local.md deprecation (use imports instead), `/memory` command to view loaded memories

**terminal-config.md**
- Overview: Terminal configuration including multiline input and vim mode
- Details: `/terminal-setup` for Shift+Enter in iTerm2/VS Code, Option+Enter on macOS (requires "Use Option as Meta Key"), vim mode subset (i/a/o, h/j/k/l, w/e/b, dd/dw/cc, . repeat), paste mode for large inputs (avoid pasting in VS Code terminal - write to file instead)

**network-config.md**
- Overview: Network, proxy, and certificate configuration
- Details: Proxy environment variables (HTTPS_PROXY/HTTP_PROXY/NO_PROXY), NO_PROXY="*" for bypass all, `NODE_EXTRA_CA_CERTS` for custom CAs, mTLS via `CLAUDE_CODE_CLIENT_CERT/KEY/KEY_PASSPHRASE`, **no SOCKS proxy support**, required URLs: api.anthropic.com, claude.ai, statsig.anthropic.com, sentry.io

**output-styles.md**
- Overview: System prompt customization via output styles
- Details: Output styles **directly modify system prompt** (unlike CLAUDE.md which is user message), non-default styles exclude default efficiency instructions, custom styles in `~/.claude/output-styles/*.md` or `.claude/output-styles/*.md`, `/output-style:new` for creation, `/output-style [name]` to switch

**statusline.md**
- Overview: Custom status line configuration and scripting
- Details: Status line script receives JSON via stdin with session_id/cwd/model/cost, updates max every 300ms, first line of stdout becomes status text, ANSI color codes supported, `/statusline` command helps create script, `padding: 0` for edge-to-edge display

### Features & Workflows

**interactive-mode.md**
- Overview: Interactive REPL features, shortcuts, and session management
- Details: Multiline input (\ + Enter, Option+Enter, /terminal-setup for Shift+Enter), quick shortcuts (# for CLAUDE.md, ! for bash mode, Ctrl+R history search), Ctrl+B for background bash (use BashOutput tool to retrieve), Esc+Esc or /rewind for checkpointing (conversation/code/both modes), Ctrl+L clears screen not history

**headless.md**
- Overview: Non-interactive mode for automation and scripting
- Details: `-p` flag for SDK mode (exits after response), output formats (text/json with metadata/stream-json JSONL), streaming JSON input (JSONL via stdin, requires -p and stream-json), `--continue "query"` for multi-turn automation, `--resume SESSION_ID --no-interactive`, `--permission-prompt-tool mcp__auth` for CI/CD

**common-workflows.md**
- Overview: Common development workflows and usage patterns
- Details: Plan mode with Shift+Tab toggle or `--permission-mode plan`, session continuity with `--continue` (most recent) vs `--resume` (picker with summary/count/branch), extended thinking with Tab or "think hard" phrases (disabled by default, impacts caching), git worktrees for parallel isolated sessions (remember to init dev environment per worktree)

**checkpointing.md**
- Overview: Conversation and code rewinding capabilities
- Details: Esc+Esc or `/rewind` opens menu with 3 modes (conversation/code/both), checkpoints persist across resumed sessions, **critical limitation: Bash command file changes NOT tracked** (only direct tool edits)

**slash-commands.md**
- Overview: Custom slash command creation and configuration
- Details: Frontmatter: `description` (required for SlashCommand tool), `argument-hint`, `allowed-tools`, `model`, `disable-model-invocation`, argument handling ($ARGUMENTS all, $1/$2 positional), `!`backtick`` for bash execution (output added to context, requires allowed-tools), subdirectories for namespacing (shown in description), SlashCommand tool has 15K char budget (SLASH_COMMAND_TOOL_CHAR_BUDGET)

**sub-agents.md**
- Overview: Subagent configuration for specialized tasks
- Details: Precedence: project (.claude/agents/) → CLI --agents JSON → user (~/.claude/agents/), separate context window per invocation (prevents pollution, may add latency), tool inheritance via omitting `tools` field (includes MCP), `model: 'inherit'` to match main conversation, use "PROACTIVELY" in description for auto-delegation, `/agents` command shows available tools including MCP

**hooks.md**
- Overview: Hook system basics and configuration
- Details: Hook types and basic configuration structure

**hooks-guide.md**
- Overview: Comprehensive guide to hook events, configuration, and security
- Details: PreToolUse can block (exit 2 + stderr or JSON permissionDecision), PostToolUse runs after tool (exit 2 shows stderr to Claude, JSON decision: "block"), UserPromptSubmit (exit 0 + stdout = context injection, exit 2 blocks), Stop/SubagentStop (exit 2 continues, JSON decision: "block"), SessionStart matchers (startup/resume/clear/compact), all hooks run in parallel with 60s timeout, **hooks run with your credentials** (review before registering), `CLAUDE_PROJECT_DIR` env var for project-relative paths

### IDE & Integrations

**ide-integrations.md**
- Overview: IDE integration options and approaches
- Details: VS Code extension (Beta, native sidebar, Spark icon, standalone app not CLI wrapper, Cmd+Shift+P → "Update") vs legacy CLI integration (auto-installs from IDE terminal, selection sharing, diff in IDE, Cmd+Option+K for file refs, /ide to connect external terminal), **security warning: auto-edit can modify IDE config files** (use VS Code Restricted Mode, manual approval mode)

**vs-code.md**
- Overview: VS Code extension and legacy CLI integration details
- Details: Extension features (plan mode, auto-accept, multiple sessions, inline diffs), not yet available (MCP/subagent config via CLI first, checkpoints, #/! shortcuts, tab completion), legacy requires CLI command installed (code/cursor/windsurf/codium), Cmd+Shift+P → "Shell Command: Install", `/config` to set diff tool to "auto", third-party provider env vars in extension settings (no login prompt when configured)

**jetbrains.md**
- Overview: JetBrains IDE plugin installation and configuration
- Details: Supported IDEs (IntelliJ, PyCharm, Android Studio, WebStorm, PhpStorm, GoLand), plugin from marketplace, **must completely restart IDE** (may need multiple restarts), Cmd+Esc (Mac) or Ctrl+Esc (Windows/Linux) quick launch, WSL: set `wsl -d Ubuntu -- bash -lic "claude"` in plugin settings, ESC key fix: Settings → Tools → Terminal → uncheck "Move focus to editor with Escape", WSL2 networking: create Windows Firewall rule for subnet or switch to mirrored mode in .wslconfig, Remote Development: plugin on remote host not local

**mcp.md**
- Overview: Model Context Protocol configuration and server management
- Details: Server types: stdio (local `-- npx`), SSE (streaming `--transport sse`), HTTP (`--transport http`), scopes: local (.claude/settings.local.json, was "project" in old versions) → project (.mcp.json, was "global", requires approval) → user (~/.claude/settings.json), env var expansion in .mcp.json with ${VAR} or ${VAR:-default} (works in command/args/env/url/headers), MCP resources via @server:protocol://path, MCP prompts as /mcp__server__prompt, `--` separates CLI flags from server command, OAuth with /mcp command (auto-refresh), output limit 25K tokens (warning at 10K, MAX_MCP_OUTPUT_TOKENS), Windows native requires `cmd /c npx`, `claude mcp serve` to use Claude Code as MCP server, `claude mcp add-from-claude-desktop` (macOS/WSL only), **no wildcard support** in permissions (mcp__github not mcp__github__*)

**third-party-integrations.md**
- Overview: Third-party provider and LLM gateway integration
- Details: Layers: corporate proxy (HTTPS_PROXY for routing) vs LLM gateway (provider-compatible endpoints with auth/tracking), can use both together, auth: ANTHROPIC_AUTH_TOKEN for header, CLAUDE_CODE_SKIP_BEDROCK_AUTH=1 or SKIP_VERTEX_AUTH=1 for gateway-handled auth, LiteLLM unified endpoint (recommended for load balancing/fallback/tracking): ANTHROPIC_BASE_URL + ANTHROPIC_AUTH_TOKEN, provider pass-through: ANTHROPIC_BEDROCK_BASE_URL or ANTHROPIC_VERTEX_BASE_URL, apiKeyHelper for dynamic keys (lower precedence than ANTHROPIC_AUTH_TOKEN, 1hr TTL), debug with `claude /status` and ANTHROPIC_LOG=debug

### CI/CD & Automation

**github-actions.md**
- Overview: GitHub Actions integration with Claude Code
- Details: Quick install: `/install-github-app`, manual: install app + ANTHROPIC_API_KEY secret + copy workflow from examples, **breaking change from beta**: @v1 not @beta, removed `mode` (auto-detect), renamed `direct_prompt` → `prompt`, all CLI via `claude_args`, trigger modes: interactive (responds to @claude mentions in comments) vs automation (runs immediately on schedule/push), Bedrock OIDC: AWS_ROLE_TO_ASSUME + aws-actions/configure-aws-credentials@v4, Vertex Workload Identity: GCP_WORKLOAD_IDENTITY_PROVIDER + google-github-actions/auth@v2, model format: region-prefixed with version (us.anthropic.claude-sonnet-4-5-20250929-v1:0), custom GitHub App (not GITHUB_TOKEN) for branded commits + CI continuation, slash commands in workflows: `prompt: "/review"`, **critical: use App token not GITHUB_TOKEN** for CI pipelines on Claude commits

**gitlab-ci-cd.md**
- Overview: GitLab CI/CD integration
- Details: Minimal job: node:24-alpine3.21 image, apk add git curl bash, npm install -g @anthropic-ai/claude-code, ANTHROPIC_API_KEY masked variable, optional /bin/gitlab-mcp-server for MCP, claude -p with --permission-mode acceptEdits, rules: web or merge_request_event, **mention-driven triggers not built-in** (requires custom webhook listener + pipeline trigger API with AI_FLOW_INPUT/CONTEXT/EVENT variables)

**devcontainer.md**
- Overview: Devcontainer setup for secure unattended operation
- Details: For unattended operation with --dangerously-skip-permissions, security layers: custom firewall (iptables), whitelisted domains only (npm/GitHub/Claude API), default-deny network, container isolation, reference implementation: github.com/anthropics/claude-code/.devcontainer, use cases: CI/CD, team onboarding, secure client isolation, **critical warning: malicious code can exfiltrate credentials** (only trusted repos)

**sdk.md**
- Overview: Claude Agent SDK overview and basic usage
- Details: Claude Agent SDK overview (programmatic API for building agents, not terminal CLI)

**sdk/migration-guide.md**
- Overview: SDK v0.1.0 migration guide with breaking changes
- Details: **CRITICAL v0.1.0 breaking changes**: (1) no default system prompt - must set `systemPrompt: { type: "preset", preset: "claude_code" }` or custom string, (2) no default settings loading - must set `settingSources: ["user", "project", "local"]` to read CLAUDE.md/settings.json, package rename: @anthropic-ai/claude-code → @anthropic-ai/claude-agent-sdk (npm/pip), import changes, why: isolation for CI/CD, deployed apps without filesystem dependency, testing environments, multi-tenant apps, **SDK behaves fundamentally different from CLI** - always explicitly configure

**sdk/sdk-headless.md**
- Overview: SDK headless patterns and automation examples
- Details: Headless automation patterns, output formats (text/json with total_cost_usd/duration_ms/num_turns/session_id, stream-json JSONL), streaming JSON input (JSONL via stdin, requires -p + stream-json output), tool control via --allowedTools/--disallowedTools (space or comma-separated), examples: SRE incident response, security review, multi-turn legal assistant with session persistence, best practices: JSON parsing with jq, error handling, timeouts, rate limiting, --permission-prompt-tool for MCP in headless, --max-turns for cost control

### Enterprise & Infrastructure

**amazon-bedrock.md**
- Overview: AWS Bedrock integration and configuration
- Details: Auth priority: SSO with `AWS_PROFILE` + awsAuthRefresh in settings.json (recommended), AWS_REGION required (does NOT read .aws config), **critical: CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096** (Bedrock's minimum burndown penalty, lower doesn't reduce costs), IAM policy: bedrock:InvokeModel/InvokeModelWithResponseStream/ListInferenceProfiles on inference-profile/application-inference-profile resources, model config: use inference profiles (global.anthropic.claude-sonnet-4-5-20250929-v1:0) to avoid region errors, regional override: ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION, uses Invoke API not Converse API

**google-vertex-ai.md**
- Overview: Google Vertex AI integration and configuration
- Details: Auth: CLAUDE_CODE_USE_VERTEX=1 + CLOUD_ML_REGION (global or regional) + ANTHROPIC_VERTEX_PROJECT_ID, regional override env vars: VERTEX_REGION_CLAUDE_3_5_HAIKU/SONNET/4_0_OPUS for unsupported in global, IAM: roles/aiplatform.user (includes aiplatform.endpoints.predict + computeTokens), **model approval 24-48 hours** (verify in Model Garden before deploying), 1M context beta (requires context-1m-2025-08-07 header, not yet in CLI config)

**bedrock-vertex-proxies.md**
- Overview: Combined proxy and LLM gateway configurations for cloud providers
- Details: Combined configurations: Bedrock + corporate proxy (HTTPS_PROXY + CLAUDE_CODE_USE_BEDROCK + AWS_REGION), Bedrock + LLM gateway (ANTHROPIC_BEDROCK_BASE_URL + CLAUDE_CODE_SKIP_BEDROCK_AUTH=1), Vertex + corporate proxy (HTTPS_PROXY + CLAUDE_CODE_USE_VERTEX + CLOUD_ML_REGION + PROJECT_ID), Vertex + LLM gateway (ANTHROPIC_VERTEX_BASE_URL + CLAUDE_CODE_SKIP_VERTEX_AUTH=1), deployment selection: direct (simplest), proxy (traffic monitoring/compliance), gateway (usage tracking, dynamic switching, rate limiting, centralized auth)

**llm-gateway.md**
- Overview: LLM gateway integration patterns and best practices
- Details: LiteLLM unified endpoint (recommended): ANTHROPIC_BASE_URL=https://litellm:4000 + ANTHROPIC_AUTH_TOKEN, benefits: load balancing, fallback routing, consistent cost tracking, dynamic API keys via apiKeyHelper (CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000 for 1hr refresh, lower precedence than ANTHROPIC_AUTH_TOKEN), headers sent as both Authorization and X-Api-Key, organizational best practices: org-wide CLAUDE.md at /Library/Application Support/ClaudeCode/CLAUDE.md (macOS), repo-level checked into source control, create one-click install, central MCP config in .mcp.json

**iam.md**
- Overview: Permission system architecture and enterprise policies
- Details: Permission modes: default (prompts each tool) / acceptEdits (auto file edits) / plan (read-only) / bypassPermissions (dangerous, enterprise-disableable), tool categories: no permission (Glob/Grep/Read/NotebookRead/Task/TodoWrite) vs required (Bash/Edit/MultiEdit/NotebookEdit/SlashCommand/WebFetch/WebSearch/Write), pattern syntax: tool-specific (Bash prefix matching, Read/Edit gitignore syntax with /absolute vs //filesystem-root vs ~/home vs ./relative), **critical limitation: Bash prefix bypass** (options/variables/redirects circumvent, use hooks for robust validation), MCP no wildcards (mcp__github or mcp__github__get_issue, NOT mcp__github__*), managed policies locations (cannot override): /Library/Application Support/ClaudeCode/managed-settings.json (macOS), /etc/claude-code/managed-settings.json (Linux), C:\ProgramData\ClaudeCode\managed-settings.json (Windows), precedence: enterprise → CLI → local → project → user

**security.md**
- Overview: Security safeguards, limitations, and best practices
- Details: Prompt injection: separate context for WebFetch (prevents injection), command injection detection, trust verification for new codebases/MCP, curl/wget blocklist by default, **permission bypasses: Bash prefix matching easily circumvented** (see IAM docs), use hooks for validation, IDE auto-edit risk: can modify IDE config files that execute automatically (VS Code Restricted Mode, manual approval mode, trusted prompts only), credential storage: macOS Keychain encrypted, apiKeyHelper refreshes 5min or HTTP 401, awsAuthRefresh for SSO (output shown), awsCredentialExport for direct JSON (silent)

**monitoring-usage.md**
- Overview: OpenTelemetry monitoring and metrics collection
- Details: OTel central collector: CLAUDE_CODE_ENABLE_TELEMETRY=1 + OTEL_METRICS_EXPORTER=otlp + OTEL_LOGS_EXPORTER=otlp + OTEL_EXPORTER_OTLP_PROTOCOL=grpc + OTEL_EXPORTER_OTLP_ENDPOINT + OTEL_EXPORTER_OTLP_HEADERS, dynamic headers: otelHeadersHelper script outputs JSON (**critical: fetched only at startup not runtime**, use OTel Collector as proxy for frequent refresh), cardinality control: OTEL_METRICS_INCLUDE_SESSION_ID/ACCOUNT_UUID=false, multi-team tracking: OTEL_RESOURCE_ATTRIBUTES="department=eng,team.id=platform,cost_center=123" (W3C Baggage format, **NO SPACES**, comma-separated key=value), key metrics: claude_code.cost.usage (USD approximate), claude_code.token.usage (by type), claude_code.active_time.total (not idle), key events: claude_code.tool_result (decision/source/parameters), claude_code.api_request (token/cost breakdown), claude_code.user_prompt (length default, full with OTEL_LOG_USER_PROMPTS=1), default intervals: 60s metrics, 5s logs

**data-usage.md**
- Overview: Data retention, training policies, and telemetry
- Details: Training policies: Consumer (Free/Pro/Max) opt-in default enabled as of Aug 28 2025, 5yr retention if opted in / 30day if out, change at claude.ai/settings/privacy; Commercial (Team/Enterprise/API) no training, 30day retention default, zero retention available, **Bedrock/Vertex follow AWS/GCP policies not Anthropic's**, telemetry by provider: Claude API (Statsig/Sentry/bug on by default, opt-out: DISABLE_TELEMETRY/ERROR_REPORTING/BUG_COMMAND=1), Bedrock/Vertex (all off by default), CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 disables all, Statsig/Sentry encrypted in transit (TLS) and at rest (AES-256)

### Operations & Troubleshooting

**troubleshooting.md**
- Overview: Common installation and operational issues with fixes
- Details: WSL installation fix: `npm config set os linux && npm install -g @anthropic-ai/claude-code --force --no-os-check`, force clean auth: `rm -rf ~/.config/claude-code/auth.json && claude`, **WSL cross-filesystem search degradation**: projects on /mnt/c/ (Windows FS) slow, move to /home/ (Linux FS) or use native Windows, WSL2 JetBrains detection: create Firewall rule for subnet or mirrored networking in .wslconfig, search/discovery failures: install system ripgrep (brew/winget/apt) + USE_BUILTIN_RIPGREP=0, verify installation: `claude doctor`, binary location: `~/.claude/local/claude` after migrate-installer

**costs.md**
- Overview: Cost metrics, team rate limits, and cost management
- Details: Average cost $6/dev/day (90% under $12/day), monthly $100-200/dev with Sonnet 4.5 (high variance), background token usage ~$0.04/session (summarization + /cost checks), **team rate limits org-level not per-user hard caps** (users can burst when others idle): 1-5 users 200-300k TPM/user, 5-20 users 100-150k TPM/user, 20-50 users 50-75k TPM/user, 50-100 users 25-35k TPM/user, 100-500 users 15-20k TPM/user, 500+ users 10-15k TPM/user, cost reduction: customize compaction in CLAUDE.md ("focus on test output and code changes"), manual `/compact [instructions]`, auto-compact at 95% context (toggle in /config), cost tracking: individual `/cost` (not Pro/Max), team-wide Console (Admin/Billing roles), "Claude Code" workspace auto-created (API key creation disabled - auth only), Bedrock/Vertex: use LiteLLM for spend tracking

**analytics.md**
- Overview: Claude Code analytics dashboard and metrics
- Details: Access: console.anthropic.com/claude-code (Console/API users only), required roles: Primary Owner/Owner/Billing/Admin/Developer (NOT User/Claude Code User/Membership Admin), metrics: lines accepted (total, doesn't track deletions), suggestion accept rate (% of Edit/MultiEdit/Write/NotebookEdit accepted), activity (users + sessions per day, dual Y-axis), spend (users + dollars per day, dual Y-axis), team insights (per-user spend + lines this month, API key users by identifier, OAuth by email)

**legal-and-compliance.md**
- Overview: Legal agreements, compliance, and security reporting
- Details: Commercial agreement extension: existing commercial (1P direct API or 3P Bedrock/Vertex) automatically extends to Claude Code unless mutually agreed otherwise, healthcare compliance: **BAA automatically extends** if customer executed BAA AND activated Zero Data Retention (no separate amendment), security vuln reporting: HackerOne form at hackerone.com/anthropic-vdp/reports/new

## How to Use This Index

When discussing Claude Code topics:
1. **Locate the relevant file(s)** in the index above based on your question
2. **Reference specific files** for complete context: e.g., "See @claude-code-docs/mcp.md for MCP configuration details"
3. **Combine related files** for comprehensive understanding: e.g., MCP setup requires both mcp.md and settings.md

## Common Commands

### Installation & Setup
```bash
# Check installation health and version
claude doctor

# Update to latest version
claude update

# Login or switch accounts
/login
```

### Running Claude Code
```bash
# Interactive mode
claude

# Non-interactive (SDK mode) - query and exit
claude -p "explain this function"

# Continue most recent conversation
claude -c

# Resume specific session
claude -r <session-id>

# Plan mode (read-only analysis)
claude --permission-mode plan
```

### Configuration
```bash
# Open settings interface
/config

# Edit memory files
/memory

# Configure custom status line
/statusline

# Switch models
/model sonnet
/model opus

# Check current status
/status

# Configure MCP servers
claude mcp
```

### Session Management
```bash
# Clear current conversation
/clear

# Rewind conversation or code changes
/rewind  # or press Esc+Esc

# Compact conversation to reduce token usage
/compact [optional instructions]
```

## Architecture Overview

### Core Components

**Dual Execution Modes:**
1. **Interactive REPL Mode**: `claude` - Full conversational interface with session management
2. **Headless/Print Mode**: `claude -p "query"` - One-shot execution for scripting/automation

**Dual Account System:**
- **Claude.ai** (Subscription plans: Pro/Max) - Unified subscription for CLI + web interface
- **Claude Console** (API credits) - Creates auto-managed "Claude Code" workspace for cost tracking

**Critical Distinction - CLI vs SDK:**
- **Claude Code CLI**: Terminal-based AI coding assistant (this documentation)
- **Claude Agent SDK**: Programmatic API for building custom AI agents (package: `@anthropic-ai/claude-agent-sdk`)
- SDK was renamed from `@anthropic-ai/claude-code` to reflect its broader agent-building capabilities

### Configuration System

**Hierarchical Settings (5 layers, highest to lowest priority):**
1. **Enterprise managed policies** - Cannot be overridden
2. **Command line arguments** - Session-specific overrides
3. **Local project settings** - `.claude/settings.local.json` (git-ignored)
4. **Shared project settings** - `.claude/settings.json` (version controlled)
5. **User settings** - `~/.claude/settings.json` (global across all projects)

Settings are **merged** down the hierarchy, with more specific settings adding to or overriding broader ones.

**Three Parallel Configuration Systems:**
1. **CLAUDE.md files**: Natural language instructions and context (memory)
2. **settings.json files**: Structured permissions, environment variables, tool behavior
3. **MCP servers**: External tool integrations via Model Context Protocol

### Memory System (CLAUDE.md)

**Memory Hierarchy:**
- **Enterprise policy**: `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS)
- **User memory**: `~/.claude/CLAUDE.md` (personal, all projects)
- **Project memory**: `./CLAUDE.md` or `./.claude/CLAUDE.md` (team-shared)

**Discovery Mechanism:**
- Reads CLAUDE.md files **recursively** from `cwd` up to (but not including) root `/`
- CLAUDE.md files in subtrees loaded **only when files in those subtrees are read** (lazy loading)

**Import System:**
```markdown
# Import other files
@README.md
@docs/git-instructions.md
@~/.claude/my-project-instructions.md

# Individual preferences (not in version control)
- @~/.claude/my-project-instructions.md
```

**Import Rules:**
- Both relative and absolute paths supported
- Imports not evaluated inside code spans (`` `@anthropic-ai/claude-code` `` ignored)
- Recursive imports allowed (max depth: 5 hops)
- View loaded memories with `/memory` command

### Permission System

**Permission Modes (Toggle with Shift+Tab):**
1. **Normal Mode**: Prompts for each tool use
2. **Auto-Accept Mode** (`acceptEdits`): Auto-approves file edits, still asks for Bash/WebFetch
3. **Plan Mode**: Read-only analysis (perfect for exploration without changes)
4. **Bypass Mode** (`bypassPermissions`): No prompts (use with caution, can be enterprise-disabled)

**Tool Categories:**
- **No permission required**: Glob, Grep, Read, NotebookRead, Task, TodoWrite
- **Permission required**: Bash, Edit, MultiEdit, NotebookEdit, SlashCommand, WebFetch, WebSearch, Write

**Permission Pattern Examples:**
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Bash(git status:*)",
      "Read(~/.zshrc)"
    ],
    "ask": [
      "Bash(git push:*)"
    ],
    "deny": [
      "Bash(curl:*)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "WebFetch"
    ],
    "additionalDirectories": ["../docs/"]
  }
}
```

**Critical Limitation**: Bash permissions use **prefix matching, not regex** - can be bypassed with command-line options, variables, or redirects. Not suitable as sole security mechanism.

### Model Configuration

**Model Aliases:**
- `default` - Recommended model (account-dependent, may fall back)
- `sonnet` - Latest Sonnet (currently 4.5)
- `opus` - Opus 4.1
- `haiku` - Fast, efficient
- `sonnet[1m]` - 1M token context window (Console/API users only)
- `opusplan` - Opus in plan mode, Sonnet in execution (hybrid)

**Model Setting Priority (Highest to Lowest):**
1. During session: `/model <alias|name>`
2. At startup: `claude --model <alias|name>`
3. Environment variable: `ANTHROPIC_MODEL=<alias|name>`
4. Settings file: `"model": "opus"` in settings.json

**Model Override Environment Variables:**
```bash
ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-1
ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-5-20250929
ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-3-5-haiku-20241022
CLAUDE_CODE_SUBAGENT_MODEL=sonnet
```

### Slash Commands

**Custom Slash Command Structure:**
```markdown
---
description: "What this command does (shown in /help)"
argument-hint: "[pr-number] [priority]"
allowed-tools: Bash(git add:*), Bash(git commit:*)
model: sonnet
disable-model-invocation: false
---

# Command Content
Review PR #$1 with priority $2.

## Context
- Current git status: !`git status`
- Recent commits: !`git log --oneline -10`

## Instructions
Create detailed review focusing on security and performance.
```

**Command Features:**
- `$ARGUMENTS` - All arguments as single string
- `$1`, `$2`, `$3` - Individual positional arguments
- `!` prefix - Execute bash before command runs (output added to context)
- `@` prefix - Include file contents
- Subdirectories for organization (shown in description, not command name)

**SlashCommand Tool:**
- Claude can invoke custom slash commands programmatically
- Requires `description` frontmatter field
- Character budget: 15,000 (configurable via `SLASH_COMMAND_TOOL_CHAR_BUDGET`)
- Disable specific command: `disable-model-invocation: true`

**Command Locations:**
- **Project**: `.claude/commands/` - "(project)" in /help
- **User**: `~/.claude/commands/` - "(user)" in /help

### MCP (Model Context Protocol) Integration

**MCP Server Types:**
```bash
# stdio (local process)
claude mcp add airtable --env AIRTABLE_API_KEY=KEY -- npx -y airtable-mcp-server

# SSE (Server-Sent Events)
claude mcp add --transport sse linear https://mcp.linear.app/sse

# HTTP (request/response)
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**MCP Server Scopes:**
- **local** (default): `.claude/settings.local.json` - Personal, highest precedence
- **project**: `.mcp.json` - Team-shared, version controlled
- **user**: `~/.claude/settings.json` - Personal, cross-project

**Environment Variable Expansion in .mcp.json:**
```json
{
  "mcpServers": {
    "api-server": {
      "type": "sse",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

**MCP Resources (@ mentions):**
```
@server:protocol://resource/path
@github:issue://123
@docs:file://api/authentication
```

**MCP Prompts as Slash Commands:**
```
/mcp__github__list_prs
/mcp__jira__create_issue "Bug title" high
```

### Subagents

**Subagent Configuration:**
```markdown
---
name: code-reviewer
description: Expert code review. Use PROACTIVELY after code changes.
tools: Read, Grep, Glob, Bash
model: inherit  # OR sonnet, opus, haiku
---

You are a senior code reviewer ensuring high standards.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is simple and readable
- No exposed secrets
- Good test coverage
```

**Subagent Precedence:**
1. Project subagents (`.claude/agents/`)
2. CLI `--agents` JSON flag (for testing/automation)
3. User subagents (`~/.claude/agents/`)

**Key Features:**
- Separate context window (prevents main conversation pollution)
- Tool inheritance: Omit `tools` field to inherit all (including MCP)
- Proactive delegation: Use "use PROACTIVELY" in description
- Can use different models per subagent

### Hooks System

**Hook Events:**
- `PreToolUse` - Before tool execution (can block)
- `PostToolUse` - After tool execution
- `UserPromptSubmit` - User submits prompt (can block)
- `Notification` - Claude needs input
- `Stop` - Response complete
- `SubagentStop` - Subagent task done
- `PreCompact` - Before compaction
- `SessionStart` - Session starts/resumes
- `SessionEnd` - Session ends

**Hook Configuration:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/bash-log.txt"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read f; [[ $f =~ \\.ts$ ]] && prettier --write \"$f\"; }"
          }
        ]
      }
    ]
  }
}
```

**Security Note**: Hooks run with your credentials - review before registering.

### Output Styles

**Built-in Styles:**
1. **Default** - Standard software engineering agent
2. **Explanatory** - Adds educational "Insights" sections
3. **Learning** - Collaborative mode with `TODO(human)` markers

**How They Work:**
- Output styles **directly modify the system prompt**
- Non-default styles exclude default efficiency instructions
- Unlike CLAUDE.md (user message) or `--append-system-prompt` (appends)

**Custom Output Styles:**
```markdown
---
name: My Custom Style
description: Brief description shown to user
---

# Custom Style Instructions
[Your custom system prompt modifications here...]
```

**Locations:**
- User level: `~/.claude/output-styles/*.md`
- Project level: `.claude/output-styles/*.md`

**Commands:**
- `/output-style:new I want an output style that...`
- `/output-style [style]`

### Status Line

**Configuration:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

**JSON Input (via stdin):**
```json
{
  "hook_event_name": "Status",
  "session_id": "...",
  "cwd": "/current/working/directory",
  "model": {"id": "claude-opus-4-1", "display_name": "Opus"},
  "workspace": {
    "current_dir": "/current/working/directory",
    "project_dir": "/original/project/directory"
  },
  "cost": {
    "total_cost_usd": 0.01234,
    "total_duration_ms": 45000,
    "total_lines_added": 156,
    "total_lines_removed": 23
  }
}
```

## Key Features and Workflows

### Session Continuity
- `--continue` / `-c` - Resume most recent conversation
- `--resume` / `-r` - Interactive picker for past conversations
- Full context restoration: tool state, message history, attachments
- Conversations auto-delete after 30 days (configurable via `cleanupPeriodDays`)

### Extended Thinking
- Disabled by default; enable with `Tab` key or phrases like "think hard"
- Best for: architectural decisions, debugging, planning, evaluating tradeoffs
- Set `MAX_THINKING_TOKENS` environment variable to enable permanently
- **Note**: Impacts prompt caching efficiency

### Interactive Mode Features

**Multiline Input:**
- `\` + Enter (works everywhere)
- `Option+Enter` on macOS
- Run `/terminal-setup` to install `Shift+Enter` for iTerm2/VS Code

**Quick Input Shortcuts:**
- `#` at start - Add to CLAUDE.md with file selection prompt
- `!` at start - Bash mode (runs commands, adds output to conversation)
- `Ctrl+R` - Reverse search command history

**Background Bash Commands:**
- `Ctrl+B` moves Bash tool to background
- Use `BashOutput` tool to retrieve output
- Useful for: build tools, test runners, dev servers

**Rewinding/Checkpointing:**
- `Esc` + `Esc` or `/rewind` - Opens rewind menu
- Three modes: conversation only, code only, or both
- **Limitation**: Bash command file changes NOT tracked

### Headless Mode (Automation)

**Output Formats:**
```bash
# Plain text response
claude -p "query" --output-format text

# Structured JSON with metadata
claude -p "query" --output-format json

# Real-time streaming JSONL
claude -p "query" --output-format stream-json
```

**Tool Control:**
```bash
claude -p "query" \
  --allowedTools "Bash(npm install),mcp__filesystem" \
  --disallowedTools "Bash(git commit),mcp__github"
```

**Multi-turn Automation:**
```bash
# Continue from most recent
claude --continue "refactor for performance"

# Resume specific session non-interactively
claude --resume SESSION_ID "fix linting" --no-interactive
```

**Permission Handling:**
```bash
# Use MCP tool for permission prompts
claude -p "query" --permission-prompt-tool mcp__auth__prompt
```

### File References (`@` syntax)

- `@src/utils/auth.js` - Includes full file content
- `@src/components` - Shows directory listing
- `@github:issue://123` - Fetches MCP resources
- **Auto-includes CLAUDE.md** from file's directory and parent directories

### Git Worktrees for Parallel Sessions

```bash
# Create separate worktree for isolated work
git worktree add ../project-feature-a -b feature-a
cd ../project-feature-a && claude
```

**Benefits:**
- Independent file state (no interference)
- Shared Git history and remotes
- Multiple Claude instances on same repo

**Remember**: Initialize dev environment per worktree (npm install, etc.)

### Unix-Style Integration

```bash
# Piping
cat build-error.txt | claude -p 'explain root cause' > output.txt

# Streaming
tail -f app.log | claude -p "alert if errors spike"

# Composability
claude -p "translate new strings to French and raise PR"
```

## Important Technical Details

### Authentication & Credential Storage

- Credentials stored locally after first `/login`
- Console authentication creates "Claude Code" workspace automatically
- Cannot create API keys for "Claude Code" workspace (dedicated for CLI only)
- Enterprise: Support for custom `apiKeyHelper` scripts in settings.json

### Installation & Binary Location

- **Post-migration path**: `~/.claude/local/claude` (after `claude migrate-installer`)
- Three installation methods: npm global, native binary (beta), local migration
- Verify with `claude doctor`

### SDK vs CLI Differences (Critical)

**Claude Agent SDK v0.1.0+ Breaking Changes:**
1. **No default system prompt** - Must set `systemPrompt: { type: "preset", preset: "claude_code" }`
2. **No default settings loading** - Does not read CLAUDE.md, settings.json unless `settingSources` specified
3. **Isolation by design** - SDK apps independent of filesystem config

**When This Matters**: Building custom agents/automation with SDK behaves differently from CLI.

### Environment Variables

**Model Control:**
```bash
ANTHROPIC_MODEL=sonnet
ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-5-20250929
CLAUDE_CODE_SUBAGENT_MODEL=haiku
```

**Behavior Tuning:**
```bash
CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1
BASH_DEFAULT_TIMEOUT_MS=120000
BASH_MAX_OUTPUT_LENGTH=50000
```

**Context Management:**
```bash
CLAUDE_CODE_MAX_OUTPUT_TOKENS=8000
MAX_MCP_OUTPUT_TOKENS=25000
SLASH_COMMAND_TOOL_CHAR_BUDGET=15000
MAX_THINKING_TOKENS=10000
```

**Privacy/Telemetry:**
```bash
DISABLE_TELEMETRY=1
DISABLE_ERROR_REPORTING=1
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
```

**Network Configuration:**
```bash
HTTPS_PROXY=https://proxy.example.com:8080
HTTP_PROXY=http://proxy.example.com:8080
NO_PROXY="localhost,192.168.1.1,example.com"
NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem

# mTLS
CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem
CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem
CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

### Required Network Access

- `api.anthropic.com` - Claude API endpoints
- `claude.ai` - WebFetch safeguards
- `statsig.anthropic.com` - Telemetry
- `sentry.io` - Error reporting

### System Requirements

- Node.js 18+ (for npm install)
- 4GB+ RAM
- Supported OS: macOS 10.15+, Ubuntu 20.04+/Debian 10+, Windows 10+ (WSL/Git Bash)
- Best shells: Bash, Zsh, Fish
- **Alpine Linux/musl**: Requires manual install of `libgcc`, `libstdc++`, `ripgrep`; set `USE_BUILTIN_RIPGREP=0`

### Auto-Update Behavior

- Checks on startup and periodically
- Downloads in background, applies on next start
- Disable: `DISABLE_AUTOUPDATER=1` or in settings.json
- Manual update: `claude update`

## Non-Obvious Behaviors

### Settings vs Memory Distinction

- **Settings (JSON)**: Tool behavior, permissions, environment
- **Memory (Markdown)**: Instructions and context for Claude
- Different precedence hierarchies
- System prompt not published (use CLAUDE.md or `--append-system-prompt`)

### Permission System Bypass Scenarios

- Bash permissions use prefix matching, not regex
- Easily bypassed with options/variables/redirects
- Use hooks for robust validation

### CLAUDE.local.md Deprecation

- **Old**: `./CLAUDE.local.md` for personal project preferences
- **New**: Use imports in CLAUDE.md: `@~/.claude/my-project-instructions.md`
- Better for multiple git worktrees

### Model Fallback Behavior

- `default` alias may automatically fall back (e.g., Opus → Sonnet for usage limits)
- Account-type dependent

### CLI vs SDK Mode (`-p` flag)

- `claude -p "query"` - SDK query mode (programmatic, exits after response)
- `claude "query"` - Starts REPL with initial prompt (interactive)

### Conversation Storage

- All conversations auto-saved locally
- Retention: 30 days default
- Directory-scoped (tied to working directory)
- Location varies by installation type

## Tips for Effective Use

### Structuring CLAUDE.md

```markdown
# [Project Name] - CLAUDE.md

## Project Overview
@README.md for full description.

## Common Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## Code Style
- Use 2-space indentation
- Prefer const over let
- Always use descriptive variable names

## Architecture Patterns
- Feature-based folder structure
- State management with Redux Toolkit
- API calls in services/ directory

## Testing Guidelines
- Unit tests co-located with code
- Integration tests in tests/
- Use data-testid for selectors

## Personal Preferences (via import)
@~/.claude/my-preferences.md
```

### Permission Presets

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run:*)",
      "Bash(git diff:*)",
      "Bash(git status:*)"
    ],
    "ask": [
      "Bash(git push:*)",
      "Bash(git commit:*)"
    ],
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(secrets/**)",
      "Read(**/credentials.json)",
      "Bash(rm:*)",
      "Bash(curl:*)"
    ]
  }
}
```

### Designing Focused Subagents

- Single, clear responsibility
- Detailed system prompts with examples
- Limit tool access to necessary only
- Use "PROACTIVELY" in description for automatic delegation

### Combining Hooks with Permissions

```json
{
  "permissions": {
    "deny": ["WebFetch"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "prettier --write $(jq -r '.tool_input.file_path')"}
        ]
      }
    ]
  }
}
```

## IDE Integration

### VS Code Extension (Beta)

**Installation:**
- Native sidebar panel accessed via Spark icon
- Runs as standalone application, not CLI wrapper
- Extension updates: `Cmd+Shift+P` → "Claude Code: Update"

**Features:**
- Plan mode, Auto-accept edits mode
- Multiple simultaneous sessions
- Inline diffs in sidebar (drag wider to see better)

**Not Yet Available in Extension:**
- MCP server configuration (configure via CLI first, extension will use them)
- Subagent configuration (configure via CLI)
- Checkpoints
- `#` shortcut to add to memory
- `!` shortcut for bash commands
- Tab completion for file paths

### Legacy CLI Integration (VS Code, Cursor, Windsurf, VSCodium)

**Auto-installs when running from IDE's integrated terminal:**
- Selection context sharing (current selection/tab automatically shared)
- Diff viewing in IDE instead of terminal
- File reference shortcuts: `Cmd+Option+K` (Mac) or `Alt+Ctrl+K` (Windows/Linux)
- Automatic diagnostic sharing (lint/syntax errors)

**External Terminal Connection:**
```bash
/ide  # Connect external terminal to IDE
```

**Diff Tool Configuration:**
```bash
claude
/config  # Set diff tool to "auto"
```

**Required:** IDE CLI command must be installed:
- VS Code: `code` command
- Cursor: `cursor` command
- Windsurf: `windsurf` command
- VSCodium: `codium` command

Install via command palette: `Cmd+Shift+P` → "Shell Command: Install 'code' command in PATH"

### JetBrains IDE Integration

**Supported IDEs:**
IntelliJ IDEA, PyCharm, Android Studio, WebStorm, PhpStorm, GoLand

**Installation:**
1. Install [Claude Code plugin](https://plugins.jetbrains.com/plugin/24099-claude-code) from marketplace
2. **Completely restart IDE** (may need multiple restarts)
3. Remote Development: Install plugin on remote host via Settings → Plugin (Host)

**Quick Launch:**
- `Cmd+Esc` (Mac) or `Ctrl+Esc` (Windows/Linux)

**Plugin Settings** (Settings → Tools → Claude Code [Beta]):
- Custom Claude command path
- WSL users: Set `wsl -d Ubuntu -- bash -lic "claude"` (replace distribution name)
- Option+Enter for multiline prompts (macOS only)

**ESC Key Configuration Fix:**
If ESC doesn't interrupt Claude operations:
1. Settings → Tools → Terminal
2. Uncheck "Move focus to the editor with Escape" OR delete "Switch focus to Editor" shortcut
3. Apply changes

**WSL Configuration:**
- May require additional networking/firewall configuration
- Create Windows Firewall rule for WSL2 subnet:
  ```powershell
  # As Administrator, adjust IP range to match your WSL2 subnet
  New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
  ```
- Alternative: Switch to mirrored networking in `.wslconfig`

### Third-Party Provider Configuration (VS Code Extension)

**Environment Variables in Extension Settings:**
```
Settings → Search "Claude Code: Environment Variables"
```

**Key Variables:**
- `CLAUDE_CODE_USE_BEDROCK="1"` or `"true"`
- `CLAUDE_CODE_USE_VERTEX="1"` or `"true"`
- `ANTHROPIC_API_KEY="your-api-key"`
- `AWS_REGION="us-east-2"`
- `AWS_PROFILE="your-profile"`
- `CLOUD_ML_REGION="global"` or `"us-east5"`
- `ANTHROPIC_VERTEX_PROJECT_ID="your-project-id"`
- `ANTHROPIC_MODEL="us.anthropic.claude-3-7-sonnet-20250219-v1:0"`
- `ANTHROPIC_SMALL_FAST_MODEL="us.anthropic.claude-3-5-haiku-20241022-v1:0"`

**Note:** Extension will NOT prompt for login when third-party providers configured.

### Security Considerations for IDE Usage

**Auto-Edit Risk:**
- Claude Code with auto-edit permissions can modify IDE configuration files
- IDE config files may be automatically executed
- Could bypass Claude Code's permission prompts for bash execution

**Mitigations:**
- **VS Code**: Enable [Restricted Mode](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode)
- **All IDEs**: Use manual approval mode for edits
- Ensure Claude only used with trusted prompts

## MCP Integration Details

### MCP Configuration Scopes

**Scope Hierarchy (Highest to Lowest Precedence):**
1. **local** (default) - `.claude/settings.local.json` (git-ignored)
2. **project** - `.mcp.json` (version controlled, requires approval prompt)
3. **user** - `~/.claude/settings.json` (personal cross-project)

**Security Note:** Claude Code prompts for approval before using project-scoped servers from `.mcp.json`. Reset approvals: `claude mcp reset-project-choices`.

### MCP Server Configuration

**Startup Timeout:**
```bash
MCP_TIMEOUT=10000 claude  # 10-second timeout
```

**Output Limits:**
```bash
MAX_MCP_OUTPUT_TOKENS=50000  # Default: 25000
```
Warning displayed at 10,000 tokens.

**Windows MCP (Native, not WSL):**
```bash
# Requires cmd /c wrapper for npx
claude mcp add my-server -- cmd /c npx -y @some/package
```

### Claude Code as MCP Server

**Usage:**
```bash
claude mcp serve
```

**In Claude Desktop (claude_desktop_config.json):**
```json
{
  "mcpServers": {
    "claude-code": {
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

**Note:** MCP client responsible for implementing user confirmation - Claude Code's permission prompts not invoked.

### MCP Import from Claude Desktop

**Commands:**
```bash
claude mcp add-from-claude-desktop  # Interactive selection
claude mcp add-from-claude-desktop --scope user  # Add to user config
```

**Behavior:** macOS and WSL only. Reads Claude Desktop config from standard location.

### Non-Obvious MCP Behaviors

- `local` scope stored in `.claude/settings.local.json` (was called `project` in older versions)
- `project` scope means shared via `.mcp.json` (was called `global` in older versions)
- `--` (double dash) separates Claude CLI flags from MCP server command
- OAuth authentication works with both SSE and HTTP transports
- Use `/mcp` command for OAuth, token refresh automatic
- MCP tools automatically available - no special permission needed for discovery

### Enterprise MCP Configuration

**Managed MCP Locations:**
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Windows: `C:\ProgramData\ClaudeCode\managed-mcp.json`
- Linux: `/etc/claude-code/managed-mcp.json`

**Precedence:** Enterprise MCP has highest precedence when `useEnterpriseMcpConfigOnly` enabled.

### Third-Party Provider Integration

**Provider Configuration Layers:**
- **Corporate proxy**: HTTP/HTTPS proxy for traffic routing (`HTTPS_PROXY`, `HTTP_PROXY`)
- **LLM Gateway**: Provider-compatible endpoints with auth/tracking/budgeting
- **Both can be used together**

**Authentication Environment Variables:**
- `ANTHROPIC_AUTH_TOKEN` - Used for `Authorization` header
- `CLAUDE_CODE_SKIP_BEDROCK_AUTH=1` - Gateway handles AWS auth
- `CLAUDE_CODE_SKIP_VERTEX_AUTH=1` - Gateway handles GCP auth

**LiteLLM Unified Endpoint (Recommended):**
```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key
```

**Dynamic API Key via Helper:**
```json
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```
```bash
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000  # 1-hour refresh
```

**Provider-Specific Pass-Through:**
```bash
# Bedrock via LiteLLM
export ANTHROPIC_BEDROCK_BASE_URL=https://gateway:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1

# Vertex via LiteLLM
export ANTHROPIC_VERTEX_BASE_URL=https://gateway:4000/vertex_ai/v1
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
```

**Debugging:**
```bash
claude /status  # Shows applied authentication, proxy, URL settings
export ANTHROPIC_LOG=debug  # Log requests
```

## CI/CD Integration

### GitHub Actions Setup

**Quick Installation:**
```bash
# From Claude CLI
/install-github-app
```

**Manual Setup:**
1. Install Claude GitHub app: https://github.com/apps/claude
2. Add `ANTHROPIC_API_KEY` to repository secrets
3. Copy workflow from: https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml

**Breaking Change from Beta:**
- Version: `@v1` (no longer `@beta`)
- Removed: `mode` parameter (auto-detected)
- Renamed: `direct_prompt` → `prompt`
- Consolidated: All CLI options via `claude_args` parameter

### GitLab CI/CD Setup

**Minimal Job Configuration:**
```yaml
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk add --no-cache git curl bash
    - npm install -g @anthropic-ai/claude-code
  script:
    - /bin/gitlab-mcp-server || true  # Optional MCP integration
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Review this MR'}"
      --permission-mode acceptEdits
      --allowedTools "Bash(*) Read(*) Edit(*) Write(*) mcp__gitlab"
      --debug
```

**Required Variable:** `ANTHROPIC_API_KEY` (masked CI/CD variable)

### AWS Bedrock Integration (GitHub Actions)

**Authentication:** OIDC (no static keys)

**Required Secrets:**
- `AWS_ROLE_TO_ASSUME` - IAM role ARN
- `AWS_REGION` - Bedrock region

**Configuration:**
```yaml
- name: Configure AWS Credentials (OIDC)
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
    aws-region: us-west-2

- uses: anthropics/claude-code-action@v1
  with:
    use_bedrock: "true"
    claude_args: '--model us.anthropic.claude-sonnet-4-5-20250929-v1:0'
```

**Model ID Format:** Region-prefixed with version suffix

### Google Vertex AI Integration (GitHub Actions)

**Authentication:** Workload Identity Federation (no service account keys)

**Required Secrets:**
- `GCP_WORKLOAD_IDENTITY_PROVIDER` - Full provider resource name
- `GCP_SERVICE_ACCOUNT` - Service account email
- `CLOUD_ML_REGION` - Vertex region (e.g., `us-east5`)

**Configuration:**
```yaml
- name: Authenticate to Google Cloud
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
    service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

- uses: anthropics/claude-code-action@v1
  with:
    use_vertex: "true"
    claude_args: '--model claude-sonnet-4@20250514'
  env:
    ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
    CLOUD_ML_REGION: us-east5
```

### Custom GitHub App (Enterprise)

**Why Create Your Own:**
- Branded username in commits/comments
- Custom authentication flows
- Fine-grained repository access

**Minimal Required Permissions:**
- Contents: Read & Write
- Issues: Read & Write
- Pull Requests: Read & Write

**Usage:**
```yaml
- name: Generate GitHub App token
  id: app-token
  uses: actions/create-github-app-token@v2
  with:
    app-id: ${{ secrets.APP_ID }}
    private-key: ${{ secrets.APP_PRIVATE_KEY }}

- uses: anthropics/claude-code-action@v1
  with:
    github_token: ${{ steps.app-token.outputs.token }}
```

**Critical:** Use GitHub App token (not `GITHUB_TOKEN`) to enable CI pipelines on Claude's commits.

### Advanced Workflow Patterns

**Unified CLI Arguments:**
```yaml
claude_args: |
  --max-turns 5
  --model claude-sonnet-4-5-20250929
  --mcp-config /path/to/config.json
  --allowed-tools Bash,Read,Edit,Write
  --debug
```

**Permission Control in CI:**
```yaml
claude_args: |
  --permission-mode acceptEdits
  --allowedTools "Bash(npm test),Read(*),Edit(*)"
  --disallowedTools "Bash(rm),Bash(curl)"
```

**Slash Commands in Workflows:**
```yaml
with:
  prompt: "/review"  # Uses pre-built prompts
  claude_args: "--max-turns 5"
```

## Claude Agent SDK

### Package Names (Post-Rename)

**TypeScript/JavaScript:**
```bash
npm uninstall @anthropic-ai/claude-code
npm install @anthropic-ai/claude-agent-sdk
```

**Python:**
```bash
pip uninstall claude-code-sdk
pip install claude-agent-sdk
```

**Import Changes:**
```typescript
// Old
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-code";

// New
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
```

### Critical SDK v0.1.0+ Breaking Changes

**1. System Prompt No Longer Default**

```typescript
// v0.0.x - Used Claude Code system prompt automatically
const result = query({ prompt: "Hello" });

// v0.1.0+ - Uses empty system prompt by default
// To get old behavior:
const result = query({
  prompt: "Hello",
  options: {
    systemPrompt: { type: "preset", preset: "claude_code" }
  }
});

// Or use custom:
const result = query({
  prompt: "Hello",
  options: {
    systemPrompt: "You are a helpful coding assistant"
  }
});
```

**2. Settings Sources Not Loaded by Default**

```typescript
// v0.0.x - Loaded all settings automatically
const result = query({ prompt: "Hello" });

// v0.1.0+ - No settings loaded by default
// To get old behavior:
const result = query({
  prompt: "Hello",
  options: {
    settingSources: ["user", "project", "local"]
  }
});

// Or load specific sources only:
const result = query({
  prompt: "Hello",
  options: {
    settingSources: ["project"]  // Only project settings
  }
});
```

**Why This Changed:**
- **CI/CD**: Consistent behavior without local customizations
- **Deployed apps**: No filesystem dependency
- **Testing**: Isolated test environments
- **Multi-tenant**: Prevents settings leakage between users

### SDK vs CLI Behavioral Differences

**CLI (`claude` command):**
- Loads system prompt automatically
- Reads CLAUDE.md, settings.json by default
- Filesystem-aware by design

**SDK (programmatic):**
- No default system prompt (v0.1.0+)
- No filesystem settings unless specified (v0.1.0+)
- Isolation by design for custom agents

**When This Matters:** Building automation or custom agents with the SDK behaves fundamentally different from CLI.

## Enterprise Deployment

### Amazon Bedrock Configuration

**Authentication Priority:**
```bash
# SSO with auto-refresh (recommended for enterprise)
export AWS_PROFILE=your-profile-name
```

**Auto-refresh in settings.json:**
```json
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

**Critical Settings:**
```bash
# Required - does NOT read from .aws config
export AWS_REGION=us-east-1

# Bedrock token limits
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096  # Bedrock's minimum penalty threshold
export MAX_THINKING_TOKENS=1024
```

**Why 4096:** Bedrock's burndown throttling sets minimum 4096-token penalty. Lower values don't reduce costs.

**IAM Policy (Minimal):**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream",
      "bedrock:ListInferenceProfiles"
    ],
    "Resource": [
      "arn:aws:bedrock:*:*:inference-profile/*",
      "arn:aws:bedrock:*:*:application-inference-profile/*"
    ]
  }]
}
```

**Model Configuration:**
```bash
# Use inference profiles to avoid region errors
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-5-20250929-v1:0'
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-3-5-haiku-20241022-v1:0'
```

### Google Vertex AI Configuration

**Authentication:**
```bash
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global  # or regional
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID
```

**Regional Override Strategy:**
```bash
# When using CLOUD_ML_REGION=global, override unsupported models
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
```

**IAM Role:** `roles/aiplatform.user`

**Note:** Model approval may take 24-48 hours. Verify in Model Garden before deploying.

### Enterprise Security & Compliance

**Managed Policy Settings Locations (Cannot be Overridden):**
- macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
- Linux/WSL: `/etc/claude-code/managed-settings.json`
- Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

**Example Managed Policy:**
```json
{
  "permissions": {
    "deny": [
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(rm -rf:*)",
      "Read(.env)",
      "Read(**/secrets/**)",
      "WebFetch"
    ],
    "defaultMode": "default"
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317"
  }
}
```

**Credential Management:**
- Storage: macOS Keychain (encrypted)
- `apiKeyHelper` - Refreshes every 5 min or on HTTP 401
- `awsAuthRefresh` - For SSO/browser-based flows
- `awsCredentialExport` - For direct credential JSON

### Monitoring & Observability (OpenTelemetry)

**Central Collector Setup:**
```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer company-token"
  }
}
```

**Dynamic Headers:**
```json
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

**Cardinality Control:**
```bash
export OTEL_METRICS_INCLUDE_SESSION_ID=false
export OTEL_METRICS_INCLUDE_ACCOUNT_UUID=false
```

**Multi-Team Tracking (W3C Baggage format - NO SPACES):**
```bash
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

**Key Metrics:**
- `claude_code.cost.usage` (USD) - Approximate
- `claude_code.token.usage` - By type: input/output/cacheRead/cacheCreation
- `claude_code.active_time.total` - Actual usage time (not idle)

**Key Events:**
- `claude_code.tool_result` - Tool execution with decision, source, parameters
- `claude_code.api_request` - Model calls with token/cost breakdown
- `claude_code.user_prompt` - Length by default, full content with `OTEL_LOG_USER_PROMPTS=1`

### Data Governance

**Training Policies by Account Type:**

**Consumer (Free/Pro/Max):**
- Opt-in model training (default: enabled as of Aug 28, 2025)
- 5-year retention if opted in, 30-day if opted out
- Change at `claude.ai/settings/privacy`

**Commercial (Team/Enterprise/API):**
- No training on your data
- 30-day retention (default)
- Zero data retention available

**Telemetry Services (Default Behavior by Provider):**

| Service | Claude API | Vertex | Bedrock |
|---------|-----------|--------|---------|
| Statsig (Metrics) | On | Off | Off |
| Sentry (Errors) | On | Off | Off |
| `/bug` reports | On | Off | Off |

**Disable All Non-Essential:**
```bash
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
```

## Troubleshooting and Operations

### Critical Installation Commands

**WSL-Specific Fix:**
```bash
npm config set os linux
npm install -g @anthropic-ai/claude-code --force --no-os-check
```

**Force Clean Authentication:**
```bash
rm -rf ~/.config/claude-code/auth.json
claude
```

### WSL Performance Issues

**Cross-Filesystem Search:**
- Projects on `/mnt/c/` (Windows filesystem) have degraded search performance
- **Solution:** Move projects to Linux filesystem (`/home/`) or use native Windows installation

**JetBrains IDE Detection on WSL2:**
- Create Windows Firewall rule (see JetBrains section above)
- Or switch to mirrored networking in `.wslconfig`

### Search and Discovery Issues

**If Search, @file mentions, custom agents, or slash commands fail:**
```bash
# Install system ripgrep
brew install ripgrep  # macOS
winget install BurntSushi.ripgrep.MSVC  # Windows
sudo apt install ripgrep  # Ubuntu/Debian

# Disable built-in ripgrep
USE_BUILTIN_RIPGREP=0
```

### Cost Management

**Team Rate Limit Recommendations (TPM/RPM per user):**

| Team Size | TPM per user | RPM per user |
|-----------|--------------|--------------|
| 1-5 | 200k-300k | 5-7 |
| 5-20 | 100k-150k | 2.5-3.5 |
| 20-50 | 50k-75k | 1.25-1.75 |
| 50-100 | 25k-35k | 0.62-0.87 |
| 100-500 | 15k-20k | 0.37-0.47 |
| 500+ | 10k-15k | 0.25-0.35 |

**Cost Reduction:**
```markdown
# Add to CLAUDE.md
When you are using compact, please focus on test output and code changes
```

**Cost Tracking:**
- Individual: `/cost` command (not for Pro/Max subscribers)
- Team-wide: [Claude Console](https://support.claude.com/en/articles/9534590-cost-and-usage-reporting-in-console) (Admin/Billing roles)
- "Claude Code" workspace auto-created (API key creation disabled)

**Bedrock/Vertex Cost Tracking:** Use [LiteLLM](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend) for spend tracking by key.

### Analytics (Console/API Users Only)

**Access:** [console.anthropic.com/claude-code](https://console.anthropic.com/claude-code)

**Required roles:** Primary Owner, Owner, Billing, Admin, Developer

**Key Metrics:**
- Lines of code accepted
- Suggestion accept rate
- Activity (users + sessions per day)
- Spend (users + dollars per day)
- Team insights (per-user spend and lines)
