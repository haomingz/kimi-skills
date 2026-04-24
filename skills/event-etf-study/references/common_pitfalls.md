# Common Event Study ETF Pitfalls And Notes

> **Mandatory rule**: read this file in full **before** writing code, and self-check against the checklist at the end **before** delivery.

---

## 1. Market-Cap Weight Concentration
Large-cap stocks can take extremely high weights, for example above 50%, causing the ETF to behave almost like that single stock.
-> Calculate HHI, disclose the largest weight, and **always compute an equal-weighted version as well**.

## 2. The Event Date Must Have Evidence
Do not guess. Good: "2025-01-20, source: official release record". Bad: "around mid-January".

## 3. Survivorship Bias
A constituent list chosen after the fact is inherently upward-biased. If this is unavoidable, explain it in the "Known Limitations" section.

## 4. Look-Ahead Bias
The timestamp for constituent-selection information must be <= the event date. Do not use T+30 performance to select the stocks for day T.

## 5. Total Shares Freshness
Share count changes through issuance and buybacks. Use the latest available data and state the value date.

## 6. Suspended Stock Handling
- Check the number of valid trading days for every stock.
- Fixed policy: use `ffill_before_pct_change`, meaning forward-fill first, then compute simple returns, and record the policy in the manifest.
- Consider excluding long-suspended stocks, for example those suspended for more than 50% of trading days.

## 7. Market-Cap Units
ifind may return values in `CNY 10K` units or raw shares. Normalize to **CNY 100M** immediately after loading.

## 8. NAV Base Date
The NAV base must be **`pre_event_date` (the reference date)**, not the earliest data date. This keeps the NAV curve anchored at 100 on the last trading day before the event, regardless of how much pre-event data was fetched.

## 9. Weight Calculation Date
Use market cap from the **trading day before the event** to avoid introducing look-ahead from the event shock.

## 10. Subjective Tiering
State the classification standard and the reason for each stock's tier. Consider sensitivity analysis, such as T1 only vs all constituents.

## 11. Limit Up / Limit Down
China A-shares have 10%/20% daily price limits. Consecutive limit-up moves can understate "true return"; note this in the report.

## 12. Price Adjustment
Use **forward-adjusted** prices. Unadjusted prices are suitable only for same-day snapshots.

## 13. Time Zone
ifind returns UTC+8. Use either tz-naive dates or UTC+8 consistently.

## 14. Dynamic Concept Membership
ifind concept boards may be updated after the fact. If historical snapshots are unavailable, note this in the report.

## 15. Overly Wide Data Windows Distort Visuals
Fetching too much pre-event history, for example 2 months, pushes the event date to the right side of the dashboard/Matplotlib charts and dilutes the buy-and-hold window with irrelevant data.
-> **Set the window exactly to the user request**: "buy after the event and hold for one week" requires only 3-5 days before the event plus 1-2 weeks after it, about 10-15 trading days.
-> The NAV base is always `pre_event_date`, not the earliest data date.

## 16. Equal-Weighted Vs Market-Cap-Weighted
**Always** compute and report both versions. If they differ materially, explain why.

## 17. Matplotlib Unicode Font
```python
from matplotlib.font_manager import FontProperties
FONT = FontProperties(fname="/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
```

## 18. Simple Returns Vs Log Returns
Use **simple returns** with `pct_change()` for event studies. Log returns have the wrong interpretation in a weighted portfolio.

## 19. Weight Normalization
`assert abs(weights.sum() - 1.0) < 1e-6`

## 20. Timestamp Drift
`summary.json` and the HTML dashboard must not refresh `generated_at` automatically on every rerun, or identical inputs will produce meaningless diffs.
-> Pass a fixed `generated_at` explicitly in the analysis code, and reuse it for reproducible reruns.

## 21. Constituent Sources Cannot Be Rechecked Reliably
Dynamic web pages such as Tonghuashun, Xueqiu, and East Money update over time, so simply "searching again" cannot reproduce the original stock universe.
-> Save a `<prefix>_constituents_sources.csv` snapshot and derive the final stock pool from that snapshot.

## 22. Missing Output Hash Reconciliation
Without output hashes, it is hard to confirm whether a reproducible rerun generated the same files.
-> Generate `<prefix>_run_manifest.json` with input hashes, parameters, dependency versions, and output hashes.

## 23. Language Mismatch Across Output Artifacts
When the user writes in Chinese but the outputs (HTML dashboard, PNG chart labels, `report.md`, constituent labels/reasons) contain English text, or vice versa.
-> Resolve `language` from the **original query text** using CJK detection (`\u3400-\u9fff`) immediately after receiving the query. Hard-code the resolved `"zh"` or `"en"` value. Never pass `"auto"` to `export_event_results()` or `generate_event_dashboard()`. For visible stock labels, Chinese outputs use constituent names only and English outputs use tickers/symbols only. Keep `reason` values in the output language because they are written verbatim when displayed or audited. Treat mixed-language natural-language fields as validation errors. Before delivery, run `validate_event_outputs.py` after generating `report.md` and HTML, then cross-check PNG chart titles/labels as the only non-text-scanned artifact.

---

## Self-Check Checklist

```
[ ] 1. Does the event date have a clear source?
[ ] 2. Was the constituent list determined at a time <= the event date? Is survivorship bias disclosed?
[ ] 3. Are weights based on market cap from the trading day before the event?
[ ] 4. Are market-cap units normalized to CNY 100M?
[ ] 5. Are forward-adjusted prices used?
[ ] 6. Is suspended-stock handling explicit?
[ ] 7. Is NAV base date = pre_event_date (reference date)?
[ ] 8. Do weights sum to 100%?
[ ] 9. Are both market-cap-weighted and equal-weighted versions computed?
[ ] 10. Are HHI and largest weight disclosed?
[ ] 11. Are tiering standards documented?
[ ] 12. Are limit-up / limit-down effects noted?
[ ] 13. Is data coverage complete? Are missing values explained?
[ ] 14. Does the data-window length match the user request without being too wide?
[ ] 15. Is the Matplotlib Unicode font configured?
[ ] 16. Does the report include Assumptions and Known Limitations?
[ ] 17. Does the dashboard HTML open correctly?
[ ] 18. Is `generated_at` fixed and consistent between summary and manifest?
[ ] 19. Has the constituent source snapshot been saved?
[ ] 20. Are actual ifind parameters recorded, especially the adjustment convention?
[ ] 21. Has `<prefix>_run_manifest.json` been generated with output hashes?
[ ] 22. Does `reference/validate_event_outputs.py` pass?
[ ] 23. Are all output artifacts (HTML, PNG, report.md, summary/manifest) in the same language as the query? Is `language` resolved to a concrete "zh"/"en" value?
```
