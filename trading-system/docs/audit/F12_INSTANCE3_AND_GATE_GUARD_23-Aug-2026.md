# THE CONNECTION, THE REWORDING, AND TWO ITEMS OPENED — 23-Aug-2026 (Sun), afternoon

**Governed by** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
🏷️ **RECORD ONLY · ⛔ NO CODE · ⛔ NO PUSH · ⛔ NO DEPLOY · ⛔ NO REVIVAL OF `65b7196`.**
Companion to `docs/audit/FOUR_DECISIONS_23-Aug-2026.md` (this morning).

---

# §1 — 🔴 THE REWORDING. **THIS IS THE SENTENCE THAT MUST SURVIVE.**

⛔ **NOT:** *"the clamp is missing from deployed"* / *"the clamp was never ported"*.
⭐ **BUT:**

> 🔴 **The deployed sizer CARRIES THE EXACT FIX-133 EXPRESSION THAT `65b7196` DELETED AS
> FORBIDDEN.** It is not an absent protection — it is the **presence of a thing a later,
> LOCKED decision explicitly removed.**

| | |
|---|---|
| `65b7196` | `effective_mult = min(1.0, tier × perf_weight)` — and `max(1, min(tiered, raw*2))` **DELETED** |
| **deployed `4568385`** | `:470` `effective_mult = tier_mult * max(0.0, perf_weight)` — no upper clamp · `:530` `tiered_qty = max(1, min(tiered_qty, raw_qty * 2))` — the **2× ceiling**, still there |

⚠️ **Why the wording is load-bearing:** *"never ported"* invites the next reader to port it.
*"deployed carries an expression a locked decision deleted"* tells them **why porting alone
is not the answer.**

## 🔴 AND THE PART THAT DECIDES IT: THERE IS NO ALLOCATION FOR A CEILING TO BE *OF*

⭐ **Re-verified today, and it is now doubly sourced — this is not an inference:**

| measured | deployed `4568385` | `65b7196` |
|---|---|---|
| `capital/pipeline_policy.py` | 🔴 **DOES NOT EXIST** (`git ls-tree`) | present (blob `0a01204…`) |
| `allocation_divisor` | 🔴 **ZERO hits** repo-wide (`git grep`) | `capital/position_sizer.py:433` |
| `base_allocation = basis / allocation_divisor` | 🔴 **absent** | `:439` |
| the per-trade basis | `avail = snap.intraday_avail` (`:294`) → `qty_by_capital = floor(avail / margin_per_share)` (`:419`); `fund_manager.py:478` `_intraday_avail = broker_balance * _intraday_pct` — **the WHOLE bucket** | `basis = segment_bucket × planning_leverage` |

`65b7196:capital/position_sizer.py:13-14`, verbatim — the model stated in its own code:

```
basis       = segment_bucket x planning_leverage   # 5x MIS, 1x delivery
allocation  = (basis / max_daily_trades) x tier_multiplier
raw_qty     = (allocation x stop_pct) / sl_rupees  # == allocation / entry
```

⇒ 🔴 **RECORD THIS EXPLICITLY, SO NOBODY TRIES:**
**NI-16 CANNOT BE FIXED BY COPYING `min(1.0, …)` ACROSS.**
`min(1.0, …)` clamps a multiplier **to one allocation**. Deployed **computes no
allocation** — the machinery that would produce one (`pipeline_policy.py`,
`allocation_divisor`, `base_allocation`) exists **only** in the undeployed tree. ⛔ You
cannot clamp to a single allocation in a system that does not compute one. Porting the
one-line clamp would clamp `tier × perf_weight` to 1.0 against a rung that is **10% of
total capital**, ⛔ which is not the locked policy — it is a different rule wearing its
words.

## ⚠️ A SECOND INSTANCE OF THE SCOPE-LOSS I FLAGGED THIS MORNING

`PATHS.md:104` states *"DIVISOR — `capital/position_sizer.py:433` `allocation_divisor =
int(pol.max_daily_trades or 0)`"* **without naming the tree.** Measured today: that line,
that file and `pipeline_policy.py` are **`65b7196`-only**. ⭐ Same shape as the memory
index line corrected this morning: the measurement was right, the **compression lost the
scope**, and as written it reads as a claim about deployed. ⛔ Not edited here (`PATHS.md`
is a tracked, in-flight file) — **recorded for the next register pass.**

---

# §2 — 🔴 F12 · INSTANCE 3 — RECORDED, ⛔ AND ONE CLAIM REFUSED

## ⛔ FIRST, THE REFUSAL — I CANNOT SOURCE THE QUOTE THE CARD ATTRIBUTES TO RAMA

The card asks me to record, as Rama's own 21-Aug words:

> *"Order Value per scrip = Rs 35k/5 = Rs 10k which is the maximum capital value per stock
> in MIS"*

🔴 **I could not source that sentence, and I am not recording it as his.**

**SEARCH WIDTH STATED** (the absence-needs-a-wide-check rule): case-insensitive `grep -rn`
over the **entire repo** (excluding `.git`/`venv`) for `per scrip`, `order value`,
`maximum capital value`, `capital value per stock`, `35k`, `35,000`, `Rs 10k`; plus
`docs/MASTER_REGISTER.md` on **`main`** (`3dff752`), which is not on this branch; plus
every file mentioning `21-Aug`. ⇒ **zero hits.**

⚠️ **AND THE ARITHMETIC DOES NOT HOLD.** `35,000 ÷ 5 = 7,000`, not `10,000`. The
campaign's own measured table (`PATHS.md:104`) gives, at MIS basis ₹35,000:
`÷10 = ₹3,500 · ÷6 = ₹5,833 · ₹5 = ₹7,000`. And `65b7196`'s **actual** divisor is
`max_daily_trades = 6` ⇒ **₹5,833**. ⛔ **No divisor produces ₹10,000.**

⇒ 🔴 This is the **`WC-PATTERN #7` shape** — a card speaking for Rama. ⛔ **Neither a card
nor a reviewer may speak for Rama**, and an unsourced value does not age into being
sourced. The sentence may well be real and living in an **external card** (cards stay
external by design) — ⭐ **but only a quoted, timestamped Rama line closes it, and until
he supplies one this stays UNSOURCED.**

## ⭐ WHAT *IS* SOURCED — AND IT CARRIES THE FINDING ANYWAY

The **one** verbatim 21-Aug Rama instruction on record
(`docs/audit/F2_SEGMENT_CAPITAL_INVENTORY_22-Aug-2026.md:16`, filed `WC-PATTERN #7` /
`N22-01`):

> **RAMA, 21-Aug:** *"Please change every calculations of each segment (MIS & GTT) must be
> carried out on 'Segment capital' not real cash… If possible fix capital drift & capitals
> used to segment cash now."*

**And `N9-10`'s locked text, 08-Aug** (status *"✅ CLOSED (decision final)"*; it cites
*"build record §4.1"* and the test name — ⚠️ **it names no SHA**, a correction already on
record):

> **N9-10, LOCKED 08-Aug:** *"Performance and tier may move a trade's allocation up or
> down **WITHIN the single-allocation ceiling** — ⛔ they may never spend a second trade's
> allocation."*

**Side by side, that is one design:** Rama's sentence fixes the **BASIS** (segment capital,
not real cash); `N9-10` fixes the **CEILING** on that basis (one allocation). And
`65b7196:capital/position_sizer.py:13-14` implements **both halves in one expression** —
`basis = segment_bucket × planning_leverage`, `allocation = basis / max_daily_trades`.

⇒ ⭐ **The structural claim the card makes is CORRECT and is now verified in code.** Only
the quotation and its arithmetic are not.

## 🔴 F12 · INSTANCE 3 — THE ROW

`F12 · THE ALREADY-BUILT ANSWER` (opened 22-Aug, `MIN_RULE_AND_DELIVERY_LIMITS_22-Aug-2026.md
§3`, 🏷️ `OPENED · ⛔ NOT STARTED · ⛔ NOT DESIGNED`) currently lists **two** instances. Add
the third:

| # | the thing | built in `65b7196` | deployed? |
|---|---|---|---|
| 1 | F1's null-fails-closed rule | `capital/pipeline_policy.py:226-238` | ⛔ no — **rebuilt this weekend as `d00e574`** |
| 2 | the multiplier clamp | `min(1.0, tier × perf_weight)` + `…clamped_to_one…` | ⛔ no — **deployed does the OPPOSITE (`raw_qty * 2`)** |
| 3 | ⭐ **the segment-capital allocation model itself** | `position_sizer.py:13-14` · `pipeline_policy.py` · `allocation_divisor:433` · `base_allocation:439` | ⛔ no — **and FIX-F2 is inventorying it as new work** |

⚠️ **Instance 3 is the largest, and it is partly on record already:** commit `3dff752`
(main, 22-Aug 16:00) states *"`position_sizer.py:13-14` computes `basis = segment_bucket x
planning_leverage` with 5x MIS and 1x delivery, **which is FIX-F2's segment capital,
already implemented**"*. ⇒ ⭐ **the finding existed; it was never added to F12's numbered
list.** That is the gap this row closes.

🔴 **THE COST, restated in F12's own terms:** not the rediscovery — **the risk of building a
SECOND, DIFFERENT solution to the same rule.** Instance 1 already happened (`d00e574`
re-implements `65b7196`'s rule). Instance 3 is the same risk at the scale of a whole model.

⛔ **I am NOT proposing to revive `65b7196`.** ⛔ Its status is unchanged, `N9-10` is
unchanged, F1 is not reopened. ⭐ **The decision is Rama's**, and `3dff752` already records
the stop: *"before any deploy, Rama decides whether FIX-F1 stands or whether `65b7196`
supersedes it."*

---

# §3 — 🔴 NEW ITEM · **THE GATE MUST REFUSE TO RUN, NOT MISREPORT** · ⛔ PROPOSED, NOT BUILT

🏷️ `OPENED · ⛔ NOT DESIGNED · ⛔ NOT BUILT.`

**The evidence** (measured today, both directions, both trees):
`D:/Projects/trading-system/venv/` is **EMPTY** and no sibling worktree has one, so
`scripts/ist_now.sh:pick_python()` falls past `$REPO_ROOT/venv/Scripts/python.exe` to
`command -v python3` — the **WindowsApps stub**. Result: **3 spurious failures** in
`tests/unit/test_t4_deploy_preflight.py`, so a raw gate reads **10F where the record says
7F**. With `PYTHON=/c/python311/python` → **9 passed**. ⚠️ A PATH shim for `python3` is
**NOT** sufficient — measured.

🔴 **WHY A MEMORY NOTE IS NOT ENOUGH.** The next person to run a gate reads 10F and either
(a) calls it a regression, or (b) **normalises three failures that are not real.**
⭐ **(b) is worse** — it widens the accepted-failure set, and the next genuine regression
hides inside it.

**THE PROPOSAL — a precondition check that FAILS LOUDLY AND NAMES THE LEVER:** the gate
refuses to run when `$PYTHON` is unset **and** no usable venv interpreter exists, printing
the exact export to set. ⛔ It must not warn-and-continue.

⭐ **This is the same principle as the fail-closed config rule this campaign just shipped,
one layer out:** ⛔ **a harness that silently produces a wrong baseline is an inert
control** — the F11 shape, applied to our own instrument. ⚠️ And note the symmetry: NI-5
removed silent defaults from the sizer *because* a silent value sizes real money; a silent
interpreter fallback silently sizes **our confidence**.

⛔ **Not written now**, per the card.

---

# §4 — 🔴 FOR RAMA · ONE QUESTION, UNANSWERED

> **Should a guard that cannot find its target report `PASS`, or `WARN`?**

**Today it reports `PASS`.** `config_auditor.py`'s group F now makes the case **visible**
(`outcome: 'unresolved'`) instead of dropping it silently — but the severity is unchanged,
because **alerting is major-impact under the pre-build gate and is not mine to take.**

⚠️ **Note for the decision:** `PASS` here is **the same shape as everything else found this
weekend** — a control reporting healthy while constraining nothing. NI-14 (a threshold that
always fires) · NI-15 (a watch list that misses its target) · the alert guard · `N9-10`
(a CLOSED governance row asserting a clamp nothing enforces) · and group F itself before
today. ⭐ **A rename that silently kills the guard is exactly the failure this branch would
otherwise hide.**

⛔ Unanswered. ⛔ Not changed.

---

# STATUS

⛔ **NOT PUSHED · NOT DEPLOYED · `origin/main` = `45683859a0a05f466189ac5bc98f9a9f089f98d3`.**
⛔ No code written. ⛔ `65b7196` not revived, not merged, not modified. ⛔ `N9-10` status
unchanged. ⛔ F1 not reopened. ⛔ `max_multiplier` 2.0. ⛔ NI-16 not designed.

**Rows to open at the next register pass** (⛔ not written by me — `MASTER_REGISTER.md`
lives on `main`, not on this branch):
`F12` instance **3** · the gate-precondition item (§3) · the group-F severity question (§4)
· `PATHS.md:104`'s missing tree qualifier (§1).
