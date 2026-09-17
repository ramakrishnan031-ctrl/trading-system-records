# NI-1 — THE END-TO-END TRACE · M-1…M-5 · 23-Aug-2026 (Sun), afternoon

**Governed by** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
🏷️ **MEASUREMENT ONLY · ⛔ NO CODE · ⛔ NO PUSH · ⛔ NO DEPLOY · ⛔ NI-1 NOT REVERTED ·
⛔ PS10 NOT REDESIGNED.** All measurements 🔬 at **`742d9da`**.

---

## 🔴 THE HEADLINE — BOTH THE CARD'S HYPOTHESIS AND MY ALARM NEEDED CORRECTING

| claim | verdict |
|---|---|
| 📄 **The card:** *"`sl_distance` is NEGATIVE for a BUY with `sl > entry` ⇒ `:354` should trip immediately"* | 🔴 **REFUTED.** `:406` is `sl_distance = **abs**(entry_price - sl_price)` ⇒ the distance is **+10.0**, not negative. The guard never sees a bad value |
| 📄 **My §3:** *"a class of malformed signal that could never place an order can now place one"* | ⚠️ **CORRECT ON MECHANISM, OVERSTATED ON REACHABILITY.** I never checked where `sl_price` comes from. It is **derived**, and the derivation cannot invert |

⭐ **Stated as plainly as the alarm was:** ⛔ **I overstated it.** The money path is open in
the code, but **nothing on the current signal path can produce the input that opens it.**

---

## M-1 — THE ACTUAL GUARD SEQUENCE, `:323` → PLACEMENT (🔬 `file:line` at `742d9da`)

| # | site | what it checks | does it stop a BUY with `sl > entry`? |
|---|---|---|---|
| 1 | `position_sizer.py:323-335` | **PS10** — `# SL direction sanity (WARNING only, calc proceeds)` | ⛔ **NO — by design.** It warns |
| 2 | `position_sizer.py:406` | `sl_distance = **abs**(entry_price - sl_price)` | 🔴 **THE DECISIVE LINE.** `abs()` makes the malformed distance **indistinguishable** from a well-formed one |
| 3 | `position_sizer.py:411` | `if sl_distance < self._min_tick_size` → `INVALID_SL_DISTANCE` | ⛔ **NO.** `10.0 ≥ 0.05` — the card's expected catch **does not fire** |
| 4 | `position_sizer.py:444` | `QTY_EXPLOSION_GUARD` (`qty_by_risk > max_single_order_qty`) | ⛔ NO — a quantity guard, not a direction guard |
| 5 | `signal_processor.py:1955` | `if not sizing.success` | ⛔ NO — sizing **succeeded** |
| 6 | `signal_processor.py:1973-1976` | `_enforce_strategy_position_cap` · `_enforce_one_trade_per_symbol_direction` | ⛔ NO — counts and dedup |
| 7 | `signal_processor.py:1977` | `risk.approve(symbol, side, intent, sizing, …)` | ⛔ **NO — and it CANNOT.** 🔬 `capital/risk_engine.py` has **ZERO** hits for `sl_price` / `sl_distance`; it is never passed one |
| 8 | `signal_processor.py:1990` | `fm.reserve(symbol, sizing.qty, entry_price, …)` | ⛔ **NO — no SL parameter exists in the signature** |
| 9 | `signal_processor.py:2004` | `update_signal_status(signal_id, "RESERVED")` | 🔴 **CAPITAL IS RESERVED** |
| 10 | `signal_processor.py:2006+` | Step 8 — order placement | — |

⇒ **Between PS10 and capital reservation, NOTHING inspects SL direction.**

## M-2 — CONSTRUCTED AND RUN, ⛔ NOT REASONED

`PositionSizer.calculate("SYM", "BUY", entry=100.0, sl=110.0, "INTRADAY", tier="HIGH")`
against a ₹100,000 / 70-30 / 5× snapshot:

```
LOG WARNING position_sizer.sl_direction_warning
  RETURNED  success=True qty=100 constraint=RISK
  margin_required=2000.0 risk_amount=1000.0
  reason='SYM qty=100 [RISK-bound tier=HIGH(1.0)]: risk_qty=100 capital_qty=3500 conc_qty=100'
CONTROL: BUY entry=100 sl=90 (well formed)
  RETURNED  success=True qty=100 constraint=RISK
```

🔴 **The malformed case and the well-formed control return the IDENTICAL quantity.** That
is `abs()`: the sizer cannot tell them apart, which is precisely why no downstream check
does either. ⭐ The warning is the **only** trace.

## M-3 / M-4 — IT DOES NOT STOP · **BUT THE TRIGGER IS UNREACHABLE**

**M-4's condition is met on mechanism.** Nothing halts it before reservation.

🔴 **AND HERE IS WHAT I FAILED TO CHECK THE FIRST TIME — `sl_price` IS DERIVED, NEVER
TAKEN FROM THE PAYLOAD.** 🔬 Every assignment in `signal_processor._derive_prices` is
direction-aware:

| site | expression | can it invert a LONG? |
|---|---|---|
| `:1663-1669` | `if sl_pct <= 0.0:` → **explicit reject**; schema validates `sl_pct > 0` | ⛔ no |
| `:1669` / `:1671` | `LONG → sl = entry × (1 − sl_pct)` · `SHORT → × (1 + sl_pct)` | ⛔ **no — always below entry for LONG** |
| `:1690` / `:1700` | bounds: `entry − adj_dist if direction == "LONG"` | ⛔ no |
| `:1718` / `:1720` | FIX-130 gap buffer: `LONG → sl × (1 − factor)` — moves **further below** | ⛔ no |
| `:1928` | gate path reads `entry.sl_price` from a `WatchEntry` — itself derived above | ⛔ no |

⇒ ⭐ **On the deployed signal path an inverted SL for a LONG is STRUCTURALLY IMPOSSIBLE.**

### 🏷️ THE CORRECT CLASSIFICATION

**`LATENT`, ⛔ not `LIVE`** — judged by **reachability**, per the standing rule.

- ⭐ **The mechanism is real and worth pinning:** *if* an inverted SL ever reaches
  `calculate()` — a new caller, a payload-sourced SL, an ATR path that returns an inverted
  level, a future refactor — it will size, be approved, and **reserve capital**.
- ⛔ **It is not a live exposure today**, and ⛔ **it does not by itself block push 2.**
- ⚠️ ⛔ **And it is not an argument that NI-1 is wrong.** Before NI-1 the `_warn` call
  raised `KeyError`, so **any** inverted SL crashed that signal's pipeline with an opaque
  *"unhandled"* error. NI-1 makes PS10 behave as its own comment says. 👤 **The open
  question is whether PS10's *"WARNING only, calc proceeds"* design is still what Rama
  wants — that is his, and it predates NI-1 by a long way.**

## M-5 — ⛔ UNANSWERED HERE · **AND THE OBVIOUS SEARCH IS POISONED**

**Search width, stated:** `data_store/trading_system.db` and `data/trading_system.db` —
🔬 **both 0 rows** (schema-only scaffolds; the second has no `trades`/`signals` table at
all). Local `logs/` = **one day** (`2026-08-03`). ⛔ Production is on the VM; I have no read
access this session. ⇒ **a zero here proves nothing.**

🔴 **THE TRAP, and it must be stated before anyone runs this on the VM:**

> ⛔ **Searching production for `sl_direction_warning` will return ZERO BY CONSTRUCTION**
> and that zero is **meaningless**. Before NI-1 the `_warn` call **raised** instead of
> logging, so the warning string could never have been written. **The gate is poisoned by
> the very artifact the change prevents.**

⭐ **THE CORRECT SEARCH** — the signature the old defect actually left behind:

```
signals.status = 'PLACEMENT_FAILED'  AND  reason LIKE '%unhandled%msg%'
logs/system_<date>.log : "Unhandled exception in pipeline" + "Attempt to overwrite 'msg' in LogRecord"
```

`signal_processor.py:418-426` writes `update_signal_status(signal_id, "PLACEMENT_FAILED",
f"unhandled: {exc}")`, and the exception is
`KeyError: "Attempt to overwrite 'msg' in LogRecord"`.
⚠️ **After NI-1 ships, the artifact flips** — from that `PLACEMENT_FAILED` signature to a
`sl_direction_warning` line. Both must be searched, on the correct side of the deploy.

---

## §2 — THE ARITHMETIC, TO PUT TO RAMA · 👤 HIS OWN MODEL

📄 He wrote (in `rama-reply.txt`, ⛔ **still not supplied to me** — 🔬 `find` + `grep` over
the repo return **zero** hits, so I cannot even see the register's citation of it):

> *"Order Value per scrip = Rs 35k/5 = Rs 10k"*

🔬 **The arithmetic:**

| | |
|---|---|
| `35,000 ÷ 5` | = **₹7,000** — ⛔ not ₹10,000 |
| his figure at 5 slots | `5 × 10,000` = **₹50,000** against a **₹35,000** segment ⇒ **42.9% over-allocated** |
| ₹10,000 would require | `35,000 ÷ 10,000` = **max_trades ≈ 3.5** |
| `65b7196`'s actual divisor | `max_daily_trades = 6` ⇒ **₹5,833** |

🔴 **Why it matters:** ⚠️ if the allocation model is ever built to his stated number, it
would size **every MIS trade ~43% too large**, and the over-allocation would only surface
when the 5th slot could not be funded.

⭐ **The quote stays UNSOURCED.** A reviewer saying the file exists does ⛔ not close it —
👤 only Rama supplying `rama-reply.txt`, or quoting the line himself, does.
⚠️ **The real finding stands:** a document Rama has quoted from repeatedly, that the
register cites, and that has **never been supplied** since 22-Aug.

---

## STATUS

⛔ **NOT PUSHED · NOT DEPLOYED · `origin/main` = `45683859a0a05f466189ac5bc98f9a9f089f98d3`.**
⛔ No code · ⛔ NI-1 not reverted · ⛔ PS10 not redesigned · ⛔ nothing adopted.

**Owed to Rama:** 👤 whether PS10's *"WARNING only, calc proceeds"* stands · the M-5
production search (with the poisoned-gate caveat) · a test pinning the inverted-SL path so
the latent case cannot silently become live · and everything already listed in
`GOVERNANCE_DRAFT_RECORD_23-Aug-2026.md`.
