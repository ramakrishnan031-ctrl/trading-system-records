---
name: fixture-blindness-17jul
description: "Fixture-blindness scoped 17-Jul (READ-ONLY) — the premise was STALE (10 of 11 auth surfaces ARE tested); found ONE runtime-proven latent bug: /health ignores require_hmac"
metadata: 
  node_type: memory
  type: project
  originSessionId: 26214a92-ac1b-4507-998c-ca000415a4c5
---

# Fixture blindness — SCOPED 17-Jul-2026 (READ-ONLY, nothing changed, nothing pushed)

Report: `docs/audit/fixture_blindness_investigation_17jul2026.md` · base `5e74b9d` · docs-only commit.

## THE STEER: neither "small fix" nor "wide sweep" — the premise was STALE

**Of 11 security-gated surfaces, 10 have their secured branch TESTED. There is nothing to sweep.**
The build is SMALLER than the instruction's "small": one ~3-line prod fix + 2 tests + 1 fixture.

### 3 instruction premises were WRONG — corrected with evidence
1. ❌ *"every wired fixture is `secret_token=None` ⇒ S4's auth branch never executes"* — **FALSE.**
   `test_fix134_backpressure.py:151` `_make_receiver_with_secret()` builds auth-ON and drives
   `/health` (6 tests, `:170-214`). `test_webhook_receiver.py:288/300/319/341` cover HMAC 401/401/200/200.
2. ❌ *"the 401 cannot occur in any test"* — **FALSE/STALE.** `test_hardening_scenarios.py:298-331`
   (added BY the S4 fix) builds `secret_token="a-prod-like-secret"`, asserts a real 401, feeds the
   real `check_webhook_endpoint`.
3. ✅ Q2 *"the seam was untested"* — **now COVERED.** `test_startup_checks.py:768` (401→reachable)
   + `:789` (5xx/404/429 still unreachable = anti-over-widening) + the wired test above.

**Where the overreach came from:** the original S4 report + `test_hardening_scenarios.py:26-27`
scoped it correctly to the **wired/integration** suite ("anywhere else *in this suite*"). Memory
compressed that to "SYSTEMIC"; the instruction expanded it to "any test". The unit suite refutes it.
**The blindness was never "auth never executes" — it was "auth-ON never met the boot self-check".**
Mirror of [[feedback-verify-the-finding-premise]].

## 🔴 THE FIND: `GET /health` does NOT honour `require_hmac` — RUNTIME-PROVEN, latent

`webhook_receiver.py:290-304` (`/health`) **never reads `_require_hmac`**. Its ONLY request-time
site is `:469`, on `/webhook`. So the contract stated at `:165-168` — *"When True the token-param
fallback is disabled — HMAC is the sole accepted auth surface"* — holds for `/webhook` and
**silently breaks on `/health`**, the route deliberately exposed on `0.0.0.0:5000`.

**PROVEN by probe, with a control that could have failed it:**
```
require_hmac=True + secret:
  CONTROL  POST /webhook?token=<secret> -> 401  "token param is not accepted"   ← G.1 works
  SUBJECT  GET  /health?token=<secret>  -> 200  {"kill_switch_active": false, "queue_depth": "0/20"}
```
The 200 body IS the point: it returns **exactly the "is the system halted / how loaded" oracle**
AB-910 §1.7 + the comment at `:273-281` exist to close.

- **LATENT, not live** — `require_hmac: false` today ⇒ both routes agree.
- **⚠️ IT ARMS THE MOMENT RAMA FLIPS `require_hmac`** — an OPEN Rama-action on the owed list.
  A bug *scheduled to be created* by a change already on the board.
- **Same shape as S4** ([[s4-boot-outage-17jul]]): two green + correct suites (G.1 owns
  `require_hmac` on `/webhook`; TestHealthAuth owns auth on `/health`), bug in the cell neither owns.
- **Root cause:** auth implemented **TWICE, per-route** (`:290-304` and `:459-479`) and drifted.
  The dashboard implements it **ONCE globally** (`app.py:169` `before_request`, exempt set of 2)
  and *cannot* drift — a forgotten decorator is structurally impossible there.
- Design note (not a defect): `/health`'s HMAC is over `b""` ⇒ a **constant** per secret = a bearer
  token in a header. Its edge over `?token=` is only "not in the URL" — which is still the AB-910
  §1.1 leak class, so P1 is worth doing; just don't claim "/health is cryptographically weak".

## ⚠️ FALSE CONFIDENCE (the tests that look like coverage and aren't)
- **`TestHealthAuth`, 6 tests** (`test_fix134_backpressure.py:166-214`) — ALL run
  `require_hmac=False`, because `_make_config()` (`:35-48`) **omits `webhook` entirely** ⇒
  `getattr(_webhook_cfg, "require_hmac", False)` → False. Green, and blind to the find. **The most
  misleading set in the suite — it is *the* S4-shaped test.**
- **BL-18, 5 tests** (`test_webhook_receiver.py:1137-1180`) — **constructor-only**. Delete
  request-time enforcement (`:469`) entirely and all 5 still pass. (G.1's 4 tests at `:1201-1280`
  DO cover request-time — but they POST to `/webhook` only, never GET `/health`.)
- Compensated (note, don't convert): `tests/integration/conftest.py:332` wired fixture is auth-off;
  `ops_dashboard/tests/conftest.py:617` `client` pre-seeds `sess["user"]` — but
  `test_api_contract.py:90-103` proves default-deny with a separate `anon` client (8 APIs → 401,
  7 pages → 302). `ops_dashboard/tests/conftest.py:600-603` has **empty** `password_hash`/`totp_secret`
  ⇒ **no test using the shared `gui_config` can ever perform a real login** (`auth.py:226` returns
  "Auth not configured").

## FIXTURE ROOT = SHARED, one line per domain (Q4)
Auth-ON variants ALREADY exist for unit-webhook and unit-/health and the dashboard. **The ONLY
domain with no auth-ON variant is the wired fixture — `tests/integration/conftest.py:332`.**
The S4 test hand-builds its own receiver (`test_hardening_scenarios.py:308-312`) instead of using
the fixture — **that hand-build is the tell.**

## RECOMMENDED BUILD — ✅ ALL DONE + DEPLOYED 17-Jul ([[p1-health-require-hmac-17jul]])
- **P1 (LOOP)** ✅ `6e2a826` — `/health` honours `require_hmac` (mirrors `/webhook`). RED-on-old
  proven twice (isolated + full-suite: base=44 fails incl. my fix-test, mine=43). S4 seam proof green.
- **P2** ✅ `7e101aa` — `wired_system_authenticated` fixture; S4 test uses it, not a hand-built receiver.
- **P3** ✅ `f10b2f1` — route-map guard invariant (37 routes incl. static + /logout).
- **P4** ✅ `695aa84` — comments (BL-18 constructor-only; TestHealthAuth require_hmac=False).
- **DEPLOYED:** tag `deploy-17jul-p1-health-hmac`→`695aa84`; PC==VM==`2b10b5e`; inert until Rama
  flips `require_hmac` (that flip is now SAFE on both routes). **NOT a sweep** — the structural
  single-global-auth refactor stays a Rama LOOP decision; P1 was independent of it.

Related: [[s4-boot-outage-17jul]] · [[ab910-ops-security-audit-16jul]] · [[feedback-verify-the-finding-premise]] · [[feedback-verify-rc-not-output]]
