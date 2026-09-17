# F2 SCOPING · Q-1 SEPARABILITY · TERMINOLOGY · THE MEMORY CONTRADICTION

**25-Aug-2026, IST.** 🔴 SCOPING ONLY. ⛔ No code · no design · no config schema · no capital model ·
no implementation sizing · no push · no service action.
**Provenance:** 🔬 measured · 📄 source-derived · 💭 inference · 👤 Rama.
⚠️ **M3:** every line cite holds at deployed HEAD **`195436bb…`**, tree drift **0**. ⛔ Nowhere else.

---

# 🔴 Q-1 — IS THE EOD-GATE FIX SEPARABLE FROM F2?

## 🏷️ ANSWER: **YES — SEPARABLE.** ⛔ Answered from source + data, ⛔ not by reasoning.

💭 The card's inference was that it *"needs a pipeline dimension on 'active position' — which is F2's
item 4."* 🔬 **Measured: that dimension already exists and is already reliable.**

### Evidence 1 — the product dimension exists today

🔬 `product` is derivable now via `orders LEFT JOIN … AND o.leg='ENTRY'` — the standing schema fact
(there is no `trades.product` column). ⛔ It needs nothing F2 would build.

### Evidence 2 — the known NULL hazard does **not** reach the gate's status set

⚠️ The standing warning is that a LEFT JOIN yields `product NULL` for a missing ENTRY row, making the
trade **invisible to any product filter**. 🔬 **Measured, whole table (730 trades):**

| trade status | NULL product | total | reaches the EOD gate? |
|---|---|---|---|
| REJECTED | **80** | 80 | ⛔ no |
| FAILED | **68** | 345 | ⛔ no |
| CANCELLED | 0 | 9 | ⛔ no |
| CLOSED | 0 | 240 | ⛔ no |
| CLOSED_MANUAL | 0 | 52 | ⛔ no |
| **OPEN** | **0** | 4 | ✅ **yes** |

⇒ 📄 **The hazard is structurally confined to trades that never reached the broker** — no broker
order ⇒ no ENTRY row ⇒ NULL. 🔬 **Across `OPEN` / `PARTIAL` / `PENDING_FILL` — the exact and only
statuses `_eod_self_exit_due` reads — NULL is ZERO.**
⚠️ ⭐ **But this is an observation, ⛔ not a guarantee.** The rule that follows is a REQUIREMENT, not a
convenience: **any pipeline-scoped count must be FAIL-CLOSED** — `NULL` ⇒ *unknown pipeline* ⇒ **keep
the service up.** ⛔ Never fail-open, or the defect inverts into "exits while a position is live."

### Evidence 3 — 🔴 the constraint that actually bounds the change

🔬 `count_active_positions()` (`core/state_store.py:639`) has **THREE production consumers**, ⛔ not one:

| consumer | file:line | what it governs |
|---|---|---|
| `_eod_self_exit_due` | `main.py:1109` | 🔴 the process lifecycle — **F6's defect** |
| `risk_engine` OPEN_POSITIONS (RE5) | `capital/risk_engine.py:303` | ⚠️ **a LIVE RISK CAP** |
| `portfolio_allocator` `active_count_fn` | `main.py:3207` → `allocation/portfolio_allocator.py:42` | allocation |

⇒ 🔴 **Changing `count_active_positions()` ITSELF is NOT separable** — it would move a live risk cap
and the allocator in the same stroke. ⭐ **Adding a SEPARATE pipeline-scoped count consumed ONLY by
the EOD gate IS separable**: one new read, one call site, ⛔ zero change to the existing three.

## Q-2 — the smallest change, ⛔ SCOPED ONLY

⛔ Not designed, ⛔ not sized, ⛔ not built. **What it would touch:** one new pipeline-scoped read
alongside `count_active_positions()`, and the single call site at `main.py:1109`.
**What it must NOT touch:** `count_active_positions()` itself · `risk_engine.py:303` ·
`main.py:3207` · the kill switch · any capital, config or sizing surface.
**Two properties it must carry:** ① **fail-CLOSED** on `NULL`; ② it inherits the same
**EXITING-blindness** the current count has (`main.py:1055`) — the HARD_KILL flatten gate
(`_ACTIVE_FLATTEN_IN_PROGRESS`) remains the separate, load-bearing guard and ⛔ must not be folded in.

## ⇒ Q-3 does not apply. ⛔ F2-07 need not absorb it.

⭐ **Why this matters right now:** the hazard is **LIVE every night a CNC carries**, and today it is
mitigated only by 👤 Rama remembering a manual stop. ⭐ Separability means it does **not** have to
wait for F2.

---

# §2 · TERMINOLOGY — PERMANENT, IN THE RECORD

⭐ **Correct:** *"logical pipeline independence"* · *"pipeline-separated trading/risk logic."*
⛔ **NEVER:** *"fully operationally independent pipelines."*

⭐ **Three things that must never be merged:**

| | where it lives | survives a service stop? |
|---|---|---|
| **GTT PROTECTION** | broker-side, rests at Zerodha | ✅ yes |
| **GTT REPAIR** | service-side, **in-hours only** | ⛔ no |
| **SERVICE LIFECYCLE** | one process, shared | 🔴 shared by both pipelines |

⛔ ***"Stopping the service does not remove a resting OCO"* must NEVER be read as *"therefore MIS and
Delivery are independent."*** ⭐ The first is about **protection**; independence is about **control**.

⭐ **And the distinction that goes into F2's constraints verbatim:**
**SHARED INFRASTRUCTURE** (one process, DB, logging, market data) — **acceptable.**
🔴 **SHARED CONTROL** (one pipeline's state governs another) — **the thing being removed.**

---

# ⚠️ §4 · THE MEMORY CONTRADICTION — RECONCILED AND MEASURED

## 🏷️ BOTH MEASUREMENTS WERE CORRECT. THE 23-AUG **CONCLUSION** WAS WRONG IN SCOPE.

🔬 **23-Aug is still true, re-verified today:** MEMORY.md is **129 lines** against a 2,000-line Read
limit, and `check_memory_budget.py` **does not exist** anywhere under `~/.claude` (searched). ⛔ No
line-based truncation; ⛔ no enforcing script.

🔴 **But the real limit is a CHARACTER budget applied at AUTO-LOAD — a different mechanism entirely,
which the 23-Aug check could not have found because it only looked at lines and at a script.**
⭐ This is the standing rule firing on my own record: *an absence needs a check wide enough to have
found the thing.*

### 🔬 M-1 — what the budget actually is

| quantity | value |
|---|---|
| MEMORY.md bytes | **27,814** |
| MEMORY.md characters (`wc -m`) | **26,144** → **25.5 KB** |
| harness-reported size | **25.5 KB** ✅ **exact match** |

⇒ 📄 **The unit is CHARACTERS, ⛔ not bytes.** The 1,670-byte gap is UTF-8 emoji (3–4 bytes each) —
⭐ which is why a file that "looks" 27 KB is measured 25.5 KB.
📄 The **24.4 KB** figure is the **read limit**; the **17.1 KB** figure is the **rewrite target**
(70% of it). ⛔ Neither is a project hook — nothing in `.claude/settings*.json` enforces it; it is
**harness-built-in**, surfaced as a `PostToolUse` notice and as the session-start warning.

### 🔴 M-2 — does anything ACTUALLY drop? **YES. MEASURED, NOT INFERRED.**

⭐ The decisive test: compare what this session **received** against what the file **contains**.

🔬 Limit ≈ **24,985 chars** ⇒ the cut lands at **line ~121**. 🔬 This session received **lines 1-120**,
ending mid-`### Tests`. 🔬 The file has **129 lines**. ⇒ 🔴 **LINES 121-129 WERE NEVER DELIVERED.**

🔴 **What was silently missing at session start:**
- `## The CAREFUL-LOOP queue` — ⭐ *anything touching capital, kill, order, schema, sizing or a live
  trading decision goes through design → review → implement.*
- `## RAMA-ACTIONS owed` — ⭐ **commit `nse_holidays_2027.yaml` BEFORE 31-Dec-2026, or the first
  08:15 boot of 2027 does not start.**

⚠️ ⭐ **A dated safety deadline was invisible to the agent expected to honour it.** ⇒ *"silently
dropped"* is ⛔ **not** an inherited phrase — 🔬 it is measured, and this session was a live instance.

### ⛔ NOT REPAIRED — and the consequence that binds every future batch

⛔ No restructure (👤 not authorised). ⚠️ 🔴 **Adding any line to MEMORY.md now pushes MORE content off
the end.** ⇒ ⛔ **Do not add HOT lines until the index is under budget** — edit an existing line, or
write to a topic file / the ledger. ⭐ This session followed that rule: **both** MEMORY.md edits were
made **net-neutral or shrinking**, and all new detail went to topic files and the ledger.
🏷️ **OWED TO 👤 RAMA: a decision on the index rebuild.** ⛔ Not taken unilaterally.

---

# §5 · F2 SCOPING — THE LIFECYCLE CONTRACT

⛔ Scoping only. ⛔ No capital model, ⛔ no config schema, ⛔ no sizing, ⛔ no code.

## What F2 inherits as MEASURED FACT (⛔ not assumption)

One process hosts both pipelines · the active-position count is product-blind · delivery GTT
protection is broker-side · GTT repair is service-side and in-hours-only · `delivery_enabled` is an
entry-control precedent but is **boot-time** · the kill switch is a **carve-out with no pipeline
argument** · lifecycle is whole-service ⇒ 🔴 **the current architecture HAS shared lifecycle coupling.**

## 🔴 THE SIX CLAUSES THE LIFECYCLE CONTRACT MUST CONTAIN

⛔ Named, ⛔ not designed. A contract that omits any of these is incomplete.

1. **WHO MAY HOLD THE PROCESS OPEN PAST EOD.** Today: *anyone* — that is the defect. The contract
   must state the rule, and the discriminator the evidence hands it is *whose protection is
   service-dependent*.
2. **WHAT HAPPENS TO PIPELINE B WHILE PIPELINE A HOLDS THE PROCESS OPEN.** Today unstated, and the
   answer is currently *"B is silently disabled tomorrow."*
3. **WHAT A PIPELINE HALT MEANS.** Must be **entries only, never protection** — the R2 guard split
   already settles this and F2 must adopt it rather than re-decide it.
4. **WHAT IS GUARANTEED WHILE THE PROCESS IS ABSENT.** Broker-side protection persists; **repair does
   not**. The contract must name the repair gap, ⛔ not paper over it.
5. **WHAT MUST BE TRUE AT THE NEXT BOOT** for each pipeline to trade — including that the kill
   auto-clear is boot-bound, so *"no boot"* silently means *"no entries."*
6. **WHICH SHARING IS PERMITTED.** Infrastructure yes; **control no** — stated per shared surface,
   ⛔ not as a slogan.

## The six acceptance scenarios, against measured reality

| | scenario | today | reachable **without** changing the shared-process model? |
|---|---|---|---|
| **A** | MIS halts ⇒ MIS entries stop, MIS exits handled, Delivery continues | ⛔ no — `SOFT_KILL` blocks **all** entries | ✅ yes — needs a pipeline-scoped entry permission |
| **B** | Delivery halts ⇒ Delivery entries stop, protection remains, MIS continues | ⚠️ partly — `delivery_enabled` does exactly this, but **boot-time only** | ✅ yes — make it runtime |
| **C** | 🔴 Delivery carries overnight ⇒ protection valid **AND MIS operates next session** | 🔴 **FAILS TODAY** — F6's defect | ✅ **yes** — Q-1's separable fix; ⛔ needs no process split |
| **D** | MIS state persists ⇒ Delivery independently operable | ⛔ no — global kill | ✅ yes — pipeline-scoped kill |
| **E** | Both active ⇒ neither halt mutates the other's risk/entry state | ⛔ no — shared counters/kill | ✅ yes — pipeline-scoped counters |
| **F** | Whole process fails ⇒ broker protection remains, repair limits named | ⚠️ true but **undocumented** | ✅ yes — it is a documentation obligation |

## ⭐ 👤 THE EXPLICIT REPORT §5 ASKS FOR

🏷️ **TRUE LIFECYCLE INDEPENDENCE, AS THE SIX SCENARIOS DEFINE IT, IS REACHABLE WITHOUT CHANGING THE
SHARED-PROCESS MODEL.** 📄 Because delivery's protection is broker-side, nothing in A–F requires a
second process; every gap is **shared CONTROL** (a global kill, a product-blind counter, a boot-time
flag), ⛔ not shared infrastructure.

⚠️ 🔴 **BUT ONE LIMIT IS IRREDUCIBLE IN A ONE-PROCESS MODEL, AND F2 MUST NOT CLAIM PAST IT:**
**a whole-process failure takes BOTH pipelines down simultaneously.** ⭐ Scenario F already concedes
this by asking for *"repair limits named"* rather than continued operation. ⇒ ⛔ **F2 may claim
logical/control independence; it may NOT claim process-level fault isolation.** ⭐ That is exactly why
the terminology rule in §2 is permanent and not cosmetic.

---

# 🔴 STATUS OF THE LIFECYCLE CONTRACT: **INCOMPLETE**

⛔ **This contract is INCOMPLETE and must be labelled so wherever it is cited.** Two clauses cannot
be written until 👤 Rama answers them **in his own words**:

| # | open question | state |
|---|---|---|
| ① | **Which pipeline may legitimately hold the shared process open past EOD?** | 🏷️ OPEN — a recommendation (*MIS only*) is on record; ⛔ a reviewer's ruling on it is **NOT** accepted as settled (`WC-PATTERN #8`, instance 3) |
| ② | **What is the intended EOD condition?** | 🏷️ OPEN |

⛔ **Neither may be silently filled.** ⭐ Everything else below is settled and measured.

---

# §3 · THE CONTRACT CLAUSE — ADDED VERBATIM (👤 Rama)

> **"A pipeline's ability to hold or release the shared process must never be inferred indirectly
> from a global product-blind position count."**

⭐ **It prohibits the PATTERN, ⛔ not merely today's line.** ⚠️ The defect arose from an *accidental*
coupling of exactly that shape — a lifecycle decision reading a counter built for a risk cap. ⛔ A
contract that bans only `main.py:1109` leaves tomorrow's equivalent free.

## The permanent distinction — ⛔ never collapsed

| | status |
|---|---|
| ⭐ **PIPELINE CONTROL / RISK INDEPENDENCE** | F2's target — 🔬 **measured REACHABLE** without changing the shared-process model, because delivery protection is broker-side and every remaining gap is shared **CONTROL** |
| 🔴 **PROCESS FAULT ISOLATION** | ⛔ **NOT provided by a single process, and F2 may never claim it.** A whole-process crash necessarily takes both pipelines down |

⇒ ⭐ After F2, *"MIS and Delivery are independently controlled pipelines inside one trading system"*
is **accurate**. ⛔ *"A process failure cannot affect either"* is **not**.

## ⭐ AND: DAILY HALT ≠ PROCESS STOP
A pipeline halt stops **NEW ACTIVITY for that pipeline**. ⛔ It does not stop the system, and ⛔ it
does not remove protection for open positions.

---

# §4 · THE TEN QUESTIONS — SCOPING ANSWERS

⛔ Plain language. ⛔ No design, ⛔ no sizing, ⛔ no code. 🔬 = measured today · 🏷️ = **decision owed to
👤 Rama** (⛔ mine to scope, ⛔ not to take).

**1 · What exact condition allows the shared process to remain alive past EOD?**
🔬 **Today:** it exits only when `now ≥ 17:35` **AND** no HARD_KILL flatten is in flight **AND**
`count_active_positions() == 0` — product-blind. ⇒ **any** open trade in **either** book holds it up.
🏷️ The contract must state the *intended* condition. ⭐ The discriminator the evidence hands it:
*whose protection is service-dependent.*

**2 · Which pipeline(s) may legitimately cause that condition?**
🔬 **Today: both.** ⭐ Evidence-based candidate: **MIS only** — delivery is broker-protected, so a
delivery carry has no protection reason to hold the process. 🏷️ **Rama's decision, ⛔ not mine.**

> 🔴 **⛔ STILL OPEN — AND A RULING WAS TAKEN ON IT WITHOUT AUTHORITY.** 📄 A reviewer answered this
> question (*"ONLY MIS MAY LEGITIMATELY KEEP THE SHARED PROCESS ALIVE PAST EOD"*) after it had been
> deliberately left with 👤 Rama. 🏷️ **Recorded as `WC-PATTERN #8`, instance 3.**
> ⭐ The substance is probably right and it **matches the candidate above** — ⛔ but *derivable is not
> decided*, and a reviewer cannot convert a good argument into a ruling.
> ⇒ 🏷️ **HELD AS A RECOMMENDATION AWAITING RAMA'S WORDS.** ⛔ NOT settled. ⛔ NOT written into the
> contract.

**3 · What happens to the OTHER pipeline while that condition exists?**
🔴 **Today: it is silently disabled the next day.** Process stays up → still `active` at 08:15 →
`token_watcher` does nothing → no boot → the 15:15 `SOFT_KILL` never auto-clears → **no entries in
either book.** ⭐ The contract must require that the other pipeline is **unaffected**.

**4 · What does "halt" mean for each pipeline?**
🔬 **Today:** `SOFT_KILL` = a **global** entry block (exits still run, delivery not squared off);
`delivery_enabled=false` = CNC `place_order` blocked, **GTT ops untouched**.
⇒ ⭐ Two different halt meanings already coexist. 🏷️ The contract must define ONE per pipeline:
**new activity stops, the system does not, protection does not.**

**5 · What protection remains active during a halt?**
🔬 **Measured: all of it.** `SOFT_KILL` never flattens; `HARD_KILL` flattens MIS/CO only and delivery
survives by design; the broker OCO is explicitly **not** gated on `delivery_enabled` (R2 guard split).
⇒ ⭐ *Protection is already invariant under halt* — F2 must **preserve** this, ⛔ not re-decide it.

**6 · What must be reconstructed at the next boot?**
🔬 `gtt_state` is durable and is the authority; `CncGttPlacer.hydrate_from_store()` rebuilds the
in-memory map; `_preopen_queue` is in-memory and is re-derived from `gtt_state`; the kill auto-clear
is **boot-bound**; daily counters are **clock-bound**. 🏷️ The contract must enumerate this **per
pipeline** — ⚠️ the boot-bound kill clear is precisely what makes *"no boot"* mean *"no entries."*

**7 · Which shared resources are INFRASTRUCTURE only?**
🔬 Candidates measured in the tree: the process itself · the SQLite store · logging · market
data/`candle_store` · the broker session/token · the webhook server. 🏷️ The contract must **list**
them, so anything not listed is presumed control-bearing until proven otherwise.

**8 · Which shared states are FORBIDDEN from controlling the other pipeline?**
🔬 **Currently violating, all three measured:** ① `count_active_positions()` — lifecycle **and** the
`risk_engine` cap **and** the allocator; ② the **global kill-switch state** (no pipeline argument);
③ the single `tier_multipliers` dict that serves **both** books. ⇒ ⭐ These are the concrete targets
of §3's clause.

**9 · What happens if the entire process crashes?**
🔬 `Restart=on-failure`, `RestartSec=10`, `RestartPreventExitStatus=3 4 5`. Broker-side OCO
protection **persists**; **repair capability does not**; **both pipelines go down together.**
⭐ The contract must name the repair gap — ⛔ and must not describe this as isolation.

**10 · Which parts are logical/control independence, and which are impossible without process
separation?**
🔬 **Reachable in one process:** all six scenarios — A, B, D, E, F, **and C** (Q-1's separable fix).
🔴 **Impossible without process separation:** **fault isolation.** ⛔ One crash takes both down, and
no amount of pipeline-scoping changes that.

## 🔴 SCENARIO C REMAINS THE HEADLINE ACCEPTANCE TEST
*Delivery carries overnight → its protection stays valid → **AND MIS STILL OPERATES NEXT SESSION.***
⚠️ **It fails today.** ⭐ A system passing A and B but failing C is ⛔ **not** independent in the sense
👤 Rama requires. ⛔ Scenarios are **acceptance criteria**, ⛔ not implementation instructions.

⚠️ ⭐ **AND ONE INHERITED RULE F2 MUST CARRY EXPLICITLY** (currently invisible in the memory index —
`docs/audit/MEMORY_TRUNCATION_INVENTORY_25-Aug-2026.md`): **paper nets by *SYMBOL* while live Kite
nets per *(SYMBOL, PRODUCT)* ⇒ a paper drill of any product-semantics change is vacuously GREEN.**
🔴 **F2 is entirely a product-semantics change** ⇒ ⛔ a green paper validation of F2 proves nothing.

---

## ⛔ STATE

⛔ **NOTHING BUILT · NOTHING PUSHED · NOTHING TOUCHED.** No code, no design, no config, no service
action. Every VM call a read. 🔬 `origin/main` = `195436bb…` unchanged; deployed-tree drift **0**.
⛔ F6 not reopened. ⛔ No F2 implementation. ⛔ The eight closed decisions untouched — including
**MIS leverage 5×** (⛔ 3.5× is 70% × 5 and is never the leverage).
