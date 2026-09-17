---
name: live_day1_zombie_remediation
description: Live Day 1 (15-Jun-2026) 3 zombie entry orders — root cause + how they were remediated on 16-Jun
metadata: 
  node_type: memory
  type: project
  originSessionId: c451e7dc-8922-4a48-8e2b-40197f2c20a4
---

Live Day 1 (2026-06-15): system placed LIMIT entries 11:34–11:35 IST then crashed ~11:53 (pre FIX-178/179) before any fills processed. Three entries left non-terminal in DB and never reconciled: SETL (trd_aa6d346a, CNC qty2 @168.11, order 260615170825087, OPEN), HARIOMPIPE (trd_accc9cab, CNC qty1 @440.40, order 260615170827437, PENDING), AVL (trd_b6bc01c7, MIS qty1 @565.45, order 260615170827485, PENDING).

On 16-Jun ~04:30 the Jun-15 access token expired; order_monitor's get_order_history hit BrokerAuthError x3 → circuit breaker → **HARD_KILL persisted** → system crash-looped, HALTing on startup ("startup_scenario=HALT: hard_kill active"). That was the actual blocker.

**They never filled.** Evidence: fm_ledger had RESERVE-only (no COMMIT) for all three; only SULA actually filled+exited Jun-15 (pnl −0.18). Broker on 16-Jun: 0 positions, 0 holdings, used margin 0, net ₹9995.5 (start ₹9996.91; −1.41 == SULA loss+costs, not ~₹776 of CNC fills). The "COMPLETE" order_monitor saw at 04:29 was a cross-session order_history read with filled_qty=0 (same artifact as order …827398). order_history later returned "Couldn't find that order_id" (purged). So option-2 "reconstruct real P&L" had no fills to reconstruct — corrected to mark CANCELLED.

**Remediation (16-Jun ~09:04, service stopped, backup `trading_system-prefix179remediation-20260616-085459.db`):** UPDATE the 3 orders → status='CANCELLED', reconciliation_status='RECONCILED_NO_FILL' (no trades rows created — they never filled); UPDATE kill_switch_state → state='INACTIVE' (equivalent to KillSwitch.resume(); _persist_state only writes that one row). Restart → clean: "order_monitor rehydrated 0 orders", 0 non-terminal orders, entered runtime loop, get_margins OK (FIX-178). Dangling reservations were already wiped by post-crash capital re-INIT (ledger 7055/7056). See [[co_bracket_operational_note]], [[order_lifecycle_operational_note]].

Also deleted stale nested duplicate `~/systems/trading-system/trading-system/` (103M full clone at FIX-169, ancestor of deployed, empty DB, byte-identical reports, unreferenced). Canonical deploy `~/systems/trading-system` has NO .git (deployed from bare `~/trading-system.git`).

Bare-repo sync (resolved 16-Jun): bare `~/trading-system.git` main was at FIX-177 (41e9592) while the deployed working tree `~/systems/trading-system` was already byte-for-byte FIX-179 (verified all 509 tracked files via git-hash-object == local HEAD blobs — the bare ref had been rewound without reverting the work-tree). Pushed local main → origin (`git push`, remotes origin+vm both = `trading-vm:~/trading-system.git`); post-receive hook auto-deploys via `git --work-tree=$TARGET checkout -f main`. Bare tip now 7614941 (FIX-179) == local HEAD; checkout-f was a no-op (identical content); live service stayed active. Deploy model: working tree has NO .git; canonical = bare repo + post-receive hook.
