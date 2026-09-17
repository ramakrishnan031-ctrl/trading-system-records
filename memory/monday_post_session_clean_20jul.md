---
name: monday-post-session-clean-20jul
description: "Monday 20-Jul post-session checklist = CLEAN WITH NOTES. Forward shadow uncontaminated (1 new date, sim_R 6.4% null, OOS 3->4); worst intraday -Rs 18.29 (6.18% of the -296 limit); capital invariant holds to the paisa once RESET_PNL is excluded."
metadata: 
  node_type: memory
  type: project
  originSessionId: cc7e4afb-c67e-4eb3-8fc7-ff345f73333a
  modified: 2026-07-20T13:26:19.744Z
---

**Verdict: CLEAN WITH NOTES — no BAD item, no STOP condition.** Report
`docs/audit/monday_post_session_results_20jul2026.md` (commit `a47bc87`). Run read-only 20-Jul 18:39.

**⭐ THE FORWARD SHADOW (the sole confirmation path for D3/D4/#10/#06) IS SOUND:** exactly **ONE** new date
`2026-07-20`; **7,827 → 8,855** lines (+1,028, exact); **`sim_R` NULL = 6.4%**, `ms4_stats_ok` 962/1028;
recorder heartbeat `wrote=1028 sim=962` cross-checks. **The silent-degradation mode did NOT occur** — the
token was present and candles fetched. **Genuine OOS window 3 → 4 days** (07-14/15/16 + 07-20; 07-13 is the
basis day). Provenance stamped `git_commit=056963e3470b`. **D3 was NOT re-run** (per B5). ⭐ Also **answered
by observation, not assumption: the 18:15 cron recorder DOES fire on a day the service self-exited at 16:00**
— it is a cron, independent of the service.

**The numbers** (capital vocabulary: all P&L vs **actual capital** Rs 9,875.60, unlevered):
- **Worst intraday cumulative = −Rs 18.29 = 6.18% of the ~−Rs 296 limit.** No DAILY kill. (Ongoing input to
  decision 01.)
- 4 entered trades (BEPL, PNB, KROSS, HUHTAMAKI — all MIS, all hour 10), 4 rejected; 1,028 scored;
  87.5% in hour 10. Row deltas: signals +3,076 · trades +8 · orders +12 · fm_ledger +29.
- **Σgross = −16.97** (= the broker account delta 9,875.60 → 9,858.63, exactly) · **Σcharges = 1.32** ·
  **Σnet = −18.29** (what the daily-loss control reads). ⚠️ **The "~−Rs 17" and "−18.29" do NOT disagree —
  they are gross vs net.** HUHTAMAKI was an RMS/external close at 13:52 (costs passed 0.0, as documented).
- **Capital invariant HOLDS to the paisa** once the reversal row is excluded: `Σ pnl_delta(trading)` ==
  `Σ trades.net_pnl` == **−18.29**, and per-trade `pnl_delta == net_pnl` row for row.
  `RESET_PNL.pnl_delta = +19.61 = −(Σpnl_delta − Σcosts)` = the **expected Option-B signature**, E4/W10 not
  shipped. Its only observable: the day counter resets to **+1.32** (=+Σcosts) not 0.00 — **date-scoped, so
  it cannot leak to the next day**, and it lands at 15:17 after the 15:15 SOFT_KILL. **E4/W10's impact today
  = one bookkeeping row by Rs 1.32; nil on outcomes.**
- Boot 08:15:19 → `eod_self_exit` 16:00:04 (exit 0, NRestarts=0) = 7h44m. Rehydrate the predicted **no-op**
  (0 trades / 0 P&L rows / M-C1 carryover 0), seed landed on 9,875.60. All crons SUCCESS
  (`backup_retention` FAILED = the known benign safety-abort). **Liveness probe measured, not assumed** —
  0-byte log + no sentinel + its schedule-twin `capture_metrics_baseline` logged **84 contiguous 5-min
  heartbeats 09:00:02→15:55:01**. **The S4 class did not recur.**

**Recorded, NOT today:** `eod_cleanup` crashed 15-Jul with `FOREIGN KEY constraint failed` on the signal
fingerprint prune (`scripts/eod_cleanup.py:201`) and **wrote no heartbeat at all** — so it reads as MISSED,
never FAILED (an S4-shaped silent failure). Today it succeeded; 3 clean runs since. **Direct evidence for
decision #09 (prune-retention): the fingerprint prune CAN violate an FK against a child table.**

⚠️ Four of the checklist's own prose expectations were wrong — see [[verify-check-the-rc-not-the-output]] §4.
See also [[preflight-401-third-sibling-20jul]] for the one NEW live finding.
[[monday-first-real-boot-proven-20jul]] [[capital-vocabulary]] [[dual-daily-loss-mechanism]]
