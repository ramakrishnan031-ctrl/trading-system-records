---
name: human_order_policy
description: "System manages only system trades; human/operator orders in Kite are detected, logged once, never adopted/protected/flattened"
metadata: 
  node_type: memory
  type: project
  originSessionId: 705e3934-5847-4a81-9394-fec010dffb93
---

Rama's decision (FINAL, 16-Jun-2026): the system manages ONLY system trades. Human orders (operator-placed directly in Kite, e.g. ITC, manual AGARIND adds) are NOT tracked — the system never places SL/TGT for them, never adopts, never flattens them.

Detection (post-FIX-181): a broker position whose only/any local trade is PENDING/PENDING_FILL routes to `_check2_inflight_orphan` (system in-flight fill → flatten on HARD_KILL). A broker position with NO local trade at all = human order → `_check2_orphan_adoption`.

Behaviour ([[fix_182_complete]] FIX 2):
- order_reconciler `_check2_orphan_adoption`: log INFO once per symbol per day, then silent. No repeated CapitalDriftDetected. Daily set `_human_order_symbols` reset at IST date change.
- Capital: broker margin is source of truth; FM tracks only system trades. Drift from human orders is EXPECTED. G3 capital-drift effective tolerance = capital_drift_tolerance + human_order_margin_tolerance (default Rs5000) when human orders detected today. Genuine catastrophic drift beyond the allowance still alerts CRITICAL.
- EOD residual sweep: flattens system orphans (local trade exists for symbol today) but skips human positions (no local trade).

Discriminator used everywhere: "does a local trade row exist for this symbol today?" (Kite positions don't carry order tags, so the trades table is the reliable system-vs-human signal).
