# PREDICTION — TICK 2, PIPELINE-SCOPED DAILY GATE (INSTALL ⑥)

**Written:** 2026-08-17, frozen at **20:42 IST**, ⛔ **BEFORE the push.**
**Unit:** `08b462ba175d904e8723ed34a13c956f0dd33679`, branch `fix/tick2-refit-17aug`.
**Frozen against base:** `origin/main` = `f62db55d3bb60eabf674ba1867c4f9c3fc8fab86`,
measured at extraction time two independent ways (VM bare `rev-parse` + PC `ls-remote`).
**Push slot:** Tuesday 18-Aug evening. **First execution: the WED 19-Aug 08:15 boot.**

⚠️ **BASE-STALENESS CLAUSE, STATED IN ADVANCE.** This prediction is frozen against
`f62db55`. **If `origin/main` moves before the push, this prediction's base is stale and
it MUST be re-frozen** — ⛔ do not push against a prediction written for a different
base. Tuesday's Gate C re-measures `origin/main`, and that measurement, ⛔ not this line,
is the authority.

## §A — WHAT IS BEING INSTALLED, AND WHAT IT IS NOT

Two commits **extracted** onto `f62db55` — ⛔ **not** a rebase of
`fix/tick2-pipeline-scoped-daily-gate`, because that branch carries **`c39e799` (F6)** in
its ancestry, and F6 is NO-GO. Old to new:
`0337378` to **`5ece1ef08116d069e272d819687ce429702737cd`** ·
`43f73b1` to **`08b462ba175d904e8723ed34a13c956f0dd33679`**.

**THREE files** (⛔ not four — `43f73b1` modifies the same test file `0337378` creates):
`core/state_store.py` · `signals/signal_processor.py` ·
`tests/unit/test_tick2_pipeline_scoped_daily_gate.py`.

**CONTENT PROVEN UNCHANGED, BOTH WAYS:** `range-diff` prints `=` on both rows;
base-independent `patch-id` **IDENTICAL** (`7ed0a767…`, `66cd028c…`); net-diff md5
**index-stripped identical** (`0f91ff0673a44c4f217f858f28b63990`). ⛔ The RAW net-diff md5
DIFFERS (`f4447652…` vs `db22158b…`) and byte-identity is **NOT** claimed: the old base
`f963438` carries F6's +114 in `core/state_store.py` and `f62db55` does not, so the
`index <old>..<new>` blob lines must differ. **ANCESTRY CLEAN:** `c39e799`, `9fdfe41`,
`4f91784`, `071169b`, `bfd6b5f`, `43f73b1` — every `merge-base --is-ancestor` **FALSE**.
0 merge commits; 0 behind / 2 ahead of `f62db55`.

**WHAT IT CHANGES:** gate 1 (one completed trade per symbol+direction per day) becomes
**per-pipeline**. Gate 3 (one simultaneous OPEN position per symbol, account-wide) is
**UNCHANGED**. Product is derived from `orders.product` via `LEFT JOIN … leg='ENTRY'`;
**no schema change**. The join is **fail-closed**: a trade whose product cannot be
resolved counts for BOTH pipelines, i.e. exactly today's behaviour.

**PRECONDITION MEASURED LIVE:** `one_trade_per_symbol_direction_per_day: **true**`
(deployed `config/system_config.yaml:224`). ⇒ the gate is enabled and this code path WILL
execute. ⛔ Had it been false, Tick 2 would be inert by config and this prediction void.

## §B — THE PRESENCE SIGNATURE, AND ITS CONTROL

🔑 Tick 2 rewrote gate 1's reject text, where `book = pipeline or "account-wide"`:

```
OLD: "{sym} {dir} already traded today ({n} executed trade(s)); one completed
      trade per symbol+direction per day"
NEW: "{sym} {dir} already traded today in the {book} book ({n} executed trade(s));
      one completed trade per symbol+direction per day, per pipeline"
```

**PRESENCE TOKEN: `, per pipeline`.** **CONTROL MEASURED BEFORE IT CAN FIRE, ON TWO
INDEPENDENT CHANNELS:**

| token | deployed `*.py` | every VM log | `signals.rejection_reason`, ALL TIME |
|---|---|---|---|
| `, per pipeline` | **0** | **0** | **0** |
| `in the intraday book` | **0** | **0** | **0** |
| `in the delivery book` | **0** | **0** | **0** |
| `in the account-wide book` | **0** | **0** | **0** |

⭐ **AND THE CHANNEL IS PROVEN LIVE, so a future absence is meaningful rather than
vacuous:** the OLD text is present in BOTH channels today at exactly matching counts —
**22 rejects on 17-Aug and 163 all-time**, by log grep AND by SQL independently.

## §C — 🔑 THE INERT-VS-WORKING DISCRIMINATOR

`_pipeline_for_intent` wraps its import in `try/except Exception: pass → return None`,
which scopes the gate account-wide. **A broken import therefore makes Tick 2 silently
inert with no alarm** — configured, deployed, and doing nothing, which is the exact
failure class this campaign keeps finding. This prediction separates the two states:

| observed `{book}` token | verdict |
|---|---|
| `in the intraday book` **or** `in the delivery book` | ✅ **PIPELINE-SCOPED AND WORKING** — import resolved, intent matched |
| **only** `in the account-wide book` | 🔴 **DEPLOYED BUT INERT** — `_pipeline_for_intent` returned `None` |
| `, per pipeline` absent while rejects exist | 🔴 **THE NEW CODE IS NOT RUNNING AT ALL** |

**THE DISCRIMINATOR IS SHARP, AND THAT RESTS ON MEASUREMENT, ⛔ not assumption:** all
**16** deployed strategy YAMLs declare an intent (13 `INTRADAY`, 3 `DELIVERY`), **zero**
lack one; `strategies/schema.py:59` types it **`intent: str`** with a `field_validator`
(`:152-157`) that REJECTS anything but `INTRADAY`/`DELIVERY`; **no Enum exists anywhere**;
and both literals are members of `_INTRADAY_INTENTS` / `_POSITIONAL_INTENTS` at `f62db55`
(`capital/fund_manager.py:100-101`). ⇒ **for a real production signal, `account-wide`
cannot be legitimate.** ⭐ Corroboration, verified rather than accepted from a docstring:
`fund_manager.py:2338-2340` shows `reserve()` branching on the SAME two frozensets with
the SAME `in` comparison — the gate and the money path share one decision procedure.
⭐ The suite's `intent="DELIVERY"` is therefore the SAME type production passes, so the
tests are **not vacuous** on this point.

## §D — FALSIFIERS, each independently scoreable

| # | FIRES IF | source |
|---|---|---|
| **T1** | after the push `origin/main` ≠ `08b462b…` on either independent measure | VM `rev-parse` + PC `ls-remote` |
| **T2** | any of the 3 files differs PC vs VM by md5 | `md5sum`, PC side from the REF'S BLOBS |
| **T3** | the VM deployed tree shows tracked drift vs the new HEAD | `git --git-dir=… --work-tree=… status --porcelain` |
| **T4** | the 19-Aug 08:15 boot fails to reach `active`, or exits non-zero | `systemctl show` |
| **T5** | the 19-Aug boot logs `ImportError`/`ModuleNotFoundError` naming `capital.fund_manager` or `signals.signal_processor` | `logs/system_2026-08-19.log` |
| **T6** | gate-1 rejects EXIST on 19-Aug **and none** contains `, per pipeline` | log + `signals.rejection_reason` |
| **T7** | rejects contain `, per pipeline` **but every one** says `account-wide` | ⇒ **DEPLOYED BUT INERT** |
| **T8** | any of the four tokens appears **before** the 19-Aug 08:15 boot | ⇒ §B's ceiling was wrong |

**SCORING RULE FOR T6/T7, FIXED IN ADVANCE.** Let **R** = gate-1 rejects on 19-Aug.
**R = 0 ⇒ T6 and T7 are `NOT TESTED`** — ⛔ never a pass. **R > 0 ⇒** T6/T7 score exactly
as the table states. ⚠️ **R = 0 is a live possibility, ⛔ not a formality:** measured
gate-1 rejects per trading day — 06-Aug 19 · 07-Aug 10 · **10-Aug 0** · 11-Aug 11 ·
12-Aug 43 · 13-Aug 18 · 14-Aug 4 · 17-Aug 22 ⇒ non-zero on **7 of 8**, but 10-Aug proves
zero happens.

**CORROBORATION, ⛔ NOT A TEST — the behaviour delta.** On 17-Aug's real data, **5 of 13
distinct (symbol, strategy) reject groups were CROSS-PIPELINE**, and gate 1 would no
longer block them: GKSL/`positional_sector_rotation` (DELIVERY vs MIS) ·
MAXESTATES/`positional_sector_rotation` · MAXESTATES/`positional_swing_long` ·
SHANTIGOLD/`gap_go_long` (INTRADAY vs CNC) · SHANTIGOLD/`vwap_bounce_long`. ⇒ the change
is **REACHABLE on ordinary days**, ⛔ not theoretical. ⚠️ **"Gate 1 would allow" is ⛔ NOT
"a trade would have happened"** — gate 3 is unchanged and would still block while the
position is OPEN. ⛔ And the per-group counts behind that finding are **JOIN-INFLATED**
(they sum to 39 against a true 22); the structure is used, ⛔ never those numbers.

## §E — THE CEILING, STATED IN ADVANCE

**`NOT TESTED` and `CANNOT DETERMINE` are declared available up front**, and will be used
rather than a soft pass.

- ⛔ **`VERIFIED LIVE` is NOT available on push night.** T1-T3 are deploy-time only.
- **T4-T8 cannot be scored before the 19-Aug 08:15 boot.**
- ⛔ **Even a fully green T6 does NOT prove the SQL is correct.** It proves the pipeline
  resolved and the new message emitted. Whether `COUNT(DISTINCT t.trade_id)` and the
  `LEFT JOIN` return the right number on **production** data is NOT established here; the
  local suite covers it, production does not.
- ⚠️ **HISTORICAL PIPELINE RESOLVABILITY IS UNMEASURED ON THE VM.** The fail-closed
  branch triggers when a trade has no ENTRY order row, and the rate at which that occurs
  across production history has never been measured. ⛔ An open measurement, ⛔ not a
  blocker — the join fails CLOSED, i.e. toward today's stricter behaviour.
- 🧪 **PARITY: paper CAN exercise this one, and that is worth stating plainly** — it is a
  DB-predicate gate, ⛔ not a broker path. ⛔ This is the exception, not the rule: most of
  this system's paths cannot be rehearsed in paper, and that is recorded elsewhere.

## §F — THE GATE THAT PRECEDED THIS FREEZE

Fresh throwaway worktrees at `f62db55` and `08b462b`, both with the gitignored
`config/instruments.csv` copied in; system Python **3.11.9**, pytest **9.0.3**; ⛔ no venv
exists anywhere, confirmed by `pyvenv.cfg` search, ⛔ not by testing for a directory.

**RAW rc read from pytest itself, ⛔ not from a pipeline tail:** `RAW_PYTEST_RC=1` on
**both** sides. Base **10 failed / 5,626 passed / 4 skipped** (902.14 s); unit **10 failed
/ 5,643 passed / 4 skipped** (881.88 s). **`comm` BOTH directions: 0 NEW, 0 disappeared,
10 common — and 10/10 with IDENTICAL failure messages**, which is the load-bearing half,
since same ID is not same cause. **0 failures in any Tick-2 file.**

**NON-VACUITY PROVEN, ⛔ not asserted:** collected **5,640 → 5,657 = +17**, and the Tick-2
file contributes **exactly 17** tests while being **absent** at the base. Targeted run of
that file alone: **17 passed, `RAW_PYTEST_RC=0`.**

⭐ Wording, deliberately: **full clean-worktree regression completed; rc=1 both sides; all
failures independently attributed; no Tick-2-specific failure found.** ⛔ Not "clean",
⛔ not "set-identical". ⛔ No config value was changed to make anything pass.

⛔ **WHAT THIS PREDICTION DOES NOT CLAIM.** It does not claim Ruling 2 is fully
implemented — gate 3 is untouched by design. It makes no claim about any file outside the
three. It does not claim reversibility of EFFECT: the code reverts to `f62db55`, but an
entry admitted because gate 1 relaxed is a produced effect that a revert does not undo.

<!-- FROZEN-BOUNDARY — everything ABOVE this line is FROZEN. ⛔ No edit above it, especially if a call turns out wrong. Addenda go BELOW, appended only, each with its own timestamp. -->

## ADDENDA (append-only, below the boundary)


## ADDENDUM 1 — **THE PREMISE MOVED: TOMORROW'S BOOT IS NO LONGER CLEAN.**
Added **18-Aug-2026 19:4x IST (measured on the VM, read-only)**, ⛔ BEFORE the push (D1),
⛔ before any result exists. ⭐ Same placement and purpose as F7 in
`PREDICTION_fix1_boot_12-Aug-2026.md`: the frozen calls above are **unchanged**; what
changed is the STARTING STATE they will be scored against.

### THE CHANGED STARTING STATE, MEASURED
This prediction was frozen 17-Aug against an expected-clean book. It is not clean:

| Fact | Measured |
|---|---|
| A phantom **OPEN** trade row | `trd_433569141d0b41c8a449c98c5281ac6c` · **UTTAMSUGAR** · qty 1 @ 294.60 · entered `10:07:30.531942` · `updated_at 10:07:30.564902` (33 ms after entry — ⛔ nothing wrote to it all day) |
| Broker reality | all six positions **qty 0** (Rama's broker screens, ~19:00) |
| Capital still committed | **RESERVE ₹309.329601** `10:07:15.649` + **COMMIT ₹294.60** `10:07:30.532`, bucket **positional** — ⛔ **no RELEASE/RELEASE_USED, ever** (widest search: whole `fm_ledger`, all time, on `trade_id` AND `signal_id` AND `reason`) |
| Positional bucket | `balance_after` **₹2,901.41** at `14:49:53` (last positional row, MMFL's release) |
| Local vs broker GTT | `gtt_state` `332269938` **ACTIVE**, last verified **15:20:17**; broker OCO **TRIGGERED 15:25:25**, SL leg exchange-rejected (*"Insufficient stock holding … Holding quantity: 0"*), target **DORMANT** |
| Root cause | `orders/order_reconciler.py:665-672` — the CNC GTT monitor runs **ONLY within market hours**; MMFL was verified at **14:34:25** and finalised, UTTAMSUGAR's next cycle was due **~15:35** and the gate returned |
| The service | **operator-stopped 19:20:39** (`systemd[1]: Stopping…`), ⛔ NOT `eod_self_exit` — which re-checks forever and would never have exited, because `count_active_positions()` counts the phantom |

### WHAT IT DOES TO SCORING — falsifier by falsifier
⭐ **T1 · T2 · T3 · T5 · T8 — UNAFFECTED.** These are about code identity, file md5s,
deployed-tree drift, import failure and pre-boot token appearance. None reads a trade row,
a capital bucket or a GTT. Score them exactly as frozen.

🔴 **T4 — AT RISK FROM A NON-TICK-2 CAUSE. THIS IS THE ATTRIBUTION HAZARD.**
T4 fires if the 19-Aug 08:15 boot fails to reach `active` or exits non-zero. The boot now
starts with a phantom OPEN row and ₹294.60 committed against zero shares. ⇒ **If T4 fires,
it MUST NOT be scored against Tick 2 without first excluding tonight's stranded state.**
⭐ The discriminator is already available: T5's `ImportError` naming
`signals.signal_processor` / `capital.fund_manager` is Tick-2-attributable; a boot-time
invariant or capital violation naming UTTAMSUGAR, the positional bucket or the GTT is not.
⛔ **T4 alone cannot distinguish them. If both are present, the honest score is CANNOT
DETERMINE, ⛔ not a Tick 2 failure.**

🔴 **T6 / T7 — THE REAL RISK IS *NO SAMPLE*, ⛔ NOT A WRONG ANSWER.**
⭐ Gate 1 is **date-scoped** (`SUBSTR(t.created_at,1,10) = ?`), so the phantom — created
**18-Aug** — is **excluded from gate 1's count on 19-Aug**. Gate 1's arithmetic is therefore
NOT corrupted by it, and T6/T7 remain meaningful *if they get a sample*.
⛔ **But `count_active_positions()` is NOT date-scoped** —
`SELECT COUNT(*) FROM trades WHERE status IN ('OPEN','PARTIAL','PENDING_FILL')` — so it
returns **1** at tomorrow's boot (measured tonight). Against the deployed
`max_open_positions: 5` that is **one of five concurrent slots, 20% of portfolio capacity,
consumed by a position that does not exist**, plus **₹294.60** unavailable in the positional
bucket. ⇒ **Fewer entries admitted ⇒ fewer gate-1 evaluations ⇒ T6/T7 may produce ZERO
rejects to inspect.**
⛔ **A zero-sample day scores `NOT TESTED`. It is ⛔ NEVER a pass and ⛔ never a refutation** —
the same rule §B's ceiling already states for absence.

### WHAT THIS ADDENDUM DOES NOT DO
⛔ It does not change any call above the boundary. ⛔ It does not claim the stranded row will
or will not clear at boot (`clear_stale_state` is on the **kill switch**, ⛔ not on trades —
nothing measured tonight clears an OPEN trade row). ⛔ It does not license installing or
skipping anything: the install decision is Rama's and was taken on the semantic check that
**Tick 2 does not touch `count_active_positions()` — zero occurrences in the entire diff.**

## ADDENDUM 2 — **`N18-16` SCORED: `NOT SCORED` — ITS OWN PRE-REGISTERED CONFOUND FIRED.**
Added **19-Aug-2026 ~09:30 IST**. All figures measured read-only on the VM
(`~/systems/trading-system`, service PID `4022378`, booted `08:15:29 IST`) from the running
service's own logs and a `sqlite3 -readonly` DB read. ⛔ **Nothing was run, cancelled,
released or repaired to bring any of this about.** ⛔ No edit above the boundary.

### A · THE FOUR CONSEQUENCES, SCORED SEPARATELY — ⛔ NOT ROUNDED TO "CLEARED"
All four occurred, and all four at **`08:15:39`**, ⛔ **at the boot — not at the first
in-hours cycle.**

| # | predicted consequence | outcome | measured artifact |
|---|---|---|---|
| ① | row → terminal status | ✅ **OCCURRED** | `trades.status` `OPEN` → **`CLOSED`**; `exit_time 2026-08-19T08:15:39.578028+05:30`; `exit_reason=GTT_EXIT`; `exit_price 290.32`; `net_pnl −5.03` |
| ② | `RELEASE`/`RELEASE_USED` of **₹294.60** to **positional** | ✅ **OCCURRED** | `fm_ledger` `ledger_id 10825` · `RELEASE_USED −294.60` · bucket `positional` · `balance_before 3186.81` → `balance_after 3476.38` · ts `08:15:39.575333` · `trade_id` set · `pnl_delta −5.03` · `costs 0.75` |
| ③ | `gtt_state 332269938` off **`ACTIVE`** | ✅ **OCCURRED** | → **`CLEANED`**, `updated_at 08:15:39.580719` |
| ④ | `count_active_positions()` → **0** | ✅ **OCCURRED** | trades in `OPEN\|PARTIAL\|PENDING_FILL\|EXITING` = **0**; `ACTIVE` rows in `gtt_state` = **0** |

### B · 🔑 THE VERDICT IS `NOT SCORED`, AND THE PREDICTION ITSELF SAYS SO
`N18-16` carries, verbatim: ***"CONFOUND NAMED IN ADVANCE: the 08:15 boot itself may clear
or alter the row by another path; if it does, ⛔ this prediction is NOT scored against the
CNC monitor."*** ⭐ **That is exactly what happened.** The clear came from the **synchronous
startup path**, `orders/order_reconciler.py:424-426` — `self._cnc_gtt_monitor.reconcile()`
called with **no `in_hours` argument** — logged as `Startup reconciliation: 1 action(s)
taken` at `08:15:39.394`, with `cnc_gtt_monitor.gtt_exit` at `08:15:39.583`. That is
**57 minutes before market open**. The predicted trigger — *"the first `reconcile_once()`
poll after `market_is_open()` turns true, ~09:15"* — **never had anything to act on**: the
in-hours cycle did run (`get_holdings` at `09:15:08.136`) and the single hydrated row
(`cnc_gtt.hydrated count=1`) was already `CLEANED`.

⇒ **`NOT SCORED` (confound fired, as pre-registered).** ⛔ Not a pass. ⛔ Not a refutation
of the K6 mechanism either — the K6 branch *did* execute and *did* do all four things.

### C · ⛔ THIS CORRECTS `N18-16`'s OWN CLOSING CLAIM, AND `N18-10`'s SCOPE
`N18-16` states *"no such path is currently known."* **One is now known and measured:**

| path | file:line | market-hours gated? |
|---|---|---|
| **startup**, synchronous | `orders/order_reconciler.py:424-426` | ⛔ **NO — ungated.** This is the path that fired |
| **15 s poll**, `_maybe_run_cnc_monitor` | `orders/order_reconciler.py:658-670` — `if not in_hours: return` | ✅ YES. **This, and only this, is the gate `N18-10` named** |
| the K6 **finalise** branch itself | `orders/cnc_gtt_monitor.py:106-110`, `:526` | ⛔ **NOT conditioned on `in_hours`** — only the re-protect / re-create actions at `:514` are |

⇒ 🔑 **The fifteen-minute window explains why 18-Aug did NOT clear it. It does ⛔ NOT
explain the clear — any boot clears it out of hours, and always would have.**
⭐ **Corollary, and it inverts the intuition: the operator stop at 19:20:39 on 18-Aug
*accelerated* the clear by ~57 minutes.** Had the service stayed up overnight, the poll
path's gate would have held the row until ~09:15 today.

### D · 🔴 TWO FACTS OUTSIDE THE FOUR CONSEQUENCES — ⛔ THE FALSIFIER IS NOT MET, AND THE QUESTION IS NOT CLOSED
`N18-16`'s falsifier (row still `OPEN` / ₹294.60 still unreleased / `gtt_state` still
`ACTIVE`) is **NOT met**. ⛔ But it does not follow that the reconciliation path is sound.

🔴 **(F1) THE RELEASE IS NOT CORROBORATED BY THE BROKER'S CASH.** `G3 CAPITAL_DRIFT`, twice:

| measured at | `expected` (system) | `actual` (broker net) | `delta` | tolerance |
|---|---|---|---|---|
| `08:15:38.701` — pre-release | 10,917.30 | **10,622.70** | **294.60** | 50.00 |
| `08:45:40.089` — post-release | 10,912.27 | **10,622.70** | **289.57** | 50.00 |

The broker's net is **₹10,622.70 on every `get_margins` from `08:15:38.476` through
`09:18:39.758`** — it has not moved. `289.57 = 294.60 − 5.03`. ⭐ **Had the share sold at
290.32, ~₹289.57 of proceeds should have appeared in the broker's net. It did not.**
Tier `LOG_ONLY`, non-escalating ⇒ it cannot kill, but the condition is **LIVE**.

🔴 **(F2) THERE IS NO EXECUTION BEHIND THE EXIT PRICE.** `_resolve_exit_price`
(`cnc_gtt_monitor.py:674-694`) tries broker `get_trades()` matching the exit side **first**,
then LTP, then the entry proxy. `get_quote` fired at `08:15:39.559` — **reachable only if
the trades loop yielded no matching SELL.** ⇒ **`290.32` is a pre-open LTP (18-Aug's close),
⛔ NOT an execution price.** Corroborating: the `orders` table holds **exactly one leg** for
this trade — `ENTRY / BUY / LIMIT / CNC`, broker id `260818170302734` — and **no SELL leg at
all**. ⭐ Same shape as the DIFFNKG finding of 11-Aug (`get_quote` fired, `get_trades()`
produced nothing) — ⚠️ **a recurrence, not a novelty.**

### E · WHAT IS, AND IS NOT, DETERMINED ABOUT THE SHARE
✅ **DETERMINED (search width stated):** `get_holdings()` returned **`0 holdings`** at
`08:15:39.471` **and** at `09:15:08.136` (in-hours, post-open) — and
`broker/zerodha_adapter.py:955` computes `total = quantity + t1_quantity`, so a **T+1
delivery share WOULD have been counted**. `get_positions()` returned **`0 positions`** at
`08:15:38.616`, `:39.443`, `:39.514` and `08:15:40.289`. `position_reconciliation` **id 18**
(18-Aug `15:45:02.186905`) already recorded **`broker_qty=0 / system_qty=1 /
MISSING_AT_BROKER`**, `resolved_at` NULL.
⛔ **NOT DETERMINED — and I will not manufacture a verdict:** *why the broker's cash still
carries the ₹294.60 while the broker reports no shares.* The two readings — *"the share is
genuinely gone"* and *"we released capital against something still owed"* — are **not
separated by any artifact I hold.** ⭐ **I did not call the broker myself; every figure above
is the running service's own logged read.**

### F · ⛔ A CORRECTION TO MY OWN R1, MADE BEFORE IT COULD PROPAGATE
In R1 I wrote that the K6 *"holding FLAT"* leg *"cannot go red"* and called it the `V5`
tautological shape. **That is WRONG.** `_gather` (`cnc_gtt_monitor.py:432-465`) unions
`get_holdings()` with **same-day CNC rows from `get_positions()`**, and `get_positions()`
demonstrably carried CNC rows on 18-Aug (`1 positions` / `2 positions` from `10:00:39`).
**The probe has a failing input available; it is NOT tautological.** ⭐ The `0 holdings`
constancy I cited is explained by the union's *other* term, not by a dead probe.

### WHAT THIS ADDENDUM DOES NOT DO
⛔ It does not change any call above the boundary. ⛔ It does not score Tick 2 — that is
`§4` and is kept **separate**. ⛔ It does not claim the trade was correctly or incorrectly
closed; it records that the close is **uncorroborated by the broker's cash** and says which
single measurement would separate the readings. ⛔ It licenses no fix, no DB edit, no
capital action, and none was taken.

## ADDENDUM 3 — **A FROZEN SETTLEMENT PREDICTION (⛔ NOT A FINDING), + TWO MECHANISM ROWS.**
Added **19-Aug-2026 ~10:10 IST**, ⛔ **BEFORE the 11:30 measurement it will be scored on.**
⭐ Rama's instruction was to add this at 11:30; I froze it at 10:10 instead **because a
prediction written after its first measurement is not frozen** — the 11:30 leg would have
been scored against a number already in hand. The 11:30 and 15:20 measurements happen
exactly as instructed. Origin of ① and ②: **Rama, 19-Aug ~09:5x, quoted below.**

### ① 🔮🧊 FROZEN PREDICTION — **THE ₹289.57 IS PROBABLY UNSETTLED, ⛔ NOT MISSING**
**Rama's words, verbatim:** *"The ₹289.57 is probably not missing — it is probably
unsettled. UTTAMSUGAR was bought AND sold on 18-Aug in CNC, and India settles T+1, so the
proceeds are due to credit today. ⛔ Do not call it a discrepancy yet."*

⭐ **HIS PREMISE IS BETTER SUPPORTED THAN MY OWN AGNOSTIC FRAMING, AND I SAY SO PLAINLY.**
In ADDENDUM 2 §E I left *"the share is genuinely gone"* and *"we released capital against
something still owed"* as unseparated. **The bought-and-sold-same-day reading explains the
one leg my framing could not:** `get_holdings()` returns `0` while
`zerodha_adapter.py:955` sums `quantity + t1_quantity` — a share bought 18-Aug and **never
sold** would have to appear there as `t1_quantity=1`, and it does not. Corroborating:
`position_reconciliation` id 18 recorded `broker_qty=0` at **18-Aug 15:45:02**, so the
position had already left the broker's book *before* that read. ⇒ **something closed it on
18-Aug between 10:07 and 15:45**, and cash-still-debited + holdings-zero is exactly what an
unsettled same-day round trip looks like.

**THE CALL:** the ₹289.57 credits by settlement, and the drift closes on its own.
**THE FALSIFIER, single and unambiguous:** ⛔ **if the broker's net has NOT moved to
≈₹10,912 by tomorrow's 08:15 boot, the shortfall is REAL** and the release in ADDENDUM 2 §D
(F1) stands as an uncorroborated capital event.
**SCORING SCHEDULE:** `11:30` today · `15:20` today · **`08:15` 20-Aug = the decisive leg.**
⭐ `NOT TESTED` if the service is down at a checkpoint. ⛔ Never a pass.

🔴 **CONFOUND NAMED IN ADVANCE — ⛔ WITHOUT THIS THE PREDICTION IS UNSCOREABLE.** The broker
net is **no longer a clean instrument**: at `10:00:25.944` it moved **10,622.70 →
10,515.33**, and that drop is **exactly ₹107.37** = `fm_ledger 10832` `COMMIT 107.37`
(DHAMPURSUG qty 3 @ 178.95, **MIS/intraday**). ⇒ **every later reading must have concurrent
live margin subtracted before it is compared to ≈₹10,912.** ⛔ **A raw net below ₹10,912 is
NOT evidence against settlement** while an intraday position is open. ⭐ The clean read is
after today's MIS positions are flat — which is why **the 20-Aug 08:15 leg is the decisive
one** and today's two are indicative only.

⚠️ **ALSO CONFOUNDING, MEASURED:** `fm_ledger 10826` — a **`SYNC` at `09:15:00.034`**,
`+5.03` to `both`, *"broker sync: 10912.27 -> 10917.30"*. The system moved its **own
expectation back UP** by the realised loss, so `expected` is ₹10,917.30 again. ⇒ the next
`G3` delta will read ≈₹401.97 (`294.60 + 107.37`), ⛔ **not** ₹289.57. **Do not read that
growth as the shortfall widening** — it is the SYNC plus the new entry. ⛔ I have not
established why a broker sync raised the expectation rather than lowering it to the broker's
figure; that is **NOT DETERMINED** and is not part of this prediction.

### ② 🔑 MECHANISM ROW — **EVERY BOOT-TIME CLEAR WRITES A FABRICATED EXIT PRICE, ⛔ NECESSARILY — NOT OCCASIONALLY**
**Rama's words, verbatim:** *"the startup path runs BEFORE market open by construction, so
`get_trades()` can never find a matching SELL, so `_resolve_exit_price` always falls through
to LTP. ⇒ Every boot-time clear writes a fabricated exit price, necessarily — not
occasionally. ⭐ That is the DIFFNKG mechanism made systematic."*

✅ **CONFIRMED — and the mechanism is STRONGER than the pre-open argument, so I am recording
the stronger form.** `broker/zerodha_adapter.py:1760-1772` — `get_trades()` returns
***today's*** executed trades from Kite's `trades()` API. It is **day-scoped**. A boot-time
clear is, by definition, clearing a row **stranded from a PRIOR session**. ⇒ **the matching
SELL is on a previous day and can never be in `get_trades()`'s result set — irrespective of
market hours.** `_resolve_exit_price` (`cnc_gtt_monitor.py:674-694`) therefore falls to LTP
**100 % of the time on this path, by construction.**

⭐ The pre-open argument then **compounds** it rather than causing it: the 08:15 boot reads
LTP before the first tick, so the fabricated price is **the prior day's close**. Measured
today: `290.32`, written as `exit_price` with `exit_reason=GTT_EXIT`.

⛔ **AND THE ERROR HAS NO PREDICTABLE SIGN** — it is not conservative. On 11-Aug DIFFNKG the
same fallback produced `exit_price 395.55` against an SL trigger of `437.20`, making
`net_pnl −51.63` **too UNFAVOURABLE**. ⇒ ⛔ **never assume the fabricated price errs safe.**

🔑 **WHY THIS IS WORSE THAN EITHER FACT ALONE:** ADDENDUM 2 §C established that the boot path
is the **only** ungated route to K6 finalise. This row establishes that **that same route
can never price its own exit from an execution.** ⇒ the only mechanism that reliably clears
a stranded delivery row is also the one that **guarantees** the P&L it books is invented.
⛔ **RECORDED, ⛔ NOT FIXED** — no change proposed, designed or made.

**PRECISION, so the row does not overreach:** *"before market open"* holds for the
**scheduled 08:15 boot**, which is the observed case both today and on 11-Aug. The token
watcher's window is `[08:00,16:00)` and the unit carries `Restart=on-failure`, so an
**in-hours** boot is possible and unobserved. ⛔ It would not rescue the price anyway — the
day-scoping above is what forces the fallback, and it holds at any hour.

### ③ ⭐ THE BOUNDED EXPOSURE — **THE REASSURING HALF, AND IT IS REAL**
**Rama's words, verbatim:** *"a stranded row can only persist from the last in-hours cycle
to the next boot — never longer."*

✅ **HOLDS, with one widening and one narrowing, both measured:**
- **NARROWING (better than stated):** the **next boot is not the only exit.** The in-hours
  poll (`order_reconciler.py:658-670`) drains on the **FIRST in-hours cycle** —
  `first = not self._cnc_first_in_hours_done` — so the bound is *"last in-hours cycle of day
  D → **whichever comes first** of the next boot or ~09:15 on day D+1."* Today the boot won
  by ~57 min.
- **WIDENING (⛔ do not drop it):** *"day D+1"* means the next **TRADING** day. A Friday
  15:20 strand runs to **Monday**, and a long weekend longer. ⚠️ And if the service is never
  stopped, `deploy/token_watcher.sh:139-141` means **no boot occurs at all** — the bound then
  rests **entirely** on the ~09:15 in-hours cycle.

⇒ ⭐ **the exposure is one session-gap, ⛔ not unbounded** — the phantom could not have
survived into a second trading session undetected. ⛔ It does **not** bound the §D(F1)
capital question, which is about correctness of the clear, ⛔ not its latency.

### PROVENANCE + PROHIBITIONS
📌 Broker balance **₹10,622.70** independently stated by **Rama at ~09:58 IST** — ⭐ it
matches the service's own `get_margins` reads exactly, from `08:15:38.476` to
`09:59:55.664`, and the **first** departure is the ₹107.37 entry at `10:00:25.944`.
⛔ Nothing above was run, cancelled, released, repaired or fixed. ⛔ No DB edit, no GTT
action, no manual cron, no push. ⛔ No edit above the boundary.

## ADDENDUM 4 — **① SCORED `REFUTED` BY THE CONTRACT NOTE. THE DRIFT IS SYSTEM-SIDE OVER-COUNT.**
Added **19-Aug-2026 ~11:25 IST**. ⭐ **Scored against a PRIMARY DOCUMENT the system never
had:** `18-08-2026-contract-notes_LFL836.pdf` (Zerodha, LFL836), read directly — ⛔ not
inferred, ⛔ not relayed. Refutation raised by **Rama, 19-Aug ~11:0x**. ⛔ Nothing was run,
adjusted, released or repaired; ⛔ `fm_ledger` untouched; ⛔ the drift untouched.

### A · 🔴 ① IS **REFUTED**. ⛔ THE DRIFT WILL NOT CLOSE BY SETTLEMENT.
ADDENDUM 3 ① called the ₹289.57 *"probably unsettled, not missing"*, falsifiable at
tomorrow's 08:15. **It did not survive to that leg.** The contract note settles it now:

| contract note, measured | value |
|---|---|
| Pay in/Pay out obligation | **₹14.92** |
| less levies (brokerage 1.66 · txn 0.17 · GST 0.33 · STT 1.00 · SEBI 0.01) | **₹3.17** |
| **Net amount receivable by client** | **₹11.75** |
| UTTAMSUGAR net obligation for ISIN `INE786F01031` | **−₹4.68** |

⇒ **₹11.75 was the entire sum in transit, and Rama confirms settlement `2026155` credited it
on 18-Aug (closing ₹10,622.71).** ⛔ **Nothing of ₹294.60's order was ever pending.**
🏷️ **VERDICT: `REFUTED` — ⛔ not "awaiting the decisive leg". The 15:20 and 20-Aug 08:15 legs
are CANCELLED; they would measure a quantity now known not to exist.**

### B · 🔑 THE MEASUREMENT RAMA ASKED FOR — **THE CASH BASIS DEBITED *AND* WAS CREDITED BACK, AND THE SYSTEM SAW BOTH**
The question was whether the expected-cash basis ever debited the buy. It did — **and the far
more important half is that the broker returned it, in view, and nothing consumed the fact.**
From the service's own `get_margins` reads on 18-Aug:

| time (IST) | broker net | event |
|---|---|---|
| `08:15:40.662` | 10,611.00 | `fm_ledger 10742` INIT |
| `10:07:13.298` | 9,681.11 | before the UTTAMSUGAR buy |
| `10:07:28.424` | 9,387.50 | **Δ −293.61 — the buy** (fill `10:07:29`, note trade `602111852`) |
| `15:22:03.782` | 10,316.40 | before the sell |
| **`15:22:18.904`** | **10,611.00** | 🔑 **Δ +294.60 — THE SELL, TO THE PAISA** (note trade `608618503`, `15:22:18`) |
| `19:20:26.863` | 10,611.00 | flat to the operator stop |

⭐ **The system polled that figure every ~15 s for FOUR HOURS after the exit** — ~950 reads —
and never associated the +294.60 with the open trade row. ⛔ **The evidence of its own exit
was in its own hands the entire time.**

**Then the invention, at today's boot:**

| ts | event | total | vs broker 10,622.70 |
|---|---|---|---|
| `08:15:38.479` | `INIT broker_balance=10622.7` | 10,622.70 | ✅ **correct** (= 10,611.00 + the ₹11.75 credit) |
| `08:15:38.484` | `rehydrate_carry positional_carry=294.6` | **10,917.30** | ⛔ **+294.60 OVERSTATED** |
| `08:15:39.575` | `RELEASE_USED −294.60` | 10,912.27 | ⛔ +289.57 overstated |
| `09:15:00.034` | `SYNC +5.03` *"10912.27 -> 10917.30"* | **10,917.30** | ⛔ +294.60 — **moved AWAY from the broker** |

🔑 **`rehydrate_carry`'s stated premise — *"margin already removed from broker net by the
broker; re-added to the bucket base so it is not deducted twice"* — was TRUE on 18-Aug
between `10:07:28` and `15:22:18`, and FALSE from `15:22:18.904` onward. It was evaluated at
`08:15:38` on 19-Aug, roughly SEVENTEEN HOURS after it stopped being true.**

⇒ ⛔ **THE DRIFT IS ENTIRELY SYSTEM-SIDE OVER-COUNT. ⛔ Nothing is in transit. ⛔ It will not
close.** ⚠️ **AND THE DIRECTION IS THE UNSAFE ONE: the system believes it holds ₹294.60 MORE
than it does** — the over-allocation direction, ⛔ not the conservative one. ⭐ The 09:15
`SYNC`, the one scheduled opportunity to reconcile against the broker, **increased** the
error rather than closing it. ⛔ **Why it moves away from the broker's figure is NOT
DETERMINED and is not chased here.**

### C · ✅ THE OTHER FIVE DO **NOT** SHOW IT — AND THE REASON IS STRUCTURAL, ⛔ NOT LUCK
All six 18-Aug filled trades, system-booked exit vs the contract note:

| symbol | product | exit legs in `orders` | system exit | contract note | match |
|---|---|---|---|---|---|
| MAWANASUG | MIS | `SL:COMPLETE TGT:CANCELLED` | 128.14 | 128.14 | ✅ |
| INDSWFTLAB | MIS | `SL:CANCELLED TGT:COMPLETE` | 340.98 | 340.98 | ✅ |
| ICIL | MIS | `SL:CANCELLED TGT:COMPLETE` | 434.50 | 434.50 | ✅ |
| AEQUS | MIS | `SL:COMPLETE TGT:CANCELLED` | 259.25 | 259.25 | ✅ |
| **MMFL** | **CNC** | **0** | 684.20 | 684.20 | ✅ |
| **UTTAMSUGAR** | **CNC** | **0** | **290.32** | **290.10** | ❌ **−0.22** |

⭐ **THE SPLIT IS BY PRODUCT AND BY TIMING, AND BOTH TERMS ARE NECESSARY:**
- The **four MIS** trades **own their exit legs** — `order_monitor` learns the fill from its
  own order row. ⇒ **no inference is ever required**, so no price can be fabricated.
- The **two CNC** trades have **ZERO exit legs** — the OCO lives at the broker — so both must
  infer via `_resolve_exit_price`.
- 🔑 **MMFL IS THE CONTROL, AND IT IS THE MOST VALUABLE ROW HERE:** same code, same absent
  legs, finalised **in-hours, same day** (`14:49:53`, seven minutes after its `14:42:48`
  execution) ⇒ day-scoped `get_trades()` still held the SELL ⇒ **684.20, exact.**
- **UTTAMSUGAR is the only trade that crossed a day boundary** ⇒ `get_trades()` could not
  contain a prior-day SELL ⇒ LTP fallback ⇒ **290.32** = 18-Aug's close.

⇒ ⭐⭐ **THIS NARROWS ADDENDUM 3 ② FROM A PROPERTY OF THE BOOT PATH TO A NAMED, BOUNDED
POPULATION:** ⛔ **a DELIVERY (CNC/GTT) trade whose exit is not detected before the LAST
in-hours monitor cycle of its own day.** ⛔ An intraday trade cannot reach it — it carries its
own monitored exit legs. ⭐ ADDENDUM 3 ② is **not weakened** — every boot-time clear still
fabricates, necessarily — but **only delivery trades can ever reach a boot-time clear**, and
that is a much smaller and nameable exposure than the row implied.

### D · ⛔ TWO CORRECTIONS TO MY OWN RECORD, BOTH MATERIAL
1. 🔴 **ADDENDUM 2 §D(F2): *"no SELL leg exists at all"* — TRUE of the `orders` table, ⛔ FALSE
   of reality.** The sell executed: note trade **`608618503`**, `15:22:18`, qty 1 @ **₹290.10**,
   order **`1300000076754550`**. ⭐ **I stated a table's contents as though they were the
   world's** — the exact error the campaign's *"counts its own DB rows where it means the
   broker's reality"* row already names, committed while writing about that very defect.
2. 🔴 **THE WINDOW WAS NEVER FIFTEEN MINUTES.** `N18-10` and ADDENDUM 2 §C carried
   *"UTTAMSUGAR's next cycle was due ~15:35"*. **The last in-hours cycle ran `15:20:17` and
   the sell executed `15:22:18` — TWO MINUTES later.** The GTT SL then triggered `15:25:25`
   against a position already gone, which is the whole of *"Insufficient stock holding …
   Holding quantity: 0"*. ⇒ **the miss margin was ~2 minutes, ⛔ not ~15.**

### E · ⚠️ THE ₹0.22 HIDES THE MORE USEFUL NUMBER — AND THE SIGN CAME FROM THE CHARGES
| quantity | system booked | contract note | error |
|---|---|---|---|
| exit price | 290.32 | **290.10** | **+0.22 (favourable)** |
| net P&L | **−5.03** | **−4.68** | **−0.35 (UNfavourable)** |
| implied costs | 0.75 | 0.18 (brokerage 0.0884+0.0870) | **+0.57 over-charged** |

⇒ ⛔ **The two errors do NOT cancel, and the SIGN of the net error was set by the COST MODEL,
not by the fabricated price.** ⭐ Same lesson as 11-Aug DIFFNKG, reached by a different route:
⛔ **never assume a fabricated exit errs safe, and never reason about the P&L error from the
price error alone.**

### F · WHAT THIS ADDENDUM DOES NOT DO
⛔ No fix, no design, no `fm_ledger` adjustment, no capital release, no drift suppression, no
GTT action, no DB edit, no push. ⛔ It does not propose how `rehydrate_carry` should decide a
carry is live — that is a capital-path change and belongs in the careful loop. ⛔ It does not
re-open Tick 2, which remains scored separately. ⛔ No edit above the boundary.

## ADDENDUM 5 — **THE EXPOSURE QUANTIFIED · A FROZEN END-PREDICTION · AND THREE DEFECTS KEPT APART.**
Added **19-Aug-2026 ~10:45 IST** (VM clock), ⛔ **BEFORE the 11:30 checkpoint.** Raised by
**Rama, 19-Aug ~10:4x**. ⛔ Nothing fixed, ⛔ no SYNC run, ⛔ no ledger edit, ⛔ no push.

### ① 💰 TODAY'S LIVE COST — MEASURED, WITH EVERY BASE STATED
**System state, from the running process's own log** (`fund_manager.sync_from_broker`,
`09:15:00.037`): `broker_cash=10622.7 · carry=294.6 · new_total=10917.30`.
**Base for every cap below is `total_capital` = FundManager `_total`** — confirmed in code,
⛔ not inferred: `position_sizer.py:424` `total_capital * self._max_concentration_pct` ·
`:585` `eff_max_position_value_pct * total_capital` · `fund_manager.py:1347`
`self._daily_loss_limit_pct * self._total`.

| quantity | system-computed | on TRUE broker net 10,622.70 | overstated by |
|---|---|---|---|
| total capital | **10,917.30** | 10,622.70 | **+294.60 = +2.7734 %** |
| concentration ceiling (`0.10 ×`) | **1,091.73** | 1,062.27 | **+29.46** |
| position-value cap (`0.40 ×`) | **4,366.92** | 4,249.08 | **+117.84** |
| risk per trade (`0.01 ×`) | **109.17** | 106.23 | **+2.95** |
| daily-loss limit (`0.03 ×`) | **327.52** | 318.68 | **+8.85** |

🔑 **THE HEADLINE NUMBER IS NOT 2.77 % — IT IS 9.24 %, AND IT IS CONCENTRATED IN ONE BUCKET.**
`_bucket_base` (`fund_manager.py:2331-2335`) adds a carry to **its own** bucket, ⛔ not
pro-rata. With a *phantom* carry the entire error therefore lands in one place:

| bucket | system base | true base | error |
|---|---|---|---|
| intraday (`0.70 × cash + intraday_carry`) | **7,435.89** | 7,435.89 | ✅ **0.00 % — exactly right** |
| positional (`0.30 × cash + 294.60`) | **3,481.41** | 3,186.81 | 🔴 **+294.60 = +9.2444 %** |

⭐ Corroborated live: `fm_ledger 10922` (`10:13:23`) shows positional `balance_after`
**3,481.41** with nothing reserved or used — the inflated base, ⛔ not a derivation of mine.

⚠️ **AND WHAT IT HAS ACTUALLY COST TODAY, SO FAR: NOTHING — ⛔ WHICH IS NOT THE SAME AS "NO
EXPOSURE".** Reported honestly in both directions:
- **All four fills today are MIS**, sized off the intraday bucket — the bucket with **zero**
  error. ⛔ No delivery entry has filled; **every** delivery attempt was `entry_throttled`
  (MAWANASUG ₹554.88, UTTAMSUGAR ₹317.51, `10:00:27`–`10:00:31`).
- ⭐ **The per-trade allocation IS the concentration cap here** — `max_daily_trades: 10` and
  `max_concentration_pct: 0.10` make `capital/10` and `0.10 × capital` **the same number**.
  At today's prices the inflation does **not** change a single integer share count:
  MAWANASUG delivery @132.115 → `1091.73/132.115 = 8.26 → 8` vs `1062.27/132.115 = 8.04 → 8`;
  UTTAMSUGAR delivery @302.394 → `3.61 → 3` vs `3.51 → 3`. **Same qty either way.**
- Every filled position today is far inside both ceilings — DHAMPURSUG `3×178.95 = 536.85`,
  MAWANASUG `4×131.24 = 524.96`, PATELRMART `2×237.29 = 474.58`, against a true ceiling of
  1,062.27. ⇒ **~2× headroom; the ₹29.46 could not bind.**
⇒ 🏷️ **`EXPOSURE LIVE · HARM NOT YET REALISED TODAY`.** ⛔ Do not read that as benign: the
direction is **unsafe** (the system believes it has more than it has), the **daily-loss halt
sits ₹8.85 too far away**, and the moment a delivery entry clears the throttle it will be
sized against a bucket **9.24 % too large**.

### ② 🔮🧊 FROZEN PREDICTION — **THE OVER-COUNT SHOULD DIE AT TOMORROW'S 08:15 INIT**
**Rama's words, verbatim:** *"tomorrow's 08:15 INIT re-bases from broker net with no delivery
carry to rehydrate, so the ₹294.60 over-count should vanish and expected should equal broker
net. Falsifier: if tomorrow's post-INIT expected still exceeds broker net, the over-count is
persistent, not per-session — and that is a much larger defect."*

**MECHANISM SUPPORTING THE CALL, measured:** `initialize()` sets
`self._intraday_carry = 0.0` / `self._positional_carry = 0.0` **unconditionally**
(`fund_manager.py:485-486`, comment *"a fresh session carries nothing until rehydrate says
so"*). `rehydrate_carry` (`:1832`) then repopulates it **from open delivery trades**. ⭐ As of
`10:40` today there are **0 open CNC trades** and **0 `ACTIVE` gtt_state rows**.

**THE CALL:** at the 20-Aug 08:15 boot, `fund_manager.initialize` logs
`total == broker_balance`, and **either no `rehydrate_carry` line appears at all or it
carries `positional_carry: 0`** ⇒ post-INIT `expected` **equals** broker net ⇒ the first `G3`
delta of the day is **within the ₹50 tolerance** (≈0).
**FALSIFIER, single:** ⛔ **if post-INIT `expected` still exceeds broker net, the over-count
is PERSISTENT, not per-session** — a materially larger defect than DEFECT A, because it would
mean the inflation survives a re-base.

🔴 **CONFOUND NAMED IN ADVANCE — ⛔ WITHOUT IT THE PREDICTION IS UNSCOREABLE:** if a
**delivery entry fills today and is carried overnight**, then `_positional_carry` will be
**legitimately** non-zero tomorrow and `expected > broker net` is **CORRECT BEHAVIOUR**, ⛔ not
a falsification. ⇒ **the prediction is scoreable ONLY on a flat delivery book at 20-Aug
08:15.** ⭐ Today's book is flat so far and every delivery attempt has been throttled, but the
session runs to 15:30 — **check the delivery book before scoring.**
⭐ `NOT TESTED` if the service does not boot. ⛔ Never a pass.
⛔ **AND IT MUST NOT BE MADE TO PASS: no manual correction, no SYNC, no `fm_ledger` edit, no
restart engineered to re-base. Rama's instruction, and it is recorded here so a later session
cannot quietly satisfy the prediction instead of measuring it.**

### ③ 🔴 DEFECT C — **THE 09:15 `SYNC` HAD BROKER TRUTH IN HAND AND MOVED AWAY FROM IT**
⛔ **Its own row. ⛔ Not part of A, ⛔ not part of B.**

**MEASURED:** `fm_ledger 10826`, `09:15:00.034` — `SYNC +5.03`, `both`,
*"broker sync: 10912.27 -> 10917.30"*. Log line `09:15:00.037`:
`broker_cash=10622.7 · carry=294.6 · old_total=10912.27 · new_total=10917.30`.

**WHAT IT ACTUALLY DOES** — `fund_manager.sync_from_broker`, `capital/fund_manager.py:1411`:
```
carry_total = self._intraday_carry + self._positional_carry     # :1430
new_total   = broker_balance + carry_total                      # :1431
```
⇒ 🔑 **it does NOT reconcile to the broker. It reconciles to `broker + carry`, and then
OVERWRITES the running total with that reconstruction.** Whatever the session had learned in
between is discarded.

**WHY THE SIGN IS EXACTLY `+5.03`, and why that number is the tell:**
`_positional_carry` is written in exactly **two** places — set at `:1832` (`rehydrate_carry`)
and zeroed at `:485-486` (`initialize`). 🔑 **It is NEVER decremented when the carried
position is released.** So:
- `08:15:39` `RELEASE_USED` closes the trade and books `−5.03` ⇒ `_total` 10,917.30 → 10,912.27.
- `_positional_carry` **still holds 294.60** for a position that no longer exists.
- `09:15:00` SYNC recomputes `10,622.70 + 294.60 = 10,917.30` ⇒ **the realised loss is erased.**

⇒ ⭐⭐ **`+5.03` is not a rounding artefact — it is the ABSOLUTE VALUE OF THE BOOKED `net_pnl`,
and it appears because the reconstruction rebuilds the total from `cash + stale carry` and
discards the P&L the session had already recorded.** ⚠️ **Generalised: any realised P&L on a
released carry is wiped at the next SYNC.** ⭐ The one scheduled opportunity each day to
correct against the broker instead **re-injects** the error, at full value.
⛔ **REPORT ONLY. ⛔ No fix, ⛔ no design, ⛔ no SYNC invoked.**

### ④ 🗂️ THE THREE DEFECTS, KEPT SEPARATE — ⛔ DO NOT MERGE
| | **DEFECT A** | **DEFECT B** | **DEFECT C** |
|---|---|---|---|
| **name** | stale carry rehydration | prior-session SELL never discovered | the SYNC that reconstructs instead of reconciling |
| **what** | `rehydrate_carry` re-adds margin **the broker already returned** | exit undetected before the day's last in-hours cycle ⇒ cross-day finalise ⇒ day-scoped `get_trades()` cannot match ⇒ **LTP fallback ⇒ fabricated price** | `new_total = broker_cash + carry` with a carry never decremented on release |
| **site** | `fund_manager.py:1832` + `_bucket_base :2331-2335` | `cnc_gtt_monitor.py:674-694` + `zerodha_adapter.py:1760-1772` | `fund_manager.py:1411-1431` |
| **effect** | capital basis inflated ₹294.60; positional bucket **+9.24 %** | `exit_price 290.32` vs actual **290.10**; `net_pnl −5.03` vs **−4.68** | realised P&L on a released carry **erased**; error re-injected daily |
| **direction** | 🔴 **unsafe** (believes it has more) | ⛔ **no predictable sign** — here the price erred favourable ₹0.22 while the P&L erred unfavourable ₹0.35, the sign set by the **cost model** | 🔴 **unsafe** (restores the inflation) |
| **exposed population** | any delivery trade whose row outlives its broker position into a new session | **a DELIVERY (CNC/GTT) trade whose exit is not detected before the last in-hours monitor cycle of its own day.** ⛔ Intraday cannot reach it — it owns monitored exit legs | every session with a non-zero carry at 09:15 |
| **control / counter-example** | — | ⭐ **MMFL IS B's CONTROL AND BELONGS HERE.** Same code, same zero exit legs, finalised **in-hours same day** (`14:49:53`, 7 min after its `14:42:48` execution) ⇒ `get_trades()` still held the SELL ⇒ **684.20, EXACT.** ⛔ MMFL is **not** evidence about A | — |

⭐ **A and B share a victim and a date, ⛔ nothing else.** A is a **capital-accounting** defect
that would have occurred even if the price had been perfect. B is a **price-discovery** defect
that would have occurred even if the capital had been perfect. ⛔ Merging them would lose the
fact that **B has a control (MMFL) and A has none**, and would make the exposed populations —
which are *different sets* — look like one.

### PROHIBITIONS
⛔ No fix, ⛔ no SYNC, ⛔ no ledger edit, ⛔ no drift suppression, ⛔ no GTT action, ⛔ no DB
write, ⛔ no push, ⛔ no config change. ⛔ No edit above the boundary. ⭐ Every figure above is
either the running process's own logged value, a `sqlite3 -readonly` read, a line of deployed
source, or the contract note.

## ADDENDUM 6 — **THE DRIFT RECONCILES EXACTLY. ⛔ THE 10:12 CAVEAT IS RESOLVED, NOT STANDING.**
Added **19-Aug-2026 ~10:52 IST**. Broker figures raised by **Rama at 10:48**; ⭐ **verified
here against the RUNNING SERVICE's own `get_margins`, ⛔ not accepted as given.**
⛔ Nothing run, adjusted or fixed.

### A · ✅ INDEPENDENT VERIFICATION — THE SERVICE AGREES TO THE PAISA
| Rama's broker read, 10:48 | service's own measurement | agrees |
|---|---|---|
| available margin **₹10,511.31** | `get_margins` **`net=10511.314`**, flat across **20 consecutive reads** `10:44:56.196` → `10:49:43.320` | ✅ |
| one position open: **PATELRMART MIS ×2 @ 237.29** | `trades` open set = **exactly one row**: PATELRMART, `OPEN`, qty 2 @ 237.29, product **MIS** | ✅ |
| DHAMPURSUG · IDEAFORGE · MAWANASUG closed at qty 0 | `CLOSED_MANUAL` / `CLOSED` / `CLOSED`, all with `exit_price` written | ✅ |
| opening balance **₹10,622.70**, payin 0, payout 0 | today's `INIT` = `initialize with broker_balance=10622.7` | ✅ |

### B · 🔑 THE RECONCILIATION, ON THE SERVICE'S OWN NUMBER
```
expected (system)                       10,917.30
actual   (service get_margins @10:44:56) 10,511.314
                                        ───────────
delta                                      405.986

system-side over-count (DEFECT A)          294.60
residual                                   111.386   <-- broker USED MARGIN
Rama's used-margin figure                  111.39
                                        difference    0.004
```
⇒ ⭐⭐ **EXACT AT PAISA PRECISION.** The 0.004 is the broker's own rounding of used margin
(111.386 → 111.39), ⛔ not an unexplained term.

🔑 **ADDENDUM 3's caveat — *"the raw delta is unreadable as a shortfall measure while
positions are open"* — is hereby RESOLVED, ⛔ not left standing.** It was the right caution at
10:12 when I could not itemise the ₹882.71 residual; it is now **superseded by measurement**:
the residual **IS** the used margin, exactly, and nothing else is in it.

⭐ **AND THE CHECK COULD HAVE GONE RED** — this is why it is worth having done. Any *second*
system-side error would have surfaced as a **non-zero remainder after subtracting used
margin**. There is none. ⇒ **₹294.60 is the ENTIRE system-side error.** ⛔ Not "the largest
one" — the only one.

### C · WHAT THIS ESTABLISHES, AND ⛔ WHAT IT DOES NOT
✅ **ESTABLISHED (1):** ₹294.60 is the complete system-side error; there is no second defect
hiding in the delta.
✅ **ESTABLISHED (2):** **today's `INIT` of 10,622.70 was CORRECT.** Opening balance matches,
**payin 0, payout 0** ⇒ nothing moved externally; the boot re-based on a true figure and then
`rehydrate_carry` corrupted it 5 ms later.
⚠️ **CHAIN AGREES TO ~5 PAISE, AND I STATE THE RESIDUAL RATHER THAN CLAIM "EXACT":** service's
18-Aug close **10,611.00** + Rama's settlement credit **11.75** = **10,622.75**, against the
funds statement's closing **10,622.71** and the service's INIT **10,622.70**. ⛔ The ~4-5 paise
across three independent sources is **NOT explained here** and is below any threshold that
moves a decision — ⭐ recorded so nobody later reports it as exact.
⛔ **DOES NOT ESTABLISH that it self-corrects.** ⭐ That remains **ADDENDUM 5 ②**, frozen,
scored at the **20-Aug 08:15** boot, on a flat delivery book. ⛔ Nothing here advances it.

### D · 🔴 **`B-2`** — A CONSEQUENCE OF DEFECT B: **YESTERDAY'S FABRICATED LOSS IS CONSUMING TODAY'S DAILY-LOSS BUDGET**
⛔ Filed as a **consequence of B**, ⛔ not a fourth defect — it follows directly from the
cross-day finalisation that defines B's population.

**MEASURED:** `fund_manager.py:1346` — `daily_pnl = self._store.get_daily_realized_net_pnl(today)`,
compared at `:1348` against `loss_limit = daily_loss_limit_pct × self._total`. The daily figure
sums `fm_ledger.pnl_delta` for `date = today`, and `date` is a STORED column derived from the
row's **write** timestamp.

⇒ UTTAMSUGAR's `RELEASE_USED` was written at **`08:15:39` on 19-Aug**, so its `pnl_delta`
carries `date = 2026-08-19` — **although the trade executed at `15:22:18` on 18-Aug.**

| today's booked P&L | ledger | note |
|---|---|---|
| UTTAMSUGAR | **−5.03** | 🔴 **an 18-Aug execution**, and the figure is itself **fabricated** (actual −4.68) |
| IDEAFORGE | −8.02 | today |
| DHAMPURSUG | −5.49 | today |
| MAWANASUG | −4.97 | today |
| **SUM (system's 19-Aug daily P&L)** | **−23.51** | of which **−5.03 = 21.4 % belongs to yesterday** |

⇒ 🔑 **today's daily-loss budget is being consumed by a fabricated loss from a prior
session.** ⭐ Two errors now run in **opposite** directions and ⛔ must not be netted or relied
on: the **limit** is **₹8.85 too generous** (halt too far away — unsafe), while the
**counter** starts **₹5.03 too low** (halt too near — safe). ⛔ **A partial offset is not a
control**; either term can move independently tomorrow.

📌 **Broker Day P&L −₹16.21 vs the system's −₹23.51 is ⛔ NOT a discrepancy and must not be
reported as one** — they are different quantities: the broker's figure includes PATELRMART's
open MTM and **excludes** UTTAMSUGAR entirely (settled yesterday); the system's is realised-only
and **includes** UTTAMSUGAR. ⛔ Not like-for-like; ⛔ no conclusion drawn.

### E · ⚠️ THE DRIFT ALARM'S CADENCE — 🔴 **CORRECTED 19-Aug ~17:45, SEE §E-2 BELOW**
~~`G3 CAPITAL_DRIFT` has fired **3 times today** … the gaps mean it is **throttled, ⛔ not a
30-minute heartbeat**~~ — ⛔ **that sentence was written at ~10:45 from IN-HOURS data only and
is WRONG as a general statement.** ⭐ The half that survives: ⛔ **a quiet period is NOT the
drift closing, and the last printed delta is NOT the current one** — the delta at `10:44:56`
was **405.986**, computed, ⛔ never alarmed.

### E-2 · 🔴 CORRECTION — THE CADENCE IS ~30 MIN POST-CLOSE; THE IN-HOURS SILENCE IS THE ANOMALY
Raised by **Rama, 19-Aug ~17:45**, from the alert stream; ⭐ **verified here against the full-day
log rather than accepted.** The service ran to `17:35:04`, so my 15:16 count of *"3 all day"*
was measured with **two hours still to run** — it was true when taken and stale by 17:35.

**ALL SEVEN `G3` ALARMS, FULL DAY:**

| # | ts | expected | actual | delta | gap from prev |
|---|---|---|---|---|---|
| 1 | `08:15:38.701` | 10,917.30 | 10,622.70 | 294.60 | — |
| 2 | `08:45:40.089` | 10,912.27 | 10,622.70 | 289.57 | **30 m 02 s** |
| 3 | `10:12:35.908` | 10,917.30 | 9,739.99 | 1,177.31 | ⚠️ **86 m 56 s** |
| 4 | `15:45:07.398` | **10,904.01** | **10,611.91** | **292.10** | 🔴 **5 h 32 m 32 s** |
| 5 | `16:15:22.057` | 10,904.01 | 10,611.91 | 292.10 | **30 m 15 s** |
| 6 | `16:45:35.471` | 10,904.01 | 10,611.91 | 292.10 | **30 m 13 s** |
| 7 | `17:15:48.241` | 10,904.01 | 10,611.91 | 292.10 | **30 m 13 s** |

⇒ 🔑 **POST-CLOSE IT IS A CLEAN ~30 m 13 s HEARTBEAT (4 alarms). IN-HOURS IT IS NOT** — an
**87-minute** gap and then a **5½-hour** gap swallowing ~11 consecutive slots.
⛔ **So neither *"it is throttled"* nor *"it is a 30-minute heartbeat"* is right on its own.**
⛔ **WHY the in-hours slots were suppressed is NOT DETERMINED** — ⭐ and it is **not**
value-deduplication, because alarms 4–7 carry **byte-identical figures** and still fired every
30 minutes. 📌 **THE RULE FOR TOMORROW'S READER, unchanged in force and now correctly based:
⛔ G3's SILENCE MEANS NOTHING IN EITHER DIRECTION — compute the delta.**

### E-3 · ⭐ THE INVARIANCE IS ITSELF EVIDENCE — **DEFECT A IS STATIC, ⛔ NOT ACCUMULATING**
Alarms 4–7 span **90 minutes** and carry **identical figures to the paisa** — `expected
10,904.01 · actual 10,611.91 · delta 292.10`, four times over.
⇒ 🔑 **DEFECT A is a FIXED over-count, ⛔ not a leak.** ⭐ That is exactly what a **stale carry**
predicts (one wrong constant, re-applied) and exactly what a **leak** would contradict (a
growing delta). ⭐⭐ **And it independently corroborates my own reconciliation: I computed
`expected = 10,904.01` at 15:15 from the bucket sum `7,422.60 + 3,481.41`, and the system's own
alarm printed the same number four times — ⛔ two different derivations, one figure.**
📌 **This strengthens tomorrow's ② without touching it:** a static over-count is precisely what a
fresh `INIT` with **no carry to rehydrate** should erase.

### E-4 · ⛔ THE GEMINI `log_review` FAILURE IS TOOLING, ⛔ NOT TRADING EVIDENCE
Recorded so it is not mistaken for a finding: the EOD `log_review` **FAILED on quota/timeout**.
⛔ **A review that did not run produces NO conclusion** — ⛔ not a clean bill, ⛔ not a concern.
⭐ Nothing in tonight's EOD assessment rests on it.

### PROHIBITIONS
⛔ No fix, ⛔ no SYNC, ⛔ no ledger edit, ⛔ no drift suppression, ⛔ no DB write, ⛔ no push.
⛔ No edit above the boundary.

## ADDENDUM 7 — **`B-2` PROMOTED TO **DEFECT D**, ON RAMA'S RULING. + THE ALARM VERIFIED.**
Added **19-Aug-2026 11:15 IST**. Ruling by **Rama, 19-Aug ~11:1x**: *"B-2 is the most
consequential finding of the morning and it deserves its own row, ⛔ not a sub-item of B."*
⛔ Observation only; ⛔ no SYNC, ⛔ no ledger edit, ⛔ no fix.

### A · 🔴 **DEFECT D — THE REALISED-P&L BUCKET KEYS ON THE LEDGER *WRITE* TIMESTAMP**
⛔ **Its own row.** ⭐ It was filed under B in ADDENDUM 6 §D; that placement is **superseded**.
**Why it is not B:** B is a *price-discovery* defect — it corrupts the **value** written.
D is a *date-attribution* defect — it corrupts **which day the value counts against**.
🔑 **D would fire even if B were fully fixed**: a boot-time clear with a *perfectly correct*
exit price would still book that P&L to the boot's date.

**MECHANISM, measured:**
- `capital/fund_manager.py:1346` — `daily_pnl = self._store.get_daily_realized_net_pnl(today)`
- `:1347-1348` — `loss_limit = self._daily_loss_limit_pct * self._total`; breach when
  `daily_pnl <= -loss_limit`
- the daily figure sums `fm_ledger.pnl_delta` where `date = today`, and `date` is a **STORED
  generated column** — `substr(ts,1,10)` — i.e. **the row's WRITE time**, ⛔ never the trade's
  execution time.

**MEASURED INSTANCE:** UTTAMSUGAR executed its SELL at **`15:22:18` on 18-Aug**. Its
`RELEASE_USED` was written at **`08:15:39.575` on 19-Aug** ⇒ `date = 2026-08-19` ⇒ its
`pnl_delta −5.03` counts against **today's** loss budget.

| today's booked realised P&L | value | execution day |
|---|---|---|
| UTTAMSUGAR | **−5.03** | 🔴 **18-Aug** — and the value is itself fabricated (actual −4.68) |
| IDEAFORGE | −8.02 | 19-Aug |
| DHAMPURSUG | −5.49 | 19-Aug |
| MAWANASUG | −4.97 | 19-Aug |
| **SUM = system's 19-Aug daily P&L** | **−23.51** | **21.4 % of it belongs to yesterday** |

⇒ ⭐⭐ **STRUCTURAL, ⛔ NOT INCIDENTAL: every boot-time delivery clear will do this, by
construction** — the clear happens at boot, the boot is a new date, the ledger row therefore
carries the new date. **D's exposed population is exactly DEFECT B's** (a delivery trade
finalised in a later session), ⛔ **but its harm is different and independent.**

⛔⛔ **AND THE TWO ERRORS MUST NOT BE READ AS OFFSETTING INTO SAFETY** — Rama's ruling,
recorded verbatim because the temptation is real: the **limit** is **₹8.85 too generous**
(₹327.52 vs a true ₹318.68 — the halt sits too far away) while the **counter** starts
**₹5.03 too low** (the halt sits too near). ⭐ **They have different causes (D's is the write
date, A's is the inflated `_total`) and move INDEPENDENTLY.** ⛔ A partial offset is not a
control, and tomorrow either term can move alone.

### B · 🗂️ THE DEFECT REGISTER NOW READS FOUR ROWS — ⛔ DO NOT MERGE ANY PAIR
| | **A** | **B** | **C** | **D** |
|---|---|---|---|---|
| defect | stale carry rehydration | prior-session SELL never discovered | SYNC reconstructs instead of reconciling | realised-P&L keyed on ledger WRITE date |
| corrupts | the capital **basis** | the exit **value** | the **correction** that should fix A | the **date** the value counts against |
| site | `fund_manager.py:1832`, `:2331-2335` | `cnc_gtt_monitor.py:674-694`, `zerodha_adapter.py:1760-1772` | `fund_manager.py:1411-1431` | `fund_manager.py:1346`, `fm_ledger.date` |
| direction | 🔴 unsafe | ⛔ no predictable sign | 🔴 unsafe | 🔴 unsafe *in the limit*, safe *in the counter* — ⛔ independently |
| control | none | ⭐ **MMFL** | none | none |
| survives the others being fixed? | yes | yes | yes | **yes — fix B and D still fires** |

### C · ⏰ THE ALARM WAS CHALLENGED AND VERIFIED — ⛔ NOT ASSUMED
Rama flagged a possible timezone fault (*"same class as the PC's broken `TZ=Asia/Kolkata`"*).
**Measured, four ways:**

| | value |
|---|---|
| PC shell `date` | `2026-08-19 11:11:51 IST +0530` (epoch `1787118111`) |
| VM `date` | `2026-08-19 11:11:56 IST +0530` (epoch `1787118116`) — **5 s apart** |
| VM `timedatectl` | `Asia/Kolkata (IST, +0530)`, **clock synchronized: yes**, NTP active |
| PC `tzutil /g` | `India Standard Time`; `TZ` env **unset** ⇒ no override to misresolve |
| target epoch | `1787119200` = **`2026-08-19 11:30:00 IST`** ✅ |

Launch line reconciles: `now=09:19:42 target=11:30 delta=7818s`, and `09:19:42 + 7818 s =
11:30:00`. ⇒ ✅ **CORRECT; no manual fallback required.**
⭐ **The apparent discrepancy was MY reporting, ⛔ not the clock** — my last VM read
(`10:49:52`) was ~22 min stale when challenged. ⛔ **This is NOT the `TZ=Asia/Kolkata` class:**
that trap presents as a **5 h 30 m** offset, and the two clocks are within **5 seconds**.
📌 ⭐ **The check was still worth running — it could have gone red, and a silently-wrong alarm
would have cost the checkpoint.**

### D · CARRIED INTO THE 11:30 CHECKPOINT
⛔ **`G3`'s last printed delta is STALE and must NOT be reported as current.** It has fired
**3 times all day** (`08:15:38.701` Δ294.60 · `08:45:40.089` Δ289.57 · `10:12:35.908`
Δ1177.31) — throttled via `_should_alert_capital_drift`, ⛔ **not a 30-minute heartbeat**.
⇒ ⭐ **at 11:30 the delta is to be COMPUTED from `expected` and a fresh `get_margins`, ⛔ never
read off the last alarm.** ⛔ A quiet period is **not** the drift closing.

## ADDENDUM 8 — **A WRONG CALL RECORDED, AND A SCOPING BRIEF REGISTERED BUT ⛔ NOT STARTED.**
Added **19-Aug-2026 11:19 IST**. ⛔ No design, no code, no measurement beyond what ADDENDUM 7
already recorded. ⭐ Filed now so the instruction trail survives the checkpoint.

### A · 🔴 **`WC-1` — A WEB CLAUDE CALL THAT WAS WRONG, RECORDED AT RAMA'S INSTRUCTION**
**The call (Web Claude, 19-Aug ~11:1x):** the 11:30 alarm may be mis-scheduled; the task's
runtime against its 09:19 start implied ~11:08, and `date -d "today 11:30"` was evaluated once
at launch ⇒ *"same class as the PC's broken `TZ=Asia/Kolkata`"*.

**🔴 WRONG — REFUTED BY MEASUREMENT** (ADDENDUM 7 §C): PC `11:11:51 IST +0530` and VM
`11:11:56 IST +0530` — **5 seconds apart**; `timedatectl` `Asia/Kolkata`, synchronized, NTP
active; `TZ` env **unset**; target epoch `1787119200` = **`11:30:00 IST`**; and the launch line
reconciles exactly (`09:19:42 + 7818 s = 11:30:00`).

**Rama's own words closing it, verbatim:** *"my concern was wrong and your explanation is
right: both readings were correct at their moments and never conflicted. ⛔ Not the TZ class;
that would show as a 5h30m offset. Record it as a Web Claude call that was WRONG."*

⭐ **WHAT THE EPISODE IS WORTH KEEPING FOR, since the alarm turned out fine:**
1. ⛔ **The apparent conflict was a STALENESS artefact in MY reporting, ⛔ not a clock fault** —
   I quoted a VM read (`10:49:52`) that was ~22 minutes old as though it were current. ⇒ 📌
   **a measured time must carry the moment it was measured, exactly like every other figure.**
2. ⭐ **The check was still right to run: it could have gone red**, and a silently-wrong alarm
   would have cost the checkpoint outright.
3. 🏷️ **The discriminator is now written down** so the class is not mis-diagnosed again:
   **the `TZ=Asia/Kolkata` trap presents as a 5 h 30 m offset.** ⛔ Anything inside seconds is
   not that class.
📌 Companion to `N18-15` (*"two premises in the evening card were wrong and were flagged
rather than absorbed"*) — ⭐ **the same practice, now applied to a Web Claude call.**

### B · 📋 SCOPING BRIEF REGISTERED — ⛔ EXPLICITLY NOT STARTED
**Rama, 19-Aug ~11:1x, verbatim:** *"finish the 11:30 checkpoint first, ⛔ design nothing
before it."* ⭐ **Nothing below has been investigated; ⛔ no file:line has been looked up for
this purpose; ⛔ no values proposed; ⛔ no code written.** Recorded only so the brief is not
lost or silently reinterpreted later.

**The ask, after the checkpoint — three surgical fixes, one root each, `file:line` for each,
plus an honest verdict on whether each is genuinely that small:**

| defect | the proposed root, in Rama's words | his own size claim |
|---|---|---|
| **D** | *"`fm_ledger.date` is `substr(write_ts,1,10)`. Pass the business date explicitly for boot-time clears."* | ⭐ *"One argument, ⛔ not a schema migration."* |
| **B** | *"when `get_trades()` finds no SELL, ⛔ do NOT fall back to LTP. Mark the exit UNRESOLVED and alert."* | 🔑 *"That single principle — fail loudly rather than fabricate — would have surfaced A and D back on 11-Aug when DIFFNKG first showed it."* |
| **A** | *"`rehydrate_carry` re-adds margin on the premise the broker still holds it. Check the position actually exists at the broker first; the system already makes that call."* | — |

⛔ **AND THE REJECTED SCOPE IS RECORDED TOO, because it is the more important half:** Rama
explicitly rejected *"new date columns, an idempotency layer, freshness guards, invariant
failures and a six-part regression matrix"* as **"larger than everything deployed this week
combined, and it touches the exact paths that hard-killed 10-Aug."** ⇒ ⛔ **a later session
must not quietly re-expand to that plan.**

📌 **SEQUENCING, ruled by Rama and ⛔ not negotiable by a later session:**
1. ⭐ **`tiers` lands FIRST — it is a DB change and goes ALONE.**
2. ⛔ **NO capital-path change stacks on top of a pending DB change.**
3. ⭐ **Then ONE fix per evening, each with its own frozen prediction.**

⚠️ **STANDING CONSTRAINT, unchanged:** A, C and D are all capital-path and B is signal/order
path ⇒ **all four go through the careful loop (design → review → implement)**, ⛔ never a
direct patch.

## ADDENDUM 9 — **`WC-2` RECORDED · THE THREE ROOTS MEASURED · TWO OF THE THREE FRAMINGS ARE WRONG.**
Added **19-Aug-2026 ~11:50 IST**. ⛔ **No code. ⛔ No design. ⛔ No values proposed.** Every
`file:line` below was read on the **deployed tree** (`~/systems/trading-system`, `origin/main`
`08b462b`). 📌 Line numbers hold **only** at this SHA (`M3`).

### A · 🔴 **`WC-2` — A SECOND WEB CLAUDE CALL THAT WAS WRONG**
**The call (Web Claude, 19-Aug 10:48):** *"expected 10,917.30 − actual 10,511.31 = 405.99. And
294.60 + 111.39 = 405.99. Exact to the paisa … the drift is now FULLY reconciled … And it
could have gone red."*

**🔴 WRONG.** `expected` was the **09:15 SYNC value**, already stale by **₹18.48** at 10:48 —
three `RELEASE_USED` rows had booked IDEAFORGE −8.02 (`10:20:40`), DHAMPURSUG −5.49
(`10:30:49`) and MAWANASUG −4.97 (`10:33:24`). True `_total` at 10:48 was **10,898.82**
(verified two ways: `10,917.30 − 18.48`; and bucket sum `7,322.494 + 94.916 + 3,481.41`).

⇒ **the two-term decomposition omitted the same ₹18.48 that the stale `expected` carried, so
the equation balanced by CANCELLATION.** The correct three-term form:
```
expected 10,898.82 − actual 10,511.314 = 387.506
       = used margin 111.386 + DEFECT A 294.60 + realised P&L (−18.48)
```
**Rama's own words closing it, verbatim:** *"My 10:48 reconciliation was WRONG and yours
corrects it … I used the 09:15 expected as if it were current, and the two-term decomposition
omitted the same ₹18.48, so it read as exact by cancellation. ⭐ Exactly the staleness error I
flagged in your alarm report, made by me twenty minutes later. ⛔ Two errors cancelling is not
a verification, and I called it 'could have gone red' when it could not."*

⭐⭐ **THE LESSON, AND IT IS THE SAME ONE TWICE IN THIRTY MINUTES (`WC-1`, then `WC-2`):
A FIGURE MUST CARRY THE MOMENT IT WAS MEASURED.** ⛔ And a reconciliation that balances is
**not** self-verifying — ⭐ **it must be shown that it COULD have failed.** Here it could not:
both sides shared the omission. 📌 The third term is not new — the standing memory row already
states it: *"delta = deployed capital + unsettled realised P&L; decomposes EXACTLY."*
**DEFECT A is the only anomalous term, which is the conclusion `WC-2` reached by a route that
did not support it.**

---

### B · 🔑 **DEFECT B — `NOT SMALL`. RAMA'S CONCERN CONFIRMED, AND HIS ALTERNATIVE IS INFEASIBLE.**
**ROOT SITE:** `orders/cnc_gtt_monitor.py:674-694` (`_resolve_exit_price`).
**BINDING CONSTRAINT:** `broker/zerodha_adapter.py:1760-1772` — `get_trades()` returns
***today's*** executed trades. **Day-scoped.**
**CURRENT BEHAVIOUR:** broker trades matching the exit side → **LTP** → entry proxy, falling
through **silently**.

**① THE DOWNSTREAM RISK RAMA ASKED TO BE MEASURED FIRST — ✅ CONFIRMED, EXACTLY AS HE PUT IT:**
- `core/state_store.py:639-656` — `count_active_positions()` =
  `SELECT COUNT(*) FROM trades WHERE status IN ('OPEN','PARTIAL','PENDING_FILL')`
- `main.py:1074-1112` — `_eod_self_exit_due(...)` returns `(active == 0, active)`
⇒ 🔴 **if "mark UNRESOLVED" leaves the row NON-TERMINAL, it feeds `count_active_positions()`,
`eod_self_exit` never fires, and the manual stop becomes owed EVERY NIGHT a delivery exit goes
undiscovered.** ⭐ That is the **05-Aug / 18-Aug pathology re-created deliberately** — trading
a fabricated price for a service that never shuts down.
🏷️ **VERDICT: `NOT SMALL` as framed.**

**② A NEW *TERMINAL* STATUS IS ALSO `NOT SMALL`** — `trades.status` carries **both** a
`CHECK (status IN (…) OR status GLOB 'REJECTED*')` **and** the trigger
`trg_trades_terminal_status_guard` (BEFORE UPDATE, RAISE(ABORT) on any terminal transition).
⇒ **a schema migration**, and the standing rule is that an evening schema push buys a night of
CRITICALs.

**③ 🔴 RAMA'S ALTERNATIVE — *"resolve the price correctly (query the prior session's
trades)"* — IS `INFEASIBLE` ON THE CURRENT BROKER SURFACE. ⛔ Not merely hard.**
The adapter exposes exactly **three** broker read paths:
`get_gtts()` `:893` · `get_order_history(broker_order_id)` `:1118` · `get_trades()` `:1760`.
Kite's `trades()`/`orders()` are **day-scoped**, and `get_order_history` needs a
**broker_order_id the system never had** — 🔑 **because the 15:22:18 sell was NOT the system's
order.** Measured, three ways:
- `eod_squareoff` at `15:17:06.069` — *"broker-position filter kept **0/0** trades (broker
  open symbols=0)"*, then *"Pass 2 complete: **0** open positions exited"* ⇒ the system placed
  nothing;
- the `orders` table holds **one** leg for that trade, the ENTRY BUY;
- the GTT that *would* have sold it triggered at **15:25:25 — three minutes LATER** — and was
  **exchange-rejected** because the position was already gone.
⇒ ⭐⭐ ~~**THE EXIT WAS EXTERNALLY INITIATED**~~ — 🔴 **CORRECTED 19-Aug ~12:2x: THE EXIT WAS
*OPERATOR*-INITIATED. Rama closed it himself** — Positions → ⋮ → Exit — and said so at **19:15
on 18-Aug**. ⛔ **Not external, ⛔ not RMS, ⛔ not unexplained.** ⭐ The original phrasing was
correct as *"not the system's own order"* and **wrong as *"unknown"***.
⭐ Still exactly what `_resolve_exit_price`'s docstring covers — *"closed externally (RMS
squareoff, **manual close via terminal**)"* — the **second** clause, ⛔ not the first.
⛔ **There is no API that returns a prior day's trades; that data lives only in the contract
note / console reports** — that part stands.
⇒ **the defect is not that the system lost its own exit — it is that it never DISCOVERED an
operator's close, and then invented a number rather than saying so.**

**④ ⭐ A THIRD SHAPE THAT *MIGHT* BE SMALL — ⛔ FLAGGED, NOT DESIGNED, NOT VERIFIED:**
keep the row **TERMINAL** (so `count_active_positions()` and `eod_self_exit` are untouched)
but **refuse to write a fabricated price**: `exit_price` NULL, a distinct `exit_reason`, and
alert. Schema *appears* free — `exit_price`/`net_pnl` are nullable REAL, `exit_reason` is free
TEXT with no CHECK. ⚠️ ⛔ **I will NOT call it SMALL until the consumers of a NULL
`exit_price`/`net_pnl` are swept** — reports, GUI, the 17:35 census, the daily-P&L sum, and
`RELEASE_USED`'s own pnl argument (the margin must still be freed). ⭐ **Rama's principle —
*fail loudly rather than fabricate* — survives intact in this shape; only his mechanism does
not.**

---

### C · **DEFECT D — `NOT SMALL` AS FRAMED (write side); ⭐ PLAUSIBLY SMALL ON THE READ SIDE**
**ROOT SITES:** `core/state_store.py:2555-2586` (`get_daily_realized_net_pnl`) ·
`fm_ledger.date` = **`TEXT GENERATED ALWAYS AS (substr(ts, 1, 10)) STORED`** ·
consumed at `capital/fund_manager.py:1346-1348`.

**Rama's proposal:** *"Pass the business date explicitly for boot-time clears. ⭐ One argument,
⛔ not a schema migration."*
🔴 **NOT ACHIEVABLE ON THE WRITE SIDE.** `date` is **GENERATED ALWAYS … STORED** from `ts`.
⛔ It cannot be passed. The only write-side routes are (i) falsify `ts` — ⛔ it must remain the
write time, it is the ledger's audit spine — or (ii) **ALTER TABLE to add a `business_date`
column** = **a schema migration**, which is what he explicitly ruled out.

⭐ **BUT A ONE-ARGUMENT-SHAPED FIX EXISTS ON THE READ SIDE, AND IT IS SCHEMA-FREE:**
`get_daily_realized_net_pnl` is a **single query** (`:2582-2585`); attributing by the trade's
own exit date instead of the ledger write date means joining `fm_ledger.trade_id → trades`.
⚠️ **Named caveats, ⛔ not waved past:** `fm_ledger.trade_id` is **nullable** and set only on
COMMIT/RELEASE_USED; `RESET_PNL` rows carry none; the join abandons the **indexed `date`
column** that `O4 (v27)` was introduced specifically to use; and the same NET contract is
consumed by rehydrate, the GUI and the capacity readers (named in the docstring).
🏷️ **VERDICT: `NOT SMALL` as framed · ⭐ `PLAUSIBLY SMALL` re-framed to the read side** —
⛔ subject to the four caveats above being cleared.

---

### D · **DEFECT A — `NOT SMALL`. THE BROKER CALL EXISTS BUT HAPPENS ~90 ms TOO LATE.**
**ROOT SITE:** `capital/fund_manager.py:1831-1834`, inside `rehydrate_from_open_trades`
(defined `:1720`), invoked from `main.py:2476`.
**CURRENT BEHAVIOUR:**
```
self._positional_carry = (self._positional_reserved + self._positional_used
                          - _positional_committed_before)
```
⇒ 🔑 **derived ENTIRELY from the system's own trade rows. ⛔ There is no broker call in this
method at all**, and `rehydrate_from_open_trades(_start_of_today_iso)` **takes no adapter**.

**Rama's claim — *"the system already makes that call"* — ⭐ TRUE, but at the WRONG TIME:**
| event | timestamp |
|---|---|
| `fund_manager.rehydrate_carry` (carry decided) | **`08:15:38.484`** |
| `get_positions` → `0 positions` | `08:15:38.572` — **+88 ms** |
| `get_holdings` → `0 holdings` | `08:15:39.471` — **+987 ms** |
⇒ **the refuting evidence was obtained inside the same second and arrived after the decision.**

**WHY IT IS `NOT SMALL`:**
1. 🔴 It changes the **boot-time capital path** — ⛔ the exact path that **hard-killed 10-Aug**.
2. ⛔ The method carries an explicit **`⛔⛔ DO NOT RE-KEY THIS ON THE LEDGER`** invariant
   (`main.py:2449-2453`): trade status is deliberately the **sole** source of truth, *"the ONLY
   reason a corrupt ledger cannot poison startup capital."* Adding a **broker** dependency is an
   architectural change, ⛔ not a parameter.
3. ⛔ **`sync_from_broker` (`:1430`) reads the same `_positional_carry`** — DEFECT C. Fixing A
   without C leaves the 09:15 SYNC re-injecting the error daily; fixing both is **two capital
   sites in one change**.
4. 🔑 **It introduces a new failure mode with no safe default:** if `get_positions` fails at
   boot, fail-OPEN re-adds the phantom carry (today's bug) and fail-CLOSED risks the negative-
   bucket hard-kill. ⭐ The `Y4` rule already in `cnc_gtt_monitor` — *"defer + alert, never treat
   no-data as no-positions"* — is the precedent, and it is a **third** behaviour, not a flag.

---

### E · 🗂️ SUMMARY — ⛔ AND THE EVENINGS DO NOT MIX
| defect | root `file:line` | framing as given | verdict | principal downstream risk |
|---|---|---|---|---|
| **A** | `fund_manager.py:1831-1834` (in `:1720`), called `main.py:2476` | check the broker first | 🔴 **NOT SMALL** | boot capital path (10-Aug hard-kill); entangled with **C** |
| **B** | `cnc_gtt_monitor.py:674-694` + `zerodha_adapter.py:1760-1772` | mark UNRESOLVED, don't fall back | 🔴 **NOT SMALL** | non-terminal row ⇒ `eod_self_exit` never fires ⇒ **manual stop owed nightly** |
| **C** | `fund_manager.py:1411-1431` | *(not tabled by Rama)* | — | re-injects A daily; ⛔ cannot be fixed independently of A |
| **D** | `state_store.py:2555-2586`; `fm_ledger.date` generated column | one argument, no migration | 🔴 **NOT SMALL** as framed · ⭐ **PLAUSIBLY SMALL** on the read side | join caveats; drops the `O4` index |

📌 **PATH SEPARATION, per Rama — ⛔ they do not share an evening:**
**A · C · D = CAPITAL path** · **B = SIGNAL/ORDER path.**
📌 **SEQUENCING, unchanged:** `tiers` lands **first and alone** (DB change) ⇒ ⛔ no capital-path
change stacks on a pending DB change ⇒ then **one fix per evening, each with its own frozen
prediction.**
⚠️ **All four go through the CAREFUL LOOP (design → review → implement).** ⛔ None is a patch.

⛔ **Nothing built, designed, valued or proposed beyond naming the roots and sizing them.**

## ADDENDUM 10 — **ONE ROW ABOUT HOW THE DAY WENT WRONG · AND A ZERO-CODE OPERATOR MITIGATION.**
Added **19-Aug-2026 ~12:00 IST**. ⛔ No implementation, ⛔ no code, ⛔ no design.

### A · 🔑 **`WC-PATTERN` — FIVE WRONG CALLS, FILED AS ONE ROW ABOUT METHOD, ⛔ NOT FIVE ERRORS**
**Rama's instruction, verbatim:** *"The pattern is worth more than the four entries: I proposed
each from reasoning, you refuted each by reading the deployed code. Five Web Claude calls wrong
today — alarm, reconciliation, A, B, D. File it as one row about how I'm operating, ⛔ not five
isolated errors. SOURCE WINS, and today it won five times."*

| # | the call, from reasoning | what the deployed source said |
|---|---|---|
| **1** | the 11:30 alarm is mis-scheduled, *"same class as the broken `TZ=Asia/Kolkata`"* | PC and VM clocks **5 s apart**, both IST, NTP synced; target epoch `1787119200` = **11:30:00 IST**. ⛔ The TZ class presents as **5 h 30 m**, not seconds |
| **2** | the drift *"reconciles exactly … and could have gone red"* | `expected` was **stale by ₹18.48**; the two-term form omitted the same ₹18.48 ⇒ **balanced by cancellation**. ⛔ It could **not** have gone red |
| **3** | **A**: *"check the position exists at the broker first; the system already makes that call"* | the call fires **88 ms AFTER** the decision (`rehydrate_carry 08:15:38.484` → `get_positions 08:15:38.572`), and the method carries an explicit **`⛔⛔ DO NOT RE-KEY THIS ON THE LEDGER`** invariant |
| **4** | **B**: *"query the prior session's trades"* | **infeasible** — Kite `trades()`/`orders()` are **day-scoped**, and `get_order_history` needs an id the system never had, **because the sell was never the system's order** |
| **5** | **D**: *"pass the business date explicitly — one argument, not a schema migration"* | `fm_ledger.date` is **`GENERATED ALWAYS AS (substr(ts,1,10)) STORED`** ⇒ ⛔ it **cannot be passed**; the write-side fix **is** a migration |

⭐⭐ **THE ROW, AND IT IS THE POINT: EVERY ONE WAS A PLAUSIBLE INFERENCE FROM A CORRECT MENTAL
MODEL, AND EVERY ONE DIED ON A LINE OF DEPLOYED SOURCE.** ⛔ None was careless; ⭐ that is what
makes the pattern worth a row rather than five apologies. **`SOURCE WINS` — five times in one
morning.**

📌 **Operationally, and this is the useful half:** ⭐ **the division of labour that produced
today's findings is the reasoning side PROPOSING and the source side REFUTING** — ⛔ it breaks
the moment either side is trusted to do both. **Two of the five (`1`, `2`) were staleness — a
figure quoted without the moment it was measured — and one of those was mine.** ⇒ 📌 **a
measured value carries its timestamp, or it is not evidence.**
⚠️ **`WC-2`'s deeper lesson stands separately: a reconciliation that BALANCES is not
self-verifying. ⛔ It must be shown that it COULD have failed.**

📌 **RECORDED WITHDRAWAL:** Rama withdrew his B framing in favour of the third shape —
*"keep the row terminal, `exit_price` NULL, distinct `exit_reason`, alert."* ⛔ **And it stays
`NOT YET SIZED` until the NULL-consumer sweep is done: reports · GUI · the 17:35 census · the
daily-P&L sum · `RELEASE_USED`'s own pnl argument.** ⛔ Not called SMALL.

---

### B · ⏰ **THE MANUAL-CLOSE BOUNDARY — MEASURED. ⛔ IT IS NOT A FIXED CLOCK TIME.**
**The question (Rama):** *"MMFL closed manually at ~14:30 and reconciled correctly at 14:34;
UTTAMSUGAR closed at 15:22 and did not. What is the last clock time at which a manual delivery
close still reconciles?"*

**MECHANISM:** `order_reconciler.py:658-676` — the monitor runs from the 15 s poll thread,
gated `if not in_hours: return`, then every `_cnc_monitor_every = 60` cycles ⇒ **60 × 15 s =
900 s nominal**. `_market_hours_fn = market_windows.is_market_open(...)`;
`config/system_config.yaml:51` — **`market_close: "15:30"`**.

**MEASURED CADENCE** (one `get_holdings` per cycle):

| 18-Aug (last 4) | 19-Aug (last 4 so far) |
|---|---|
| 14:49:53.080 · 15:05:09.657 · **15:20:17.936 ← LAST** · *(none)* | 11:16:01.872 · 11:31:10.830 · 11:46:24.537 · … |

⭐ **Real interval ≈ 15 m 08 s, ⛔ not 15 m 00 s** — it drifts ~8 s per cycle (poll overhead on
top of 60×15 s), so it accumulates ~3 minutes across a session.

**⇒ THE BOUNDARY IS THE LAST IN-HOURS CYCLE, AND ITS CLOCK TIME MOVES DAY TO DAY:**
- **18-Aug measured last cycle: `15:20:17`.**
- **19-Aug projected last cycle: `~15:18:30`** (from `11:46:24.5` at ~15 m 09 s; the next after
  that lands ~15:33 ⇒ **out of hours**).
- ⇒ **~2-minute day-to-day spread**, driven by when the first in-hours cycle lands and by
  accumulated drift. ⛔ **There is no fixed clock time to publish.**

**THE TWO CASES, AGAINST THAT BOUNDARY:**
| | closed | next in-hours cycle | outcome |
|---|---|---|---|
| **MMFL** | 14:42:48 | **14:49:53** (+7 m 05 s) | ✅ reconciled, **price EXACT (684.20)** |
| **UTTAMSUGAR** | 15:22:18 | ⛔ none — last was **15:20:17** | ❌ **missed by 2 m 01 s** ⇒ finalised at next boot with a fabricated price |

**⛔ AND THERE IS NO SAFETY NET AFTER IT — PROVEN, ⛔ NOT ASSUMED:** the 15:45
`reconcile_positions` cron **did run** on 18-Aug (it wrote `position_reconciliation` id 18 at
`15:45:02.186`, `broker_qty=0 / system_qty=1 / MISSING_AT_BROKER`, `resolved_at` NULL) — ⭐ **it
DETECTED and did not finalise**, and the row was still `OPEN` at the 19:20:39 stop. ⇒ **between
the last in-hours cycle and the next boot, nothing closes the row.**

> 🔑🔑 **PROMOTED TO ITS OWN FINDING (Rama, 19-Aug ~12:1x — *"the sharpest thing in the boundary
> work"*): DETECTION AND RECONCILIATION ARE SEPARATE CAPABILITIES, AND THIS SYSTEM HAS THE FIRST
> WITHOUT THE SECOND.** `reconcile_positions` saw the divergence **within 23 minutes** of the
> 15:22:18 sell, named it correctly as `MISSING_AT_BROKER`, wrote it to a durable table — and
> **took no action**, leaving `resolved_at` NULL forever.
> ⇒ ⛔ **THIS IS WHY A LATER SCAN IS NOT A SAFETY NET, and it generalises past the cadence
> measurement:** adding *more* or *later* detectors cannot close DEFECT B or D, because the gap
> is not detection latency — ⛔ **it is that nothing consumes the detection.**
>
> ⛔⛔ **SEARCH WIDTH, STATED — THIS CLAIM IS NARROWED ON PURPOSE (Rama, 19-Aug ~12:0x).** I
> originally wrote *"the only component that FINALISES a delivery row is the CNC monitor."*
> ⛔ **I did NOT establish that exhaustively, and I am not entitled to it.** What I measured is
> **four paths** on this one incident: `cnc_gtt_monitor` (finalises — observed doing it twice) ·
> `reconcile_positions` @15:45 (detected, `resolved_at` NULL, did not finalise) · `eod_squareoff`
> @15:17 (*"0 open positions exited"*) · the boot-time startup reconcile (finalises, via the CNC
> monitor). ⛔ `eod_broker_reconcile` @15:58 and the 17:35 census were **NOT examined today** —
> they are cited from the standing record, ⛔ not measured here.
> ⇒ 🏷️ **THE SUPPORTABLE CLAIM: *"across the four paths measured on this incident, only the CNC
> monitor finalises; the others detect or no-op."*** ⛔ **The stronger architectural statement —
> *"the CNC monitor is the ONLY finaliser in the system"* — is UNVERIFIED and needs its own
> exhaustive sweep of every writer to `trades.status`.** ⭐ It is worth doing; ⛔ it was not done
> today and must not be reported as if it were.
> ⚠️ ⭐ **Even narrowed, this is worth more than the boundary itself** — the boundary is a fact
> about one code path; this is a fact about how detection and action are wired.

### C · ⭐ **THE MITIGATION RAMA CAN USE TOMORROW — ZERO CODE. ⛔ AND IT IS NOT A CLOCK RULE.**
Because the boundary **moves**, a clock rule alone is fragile. ⭐ **A confirmation rule is not:**

> 🔑 **① Close any delivery position manually BEFORE ~15:00 IST — ⛔ A BUFFER, NOT A GUARANTEE.**
> ~~"That guarantees at least one full in-hours cycle runs afterwards"~~ — **CORRECTED 19-Aug
> ~12:1x: it guarantees nothing.** The last cycle's clock time **moves** (15:20:17 on 18-Aug,
> ~15:18:30 projected today), and a late boot, a shortened session or a changed cadence moves it
> further. ⭐ ~15:00 buys **~18 minutes of margin** against the earliest plausible last cycle —
> ⛔ margin is not a guarantee, and ① must never be relied on alone.
>
> 🔑 **② THEN CONFIRM IT LANDED — ⭐ THIS IS THE REAL CONTROL, because it observes the path
> directly rather than predicting it.** ⛔ **A generic GTT-exit alert is NOT confirmation.** The
> confirmation must match **ALL THREE**:
> **(a) `source_module` = `cnc_gtt_monitor`** · **(b) the title names THE SYMBOL just closed**
> (`[LIVE] GTT exit — <SYMBOL>`) · **(c) its timestamp is within ~16 minutes of the manual
> close** (one cycle at the measured ~15 m 08 s, plus slack).
> ⇒ ⭐⭐ **IF NO ALERT SATISFIES ALL THREE WITHIN ~16 MINUTES, THE CLOSE IS `NOT CONFIRMED BY THE
> CNC-MONITOR PATH`.** ⛔ **NOT "not reconciled"** — ⭐ this whole finding separates **detection**
> from **reconciliation**, and ⛔ it would be self-defeating to replace one overclaim with
> another. The alert's absence is evidence about **one observed path**, ⛔ not proof that no
> component anywhere acted. ⭐ What the operator actually learns is: *"the path that finalises
> delivery rows in every case I have measured did not report this one"* — which is enough to act
> on, and ⛔ is not a claim about the whole system.
>
> 🔴 **CORRECTION — MY OWN EVIDENCE ROW WAS WRONG, AND IT IS THE EXACT ERROR THIS INVESTIGATION
> EXISTS TO AVOID.** Caught by **ChatGPT, 19-Aug ~12:1x**; ⭐ **verified here before accepting.**
> I originally cited *"Measured both times: MMFL `18-Aug 14:49:53.788` · UTTAMSUGAR `19-Aug
> 08:15:40.229`"* as evidence **for** this practice.
> ⛔ **UTTAMSUGAR's `08:15:40.229` is NOT a confirmation of the 15:22:18 close.** It is **today's
> BOOT-TIME CLEAR — the fabricated-price event itself**, fired **~17 hours** after the close and
> carrying `exit_price 290.32` against an actual `290.10`. Under criterion **(c)** it fails by
> roughly a thousand minutes.
> ⇒ ⭐ **MMFL `14:49:53.788` is the ONLY genuine example. UTTAMSUGAR is the COUNTER-EXAMPLE** —
> the case where rule ② would correctly have raised the alarm at ~15:38 on 18-Aug.
> 📌 **Filed to `WC-PATTERN` as a sixth instance, and the first of the day that is MINE:** ⛔ a
> timestamp cited as evidence for a claim it does not support. ⭐ **`SOURCE WINS` applies to my
> own write-ups too.**

⭐ **Why ② beats ① on its own:** it is an **observable positive confirmation** on an existing
alert path, so it is immune to the drift, to a late boot, to a holiday-shortened session and to
the cadence changing. ⛔ ① alone is a deadline against a moving target.
### 🔴 **THE SCOPE LIMIT — ⛔ READ THIS BEFORE TREATING ①+② AS COVER**
📌 **Elevated and sharpened 19-Aug ~12:0x on Rama's instruction.** ⚠️ **A one-line version of
this was already present as a trailing caveat below — ⛔ under-weighted, where it could be read
past. It is the operator-facing half and it belongs here, not in a footnote.**

⛔ **① AND ② BOUND *OPERATOR-INITIATED* CLOSES ONLY.** Both begin with *"Rama closes a
position"*. ⛔ Neither has any purchase on a close he did not initiate.

🔴 **THIS SECTION WAS OVERSTATED AND IS NARROWED — 19-Aug ~12:2x.** ~~"AND THE CASE THAT
ACTUALLY HAPPENED IS THE UNCOVERED ONE … the `15:22:18` sell was externally initiated … origin
remains NOT DETERMINED … no operator rule reaches it."~~ ⛔ **FALSE.** **Rama closed UTTAMSUGAR
himself** (Positions → ⋮ → Exit), as he closed MMFL. ⇒ ⭐⭐ **①+② DO cover the case that caused
this investigation — it was a manual close all along.**

✅ **AND RULE ② WOULD HAVE CAUGHT IT.** Close executed `15:22:18` (contract note); the last
in-hours cycle had already run at `15:20:17`, so **no confirming alert could arrive**; ⇒ at
`15:22:18 + 16 min = ~15:38` on **18-Aug** the rule fires and Rama learns that evening — ⛔
instead of from a contract note the next morning. ⭐ Rule ① would have prevented it outright
(he closed at 15:22, after the day's last cycle).

⇒ 📌 **WHAT REMAINS GENUINELY UNCOVERED IS NARROWER: RMS square-offs and true broker-side
events** — exchange actions, corporate actions, a broker-initiated liquidation. ⛔ Nobody has
observed one of those on this account, so the residual is **real but unquantified**, ⛔ not
demonstrated.
⚠️ **STILL NOT A CONTROL, and that is unchanged:** ①+② are **operator practice** — nothing
enforces them, nothing alarms when they are skipped, and they alter **no code**.
⛔ **A/B/C/D remain exactly as open as before**; ⭐ what changed is that the practice's coverage
is **better** than this section first claimed, ⛔ not that the defects are smaller.

## ADDENDUM 11 — **`WC-PATTERN` #7: THE ANSWER WAS IN THE REGISTER AND I TRUNCATED IT.**
Added **19-Aug-2026 ~12:25 IST**. ⛔ No design, no implementation, no further investigation.

### A · 🔴 THE CORRECTION, AND ITS SOURCE
**Rama, 19-Aug ~12:2x, verbatim:** *"The 15:22:18 origin is DETERMINED — it was Rama, and he
told us at 19:15 yesterday: he closed both CNC positions manually via Positions → ⋮ → Exit,
MMFL at ~14:30 and UTTAMSUGAR at ~15:28."*

⇒ ⛔ **"externally initiated / origin NOT DETERMINED" is WRONG and has been struck through in
both places it appeared** (§B ③ of ADDENDUM 9's B-root, and the SCOPE LIMIT section). ⭐ It was
accurate as *"not the system's own order"* and **wrong as *"unknown"***. 📌 `_resolve_exit_price`'s
docstring covers it under its **second** clause — *"manual close via terminal"* — ⛔ not RMS.

### B · ⛔⛔ **AND IT WAS IN THE DURABLE RECORD ALL ALONG — I MEASURED WHERE, RATHER THAN ACCEPT "we reasoned around it"**
Rama's framing was *"the operator's own account was in the record from 19:15 last night, and
three of us reasoned around it for four hours instead of reading it."* ⭐ **I checked whether
that is literally true, and it is — with a sharper and more damning mechanism than "we did not
read it".**

🔑 **`MASTER_REGISTER.md:708`, row `N18-10`, written 18-Aug, contains VERBATIM:**
> *"…**MMFL `14:34:25`** (**Rama exited ~14:30** ⇒ an in-hours cycle ran AFTER it ⇒ `CLEANED`,
> finalised `14:49:53`) vs **UTTAMSUGAR `15:20:17`** — its SL triggered **`15:25:25`**, **Rama
> exited ~15:28**, market closes **15:30**, next cycle due **~15:35** ⇒ the gate returned."*

⇒ 🔴 **THE REGISTER SAID "Rama exited" — TWICE — AND I READ THAT ROW THIS MORNING.**
⛔⛔ **AND I DESTROYED THE EVIDENCE MYSELF: I printed the register tail through
`cut -c1-160`.** `N18-10` is a ~2,600-character row; the phrase *"Rama exited ~15:28"* sits far
past character 160. **My own truncation removed the answer**, and I then spent four hours
deriving *"externally initiated / origin NOT DETERMINED"* from code and logs — a conclusion the
register **contradicted in plain text** the whole time.

⭐⭐ **THE LESSON, AND IT IS MORE SPECIFIC THAN `SOURCE WINS`:** ⛔ **a convenience filter applied
while READING evidence is itself a measurement decision, and it can silently delete the
answer.** `cut`, `head`, `| head -5`, a truncated grep — each is a **narrowing of search width
that never announces itself.** 📌 This is the same family as the standing rule *"an absence
needs a check wide enough to have found the thing"* — ⭐ here the check was wide enough and
**I clipped its output.**
📌 It also re-earns `M8` (*read the map first — applies to your OWN notes too*): I read `N18-16`
in full because I grepped for it **by name**, and read `N18-10` truncated because I only
listed it. ⛔ **The row I read carefully answered a question I already had; the row I skimmed
answered the one I did not know I had.**

### C · ⭐ THE CORRECTION MAKES THE FINDING BETTER, ⛔ NOT WEAKER
- ✅ **①+② DO cover the case that caused this investigation** — it was a manual close.
- ✅ **Rule ② would have fired at ~`15:38` on 18-Aug**: close `15:22:18`, last in-hours cycle
  already past at `15:20:17`, so no confirming alert could arrive within 16 minutes.
- ✅ **Rule ① would have prevented it outright** — he closed at `15:22`, after the day's last cycle.
- 📌 **What remains uncovered is narrower: RMS square-offs and genuine broker-side events.**
  ⛔ None has been observed on this account ⇒ **real but unquantified**, ⛔ not demonstrated.
- ⛔ **A/B/C/D are exactly as open as before.** ⭐ The practice's *coverage* improved; ⛔ the
  defects did not shrink.

### D · ⚠️ A SECOND CORRECTION THIS SURFACES — **`N18-10`'s EVENT ORDER IS WRONG**
`N18-10` reads *"its SL triggered `15:25:25`, Rama exited **~15:28**"* — ⛔ **that ordering is
impossible**, because the SL leg was rejected for *"Insufficient stock holding … Holding
quantity: 0"*, which requires the position to be **already gone**.
✅ **The contract note settles it:** the sell executed **`15:22:18`** (trade `608618503`), *then*
the GTT triggered `15:25:25` and was rejected. ⇒ **Rama's `~15:28` is recall slack of ~6 minutes
— ⛔ NOT a discrepancy, and his own characterisation.** 📌 **The register's ORDER should be
corrected when `N19-*` is written; the execution time is the contract note's, ⛔ not the
recollection's.**

### E · `WC-PATTERN` NOW READS SEVEN
| # | wrong call | refuted by |
|---|---|---|
| 1 | the alarm is mis-scheduled (TZ class) | two clocks 5 s apart; target epoch = 11:30:00 IST |
| 2 | the drift *"reconciles exactly … could have gone red"* | stale `expected`; balanced by cancellation |
| 3 | **A** — *"the system already makes that call"* | it fires **88 ms after** the decision |
| 4 | **B** — *"query the prior session's trades"* | Kite is day-scoped; no order id existed |
| 5 | **D** — *"pass the business date, one argument"* | `GENERATED ALWAYS … STORED` |
| 6 | **(mine)** UTTAMSUGAR's `08:15:40` alert cited as confirmation evidence | it is the fabricated-price event, ~17 h late |
| 7 | **(mine)** *"externally initiated / origin NOT DETERMINED"* | 🔴 **`MASTER_REGISTER.md:708` said *"Rama exited"* — and I truncated the row at 160 chars** |

⭐ **Two of seven are mine, and #7 is the worst of the set**: ⛔ 1–5 were reasoning outrunning
source; **#7 was source in hand, clipped before reading.**

## ADDENDUM 12 — **R4 SCORED, WITH THREE BOUNDARIES RAMA SET ON THE WORDING.**
Added **19-Aug-2026 ~15:20 IST**. ⛔ Observation only; ⛔ nothing run, fixed or adjusted.

### A · ⚠️ **"MANUAL STOP NOT OWED" IS A PREDICTION, ⛔ NOT AN OBSERVATION**
**Rama, verbatim:** *"'Manual stop NOT OWED' stays conditional — it is a prediction from the
15:15–15:17 gate inputs, ⛔ not an observation of a 17:35 event that hasn't happened. ⭐ The
15:17 `eod_squareoff` also hadn't run when you measured. If no shutdown by ~17:40, the stop
becomes owed."*

**THE GATE INPUTS, MEASURED `15:15`–`15:17`:** `count_active_positions()` = **0** (exact statuses
`OPEN`/`PARTIAL`/`PENDING_FILL`, `state_store.py:653`) · `EXITING` = **0** (M-C8: the gate is
EXITING-blind) · delivery book **flat** · all four of today's trades terminal.
⛔ **The `15:17` `eod_squareoff` had NOT yet run at the time of measurement** — a late fill would
change the input. 🏷️ **STATUS: `PREDICTED NOT OWED · ⛔ UNOBSERVED`. Scored at ~17:40.**

### B · ⛔ **THE 15:15 SOFT_KILL IS NOT EVIDENCE ABOUT THE 17:35 SELF-EXIT**
**Rama, verbatim:** *"⛔ The 15:15 SOFT_KILL is not evidence about the 17:35 self-exit. ⭐ Two
separate events; ⛔ do not let the first stand in for the second."*
📌 `15:15:01.597` `SOFT_KILL reason=circuit_breaker_force_close_15:15 triggered_by=order_monitor`
is the **routine daily circuit breaker**. ⛔ It says nothing about whether `eod_self_exit` will
fire at 17:35 — that gate is `count_active_positions() == 0` **re-evaluated then**, ⛔ not now.

### C · 🏷️ **TICK 2 — `MECHANISM LIVE / EFFECT NOT TESTED`. ⛔ NOT PASS, ⛔ NOT FAIL.**
**Rama, verbatim:** *"All five rejects were same-book and the old account-wide code would have
rejected every one — zero discriminating evidence. ⛔ Do not read a clean day as success."*
**FINAL FOR 19-Aug:** signature `", per pipeline"` **5** · `{book}` = `in the intraday book` **×5**
· `account-wide` **0** · `in the delivery book` **0** · gate-1 rejects **5**, all same-book.
⇒ ✅ the resolver returns a real book (**not inert**) · ⛔ **no cross-pipeline admission occurred**,
so the behaviour change is **unexercised**. Entry window closed **15:00** ⇒ ⛔ no further sample
today.

### D · ⭐ THE DRIFT RECONCILIATION — AND WHY THE SECOND PASS IS THE ONE THAT COUNTS
**Rama, verbatim:** *"Your second-pass correction on the drift is the good work here: the 09:15
SYNC had already erased UTTAMSUGAR's −5.03, so only the post-SYNC −13.29 applies. ⭐ The bucket
sum 7,422.60 + 3,481.41 = 10,904.01 confirms it independently — that is what makes it a
reconciliation rather than an assertion."*

| term | value |
|---|---|
| `expected` (post-SYNC 10,917.30 less post-SYNC realised −13.29) | **10,904.01** |
| `actual` — fresh `get_margins`, flat `15:15:38`→`15:16:08` | **10,611.91** |
| **delta** | **292.10** |
| DEFECT A over-count | **294.60** |
| used margin (book flat) | 0.00 |
| P&L timing (system booked −13.29; broker moved −10.79) | **−2.50** |

⛔ **MY FIRST PASS WAS WRONG AND IS RECORDED AS SUCH:** I subtracted the day's full **−18.32** and
got `10,898.98`, which did **not** reconcile. ⭐ It could not — **the 09:15 SYNC had already
erased UTTAMSUGAR's −5.03 (DEFECT C)**, so only the **−13.29** booked *after* it applies.
🔑 **The independent bucket sum `7,422.60 + 3,481.41 = 10,904.01` is what turns this from an
assertion into a reconciliation** — ⭐ it could have disagreed, and it did not.
⇒ **A is unchanged at ₹294.60 and remains the ONLY anomalous term.**
📌 G3 last alarmed `10:12:35` — **stale by ~5 h**; the delta above is **computed**, ⛔ never read
off the alarm.

### E · TOMORROW'S 08:15 — THE CLEAN TEST FOR PREDICTION ②
🟢 **The confound named this morning did NOT materialise: the delivery book is FLAT** (0 CNC open,
0 `ACTIVE` GTT) ⇒ **prediction ② is SCOREABLE.**
**The call, unchanged:** post-`INIT` `expected` **equals** broker net; first `G3` delta **inside
the ₹50 tolerance**. **Falsifier:** if `expected` still exceeds broker net, the over-count is
**PERSISTENT, ⛔ not per-session** — a materially larger defect than DEFECT A.
⛔ **DO NOT touch the threshold or the prediction before measuring.** ⛔ No manual correction,
no SYNC, no ledger edit.

## ADDENDUM 13 — **② SCORED: `CORROBORATED`. THE OVER-COUNT DID NOT SURVIVE THE SESSION BOUNDARY.**
Added **2026-08-20 ~08:30 IST**. ⛔ **No edit above the boundary.** ⛔ Nothing run, restarted,
synced, corrected or fixed — every figure below is either the running process's own logged
value, a `sqlite3 …?mode=ro` read, `systemctl show`, or a line of deployed source.

### A · BOOT STATE — ⭐ CLEAN, ⛔ NO `HARD_KILL`
| item | measured | source |
|---|---|---|
| start | **`2026-08-20 08:15:27 IST`** | `systemctl show -p ExecMainStartTimestamp` |
| PID | **`4103096`** | `-p MainPID` |
| state | **`active` / `running`**, `NRestarts=0`, `Result=success` | `systemctl show` |
| scenario | `COLD: new day (prev=2026-08-19, today=2026-08-20)` `08:15:28.190` | `system_2026-08-20.log` |
| **`HARD_KILL`** | 🟢 **NONE.** `grep -i kill` over today's log returns **exactly 3 lines** — the two below plus `check_kill_switch_present: OK` | log |
| prior-day `SOFT_KILL` | `08:15:28.184` **CRITICAL** *"KILL SWITCH ACTIVE AT STARTUP: state=SOFT_KILL reason=circuit_breaker_force_close_15:15 triggered_by=order_monitor"* | log |
| **auto-clear** | ✅ `08:15:28.189` **WARNING** *"Kill switch auto-cleared: prior SOFT_KILL from 2026-08-19 … new day 2026-08-20 starts clean (HEADLESS); audited to system_events"* | log |

⇒ ⭐ **The boot did not hard-kill.** The routine 15:15 kill cleared on the date rule, `5 ms` after it was read.

### B · 🔑 POST-`INIT` EXPECTED vs BROKER NET — **EQUAL TO THE PAISA**
| | value | measured at | source |
|---|---|---|---|
| **broker net** | **`10,609.10`** | **`08:15:36.054`** | `zerodha_adapter get_margins call_end … result_summary:"net=10609.1"` — the `initialize` call's own broker read |
| **post-`INIT` expected** | **`10,609.10`** | **`08:15:36.063`** | `fund_manager.initialize` `intraday_avail=7426.37` + `positional_avail=3182.73` = `total=10609.1` |
| **post-rehydrate expected** | **`10,609.10`** | **`08:15:36.064`** | `fund_manager.rehydrate_complete` `total=10609.1`, `replayed_trades=0`, `replayed_pnl_rows=0`, `daily_pnl=0.0`, `anomaly_count=0` |
| `fm_ledger` | **ONE row all day** — `10934 · 08:15:36.059667 · INIT · 10609.1 · both · 0.0 → 10609.1 · fm_73da922e3de8 · "initialize with broker_balance=10609.1"` | `08:26 read` | `sqlite3 -readonly` |

🔑 **`rehydrate_carry` DID NOT FIRE WITH A CARRY, AND ITS SILENCE IS DIAGNOSTIC — ⛔ not merely
uninformative.** `fund_manager.py:1836-1838`: `self._total += self._positional_carry` runs
unconditionally, but the `fund_manager.rehydrate_carry` log line is guarded by
`if self._positional_carry:`. ⇒ **its absence entails `_positional_carry == 0.0`.** ⭐ And the
conclusion does not rest on that inference alone: the *post-rehydrate* total was itself logged
at `10,609.10`, equal to broker net, whichever branch ran.
⇒ ⭐ **This is exactly the predicted alternative:** *"either no `rehydrate_carry` line appears
at all or it carries `positional_carry: 0`."*

### C · ⭐ THE CONFOUND DID NOT MATERIALISE — **DELIVERY BOOK FLAT, BROKER-MEASURED**
⛔ Not inferred from DB rows alone (`counts_db_rows_not_broker_06aug`):
- **`get_positions` → `0 positions`** — `08:15:36.169`, and on **every 15 s cycle since**; latest confirmed `08:22:09.107`.
- **`get_holdings` → `0 holdings`** — `08:15:36.270`.
- DB side, corroborating: `gtt_state` `ACTIVE` = **0**; `trades.status` vocabulary holds **no** `OPEN` / `PENDING_FILL` / `PARTIAL` / `EXITING` row at all (`FAILED 318 · CLOSED 216 · REJECTED 75 · CLOSED_MANUAL 50 · CANCELLED 9`).

⇒ ⭐ **`_positional_carry` had nothing legitimate to hold. The prediction is SCOREABLE.**

### D · 🔑 THE FIRST `G3` DELTA — **COMPUTED, ⛔ NOT READ OFF AN ALARM**
**Operands, from deployed source `orders/order_reconciler.py:3564-3593`:**
`expected = fm.get_snapshot().total` (`= self._total`, `fund_manager.py:1602`) ·
`actual = adapter.get_margins().net` · `delta = abs(actual - expected)`.

**The first `G3` cycle:** `order_reconciler started (poll_interval=15s)` `08:15:36.932` ⇒ first
cycle `get_positions 08:15:51.945` / **`get_margins 08:15:51.984 → 08:15:52.016`, `net=10609.1`**.

**`expected` at that instant = `10,609.10`**, established as: the process's **own post-rehydrate
emission** (`08:15:36.064`), plus completeness of the ledger over the intervening `15.9 s` — of
the five `self._total` write sites (`:477 :1326 :1449 :1837 :1871`), `:477/:1837/:1871` are boot-path
and already reflected in that emission, and `:1326` (`RELEASE_USED`) / `:1449` (`SYNC`) each write an
`fm_ledger` row **before** mutating; `fm_ledger` holds **no row after `10934`**.

> ### 🟢 **FIRST `G3` DELTA = |10,609.10 − 10,609.10| = ₹0.00**

**Tolerance in force at `08:15`: ₹50.00 FLAT.** `capital_drift_tolerance: 50.0`;
the `capital_drift_tolerance_pct: 0.10` widening applies **only** when `broker_margin_reliable`,
i.e. `_MARGIN_RELIABLE_OPEN 09:00 ≤ now < _MARGIN_RELIABLE_CLOSE 15:45` on a market day
(`order_reconciler.py:112-113, 3602-3628`) — **false at 08:15**. ⭐ So the ₹50 the prediction
names is the threshold that actually applied; ⛔ the percentage band did not silently do the work.

**Cross-check (⛔ not the measurement):** `reconciliation_log` rows for `2026-08-20` = **0**.
Yesterday's last was `id 7881 · 2026-08-19T17:15:48.904549 · CAPITAL_DRIFT ·
"Broker capital=10611.91 vs local=10904.01 delta=292.10 exceeds tolerance=50.00"`.

### E · 🏷️ **VERDICT — ② `CORROBORATED`. THE OVER-COUNT IS PER-SESSION.**
`₹0.00 ≤ ₹50.00` ⇒ the call lands: post-`INIT` `expected` **equals** broker net, and the first
`G3` delta is inside tolerance. **The single falsifier — *"post-INIT expected still exceeds
broker net"* — IS NOT MET.** 🟢 **DEFECT A does not survive a clean session boundary**, and the
**stale-carry root is corroborated**: `initialize` zeroes the carry unconditionally
(`:485-486`) and nothing rehydrated it, so the `₹292.10` of 19-Aug is gone at `08:15` on 20-Aug.

⛔ **AND IT WAS NOT MADE TO PASS:** no manual correction, no `SYNC`, no `fm_ledger` edit, no
restart — `NRestarts=0`, and the single ledger row is the boot's own `INIT`.

### F · ⛔ WHAT THIS DOES **NOT** ESTABLISH
1. ⛔ **It does not close DEFECT A.** A is *"`rehydrate_carry` re-adds margin the broker already
   returned"*. Today had **nothing to rehydrate** — a flat book is the condition under which A
   *cannot* express, ⛔ not a demonstration that A is repaired. **A re-arms the moment a delivery
   position is carried overnight.** ⭐ Today is the **control**, ⛔ not the cure.
2. ⛔ **It says nothing about DEFECT C** (`sync_from_broker` reconstructing from `cash + stale
   carry`). The 09:15 `SYNC` had **not yet run** at this measurement. With carry `0.0` it should
   be a no-op today — ⭐ that is a *further* prediction, ⛔ not a result.
3. ⛔ **It says nothing about DEFECT B or DEFECT D.**
4. ⚠️ **`expected` was not read directly out of the live process** — `capital_snapshot` (singleton,
   `id=1`) is **EMPTY**, so no independent in-process reader exists. The value rests on the
   process's own log emission + ledger completeness, stated in full in §D so a later reader can
   attack it.

### PROHIBITIONS OBSERVED
⛔ No fix, ⛔ no `SYNC`, ⛔ no ledger edit, ⛔ no threshold change, ⛔ no drift suppression, ⛔ no GTT
action, ⛔ no DB write, ⛔ no push, ⛔ no config change, ⛔ no service action. ⛔ No edit above the
boundary.
