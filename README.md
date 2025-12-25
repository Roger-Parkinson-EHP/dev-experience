# dev-experience

Developer experience tools for working with Claude Code on compliant infrastructure.

## Quick Start

Clone and run setup to provision your Claude Code environment:

```bash
git clone https://github.com/licensecorporation/dev-experience
cd dev-experience

# Windows (PowerShell as Admin or Developer Mode enabled)
.\setup.ps1

# macOS / Linux
chmod +x setup.sh && ./setup.sh
```

This creates symlinks from `~/.claude/` to this repository, so:
- **Skills** are automatically available (`/search-history`, `/post-compact`)
- **Services** (conversation search) are accessible from any repo
- **MCP servers** for Gemini are configured
- **Updates apply instantly** with `git pull`

## What Gets Configured

| Your ~/.claude/ | Linked to | Purpose |
|-----------------|-----------|---------|
| `services/` | `claude-code/agentic-tools/` | Conversation search tool |
| `skills/` | `claude-code/skills/` | post-compact, search-history |
| `statusline.ps1` or `.sh` | `claude-code/statusline/` | Custom status line |
| `CLAUDE.md` | Imports shared instructions | Startup guidance |

## Components

| Folder | Purpose |
|--------|---------|
| [claude-code/](claude-code/) | Claude Code skills, tools, and configuration |
| [speech-to-text/](speech-to-text/) | WhisperFlow dictation service |

## How It Works

```
~/.claude/                          This Repository
├── services/ ──── symlink ────►    claude-code/agentic-tools/
├── skills/ ────── symlink ────►    claude-code/skills/
└── CLAUDE.md ──── imports ────►    claude-code/agentic-tools/CLAUDE.md

After setup:
- Open any repo with Claude Code
- Skills work automatically
- `git pull` in dev-experience updates everyone instantly
```

## Compliance

All AI inference goes through FedRAMP-authorized infrastructure:

| Standard | Status |
|----------|--------|
| FedRAMP High | Authorized (us-east5) |
| PCI-DSS | Compliant |
| DoD IL4/IL5 | Eligible (us-east5) |
| Data used for training | **Never** |

## Available Skills

After setup, these skills are available in Claude Code:

- **`/search-history`** - Search past conversations for context
- **`/post-compact`** - Recover full context after compaction

## MCP Servers Configured

| Server | Model | Region | Use |
|--------|-------|--------|-----|
| `gemini-25-pro-fedramp` | Gemini 2.5 Pro | us-east5 | FedRAMP-compliant |
| `gemini-3-pro-global` | Gemini 3 Pro Preview | global | Advanced reasoning |
| `gemini-3-flash-global` | Gemini 3 Flash Preview | global | Fast tasks |

## Updating

Pull latest and the symlinks automatically use new content:

```bash
cd ~/Documents/GitHub/dev-experience
git pull
```

## Uninstalling

Remove symlinks and restore standalone Claude Code:

```bash
# Windows
.\setup.ps1 -Uninstall

# macOS / Linux
./setup.sh uninstall
```

## Full Documentation

- [Claude Code Setup](claude-code/README.md)
- [Vertex AI Configuration](claude-code/vertex-ai-model-garden/README.md)
- [AI Policy v2](AI-POLICY-v2.md)

## License

MIT
