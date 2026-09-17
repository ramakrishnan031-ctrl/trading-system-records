---
name: Use VM terminal for curl webhook tests
description: Windows PowerShell escaping breaks JSON in curl commands; SSH to VM and run curl there
type: feedback
originSessionId: d5bd2391-ce3d-4d13-8c5f-cd1d20f63b64
---
Windows PowerShell mangles JSON quotes/escapes when passing to curl or SSH.

**Why:** PowerShell processes backslashes and quotes before passing to external commands, resulting in malformed JSON on the remote end.

**How to apply:**
- For webhook tests: `ssh trading-vm` then run curl directly on VM
- Correct Chartink payload format: `{"stocks":"HDFC","trigger_prices":"1650.00","triggered_at":"1:35 pm"}`
- Alternative: write JSON to local file, use `curl.exe -d @file.json` (works sometimes)
