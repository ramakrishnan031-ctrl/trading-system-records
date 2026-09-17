---
name: ct-guard-invariant-18jul
description: 18-Jul — the CT live-DB guard is now bypass-proof by an AST invariant (proven to bite); 5 real bypass routes were found and closed. The permanent engineering rule is recorded. security-watcher was REFUSED as a non-bug (it runs at its designed 60s cadence).
metadata: 
  node_type: memory
  type: project
  originSessionId: b9e84959-b70c-4ce6-9521-3db6f6dd3fee
---

**🛡️📌 CT-GUARD ANTI-DECAY INVARIANT (item 1 DONE) + SECURITY-WATCHER (item 2 ⛔ REFUSED) — 18-Jul-2026.**
Report `docs/audit/ct_guard_invariant_and_secwatcher_18jul2026.md`. **Test-infra only; item 2 changed
NOTHING.**

## ITEM 1 — the guard is now bypass-proof BY INVARIANT

**⭐ The "single route" claim was FALSE.** 5 modules bypassed `assert_not_live_db` entirely with raw
`sqlite3.connect()` on a hardcoded live path: `ct140_eod_failure`, `ct143_verify`, `ct145_rapid_crash`,
`vm_investigate`, `vm_investigate2`. **Honest severity: SELECT-only (0 write statements) ⇒ no writes were
happening — BUT a plain `sqlite3.connect(path)` is READ-WRITE**, so they held **unguarded writable handles
on production**, and one future `UPDATE` would have reached it silently (plus `-wal`/`-shm` creation).
**All 5 → `get_db_connection(readonly=True)`** (`mode=ro`; same data, no write capability, matches what
they already did). **0 raw connects remain outside `ct_utils.py`.**

**THE INVARIANT** — `tests/crash_test/test_ct_guard_invariant.py`, an **AST** scan of every harness module
(comments/strings can't fool it), enforcing 3 properties that are load-bearing TOGETHER:
* **A** no raw `sqlite3.connect()` outside `ct_utils.py` ⇒ every open goes through the one guard;
* **B** no live-DB path literal (`trading_system.db`/`analytics.db`) outside `ct_utils.py` ⇒ **you cannot
  open what you are not allowed to name**;
* **C** `StateStore(db_path=…)` never receives `LIVE_DB_PATH`/`LIVE_ANALYTICS_DB_PATH` (it opens WRITABLE
  and can migrate the schema on open).
⇒ a writable live handle would need `sqlite3.connect` (blocked by A), the live name (B), or the live
constant passed to a writable opener (C + the runtime guard). **Every route closed, checked automatically.**

**⭐ PROVEN TO BITE (a green check is evidence only if it could be red):** planting a bypass file
(`sqlite3.connect("data_store/trading_system.db")`) ⇒ **2 failed / 3 passed** (A and B both fired);
removing it ⇒ **5 passed**. Pinned as its own test (`test_invariant_detects_a_planted_bypass`) **plus a
coverage assertion** (`≥20 modules incl. cleanup.py`) so the scan can never pass by matching nothing.
**It earned its keep on day one** — it caught a real leftover I'd missed: a dead live-path literal still at
`ct145_rapid_crash.py:10` after its connect had been converted.
**Allow-list = 3 files, each justified in-line:** `ct_utils.py` (defines the guard + constants),
`test_ct_harness_safety.py` (asserts the guard REFUSES those paths), the invariant file itself.

**📌 THE PERMANENT ENGINEERING RULE — recorded in `docs/SYSTEM_MAP.md` (⚠️ ENGINEERING RULE section, next
to the migration-on-open rule) + the invariant's module docstring:**
> **A destructive / crash-test harness must NEVER hold a writable handle on a live database. ALL writable
> DB access goes through ONE guard that fails CLOSED — no override flag, no environment escape hatch.
> Resetting a live system is an OPERATOR tool in `scripts/` with a backup + confirmation gate, NEVER part
> of a test harness.**

## ITEM 2 — security-watcher: ⛔ REFUSED WITH EVIDENCE (it is NOT broken)

The premise ("stuck in activating/auto-restart — the same pattern alert-watcher had before its `--loop`
fix, a 104k-restart loop") **does not hold.** Four independent proofs:
1. **Rate = the configured cadence, not a loop: 10 restarts in 10 min · 59 in an hour · `RestartSec=60`.**
   Passes are 60s apart to the second (13:52:23→13:53:23→13:54:24). alert-watcher's REAL bug restarted
   *immediately* (104,567).
2. **The unit file DOCUMENTS the design:** *"Rising NRestarts is NORMAL (it's a heartbeat, not a
   crash-loop). NB: systemd REFUSES Restart=always with Type=oneshot — must be Type=simple."* The journal's
   first entry (19-Jun 23:19) shows that refusal actually happening ⇒ an **informed workaround**.
3. **The scan runs and alerts:** `pass complete (1 finding(s), 0 new alert(s))` every 60s,
   `ExecMainStatus=0`, `Deactivated successfully`; `data_store/security_state.json` was **16.7s** old.
4. **⭐ NOTHING reads its systemd `ActiveState`** — all 3 monitors use **state-file freshness**:
   `cron_officer.security_watcher_health` (stale >5min ⇒ DOWN), `system_manager:825-829`,
   `scripts/preflight/checks/security.py`. A grep for `is-active`/`ActiveState` on anything security =
   nothing. ⇒ **the `activating` sighting is just the transient between 60s passes.**
**NOT CHANGED** — altering a working LIVE security service the weekend before **Mon 20-Jul 08:15** (the
first real boot after the S4 fix) adds risk for **zero functional gain**, on a premise now disproven.
Applied the standing rule [[feedback-verify-the-finding-premise]]: *refusing an item with evidence is a
valid outcome.*

**⚠️ OPTIONAL FOR RAMA (NOT applied):** convert to a **systemd timer** — `security-watcher.timer`
(`OnUnitActiveSec=60`) + `Type=oneshot`/`Restart=no`. Canonical for scan-and-exit and **consistent with the
existing `cron-watchdog.timer`** on this VM. Wins: `NRestarts` stays 0, `ActiveState` becomes meaningful,
and it removes **5,720 journal lines/day** + the "is it crash-looping?" ambiguity that generated this task.
**Verify after:** `security_state.json` still refreshing (~60s) — a botched conversion would silently stop
security scanning.

## Board carried forward
* 🆕 **RAMA DECISION: `cleanup.py --live` capability was REMOVED (it refuses).** Does live-reset return as
  an OPERATOR tool in `scripts/` with backup + confirmation? [[ct-harness-safety-18jul]]
* 🔓⛔ **The 6 destructive CTs (CT114/127/130/132/133/135) are UNBLOCKED but NOT RUN** — a separate,
  deliberate sandbox/off-hours, Rama-aware step.
* **E4/W10** (Rama risk sign-off) · **Q10 Part B** (Rama's Kite token) · **regime strategic choice +
  FREEZE `min_pass_score` while measuring** · **D1–D4** · Rama's security actions · **Q9** (last sizeable
  own-run) · live-gated (F1 enforce, B3, alert-watcher soak).
* ⚠️ **MONDAY 20-Jul 08:15 = the first real boot after the S4 fix — WATCH IT.** The missing-direction alert
  also first arms then; the strategy-registry officer's first live run is **Mon 16:22**.

Related: [[ct-harness-safety-18jul]] · [[migration-on-open-rule-14jul]] ·
[[feedback-verify-the-finding-premise]] · [[liveness-alarm-17jul]].
