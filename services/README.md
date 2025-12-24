# Platform Services

Cross-platform utilities for Claude Code conversation management.

## Tools

### conversation-search.py
Search Claude JSONL conversation history with regex support.

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

**Options:**
| Flag | Description |
|------|-------------|
| `--list-sessions`, `-l` | List all sessions with metadata |
| `--session`, `-s` | Filter to specific session ID (partial match) |
| `--context`, `-c` | Number of context messages (default: 3) |
| `--max`, `-m` | Maximum results (default: 20) |
| `--verbose`, `-v` | Show context messages |
| `--full`, `-f` | Show full message content |

### conversation-indexer.py
Index Claude conversations into markdown files with YAML summaries.

```bash
# One-time index
python conversation-indexer.py --once

# Watch mode (continuous)
python conversation-indexer.py

# Index specific repo
python conversation-indexer.py --repo bazel-test
```

**Output structure:**
```
repo/AI_Interaction/
├── 2025-12-24/
│   ├── data/
│   │   ├── 091603_Roger_topic-summary.md
│   │   └── 094728_Agent_another-topic.md
│   └── 2025-12-24_Index.yaml
```

### indexer-watch.py
Daemon that watches for new conversations and indexes automatically.

```bash
python indexer-watch.py
```

### daily-dashboard.py
Generate matplotlib dashboards of conversation activity.

```bash
python daily-dashboard.py
python daily-dashboard.py --days 7
```

### daily-summary.py
Generate daily YAML summaries of conversation activity.

```bash
python daily-summary.py
python daily-summary.py --date 2025-12-23
```

## Configuration

All tools use `config.py` for shared configuration:

- **Auto-discovers repos** from `~/Documents/GitHub/`
- **Auto-discovers Claude projects** from `~/.claude/projects/`
- **Cross-platform** - Works on Windows, Linux, WSL

### Environment Variables
| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECTS` | Override Claude projects path |
| `GITHUB_REPOS` | Override GitHub repos path |

## Requirements

```bash
pip install pyyaml matplotlib
```

## Token-Efficient Searching

The search tool runs outside Claude's context window:

| Approach | Token Cost |
|----------|------------|
| Read full JSONL (6MB) | ~1.5M tokens (impossible) |
| Search externally | 0 tokens |
| Return 3 previews | ~300 tokens |
| Return 1 full message | ~1500 tokens |

Use search to filter first, then fetch only what you need.
