# kimi-skills — project context

This repository is a local mirror of the official Kimi skill library, for offline use and version control.

## Layout

- `skills/<name>/` — one directory per skill. `SKILL.md` is the entry file.
- `scripts/` — browser snippets (run them in the agent's built-in browser first; use Playwright MCP or another browser MCP only when there is no built-in browser) and Python scripts for the local audit and unzip.
- `.agents/skills/kimi-sync/SKILL.md` — the sync skill, in the shared Agent Skills layout (`<skill-name>/SKILL.md`). Full procedure for pulling skills from kimi.com.

## Where the skills come from

### Kimi official skills

From the official Kimi skills catalog at [kimi.com](https://www.kimi.com/). The public list changes; the category index lives in [skills/README.md](skills/README.md). Examples by area:

- **Investment research and financial analysis:** equity-researcher, financial-report-reader, stock-tech-analysis, cashflow-valuation
- **Marketing and content:** ad-copywriter, seo-copywriting-guide, wechat-post-craft, xhs-note-creator
- **Software engineering:** code-safety-audit, api-doc-gen, tdd-coach, web-security-audit
- **Data analysis and visualization:** chart-gen, auto-stat-test, outlier-scan, split-test-evaluator
- **Product and project management:** idea-to-prd, gantt-chart-builder, incident-retrospective
- **Writing and academic research:** research-paper-refiner, xindaya-translator, flashcard-studio
- **Workplace productivity:** resume-craft, interview-simulator, pro-email-composer
- **Legal and compliance:** legal-contract-gen, compliance-review-planner, tos-risk-checker
- **Visual design and layout:** ui-blueprint, sci-paper-cn, photo-magazine-cn

### kimi-cli tool skills (9)

From [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli), stored in the same `skills/` directory:

`codex-worker`, `feature-smoke-test`, `gen-changelog`, `gen-docs`, `gen-rust`, `pull-request`, `release`, `translate-docs`, `worktree-status`

Exclude these nine when diffing against the official Kimi list.

## How to update skills

Preferred: tell the agent to use the kimi-sync skill. Pick a browser in this order:

1. **The agent's built-in browser** (preferred; for example Cursor `browser_navigate` / `browser_cdp`).
2. **Playwright MCP**, only if there is no built-in browser (`--extension` drives the local logged-in Chrome; isolated mode needs a login in that browser).
3. **Any other browser MCP** that can open a page and run JavaScript.

The page is `https://www.kimi.com/skills`. A built-in browser runs `scripts/kimi-list.js` with `Runtime.evaluate`; Playwright uses `browser_evaluate`. Then `kimi-audit.py` compares names, the file trees are compared for content changes, and missing or updated zips are extracted into `skills/`.

> Playwright `--extension` downloads go to the real Chrome Downloads folder. Isolated mode uses `.playwright-mcp/`. A built-in browser often cannot save into the system Downloads folder; use the signed zip URL returned by the page and download it with `curl`.

The full procedure and timing constraints are in [.agents/skills/kimi-sync/SKILL.md](.agents/skills/kimi-sync/SKILL.md).

## Constraints

- **Download lives in the ⋯ menu.** The item label is Download or 下载. A skill that is not added yet (button Add / 安装) must be added first. The built-in browser should use the signed zip URL; the menu click is the fallback for a browser that can save downloads.
- **Each category first renders about 10 cards.** Click `button.skill-section-overflow` (View … more) before scraping. `kimi-list.js` does this. If the selectors break, re-check the table at the end of the kimi-sync skill.
- **5.5 second download gap.** Browsers merge or block rapid downloads. The gap is built into `kimi-download.js`.
- **Duplicate zips.** `skill (1).zip` style repeats are handled by `kimi-extract.py`, which keeps the newest file.
- **Download directory depends on the browser.** `--extension` mode uses the real Chrome Downloads folder (`kimi-extract.py` with no arguments, including a Windows folder redirected to another drive such as `F:\Downloads`). Isolated mode uses `.playwright-mcp/` (`--downloads-dir`).
- **kimi-cli skills are excluded.** `kimi-audit.py` skips them via `KIMI_CLI_SKILLS`.

## Credits and license

- Official Kimi skills are copyright [Moonshot AI](https://www.moonshot.cn/) and the individual skill authors.
- kimi-cli skills use the Apache 2.0 license.
- Scripts and docs in this repository use the MIT license.
