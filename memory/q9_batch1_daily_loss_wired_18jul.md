---
name: q9-batch1-daily-loss-wired-18jul
description: "18-Jul Q9 batch 1 DONE+DEPLOYED — the daily loss limit is now WIRED-proven (both halves, positive+negative, planted-break proven). Tightening the 9-way assertions exposed that neither test ever exercised the global max_open_positions gate; fixed. Records the STANDING Q9 RULES A-E."
metadata: 
  node_type: memory
  type: project
  originSessionId: b9e84959-b70c-4ce6-9521-3db6f6dd3fee
---

**💰✅🚀 Q9 BATCH 1 — THE DAILY LOSS LIMIT IS WIRED-PROVEN. DONE + DEPLOYED 18-Jul-2026.**
Report `docs/audit/q9_batch1_daily_loss_wired_18jul2026.md`. Tag **`deploy-18jul-q9-batch1`→`92d3c71`**;
PC == VM bare == tag. **TEST-ONLY — zero production files; no runtime behaviour change.**

## ITEM 1 — daily loss limit, wired (Q9's #1 gap, closed)
`tests/integration/test_q9_daily_loss_limit_wired.py` on the existing `wired_system` fixture drives
**3 REAL losing round-trips** (reserve→place→ENTRY fill→SL fill→close) until the limit is crossed.
**BOTH halves, each POSITIVE + NEGATIVE:** post-close breach (`fund_manager.py:1279-1290`) must NOT fire
below 2% / must dispatch `on_daily_loss_breach` above it; pre-trade RE7 (`risk_engine.py:598-604`) must NOT
cite DAILY_LOSS below 5% / must reject **`REJECTED_DAILY_LOSS` specifically** above it.

**⭐ ASSERTIONS ARE RELATIONSHIP-BASED, NEVER LITERAL — and this is load-bearing.** The reader's contract is
**mid-migration**: today `get_daily_realized_net_pnl` = `SUM(pnl_delta) - SUM(costs)`; **E4/W10 changes it to
`SUM(pnl_delta)`**. A literal ₹ figure would bake in today's double-subtracting behaviour and break when that
branch lands; an assertion on TRUE net loss would be wrong today (the current reader OVER-states the loss ⇒
fires EARLIER). So: *"whatever the reader returns, once it is ≤ −(pct × total) the next signal is
REJECTED_DAILY_LOSS; above that, DAILY_LOSS is not the reason."* Correct under BOTH contracts.
**Q9 proves the layer is WIRED; E4/W10 fixes whether the NUMBER is right. Do not conflate them.**

**⚠️ TWO SUBTLETIES the scenario had to respect (both nearly caused a pass-for-the-wrong-reason):**
1. **Gate order:** RE5 = `… DAILY_TRADES, CONSECUTIVE_LOSSES, DAILY_LOSS …` and the fixture allows 4 ⇒ the
   limit MUST be crossed in **≤3 closes** or CONSECUTIVE_LOSSES fires first.
2. **The limit MOVES:** both halves use `pct × the CURRENT total`, which **shrinks as losses accrue** — the
   run enforced **23,642**, not the 25,000 a start-of-day figure implies. Re-derive at each check.
Every polarity assert is preceded by a **precondition assert on the reader** ⇒ cannot pass vacuously.

**⭐ PROVEN TO BITE (planted break in EACH half):** neutering `risk_engine.py:598` ⇒
*"PRE-TRADE GATE DID NOT FIRE: reader -27283.62 <= limit -23642.91 … terminated as 'PROCESSED'"*;
neutering `fund_manager.py:1281` ⇒ *"POST-CLOSE HALF DID NOT FIRE … callback was never called"*;
both restored ⇒ green, `capital/` 0 modified.

## ITEM 2 — ⭐ tightening the 9-way asserts EXPOSED A REAL MISMATCH
`test_risk_rejection_max_open_positions` (in BOTH integration files) accepted **any of 9** statuses.
Tightening it to `REJECTED_OPEN_POSITIONS` **failed** with `got 'REJECTED_STRATEGY_POSITION_LIMIT'`:
it seeded both OPEN positions on the **SAME strategy** as the incoming signal, tripping the **per-strategy
cap at `signals/signal_processor.py:624-640` — which runs BEFORE the risk engine is reached at all** (not part
of RE5). **⇒ the global `max_open_positions` gate was NEVER exercised**, and the 9-way accept hid it.
**Neither gate is broken** ⇒ test-quality finding, not a live capital finding (the §1 STOP clause did not apply).
**Fix:** `_seed_open_trades` takes a `strategy`; both tests seed `gap_go_long` ⇒ the incoming
`vwap_bounce_long` sits at 0/2 of its own cap while the GLOBAL cap is saturated ⇒ OPEN_POSITIONS fires.
**The global cap is now wired-proven — coverage that did not previously exist.** Bite-proven: neutering
`risk_engine.py:490` ⇒ both fail `got 'PROCESSED'`. Also fixed `test_full_signal_flow.py:9`'s docstring, which
advertised a **daily-loss scenario the suite never ran** — exactly how the gap survived review.

**Regression 11F/4939P, ZERO attributable** (4938+1); integration 33/33. Backup `pre_deploy_q9b1_20260718.db`
sound (`quick_check=ok`, v44, 361 trades). Schema v44, integrity ok, 0 FK. **The new test PASSES ON THE VM.**

## 📌 STANDING Q9 RULES (ChatGPT — apply to every future money-path test)
* **(A)** Every money-path integration test asserts **ledger / available / used / reserved / net+gross P&L /
  position state BEFORE *and* AFTER each transition.**
* **(B)** Every safety layer needs **BOTH** a positive (must fire) **and** a negative (must NOT fire) wired test.
* **(C) STILL TO BUILD — the CAPITAL INVARIANT integration test:** `Starting Capital − Realized Loss − Charges
  − Reserved + Released == Expected Available`, asserted at **EVERY** lifecycle stage. **This is the
  E4/W10-class catcher** (Q4 showed money writes are single-writer and column-correct ⇒ only an end-to-end
  VALUE assertion catches a contract bug).
* **(D)** Write assertions against the **logical NET contract / relationships**, never hard-coded figures.
* **(E) PERMANENT RULE: any NEW money-related safety feature is added to the Q9 coverage matrix IMMEDIATELY**,
  so no new seam appears.

## Remaining Q9 queue (later batches)
#3 **kill-switch last-mile re-check** (TOCTOU, `order_placer.py:1003`/`:1274` — an entry placed AFTER a kill) ·
**(C) the capital-invariant test** · #4 **sizing floors/caps** (min-lot · M-C6 zero-multiplier SKIP ·
`max_position_value` · tier multiplier — batchable) · #5 **post-restart capital restoration**.

## Board carried forward
**RAMA DECISIONS:** E4/W10 risk-posture sign-off · `cleanup.py` live-reset as a `scripts/` operator tool? ·
security-watcher systemd-timer hygiene (**offered, NOT applied — refused as not-a-bug with evidence: a
documented 60s heartbeat**) · D1–D4 · the regime strategic choice + **FREEZE `min_pass_score` while measuring**.
**RAMA ACTIONS:** **Kite token refresh (blocks Q10 Part B)** · rotate the Telegram token · 2FA seed VM-only ·
offsite backup target · rpcbind · SSH→Tailscale · `require_hmac` (safe to flip now) · arm `pre-receive`?
**⚠️ MONDAY 20-Jul 08:15 = the FIRST REAL BOOT after the S4 fix — WATCH IT** (the missing-direction alert also
first arms then); the strategy-registry officer's first live run is **Mon 16:22**.
**The 6 destructive CTs (CT114/127/130/132/133/135) are UNBLOCKED but NOT RUN** (separate deliberate step).

Related: [[q9-money-path-coverage-18jul]] · [[e4-w10-done-17jul]] · [[dual-daily-loss-mechanism]] ·
[[capital-operational-note]] · [[ct-guard-invariant-18jul]].
