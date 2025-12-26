# Claude Code

Configuration, tools, and skills for Claude Code on Vertex AI.

## Quick Start

### 1. Authenticate (Daily)

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev
```

### 2. Run Claude Code

```bash
claude
```

That's it. Claude Code reads ADC and uses Vertex AI automatically.

## What's Here

| Folder | Purpose |
|--------|---------|
| `agentic-tools/` | Python tools (conversation-search.py) |
| `skills/` | Claude Code skills (post-compact, search-history) |
| `statusline/` | Custom status line scripts |

## Skills

Skills enhance Claude Code's capabilities. Install via the root `setup.ps1`:

| Skill | Description |
|-------|-------------|
| `post-compact` | Recover context after compaction |
| `search-history` | Search JSONL conversation history |

Usage: `/search-history` or `/post-compact` in Claude Code.

## Agentic Tools

```bash
cd agentic-tools

# List recent sessions
python conversation-search.py --list-sessions

# Search for topic
python conversation-search.py "vertex ai" --max 5 --full
```

## Status Line

Shows model, git info, session stats, and context usage:

```
Opus 4.5 | git: lc@main +10/-5 | session: 1h 23m, $4.50 | ctx: 52% left
```

Configured automatically by `setup.ps1`.

## Environment Variables

These are set by the root `setup.ps1`, but for reference:

| Variable | Value | Purpose |
|----------|-------|---------|
| `CLAUDE_CODE_USE_VERTEX` | `1` | Use Vertex AI |
| `CLOUD_ML_REGION` | `us-east5` | FedRAMP region |
| `ANTHROPIC_VERTEX_PROJECT_ID` | `licensecorporation-dev` | GCP project |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid API key" | Run `gcloud auth application-default login` |
| Wrong model | Check `~/.claude/settings.json` |
| 429 rate limit | Request quota increase in GCP Console |
| "invalid_rapt" | Re-authenticate (security session expired) |

## Models Available

See [vertex-ai-model-garden/README.md](../vertex-ai-model-garden/README.md) for full list.

| Model | Use Case |
|-------|----------|
| Claude Opus 4.5 | Complex reasoning, architecture |
| Claude Sonnet 4.5 | Daily development |
| Claude Haiku 4.5 | Fast tasks, agents |
