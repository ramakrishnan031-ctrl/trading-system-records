---
name: E.6 EF-2 track-failure cleanup landed (19-Apr-2026, commit 1ad3d5c)
description: Phase E.6 - EF-2 track() post-persist failure cleanup symmetric to BL-8; NO hard_kill; OP-EF2a-d locks; EF-6/EF-6a filed; firm baseline 1645
type: project
originSessionId: daf7a7d0-49f5-49f6-8f12-9791b8824592
---
**Commit:** `1ad3d5c` (19-Apr-2026)
**Subject:** `E.6 | orders | EF-2 track-failure cleanup symmetric to BL-8 persist-failure`

**Items delivered:**

- **EF-2** (CLOSED) — `orders/order_placer.py` `place()` wraps the 3-leg
  (ENTRY/SL/TGT) `_order_monitor.track()` + `_fill_map` write loop in a single
  try/except. On exception:
  1. Pop `_fill_map` entries for legs in `successfully_tracked` (set before
     the exception).
  2. `untrack()` each successfully_tracked leg (exceptions swallowed + logged).
  3. CRITICAL log with grep tag `EF2_TRACK_FAILURE_CLEANUP`.
  4. `_handle_placement_failure(..., broker_order_ids=[all 3 IDs])` — reuses
     the BL-8 symmetric path to cancel broker orders, release capital,
     mark trade FAILED.
  5. Re-raise so the caller knows placement failed.

- **NO hard_kill fires** on EF-2 path. OP-BL8e scope boundary: protocol-only
  failure, capital tracking stays consistent. Same rule as BL-8's
  broker_order_ids cleanup branch.

**Locked decisions (in `orders/order_placer.py` module docstring):**

- **OP-EF2a** — wrap the 3-leg loop; 5-step cleanup as above.
- **OP-EF2b** — NO hard_kill. Reason: protocol-only failure class; capital
  and broker state are recoverable via BL-8 path.
- **OP-EF2c** — trigger near-impossible today (UUID4 collision probability
  ~0, `OrderMonitor.track` has no other raise paths today). Gap kept closed
  defensively because future code may introduce raise paths.
- **OP-EF2d** — greenlight-framed race ("fill arrives before `_fill_map`
  populated") is explicitly out of scope. That race is NOT production-
  reachable: live mode is delayed-discovery via poll (≤poll_interval_sec),
  paper mode has a 10× safety margin (default 500ms synth delay vs ~50ms
  main-thread populate). Implementing for the greenlight framing would
  have added a quarantine queue for a non-existent bug.

**Tests (3 new in `TestEf2TrackFailureCleanup`):**

- `test_ef2_track_raises_on_entry_leg_full_cleanup` — forces
  `ValueError("boom: duplicate internal_id")` on first track(); asserts
  empty _fill_map, 0 untrack calls, all 3 broker IDs cancelled, trade
  FAILED, reservation released, grep tag present in CRITICAL logs,
  `ks.hard_kill_calls == []`.
- `test_ef2_track_raises_mid_loop_partial_cleanup` — forces `[None,
  ValueError("boom on SL")]`; asserts exactly 1 untrack for ENTRY's iid
  (via `assert_called_once_with`), 3 broker cancels, grep tag, no hard_kill.
- `test_ef2_track_success_unchanged_behavior` — regression guard: 3 track
  calls, 0 untrack, 0 cancel, PENDING_FILL, no grep tag, no hard_kill.

**Test count:** 1645 collected at commit 1ad3d5c (verified via `pytest --co`).
test_order_placer.py went 85 → 88. Full suite 1645 green. Phase A gate 15/15.

**Drift investigation (performed immediately after landing):**
Expected ~1630 per greenlight; actual 1645 = +15 unexplained drift. Traced
to E.3's commit-message miscount; E.4 and E.5 inherited the wrong baseline
via delta arithmetic. Process lock added: `pytest --co -q | tail -1` is now
mandatory for every landing report. See `process_lock_test_count.md` +
correction blocks in project_e3/e4/e5 memory files.

**Deferred-EF tracker deltas:**
- **EF-2** — CLOSED this commit.
- **EF-6** — NEW, LOW, deferred: orders-row status on FAILED-trade path
  stays stale (cosmetic; capital+broker+trade all correct).
- **EF-6a** — NEW, LOW, deferred: paper-mode synth-fill race vs cancel
  (paper-only, silent drop via unknown-iid branch, no capital impact).

**Mock parity:** No adjustments needed. All existing `MagicMock(spec=OrderMonitor)`
mocks supported `side_effect` for forcing track() exceptions.

**Architectural locks added:**

- The `_handle_placement_failure(broker_order_ids=...)` contract is now the
  canonical rollback path for ANY `order_placer.place()` failure after
  `_persist_entry_orders` succeeds. New raise points in the post-persist
  block MUST route through it; do not invent a parallel cleanup.
- Grep tag discipline for cross-cutting rollback paths: every critical log
  line emitted from such a path carries an uppercase `<TAG>_CLEANUP` token
  in its message body. `EF2_TRACK_FAILURE_CLEANUP` is the prototype.

**Why:** Close the last of the pre-paper HIGH-latent gaps in order_placer.
EF-2's trigger probability is near-zero today but the rollback semantics
are now symmetric and documented, so future raise-paths inherit the lock.

**How to apply:** Any new post-`_persist_entry_orders` work in `place()`
must stay inside the try/except envelope and append to `successfully_tracked`
on success; the cleanup branch handles the rollback uniformly.
