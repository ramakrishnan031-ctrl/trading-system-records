# FILE 24 §1–§3 · LATENCY BUDGET · PARITY FINDING · SPECIAL SESSIONS

⭐ Third companion. ⛔ The two frozen records are **not modified**:
`PREBUILD_MIS_SQUAREOFF_28-Aug-2026.md` = `db3c7df7cc62ff5d7e2c21a5acc0ddaf` ·
`PREBUILD_S1-S5_28-Aug-2026.md` = `0f1deac4787bbb2b820ad4b741987e3f`.

🔬 Read-only, `52ccb4f`, 12:12–12:16 IST. ⛔ No production change.

> ## 🔴 **§2 Q-2 REQUIRED A REPORT BEFORE BUILDING, AND IT IS REQUIRED. ⭐ ONE CONFIG DECISION IS NEEDED.**
> ✅ The **API latency** fits the 2-minute budget with enormous margin (~1.7 % used).
> 🔴 But the inherited **`limit_grace_sec: 120` is a BLOCKING `time.sleep`** that
> consumes the **entire** PASS 2 budget and would push the MARKET promotion
> **past the 15:12 cutoff**.

---

## §1 — THE PAPER DEFAULT · 🏷️ **PARITY FINDING**, ⛔ not a coding note

🔬 `broker/zerodha_adapter.py` — the same absent field, two answers:

| mode | line | absent `product` → | ⇒ eligibility |
|---|---|---|---|
| **live** | `:1234` | `str(row.get("product", ""))` → `""` | **EXCLUDED** |
| **paper** | `:1204` | `info.get("product", "MIS")` → `"MIS"` | 🔴 **ELIGIBLE** |

> 🔴 **PAPER IS MORE PERMISSIVE THAN LIVE ON A SAFETY BOUNDARY, WHICH INVERTS WHAT
> PAPER IS FOR.**
> ⇒ A position with a missing product would be **squared off in paper** and
> **silently skipped in live** — ⭐ precisely the failure this unit exists to
> prevent — ⚠️ **and paper would have shown a green result.**

> ### ⇒ 🏷️ **PAPER EVIDENCE FOR THIS UNIT'S PRODUCT BOUNDARY IS NOT TRANSFERABLE
> ### TO LIVE** until the default is neutralised **inside the new unit**.

⛔ **The adapter defaults are NOT changed tonight** — that is the OLD path and a
separate item. ⭐ The new unit must simply never consume a **defaulted** product
from either mode: require an **explicit** `product == "MIS"`.

⭐ Falsifier already frozen — **prediction #12**: a paper position with a missing
product must be **EXCLUDED**. ⚠️ If it is selected, the asymmetry is load-bearing
and 🔴 the unit is unsafe in paper mode.

---

## §2 — Q-1 · MEASURED LATENCY, ⛔ NOT ASSUMED

🔬 Every adapter call today (28-Aug), from the `call_start`/`call_end`
`duration_ms` pairs already in the log. ⛔ Nothing synthetic.

| method | n | min | p50 | p95 | **max** |
|---|---|---|---|---|---|
| `get_positions` | 957 | 12 | 18 | 28 | **150** |
| `get_holdings` | 13 | 11 | 15 | 18 | 18 |
| `get_order_history` | 349 | 11 | 17 | 20 | **47** |
| `cancel_order` | 4 | 40 | 40 | 43 | **44** |
| `place_order` | 10 | 37 | 43 | 51 | **63** |
| `get_margins` | 945 | 29 | 37 | 57 | 161 |
| 🔴 **`get_quote`** | 2020 | 10 | 18 | **2 317** | **4 730** |

⚠️ 🔬 **`get_quote` is the one outlier — p95 2.3 s, max 4.7 s.** Everything else is
tens of milliseconds. 🏷️ `cancel_order` n=4 and `place_order` n=10 are **thin
samples**; max is used below, ⛔ not p50.

### Q-2 · THE BUDGET, SUMMED AT WORST-CASE MAX

⭐ Sequence per FILE 24 §4: positions query → per symbol {cancel SL, cancel TGT,
verify ×2, submit exit} → re-query. 🔬 `inter_order_delay_ms: 500`
(`system_config.yaml:307`).

**PASS 2 budget = 15:10 → 15:12 = 120 000 ms.**

| variant | worst-case total | verdict |
|---|---|---|
| **MARKET exits** (no quote, no grace) | `150 + 3×245 + 2×500 + 150` = **≈ 2 035 ms** | ✅ **1.7 % of budget · ~118 s spare** |
| **inherited `LIMIT_THEN_MARKET`** | `+4 730 (get_quote) + 120 000 (grace)` = **≈ 126 765 ms** | 🔴 **EXCEEDS 120 000 ms** |

### 🔴 THE SQUEEZE, NAMED

🔬 `orders/eod_squareoff.py:1387-1393`:

```python
self._log.info("EOD phase-2: %d LIMIT order(s) pending; sleeping %.1fs grace "
               "before MARKET promotion sweep", len(pending_limits), self._limit_grace_sec)
if self._limit_grace_sec > 0:
    time.sleep(self._limit_grace_sec)          # ← BLOCKING
```

🔬 `config/system_config.yaml:310-312` — `exit_protocol: "LIMIT_THEN_MARKET"` ·
`limit_grace_sec: 120`.

> ⇒ 🔴 **If PASS 2 inherits this protocol, it submits LIMITs at 15:10, sleeps 120 s,
> and promotes to MARKET at ≈ 15:12:07 — AFTER the cutoff it exists to beat.**
> ⚠️ Worse with a slow `get_quote`: ≈ 15:12:12.

✅ **PASS 1 is fine:** 15:07 + ~6.6 s + 120 s grace ⇒ promotion ≈ **15:09:07**,
comfortably before PASS 2 at 15:10 (**~53 s margin**).

⚠️ 🔬 **The OLD 15:17 path is NOT newly defective** — its promotion lands ≈ 15:19:07
against the non-CAS 15:25 cutoff (~6 min spare). ⛔ Nothing to fix there.

### ⭐ THE DECISION NEEDED — 👤 RAMA'S, and it is config-only

| option | PASS 2 worst case | assessment |
|---|---|---|
| **A ⭐ RECOMMENDED — PASS 2 uses MARKET, no grace** | **≈ 2.0 s** (1.7 %) | ⭐ At two minutes from a hard broker cutoff, **execution certainty beats price**. That IS the two-pass intent: PASS 1 seeks price, PASS 2 guarantees the exit. |
| **B — the new unit gets its own shorter grace** (e.g. `mis_squareoff_limit_grace_sec: 30`) | ≈ 36.6 s (31 %) | ⭐ Viable, keeps some price-seeking; ⚠️ one more knob to validate. |
| **C — widen the offsets** so a 120 s grace fits | needs `second_offset ≳ 2m10s` | ⛔ **Not recommended** — fragile, and it surrenders more trading time for no gain. |

⭐ **PASS 1 keeps `LIMIT_THEN_MARKET` under every option.**

---

## §3 — L-1 · SPECIAL SESSIONS · 🔴 **THE MECHANISM EXISTS — AND THAT MAKES THIS SHARPER THAN A "LIMITATION"**

✅ 🔬 **The system already holds one, and it already overrides the square-off time.**

🔬 `config/system_config.yaml:62-70` (FIX-094):

```yaml
# Special sessions (Muhurat trading, etc.) — override market hours for specific dates
# Format: date (YYYY-MM-DD) -> {market_open, market_close, eod_squareoff_time}
special_sessions:
  # 2026-11-01:
  #   market_open: "18:15"
  #   market_close: "19:15"
  #   eod_squareoff_time: "19:12"
```

🔬 `core/market_windows.py:68-78` — `special_sessions: dict[date, tuple[time, time,
time]]`, resolved per-date by `_get_effective_times(d)`.

> ### 🔴 SO THE RISK IS NOT "WE HAVE NO CALENDAR". IT IS **DIVERGENCE**.
> On a Muhurat-style day `eod_squareoff_time` correctly becomes **19:12**, while a
> flat `mis_squareoff_cutoff: "15:12"` **does not move**.
>
> ⚠️ **AND THE ORDERING INVARIANT WOULD NOT CATCH IT** — `15:12 < 19:12` is
> numerically valid, so the fail-closed validation **passes silently**.
>
> ⇒ CHECK 1 fires at **15:07**, ~3 h **before** `market_open 18:15`, on an empty
> book (logs FLAT, harmless) — ⭐ and the session's **real** MIS positions then get
> **no protective pass at all** before the broker's own cutoff.

⛔ **NOT BUILT TONIGHT** — 👤 Rama's *"simple by decision"* stands, and ⛔ FILE 24
§3 forbids session-relative logic tonight.

⭐ **RECORDED FOR THE DEFERRAL, so a future maintainer meets a documented design,
⛔ not a surprise:**
1. **Preferred:** derive `mis_squareoff_cutoff` from the **same per-date
   `special_sessions` override** that already moves `eod_squareoff_time`. ⭐ The
   plumbing exists; only the wiring is missing.
2. **Minimum guard:** validate `CHECK_1` against the **effective** `market_open`
   for the date, ⛔ not against a bare clock literal.
3. ⭐ Until then the config provenance block must say, verbatim: *"absolute IST
   time; **not** session-relative; special sessions are out of scope and the
   ordering invariant will not detect divergence."*

⚠️ 🏷️ **NOT MEASURED:** whether `special_sessions` has ever been populated (the
block ships fully commented out) ⇒ 🏷️ **NOT EXERCISED** in production.

---

## STATUS FOR TONIGHT

✅ Every other gate stays clear. ⛔ Nothing built. ⭐ The build proceeds after 17:45
**once 👤 Rama picks A, B or C** for PASS 2's exit protocol — ⭐ config-only, and
⛔ it must not be guessed.

⚠️ **A currency note, ⛔ not a correction:** FILE 24 refers to *"OAL + RAMRAT"*.
🔬 **OAL exited on target at 12:01:21.404** (₹445.55, **+₹11.68**). ⭐ The CNC book
is **RAMRAT only**, `D = ₹592.96`. 👤 The 15:00 call now concerns **one** symbol.

⛔ push ≠ boot · ⛔ executed ≠ exercised · ⛔ exercised ≠ load-bearing ·
⛔ green ≠ red-capable · ⛔ order accepted ≠ position closed ·
⛔ broker query failure ≠ flat · ⭐ **SIMPLE BY DECISION, ⛔ NOT SIMPLE BY ACCIDENT.**

## END
