# Windows Setup for Claude Code + Vertex AI

This directory contains scripts to configure Claude Code with FedRAMP-compliant Vertex AI.

## Prerequisites

1. **Google Cloud SDK** - [Install gcloud CLI](https://cloud.google.com/sdk/docs/install)
2. **Claude Code** - `npm install -g @anthropic-ai/claude-code`
3. **GCP Project** with Vertex AI API enabled

## Environment Variables

Add these to your PowerShell profile (`$PROFILE`):

```powershell
# Required: Enable Vertex AI mode
$env:CLAUDE_CODE_USE_VERTEX = "1"

# Required: Your GCP project ID
$env:ANTHROPIC_VERTEX_PROJECT_ID = "<your-gcp-project-id>"

# Required: FedRAMP-eligible region
$env:CLOUD_ML_REGION = "us-east5"
```

### FedRAMP-Eligible Regions

| Region | Compliance |
|--------|------------|
| `us-east5` | FedRAMP High, DoD IL4/IL5 |
| `us-central1` | FedRAMP High |
| `us-west1` | FedRAMP High |

## Authentication

```powershell
# Login to gcloud
gcloud auth login

# Set up Application Default Credentials (ADC)
gcloud auth application-default login

# Verify project
gcloud config set project <your-gcp-project-id>
```

## Validation

Run the validation script to confirm your setup:

```powershell
.\validate-vertex-setup.ps1
```

### Expected Output

```
=== Claude Code Vertex AI Validation ===

Checking environment variables...
  [OK] CLAUDE_CODE_USE_VERTEX = 1
  [OK] ANTHROPIC_VERTEX_PROJECT_ID = <your-gcp-project-id>
  [OK] CLOUD_ML_REGION = us-east5
  [OK] Region is FedRAMP-eligible

Checking gcloud authentication...
  [OK] Logged in as: <your-email>@<your-domain>.com
  [OK] Application Default Credentials exist

Checking Claude Code installation...
  [OK] Claude Code installed: 2.x.x (Claude Code)

=== FedRAMP Compliance Status ===

SUCCESS: Your setup is configured for FedRAMP-compliant Vertex AI!

You are inferencing from:
  - Project: <your-gcp-project-id>
  - Region: us-east5
  - Provider: Google Cloud Vertex AI (FedRAMP High)

All API calls are logged in GCP Cloud Logging for audit compliance.
```

## Compliance Summary

When configured correctly:

- All Claude API calls route through **Google Cloud Vertex AI**
- Data stays within **FedRAMP High** boundary
- No data sent to Anthropic directly
- All requests logged in **GCP Cloud Logging** for audit
- Supports **HIPAA**, **SOC 2**, **PCI-DSS** compliance requirements

## Troubleshooting

### ADC Expired
```powershell
gcloud auth application-default login
```

### Wrong Project
```powershell
gcloud config set project <your-gcp-project-id>
```

### Vertex AI API Not Enabled
```powershell
gcloud services enable aiplatform.googleapis.com
```
