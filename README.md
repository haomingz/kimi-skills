# kimi-skills

Local mirror of the [Kimi](https://www.kimi.com/) skills catalog, kept for offline use and version control. The previous Chinese README is archived as [README.zh-CN.md](README.zh-CN.md).

Each skill is its own directory under `skills/`, with a `SKILL.md` entry file and optional references, scripts, and templates. The tree also includes the 9 tool skills shipped with [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli). The public catalog changes over time; this repo currently has **134** skill directories (125 from Kimi, including a few no longer listed on the site, plus those 9 kimi-cli skills).

> Categories and the full list: [skills/README.md](skills/README.md).

---

## Install

Use the [vercel-labs/skills](https://github.com/vercel-labs/skills) CLI to install these skills into an AI coding agent (Claude Code, Cursor, Copilot, and 45+ others):

```bash
# Install into the current project (recommended)
npx skills add haomingz/kimi-skills

# Install globally, for every project
npx skills add -g haomingz/kimi-skills

# Install a subset
npx skills add haomingz/kimi-skills -s equity-researcher,chart-gen

# List installed skills
npx skills list

# Upgrade to the latest version
npx skills update
```

> On the first `npx skills add`, pick the agent you use (for example `claude-code`), or pass `-a claude-code`.

---

## Layout

```
skills/
  <skill-name>/
    SKILL.md          # skill entry file
    references/       # optional reference docs
    scripts/          # optional helper scripts
    ...
.agents/skills/
  kimi-sync/SKILL.md  # sync skill (shared Agent Skills layout)
scripts/
  kimi-list.js        # in-page script: collect skill names
  kimi-download.js    # in-page script: download skill zips from the card menu
  kimi-audit.py       # diff local directories against the Kimi name list
  kimi-extract.py     # unzip downloads into skills/, keeping the newest duplicate
```

---

## Development

The Python scripts use the standard library only. [uv](https://github.com/astral-sh/uv) is the recommended way to run them:

```bash
# First time: create .venv and pin the Python version
uv sync

uv run python scripts/kimi-audit.py
uv run python scripts/kimi-extract.py
```

Without uv, `python scripts/kimi-audit.py` works on Python ≥ 3.9.

---

## Updating skills

### Option 1 (recommended): let the agent sync

Tell the agent:

```
Use the kimi-sync skill to sync the latest skills from kimi.com into this repo
```

The agent picks a browser in this order:

1. The agent's **built-in browser** (for example Cursor's browser tools).
2. **Playwright MCP**, if there is no built-in browser. Extension mode drives your already logged-in Chrome; isolated mode needs a login inside that browser.
3. Any other browser MCP that can open a page and run JavaScript in it.

It then opens `https://www.kimi.com/skills`, expands every category, diffs names and file contents against `skills/`, downloads what is missing or changed, and extracts the zips. Details: [.agents/skills/kimi-sync/SKILL.md](.agents/skills/kimi-sync/SKILL.md).

---

### Option 2: manual, without an agent

`kimi-list.js` and `kimi-download.js` are function expressions. In the DevTools console, wrap and call them: `(<paste>)()`.

#### 1. List the skills currently on Kimi

Open https://www.kimi.com/skills while logged in. Click every "View … more" row so each category is fully loaded, then run `(<contents of scripts/kimi-list.js>)()` and copy the comma-separated names. The list script expands those rows itself.

#### 2. Audit missing names

```bash
uv run python scripts/kimi-audit.py --kimi-names "skill-a,skill-b,..."
```

The script prints missing names and a `window._kimiTargets = [...]` snippet. Directories that exist only locally are left in place.

#### 3. Download missing or updated skills

In the console, on the Skills page:

```js
window._kimiTargets = ["skill-a", "skill-b"];  // missing or changed skills only
(<paste all of scripts/kimi-download.js>)()
```

The script uses each card's **⋯ More → Download** menu (Chinese UI: **下载**). If the skill is not installed yet, it clicks **Add** / **安装** first. Allow multiple downloads if Chrome asks. Each skill takes about 6 seconds (a built-in 5.5 second gap).

A logged-in page can also return a signed zip URL from `getSkillFileTree`. That URL can be fetched with `curl` and does not depend on the browser download folder. The sync skill uses this path for in-agent browsers.

#### 4. Extract into the repo

```bash
# Finds the real Downloads folder, including a Windows folder redirected to another drive
uv run python scripts/kimi-extract.py
# Or point at a specific folder, such as Playwright's .playwright-mcp directory
uv run python scripts/kimi-extract.py --downloads-dir "D:/Downloads"
```

#### 5. Commit

```bash
git add skills
git commit -m "Sync Kimi skills $(date +%Y-%m-%d)"
```

---

## Notes

- **Where is Download?** On the current Kimi UI it is the **⋯** menu on each card (`.skill-more-btn`). The menu item reads **Download** or **下载**. Skills that are not added yet show **Add** or **安装** and must be added before that menu item appears. `kimi-download.js` does this.
- **Categories are paged.** Each section renders about 10 cards until `button.skill-section-overflow` is clicked. A scrape that skips those rows misses most of the catalog.
- **Why 5.5 seconds?** Browsers merge or block rapid downloads from the same site. The gap avoids that.
- **Duplicate zips.** Chrome saves repeats as `skill (1).zip`. `kimi-extract.py` keeps the newest file for each name.
- **Where do downloads land?** A built-in agent browser often cannot write to the system Downloads folder; use the signed zip URL instead. Playwright extension mode uses the normal Chrome Downloads folder (`kimi-extract.py` with no arguments). Isolated Playwright uses `.playwright-mcp/`, which needs `--downloads-dir`.
- **kimi-cli skills stay out of the Kimi diff.** `kimi-audit.py` ignores `codex-worker`, `feature-smoke-test`, `gen-changelog`, `gen-docs`, `gen-rust`, `pull-request`, `release`, `translate-docs`, and `worktree-status`.

---

## Credits

- **Kimi skills** — published by [Moonshot AI](https://www.moonshot.cn/). Copyright remains with the original authors. See the `LICENSE` file in each skill directory.
- **kimi-cli skills** — from [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) (Apache 2.0).
- **Sync scripts and docs** — original to this repo, MIT licensed.

## License

The **scripts** in `scripts/` and the **docs** (`README.md`, `README.zh-CN.md`, `AGENTS.md`) are under the [MIT License](https://opensource.org/licenses/MIT).

Skills under `skills/` keep their original authors' copyright. Read the `LICENSE` file in each directory. Skills with no license file are all rights reserved and come from the Kimi platform.

---

*Personal mirror archive. Not affiliated with Moonshot AI.*
