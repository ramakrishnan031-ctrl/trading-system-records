# 🔴 THE RECURRENCE CEILING — 10-Aug-2026

**Written 10-Aug-2026, session resumed 11:19 IST** *(clock via PowerShell `Get-Date` =
`2026-08-10 11:19:17`, TZ `India Standard Time (UTC+05:30)`; ⚠️ Git Bash `TZ=Asia/Kolkata date`
double-converts on this box and reads 05:48 — **do not use it**).*

**⛔ READ-ONLY SESSION. Nothing on the VM was written, restarted, cleared or fixed. No push, no
merge, no deploy.** The service remains `failed` / `ExecMainStatus=3`; the token watcher is
measured as deliberately NOT restarting it. **Halted is the safe state.**

**Measured against the DEPLOYED ref `645728d` only** — ⛔ not local `main` (48 commits ahead),
⛔ not recall. The VM is not a git checkout, so deployed identity was established by **md5 of the
running files** against `git show 645728d:<file>`, not by SHA.

🧪 **PARITY: LIVE-ONLY throughout.** CNC settlement, broker cash, T+1 rollover. ⛔ **No paper
analogue exists and a paper drill of any of it would be vacuously green** — paper nets by *symbol*,
live Kite per *(symbol, product)*, and the paper adapter has no settlement model.

---

# §1 · 🔴 THE ANSWER RAMA NEEDS TODAY

> ## ⛔ **NO. At the deployed configuration, the delivery pipeline CANNOT fill its configured slots without hard-killing the following morning's boot.**

**And the finding that matters is not the rupee figure — it is that there isn't one:**

> ## ⭐⭐ **THE CEILING IS A RATIO, NOT AN AMOUNT. It is `0.2308 × C₀` on BOTH sides of the comparison, so NO level of capital escapes it. Adding money does not help. The configured capacity exceeds the survival ceiling BY CONSTRUCTION.**

| the two numbers, both fractions of the same base | value |
|---|---|
| what the delivery pipeline is **ALLOWED** to hold overnight *(the positional bucket, 100 % fillable)* | **`0.30 × C₀`** |
| what the **NEXT BOOT SURVIVES** | **`0.2308 × C₀`** |
| ⇒ **the trap** | 🔴 **the top `23.1 %` of the delivery bucket is unreachable without killing the next boot** |

**Stated the way an operator uses it:**

> ### 🔑 **THE BOOT DIES WHEN THE OVERNIGHT DELIVERY BOOK EXCEEDS ≈ 76.9 % OF THE POSITIONAL BUCKET IT WAS PERMITTED TO FILL.**

**The slot ladder** *(each slot at the 10 %-of-capital concentration cap = 33.3 % of the bucket)*:

| overnight delivery slots filled | book as % of `C₀` | book as % of the bucket | next 08:15 boot |
|---|---|---|---|
| 1 | 10 % | 33.3 % | ✅ survives — **and cannot kill it even at the tier-boosted maximum** |
| 2 | 20 % | 66.7 % | ✅ survives at plain concentration sizing — 🔴 **KILLS if either slot is tier-boosted past 11.54 % of `C₀`** |
| **3** *(= `max_open_delivery_positions`)* | **30 %** | **100 %** | 🔴🔴 **HARD_KILL — both books halted, on an ordinary day, with no mistake by anyone** |

⭐ **The third slot is the one that kills the boot.** ⚠️ **And two slots suffice whenever the tier ×
performance multiplier boosts either of them** — see §4.3, where that boost is measured at up to **2×**.

## §1.1 — ⛔ WHAT THIS IS *NOT*

🔴 **TODAY'S HARD_KILL WAS NOT THIS.** Today's book was **`₹907.02`** against a **07-Aug** basis of
`₹9,444.50` — **9.6 % of `C₀`, i.e. 32 % of the bucket, comfortably inside the ceiling.** Today died
because **cash collapsed over the weekend** (§3), not because the book was large.

> ⭐ **Both cases are the SAME defect at the SAME line.** The invariant compares a **re-measured**
> total against an **un-rebased** reservation replay. Either operand moving breaks it:
> **cash falling** *(today — happened)* or **the book rising** *(the ceiling — has not happened yet)*.
> 🔑 **The incident is history. The ceiling is the exposure, and it needs no anomaly at all.**

---

# §2 · THE MECHANISM — MEASURED, WITH ZERO RESIDUAL

## §2.1 — What actually executed, from the boot's own log

```
08:15:25.643  fund_manager.session_start
08:15:25.643  get_margins call_start
08:15:25.673  get_margins call_end        result_summary: "net=209.8"
08:15:25.676  fund_manager.initialize     intraday_avail=146.86  positional_avail=62.94  total=209.8
08:15:25.678  CRITICAL  Capital balance violation: NEGATIVE_MARGIN_AVAILABLE: -844.0800
08:15:25.680  HARD_KILL persisted
08:15:25.683  CRITICAL  capital_state_inconsistent   ← main.py:2469, rehydrate_from_open_trades
```

**The CRITICAL record's own fields, quoted:**

| field | value |
|---|---|
| `bucket` | **`positional`** |
| `cash_floor` | **`62.94`** |
| `margin_used` | **`907.02`** |
| `margin_reserved` | `0.0` |
| `margin_available` | **`-844.0799999999999`** |
| `realized_pnl_today` | `0.0` |
| `tolerance` | `1.0` |
| `delta` *(ledger identity residual)* | **`5.684341886080802e-14`** |

## §2.2 — The reconciliation, exact

```
positional bucket   =  0.30 × 209.80   =   62.94          ← config positional_bucket_pct
replayed reservation=  446.106 + 460.91632  =  907.02232  ← the two OPEN CNC trades
margin_available    =   62.94 − 907.02      = −844.08
```

⭐ **`−844.08` is the logged value to the paisa, and the ledger identity `avail + reserved + used ==
_total` closed at a residual of `5.68e-14`** — floating-point noise, nothing more.

> ## ⛔ **THAT IS THE MOST IMPORTANT LINE IN THIS DOCUMENT: THE LEDGER WAS NOT CORRUPT.**
> **Every rupee reconciles.** ⭐ **Only INV6's sign guard fired** — the arithmetic was right and the
> *comparison* was wrong. ⛔ **There is nothing to repair in the ledger, and treating this as data
> corruption would send the fix after the wrong component.**

## §2.3 — ⛔ THE EARLIER MECHANISM WAS WRONG; THIS ONE IS THE MEASURED ONE

> **REFUTED:** *"the invariant compares cash against a broker `margin_used` and double-counts."*
> **(width: `git grep` over the full deployed tree)** — ⛔ **there is no broker `margin_used` input
> anywhere in the path.**
>
> **MEASURED:** it is a **purely internal identity**. It breaks because **`_total` is RE-MEASURED
> across the settlement boundary while the reservation replay is NOT RE-BASED.**
> ⭐ **The money half of the hypothesis survived; the formula half did not.**

**The pivot, and the date it became reachable:** `leverage_map.DELIVERY: 1.0` means a delivery
reservation is the **FULL purchase value**, deducted as though it were a margin. Verified against
both open rows:

| trade | qty | entry | `margin_reserved` | qty × entry |
|---|---|---|---|---|
| DIFFNKG | 1 | `446.106` | **`446.106`** | `446.106` ✅ |
| MANINFRA | 4 | `115.22908` | **`460.91632`** | `460.91632` ✅ |

⭐ **05-Aug is the first day the operand existed** — before a delivery position could be carried
overnight, nothing was ever replayed into the positional bucket.

---

# §3 · THE CEILING, DERIVED FROM MEASURED VALUES

## §3.1 — The deployed configuration · ⛔ every value from `645728d`, none from memory

| key | value | location |
|---|---|---|
| `capital.positional_bucket_pct` | **`0.30`** | `config/system_config.yaml:145` |
| `capital.intraday_bucket_pct` | `0.70` | `:144` |
| `capital.conditional_allocation_enabled` | `false` *(⇒ the fixed split above is live)* | `:146` |
| `capital.leverage_map.DELIVERY` | **`1.0`** | `:157` |
| `delivery_enabled` | `true` | `:102` |
| `risk.max_open_delivery_positions` | **`3`** | `:205` |
| `risk.max_daily_delivery_trades` | `5` | `:206` |
| `position_sizing.max_concentration_pct` | **`0.10`** | `:169` |
| `position_sizing.risk_per_trade_pct` | `0.01` | `:167` |
| `position_sizing.max_position_value_pct` | `0.40` | `:178` |
| `position_sizing.max_multiplier` | **`2.0`** | *(tier × perf ceiling)* |
| `delivery_risk_per_trade_pct` / `delivery_max_position_value_pct` | **`null` / `null`** | `:190-191` |

> ## 🔴 **§2.1 OF THE CARD ASKED FOR "THE PER-SYMBOL ALLOCATION". IT DOES NOT EXIST — AND THAT IS THE FINDING.**
> ⛔ **The recalled `~₹1,000 per symbol` is NOT A CONFIG VALUE and is NOT PROMOTED HERE.**
> **(width: `grep` over every capital/sizing/risk/delivery key in the deployed `system_config.yaml`)**
> — there is **no rupee allocation, no per-symbol budget, and no divisor** in the deployed sizer.
>
> **What is actually there** (`capital/position_sizer.py:290-294`, `:419-428` @`645728d`):
> ```python
> bucket = "intraday" if intent in _INTRADAY_INTENTS else "positional"
> snap   = self._fm.get_snapshot()
> total_capital = snap.total
> avail  = snap.intraday_avail if bucket == "intraday" else snap.positional_avail
> ...
> qty_by_capital       = floor(avail / margin_per_share)
> qty_by_concentration = floor((total_capital * max_concentration_pct) / entry_price)
> raw_qty              = min(qty_by_risk, qty_by_capital, qty_by_concentration)
> ```
> ⇒ 🔑 **A delivery trade is sized against the WHOLE REMAINING POSITIONAL BUCKET, capped per symbol
> only by concentration (10 % of total capital). There is no fixed slice. The bucket is 100 %
> fillable across its 3 slots — `3 × 10 % = 30 %`, which is exactly the bucket.**
>
> ⚠️ **AND THE MEMORISED DIVISOR IS ALSO ABSENT AT THIS REF.** The note *"the sizing divisor is
> `max_daily_trades`, `position_sizer.py:433`"* does **not** hold at `645728d` — line 433 is
> effect-telemetry inside the `constraint = "RISK"` branch. **(`M3`: line numbers hold only at their
> measured SHA.)** ⛔ **This does not refute the note at the SHA where it was taken; it means the note
> must not be applied to the deployed build.**

## §3.2 — The formula · ⛔ stated in `C`, never as a rupee figure

**Let** `C₁` = broker net cash the boot reads · `D` = Σ `margin_reserved` of OPEN delivery trades ·
`p` = `positional_bucket_pct` = `0.30` · `τ` = invariant tolerance = `1.0`.

**① The boot survives iff:**

```
D  ≤  p × C₁ + τ                    →     D  ≤  0.30 × C₁ + 1.0
```

**② And `C₁` is not free — buying `D` of CNC debits the cash account:**

```
C₁  ≈  C₀ − D                        (C₀ = cash on the day the book was bought)
```

**③ Substituting gives the ceiling in the variable that the SIZER actually saw:**

```
D ≤ 0.30 × (C₀ − D) + 1
1.30 D ≤ 0.30 C₀ + 1
──────────────────────────────────────────────────────────
        D  ≤  (0.30 × C₀ + 1.0) / 1.30   ≈   0.2308 × C₀
──────────────────────────────────────────────────────────
```

**④ Against the bucket the sizer is allowed to fill — the operator-facing form:**

```
D_max_safe / bucket  =  0.2308 / 0.30  =  0.769
⇒  ANY overnight delivery book above ≈76.9 % of the positional bucket kills the next boot.
```

> ⭐ **Both `/1.30` and the plain `0.30 × C₁` are correct — they are the SAME rule in DIFFERENT
> BASES**, and conflating them is exactly the `%`-without-its-base error this campaign has already
> paid for once. **`0.30 × C₁` is measured against BOOT-DAY cash; `0.2308 × C₀` against the cash the
> book was BOUGHT from.** ⛔ Quote which one you mean, every time.

**⚠️ ASSUMPTIONS, STATED:** ② treats `C₁ = C₀ − D` exactly. In reality `C₁` also moves with intraday
realised P&L, brokerage and any cash movement — all small relative to `D` on an ordinary day, ⛔ but
**not** on a day like today (§5). The ratio result is unaffected; only the day's exact margin is.

## §3.3 — The formula reproduces BOTH observed cases

| case | `C₁` | bucket `0.30×C₁` | `D` | predicted | observed |
|---|---|---|---|---|---|
| **10-Aug actual** | `209.80` | `62.94` | `907.02` | 🔴 **KILL** (`−844.08`) | 🔴 **HARD_KILL, `−844.0800`** ✅ |
| counterfactual: Friday's cash had held | `8,983.58` | `2,695.07` | `907.02` | ✅ survive | *(not run — the cash did not hold)* |
| counterfactual: the ₹10 k payin had landed pre-boot | `10,209.80` | `3,062.94` | `907.02` | ✅ survive `+2,155.92` | *(not run — see §4)* |

⭐ **The model predicts the one case that happened, to the paisa, and explains why the same book was
harmless on Friday.** 🔑 **That is what makes the forward projection in §1 something other than
speculation.**

---

# §4 · §3 OF THE CARD — THE CAPITAL SYNC PATH

## §4.1 — `sync_from_broker`: when · what it reads · what it mutates

**(width: `git grep sync_from_broker 645728d -- '*.py'` — the complete tree.)**
**There is EXACTLY ONE production caller.** Every other hit is a test, a comment, or a docstring.

| question | measured answer |
|---|---|
| **when invoked** | `main.py:1012`, inside a one-shot thread that **sleeps until 09:15 IST and fires once**. Skipped on trading holidays. 🔑 **If the service starts AFTER 09:15 it logs `"started after 09:15, skipping re-sync"` and returns — it never runs at all.** |
| **how often** | 🔴 **ONCE PER DAY. ⛔ There is NO frequent or periodic sync in the deployed build** — Rama's recollection of *"sync at frequent period earlier"* does not match `645728d`. |
| **what it READS** | `broker_adapter.get_margins().net` — broker net cash. |
| **what it MUTATES** | `self._total = broker_balance`; recomputes `_intraday_avail` / `_positional_avail` as `pct × broker_balance − reserved − used`; writes a `SYNC` ledger row. |
| **what it does NOT touch** | 🔑 **`_intraday_reserved` · `_positional_reserved` · `_used`.** ⛔ **The reservations are NEVER re-based — which is the same asymmetry as the boot's.** |
| **would it have rebased after the payin?** | ✅ **YES — arithmetically.** `0.30 × 10,209.80 − 907.02 = +2,155.92`, and the invariant would have passed. |

## §4.2 — ⛔ BUT IT COULD NOT HAVE SAVED TODAY, AND THE REASON IS STRUCTURAL

> ## 🔴 **THE CHECK PRECEDES ITS ONLY REPAIR BY ONE HOUR.**
> **The invariant is evaluated at `rehydrate` — `08:15:25.680`. The sync that would rebase `_total`
> is at `09:15`.** The boot raised `CapitalStateInconsistent` at `main.py:2469` and the process
> exited **~60 minutes before the sync thread's deadline** — and in fact before that thread is ever
> started. ⛔ **No payin timing could have rescued this boot.** ⭐ **Say that plainly: the recollection
> does not apply here, and the boot would still have died.**

## §4.3 — ⚠️ THE PART WORTH SAYING OUT LOUD · ⛔ REPORTED, NOT RESOLVED

**`sync_from_broker` DOES rebase `_total` from live broker cash** — and `_total` is precisely what the
sizer reads as `total_capital` (`position_sizer.py:293`), the base of **risk 1 %**, **concentration
10 %** and **max-position-value 40 %**.

> ### 🔑 **THE MECHANISM RAMA REMEMBERS AS PROTECTIVE IS THE ONE THE SIZING SETTLEMENT FORBIDS.**
> The settlement: ***"a won TGT must not restore the basis and enlarge later orders."***
> ⛔ **DO NOT RESOLVE THIS TODAY. It is recorded as a live contradiction between two of Rama's own
> rulings, for him to settle.**

**⚠️ AND THE HONEST QUALIFICATION, so the contradiction is not overstated:** the sync fires **at
09:15**, when the day's realised P&L is still ≈ zero. In practice it captures **overnight and payin**
movements, ⛔ **not** intraday wins. **The mechanism the settlement forbids is present; its once-daily
timing means it is not currently the profit-restoration case.** ⭐ **Both halves matter — the first is
why it must be raised, the second is why it is not an emergency.**

## §4.4 — 🔴 A SECOND, INDEPENDENT FIRING SITE FOR THE SAME DEFECT

`sync_from_broker` calls `_check_invariant("sync_from_broker", …)` (the **H-1** change) and can itself
raise `CapitalInvariantViolation` → the same `HARD_KILL`.

> ⇒ **The same operand mismatch has TWO firing sites: `08:15` rehydrate and `09:15` sync.**
> ⚠️ **The second is arguably worse: it kills a RUNNING, HEALTHY session at 09:15, with live positions
> and the market open** — whereas the boot case merely refuses to start.
> **PRECONDITION, stated with its tense:** this **would** fire if broker cash fell below
> `reserved + used` on a bucket between the boot and 09:15. ⛔ **It has NOT been observed.**

---

# §5 · 🔴 THE WEEKEND CASH DROP — ⛔ ONLY RAMA CAN CLOSE THIS

| reading | value | source |
|---|---|---|
| Friday 07-Aug **18:36:34** `get_margins` | **`net = 8,983.58`** | `logs/system_2026-08-07.log` |
| Monday 10-Aug **08:15:25** `get_margins` | **`net = 209.80`** | `logs/system_2026-08-10.log` |
| **difference** | 🔴 **`−8,773.78`** | arithmetic |
| Friday's TOTAL realised P&L | **`−4.26`** *(`RESET_PNL`, ledger `10295`, 15:17:02)* | `fm_ledger` |

> ## ⛔ **TRADING CANNOT EXPLAIN IT, AND THE SYSTEM'S OWN LEDGER HAS NO RECORD OF IT.**
> The market was closed for the entire interval. **(width: every `fm_ledger` row between the two
> readings — the last is `10295` on Friday, the next is `10296`, today's INIT.)** ⇒ **the money left
> the account by a path the system never saw.**
>
> ### 🔑 **THE QUESTION FOR RAMA, AND IT IS THE ONE THAT DECIDES HOW URGENT ALL OF THIS IS:**
> **Was the `₹8,773.78` a broker sweep, a payout, or a withdrawal — and is it PERIODIC?**
>
> ⭐ **If it recurs (e.g. every weekend, or on settlement days), then "Monday-after HARD_KILL with any
> carried CNC" stops being a rare coincidence and becomes a SCHEDULE** — and it would fire far below
> the §1 ceiling, because it attacks the *other* operand.

---

# §6 · SCORING E1–E7 · ⛔ THREE STATES, NEVER TWO

**Scored against `MONDAY_10-Aug-2026_PREDICTION.md` §2.1 as frozen at `4cf6217`.**
⛔ **No prediction wording was edited.** ⭐ **`NOT TESTED` is a recorded outcome and satisfies gate
line 2; a BLANK does not.**

## §6.1 — 🔑 FIRST, THE BOOT-STAGE WALK — because it decides five of the seven rows

Walking the frozen `B0…B15` trace, the **first divergence localises the failure**:

| stage | expected | 10-Aug actual | verdict |
|---|---|---|---|
| B4–B8 | banner → kill-switch auto-clear → scenario | `08:15:12.752` → `.844`; Friday's `15:15 SOFT_KILL` **auto-cleared as prior-day** | ✅ |
| B9 | `run_all_startup_checks: OK` | `08:15:25.637`, `scenario=CRASH`, `warnings=[]` | ✅ |
| **B10a** | `fund_manager.session_start` | `08:15:25.643` | ✅ |
| **B10b** | 🔑 **`cnc_gtt.hydrated`** | 🔴 **ABSENT** | 🔴 **FIRST DIVERGENCE** |
| B11–B15 | `get_positions` → `get_holdings` → `forensic` → `delete_gtt` → `gtt_exit` | 🔴 **NONE emitted by the monitor** | 🔴 absent |

> ## ⭐⭐ **THE TRACE DID EXACTLY THE JOB IT WAS BUILT FOR.**
> §3.1b wrote in advance: *"stages 11-12 present but 13-15 absent ⇒ the monitor ran and chose NOT to
> act, which is E2 FAILING rather than the boot failing."* **Here stages 11-15 are ALL absent** ⇒
> 🔑 **the BOOT failed, ⛔ NOT E2.** **A flat set of red checks would have merged these two and scored
> five predictions red against a monitor that never executed.**
>
> ⚠️ **The `get_positions` call at `08:15:25.690` is NOT stage B11** — it is the `HARD_KILL` flatten
> worker's read (`"flatten worker finished — all 0 attempted position(s) flat"`). ⛔ **Do not score it
> as the monitor's.**

## §6.2 — THE SCORE SHEET

| # | prediction | 🔒 conf. | 🔒 width | **OUTCOME** | **PROVENANCE** | reason |
|---|---|---|---|---|---|---|
| **E1** | Friday stop ran ⇒ boot runs | CERTAIN | X3+ | ✅ **PASS** | PRE-EXISTING | Stop ran `18:36:44→48`; the 10-Aug boot **did** start (`08:15:12.752`). ⭐ Already resolved before Monday; recorded as measured. |
| **E2** | `held = 0` for DIFFNKG | HIGH | X2 | ⚪ **NOT TESTED** | — | 🔑 **`held` was NEVER COMPUTED.** The boot died at `08:15:25.680` in `rehydrate_from_open_trades`, before `cnc_gtt.hydrated`. ⛔ **None of E2's three falsifiers was observed.** |
| **E3a** | `forensic → delete_gtt → gtt_exit → CLOSED` | HIGH | X2 | ⚪ **NOT TESTED** | — | The sequence requires the monitor cycle. It never ran. |
| **E3b** | exit price from LTP, P&L overstated | MED-HIGH | X2 | ⚪ **NOT TESTED** | — | No exit occurred ⇒ no price was resolved. *(Its stated dependency — "E3a firing at all" — was not met.)* |
| **E4** | no 4th GTT (branch 2 `healthy`) | HIGH | X1 | ⚪ **NOT TESTED** | — | `_handle_row` was never entered; no branch was walked. ⛔ **The absence of a 4th GTT is NOT evidence for E4** — nothing could have created one. |
| **E5** | order on trigger — CANNOT DETERMINE | N/A | X1 | ⚪ **NOT TESTED** | — | `330944932` never triggered. ⚠️ **And it now never can: Rama deleted it manually (§7).** 🔑 **A/B/C/D remain unresolved and the venue invariant is still unmeasured.** |
| **E6** | stop leg reachable (−0.862 %) | CERTAIN | X1 | ✅ **PASS** | PRE-EXISTING | Arithmetic on Friday's quoted quote; true as written. ⛔ **Its Monday extension (did the level actually trade?) is NOT TESTED** — no Monday quote was captured. |
| **E7** | MANINFRA untouched *(NEGATIVE CONTROL)* | HIGH | X2 | ⚠️ **PASS on wording — VOID as a control** | PRE-EXISTING | See §6.3. |

## §6.3 — 🔴 E7 PASSED EVERY FALSIFIER, BY A MECHANISM IT DID NOT PREDICT

**MANINFRA was untouched**: GTT `330856765` still `ACTIVE`, trade row still `OPEN`, qty 4. **Scored
against the wording as written (§2.2's freeze): PASS.**

> ### ⛔ **BUT ITS PURPOSE WAS NOT SERVED, AND RECORDING THE PASS WITHOUT THAT WOULD BE THE MISLEADING OUTCOME.**
> E7 exists to demonstrate **the monitor's SELECTIVITY** — *"the boot did the RIGHT thing"* (§3.2b).
> **The monitor never ran.** MANINFRA survived because ① the boot died before the monitor, and then
> ② **`HARD_KILL`'s Q4 product filter SPARED it.**
>
> ```
> 08:15:25.689  CRITICAL kill_switch: SPARED delivery position DIFFNKG  (product=CNC, qty=1)
>                         — HARD_KILL flattens intraday only (Q4)
> 08:15:25.689  CRITICAL kill_switch: SPARED delivery position MANINFRA (product=CNC, qty=4)
> 08:15:25.732  CRITICAL kill_switch: flatten worker finished — all 0 attempted position(s) flat
> ```
>
> ⇒ 🔑 **A control that passes for a reason unrelated to what it controls has measured nothing.**
> ⭐ **Real selectivity WAS demonstrated — but by `kill_switch`, not `cnc_gtt_monitor`.** That is a
> genuine, valuable first (§6.4 · U2), and it belongs to a different component than E7's claim.

## §6.4 — 🆕 UNEXPECTED OBSERVATIONS · ⭐ THE ROWS NO PREDICTION COVERED

*(§2.1 requires these: "something true on Monday that no prediction covered is worth more than a
confirmed prediction, and it is the only way the set can be shown to be incomplete.")*

| # | observation | PROVENANCE | why it matters |
|---|---|---|---|
| **U1** | 🔴 **The boot HARD_KILLed on a CAPITAL invariant before the delivery monitor ran.** | **PRE-EXISTING**, *exposed* by MONDAY-BOOT | ⛔ **No prediction contemplated a capital-path failure at all.** ⭐ Applying §3.6's interpretation rule: the weekend state **EXPOSED a latent defect**; it did not create one. The defect has existed since delivery carry became possible (05-Aug). |
| **U2** | ✅ **Q4's delivery-spare fired LIVE for the first time**, on byte-identical deployed `kill_switch.py`. | PRE-EXISTING | 🔑 **The `HARD_KILL`-does-not-flatten-delivery ruling is now VERIFIED LIVE, not merely BUILT.** Both CNC positions were spared and `0` positions were flattened. |
| **U3** | 🔴 **`₹8,773.78` left the account over the weekend, unrecorded by the system.** | **UNKNOWN** — ⛔ must stay UNKNOWN until Rama answers | §5. Decides whether the Monday-kill is rare or scheduled. |
| **U4** | ⚠️ **`capital_deployment` preflight saw `432.3 %` deployed and returned PASS.** | PRE-EXISTING | §8. A tautological check. |
| **U5** | 🔴 **The recurrence ceiling** — a full delivery book kills the next boot at ANY capital level. | PRE-EXISTING *(latent)* | §1. ⭐ The finding with the longest reach; needs no anomaly to fire. |
| **U6** | ⚠️ **`CONFIG_DIFF` does not exist in the record.** | PRE-EXISTING | §9. Gate line 5 rests on an event that was never observed. |

---

# §7 · 📌 RAMA'S INTERVENTION, RECORDED CORRECTLY

> ## ⛔ **RAMA MANUALLY DELETED DIFFNKG'S GTT `330944932`. THAT IS AN OPERATOR INTERVENTION — ⛔ NOT EVIDENCE THAT BOOT RECOVERY WORKED.**
> ⭐ **E2 is NOT TESTED for the measured reason: the boot died at `08:15:25.680`, before the monitor
> ran a single cycle.** ⛔ **The GTT's absence must never be read as the system having cleaned it up.**

**⚠️ AND THE ROW IS STILL STRANDED, WHICH IS THE PART THAT CARRIES FORWARD:**

The DB carries `trd_010f8e21…` as **`OPEN`**, `margin_reserved = ₹446.106`, with **no holding at the
broker and now no GTT**. ⇒ 🔑 **Tomorrow's 08:15 boot replays that `₹446.106` again**, exactly as
today's did.

> ## ⭐⭐ **THIS INCIDENT STRENGTHENS THE CASE FOR F6 — AND F6'S DEPLOY HAS JUST BEEN DEFERRED.**
> **F6 is what closes that row.** Every additional day it stays open is another boot that replays a
> phantom `₹446.106` into the positional bucket, pushing the book **closer to §1's ceiling for a
> position that does not exist.**
> ⛔ **RECORDED AS A TENSION, NOT RESOLVED.** ⚠️ **And note the trap in it: the argument "deploy F6
> sooner because of this incident" is exactly the pressure the gate exists to resist.**

---

# §8 · THE TWO TAUTOLOGICAL CHECKS · 🏷️ FILED SEPARATELY, AS DIFFERENT DEFECTS

> ## ⭐⭐ **THE HEADLINE: THREE CAPITAL CHECKS RAN ON THE ONE MORNING IT MATTERED. TWO PASSED. ONE CAUGHT IT.**

| check | reading on 10-Aug | verdict |
|---|---|---|
| `kite_funds_available` | ✅ PASS | 🔴 threshold is **`0.0`** — a **LIVENESS** check, ⛔ not an adequacy one |
| `capital_deployment` | ✅ **PASS** — *"capital deployed **432.3 %** (margin_used ₹907 / total ₹210; pending ₹0)"* | 🔴 returns `_passed()` **unconditionally** — it **reports** a number and **never judges** it |
| `fund_manager_balance` | 🔴 **FAIL** — *"cash_floor <= 0 (−697.22; opening 209.80 − margin_used 907.02)"* | ✅ **the one that worked** |

## §8.1 — ⛔ THEY ARE TWO DIFFERENT DEFECTS AND MUST NOT BE FIXED AS ONE

| | `kite_funds_available` | `capital_deployment` |
|---|---|---|
| **defect** | a threshold set so low it cannot fail | **no threshold at all** |
| **class** | **`V5` — a check with no failing input** | **`V5` — a check with no PREDICATE** |
| **what a fix looks like** | choose an adequacy threshold *(and ⛔ **it must be capital-relative** — a rupee constant becomes the next `₹4,200`)* | decide **what deployment percentage is wrong**, then branch on it |
| ⭐ **the sharper one** | it *could* have been red | 🔴 **it could NEVER have been red** — it saw `432.3 %` and reported PASS |

> ### 🔑 **`capital_deployment` IS THE WORSE OF THE TWO, AND ITS OWN OUTPUT PROVES IT.**
> **It printed the exact number that names the incident — `432.3 %` — and passed.** ⭐ A MISSING check
> leaves you uncertain; **a tautological one leaves you WRONGLY certain**, and this one manufactured a
> green tick out of the single most damning figure available that morning.

## §8.2 — ⚠️ THE OBSERVATION THAT OUTLIVES BOTH

**`fund_manager_balance` used `−697.22` (`209.80 − 907.02`, the WHOLE-account view). The invariant
that actually fired used `−844.08` (`62.94 − 907.02`, the POSITIONAL-BUCKET view).**

> 🔑 **The difference is `146.86` — exactly `0.70 × 209.80`, the intraday bucket.** ⭐ **Two checks on
> the same condition disagree by a whole bucket because they are computed on DIFFERENT BASES.** ⚠️ The
> preflight's number is the more forgiving one; **had cash been between the two thresholds, preflight
> would have read GREEN on a book that still kills the boot.** ⛔ **Every capital figure must name
> which capital it means.**

---

# §9 · GATE LINE 5 — `CONFIG_DIFF` IS REFUTED

> ## ⛔ **THERE IS NO `CONFIG_DIFF` EVENT IN THE RECORD.**
> **WIDTH, stated in the same sentence as the zero:** recursive over **all** of `logs/`, **all** dates
> in the 30-day retention, **four spellings** of the token, plus a whole-tree grep over files modified
> in the last three days. **Result: ZERO hits.**
>
> **What DOES exist is a different event:** `config_snapshotter: wrote config snapshot id=29 for
> 2026-08-10 (hash=79932bde50fe)` — **a normal snapshot write**, and `config_drift ✅ PASS  risk caps
> OK (max_open=5, max_daily…)` on nine occasions, all passing.
>
> ⇒ ⚠️ **`GO_NOGO` line 5 should not carry weight it has not earned.** ⭐ The line itself is sound —
> *"this build changes neither, so any drift is unexplained and blocks"* — ⛔ **but no drift-detection
> event has ever been observed to fire**, so it is currently an unexercised control, not a passing one.

---

# §10 · 🚦 **F6 = NO-GO, 10-Aug-2026**

> ## ⛔⛔ **DEFERRED. THE CALENDAR SLIPS A DAY. FIRST-LIVE MOVES FROM TUE 11-Aug TO THE NEXT CLEARED EVENING.**

## §10.1 — The failing lines, named exactly

| # | line | state | why |
|---|---|---|---|
| **3** | *No safety-critical finding invalidating an F6 assumption* | 🔴 **NO-GO** | **§1's ceiling and §2's operand mismatch are safety-critical and land directly on F6's reachability.** See §10.2 — this is the decisive one. |
| **6** | *The service is DOWN — **RAMA'S manual stop** — `ActiveState=inactive`* | 🔴 **NO-GO as written** | The service is **`failed` / `ExecMainStatus=3`**, ⛔ not `inactive`, and ⛔ not from a manual stop. ⚠️ **The line's PURPOSE (nothing running when `checkout -f` lands) is met** — but its stated condition is not, and **the reason it is down is an unresolved capital defect**, which is a stronger reason to defer, not a weaker one. |
| **2** | *E1–E7 SCORED* | ✅ **satisfied by §6** | Each row now carries a recorded outcome; five are `NOT TESTED` **with reasons**. |
| **5** | *No config or schema drift* | ⚠️ **unexercised** | §9 — no drift event exists in the record; the schema-version comparison was **not run today**. |
| **7** | *Before-snapshot taken, hashed, FROZEN* | ⚪ **not taken** | ⚠️ **And the subject has MOVED**: DIFFNKG's GTT was deleted by Rama today (§7), so any deploy-time snapshot now describes a different state than the authorisation contemplated. |
| **10** | *Evening cron chain finished* | ⚪ **not reached** | It is `11:19`. ⛔ **And the chain cannot complete normally — the service is down, so `18:15 forward_shadow_record` has no running system to record from.** |

## §10.2 — 🔑 WHY LINE 3 IS THE DECISIVE ONE, AND IT IS NOT A TECHNICALITY

> ## ⭐⭐ **F6'S FIX LIVES IN `cnc_gtt_monitor`. TODAY THE MONITOR NEVER EXECUTED — THE CAPITAL INVARIANT KILLED THE BOOT ~60 SECONDS UPSTREAM OF IT.**
> **F6 is built on the assumption that a carried delivery position is resolved AT THE NEXT BOOT.**
> §1 establishes a condition under which **the next boot never gets that far**, and today is the
> measured proof that the condition is reachable.
>
> ⇒ 🔑 **Deploying F6 tonight would put its first live execution behind a gate that can prevent it
> from ever running — and the first-live observation would then be uninterpretable**, which is
> precisely what gate line 8 exists to protect.
> ⭐ **F6 is not wrong, and this does not weaken it. It means F6's validation depends on a boot that
> survives, and that dependency was invisible until today.**

## §10.3 — ⛔ WHAT MUST NOT BE CONCLUDED FROM TOMORROW

> ## 🔴 **TOMORROW MORNING THE SYSTEM WILL LOOK COMPLETELY HEALTHY, AND THAT IS NOT A REPAIR.**
> **The mechanism, measured:** the 08:15 cron mints a token → `token_watcher` starts the service →
> `clear_stale_state` auto-clears today's `HARD_KILL` **as a prior-day kill** *(⚠️ the auto-clear
> matches on prior-DATE and ignores open positions — verified in today's own log, where Friday's
> `15:15 SOFT_KILL` was cleared exactly this way)* → the boot reads the **post-payin** cash.
>
> **If cash is `₹10,209.80`: `0.30 × 10,209.80 − 907.02 = +2,155.92` ⇒ IT PASSES.**
>
> ⛔ **A passing boot tomorrow is NOT evidence of repair. It is the SAME code meeting a FRIENDLIER
> OPERAND.** ⭐ **Any fix must be shown to hold in BOTH states — low cash with a carry, AND high cash
> with a carry** — and only the second of those will be available tomorrow.

---

# §11 · EVIDENCE — PRESERVED AND HASHED

**⛔ The capture was taken read-only during the incident and has NOT been re-read against the live
source since.** It was written to a session-temp directory and **copied byte-for-byte into the
repository at `11:19` on 10-Aug**; all eight `sha256` values were verified identical across the copy.

`docs/audit/capture_10aug2026/`

```
e16256798432c374bb0e81bd98a499c469c67ce70cbaa1832d8d12e77f207874  A_db_capture.txt
0f6afa700fe0e36b19f2603854e9da5eabe4875b3a98684669b66c885202b4d5  B_orders_pnl.txt
5bb10850edc5790135529545954bafdcb8f628750b812cbc279bc33ad05149b6  C_orders_logs.txt
679b31018b834a9e7bdf9623214be9d450c5ce7e7f700fdc3469a96983271b03  D_boot_logs.txt
769ab3e7cfb4f1e92fb92fd11625d36ad0923172c79a44ad4279cd0eafca5028  E_fulllog_configdiff.txt
44a0799896ea6355e2bbe93b074fa17fa3d911a704acdb7348856b2598ae3345  F_watcher_configdiff.txt
4fe189a40eeaa7526731a6b4663e3fda2d567cc8a0e16ed79aa1edcc00e3b069  G_configdrift_preflight.txt
4074550825ce33579c1b5c07c21a4f05039bd039cc40992b873e861bf14f0f8e  H_preflightB.txt
```

⚠️ **PROVENANCE, STATED HONESTLY:** the original hash list printed during the capture is **not in the
resumed session's context**. **What is verified is COPY FIDELITY** — source and destination hash
identically, and the files' mtimes (`10:35`–`10:40`) are unchanged and consistent with the capture
run. ⛔ **This is NOT the same as a cross-session baseline confirmation, and it is not claimed as one.**

**Deployed-source identity** — the four VM pulls md5-matched `645728d`; the files themselves are not
re-committed because `git show 645728d:<path>` regenerates them exactly:

```
3dab7020cb5d61b32163d1aca5f8a94c  capital/fund_manager.py
807da52ef284f20337819d1d25ec5405  capital/invariant.py
6cff0ce80b613f9378b850f4f8d58c5c  main.py
f8a28eb99500b900049293957091b847  capital/position_sizer.py
```

---

# §12 · WHAT IS OWED, AND BY WHOM

## §12.1 — ⛔ RAMA — the one that gates everything else

> ## 🔴 **WHAT WAS THE `₹8,773.78` THAT LEFT THE ACCOUNT OVER THE WEEKEND — SWEEP, PAYOUT OR WITHDRAWAL — AND IS IT PERIODIC?**
> ⭐ **Until this is answered, the frequency of the whole failure class is unknown.** A one-off makes
> today rare; a schedule makes it recurring **and independent of §1's ceiling.**

**Also for Rama, ⛔ not to be resolved without him:**
- **§4.3's contradiction** — `sync_from_broker` rebases the sizing basis from live broker cash. Two of
  his own rulings disagree.
- **§10** — F6 is `NO-GO`; the first-live date moves. ⭐ **The deploy window recurs every evening; the
  first-live observation does not.**

## §12.2 — ⚪ STILL OPEN, ⛔ NOT ATTEMPTED TODAY *(prohibited by the card)*

| item | state |
|---|---|
| the invariant / the ceiling | **DIAGNOSED — ⛔ NOT BUILT, NOT DEPLOYED.** No fix was designed or attempted. |
| the two tautological checks (§8) | **FILED — ⛔ NOT BUILT.** ⚠️ Both touch the capital path ⇒ **CAREFUL LOOP** (design → review → implement). |
| `trd_010f8e21…` (DIFFNKG) stranded `OPEN` | **UNTOUCHED, deliberately.** ⛔ Not hand-closed. Replays `₹446.106` at every boot until F6 lands. |
| MANINFRA GTT `330856765` | **UNTOUCHED, deliberately.** Still `ACTIVE`, still correct. |
| E5's venue invariant (A/B/C/D) | 🔴 **STILL UNMEASURED, and this instance can no longer supply it** (§7). Needs the next triggered GTT meeting a zero holding. |
| the ₹2,357 figure | ⛔ **NOT PROMOTED.** §3.2 replaces it with a ratio, deliberately — ⭐ **a fixed rupee number would have been the next `₹4,200`.** |
| the `~₹1,000 per symbol` allocation | ⛔ **REFUTED as a config value** (§3.1). It does not exist in the deployed build. |

---

> # 🔒 STATUS LABELS, APPLIED
> **VERIFIED LIVE:** the invariant firing · the reconciliation · Q4's delivery-spare (U2) · the
> single-caller sync path · the two tautological checks' behaviour.
> **MEASURED (config/source at `645728d`):** every value in §3.1 · the ceiling derivation.
> **PROJECTED:** §1's slot ladder — ⚠️ **arithmetic on measured operands, ⛔ NOT an observed event.**
> **NOT TESTED:** E2 · E3a · E3b · E4 · E5.
> **DEFERRED:** F6 · every fix named above.
> ⛔ **The word "fixed" does not appear in this document about anything.**
