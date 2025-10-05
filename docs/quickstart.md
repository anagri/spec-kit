# Quick Start Guide

This guide will help you get started with Spec-Driven Development using Spec Kit (Claude Code edition).

> **Fork Note**: This is a Claude Code-only, bash-only fork optimized for solo developers on Unix-like systems (macOS/Linux).

## The 4-Step Process

### 1. Install Spec-Kit

Initialize your project:

```bash
uvx --from git+https://github.com/anagri/spec-kit.git speclaude init <PROJECT_NAME>
```

Or initialize in the current directory:

```bash
uvx --from git+https://github.com/anagri/spec-kit.git speclaude init .
```

### 2. Create the Spec

Use the `/specify` command in Claude Code to describe what you want to build. Focus on the **what** and **why**, not the tech stack.

```bash
/specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
```

### 3. Create a Technical Implementation Plan

Use the `/plan` command to provide your tech stack and architecture choices.

```bash
/plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

### 4. Break Down and Implement

Use `/tasks` to create an actionable task list, then ask Claude Code to implement the feature.

```bash
/tasks
```

Then:

```bash
/implement
```

## Example 1: Building a Web App (Taskify)

Here's a complete example of building a team productivity platform:

### Step 1: Define Requirements with `/specify`

```text
/specify Develop Taskify, a team productivity platform. It should allow users to create projects, add team members, assign tasks, comment and move tasks between boards in Kanban style. In this initial phase for this feature, let's call it "Create Taskify," let's have multiple users but the users will be declared ahead of time, predefined. I want five users in two different categories, one product manager and four engineers. Let's create three different sample projects. Let's have the standard Kanban columns for the status of each task, such as "To Do," "In Progress," "In Review," and "Done." There will be no login for this application as this is just the very first testing thing to ensure that our basic features are set up. For each task in the UI for a task card, you should be able to change the current status of the task between the different columns in the Kanban work board. You should be able to leave an unlimited number of comments for a particular card. You should be able to, from that task card, assign one of the valid users. When you first launch Taskify, it's going to give you a list of the five users to pick from. There will be no password required. When you click on a user, you go into the main view, which displays the list of projects. When you click on a project, you open the Kanban board for that project. You're going to see the columns. You'll be able to drag and drop cards back and forth between different columns. You will see any cards that are assigned to you, the currently logged in user, in a different color from all the other ones, so you can quickly see yours. You can edit any comments that you make, but you can't edit comments that other people made. You can delete any comments that you made, but you can't delete comments anybody else made.
```

### Step 2: Refine the Specification

After the initial specification is created, clarify any missing requirements:

```text
For each sample project or project that you create there should be a variable number of tasks between 5 and 15 tasks for each one randomly distributed into different states of completion. Make sure that there's at least one task in each stage of completion.
```

Also validate the specification checklist:

```text
Read the review and acceptance checklist, and check off each item in the checklist if the feature spec meets the criteria. Leave it empty if it does not.
```

### Step 3: Generate Technical Plan with `/plan`

Be specific about your tech stack and technical requirements:

```text
/plan We are going to generate this using .NET Aspire, using Postgres as the database. The frontend should use Blazor server with drag-and-drop task boards, real-time updates. There should be a REST API created with a projects API, tasks API, and a notifications API.
```

### Step 4: Validate and Implement

Have Claude Code audit the implementation plan:

```text
Now I want you to go and audit the implementation plan and the implementation detail files. Read through it with an eye on determining whether or not there is a sequence of tasks that you need to be doing that are obvious from reading this. Because I don't know if there's enough here.
```

Finally, implement the solution:

```text
/implement specs/002-create-taskify/
```

## Example 2: Building a CLI Tool

For CLI tools, template generators, or build tools, the workflow is similar but Phase 1 artifacts differ:

### Step 1: Define Requirements

```text
/specify Create a markdown linter CLI tool that checks markdown files for style violations. It should support custom rules defined in a .mdlint.json configuration file. The tool should output violations in a format compatible with CI/CD pipelines (exit code 1 if violations found). Rules should include: heading hierarchy, link validation, code block language specification, and line length limits.
```

### Step 2: Generate Technical Plan

```text
/plan Build with Python 3.11+, use Click for CLI framework, implement as a pip-installable package. Configuration uses JSON schema validation. Output formats: human-readable, JSON, and GitHub Actions format. Include --fix flag for auto-fixable violations.
```

**Note**: For CLI tools, `/plan` will generate `template-contracts.md` (defining config file formats, CLI arguments, output schemas) instead of `data-model.md` (which is for apps with database entities).

### Step 3: Implement

```text
/tasks
/implement
```

## Key Principles

- **Be explicit** about what you're building and why
- **Don't focus on tech stack** during specification phase
- **Iterate and refine** your specifications before implementation
- **Validate** the plan before coding begins
- **Let Claude Code handle** the implementation details
- **Consult docs/** folder during research phase (constitutional requirement)

## Understanding Feature Types

Spec-kit adapts to your project type:

| Project Type | Phase 1 Artifacts | Examples |
|--------------|-------------------|----------|
| **Web/Mobile Apps** | data-model.md, API contracts | Taskify, photo albums, e-commerce |
| **CLI/Template Tools** | template-contracts.md, file structure contracts | spec-kit itself, linters, generators |

## Next Steps

- Read the complete methodology in `docs/PHILOSOPHY.md` for in-depth architectural guidance
- Check out the `specs/` directory for examples from dogfooding spec-kit development
- Review the constitution at `.specify/memory/constitution.md` in your initialized project
