# Vertex AI Model Garden

What's enabled in our FedRAMP data center and how to authenticate.

## Models Enabled (us-east5 - FedRAMP High)

| Model | ID | Provider | Use Case |
|-------|-----|----------|----------|
| **Claude Opus 4.5** | `claude-opus-4-5@20251101` | Anthropic | Complex reasoning, architecture |
| **Claude Sonnet 4.5** | `claude-sonnet-4-5@20251022` | Anthropic | Daily development (default) |
| **Claude Haiku 4.5** | `claude-haiku-4-5@20251001` | Anthropic | Fast tasks, agents |
| Gemini 2.5 Pro | `gemini-2.5-pro` | Google | Alternative reasoning |
| Gemini 2.5 Flash | `gemini-2.5-flash` | Google | Fast alternative |

**Note**: Gemini 3 Preview models are only available in `global` region (not FedRAMP compliant).

## Daily Authentication

Run this **once per day** (or when your session expires):

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev
```

This creates Application Default Credentials (ADC) valid for ~24 hours. Both Claude Code and Gemini CLI use these credentials.

## First-Time Setup

### Windows (PowerShell)

```powershell
# Install gcloud SDK: https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login
gcloud config set project licensecorporation-dev

# Create ADC
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev

# Validate
.\validate-vertex-setup.ps1
```

### macOS / Linux

```bash
# Install gcloud SDK: https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login
gcloud config set project licensecorporation-dev

# Create ADC
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev

# Validate
chmod +x validate-vertex-setup.sh
./validate-vertex-setup.sh
```

## How It Works

```
Your Terminal (VS Code, PowerShell, iTerm, etc.)
        │
        ▼
   Claude Code / Gemini CLI
        │
        ▼
   Application Default Credentials (ADC)
        │
        ▼
   Google Cloud Vertex AI (us-east5)
        │
        ▼
   Model Garden (Claude, Gemini)
```

Any terminal that has access to your ADC can use these models. This works in:
- VS Code integrated terminal
- Windows Terminal / PowerShell
- iTerm2 / Terminal.app (macOS)
- Standard Linux terminals

**Other IDEs**: Cursor, Windsurf, and similar tools may work if they respect ADC, but are not officially tested.

## Compliance

| Standard | Status |
|----------|--------|
| FedRAMP High | ✅ us-east5 region |
| DoD IL4/IL5 | ✅ us-east5 region |
| PCI-DSS | ✅ GCP certified |
| SOC 2 Type II | ✅ GCP certified |

**Data guarantees:**
- All inference within GCP's FedRAMP boundary
- Data **never used for model training** (Google Cloud Terms §17)
- All API calls logged in Cloud Logging for audit
- Data residency: United States only

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ADC expired | `gcloud auth application-default login` |
| Wrong project | `gcloud config set project licensecorporation-dev` |
| API not enabled | `gcloud services enable aiplatform.googleapis.com` |
| Permission denied | Request IAM role: `roles/aiplatform.user` |
| "invalid_rapt" error | Re-run ADC login (security session expired) |

## Validation Scripts

- `validate-vertex-setup.ps1` - Windows (PowerShell)
- `validate-vertex-setup.sh` - macOS/Linux (Shell)

Run these to confirm your setup is correct before starting work.
