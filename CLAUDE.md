# kimi-skills — Project Context

This repository is a local mirror of all official Kimi AI skills from kimi.com, maintained for offline access and version control.

## Layout

- `skills/<name>/` — each skill as a directory; `SKILL.md` is the entry point
- `scripts/` — browser JS snippets and PowerShell helpers for downloading/auditing skills

## Skills that live here but are NOT from kimi.com

The following 9 skills come from [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) and are stored alongside the official ones:

`codex-worker`, `feature-smoke-test`, `gen-changelog`, `gen-docs`, `gen-rust`, `pull-request`, `release`, `translate-docs`, `worktree-status`

Exclude these when auditing against the Kimi official list.

## Updating skills

See `README.md` for the full update workflow. The short version:

1. Run `scripts/kimi-list.js` in browser → get current Kimi skill names
2. Run `scripts/kimi-audit.ps1 -KimiNames "..."` → see what's missing
3. Set `window._kimiTargets = [...]` in browser, then run `scripts/kimi-download.js`
4. Run `scripts/kimi-extract.ps1` to unzip into `.agents/skills/`
5. `git add .agents/skills && git commit`

## Key constraints

- The zip download button only appears **after** a skill is installed (Add button clicked)
- Chrome blocks rapid successive downloads — the download script uses a **5.5 s delay** between each skill
- `kimi-extract.ps1` deduplicates `skill (1).zip` / `skill (2).zip` by keeping the newest file
