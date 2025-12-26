# dev-experience

**License Corporation Developer Experience**

The tools, policies, and infrastructure that enable AI-assisted development while protecting intellectual property.

---

## Vision

> *[To be validated by Jonathan Rose, CEO]*

**The Promise**: If you align with the practices in this repository, you will:

1. **Protect your intellectual property** - FedRAMP infrastructure, no training on your code
2. **Be maximally productive** - AI-assisted development at full speed
3. **Contribute to our culture** - Standards that make everyone better

This repository, combined with [lc](https://github.com/licensecorporation/lc), forms the productivity engine for License Corporation. Together they deliver:

- **AI-assisted development** at full speed, without IP concerns
- **Integrated testing and CI/CD** baked into the workflow
- **Visualization and observability** throughout the development process
- **Controls built in by design** - not bolted on as afterthoughts

**Clone this repo. Follow the practices. You're protected and productive.**

---

## What This Is

This repository provisions developers with compliant AI tools. Clone it, run setup, authenticate, and you're ready to build.

**Key principle**: All AI inference happens via FedRAMP-authorized infrastructure. Your code never trains models. IP is protected by design.

---

## Structure

```
dev-experience/
├── agentic-tools/           # AI-powered development tools
│   ├── claude-code/         # Claude Code (primary tool)
│   ├── gemini-cli/          # Gemini CLI (alternative)
│   ├── pdf-producer/        # Markdown to PDF conversion
│   └── speech-to-text/      # WhisperFlow dictation
│
├── brand/                   # Brand guidelines and assets
│   └── README.md            # Colors, typography, usage
│
├── fedramp-vertex-ai-model-garden/  # What's enabled in us-east5
│   ├── README.md                    # Models, auth, compliance
│   ├── validate-vertex-setup.ps1    # Windows validation
│   └── validate-vertex-setup.sh     # Unix validation
│
├── legal/                   # Policies and agreements
│   ├── AI-POLICY-v2.md      # Current AI development policy
│   └── 250813...AI Policy.* # Legacy policy (superseded)
│
├── setup/                   # Environment provisioning
│   ├── setup.ps1            # Windows setup
│   └── setup.sh             # macOS/Linux setup
│
├── ONBOARDING.md            # New developer orientation
├── CLAUDE.md                # Claude Code project instructions
└── LICENSE                  # Proprietary - License Corporation
```

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/licensecorporation/dev-experience
cd dev-experience
```

### 2. Setup (One-Time)

```bash
# Windows
.\setup\setup.ps1

# macOS/Linux
chmod +x setup/setup.sh && ./setup/setup.sh
```

### 3. Authenticate (Daily)

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev
```

### 4. Start

```bash
claude    # Claude Code
gemini    # Gemini CLI
```

---

## Why FedRAMP?

| Concern | How FedRAMP Solves It |
|---------|----------------------|
| Will AI train on our code? | **No** - contractually prohibited (Google Terms §17) |
| Where does inference happen? | **us-east5** - US soil, FedRAMP High authorized |
| Is there an audit trail? | **Yes** - all API calls logged in Cloud Logging |
| Can we work with federal clients? | **Yes** - FedRAMP High, DoD IL4/IL5 eligible |

No exceptions. No discussions. Inference from FedRAMP = IP protected.

---

## Intellectual Property

**Everything created through this repository is License Corporation intellectual capital.**

| Principle | What It Means |
|-----------|---------------|
| **AI-agnostic ownership** | It doesn't matter which AI assisted. Claude, Gemini, any of them. If it goes through our process, it's ours. |
| **Safe path** | This repository provides the only approved path for AI-assisted development. Use it and you're protected. |
| **Audit trail** | All API calls logged. We can identify who's using what, when. |
| **No leakage** | FedRAMP infrastructure means your code never leaves compliant boundaries, never trains models. |

The dev-experience repository makes you productive AND safe. That's the deal.

---

## Agentic Tools

These tools let you partner with AI to write code:

| Tool | Description |
|------|-------------|
| **Claude Code** | Primary tool. Best-in-class agentic coding. Terminal + IDE integration. |
| **Gemini CLI** | Google's CLI. Gemini 2.5 (FedRAMP) or 3 Preview (global). |
| **PDF Producer** | Markdown to PDF. For legal docs, policies, proposals. |
| **Speech-to-Text** | WhisperFlow. Local dictation, no cloud. |

We use Claude Code because Anthropic is the only tier-1 LLM provider with models in Google's FedRAMP Vertex AI Model Garden.

---

## Legal

By using this repository, you agree to:

1. **AI Policy v2** - [legal/AI-POLICY-v2.md](legal/AI-POLICY-v2.md)
2. **Your employment/contractor agreement** with License Corporation
3. **Confidentiality obligations** per your signed agreements

See [ONBOARDING.md](ONBOARDING.md) for full orientation and [ACCESS-CONTROL.md](ACCESS-CONTROL.md) for team/role permissions.

---

## Contributing

**All changes happen via Pull Request.** No exceptions.

1. Create a branch from `production`
2. Make changes
3. Open a PR
4. Get approval from [CODEOWNERS](.github/CODEOWNERS) (includes @jonsyrose for key files)
5. Merge after approval

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

This repository is the foundation. Changes are reviewed by leadership because they affect everyone.

---

## Questions?

- Slack: #engineering
- Issues: Open in this repo
- Legal: legal@licensecorporation.com
