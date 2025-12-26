# Claude Code + Vertex AI Setup Guide

This guide will help you set up Claude Code to use Claude Opus 4.5 via Google Cloud Vertex AI (FedRAMP compliant).

## Prerequisites

1. **Google Cloud Account** - You need access to the `licensecorporation-dev` GCP project
2. **IAM Permissions** - Your account needs the `Vertex AI User` role (or equivalent)
3. **Node.js** - Version 18+ required for Claude Code
4. **gcloud CLI** - Google Cloud SDK installed

## Step 1: Install Google Cloud CLI

If not already installed:

**Windows (PowerShell as Admin):**
```powershell
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:TEMP\GoogleCloudSDKInstaller.exe")
& "$env:TEMP\GoogleCloudSDKInstaller.exe"
```

**Or download from:** https://cloud.google.com/sdk/docs/install

## Step 2: Authenticate with Google Cloud

Open a terminal and run:

```bash
# Login to Google Cloud
gcloud auth login

# Set the project
gcloud config set project licensecorporation-dev

# Verify your account
gcloud auth list
```

You should see your `@licensecorporation.com` account marked as active.

## Step 3: Set Up Application Default Credentials (ADC)

This is the critical step that allows Claude Code to authenticate:

```bash
# Create Application Default Credentials
gcloud auth application-default login

# Set the quota project (for billing)
gcloud auth application-default set-quota-project licensecorporation-dev
```

A browser window will open - complete the OAuth flow with your work account.

## Step 4: Install Claude Code

**Windows (PowerShell):**
```powershell
npm install -g @anthropic-ai/claude-code
```

**Or using the installer:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

Verify installation:
```bash
claude --version
```

## Step 5: Configure Environment Variables

Add these to your shell profile or system environment variables:

**Windows (PowerShell - add to $PROFILE):**
```powershell
$env:CLAUDE_CODE_USE_VERTEX = "1"
$env:CLOUD_ML_REGION = "us-east5"
$env:ANTHROPIC_VERTEX_PROJECT_ID = "licensecorporation-dev"
```

**To make permanent (System Environment Variables):**
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to **Advanced** tab → **Environment Variables**
3. Under **User variables**, add:
   - `CLAUDE_CODE_USE_VERTEX` = `1`
   - `CLOUD_ML_REGION` = `us-east5`
   - `ANTHROPIC_VERTEX_PROJECT_ID` = `licensecorporation-dev`

**Or via PowerShell (permanent):**
```powershell
[Environment]::SetEnvironmentVariable("CLAUDE_CODE_USE_VERTEX", "1", "User")
[Environment]::SetEnvironmentVariable("CLOUD_ML_REGION", "us-east5", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_VERTEX_PROJECT_ID", "licensecorporation-dev", "User")
```

## Step 6: Configure Claude Code Model

Set the model to Opus 4.5:

```bash
claude config set model claude-opus-4-5@20251101
```

Or edit `~/.claude/settings.json`:
```json
{
  "model": "claude-opus-4-5@20251101"
}
```

## Step 7: Test the Setup

```bash
claude
```

Type `hi` - if you get a response, you're connected to Vertex AI!

## Troubleshooting

### Error: `invalid_grant` or `invalid_rapt`

Your ADC token expired. Refresh it:

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev
```

### Error: `Permission denied` or `403`

Your account may not have Vertex AI permissions. Contact your GCP admin to add:
- `roles/aiplatform.user` (Vertex AI User)

### Error: `Could not find project`

Ensure environment variables are set correctly:
```bash
echo $ANTHROPIC_VERTEX_PROJECT_ID
```

Should output: `licensecorporation-dev`

### Claude Code not using Vertex

Verify the environment variable:
```bash
echo $CLAUDE_CODE_USE_VERTEX
```

Should output: `1`

## Quick Reference

| Variable | Value |
|----------|-------|
| `CLAUDE_CODE_USE_VERTEX` | `1` |
| `CLOUD_ML_REGION` | `us-east5` |
| `ANTHROPIC_VERTEX_PROJECT_ID` | `licensecorporation-dev` |
| Model | `claude-opus-4-5@20251101` |

## IAM Permissions Required

The user's Google Cloud account needs:
- `roles/aiplatform.user` - To invoke Vertex AI models
- Access to the `licensecorporation-dev` project

## Security Notes

- ADC credentials are stored locally at `~/.config/gcloud/application_default_credentials.json`
- Tokens expire periodically (based on org security policy)
- Never share your ADC credentials file
- All API calls are logged in GCP Cloud Logging

---

*Last updated: December 2025*
