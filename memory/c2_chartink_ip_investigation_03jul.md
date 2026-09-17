---
name: c2_chartink_ip_investigation_03jul
description: "C-2 prep — Chartink webhook source-IP investigation (read-only, 03-Jul); 1 static IP across 15 trading days, Leaseweb Singapore ASN; no A-vs-B verdict, facts only for a later C-2 design session"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9fe7c775-fb70-4094-bcaf-e66df45399c5
---

**Read-only investigation (03-Jul-2026 ~22:30 IST, off-market).** Zero code/config changes, nothing pushed. Purpose: determine whether C-2 Option A (IP allowlist) is safe or Option B (reverse proxy + HMAC) is needed because Chartink's egress IP drifts. Full report: `docs/audit/c2_chartink_ip_investigation_03jul2026.md`.

**Ground truth source:** `webhook_audit.source_ip` in `trading_system.db` — populated from `request.remote_addr` at `signals/webhook_receiver.py:341` (no reverse proxy exists on the VM, confirmed no nginx, so this is the raw TCP peer, not a spoofable `X-Forwarded-For`). No other IP source exists: fail2ban only has an `sshd` jail (nothing webhook-related), and app debug/system logs don't echo `source_ip` at all — the DB table is the sole record.

**Findings (15 trading days, 2026-06-12→2026-07-03, 58,507 total webhook hits):**
- **23.106.53.213** — 58,504 hits (99.99%), hit **every single one of the 15 days**, all 13 scanner names, no gaps. **STATIC-so-far.**
- 2 single-hit outliers in the **same /24** (23.106.53.222, 23.106.53.196) — both carried real scanner names + realistic payload sizes (366/369 bytes), both 403'd for reasons unrelated to IP (webhook_receiver.py has only two 403 causes: kill-switch-active or outside the 10:00–15:00 entry window — confirmed by code, not IP-based rejection since no allowlist exists yet). These look like genuine Chartink deliveries, not noise.
- 1 hit from `127.0.0.1` (0-byte payload, 3 min after one outlier) — classified as an operator test/curl reproduction, not Chartink.
- **CIDR/ASN:** all 3 non-localhost IPs → same `/24` (`23.106.53.0/24`), same `/21` (`23.106.48.0/21`), same ASN **AS59253 (Leaseweb Singapore Pte. Ltd.)** — Chartink's alert infra sits on rented hosting capacity, not a fixed corporate range.

**Verdict:** STATIC-so-far for the dominant IP (99.99%, 15/15 days unbroken), with an explicit caveat: 2 single-occurrence same-/24 hits in 15 days are **insufficient data** to rule out occasional pool-IP variation. Not "drifting," not "fully static with zero exceptions."

**Deliberately NOT decided here (per scope):** Option A (IP allowlist) vs Option B (reverse proxy + existing secret/HMAC auth) — that's Web Claude + Rama's call in a dedicated C-2 session, working from these facts. See [[c2_webhook_lockdown_02jul]] for the Phase-2 lockdown already deployed (token-bucket rate limit + WEBHOOK_SECRET required both modes; bind still `0.0.0.0`/`require_hmac:false` pending this Phase-3 network decision).
