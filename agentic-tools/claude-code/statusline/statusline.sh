#!/bin/bash
# Claude Code Status Line Script (Unix version)
# Reads JSON from stdin and outputs a formatted status line

# Read all input
input_json=$(cat)

# Extract value from JSON using grep/sed (no jq dependency)
json_get() {
    local key="$1"
    echo "$input_json" | grep -o "\"$key\"[[:space:]]*:[[:space:]]*[^,}]*" | head -1 | sed 's/.*:[[:space:]]*//' | tr -d '"'
}

json_get_num() {
    local key="$1"
    local val=$(json_get "$key")
    echo "${val:-0}" | grep -o '[0-9]*' | head -1
}

# === MODEL ===
model=$(json_get "display_name")
[ -z "$model" ] && model="Claude"

# === CONTEXT ===
context_left="100%"
context_size=$(json_get_num "context_window_size")
if [ "$context_size" -gt 0 ] 2>/dev/null; then
    input_tokens=$(json_get_num "input_tokens")
    cache_creation=$(json_get_num "cache_creation_input_tokens")
    cache_read=$(json_get_num "cache_read_input_tokens")
    used=$((input_tokens + cache_creation + cache_read))
    usable_context=195000
    remaining=$((usable_context - used))
    [ $remaining -lt 0 ] && remaining=0
    pct=$((remaining * 100 / usable_context))
    context_left="${pct}% left"
fi

# === SESSION INFO ===
duration=""
total_ms=$(json_get_num "total_duration_ms")
if [ "$total_ms" -gt 0 ] 2>/dev/null; then
    total_mins=$((total_ms / 60000))
    hours=$((total_mins / 60))
    mins=$((total_mins % 60))
    if [ $hours -gt 0 ]; then
        duration="${hours}h ${mins}m"
    else
        duration="${mins}m"
    fi
fi

# === COST ===
cost_display=""
session_cost=$(json_get "total_cost_usd")
if [ -n "$session_cost" ] && [ "$session_cost" != "0" ]; then
    # Round to 2 decimal places
    session_cost=$(printf "%.2f" "$session_cost" 2>/dev/null || echo "$session_cost")

    # Track month-to-date in persistent file
    cost_file="$HOME/.claude/monthly-costs.json"
    current_month=$(date +%Y-%m)
    session_id=$(json_get "session_id")

    # Simple MTD tracking (just show session cost if file operations fail)
    mtd_cost="$session_cost"
    if [ -f "$cost_file" ] && command -v jq >/dev/null 2>&1; then
        stored_month=$(jq -r '.month // ""' "$cost_file" 2>/dev/null)
        if [ "$stored_month" = "$current_month" ]; then
            mtd_cost=$(jq -r '[.sessions | to_entries[].value] | add | . * 100 | floor / 100' "$cost_file" 2>/dev/null || echo "$session_cost")
        fi
    fi

    cost_display="\$${session_cost} (mtd:\$${mtd_cost})"
fi

# === TURNS ===
user_turns=0
ai_turns=0
compactions=0
transcript_path=$(json_get "transcript_path")
if [ -n "$transcript_path" ] && [ -f "$transcript_path" ]; then
    user_turns=$(grep -c '"type"[[:space:]]*:[[:space:]]*"user"' "$transcript_path" 2>/dev/null || echo 0)
    ai_turns=$(grep -c '"type"[[:space:]]*:[[:space:]]*"assistant"' "$transcript_path" 2>/dev/null || echo 0)
    compactions=$(grep -c '"summary_type"' "$transcript_path" 2>/dev/null || echo 0)
fi

# === LINES CHANGED ===
lines_added=$(json_get_num "total_lines_added")
lines_removed=$(json_get_num "total_lines_removed")

# === GIT INFO ===
repo_name=""
branch=""
modified=0
untracked=0
deleted=0

cwd=$(json_get "cwd")
[ -z "$cwd" ] && cwd=$(echo "$input_json" | grep -o '"current_dir"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"current_dir"[[:space:]]*:[[:space:]]*//' | tr -d '"')

if [ -n "$cwd" ] && [ -d "$cwd" ]; then
    cd "$cwd" 2>/dev/null
    branch=$(git branch --show-current 2>/dev/null)
    if [ -n "$branch" ]; then
        repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
        if [ -n "$repo_root" ]; then
            repo_name=$(basename "$repo_root")
            status_out=$(git status --porcelain 2>/dev/null)
            if [ -n "$status_out" ]; then
                modified=$(echo "$status_out" | grep -c '^.M\|^M\|^.R\|^R' 2>/dev/null || echo 0)
                untracked=$(echo "$status_out" | grep -c '^??' 2>/dev/null || echo 0)
                deleted=$(echo "$status_out" | grep -c '^.D\|^D' 2>/dev/null || echo 0)
            fi
        fi
    fi
fi

# === BUILD STATUS LINE ===
parts=()

# Model
parts+=("$model")

# Git group
if [ -n "$repo_name" ]; then
    git_part="${repo_name}@${branch}"
    changes=""
    [ $modified -gt 0 ] && changes="${modified} mod"
    [ $untracked -gt 0 ] && { [ -n "$changes" ] && changes+=", "; changes+="${untracked} new"; }
    [ $deleted -gt 0 ] && { [ -n "$changes" ] && changes+=", "; changes+="${deleted} del"; }
    [ -n "$changes" ] && git_part+=" [$changes]"
    [ $lines_added -gt 0 ] || [ $lines_removed -gt 0 ] && git_part+=" +${lines_added}/-${lines_removed}"
    parts+=("git: $git_part")
fi

# Session group
session_parts=""
[ -n "$duration" ] && session_parts="$duration"
[ -n "$cost_display" ] && { [ -n "$session_parts" ] && session_parts+=", "; session_parts+="$cost_display"; }
[ $user_turns -gt 0 ] || [ $ai_turns -gt 0 ] && { [ -n "$session_parts" ] && session_parts+=", "; session_parts+="${user_turns} user / ${ai_turns} AI"; }
[ $compactions -gt 0 ] && { [ -n "$session_parts" ] && session_parts+=", "; session_parts+="${compactions} compact"; }
[ -n "$session_parts" ] && parts+=("session: $session_parts")

# Context
parts+=("ctx: $context_left")

# Join with pipes
IFS='|'
echo "${parts[*]}" | sed 's/|/ | /g'
