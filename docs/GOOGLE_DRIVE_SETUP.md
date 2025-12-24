# Google Drive / GCP Integration

This document describes how to access Google Drive files programmatically for test automation.

## rclone Setup

rclone is configured to access Google Drive for downloading test data spreadsheets.

### Installation

rclone was installed via winget:
```bash
winget install Rclone.Rclone --source winget
```

### Configuration

Config file location: `C:\Users\Roger\AppData\Roaming\rclone\rclone.conf`

The `gdrive` remote is configured with OAuth credentials for `roger@licensecorporation.com`.

### Usage

**List files in Drive:**
```bash
rclone lsf gdrive: --max-depth 1
```

**List shared files:**
```bash
rclone lsf gdrive: --drive-shared-with-me
```

**Download a file:**
```bash
rclone copy "gdrive:filename.xlsx" ./local-folder/ --drive-shared-with-me
```

**Refresh test data from spreadsheet:**
```bash
rclone copy "gdrive:Release Test  LC v0.10.0, 0.10.1.xlsx" tests/data/ --drive-shared-with-me
```

### rclone Path

Full path to rclone executable:
```
C:\Users\Roger\AppData\Local\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.72.1-windows-amd64\rclone.exe
```

## Test Data Files

Downloaded from Google Drive and stored in `tests/data/`:

| File | Description |
|------|-------------|
| `Accounts.csv` | Test accounts for DEV/STAGE environments |
| `Addresses.csv` | Test addresses |
| `Addresses_Prod.csv` | Production addresses |
| `Addresses_subway.csv` | Subway location addresses |

## Token Refresh

The OAuth token will automatically refresh. If authentication fails:

1. Run: `rclone authorize "drive"`
2. Complete browser OAuth flow
3. Copy the token JSON to rclone.conf

## Security Notes

- rclone.conf contains OAuth tokens - do not commit to git
- The token has read-only access to Drive (`scope = drive.readonly`)
- Tokens expire but are auto-refreshed using the refresh_token
