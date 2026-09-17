---
name: project-crash-test-monday-plan
description: "Crash test Day 1 plan: Mon Jun 8 starts at CT008; skip list; token needed first"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6baefba5-fbd6-4be5-a6cf-cb04d7f1755c
---

Day 1 Mon Jun 8 starts at CT008.

**Skip (already done or not applicable offline):** CT001-CT007, CT019-CT022, CT035-CT036, CT047-CT048, CT093, CT096, CT100, CT103, CT105, CT114, CT116-CT118, CT120, CT126-CT127, CT132-CT133, CT135.

**Needs broker API:** CT008-CT018, CT023-CT034. Token needed first.

**Deferred to Monday (need running system):** CT114 (disk full), CT127 (clock backward), CT132 (delete config mid-session), CT135 (cleanup safety gate). CT133 ran on VM 07-Jun (PASS_WITH_RISK).

**Why:** Day 0 offline testing (05-Jun + 07-Jun) covered all API-independent scenarios. Day 1 shifts to live broker-dependent tests.

**How to apply:** Start Monday by generating Zerodha token, verify system starts, then run CT008 onwards via scenario_runner.py.
