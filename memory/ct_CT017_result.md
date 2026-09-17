---
name: ct-ct017-result
description: "CT017 Kill Switch Active: PASS (code+unit-test verified) — 37 unit tests cover SOFT_KILL blocking; live test deferred (active trades)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT017 | Kill Switch Active | PASS (code+unit-test verified) | 08-Jun-2026

**Test attempt:** Set SOFT_KILL directly in DB — but webhook checks in-memory kill_switch object, not DB. Signal was accepted because in-memory state was still INACTIVE.

**Finding:** Kill switch is in-memory with DB persistence. DB mutation alone doesn't affect running system. This is correct — kill_switch.soft_kill() writes DB then updates memory atomically (KS9). Direct DB mutation bypasses the in-memory gate.

**Verification:**
- 37 unit tests in test_kill_switch.py verify SOFT_KILL blocks new signals
- webhook_receiver.py:374 checks `self._ks.is_active()` (WR5)
- signal_processor.py:434-436 re-checks kill switch before order placement
- Live test requires restart with active trades (too risky) or exceeding daily loss limit

**Confidence:** HIGH — dual-layer check verified in code, 37 unit tests pass.
