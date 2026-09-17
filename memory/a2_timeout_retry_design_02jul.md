---
name: a2_timeout_retry_design_02jul
description: A-2 investigate+design (02-Jul) — stop retrying BrokerTimeoutError (duplicate entry); defer to A-1/E-1 recovery. NO code yet
metadata: 
  node_type: memory
  type: project
  originSessionId: 567e201a-8ff2-4882-b687-0f55318fab0f
---

Audit A-2 (HIGH) INVESTIGATE+DESIGN done 02-Jul against `main @ 9becf8c` (post A-1/E-1). Design doc: `docs/design/a2_timeout_retry_design_02jul2026.md` (SYSTEM_MAP points to it). **NO code this pass — awaiting review.**

**Verified root cause (CONFIRMED, live):** `signal_processor.py:1009` catches `BrokerTimeoutError` **together with** `BrokerRateLimitError` and re-queues → pipeline re-runs → **second `place_order` = duplicate/2× exposure**. order_placer itself is correct: `order_placer.py:1291-1323` sets `UNKNOWN_IN_FLIGHT` + enqueues `_timeout_recovery_queue` + KEEPS the reservation (FIX-068) + re-raises (no retry there). The retry is the caller's.

**Masking (not prevention):** the re-queued signal re-hits `entry_throttle.admit` (`signal_processor.py:981`; `min_gap_between_entries_sec:20` + `per_symbol_cooldown_sec:300`) → rejected. It's a RATE-LIMITER; disable it / delay the retry past the gap and the double-submit goes live. Idempotency must not depend on it.

**Two exceptions differ:** `BrokerRateLimitError` (`rate_limiter.py:191/215`) is raised PRE-submission (nothing sent) → retry-safe. `BrokerTimeoutError` is raised inside the live place → order may be at broker → NOT retry-safe.

**Decisive A-1/E-1 interaction:** reconciler daemon polls every 15s (RC3, `order_reconciler.py:576`), running `_recover_in_flight_entries` (`:3133`) startup AND mid-session → correlate-by-tag → adopt+protect (FILLED) / defer (RESTING, reserve restored) / FAILED-only-on-confirmed-ABSENT / flatten-under-HARD_KILL; capital reconstructed (`restore_adopted_reservation` / crash-aware commit `:3400-3408`). So the correct timeout behaviour is: **don't retry — the recovery already OWNS it.** The retry is unsafe AND redundant.

**Design (one file, `signal_processor._process_signal`):** split the `except` — dedicated `except BrokerTimeoutError` that (1) `record_api_failure`, (2) does NOT re-queue, (3) does NOT release the reservation (null `reservation_id` locally so outer/finally don't either → closes the secondary capital under-count where signal_processor released `:1047` what order_placer kept), (4) sets signal status honestly (propose `PLACEMENT_UNKNOWN`, not misleading `PLACEMENT_FAILED`; trade stays authoritative `UNKNOWN_IN_FLIGHT`), (5) `requeued=False` → finally frees the symbol lock, (6) return. Keep `BrokerRateLimitError` in the retry branch. Paper simulates timeout → same single path (parity). Preserves RAMCOIND/CHECK9/G5b/FIX-068; no schema/config/cron.

**Risk:** ≤15s unmanaged window if live = same as existing A-1 window (not new; CHECK9+reconciler cover); depends on reconciler thread alive (audit D-1 `/health is_alive` — track). Test matrix (8 rows) in the design doc: timeout-reached-filled→ONE order adopted; reached-resting→defer→adopt; never-reached→FAILED-on-absence; rate-limit→still retried; reservation held; throttle-off still ONE order; paper parity; HARD_KILL flatten. Fail-on-old / pass-on-new.

Related: [[a1_e1_orphan_fix_impl_02jul]], [[ref_security_audit_02jul]], [[post_rotation_creds_02jul]]. Next after implement: this is the last of the A-group order-path HIGHs.
