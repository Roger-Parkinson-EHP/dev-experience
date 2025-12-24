# DevTools

Developer tools and configuration for Claude Code, speech-to-text, and AI-assisted development.

## What's Included

### WhisperFlow
Local speech-to-text using OpenAI Whisper. Press a hotkey, speak, and text is pasted to cursor.

```bash
cd whisperflow
pip install -r requirements.txt
python -m whisperflow
```

### Claude Code Skills
Custom skills for Claude Code that extend its capabilities.

- **search-history**: Search conversation history from JSONL files
- Copy to `~/.claude/skills/` to activate

### Claude Code Setup
Scripts and documentation for setting up Claude Code with Vertex AI.

- GCP project configuration
- Environment variables (Windows/Mac/Linux)
- API quota setup

### Conversation Services
Tools for managing Claude conversation history.

- **conversation-search**: Search JSONL transcripts
- **conversation-indexer**: Generate markdown summaries
- **daily-dashboard**: Visualize usage patterns

## Quick Start

### Windows
```powershell
# 1. Clone this repo
git clone https://github.com/yourorg/DevTools.git

# 2. Run setup script
.\setup\windows\setup-claude-code.ps1

# 3. Install WhisperFlow
cd whisperflow
pip install -r requirements.txt
```

### Mac/Linux
```bash
# 1. Clone this repo
git clone https://github.com/yourorg/DevTools.git

# 2. Run setup script
./setup/unix/setup-claude-code.sh

# 3. Install WhisperFlow
cd whisperflow
pip install -r requirements.txt
```

## Directory Structure

```
DevTools/
├── whisperflow/           # Speech-to-text application
├── skills/                # Claude Code custom skills
├── services/              # Conversation indexing/search
├── setup/
│   ├── windows/           # Windows setup scripts
│   └── unix/              # Mac/Linux setup scripts
└── docs/
    ├── claude-code-setup.md
    ├── vertex-ai-setup.md
    └── environment-variables.md
```

## Requirements

- Python 3.10+
- Claude Code CLI
- GCP account (for Vertex AI)
