url: https://docs.anthropic.com/en/docs/claude-code/common-workflows

---

Each task in this document includes clear instructions, example commands, and best practices to help you get the most from Claude Code.

## Understand new codebases

### Get a quick codebase overview

Suppose you’ve just joined a new project and need to understand its structure quickly.

1

Navigate to the project root directory

Copy
[code]
    cd /path/to/project

[/code]

2

Start Claude Code

Copy
[code]
    claude

[/code]

3

Ask for a high-level overview

Copy
[code]
    > give me an overview of this codebase

[/code]

4

Dive deeper into specific components

Copy
[code]
    > explain the main architecture patterns used here

[/code]

Copy
[code]
    > what are the key data models?

[/code]

Copy
[code]
    > how is authentication handled?

[/code]

Tips:

  * Start with broad questions, then narrow down to specific areas
  * Ask about coding conventions and patterns used in the project
  * Request a glossary of project-specific terms

### Find relevant code

Suppose you need to locate code related to a specific feature or functionality.

1

Ask Claude to find relevant files

Copy
[code]
    > find the files that handle user authentication

[/code]

2

Get context on how components interact

Copy
[code]
    > how do these authentication files work together?

[/code]

3

Understand the execution flow

Copy
[code]
    > trace the login process from front-end to database

[/code]

Tips:

  * Be specific about what you’re looking for
  * Use domain language from the project

* * *

## Fix bugs efficiently

Suppose you’ve encountered an error message and need to find and fix its source.

1

Share the error with Claude

Copy
[code]
    > I'm seeing an error when I run npm test

[/code]

2

Ask for fix recommendations

Copy
[code]
    > suggest a few ways to fix the @ts-ignore in user.ts

[/code]

3

Apply the fix

Copy
[code]
    > update user.ts to add the null check you suggested

[/code]

Tips:

  * Tell Claude the command to reproduce the issue and get a stack trace
  * Mention any steps to reproduce the error
  * Let Claude know if the error is intermittent or consistent

* * *

## Refactor code

Suppose you need to update old code to use modern patterns and practices.

1

Identify legacy code for refactoring

Copy
[code]
    > find deprecated API usage in our codebase

[/code]

2

Get refactoring recommendations

Copy
[code]
    > suggest how to refactor utils.js to use modern JavaScript features

[/code]

3

Apply the changes safely

Copy
[code]
    > refactor utils.js to use ES2024 features while maintaining the same behavior

[/code]

4

Verify the refactoring

Copy
[code]
    > run tests for the refactored code

[/code]

Tips:

  * Ask Claude to explain the benefits of the modern approach
  * Request that changes maintain backward compatibility when needed
  * Do refactoring in small, testable increments

* * *

## Use specialized subagents

Suppose you want to use specialized AI subagents to handle specific tasks more effectively.

1

View available subagents

Copy
[code]
    > /agents

[/code]

This shows all available subagents and lets you create new ones.

2

Use subagents automatically

Claude Code will automatically delegate appropriate tasks to specialized subagents:

Copy
[code]
    > review my recent code changes for security issues

[/code]

Copy
[code]
    > run all tests and fix any failures

[/code]

3

Explicitly request specific subagents

Copy
[code]
    > use the code-reviewer subagent to check the auth module

[/code]

Copy
[code]
    > have the debugger subagent investigate why users can't log in

[/code]

4

Create custom subagents for your workflow

Copy
[code]
    > /agents

[/code]

Then select “Create New subagent” and follow the prompts to define:

  * Subagent type \(e.g., `api-designer`, `performance-optimizer`\)
  * When to use it
  * Which tools it can access
  * Its specialized system prompt

Tips:

  * Create project-specific subagents in `.claude/agents/` for team sharing
  * Use descriptive `description` fields to enable automatic delegation
  * Limit tool access to what each subagent actually needs
  * Check the [subagents documentation](/en/docs/claude-code/sub-agents) for detailed examples

* * *

## Use Plan Mode for safe code analysis

Plan Mode instructs Claude to create a plan by analyzing the codebase with read-only operations, perfect for exploring codebases, planning complex changes, or reviewing code safely.

### When to use Plan Mode

  * **Multi-step implementation** : When your feature requires making edits to many files
  * **Code exploration** : When you want to research the codebase thoroughly before changing anything
  * **Interactive development** : When you want to iterate on the direction with Claude

### How to use Plan Mode

**Turn on Plan Mode during a session** You can switch into Plan Mode during a session using **Shift+Tab** to cycle through permission modes. If you are in Normal Mode, **Shift+Tab** will first switch into Auto-Accept Mode, indicated by `⏵⏵ accept edits on` at the bottom of the terminal. A subsequent **Shift+Tab** will switch into Plan Mode, indicated by `⏸ plan mode on`. **Start a new session in Plan Mode** To start a new session in Plan Mode, use the `--permission-mode plan` flag:

Copy
[code]
    claude --permission-mode plan

[/code]

**Run “headless” queries in Plan Mode** You can also run a query in Plan Mode directly with `-p` \(i.e., in [“headless mode”](/en/docs/claude-code/sdk/sdk-headless)\):

Copy
[code]
    claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"

[/code]

### Example: Planning a complex refactor

Copy
[code]
    claude --permission-mode plan

[/code]

Copy
[code]
    > I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.

[/code]

Claude will analyze the current implementation and create a comprehensive plan. Refine with follow-ups:

Copy
[code]
    > What about backward compatibility?
    > How should we handle database migration?

[/code]

### Configure Plan Mode as default

Copy
[code]
    // .claude/settings.json
    {
      "permissions": {
        "defaultMode": "plan"
      }
    }

[/code]

See [settings documentation](/en/docs/claude-code/settings#available-settings) for more configuration options.

* * *

## Work with tests

Suppose you need to add tests for uncovered code.

1

Identify untested code

Copy
[code]
    > find functions in NotificationsService.swift that are not covered by tests

[/code]

2

Generate test scaffolding

Copy
[code]
    > add tests for the notification service

[/code]

3

Add meaningful test cases

Copy
[code]
    > add test cases for edge conditions in the notification service

[/code]

4

Run and verify tests

Copy
[code]
    > run the new tests and fix any failures

[/code]

Tips:

  * Ask for tests that cover edge cases and error conditions
  * Request both unit and integration tests when appropriate
  * Have Claude explain the testing strategy

* * *

## Create pull requests

Suppose you need to create a well-documented pull request for your changes.

1

Summarize your changes

Copy
[code]
    > summarize the changes I've made to the authentication module

[/code]

2

Generate a PR with Claude

Copy
[code]
    > create a pr

[/code]

3

Review and refine

Copy
[code]
    > enhance the PR description with more context about the security improvements

[/code]

4

Add testing details

Copy
[code]
    > add information about how these changes were tested

[/code]

Tips:

  * Ask Claude directly to make a PR for you
  * Review Claude’s generated PR before submitting
  * Ask Claude to highlight potential risks or considerations

## Handle documentation

Suppose you need to add or update documentation for your code.

1

Identify undocumented code

Copy
[code]
    > find functions without proper JSDoc comments in the auth module

[/code]

2

Generate documentation

Copy
[code]
    > add JSDoc comments to the undocumented functions in auth.js

[/code]

3

Review and enhance

Copy
[code]
    > improve the generated documentation with more context and examples

[/code]

4

Verify documentation

Copy
[code]
    > check if the documentation follows our project standards

[/code]

Tips:

  * Specify the documentation style you want \(JSDoc, docstrings, etc.\)
  * Ask for examples in the documentation
  * Request documentation for public APIs, interfaces, and complex logic

* * *

## Work with images

Suppose you need to work with images in your codebase, and you want Claude’s help analyzing image content.

1

Add an image to the conversation

You can use any of these methods:

  1. Drag and drop an image into the Claude Code window
  2. Copy an image and paste it into the CLI with ctrl+v \(Do not use cmd+v\)
  3. Provide an image path to Claude. E.g., “Analyze this image: /path/to/your/image.png”

2

Ask Claude to analyze the image

Copy
[code]
    > What does this image show?

[/code]

Copy
[code]
    > Describe the UI elements in this screenshot

[/code]

Copy
[code]
    > Are there any problematic elements in this diagram?

[/code]

3

Use images for context

Copy
[code]
    > Here's a screenshot of the error. What's causing it?

[/code]

Copy
[code]
    > This is our current database schema. How should we modify it for the new feature?

[/code]

4

Get code suggestions from visual content

Copy
[code]
    > Generate CSS to match this design mockup

[/code]

Copy
[code]
    > What HTML structure would recreate this component?

[/code]

Tips:

  * Use images when text descriptions would be unclear or cumbersome
  * Include screenshots of errors, UI designs, or diagrams for better context
  * You can work with multiple images in a conversation
  * Image analysis works with diagrams, screenshots, mockups, and more

* * *

## Reference files and directories

Use @ to quickly include files or directories without waiting for Claude to read them.

1

Reference a single file

Copy
[code]
    > Explain the logic in @src/utils/auth.js

[/code]

This includes the full content of the file in the conversation.

2

Reference a directory

Copy
[code]
    > What's the structure of @src/components?

[/code]

This provides a directory listing with file information.

3

Reference MCP resources

Copy
[code]
    > Show me the data from @github:repos/owner/repo/issues

[/code]

This fetches data from connected MCP servers using the format @server:resource. See [MCP resources](/en/docs/claude-code/mcp#use-mcp-resources) for details.

Tips:

  * File paths can be relative or absolute
  * @ file references add CLAUDE.md in the file’s directory and parent directories to context
  * Directory references show file listings, not contents
  * You can reference multiple files in a single message \(e.g., “@file1.js and @file2.js”\)

* * *

## Use extended thinking

Suppose you’re working on complex architectural decisions, challenging bugs, or planning multi-step implementations that require deep reasoning.

[Extended thinking](/en/docs/build-with-claude/extended-thinking) is disabled by default in Claude Code. You can enable it on-demand by using `Tab` to toggle Thinking on, or by using prompts like “think” or “think hard”. You can also enable it permanently by setting the [`MAX_THINKING_TOKENS` environment variable](/en/docs/claude-code/settings#environment-variables) in your settings.

1

Provide context and ask Claude to think

Copy
[code]
    > I need to implement a new authentication system using OAuth2 for our API. Think deeply about the best approach for implementing this in our codebase.

[/code]

Claude will gather relevant information from your codebase and use extended thinking, which will be visible in the interface.

2

Refine the thinking with follow-up prompts

Copy
[code]
    > think about potential security vulnerabilities in this approach

[/code]

Copy
[code]
    > think hard about edge cases we should handle

[/code]

Tips to get the most value out of extended thinking:[Extended thinking](/en/docs/build-with-claude/extended-thinking) is most valuable for complex tasks such as:

  * Planning complex architectural changes
  * Debugging intricate issues
  * Creating implementation plans for new features
  * Understanding complex codebases
  * Evaluating tradeoffs between different approaches

Use `Tab` to toggle Thinking on and off during a session.The way you prompt for thinking results in varying levels of thinking depth:

  * “think” triggers basic extended thinking
  * intensifying phrases such as “keep hard”, “think more”, “think a lot”, or “think longer” triggers deeper thinking

For more extended thinking prompting tips, see [Extended thinking tips](/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips).

Claude will display its thinking process as italic gray text above the response.

* * *

## Resume previous conversations

Suppose you’ve been working on a task with Claude Code and need to continue where you left off in a later session. Claude Code provides two options for resuming previous conversations:

  * `--continue` to automatically continue the most recent conversation
  * `--resume` to display a conversation picker

1

Continue the most recent conversation

Copy
[code]
    claude --continue

[/code]

This immediately resumes your most recent conversation without any prompts.

2

Continue in non-interactive mode

Copy
[code]
    claude --continue --print "Continue with my task"

[/code]

Use `--print` with `--continue` to resume the most recent conversation in non-interactive mode, perfect for scripts or automation.

3

Show conversation picker

Copy
[code]
    claude --resume

[/code]

This displays an interactive conversation selector with a clean list view showing:

  * Session summary \(or initial prompt\)
  * Metadata: time elapsed, message count, and git branch

Use arrow keys to navigate and press Enter to select a conversation. Press Esc to exit.

Tips:

  * Conversation history is stored locally on your machine
  * Use `--continue` for quick access to your most recent conversation
  * Use `--resume` when you need to select a specific past conversation
  * When resuming, you’ll see the entire conversation history before continuing
  * The resumed conversation starts with the same model and configuration as the original

How it works:

  1. **Conversation Storage** : All conversations are automatically saved locally with their full message history
  2. **Message Deserialization** : When resuming, the entire message history is restored to maintain context
  3. **Tool State** : Tool usage and results from the previous conversation are preserved
  4. **Context Restoration** : The conversation resumes with all previous context intact

Examples:

Copy
[code]
    # Continue most recent conversation
    claude --continue

    # Continue most recent conversation with a specific prompt
    claude --continue --print "Show me our progress"

    # Show conversation picker
    claude --resume

    # Continue most recent conversation in non-interactive mode
    claude --continue --print "Run the tests again"

[/code]

* * *

## Run parallel Claude Code sessions with Git worktrees

Suppose you need to work on multiple tasks simultaneously with complete code isolation between Claude Code instances.

1

Understand Git worktrees

Git worktrees allow you to check out multiple branches from the same repository into separate directories. Each worktree has its own working directory with isolated files, while sharing the same Git history. Learn more in the [official Git worktree documentation](https://git-scm.com/docs/git-worktree).

2

Create a new worktree

Copy
[code]
    # Create a new worktree with a new branch
    git worktree add ../project-feature-a -b feature-a

    # Or create a worktree with an existing branch
    git worktree add ../project-bugfix bugfix-123

[/code]

This creates a new directory with a separate working copy of your repository.

3

Run Claude Code in each worktree

Copy
[code]
    # Navigate to your worktree
    cd ../project-feature-a

    # Run Claude Code in this isolated environment
    claude

[/code]

4

Run Claude in another worktree

Copy
[code]
    cd ../project-bugfix
    claude

[/code]

5

Manage your worktrees

Copy
[code]
    # List all worktrees
    git worktree list

    # Remove a worktree when done
    git worktree remove ../project-feature-a

[/code]

Tips:

  * Each worktree has its own independent file state, making it perfect for parallel Claude Code sessions
  * Changes made in one worktree won’t affect others, preventing Claude instances from interfering with each other
  * All worktrees share the same Git history and remote connections
  * For long-running tasks, you can have Claude working in one worktree while you continue development in another
  * Use descriptive directory names to easily identify which task each worktree is for
  * Remember to initialize your development environment in each new worktree according to your project’s setup. Depending on your stack, this might include:
    * JavaScript projects: Running dependency installation \(`npm install`, `yarn`\)
    * Python projects: Setting up virtual environments or installing with package managers
    * Other languages: Following your project’s standard setup process

* * *

## Use Claude as a unix-style utility

### Add Claude to your verification process

Suppose you want to use Claude Code as a linter or code reviewer. **Add Claude to your build script:**

Copy
[code]
    // package.json
    {
        ...
        "scripts": {
            ...
            "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
        }
    }

[/code]

Tips:

  * Use Claude for automated code review in your CI/CD pipeline
  * Customize the prompt to check for specific issues relevant to your project
  * Consider creating multiple scripts for different types of verification

### Pipe in, pipe out

Suppose you want to pipe data into Claude, and get back data in a structured format. **Pipe data through Claude:**

Copy
[code]
    cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt

[/code]

Tips:

  * Use pipes to integrate Claude into existing shell scripts
  * Combine with other Unix tools for powerful workflows
  * Consider using —output-format for structured output

### Control output format

Suppose you need Claude’s output in a specific format, especially when integrating Claude Code into scripts or other tools.

1

Use text format \(default\)

Copy
[code]
    cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt

[/code]

This outputs just Claude’s plain text response \(default behavior\).

2

Use JSON format

Copy
[code]
    cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json

[/code]

This outputs a JSON array of messages with metadata including cost and duration.

3

Use streaming JSON format

Copy
[code]
    cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json

[/code]

This outputs a series of JSON objects in real-time as Claude processes the request. Each message is a valid JSON object, but the entire output is not valid JSON if concatenated.

Tips:

  * Use `--output-format text` for simple integrations where you just need Claude’s response
  * Use `--output-format json` when you need the full conversation log
  * Use `--output-format stream-json` for real-time output of each conversation turn

* * *

## Create custom slash commands

Claude Code supports custom slash commands that you can create to quickly execute specific prompts or tasks. For more details, see the [Slash commands](/en/docs/claude-code/slash-commands) reference page.

### Create project-specific commands

Suppose you want to create reusable slash commands for your project that all team members can use.

1

Create a commands directory in your project

Copy
[code]
    mkdir -p .claude/commands

[/code]

2

Create a Markdown file for each command

Copy
[code]
    echo "Analyze the performance of this code and suggest three specific optimizations:" > .claude/commands/optimize.md

[/code]

3

Use your custom command in Claude Code

Copy
[code]
    > /optimize

[/code]

Tips:

  * Command names are derived from the filename \(e.g., `optimize.md` becomes `/optimize`\)
  * You can organize commands in subdirectories \(e.g., `.claude/commands/frontend/component.md` creates `/component` with “\(project:frontend\)” shown in the description\)
  * Project commands are available to everyone who clones the repository
  * The Markdown file content becomes the prompt sent to Claude when the command is invoked

### Add command arguments with $ARGUMENTS

Suppose you want to create flexible slash commands that can accept additional input from users.

1

Create a command file with the $ARGUMENTS placeholder

Copy
[code]
    echo 'Find and fix issue #$ARGUMENTS. Follow these steps: 1.
    Understand the issue described in the ticket 2. Locate the relevant code in
    our codebase 3. Implement a solution that addresses the root cause 4. Add
    appropriate tests 5. Prepare a concise PR description' >
    .claude/commands/fix-issue.md

[/code]

2

Use the command with an issue number

In your Claude session, use the command with arguments.

Copy
[code]
    > /fix-issue 123

[/code]

This will replace $ARGUMENTS with “123” in the prompt.

Tips:

  * The $ARGUMENTS placeholder is replaced with any text that follows the command
  * You can position $ARGUMENTS anywhere in your command template
  * Other useful applications: generating test cases for specific functions, creating documentation for components, reviewing code in particular files, or translating content to specified languages

### Create personal slash commands

Suppose you want to create personal slash commands that work across all your projects.

1

Create a commands directory in your home folder

Copy
[code]
    mkdir -p ~/.claude/commands

[/code]

2

Create a Markdown file for each command

Copy
[code]
    echo "Review this code for security vulnerabilities, focusing on:" >
    ~/.claude/commands/security-review.md

[/code]

3

Use your personal custom command

Copy
[code]
    > /security-review

[/code]

Tips:

  * Personal commands show “\(user\)” in their description when listed with `/help`
  * Personal commands are only available to you and not shared with your team
  * Personal commands work across all your projects
  * You can use these for consistent workflows across different codebases

* * *

## Ask Claude about its capabilities

Claude has built-in access to its documentation and can answer questions about its own features and limitations.

### Example questions

Copy
[code]
    > can Claude Code create pull requests?

[/code]

Copy
[code]
    > how does Claude Code handle permissions?

[/code]

Copy
[code]
    > what slash commands are available?

[/code]

Copy
[code]
    > how do I use MCP with Claude Code?

[/code]

Copy
[code]
    > how do I configure Claude Code for Amazon Bedrock?

[/code]

Copy
[code]
    > what are the limitations of Claude Code?

[/code]

Claude provides documentation-based answers to these questions. For executable examples and hands-on demonstrations, refer to the specific workflow sections above.

Tips:

  * Claude always has access to the latest Claude Code documentation, regardless of the version you’re using
  * Ask specific questions to get detailed answers
  * Claude can explain complex features like MCP integration, enterprise configurations, and advanced workflows

* * *

## Next steps

## [Claude Code reference implementationClone our development container reference implementation.](https://github.com/anthropics/claude-code/tree/main/.devcontainer)

Was this page helpful?

YesNo

[Quickstart](/en/docs/claude-code/quickstart)[Subagents](/en/docs/claude-code/sub-agents)
