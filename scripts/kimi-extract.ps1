# Kimi Skills Extractor
# Extracts downloaded Kimi skill zips into the repo, deduplicating by keeping only
# the most recent file when Chrome created numbered duplicates like "skill (1).zip".
#
# USAGE:
#   .\scripts\kimi-extract.ps1
#   .\scripts\kimi-extract.ps1 -DownloadsDir "D:\Downloads" -HoursBack 6
#
# After extraction, run: git add .agents/skills && git commit -m "Update Kimi skills"

param(
    [string]$DownloadsDir = "F:\Downloads",
    [int]$HoursBack = 4,
    [string]$SkillsDir = "$PSScriptRoot\..\\skills"
)

Add-Type -AssemblyName System.IO.Compression.FileSystem

$SkillsDir = (Resolve-Path $SkillsDir).Path
$cutoff = (Get-Date).AddHours(-$HoursBack)

$allZips = Get-ChildItem $DownloadsDir -Filter "*.zip" | Where-Object { $_.LastWriteTime -gt $cutoff }
Write-Host "Found $($allZips.Count) zip(s) newer than $HoursBack hours in $DownloadsDir"

# Deduplicate: strip " (N)" suffix, keep the most recently written file per base name
$unique = $allZips |
    Group-Object { $_.BaseName -replace ' \(\d+\)$', '' } |
    ForEach-Object { $_.Group | Sort-Object LastWriteTime -Descending | Select-Object -First 1 }

Write-Host "Unique skills to extract: $($unique.Count)"

$extracted = 0
$skipped = 0

foreach ($zip in $unique) {
    $name = $zip.BaseName -replace ' \(\d+\)$', ''
    $dest = Join-Path $SkillsDir $name

    # Remove existing directory so extraction is idempotent
    if (Test-Path $dest) {
        Remove-Item -Recurse -Force $dest
    }

    try {
        [System.IO.Compression.ZipFile]::ExtractToDirectory($zip.FullName, $dest)
        Write-Host "  Extracted: $name"
        $extracted++
    } catch {
        Write-Warning "  Failed to extract $($zip.Name): $_"
        $skipped++
    }
}

Write-Host ""
Write-Host "Done. Extracted: $extracted  Failed: $skipped"
Write-Host "Total skill dirs now: $((Get-ChildItem $SkillsDir -Directory).Count)"
