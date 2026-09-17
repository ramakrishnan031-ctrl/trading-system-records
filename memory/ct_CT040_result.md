---
name: ct-ct040-result
description: CT040 Pipeline Timeout >30s — PASS; slow quote blocks screener thread but caller not blocked
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

**CT040: Pipeline Timeout (>30s screening)** — PASS (2/2)

Isolated test on VM. Mocked quote_fn sleeps 35s. Screener thread blocks (expected — no internal timeout). Caller thread returned within 5s join timeout.

Key insight: `pipeline_timeout_sec` is enforced at signal_processor level, not inside screener. Screener itself has no timeout — the orchestrator kills the thread.

**Related:** [[ct-day1-progress]]
