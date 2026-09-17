---
name: census-not-in-journalctl-05aug
description: The EOD census (and every INFO log) never reaches journald — stdout is WARNING+. The real source is logs/system_<date>.log. Measured 05-Aug-2026.
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4eb48114-5788-48ac-94d6-e91b992a6fe4
  modified: 2026-08-05T06:16:47.745Z
---

⛔⛔ **`journalctl -u trading-system.service` DOES NOT CONTAIN THE 17:35 CENSUS — OR ANY `INFO` LOG.**
Measured 05-Aug-2026 at HEAD.

**THE MECHANISM:** `core/logger.py:419-420` —
`h_stdout = logging.StreamHandler(sys.stdout); h_stdout.setLevel(logging.WARNING)`.
For a systemd unit, **journald captures stdout** ⇒ **journald only ever sees `WARNING` and above.**
The census is emitted at **`INFO`** — `logger.info(ln)` at `core/effect_telemetry.py:302`, using
`get_logger("effect_census")` passed in at `main.py:1319-1320`.
⇒ **`journalctl … | grep effect_census` returns NOTHING, and always has.**

✅ **THE REAL SOURCE — `logs/system_<YYYY-MM-DD>.log`.** Root gets a `QueueHandler` (FIX-099, async)
feeding four file handlers (`logger.py:441-448`); `h_system` is the **INFO+ catch-all**
(`:400-402`, `_SystemFilter` `:240-243`) in **JSON, one object per line** (`_JsonFormatter`).
Also written: `trades_<date>.log` (records carrying a trade/signal/order id), `reconciler_<date>.log`,
`debug_<date>.log` (DEBUG+, plain text). One file per day, appended across restarts, **no mid-day
rotation** (`:392-395`).
⏳ **Retention 30 days** — `find logs -name '*.log' -mtime +30 -delete`
(`config/cron_registry.yaml:9`, `:19`) ⇒ ⛔ **an empty grep means "not in the last 30 days", NEVER
"never" — state the bound beside the zero.**

⭐ **THE LESSON:** the census grep anchor was also wrong (`CENSUS BEGIN` vs the emitted
`effect_census | BEGIN …`, `effect_telemetry.py:242`). **Fixing the ANCHOR was correct and
INSUFFICIENT — the SOURCE was wrong too**, and both failures are silent and identical from the
console: an empty result. ⇒ **on a non-reproducible artifact, verify WHERE it lands before you tune
WHAT you search for.** [[feedback-absence-needs-wide-check]]

⛔⛔ **AND THE PART THAT MATTERS MORE THAN THE MEASUREMENT: THIS WAS ALREADY IN `SYSTEM_MAP.md`, AND
HAD BEEN SINCE 25-JUL.** Its BATCH-4 banner states *"the app boot log is `logs/system_<YYYY-MM-DD>.log`,
**NOT journald** (journald holds only ~6 lines/boot — WARNING+ and stdout; MEASURED on Fri 24-Jul)"* —
**and carries the exact rule I then broke twice:** *"an operator instruction that says 'grep X' must
be VERIFIED against a real log before it ships — a check that silently finds nothing is WORSE than no
check, because 'no output' reads as 'it failed'."*
⇒ ⭐ **I re-derived from source what the map already said. The failure was not measurement — it was
not READING `SYSTEM_MAP.md` first, which is the standing NON-NEGOTIABLE rule.**
[[feedback-system-map-first]] ⛔ **No SYSTEM_MAP entry was added (G3): the fact is already there and a
second copy is the duplication the rule forbids.** This entry exists to make it findable from the
memory index and to record the process failure beside the fact.

Related: [[schema-product-is-on-orders-05aug]], [[silent-failure-gaps-25jul]].
