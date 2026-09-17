---
name: missing-direction-alert-18jul
description: "DONE+DEPLOYED 18-Jul — a strategy YAML missing/with an invalid `direction` (or ANY validation failure) fires ONE loud Telegram+email alert naming the file at boot; the boot still fails (path A). Tag deploy-18jul-missing-direction-alert -> 34fd6a5."
metadata: 
  node_type: memory
  type: project
  originSessionId: b9e84959-b70c-4ce6-9521-3db6f6dd3fee
---

**🚨✅🚀 MISSING/INVALID `direction` NOW ALERTS LOUDLY AT BOOT — DONE + DEPLOYED 18-Jul-2026 ~11:2x IST**
(off-market, system DOWN, book flat ⇒ no flatten). **PC == origin == VM bare == `2956ed1`**;
**code tag `deploy-18jul-missing-direction-alert` → `34fd6a5`** (delta tag..HEAD = **0 non-markdown**).
Report `docs/audit/missing_direction_alert_done_18jul2026.md`.

**Rama's concern (solved):** if he adds a strategy and FORGETS `direction: LONG|SHORT` (or mistypes
it), the strategy must not quietly fail to trade — he must be told LOUDLY. Covers the current 16
YAMLs and all future ones.

**⭐ §2 FINDING — path (A) FAIL-BOOT, NOT silent-skip (this decided the fix):**
`load_all_strategies` (`strategies/loader.py:67-69`) calls `validate_strategy` with **no
try/except** ⇒ the FIRST bad YAML's `ConfigSchemaError` propagates ("no partial loads"). But the
boot's REAL gate is the **preflight**, not the live load at `main.py:2530`:
`run_all_startup_checks` (`main.py:1887`) → `check_strategy_configs` (`utils/startup_checks.py:1266`)
**catches** it → `blocking_failures += "invalid_strategy_configs"` (`:1616-1618`) → `main.py`
`_log.critical` + **`return 3`** — **BEFORE the `notifier` is constructed (`main.py:2048`)**.
⇒ Today: clean `exit 3`, **NO Telegram, NO email**, one log line naming only the FIRST bad file.

**FIX (path A: alert, then KEEP failing the boot — a broken strategy set must not run):**
* NEW `strategies/loader.py::scan_strategy_errors(dir) -> [(filename, reason)]` — pure Layer-2,
  collects **ALL** bad files in one pass, **never raises**; reasons from pydantic `.errors()` via
  `ConfigSchemaError.__cause__`: `missing required field 'direction'` · `direction: direction must
  be LONG or SHORT, got 'FOO'` · `unknown field 'x' not permitted`.
* NEW `main.py::_alert_invalid_strategy_configs()` — **ONE consolidated CRITICAL** naming every
  file+reason. **REUSES the strategy-registry/cron-officer path** (`TelegramNotifier.from_env` +
  `write_critical_sentinel`) — **no parallel notifier**. Telegram uses **`write_sentinel=False`** so
  the helper owns the SINGLE email sentinel ⇒ **one Telegram + one email, no duplicate**, and the
  **email still fires if the Telegram token is unset**. **FAIL-SAFE** (every send wrapped — can
  never crash or mask the abort). **Mode-agnostic (paper == live)**.
* Wired guarded into the `if not report.ok` abort branch **before** `store.close()`+`return 3` —
  **the abort itself is byte-identical**. Covers **ANY** validation failure, not just `direction`.

**No schema change** (v44 == deployed `EXPECTED_SCHEMA_VERSION` ⇒ no migration); integrity ok, 0 FK.
Backup `pre_deploy_missing_direction_alert_20260718.db` — **verified sound** (`quick_check=ok`, v44,
361 trades), not merely present.

**⭐ PROVEN ON THE VM WITH THE DEPLOYED CODE (real config never modified):** the real **16 YAMLs scan
`[]` ⇒ SILENT (no false alarm)**; a temp COPY with `direction` deleted / set `BUYSELL` yields exactly
`first_pullback_long.yaml -> missing required field 'direction'` and
`first_pullback_short.yaml -> direction: direction must be LONG or SHORT, got 'BUYSELL'`; re-scan of
the real config → still `[]`.

**RED-on-old** proven on a base-HEAD **`git worktree`** (never `git stash`; rc-checked): the 6 scan
tests fail `cannot import name 'scan_strategy_errors'`, the 5 alert tests ERROR on
`ImportError: cannot import name '_alert_invalid_strategy_configs'`.
**Regression: 11F/4918P vs base 41F/4877P ⇒ ZERO attributable** (`comm -13 base mine` EMPTY; the 30
base-only failures are the flaky heavy `test_main.py`/preflight set moving fail→pass).

**⏰ When it bites:** at the next boot's strategy load — **Mon 20-Jul 08:15** (the same boot that is
the first real proof of the S4 fix [[s4-boot-outage-17jul]]). With today's all-valid config it stays
**SILENT**; it only speaks when a YAML is actually broken. **Rollback = revert `34fd6a5`** (schema-free,
additive, no config/cron dependency).

Related: [[strategy-direction-registry-17jul]] (the registry mirrors `StrategyConfig.direction`; this
protects the field itself) · [[regime-phase0-17jul]] · [[feedback-verify-the-finding-premise]].

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 610 B (budget 300 B). The index now carries a hook and this link.

- 🚨✅🚀 **[MISSING/INVALID `direction` ALERTS AT BOOT — DEPLOYED 18-Jul](missing_direction_alert_18jul.md)** — a strategy YAML missing/with an invalid `direction` (or ANY validation failure) fires **ONE Telegram+email CRITICAL naming the file**; **the boot STILL fails** (path A: the preflight catches the loader raise and aborts before the notifier exists ⇒ there was NO alert at all). Reuses the registry/cron-officer notifier; fail-safe; no schema change. Tag →`34fd6a5`. PROVEN on the VM (real 16 YAMLs silent; broken copy named). **Bites Mon 20-Jul 08:15.** [[missing-direction-alert-18jul]]
