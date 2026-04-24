# Event Study ETF Dashboard Schema Quick Reference

> This document is a quick reference for the **internal JSON schema used by the dashboard template**.
> For the full workflow, see the "Standard Output Files" and "HTML Dashboard" sections in `SKILL.md`.

## End-To-End Flow In One Sentence

Run the event study -> the script writes 3 standard data files (`<prefix>_prices.csv` / `<prefix>_portfolio.csv` / `<prefix>_summary.json`) and 1 reproducibility manifest (`<prefix>_run_manifest.json`) -> the dashboard script reads `portfolio.csv` + `summary.json` -> builds a `report_data` dict -> replaces the `__REPORT_DATA__` placeholder in `dashboard_template.html` -> outputs a standalone HTML file.

## Expected `report_data` Structure

```python
report_data = {
    "meta": {
        "strategy_name": "DeepSeek Concept ETF Event Study",
        "symbol": "DeepSeek Concept Stocks",
        "start": "2025-01-20",              # event date
        "end": "2025-04-10",                # data end date
        "event_date": "2025-01-20",         # actual event date
        "benchmark": "CSI 300",             # optional benchmark index
        "weighting": "market_cap",          # market_cap / equal
        "num_stocks": 25,                   # constituent count
        "generated_at": "2026-04-11T10:00:00+08:00",  # from summary/manifest; do not auto-refresh on reruns
        "price_adjustment": "forward",      # forward-adjusted; record the actual ifind enum value
        "data_source": "mshtools/ifind",
        "missing_price_policy": "ffill_before_pct_change",
        "language": "en",                   # zh / en; inferred from query or explicitly configured
        "query": "DeepSeek concept stock event study",  # optional original user query for language detection and reproducibility
    },
    "summary": {
        "total_return_pct": 38.72,           # synthetic ETF cumulative return
        "max_drawdown_pct": 12.45,           # maximum drawdown
        "top_weight_pct": 49.2,              # largest weight
        "top_weight_name": "Hygon Information",  # largest-weight stock
        "hhi": 0.182345,                     # weight concentration
        "equal_weighted_return_total_pct": 25.31,  # equal-weighted benchmark return
    },
    "equity_curve": [{"date": "2025-01-20", "value": 1.0}, ...],  # ETF NAV series
    "constituents": [{"ticker": "688041.SH", "name": "Hygon Information", "tier": 1,
                      "reason": "Core domestic GPU exposure", "weight": 49.2,
                      "event_day_chg": 8.6, "peak_chg": 35.6,
                      "latest_chg": 18.2, "market_cap_billion": 3218.5}, ...],
    "ui": {
        "active_tab": "overview",
        "tabs": [{"id": "overview", "label": "Overview"}],
        "language": "en",
        "i18n": { ... },
    },
    "modules": [ ... ],      # see below
}
```

### Field Sources

| Field | Source |
|---|---|
| `meta` / `summary` | `<prefix>_summary.json` |
| `equity_curve` | `date + mcap_weighted_nav` from `<prefix>_portfolio.csv` |
| `constituents` | `constituents` array from `<prefix>_summary.json` |
| `generated_at` | `<prefix>_summary.json`; must match `<prefix>_run_manifest.json` |
| `language` | `<prefix>_summary.json`; usually inferred from the original query; HTML/PNG/report must agree |
| Output file hashes | `outputs` in `<prefix>_run_manifest.json` |

## `modules` Array

`modules` controls which cards render on the page. Modules under the same tab render from top to bottom in array order.

Common module types for event-study ETF dashboards:

| type | Purpose |
|---|---|
| `overview_chart` | KPI card strip + main synthetic ETF NAV curve + drawdown sub-chart |
| `line_chart` | Multi-series NAV comparison, such as market-cap-weighted vs equal-weighted vs benchmark |
| `custom_html` | echarts donut for weight distribution, horizontal bars for per-stock contribution, area chart for market-cap distribution, etc. |
| `trades_table` | Reused as a constituent detail table: display label, tier, weight, returns, market cap, industry. Display label is stock name for Chinese output and ticker/symbol for English output. |
| `text` | Event description, research assumptions, and data-source notes |

### `overview_chart`

KPI cards plus synthetic ETF NAV curve. Event studies generally do not need buy/sell markers, so `markers` can stay empty.

**Colors switch automatically by market**: China A-shares use red for up and green for down; US equities use green for up and red for down. `render_event_dashboard.py` selects the scheme from `meta.market`.

```python
{
    "type": "overview_chart",
    "tab": "overview",
    "width": "full",
    "stats": [
        {"label": "Constituents", "value": "25"},                   # non-change KPI: neutral color
        {"label": "Pre-event Market Cap", "value": "3,218 B CNY"},  # non-change KPI: neutral color
        {"label": "Peak Market Cap Change", "value": "+38.72%", "raw": 38.72},
        {"label": "Latest Market Cap Change", "value": "-5.12%", "raw": -5.12},
        {"label": "ETF NAV Return", "value": "+25.31%", "raw": 25.31},
    ],
    "points": [
        {"date": "2025-01-20", "equity": 1.0,   "drawdown_abs": 0.0},
        {"date": "2025-01-21", "equity": 1.023, "drawdown_abs": 0.0},
        ...
    ],
    "markers": [],               # event studies usually have no buy/sell markers
    "series_key": "equity",
    "stroke": "#ef5350",         # market-aware up/down color by ETF total return; China A-share positive = red, US positive = green
    "bars_key": "drawdown_abs",
    "bars_fill": "rgba(38,166,154,0.40)",  # China A-shares = green down/drawdown, US = red, controlled by MARKET_COLORS
    "toggles": [
        {"id": "equity", "label": "Cap-weighted", "color": "#ef5350", "checked": True},
        {"id": "drawdown", "label": "Drawdown", "color": "#26a69a", "checked": True},
    ],
    "modes": [
        {"id": "absolute", "label": "NAV", "active": True},
        {"id": "percentage", "label": "Return"},
    ],
}
```

### `line_chart`

Multi-series NAV comparison, commonly market-cap-weighted vs equal-weighted vs benchmark:

```python
{
    "type": "line_chart",
    "tab": "overview",
    "title": "NAV Comparison",
    "subtitle": "Market-cap-weighted vs equal-weighted vs CSI 300",
    "series": [
        {"name": "Cap-weighted", "points": [{"date": "2025-01-20", "value": 1.0}, ...]},
        {"name": "Equal-weighted", "points": [{"date": "2025-01-20", "value": 1.0}, ...]},
        {"name": "CSI 300", "points": [{"date": "2025-01-20", "value": 1.0}, ...]},
    ],
}
```

### `custom_html` - Donut Chart (Weight Distribution)

```python
{
    "type": "custom_html",
    "tab": "overview",
    "title": "Constituent Weight Distribution",
    "width": "half",
    "html": """
        <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
        <div id="es-custom-weight-donut" style="height:320px;"></div>
    """,
    "mount_script": """
        const el = host.querySelector('#es-custom-weight-donut');
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const chart = echarts.init(el, isDark ? 'dark' : null);
        const data = module.chart_data || [];
        chart.setOption({
            backgroundColor: 'transparent',
            tooltip: { trigger: 'item', formatter: '{b}: {d}%' },
            series: [{
                type: 'pie',
                radius: ['42%', '70%'],
                label: { color: isDark ? '#d1d4dc' : '#131722', fontSize: 12 },
                data: data,
            }],
        });
        new ResizeObserver(() => chart.resize()).observe(el);
    """,
    "chart_data": [
        {"name": "Hygon Information", "value": 49.2},
        {"name": "Dawning Information", "value": 12.8},
        {"name": "Other", "value": 38.0},
    ],
}
```

### `custom_html` - Horizontal Bar Chart (Per-Stock Return Contribution)

```python
{
    "type": "custom_html",
    "tab": "overview",
    "title": "Per-stock Return Contribution",
    "width": "half",
    "html": """
        <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
        <div id="es-custom-stock-impact" style="height:400px;"></div>
    """,
    "mount_script": """
        const el = host.querySelector('#es-custom-stock-impact');
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const chart = echarts.init(el, isDark ? 'dark' : null);
        const names = module.bar_names || [];
        const values = module.bar_values || [];
        const market = module.market || 'china_a';  // 'china_a' or 'us'
        const upColor = market === 'us' ? '#26a69a' : '#ef5350';   // US up = green, China A-share up = red
        const downColor = market === 'us' ? '#ef5350' : '#26a69a'; // US down = red, China A-share down = green
        chart.setOption({
            backgroundColor: 'transparent',
            tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
            grid: { left: 100, right: 30, top: 10, bottom: 30 },
            xAxis: { type: 'value', axisLabel: { formatter: '{value}%' } },
            yAxis: { type: 'category', data: names, inverse: true,
                     axisLabel: { color: isDark ? '#d1d4dc' : '#131722' } },
            series: [{
                type: 'bar',
                data: values.map(v => ({
                    value: v,
                    itemStyle: { color: v >= 0 ? upColor : downColor }
                })),
            }],
        });
        new ResizeObserver(() => chart.resize()).observe(el);
    """,
    "market": "china_a",
    "bar_names":  ["Hygon Information", "Dawning Information", "Cambricon", ...],
    "bar_values": [35.6, 28.1, 22.3, ...],
}
```

### `custom_html` - Area Chart (Market-Cap Distribution)

```python
{
    "type": "custom_html",
    "tab": "overview",
    "title": "Constituent Market-Cap Distribution",
    "width": "full",
    "html": """
        <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
        <div id="es-custom-mcap-area" style="height:280px;"></div>
    """,
    "mount_script": """
        const el = host.querySelector('#es-custom-mcap-area');
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const chart = echarts.init(el, isDark ? 'dark' : null);
        const names = module.area_names || [];
        const caps = module.area_values || [];
        chart.setOption({
            backgroundColor: 'transparent',
            tooltip: { trigger: 'axis' },
            xAxis: { type: 'category', data: names, axisLabel: { rotate: 45, fontSize: 10 } },
            yAxis: { type: 'value', name: 'Market Cap (B CNY)' },
            series: [{
                type: 'bar',
                data: caps,
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#2962ff' },
                        { offset: 1, color: 'rgba(41,98,255,0.15)' },
                    ]),
                },
                areaStyle: { opacity: 0.25 },
            }],
        });
        new ResizeObserver(() => chart.resize()).observe(el);
    """,
    "area_names":  ["Hygon Information", "Dawning Information", ...],
    "area_values": [3218.5, 1456.2, ...],
}
```

### `trades_table` Reused As Constituent Details

Remap the `trades_table` column semantics to constituent data. Override column labels through `ui.i18n`:

```python
{
    "type": "trades_table",
    "tab": "overview",
    "title": "Constituent Details",
    "rows": [
        {
            "symbol": "寒武纪",           # zh: stock name only; en: ticker/symbol only
            "side": "T1",                    # reuse side for tier
            "entry_date": "Hygon Information",  # reuse for name
            "exit_date": "Semiconductors",   # reuse for industry
            "holding_bars": "",
            "size": "",
            "entry_price": 49.2,             # reuse for weight (%)
            "exit_price": 3218.5,            # reuse for market cap (B CNY)
            "pnl": 35.6,                     # return (%)
            "pnl_pct": 35.6,
        },
        ...
    ],
}
```

Matching `ui.i18n` override:

```python
"i18n": {
    "trades_col_symbol":      "名称",     # en: "Ticker"
    "trades_col_side":        "Tier",
    "trades_col_entry_date":  "Name",
    "trades_col_exit_date":   "Industry",
    "trades_col_holding":     "",
    "trades_col_size":        "",
    "trades_col_entry_price": "Weight (%)",
    "trades_col_exit_price":  "Market Cap (B CNY)",
    "trades_col_pnl":         "Return",
    "trades_col_pnl_pct":     "Return (%)",
}
```

> **Note**: if the `trades_table` column mapping becomes too awkward, for example because columns need to be hidden or added, injecting a full HTML `<table>` through `custom_html` is cleaner.

## `custom_html` Conventions

| Convention | Description |
|---|---|
| DOM id / CSS class prefix | Use **`es-custom-<name>`** to avoid conflicts with the template and backtest-dashboard elements |
| echarts CDN | `<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>`, loaded through the `html` field |
| Dark-theme support | In `mount_script`, check `document.documentElement.getAttribute('data-theme') === 'dark'`; initialize echarts with the `'dark'` theme and set background to `'transparent'` |
| Responsiveness | Use `new ResizeObserver(() => chart.resize()).observe(el)` to handle container-size changes |
| Custom data | Put extra data on custom fields in the module dict, such as `chart_data` or `bar_names`; access it through `module.xxx` in `mount_script` |
| Language consistency | All titles, tooltips, and labels must match dashboard `language`; explicitly pass `language="zh"` or `language="en"` when needed |
| Error handling | `mount_script` errors are caught and appended to the card bottom as `<pre class="custom-html-error">` |

## Implementation Floor

- Output must be a **single-file HTML** document with no backend dependency.
- Dashboard assembly logic must stay separate from the event-study calculation script.
- Curves and tables must be read from the standard output files; do not bypass standard files and recalculate metrics ad hoc.
- Include at least: KPI cards + NAV curve + constituent detail table. Use `custom_html` for task-specific charts such as weights, contribution, and market cap.
- Do not skip the dashboard merely because there are no real buy/sell trades.
