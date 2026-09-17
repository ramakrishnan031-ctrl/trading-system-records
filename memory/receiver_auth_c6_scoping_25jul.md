---
name: receiver-auth-c6-scoping-25jul
description: "C6 scoping — the receiver has only TWO routes; auth STATE is already shared, only the CHECK is duplicated. PB-01's route is safe (it IS /webhook/<scanner_name>); the real Monday risk is a swallowed boot-wiring except."
metadata: 
  node_type: memory
  type: project
  originSessionId: f2fbf924-aa62-447a-8c75-c058b96e494a
  modified: 2026-07-24T21:01:36.447Z
---

**READ-ONLY scoping, 25-Jul-2026, HEAD `570b3e8`.** Report:
`docs/audit/receiver_auth_c6_scoping_2026-07-25.md`. Nothing changed, nothing designed.

**⭐ C6 IS SMALLER THAN ITS NAME SUGGESTS.** `signals/webhook_receiver.py` registers exactly
**TWO** routes — `GET /health` (`:271`) and `POST /webhook/<scanner_name>` (`:330`). And the
auth **STATE is already shared**: `_secret` (`:159`), `_require_hmac` (`:169`), `_ip_limiter`
(`:214`) are instance attributes both routes read (`/health` via the `receiver = self` closure
at `:269`). ⇒ **C6 is not "introduce shared auth state" — it is "collapse two spellings of one
three-way decision into one call site."** `/health` accumulates an `ok` bool then one 401
(`:291-317`); `/webhook` returns early per branch (`:472-494`). Same policy, two idioms, patched
separately (G.1 hit `/webhook` first; `/health` got a parity fix later).

**✅ PB-01 IS SAFE FOR MONDAY — and is NOT a C6 blocker.** `/webhook/pb01_breakout_retest` is
**not a separate route**; it IS `/webhook/<scanner_name>`, so its auth is byte-identical to the
trading routes by construction. Auth `:472-494` runs BEFORE the EOD dispatch `:507-509`
(`_handle_eod` docstring records it, `:696`). Unknown-scanner 404 is also post-auth ⇒ no
unauthenticated scanner enumeration.

**⚠️🔴 THE REAL MONDAY RISK IS BOOT WIRING, NOT AUTH.** `_eod_capture` is **late-bound**
(`main.py:3203 set_eod_capture`, NOT passed at construction `:2890-2898`), and the whole PB-01
block sits in `except Exception → log ERROR → pb01_capture_worker = None` (`main.py:3208-3210`).
If it raises at 08:15, the 17:00 alert returns **200 `{"accepted":0,"captured":0,"detail":
"watchlist disabled"}`** (`webhook_receiver.py:718-722`) — one WARNING, no Telegram, no
heartbeat. **An empty Tuesday `pb01_watchlist` would look identical to "no breakouts" AND to
"the service died at 16:20".**
⭐ **FREE MITIGATION:** grep the Monday 08:15 boot log for
`"V3 Step 10b PB-01 watchlist: ENABLED"` (`main.py:3206`). Absent, or `"pb01 watchlist wiring
failed"` (`:3209`) present ⇒ no capture will happen — known hours before 17:00, with time to act.

**Four divergences a refactor must not flatten** (full list §B6 of the report): `/health` signs
`b""` so a valid `/health` signature is a per-secret CONSTANT and replayable, `/webhook` signs the
body · `/health`'s uniform "authentication required" is a deliberate anti-oracle (naming the
reason would leak `require_hmac` state) · **the EOD route returns at `:509` BEFORE the kill and
entry-window gates — that early return is what makes the 17:00 capture possible at all** ·
`/webhook` writes a `webhook_audit` row on every outcome incl. 401, `/health` writes none (so a
brute-force on `/health` leaves no audit row).

**Secret:** ONE value, no per-route tokens — `os.environ.get("WEBHOOK_SECRET")` (`main.py:2897`),
**required in BOTH modes** with fail-fast (`main.py:226`, C-2 02-Jul) ⇒ the `if self._secret:`
guards are **unreachable-false in production** (test-only paths). Chartink sends it as `?token=`,
accepted only while `require_hmac=False`. [[require-hmac-keep-false-20jul]]

**Pre-auth work on `/webhook`** (not defects; a refactor must know): `request.get_data()` at
`:404` reads the body before auth (unavoidable — the HMAC is over the body; capped 1 MB `:220`),
and `_write_audit` DB rows are written on the 503/429 exits (`:411`, `:421`) — i.e. an
unauthenticated caller can cause audit rows, bounded by the IP limiter.

📌 **Line-number drift caught:** the 24-Jul reports cite `watchlist.enabled` at
`system_config.yaml:434`; the 25-Jul service-window deploy inserted 8 lines into `trading_hours`
above it, so it is now **`:442`**. Apply a +8 shift to any 24-Jul citation below `trading_hours`.
[[service-window-configurable-25jul]] [[feedback-verify-the-finding-premise]]
