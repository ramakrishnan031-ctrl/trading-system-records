---
name: no_order_path_can_send_market_09sep
description: Every MARKET exit in this system is unplaceable -- the Kite chokepoint has no market_protection kwarg, and entries never hit it because entries are LIMIT.
metadata:
  type: project
---

**MEASURED 09-Sep-2026 at `3b15bbf`.** Zerodha refuses `MARKET` without market
protection.

⭐ **THE LIBRARY SUPPORTS IT -- the gap is ours.** 🔬 `kiteconnect` **5.1.0** on all
three machines; `KiteConnect.place_order(...)` ends with **`market_protection=None`**
(`-1` = automatic, or `>0` up to `100` as a percentage). Its body is
`params = locals()` with every `None` **stripped**, so passing nothing DELETES the
key and the order arrives unprotected -- exactly the rejection text. ⛔ No `**kwargs`:
only named params marshal. ⇒ **a protected MARKET order is available today; it is one
parameter at the adapter, NOT a new order type.**

⛔ **But this system cannot express it** -- `market_protection` is not a parameter
anywhere in OUR placement path:

- `broker/zerodha_adapter.py:478` `place_order(...)` signature: symbol, side,
  qty, price, order_type, intent, tag, trigger_price, variety. **No
  market_protection.**
- `broker/zerodha_adapter.py:604-614` is the ONLY call to `kite.place_order`.
  Kwargs: variety, exchange, tradingsymbol, transaction_type, quantity, product,
  order_type, price, trigger_price, tag. **No market_protection.**

⛔ **THERE IS NO ENTRY/EXIT ASYMMETRY TO CLOSE.** Both go through that one
chokepoint. 🔬 All-time `orders` by leg: **ENTRY=LIMIT 735 · EOD=LIMIT 28 ·
SL=SL 327 · TGT=LIMIT 311 — zero MARKET rows, ever.** Entries never hit the wall
because entries are LIMIT. The MIS squareoff is the only path that sends MARKET.

⛔ **The "9 market_protection reconciliation rows prove we met this before" read
is FALSE.** In `docs/incident/2026-09-03_ANANTRAJ_broker_book.json` the field
appears **51 times, value `0` every time** -- the broker echoing "unset". It is
evidence the constraint was NEVER met.

**FOUR senders of MARKET, all unplaceable:** `mis_autosquareoff.py:636` PASS_1;
same line PASS_2 via `PASS_2_EXIT_PROTOCOL="MARKET"` (:93);
`order_reconciler.py` check9 EMERGENCY MARKET EXIT (~:3080, `order_type="MARKET"`,
`price=0.0`); `eod_squareoff.py` LIMIT_THEN_MARKET phase 2 (never exercised).

⭐ A proven LIMIT exit already exists: `eod_squareoff.py:1275-1286` prices
`LTP*(1∓limit_aggressive_pct)`, batch LTP at `:1130-1139`. ⛔ But its phase-2
fallback is MARKET -- a naive port inherits the same wall.

See [[restore_side_is_empty_because_the_query_omits_the_column_09sep]].

## ⭐ 10-Sep-2026 — `-1` vs A NUMBER: MEASURED, AND THEY NEED **ONE** MECHANISM
🔬 Built the param dict exactly as `place_order` does and form-encoded it with
`requests` (`kiteconnect` 5.1.0, `C:/python311`), ⛔ no broker call:

| passed | key present | wire |
|---|---|---|
| `None` (today) | False | `<ABSENT>` |
| `-1` | True | `market_protection=-1` |
| `5` | True | `market_protection=5` |
| `0` | True | `market_protection=0` |
| `2.5` | True | `market_protection=2.5` |
| `999` / `-7` | True | `market_protection=999` / `-7` |

⭐ **`-1` MARSHALS IDENTICALLY TO ANY NUMBER** — one form field in an
`application/x-www-form-urlencoded` POST body (`_request` passes `data=params`,
`is_json` False). ⇒ ⭐ **PASS_1 and PASS_2 can be "materially different" through ONE
parameter; ⛔ `-1` needs no special handling.**

🔴 **THE SDK VALIDATES NOTHING.** `999`, `-7`, `0`, `2.5` and the STRING `"-1"`
all reach the wire unchanged. The only filter is `if params[k] is None: del` — and
`0 is None` is False, so **`0` IS SENT** while `None` is dropped. ⛔ A range check is
**ours to write**; ⛔ never assume the library refuses a bad value.

⚠️⚠️ **WORDING WITHDRAWN (👤 FILE, 10-Sep): ⛔ NEVER "protected market always
fills".** ⭐ Write instead: *"Protected MARKET is available through the installed SDK
and is materially different from today's unprotected MARKET request, but it does not
guarantee execution. Final correctness still requires broker-position confirmation."*
⭐ **THE AGREED WORDING (👤 10-Sep, supersedes any earlier phrasing):** *"Zerodha's protected MARKET behaves with a protected execution range and may leave unfilled quantity open when price moves beyond that range."* ⛔ Never describe the internals more precisely than that — we have not observed them.

📦 **INSTALL HYGIENE, MEASURED:** `site-packages` carries **TWO** dist-info dirs,
`kiteconnect-5.1.0` and `kiteconnect-5.2.0`, so `importlib.metadata` enumerates the
package **twice**. ⭐ The 5.1.0 install is the later one (12:07:51 vs 12:06:33) and
owns the files; `pip show`, `__version__.py` and `requirements.txt:8` all say
**5.1.0**. ⚠️ `utils/startup_checks.py:49` imports `importlib.metadata.version` —
⛔ check it before trusting any version gate.

⭐ **THE TWO CALL SITES ARE STILL EXACTLY TWO** (verified at `3b15bbf`, deployed tree
md5-identical): `zerodha_adapter.py:604` `place_order`, `:1092` `modify_order`.
⛔ Nothing else in non-test code calls Kite to place or modify.
