---
name: phase2-carryover-proven-21jul
description: "21-Jul mid-session restart (11:57) PROVED the Phase-2 P&L carryover rehydrate in production for the first time: daily_pnl=-12.57, 3 rows replayed, 0 anomalies, _total on broker.net, on the new E4/W10 contract."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c4770e8-90bb-44e6-90c3-bfe4c179b944
  modified: 2026-07-21T07:29:46.442Z
---

The forced 11:57 mid-session restart (fallout of the soft-kill halt) exercised `fund_manager.rehydrate` with **real same-day state** — the first non-trivial production observation: `rehydrate_complete anomaly_count=0 daily_pnl=-12.57 replayed_pnl_rows=3 replayed_trades=0 total=9846.16`. It reconstructed the day's realized net **exactly**, `_total` landed on `broker.net` (9846.16), zero anomalies — **on the new E4/W10 reader contract, with non-zero carryover.**

**Why:** every prior production observation of the restore path was a 0/0/0 no-op on a flat book (Monday included). This is the exact mechanism the whole M-C1 re-derivation concerned; it arrived as a by-product of an accident no plan would have scheduled.

**How to apply:** treat Phase-2 P&L carryover as PROVEN in prod — remove it from the never-proven list. Still UNPROVEN (do not conflate): Phase-1 replay of a live OPEN position; same-day-kill survival with the service RUNNING (shown impossible — [[persisted-kill-is-halt-21jul]]); first live HARD_KILL.

Related: [[monday-first-real-boot-proven-20jul]] [[e4-w10-deployed-20jul]] [[q9-live-seed-mc1-wired-19jul]]
