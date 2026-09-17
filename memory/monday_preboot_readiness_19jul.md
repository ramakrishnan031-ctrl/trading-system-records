---
name: monday-preboot-readiness-19jul
description: "19-Jul VERIFY-ONLY pre-boot check for Monday 20-Jul 08:15 (first real boot since S4). VERDICT: READY with one caveat (the 08:15 token gates trading, but its failure is LOUD via the 09:00 liveness alarm). S4 fix verified in deployed code; the S4 CLASS is closed by the independent liveness_probe. Crontab clean after ~8 reinstalls (0 dups). Nothing changed."
metadata: 
  node_type: memory
  type: project
  originSessionId: 69886370-a044-4d23-87ae-f3c02b539e6e
  modified: 2026-07-20T14:23:49.748Z
---

**MONDAY 20-Jul PRE-BOOT READINESS (19-Jul-2026, VERIFY-ONLY, docs-only, nothing changed/started).**
Report `docs/audit/monday_preboot_readiness_19jul2026.md`. All 3 artifacts untouched (DB `6df0c09a…`,
JSONL 7,827@16-Jul, analytics `bb229f44…`).

## ⭐ VERDICT: READY — one caveat, loudly backstopped
Boot code = `d271525` (markdown-only delta since). **S4 fix VERIFIED in the deployed tree** (`63a6f0d`):
`utils/startup_checks.py:807-808` `reachable = 2xx OR 401`. Service `enabled` (inactive; `token-watcher.service`
enabled starts it on the fresh token); kill-switch **INACTIVE** (auto-cleared 17-Jul, no resume owed);
`require_hmac:false` (unchanged). **The caveat:** the 08:15 TOTP refresh gates whether it trades at all — but
its failure is **LOUD** (the 09:00 liveness alarm), not silent like S4.

## ⭐ THE S4 CLASS IS CLOSED (not just the instance)
Only **ONE** boot step exits 0 on failure — the post-start `/health` self-check (`main.py:3327`
`_shutdown_event.set()`); now 401-safe, fatal only on a genuine Flask-down. Every other boot failure exits
NON-ZERO (token→6, preflight→3, others 5/7/8) or warns-and-continues. **Closed by `scripts/liveness_probe.py`**
(deployed 17-Jul, cron `*/5 9-15 Mon-Fri`, **independent** — doesn't import main.py): alarms ONE CRITICAL if the
service is inactive during [09:00,16:00) on a trading day and not operator-parked ⇒ **a clean-dead boot is caught
at 09:00, an hour before entries.** **Latent sibling (benign, do NOT touch):** `check_scanner:703` is still
"2xx only" (same misread pattern) but its failure is a WARNING (`main.py:1597`), not a shutdown, and scanner URLs
are public. **Residual (Rama, AFTER Monday):** should the webhook self-check shut the boot down at all? (S4 lesson 4).

## ⭐ STANDING FACTS carried forward
- **`sim_R=None` silent-degradation:** if the recorder's Kite fetch fails at 18:15 (app DID trade ⇒ screener_results
  exist), the forward shadow appends `sim_R=None`, exits 0 ⇒ fail-LOUD never fires. **Distinguishable after** (null
  `sim_R` in the JSONL) — check OOS day 4 after Monday's close. (If the app didn't run at all, the recorder appends
  nothing, not nulls.) [[forward-shadow-capacity-d4-feasibility-19jul]]
- **Preservation gap:** the preserved snapshot is `trading_system.db` ONLY; the **1-min candles** that make D4
  partially testable live in the ATTACHed **`analytics.db`** (not snapshotted). [[db-schema-v28-split]]
- **⚠️ NEW QUEUE ITEM — candle retention:** will the OOS 1-min candles survive the ~17-34 trading days D4 needs?
  `analytics.db` may have its own retention (`db_retention.py` cron, Mon-Sat + Sun variants) — **verify, do not
  assume**, before D4 relies on them.
- Crontab clean after ~8 reinstalls: **0 exact-line dups**, all 5 boot-critical present once, reinstall is a full
  block-replace. The 4 Sunday `cron_heartbeat` rows are benign (only `eod_cleanup`'s own freshness check reads them).

## ⭐ RESUMED 19-Jul (interrupted mid-trim) — committed, pushed, verified; NOTHING fixed
The batch powered down mid MEMORY.md-trim, before commit/push/fingerprints. On resume, nothing was
re-investigated and nothing fixed:
- **Committed + pushed, markdown-ONLY:** report `bfcd964` (with the deploy-proof) then addendum `1462984`.
  **PC == origin == VM bare == `1462984`.** `origin` **IS** the VM bare (`trading-vm:~/trading-system.git`)
  ⇒ **every push fires a full crontab reinstall** (post-receive installs `deploy/cron/trading-system.cron`
  verbatim, gated on `generate_crontab.py --generate == canonical`). Both pushes printed
  `post-receive: crontab AUTO-INSTALLED from canonical` (reinstalls #9, #10) — the reinstall is invariant
  under a docs change, so the chain stops without regress.
- **Post-push crontab (§D3) clean:** installed == canonical byte-identical; **0 dups**; the 5 boot-critical
  jobs each present once — token `15 8 * * 1-5`, token-cleanup `0 5 * * *`, eod `50 15 * * 1-5`, officer
  `22 16 * * 1-5`, forward-shadow `15 18 * * 1-5`.
- **Artifacts re-fingerprinted on the VM over SSH post-restart (§C) — all 3 byte-identical to recorded**
  (DB `6df0c09a…`/89,968,640/`11:14:29` · analytics `bb229f44…` · JSONL 7,827 @ 16-Jul 18:15). The JSONL
  mtime is **still 16-Jul** ⇒ the 17/18/19-Jul 18:15 crons did NOT touch it (no manual run, no contamination).
- **Delta vs code tag `d271525` = markdown ONLY** — every changed file is `.md` (`docs/**` + root **`PATHS.md`**
  + `docs/SYSTEM_MAP.md`); no code/config/schema/test. **CODE LEDGER still EMPTY** (only
  `e4-w10-pnl-contract`@`ad34ee4`, sign-off-gated).

## ⭐ §B — the interrupted MEMORY.md trim lost NOTHING; nothing restored
No pre-trim snapshot exists (the palace is **not** git-tracked; no `.bak`/`.tmp`) ⇒ a literal byte-diff of
removals is **impossible** — stated plainly, not fabricated. Verified LOSSLESS by four positive checks:
(1) all 10 board items + Q10 Part B/Kite token + security actions **present**; (2) every topic-file link in
MEMORY.md resolves — **0 missing**; (3) `MEMORY_ARCHIVE_2026H1.md` **not modified today** (mtime 18-Jul 21:04)
⇒ the trim relocated nothing out, so nothing was stranded; (4) the file is **20,032 B — ABOVE** the ~17 KB
target the prior (verified-lossless) compaction set ⇒ the interruption hit before material removal. Nothing in
category (iii); **nothing restored (§B4).** Over-target is acceptable (**§B5**); a considered compaction is
deferred to after Monday.

## ⭐ check_scanner:703 — ❌ CLOSED 20-Jul-2026, REFUSED WITH EVIDENCE (superseded record below)

> **The "add the `== 401` tolerance" follow-up was REFUSED on 20-Jul.** `:703` calls **external
> `https://chartink.com/screener/*`**, not the local `/health`; there a 401 is an *anomaly*, not an
> expected answer, so the tolerance would have made a correct check silently permissive. Monday's boot
> logged `warnings=[]` — it is not misfiring. **The half that stands: `scanner_unreachable` must remain
> a WARNING, never escalated to blocking.** The genuine S4 sibling is `scripts/preflight/checks/signals.py:28`
> (same local `/health`, unauthenticated, 2xx-only) — **LIVE**, fired a false CRITICAL 09:19 on 20-Jul.
> ⚠️ The §80 completeness claim below searched only the `200 <= status_code < 300` range shape in `*.py`,
> which is why `signals.py:28` was missed; a 4th-instance sweep is queued.
> See [[preflight-401-third-sibling-20jul]] and `docs/audit/boot_path_pair_design_20jul2026.md`.

### Superseded record (19-Jul), kept legible:
`utils/startup_checks.py:703` still uses the **2xx-only** reachability shape (no `== 401` branch), same misread
that took prod down at S4 — **but its failure is WARNING-only** (`main.py:1596-1597` →
`warnings.append("scanner_unreachable")`), **not a `_shutdown_event`**, so it is LATENT not LIVE. It would
become LIVE only if `scanner_unreachable` were escalated into `blocking_failures` or a shutdown. **Completeness
(verified repo-wide):** exactly **two** sites compute reachability from the `200 <= status_code < 300` range,
both in `startup_checks.py` — `:703` (scanner, latent) and `:808` (webhook, FIXED); other `== 200` hits are
exact-success checks, none boot-shutdown-coupled. **Left untouched tonight** (boot path, night before first
real boot since S4); queued for the careful loop **after Monday alongside the live-seed extraction**.

Related: [[s4-boot-outage-17jul]] [[forward-shadow-capacity-d4-feasibility-19jul]] [[liveness-alarm-17jul]]
[[token-workflow-confirmed-21jun]] [[db-schema-v28-split]] [[consecutive-losses-gate-wired-19jul]]
[[unpushed-pending-deploy-ledger]] [[feedback-verify-the-finding-premise]]
