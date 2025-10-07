#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh
# Build Spec Kit template release archive for Claude Code with bash scripts.
# Simplified version - templates are pre-processed, just copy as-is.
# Usage: .github/workflows/scripts/create-release-packages.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-with-v-prefix>" >&2
  exit 1
fi

NEW_VERSION="$1"
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must look like v0.0.0" >&2
  exit 1
fi

echo "Building release package for $NEW_VERSION (Claude Code + bash)"

# Create build directory
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "$GENRELEASES_DIR"/* || true

BASE_DIR="$GENRELEASES_DIR/sdd-claude-package-sh"
SPEC_DIR="$BASE_DIR/.specify"
CLAUDE_DIR="$BASE_DIR/.claude"

# Create directory structure
mkdir -p "$SPEC_DIR/templates"
mkdir -p "$SPEC_DIR/scripts"
mkdir -p "$SPEC_DIR/memory"
mkdir -p "$CLAUDE_DIR/commands"

echo "Copying pre-processed templates..."

# Copy memory files
if [[ -d memory ]]; then
  cp -r memory "$SPEC_DIR/"
  echo "  ✓ Copied memory/ → .specify/memory/"
fi

# Copy bash scripts
if [[ -d scripts/bash ]]; then
  cp -r scripts/bash "$SPEC_DIR/scripts/"
  echo "  ✓ Copied scripts/bash/ → .specify/scripts/bash/"
fi

# Copy template files (excluding commands directory)
if [[ -d templates ]]; then
  # Copy all .md files from templates/ root (not commands/)
  find templates -maxdepth 1 -type f -name "*.md" -exec cp {} "$SPEC_DIR/templates/" \;
  echo "  ✓ Copied templates/*.md → .specify/templates/"
fi

# Copy command files (already pre-processed)
if [[ -d templates/commands ]]; then
  cp templates/commands/*.md "$CLAUDE_DIR/commands/" 2>/dev/null || true
  echo "  ✓ Copied templates/commands/*.md → .claude/commands/"
fi

# Create zip archive
cd "$BASE_DIR" && zip -q -r "../spec-kit-template-claude-sh-${NEW_VERSION}.zip" .
cd - > /dev/null

echo ""
echo "✅ Created $GENRELEASES_DIR/spec-kit-template-claude-sh-${NEW_VERSION}.zip"
echo ""

# Show archive contents for verification
echo "Archive contents:"
unzip -l "$GENRELEASES_DIR/spec-kit-template-claude-sh-${NEW_VERSION}.zip" | tail -n +4 | head -n -2
