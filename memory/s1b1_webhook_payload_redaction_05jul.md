---
name: s1b1_webhook_payload_redaction_05jul
description: "S-1B.1 DONE (05-Jul, commit 58ff1e7 unpushed) — webhook secret redacted going-forward from signals.webhook_payload; auth+parsing unchanged; scrub of history still pending"
metadata: 
  node_type: memory
  type: project
  originSessionId: 46720e02-4098-4c34-87c3-16d4cb5c52fa
---

**S-1B.1 FIXED** (commit `58ff1e7`, main, UNPUSHED — Rama pushes off-market; push = checkout only, no restart → receiver picks it up on next start; inactive now). Redact-going-forward so the webhook secret NEVER persists to `signals.webhook_payload`.

**Root cause:** `signals/webhook_receiver.py` persists the full raw body to `signals.webhook_payload`, and Chartink echoes the configured URL — incl. `?token=<SECRET>` — inside the body's `webhook_url` field → secret plaintext at rest (was 95,431/95,431 rows). See [[s1_webhook_verification_05jul]].

**Fix (storage-only):** new `_sanitize_payload_for_storage()`, computed ONCE before the per-symbol loop, passed as `webhook_payload` (replaces the inline `raw_body.decode(...)` at the old `:579`). Belt-and-suspenders on the stored string only: (a) replace literal `self._secret` anywhere; (b) regex `token=[^&"'\s]+`→`token=<REDACTED>`; (c) blank the `webhook_url` JSON value. `import re` added.

**Invariants held:** auth (`:410-432`) untouched (redaction is post-auth); parsing untouched — the parsed `body` (stocks/trigger_prices/triggered_at/scan_name, extracted before the loop) is never passed to the sanitizer, which only touches the INSERT string. Malformed-JSON→400 and auth-fail→401 return BEFORE `_process_signal`, so no other persist site. Audit fields (stocks/prices/triggered_at/scan_name) preserved in storage.

**Parity:** webhook ingress is mode-agnostic (one WEBHOOK_SECRET, one shared persist path); no paper-specific duplicate. One fix, both modes.

**Tests** (`tests/unit/test_webhook_receiver.py`, real StateStore + Flask test_client): `test_s1b1_secret_never_persists_to_webhook_payload` (core RED→GREEN: RED = stored payload contains secret+`token=<secret>`; GREEN = redacted, rows still created w/ correct stocks/prices; proven via revert) · `_parsing_unchanged_plain_payload` · `_auth_unchanged` (200/401) · `_secret_redacted_even_outside_webhook_url`. Full `test_webhook_receiver.py`+`test_c2_webhook_lockdown.py` = **69 pass**. NOTE: the pre-commit secret scanner blocked a credential-named test const → renamed `_S1B1_SECRET`→`_S1B1_FIXTURE` + `dummy`-prefixed placeholder value (redaction is value-agnostic).

**S-1 SEQUENCE STATUS:** S-1B.1 redact-going-forward ✓ (this) · S-1A ingress hardening (nginx+TLS+Flask→127.0.0.1+close public :5000) + `/32` Leaseweb-SG allowlist (`23.106.53.213`) + token rotation = PENDING · S-1B.2 scrub of the 95,431 historical rows + backups = PENDING. Residual: the token STILL travels in the URL (Chartink-inherent → S-1A allowlist+rotation); history/backups still hold the old secret until S-1B.2.

Related: [[s1_webhook_verification_05jul]] · [[audit_phase9_10_ops_security_05jul]] (S-1) · [[c2_webhook_lockdown_02jul]] · [[webhook_token_rotated_03jul]].
