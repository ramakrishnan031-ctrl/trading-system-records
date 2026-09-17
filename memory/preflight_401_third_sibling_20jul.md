---
name: preflight-401-third-sibling-20jul
description: "The S4 /health 401 misread has a THIRD site — scripts/preflight/checks/signals.py:28 — and it is LIVE, firing a false CRITICAL every trading day. The queued startup_checks.py:703 item is REFUSED: it hits external chartink.com URLs where 401 is NOT expected."
metadata: 
  node_type: memory
  type: project
  originSessionId: cc7e4afb-c67e-4eb3-8fc7-ff345f73333a
  modified: 2026-07-20T13:26:40.000Z
---

Design (DESIGN ONLY, awaiting **ChatGPT review** before any implementation):
`docs/audit/boot_path_pair_design_20jul2026.md`, commit `a47bc87`. **The queued "boot-path pair" was not the
right pair.**

**🔴 NEW + LIVE — `scripts/preflight/checks/signals.py:26-33` (`webhook_responsive`).** Calls the **same**
endpoint as the S4 fix (`127.0.0.1:5000/health`), **unauthenticated**, and accepts **only `status == 200`**
⇒ since AB-910 §1.7 (`84cee3e`) put `/health` behind the webhook secret, it now returns 401 and preflight
Phase C fires a **CRITICAL_FAILURE + Telegram at ~09:19 on a perfectly healthy webhook** (20-Jul: 2,572 ×
HTTP 200, 1,028 scored, 4 trades). Proven from `logs/preflight.log`: **PASS 30-Jun…16-Jul (13 days) → 17-Jul
FAIL "Connection refused" (that one was real, S4) → 20-Jul FAIL "HTTP 401" (new).** 20-Jul was simply the
first trading day since AB-910. **Recurs daily.** Harm is **alert fatigue + a corrupted oracle** (Phase C
pinned at 33% readiness), NOT trading — preflight is a cron and gates nothing. Fix = one line,
`if status == 200 or status == 401`, modelled on `utils/startup_checks.py:807-808`, rendering the code in the
pass message. ⚠️ **Do NOT lower `criticality` to WARN** — fix the predicate, keep the severity; and keep the
`status == 0` test (that is the true S4 signature).

**⛔ REFUSED with evidence — `utils/startup_checks.py:703` ("add the `== 401` tolerance").** Premise
defective. `check_scanner_connectivity` does **not** call `/health`; via `_resolve_url` →
`config/chartink_scanners.yaml` it calls **external public `https://chartink.com/screener/*` pages**, where
nothing is behind a secret and a 401 is an anomaly, not an expected answer. Tolerating it would turn a
correct check into a silently-permissive one — **the S4 shape pointed the other way**. Measured: Monday's
boot logged `run_all_startup_checks: OK warnings=[]`, so those URLs answer 2xx; **the line is correct as
written — leave it alone.** ✅ The item's *other* half stands as a standing constraint: **`scanner_unreachable`
must stay a WARNING** (escalating it would manufacture an S4-class risk where none exists).

**B1 live-seed extraction (`main.py:2255-2258`) — design ready.** Module-level
`compute_live_startup_capital(broker_adapter, fund_manager)` **kept inside `main.py`**, because the existing
structural pin (`tests/integration/test_q9_post_restart_capital_wired.py:667-674`) is a **whole-file regex**
over `main.py` ⇒ keeping the two-line expression there leaves it green with **zero test edits**; and `main.py`
is import-safe (all execution under `__main__`; precedent `tests/unit/test_fix164…:26` already imports from
it). Payoff: `test_q9_live_seed_mc1_wired.py:123-126` currently **reimplements** the seed, so 4 downstream
tests validate a *copy* — they would then exercise production code with no new assertions. ⚠️ Sequencing:
**B2′ first** (zero blast radius), **B1 alone in a dedicated off-market window**; a wrong seed does not crash,
it drifts silently — the acceptance test in production is the boot's
`fund_manager.rehydrate_complete → total` (Monday: 9,875.60 exactly). Stale line refs to sweep:
`test_mc1_live_seed_rehydrate.py:11` says `main.py:2007`.

[[monday-post-session-clean-20jul]] [[s4-boot-outage-17jul]] [[feedback-verify-the-finding-premise]]
[[feedback-live-vs-latent-findings]] [[p1-health-require-hmac-17jul]]
