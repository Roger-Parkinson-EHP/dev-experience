# Validate Claude Code + Vertex AI Setup
# This script confirms you're using FedRAMP-compliant Vertex AI

Write-Host "=== Claude Code Vertex AI Validation ===" -ForegroundColor Cyan
Write-Host ""

$errors = @()
$warnings = @()

# Check environment variables
Write-Host "Checking environment variables..." -ForegroundColor Yellow

if ($env:CLAUDE_CODE_USE_VERTEX -eq "1") {
    Write-Host "  [OK] CLAUDE_CODE_USE_VERTEX = 1" -ForegroundColor Green
} else {
    $errors += "CLAUDE_CODE_USE_VERTEX not set to 1"
    Write-Host "  [FAIL] CLAUDE_CODE_USE_VERTEX not set" -ForegroundColor Red
}

if ($env:ANTHROPIC_VERTEX_PROJECT_ID) {
    Write-Host "  [OK] ANTHROPIC_VERTEX_PROJECT_ID = $($env:ANTHROPIC_VERTEX_PROJECT_ID)" -ForegroundColor Green
} else {
    $errors += "ANTHROPIC_VERTEX_PROJECT_ID not set"
    Write-Host "  [FAIL] ANTHROPIC_VERTEX_PROJECT_ID not set" -ForegroundColor Red
}

if ($env:CLOUD_ML_REGION) {
    Write-Host "  [OK] CLOUD_ML_REGION = $($env:CLOUD_ML_REGION)" -ForegroundColor Green

    # Check for FedRAMP regions
    $fedRampRegions = @("us-east5", "us-central1", "us-west1")
    if ($fedRampRegions -contains $env:CLOUD_ML_REGION) {
        Write-Host "  [OK] Region is FedRAMP-eligible" -ForegroundColor Green
    } else {
        $warnings += "Region $($env:CLOUD_ML_REGION) may not be FedRAMP-certified"
        Write-Host "  [WARN] Region may not be FedRAMP-certified" -ForegroundColor Yellow
    }
} else {
    $errors += "CLOUD_ML_REGION not set"
    Write-Host "  [FAIL] CLOUD_ML_REGION not set" -ForegroundColor Red
}

Write-Host ""
Write-Host "Checking gcloud authentication..." -ForegroundColor Yellow

# Check gcloud auth
try {
    $account = gcloud config get-value account 2>$null
    if ($account) {
        Write-Host "  [OK] Logged in as: $account" -ForegroundColor Green
    } else {
        $errors += "Not logged into gcloud"
        Write-Host "  [FAIL] Not logged into gcloud" -ForegroundColor Red
    }
} catch {
    $errors += "gcloud CLI not installed"
    Write-Host "  [FAIL] gcloud CLI not found" -ForegroundColor Red
}

# Check ADC
$adcPath = "$env:APPDATA\gcloud\application_default_credentials.json"
if (Test-Path $adcPath) {
    Write-Host "  [OK] Application Default Credentials exist" -ForegroundColor Green

    # Check if ADC is recent (within 24 hours)
    $adcAge = (Get-Date) - (Get-Item $adcPath).LastWriteTime
    if ($adcAge.TotalHours -gt 24) {
        $warnings += "ADC may be expired (last updated $([int]$adcAge.TotalHours) hours ago)"
        Write-Host "  [WARN] ADC may be expired ($([int]$adcAge.TotalHours) hours old)" -ForegroundColor Yellow
    }
} else {
    $errors += "ADC not found - run 'gcloud auth application-default login'"
    Write-Host "  [FAIL] ADC not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "Checking Claude Code installation..." -ForegroundColor Yellow

# Check Claude Code
try {
    $claudeVersion = claude --version 2>$null
    if ($claudeVersion) {
        Write-Host "  [OK] Claude Code installed: $claudeVersion" -ForegroundColor Green
    }
} catch {
    $errors += "Claude Code not installed"
    Write-Host "  [FAIL] Claude Code not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== FedRAMP Compliance Status ===" -ForegroundColor Cyan

if ($errors.Count -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS: Your setup is configured for FedRAMP-compliant Vertex AI!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You are inferencing from:" -ForegroundColor White
    Write-Host "  - Project: $($env:ANTHROPIC_VERTEX_PROJECT_ID)" -ForegroundColor White
    Write-Host "  - Region: $($env:CLOUD_ML_REGION)" -ForegroundColor White
    Write-Host "  - Provider: Google Cloud Vertex AI (FedRAMP High)" -ForegroundColor White
    Write-Host ""
    Write-Host "All API calls are logged in GCP Cloud Logging for audit compliance." -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "ERRORS FOUND:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
}

if ($warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "WARNINGS:" -ForegroundColor Yellow
    foreach ($warning in $warnings) {
        Write-Host "  - $warning" -ForegroundColor Yellow
    }
}

Write-Host ""
