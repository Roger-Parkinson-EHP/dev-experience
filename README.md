# dev-experience

Developer experience tools for working with Claude Code on FedRAMP-compliant infrastructure.

## What's This?

This repo helps you:
1. **Set up Claude Code** with Vertex AI (FedRAMP High compliant)
2. **Use WhisperFlow** for speech-to-text while coding
3. **Search conversation history** to find past solutions

## Quick Start

### 1. Validate Your Setup

```powershell
# Windows
.\setup\windows\validate-vertex-setup.ps1
```

Expected output:
```
SUCCESS: Your setup is configured for FedRAMP-compliant Vertex AI!

You are inferencing from:
  - Project: licensecorporation-dev
  - Region: us-east5
  - Provider: Google Cloud Vertex AI (FedRAMP High)
```

### 2. Start WhisperFlow (Speech-to-Text)

```powershell
cd whisperflow
pip install -r requirements.txt
python run.py
```

**Usage**: Press `Ctrl+Shift+Space` to start recording, speak, press again to stop. Text is pasted to cursor.

### 3. Search Conversation History

```bash
cd services
python conversation-search.py "search term"
python conversation-search.py --list-sessions
```

## Compliance Built-In

By using Claude Code with Vertex AI, compliance is automatic - not a blocker:

| Framework | Status |
|-----------|--------|
| FedRAMP High | Authorized |
| PCI-DSS | Compliant infrastructure |
| DoD IL4/IL5 | Eligible (us-east5 region) |
| SOC 2 Type II | Compliant |
| Data used for training | Never |
| Audit logging | GCP Cloud Logging |

You're running on **your own GCP project** with full audit trail. Just write code - compliance is handled by the infrastructure.

## Directory Structure

```
dev-experience/
├── setup/
│   └── windows/
│       └── validate-vertex-setup.ps1    # Validate your setup
├── whisperflow/                          # Speech-to-text service
├── services/
│   └── conversation-search.py           # Search JSONL history
├── skills/
│   └── search-history/                  # Claude Code skill
└── docs/
    └── claude-code-vertex-setup.md      # Full setup guide
```

## Need Full Setup?

See [docs/claude-code-vertex-setup.md](docs/claude-code-vertex-setup.md) for complete installation instructions.

## Custom Vocabulary (WhisperFlow)

WhisperFlow uses a custom vocabulary to correctly recognize technical terms. Edit `~/.whisperflow/config.json`:

```json
{
  "custom_vocabulary": "Claude Code, FedRAMP, HIPAA, Vertex AI, ..."
}
```

## Requirements

- Python 3.10+
- Claude Code CLI
- GCP account with Vertex AI access

## License

MIT
