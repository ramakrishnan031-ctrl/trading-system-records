---
name: f6-delivery-exit-abs-defect-06aug
description: "cnc_gtt_monitor.py:464 abs() breaks the T+1 delivery exit -- trade never closes AND a GTT spawns every cycle, from one line"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1be512bf-9d53-473e-960c-c17572bc2911
  modified: 2026-08-08T05:01:04.830Z
---

🔴 **`orders/cnc_gtt_monitor.py:464` — `held[sym] = held.get(sym, 0) + abs(int(qty))`.**
On a **T+1 exit** `holdings()` has *already* decremented, so adding the `−1` CNC `positions()` row **double-counts the sale** ⇒ `held = 1`.
**(P)** measured 06-Aug: `get_holdings → 0` at 09:31:55.600, F6 printed `held=1` **810 ms later**.

⭐⭐ **ONE LINE, BOTH SYMPTOMS.** `held == 0` (`:487`) is the **SOLE** door to `_finalize_gtt_exit`, which closes the trade **and** releases capital. Force it false and you get **a trade that never closes AND a new GTT every cycle**. ⛔ They are not two findings.

⛔ **DELETING `abs()` DOES NOT FIX IT** — the signed sum gives `held = −1`, still `!= 0`, still re-protects, and hands `_reprotect` a negative qty. Both the current expression and its obvious removal fail the same row.

⛔ **TWO branches read the same poisoned `held`:** F6 re-protect (triggered) **and** auto-recreate (`"GTT missing; holding intact"`). Fixing one fixes half a loop. ⇒ **a cancelled GTT is a missing GTT** — see [[do-not-cancel-system-gtt-06aug]].

⭐ **Reachable ONLY on a T+1 exit.** A same-day round trip nets `+1 −1 = 0` ⇒ `abs(0) = 0` ⇒ the clean door. That is why 05-Aug was clean and why this was the first sighting, not the first noticed.

**COST — the part that persists:** the reservation is stranded and **replayed at every 08:15 boot** (~21 % of the delivery bucket, daily, for a position that does not exist). ⛔ **NO supported closure path exists** — CHECK1 is blocked by the delivery skip, `_finalize_gtt_exit` by the `held` gate, EOD squareoff by CNC exemption. ⭐ The `gtt_state` row keeping CHECK1's skip armed **was created by the defect itself**.

🏷️ **`<BUILT 08-Aug-2026 · c39e799>` — ⛔ NOT DEPLOYED · NOT PUSHED · NOT VERIFIED LIVE.** Design: `docs/design/f6_delivery_exit_predicate_design_06aug2026.md`. Build record: `docs/audit/f6_build_08aug2026.md`.

## ✅ WHAT LANDED (local only — **the VM still runs the defect**)
**D-1** `max(0, int(qty))` — a same-day CNC row is a **DELTA**; only a LONG delta is unsettled shares. **D-2** `gtt_state.status='TRIGGERED'` written at **OBSERVATION** by a conditional `UPDATE … WHERE status='ACTIVE'` (exactly-once by SQLite, ⛔ not read-then-write), **keyed on the TRADE** — every re-protect mints a new gtt_id, so a per-row marker bounds nothing. **BOTH** consumers read it. **D-3** `RELEASE_USED` carries `reservation_id` (was 0/220) + a second release path (3 flat in-hours cycles).

⭐⭐ **THE 06-Aug BLOCKER *"D-2 ⇒ schema"* WAS WRONG — and precisely why matters:** §12.3.1 measured that `status` is written **by the handler, recording what it DID**, and correctly concluded such a marker cannot guard its own gate. ⛔ But that is a fact about the **WRITE DISCIPLINE, not the column.** Writing `TRIGGERED` at observation makes it record **what was SEEN**. ⇒ **NO DDL. Changing *when* a value is written is not a schema change.**

## 🔴 THREE SEAMS — each would have been LIVE
① **M2 would have SOFT-KILLED on the ordinary partial-fill path** (a re-protect leaves 1 TRIGGERED + 1 ACTIVE row; M2 rejects ">1 ACTIVE per trade") ⇒ scoped to ACTIVE. ② **CHECK1's delivery skip would have DISARMED MID-EXIT** — it read `get_active_gtt_states()`; both now share `get_reconcilable_gtt_states()`. ③ the orphan sweep would have read a TRIGGERED row as healthy protection.

⛔ **THE SECOND RELEASE PATH BOOKS NO PRICE AND NO P&L.** `_resolve_exit_price` rung 1 always misses for a stranded trade ⇒ it would book an unrelated live quote into the daily-loss reader and the expectancy corpus. ⭐ **A gap is a loss; a fabricated number is a CORRUPTION.** Capital is released (margin reverses from the persisted COMMIT row, priceless), `exit_price`/`net_pnl` stay **NULL**, `pnl_delta` is exactly 0.0, CRITICAL names the trade. ⇒ cost 5 is **not retired**, only not worsened.

🧪 **GATE:** `PYTEST_RC=1 · 9F/5582P/4S` — the 9 are the §8.12 baseline **line for line, zero new**; `5557+25=5582` reconciles exactly. **17 of 21 new tests go RED on the pre-fix code**; case 3 fails `['recreated:ATULAUTO'] != ['gtt_exit:ATULAUTO']`. ⛔ Run the gate **from Git Bash** — [[pc-test-env-hygiene]].

🔴 **§15.2's FIVE retirement criteria are ALL UNMET — every one needs an OBSERVED LIVE EVENING.** ⛔ **THE NIGHTLY MANUAL STOP IS STILL OWED, EVERY TRADING NIGHT.** Also [[release-used-has-no-reservation-id-06aug]].
