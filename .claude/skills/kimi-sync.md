---
name: kimi-sync
description: Sync this repo with the latest Kimi official skills. Uses the Playwright MCP to operate the Kimi web UI, then calls local Python scripts to audit and extract. Run this skill whenever you need to pull new or updated skills from kimi.com.
---

# Kimi Skills Sync

Syncs this repo with the current Kimi official skills list by driving the Kimi web UI via the **Playwright MCP**, then running local scripts for the diff and extraction.

## Prerequisites

- Playwright MCP is available. Tool names depend on how it is wired up:
  - **`--extension` mode (recommended here):** Playwright drives your **real, logged-in Chrome** through the Playwright Chrome extension. Tools are named `mcp__playwright__browser_*`. You are already logged into kimi.com, and downloads land in your normal Chrome Downloads folder.
  - **Isolated mode:** Playwright launches its own browser with a separate profile (tools may be named `mcp__plugin_playwright_playwright__browser_*`). You must log into kimi.com inside that browser, and downloads land in Playwright's MCP output dir (e.g. `<repo>\.playwright-mcp\`).
- Python 3 (via `uv`) is available for the audit/extract scripts.
- The repo's `scripts/` folder is present.

> The steps below use the short tool names (`browser_navigate`, `browser_evaluate`, …). Prefix with the qualified namespace your setup uses (`mcp__playwright__` for extension mode).

## Step 1 — Open the Skills tab

Navigate straight to the Skills tab — far more reliable than hunting for a button:

```
browser_navigate(url="https://www.kimi.com/extensions?tab=skill")
```

If a promo/marketing dialog covers the page, dismiss it (`browser_snapshot` to find the close/我知道了 button, then `browser_click`). Confirm the skills grid is loaded and you are logged in with a quick check:

```
browser_evaluate(function="() => ({ loggedIn: !document.querySelector('img[alt*=\"用户\"], .login, [class*=\"login\"]') ? 'maybe' : 'check', cards: document.querySelectorAll('.skill-card-title').length })")
```

You want `cards` > 0. If `cards` is 0: in extension mode you may have landed on the 插件 (Plugins) tab — make sure the URL has `?tab=skill`, or click the **技能** tab button. In isolated mode, a 0 usually means you are not logged in — pause and ask the user to log in, then retry.

## Step 2 — Scrape the current skill list

Call `browser_evaluate`, passing the **entire contents** of `scripts/kimi-list.js` as the `function` argument. It returns a comma-separated string of every skill name (uses `.skill-card-title`).

```
browser_evaluate(function="<paste full contents of scripts/kimi-list.js>")
```

Capture the returned comma-separated string. If it returns `null`, the Skills tab is not open — go back to Step 1.

## Step 3 — Audit local vs remote

```bash
uv run python scripts/kimi-audit.py --kimi-names "<comma-separated names from Step 2>"
```

Parse the output:
- If "All Kimi skills are present locally" → nothing to download; report to the user and stop. (Any "Local only" entries are skills removed from the platform — leave them unless the user asks to prune.)
- Otherwise collect the missing skill names and the `window._kimiTargets = [...]` snippet it prints.

## Step 4 — Download missing skills

First set the targets (missing skills only) with one `browser_evaluate`. The `function` must be a function expression, so wrap the assignment:

```
browser_evaluate(function="() => { window._kimiTargets = [\"skill-a\", \"skill-b\"]; return 'ok'; }")
```

(Omit this to download ALL skills shown on the tab.)

Then start the downloader by passing the **entire contents** of `scripts/kimi-download.js` as the `function` argument:

```
browser_evaluate(function="<paste full contents of scripts/kimi-download.js>")
```

It returns `'started'` immediately and runs the download loop **inside the page** (fire-and-forget). Per skill it: finds the `.skill-card`, installs it first if the button says 安装, then opens the card's **⋯ More** menu (`.skill-more-btn`) and clicks **下载** (`.skill-menu-item`).

**Timing constraints:**
- A 5.5 s spacing between downloads is built in — do NOT reduce it.
- Playwright generally permits multiple downloads without prompting. If a real-Chrome "Allow multiple downloads?" prompt or any JS dialog appears, accept it with `browser_handle_dialog(accept=true)`.
- Budget ~7 s per skill. Poll progress with a separate `browser_evaluate`:

```
browser_evaluate(function="() => ({ done: window._kimiDLDone, log: window._kimiDLLog, error: window._kimiDLError })")
```

Wait between polls with `browser_wait_for(time=10)` and re-poll until `done` is `true`. If any entries have `ok:false`, retry just those by re-setting `window._kimiTargets` to that subset and re-running `scripts/kimi-download.js`.

## Step 5 — Extract zips

**Extension mode (real Chrome):** downloads land in your normal Downloads folder, so run the extractor with **no flag** — it auto-detects the real Downloads dir (including Windows folders redirected to another drive, e.g. `F:\Downloads`):

```bash
uv run python scripts/kimi-extract.py
```

**Isolated mode:** point it at Playwright's output dir instead:

```bash
uv run python scripts/kimi-extract.py --downloads-dir "<playwright output dir, e.g. .playwright-mcp>"
```

Verify the output reports the expected number of skills extracted.

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
| `scripts/kimi-list.js` | Scrape skill names from the Skills tab | `browser_evaluate` in Step 2 |
| `scripts/kimi-download.js` | Batch-download skill zips via the ⋯ More → 下载 menu | `browser_evaluate` in Step 4 |
| `scripts/kimi-audit.py` | Diff local skills vs Kimi list | `bash` in Steps 3 & 6 |
| `scripts/kimi-extract.py` | Unzip downloads into `skills/` | `bash` in Step 5 |

## Current Kimi UI selectors (2026)

If the scrape/download breaks, the UI likely changed. Re-derive these by inspecting `https://www.kimi.com/extensions?tab=skill`:

| Element | Selector |
|---------|----------|
| Skill card | `.skill-card` |
| Skill name | `.skill-card-title` |
| Scroll host | `main.skill-page` |
| Install/Use button | `.skill-card-btn` (text 安装 / 使用) |
| More (⋯) button | `.skill-more-btn` |
| More-menu items | `.skill-menu-item` (使用 / 编辑 / 下载 / 删除) inside `.skill-card-more-popover` |
