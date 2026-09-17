---
name: c2_webhook_lockdown_02jul
description: "C-2 HIGH remediation — webhook paper-parity secret + per-IP rate limit DONE (committed); network-layer option (A vs B) is Rama's pick"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3e62fe89-aead-435f-8580-0a242667edcc
---

Remediation of audit finding **C-2** (webhook binds 0.0.0.0 + require_hmac:false; paper could run unauthenticated). Follows [[system_audit_02jul]]. Stacked on [[c1_secret_remediation_02jul]].

**PHASE 1 — VERIFIED (source + live VM):** bind_host `0.0.0.0`, require_hmac `false`, port 5000 (matches audit). Both **:5000 (webhook) and :8080 (healthcheck) LISTEN on 0.0.0.0** on the VM. **NO reverse proxy** (nginx/caddy/haproxy/apache/traefik all absent) → Waitress serves :5000 directly, plaintext. Auth: `webhook_receiver._process_request` gates the whole check behind `if self._secret:` → falsy secret = NO auth; `main.py` appended WEBHOOK_SECRET to required-secrets only `if not is_paper` → paper unauthenticated if unset (parity defect). **Chartink egress IPs NOT known-static** (repo docs: "mitigated by Oracle SG + iptables"; "no per-IP throttle; Chartink bursts from one IP") — Option A depends on obtaining them from Chartink.

**PHASE 2 — CODE HARDENING DONE + COMMITTED.** Branch `fix-c2-webhook-lockdown-02jul` @ `d922007` (stacked on C-1 `7bc3367`; **UNPUSHED**; Rama pushes off-market). Both modes, permanent, tested:
- **Paper-parity:** NEW `main.required_startup_secrets(primary_id)` ALWAYS includes WEBHOOK_SECRET (both modes) → replaced the `if not is_paper:` exemption. Startup fails fast if unset → the webhook is never unauthenticated in any mode. (Note: paper operators must now include `?token=` when POSTing test payloads.)
- **Per-IP rate limit:** NEW `_PerIpRateLimiter` (token bucket) in `signals/webhook_receiver.py`, wired in `_handle_webhook` (keyed on `request.remote_addr`, before auth/parse/queue) → 429 on exceed. Burst-tolerant (absorbs Chartink's ~40 open-bell burst). Config `WebhookConfig.per_ip_{rate_limit_enabled(true),burst(60),refill_per_sec(5.0)}` + system_config.yaml. Idle buckets evicted on idle-TIME (not token count — first cut had that bug, fixed). `now` injectable → deterministic tests.
- Tests: `tests/unit/test_c2_webhook_lockdown.py` (8: limiter burst/refill/per-IP/eviction/Chartink-burst + config defaults/validators + required-secrets parity). Throughput test `test_performance_100_posts_under_5_seconds` now disables the limiter (raw-latency test). Regression: test_webhook_receiver 57, config_loader 42, startup_checks+config_auditor 98 — all green; real `load_all()` OK (per_ip True/60/5.0).
- **Scanner fix folded into C-1** (`7bc3367`, was 80da5e6): `deploy/hooks/secret_scan.py` now decodes git output as UTF-8 (Windows `text=True`=cp1252 crashed on em-dashes/arrows). fix-c1 branch realigned to 7bc3367.

**PHASE 3 — NETWORK OPTIONS (Rama decides; NOT executed):**
- **Option A — IP allowlist** (Oracle SG + iptables restrict :5000 to Chartink IPs; keep rotated token). Low friction, no new component. **Depends on Chartink publishing STATIC egress IPs** — verify with Chartink support FIRST; if they drift, legit signals silently drop (missed trades). Rollback: revert SG/iptables rule. No app restart/code.
- **Option B — reverse proxy** (bind webhook 127.0.0.1 + Caddy [auto-TLS, minimal config] → localhost:5000, + IP allowlist and/or proxy-signed HMAC). Defense-in-depth; removes plaintext + all-interfaces exposure regardless of Chartink IPs. Friction: new component + cert + `bind_host`→127.0.0.1 (app restart) + repoint Chartink to https. Rollback: stop caddy, revert bind_host, restart, repoint to http.
- **RECOMMENDATION:** Option A **iff** Chartink egress IPs are static (confirm with them); **else Option B with Caddy**. EITHER WAY also do the C-3 quick win — bind **:8080 healthcheck to 127.0.0.1** (it currently leaks P&L/capital/kill-state on 0.0.0.0), independent of the webhook choice.
- **Test plan:** A → non-allowlisted IP POST refused at SG; allowlisted/token → 200; watch webhook_audit received-count next session for drops. B → https+token → 200, http refused, direct :5000 external refused (localhost-bound), cert valid.

**Execution order (overall C-2):** (1) [DONE] Phase-2 code — Rama pushes off-market; (2) [Rama] rotate WEBHOOK_SECRET (rides the C-1 rotation); (3) [Rama] pick Phase-3 A/B after verifying Chartink IPs; (4) quick win: bind :8080 to localhost (C-3).

**Why:** the audit's sole-live-auth (`?token=`) rested on a private firewall + a committed secret. Phase-2 closes the paper-parity hole + caps per-IP flooding in code (permanent, both modes); the real network control is Rama's infra call, framed with trade-offs. NOTE: the whole webhook path stays HTTP/`require_hmac:false` until Phase 3 — Phase 2 is necessary, not sufficient.
