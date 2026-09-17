---
name: delivery-book-ceiling-10aug
description: "A full overnight delivery book hard-kills the next 08:15 boot at ANY capital level — the ceiling is a ratio (76.9% of the positional bucket), not a rupee figure, because _total is re-measured across the settlement boundary while the reservation replay is not re-based."
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-10T08:35:44.372Z
  originSessionId: 066e06b5-7945-47b6-a4f7-994bd13d28a9
---

**10-Aug-2026 · the 08:15 boot HARD_KILLed on `NEGATIVE_MARGIN_AVAILABLE: -844.0800`
(`bucket=positional`, `08:15:25.680`, from `rehydrate_from_open_trades` → `main.py:2469`).**
⛔ **READ-ONLY all day: no restart, no kill-clear, no fix, no push.** Measured at the **DEPLOYED ref
`645728d`** by md5 on the running files (the VM is not a git checkout), ⛔ not local `main` (48 ahead).

---

## ① THE MECHANISM — ⛔ NOT THE ONE FIRST HYPOTHESISED

⛔ **There is NO broker `margin_used` input anywhere in the path** *(width: `git grep` over the whole
deployed tree)*. It is a **purely internal identity**, and it breaks because:

> ## 🔑 **`_total` IS RE-MEASURED ACROSS THE SETTLEMENT BOUNDARY WHILE THE RESERVATION REPLAY IS NOT RE-BASED.**

✅ **Reconciles exactly, zero residual:** `0.30 × 209.80 = 62.94` cash floor vs `446.106 + 460.91632
= 907.02` replayed ⇒ `−844.08`; the ledger identity closed at `delta = 5.68e-14`.
⛔⛔ **THE LEDGER WAS NOT CORRUPT — every rupee reconciles and ONLY INV6's SIGN GUARD FIRED.**
Treating it as data corruption sends the fix after the wrong component.

⭐ **The pivot is `leverage_map.DELIVERY: 1.0`** — a delivery reservation is the **FULL purchase
value** *(verified: `1 × 446.106` and `4 × 115.22908`)*. **05-Aug is the first day the operand could
exist.** Same defect, same line, as [[capital-drift-is-operand-mismatch-05aug]] — **either operand
moving breaks it: cash falling (today) or the book rising (the ceiling below).**

---

## ② 🔴 THE FORWARD FINDING — ⛔ A RATIO, NEVER A RUPEE FIGURE

**`D` = Σ `margin_reserved` of OPEN delivery trades · `C₁` = boot-day broker net cash · `C₀` = cash
the book was bought from · tolerance `1.0`.**

```
boot survives iff   D ≤ 0.30 × C₁ + 1
a CNC buy debits cash ⇒  C₁ ≈ C₀ − D
────────────────────────────────────────────
  D ≤ (0.30·C₀ + 1)/1.30  ≈  0.2308 × C₀
  bucket the sizer may fill = 0.30 × C₀
  ⇒ 0.2308 / 0.30 = 0.769
────────────────────────────────────────────
```

> ## ⭐⭐ **ANY OVERNIGHT DELIVERY BOOK ABOVE ≈76.9 % OF ITS OWN POSITIONAL BUCKET HARD-KILLS THE NEXT BOOT — on an ordinary day, with no mistake by anyone.**
> 🔑 **NO LEVEL OF CAPITAL ESCAPES IT: both sides are fractions of the same base. Adding money does
> not help. The configured capacity EXCEEDS the survival ceiling BY CONSTRUCTION.**

**SLOT LADDER** *(each slot at the `0.10 × total` concentration cap = 33.3 % of the bucket)*:
**1 ✅** *(cannot kill it even tier-boosted)* · **2 ✅ at plain sizing but 🔴 KILLS if either is boosted
past `11.54 % of C₀`** *(`position_sizer.py:530` `tiered_qty = max(1, min(tiered_qty, raw_qty*2))` —
up to **2×**)* · **3 = `max_open_delivery_positions` = 100 % of the bucket = 🔴🔴 HARD_KILL.**
⇒ ⭐ **THE THIRD DELIVERY SLOT IS THE ONE THAT KILLS THE BOOT.**

⛔ **`₹2,357` IS NOT PROMOTED — a fixed rupee number would have been the next `₹4,200`.**
⚠️ **Quote WHICH BASE every time: `0.30 × C₁` is boot-day cash; `0.2308 × C₀` is buy-day cash.**
Same rule as [[tick1-threshold-base-mixup-09aug]].

**⚠️ TODAY WAS *NOT* THE CEILING CASE:** the book was `₹907.02` = **32 % of the 07-Aug bucket**, well
inside it. **Today died because CASH COLLAPSED (§④).** ⭐ **The incident is history; the ceiling is the
exposure and it needs no anomaly at all.**

---

## ③ ⛔ THE "PER-SYMBOL ALLOCATION" DOES NOT EXIST — AND THAT IS THE FINDING

**(P) at `645728d` there is NO rupee allocation, NO per-symbol budget and NO divisor.**
`position_sizer.py:290-294` picks `bucket="positional"` for DELIVERY and reads `avail =
snap.positional_avail`; `:419-428` `qty_by_capital = floor(avail / margin_per_share)`.

> 🔑 **A delivery trade is sized against THE WHOLE REMAINING BUCKET, capped per symbol only by
> concentration `0.10 × total`. `3 × 10 % = 30 %` is EXACTLY the bucket ⇒ 100 % fillable.**

⛔ **The recalled `~₹1,000/symbol` is REFUTED as a config value.**
⚠️ **And the memorised divisor `max_daily_trades` @`position_sizer.py:433` does NOT hold at this ref**
— `:433` is effect-telemetry inside the `constraint="RISK"` branch. **`M3`: line numbers hold ONLY at
their measured SHA.** ⛔ This does not refute [[stated-vs-configured-limits-09aug]] at *its* SHA; it
means **that note must not be applied to the deployed build.**

---

## ④ ✅ THE WEEKEND CASH DROP — **ANSWERED BY RAMA 10-Aug: THE SEBI QUARTERLY SETTLEMENT**

**Fri `18:36:34 net=8,983.58` → Mon `08:15:25 net=209.80` = `−₹8,773.78`, while Friday's TOTAL
realised P&L was `−₹4.26`.** Market shut throughout. *(Width: every `fm_ledger` row between the two
readings — `10295`, then today's INIT `10296`.)*
⇒ ⛔ **THE MONEY LEFT BY A PATH THE SYSTEM NEVER SAW — and that path is the broker returning unused
client funds to the bank.**

> ## 🗓️ **⛔ NOT A LOSS, ⛔ NOT A WITHDRAWAL, ⛔ NOT AN ERROR — A SCHEDULED, RECURRING SETTLEMENT. IT WILL KEEP ITS NEXT APPOINTMENT.**
> ⭐ **So "Monday-after HARD_KILL with any carried CNC" was never rare — it is a SCHEDULE, and it fires
> far BELOW the ceiling because it attacks the OTHER operand.** ⛔ **The conditional in the original
> note is now resolved: the antecedent HOLDS.**

✅ **PINNED BY TEST, ⛔ not by prose — `test_fix1_carried_position_rehydrate.py` case **A** (boot path,
carry established at 10,000, boot at 500) and case **H/H2** (the same sweep arriving at the 09:15
`sync_from_broker`, five depths down to ZERO cash). Both RED pre-fix.**
🔴 **BUT ONLY FOR DELIVERY — [[fix1-carried-position-accounting-10aug]] §⑨: the same sweep STILL kills
through the INTRADAY bucket, which Fix 1 left untouched on purpose.**

---

## ⑤ THE SYNC PATH — ⛔ THE CHECK PRECEDES ITS ONLY REPAIR BY AN HOUR

**`sync_from_broker` (`fund_manager.py:1380`, FM9) has EXACTLY ONE production caller: `main.py:1012`,
a one-shot thread that sleeps to 09:15 and fires ONCE** — and returns early logging *"started after
09:15, skipping re-sync"* if the service booted later. *(Width: `git grep sync_from_broker 645728d --
'*.py'`; every other hit is a test, comment or docstring.)*
⛔⛔ **THERE IS NO FREQUENT/PERIODIC SYNC — Rama's recollection does not match the deployed build.**

It sets `_total`, recomputes both bucket availables, writes a `SYNC` row, and calls `_check_invariant`
at `:1474` (H-1). ⛔ **It NEVER re-bases `reserved`/`used` — the SAME asymmetry as the boot's.**

> ## 🔴 **IT COULD NOT HAVE SAVED TODAY, STRUCTURALLY: the invariant runs at `08:15:25.680`, the sync at `09:15`, and the process was already dead.** ⭐ **The payin timing is irrelevant; the boot would still have died.**

⚠️⚠️ **THE CONTRADICTION — RECORDED, ⛔ NOT RESOLVED:** `sync_from_broker` **does** rebase `_total`
from live broker cash, and **`_total` IS the sizer's `total_capital`** (`position_sizer.py:293`) — the
base of risk 1 %, concentration 10 % and position-value 40 %. ⇒ 🔑 **THE MECHANISM RAMA REMEMBERS AS
PROTECTIVE IS THE DYNAMIC RE-SYNC THE SIZING SETTLEMENT FORBIDS** *("a won TGT must not restore the
basis and enlarge later orders")*. ⭐ **HONEST QUALIFICATION: it fires at 09:15 when realised P&L is
≈0, so in practice it captures OVERNIGHT/PAYIN moves, ⛔ not intraday wins** — the forbidden mechanism
is present; its once-daily timing means it is not currently the profit-restoration case.
[[capital-vocabulary]]

🔴 **SECOND INDEPENDENT FIRING SITE:** because `sync_from_broker` calls `_check_invariant`, the same
mismatch **WOULD** kill a **RUNNING, HEALTHY 09:15 session with the market open** if cash fell below
`reserved + used` between boot and 09:15. ⛔ **NOT OBSERVED — precondition stated with its tense.**

---

## ⑥ ⛔ WHAT MUST NOT BE CONCLUDED FROM TOMORROW

**The 08:15 cron mints a token → the watcher starts the service → `clear_stale_state` clears today's
HARD_KILL AS A PRIOR-DAY KILL** *(verified in today's own log, where Friday's 15:15 SOFT_KILL was
cleared exactly that way — [[killswitch-autoclear-prior-day]])* **→ at `₹10,209.80` the boot reads
`3,062.94 − 907.02 = +2,155.92` ⇒ IT PASSES.**

> ## ⛔⛔ **THAT IS NOT A REPAIR — IT IS THE SAME CODE MEETING A FRIENDLIER OPERAND. The system will look completely healthy and the defect will be invisible.**
> ⭐ **Any fix must hold in BOTH states — low cash with a carry AND high cash with a carry — and only
> the second is available tomorrow.** [[feedback-baseline-before-change-28jul]]

---

## ⑦ SCORING, GATE, AND WHAT WAS *NOT* TOUCHED

**E1-E7 SCORED** *(gate line 2 SATISFIED — `NOT TESTED` with a reason IS a score)*: **E1 ✅ · E6 ✅ ·
E2/E3a/E3b/E4/E5 ⚪ NOT TESTED** — 🔑 **`held` was NEVER COMPUTED**; the boot died before
`cnc_gtt.hydrated`, so B11-B15 never ran and ⛔ **none of E2's three falsifiers was observed.**
⭐⭐ **The frozen boot-stage trace did exactly its job** — it wrote in advance that *"11-12 present but
13-15 absent ⇒ E2 failing"*, and here **11-15 are ALL absent ⇒ THE BOOT failed, ⛔ NOT E2.**
⚠️ **The `get_positions` at `08:15:25.690` is the HARD_KILL flatten worker's, ⛔ not stage B11.**
⚠️ **E7 = `PASS on wording · VOID as a control`:** MANINFRA survived because the boot died before the
monitor and then **Q4 SPARED it** — ⛔ **a control that passes for a reason unrelated to what it
controls has measured nothing.**

✅ **Q4's delivery-spare FIRED LIVE FOR THE FIRST TIME** on byte-identical deployed `kill_switch.py`:
both CNC positions SPARED, `0` flattened ⇒ [[q4-hard-kill-delivery-30jul]] moves **BUILT → VERIFIED
LIVE.**

🏷️ **TWO TAUTOLOGICAL CHECKS, filed as TWO DIFFERENT defects** *(both [[tautological-check-class-05aug]])*:
`kite_funds_available` = threshold `0.0`, a **LIVENESS** check ⛔ not an adequacy one *(it COULD have
been red)* · `capital_deployment` = returns `_passed()` **UNCONDITIONALLY, NO PREDICATE AT ALL** — 🔴
**it printed `432.3 %` and PASSED.** ⭐ **A missing check leaves you uncertain; a tautological one
leaves you WRONGLY certain.** 🔑 **And `fund_manager_balance` caught it with `−697.22` (whole-account)
while the invariant used `−844.08` (positional bucket) — they differ by `146.86 = 0.70 × 209.80`,
EXACTLY the intraday bucket ⇒ two checks on ONE condition disagree by a whole bucket because they sit
on DIFFERENT BASES, and the preflight's is the MORE FORGIVING one.**

⛔ **`CONFIG_DIFF` REFUTED — ZERO hits** *(width: recursive over ALL of `logs/`, ALL dates in 30-day
retention, FOUR spellings, plus a whole-tree grep of files modified in 3 days)*; the only config event
was a normal `config_snapshotter` write ⇒ **`GO_NOGO` line 5 is an UNEXERCISED control, ⛔ not a
passing one.**

🚦🔴 **F6 = NO-GO 10-Aug; the calendar slips a day.** **Line 3 FAILS and it is decisive, ⛔ not a
technicality: F6's fix lives in `cnc_gtt_monitor`, and TODAY THE MONITOR NEVER EXECUTED** because the
capital invariant killed the boot ~60 s upstream ⇒ **deploying puts F6's first live execution behind a
gate that can prevent it from ever running.** **Line 6 FAILS as written** — `failed`/`ExecMainStatus=3`,
⛔ not `inactive`, ⛔ not Rama's manual stop. [[f6-delivery-exit-abs-defect-06aug]]

📌 **Rama manually deleted DIFFNKG's GTT `330944932` — ⛔ AN OPERATOR INTERVENTION, ⛔ NOT evidence
that boot recovery worked**, and **E5 can now never be settled from this instance.**
⚠️ **The row is STILL STRANDED** — `trd_010f8e21…` `OPEN` at `₹446.106`, no GTT ⇒ **tomorrow's boot
replays it again.**
🔴 **CORRECTED 10-Aug (later): the *"no holding"* half of this line was UNSOURCED and is now
withdrawn.** ⛔ **`get_holdings` was NEVER CALLED on 10-Aug** *(the monitor never ran — B11-B15 all
absent)*, and the `SPARED delivery position DIFFNKG (product=CNC, qty=1)` line that appeared to
support it is the **`site=local-pass`** emitter, which reads **`abs(trades.qty_filled)` from the DB**
— ⛔ **not the broker.** *(`kill_switch.py:1668-1691` vs the `site=broker-sweep` emitter at `:1853`,
whose wording is `broker product=CNC`.)* 🏷️ [[counts-db-rows-not-broker-06aug]] a THIRD time, this
time inside the evidence for a different incident. ⇒ **DIFFNKG's broker holdings/positions are
UNKNOWN.** [[diffnkg-prediction-11aug]] ⭐⭐ **This incident STRENGTHENS the case for F6 while F6 has just
been DEFERRED — a tension, ⛔ not resolved; and note the trap: *"deploy F6 sooner because of this"* is
exactly the pressure the gate exists to resist.**

---

🔒 **STATUS** *([[feedback-status-label-rule-27jul]])*: **VERIFIED LIVE** — the invariant firing, the
reconciliation, Q4's spare, the single-caller sync, both tautologies. **MEASURED @`645728d`** — every
config/source value. **PROJECTED** — the slot ladder *(arithmetic on measured operands, ⛔ not an
observed event)*. **DIAGNOSED — ⛔ NOT BUILT, NOT DEPLOYED.** Both tautological checks touch the
capital path ⇒ **CAREFUL LOOP.**
📄 **Record `docs/audit/RECURRENCE_CEILING_10-Aug-2026.md` · evidence `docs/audit/capture_10aug2026/`
(8 files, sha256 in §11).** ⚠️ **COPY FIDELITY is proven, ⛔ NOT a cross-session baseline.**
