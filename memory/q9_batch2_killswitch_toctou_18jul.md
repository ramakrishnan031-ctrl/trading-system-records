---
name: q9-batch2-killswitch-toctou-18jul
description: "18-Jul Q9 batch 2 DONE+DEPLOYED — the kill switch's last-mile re-check (A-3, the TOCTOU guard before broker dispatch) is now WIRED-proven: pos+neg, gate-order verified, no capital leak, parity structural, bite-proven. §A verdict: the 2%/5% daily-loss split is FIXTURE-ONLY (production is one key at 3%)."
metadata: 
  node_type: memory
  type: project
  originSessionId: b9e84959-b70c-4ce6-9521-3db6f6dd3fee
---

**🛑✅🚀 Q9 BATCH 2 — THE KILL SWITCH'S LAST-MILE RE-CHECK IS WIRED-PROVEN. DONE + DEPLOYED 18-Jul-2026.**
Report `docs/audit/q9_batch2_killswitch_toctou_18jul2026.md`. Tag **`deploy-18jul-q9-batch2`→`4176c3f`**;
PC == VM bare == tag. **TEST-ONLY — zero production files; no runtime behaviour change.**
**No STOP-branch triggered (§A2/§B1c/§B5/§B6 all clean) — but each was checked against evidence.**

## §A VERDICT — the 2%/5% daily-loss split is **FIXTURE-ONLY. No action.**
Both halves get the **SAME key** in production: FundManager ← `app_config.system.risk.daily_loss_limit_pct`
(`main.py:2231`); RiskEngine ← `risk_cfg.daily_loss_limit_pct` (`main.py:2369`); and
**`risk_cfg = app_config.system.risk`** (`main.py:2357`). Production value **`daily_loss_limit_pct: 0.03`**
— *"SOLE daily-loss authority (3% of capital), PERMANENT"* (`system_config.yaml:193`). Neither half falls
back to a hard-coded default. **⇒ live fires BOTH halves off ONE key at 3%; the 2%/5% divergence exists only
in the integration fixture's constructor literals (`conftest.py:235` / `:257`). The recorded single-source
principle HOLDS.** **What the breach DOES:** `_make_daily_loss_cb` (`main.py:757-800`) = CRITICAL log →
notify → EOD `fire_now` (closes positions) → **`kill_switch.soft_kill`** ⇒ **it HALTS, not notify-only.**
⚠️ Note for whoever next edits the fixture: the split is convenient for testing (batch 1 used it for a clean
negative case) but does NOT mirror production — never infer production semantics from it.

## §B — the TOCTOU window, MAPPED IN REAL CODE (not assumed)
**Check sites in execution order:** webhook `webhook_receiver.py:512` → signal_processor `:684` (+`:1149`
`:1749` `:1915` `:2081` `:2201`) → RE5 `risk_engine.py:270` → **OP-LM1 `order_placer.py:1004`** →
**A-3 `order_placer.py:1289` = THE TRUE LAST MILE** (immediately before `self._engine.execute(...)`, INSIDE
the retry loop so a kill during a 429 backoff is caught, raised OUTSIDE the `try` so the loop's own
`OrderRejectedError` handler can't catch-and-retry).
**⭐ THE TWO RAISE DIFFERENT MESSAGES — this is the whole proof technique:** OP-LM1 →
`kill_switch_active_last_mile`; A-3 → `kill_switch_active_last_mile_presubmit`. Asserting `_presubmit`
proves the LAST-MILE check fired and NOT the earlier one (the batch-1 lesson: prove you exercised the
INTENDED gate). **No multi-way accepts anywhere.**

**⚠️ THE ARMING SEAM WAS PROBED, NOT ASSUMED — and the obvious candidate was WRONG.** `_fetch_ltp` appears
in the window in source order but **is never called on the paper path** (probe: `_fetch_ltp CALLED 0 times`)
⇒ unusable. The call that DOES execute strictly between the two checks is
**`self._om.update_trade_status(trade_id, "PENDING")` (`order_placer.py:1016`)**. A **delegating** wrapper
arms a soft kill on that transition then calls through (path unchanged apart from the arming), and the test
asserts the seam actually fired ⇒ cannot pass vacuously.

**POSITIVE:** nothing reached the broker — asserted against a delegating spy on **`adapter.place_order`**
(the real boundary), corroborated by zero `ENTRY` rows in `orders`. **NEGATIVE:** the same signal with the
kill CLEAR does reach the broker (distinguishes a working re-check from one that blocks everything).
**DISTINGUISHER:** arming BEFORE `place()` is caught by **OP-LM1** (no `presubmit`) ⇒ the two sites are
genuinely distinct, which is what makes the positive test's `_presubmit` assertion meaningful.

**§B1e semantics:** `is_active("entry")` = SOFT **or** HARD; `is_active("exit")` = **HARD only** (a soft kill
must still allow exits). Both last-mile checks use `"entry"` ⇒ block entries under either kill, never block
an exit under a soft kill — the correct asymmetry.
**§B1f no masking:** the kill is armed INSIDE `place()`, so webhook / signal-processor / RE5 have all already
passed — reaching `place()` at all is the proof.

## §B5 — ORPHAN RESERVATION: **NO LEAK** (asserted)
After a last-mile block, `intraday_reserved` + `intraday_avail` return to their pre-signal values,
`intraday_used` unchanged, realized P&L unmoved. Mechanism: `_handle_placement_failure` →
`self._fm.release(reservation_id, …)` — the same path OP-LM1 uses. (Had this failed it would have been a
live capital finding: margin stranded on every kill until restart/reconciliation.)

## §B6 — PARITY: **SHARED check, structurally upstream of the mode branch**
`order_placer.place()` has **no paper/live branch** between the checks and dispatch (`self._mode` appears
only in alert titles `:691/:710/:964/:1130`); the divergence lives DOWNSTREAM in
`broker/zerodha_adapter.py` (`paper_mode` → `_paper_place_order`, `:348`, ZA10). **⇒ one shared check, no
second copy to drift** — which is exactly what caused the P1 `/health` bug elsewhere. Proving the block in
paper proves it for live.

## §B7 — ⭐ PROVEN TO BITE
Neutering A-3 ⇒ **`assert ['RELIANCE'] == []`** — *"AN ORDER REACHED THE BROKER AFTER THE KILL WAS ARMED
MID-FLIGHT … the last-mile re-check did not hold"*. Restored ⇒ 3 passed; `orders/` + `capital/` 0 modified.
**⭐ Assertion ORDER is deliberate: the broker record is asserted BEFORE the exception**, so a broken
re-check fails with *"an order reached the broker"* instead of the useless `DID NOT RAISE` (an earlier draft
did exactly that and was restructured). The break is meaningful because OP-LM1 cannot cover for it — the
kill is armed AFTER OP-LM1 already passed.

## Q9 coverage matrix — kill-switch row (§B8)
**WIRED** (was UNIT-ONLY) · positive ✅ · negative ✅ · planted-break ✅ · **gate-order verified** ✅
(`_presubmit` proves A-3 not OP-LM1) · **production path verified** ✅ (shared check upstream of the mode
branch). *Back-filling these fields for the OTHER layers is a separate later item — NOT done.*

## Remaining Q9 queue
**(C) the CAPITAL INVARIANT integration test** (`Starting Capital − Realized Loss − Charges − Reserved +
Released == Expected Available` at EVERY lifecycle stage — **the E4/W10-class catcher**, and the one I'd do
next) · **#4 sizing floors/caps** (min-lot · M-C6 zero-multiplier SKIP · `max_position_value` · tier
multiplier — batchable) · **#5 post-restart capital restoration** · back-fill the coverage-matrix metadata
for the remaining layers.
**Explicitly NOT this batch (separate, larger):** HARD-kill order cancellation + flatten-worker verification
— the first LIVE hard kill is its real test.

## Board carried forward (unchanged)
**RAMA DECISIONS:** E4/W10 risk-posture sign-off · `cleanup.py` live-reset as a `scripts/` operator tool? ·
security-watcher systemd-timer hygiene (offered, NOT applied — refused as not-a-bug: a documented 60s
heartbeat) · D1–D4 · the regime strategic choice · **FREEZE `min_pass_score` while measuring**.
**RAMA ACTIONS:** **Kite token refresh (blocks Q10 Part B)** · rotate the Telegram token · 2FA seed VM-only ·
offsite backup · rpcbind · SSH→Tailscale · `require_hmac` (safe to flip now) · arm `pre-receive`?
**⚠️ MONDAY 20-Jul 08:15 = the FIRST REAL BOOT after the S4 fix — WATCH IT**; the strategy-registry officer's
first live run is **Mon 16:22**. **The 6 destructive CTs are UNBLOCKED but NOT RUN.**

Related: [[q9-batch1-daily-loss-wired-18jul]] · [[q9-money-path-coverage-18jul]] ·
[[dual-daily-loss-mechanism]] · [[ct-guard-invariant-18jul]].
