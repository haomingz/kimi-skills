/**
 * Kimi Official Skills Downloader
 * Run this in the browser console on https://www.kimi.com/ while the Kimi Picks
 * skill dialog is open (the panel listing all official skills).
 *
 * USAGE:
 *   1. Open https://www.kimi.com/ and log in
 *   2. Open the Kimi Picks skill browser panel
 *   3. Open DevTools console (F12)
 *   4. Optionally set targets: window._kimiTargets = ["skill-a", "skill-b"]
 *      before running, otherwise ALL visible skills are downloaded
 *   5. Paste this entire script and press Enter
 *   6. Monitor progress: window._kimiDLLog
 *   7. After done=true, run kimi-extract.py to unzip into the repo
 *
 * Chrome will ask to allow multiple downloads — click "Allow".
 * A 5.5 s delay between downloads prevents Chrome from blocking them.
 *
 * NOTE: Uses .skill-card / .card-name selectors (current Kimi UI as of 2025).
 */

(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  const waitFor = (fn, timeout = 8000) => new Promise((res, rej) => {
    const start = Date.now();
    const poll = () => {
      const v = fn();
      if (v) return res(v);
      if (Date.now() - start > timeout) return rej(new Error('waitFor timeout'));
      setTimeout(poll, 300);
    };
    poll();
  });

  const scrollEl = document.querySelector('.skill-cards-scroll');
  if (!scrollEl) {
    console.error('[kimi-dl] No .skill-cards-scroll element found. Open the skills panel first.');
    return;
  }

  // Scroll through to load all lazy-rendered cards
  scrollEl.scrollTop = 0;
  await sleep(300);
  const allNames = new Set();
  let lastCount = 0;
  let stableRounds = 0;
  for (let i = 0; i < 50; i++) {
    document.querySelectorAll('.card-name').forEach(el => {
      const t = el.textContent?.trim();
      if (t) allNames.add(t);
    });
    if (allNames.size === lastCount) {
      stableRounds++;
      if (stableRounds >= 3) break;
    } else {
      stableRounds = 0;
    }
    lastCount = allNames.size;
    scrollEl.scrollTop += 1500;
    await sleep(400);
  }
  scrollEl.scrollTop = 0;
  await sleep(300);

  const targets = window._kimiTargets?.length ? window._kimiTargets : Array.from(allNames);
  console.log(`[kimi-dl] Found ${allNames.size} skills total, downloading ${targets.length}...`);

  window._kimiDLLog = [];
  window._kimiDLDone = false;
  window._kimiDLCurrent = null;

  const findCard = async (name) => {
    // Scroll to find the card (lazy rendering means it may not be in DOM yet)
    scrollEl.scrollTop = 0;
    await sleep(300);
    for (let attempt = 0; attempt < 30; attempt++) {
      const cards = Array.from(document.querySelectorAll('.skill-card'));
      const card = cards.find(c => c.querySelector('.card-name')?.textContent?.trim() === name);
      if (card) return card;
      scrollEl.scrollTop += 1500;
      await sleep(400);
    }
    return null;
  };

  const downloadOne = async (name) => {
    window._kimiDLCurrent = name;

    const card = await findCard(name);
    if (!card) throw new Error('card not found');

    card.click();
    await sleep(1000);

    // Install skill if not yet added (download zip only appears after installing)
    const addBtn = Array.from(document.querySelectorAll('button.btn-primary'))
      .find(b => b.textContent?.trim() === 'Add');
    if (addBtn) {
      addBtn.click();
      await sleep(3000);
    }

    // Wait for download icon in the skill preview modal header
    const dlIcon = await waitFor(
      () => Array.from(document.querySelectorAll('.action-icon'))
             .find(el => el.querySelector('svg[name="Download"]')),
      8000
    );
    dlIcon.click();

    // Critical: Chrome blocks rapid successive downloads — must wait ≥5 s
    await sleep(5500);

    const closeIcon = Array.from(document.querySelectorAll('.action-icon'))
      .find(el => el.querySelector('svg[name="Close"]'));
    if (closeIcon) closeIcon.click();
    await sleep(700);
  };

  for (const name of targets) {
    try {
      await downloadOne(name);
      window._kimiDLLog.push({ name, ok: true });
      console.log(`[kimi-dl] ✓ ${name} (${window._kimiDLLog.length}/${targets.length})`);
    } catch (e) {
      window._kimiDLLog.push({ name, ok: false, error: e.message });
      console.warn(`[kimi-dl] ✗ ${name}: ${e.message}`);
    }
  }

  window._kimiDLDone = true;
  const ok = window._kimiDLLog.filter(l => l.ok).length;
  const failed = window._kimiDLLog.filter(l => !l.ok);
  console.log(`[kimi-dl] Done. ${ok}/${targets.length} succeeded.`);
  if (failed.length) console.warn('[kimi-dl] Failed:', failed.map(l => l.name));
})();
