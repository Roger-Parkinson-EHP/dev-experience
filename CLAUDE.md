# dev-experience

Developer experience tools for Claude Code on compliant infrastructure.

## On Startup

**ALWAYS search recent history at the start of a conversation** to recover context from previous sessions:

```bash
cd C:/Users/Roger/Documents/GitHub/dev-experience/services
python conversation-search.py --list-sessions | head -5
python conversation-search.py "." --max 5 --full
```

This applies whether:
- After `/compact` (you'll see a summary)
- After `/clear` (you'll have no memory)
- Starting fresh on this project

Do this BEFORE responding to the user's first request. It takes 2-3 tool calls and dramatically improves continuity.

## Key Components

| Component | Purpose |
|-----------|---------|
| `skills/post-compact/` | Context recovery after compaction |
| `skills/search-history/` | Search JSONL history |
| `services/conversation-search.py` | The actual search tool |
| `whisperflow/` | Speech-to-text service |

## Search Tool

```bash
cd C:/Users/Roger/Documents/GitHub/dev-experience/services
python conversation-search.py "search term"           # Basic search
python conversation-search.py --list-sessions         # List all sessions
python conversation-search.py "topic" --max 5 --full  # Full context
```

## Compliance

All Claude API calls go through Vertex AI:
- FedRAMP High authorized
- PCI-DSS compliant
- DoD IL4/IL5 eligible (us-east5)
- Data never used for training
