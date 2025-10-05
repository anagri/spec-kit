# Spec Kit (Claude Code Edition)

*Build high-quality software faster.*

**A solo-developer-optimized fork enabling focus on product scenarios rather than undifferentiated code through Spec-Driven Development with Claude Code.**

> **Fork Note**: This is `anagri/spec-kit` - a Claude Code-only, bash-only fork of `github/spec-kit` optimized for solo developers on Unix-like systems. See [Philosophy](PHILOSOPHY.md) for rationale.

## What is Spec-Driven Development?

Spec-Driven Development **flips the script** on traditional software development. For decades, code has been king — specifications were just scaffolding we built and discarded once the "real work" of coding began. Spec-Driven Development changes this: **specifications become executable**, directly generating working implementations rather than just guiding them.

## Getting Started

- [Installation Guide](installation.md)
- [Quick Start Guide](quickstart.md)
- [Local Development](local-development.md)

## Core Philosophy

Spec-Driven Development is a structured process that emphasizes:

- **Intent-driven development** where specifications define the "_what_" before the "_how_"
- **Rich specification creation** using guardrails and organizational principles
- **Multi-step refinement** rather than one-shot code generation from prompts
- **Heavy reliance** on advanced AI model capabilities for specification interpretation

## Development Phases

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **0-to-1 Development** ("Greenfield") | Generate from scratch | <ul><li>Start with high-level requirements</li><li>Generate specifications</li><li>Plan implementation steps</li><li>Build production-ready applications</li></ul> |
| **Creative Exploration** | Parallel implementations | <ul><li>Explore diverse solutions</li><li>Support multiple technology stacks & architectures</li><li>Experiment with UX patterns</li></ul> |
| **Iterative Enhancement** ("Brownfield") | Brownfield modernization | <ul><li>Add features iteratively</li><li>Modernize legacy systems</li><li>Adapt processes</li></ul> |

## Goals & Philosophy

This fork focuses on:

### Simplicity Through Constraint
- **Claude Code-only**: Eliminate multi-agent complexity, optimize for one AI assistant
- **Bash-only**: No PowerShell dual implementation burden
- **Solo developer workflow**: No mandatory git branch creation, work directly on main
- **Unix-focused**: macOS and Linux (Windows users can use WSL/Git Bash)

See [PHILOSOPHY.md](PHILOSOPHY.md) for detailed architectural rationale.

### Technology Independence
- Create applications using diverse technology stacks
- Validate that Spec-Driven Development is a process not tied to specific technologies, programming languages, or frameworks

### Project Type Flexibility
- **Web/Mobile Apps**: Generate data models and API contracts
- **CLI/Template Tools**: Generate template structures and file contracts
- Adapt artifacts to feature type (not one-size-fits-all)

### Creative & Iterative Processes
- Validate the concept of iterative feature development
- Provide robust workflows for adding features and modernizing code
- Support both greenfield and brownfield development

## Contributing

Please see our [Contributing Guide](https://github.com/anagri/spec-kit/blob/main/CONTRIBUTING.md) for information on how to contribute to this project.

## Support

For support, please check our [Support Guide](https://github.com/anagri/spec-kit/blob/main/SUPPORT.md) or open an issue on GitHub.
