---
name: kimi-sync
description: Sync this repo with the latest Kimi official skills. Prefer the agent's built-in browser, then fall back to Playwright MCP or another browser MCP. Run this skill whenever you need to pull new or updated skills from kimi.com.
---

# Kimi Skills Sync

Sync this repo with the skills listed on kimi.com. Drive the Kimi web UI from a browser, then use the local Python scripts to audit names and extract zips.

## Choose a browser

Use the first backend that actually exists in this session. Do not require Playwright when a built-in browser is available.

1. **Built-in agent browser (preferred).** Examples: Cursor `cursor-ide-browser` (`browser_navigate`, `browser_snapshot`, `browser_lock`, `browser_click`, `browser_cdp`). This profile is separate from the user's everyday Chrome. If kimi.com is not logged in, unlock the browser and ask the user to log in, then continue.
2. **Playwright MCP.** Use it only when no built-in browser tools are available.
   - **`--extension` mode:** tools named `mcp__playwright__browser_*`. Drives the user's logged-in Chrome. Downloads land in the normal Chrome Downloads folder.
   - **Isolated mode:** tools may be named `mcp__plugin_playwright_playwright__browser_*`. Log into kimi.com in that browser. Downloads land in Playwright's output dir (for example `<repo>\.playwright-mcp\`).
3. **Any other browser MCP** that can navigate and evaluate JavaScript in the page. Treat it like the closest of the two backends above.

If none of these exist, stop and tell the user. Python 3 (via `uv`) and `scripts/` are also required.

### Running page JavaScript

| Backend | How |
|---------|-----|
| Built-in browser | `browser_cdp` → `Runtime.evaluate`. Set `returnByValue: true`. For async scripts set `awaitPromise: true` and pass an invoked expression: `"(async () => { ... })()"`. There is no `browser_evaluate`. |
| Playwright or similar | `browser_evaluate`, passing the script as the `function` argument. Prefix the tool with the namespace that is actually connected. |

Lock a built-in browser before a long run (`browser_lock`) and unlock it when you stop or when the user must log in. CDP download, cookie, and filesystem commands are often denied on a built-in browser. Do not depend on its download folder.

## Step 1 — Open the Skills page

```
browser_navigate(url="https://www.kimi.com/skills")
```

`https://www.kimi.com/extensions?tab=skill` currently redirects away from the catalog. If you land on Plugins, click the **Skills** / **技能** tab (`button.top-tab`).

Dismiss a promo dialog if one covers the page. Then confirm the grid:

```
() => ({ cards: document.querySelectorAll('.skill-card-title').length, href: location.href })
```

You want `cards` > 0. Zero cards on a logged-out page means you should ask the user to log in. Zero cards while logged in usually means the Skills tab is not selected.

## Step 2 — Scrape the current skill list

Each category first renders about 10 cards. Click every `button.skill-section-overflow` ("View … more"), wait ~700 ms, and repeat until none remain (cap about 25 rounds). `scripts/kimi-list.js` does this, then scrolls and returns a comma-separated name list.

- Built-in browser: `Runtime.evaluate` the file as `"(<contents of scripts/kimi-list.js>)()"` with `awaitPromise: true`.
- Playwright: pass the file contents as `browser_evaluate`'s `function`.

If the result is `null`, the Skills tab is not open — go back to Step 1.

## Step 3 — Audit local vs remote names

```bash
uv run python scripts/kimi-audit.py --kimi-names "<comma-separated names from Step 2>"
```

- Missing names must be downloaded.
- "Local only" entries were removed from the page. Leave them unless the user asks to prune.
- "All Kimi skills are present locally" does **not** finish the sync. Continue to Step 4 and compare file contents.

## Step 4 — Compare file contents

For every remote skill that already has a `skills/<name>/` directory, compare the live file tree with the local files.

On the logged-in page:

1. Read `document.querySelector('#app').__vue_app__._context.provides`.
2. Use the `VUE_QUERY_CLIENT` cache. Take the successful `skills` / `skillSections` query that has data. A pending query whose user id is null is the logged-out one.
3. Find the provide object that has `getSkillFileTree`.
4. Collect skill ids from installed skills plus each section's `skills` and `overflowSkills`.
5. `await model.getSkillFileTree({ skillId })`. **Omit `versionNo`.** Passing `versionNo: 1` returns an internal error. The result is `{ downloadUrl, skillFileTree }`. Nodes have `name`, `isDir`, `size`, and `children`.

Walk the tree to relative paths and byte sizes. Compare with `skills/<name>/`. Skip `.git` and `__pycache__`. If the only size gap equals the number of LF newlines, the files differ by CRLF versus LF — treat them as unchanged. Any other path or size difference means the skill should be replaced.

Keep the signed `downloadUrl` for skills that need a download. A GET of that URL returns a zip and does not need browser cookies. Zip entries are paths inside the skill directory (`SKILL.md`, not `<name>/SKILL.md`).

Fetch trees with a small concurrency (about 4). One internal error should be retried once without `versionNo`.

## Step 5 — Download missing and changed skills

**Preferred on every backend, and required for the built-in browser:** download the signed zip with `curl` or Python, reject entries that are absolute or contain `..`, delete `skills/<name>/`, and extract into that directory. This is the same replace behavior as `scripts/kimi-extract.py`.

**Menu-click fallback** (Playwright, or a browser that can save downloads) when a signed URL is unavailable:

1. Set targets: `() => { window._kimiTargets = ["skill-a", "skill-b"]; return 'ok'; }`
2. Run the whole of `scripts/kimi-download.js`. It returns `'started'` and downloads inside the page. For each skill it finds `.skill-card`, clicks **Add** / **Install** / **安装** when that is the primary button (`.skill-card-btn` or `.skill-card-use-btn`), opens `.skill-more-btn`, and clicks **Download** / **下载** (`.kimi-menu-item` or `.skill-menu-item`).
3. Keep the built-in 5.5 s gap. Do not reduce it.
4. If Chrome asks to allow multiple downloads, or a JS dialog appears, accept it (`browser_handle_dialog` on Playwright).
5. Poll `() => ({ done: window._kimiDLDone, log: window._kimiDLLog, error: window._kimiDLError })` about every 10 seconds until `done` is true. Retry names with `ok: false`.
6. Extract:

```bash
# Extension mode, or any download that landed in the real Downloads folder
uv run python scripts/kimi-extract.py

# Isolated Playwright
uv run python scripts/kimi-extract.py --downloads-dir "<playwright output dir, e.g. .playwright-mcp>"
```

## Step 6 — Verify and commit

Run the name audit again with the same list from Step 2. Re-check byte sizes for every skill you replaced.

When the user asked to sync the repo, commit the skill changes:

```bash
git add skills
git commit -m "Sync Kimi skills $(date +%Y-%m-%d)"
```

Do not commit unrelated files. Report the remote count, what was added or updated, what was unchanged, and any skills that still failed. Mention local-only names and leave them in place.

## Reference scripts

| File | Purpose |
|------|---------|
| `scripts/kimi-list.js` | Expand category overflow, then scrape `.skill-card-title` |
| `scripts/kimi-download.js` | Menu download fallback (⋯ → Download / 下载) |
| `scripts/kimi-audit.py` | Diff local skill directory names against the Kimi list. Excludes the 9 kimi-cli skills |
| `scripts/kimi-extract.py` | Unzip downloads into `skills/`, keeping the newest `skill (N).zip` |

## Current Kimi UI selectors (2026)

If scraping breaks, re-derive these on `https://www.kimi.com/skills`:

| Element | Selector |
|---------|----------|
| Skills tab (when the page opens on Plugins) | `button.top-tab` (text Skills / 技能) |
| Category chips | `.carousel-scroll button` (Added, Featured, Productivity, …) |
| Skill card | `.skill-card` |
| Skill name | `.skill-card-title` |
| Scroll host | `main.skill-page` |
| Section overflow ("View … more") | `button.skill-section-overflow` |
| Add / Use button | `.skill-card-use-btn` or `.skill-card-btn` (Add / Install / 安装, or Use / 使用) |
| More (⋯) button | `.skill-more-btn` |
| More-menu items | `.kimi-menu-item` or `.skill-menu-item` (Use / Edit / Download / Delete, or 使用 / 编辑 / 下载 / 删除) |
