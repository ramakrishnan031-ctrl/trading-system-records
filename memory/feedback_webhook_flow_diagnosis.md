---
name: feedback_webhook_flow_diagnosis
description: "How to correctly diagnose \"no signals\" — query webhook_audit (the authoritative inbound-POST record), NOT just the signals table + systemd journal; the entry_start=10:00 launch-phase gate 403s every POST pre-10:00 so it LOOKS like a silent outage but isn't."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1d1e6c9d-1d21-4715-b704-3b6d175f00db
---

**Diagnosing webhook intake / "no signals": check `webhook_audit` FIRST — it is the sole authoritative record of inbound POSTs. Do NOT infer "no POSTs" from an empty `signals` table + a journal grep.**

**Why:** On 13-Jul-2026 ~09:56 (Block 2) I wrongly reported "ZERO inbound webhook POSTs all day / silent outage." I had checked only (a) the `signals` table (0 today — correct) and (b) a systemd-journal grep (webhooks don't log there). That false premise triggered an urgent, unnecessary firewall/IP/fail2ban diagnosis (D1-D5). **Reality:** `webhook_audit` held **598 POSTs from 23.106.53.213** — **289× 403 (09:16→09:59)** then **309× 200 (10:00:19→10:37)**; the system was trading normally (413 signals, 23 MIS orders, 11 trades). Nothing was wrong: VM IP unchanged (161.118.187.249), /32 allowlist accepting (20,725 pkts), fail2ban only `sshd`.

**How to apply — before EVER declaring a webhook outage:**
- Query **`webhook_audit`** (cols: `ts, scanner_name, source_ip, payload_size_bytes, response_code, signals_accepted, signals_rejected, duration_ms`) — today's count + `response_code` split + `source_ip`. This is the ground truth (per [[c2_chartink_ip_investigation_03jul]] the DB table is the sole record; the journal does NOT record webhook POSTs).
- **A POST creates a `signals` row ONLY if it passes the entry-window gate.** `entry_start: "10:00"` (LAUNCH-PHASE; relax toward 09:20 later) → **every POST before 10:00 is 403'd "outside entry window" and creates NO signal row.** So `signals=0` before 10:00 is EXPECTED, not an outage. `screener_results` is likewise empty until signals pass.
- **Response-code semantics (from S-1A GATE D):** only **401 = token/auth failure**; **403 = kill-switch OR outside entry-window (NEVER the token)**; **200 = accepted+enqueued**.
- **A real upstream outage (IP change / firewall drop / fail2ban ban / pool-IP drift off the `23.106.53.213/32` allowlist) shows as ZERO `webhook_audit` rows** (packets dropped before the app) — distinguishable from the 10:00 gate (which shows 403 rows). To catch a live pool-IP drift when webhook_audit is genuinely empty, `sudo tcpdump -ni any 'tcp port 5000'` while Rama fires a Chartink "Test webhook" reveals the true source IP even if the firewall rejects it.

Related: [[s1a_webhook_allowlist_rotation_05jul]] (the /32 allowlist + rotation) · [[c2_chartink_ip_investigation_03jul]] (Chartink = 23.106.53.213 Leaseweb pool, AS59253).
