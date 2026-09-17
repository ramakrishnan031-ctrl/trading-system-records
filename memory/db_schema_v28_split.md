---
name: db-schema-v28-split
description: "DB is now TWO SQLite files (analytics split, schema v28); all 9 DB-audit observations closed"
metadata: 
  node_type: memory
  type: project
  originSessionId: cc19b3c6-40de-435a-9a20-12c619ad18e6
---

As of 2026-06-14, the state store is **two SQLite files**, not one (schema v28, O6 / FIX-176):

- `data_store/trading_system.db` — main: trades, orders, signals, fm_ledger, etc.
- `data_store/analytics.db` — `candles`, `system_metrics`, `system_metrics_daily` only.

`analytics.db` is **ATTACHed as schema `analytics`** on every connection, so unqualified
`SELECT ... FROM candles` still resolves (the tables exist only in analytics.db). `core/db_connect.py`
is the single source of truth for the path, the relocated-table set, `init_analytics_schema()`, and
`connect()`+attach.

**Gotcha:** any raw `sqlite3.connect(trading_system.db)` will NOT see candles/system_metrics — use
`core.db_connect.connect(db_path)` (attach-aware) instead. StateStore handles it automatically.

**Live VM DB migrated to v28 on 2026-06-14** (applied manually via direct `StateStore` init — see
gotcha below). Was at v26 beforehand; v26→v28 ran clean (main + analytics integrity ok, fk_check []).
candles/system_metrics/system_metrics_daily were EMPTY on the live DB (populated only by weekday
crons), so the relocation moved 0 rows — analytics.db exists with empty tables, no data loss.
`relocate_analytics_tables()` is idempotent (per-table txn, target cleared first so a crash-retry
can't duplicate). Nightly cron now `.backup`s BOTH files (analytics-*.db added) with shared 7-day cleanup.

**GOTCHA — migrations do NOT apply on a market-closed restart.** `main.py` checks market-open and
exits (status 0) BEFORE `StateStore` init on weekends/holidays, so a `systemctl restart` on a
non-trading day will NOT run pending schema migrations. They otherwise apply at the first trading-day
market-open startup (inside the live window). To migrate in a quiet window, run StateStore init
directly: `PYTHONPATH=. venv/bin/python -c "from core.state_store import StateStore; StateStore('data_store/trading_system.db').close()"`.
The service auto-starts each trading day via `token-watcher.service` (running) when the 08:00 Mon-Fri
token-refresh cron writes a fresh token; `Restart=on-failure` so a clean weekend exit stays down till then.

**O5 retention (FIX-175):** `scripts/db_retention.py` prunes old rows (candles/system_metrics/
webhook_audit/screener 90d, reconciliation_log 180d, fm_ledger 365d). Cron 02:30 IST (Sun +VACUUM,
which vacuums main + analytics). Runs after the 01:00 backup.

**All 9 observations from `docs/audit/db_schema_review_15jun2026.md` are now closed** —
O1–O9 across FIX-171→FIX-176, schema v24→v28. See [[live_trading_readiness]] and the lifetime
audit doc in repo. Nothing outstanding.
