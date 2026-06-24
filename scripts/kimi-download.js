/**
 * Kimi Official Skills Downloader — Playwright MCP form
 *
 * Drives the Skills tab on https://www.kimi.com/extensions?tab=skill to download
 * skill zips. Designed to be passed to:
 *   mcp__playwright__browser_evaluate
 *
 * USAGE (via Playwright MCP):
 *   1. Open https://www.kimi.com/extensions?tab=skill (logged in).
 *   2. (Optional) pick targets with a separate browser_evaluate:
 *        () => { window._kimiTargets = ["skill-a","skill-b"]; return 'ok'; }
 *      Omit to download ALL skills shown on the tab.
 *   3. Pass the ENTIRE contents of this file as the `function` argument.
 *      It returns 'started' IMMEDIATELY and runs the download loop in the page
 *      (fire-and-forget), so the tool call does not block for the whole batch.
 *   4. Poll progress with another browser_evaluate:
 *        () => ({ done: window._kimiDLDone, log: window._kimiDLLog, error: window._kimiDLError })
 *   5. After done === true, run kimi-extract.py to unzip into the repo.
 *
 * Download flow per skill (current Kimi UI, 2026):
 *   find .skill-card by its .skill-card-title text
 *     -> if its .skill-card-btn says "安装", click to install first
 *     -> click .skill-more-btn (the "More" ⋯ button)
 *     -> in the .skill-card-more-popover, click the .skill-menu-item whose text is "下载"
 * The zip downloads to the browser's normal download folder. In Playwright
 * `--extension` mode that is your real Chrome Downloads dir; in isolated mode it
 * is Playwright's MCP output dir. The 5.5 s spacing avoids Chrome throttling /
 * merging rapid downloads — do NOT reduce it.
 *
 * To run it in a plain DevTools console instead, wrap and invoke: (<paste>)()
 */
() => {
  if (window._kimiDLRunning) return 'already-running';
  window._kimiDLRunning = true;
  window._kimiDLDone = false;
  window._kimiDLLog = [];
  window._kimiDLError = null;
  window._kimiDLCurrent = null;

  (async () => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));

    if (!document.querySelector('.skill-card-title')) {
      throw new Error('No .skill-card-title — open the Skills tab (/extensions?tab=skill) first.');
    }

    const scrollEl = document.querySelector('.skill-page') || document.scrollingElement;

    const findCard = (name) => Array.from(document.querySelectorAll('.skill-card'))
      .find(c => c.querySelector('.skill-card-title')?.textContent?.trim() === name) || null;

    const downloadOne = async (name) => {
      window._kimiDLCurrent = name;

      let card = findCard(name);
      // Scroll to find the card if the list is virtualized.
      if (!card && scrollEl) {
        scrollEl.scrollTop = 0;
        await sleep(200);
        for (let i = 0; i < 40 && !card; i++) {
          scrollEl.scrollTop += 1200;
          await sleep(200);
          card = findCard(name);
        }
      }
      if (!card) throw new Error('card not found');

      card.scrollIntoView({ block: 'center' });
      await sleep(200);

      // Install first if not yet added (download only works after install).
      const primary = card.querySelector('.skill-card-btn');
      if (primary && primary.textContent.trim() === '安装') {
        primary.click();
        await sleep(2500);
      }

      // Open the card's "More" menu and click 下载 (Download).
      const moreBtn = card.querySelector('.skill-more-btn');
      if (!moreBtn) throw new Error('no more button');
      moreBtn.click();
      await sleep(600);

      const dl = Array.from(document.querySelectorAll('.skill-menu-item'))
        .find(el => el.textContent.trim() === '下载');
      if (!dl) throw new Error('no 下载 item in more menu');
      dl.click();

      // Critical: space out downloads so Chrome does not throttle/merge them.
      await sleep(5500);
    };

    const targets = window._kimiTargets?.length
      ? window._kimiTargets
      : Array.from(document.querySelectorAll('.skill-card-title')).map(e => e.textContent.trim());

    for (const name of targets) {
      try {
        await downloadOne(name);
        window._kimiDLLog.push({ name, ok: true });
      } catch (e) {
        window._kimiDLLog.push({ name, ok: false, error: e.message });
      }
    }

    window._kimiDLDone = true;
    window._kimiDLRunning = false;
  })().catch(e => {
    window._kimiDLError = String((e && e.message) || e);
    window._kimiDLDone = true;
    window._kimiDLRunning = false;
  });

  return 'started';
}
