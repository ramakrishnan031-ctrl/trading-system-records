---
name: batch3-done-17jul
description: "BATCH-3 (17-Jul): X7 exec-log join + X5 OS-owned instance lock SHIPPED; X3 DEFERRED (survivor doesn't cover it). The batch-safe pile is now EMPTY. 2 of 3 ticket premises were wrong."
metadata: 
  node_type: memory
  type: project
  originSessionId: b8e3571f-ea7d-4863-b873-b303871b1932
---

**BATCH-3 — the LAST batch-safe items. 2 shipped + DEPLOYED, 1 deferred on its own precondition.
⇒ THE BATCH-SAFE PILE IS NOW EMPTY.** Report `docs/audit/batch3_done_17jul2026.md`.
System down, off-market waived, book flat. No schema change (v44), no trading-path change.

**✅ DEPLOYED 17-Jul ~14:0x — PC == VM == bare == `2fa08a77`** (tag **`deploy-17jul-batch3` →
`65cd7df`** = the CODE identity + rollback anchor; delta tag..HEAD = markdown only). Backup
`pre_deploy_batch3_20260717_140208.db` (integrity ok, v44, 361 trades). Gates: v44 == expected
44 **no migration** · integrity ok · FK empty · **crontab unchanged (no cron/config/schema file
anywhere in the diff)** · services as expected. **Takes effect at the next 08:15 boot** — the
system was NOT started to apply it. **Watch (X7):** the first fill should write a non-NULL
`parent_trade_id`, a REAL `leg` (SL/TGT rows appearing, not 100% ENTRY) and a non-NULL
`order_timestamp`; the GUI per-trade execution drill-down should stop being empty.
**Rollback:** revert `fd77f80`+`65cd7df`, or reset to `9be3902`. Schema-free.

**⚠️ A grep trap worth remembering:** `grep -c SO_REUSEADDR utils/instance_lock.py` = **3** on the
deployed tree — **all COMMENTS**; `grep -E "setsockopt\(.*SO_REUSEADDR"` = 0. Verify a removed
socket option by **runtime `getsockopt`**, never by source grep (that is exactly how the old
vacuous test lied). Deployed-tree runtime proof: `SO_REUSEADDR=0`, OS lock held, release +
re-acquire works.

| Item | Outcome | SHA |
|---|---|---|
| X7 exec-log `trade_id` NULL | SHIPPED | `fd77f80` |
| X3 retire duplicate `daily_report` | **DEFERRED** | — |
| X5 `instance_lock` singleton | SHIPPED | `65cd7df` |

## ⭐ 2 of 3 ticket premises were WRONG (verified before building)

**X5's premise was BACKWARDS.** Raised as "SO_REUSEADDR lets a second bind ⇒ two instances
⇒ double-trade risk". **Measured** (second bind of a LISTENING 127.0.0.1 port):
`Linux/prod = REFUSED EADDRINUSE(98) with AND without it` · `Windows/dev = SUCCEEDS with it`.
So **P1 was never broken on the platform that trades** — and it is moot anyway, because the
PID layer refuses a second start *before* the socket is reached (proven cross-process on the
OLD code, property-only). The belief came from a **vacuous test**
(`test_phase17_batch3.py:47`) that states the Windows behaviour as universal, concludes "the
real test is whether the code PATHS exist", then asserts `inspect.getsource()` contains
`"bind("` — it cannot fail.
**The REAL prod bug is the opposite direction: a RECYCLED PID blocks a legitimate start.**
`_pid_is_alive()` can't tell the trading system from whatever now holds PID 4711; a crash
leaves the file, `main()` exits 1, and the unit's `RestartPreventExitStatus=3 4` means
**exit 1 is RESTARTED ⇒ restart loop = silent total outage**. Fix = OS-owned lock
(`fcntl.flock`/`msvcrt`) the KERNEL drops on any death ⇒ a stale lock is impossible *by
construction*. Also: lock file **never unlinked** (flock's inode/unlink race — unlinking a
path a live instance holds lets the next start lock a FRESH inode and run alongside).
`_pid_is_alive` **KEPT** (`reconstruct_excursions.py:363` imports it).

**X7 was UNDERSTATED by five columns.** Not a missing field — **the lookup key**.
`orders`' PK is the **BROKER** order id (`order_manager.insert_order:290-291` — "internal_order_id
is NOT stored"), but `_enrich_order` queried `WHERE order_id=?` passing `ev.internal_order_id`
⇒ **matched nothing, ever**. Live: `parent_trade_id`/`order_type`/`qty`/`strategy_name`/
`signal_id`/`order_timestamp` **NULL 262/262 each**; `is_partial`=0 262/262; 0 rows joinable
to `orders`; `market_execution_context` **262/262 NULL trade_id+leg** (its `idx_mec_trade`
indexed nothing). **`leg` was WRONG, not missing**: `leg or "ENTRY"` labelled all 262 rows
ENTRY when live had **155 ENTRY + 79 SL + 50 TGT + 21 EOD** ⇒ ~107 exit fills silently
relabelled as entries. Now → `UNKNOWN` when unresolved (col is NOT NULL; must write
something, must not write a lie).
**Unblocks two dead consumers, NEITHER of which had adapted** (the opposite of E4/W10 —
checked first): `db_reader.py:1397` per-trade drill-down (`WHERE parent_trade_id=?` → 0 rows
for every trade) and `db_reader.py:1063` `execution_log_today` (`WHERE order_timestamp LIKE ?`
— the recorder never wrote that column at all; now from `orders.placed_at`).
**Order path NOT touched**: `_WatchEntry` has no `trade_id`, so making `order_monitor` publish
one = editing the order path for a reporting column ⇒ declined per the escalation valve. The
whole fix lives in the async recorder that "can never block trade execution".

## ⛔ X3 DEFERRED — the survivor does NOT cover the generator

The instruction made it conditional; **the condition is not met.** Do not retire on suspicion.
- **`daily_trade_review.py:2112` says so ITSELF**: emits `{"section":"Telegram","coverage":"0%","note":"not in DB → W1"}`
  (and line 2222 lists the gap). **`candle`/`Candle` = 0 hits** in the whole module. No Capital sheet.
  `daily_report` has 7 sheets incl. **Capital · Candles · Telegram** — 3 uncovered.
- Its docstring (17-18): "Runs PARALLEL to reports/daily_report.py … it does NOT edit, retire, or re-cron them."
- **Not dead**: `daily_report` ran SUCCESS 16:05 on 14/15/16-Jul; pings Telegram on completion.
  GUI `/api/reports/download` is 403-gated (`reports_download_enabled=false`, **Q3 pending**) —
  a pending gate, not a decision the artifact is unwanted.
- **Near-miss**: `gemini_weekly_patterns.py:110` reads `daily_report_<date>.{md,txt}` via
  `read_text()` — right dir, but `daily_report` only writes `.xlsx` ⇒ **that read has NEVER
  found a file**. A dormant pre-existing bug, NOT a live consumer (and not evidence of deadness).
- **Cascade**: `fetch_daily_candles.py` exists SOLELY to feed it ("consumed by reports/daily_report.py")
  ⇒ retiring one orphans the other.
- **To retire later, in order:** resolve **W1** (Telegram → DB) → decide if Candles/Capital are
  wanted at all → retire `daily_report` **+ `fetch_daily_candles`** together (cron+docs+SYSTEM_MAP,
  one commit) → fix-or-delete the gemini `.md/.txt` read either way.

## Process notes worth keeping
- **Both fixes' RED-on-old was proven on the TRUE pre-change tree** (`git checkout HEAD -- <file>`
  + grep-confirm absent + check rc; never `git stash`). X7: 4F/21P rc=1 → 25P. X5: Linux 4F/15P → 19P.
- **X5 was verified on BOTH platforms** because the fix takes DIFFERENT code paths (`fcntl` vs
  `msvcrt`) — Windows-green proves nothing about prod. Linux 19/19 · Windows 19/19.
- **I caught my own vacuous assertion**: my first X5 test grepped `inspect.getsource()` for
  "SO_REUSEADDR" and failed on the *comment* explaining the change — the exact style I was
  criticising. Replaced with a live `getsockopt` check.
- **I caught my own false RED**: `test_p1` asserted the NEW message wording, so it went red on
  old for the wording, not the property — which would have mis-reported WHICH property was
  broken. Relaxed to the property; the honest answer is P1 was fine, P2 was not.
- **I caught my own bad citation**: cited `order_manager.record_order`; the function is
  `insert_order`. Amended before push.
- Both suites were **vacuous exactly where the bugs lived**: `_FakeStore.fetch_one` answered
  ANY "FROM orders" query regardless of key, and every test hand-set `ev.trade_id` (no real
  publisher does). `test_fails_when_same_pid_alive` wrote pytest's own PID and demanded refusal
  = the recycling outage encoded as a REQUIREMENT. Both inverted deliberately.

Related: [[feedback-verify-the-finding-premise]] [[feedback-verify-rc-not-output]]
[[s1s3s5-done-17jul]] [[e4-w10-done-17jul]] [[pc-test-env-hygiene]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 670 B (budget 450 B). The index now carries a hook and this link.

- ✅🚀🔝🏁 **[BATCH-3 DEPLOYED 17-Jul — `2fa08a77`, tag→`65cd7df`; PC==origin==VM. ⭐ THE BATCH-SAFE PILE IS NOW EMPTY](batch3_done_17jul.md)** — **X7** exec-log join (the lookup keyed `orders` on the internal id; PK is the BROKER id ⇒ 6 cols NULL 262/262 + `leg` WRONG-not-missing) · **X5** instance lock now OS-owned (the real bug was a recycled PID **blocking** a restart ⇒ restart-loop outage; `SO_REUSEADDR`/two-instances was **false on Linux**) · **X3 DEFERRED — the survivor doesn't cover it and says so itself**. **⭐ 2 of 3 ticket premises were wrong.** 10F/4849P 0 attributable; v44 no-migration; crontab unchanged. [[batch3-done-17jul]]
