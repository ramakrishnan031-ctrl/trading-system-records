# F · D-1b NOTIFICATION UNIT — SPECIFICATION

**Written 28-Aug-2026, after the `effff24` release gate closed.** ⛔ Nothing here
reopens that gate. ⭐ This is the weekend's **priority** unit.

🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S · 🏷️ NOT EXERCISED.

---

## 1 — WHY F EXISTS

🔬 The MIS orchestrator (`effff24`) emits **CRITICAL** on four states:
`DEADLINE_BREACH` · `MIS_REMAINS` · `CANCEL_FAILED` · `BROKER_STATE_UNAVAILABLE`.

🔴 **If those are log-only when the unit first executes live on Monday at 15:07 —
with real exit orders in flight — nobody learns until someone next looks.**

⭐ F does **not** enable intervention. 🔬 PASS 2's measured-bound execution is **≈2 s**
⇒ ⛔ nobody reads an alert and acts inside that. ⭐ **F buys a same-day response
instead of an unbounded one.** That is the whole claim.

---

## 2 — 🔴 THE CHICKEN-AND-EGG, AND THE SEVEN-HOUR GAP

⚠️ F ships Sunday night and boots **Monday 08:15** ⇒ ⭐ **F's own first live
execution is also Monday**, and it is expected to report on the **orchestrator's**
first live execution.

> 🔴 **Two untested-in-production units, mutually dependent, on the same day.**
> ⚠️ If F's transport is silently broken, the 15:07 CRITICAL is **exactly as
> invisible as with no F — but now with a FALSE BELIEF that it is covered.**
> ⛔ **That is worse than no F.**

### ⭐ SELF-TEST 1 — AT BOOT (~08:15)

⭐ A **benign** startup notification, email **and** telegram, **every boot**, ⛔ not
only on CRITICAL. ⇒ ⭐ proves the transport **seven hours before 15:07 needs it**.

### 🔴 SELF-TEST 2 — AT `CHECK_1 − 2 min` (~15:05) — because boot health ≠ health at use

⚠️ **A transport healthy at 08:15 can be dead at 15:07:** a revoked bot token · an
expired SMTP session · a network change · a rate limit reached during the day.
⛔ **None of those is visible at boot.**

> ⇒ ⭐ **A SECOND SELF-TEST AT ~15:05 — two minutes before it matters, ⛔ not seven
> hours.** One extra INFO line per trading day.

⭐ **AND IT LARGELY REPLACES THE MONDAY WATCH.** 👤 Rama receives *"MIS pass due in
2 minutes; alerting live"*, then either **silence** (the pass ran clean) or a
**CRITICAL**. ⭐ That is the closest thing to live observation that requires ⛔ no
session at 15:07.

⚠️ **KEEP IT INFORMATIVE, ⛔ NOT NOISE.** One line, `NOTIFICATION_SELF_TEST` / INFO,
unmistakably distinct from the four CRITICAL states. ⭐ If the 15:05 line becomes
something 👤 Rama ignores, **it is worse than nothing**.
⛔ **Do NOT run the scan at 15:05 to enrich it** — ⭐ scope creep; the scan belongs
at 15:07.

---

## 2a — 🔴 CONFIG COUPLING = YES · EXECUTION COUPLING = **NO**

⭐ The ~15:05 trigger must be **derived from the authoritative schedule**, ⛔ never
hardcoded as `15:05` — otherwise F drifts the moment a holiday or special session
moves `CHECK_1`.

🔴 **But there are two ways to derive it, and only one is safe:**

| | approach | verdict |
|---|---|---|
| ✅ | **CONFIG-COUPLED** — F reads `mis_squareoff_cutoff` + `first_offset` from the **same config** and computes its own trigger on its **own timer** | ⭐ moves when the cutoff moves |
| ⛔ | **EXECUTION-COUPLED** — F hangs off the orchestrator's scheduler / poll loop / fired-flag machinery | 🔴 **FORBIDDEN** |

> ## 🔴 **EXECUTION COUPLING CREATES THE EXACT FAILURE F EXISTS TO DETECT.**
> ⚠️ If the orchestrator's scheduler is broken such that `CHECK_1` never fires, a
> scheduler-derived pre-pass self-test **never fires either** ⇒ ⭐ **both go silent
> together**, and the one thing meant to report on the other is **taken out by the
> same fault**.

⚠️ ⭐ **And this is not a hypothetical framing.** 🔬 **Scheduler semantics are NOT
TRACED** — what `_cnc_monitor_every` counts, its unit, the market-hours gating,
shutdown behaviour. ⛔ **Do not couple F to an untraced mechanism.**

⇒ ⭐ **F reads the config; ⛔ F does not ride the orchestrator's scheduler.**
⭐ Same source of truth for the **time**; ⛔ independent path for the **firing**.

⭐ This is the concrete form of *"Q1 (F fired on time) ≠ Q2 (PASS 1 ran on time)"* —
⇒ ⛔ they cannot be independent observations if one is **derived from the other's
execution**.

---

## 2a-i — ⭐ THE INDEPENDENCE TEST · **CONSTRUCT F WITH NO ORCHESTRATOR AT ALL**

⚠️ A suppression test (*"disable the orchestrator's CHECK_1 while letting F's timer
fire"*) proves F survives **one particular suppression**. ⛔ It does **not** prove F
has no dependency.

> ## ⭐ **THE DISPOSITIVE FORM:**
> *If F can be instantiated **from configuration alone** and fire its pre-pass
> self-test in a test where **NO ORCHESTRATOR OBJECT EXISTS**, execution
> independence is **proven**, ⛔ not inferred.*

⭐ **And it is CHEAPER** — ⛔ no suppression harness, ⛔ no partial-orchestrator
fixture. ⭐ Just: **config in, self-test out.**

⭐ **IT MIRRORS A PATTERN ALREADY PROVEN IN THIS REPO** — U3-c's *"a missing map
cannot resurrect hardcoded leverage."* ⭐ Same shape: prove the absence of a
dependency by **removing the dependency entirely**, ⛔ not by disabling it.

⭐ **MUTATION:** wire F's trigger to **any** orchestrator artefact ⇒ 🔴 the
no-orchestrator test goes **RED**. ⇒ ⭐ that is the invariant, ⛔ not a code reading.

⚠️ ⛔ **DO NOT OVERCLAIM WHAT IT PROVES.** ⭐ It establishes independence from the
**orchestrator's execution scheduler**. ⛔ It says nothing about a dead process, an
unavailable VM, a wrong clock, or a dead network — ⭐ F still shares **host, process,
runtime, clock and network stack**. ⛔ *"Not coupled to the orchestrator"* must never
be paraphrased as *"independent of all failures."*

⭐ If the test cannot be run safely ⇒ **NOT PROVEN.** ⛔ Never a manufactured green.

---

## 2a-ii — 🔴 THE COUPLING VECTOR THE EXECUTION LIST MISSES: **SHARED MUTABLE STATE**

⚠️ The obvious review list is all **execution** artefacts: the CHECK_1 fired flag ·
a PASS 1 callback · the orchestrator's poll function · retry/fired state ·
*"register after PASS 1"*.

> ## 🔴 **MISSING: F READING A VALUE THE ORCHESTRATOR COMPUTED AND STORED.**
> ⭐ A cached `check_1_ts` on the orchestrator object · a timing object the
> orchestrator populates at startup · a lazily-initialised schedule.
> ⇒ ⚠️ **F is then coupled even though it owns its timer.**

🔴 An orchestrator that fails **before** computing CHECK_1 leaves F with **no trigger
at all** — ⭐ exactly the silent-together failure, ⚠️ arriving through the **data**
path instead of the **execution** path.

### 🔬 AND THIS IS A LIVE RISK IN THE SHIPPED CODE, ⛔ NOT A HYPOTHETICAL

🔬 `MisAutoSquareoff` holds a `MisSquareoffTiming` instance as `self._t`, built at
construction by `MisSquareoffTiming.build(...)`. ⚠️ **The obvious wiring would hand F
that same object** — `mis_autosq._t` — or pass the orchestrator itself.

> ⭐ **THE RULE: F CALLS `MisSquareoffTiming.build(...)` ITSELF, FROM CONFIG.**
> ⛔ **Never** `orchestrator._t`. ⛔ **Never** the orchestrator instance.
> ⭐ Same *validated constructor*, ⭐ same *config source* — ⛔ **separate object,
> separately built.**

⭐ **ADD TO THE COUPLING REVIEW:** any read of orchestrator-owned attributes · any
shared timing/schedule object · any lazily-computed value the orchestrator
initialises · **any import that pulls orchestrator construction in as a side
effect**.

✅ ⭐ **AND §2a-i's TEST CATCHES THIS FOR FREE** — ⇒ with no orchestrator present, any
such read fails immediately. ⭐ **One test, both coupling classes.**

---

## 2a-iii — 🔴 THE `sys.modules` ASSERTION · AND THE FINDING IT IMMEDIATELY PRODUCES

⭐ *"The fixture must be authoritative"* is a **judgement call**. ⭐ Make it mechanical:

> ## ⭐ **At the moment the pre-pass self-test FIRES in the test, assert the orchestrator module is ABSENT from `sys.modules`.**

⇒ ⭐ If it is absent then ⛔ no orchestrator object can exist · ⛔ no orchestrator
helper can be called · ⛔ no import side effect can have run · ⛔ no module-global the
orchestrator populates can be present. ⭐ **All four coupling routes closed by one
assertion**, one line, RED-capable.

⚠️ ⛔ Do **not** weaken it to *"the fixture looks clean"* or *"no orchestrator object
was constructed."* ⭐ The assertion is about the **MODULE**, ⛔ not the object — ⭐ a
lazy dependency needs only the module to be present.

### 🔴 AND TAKING IT LITERALLY PRODUCES A FINDING IN THE **SHIPPED** CODE

🔬 **MEASURED against `effff24`:**

```
orders/mis_autosquareoff.py:152   class MisSquareoffTiming      <- the contract F needs
orders/mis_autosquareoff.py:263   class MisAutoSquareoff        <- the orchestrator

>>> from orders.mis_autosquareoff import MisSquareoffTiming
    'orders.mis_autosquareoff' in sys.modules  ->  True
    MisAutoSquareoff reachable from it         ->  True
```

> ## 🔴 **THE TWO CONSTRAINTS ARE UNSATISFIABLE AS THE CODE STANDS.**
> ⭐ §2a-ii requires F to call `MisSquareoffTiming.build(...)` itself.
> ⭐ §2a-iii requires `orders.mis_autosquareoff` to be **absent** from `sys.modules`.
> ⚠️ **But the timing contract lives INSIDE the orchestrator's module**, so importing
> the one imports the other.

⭐ **This is exactly the case FILE 47 §1 said not to exempt.** ⛔ Do not carve out an
allowance. ⭐ **Report it and fix the structure.**

### ⭐ THE RESOLUTION — a MOVE, ⛔ not a behaviour change

⭐ **Extract the timing contract into its own module** — `MisSquareoffTiming` ·
`MisSquareoffConfigError` · `_parse_hhmm` · `_parse_offset_minutes` — e.g.
`core/mis_squareoff_timing.py`.

```
core/mis_squareoff_timing.py     <- the validated contract, imported by BOTH
        ^                    ^
        |                    |
orders/mis_autosquareoff.py   F   <- F imports ONLY the contract module
   (re-exports for existing
    imports, so the 59 shipped
    tests keep working)
```

⇒ ✅ F imports `core.mis_squareoff_timing` only ⇒ ⭐ `orders.mis_autosquareoff` stays
**absent** from `sys.modules` ⇒ ⭐ the assertion holds.
⇒ ✅ Both still share the **CLASS** (config coupling, desirable).
⇒ ✅ Neither shares an **INSTANCE** (data coupling, forbidden).

⚠️ **THIS IS A CHANGE TO ALREADY-PUSHED CODE** (`effff24`) ⇒ ⭐ it is **Saturday's
FIRST task**, inside F's unit, with F's gate. ⭐ It is a **move + re-export**, ⛔ not a
behaviour change — 🔬 the 59 shipped tests import from `orders.mis_autosquareoff` and
must **still pass unchanged**. ⛔ If any behaviour moves, that is a separate finding.

---

## 2a-iii-b — 🔴 THE EXTRACTION IS A CHANGE · ⭐ IT NEEDS ITS OWN THREE CHECKS

⭐ SAT TASK 1 is not free. ⛔ An extraction that "looks right" is not verified.

### ✅ CHECK 1 — ASSERT THE **DIRECTION**, ⛔ not merely that tests pass

🔴 **An extraction only breaks the cycle if the new module does NOT import back.**
⚠️ A single type hint · a shared constant · a helper · an `if TYPE_CHECKING` block
that later becomes a real import ⇒ ⛔ the contract module reaches the orchestrator
again and ⭐ the `sys.modules` assertion **still fails**.

> ⭐ **ASSERT MECHANICALLY: the contract module's import graph does NOT reach the
> orchestrator module.** ⭐ Statically checkable, ⭐ and it is the extraction's
> **actual success criterion** — ⛔ not *"the tests still pass."*

⭐ **INTENDED SHAPE:**

```
contract module      ->  (nothing from the orchestrator)
orchestrator module  ->  imports contract, RE-EXPORTS it
F                    ->  imports the CONTRACT MODULE ONLY
```

⚠️ 🔴 **AND THE RE-EXPORT IS ITSELF A LATENT RISK.** ⭐ After it,
`from orders.mis_autosquareoff import MisSquareoffTiming` **still works** ⇒ a future
developer can "simplify" F's import back to the orchestrator module and ⛔ silently
destroy the independence.

⇒ ✅ ⭐ **The re-export and the `sys.modules` assertion are a MATCHED PAIR: the
re-export creates the hazard, the assertion holds the line.** ⛔ Neither is optional.

### ✅ CHECK 2 — 🔴 THE 59 SHIPPED TESTS ARE THE **WRONG** SAFETY NET HERE

⚠️ Those tests import `MisSquareoffTiming` **from the orchestrator module** ⇒ ⭐ via
the re-export they pass **either way**.

> ⇒ ⭐ **They prove the RE-EXPORT works. ⛔ They do NOT prove the extraction was
> behaviour-neutral for the orchestrator.**

⭐ **THE REAL NEUTRALITY CHECK is the full differential against `effff24`:** same
failure IDs · **new-failure set EMPTY** · and —

> ## 🔴 **THE TEST-COUNT DELTA MUST BE EXACTLY ZERO.**
> ⭐ *"Move + re-export"* is the claim. ⭐ **A pure move adds no tests.**
> ⇒ ⚠️ **A non-zero delta means it was not a pure move** — ⛔ a finding, ⛔ not a
> rounding detail.

🔬 **CONCRETE BASELINE FOR SATURDAY:** `effff24` = **`10 failed · 5,956 passed ·
4 skipped`**, fingerprint `46c38a3eee03d34be8defedba73421c803c6ba42e05375a8968632e4cb118f0b`.
⇒ ⭐ **Commit 1 must reproduce `10 / 5,956 / 4` EXACTLY.**

⚠️ ⭐ **AND IF ANY BEHAVIOUR MOVES, THAT IS A SEPARATE FINDING** — ⛔ it does not get
absorbed into "the extraction". ⭐ Report it on its own.

### ✅ CHECK 3 — ⭐ SATURDAY IS **TWO** CHANGES · SEPARATE COMMITS, EXTRACTION FIRST

⭐ The extraction touches **already-pushed code** (`effff24` is on the VM). ⭐ F is new
code. ⇒ ⚠️ **Saturday is no longer one change.**

| | commit | its own gate |
|---|---|---|
| **1** | **the extraction** | direction assertion · **delta ZERO** · 59 green · differential clean |
| **2** | **F itself** | TESTS A–F · the full acceptance list |

⭐ **WHY:** if Monday's boot fails, *"was it the extraction or F?"* must be
answerable. ⚠️ ⭐ This is the 24-Aug lesson **one level deeper** — ⛔ it now applies
**inside** Saturday, ⛔ not only between F and F2-CORE.

⇒ ⭐ Monday's attribution therefore has **THREE** component identities: **extraction ·
F · F2-CORE** (if it ships). ⭐ Combined SHA = release identity; ⛔ *"the combined tree
booted"* must not hide which of the three ran.

✅ ⭐ **AND COMMIT 1 IS INDEPENDENTLY VALUABLE** — ⭐ if F does not finish, the
extraction still ships as a clean structural improvement, ⛔ and F's blocker is
removed for whenever it does.

### ✅ CHECK 0 — THE PACKAGE INITIALISER · **PRE-VERIFIED 28-Aug, ⛔ NOT LEFT TO SATURDAY**

⚠️ 🔴 **THE BLIND SPOT:** if `orders/__init__.py` imports `mis_autosquareoff` — a very
common convenience re-export — then:

```
from orders.<contract> import MisSquareoffTiming
   -> Python imports the `orders` PACKAGE first
   -> runs orders/__init__.py
   -> which imports mis_autosquareoff
   -> the orchestrator module is now in sys.modules
```

⇒ 🔴 **The contract module's own import graph would be clean and the assertion would
STILL fail.** ⭐ Importing *anything* from the package would drag the orchestrator in.

🔬 **MEASURED 28-Aug, before writing any extraction code:**

| check | result |
|---|---|
| `orders/__init__.py` size | 🔬 **0 bytes — empty** |
| `import orders` ⇒ orchestrator in `sys.modules`? | ✅ **False** |
| `from orders import eod_squareoff` ⇒ orchestrator present? | ✅ **False** |
| `core/__init__.py` (37 B) ⇒ pulls in `orders`? | ✅ **False** |
| 🔬 **rehearsal** — `from orders import cnc_gtt_monitor` (a sibling), then assert orchestrator absent | ✅ **ASSERTION HOLDS** |

> ## ✅ **⇒ THE BLIND SPOT DOES NOT APPLY TO THE PACKAGE AS IT STANDS.**
> ⇒ ⭐ **COMMIT 1 STAYS A PURE MOVE** — ⛔ no `__init__.py` cleaning is needed, so
> **delta-zero is achievable**.

### 🔴 BUT THIS IS A **PRE-CHECK**, ⛔ NOT THE POST-CHECK

⚠️ **The rehearsal ran at `effff24` and imported an EXISTING module
(`orders.cnc_gtt_monitor`). ⛔ The module it must actually test DOES NOT EXIST YET.**
⭐ After COMMIT 1 there is a **new** contract module, and the orchestrator imports it —
⭐ a different import graph from the one rehearsed.

> ⇒ 🔴 **THE REHEARSAL IS EVIDENCE THE *PACKAGE* IS CLEAN. ⛔ IT IS NOT EVIDENCE THAT
> THE *POST-EXTRACTION IMPORT PATH* IS CLEAN.**
> ⇒ ⭐ **RE-RUN THE ASSERTION AFTER THE EXTRACTION, AGAINST THE ACTUAL NEW MODULE**,
> as part of COMMIT 1's own gate. ⛔ Do not carry the pre-check forward as the
> post-check.

⭐ Same shape as everything else binding here: **pre-verification ≠
post-verification**, exactly as ⛔ *boot ≠ the changed line executed*.

⚠️ ⛔ **Had it been otherwise**, the two legitimate options were: place the contract
**outside** the `orders` package, or clean the initialiser — ⭐ and cleaning it is
itself a change to shipped code needing its own differential, ⛔ **named in the commit
description**, ⛔ never smuggled in as part of "the move."
⛔ **And never** by deleting the `orders` entry from `sys.modules` — ⭐ that is the
prohibited import surgery.

---

### ⭐ CHECK 0b — **LOCATION IS A DURABILITY QUESTION, ⛔ NOT TASTE** ⇒ `core/`

⭐ Both locations work **today** — 🔬 `orders/__init__.py` is 0 B, `core/__init__.py`
is 37 B and clean. ⚠️ **They differ in what can break them LATER.**

| location | the plausible future regression |
|---|---|
| ⚠️ `orders/` | the contract sits in the **same package as the orchestrator**. 🔴 Someone later adding an ordinary convenience line to `orders/__init__.py` — e.g. `from .mis_autosquareoff import MisAutoSquareoff` — puts the orchestrator on **F's import path** and breaks the assertion. |
| ✅ **`core/`** | a different package from the orchestrator ⇒ ⭐ that same future edit **cannot reach F**. |

> ## ⭐ **DECISION: the contract module goes in `core/`.**
> ⛔ **Not** because `orders/` is unclean today — 🔬 it is clean — ⭐ but because
> `core/` **removes the most plausible future regression entirely**, rather than
> relying on the assertion to catch it each time.

⭐ The assertion still guards either choice; ⭐ this only decides **how often it is
likely to have to**. ⭐ The choice is recorded as **deliberate**, ⛔ not incidental.

---

### 🔴 CHECK 2b — **TWO BASELINES ARE IN PLAY**, and the fingerprint cannot tell them apart

```
52ccb4f  C-4 serial baseline ......... 10 failed · 5,896 passed · 4 skipped
effff24  the pushed candidate ........ 10 failed · 5,956 passed · 4 skipped
```

> ## 🔴 **COMMIT 1's BASELINE IS `effff24` — 5,956. ⛔ NOT 5,896.**

⚠️ If the older figure is picked up by mistake, *"delta zero"* becomes **meaningless**:
a **+60** discrepancy would read as the extraction adding tests ⇒ ⭐ the check meant to
catch scope creep would instead **manufacture a false finding**.

🔴 **AND THE FINGERPRINT CANNOT DISCRIMINATE.** ⭐ `46c38a3e…` hashes the sorted
**failure IDs**, and the standing ten are identical in both ⇒ ⚠️ **it is the same hash
for both baselines.**

> ⭐ **THE PASS COUNT IS THE DISCRIMINATOR — ⛔ never the fingerprint.**

⭐ Take **both** the count and the failure-ID list from the **stored `effff24`
artifact**, ⛔ never retyped from chat. ⚠️ If the artifact cannot be reproduced exactly
⇒ **NOT PROVEN**, ⛔ not reconstructed from memory.

---

### ⭐ THREE CLAIMS · THREE PIECES OF EVIDENCE · ⛔ NONE SUBSTITUTES FOR ANOTHER

| claim | its evidence |
|---|---|
| the **dependency architecture** is right | the **direction check** (+ the post-extraction `sys.modules` assertion) |
| the change is **population-neutral** | the `effff24` differential with **delta EXACTLY ZERO** |
| **compatibility** is preserved | the 59 shipped tests, green, via the **old import path** |

⚠️ 🔴 **THE 60-TEST GAP IS HISTORICAL BASELINE EVOLUTION**, present **BEFORE** COMMIT 1
(`52ccb4f` 5,896 → `effff24` 5,956, from the MIS orchestrator's own tests).
⛔ **It must never be charged to the extraction.** ⭐ That is precisely why `effff24`
is the comparand.

⭐ **TWO BASELINES, ⛔ NEVER CONFLATED — write BOTH explicitly in the record:**
rollback baseline **`52ccb4f`** · extraction differential baseline **`effff24`**.

---

### 🔴 CHECK 3b — THE CONTRACT MODULE MUST NOT OWN A SINGLETON

⭐ It holds the validated **class**, its config error type and the parsers — ⛔ **nothing
process-wide.**

⚠️ A module-level cached instance there would **MOVE** the shared-instance problem from
the orchestrator to the contract module, ⛔ **not solve it** — ⭐ and both F and the
orchestrator would then share it, ⛔ which is exactly the lifecycle coupling that is
forbidden.

> ⭐ **Same class ✅ · same config ✅ · same instance ⛔.**

⇒ ⭐ The instance-identity test still catches it — ⭐ but catching it *after* the
extraction is more expensive than **not building it in**.

---

### ⭐ ASSERTION MECHANICS · ⛔ BINDING

* ⭐ **NAME THE CANONICAL MODULE**, ⛔ not a package scan:
  `CANONICAL_ORCHESTRATOR_MODULE = <exact production path>`. ⚠️ If an alias path
  loads the same orchestrator code, ⛔ do not work around it — ⭐ **that is a coupling
  finding.**
* ⭐ **ASSERT AT FIRE TIME, ⛔ not before construction:**
  `config → construct → derive PRE_PASS → register/own trigger → FIRE → assert module
  absent → assert observable result.` ⚠️ A clean constructor with a forbidden
  **callback** lookup must be **RED**.
* 🔴 **"DID NOT CRASH" IS NOT "FIRED."** ⭐ The evidence needs an **observable
  self-test result**. ⚠️ If the trigger never fired ⇒ **NOT PROVEN / NOT EXERCISED**,
  ⛔ never PASS.
* 🔴 ⛔ **NO IMPORT SURGERY TO MANUFACTURE GREEN.** ⛔ Do not delete `sys.modules`
  entries; ⛔ do not reload modules. ⚠️ If the harness legitimately imports the
  orchestrator before F fires, ⭐ **the test has DISCOVERED a dependency and must
  report it.** ⛔ Hiding it manufactures the very clean-room condition the assertion
  exists to prove.
* ⭐ **IDENTITY, ⛔ NOT EQUALITY.** ⭐ Two independently built timing objects **should**
  compare equal; ⛔ they must not be the same object. ⚠️ A future "cleanup" replacing
  `is not` with `!=` would **silently void the guard**.
* ⭐ **TESTS A AND B ARE COMPLEMENTARY, ⛔ NOT DUPLICATES:** **A** proves F's *firing
  path* needs no orchestrator; **B** proves that **when both exist** they share no
  instance.

---

## 2a-iv — ⭐ SHARE THE CLASS · ⛔ NEVER THE INSTANCE · **ASSERTED, ⛔ NOT COMMENTED**

| | coupling | verdict |
|---|---|---|
| ⭐ same **CLASS** — a validated constructor | **config coupling**: same validation, same rules, same config source | ✅ **desirable** |
| 🔴 same **INSTANCE** | **data coupling**: one component's lifecycle becomes the other's precondition | ⛔ **FORBIDDEN** |

⭐ **MECHANICALLY ASSERTABLE:** where both exist, assert F's timing object
**`is not`** the orchestrator's. ⭐ **Object identity, ⛔ not equality** — they *should*
be equal in value and ⛔ must not be the same object.

⚠️ 🔴 **THE FAILURE THIS PREVENTS IS A PLAUSIBLE FUTURE REFACTOR:** *"both build the
same timing object — let's build it once and pass it in."* ⭐ That reads as good
hygiene and **silently reintroduces the silent-together failure.**
⇒ ⭐ **The assertion is what stops it. ⛔ A comment is not.**

⭐ **MUTATION:** hand F the orchestrator's instance ⇒ 🔴 the identity assertion goes
**RED**, ⭐ and the `sys.modules` assertion goes red too. ⇒ ⭐ **two independent
detectors for the same defect.**

---

## 2a-v — 🔴 CONSTRUCTED ≠ FIRED

⚠️ A defective implementation can **construct cleanly** and defer the forbidden
lookup to registration, or to the callback itself.

⇒ ⭐ **The test must exercise the whole path:**

```
config -> construction -> derive PRE_PASS -> register/own trigger -> FIRE -> observable result
```

⇒ ⚠️ If only construction is tested, the claim is *"F can be constructed without an
orchestrator"* — ⛔ **NOT** *"F is proven execution-independent."*

⭐ **DEPENDENCY GRAPH, desired:**
`CONFIG → F derives its own trigger` **and** `CONFIG → ORCHESTRATOR derives its own`.
🔴 **FORBIDDEN:** `CONFIG → ORCHESTRATOR derives/caches CHECK_1 → F consumes the
cache.` ⚠️ That is execution-independent only **cosmetically** — ⭐ the silent-together
failure survives.

⭐ **INDEPENDENCE IS NARROW, and the wording is fixed:** *"F is execution-independent
from the orchestrator's scheduler and orchestrator-owned timing state."*
⛔ **NEVER** *"F is independent of all failures."* ⚠️ Host, process, runtime, clock and
network are still shared — ⛔ a dead host, dead process, wrong clock or provider
outage takes F with it.

---

## 2b — 🔴 SILENCE IS NOT EVIDENCE · ⭐ A LIMITATION, ⛔ NOT A NEW CONTROL

⚠️ What should 👤 Rama conclude if nothing arrives at 15:05? ⛔ Currently ambiguous:
F could be dead · the schedule could be dead · or the message could simply be late.

> ## ⭐ **F CAN PROVE IT IS ALIVE. ⛔ IT CANNOT PROVE IT IS DEAD.**
> ⭐ The self-tests are **POSITIVE SIGNALS ONLY.**

🔴 **AN ABSENT MESSAGE MUST NEVER BE READ AS *"nothing went wrong."*** ⭐ It is
**uninformative** — ⚠️ and humans are poor at noticing an absence, which is exactly
why this is written down rather than assumed.

⭐ **RECORD AS A KNOWN LIMITATION, verbatim:**

> *"The boot and pre-pass self-tests are positive signals only. Their absence is
> ⛔ NOT evidence of health and ⛔ NOT evidence of failure — it is uninformative.
> Silence must never be interpreted as an all-clear."*

⛔ **DO NOT** add a watchdog, a dead-man's switch, a second channel, or a repeated
heartbeat to close this. ⭐ That is precisely the overengineering already ruled out.
⭐ The evidence copy at ~15:20–15:30 answers *"did it actually fire?"*
retrospectively, ⭐ and that is sufficient.

---

## 2c — ⭐ THE THREE-TIER CLAIM · ⛔ EXACT WORDING

| when | what it proves |
|---|---|
| `08:15` | path health **at boot** |
| `~15:05` | path health **near use** |
| `15:07` | **actual use / incident delivery** |

⚠️ ⛔ **The 15:05 test does NOT prove the transport is alive at 15:07.** ⭐ It reduces
the uncertainty window from **~7 hours to ~2 minutes**.
⭐ **Canonical:** *"near-use evidence that the path was healthy immediately before
PASS 1."*

⭐ **SELF-TEST FRESHNESS IS A TIMESTAMP, ⛔ NOT A LATCH:**
`SELF_TEST_AT` · `SELF_TEST_RESULT` · `SELF_TEST_BOOT_ID` ·
`SELF_TEST_KIND` (BOOT / PRE_PASS).
⛔ **Never a long-lived `notification_healthy = TRUE`** — ⚠️ a stale 08:15 PASS must
not read as protection at 15:07.

---

## 2d — 🔴 TRANSPORT STATES · CORRELATION · NON-BLOCKING

⭐ **STATES:** `ATTEMPTED · ACCEPTED_BY_PROVIDER · REJECTED · TIMEOUT · EXCEPTION ·
UNKNOWN`. ⛔ **Never invent `DELIVERED_TO_HUMAN` from an API result.**

⭐ Email and telegram results stay **independent**; the aggregate is
`BOTH_ACCEPTED · PARTIAL · BOTH_FAILED · UNKNOWN`.
🔴 ⛔ **PARTIAL IS NOT SUCCESS**, and one channel's failure must not erase the
other's evidence.

⭐ **CORRELATION IDENTITY** — each incident carries an event/correlation id so
`orchestrator event → F attempt → email result → telegram result` **provably**
belong to the same incident. ⛔ **Log adjacency is not identity.** ⭐ Reuse an
existing event id if one exists; ⛔ do not build a parallel identity system.

🔴 **NOTIFICATION MUST NEVER BLOCK THE TRADING PATH.** ⭐ Slow SMTP · telegram
timeout · provider retry · network stall ⇒ ⛔ must not hold the orchestrator beyond
its execution budget. ⭐ Bounded failure behaviour; ⭐ the CRITICAL is preserved
regardless of notification outcome.

⚠️ ⭐ This compounds with PASS 2's **≈2 s** measured-bound execution: a blocking
notification could by itself push the pass past the 15:12 cutoff.

---

## 3 — 🔴 CASE G · THE WORST CASE, AND IT WAS MISSING

⭐ CASE C covers *"CRITICAL occurs, notification fails."* 🔴 **The more dangerous
case:**

> ## **CASE G — a CRITICAL occurs · the transport reports SUCCESS · 👤 Rama never sees it.**
> Telegram delivered to a **muted chat** · email filed as **spam** · the app not
> opened. ⇒ ⭐ **Every layer reports green and the incident is still invisible.**

⭐ **`transport result ≠ human receipt`.** ⇒ 🔴 **The only recipient-side
acknowledgement available is 👤 Rama himself.**

> ### ⇒ **MONDAY'S F EVIDENCE MUST INCLUDE 👤 RAMA CONFIRMING HE RECEIVED AT LEAST ONE MESSAGE** — the 08:15 self-test or the 15:05 one. ⭐ One line from him.
>
> ⭐ Explicit acceptance item: **`F_RECIPIENT_CONFIRMED = YES / NO`.**
> ⛔ Not inferred. ⛔ Not assumed from a green API result.

🔴 **AND `F_RECIPIENT_CONFIRMED` MUST NEVER GATE ALERTING.** ⛔ `if not confirmed:
suppress` is a **circular dependency** and is forbidden. ⭐ It is an
**acceptance/evidence field**, ⛔ nothing else. ⭐ `YES` means only: 👤 Rama confirmed
receipt of **that specific test message** — ⛔ not that every future message will be
seen.

### ⭐ CASE H — DISTINCT FROM CASE G, ⛔ DO NOT COLLAPSE THEM

| | |
|---|---|
| **G** | transport reports SUCCESS, 👤 Rama never sees it ⇒ **recipient-side visibility failure** |
| **H** | healthy at 15:05, **fails by 15:07** ⇒ **time-of-use transport failure** |

⭐ In **H** the orchestrator may still PASS; ⭐ F incident delivery FAILS; ⭐ the 15:05
evidence remains valid **for 15:05** and ⛔ **must never be retroactively relabelled
as proof of 15:07 health.**

### ⭐ FOUR TERMS, ⛔ NEVER INTERCHANGEABLE

**PASS** (expected observable state, with provenance) · **FAIL** (expected state did
not occur) · **NOT PROVEN** (insufficient evidence) · **NOT EXERCISED** (the path did
not naturally occur).

⚠️ Without it, F's coverage claim rests entirely on transport API results — ⭐ which
is **exactly the false-belief-of-coverage failure F exists to prevent**.

---

## 4 — 🔴 ARCHITECTURAL INVARIANTS · ⛔ NON-NEGOTIABLE

1. **THE SELF-TEST MUST NEVER GATE A CRITICAL.**
   ⭐ `orchestrator CRITICAL → F path` **and** `→ telemetry/log`, **in parallel**.
   ⛔ A failed self-test must never convert future CRITICALs into *"no alert
   because self-test failed."* ⭐ If the path is down, the CRITICAL is **still
   recorded**.
2. **F FAILURE MUST NEVER HIDE THE ORCHESTRATOR FAILURE.**
   ⛔ F must not delete, swallow, replace or downgrade the underlying CRITICAL
   state. ⭐ **The notification layer is an observability mechanism, ⛔ not the
   source of truth.**
3. **RECORD ATTEMPT AND RESULT SEPARATELY, ⛔ never collapsed into "sent = yes":**
   `F invoked` → `email attempt/result` → `telegram attempt/result` → `final
   self-test state`. ⭐ Distinguish **attempted · API accepted · API rejected ·
   timeout/exception**. ⇒ ⭐ a broken transport **cannot appear green**.
4. **ONE SELF-TEST PER ACTUAL BOOT**, carrying an observable boot/run identifier
   ⇒ ⭐ a legitimate restart is distinguishable from a duplicate-notification bug.
   ⛔ Do not suppress a legitimate restart's self-test to reduce message count.

---

## 5 — ACCEPTANCE · ⛔ CODE EXISTING IS NOT ACCEPTANCE

⭐ **TWO TEST CLASSES, ⛔ never one:**

**(A) PATH HEALTH** — boot self-test · the 15:05 self-test · a normal
(non-critical) event produces **no** false critical · transport result recorded ·
failure handling.

**(B) INCIDENT DELIVERY** — **each of the four CRITICAL branches independently
RED-capable**: `DEADLINE_BREACH` · `MIS_REMAINS` · `CANCEL_FAILED` ·
`BROKER_STATE_UNAVAILABLE`.

> 🔴 ⛔ **A GREEN SELF-TEST IS NOT PROOF THE FOUR BRANCHES ARE WIRED.** ⭐ Class A
> passing says nothing about class B.

⭐ **CONTENT:** the message names the **exact condition** and carries enough context
to act. ⭐ **DELIVERY:** the send attempt **and its result** are observable.
🔴 **FAILURE:** a transport failure is **itself recorded** and ⛔ can never be
mistaken for successful alerting.

### ⭐ THE TEN IMPLEMENTATION QUESTIONS — build-evidence, ⛔ not questions for 👤 Rama

what counts as *email delivered* · what counts as *telegram delivered* · API
acceptance recorded **separately** from receipt · email OK + telegram fail ·
telegram OK + email fail · both fail · **is the CRITICAL still recorded when
delivery fails** · exactly once per boot · unmistakably INFO · does the self-test
result survive log rotation.

---

## 6 — ⚠️ THE WEEKEND STACK BOOTS TWO UNTESTED UNITS AT ONCE

⭐ F and F2-CORE both push Sunday night and both boot Monday 08:15.
⇒ 🔴 **If that boot fails, ⛔ nothing isolates which one caused it** — ⭐ the same
lesson as 24-Aug, where twenty commits ran together and a failure would have
isolated none.

⭐ **MITIGATION, costs nothing:** keep **F and F2-CORE as SEPARATE COMMITS** even
though they ship in one push ⇒ ⭐ a failed boot can be **bisected**, ⛔ not reverted
wholesale.

⭐ **RECOVERY ALREADY EXISTS:** the rollback TREE stays **`52ccb4f`** — a known-good,
proven-to-boot tree. ⛔ **Do not advance it on Sunday's push.**

### ⚠️ HONEST SIZING — ⭐ F ALONE IS LIKELY THE WEEKEND

🔬 **F's acceptance is now ~22 items:** two self-tests · four CRITICAL branches
**independently** RED-capable · a six-state transport vocabulary × two independent
channels · aggregate semantics with `PARTIAL ≠ SUCCESS` · correlation identity
end-to-end · a non-blocking bound that is **tested, ⛔ not asserted** · the
no-orchestrator independence test · the coupling review · evidence preservation.

🔬 **F2-CORE is 7 collision files carrying 19 main commits (+957/−100) plus a new
420-line file, with seven behavioural criteria each RED-capable.**

⇒ ⚠️ ⭐ **Either one is comparable in size to the MIS orchestrator, which consumed
most of Friday at this standard.**

⇒ ⭐ **REALISTIC: F = Saturday. F2-CORE = Sunday only if F is clean — and it may not
finish.** ⛔ That is not a failure; ⭐ F2-CORE has no Monday deadline and ⛔ must not be
rushed into one.

> 🔴 ⛔ **DO NOT COMPRESS F's ACCEPTANCE TO MAKE ROOM FOR F2-CORE.**
> ⭐ **A partially accepted F is worse than no F** — ⚠️ it produces exactly the
> **false belief of coverage** that F exists to prevent.

⭐ **IF SUNDAY IS SHORT: push F alone.** ⭐ A single-component push is **easier** to
attribute on Monday, ⛔ not harder — ⇒ ⭐ the bisect problem disappears entirely.

> ## 🔴 **PRIORITY INVERSION, AND IT IS DELIBERATE: IF THE WEEKEND RUNS SHORT, F SHIPS AND F2-CORE WAITS.**
> ⭐ F is what makes Monday 15:07 observable. ⭐ **F has a Monday deadline; F2-CORE
> does not.**

---

## 7 — MONDAY · THE EVIDENCE **CHAIN**, ⛔ NOT A CHECKLIST

```
AUTHORISED SHA → VM SHA → boot/config validation → F boot self-test
→ 15:05 F pre-pass self-test → PASS 1 invocation → candidate census
→ cancel/verify/exit activity → CRITICAL telemetry if any
→ F notification attempt/result → PASS 2 outcome
→ final MIS/CNC reconciliation → ledger/effect evidence
→ F_RECIPIENT_CONFIRMED
```

⭐ **The question is whether the evidence establishes the CAUSAL SEQUENCE** — ⛔ not
whether each line individually looks fine.

### DECISION CASES

| | condition | verdict |
|---|---|---|
| **A** | boot ✅ · self-test ✅ · candidate exists · passes behave | ⭐ candidate-bearing evidence **established** |
| **B** | self-test ✗ | ⛔ notification coverage **NOT PROVEN**, regardless of orchestrator behaviour |
| **C** | CRITICAL occurs, notification fails | ⭐ orchestrator may still be proven; **F path FAIL** — ⛔ do not collapse them |
| **D** | no MIS candidate at 15:07 | ⭐ scheduled execution **PROVEN**; ⛔ candidate-bearing effect **NOT EXERCISED** |
| **E** | boot ✗ | ⭐ stop at the boot tier; ⛔ **no inference** about 15:07 |
| **F** | runtime/path failure | 🔴 **STOP → NO-GO → RE-MEASURE → RE-AUTHORISE** |
| **G** | everything green, 👤 Rama saw nothing | 🔴 ⛔ **coverage NOT PROVEN** (§3) |

🔴 ⛔ **A flat book at 15:07 proves only the trivial arm. ⛔ MANUFACTURE NOTHING.**

### ⭐ EVIDENCE COPY BOUNDARY (~15:20–15:30)

Preserve: run/date id · exact candidate SHA · pass ids · timestamps · scan counts ·
cancel requests **and results** · verifications · exit submissions **with order
ids** · state transitions · CRITICAL states · F notification events and results ·
final MIS/CNC state.

⭐ **ALSO COPY:** boot self-test result · pre-pass self-test result · boot/run
identifier · `F_RECIPIENT_CONFIRMED`. ⭐ **Copy, hash, preserve** — ⛔ never edit,
filter or rewrite. ⭐ The original runtime record remains the source.

⭐ **MONDAY BOOT EVIDENCE RECORDS BOTH IDENTITIES:** the combined SHA = **release**
identity · F and F2-CORE component SHAs = **attribution** identity. ⇒ ⛔ *"the
combined tree booted"* must not hide **which component was exercised**.

⭐ **Preservation, ⛔ not a second chance to interpret.** ⚠️ Guards the two cheap
failure modes: log rotation before anyone reads, and a mid-pass crash truncating
the record.

---

## 7a — ⛔ DO NOT OVERSTATE F · what it does and does not provide

✅ **F PROVIDES:** notification **attempts** with observable provider results ·
boot and near-use self-tests · the CRITICAL preserved **independently** of delivery.

⛔ **F CANNOT GUARANTEE:** human attention · human receipt inferred from provider
acceptance · continuous transport health **between** tests · anything if the host is
dead · intervention inside PASS 2's **~2 s** window.

---

## 8 — TIMESTAMP CANON (carried forward)

`position_flat_observed_ts = 15:10:53.332`, source **`get_positions` call_end** ·
`accounting_lag` = **detection-to-ledger** · broker exit fill timestamp
🔴 **UNAVAILABLE** · ⛔ never describe the 15.1 s interval as a fill bound ·
⭐ if a broker fill time ever becomes available, create **`fill_to_ledger_lag`** —
⛔ never substitute it into `accounting_lag`.

⭐ **Ordering proof and latency measurement stay SEPARATE audit dimensions.**
`reset_crossing = TRUE` holds **without** an exact fill time. ⭐ Reuse that pattern.

⛔ push ≠ boot · ⛔ boot ≠ the changed path executed · ⛔ transport success ≠ human
receipt · ⛔ healthy at boot ≠ healthy at 15:07 · ⛔ a green self-test ≠ the four
CRITICAL branches wired · ⛔ detection ≠ fill · ⛔ adjacency ≠ identity ·
🔴 ⛔ **an alerting unit that has never fired in production is not coverage.**

## END
