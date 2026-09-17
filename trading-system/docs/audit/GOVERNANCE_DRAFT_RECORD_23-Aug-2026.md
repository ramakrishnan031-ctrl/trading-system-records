# DEPLOY-GOVERNANCE DRAFT — RECORDED · 23-Aug-2026 (Sun), afternoon

**Governed by** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
🏷️ **RECORD ONLY · ⛔ NO CODE · ⛔ NO PUSH · ⛔ NO DEPLOY · ⛔ NOT AN AUTHORISATION.**

---

## §0 — STATUS, VERBATIM

```
STATUS = DRAFT / ⛔ NOT ACTIVE
AUTO-PUSH = ⛔ NOT ENABLED
AUTO-DEPLOY = ⛔ NOT ENABLED
TIER 1 / TIER 2 = PROPOSED
RAMA-CONTROLLED TIER = ⛔ RAMA-CONTROLLED
EVIDENCE-BLOCKED = STOP CONDITION
```

⛔ **No deploy-key change is created from this. The existing workflow stands.**

## THE HEADLINE — Rama's reframing, and it is the accurate diagnosis

> ⭐ **AI APPROVAL IS CONDITIONAL ON EVIDENCE ACCESS AND EVIDENCE QUALITY.**
> ⛔ Not *"AI is untrustworthy"*. ⚠️ **The failure mode is a reviewer certifying something
> it could not inspect.**

---

## 🔴 SCOPE LIMIT — STATED FIRST, BECAUSE IT GOVERNS EVERYTHING BELOW

**The governance draft and Rama's reply are NOT in this repository.** Measured today:
`grep -rniI 'evidence[- ]blocked'` over the whole repo (excluding `.git`/`venv`) returns
**zero hits**; so does a search for the tier model, the A–L evidence contract, and the
`AUTO-PUSH`/`AUTO-DEPLOY` block. `docs/decisions/cards/` holds nothing later than
08-Aug. ⇒ they are **external**, which is by design (cards and decision sheets stay
external).

⚠️ **CONSEQUENCE, and it is exactly the draft's own subject:** I have **not read** §§1–13,
§4's A–L, or §11. Everything I say about their *content* is **📄 from provided evidence** —
the card's own quotation of them — ⛔ never 🔬 measured.

⭐ **That is this session's own EVIDENCE-BLOCKED state, and the right response is the one
§2 proposes:** ⛔ do not certify what cannot be inspected; ⭐ label it and obtain the
missing evidence. **I cannot confirm the §1 collision by reading it, and I have not
pretended to.**

---

## §4 (TAKEN FIRST — ⭐ ADOPTED NOW, IT NEEDS NOTHING)

**In use from this document onward, in every direction — Rama's cards, ChatGPT's reviews,
my reports:**

| label | meaning |
|---|---|
| 🔬 **VERIFIED BY DIRECT MEASUREMENT** | I ran it, at a named SHA |
| 📄 **VERIFIED FROM PROVIDED EVIDENCE** | read in a supplied report; ⛔ not independently run |
| 💭 **INFERENCE / INTERPRETATION** | reasoned, ⛔ not measured |
| 👤 **USER / POLICY DECISION** | Rama's, ⛔ nobody else's |

⭐ **The test case is real, not hypothetical.** *"`N9-10` is recorded against `65b7196`"*
was written as fact and later corrected — it was 💭. **The label alone would have caught
it**, because writing 💭 forces the question *"then what would 🔬 look like?"*
⭐ Today's §1 refusal (the unsourceable *"Rs 35k/5"* quote) is the same mechanism working
**before** the error instead of after.

---

## §1 — 🔴 THE COLLISION · SURFACED · ⛔ NOT RESOLVED

📄 **From the card** (⛔ I could not open the document to confirm):

| where | text | meaning |
|---|---|---|
| §6 | *"TIER 3 — I AGREE"* → sizing, risk, capital, kill switch | ⇒ **RAMA-CONTROLLED** |
| §13 | *"TIER 3 = RAMA-CONTROLLED"* | ⇒ **RAMA-CONTROLLED** |
| §10 | *"TIER 3 — EVIDENCE-BLOCKED / AMBIGUOUS"* | ⇒ **A STOP CONDITION** |

⇒ **one label, two meanings, in one document.**

⛔ **NOT resolved by picking one.** 👤 **Rama names them.** ⚠️ Ambiguity in a governance
label already cost him a full night once.

### ⚠️ ONE CORRECTION TO THE CARD'S COUNT — 🔬 measured

The card calls this *"the third instance this weekend, after the bare 'one scrip per day'
and the trading-vs-deployment collision."* **The record already counts three.**
`docs/audit/OPS_FINDINGS_22-Aug-2026_evening.md:530-532`, verbatim:

> *"This is a THIRD instance of the class `N20-56` was created to prevent — hours after it
> was created. `N20-56` retired the bare phrase 'one scrip per day' precisely because it
> cost a night of ambiguity; **`N22-10` did the same for a bare `F1`/`F6`**."*

⇒ priors are **(1)** bare *"one scrip per day"* (`N20-56`) · **(2)** bare `F1`/`F6`
(`N22-10`) · **(3)** the phrase escaping into deployment governance.
⭐ **TIER 3 is therefore the FOURTH instance, not the third.** The card omitted `N22-10`.
⚠️ The count matters: a recurrence rate is the argument for a structural fix rather than
another one-off retirement.

---

## §2 — EVIDENCE-BLOCKED IS A STATE, NOT A TIER · ⛔ PROPOSED, NOT ADOPTED

A tier answers **"who may authorise this?"** EVIDENCE-BLOCKED answers **"can this be
assessed at all?"** ⇒ different axes; stacking them **creates** the §1 collision.

```
TIERS   0 / 1 / 2        — WHO AUTHORISES          (one axis)
STATUS  EVIDENCE-BLOCKED — CAN IT BE ASSESSED?     (orthogonal; attaches to ANY tier)

when EVIDENCE-BLOCKED attaches:
   ⛔ automation stops
   ⭐ the missing evidence is obtained
   ⛔ the ENGINEERING question is NOT escalated to Rama merely because evidence is thin
```

⚠️ **A TIER 1 change can be EVIDENCE-BLOCKED** — e.g. nobody can confirm the diff really is
docs-only. So can Tier 2, so can a Rama-tier change.

⭐ **This session is a live worked example** (🔬): the draft is unreadable from here ⇒ this
record is EVIDENCE-BLOCKED **at every tier at once**, which is only expressible if the
state is orthogonal.

👤 ⛔ Rama's call. Not adopted.

---

## §3 — THE GAP · ⛔ PROPOSED, NOT ADOPTED — ⚠️ **AND THE CARD'S OWN EXAMPLE INVERTS IT**

📄 The gap as stated: TIER 1 = non-executable · TIER 2 = **measured behaviour-neutral**
code · RAMA = policy/risk/live-money. ⇒ **where does a change go that changes behaviour and
contains no policy?** A crash fix, a race fix, any bug whose whole purpose is to change
what happens.

⭐ **The gap is REAL.** The proposal:

```
TIER 2a — MEASURED BEHAVIOUR-NEUTRAL                          (as drafted)
TIER 2b — BEHAVIOUR-CHANGING, NON-POLICY, with EVERY changed
          surface ENUMERATED IN ADVANCE + a control proving each moves
```
⚠️ 2b needs a **stricter** first-live-observation rule than 2a, ⛔ not looser — because
there **is** something to observe. ⛔ 2b must not become a hole a policy change walks
through.

### 🔴 BUT NI-1 IS THE WRONG WITNESS — 🔬 MEASURED TODAY

📄 The card offers NI-1 as the case that falls through: *"no percentage, no threshold, no
risk semantic."* **The first half is right. The conclusion is not.**

🔬 Measured at `742d9da`:

| | |
|---|---|
| `capital/position_sizer.py:323` | `# ── PS10: SL direction sanity (WARNING only, calc proceeds) ──` |
| the defect | `_warn` passed `"msg"` — a reserved `LogRecord` attribute ⇒ `makeRecord` raised `KeyError` **out of `calculate()`** |
| the call site | `signals/signal_processor.py:1001` catches **only `BrokerError`** |
| where it landed | `signal_processor.py:418` `except Exception` → *"Unhandled exception in pipeline"* → `update_signal_status(signal_id, "PLACEMENT_FAILED", …)` |

⇒ 🔴 **BEFORE NI-1: a BUY with `sl > entry` was recorded `PLACEMENT_FAILED` — no sizing, no
reservation, NO ORDER. AFTER NI-1: it warns, `calc proceeds`, and the signal continues to
risk approval → capital reservation → PLACEMENT.**

⭐ **A class of malformed signal that could never place an order can now place one.** That
is the **money path** — `PRE_BUILD_REVIEW_GATE`'s own major-impact list names both *"Signal
path"* and *"Capital / sizing / risk"*.

⇒ 🔴 **NI-1 does not demonstrate that a behaviour-changing non-policy change falls through
the model. It demonstrates that *"contains no policy"* IS THE WRONG TEST.** ⭐ **The
discriminator must be REACH — what the change can cause — ⛔ not whether a number moved.**

⚠️ ⛔ **Do not read this as "NI-1 is wrong."** It restores PS10's stated design and the
`KeyError` was plainly a defect. The point is **classification**: under *"no policy ⇒ 2b"*
NI-1 would be self-approvable, and it should not be.

---

## §5 — THE MODEL TESTED AGAINST THIS WEEKEND · ⭐ AMBIGUITIES NAMED, ⛔ NOT RESOLVED

⚠️ The purpose is to **find where the model is ambiguous**, ⛔ not to confirm it works.

| # | change | card says | 🔬 measured | verdict |
|---|---|---|---|---|
| **1** | **F1 `d00e574`** | *"behaviour-neutral, prediction frozen, control present"* | 🔴 **NOT behaviour-neutral.** `test_unconfigured_delivery_refuses_it_does_not_inherit`: *"NOW: sizing a DELIVERY entry without delivery config **RAISES**"*. And F1 + NI-4 route seven keys into `main.py:1862` ⇒ **exit 5 can stop the UNATTENDED 08:15 boot** | 🔴 **THE CARD'S OWN PREMISE FAILS.** F1 is fail-closed = behaviour-changing **on the boot path** ⇒ **2b at best, arguably Rama's** |
| **2** | **NI stack `742d9da`** | *"7 commits, but NI-1 changes behaviour"* | 🔬 mixed: NI-1 money-path · NI-2 auditor C2 now fires where it did not · NI-4 config fail-closed (boot path) · NI-3/NI-6 docs · NI-7 pure rename · job-1 tests | 🔴 **A BUNDLE SPANNING TIERS. The model has no rule for one.** Does a bundle take its **highest** tier? If yes, §4's push 2 is a Rama-tier push |
| **3** | **NI-5 `a4a5cef`** | *"Tier 2, or Rama's?"* | 🔬 **Both, depending on the lens.** As a **contract** it is behaviour-changing (construction now raises). On the **deployed path** it is behaviour-**neutral** — measured: `main.py:2501` already passes all three keys, so no production call site changes | 🔴 **THE PREDICTED SPLIT IS REAL.** 2a by measurement, 2b by intent. ⇒ **the model must say which lens governs** |
| **4** | **OPS ②** | *"obviously Rama's — a control case"* | 🔬 agreed — boot path, needs `sudo`, and ⭐ **deploy does not install unit files at all**: it is a manual VM act, ⛔ not a repo change | ⚠️ **A CONTROL CASE THAT EXPOSES A GAP: the tiers classify *code changes*. OPS ② is an INFRASTRUCTURE act with no commit.** The model does not reach it |
| **5** | **group-F WARN question** | *"pure policy, zero code"* | 🔬 agreed — 👤 Rama's | ⚠️ **BUT:** it is a **severity** decision, and `PRE_BUILD_REVIEW_GATE` **already** lists *"Alerting — routing, severity, channels, thresholds"* as major impact |

### 🔴 THE STRUCTURAL FINDING §5 PRODUCED — ⛔ THE CARD DID NOT NAME IT

Cases 4 and 5 together expose a **second classification system**. `PRE_BUILD_REVIEW_GATE`
(`23ea03d`) already carries *"WHAT COUNTS AS MAJOR IMPACT"* — capital/sizing/risk, order
path, exit logic, kill switch, schema/DB, config schema, signal path, broker adapter, boot
path, cron/scheduler, **alerting** — closing with *"If unsure whether something qualifies:
**it qualifies.**"*

⇒ 🔴 **The tier model and the gate's list will overlap and can disagree.** ⚠️ Two
overlapping classifiers is the `N20-56` failure at the level of a whole framework rather
than a phrase. **The draft must state its relationship to that list — subordinate to it,
superseding it, or a refinement inside it.** ⛔ Unstated today.
⭐ **And the safe default already exists and must not be weakened:** *"if unsure, it
qualifies."*

---

## §6 — ACCEPTED WITHOUT CHANGE, AND ONE WORDING FIX

📄 Accepted as reported: **§4's A–L evidence contract** — ⭐ especially **B** (exact diff,
⛔ not a prose summary) and **E** (a negative control); **§5** first-live-observation
(⚠️ a Sunday 21:00 push ≠ a Monday evening push — the 08:15 boot is the first execution and
nobody is watching); **§9** separating PUSH from DEPLOY authority (⭐ the escape hatch for a
future staging step, even though today's post-receive hook couples them); **§8**'s
escalation rule (policy → Rama, engineering → the evidence); **§11**'s not-authorised list.

⭐ **B and E are the two that close the gap I named** — an exact diff is what makes
EVIDENCE-BLOCKED detectable, and a negative control is what makes a green check evidence.

### 🔴 THE §11 WORDING CORRECTION — ⛔ RECORDED, ⚠️ **I CANNOT APPLY IT**

⛔ **§11 is not in this repository** (measured above), so I cannot edit it. **The
replacement text, to be applied by whoever holds the document:**

> ⛔ **REPLACE:** *"implementation of the missing allocation ceiling"*
>
> ⭐ **WITH:** *"any change to the tier/performance multiplier ceiling. ⚠️ Note the
> ceiling is **not merely missing**: deployed `4568385:capital/position_sizer.py:530`
> **carries the exact FIX-133 expression `max(1, min(tiered_qty, raw_qty * 2))` that
> `65b7196` DELETED as forbidden** — the presence of a thing a locked decision removed.
> 🔴 **AND THERE IS NO ALLOCATION FOR A CEILING TO BE OF:** `capital/pipeline_policy.py`
> does not exist on deployed and `allocation_divisor` has zero hits there; both are
> `65b7196`-only. ⇒ ⛔ **porting `min(1.0, …)` across would NOT implement this** — it would
> clamp against a rung that is 10% of TOTAL CAPITAL, a different rule wearing the locked
> policy's words."*

⭐ Rationale: the old phrasing **invites someone to port a clamp**. 🔬 Full measurement in
`docs/audit/F12_INSTANCE3_AND_GATE_GUARD_23-Aug-2026.md` §1.

---

## STATUS

⛔ **NOT PUSHED · NOT DEPLOYED · `origin/main` = `45683859a0a05f466189ac5bc98f9a9f089f98d3`.**
⛔ No code. ⛔ Nothing adopted. ⛔ Nothing authorised. ⛔ No deploy-key change.
⛔ The existing workflow stands.

**Open and owed to Rama:** the §1 TIER-3 naming (⚠️ **fourth** instance, not third) · §2
tier-vs-state · §3 the 2a/2b split **and the REACH-not-policy discriminator** · §5's four
ambiguities · **the draft's relationship to `PRE_BUILD_REVIEW_GATE`'s major-impact list** ·
the group-F `PASS`-vs-`WARN` question (still unanswered from this morning).
