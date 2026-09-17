---
name: stated-vs-configured-limits-09aug
description: "Rama's stated limits vs config, MEASURED — his \"MIS=5 & GTT=3\" matches DEPLOYED main EXACTLY; the frozen sizing build raises every count limit and rebases the caps onto a leveraged basis."
metadata: 
  node_type: memory
  type: project
  originSessionId: 47b06b64-d65c-4b31-9c0d-e9517c6a78bf
  modified: 2026-08-09T15:13:32.342Z
---

# 🔴 THE PREMISE INVERTED — ⛔ RAMA'S NUMBERS ARE NOT WRONG. THE FROZEN BUILD CHANGES THEM.

**(P) `git show main:` and `git show 65b7196:config/system_config.yaml`.** ⭐⭐ **He was quoting his LIVE system, and on the counts he was EXACT.**

| Rama stated | deployed `main` | verdict |
|---|---|---|
| **"Max trades MIS = 5"** | `max_open_positions: 5` | ✅ **EXACT** |
| **"GTT = 3"** | `max_open_delivery_positions: 3` | ✅ **EXACT** |
| **"Max position value GTT = 1k"** | `max_concentration_pct: 0.10` × ₹10,000 = **₹1,000** | ✅ **EXACT at a ₹10k total** |
| **"Max position value MIS = 1.5k"** | concentration ₹1,000 · position-value `0.40` = ₹4,000 | ❌ **no key produces ₹1,500** |
| **"Max Qty MIS = 50 / GTT = 30"** | 🔴 **NO SUCH KEY EXISTS** | ❌ **see below** |

## §1.2 ⛔ THERE IS NO ORDER-QUANTITY CAP. ANYWHERE. IN EITHER BUILD.
**`max_qty` is COMMENTED OUT in `65b7196` (`# max_qty: 10`, `# delivery_max_qty: 10`) and ABSENT from `main`.** Code: `pipeline_policy.py:109 max_qty: Optional[int] = None` → `position_sizer.py:683 if eff_max_qty is not None:` ⇒ **absent = None = NO CAP.** ⚠️ **(P) a search of `system_config.yaml` + `broker_limits.yaml` for a 50 or 30 quantity cap returns NOTHING** — `broker_limits.yaml` is API rate-limiting, ⛔ not order size. ⭐ `max_single_order_qty: 10000` is a **REJECTING bug-guard** *(`QTY_EXPLOSION_GUARD`)*, ⛔ never a policy lever, and at ₹5,833 allocation it is unreachable above ~₹0.58/share.

## 🔴 WHAT THE FROZEN BUILD DOES TO EVERY ONE OF THEM — the config's own comments say "was"
| limit | deployed `main` | frozen `65b7196` |
|---|---|---|
| intraday concurrent | **5** | **6** *(comment: "was 5")* |
| intraday trades/day | **10** | **6** ⭐ *(tightened — and it is ALSO the sizing divisor)* |
| delivery concurrent | **3** | **6** *(comment: "was 3")* |
| delivery trades/day | **5** | **6** |
| concentration | `0.10` of **TOTAL CAPITAL** = ₹1,000 | `0.20` of the **INTRADAY BASIS ₹35,000** = **₹7,000** |
| position value | `0.40` of capital = ₹4,000 *(REJECTS)* | `0.25` of basis = **₹8,750** *(TRIMS)* |
| delivery caps | 🔴 **NO delivery sizing keys at all** | conc **₹600** · pos-value **₹750** |

⇒ 🔑🔑 **THE EFFECTIVE PER-SYMBOL INTRADAY CEILING: `₹1,000` LIVE → `₹2,917` WEDNESDAY (tier 0.50) → `₹5,833` if the tier mapping also lands.** ⭐ **~2.9× then ~5.8×**, and ⛔ **the base changed too — a % of TOTAL CAPITAL became a % of a 5×-LEVERAGED BASIS**, which is most of the move. ⚠️ **₹10,000 is a REFERENCE; the ratios hold at any capital, the rupees do not — the actual is `fm_ledger` INIT.**

## ⛔ THIS IS A QUESTION FOR RAMA, ⛔ NOT A DEFECT — AND ⛔ NOTHING WAS "CORRECTED"
⭐ **The caps genuinely never bind in the frozen build** *(max order ₹5,833 vs caps ₹7,000/₹8,750 — the config's own comment: "only catches an anomaly")* ⇒ **every tier conversation this week assumed a cap would catch a mistake; it will not.** 🔑 **But the finding is NOT "his numbers are wrong" — it is that HE DESCRIBED THE LIVE SYSTEM ACCURATELY and the build queued for WEDNESDAY raises all four counts and multiplies the per-symbol ceiling.** ⛔ **His three-line answer may change once he sees that.** 📌 **§3's ship-or-amend must NOT be put to him until this is answered.**

## 🔄 CORRECTED 09-Aug (LATER) — ⭐ THE `₹1,500 / Qty 50` FIGURES WERE **EXAMPLES**, ⛔ NOT POLICY
**Withdrawn by the author of the claim.** ⭐⭐ **BUT THE LOAD-BEARING HALF SURVIVES INTACT AND IS INDEPENDENT OF THE ATTRIBUTION: (P) the configured caps NEVER BIND at any price** — max order `₹5,833` vs concentration `₹7,000` and position-value `₹8,750`; delivery `₹500` vs `₹600`/`₹750` — **which the config's OWN comment already admits: *"only catches an anomaly."*** ⇒ 🔑 **THERE IS CURRENTLY NO EFFECTIVE CEILING ON POSITION SIZE OTHER THAN THE ALLOCATION ITSELF.** ⛔ Keep this on the record independently of who said what.

## ✅ THE DIVISOR RULE — SETTLED, AND THE CODE PRE-REGISTERED ITS OWN TRAP
**(P) `position_sizer.py:433` — `allocation_divisor = int(pol.max_daily_trades or 0)`**, mapped per pipeline at `pipeline_policy.py:411` *(`intraday_max_daily_trades`)* and `:363` *(`max_daily_delivery_trades`)*. ⇒ ⛔ **THE DIVISOR IS MAX TRADES/DAY, NEVER MAX OPEN POSITIONS.** ⭐⭐ **The warning is IN THE CODE, three lines above it, verbatim: *"Both are 6 today, which is exactly why picking the wrong one would go unnoticed — so the FIELD NAME is recorded in the audit line, not just its value."*** 📏 **At the ₹35,000 / ₹3,000 bases: `÷10 = ₹3,500` · `÷6 = ₹5,833` · `÷5 = ₹7,000` (MIS) · `÷5 = ₹600` · `÷6 = ₹500` · `÷3 = ₹1,000` (GTT).**

## ⛔ A SHARE-COUNT CAP IS THE WRONG SHAPE FOR A SAFETY CEILING
**(P) `position_sizer.py:683-685` — `max_qty` joins `candidates` and `min(candidates)` picks the smallest ⇒ at `3` it BINDS ON EVERYTHING** *(it fails to bind only above `₹7,000 ÷ 3 = ₹2,333`/share)*. **On a ₹45 share: 155 → 3, `₹6,975 → ₹135` = 1.9 % of allocation deployed.** ⇒ ⛔ **a validation run under it proves ONLY that a quantity cap works** — tier multiplier, allocation, position-value and concentration all become unobservable. ⭐ **A safety ceiling must be a RUPEE figure: a share count means something different on a ₹45 share than a ₹4,500 one, which is exactly the property a safety limit must not have.**

## 🔴🔴 PROVENANCE — ⛔ **BOTH** SIDES ARE UNSOURCED, AND THE SECOND ONE IS THE SURPRISE
**(P) SEARCH WIDTH: every file under `memory/`, all of `Downloads/`, and all of `docs/`.**
- ❌ **`"Qty 3, as Rama requested"` — NO SOURCE.** Every `qty 3` hit is unrelated *(T2 basket, late-July)*. ⭐ The card flagged this correctly.
- ❌🔴 **AND SO IS THE CARD'S OWN COUNTER-CLAIM: `"fix these as config"` returns ZERO hits.** ⛔ **The `6/6/6/6` attributed to *"Rama, 08-Aug, his own words, quoted at the time"* IS NOT SOURCED EITHER.** ✅ **What IS sourced: `git log -S` puts the `6/6/6/6` values into the repo at `65b7196` — the frozen sizing build itself.** ⚠️ An 08-Aug Rama quote does exist *(the "one system, one command centre" line)*, ⛔ **but it is about ARCHITECTURE and sets no count.**
⇒ 🔑 **THE RULE APPLIES SYMMETRICALLY OR IT IS NOT A RULE: neither figure may be a premise until a QUOTED, TIMESTAMPED Rama line exists.** ⛔ **Do not resolve the conflict by preferring the side that invoked the rule.**

## ⭐ THE SETS COLLAPSE FROM FOUR TO **TWO** — measured, not asserted
**(P) the proposal's `10 / 5 / 5 / 3` IS DEPLOYED `main`, EXACTLY** *(`max_daily_trades` 10 · `max_open_positions` 5 · `max_daily_delivery_trades` 5 · `max_open_delivery_positions` 3)*. **And Rama's 09-Aug `MIS=5 / GTT=3` matches `main`'s OPEN-POSITION keys, ⛔ NOT its trades/day keys.** ⇒ ⭐⭐ **there are not four competing sets — there are TWO: the LIVE one (`10/5/5/3`) and the WEDNESDAY one (`6/6/6/6`); Rama's 09-Aug words DESCRIBE the live one rather than proposing a third.** 🔴 **AND `§1`'s TRAP RECURS ONE LEVEL UP: reading his `5` as *trades/day* would set the divisor to 5 (₹7,000); read correctly as *max-open*, the divisor is untouched at 10 (₹3,500).** ⛔ **Same defect, different layer — the number is right and the KEY is wrong.**

See also [[tier-mapping-measured-09aug]] · [[two-pipeline-split-08aug]] · [[capital-vocabulary]] · [[feedback-unsourced-promoted-by-repetition-09aug]]
