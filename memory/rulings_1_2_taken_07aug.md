---
name: rulings-1-2-taken-07aug
description: "Rulings 1 (G2a is the control-inventory authority) and 2 (one open position per symbol, account-wide) TAKEN by Rama 07-Aug-2026 — and the verification reversed the sequencing: F6 is Ruling 2's PREREQUISITE, not its beneficiary."
metadata: 
  node_type: memory
  type: project
  originSessionId: e3d9dec6-1430-4604-9156-4842389f2b23
  modified: 2026-08-07T10:55:55.638Z
---

**07-Aug-2026 — Rama took decision-ledger rows 1 and 2.** Docs-only; `git diff 348c226..HEAD -- '*.py' '*.yaml' '*.sql'` is EMPTY. Report `docs/audit/rulings_1_2_verification_07aug2026.md`; ruling text `docs/MASTER_PENDING_01-Aug-2026.md` §R.

## RULING 1 — the control inventory
**`ops_dashboard/docs/G2a_capacity_inventory.md` IS THE AUTHORITY (44 rows).**
- ⛔ `docs/audit/audit_05jul2026.md:527` (27 rows) is **SUPERSEDED** — frozen history, pointer only, rows untouched.
- ⛔ `docs/design/sizing/config_surface_review_06aug2026.md` is **MERGED IN** — evidence, never an inventory.
- ⛔ **DO NOT MOVE the G2a file.** It lives under `ops_dashboard/` on purpose-by-accident; `capacity.py` consumes it and the location is a separate untaken decision.
- Merge arithmetic **30 + 14 = 44**; leaf coverage **169/301** measured; uncovered **98 signal-gen + 34 infra = 132**.
- ⛔ It does **not** hold "113 keys" — the 113 is a **scope count, never a row set**.

### STALE VALUES the old inventories carry — re-read before quoting either
`max_consecutive_losses` = **4** (both said 5) · **`force_intraday_only: false`** + `delivery_enabled: true` ⇒ the delivery caps tagged **INERT** in both are **LIVE** · `alerts.*` = **31** keys (review said 9) · `entry_gate.*` = **17** (review said 9). ⭐ **10 of 11 shared families disagree with the measured config; only `drift_handler.*` (4) matches** — a family counted as if it were a key, the same shape as the `31+34+6+42=113` accident.

### The rule bound AND needed amending
It stopped a third inventory being written, and stopped 113 rows being fabricated — then still needed **ROW UNIT · INCLUSION RULE · VALUE PROVENANCE** added, because the dotted key is a sufficient JOIN identifier and an insufficient MERGE one. 🏷️ Fourth campaign rule found wanting **by being run, not read**.

## RULING 2 — one simultaneous open position per symbol, account-wide, pipeline-independent
Reject while any open position exists; **eligible again the instant it is flat**; *"evaluated from the current account state, not from historical ownership."*

**⭐⭐ GATES 2 AND 3 ALREADY IMPLEMENT IT** — `DUPLICATE_SYMBOL` (`capital/risk_engine.py:688-694`) and `CONTRARY_POSITION` (`:665-686`) are product-blind, have **no date term**, and release the instant the trade leaves `PENDING_FILL/OPEN/PARTIAL`. They read **one predicate twice**, which is why `REJECTED_CONTRARY_POSITION` is **0 in 109,254 signals**.

**Only gate 1 is date-scoped** — `SYMBOL_DIRECTION_DAILY_LIMIT`, `signals/signal_processor.py:706-720` — and it is the only one with a config key ⇒ the loosening half is **one boolean**, `risk.one_trade_per_symbol_direction_per_day: true→false`, byte-identical to the pre-27-Jul path by the code's own docstring. ⛔ **NOT AUTHORISED, NOT FLIPPED, NOT STAGED.** It re-admits the SENCO class (27-Jul: re-entry 80 s after its own TGT, above that price, gave back 83 % of the gain).

**A FOURTH site emits the identical label** — `allocation/portfolio_allocator.py:182-183`, a batch rule, inert (`allocator_mode: shadow`), and in **no** inventory before today. **A FIFTH is a different class, same key**: the 300 s per-symbol cooldown, `signals/entry_throttle.py:97-107` — it contradicts *"immediately becomes eligible again"* and needs one sentence from Rama.

## 🔒 THE SEQUENCING REVERSAL — the reason the card existed
**F6 IS A PREREQUISITE OF RULING 2, NOT A BENEFICIARY. 0 of F6's 7 costs retired.**
The `abs()` is **not lexically** on the gate path, but `held == 0` is the **sole** door to `_finalize_gtt_exit` (`orders/cnc_gtt_monitor.py:487`/`:501-510`) ⇒ F6 is why a delivery trade never leaves `OPEN`, and `trades` is the gate's **only reachable** source. Cost 3 (the symbol block) would retire **only** on broker truth — and broker truth is unreachable at the gate: `RiskEngine.__init__` takes **no adapter**, `signal_processor.py:26` says *"SP14 — Layer 5; no direct broker import"*, `positions()` is blind to delivery from T+1 and `holdings()` blind to intraday, so **neither alone covers both products**.

**🔴 `abs()` on a SIGNED broker quantity is a CLASS at SIX production sites** — `cnc_gtt_monitor:464` · `order_reconciler:2185/2291/2968/3120` · `eod_squareoff:1079/1487/1525/1613` · `kill_switch:1281` · `structure_exit_manager:631`. Harmless where the intraday net reaches 0; wrong wherever a completed CNC SELL survives as a negative row. ⭐ A broker-truth predicate written in the house style would reproduce F6 at a new site on day one.

## The two numbers to carry
- **H6 — 9 entries would now be permitted**, on 2 days across 4 symbols (65 rejections = 56 still-reject + 9). ⭐ **But the number that matters is 11:** 05-Aug 8+3 and 06-Aug 5+6 both reach **11** against `max_daily_trades = 10`. ⚠️ Lower bound — 7 of the 56 are blocked by a trade with `exit_time IS NULL` (`DIFFNKG`, `MANINFRA`), so F6 contaminates the denominator in the defect's own direction.
- **H7 — no DAILY cap has bound since 10-Jul.** `REJECTED_DAILY_TRADES` 5,146, **all of it 09–10 Jul**; peak since is **9** vs cap 10. What still fires is **concurrency** (`max_open_positions` 500, per-strategy 302) — ⭐ **and a same-day re-entry does not consume a concurrency slot, because the exit released it.** `daily_loss_limit_pct` has never rejected anything.

⚠️ **(P) The gate-1 switchover is a clean edge:** `REJECTED_DUPLICATE_SYMBOL` 107, **last 31-Jul**; `REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT` 65, **first 03-Aug** ⇒ measuring the symbol block under the old code after 03-Aug reads **ZERO**.

Related: [[f6-delivery-exit-abs-defect-06aug]] · [[schema-product-is-on-orders-05aug]] · [[counts-db-rows-not-broker-06aug]] · [[paper-cannot-exercise-class-26jul]]
