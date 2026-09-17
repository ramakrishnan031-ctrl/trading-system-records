# RULINGS 1 & 2 — RECORDED, AND THE VERIFICATION THEY COMMISSIONED

**07-Aug-2026 (Friday) · Opus 5 · ⛔ READ-ONLY MEASUREMENT + DOCUMENTATION. NO CODE. NO SCHEMA. NO GATE.**

> # 🏷️ **LEGEND — READ BEFORE THE FINDINGS** *(moved here 07-Aug-2026; it used to sit mid-document, after two sections of graded claims)*
>
> **THREE vocabularies are in use. They answer THREE DIFFERENT QUESTIONS, which is why there are three
> and why there will not be a fourth.**
>
> | vocabulary | the question it answers | values |
> |---|---|---|
> | **VERDICT BUCKETS** | *what is the conclusion?* | **(a)** confirmed defect · **(b)** confirmed design · **(c)** assumption disproved · **(d)** cannot determine |
> | **EVIDENCE CLASS** *(`M9`)* | 🔑 ***HOW* is it known?** | **(P)** it happened · **(S)** the code says so · **(I)** follows from the code, never observed |
> | **EVIDENCE STRENGTH** | 🔑 ***HOW MANY WAYS* is it known?** | **`X1`** one source · **`X2`** two independent · **`X3+`** three or more |
>
> ⭐ **`(P)/(S)/(I)` and `X1/X2/X3+` are orthogonal and both are needed:** an **(S)·X1** claim is read
> from one file and never observed; a **(P)·X3+** claim happened and three independent sources agree.
> ⛔ **A proposed scheme that answers one of these three questions a SECOND time will be refused** —
> three such proposals have now been declined *(`campaign_practices.md` `M9.2`/`M9.3`)*, each after
> trying and failing to construct a claim the existing vocabulary could not express.
> ⚠️ **X-tags are applied to the Monday prediction card and to §11–§12 here; ⛔ §8–§10 carry
> `(P)/(S)/(I)` only, and that back-fill is NOT owed** *(§10.3)*.

> ## 📌 PROVENANCE OF EVERY CODE CITE
> Measured at repo **`612a06b`**. Every commit from `348c226` to that point is **docs-only** —
> `git diff --name-only 348c226..HEAD -- '*.py' '*.yaml' '*.sql'` returns **empty** — so every file
> cited below is **byte-identical to `348c226`**. `capital/risk_engine.py`, `core/state_store.py`,
> `orders/cnc_gtt_monitor.py` and `allocation/portfolio_allocator.py` are additionally unchanged
> since `0197923` (the SHA the prior documents pinned); **`signals/signal_processor.py` is NOT** —
> it changed between `0197923` and here, so its line numbers were **re-measured**, not inherited.
> **(M3: line numbers hold only at their measured SHA.)**
>
> **Production reads:** `data_store/trading_system.db` on the VM, `mode=ro` URI, ~16:0x–16:2x IST.
> **Config reads:** `config/system_config.yaml`, PC and VM compared on the keys that matter — identical.

---

# §0 · OBJECTIVE

Two things, and they are different in kind:

**(A) RECORD** the two governance rulings Rama took on 07-Aug-2026 — decision-ledger rows **1**
(control-inventory authority) and **2** (shared symbol namespace, tightened). Documentation only.

**(B) VERIFY** seven hypotheses (H1–H7) about whether the system can actually answer the question
Ruling 2 rests on: *"does an OPEN position currently exist for this symbol?"* Read-only.

⛔ **NO IMPLEMENTATION IS AUTHORISED BY ANY OF THIS.** No gate changed, no predicate rewritten, no
config key flipped, no schema, no F6 fix, F6's retirement checklist untouched. Gate 2 — Rama's
authorisation in his own words for a build — has not been given.

---

# §1 · DOCUMENTATION CHANGES MADE

| # | commit | what |
|---|---|---|
| 1 | `98e7406` | **Ruling 1 recorded.** Authority header on `ops_dashboard/docs/G2a_capacity_inventory.md`; one-line superseded pointer at `docs/audit/audit_05jul2026.md:527`. The 27 rows **not** edited. Location **not** decided — the file stays put. |
| 2 | `612a06b` | **The 113-key review merged in.** `30 + 14 = 44` rows; five collision classes; the review demoted in place to evidence. |
| 3 | `520d363` | **Ruling 2 recorded verbatim** in `MASTER_PENDING_01-Aug-2026.md` §R.2, with the three consequences scored against measurement; cross-referenced at `delivery_config_surface` §7.1, `module_17_risk_engine.txt`, G2a row 36 + §H-5; dated note only in the F6 design doc. |
| 4 | *(this file)* | the verification. |
| 5 | — | `PATHS.md` + `docs/SYSTEM_MAP.md` refreshed. |

**⛔ ONE DOCUMENTED SITE WAS DELIBERATELY NOT CROSS-REFERENCED.** `docs/report_data_contract.md:189`
names `REJECTED_DUPLICATE_SYMBOL`, but it documents *how the reject code is bucketed in a report*,
not the protection rule. A ruling cross-ref there would be noise in a data contract. **Stated, not
silently skipped.** The 27 other files matching the grep are **dated audit reports** — history, and
the campaign rule against editing dated history applies.

---

# §2 · H1–H7 — VERDICTS

**Buckets:** **(a) CONFIRMED DEFECT · (b) CONFIRMED DESIGN · (c) ASSUMPTION DISPROVED ·
(d) CANNOT DETERMINE.** **Evidence classes:** **(P)** it happened · **(S)** the code says so ·
**(I)** it follows from the code but has never been observed.

## H1 — "exactly THREE product-blind gates enforcing one-trade-per-symbol"
### 🏷️ **(b) CONFIRMED DESIGN — with a correction: the true count is 3, 4 or 5 depending on the definition, and the card's definition yields 3.** **(S)** + **(P)**

**Width of the search:** every call site of `has_active_position`, `get_active_position_direction`
and `count_executed_trades_today_for_symbol_direction` across the whole repo (**each has exactly ONE
production caller**), plus a repo-wide grep for `DUPLICATE_SYMBOL|CONTRARY_POSITION|SYMBOL_DIRECTION_DAILY_LIMIT|one_trade_per_symbol`
across all `*.py`.

| # | gate | file:line **@`612a06b`** | reject code emitted | config key | **the EXACT predicate, quoted** |
|---|---|---|---|---|---|
| **1** | symbol + **direction**, per day | `signals/signal_processor.py:706-720` | `SYMBOL_DIRECTION_DAILY_LIMIT` <sub>(raised as `_PipelineReject`)</sub> | **`risk.one_trade_per_symbol_direction_per_day` = `true`** (`:224`) | `n = count_executed_trades_today_for_symbol_direction(symbol, direction, today)` → `if n >= 1: raise` — SQL at `core/state_store.py:723-730`: `WHERE symbol = ? AND direction = ? AND SUBSTR(created_at,1,10) = ? AND status IN (PENDING_FILL, OPEN, PARTIAL, EXITING, CLOSED, CLOSED_MANUAL)` |
| **2** | symbol, **opposite** direction | `capital/risk_engine.py:665-686` <sub>(check **9**)</sub> | `CONTRARY_POSITION` | ⛔ **none — unconditional** | `if active_direction is not None:` … `is_contrary = (incoming=="LONG" and active=="SHORT") or (incoming=="SHORT" and active=="LONG")`. Fed at `:289` by `get_active_position_direction` — `core/state_store.py:866-874`: `SELECT direction FROM trades WHERE symbol = ? AND status IN ('PENDING_FILL','OPEN','PARTIAL') LIMIT 1` |
| **3** | symbol, **any** direction | `capital/risk_engine.py:688-694` <sub>(check **10**)</sub> | `DUPLICATE_SYMBOL` | ⛔ **none — unconditional** | `if has_dup:` … Fed at `:286` by `has_active_position` — `core/state_store.py:845-852`: `SELECT COUNT(*) FROM trades WHERE symbol = ? AND status IN ('PENDING_FILL','OPEN','PARTIAL')` |

**The card's count of three is right.** Two further sites exist and are named because a later reader
who greps will find them:

| # | site | why it is **not** one of the three | status |
|---|---|---|---|
| **4** | `allocation/portfolio_allocator.py:182-183` — `if c.symbol in admitted_symbols: return "DUPLICATE_SYMBOL"` | it dedupes **within one admission batch**, not against the book | 🔴 **INERT** — `allocator_mode: 'shadow'`; shadow **never reserves or places** ⇒ live admission byte-identical. ⚠️ **It emits the identical label `DUPLICATE_SYMBOL`** — a classification-leakage hazard for anyone counting by string |
| **5** | `signals/entry_throttle.py:97-107` — `per_symbol_cooldown_sec = 300` | it is a **spacing** rule, not a **uniqueness** rule | ✅ **LIVE** — and see §4 OPEN-2: *"immediately becomes eligible again"* and a 5-minute cooldown are in direct tension |

> ⭐ **THE STRUCTURAL FINDING H1 EXISTS TO SURFACE: gates 2 and 3 ARE ONE PREDICATE.**
> `has_active_position(symbol)` and `get_active_position_direction(symbol) is not None` are the same
> SQL condition — same table, same status triple — read twice. Gate 2 partitions it by direction and
> runs first; gate 3 catches the remainder. **(P) `CONTRARY_POSITION` has fired ZERO times in
> 109,254 signals** *(width: the complete `signals.status` distribution, every status listed)* —
> because gate 3 is unconditional, so any active position rejects regardless of direction, and gate 2
> can only ever claim the opposite-direction slice of that.

## H2 — "one is date-filtered; `DUPLICATE_SYMBOL` is not, so a carried delivery position blocks intraday indefinitely"
### 🏷️ **(b) CONFIRMED DESIGN, per gate — and (a) CONFIRMED DEFECT in its consequence.** **(S)** + **(P)**

| gate | date-filtered? | evidence | expiry |
|---|---|---|---|
| 1 `SYMBOL_DIRECTION_DAILY_LIMIT` | ✅ **YES** | `AND SUBSTR(created_at,1,10) = ?` with `today = now_ist().date().isoformat()` (`signal_processor.py:712`) | **midnight** |
| 2 `CONTRARY_POSITION` | ⛔ **NO** | the SQL has no date term | 🔴 **never** — only the trade closing |
| 3 `DUPLICATE_SYMBOL` | ⛔ **NO** | the SQL has no date term | 🔴 **never** — only the trade closing |

**The consequence is CONFIRMED and it is LIVE right now.** **(P)** two trades sit `OPEN` with
`exit_time IS NULL`: `DIFFNKG` (`trd_010f8e21…`, since 06-Aug 10:02:16) and `MANINFRA`
(`trd_9e709c50…`, since 07-Aug 10:05:23). Both symbols are therefore blocked to **every** pipeline,
with **no expiry mechanism other than the trade closing** — which is exactly what F6 prevents.

> ### ⭐⭐ **AND THE MASKING IS NOW MEASURED, NOT ONLY REASONED**
> `delivery_config_surface` §7.2 argued from source that gate 1 fires first and masks gate 2 on day 1.
> **(P) The production record shows the switchover as a clean edge:**
> `REJECTED_DUPLICATE_SYMBOL` — **107 all-time, LAST fired 31-Jul-2026**.
> `REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT` — **65 all-time, FIRST fired 03-Aug-2026**.
> 31-Jul (Fri) → 03-Aug (Mon) are consecutive trading days. ⛔ **Anyone measuring the symbol block
> under `REJECTED_DUPLICATE_SYMBOL` after 03-Aug reads ZERO and concludes it stopped happening.**
> ⚠️ **NOT ESTABLISHED, and not chased (G3):** the config commit that set the key `true` is
> `300a247`, dated **27-Jul** — four trading days before the first rejection. Whether the gap is a
> deploy lag or simply no qualifying signal is **not determined here**.

## H3 — "NONE of the three evaluates *is a position open right now*"
### 🏷️ **(c) ASSUMPTION DISPROVED — and this is the report's most consequential correction.** **(S)**

| gate | what it actually evaluates | is that "open right now"? |
|---|---|---|
| 1 | *"has this symbol+direction been traded **today**"* — the status set includes **`CLOSED`** and **`CLOSED_MANUAL`** | ⛔ **NO.** This is historical ownership, and Rama's ruling names that exact thing as what it is *not* |
| 2 | *"is there an active position in the **opposite** direction"* — `PENDING_FILL/OPEN/PARTIAL` | ✅ **YES**, restricted to one direction |
| 3 | *"is there an active position"* — `PENDING_FILL/OPEN/PARTIAL`, any direction, any product | ✅ **YES** |

> 🔴🔴 **GATES 2 AND 3 ALREADY IMPLEMENT RULING 2.** Product-blind ✅ · never date-scoped ✅ ·
> release the instant the trade leaves `PENDING_FILL/OPEN/PARTIAL` ✅ · *"evaluated from the current
> account state"* ✅ (to the limit of what `trades` knows — see H4/H5).
> **Gate 1 is the only one the ruling contradicts**, and it is the only one with a config key.
> ⇒ **The loosening half of Ruling 2 is `risk.one_trade_per_symbol_direction_per_day: false`.**
> **(S)** the code's own docstring: *"DEFAULT OFF. When … is false this returns before touching the
> store, so the pre-27-Jul path is **byte-identical**."* (`signal_processor.py:678-679`, and the
> guard at `:706-707` is a bare early `return`.)
> ⛔ **This is a measurement, NOT a recommendation to flip it.** See §4 OPEN-1 and consequence (ii).

## H4 — what source of truth WOULD answer *"is a position open for this symbol right now"*
### 🏷️ **(b) CONFIRMED DESIGN — the enumeration is complete and the answer is: nothing reachable covers both products.** **(S)**

**The gate's call sites, and what they can reach.** `RiskEngine.__init__` (`capital/risk_engine.py:139-190`)
takes `fund_manager`, `state_store`, `kill_switch`, `sector_lookup_fn`, `logger` and scalars —
**no broker adapter, no parameter of any adapter type.** `signals/signal_processor.py:26` states the
rule in the file header: **"SP14 — Layer 5; no direct broker import."**

| # | candidate source | reachable **at the gate**? | covers INTRADAY? | covers DELIVERY? | sign-safe? |
|---|---|---|---|---|---|
| 1 | broker `get_positions()` — `broker/zerodha_adapter.py:1182-1240` | 🔴 **NO** — no adapter on either gate object | ✅ | ⚠️ **T+0 only.** From T+1 the holding moves to `holdings()`; the CNC row that remains is the **SELL** | 🔴 **signed** — `qty=int(row["quantity"])` from Kite's `net`; paper mirrors it deliberately (`:1194-1200`) |
| 2 | broker `get_holdings()` — `:928` | 🔴 **NO** | ⛔ no | ✅ **T+1 onward only** | positive by nature |
| 3 | `trades` via `has_active_position` | ✅ **YES — the only one that is** | ✅ | ✅ | n/a — status-based, no qty |
| 4 | `orders` table | ✅ yes | ✅ | ✅ | it carries **`product`**, but no position state; ⛔ and there is **no `trades.product` column** — product is reachable only via `LEFT JOIN orders … leg='ENTRY'` |
| 5 | `fund_manager` reservation ledger (`get_live_reservations()`, `:1494`; `_Reservation.symbol` exists) | ✅ yes | ✅ in-flight only | ✅ in-flight only | n/a |
| 6 | `cnc_gtt_monitor`'s `held` map (`orders/cnc_gtt_monitor.py:451-465`) | 🔴 **NO** — an exit monitor; **no gate calls it** | ⛔ no | ✅ | 🔴 **NO — `abs(int(qty))` at `:464`. This is F6** |
| 7 | `gtt_state` ACTIVE rows | ✅ yes | ⛔ no | ✅ proxy only | n/a |

> ⭐ **THE ANSWER:** only **candidate 3** is reachable at the gate **and** covers both products —
> and it is a **DB assertion about our own bookkeeping**, not a statement about the account.
> **Candidates 1+2 TOGETHER are the only broker-truth answer, and neither is reachable.**
> ⚠️ **Even combined they are not sufficient without a sign rule** — see H5b.

## H5a — is `cnc_gtt_monitor`'s held computation (the `abs()` defect, F6) ON the path that would answer H4?
### 🏷️ **(c) ASSUMPTION DISPROVED — LEXICALLY. And (a) CONFIRMED DEFECT — CAUSALLY.** **(S)**

**Lexically: NO.** `_gather` and `_handle_row` have no caller in `risk_engine` or `signal_processor`;
the grep for `has_active_position` / `get_active_position_direction` returns exactly one production
caller each, both inside `risk_engine`. The gate never evaluates `:464`.

**Causally: YES, and it is decisive.** The gate reads `trades.status`. What writes `CLOSED` to a
delivery trade is `_finalize_gtt_exit` → `mark_trade_closed_gtt`, and **`held == 0` is the sole door
to it** — reached at `cnc_gtt_monitor.py:487` (GTT triggered), `:501-510` (holding flat), and nowhere
else. `:464` makes `held` unable to reach 0 after a completed SELL. ⇒

> ## 🔒 **F6 IS A PREREQUISITE OF RULING 2, NOT A BENEFICIARY OF IT.**
> The `abs()` is not *in* the predicate; it is the reason the predicate's **data source is wrong**.
> A gate can be perfectly implemented on `trades` and still block a genuinely free symbol forever.
> **(P) That is not hypothetical — it happened.** ATULAUTO was sold by its own GTT at ~09:31:56 on
> 06-Aug; the trade row stayed `OPEN`; the symbol stayed blocked; it cleared only at the 07-Aug
> 08:15 boot. **(P)** `DIFFNKG` and `MANINFRA` are in that state **right now**.

## H5b — does ANY candidate in H4 mishandle the SIGN of quantity?
### 🏷️ **(a) CONFIRMED DEFECT — it is a CLASS, at six production sites.** **(S)**

**The source is signed.** `zerodha_adapter.py:1233` `qty=int(row.get("quantity", 0))` from Kite's
`net` book; `:1194-1200` records that paper returns the **signed** net *on purpose*, "NOT `abs()`",
so reverse-aware consumers pick the right flatten direction. **A completed CNC SELL of a T+1 holding
survives the `!= 0` filter as a NEGATIVE row.**

**Every production site that applies `abs()` to a position quantity** *(width: repo-wide grep for
`abs(int(` / `abs(float(` / `abs(qty` / `abs(...quantity` across all `*.py`, excluding `tests/`)*:

| site | context | would a completed SELL read as a HOLD? |
|---|---|---|
| `orders/cnc_gtt_monitor.py:464` | the F6 line | 🔴 **YES — measured** |
| `orders/order_reconciler.py:2968` | CHECK9 FACET-2 oversell guard, `live_held = abs(int(_p.qty))` | 🔴 **YES** — and it takes the **first** matching symbol row and `break`s, so it is also product-blind |
| `orders/order_reconciler.py:2185` · `:2291` · `:3120` | FACET-1 / FACET-2 / CHECK7 | 🔴 yes, same shape |
| `orders/eod_squareoff.py:1079` · `:1487` · `:1525` · `:1613` | flatten sweeps | 🔴 yes, same shape |
| `capital/kill_switch.py:1281` | `if abs(int(getattr(p,"qty",0) or 0)) > 0` | 🔴 yes |
| `orders/structure_exit_manager.py:631` | `abs(int(getattr(p,"qty",0) or 0))` | 🔴 yes |

⚠️ **Most of these are on INTRADAY paths where the net genuinely reaches 0 and the row is filtered
out, so the `abs()` is harmless today.** ⛔ That is exactly what makes it a class rather than a bug:
**the same expression is correct on one path and wrong on the other, and nothing at the call site
distinguishes them.** ⭐ **A broker-truth open-position predicate written in the house style would
reproduce F6 at a new site on its first day.**

### 🎯 H5 — CROSS-CHECK AGAINST F6's SEVEN COSTS

Costs 1–5 are tabulated at `f6_delivery_exit_predicate_design_06aug2026.md` §15; cost 6 at §15.1;
cost 7 (the measurement layer publishing numbers it cannot vouch for) at `MASTER_PENDING` candidate 4.

| F6 cost | does Ruling 2 retire it? |
|---|---|
| 1 · ₹587.42 re-reserved every boot — **capital** | ⛔ **no** — untouched |
| 2 · 1 of 3 delivery slots held — **concurrency** | ⛔ **no** — untouched |
| **3 · `DUPLICATE_SYMBOL` blocks the symbol indefinitely** | 🔴 **NO — and this is the cost the retirement claim was about.** Ruling 2 **ratifies** the block: *"if any open position already exists… every new entry is rejected."* A phantom `OPEN` row **is** such a position under a `trades`-based reading. ⭐ **It would retire only under a BROKER-TRUTH reading — which H4 shows is not reachable at the gate, and H5b shows would need a sign rule the codebase does not have** |
| 4 · three live SELL GTTs on a flat holding | ⛔ no |
| 5 · a fabricated exit price, permanently in the data | ⛔ no |
| 6 · the nightly manual stop; a missed one costs a full trading day | ⛔ no |
| 7 · the day's P&L understated (−7.20 reported vs ≈−19.10 real) | ⛔ no |

> ## ⛔ **0 of 7 RETIRED. THE DEPENDENCY RUNS THE OTHER WAY, AND THE SEQUENCING REVERSES WITH IT.**
> ⭐ The claim made when option (b) was offered is **false**, and it was false in the direction that
> would have let Ruling 2 be built first.

## H6 — how much same-day re-entry does the tightened rule actually permit?
### 🏷️ **(a) CONFIRMED — measured, and it exceeds the daily cap on the first day it applies.** **(P)**

**Method.** Take every signal with `status='REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT'` (gate 1 is the
only gate whose predicate Ruling 2 contradicts — H3). For each, ask whether a position was open for
that symbol **at that instant**: a trade with `created_at <= t` and `(exit_time IS NULL OR
exit_time > t)`. If yes, Ruling 2 rejects too and nothing changes. If no, Ruling 2 **permits**.

```sql
-- the population
SELECT signal_id, symbol, received_at, substr(received_at,1,10) AS d
  FROM signals WHERE status='REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT' ORDER BY received_at;
-- per row, "was the symbol genuinely free at that instant?"
SELECT count(*) FROM trades
 WHERE symbol = ? AND created_at <= ?
   AND (exit_time IS NULL OR exit_time > ?)
   AND status IN ('PENDING_FILL','OPEN','PARTIAL','EXITING','CLOSED','CLOSED_MANUAL');
```

| measured | value |
|---|---|
| rejections in the population | **65** (03-Aug 10:12:15 → 07-Aug 14:53:15) |
| distinct days · distinct symbols | **5 days · 16 symbols** |
| **WOULD STILL REJECT** (a position was open) | **56** |
| 🔴 **WOULD NOW BE PERMITTED** | **9** |
| **on how many days** | **2** — 05-Aug (**3**) and 06-Aug (**6**) |
| **for how many symbols** | **4** — `ENGINERSIN`(1) · `SUDEEPPHRM`(2) *(05-Aug)* · `DECNGOLD`(3) · `MAYURUNIQ`(3) *(06-Aug)* |

**56 + 9 = 65 ✅.**

> ### 🔴 **AND THE NUMBER THAT MATTERS MOST IS NOT 9 — IT IS 11.**
> **(P)** 05-Aug executed **8** trades; +3 permitted ⇒ **up to 11**. 06-Aug executed **5**; +6 ⇒
> **up to 11**. `risk.max_daily_trades` = **10**.
> ⇒ **On BOTH days the loosening pushes the book past the daily cap.** The extra entries would not
> all have been taken — `max_daily_trades` would have rejected the overflow — but the constraint
> that catches them is a cap that **has not bound since 10-Jul** (H7). ⛔ **The loosening is not
> absorbed by headroom; it consumes all of it and reactivates a dormant cap.**

**⛔ THREE LIMITS ON THIS NUMBER, STATED RATHER THAN BURIED:**
1. **It is a LOWER bound, and F6 pushes it down.** **(P)** 7 of the 56 "would still reject" rows are
   blocked by a trade whose `exit_time IS NULL` — `DIFFNKG` and `MANINFRA`. If F6 were fixed, some
   of those symbols may have been genuinely flat, moving rows from 56 into the permitted set.
   ⭐ **The contamination runs in the same direction as the defect.**
2. **The population is 5 trading days.** Gate 1's reject code first appears 03-Aug (H2). ⛔ Nothing
   here says what a month looks like.
3. **9 rejected SIGNALS ≠ 9 additional TRADES.** The scanner re-fires the same symbol; the permitted
   set contains repeats (`SUDEEPPHRM` ×2, `DECNGOLD` ×3, `MAYURUNIQ` ×3). Upper bound **9**; the
   realistic figure is bounded below by **4** (distinct symbols).

## H7 — what caps bound entries today, and which BINDS first?
### 🏷️ **(c) ASSUMPTION DISPROVED — no DAILY cap has bound in ~20 trading days. The live bound is CONCURRENCY, and a same-day re-entry does not consume it.** **(P)**

| cap | key | value @07-Aug | enforcement site | **(P) rejections all-time** | last fired |
|---|---|---|---|---|---|
| score gate | `scoring_weights.min_pass_score` | 60 | `quality_scorer` | **61,117** `REJECTED_SCORE_*` (32 distinct statuses, of 109,254 signals) | daily |
| strategy control | — | — | `signal_processor` control gate | **21,430** | daily |
| **concentration (sizing)** | `position_sizing.max_concentration_pct` | **0.10** | `position_sizer.py` | **3,486** | daily |
| strategy circuit breaker | `strategy_circuit_breaker.*` | 2.0× / 12:00 / 10d | `strategy_governor` | **4,433** | daily |
| **entry throttle** | `min_gap` 20s · `burst` 3/60s · `per_symbol` 300s | — | `signals/entry_throttle.py` | **436** | daily — **earliest-firing control on 19 of 21 trading days** |
| **max open positions** | `risk.max_open_positions` | **5** | `risk_engine` check 4 | **500** | **07-Aug** ✅ still live |
| per-strategy concurrency | `strategies/<s>.max_concurrent_positions` | 2 (gap_fade 3) | `signal_processor` H-7 cap | **302** | **07-Aug** ✅ still live |
| **max daily trades** | `risk.max_daily_trades` | **10** | `risk_engine` check 5 | **5,146** | 🔴 **10-Jul — and never since** |
| bucket capital 70/30 | `capital.intraday_bucket_pct` / `positional_bucket_pct` | 0.70 / 0.30 | check 3 + `reserve()` | **24** `REJECTED_SIZING_CAPITAL` | 07-Aug |
| consecutive losses | `risk.max_consecutive_losses` | **4** *(both inventories said 5)* | check 6 | **3** | 03-Aug |
| **daily loss limit** | `risk.daily_loss_limit_pct` | **0.03** | check 7 + post-close breach | 🔴 **0 — no such reject status exists** | never |
| sector exposure | `risk.max_sector_exposure_pct` + `sector_cap_mode` | 0.40, **`observe`** | check 8 | **0** — observe mode | never |
| delivery caps | `risk.max_open_delivery_positions` / `max_daily_delivery_trades` | **3 / 5** | checks 4/5 positional branch | ⛔ **not separately countable** — the delivery branch emits the **same** check name | — |

> ## 🔴 **WHICH BINDS FIRST — TWO ANSWERS, AND THE CARD'S RATIONALE DEPENDS ON THE SECOND**
> **(1) By pipeline order / frequency:** the **entry throttle** fires earliest on **19 of 21** days
> (typically 10:00:2x, on the window-open burst) and `SIZING_CONCENTRATION` on the other 2.
> ⛔ **But a throttle DELAYS; it does not consume the day.**
> **(2) By what actually stops the day:** 🔴 **nothing does.** `max_daily_trades` last bound
> **10-Jul**; peak trades since is **9** (29-Jul) against a cap of **10**. The caps still firing —
> `max_open_positions` (500) and per-strategy concurrency (302) — are **CONCURRENCY** caps, and
> ⭐⭐ **a same-day re-entry after a complete exit does not consume a concurrency slot: the slot was
> released by the exit.** ⇒ **Ruling 2's loosening is bounded by `max_daily_trades = 10` alone, and
> H6 shows both affected days reaching 11.**
> ⚠️ **STATED NOT CHASED (G3):** **(P)** 17-Jun shows **12** executed trades against a cap of 10.
> Outside this card's scope; recorded so it is not later found and mistaken for new.

---

# §3 · P1–P7 SCORED

⭐ **Written by the card's author BEFORE any measurement existed. 5 HELD · 1 FAILED · 1 SPLIT.**

| # | prediction | score | why |
|---|---|---|---|
| **P1** | H1 = exactly 3 *(low confidence, "never measured")* | ✅ **HELD** | 3 uniqueness gates, confirmed at source with all call sites enumerated. ⚠️ The author's own low-confidence flag was warranted for a different reason than expected: the count is right, but **two further symbol-keyed sites exist** (inert allocator, live 300 s cooldown) and neither had ever been written down |
| **P2** | H2 CONFIRMED as stated | ✅ **HELD** | per gate, and the consequence is live on two symbols right now |
| **P3** | H3 CONFIRMED for **all** gates — none consults live openness | 🔴 **FAILED** | **Gates 2 and 3 DO** consult current openness (`PENDING_FILL/OPEN/PARTIAL`, no date term). ⭐⭐ **The most valuable failure in the set:** it converts Ruling 2 from *"build a new predicate"* into *"turn one date-scoped gate off"*, and it is the reason consequence (i) is half-refuted |
| **P4** | broker positions/holdings the only both-product candidate, **and not reachable** at the gate | ➗ **SPLIT — reachability HELD, sufficiency FAILED** | ✅ not reachable: `RiskEngine.__init__` has no adapter; `signal_processor.py:26` *"no direct broker import"*. 🔴 but **neither API alone covers both** — `positions()` is blind to delivery from T+1, `holdings()` blind to intraday; **and `trades` (candidate 3) DOES cover both**, which the prediction did not anticipate |
| **P5a** | REFUTED — `cnc_gtt_monitor` is an exit monitor, not on the gate path *(explicitly the corrected, weaker form of what was said in chat)* | ✅ **HELD** | lexically refuted, exactly as predicted. ⭐ **The correction was right to make**: the chat statement overreached, and the weaker prediction is the one that survived |
| **P5b** | CONFIRMED — sign handling is a class, not a line | ✅ **HELD** | **six** production sites apply `abs()` to a signed broker quantity |
| **P6** | count > 0 *(no figure predicted)* | ✅ **HELD** | **9**, on 2 days, across 4 symbols |
| **P7** | at least max-positions + daily-loss exist; **max-positions binds** | ➗ **HELD on the letter, and the letter understates it** | both exist ✅ and max-positions **is** the binding cap among those still firing ✅ — but **daily loss has never fired at all**, and **the daily-trade cap has not fired since 10-Jul**, so "binding" describes a much emptier field than the prediction implies |

> ⭐⭐ **THE METHODOLOGICAL RESULT HOLDS AGAIN, AND P3 IS THE EVIDENCE.** Every prediction was written
> down first; the one that failed, failed *informatively* and changed the sequencing. ⛔ **A predicted
> outcome that merely gets confirmed teaches nothing about the predictor.**

---

# §4 · §1.4 — **DID THE AUTHORITY RULE BIND?**

## ✅ **YES — it bound twice, and it then required an AMENDMENT. Both, not either.**

**IT BOUND (1) — it stopped the obvious action.** The natural way to "merge 113 keys into a 30-row
inventory" is to write a fresh table containing both key sets. The authority rule forbids creating a
parallel inventory, so the merge had to be **G2a absorbing the review's axes**, with the review
demoted **in place**. ⛔ Without the rule I would have produced a new file, and it would have been a
third inventory wearing a merge's name.

**IT BOUND (2) — it stopped a fabrication.** §1.3 asked for the row arithmetic. The honest arithmetic
is `30 + 14 = 44`, **not** anything ending in 113. The review's **113 is a scope count and was never a
row set** — the document nowhere enumerates 113 rows, and its own bucket total is on record as
reconciling by accident. Producing 113 rows would have required re-deriving the key list from YAML:
**a new measurement wearing a merge's clothes.** The authority rule made that visible as a violation
rather than as diligence.

## ⚠️ **AND IT NEEDED AMENDING — the ruling as taken is necessary and insufficient**

The ruling says the documents are *"keyed on the dotted config key, and the dotted key is the join
identifier."* **That is true, and it did not prevent a single one of the five collisions.** The join
worked perfectly. What failed is that **the two documents mean different things by a *row***:

- G2a's row unit is *a configured limit with a capacity semantic* (a limit ↔ a live counter).
- The review's row unit is *a key or family in the delivery-isolation decision*.
- ⇒ They disagree about whether `webhook.*`, `clock.*`, `signal_queue.*` and `live_feed.*` belong
  **at all** (§H-4), and about how many leaf keys a family has in **10 of 11** shared families (§H-3).

**AMENDMENT ADOPTED** (in the authority header, same day): an authority also declares its **ROW
UNIT**, its **INCLUSION RULE**, and its **VALUE PROVENANCE**. 🏷️ **Parent (G7): it narrows Ruling 1
itself** — the join identifier stays, and two clauses are added without which the ruling permits a
merge that silently changes what the document is.

> ⭐⭐ **AND THE RULE'S FIRST APPLICATION IS WHAT CAUGHT IT — not a review of the rule.**
> That is now the **fourth** governance rule in this campaign found wanting by being *run* rather
> than by being *read*, and the third to be repaired by amendment rather than replacement.
> **(G7.1: AMENDED beats binding unchanged.)**

---

# §5 · COLLISIONS FOUND IN THE 113-KEY MERGE

Full tables with both values and both sources: `ops_dashboard/docs/G2a_capacity_inventory.md` §H.
**Five classes. None resolved silently.**

| # | class | the collision | resolution |
|---|---|---|---|
| **H-1** | **VALUE** | `risk.max_consecutive_losses`: G2a row 5 says **5** · `audit_05jul2026.md:537` says **5** · **`system_config.yaml:226` says 4** | measured value governs; row 5 corrected in place with its provenance |
| **H-2** | 🔴 **SCOPE — a false premise in both inventories** | the delivery caps are tagged **"INERT (`force_intraday_only=true`)"** in both. **Measured: `force_intraday_only: false` (`:89`), `delivery_enabled: true` (`:102`), `trade_type: BOTH` (`:96`)** — and two CNC positions are open | the tag is **superseded** in the authority. ⛔ An operator reading "INERT" about a live delivery cap is the exact failure the authority exists to stop |
| **H-3** | **FAMILY SIZE** | `alerts.*` — G2a: absent · review: **9** · **measured 31**. `entry_gate.*` — G2a: 4 · review: **9** · **measured 17**. Also `smart_tgt` 3/5/**5** · `strategy_circuit_breaker` 3/4/**4** · `circuit_breaker` 3/2/**3** · `clock` 3/—/**6** · `order_reconciler` 3/3/**7** · `signal_queue` 2/—/**4** · `webhook` 2/—/**7** · `live_feed` 1/—/**3** | ⭐⭐ **exactly ONE of eleven — `drift_handler.*` (4) — matches.** Same defect shape as the 113 accident: **a family counted as if it were a key.** ⇒ the ROW-UNIT clause |
| **H-4** | **INCLUSION RULE** | 4 of G2a's 30 rows sit inside the review's **~90-key excluded infra families** | the authority's inclusion rule governs; the rows stay; the review's exclusion is recorded as *that review's scope*, never a deletion |
| **H-5** | **AN UNRECORDED SITE** | `allocation/portfolio_allocator.py:182-183` emits the label `DUPLICATE_SYMBOL` for a batch rule; it is in **no** inventory, 27-row or 30-row | added as row **41**; cross-referenced to Ruling 2 |

**ARITHMETIC, operands shown:** `BEFORE 30` (§A 8 + §B 2 + §C 7 + §D 5 + §E 8) `+ ADDED 14`
(§G 31–44, each checked against all 30 by dotted prefix) `= AFTER 44`. Re-added independently by
section: `8+2+7+5+8+14 = 44` ✅, and the highest row number is **44** ✅ — two checks that could have
disagreed. **Leaf-key coverage measured, not hand-counted: 169 of 301**; the 132 uncovered decompose
`98` signal-generation + `34` infra `= 132` ✅, **independently reproducing the review's own "98
excluded" figure by a different route.**

⚠️ **NOT RESOLVED:** the review's **301 vs 302** corpus ambiguity. Today's read reproduces **301 leaf
keys / 42 sections by YAML parse** — the *same method* as the review, so it corroborates one arm and
settles nothing. The 302 came from an indentation walk, which was **not re-run**.

---

# §6 · OPEN ITEMS — ⛔ owed to Rama, nothing started

| # | item | why it is open |
|---|---|---|
| **OPEN-1** | 🔴 **Ruling 2's loosening half is a CONFIG FLIP, and it is NOT authorised.** `risk.one_trade_per_symbol_direction_per_day: true → false` is the whole of it (H3). ⛔ **Not flipped, not staged, not proposed as a next step.** It re-admits the SENCO trade class by design, and **H6 shows both affected days reaching 11 against a cap of 10**. **⚠️ AMENDED 07-Aug evening — TWO THINGS THIS ROW DID NOT SAY:** ① 🔴 **THE EVIDENCE IS ONE-SIDED: the protection LOST is measured, the OPPORTUNITY GAINED is NOT — and cannot be, from 9 rejected signals with no outcomes (§9.4).** The only adjacent figure (~38–39 % win vs ~43.5 % breakeven) argues *against* removal but is **formally silent** on the sub-population gate 1 actually rejects. ② **(P) the cooldown is NOT a fallback** — it measures entry→entry, residual **zero on 82.2 %** of trades (§8.3), so removal falls back onto nothing. ⛔ **And per §9.1, "SENCO created gate 1" is HISTORY, ⛔ not an argument that it should stay** | Gate 2 has not been given. **And the sequencing now says F6 first regardless** (H5) |
| **OPEN-2** | ⚠️ **`per_symbol_cooldown_sec: 300` contradicts the ruling's wording.** Rama's text says the symbol *"immediately becomes eligible again"*; the throttle blocks re-entry for 5 minutes. It is a **spacing** control, not an ownership one, so it may be intended to survive — **but that is a decision, not an inference** | needs one sentence from Rama: does *"immediately"* govern throttles too? |
| **OPEN-3** | 🔒 **Sequencing REVERSED: F6 must land before Ruling 2 is implemented.** Not before it is *recorded* — that is done | H5: 0 of 7 F6 costs retired; F6 is what makes the predicate's data source wrong |
| **OPEN-4** | **Gates 2 and 3 are one predicate read twice, and gate 3 makes gate 2 unreachable** — `CONTRARY_POSITION` has fired **0** times in 109,254 signals. Whether it is retired, or kept as a documented no-op, is a decision | ⛔ **not proposed.** Recorded because a gate that cannot fire is indistinguishable from one that has not yet needed to |
| **OPEN-5** | **The `abs()`-on-signed-quantity class (6 sites, H5b) has no owner.** F6 fixes one line of it | belongs with the F6 design, not with this card |
| **OPEN-6** | **The 27-row and 30-row inventories are DIFFERENT PARTITIONS** — one keyed on *control*, one on *config key*. Recorded in G2a's footer so `27 → 30` is never read as `+3` | ⛔ no reconciliation attempted; the 27 rows are frozen history |
| **OPEN-7** | ⚠️ **A gate-1 deploy-lag question, stated not chased (G3):** config `true` committed **27-Jul** (`300a247`); first rejection **03-Aug**; four trading days between | not determined here |

---

# §7 · WHAT THIS REPORT DOES NOT ESTABLISH

- ⛔ **Nothing about a month of behaviour.** H6's population is **5 trading days**, H7's is 21.
- ⛔ **Nothing about paper/live parity of the gates themselves.** Both gate call sites are DB-only and
  therefore mode-agnostic *(that is (I) — it follows from `no direct broker import`, and no paper
  drill of these gates was run)*. ⚠️ **But the parity hazard is real one layer down:** any
  broker-truth implementation inherits **PAPER NETS BY SYMBOL / LIVE KITE NETS PER (SYMBOL, PRODUCT)**,
  and a paper drill of it would be **vacuously green**.
- ⛔ **No claim that flipping the config key is safe.** H6 measures what it permits; it says nothing
  about whether those nine entries would have been profitable.
- ⛔ **No test was run and none was needed** — this card changed no code, so there was nothing a
  regression could have gone red on. **(P)** `git diff --name-only 348c226..HEAD -- '*.py' '*.yaml'
  '*.sql'` = empty.

---
---

# §8 · 07-Aug-2026 EVENING — THE ENTRY-THROTTLE MEASUREMENT (Q1–Q5) + THE BROKER GTT CHECK

**⛔ READ-ONLY. NO CODE. NO CONFIG. NO SCHEMA. NO GTT CANCELLED. NO BUILD.**

> **WHY THIS IS HERE AND NOT IN A NEW FILE.** The card offered a choice. This is an **append**,
> because §8 does not introduce a topic — it **closes OPEN-1 and OPEN-2 of this document's own §6**
> and **corrects this document's own H1 row 5 and H7 row 5**. A companion file would fork the record
> that PATHS.md and `SYSTEM_MAP.md` already point at by section. The anti-duplication rule binds here
> exactly as it bound Ruling 1 in §4.
>
> **PROVENANCE.** Code read at working-tree `8affcae` (docs-only since `348c226`; `signals/entry_throttle.py`
> is byte-identical to its only ever commit, `c0554c6`). Production reads: VM
> `/home/ubuntu/systems/trading-system/logs/system_2026-07-27.log` (JSON), `journalctl -u trading-system.service`,
> `data_store/trading_system.db` `mode=ro`, and **the Zerodha GTT/orders/holdings/positions API**, ~17:0x–17:3x IST.

---

## §8.1 — Q1 · FROM WHAT EVENT DOES `per_symbol_cooldown_sec` MEASURE?

### 🏷️ **(b) CONFIRMED DESIGN — it measures PREVIOUS ENTRY → NEW ENTRY. There is no exit hook anywhere in the class.** **(S)** + **(P)**

**The code that RECORDS the timestamp** — `signals/entry_throttle.py:109-113`, inside `admit()`, on the
admit path only:

```python
            # admit — record the placement
            self._last_entry = now
            self._recent.append(now)
            if symbol:
                self._per_symbol_last[symbol] = now
```

**The code that COMPARES against it** — `signals/entry_throttle.py:97-107`:

```python
            # 3. per-symbol cooldown
            if self._per_symbol > 0 and symbol:
                last = self._per_symbol_last.get(symbol)
                if last is not None:
                    elapsed = now - last
                    if elapsed < self._per_symbol:
```

> ### ⭐ **`_per_symbol_last[symbol]` IS WRITTEN AT EXACTLY ONE PLACE IN THE REPOSITORY — LINE 113, INSIDE `admit()`.**
> *(Width: repo-wide grep for `entry_throttle|EntryThrottle|per_symbol_cooldown|\.admit\(` across every
> `*.py`. Every hit outside `tests/` is a **constructor** argument (`main.py:3150`, `core/config_loader.py:404`,
> `signals/signal_processor.py:151/230-234`), a **metrics read** (`:602`), or one of the three `admit()`
> calls. **No exit path, no fill path, no `trade_closed` path, and no reconciler touches this class.**)*
>
> ⇒ **The interval is PREVIOUS ENTRY → NEW ENTRY.** The class has no way to learn that a position exited.

**And `admit()` is reached at entry DISPATCH, not at fill.** All **three** production `_placer.place(`
call sites — `signal_processor.py:1263` (main), `:2028` (gate path), `:2305` (retest path) — are each
immediately preceded by `_tr = self._entry_throttle.admit(symbol)` at `:1249`, `:2017`, `:2296`.
**(S)** The chokepoint is complete: there is no fourth production `place()` site.

---

## §8.2 — Q2 · WHY DID IT NOT BLOCK SENCO ON 27-JUL? — **ALL FOUR NAMED CANDIDATES, SCORED**

### 🏷️ **(b) CONFIRMED DESIGN. Candidate 1 is the whole explanation. Candidates 2, 3 and 4 are each REFUTED BY MEASUREMENT — not merely unsupported.** **(P)** + **(S)**

| # | candidate | verdict | evidence, and the width of the check |
|---|---|---|---|
| **1** | **the cooldown measures from the wrong event** | ✅ **SUPPORTED — and sufficient alone** | §8.1 (S) + §8.3's arithmetic (P): the operand the throttle actually held was **719.644 s**, which is **2.399×** the 300 s threshold. It was consulted, it evaluated correctly, and it correctly admitted |
| **2** | the value was different on 27-Jul | 🔴 **REFUTED** | **(P)** `git show d3fa5b8:config/system_config.yaml` — the tree deployed at 10:14 on 27-Jul — reads `per_symbol_cooldown_sec: 300`, identical to today. **Width:** `git log -S "per_symbol_cooldown_sec"` over `system_config.yaml`, `entry_throttle.py`, `signal_processor.py`, `main.py`, `config_loader.py` returns **exactly one commit ever** — `c0554c6`, 19-Jun-2026. **The value has been 300 continuously since the day it was created and has never been edited** |
| **3** | the throttle is not on that code path | 🔴 **REFUTED** | **(S)** all 3 production `place()` sites are throttle-gated (§8.1). **(P)** and it demonstrably ran on that symbol that morning: `SENCO … rejected at ENTRY_THROTTLED` never appears, but the gate itself fired **7 times on 27-Jul**, including its **`per_symbol` category twice** (§8.4) |
| **4** | **the throttle state is in-memory and had been LOST** *(the card flagged this as the more serious outcome)* | 🔴 **REFUTED — decisively** | **(P)** the **complete** `systemd[1]` record for `trading-system.service` on 27-Jul is **THREE LINES**: `Started 08:15:30` · `Deactivated successfully 17:35:04` · the CPU-consumption summary. **Width:** `journalctl -u trading-system.service --since 2026-07-27 00:00 --until 2026-07-28 00:00`, filtered to `systemd[1]` — the emitter that *must* log any start, stop, crash or scheduled restart — and the line count is **3**. ⇒ **ONE continuous process spanning both SENCO entries.** The in-memory map still held SENCO's 10:02 timestamp at 10:14 |

> ## ⭐⭐ **THE RESULT IS THE OPPOSITE OF A FAILURE, AND THAT IS WHY IT MATTERS**
> The throttle did not miss SENCO, was not reset, was not bypassed and was not misconfigured.
> **It held the correct timestamp, computed the correct interval, and correctly admitted** — because
> the interval it is built to measure is not the interval the incident is about.
> ⛔ **There is nothing here to fix.** There is a semantic to be *known before a control is removed.*

### 🔴 **AND A SECOND, INDEPENDENT REASON — WHICH REFRAMES OPEN-1 ENTIRELY**

**(P) Gate 1 did not exist when SENCO re-entered.** The tree deployed at 10:14 on 27-Jul was
`d3fa5b8` (26-Jul 23:19:19). In that tree **both halves are absent** — the config key
`one_trade_per_symbol_direction_per_day` and the code site `SYMBOL_DIRECTION_DAILY_LIMIT` /
`count_executed_trades_today_for_symbol_direction`. They arrive later **the same day**:

| commit | timestamp (IST) | what | Δ after the 10:14:12 re-entry |
|---|---|---|---|
| — | **27-Jul 10:14:12** | **the SENCO re-entry** | — |
| `656b62d` | **27-Jul 13:54:12** | `feat(signals): one completed trade per symbol+direction per day -- DEFAULT OFF` — the code | **+3 h 40 min** |
| `300a247` | **27-Jul 15:24:31** | `feat(config): TURN ON the one-trade-per-symbol+direction rule (Rama, 27-Jul eve)` — `: true` | **+5 h 10 min** |

> ## 🔴🔴 **SENCO IS NOT A TRADE THAT GATE 1 HAPPENS TO COVER. SENCO IS THE INCIDENT THAT CREATED GATE 1 — CODE AND CONFIG BOTH AUTHORED THAT SAME AFTERNOON.**
> ⭐ This also settles **OPEN-7** in passing: the "four trading days" between the config commit
> (27-Jul) and the first rejection (03-Aug) is **not** a deploy lag question about a pre-existing
> rule — the rule was **born** on 27-Jul evening, after the market closed. *(⛔ Whether the gap from
> 28-Jul to 03-Aug is deploy lag or simply no qualifying signal is still **not determined** — that
> half of OPEN-7 stands.)*

---

## §8.3 — Q3 · THE SENCO ARITHMETIC, OPERANDS SHOWN

### 🏷️ **(b) CONFIRMED DESIGN — the interval the throttle evaluated was 719.644 s, and every operand is quoted.** **(P)**

**Every timestamp below is quoted from the `ts` field of a JSON line in
`logs/system_2026-07-27.log` on the VM. No figure is stated that was not read from that record.**

**The proxy, stated rather than assumed:** `admit()` returns at `signal_processor.py:1249`,
microseconds before `place()` emits `order_placer.place_start`. `place_start` is therefore used as the
**admit instant**. Its error is bounded below by the preceding `risk_engine.approve` line, so the true
interval lies in **[718.941 s, 720.298 s]** — and every value in that interval exceeds 300 s, so the
verdict does not depend on the proxy.

| # | event | quoted timestamp (IST) |
|---|---|---|
| ① | trade 1 `risk_engine.approve … approved=True` | `10:02:12.033` |
| ② | trade 1 `trade_created` `trd_c9675b4fae4a…` | `10:02:12.685` |
| ③ | 🔑 **trade 1 `order_placer.place_start` — `admit("SENCO")` recorded here** | **`10:02:12.687`** |
| ④ | trade 1 entry fill @ **418.75** (`avg_fill_price`) | `10:02:17.674` |
| ⑤ | 🔑 **trade 1 `trade_closed` `exit_reason:"TGT_HIT"` @ **425.05** | **`10:13:31.744`** |
| ⑥ | trade 2 `risk_engine.approve … approved=True` | `10:14:11.628` |
| ⑦ | 🔑 **trade 2 `order_placer.place_start` — `admit("SENCO")` consulted here** | **`10:14:12.331`** |
| ⑧ | trade 2 entry fill @ **425.25** (`limit_triple_exits_placed reason:"entry_fill"`) | `10:14:51.157` |

### THE THREE INTERVALS

| interval | operands | seconds | vs 300 s | outcome |
|---|---|---|---|---|
| 🔑 **ENTRY → ENTRY** — *what the throttle actually measured* | ⑦ − ③ = `10:14:12.331 − 10:02:12.687` | **719.644** | **+419.644 (2.399×)** | ✅ **ADMITTED — correctly** |
| **EXIT → re-entry DISPATCH** — *what an exit-keyed cooldown would have measured* | ⑦ − ⑤ = `10:14:12.331 − 10:13:31.744` | **40.587** | **−259.413** | 🔴 **would have BLOCKED** |
| **EXIT → re-entry FILL** — *the figure carried in the incident record* | ⑧ − ⑤ = `10:14:51.157 − 10:13:31.744` | **79.413** | −220.587 | 🔴 would have BLOCKED |

**✅ RECONCILIATION:** the SENCO report's *"Exit → re-entry gap: 10:13:31 → 10:14:51 = 80 seconds"* is
**79.413 s** at full precision. The record is correct; the "80" is a rounding of it.

> ### ⭐ **THE TENSION THE CARD OPENED WITH IS DISSOLVED, NOT EXPLAINED AWAY**
> The card wrote: *"A live 300-second per-symbol cooldown did not stop an 80-second re-entry."*
> **(P) The throttle never saw 80 seconds. It saw 719.644.** The 80 s figure describes an interval
> that **no control in this system measures.** Both stated facts were true; they were about different
> intervals, and nothing in the repo reconciled them because nothing in the repo computes the second.

### 🔑 **AND THE NUMBER THAT PRICES THE DECISION — TRADE 1's HOLDING PERIOD**

⑤ − ③ = `10:13:31.744 − 10:02:12.687` = **679.057 s** (11 min 19 s).

⇒ **When SENCO exited, its cooldown had already been expired for 379.057 s.** Generalised:

> ## 🔴 **THE PER-SYMBOL COOLDOWN'S RESIDUAL PROTECTION AGAINST AN IMMEDIATE RE-ENTRY IS EXACTLY `max(0, 300 − holding_period)`. FOR ANY TRADE HELD LONGER THAN FIVE MINUTES IT IS *ZERO*.**
> **(P) MEASURED over the whole book** — 225 closed trades carrying both `entry_time` and `exit_time`
> (`status IN ('CLOSED','CLOSED_MANUAL')`):
>
> | | n | share |
> |---|---|---|
> | held **< 300 s** — cooldown still alive at exit, offers *some* cover | **40** | **17.8 %** |
> | 🔴 held **≥ 300 s** — cooldown already dead at exit, offers **NO** cover | **185** | **82.2 %** |
>
> **median holding period = 1,596 s (26.6 min) = 5.3× the cooldown.** *(min 2 s · max 166,460 s)*
> ⇒ **On roughly four trades in five, the 300 s cooldown has nothing left to give at the moment the
> re-entry question arises.**
>
> ### ✅ **ROBUSTNESS — the figure is NOT an artifact of delivery carries, and this check could have gone red**
> The 166,460 s maximum is a T+1 carry, and a `GTT_EXIT` trade's `exit_time` is the **boot-time
> finalisation**, not the real exit (F6) — so delivery rows could have inflated the number. **Re-run
> with them excluded:**
>
> | population | n | held ≥ 300 s | median |
> |---|---|---|---|
> | all closed | 225 | **185 = 82.2 %** | 1,596 s |
> | **excluding `exit_reason='GTT_EXIT'`** | 222 | **182 = 82.0 %** | 1,574 s |
> | only `GTT_EXIT` (delivery) | 3 | 3 = 100 % | 2,479 s |
>
> ⇒ **82.2 % → 82.0 %. The conclusion is carried by the intraday book, not by the three delivery
> rows.** *(Exit-reason mix: `SL_HIT` 106 · `TGT_HIT` 72 · `MANUAL` 44 · `GTT_EXIT` 3.)*

---

## §8.4 — ⭐⭐ THE PYRAMID CONTROL — THE SEMANTICS PROVEN ON PRODUCTION DATA, NOT ONLY READ FROM SOURCE

**(P)** The `per_symbol` gate fired **twice on 27-Jul**, on PYRAMID. Because the reject string prints
the operand (`f"per_symbol {symbol} {elapsed:.0f}s < {self._per_symbol:.0f}s"`), the log **states the
interval the throttle measured** — which makes this a direct discriminator between the two candidate
semantics, on live data, on the same day as SENCO.

| # | previous PYRAMID `order_placer.place_start` | throttle reject line | wall-clock Δ | **printed `elapsed`** | match at printed precision |
|---|---|---|---|---|---|
| 1 | `10:06:13.701` | `10:07:14.035` — `per_symbol PYRAMID 60s < 300s` | **60.334 s** | **60** | ✅ |
| 2 | `10:11:13.903` | `10:12:14.835` — `per_symbol PYRAMID 61s < 300s` | **60.932 s** | **61** | ✅ |

> ### 🔴 **AND THE DISCRIMINATOR IS CLEAN BECAUSE PYRAMID NEVER EXITED — IT NEVER EVEN OPENED.**
> **(P)** the full PYRAMID event list for 10:00–10:20 shows the 10:06 entry was **REJECTED BY THE BROKER**:
> `place_order call_start 10:06:14.637` → **`Zerodha rejected order: MIS orders are currently blocked for PYRAMID`** `10:06:14.678`
> → `mis_blocklist: recorded MIS-block` `10:06:15.471` → `Pipeline exception` `10:06:15.474`.
> **There is no PYRAMID position, no fill and no exit anywhere in that window** ⇒ an exit-keyed
> cooldown would have had **no timestamp to measure from** and could not have printed `60s`/`61s` at all.
> **The only events 60.3 s and 60.9 s before the two rejects are the two dispatches.** **Q1 is proven twice over.**

### ⚠️ **A CONSEQUENCE THIS SURFACED THAT WAS IN NO DOCUMENT — REGISTERED, NOT FIXED**

### 🏷️ **(b) CONFIRMED DESIGN, with a consequence worth knowing** **(P)**

**`admit()` records the placement BEFORE `place()` is called** — deliberately, and the docstring gives
the reason: *"a split would leave a TOCTOU window where a burst of concurrent worker threads all pass
check() before any records."* Correct for burst suppression. **But it means a placement the broker
REJECTS still consumes the symbol's full 300 s cooldown.** PYRAMID is the measured instance: an order
that was never accepted locked the symbol for five minutes and blocked **three** later signals
(`10:07:14.035`, `10:07:14.840`, `10:12:14.835`).

⭐ **Same family as the standing finding *"it counts its own rows where it means the broker's reality"*** —
here the throttle counts its own **dispatch** where a reader would assume it counts an **entry**.
⛔ **Not a defect and not proposed for change**: the TOCTOU rationale is sound and this is the price of it.

⚠️ **And one more, stated because it bears directly on OPEN-2:** PYRAMID's two dispatches are
`10:11:13.903 − 10:06:13.701` = **300.202 s** apart. It re-entered **0.202 s after the cooldown
expired.** With a scanner re-firing on a ~60 s cadence, **the cooldown does not prevent the re-entry —
it schedules it.** *(This is the measured form of H7's "a throttle DELAYS; it does not consume the day.")*

---

## §8.5 — Q4 · DOES THE THROTTLE DISCRIMINATE DIRECTION, OR PRODUCT?

### 🏷️ **(b) CONFIRMED DESIGN — NEITHER. It is direction-blind and product-blind, and its key is the bare symbol string.** **(S)**

- The state is `self._per_symbol_last: dict[str, float]` (`:58`) — **`symbol -> last placement ts`**. One
  scalar per symbol; the type cannot carry a second dimension.
- The signature is `admit(self, symbol: Optional[str] = None)` (`:65`). **Direction, product, intent,
  strategy and side are not parameters** — all three call sites pass `admit(symbol)` and nothing else.

> ⭐ **This is the same shape as the three symbol gates in H1** *(gate 3 `DUPLICATE_SYMBOL` is
> direction-blind and product-blind; gate 2 is the direction-partitioned slice of it)*. ⇒ **Ruling 2 is
> pipeline-independent and so is the throttle** — a CNC delivery entry and a MIS intraday entry on the
> same symbol contend for **one** 300 s cooldown. **Relevant to OPEN-2: whatever Rama decides about
> *"immediately"*, the throttle will apply it across products, because it cannot do otherwise.**

---

## §8.6 — Q5 · WAS THE THROTTLE EXERCISED IN BOTH PAPER AND LIVE?

### 🏷️ **(d) CANNOT DETERMINE BY OBSERVATION — parity is (I), never (P). ⛔ IT WAS EXERCISED IN LIVE ONLY.** **(P)** for the negative; **(S)/(I)** for the parity claim

**MEASURED, not inferred.** Every retained daily log on the VM, checked for its boot-banner mode:

| | |
|---|---|
| retained `logs/system_*.log` files | **24** (`2026-07-07` → `2026-08-07`, the full 30-day window) |
| days whose boot banner reads `mode=live` | **24 of 24** |
| 🔴 days whose boot banner reads `mode=paper` | **0** |
| days on which the `per_symbol` gate fired | **19 of 24** *(all live)* |

⇒ **The per-symbol cooldown has NOT been exercised in paper within any evidence window available to
me.** ⛔ **This does NOT establish "never in paper"** — 30-day retention means the check can only say
*"not in the last 24 trading days."* **(Absence is bounded by the width of the check.)**

**What supports parity is structural, and it is (I):**
`EntryThrottle` holds no adapter, imports nothing from `broker/`, and its outcome depends only on
`time.monotonic()` and the symbol string; `main.py:3150` constructs it identically regardless of mode;
`signal_processor.py:26` declares *"no direct broker import."* The module docstring asserts
*"Parity: pure in-memory rate logic, identical in paper and live"* — **an assertion, not a measurement.**

> ⭐ **AND THE PARITY HAZARD NAMED IN §7 DOES NOT REACH THIS CONTROL — which is worth saying, because
> it is the one place in this campaign where a paper drill would NOT be vacuously green.** The standing
> hazard is **PAPER NETS BY *SYMBOL* / LIVE KITE NETS PER *(SYMBOL, PRODUCT)*** — it bites anything
> reading broker position quantities. **The throttle reads none.** ⇒ a paper drill of the throttle would
> be genuinely informative. ⛔ **It has not been run, and this report does not propose one.**

---

## §8.7 — THE CARD'S PRE-REGISTERED EXPECTATIONS, SCORED

⭐ **Written by the card's author before any measurement existed. 4 HELD · 0 FAILED · 1 correctly ABSTAINED.**

| # | prediction | score | why |
|---|---|---|---|
| **Q1-P** | **ENTRY → ENTRY** *(moderate confidence, reasoned from "atomic check-and-record")* | ✅ **HELD** | and the stated reasoning was the *correct* reasoning — "records at placement ⇒ no exit hook" is exactly what `:113` does. ⭐ The prediction was right for the right reason, which is the stronger form |
| **Q2-P** | the explanation is Q1's answer **alone**; **no** restart or lost-state involvement | ✅ **HELD — and more strongly than predicted** | lost state is not merely *unsupported*, it is **REFUTED**: a 3-line `systemd[1]` record proves one continuous process across both entries. ⭐ The card asked for the serious alternative to be checked rather than assumed away, and that instruction is what turned an absence into a refutation |
| **Q3-P** | entry→re-entry **exceeds** 300 s; exit→re-entry is the recorded 80 s; **no figure predicted for the entry time** | ✅ **HELD** | 719.644 s and 79.413 s. ⭐ **The abstention was correct discipline** — the entry timestamp was genuinely not in the card, and inventing one would have been unfalsifiable |
| **Q4-P** | product-blind **and** direction-blind, same shape as the symbol gates | ✅ **HELD** | `dict[str, float]` keyed on the bare symbol; `admit(symbol)` takes nothing else |
| **Q5-P** | *no prediction offered — "I have no basis"* | ➖ **CORRECTLY ABSTAINED** | there genuinely was no basis in the card, and the measured answer (live-only, 24/24) could not have been reasoned to |

> ### ⚠️ **AND THE HONEST METHODOLOGICAL READ: THIS SET IS WEAKER EVIDENCE THAN THIS MORNING'S.**
> **A clean sweep of confirmations teaches less about the predictor than P3's failure did.** The card
> says so itself and it is right. ⭐ **The one place these predictions earned their keep is Q2-P**: by
> naming lost in-memory state *in advance* as the more serious alternative, the card forced a check
> that would otherwise have been skipped once candidate 1 already explained everything —
> **and a skipped check would have left "the state was probably fine" where there is now a 3-line proof.**

---

## §8.8 — 🔴 WHAT THIS DECIDES — OPEN-1 AND OPEN-2

> ## ⛔ **THE CARD PRE-COMMITTED THAT THE TWO ANSWERS LEAD TO OPPOSITE RECOMMENDATIONS AND FORBADE SOFTENING WHICHEVER WAS FOUND. THE ANSWER FOUND IS THE EXPENSIVE ONE, AND IT IS RECORDED UNSOFTENED.**

**The finding is ENTRY → ENTRY.** Therefore, in the card's own words: *"gate 1 is the ONLY control
standing between the system and an immediate re-entry after a profitable exit, and Rama is being asked
to remove it."* **That reading is CONFIRMED, and measurement makes it sharper than the card put it.**

**Every control enumerated in H7, tested against the SENCO shape** — *a completed, profitable exit
followed by a same-symbol same-direction re-entry seconds later*:

| control | does it block the re-entry? | why not |
|---|---|---|
| **gate 1 `SYMBOL_DIRECTION_DAILY_LIMIT`** | ✅ **YES — the only one** | its status set includes **`CLOSED`/`CLOSED_MANUAL`**, so a completed trade still counts (H3). **This is the loosening half of Ruling 2** |
| gate 2 `CONTRARY_POSITION` | ⛔ no | requires `PENDING_FILL/OPEN/PARTIAL`; a closed trade has left that set. *(And it has fired **0** times in 109,254 signals)* |
| gate 3 `DUPLICATE_SYMBOL` | ⛔ no | same status set — **released by the exit, by design** |
| **`per_symbol_cooldown_sec: 300`** | ⛔ **no — measured: 719.644 s ≥ 300** | entry-keyed; **dead for 82.2 % of trades by the time they exit** (§8.3) |
| throttle `min_gap` 20 s | ⛔ no | global, and 719 s ≫ 20 s |
| throttle `burst` 3/60 s | ⛔ no | one entry in the window |
| `max_open_positions` 5 · per-strategy concurrency | ⛔ no | **the exit released the slot** — H7's ⭐⭐ point |
| `max_daily_trades` 10 | ⚠️ only at the margin | has not bound since **10-Jul**; H6 measures both affected days reaching **11** |

⇒ **Turning gate 1 off does not fall back onto the cooldown. It falls back onto nothing**, on ~82 % of
trades. ⭐ **And §8.2 adds the fact that most changes the character of the decision: gate 1 was written
and switched on within five hours of the SENCO re-entry, in response to it.** OPEN-1 is therefore not
*"should we relax an incidental legacy rule"* — it is *"should we remove the control this incident
caused, given that measurement now shows nothing else would have stopped it."*

⛔ **THIS IS A MEASUREMENT AND A FRAMING. IT IS NOT A RECOMMENDATION, AND THE DECISION IS RAMA'S.**
The counter-argument remains fully alive and is **not** weakened by anything here: the SENCO report's
own §4 measured the re-entry population at **n=2 over five weeks, total stake ≈ ₹5**, and called it
*"two anecdotes… a rule justified on one blocked trade is a rule justified on nothing."* **A control
can be the only one of its kind and still not be worth its cost.** ⭐ What §8 changes is that the price
of removing it is now **known** rather than assumed.

**FOR OPEN-2 — the one sentence Rama was asked for is now better posed.** Rama's text says a symbol
*"immediately becomes eligible again."* **(P)** The cooldown does not contradict that as a matter of
*ownership* — it never asserts ownership, it spaces dispatches, and §8.4 shows it **defers** a re-entry
by seconds rather than preventing it (PYRAMID re-entered at 300.202 s). ⇒ the two can coexist without
amendment. ⛔ **But that is still a decision, not an inference, and §8 does not take it.**

---

## §8.9 — 🔴 THE BROKER GTT SAFETY CHECK — AND THE CARD'S PREMISE IS **REFUTED**

**⛔ ANSWERED FROM THE BROKER API (`kite.get_gtts()` / `.orders()` / `.holdings()` / `.positions()`),
NOT FROM `gtt_state`, exactly as §3.1 required. NOTHING WAS CANCELLED.**

### ✅ **3.1 — ATULAUTO GTT `330657774`: ABSENT FROM THE BROKER. IT IS GONE.**

**(P)** The broker returns **4** GTTs in total. `330657774` is **not among them**, and **no ATULAUTO GTT
of any status exists at the broker.**

### 3.3 — WHAT CLOSED IT, AND WHEN — traced in the log

| timestamp (IST) | line |
|---|---|
| `2026-08-06 10:02:13.710` | `place_gtt call_end … gtt_id:"330657774"` — placed by `cnc_gtt_monitor.recreated`, `why:"GTT missing; holding intact"` **(the F6 respawn)** |
| `2026-08-07 08:15:41.704` | ⚠️ `cnc_gtt_monitor.forensic … detail:"GTT active but holding flat (external close)"` |
| 🔑 `2026-08-07 08:15:41.722` | **`delete_gtt call_end … gtt_id:"330657774", mode:"LIVE"`** ← **the system cancelled it itself, at this morning's 08:15 boot** |
| `2026-08-07 08:15:41.795` | `cnc_gtt_monitor.gtt_exit … exit_price:579.55, pnl:-9.35` → trade `trd_e66ee17b…` **CLOSED**, `exit_reason='GTT_EXIT'` |

⇒ **The "no manual ATULAUTO buy" DO-NOT can be lifted.** ⛔ **I have NOT lifted it — that is Rama's,
as §3.3 requires.**

### 🔴🔴 **BUT THE CARD'S CLOSING PREMISE IS WRONG, AND IT IS WRONG IN THE DIRECTION THAT MATTERS**

The card wrote that ATULAUTO is *"the only item here that involves real money at the broker tonight."*
**(P) It is not — and it is the one item that is now clean. The live one is `DIFFNKG`.**

**MEASURED AT THE BROKER, 07-Aug ~17:2x IST:**

| source | reading |
|---|---|
| `holdings()` DIFFNKG | **`quantity=0`, `t1_quantity=0`, `realised=0`** — the holding is **FLAT** |
| `positions()` net DIFFNKG | **CNC `net=-1`, `buy=0`, `sell=1`** — a completed SELL, surviving as a **NEGATIVE** row |
| `orders()` DIFFNKG today | **ONE** order: `260807170745584` SELL CNC LIMIT qty 1 **`filled=1` `COMPLETE` at 14:50:52** |
| 🔴 `get_gtts()` | **`330944932` · DIFFNKG · `active` · SELL/SELL · CNC/CNC · triggers `[437.2, 459.45]` · created today `15:20:35`** |
| `trades` row `trd_010f8e21…` | **`OPEN`, `exit_time` NULL** — a **PHANTOM** |

**And the respawn is visible as a sequence** — `gtt_state` for DIFFNKG: `330658430` TRIGGERED (→ the
14:50:52 fill) → `330940420` created **15:05:26**, TRIGGERED 15:08:11 → `330944932` created **15:20:35**,
**ACTIVE now**. *(⚠️ **Stated not chased (G3):** the second trigger at 15:08:11 has **no corresponding
order** in the broker's order book — only one DIFFNKG order exists today. Observed, not explained.)*

> ## 🔴 **THERE IS A LIVE, RESTING SELL GTT AT ZERODHA (`330944932`, DIFFNKG, CNC, triggers 437.2 / 459.45) AGAINST A HOLDING THAT IS ALREADY FLAT AND ALREADY SOLD.**
> **This is F6 cost 4 — "three live SELL GTTs on a flat holding" — measured live, tonight, on the
> symbol the card did not name.** The mechanism is exactly the recorded one: the completed CNC SELL
> survives as `net=-1`, `abs()` at `cnc_gtt_monitor.py:464` reads it as `held=1`, the monitor concludes
> the holding is intact and **recreates the GTT every cycle**.
> ⛔ **NOT CANCELLED — §3.2 and §5 forbid it, and they are right to: cancellation is a live broker
> action and it is not authorised here.** ⭐ **Markets are closed, so nothing can fire tonight; the
> exposure is MONDAY.**
> ⭐ **`MANINFRA` is by contrast CORRECT and needs nothing:** `positions()` CNC `net=+4, buy=4, sell=0`
> — a real position — with one matching `active` GTT `330856765`. ⛔ **Do not sweep it with DIFFNKG.**

---

## §8.10 — WHAT §8 REFUTES IN THE CARD *(the card asked for this explicitly)*

| # | the card said | verdict |
|---|---|---|
| 1 | *"Your own **H1 note** says the throttle state is not persisted"* | ⚠️ **MIS-ATTRIBUTED.** H1 row 5 says only that the cooldown is a *spacing* rule and **LIVE**; it makes **no** persistence claim. The in-memory fact is real but its sources are the **code** (`dict`/`deque` instance attrs, no store) and the 19-Jul throttle report — **not H1.** ⭐ Immaterial to the answer; corrected so a later reader does not go looking for it in H1 |
| 2 | *"A live 300-second cooldown did not stop an 80-second re-entry"* — framed as an unreconciled tension | ⚠️ **DISSOLVED, not resolved.** The throttle never evaluated 80 s; it evaluated **719.644 s**. The two facts were never in tension — they describe **different intervals**, and the 80 s one is measured by **no control in the system** |
| 3 | 🔴 *"ATULAUTO … is the only item here that involves real money at the broker tonight"* | 🔴 **REFUTED.** ATULAUTO is **clean** — the system cancelled its GTT at 08:15:41 today. The real-money item is **DIFFNKG `330944932`, resting and active** (§8.9), which the card did not know about |
| 4 | *(implicit)* SENCO passed gate 1 | 🔴 **REFUTED — gate 1 did not exist yet.** Both halves were authored **3 h 40 min and 5 h 10 min AFTER** the re-entry, the same day (§8.2) |

⭐ **Nothing here refutes the card's core instruction, which was correct and load-bearing:** Q1 was
*"the whole question,"* and it was. **And Q2's demand that lost in-memory state be checked rather than
assumed away is what produced the strongest single piece of evidence in this section.**

---

## §8.11 — WHAT §8 DOES **NOT** ESTABLISH

- ⛔ **Nothing about paper.** The throttle has **not** been exercised in paper in 24 retained trading
  days; parity remains **(I)**. ⛔ "Never in paper" is **not** established — retention is 30 days.
- ⛔ **No recommendation on OPEN-1 or OPEN-2.** §8.8 prices the decision; it does not take it.
- ⛔ **Nothing about whether the 300 s value is right.** Only what it measures **from**.
- ⛔ **No claim that the throttle is defective.** It is not. It did exactly what it is built to do.
- ⛔ **Nothing done about `330944932`.** Reported only. Cancellation, and any F6 work, need their own
  card and Rama's authorisation in his own words.
- ⛔ **The 15:08:11 DIFFNKG trigger with no matching broker order is UNEXPLAINED** and was not chased.

---

## §8.12 — THE PUSH GATES, AND THE FAILURE SET WRITTEN DOWN

**Clock read with PowerShell `Get-Date` per the standing rule.** ⚠️ **The recorded clock hazard is
REFINED, not contradicted, by tonight's reading:** bare `date` in Git Bash returns **correct IST**
(`17:38:36 IST`, matching PowerShell); it is specifically **`TZ=Asia/Kolkata date` that lies**,
printing `12:08:37 GMT` — 5½ h early. **The hazard is the `TZ=` prefix, not Git Bash.**

| gate | result |
|---|---|
| **①** service state | `ActiveState=active · SubState=running · NRestarts=0 · ExecMainStatus=0 · Result=success`. ⚠️ **`active` is tonight's EXPECTED state, not a failure** — a carried delivery position defers `eod_self_exit`. ⛔ **The manual stop and the 17:35 census are RAMA's (`sudo` denied here) and were NOT run** — stated, not silently skipped |
| **②** forward shadow banked | checked, and **NOT satisfied on the first read** (`Aug 6 18:18`, last date `2026-08-06`) ⇒ **waited for the 18:15 cron rather than pushing on a stale artifact** |
| **③** D2 behavioural surface | ✅ **ZERO.** `git diff --name-only origin/main..HEAD` excluding `docs/**` and `*.md` = **0 files**; `-- '*.py'` = 0; `-- '*.yaml' '*.sql'` = 0; and per-commit, **every one of the 14 commits ships 0 non-doc files** |
| **④** tree + remote | ✅ working tree **CLEAN**; `git ls-remote origin main` = `6ae47d0` |
| **⑤** full regression | see below |
| **D6.1** crontab pre-hash | ✅ `b8276da7043975cda2d0ce6578960c6a`, **148 lines / 46 cmds** — identical to the standing baseline |

### GATE ⑤ — `PYTEST_RC=1`, AND THE 9 ARE STRUCTURALLY NOT MINE

**Invocation:** `pytest tests/unit tests/integration`, ⛔ **not `run_tests.py`**, ⛔ **not through a
pipe.** **The rc was captured into a variable immediately (`D5.1 v2`) and read back separately from
the wrapper's own exit code** — the wrapper reported `0` because its last command was a `tail`, which
is precisely the trap `D5.1` exists for.

```
PYTEST_RC=1
===== 9 failed, 5557 passed, 4 skipped, 281 warnings in 880.47s (0:14:40) =====
```

**Counts are IDENTICAL to the two runs recorded last night (9F / 5557P / 4S).**

> ### ⭐ **THE SET, WRITTEN DOWN — because last night recorded *"the set is STABLE"* WITHOUT RECORDING THE SET**
> A stability claim that cannot be re-checked is a count, and **the count is exactly what the 55→29
> episode proved untrustworthy.** These nine are now on record so the next run can do a **true
> set-compare** instead of matching a total:
>
> ```
> tests/unit/test_closure_source_contract.py::test_no_module_restates_the_vocabulary_literals
> tests/unit/test_fix181.py::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active
> tests/unit/test_instance_lock.py::TestSingleInstanceAcrossProcesses::test_p1_second_concurrent_instance_is_refused
> tests/unit/test_instance_lock.py::TestSingleInstanceAcrossProcesses::test_p2_restart_after_crash_is_not_blocked
> tests/unit/test_main.py::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret
> tests/unit/test_main.py::TestContinueFromGate::test_price_hit_calls_placer_with_correct_prices
> tests/unit/test_main.py::TestContinueFromGate::test_no_placer_releases_reservation_and_updates_status
> tests/unit/test_main.py::TestContinueFromGate::test_stats_placed_incremented_on_success
> tests/unit/test_phase17_batch2.py::test_fix077_flask_max_content_length
> ```
>
> ⭐ **`test_instance_lock` p1+p2 is the documented pre-existing full-suite ORDERING artifact**
> (unreaped-`Popen` orphan), already proven on BASE as well as MERGE on 06-Aug.

**ATTRIBUTION IS STRUCTURAL, ⛔ NOT A COUNT-COMPARE:** every executable file in the repo is
**byte-identical to `origin/main`** (0 differing non-doc files), and each of the five failing test
files was checked individually — **all five `IDENTICAL to origin/main`.** ⇒ **no failure in this set
can have been caused by this push.** ⛔ **And they are NOT labelled "known env failures"** — that is a
label, not a diagnosis, and the standing record says not one of them is environmental.

---
---

# §9 · CHATGPT'S REVIEW OF §8 — ADOPTED, 07-Aug-2026 evening · ⛔ DOCUMENTATION ONLY

**The review returned NO material corrections; all seven points are architectural.** ⛔ **None is a
code change and none was implemented as one.** ⭐ **The campaign's own standard is applied to them:
a rule is not adopted until it has been APPLIED and has either BOUND or been AMENDED** — so where a
point could be applied inside this session's own work, it was applied there rather than filed.

| # | point | disposition | outcome |
|---|---|---|---|
| **2.1** | semantic-validation checklist | 🏷️ **APPLIED** — filed as **`M15`** in `docs/campaign_practices.md` **and immediately filled in for all four symbol-keyed controls** | ✅ **BOUND — see below** |
| **2.2** | preserve the residual-protection invariant as a reusable rule | 🏷️ **APPLIED** — `docs/foundation_engineering_rules.md` **§1.14** | ✅ generalised past SENCO; carries the design-time discriminator |
| **2.3** | separate historical motivation from present justification | 🏷️ **APPLIED** — §9.1 below | ✅ **BOUND — it caught a claim in my own §8.8** |
| **2.4** | DIFFNKG replaces ATULAUTO as the primary F6 example | 🏷️ **APPLIED** — §9.2 below, **superseded not erased** | ✅ |
| **2.5** | document the dependency chain once | 🏷️ **APPLIED** — §9.3 below | ✅ |
| **2.6** | evidence-STRENGTH tags | 🏷️ **APPLIED** — prefix **`X1/X2/X3+`** chosen; collision named | ⚠️ **AMENDED — the proposed `E1/E2/E3` collided** |
| **2.7** | the unmeasured half of OPEN-1 | 🏷️ **APPLIED** — §9.4 below, **as a finding, ⛔ not a caveat** | 🔴 **the sharpest of the seven** |

## §9.1 — 2.3 · HISTORY IS NOT JUSTIFICATION — **and this BOUND against my own §8.8**

Two claims, and they must never be used to settle one another:

| | claim | status |
|---|---|---|
| **HISTORICAL** | *Gate 1 was created by SENCO* — `656b62d` 13:54:12 and `300a247` 15:24:31, both **+3 h 40 m / +5 h 10 m after** the 10:14:12 re-entry | **(P) SETTLED FACT.** ⛔ It says nothing about whether the gate should remain |
| **PRESENT** | *Should gate 1 remain?* | 🔴 **OPEN. Rama's. ⛔ Not settled by anything in this report** |

> ### ⭐ **IT BOUND IMMEDIATELY — §8.8 SAILS CLOSE TO THE LINE AND IS CORRECTED HERE, NOT QUIETLY EDITED**
> §8.8 wrote: *"OPEN-1 is therefore not 'should we relax an incidental legacy rule' — it is 'should we
> remove the control this incident caused…'"*. ⚠️ **That sentence uses the historical claim to shape
> the present decision.** The origin fact is legitimate **context** — it refutes "incidental legacy
> rule" as a *description* — but ⛔ **"SENCO caused it" is NOT an argument that it should stay.**
> A control created in response to a single incident may still be the wrong control; **`n=2` re-entries
> over five weeks, total stake ≈ ₹5, is the counter-case and it is undiminished by the origin story.**
> 🏷️ **The claim stands as history; its use as justification is withdrawn.**

## §9.2 — 2.4 · **DIFFNKG SUPERSEDES ATULAUTO AS THE PRIMARY F6 OPERATIONAL EXAMPLE** — ⛔ supersede, do not erase

| | ATULAUTO `trd_e66ee17b…` | **DIFFNKG `trd_010f8e21…`** |
|---|---|---|
| status | **CLOSED HISTORY** — resolved at the 07-Aug 08:15 boot | 🔴 **LIVE, broker-confirmed 07-Aug ~17:2x** |
| role | ⭐ **the ONLY observed FULL RESOLUTION of an F6 phantom** | **the primary example** — phantom `OPEN`, flat holding, resting GTT |
| ⛔ **why it is KEPT** | **E2 and E3 of the Monday card depend on it** — it is the sole precedent for `positions()` returning `0 positions` pre-market, and the sole precedent for the fabricated exit price | — |

⇒ **Cite DIFFNKG for *what F6 does*; cite ATULAUTO for *how it ends*.** ⛔ **Deleting the ATULAUTO trace
would destroy the only evidence the Monday predictions rest on.**

## §9.3 — 2.5 · THE DEPENDENCY CHAIN, WRITTEN ONCE

> ## **BROKER TRUTH → F6 CORRECTNESS → `trades.status` INTEGRITY → GATE 2 / GATE 3 CORRECTNESS → THE GOVERNANCE DECISION**

| link | what breaks it | evidence |
|---|---|---|
| broker truth → F6 | `abs(int(qty))` at `cnc_gtt_monitor.py:464` reads a completed CNC SELL (`net=-1`) as `held=1` | **(P)** DIFFNKG, live now |
| F6 → `trades.status` | `held == 0` is the **sole** door to `_finalize_gtt_exit` (`:487`, `:501-510`) ⇒ the trade never leaves `OPEN` | **(S)** + **(P)** |
| `trades.status` → gates 2/3 | both read `status IN ('PENDING_FILL','OPEN','PARTIAL')` — a phantom `OPEN` **is** an open position to them | **(S)** |
| gates 2/3 → the decision | Ruling 2 is implemented **by** gates 2/3 (H3), so it inherits every defect above | **(S)** |

> ⇒ 🔒 **THIS IS WHY THE SEQUENCING REVERSED. A gate can be perfectly implemented and still be wrong,
> because its DATA SOURCE is wrong.** ⭐ **F6 is not a beneficiary of Ruling 2; it is its prerequisite** —
> and the chain, not the argument, is the reason.

## §9.4 — 2.7 · 🔴 **THE UNMEASURED HALF OF OPEN-1 — recorded as a FINDING, ⛔ not a caveat**

> ## ⭐⭐ **H6 MEASURED THE PROTECTION LOST BY REMOVING GATE 1. IT DID NOT MEASURE THE OPPORTUNITY GAINED. THE DECISION NEEDS BOTH, AND ONLY ONE EXISTS.**

| half | measured? | what exists |
|---|---|---|
| **protection LOST** | ✅ **YES** | H6: **9** rejections would be permitted, 2 days, 4 symbols; both days reach **11** against `max_daily_trades = 10`; §8.3: the cooldown's residual is **zero on 82.2 %** of trades |
| 🔴 **opportunity GAINED** | ⛔ **NO — NOT MEASURED, AND NOT MEASURABLE FROM THIS SAMPLE** | — |

**⛔ WHY IT CANNOT BE CLOSED FROM WHAT WE HAVE — stated plainly rather than estimated:**
- The population is **9 rejected signals over 2 trading days, 4 symbols**, and **9 signals ≠ 9 trades**
  (`SUDEEPPHRM` ×2, `DECNGOLD` ×3, `MAYURUNIQ` ×3 — the realistic floor is **4** distinct symbols).
- ~~⛔ **A rejected signal has no outcome.** There is no fill, no exit, no P&L — so the profit those
  entries *would* have made is **not recoverable from the record at all**, at any sample size.~~
  🔴 **STRUCK 07-Aug LATE — THIS CLAIM IS FALSE. See the correction immediately below.**
- ⛔ **`n` of this size cannot separate signal from noise in either direction.** The SENCO report already
  established the same limit on the mirror question: re-entries are **n=2, ≈₹5 over five weeks** —
  *"a rule justified on one blocked trade is a rule justified on nothing."* **⭐ This limb STANDS.**

> ## 🔴🔴 **CORRECTION, 07-Aug-2026 LATE — I WAS WRONG, AND IT IS THE MOST DECISION-RELEVANT ERROR IN THIS REPORT**
> **§9.4 asserted that the opportunity side is *"not recoverable from the record at all, at any sample
> size."* THAT IS FALSE, AND IT WAS FALSE WHEN WRITTEN. (P) MEASURED:**
>
> | | |
> |---|---|
> | gate-1-rejected `signal_id`s in `signals` | **65** |
> | **of those, present in `data_store/v3/forward_shadow_fs-v1.jsonl`** | 🔑 **65 — ALL of them** *(width: all 63,506 shadow lines scanned)* |
> | **rows carrying a NON-NULL `sim_R`** | 🔑 **65. Zero nulls.** |
> | the shadow's own `decision` field on those rows | `REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT` ×65 — **the shadow tags them explicitly** |
> | dates covered | `2026-08-03` → `2026-08-07`, **5 trading days** |
>
> ⇒ ⭐⭐ **THE MEASUREMENT INSTRUMENT ALREADY EXISTS, IS ALREADY RUNNING, AND IS ALREADY CAPTURING
> EXACTLY THIS POPULATION.** The forward-shadow recorder simulates an outcome (`sim_R`) for signals the
> live system rejected — **which is precisely the counterfactual §9.4 declared unavailable.**
> ⛔ **The error was mine: I reasoned "a rejected signal has no outcome" from the live path and never
> checked the shadow path, despite the shadow being the campaign's established OOS instrument** *(it is
> what tested D3, and its `wrote=` counts are gated at every push)*. 🏷️ **`M8` — read the record before
> concluding from it.**
>
> ### ⛔⛔ **AND NOW THE DISCIPLINE, BECAUSE THIS NUMBER IS SEDUCTIVE AND MUST NOT BE ACTED ON**
> **(P) over the 65: `sum = +3.329R`, `mean = +0.0512R`, wins 33 / losses 32.** ⛔ **DO NOT READ THAT
> AS "the blocked trades were profitable."** Four reasons, each independently sufficient:
> 1. 🔑 **WRONG POPULATION.** All 65 are **gate-1** rejections. **Under Ruling 2, 56 of them would still
>    be rejected** (a position *was* open — H6). **The decision-relevant subset is the 9**, not the 65.
> 2. **`+0.0512R` mean is indistinguishable from zero** at n=65, and a 33/32 split is a coin.
> 3. 🔑 **`sim_R` IS A SIMULATION, NOT A FILL.** It models neither the LIMIT-fill mechanism — **(P)** the
>    live book fills ~**48 of 78** placed entries — nor slippage guards, nor the entry throttle, nor
>    `max_daily_trades`. **The realisable subset is strictly smaller than the simulated one.**
> 4. **5 trading days.**
>
> ⇒ 🔑 **THE CORRECT RESTATEMENT: OPEN-1 is not undecidable — it is UNDER-SAMPLED. The instrument
> exists; what is missing is `n` and a pre-registered threshold.** ⭐ **That is a far better position
> than §9.4 described, because under-sampled is a condition that TIME FIXES and unmeasurable is not.**
> ➡️ **This is what the OPEN-1 decision record in `Downloads/DECISION_RECORDS_OPEN-1-2-4_07Aug2026.txt`
> is built on.**

> ### ⚠️ **THE ONE ADJACENT FIGURE — AND IT POINTS THE OTHER WAY WITHOUT BEING AN ANSWER TO THIS QUESTION**
> The book's first-entry population runs **~38–39 % win against a ~43.5 % breakeven** *(24-Jul entries
> work; corroborated independently by the SENCO cut at **40.3 %**, n=181)*. **On that base rate the
> average additional entry is negative-expectancy**, which argues that the opportunity gained is
> **negative** — i.e. gate 1 is doing good by blocking them.
> ⛔⛔ **BUT THAT IS NOT AN ANSWER TO THIS QUESTION, AND MUST NOT BE USED AS ONE.** It describes **all
> first entries**, not the specific sub-population gate 1 rejects — **same-symbol, same-direction,
> same-day re-entries**, which may be systematically better or worse than the book. **Nothing measures
> that sub-population's expectancy, and 9 signals never will.**
> ⇒ 🔑 **OPEN-1 is a decision under genuine one-sided evidence: the cost of removal is measured, the
> benefit is not, and the only nearby number is suggestive against removal while being formally silent.**
> ⛔ **Recorded so the asymmetry is visible to whoever decides — NOT resolved.**

---
---

# §10 · THE SECOND REVIEW ROUND — 16 POINTS, 07-Aug-2026 late · ⛔ DOCUMENTATION ONLY

**⭐ The campaign standard again: a point is not adopted until APPLIED, and it has BOUND or been
AMENDED.** ⛔ **Filing all sixteen and calling that adoption is exactly what the standard forbids.**

| # | point | disposition | outcome |
|---|---|---|---|
| 2.1 | predicate correctness vs operational dependency | **APPLIED** — §10.1 | 🔴 **AMENDED my own conclusion** |
| 2.2 | dependency CLASSES, applied to §9.3 | **APPLIED** — §10.1 | 🔴 **BOUND — the F6 edge is class D, and I wrote it as if it were A** |
| 2.3 | post-F6 residual risks | **APPLIED** — F6 design **§16** | ✅ R-5 was already Invariant A |
| 2.4 | invariants as regression targets | **APPLIED** — F6 design **§17** | ⭐ **BOUND by REFUSING 2 of 3 as restatements** |
| 2.5 | X-tags applied consistently? | **APPLIED** — §10.3 | ⚠️ **NO — and where is stated** |
| 2.6 | new failure modes if gate 1 is removed | **APPLIED** — §10.2 | 🔴 **the mirror of §9.4, and it IS analysable** |
| 2.7 | recovery philosophy vs foundation §1.12 | **APPLIED** — `foundation_engineering_rules.md` §1.12 amended | ✅ binds future work, not just F6 |
| 2.8 + 3.7 | the Monday artifact | **APPLIED** — **ONE** table, in the Monday card | ✅ built once, not twice |
| 3.1 · 3.2 · 3.6 · 3.8 | decision-record structure, rollback cost, success/rollback/re-validation | **APPLIED** — the §4 draft (`Downloads/`) | ✅ |
| 3.3 | F6-first is today's dependency | **APPLIED** — folded into §10.1, ⛔ written once | ✅ cross-referenced, not duplicated |
| 3.4 | OWNERSHIP vs SCHEDULING vocabulary | **APPLIED** — §10.4 + `M15` | ✅ |
| 3.5 | `CONTRARY_POSITION` activation condition **at the source** | ⚠️ **PARTIALLY APPLIED — §10.5** | 🔴 **BLOCKED BY THE CARD'S OWN §6** |

## §10.1 — 2.1 + 2.2 + 3.3 · **DEPENDENCY CLASSES — and this BOUND against my own §9.3**

**The classes:** **A · LOGICAL** *(the conclusion cannot be true without it)* · **B · DATA**
*(correct only if the data source is correct)* · **C · OPERATIONAL** *(safe to do only in this order
today)* · **D · TEMPORARY-IMPLEMENTATION** *(an artefact of the current implementation; a different
implementation removes the edge)*.

**§9.3's chain, re-labelled:**

| edge | class | why |
|---|---|---|
| broker truth → F6 correctness | **B · DATA** | F6 *is* a misreading of broker data |
| F6 → `trades.status` integrity | **B · DATA** | a wrong `held` writes a wrong status |
| `trades.status` → gates 2/3 correctness | **B · DATA** | the gates are correct predicates over a corrupt source |
| 🔑 **F6 → Ruling 2 (*"F6 first"*)** | 🔴 **D · TEMPORARY-IMPLEMENTATION** | — |

> ### 🔴🔴 **THE HONEST ANSWER IS D, AND IT WEAKENS A CONCLUSION I WROTE TODAY. SAYING SO IS THE POINT.**
> §8/§9 stated **"F6 IS A PREREQUISITE OF RULING 2"** in a form that reads as **class A — logical,
> permanent, architectural.** ⛔ **It is not.**
> **Ruling 2 is LOGICALLY independent of F6.** Its predicate is *"does an open position exist for this
> symbol right now?"* — a question about the **account**. **F6 only matters because the current
> implementation answers that question from `trades.status`**, and `trades.status` is what F6 corrupts.
> ⇒ **a broker-truth predicate replacing `trades.status` would remove the F6→Ruling-2 edge entirely** —
> the dependency is on the **chosen data source**, not on the ruling.
> ⭐ **What survives unchanged:** *given the implementation that exists today*, F6 must land first —
> **class C/D, and operationally binding.** ⛔ **What does NOT survive: any reading of "F6 first" as an
> architectural law.** 🏷️ **Unclassified, it would have hardened into doctrine within a week** — which
> is precisely what 2.2 predicted, and why the classes were worth introducing.
> ⚠️ **AND THE HONEST CAVEAT ON THE ESCAPE ROUTE:** H4 measured that broker truth is **not reachable at
> the gate** (no adapter on `RiskEngine`; `positions()` blind to delivery from T+1, `holdings()` blind
> to intraday), and H5b measured that writing one in the house style would **reproduce F6 at a new
> site**. ⇒ **the class-D edge is real and currently unavoidable — it is just not permanent.**

## §10.2 — 2.6 · 🔴 **THE MIRROR OF §9.4 — WHAT NEW FAILURE MODES BECOME REACHABLE IF GATE 1 IS REMOVED**

> ⭐⭐ **§9.4 proved the *opportunity* side is unmeasurable from the record. THIS question is different
> and it IS analysable** — reachability is a property of the live control set, not of outcomes that
> never happened. ⛔ **Governance completeness, NOT a recommendation.**

| # | failure mode | reachable today if gate 1 is off? | what bounds it | 🔎 what it would look like in the record |
|---|---|---|---|---|
| **F-1** | **RAPID SAME-DAY CHURN** — repeated enter/exit on one symbol | 🔴 **YES, and it is the SENCO shape by construction** | only `per_symbol_cooldown_sec` (300 s) and `max_daily_trades` (10). **(P)** the cooldown's residual is **zero on 82.2 %** of trades, and the cap **has not bound since 10-Jul** | ≥3 trades on one symbol+direction in a day; `trades` rows with short gaps; **(P)** H6 already shows `DECNGOLD`×3 and `MAYURUNIQ`×3 in the permitted set |
| **F-2** | **CAPITAL OSCILLATION** — reserve/release churn on one symbol | ⚠️ **PARTIALLY** — the money is bounded, the *churn* is not | `max_open_positions` (5) and the bucket split bound **exposure**; nothing bounds **reservation turnover** | repeated `RESERVE`/`RELEASE_USED` pairs for one symbol in `fm_ledger`; **⚠️ and the 10 % in-session drift band is ₹50 FLAT overnight** ⇒ churn near the close could alarm all night |
| **F-3** | **STRATEGY FEEDBACK LOOP** — a scanner re-firing into its own exit | 🔴 **YES — and the mechanism is MEASURED, not hypothesised** | ⛔ **nothing.** **(P)** the SENCO record: `open_low_breakout_long` fired SENCO every ~5-6 min all morning, held back **only** by the open-position guard, which **releases the instant the position closes** | a continuous `REJECTED_STRATEGY_POSITION_LIMIT` stream that converts to `PROCESSED` the moment a trade closes — **(P) exactly the 10:08→10:14 transition already on record** |
| **F-4** | **TRIGGER-QUALITY DECAY** *(not named in the review; added)* | 🔴 **YES** | — | **(P)** SENCO's two entries both scored **exactly 60** against `min_pass_score: 60`, and the same scanner scored **59** for the rest of the morning ⇒ **re-entries concentrate at the score threshold**, where the 24-Jul work measured the edge to be worst |

> ### 🔑 **THE PATTERN ACROSS ALL FOUR: EVERY ONE IS BOUNDED ONLY BY CONTROLS THAT H7 MEASURED AS NOT CURRENTLY BINDING.**
> `max_daily_trades` last bound **10-Jul**; the cooldown's residual is zero on ~82 %; the concurrency
> caps are **released by the exit**, which is the very event that starts each of these modes. ⇒
> **removing gate 1 does not merely re-admit a trade class — it re-admits it into a control set with no
> live binding constraint.** ⛔ **Still not a recommendation.** ⚠️ **And F-1/F-3 are the two the
> `n=2, ≈₹5` counter-case does NOT address**, because that case measures *realised cost of past
> re-entries*, not *reachability of a mode*.
> 🧪 **PARITY: F-1, F-2 and F-4 are paper-exercisable** (all internal — signal flow, sizing, ledger).
> ⛔ **F-3 is NOT reliably paper-exercisable** — it depends on live scanner arrival timing, which paper
> replays rather than generates.

## §10.3 — 2.5 · X-TAGS: **APPLIED CONSISTENTLY IN THE MONDAY CARD, ⛔ NOT ELSEWHERE**

**(P)** `X1/X2/X3+` appears on **every** prediction in `MONDAY_10-Aug-2026_PREDICTION.md` (E1 X3+ ·
E2 X2 · E3 X2 · E4 X1 · E5 X1 · E6 X1). ⛔ **It is NOT applied to §8's H1–H7 verdicts, §9, or this §10** —
those carry **(P)/(S)/(I)** only. **Stated rather than quietly left uneven:** retro-fitting X-tags to
§8 would mean re-deriving source counts for verdicts already written, which is a measurement wearing a
formatting change's clothes. 🏷️ **The convention is adopted going forward; the back-fill is NOT done
and is NOT owed.**

## §10.4 — 3.4 · THE VOCABULARY: **OWNERSHIP** vs **SCHEDULING**

> **OWNERSHIP CONTROL** — answers *"may this symbol be held at all?"* Gates **1, 2, 3**. State lives in
> `trades`, DB-backed, survives restart; released by a **position** event.
> **SCHEDULING CONTROL** — answers *"may this order go out NOW?"* The **entry throttle** (`min_gap`,
> `burst`, `per_symbol_cooldown`). State in memory, dies on restart; released by a **clock**.

⭐ **This is `M15`'s finding given a name, and the name is the part that stops the confusion recurring.**
⛔ **A scheduling control can never substitute for an ownership control** — it does not know what is
owned; it only knows when we last spoke. ⚠️ **The 300 s cooldown was discussed for weeks as partial
ownership cover precisely because no vocabulary distinguished the two.**

## §10.5 — 3.5 · `CONTRARY_POSITION`'s ACTIVATION CONDITION — ⚠️ **RECORDED HERE, ⛔ NOT PLACED AT SOURCE**

**THE CONDITION, written so a future reviewer cannot mistake the gate for dead code:**

> ### 🔒 **`CONTRARY_POSITION` (`capital/risk_engine.py:665-686`) is UNREACHABLE-BY-CONSTRUCTION, ⛔ NOT DEAD.**
> **(P)** 0 fires in 109,254 signals — **because gate 3 (`DUPLICATE_SYMBOL`) is unconditional and
> rejects any active position first**, so gate 2 can only ever claim a slice gate 3 has already taken.
> ### ⭐ **ACTIVATION CONDITION: it becomes meaningful the moment gate 3's scope NARROWS** — e.g. if
> `DUPLICATE_SYMBOL` is ever made direction-aware, product-aware, or pipeline-scoped. **At that moment
> gate 2 becomes the only thing preventing a simultaneous long and short in one symbol.**
> ⛔ **Deleting it as dead code would remove a protection whose absence would not be noticed until the
> day gate 3 is narrowed.**

### 🔴 **AND THE CARD ASKED FOR THIS AT THE SOURCE — I HAVE NOT DONE THAT, AND THE REASON IS THE CARD ITSELF (see also §11.6: the conflict is now ROUTED to Rama as an explicit ask)**
Point 3.5 says *"put the condition at the source, not only in a report."* ⛔ **The same card's §6 says
"Do not alter or retire `CONTRARY_POSITION` in code."** A source comment **is** an edit to
`capital/risk_engine.py` — inert at runtime, but an edit to a capital-path file, in a session that is
docs-only and whose commits are held unpushed. ⇒ 🏷️ **§6 OUTRANKS 3.5 and the condition stays in
documentation.** ⭐ **Flagged rather than silently resolved either way** — and it is a real gap:
**a reviewer greps the code, not this report.** 🔴 **OWED: a one-line source comment carrying this
condition, needing its own authorisation.**

---
---

# §11 · 🔴🔴 RE-VERIFICATION FOR RAMA'S GTT DECISION — **HIS CHOICE RESTED ON A FALSE PREMISE**

**07-Aug-2026 night · READ-ONLY · measured at HEAD `c10e700`.**
**⛔ `330944932` NOT cancelled. Nothing staged. This changes the DECISION INPUTS, not the state.**

> ## ⚠️ **WHY THIS EXISTS: I put a two-branch trade-off to Rama and the first branch was wrong.**
> I wrote *"CANCEL ⇒ the chain is closed at zero cost if E2 holds."* **That is false.** My own F6
> design recorded the refutation at §15.1 on 06-Aug and **I did not consult it before framing the
> choice.** 🏷️ **`M8` — and this is the SECOND `M8` failure in one day**, the first being §9.4's
> measurability claim. ⭐ **Same shape twice: reasoning forward from what was in front of me instead
> of reading the record that already held the answer.**

## §11.1 — Q1 · **DOES THE LADDER STILL BEHAVE AS §15.1 RECORDS?**
### 🏷️ **(b) CONFIRMED DESIGN — §15.1 HOLDS AT HEAD, and every line number is EXACT.** **(S)** · **X2**

**(P) `orders/cnc_gtt_monitor.py` is BYTE-IDENTICAL to `0197923`** — `git diff --quiet 0197923..HEAD --
orders/cnc_gtt_monitor.py` returns clean ⇒ the citations are not merely still valid, **the file has not
moved at all.** Line numbers re-measured at `c10e700`, ⛔ not inherited **(M3)**:

| §15.1 cited | at HEAD | the condition, quoted |
|---|---|---|
| `:486` | ✅ **486** | `if triggered:` |
| `:492` | ✅ **492** | `if present_active and held == row_qty:` |
| `:497` | ✅ **497** | `if held > 0 and held != row_qty:` |
| `:501` | ✅ **501** | `if held == 0:` |
| `:513` | ✅ **513** | `if held == row_qty:` |
| — | **514 / 517** | `if in_hours:` → `_recreate` · **else** → `_queue_preopen(r, held)` |
| — | **477** | `if r["needs_review"]:` → stand down, no action |

## §11.2 — Q2 · **GTT ABSENT, `held = 1`, `row_qty = 1` — WHICH BRANCH FIRES?**
### 🏷️ **(a) CONFIRMED — `:513` fires. Cancelling REBUILDS it.** **(S)** · **X2**

`bg = broker_gtts.get(gid)` → `None` ⇒ `triggered = False`, `present_active = False`:

| branch | test | result |
|---|---|---|
| `:486` | `triggered` | ⛔ False |
| `:492` | `present_active and held == row_qty` | ⛔ False — `present_active` is False |
| `:497` | `held > 0 and held != row_qty` | ⛔ `1 > 0` true **but `1 != 1` is FALSE** |
| `:501` | `held == 0` | ⛔ `1 == 0` False |
| 🔑 `:513` | `held == row_qty` | ✅ **`1 == 1` — TRUE, FIRES** |

⇒ **`in_hours` decides only the FORM:** `True` → `_recreate` at once; `False` → `_queue_preopen` plus a
`WARNING`, returning `queued_preopen:DIFFNKG`.

## §11.3 — Q3 · **WHEN DOES THE QUEUED REBUILD EXECUTE?** ⇒ 🔴 **IN MARKET HOURS**
### 🏷️ **(a) CONFIRMED — the rebuild lands AFTER the open, not at the boot.** **(S)** · **X2**

**(S)** `main.py:2752` `_market_hours_fn = lambda: market_windows.is_market_open(_now_ist_mh())`,
passed at `:2763`. `reconcile()` sets `in_hours = bool(self._in_hours())` (`:109-110`), and
`:117-118` reads `if in_hours and self._preopen_queue: actions.extend(self._drain_preopen())`.

⇒ at the **08:15 boot the market is shut** ⇒ `in_hours = False` ⇒ the row is **queued, not rebuilt**.
The queue drains on the **first reconcile cycle where `is_market_open()` is True — at/after 09:15** ⇒
🔴 **a cancelled GTT is REPLACED DURING MARKET HOURS, about an hour after the boot.**

## §11.4 — Q4 · **WHAT TRIGGERS WOULD A REBUILT GTT CARRY?** ⇒ **THE SAME ONES**
### 🏷️ **(b) CONFIRMED DESIGN — a rebuild is trigger-equivalent.** **(S)** + **(P)** · **X3+**

**(S)** `_recreate` (`:615-618`) passes `sl_price=float(r["sl_trigger"])` and
`tgt_price=float(r["tgt_trigger"])` — **read from the persisted `gtt_state` row, not re-derived.** Only
the LTP is fresh (Y3, a Kite field requirement).
**(P) PROVEN ON THIS EXACT SYMBOL:** all three DIFFNKG GTTs — `330658430` (original) and `330940420` +
`330944932` (**both built by `_recreate`**) — carry **identical `trigger_values [437.2, 459.45]`**,
while their `last_price` differed (`438.75` at 15:05:26 vs `440.6` at 15:20:35).
⇒ ⛔ **The replacement is NOT a materially different order.** The cost of cancelling is **timing,
identity, and the forensic record** — not a changed trigger.

## §11.5 — 🔑 **THE DECISION MATRIX — BOTH BRANCHES OF THE CHOICE I PUT TO RAMA COLLAPSE**

| | **`held = 0` (E2 HOLDS)** | **`held = 1` (E2 FAILS)** |
|---|---|---|
| **IF CANCELLED over the weekend** | `:501` → `present_active` False → **`:510` finalize** ⇒ trade closes ✅ **but ⛔ the `orphan_active_gtt_flat` FORENSIC LOG and the `delete_gtt` record are NEVER WRITTEN** | 🔴🔴 `:513` → `in_hours` False → **`_queue_preopen`** → drains **09:15+** ⇒ **A NEW GTT IS CREATED IN MARKET HOURS** |
| **IF LEFT ALONE** | `:501` → `present_active` True → **`:505` forensic → `:507` `delete_gtt` → `:508` finalize** ⇒ trade closes ✅ **with the full forensic trail** | `:492` → **`healthy:DIFFNKG`** ⇒ rests unchanged (**this is E4**) |

> ## ⛔⛔ **CONCLUSION: CANCELLING IS REDUNDANT IN ONE BRANCH AND ACTIVELY WORSE IN THE OTHER. IT IS A "ZERO-COST CLOSE" IN NEITHER.**
> - **E2 holds** ⇒ the system deletes it **itself** at 08:15 — **(P)** precisely what happened to
>   ATULAUTO at `08:15:41.722`. Cancelling first changes nothing **except losing the forensic record**,
>   which is the artifact that documented that resolution and on which **E2 and E3 both rest**.
> - **E2 fails** ⇒ cancelling **manufactures** the `:513` condition and buys a **brand-new GTT created
>   during market hours** — plausibly worse than one resting quietly since Friday.
> - **In both branches it destroys E5's only observation.**
>
> ⇒ ⭐ **On the measured mechanics, DOING NOTHING dominates cancelling in every cell.**
> ⛔⛔ **That is an ANALYSIS, NOT A DECISION — and it is NOT an authorisation to leave it either.**
> Rama may weigh the tail risk of a live trigger above every mechanical consideration here, and that
> remains entirely his call. **The analysis narrows the question; it does not answer it.**

### 🔴🔴 **THE MATRIX IS ONE-DIMENSIONAL AND WILL BE MISREAD — SO THE SECOND DIMENSION IS STATED *IN* IT, NOT BESIDE IT**

> ⚠️ **Every cell above compares MECHANICS. The tail risk of a live trigger is in NONE of them.**
> ⭐ A later reader will see the table and not the sentence under it, so the two axes are named here:

| axis | what it measures | where the matrix stands |
|---|---|---|
| **① MECHANICAL DOMINANCE** | does cancelling achieve what it is supposed to achieve? | ✅ **ANSWERED: no.** Redundant if E2 holds *(and it loses the forensic record)*; counter-productive if E2 fails *(a new in-hours GTT)*. **This is what the matrix measures, and it is ALL the matrix measures** |
| **② DECISION DOMINANCE** | expected value of the observation **vs** the cost of a low-probability catastrophic branch | 🔴 **NOT ANSWERED, AND NOT ANSWERABLE HERE.** E5 is `CANNOT DETERMINE` — outcome **C** *(a live sell for stock we do not own ⇒ short delivery + auction settlement)* has **no measured probability**. ⛔ A branch whose probability is unknown cannot be traded off against a certain small gain |

> ## ⛔⛔ **THEREFORE: *"DOMINATES IN EVERY CELL"* IS A STATEMENT ABOUT MECHANICS. IT IS ⛔ NEVER A RECOMMENDED ACTION.**
> **A rational person may cancel purely to close axis ②, accepting every axis-① cost — including the
> new in-hours GTT — because they decline to hold an unquantified tail over a weekend.** ⭐ **That is
> not a mistake and this report does not argue against it.** What the report establishes is only that
> **cancelling does not buy what it was believed to buy on axis ①**, so the choice should be made on
> axis ② with axis ① priced correctly — ⛔ **not on the false premise I originally supplied.**

## §11.6 — Q5 · **ANY SEQUENCE THAT DURABLY REMOVES THE GTT WITHOUT F6?**
### 🏷️ **NO *OPERATOR-INITIATED* PATH — ⭐ BUT ONE SYSTEM PATH EXISTS AND IS OBSERVED TO WORK.** **(S)** + **(P)** · **X2**

| # | candidate | verdict |
|---|---|---|
| 1 | cancel at the broker | 🔴 **NO** — respawns via `:513` whenever `held ≠ 0` (§11.2) |
| 2 | latch `gtt_state.needs_review = 1` (`:477` stands the row down entirely) | ⛔ **NO SUPPORTED PATH.** `set_gtt_state_needs_review` exists (`core/state_store.py:2272`) but **(P) its only callers are inside `cnc_gtt_monitor` itself** — `_recreate`'s failure path and `_qty_mismatch`. *(Width: repo-wide grep over `scripts/`, `core/`, `orders/`.)* Reaching it means raw DB manipulation, which **foundation §1.12 explicitly excludes as a recovery path** |
| 3 | delete the `gtt_state` row | ⛔ same — raw DB manipulation |
| 4 | the nightly manual stop | ⛔ **NO** — it stops the **monitor**, not the **GTT**; the order keeps resting at Zerodha |
| 5 | operator tooling in `scripts/` | ⛔ **NONE EXISTS.** **(P)** the only GTT script is `t2_cnc_gtt_realtest.py`, which **places REAL orders** and is prohibited |
| 6 | ⭐ **the system's own 08:15 boot, once `held` reaches 0** | ✅ **YES — DURABLE, AND OBSERVED.** `:501` → `:505` → `:507` → `:508`. **(P)** it resolved ATULAUTO on 07-Aug at `08:15:41.722` — GTT deleted, trade closed |

> ### ⭐ **THE REFINEMENT, AND IT IS NOT A FLAT "NO":**
> **No *operator-initiated* durable removal exists without F6 — §15.1's conclusion stands.** ⭐ **But
> the system already owns a durable path (candidate 6), it has been observed to work exactly once, and
> E2 predicts it fires on Monday.** ⇒ **The honest thing to tell Rama is not "you have no options" but
> "the option that works is the one requiring you to do nothing — and E2 is the bet you take by
> choosing it."**
> ⚠️ **THE LIMIT ON THAT, STATED: candidate 6 is conditional on `held == 0`, which is exactly what E2
> predicts and what has NEVER been observed across a weekend.** ⛔ **It is not a guarantee.**

### 🧪 **PARITY — at the item, ⛔ not left to silence**
**Every path in §11 is LIVE-ONLY.** The ladder reads `holdings()` + CNC rows of `positions()`; **paper
nets by *symbol* while live Kite nets per *(symbol, product)*, and the paper adapter has NO T+1
settlement model**, so the `-1` residue that produces `held = 1` **cannot exist in paper**. ⇒ ⛔ **a
paper drill of §11.2 would be VACUOUSLY GREEN** — it would take `:501` every time and never reach
`:513`. **No paper claim is made anywhere in this section.**

## §11.7 — THE PRE-REGISTERED EXPECTATION, SCORED

| prediction | score | why |
|---|---|---|
| *"§15.1 will HOLD at HEAD"* *(stated at moderate confidence)* | ✅ **HELD — more strongly than the confidence implied** | the file is **byte-identical** to `0197923`, so every cited line number is exact rather than merely still valid |
| *"Q5 = NO — no durable cancellation exists without F6"* | ✅ **HELD, with a REFINEMENT that improves Rama's position** | no **operator-initiated** path exists ✅. ⭐ **But the framing missed candidate 6** — the system's own boot path is durable and is what resolved ATULAUTO. **"You have no option" would have been the wrong thing to tell him** |

⭐ **The instruction to say so if refuted was right, and it half-fired:** the expectation held, but
demanding an *enumeration* rather than a yes/no surfaced the one path the question's framing excluded.
🏷️ **A question that presumes its own answer will get it; Q5 asked for the list, and the list caught
candidate 6.**

---
---

# §12 · 🔑 **THE SHARED DEPENDENCY — NAMED ONCE, BECAUSE FOUR CONCLUSIONS FAIL TOGETHER**

> ## **`SD-1` · THE WEEKEND / SETTLEMENT BEHAVIOUR OF `positions()` — specifically, whether a Friday CNC SELL's `-1` day-book row is GONE by Monday's pre-market read.**

**⛔ Repeating this assumption inside each finding HIDES that they are one assumption.** Written once:

| depends on `SD-1` | how it depends | if `SD-1` is WRONG |
|---|---|---|
| **E2** (`held = 0` at the boot) | directly — it *is* `SD-1` | ⛔ **fails outright** |
| **E3** (the resolution sequence + the LTP-priced exit) | `:501` is only reached when `held == 0` | ⛔ **never fires; nothing to score** |
| **§11.6 candidate 6** (the only durable removal path) | it is `:501`→`:508`, gated on `held == 0` | 🔴 **the system's own removal path evaporates ⇒ NO durable removal exists at all without F6** |
| **§11.5's entire matrix** | every `E2 holds` column | 🔴 **half the matrix is void, and only the `E2 fails` column — the bad one — remains** |

> ### 🔴🔴 **⇒ ONE OBSERVATION ON MONDAY MORNING MOVES FOUR CONCLUSIONS AT ONCE. That is the fact worth surfacing, and it is invisible when the assumption is restated four times in four places.**
> ⭐ **It also tells you where to look first on Monday:** `get_positions` in the boot log is not merely
> E2's evidence — **it is the load-bearing read for the whole analysis**, and it should be captured
> before anything else is interpreted (§3.1 instant **B**).
>
> **CURRENT EVIDENCE FOR `SD-1`: (P) X2, and honestly bounded.** ✅ `positions()` returned
> **`0 positions`** at the 07-Aug 08:15 boot — twice, pre-market, on the T+1 morning after ATULAUTO's
> sale — and **zero for the WHOLE BOOK**, so it is a day-book rollover property rather than a
> symbol-specific accident. ⛔ **But that is ONE instance, overnight between consecutive trading days.
> `SD-1` has NEVER been observed across a weekend**, and a settlement gap is exactly where it could
> differ. ⚠️ **And a further wrinkle now on record (Monday card §3.9a): 26-Aug-2026 is a SETTLEMENT
> holiday — trading normal, pay-in/pay-out deferred — a case `nse_holidays_2026.yaml` cannot even
> express.** ⇒ **`SD-1` is well-grounded, singly-observed, and not a guarantee.**
>
> 🧪 **PARITY: ⛔ `SD-1` is UNTESTABLE IN PAPER.** Paper nets by *symbol* with **no T+1 settlement
> model**, so the `-1` residue whose disappearance `SD-1` asserts **cannot exist there**. A paper drill
> would report `held = 0` unconditionally and "confirm" `SD-1` **vacuously**.

🏷️ **Cross-referenced from:** Monday card **E2** · **E3** · §3.9 · §2.1's DEPENDS-ON column · and
§11.5/§11.6 above. ⛔ **Do not restate the assumption at those sites — point here.**

---
---

# §13 · THE THIRD REVIEW ROUND — 07-Aug-2026 night · ⛔ DOCS-ONLY

| # | point | disposition | outcome |
|---|---|---|---|
| 1,2,3,7 | **frozen BOOT-STAGE REFERENCE TRACE** | 🏷️ **APPLIED** — Monday card **§3.1b**, 15 stages with real offsets quoted from Friday's logs | 🔴 **BOUND — it surfaced, IN ADVANCE, that Monday should resolve `startup_scenario=COLD` where Friday resolved `CRASH`** *(Friday now HAS a clean shutdown event; 06-Aug did not)*. ⭐ **That would otherwise have been the most convincing false alarm available.** ⚠️ **And it corrected the stage list I was given: the CENSUS IS NOT A BOOT STAGE** — it is emitted at shutdown |
| 2.2 | **settlement ≠ trading calendar** | 🏷️ **APPLIED as a RULE** — `foundation_engineering_rules.md` **§1.15** | ⭐ **named as a CLASS, not a date: every T+1/delivery conclusion here is keyed to SETTLEMENT while the only calendar the system owns describes TRADING** |
| 2.3 | **DEPENDENCIES column** | 🏷️ **APPLIED** — Monday card §2.1 | ⭐ **BOUND — it made two structural facts visible that prose had hidden: E4 depends on `SD-1` being WRONG, and E7 does not depend on `SD-1` at all**, which is precisely what qualifies E7 as a control |
| 2.4 | **E7 as an INVARIANT, not just a control** | 🏷️ **APPLIED** — `foundation_engineering_rules.md` **§1.16** | ⭐ generalised: *a repair path must be demonstrably SELECTIVE — "it fixed the broken thing" is half a claim* |
| 2.5 | **Observed / Derived / Inferred labels** | 🚫 **REFUSED, with the reason recorded** — `campaign_practices.md` **`M9.2`** | ⛔ near-isomorphic to `(P)/(S)/(I)`; would be the **4th** scheme and the **2nd** answering the same question. ⭐ **MAPPED instead**, with a stated reopen condition *(produce a claim P/S/I cannot express)*. ⚠️ **The honest test was run before refusing — I tried to construct such a claim and could not** |
| 6 | §11.5's second axis | ✅ **ALREADY APPLIED** — the two-axis table is in §11.5 | ⛔ not re-implemented |
| 8 | hash-and-archive | ✅ **ALREADY APPLIED** — Monday card §3.1 | ⛔ not re-implemented — **and it was USED tonight: `A′` is preserved `chmod 444` with sha256 in `MANIFEST.txt`** |

## §13.1 — 🔴 **THE ONE THING THAT COULD NOT HAVE WAITED**

**Instant `A` of the capture plan — *"BEFORE the 08:15 boot"*, described in my own words as
*"THE BASELINE. Without it, nothing on Monday is attributable"* — is IMPOSSIBLE.**

**(P)** the token's `expires_at` is **`2026-08-08T05:00:00+05:30`**; `token_cleanup` runs **`0 5 * * *`
— daily, weekends included**; `auto_refresh_token` runs **`15 8 * * 1-5`**. ⇒ **from 05:00 Saturday
until 08:15 Monday there is no token and no broker read is possible.**

⇒ ✅ **A FRIDAY-NIGHT BASELINE (`A′`) WAS TAKEN AT `2026-08-07 21:07:28 +0530`**, ~8 hours before the
token died — preserved `chmod 444` at `~/preserved/monday_10aug2026/` with sha256 in `MANIFEST.txt`
(`b5895a8e…` broker 41,626 B · `6a652e5e…` db 7,585 B, **0 bytes stderr**).

> ⭐ **It brackets the weekend from the NEAR side.** Paired with Monday's boot log it isolates **what
> settlement did** — which is `SD-1`, and therefore E2's entire content.
> 🏷️ **And the instruction was AMENDED rather than left standing: an instruction that cannot be
> executed is worse than none, because it is recorded as a MISSED step rather than an IMPOSSIBLE one.**

---

# §14 · ROUND 4 — **THREE TAKEN, SEVEN CLOSED. ⛔ The Monday artifact is complete.**

| # | point | disposition |
|---|---|---|
| 2 | **stage IDs** | ✅ **TAKEN** — `B0…B15` in Monday card §3.1b. ⛔ No stage content or offset changed. ⭐ Monday now reads *"B11 passed, B12 failed"* |
| 7 | elapsed between milestones | ✅ **TAKEN AS A BY-PRODUCT of 2.1's offsets** — a Δ column, ⛔ not a separate artifact. ⭐ It immediately showed **B9 is the only slow stage (+12.89 s)** while **B10→B15 completes in 0.46 s**, so a gap in B10-B15 is itself a signal |
| 1 + 6 | **assumption register + explicit unknowns** | ✅ **TAKEN AS *ONE* ARTIFACT** — §3.8b, three columns. 🔑 **`330944932` sits in WAITING-FOR-MONDAY and stays there — ⛔ not "safe", not "unsafe"** |
| 4 | **baseline drift detection** | ✅ **TAKEN** — §3.9a-0. Hashing the FILES proves they were not edited; **hashing the STATE proves the world did not move.** `sha256 857258db…` over a canonical state structure ⇒ Monday diffs **mechanically**, not by eye |
| 8 | a second (intraday) negative control | ⛔ **DECLINED — timing, not merit.** ⭐ The reasoning is sound, but **the predictions are frozen**, and adding a control at 21:4x Friday means authoring a prediction for a symbol nobody has examined. **A control assembled at the deadline is not a control.** 🏷️ **OWED for the NEXT observation**, where it can be chosen deliberately |
| 3 | separate archives | ✅ **ALREADY SATISFIED** — `FRIDAY-NIGHT_*` and the Monday instants are distinct files under one manifest |
| 5 | confidence recorded | ✅ **ALREADY SATISFIED** — frozen per prediction in §2.1 |
| 9 | scoring order | ✅ **ALREADY SATISFIED** — §3.6 states it |
| 10 | dependency visibility | ✅ **ALREADY SATISFIED** — §2.1's DEPENDS-ON column |

> ⛔ **3, 5, 9 and 10 were CLOSED, not rebuilt.** ⭐ **A review point already satisfied must be closed,
> not built twice** — re-implementing it produces a second artifact saying the same thing, which is the
> exact failure `GD-1` recorded *(the pull to ADD is stronger than the memory of what exists)*.
> 🏁 **And that is the last addition. The Monday artifact is complete; further documentation now would
> only increase what must be read at 08:15 while something is actually happening.**

---

# §15 · ROUND 5 — **TWO TAKEN, ONE REFUSED, FOUR CLOSED. 🏁 THE ARTIFACT IS FINISHED.**

| # | point | disposition |
|---|---|---|
| — | **PROVENANCE classification** | ✅ **TAKEN** — a column in Monday card §2.1: **`BEFORE` · `WEEKEND` · `BOOT`.** 🔑 **The Friday baseline + state fingerprint exist to make it answerable, and ⛔ without it every finding defaults to `BOOT` because the boot is what everyone is watching** |
| — | **the INTERPRETATION RULE** | ✅ **TAKEN** — one sentence in §3.6: *ask FIRST whether the preserved weekend state **EXPOSED** a latent defect, ⛔ not whether the boot **CREATED** one.* ⭐ **A weekend carry with a settled T+1 sell is a state this system has never been in; novel states expose, they rarely create** |
| 7 | **HIGH/MEDIUM/LOW confidence by source agreement** | 🚫 **REFUSED** — **near-isomorphic to `X1/X2/X3+`**, which already grades exactly *"how many independent sources agree"*: `X1`≈LOW · `X2`≈MEDIUM · `X3+`≈HIGH. ⛔ It would be the **FIFTH** scheme. ⚠️ **Same honest test as `M9.2`: I tried to construct a claim X-tags cannot express and could not.** 🔗 Mapped, not adopted |
| 1 | the frozen window | ✅ **ALREADY SATISFIED** — §2.2, frozen at `4cf6217`, md5 re-verified |
| 4 | boot stage IDs | ✅ **ALREADY SATISFIED** — `B0…B15`, §3.1b |
| 5 | the baseline | ✅ **ALREADY SATISFIED** — `A′` at `21:07:28`, hashed |
| 8 | the prediction set | ✅ **ALREADY SATISFIED** — E1–E7 with falsifiers, confidence and width |

> ## ⭐⭐ **THE SECOND REFUSAL IN TWO ROUNDS, AND THE CONSISTENCY IS THE FINDING.**
> Round 4 refused a **fourth** labelling scheme (`M9.2`); round 5 refuses a **fifth**. **Both were
> near-isomorphic to something already in use; both were refused only after trying and failing to
> construct a claim the existing scheme could not express.** 🏷️ **A framework that keeps adding schemes
> has not become structural** — and the *rate of proposals* is now a better signal than any individual
> proposal.
> ## 🏁 **AND THE CURVE SAYS IT IS DONE: five review rounds, each yielding fewer usable points than the last** *(7 → 16 → 10 → 3 of 10 → 2 of 8, with 2 refusals)*. **⛔ Anything arriving before Monday 08:15 is filed for AFTER the observation — not folded into the artifact it is meant to test.**
