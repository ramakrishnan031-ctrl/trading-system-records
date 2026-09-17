---
name: require-hmac-keep-false-20jul
description: "webhook require_hmac must stay FALSE — Chartink can't sign; enabling disables the ?token= fallback and kills the live signal path. \"De-risked\" (P1) meant the /health oracle ONLY, not safe-to-enable."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b14d1d0c-0ba5-4905-a624-c9bdc6af7245
  modified: 2026-07-20T07:41:42.396Z
---

**`webhook.require_hmac` must stay `false` in prod.** A VS-Code instruction (20-Jul, ~09:50 IST, LIVE market hours) to "enable require_hmac because it's already marked SAFE" was **REFUSED with evidence** — the "SAFE" premise is a misread of "de-risked".

**Enabling it would be a silent, S4-shaped outage** (verified against CURRENT code 20-Jul, not just memory):
- `config/system_config.yaml:212` — `require_hmac: false  # Chartink cannot sign payloads; use ?token= auth (WEBHOOK_SECRET required BOTH modes as of C-2)`. The signal source (Chartink) CANNOT produce HMAC signatures; prod webhook auth is `?token=`.
- `signals/webhook_receiver.py:166-169, 300-302` — when `require_hmac=True` the `?token=` fallback is **disabled**; HMAC becomes the sole accepted auth (codified by test `test_token_only_is_refused_when_require_hmac`).
- ⇒ `require_hmac=true` ⇒ every Chartink POST → 401 → **zero signals → zero trades**, cron exits 0, looks like a quiet day. Same failure *shape* as S4.
- Boot gate `webhook_receiver.py:146-151` (BL-18): `require_hmac=True` + empty `secret_token` ⇒ **ValueError at construction ⇒ app fails to boot**. So depending on whether `WEBHOOK_SECRET` is set on the VM, enabling either bricks the next boot OR 401s every POST — both outages.

**What "DE-RISKED" actually meant** ([[p1-health-require-hmac-17jul]], 17-Jul): P1 made `GET /health` honor `require_hmac` so a *future* flip wouldn't leave a `/health` `?token=` recon oracle open. That closed ONE secondary bug on the /health route. The note itself says "require_hmac is still false in prod, P1 is inert at runtime… the require_hmac decision stays a Rama action." **De-risked (the /health oracle) ≠ safe-to-enable (the signal path).**

The 0.0.0.0 all-interfaces bind's security concern (`system_config.yaml:204-210`) is already mitigated **without** HMAC: `?token=`/`WEBHOOK_SECRET` + firewall/security-group + per-IP rate limit (C-2).

**Why:** the "SAFE" label came from reading "de-risked" as "enable it"; the real operational blocker (Chartink can't sign) is unchanged, and the failure is silent.
**How to apply:** Do NOT enable `require_hmac` while Chartink is the signer. If HMAC is ever genuinely wanted it needs a signing proxy in front of the receiver + `WEBHOOK_SECRET` set + a webhook self-POST verification + rollback ready, done off-market through the careful loop — never a market-hours flip-and-push. Also: never commit/push during market hours (crontab reinstall on a live system).

Related: [[p1-health-require-hmac-17jul]] [[s4-boot-outage-17jul]] [[feedback-verify-the-finding-premise]] [[c2_webhook_lockdown_02jul]] [[feedback-webhook-flow-diagnosis]]
