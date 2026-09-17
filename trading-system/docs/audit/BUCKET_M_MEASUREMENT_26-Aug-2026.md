# BUCKET M — FULL READ-ONLY MEASUREMENT SWEEP · 26-Aug-2026 · at `75e637c`

**Scope: M1–M14, read-only.** ⛔ Zero code changes, zero config changes, zero schema changes, zero DB writes. Every DB read used `file:…?mode=ro`. The **one** permitted content write was the Q-3 correction to `PATHS.md` (M3c).

**Anti-duplication check (mandatory):** searched `docs/audit/` (**297 files**) for `sweep|inventory|measure|bucket|F11|F14|M[0-9]` and for `26-Aug`. Found related-but-distinct records (`capital_figure_sweep_28jul2026.md`, `F2_SEGMENT_CAPITAL_INVENTORY_22-Aug-2026.md`, `MEMORY_TRUNCATION_INVENTORY_25-Aug-2026.md`, …) and one 26-Aug file — `BOOT_PROOF_75e637c_26-Aug-2026.md`, which is FILE 1's boot proof and serves a different purpose. **No existing Bucket-M / F11-F14 sweep record exists**, so this is a new file rather than a duplicate.

## §0 — SESSION START

**S1.** `UNPUSHED_PENDING_DEPLOY_LEDGER.md` — 1,403,449 B / 4,010 lines. ⚠️ Read **structurally, not line-by-line** (frontmatter, the four structured sections, the two-clock block, and exhaustive search on F6/EOD/`75e637c`/the five unit SHAs). Stated plainly rather than claimed as an end-to-end read.

**S2.** `git ls-remote origin refs/heads/main` → `75e637c300c1bead4aad3cf549e6dbe9318c6b1f`; VM bare `rev-parse --short HEAD` → `75e637c`. ✅ Expected value. No STOP.

**S3.** Market **OPEN**. `date` on VM = `Wed Aug 26 10:31:24 IST 2026`. Service `active/running`, PID `402677`, `NRestarts=0`, kill switch `INACTIVE`, **3** open trades at that moment (down from 4 at FILE 1 — one closed intraday). All DB access read-only throughout.

---

## M1 — OWED-1: 25-Aug entries, fills, realised P&L

**Answer to the UNKNOWN: YES — 25-Aug took and closed five intraday trades.**

**(a)** `SELECT t.trade_id,t.symbol,t.strategy,t.direction,o.product,t.qty_filled,t.entry_time,t.exit_time,t.entry_actual_price,t.exit_price,t.exit_reason,t.status FROM trades t LEFT JOIN orders o ON o.trade_id=t.trade_id AND o.leg='ENTRY' WHERE date(t.entry_time)='2026-08-25' OR date(t.exit_time)='2026-08-25' OR date(t.created_at)='2026-08-25';` → **19 rows**; 5 filled+closed, 14 `FAILED`.

| symbol | strategy | product | qty | entry | exit | in | out | reason |
|---|---|---|---|---|---|---|---|---|
| FACT | first_pullback_long | MIS | 1 | 10:01:49 | 10:36:50 | 890.30 | 876.80 | SL_HIT |
| RCF | first_pullback_long | MIS | 4 | 10:06:13 | 14:15:14 | 126.82 | 124.85 | SL_HIT |
| FMGOETZE | gap_go_long | MIS | 1 | 10:06:16 | 10:43:39 | 539.45 | 533.00 | SL_HIT |
| TEXRAIL | vwap_bounce_long | MIS | 4 | 10:09:25 | 10:32:16 | 109.01 | 108.13 | SL_HIT |
| GROWW | first_pullback_long | MIS | 2 | 12:33:28 | 15:17:14 | 204.14 | 203.06 | MANUAL |

**(b)** `SELECT COUNT(*),SUM(gross_pnl),SUM(net_pnl),SUM(charges) FROM trades WHERE date(exit_time)='2026-08-25';` → **n=5, gross −33.51, net −36.42, charges 2.91.** Five losses, no winners.

**(c)** `SELECT product,leg,status,COUNT(*) FROM orders WHERE date(placed_at)='2026-08-25' GROUP BY …` → **CANCELLED 19 / COMPLETE 10.** Breakdown: **CNC ENTRY CANCELLED 10** (⚠️ *all ten CNC entries that day failed*) · MIS ENTRY COMPLETE 5 · MIS TGT CANCELLED 5 · MIS SL COMPLETE 4 · MIS ENTRY CANCELLED 3 · MIS EOD COMPLETE 1 · MIS SL CANCELLED 1.

**(d)** 25-Aug signals = **3,809**. Top statuses: `REJECTED_SCORE_57` 1,729 · `REJECTED_SCORE_59` 605 · `REJECTED_CIRCUIT_PROXIMITY` 176 · **`PROCESSED` 18** · `REJECTED_ENTRY_THROTTLED` 18 · `REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT` 13 · `REJECTED_STRATEGY_POSITION_LIMIT` 9 · `PLACEMENT_FAILED` 1.

**(e) RECONCILIATION — it closes to ₹0.18.**

```
25-Aug 09:15  fund_manager.sync_from_broker  broker_cash = 10604.20
26-Aug 09:15  fund_manager.sync_from_broker  broker_cash = 10567.60
                                             observed delta = -36.60
25-Aug realised net P&L (trades)             = -36.42
                                 UNEXPLAINED = -0.18
```

✅ **(a) explains 10,604.20 → 10,567.60 to within ₹0.18.** 💭 **INFERENCE** (not measured): the ₹0.18 is most likely cost-attribution rounding. ⚠️ Noted, not chased.

⚠️ **One thing that does NOT reconcile and is recorded rather than smoothed:** `SELECT COUNT(*),SUM(pnl_delta) FROM fm_ledger WHERE date(ts)='2026-08-25'` → **82 rows, SUM = −2.66e-15 (i.e. exactly 0)**, while `trades.net_pnl` says −36.42. That is a genuine divergence between the two ledgers for the day. 📌 **Recorded, not investigated** — it borders DEFECT C (09:15 SYNC erasing realised P&L), which M15 places out of scope.

---

## M2 — Q-4 EXIT TIMESTAMP TIMEZONE · **VERDICT: `IST CONFIRMED`**

🔴 **The section's premise is inverted, and measurement settles it.**

**(a)** Column = **`trades.exit_time`**, `TEXT`, nullable. Stored values, read raw:

```
BALUFORGE   2026-08-24T12:47:50.154389+05:30   len=32  typeof=text
KAMATHOTEL  2026-08-24T11:31:29.719792+05:30   len=32  typeof=text
```

⇒ The stored values **already read 12:47:50 and 11:31:29 IST**, carrying an explicit `+05:30`. The `07:17:50` / `06:01:29` figures quoted in the brief are the **UTC renderings** of those same two instants (12:47:50 − 5:30, 11:31:29 − 5:30). ⛔ Nothing "precedes the IST market open".

**(b) The writer.** These two rows are `GTT_EXIT`, so the path is `mark_trade_closed_gtt` → `record_gtt_close_financials`:
* `core/state_store.py:2398` — `(exit_reason, _now_ist_iso(), trade_id)`
* `core/state_store.py:2419` — `ts = exit_time or _now_ist_iso()`; `:2425` — `exit_time = COALESCE(exit_time, ?)`
* `core/state_store.py:70-74` — `def _now_ist_iso(): return datetime.now(_IST).isoformat()`, with `_IST = timezone(timedelta(hours=5, minutes=30))` at `:67`.

⇒ **Named: `datetime.now(_IST).isoformat()`.** ⛔ Not `utcnow()`, ⛔ not a broker field.

**(c) Readers.** 16 non-test files reference `exit_time`. Day-bucketing consumers: `state_store.py:993` and `:3190` (`substr(COALESCE(exit_time, updated_at),1,10)`), `capital/performance_allocator.py:142` (`COUNT(DISTINCT DATE(exit_time))`), and the `ops_dashboard` readers (`exit_time LIKE ?` prefix matching, `julianday(exit_time)-julianday(entry_time)` at `db_reader.py:832`). All assume IST — and given the column IS IST, all are correct.

**(d) Entry vs exit — no inconsistency.** `SELECT substr(entry_time,-6), substr(exit_time,-6), COUNT(*) … GROUP BY 1,2` → **one row: `+05:30 | +05:30 | 295`.** ✅ All 295 trades with both timestamps agree.

**(e) Independent clock — agrees to ~1.5 ms.**

```
DB   KAMATHOTEL exit_time  2026-08-24T11:31:29.719792+05:30
LOG  {"ts":"2026-08-24T11:31:29.721+05:30",…,"logger":"cnc_gtt_monitor","msg":"cnc_gtt_monitor.gtt_exit",…,"reason":"GTT_EXIT"}
DB   BALUFORGE  exit_time  2026-08-24T12:47:50.154389+05:30
LOG  {"ts":"2026-08-24T12:47:50.156+05:30",…,"symbol":"BALUFORGE",…,"reason":"GTT_EXIT"}
```

**(f) BLAST RADIUS — the UTC hypothesis has none, but a REAL latent trap was found.**

The two day-bucketing idioms in the codebase **do** diverge — `DATE()` converts to UTC, `substr(…,1,10)` does not:

| value | `DATE()` | `substr(…,1,10)` |
|---|---|---|
| `2026-08-24T12:47:50+05:30` | `2026-08-24` | `2026-08-24` |
| `2026-08-24T05:29:00+05:30` | **`2026-08-23`** | `2026-08-24` |
| `2026-08-24T03:00:00+05:30` | **`2026-08-23`** | `2026-08-24` |

⇒ They disagree **only** for IST times before 05:30. Measured: **0** rows have `exit_time` before 05:30 IST, **0** have `entry_time` before 05:30 IST, and **0** rows where `DATE(exit_time) <> substr(exit_time,1,10)`. ✅ **LATENT, ⛔ not live** — market hours make the band unreachable today.

**(g) VERDICT: `IST CONFIRMED`.** ⛔ Nothing fixed. ⚠️ **DEFECT D's stated premise (P&L date bucketing wrong because the column is UTC) is NOT supported.** Whatever produced `07:17:50` did the conversion; the column did not.

---

## M3 — Q-3 · **there was no conflict; the defect was the METHOD**

**(a) Measured by reading `main.py` at `75e637c`:**

```
4037|     if _eod_exit_armed:
4038|         _start_eod_self_exit_thread(          <-- the CALL SITE
…
4051|             strategy_intent_fn=(              <-- Link 1, the kwarg
4052|                 lambda name: getattr(strategies.get(name), "intent", None)
4053|             ),
…
4059|         )                                     <-- the call closes
```
Link 2 — `main.py:1489`: `strategy_intent_fn=strategy_intent_fn,`

**(b)** ✅ **PROVEN by quoting the whole call:** `:4038` and `:4051` are **both correct and name different things** — the line that opens a 22-line call, and one kwarg inside it. The "13–14 line difference" is the kwarg's offset. **`PATHS.md:37` already drew this distinction correctly.**

🔴 **What WAS wrong:** `:4038` was obtained by **arithmetic** (`:4004 @02a2a6b` + a `+34` shift). It was right **by luck, not by method** — and M3's own rule forbids exactly that. 🔬 **The rule proved itself twice today:** the record places the FIX-133 clamp at `position_sizer.py:506`; measured, it is at **`:605`** (see M12e).

**(c)** ✅ `PATHS.md` corrected in place; superseded wording **retained and marked**, not deleted. Sizes in §15.
**(d)** ✅ Rule recorded in `mempalace.yaml` under `m3_the_standing_rule`.

---

## M4 — F6 A–F · PIPELINE LIFECYCLE

**(A) One process runs both books.** Entry point `main.py --mode live` (measured from `/proc/402677/cmdline`). MIS runs in `signal_processor`, `order_monitor`, `order_reconciler`, `entry_gate`, `smart_tgt`, `tgt_retry_manager` (all `.start()` at `main.py:3863-3880`), plus named threads `eod-pre-alert` (`:966`), `market-open-margin-sync` (`:1035`), `eod-self-exit` (`:1559`), `webhook` (`:3891`). 🔴 **The delivery/GTT path has NO thread of its own** — it is driven from *inside* the reconciler.

**(B/D) The GTT monitor's schedule, and what dies with the service.**
* `orders/order_reconciler.py:335` — `self._cnc_monitor_every = 60  # cycles between full monitor runs (15 min / 15s)`
* `:429-433` — a startup reconcile pass
* `:661` → `:663 _maybe_run_cnc_monitor` → `:678-683` — `self._cnc_gtt_monitor.reconcile(in_hours=True)` every 60 cycles × `poll_interval_sec: 15` = **every 15 minutes**
* 🔬 **`config/cron_registry.yaml` matches for `gtt|cnc|delivery` = 0**, across all **47** registry jobs.

⇒ **Stops when the service stops:** `_drain_preopen` (pre-open queue), `_gather`, `_handle_row` (the whole K6 ladder), `_recreate` (GTT re-placement), `_qty_mismatch`, `_reprotect`, `_safe_delete_gtt`, and **`_finalize_gtt_exit`** — plus every reconciler CHECK. Consequence: **a GTT that fires at the broker while the service is down is never RECORDED locally** (the trade stays `OPEN`), **and its capital is never released**.

**(C) Are broker-side GTT OCO orders sufficient?** ✅ **For PRICE protection, yes** — the two-leg OCO is `place_gtt`'d and rests at the broker (`cnc_gtt.placed` log lines carry `gtt_id`, `sl_trigger`, `tgt_trigger`). ⛔ **For everything else, no** — recreate-if-missing, qty-mismatch detection, orphan handling, local finalisation and capital release are all in-process (list above).

**(E) 🔴 NONE EXISTS — with a precise qualification.**
* `capital/kill_switch.py:483` — `def is_active(self, intent: str = "entry")`. The parameter is named `intent` but carries an **action** ("entry"), ⛔ not a pipeline.
* `force_intraday_only: false` (`system_config.yaml:89`) and `delivery_enabled: true` (`:102`) **are pipeline-scoped ENTRY gates** (`zerodha_adapter.py:544` coerces intent), ⛔ **not lifecycle controls**.

⇒ **There is NO pipeline-scoped LIFECYCLE stop.** You cannot stop MIS while keeping the delivery pipeline's service duties alive, or vice versa. One process, one unit, one EOD decision.

**(F)** ✅ **F6 has exposed a missing pipeline-scoped lifecycle control.** 📝 **DESCRIBED ONLY, nothing built.** The smallest such control would have to touch: (1) the **process/unit boundary** — today one systemd unit owns both books; (2) the **EOD self-exit decision** — already pipeline-aware as of `75e637c`, so this half is done; (3) the **cadence driver** `order_reconciler:663`, since the delivery monitor's liveness is currently a side-effect of the MIS reconciler's loop; (4) the **kill-switch scope**, which today has no pipeline axis. ⛔ Consistent with the recorded ONE-TRADING-SYSTEM principle; nothing here restates or contradicts it.

---

## M5 — O-1 INPUT · the EOD exit condition **as it runs today**

**(a)** `_eod_self_exit_due` read end-to-end at **`main.py:1227-1323`**; helpers `_position_requires_service` **`:1161-1176`**, `_classify_active_positions` **`:1179-1224`**, `_resolve_position_pipeline` **`:1118-1145`**.

**(b) The condition in force — `due` is True iff ALL THREE hold:**
1. `now.time() >= window_end` — `:1267-1268` (`if now.time() < window_end: return (False, -1)`, **without querying**)
2. no HARD_KILL flatten — `:1269-1274`; ⚠️ **fail-safe: an exception is treated as "flatten IS in progress" ⇒ stay up**
3. `active == 0` — `:1302`, where `active` counts only positions that **require this service**

`_position_requires_service` (`:1173-1176`): `if pipeline != _PIPELINE_DELIVERY: return True` … `return product not in _BROKER_PROTECTED_PRODUCTS`, with `_BROKER_PROTECTED_PRODUCTS = frozenset({"CNC"})` at `:1158`.

✅ **The record's statement — *"due iff past window_end AND no HARD_KILL flatten AND zero positions require this service"* — VERIFIES against the source with NO difference.**

**(c)** ✅ Confirmed: `968bb9c` added **only** the `if strategy_intent_fn is None:` guard + `log.critical(...)` at **`main.py:1374-1386`**, placed **before** `def _run()` at `:1388`. It changes **no** decision branch, and `_eod_self_exit_due` — which computes `due` — is untouched by it.

**(d) The chain, traced on TODAY'S live book:**

| symbol | strategy | YAML `intent` | entry product | `PRODUCT_TO_INTENT` | pipeline | requires service? |
|---|---|---|---|---|---|---|
| THEMISMED | positional_swing_long | DELIVERY | CNC | DELIVERY | DELIVERY | **NO** (CNC is protected) |
| FMGOETZE | positional_sector_rotation | DELIVERY | CNC | DELIVERY | DELIVERY | **NO** |
| HINDCOPPER | first_pullback_long | INTRADAY | MIS | INTRADAY | INTRADAY | **YES** |
| CYIENT | gap_go_long | INTRADAY | MIS | INTRADAY | INTRADAY | **YES** |

(`PRODUCT_TO_INTENT` at `core/constants.py:5-10`: `MIS→INTRADAY, CO→COVER_ORDER, CNC→DELIVERY, NRML→DELIVERY`.)

🔴 **⇒ At 17:35 today, if only the two CNC legs remain, `active == 0` and the service WILL self-exit with a live delivery carry.** That is the designed new behaviour, and it is exactly what tonight tests.

**(e) Strategy census, measured from config today — 16 files: 13 INTRADAY, 3 DELIVERY.** DELIVERY = `positional_momentum_long`, `positional_sector_rotation`, `positional_swing_long`. ⚠️ `pb01_breakout_retest` declares `intent: INTRADAY` but is gated off pending the spec-13 promotion gate.

**(f) L-3 POSTURE — ✅ the code matches.** With `strategy_intent_fn=None`, the `if strategy_intent_fn is not None:` block at `:1283` is skipped entirely and control falls to `:1319-1323` — `active = int(store.count_active_positions())`, the **product-blind** count, which counts **more** and therefore errs toward **staying up**. ⛔ It can never become "assume zero / exit service". Plus the `:1374` CRITICAL. ✅ **No finding.**

---

## M6 — F4 · CNC FILL FAILURE

**(a) All 8 delivery orders, 21-Aug-2026** (`SELECT … FROM orders o LEFT JOIN trades t … WHERE date(o.placed_at)='2026-08-21' AND o.product='CNC'`):

| broker order | symbol | side | qty | type | limit price | status | placed | filled | to fill |
|---|---|---|---|---|---|---|---|---|---|
| …227705 | IIFL | BUY | 1 | LIMIT | **NULL** | CANCELLED | 10:02:16 | — | timeout |
| …230199 | JSFB | BUY | 1 | LIMIT | **NULL** | CANCELLED | 10:03:15 | — | timeout |
| …240209 | KRONOX | BUY | 2 | LIMIT | **NULL** | CANCELLED | 10:07:19 | — | timeout |
| …245066 | CLSEL | BUY | 1 | LIMIT | **NULL** | COMPLETE | 10:09:16 | 10:09:23 | **6.7 s** |
| …253243 | RIIL | BUY | 1 | LIMIT | **NULL** | CANCELLED | 10:12:20 | — | timeout |
| …255539 | MANINDS | BUY | 1 | LIMIT | **NULL** | COMPLETE | 10:13:18 | 10:13:35 | **17.8 s** |
| …257662 | IIFL | BUY | 1 | LIMIT | **NULL** | CANCELLED | 10:14:18 | — | timeout |
| …363253 | KRONOX | BUY | 2 | LIMIT | **NULL** | COMPLETE | 11:07:16 | 11:07:25 | **8.9 s** |

⇒ **5 CANCELLED / 3 COMPLETE = 62.5% failure.** ⚠️ **Correction to the record:** MIS that day was **7 COMPLETE / 1 CANCELLED**, ⛔ not "0 failures".

🔴 **Fills are FAST or never** — the three that filled took 6.7 s, 8.9 s, 17.8 s, all far inside the 60 s window. ⇒ 💭 **INFERENCE:** the timeout length is unlikely to be the binding factor.

**(b) 🔴 THE LIMIT PRICE AT PLACEMENT IS NOT PERSISTED.** `orders.price` is **NULL on all eight**. No LTP/bid/ask is recorded on the order row either. ⭐ **An absent measurement, and the absence is itself the finding** — the single most useful datum for diagnosing a limit-order fill failure is not retained.

**(c/d/e) The paths, and the differences between them.**
* Order type: **LIMIT for both books** — `orders.order_type='LIMIT'` on every CNC entry above, and the live 26-Aug MIS entries log `"order_type":"LIMIT"`.
* Timeout: **`fill_timeout_sec: 60`** — `config/system_config.yaml:141`, **one key, both books**.
* Protocol: 🔴 **identical, and that is itself the M8 finding** — `orders/order_placer.py:960-961` reads `# OP9: choose protocol` / `order_protocol = self._default_protocol`, **unconditionally**. No branch on intent or product. See M8.
* **(e) VERIFIED at `75e637c`, and it applies to the delivery path too**: 13 of 16 strategy YAMLs declare `order_protocol: "CO_PLUS_TGT"`; 3 declare `LIMIT_TRIPLE`; `main.py:3058` constructs `OrderPlacer(` **without** `default_order_protocol`, so the `"LIMIT_TRIPLE"` default at `order_placer.py:572` stands. ✅ **Live proof: all 752 trades across all 13 strategies ran `LIMIT_TRIPLE`; zero `CO_PLUS_TGT` have ever existed.**

**(f) Ranked hypotheses — every one labelled HYPOTHESIS, nothing fixed.**

1. **HYPOTHESIS — LIQUIDITY / SPREAD (strongest).** The CNC names are small/mid-caps (KRONOX, CLSEL, MANINDS, JSFB, RIIL); MIS names are more liquid. A resting LIMIT on a wide spread simply never trades. Supporting evidence: full-history **CNC ENTRY 22 COMPLETE / 51 CANCELLED = 30.1% fill vs MIS 278/531 = 52.4%** — the deficit is **persistent, not a 21-Aug fluke** — and fills, when they happen, are fast.
2. **HYPOTHESIS — LIMIT PRICE PLACED THROUGH THE SPREAD.** Cannot be tested at all, because of (b). ⭐ Testing this requires persisting the limit price and the quote at placement — that is the first thing any F4 fix should add.
3. **HYPOTHESIS — TIMEOUT TOO SHORT (weak).** 60 s is uniform across both books, so it cannot explain a CNC-only deficit; and the successful fills all landed inside 18 s.
4. **HYPOTHESIS — PROTOCOL (REFUTED as a differentiator).** Both books are LIMIT_TRIPLE, so protocol cannot explain a CNC-vs-MIS difference. ⚠️ It remains a live F11 finding in its own right.

---

## M7 — F7 + F8 · CHECK 1 AND CHECK 2

### F7 — 🔴 **NOT an identity. They are OPPOSITE directions of one set difference.**

**(a)** Both read end-to-end:
* `_check1_manual_close` — **`orders/order_reconciler.py:1188`**: *"Local trade is OPEN/PARTIAL but broker has no matching position (RC5a)."*
* `_check2_orphan_adoption` — **`orders/order_reconciler.py:1790`**: *"Broker position exists but no local trade of ANY status tracks it (RC5b)."*

**(b) The algebra.** Let `L` = locally OPEN/PARTIAL trades, `B` = broker positions.
* **CHECK 1 = L \ B**
* **CHECK 2 = B \ L**

These are the two halves of the symmetric difference `L △ B`. They are **complementary, ⛔ not identical**: one is non-empty exactly when the local book over-states, the other exactly when it under-states. ⇒ **The record's "algebraically the same measurement" is REFUTED.** They share an input pair, ⛔ not a measurement.

**(c) CHECK 1 CRITICAL firings — measured over 23 system logs (2026-07-27 → 2026-08-26):** `CHECK1` lines total **30**; **at CRITICAL: exactly 1**. `MANUAL_CLOSE` at CRITICAL: **1**. ⇒ 🔴 **The claim that CHECK 1 "fires CRITICAL on the normal reservation gap" is REFUTED — it has fired CRITICAL once in a month.**

**(d)** A broker-identity-based check would need to read, per symbol: the broker position's `product` (to separate MIS from CNC), its signed `qty`, the broker's `avg_price`, and the resting order book (to tell an unprotected position from a protected one) — then join to the **ENTRY leg** in `orders` for local product identity, since **there is no `trades.product` column**. 📝 **DESCRIBED ONLY.** ⛔ This is a redesign, not a threshold tweak, and is not authorised here.

### F8 — 🔴 **The premise does not match the code at `75e637c`.**

**(a)** The CHECK 2 log statement is **`self._log.info(...)`** at **`orders/order_reconciler.py:1834`**: `"CHECK2 HUMAN_ORDER: symbol=%s broker_qty=%d avg_price=%.2f — no local trade; treating as operator/untracked order…"`. CHECK 2 also carries `.critical` at `:1959` and `:2152`, and `.error` at `:1862`, `:1952`, `:1968`. ⛔ **No CHECK 2 statement is at DEBUG.**

**(b)** Levels: `core/logger.py:450` `root.setLevel(logging.DEBUG)`, `:396` handler at DEBUG with *"level controlled by filters, not handler"*, `:437` queue handler DEBUG, **`:420` `h_stdout.setLevel(logging.WARNING)`**, `:351` a per-logger `INFO`. `config/system_config.yaml:394-395` `logging:` carries only `min_free_disk_gb`. ⇒ routing is per-**destination**, ⛔ not one global level.

**(c) 🔴 REFUTED — CHECK 2 HAS appeared in production.** Across all system logs: **21 CHECK2 lines**, of which **10** are `CHECK2 HUMAN_ORDER`. Example, verbatim: `{"ts":"2026-07-27T10:00:28.004+05:30","level":"WARNING","logger":"order_reconciler","msg":"CHECK2 INFLIGHT_ORPHAN: RKFORGE qty=1 …"}`. FILE 1 also observed one live today (CYIENT, 10:02:17).

**(d) ⛔ The one-line `DEBUG → INFO` change does not apply to CHECK 2.** ⭐ The DEBUG line in this family is **`G3 MARGIN_RECON` at `orders/order_reconciler.py:3709`** (`self._log.debug`) — and it is **not invisible**: **571 lines today** in `reconciler_2026-08-26.log` and in `debug_2026-08-26.log`, and **0** in `system_2026-08-26.log`. ⇒ **a ROUTING distinction, ⛔ not a suppression.** ⛔ Nothing changed.

⭐ **Worth carrying to OWED-2:** that line's own comment (`:3704-3708`) says — *"broker `used` for a SETTLED CNC holding is unmeasured … so alerting here would fire falsely on the first carry day. **Owed: measure a T+1 carry, then decide a threshold.**"* The code itself declares the owed measurement that tonight's carry may finally supply.

---

## M8 — F11 + F14

### 🔴 FIRST, THE SWEEP'S OWN LIMIT — stated before its numbers, because it governs them

The mechanical pass covered **31 YAML files → 2,172 leaf key paths → 428 distinct bare names**, grepped against **261 non-test Python files**. Result: **9** keys with no reader anywhere; **31** read only in `scripts/`/`ops_dashboard/`; **388** with a reader somewhere in the core.

⛔ **That 388 figure is NOT evidence of effect, and must never be quoted as one.** The proof is `order_protocol`: it **has** readers (`ops_dashboard/backend/readers/config_reader.py:73`, `core/state_store.py:1048/1069/1175/1200`), it is **persisted on every trade row**, and it is nonetheless **100% inert at the decision point**. ⭐ **F11 is a REACHABILITY property; only reading the decision site measures it. A name-grep cannot.**

⇒ **(d) I therefore do NOT report a count against the recorded "~22 inert subsystems".** It is **neither confirmed nor refuted** here. ⛔ Manufacturing a number to make the section look complete is precisely the failure this file exists to avoid.

### The 10 named instances — CONFIRMED / REFUTED at `75e637c`

| # | instance | verdict | evidence |
|---|---|---|---|
| 1 | sector cap on empty data | ⚠️ **NOT REACHED** | `sector_cap_mode: observe` (`system_config.yaml:263`) — observe-mode was noted but the empty-data path was not read end-to-end. Honestly untested. |
| 2 | CHECK 2 below log level | 🔴 **REFUTED** | INFO at `:1834`; 21 lines in production (M7 F8) |
| 3 | `max_position_value` dominated | ✅ **CONFIRMED** | `max_position_value_pct: 0.40` (`:177`); concentration binds 100% of the time; max `actual_position_value_rs` ever = **₹1,040.31**. Config itself calls the delivery twin *"MEASURED UNREACHABLE"* (`:196-199`). Family **gamma** |
| 4 | `sl_atr_multiplier` no readers | ✅ **CONFIRMED** | Declared in 16 YAMLs; in Python only `strategies/schema.py:87` (field default) + `:222` (validator). ⛔ No consumer on the SL/sizing path. Family **alpha** |
| 5 | `dynamic_by_winrate` gates nothing | ✅ **CONFIRMED** | `PerformanceAllocator(` appears only at `capital/performance_allocator.py:41` — never instantiated in wiring. Live: `perf_weight_applied = 1.0` on **689/689**. Family **alpha** |
| 6 | startup warnings discarded | ⚠️ **PARTLY — F14-shaped, not F11** | Built at `utils/startup_checks.py:1547`, appended `:1580/1585/1597/1623/1641/1646`, logged `:1666`, returned `:1678`. In `main.py` the only read of `report.warnings` is a `print()` at **`:2477`** in the status branch; the live boot path reads `report.ok` (`:2481`) and `report.blocking_failures` (`:2483`, `:2491`) — **never `warnings`.** Computed, logged, then ignored |
| 7 | `position_reconciliation` unconsumed | 🔴 **REFUTED as F11 → ✅ CONFIRMED as F14** | see below |
| 8 | EOD gate silent degradation | ✅ **CLOSED by `968bb9c`** | guard at `main.py:1374`; FILE 1 proved it live |
| 9 | concentration cap → risk sizer dead | ✅ **CONFIRMED, production-proven** | `binding_constraint='concentration'` on **689/689 = 100.0%**; avg qty candidates: conc **3.28** vs risk **33.73** vs capital **116.46** ⇒ `min()` can never pick another arm. Family **gamma** |
| 10 | tier multiplier pinned at 0.5 | ✅ **CONFIRMED** | `tier_weight_applied = 0.5` on **688/689**; exactly one 0.7; **zero** HIGH. `high_score_threshold: 80` / `medium_score_threshold: 65` (`scoring_weights.yaml:28-29`) against an observed rejection ceiling of **59** |

### 🔴 A FIFTH CONFIRMED F11 — found by the sweep, and the sharpest of them

**`order_protocol` is dead config on BOTH pipelines.**
* `config/strategies/*.yaml` — **13 of 16** declare `order_protocol: "CO_PLUS_TGT"`; 3 (the DELIVERY ones) declare `"LIMIT_TRIPLE"`.
* `orders/order_placer.py:960-961`:
  ```python
  # OP9: choose protocol
  order_protocol = self._default_protocol
  ```
  ⛔ Nothing chooses. No branch on intent, no read of the strategy's value. The module docstring at `:31` promises *"order_protocol determined by intent"* — the code does not implement it.
* `main.py:3058` constructs `OrderPlacer(` (closing `:3084`) **without** `default_order_protocol`, so the `"LIMIT_TRIPLE"` default at `:572` stands.
* ✅ **LIVE PROOF: all 752 trades, across all 13 strategies, ran `LIMIT_TRIPLE`. Zero `CO_PLUS_TGT` trades have ever existed.**

Family: **alpha** (declared, loaded, persisted — never consulted at the decision point).

### F14 — ✅ **FIRST CONFIRMED INSTANCE** (the class previously had none)

**`position_reconciliation`.**
* It **is written** — **18 rows** today, ⛔ not the 0 the 05-Jul audit recorded — and they are not benign: `MISSING_AT_BROKER`, `QTY_MISMATCH`, `ORPHAN_AT_BROKER` (5 on 29-Jul, 5 on 31-Jul).
* It **is read** — `scripts/eod_broker_reconcile.py:274` (`SELECT status FROM position_reconciliation WHERE date = ?`) → `:276` sets `position_recon_issue` (`:86`) → `:134` `if diffs or local.position_recon_issue:` drives the verdict.
* 🔴 **And the verdict gates nothing.** `config/system_config.yaml:407` — `authoritative: false   # SHADOW default: P1 runs alongside eod_verify, writes its verdict + shadow comparison, alerts INFO, **gates nothing**.`

⇒ ⭐ **A control that fires, is consumed, and gates nothing. That is F14, confirmed by measurement rather than manufactured.**

**(g)** Second candidate: the startup `warnings` list (#6 above) — computed, logged once, then never read on the live path. ⚠️ Weaker than the first because it *is* at least logged at INFO.

⛔ **Nothing in M8 was fixed.** Each instance becomes its own unit later.

---

## M9 — F6-LEG · `cnc_gtt_monitor` `abs(int(qty))`

**(a) MEASURED, ⛔ not derived — `orders/cnc_gtt_monitor.py:466`**, inside `_gather` (`:434`):

```python
459|        for p in positions:
460|            product = getattr(p, "product", "") or (p.get("product", "") …)
461|            if str(product).upper() != "CNC":
462|                continue
463|            sym = getattr(p, "symbol", None) or …
464|            qty = getattr(p, "qty", 0) or …
465|            if sym:
466|                held[sym] = held.get(sym, 0) + abs(int(qty))
```
⚠️ **Contrast `:458`, ten lines above, which sums holdings SIGNED:** `held[sym] = held.get(sym, 0) + int(qty)`.

**(b) Mechanism CONFIRMED against the K6 ladder** (`_handle_row`, `:470`):
```python
487|        # 1) GTT fired.
488|        if triggered:
489|            if held == 0:
490|                return self._finalize_gtt_exit(r, reason="GTT_EXIT")   # clean exit
491|            return self._reprotect(r, held, why="F6: GTT triggered but holding still > 0")
```
`held == 0` at `:489` is the **only** gate to the clean exit. On a T+1 GTT sell the same-day CNC position row is `-1`; `abs(-1)` **adds** `+1` instead of cancelling the `+1` holding, so `held` cannot reach 0, `:490` is unreachable, and the row falls to `_reprotect` at `:491`. ✅ **Shape unchanged from the record.**

**(c) ⚠️ I CANNOT CONFIRM the self-resolution claim from code.** The asserted mechanism — settlement clearing the `-1` by the next boot — is a **broker-side state transition**, not a code path; nothing in `cnc_gtt_monitor.py` or `state_store.py` implements or observes it. 💭 It is plausible (a settled sale leaves holdings reduced and no same-day position), but ⛔ **it is an INFERENCE about Kite's behaviour, and I did not measure it.** No T+1 carry has occurred to observe.

**(d) 🔴 THE OPERATIONAL ANSWER, and it is the one that touches the evening routine.**
**A nightly manual `systemctl stop` is NO LONGER required** — provided the 17:35 self-exit fires. Per M5, `due` requires `active == 0`, and `active` now **excludes** a broker-protected CNC carry. So:
* **Flat, or carrying only CNC** ⇒ the service self-exits at 17:35. ⛔ **No manual stop needed.**
* **An INTRADAY position survives past 17:35**, or identity is `CONFLICT`/`UNRESOLVED`, or a HARD_KILL flatten is running, or the pipeline-aware read fails (`:1303`) ⇒ `active > 0` ⇒ **the service stays up, and a manual stop IS required** — otherwise `token_watcher` reads *"running — nothing to do"* at 08:15 and **no boot happens**.

⚠️ **This is behaviour deployed 25-Aug and NOT yet observed at a 17:35.** Tonight is its first test. ⛔ Nothing built.

---

## M10 — F12 / BUCKET R · INVENTORY ONLY

**(a)** ✅ **All five are reachable, and `git merge-base --is-ancestor <sha> 75e637c` is FALSE for every one ⇒ all five are GENUINELY UNPUSHED.** ⛔ No record correction needed on that point.

| unit | SHA | branch | merge-base | files touched | **also changed in `75e637c`** (refit cost) |
|---|---|---|---|---|---|
| tiers | `7d1fd4e` | `feat/tier-multipliers-61-62` | `645728d` | 102 | 🔴 **33** |
| main | `3dff752` | `main` | `645728d` | 34 | 8 |
| controlplane | `5cdd7e9` | `feat/control-plane-g3` | `6fa8a1c` | 9 | 3 |
| gui09 | `725ede9` | `feat/screen10-slippage-analytics` | `6fa8a1c` | 132 | ✅ **0** |
| S07 | `66fc82e` | *(no branch points AT it)* | `6fa8a1c` | 128 | ✅ **0** |

✅ **S07 is SAFE:** `66fc82e` **is an ancestor of `725ede9`**, so `feat/screen10-slippage-analytics` holds it. ⛔ Not dangling.
⭐ **Prioritisation this yields:** `gui09` and `S07` are the **cheapest** refits (zero file collisions) despite being the largest diffs; `tiers` is by far the **most expensive** (33 colliding files).

**Gate status:** every gate any of these holds predates the 25-Aug push. 🏷️ **ALL MARKED `DEAD — OWES REFIT + RE-GATE vs 75e637c`** in the ledger.

**(b) 🔴 THE %TEMP% HAZARD HAS ALREADY FIRED.** Nine worktrees are registered under `C:/Users/rama/AppData/Local/Temp/claude/…`, all `prunable`, and **the directories are already GONE** (verified by `test -d` on `gov-work`, `j2-work`, `eod-work`, `item1-work` — all absent). ✅ **Every commit survived**, because the branch refs live in the MAIN repo's `.git`: `fix/unit-file-reconcile-23aug` `63e0d3d` · `fix/ni-batch-23aug` `b397806` · `fix/ni5-policy-defaults-23aug` `a4a5cef` · `fix/delivery-fill-and-ni-22aug` `742d9da` · `fix/delivery-config-independence-22aug` `d00e574` · `fix/eod-lifecycle-pipeline-aware-25aug` `75e637c`.
⭐ **The lesson, exactly: the REF is what survives, ⛔ never the directory. Anything UNCOMMITTED in a %TEMP% worktree is already lost.**
✅ Safe, outside `%TEMP%`: `trading-system-tiers`, `-controlplane`, `-main`, `-gui09`, `-n907` on `D:/`.

**(c)** ✅ Written into `UNPUSHED_PENDING_DEPLOY_LEDGER.md`. **(d)** ⛔ Nothing refitted, re-gated, or pushed. ⛔ No `worktree remove`, no `prune`.

---

## M11 — Q-2 · THE POST-RECEIVE HOOK

**(a)** `deploy/hooks/post-receive`, 41 lines, read end-to-end; armed at `~/trading-system.git/hooks/post-receive`. Operative body:

```bash
23  TARGET=/home/ubuntu/systems/trading-system
24  GIT_DIR=/home/ubuntu/trading-system.git
25  BRANCH=main
26  VENV_PY=/home/ubuntu/systems/venv/bin/python
28  while read -r oldrev newrev ref; do
29    if [ "$ref" = "refs/heads/$BRANCH" ]; then
30      echo "Deploying $BRANCH to $TARGET..."
31      git --work-tree="$TARGET" --git-dir="$GIT_DIR" checkout -f "$BRANCH"
32      cd "$TARGET" || exit 1
34      if "$VENV_PY" scripts/generate_crontab.py --generate | diff -q - deploy/cron/trading-system.cron >/dev/null 2>&1; then
35        crontab deploy/cron/trading-system.cron && echo "post-receive: crontab AUTO-INSTALLED from canonical."
36      else
37        echo "post-receive: WARNING canonical != generate(registry) on the deployed tree — crontab NOT installed."
38      fi
39      echo "Deployment complete."
```

**(b) ✅ CONFIRMED.** It reads `oldrev newrev ref` at `:28` and gates on the ref at `:29` — then checks out **`"$BRANCH"`** at `:31`, ⛔ **not `$newrev`**. The pushed SHA is never used.

**(c) Every clause verified.** `git remote -v` → `origin trading-vm:~/trading-system.git` ✅ **origin IS the VM's own bare repo** · app dir is not a git repo ✅ (FILE 1) · the push IS the deploy ✅ (`:31`) · no scp ✅ · no separate activation ✅ · **no auto-restart ✅ — `systemctl|restart|service` mentions in the hook = 0.**

**(d) ✅ CONFIRMED, quoted at `:33-38` above.** It regenerates from the **deployed** registry, `diff`s against the canonical file, and installs **only** on a match — otherwise it WARNs and installs nothing. ⛔ Not changed. ⛔ No crontab restored. **Q-1 stays UNKNOWN and unrecoverable by ruling.**

**(e) 🔴 THE MISSING SECOND STEP.** Because `:31` checks out the **branch**, a VM working-tree rollback (`checkout -f <old-sha>`) leaves `refs/heads/main` still pointing at the new SHA. ⇒ **the very next push of ANYTHING to main re-runs `:31` and silently restores the rolled-back code.** ⭐ **A VM-tree rollback is durable only until someone pushes.** The runbook's rollback recipe must therefore either move the remote ref too (RB-2's revert-commit shape) or state explicitly that a tree-only rollback is temporary.

**(f) 🔢 Measured, changed nothing.** Live crontab: **148 total lines, 46 command lines**. Canonical `deploy/cron/trading-system.cron`: **46 command lines**. Registry: **47 job keys** (1 disabled ⇒ 46 generated). ✅ **Live == canonical == generated. Consistent.**

**(g) ✅ Confirmed.** RB-2's parent is derived at use time — `ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md:232` (*"derived, ⛔ never pasted"*), `:154`, `:269`. ✅ **`docs/RUNBOOK.md` names ZERO SHAs — still true** (0 hex-like tokens). ⭐ **Records that should adopt the derive-at-use-time pattern:** any doc that pastes `origin/main`; the TREE/RB-3 target, by contrast, must stay **literal**, because "last SHA proven to boot" is ⛔ not derivable from `origin/main`.

**(h) 📝 DESCRIBED ONLY, ⛔ NOT WRITTEN.** The amendment needs: a step stating that a tree-only rollback is undone by the next push; the ref-moving alternative (revert commit + push) as the durable form; and a post-rollback verification that the bare `refs/heads/main` matches the intended tree. ⛔ Separate authorised documentation unit.

---

## M12 — F2 RE-ANCHOR INVENTORY AT `75e637c` (measurement only)

**(a/b) The keys, with pipeline scope.** ✅ The 22-Aug independence work is visible and explicit — `system_config.yaml:185-193` states there is **NO inheritance** between the books.

| key | value | file:line | pipeline |
|---|---|---|---|
| `capital.intraday_bucket_pct` | 0.70 | `:144` | INTRADAY |
| `capital.positional_bucket_pct` | 0.30 | `:145` | DELIVERY |
| `capital.slm_margin_buffer_pct` | 0.05 | `:150` | BOTH |
| `capital.sl_limit_offset_pct` | 0.005 | `:151` | INTRADAY |
| `capital.gtt_sl_limit_offset_pct` | 0.03 | `:152` | DELIVERY |
| `capital.leverage_map` | INTRADAY 5.0 / CO 6.0 / DELIVERY 1.0 / BO 5.0 | `:154-158` | BOTH (by intent) |
| `position_sizing.risk_per_trade_pct` | 0.01 | `:166` | INTRADAY |
| `position_sizing.max_concentration_pct` | 0.10 | `:167` | INTRADAY |
| `position_sizing.max_position_value_pct` | 0.40 | `:177` | INTRADAY |
| `position_sizing.tier_multipliers` | 1.0 / 0.70 / 0.50 | `:178-181` | BOTH |
| `position_sizing.dynamic_by_winrate` | true | `:182` | ⚠️ **INERT** (F11 #5) |
| `delivery_risk_per_trade_pct` | 0.01 | `:194` | DELIVERY |
| `delivery_max_concentration_pct` | 0.10 | `:195` | DELIVERY |
| `delivery_max_position_value_pct` | 0.40 | `:200` | ⚠️ **DELIVERY, self-declared UNREACHABLE** |
| `risk.max_open_positions` | 5 | `:212` | ⚠️ **AMBIGUOUS** |
| `risk.max_daily_trades` | 10 | `:213` | ⚠️ **AMBIGUOUS** |
| `risk.max_open_delivery_positions` | 3 | `:224` | DELIVERY |
| `risk.max_daily_delivery_trades` | 5 | `:225` | DELIVERY |
| `risk.max_sector_exposure_pct` | 0.40 | `:254` | INTRADAY |
| `risk.delivery_max_sector_exposure_pct` | 0.40 | `:255` | DELIVERY |
| `risk.daily_loss_limit_pct` | 0.03 | `:257` | INTRADAY |
| `risk.delivery_daily_loss_limit_pct` | 0.03 | `:258` | DELIVERY |

**⚠️ AMBIGUITY IS A FINDING — and there is one:** `max_open_positions: 5` is commented *"portfolio-wide cap on concurrent open positions"*, i.e. **BOTH books**, while `max_open_delivery_positions: 3` is a delivery-only cap **nested inside it**. Same for `max_daily_trades: 10` vs `max_daily_delivery_trades: 5`. ⇒ these two are **shared, not split**, and they are the only capital-path caps that still couple the books.

**(c) Name/meaning disagreements.**
1. 🔴 **`slm_margin_buffer_pct`** — named for an **SL-M** order, but `:151`'s own comment states *"Zerodha rejects SL-M via API"*. The buffer is named after an order type the system cannot place.
2. ⚠️ **`delivery_max_position_value_pct`** — the config itself calls it **"MEASURED UNREACHABLE"** (`:196-199`): 40% of TOTAL while the positional bucket is 30% of TOTAL and concentration binds at 10% first. Present only because the no-fallback contract admits no absent key.
3. ⚠️ **`dynamic_by_winrate` / `min_multiplier` / `max_multiplier`** — read by nothing on the sizing path (F11 #5).
4. ✅ **No duplicate found for daily loss** — `capital.daily_loss_limit` was deleted (`:147-149`); `risk.daily_loss_limit_pct` is the sole authority.

**(d) ✅ Reservation behaviour CONFIRMED FROM SOURCE** — `capital/fund_manager.py:557-563`:
```python
557|            bucket = self._bucket_for_intent(intent)
558|            base_margin = required_margin(qty, price, intent, self._leverage_map)
560|            # FIX-090: Add SL-M margin buffer (5% for unknown fill price risk)
562|            slm_buffer = base_margin * self._slm_buffer_pct
563|            total_margin = base_margin + slm_buffer
```
with `required_margin` at `:267-268`: `leverage = leverage_map.get(intent, 1.0); return (qty * price) / leverage`. ⇒ **ONE reservation per entry attempt; base = notional / leverage; plus a 5% buffer.** SL and TGT legs reserve nothing (no `reserve` call on the exit paths). ✅ Matches the 22-Aug finding.

**(e) 🔴 CONFIRMED, AND THE LINE NUMBER MOVED.** `max(1, min(tiered_qty, raw_qty * 2))` is **LIVE at `capital/position_sizer.py:605`**. ⚠️ **The record says `:506`.** That is a second independent line-number drift today — the Q-3 lesson repeating. ⛔ Reported only; not removed.

**(f) 🔴 CONFIRMED — the code uses CONFIGURED leverage, never actual-applicable.** `leverage_map` is a flat per-intent table (`:154-158`); `broker_limits.yaml` is **rate-limiting only** and carries no leverage data; and there is **no per-symbol or per-day leverage lookup anywhere in the code** (0 matches for `mis_multiplier|margin_multiplier|per_symbol_leverage|instrument_leverage`). ⇒ Zerodha's *"UP TO 5x, varying by instrument and day"* is treated as **exactly 5x, always**. Under-reserving is the direction of error where Zerodha grants less.

**(g) ✅ `count_active_positions` — PRODUCT-BLIND, CONFIRMED.** `core/state_store.py:639-656`:
```sql
SELECT COUNT(*) AS n FROM trades WHERE status IN ('OPEN', 'PARTIAL', 'PENDING_FILL')
```
⛔ No product filter, ⛔ no join to `orders`. Its own docstring (`:663-667`) records that this is deliberate: it has three production consumers (the EOD gate, the risk_engine OPEN_POSITIONS cap, the portfolio allocator), so making it pipeline-aware would move a live risk cap.
**Digest:** md5 **`43a5648304a093b025fb9d94812d84c9` — MATCHES the record exactly.** Length reads **943** vs the recorded **941** — a measurement-method difference (the md5 match proves the content is identical). 👤 **O-4 left unresolved BY DESIGN; both figures retained.**

**(h)** ⛔ No design, no proposals. Inventory only. ⛔ The decided capital model was neither recomputed nor contradicted.

---

## M13 — O-2 · MEMORY.md TRUNCATION — **MEASURE AND ESCALATE ONLY**

**(a) 🔴 `MEMORY.md` = 8,877 bytes.** ⛔ **NOT ~25.5 KB.** The premise is **stale**.

**(b)** ⚠️ **I could not locate a harness-defined load limit**, and say so plainly rather than inventing one. The **24,000 B** figure is a **self-imposed guard written inside `MEMORY.md` itself**, whose own text records that the file *"hit 27,820 B on 26-Aug and WAS TRUNCATED ON LOAD"*. That event evidently prompted a trim that has already happened.

**(c) Nothing is being lost today.** At 8,877 B the file is at **37%** of its own 24,000 B guard. ⛔ No truncation, so the head-vs-tail question does not arise.

**(d) All sizes, measured now:**

| file | bytes |
|---|---|
| `MEMORY.md` | **8,877** ✅ |
| `MEMORY_REFERENCE.md` | 6,408 |
| `MEMORY_RULES.md` | 9,375 |
| `MEMORY_HAZARDS.md` | 17,496 |
| `MEMORY_ARCHIVE_2026H1.md` | 40,824 |
| `MEMORY_BOARD.md` | **50,632** ← largest MEMORY_* |
| `mempalace.yaml` | 48,755 |
| `PATHS.md` | 484,515 |
| `docs/SYSTEM_MAP.md` | 1,063,300 |
| `UNPUSHED_PENDING_DEPLOY_LEDGER.md` | **1,406,022** ← largest overall |

⚠️ **Only `MEMORY.md` auto-loads**, so the five large files are not a load-limit risk in the same way — but the **1.4 MB ledger** and **1.06 MB SYSTEM_MAP** are past the point where any reader (human or model) can read them end-to-end, which is why S1 above is stated honestly.
⚠️ **A pre-existing guard violation stands, and I did ⛔ NOT fix it:** `LC_ALL=C awk 'length>(index($0,"🔝")?450:300)' MEMORY*.md` prints **`MEMORY_BOARD.md 6: 829`**.

**(e)** 👤 **ESCALATED to Rama as a decision item.** ⛔ Nothing rebuilt, split, trimmed or reordered.

---

## M14 — F10 · UPSTREAM FUNNEL (numbers only; stays PARKED)

**(a) Full history, ⛔ not 12 sampled days.** `2026-06-12 → 2026-08-26`: **172,345 signals → 602 `PROCESSED` (0.35%) → 300 filled trades (0.17%)** (752 trade rows, 300 with `qty_filled > 0`).

| family | n | % |
|---|---|---|
| scoring (`REJECTED_SCORE_*`) | 112,629 | **65.35** |
| **`REJECTED_STRATEGY_CONTROL`** | 21,430 | **12.43** |
| circuit proximity | 8,461 | 4.91 |
| **`SKIPPED_QUOTE_UNAVAILABLE`** | 6,888 | **4.00** |
| strategy circuit breaker | 6,864 | 3.98 |
| daily trade limit | 5,146 | 2.99 |
| shadow inning | 4,168 | 2.42 |
| sizing | 3,862 | 2.24 |
| other | 2,295 | 1.33 |
| **`PROCESSED`** | **602** | **0.35** |

⭐ **A material difference from the recorded sample:** `REJECTED_STRATEGY_CONTROL` — *"WON'T TRADE — emergency breaker (force_intraday_only) forces intraday; delivery strategy dormant"* — is the **second-largest family at 21,430 (12.43%)** and does not appear in the 12-day breakdown at all. 🔬 **It is HISTORICAL: it last fired 2026-08-04.** Today `force_intraday_only: false` (`:89`) and `delivery_enabled: true` (`:102`), consistent with delivery trading live.

**(b) `SKIPPED_QUOTE_UNAVAILABLE` — 6,888 (4.00%).** ⭐ Agreed framing: this is **the system failing to look**, not a strategy declining.

| month | n | | recent day | n | % of that day |
|---|---|---|---|---|---|
| 2026-06 | 1,202 | | 2026-08-26 | **0** | 0.00 |
| 2026-07 | 1,973 | | 2026-08-25 | **0** | 0.00 |
| 2026-08 | 3,713 | | 2026-08-24 | 131 | 1.76 |
| | | | 2026-08-20 | 406 | 6.40 |
| | | | 2026-08-19 | 521 | **12.22** ← peak |

🔬 **Trend: rising through August, then ZERO on both 25-Aug and 26-Aug.** ⛔ I did not establish the cause of the drop and do not speculate.
**Code path:** emitted at `screening/secondary_screener.py:177-191` (`_make_skipped("SKIPPED_QUOTE_UNAVAILABLE", …)`). A related, distinct release exists at `screening/entry_gate.py:454` (`EG9`: skip 1–2 quote failures, release `QUOTE_UNAVAILABLE` on the 3rd consecutive). ⚠️ **Honest limit: I located these paths but did NOT read `secondary_screener.py` end-to-end**, so I do not draw a conclusion about *why* quotes fail.

**(c)** ✅ **F10 STAYS PARKED.** No fix, no proposal.

---

## M15 — SCOPE BOUNDARY

⛔ Confirmed left alone, untouched and un-reported-on beyond this line: **F1, F3, F5, F6e, the F8 fix, F9, F13 (no `/etc/sudoers*` access), S6, S07 (inventory only), D-1b, D-3, NI-16, O-3, O-4, O-5, Q-1, Q-5, G-G, P6-EV, DEFECTS A/B/C, N20-19, N20-20, N20-47, the Phase-2 90 rows, `integrity_audit_2026.md`, V3/PB-01 (the 18:15 shadow cron untouched), and worktree housekeeping.** ⛔ No pair of defects was merged. ⛔ No unpushed unit was refitted or re-gated.
