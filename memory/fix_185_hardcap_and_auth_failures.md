---
name: fix_185_hardcap_and_auth_failures
description: FIX-185 — hard position cap during restart burst + 403 auth errors excluded from auto-trip
metadata: 
  node_type: memory
  type: project
  originSessionId: 926bcdec-f5d1-4d8b-ab01-42b2d61dba29
---

FIX-185 (2026-06-18, commit 6cb29b0). Two live-trading hardenings from the
18-Jun incident.

**(1) Hard position cap during restart burst.** OPEN_POSITIONS relied on
signal_processor's in-memory `processor_in_flight` snapshot, taken at increment
time BEFORE the candidate takes portfolio_lock — a restart burst could
under-count it and exceed max_open (observed 6 open vs max 5). Added authoritative
count: every accepted entry holds a FundManager reservation from reserve() until
the entry FILLS (commit pops it as status flips to OPEN), so OPEN/PARTIAL
(open_count) + live reservations (reserve→fill, incl reserved-not-placed and
PENDING_FILL) partition all positions with no overlap/gap. New
`FundManager.count_live_reservations()`. risk_engine uses
`max(legacy_total, open_count+reservations, active_count_floor) + 1` — can only
HARDEN, never loosen; FIX-181 final-slot off-by-one preserved; getattr guard for
pre-FIX-185 fund managers. active_count kept as floor for PENDING_FILL rows whose
reservation was lost across a restart.

**(2) 403 auth errors don't auto-trip.** A 403 PermissionException ("IP not
allowed to place orders") is a config/credential error, not a transient API
failure, but counted toward the consecutive-API-failure auto-trip → SOFT_KILL →
restart crash-loop (see [[kite_ip_allowlist_dependency]]).
`kill_switch.record_api_failure(exc)` now skips `BrokerAuthError` (logged
CRITICAL for visibility); the 8 BrokerError call sites in signal_processor
forward the exception. Timeout/rate-limit still count and still trip.

**Config:** max_open_positions left at **5** (operator confirmed; NOT reverted to
3 despite the prompt's "=3" — the recent 3→5 raise in 5311dcb stands). The fix is
value-agnostic.

**Validation:** 317 tests pass on the VM (test_risk_engine, test_kill_switch,
test_signal_processor, test_fund_manager, test_p0_live_day1_fixes, test_main).
Locally only the 5 touched suites run green (251) — the rest of the local suite
has env gaps (waitress/pyotp/tzdata missing, real NTP) unrelated to the change.

**Deploy:** pushed + deployed to VM working tree. Takes effect on NEXT restart
(per [[deploy_requires_restart]]) — NOT force-restarted (preventive fixes; system
was healthy with 6 open positions; no active 403s since the IP allowlist fix).
Parity: identical paper/live paths.
