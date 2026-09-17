---
name: s1a_webhook_allowlist_rotation_05jul
description: "S-1A (/32 webhook allowlist + token rotation) — CLOSED 06-Jul: GATE D PASS on live Monday first-signal e2e. A(redact 58ff1e7)+B(/32 allowlist 23.106.53.213)+C(rotation) all live-verified. Remaining: S-1B.2 history scrub + TLS (deferred)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 46720e02-4098-4c34-87c3-16d4cb5c52fa
---

**S-1A status: CLOSED ✅ 06-Jul-2026 — GATE D PASS on live Monday first-signal e2e (read-only verify, NO changes, no rollback). All three staged controls (A redact / B /32 allowlist / C rotation) confirmed on real Chartink traffic — see GATE D section below.** _(History:)_ Off-market runbook (allowlist :5000 to Chartink + rotate WEBHOOK_SECRET). I did read-only + authored exact commands; Rama ran the mutating steps after approval.

## GATE A = GO ✅ (re-verified 05-Jul, push landed)
Redact NOW DEPLOYED: bare-repo HEAD = `58ff1e7`; running `signals/webhook_receiver.py` has `_sanitize_payload_for_storage` (grep 2) + persist wired `webhook_payload=stored_payload` (line 591). Service = `inactive`/`Result=success`/`ExecMainStatus=0` = clean market-closed (NOT halted — acceptable Sunday state per the caveat); NOT restarted after push (ActiveEnterTimestamp still Fri 03-Jul) but doesn't need to be — the redact runs on next natural start (Mon session). **Rotation (GATE C) UNBLOCKED. GATE B (allowlist) next — nothing applied yet.** (History before the push: GATE A first failed because `58ff1e7` was unpushed; Rama then pushed all unpushed main commits incl. H-10 `ee9f993`.)

## FIREWALL FINDING (corrects the runbook's nft assumption)
Box is **iptables-nft**, persisted `/etc/iptables/rules.v4` via **netfilter-persistent** (enabled+active). `nftables.service` DISABLED; `/etc/nftables.conf` NOT used. Use `iptables` + `netfilter-persistent save`, NOT `nft`/`nftables.conf`. INPUT policy ACCEPT with catch-all `REJECT icmp-host-prohibited` at rule #7. Target = rule **#6** `-A INPUT -p tcp -m tcp --dport 5000 -j ACCEPT` (rules.v4 line 29), accepts :5000 from 0.0.0.0/0. ufw enabled-but-inactive; fail2ban active (own `f2b-table`); Tailscale ts-input chains.

## GATE B — allowlist APPLIED + VERIFIED ✅ (05-Jul, Rama ran STEP 2)
Runtime + persisted (`/etc/iptables/rules.v4` line 43): `-A INPUT -s 23.106.53.213/32 -p tcp -m tcp --dport 5000 -j ACCEPT` — ONLY the /32 accept, no bare :5000 accept; #6 before catch-all REJECT #7; SSH :22 intact. Snapshots kept: `~/rules.v4.bak-05jul` + `~/iptables-runtime-05jul.txt` (rollback: `sudo iptables-restore < ~/iptables-runtime-05jul.txt && sudo netfilter-persistent save`). Definitive Chartink reachability = GATE D (next signal). **:5000 is now Chartink-IP-only. GATE C (rotation) is next.**

### GATE B commands as authored (for reference)
Because REJECT #7 immediately follows #6, a single in-place REPLACE suffices (no explicit drop):
- SNAPSHOT: `sudo cp -a /etc/iptables/rules.v4 ~/rules.v4.bak-05jul` ; `sudo iptables-save | sudo tee ~/iptables-runtime-05jul.txt >/dev/null`
- PRE-CHECK: `sudo iptables -L INPUT --line-numbers -n | awk 'NR<=9'` → confirm #6=dpt:5000 ACCEPT, #7=REJECT
- APPLY: `sudo iptables -R INPUT 6 -s 23.106.53.213/32 -p tcp -m tcp --dport 5000 -j ACCEPT`
- VERIFY: `sudo iptables -S INPUT | grep -- '--dport 5000'` → only the `-s 23.106.53.213/32` line, no bare accept
- PERSIST: `sudo netfilter-persistent save` ; `sudo grep -n -- '--dport 5000' /etc/iptables/rules.v4`
- ROLLBACK fast: `sudo iptables -R INPUT 6 -p tcp -m tcp --dport 5000 -j ACCEPT && sudo netfilter-persistent save` ; full: `sudo iptables-restore < ~/iptables-runtime-05jul.txt`
Allowlist target `23.106.53.213` = Leaseweb SG, the SOLE Chartink source across 38,046 POSTs 12-Jun→03-Jul (stable) — see [[s1_webhook_verification_05jul]].

## GATE C — rotation STAGED for Monday (05-Jul; hashes only, raw secret never stored)
`.env WEBHOOK_SECRET` ROTATED by Rama: OLD sha256 `b7a4b7d4…1555b9ca` → NEW `484c43a9…716721b43` (differs ✅, 64-hex ✅). Redact still deployed (`58ff1e7`). Service left inactive-clean — **NO Sunday restart by design** (weekend no-token → new secret loads at Monday's natural start). Chartink URL updated by Rama (his URL-token sha256 must == `484c43a9…` — his confirm, I can't read Chartink). **C.4 other-location sweep (all reconciled):** (1) `.env` = sole EnvironmentFile, rotated✓; (2) Chartink = pending Rama hash-match; (3) code (main.py:2479, webhook_receiver, tests, crash_test injectors, premarket_healthcheck, preflight) ALL read `os.environ.get("WEBHOOK_SECRET")` → auto-consistent, no hardcoded value; (4) systemd = single `EnvironmentFile=.env`, drop-in dir only `watchman.conf` (no webhook shadow); (5) no cron token; (6) `.env.example` = `FILL_WHEN_READY` placeholder; (7) NO raw token literal anywhere in repo/docs (`token=[0-9a-f]{32,}` → 0 hits). **⚠️ STALE FILE:** `.env.pre-rotation-02jul.bak` (VM repo root) holds an even-OLDER secret sha256 `1dedac32…534af0db` (pre-02jul, ≠ old ≠ new) — NOT loaded, but a stale-secret-at-rest → **delete in S-1B.2**. **GATE C = STAGED (GO pending Rama's Chartink hash-match); activates Monday start; GATE D verifies at first signal.**

## GATE D — PASS ✅ (06-Jul-2026 ~10:05 IST, read-only live verify) → **S-1A CLOSED, no rollback**
Verified on Monday's REAL first signals (service up since the 08:15 natural start that loaded the new secret + redact):
- **D.1** — `trading-system.service` `active (running)` since 08:15:14 IST; `/health` ok (`kill_switch_active:false`; Fri SOFT_KILL auto-cleared new-day); bare-repo HEAD `58ff1e7` (redact deployed).
- **D.2 allowlist + new token** — today's `webhook_audit`: **86× 200 + 309× 403, ZERO 401**, ALL from `23.106.53.213`. Rows present from the Chartink IP ⇒ the `/32` allowlist (GATE B) permits Chartink (a netfilter block = zero rows); the 200s ⇒ the NEW `WEBHOOK_SECRET` authenticates.
- **D.3 old token dead** — passive proof, stronger than the active test: **0× 401** in live traffic ⇒ Chartink migrated to the NEW secret (any non-matching token, incl. the old, → 401 at `webhook_receiver.py:431`). The localhost old-token curl was NOT run (avoided during market hours, per runbook); available to Rama as optional belt-and-suspenders.
- **403 window = NORMAL, not a token issue** — 403 has only two sources (`:442` kill-switch / `:457` outside-entry-window); kill-switch was inactive (0 logged webhook rejections) ⇒ all 309 403s = "Outside entry window" (`trading_hours.entry_start: "10:00"` LAUNCH-PHASE gate). Last 403 `09:59:15` → first 200 `10:00:16` straddles 10:00 exactly. **Operational rule: only 401 = webhook auth/token failure; 403 = kill-switch OR pre-entry-window, NEVER the token.**
- **D.4 redact live** — today's 113 signals: **113 contain `<REDACTED>`, 0 contain `token=`**; the `webhook_url` echo (the leak vector) is redacted to `<REDACTED>`; secret not at rest going-forward. Sample parsed clean (`stocks`/`trigger_prices`/`triggered_at`/`scan_name`).
- **D.5 processed** — 113 ingested→parsed→pipelined to legit verdicts (`REJECTED_SIZING_CAPITAL` ×70 on the Rs 10k account, `REJECTED_SCORE_*` <60 floor, `REJECTED_CIRCUIT_PROXIMITY` ×5); **0 ERROR / 0 Traceback** (the 1 CRITICAL = benign 08:15 startup kill-switch, auto-cleared). No entries yet = capital/score-gated + early session = business outcome, not a fault. Service is `--mode live` (LIVE since 16-Jun); ingress verify is mode-agnostic.

**STOP/GO = GO. S-1A CLOSED.** Remaining (NOT started, per runbook — do not begin without a fresh directive): **S-1B.2** = scrub 95,431 historical `signals.webhook_payload` rows + regenerate backups + delete the stale `.env.pre-rotation-02jul.bak` (older dead secret `1dedac…`); **TLS** = deferred.

## Parity: webhook ingress mode-agnostic (one WEBHOOK_SECRET, both paper+live) — infra change affects both identically.
## S-1 sequence: S-1B.1 redact ✓ (committed `58ff1e7`, UNPUSHED) → **S-1A (this) AUTHORED/blocked** → S-1B.2 scrub 95,431 rows + backups (pending). Related: [[s1b1_webhook_payload_redaction_05jul]] · [[audit_phase9_10_ops_security_05jul]].
