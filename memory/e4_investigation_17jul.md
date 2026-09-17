---
name: e4-investigation-17jul
description: "E4 investigated read-only 17-Jul — E4 IS W10, one pnl_delta contract mismatch; fixing either half alone is a regression. Normal exits already pass real costs; only 3 backstop paths pass costs=0.0."
metadata: 
  node_type: memory
  type: project
  originSessionId: a8c00bd7-f7a4-4643-bf7d-9bab09ae2c49
---

**READ-ONLY investigation, 17-Jul. Nothing fixed, nothing pushed.** Report:
`docs/audit/e4_investigation_17jul2026.md`. Feeds the design step (Web Claude → ChatGPT → implement).

## ⭐ THE STEER — do NOT "just pass the real costs"; that alone makes it WORSE
**E4 and W10 are ONE bug: a `pnl_delta` contract mismatch. Either half alone is a regression.**
- **WRITER** `capital/fund_manager.py:1228` `pnl = gross_pnl - costs` → `:1251 pnl_delta=pnl`
  (**NET**) + `:1252 costs=costs` stored alongside.
- **READER** `core/state_store.py:2447` `get_daily_realized_net_pnl` = `SUM(pnl_delta) −
  SUM(costs)`, and its docstring (`:2434`) **wrongly claims `pnl_delta` is gross** ⇒ **costs
  subtracted TWICE**. This is **W10** — already known, **OPEN, 0 fix commits**
  (`audit_05jul2026.md:572`, `pending_reconciliation_14jul2026.md:73`, classified LOOP).
- **E4 alone** (pass real costs into the 3 backstop paths) ⇒ those rows become net and the reader
  double-subtracts them too ⇒ **understatement becomes a double-count on EVERY close**.
- **W10 alone** ⇒ the 36 backstop rows stay **gross** ⇒ the limit keeps under-counting exactly the
  forced exits (RMS/CHECK1) that matter most.

## ✅ NORMAL EXITS ARE ALREADY CORRECT (for the cost input)
All **4** production callers of `release_used`:
| Caller | costs |
|---|---|
| `orders/order_placer.py:2410` **normal exit** | **`costs=charges`** ✅ REAL |
| `orders/order_reconciler.py:1109` CHECK1 | `0.0` ❌ |
| `orders/order_reconciler.py:1901` partial (M-O2) | `0.0` ❌ |
| `orders/cnc_gtt_monitor.py:450` CNC/GTT | `0.0` ❌ |

**WHY they pass 0.0: neither `order_reconciler` nor `cnc_gtt_monitor` holds a `CostCalculator`
at all** (grep=0 in both). **Missing wiring, not broken arithmetic.**

## COST SOURCE — exists, and parity is FREE
`broker/cost_calculator.py` → **`CostCalculator.round_trip_breakdown(qty, entry_price,
exit_price, product).total`** (already used at `order_placer.py:2301-2307`). Built at
**`main.py:1786` BEFORE the `if args.mode == "paper"` branch ⇒ mode-agnostic, one instance,
config-driven ⇒ no paper/live fork.** The reconciler needs only `product` (via the existing
`ProductResolver`, `main.py:1785`) + the injected instance. **Nothing to compute from scratch.**
⚠️ `order_placer:2314` silently falls back to `charges = 0.0` on exception — same silent-gross
failure mode on the good path; the fix should decide whether that stays silent.

## THE GAP — two errors, OPPOSITE directions, they do NOT cancel
| Rows | pnl_delta | costs | reader sees | effect |
|---|---|---|---|---|
| **119** normal exit | net | charges | gross − **2×**charges | **loss OVERSTATED** (Σcosts 60.24) |
| **36** CHECK1/RMS/GTT | **gross** | 0 | gross | **loss UNDERSTATED** ← E4 (≈₹18 est., never recorded) |

**16-Jul live: control saw −4.01 vs a TRUE net of −2.62 (53% too big).** Proof `pnl_delta` is
NET: `release_used:1246` writes `reason="pnl={pnl} costs={costs}"` where `pnl = gross−costs`, and
it matches the column exactly (`pnl_delta=2.43, costs=0.49, reason "pnl=2.43 costs=0.49"`).

## BLAST RADIUS
**BOTH daily-loss halves read the W10 function** ([[dual-daily-loss-mechanism]]):
post-close breach `fund_manager.py:1279` · **pre-trade gate** `risk_engine.py:25` (RE7) via
`get_snapshot()` `:1507` · **`reset_daily_pnl:1603`** (must move in lockstep or EOD zeroing
breaks — the data shows `Σpnl_delta == Σcosts` on every completed day, i.e. the reset is built ON
the bug) · `:1736` logging only.
**Available capital** (`:1231/:1257/:1259`) uses `pnl` **ONCE** ⇒ **correct on the normal path**,
over-credited on the 3 backstop paths (and `_total`, the limit's denominator, drifts up).
**Rehydrate** (`:1706-1708`) uses `pnl_delta` directly and does NOT subtract costs ⇒ consistent
with NET; would **break** if a fix made `pnl_delta` gross.
**Already routing around W10 — do NOT "fix" these:** `capacity.py:15` (**D2, approved permanent,
G2a**) · `risk_capital.py:37` · `db_reader.py:300/840` · `daily_trade_review.py:1068` (states the
bug verbatim). **⇒ `pnl_delta`-is-NET is the ESTABLISHED contract; the reporting layer was fixed,
the CONTROL was not.**
**Regression surface (several encode the CURRENT double-subtracting semantic ⇒ expect a ratified
contract inversion like M-C6/FIX-133):** `test_fund_manager.py:2318` · `test_mo2_check4_partial_capital.py:200/253/278`
· `test_migrations.py:234` · `test_fix128_daily_loss_sequence.py` · `test_daily_trade_review.py:499`.

## RECOMMENDED DIRECTION (design step decides)
Make `pnl_delta` mean **NET, always** (the contract the writer, rehydrate, GUI, reports + D2
already assume): **(1)** reader → `SUM(pnl_delta)` + fix the false docstring; **(2)** inject the
existing CostCalculator into reconciler + gtt_monitor and pass real charges; **(3)** `reset_daily_pnl`
in lockstep; **(4)** decide the silent `charges=0.0` fallback; **(5)** consider persisting `trade_id`
on RELEASE_USED rows.
**⚠️ RISK-POSTURE CHANGE to state to Rama: the fix removes today's accidental conservatism ⇒ the
loss limit will trip LATER than it does now on normal exits.** Today: overstated (trips early) on
normal exits, understated (trips late) on backstops.

## Side finding
`release_used` receives `trade_id` (`:1170`) but **never passes it to `_write_ledger`** ⇒
**155/155 RELEASE_USED rows have `trade_id NULL`** ⇒ the ledger cannot be joined to `trades`,
which blocks per-trade reconciliation of exactly this bug.

Links: [[capital-operational-note]] [[dual-daily-loss-mechanism]] [[deploy-batch1-done-16jul]]
[[sweep-done-17jul]] [[feedback-verify-the-finding-premise]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 1445 B (budget 300 B). The index now carries a hook and this link.

- 🔴💰 **[E4 INVESTIGATED (17-Jul, read-only) — E4 *IS* W10; fixing either half ALONE is a regression](e4_investigation_17jul.md)** — the *why* (still valid; the fix is ↑) — **STEER: do NOT "just pass the real costs".** WRITER `fund_manager.py:1228/1251` stores `pnl_delta = gross−costs` (**NET**); READER `state_store.py:2447` computes `SUM(pnl_delta)−SUM(costs)` (docstring wrongly says gross) ⇒ **costs subtracted TWICE** = **W10, already OPEN, 0 fix commits**. **Normal exits ALREADY pass real costs** (`order_placer.py:2410`) ⇒ E4 is scoped to **3 backstop paths** (`order_reconciler:1109/:1901`, `cnc_gtt_monitor:450`) which pass 0.0 **because neither class holds a CostCalculator at all** (missing wiring). Live: **119 rows OVERSTATE the loss vs 36 rows UNDERSTATE it** — they don't cancel; 16-Jul the control saw **−4.01 vs a true −2.62**. **BOTH loss halves read it** (post-close `:1279` + pre-trade `risk_engine.py:25` RE7); `reset_daily_pnl:1603` is built ON the bug. Available capital uses `pnl` **once** ⇒ right on the normal path, over-credited on the 3. **Parity free** (`CostCalculator` built at `main.py:1786` *before* the mode branch). GUI/reports already route around it (**D2 approved permanent**) ⇒ NET is the established contract; the CONTROL was never fixed. **⚠️ A fix makes the limit trip LATER on normal exits — a live risk-posture change.** Nothing fixed. [[e4-investigation-17jul]]
