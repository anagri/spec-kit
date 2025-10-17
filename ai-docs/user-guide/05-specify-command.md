# Page 05: /specify - Feature Specification

**Command**: `/specify "natural language feature description"`
**Phase**: Requirements Definition (after `/constitution`, before `/plan`)
**Purpose**: Transform natural language feature descriptions into structured, testable specifications
**Duration**: 2-5 minutes execution, creates foundation for all downstream artifacts

---

## What This Command Does

The `/specify` command is the first step in feature development after establishing your project constitution. It takes a 1-3 sentence natural language description of what users need and generates a structured specification document with:

- User scenarios and acceptance criteria
- Functional requirements (FR-001, FR-002, etc.)
- Key entities and their attributes
- [NEEDS CLARIFICATION] markers for ambiguities

This specification becomes the **source of truth** for all subsequent design and implementation work.

---

## When to Use

**Use `/specify` when**:
- Starting a new feature from scratch
- You have a clear understanding of WHAT users need (even if details are fuzzy)
- After `/constitution` has established project governance principles

**Don't use `/specify` for**:
- Updating existing specifications (manually edit the spec.md file instead)
- Technical design decisions (that's `/plan`'s job)
- Task breakdowns (that's `/tasks`'s job)

---

## Input Requirements

### The Feature Description

Your input should be **1-3 sentences** focusing on:

1. **WHAT** users need (not HOW to implement)
2. **WHY** it matters (user goals, business value)
3. **WHO** uses it (actors, user types)

**Good Examples**:
```
/specify "Real-time chat system with message history supporting 10k concurrent users"

/specify "User authentication via OAuth2 with session management and role-based permissions"

/specify "File upload system that processes images, generates thumbnails, and stores in S3"
```

**Bad Examples** (too much technical detail):
```
/specify "WebSocket-based chat using Redis Pub/Sub with PostgreSQL persistence"
↑ Includes implementation details (WebSocket, Redis, PostgreSQL)

/specify "Use FastAPI to create REST endpoints for user CRUD operations"
↑ Specifies framework and implementation approach
```

**Bad Examples** (too vague):
```
/specify "Chat feature"
↑ Missing scale, user goals, key capabilities

/specify "Fast and secure authentication"
↑ Vague adjectives without measurable criteria
```

---

## What Happens Behind the Scenes

### Step 1: Script Execution

Claude runs the bash script to create the feature directory:

```bash
.specify/scripts/bash/create-new-feature.sh --json "Real-time chat with message history"
```

**Script Output** (JSON format):
```json
{
  "FEATURE_ID": "001-real-time-chat",
  "SPEC_FILE": "/absolute/path/to/specs/001-real-time-chat/spec.md",
  "FEATURE_NUM": "001"
}
```

**What the script does**:
- Scans `specs/` directory for existing features (000-\*, 001-\*, 002-\*, etc.)
- Calculates next sequential ID (if highest is 002, next is 003)
- Creates feature directory: `specs/###-feature-name/`
- Copies `spec-template.md` to `spec.md` in the new directory
- Sets `SPECIFY_FEATURE` environment variable for subsequent commands

### Step 2: Template Processing

Claude loads `.specify/templates/spec-template.md` which contains:

- Required sections (User Scenarios, Requirements, Key Entities)
- Optional sections (only included if relevant)
- Execution flow pseudocode that Claude follows step-by-step
- [NEEDS CLARIFICATION] placeholder examples

### Step 3: Specification Generation

Claude executes the template's workflow:

```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

### Step 4: Completion Status

Claude updates the **Execution Status** section at the bottom of the spec with checkboxes:

```markdown
## Execution Status
- [X] User description parsed
- [X] Key concepts extracted
- [X] Ambiguities marked
- [X] User scenarios defined
- [X] Requirements generated
- [X] Entities identified
- [X] Review checklist passed
```

---

## Example Terminal Output

```
User: /specify "Real-time chat system with message history and user presence"

Claude:
  Running script: create-new-feature.sh --json "Real-time chat system with message history and user presence"
  ✓ Received: {"FEATURE_ID":"001-real-time-chat","SPEC_FILE":"...","FEATURE_NUM":"001"}

  Loading spec template...
  Extracting key concepts from description...

  Identified actors: Chat User
  Identified actions: Send messages, view history, track presence
  Identified data: Messages, chat rooms, user status
  Identified constraints: Real-time delivery, concurrent users (unspecified)

  Creating specification at specs/001-real-time-chat/spec.md...

  Sections completed:
  - User Scenarios: 3 primary flows defined
  - Functional Requirements: 8 requirements (4 with clarification markers)
  - Key Entities: Message, Room, User

  ⚠ Clarifications needed (4):
  - FR-001: Message delivery latency target
  - FR-003: Message retention policy
  - FR-006: User authentication method
  - FR-007: Presence update frequency

  Feature 001-real-time-chat created successfully!

  Next command: /clarify (to resolve ambiguities) OR /plan (if acceptable as-is)
```

---

## Generated Specification Structure

The generated `specs/001-real-time-chat/spec.md` looks like this:

```markdown
# Feature Specification: Real-Time Chat System

**Feature ID**: `001-real-time-chat`
**Created**: 2025-10-17
**Status**: Draft
**Input**: User description: "Real-time chat system with message history and user presence"

## User Scenarios & Testing

### Primary User Story
Users need to communicate in real-time within chat rooms, with the ability to view message history and see which other users are currently active.

### Acceptance Scenarios
1. **Given** a user is in a chat room, **When** they send a message, **Then** all room participants see the message within [NEEDS CLARIFICATION: latency target?]
2. **Given** a user joins a chat room, **When** the room loads, **Then** they see the last 50 messages
3. **Given** multiple users are in a room, **When** one user's connection status changes, **Then** other users see updated presence indicators

### Edge Cases
- What happens when network connection drops during message send?
- How does system handle message history exceeding [NEEDS CLARIFICATION: pagination limit?]
- What happens when user rejoins after being offline?

## Requirements

### Functional Requirements
- **FR-001**: System MUST deliver messages to all room participants within [NEEDS CLARIFICATION: latency target - 100ms? 1s? 5s?]
- **FR-002**: System MUST persist message history
- **FR-003**: System MUST retain messages for [NEEDS CLARIFICATION: retention period - 30 days? 1 year? forever?]
- **FR-004**: Users MUST be able to join/leave rooms dynamically
- **FR-005**: System MUST queue messages for offline users
- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method - email/password? OAuth2? SSO?]
- **FR-007**: System MUST update user presence every [NEEDS CLARIFICATION: update frequency - 30s? 1min? 5min?]
- **FR-008**: System MUST support [NEEDS CLARIFICATION: concurrent user count - 100? 1000? 10k?]

### Key Entities
- **Message**: text content, timestamp, sender identifier, room identifier
- **Room**: room identifier, participant list, created timestamp
- **User**: user identifier, username, connection status (online/offline)

---

## Review & Acceptance Checklist

### Content Quality
- [X] No implementation details (languages, frameworks, APIs)
- [X] Focused on user value and business needs
- [X] Written for non-technical stakeholders
- [X] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain  ← **4 markers present**
- [X] Requirements are testable and unambiguous
- [X] Success criteria are measurable
- [X] Scope is clearly bounded
- [X] Dependencies and assumptions identified

---

## Execution Status

- [X] User description parsed
- [X] Key concepts extracted
- [X] Ambiguities marked
- [X] User scenarios defined
- [X] Requirements generated
- [X] Entities identified
- [X] Review checklist passed
```

---

## Understanding [NEEDS CLARIFICATION] Markers

### What Are They?

`[NEEDS CLARIFICATION: specific question]` markers indicate where Claude detected ambiguities in your feature description that require explicit user decisions.

### Common Areas Requiring Clarification

1. **Authentication Methods**
   - `[NEEDS CLARIFICATION: email/password, OAuth2, or SSO?]`

2. **Performance Targets**
   - `[NEEDS CLARIFICATION: latency target - <100ms? <1s?]`
   - `[NEEDS CLARIFICATION: support 100 or 10k concurrent users?]`

3. **Data Retention**
   - `[NEEDS CLARIFICATION: retain for 30 days? 1 year? indefinitely?]`

4. **Scale and Capacity**
   - `[NEEDS CLARIFICATION: max file size - 10MB? 100MB? 1GB?]`
   - `[NEEDS CLARIFICATION: requests per second - 100? 1000? 10k?]`

5. **Error Handling**
   - `[NEEDS CLARIFICATION: retry failed uploads automatically?]`
   - `[NEEDS CLARIFICATION: queue or drop messages when offline?]`

### Why Claude Doesn't Guess

**The "Never Guess" Rule**: Claude is explicitly instructed to mark ambiguities rather than making assumptions. This prevents the most common LLM failure mode: hallucinating plausible but incorrect details.

**Example of Prevented Hallucination**:
```
User: /specify "Login system"

BAD (guessing):
FR-001: System MUST authenticate via email/password with SHA-256 hashing
FR-002: System MUST enforce 8-character minimum passwords
FR-003: Session timeout after 30 minutes
↑ Claude invented password policy details

GOOD (marking uncertainty):
FR-001: System MUST authenticate via [NEEDS CLARIFICATION: email/password? OAuth2? SSO?]
FR-002: System MUST enforce [NEEDS CLARIFICATION: password policy requirements?]
FR-003: Session timeout after [NEEDS CLARIFICATION: duration - 15min? 1hr? 24hr?]
↑ Claude marks what needs decisions
```

---

## Sequential Feature Numbering

### How It Works

Feature IDs are assigned sequentially using a **3-digit prefix**:

```
specs/
├── 001-user-authentication/
│   └── spec.md
├── 002-file-upload/
│   └── spec.md
├── 003-real-time-chat/
│   └── spec.md
```

### Numbering Logic

1. Script scans `specs/` directory for existing feature directories
2. Extracts numeric prefix from each directory name (001, 002, 003, etc.)
3. Finds highest number (e.g., 003)
4. Increments to get next ID (004)
5. Creates directory with new ID

### Feature Name Slugification

The feature description is converted to a URL-friendly slug:

**Input**: `"Real-time chat system with message history"`
**Slugification Process**:
1. Convert to lowercase: `"real-time chat system with message history"`
2. Replace non-alphanumeric with hyphens: `"real-time-chat-system-with-message-history"`
3. Collapse multiple hyphens: `"real-time-chat-system-with-message-history"`
4. Take first 3 words: `"real-time-chat"`

**Output**: `001-real-time-chat`

### Why Sequential Numbering?

- **Prevents conflicts**: Multiple developers can create features without coordination
- **Chronological tracking**: Feature order reflects development timeline
- **No manual intervention**: Automatic assignment prevents human error
- **Solo workflow optimized**: No need for git branches (feature = directory, not branch)

---

## All Possible Outcomes

### Success with Clarification Markers

```
✓ Feature 001-real-time-chat created
✓ spec.md generated with 8 requirements
⚠ 4 clarifications needed

Next: /clarify (highly recommended)
```

**Files Created**:
- `specs/001-real-time-chat/spec.md`

**Follow-up**: Run `/clarify` to resolve ambiguities interactively, **or** manually edit `spec.md` to replace markers, **or** proceed to `/plan` if ambiguities are acceptable.

---

### Success with No Markers (Rare)

```
✓ Feature 002-simple-endpoint created
✓ spec.md complete with no ambiguities
✓ Ready for planning

Next: /plan
```

**When This Happens**: Very simple features with clear, well-specified requirements (e.g., "Add GET /health endpoint returning status 200").

---

### Error: Empty Description

```
❌ Error: No feature description provided

Usage: /specify "feature description"
```

**Resolution**: Provide a feature description:
```
/specify "User authentication with OAuth2"
```

---

### Error: Script Execution Failed

```
❌ Error: create-new-feature.sh failed with exit code 1

Details: Could not determine repository root
```

**Possible Causes**:
- Not in a spec-kit initialized project (missing `.specify/` directory)
- Script permissions not set (not executable)
- Invalid repository structure

**Resolution**:
```bash
# Verify you're in a spec-kit project
ls .specify/templates/  # Should exist

# If missing, initialize project
speclaude init --here

# Retry command
/specify "Feature description"
```

---

### Error: JSON Parsing Failed

```
❌ Error: Could not parse JSON output from create-new-feature.sh

Expected format: {"FEATURE_ID":"...","SPEC_FILE":"...","FEATURE_NUM":"..."}
Received: [error message or malformed output]
```

**Possible Causes**:
- Script wrote errors to stdout instead of stderr
- Script was modified and broke JSON contract
- Filesystem permissions issue

**Resolution**:
```bash
# Test script directly
.specify/scripts/bash/create-new-feature.sh --json "test feature"

# Should output valid JSON
# If not, check script integrity or reinstall templates
speclaude init --here --force
```

---

## Best Practices

### 1. Be Specific, Not Technical

Focus on **requirements**, not **implementation**:

**Good**:
```
/specify "Real-time chat supporting 10k concurrent users with <100ms message delivery"
```

**Bad**:
```
/specify "WebSocket-based chat using Redis Pub/Sub and PostgreSQL"
```

### 2. Include Scale and User Goals

Mention **who**, **how many**, and **why**:

**Good**:
```
/specify "Admin dashboard showing login analytics for 50k daily active users to identify security anomalies"
```

**Bad**:
```
/specify "Admin dashboard with analytics"
```

### 3. Accept Ambiguity, Don't Force Details

If you're unsure about specifics, let Claude mark them:

**Good**:
```
/specify "File upload system for images"
→ Claude will mark [NEEDS CLARIFICATION: max file size? supported formats?]
```

**Bad**:
```
/specify "File upload system for images max 10MB supporting JPG/PNG"
→ You've prematurely decided limits without analysis
```

### 4. Avoid Vague Adjectives

Replace "fast", "secure", "robust" with **measurable criteria** or let Claude mark them:

**Vague**:
```
/specify "Fast image processing system"
```

**Measurable**:
```
/specify "Image processing system handling 1000 images/hour with <30s per image"
```

---

## Common Issues and Troubleshooting

### Issue 1: Too Much Technical Detail in Spec

**Symptom**: Spec mentions frameworks, databases, APIs

**Example**:
```markdown
FR-001: Use FastAPI to create REST endpoint
FR-002: Store data in PostgreSQL with SQLAlchemy ORM
```

**Resolution**: Manually edit `spec.md` to remove technical details:
```markdown
FR-001: System MUST provide HTTP API for data access
FR-002: System MUST persist data reliably
```

**Why This Happens**: Your `/specify` input included technical details. For next time, focus on WHAT not HOW.

---

### Issue 2: Vague Requirements Slip Through

**Symptom**: Requirements like "fast", "secure", "robust" without clarification markers

**Example**:
```markdown
FR-001: System MUST be fast
FR-002: System MUST be secure
```

**Resolution**: Manually add clarification markers or replace with measurable criteria:
```markdown
FR-001: System MUST respond within [NEEDS CLARIFICATION: latency target?]
FR-002: System MUST implement [NEEDS CLARIFICATION: authentication method?]
```

**Prevention**: In future `/specify` calls, include specific metrics:
```
/specify "API with <100ms response time and OAuth2 authentication"
```

---

### Issue 3: Feature ID Collision

**Symptom**: Script fails with "Directory already exists" error

**Cause**: You re-ran `/specify` with same description, or manually created directory with conflicting ID

**Resolution**:
```bash
# Check existing features
ls specs/

# If 001-real-time-chat exists and you want to recreate it
rm -rf specs/001-real-time-chat/

# Or use different description to get new ID
/specify "Real-time messaging system"  # Will create 002-real-time-messaging
```

---

### Issue 4: Missing Key Entities

**Symptom**: Spec's "Key Entities" section is empty for a data-heavy feature

**Example**: Specified "User management system" but no User entity listed

**Resolution**: Manually add entities to spec.md:
```markdown
### Key Entities
- **User**: user_id, email, username, created_at
- **Role**: role_id, role_name, permissions
- **Session**: session_id, user_id, expires_at
```

**Prevention**: Mention key data types in `/specify` description:
```
/specify "User management system with users, roles, and session tracking"
```

---

## Importance in the Workflow

### Foundation for All Downstream Work

The specification created by `/specify` is the **single source of truth** for:

1. **`/plan`** - Technical design decisions reference functional requirements
2. **`/tasks`** - Task breakdown maps to specific requirements (FR-001 → T010)
3. **`/implement`** - Implementation validates against acceptance scenarios
4. **`/analyze`** - Consistency checks ensure all requirements have tasks

### Prevents Scope Creep

A written specification acts as a **contract**:
- Stakeholders can review and approve before implementation
- Changes require updating the spec (visible, trackable)
- Implementation stays focused on documented requirements

### Enables Test-Driven Development

Specifications define **acceptance criteria** before implementation:
- FR-001: Message delivery <100ms → Performance test task
- Scenario: User sends message → Integration test task
- Entity: Message with fields → Model test task

---

## Cross-References

### Related Commands
- **Next Step**: [`/clarify`](06-clarify-command.md) - Resolve [NEEDS CLARIFICATION] markers interactively
- **Alternative Next**: [`/plan`](07-plan-command.md) - Skip clarification and proceed to technical design
- **Previous Step**: [`/constitution`](04-constitution-command.md) - Project governance setup

### Related Templates
- **Source**: `templates/commands/specify.md` - Command implementation ([lines 1-22](../../templates/commands/specify.md))
- **Structure**: `templates/spec-template.md` - Spec structure with execution flow ([lines 1-117](../../templates/spec-template.md))

### Related Scripts
- **Script**: `scripts/bash/create-new-feature.sh` - Feature directory creation ([lines 1-101](../../scripts/bash/create-new-feature.sh))
- **Contract**: JSON output format ([lines 93-94](../../scripts/bash/create-new-feature.sh))

### Related Documentation
- **Overview**: `ai-docs/kb/04-commands-core.md` - Specify command details ([lines 150-300](../../ai-docs/kb/04-commands-core.md))
- **Workflow**: `ai-docs/kb/10-workflows.md` - Specify examples in full workflows ([lines 87-117](../../ai-docs/kb/10-workflows.md))
- **Philosophy**: `ai-docs/kb/02-philosophy.md` - Power inversion paradigm (specifications as truth)

---

## Summary Checklist

Before running `/specify`, ensure:
- [ ] You've run `/constitution` to establish project principles
- [ ] You have a 1-3 sentence feature description ready
- [ ] Description focuses on WHAT/WHY/WHO (not HOW)
- [ ] You're prepared to accept [NEEDS CLARIFICATION] markers

After `/specify` completes, check:
- [ ] `specs/###-feature-name/spec.md` file was created
- [ ] Feature ID assigned (001, 002, 003, etc.)
- [ ] User Scenarios section is populated
- [ ] Functional Requirements are listed (FR-001, FR-002, etc.)
- [ ] [NEEDS CLARIFICATION] markers are present (if ambiguities exist)

Decide next step:
- [ ] Run `/clarify` if markers exist (highly recommended)
- [ ] Run `/plan` directly if spec is acceptable as-is
- [ ] Manually edit spec.md if you want to resolve markers yourself

---

**Navigation**: [← Constitution Command](04-constitution-command.md) | [Clarify Command →](06-clarify-command.md)
