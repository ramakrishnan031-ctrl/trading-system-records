# FILE 15 §1 — L-1 … L-5 · LEVERAGE AS EXPLICIT CONFIG · MEASURED

**27-Aug-2026 (Thu), ~11:2x IST · market OPEN.** 🔬 MEASURED · 📄 EVIDENCE ·
💭 INFERENCE · 👤 RAMA'S.

⛔ **§2–§4 ARE NOT IN THIS DOCUMENT** — FILE 15 gates the build to **17:45**.
⛔ No push, ⛔ no code change, ⛔ no branch operation, ⛔ nothing built.
🔬 `origin/main` resolved BY MEASUREMENT = **`bc9a9f5`**. ⚠️ ROOT sits on
`feat/delivery-config-split`; every quote below is `git show origin/main:…`.

---

## 🔴 THE HEADLINE — 👤 RAMA'S REQUEST IS ALREADY IMPLEMENTED

> 👤 *"5x is multiplication available in MIS… same way 1x available in GTT?
> **If no create/add it.**"*

🔬 **The answer is YES — it already exists, and it is already explicit.**
`leverage_map.DELIVERY: 1.0` is present in deployed config, is read at boot, and
is **actively multiplied** through the *same* intent-generic code path as MIS.
⇒ ⭐ **His future-proofing requirement — *"change the config number → auto
applied"* — is ALREADY TRUE today.** ⛔ Nothing needs to be created.

🔴 **BUT THE GUARD HE IMPLIED DOES NOT EXIST, AND THE GAP IS REAL:**
🔬 A fat-fingered **`INTRADAY: 0.05`** (instead of `5.0`) **loads cleanly, passes
every existing check, and does NOT stop the boot.** ⇒ ⭐ **That — U3-d — is the
only genuine work in UNIT 3.** ⛔ U3-a and U3-b are no-ops.

---

## L-1 · DOES `leverage_map` EXIST? → ✅ **YES — ALL FOUR KEYS, INCLUDING DELIVERY**

🔬 `config/system_config.yaml` **`:154-158`** @ `bc9a9f5`, verbatim, every key and
value:

```yaml
154:  leverage_map:
155:    INTRADAY: 5.0             # MIS leverage
156:    COVER_ORDER: 6.0          # CO leverage
157:    DELIVERY: 1.0             # CNC, no leverage
158:    BRACKET_ORDER: 5.0        # BO leverage
```

- ✅ **`INTRADAY: 5.0` CONFIRMED** — the F2 inventory's figure re-verified at the
  deployed SHA.
- ✅ 🔴 **`DELIVERY: 1.0` EXISTS.** ⛔ It is **not** absent. ⇒ **U3-a is a NO-OP.**
- ⭐ Two further keys the request did not mention: `COVER_ORDER: 6.0`,
  `BRACKET_ORDER: 5.0`. ⚠️ Any ceiling proposed in U3-d must accommodate **6.0**.
- ✅ Notation is already correct in config: **`5.0` / `1.0`**, ⛔ not `0.05` / `0.01`.

---

## L-2 · MIS CAPITAL PATH — DOES IT READ THE MAP, OR IS 5.0 HARDCODED?

🔬 **It reads the map — and the wiring is what makes that true.** Traced end-to-end:

| # | site | what happens |
|---|---|---|
| 1 | `main.py:2675-2679` | `leverage_map = {"INTRADAY": cap_cfg.leverage_map.INTRADAY, "COVER_ORDER": …, "DELIVERY": …, "BRACKET_ORDER": …}` — built **from config**, all four intents |
| 2 | `main.py:2725` | injected into **`FundManager`** |
| 3 | `main.py:2839` | injected into **`PositionSizer`** |
| 4 | `capital/fund_manager.py:267-268` | **the ONE multiply site** (see L-3) |
| 5 | `capital/position_sizer.py:388` | `leverage = self._leverage_map.get(intent, 1.0)` |
| 6 | `position_sizer.py:493` | `margin_per_share = effective_entry_price / leverage` |

### 🔴 L-2's REAL FINDING — FIX-072's LIVE-MARGIN OVERRIDE IS **DEAD CODE IN PRODUCTION**

🔬 `position_sizer.py:389-400` would **overwrite** the configured leverage with the
broker's live figure:
```python
388:  leverage = self._leverage_map.get(intent, 1.0)  # static fallback
389:  if self._broker_adapter is not None:
391:      margin_pct = self._broker_adapter.get_live_margin_pct(symbol, intent)
399:      live_leverage = 1.0 / margin_pct if margin_pct > 0 else 1.0
400:      leverage = live_leverage
```
🔬 **But `broker_adapter` is NEVER PASSED.** `position_sizer.py:166` defaults it to
`None`, and the **only** production construction site — `main.py:2837-2860` — does
**not** supply it (verified: the whole kwarg block contains no `broker_adapter=`).
🔬 `PositionSizer(` appears in exactly **two** places in production: its own
docstring example `:116` and `main.py:2837`. ⛔ No second wiring path.

⇒ 🔴 **`self._broker_adapter is None` ⇒ line 389 never enters ⇒ the configured
`leverage_map` is AUTHORITATIVE in production.**
⇒ ⭐ **This is precisely WHY Rama's *"change the number → auto applied"* holds.**
⚠️ Were FIX-072 ever wired, the broker's live margin would **override** the config
and his premise would silently stop being true. 🏷️ **RECORDED — this is a
standing constraint on any future FIX-072 activation.**

⚠️ ⭐ **AND A NEGATIVE RESULT, STATED HONESTLY:** I checked the logs for
`live_margin_used` / `live_margin_fallback` and found **0 / 0** on every sink.
🔴 **That zero is VACUOUS and I am not resting anything on it** — the positive
control **FAILED**: `"logger":"position_sizer"` appears **0** times in today's logs
too, so the sizer emits nothing to these files at all. ⛔ The zero could not have
been red. ⭐ **The static wiring proof above stands on its own.**
🔬 Positive control that DID hold: the sizer demonstrably ran today — 7 entries
carry populated `qty_by_capital` / `qty_by_concentration` / `binding_constraint`
(JINDALSAW, TATAPOWER, SHANTIGOLD, RAMRAT, OAL, BIKAJI, OAL).

---

## L-3 · DELIVERY PATH — IS 1× **EXPLICIT** OR **IMPLICIT**? → ✅ **EXPLICIT *AND* ACTIVE**

🔬 **There is exactly ONE multiply site, and it is INTENT-GENERIC** —
`capital/fund_manager.py:267-268`:
```python
267:    leverage = leverage_map.get(intent, 1.0)
268:    return (qty * price) / leverage
```
⇒ ⭐ **DELIVERY flows through the SAME line as INTRADAY.** ⛔ There is **no**
delivery-specific branch that skips the multiply, and ⛔ **no** "code simply never
multiplies" case.

⇒ ✅ **L-3 ANSWER: the delivery 1× is EXPLICIT in config AND ACTIVE in code.**
⇒ 🔴 **Therefore FILE 15's second branch does not apply.** §1's own rule was:
> *explicit key present ⇒ config-only change, ⭐ near-zero risk*

⇒ ⭐ **U3-b (add a multiply step) is a NO-OP.** ⛔ Do not add one — a second
multiply site would be a second source of truth.

---

## L-4 · ANY OTHER HARDCODED LEVERAGE? → 🟡 **FOUR, AND ONLY ONE MATTERS**

| # | site | verdict |
|---|---|---|
| 1 | 🔴 **`capital/fund_manager.py:312-318`** — `if leverage_map is None:` substitutes a **hardcoded dict** `{INTRADAY: 5.0, COVER_ORDER: 6.0, DELIVERY: 1.0, BRACKET_ORDER: 5.0}` | 🔴 **A GENUINE SECOND SOURCE OF TRUTH.** ⚠️ Unreachable today (main.py always passes the map) ⇒ 🏷️ **LATENT**. ⭐ **This is U3-c's real target.** ⚠️ It duplicates the config block exactly — so it would drift silently the day config changes |
| 2 | 🟡 `capital/position_sizer.py:388` / `:409` — `.get(intent, 1.0)` | a **silent fallback to 1× for an unknown intent**. ⚠️ `PositionSizer` (`:183`) does **NOT** validate completeness, unlike `FundManager` (`:319-322`). 🏷️ LATENT — an intent typo would size at 1× rather than fail |
| 3 | 🟢 `scripts/replay_signals.py:163` — `margin = qty * trigger_price / 5.0  # approx intraday leverage` | **hardcoded**, but an **offline replay script** — ⛔ not the live capital path. 🏷️ Cosmetic |
| 4 | 🟢 `ops_dashboard/backend/api/risk_capital.py:121` — `"mis_leverage": 5.0, "gtt_leverage": 1.0` | 🔬 a **pinned TEST FIXTURE** (same dict holds `opening_real_cash: 10000.0`, `additional_payin: 5000.0`). The live path reads config at `:196` `lev_map = (cap_cfg.get("leverage_map") or {})`. 🏷️ ⛔ Not a defect |

⭐ Docstring examples at `fund_manager.py:287` and `position_sizer.py:118` quote
`5.0`/`1.0` illustratively — ⛔ not code.

---

## L-5 · IS `leverage_map` VALIDATED AT BOOT? → 🔴 **PARTIALLY — AND THE GAP IS THE DANGEROUS HALF**

**What DOES hold today:**
- ✅ 🔬 `core/config_loader.py:184-189` — `class LeverageMapConfig(BaseModel)` with
  `model_config = ConfigDict(extra="forbid")` and **four required `float` fields**
  (`INTRADAY`, `COVER_ORDER`, `DELIVERY`, `BRACKET_ORDER`) — **no defaults**.
  ⇒ ✅ **A MISSING key IS rejected at config load.** ⇒ ✅ An **unknown** key is
  rejected too.
- ✅ 🔬 `capital/fund_manager.py:319-322` — raises `ValueError` if any intent is
  absent from the dict passed in.

**🔴 What does NOT hold — measured, not assumed:**
- 🔴 **NO bounds anywhere.** `LeverageMapConfig` declares bare `float`: ⛔ no
  `ge=1.0`, ⛔ no upper bound. ⇒ `0.05`, `0.0` and `-5.0` **all load**.
- 🔴 **`core/config_auditor.py:694-702` (G2) is the ONLY sanity check, and it is
  three-ways insufficient:**
  ```python
  696:  for intent, value in (("INTRADAY", lev.INTRADAY), ("COVER_ORDER", lev.COVER_ORDER)):
  697:      if value > 10:
  699:          … Severity.WARN …
  ```
  1. ⛔ It checks **only INTRADAY and COVER_ORDER** — **DELIVERY and
     BRACKET_ORDER are never checked at all.**
  2. ⛔ It has **no lower bound** — it tests `> 10` only.
  3. ⛔ It is **`Severity.WARN`**, ⛔ not CRITICAL/exit 5.
- 🔴 ⛔ **Leverage gets NONE of F1's fail-closed treatment.** F1's contract —
  *"a missing or null value is REJECTED at config load; the boot logs the key name
  at CRITICAL and exits 5"* — covers the **delivery risk keys**, ⛔ **not**
  `leverage_map`'s values.

### 🔴 THE FAT-FINGER SCENARIO, TRACED — FILE 15's WARNING IS **CONFIRMED**

Writing `INTRADAY: 0.05` instead of `5.0`:
1. `LeverageMapConfig` — ✅ accepts (a valid `float`, no bounds)
2. `FundManager:319` — ✅ accepts (the key is present)
3. `config_auditor` G2 — ✅ **`0.05 > 10` is False ⇒ not even a WARN is emitted**
4. ⇒ 🔴 **THE BOOT PROCEEDS NORMALLY.**
5. ⇒ `required_margin = (qty × price) / 0.05` = **20× the notional** per share
   ⇒ every MIS size collapses to **1/100th of intent** (`5.0 / 0.05 = 100`).

⇒ 🔴 **A one-character config slip silently sizes every intraday trade at 1% of
intent, with no CRITICAL, no exit, and no WARN.** ⭐ Exactly the failure FILE 15
predicted — ⛔ and it is not hypothetical, it is the measured behaviour of the
deployed validation surface.

---

## ⭐ WHAT §2's UNIT 3 ACTUALLY IS, AFTER MEASUREMENT

| step | status after L-1…L-5 |
|---|---|
| **U3-a** add `DELIVERY: 1.0` | ⛔ **NO-OP** — L-1: it already exists, explicitly |
| **U3-b** add a delivery multiply step | ⛔ **NO-OP** — L-3: one intent-generic multiply already covers DELIVERY. ⚠️ Adding one would CREATE a second source of truth |
| **U3-c** remove hardcoded leverage | ✅ **REAL, SMALL** — `fund_manager.py:312-318`'s `None`-default dict (LATENT), and `position_sizer.py:183`'s missing completeness check |
| **U3-d** fail-closed validation | 🔴 **THE ENTIRE VALUE OF THIS UNIT** — bounds + all four intents + CRITICAL/exit 5 |
| **U3-e** Live+Paper parity · **U3-f** red-capable test · **U3-g** frozen prediction | ⭐ unchanged, ⛔ not started |
| **U3-h** touch nothing else | ⭐ easier than expected — U3 is now **validation-only** |

💭 **CEILING PROPOSAL FOR U3-d, WITH ITS REASON — 👤 Rama's to confirm, ⛔ not
adopted silently:** **`1.0 ≤ leverage ≤ 10.0`**.
- **Lower `1.0`** — 🔬 1× *is* "no leverage" (`DELIVERY: 1.0`); ⛔ nothing below 1
  is meaningful, and every fat-finger decimal slip (`0.05`, `0.01`) lands there.
- **Upper `10.0`** — ⭐ **not invented**: it is the threshold `config_auditor` G2
  **already uses** (`if value > 10`). ⭐ Reusing it converts an existing WARN into
  a hard bound, ⛔ introducing no new number. 🔬 It clears the highest configured
  value (`COVER_ORDER: 6.0`) with margin.

---

## ⭐ RECORDED — THE CANONICAL WORDING (permanent)

> **5× = broker/MIS leverage · 70% = MIS allocation · 3.5× = the total-capital
> planning multiple that `0.70 × 5.0` produces.** ⛔ **NEVER call 3.5× "leverage."**
> 🔴 **5× = `5.0`, ⛔ NOT `0.05`. 1× = `1.0`, ⛔ NOT `0.01`.** A percentage
> (`0.70`) and a multiplier (`5.0`) are different kinds of number.
> ⚠️ **5× is an ASSUMPTION, ⛔ not a guarantee** — Zerodha grants *up to* 5×,
> varying by instrument and day. ⛔ CONFIGURED leverage ≠ ACTUAL APPLICABLE
> leverage. 🔬 And today the system never asks the broker (L-2), so the config
> value is what is used — ⛔ whether or not the broker would agree.

⚠️ 👤 Rama's *"GTT = 10k × 70% = 3k"* was a label slip — the ₹3,000 is right,
the percentage is **30%**. ⛔ No action; ⭐ recorded so the record is clean.

---

## WHAT I DID ⛔ NOT MEASURE
1. ⛔ **Nothing was built, changed, or pushed.** §2–§4 remain gated to 17:45.
2. ⛔ **I did not measure the broker's ACTUAL applicable margin** for any symbol —
   `get_live_margin_pct` is never called in production, so ⛔ there is no live
   evidence that 5.0 matches Zerodha's real MIS margin on any instrument.
3. ⛔ **Whether `fund_manager.py:312-318`'s default is reachable by any path other
   than `main.py`** — I checked the production construction sites; ⛔ I did not
   audit scripts or tooling that may construct a `FundManager` directly.
4. ⛔ **No red-capable test was written**; U3-f is untouched.
5. ⚠️ **The ceiling `10.0` is a PROPOSAL, ⛔ not a decision.** 👤 Rama's to confirm.
