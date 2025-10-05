url: https://docs.anthropic.com/en/docs/claude-code/overview

---

## Get started in 30 seconds

Prerequisites:

  * [Node.js 18 or newer](https://nodejs.org/en/download/)
  * A [Claude.ai](https://claude.ai) \(recommended\) or [Claude Console](https://console.anthropic.com/) account

Copy
[code]
    # Install Claude Code
    npm install -g @anthropic-ai/claude-code

    # Navigate to your project
    cd your-awesome-project

    # Start coding with Claude
    claude
    # You'll be prompted to log in on first use

[/code]

That’s it\! You’re ready to start coding with Claude. [Continue with Quickstart \(5 mins\) →](/en/docs/claude-code/quickstart) \(Got specific setup needs or hit issues? See [advanced setup](/en/docs/claude-code/setup) or [troubleshooting](/en/docs/claude-code/troubleshooting).\)

**New VS Code Extension \(Beta\)** : Prefer a graphical interface? Our new [VS Code extension](/en/docs/claude-code/vs-code) provides an easy-to-use native IDE experience without requiring terminal familiarity. Simply install from the marketplace and start coding with Claude directly in your sidebar.

## What Claude Code does for you

  * **Build features from descriptions** : Tell Claude what you want to build in plain English. It will make a plan, write the code, and ensure it works.
  * **Debug and fix issues** : Describe a bug or paste an error message. Claude Code will analyze your codebase, identify the problem, and implement a fix.
  * **Navigate any codebase** : Ask anything about your team’s codebase, and get a thoughtful answer back. Claude Code maintains awareness of your entire project structure, can find up-to-date information from the web, and with [MCP](/en/docs/claude-code/mcp) can pull from external datasources like Google Drive, Figma, and Slack.
  * **Automate tedious tasks** : Fix fiddly lint issues, resolve merge conflicts, and write release notes. Do all this in a single command from your developer machines, or automatically in CI.

## Why developers love Claude Code

  * **Works in your terminal** : Not another chat window. Not another IDE. Claude Code meets you where you already work, with the tools you already love.
  * **Takes action** : Claude Code can directly edit files, run commands, and create commits. Need more? [MCP](/en/docs/claude-code/mcp) lets Claude read your design docs in Google Drive, update your tickets in Jira, or use _your_ custom developer tooling.
  * **Unix philosophy** : Claude Code is composable and scriptable. `tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream"` _works_. Your CI can run `claude -p "If there are new text strings, translate them into French and raise a PR for @lang-fr-team to review"`.
  * **Enterprise-ready** : Use the Claude API, or host on AWS or GCP. Enterprise-grade [security](/en/docs/claude-code/security), [privacy](/en/docs/claude-code/data-usage), and [compliance](https://trust.anthropic.com/) is built-in.

## Next steps

## [QuickstartSee Claude Code in action with practical examples](/en/docs/claude-code/quickstart)## [Common workflowsStep-by-step guides for common workflows](/en/docs/claude-code/common-workflows)## [TroubleshootingSolutions for common issues with Claude Code](/en/docs/claude-code/troubleshooting)## [IDE setupAdd Claude Code to your IDE](/en/docs/claude-code/ide-integrations)

## Additional resources

## [Host on AWS or GCPConfigure Claude Code with Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/third-party-integrations)## [SettingsCustomize Claude Code for your workflow](/en/docs/claude-code/settings)## [CommandsLearn about CLI commands and controls](/en/docs/claude-code/cli-reference)## [Reference implementationClone our development container reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer)## [SecurityDiscover Claude Code’s safeguards and best practices for safe usage](/en/docs/claude-code/security)## [Privacy and data usageUnderstand how Claude Code handles your data](/en/docs/claude-code/data-usage)

Was this page helpful?

YesNo

[Quickstart](/en/docs/claude-code/quickstart)
