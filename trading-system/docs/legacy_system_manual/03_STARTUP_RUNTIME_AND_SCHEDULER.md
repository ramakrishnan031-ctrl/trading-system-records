# 03 — STARTUP, RUNTIME AND SCHEDULER

> **Evidence basis.** The PC worktree `D:/Projects/wt-sr-shadow-15sep` at commit **`e7bf477`** with the uncommitted **`force_qty`** change set in the working tree — byte-equivalent to the **TESTING VM** as delivered 17-Sep-2026 19:31 IST. ⚠️ Because `main.py`, `core/config_loader.py` and `capital/position_sizer.py` are modified in the working tree, **every line number below holds for the files as read, not for `e7bf477` alone.**
> **Machine-side facts** (the installed unit files, the real `crontab -l`, the armed deploy hook) are RECORD-DERIVED from the captures preserved in `trading-system-sbx-snapshot/_machine/`, taken from the testing VM on 17-Sep-2026 at 20:06 IST. They are labelled RECORD-DERIVED where used.
> **PRODUCTION WAS NEVER READ.** No statement here describes the production host.
> **Evidence date:** 18-Sep-2026. The system is retired; this chapter describes how it started, ran and stopped. Defects noticed while writing are registered in chapter 22 and nowhere else.

---

## 3.1 What actually starts this system

Two independent mechanisms start work on this host, and they do not start each other.

| Mechanism | What it starts | Declared where | Installed where |
|---|---|---|---|
| **systemd** | the long-running trading service (`main.py`), plus five watcher units and one timer | `deploy/systemd/*.service` (7 files, in git) | `/etc/systemd/system/` — **8** units are installed (RECORD-DERIVED capture) |
| **cron** | 42 scheduled jobs: token refresh, pre-flight, metrics, EOD reports, retention, drift checks | `config/cron_registry.yaml` (47 jobs) → generated into `deploy/cron/trading-system.cron` (46 entries) | the `ubuntu` user's crontab — **42** active entries (RECORD-DERIVED capture) |

**FACT — nothing in cron starts the trading service.** Across `config/cron_registry.yaml` and the four consuming programs (`core/cron_registry.py`, `scripts/cron_officer.py`, `scripts/check_cron_drift.py`, `scripts/generate_crontab.py`) the only `crontab` invocations are **reads** — `crontab -l` at `scripts/cron_officer.py:557`, `scripts/cron_officer.py:890` and `scripts/check_cron_drift.py:135`. No cron job runs `systemctl start`. The service is started by systemd (boot, or a manual `systemctl start`) or by the token-watcher unit described in §3.8.

---

## 3.2 The service unit, as installed

`ExecStart` runs the venv interpreter against `main.py` **with `--mode live`** (`deploy/systemd/trading-system.service:19`; identical in the installed capture). The unit sets `WorkingDirectory=/home/ubuntu/systems/trading-system`, `EnvironmentFile=.../.env`, `StandardInput=null`, `KillSignal=SIGINT` and `TimeoutStopSec=30`.

| Directive | Value | What it means here |
|---|---|---|
| `Type` | `simple` | systemd considers the service started the moment the process forks; readiness is not reported |
| `User` / `Group` | `ubuntu` | the same account whose crontab holds the 42 jobs |
| `Environment` | `PATH=/home/ubuntu/systems/venv/bin:...`, `PYTHONUNBUFFERED=1` | the venv interpreter comes first on `PATH` |
| `EnvironmentFile` | `/home/ubuntu/systems/trading-system/.env` | systemd injects the secrets into the process environment; **the file's own comment in the unit is the only declaration of this dependency** |
| `StandardInput` | `null` | headless by design: an accidental interactive prompt fails instead of hanging |
| `KillSignal` | `SIGINT` | `systemctl stop` runs the same handler as Ctrl+C, so the clean-shutdown path of §3.9 executes |
| `Restart` | `on-failure`, `RestartSec=10` | exit 0 never restarts |
| `RestartPreventExitStatus` | `3 4 5` | **only** those three codes suppress a restart |
| Hardening | `NoNewPrivileges`, `ProtectSystem=full`, `ProtectHome=false`, `PrivateTmp=true` | — |

**FACT — the machine carries one unit that the repository does not.** The repository has **7** unit files; the machine has **8** installed. `gui-dashboard.service` exists only on the machine — there is no file for it anywhere in the tree (chapter 25 covers the dashboard it starts).

**FACT — installing a unit is a manual act, and drift already exists.** Comparing each repository unit with its installed capture, ignoring blank lines:

| Unit | Repo vs installed |
|---|---|
| `alert-watcher.service` | identical |
| `cron-watchdog.service` | identical |
| `cron-watchdog.timer` | identical |
| `security-watcher.service` | identical |
| `token-watcher.service` | identical |
| `trading-system.service` | **differs**: the installed copy lacks two comment lines the repo has (the `Exit 4 = HALT` note), and the machine carries a drop-in, `trading-system.service.d/watchman.conf`, which adds `Wants=trading-watchman.service`. The drop-in exists in no repository file |
| `trading-watchman.service` | **differs**: the installed `Environment=PATH=...` omits the `/home/ubuntu/tools/antigravity` element the repo version has — a functional difference, not a comment |

## 3.3 The boot sequence

Boot runs in three code regions: **module import**, **`main()`** (`main.py:2093`–`2198`) and **`_main_locked()`** (`main.py:2201`–`4314`). 154 steps of this sequence were traced and each one's quoted line re-checked against the file; §3.12 gives the accounting.

### 3.3.1 Import time — where `.env` is read

**FACT.** `main.py` never calls `load_dotenv()` itself. It imports `scripts.zerodha_login` at `main.py:106`, and that module executes a bare `load_dotenv()` at `scripts/zerodha_login.py:36` — no explicit path, so resolution is relative to the process working directory.

⚠️ **INTERPRETATION.** Under systemd the environment arrives through `EnvironmentFile` before the process starts, so this import-time load is redundant there. Run by hand from another directory, it is the only loader — and it may find nothing. **UNKNOWN:** which of the two paths actually supplied each variable on any given day is not determinable from the code.

Also at import time: a module-level `ThreadPoolExecutor(2)` for entry-gate work is created at `main.py:865`, and the process entry point is `sys.exit(main())` at `main.py:4323`.

### 3.3.2 `main()` — four things happen before any log file exists

1. **Argument parsing** (`main.py:2098`). `--mode paper|live` (default **paper**, `main.py:185`–`186`), `--resume`, `--config`, `--status`, `--dry-run`, `--version`, `--interactive`. An argparse `SystemExit` becomes **exit 5** (`main.py:2209`; and `return 5 if se.code != 0 else 0` at `main.py:2104`).
2. **`--version`** prints and returns 0 (`main.py:2102`).
3. **The weekend/holiday guard** (`main.py:2110`) — `is_trading_day(today, config_dir)`, where `today` comes from `date.today()`, the **host's local date** (`main.py:2108`). On a non-trading day it prints a banner, writes a sentinel file and **`return 0`** at `main.py:2158`. Inside the guard, the weekend test returns False before the holiday file is even consulted (`utils/holiday_guard.py:92`). A missing holiday file raises `FileNotFoundError`, which is caught so that startup proceeds.
4. **The service-START-window guard** (`main.py:2170`) — outside the START window the process prints the window and **`return 0`** at `main.py:2184`. `--status`, `--dry-run` and `--interactive` bypass it, as does `TS_IGNORE_MARKET_WINDOW=1` or `--resume`. Its own comment records that it runs *before* `load_all()` and therefore cannot know the configured stop time.

   The window is `[SERVICE_WINDOW_START, SERVICE_START_CUTOFF)` = **`[08:00, 18:15)`** (`main.py:2008`–`2009`, predicate at `main.py:2023`), a pure time-of-day test and so host-timezone independent by its own docstring. The upper bound is `SERVICE_WINDOW_END_MAX = 18:15` from `core/config_loader.py:83`, the same constant the configuration validator uses to require `market_close <= service_window_end < 18:15` (`core/config_loader.py:180`) — the reason given there is that 18:15 is the forward-shadow recorder's cron time. ⭐ So the *start* window and the ceiling on the configured *stop* time are one constant.

⭐ **Both guards return before `setup_logging`** (`main.py:2186`), before the config load, and therefore before any secret is required. **A clean exit here proves nothing about configuration, credentials or the broker token.** Logging is configured only at `main.py:2186`; the single-instance lock is taken at `main.py:2191` (an OS file lock plus a TCP bind on `127.0.0.1:5001`), and a failure to acquire it is **exit 1** (`main.py:2194`).

### 3.3.3 `_main_locked()` — phases 0b to 0h

| Phase | What it does | Anchor |
|---|---|---|
| **0b — config** | `load_all` reads, hashes and validates every configuration file | `main.py:2206` |
| | config values registered for usage tracking | `main.py:2213` |
| | the configured service STOP time parsed once and logged | `main.py:2219` |
| **0c — state** | `StateStore` opens `data_store/trading_system.db`; this is the only sanctioned schema migrator | `main.py:2241` |
| | event bus constructed | `main.py:2246` |
| | `KillSwitch` built, recovering persisted state from `kill_switch_state` | `main.py:2251`, `capital/kill_switch.py:313` |
| | `TimeAuthority` configured with clock skew thresholds | `main.py:2262` |
| | prior-day kills auto-cleared; same-day *scheduled* kills auto-cleared | `main.py:2268`, `main.py:2273` |
| | startup scenario detected — COLD / WARM / CRASH / HALT | `main.py:2276` |
| | **HALT without `--resume` → exit 4** | `main.py:2298` |
| | config-hash diff against the last session row | `main.py:2303` |
| | early session row written (`INSERT OR REPLACE INTO session id=1`) | `main.py:2316` |
| **0d — checks** | market windows built from `trading_hours`; order state machine; rate limiter | `main.py:2328`, `:2354`, `:2356` |
| | **paper**: no Kite client at all, adapter gets a quote provider | `main.py:2360` |
| | **live**: `accounts.csv` pre-read, account env alias, token file read, `KiteConnect` built | `main.py:2367`–`2383` |
| | broker adapter constructed (needed by the clock-skew check) | `main.py:2391` |
| | full account registry load; failure → **exit 3** | `main.py:2422`, `:2431` |
| | required-secret **names** assembled | `main.py:2438` |
| | instrument master pre-loaded from `config/instruments.csv` | `main.py:2449` |
| | the aggregate startup checks run — **15** of them (§3.5) | `main.py:2459` |
| | `--dry-run` prints the report and returns | `main.py:2484` |
| | any blocking failure → **exit 3** | `main.py:2510` |
| | live non-interactive token gate; missing/expired → **exit 6** | `main.py:2555`, `:2560` |
| | resolved config persisted to `config_snapshots` (idempotent) | `main.py:2611` |
| **0e — subsystems** | Telegram notifier; notifier and adapter late-bound into the kill switch | `main.py:2636`, `:2656`, `:2661` |
| | capital: bucket split resolved, `FundManager` constructed and seeded | `main.py:2710`, `:2726`, `:2769` |
| | capital rehydration replays `fm_ledger` / `trades` / `orders` for open trades | `main.py:2823` |
| | `PositionSizer`, `RiskEngine` | `main.py:2848`, `:2906` |
| | live feed, candle store, shadow tracker, tick dispatcher | `main.py:2937`, `:2950`, `:2956`, `:2981` |
| | order monitor, GTT placer (+ hydration from `gtt_state`), order placer, GTT monitor, reconciler, TGT retry | `main.py:3008`, `:3037`, `:3049`, `:3071`, `:3119`, `:3134`, `:3154` |
| | strategy YAMLs loaded; scoring and screening chain built | `main.py:3169`, `:3240` |
| | EOD square-off (15:17 backstop) and MIS square-off timing | `main.py:3310`, `:3339` |
| | webhook receiver constructed — Flask object only | `main.py:3417` |
| | **config auditor runs a second and third time** with strategies loaded | `main.py:3447`, `:3468` |
| | signal processor and entry gate | `main.py:3609`, `:3874` |
| | event-bus subscriptions | `main.py:3882`–`3901` |
| **0f — reconcile** | `reconcile_once()` runs **synchronously**, then a stale-order sweep; if it tripped the kill switch → **exit 1** | `main.py:3915`, `:3926`, `:3929` |
| **0g — start** | candle store, tick feed, order-monitor re-tracking, `_fill_map` rehydration, signal handlers, then the threads | `main.py:3957`–`3999` |
| | a boot-order invariant is asserted: the synchronous reconcile must have run first | `main.py:4003` |
| | **webhook listener bound and started** — Waitress, not Flask's dev server | `main.py:4023`, `:4035` |
| | 2-second sleep, then a self-check against `http://127.0.0.1:<bind_port>/health`; unreachable **degrades** the boot rather than halting it | `main.py:4038`, `:4040`, `:4069` |
| | **second listener**: health server on `127.0.0.1:8080`, loopback-only | `main.py:4109` |
| | EOD scheduler, 14:45 pre-alert, 09:15 margin re-sync, EOD self-exit watchdog | `main.py:4129`, `:4138`, `:4148`, `:4170` |
| **0h — mark** | `STARTUP` row in `system_events`; session row rewritten; "System Active" Telegram sent | `main.py:4203`, `:4209`, `:4226` |
| | composition-root registration and the effect-composition assertion | `main.py:4275`, `:4279` |
| **runtime** | the main thread waits on a shutdown event — that is the whole runtime loop | `main.py:4284` |

## 3.4 Configuration loading and validation

**FACT — one directory, no search path.** `config_dir = Path(args.config) if args.config else Path("config")` (`main.py:2107`): the literal relative path `config` against the process working directory, unless `--config` is given. There is no environment variable and no fallback location.

**FACT — the file set is a fixed registry of eight files.** `_CONFIG_FILES` at `core/config_loader.py:2536` holds the (key, filename, model) triples: `system_config.yaml`, `broker_costs.yaml`, `broker_limits.yaml`, `slippage_model.yaml`, `scoring_weights.yaml`, `scan_webhook_map.yaml`, `chartink_scanners.yaml` and `nse_holidays_<year>.yaml`. The only computed filename is the holiday file, whose year is derived at `core/config_loader.py:2544`. The 16 strategy YAMLs under `config/strategies/` are **not** in this registry; they are loaded separately at `main.py:3169`. `system_config.yaml` itself carries 43 top-level sections.

⚠️ **KNOWN DEFECT (parked for chapter 22).** The holiday filename's year comes from a naive local `date.today()` at `core/config_loader.py:2544`, while the guard that runs ~2,400 lines earlier reads the same calendar through its own path. A year boundary therefore depends on the host's local date in two places rather than one.

**FACT — the order inside `load_all` is: exist → hash → parse → validate.** Existence first, a missing file raising `ConfigMissingError` (`:2578`); the raw bytes SHA-256 hashed **before** parsing, so the hash describes the bytes on disk (`:2586`); `yaml.safe_load` only, with environment-variable interpolation forbidden by rule CL5 (`:20`–`21`, parse at `:2589`); an empty file normalised to `{}` rather than rejected (`:2598`); then per-file Pydantic validation (`:2602`).

**FACT — every configuration model forbids unknown keys.** `core/config_loader.py` defines **67** top-level classes and carries exactly **67** `model_config = ConfigDict(extra="forbid")` lines, the first at `:87`. The rule is also stated in prose as CL3 at `:16`. ⭐ This is the mechanism by which *any* unknown key in a configuration file fails the boot rather than being ignored.

**FACT — the auditor runs inside validation, and twice more later.** `SystemConfig`'s `mode="after"` validator invokes the config auditor at `core/config_loader.py:2170`; a BLOCK finding raises and Pydantic wraps it into a `ValidationError` (`:2175`). Group A is then re-run at `main.py:3447` with the loaded strategies, and again at `main.py:3468`.

## 3.5 Startup checks, and the secrets the boot requires

**FACT.** `required_startup_secrets(primary_account_id)` at `main.py:218` returns four environment-variable **names**, required in **both** paper and live:

- `ZERODHA_API_KEY_<account>` · `ZERODHA_API_SECRET_<account>` · `TELEGRAM_BOT_TOKEN` · `WEBHOOK_SECRET`

Its docstring records the reason for the fourth: decision **C-2** of 02-Jul-2026 made `WEBHOOK_SECRET` mandatory in every mode, because paper previously omitted it and an unset secret made the paper webhook accept unsigned requests. The blocking check that enforces the list is `utils/startup_checks.py:1556`, and any blocking failure is **exit 3** (`main.py:2510`).

**FACT — 15 checks run, out of 17 that exist.** `run_all_startup_checks` (`utils/startup_checks.py:1508`–`1691`) calls exactly **15** distinct `check_*` functions, each once: config files present, config hash, required secrets, strategy configs, temp config values, holiday calendar, market holiday today, clock skew, NTP sync, SDK version, DB permissions, disk space, instrument cache size, scanner connectivity, webhook endpoint. The module defines **17**; `check_kill_switch_present` and `check_paper_capital_consistency` are **not** called by the aggregator. *(An earlier trace of this sequence reported 16; the count above was re-derived by listing the call sites.)*

⛔ **No secret value appears in this manual.** Only names. Chapter 18 states where the values lived and what class they are.

## 3.6 What the process is running once boot completes

| Listener / thread | Where | Detail |
|---|---|---|
| Webhook HTTP listener | `main.py:4023`, `:4035` | Waitress serving the Flask app from `signals/webhook_receiver.py`; bind host and port come from config. The receiver's own comment records the deployed endpoint as `0.0.0.0:5000`, open for the external scanner (`signals/webhook_receiver.py:366`) |
| Health / metrics server | `main.py:4109` | `127.0.0.1:8080`, loopback-only by decision C-3, because `/health` and `/metrics` expose P&L, capital and kill-switch posture (`scripts/healthcheck_server.py:301`) |
| Instance lock | `main.py:2191` | file lock plus a TCP bind on `127.0.0.1:5001` |
| Poll threads | `main.py:3995`–`4012` | order monitor, order reconciler, clock-skew probe (live only), token monitor, signal-processor pool, entry gate, smart-TGT trail, TGT retry |
| Timed daemons | `main.py:3367`, `:3369`, `:4129`, `:4138`, `:4148`, `:4170` | MIS square-off notifier, MIS auto square-off, EOD scheduler, 14:45 EOD pre-alert, 09:15 margin re-sync, EOD self-exit watchdog |
| Broker token monitor | `main.py:3398` | live polls `kite.profile` every 1800 s; a no-op in paper |

## 3.7 Exit codes, and which ones systemd restarts

| Code | Meaning | Anchor | Restarts? |
|---:|---|---|---|
| 0 | holiday/weekend guard, service-window guard, `--version`, `--status` | `main.py:2158`, `:2184`, `:2102`, `:650` | no (`Restart=on-failure`) |
| 1 | instance lock failed; kill switch active after startup reconcile; `TradingSystemError` at top level | `main.py:2194`, `:3934`, `:4326` | **yes**, after 10 s |
| 2 | unexpected exception at top level | `main.py:4329` | **yes** |
| 3 | startup failure — `accounts.csv` load, strategy configs, `StartupCheckFailed`, and four more sites | `main.py:2431`, `:2510`, `:2786`, … (7 sites) | no |
| 4 | startup scenario HALT without `--resume` | `main.py:2298` | no |
| 5 | argparse error; interactive path with a missing credential env var | `main.py:2209`, `:1906`, `:1909` | no |
| 6 | live token file missing or expired; missing credential env var | `main.py:2378`, `:2382`, `:2560` | **yes**, every 10 s |
| 7 | interactive confirmation declined | `main.py:1954` | **yes** |
| 8 | interactive account selection cancelled | `main.py:1866` | **yes** |
| 9 | `accounts.csv` names a broker other than `zerodha` | `main.py:2580` | **yes** |

⚠️ **KNOWN DEFECT (registered in chapter 22).** `RestartPreventExitStatus=3 4 5` suppresses three codes. Exit **6** — the live token being missing or expired — is not among them, so a token problem produces an unbounded restart every 10 seconds rather than a single loud failure. The same holds for 1, 2, 7, 8 and 9.

## 3.8 The broker token chain

47 steps were traced across the cron entries, `scripts/auto_refresh_token.py`, the Windows-side helpers and the runtime read. In order:

| When | What | Anchor |
|---|---|---|
| 05:00 **every** day, including weekends and holidays | cron deletes `data_store/session/zerodha_token.json` | `deploy/cron/trading-system.cron:43`; declared at `config/cron_registry.yaml:157` |
| 08:15 Mon–Fri | cron runs the headless refresh; its entry point is `_cron_main`, **not** `main`, so the service's holiday guard does not apply — the script has its own | `deploy/cron/trading-system.cron:52`; `scripts/auto_refresh_token.py:420`, `:414` |
| | the script loads `.env` itself, in addition to cron's `. ./.env` | `scripts/auto_refresh_token.py:53` |
| | account resolved from `config/accounts.csv`; credentials resolved by account-specific env **name** first, then a generic fallback | `:340`, `:349` |
| | on a missing credential it logs the missing **key names only** | `:367` |
| | headless login: password POST, then a TOTP 2FA POST, then the `request_token` is recovered from a redirect rather than the 2FA response | `:58`, `:189`, `:132` |
| | the token is written to `<repo>/data_store/session/zerodha_token.json` | `:61` |
| at service boot (live) | the token file is read and validated for account match and freshness; missing or expired → **exit 6** | `main.py:2370`, `:2555`, `:2560` |
| during the session (live) | the token monitor polls `kite.profile` every 1800 s | `main.py:3398` |

**UNKNOWN, and stated as such:** which OS user's crontab holds the canonical file on the VM (the hook installs it with a bare `crontab`, which targets the invoking user); where the `trading-vm` SSH alias in the Windows helpers points; and whether anything on the PC schedules `deploy/zerodha_morning.ps1` at all — nothing in this tree invokes it, and its own header says it is run by hand.

## 3.9 The scheduler: registry → canonical → live crontab

### The three artifacts, and the arithmetic that ties them

| Artifact | What it is | Entries |
|---|---|---:|
| `config/cron_registry.yaml` | the declared source of truth — 767 lines, a `jobs:` map plus an `officer:` block at line 757 | **47 jobs** |
| `deploy/cron/trading-system.cron` | the generated canonical crontab, committed to git | **46 active** |
| the machine's real `crontab -l` | RECORD-DERIVED capture, 17-Sep 20:06 IST | **42 active** |

**47 − 1 disabled (`daily_report`) = 46 canonical. 46 − 5 hand-commented `gemini_*` + 1 hand-added `sr_shadow_evaluate` = 42 live.** Both identities hold on the measured counts.

Registry totals, measured by loading the YAML: **9** jobs `critical: true` · **34** `monitored: true` · **32** `market_day_only: true` · **42** python, **5** shell · **22** carry a `marker_name` · **1** disabled. Every job declares the same twelve fields; `log_target` appears on 45, `detection_method` on 5.

The `officer:` block sets the Cron Officer's day window and thresholds: `day_window_start 00:00`, `day_window_end 23:59`, `morning_briefing_time 09:20`, `eod_floor_time 18:45`, `eod_gap_minutes 5`, `miss_grace_minutes 2`, `telegram_ban_until null`.

### Why the daily drift check has two standing findings

The 18:00 job compares the live crontab against the canonical file in both directions. Two differences are permanent and deliberate, so the check reports them every day:

| Direction | Jobs | Why |
|---|---|---|
| in canonical, missing from live | the five `gemini_*` jobs | all five declare `enabled: true` **and** `monitored: true` in the registry, and all five are commented out in the live crontab with `# DISABLED 09-Sep-2026 (Rama): AI tooling off on the testing VM` |
| in live, missing from canonical | `sr_shadow_evaluate` (`5 16 * * 1-5`) | hand-added on the testing VM only; the registry does not declare it, so the generator cannot emit it |

⭐ **INTERPRETATION.** The daily CRITICAL drift report is therefore an expected consequence of two human decisions, not a failure of the scheduler. Reconciling it would mean either editing the registry or re-enabling the jobs — both decisions, neither of them this manual's business.

### The full schedule

The 47 declared jobs, in clock order, with the registry line each is declared on, its cron expression, criticality, monitoring flag, market-day flag, the program it runs and where its output goes, appear in **Appendix 03-A** at the end of this chapter.

## 3.10 What a push does — the deploy path

**FACT, RECORD-DERIVED** from the hook armed on the VM's bare repository (`_machine/bare-repo-hooks/post-receive`, 41 lines; byte-identical to `deploy/hooks/post-receive` in the tree):

1. On a push to `refs/heads/main` it runs `git --work-tree=/home/ubuntu/systems/trading-system --git-dir=/home/ubuntu/trading-system.git checkout -f main`. **A push therefore overwrites the deployed working tree, discarding any local edit there.**
2. It then regenerates the crontab from the **deployed** registry and compares it with the deployed canonical file. If they match it runs `crontab deploy/cron/trading-system.cron` and prints `post-receive: crontab AUTO-INSTALLED from canonical.` If they do not match it prints a warning and installs nothing.
3. It prints `Deployment complete.`

⚠️ **What the hook does not do:** it never installs a systemd unit. Unit files and drop-ins are a manual act on the machine, which is why §3.2 finds drift and one unit with no repository file at all.

⚠️ **HISTORICAL, and recorded in the hook's own header:** an earlier version of that header claimed this was *not* the armed hook and that the live one was checkout-only. The header now records that the claim was false, that an md5 comparison proves this file is the armed hook, and that a real push on 17-Jul-2026 printed the AUTO-INSTALLED line, which only this version can print. The header also warns that nothing auto-installs the hook itself, so it must be re-armed from the deployed tree after any edit.

## 3.11 End of day, and shutdown

Two different mechanisms, often conflated: a **square-off** that flattens intraday positions, and a **process shutdown** that ends the service. 95 steps were traced.

### 3.11.1 The 15:17 square-off

**Trigger.** A daemon thread started at `main.py:4129` calls `EodSquareoff.check_and_fire(now_ist())` every `eod_squareoff.poll_interval_sec` (5 s, `main.py:4131`). It fires when the IST clock reaches `trading_hours.eod_squareoff_time` — **"15:17"** in `config/system_config.yaml:49`, compared at `core/market_windows.py:205` — on a non-holiday date, and **once per IST date** (an in-memory per-date claim, `orders/eod_squareoff.py:215`, `:217`, `:227`). The time source is the VM clock rendered in IST (`core/time_authority.py:99`).

**The fire sequence, in order:**

| # | Step | Anchor |
|---:|---|---|
| 0 | clear entry-gate state — ⚠️ **dead in this wiring**: the entry gate is never wired into this object | `orders/eod_squareoff.py:341` |
| 0b | clear parked `WAIT_FOR_RETEST` candidates | `:353` |
| 1 | **write-ahead**: an `IN_PROGRESS` row into `eod_squareoff_log` with zero counts | `:364`, `core/state_store.py:1365` |
| 2 | `soft_kill("EOD_SQUAREOFF")` so no new entry can start mid-sequence | `:383` |
| 3 | **PASS 1** — cancel pending intraday ENTRY orders (`PENDING_FILL`, product MIS or CO only; a CNC/delivery entry is out of scope), mark the trade and order rows CANCELLED, release the reservation with reason `EOD_CANCEL` | `:397`, `:400`, `core/state_store.py:1035`–`1036`, `:898`, `:902`, `:910` |
| 4 | cancel resting SL/TGT legs of open intraday positions (non-terminal legs only) | `:407`, `core/state_store.py:1163`–`1164` |
| 5 | a hard **2-second sleep** between the passes, so a fill racing a cancel is seen | `:424` |
| 6 | **PASS 2** — exit open positions. Broker truth is fetched once and used to filter the local candidate set; a local row the broker does not know is skipped as stale | `:430`, `:1063`, `:1086`, `:1107` |
| 7 | per product: **CO** is closed by cancelling the CO's second leg; **MIS / LIMIT_TRIPLE** is exited with a LIMIT priced from the LTP, falling back per symbol when no usable LTP exists; every phase-1 exit carries the broker tag `EOD_SQ` | `:1166`, `:1198`, `:1257`, `:1275`, `:1280`, `:1294`, `:1300`, `:1307` |
| 8 | orders are staggered by `eod_squareoff.inter_order_delay_sec` | `:1379` |
| 9 | **one** sleep of `limit_grace_sec` (120 s), then still-open LIMITs are cancelled and replaced with MARKET | `:1392`, `:1395`, `:1645`, `:1663` |
| 10 | a residual broker sweep re-queries the broker and flattens any still-open MIS position it owns; a residual with no local trade is out of scope | `:1418`, `:1447`, `:1488`, `:1557` |
| 11 | the reconciler's stale-order sweep is invoked | `:444` |
| 12 | the one-line EOD summary is logged; the `IN_PROGRESS` row is transitioned to `COMPLETE`, with a single-shot INSERT fallback if the UPDATE fails | `:453`, `:465`, `:482`, `core/state_store.py:1397` |
| 13 | a **TRUNCATE** WAL checkpoint runs | `:501`, `core/state_store.py:313` |
| 14 | `EodSquareoffComplete` is published; its only non-test subscriber is the shadow tracker | `:514`, `orders/shadow_tracker.py:415` |
| 15 | **daily realized P&L is reset**, writing an `fm_ledger` row | `:531`, `capital/fund_manager.py:1704` |
| 16 | the SOFT_KILL is resumed **only if this module set it** | `:537` |
| 17 | the EOD daily-summary Telegram is sent | `:562` |

**Fill confirmation is out of scope by design** (rule EOD7, `:1313`): the sequence places exits and hands off; it does not wait to see them filled.

**Restart recovery.** At boot, `post_wire_init` inspects `eod_squareoff_log`: an `IN_PROGRESS` row re-fires the sequence in recovery mode; with no row it returns if the time is not yet due, and handles the past-EOD-before-close case separately (`:1750`, `:1788`, `:1825`, `:1887`).

**⛔ DELIVERY is excluded at the query** (`core/state_store.py:1246`), as the module's own design note states (`:23`). Delivery positions are carried, with their stop and target as a broker-side OCO GTT. **UNKNOWN:** how delivery is closed at end of day is not established by this chapter's sources.

### 3.11.2 Process shutdown

**Triggers.** The self-exit daemon is armed only for a normal service start (`main.py:4164`); its stop time is the configured `trading_hours.service_window_end` (`main.py:4177`, `config/system_config.yaml:112`). Before that time the gate returns not-due (`main.py:1270`); it also refuses while a HARD_KILL flatten is in progress (`main.py:1272`). When due it reads the pipeline state and is due **only if zero positions still require this service** (`main.py:1288`, `:1305`), with a fallback if that read raises (`main.py:1323`). It then logs and sends an "EOD Clean Shutdown" alert (`main.py:1525`). Externally, the SIGINT/SIGTERM handler sets the same event (`main.py:1573`) — which is what `systemctl stop` does, because the unit sets `KillSignal=SIGINT`.

**Teardown order** (`_shutdown`, first log line at `main.py:1631`): drain the HARD_KILL flatten worker first (`:1646`) → emit the EOD effect census (`:1666`) → stop the webhook receiver so no new signal arrives (`:1687`) → cancel pending ENTRY orders (`:1776`) → stop the order monitor, clock-skew probe, token monitor and live feed (`:1782`) → send a "System Stopping" alert (`:1805`) → write a `SHUTDOWN` row to `system_events` (`:1815`) → a **PASSIVE** WAL checkpoint (`:1824`) → close the store (`:1836`) → log **`Shutdown complete`** (`main.py:1839`), the final statement of the function.

⭐ **Why that matters operationally.** The shutdown gate is conditional on no position requiring the service. A carried position therefore prevents the clean shutdown, and the process stays up. `Shutdown complete` is the only positive evidence that the sequence finished.

## 3.12 Verification accounting for this chapter

The startup, config, token, unit, scheduler and EOD sequences were traced by six parallel research agents, each returning ordered steps with a file, a line and **the verbatim text of that line**. Every step was then re-checked against the file:

| Surface | Steps | Quote matched the cited line | Re-anchored | Rejected |
|---|---:|---:|---:|---:|
| `main.py` boot | 154 | 154 | 0 | 0 |
| systemd units and deploy | 98 | 98 | 0 | 0 |
| EOD and shutdown | 95 | 95 | 0 | 0 |
| cron registry and drift | 47 | 47 | 0 | 0 |
| broker token chain | 47 | 47 | 0 | 0 |
| config load and validation | 39 | 39 | 0 | 0 |
| **total** | **480** | **480 (100%)** | **0** | **0** |

Independently of the agents, the following were measured directly for this chapter: the 47-job registry parse and its flag totals; the 46/42 canonical-versus-live counts; the seven-versus-eight unit comparison and its two diffs; the 67 strict configuration models; the exit-code inventory; and the schema table counts quoted in §3.11. Where an agent's number and mine disagreed, mine was re-derived and the disagreement resolved before writing: the registry is **767** lines, not 768 — an earlier count of my own had added one for the trailing newline.

## 3.13 What this chapter could not establish

- **Which mode production boots in.** The CLI default is `paper` (`main.py:185`–`186`) and the repository unit says `--mode live` (`deploy/systemd/trading-system.service:19`). The testing VM's installed unit also says `--mode live`. Production's unit was never read. **NOT ESTABLISHED.**
- **The deployed configuration, precisely.** Every time and threshold quoted above is read from `config/system_config.yaml` **in the worktree**, which is `e7bf477`'s copy. For the **testing VM** the difference is measured and bounded (chapter 01's appendix): four `position_sizing` / `trading_hours` keys and three SMTP address keys, nothing else — so `eod_squareoff_time` 15:17, `service_window_end` 17:35, `market_open` 09:15 and the EOD protocol knobs hold on the twin as written here, while the twin's `entry_start` is **09:30**, not the 10:00 in this worktree. For **production**, every one of these values is **NOT ESTABLISHED**.
- **Which `.env` path actually supplied each variable** on a given run (§3.3.1).
- **Who installs the crontab, and into which user's table.** The hook runs a bare `crontab`, which targets the invoking user; the capture is the `ubuntu` user's table. Other users' crontabs were never examined and would need root.
- **The SQL behind three boot calls** — `fund_manager.rehydrate_from_open_trades`, `today_realized_pnl_carryover`, and `order_reconciler.reconcile_once()` / `sweep_stale_orders`. Their tables are named from docstrings, not from the statements; chapters 09, 10 and 16 own them.
- **What the MIS auto square-off unit does**, versus the 15:17 sequence that `config/system_config.yaml:49` itself calls an emergency backstop.
- **How delivery/CNC positions are closed at end of day** (§3.11.1).
- **What writes `eod_verification` and `eod_broker_reconciliation`**, and when — the cron jobs exist (`eod_verify`, `eod_broker_reconcile`); their programs were not read here.
- **Whether the pre-receive guard** that the generator's comments claim rejects a hand-edited canonical actually exists. Asserted only in comments at `scripts/generate_crontab.py:178`–`182`; no such hook was verified.
- **Whether the live host's crontab still matches the capture.** The capture is 17-Sep 20:06 IST. Nothing was read from any machine while writing this chapter.

---

## Appendix 03-A — the 47 declared jobs

See `03A_CRON_REGISTRY_TABLE.md` beside this file: one row per declared job with its registry line, declared schedule, cron expression, type, criticality, monitoring flag, market-day flag, program and log target, followed by the registry→canonical→live reconciliation and the unit and hook tables in full.
