---
name: delivery-carry-blocks-shutdown-05aug
description: "A held delivery position stops the service ever shutting down, which removes the census, the 08:15 boot, and the kill auto-clear"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6c0766d2-5020-475a-acf9-0404853b0fbc
  modified: 2026-08-25T04:42:57.380Z
---

**MEASURED 05-Aug-2026 17:49 IST, the first night a CNC position was carried.**

## The chain, each link measured

1. **(P)** `17:35:00.002 WARNING main: "eod_self_exit: past 17:35 IST but 1 active
   position(s) remain — staying up to manage them; will exit once flat."` Telegram
   `[LIVE] EOD shutdown deferred` DELIVERED. At 17:49 `ActiveState=active`,
   `ExecMainStartTimestamp=08:15:05` — never exited.
2. **(S)** `_eod_self_exit_due` (`main.py:1073-1113`) is due **only** when active
   positions (`OPEN`/`PARTIAL`/`PENDING_FILL`) is **zero**. A carried delivery position
   is `OPEN` by design ⇒ **the self-exit is unreachable for as long as it is held.**
3. **(S)** `emit_census()` runs at `_shutdown()` entry (`main.py:1319`,
   `core/effect_telemetry.py:33`). ⇒ ⛔ **NO SHUTDOWN, NO CENSUS.**
   **(P)** 0 `effect_census` and 0 case-insensitive `census` in 93,833 lines — against
   **8,204** hits for `effect` as the control that makes the zero interpretable.
4. **(S)** `deploy/token_watcher.sh` first branch:
   `if [ "$active_state" = "active" ] || [ "$active_state" = "activating" ]; then
   clear_alert_flags  # running -- nothing to do`. Every restart path it owns keys on
   the **last exit code**; a service that never exits has none.
   ⇒ ⛔ **NO 08:15 BOOT.**
5. **(S)** `clear_stale_state` and `auto_clear_scheduled_kill` have **exactly one
   non-test call site each** — `main.py:1914` and `:1919`, **both in the boot path**.
   No date-rollover handler exists in `main.py`/`core/`/`capital/`/`orders/`
   *(name-based grep — width stated)*. ⇒ ⛔ **THE DAY'S SOFT_KILL NEVER AUTO-CLEARS.**

## What it costs

- ⛔ **The census is gone on exactly the days delivery is held** — and it is the only
  source separating *"`cnc_gtt_monitor` observed the trigger"* from *"a cleanup swept
  the row"*. `gtt_state` reads `CLEANED` and answers neither. Structurally
  unavailable, not merely late. See [[census-not-in-journalctl-05aug]].
- 🔴 **The 15:15 breaker's SOFT_KILL persists into the next day** with no in-system path
  to clear it. ~~**(I)** — never observed; this state has never existed before.~~
  ✅ **UPGRADED (P)+(S) 06-Aug 19:2x — AND IT COSTS A TRADING DAY, not just tidiness.**
  **(P)** the breaker fired `15:15:01.115` (`circuit_breaker_force_close_15:15`,
  `order_monitor`); **(P)** `kill_switch_state` id=1 was still `SOFT_KILL` at 19:2x;
  **(P)** service `active` at 19:08:44, past the 17:35 self-exit. ⇒ **no boot ⇒ the next
  trading day opens in SOFT_KILL ⇒ NO NEW ENTRIES ALL DAY.**
  ⭐⭐ **The mechanism was OBSERVED IN PRODUCTION, not inferred:** today's own
  `08:15:02.876` line — *"Kill switch auto-cleared: prior SOFT_KILL from **2026-08-05**
  (reason=`circuit_breaker_force_close_15:15` by=order_monitor) — new day starts clean
  (HEADLESS)"* — **the same event, byte-identical reason, one day earlier.**
  ⭐ **And it clears WITH POSITIONS OPEN:** ATULAUTO was `OPEN` at 08:15:02.876 and the
  prior-day kill cleared anyway — `clear_stale_state` ignores open positions; the
  no-open-positions condition belongs to `auto_clear_scheduled_kill`, the **same-day**
  path. ⇒ ⛔ **"we hold positions so it wouldn't clear anyway" is REFUTED.**
- ⛔ **Every alarm emitter stays alive all night.** See the drift loop in
  [[capital-drift-is-operand-mismatch-05aug]].

## ⛔ The obvious remedy is NOT safe — do not default to it

A manual `systemctl restart` the next morning **would** clear the kill
(`clear_stale_state` treats it as prior-day). ⛔ **But T+1 moves the stock from
`positions()` to holdings, and `reconcile_positions` is blind to delivery T+1** —
`MISSING_AT_BROKER` has never fired and *could not* until a delivery trade was OPEN in
the live DB. One now is. **Both branches carry a first-ever path.**
⇒ **Rama's ruling, with the trade-off in front of it. Never a default.**
See [[reconcile-positions-blind-t1-30jul]].

Record: `docs/audit/HANDOFF_05-Aug-EVENING.md` §10.

---

## 🔴 F6 FOUND THE MECHANISM — 25-Aug-2026. ⛔ IT IS **NOT** GTT FRAGILITY.
🔬 Measured at deployed HEAD `195436bb…` (tree drift 0):
`_eod_self_exit_due` (`main.py:1074-1113`) gates **the entire process** on
`store.count_active_positions()` (`main.py:1109`) — the **PRODUCT-BLIND** count.

▎ carried CNC ⇒ no self-exit ⇒ service still `active` at 08:15 ⇒ `token_watcher`
▎ reads *"running — nothing to do"* ⇒ **NO BOOT** ⇒ the 15:15 `SOFT_KILL` never
▎ auto-clears ⇒ 🔴 **the next day takes NO ENTRIES — in BOTH pipelines.**

⇒ 🔴 **THE COUPLING RUNS DELIVERY → WHOLE SERVICE → MIS.** ⭐ A delivery carry can
**silently disable the INTRADAY pipeline the following day.** 🏷️ Recorded as an
**ARCHITECTURE DEFECT**, ⛔ not an operational inconvenience.

⭐ **SO THE MANUAL STOP'S MEANING IS NOW KNOWN:** it compensates for the EOD gate's
**product-blindness**, ⛔ NOT for any GTT fragility — 📄 delivery protection is a
broker-side OCO that rests at Zerodha (`orders/cnc_gtt.py:2-7`) and GTT *repair* is
already in-hours-only (`orders/order_reconciler.py:674-675`). ⇒ ⭐ **what would retire
the safeguard is a pipeline-aware EOD gate**, ⛔ nothing about GTTs.
👤 It stays labelled **LEGACY SAFEGUARD** until that lands.

⭐ **AND IT IS SEPARABLE FROM F2 (measured 25-Aug):** `product` is derivable today via
`orders LEFT JOIN … leg='ENTRY'`, and the NULL-product hazard is **confined to
REJECTED (80/80) and FAILED (68/345)** — **0 NULLs** in `OPEN`/`PARTIAL`/`PENDING_FILL`,
the exact statuses the gate reads. ⚠️ ⛔ But any pipeline-scoped count MUST be
**fail-CLOSED** (NULL ⇒ unknown ⇒ stay up), and ⛔ must NOT change
`count_active_positions()` itself — it also feeds the `risk_engine` OPEN_POSITIONS cap
(`capital/risk_engine.py:303`) and the portfolio allocator (`main.py:3207`).
📄 `docs/audit/F6_LIFECYCLE_25-Aug-2026.md` · `docs/audit/F2_SCOPING_Q1_25-Aug-2026.md`.
