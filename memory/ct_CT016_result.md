---
name: ct-ct016-result
description: "CT016 Invalid Scanner: PASS — HTTP 404 'Unknown scanner' for nonexistent_scanner"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT016 | Invalid Scanner | PASS | 08-Jun-2026

**Test:** POST to /webhook/nonexistent_scanner. Result: HTTP 404, `{"error":"Unknown scanner: 'nonexistent_scanner'"}`.

**Mechanism:** WR4 at webhook_receiver.py:370-372 checks scanner_name against scan_webhook_map. Unknown scanners rejected before parsing payload.
