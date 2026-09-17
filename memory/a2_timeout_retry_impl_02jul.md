---
name: a2_timeout_retry_impl_02jul
description: "A-2 IMPLEMENTED (02-Jul, commit fd09a38, unpushed) — stop retrying BrokerTimeoutError; mark signal TIMEOUT; 3 paths; deploy after 03-Jul boot"
metadata: 
  node_type: memory
  type: project
  originSessionId: 567e201a-8ff2-4882-b687-0f55318fab0f
---

Audit A-2 (HIGH) IMPLEMENTED 02-Jul on branch `fix-a2-timeout-no-retry-02jul` @ **`fd09a38`** (UNPUSHED). Follows [[a2_timeout_retry_design_02jul]]. Design doc `docs/design/a2_timeout_retry_design_02jul2026.md`, SYSTEM_MAP pointer updated.

**Fix:** `signals/signal_processor.py` ONLY — a dedicated `except BrokerTimeoutError` in ALL THREE placement paths (`_process_one`, `continue_from_gate`, `continue_from_retest`): record_api_failure; do NOT re-queue (kills the duplicate); do NOT release the reservation (null `reservation_id` locally → order_placer's FIX-068 reservation stays HELD, the 15s reconciler recovery reconstructs/owns it — SINGULAR ownership); mark the signal `TIMEOUT`; free the lock; return. `BrokerRateLimitError` KEEPS its retry (raised pre-submission, nothing sent → idempotent). All 3 paths (not just the audit-cited `_process_one`) because gate/retest also released the reservation on timeout via their outer PLACEMENT_FAILED handler.

**Key implementation discovery (Phase-0 miss):** `signals.status` has a multi-line **CHECK constraint** (the Phase-0 grep didn't match it). A new `PLACEMENT_UNKNOWN` would violate it (IntegrityError → fell through to PLACEMENT_FAILED — the new test caught it). So reused **`TIMEOUT`** instead — already in the CHECK constraint AND already in the report's `_KNOWN_OTHER_STATUSES` (→ "other", SIGNAL-STORAGE Δ=0), currently unused as a signal status. Result: **ZERO schema change, ZERO report change** (the daily_trade_review bucket edits were made then reverted). Trade stays authoritative `UNKNOWN_IN_FLIGHT` (already mapped → rejected_failed in `_trade_bucket`).

**Phase-0 (all 6 GREEN):** no monitoring/alerting keys off PLACEMENT_FAILED-for-timeout or the retry event (only send_warning is EXPIRED); reservation ownership singular after fixing all 3 release sites; recovery is sole authority; paper mode-agnostic; new-status resolved by reusing TIMEOUT.

**Tests (fail-on-old/pass-on-new):** 6 A-2 tests — `test_signal_processor.py` main ×4 (no-requeue+reservation-held+TIMEOUT+one-attempt+api-failure; rate-limit-still-requeued regression; throttle-off-still-one; paper/live parity), `test_sr_v2_continue.py` retest, `test_slice2_strategy_control.py` gate. Reconciler-side rows (adopt/defer/FAILED/flatten) already in `test_a1e1_recovery_matrix.py`. **408 regression green** (signal_processor/gate/retest/a1e1/fix068/order_reconciler/daily_trade_review/order_placer) + 54 naked/RAMCOIND/CHECK9/G5b green.

**DEPLOY: NOT tonight.** Deploy AFTER the 03-Jul 08:15 A-1/E-1 first-boot confirms clean (keep the two changes on the shared timeout path isolated; each validates on a clean base). Rollback = revert `fd09a38`. Then push per the fast-forward pattern ([[post_rotation_creds_02jul]]). NOTE: `.gitignore` (credentials.xlsx) is still uncommitted from the credential task — separate concern, left out of this commit. Related: [[ref_security_audit_02jul]], [[a1_e1_orphan_fix_impl_02jul]].
