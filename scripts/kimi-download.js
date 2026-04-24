/**
 * Kimi Official Skills Downloader
 * Run this in the browser console on https://www.kimi.com/ while the Kimi Picks
 * skill dialog is open (the panel listing all official skills).
 *
 * USAGE:
 *   1. Open https://www.kimi.com/ and log in
 *   2. Open the Kimi Picks / skill browser panel so .skill-row elements are visible
 *   3. Open DevTools console (F12)
 *   4. Paste this entire script and press Enter
 *   5. Optionally pass a subset list: window._kimiTargets = ["skill-a", "skill-b"]
 *      before running, otherwise ALL visible skills are downloaded
 *   6. Monitor progress: window._kimiDLLog
 *   7. After done=true, run kimi-extract.ps1 to unzip into the repo
 *
 * Chrome will ask to allow multiple downloads — click "Allow".
 * A 5.5 s delay between downloads prevents Chrome from blocking them.
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

  // Collect skill names to download
  const allRows = Array.from(document.querySelectorAll('.skill-row'));
  if (allRows.length === 0) {
    console.error('[kimi-dl] No .skill-row elements found. Open the skills panel first.');
    return;
  }

  const allNames = allRows.map(r => r.querySelector('.skill-name')?.innerText?.trim()).filter(Boolean);
  const targets = window._kimiTargets?.length ? window._kimiTargets : allNames;

  window._kimiDLLog = [];
  window._kimiDLDone = false;
  window._kimiDLCurrent = null;

  console.log(`[kimi-dl] Starting download of ${targets.length} skills...`);

  const downloadOne = async (name) => {
    window._kimiDLCurrent = name;

    const row = allRows.find(r => r.querySelector('.skill-name')?.innerText?.trim() === name);
    if (!row) throw new Error('row not found');

    row.click();
    await sleep(900);

    const modal = document.querySelector('.skill-preview-modal');
    if (!modal) throw new Error('modal not found');

    // Install skill if not yet added (download zip only appears after installing)
    const addBtn = modal.querySelector('button.btn-primary');
    if (addBtn && addBtn.innerText.trim() === 'Add') {
      addBtn.click();
      await sleep(3000);
    }

    // Wait for zip download button (only visible after skill is installed)
    const dlBtn = await waitFor(
      () => Array.from(modal.querySelectorAll('.action-icon')).find(e => e.querySelector('svg[name="Download"]')),
      8000
    );
    dlBtn.click();

    // Critical: Chrome blocks rapid successive downloads — must wait ≥5 s
    await sleep(5500);

    const closeBtn = Array.from(modal.querySelectorAll('.action-icon')).find(e => e.querySelector('svg[name="Close"]'));
    if (closeBtn) closeBtn.click();
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
