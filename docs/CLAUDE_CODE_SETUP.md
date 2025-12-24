# Claude Code Setup (Vertex AI)

This project uses Claude Code with Google Cloud Vertex AI authentication.

## Prerequisites

- Google Cloud SDK (`gcloud` CLI)
- Access to `licensecorporation-dev` GCP project
- Vertex AI API enabled

## Environment Variables

Set these in your terminal before running `claude`:

```powershell
# PowerShell
$env:CLAUDE_CODE_USE_VERTEX = "1"
$env:CLOUD_ML_REGION = "global"
```

```bash
# Bash/Git Bash
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
```

## Authentication

### First-Time Setup

1. **Login to GCP**:
   ```bash
   gcloud auth login
   ```

2. **Set project**:
   ```bash
   gcloud config set project licensecorporation-dev
   ```

3. **Create application default credentials**:
   ```bash
   gcloud auth application-default login
   ```

4. **Start Claude Code**:
   ```bash
   claude
   ```

### Verify Setup

Run `/status` in Claude Code to confirm:
```
API provider: Google Vertex AI
GCP project: licensecorporation-dev
```

## Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| GCP Config | `%APPDATA%\gcloud\configurations\config_default` | Project/account settings |
| ADC Credentials | `%APPDATA%\gcloud\application_default_credentials.json` | OAuth tokens |
| Claude Settings | `~\.claude\settings.json` | Model selection |

## Current Configuration

```
[core]
account = roger@licensecorporation.com
project = licensecorporation-dev
```

## Model Selection

The model is set in `~\.claude\settings.json`:

```json
{
  "permissions": {
    "defaultMode": "default"
  },
  "model": "claude-opus-4-5@20251101"
}
```

Available models on Vertex AI:
- `claude-opus-4-5@20251101` (current)
- `claude-sonnet-4@20250514`
- `claude-3-5-haiku@20241022`

## Troubleshooting

### "Invalid API key" Error

This means credentials aren't being picked up. Run:
```bash
gcloud auth application-default login
```

### 429 Rate Limit Errors

Check/increase quotas in GCP Console:
- Navigate to IAM & Admin > Quotas
- Search for "Vertex AI"
- Request increase if needed

### Corporate Environment (Rippling/SentinelOne)

If your corporate tools manage environment variables, you may need to:
1. Set env vars in the terminal session directly
2. Or add them to your shell profile permanently

**PowerShell Profile** (`$PROFILE`):
```powershell
$env:CLAUDE_CODE_USE_VERTEX = "1"
$env:CLOUD_ML_REGION = "global"
```

**Git Bash Profile** (`~/.bashrc`):
```bash
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
```

## Sources

- [Claude Code on Vertex AI - Official Docs](https://code.claude.com/docs/en/google-vertex-ai)
- [Step-by-step Vertex AI Setup Guide](https://medium.com/@dan.avila7/step-by-step-guide-to-connect-claude-code-with-google-cloud-vertex-ai-17e7916e711e)
- [Google Cloud Vertex AI Claude Docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude)
