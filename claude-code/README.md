# Claude Code Configuration & Tools

Tools, skills, and configuration for Claude Code on compliant infrastructure.

## Contents

| Folder | Purpose |
|--------|---------|
| [vertex-ai-model-garden/](vertex-ai-model-garden/) | Setup for FedRAMP-compliant Vertex AI inference |
| [skills/](skills/) | Claude Code skills for context recovery |
| [statusline/](statusline/) | Custom status line configuration |
| [agentic-tools/](agentic-tools/) | Python tools that enhance Claude Code capabilities |

---

## Quick Start

### 1. Vertex AI Setup (Required)

Configure Claude Code to use Anthropic models via Google Cloud:

```bash
# Windows
cd vertex-ai-model-garden/windows
.\validate-vertex-setup.ps1

# macOS/Linux
cd vertex-ai-model-garden/unix
./validate-vertex-setup.sh
```

See [vertex-ai-model-garden/](vertex-ai-model-garden/) for full setup instructions.

### 2. Install Skills (Optional)

Copy skills to your Claude Code skills directory:

```bash
# Windows
cp -r skills/* ~/.claude/skills/

# Verify
claude /skills
```

### 3. Status Line (Optional)

Custom status line showing model, git info, session stats, and context usage:

```powershell
# Windows - copy to Claude config
cp statusline/statusline.ps1 ~/.claude/
```

---

## Agentic Tools

Python utilities that enhance Claude Code's capabilities:

| Tool | Description |
|------|-------------|
| `conversation-search.py` | Search JSONL conversation history |
| `config.py` | Cross-platform configuration for Claude tools |

### Usage

```bash
cd agentic-tools

# List recent sessions
python conversation-search.py --list-sessions

# Search for topic
python conversation-search.py "vertex ai" --max 5 --full
```

---

## Using Other Models in Claude Code

Claude Code can access other AI models via MCP servers, including using them as subagents.

### Vertex AI Model Garden

Your GCP project has access to 200+ models. Key text generation models:

**Google Gemini (Latest)**
| Model | ID | Best For |
|-------|-----|----------|
| Gemini 3 Pro Preview | `gemini-3-pro-preview` | Most powerful agentic/coding |
| Gemini 3 Flash Preview | `gemini-3-flash-preview` | Balanced speed/quality |
| Gemini 2.5 Pro | `gemini-2.5-pro` | GA, code & complex prompts |
| Gemini 2.5 Flash | `gemini-2.5-flash` | GA, reasoning + speed |

**Partner Models (Managed API)**
| Model | ID | Notes |
|-------|-----|-------|
| DeepSeek V3.2 | `deepseek-v3.2` | Strong coding |
| DeepSeek R1 | `deepseek-r1` | Reasoning model |
| Llama 4 | `llama-4` | Meta's latest |
| Codestral 2 | `codestral-2` | Mistral code model |
| Qwen3 Coder | `qwen3-coder` | Code-specialized |
| GPT OSS | `gpt-oss` | OpenAI open weights |

**Note**: Proprietary OpenAI models (GPT-4, o1, o3) are NOT in Model Garden. Use OpenRouter MCP for those.

### MCP Integration Options

| MCP Server | Use Case |
|------------|----------|
| [Vertex AI MCP](https://playbooks.com/mcp/vertex-ai-gemini) | Access Gemini via Vertex (FedRAMP) |
| [PAL MCP](https://github.com/BeehiveInnovations/pal-mcp-server) | Multi-model subagents |
| [OpenRouter MCP](https://playbooks.com/mcp/slyfox1186-openrouter) | 400+ models (including proprietary) |

### Subagents with Different Models

Claude Code subagents can use different models via MCP. Example architecture:

```
Claude Opus 4.5 (orchestrator)
    ├── Gemini 3 Pro subagent (large codebase analysis)
    ├── DeepSeek R1 subagent (complex reasoning)
    └── Gemini 3 Flash subagent (fast tasks)
```

Benefits:
- **Parallel processing**: Multiple models working simultaneously
- **Context isolation**: Subagents have separate context windows
- **Specialization**: Route tasks to best-fit models
- **Cost optimization**: Use cheaper models for simple tasks

### Quick Setup: Gemini via Vertex AI

```bash
# Add Gemini 3 Pro
claude mcp add-json "gemini-3-pro" '{
  "command": "bunx",
  "args": ["-y", "vertex-ai-mcp-server"],
  "env": {
    "GOOGLE_CLOUD_PROJECT": "licensecorporation-dev",
    "VERTEX_MODEL_ID": "gemini-3-pro-preview",
    "GOOGLE_CLOUD_LOCATION": "us-central1"
  }
}'
```

---

## Compliance

All Claude inference through Vertex AI Model Garden:

| Standard | Status |
|----------|--------|
| FedRAMP High | ✅ us-east5 region |
| DoD IL4/IL5 | ✅ us-east5 region |
| HIPAA | ✅ BAA available |
| SOC 2 Type II | ✅ GCP certified |

See [vertex-ai-model-garden/](vertex-ai-model-garden/) for details.
