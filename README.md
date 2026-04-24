# kimi-skills

Local mirror of all official [Kimi](https://www.kimi.com/) AI skills, plus the skills from [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli).

Each skill is a self-contained directory under `skills/` containing a `SKILL.md` instruction file and optional reference files, scripts, and templates.

## Structure

```
skills/
  <skill-name>/
    SKILL.md          # main skill definition
    references/       # optional reference docs
    scripts/          # optional helper scripts
    ...
scripts/
  kimi-list.js          # browser snippet: list all Kimi skill names
  kimi-download.js      # browser snippet: download all/selected skills as zips
  kimi-extract.ps1      # PowerShell: extract zips into .agents/skills/
  kimi-audit.ps1        # PowerShell: compare local vs Kimi, print missing
```

## Skills count

| Source | Count |
|--------|-------|
| Kimi official (kimi.com) | 120 |
| kimi-cli (MoonshotAI) | 9 |

## How to update / add missing skills

### 1. List what Kimi currently has

Open https://www.kimi.com/, open the Kimi Picks panel, then run in DevTools console:

```js
// scripts/kimi-list.js
```

Copy the comma-separated output.

### 2. Audit what's missing locally

```powershell
.\scripts\kimi-audit.ps1 -KimiNames "skill-a,skill-b,..."
```

This prints the missing skill names and a ready-to-paste `window._kimiTargets = [...]` line.

### 3. Download missing skills

In the browser (Kimi Picks panel open):

```js
// Optional: target only missing skills
window._kimiTargets = ["skill-a", "skill-b"];

// Then paste scripts/kimi-download.js
```

Chrome will ask to allow multiple downloads — click **Allow**.  
Each skill takes ~6 s (5.5 s delay prevents Chrome from blocking rapid downloads).

### 4. Extract zips

```powershell
.\scripts\kimi-extract.ps1
# Optional params:
.\scripts\kimi-extract.ps1 -DownloadsDir "D:\Downloads" -HoursBack 6
```

### 5. Commit

```bash
git add .agents/skills
git commit -m "Update Kimi skills $(date +%Y-%m-%d)"
```

## Notes

- **Why the "Add" step?** Kimi only shows the full zip download button after you install (Add) a skill. Individual file downloads are available without installing, but the zip is needed to get all files at once.
- **Why 5.5 s delay?** Chrome blocks multiple rapid downloads from the same origin. A ≥5 s gap between each download prevents this.
- **Deduplication:** Chrome saves repeated downloads as `skill (1).zip`, `skill (2).zip`, etc. `kimi-extract.ps1` deduplicates by keeping only the most recently written file per skill name.
