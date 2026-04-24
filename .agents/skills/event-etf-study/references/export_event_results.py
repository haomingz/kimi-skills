"""
export_event_results.py - Standard export module for event-study ETF analysis.

Produces three standardized output files plus one reproducibility manifest:
  1. <prefix>_prices.csv   - Daily per-stock data (close, market cap, tier)
  2. <prefix>_portfolio.csv - ETF index time series (NAV + total market cap)
  3. <prefix>_summary.json  - Full summary with meta, aggregate stats, per-stock stats
  4. <prefix>_run_manifest.json - Inputs, parameters, environment, output hashes

Usage:
    from export_event_results import export_event_results

    paths = export_event_results(
        constituents=[
            {"ticker": "688041.SH", "name": "Hygon Information", "tier": 2,
             "reason": "GPU/AI chips", "weight": None},
            ...
        ],
        prices_df=prices_df,          # DataFrame with columns: date, ticker, close
        shares_map={"688041.SH": 2.3e9, ...},
        event_date="2026-03-09",
        pre_event_date="2026-03-06",
        prefix="openclaw_etf",
        output_dir="./output",
        etf_name="OpenClaw Lobster Concept ETF",
        event_name="OpenClaw Concept Stock Breakout",
        generated_at="2026-03-15T18:00:00+08:00",
        price_adjustment="forward",
        language="en",
        query="OpenClaw concept stock event study",
        run_metadata={"event_date_source": "user-specified/announcement URL"},
    )
    # paths == {"prices": Path(...), "portfolio": Path(...),
    #           "summary": Path(...), "manifest": Path(...)}

Dependencies: pandas, numpy, json, pathlib, datetime (stdlib + common scientific).
No dependency on backtrader or any backtesting framework.
"""

from __future__ import annotations

import hashlib
import json
import platform
import re
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _yi_yuan(value: float) -> float:
    """Convert raw CNY value to CNY 100M units (1e8), rounded to 2 decimals."""
    return round(value / 1e8, 2)


def _pct(a: float, b: float) -> float:
    """Percentage change from *b* (base) to *a*, rounded to 2 decimals.

    Returns (a / b - 1) * 100.  Returns 0.0 if *b* is zero or NaN.
    """
    if b == 0 or np.isnan(b):
        return 0.0
    return round((a / b - 1) * 100, 2)


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


_CJK_RE = re.compile(r"[\u3400-\u9fff]")
_LATIN_RE = re.compile(r"[A-Za-z]")
_AUTO_LANGUAGE_VALUES = {"", "auto"}


def _resolve_language(language: str | None, *texts: object) -> str:
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
    return "en"


def _is_auto_language(language: str | None) -> bool:
    return (language or "auto").strip().lower().replace("_", "-") in _AUTO_LANGUAGE_VALUES


def _stable_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, default=str, separators=(",", ":")
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Core export function
# ---------------------------------------------------------------------------

def export_event_results(
    constituents: list[dict],
    prices_df: pd.DataFrame,
    shares_map: dict[str, float],
    event_date: str,
    pre_event_date: str,
    prefix: str,
    output_dir: str | Path | None = None,
    etf_name: str = "",
    event_name: str = "",
    market: str = "china_a",
    generated_at: str | None = None,
    price_adjustment: str = "forward",
    data_source: str = "mshtools/ifind",
    language: str = "auto",
    query: str = "",
    run_metadata: dict | None = None,
    write_manifest: bool = True,
) -> dict[str, Path]:
    """Export event-study ETF analysis results to standard files and manifest.

    Parameters
    ----------
    constituents : list[dict]
        Each dict must contain keys ``ticker``, ``name``, ``tier``, ``reason``,
        ``weight``.  If ``weight`` is ``None`` for **any** entry the weights
        are auto-computed from pre-event-date market capitalizations.
    prices_df : pd.DataFrame
        Columns: ``date`` (str or datetime), ``ticker`` (str), ``close`` (float).
        Must cover at least *pre_event_date* for every ticker.
    shares_map : dict[str, float]
        Mapping from ticker to total outstanding shares (absolute count).
    event_date : str
        Event explosion date in ``YYYY-MM-DD`` format.
    pre_event_date : str
        Reference date used for weight calculation (``YYYY-MM-DD``).
    prefix : str
        Filename prefix, e.g. ``"openclaw_etf"``.
    output_dir : str | Path | None
        Directory for output files.  Defaults to the current working directory.
    etf_name : str
        Human-readable ETF name for the summary.
    event_name : str
        Human-readable event description for the summary.
    market : str
        Market code for color scheme: ``"china_a"`` (default, red up and green
        down) or ``"us"`` (green up and red down). Written to ``summary.json``
        meta for dashboard rendering.
    generated_at : str | None
        Stable ISO timestamp for reproducible reruns. If omitted, the current
        local time is used and recorded in both ``summary.json`` and the
        manifest.
    price_adjustment : str
        Price adjustment convention, e.g. ``"forward"`` for forward-adjusted
        prices if that is the ifind tool's configured value. Recorded for
        auditability.
    data_source : str
        Data provider/toolchain label recorded in the manifest.
    language : str
        Output language: ``"zh"`` or ``"en"``. ``"auto"`` is accepted only
        when ``query`` is provided, and is resolved from the original query.
    query : str
        Original user query/request, used for language auto-detection and
        provenance when available.
    run_metadata : dict | None
        Extra caller-supplied provenance such as event source URLs, raw snapshot
        paths, exact MCP arguments, or research notes.
    write_manifest : bool
        Write ``<prefix>_run_manifest.json`` when true.

    Returns
    -------
    dict[str, Path]
        ``{"prices": Path, "portfolio": Path, "summary": Path, "manifest": Path}``
        when ``write_manifest`` is true.
    """

    # --- Setup ----------------------------------------------------------------
    out = Path(output_dir) if output_dir else Path.cwd()
    out.mkdir(parents=True, exist_ok=True)
    generated_at_value = generated_at or _now_iso()
    if market not in {"china_a", "us"}:
        raise ValueError(f"market must be 'china_a' or 'us', got {market!r}")
    if _is_auto_language(language) and not str(query or "").strip():
        raise ValueError(
            "language='auto' requires the original query for language detection; "
            "pass language='zh' or language='en' explicitly."
        )
    resolved_language = _resolve_language(language, query)

    # Build look-up tables from constituents list.
    ticker_meta: dict[str, dict] = {}
    raw_tickers = [c["ticker"] for c in constituents]
    duplicated = sorted({t for t in raw_tickers if raw_tickers.count(t) > 1})
    if duplicated:
        raise ValueError(f"Duplicate constituent tickers: {duplicated}")
    for c in constituents:
        ticker_meta[c["ticker"]] = {
            "name": c["name"],
            "tier": c["tier"],
            "reason": c["reason"],
            "weight": c.get("weight"),  # may be None
        }

    tickers = raw_tickers

    # --- Prepare prices -------------------------------------------------------
    df = prices_df.copy()
    required_price_cols = {"date", "ticker", "close"}
    missing_cols = required_price_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"prices_df missing required columns: {sorted(missing_cols)}")
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    # Keep only constituent tickers
    df = df[df["ticker"].isin(tickers)].copy()
    df = df.sort_values(["date", "ticker"]).reset_index(drop=True)
    if df.empty:
        raise ValueError("prices_df has no rows for the requested constituents.")

    missing_price_tickers = sorted(set(tickers) - set(df["ticker"].unique()))
    if missing_price_tickers:
        raise ValueError(f"Missing price data for tickers: {missing_price_tickers}")

    missing_shares = sorted(
        t for t in tickers
        if t not in shares_map or pd.isna(shares_map[t]) or float(shares_map[t]) <= 0
    )
    if missing_shares:
        raise ValueError(f"Missing or non-positive total shares for tickers: {missing_shares}")

    all_dates = sorted(df["date"].unique())
    start_date = all_dates[0]
    end_date = all_dates[-1]

    # --- Market cap -----------------------------------------------------------
    # Raw market cap in CNY
    df["total_shares"] = df["ticker"].map(shares_map)
    df["market_cap_raw"] = df["close"] * df["total_shares"]
    # Market cap in CNY 100M units.
    df["market_cap"] = (df["market_cap_raw"] / 1e8).round(2)

    # --- Pivot tables ---------------------------------------------------------
    close_pivot = df.pivot_table(
        index="date", columns="ticker", values="close", aggfunc="last",
    ).reindex(columns=tickers)

    mcap_pivot = df.pivot_table(
        index="date", columns="ticker", values="market_cap_raw", aggfunc="last",
    ).reindex(columns=tickers)

    if pre_event_date not in close_pivot.index:
        raise ValueError(
            f"pre_event_date {pre_event_date!r} not found in price data. "
            f"Available dates: {all_dates[:5]}...{all_dates[-5:]}"
        )

    # --- Weights --------------------------------------------------------------
    auto_compute_weights = any(
        ticker_meta[t]["weight"] is None for t in tickers
    )

    if auto_compute_weights:
        # Derive weights from pre_event_date market caps.
        pre_mcaps = mcap_pivot.loc[pre_event_date]
        total_pre = pre_mcaps.sum()
        if pd.isna(total_pre) or total_pre <= 0:
            raise ValueError(f"Total market cap on {pre_event_date} must be positive.")
        weights = (pre_mcaps / total_pre).fillna(0.0)
    else:
        # Use explicitly provided weights (normalised to sum to 1).
        raw_w = pd.Series(
            {t: float(ticker_meta[t]["weight"]) for t in tickers},
            index=tickers,
        )
        if raw_w.sum() <= 0:
            raise ValueError("Explicit constituent weights must sum to a positive value.")
        weights = raw_w / raw_w.sum()

    weight_pct = (weights * 100).round(2)  # for display (% summing to ~100)

    # Store computed weight back into ticker_meta for output.
    for t in tickers:
        ticker_meta[t]["weight"] = float(weight_pct[t])

    # --- Equal weights --------------------------------------------------------
    n_stocks = len(tickers)
    equal_weights = pd.Series(1.0 / n_stocks, index=tickers)

    # --- Daily returns --------------------------------------------------------
    # Make suspended/missing-price handling explicit. Pandas' pct_change
    # default fill behavior has changed across versions, so we ffill first and
    # then disable any implicit fill inside pct_change.
    close_for_returns = close_pivot.ffill()
    daily_returns = close_for_returns.pct_change(fill_method=None)  # first row is NaN

    # --- NAV computation (starts at 100 on pre_event_date) --------------------
    # Portfolio return on each day = weighted sum of individual returns.
    mcap_port_ret = daily_returns.multiply(weights, axis=1).sum(axis=1)
    eq_port_ret = daily_returns.multiply(equal_weights, axis=1).sum(axis=1)

    # Cumulative NAV: pre_event_date = 100, all dates relative to it.
    # This ensures the chart is anchored to the event reference date,
    # regardless of how much pre-event data was fetched.
    mcap_nav = pd.Series(np.nan, index=close_pivot.index, name="mcap_weighted_nav")
    eq_nav = pd.Series(np.nan, index=close_pivot.index, name="equal_weighted_nav")

    dates_list = list(close_pivot.index)
    pre_idx = dates_list.index(pre_event_date) if pre_event_date in dates_list else 0

    mcap_nav.iloc[pre_idx] = 100.0
    eq_nav.iloc[pre_idx] = 100.0

    # Forward fill from pre_event_date
    for i in range(pre_idx + 1, len(dates_list)):
        mcap_nav.iloc[i] = mcap_nav.iloc[i - 1] * (1 + mcap_port_ret.iloc[i])
        eq_nav.iloc[i] = eq_nav.iloc[i - 1] * (1 + eq_port_ret.iloc[i])

    # Back fill before pre_event_date (if any earlier data exists)
    for i in range(pre_idx - 1, -1, -1):
        mcap_nav.iloc[i] = mcap_nav.iloc[i + 1] / (1 + mcap_port_ret.iloc[i + 1])
        eq_nav.iloc[i] = eq_nav.iloc[i + 1] / (1 + eq_port_ret.iloc[i + 1])

    mcap_nav = mcap_nav.round(4)
    eq_nav = eq_nav.round(4)

    # --- Total market cap (CNY 100M units) per day ----------------------------
    total_mcap_daily = (mcap_pivot.sum(axis=1) / 1e8).round(2)

    # =========================================================================
    # FILE 1: <prefix>_prices.csv
    # =========================================================================
    prices_out = df[["date", "ticker", "close", "market_cap"]].copy()
    prices_out["name"] = prices_out["ticker"].map(
        {t: m["name"] for t, m in ticker_meta.items()}
    )
    prices_out["tier"] = prices_out["ticker"].map(
        {t: m["tier"] for t, m in ticker_meta.items()}
    )
    prices_out = prices_out[["date", "ticker", "name", "close", "market_cap", "tier"]]
    prices_out = prices_out.sort_values(["date", "ticker"]).reset_index(drop=True)

    prices_path = out / f"{prefix}_prices.csv"
    prices_out.to_csv(prices_path, index=False)

    # =========================================================================
    # FILE 2: <prefix>_portfolio.csv
    # =========================================================================
    portfolio_df = pd.DataFrame({
        "date": dates_list,
        "mcap_weighted_nav": mcap_nav.values,
        "equal_weighted_nav": eq_nav.values,
        "total_market_cap": total_mcap_daily.values,
    })

    portfolio_path = out / f"{prefix}_portfolio.csv"
    portfolio_df.to_csv(portfolio_path, index=False)

    # =========================================================================
    # FILE 3: <prefix>_summary.json
    # =========================================================================

    # --- Aggregate statistics ------------------------------------------------
    pre_event_total_mcap = _yi_yuan(mcap_pivot.loc[pre_event_date].sum()) \
        if pre_event_date in mcap_pivot.index else 0.0

    peak_total_mcap = _yi_yuan(mcap_pivot.sum(axis=1).max())
    latest_total_mcap = _yi_yuan(mcap_pivot.sum(axis=1).iloc[-1])

    mcap_change_to_peak = _pct(
        mcap_pivot.sum(axis=1).max(),
        mcap_pivot.loc[pre_event_date].sum() if pre_event_date in mcap_pivot.index else 1.0,
    )
    mcap_change_to_latest = _pct(
        mcap_pivot.sum(axis=1).iloc[-1],
        mcap_pivot.loc[pre_event_date].sum() if pre_event_date in mcap_pivot.index else 1.0,
    )

    etf_return_total = round(float(mcap_nav.iloc[-1] / 100 - 1) * 100, 2)

    # ETF return on event day specifically
    if event_date in mcap_nav.index:
        evt_idx = list(mcap_nav.index).index(event_date)
        if evt_idx > 0:
            etf_return_event_day = round(
                float(mcap_nav.iloc[evt_idx] / mcap_nav.iloc[evt_idx - 1] - 1) * 100, 2,
            )
        else:
            etf_return_event_day = 0.0
    else:
        etf_return_event_day = 0.0

    eq_return_total = round(float(eq_nav.iloc[-1] / 100 - 1) * 100, 2)
    hhi = round(float((weights ** 2).sum()), 6)
    top_weight_ticker = weight_pct.idxmax()
    top_weight_pct = float(weight_pct[top_weight_ticker])

    # --- Per-stock statistics -------------------------------------------------
    pre_close = close_pivot.loc[pre_event_date] if pre_event_date in close_pivot.index else None

    constituents_out: list[dict] = []
    for t in tickers:
        meta = ticker_meta[t]

        if pre_close is not None and not np.isnan(pre_close[t]):
            base = pre_close[t]

            # Event-day change
            if event_date in close_pivot.index:
                event_day_chg = _pct(close_pivot.loc[event_date, t], base)
            else:
                event_day_chg = 0.0

            # Peak change (max close from event_date onward vs pre_event close)
            post_event = close_pivot.loc[event_date:, t] \
                if event_date in close_pivot.index else close_pivot[t]
            peak_close = post_event.max()
            peak_chg = _pct(peak_close, base)

            # Latest change
            latest_close = close_pivot[t].iloc[-1]
            latest_chg = _pct(latest_close, base)
        else:
            event_day_chg = 0.0
            peak_chg = 0.0
            latest_chg = 0.0

        # Market cap in CNY 100M units on pre_event_date (or latest if unavailable).
        if pre_event_date in mcap_pivot.index:
            stock_mcap = _yi_yuan(mcap_pivot.loc[pre_event_date, t])
        else:
            stock_mcap = _yi_yuan(mcap_pivot[t].iloc[-1])

        constituents_out.append({
            "ticker": t,
            "name": meta["name"],
            "tier": meta["tier"],
            "reason": meta["reason"],
            "weight": meta["weight"],
            "event_day_chg": event_day_chg,
            "peak_chg": peak_chg,
            "latest_chg": latest_chg,
            "market_cap_billion": stock_mcap,
        })

    summary = {
        "meta": {
            "etf_name": etf_name,
            "event_name": event_name,
            "event_date": event_date,
            "pre_event_date": pre_event_date,
            "num_stocks": n_stocks,
            "start": start_date,
            "end": end_date,
            "market": market,
            "generated_at": generated_at_value,
            "price_adjustment": price_adjustment,
            "data_source": data_source,
            "missing_price_policy": "ffill_before_pct_change",
            "language": resolved_language,
            **({"query": query} if query else {}),
        },
        "summary": {
            "pre_event_mcap": pre_event_total_mcap,
            "peak_mcap": peak_total_mcap,
            "latest_mcap": latest_total_mcap,
            "mcap_change_to_peak_pct": mcap_change_to_peak,
            "mcap_change_to_latest_pct": mcap_change_to_latest,
            "etf_return_total_pct": etf_return_total,
            "etf_return_event_day_pct": etf_return_event_day,
            "equal_weighted_return_total_pct": eq_return_total,
            "hhi": hhi,
            "top_weight_ticker": top_weight_ticker,
            "top_weight_name": ticker_meta[top_weight_ticker]["name"],
            "top_weight_pct": top_weight_pct,
            "single_stock_weight_gt_30pct": top_weight_pct > 30.0,
        },
        "constituents": constituents_out,
    }

    summary_path = out / f"{prefix}_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8",
    )

    paths = {
        "prices": prices_path,
        "portfolio": portfolio_path,
        "summary": summary_path,
    }

    if write_manifest:
        manifest_path = out / f"{prefix}_run_manifest.json"
        prices_digest_df = df[["date", "ticker", "close", "market_cap"]].copy()
        manifest = {
            "schema_version": "event-study-etf-run-manifest-v1",
            "generated_at": generated_at_value,
            "prefix": prefix,
            "inputs": {
                "etf_name": etf_name,
                "event_name": event_name,
                "event_date": event_date,
                "pre_event_date": pre_event_date,
                "data_start": start_date,
                "data_end": end_date,
                "market": market,
                "language": resolved_language,
                **({"query": query} if query else {}),
                "price_adjustment": price_adjustment,
                "data_source": data_source,
                "missing_price_policy": "ffill_before_pct_change",
                "num_constituents": n_stocks,
                "constituents": [
                    {
                        "ticker": t,
                        "name": ticker_meta[t]["name"],
                        "tier": ticker_meta[t]["tier"],
                        "reason": ticker_meta[t]["reason"],
                        "weight_pct": ticker_meta[t]["weight"],
                    }
                    for t in tickers
                ],
                "constituents_hash": _sha256_bytes(_stable_json_bytes([
                    {k: c.get(k) for k in ("ticker", "name", "tier", "reason", "weight")}
                    for c in constituents
                ])),
                "shares_map_hash": _sha256_bytes(_stable_json_bytes({
                    t: float(shares_map[t]) for t in tickers
                })),
                "prices_input_hash": _sha256_bytes(
                    prices_digest_df.to_csv(index=False).encode("utf-8")
                ),
            },
            "parameters": {
                "weighting": "market_cap",
                "auto_compute_weights": auto_compute_weights,
                "weight_basis": (
                    "pre_event_date_market_cap" if auto_compute_weights
                    else "explicit_constituent_weights"
                ),
                "nav_base_date": pre_event_date,
                "nav_base_value": 100.0,
                "equal_weight_also_computed": True,
            },
            "environment": {
                "python": sys.version.split()[0],
                "platform": platform.platform(),
                "pandas": pd.__version__,
                "numpy": np.__version__,
            },
            "outputs": {
                key: {
                    "path": path.name,
                    "sha256": _sha256_file(path),
                }
                for key, path in paths.items()
            },
            "run_metadata": run_metadata or {},
        }
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        paths["manifest"] = manifest_path

    return paths
