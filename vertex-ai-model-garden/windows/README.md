# Vertex AI Model Garden Setup (Windows)

Configure Claude Code and Gemini CLI to use Vertex AI for compliant inference.

## Available Models (us-east5 - FedRAMP High)

| Model | ID | Use Case |
|-------|----|----|
| **Claude Opus 4.5** | `claude-opus-4-5@20251101` | Complex reasoning, architecture |
| **Claude Sonnet 4.5** | `claude-sonnet-4-5@20251022` | Daily development |
| **Claude Haiku 4.5** | `claude-haiku-4-5@20251001` | Fast tasks, agents |
| Gemini 2.5 Pro | `gemini-2.5-pro` | Alternative reasoning |
| Gemini 2.5 Flash | `gemini-2.5-flash` | Fast alternative |

**Note**: Gemini 3 Preview is only available in `global` region (not FedRAMP).

## Prerequisites

| Requirement | Installation |
|-------------|--------------|
| Google Cloud SDK | [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install) |
| Claude Code | `npm install -g @anthropic-ai/claude-code` |
| GCP Access | Request IAM access to `licensecorporation-dev` |

---

## Daily Authentication

Run this **once per day** (or when ADC expires):

```powershell
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev
```

This creates Application Default Credentials (ADC) that both Claude Code and Gemini CLI use. Valid for ~24 hours.

## First-Time Setup

```powershell
# Login with your @licensecorporation.com account
gcloud auth login

# Set the project
gcloud config set project licensecorporation-dev

# Create ADC
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev
```

---

## Step 2: Environment Variables

Add to your PowerShell profile (`notepad $PROFILE`):

```powershell
# Vertex AI Model Garden Configuration
$env:CLAUDE_CODE_USE_VERTEX = "1"
$env:ANTHROPIC_VERTEX_PROJECT_ID = "licensecorporation-dev"
$env:CLOUD_ML_REGION = "us-east5"
```

Reload your profile:
```powershell
. $PROFILE
```

---

## Step 3: Validate Setup

```powershell
.\validate-vertex-setup.ps1
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
| PCI-DSS | ✅ GCP certified |
| SOC 2 Type II | ✅ GCP certified |

**Key points:**
- All inference happens within GCP's FedRAMP boundary
- Data is **never used for model training** (Google Cloud Terms §17)
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
