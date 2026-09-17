---
name: sweep-done-17jul
description: 17-Jul SWEEP DEPLOYED (PC==VM==b2d7b2b) — batch-2 + purge (0 live-token hits) + 4 ops/security fixes; S1/S3/S5 escalated because the obvious fix was worse than the bug.
metadata: 
  node_type: memory
  type: project
  originSessionId: a8c00bd7-f7a4-4643-bf7d-9bab09ae2c49
---

**17-Jul 01:10–02:45 IST, off-market gating WAIVED by Rama. ALL DEPLOYED: PC == VM == bare ==
`b2d7b2b`.** Tags `deploy-17jul-batch2`→`0a9a6a8`, `deploy-17jul-sweep`→`f57d308`.
Schema **v44, no migration**. Trading/capital path NOT touched. Report:
`docs/audit/sweep_done_17jul2026.md`.
**Regression: 4814 pass / 11 known-PC-env / 0 attributable** + **dashboard 357/357 in its own venv**.

## 🔴 THE TOKEN PURGE IS DONE — but rotation is STILL OWED
`shred -u` on **19 files** (10 live-token 984 lines · **9 revoked-token 678 lines the audit never
counted**) + `logs/cron-candle-fetch.log`. **Verified after: 0 live-token hits, 0 token-shaped
paths, 0 outside `.env`.** logs/ 1.1 GB → 642 MB. Ran ~02:00 with the app down, before the 08:15
boot ⇒ `debug_2026-07-17.log` never existed to leak into.
**🔴 RAMA STILL OWES: ROTATE `@Trade_sysbot` (id 8648177777)** — purging is not un-disclosing.
**Rotation is PROVEN clean here**: the 02-Jul rotation left the old token verifiably **401-revoked**.

## Shipped (4)
- **S2 `3ad047e`** — dashboard 2FA **fails CLOSED** on an empty `totp_secret`; explicit
  `auth.totp_disabled: true` is the only escape hatch. **Cannot lock Rama out — verified**: the
  effective config merges `gui_config.local.yaml` (real 32-char base32) over the base. The
  fail-open path is reachable *exactly when the local overlay goes missing* — when you'd least
  want a silent 1FA downgrade.
- **S4 `84cee3e`** — `/health` (webhook, `0.0.0.0:5000`) now **authenticated + behind the per-IP
  limiter**; it was a free oracle for `kill_switch_active`+queue depth. Scope = that ONE route;
  `_handle_webhook` untouched. **UptimeRobot polls a DIFFERENT /health (`healthcheck_server.py`
  :8080)** — nothing in prod polls :5000/health.
- **S6 `e4c6d3e`** — FIX-065 market-hours guard implemented **in `pre-receive`, NOT post-receive**
  (git ignores post-receive's exit status ⇒ a guard there skips the checkout while the bare ref
  moves = **bare≠tree half-deploy**). Logic in `deploy/hooks/market_hours_guard.sh` = pure
  function of (HHMM,DOW,MSG) ⇒ clock injected. **12 vacuous tests → 21 real** (move the guard
  away ⇒ 20/21 RED). **SHIPS UNARMED — arming is Rama's call** (the same file carries the
  never-live cron-integrity guard, enforcing by default; a buggy pre-receive blocks EVERY deploy.
  Break-glass `rm ~/trading-system.git/hooks/pre-receive`).
- **S7 `5f89ec5` + `b2d7b2b`** — post-receive header said "NOT the currently-installed hook"; md5
  AND a live push (`crontab AUTO-INSTALLED from canonical`) prove it IS. **md5 `bd950b7…` →
  `b716673…`; VM hook RE-ARMED, identity verified.** ⚠️ I first recorded `e493dc5…` — measured
  after the FIRST of two edits; corrected in `b2d7b2b`. **Lesson: re-measure a checksum AFTER the
  last edit** ([[feedback-verify-the-finding-premise]]).

## ⛔ ESCALATED to the careful loop (3) — the obvious fix was WORSE than the bug
- **S1 `market_day_only`** — the instruction's own gate ("confirm none of the 20 is a trading
  decision") **FAILS**. **`auto_refresh_token` is `critical:true` and gates whether the system
  STARTS** (verified from code: `token-watcher.service` = "auto-start on fresh token";
  `token_watcher.sh` = the headless starter). A central guard keyed on the holiday calendar ⇒
  **one wrong calendar entry = no token = no trading that day.** Also `eod_cleanup` (order
  status) + `eod_verify`/`eod_broker_reconcile`/`reconcile_positions` (capital). AB-910 itself
  tagged §2.2 **LOOP "with the central mechanism designed first"**.
- **S3 lockout DoS** — **per-IP keying (the audit's AND the instruction's fix) would be STRICTLY
  WORSE.** `tailscaled` proxies `100.74.84.44:443` → Waitress **`127.0.0.1:8500`** ⇒
  `remote_addr` is **127.0.0.1 for every request** ⇒ one bucket ⇒ an attacker's 5 failures lock
  out **EVERYONE incl. Rama**. Needs `X-Forwarded-For` (unverifiable without touching prod serve
  config) or an explicit throttle-vs-lock decision. `gui-dashboard.service` is LIVE.
- **S5 functional-criterion tail** — **the blocking design question found here:**
  `cron_officer.py:189` flags **any** functional status ∉ {OK,SUCCESS,DELIVERED} as an issue ⇒
  marking `gemini_trade_coach` SKIPPED on a legit **no-trade day** raises a false issue **every
  quiet day** (the alert noise the Foundation Rule forbids). Batch-1's `daily_trade_review`
  escapes only because the Officer self-guards on holidays — that does NOT transfer to a quiet
  *trading* day. **Settle the Officer's benign-set semantics FIRST**, then apply criteria to ~16 jobs.

## Corrections I made to my own interim claims (both disproven before they shipped)
- The 4 gemini jobs **ARE** monitored — they call `record_heartbeat()` **directly** (not
  `HeartbeatTimer`), which is why my `HeartbeatTimer` grep missed them.
- Their unconditional `record_heartbeat()` is **NOT** an execution bug for `gemini_premarket_brief`
  (**AST**: `run_briefing` returns 0 or raises). `run_coaching`/`run_check` do return non-zero, but
  those are **documented legitimate states** ("no trades to coach", "no traded symbols",
  `DIVERGENCE_DETECTED` — which already alerts).

## ⏰ Operational
**The 16-Jul SOFT_KILL is a PRIOR-DAY kill** (`triggered_at 2026-07-16T10:54:28`, "planned pause
for pending fix/review work") ⇒ per `token_watcher.sh` it **auto-clears at the 08:15 boot** ⇒ the
system **resumes trading 17-Jul with the swept code** unless re-paused. **Book FLAT** (7 CLOSED +
3 CLOSED_MANUAL since 15-Jul; zero OPEN). The `failed` unit state = exit 4 from the intended HALT,
not an incident. [[killswitch-autoclear-prior-day]]

Links: [[batch2-done-17jul]] [[ab910-ops-security-audit-16jul]] [[unpushed-pending-deploy-ledger]]
[[feedback-verify-the-finding-premise]] [[feedback-verify-rc-not-output]] [[pc-test-env-hygiene]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 677 B (budget 450 B). The index now carries a hook and this link.

- ✅🚀🔒🔝 **[17-Jul SWEEP + BATCH-2 DEPLOYED — PC==VM==bare==`b2d7b2b`; the token PURGE is DONE](sweep_done_17jul.md)** — tags `deploy-17jul-batch2`→`0a9a6a8`, `deploy-17jul-sweep`→`f57d308`; v44 no-migration; 4814 pass / 11 known-PC-env / **0 attributable** + dashboard 357/357. **19 files shredded ⇒ 0 live-token hits anywhere outside `.env`.** Shipped S2 (2FA fail-CLOSED) · S4 (`/health` auth+limiter) · S6 (FIX-065 guard in **pre-receive**, ships UNARMED) · S7 (hook header, md5→`b716673`, re-armed). **⛔ S1/S3/S5 escalated — the obvious fix was WORSE than the bug.** **🔴 RAMA OWES: ROTATE `@Trade_sysbot` (8648177777).** [[sweep-done-17jul]]
