/**
 * Kimi Skills Lister — Playwright MCP form
 *
 * Pass the ENTIRE contents of this file as the `function` argument of
 *   mcp__playwright__browser_evaluate
 * while the Skills tab is open at https://www.kimi.com/extensions?tab=skill .
 * It RETURNS a comma-separated string of every skill name (or null if the
 * Skills tab is not open). Pass that string to:  kimi-audit.py --kimi-names "..."
 *
 * To run it in a plain DevTools console instead, wrap and invoke: (<paste>)()
 *
 * NOTE: Current Kimi UI (2026) selectors —
 *       card        : .skill-card
 *       card title  : .skill-card-title   (was .card-name)
 *       scroll host : main.skill-page     (was .skill-cards-scroll)
 *       All cards normally render at once; the scroll loop is a safety net in
 *       case the list virtualizes for larger catalogs.
 */
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  // Skills tab not open / wrong tab.
  if (!document.querySelector('.skill-card-title')) return null;

  const scrollEl = document.querySelector('.skill-page') || document.scrollingElement;
  const names = new Set();
  let lastCount = 0;
  let stableRounds = 0;

  if (scrollEl) scrollEl.scrollTop = 0;
  await sleep(300);

  for (let i = 0; i < 50; i++) {
    document.querySelectorAll('.skill-card-title').forEach(el => {
      const t = el.textContent?.trim();
      if (t) names.add(t);
    });

    if (names.size === lastCount) {
      stableRounds++;
      if (stableRounds >= 3) break;
    } else {
      stableRounds = 0;
    }
    lastCount = names.size;

    if (scrollEl) scrollEl.scrollTop += 1500;
    await sleep(300);
  }

  return Array.from(names).sort().join(',');
}
