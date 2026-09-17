---
name: mc8_investigation_16jul
description: M-C8 deeper read-only investigation (16-Jul) — the async hard_kill design CAN fire-and-return; shutdown/EXITING-blind is the
metadata: 
  node_type: memory
  type: project
  originSessionId: 20d49820-4aec-41c6-8377-564b6e4855d9
---

**16-Jul-2026 — M-C8 deeper READ-ONLY investigation (fixed nothing).** Report
`docs/audit/mc8_investigation_16jul2026.md`, docs-only `main`@**`63dbb38`** (UNPUSHED). Verified at
`main`@`f68d15d`; refs = `capital/kill_switch.py` unless stated. This is the evidence the async design
must be built on.

**⭐ STEER (Q1): NO — nothing in prod needs the `CancellationReport` synchronously ⇒ the async design CAN
FIRE-AND-RETURN (no future/poll/callback needed).** All 6 prod callers ignore the return:
`order_placer:1499`/`:3750` · `fund_manager:974`/`:2259` · `drift_handler:231` · `main.py:647`. No
assignment anywhere; `_run_cancel` has 1 caller (`:550`), `_exit_all_trades_indestructible` 1 prod caller
(`:821`).

**Q2 — the clean SEAM:** the 3 sync-contract tests (`test_kill_switch.py:321-374`) DO assert
`report.attempted/succeeded/failed`, **but they use the LEGACY `cancel_fn` path** (`_make_ks` passes no
adapter → `_run_cancel:824-846`). **Prod ALWAYS sets the adapter** (`main.py:1983`) → always takes
`_exit_all_trades_indestructible` (`:820-821`). The loop's own tests call it **directly**
(`test_hard_kill_flatten_chain:132`, `test_fix181:402/438`). ⇒ **dispatch ONLY the adapter path to a
worker + keep the method synchronous internally ⇒ every existing test passes unchanged.**

**🔴 Q3 — #1 HAZARD (latent even TODAY):** `_eod_self_exit_due` (`main.py:964-978`) is due iff
`count_active_positions()==0`, which counts **only OPEN/PARTIAL/PENDING_FILL** (`state_store.py:639-651`) —
**`EXITING` is BLIND** — and the flatten marks EXITING **early** (`_mark_trade_exiting:955-969`, called
`:1110`/`:1134`, before the retry loop confirms fills). ⇒ past 16:00 the **eod-self-exit daemon**
(`main.py:1062`, sets the event at `:1012-1035`) can fire **mid-flatten** → main wakes from
`_shutdown_event.wait()` (`main.py:3303`) → `_shutdown` (`:1099`) → **process exits with trades still in
the retry loop**. Sync-blocking only narrows this; `_shutdown` joins no flatten worker. **The async design
MUST: non-daemon worker + explicit join/drain in `_shutdown` (bounded by the 2h deadline) + a
flatten-in-progress gate — never rely on `count_active_positions()`.**

**Q4 — no join point:** a repeat `hard_kill` (already HARD_KILL → `do_publish=False`, `:535-540`) still
runs **`_run_cancel()` unconditionally at `:550`** = a SECOND full flatten; **no flag/handle/in-flight
marker exists**. Only partial guards: `_mark_trade_exiting` (EXITING removes it from the
OPEN/PARTIAL/PENDING_FILL re-select — comment `:958`) + broker-truth skip-if-flat. ⇒ **add single-flight**
(in-progress flag + worker handle) so a repeat joins/no-ops; re-specify KS6's "re-runs cancellation".

**Q5 — the new race:** on a worker the loop becomes CONCURRENT with the fill thread/reconciler (today it
runs ON them). Mutates `trades.status='EXITING'` (`:960-963`,`:1273-1277`), `orders.status='CANCELLED'`
(`:1012-1017`), broker `place_order` (`:1118`,`:1178`,`:1259`)/`cancel_order` (`:1004`), `_exit_alert_ts`
RMW (`:936-939`). **Main exposure = EXITING/order-status writes vs a late fill.** **No capital race** —
the loop never touches fund_manager (release deferred to CHECK1/`_check_stuck_exiting`,
`order_reconciler.py:3657`). **Safe-by-construction property:** every decision re-derives from **broker
truth** (`determine_close_direction` each retry `:1230-1246`; sweep `get_positions` `:1151`); DB writes are
explicitly best-effort ("Broker truth > DB truth", `:1279`).

**Q6 — invariants to preserve:** FIX-180 2h bound (`:65`,`:1201`,`:1207-1219`) + 5-min per-trade alert
dedup (`:67`,`:925-953`) + 5/15/45s backoff (`:1199`,`:1221-1226`) · FIX-181 no-early-return (`:1065-1069`)
+ broker sweep (`:1145-1195`) + H-5 own-product intent (`:1160-1168`) + marketable LIMIT (`:906-923`,
`:885-904`) · FIX-190 Bug A reverse-aware/skip-if-flat (`:1102-1111`) + Bug E cancel resting exits
(`:971-1025`) · H-4 re-derive from current broker net every retry (`:1230-1246`).

**Why:** the async move is the riskiest change in the cluster; its shape hinged on Q1 (fire-and-return? →
YES) and Q3 (what keeps the process alive? → nothing, and EXITING is blind).
**How to apply:** Web Claude designs the M-C8 async fix from these six answers → ChatGPT red-team →
implement (parity paper+live, one commit, off-market deploy). **M-C4 is DONE** ([[mc4-killswitch-lock-16jul]]);
M-C5 mitigated, M-C6 latent. [[mc-cluster-investigation-16jul]] [[unpushed-pending-deploy-ledger]]
