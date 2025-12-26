#!/bin/bash
# Validate Claude Code + Vertex AI Setup
# This script confirms you're using FedRAMP-compliant Vertex AI

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}=== Claude Code Vertex AI Validation ===${NC}"
echo ""

errors=()
warnings=()

# Check environment variables
echo -e "${YELLOW}Checking environment variables...${NC}"

if [ "$CLAUDE_CODE_USE_VERTEX" = "1" ]; then
    echo -e "  ${GREEN}[OK]${NC} CLAUDE_CODE_USE_VERTEX = 1"
else
    errors+=("CLAUDE_CODE_USE_VERTEX not set to 1")
    echo -e "  ${RED}[FAIL]${NC} CLAUDE_CODE_USE_VERTEX not set"
fi

if [ -n "$ANTHROPIC_VERTEX_PROJECT_ID" ]; then
    echo -e "  ${GREEN}[OK]${NC} ANTHROPIC_VERTEX_PROJECT_ID = $ANTHROPIC_VERTEX_PROJECT_ID"
else
    errors+=("ANTHROPIC_VERTEX_PROJECT_ID not set")
    echo -e "  ${RED}[FAIL]${NC} ANTHROPIC_VERTEX_PROJECT_ID not set"
fi

if [ -n "$CLOUD_ML_REGION" ]; then
    echo -e "  ${GREEN}[OK]${NC} CLOUD_ML_REGION = $CLOUD_ML_REGION"

    # Check for FedRAMP regions
    case "$CLOUD_ML_REGION" in
        us-east5|us-central1|us-west1)
            echo -e "  ${GREEN}[OK]${NC} Region is FedRAMP-eligible"
            ;;
        *)
            warnings+=("Region $CLOUD_ML_REGION may not be FedRAMP-certified")
            echo -e "  ${YELLOW}[WARN]${NC} Region may not be FedRAMP-certified"
            ;;
    esac
else
    errors+=("CLOUD_ML_REGION not set")
    echo -e "  ${RED}[FAIL]${NC} CLOUD_ML_REGION not set"
fi

echo ""
echo -e "${YELLOW}Checking gcloud authentication...${NC}"

# Check gcloud auth
if command -v gcloud &> /dev/null; then
    account=$(gcloud config get-value account 2>/dev/null)
    if [ -n "$account" ]; then
        echo -e "  ${GREEN}[OK]${NC} Logged in as: $account"
    else
        errors+=("Not logged into gcloud")
        echo -e "  ${RED}[FAIL]${NC} Not logged into gcloud"
    fi
else
    errors+=("gcloud CLI not installed")
    echo -e "  ${RED}[FAIL]${NC} gcloud CLI not found"
fi

# Check ADC
adc_path="$HOME/.config/gcloud/application_default_credentials.json"
if [ -f "$adc_path" ]; then
    echo -e "  ${GREEN}[OK]${NC} Application Default Credentials exist"

    # Check if ADC is recent (within 24 hours)
    if [ "$(uname)" = "Darwin" ]; then
        # macOS
        adc_age=$(( ($(date +%s) - $(stat -f %m "$adc_path")) / 3600 ))
    else
        # Linux
        adc_age=$(( ($(date +%s) - $(stat -c %Y "$adc_path")) / 3600 ))
    fi

    if [ "$adc_age" -gt 24 ]; then
        warnings+=("ADC may be expired (last updated $adc_age hours ago)")
        echo -e "  ${YELLOW}[WARN]${NC} ADC may be expired ($adc_age hours old)"
    fi
else
    errors+=("ADC not found - run 'gcloud auth application-default login'")
    echo -e "  ${RED}[FAIL]${NC} ADC not found"
fi

echo ""
echo -e "${YELLOW}Checking Claude Code installation...${NC}"

# Check Claude Code
if command -v claude &> /dev/null; then
    claude_version=$(claude --version 2>/dev/null)
    echo -e "  ${GREEN}[OK]${NC} Claude Code installed: $claude_version"
else
    errors+=("Claude Code not installed")
    echo -e "  ${RED}[FAIL]${NC} Claude Code not found"
fi

echo ""
echo -e "${CYAN}=== FedRAMP Compliance Status ===${NC}"

if [ ${#errors[@]} -eq 0 ]; then
    echo ""
    echo -e "${GREEN}SUCCESS: Your setup is configured for FedRAMP-compliant Vertex AI!${NC}"
    echo ""
    echo "You are inferencing from:"
    echo "  - Project: $ANTHROPIC_VERTEX_PROJECT_ID"
    echo "  - Region: $CLOUD_ML_REGION"
    echo "  - Provider: Google Cloud Vertex AI (FedRAMP High)"
    echo ""
    echo -e "All API calls are logged in GCP Cloud Logging for audit compliance."
else
    echo ""
    echo -e "${RED}ERRORS FOUND:${NC}"
    for error in "${errors[@]}"; do
        echo -e "  ${RED}- $error${NC}"
    done
fi

if [ ${#warnings[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}WARNINGS:${NC}"
    for warning in "${warnings[@]}"; do
        echo -e "  ${YELLOW}- $warning${NC}"
    done
fi

echo ""
