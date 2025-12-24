# Claude Code + Vertex AI Setup (macOS / Linux)

Configure Claude Code to use Anthropic models via Google Cloud Vertex AI Model Garden for FedRAMP-compliant inference.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Your Workstation                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │ Claude Code  │───▶│   gcloud     │───▶│ Application      │  │
│  │   (CLI)      │    │    ADC       │    │ Default Creds    │  │
│  └──────────────┘    └──────────────┘    └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Google Cloud Platform (FedRAMP High)               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Vertex AI Model Garden                       │  │
│  │                   (us-east5)                              │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Claude Models (Anthropic via Model Garden)        │  │  │
│  │  │  • claude-sonnet-4                                 │  │  │
│  │  │  • claude-opus-4                                   │  │  │
│  │  │  • claude-haiku-4                                  │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Project: licensecorporation-dev                                │
│  Region:  us-east5 (DoD IL4/IL5, FedRAMP High)                 │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

| Requirement | Installation |
|-------------|--------------|
| Google Cloud SDK | [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install) |
| Claude Code | `npm install -g @anthropic-ai/claude-code` |
| GCP Access | Request IAM access to `licensecorporation-dev` |

---

## Step 1: GCP Authentication

```bash
# Login with your @licensecorporation.com account
gcloud auth login

# Set the project
gcloud config set project licensecorporation-dev

# Create Application Default Credentials (required for Claude Code)
gcloud auth application-default login
```

---

## Step 2: Environment Variables

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, or `~/.profile`):

```bash
# Vertex AI Model Garden Configuration
export CLAUDE_CODE_USE_VERTEX="1"
export ANTHROPIC_VERTEX_PROJECT_ID="licensecorporation-dev"
export CLOUD_ML_REGION="us-east5"
```

Reload your profile:
```bash
source ~/.bashrc  # or ~/.zshrc
```

---

## Step 3: Validate Setup

```bash
chmod +x validate-vertex-setup.sh
./validate-vertex-setup.sh
```

### Expected Output

```
=== Claude Code Vertex AI Validation ===

Checking environment variables...
  [OK] CLAUDE_CODE_USE_VERTEX = 1
  [OK] ANTHROPIC_VERTEX_PROJECT_ID = licensecorporation-dev
  [OK] CLOUD_ML_REGION = us-east5
  [OK] Region is FedRAMP-eligible

Checking gcloud authentication...
  [OK] Logged in as: <you>@licensecorporation.com
  [OK] Application Default Credentials exist

Checking Claude Code installation...
  [OK] Claude Code installed: 2.x.x (Claude Code)

=== FedRAMP Compliance Status ===

SUCCESS: Your setup is configured for FedRAMP-compliant Vertex AI!

You are inferencing from:
  - Project: licensecorporation-dev
  - Region: us-east5
  - Provider: Google Cloud Vertex AI (FedRAMP High)

All API calls are logged in GCP Cloud Logging for audit compliance.
```

---

## Compliance

| Standard | Status |
|----------|--------|
| FedRAMP High | ✅ us-east5 region |
| DoD IL4/IL5 | ✅ us-east5 region |
| HIPAA | ✅ BAA available |
| SOC 2 Type II | ✅ GCP certified |
| PCI-DSS | ✅ GCP certified |

**Key points:**
- All inference happens within GCP (no data to Anthropic)
- All API calls logged in Cloud Logging for audit
- Data residency: United States only

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ADC expired | `gcloud auth application-default login` |
| Wrong project | `gcloud config set project licensecorporation-dev` |
| API not enabled | `gcloud services enable aiplatform.googleapis.com` |
| Permission denied | Request IAM role: `roles/aiplatform.user` |

---

## macOS-Specific Notes

If using zsh (default on macOS):
```bash
# Add to ~/.zshrc
export CLAUDE_CODE_USE_VERTEX="1"
export ANTHROPIC_VERTEX_PROJECT_ID="licensecorporation-dev"
export CLOUD_ML_REGION="us-east5"
```

## Linux-Specific Notes

For systemd services or cron jobs, ensure environment variables are available:
```bash
# /etc/environment (system-wide)
CLAUDE_CODE_USE_VERTEX="1"
ANTHROPIC_VERTEX_PROJECT_ID="licensecorporation-dev"
CLOUD_ML_REGION="us-east5"
```
