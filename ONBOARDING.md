# Developer Onboarding: Claude Code on FedRAMP Infrastructure

Welcome to License Corporation's AI-assisted development environment.

## What You're Getting

You have access to **Claude Code** - an agentic coding tool that lives in your terminal and understands your entire codebase. It runs on **Google Cloud Vertex AI** in the **us-east5** region, which is:

- **FedRAMP High authorized** - meets federal security requirements
- **DoD IL4/IL5 eligible** - approved for sensitive unclassified data
- **PCI-DSS compliant** - meets payment card industry standards
- **No training on your data** - contractually guaranteed (Google Cloud Terms §17)

This means you can use AI at full speed without IP concerns.

---

## Claude Code Capabilities

### What It Can Do

| Capability | Description |
|------------|-------------|
| **Read your codebase** | Understands project structure, dependencies, patterns |
| **Edit files directly** | Makes changes with visual diffs in your IDE |
| **Run commands** | Executes tests, builds, git operations |
| **Create commits & PRs** | Full git workflow automation |
| **Search the web** | Research docs, APIs, solutions |
| **Connect to tools** | MCP servers for Jira, Google Drive, databases |

### How It Works

```
You (natural language) → Claude Code → Vertex AI (us-east5) → Response
                                              ↓
                                    FedRAMP boundary
                                    Data never leaves US
                                    Never used for training
```

### Example Commands

```bash
# Start Claude Code
claude

# Inside Claude Code:
"Explain how authentication works in this codebase"
"Write tests for the user service"
"Find all API endpoints and document them"
"Create a PR that fixes the login bug"
"Search recent conversations for context on the payment flow"
```

---

## Quick Setup

### 1. Get GCP Access

Request `roles/aiplatform.user` on `licensecorporation-dev` from your admin.

### 2. Clone and Setup

```bash
git clone https://github.com/licensecorporation/dev-experience
cd dev-experience

# Windows
.\setup.ps1

# macOS/Linux
chmod +x setup.sh && ./setup.sh
```

### 3. Authenticate (Daily)

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev
```

### 4. Start Coding

```bash
claude
```

---

## Models Available

All via Vertex AI Model Garden in us-east5:

| Model | Best For |
|-------|----------|
| **Claude Opus 4.5** | Complex architecture, deep reasoning |
| **Claude Sonnet 4.5** | Daily development (default) |
| **Claude Haiku 4.5** | Fast tasks, quick questions |
| Gemini 2.5 Pro | Alternative reasoning |
| Gemini 2.5 Flash | Fast alternative |

---

## Team Collaboration Features

### Shared Skills

After setup, everyone has access to:
- `/search-history` - Search past conversations for context
- `/post-compact` - Recover context after long sessions

### Shared MCP Servers

Configured at user level, available in all projects:
- Gemini 2.5 Pro (FedRAMP)
- Gemini 3 Pro Preview (global)

### Shared Commands

Custom commands in `.claude/commands/` can be committed to git and shared with the team.

---

## IDE Integration

Claude Code works in:
- **VS Code** - Native extension available
- **VS Code Insiders** - Same extension
- **Terminal** - Direct CLI usage
- **JetBrains** - Extension available

The same ADC credentials work everywhere.

---

## What This Replaces

| Old Approach | New Approach |
|--------------|--------------|
| ChatGPT web (data exposure risk) | Claude Code via Vertex AI (FedRAMP) |
| Cursor (cloud risk) | Claude Code (compliant) |
| Manual AI limits (50% rule) | No limits (infrastructure handles compliance) |
| Hoping devs disable training | Contractually guaranteed no training |

---

## Compliance Summary

| Guarantee | How It's Achieved |
|-----------|-------------------|
| Data stays in US | us-east5 region, Assured Workloads |
| No training on data | Google Cloud Terms §17 |
| Audit trail | All API calls logged in Cloud Logging |
| FedRAMP High | Vertex AI P-ATO from FedRAMP Board |

---

## Getting Help

- **This repo**: [dev-experience](https://github.com/licensecorporation/dev-experience)
- **AI Policy**: [AI-POLICY-v2.md](AI-POLICY-v2.md)
- **Slack**: Ask in #engineering
- **Issues**: Open an issue in this repo

---

## First Thing to Try

After setup, run:

```bash
claude
```

Then ask:

> "Read this codebase and tell me what it does. What are the main components?"

Claude Code will explore the project and give you an overview. From there, you can start asking it to help with real work.

---

*This is the start of your AI-assisted development journey at License Corporation.*

**Sources:**
- [Claude Code Overview](https://www.anthropic.com/claude-code)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Google Cloud FedRAMP Compliance](https://cloud.google.com/security/compliance/fedramp)
- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp)
