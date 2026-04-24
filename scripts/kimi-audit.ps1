# Kimi Skills Audit
# Compares locally extracted skills against a reference list retrieved from the Kimi UI.
# Prints missing skills so you can run a targeted re-download.
#
# USAGE:
#   .\scripts\kimi-audit.ps1 -KimiNames "skill-a,skill-b,..."
#   (paste the comma-separated list from the browser console output of kimi-list.js)

param(
    [string]$KimiNames = "",           # comma-separated list from browser
    [string]$SkillsDir = "$PSScriptRoot\..\\skills",
    # kimi-cli skills that live in the same dir but are not Kimi official
    [string[]]$ExcludeLocal = @('codex-worker','feature-smoke-test','gen-changelog','gen-docs','gen-rust','pull-request','release','translate-docs','worktree-status')
)

$SkillsDir = (Resolve-Path $SkillsDir).Path

$local = (Get-ChildItem $SkillsDir -Directory | Where-Object { $_.Name -notin $ExcludeLocal }).Name

if ($KimiNames) {
    $kimi = $KimiNames -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ }
} else {
    Write-Host "No -KimiNames provided. Showing local skill count only."
    Write-Host "Local skills: $($local.Count)"
    Write-Host ""
    Write-Host "To get the full Kimi list, run kimi-list.js in the browser console and paste the output here."
    exit 0
}

$missing  = $kimi  | Where-Object { $_ -notin $local }
$extra    = $local | Where-Object { $_ -notin $kimi }

Write-Host "Kimi official : $($kimi.Count)"
Write-Host "Local         : $($local.Count)"
Write-Host ""

if ($missing.Count -eq 0) {
    Write-Host "All Kimi skills are present locally."
} else {
    Write-Host "Missing locally ($($missing.Count)):"
    $missing | ForEach-Object { Write-Host "  - $_" }
    Write-Host ""
    Write-Host "Set these as targets in the browser before running kimi-download.js:"
    $json = $missing | ForEach-Object { "`"$_`"" }
    Write-Host "window._kimiTargets = [$($json -join ',')]"
}

if ($extra.Count -gt 0) {
    Write-Host ""
    Write-Host "Local only (not in Kimi list — may be removed from platform):"
    $extra | ForEach-Object { Write-Host "  + $_" }
}
