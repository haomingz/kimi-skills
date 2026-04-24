#!/usr/bin/env python3
"""Validate event-study ETF outputs for reproducibility.

Checks the three analysis files plus ``<prefix>_run_manifest.json`` created by
``export_event_results.py``. The checks are intentionally structural and
deterministic so they can run before every handoff.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


REQUIRED_PRICE_COLUMNS = {"date", "ticker", "name", "close", "market_cap", "tier"}
REQUIRED_PORTFOLIO_COLUMNS = {
    "date",
    "mcap_weighted_nav",
    "equal_weighted_nav",
    "total_market_cap",
}
REQUIRED_SUMMARY_META = {
    "event_date",
    "pre_event_date",
    "start",
    "end",
    "market",
    "generated_at",
    "price_adjustment",
    "data_source",
    "missing_price_policy",
    "language",
}
REQUIRED_SUMMARY_STATS = {
    "etf_return_total_pct",
    "equal_weighted_return_total_pct",
    "hhi",
    "top_weight_pct",
}
_CJK_RE = re.compile(r"[\u3400-\u9fff]")
_LATIN_RE = re.compile(r"[A-Za-z]")
_DASHBOARD_DATA_RE = re.compile(
    r'<script[^>]+id=["\']report-data["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_MARKDOWN_CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
_MARKDOWN_INLINE_CODE_RE = re.compile(r"`[^`]*`")
_MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_URL_RE = re.compile(r"https?://\S+")
_DATE_TIME_RE = re.compile(r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}(?:[T\s]\d{1,2}:\d{2}(?::\d{2})?(?:[+-]\d{2}:\d{2})?)?\b")
_FILE_NAME_RE = re.compile(r"\b[\w.-]+\.(?:csv|json|html|png|md|py|txt|xlsx|pdf)\b", re.IGNORECASE)
_ALLOWED_ZH_LATIN_TERMS = {
    "A",
    "API",
    "AI",
    "AIGC",
    "B",
    "CPU",
    "CSV",
    "CNY",
    "ETF",
    "GPU",
    "HHI",
    "HTML",
    "JSON",
    "MCP",
    "NAV",
    "PNG",
    "RMB",
    "T1",
    "T2",
    "T3",
    "USD",
    "ifind",
    "mshtools",
}
_ALLOWED_ZH_LATIN_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:"
    + "|".join(re.escape(term) for term in sorted(_ALLOWED_ZH_LATIN_TERMS, key=len, reverse=True))
    + r")(?![A-Za-z0-9])",
    re.IGNORECASE,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def safe_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result


def infer_language(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    if _CJK_RE.search(text):
        return "zh"
    if _LATIN_RE.search(text):
        return "en"
    return None


def language_mismatch(value: Any, expected_language: str) -> bool:
    text = normalize_visible_text(value)
    if not text:
        return False
    if expected_language == "zh":
        residue = strip_allowed_zh_latin(text)
        return bool(_LATIN_RE.search(residue))
    if expected_language == "en":
        return bool(_CJK_RE.search(text))
    return False


def normalize_visible_text(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    text = _MARKDOWN_CODE_BLOCK_RE.sub(" ", text)
    text = _MARKDOWN_INLINE_CODE_RE.sub(" ", text)
    text = _MARKDOWN_LINK_RE.sub(r"\1", text)
    text = _HTML_TAG_RE.sub(" ", text)
    text = _URL_RE.sub(" ", text)
    text = _DATE_TIME_RE.sub(" ", text)
    text = _FILE_NAME_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def strip_allowed_zh_latin(text: str) -> str:
    text = _ALLOWED_ZH_LATIN_RE.sub(" ", text)
    text = re.sub(r"\b\d+(?:\.\d+)?%?\b", " ", text)
    text = re.sub(r"[%+\-~|:：/().,，。;；、\[\]{}#*_]+", " ", text)
    return text


def add_language_errors(
    errors: list[str],
    expected_language: str,
    fields: list[tuple[str, Any]],
    max_errors: int = 20,
) -> None:
    emitted = 0
    omitted = 0
    for field_name, value in fields:
        if not language_mismatch(value, expected_language):
            continue
        if emitted < max_errors:
            errors.append(
                f"{field_name} appears inconsistent with language={expected_language!r}: {value!r}"
            )
            emitted += 1
        else:
            omitted += 1
    if omitted:
        errors.append(f"{omitted} additional language consistency errors omitted")


def report_visible_fields(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    text = _MARKDOWN_CODE_BLOCK_RE.sub("\n", text)
    fields: list[tuple[str, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        visible = normalize_visible_text(line)
        if not visible or set(visible) <= {"-", "|", " "}:
            continue
        fields.append((f"report.md:{lineno}", visible))
    return fields


def dashboard_payload(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    match = _DASHBOARD_DATA_RE.search(text)
    if not match:
        errors.append(f"dashboard report-data payload missing: {path}")
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        errors.append(f"dashboard report-data payload is invalid JSON: {exc}")
        return None


def dashboard_visible_fields(payload: dict[str, Any]) -> list[tuple[str, Any]]:
    fields: list[tuple[str, Any]] = []
    meta = payload.get("meta", {})
    for key in ("strategy_name", "symbol", "event_name", "etf_name"):
        fields.append((f"dashboard.meta.{key}", meta.get(key)))

    ui = payload.get("ui", {})
    fields.append(("dashboard.ui.subtitle", ui.get("subtitle")))
    fields.append(("dashboard.ui.window_status", ui.get("window_status")))
    for idx, tab in enumerate(ui.get("tabs", []) or []):
        fields.append((f"dashboard.ui.tabs[{idx}].label", tab.get("label")))
    for idx, item in enumerate(ui.get("topbar_menu", []) or []):
        fields.append((f"dashboard.ui.topbar_menu[{idx}].label", item.get("label")))
    for key, value in (ui.get("i18n", {}) or {}).items():
        if key in {"html_lang"}:
            continue
        fields.append((f"dashboard.ui.i18n.{key}", value))

    for idx, module in enumerate(payload.get("modules", []) or []):
        prefix = f"dashboard.modules[{idx}]"
        fields.append((f"{prefix}.title", module.get("title")))
        fields.append((f"{prefix}.subtitle", module.get("subtitle")))
        for item_idx, item in enumerate(module.get("items", []) or []):
            fields.append((f"{prefix}.items[{item_idx}].label", item.get("label")))
            fields.append((f"{prefix}.items[{item_idx}].subvalue", item.get("subvalue")))
        for stat_idx, stat in enumerate(module.get("stats", []) or []):
            fields.append((f"{prefix}.stats[{stat_idx}].label", stat.get("label")))
            fields.append((f"{prefix}.stats[{stat_idx}].subvalue", stat.get("subvalue")))
        for toggle_idx, toggle in enumerate(module.get("toggles", []) or []):
            fields.append((f"{prefix}.toggles[{toggle_idx}].label", toggle.get("label")))
        for mode_idx, mode in enumerate(module.get("modes", []) or []):
            fields.append((f"{prefix}.modes[{mode_idx}].label", mode.get("label")))
        for col_idx, column in enumerate(module.get("columns", []) or []):
            fields.append((f"{prefix}.columns[{col_idx}]", column))
        for row_idx, row in enumerate(module.get("rows", []) or []):
            fields.append((f"{prefix}.rows[{row_idx}].symbol", row.get("symbol")))
            fields.append((f"{prefix}.rows[{row_idx}].side", row.get("side")))
            fields.append((f"{prefix}.rows[{row_idx}].exit_price", row.get("exit_price")))
            fields.append((f"{prefix}.rows[{row_idx}].metric", row.get("metric")))
            for value_idx, value in enumerate(row.get("values", []) or []):
                if isinstance(value, dict):
                    fields.append((f"{prefix}.rows[{row_idx}].values[{value_idx}].main", value.get("main")))
                    fields.append((f"{prefix}.rows[{row_idx}].values[{value_idx}].secondary", value.get("secondary")))
        if module.get("html"):
            fields.append((f"{prefix}.html", normalize_visible_text(module.get("html"))))
    return fields


def parse_date(value: str, field_name: str, errors: list[str]) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except (TypeError, ValueError):
        errors.append(f"{field_name} must be YYYY-MM-DD, got {value!r}")


def validate_event_outputs(prefix: str, data_dir: str | Path = ".") -> dict[str, list[str]]:
    """Return ``{"errors": [...], "warnings": [...]}`` for output files."""
    base = Path(data_dir)
    paths = {
        "prices": base / f"{prefix}_prices.csv",
        "portfolio": base / f"{prefix}_portfolio.csv",
        "summary": base / f"{prefix}_summary.json",
        "manifest": base / f"{prefix}_run_manifest.json",
        "dashboard": base / f"{prefix}_dashboard.html",
        "report": base / "report.md",
    }
    errors: list[str] = []
    warnings: list[str] = []

    for key in ("prices", "portfolio", "summary", "manifest"):
        path = paths[key]
        if not path.exists():
            errors.append(f"missing {key} file: {path}")
        elif path.stat().st_size == 0:
            errors.append(f"empty {key} file: {path}")
    if errors:
        return {"errors": errors, "warnings": warnings}

    prices = read_csv_rows(paths["prices"])
    portfolio = read_csv_rows(paths["portfolio"])
    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))

    price_cols = set(prices[0].keys()) if prices else set()
    portfolio_cols = set(portfolio[0].keys()) if portfolio else set()
    if not prices:
        errors.append("prices file has no data rows")
    if not portfolio:
        errors.append("portfolio file has no data rows")
    missing_price_cols = REQUIRED_PRICE_COLUMNS - price_cols
    missing_portfolio_cols = REQUIRED_PORTFOLIO_COLUMNS - portfolio_cols
    if missing_price_cols:
        errors.append(f"prices file missing columns: {sorted(missing_price_cols)}")
    if missing_portfolio_cols:
        errors.append(f"portfolio file missing columns: {sorted(missing_portfolio_cols)}")

    meta = summary.get("meta", {})
    stats = summary.get("summary", {})
    constituents = summary.get("constituents", [])
    missing_meta = REQUIRED_SUMMARY_META - set(meta.keys())
    missing_stats = REQUIRED_SUMMARY_STATS - set(stats.keys())
    if missing_meta:
        errors.append(f"summary.meta missing keys: {sorted(missing_meta)}")
    if missing_stats:
        errors.append(f"summary.summary missing keys: {sorted(missing_stats)}")
    if not constituents:
        errors.append("summary.constituents is empty")

    event_date = meta.get("event_date")
    pre_event_date = meta.get("pre_event_date")
    if event_date:
        parse_date(event_date, "meta.event_date", errors)
    if pre_event_date:
        parse_date(pre_event_date, "meta.pre_event_date", errors)

    portfolio_dates = [row.get("date", "") for row in portfolio]
    price_dates = [row.get("date", "") for row in prices]
    if pre_event_date and pre_event_date not in portfolio_dates:
        errors.append(f"pre_event_date {pre_event_date} is absent from portfolio dates")
    if pre_event_date and pre_event_date not in price_dates:
        errors.append(f"pre_event_date {pre_event_date} is absent from price dates")
    if event_date and event_date not in portfolio_dates:
        warnings.append(
            f"event_date {event_date} is not a trading row; document the next-trading-day policy"
        )

    if pre_event_date and pre_event_date in portfolio_dates:
        pre_row = next(row for row in portfolio if row.get("date") == pre_event_date)
        mcap_nav = safe_float(pre_row.get("mcap_weighted_nav"))
        equal_nav = safe_float(pre_row.get("equal_weighted_nav"))
        if mcap_nav is None or abs(mcap_nav - 100.0) > 1e-6:
            errors.append("mcap_weighted_nav must be 100.0 on pre_event_date")
        if equal_nav is None or abs(equal_nav - 100.0) > 1e-6:
            errors.append("equal_weighted_nav must be 100.0 on pre_event_date")

    weights = [safe_float(c.get("weight")) for c in constituents]
    if any(w is None for w in weights):
        errors.append("all constituents must have numeric weight")
    else:
        weight_sum = sum(w for w in weights if w is not None)
        max_weight = max(weights) if weights else 0.0
        if abs(weight_sum - 100.0) > 0.10:
            errors.append(f"constituent weights must sum to 100%, got {weight_sum:.4f}%")
        if max_weight > 30.0:
            warnings.append(f"single-stock weight exceeds 30%: {max_weight:.2f}%")

    if meta.get("generated_at") != manifest.get("generated_at"):
        errors.append("summary.meta.generated_at must match manifest.generated_at")
    if meta.get("language") not in {"zh", "en"}:
        errors.append("summary.meta.language must be 'zh' or 'en'")
    if manifest.get("inputs", {}).get("language") != meta.get("language"):
        errors.append("manifest.inputs.language must match summary.meta.language")
    query_language = infer_language(meta.get("query") or manifest.get("inputs", {}).get("query"))
    if query_language and meta.get("language") in {"zh", "en"} and query_language != meta.get("language"):
        errors.append(
            "summary.meta.language must match the original query language "
            f"({query_language!r})"
        )
    if manifest.get("schema_version") != "event-study-etf-run-manifest-v1":
        errors.append("manifest.schema_version is missing or unsupported")

    if meta.get("language") in {"zh", "en"}:
        language_fields: list[tuple[str, Any]] = [
            ("summary.meta.etf_name", meta.get("etf_name")),
            ("summary.meta.event_name", meta.get("event_name")),
        ]
        for idx, constituent in enumerate(constituents):
            ticker = constituent.get("ticker", f"#{idx + 1}")
            if meta["language"] == "zh":
                language_fields.append(
                    (f"summary.constituents[{ticker}].name", constituent.get("name"))
                )
            language_fields.append(
                (f"summary.constituents[{ticker}].reason", constituent.get("reason"))
            )
        add_language_errors(errors, meta["language"], language_fields)
        add_language_errors(errors, meta["language"], report_visible_fields(paths["report"]))
        dashboard_data = dashboard_payload(paths["dashboard"], errors)
        if dashboard_data is not None:
            dashboard_language = dashboard_data.get("meta", {}).get("language")
            if dashboard_language != meta["language"]:
                errors.append(
                    "dashboard.meta.language must match summary.meta.language: "
                    f"{dashboard_language!r} != {meta['language']!r}"
                )
            add_language_errors(errors, meta["language"], dashboard_visible_fields(dashboard_data))
        else:
            warnings.append(f"dashboard file not language-scanned: {paths['dashboard']}")
        if not paths["report"].exists():
            warnings.append(f"report file not language-scanned: {paths['report']}")

    manifest_outputs = manifest.get("outputs", {})
    for key in ("prices", "portfolio", "summary"):
        expected = manifest_outputs.get(key, {}).get("sha256")
        actual = sha256_file(paths[key])
        if expected != actual:
            errors.append(f"manifest hash mismatch for {key}: expected {expected}, got {actual}")

    if not manifest.get("inputs", {}).get("price_adjustment"):
        errors.append("manifest.inputs.price_adjustment must be recorded")
    if not manifest.get("inputs", {}).get("data_source"):
        errors.append("manifest.inputs.data_source must be recorded")
    if manifest.get("inputs", {}).get("missing_price_policy") != "ffill_before_pct_change":
        errors.append("manifest.inputs.missing_price_policy must be ffill_before_pct_change")
    if not manifest.get("inputs", {}).get("constituents_hash"):
        errors.append("manifest.inputs.constituents_hash must be recorded")
    if not manifest.get("inputs", {}).get("prices_input_hash"):
        errors.append("manifest.inputs.prices_input_hash must be recorded")

    return {"errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate event-study ETF output files")
    parser.add_argument("prefix", help="Output prefix, e.g. openclaw_etf")
    parser.add_argument("--data-dir", default=".", help="Directory containing output files")
    args = parser.parse_args()

    result = validate_event_outputs(args.prefix, args.data_dir)
    for warning in result["warnings"]:
        print(f"WARNING: {warning}")
    for error in result["errors"]:
        print(f"ERROR: {error}", file=sys.stderr)

    if result["errors"]:
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
