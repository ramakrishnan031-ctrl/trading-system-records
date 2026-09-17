---
name: PHASE A COMPLETE milestone
description: Phase A landed green on 2026-04-19 with commit 4a08d73 (A.3.g); 1494 tests; 10-commit series 9c7a195..4a08d73
type: project
originSessionId: 41e4666f-fea1-4279-965e-4551beac45c9
---
PHASE A COMPLETE on 2026-04-19.

**Why:** Phase A closed the entry-to-exit lifecycle loop: OrderPlacer now splits entry vs. exit fill handling, publishes PositionClosed on exit, releases capital direction-aware, and the paper adapter synthesizes OrderFilled so downstream is actually exercised in paper mode. Before Phase A, paper trials stopped at entry placement and everything past commit_to_used was silently untested.

**How to apply:** When asked about Phase A scope, cite commit 4a08d73 (A.3.g) as the exit gate. Phase B work begins with BL-5 (write-ahead ledger) then BL-1 (rehydrate_from_open_trades) — BL-5 must land before BL-1 because rehydrate depends on a trustworthy ledger.

### Closeout facts
- Final commit: **4a08d73** (A.3.g integration exit gate)
- Final test count: **1494 green** (+2 from A.3.g; pre-A.3.g baseline was 1492)
- 3× consecutive run verdict on the new Phase A exit-gate class: **3/3 clean, no flake detected at N=3**
- Phase A commit list (in order 9c7a195 → 4a08d73):
  1. `9c7a195` BL-14 | alerts | fix TelegramNotifier.send() caller signature drift
  2. `fa41b80` docs | track EF-1: WebhookReceiver config-shape mismatch (deferred Phase E)
  3. `c179568` BL-12 | events | OrderStatusChanged pipeline: order_monitor → order_manager
  4. `2708e57` BL-7a | orders | lock _FillEntry.leg taxonomy + add order_protocol/direction
  5. `635d2dc` BL-7b | orders+main | inject order_monitor + smart_tgt + smart_tgt_cfg into OrderPlacer
  6. `55cd63b` BL-7c | orders | call order_monitor.track() for entry/SL/TGT; guard non-ENTRY fills (interim)
  7. `a5ea780` BL-7d+BL-10a | orders+capital | split _on_order_filled into entry/exit; publish PositionClosed on exit; OrderManager.close_trade; EF-3 direction-aware release_used
  8. `8e72d10` BL-10b | reconciler | publish PositionClosed from MANUAL_CLOSE path
  9. `0fc60b4` H-20 | broker | paper adapter synthesizes OrderFilled after configurable delay (ZA16a amendment)
  10. `4a08d73` A.3.g | integration | Phase A exit gate: full-lifecycle capital accounting test (LONG + SHORT)

### Architectural locks established in Phase A
- **ZA16 / ZA16a** — zerodha_adapter publishes OrderFilled ONLY in paper mode (via _synth_fill daemon thread). Live mode never publishes; order_monitor does. Runtime guard: _synth_fill logs CRITICAL and returns if invoked with self._paper=False.
- **BL-7 spine** — OrderPlacer._on_order_filled dispatches on _FillEntry.leg; ENTRY → _handle_entry_fill (commit_to_used + record_entry_fill); SL/TGT/EOD → _handle_exit_fill (close_trade + release_used + publish PositionClosed).
- **BL-10 dual publishers** — PositionClosed is emitted from two paths: order_placer._handle_exit_fill (normal fills) and order_reconciler MANUAL_CLOSE branch (broker-side manual closes). Subscribers (shadow_tracker, alerts) receive it regardless of origin.
- **EF-3 direction-aware release_used** — FundManager.release_used now requires `direction` kw; LONG gross_pnl = (exit - entry) * qty, SHORT gross_pnl = (entry - exit) * qty. Pre-EF-3 was LONG-only and silently inverted SHORT PnL.
- **_LEG_ENTRY / _LEG_SL / _LEG_TGT / _LEG_EOD taxonomy** — frozenset-validated in _FillEntry.__init__. Unknown leg raises ValueError at construction.
- **_VALID_EXIT_REASONS** — frozenset({TGT_HIT, SL_HIT, MANUAL_CLOSE, EOD_SQUAREOFF}) enforced in OrderManager.close_trade.
- **PaperConfig + auto_fill_delay_sec** — default 0.5s, Pydantic cap ≤10s, validated in core.config_loader.PaperConfig. Adapter constructor takes the raw float so tests can override past the cap (A.3.g uses 60.0 via indirect parametrize to kill synth-thread races).

### Extra findings status
- **EF-1** WebhookReceiver config shape mismatch — **DEFERRED** to Phase E
- **EF-2** track-after-persist race — **DEFERRED** to Phase E
- **EF-3** release_used LONG-bias — **RESOLVED** in a5ea780 (BL-7d+BL-10a); locked at integration level by A.3.g SHORT test
- **EF-4** paper_capital loose getattr — **DEFERRED** to Phase E

### Next phase pointer
**Phase B** starts with:
1. **B.1 = BL-5** (write-ahead ledger) — MUST land first
2. **B.2 = BL-1** (rehydrate_from_open_trades) — depends on BL-5

Rehydrate cannot be trusted without a write-ahead ledger; do not reverse this order.
