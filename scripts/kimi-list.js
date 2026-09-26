/**
 * Kimi Skills Lister
 *
 * Run this in the page while https://www.kimi.com/skills is open and logged in.
 *   - Built-in agent browser: browser_cdp Runtime.evaluate, awaitPromise true,
 *     expression is "(<paste>)()"
 *   - Playwright MCP: pass the entire file as browser_evaluate's function
 *   - DevTools console: (<paste>)()
 *
 * Returns a comma-separated string of every skill name, or null if the Skills
 * tab is not open. Pass that string to: kimi-audit.py --kimi-names "..."
 *
 * Each category first renders about 10 cards. Overflow rows
 * (button.skill-section-overflow) are expanded before the scroll scrape.
 */
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  // Skills tab not open / wrong tab.
  if (!document.querySelector('.skill-card-title')) return null;

  for (let round = 0; round < 25; round++) {
    const more = Array.from(document.querySelectorAll('button.skill-section-overflow'));
    if (!more.length) break;
    for (const btn of more) btn.click();
    await sleep(700);
  }

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
