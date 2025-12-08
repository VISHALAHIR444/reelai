#!/bin/bash

# GRAVIXAI Backend - API Testing Script
# Test all endpoints to verify the system is working

API_URL="http://localhost:8000"

echo "🚀 GRAVIXAI Backend - API Endpoint Testing"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    
    echo -e "${BLUE}Testing:${NC} $description"
    echo -e "  ${method} ${endpoint}"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "${API_URL}${endpoint}")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST \
            -H "Content-Type: application/json" \
            -d '{}' \
            "${API_URL}${endpoint}")
    elif [ "$method" = "DELETE" ]; then
        response=$(curl -s -w "\n%{http_code}" -X DELETE \
            "${API_URL}${endpoint}")
    fi
    
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    if [[ "$http_code" =~ ^[2] ]]; then
        echo -e "  ${GREEN}✓ Status: $http_code${NC}"
    else
        echo -e "  ${RED}✗ Status: $http_code${NC}"
    fi
    echo ""
}

# Health Checks
echo -e "${BLUE}━━━ HEALTH CHECKS ━━━${NC}"
test_endpoint "GET" "/" "Root endpoint"
test_endpoint "GET" "/health" "Health check"
test_endpoint "GET" "/ready" "Readiness check"

# Video Endpoints
echo -e "${BLUE}━━━ VIDEO ENDPOINTS ━━━${NC}"
test_endpoint "GET" "/api/video/" "List all videos"

# Reels Endpoints
echo -e "${BLUE}━━━ REELS ENDPOINTS ━━━${NC}"
test_endpoint "GET" "/api/reels/" "List all reels"

# Social Endpoints
echo -e "${BLUE}━━━ SOCIAL/OAUTH ENDPOINTS ━━━${NC}"
test_endpoint "GET" "/api/social/connect" "Get OAuth URL"
test_endpoint "GET" "/api/social/status" "Check connection status"

echo -e "${GREEN}✓ API Testing Complete!${NC}"
echo ""
echo "To see full API documentation, visit:"
echo "  http://localhost:8000/docs"
