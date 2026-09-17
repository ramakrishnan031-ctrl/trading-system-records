---
name: deploy-done-16jul
description: "15-Jul COMBINED DEPLOY executed + verified 16-Jul (F0 SMTP + push c9fb298 + Phase-B prune 113k); VM live, only docs unpushed"
metadata: 
  node_type: memory
  type: project
  originSessionId: e6ec189e-d4ac-47ad-8ae0-4379fa2ec5ee
---

**15-Jul COMBINED DEPLOY — EXECUTED + VERIFIED 16-Jul-2026 ~00:1x IST (off-market), Rama-authorized full run by VS Code Claude.** VM==bare==`c9fb298`; annotated tag `deploy-15jul-combined`→`1645bd6` pushed (single-tag rollback anchor); **schema v44, no migration** (v44==v44). Branch A (eod_cleanup FK-safe children-first prune + 90d retention · generate_screened_csv M-SC2b read-only · fm_ledger ledger_id) + Branch B (monitoring F1-F4 · canary 08:20 · deploy_assert) + record_heartbeat autospec/guard. Push hook clean ("crontab AUTO-INSTALLED from canonical"); canary cron `20 8 * * *` registered; deployed tree == HEAD (no modified tracked files).

**Why:** first fully-delegated push+deploy+destructive-prune+credential install; the record of what actually went live and the exact restore points.

**How to apply:** VM now runs `c9fb298`; the next 08:15 boot (16-Jul, a trading day) loads it. Before any further off-market work, read this + the ledger. The two PC docs banners already say DEPLOYED.

**F0 DONE:** fresh Gmail app-password installed as `ALERT_SMTP_PASSWORD` in VM `.env` (`/home/ubuntu/systems/trading-system/.env`, 600, **surgical** — only that line changed, 24 keys intact; installed via SSH **stdin** not argv → never in VM ps/history). PROVEN valid: direct Gmail SMTP login OK + canary `✅ email`. alert-watcher restarted onto new code+cred → `ExecMainStatus=0` (exit-2 SMTP loop cleared, 0 pending sentinels). NB: Q3 claimed F0-done but `.env` mtime was Jul-5 (stale/expired) — the instruction correctly overrode Q3 and installed from Q6.

**Phase-B prune DONE** (window 7 → cutoff 2026-07-09): **113,377 old signals cleared** — signals 146,000→**32,623**, screener_results 122,453→**23,363** (other children unchanged); **trades 355 UNCHANGED, foreign_key_check CLEAN, integrity ok, schema 44**. Ran the deployed FK-safe `run_eod_cleanup(dry_run=False)` directly for count visibility — NB the `scripts/eod_cleanup.py __main__`/`_cron_main` path **self-skips the whole job via `skip_if_non_trading_day` on non-trading days** (returns rc0 with NO output — that is what made the first CLI dry-run look empty; 16-Jul IS a trading day so the normal path would also have run). **Steady-state `system.eod_cleanup.signal_retention_days: 90` UNCHANGED** — the 15:50 cron maintains the small daily increment.

**VM gotcha (correct the instruction next time):** the shared venv is `/home/ubuntu/systems/venv/bin/python` (ABSOLUTE) — there is NO `venv/` inside the working tree, so the runbook's relative `venv/bin/python` would fail. The proven cron form: `cd .../trading-system && set -a && . ./.env && set +a && PYTHONPATH=. /home/ubuntu/systems/venv/bin/python scripts/<x>.py`.

**Backups (VM restore points, kept):** `data_store/backups/pre_deploy_combined_20260716_001521.db` + `pre_prune_20260716_002038.db` (both 357MB, quick_check ok). Old `.env.pre_f0_bak` (held the expired pw) removed after F0 verify.

**Git state:** VM==bare==`c9fb298`. PC `main`==`9226ad2` = c9fb298 + **1 docs-only commit (UNPUSHED)** (report + PATHS + SYSTEM_MAP flipped to DEPLOYED); zero runtime effect — push anytime or ride the next deploy.

**Security:** the decision sheet held the app-password in Q6 (typed there despite its own rule) → **excluded from git** (`.git/info/exclude`; `git status` clean, `!!` ignored, 0 tracked). **⏰ Rama: DELETE** `DEPLOY_DECISION_SHEET_TEMPLATE_15-Jul-2026.txt`. No separate Gmail *account* password in the sheet. VM `.env` gitignored (`.gitignore:6`) + untracked in bare.

**Rollback (documented, not executed):** L1 = `git revert` the fix commits + one off-market `systemctl restart trading-system` (schema-free); L2 = reset to the tag's first parent `deploy-15jul-combined^`.

**⏰ Owed (Rama, 16-Jul close):** eod_cleanup(90d) + generate_screened_csv PASS · canary 4 paths ✅ · Cron Officer functional status · check_cron_drift false-alarm gone · **EOD emails actually arrive** (the real proof F0 holds a full session). Report `docs/audit/deploy_done_15jul2026.md`. [[unpushed-pending-deploy-ledger]] [[integration-merge-blocked-15jul]] [[system-health-audit-15jul]] [[fixes-15jul]] [[monitoring-hardening-15jul]] [[migration-on-open-rule-14jul]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 952 B (budget 300 B). The index now carries a hook and this link.

- ✅🔀🟢 **[15-Jul COMBINED-DEPLOY — DEPLOYED 16-Jul (VM==bare==`c9fb298`; F0 + Phase-B prune DONE)](deploy_done_16jul.md)** — Branch A (3 hygiene fixes) + Branch B (monitoring hardening) LIVE in `c9fb298`; **annotated tag `deploy-15jul-combined`→`1645bd6` pushed = rollback anchor. F0 SMTP restored (canary ✅ email) + Phase-B prune 113,377 cleared (146k→32,623; trades 355 UNCHANGED; FK clean).** The STOP blocker (Branch-B/F2 stale `record_heartbeat` mock) was resolved **test-only** after an approved compat audit found **NO production incompatibility**: both mocks → `create_autospec` (`397f3f6`); **signature-lock + discovery-guard** (`1645bd6`); **Interface Change Checklist** (`32389c0`). Gates GREEN: regression **5052 pass/12 fail** (known PC-env only); EOD dry-run clean on a DB COPY; deploy_assert rc=0; integrity/fk clean; schema v44. Report `docs/audit/integration_deploy_15jul2026.md`. [[integration-merge-blocked-15jul]]
