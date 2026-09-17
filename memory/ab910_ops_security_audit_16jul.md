---
name: ab910-ops-security-audit-16jul
description: "16/17-Jul-2026 AB-910 — the missing Audit-B Phase 9 (Ops) + Phase 10 (Security), produced read-only. 5 HIGH; 2 NEW systemic finds (live Telegram token in logs; market_day_only unenforced on 20 jobs)."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
---

**AB-910 PRODUCED — the two Audit-B phases that never existed (`audit_05jul2026.md` ends at "Batch 5 running…").
READ-ONLY: nothing fixed, nothing changed, nothing pushed.** Report
`docs/audit/audit_b_phase9_ops_phase10_security_16jul2026.md` (docs-only commit, UNPUSHED).
Baseline PC==VM==`6969599`. **No secret value is in the report** — seeds compared by SHA-256, configs
classified by shape, log hits counted, the one quoted line redacted.

**COUNTS: Security 3 HIGH · 5 MED · 1 LOW · Ops 2 HIGH · 3 MED · 1 LOW. NO CRITICAL** — nothing presently
exploitable from the internet without a prior compromise.

**🔴 THE TWO NEW SYSTEMIC FINDS (nobody had these on a list):**
1. **[HIGH] The LIVE Telegram bot token is written to logs in CLEARTEXT — 984 lines, 10 files,
   `debug_2026-07-03` → `debug_2026-07-16` (ONGOING TODAY).** Emitter = **`urllib3.connectionpool` at DEBUG**
   — *our code never prints it*; **Telegram puts the credential in the URL PATH**
   (`"POST /bot<TOKEN>/sendMessage"`), and `core/logger.py:373`+`:409` sink ALL loggers at DEBUG. Verified
   real: literal match vs `.env`, 46 chars, canonical `digits:base64ish`. **Impact: an attacker with the token
   can SEND messages that look exactly like the system's own alerts** — forging "✅ all clear" beats silencing.
   Fix: raise urllib3 to INFO / redaction filter, then purge the 10 files; treat as compromised-at-rest.
   **BATCH-safe** (logging config).
2. **[HIGH] `market_day_only` is DECORATIVE on 20 of 25 scripts.** 30 jobs declare it;
   `core/cron_registry.py:75` defines it, `generate_crontab.py` copies it, **NOTHING enforces it**; the crontab
   (`* * 1-5`) excludes weekends only. **Only 5 self-guard** (daily_trade_review [batch-1], cron_officer,
   fetch_daily_candles, reconcile_positions, system_manager). **20 UNGUARDED** incl. eod_verify,
   eod_broker_reconcile, eod_cleanup, trade_journal, refresh_instruments and **4× gemini (paid API calls)** —
   all run on every mid-week NSE holiday. Batch-1 fixed ONE; this is the systemic version. Fix: enforce
   CENTRALLY (crontab wrapper or a cron_heartbeat decorator), not 20 copies; the correct skip is
   `SUCCESS` + `functional_status=SKIPPED`. **LOOP.**

**CONFIRMED (with calibration that matters):**
- **[HIGH] The live PROD 2FA seed is in the PC dev tree** — `gui_config.local.yaml` PC seed
  **sha256 == VM seed sha256** (`831323f7889ca9f1`). Both factors (password_hash + seed) on one box ⇒ **2FA
  adds nothing against a PC compromise** — the main scenario. Fix = regenerate VM-only + re-enrol. **Rama.**
- **[HIGH] Fail-open 2FA is LATENT, NOT LIVE** (`auth.py:62-64` `if not secret: return True`; `:120` defaults
  to `""`). **Why not live:** the VM has a real seed, and the TRACKED `gui_config.yaml` carries **prose
  placeholders** (contain spaces ⇒ non-base32 ⇒ pyotp RAISES ⇒ returns False) ⇒ **the shipped default fails
  CLOSED**. It fires only if the key is emptied/missing. Fix = invert to fail-closed. **LOOP/Rama** (a careless
  fix locks Rama out — that is why it was LOOP, not because it is low-value).
- **[HIGH] S2 backups have NO independent failure domain** — live DB **and all 33 backups (5.5GB) on
  `/dev/sda1`**, **no other mounts**, nothing offsite. Protects against logical loss ONLY; one disk/VM loss
  destroys system + every backup together. **Rama — BLOCKED on provisioning a target.**
- [MED] **rpcbind `0.0.0.0:111` enabled+active with 0 NFS mounts** = pure attack surface + UDP amplification
  vector (C5). · [MED] **SSH on `0.0.0.0:22` while Tailscale already works** (GUI is Tailscale-only
  `100.74.84.44:443`) — **bounded to MED because `sshd -T` is key-only** (`passwordauthentication no`,
  `permitrootlogin no`, no empty passwords): **that is WHY the July bot got 0 successes.** Do C1 re-baseline
  BEFORE C2. · [MED] username-keyed lockout DoS (`auth.py:98-102`) — locks the operator out mid-market ·
  [MED] `/health` unauth, discloses `kill_switch_active`+queue depth on `0.0.0.0:5000` (**dormant now — the
  engine is halted; returns at the 08:15 boot**) · [MED] `require_hmac:false` (accepted, Rama) ·
  [LOW] the C1 8-char token prefix persists in `cron-candle-fetch.log` (batch-1 stopped future writes).
- [MED] **Logs 1.1GB / 132 files / oldest 15-Jun, no retention** — same disk as DB+backups, and §1.1 means
  they currently hold a live credential. · [MED] **stale `deploy/post-receive` (md5 `604d2b37`, May-16) is
  DEAD** — the live hook is `deploy/hooks/post-receive` (`bd950b7b`, md5-proven); a dead file on the DEPLOY
  path is a trap. **BATCH** (identity now proven; X4's LOOP tag can drop). · [MED] Q10 functional-criterion
  tail (~20 jobs EXECUTION-only = the "green while broken" class).

**✅ CLEAN, stated because "we checked" is a finding:** NO injection (only a static `__import__` idiom; raw
f-string SQL confined to `core/migrations.py` internal table names; webhook inserts parameterised) ·
**`WEBHOOK_SECRET` 0 hits · `ALERT_SMTP_PASSWORD` 0 hits · full access_token 0 hits** in logs · no real
credential tracked in git (repo = prose placeholders; `credentials.xlsx` **absent from the PC** ⇒ NR-2 looks
done) · **M-K5 fixed+deployed** · SSH properly configured · GUI Tailscale-only · **deploy/rollback is the
best-run part of the system** (tag-as-code-identity caught a stale SHA twice today; migration guard; 3
rollback levels).

**⚠️ METHOD NOTE worth keeping:** a naive "long alphanumeric" grep over `logs/` returned **433,305 hits** —
order IDs, hashes, tracebacks: **noise, not evidence.** §1.1 stands on a **literal match against the actual
`.env` value**. Do not report a pattern count as a secret leak. [[verify-check-the-rc-not-the-output]]

**⏰ RANKED QUEUE THIS FEEDS:** 1 Telegram token (BATCH+rotate?) · 2 prod seed in dev tree (Rama) · 3 backups
one disk (Rama, blocked) · 4 market_day_only central enforcement (LOOP) · 5 fail-open 2FA (LOOP/Rama) ·
6 rpcbind (Rama) · 7 SSH→Tailscale, C1 first (Rama) · 8 lockout DoS + /health (LOOP) · 9 log retention +
stale post-receive + token residue (BATCH) · 10 functional tail (LOOP).

See [[batch1-done-16jul]] [[batch-classification-16jul]] [[pending-register-16jul]] [[deploy-batch1-done-16jul]]
</content>
