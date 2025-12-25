#!/bin/bash
#
# setup.sh - Sets up Claude Code configuration via symlinks to dev-experience repository.
#
# Usage:
#   ./setup.sh           # Install symlinks
#   ./setup.sh uninstall # Remove symlinks
#
# This enables:
# - Live updates via git pull
# - Shared skills, services, and configuration
# - FedRAMP-compliant MCP servers
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Paths
CLAUDE_DIR="$HOME/.claude"
DEV_EXP_DIR="$(cd "$(dirname "$0")" && pwd)"

# Detect OS for statusline
detect_statusline() {
    case "$(uname -s)" in
        Darwin*) echo "$DEV_EXP_DIR/claude-code/statusline/statusline.sh" ;;
        Linux*)  echo "$DEV_EXP_DIR/claude-code/statusline/statusline.sh" ;;
        *)       echo "$DEV_EXP_DIR/claude-code/statusline/statusline.ps1" ;;
    esac
}

STATUSLINE_TARGET=$(detect_statusline)

# Symlink definitions
declare -a SYMLINKS=(
    "$CLAUDE_DIR/services:$DEV_EXP_DIR/claude-code/agentic-tools"
    "$CLAUDE_DIR/skills:$DEV_EXP_DIR/claude-code/skills"
    "$CLAUDE_DIR/statusline.sh:$STATUSLINE_TARGET"
)

uninstall_symlinks() {
    echo -e "${YELLOW}Removing Claude Code symlinks...${NC}"

    for link_def in "${SYMLINKS[@]}"; do
        link_path="${link_def%%:*}"
        if [ -L "$link_path" ]; then
            rm -f "$link_path"
            echo -e "  ${GREEN}Removed: $link_path${NC}"
        elif [ -e "$link_path" ]; then
            echo -e "  ${YELLOW}Skipped (not a symlink): $link_path${NC}"
        fi
    done

    # Remove import line from CLAUDE.md if present
    CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"
    IMPORT_LINE="@~/.claude/services/CLAUDE.md"
    if [ -f "$CLAUDE_MD" ]; then
        if grep -q "$IMPORT_LINE" "$CLAUDE_MD"; then
            # Remove the import line and any following blank line
            sed -i.bak "/$IMPORT_LINE/d" "$CLAUDE_MD"
            rm -f "$CLAUDE_MD.bak"
            echo -e "  ${GREEN}Removed import from CLAUDE.md${NC}"
        fi
    fi

    echo -e "\n${GREEN}Symlinks removed. Claude Code is now standalone.${NC}"
}

install_symlinks() {
    echo -e "${CYAN}Setting up Claude Code via symlinks to dev-experience...${NC}"
    echo -e "  ${GRAY}Source: $DEV_EXP_DIR${NC}"
    echo -e "  ${GRAY}Target: $CLAUDE_DIR${NC}"
    echo ""

    # Ensure ~/.claude exists
    if [ ! -d "$CLAUDE_DIR" ]; then
        mkdir -p "$CLAUDE_DIR"
        echo -e "  ${GREEN}Created: $CLAUDE_DIR${NC}"
    fi

    # Create symlinks
    for link_def in "${SYMLINKS[@]}"; do
        link_path="${link_def%%:*}"
        target_path="${link_def#*:}"

        # Remove existing if present
        if [ -e "$link_path" ] || [ -L "$link_path" ]; then
            rm -rf "$link_path"
        fi

        # Create symlink
        ln -sfn "$target_path" "$link_path"
        echo -e "  ${GREEN}Linked: $link_path -> $target_path${NC}"
    done

    # Handle CLAUDE.md (additive import)
    CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"
    IMPORT_LINE="@~/.claude/services/CLAUDE.md"

    if [ -f "$CLAUDE_MD" ]; then
        if ! grep -q "$IMPORT_LINE" "$CLAUDE_MD"; then
            # Prepend import to existing file
            echo -e "$IMPORT_LINE\n\n$(cat "$CLAUDE_MD")" > "$CLAUDE_MD"
            echo -e "  ${GREEN}Added import to existing CLAUDE.md${NC}"
        else
            echo -e "  ${GRAY}CLAUDE.md already has import (skipped)${NC}"
        fi
    else
        echo "$IMPORT_LINE" > "$CLAUDE_MD"
        echo -e "  ${GREEN}Created CLAUDE.md with import${NC}"
    fi

    # Add MCP servers at user scope (idempotent)
    echo -e "\n${CYAN}Configuring MCP servers...${NC}"

    add_mcp_server() {
        local name="$1"
        shift
        if claude mcp list 2>/dev/null | grep -q "$name"; then
            echo -e "  ${GRAY}$name: already configured${NC}"
        else
            if claude mcp add "$name" "$@" 2>/dev/null; then
                echo -e "  ${GREEN}$name: added${NC}"
            else
                echo -e "  ${YELLOW}$name: failed to add (run 'claude mcp add' manually)${NC}"
            fi
        fi
    }

    add_mcp_server "gemini-25-pro-fedramp" \
        --scope user \
        --command bunx \
        --args "-y vertex-ai-mcp-server" \
        --env "AI_PROVIDER=vertex" \
        --env "GOOGLE_CLOUD_PROJECT=licensecorporation-dev" \
        --env "VERTEX_MODEL_ID=gemini-2.5-pro" \
        --env "GOOGLE_CLOUD_LOCATION=us-east5" \
        --env "AI_USE_STREAMING=true"

    add_mcp_server "gemini-3-pro-global" \
        --scope user \
        --command bunx \
        --args "-y vertex-ai-mcp-server" \
        --env "AI_PROVIDER=vertex" \
        --env "GOOGLE_CLOUD_PROJECT=licensecorporation-dev" \
        --env "VERTEX_MODEL_ID=gemini-3-pro-preview" \
        --env "GOOGLE_CLOUD_LOCATION=global" \
        --env "AI_USE_STREAMING=true"

    add_mcp_server "gemini-3-flash-global" \
        --scope user \
        --command bunx \
        --args "-y vertex-ai-mcp-server" \
        --env "AI_PROVIDER=vertex" \
        --env "GOOGLE_CLOUD_PROJECT=licensecorporation-dev" \
        --env "VERTEX_MODEL_ID=gemini-3-flash-preview" \
        --env "GOOGLE_CLOUD_LOCATION=global" \
        --env "AI_USE_STREAMING=true"

    echo -e "\n${GREEN}✓ Claude Code configured via symlinks to dev-experience${NC}"
    echo -e "\n${CYAN}To update: cd $DEV_EXP_DIR && git pull${NC}"
    echo -e "${CYAN}To uninstall: ./setup.sh uninstall${NC}"
}

# Main
case "${1:-}" in
    uninstall|--uninstall|-u)
        uninstall_symlinks
        ;;
    *)
        install_symlinks
        ;;
esac
