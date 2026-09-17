---
name: config_change_needed_concentration
description: "Position sizing gives qty=1 for a ~Rs 572 stock on a Rs 10K account — caused by max_concentration_pct=0.10; raising it is a config decision for Rama, not a bug"
metadata: 
  node_type: memory
  type: project
  originSessionId: 768ee318-85d1-4db9-a514-076df3b7c129
---

Position sizing returns qty=1 for a ~Rs 572 stock on the Rs 10K live account.

**Root cause:** `max_concentration_pct=0.10` (10% of Rs 10K = Rs 1000 max per stock) caps a single position to ~1 share at that price. NOT a bug — it's the concentration guard working as configured.

**To get qty=4:** raise `max_concentration_pct` toward ~0.25 in config/system_config.yaml (25% of 10K = Rs 2500 → ~4 shares at Rs 572).

**Decision is Rama's** — it's a risk/config trade-off (concentration vs. tradeable size on a tiny account), not something to change unilaterally. Surface it; don't auto-apply. Related: [[fix_181_complete]] (same Live Day 1 review window).
