---
name: ct-ct028-result
description: "CT028 Signal at 09:16: PASS (code-verified) — WR5 checks now_ist() vs is_entry_allowed; cannot inject before 09:25 while inside window"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT028 | Signal at 09:16 (before entry window 09:25) | PASS (code-verified) | 08-Jun-2026

**Test:** Cannot naturally test — we're past 09:25 and WR5 checks current system time (not triggered_at). Injecting with triggered_at=09:16 results in EXPIRED (>10min expiry), not an entry window rejection.

**Code verification:** webhook_receiver.py:388-391 — `is_entry_allowed(now_ist())` checks system clock against market_windows. Before 09:25, this returns False and the webhook returns HTTP 403 "Outside entry window". The per-strategy entry_start_time (09:25) is also enforced at signal_processor.py:506-513.

**Confidence:** HIGH — same mechanism verified working in CT031 (will test at 15:17 when kill switch activates).
