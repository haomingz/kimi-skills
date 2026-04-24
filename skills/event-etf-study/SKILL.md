---
name: event-etf-study
description: 基于关键事件进行ETF研究。从概念或事件出发，识别相关股票，构建市值加权ETF指数，分析事件窗口期间的市值变化，并生成交互式HTML仪表盘。当用户询问概念股、概念ETF、事件驱动分析或事件研究时使用。触发条件：提及影响A股概念板块的热门话题、政策或事件；请求构建主题ETF或概念指数；分析特定事件前后的股票表现。
---
## IMPORTANT: Output-Language Lock

- The final conversation reply and every deliverable (dashboard / charts / tables / custom_html) must follow the language of the user's latest query, not the market
- If the prompt is in English and the symbols are China / Hong Kong stocks, both the reply and the deliverables must stay in English; stock references should default to ticker code such as `600519.SH` / `0700.HK`
- If the prompt is in Chinese, both the reply and the deliverables must stay in Chinese; when a Chinese stock name is known, prefer the Chinese name
- Do not make this mistake: the HTML is in English but the actual conversation reply switches back to Chinese
- If the English stock name is uncertain, use the ticker code instead of a Chinese stock name

# Event Study ETF

## Workflow

1. **Read the pitfalls**: read `references/common_pitfalls.md` in full, then self-check against the checklist at the end before delivery.
2. **Freeze reproducibility metadata**: hard-code `query`, `language`, `event_date_source`, `generated_at`, `price_adjustment`, `market`, `data_source`, and `constituent_snapshot` in the code configuration block. Resolve `language` to a concrete `"zh"` or `"en"` string from the query text (CJK detection) before hard-coding it. Do not let reruns of the same study update these values automatically.
3. **Identify concept stocks**: search concept stocks across Tonghuashun (10jqka), Xueqiu, and East Money -> save a source snapshot CSV -> take the union as constituent candidates -> validate with mshtools/ifind -> assign T1/T2/T3 tiers by relevance. See `references/concept_research.md` for methodology.
4. **Fetch data**: use MCP ifind to fetch forward-adjusted daily prices plus total shares -> save raw returns/previews under `raw/` -> compute daily market cap.
   - Set the window length exactly to the user's request: if the user asks for "buy after the event and hold for one week", use 3-5 trading days before the event plus 1-2 weeks after the event (about 10-15 trading days).
   - General rule: `start_date = 3-5 trading days before the reference date`; `end_date = 2-3 trading days after the user's focus window`.
5. **Build the ETF**: use market cap on the pre-event reference date to calculate weights, then generate both market-cap-weighted NAV and equal-weighted NAV.
6. **Export standard files**: call `references/export_event_results.py` to produce 3 standard data files plus 1 reproducibility manifest. Always pass `market` (`"china_a"` or `"us"`) and `generated_at`.
7. **Generate the dashboard**: call `references/render_event_dashboard.py` to read the standard files and produce an HTML dashboard. Use `assets/dashboard_template.html` as the shell template. See "Dashboard Chart Selection" below for choosing modules.
8. **Static charts**: use Matplotlib to generate standalone PNG files in the cwd.
9. **Report**: write `report.md`; it must include `## Assumptions` and `## Known Limitations`.
10. **Self-check**: trial run -> 4 standard files written -> run `references/validate_event_outputs.py` -> reconcile numbers -> complete the pitfalls checklist.
11. **Deliver**: runnable code + 4 standard files + `report.md` + PNG files + HTML dashboard.

## Load On Demand

| File                                     | When to read it                                                    |
| ---------------------------------------- | ------------------------------------------------------------------ |
| `references/common_pitfalls.md`        | **Required reading**, first step for every task              |
| `references/concept_research.md`       | When identifying concept stocks or searching for related companies |
| `references/dashboard_schema.md`       | When generating or customizing the HTML dashboard                  |
| `references/export_event_results.py`   | Call when exporting standard files                                 |
| `references/render_event_dashboard.py` | Call when generating the dashboard                                 |
| `references/validate_event_outputs.py` | Validate before delivery                                           |
| `references/event_study_template.py`   | Skeleton for writing analysis code                                 |

## Standard Output Files

Write 4 files to the cwd, using the concept name as the prefix (e.g. `ai_chip`):

| File                           | Content                                                                                              |
| ------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `<prefix>_prices.csv`        | Daily constituent prices and market caps:`date, ticker, name, close, market_cap, tier`             |
| `<prefix>_portfolio.csv`     | Daily ETF NAV and total market cap:`date, mcap_weighted_nav, equal_weighted_nav, total_market_cap` |
| `<prefix>_summary.json`      | Summary metadata + statistics + constituent list                                                     |
| `<prefix>_run_manifest.json` | Reproducibility manifest: input hashes, parameters, dependency versions, output hashes               |

### Key Reproducibility Rules

- `generated_at` must be passed explicitly and reused for reproducible reruns.
- `language` must be resolved to `"zh"` or `"en"` and hard-coded in the configuration block.
- Weights based on market cap from the trading day before the event.
- NAV base date is `pre_event_date`, anchored at 100.
- Missing-price handling: `ffill_before_pct_change`.
- Every ifind call must record actual parameters in the manifest.
- Save constituent source snapshots as `<prefix>_constituents_sources.csv`.

## HTML Dashboard

- Use `assets/dashboard_template.html` as the shell template.
- Output one standalone HTML file: `<prefix>_dashboard.html`.
- Module selection via `include_modules` parameter. Available modules:

| Module ID    | Chart Content                                       | Suggested Scenario                       |
| ------------ | --------------------------------------------------- | ---------------------------------------- |
| `overview` | KPI cards + main NAV curve + drawdown               | **Required**                       |
| `nav`      | Market-cap-weighted vs equal-weighted NAV dual-line | When comparing weighting methods         |
| `weight`   | Tier-colored weight donut                           | When many constituents or uneven weights |
| `impact`   | Per-stock event-day/peak/latest return bars         | When analyzing stock-level reactions     |
| `mcap`     | Sector total market-cap trend area                  | When focusing on sector value changes    |
| `table`    | Constituent detail table                            | **Required**                       |

Selection guidance:

- **Full**: `["overview", "nav", "weight", "impact", "mcap", "table"]`
- **Concise**: `["overview", "nav", "table"]`
- **Stock-focused**: `["overview", "weight", "impact", "table"]`
- **Trend-focused**: `["overview", "nav", "mcap", "table"]`

### Color Scheme

Market-aware colors: China A-shares (`china_a`) use red up/green down; US equities (`us`) use green up/red down.

| Market      | Up          | Down        |
| ----------- | ----------- | ----------- |
| `china_a` | `#ef5350` | `#26a69a` |
| `us`      | `#26a69a` | `#ef5350` |

- Main chart NAV line color follows the sign of total ETF return.
- KPI cards involving gains/losses pass `raw` for market-aware coloring.
- Regular comparison charts (nav, mcap, weight) use fixed data colors: blue `#3b82f6`, orange `#f97316`, purple `#8b5cf6`.
- Tier coloring: T1 `#3b82f6`, T2 `#60a5fa`, T3 `#93c5fd`.
- Event-date marker: red dashed line `#ef4444` with white label on red background.

### `custom_html` Constraints

- DOM ids and CSS classes must use the `es-custom-` prefix.
- echarts is already loaded globally in the template.
- Titles, labels, and tooltips must use the same language as dashboard `language`.

## Matplotlib Charts

- Dark theme: dark background plus light text.
- Use red/green on the main chart to match the dashboard color scheme; blue tones for other charts.
- macOS Unicode font: `FontProperties(fname="/System/Library/Fonts/Supplemental/Arial Unicode.ttf")`.
- File name: `<prefix>_<name>.png`, `dpi=150`.

## Required Report Sections

`report.md` must include:

- `## Assumptions`: event-date source, reference-date choice, constituent criteria, weighting method, share basis, window length, price-adjustment method.
- `## Known Limitations`: survivorship bias, data coverage, excessive single-stock weight, market-cap calculation basis, and event expectations priced in before the official event date.

## Core Rules

- Use mshtools/ifind for data; do not hard-code prices.
- Proactively warn when a single-stock weight exceeds 30%.
- Always compute both market-cap-weighted and equal-weighted versions.
- Keep all output artifacts in one consistent language matching the user's query.
- The event date must be evidence-backed.

## Out Of Scope

Options/derivatives pricing, live trading, deep single-stock fundamental analysis, and cross-market arbitrage.
