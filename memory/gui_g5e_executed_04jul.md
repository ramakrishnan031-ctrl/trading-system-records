---
name: gui_g5e_executed_04jul
description: "G5 redesign DEPLOYED to VM 04-Jul (merge b4aea6f); gate GO, smoke clean, real-data reconciles; G5.1 UI/UX backlog seeded"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5504e191-b244-4ae5-8321-b8eac900a8f7
---

The ops_dashboard G5 redesign (G5a–G5d) is **DEPLOYED to the VM** (04-Jul-2026 Sat,
off-market, GUI-only). Follows [[gui_g5_local_validation_04jul]] + [[gui_g5e_deploy_plan_04jul]].
Live at **https://trading-system.tail1cdc6d.ts.net** (tailnet-only).

**Commits:** deploy branch `gui-g5-deploy` @ `91cc207` (45 files `ops_dashboard/**`)
→ merged `--no-ff` to main = **`b4aea6f`** (pushed origin/main; post-receive checked
out; VM main HEAD == `b4aea6f`). Pre-G5 tip was `80be23a`. **Rollback tag
`gui-pre-g5-rollback` → `80be23a`** (annotated obj `69980bd`; pushed; == live G2 build,
functionally == `7b1c92d`). One-command rollback: revert the merge / redeploy the tag
→ restart gui-dashboard (GUI-only blast radius; trading/DB/cron untouched).

**Merge-gate:** CLEAN at BOTH push and merge — `origin/main..HEAD` = 45 files, all
`ops_dashboard/**`, 0 core/orders/capital/strategies/broker/signals/main.py/config/
schema. The 5 non-G5 dirty paths (`PATHS.md`, `docs/SYSTEM_MAP.md`, 2×`docs/audit/*`,
`gui/`) stayed UNSTAGED (ride a later docs commit). Post-receive is **main-only**
(`if ref==refs/heads/main`) so the branch push did NOT deploy; crontab reinstall on
main-push was a no-op (no cron files in the diff → generate==canonical).

**STAGE 2 GATE (binding, clean VM venv `/tmp/g5_validate`, throwaway):** I4 PASS
(kiteconnect absent); **`pytest -q` → 354 passed / 0 failed** (46s); ZERO env-only
failures on the clean VM venv (the 32 PC failures are PC-specific, [[pc_test_env_hygiene]]);
28/28 gate tests PASS (pinned 6/13/8/6/4 · HARD_KILL blink==1 · two-state honesty ·
single System Score · export OFF · isolation I1–I7 incl. CDN gate).

**Deploy:** overlay `gui_config.local.yaml` survived `checkout -f` (600, ubuntu,
`session_cookie_secure: true`, real main_db path); **only gui-dashboard restarted**
→ active; trading-system stayed inactive (off-market), token-watcher active — trading
stack byte-untouched; Tailscale serve persisted (no re-auth).

**SMOKE:** real server — `/`→302, `/login`→200, `/api/dashboard`(anon)→401;
**61-route sweep 0 unexpected / 0×404 / 0×500**; deployed files: no "Signal Score"
string, controls.html 0 write-controls, "Pending Broker Source" in positions(2)/
holdings(3), export flags not overridden true.

**REAL-DATA VALIDATION (authed test-client on the REAL read-only DB vs independent
SQL — ALL MATCH):** every key endpoint 200 on real data, no 500s. P&L month
(2026-06-06..07-05): closed 81 / net 43.67 == SQL. Strategy Ranking
positional_sector_rotation 12 trades / net 31.99 == SQL. Scanner Attribution psr
accepted 19572 == SQL signals. Trade Explorer 228 == SQL total. Trade Story
`trd_84e9…` assembles from real signal+orders+scanner+raw_payload+timeline joins
(vwap_bounce_long/EFCIL/−3.97/SL_HIT). Dashboard (Sun) trades_today 0 == SQL 0.
Positions/Holdings broker side honestly `unavailable` (count 0, no fabricated numbers).
Controls `read_only:true`. Pipeline 13 stages. Latest real trading day in DB =
2026-07-03.

**G5.1 UI/UX BACKLOG SEED (real-data observations — NOT deploy blockers; Rama drives
G5.1 after his browser review):**
1. **Scanner `quality_score` ≈ 0 for ALL scanners** on real data — opportunity_quality
   = 100×accept_rate×trade_conversion×win_rate; trade_conversion = trades/accepted is
   tiny (e.g. 32/19572) because scanners fire thousands of signals → quality rounds to
   ~0 uniformly (uninformative). Funnel RAW numbers are correct/honest. Reconsider the
   metric scaling (relative-rank or drop the conversion factor).
2. **Large funnel numbers** (received 108060 / rejected 88488 / stored 19572 per
   scanner) — verify Scanner Attribution column widths + thousands-formatting don't
   overflow.
3. **None/null on a non-trading day** (opening_capital / deployed_pct / remaining /
   margin_vs_capital_pct = None on Sunday) — verify templates render "—"/"n/a" not
   literal "None"; empty-state polish for Capital/Risk/Exposure.
4. **Empty Positions/Holdings/Capital-ledger** (count 0 / ledger [] on non-session
   day) — verify graceful empty-state.
5. **Richer-than-fixture data** (228 trades, 11 strategies, 13 scanners) — check Trade
   Explorer / Trade Logs (228 rows) pagination/sort layout.

**NEXT:** Rama does his full browser review on real data (his binding visual pass) →
hands the G5.1 UI/UX correction list → Web Claude issues the G5.1 polish file. Soak
S1–S8 resumes from Monday 06-Jul 08:15 boot on the deployed G5 build per the locked
contract ([[gui_g2c_deploy_prep_03jul]], `SOAK_EVIDENCE_TEMPLATE.md`). Parity: the
GUI reads the same real DB regardless of paper/live; mode is a displayed attribute
only (confirmed — `/api/positions` mode=LIVE is a label, no path branches on it).
Cleanup: VM `/tmp/g5_test`+`/tmp/g5_validate` removed; local `gui-g5-deploy` branch +
remote branch ref retained as deploy record.
