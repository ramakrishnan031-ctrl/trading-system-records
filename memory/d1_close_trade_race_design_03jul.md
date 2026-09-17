---
name: d1_close_trade_race_design_03jul
description: "D-1 close_trade double-release race — CONFIRMED still live on current main (post A-1/E-1); root evidence + race interleave + design (atomic close + trade_id-latched release_used, no schema change) + test matrix"
metadata: 
  node_type: memory
  type: project
  originSessionId: 54ecd864-01af-4fbe-b453-740efca8a1e9
---

**D-1 (MEDIUM, 02-Jul audit) re-verified 03-Jul vs current main==9becf8c: STILL LIVE — A-1/E-1
did NOT fix it** (it added MORE atomic siblings but never touched close_trade; audit line numbers
still exact). Distinct from the 12-May "double-release fixed" (that closed the OCO/skip-release
layers; D-1 is the residual TOCTOU). NO code written (market-hours read-only, investigate+design).

**Root (evidence):**
- Guard non-atomic: `orders/order_manager.py:533-542` — `get_trade()` autocommit read → Python
  check `status not in ('OPEN','PARTIAL')` → raise. Commit `:587-616` — `UPDATE trades SET
  status='CLOSED' … WHERE trade_id=?` — **NO status predicate, NO rowcount check** → overwrites a
  concurrent winner (incl. CLOSED_MANUAL relabel → audit-trail corruption too).
- `release_used` NOT idempotent: `fund_manager.py:1104-1113` — keyed symbol/intent/prices, **no
  trade_id param, no latch**; every call recomputes margin, mutates buckets, `_total += pnl`,
  writes a RELEASE_USED ledger row. `_bucket_deduct_used:1993-97` has NO negative guard.
- close_trade is the ONLY closing transition NOT rowcount-guarded — siblings all atomic:
  `mark_trade_manually_closed:1528` (CHECK1; reconciler skips release on False,
  order_reconciler:1032-49), `mark_trade_closed_gtt:2148` ("duplicate observer … MUST NOT
  double-release"), `revert_exiting_to_open:1266`, A-1/E-1 `adopt_recovery_trade_to_open:1290`
  (docstring: "Mirrors the mark_trade_manually_closed atomic guard … exactly-once").

**Race (realistic trigger = BOTH actors process the SAME physical close):** our exit fills at
broker → CHECK1 (15s) sees broker-flat + local OPEN before the fill event is consumed →
`mark_trade_manually_closed` WINS atomically → releases (#1, costs=0.0, FIX-180 financials).
Meanwhile placer `_handle_exit_fill` passed its stale L533 check (read OPEN pre-commit; SQLite
write-serialization can queue its UPDATE behind CHECK1's txn, WIDENING the window) → unguarded
UPDATE overwrites CLOSED_MANUAL→CLOSED → `release_used` again (#2) → **double release**. Reverse
orderings are safe (guard raises / rowcount=0 skips) — only the unguarded UPDATE defeats the system.

**Capital impact:** 2nd release: avail += margin+pnl, used −= margin, _total += pnl → FM2 sum
invariant **stays balanced** (Δlhs=Δrhs=+pnl; fm passes cash_floor=_total, pnl_today=0 —
fund_manager:2006-09) → slips. **INV6 negative guards (invariant.py:154-172) catch it ONLY when
doubled margin > remaining used** (few concurrent positions → used<0 → hard_kill; else silent).
Also: fm_ledger gets 2 RELEASE_USED rows → `get_daily_realized_net_pnl` double-counts that trade's
pnl → RE7/FM7 gates skewed (loss→trips early; profit→masks losses) + trades.net_pnl vs ledger
mismatch. Detection today = capital-drift vs broker (alert-only, never kills) + P1 EOD reconcile
(shadow from Mon 06-Jul).

**A-1/E-1 + A-2 interaction: neither mitigates nor races.** Recovery releases go through
idempotent `release_adopted_reservation` (fund_manager:1072-99, "No double-release") on
recovery-status trades (UNKNOWN_IN_FLIGHT/PENDING/PENDING_FILL→FAILED) — disjoint from
OPEN/PARTIAL closes; capital committed only AFTER the atomic adopt win. A-2 timeout holds the
reservation (no release). ADOPTED→OPEN trades later close via the normal path → same D-1 exposure
→ same fix covers. A-1/E-1's contribution = the proven idiom to copy.

**DESIGN (no code yet):** (1) **Atomic close_trade** — fold the guard into the UPDATE
(`WHERE trade_id=? AND status IN ('OPEN','PARTIAL')` + rowcount; on 0 → re-read to classify
not-found vs already-terminal and raise the SAME ValueError taxonomy → placer's existing
except-ValueError "already_closed, return-without-release" path (order_placer:2211-17) becomes the
structural exactly-once gate; keep pre-read only for E.2 pnl-ceiling + qty warning). (2)
**release_used idempotency (defense-in-depth, NO schema change):** add optional `trade_id` param;
write it into the RELEASE_USED ledger row (**column already EXISTS** — schema.sql:471, currently
NULL because the signature can't pass it); latch = in-memory released-set + durable
`fm_ledger WHERE entry_type='RELEASE_USED' AND trade_id=?` check → duplicate ⇒ WARN
`duplicate_suppressed` + no-op ReleaseResult. First-winner semantics (CHECK1 costs=0.0 stands;
placer's richer financials logged-not-written — honest CLOSED_MANUAL). Callers pass trade_id
(placer/CHECK1/GTT). Parity: pure logic, one path. Preserves CHECK1-skip, GTT gate, A1E1
adopt/fail, RAMCOIND/CHECK9/G5b (no status-flow change).

**Plan:** branch `fix-d1-atomic-close` AFTER the batch+GUI soak (next week, can pair with B-2);
fail-on-old tests first; no flag needed (deterministic correctness fix); off-market push. **Test
matrix:** ① concurrent close_trade ×2 → ONE wins, single release [fail-on-old] ② rowcount=0 →
correct ValueError classification ③ placer-vs-CHECK1 interleave → CLOSED_MANUAL preserved, no 2nd
release ④ release_used same trade_id ×2 → 2nd no-op+WARN, buckets/invariant green ⑤ INV6
negative-used regression ⑥ GTT duplicate-observer (3.5e) regression ⑦ adopted→OPEN→close single
release ⑧ paper/live parity ⑨ FIX-180 financials when CHECK1 wins ⑩ normal single-exit unchanged
(fields/alerts/OCO). **SYSTEM_MAP pointer DEFERRED** — tree=gui-deploy-03jul frozen for tonight's
push (same flag as [[b1_unrealized_mtm_design_03jul]]); land with the fix branch or post-deploy
docs pass.
