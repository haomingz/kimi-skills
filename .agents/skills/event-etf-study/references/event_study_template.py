#!/usr/bin/env python3
"""
Event-study ETF analysis template (code skeleton).

Full demonstration: MCP data fetch -> ETF construction -> standard file export
-> HTML dashboard -> Matplotlib charts -> report.
After copying this file, the LLM usually only needs to edit the configuration
block to adapt it to a different event-study task.

Usage: copy to cwd, rename to <prefix>_analysis.py, edit the configuration
block, and run.
"""
from __future__ import annotations

import json
import csv
import io
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import requests

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

FONT = FontProperties(fname="/System/Library/Fonts/Supplemental/Arial Unicode.ttf")

# Import helper modules from the same directory.
SKILL_REF = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL_REF))
from export_event_results import export_event_results
from render_event_dashboard import generate_event_dashboard, resolve_language
from validate_event_outputs import validate_event_outputs

# ========== Configuration block (edit for each task) ==========
ETF_NAME       = "XXX Concept ETF"
EVENT_NAME     = "XXX Concept Stock Breakout"
QUERY          = ""                 # Original user query; used as the primary source for language resolution (CJK detection).
LANGUAGE       = ""                 # REQUIRED: set to "zh" or "en" after resolving from QUERY. Do not leave blank/auto in final runs.
EVENT_DATE     = "2026-03-09"     # Event breakout date.
EVENT_DATE_SOURCE = "user-specified/announcement URL/news URL"  # Required for event-date provenance.
PRE_EVENT_DATE = "2026-03-06"     # Weight reference date, usually the last trading day before the event.
DATA_START     = "2026-03-03"     # Data-window start: 3-5 trading days before the reference date.
DATA_END       = "2026-04-10"     # Data-window end: 2-3 trading days after the user's focus window.
OUTPUT_DIR     = "output"
PREFIX         = "xxx_concept_etf"
MARKET         = "china_a"        # "china_a"=China A-shares (red up, green down); "us"=US equities.
PRICE_ADJUSTMENT = "forward"      # Forward-adjusted; if the tool enum differs, record the actual value in the manifest.
GENERATED_AT   = "2026-04-10T18:00:00+08:00"  # Keep fixed for reproducible reruns.
RAW_DATA_DIR   = Path(OUTPUT_DIR) / "raw"
CONSTITUENT_SNAPSHOT = Path(OUTPUT_DIR) / f"{PREFIX}_constituents_sources.csv"

# Constituent list - tier: 1=core, 2=strongly related, 3=ecosystem.
# Keep name/reason in the same language as LANGUAGE; the exporter writes them verbatim.
CONSTITUENTS = [
    {"ticker": "XXXXXX.SH", "name": "XXX", "tier": 1, "reason": "Core exposure"},
    {"ticker": "XXXXXX.SZ", "name": "YYY", "tier": 2, "reason": "Upstream/downstream supply chain"},
    {"ticker": "XXXXXX.SZ", "name": "ZZZ", "tier": 3, "reason": "Indirect beneficiary"},
]

TEXT_ZH = {
    "data_window_rule": "参考日前3~5个交易日到用户关注期末+2~3个交易日",
    "plot_nav_cap": "市值加权",
    "plot_nav_equal": "等权",
    "plot_event_date": "事件日",
    "plot_nav_title": "{etf_name} - NAV 走势",
    "plot_nav_ylabel": "净值（基准=100）",
    "plot_event_day_pct": "事件日%",
    "plot_peak_pct": "峰值%",
    "plot_chg_xlabel": "涨跌幅 (%)",
    "plot_impact_title": "{etf_name} - 个股事件影响",
    "plot_mcap_title": "{etf_name} - 总市值（亿元）",
    "plot_mcap_ylabel": "亿元",
    "report_title": "{etf_name} - 事件研究报告",
    "overview": "概述",
    "event": "事件",
    "date": "日期",
    "pre_event_date": "参考日",
    "window": "窗口",
    "constituents": "成分股",
    "event_date_source": "事件日期来源",
    "price_adjustment": "复权口径",
    "generated_at": "固定生成时间",
    "missing_price_policy": "缺失价格处理",
    "key_metrics": "核心指标",
    "metric": "指标",
    "value": "值",
    "pre_event_mcap": "事件前总市值",
    "peak_mcap_chg": "峰值市值涨幅",
    "etf_total_return": "ETF 总回报",
    "equal_total_return": "等权总回报",
    "top_weight": "最大单股权重",
    "assumptions": "假设清单",
    "reference_date_reason": "参考日选择理由：事件前最后一个交易日",
    "constituent_selection": "成分股筛选：ifind 概念板块 + 人工梯队划分；来源快照 `{snapshot}`",
    "weighting": "权重方式：市值加权（参考日总市值）",
    "shares_basis": "总股本口径：总股本（含限售股）",
    "price_adjustment_bullet": "价格复权：{price_adjustment}",
    "missing_price_bullet": "缺失价格处理：{missing_policy}",
    "analysis_window": "分析窗口：{start} ~ {end}",
    "known_biases": "已知偏差",
    "survivorship_bias": "幸存者偏差：成分股为当前时点选取",
    "coverage_bias": "数据覆盖率：目标 {target} 只，实际 {actual} 只",
    "mcap_basis_bias": "市值口径：总股本×收盘价，未剔除限售股",
    "event_timing_bias": "事件日期模糊性：政策类事件可能被市场提前消化",
    "outputs": "产出物",
    "stocks_unit": "只",
    "mcap_unit": "亿",
}

TEXT_EN = {
    "data_window_rule": "3-5 trading days before the reference date through 2-3 trading days after the user focus window",
    "plot_nav_cap": "Cap-weighted",
    "plot_nav_equal": "Equal-weighted",
    "plot_event_date": "Event date",
    "plot_nav_title": "{etf_name} - NAV",
    "plot_nav_ylabel": "NAV (base=100)",
    "plot_event_day_pct": "Event day %",
    "plot_peak_pct": "Peak %",
    "plot_chg_xlabel": "Change (%)",
    "plot_impact_title": "{etf_name} - Per-stock Event Impact",
    "plot_mcap_title": "{etf_name} - Total Market Cap (B CNY)",
    "plot_mcap_ylabel": "B CNY",
    "report_title": "{etf_name} - Event Study Report",
    "overview": "Overview",
    "event": "Event",
    "date": "Date",
    "pre_event_date": "Reference Date",
    "window": "Window",
    "constituents": "Constituents",
    "event_date_source": "Event Date Source",
    "price_adjustment": "Price Adjustment",
    "generated_at": "Fixed Generated Time",
    "missing_price_policy": "Missing Price Policy",
    "key_metrics": "Key Metrics",
    "metric": "Metric",
    "value": "Value",
    "pre_event_mcap": "Pre-event Market Cap",
    "peak_mcap_chg": "Peak Market Cap Change",
    "etf_total_return": "ETF Total Return",
    "equal_total_return": "Equal-weighted Total Return",
    "top_weight": "Largest Single-stock Weight",
    "assumptions": "Assumptions",
    "reference_date_reason": "Reference date: last trading day before the event",
    "constituent_selection": "Constituent selection: ifind concept universe plus manual tiering; source snapshot `{snapshot}`",
    "weighting": "Weighting: market-cap weighted using reference-date market cap",
    "shares_basis": "Share basis: total shares outstanding, including restricted shares",
    "price_adjustment_bullet": "Price adjustment: {price_adjustment}",
    "missing_price_bullet": "Missing price handling: {missing_policy}",
    "analysis_window": "Analysis window: {start} ~ {end}",
    "known_biases": "Known Limitations",
    "survivorship_bias": "Survivorship bias: constituents are selected at the current point in time",
    "coverage_bias": "Data coverage: target {target}, actual {actual}",
    "mcap_basis_bias": "Market-cap basis: total shares x close price; free float is not isolated",
    "event_timing_bias": "Event timing ambiguity: policy events may be priced before the event date",
    "outputs": "Outputs",
    "stocks_unit": "",
    "mcap_unit": "B CNY",
}

TEXT = {
    "zh": TEXT_ZH,
    "en": TEXT_EN,
}


def current_language() -> str:
    """Return a concrete language code; fail fast if the query/config is ambiguous."""
    configured = (LANGUAGE or "").strip().lower().replace("_", "-")
    if configured in {"zh", "zh-cn", "zh-hans", "cn", "chinese"}:
        return "zh"
    if configured in {"en", "en-us", "en-gb", "english"}:
        return "en"
    if configured in {"", "auto"}:
        if str(QUERY).strip():
            return resolve_language("auto", QUERY)
        raise ValueError(
            "LANGUAGE must be set to 'zh' or 'en', or QUERY must contain the "
            "original user request for auto-detection."
        )
    raise ValueError(f"LANGUAGE must be 'zh' or 'en', got {LANGUAGE!r}")


def text() -> dict[str, str]:
    return TEXT[current_language()]


def stock_display_label(constituent: dict) -> str:
    """Display stocks as Chinese names for zh outputs and tickers for en outputs."""
    ticker = str(constituent.get("ticker") or "").strip()
    name = str(constituent.get("name") or "").strip()
    if current_language() == "en":
        return ticker or name
    return name or ticker

# ========== MCP call infrastructure ==========
MCP_URL = "http://localhost:1991/mcp/"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}

def mcp_call(method: str, params: dict | None = None) -> dict:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    resp = requests.post(MCP_URL, json=payload, headers=HEADERS, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"MCP error: {data['error']}")
    return data

def call_tool(name: str, arguments: dict) -> dict:
    return mcp_call("tools/call", {"name": name, "arguments": arguments})

def iter_tool_payloads(res: dict):
    """Yield JSON objects or CSV preview strings from common MCP response shapes."""
    result = res.get("result", {})
    if isinstance(result, list):
        yield result
        return
    if not isinstance(result, dict):
        return
    if isinstance(result, dict) and result.get("data_preview"):
        yield result["data_preview"]
    for item in result.get("content", []):
        text = item.get("text", "")
        if not text:
            continue
        try:
            yield json.loads(text)
        except (json.JSONDecodeError, TypeError):
            yield text

def parse_csv_preview(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text)))

# ========== Step 1: Data fetch ==========

def fetch_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """Fetch daily closes through MCP ifind_get_price -> DataFrame(date, ticker, close)."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for tk in tickers:
        print(f"  Fetching prices: {tk}")
        raw_path = RAW_DATA_DIR / f"{tk.replace('.', '_')}_prices.csv"
        res = call_tool("ifind_get_price", {
            "code": tk, "start_date": start, "end_date": end,
            "fields": "close", "period": "D",
            "adjust": PRICE_ADJUSTMENT,
            "file_path": str(raw_path),
        })
        for data in iter_tool_payloads(res):
            if isinstance(data, str) and "\n" in data:
                data = parse_csv_preview(data)
            if isinstance(data, list):
                for r in data:
                    close = r.get("close", r.get("\u6536\u76d8\u4ef7", r.get("thscode_close", 0)))
                    rows.append({"date": r.get("date", r.get("time", "")),
                                 "ticker": tk, "close": float(close)})
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No price data fetched; check MCP connectivity and tickers.")
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    return df

def fetch_total_shares(tickers: list[str]) -> dict[str, float]:
    """Fetch total shares through MCP ifind_get_stock_info -> {ticker: shares}."""
    smap: dict[str, float] = {}
    for tk in tickers:
        print(f"  Fetching total shares: {tk}")
        res = call_tool("ifind_get_stock_info", {
            "code": tk,
            "fields": "ths_total_shares_stock",
        })
        for data in iter_tool_payloads(res):
            if isinstance(data, str) and "\n" in data:
                data = parse_csv_preview(data)
            if isinstance(data, dict):
                smap[tk] = float(data.get(
                    "ths_total_shares_stock",
                    data.get("totalShares", data.get("total_shares", 0)),
                ))
            elif isinstance(data, list) and data:
                smap[tk] = float(data[0].get(
                    "ths_total_shares_stock",
                    data[0].get("totalShares", data[0].get("total_shares", 0)),
                ))
    if not smap:
        raise RuntimeError("No total-share data fetched.")
    return smap

# ========== Step 2: ETF construction and standard-file export ==========

def build_etf(prices_df: pd.DataFrame, shares_map: dict[str, float]) -> dict[str, Path]:
    """Call export_event_results to generate standard data files and run_manifest."""
    L = text()
    paths = export_event_results(
        constituents=CONSTITUENTS,  prices_df=prices_df,  shares_map=shares_map,
        event_date=EVENT_DATE,      pre_event_date=PRE_EVENT_DATE,
        prefix=PREFIX,              output_dir=OUTPUT_DIR,
        etf_name=ETF_NAME,         event_name=EVENT_NAME,
        market=MARKET,
        generated_at=GENERATED_AT,
        price_adjustment=PRICE_ADJUSTMENT,
        data_source="mshtools/ifind",
        language=current_language(),
        query=QUERY,
        run_metadata={
            "event_date_source": EVENT_DATE_SOURCE,
            "constituent_snapshot": str(CONSTITUENT_SNAPSHOT),
            "raw_data_dir": str(RAW_DATA_DIR),
            "mcp_url": MCP_URL,
            "data_window_rule": L["data_window_rule"],
        },
    )
    print(f"  Exported: {[str(p) for p in paths.values()]}")
    return paths

# ========== Step 3: Dashboard generation ==========

def build_dashboard() -> Path:
    """Read standard files and generate an interactive HTML dashboard."""
    html_path = Path(OUTPUT_DIR) / f"{PREFIX}_dashboard.html"
    path = generate_event_dashboard(
        prefix=PREFIX, output_path=html_path, data_dir=OUTPUT_DIR, language=current_language(),
    )
    print(f"  Dashboard: {path}")
    return path

# ========== Step 4: Matplotlib charts ==========

def plot_charts(focus_days_before: int = 5, focus_days_after: int = 10):
    """Generate standalone PNG charts from standard files.

    Args:
        focus_days_before: Trading days to keep before the event date for visualization (default 5).
        focus_days_after: Trading days to keep after the event date for visualization (default 10).
    """
    L = text()
    portfolio = pd.read_csv(Path(OUTPUT_DIR) / f"{PREFIX}_portfolio.csv")
    summary   = json.loads((Path(OUTPUT_DIR) / f"{PREFIX}_summary.json").read_text("utf-8"))
    constituents = summary.get("constituents", [])

    # Market colors: China A-shares use red up/green down; US equities use green up/red down.
    market = summary.get("meta", {}).get("market", "china_a")
    UP_COLOR   = "#ef5350" if market == "china_a" else "#22c55e"  # up color
    DOWN_COLOR = "#22c55e" if market == "china_a" else "#ef5350"  # down color

    # --- Window trim: focus near the event so wide windows do not dilute charts. ---
    portfolio["date"] = pd.to_datetime(portfolio["date"])
    event_dt = pd.to_datetime(EVENT_DATE)
    # Find the event date or the first trading day after it.
    mask_after = portfolio["date"] >= event_dt
    event_idx = mask_after.idxmax() if mask_after.any() else 0
    start_idx = max(0, event_idx - focus_days_before)
    end_idx = min(len(portfolio), event_idx + focus_days_after + 1)
    portfolio = portfolio.iloc[start_idx:end_idx].copy()
    # --------------------------------------------------------

    dates = portfolio["date"]

    # Dark theme.
    plt.rcParams.update({
        "figure.facecolor": "#0f172a", "axes.facecolor": "#1e293b",
        "axes.edgecolor": "#334155",   "axes.labelcolor": "#e2e8f0",
        "xtick.color": "#94a3b8",      "ytick.color": "#94a3b8",
        "grid.color": "#334155",        "grid.alpha": 0.5,
        "text.color": "#e2e8f0",
    })

    # Chart 1: NAV trend.
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(dates, portfolio["mcap_weighted_nav"], "#2dd4bf", lw=2, label=L["plot_nav_cap"])
    ax.plot(dates, portfolio["equal_weighted_nav"], "#f97316", lw=1.5, ls="--", label=L["plot_nav_equal"])
    if (portfolio["date"] == event_dt).any():
        ax.axvline(event_dt, color="#ef4444", ls="--", lw=1, label=L["plot_event_date"])
    ax.axhline(100, color="#64748b", ls=":", lw=0.8)
    ax.set_title(L["plot_nav_title"].format(etf_name=ETF_NAME), fontproperties=FONT, fontsize=14)
    ax.set_ylabel(L["plot_nav_ylabel"], fontproperties=FONT)
    ax.legend(prop=FONT); ax.grid(True); fig.tight_layout()
    fig.savefig(Path(OUTPUT_DIR) / f"{PREFIX}_nav.png", dpi=150); plt.close(fig)

    # Chart 2: Per-stock event impact.
    sc = sorted(constituents, key=lambda x: x.get("weight", 0), reverse=True)[:15]
    names = [stock_display_label(c) for c in sc]
    fig, ax = plt.subplots(figsize=(12, max(4, len(names) * 0.45)))
    y = np.arange(len(names)); h = 0.35
    ax.barh(y - h/2, [c.get("event_day_chg", 0) for c in sc], h, color="#f97316", label=L["plot_event_day_pct"])
    ax.barh(y + h/2, [c.get("peak_chg", 0)      for c in sc], h, color=UP_COLOR, label=L["plot_peak_pct"])
    ax.set_yticks(y); ax.set_yticklabels(names, fontproperties=FONT, fontsize=10)
    ax.set_xlabel(L["plot_chg_xlabel"], fontproperties=FONT)
    ax.set_title(L["plot_impact_title"].format(etf_name=ETF_NAME), fontproperties=FONT, fontsize=14)
    ax.legend(prop=FONT); ax.grid(True, axis="x"); fig.tight_layout()
    fig.savefig(Path(OUTPUT_DIR) / f"{PREFIX}_impact.png", dpi=150); plt.close(fig)

    # Chart 3: Total market-cap area.
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.fill_between(dates, portfolio["total_market_cap"], color="#3b82f6", alpha=0.3)
    ax.plot(dates, portfolio["total_market_cap"], "#3b82f6", lw=1.5)
    if (portfolio["date"] == event_dt).any():
        ax.axvline(event_dt, color="#ef4444", ls="--", lw=1, label=L["plot_event_date"])
    ax.set_title(L["plot_mcap_title"].format(etf_name=ETF_NAME), fontproperties=FONT, fontsize=14)
    ax.set_ylabel(L["plot_mcap_ylabel"], fontproperties=FONT)
    ax.legend(prop=FONT); ax.grid(True); fig.tight_layout()
    fig.savefig(Path(OUTPUT_DIR) / f"{PREFIX}_mcap.png", dpi=150); plt.close(fig)

    print("  Charts saved: nav / impact / mcap .png")

# ========== Step 5: Report generation ==========

def generate_report():
    """Generate report.md with language aligned to query/dashboard."""
    L = text()
    s = json.loads((Path(OUTPUT_DIR) / f"{PREFIX}_summary.json").read_text("utf-8"))
    meta, stats = s["meta"], s["summary"]
    actual_stocks = meta.get("num_stocks", len(CONSTITUENTS))
    stock_count = f"{actual_stocks}{L['stocks_unit']}" if L["stocks_unit"] else str(actual_stocks)
    pre_mcap = stats.get("pre_event_mcap", "-")
    pre_mcap_display = f"{pre_mcap} {L['mcap_unit']}".strip()
    start = meta.get("start", DATA_START)
    end = meta.get("end", DATA_END)
    missing_policy = meta.get("missing_price_policy", "ffill_before_pct_change")

    md = f"""# {L['report_title'].format(etf_name=ETF_NAME)}

## {L['overview']}
- **{L['event']}**: {EVENT_NAME} | **{L['date']}**: {EVENT_DATE} | **{L['pre_event_date']}**: {PRE_EVENT_DATE}
- **{L['window']}**: {start} ~ {end} | **{L['constituents']}**: {stock_count}
- **{L['event_date_source']}**: {EVENT_DATE_SOURCE}
- **{L['price_adjustment']}**: {PRICE_ADJUSTMENT} | **{L['generated_at']}**: {meta.get('generated_at', GENERATED_AT)}
- **{L['missing_price_policy']}**: {missing_policy}

## {L['key_metrics']}
| {L['metric']} | {L['value']} |
|---|---|
| {L['pre_event_mcap']} | {pre_mcap_display} |
| {L['peak_mcap_chg']} | {stats.get('mcap_change_to_peak_pct', '-')}% |
| {L['etf_total_return']} | {stats.get('etf_return_total_pct', '-')}% |
| {L['equal_total_return']} | {stats.get('equal_weighted_return_total_pct', '-')}% |
| {L['top_weight']} | {stats.get('top_weight_pct', '-')}% |
| HHI | {stats.get('hhi', '-')} |

## {L['assumptions']}
- {L['event_date_source']}: {EVENT_DATE_SOURCE}
- {L['reference_date_reason']}
- {L['constituent_selection'].format(snapshot=CONSTITUENT_SNAPSHOT)}
- {L['weighting']}
- {L['shares_basis']}
- {L['price_adjustment_bullet'].format(price_adjustment=PRICE_ADJUSTMENT)}
- {L['missing_price_bullet'].format(missing_policy=missing_policy)}
- {L['analysis_window'].format(start=start, end=end)}

## {L['known_biases']}
- {L['survivorship_bias']}
- {L['coverage_bias'].format(target=len(CONSTITUENTS), actual=actual_stocks)}
- {L['mcap_basis_bias']}
- {L['event_timing_bias']}

## {L['outputs']}
`{PREFIX}_prices.csv` / `{PREFIX}_portfolio.csv` / `{PREFIX}_summary.json` / `{PREFIX}_run_manifest.json` / `{PREFIX}_dashboard.html` / `{PREFIX}_nav.png` / `{PREFIX}_impact.png` / `{PREFIX}_mcap.png`
"""
    rp = Path(OUTPUT_DIR) / "report.md"
    rp.write_text(md, encoding="utf-8")
    print(f"  Report: {rp}")

def validate_outputs():
    """Pre-delivery reproducibility validation: schema, weights, NAV base date, manifest hash."""
    result = validate_event_outputs(PREFIX, OUTPUT_DIR)
    for warning in result["warnings"]:
        print(f"  WARNING: {warning}")
    if result["errors"]:
        raise RuntimeError("Output validation failed:\n" + "\n".join(result["errors"]))
    print("  Output validation passed")

# ========== Main workflow ==========

def main():
    tickers = [c["ticker"] for c in CONSTITUENTS]
    print(f"=== {ETF_NAME} event study ({len(tickers)} stocks) ===\n")

    print("[1/5] Fetching prices ...")
    prices_df = fetch_prices(tickers, DATA_START, DATA_END)
    print(f"  {len(prices_df)} rows\n")

    print("[2/5] Fetching total shares ...")
    shares_map = fetch_total_shares(tickers)
    missing = set(tickers) - set(shares_map.keys())
    if missing: print(f"  WARNING missing: {missing}")
    assert len(shares_map) == len(tickers), f"Insufficient coverage: {len(shares_map)}/{len(tickers)}"

    print("[3/5] Building ETF ...")
    paths = build_etf(prices_df, shares_map)
    for p in paths.values(): assert p.exists() and p.stat().st_size > 0, f"File issue: {p}"

    print("[4/5] Generating dashboard ...")
    build_dashboard()

    print("[5/5] Charts + report ...")
    plot_charts()
    generate_report()
    validate_outputs()
    print(f"\n=== Done - outputs: {Path(OUTPUT_DIR).resolve()} ===")

if __name__ == "__main__":
    main()
