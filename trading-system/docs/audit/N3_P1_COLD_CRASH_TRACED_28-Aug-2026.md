# N-3 · P-1 COLD/CRASH · 🔬 **TRACED** · FILE 25 §1

🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S · 🏷️ NOT EXERCISED.
🔬 Read-only at `52ccb4f`, 13:01–13:07 IST. ⛔ No scenario logic changed.

> ## ✅ **P-1 MOVES FROM 💭 INFERENCE TO 🔬 TRACED — AND THE ALARMING COROLLARY IS ⛔ REFUTED.**
> 🔴 The suspicion was *"COLD is unreachable; the system runs crash-recovery every
> morning."* 🔬 **The truth is the inverse:** COLD is exactly what the **authoritative**
> call returns, and the CRASH is a **positional artefact of a second call that is
> never acted on.**

---

## 1 — 🔬 THE ALGORITHM, QUOTED

📄 `utils/startup_checks.py:198-213` — `detect_startup_scenario`, docstring verbatim:

```
1. No session row at all                     -> COLD
2. kill_switch == HARD_KILL                  -> HALT
3. kill_switch == SOFT_KILL:
     triggered_at.date() == today            -> HALT
     triggered_at.date()  < today            -> fall through
4. session.session_date != today             -> COLD
5. Same day. SHUTDOWN event for today found  -> WARM
   Same day. No SHUTDOWN event               -> CRASH
```

⭐ **"Same day" is a CALENDAR-DAY comparison** (`session.session_date != today`), ⛔ not
a run-state.

---

## 2 — 🔴 THE ORDERING, AND IT IS THE WHOLE ANSWER

🔬 Three sites in `main.py`, in execution order:

| line | what happens | scenario returned |
|---|---|---|
| **`:2265`** | `detect_startup_scenario(...)` — ⭐ **the FIRST, AUTHORITATIVE call** | **COLD** (step 4: `2026-08-27 != 2026-08-28`) |
| `:2268-2289` | the `if/elif` ladder consumes it; its value becomes the `STARTUP` row's scenario column | — |
| 🔴 **`:2305`** | **`_write_session(session_date=today_iso, …)`** — ⭐ **writes TODAY's session row** | — |
| `:2448` | `run_all_startup_checks(...)` | — |
| **`startup_checks.py:1561`** | `detect_startup_scenario(...)` — the **SECOND** call | **CRASH** |

> ### 🔬 **THE FLIP IS AN ORDERING ARTEFACT.** `_write_session` runs **between** the
> two calls, so by the second call `session.session_date == today` and **step 4 can
> no longer fire.** ⇒ Step 5 applies.

### ⭐ AND STEP 5 CAN ONLY EVER SAY "CRASH" AT BOOT — BY CONSTRUCTION

⭐ A `SHUTDOWN` event for **today** is written at **shutdown**. ⇒ At boot it **cannot
exist yet**. ⇒ step 5's *"no SHUTDOWN event"* branch is **always** taken.

> ## 🔴 **⇒ THE SECOND CALL IS STRUCTURALLY GUARANTEED TO RETURN `CRASH` ON ANY NORMAL BOOT. IT CARRIES ZERO INFORMATION.**

---

## 3 — ⭐ WHY IT IS HARMLESS: THE SECOND CALL'S **ONLY** CONSUMER

🔬 `utils/startup_checks.py:1561-1565`, quoted **in full** — this is the entire use:

```python
scenario_details = detect_startup_scenario(
    state_store, kill_switch, today_date, logger
)
if scenario_details.scenario == StartupScenario.HALT:
    blocking_failures.append("halt_requires_resume")
```

⇒ ⭐ **Only `HALT` is tested.** ⛔ `CRASH`, `COLD` and `WARM` are **indistinguishable**
to this consumer — none is acted on. (⭐ Plus `:1667`, a log string.)

🔬 **Blast radius, re-measured three consecutive days (26, 27, 28-Aug):**

| falsifier that could have fired | result |
|---|---|
| `grep -c "Startup scenario: CRASH"` (the ladder's own CRITICAL) | **0** |
| `SELECT COUNT(*) … event_type='CRASH_DETECTED'` | **0** |
| the `STARTUP` row's scenario column | **`COLD`** |

---

## 4 — 🔴 THE FIVE QUESTIONS FILE 25 ASKED · ANSWERED

| question | 🔬 answer |
|---|---|
| where `startup_scenario` is first assigned | `main.py:2265` — the authoritative call |
| what condition flips it to CRASH | `_write_session` at `main.py:2305` creates today's session row **between** the calls ⇒ step 4 falls through to step 5 ⇒ no SHUTDOWN today ⇒ CRASH |
| whether the override is intentional | 🔴 **It is NOT an override.** ⭐ They are two **independent** calls; only the first is authoritative. ⛔ The second never overwrites anything. |
| whether the SHUTDOWN marker is written before or after the decision | **After** — a SHUTDOWN row for *today* is written at shutdown, so it can never exist at boot ⇒ step 5 is predetermined |
| whether the COLD and CRASH check sets differ materially | ⛔ **No** — the second call's consumer tests **only** `HALT`; COLD, WARM and CRASH are equivalent there |

---

## 5 — ⭐ THE CORRECTED WORDING · ⛔ THE OLD PHRASING IS WITHDRAWN

⛔ **Withdrawn:** *"The observed startup sequence makes the COLD arm appear
unreachable under the tested production startup path."*
⚠️ That was the honest conditional form at the time, ⛔ but it pointed at the wrong
arm.

⭐ **REPLACEMENT, traced:**

> *"`detect_startup_scenario` is called twice. The **first** call (`main.py:2265`) is
> authoritative and correctly returns **COLD** on a new day; its value is what the
> `STARTUP` row records. The **second** call (`startup_checks.py:1561`) runs **after**
> `_write_session` has created today's session row, so it is **structurally
> guaranteed** to return **CRASH** at boot and its result is consumed **only** to test
> for `HALT`. The CRASH line in the log is a positional artefact, ⛔ not a
> classification of the boot."*

🔴 **AND THE COROLLARY IS REFUTED, ⛔ not merely left unproven:**
⛔ *"the system runs crash-recovery every morning as its normal path"* is **FALSE**.
🔬 No CRASH branch executes: the ladder's CRITICAL never logs, no `CRASH_DETECTED`
row is ever written, and the recorded scenario is `COLD`.

⭐ 💭 **The one thing that remains INFERENCE:** whether the double call is *deliberate*
design or incidental. ⛔ Not determinable from the code; ⛔ not investigated.

---

## 6 — ⭐ DISPOSITION

🏷️ **P-1: TRACED · ⛔ NOT FIXED · ⛔ NO SCENARIO LOGIC TOUCHED.**

⭐ **It is a LOG-LEGIBILITY defect, ⛔ not a behavioural one** — a reader of
`system_<date>.log` sees `startup_scenario=CRASH` eight lines after
`startup_scenario=COLD` and reasonably concludes the system thinks it crashed.
⚠️ 🔬 It cost real investigation time on 26-Aug **and** 27-Aug.

⭐ **Cheapest future fix, recorded ⛔ not built:** have the second call either reuse the
first result or log at DEBUG with an explicit *"advisory; only HALT is consumed"*
qualifier. ⛔ **Out of scope tonight** — ⭐ tonight is the MIS orchestrator.

---

## WHAT IS NOT MEASURED

1. ⛔ Whether the double call is deliberate — 💭 INFERENCE, ⛔ not investigated.
2. ⛔ The WARM arm — 🏷️ **NOT EXERCISED**: it needs a same-day restart *after* a
   clean shutdown, which the 08:15 boot never is.
3. ⛔ The HALT arms (HARD_KILL / same-day SOFT_KILL) — 🏷️ **NOT EXERCISED** today;
   ⭐ note the prior-day SOFT_KILL correctly *falls through* (step 3), as observed at
   `08:15:14.290` `KILL_AUTO_CLEARED`.
4. ⛔ Nothing changed. ⛔ No fix built.

⛔ executed ≠ exercised · ⛔ a log line ≠ a decision · ⭐ **a value that no consumer
reads cannot change behaviour, however alarming it looks.**

## END
