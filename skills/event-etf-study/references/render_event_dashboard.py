"""
Event-study ETF dashboard renderer.

Reads the standard portfolio and summary files produced by export_event_results,
assembles a report_data dict, replaces the __REPORT_DATA__ placeholder in
dashboard_template.html, and writes a standalone HTML file.

This is a copyable example. The LLM can call it directly, or adjust the modules
list for a specific task.

Usage:
    from reference.render_event_dashboard import generate_event_dashboard

    # Generate all charts by default.
    generate_event_dashboard(
        prefix="openclaw_etf",
        output_path="output/openclaw_dashboard.html",
        data_dir=".",
        template_path=None,
        language="zh",  # pass a concrete "zh" or "en"; avoid "auto" in final runs
    )

    # Model-selected concise dashboard: overview + NAV + table only.
    generate_event_dashboard(
        prefix="openclaw_etf",
        output_path="output/openclaw_dashboard.html",
        include_modules=["overview", "nav", "table"],
    )

Command line:
    python render_event_dashboard.py openclaw_etf output/dashboard.html
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Locales
# ---------------------------------------------------------------------------

LOCALES: dict[str, dict[str, Any]] = {
    "zh": {
        "tab_overview": "总览",
        "subtitle": "事件研究 ETF 看板",
        "kpi_num_stocks": "成分股数量",
        "kpi_pre_event_mcap": "事件前总市值",
        "kpi_peak_chg": "峰值市值涨幅",
        "kpi_latest_chg": "最新市值变动",
        "kpi_etf_return": "ETF 净值回报",
        "chart_nav_title": "ETF 净值走势",
        "chart_nav_mcap": "市值加权",
        "chart_nav_equal": "等权",
        "chart_weight_title": "成分股权重分布",
        "chart_impact_title": "个股事件影响",
        "chart_mcap_title": "总市值走势",
        "table_title": "成分股明细",
        "table_subtitle": "按权重降序排列",
        "unit_billion": "亿元",
        "toggle_drawdown": "回撤",
        "mode_absolute": "绝对值",
        "mode_percentage": "百分比",
        "label_weight": "权重",
        "i18n": {
            "html_lang": "zh-CN",
            "strategy_fallback": "策略",
            "subtitle_fallback": "事件研究 ETF 看板",
            "event_date_label": "事件日",
            "brand": "事件研究",
            "status_ready": "就绪",
            "theme_toggle": "切换主题",
            "drawdown_pane": "回撤",
            "tooltip_equity": "净值",
            "tooltip_return": "收益",
            "tooltip_drawdown": "回撤",
            "empty_data": "暂无数据",
            "empty_trades": "暂无成分股",
            "empty_content": "暂无内容",
            "trades_col_symbol": "名称",
            "trades_col_side": "梯队",
            "trades_col_entry_date": "事件日涨跌",
            "trades_col_exit_date": "峰值涨跌",
            "trades_col_holding": "最新涨跌",
            "trades_col_size": "权重%",
            "trades_col_entry_price": "市值(亿)",
            "trades_col_exit_price": "",
            "trades_col_pnl": "",
            "trades_col_pnl_pct": "",
            "side_long": "T1",
            "side_short": "T3",
            "marker_buy": "买入",
            "marker_sell": "卖出",
            "marker_short": "做空",
            "marker_cover": "平空",
            "marker_pnl": "盈亏",
        },
    },
    "en": {
        "tab_overview": "Overview",
        "subtitle": "Event Study ETF Dashboard",
        "kpi_num_stocks": "Constituents",
        "kpi_pre_event_mcap": "Pre-event Mkt Cap",
        "kpi_peak_chg": "Peak Mkt Cap Chg",
        "kpi_latest_chg": "Latest Mkt Cap Chg",
        "kpi_etf_return": "ETF Return",
        "chart_nav_title": "ETF NAV",
        "chart_nav_mcap": "Cap-weighted",
        "chart_nav_equal": "Equal-weighted",
        "chart_weight_title": "Constituent Weights",
        "chart_impact_title": "Per-stock Event Impact",
        "chart_mcap_title": "Total Market Cap",
        "table_title": "Constituent Details",
        "table_subtitle": "Sorted by weight descending",
        "unit_billion": "B CNY",
        "toggle_drawdown": "Drawdown",
        "mode_absolute": "Absolute",
        "mode_percentage": "Percentage",
        "label_weight": "Weight",
        "i18n": {
            "html_lang": "en",
            "strategy_fallback": "Strategy",
            "subtitle_fallback": "Event Study ETF Dashboard",
            "event_date_label": "Event Date",
            "brand": "Event Study",
            "status_ready": "READY",
            "theme_toggle": "Toggle theme",
            "drawdown_pane": "DRAWDOWN",
            "tooltip_equity": "NAV",
            "tooltip_return": "Return",
            "tooltip_drawdown": "Drawdown",
            "empty_data": "No data",
            "empty_trades": "No constituents",
            "empty_content": "No content",
            "trades_col_symbol": "Ticker",
            "trades_col_side": "Tier",
            "trades_col_entry_date": "Event Day Chg",
            "trades_col_exit_date": "Peak Chg",
            "trades_col_holding": "Latest Chg",
            "trades_col_size": "Weight%",
            "trades_col_entry_price": "Mkt Cap(B)",
            "trades_col_exit_price": "",
            "trades_col_pnl": "",
            "trades_col_pnl_pct": "",
            "side_long": "T1",
            "side_short": "T3",
            "marker_buy": "Buy",
            "marker_sell": "Sell",
            "marker_short": "Short",
            "marker_cover": "Cover",
            "marker_pnl": "PnL",
        },
    },
}

DEFAULT_LANGUAGE = "en"
LANGUAGE_CHOICES = ("auto", "zh", "en")
_CJK_RE = re.compile(r"[\u3400-\u9fff]")
_LATIN_RE = re.compile(r"[A-Za-z]")
_AUTO_LANGUAGE_VALUES = {"", "auto"}

# ---------------------------------------------------------------------------
# Market-aware color scheme
# ---------------------------------------------------------------------------

# China A-shares: up = red, down = green. US equities: up = green, down = red.
MARKET_COLORS: dict[str, dict[str, str]] = {
    "china_a": {
        "up": "#ef5350",                 # red - gains / positive return
        "down": "#26a69a",               # green - losses / negative return / drawdown
        "up_stroke": "#ef5350",          # NAV line, up color
        "up_area": "rgba(239,83,80,0.12)",   # NAV area fill
        "down_bars": "rgba(38,166,154,0.40)", # drawdown bars / area
    },
    "us": {
        "up": "#26a69a",                 # green - gains / positive return
        "down": "#ef5350",               # red - losses / negative return / drawdown
        "up_stroke": "#26a69a",          # NAV line, up color
        "up_area": "rgba(38,166,154,0.12)",   # NAV area fill
        "down_bars": "rgba(239,83,80,0.40)",  # drawdown bars / area
    },
}
DEFAULT_MARKET = "china_a"


# ---------------------------------------------------------------------------
# Available module registry
# ---------------------------------------------------------------------------

# Module IDs that _build_modules understands. Passed via include_modules.
AVAILABLE_MODULE_IDS = ["overview", "nav", "weight", "impact", "mcap", "table"]


def _L(language: str | None) -> dict[str, Any]:
    return LOCALES.get(resolve_language(language), LOCALES[DEFAULT_LANGUAGE])


def resolve_language(
    language: str | None = "auto",
    *texts: object,
    default: str = DEFAULT_LANGUAGE,
) -> str:
    """Resolve ``auto``/aliases to a supported dashboard language.

    ``auto`` checks texts in order, so the original query can win over
    placeholder/fallback names. Within one text, CJK wins over Latin.
    Callers should pass the original user query when available, followed by
    event/ETF names as fallbacks.
    """
    value = (language or "auto").strip().lower().replace("_", "-")
    if value in {"zh", "zh-cn", "zh-hans", "cn", "chinese"}:
        return "zh"
    if value in {"en", "en-us", "en-gb", "english"}:
        return "en"
    if value not in _AUTO_LANGUAGE_VALUES:
        raise ValueError(f"language must be 'zh', 'en', or 'auto', got {language!r}")

    for text in texts:
        if text is None:
            continue
        value = str(text).strip()
        if not value:
            continue
        if _CJK_RE.search(value):
            return "zh"
        if _LATIN_RE.search(value):
            return "en"
    return default


def _is_auto_language(language: str | None) -> bool:
    return (language or "auto").strip().lower().replace("_", "-") in _AUTO_LANGUAGE_VALUES


def _html_lang(language: str | None) -> str:
    return "zh-CN" if resolve_language(language) == "zh" else "en"


def _resolve_dashboard_language(language: str | None, meta: dict[str, Any]) -> str:
    if not _is_auto_language(language):
        resolved = resolve_language(language)
        summary_language = meta.get("language")
        if summary_language and resolve_language(summary_language) != resolved:
            raise ValueError(
                "Dashboard language conflicts with summary.meta.language: "
                f"{resolved!r} != {summary_language!r}"
            )
        return resolved

    summary_language = meta.get("language")
    if summary_language:
        return resolve_language(summary_language)

    query = str(meta.get("query") or "").strip()
    if query:
        return resolve_language("auto", query)

    raise ValueError(
        "Dashboard language is auto, but summary.meta.language and "
        "summary.meta.query are missing; pass language='zh' or language='en'."
    )


# ---------------------------------------------------------------------------
# File readers
# ---------------------------------------------------------------------------

def _read_portfolio_csv(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "date": row["date"],
                "mcap_weighted_nav": _safe_float(row.get("mcap_weighted_nav")),
                "equal_weighted_nav": _safe_float(row.get("equal_weighted_nav")),
                "total_market_cap": _safe_float(row.get("total_market_cap")),
            })
    return rows


def _read_summary_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Dashboard data builder
# ---------------------------------------------------------------------------

def build_event_dashboard_data(
    prefix: str,
    data_dir: str | Path | None = None,
    language: str = "auto",
    include_modules: list[str] | None = None,
    custom_modules: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Read 3 standard files and build report_data dict for the template.

    Args:
        include_modules: Module IDs to include from AVAILABLE_MODULE_IDS.
            Defaults to all built-in modules.
            Example: ["overview", "nav", "table"] for a minimal dashboard.
        custom_modules: Extra module dicts to append after built-in ones.
            Use this to inject task-specific charts.
    """
    base = Path(data_dir) if data_dir else Path.cwd()

    portfolio_path = base / f"{prefix}_portfolio.csv"
    summary_path = base / f"{prefix}_summary.json"

    portfolio = _read_portfolio_csv(portfolio_path)
    summary_data = _read_summary_json(summary_path)

    meta_raw = summary_data.get("meta", {})
    summ_raw = summary_data.get("summary", {})
    constituents = summary_data.get("constituents", [])
    language = _resolve_dashboard_language(language, meta_raw)
    L = _L(language)

    # Build equity curve from portfolio NAV
    equity_curve = [
        {"date": p["date"], "value": p["mcap_weighted_nav"]}
        for p in portfolio if p["mcap_weighted_nav"] is not None
    ]

    # Build drawdown curve
    drawdown_curve = _build_drawdown_curve(equity_curve)

    # NAV stats
    first_nav = equity_curve[0]["value"] if equity_curve else 100.0
    final_nav = equity_curve[-1]["value"] if equity_curve else 100.0
    total_return_pct = (final_nav / first_nav - 1.0) * 100.0 if first_nav else 0.0
    max_dd = abs(min(p["drawdown_pct"] for p in drawdown_curve)) if drawdown_curve else 0.0

    # report_data structure
    report_data = {
        "meta": {
            "strategy_name": meta_raw.get("etf_name", prefix),
            "symbol": "概念ETF" if language == "zh" else "Concept ETF",
            "start": meta_raw.get("start", portfolio[0]["date"] if portfolio else ""),
            "end": meta_raw.get("end", portfolio[-1]["date"] if portfolio else ""),
            "initial_cash": 100.0,
            "window_start_value": first_nav,
            "final_value": final_nav,
            "market": meta_raw.get("market", DEFAULT_MARKET),
            "generated_at": meta_raw.get(
                "generated_at",
                datetime.now().astimezone().isoformat(timespec="seconds"),
            ),
            # Event-study specific fields
            "event_date": meta_raw.get("event_date"),
            "pre_event_date": meta_raw.get("pre_event_date"),
            "event_name": meta_raw.get("event_name"),
            "etf_name": meta_raw.get("etf_name"),
            "language": language,
        },
        "summary": {
            "total_return_pct": total_return_pct,
            "annual_return_pct": None,
            "max_drawdown_pct": max_dd,
            "sharpe": None,
            "win_rate_pct": None,
            "total_trades": meta_raw.get("num_stocks", len(constituents)),
        },
        "equity_curve": equity_curve,
        "drawdown_curve": drawdown_curve,
        "trade_history": [],
        # Extra data for custom modules
        "_event_study": {
            "portfolio": portfolio,
            "summary": summ_raw,
            "meta": meta_raw,
            "constituents": constituents,
        },
    }

    report_data["ui"] = _build_ui(report_data, language)
    report_data["modules"] = _build_modules(
        report_data, language,
        include_modules=include_modules,
        custom_modules=custom_modules,
    )

    return report_data


# ---------------------------------------------------------------------------
# UI builder
# ---------------------------------------------------------------------------

def _build_ui(report_data: dict, language: str) -> dict[str, Any]:
    L = _L(language)
    return {
        "subtitle": L["subtitle"],
        "active_tab": "overview",
        "tabs": [{"id": "overview", "label": L["tab_overview"]}],
        "topbar_menu": [],
            "window_status": "",
            "language": language or DEFAULT_LANGUAGE,
            "html_lang": _html_lang(language),
            "i18n": L["i18n"],
        }


# ---------------------------------------------------------------------------
# Module builders
# ---------------------------------------------------------------------------

def _build_modules(
    report_data: dict,
    language: str,
    include_modules: list[str] | None = None,
    custom_modules: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build modules list. Models can select which charts to include.

    Args:
        include_modules: List of module IDs from AVAILABLE_MODULE_IDS.
            Defaults to all if None.
            Order matters: modules appear in the dashboard in this order.
        custom_modules: Additional modules to append after built-ins.
    """
    L = _L(language)
    es = report_data.get("_event_study", {})
    portfolio = es.get("portfolio", [])
    summ = es.get("summary", {})
    meta = es.get("meta", {})
    constituents = es.get("constituents", [])
    equity_curve = report_data.get("equity_curve", [])
    drawdown_curve = report_data.get("drawdown_curve", [])
    event_date = meta.get("event_date", "")
    unit = L["unit_billion"]
    market = report_data.get("meta", {}).get("market", DEFAULT_MARKET)
    colors = MARKET_COLORS.get(market, MARKET_COLORS[DEFAULT_MARKET])

    # Determine which modules to include
    selected = include_modules if include_modules is not None else AVAILABLE_MODULE_IDS[:]
    # Filter to valid IDs only
    selected = [m for m in selected if m in AVAILABLE_MODULE_IDS]

    modules: list[dict[str, Any]] = []

    for mod_id in selected:
        if mod_id == "overview":
            modules.append(_build_overview_module(
                report_data, equity_curve, drawdown_curve, portfolio, summ, meta, constituents, L, language, colors
            ))
        elif mod_id == "nav":
            modules.append(_build_nav_line_chart(portfolio, event_date, language))
        elif mod_id == "weight":
            modules.append(_build_weight_donut(constituents, language))
        elif mod_id == "impact":
            modules.append(_build_impact_bar(constituents, language, colors))
        elif mod_id == "mcap":
            modules.append(_build_mcap_area(portfolio, event_date, language))
        elif mod_id == "table":
            table_rows = _build_constituent_table_rows(constituents, language)
            modules.append({
                "type": "trades_table",
                "tab": "overview",
                "title": L["table_title"],
                "subtitle": L["table_subtitle"],
                "rows": table_rows,
            })

    # Append custom modules if provided
    if custom_modules:
        modules.extend(custom_modules)

    return modules


def _build_overview_module(
    report_data: dict,
    equity_curve: list[dict],
    drawdown_curve: list[dict],
    portfolio: list[dict],
    summ: dict,
    meta: dict,
    constituents: list[dict],
    L: dict,
    language: str,
    colors: dict[str, str],
) -> dict[str, Any]:
    """Build the overview chart with KPI cards."""
    pre_mcap = summ.get("pre_event_mcap", 0)
    peak_mcap = summ.get("peak_mcap", 0)
    latest_mcap = summ.get("latest_mcap", 0)
    peak_chg = summ.get("mcap_change_to_peak_pct", 0)
    latest_chg = summ.get("mcap_change_to_latest_pct", 0)
    etf_ret = summ.get("etf_return_total_pct", 0)
    equity_color = colors["up"] if (etf_ret or 0) >= 0 else colors["down"]

    overview_stats = [
        {"label": L["kpi_num_stocks"], "value": str(meta.get("num_stocks", len(constituents)))},
        {"label": L["kpi_pre_event_mcap"], "value": f"{pre_mcap:,.0f}{L['unit_billion']}"},
        {"label": L["kpi_peak_chg"], "value": _fmt_pct(peak_chg),
         "raw": peak_chg},
        {"label": L["kpi_latest_chg"], "value": _fmt_pct(latest_chg),
         "raw": latest_chg},
        {"label": L["kpi_etf_return"], "value": _fmt_pct(etf_ret),
         "raw": etf_ret},
    ]

    overview_points = [
        {
            "date": p["date"],
            "equity": p.get("value", 100),
            "drawdown_abs": abs(dd.get("drawdown_pct", 0)) if (dd := _find_dd(drawdown_curve, p["date"])) else 0,
            "pnl": (p.get("value", 100) - 100),
        }
        for p in equity_curve
    ]

    return {
        "type": "overview_chart",
        "tab": "overview",
        "width": "full",
        "stats": overview_stats,
        "points": overview_points,
        "markers": [],
        "series_key": "equity",
        "stroke": equity_color,
        "bars_key": "drawdown_abs",
        "bars_fill": colors["down_bars"],
        "toggles": [
            {"id": "equity", "label": L["chart_nav_mcap"], "color": equity_color, "checked": True},
            {"id": "drawdown", "label": L["toggle_drawdown"], "color": colors["down"], "checked": True},
        ],
        "modes": [
            {"id": "absolute", "label": L["mode_absolute"], "active": True},
            {"id": "percentage", "label": L["mode_percentage"], "active": False},
        ],
    }


# ---------------------------------------------------------------------------
# Custom HTML module builders
# ---------------------------------------------------------------------------

def _build_nav_line_chart(portfolio: list[dict], event_date: str, language: str) -> dict[str, Any]:
    """NAV dual-line chart with distinct blue colors and spaced legend (custom echarts)."""
    L = _L(language)
    dates = [p["date"] for p in portfolio if p["mcap_weighted_nav"] is not None]
    mcap_vals = [round(p["mcap_weighted_nav"], 2) for p in portfolio if p["mcap_weighted_nav"] is not None]
    eq_vals = [round(p["equal_weighted_nav"], 2) for p in portfolio if p["equal_weighted_nav"] is not None]
    dates_json = json.dumps(dates)
    mcap_json = json.dumps(mcap_vals)
    eq_json = json.dumps(eq_vals)
    label_mcap = L["chart_nav_mcap"]
    label_eq = L["chart_nav_equal"]
    event_label = "事件日" if language == "zh" else "Event"
    return {
        "type": "custom_html",
        "tab": "overview",
        "title": L["chart_nav_title"],
        "width": "full",
        "html": """
            <div id="es-custom-nav-line" style="height:380px;width:100%;"></div>
        """,
        "mount_script": f"""
            (function() {{
                var el = host.querySelector('#es-custom-nav-line');
                if (!el) return;
                var chart = echarts.init(el);
                chart.setOption({{
                    backgroundColor: 'transparent',
                    tooltip: {{ trigger: 'axis', backgroundColor: 'rgba(255,255,255,0.96)', borderColor: '#cbd5e1', textStyle: {{ color: '#1e293b', fontSize: 13 }} }},
                    legend: {{ data: ['{label_mcap}', '{label_eq}'], top: 8, textStyle: {{ color: '#1e293b', fontSize: 14, fontWeight: 600 }}, itemWidth: 20, itemHeight: 12, itemGap: 40 }},
                    grid: {{ left: 56, right: 24, top: 50, bottom: 36, containLabel: false }},
                    xAxis: {{ type: 'category', data: {dates_json}, axisLabel: {{ color: '#475569', fontSize: 12, fontWeight: 500 }}, axisLine: {{ lineStyle: {{ color: '#94a3b8' }} }} }},
                    yAxis: {{ type: 'value', axisLabel: {{ color: '#475569', fontSize: 12, fontWeight: 500 }}, splitLine: {{ lineStyle: {{ color: '#e2e8f0' }} }} }},
                    series: [
                        {{ name: '{label_mcap}', type: 'line', data: {mcap_json}, smooth: 0.25, symbol: 'none', lineStyle: {{ color: '#3b82f6', width: 2.5 }}, itemStyle: {{ color: '#3b82f6' }} }},
                        {{ name: '{label_eq}', type: 'line', data: {eq_json}, smooth: 0.25, symbol: 'none', lineStyle: {{ color: '#f97316', width: 2.5, type: 'dashed' }}, itemStyle: {{ color: '#f97316' }} }},
                    ],
                }});
                chart.setOption({{
                    series: [{{ markLine: {{
                        silent: true, symbol: 'none',
                        lineStyle: {{ color: '#ef4444', type: 'dashed', width: 1.2 }},
                        data: [{{ xAxis: '{event_date}', label: {{ formatter: '{event_label}', color: '#fff', fontSize: 13, fontWeight: 600, backgroundColor: 'rgba(239,68,68,0.85)', padding: [3,8], borderRadius: 3 }} }}],
                    }} }}, {{}}],
                }});
                new ResizeObserver(function() {{ chart.resize(); }}).observe(el);
            }})();
        """,
    }


TIER_COLORS = {"1": "#3b82f6", "2": "#60a5fa", "3": "#93c5fd"}
TIER_LABELS_ZH = {"1": "T1-核心", "2": "T2-强相关", "3": "T3-生态"}
TIER_LABELS_EN = {"1": "T1-Core", "2": "T2-Related", "3": "T3-Ecosystem"}


def _build_weight_donut(constituents: list[dict], language: str) -> dict[str, Any]:
    L = _L(language)
    tier_labels = TIER_LABELS_ZH if language == "zh" else TIER_LABELS_EN
    weight_label = L["label_weight"]

    # Aggregate by tier
    tier_data = {}
    for c in constituents:
        t = str(c.get("tier", 3))
        tier_data.setdefault(t, {"weight": 0, "stocks": []})
        tier_data[t]["weight"] += c.get("weight", 0)
        tier_data[t]["stocks"].append(_constituent_label(c, language))

    chart_data = []
    for t in sorted(tier_data.keys()):
        label = tier_labels.get(t, f"T{t}")
        chart_data.append({
            "name": f"{label} ({len(tier_data[t]['stocks'])})",
            "value": round(tier_data[t]["weight"], 2),
        })

    data_json = json.dumps(chart_data, ensure_ascii=False)
    colors_json = json.dumps([TIER_COLORS.get(t, "#94a3b8") for t in sorted(tier_data.keys())])

    return {
        "type": "custom_html",
        "tab": "overview",
        "title": L["chart_weight_title"],
        "width": "half",
        "html": f"""
            <div id="es-custom-weight-donut" style="height:400px;width:100%;"></div>
        """,
        "mount_script": f"""
            (function() {{
                var el = host.querySelector('#es-custom-weight-donut');
                if (!el) return;
                var chart = echarts.init(el);
                chart.setOption({{
                    backgroundColor: 'transparent',
                    tooltip: {{ trigger: 'item', formatter: '{{b}}<br/>{weight_label}: {{c}}%', backgroundColor: 'rgba(255,255,255,0.96)', borderColor: '#cbd5e1', textStyle: {{ color: '#1e293b', fontSize: 14 }} }},
                    color: {colors_json},
                    series: [{{
                        type: 'pie',
                        radius: ['38%', '65%'],
                        center: ['50%', '50%'],
                        avoidLabelOverlap: true,
                        itemStyle: {{ borderRadius: 4, borderColor: '#fff', borderWidth: 3 }},
                        label: {{ show: true, color: '#1e293b', fontSize: 15, fontWeight: 700, formatter: '{{b}}\\n{{d}}%' }},
                        labelLine: {{ length: 18, length2: 12, lineStyle: {{ color: '#94a3b8', width: 1.5 }} }},
                        emphasis: {{ itemStyle: {{ shadowBlur: 12, shadowColor: 'rgba(59,130,246,0.35)' }}, label: {{ fontSize: 16, fontWeight: 800 }} }},
                        data: {data_json},
                    }}],
                }});
                new ResizeObserver(function() {{ chart.resize(); }}).observe(el);
            }})();
        """,
    }


def _build_impact_bar(constituents: list[dict], language: str, colors: dict[str, str]) -> dict[str, Any]:
    L = _L(language)
    # Sort by weight descending, limit to top 15 for readability
    sorted_c = sorted(constituents, key=lambda x: x.get("weight", 0), reverse=True)[:15]
    sorted_c.reverse()  # echarts horizontal bar renders bottom-to-top

    names = [_constituent_label(c, language) for c in sorted_c]
    event_day = [c.get("event_day_chg") or 0 for c in sorted_c]
    peak = [c.get("peak_chg") or 0 for c in sorted_c]
    latest = [c.get("latest_chg") or 0 for c in sorted_c]

    names_json = json.dumps(names, ensure_ascii=False)
    event_json = json.dumps(event_day)
    peak_json = json.dumps(peak)
    latest_json = json.dumps(latest)

    legend = ["事件日涨跌%", "峰值涨跌%", "至今涨跌%"] if language == "zh" else ["Event Day %", "Peak %", "Latest %"]
    legend_json = json.dumps(legend, ensure_ascii=False)
    up_label = "上涨" if language == "zh" else "Up"
    down_label = "下跌" if language == "zh" else "Down"
    metric_hint = "每组柱：事件日 / 峰值 / 至今" if language == "zh" else "Bars per row: event day / peak / latest"

    up_color = colors["up"]
    down_color = colors["down"]

    return {
        "type": "custom_html",
        "tab": "overview",
        "title": L["chart_impact_title"],
        "width": "half",
        "html": f"""
            <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin:2px 0 8px 0;color:#1e293b;font-size:14px;font-weight:600;">
                <span style="display:inline-flex;align-items:center;gap:7px;"><i style="display:inline-block;width:18px;height:12px;border-radius:3px;background:{up_color};"></i>{up_label}</span>
                <span style="display:inline-flex;align-items:center;gap:7px;"><i style="display:inline-block;width:18px;height:12px;border-radius:3px;background:{down_color};"></i>{down_label}</span>
                <span style="color:#64748b;font-size:13px;font-weight:500;">{metric_hint}</span>
            </div>
            <div id="es-custom-impact-bar" style="height:490px;width:100%;"></div>
        """,
        "mount_script": f"""
            (function() {{
                var el = host.querySelector('#es-custom-impact-bar');
                if (!el) return;
                var chart = echarts.init(el);
                var upColor = '{up_color}';
                var downColor = '{down_color}';
                function colorByValue(val) {{
                    return val >= 0 ? upColor : downColor;
                }}
                chart.setOption({{
                    backgroundColor: 'transparent',
                    tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'shadow' }}, backgroundColor: 'rgba(255,255,255,0.96)', borderColor: '#cbd5e1', textStyle: {{ color: '#1e293b', fontSize: 13 }} }},
                    legend: {{ show: false }},
                    grid: {{ left: 80, right: 28, top: 12, bottom: 32, containLabel: false }},
                    xAxis: {{ type: 'value', axisLabel: {{ formatter: '{{value}}%', color: '#475569', fontSize: 13, fontWeight: 500 }}, splitLine: {{ lineStyle: {{ color: '#e2e8f0' }} }} }},
                    yAxis: {{ type: 'category', data: {names_json}, axisLabel: {{ color: '#1e293b', fontSize: 14, fontWeight: 600 }}, axisTick: {{ show: false }}, axisLine: {{ lineStyle: {{ color: '#94a3b8' }} }} }},
                    series: [
                        {{ name: {legend_json}[0], type: 'bar', data: {event_json}, barGap: '20%', itemStyle: {{ color: function(p) {{ return colorByValue(p.value); }}, borderRadius: [0,3,3,0] }} }},
                        {{ name: {legend_json}[1], type: 'bar', data: {peak_json}, itemStyle: {{ color: function(p) {{ return colorByValue(p.value); }}, borderRadius: [0,3,3,0] }} }},
                        {{ name: {legend_json}[2], type: 'bar', data: {latest_json}, itemStyle: {{ color: function(p) {{ return colorByValue(p.value); }}, borderRadius: [0,3,3,0] }} }},
                    ],
                }});
                new ResizeObserver(function() {{ chart.resize(); }}).observe(el);
            }})();
        """,
    }


def _build_mcap_area(portfolio: list[dict], event_date: str, language: str) -> dict[str, Any]:
    L = _L(language)
    dates = [p["date"] for p in portfolio if p["total_market_cap"] is not None]
    values = [round(p["total_market_cap"], 1) for p in portfolio if p["total_market_cap"] is not None]

    dates_json = json.dumps(dates)
    values_json = json.dumps(values)
    event_label = "事件日" if language == "zh" else "Event"
    unit = L["unit_billion"]

    return {
        "type": "custom_html",
        "tab": "overview",
        "title": L["chart_mcap_title"],
        "width": "full",
        "html": """
            <div id="es-custom-mcap-area" style="height:340px;width:100%;"></div>
        """,
        "mount_script": f"""
            (function() {{
                var el = host.querySelector('#es-custom-mcap-area');
                if (!el) return;
                var chart = echarts.init(el);
                chart.setOption({{
                    backgroundColor: 'transparent',
                    tooltip: {{ trigger: 'axis', backgroundColor: 'rgba(255,255,255,0.96)', borderColor: '#cbd5e1', textStyle: {{ color: '#1e293b' }}, formatter: function(p) {{
                        return '<span style="color:#475569">' + p[0].axisValue + '</span><br/>' + p[0].marker + ' <b>' + p[0].value.toLocaleString() + '</b> {unit}';
                    }} }},
                    xAxis: {{ type: 'category', data: {dates_json}, axisLabel: {{ color: '#475569', fontSize: 12, fontWeight: 500 }}, axisLine: {{ lineStyle: {{ color: '#94a3b8' }} }} }},
                    yAxis: {{ type: 'value', axisLabel: {{ color: '#475569', fontSize: 12, fontWeight: 500 }},
                             splitLine: {{ lineStyle: {{ color: '#e2e8f0' }} }},
                             name: '{unit}', nameTextStyle: {{ color: '#475569', fontSize: 13, fontWeight: 600 }} }},
                    series: [{{
                        type: 'line',
                        data: {values_json},
                        smooth: 0.3,
                        symbol: 'none',
                        areaStyle: {{ color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            {{ offset: 0, color: 'rgba(59,130,246,0.28)' }},
                            {{ offset: 0.7, color: 'rgba(59,130,246,0.08)' }},
                            {{ offset: 1, color: 'rgba(59,130,246,0)' }}
                        ]) }},
                        lineStyle: {{ color: '#3b82f6', width: 2 }},
                        itemStyle: {{ color: '#3b82f6' }},
                        markLine: {{
                            silent: true,
                            symbol: 'none',
                            lineStyle: {{ color: '#ef4444', type: 'dashed', width: 1.2 }},
                            data: [{{ xAxis: '{event_date}', label: {{ formatter: '{event_label}', color: '#fff', fontSize: 13, fontWeight: 600, backgroundColor: 'rgba(239,68,68,0.85)', padding: [3,8], borderRadius: 3 }} }}],
                        }},
                    }}],
                }});
                new ResizeObserver(function() {{ chart.resize(); }}).observe(el);
            }})();
        """,
    }


# ---------------------------------------------------------------------------
# Constituent table (reuses trades_table module type)
# ---------------------------------------------------------------------------

def _build_constituent_table_rows(constituents: list[dict], language: str) -> list[dict[str, Any]]:
    """Map constituents to trades_table row format.

    The template's trades_table expects rows with these keys:
    symbol, side, entry_date, exit_date, holding_bars, size, entry_price, ...
    We repurpose them for constituent data.
    """
    rows = []
    for c in sorted(constituents, key=lambda x: x.get("weight", 0), reverse=True):
        rows.append({
            "symbol": _constituent_label(c, language),
            "side": f"T{c.get('tier', '?')}",
            "entry_date": _fmt_pct_val(c.get("event_day_chg")),
            "exit_date": _fmt_pct_val(c.get("peak_chg")),
            "holding_bars": _fmt_pct_val(c.get("latest_chg")),
            "size": f"{c.get('weight', 0):.1f}",
            "entry_price": f"{c.get('market_cap_billion', 0):,.1f}",
            "exit_price": c.get("reason", "") if resolve_language(language) == "zh" else "",
            "pnl": None,
            "pnl_pct": None,
        })
    return rows


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render_event_dashboard(
    report_data: dict[str, Any],
    output_path: str | Path,
    template_path: str | Path | None = None,
) -> Path:
    """Replace template placeholders and write HTML."""
    if template_path:
        tpl_file = Path(template_path)
    else:
        tpl_file = Path(__file__).with_name("dashboard_template.html")

    template = tpl_file.read_text(encoding="utf-8")

    # Clean _event_study before serializing (internal-only data)
    data_copy = {k: v for k, v in report_data.items() if not k.startswith("_")}

    language = report_data.get("meta", {}).get("language") or DEFAULT_LANGUAGE
    title = report_data.get("meta", {}).get("strategy_name") or "Event Study ETF"
    report_json = _json_for_html(data_copy)

    rendered = (
        template
        .replace("__REPORT_TITLE__", html.escape(title))
        .replace("__HTML_LANG__", html.escape(_html_lang(language)))
        .replace("__REPORT_DATA__", report_json)
    )

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(rendered, encoding="utf-8")
    return output_file


def generate_event_dashboard(
    prefix: str,
    output_path: str | Path,
    data_dir: str | Path | None = None,
    template_path: str | Path | None = None,
    language: str = "auto",
    include_modules: list[str] | None = None,
    custom_modules: list[dict[str, Any]] | None = None,
) -> Path:
    """Convenience wrapper: read files -> build data -> render HTML.

    Args:
        include_modules: Module IDs to include. Defaults to all built-ins.
        custom_modules: Extra module dicts to append after built-in ones.
    """
    report_data = build_event_dashboard_data(
        prefix=prefix,
        data_dir=data_dir,
        language=language,
        include_modules=include_modules,
        custom_modules=custom_modules,
    )
    return render_event_dashboard(
        report_data,
        output_path=output_path,
        template_path=template_path,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_drawdown_curve(equity_curve: list[dict]) -> list[dict]:
    curve = []
    peak = None
    for p in equity_curve:
        v = _safe_float(p.get("value"))
        if v is None:
            continue
        peak = v if peak is None else max(peak, v)
        dd_pct = (v / peak - 1.0) * 100.0 if peak else 0.0
        dd_abs = peak - v if peak else 0.0
        curve.append({
            "date": p["date"],
            "drawdown_pct": dd_pct,
            "drawdown_abs": dd_abs,
        })
    return curve


def _find_dd(drawdown_curve: list[dict], date_str: str) -> dict | None:
    for d in drawdown_curve:
        if d["date"] == date_str:
            return d
    return None


def _constituent_label(constituent: dict, language: str) -> str:
    ticker = str(constituent.get("ticker") or "").strip()
    name = str(constituent.get("name") or "").strip()
    if resolve_language(language) == "en":
        return ticker or name
    return name or ticker


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(result) or math.isinf(result):
        return None
    return result


def _fmt_pct(value: Any) -> str:
    if value is None:
        return "--"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return str(value)
    sign = "+" if v > 0 else ""
    return f"{sign}{v:.2f}%"


def _fmt_pct_val(value: Any) -> str:
    if value is None:
        return "--"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return str(value)
    sign = "+" if v > 0 else ""
    return f"{sign}{v:.2f}%"


def _json_for_html(data: dict[str, Any]) -> str:
    return (
        json.dumps(data, ensure_ascii=False, default=str)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate an HTML dashboard from standard event-study files"
    )
    parser.add_argument("prefix", help="Standard file prefix, e.g. openclaw_etf")
    parser.add_argument("output", help="Output HTML path")
    parser.add_argument("--data-dir", default=None, help="Directory containing standard files; defaults to cwd")
    parser.add_argument("--template", default=None, help="Custom dashboard template path")
    parser.add_argument("--language", default="auto", choices=LANGUAGE_CHOICES)
    args = parser.parse_args()

    path = generate_event_dashboard(
        prefix=args.prefix,
        output_path=args.output,
        data_dir=args.data_dir,
        template_path=args.template,
        language=args.language,
    )
    print(f"Dashboard rendered: {path}")


if __name__ == "__main__":
    main()
