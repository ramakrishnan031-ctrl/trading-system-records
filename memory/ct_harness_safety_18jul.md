---
name: ct-harness-safety-18jul
description: DONE+DEPLOYED 18-Jul — the crash-test harness can no longer open a live DB writable; a hard guard (assert_not_live_db) refuses every route incl. symlink/hardlink/env-override. The 6 destructive CTs are UNBLOCKED but deliberately NOT RUN. cleanup.py --live now refuses.
metadata: 
  node_type: memory
  type: project
  originSessionId: b9e84959-b70c-4ce6-9521-3db6f6dd3fee
---

**🛡️✅🚀 CT HARNESS SCRATCH-SAFE BY CONSTRUCTION — DONE + DEPLOYED 18-Jul-2026** (off-market, system
DOWN). **PC == VM bare == tag `deploy-18jul-ct-harness-safety` → `6b7a74f`.** Report
`docs/audit/ct_harness_safety_18jul2026.md`. **TEST-INFRA ONLY — zero production files changed; no
runtime behaviour change (nothing here is imported by the trading process).**

**⭐ PREMISE HALF-CORRECTED (the rule keeps earning its keep).** The note said *"importing the harness
acquires a writable handle on production data"*. **The import claim is FALSE** — import only computes a
`Path`; no `sqlite3.connect` runs at module level. **What WAS true:** `DB_PATH = BASE_DIR/data_store/
trading_system.db` (base `ct_utils.py:63`) + `get_db_connection(readonly: bool = False)` (`:75`) →
`sqlite3.connect(str(DB_PATH))` (`:82`) ⇒ **the DEFAULT was a writable LIVE handle.** **Proven
empirically on a base worktree** (dummy DB at the hardcoded path): a no-arg `get_db_connection()`
executed `CREATE TABLE`. ⇒ the hazard was **a default-writable function + an ambiguous name**, NOT
import-time acquisition — a distinction that shaped the fix (guarding imports would have missed it).

**🔴 Q3 — IT HAS FIRED (evidence, not speculation).** VM `reports/crash_test/cleanup_log.jsonl`:
05-Jun `soft_cleanup` *"Released 37 orphan reservations"* / *"Kill switch cleared (1 rows updated)"*;
07-Jun `hard_cleanup` *"Cancelled 0 open trades / 0 pending orders / Reset capital..."* — **real
mutations of the live DB.** Non-alarmist reading: inside the deliberate Days 1–6 crash-test window
(the closed book only starts 15-Jun), so probably intentional then. **The point: NOTHING PREVENTED IT.**

**🆕 TWO HAZARDS THE NOTE DIDN'T MENTION:** (1) 4 scripts passed the live path straight into
`StateStore(db_path=DB_PATH)` (`test_double_release/fund_manager_edges/kill_switch_edges/
position_sizer_edges`) ⇒ writable + **migration-on-open** risk [[migration-on-open-rule-14jul]];
(2) `cleanup.py::do_hard()` runs `UPDATE trades SET status='CANCELLED'`, cancels orders, resets capital.
**Reassuring finding: the FULL SUITE was never at risk** — pytest collects only 6 tests here, all from
`test_ramcoind_oversell_prevented.py`, which already used `tmp_path` and never imported `ct_utils`.
**The exposure was DIRECT INVOCATION of the harness tools.**

**THE FIX — the ambiguous name WAS the bug ⇒ `DB_PATH` DELETED, not repointed** (a silently repointed
constant would be a new trap; an ImportError is loud and safe). Callers must now say which DB they mean:
* **`LIVE_DB_PATH` / `LIVE_ANALYTICS_DB_PATH`** — read-only diagnostics + the guard's comparison target
  (`state_inspector` / `invariant_checker` keep EXACT prior semantics).
* **`SCRATCH_DB_PATH` / `make_scratch_db()`** — all writable/destructive work; real `core/schema.sql`
  (constraints included) ⇒ **CT destructive capability preserved**.
* **`assert_not_live_db()` — THE HARD GUARD** → raises `LiveDatabaseRefused`. **No override flag, no env
  escape hatch. FAILS CLOSED.**
* `get_db_connection(readonly=True)` still reads live (`mode=ro`, safe by construction);
  `readonly=False` → guarded, defaults to scratch.
**Guard mechanism:** `normcase(realpath(abspath(expanduser(p))))` (absorbs relative/`..`/`~`/symlink/
Windows-case) **+ `os.path.samefile()`** — the ONLY thing that catches a **hardlink** (realpath can't
resolve one) — **+ refuses the `-wal`/`-shm` sidecars** (writing those corrupts live just as surely).
**Reused the harness's OWN idiom** (`ct_day3_isolated.py:50-54` StateStore+schema_path), not a new mechanism.

**⚠️ DELIBERATE CAPABILITY REMOVAL (Rama's call, flagged not silent): `cleanup.py --live` now REFUSES.**
Its purpose was resetting the LIVE system; silently resetting scratch while reporting success is worse
than stopping. **Live reset is an OPERATOR action → belongs in `scripts/` with a backup+confirm gate.**

**PROOFS.** RED-on-old on a base-HEAD **worktree** (never stash): `ImportError: cannot import name
'LIVE_ANALYTICS_DB_PATH'`; all 4 new symbols = 0 occurrences in the base blob. **Guard proven route by
route (16 tests):** absolute · analytics DB · relative · `..` · `-wal`/`-shm` · **CT_SCRATCH_DIR env
override** · **symlink** · **hardlink** · default-writable opener — all refused; scratch allowed.
**⭐ LIVE-DB UNTOUCHED ON THE REAL VM against the REAL production DB: `16 passed, 0 skipped` (so the
symlink AND hardlink routes actually executed there) and both live DBs IDENTICAL by size+sha256.**
PC equivalent around the whole `tests/crash_test` suite: 20 passed, DB/analytics/`-wal` identical.
*Honest nuance:* `trading_system.db-shm` **mtime** moves because any `mode=ro` reader must map SQLite's
WAL shared-memory index — **content unchanged, no data written.**
**Regression 11F/4933P, ZERO attributable** (new-failure set vs the base baseline EMPTY; 4918+15 new
guard tests = 4933; no crash_test failures). Backup `pre_deploy_ct_harness_20260718.db` **verified
sound** (`quick_check=ok`, v44, 361 trades). Schema v44 unchanged, integrity ok, 0 FK.

**🔓⛔ THE 6 DESTRUCTIVE CTs (CT114 · CT127 · CT130 · CT132 · CT133 · CT135) ARE NOW *UNBLOCKED* BUT
DELIBERATELY *NOT RUN*** — running them is a SEPARATE, deliberate, Rama-aware step (sandbox / off-hours).
Scratch satisfies them: CT114 disk-fill + CT127 clock-skew aren't DB-bound; CT135 tests `cleanup.py
--hard`'s `--force` gate (still testable); the rest need state manipulation, which scratch supports with
the real schema.

**Open follow-ups:** (1) run the 6 CTs — separate step; (2) `cleanup.py`'s live-reset capability →
Rama decides whether it returns as a `scripts/` operator tool; (3) `ct_day3_isolated.py` writes scratch
DBs into `data_store/` rather than `data_store/ct_scratch/` — untidy, not a hazard, left alone.

Related: [[migration-on-open-rule-14jul]] · [[feedback-verify-the-finding-premise]] ·
[[feedback-verify-rc-not-output]].

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 915 B (budget 300 B). The index now carries a hook and this link.

- 🛡️✅🚀📌 **[CT HARNESS SCRATCH-SAFE + GUARD PINNED BY INVARIANT — DEPLOYED 18-Jul](ct_harness_safety_18jul.md)** — the destructive harness can no longer open a live DB **writable** (`assert_not_live_db` fails closed, no override; catches relative/`..`/symlink/**hardlink**/`-wal`/env). **It HAD fired** (live writes 05/07-Jun). **Then pinned BY INVARIANT** — **5 more bypass routes found+closed** (raw `sqlite3.connect` on a live path) + an **AST** scan (no raw connect · no live literal · no live path to `StateStore`), **PROVEN TO BITE** (planted bypass ⇒ 2 failed; removed ⇒ 5 passed). **📌 PERMANENT RULE in SYSTEM_MAP.** Tags →`6b7a74f`, →`ae70567`; VM 21 passed, live DBs identical. **🔓⛔ 6 destructive CTs UNBLOCKED, NOT RUN.** **⚠️ RAMA: `cleanup.py --live` REMOVED — return it as a `scripts/` operator tool?** [[ct-harness-safety-18jul]] [[ct-guard-invariant-18jul]]
