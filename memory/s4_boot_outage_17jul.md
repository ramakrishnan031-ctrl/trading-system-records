---
name: s4-boot-outage-17jul
description: "S4's authenticated /health halted the system at boot 17-Jul — a live self-inflicted outage, 0 trades on a trading day. Fixed + deployed. Both sides' tests were green; the seam was untested, and every wired fixture uses secret_token=None so the 401 CANNOT occur in the suite."
metadata:
  node_type: memory
  type: project
  originSessionId: 8ce14ca5-df4a-451f-aa35-493d91436ae9
---

**🔴 S4 HALTED THE SYSTEM AT BOOT — a LIVE, self-inflicted outage. FIXED + DEPLOYED 17-Jul
(`e393b3f`, in tag `deploy-17jul-s4-p3s14`).** Report `docs/audit/s4_boot_outage_17jul2026.md`.

## What happened
**0 trades on a live trading day** (13-Jul=9 · 14-Jul=9 · 15-Jul=7 · 16-Jul=3 · **17-Jul=0**;
17-Jul was NOT a holiday). The system booted 08:15:51, auto-cleared the prior-day kill
(correct), and **shut itself down at 08:16:09** — clean **exit 0**.

**The chain:** S4 (`84cee3e`, deployed ~02:00) put `/health` behind the webhook secret
(AB-910 §1.7) — *correct* — but `main.py:3238`'s post-start self-check GETs that same
`/health` **unauthenticated** (unchanged since `bcf03b5`) ⇒ **401** ⇒
`startup_checks.py:797` counted only **2xx** as reachable ⇒ `main.py:3242`
**`_shutdown_event.set()`** ⇒ whole system down.

## The fix
**A 401 PROVES Flask is listening** — the only thing the check exists to prove (its own
docstring: *"to confirm Flask is listening"*) ⇒ `reachable = 2xx **or 401**`.
**5xx/404/429/no-answer still fail the boot** (guard test pins it); **S4's security property
is fully preserved** (`/health` still denies anonymous callers).
**Rejected:** token-in-URL (`main.py:3241` **logs** that URL ⇒ re-opens the token-at-rest leak
the sweep just closed) · loopback-exempt (behind Tailscale **every** caller is 127.0.0.1 —
the S3 lesson ⇒ silently disables the auth).

## ⭐⭐ THE LESSONS (the durable part)
1. **Both sides were tested, correct, and GREEN — the defect lived in the SEAM neither
   owned.** S4's tests: "/health 401s anonymous callers" ✅. The boot check's tests: "2xx →
   reachable" ✅. Unit tests on each side of a seam can both pass while the seam is broken.
2. **⭐ SYSTEMIC: every wired fixture builds the receiver with `secret_token=None`**
   (`tests/integration/conftest.py:332`) ⇒ S4's `if receiver._secret:` branch **never executes
   anywhere in the suite** ⇒ the 401 that took prod down **cannot occur in any test**. The
   suite was green because it is configured **unlike production**. ANY future defect in an
   auth branch is invisible the same way. **→ loop: should the wired fixture default to a
   secret, as prod does?**
3. **⭐ NOTHING ALARMED — the canary reported HEALTHY.** `canary_service_state.json` @
   08:20:05 (4 min after death) = **`{"nrestarts": 0}`** — it watches for a **restart loop**,
   not **liveness**, so a cleanly-dead service scores the *good* value. 5 CRITICALs were
   delivered today; **none** mentions the boot/webhook. **A clean exit 0 + 0 restarts is
   indistinguishable from a healthy system.** → **loop/Rama: add a "should be up during the
   service window but isn't" check.**
4. **⚠️ `_shutdown_event.set()` on one non-2xx from one local endpoint costs a whole trading
   day, behind an exit 0 that looks like a normal stop.** Worth asking whether that check
   should block the boot at all. → **decision, Rama.**
5. **FOUND BY VERIFYING A PREMISE, NOT BY AN ALARM.** The P3-s14 instruction said *"System
   DOWN today"* as a given — **true, but the author meant the planned pause**, while memory
   expected it to RESUME ([[sweep-done-17jul]]). Checking the VM instead of accepting the
   premise is the only reason it was found. Mirror of [[feedback-verify-the-finding-premise]].

## Verified on the VM with the DEPLOYED code
Replaying the exact 401 the live system produced at 08:16:04 into the deployed check:
**401 → reachable=True** (was False ⇒ the halt); 500/404/429/refused → **False** (guard holds).
**⇒ the boot proceeds past `main.py:3242`.**
**⚠️ RESIDUAL RISK: the boot region AFTER the webhook check is unverified on this code** — the
only boot on sweep+batch-3 died at 08:16:04. It is materially unchanged from 16-Jul's
successful boot (X5's lock is earlier and passed; X7 is async observability; S2/S6/S7 aren't
in that path), but **Monday 20-Jul 08:15 is the first real proof**.

Related: [[p3s14-done-17jul]] [[sweep-done-17jul]] [[ab910-ops-security-audit-16jul]]
[[feedback-verify-the-finding-premise]] [[feedback-verify-rc-not-output]]
[[pc-test-env-hygiene]]
