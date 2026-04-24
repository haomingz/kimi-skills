/**
 * Kimi Skills Lister
 * Run in the browser console on https://www.kimi.com/ while the Kimi Picks panel is open.
 * Outputs the full list of skill names for use with kimi-audit.ps1 or kimi-download.js.
 *
 * USAGE:
 *   1. Open the Kimi Picks skill panel on kimi.com
 *   2. Paste this in DevTools console
 *   3. Copy the printed list and pass to kimi-audit.ps1 -KimiNames "..."
 */
(() => {
  const rows = Array.from(document.querySelectorAll('.skill-row'));
  if (rows.length === 0) {
    console.error('No .skill-row elements found — open the Kimi Picks panel first.');
    return;
  }
  const names = rows.map(r => r.querySelector('.skill-name')?.innerText?.trim()).filter(Boolean);
  console.log(`Total skills visible: ${names.length}`);
  console.log('Names (comma-separated for kimi-audit.ps1):');
  console.log(names.join(','));
  return names;
})();
