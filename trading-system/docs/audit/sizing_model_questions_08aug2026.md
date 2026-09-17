# §3 — RAMA'S ORDER-SIZING MODEL: RECORDED, AND THE THREE QUESTIONS ANSWERED

**08-Aug-2026. ⛔ NOTHING BUILT.** Read-only measurement + source trace.

## THE MODEL, IN HIS WORDS — recorded so it is not re-derived

Real broker cash **₹10k** · **MIS = 70 % = ₹7,000 × 5× margin = ₹35,000** for the MIS
**quantity calculation** · **GTT/Delivery = 30 % = ₹3,000, NO margin (1×)** ·
**qty = capital-per-scrip ÷ SL points** · ⛔ **the 5× is used for QUANTITY ONLY and
nowhere else** — real capital stays ₹10k so nothing drifts · **max-trades and
position-value stay the master controls** so the formula cannot produce a wild qty at
high capital.

---

## 3.1 · DO SL / TGT LEGS CONSUME ADDITIONAL CAPITAL AT ZERODHA?

> ### ⛔ **ANSWERED FOR OUR SIDE. ⛔ NOT ANSWERED FOR THE BROKER'S — AND I AM NOT GOING TO REASON PAST THAT.**

**(P) OUR SYSTEM RESERVES NOTHING FOR A PROTECTIVE LEG.** Measured on the live VM DB:

| evidence | value |
|---|---|
| protective legs actually placed | **233 SL + 221 TGT = 454** (193 filled) — a real population, ⛔ not an empty scan |
| `fm_ledger` entry types with a non-zero `margin_delta` | `RESERVE` 1453 · `RELEASE` 1214 · `RELEASE_USED` 227 · `TOP_UP` 7 — **all ENTRY-keyed** |
| `COMMIT` rows with non-zero `margin_delta` | **0 of 229** |
| ledger rows tied to an `SL`/`TGT` leg carrying margin | 🔑 **0** |

**(I) BROKER SIDE — INDIRECT, AND LABELLED AS INFERENCE.** If Zerodha held margin
against protective legs that our model does not, it would show up as an **unexplained
residual** in the capital-drift delta. The 05-Aug analysis (8 observations) found the
delta **decomposes EXACTLY** into deployed capital + unsettled realised P&L, with no
residual term. A drift observation on 06-Aug is consistent
(`actual 8888.50 · expected 9330.64 · delta 442.14`, `tier=LOG_ONLY`).

> ### ⛔⛔ **THE DIRECT TEST WAS NOT RUN, AND IT CANNOT BE RUN THIS WEEKEND.**
> §3.1 asks for `margins()` **before and after** a protective leg exists. That needs a
> broker token, and **(P)** the token expired `2026-08-08T05:00:00+05:30` with
> `auto_refresh_token` on `15 8 * * 1-5` ⇒ **there is no token from 05:00 Saturday
> until Monday 08:15.** ⭐ **The general principle — a position-REDUCING order needs no
> fresh margin — is exactly the "everyone knows" claim §3.1 warned about, so it is NOT
> being recorded as the answer.**
> 🔴 **OWED: one `margins()` before/after on a live day. Until then this is (P) for our
> ledger and (I) for the broker.**

⚠️ **PARITY: paper cannot answer this at all** — it synthesises fills and never calls
`margins()`. **(P)** the VM DB holds 561 trades, **all `mode=LIVE`, zero paper rows**;
⛔ an absent instrument is not a passing control.

---

## 3.2 · IS THE 5× APPLIED IN THE SIZING PATH? — **PARTLY, AND THAT IS THE GAP**

**(S) `capital.leverage_map`:** `INTRADAY 5.0 · COVER_ORDER 6.0 · **DELIVERY 1.0** ·
BRACKET_ORDER 5.0` — matching Rama's 5× MIS / 1× delivery exactly.

**(S) Leverage IS read, at `position_sizer.py:475`:**
`margin_per_share = effective_entry_price / leverage` → `qty_by_capital = floor(avail / margin_per_share)`.

> ### 🔑 **BUT IT REACHES ONLY *ONE* OF THE THREE CANDIDATE QUANTITIES.**
>
> | candidate | formula | levered? |
> |---|---|---|
> | `qty_by_risk` | `(base × risk_per_trade_pct) ÷ sl_distance` | ⛔ **NO** |
> | `qty_by_concentration` | `(base × max_concentration_pct) ÷ entry_price` | ⛔ **NO** |
> | `qty_by_capital` | `avail_bucket ÷ (price ÷ leverage)` | ✅ **YES — the only one** |
>
> **`raw_qty = min(all three)`**, so leverage can only ever matter when the CAPITAL term
> is the binding one.

**🔴 THE GAP, STATED PLAINLY — this is the whole reason Rama wrote the model out:**

Worked at ₹10,000 total, entry ₹500, SL distance ₹25 (a 5 % stop):

| | numerator | qty |
|---|---|---|
| **Rama's model** | capital-per-scrip **÷ SL points** | ₹7,000 / 25 = **280** |
| **code — risk** | (₹10,000 × 1 %) ÷ 25 | **4** |
| **code — concentration** | (₹10,000 × 10 %) ÷ 500 | **2** ← binds |
| **code — capital (levered)** | ₹7,000 × 5 ÷ 500 | **70** |

⇒ **the code sizes 2 where the model says 280.** ⭐ And the levered term (70) is not the
binder, so **the 5× has no effect on the size actually taken** — which is why the
standing memory note reads *"the system is UNAWARE of leverage."*

⚠️ **AND RAMA'S FORMULA AS LITERALLY WRITTEN OVERSHOOTS HIS OWN BUYING POWER:** 280 ×
₹500 = **₹140,000** of exposure against ₹35,000 of MIS buying power. ⇒ 🔑 **the formula
only works if its numerator is a RISK BUDGET, not deployable capital** — which is
exactly what §3.4 insists on. ⛔ **Not a criticism of the model; a statement that the
numerator has to be named before it can be built.**

---

## 3.3 · THE EXISTING NOTE — **FOUND, AND IT DISAGREES**

📍 **It lives in the memory palace: `capital_vocabulary.md`**, and it is quoted in
`MEMORY.md`'s hot index (*"70/30 MIS/CNC · System UNAWARE of leverage"*).

> **Its words:** *"live ACTUAL CAPITAL Rs 9,875.60, 70/30 intraday(MIS)/delivery(CNC);
> broker 5x MIS / 1x CNC; **the SYSTEM IS UNAWARE of leverage and sizes against
> UNLEVERED capital**. Four quantities diverge — always label which: ACTUAL CAPITAL /
> BUYING POWER / RISK CAPITAL / POSITION EXPOSURE."*

| the two versions | verdict |
|---|---|
| ✅ **AGREE** on 70/30, on 5× MIS / 1× CNC as the BROKER's terms, and on ₹10k order-of-magnitude actual capital *(⚠️ the note itself insists ₹9,875.60 is a DAILY measurement, ⛔ never a constant — read the latest `fm_ledger` `INIT`)* | consistent |
| 🔴 **DISAGREE:** *"the system is UNAWARE of leverage"* is **TOO STRONG**. `leverage_map` is read and `qty_by_capital` IS levered | **the note needs one qualifier** |

⭐ **The note is right about the OUTCOME and wrong about the MECHANISM** — and the
distinction matters, because *"unaware"* implies wiring the 5× in would be an addition,
when in fact it is already wired and simply never binds. ⛔ **A future build that
"adds leverage to sizing" on the strength of that sentence would be adding a second
levered term to a path that already has one.**

🔧 **CORRECTED WORDING, ⛔ one qualifier only, no second copy:** *"the system reads
leverage but sizes against UNLEVERED capital in practice — `leverage_map` is applied
ONLY to `qty_by_capital`, which is not the binding constraint (492/492 samples bound on
concentration, 0 ties)."*

---

## 3.4 · THE SIZING INPUT — ✅ ALREADY CORRECT, AND PINNED

**(S)** `qty_by_risk = (base × risk_per_trade_pct) ÷ sl_distance` — **risk capital ÷ SL
distance.** ⛔ **`R:R` appears nowhere in the sizing path.** ⭐ Preserved, and worth
keeping stated: R:R is *expected reward*, ⛔ not a sizing-risk input, and that confusion
is already on this system's record.

---

## ⛔ WHAT IS *NOT* DECIDED HERE

Nothing was built. **Before any sizing build can start, ONE thing must be named:
what the numerator of `capital-per-scrip ÷ SL points` IS** — a risk budget or deployable
capital. ⭐ Everything else in the model follows from that answer, and the worked
example above shows the two readings differ by ~140×.
