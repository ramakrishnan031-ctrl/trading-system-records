# THE ARMED REVERT TRIGGER — END-TO-END TRACE + A/B/C/D/E CLASSIFICATION

**27-Aug-2026 (Thu), ~10:0x IST.** Executes FILE 13 §2's mandated map, which
`SECTION_E_AND_F2_INVENTORY_27-Aug-2026.md` §6 recorded as **NOT DONE**.
🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S.

⛔ **READ-ONLY.** No code changed, no config touched, no service acted on, no push.
⛔ **The trigger is NOT re-armed, NOT disarmed, NOT reworded, NOT tuned by this
document.** It classifies; ⛔ it does not adjudicate. 👤 The ruling is Rama's.

🔬 **Deployed SHA resolved BY MEASUREMENT at trace time: `origin/main` =
`bc9a9f5`.** Every line number below was re-verified at that SHA (M3) — ⛔ not
carried from a card. ⚠️ The ROOT working tree sits on `feat/delivery-config-split`,
where these numbers do **NOT** hold; every read was `git show origin/main:…`.

---

## 0 — THE TRIGGER, VERBATIM (👤 Rama, 25-Aug 09:45 rewording)

> ▎ **`carry > 0` IS NOW AN EXPLICIT PRECONDITION.** IF `carry > 0` **AND** the
> CHECK 1 residual ≈ the carried CNC amount ⇒ 🔴 **REVERT** (👤 on Rama's word).
> IF `carry = 0` and the residual merely RESEMBLES a position value ⇒ ⛔ **NOT a
> carry failure — it is same-day broker-`used` settlement lag.**

📄 Target already resolved by `EOD_CARRY_SEQUENCE` §PHASE 0 via the 55/46
sample-count fingerprint: the trigger's wording says *"CHECK 1"*, but the quantity
it actually names is **G3 CHECK 2's `margin_residual`**. ⭐ This trace **inherits**
that resolution, ⛔ does not re-litigate it, and re-verified its anchors.

---

## 1 — THE MAP (the seven hops FILE 13 §2 demanded)

### Hop 1 · TRIGGER → OWNING FUNCTION
🔬 `_g3_capital_drift` — **`orders/order_reconciler.py:3569`** @ `bc9a9f5`.
Its docstring `:3572-3576` declares **two checks, deliberately NOT merged**:
`CHECK 1 (drift) expected_broker_net vs margins.net` · `CHECK 2 (margin)
system_held_capital vs margins.used`. **The residual is CHECK 2's.**

### Hop 2 · CALLERS
🔬 **Exactly ONE call site: `:1013`**, inside `_reconcile()`. ⛔ No other caller
anywhere in the tree. The function is reached once per reconciler cycle.

### Hop 3 · INPUT FIELDS — every operand, with its unit

| operand | expression | line | origin | **unit** |
|---|---|---|---|---|
| `held` | `intraday_reserved + intraday_used + positional_reserved + positional_used` | `:3684-3687` | **LOCAL** FundManager snapshot | **₹** |
| `carry` | `snapshot.intraday_carry + snapshot.positional_carry` | `:3701` | **LOCAL**, set at rehydrate | **₹** |
| `held_today` | `held − carry` | `:3701` | derived | **₹** |
| `margins.used` | broker utilised margin | `:3702` | **BROKER** | **₹** |
| **`margin_residual`** | **`held_today − margins.used`** | **`:3702`** | derived | **₹** |

### Hop 4 · UNIT AND SEMANTIC MEANING
🔴 **FILE 13's CENTRAL FEAR IS REFUTED BY MEASUREMENT.** The concern was that the
trigger's code path might read `quantity_delta_shares` or a wrong rupee quantity
and so compare incompatible units.
🔬 **It does not.** All five operands above are **RUPEES**. The shares quantity at
`:2566` belongs to **`_check5_position_grew` (`:2539`)** — a different function
that G3 never calls and that never touches `margin_residual`.
⇒ ✅ **No unit mismatch exists inside the trigger's own path.**

⚠️ 🔴 **BUT A REAL UNIT COLLISION EXISTS ONE LAYER OUT, AND IT IS LIVE.** The
**same event class** `CapitalDriftDetected` carries a field named `delta` that is:
- 🔬 **RUPEES** from G3 CHECK 1 — `:3695` `delta = abs(actual - expected)`
- 🔬 **SHARES** from CHECK 5 — `:2566` `delta=float(broker_qty - local_qty)`

📄 `capital/drift_handler.py:18-24` names this hazard in its own docstring:
*"their delta semantics differ (CHECK5 emits integer share qty, not rupees — a
percentage/absolute-rupee escalation would misfire catastrophically)."*
⇒ ⭐ **The collision is REAL and DOCUMENTED, but it does NOT reach the revert
trigger**, because the trigger reads a **log field**, ⛔ not the event. 🏷️ Recorded;
⛔ not chased here.

**Semantic meaning of `margin_residual`, stated plainly:**
> *"What the system believes it has blocked TODAY (excluding what carried in),
> minus what the broker says is utilised."*

⇒ It is a **two-ledger difference**. ⛔ Nothing in its computation observes capital
being released, lost, or returned. It measures **disagreement**, ⛔ not loss.

### Hop 5 · DOWNSTREAM ACTION — 🔴 THERE IS NONE
🔬 **All SIX occurrences of `margin_residual` in the deployed tree:**

| line | use |
|---|---|
| `:3702` | assignment |
| `:3714` | `self._log.debug` argument — every cycle |
| `:3781` / `:3786` | CHECK 1's `log.error` format + argument |
| `:3816` | Telegram body f-string |
| `:3832` | Telegram `context` dict |

🔬 **ZERO conditionals. ZERO comparisons. `margin_residual` never appears in an
`if`, a `while`, or any comparison operator anywhere in the codebase.**
⇒ 🔴 **IT GATES NOTHING. It is a pure reported value.**

📄 And the code says so itself, `:3703-3708`, verbatim:
> *"Measured every cycle (forensics) and carried in CHECK 1's alert context below.
> **No alert of its own yet**, and the reason is a measurement gap rather than
> convenience: broker `used` for a SETTLED CNC holding is unmeasured … so alerting
> here would **fire falsely on the first carry day**. Owed: measure a T+1 carry,
> then decide a threshold."*

⇒ ⭐ **CHECK 2 HAS NO THRESHOLD AND NO ALERT — BY DESIGN, AND THE DESIGN SAYS WHY.**

**What G3 *does* do — and it is driven by CHECK 1's `delta`, ⛔ never the residual:**
1. `:3757` `if delta <= effective_tolerance: return None` — **CHECK 1's quantity.**
2. `:3792` `CapitalDriftDetected(source_module="order_reconciler", …)`
3. `:3801` Telegram `severity="CRITICAL"` (the residual rides along as context)
4. `:3856` `ReconciliationAction(check_name="CAPITAL_DRIFT", tier="UNRECOVERABLE")`

🔬 **Escalation is structurally impossible from this source.**
`capital/drift_handler.py:66-70` — `_ESCALATING_SOURCES = frozenset({"fund_manager",
"fund_manager_self_check", "fund_manager_bucket_overflow"})`.
⇒ **`order_reconciler` is NOT in it.** `:147` `is_escalating = event.source_module
in _ESCALATING_SOURCES` ⇒ **False**. DH1 logs at INFO and ignores it.
⇒ ✅ **G3 — CHECK 1 or CHECK 2 — CANNOT ARM THE KILL SWITCH IN EITHER DIRECTION.**

🔬 **`tier="UNRECOVERABLE"` is a LABEL, ⛔ not a gate.** A whole-tree grep for a
branch on `tier == "UNRECOVERABLE"` returns **nothing outside tests**. Its own
`action_taken` string reads *"manual intervention required"*.

### Hop 6 · REVERSAL / STOP CONSEQUENCE
🔬 The unit the trigger would revert is **`7fc5d5a`** (20-Aug-2026) —
*"fix(capital): G3 compared real capital against broker cash — compare expected
net"* — **3 files, +547/−65** (`broker/zerodha_adapter.py`,
`orders/order_reconciler.py`, its tests).
🔬 **`7fc5d5a` IS DEPLOYED** (verified ancestor of `bc9a9f5`).

⇒ 🔴 **The consequence is a HUMAN revert of deployed capital-path code**, ⛔ not any
automated action. 📄 The standing fail-safe **C-3** already governs it:
> *"⛔ NO AUTOMATIC REVERT · ⛔ NO TUNING · ⛔ NO TRIGGER REDESIGN while the cause
> cannot be distinguished. A revert of deployed code is an IRREVERSIBLE TRADING
> ACTION… 👤 Escalation — ⛔ not adjudication — is the correct terminal action."*

### Hop 7 · 🔴 THE OBSERVABILITY FINDING — AND A CORRECTION TO MY OWN FIRST READ
⚠️ **I first measured `MARGIN_RECON` = 0 in `logs/system_2026-08-27.log` and was
about to report the check as unobservable. THAT WAS MY GREP, ⛔ NOT THE SYSTEM.**
🔬 Corrected: the DEBUG line is routed to **`logs/reconciler_YYYY-MM-DD.log`** and
`logs/debug_YYYY-MM-DD.log`, ⛔ not the system log. Today's holds **438+ samples**.
⭐ Recorded because the near-miss is the lesson: **a zero is only evidence once the
surface is proven to be the right one.**
⇒ ✅ **The residual IS observable in production, every cycle.** But ⚠️ it is
**DEBUG-level and in a non-default file** — so on a carry day nobody sees it unless
they know to grep `reconciler_*.log`. 🏷️ Recorded.

---

## 2 — 🔴 THE MEASUREMENT THAT SETTLES THE TRIGGER'S STATUS

🔬 **Across EVERY reconciler log since the check was born:**

| measure | value |
|---|---|
| first log containing `MARGIN_RECON` | **`reconciler_2026-08-21.log`** — the first trading day after `7fc5d5a` deployed 20-Aug |
| total `MARGIN_RECON` samples | **9,289** |
| samples with **`carry != 0`** | 🔴 **ZERO** |

⇒ 🔴 **THE TRIGGER'S MANDATORY PRECONDITION (`carry > 0`) HAS NEVER ONCE BEEN
SATISFIED IN THE ENTIRE LIFETIME OF THE CODE IT GUARDS.**
⇒ ⭐ **The trigger has never been evaluable — not on 24-Aug, not on 25-Aug, not on
any of 9,289 samples.** ⛔ This is **NOT** a pass and ⛔ **NOT** a failure; it is
*never exercised*.

🔬 **`carry` HAS been non-zero exactly once in production — and it was BEFORE the
check existed.** `fund_manager.rehydrate_carry` fired **19-Aug-2026 08:15:38.484**,
`positional_carry = 294.6`, `total_after = 10917.30`. 🔬 `debug_2026-08-19.log`
contains **no `MARGIN_RECON` at all** — `7fc5d5a` landed the next day.
⇒ ⭐ **The one day the precondition was met, the quantity did not yet exist.**

🔬 **Today, 27-Aug (for completeness):** `carry=0.00` on all 438+ samples; the book
was flat at 09:15 and **4 trades had entered by 10:05**, e.g.
`held=104.73 carry=0.00 held_today=104.73 broker_used=99.74 residual=4.99` —
ordinary small broker-lag residuals. ⛔ Trigger not met.

---

## 3 — 🔴 THE CLASSIFICATION

⭐ **The question has TWO answers, because the quantity and the rule built on it
are not the same object.** Collapsing them is what made this look unresolvable.

### 3.1 — THE QUANTITY `margin_residual` → **CLASS B**
> **B — a broker/local reconciliation artefact.**

🔬 **Unambiguous, by construction.** `margin_residual = held_today − margins.used`
is *literally* LOCAL FundManager state minus BROKER-reported utilised margin. It is
a difference between two ledgers that are **permitted to disagree transiently**
(fills, settlement, marking to market).

⛔ **It is NOT class A.** Nothing in its computation observes capital being
released; a non-zero value means *the two books disagree right now*, ⛔ not *money
moved*. ⛔ **Not C** — no quantity/position term enters it; both operands are ₹.
⛔ **Not D** on its own — the value itself is recomputed fresh every cycle.

### 3.2 — THE TRIGGER (the governance rule) → 🔴 **CLASS E**
> **E — an ambiguous mixture.**

⭐ Because the observable `residual ≈ position value` is producible by **at least
FOUR distinct causes spanning three classes, and the trigger tests only
`carry > 0` + a rupee resemblance — which discriminates none of them:**

| # | cause | class | status |
|---|---|---|---|
| ① | the carry algebra genuinely double-counts ⇒ the armed REVERT signature | **A** | ⛔ **never observed** (§2) |
| ② | G3's own predicted false positive (`:3703-3708`) — broker drops a settled CNC from `used` while `held` retains it | **B** | 📄 predicted **in the code itself**; ⛔ never measured |
| ③ | **broker-`used` LAG** | **B** | 🔬 **MEASURED 26-Aug 11:21→11:31** — `residual 554.58` vs position `573.05`, at `carry=0` |
| ④ | **carry-snapshot staleness — 🆕 NEW, FROM THIS TRACE** | **D** | 💭 INFERENCE from two measured write sites |

**④ in full, because it is new.** 🔬 `_positional_carry` has **exactly two write
sites** in the deployed `capital/fund_manager.py`: `:486` (reset to `0.0` in
`initialize`) and `:1832` (set once at rehydrate). 🔬 **It is NEVER decremented when
a carried position exits.** 🔬 `_intraday_carry` is *permanently* `0.0` — `:1831`
assigns it literally, with a comment saying extending it is owed.
⇒ 💭 Therefore, once a carried CNC exits intraday, `positional_used` falls by its
margin **M** while `carry` stays at **M** ⇒ `held_today = held − carry` under-states
by **M** ⇒ **`margin_residual` goes NEGATIVE with magnitude ≈ the carried position's
value.** 🏷️ **UNPROVEN LIVE** — no carry day has occurred since the check existed,
so this is read from code, ⛔ not measured.

⭐ **A USABLE DISCRIMINATOR FALLS OUT OF ④, AND IT IS FREE:** ①②③ drive the residual
**POSITIVE** (local holds what the broker has released); ④ drives it **NEGATIVE**.
⚠️ 🔴 **The trigger as worded is SIGN-BLIND** — *"residual ≈ the carried CNC amount"*
states a magnitude and no sign. ⇒ ⭐ **Adding sign to the wording would separate ④
from ①②③ at zero cost.** ⛔ **I have NOT changed the wording** — 👤 Rama's.

### 3.3 — WHY NOT SIMPLY "A"
👤 The trigger's *intent* is class **A** — *"the carry algebra is wrong, therefore
capital is wrong."* ⭐ But intent is not classification. 🔬 The trigger's **only**
input is a class-**B** artefact with no threshold, no alert and no gate, whose
signature is shared with a measured class-B transient (③) and a code-read class-D
staleness (④). ⇒ **A rule cannot be classified above the evidence it reads.**

---

## 4 — WHAT THIS CHANGES · AND WHAT IT DOES ⛔ NOT

- ✅ **FILE 13's stated fear is CLOSED: no unit mismatch inside the trigger's path.**
  All operands are ₹. ⚠️ A real ₹/shares collision exists on `CapitalDriftDetected`
  one layer out — 🏷️ recorded, ⛔ not chased.
- ✅ **The escalation fear is CLOSED:** G3 **cannot** arm the kill switch from
  either check (`order_reconciler` ∉ `_ESCALATING_SOURCES`), and `UNRECOVERABLE`
  gates nothing. ⇒ **The trigger's blast radius is a HUMAN revert, ⛔ nothing
  automated.** ⭐ That is *smaller* than feared — ⛔ but a revert of deployed
  capital-path code is still irreversible.
- 🔴 **The trigger stays DISARMED BY POLICY.** ⛔ Nothing here authorises a revert.
  Class **E** + fail-safe **C-3** point the same way: **escalate, ⛔ do not
  adjudicate.**
- ⭐ **The cheapest thing that would make it evaluable is NOT a code change:** it is
  ① a **sign** in the wording and ② the T+1 carry measurement the code has been
  asking for since 20-Aug (*"Owed: measure a T+1 carry, then decide a threshold"*).
  ⛔ Neither was done here.
- ⛔ **NOTHING WAS TUNED.** `capital_drift_tolerance`, `capital_drift_tolerance_pct`,
  `_total`, RESERVE, COMMIT, the buckets and the carry algebra were **read only**.

## 5 — WHAT I DID ⛔ NOT MEASURE
1. **A live carry day.** ⛔ None has occurred since the check existed ⇒ ①, ② and ④
   are all **UNPROVEN LIVE**. This trace is code + historical logs, ⛔ not a T+1.
2. **Whether ④ actually fires.** 💭 Inferred from two write sites; ⛔ never observed.
3. **Broker `used` for a settled CNC holding** — still unmeasured, exactly as
   `:3703-3708` says. ⛔ Still owed.
4. **The ₹/shares `CapitalDriftDetected` collision's blast radius** — I confirmed it
   exists and that `drift_handler` ignores `order_reconciler`; ⛔ I did not audit
   every other consumer of that event.
