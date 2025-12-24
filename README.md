# dev-experience

Developer experience tools for working with Claude Code on compliant infrastructure.

## Purpose

This repo solves three problems:

1. **Onboarding** - Get developers set up with Claude Code + Vertex AI in minutes
2. **Productivity** - Speech-to-text and conversation search for faster coding
3. **Continuity** - Never lose context after compaction or across sessions

```mermaid
flowchart LR
    subgraph "Developer Experience"
        A[New Developer] --> B[validate-vertex-setup.ps1]
        B --> C{Setup Valid?}
        C -->|Yes| D[Start Coding with Claude]
        C -->|No| E[Follow Setup Guide]
        E --> B
    end

    subgraph "Daily Workflow"
        D --> F[WhisperFlow: Speak → Code]
        D --> G[Claude Code: Think → Build]
        G --> H{Context Full?}
        H -->|Compact| I[post-compact skill]
        I --> J[Search History]
        J --> G
    end
```

## Quick Start

### 1. Validate Your Setup

```powershell
.\setup\windows\validate-vertex-setup.ps1
```

```
SUCCESS: Your setup is configured for FedRAMP-compliant Vertex AI!

You are inferencing from:
  - Project: licensecorporation-dev
  - Region: us-east5
  - Provider: Google Cloud Vertex AI (FedRAMP High)
```

### 2. Start WhisperFlow

```powershell
cd whisperflow && pip install -r requirements.txt && python run.py
```

Press `Ctrl+Shift+Space` → Speak → Text appears at cursor.

### 3. Use Claude Code

```bash
claude
```

Skills are automatically available:
- **search-history** - Find past discussions
- **post-compact** - Recover context after compaction

## Architecture

```mermaid
flowchart TB
    subgraph "Your Machine"
        CC[Claude Code CLI]
        WF[WhisperFlow]
        SK[Skills]
        CS[conversation-search.py]
    end

    subgraph "Google Cloud (FedRAMP High)"
        VA[Vertex AI]
        CL[Cloud Logging]
    end

    subgraph "Local Storage"
        JL[JSONL Transcripts]
        CF[~/.whisperflow/config.json]
    end

    CC <-->|API Calls| VA
    VA --> CL
    CC --> JL
    WF --> CC
    SK --> CS
    CS --> JL
    WF --> CF
```

## How Context Recovery Works

When context gets compacted, Claude doesn't just read the summary - it recovers full context:

```mermaid
sequenceDiagram
    participant U as User
    participant C as Claude
    participant S as Search Tool
    participant H as History (JSONL)

    Note over C: Context compacted
    C->>C: See compaction summary
    C->>S: Search recent history
    S->>H: Query JSONL files
    H-->>S: Return matches
    S-->>C: Full context
    C->>U: Continue with understanding
```

**Result**: Within 3-5 tool uses, Claude is fully up to speed on:
- What was being worked on
- Decisions that were made
- Files that were modified
- Problems that remain open

## Components

| Component | Purpose | Usage |
|-----------|---------|-------|
| `validate-vertex-setup.ps1` | Confirm FedRAMP/PCI/DoD compliance | Run once after setup |
| `whisperflow/` | Speech-to-text service | `Ctrl+Shift+Space` to toggle |
| `conversation-search.py` | Search JSONL history | `python conversation-search.py "term"` |
| `skills/search-history/` | Claude auto-searches past | Automatic |
| `skills/post-compact/` | Recover context after compact | Automatic |

## Compliance

Infrastructure handles compliance - you just code:

```mermaid
flowchart LR
    subgraph "Your Code"
        A[Write Code]
    end

    subgraph "Vertex AI Infrastructure"
        B[FedRAMP High]
        C[PCI-DSS]
        D[DoD IL4/IL5]
        E[SOC 2 Type II]
    end

    subgraph "Guarantees"
        F[No Training on Data]
        G[Full Audit Logging]
        H[Your Own GCP Project]
    end

    A --> B & C & D & E
    B & C & D & E --> F & G & H
```

| Framework | Status |
|-----------|--------|
| FedRAMP High | Authorized |
| PCI-DSS | Compliant |
| DoD IL4/IL5 | Eligible (us-east5) |
| SOC 2 Type II | Compliant |
| Data used for training | **Never** |

## Directory Structure

```
dev-experience/
├── setup/
│   └── windows/
│       └── validate-vertex-setup.ps1    # Validate compliance
├── whisperflow/                          # Speech-to-text
│   ├── main.py
│   ├── transcriber.py                   # Whisper integration
│   └── utils/config.py                  # Custom vocabulary
├── services/
│   ├── conversation-search.py           # Search JSONL
│   └── config.py                        # Auto-discovery
├── skills/
│   ├── search-history/                  # Find past discussions
│   │   └── SKILL.md
│   └── post-compact/                    # Context recovery
│       └── SKILL.md
└── docs/
    └── claude-code-vertex-setup.md      # Full setup guide
```

## Custom Vocabulary

WhisperFlow recognizes technical terms via `~/.whisperflow/config.json`:

```json
{
  "custom_vocabulary": "Claude Code, FedRAMP, PCI-DSS, Vertex AI, Bazel, ..."
}
```

Add your project-specific terms for better transcription.

## Contributing

1. Clone the repo
2. Run validation script
3. Test WhisperFlow
4. Test search-history skill
5. Submit PRs for improvements

## Full Setup Guide

See [docs/claude-code-vertex-setup.md](docs/claude-code-vertex-setup.md) for complete installation.

## License

MIT
