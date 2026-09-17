# 01 — SYSTEM OVERVIEW

> **Evidence basis.** The PC worktree `D:/Projects/wt-sr-shadow-15sep` at commit **`e7bf477`** with the uncommitted **`force_qty`** change set — byte-equivalent to the **TESTING VM** as delivered 17-Sep-2026 19:31 IST. Machine-side facts are RECORD-DERIVED from the captures preserved in `trading-system-sbx-snapshot/_machine/` (testing VM, 17-Sep-2026 20:06 IST) and are labelled where used. **PRODUCTION WAS NEVER READ**; every statement about production is RECORD-DERIVED or NOT ESTABLISHED.
> **Evidence date:** 18-Sep-2026. The system is retired. This chapter is the map: it states what existed and points at the chapter that owns each part. Defect observations are parked for chapter 22 and are not argued here.

---

## 1.1 What this system was

An automated equity trading system for the Indian market (NSE), trading a single broker (Zerodha) through that broker's `kiteconnect` SDK. It did not find its own trades: external scanners (Chartink) posted signals to an HTTP endpoint, and the system decided whether each signal became an order, sized it against its own capital ledger, placed and supervised the resulting orders, squared off intraday positions before the close, reconciled itself against the broker, and reported the day.

It ran two books at once — **intraday** (MIS / CO products, flattened the same day) and **delivery** (CNC, carried overnight with a broker-side OCO GTT) — and it ran in one of two **modes**:

| Mode | What differs | Anchor |
|---|---|---|
| **paper** | no Kite client is constructed at all; the broker adapter is given a quote provider and an in-memory simulator for orders, fills, positions, GTTs and capital | `main.py:2360`; the simulator lives inside `broker/zerodha_adapter.py` |
| **live** | `accounts.csv` is read, the account's API-key environment variable is aliased, the token file is read and validated, and a real `KiteConnect` is built | `main.py:2367`–`2383` |

The CLI default is `paper` (`main.py:185`–`186`). The service unit on the machine starts it with `--mode live` (`deploy/systemd/trading-system.service:19`, identical in the installed capture). **Paper and live are traced separately throughout this manual**; where a chapter describes one and not the other, it says so.

## 1.2 The three environments

| Environment | Role | What is established about it |
|---|---|---|
| **The PC** (Windows workstation) | development, operations, evidence and records; the git origin of the deployed code; the Windows-side token helpers | this manual is written from its worktree |
| **The testing VM** ("the twin", `130.210.13.114`) | a full second instance used for measurement and rehearsal | the tree, the installed units, the real crontab and the deploy hook are all captured and measured; it runs `e7bf477` plus the `force_qty` change set, with the differences listed in Appendix 01-A |
| **Production** (`161.118.187.249`) | the instance that traded real money | ⛔ **never read.** Its code is RECORD-DERIVED at git `970aabf`; its configuration, crontab, units and database are **NOT ESTABLISHED** |

**Account registry.** `config/accounts.csv` (tracked, 704 bytes, 6 lines, last changed `13eb727` on 2026-06-12) declares five Zerodha accounts, one marked primary, each with the **names** of its API-key, API-secret and TOTP environment variables plus a paper capital figure and a capital share. ⚠️ The testing VM carries its **own** `config/accounts.csv` of 228 bytes (RECORD-DERIVED from the snapshot manifest's exclusion table; its contents were not read), so the twin's registry is a different file from the repository's. ⛔ No credential value appears anywhere in this manual — only variable names. Chapter 18 states where the values lived.

## 1.3 The components

The tree holds **757** Python modules and **289,044** lines. **200** modules (**92,168** lines) are reachable by import from an entry point — the service plus the 38 scripts the scheduler names — and those are the ones chapter 02 maps one by one.

| Package | Runtime modules | Runtime lines | What it is | Owning chapter |
|---|---:|---:|---|---|
| `orders` | 19 | 19,250 | order construction, placement, monitoring, reconciliation, EOD square-off, GTTs, exits | 10, 11, 12 |
| `scripts` | 45 | 15,970 | every scheduled job: token refresh, pre-flight, retention, reports, drift checks | 03, 14, 15, 19, 20 |
| `core` | 26 | 13,145 | config loading and auditing, the SQLite gateway, time authority, event bus, telemetry | 03, 16, 17 |
| `capital` | 8 | 7,157 | the capital ledger, kill switch, position sizer, risk engine, drift handler | 09 |
| `broker` | 12 | 5,664 | the Zerodha adapter, rate limiter, order state machine, cost and slippage models | 04, 10 |
| `reports` | 5 | 5,144 | the daily report, the trade review, styling | 15 |
| `main` | 1 | 4,329 | the single composition root and boot sequence | 03 |
| `signals` | 4 | 4,088 | the webhook ingress and the signal-admission pipeline | 05, 06 |
| `screening` | 7 | 2,734 | the ten-step screener, quality scoring, step execution | 06 |
| `sr_shadow` | 11 | 2,419 | the support/resistance shadow track (nothing live depends on it) | 07 |
| `utils` | 5 | 2,290 | startup checks, holiday guard, heartbeats | 03, 19 |
| `sr_detector` | 12 | 1,931 | support/resistance detection and its backfill | 07 |
| `v3_chain` | 9 | 1,902 | the newer "hard gate" scoring chain, switchable off / shadow / enforce | 06 |
| `alerts` | 6 | 1,787 | Telegram, email, critical-alert delivery and sentinels | 14 |
| `ops` | 13 | 1,271 | the control tower reporting job | 15 |
| `data` | 3 | 1,158 | the live tick feed and candle store | 04 |
| `strategies` | 5 | 749 | strategy YAML loader and schema | 05 |
| `regime` | 4 | 655 | market-regime classification | 06 |
| `allocation` | 5 | 525 | portfolio allocation and ranking | 09 |

Outside the runtime set: **413** test modules (**144,581** lines, chapter 19), the **93**-module `ops_dashboard` web application (**40,722** lines — a separate process with its own installed unit, chapter 25), and 144 further modules that no entry point imports (chapter 02 lists every one and marks it NOT MAPPED).

## 1.4 External systems

Measured from the import graph of the runtime set, then read at the call sites:

| External system | How it is reached | Runtime modules that touch it |
|---|---|---|
| **Zerodha Kite (REST)** | the `kiteconnect` SDK | 10 modules import it — `broker/zerodha_adapter.py` is the wrapper the trade path uses; `main.py` builds the session; eight scripts build their own client |
| **Zerodha Kite (streaming)** | `KiteTicker` | `data/live_feed.py:18` |
| **Chartink scanners** | inbound HTTP `POST /webhook/<scanner_name>`, authenticated by an HMAC header or a `?token=` query parameter | `signals/webhook_receiver.py:406` |
| **Telegram** | HTTPS via `requests` | `alerts/telegram_notifier.py`, plus `scripts/cron_officer.py` and `scripts/monitoring_canary.py` |
| **E-mail (SMTP)** | `smtplib` | `alerts/telegram_notifier.py` (the same module carries both transports) and `scripts/monitoring_canary.py` |
| **NSE holiday calendar** | a per-year YAML file in `config/`, read by the boot guard before anything else | `utils/holiday_guard.py` |
| **NSE F&O ban list** | an HTTP fetch, 08:35 on weekdays | `scripts/fetch_fno_ban.py` |
| **Zerodha instrument dump** | an HTTP fetch into `config/instruments.csv`, 09:00 on weekdays | `scripts/refresh_instruments.py` |

Python packages of note in the runtime set: `waitress` (the production HTTP server), `flask` (the app object and the health endpoint), `pydantic` (all configuration schemas), `openpyxl` (the Excel reports), `pyotp` (the TOTP step of the headless login), `cachetools`, and `fcntl` / `msvcrt` for the cross-platform instance lock.

## 1.5 Persistent storage

| Database | Tables | Declared in | What it holds |
|---|---:|---|---|
| `data_store/trading_system.db` | **45** | `core/schema.sql` (104,053 bytes, 73 indexes) | the operational record: `trades`, `orders`, `signals`, `fm_ledger`, `session`, `system_events`, `kill_switch_state`, `screener_results`, reconciliation and pre-flight tables, and the EOD log |
| `data_store/analytics.db` | **3** | `core/analytics_schema.sql` | `candles`, `system_metrics`, `system_metrics_daily`; created and attached on every store open |
| `data_store/sr_shadow.db` | **4** | created in code | the S&R shadow track: `shadow_rows`, `spool`, `evaluation_runs`, `meta` |

The store is opened once at boot with WAL journalling, `synchronous = FULL`, foreign keys on and a 30-second busy timeout (`core/state_store.py:107`–`113`), and it is the only sanctioned schema migrator: a database newer than the code refuses to open, and a pending migration may be run **only** by the boot path and **only** off-market (`core/state_store.py:398`, `:420`–`427`). Chapter 16 owns the schema; chapter 15 owns the reports and evidence files.

## 1.6 The trading day

All times IST. The scheduled column is the installed crontab (RECORD-DERIVED, 42 active entries); the in-process column is the service's own timers.

| Time | What runs | Where it comes from |
|---|---|---|
| 00:00 · 01:00 · 01:05 · 01:10 · 02:00–02:30 | log cleanup; the two SQLite backups; the evidence backup; backup, sentinel, output and DB retention | cron |
| 05:00 **daily** | the broker token file is deleted | cron |
| 08:15 Mon–Fri | headless token refresh: password, TOTP, redirect capture, token written | cron → `scripts/auto_refresh_token.py` |
| 08:20 | monitoring canary | cron |
| 08:30 / 09:14 / 09:15 | pre-flight phases A, B and C (C watches for 285 s) | cron → `scripts/preflight/orchestrator.py` |
| 08:35 | F&O ban list fetch | cron |
| **08:00–18:15** | the window inside which the service is allowed to *start*; outside it the process exits 0 without loading configuration | `main.py:2170`, `:2184` |
| 09:00 | instrument master refresh | cron |
| 09:15 | market open; the in-process margin re-sync thread fires | `config/system_config.yaml` `trading_hours.market_open`; `main.py:4148` |
| 09:20 | Cron Officer morning briefing | cron |
| **10:00** (production and the repository) / **09:30** (the testing VM) | the earliest an entry may be taken | `trading_hours.entry_start`; the twin's value is part of the `force_qty` change set |
| every 5 min, 09–15 | metrics capture and the liveness probe | cron |
| 15:00 | last entry by configuration | `trading_hours.entry_end` |
| 15:09 | MIS square-off cutoff, with the in-process notifier and auto square-off ahead of it | `trading_hours.mis_squareoff_cutoff`; `main.py:3353`, `:3369` |
| 15:15 | EOD entry cutoff | `trading_hours.eod_entry_cutoff` |
| **15:17** | the EOD square-off backstop fires: soft-kill, cancel, exit, promote to market after 120 s, sweep, reset daily P&L, report | `trading_hours.eod_squareoff_time`; chapter 03 §3.11 |
| 15:30 | market close | `trading_hours.market_close` |
| 15:40 → 16:22 | candle fetch, position reconcile, EOD cleanup, excursions, EOD verify, broker reconcile, S&R backfill, WAL checkpoint, screened CSV, **daily trade review**, trade journal, strategy metrics, registry officer | cron |
| 16:05 | the S&R shadow evaluator — **testing VM only**, hand-added, not in the registry | the live crontab capture |
| **17:35** | the service's own clean-shutdown time, taken only if no position still requires the service | `trading_hours.service_window_end`; `main.py:4177`, `:1305` |
| 17:05 · 18:00 · 18:15 · 18:45 · 18:50 | control tower; cron-drift check; forward-shadow record; system manager; Cron Officer EOD summary | cron |

## 1.7 The trade path, end to end

Each step names the chapter that owns it. Chapter 21 walks this same path as a single concrete trace and is the place where any contradiction between chapters must surface.

1. **A scanner fires** and posts to `POST /webhook/<scanner_name>`. The receiver authenticates, rate-limits per source IP, validates the payload, resolves symbol aliases, de-duplicates, enforces queue backpressure and per-signal expiry, writes a `signals` row and pushes a tuple onto the in-process queue (`signals/webhook_receiver.py`, chapter 05).
2. **The signal-processor pool drains the queue** and runs the admission pipeline: status write, kill-switch and entry-window and age checks, scanner→strategy lookup through `scan_webhook_map`, the strategy-control verdict (chapter 06).
3. **The secondary screener** fetches a quote, builds the market-data dictionary, runs ten steps through the step executor, scores them, applies the per-strategy minimum score, and persists exactly one verdict per signal. The newer `v3_chain` hard gate sits here in one of three modes — `off`, `shadow`, `enforce` (chapter 06).
4. **Entry price and stop are derived**, with an optional fresh-quote re-anchor for momentum strategies (chapter 08 — the chapter that also carries the whole reference → planned entry → buffer → submitted limit → fill chain).
5. **Position sizing** turns risk into a quantity, through the sizing rungs, the concentration and value caps and the lot rules (chapter 09).
6. **The risk engine approves or rejects**, running ten portfolio checks in a fixed order and short-circuiting on the first failure; it reads state but never mutates it (`capital/risk_engine.py`, chapter 09).
7. **Capital is reserved** in the fund manager, which writes its ledger row before touching memory and re-checks its invariant afterwards (`capital/fund_manager.py`, chapter 09).
8. **The order placer** creates the trade row, runs the last-mile gates, places the ENTRY leg, persists the order rows and registers each leg with the monitor (chapter 10).
9. **On the entry fill** it commits the reservation and places the deferred stop and target at the actually filled quantity; on an exit fill it closes the trade, cancels the OCO sibling and releases the used capital (chapters 10, 11, 12).
10. **The monitor and reconciler** poll order state, sweep orphans and reconcile against the broker (chapters 10, 13).
11. **At 15:17 the square-off** flattens the intraday book; delivery is excluded by design and carries on a broker-side GTT (chapter 12).
12. **After the close** the EOD jobs verify, reconcile against the broker book, compute metrics and produce the reports; alerts go out by Telegram and e-mail throughout (chapters 13, 14, 15).

## 1.8 The control planes

| Plane | What it does | Where |
|---|---|---|
| **Kill switch** | soft kill blocks new entries; hard kill flattens and halts. Its state is persisted in `kill_switch_state` and recovered at construction; prior-day and scheduled kills auto-clear at boot | `capital/kill_switch.py:313`; `main.py:2251`, `:2268`, `:2273` |
| **Boot guards** | the weekend/holiday guard and the service-start-window guard, both returning 0 before configuration is loaded | `main.py:2110`/`:2158`, `:2170`/`:2184` |
| **Startup checks** | 15 checks run by the aggregator (17 exist in the module; two are not called), including the four required secret **names**; any blocking failure is exit 3 | `utils/startup_checks.py:1508`; `main.py:2459`, `:218`, `:2510` |
| **Config auditor** | runs inside configuration validation and twice more once strategies are loaded; a BLOCK finding fails the boot | `core/config_loader.py:2170`; `main.py:3447`, `:3468` |
| **Capital invariant** | available + reserved + used must equal total, re-checked after every mutation, and a break fires a hard kill | `capital/fund_manager.py:2391`, `:2495` |
| **Cron Officer and drift check** | a daily reconciliation of the live crontab against the generated canonical, plus an EOD job-completion summary | chapter 03 §3.9 |
| **Effect telemetry** | a composition-root census of which side-effecting units exist, asserted at boot and reported at EOD | `main.py:4275`, `:4279`, `:1666` |

## 1.9 What the system did not do

- **It did not generate its own entry signals.** Without an external scanner posting to the webhook, nothing enters the pipeline.
- **It did not trade any instrument class other than NSE equities**, and `accounts.csv` naming a broker other than `zerodha` is a fatal exit 9 (`main.py:2580`).
- **It did not run unattended across a year boundary** without a new holiday file: the filename carries the year, and the guard reads the calendar before anything else.
- **It did not wait for its EOD exits to fill** — placement and hand-off only, by rule EOD7 (`orders/eod_squareoff.py:1313`).
- **It did not start itself from cron.** Nothing in the 42 scheduled jobs runs `systemctl start`.

## 1.10 What this chapter could not establish

- **Anything about production's running state.** Its configuration, crontab, installed units, database contents and mode are NOT ESTABLISHED; only its code, at `970aabf`, is RECORD-DERIVED.
- **Which mode each instance actually booted in.** The CLI default and the unit file disagree, and only the unit file was read (chapter 03 §3.13).
- **The contents of the testing VM's own `accounts.csv`** (228 bytes versus the repository's 704).
- **Whether the scanners were still posting.** The webhook ingress is described from code; no traffic was observed for this manual.

---

# Appendix 01-A — the measured divergences

## A.1 Testing VM versus `e7bf477`

RECORD-DERIVED from the 17-Sep-2026 20:06 IST comparison: the deployed files compared by git blob hash against `e7bf477` (the commit the twin runs — `970aabf` plus the S&R shadow files). The twin's own bare repository, at `20061b6`, does **not** describe the running files.

| # | What differs | On the testing VM | Deliberate? |
|---:|---|---|---|
| 1 | 1,340 files | **identical** to `e7bf477` | — |
| 2 | `core/config_loader.py`, `capital/position_sizer.py`, `main.py` | content differs — the `force_qty` build | yes: the closed change set delivered 17-Sep 19:31 |
| 3 | `config/system_config.yaml` | `position_sizing.force_qty` absent → **1** · `trading_hours.entry_start` 10:00 → **09:30** · `max_position_value_pct` 0.4 → **0.5** · `delivery_max_position_value_pct` 0.4 → **0.5** | yes: the same change set |
| 4 | `config/system_config.yaml` | `alerts.smtp.from_address`, `.to_addresses`, `.username` → the sandbox mailbox | yes: the twin's own mailbox |
| 5 | `config/cron_registry.yaml` | `reconcile_positions` and `refresh_instruments` pass `--account VBB097` instead of the production account | yes: the twin's account |
| 6 | `scripts/copy_token_to_vm.bat` | the target host is the twin's address, three lines changed, nothing else | consistent with a deliberate retarget; **no decision record was found** |
| 7 | 23 files | **CRLF-only** — identical once line endings are normalised | ⚠️ **cause UNRESOLVED.** Earlier records said "four CRLF files"; that four came from a check of specific files, this 23 is the whole tree — the number did not grow |
| 8 | 14 files | present on the VM, absent from `e7bf477` — `config/instruments.csv` (gitignored, refreshed daily), two `system_config.yaml` backups, six documents, three gitignored `.docx` manuals, a memory note, and a 0-byte file named `select` | mixed: `instruments.csv` by design; the rest NOT ESTABLISHED (the 0-byte `select` looks like a shell accident) |
| 9 | 10 files | in `e7bf477`, absent on the VM — the 8 S&R shadow test files, `scripts/sr_shadow_mutation_check.py`, and one design note | yes: the S&R deploy delivered 17 files and did not include the tests or the tooling |

⚠️ **`config/accounts.csv` is not in that comparison.** It was excluded from the snapshot as an account-identifier file, and the manifest records the VM's copy as **228 bytes** against the repository's **704**. The twin therefore runs a different account registry, and its contents are NOT ESTABLISHED.

## A.2 The file-count reconciliation

The snapshot repository holds **1,418** committed files. Thirteen of those are repository artifacts that are not part of the machine's tree (`README.md`, `SNAPSHOT_MANIFEST.md` and eleven `_machine/` captures), leaving **1,405** tree files. The manifest names **3,916** excluded files (18,208,587,107 bytes, dominated by database backups). **1,405 + 3,916 = 5,321.**

An earlier record put the VM tree at **5,322** files with **3,939** exclusions. The 3,939 predates the 23 reference-data CSVs being moved from the excluded set into the repository (3,939 − 23 = 3,916 ✓). The residual **one file** between 5,321 and the 5,322 counted by a live `find` at 20:06 is **not explained** and is recorded here rather than smoothed away.
