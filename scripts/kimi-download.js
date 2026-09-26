/**
 * Kimi Official Skills Downloader
 *
 * Drives the Skills tab on https://www.kimi.com/skills to download skill zips.
 *   - Built-in agent browser: Runtime.evaluate this file as "(<paste>)()"
 *   - Playwright MCP: pass the entire file as browser_evaluate's function
 *
 * Prefer the signed zip URL from getSkillFileTree when the browser cannot save
 * downloads (typical of an in-agent browser). This menu clicker is the fallback
 * for a browser that writes zip files to a Downloads folder.
 *
 * USAGE (via Playwright MCP):
 *   1. Open https://www.kimi.com/skills (logged in). Expand section overflow
 *      rows first so every card is in the DOM.
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
 *     -> if its install button says "安装", "Add", or "Install", click it first
 *     -> click .skill-more-btn (the "More" ⋯ button)
 *     -> click the menu item whose text is "下载" or "Download"
 *        (.skill-menu-item or .kimi-menu-item)
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
      const primary = card.querySelector('.skill-card-btn, .skill-card-use-btn');
      const primaryLabel = primary && primary.textContent.trim();
      if (primaryLabel === '安装' || primaryLabel === 'Add' || primaryLabel === 'Install') {
        primary.click();
        await sleep(2500);
      }

      // Open the card's "More" menu and click 下载 / Download.
      const moreBtn = card.querySelector('.skill-more-btn');
      if (!moreBtn) throw new Error('no more button');
      moreBtn.click();
      await sleep(600);

      const dl = Array.from(document.querySelectorAll('.skill-menu-item, .kimi-menu-item'))
        .find(el => {
          const label = el.textContent.trim();
          return label === '下载' || label === 'Download';
        });
      if (!dl) throw new Error('no 下载/Download item in more menu');
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
