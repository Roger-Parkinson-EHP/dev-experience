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

Claude Code can access other AI models (Gemini, GPT, etc.) via MCP servers:

### Available MCP Integrations

| MCP Server | Models Supported |
|------------|------------------|
| [Zen MCP](https://claudelog.com/claude-code-mcps/zen-mcp-server/) | Gemini Pro, OpenAI O3, Grok |
| [OpenRouter MCP](https://playbooks.com/mcp/slyfox1186-openrouter) | 400+ models including GPT-4, Gemini |
| [PAL MCP](https://www.xugj520.cn/en/archives/pal-mcp-guide-orchestrate-ai-models.html) | OpenAI, Google, Azure, Ollama |

### Example: Add Gemini to Claude Code

```bash
npm install -g gemini-mcp-tool
claude mcp add -s local gemini-cli -- npx -y gemini-mcp-tool
```

### Why Multi-Model?

- **Backup**: When Claude hits rate limits, use Gemini or GPT
- **Specialization**: Use Gemini's large context for big codebases
- **Cost**: Route simple tasks to cheaper models

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
