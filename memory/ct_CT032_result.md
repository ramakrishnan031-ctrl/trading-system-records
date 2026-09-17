---
name: ct-ct032-result
description: CT032 Signal while position open same symbol — PASS; correctly rejected as REJECTED_DUPLICATE_SYMBOL
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT032: Signal While Position Open Same Symbol** — PASS

- **Day 2 (09-Jun):** Injected gap_fade_long signal for JNKINDIA while 2 OPEN positions existed → REJECTED_DUPLICATE_SYMBOL
- **Day 6 retest (11-Jun):** Injected UNICHEMLAB SHORT (gap_fade_short) while 2 OPEN LONG positions existed → REJECTED_CONTRARY_POSITION (wash trade prevention)
- Also tested SBIN re-entry after SL_HIT → REJECTED_SHADOW_INNING_ACTIVE
- No duplicate position created in any test
- Kill switch remained INACTIVE
