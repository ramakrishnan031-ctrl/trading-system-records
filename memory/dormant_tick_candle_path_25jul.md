---
name: dormant-tick-candle-path-25jul
description: "🔒 DECIDED 25-Jul: the live tick→candle feed STAYS DORMANT — a decision with a reopen trigger, not a backlog item. Root cause was NEVER WIRED (32 connects, 0 tokens, 0 ticks ever). ShadowTracker (which fabricated 141 rows of zeros) is now DISABLED; FIX-029's health check un-gated. Reopen ONLY on a live safety dependency or post-M-S4 exits re-derivation."
metadata:
  node_type: memory
  type: project
  originSessionId: d1e7bd64-5bf1-4dff-b36a-00be10f2dfe0
  modified: 2026-07-25T14:02:46.489Z
---

**Discovered 25-Jul proving M-D1 inert; ROOT CAUSE RESOLVED batch 3; DECIDED batch 5.**
Full report: `docs/audit/tick_candle_dormancy_25jul2026.md`.

## 🔒 THE DECISION (25-Jul, Rama + ChatGPT agreed) — LEAVE IT DORMANT
⛔ **NOT "we never got to it". A decision, with reasoning and a TRIGGER — same discipline
as the exits closure.** FOUR LEGS:
1. **The 15:40 historical 1-min fetch covers every ANALYTICAL need and carries TRUE DELTA
   volume**; the tick path under MODE_LTP carries **no** `volume_traded` ⇒ wiring it gives
   strictly **WORSE** data.
2. **Four of five starved consumers are blocked INDEPENDENTLY anyway** — `smart_tgt` (never
   registered), `StructureExitManager` (flag-off, deliberate), `BreakevenManager` (never
   constructed) ⇒ a subscription alone lights up **none** of them.
3. **The fifth (`ShadowTracker`) is now DISABLED** (`d31759f`).
4. ⭐ **Every feature it would serve is an EXIT feature, and the exits thread is CLOSED on
   measured numbers** (8 policies / 115 trades / real costs; best −0.076R vs current
   −0.100R; none profitable).

**⭐⭐ REOPEN TRIGGER — revisit ONLY if:** **(a)** a **live SAFETY dependency on ticks** is
identified — **none exists today**: the broker-side SL is independent of the feed; the
tick-age watchdog and H-9 guard are the feed's *own* health checks, not position protection;
and ⭐ **the one genuine safety casualty — FIX-029's consumer-thread death detector — was
UN-GATED 25-Jul (B1) and no longer depends on ticks at all**; **or (b)** the **entry work
materially changes and the exits are re-derived post-M-S4** (the exits closure's own
trigger). **Any earlier reopen is a mistake.**
**⭐ `_persist_candle` should stay dark EVEN IF the feed is ever wired** — it is fully
redundant and would add a second, worse-quality writer to `analytics.candles`.

## 1. WHY nothing subscribes — **NEVER WIRED** (not removed, not gated off)
`git log -S "subscribe([" --all -- '*.py'` = **3 commits, all accounted for**: `bcf03b5`
(initial foundation — *defines* it), `de22a04` (BL-11 `ws.subscribe` inside `_on_connect`,
re-subscribe only), `91ab56a` (FIX-061 → `order_placer.py:3393`, the only caller, one token,
exit-retry). **No commit ever added a boot-path subscription, so none removed one.**
⛔ `config_loader.py:1259` says *"nothing subscribes to the candle feed"* and looks like a
deliberate global switch at grep-level — **it is NOT**; it is scoped to `StructureExitConfig`
(when its flag is off, *that manager* doesn't subscribe). Premise checked and rejected.

**MEASURED (VM logs, all history):** `connected to KiteTicker` = **32** ·
`exit_retry_subscribed_to_ltp` = **0** · `re-subscribing to N tokens` = **0** ⇒
**the socket has connected 32 times and never carried a single token. Zero ticks, ever.**

Everything downstream IS wired and correct: `_tick_dispatcher` registered (`main.py:2547`),
`_persist_candle` registered (`:3391`), `candle_store.start()` (`:3373`), token map injected
(`:3393`). **One missing call.** With `_subscribed` empty, `_on_connect` hits
`if not tokens: return` (`live_feed.py:333`).

## 2. WHAT it breaks — 5 consumers, and ⭐ one FABRICATES data
`_persist_candle` (0 rows ever) · `smart_tgt._on_candle_close` · `StructureExitManager`
(flag-off anyway) · `BreakevenManager` (never constructed anyway) · **`ShadowTracker.on_tick`
— blocked ONLY by this.** Plus `get_candles()` → always `[]` (`smart_tgt:796`).

**⭐ ShadowTracker is the real damage — it writes confident zeros, not nothing.** MEASURED:
141 simulated innings; **exit_reason SL=0, TGT=0, EOD=130, NULL=11**; **exit_price ==
entry_price on 130/130** with **avg pnl_pct 0.0** (real innings: 1/181 and 180 non-zero);
`inning_number` = **{2: 141}, zero inning-3 ever** (cascade needs `SL`/`TGT`, `:398`). Real
innings look healthy only because inning 1 copies the **trade record** (`:343-351`), not ticks.
EOD close prices at `_last_price.get(sym, entry_price)` (`:445`) and `_last_price` is
tick-fed ⇒ every close fell back to entry. **`enabled: true`.** A silent no-op is obvious;
this looks alive and answers nothing.

## 3. ⚠️ THREE WATCHDOGS DISARMED BY IT (one protects an unrelated thread)
- **H-9 starvation guard** (`candle_store.py:294-308`): `if to_close: … elif synthetic_candidates: warn`
  — under **total** dormancy both are empty ⇒ **neither branch runs**. Structurally blind to
  never-started; only catches ticks-that-stop. 0 firings / 32 boots.
- **Tick-age watchdog** (`live_feed.py:695-699`) pre-arms on `_last_tick_at is not None` ⇒
  **never leaves the pre-arm loop.** Started 32, armed 0.
- **⭐ FIX-029 consumer-thread health check** is called *inside* that never-entered loop
  (`:707`) ⇒ **the consumer-thread death detector has never run in production.**
⚠️ `system_security_audit_02jul2026.md:187` asserts "auto-reconnect + re-subscribe + tick-age
watchdog" resilience — **all three legs are vacuous.** Correct that claim.

## 4. ⭐ NOT the same root as the trail never firing — INDEPENDENT, each sufficient
**Cause A (24-Jul):** nothing is ever *registered* — `order_placer.py:949`
`order_protocol = self._default_protocol` set unconditionally ("OP9: choose protocol", no
choosing) discards the 13/16 `CO_PLUS_TGT` strategies; registration `:2192` gated on
`== "CO_PLUS_TGT"`. MEASURED `smart_tgt_state` = **0 rows**.
**Cause B (this):** no candle event ever *arrives*.
Different files, different provenance, **neither causes the other; fixing either alone still
yields 0 trails.** Shared *pattern* (built-and-never-wired), not a shared root.
⇒ **"wire the trail" is a THREE-fix job** (+ `BreakevenManager` never constructed).
Does NOT reopen the exits thread (post-M-S4 trigger stands) — it corrects the **cost estimate**
feeding Rama's 5A. [[trailing-stop-never-fired-24jul]]

## 5. Is the historical API an adequate substitute? **YES for analysis, NO for live**
`fetch_daily_candles` = cron **15:40**, post-close, `interval="minute"`, traded symbols +
index universe; 275,129 rows / 482 symbols / 19-Jun→24-Jul, **true DELTA volume**. ⇒
`_persist_candle`'s dormancy is **HARMLESS and re-enabling it would add a worse writer**
(MODE_LTP carries no `volume_traded` ⇒ 0). But it runs **once, after the close**, only for
symbols that **already traded** ⇒ cannot trail a stop at 11:20 or close an inning at 13:45.
**Named gap: intraday 1-min OHLC for currently-held symbols, in-session.** Nothing provides it.

## 6. Cost of subscribing (SIZED, NOT CHANGED)
Need is **~5–20 tokens** (`max_open_positions: 5` + active innings), **not** the 2,228 in
`token_map()`. ~0.5% of one connection (Kite: 3,000/conn, 3 conns — *external, re-verify*).
Bandwidth/rate limits are **not** the constraint; batching exists (FIX-059, 50/call).
**Use MODE_LTP** — sufficient (OHLC is built from LTP by construction; `_check_hit` compares
LTP). ⛔ **MODE_FULL would ACTIVATE M-D1's corruption** (`volume_traded` is cumulative and
`_Accumulator.update` sums it per tick) — fix M-D1 *first* if ever flipping.
⚠️ **Two hazards for whoever fixes it:** (1) **synthetic candles are sticky** — one real tick
gives a token `_history`, then a carry-forward candle fires **every 60 s for the rest of the
process even after unsubscribe** (no eviction but `gc_sweep`/`MAX_HISTORY`), each fanning to
every callback incl. a DB insert; (2) the H-9 guard **flips from silent to loud** on the first
tick — expect a burst of "ZERO real ticks" for quiet illiquid names; that is it working.

## ✅ ACTED 25-Jul batch 4 (P1-P5 all discharged)
- **P1 ShadowTracker — BUILT + HELD.** `shadow_tracker.enabled: false` committed on branch
  **`hold-shadowtracker-disable-25jul` @ `0c74860`, NOT pushed — awaits Rama's "off"**;
  ship = one cherry-pick. **CONFIG ONLY, component left intact** (correct the day ticks flow).
  ⭐ **A2 proven by EXECUTION, not by reading guards:** with `enabled=False`, driving
  `on_tick` + `_on_position_closed` + `_on_eod_complete` gives **`insert_inning`=0,
  `update_inning_close`=0**. All 3 write sites (`:384`/`:510`/`:555`) sit behind one of 4
  guarded entry points (`:209`/`:224`/`:269`/`:422`). It still constructs + subscribes to the
  bus (`:190-191` unconditional) — handlers no-op. **No half-disabled writer.**
  ⭐ **A4 — nothing real is lost, MEASURED:** `daily_report.py:646`'s `max_favorable` loop is
  a **no-op — 309/309 innings have `exit_price` EXACTLY equal to the trade's exit price, 0
  exceeding** (a simulated inning starts at `prev_inning.exit_price`, `:475`) ⇒ the 16:05
  report is **byte-identical** without innings. GUI `inning_no` is already always NULL
  (innings exist only post-close; that query filters `_OPEN_STATES`). The count tile just
  stops growing. Nothing in `innings` is absent from `trades`.
  ⛔ **A3 — the 141 rows are VOID and MARKED IN SYSTEM_MAP, NOT DELETED.** Exact predicate:
  `is_real=0`, **141 rows, id 4..321, entry_ts 2026-06-17T10:00:53 → 2026-07-24T13:56:20**,
  all `inning_number=2`, 141 distinct trades, EOD=130/NULL=11. **Future `is_real=0` rows
  written after ticks flow are VALID — the void set is date-bounded.**
- ✅ **P2/B1 FIXED + pushed — FIX-029's consumer-thread death detector never ran in prod.**
  `_watchdog_loop` had a pre-arm loop spinning on `_last_tick_at is not None` with
  `_check_consumer_health()` in the loop *after* it. Collapsed to ONE loop; the health check
  now runs every interval **ahead of** the arming gate. RED-first 1-of-6. PARITY: paper starts
  no consumer thread and no watchdog. No new alerts (no-ops when healthy/not-started).
- ⛔ **B2 REPORTED, DELIBERATELY NOT ARMED.** Tick-age watchdog + H-9 guard are silent because
  there are no ticks — **correct** for this state; arming them now alarms every interval of
  every day. **RIGHT SHAPE: arm on "a subscription exists" (`_subscribed` non-empty), not on
  connect and not on first tick.** Pinned by tests so neither can be armed silently.
- ✅ **P3** the 02-Jul security-audit resilience claim corrected **in place**, struck-through
  but legible (all 4 legs vacuous; the "broker SL still protects" clause is unaffected).
- ✅ **P4/P5** trail = 3 fixes + the MODE_FULL ordering trap + synthetic stickiness — all
  recorded in SYSTEM_MAP (C2-C5).

## 🆕 Found while taking BASE — a WALL-CLOCK TIME-BOMB TEST (recorded, not fixed)
`tests/unit/test_interactive_startup.py::test_holiday_guard_missing_yaml_proceeds` calls
`main()` without mocking the service-window guard, so after the **18:15
`SERVICE_START_CUTOFF`** (widened 25-Jul `570b3e8`) `main()` returns 0 at the window check
instead of reaching the config load it asserts on. **Passes before 18:15, fails after** —
MEASURED both ways on identical code (BASE 17:35 = 32F; BASE 18:20 = 34F).
⚠️ **An EVENING regression therefore shows 33-34 failures, not 32 — do NOT misread as a code
regression.** Sibling of [[feedback-no-fixed-test-baseline]].

[[ma2-ms3-md1-25jul]] [[trailing-stop-never-fired-24jul]] [[silent-failure-gaps-25jul]]
