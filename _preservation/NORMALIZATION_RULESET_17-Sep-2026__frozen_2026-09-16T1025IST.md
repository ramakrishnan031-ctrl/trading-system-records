# NORMALIZATION RULESET — FROZEN — for the 17-Sep-2026 boot comparison

**Written 2026-09-16 10:25 IST, BEFORE the first VM write.** Per **AMENDMENT 13 §3**.
Companion to the expected-diff **v2** and to the two baseline captures. ⛔ **Verified at Gate 7/8 BEFORE the comparison runs.**

> ⛔🔴🔝 **WHY THIS IS A FILE AND NOT A NOTE.** *"Do not add exclusions after tomorrow's log"* is a rule with **no enforcement** if the ruleset is something someone can edit. ⭐ **Frozen with filename + size + md5, widening it tomorrow is ⛔ not a temptation resisted — it is a MISMATCH THAT SHOWS.**
>
> ⭐ **Normalize ONLY what is mechanically established from the log format or the code.** ⛔ **A field is not dynamic because it differed; it is dynamic because THE CODE MAKES IT SO.**

## R1 — `logs/system_YYYY-MM-DD.log` (JSON lines)
🔬 `_JsonFormatter` emits fixed fields **`ts` · `level` · `logger` · `msg`**, then extras.
- **R1.1** Parse each line as JSON. The comparison key is the tuple **(`level`, `logger`, normalized `msg`)**.
- **R1.2** **DROP `ts`** — 🔬 per-record wall-clock, `datetime.fromtimestamp(record.created)`.
- **R1.3** ⛔ **No other field is dropped.** Extras are compared as-is.
- **R1.4** ⛔ **`level` and `logger` are NEVER normalized** — they are part of what is under test.

## R2 — the journal (`journalctl -u trading-system`)
- **R2.1** Strip the syslog prefix: `^<Mon> <D> <HH:MM:SS> <host> trading-system\[<pid>\]: ` — 🔬 host and **PID** are process/boot-dependent.
- **R2.2** Strip systemd's own lifecycle timestamps in `Started`/`Stopped`/`Main process exited` lines; ⛔ **keep their status/code fields** — those are evidence.
- **R2.3** ⛔ **Nothing else.** ⚠️ Recall the journal only ever holds **WARNING+** ⇒ ⛔ absence of an INFO row here is **NOT** a finding.

## R3 — message-body normalization (the ONLY three, each justified by code)
| # | Pattern | Why it is dynamic (🔬 from code) |
|---|---|---|
| **R3.1** | in E1.1, the **`db=` path prefix** → `<PATH>`; ⛔ the filename `sr_shadow.db` is **kept** | `runner.py:152` logs `self._store.path`, resolved at runtime |
| **R3.2** | in E3.5, `counters={…}` and `history={…}` → `<JSON>` | `runner.py:158` logs `json.dumps(self.counters)` / `self._history.stats` — ⭐ **session-dependent by construction** |
| **R3.3** | in E5.12, the `<symbol>` | `signal_processor.py` interpolates the symbol |

⛔🔴 **R3 IS CLOSED. Exactly three entries.** ⭐ **The composition COUNTS in E2.3 are ⛔ NEVER normalized — they are the measurement.** ⛔ Adding an R3.4 tomorrow is the escape hatch this file exists to close.

## R4 — comparison procedure
1. Verify filename + size + md5 of: both baselines · expected-diff **v2** · **this file**. ⛔ Mismatch ⇒ **STOP**.
2. Normalize both sides with **R1–R3 only**.
3. **Multiset compare** — ⭐ multiplicity is part of the test (E-1 rows: exactly 1; **0 ⇒ finding**, **2 ⇒ anomaly**).
4. ⛔ **Order is asserted ONLY where the SOURCE proves it** (E1.1 before E1.2). ⛔ **Incidental baseline order is NEVER promoted to a contract.**
5. **Boot window and EOD window are compared SEPARATELY.**
6. **CRITICAL:** compare the baseline **set** against the post-deploy **set**; ⛔ a CRITICAL already in the baseline is **not new**.
