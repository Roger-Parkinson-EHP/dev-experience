# dev-experience

**The developer toolkit for License Corporation.**

This repository is the single source of truth for AI-assisted development tools. Clone it, run setup, and you're ready to build.

## Why This Exists

We use AI tools (Claude Code, Gemini CLI) to accelerate development while maintaining FedRAMP compliance. This repo:

- **Provisions your environment** with one command
- **Keeps everyone in sync** via symlinks (pull once, update everywhere)
- **Enforces compliance by design** (you can't accidentally use non-compliant tools)
- **Accumulates best practices** as we learn what works

Changes happen via PR. Everyone participates. This is a living document.

---

## Quick Start

```bash
git clone https://github.com/licensecorporation/dev-experience
cd dev-experience

# Windows (PowerShell - requires Developer Mode or Admin)
.\setup.ps1

# macOS / Linux
chmod +x setup.sh && ./setup.sh
```

**Daily authentication** (run once per day):
```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev
```

Then just run `claude` or `gemini` from any terminal.

---

## What's Here

| Folder | Purpose |
|--------|---------|
| [claude-code/](claude-code/) | Claude Code skills, tools, status line |
| [gemini-cli/](gemini-cli/) | Gemini CLI configuration |
| [vertex-ai-model-garden/](vertex-ai-model-garden/) | Models enabled in our FedRAMP data center |
| [speech-to-text/](speech-to-text/) | WhisperFlow dictation (Ctrl+Shift+Space) |

---

## What Setup Does

Creates symlinks from `~/.claude/` to this repo:

| Your ~/.claude/ | Points to | Purpose |
|-----------------|-----------|---------|
| `services/` | `claude-code/agentic-tools/` | Conversation search |
| `skills/` | `claude-code/skills/` | Context recovery skills |
| `statusline.ps1` | `claude-code/statusline/` | Rich status line |

After setup:
- Skills work in any repo
- `git pull` here updates everyone instantly
- No per-project configuration needed

---

## Models Available

See [vertex-ai-model-garden/](vertex-ai-model-garden/) for full details.

| Model | Region | Use Case |
|-------|--------|----------|
| **Claude Opus 4.5** | us-east5 | Complex reasoning, architecture |
| **Claude Sonnet 4.5** | us-east5 | Daily development |
| **Claude Haiku 4.5** | us-east5 | Fast tasks, agents |
| Gemini 2.5 Pro/Flash | us-east5 | FedRAMP alternative |
| Gemini 3 Pro/Flash | global | Preview (not FedRAMP) |

---

## Compliance

All AI inference through Vertex AI:

| Guarantee | Status |
|-----------|--------|
| FedRAMP High | ✅ us-east5 region |
| DoD IL4/IL5 | ✅ us-east5 region |
| PCI-DSS | ✅ GCP certified |
| Data used for training | **Never** (Google Terms §17) |

---

## Documentation

| Document | Purpose |
|----------|---------|
| [AI-POLICY-v2.md](AI-POLICY-v2.md) | Official AI development policy |
| [claude-code/README.md](claude-code/README.md) | Claude Code setup and tools |
| [gemini-cli/README.md](gemini-cli/README.md) | Gemini CLI setup |
| [vertex-ai-model-garden/README.md](vertex-ai-model-garden/README.md) | What's enabled, how to authenticate |

---

## Contributing

1. Create a branch
2. Make your changes
3. Open a PR

CODEOWNERS require approval for critical paths. See [.github/CODEOWNERS](.github/CODEOWNERS).

---

## Questions?

Ask in Slack or open an issue. This repo is meant to evolve with our needs.
