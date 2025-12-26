# Gemini CLI Configuration

Gemini CLI is an alternative to Claude Code for AI-assisted development. This configuration enables Vertex AI authentication with Gemini 3 Preview models.

## Quick Setup

1. **Install Gemini CLI**
   ```bash
   npm install -g @anthropic/gemini-cli
   ```

2. **Ensure ADC is configured**
   ```powershell
   gcloud auth application-default login
   gcloud auth application-default set-quota-project licensecorporation-dev
   ```

3. **Copy configuration files**
   ```powershell
   # Create .gemini directory
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini"

   # Copy settings
   Copy-Item "settings.json" "$env:USERPROFILE\.gemini\settings.json"
   Copy-Item ".env" "$env:USERPROFILE\.gemini\.env"
   Copy-Item "GEMINI.md" "$env:USERPROFILE\.gemini\GEMINI.md"
   ```

4. **Add to PowerShell profile**
   ```powershell
   # Add these lines to $PROFILE
   $env:GOOGLE_CLOUD_PROJECT = "licensecorporation-dev"
   $env:GOOGLE_CLOUD_LOCATION = "global"
   Remove-Item Env:GOOGLE_API_KEY -ErrorAction SilentlyContinue
   Remove-Item Env:GEMINI_API_KEY -ErrorAction SilentlyContinue
   ```

## Configuration Files

| File | Purpose |
|------|---------|
| `settings.json` | Gemini CLI settings (auth type, UI preferences) |
| `.env` | Environment variables (project, location) |
| `GEMINI.md` | Global instructions for Gemini |

## Regions

| Region | Models | Compliance |
|--------|--------|------------|
| `global` | Gemini 3 Pro/Flash Preview, Gemini 2.5 | IP-safe (no training) |
| `us-east5` | Gemini 2.5 only | FedRAMP High |

Default is `global` for Gemini 3 access. Change to `us-east5` for FedRAMP compliance.

## Usage

```powershell
# Start Gemini CLI
gemini

# Select model with /model command
# Enable preview features in /settings for Gemini 3
```

## Comparison with Claude Code

| Feature | Claude Code | Gemini CLI |
|---------|-------------|------------|
| Primary model | Claude Opus 4.5 | Gemini 3 Pro/Flash |
| FedRAMP | Yes (us-east5) | No (use us-east5 for 2.5) |
| Skills | Yes (~/.claude/skills/) | No |
| MCP Servers | Yes | Limited |
| Context recovery | Yes (conversation-search) | No |

Use Claude Code for FedRAMP-compliant work. Use Gemini CLI for quick tasks with Gemini 3.
