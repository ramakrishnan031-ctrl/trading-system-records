---
name: s1_webhook_verification_05jul
description: S-1 pre-implementation verification (05-Jul) — 4 webhook-ingress facts confirmed read-only; CRITICAL new find = WEBHOOK_SECRET stored plaintext in signals.webhook_payload (95431/95431 rows) because Chartink echoes ?token= in the body
metadata: 
  node_type: memory
  type: project
  originSessionId: 46720e02-4098-4c34-87c3-16d4cb5c52fa
---

**S-1 (webhook ingress) pre-implementation verification, 05-Jul-2026 — READ-ONLY, NO changes.** Feeds the Option-B1 plan (nginx+TLS+Flask→127.0.0.1+secret-in-body+close public :5000). Evidence pasted verbatim to Web Claude.

## 🚨 CRITICAL NEW FINDING (beyond the 4 asks) — secret-at-rest leak
Chartink echoes the FULL webhook URL **including `?token=<SECRET>`** as a body field `webhook_url`, and the receiver persists the entire raw body to **`signals.webhook_payload`** (`webhook_receiver.py:579`). Live count: **95,431 / 95,431** signal rows contain `token=` in the stored payload → the WEBHOOK_SECRET is in the DB **and all 3.4G backups**, plaintext. This is worse than the URL-in-access-log concern and the 03-Jul rotation doesn't undo history. **S-1 fix MUST also redact the token/`webhook_url` before persisting `webhook_payload`** — moving the secret to a body field alone still gets stored plaintext unless the persist path strips it.

## FACT 1 — body-secret support (receiver)
Auth `webhook_receiver.py:410-432` (`if self._secret:`): accepts `X-Webhook-Signature: sha256=<hex>` (HMAC over `raw_body`, already implemented, WR8) OR `?token=<secret>` query param (`request.args.get("token")`, `_hmac.compare_digest`). Param name = **`token`**. Body = `request.get_data()` raw bytes (:342) → `json.loads(raw_body)` (:460) = **JSON, not form/get_json**. Auth runs BEFORE body-parse (:410 vs :460). Receiver does NOT read a plaintext secret from the body today. Query→body change = parse JSON earlier (or inside the auth block) + add a `body.get("<field>")` compare_digest branch at :410-432. HMAC already keeps the secret out of the URL but Chartink can't sign (config :188) → secret-in-body is the Chartink-compatible path.

## FACT 2 — transport = plain HTTP, no TLS, no proxy
Served by **waitress** `main.py:2813-2826` (`_waitress_serve(app, host=bind_host, port=bind_port, threads=8, connection_limit=100)`). **NO `ssl_context`** anywhere → plain HTTP. Self-check `http://127.0.0.1:5000/health` (:2830). No reverse proxy (waitress binds 0.0.0.0:5000 directly; Phase-10 nft showed nothing on :80, Tailscale only on :443). Config `system_config.yaml:179-188`: bind_host `0.0.0.0`, bind_port `5000`, `require_hmac: false`.

## FACT 3 — Chartink egress = ONE stable Leaseweb-SG IP
`webhook_audit.source_ip` logs it. Single IP **`23.106.53.213`** for ALL 38,046 accepted POSTs, 12-Jun→03-Jul (200×28,447 / 403×8,606 / 503×1). whois → `LSW-SG-SIN10-2`, **Leaseweb Asia Pacific Pte Ltd, SG** (matches the C-2 baseline). Stable, not drifting → **allowlist viable** (single /32). (Source IP IS logged, so the allowlist target IS derivable from logs — no test-capture needed.)

## FACT 4 — payload format (JSON body)
Keys present: `stocks` (comma symbols), `trigger_prices` (comma prices), `triggered_at` ("H:MM am/pm" or "YYYY-MM-DD HH:MM:SS"), `scan_name`, `scan_url`, `alert_name`, `webhook_url` (echoes the `?token=` URL). Receiver READS: `stocks`+`trigger_prices`+`triggered_at` (required, :482) + `scan_name` (optional, validated vs URL, :493). Ignores alert_name/scan_url/webhook_url but stores the whole body.

## NOTES (for Web Claude)
- Routes: `POST /webhook/<scanner_name>` (:268) + `GET /health` (:255).
- Token logging: app does NOT log the token — `_write_audit` stores source_ip only (:773-799); 400-handler logs body not URL (:383); waitress has no access log. BUT the token is persisted plaintext in `signals.webhook_payload` (the CRITICAL find above).
- PARITY: webhook ingress is mode-agnostic (one WEBHOOK_SECRET, both paper+live) — the eventual fix is one path for both.

Related: [[c2_webhook_lockdown_02jul]] · [[c2_chartink_ip_investigation_03jul]] · [[webhook_token_rotated_03jul]] · [[audit_phase9_10_ops_security_05jul]] (S-1). No repo/system changes made.
