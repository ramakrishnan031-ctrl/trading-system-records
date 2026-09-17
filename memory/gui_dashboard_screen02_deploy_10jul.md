---
name: gui_dashboard_screen02_deploy_10jul
description: "GUI Screen-02 Dashboard — REBUILT to Mission Control mockup, PUSHED+DEPLOYED 85058e5 (10-Jul); v1 e1faf29 rejected as incremental. UI-only, backend untouched."
metadata: 
  node_type: memory
  type: project
  originSessionId: fdc2ec50-6d89-4677-aad8-58c61d58972c
---

# ⭐ REBUILD (current) — Screen-02 "Mission Control Center" · PUSHED+DEPLOYED `85058e5` (10-Jul ~00:3x IST)

**Rama rejected v1 (`e1faf29`, below) as "incremental polish of the existing dashboard, not the
Mission Control Center."** Full visual rebuild to match `gui/02.Dashboard.png` (studied the actual
PNG this time). Backend/routes/APIs/data-bindings **untouched** — every value derives from existing
endpoints (KPI counts from `/api/pipeline` stages + `/api/dashboard` counters + `/api/strategies`;
capacity/pnl/alerts as before).

## Rebuild ships (`dashboard.html` fully rewritten + large new `.dash-page` CSS block)
- **Today's Trading Summary** — 12 KPI cards (`.kc` in `.kpi-deck`, 12→6→4→3→2): Signals
  Received/Accepted/Rejected, Orders Created/Filled, Open/Closed Trades, Wins, Losses, Win Rate,
  Profit Factor, Today's P&L. Each: inline-SVG icon (JS `DASH_ICONS`, x-html), colored top-rail +
  value by tone, %-of-base sublabel (computed client-side), P&L sparkline from `pnl.equity_curve`.
- **Signal → Trade Pipeline** — 13 `.pl-card` in one `.pl-rail`: colored top-rail per backend
  `stage.color`, big count, "Last: HH:MM:SS" from `stage.last_event`, `→` via `::after`; names
  2-line clamped so all 13 fit at 1600.
- **3-col ops row** (`.mc-3col` 3→2→1): Capacity (inline usage bar colored by tier via `capTier()`
  0-60/60-80/80-100, NOT the STATUS word; Usage% col; NEW tags; colored STATUS + legend) · Service
  Health table (dot + ACTIVE/INACTIVE badge + Last Update = probe `ist_now` for live, else "—"
  since `host_reader.all_units` has no per-unit ts) · Recent Events (category badge derived from
  `event_type` via `evCat()`).
- **Strategy Summary** compact (Total/Active/Quiet/Silent + Best/Worst + View-All).
- **Header slimmed** (base.html): dropped Received/Trades/Open/NetP&L (now in KPI deck); kept
  4 status pills + **Broker ID + Client Name** (`summary.client_name`→"--" until backend adds it) +
  emphasized blue Trading Date/Current Time. Sidebar `version 2.0.0`.

## Verification method (reuse for GUI screens with empty PC DB)
Scratchpad `serve_verify.py` gained a throwaway `/__demo` route: renders the REAL template + injects
a `window.fetch` override returning canned mock JSON — **must be `{ok:true,status:200,json:…}`**
(base.html `getJson` checks `r.ok`). Headless-Edge screenshot of `/__demo` = true production
render with data. Matched mockup at 1600; reflowed clean at 1280. **354/354 GUI tests.**
gui-dashboard active/NRestarts=0; `GET /`→302.

## Final polish pass (`30b907a`, 10-Jul ~01:1x) — deployed atop the rebuild
Rama's "make it pixel-close" list: (1) **tighter top** — summary-bar pad 10→6px + dashboard content
top pad 16→2px (≈ −22px whitespace; deck now starts right under the TRADER/MODE/KILL/PHASE strip);
(2) **type** KPI title 12→13 / value 26→28 / section 14→15 / pipeline count 22→24+name 10.5→11.5 /
strat stat 12→13+value 30→32 (card `min-height:108` unchanged so heights didn't grow); (3) **sidebar**
`.nv-item` .8→.85rem (labels stay single-line — .9rem wrapped "Scanner Attribution"); (4) **Broker ID
+ Client Name REAL from `config/accounts.csv`** — NEW read-only `config_reader.active_account(cfg,
session_account_id)` (prefers session acct → primary/enabled → first row; graceful {} if unreadable)
wired into `summary_bar` as `client_name`(=label)+`broker`; **VM-verified live: LFL836 → Kandasamy**;
(5) **width** dashboard `max-width` 1600→1800 + side pad 16→12 (fills 1080p/1200p, no gutters).
Backend/routes/APIs otherwise untouched (the CSV read is isolation-safe: reads by value, imports no
prod package; `config_dir` already in gui_config). NB PC dev can't resolve the roster — the PC's
`gui_config.local.yaml` points `config_dir` at the VM path; only the VM reads the real CSV. 354/354
tests; headless demo fills 1600 & 1920 with tighter top + larger type.

## Layout polish PASS 2 (`02ea2e4`, 10-Jul ~01:3x) — deployed
Rama round-3 list: (1) **header +10px** (summary-bar pad 6→9 + sb-item gap 2→4; measured 64→74px, less
compressed); (2) **content flush under header** (content top pad 2→0, first `section.mc-panel:first-of-type`
pad-top 15→6, `.dash-page .info-banner` compacted) — NB `:first-of-type` on `section` because the
info-banner `<div>` is the actual first child; (3) **width** max-width 1800→2100 + side pad 12→8 (fills
1080p/1200p); (4) **pipeline type** name 11.5→12.5 / count 24→26 / ts 10→11; (5) **Best/Worst name**
15→16.5; (6) **3-col ops row 45/25/30** (`grid-template-columns: 45fr 25fr 30fr`, Capacity/Health/Events
— matches mockup ~43/27/30, Capacity widest; "Events largest share" in the ask conflicts with the mockup so
followed the mockup). **KEY constraint learned:** content is already flush under the header (2px→0 gap), so
it CANNOT move up 20-30px as asked without a *shorter* header (conflicts with #1) — the live "too low"
effect was the alerts info-banner, now compacted. Used the `serve_verify.py` `/__demo` route + an added
measurement script (sets `document.title` to element rects, read via `--dump-dom --virtual-time-budget`) to
get exact px positions. CSS-only; 200 render OK; headless fills 1600 & 1920, no overflow. gui-dashboard
active/NRestarts=0.

## Final polish PASS 3 (`11388e6`, 10-Jul ~01:5x) — deployed
Rama round-4: (1) **content flush-LEFT** — `main.content:has(>.dash-page)` margin `0 auto`→`0`, left pad
8→4 (begins at sidebar edge; removes the centering left-gutter on wide monitors; max-width 2100 caps
stretch — equal margins only beyond that); (2) **~12px header gap** — content top pad 0→12 + removed the
`section.mc-panel:first-of-type` reclaim (status strip + first section were "merged"); measured panel top
74→86; (3) **pipeline stage names 12.5→13.5** (held card height: pl-card gap 6→5, pl-name min-height
2.3→2.24em). (4) **Broker ID BUG FIX (summary_bar.py):** the VM `session` row carries a *placeholder*
`account_id="default"`, and the header preferred the session value → showed Broker ID "default". Now
prefers the **roster-resolved** account_id: `account.get("account_id") or session.get("account_id")` where
`account = config_reader.active_account(cfg, session.account_id)` (matched row → is_primary fallback — the
same selection the engine's `core/account_registry.py AccountRegistry.primary()` uses). **Live-verified on
VM: Broker ID `LFL836`, Client `Kandasamy`** (fully dynamic, no hardcode). NB the active account is defined
by `is_primary=TRUE` in `config/accounts.csv` (the `.env` only holds per-account credential *var names* like
`ZERODHA_API_KEY_LFL836`), so "read from .env" == read the roster the engine keys off. No route/API/logic
change. 354/354 tests; headless fills 1600 & 1920 with 12px gap + flush-left + bigger pipeline names.

## Final polish PASS 4 (`640ac7a`, 10-Jul ~02:0x) — deployed [CSS-only]
Rama round-5: (1) ops row **45/25/30 → 46/29/25** (Capacity + Service Health wider, Recent Events
trimmed) + `white-space:nowrap` on `.cap-lim` and `.svc-name` so first-col labels ("Open Positions",
"Intraday Capital (₹)", "trading-watchman") stop wrapping to 2 lines; (2) `.dash-page .mc-3col`
`margin-bottom:16px` — Strategy Summary now has the standard section gap above it (was attached);
(3) `.summary-bar` right padding 16→40px — Date/Time/Logout group sits ~24px off the right edge.
**Screen-02 considered FROZEN pending Rama's review; next is Screen-03.**

---

# (v1 — SUPERSEDED by the rebuild above) Screen-02 redesign · `e1faf29` (10-Jul ~00:06 IST off-market)

Assets-library workflow cycle 2 (Rama's pipeline: screen-spec → asset-req-spec → [gen if
needed] → implement → verify → deploy → await live review; ONE screen at a time). Continuation
of a pre-shutdown WIP (PC lost power mid-verify); I reviewed the uncommitted state, finished
verification, fixed one layout bug, committed, deployed. [[gui_login_hero_asset_deploy_09jul]]

## What shipped (UI-only; routes/APIs/backend/data-bindings all untouched)
- **Header identity:** added Broker ID (`summary.account_id`) + Client Name (`"--"` — no backend
  field exists yet, verified absent from every read path) + Trading Date + Current Time; dropped
  the redundant sidebar IST clock item.
- **Sidebar brand:** reuse Screen-01 eagle mark, base64-inlined optimized WebP (`sb-brand-mark`);
  hidden at ≤900px (icon-only collapse). Identical branding app-wide.
- **Strategy panel:** removed Best/Worst cards + per-strategy chip strip → compact **Strategy
  Summary** (Total/Active/Quiet/Silent from the existing server-side `silence.color` tier in
  strategy_tower.py — no new backend field; plus Best/Worst P&L).
- **Capacity:** added Usage % column. **Pipeline:** stage age → absolute Last-event clock HH:MM:SS.
- **Layout:** max-width 1600, 16px card/grid gaps, 22px section spacing, 13px readability floor
  (all dashboard-scoped via `.dash-page`).

## The layout bug I found + fixed (the key deviation from pre-shutdown WIP)
Shared `.content` uses `margin:0 auto` inside the flex-column `.main-col`; on the cross axis that
auto-margin **overrides `align-items:stretch`**, so `.content` shrink-wraps to content width and
floats in a narrow centered band with big side gutters — exactly the "Screen-01 spacing issue"
the spec says to avoid. **This is PRE-EXISTING + APP-WIDE** (confirmed identical on untouched
`/strategies` + `/positions`). Fix: `main.content:has(> .dash-page) { width:100% }` — scoped via
`:has()` so it fills to max-width:1600 and only centers beyond 1600px, and **no other
not-yet-redesigned screen changes.**

## Verification
- **354/354 GUI tests** (in `ops_dashboard/.venv` — the lone system-Python "failure" is just the
  venv-isolation guard `test_c_venv_has_no_kiteconnect` detecting the wrong interpreter; passes in
  the correct venv). Templates are the only change; no Python touched.
- Headless-Edge render **clean at 1600 + 1280**: full-width, cards aligned, 16px gaps, no gutters.
- Deployed-file markers verified on VM; `gui-dashboard` active/NRestarts=0/clean log; `GET /`→302
  (up, auth-gating). Token-watcher untouched.

## Known / deferred (NOT in Screen-02 scope)
- **Mobile ≤~640px horizontal overflow** — PRE-EXISTING + app-wide (untouched `/positions`
  overflows identically); repo explicitly defers it (`/* mobile ... full pass is G4-adjacent */`).
  My new Strategy Summary grid correctly collapses to 1 column there. Left alone by design.
- Client Name renders `"--"` until a backend name field is added.

## Asset policy (reconfirmed): production ships ONLY the optimized derivative
`assets/branding/logos/algocore-mark.web.webp` (8 KB) committed; master PNG git-ignored
(`assets/**/*.png|jpg|jpeg`) + local-only. **Awaiting Rama live review before Screen 03.**
