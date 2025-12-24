# Claude Code Status Line Script

$input_json = [Console]::In.ReadToEnd()

# Clean input (remove BOM if present)
$input_json = $input_json -replace '^\xEF\xBB\xBF', '' -replace '^\uFEFF', ''

try {
    $data = $input_json | ConvertFrom-Json

    # === MODEL ===
    $model = if ($data.model.display_name) { $data.model.display_name } else { "Claude" }

    # === CONTEXT ===
    # Show % REMAINING (to match Claude Code's display)
    $contextLeft = "100%"
    $cw = $data.context_window
    if ($cw -and $cw.context_window_size -gt 0) {
        $used = 0
        if ($cw.current_usage) {
            $cu = $cw.current_usage
            # Context = input_tokens + cache_read + cache_creation (NOT output_tokens)
            $used = [int]$cu.input_tokens +
                    [int]$cu.cache_creation_input_tokens +
                    [int]$cu.cache_read_input_tokens
        }
        # Usable context is ~195K (200K minus small buffer)
        $usableContext = 195000
        $remaining = $usableContext - $used
        if ($remaining -lt 0) { $remaining = 0 }
        $pct = [math]::Round(($remaining / $usableContext) * 100)
        $contextLeft = "${pct}% left"
    }

    # === SESSION INFO ===
    $duration = ""
    if ($data.cost.total_duration_ms) {
        $ms = [long]$data.cost.total_duration_ms
        $totalMins = [math]::Floor($ms / 60000)
        $hours = [math]::Floor($totalMins / 60)
        $mins = $totalMins % 60
        if ($hours -gt 0) {
            $duration = "${hours}h ${mins}m"
        } else {
            $duration = "${mins}m"
        }
    }

    # Cost tracking - session and month-to-date
    $sessionCost = 0
    $mtdCost = 0
    $costDisplay = ""

    if ($data.cost.total_cost_usd) {
        $sessionCost = [math]::Round($data.cost.total_cost_usd, 2)

        # Track month-to-date in persistent file
        $costFile = "$env:USERPROFILE\.claude\monthly-costs.json"
        $currentMonth = Get-Date -Format "yyyy-MM"

        try {
            if (Test-Path $costFile) {
                $costData = Get-Content $costFile -Raw | ConvertFrom-Json
            } else {
                $costData = @{ month = $currentMonth; sessions = @{} }
            }

            # Reset if new month
            if ($costData.month -ne $currentMonth) {
                $costData = @{ month = $currentMonth; sessions = @{} }
            }

            # Update this session's cost
            $sessionId = $data.session_id
            if ($sessionId) {
                $costData.sessions[$sessionId] = $sessionCost
            }

            # Calculate MTD total
            $mtdCost = 0
            foreach ($s in $costData.sessions.PSObject.Properties) {
                $mtdCost += $s.Value
            }
            $mtdCost = [math]::Round($mtdCost, 2)

            # Save updated costs
            $costData | ConvertTo-Json | Set-Content $costFile -Encoding UTF8
        } catch {
            $mtdCost = $sessionCost
        }

        $costDisplay = "`$${sessionCost} (mtd:`$${mtdCost})"
    }

    # Turns and compactions from transcript
    $userTurns = 0
    $aiTurns = 0
    $compactions = 0
    if ($data.transcript_path -and (Test-Path $data.transcript_path)) {
        try {
            $lines = Get-Content $data.transcript_path -ErrorAction SilentlyContinue
            $userTurns = ($lines | Where-Object { $_ -match '"type"\s*:\s*"user"' }).Count
            $aiTurns = ($lines | Where-Object { $_ -match '"type"\s*:\s*"assistant"' }).Count
            # Count compaction events (look for summary messages after compaction)
            $compactions = ($lines | Where-Object { $_ -match '"summary_type"' }).Count
        } catch {}
    }

    # Lines changed (for git section)
    $linesAdded = [int]$data.cost.total_lines_added
    $linesRemoved = [int]$data.cost.total_lines_removed

    # === GIT INFO ===
    $repoName = ""
    $branch = ""
    $modified = 0
    $untracked = 0
    $deleted = 0
    $cwd = if ($data.cwd) { $data.cwd } else { $data.workspace.current_dir }

    if ($cwd) {
        Push-Location $cwd
        try {
            $branchName = git branch --show-current 2>$null
            if ($branchName) {
                $branch = $branchName
                $repoRoot = git rev-parse --show-toplevel 2>$null
                if ($repoRoot) {
                    $repoName = Split-Path $repoRoot -Leaf
                    $statusOut = git status --porcelain 2>$null
                    if ($statusOut) {
                        $statusLines = $statusOut -split "`n" | Where-Object { $_ }
                        $modified = ($statusLines | Where-Object { $_ -match '^ M|^M|^ R|^R' }).Count
                        $untracked = ($statusLines | Where-Object { $_ -match '^\?\?' }).Count
                        $deleted = ($statusLines | Where-Object { $_ -match '^ D|^D' }).Count
                    }
                }
            }
        } catch {}
        Pop-Location
    }

    # === BUILD STATUS LINE ===
    $parts = @()

    # Model
    $parts += $model

    # Git group: repo@branch [changes] +lines/-lines
    if ($repoName) {
        $gitParts = @("${repoName}@${branch}")
        $changes = @()
        if ($modified -gt 0) { $changes += "${modified} mod" }
        if ($untracked -gt 0) { $changes += "${untracked} new" }
        if ($deleted -gt 0) { $changes += "${deleted} del" }
        if ($changes) { $gitParts += "[" + ($changes -join ", ") + "]" }
        if ($linesAdded -gt 0 -or $linesRemoved -gt 0) {
            $gitParts += "+${linesAdded}/-${linesRemoved}"
        }
        $parts += "git: " + ($gitParts -join " ")
    }

    # Session group: duration, cost, user/AI turns, compactions
    $sessionParts = @()
    if ($duration) { $sessionParts += $duration }
    if ($costDisplay) { $sessionParts += $costDisplay }
    if ($userTurns -gt 0 -or $aiTurns -gt 0) {
        $sessionParts += "${userTurns} user / ${aiTurns} AI"
    }
    if ($compactions -gt 0) {
        $sessionParts += "${compactions} compact"
    }
    if ($sessionParts) {
        $parts += "session: " + ($sessionParts -join ", ")
    }

    # Context remaining
    $parts += "ctx: ${contextLeft}"

    $statusLine = $parts -join " | "
    Write-Output $statusLine

} catch {
    Write-Output "Claude"
}
