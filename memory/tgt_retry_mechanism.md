---
name: tgt_retry_mechanism
description: Standalone TGT retry — re-places a TGT left unplaced by FIX-190 Bug C (SL still protects) on exponential backoff; schema v30
metadata: 
  node_type: memory
  type: project
  originSessionId: fdfc0dce-640b-4e4c-b2f4-1424f338ed1f
---

TGT retry mechanism added 2026-06-19 (pushed/deployed; activates next restart). Closes the
"TGT fails forever" gap from [[fix_190_incident]] Bug C — the 19-Jun THELEELA TGT that
failed at 10:00:28 and was never retried (position rode to SL with no profit target).

**Flow:** when a LIMIT_TRIPLE TGT can't be placed but the SL is live (Bug C SL-only path),
`order_placer._persist_sl_only_protected` flags the trade via
`state_store.mark_needs_tgt_retry` → `trades.needs_tgt_retry=1`. New
`orders/tgt_retry_manager.py` `TGTRetryManager` (30s daemon, started after smart_tgt in
main.py, stopped in `_shutdown`) re-attempts on exponential backoff
**30/60/120/240/480s, give up after 5** (position stays SL-protected) via
`OrderPlacer.retry_tgt_for_trade` → `FullEntryEngine.place_deferred_tgt_only` →
`LimitTripleProtocol.place_tgt_only` (re-clamps to the CURRENT circuit band each attempt —
Bug D, so a relaxed band lets a retry succeed).

**Key design points:**
- **Schema v30** (auto-migrates v29→v30 on restart via the rebuild-from-schema.sql framework):
  `trades.needs_tgt_retry` / `tgt_retry_count` / `tgt_last_retry_at`. State in the DB →
  retries survive restart. `EXPECTED_SCHEMA_VERSION=30`.
- **OCO-critical:** the retried TGT is registered in OrderPlacer `_fill_map` + order_monitor
  (reservation_id="" like a rehydrated exit leg — exit legs use `release_used`, not the
  reservation), so a TGT fill triggers software OCO (cancels the SL). Getting this wrong =
  orphan SL / naked position.
- **Guards in `retry_tgt_for_trade`:** SL must still be standing (never place a naked TGT →
  "skipped_no_sl"); no double-TGT (idempotent → "skipped_has_tgt"); never place an
  unprofitable TGT incl. post-clamp re-check that cancels a clamp-unprofitable order →
  "skipped_unplaceable"; trade must be OPEN/PARTIAL → "skipped_closed".
- **Manager guards:** skip while kill switch active (a flatten, not a target) and outside
  market hours. "failed"/"skipped_unplaceable" count toward the 5 (termination); the
  terminal skips clear the flag. INFO on success / WARNING on give-up.
- Config `tgt_retry:` (enabled/poll_interval_sec/max_attempts/backoff_base_sec) — OPTIONAL
  (default_factory), defaults reproduce the schedule. `backoff_base_sec` floored to 1.
- `calc_tgt_price` uses the ABSOLUTE sl-distance, so an unprofitable TGT only arises from
  the circuit clamp, not the recompute (relevant when writing tests).
- `_circuit_limits` calls `adapter.get_quote([symbol])` expecting `{symbol: quote_obj}`.

18 tests in `tests/unit/test_tgt_retry.py`. Commit on main (TGT retry). Related:
[[fix_190_incident]] · [[followup_reconciler_exiting_gap]]
