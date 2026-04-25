/**
 * Kimi Skills Lister
 * Run in the browser console on https://www.kimi.com/ while the Kimi Picks panel is open.
 * Outputs the full list of skill names for use with kimi-audit.py or kimi-download.js.
 *
 * USAGE:
 *   1. Open the Kimi Picks skill panel on kimi.com
 *   2. Paste this in DevTools console (or evaluate_script via chrome-devtools MCP)
 *   3. Copy the printed list and pass to kimi-audit.py --kimi-names "..."
 *
 * NOTE: Uses .skill-card / .card-name selectors (current Kimi UI as of 2025).
 *       Uses textContent (not innerText) since these elements are hidden/virtual.
 *       Scrolls through the entire list to load all lazy-rendered cards.
 */
(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  const scrollEl = document.querySelector('.skill-cards-scroll');
  if (!scrollEl) {
    console.error('No .skill-cards-scroll element found — open the Kimi Picks panel first.');
    return null;
  }

  const names = new Set();
  let lastCount = 0;
  let stableRounds = 0;

  scrollEl.scrollTop = 0;
  await sleep(300);

  for (let i = 0; i < 50; i++) {
    document.querySelectorAll('.card-name').forEach(el => {
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

    scrollEl.scrollTop += 1500;
    await sleep(400);
  }

  const sorted = Array.from(names).sort();
  console.log(`Total skills found: ${sorted.length}`);
  console.log('Names (comma-separated for kimi-audit.py --kimi-names):');
  console.log(sorted.join(','));
  return sorted.join(',');
})();
