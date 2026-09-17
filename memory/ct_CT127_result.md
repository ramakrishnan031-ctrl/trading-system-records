---
name: ct-ct127-result
description: "CT127 Clock Backward -60s — PASS; NTP check detects drift, blocks startup"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

**CT127: Clock Backward -60s** — PASS (code-level verification)

Tested by injecting mock NTP response 60s behind local time into `check_ntp_sync()` on VM:
```
CRITICAL: check_ntp_sync: BLOCKING drift 60.00s >= 5s threshold (host=pool.ntp.org)
passed=False, drift_sec=60.0, block_sec=5.0
VERDICT: BLOCKED
```

System correctly detects 60s clock skew and blocks startup. Two defense layers:
1. `check_ntp_sync()` — queries NTP, blocks if drift >= 5s
2. `check_clock_skew()` — compares local vs broker time, blocks if skew > configured threshold

Did not change actual system clock (service running post-market, VM stability preserved). Code path verified via injectable mock.

**Related:** [[ct-day1-progress]]
