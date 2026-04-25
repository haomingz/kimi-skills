---
name: kimi-sync
description: Sync this repo with the latest Kimi official skills. Uses chrome-devtools MCP to operate the Kimi web UI, then calls local Python scripts to audit and extract. Run this skill whenever you need to pull new or updated skills from kimi.com.
---

# Kimi Skills Sync

Syncs this repo with the current Kimi official skills list by driving the Kimi web UI via the chrome-devtools MCP, then running local scripts for the diff and extraction.

## Prerequisites

- chrome-devtools MCP is available (check with `mcp__chrome-devtools__list_pages`)
- User is already logged into kimi.com in an open Chrome tab, OR you open one and ask the user to log in
- Python 3 is available for the audit/extract scripts
- The repo's `scripts/` folder is present

## Step 1 — Open kimi.com and navigate to the skills panel

```
mcp__chrome-devtools__navigate_page(url="https://www.kimi.com/")
```

Wait for the page to load. Then find and click the Kimi Picks / skills panel button to make `.skill-row` elements appear in the DOM. Use `take_screenshot` to verify the panel is open before proceeding.

If the user is not logged in, pause and ask them to log in, then continue.

## Step 2 — Scrape the current skill list

Run `scripts/kimi-list.js` via `evaluate_script` to get all skill names currently on the platform:

```js
// paste the full contents of scripts/kimi-list.js
// NOTE: uses .skill-card / .card-name (current Kimi UI); scrolls to load all lazy cards
```

Paste and run the full contents of `scripts/kimi-list.js` via `evaluate_script`. It scrolls through the entire panel and returns a comma-separated string of all skill names.

Capture the returned comma-separated string. If `null` is returned, the panel is not open — go back to Step 1.

## Step 3 — Audit local vs remote

Pass the scraped names to the audit script:

```bash
uv run python scripts/kimi-audit.py --kimi-names "<comma-separated names from Step 2>"
```

Parse the output:
- If "All Kimi skills are present locally" → nothing to do, report to user and stop.
- Otherwise, collect the missing skill names and the `window._kimiTargets = [...]` snippet.

## Step 4 — Download missing skills

Still on the kimi.com page with the skills panel open, inject the targets and then run the downloader:

```js
// First, set targets (only the missing ones):
window._kimiTargets = ["skill-a", "skill-b", ...];
```

Then inject and execute the full contents of `scripts/kimi-download.js` via `evaluate_script`.

**Important timing constraints:**
- The script has a built-in 5.5 s delay between downloads to avoid Chrome's download throttle — do NOT reduce it.
- Chrome will show a "Allow multiple downloads?" prompt — use `handle_dialog` or click Allow via `click`.
- Each skill takes ~7 s total. For N skills, budget N×7 s before checking completion.
- Poll `window._kimiDLDone` to know when finished:

```js
({ done: window._kimiDLDone, log: window._kimiDLLog })
```

If any skills failed (e.g. `ok: false` in the log), retry just those by resetting `window._kimiTargets` and re-running the downloader.

## Step 5 — Extract zips

Run the extract script. It defaults to `~/Downloads` and looks for zips from the last 4 hours:

```bash
uv run python scripts/kimi-extract.py
```

If the user's Downloads folder is elsewhere:

```bash
uv run python scripts/kimi-extract.py --downloads-dir "/path/to/Downloads"
```

Verify the output says the expected number of skills were extracted.

## Step 6 — Verify and commit

```bash
# Confirm the new skill dirs are present
uv run python scripts/kimi-audit.py --kimi-names "<same list from Step 2>"

# Stage and commit
git add skills
git commit -m "Sync Kimi skills $(date +%Y-%m-%d)"
```

Report the final count and any skills that still failed to the user.

## Reference scripts

| File | Purpose | How agent uses it |
|------|---------|-------------------|
| `scripts/kimi-list.js` | Scrape skill names from Kimi UI | `evaluate_script` in Step 2 |
| `scripts/kimi-download.js` | Batch-download skill zips via Kimi UI | `evaluate_script` in Step 4 |
| `scripts/kimi-audit.py` | Diff local skills vs Kimi list | `bash` in Steps 3 & 6 |
| `scripts/kimi-extract.py` | Unzip downloads into `skills/` | `bash` in Step 5 |
