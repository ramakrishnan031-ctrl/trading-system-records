/* ============================================================================
 * GUI DEPLOYED-INSTANCE SWEEP  —  03-Sep-2026
 * ----------------------------------------------------------------------------
 * HOW TO RUN (👤 Rama):
 *   1. Restart gui-dashboard FIRST, and confirm the new PID. This script does
 *      NOT check that — a sweep against the old process is void (auto_reload is
 *      off, so a template cached before the deploy stays cached).
 *   2. Open the dashboard, log in normally, and land on ANY dashboard page.
 *   3. Open devtools → Console → paste this whole file → Enter.
 *   4. ⚠️ KEEP THE TAB VISIBLE AND FOCUSED until it prints END. Chrome throttles
 *      timers to ~1s in a background tab and may suspend rendering entirely,
 *      which makes the settle loop slow and the measurements unreliable.
 *      Expect roughly 3 minutes for 21 routes x 2 viewports.
 *   5. When it finishes, copy the WHOLE console output back (it is also left in
 *      window.__GUI_SWEEP as a single string).
 *
 * WHY THE CONSOLE, AND NOT A FILE:
 *   The script reads each route's rendered document through a SAME-ORIGIN
 *   iframe. Run from a local file that is cross-origin and every read is
 *   blocked. It must run on the dashboard's own origin.
 *
 * WHAT IT DOES *NOT* DO — read this before trusting it:
 *   · It moves NO credential. No cookie, password or TOTP is read, printed or
 *     transmitted. It only navigates iframes inside the session you already
 *     have open.
 *   · It performs NO writes. Every route it visits is a GET page route.
 *   · It changes nothing on the VM and touches no config.
 *
 * IT SELF-TESTS BEFORE IT MEASURES. If SELFTEST fails, the run is void and it
 * stops — a detector that cannot return a wrong answer has not been validated.
 * ========================================================================== */
(async () => {
  'use strict';

  // ==== CONFIG — auditable, change nothing silently ========================
  // TEST HOOK: inert in production. If window.__GUI_SWEEP_CFG is undefined
  // (it will be, on the dashboard) every value below is the shipped default.
  // It exists so this exact file could be validated against a synthetic origin
  // before being pasted into a live session.
  const CFG = (typeof window !== 'undefined' && window.__GUI_SWEEP_CFG) || {};
  if (CFG.__present) console.log('⚠️ TEST CONFIG ACTIVE — this is not a production run');

  const CONTINUE_ON_S02_FAIL = false;   // S02 is a PRECONDITION, not a probe.

  // SCOPE. The question "is the deployed GUI serving the refitted build?" is
  // fully answered by C0-C2 (SELFTEST + AUTHENTICATED + DEPLOYED-S02 + S17) and
  // takes well under a minute. Everything after that is BASELINE-BUILDING for
  // the future, not deployment verification.
  //   false = full sweep (~3 min focused) — also prints the C2 answer in place
  //   true  = stop after S17 and report
  // ⚠️ If you stop early, the record must say "deployment verified at C2;
  //    Tiers 2 and 3 not measured" — ⛔ never "sweep complete".
  const STOP_AFTER_C2 = CFG.STOP_AFTER_C2 ?? false;
  const ANSWER_AT = 'S17';              // the last screen of the minimum answer
  const VIEWPORTS  = CFG.VIEWPORTS || [[1920, 1080], [1440, 900]];
  const SETTLE_MS  = 300;   // poll interval while waiting for height to settle
  const SETTLE_N   = 3;     // consecutive identical samples == settled
  const SETTLE_MAX = 30000; // hard cap per route/viewport
  const SUB13_FLOOR = 13;   // px

  // S02's 19-Aug recorded numbers — the environment precondition.
  const S02_EXPECT = CFG.S02_EXPECT || { h: 1212, ovf: false, sub13: 0 };
  const S02_ROUTE  = CFG.S02_ROUTE  || '/';

  // route, screen id, template churn since be41d3c (19-Aug capture)
  const ROUTES = CFG.ROUTES || [
    ['/',                     'S02', 'dashboard.html',           'UNCHANGED'],
    ['/controls',             'S17', 'controls.html',            'freeze+new backend'],
    ['/execution',            'S11', 'execution.html',           'freeze'],
    ['/live-activity',        'S18', 'live_activity.html',       'freeze'],
    ['/config',               'S16', 'config.html',              'freeze'],
    ['/scanner-attribution',  'S21', 'scanner_attribution.html', 'freeze'],
    ['/strategy-ranking',     'S19', 'strategy_ranking.html',    'freeze'],
    ['/strategy-health',      'S20', 'strategy_health.html',     'freeze'],
    ['/trade-logs',           'S14', 'trade_logs.html',          '112+/25-'],
    ['/strategies',           'S03', 'strategies.html',          '149+/67-'],
    ['/trades',               'S07', 'trade_explorer.html',      '20+/29-'],
    ['/signals',              'S04', 'signals.html',             '17+/31-'],
    ['/orders',               'S05', 'orders.html',              '33+/36-'],
    ['/positions',            'S06', 'positions.html',           '50+/44-'],
    ['/capital-risk',         'S08', 'capital_risk.html',        '885+/417-'],
    ['/pnl-analytics',        'S09', 'pnl_analytics.html',       '97+/19-'],
    ['/slippage',             'S10', 'slippage.html',            '64+/28-'],
    ['/services',             'S12', 'services.html',            '211+/60-'],
    ['/audit',                'S13', 'audit.html',               '39+/45-'],
    ['/logs',                 'S15', 'logs.html',                '151+/103-'],
    ['/holdings',             'S22', 'holdings.html',            '34+/28-'],
  ];

  const out = [];
  const say = (s) => { out.push(s); console.log(s); };

  // ==== DETECTORS — one definition, used by the self-test AND the sweep =====
  // h: matches the 19-Aug instrument's stated definition (documentElement.scrollHeight).
  const mHeight = (d) => d.documentElement.scrollHeight;
  const mScrollW = (d) => d.documentElement.scrollWidth;
  const mClientW = (d) => d.documentElement.clientWidth;
  const mOvf = (d) => mScrollW(d) > mClientW(d);

  // sub13: elements carrying THEIR OWN text below the floor (not text in children).
  const mSub13 = (d) => {
    let n = 0; const byClass = {};
    for (const el of d.querySelectorAll('*')) {
      let own = '';
      for (const node of el.childNodes) {
        if (node.nodeType === 3) own += node.nodeValue;
      }
      if (!own.trim()) continue;
      const fs = parseFloat(d.defaultView.getComputedStyle(el).fontSize);
      if (fs && fs < SUB13_FLOOR) {
        n++;
        const cn = (typeof el.className === 'string') ? el.className.trim() : '';
        const k = cn || el.tagName.toLowerCase();
        byClass[k] = (byClass[k] || 0) + 1;
      }
    }
    return { n, byClass };
  };

  // clipped: a table cell whose content is wider than its box.
  const mClipped = (d) => {
    let n = 0;
    for (const c of d.querySelectorAll('td, th')) {
      if (c.scrollWidth > c.clientWidth + 1) n++;
    }
    return n;
  };

  // authenticated: chrome that only an authenticated render carries,
  // AND positive proof we are not looking at the login page.
  const mAuth = (d) => {
    const marks = ['.sidebar', '.btn-logout', '.shell'].filter((s) => d.querySelector(s));
    const isLogin = !!d.querySelector('.login-hero, .login-card-wrap');
    return { ok: marks.length > 0 && !isLogin, marks, isLogin };
  };

  // ==== IFRAME PLUMBING ====================================================
  const mkFrame = (w, h) => {
    const f = document.createElement('iframe');
    f.style.cssText =
      `position:fixed;left:-20000px;top:0;border:0;margin:0;padding:0;` +
      `width:${w}px;height:${h}px;`;
    document.body.appendChild(f);
    return f;
  };

  const loadInto = (f, url) => new Promise((res, rej) => {
    const t = setTimeout(() => rej(new Error('load timeout ' + url)), SETTLE_MAX);
    f.onload = () => { clearTimeout(t); res(); };
    f.src = url;
  });

  // Wait until the page stops growing — these screens fetch their data async,
  // and measuring an empty table would understate every height.
  const settle = async (f) => {
    const t0 = Date.now(); let last = -1, same = 0;
    while (Date.now() - t0 < SETTLE_MAX) {
      await new Promise((r) => setTimeout(r, SETTLE_MS));
      const h = mHeight(f.contentDocument);
      if (h === last) { if (++same >= SETTLE_N) return { settled: true, ms: Date.now() - t0 }; }
      else { last = h; same = 0; }
    }
    return { settled: false, ms: Date.now() - t0 };
  };

  // ==== 0. PREFLIGHT =======================================================
  say('================ GUI DEPLOYED-INSTANCE SWEEP — 03-Sep-2026 ================');
  say('origin        : ' + location.origin);
  say('host page     : ' + location.pathname);
  say('UA            : ' + navigator.userAgent);
  say('host DPR      : ' + window.devicePixelRatio + '   (host window is NOT the measurement surface)');
  say('started       : ' + new Date().toISOString());
  say('');

  const hostAuth = mAuth(document);
  say('C0  AUTHENTICATED = ' + (hostAuth.ok ? 'TRUE' : 'FALSE') +
      '   markers=[' + hostAuth.marks.join(',') + '] loginPage=' + hostAuth.isLogin);
  if (!hostAuth.ok) {
    say('⛔ ABORT — this is not an authenticated dashboard page. Log in, open a');
    say('   dashboard screen, and paste again. (Two earlier probes died here.)');
    return;
  }
  say('');

  // ==== 1. SELFTEST — prove each detector CAN return non-zero ===============
  say('SELFTEST — mutation-testing every detector before any number is believed');
  // A freshly appended iframe is already about:blank and its document is
  // available synchronously. ⛔ Do NOT loadInto('about:blank') — the load event
  // may never fire for a document the frame already has, and the run would hang.
  const sf = mkFrame(800, 600);
  const sd = sf.contentDocument;
  sd.body.innerHTML =
    '<div id="tiny" style="font-size:9px">tiny text</div>' +
    '<div style="width:4000px;height:10px"></div>' +
    '<table><tr><td id="clip" style="width:20px;max-width:20px;overflow:hidden;' +
    'white-space:nowrap">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</td></tr></table>';
  await new Promise((r) => setTimeout(r, 400));

  const t_sub13 = mSub13(sd).n, t_clip = mClipped(sd), t_ovf = mOvf(sd);
  say('  sub13 detector fired : ' + t_sub13 + '   (expect >=1 on a 9px element)');
  say('  clipped detector fired: ' + t_clip + '   (expect >=1 on a 20px cell of 30 chars)');
  say('  overflow detector fired: ' + t_ovf + '   (expect true on a 4000px child)');

  sd.body.innerHTML = '<div style="font-size:20px">normal</div>';
  await new Promise((r) => setTimeout(r, 200));
  const n_sub13 = mSub13(sd).n, n_clip = mClipped(sd), n_ovf = mOvf(sd);
  say('  and go quiet on a clean page: sub13=' + n_sub13 + ' clipped=' + n_clip + ' ovf=' + n_ovf);

  const selftestOK = t_sub13 >= 1 && t_clip >= 1 && t_ovf === true &&
                     n_sub13 === 0 && n_clip === 0 && n_ovf === false;
  say('  SELFTEST: ' + (selftestOK ? 'PASS' : '⛔ FAIL'));
  sf.remove();
  if (!selftestOK) {
    say('⛔ ABORT — a detector cannot be trusted. Every zero below would be meaningless.');
    return;
  }
  say('');

  // ==== 2. THE SWEEP =======================================================
  const rows = [];
  // Focus/visibility is sampled AROUND every measurement. Chrome throttles
  // timers AND can suspend rendering in a background tab, so a row measured
  // while the tab was not focused is WRONG, not merely slow — and nothing else
  // in the output would say so. "Keep the tab focused" is an instruction to a
  // human mid-run; this is the control.
  const focusNow = () => ({ f: document.hasFocus(), v: document.visibilityState });

  const measure = async (route, w, h) => {
    const fb = focusNow();
    const f = mkFrame(w, h);
    try {
      await loadInto(f, route);
      const iw = f.contentWindow.innerWidth, ih = f.contentWindow.innerHeight;
      if (iw !== w) {
        return { err: `VIEWPORT ${iw}x${ih} != ${w}x${h} — DPR/layout trap, number void` };
      }
      const st = await settle(f);
      const d = f.contentDocument;
      const a = mAuth(d);
      const s = mSub13(d);
      const fa = focusNow();
      const focusOK = fb.f && fa.f && fb.v === 'visible' && fa.v === 'visible';
      const cw = mClientW(d);
      return {
        h: mHeight(d), sw: mScrollW(d), cw, ovf: mOvf(d),
        scrollbarPx: w - cw,          // >0 means a vertical scrollbar narrowed the box
        sub13: s.n, sub13by: s.byClass, clipped: mClipped(d),
        auth: a.ok, isLogin: a.isLogin, focusOK, focusBefore: fb, focusAfter: fa,
        settled: st.settled, ms: st.ms, vp: `${iw}x${ih}`, reqW: w,
      };
    } catch (e) {
      return { err: String(e && e.message || e) };
    } finally { f.remove(); }
  };

  const fmt = (r) => r.err ? ('ERR ' + r.err)
    : `h=${r.h} ovf=${r.ovf} (sw=${r.sw}/cw=${r.cw} sbar=${r.scrollbarPx}) ` +
      `sub13=${r.sub13} clipped=${r.clipped} auth=${r.auth}` +
      `${r.isLogin ? ' ⛔LOGINPAGE' : ''}${r.focusOK ? '' : ' ⛔UNFOCUSED'}` +
      `${r.settled ? '' : ' ⚠️UNSETTLED'} ${r.ms}ms`;

  // --- C1: S02 is the environment PRECONDITION, run first ------------------
  say('C1  DEPLOYED-S02 ENVIRONMENT PRECONDITION');
  say('    historical record (19-Aug, approval_final_19aug/INDEX.md): h=' +
      S02_EXPECT.h + ' ovf=' + S02_EXPECT.ovf + ' sub13=' + S02_EXPECT.sub13 +
      '   ⛔ cw was NOT recorded then');
  const s02 = await measure(S02_ROUTE, VIEWPORTS[0][0], VIEWPORTS[0][1]);
  say('    ' + S02_ROUTE + '  @' + VIEWPORTS[0][0] + 'x' + VIEWPORTS[0][1] + '  ' + fmt(s02));
  // The verdict is TWO-PART: the height AND the client width it was measured in.
  // DEPLOYED-S02's recorded height (1212) exceeds the 1080 viewport, so there WILL
  // be a vertical scrollbar; it narrows the client box, which REFLOWS the page and
  // changes the height. Scrollbar width is exactly the environmental variable we
  // cannot control — and the 19-Aug instrument never recorded cw. So a height
  // mismatch with a scrollbar present is DIAGNOSABLE, not automatically a failure.
  // ⚠️ WHY THERE IS NO "SCROLLBAR-PLAUSIBLE" PASS LABEL HERE.
  // DEPLOYED-S02's recorded height (1212) EXCEEDS the 1080 viewport, so a
  // vertical scrollbar is CERTAIN ⇒ scrollbarPx > 0 ALWAYS ⇒ a classifier that
  // keys on "is a scrollbar present" would return the same answer for every
  // possible deviation. That branch is algebraically unreachable for the one
  // screen it was built for. So the scrollbar is not a verdict — the MAGNITUDES
  // are printed side by side and the reader judges. ⛔ No tolerance, ⛔ no band.
  let s02ok = false, s02diag = '';
  if (!s02.err) {
    const okH = s02.h === S02_EXPECT.h, okO = s02.ovf === S02_EXPECT.ovf,
          okS = s02.sub13 === S02_EXPECT.sub13;
    s02ok = okH && okO && okS;
    if (!s02ok) {
      const dh = s02.h - S02_EXPECT.h, sb = s02.scrollbarPx;
      say('    Δ vs 19-Aug: h ' + dh + ' | ovf ' + S02_EXPECT.ovf +
          '→' + s02.ovf + ' | sub13 ' + S02_EXPECT.sub13 + '→' + s02.sub13);
      say('    MAGNITUDES:  Δh = ' + Math.abs(dh) + 'px   ·   scrollbar = ' + sb + 'px' +
          (sb > 0 ? '   ·   ratio ' + (Math.abs(dh) / sb).toFixed(1) + '×' : ''));
      say('    cw=' + s02.cw + ' of requested ' + s02.reqW +
          '. A scrollbar is ~15-25px and its reflow effect on page height is');
      say('    bounded by that order. ⛔ A scrollbar being PRESENT proves nothing here —');
      say('    at h=' + S02_EXPECT.h + ' vs a ' + VIEWPORTS[0][1] +
          'px viewport one is CERTAIN. Judge the ratio.');
      if (s02.sub13) say('    sub13 breakdown: ' + JSON.stringify(s02.sub13by));
      s02diag = (okO && okS) ? 'HEIGHT-ONLY' : 'MORE-THAN-HEIGHT';
    }
  }
  say('    VERDICT: ' + (s02ok ? '✅ environment COMPARABLE (necessary, not sufficient)'
        : (s02diag === 'HEIGHT-ONLY'
             ? '⚠️ DEVIATION — HEIGHT ONLY (ovf and sub13 both match)'
             : '🔴 DEVIATION — MORE THAN THE HEIGHT MOVED')));
  if (!s02ok && !CONTINUE_ON_S02_FAIL) {
    say('');
    if (s02diag === 'HEIGHT-ONLY') {
      say('⚠️ HALTED — only the HEIGHT differs; overflow and sub-13px both match.');
      say('   A narrower client box (scrollbar) reflows the page, so SOME of this');
      say('   deviation may be scrollbar width. How much is a judgement about the');
      say('   MAGNITUDES printed above — ⛔ this script does not decide it, because any');
      say('   cutoff would be an invented tolerance.');
      say('   🔴 NOT RESOLVABLE against the historical record either way: the 19-Aug');
      say('   instrument did not record cw. It can be HYPOTHESISED, not PROVEN.');
      say('   ⇒ 👤 Rama decides. If the ratio is small, record as "deviation, plausibly');
      say('     scrollbar-width; not resolvable against the historical record".');
      say('     If it is large, the scrollbar cannot account for it — treat as');
      say('     environmental and investigate fonts / static assets / browser.');
    } else {
      say('🔴 STOP — S02 is a PRECONDITION, not a probe. Its template is byte-unchanged');
      say('   since the 19-Aug capture, it gained no freeze wrap, and the only CSS rule');
      say('   reaching it is a text-align change that cannot move these metrics.');
      say('   MORE THAN THE HEIGHT MOVED — overflow and/or sub-13px changed too, and a');
      say('   scrollbar cannot explain either. The RENDERING ENVIRONMENT differs, so');
      say('   every other number would carry the same unknown offset, including S14');
      say('   and all of Tier 3.');
      say('   Investigate the environment (fonts, static assets, browser) before sweeping.');
    }
    say('   (To override deliberately, set CONTINUE_ON_S02_FAIL = true and re-paste.)');
    say('');
    say('================ END (halted at C1) ================');
    window.__GUI_SWEEP = out.join('\n');
    return;
  }
  say('');

  // --- C2..C4: the rest, both viewports ------------------------------------
  say('C2-C4  FULL SWEEP');
  say('screen route                    churn//note          viewport   metrics');
  let answered = false;
  for (const [route, sid, tpl, churn] of ROUTES) {
    for (const [w, h] of VIEWPORTS) {
      const r = (sid === 'S02' && w === VIEWPORTS[0][0]) ? s02 : await measure(route, w, h);
      rows.push({ sid, route, churn, w, h, r });
      say('  ' + sid.padEnd(5) + route.padEnd(24) + String(churn).padEnd(20) +
          `${w}x${h}`.padEnd(11) + fmt(r));
    }
    if (sid === ANSWER_AT && !answered) {
      answered = true;
      say('');
      say('  ══════ COMPLETE ANSWER REACHED (C2) ══════');
      say('  Everything above answers "is the deployed GUI serving the refitted');
      say('  build?" — environment comparable, and S17 rendered by a backend whose');
      say('  controls.py did not exist at 39292d3. Everything BELOW is');
      say('  baseline-building for the future, ⛔ not deployment verification.');
      say('  ⚠️ If you stop here, record "deployment verified at C2; Tiers 2 and 3');
      say('     not measured" — ⛔ never "sweep complete".');
      say('  ══════════════════════════════════════════');
      say('');
      if (STOP_AFTER_C2) { say('  STOP_AFTER_C2 = true ⇒ stopping here by request.'); break; }
    }
  }
  say('');

  // --- summary -------------------------------------------------------------
  const bad = rows.filter((x) => x.r.err || x.r.isLogin || x.r.auth === false ||
                                 x.r.focusOK === false);
  say('INTEGRITY: ' + (bad.length === 0
      ? 'all routes authenticated, none served the login page, tab stayed focused, no errors'
      : '⛔ ' + bad.length + ' row(s) suspect (NOT data): ' +
        bad.map((x) => x.sid + '@' + x.w).join(', ')));
  const unfoc = rows.filter((x) => x.r.focusOK === false);
  if (unfoc.length) {
    say('⛔ UNFOCUSED — the tab lost focus/visibility across these rows. Chrome');
    say('   throttles timers AND can suspend rendering when backgrounded, so these');
    say('   numbers are WRONG, not merely slow. Re-run them with the tab focused:');
    say('   ' + unfoc.map((x) => x.sid + '@' + x.w).join(', '));
  }
  const unsettled = rows.filter((x) => !x.r.err && x.r.settled === false);
  if (unsettled.length) say('⚠️ UNSETTLED (height still moving at cap): ' +
      unsettled.map((x) => x.sid + '@' + x.w).join(', '));
  say('finished      : ' + new Date().toISOString());
  say('================ END ================');
  say('');
  say('Copy everything above. It is also in window.__GUI_SWEEP (a string).');
  window.__GUI_SWEEP = out.join('\n');
})();
