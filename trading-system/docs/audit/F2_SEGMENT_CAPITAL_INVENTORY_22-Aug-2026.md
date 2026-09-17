# FIX-F2 · SEGMENT-CAPITAL BASIS — PRE-BUILD INVENTORY

**22-Aug-2026 (Saturday), IST.** Card: TRACKER + F2/F3 VERIFICATION, issued 12:05.
**Governed by:** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).

🏷️ **STATUS: `INVENTORY ONLY · ⛔ NO CODE WRITTEN · ⛔ NOTHING BUILT · ⛔ NOTHING PUSHED`.**
**Measured at the deployed SHA `45683859a0a05f466189ac5bc98f9a9f089f98d3`.** Line numbers hold only there (`M3`).
**Register rows:** `N22-06` (the superseded ruling) · parent finding **`N20-48`** (the capital inventory). Tracker row **`FIX-F2`** in `MASTER_REGISTER.md §FX`.

---

## §0 — THE RULING THAT WAS NEVER MADE, AND THE ONE THAT WAS

⛔ **There is no "Ruling 4".** The Item 1 card asserted the basis migration was *"DEFERRED by Rama's Ruling 4"*. It was not. Rama's 21-Aug instruction is the opposite and is recorded verbatim:

> *"Please change every calculations of each segment (MIS & GTT) must be carried out on 'Segment capital' not real cash… If possible fix capital drift & capitals used to segment cash now."*

⇒ Filed as **`WC-PATTERN #7`** (`N22-01`). **The migration is REQUIRED and OUTSTANDING.**

⚠️ **A REAL, DATED RULING DOES EXIST ON THIS SUBJECT, AND IT SAID THE OPPOSITE.**
`docs/design/sizing/sizing_thread_conclusions_06aug2026.md` §1.3, verbatim:

> *"⭐⭐ LEVERAGE — the code DEFLATES the requirement; the proposed model INFLATES the base. They are equivalent for a single position. They are NOT equivalent for any cap written as a percentage. (P) only 1 of the 5 rungs uses purchasing power (`qty_by_capital`). The other four are percentages of capital. ⇒ ⛔ Adopting inflate-the-base would silently multiply four caps by 5×. ✅ RULING SHAPE: KEEP deflate-the-requirement, and make every rung DECLARE ITS DENOMINATOR."*

**Rama's 21-Aug instruction is later and is his own words, so §1.3's *shape* is SUPERSEDED.**
⭐ **But §1.3's *warning* is not superseded — it is the specification for this work.** §1.3 objected to the caps moving **silently**. This inventory is the instrument that makes every one of those movements **explicit, per row, with its factor**. `N20-48`'s *"BLOCKED on a dated ruling"* is stale and is corrected by `N22-06`.

---

## §1 — THE ARCHITECTURE, AND THE CANONICAL EXAMPLE VERIFIED

Rama's model:

```
real cash → allocation → × leverage → SEGMENT CAPITAL
MIS  = allocation × 5      GTT = allocation × 1
system sizing runs on SEGMENT capital
REAL CASH keeps a narrow job: broker reconciliation and capital drift,
via  segment usage ÷ that segment's leverage = real-cash equivalent
```

**Canonical example — ₹10,000 · 70/30 · 5×/1×, checked rather than repeated:**

| | |
|---|---|
| MIS allocation | `0.70 × 10,000` = **₹7,000** → segment `× 5` = **₹35,000** ✅ |
| GTT allocation | `0.30 × 10,000` = **₹3,000** → segment `× 1` = **₹3,000** ✅ |
| an MIS ₹3,000 notional entry | real-cash equivalent `3,000 ÷ 5` = **₹600** ✅ |

⭐ **AND THE CARRIED-FORWARD ₹317.62 RECONCILES EXACTLY, which is the check that this reading of the model is the right one.** At the measured live capital **R = ₹10,587.00** (derived from Item 1's `risk_rs = 105.87 = 1% × R`):
`delivery concentration on segment basis = 0.10 × (0.30 × 1 × R) = 0.03 R = ₹317.61` — the carried figure to a paisa of rounding. ⇒ the model is applied as written, and GTT leverage is confirmed **1×**.

📏 **EVERYTHING BELOW IS EXPRESSED AS A MULTIPLE OF `R` (real cash), with ₹ only as an illustration at `R = ₹10,587.00`.** The ratio survives; the rupee form expires at the next capital change.

| | as a multiple of R | ₹ at R = 10,587.00 |
|---|---|---|
| MIS segment capital | `0.70 × 5` = **3.50 R** | ₹37,054.50 |
| GTT segment capital | `0.30 × 1` = **0.30 R** | ₹3,176.10 |

---

## §2 — THE PREREQUISITE: `FIX-F1` (`d00e574`)

**Stated explicitly, as the card requires.** Before `FIX-F1`, **one** `max_concentration_pct` / `risk_per_trade_pct` / `max_position_value_pct` served **both** books, and the delivery variants were `null` and silently inherited. A per-book *basis* is meaningless without a per-book *key*: applying `3.50 R` to MIS and `0.30 R` to GTT through a single shared percentage would still collapse to one number at the moment the percentage is read.

`FIX-F1` created the five independent keys and removed the inheritance, so `position_sizer` already resolves `eff_risk_pct` / `eff_conc_pct` / `eff_max_position_value_pct` **per book** at `d00e574:356-366`. **`FIX-F2` is the second half of the same change: F1 split the percentage, F2 splits the base.**

⇒ **`FIX-F2` must be built on `d00e574`, ⛔ not on `4568385`.** If `FIX-F1` is rejected or reverted, `FIX-F2` cannot proceed as specified.

---

## §3 — 🔴 THE ONE STRUCTURAL CONSTRAINT, FOUND BY MEASUREMENT

**SEGMENT CAPITAL MUST BE A DERIVED, READ-ONLY QUANTITY. ⛔ IT MUST NEVER BE WRITTEN INTO `_total`, `_bucket_base()`, OR ANY `*_avail` FIELD.**

`capital/fund_manager.py:2311-2335` — `_bucket_base(bucket)` returns `cash × pct + that bucket's own carry`, in **real cash**. It is load-bearing three times over:

1. `_check_invariant` enforces that the bucket bases sum to `_total` — the **global identity** the whole ledger rests on.
2. It is passed as `cash_floor` at `:2434` and `:2448`.
3. A negative `avail` in either bucket **HARD-KILLS BOTH BOOKS** (`fund_manager.py:2391` → `_handle_invariant_violation`; live today, `N14-09`).

⇒ Inflating those fields by 5× would multiply the reservable purse, not the policy ceiling — the exact failure `foundation rules §1.13` names: *"isolate the policy, never the purse."*

**The shape that satisfies both:** a new read-only accessor, e.g. `segment_capital(bucket) = _bucket_base(bucket) × segment_leverage(bucket)`, consumed **only** by the percentage caps in §4's *MIGRATE* group. Nothing writes it; nothing reserves against it.

---

## §4 — THE MIGRATION MATRIX

> 🏷️ **Group A = MIGRATE (clean).** Per-entry quantities: the numerator is this one entry, so swapping the denominator is well-defined.
> 🏷️ **Group B = MIGRATE ONLY WITH A NUMERATOR FIX.** The numerator is **account-wide** today; moving only the denominator creates a mixed-basis comparison. **This group is the finding of this inventory.**
> 🏷️ **Group C = DO NOT MIGRATE.** Each row states *why*, ⛔ not merely "no change".

### GROUP A — MIGRATE

| consumer | file:line @ `4568385` | CURRENT BASIS | INTENDED BASIS | REASON | BEHAVIOUR CHANGE | TEST |
|---|---|---|---|---|---|---|
| **concentration / capital per scrip** | `position_sizer.py:423-425` | `total_capital` = **R** (account-wide real cash) | `segment_capital(bucket)` — **3.50 R** MIS, **0.30 R** GTT | it is a *policy* ceiling on how much of one book may sit in one name; the book is the segment | **MIS ×3.50** (₹1,058.70 → ₹3,705.45/scrip) · **GTT ×0.30** (₹1,058.70 → ₹317.61/scrip) | reproduce ₹317.61 for GTT and ₹3,705.45 for MIS at R = 10,587; assert MIS and GTT move in **opposite directions** |
| **risk budget per trade** | `position_sizer.py:381` (`risk_rs = total_capital × eff_risk_pct`) | **R** | `segment_capital(bucket)` | the per-trade risk budget is a share of the book being traded, ⛔ not of the account | **MIS ×3.50** (₹105.87 → ₹370.55) · **GTT ×0.30** (₹105.87 → ₹31.76) | the three recorded CNC legs re-computed on the GTT segment: `31.76 / 5.78 → 5`, `/14.46 → 2`, `/4.11 → 7` — ⛔ **these MUST move; a test asserting 18/7/25 after F2 would be asserting the bug** |
| **max_position_value** | `position_sizer.py:585` | **R** | `segment_capital(bucket)` | it is the backstop *for that book*; on real cash it is a backstop for a purse the book cannot spend | **MIS 0.40 R → 1.40 R** · **GTT 0.40 R → 0.12 R** | assert it still cannot bind: MIS ceiling `0.35 R < 1.40 R`, GTT `0.03 R < 0.12 R` — **a 4× margin on both**, preserved |
| **remaining segment capacity (reporting)** | derived; ⛔ **does not exist today** | — | `segment_capital(bucket) − segment_used` | the operator has no way to see how much of a segment is left; `N20-48` had to compute ₹37,055.90 by hand | **new read-only figure**; ⛔ no gate consumes it | assert it equals `qty_by_capital`'s implied ceiling, so the two cannot drift |
| **real-cash equivalent** | ⛔ **does not exist today** | — | `segment usage ÷ that segment's leverage` | Rama's own bridge back to the broker; without it, segment figures cannot be reconciled at all | **new derived figure** | the canonical example: an MIS ₹3,000 notional → **₹600** |

### GROUP B — 🔴 MIGRATE ONLY WITH A NUMERATOR FIX

| consumer | file:line @ `4568385` | CURRENT BASIS | INTENDED BASIS | REASON IT IS NOT CLEAN | BEHAVIOUR CHANGE IF THE DENOMINATOR MOVES ALONE | TEST |
|---|---|---|---|---|---|---|
| **sector exposure** | gate `risk_engine.py:638`; numerator `state_store.py:856-877` | limit `0.40 × R`; **numerator = `SUM(margin_reserved)` over ALL trade rows in the sector, with NO product or book filter** | limit `0.40 × segment_capital` | **(P) the numerator is account-wide.** A delivery entry would be measured against a **GTT-sized** limit using **MIS + GTT** margin | 🔴 **an intraday position in the same sector would consume the delivery sector cap**, whose limit has just fallen to `0.12 R` (₹1,270 at R = 10,587) | a mixed-book fixture: one MIS trade in sector X, then a GTT entry in sector X. **The gate must not see the MIS margin.** ⚠️ Today `sector_cap_mode: observe`, so this only *logs* — ⛔ that is a reason it would go unnoticed, not a reason it is safe |
| **daily loss — pre-trade gate** | `risk_engine.py:593` | limit `0.03 × R`; **numerator = `snap.daily_realized_pnl` = `store.get_daily_realized_net_pnl(today)`, ONE account-wide figure** | limit `0.03 × segment_capital` | **(P) there is no per-book realized-P&L attribution anywhere in the system** | 🔴🔴 **the GTT limit falls to `0.009 R` = ₹95.28. An INTRADAY loss of ₹100 would then block EVERY DELIVERY ENTRY for the day.** That is a live-money behaviour change nobody asked for | per-book P&L fixture: MIS realizes −₹150, GTT flat. **A GTT entry must still be admitted.** ⛔ It would not be, under a denominator-only change |
| **daily loss — post-close circuit breaker** | `fund_manager.py:1347` | `daily_loss_limit_pct × self._total` | ⛔ **stays real cash** *(recommended)* | it is a **portfolio** circuit, ⛔ not a per-entry gate; there is one account-wide realized P&L and nothing to split it with | ⛔ none, if left alone | assert it is unchanged by F2 |
| **daily loss — `system_manager` audit** | `scripts/system_manager.py:262` | `risk.daily_loss_limit_pct × day_capital` | must follow whatever the **gate** does, or the audit reports a limit the system does not enforce | it is a *mirror*; a mirror on a different basis is a false report | ⛔ none by itself — but it **silently diverges** the moment the gate moves | assert the audit's printed limit equals the gate's enforced limit, on the same inputs |

### GROUP C — ⛔ DO NOT MIGRATE. Each row states *why*.

| consumer | file:line @ `4568385` | why it must stay as it is |
|---|---|---|
| **`margin_per_share`** | `position_sizer.py:418` (`effective_entry_price / leverage`) | 🔴 **it ALREADY divides by leverage.** Multiplying the base by leverage as well would apply leverage **twice** — a 25× MIS purse. This is the double-apply the card warns about, and it is the one that would put real money at risk |
| **`qty_by_capital`** | `position_sizer.py:419-421` (`avail / margin_per_share`) | ⭐ **it is ALREADY the segment-capacity rung, expressed in real cash.** `avail / (price/lev)` ≡ `(avail × lev) / price` — algebraically identical to sizing on segment capital. `N20-48` measured what it supports: **₹37,055.90 of MIS notional.** ⛔ It is not broken; it simply never binds |
| **the 70/30 bucket split** | `fund_manager.py:337-338`, `_bucket_base` `:2311-2335` | 🔴 it is the **purse**, and the global invariant (`bases sum to _total`) is enforced against it. Inflating it manufactures reservable capital and can drive a bucket negative, which **HARD-KILLS BOTH BOOKS** (`N14-09`, live) |
| **`RESERVE` / `COMMIT` / `RELEASE`** | `fund_manager.py:521` · `:894` · `:637`, `:1204` | they move **real money the broker has actually blocked**. Segment capital is a policy fiction; reserving against it would reserve money that does not exist |
| **CHECK 1 / CHECK 2 (capital drift)** | `order_reconciler.py:3683-3702` | 🔑 **real cash is REQUIRED for drift to reconcile — it is the narrow job Rama scoped it to.** CHECK 1 compares against `margins.net`, a broker cash figure; CHECK 2 against `margins.used`. A segment-basis expected value could never equal a broker cash reading. ⭐ The bridge Rama named — `segment usage ÷ leverage` — is what lets segment figures be *checked* against this, ⛔ not a reason to move it |
| **`leverage_map`** | `config/system_config.yaml:154-158` | it becomes **more** load-bearing, not less: today it only deflates a requirement; after F2 it also defines the segment size. ⛔ Its *values* are not changed by F2 — but see `Q1` |
| **broker as final live authority** | `position_sizer.py:316` (`get_live_margin_pct`), `fund_manager.py:1411` (`sync_from_broker`) | the broker's live margin already **overrides** the static leverage for `qty_by_capital`, and `sync_from_broker` sets `_total` from broker cash. ⛔ F2 must not weaken either. ⚠️ See `Q1` — it is also the source of an ambiguity |
| **opening capital sync** | `fund_manager.py:445-477` (`initialize`), `:1411-1455` (`sync_from_broker`) | `_total` is and must remain **broker cash + carry**. Segment capital is derived *from* it, never written *into* it |

### GUI CONSUMERS — ⛔ LISTED, ⛔ NOT MODIFIED

| file | what it reads | why F2 touches it |
|---|---|---|
| `ops_dashboard/backend/services/capacity.py:115, 140-150, 220, 228` | re-derives limits itself: `loss_pct × opening_capital`, `max_concentration_pct`, `max_sector_exposure_pct` | 🔴 **it is an INDEPENDENT re-derivation, not a read of the engine's value.** After F2 the dashboard would display the OLD limit while the engine enforces the new one — a **fourth mirror** on a stale basis |
| `ops_dashboard/backend/api/risk_capital.py:32` | `daily_loss_limit_pct` | same class |
| `ops_dashboard/backend/services/operations.py:60-61` | `max_concentration_pct`, `daily_loss_limit_pct` | same class |
| `ops_dashboard/frontend/templates/controls.html` | renders the above | display only |
| `ops_dashboard/docs/G2a_capacity_inventory.md` | the capacity contract | the document that would go stale |
| `reports/daily_trade_review.py:1237-1240` | prints `risk.*` and `position_sizing.*` into the EOD report | the operator-facing figure would disagree with the engine |
| `scripts/system_manager.py:295` | prints `risk_per_trade_pct` and `max_concentration_pct` | same |

⚠️ **`ops_dashboard` tests are NOT in the gate command** (`pytest tests/unit tests/integration`). A GUI mirror can therefore break without the gate going red.

---

## §5 — 🔴 THE HEADLINE BEHAVIOUR CHANGE, IN NUMBERS

**This is not a refactor. It is a live-money sizing change of the first order, in BOTH directions at once.**

| cap | now | MIS after | factor | GTT after | factor |
|---|---|---|---|---|---|
| concentration (per scrip) | `0.100 R` = ₹1,058.70 | `0.350 R` = ₹3,705.45 | **×3.50** | `0.030 R` = ₹317.61 | **÷3.33** |
| risk budget (per trade) | `0.010 R` = ₹105.87 | `0.035 R` = ₹370.55 | **×3.50** | `0.003 R` = ₹31.76 | **÷3.33** |
| max_position_value | `0.400 R` = ₹4,234.80 | `1.400 R` = ₹14,821.80 | **×3.50** | `0.120 R` = ₹1,270.44 | **÷3.33** |
| sector exposure | `0.400 R` | `1.400 R` | **×3.50** | `0.120 R` | **÷3.33** |
| daily loss (pre-trade gate) | `0.030 R` = ₹317.61 | `0.105 R` = ₹1,111.64 | **×3.50** | `0.009 R` = ₹95.28 | **÷3.33** |

⭐ **AND `N20-48`'s BINDING-CONSTRAINT PREDICTION SURVIVES, WHICH IS THE USEFUL PART.** Its measured averages were `conc 3 · risk 26 · capital 75`. `qty_by_capital` is in Group C and does **not** move; the other two scale by 3.50 ⇒ `conc 10.5 · risk 91 · capital 75` ⇒ **concentration still binds on MIS, at ≈3.5× the quantity.** Deployed notional would move from `5 × ₹1,058.74` = **₹5,293.70** (14.3% of MIS capacity) toward `5 × ₹3,705.45` = **₹18,527** (50%).

⚠️ **THE GTT DIRECTION IS THE ONE RAMA HAS ALREADY ACCEPTED** — `₹317.62`/scrip blocks delivery names priced above it, and he accepted that it resolves as capital grows. **Recorded as an EXPECTED DAY-ONE EFFECT, ⛔ not a blocker.**
🔴 **THE MIS DIRECTION HAS NO SUCH ACCEPTANCE ON RECORD.** A 3.5× increase in intraday position size and per-trade rupee risk is the largest single behaviour change this campaign has proposed. It must be authorised in his own words, separately.

---

## §6 — QUESTIONS RAMA MUST ANSWER BEFORE ANY BUILD. ⛔ NOT DECIDED HERE.

**Q1 · WHICH leverage defines segment capital?** `leverage_map` is keyed by **INTENT**, not by bucket: `INTRADAY 5.0` · `COVER_ORDER 6.0` · `BRACKET_ORDER 5.0` · `DELIVERY 1.0`. And `position_sizer.py:316` **overrides the static value with the broker's LIVE margin** for `qty_by_capital`. So "MIS = allocation × 5" is well-defined only if segment leverage is a **fixed per-bucket constant**. If it followed intent, a CO entry would size on `0.70 × 6 = 4.2 R`; if it followed live broker margin, **every cap would move whenever Zerodha changed its margin table.** ⭐ His words say ×5 — a fixed constant — but the code has two other candidates and the choice must be explicit.

**Q2 · Does the daily-loss gate migrate at all?** Group B shows the numerator is account-wide. Three options: **(a)** leave daily loss on real cash (smallest change, keeps one honest comparison); **(b)** build per-book realized-P&L attribution first, then migrate (largest, and it is a new subsystem); **(c)** migrate the denominator only and accept that an intraday loss blocks delivery entries. ⛔ **(c) is not recommended and is stated only so it is not chosen by accident.**

**Q3 · Does the sector cap migrate at all?** Same shape as Q2 — the numerator is account-wide sector margin. ⚠️ Its `observe` mode means a wrong answer here would **log, not reject**, so the error would be silent for as long as the soak lasts.

**Q4 · Is the 3.5× MIS increase authorised?** §5's MIS column. ⛔ This is the live-money question; the GTT tightening is already accepted, the MIS loosening is not.

---

## §7 — WHAT THIS INVENTORY DOES **NOT** CLAIM

- ⛔ No claim that any figure here is what the system will do. Nothing is built. Every number is a **projection from measured expressions**, and §5's rupee forms expire at the next capital change.
- ⛔ No claim about `COVER_ORDER` / `BRACKET_ORDER` sizing: **(P) all 16 strategy YAMLs are `INTRADAY` or `DELIVERY`** — no strategy emits CO or BO today, so `leverage_map`'s `6.0` is unexercised. That is a fact about today, ⛔ not a reason to leave `Q1` unanswered.
- ⛔ A paper drill proves nothing here: paper nets by **SYMBOL**, live Kite per **(SYMBOL, PRODUCT)**.
- ⛔ No VM contact was made for this inventory. Everything is read from the `4568385` tree.

---

## §8 — VERDICT

# ⚠️ **PROCEED WITH CORRECTIONS**

The instruction is correct and the migration is required. **Four corrections to how it is scoped:**

1. 🔴 **Group B must not be built as specified.** The card lists sector exposure and daily loss (all three points) among the consumers to migrate. **(P) both have account-wide numerators.** Moving only the denominator would let an intraday loss block delivery entries and an intraday position consume the delivery sector cap. **`Q2` and `Q3` must be answered first.**
2. 🔴 **Segment capital must be DERIVED and read-only.** It cannot be written into `_bucket_base()`, `_total` or any `*_avail` — the global invariant and the negative-margin hard-kill depend on those staying real cash.
3. ⚠️ **`Q1` is unanswered by the instruction.** Three candidate leverages exist in the code.
4. ⚠️ **The MIS 3.5× loosening needs its own authorisation.** The GTT tightening is accepted; its mirror image is not.

**One correction to the record, already applied:** `N20-48`'s *"BLOCKED on a dated ruling"* is stale — the 06-Aug §1.3 shape is superseded by Rama's 21-Aug words (`N22-06`). Its *warning* stands and is what §4 exists to satisfy.

**Prerequisite:** `FIX-F1` (`d00e574`) must be accepted and deployed first. **`FIX-F2` builds on `d00e574`, ⛔ never on `4568385`.**

# ⛔ STOP. Nothing is built. Awaiting `Q1`–`Q4`.
