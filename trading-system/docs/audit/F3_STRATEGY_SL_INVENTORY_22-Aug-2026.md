# FIX-F3 · STRATEGY SL CONFIGURATION — INVENTORY

**22-Aug-2026 (Saturday), IST.** Card: TRACKER + F2/F3 VERIFICATION, issued 12:05.
**Governed by:** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).

🏷️ **STATUS: `VERIFIED COMPLETE · ⛔ NOTHING CHANGED · ⛔ NO CODE WRITTEN`.**
**Measured at `45683859a0a05f466189ac5bc98f9a9f089f98d3`** by parsing all 16 YAMLs, ⛔ not by reading a summary. Line numbers hold only there (`M3`). Register row **`N22-07`**.

---

## §1 — THE ASK, AND THE ANSWER

**Rama's ask:** *every `strategy.yaml` owns its SL%, default 1%.*

# ✅ ALREADY SATISFIED — ⛔ CHANGE NOTHING.

**(P) all 16 strategy YAMLs carry `sl_method`, `sl_pct`, `sl_min_pct`, `sl_max_pct`, `sl_atr_multiplier` and `tgt_risk_reward` EXPLICITLY. Zero absent. Zero implicit. Zero inherited.**

⭐ **And the "default 1%" is never reached, by construction — which is a stronger result than it being merely unused:**
`strategies/schema.py:86` declares `sl_pct: float = 0.0`, and the model validator at `:303-306` **rejects `sl_pct <= 0` when `sl_method == "FIXED_PCT"`**, then at `:308-310` requires `sl_min_pct <= sl_pct <= sl_max_pct`. `sl_method` itself (`:85`) has **no default at all** and is required.
⇒ **A strategy that omitted its SL would fail to load, ⛔ not silently take 1%.** ⭐ There is no 1% default anywhere on the live path. The only literal `sl_pct = 0.01` default in the tree is `v3_chain/forward_shadow.py:77`, in the shadow recorder — ⛔ not in sizing or order placement.

---

## §2 — THE PROOF TABLE — all 16, as measured

| strategy | intent | direction | enabled | sl_method | sl_pct | sl_min | sl_max | ATR mult | explicit? | source / locked decision |
|---|---|---|---|---|---|---|---|---|---|---|
| `first_pullback_long` | INTRADAY | LONG | ✅ | `FIXED_PCT` | **0.015** | 0.003 | 0.05 | 1.5 | ✅ all 6 | widest intraday — the card's *"first_pullback is wider"* ✅ **CONFIRMED** |
| `first_pullback_short` | INTRADAY | SHORT | ✅ | `FIXED_PCT` | **0.015** | 0.003 | 0.05 | 1.5 | ✅ all 6 | as above |
| `gap_fade_long` | INTRADAY | LONG | ✅ | `FIXED_PCT` | 0.010 | 0.003 | 0.05 | 1.5 | ✅ all 6 | modal intraday value |
| `gap_fade_short` | INTRADAY | SHORT | ✅ | `FIXED_PCT` | 0.010 | 0.003 | 0.05 | 1.5 | ✅ all 6 | modal intraday value |
| `gap_go_long` | INTRADAY | LONG | ✅ | `FIXED_PCT` | **0.012** | 0.003 | 0.05 | 1.5 | ✅ all 6 | its own value, between the modal and first_pullback |
| `gap_go_short` | INTRADAY | SHORT | ✅ | `FIXED_PCT` | **0.012** | 0.003 | 0.05 | 1.5 | ✅ all 6 | as above |
| `open_high_breakdown_short` | INTRADAY | SHORT | ✅ | `FIXED_PCT` | 0.010 | 0.003 | 0.05 | 1.5 | ✅ all 6 | modal intraday value |
| `open_low_breakout_long` | INTRADAY | LONG | ✅ | `FIXED_PCT` | 0.010 | 0.003 | 0.05 | 1.5 | ✅ all 6 | modal intraday value |
| `pb01_breakout_retest` | INTRADAY | LONG | ⛔ **false** | `FIXED_PCT` | 0.010 | 0.003 | 0.05 | 1.5 | ✅ all 6 | ⚠️ **disabled** — still fully configured |
| `positional_momentum_long` | **DELIVERY** | LONG | ✅ | `FIXED_PCT` | **0.020** | 0.005 | 0.08 | 2.0 | ✅ all 6 | 🔴 locked decision `S6` says `ATR` — **contradicted**, see §3 |
| `positional_sector_rotation` | **DELIVERY** | LONG | ✅ | `FIXED_PCT` | **0.020** | 0.005 | 0.08 | 2.0 | ✅ all 6 | 🔴 as above |
| `positional_swing_long` | **DELIVERY** | LONG | ✅ | `FIXED_PCT` | **0.020** | 0.005 | 0.08 | 2.0 | ✅ all 6 | 🔴 as above |
| `range_breakout_long` | INTRADAY | LONG | ✅ | `FIXED_PCT` | 0.010 | 0.003 | 0.05 | 1.5 | ✅ all 6 | modal intraday value |
| `range_breakout_short` | INTRADAY | SHORT | ✅ | `FIXED_PCT` | 0.010 | 0.003 | 0.05 | 1.5 | ✅ all 6 | modal intraday value |
| `vwap_bounce_long` | INTRADAY | LONG | ✅ | `FIXED_PCT` | **0.008** | 0.003 | 0.05 | 1.5 | ✅ all 6 | tightest — the card's *"VWAP ones are tighter"* ✅ **CONFIRMED** |
| `vwap_rejection_short` | INTRADAY | SHORT | ✅ | `FIXED_PCT` | **0.008** | 0.003 | 0.05 | 1.5 | ✅ all 6 | as above |

**Distribution:** `0.008` ×2 · `0.010` ×6 · `0.012` ×2 · `0.015` ×2 · `0.020` ×3 (positional) — and one of the `0.010` is the disabled `pb01`.
**Bands:** intraday `[0.003, 0.05]` on all 13; positional `[0.005, 0.08]` on all 3 — **the positional band is deliberately wider on both ends**, which is the *"wider moves"* intent surviving in the one place it still binds.

⭐ **THE DIFFERENCES ARE DELIBERATE AND ARE PRESERVED. ⛔ NOTHING WAS FLATTENED TO 1%.** Two of the card's three characterisations are confirmed by measurement; the third is refuted in §3.

---

## §3 — 🔴 THREE DIVERGENCES FOUND. ⛔ EACH NAMED, ⛔ NONE FIXED.

### ⛔ D-1 · **`sl_method` is `FIXED_PCT` on ALL SIXTEEN. Not one strategy uses ATR.**

This **refutes the card's premise** *"positional strategies use ATR"*. The three positional strategies are `sl_method: FIXED_PCT`, `sl_pct: 0.020`. What they *do* carry is `sl_atr_multiplier: 2.0` (vs 1.5 intraday) and `tgt_atr_multiplier: 3.0` (vs 2.5) — **the ATR *multipliers* shipped; the ATR *methods* did not.** That is almost certainly where the belief came from.

### ⛔ D-2 · **ATR IS NOT IMPLEMENTED. Declaring it would change nothing except add a WARNING.**

- `signals/signal_processor.py:1633-1634` — `sl_method = strategy.sl_method` … `if sl_method == "ATR":` → falls back to `FIXED_PCT`. The module's own docstring (`:41`) says *"Does not implement ATR-based stop-loss (uses FIXED_PCT fallback)"*, and `SP8` records *"sl_price via FIXED_PCT; ATR = WARNING + fallback"*.
- `orders/shadow_tracker.py:826-827` — `if sl_method == "ATR": sl_method = "FIXED_PCT"  # ATR not implemented; fallback`.
- `strategies/schema.py:197-202` — the field validator **accepts** `"ATR"` as a legal value.

⇒ 🔴 **The schema accepts a value the engine cannot honour, and the engine degrades silently-but-warned rather than refusing.** ⚠️ Same class as the defect `FIX-F1` just removed: a configuration surface that looks live and is not. ⭐ Here the direction is safer (it warns, and every strategy already declares the implemented method) — but the trap is laid for whoever acts on `S6`.

### ⛔ D-3 · **A LOCKED DECISION THE SHIPPED CONFIG CONTRADICTS.**

`docs/locked_decisions.yaml` **`S6` — "Positional strategy differences from intraday"** states, verbatim:

> *"3 positional strategies differ from intraday defaults: `intent: DELIVERY` · `order_protocol: LIMIT_TRIPLE` (CO not available for CNC) · **`sl_method: ATR, sl_atr_multiplier: 2.0`** · **`tgt_method: ATR, tgt_atr_multiplier: 3.0`** · `smart_tgt_enabled: false` · `pullback_wait_enabled: false` · `entry_end_time: 14:30`"*
> rationale: *"Positional trades use CNC (no CO), **ATR-based risk (wider moves)**, longer entry window."*
> affects: `config/strategies/positional_*.yaml`

**Measured against the shipped files:**

| `S6` clause | shipped | |
|---|---|---|
| `intent: DELIVERY` | `DELIVERY` ×3 | ✅ |
| `order_protocol: LIMIT_TRIPLE` | `LIMIT_TRIPLE` ×3 (intraday: `CO_PLUS_TGT` ×13) | ✅ |
| `sl_atr_multiplier: 2.0` | `2.0` ×3 | ✅ |
| `tgt_atr_multiplier: 3.0` | `3.0` ×3 | ✅ |
| **`sl_method: ATR`** | **`FIXED_PCT` ×3** | 🔴 **CONTRADICTED** |
| **`tgt_method: ATR`** | **`RISK_REWARD` ×3** (all 16 are `RISK_REWARD`) | 🔴 **CONTRADICTED** |

⇒ **`S6` is honoured on the four clauses that decide nothing, and contradicted on the two that decide behaviour.**

🔴 **AND ADOPTING `S6` LITERALLY WOULD BE WORSE THAN LEAVING IT — MEASURED BY EXPERIMENT, ⛔ not reasoned.** Three `StrategyConfig` constructions against the real schema:

| variant | result |
|---|---|
| **(a)** `sl_method: ATR` with `sl_pct` **dropped** (the natural reading of `S6` — an ATR strategy has no fixed pct) | ⚠️ **LOADS CLEANLY**, `sl_pct = 0.0`. The `sl_pct > 0` validator only guards the `FIXED_PCT` branch, so it never runs |
| **(b)** `sl_method: ATR` with `sl_pct: 0.02` **retained** | LOADS, `sl_pct = 0.02` — and behaves **identically to today**, because the runtime falls back to `FIXED_PCT` and uses that same 0.02 |
| **(c)** the shipped file, as a control | LOADS, `FIXED_PCT` / `0.02` |

⇒ 🔴 **variant (a) loads and is silently un-tradeable.** At runtime the ATR fallback (`D-2`) selects `FIXED_PCT` with `sl_pct = 0.0` ⇒ `sl_distance = entry × 0.0 = 0` ⇒ `position_sizer.py:354` trips `sl_distance < min_tick_size` ⇒ **`INVALID_SL_DISTANCE` on every positional signal**, logged CRITICAL, no order placed. **A config that boots green and rejects every delivery trade.** ⭐ Variant (b) is inert. ⇒ **`S6` is not merely unimplemented — the obvious way to implement it is a live outage of the delivery book.**

⭐ **CONSEQUENCE, and it is the point of writing this down: `sl_atr_multiplier` and `tgt_atr_multiplier` are DEAD KEYS on all 16 files.** A wide sweep (`grep -rn sl_atr_multiplier` across every `.py` and `.yaml`) returns exactly: the 16 YAMLs, `strategies/schema.py:87` (declaration) and `:222` (a range validator), `docs/locked_decisions.yaml`, and 5 test references. **⛔ Zero production read sites.** They are validated and never consulted — the *"configured, built, started, yet INERT"* class `N20-48` named, now at its sixth instance.

---

## §4 — THE SEPARATION, PRESERVED AND RESTATED

⭐ **THE STRATEGY OWNS THE STOP DISTANCE AND METHOD. RISK POLICY OWNS THE PER-TRADE RUPEE BUDGET.** They are different quantities and they multiply, they do not substitute:

```
strategy:      sl_pct        → sl_distance = entry × sl_pct          (WHERE the stop sits)
risk policy:   risk_per_trade_pct → risk_rs = base × pct             (HOW MUCH may be lost)
sizer:         qty_by_risk = floor(risk_rs / sl_distance)            (position_sizer.py:381-382)
```

⛔ **`risk_per_trade_pct` is NOT a "global SL" and must never be described as one.** It never sets a stop price; it divides by one. This is the distinction `docs/PRE_BUILD_REVIEW_GATE.md` was created over — the gate's own founding instance was a card that specified `risk_per_trade_pct` at 1% without first establishing who owned that number.

⛔ **Per-strategy risk BUDGETS are a separate policy decision and are NOT smuggled in here.** Nothing in this inventory proposes one. ⚠️ Note that `FIX-F2` would give the budget a per-**book** base — ⛔ that is per-book, ⛔ not per-strategy, and the two must not be conflated.

---

## §5 — WHAT THIS INVENTORY DOES **NOT** CLAIM

- ⛔ No claim that the shipped `sl_pct` values are *correct* — only that they are **explicit, owned by their strategy, inside their own bands, and deliberately different**. Whether `0.008` is right for VWAP is a trading question, ⛔ not a configuration one.
- ⛔ No claim about `pb01_breakout_retest` beyond `enabled: false`. It is fully configured and would load; it simply does not trade.
- ⛔ No claim that `S6` should be changed. **Naming a divergence is not proposing a direction** — either the config or the locked decision is wrong, and which one is Rama's call.
- ⛔ Nothing was edited. No strategy YAML, no schema, no locked decision.

---

## §6 — VERDICT

# ✅ **VERIFIED COMPLETE — ⛔ CHANGE NOTHING**

Every strategy owns its SL explicitly; the schema makes an implicit SL impossible; the deliberate differences are intact; no 1% default is reachable on the live path.

**Three things owed to Rama, ⛔ none of them a code change:**

1. **`D-3` — `S6` vs the shipped config.** Which is authoritative? ⛔ Do not "fix" the config to match a locked decision the engine cannot execute.
2. **`D-2` — ATR is accepted by the schema and unimplemented in the engine.** Either implement it, or narrow the schema to reject it. ⚠️ Leaving it accepted is the trap.
3. **`D-1` — the premise *"positional strategies use ATR"* is false** and should not be carried into another card.

# ⛔ STOP. Nothing changed.
