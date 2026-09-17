# FROZEN PREDICTION — JOB 1 (fill every empty delivery setting) + JOB 2 (NI-1 … NI-8)

**Written:** 22-Aug-2026 (Saturday) evening, IST — **BEFORE any line of the build was written.**
**Card:** VS CODE CLAUDE, "TWO JOBS, NOTHING ELSE", issued 16:30 IST 22-Aug-2026.
**Governed by:** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).

**Base, MEASURED not recalled:**
- `git ls-remote origin refs/heads/main` -> deployed `45683859a0a05f466189ac5bc98f9a9f089f98d3`
- **This unit's base is `d00e574323a0b19cf0f98c3fca65031925d027cc` (F1)**, whose parent is
  `4568385`. Confirmed by `git rev-parse d00e574^`. F1 is BUILT · GATED · ⛔ UNPUSHED.
- **Build worktree:** `scratchpad/j2-work`, branch `fix/delivery-fill-and-ni-22aug`, off `d00e574`.
- **Gate base worktree:** `scratchpad/j2-base`, detached at `d00e574`.

**Status at freeze time:** `NOT BUILT · NOT GATED · NOT PUSHED · NOT DEPLOYED · NOT VERIFIED LIVE`.

---

## 0 · THE HEADLINE PREDICTION — JOB 1 FILLS NOTHING

**Predicted:** the JOB 1 sweep finds **ZERO** delivery-scoped settings that are `null`,
absent, or unset in the live config. Every one of them is already explicitly present with
a value. JOB 1 therefore writes **no** config value at all.

**Why this is predicted rather than hoped:** all 64 pydantic models in
`core/config_loader.py` carry `extra="forbid"` (measured, with a control proving an unknown
key is rejected), so the set of *possible* config keys **is** the schema field set. The
delivery-scoped subset of that field set is 13 fields, and all 13 resolve to a non-null
value on load.

**Falsifier:** any delivery-scoped key that loads as `None`, or that is absent from the
YAML and supplied by a schema default *and whose intraday twin carries the same number*
(i.e. a genuine silent inheritance F1 missed). If one is found, JOB 1 fills it and this
prediction is scored WRONG.

**The trap this prediction exists to name:** two delivery-scoped keys —
`risk.max_open_delivery_positions` (3) and `risk.max_daily_delivery_trades` (5) — LOOK like
JOB 1 candidates because their schema defaults are silent. They are **not** candidates:
they are explicitly set in the YAML, and their intraday twins are **5** and **10**. Writing
the intraday value into them would move the delivery caps 3→5 and 5→10 — a **real
loosening of a live risk limit**. The card's own tripwire covers this exactly: *"IF A
FILLED VALUE CHANGES A COMPUTED QUANTITY, IT CAME FROM THE WRONG PLACE."*
**Predicted: they are NOT filled; NI-4 fixes their schema instead, values untouched.**

---

## 1 · PREDICTIONS WITH EXPLICIT FALSIFIERS

### P-1 — JOB 1 is behaviour-neutral because it is empty
**Predicted:** `config/system_config.yaml` is **byte-identical** before and after JOB 1.
**Falsifier:** any diff hunk in the YAML attributable to JOB 1 (NI-3's comment-only edit at
`:214-215` is JOB 2, and is the only YAML change predicted in the whole pass).

### P-2 — NI-1: the fix is two words, and the OLD tests cannot see it
**Predicted:** at `d00e574`, `capital/position_sizer.py:328` and `:334` pass `"msg"` into
`_warn`'s extra dict; `_warn` (`:740`) calls `self._log.warning(msg, extra=extra)`; a REAL
`logging.Logger` raises `KeyError: "Attempt to overwrite 'msg' in LogRecord"`.
**Already proven by experiment at the base tree, ⛔ not by reading** — `KeyError` observed.
**Predicted further:** the two existing tests (`tests/unit/test_position_sizer.py:456`,
`:468`) **still pass on the UNFIXED tree**, because `_MockLogger.warning` just appends to a
list and never builds a `LogRecord`.
**Falsifier:** the new real-logger test passes on the base tree (⇒ it is blind too), or the
two old tests fail on the base tree (⇒ my account of why they are blind is wrong).

### P-3 — NI-2: C2 is algebraically silent on the multiplier
**Predicted:** `core/config_auditor.py:414` compares `posv <= conc` with no multiplier term.
With `max_multiplier: 2.0` and a hypothetical `conc=0.25 / posv=0.40`, C2 stays SILENT while
the effective ceiling `0.25 × 2.0 = 0.50 > 0.40` — the backstop would bind on routine sizing.
**Predicted:** after the fix C2 fires on that input, and stays silent on the SHIPPED config
(`conc=0.10`, `posv=0.40`, `max_multiplier=2.0` ⇒ effective `0.20 < 0.40`).
**⇒ zero new findings on the live config. Falsifier:** the shipped config produces a C2
finding after the change.

### P-4 — NI-3 is comments only
**Predicted:** the NI-3 commit's diff contains **no executable line**. `git diff` shows only
comment lines. **Falsifier:** any non-comment line in that commit's diff.
**Predicted en route:** there are **FOUR** copies of the "inert while force_intraday_only"
claim on these two keys, not the three the card names — the fourth is
`core/config_loader.py:552`. It is reported; whether it is edited is stated in the report.

### P-5 — NI-4 is behaviour-neutral on the shipped config
**Predicted:** making `max_open_delivery_positions` / `max_daily_delivery_trades` REQUIRED
changes nothing at load time, because both are already present (3 and 5). Deleting either
from the YAML, or nulling it, rejects at startup **naming the key**, exit 5 — the same
`_config_error_detail` path F1 already proved end-to-end.
**Falsifier:** the shipped config fails to load, or a missing key still boots on 3/5.

### P-6 — NI-5's diff stays inside the tripwire
**Measured before the build:** an AST sweep finds **20** `PositionSizer(...)` call sites in
the whole tree; **every one is keyword-only (0 positional args)**; **15** of them would need
an edit if all three POLICY defaults become required; those 15 live in **8 files, all under
`tests/`**. `main.py:2501` already passes all three explicitly.
**Predicted classification:** exactly THREE parameters are SAFETY-CRITICAL POLICY and lose
their default — `risk_per_trade_pct` (0.01), `max_concentration_pct` (0.10),
`max_position_value_pct` (0.40). Everything else in that signature stays defaulted, and the
reason for each is recorded.
**Falsifier:** the diff reaches any file outside `capital/position_sizer.py` + `tests/`, or
the edited-site count exceeds ~20.

### P-7 — NI-7 is a pure rename
**Predicted:** `git show --stat` reports the NI-7 commit as a **R100** rename with zero
content lines changed.
**Falsifier:** any similarity index below 100, or any `+`/`-` content line.

### P-8 — the gate is set-equal at ID level
**Predicted:** BASE (`j2-base` @ `d00e574`) and UNIT run the same standing failure set —
the campaign's enumerated 7 — with **0 NEW** and **0 DISAPPEARED**, and a passed-count delta
that is fully accounted for by arithmetic (new tests added, minus none removed).
⛔ **No message-level claim is made** (`N20-19`: it would be vacuous on `pytest -q` output).
**Falsifier:** any id in `comm -13` or `comm -23`, or a passed-delta that does not decompose.

### P-9 — nothing in this pass moves a computed quantity
**Predicted:** no percentage, cap, count, multiplier or rupee value changes anywhere in the
tree. The only *behavioural* change in the whole pass is NI-1 (a warning that logs instead
of raising) and NI-4/NI-5 (a **missing** value now refuses instead of silently defaulting).
**Falsifier:** any config value diff, or any sizing/gating quantity that moves.

---

## 2 · WHAT IS PREDICTED **NOT** TO HAPPEN

- ⛔ No deploy. ⛔ No push. ⛔ No `sudo`. ⛔ No VM contact.
- ⛔ The root worktree is not switched, not committed to, and
  `docs/MASTER_PENDING_01-Aug-2026.md` stays uncommitted and intact.
- ⛔ `65b7196` / `feat/delivery-config-split` / the allocation model are not read, not
  merged, not deleted.
- ⛔ Rama's uploaded config is not read.
- ⛔ No strategy YAML is touched. ⛔ No tier value is touched. ⛔ F2 / F2a / MIS 3.5× untouched.
- ⛔ `sl_gap_buffer_pct`'s percent-vs-fraction inconsistency is RECORDED, not fixed.

---

## 3 · SCORING RULE

Each P-n is scored CONFIRMED / WRONG / NOT TESTED against measured evidence, and a WRONG
call is reported as WRONG — ⛔ never quietly dropped, ⛔ never restated as a narrower claim
that happens to be true. (`diffnkg` 11-Aug: a failed direction call is not evidence the
mechanism is safe.)
