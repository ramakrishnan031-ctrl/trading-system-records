---
name: ct-ct114-result
description: "CT114 Disk Full: PASS_WITH_RISK — DB intact under 98% disk, no runtime disk monitor"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT114 | Disk Full Warning (<2GB) | PASS_WITH_RISK | 08-Jun-2026

**Test:** Filled disk to 98% (2GB remaining) via fallocate. Injected signal (TCS, gap_fade_short). Signal processed to terminal status (REJECTED_SCORE_57). DB integrity check: ok. No crash, no ENOSPC.

**Risk:** System has no runtime disk-space monitoring. Startup check_disk_space (2GB threshold) only runs at boot. A slow disk fill during market hours would go undetected until a write fails. The healthcheck endpoint doesn't report disk usage.

**Invariant A:** FAIL (pre-existing: no capital_snapshot row in paper cold-start). Not caused by this test.
**Invariants C, D:** PASS.

**Recommendation:** Add periodic disk check to healthcheck or reconciler loop (P2, not blocking).
