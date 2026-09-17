# D-A DESIGN REPORT — pipeline-scoped stop

**Read-only pass, 31-Aug-2026 ~20:0x IST. Deployed SHA `39292d3`**
(`deployed tree == HEAD, no tracked drift` — the system's own 18:45 check).
⛔ NO CODE WRITTEN. ⛔ F2-CORE worktree untouched. **REPORT → STOP → await Rama.**

---

## 🔴 HEADLINE: THE PREMISE IS HALF TRUE, AND THE UNIT IS SMALLER THAN SCOPED

D-A was scoped as: *"a daily-loss breach in either book fires
`EodSquareoff.fire_now()` and a global `soft_kill`… one book's loss stops both
books."*

Measured at the deployed SHA:

| surface | scoped by book today? | evidence |
|---|---|---|
| **POSITIONS** (what gets closed) | ✅ **ALREADY SCOPED** | `EMERGENCY_FLATTEN_PRODUCTS = frozenset({"MIS","CO"})` — **CNC excluded** |
| **AUTHORISATION** (what gets blocked) | ⛔ **NOT SCOPED** | `kill_switch_state` = one row, `CHECK (id = 1)`, no scope column |

⇒ **A daily-loss breach does NOT close the delivery book's positions.** It blocks
the delivery book's *entries*. **D-A is an authorisation problem, not an
enforcement problem.**

---

## Q1 — CAN THE KILL BE SCOPED BY PIPELINE TODAY? **NO — and the register's premise is wrong**

```python
def is_active(self, intent: str = "entry") -> bool:
    intent="entry" -> True for SOFT_KILL or HARD_KILL
    intent="exit"  -> True only for HARD_KILL (soft_kill allows exits)
    intent="any"   -> True for SOFT_KILL or HARD_KILL
```

🔴 **`intent` is an ACTION KIND — `entry` / `exit` / `any`. Three values, none a book.**

The register's *"four intents exist"* refers to a **different vocabulary**:
`PRODUCT_TO_INTENT = {MIS→INTRADAY, CO→COVER_ORDER, CNC→DELIVERY, NRML→DELIVERY}`.
**`KillSwitch` never takes that argument.** The two were conflated.

⇒ `intent` is not a 1:1 proxy for pipeline — **it is not the same axis at all.**
There is **zero** pipeline dimension at the check point.

**At the creation point, likewise zero:**

```sql
CREATE TABLE kill_switch_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),   -- single row, HARD-CONSTRAINED
    state TEXT CHECK (state IN ('INACTIVE','SOFT_KILL','HARD_KILL')),
    reason TEXT, triggered_at TEXT, triggered_by TEXT
);
```

⇒ **Q1 answer: NO. This is a STATE-MODEL change, not a scoping change** — and
`CHECK (id = 1)` means even per-book rows require a migration.

---

## Q2 — WHAT STATE DOES THE KILL WRITE AND READ? (data-flow, not class names)

```
TRIGGER      circuit breaker 15:15 / daily-loss / operator / recovery
   ↓
WRITE        KillSwitch._persist_state(state, reason, ts, by)
   ↓
STORED       kill_switch_state — ONE ROW (id=1), PERSISTENT (survives restart)
             + in-process mirror  self._state : KillState   (process-local)
   ↓
READ         is_active(intent)  → filters on ACTION KIND only
             current_state() / status()
   ↓
CONSEQUENCE  entry admission blocked; exits allowed under SOFT_KILL;
             HARD_KILL additionally drives the emergency flatten
   ↓
CLEAR        clear_stale_state(today)        — prior-day kills only
             auto_clear_scheduled_kill()     — the scheduled 15:15 branch
             resume()                        — operator
```

🔴 **The dimension that matters:** the persisted state has **no** book/scope key.
⇒ **Adding a `pipeline` ARGUMENT to `is_active()` isolates NOTHING** while the
row is shared. Any fix must change the **stored** representation.
Both a persistent row **and** a process-local mirror must move together.

---

## Q3 — CAN `fire_now()` BE SCOPED? **It effectively already is**

```
fire_now(reason, triggered_by) -> EodFireResult     ⛔ no scope argument
  ↓ _fire(now, recovery_fire=False)            [:326]
  ↓ _exit_open_positions(...)                  [:430 → :1027]
    :1086  if int(p.qty) != 0 and p.product in EMERGENCY_FLATTEN_PRODUCTS
    :1460  and getattr(p,"product","") in EMERGENCY_FLATTEN_PRODUCTS
```

`EMERGENCY_FLATTEN_PRODUCTS = frozenset({"MIS","CO"})` — **CNC excluded.**

**Production callers of `fire_now`: exactly ONE** — `main.py:797`
(*"cancels pending entries + market-closes all positions"* — the comment
overstates; the filter narrows it to MIS/CO).

**Is "all" intentional at that call site?** The constants file answers directly:

> *"the ONLY products an emergency (HARD_KILL) flatten may sell. **Delivery (CNC)
> SURVIVES the kill** — the Q4 invariant is 'no live INTRADAY position', NOT 'no
> live broker position' (Rama, 30-Jul)."*

⇒ **Delivery surviving is a DELIBERATE, Rama-authored invariant already in force.**

**Single source, five call sites, explicitly enumerated in-code:**
`kill_switch.py:1585` (emergency local) · `kill_switch.py:1683` (emergency broker
sweep) · `eod_squareoff.py:1085` (scheduled EOD6) · `eod_squareoff.py:1453`
(scheduled residual) · `order_reconciler.py:2174` (CHECK2 orphan).
⚠️ **Changing that set changes all five.**

---

## Q4 — DO THE KILL PATHS SHARE ONE LIFECYCLE? **YES — structurally, unavoidably**

All writers write the **same single row**. Therefore:

- Every trigger path writes one shared state.
- 🔴 **Every clear path clears it for everything.** `clear_stale_state()` and
  `auto_clear_scheduled_kill()` both set `INACTIVE` on the one row.
- ⇒ **FILE 86 §4's warning is confirmed by the schema, not merely suspected:
  a scoped SET with a global CLEAR is still a global kill.**

⇒ **Combining D-A with the SOFT_KILL scheduled-vs-emergency defect is JUSTIFIED**
— they are the same row. Fixing one without the other leaves the defect reachable
through the other door.

⚠️ **NOT established in this pass:** the precise per-path trigger inventory
(which callers invoke which write). Needs enumeration during build.

---

## Q5 — THE INVARIANT

> *"A daily-loss breach in book A may change A's kill/stop state and A's
> permitted actions, but must not change B's kill/stop state, B's permitted
> actions, B's position state, or B's ability to continue operating — and the
> same with A and B reversed."*

Evaluated at **observable boundaries**, never by inspecting internal variables.

📌 **Today's evidence already partially satisfies the position clause**: CNC
survives an emergency flatten by construction. The clauses at risk are **kill
state** and **permitted actions**.

---

## Q6 — THE THREE TESTS (they are three obligations, not one)

**TEST A — reproduce the OLD failure. BOTH books PRESENT, current code.**
Breach A → assert **B is wrongly affected** (entry admission blocked). Reverse it;
**record symmetry, do not assume it**.
🔴 **Must go RED on current code.** If the old failure cannot be reproduced from a
clean baseline, **criterion 7 is OPEN / UNPROVEN** and the original finding's
provenance gets investigated. ⛔ **Do not construct a red test to satisfy the
acceptance wording.** Same test is the after-guard: red before, green after.
**Define "affected" BEFORE running**: B's kill state · B's permitted actions ·
B's position state · B's ability to keep operating. Mutating **any one** is a
reproduction.

**TEST B — construction independence. Opposing machinery ABSENT (not disabled).**
Fail the test if the code **constructs, registers or resolves** B at all. Assert:
no B object, no B registration/listener, no shared global registration that
silently creates B, no requirement that B state exist, and A's stop completes.
Reverse.

**TEST C — non-mutation snapshot**, narrow to the invariant's named surfaces.
If some of B's state cannot be observed without invasive machinery, **state that
as a limitation** — ⛔ do not substitute a proxy.

---

## 🔴 THE TWO OPTIONS, PRICED ON BOTH SURFACES

**Because enforcement is already scoped, both options are AUTHORISATION-only.**

### (a) Add a pipeline dimension to the kill state — the big change
- Schema migration: drop/replace `CHECK (id = 1)`, one row per scope.
- Every writer, reader, clear path and the in-process mirror updated.
- Migration of existing rows.
- **Cost: a project.** Touches schema on the capital/kill path.

### (c) A `scope` field on the existing state — likely sufficient
- Add `scope` to the row (`ALL` | `INTRADAY` | `DELIVERY`); `is_active()` matches on it.
- No row-count change, so `CHECK (id = 1)` may still need relaxing **only if two
  scoped kills must coexist** — that is the design question to settle first.
- **Cost: a session, plausibly.**

### ⚠️ THE DEFAULT IS NOT SAFE ON BOTH SURFACES

| surface | default `ALL` |
|---|---|
| **ENFORCEMENT** (`fire_now`) | ✅ **safe** — existing EOD callers keep working |
| **AUTHORISATION** (kill state) | 🔴 **DANGEROUS** — a scoped kill stored/migrated/defaulted as `ALL` **silently broadens into a global kill**, worse than the defect being fixed, and invisible until a live breach |

⇒ **Produce a state-transition table before choosing**, both books:
`trigger | requested scope | stored scope | reader scope | action scope`
and answer explicitly: **is defaulting any existing/legacy row to `ALL` safe?**
If a migration or default can turn a scoped kill global, (c) needs a different
default on the authorisation surface.

**Choose on SEMANTICS, then smallest CORRECT change, then cost.**
⛔ A cheap `scope` parameter must never be camouflage for an ambiguous state model.

---

## PROOF CHAIN (acceptance is not `exit 0`, and not "22 tests passed")

```
BASELINE  (fresh SHA + gate result recorded immediately before the change)
   → TEST A  RED     old cross-pipeline failure reproduced, both books present
CHANGE
   → TEST A  GREEN   same test, same interfaces
   → TEST B  PASS    target stop works with opposing machinery ABSENT
   → TEST C  PASS    opposing observable state/action/position unmutated
   → REGRESSION      relevant existing tests green
   → GATE/MUTATION   acceptable
   → clean diff · clean worktree · separate commits
```

The existing 22 tests / 11 mutations at `587b306` are **provenance, not
acceptance**, and ⛔ **the gate does not survive a SHA change — re-gate on resume.**
Symmetry recorded per direction, never invented for tidiness.
⛔ KOPRAN and Smart TGT stay out of the design, baseline, acceptance and commits.

---

## WHAT THIS PASS DID **NOT** ESTABLISH

- The per-path trigger inventory (which callers invoke which kill write).
- Whether two scoped kills must ever coexist — decides whether `CHECK (id = 1)`
  must be relaxed under option (c).
- Whether `main.py:797`'s *"market-closes all positions"* comment is merely stale
  or reflects an intent that conflicts with the CNC-survives invariant.
- 🔴 **The 15:20 observation, carried in as evidence with its question attached:**
  `delete_gtt` executed **LIVE at 15:20:36 under a SOFT_KILL active since
  15:15:01**. So SOFT_KILL does not prevent that enforcement path from reaching a
  live broker mutation. **Is that intended?** Cleanup surviving a kill may be
  correct, or a kill leaving broker-mutating paths live may be wrong.
  ⛔ **The observation cannot choose.** It must be answered before the
  authorisation model is finalised, because it is a *second* enforcement surface
  that today's scoping analysis has not covered.

---

## RECOMMENDATION

**Option (c), authorisation-only, combined with the SOFT_KILL
scheduled-vs-emergency defect** (same row, so they cannot be separated) —
**subject to the state-transition table settling the default question first.**

⛔ **NO CODE UNTIL RAMA APPROVES THIS DESIGN.**
