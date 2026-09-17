---
name: test-suite-sends-real-telegram-27jul
description: "The unit suite POSTs real 'MARKET IS CLOSED' alerts to Rama's live Telegram channel — ~50 since 6-May. And orders.status can NEVER be REJECTED, so a rejection count of 0 means 'not recorded', not 'none happened'."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9cadf64c-e510-4d81-a606-31dcc47fea07
  modified: 2026-07-27T07:19:56.389Z
---

**Two defects found 27-Jul from live alerts. Full analysis:
`docs/audit/senco_double_entry_27jul2026.md` + this file. ⛔ Neither fixed (market hours).**

## ⛔⛔ 1. THE UNIT SUITE SENDS REAL TELEGRAM ALERTS TO THE OPERATOR'S LIVE CHANNEL

A "MARKET IS CLOSED · Market Holiday · Today: 27-Jul-2026 · connect on 20-Apr-2026" alert arrived
**while the system was trading 8 trades**. ⭐ **BOTH impossible facts have ONE cause:**
`tests/unit/test_interactive_startup.py:72-73` does
`patch.object(_main_module, "is_trading_day", return_value=False)` +
`patch.object(_main_module, "next_trading_day", return_value=date(2026, 4, 20))`.
**`20-Apr-2026` is a HARDCODED TEST FIXTURE.** `main._send_holiday_notification` is **NOT patched**
and does a **direct `urllib` POST** using the PC's real `TELEGRAM_BOT_TOKEN` /
`TELEGRAM_CHANNEL_PRIMARY` — **no mode guard, no dry-run check, bypassing the whole
sentinel→alert_watcher chain** (which is why it leaves no alert record anywhere).

⭐ **SEVERITY — ANSWERED FIRST, and PRODUCTION IS UNAFFECTED:** the branch ends in `return 0`
(`main.py:1768`), so a process taking it **stands down completely** — but the VM's service started
08:15:30, `is_trading_day` returned True, 8 trades, `NRestarts=0`, and **there is NO
`.holiday_notified_2026-07-27` on the VM.** ⇒ **nothing stood down.** The alert came from THIS PC.

⚠️ **IT HAS FIRED ~50 TIMES SINCE 6-MAY** (`logs/.holiday_notified_*` on the PC, near-daily,
including ordinary trading Mondays; the per-day sentinel is why it is ~1/run-day). ⇒ **a noise class
that trains the operator to ignore a message which, in production, means THE SYSTEM IS DOWN.**
[[feedback-verify-the-finding-premise]]

⭐ **Sibling found while reading:** `_load_holiday_set` accepts **str OR dict** entries;
`get_holiday_name` accepts **dict only** ⇒ a plain-string holiday is a holiday with **no name**,
rendering the generic "Market Holiday". Latent with today's dict-shaped file.

## ⛔⛔ 2. `orders.status` CAN NEVER BE `REJECTED` — a 0 count means NOT RECORDED

⚠️ **I got this wrong this morning and the correction matters.** I reported "zero broker-rejected
orders today". A real broker rejection DID occur (PYRAMID 10:11:14, *"MIS orders are currently
blocked for PYRAMID"*).

**MEASURED:** PYRAMID×2 (FAILED) and KECL (REJECTED) have **0 order rows each**; the 4 CLOSED trades
have **3 each** (ENTRY/SL/TGT). **Across the ENTIRE `orders` table, all time: `COMPLETE` 365 ·
`CANCELLED` 360 · `REJECTED` 0 — the status has never once existed.**
⇒ **A placement-time rejection writes NO order row at all.** It surfaces only as
`trades.status IN ('FAILED','REJECTED')` — **235 all time**, 3–11/day recently.
⭐ **RULE: never count broker rejections from `orders`. Count them from `trades.status`.**

✅ **FIX-181 is still sound — and untouched by this blind spot**, because it counts the **`trades`**
table, not `orders`. Today: **7 trade rows → `count_trades_today()` = 4** (2 FAILED + 1 REJECTED
excluded), **4 of `max_daily_trades: 10`**. It excluded exactly today's real rejections. **The fix
works; my evidence framing was the thing that was wrong.**

## ✅ GUARD BUILT 27-Jul — at the DOOR, not at each sender

`tests/conftest.py::_block_outbound_network` (autouse) patches `socket.create_connection` +
`socket.socket.connect`/`connect_ex` to refuse any **non-loopback** address. One choke point covers
`urllib`, `requests` and `smtplib` alike — **and senders nobody has written yet.** ⭐ **10+ direct
send sites across 8 modules**, so per-site guards would have been the very convention that failed
for eleven weeks.
⭐⭐ **A4 (must not silence PRODUCTION) is satisfied BY CONSTRUCTION, not by testing:** the guard
lives in the test harness and **production code is byte-identical** — a guard production cannot
import cannot misfire there. Pinned by a tree scan.
⭐ **ONE test proves BOTH directions:** the sender still *reaches the socket layer aimed at
Telegram* (⇒ in production it still sends — LOUD) **and** the guard raises (⇒ nothing leaves —
SILENT). 6 tests green.
⭐ **PRECEDENT, and the lesson:** `_isolate_real_sentinels` (23-Jun) was added for **exactly this
class** — "no test can write a CRITICAL alert into the live data_store (the VM alert-watcher would
email it)" — but it guarded **ONE path**. The holiday sender bypasses the sentinel chain entirely.
**Fixing one path of a class leaves the class open.**

## ⚠️ 3. THE MIS BLOCKLIST LEARNS AND IS THEN IGNORED

`data_store/mis_blocklist.json` recorded **`"PYRAMID": "2026-07-27"` TODAY** — recording is
always-on and it worked. **But `mis_filter.enabled: false`** ("master switch; false = fully
dormant"), and even when enabled `shadow: true` = log-only. ⇒ **PYRAMID was attempted TWICE today
(10:06 and 10:11); the system had already learned it was MIS-blocked and placed again anyway.**
⭐⭐ **PROVEN SAME-DAY, from the log: `mis_blocklist: recorded MIS-block for PYRAMID
(date=2026-07-27, ttl_days=1)` appears TWICE.** It learned at 10:06 and placed the identical order
again at 10:11. **The knowledge was recorded correctly and ignored.**

**B1 — WHY OFF: deliberately staged, not dead config.** The yaml says *"master switch; false = fully
dormant (existing flow byte-identical)"* — the house default-off pattern.
**B3 — STALENESS IS ALREADY DESIGNED OUT.** `is_blocked()` = `days < ttl_days`; at `ttl_days: 1` a
symbol is blocked only for the rest of that day, then re-tested. ⭐ A corrupt date **fails OPEN**
("do not block"). The "learns and never forgets" failure mode cannot occur.
**B2 — SIZED, and far bigger than today: 71 attempts across 45 symbol-days = ~30 % of all 235
FAILED/REJECTED trades** are same-day repeats a `ttl=1` pre-drop could have stopped. ⚠️ **UPPER
BOUND** — only MIS-block 400s are recorded, so not all 235 are MIS-blocks.
⭐⭐ **The repeats sit 5–7 min apart — the SAME scanner cadence as the SENCO re-entry.** One root
shape: **the scanner re-fires and nothing remembers the last answer.**
⭐ **Zero-risk next step exists:** `enabled: true` + `shadow: true` = log-would-drop only, behaviour
byte-identical. Measurement for free. ⛔ Signal path ⇒ Rama's call, not enabled.

## ⚠️ 4. THE COOLDOWN — DESIGNED, NOT BUILT (gate in flight); and the replay CANNOT discriminate

⛔ **NOT built:** a full-suite gate was running and **editing source mid-gate is forbidden**
(*"a gate you disturbed is not a gate"*).
**C3 ANCHOR = EXIT, not entry** — because the open-position guard is a **QUEUE, not a filter**;
entry-anchoring lets the queue fire the instant the exit lands, which is exactly today's behaviour.
**C4 SCOPE = per SYMBOL + DIRECTION** (not symbol+strategy): the risk is "we just exited this symbol
at this price", a property of the symbol, not of which strategy noticed — a strategy-scoped rule
would let a *different* strategy re-enter 80 s later, the same defect in a different hat. ⭐ But a
LONG exit → SHORT entry is a genuinely different bet and must stay allowed.
⚠️⚠️ **C5 REPLAY — 15/20/30/40 min ALL give the IDENTICAL answer** (blocks 1, +4.86, n=1); only 60
catches the second (blocks 2, +6.53, n=2). **There is exactly one re-entry under 43.5 minutes in the
whole book, so the replay cannot distinguish 15 from 40.** That is a stronger statement of "no
evidence base" than n=2 alone. ⇒ **build it default-0, never pick a value from this.**
