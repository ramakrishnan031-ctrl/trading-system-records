---
name: fix-156-complete
description: "FIX-156 committed 09-Jun-2026: paper capital re-sync, CLOSED_MANUAL PnL inclusion, locale-safe bat date"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

FIX-156 committed 09-Jun-2026 (4a89cdb). Paper capital re-sync on restart eliminates overnight drift alerts. CLOSED_MANUAL trades now included in PnL queries (state_store, strategy_governor, performance_allocator). zerodha_morning.bat uses Python for locale-independent date check. 2812 tests pass.

**Why:** Day 2 crash test found Rs 140.45 PnL variance from orphan-cleanup trades with CLOSED_MANUAL status being excluded from SUM queries. Paper capital static reset caused Rs 3,499 drift alert every restart.

**How to apply:** Verify on VM after SCP — drift alert should not fire on restart. CLOSED_MANUAL trades now count in all PnL-related reports and circuit breakers.

Related: [[ct-day3-prereqs]] [[ct-capital-drift-finding]]
