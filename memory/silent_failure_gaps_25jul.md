---
name: silent-failure-gaps-25jul
description: "25-Jul: fm_ledger ORDER BY fixed (76bca56); gui restarted. C1 daily-report-heartbeat premise REFUTED (19 heartbeats exist). C2 fwd-shadow empty-day + C3 PB-01 capture heartbeats now BUILT + DEPLOYED 5512104. M-O9 HELD — the trailed SL is not persisted."
metadata: 
  node_type: memory
  type: project
  originSessionId: 94025df9-7b5d-4673-aa44-14ccbe9d87b3
  modified: 2026-07-25T08:55:23.808Z
---

**25-Jul batch — DEPLOYED `76bca56`+`69ba15a` (off-market, service down, NO trading restart; loads Mon 08:15).**

## §A `76bca56` — `get_fm_ledger_for_date` now `ORDER BY ts ASC, ledger_id ASC`
Had **no ORDER BY**; its ONE production caller (`daily_report.py:187`) takes `init_rows[0]` as the day's opening capital. Worked only because SQLite scans in rowid order ⇒ **query-plan accident, not a contract**. On a restart day (INIT = one row per PROCESS START) it would pick an arbitrary opening capital **in the 16:05 report**.
**Fixed at the ACCESSOR** (1 caller, none wants unspecified order ⇒ the next caller inherits determinism). `ledger_id` = tiebreaker ⇒ order is TOTAL.
⭐ **The RED-first trap:** a naive test **PASSES on the broken code** because rowid order is usually chronological. All 3 tests insert the **later-timestamped row FIRST** so rowid and ts disagree; the key one shows the report would have taken **9,858.73 instead of 9,857.30**.
⚠️ **The test lives at the accessor, NOT in `test_daily_report.py`** — that suite drives the report through a `MagicMock` whose `return_value` the test itself orders, so a report-level assertion would pass regardless. **A mock you control cannot test ordering.**
⇒ all four "day's opening capital" derivations now agree and are restart-safe.

## §B — `gui-dashboard.service` RESTARTED (pid 1749999 → 1994926, 11:40:18)
It had held the OLD `db_reader` since 22-Jul. Restarted **after** the file landed (11:27:31) ⇒ loaded the fixed code (verified: `ORDER BY ts ASC LIMIT 1` present, **0** `FROM capital_snapshot`). `/`→302, `/api/capital`→401. ⛔ Trading service untouched throughout.

## §C — three silent-failure gaps SCOPED, none built (`docs/audit/silent_failure_gaps_2026-07-25.md`)
- 🟢 **C1 PREMISE REFUTED — the daily-report heartbeat EXISTS.** `daily_report.py:1903` SUCCESS + `:1919` **FAILED with the exception**; production holds **19** `daily_report` heartbeats (latest 24-Jul 16:05) and 18 for `daily_trade_review`. The in-situ comment names the 23-Jun gap it closed. **The old "daily-report cron = NO heartbeat" note was FALSE and is retired.** Residual: the db-not-found branch `:1882` returns 1 with no heartbeat (2-line fix, low value).
- ✅ **C2 FIXED + DEPLOYED 25-Jul `804ab16`** (was: 3 of 4 exits instrumented; `if not rows: return 0` wrote **nothing** ⇒ "no signals" == "recorder dead", on the **OOS dataset, forward-only, unbackfillable**). The empty path now records `SUCCESS` + **`EMPTY_NO_DATA`**; execution status deliberately **NOT** downgraded. ⭐⭐ **⇒ A MISSING `forward_shadow_record` HEARTBEAT ON A TRADING DAY NOW MEANS DEAD, not "a quiet day".** ⛔ The recorder was **never run** to test it — tests stub `StateStore`/`OUT_PATH`/`record_heartbeat` and assert the real JSONL's mtime is unchanged **and** that the only writable path was inside tmp (the mtime half alone is vacuous on a PC — the file does not exist there).
- ✅ **C3 FIXED + DEPLOYED 25-Jul `cf8d723`, live Mon 17:00.** One `cron_heartbeat("pb01_capture")` per EOD alert: `SUCCESS` / `SUCCESS`+`EMPTY_NO_DATA` at zero / **`FAILED`+`DISABLED`** on the `_eod_capture is None` boot-wiring branch (which answered 200 and looked exactly like "no breakouts"). ⚠️⚠️ **IT RECORDS `queued=`, NOT `captured=`** — `submit()` is async (WR1) ⇒ the row proves the alert ARRIVED/authenticated/was ACCEPTED, **never** that a `pb01_watchlist` row exists; **the watchlist row COUNT is still the only proof the worker finished.** ⛔ **Signal ingress: the heartbeat is swallowed TWICE (`record_heartbeat` returns False rather than raising + a call-site `except`) — do NOT "clean that up"**; 2 tests raise inside it and assert a byte-identical 200. `webhook_receiver.py:533` (the EOD early return BEFORE the kill+entry gates) UNTOUCHED and test-pinned. 📌 The missing **`DISABLED` boot line** was added too (`main.py:3171` else) — config-off used to log nothing.

## §D — M-O9 **HELD, NOT BUILT** (`docs/audit/mo9_slippage_reference_hold_25jul2026.md`)
⭐ **The trailed SL trigger is NOT PERSISTED at roll-up time.** It lives in `smart_tgt_state.current_sl`; that row is **DELETED on unregister** (`state_store.py:2120`) and only `sl_trail_count` is copied to `trades` (`order_placer.py:2489`). `orders.trigger_price` is modified **at the broker**, not locally. **And the recorder subscribes `async_dispatch=True`** (`slippage_recorder.py:114`) ⇒ reading `current_sl` **races the delete** and would give a silently **bimodal** calibration series.
A sound fix needs the value persisted FIRST = a schema change (unauthorised) **or a write on the order-close path**, which contradicts §D's own calibration-only constraint. **Defect remains UNREACHABLE** (0/421 ever trailed ⇒ `sl_initial` is exactly correct on 100% of real data). D3 **verified not inherited**: `trade_slippage_log` has no reader on the order/capital/sizing/kill path.

**RULE reinforced:** *the ordering of a publish and a delete is not a contract when the subscriber is async.* Check `async_dispatch` before relying on "A happens before B" across an event bus.

---

## 25-Jul ~14:2x — the heartbeat batch DEPLOYED `5512104` (6 commits, `69ba15a..5512104`)
PC == origin == VM bare == `5512104`; 7 changed files **sha256-identical bare-blob vs VM tree**; post-receive "Deployment complete"; **crontab byte-IDENTICAL to the pre-push capture** (160==160, 0 dups, both protected lines unchanged). Trading service **NOT** restarted (`inactive/dead`, `NRestarts=0`, start still Fri 24-Jul 08:15:27) ⇒ **§A/§B load Mon 08:15.** `gui-dashboard` restarted (1994926→2004893, 14:24:12) for the §D1 label; `/`→302, `/api/capital`→401.
Also: **§D1 re-label** — the live reason `get_daily_realized_net_pnl` is avoided is the EOD **`RESET_PNL`** counter-entry, **NOT W10** (fixed 17-Jul); 4 sites + the test pin **UPDATED, not loosened**. **Decision #09 CLOSED = Option A** (no code; there is no `prune` key in `cron_registry.yaml`, so the crontab warning was inapplicable). **§C `trade_review.txt` STOPPED — no such file exists** (see `trade_review_txt_retirement_STOP_25jul2026.md`).

⭐ **TWO METHOD LESSONS FROM THIS BATCH (both cost a re-run):**
1. **The handed-over tests patched `record_heartbeat` with a hand-written spy** — rejected by this repo's own discovery guard `test_cron_heartbeat_contract.py`, which exists because a narrow stub froze the parameter list and broke under F2 (15-Jul). **Use `create_autospec(record_heartbeat, side_effect=spy)`.**
2. **A cross-session BASE is not a BASE.** The morning BASE (12 failures) vs the afternoon MERGE (33) differed by **21**, and 20 were `bash` resolving to the **WSL stub with no distro** in the new shell (Git Bash exists but is later on PATH). Re-taken same-shell: BASE 33 / MERGE 33, **sets byte-identical**, +12 passed = exactly the new tests.
