# License Corporation Claude Code Instructions

This file is imported by all License Corp developers' Claude Code instances.
Changes here apply to everyone after they run `git pull` in dev-experience.

## On Startup / After Clear or Compact

**ALWAYS search recent conversation history** at the start of any session to recover context from previous work:

```bash
cd ~/.claude/services
python conversation-search.py --list-sessions | head -5
python conversation-search.py "TOPIC" --max 3 --full
```

Replace "TOPIC" with keywords from the user's first message or the current project name.

## CRITICAL: This Is Your FIRST Action

**Before responding to the user's first message - even if it's just "hello" - you MUST:**

1. Run `--list-sessions` to see recent work
2. Search for relevant context based on the project or user's message
3. ONLY THEN respond with recovered context

Do NOT skip this step. Do NOT just say "Hello! How can I help you?" without searching first.

## Why This Matters

Context compaction and `/clear` commands remove valuable conversation history. Before responding to the user, recover:
- What was being worked on
- Decisions that were made
- Open issues or next steps

## Available Skills

- **search-history**: Search JSONL conversation history
- **post-compact**: Detailed context recovery after compaction

## Compliance

All AI inference goes through FedRAMP-authorized infrastructure:
- **Claude**: Vertex AI Model Garden (us-east5)
- **Gemini 2.5**: Vertex AI (us-east5) - FedRAMP High
- **Gemini 3**: Vertex AI (global) - IP-safe, no training

See [dev-experience](https://github.com/licensecorporation/dev-experience) for configuration and setup.

## MCP Servers Available

| Server | Model | Region | Use |
|--------|-------|--------|-----|
| `gemini-25-pro-fedramp` | Gemini 2.5 Pro | us-east5 | FedRAMP-compliant tasks |
| `gemini-3-pro-global` | Gemini 3 Pro Preview | global | Advanced reasoning |
| `gemini-3-flash-global` | Gemini 3 Flash Preview | global | Fast tasks |
