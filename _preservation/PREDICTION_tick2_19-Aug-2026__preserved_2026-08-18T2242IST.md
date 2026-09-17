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
