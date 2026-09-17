---
name: co-bracket-operational-note
description: CO protocol SL is broker-managed; no separate SL order tracked locally
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7cbac53e-3446-42e1-8243-b814aa9e0215
---

CO_PLUS_TGT protocol SL is **broker-managed** (Zerodha CO bracket). The system never places or tracks a separate SL order for CO trades — only the TGT LIMIT leg is tracked locally.

- SmartTgtManager handles SL trailing **server-side** (updates the CO trigger).
- If a CO position is closed externally (RMS / manual), only reconciler **CHECK1** catches it (cancels orphaned TGT leg, resolves real exit price, releases capital with PnL).
- **Monitor SmartTgtManager health during live trading** — if it stalls, CO SL trailing stops while the position stays open.

Related: [[order-lifecycle-operational-note]], [[capital-operational-note]].
