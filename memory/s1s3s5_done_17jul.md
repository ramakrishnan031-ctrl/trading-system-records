---
name: s1s3s5-done-17jul
description: "S1+S3+S5 SHIPPED + DEPLOYED 17-Jul (ada0caa, tag deploy-17jul-s1s3s5). 3 instruction premises were WRONG — S1 needed no new guard and no crontab-generator change; S5 was never an S1 prereq."
metadata: 
  node_type: memory
  type: project
  originSessionId: b1aa742a-e0f9-46e6-9de8-800ed4bc60dd
---

**DEPLOYED + VERIFIED.** `ada0caa` (report docs commit `9be3902`, markdown-only ⇒ deployed CODE ==
the tag). **Tag `deploy-17jul-s1s3s5` → `b61a776`. PC == origin == VM bare** (worktree md5
verified). **Schema v44, no migration.** Backup `pre_deploy_s1s3s5_20260717_122924.db` (341M,
integrity ok). Report `docs/audit/s1s3s5_done_17jul2026.md`.

| Item | Commit | Result |
|---|---|---|
| **S1** | `09ea725` | `market_day_only` enforced at the cron entry — **30/30** (was 16/30) |
| **S3** | `c8d3621` | login **throttle** replaces the lockout — Rama can no longer be DoS'd |
| **S5** | `ada0caa` | **benign functional set** settled; 27-job criteria tail triaged + deferred |

**Regression `10F / 4837P / 4S`, rc=1 — the known PC-env 10, `0 attributable` PROVEN** (the 4
affected suites re-run on the TRUE pre-change tree ⇒ `diff` IDENTICAL). Dashboard **367 pass** in
its own venv.

## ⭐ 3 INSTRUCTION PREMISES THAT WERE WRONG (mirror of [[feedback-verify-the-finding-premise]])
1. **S1 needed NO new guard and NO `generate_crontab.py` change.** The central guard ALREADY
   EXISTED — **`utils.cron_heartbeat.skip_if_non_trading_day`** ("TASK #3 Layer 6"), already used
   by 16 jobs, already **fail-OPEN** (weekday fallback on any calendar error). Making
   `market_day_only` mechanical in the generator (it sits in `_META_FIELDS` = docs, only
   `_GEN_FIELDS` reach the command — *that's* why it's decorative) was the tempting "root cause"
   but would have risked **all 47 cron jobs** (parse↔compose byte-exact selftest + drift-check +
   pre-receive) to fix pointless holiday runs. **Crontab is byte-identical; selftest passes 47/47.**
2. **S5 was NEVER an S1 prereq.** A heartbeat **STATUS**=`SKIPPED` hits `build_eod_summary`'s
   `elif` and NEVER reaches the functional check (counted under "⏭ Skipped"). Only
   **functional_status**=`SKIPPED` would be flagged. Different paths. The guard records *status*.
3. **S1 is WASTE-elimination, NOT safety — and the FIX is more dangerous than the bug.** The
   Officer never false-alarmed (`cron_registry.py:257` `is_due_on` correctly drops market_day jobs
   on holidays). Cost of the bug: 14 jobs doing pointless work on ~15 holidays/yr. Cost of a bad
   fix: `auto_refresh_token` skipped on a TRADING day ⇒ no token ⇒ **cannot trade at all**.

## THE S1 NUMBERS (audit said "20 of 25"; a looser regex of mine said 21 — both wrong)
**30 declare `market_day_only` · 16 already self-guarded · 14 were unguarded** (incl. the CRITICAL
`auto_refresh_token` / `eod_verify` / `eod_broker_reconcile`). Guard added as a **new `_cron_main`
per script — NEVER in `main()`**, so manual/ad-hoc runs on a weekend still work (mirrors
`eod_cleanup`). `capture_metrics_baseline.py` backs **TWO** jobs (`capture_metrics` +
`metrics_summary --summarize`) ⇒ skip attributed per-job or the Officer reports a phantom miss.
**Anti-decay pin added**: a test asserts EVERY `market_day_only` job resolves to a guarded script.

## ⚠️ S3 NEEDED A GUI RESTART — deploy-to-disk was NOT enough
`gui-dashboard` had been up since **10-Jul 04:05** serving the OLD auth from memory. Restarted
12:31:22 (new PID, NRestarts=0, login HTTP 200); verified **in the running process**: 100 failures
→ `is_locked=False`, `throttle_delay=8.0s`. **S1/S5 need no restart** (cron spawns fresh procs).
**Remember this for any future ops_dashboard change.**

## S3 DESIGN (why the audit's "per-IP" was HARMFUL)
Behind the tailscaled loopback proxy `remote_addr` is ALWAYS 127.0.0.1 ⇒ per-IP collapses to ONE
bucket ⇒ any failure locks out everyone incl. Rama. XFF is caller-settable ⇒ spoofable both ways.
**Fix: verify credentials FIRST + unconditionally ⇒ a correct login can NEVER be refused ⇒ the DoS
is structurally impossible.** Only FAILURES are delayed (1→2→4→8s, capped). A delay — not a fast
rejection — because telling right from wrong REQUIRES verifying; any check-free refusal would
refuse Rama too (= a lockout again). **Residual (accepted):** each delayed failure holds a Waitress
thread ≤ cap; unbounded would trade the old DoS for a new one.

## S5 — the culprit was `EMPTY_NO_DATA`, not `SKIPPED`
`generate_screened_csv`'s own docstring calls it *"legitimate on a no-trade day"*, yet the benign
set `("OK","SUCCESS","DELIVERED")` flagged it **every quiet trading day**. *A control that cries
wolf is a disabled control* — that noise is how the 14-Jul "green heartbeat, empty CSV" silent
failure survived. `_BENIGN_FUNCTIONAL` is now a documented frozenset (+`SKIPPED`,`EMPTY_NO_DATA`).
**Still flagged:** FAILED/MISSING/DEGRADED/**UNKNOWN** (silence about silence).
**Second half DEFERRED w/ triage: 32 monitored · 5 have a criterion · 27 execution-only.** The
capital/reconciliation-adjacent ones (`eod_verify`, `eod_broker_reconcile`, `reconcile_positions`,
`daily_report`, `trade_journal`, `compute_strategy_metrics`, `forward_shadow_record`) → **CAREFUL
LOOP** per the escalation valve. Inventing 27 criteria in bulk is how a criterion becomes noise.

**Rollback:** revert any single commit (independent, schema-free) or reset `main`→`4c148fb`; S3
also needs a gui-dashboard restart either way.

Links: [[e4-w10-done-17jul]] [[sweep-done-17jul]] [[ab910-ops-security-audit-16jul]]
[[feedback-verify-the-finding-premise]] [[feedback-verify-rc-not-output]] [[token-workflow-confirmed-21jun]]
[[project-vm-architecture-locked]] [[pc-test-env-hygiene]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 565 B (budget 450 B). The index now carries a hook and this link.

- ✅🚀🔝 **[S1+S3+S5 DEPLOYED 17-Jul — tag `deploy-17jul-s1s3s5`](s1s3s5_done_17jul.md)** — **S1** `market_day_only` enforced at the cron entry 30/30 (was 16/30; incl. CRITICAL `auto_refresh_token`) · **S3** login THROTTLE replaces the lockout ⇒ Rama can't be DoS'd · **S5** benign functional set settled (`EMPTY_NO_DATA`, not SKIPPED). **⭐ 3 instruction premises were WRONG** (the S1 guard already existed + already fail-open; S5 was never an S1 prereq; **the FIX is riskier than the bug**). **⚠️ S3 needed a GUI RESTART.** [[s1s3s5-done-17jul]]
