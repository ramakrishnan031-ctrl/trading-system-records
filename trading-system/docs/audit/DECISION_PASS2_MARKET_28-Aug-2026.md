# DECISION RECORD — PASS 2 = MARKET · R-1 VERIFIED · R-2 ACCEPTED

👤 **RAMA'S RULING, 28-Aug 12:35 IST: OPTION 1 — MARKET, NO GRACE.** ⛔ Options 2
and 3 rejected. ⭐ Adopted, ⛔ not re-argued.

⭐ Fourth companion. ⛔ The three frozen records are **unmodified**:
`db3c7df7cc62ff5d7e2c21a5acc0ddaf` · `0f1deac4787bbb2b820ad4b741987e3f` ·
`198d62e00766423cf951749fa2ada075`.

---

## 1 — 🔴 R-1 · **VERIFIED, ⛔ NOT ASSUMED** — and mutual exclusion is already free

👤 R-1: *"either they share one scheduler thread (⭐ **verify this, ⛔ do not assume
it**) or PASS 2 defers."* 🔬 **Verified. They can share one — the existing proven
pattern is single-threaded and serial.**

🔬 `orders/eod_squareoff.py:300-312`:

```python
def _poll_loop() -> None:
    while True:
        try:
            self.check_and_fire(now_ist())        # ← runs SYNCHRONOUSLY
        except Exception as exc:
            log_exception(self._log, exc)
        time.sleep(poll_interval_sec)             # 5 s

t = threading.Thread(target=_poll_loop, daemon=True, name="eod_squareoff_poll")
```

🔬 `:215-234` — the fire is slot-claimed under a lock, with reset-on-exception:

```python
if not self._mw.is_eod_squareoff_due(now):   return False
if self._mw.is_trading_holiday(now):         return False      # ⭐ holiday-aware
with self._lock:
    if self._fired_for_date.get(today, False): return False
    self._fired_for_date[today] = True        # claim atomically
try:
    self._fire(now, recovery_fire=False)      # ← BLOCKING, inside the loop
except Exception:
    with self._lock: self._fired_for_date[today] = False   # retry next poll
```

> ### ⭐ **CONSEQUENCE: ONE poll thread ⇒ `_fire()` blocks the loop ⇒ the next check cannot start until the previous returns. OVERLAP IS STRUCTURALLY IMPOSSIBLE — ⛔ not a feature to add, ⭐ a property to PRESERVE.**

🔴 **THE BINDING DESIGN CONSTRAINT, stated so it cannot be lost:**

> **PASS 1 and PASS 2 must be driven by ONE poll thread, evaluated sequentially,
> with a per-date **per-pass** fired flag under the same lock.**
> ⛔ **If they are ever scheduled as two independent timers or threads, overlap
> becomes possible and R-1's hazard is real.** ⭐ That is the mutation to test.

⚠️ **AND THE RESIDUAL RISK IS NOT OVERLAP — IT IS LATENESS.** 🔬 A blocking PASS 1
delays the loop, so PASS 2's trigger is *evaluated late*, ⛔ not concurrently:

| scenario | PASS 1 blocks until | PASS 2 evaluated | before 15:12? |
|---|---|---|---|
| zero lateness, 120 s grace | ≈ 15:09:07 | ≈ 15:10:00 | ✅ |
| PASS 1 late +90 s, 120 s grace | ≈ 15:10:37 | ≈ 15:10:37 (**37 s late**) | ✅ but ⚠️ thin |
| PASS 1 late +90 s, **R-2 cap** | grace shrinks | ≈ on time | ✅ ⭐ bounded |

⭐ **`PASS_1_STILL_RUNNING_AT_PASS_2` is still required as a named state** — ⛔ never
silent — because it must be *observable* that PASS 2 started late, even when the
single-thread design makes it safe. ⚠️ A deferred PASS 2 must still complete before
15:12, ⛔ else `DEADLINE_BREACH`.

---

## 2 — ⭐ R-2 · ACCEPTED · THE GRACE CAP

```
effective_grace = min(limit_grace_sec, CHECK_2 − now − margin)
```

⭐ **Inside the new unit only.** ⛔ The general EOD `limit_grace_sec: 120` is **NOT
changed** — 👤 explicitly forbidden, and the old 15:17 path needs it (its promotion
≈ 15:19:07 vs the non-CAS 15:25 cutoff, ~6 min spare).

⭐ Makes PASS 1 **bounded by construction, ⛔ not by luck**: 90 s late ⇒ the grace
shrinks automatically instead of spilling into PASS 2.

---

## 3 — 🔴 PASS 2 OWNS ITS PROTOCOL EXPLICITLY

👤 *"⛔ Do NOT reach PASS 2 through the old EOD exit path and override a field."*

⭐ The new unit gets its own validated **`PASS_2_EXIT_PROTOCOL = MARKET`**.

> ### 🔴 **INVARIANT: PASS 2 CONTAINS NO BLOCKING LIMIT-GRACE OPERATION.**
> ⚠️ A future maintainer changing the **general** EOD `limit_grace_sec` must **not**
> be able to reintroduce a 120 s sleep into PASS 2. ⭐ **Mutation test required**
> (prediction #23).

---

## 4 — ⚠️ WORDING · BINDING

⭐ **Permanent:** *"MEASURED-BOUND ESTIMATE using today's observed maxima —
≈ 2.035 s against a 120 s budget."*
⛔ **NEVER** *"guaranteed 2.035 s worst case."*

⚠️ 🔬 `get_positions` n=957 is strong; 🏷️ `cancel_order` **n=4** and `place_order`
**n=10** are **THIN**; ⛔ broker/network latency can exceed any historical maximum.
⇒ **Prediction #17 = GREEN under the measured-bound estimate**, ⛔ nothing stronger.

⭐ 👤 **The pessimistic delay placement is no longer a gate** — a delay after every
broker call, 3 symbols ⇒ 15 calls ≈ 945 ms + 14 × 500 ms = 7 000 ms + 300 ms
≈ **8 245 ms = 6.9 %**, ~111 s spare ✅. ⭐ Option 1 is safe under **either**
placement. ⇒ still trace it, ⭐ as **CONFIRMATION**, ⛔ not a build gate; ⛔ do not
weaken Option 1 if it returns pessimistic.

---

## 5 — ⭐ ONE THING R-1's VERIFICATION ALSO SETTLED, FOR FREE

🔬 `check_and_fire` already calls **`self._mw.is_trading_holiday(now)`** and
`is_eod_squareoff_due(now)` — ⇒ ⭐ the existing scheduler **is** calendar-aware.

⚠️ 🏷️ **BUT THAT DOES NOT CLOSE L-1.** ⭐ Holiday-awareness ≠ special-session
awareness: `special_sessions` moves `eod_squareoff_time` per date, while a flat
`mis_squareoff_cutoff: "15:12"` does not, and `15:12 < 19:12` passes the ordering
invariant **silently**. ⛔ Still **NOT built tonight**; ⭐ still a tracked FUTURE FIX.
⭐ The new unit should at minimum inherit the **same holiday gate**.

---

## 6 — 🔒 PREDICTIONS 21–24 (👤 Rama's), FROZEN

21. PASS 1 delayed **+90 s** ⇒ ⛔ no overlap; grace capped; both passes complete
    before 15:12.
22. Removing R-2's cap ⇒ the **overlap test goes RED**.
23. Changing the **general** EOD `limit_grace_sec` ⇒ PASS 2 is **unchanged**.
24. Under the **pessimistic** delay placement the three-symbol path completes in
    **< 10 s**.

⭐ Plus one of mine, since R-1's verification created a new falsifiable claim:

25. **Scheduling PASS 1 and PASS 2 on two independent threads/timers ⇒ the overlap
    test goes RED.** ⭐ This pins the single-poll-thread property as a *tested*
    invariant rather than an inherited accident.

⛔ Score only after the tests. ⛔ Do not adjust a prediction to fit a result.

---

## WHAT IS NOT MEASURED

1. ⛔ Nothing built, tested or pushed. ⛔ No auto-square-off code modified.
2. 🏷️ `cancel_order` / `place_order` latency samples remain **THIN** (n=4, n=10).
3. 🏷️ The 15:07/15:10 passes ⇒ **NOT EXERCISED until Monday.**
4. 🏷️ `special_sessions` ships fully commented out ⇒ **NOT EXERCISED.**
5. ⛔ Whether the new unit will in fact reuse the single-poll-thread pattern is a
   **design commitment made here**, ⛔ not yet code.

## END
