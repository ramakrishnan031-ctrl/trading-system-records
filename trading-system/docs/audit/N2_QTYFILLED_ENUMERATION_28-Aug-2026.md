# N-2 · EXHAUSTIVE `trades.qty_filled` WRITE ENUMERATION · FILE 25 §1

🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S · 🏷️ NOT EXERCISED.
🔬 Read-only at `52ccb4f`, 12:58–13:07 IST. ⛔ No production change.

> ## 🔴 **PREDICTION #18 IS REFUTED. A DECREMENT PATH EXISTS.**
> ⭐ Per my own frozen wording: *"If a path exists, my 'observation, not defect'
> reading was wrong and that is recorded as a miss."* ⭐ It is recorded below, ⛔ not
> softened.

---

## 1 — 🔴 THE MISS, AND ITS CAUSE · ⭐ THE METHOD FAILED, ⛔ NOT JUST THE ANSWER

⚠️ On 28-Aug 11:53 I wrote: *"I searched for any path that decrements
`trades.qty_filled` on a partial exit and found none."* 🔴 **That search could not
have succeeded, for two independent reasons — so it was never evidence at all.**

| flaw | why it made the search vacuous |
|---|---|
| **1. Output truncated** | I piped through `head -8`, and all 8 lines came from a single file (`order_placer.py`, keyword-argument noise). ⛔ The scan never reached `order_reconciler.py`. |
| **2. Line-scoped grep** | I matched `UPDATE trades` and `qty_filled` **on the same line**. 🔬 **2 of the 3 real UPDATE statements span multiple lines**, so they could never match — ⛔ regardless of whether they existed. |

> ⭐ **This is the standing rule turned on my own work: a check is evidence only if
> it COULD have gone red.** ⛔ Mine could not. ⭐ The correct instrument was a
> multi-line-aware scan of every `UPDATE trades` statement and its body, which is
> what §2 uses.

⚠️ ⭐ **The first grep DID contain the answer and I cut it off** — `order_reconciler.py:2408`
literally contains the substring `SET qty_filled`. ⛔ Not a subtle miss; a truncation.

---

## 2 — 🔬 THE COMPLETE ENUMERATION · ⭐ MULTI-LINE AWARE

⭐ Method: scan **every** `.py` outside `venv/`, `tests/` and `scripts/`, find every
`UPDATE trades` token, read the **next 400 characters** of the statement, and keep
those whose body mentions `qty_filled`. ⭐ Plus the creation `INSERT`.

🔬 **Result: 3 UPDATE statements + 1 INSERT. ⛔ Nothing else writes the column.**
🔬 No generic/dynamic column writer exists (`kill_switch.py:1487` writes `status` only).

| # | site | what it writes | decrement? |
|---|---|---|---|
| 0 | `orders/order_manager.py:214` | `INSERT INTO trades (… qty_filled …) VALUES (…, **0**, …)` | ⛔ no — creation |
| 1 | `orders/order_manager.py:412` | `SET status='OPEN', entry_actual_price=?, entry_time=?, **qty_filled=?**` — the **ENTRY FILL** | ⛔ no — sets the fill |
| 2 | 🔴 `orders/order_reconciler.py:2408` | `SET qty_filled = ?` ← **`broker_qty`**, `WHERE trade_id=? AND qty_filled=?` | ✅ **YES** |
| 3 | `core/state_store.py:1564` | HARD_KILL recovery: `SET status='EXITING', recovered_flag=1, …, **qty_filled=?**` | ⛔ no — backfills an adopted fill |

### 🔴 PATH 2, QUOTED — it is deliberate, and it is a CAS latch

📄 `orders/order_reconciler.py:2380-2412` (CHECK 4, partial external close):

```python
local_qty = trade["qty_filled"] or 0
if broker_qty <= 0:
    return self._check1_manual_close(trade)      # full close → CHECK 1

# ── qty_filled CAS: the exactly-once latch for the M-O2 capital release ──
# Conditional on the CURRENT recorded qty so only the observing cycle both
# reduces qty AND releases the closed portion. rowcount==1 -> this cycle
# owns the release; ==0 -> another path already moved qty_filled.
cur.execute(
    "UPDATE trades SET qty_filled = ?, updated_at = ? "
    "WHERE trade_id = ? AND qty_filled = ?",
    (broker_qty, self._now_ist(), trade_id, local_qty),
)
qty_transition_owned = (cur.rowcount == 1)
```

⭐ The comment says **"reduces qty"** outright. ⇒ 🔬 **`trades.qty_filled` is actively
reconciled DOWN to the broker's remaining quantity on a partial external close**,
with a compare-and-swap so exactly one cycle owns the capital release.

---

## 3 — ⭐ WHAT THIS DOES TO S-1 · **⛔ IT DOES NOT CLOSE AS "PROVEN ABSENT"**

🔴 **My S-1 characterisation was TOO STRONG and is corrected:**

| I wrote (11:53) | 🔬 the measured truth |
|---|---|
| *"The old path exits the **local entry-fill** quantity"* | ⛔ Wrong. It exits a value the **reconciler actively maintains toward broker truth** via CHECK 4. |
| *"searched … found none"* | ⛔ Vacuous search (§1). |

✅ ⇒ **THE OLD EOD PATH IS MATERIALLY SAFER THAN I DESCRIBED.** ⭐ An over-exit needs
**both** a partial fill **and** CHECK 4 not yet having observed it.

⚠️ **But the residual is real and different in kind:** `qty_filled` is
**EVENTUALLY CONSISTENT** — it is only as fresh as the last reconciler cycle that ran
CHECK 4. ⛔ It is **not** read-at-use.

> ### 🏷️ **S-1 DISPOSITION: the decrement path EXISTS and is DELIBERATE. ⛔ Not "proven absent". ⛔ Not a defect. ⭐ RECORDED, ⛔ old path unchanged.**

### ⭐ AND THE RULE FOR THE NEW UNIT IS UNCHANGED — WITH A BETTER REASON

> **PASS 2 must read `broker_qty[symbol]` at use time.**
> ⛔ **Old reason (mine, wrong):** *"because `qty_filled` is never updated."*
> ⭐ **Correct reason:** *"because `qty_filled` is only **eventually** consistent, and
> two minutes from a hard broker cutoff PASS 2 must not depend on reconciler
> timing."*

⭐ Same requirement; ⭐ a justification that survives contact with the code.

---

## 4 — 🔒 PREDICTION #18 · SCORED

| | |
|---|---|
| **Predicted** | the exhaustive enumeration finds **no** decrement path ⇒ S-1 closes as PROVEN ABSENT |
| **Observed** | 🔬 a decrement path **exists** — `order_reconciler.py:2408` |
| **Score** | 🔴 **REFUTED** |
| **Consequence, per my own frozen wording** | my *"observation, not defect"* reading was **wrong in its stated reason**; ⭐ recorded as a **miss** |
| ⭐ Direction of the error | ⭐ In the **safe** direction — the old path is better than I claimed, ⛔ not worse. ⚠️ That does not make the miss smaller: ⭐ **a wrong reason for a right answer is still wrong.** |

---

## 5 — WHAT IS NOT MEASURED

1. ⛔ **How often CHECK 4 actually runs vs a partial fill** — the eventual-consistency
   *window* is 🏷️ **NOT MEASURED**.
2. ⛔ **Whether path 2 has ever fired in production** — 🏷️ **NOT MEASURED**;
   ⭐ note the 3 historical `EXTERNAL_UNATTRIBUTED` closures were **full** closes
   (`broker_qty <= 0` ⇒ routed to CHECK 1), ⛔ not partials.
3. ⛔ `scripts/t2_cnc_gtt_realtest.py:234` also inserts into `trades` — 🏷️ a **test
   script**, ⛔ not production, ⛔ not analysed.
4. ⛔ Nothing built, tested or pushed. ⛔ The old EOD path is **unmodified**.

⛔ green ≠ red-capable · ⭐ **a search that could not have found the answer is not
evidence** · ⛔ executed ≠ exercised · ⛔ a wrong reason for a right answer is still
wrong.

## END
