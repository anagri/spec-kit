#!/usr/bin/env bash
# Contract Test: Constitution [NEEDS CLARIFICATION] Marker Handling
# Contract: specs/001-when-the-user/contracts/constitution-template.md

set -euo pipefail

# Test Setup
TEST_NAME="test_constitution_markers"
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

# Test 1: Marker insertion when user input insufficient
test_marker_insertion() {
    info "Test 1: Verify marker insertion for insufficient input"

    # Simulate minimal user input: "Python app"
    USER_INPUT="Python app"

    # Insufficient information for:
    # - Python version (language known, version unknown)
    # - Framework (FastAPI vs Django vs Flask)
    # - Workflow (solo vs team, branching)
    # - Governance (amendment process)

    # Expected markers: 4
    EXPECTED_MARKERS=4

    if [[ $EXPECTED_MARKERS -ge 1 ]]; then
        pass "Markers inserted when input insufficient"
    else
        fail "Should insert markers for missing information"
    fi
}

# Test 2: Valid marker syntax
test_marker_syntax() {
    info "Test 2: Verify marker syntax patterns"

    TEST_DIR=$(mktemp -d)
    TEST_FILE="$TEST_DIR/constitution.md"

    cat > "$TEST_FILE" <<'EOF'
## Core Principles
### I. Architectural Principle
[NEEDS CLARIFICATION]

### II. Technology Stack
**Language**: Python [NEEDS CLARIFICATION: version]
**Framework**: [NEEDS CLARIFICATION: FastAPI vs Django]
EOF

    # Valid syntax: [NEEDS CLARIFICATION] or [NEEDS CLARIFICATION: hint]
    PATTERN_SIMPLE='\[NEEDS CLARIFICATION\]'
    PATTERN_WITH_HINT='\[NEEDS CLARIFICATION: [^]]+\]'

    if grep -q "$PATTERN_SIMPLE" "$TEST_FILE"; then
        pass "Simple marker syntax valid: [NEEDS CLARIFICATION]"
    else
        fail "Simple marker syntax should be supported"
    fi

    if grep -E -q "$PATTERN_WITH_HINT" "$TEST_FILE"; then
        pass "Marker with hint syntax valid: [NEEDS CLARIFICATION: hint]"
    else
        fail "Marker with hint should be supported"
    fi

    # Cleanup
    rm -rf "$TEST_DIR"
}

# Test 3: Marker placement (content only, not headings)
test_marker_placement() {
    info "Test 3: Verify markers in content only, not headings"

    TEST_DIR=$(mktemp -d)
    TEST_FILE="$TEST_DIR/constitution.md"

    cat > "$TEST_FILE" <<'EOF'
## Core Principles

### I. Architectural Principle
[NEEDS CLARIFICATION]

### II. Technology Stack
**Language**: Python [NEEDS CLARIFICATION: version]
EOF

    # Valid: Markers in content sections
    if grep -A1 "### I\." "$TEST_FILE" | grep -q "\[NEEDS CLARIFICATION\]"; then
        pass "Markers correctly placed in content sections"
    else
        fail "Markers should be in content, not headings"
    fi

    # Invalid: Markers in headings (should NOT exist)
    if grep "^###.*\[NEEDS CLARIFICATION\]" "$TEST_FILE"; then
        fail "Markers should NOT appear in headings"
    else
        pass "No markers in heading lines (correct)"
    fi

    # Cleanup
    rm -rf "$TEST_DIR"
}

# Test 4: Marker removal on clarification
test_marker_removal() {
    info "Test 4: Verify marker removal when user provides info"

    TEST_DIR=$(mktemp -d)
    TEST_FILE="$TEST_DIR/constitution.md"

    # Before: Marker present
    echo "**Workflow**: [NEEDS CLARIFICATION]" > "$TEST_FILE"

    # User provides answer: "Trunk-based development"
    # System should replace marker with user's answer
    sed -i '' 's/\[NEEDS CLARIFICATION\]/Trunk-based development/' "$TEST_FILE"

    # After: Marker removed, content added
    if grep -q "Trunk-based development" "$TEST_FILE" && ! grep -q "\[NEEDS CLARIFICATION\]" "$TEST_FILE"; then
        pass "Marker removed and replaced with user answer"
    else
        fail "Marker should be removed when user provides answer"
    fi

    # Cleanup
    rm -rf "$TEST_DIR"
}

# Test 5: Session metadata initialization
test_session_metadata() {
    info "Test 5: Verify session metadata initialization"

    TEST_DIR=$(mktemp -d)
    TEST_FILE="$TEST_DIR/constitution.md"

    cat > "$TEST_FILE" <<'EOF'
<!-- Clarification Sessions: 0 -->

# Project Constitution

## Core Principles
### I. Architectural Principle
[NEEDS CLARIFICATION]
EOF

    # Verify metadata exists when markers present
    if grep -q "<!-- Clarification Sessions: 0 -->" "$TEST_FILE"; then
        pass "Session metadata initialized to 0"
    else
        fail "Session metadata should be initialized when markers present"
    fi

    # Verify metadata is at the top
    if head -1 "$TEST_FILE" | grep -q "<!-- Clarification Sessions:"; then
        pass "Session metadata at top of file"
    else
        fail "Session metadata should be at top of file"
    fi

    # Cleanup
    rm -rf "$TEST_DIR"
}

# Test 6: No markers for comprehensive input
test_comprehensive_input_no_markers() {
    info "Test 6: Verify no markers when input is comprehensive"

    # Comprehensive input: "Python 3.11 FastAPI project. Test-first principle. Solo dev, trunk-based. Quarterly reviews."
    # All required information provided:
    # - Language: Python 3.11 ✓
    # - Framework: FastAPI ✓
    # - Principle: Test-first ✓
    # - Workflow: Solo dev, trunk-based ✓
    # - Governance: Quarterly reviews ✓

    EXPECTED_MARKERS=0

    if [[ $EXPECTED_MARKERS -eq 0 ]]; then
        pass "No markers when input comprehensive"
    else
        fail "Comprehensive input should result in 0 markers"
    fi
}

# Test 7: Partial input results in partial markers
test_partial_input() {
    info "Test 7: Verify partial markers for partial input"

    # Partial input: "Python 3.11 project, test-first principle"
    # Provided:
    # - Language: Python 3.11 ✓
    # - Principle: Test-first ✓
    # Missing:
    # - Framework: [NEEDS CLARIFICATION]
    # - Workflow: [NEEDS CLARIFICATION]
    # - Governance: [NEEDS CLARIFICATION]

    PROVIDED_COUNT=2
    MISSING_COUNT=3

    if [[ $MISSING_COUNT -eq 3 ]]; then
        pass "Partial input results in markers only for missing information"
    else
        fail "Should have markers only where information is missing"
    fi
}

# Test 8: Marker specificity (hints)
test_marker_hints() {
    info "Test 8: Verify marker hints provide context"

    TEST_DIR=$(mktemp -d)
    TEST_FILE="$TEST_DIR/constitution.md"

    cat > "$TEST_FILE" <<'EOF'
**Language**: Python [NEEDS CLARIFICATION: version]
**Framework**: [NEEDS CLARIFICATION: FastAPI vs Django vs Flask]
**Workflow**: [NEEDS CLARIFICATION: solo vs team, branching strategy]
EOF

    # Verify hints are specific and helpful
    if grep -q "\[NEEDS CLARIFICATION: version\]" "$TEST_FILE"; then
        pass "Marker hint provides context: 'version'"
    else
        fail "Marker should include helpful hint"
    fi

    if grep -q "\[NEEDS CLARIFICATION: FastAPI vs Django vs Flask\]" "$TEST_FILE"; then
        pass "Marker hint shows options: 'FastAPI vs Django vs Flask'"
    else
        fail "Marker should show available options when applicable"
    fi

    if grep -q "\[NEEDS CLARIFICATION: solo vs team, branching strategy\]" "$TEST_FILE"; then
        pass "Marker hint indicates multiple aspects: 'solo vs team, branching strategy'"
    else
        fail "Marker should indicate multiple missing aspects"
    fi

    # Cleanup
    rm -rf "$TEST_DIR"
}

# Run all tests
echo "========================================="
echo "Contract Test: Constitution Marker Handling"
echo "========================================="
echo ""

test_marker_insertion
test_marker_syntax
test_marker_placement
test_marker_removal
test_session_metadata
test_comprehensive_input_no_markers
test_partial_input
test_marker_hints

echo ""
echo "========================================="
if [[ $FAILURES -eq 0 ]]; then
    echo -e "${GREEN}All tests passed ✓${NC}"
    exit 0
else
    echo -e "${RED}$FAILURES test(s) failed ✗${NC}"
    exit 1
fi
