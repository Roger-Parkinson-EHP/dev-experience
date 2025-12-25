#Requires -Version 5.1
<#
.SYNOPSIS
    Sets up Claude Code configuration via symlinks to dev-experience repository.

.DESCRIPTION
    Creates symlinks from ~/.claude/ to this repository, enabling:
    - Live updates via git pull
    - Shared skills, services, and configuration
    - FedRAMP-compliant MCP servers

.PARAMETER Uninstall
    Remove symlinks and restore to standalone configuration.

.EXAMPLE
    .\setup.ps1
    Sets up symlinks to provision Claude Code.

.EXAMPLE
    .\setup.ps1 -Uninstall
    Removes symlinks created by this script.

.NOTES
    Requires either:
    - Run as Administrator, OR
    - Developer Mode enabled (Settings > Privacy & Security > For Developers)
#>

param(
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"

# Paths
$claudeDir = "$env:USERPROFILE\.claude"
$devExpDir = $PSScriptRoot  # Location of this script (dev-experience root)

# Symlink definitions: [link path, target path]
$symlinks = @(
    @("$claudeDir\services", "$devExpDir\claude-code\agentic-tools"),
    @("$claudeDir\skills", "$devExpDir\claude-code\skills"),
    @("$claudeDir\statusline.ps1", "$devExpDir\claude-code\statusline\statusline.ps1")
)

function Test-AdminOrDevMode {
    # Check if running as admin
    $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

    # Check if Developer Mode is enabled
    $devMode = $false
    try {
        $regPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock"
        $devMode = (Get-ItemProperty -Path $regPath -Name "AllowDevelopmentWithoutDevLicense" -ErrorAction SilentlyContinue).AllowDevelopmentWithoutDevLicense -eq 1
    } catch {}

    return $isAdmin -or $devMode
}

function Remove-Symlinks {
    Write-Host "Removing Claude Code symlinks..." -ForegroundColor Yellow

    foreach ($link in $symlinks) {
        $linkPath = $link[0]
        if (Test-Path $linkPath) {
            $item = Get-Item $linkPath -Force
            if ($item.LinkType -eq "SymbolicLink") {
                Remove-Item $linkPath -Force
                Write-Host "  Removed: $linkPath" -ForegroundColor Green
            } else {
                Write-Host "  Skipped (not a symlink): $linkPath" -ForegroundColor Yellow
            }
        }
    }

    # Remove import line from CLAUDE.md if present
    $claudeMdPath = "$claudeDir\CLAUDE.md"
    $importLine = "@~/.claude/services/CLAUDE.md"
    if (Test-Path $claudeMdPath) {
        $content = Get-Content $claudeMdPath -Raw
        if ($content.Contains($importLine)) {
            $newContent = $content -replace [regex]::Escape("$importLine`n`n"), ""
            $newContent = $newContent -replace [regex]::Escape("$importLine`n"), ""
            $newContent = $newContent -replace [regex]::Escape($importLine), ""
            Set-Content $claudeMdPath -Value $newContent.TrimStart()
            Write-Host "  Removed import from CLAUDE.md" -ForegroundColor Green
        }
    }

    Write-Host "`nSymlinks removed. Claude Code is now standalone." -ForegroundColor Green
}

function Install-Symlinks {
    Write-Host "Setting up Claude Code via symlinks to dev-experience..." -ForegroundColor Cyan
    Write-Host "  Source: $devExpDir" -ForegroundColor Gray
    Write-Host "  Target: $claudeDir" -ForegroundColor Gray
    Write-Host ""

    # Check permissions
    if (-not (Test-AdminOrDevMode)) {
        Write-Host "ERROR: This script requires either:" -ForegroundColor Red
        Write-Host "  - Run PowerShell as Administrator, OR" -ForegroundColor Yellow
        Write-Host "  - Enable Developer Mode (Settings > Privacy & Security > For Developers)" -ForegroundColor Yellow
        exit 1
    }

    # Ensure ~/.claude exists
    if (-not (Test-Path $claudeDir)) {
        New-Item -ItemType Directory -Path $claudeDir | Out-Null
        Write-Host "  Created: $claudeDir" -ForegroundColor Green
    }

    # Create symlinks
    foreach ($link in $symlinks) {
        $linkPath = $link[0]
        $targetPath = $link[1]

        # Remove existing if present
        if (Test-Path $linkPath) {
            Remove-Item $linkPath -Force -Recurse
        }

        # Create symlink
        New-Item -ItemType SymbolicLink -Path $linkPath -Target $targetPath | Out-Null
        Write-Host "  Linked: $linkPath -> $targetPath" -ForegroundColor Green
    }

    # Handle CLAUDE.md (additive import)
    $claudeMdPath = "$claudeDir\CLAUDE.md"
    $importLine = "@~/.claude/services/CLAUDE.md"

    if (Test-Path $claudeMdPath) {
        $content = Get-Content $claudeMdPath -Raw
        if (-not $content.Contains($importLine)) {
            Set-Content $claudeMdPath -Value "$importLine`n`n$content"
            Write-Host "  Added import to existing CLAUDE.md" -ForegroundColor Green
        } else {
            Write-Host "  CLAUDE.md already has import (skipped)" -ForegroundColor Gray
        }
    } else {
        Set-Content $claudeMdPath -Value "$importLine`n"
        Write-Host "  Created CLAUDE.md with import" -ForegroundColor Green
    }

    # Add MCP servers at user scope (idempotent)
    Write-Host "`nConfiguring MCP servers..." -ForegroundColor Cyan

    $mcpServers = @(
        @{
            Name = "gemini-25-pro-fedramp"
            Args = @(
                "--scope", "user",
                "--command", "bunx",
                "--args", "-y vertex-ai-mcp-server",
                "--env", "AI_PROVIDER=vertex",
                "--env", "GOOGLE_CLOUD_PROJECT=licensecorporation-dev",
                "--env", "VERTEX_MODEL_ID=gemini-2.5-pro",
                "--env", "GOOGLE_CLOUD_LOCATION=us-east5",
                "--env", "AI_USE_STREAMING=true"
            )
        },
        @{
            Name = "gemini-3-pro-global"
            Args = @(
                "--scope", "user",
                "--command", "bunx",
                "--args", "-y vertex-ai-mcp-server",
                "--env", "AI_PROVIDER=vertex",
                "--env", "GOOGLE_CLOUD_PROJECT=licensecorporation-dev",
                "--env", "VERTEX_MODEL_ID=gemini-3-pro-preview",
                "--env", "GOOGLE_CLOUD_LOCATION=global",
                "--env", "AI_USE_STREAMING=true"
            )
        },
        @{
            Name = "gemini-3-flash-global"
            Args = @(
                "--scope", "user",
                "--command", "bunx",
                "--args", "-y vertex-ai-mcp-server",
                "--env", "AI_PROVIDER=vertex",
                "--env", "GOOGLE_CLOUD_PROJECT=licensecorporation-dev",
                "--env", "VERTEX_MODEL_ID=gemini-3-flash-preview",
                "--env", "GOOGLE_CLOUD_LOCATION=global",
                "--env", "AI_USE_STREAMING=true"
            )
        }
    )

    foreach ($server in $mcpServers) {
        try {
            $existingCheck = & claude mcp list 2>&1 | Select-String $server.Name
            if ($existingCheck) {
                Write-Host "  $($server.Name): already configured" -ForegroundColor Gray
            } else {
                & claude mcp add $server.Name @($server.Args) 2>&1 | Out-Null
                Write-Host "  $($server.Name): added" -ForegroundColor Green
            }
        } catch {
            Write-Host "  $($server.Name): failed to add (run 'claude mcp add' manually)" -ForegroundColor Yellow
        }
    }

    Write-Host "`n$([char]0x2714) Claude Code configured via symlinks to dev-experience" -ForegroundColor Green
    Write-Host "`nTo update: cd $devExpDir && git pull" -ForegroundColor Cyan
    Write-Host "To uninstall: .\setup.ps1 -Uninstall" -ForegroundColor Cyan
}

# Main
if ($Uninstall) {
    Remove-Symlinks
} else {
    Install-Symlinks
}
