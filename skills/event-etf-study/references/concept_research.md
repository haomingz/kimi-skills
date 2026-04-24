# Concept Stock Research Methodology

## 1. Search Workflow

### Define The Event And Concept
Clarify the event name, date, and core keywords. Example: event = DeepSeek-R1 release, date = 2025-01-20, keywords = DeepSeek / large language model / AI inference / domestic compute.

### Search Strategy Across Three Major Platforms

1. **Tonghuashun search**: visit Tonghuashun (10jqka), search the concept name, for example `"DeepSeek concept stocks"` or `"DeepSeek sector"`, and extract the related stock list.
2. **Xueqiu search**: visit Xueqiu, search the concept name, for example `"DeepSeek concept stocks"`, and extract the related stock list.
3. **East Money search**: visit East Money, search the concept name, for example `"DeepSeek concept stocks"` or `"DeepSeek sector"`, and extract the related stock list.
4. **Save snapshots**: write each platform's raw search results to `<prefix>_constituents_sources.csv`.
5. **Take the union**: derive the full candidate constituent set only from the snapshot file by taking the union of the three platform stock lists.
6. **Cross-validate**: validate the union with supplemental keywords such as `DeepSeek supply chain supplier core stocks`, and append any supplemental sources to the snapshot.

### Constituent Source Snapshot

For reproducibility, do not revisit the day's web results in later steps. Save a CSV first, then derive constituents from the CSV.

Recommended fields:

| Field | Description |
|---|---|
| `source` | `ths` / `xueqiu` / `eastmoney` / `ifind` / `research_report` / `news` |
| `query` | Search keyword |
| `fetched_at` | Fetch time in ISO format, using the same time zone as run manifest `generated_at` |
| `ticker` | Stock ticker |
| `name` | Stock name |
| `raw_text` | Raw result snippet or title |
| `source_url` | Recheckable URL; if no URL exists, use `ifind:<tool_name>` |
| `include` | `true` / `false`, whether to include in the candidate pool |
| `tier` | `1` / `2` / `3`, final tier |
| `reason` | One-sentence inclusion and tiering rationale |

### Source Priority

| Priority | Source | Notes |
|---|---|---|
| 1 | Union of the three platforms | Broadest coverage, combining the three major platforms |
| 2 | ifind concept board | Most standardized; can directly return constituent lists |
| 3 | Overlap across two platforms | Higher confidence; can serve as core candidates |
| 4 | Broker research reports | Deeper analysis, limited coverage |
| 5 | Financial news | Timely but uneven quality |

---

## 2. ifind Stock Selection

Prefer `ifind_get_related_stock`. Query multiple keywords, take the union, then filter:

```python
keywords = ["DeepSeek", "domestic compute", "AI chips"]
all_stocks = set()
for kw in keywords:
    result = ifind_get_related_stock(keyword=kw)
    all_stocks.update(result)
# Remove pure hype names and sort by relevance.
```

---

## 3. Tiering Standard

| Tier | Standard | Example |
|---|---|---|
| **T1 Core** | Directly related main business / revenue share >30% / core supplier / consistently identified by multiple research reports | Hygon Information (domestic GPU) |
| **T2 Strongly Related** | Revenue share 10-30% / upstream or downstream beneficiary / meaningful technical reserves | |
| **T3 Ecosystem** | Revenue share <10% / weaker relevance / sentiment-driven exposure | |

- Each stock must have a tier plus a one-sentence rationale.
- Default to downgrading ambiguous names by one tier.

---

## 4. Weight Calculation

### Market-Cap Weighted (Default)
Use total market cap from the trading day before the event as the basis: `weight_i = mcap_i / sum(mcap)`.

### Equal Weighted
`weight_i = 1 / N`

### Tier Weighted (Optional)
```python
tier_weights = {'T1': 0.60, 'T2': 0.30, 'T3': 0.10}
# Equal-weight within each tier.
```

---

## 5. Data Acquisition

| Data Item | Acquisition Method |
|---|---|
| Constituent list | Union of Tonghuashun / Xueqiu / East Money snapshots plus ifind validation |
| Daily close, forward-adjusted | `ifind_get_price`; record the actual `adjust` parameter |
| Total shares | `ifind_get_stock_info` -> `ths_total_shares_stock` |
| Benchmark index, optional | `ifind_get_price`, for example `000300.SH` |

---

## 6. MCP/ifind API Reference

Call ifind through the mshtools MCP service. Initialize the session first to obtain `Mcp-Session-Id`.

| API | Function | Key Parameters |
|---|---|---|
| `ifind_get_related_stock` | Concept-related stocks | `keyword` |
| `ifind_get_price` | Historical prices | `code`, `start_date`, `end_date`, `fields` (close/open/high/low/volume), `adjust` (backward/forward/none), `file_path` |
| `ifind_get_stock_info` | Basic information | `code`, `fields` (ths_total_shares_stock/total_market_cap, etc.) |
| `ifind_get_index_members` | Index constituents | `index_code` |

**Notes**:
- `ifind_get_price` must include `file_path`. The response `data_preview` is a CSV-format string; place `file_path` under `output/raw/`.
- Record every ifind call's parameters in the manifest or `run_metadata`, especially `adjust`.
- Batch requests should generally include no more than 5 stocks at a time.
- Returned market cap / shares may use raw shares or other units; convert market cap to CNY 100M carefully.
