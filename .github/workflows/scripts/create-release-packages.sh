#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh (workflow-local)
# Build Spec Kit template release archive for Claude Code with bash scripts.
# Usage: .github/workflows/scripts/create-release-packages.sh <version>
#   Version argument should include leading 'v'.

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-with-v-prefix>" >&2
  exit 1
fi
NEW_VERSION="$1"
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must look like v0.0.0" >&2
  exit 1
fi

echo "Building release packages for $NEW_VERSION"

# Create and use .genreleases directory for all build artifacts
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "$GENRELEASES_DIR"/* || true

rewrite_paths() {
  sed -E \
    -e 's@(/?)memory/@.specify/memory/@g' \
    -e 's@(/?)scripts/@.specify/scripts/@g' \
    -e 's@(/?)templates/@.specify/templates/@g'
}

generate_commands() {
  local agent=$1 ext=$2 arg_format=$3 output_dir=$4 script_variant=$5
  mkdir -p "$output_dir"
  for template in templates/commands/*.md; do
    [[ -f "$template" ]] || continue
    local name description script_command body
    name=$(basename "$template" .md)
    
    # Normalize line endings
    file_content=$(tr -d '\r' < "$template")
    
    # Extract description and script command from YAML frontmatter
    description=$(printf '%s\n' "$file_content" | awk '/^description:/ {sub(/^description:[[:space:]]*/, ""); print; exit}')
    script_command=$(printf '%s\n' "$file_content" | awk -v sv="$script_variant" '/^[[:space:]]*'"$script_variant"':[[:space:]]*/ {sub(/^[[:space:]]*'"$script_variant"':[[:space:]]*/, ""); print; exit}')
    
    if [[ -z $script_command ]]; then
      echo "Warning: no script command found for $script_variant in $template" >&2
      script_command="(Missing script command for $script_variant)"
    fi
    
    # Replace {SCRIPT} placeholder with the script command
    body=$(printf '%s\n' "$file_content" | sed "s|{SCRIPT}|${script_command}|g")
    
    # Remove the scripts: section from frontmatter while preserving YAML structure
    body=$(printf '%s\n' "$body" | awk '
      /^---$/ { print; if (++dash_count == 1) in_frontmatter=1; else in_frontmatter=0; next }
      in_frontmatter && /^scripts:$/ { skip_scripts=1; next }
      in_frontmatter && /^[a-zA-Z].*:/ && skip_scripts { skip_scripts=0 }
      in_frontmatter && skip_scripts && /^[[:space:]]/ { next }
      { print }
    ')
    
    # Apply other substitutions
    body=$(printf '%s\n' "$body" | sed "s/{ARGS}/$arg_format/g" | sed "s/__AGENT__/$agent/g" | rewrite_paths)
    
    case $ext in
      toml)
        { echo "description = \"$description\""; echo; echo "prompt = \"\"\""; echo "$body"; echo "\"\"\""; } > "$output_dir/$name.$ext" ;;
      md)
        echo "$body" > "$output_dir/$name.$ext" ;;
      prompt.md)
        echo "$body" > "$output_dir/$name.$ext" ;;
    esac
  done
}

build_variant() {
  local base_dir="$GENRELEASES_DIR/sdd-claude-package-sh"
  echo "Building Claude Code (bash) package..."
  mkdir -p "$base_dir"
  
  # Copy base structure but filter scripts by variant
  SPEC_DIR="$base_dir/.specify"
  mkdir -p "$SPEC_DIR"
  
  [[ -d memory ]] && { cp -r memory "$SPEC_DIR/"; echo "Copied memory -> .specify"; }
  
  # Copy bash scripts
  if [[ -d scripts/bash ]]; then
    mkdir -p "$SPEC_DIR/scripts"
    cp -r scripts/bash "$SPEC_DIR/scripts/"
    echo "Copied scripts/bash -> .specify/scripts"
    # Copy any script files that aren't in variant-specific directories
    find scripts -maxdepth 1 -type f -exec cp {} "$SPEC_DIR/scripts/" \; 2>/dev/null || true
  fi
  
  # Copy templates (excluding commands directory - those are generated)
  if [[ -d templates ]]; then
    mkdir -p "$SPEC_DIR/templates"
    # Copy all template files while preserving directory structure
    (cd templates && find . -type f -not -path "./commands/*" | while read -r file; do
      mkdir -p "$SPEC_DIR/templates/$(dirname "$file")"
      cp "$file" "$SPEC_DIR/templates/$file"
    done)
    echo "Copied templates -> .specify/templates"
  fi

  # Inject script command into plan-template.md within .specify/templates if present
  local plan_tpl="$base_dir/.specify/templates/plan-template.md"
  if [[ -f "$plan_tpl" ]]; then
    plan_norm=$(tr -d '\r' < "$plan_tpl")
    # Extract script command from YAML frontmatter (sh only)
    script_command=$(printf '%s\n' "$plan_norm" | awk '/^[[:space:]]*sh:[[:space:]]*/ {sub(/^[[:space:]]*sh:[[:space:]]*/, ""); print; exit}')
    if [[ -n $script_command ]]; then
      # Always prefix with .specify/ for plan usage
      script_command=".specify/$script_command"
      # Replace {SCRIPT} placeholder with the script command and __AGENT__ with claude
      substituted=$(sed "s|{SCRIPT}|${script_command}|g" "$plan_tpl" | tr -d '\r' | sed "s|__AGENT__|claude|g")
      # Strip YAML frontmatter from plan template output (keep body only)
      stripped=$(printf '%s\n' "$substituted" | awk 'BEGIN{fm=0;dash=0} /^---$/ {dash++; if(dash==1){fm=1; next} else if(dash==2){fm=0; next}} {if(!fm) print}')
      printf '%s\n' "$stripped" > "$plan_tpl"
    else
      echo "Warning: no plan-template script command found for sh in YAML frontmatter" >&2
    fi
  fi

  # Generate Claude Code commands
  mkdir -p "$base_dir/.claude/commands"
  generate_commands claude md "\$ARGUMENTS" "$base_dir/.claude/commands" "sh"
  ( cd "$base_dir" && zip -r "../spec-kit-template-claude-sh-${NEW_VERSION}.zip" . )
  echo "Created $GENRELEASES_DIR/spec-kit-template-claude-sh-${NEW_VERSION}.zip"
}

# Build Claude Code with bash scripts package
build_variant

echo "Archives in $GENRELEASES_DIR:"
ls -1 "$GENRELEASES_DIR"/spec-kit-template-*-"${NEW_VERSION}".zip
