---
name: test-side-effect-class-27jul
description: "The sweep of what a test can reach in production: network is now closed, but logs/, data_store/*.db and reports/ are OPEN — and the test env holds every live production credential."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9cadf64c-e510-4d81-a606-31dcc47fea07
  modified: 2026-07-27T10:45:22.634Z
---

⭐ **THE CLASS: side effects escaping the test suite.** The 23-Jun
`conftest._isolate_real_sentinels` was built for exactly this and guards **ONE path**.
**Fixing one path of a class leaves the class open — the sweep is the deliverable, not the patch.**
Evidence the original guard was incomplete: **50 stale `.holiday_notified_*` on the PC.**

## §D — every path a test can write to a REAL production artifact

| artifact | status | evidence |
|---|---|---|
| CRITICAL sentinels (`write_critical_sentinel`) | ✅ **ISOLATED** | `_isolate_real_sentinels`, 23-Jun |
| outbound network (Telegram/SMTP/broker/any) | ✅ **ISOLATED 27-Jul** | `_block_outbound_network` |
| `logs/` | ⚠️ **OPEN** | **PROVEN: 50 holiday sentinels written, 6-May→27-Jul** |
| `data_store/**` (any sqlite open) | ✅ **CLOSED 27-Jul `1542c6e`** | was: mtime 14:54, my own test runs |
| `reports/` | ⚠️ **OPEN — DEFERRED, see below** | 9 files modified since 20-Jul |
| memory palace | ✅ n/a | outside the repo; no test path reaches it |

⚠️⚠️ **THE SHARP VERSION: the suite HAS run on the VM before** — that is *why* the 23-Jun sentinel
guard exists ("a full-suite run on the VM was emailing test-written CRITICALs"). On the PC an
unisolated DB write is low-harm scratch; **on the VM the same path is the LIVE
`data_store/trading_system.db`.** ⛔ Related standing rule: never `scripts/*.py --db <copy>`.
## ✅ `data_store/` CLOSED 27-Jul `1542c6e` (`fix-tests-27jul`, PUSHED)

`conftest::_block_real_data_store` patches **`sqlite3.connect`** — the DOOR, since 10+ modules call
it (`core/db_connect`, `core/state_store`, `ops_dashboard`, ~6 scripts). Covers the bare relative
path (**how a test picks the live DB up by accident**), the `file:...?mode=ro` URI, the analytics
sibling, and any `data_store/<subdir>/`. ⭐ **Reads blocked too, deliberately** — a ro open of a WAL
DB still creates `-shm`/`-wal` sidecars, so "just reading" the live DB is not side-effect free.
⭐ **Opt-in is EXPLICIT** (`allow_real_data_store` fixture, visible in the test signature, not a
hidden exclusion list). ⭐⭐ **ZERO existing tests need it** — 248 tests across the 4 DB-heaviest
suites pass with no trips. **That count IS a finding: the hole was LATENT, not routinely exercised.**
🔬 RED-first: disabling the guard ⇒ the blocked-path tests go green→red; conftest restored
md5-identical `7502f477210d`.

## ⏳ `logs/` + `reports/` — DEFERRED 27-Jul, WITH THE REASON

⛔ **Not done, and not because time ran out — because the risk is different in kind.** A stray write
to `logs/` or `reports/` is **cosmetic pollution**; a stray write to `data_store/` on the VM is the
**live trading database**. Only the latter can touch capital, so it took the remaining time.
▶️ **When picked up: same door-level shape** (patch the write primitive, not each caller), same
explicit opt-in, same RED-first. Evidence they are open: the **50 stale `.holiday_notified_*`**
(logs/) and **9 report files since 20-Jul**.

⛔ **The rest REPORTED, NOT FIXED — D4: knowing where they are is the value; do not refactor.**

## §C — what the TEST environment holds that PRODUCTION owns

**20 keys in the PC `.env`, all live:** `TELEGRAM_BOT_TOKEN` · `TELEGRAM_CHANNEL_PRIMARY` /
`_SECONDARY` / `_PERSONAL_CHAT_ID` · `WEBHOOK_SECRET` · `ZERODHA_API_KEY_*` ×4 ·
`ZERODHA_API_SECRET_*` ×4 · `ZERODHA_TOTP_*` ×4.
⭐ **The network guard is the DOOR; a separate test token is the BLAST RADIUS if the door is ever
opened.** The guard stops the send — it does **not** stop a test reading, logging or mis-using a real
token, and it is **in-process only, so a test that spawns a SUBPROCESS which sends is not covered.**
⛔ **Do not weaken the guard to make a test token work** — a test that needs a test channel opts in
explicitly; the default stays no-network.

## ✅ BUILT 27-Jul (all on `fix-symdir-27jul`, UNPUSHED)

- **`214a878` THE SEND-SIDE AUDIT TRAIL.** ⭐⭐ **Before it, the alert stream could not be audited
  below CRITICAL**: no `telegram_notifier` logger line existed in `system_<date>.log` on a normal day
  (`send()` logged only on the disabled branch), sentinels are CRITICAL-only, and
  `failed_alerts.log` records **failures only** (last entry **2-Jul**). ⇒ *"did every broker event
  produce an alert?"* was **unanswerable from the system's own records**.
  ⭐ **The OUTCOME field is the point, not the send** — `delivered` / `failed` / `suppressed` /
  `suppressed_disabled`, read off the existing `SendResult`. ⛔ **A LOG, never an alert**; ⛔ **can
  never break a send** (wrapped; the caller's result object is returned unchanged — tested with a
  logger that raises on every call). 7 tests, 3 plants RED.
  ⚠️ **It closes the gap FORWARD ONLY. Today's 3 placement failures (PYRAMID×2, KECL) stay
  unanswerable — there is no source to reconstruct them from.**
- **`b7f5eef` mis_filter → SHADOW** (`enabled: true`, `shadow: true` = log-only, falls through at
  `secondary_screener:159`). Byte-identical behaviour is the licence. ⛔ **shadow:false is the
  ENFORCING change and is Rama's** — a drift to it goes RED.

## ⛔ DECIDED, NOT DEFERRED — MIS→CNC FALLBACK WILL NOT BE BUILT

Rama, 27-Jul: ~30 trades/month, no assurance of a better outcome, and it would mean running two
product windows for a handful of trades. ⭐ **ARCHITECTURE SETTLED: INTRADAY = MIS · DELIVERY =
CNC/GTT.** Remove from the queue as a decision made.
