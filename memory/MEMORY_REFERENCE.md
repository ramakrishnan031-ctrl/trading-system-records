# Memory — STABLE REFERENCE

**Look here when you touch the area named.** Split out of `MEMORY.md` on **25-Jul-2026** — every line below is **VERBATIM**, nothing summarised.
Hazards/DO-NOTs stay **HOT** in **[`MEMORY.md`](MEMORY.md)** · open work in **[`MEMORY_BOARD.md`](MEMORY_BOARD.md)** · closed work in **[archive](MEMORY_ARCHIVE_2026H1.md)**. Same byte budget applies.

## System & environment
- [SATS tooling](sats_tooling.md) — PC-only manual SAST (Bandit+Semgrep); `sats\scripts\scan_*.bat` → `sats\reports\`; git-ignored
- [Token workflow (21-Jun)](token_workflow_confirmed_21jun.md) — AUTOMATIC: 05:00 delete → 08:15 TOTP refresh → token-watcher starts app. `auto_refresh_token` gates whether the system trades at all.
- [VM Architecture LOCKED (161.118.187.249)](project_vm_architecture_locked.md) — ubuntu; shared venv; IST; bare `~/trading-system.git` → post-receive checkout to `/home/ubuntu/systems/trading-system` (tree NOT a git repo). GUI = Waitress `127.0.0.1:8500` behind `tailscaled`.
- [Master project state](project_master_state.md) — LIVE since 11-May-2026 · [PHASE 21 COMPLETE (17-May)](project_phase_21_complete.md) — 92+ fixes; 2112 tests

- 🔒 [SSH/root-probe audit (30-Jul)](ssh_root_probe_audit_30jul.md) — **0 root + 0 non-pk/ubuntu logins; `permitrootlogin no` confirmed via `sshd -T` on the RUNNING daemon.** ⛔ auth-log retention ceiling **50 d** — "ever" is unanswerable. ⛔ grep the main sshd_config alone ⇒ wrong answer.

## Working how-tos (their absence costs time, not capital)
- 🔴 **[Deployed-tree drift check needs `update-index --refresh`](deployed_tree_check_needs_refresh_20aug.md)** — `read-tree`→`diff-files` alone called **1,309 files modified on an IDENTICAL tree**. ⛔ Never report the un-refreshed output as drift; pair it with `md5sum`-vs-blob.
- [Naive IST timestamps in tests](feedback_naive_ist_timestamps.md) — now_ist().replace(tzinfo=None)
- [Reply style (Web Claude only)](feedback_reply_style.md) — short replies; long content to .txt
- [SSH key passwordless](feedback_ssh_automation.md) — trading_vm_secure has no passphrase
- [Use VM terminal for curl](feedback_vm_curl_tests.md) — PowerShell escaping breaks JSON
- [Transfer VM scripts via base64](feedback_vm_script_transfer_base64.md) — heredoc over ssh halves backslashes; base64 instead
- [in_flight is in-memory only](feedback_in_flight_memory.md) — restart to clear
- [Log rotation](feedback_log_rotation_fix.md) — FileHandler not RotatingFileHandler; **age-based pruning DOES work** (`log_cleanup` cron, `-mtime +30`) [[batch2-done-17jul]]
- [Trade export filters](feedback_trade_export_filters.md) — candles exclude CANCELLED

## Boot-log observability — what IS and is NOT greppable (VERIFIED 25-Jul)
- 📄 **Boot log = `logs/system_<YYYY-MM-DD>.log`, NOT journald** (journald = ~6 lines/boot, WARNING+/stdout; MEASURED 24-Jul). INFO goes to the file. **Name it in any "grep the boot log" instruction.**
- 🔬🔝 **MECHANISM, FROM CODE 16-Sep:** handlers attach to **ROOT** (`core/logger.py:375,452`); `_SystemFilter` is a **pure level catch-all** (`levelno>=INFO`, ⛔ no name filter); **no `propagate=False`**; stdout is `setLevel(WARNING)` (`:420`). ⇒ ⭐ ANY new logger name reaches `system_*.log`; ⛔ **no INFO EVER reaches journald.** ⚠️ Nearly failed a correct deploy — 3 INFO rows hunted in journald read as "manager dead".
- ✅ **GREPPABLE:** `V3 Step 10b PB-01 watchlist: ENABLED` (`main.py:3207`, DISABLED `:3219`) — once per boot, verified 20-24 Jul · kill auto-clear (**journald**) · `eod_self_exit: past <HH:MM> IST` = the ONLY place the configured window appears (~17:35).
- ⛔ **NOT GREPPABLE:** (a) the service window **at boot** — guard `:1712` runs before config `:1743`, so it CANNOT print it; (b) **`shadow_tracker.enabled`** — never logged; proof = `count(*) from innings` staying **322**.
- ⭐ **RULE: an operator instruction that says "grep X" must be VERIFIED against a real log before it ships. A check that silently finds nothing is worse than no check — "no output" reads as "it failed."** (Two of three proposed 08:15 greps did not exist, 25-Jul.)

## Hygiene Queue (low priority)
- [PC test-env](pc_test_env_hygiene.md) — pre-existing PC failures (⚠️ **NOT "baseline 14"** — see the regression rule below); `ops_dashboard/tests` need `ops_dashboard/.venv` (357/357); pin tzdata

## Relocated from the hot index (08-Aug compaction) — stable fact, VERBATIM
*Moved to keep `MEMORY.md` under its read limit. ⛔ Nothing summarised, nothing dropped — each line is exactly as it stood in HOT.*
- 🌙⏰ **[SERVICE WINDOW = CONFIG; self-exit 17:35](service_window_configurable_25jul.md)** — a night `inactive(dead)`/exit-0 **when flat** is BY DESIGN, NOT S4. ⚠️ the boot guard cannot read config; START cutoff 18:15.
- 🗄️⚠️ **[MIGRATION-ON-OPEN rule](migration_on_open_rule_14jul.md)** — schema migrates on DB-OPEN not at boot. **GUARD `ed1c4b9`:** only main.py boot migrates; others refuse + CRITICAL sentinel.
- **[DB schema v28 analytics split](db_schema_v28_split.md)** — TWO DB files (ATTACHed); raw sqlite must use `core.db_connect.connect`. ⚠️ `fm_ledger.date`/`webhook_audit.date` are **VIRTUAL GENERATED**; `pragma_table_info` HIDES them — real, do NOT "fix".
- 🔒🎯 **[EXITS THREAD CLOSED 24-Jul — reopen ONLY post-M-S4](trailing_stop_never_fired_24jul.md)** — trail UNREACHABLE (423/423 LIMIT_TRIPLE); 8 policies MEASURED −0.076..−0.144R; lever=TGT.
- 📵✅🔝 **[TEST SIDE-EFFECTS — CLASS CLOSED 27-Jul](test_side_effect_class_27jul.md)** — suite posted **~50 REAL Telegram alerts**. ⭐ **Remaining hole: the guards are IN-PROCESS — a SUBPROCESS is NOT covered.** ⛔ `orders.status` NEVER `REJECTED`.
- [Webhook flow diagnosis](feedback_webhook_flow_diagnosis.md) — check `webhook_audit` (authoritative POST record). Entry window **[10:00, 15:00)**: 403s both sides are the designed gate, not an outage.
- 📊⏰ **[13 SCANNERS IS A FULL-DAY FIGURE, NOT A 10:20 ONE](scanner_13_is_a_full_day_figure_not_1020.md)** — 🔬 only **9** posted by 10:20 on 04-Sep; the 13th came **12:06**. ⛔ A 10:20 shortfall is NORMAL. Count at **12:30+**; at 10:20 read only the **401**.
- **Op notes:** [capital](capital_operational_note.md) · [order lifecycle](order_lifecycle_operational_note.md) · [CO](co_bracket_operational_note.md)

## Relocated from the hot index (27-Jul compaction) — stable fact, verbatim
- 📉🔀 **[Book is NOT long-only; net-short EXPECTED not oversell](book_not_long_only_eod_reverse_aware.md)** — intraday SHORT strategies live. Short-vs-oversell via broker `buy_qty/sell_qty`. EOD squareoff BUYs to COVER a short (`eod_squareoff.py:1155`); can't go −1→−2.
- 🗃️ **[ro-open of a WAL backup DB leaves `-shm`/`-wal` artifacts](sqlite_ro_wal_sidecar_gotcha.md)** — `?mode=ro` alone still creates a `-shm`; use `?mode=ro&immutable=1` or copy-first for zero-trace. LIVE DB unaffected (app owns them). Created 14 in backups 24-Jul.
- 🧊 **`__pycache__/main.cpython-312.pyc` NEVER MATCHES THE RUNNING `main.py` -- EXPECTED.** The service runs `main.py` as the entry script, and Python never caches bytecode for the entry script (`__main__`). A MATCH=False there is ⛔ not a finding (11-Sep 08:20 check; 08:35 file §5.1).
