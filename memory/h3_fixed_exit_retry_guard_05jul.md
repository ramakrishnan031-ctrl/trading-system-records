---
name: h3-fixed-exit-retry-guard-05jul
description: Wave 1 H-3 FIXED — _retry_limit_triple_exits now re-reads state / skips existing-SL / 180s TTL (RAMCOIND + naked-reverse class). Read before M-O1 or any exit-retry / order_placer work.
metadata: 
  node_type: memory
  type: project
  originSessionId: 195d7581-8ffa-4581-941a-90abdcae8bb2
---

**Wave 1, H-3 — FIXED (commit `a254a82`, main, UNPUSHED; Rama pushes off-market).**

Root cause: `_retry_limit_triple_exits` (orders/order_placer.py) fired from a STALE
snapshot — re-read nothing, and `_pending_exit_retry` entries never expired. After an
LTP-validation failure G5b places a recovery SL within ~15-30s; a later tick then fired
the stale retry: trade still OPEN → a SECOND SL (duplicate-SL/RAMCOIND oversell: a
stop-hit inside the one-cycle dedupe window double-fills); trade already CLOSED → SL+TGT
placed on a flat position → naked reverse.

Fix (mirror `retry_tgt_for_trade`, reuse its helpers — no divergent check):
- re-read via `store.get_trade_for_tgt_retry`; bail unless OPEN/PARTIAL (drop entry).
- if a non-terminal SL exists (`store.get_sl_order_for_trade`), skip the SL leg + place
  only the missing TGT via `self.retry_tgt_for_trade(trade_id)` (idempotent, self-guarding)
  — no duplicate SL.
- OPEN + no SL → still place SL+TGT (legit retry preserved; the guard must not over-bail).
- TTL: added `_ExitRetryParams.enqueued_at` (now_ist, set in `_add_to_exit_retry`);
  `_EXIT_RETRY_TTL_SEC=180.0`; a fire older than TTL is dropped. Rationale: 180s ≈ 6× the
  ~30s G5b recovery bound, ≪ the 15-min reconciler cycle; a legit retry fires on the first
  LTP tick (seconds) far inside it.

Parity: single shared path (`_on_ltp_tick_for_retry`→`_retry_limit_triple_exits`; paper
synth + live both dispatch here, only the adapter differs). No paper duplicate. One fix both.

⚠️ TOCTOU residual (out of scope): `get_sl_order_for_trade` is LOCAL-table based (the same
helper retry_tgt_for_trade uses) → ~40ms lag vs broker truth for NEAR-SIMULTANEOUS SL
placement. NOT an H-3 issue (the G5b SL lands ~15-30s before the retry); the RAMCOIND
4-layer reconciler/G5b defense (`_check_duplicate_exits` + G5b `_already_has_live_sl`) is
the compensating backstop. Not re-architected here.

Test: `tests/unit/test_h3_exit_retry_guard.py` (4) — real StateStore over real schema + real
`_retry_limit_triple_exits` guards (the conftest RealSchemaStore shim can't back
`get_trade_for_tgt_retry`/`get_sl_order_for_trade` — replicating them would be the forbidden
divergent check). T1 closed→bail + T2 open+SL→skip-SL RED→GREEN; T3 open+no-SL→place (no
over-bail); T4 stale→drop. Regression: order_placer 127 pass.

Emergency-exit chain: **H-1✓ H-2✓ H-3✓ — only M-O1 (NSE:NSE: double-prefix, order_reconciler)
remains.** Also open: twin `kill_switch.py:977` dead-col; H-12 paper qty-sign (Wave 3).
Deploy caveat (Wave 0a): live post-receive = checkout only, no restart; trading-system
inactive now → next start picks it up; a running session needs a manual `systemctl restart`.

Related: [[h2_fixed_exiting_close_05jul]] · [[h1_fixed_dead_column_05jul]] · [[ramcoind_duplicate_sl_incident_25jun]] · [[full_repo_audit_04jul_pending]] · [[tgt_retry_mechanism]]
