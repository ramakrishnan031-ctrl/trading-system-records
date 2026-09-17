# INPUT 3.5 RE-RUN — Fri 11-Sep-2026 · THE CORRECTED OLD-LOADER EXPERIMENT ON PRODUCTION (Block A, `d3ee69d`)

**This record covers input 3.5 ONLY.** It is a NEW record. The 08:20 record it corrects stays exactly as written — NOT ESTABLISHED, 3.5 NOT EXECUTED — because that is the historical truth of 08:20.

**Input 3.5:** PASS -- ConfigSchemaError, error_count=2, on exactly the two Block A keys (eod_squareoff.mis_pass_1_market_protection_percent and eod_squareoff.mis_pass_2_market_protection_percent, both extra_forbidden)

**Combined verdict, across the two records:** Host gate PASS and inputs 3.1-3.4, 3.6-3.12 PASS (the 08:20 record) + input 3.5 PASS (this record) => Block A's RUNTIME is ESTABLISHED on production -- and it is NOT live-proven: ESTABLISHED says the right code is running with the right values, and NOTHING about whether a protected MARKET order actually executes at the broker. That is 15:13's question, and only a real exit can answer it.

**Status of this record:** COMPLETE -- the check ran to DONE

🔗 **CITES THE 08:20 RECORD** — `docs/audit/BOOT_PROOF_BLOCK_A_d3ee69d_11-Sep-2026.md`, SHA-256 `f76f313c99e913a2a89130a106bc214401d39985e39c123c5b7f66756cbe9feb`, and its raw sidecar `docs/audit/BOOT_PROOF_BLOCK_A_d3ee69d_11-Sep-2026.raw.txt`, SHA-256 `82b2c694dcb1701e7d327c75d3e61264aa283e1d7c5f093d21d88e372670f305`, 11719 bytes — all three re-verified against these values when this record was written. A reader of the 08:20 record finds this one by the shared filename prefix in `docs/audit/` and by that record's own §4: *a later finding … is a NEW record … that names this file and its SHA-256s*. ⛔ The 08:20 record was not opened for writing.

🏷️ **NEVER-EDIT-AFTER-CREATION.** Read-only is a secondary guard. A correction to this record is another NEW record citing it and both of its SHA-256s.

---

## §0 — WHAT CHANGED, AND WHY

At 08:20, input 3.5 did NOT EXECUTE because of a defect **in the checker, not in production**: the check executed the pre-Block-A loader (`3b15bbf:core/config_loader.py`) inside a fresh module object that was never registered in `sys.modules`. pydantic completes forward references through `sys.modules[cls.__module__]`, so `SystemConfig` could not resolve `BrokerConfig`, and the loader stopped on `PydanticUserError` before it ever reached schema validation.

The correction is the narrowest possible — register the module before executing it — and **nothing else in the script changed** (08:35 file §2): 1 line(s) added, 0 removed.

````diff
--- prod_0820_check.py (08:20, v5)
+++ prod_0835_check_fix35.py (this run)
@@ -309,4 +309,5 @@
     mod = types.ModuleType("core.config_loader_old_%s" % OLD_SHA)
     mod.__file__ = os.path.join(ROOT, "core", "config_loader.py")
+    sys.modules[mod.__name__] = mod  # 08:35 file sec 2: register before exec so pydantic can complete SystemConfig
     try:
         exec(compile(old_src, "config_loader@%s" % OLD_SHA, "exec"), mod.__dict__)
````

| producer | SHA-256 |
|---|---|
| the 08:20 check (`prod_0820_check.py`, v5) | `82e39df6ded99ed53acd3508a7209b5bbf89f0518784d8fdaa34314ae59e49aa` |
| the corrected check (this run) | `642b45fa3d0189229c6f8e26aea473b2d2176ba211e58d8ee1783e1d0727ed7d` |

*Supporting evidence only — ⛔ never production evidence:* on the PC (Python 3.11.9, pydantic 2.13.0) against the same `d3ee69d` tree, the 08:20 method reproduced the `PydanticUserError` exactly, and the registered module produced `ConfigSchemaError`, error_count=2, on the two Block A keys. That result closed nothing; this production run is the evidence.

## §1 — THE CONDITION (08:35 file §1)

Today's production YAML, through the exact pre-Block-A loader from `3b15bbf`: **PASS** ⇔ `ConfigSchemaError` with **exactly two** errors, the two Block A keys; **NOT EXECUTED** ⇔ `PydanticUserError` again or any other inability to execute — including a refusal with a different count or different keys, which is not the experiment; **FAIL** ⇔ the old loader accepts today's YAML.

## §2 — INPUT 3.5, AS THE SCRIPT PRINTED IT (a verbatim excerpt of §5)

````text
  OLD loader source from 3b15bbf: 120790 bytes
  OLD loader: REFUSED -- ConfigSchemaError: Schema validation failed for system_config.yaml
      error_count=2
      loc=('eod_squareoff', 'mis_pass_1_market_protection_percent') type=extra_forbidden
      loc=('eod_squareoff', 'mis_pass_2_market_protection_percent') type=extra_forbidden

3.5   OLD loader genuinely REFUSES (ConfigSchemaError, error_count=2) PASS          REFUSED: ConfigSchemaError, error_count=2
````

## §3 — WHAT THIS RECORD DOES NOT DO

Because nothing else in the script was changed, it re-measured every input; those values are in the raw output below. ⛔ They are **not** restated here as freshly proven — the 08:20 record proves the host gate and inputs 3.1–3.4 and 3.6–3.12 (08:35 file §3.5). This record proves, or fails to prove, 3.5 alone.

## §4 — PROVENANCE

| fact | value |
|---|---|
| status | COMPLETE -- the check ran to DONE |
| target host — the script's first output | `trading-system` |
| run time — the script's own clock | `2026-09-11 08:42:09 IST` |
| run by | Rama's go via the 08:35 file (delivered 08:35:34 IST); host confirmed trading-system immediately before the run |
| raw output | `BOOT_PROOF_BLOCK_A_d3ee69d_11-Sep-2026__INPUT_3.5_RERUN.raw.txt` beside this file — written FIRST; 11709 bytes, SHA-256 `f41db86c72cd1aa2116fbf01d0005ef8359bf57b9c8d03978554b8112aaa3f04`; embedded verbatim in §5 |
| record written | 2026-09-11 08:42:10 IST (PC clock) |

## §5 — RAW OUTPUT, VERBATIM — THE PRIMARY EVIDENCE

````text
== TARGET HOST ==
  hostname  : trading-system
  production: True   (production's hostname is 'trading-system')
  time      : 2026-09-11 08:42:09 IST

== the process ==
MainPID=2298907
NRestarts=0
ExecMainStartTimestamp=Fri 2026-09-11 08:15:20 IST
ActiveState=active
SubState=running
ActiveEnterTimestamp=Fri 2026-09-11 08:15:20 IST
ps lstart: Fri Sep 11 08:15:19 2026  (epoch 1789094719)
  unit ExecStart={ path=/home/ubuntu/systems/venv/bin/python ; argv[]=/home/ubuntu/systems/venv/bin/python /home/ubuntu/systems/trading-system/main.py --mode live ; ignore_errors=no ; start_time=[Fri 2026-09-11 08:15:20 IST] ; stop_time=[n/a] ; pid=2298907 ; code=(nu
  unit EnvironmentFiles=/home/ubuntu/systems/trading-system/.env (ignore_errors=no)
  unit WorkingDirectory=/home/ubuntu/systems/trading-system
  unit Environment names: ['PATH', 'PYTHONUNBUFFERED']
  unit PYTHONPATH: not set in the unit

== boot-attempt evidence (triage) ==
Result=success
ExecMainExitTimestamp=
ExecMainCode=0
ExecMainStatus=0
StateChangeTimestamp=Fri 2026-09-11 08:15:20 IST
InactiveEnterTimestamp=Thu 2026-09-10 17:35:04 IST
  ExecMainStartTimestamp is today: True | ExecMainExitTimestamp is today: False
  today's system log (logs/system_2026-09-11.log): present
  journal readable: True | systemd start lines today: 1 | exit/fail/restart lines today: 0
  journal, the unit's last 40 lines today (masked):
    2026-09-11T08:15:20+05:30 trading-system systemd[1]: Started trading-system.service - Trading System v2 (paper/live mode).
    2026-09-11T08:15:21+05:30 trading-system trading-system[2298907]: 2026-09-11T08:15:21 CRITICAL kill_switch ? KILL SWITCH ACTIVE AT STARTUP: state=SOFT_KILL reason=circuit_breaker_force_close_15:15 triggered_by=order_monitor -- operator must call resume() to clear (Audit Issue #18 fix)
    2026-09-11T08:15:21+05:30 trading-system trading-system[2298907]: 2026-09-11T08:15:21 WARNING  kill_switch ? Kill switch auto-cleared: prior SOFT_KILL from 2026-09-10 (reason=circuit_breaker_force_close_15:15 by=order_monitor) -- new day 2026-09-11 starts clean (HEADLESS); audited to system_events
    2026-09-11T08:15:29+05:30 trading-system trading-system[2298907]: Tier multiplier: ON (tier weights: 1.0/0.7/0.5 x perf_weights)
    2026-09-11T08:15:32+05:30 trading-system trading-system[2298907]: 2026-09-11T08:15:32 WARNING  core.config_validator ? CONFIG_UNACCESSED: 396 config keys never read: ['broker_costs.zerodha.brokerage_flat_intraday', 'broker_costs.zerodha.brokerage_pct_intraday', 'broker_costs.zerodha.exchange_txn_pct
  token_watcher.log, last 12 lines (masked):
    [2026-09-04 13:47:46 IST] trading-system.service start command issued.
    [2026-09-07 08:15:21 IST] Fresh token detected (daily start, in service window). Starting trading-system.service.
    [2026-09-07 08:15:21 IST] trading-system.service start command issued.
    [2026-09-08 08:15:18 IST] Fresh token detected (daily start, in service window). Starting trading-system.service.
    [2026-09-08 08:15:18 IST] trading-system.service start command issued.
    [2026-09-08 15:16:47 IST] token_watcher started (poll=30s, backoff=300s, max_crash=3/hr)
    [2026-09-09 08:15:23 IST] Fresh token detected (daily start, in service window). Starting trading-system.service.
    [2026-09-09 08:15:23 IST] trading-system.service start command issued.
    [2026-09-10 08:15:21 IST] Fresh token detected (daily start, in service window). Starting trading-system.service.
    [2026-09-10 08:15:21 IST] trading-system.service start command issued.
    [2026-09-11 08:15:20 IST] Fresh token detected (daily start, in service window). Starting trading-system.service.
    [2026-09-11 08:15:20 IST] trading-system.service start command issued.
  today's config-load failures and tracebacks (system log, full lines, masked):
    (none)
    (none)

== token refresh evidence (07:20 file sec 4: behind any T3) ==
  token file: /home/ubuntu/systems/trading-system/data_store/session/zerodha_token.json -- mtime 2026-09-11 08:15:01 -- dated today: True
  auto_refresh_token's cron log: /home/ubuntu/systems/trading-system/logs/cron-auto-token.log -- mtime 2026-09-08 08:15:10; its last 25 lines (masked):
    telegram.send_deadline_exceeded
  'Token refresh FAILED' lines in its last 80 lines: 0
  cron journal today: auto_refresh_token CMD lines: 1
  heartbeat (cron_heartbeat.None): 3 recent token row(s)
    job=auto_refresh_token status=SUCCESS at=None msg=None
    job=auto_refresh_token status=SUCCESS at=None msg=None
    job=auto_refresh_token status=SUCCESS at=None msg=None
  its exit code: not recorded directly; by the script's own contract (0 <=> heartbeat SUCCESS, 1 <=> heartbeat FAILED) today's heartbeat says: NO heartbeat row dated today
  token reading: the token is dated today and no refresh failure is recorded

>>> EARLY TRIAGE: service active, today's process -- P4 / P5 / P6 are decided at the end

== provenance: the bare repo (context -- bare HEAD alone is NOT proof) ==
  bare HEAD : d3ee69d78e2f1e72cb552e80eef3890348fb16bd
  bare main : d3ee69d78e2f1e72cb552e80eef3890348fb16bd
  HEAD log  : d3ee69d 2026-09-10 15:37:13 +0530 docs(incident): IDEA 10-Sep -- the second market-protection rejection in two days
  cat-file -t d3ee69d: commit

== 3.3 the running source vs the APPROVED Block-A content (d3ee69d) ==
  broker/zerodha_adapter.py      disk==d3ee69d:True  (disk==HEAD:True)  mtime 2026-09-10 16:19:37  process-newer-than-file=True
  core/config_loader.py          disk==d3ee69d:True  (disk==HEAD:True)  mtime 2026-09-10 16:19:37  process-newer-than-file=True
  main.py                        disk==d3ee69d:True  (disk==HEAD:True)  mtime 2026-09-10 16:19:37  process-newer-than-file=True
  orders/mis_autosquareoff.py    disk==d3ee69d:True  (disk==HEAD:True)  mtime 2026-09-10 16:19:37  process-newer-than-file=True
  config/system_config.yaml      disk==d3ee69d:True  (disk==HEAD:True)  mtime 2026-09-10 16:19:37  process-newer-than-file=True

== 3.4 / 3.5 THE EXPERIMENT: today's YAML through the NEW and the OLD loader ==
  NEW loader: OK  pass_1=1.5 pass_2=2.5
  OLD loader source from 3b15bbf: 120790 bytes
  OLD loader: REFUSED -- ConfigSchemaError: Schema validation failed for system_config.yaml
      error_count=2
      loc=('eod_squareoff', 'mis_pass_1_market_protection_percent') type=extra_forbidden
      loc=('eod_squareoff', 'mis_pass_2_market_protection_percent') type=extra_forbidden

== 3.6 wiring: do the YAML values reach the squareoff? (the deployed source) ==
  main.py                      mis_pass_1_market_protection_percent   at lines: 3339
  main.py                      mis_pass_2_market_protection_percent   at lines: 3341
  orders/mis_autosquareoff.py  market_protection=protection           at lines: 877

== .pyc headers (corroboration only: ANY import rewrites them) ==
  broker/__pycache__/zerodha_adapter.cpython-312.pyc src-mtime/size MATCH=True
  core/__pycache__/config_loader.cpython-312.pyc   src-mtime/size MATCH=True
  __pycache__/main.cpython-312.pyc                 src-mtime/size MATCH=False
  orders/__pycache__/mis_autosquareoff.cpython-312.pyc src-mtime/size MATCH=True

== boot log (today) ==
  logs/system_2026-09-11.log (present)
  Config loaded            1
  run_all_startup_checks   1
  Config load failed       0
  STARTUP                  1
  Traceback                0
  first Config loaded : {"ts":"2026-09-11T08:15:21.036+05:30","level":"INFO","logger":"main","msg":"Config loaded from config (8 files)"}
  first STARTUP       : {"ts":"2026-09-11T08:15:21.050+05:30","level":"CRITICAL","logger":"kill_switch","msg":"KILL SWITCH ACTIVE AT STARTUP: state=SOFT_KILL reason=circuit_breaker_for
  CRITICAL lines today: 1

== 3.7 kiteconnect: what THIS interpreter imports (same venv + cwd as the unit) ==
  interpreter: /home/ubuntu/systems/venv/bin/python
  __file__   : /home/ubuntu/systems/venv/lib/python3.12/site-packages/kiteconnect/__init__.py
  __version__: (the attribute is the MODULE /home/ubuntu/systems/venv/lib/python3.12/site-packages/kiteconnect/__version__.py)
  __version__.__version__: 5.1.0
  metadata   : 5.1.0
  dist-info  : kiteconnect-5.1.0.dist-info

== 3.8 / 3.10 local state (DB, read-only) ==
  -wal present: True -> opened mode=ro
  KILL SWITCH: state=INACTIVE triggered_at=2026-09-11T08:15:21.050806+05:30 triggered_by=main.auto_clear_stale
               reason=auto_clear_stale: was SOFT_KILL from 2026-09-10 (reason=circuit_breaker_force_close_15:15, by=order_monitor)
  system_events STARTUP rows today: 1  (a PROVEN BOOT = one written AFTER the process start)
    ev 3842  2026-09-11T08:15:32.649115+05:30  COLD  after-process-start=True
  live trades (PENDING_FILL/OPEN/PARTIAL/EXITING): 0
  local orders placed today: 0

== the kill switch as an INDEPENDENT WITNESS to the boot (07:20 file sec 3) ==
  kill switch : cleared TODAY at 2026-09-11T08:15:21.050806+05:30 by main.auto_clear_stale -- corroborates a boot today
  process     : the process / log / journal evidence says a boot today
  WITNESS CHECK: AGREE

== 3.9 / 3.11 broker truth (READ-ONLY: profile, positions, holdings, orders, GTTs) ==
  token file mtime: 2026-09-11 08:15:01
  profile read OK (account id deliberately not printed)
  positions net: 0 row(s), 0 with non-zero quantity
  positions day: 0 row(s), 0 with non-zero quantity
  holdings with quantity: 0
  broker orders today: 0   (pre-open: ANY order here is unexpected)
  GTTs by status: none

== TRIAGE (explicit precedence P0-P6) -- THE FIRST LINE OF THE REPORT ==
  TRIAGE: P6 / T1 -- ESTABLISHED: host gate PASS and all twelve inputs PASS. A normal day.
  SERVICE: active, process started Fri Sep 11 08:15:19 2026 | KILL SWITCH: INACTIVE at 2026-09-11T08:15:21.050806+05:30 by main.auto_clear_stale
  WITNESS: AGREE

== VERDICT: the HOST GATE, then the twelve INPUTS (3.1-3.12) -- each separately ==
  HOST GATE : PASS  hostname=trading-system
  3.1   service active                                             PASS          ActiveState=active SubState=running NRestarts=0
  3.2   process started TODAY (2026-09-11)                         PASS          MainPID=2298907 lstart=Fri Sep 11 08:15:19 2026
  3.3   running source = approved Block-A content (d3ee69d)        PASS          disk==d3ee69d 5/5; process newer than every file: True
  3.4   today's YAML loads with PASS_1=1.5 and PASS_2=2.5          PASS          pass_1=1.5 pass_2=2.5
  3.5   OLD loader genuinely REFUSES (ConfigSchemaError, error_count=2) PASS          REFUSED: ConfigSchemaError, error_count=2
  3.6   market_protection wiring at the call site                  PASS          main.py pass_1@3339 pass_2@3341; mis_autosquareoff.py market_protection=protection@877
  3.7   kiteconnect 5.1.0 (from __file__ + __version__.__version__) PASS          version=5.1.0 file=/home/ubuntu/systems/venv/lib/python3.12/site-packages/kiteconnect/__init__.py (metadata 5.1.0)
  3.8   local live trades (read)                                   PASS          0 live: none
  3.9   broker positions + holdings (read-only)                    PASS          net non-zero 0, day non-zero 0, holdings with quantity 0
  3.10  kill-switch state (read)                                   PASS          state=INACTIVE at=2026-09-11T08:15:21.050806+05:30 by=main.auto_clear_stale
  3.11  no unexpected orders                                       PASS          pre-open at 08:42: broker orders 0, local orders placed today 0
  3.12  d3ee69d exists in this host's bare repo                    PASS          cat-file -t -> commit
  => ESTABLISHED: host gate PASS and all twelve inputs PASS -- runtime, config and provenance. NOT proof the exit path works: that is 15:13's separate question, and a flat PASS_2 will never answer it.

DONE
````

## §6 — HOW THIS RECORD CHANGES

It does not. ⛔ No edit, no appended re-run, no reinterpretation in place, no chmod-and-edit. A later finding is a NEW record that names this file and both of its SHA-256s.
