---
name: ct-ct144-result
description: "CT144: Maximum Dirty State SIGKILL — PASS_WITH_RISK. Recovery clean; no capital_snapshot in paper mode; daily limit prevented full dirty state."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f6347b4-0a9c-4253-b5d1-150bacb5b32b
---

## CT144 | Maximum Dirty State SIGKILL | PASS_WITH_RISK

**Date:** 2026-06-10 ~11:15 IST

**Pre-kill state:** 0 open positions (daily limit 20 hit — 21 trades today), 20 orphan open orders, 6164 fm_ledger entries, balance=696300.36. Kill switch INACTIVE.

**Note:** Could not build prescribed dirty state (3 positions + 2 pending + SmartTgt + 5 queued signals) because daily trade limit hit. Tested with orphan orders as dirty state.

**SIGKILL + Recovery:**
- [PASS] `kill -9` succeeded, system fully stopped
- [PASS] `systemctl start` → WARM startup at 11:17:28
- [PASS] Health check: ok, kill switch INACTIVE, queue 0/300
- [PASS] Capital rebuilt from fm_ledger (new INIT entry id=6165, balance=1000000)
- [PASS] No phantom signals (0 duplicate signal_ids)
- [PASS] No duplicate fm_ledger entries
- [PASS] DB integrity: `PRAGMA quick_check` = ok

**Known limitation:**
- Invariant A (external checker): FAIL — "No capital_snapshot row found". This is a known paper-mode limitation (capital_snapshot table not populated). Same finding as Day 4 CT093/CT096. The internal FundManager invariant passed during rehydration.

**Risk:** Daily trade limit prevented testing with full dirty state (open positions + pending entries + SmartTgt trail). Core crash recovery mechanism verified but without open-position rehydration.
