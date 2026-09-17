---
name: p1-health-require-hmac-17jul
description: "P1 DONE + DEPLOYED 17-Jul — GET /health now honours require_hmac (mirrors /webhook); pre-arms Rama's require_hmac flip so it can no longer open the /health token oracle. + P2/P3/P4 test-infra."
metadata: 
  node_type: memory
  type: project
  originSessionId: 26214a92-ac1b-4507-998c-ca000415a4c5
  modified: 2026-07-20T08:12:47.797Z
---

# P1 — /health honours require_hmac — DONE + DEPLOYED 17-Jul-2026

Report `docs/audit/p1_health_require_hmac_done_17jul2026.md`. Closes the one real gap from the
fixture-blindness investigation ([[fixture-blindness-17jul]]). **PC == VM bare == `2b10b5e`**;
code tag **`deploy-17jul-p1-health-hmac`** (`4c340c6` → **`695aa84`**, delta tag..HEAD = markdown
only). Backup `data_store/backups/pre_deploy_p1_health_hmac_20260717_211747.db` (quick_check ok, v44).

## The fix (P1, `6e2a826`) — mirrors /webhook, adds no new idiom
`signals/webhook_receiver.py` `GET /health` gained `elif receiver._require_hmac: ok = False`,
positioned exactly like `/webhook`'s `elif self._require_hmac` (`_handle_webhook`). Under
`require_hmac=True` a token-only `/health` now falls through to the existing shared 401 instead of
the token branch; a valid HMAC still 200s; the no-credential 401 is unchanged. The 401 body stays
**uniform** (`"authentication required"`) — a distinct message would leak `require_hmac`-on to an
anonymous caller, the very oracle this route must not have. Uses the `_require_hmac` the ctor
already resolved (no 2nd config read); no config/schema change. **Parity-free** — the receiver has
zero mode refs, so it holds for paper == live (confirmed by grep).

## ⭐ WHAT THIS MEANS FOR RAMA'S require_hmac ACTION
`require_hmac` is still `false` in prod, so P1 is **inert at runtime today** — the deploy is
behaviour-neutral. **The point: flipping `require_hmac` no longer CREATES a bug.** Before P1, the
flip would have hardened `/webhook` while silently leaving `/health`'s `?token=` oracle open
(200 + `kill_switch_active` + `queue_depth`, the AB-910 §1.7 recon oracle). That flip is now safe
on both routes. The "`require_hmac` decision" stays a Rama action, but it is de-risked.

**⚠️ CORRECTION 20-Jul-2026:** "safe on both routes" means safe *from the `/health` token-oracle bug ONLY* —
it does **NOT** mean safe-to-enable. Chartink cannot sign HMAC, and `require_hmac=true` disables the
`?token=` fallback → every Chartink POST 401s → **zero signals** (boot `ValueError` if no `WEBHOOK_SECRET`).
`require_hmac` **STAYS FALSE**. P1 pre-armed the *receiver*; it did not give Chartink the ability to sign.
See [[require-hmac-keep-false-20jul]] and `docs/audit/pre_receive_hook_investigation_20jul2026.md` §D.

## Proofs (both green)
- **RED-on-old** — proven twice: (1) isolated `git checkout HEAD -- webhook_receiver.py` → the
  fix-test asserts 401, got 200 on old code; (2) **full-suite** — the base tree had 44 failures =
  the 43 env failures + my `test_token_only_is_refused_when_require_hmac` failing (token-only→200);
  my tree had 43 (it passes). The fix-test could only pass because the fix is present.
- **S4 SEAM-UNCHANGED** (`TestS4SeamUnchangedByP1`) — the unauthenticated `/health` (as
  `main.py:3238` calls it) is a byte-identical 401 under BOTH require_hmac settings, and the real
  `check_webhook_endpoint` still maps it `reachable=True`. If it ever goes red, P1 re-created S4.

## P2/P3/P4
- **P2** (`7e101aa`) — `wired_system_authenticated` fixture in `tests/integration/conftest.py`
  (secret-configured sibling of `wired_system`; both delegate to one `_build_wired_system`
  generator, teardown in `finally`). `SystemContext.webhook_secret` added. The S4 wired test now
  drives `ctx.receiver` instead of hand-building one. It was the ONLY auth-off default with no ON
  variant (`conftest.py:332`) — now it has one.
- **P3** (`f10b2f1`) — `test_every_non_exempt_route_denies_anonymous` walks `app.url_map`: every
  endpoint ∉ `_LOGIN_EXEMPT` must deny anon (`/api/*`→401 else→302). Covers **37** routes incl. the
  Flask `static` endpoint + `/logout` (the manual lists missed both). `checked>=15` floor guards it.
  A new blueprint can no longer skip auth coverage by omission.
- **P4** (`695aa84`) — comments: BL-18 block = constructor-only; `TestHealthAuth` = require_hmac=False
  throughout — each pointing at where the real request-time / require_hmac coverage lives.

## Regression — ZERO attributable
Full suite (unit+integration+core), ~20:40 IST outside window: **43 failed / 4842 passed / 3 skip**.
True pre-change tree: **44 failed** — the ONLY set-diff is my own fix-test (fails on base, passes on
mine). The 43 env failures are byte-identical base-vs-mine ([[pc-test-env-hygiene]] categories:
test_main ×26 · test_fix135 ×6 · test_order_placer_fix061 ×4 · test_fix129 ×2 · test_instance_lock
×2 · test_fix181 ×1 · test_interactive_startup ×1 · test_phase17_batch2 ×1). All my added/edited
tests PASS. Dashboard venv: **369 passed**. `test_gui_secret_key.py` `--ignore`d in main venv
(imports pyotp → lives in `ops_dashboard/.venv`; pre-existing cross-venv split).

## STRUCTURAL note (NOT done — a separate Rama LOOP decision)
The bug existed because the receiver implements auth **twice, per route** (`/health` + `/webhook`
each own a block) and they drifted. The dashboard implements it **once, globally**
(`app.py:169 before_request`) and cannot drift. A single-global-auth refactor of the receiver is the
real preventative — but it is a refactor of the live signal entry path ⇒ a **LOOP decision for
Rama**. **P1 is independent of it** and closes the concrete gap now.

## Observed during deploy (pre-existing, not mine)
`security-watcher.service` is `activating/auto-restart` (Type=simple, run-a-pass-and-exit,
NRestarts~19977, ExecMainStatus=0, "0 new alerts") — the SAME respawn pattern alert-watcher had
before its 16-Jul `--loop` fix. Functional; a hygiene candidate for the same treatment. Untouched by
this deploy.

Related: [[fixture-blindness-17jul]] · [[s4-boot-outage-17jul]] · [[ab910-ops-security-audit-16jul]] · [[liveness-alarm-17jul]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 489 B (budget 300 B). The index now carries a hook and this link.

- ✅🔒🚀 **[P1 DONE + DEPLOYED 17-Jul — `/health` honours `require_hmac`](p1_health_require_hmac_17jul.md)** — mirrors `/webhook`; token-only `/health` now 401s under `require_hmac=True`. **⭐ INERT until Rama flips `require_hmac` — the flip no longer opens the `/health` `?token=` oracle.** Fixed the one gap from the (stale-premise) fixture-blindness scoping [[fixture-blindness-17jul]]. P2 wired-fixture · P3 route-map guard · P4 comments. [[p1-health-require-hmac-17jul]]
