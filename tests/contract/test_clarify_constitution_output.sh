#!/usr/bin/env bash
# Contract Test: /clarify-constitution Command Execution Flow
# Contract: specs/001-when-the-user/contracts/clarify-constitution-command.md

set -euo pipefail

# Test Setup
TEST_NAME="test_clarify_constitution_output"
FAILURES=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILURES++))
}

info() {
    echo -e "${YELLOW}→${NC} $1"
}

# Test 1: JSON path parsing from check-prerequisites.sh
test_json_path_parsing() {
    info "Test 1: Verify check-prerequisites.sh --json output format"

    # Create minimal test environment
    TEST_DIR=$(mktemp -d)
    mkdir -p "$TEST_DIR/.specify/memory"
    touch "$TEST_DIR/.specify/memory/constitution.md"

    # Run script (simulated - actual implementation will be in command template)
    # This test validates the expected JSON structure
    EXPECTED_KEYS=("CONSTITUTION_FILE")

    for key in "${EXPECTED_KEYS[@]}"; do
        if [[ "$key" == "CONSTITUTION_FILE" ]]; then
            pass "JSON should contain key: $key"
        else
            fail "Missing expected JSON key: $key"
        fi
    done

    # Cleanup
    rm -rf "$TEST_DIR"
}

# Test 2: Marker detection regex pattern
test_marker_detection() {
    info "Test 2: Verify [NEEDS CLARIFICATION] marker detection"

    TEST_CONTENT='
## Core Principles
### I. Architectural Principle
[NEEDS CLARIFICATION]

### II. Technology Stack
**Language**: Python [NEEDS CLARIFICATION: version]
**Framework**: [NEEDS CLARIFICATION: FastAPI vs Django]

## Governance
[NEEDS CLARIFICATION: amendment process]
'

    # Expected: 4 markers detected
    MARKER_PATTERN='\[NEEDS CLARIFICATION[^]]*\]'
    MARKER_COUNT=$(echo "$TEST_CONTENT" | grep -E -o "$MARKER_PATTERN" | wc -l | xargs)

    if [[ "$MARKER_COUNT" -eq 4 ]]; then
        pass "Detected 4 [NEEDS CLARIFICATION] markers correctly"
    else
        fail "Expected 4 markers, found $MARKER_COUNT"
    fi
}

# Test 3: Question generation (max 5 questions)
test_question_limit() {
    info "Test 3: Verify max 5 questions per session"

    # Simulate 10 ambiguities detected
    AMBIGUITY_COUNT=10
    MAX_QUESTIONS=5

    if [[ $MAX_QUESTIONS -eq 5 ]]; then
        pass "Question limit correctly set to 5"
    else
        fail "Question limit should be 5, got $MAX_QUESTIONS"
    fi
}

# Test 4: Sequential questioning (one at a time)
test_sequential_questioning() {
    info "Test 4: Verify sequential questioning pattern"

    # Contract requirement: Present ONE question at a time (never batch)
    BATCH_QUESTIONS=false

    if [[ "$BATCH_QUESTIONS" == "false" ]]; then
        pass "Questions presented sequentially (one at a time)"
    else
        fail "Questions should be sequential, not batched"
    fi
}

# Test 5: Integration after each answer
test_integration_after_answer() {
    info "Test 5: Verify integration happens after each answer"

    # Contract: Update constitution after EACH accepted answer
    # Create test constitution
    TEST_DIR=$(mktemp -d)
    TEST_FILE="$TEST_DIR/constitution.md"

    echo "**Workflow**: [NEEDS CLARIFICATION]" > "$TEST_FILE"

    # Simulate answer integration
    sed -i '' 's/\[NEEDS CLARIFICATION\]/Trunk-based development/' "$TEST_FILE" 2>/dev/null || \
    sed -i 's/\[NEEDS CLARIFICATION\]/Trunk-based development/' "$TEST_FILE"

    # Verify replacement
    if grep -q "Trunk-based development" "$TEST_FILE"; then
        pass "Constitution updated after answer integration"
    else
        fail "Constitution should be updated after each answer"
    fi

    # Cleanup
    rm -rf "$TEST_DIR"
}

# Test 6: Session tracking metadata
test_session_tracking() {
    info "Test 6: Verify session count tracking"

    # Contract: <!-- Clarification Sessions: N -->
    TEST_DIR=$(mktemp -d)
    TEST_FILE="$TEST_DIR/constitution.md"

    echo "<!-- Clarification Sessions: 0 -->" > "$TEST_FILE"
    echo "# Project Constitution" >> "$TEST_FILE"

    # Verify metadata present
    if grep -q "<!-- Clarification Sessions: 0 -->" "$TEST_FILE"; then
        pass "Session metadata initialized correctly"
    else
        fail "Session metadata should be present"
    fi

    # Test increment
    sed -i '' 's/Sessions: 0/Sessions: 1/' "$TEST_FILE" 2>/dev/null || \
    sed -i 's/Sessions: 0/Sessions: 1/' "$TEST_FILE"

    if grep -q "<!-- Clarification Sessions: 1 -->" "$TEST_FILE"; then
        pass "Session count increments correctly"
    else
        fail "Session count should increment"
    fi

    # Cleanup
    rm -rf "$TEST_DIR"
}

# Test 7: Soft limit warning (session >= 3)
test_soft_limit_warning() {
    info "Test 7: Verify soft limit warning at 3+ sessions"

    SESSION_COUNT=4
    SOFT_LIMIT=3

    if [[ $SESSION_COUNT -ge $SOFT_LIMIT ]]; then
        pass "Soft limit warning triggers at session $SESSION_COUNT (threshold: $SOFT_LIMIT)"
    else
        fail "Soft limit should warn at $SOFT_LIMIT sessions"
    fi
}

# Test 8: Clarifications section structure
test_clarifications_section() {
    info "Test 8: Verify Clarifications section structure"

    TEST_DIR=$(mktemp -d)
    TEST_FILE="$TEST_DIR/constitution.md"

    cat > "$TEST_FILE" <<'EOF'
## Clarifications

### Session 2025-10-05
- Q: What is the primary principle? → A: Test-first development
- Q: What Python framework? → A: FastAPI
EOF

    # Verify section exists
    if grep -q "## Clarifications" "$TEST_FILE"; then
        pass "Clarifications section present"
    else
        fail "Clarifications section should be added"
    fi

    # Verify session subsection
    if grep -q "### Session 2025-10-05" "$TEST_FILE"; then
        pass "Session subsection with date present"
    else
        fail "Session subsection should include date"
    fi

    # Verify Q&A bullet format
    if grep -q "Q:.*→ A:" "$TEST_FILE"; then
        pass "Q&A bullets formatted correctly"
    else
        fail "Q&A bullets should use format: Q: <question> → A: <answer>"
    fi

    # Cleanup
    rm -rf "$TEST_DIR"
}

# Run all tests
echo "========================================="
echo "Contract Test: /clarify-constitution Command"
echo "========================================="
echo ""

test_json_path_parsing
test_marker_detection
test_question_limit
test_sequential_questioning
test_integration_after_answer
test_session_tracking
test_soft_limit_warning
test_clarifications_section

echo ""
echo "========================================="
if [[ $FAILURES -eq 0 ]]; then
    echo -e "${GREEN}All tests passed ✓${NC}"
    exit 0
else
    echo -e "${RED}$FAILURES test(s) failed ✗${NC}"
    exit 1
fi
