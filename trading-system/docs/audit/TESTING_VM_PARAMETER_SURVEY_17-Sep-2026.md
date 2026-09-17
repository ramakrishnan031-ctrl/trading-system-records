# Testing-VM parameter survey — 17-Sep-2026 (READ-ONLY · nothing was changed)

> ⚠️ **THE S&R SHADOW MEASUREMENT POPULATION SPLITS.** 17-Sep is day 1 of the shadow under today's parameters; from the 18-Sep boot the testing VM would run a different set — and the trading-window change alters which signals the shadow **captures at all** (its capture sits after the entry-window gate), so day 1 and day 2+ are not comparable and cannot be pooled. ⛔ Stated, not decided — **Rama's call.**

**Request (👤 Rama, relayed by the 17-Sep card "NEW TASK FROM RAMA · THREE TESTING-VM PARAMETERS"):** testing VM only — (1) market open / trading start 10:00 → 09:30 · (2) concentration 10% → 50% · (3) maximum Qty → 1.
**This pass:** step 1 of 2 — read-only survey, 12:29–12:4x IST. ⛔ No config edited (VM or repo) · ⛔ no push · ⛔ no restart · ⛔ no registry change · ⛔ production not contacted.
**Execution metadata:** ran on `claude-opus-5[1m]` (Opus 5, 1M context), effort `max` — ⛔ not the card's requested Sonnet 4.6 · Medium.

**Evidence basis.**
- **Config values** are quoted from the testing VM's own `config/system_config.yaml` (read 12:30, 56,846 B, md5 `4eab1ae5a9716059431b55a210e917c9`). Of the VM's 31 config files, **29 are byte-identical** to the `e7bf477` blobs (all 16 strategy YAMLs among them); `system_config.yaml` and `cron_registry.yaml` are VM-local copies.
- **Code** is cited at `e7bf477` line numbers. On the VM (md5, 12:35:18) **10 of the 11 cited modules are byte-identical** to their `e7bf477` blobs; `signals/webhook_receiver.py` differs by **CRLF only** (1,207 CR bytes; `diff --strip-trailing-cr` = 0 lines) — a **4th** CRLF-only file on the twin, alongside the three recorded this morning.
- **Production** values are from **git at `970aabf`** — the commit production's files were pushed at on 👤 Rama's word (12-Sep). ⛔ **The production VM itself was NOT read:** the standing rule is *"PRODUCTION = EXPLICIT APPROVAL, EVERY TIME (👤 Rama, 16-Sep)"*. A production VM-local edit would therefore not be visible here. **A direct read-only production read needs your word.**

---

## Summary

| Rama's words | The real key(s) — all in `config/system_config.yaml` | Testing VM now | Production @`970aabf` (git) | Config-only change? |
|---|---|---|---|---|
| market open / trading start 10:00 → 09:30 | `trading_hours.entry_start` | `"10:00"` | `"10:00"` | ✅ valid; takes effect at the next boot |
| concentration 10% → 50% | `position_sizing.max_concentration_pct` (INTRADAY book) · `position_sizing.delivery_max_concentration_pct` (DELIVERY book) — **two keys** | `0.10` · `0.10` | `0.10` · `0.10` | ✅ valid — ⚠️ **but the 40% position-value cap turns HIGH-tier sizes into CRITICAL rejections** (§2 f) |
| maximum Qty → 1 | ⛔ **no key caps an order at 1 share** — the eight candidates are in §3 | — | — | ⛔ **not as "1 share per order"** without a code change |

---

## 1 · "Market open / trading start" 10:00 → 09:30

**a · Key and value.** `trading_hours.entry_start: "10:00"` (VM L28): *"[LAUNCH-PHASE] Live Week 1: conservative start; avoid opening-hour volatility. Relax toward 09:20 as the account scales."* ⛔ It is **not** `trading_hours.market_open: "09:15"` (L103, *"NSE regular-session open"*). The config itself explains the 10:00 (L29–39): *"This value is a FLOOR OVER the per-strategy windows … while this says 10:00, the 16 strategies declaring entry_start_time "09:25" cannot trade at 09:25 — the floor binds … Relaxing THIS line is the switch; the strategies already say what they want."*

**b · Where it lives.** The VM's `system_config.yaml` is a **VM-local copy** of a repo-tracked file (md5 `4eab1ae5…` ≠ the `e7bf477` blob `cf3422b4…`; the differences are the `sr_shadow` block's position, comments and the sandbox e-mail addresses — ⛔ none on these keys). Editing it in place is the established pattern (the `sr_shadow` block was placed the same way, as a validated copy-back). ⚠️ A push to the twin's bare repo would overwrite it (`post-receive` does `checkout -f`) — pushes are barred during the measurement anyway.

**c · Readers.** Loaded once (`core/config_loader.py:38` *"load-once at startup"*) → `main.py:2328–2329` builds one `MarketWindows(entry_start=…)` → `core/market_windows.py:150` `entry_start <= t < entry_end`.
- **Enforcing:** `signals/webhook_receiver.py:582` (the webhook edge — an out-of-window webhook is refused) · `signals/signal_processor.py:950` + `:1016` (`_process_one`) · `:2096` + `:2131` (`continue_from_gate`) · `:2453` + `:2473` (`continue_from_retest`) — the second of each pair is `is_entry_allowed_for_strategy` (`market_windows.py:152–175`), which requires the global window AND the strategy's own `entry_start_time`/`entry_end_time` · `data/live_feed.py:749` (feed watchdog, active only inside the entry window).
- **Non-enforcing:** `core/config_auditor.py:164`, `:746` (audit) · `reports/daily_trade_review.py:1229` (report) · `ops_dashboard/…` (display; fallback `"10:00"` only if the key is absent).
- **Not this key:** `v3_chain/pb01_entry.py:107` reads `watchlist.entry_start` (`"09:20"`, VM L622, PB-01 stage) · `sr_shadow/calendar.py:38` builds its own `MarketWindows` with defaults (trading-day calendar only) · `strategies/schema.py:137` defaults `entry_start_time` to `"10:00"` only for a strategy that omits it — all 16 declare `"09:25"`.

**d · When it takes effect, and the schema.** At the **next boot** (18-Sep 08:15) — ⛔ no hot reload. The schema requires `market_open <= entry_start < entry_end <= eod_entry_cutoff <= …` (`config_loader.py:144`, `:163–173`): `09:15 <= 09:30 < 15:00` ✅ **valid.** Effective start for every strategy = the later of the two windows = **09:30** (the strategies' 09:25 is still below the floor). The boot auditor's `G5` warns only when a strategy window has NO overlap with the global one — 09:25–15:00 vs 09:30–15:00 overlaps ⇒ no finding.

**e · Modes.** The testing VM boots `mode=LIVE account=VBB097`. The gates carry **no paper/live condition** (no mode term within ±8 lines of any gate site or of the `MarketWindows` construction; control: the known `is_paper` block at `main.py:2839` reads 4) ⇒ paper and live pass through the same gates. ⚠️ **S&R shadow: AFFECTED** — the shadow's capture is at `signal_processor.py:1153`, after both entry-window gates (`:950`, `:1016`), and the webhook edge refuses out-of-window signals at `:582` ⇒ **09:30–10:00 signals would enter the shadow's capture population from 18-Sep.**

**f · Keys that move with it — named, ⛔ not changed.**
- the 16 strategies' `entry_start_time: "09:25"` — ⛔ do NOT align them to 09:30 (config L34–39: they are the intended windows; the global line is the switch);
- `trading_hours.entry_end: "15:00"`, `eod_entry_cutoff: "15:15"` — unchanged, unaffected;
- the `gap_*` strategies' `sl_gap_buffer_pct: 0.3` (*"widen SL 0.3% during 09:15-09:30 gap-risk window"*) — a 09:30 start sits at that window's edge;
- `watchlist.entry_start: "09:20"` — a separate PB-01 key, ⛔ not this one;
- ⛔ **not examined:** the Chartink scanners' own schedules — whether they fire between 09:30 and 10:00 at all.

**Production @`970aabf`:** `"10:00"`; the 16 strategy YAMLs are byte-identical to `e7bf477`; `core/market_windows.py` identical. ⇒ this change creates a deliberate testing-VM ↔ production divergence.

---

## 2 · "Concentration" 10% → 50%

**a · Keys and values — TWO books, TWO keys, NO inheritance.**
- `position_sizing.max_concentration_pct: 0.10` (VM L226) — *"max 10% of total capital in one symbol (PS2)"* — sizes **INTRADAY** entries (MIS / CO / BO).
- `position_sizing.delivery_max_concentration_pct: 0.10` (VM L254) — *"= global max_concentration_pct today"* — sizes **DELIVERY** (CNC) entries.
- `capital/position_sizer.py:374–384`: a positional entry reads ONLY the delivery key, an intraday entry ONLY the global one. ⚠️ **"Concentration" names one number; the code has two — which book(s) is for 👤 Rama.**

**b · Where it lives.** The same VM-local `system_config.yaml` (§1 b).

**c · Readers.** `main.py:2852` / `:2869` → `PositionSizer` (constructed ONCE, `main.py:2848`) → `position_sizer.py:498–500` `qty_by_concentration = floor(total_capital × conc / entry_price)` → `:503` `raw_qty = min(qty_by_risk, qty_by_capital, qty_by_concentration)`. Audit: `config_auditor.py:453–511` (C2, C2d, C4). Display: `ops_dashboard/…`. Startup-only (load-once).

**d · When, and the schema.** Next boot. Schema `0 < v <= 1` (`config_loader.py:522–526`; the delivery key `(0, 1]` and non-null, `:501–513`) ⇒ `0.50` ✅ **valid.** ⚠️ The boot auditor raises **`C2` WARN** (and `C2d` if the delivery key moves too): `max_position_value_pct 0.40` ≤ `0.50 × max effective multiplier 2.0` (`config_auditor.py:453–466`, `_max_effective_multiplier` `:401–413`). **Non-blocking** — the boot hard-stops only on the A4/A5 findings (`main.py:3444–3451`, `:3466–3473`, exit 3).

**e · Modes.** One `PositionSizer` for paper and live — `main.py`'s `is_paper` block (`:2839–2845`) only re-syncs paper capital, not sizing. **S&R shadow: capture rows NOT affected** — the capture precedes sizing and admission (`signal_processor.py:1147–1159`, then `self._sizer.calculate` at `:1165`; comment: *"capacity/throttle/daily-gate/risk refusals never remove a row (addendum R6)"*). What changes is which captured signals become trades.

**f · ⚠️ THE KEY THAT DECIDES WHAT 50% ACTUALLY DOES — named, ⛔ not changed.**
- **`position_sizing.max_position_value_pct: 0.40`** (L236) and **`delivery_max_position_value_pct: 0.40`** (L259) are a **REJECT, not a clamp**, with a **CRITICAL** log `position_sizer.position_value_cap_exceeded` (`position_sizer.py:707–750`).
- The size is `raw_qty × multiplier` (`:602–605`); the multiplier today is the tier weight alone — `perf_weight` is unwired (`config_auditor.py:449–451`) ⇒ **HIGH 1.0 · MEDIUM 0.70 · LOW 0.50.**
- ⇒ **With concentration 0.50 and the value cap left at 0.40, wherever concentration is the binding rung:** HIGH-tier size ≈ 50% of capital > 40% ⇒ **REJECTED + a CRITICAL per signal** · MEDIUM ≈ 35% ⇒ trades at **3.5×** today's size · LOW ≈ 25% ⇒ **2.5×**. The best-scored signals become CRITICAL rejections, and those CRITICAL lines land in the application log — the population the shadow deployment's E4.10 check reads.
- **`risk_per_trade_pct: 0.01`** (L225): the risk rung binds when the SL distance exceeds `risk ÷ concentration` of the price — **> 10% today, > 2% at 0.50** (from `:456–457` and `:498–500`) ⇒ many more trades become risk-bound, not concentration-bound.
- `capital.intraday_bucket_pct: 0.70` × `leverage_map.INTRADAY: 5.0` ⇒ at full availability the capital rung is ≈ 3.5 × total ÷ price — it binds before concentration only once the bucket is partly reserved.
- `risk.max_open_positions: 5` · `risk.max_sector_exposure_pct: 0.40` with `sector_cap_mode: observe` (logs, does not reject) · `max_portfolio_deployment_pct: null` (inert).

**Production @`970aabf`:** `0.10` / `0.10`; `position_sizer.py`, `risk_engine.py` byte-identical to `e7bf477`.

---

## 3 · "Maximum Qty" → 1 — ⛔ AMBIGUOUS · every candidate that exists · ⛔ none picked

| # | Key (file: `system_config.yaml` unless stated) | Testing VM · production @`970aabf` | What it limits | What setting it to 1 would do |
|---|---|---|---|---|
| 1 | `position_sizing.max_single_order_qty` (L230) | `10000` · `10000` | the **quantity of one order** — the ONLY per-order qty key | ⛔ **NOTHING TODAY — INERT:** `main.py:2848–2870`, the only production construction site, never passes it, so the sizer runs on its default `10000` (`position_sizer.py:165`); same at `970aabf` (0 mentions in `main.py`). ⚠️ **And even if wired it REJECTS, it does not clamp:** `qty_by_risk > cap` (`:461–487`) or `final_qty > cap` (`:656–684`) ⇒ `QTY_EXPLOSION_GUARD` + a **CRITICAL** per signal ⇒ a value of 1 would reject nearly every signal. Schema: bare `int`, no validator. |
| 2 | `risk.max_open_positions` (L271) | `5` · `5` | **concurrent open positions**, portfolio-wide | one open position at a time, of ANY size — `risk_engine.py:610` rejects when the effective count would exceed the cap. Schema `>= 1` (`config_loader.py:824–829`) ✅ |
| 3 | `risk.max_open_delivery_positions` (L283) | `3` · `3` | concurrent open **DELIVERY** positions | one open CNC position — `risk_engine.py:565` (`>=`). Schema non-null `>= 1` |
| 4 | `max_concurrent_positions` in each of the 16 `config/strategies/*.yaml` (repo-managed; byte-identical on the VM) | `2` or `3` · same | open positions **per strategy** | one per strategy — `signal_processor.py:783–812` (open + reserved + pending, +1 for the candidate) |
| 5 | `risk.max_daily_trades` (L272) · `risk.max_daily_delivery_trades` (L284) | `10` · `5` (both machines) | **entries per day** | one entry per day (per book) |
| 6 | `risk.one_trade_per_symbol_direction_per_day` (L302) | `true` · `true` | one completed trade per symbol + direction per day | already on |
| 7 | `position_sizing.min_qty_threshold` (L227) | `1` · `1` | a **FLOOR** — rejects a size below it | ⛔ not a cap |
| 8 | `position_sizing.enabled` (L220) + `flat_value_rs` (commented, L223) | `true` · unset | flat ₹ per order when `enabled: false` | a **₹ ceiling**, not a share count: `qty = floor(flat_value_rs ÷ price)` (`position_sizer.py:625–626`) — 1 share only for prices in `[flat, 2×flat)` |

⇒ **PLAINLY: on this code no config key caps an order at 1 share.** The only per-order quantity key is unwired AND rejects; every other candidate caps POSITIONS or TRADES, not quantity.

⇒ **The pairing "concentration 50% + qty 1"** reads as *exercise the concentration path at near-zero exposure*. **None of the existing keys achieves that as configured:** candidates 2–6 reduce the number of positions or trades but not the size of each — with concentration 0.50, a single position could approach 40–50% of capital (HIGH tier rejected above 40%), the opposite of near-zero exposure. Only candidate 1 aims at quantity, and it would need a code change to be wired AND to clamp rather than reject — ⛔ outside this card, and sizing design this card does not open. 💭 With a genuine 1-share cap, concentration would decide only **affordability**: a stock is sizeable iff its price ≤ `concentration × total capital`, and the 40% value cap would still reject any single share priced above 40% of capital.

**Modes (all candidates):** `PositionSizer`, `RiskEngine` and the strategy position cap are shared by paper and live. **S&R shadow capture rows: not affected** (capture precedes sizing and admission, §2 e).

---

## Timing, and what this pass did not do

- ✅ **All three take effect only at a boot** (`config_loader.py:38`, load-once). It is already past both 09:30 and 10:00 today ⇒ nothing could take effect before **18-Sep 08:15** in any case. Applying tonight, after the measurement sequence closes, loses nothing.
- ⛔ **Applying today would have cost:** the day's resolved config hash (Gate 7/8 evidence) · a second **"Config Changed Since Last Session"** WARN Telegram (`main.py:2664–2683`) — an unpredicted event in today's full-day rows · a mixed-parameter first shadow session for Gate 9 · non-homogeneous rows for today's E-6 · and a restart ending the boot-to-`Shutdown complete` continuity every row tonight depends on.
- ⚠️ **For 18-Sep's own checks:** the change will itself trigger that WARN Telegram at the 18-Sep boot (config hash changed), and — if concentration moves while the 40% value cap does not — new **CRITICAL** families (`position_value_cap_exceeded`) in the application log. Record the change BEFORE the boot so 18-Sep's CRITICALs can be attributed to it and not to the S&R deployment.
- ⛔ Nothing edited · nothing pushed · nothing restarted · the registry untouched · ⛔ no slippage / P / B / FIX-075 / flat-tier work · tonight's frozen sequence untouched.

## Owed to 👤 Rama before the change card
1. **The shadow-population split** — accept a day-1 / day-2+ break, or defer the change until the measurement ends.
2. **Concentration — which book:** intraday (`max_concentration_pct`), delivery (`delivery_max_concentration_pct`), or both — and **whether `max_position_value_pct` (40%) moves with it**; if it stays, HIGH-tier signals where concentration binds are rejected with a CRITICAL each.
3. **"Maximum Qty" — which meaning:** a 1-share order (no config key exists; needs a code change) · or one of candidates 2–6 (positions or trades, not quantity).
4. **Optional:** a direct read-only production read of these values (the standing rule needs your word each time).
