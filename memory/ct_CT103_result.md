---
name: ct-ct103-result
description: "CT103 HALT Start Exit Code 3 — PASS_WITH_RISK; config load used exit 5 not 3, caused restart loop; fixed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT103: HALT Start (Exit Code 3)** — PASS_WITH_RISK

System correctly detects missing system_config.yaml and exits with CRITICAL log. However:

**Finding:** Config load failure returned exit code 5 instead of 3 (HALT). Since `RestartPreventExitStatus=3` only blocks code 3, systemd restarted the process on code 5, causing a restart loop until StartLimitBurst hit.

**Fix applied:**
1. Changed config load failure from `return 5` to `return 3` in main.py
2. Added exit code 6 (auth failure) to `RestartPreventExitStatus=3 6` in systemd unit

**Evidence:**
```
CRITICAL main — Config load failed: Required config file not found: system_config.yaml
systemd: Main process exited, code=exited, status=5/NOTINSTALLED
systemd: Scheduled restart job, restart counter is at 4
```

After fix: config load failure exits 3, systemd does NOT restart.

Related: [[ct-CT105-result]] [[fix-156-complete]]
