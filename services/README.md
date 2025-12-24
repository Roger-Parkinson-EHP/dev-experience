# Conversation Services

Search Claude Code conversation history efficiently.

## conversation-search.py

Search JSONL conversation history with regex support. Runs externally to save context tokens.

```bash
# List all sessions
python conversation-search.py --list-sessions

# Search across all sessions
python conversation-search.py "search term"

# Search with regex
python conversation-search.py "context.*percent|usage.*%"

# Limit to specific session
python conversation-search.py "bulk upload" --session 6cabef43

# Get more context (messages before/after)
python conversation-search.py "error" --context 5 --verbose

# Show full message content
python conversation-search.py "statusline" --full --max 1
```

## Options

| Flag | Description |
|------|-------------|
| `--list-sessions`, `-l` | List all sessions with metadata |
| `--session`, `-s` | Filter to specific session ID (partial match) |
| `--context`, `-c` | Number of context messages (default: 3) |
| `--max`, `-m` | Maximum results (default: 20) |
| `--verbose`, `-v` | Show context messages |
| `--full`, `-f` | Show full message content |

## Configuration

Uses `config.py` for shared configuration:

- **Auto-discovers repos** from `~/Documents/GitHub/`
- **Auto-discovers Claude projects** from `~/.claude/projects/`
- **Cross-platform** - Works on Windows, Linux, WSL

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECTS` | Override Claude projects path |
| `GITHUB_REPOS` | Override GitHub repos path |

## Token-Efficient Searching

The search runs outside Claude's context window:

| Approach | Token Cost |
|----------|------------|
| Read full JSONL (6MB) | ~1.5M tokens (impossible) |
| Search externally | 0 tokens |
| Return 3 previews | ~300 tokens |
| Return 1 full message | ~1500 tokens |

Search first, then fetch only what you need.
