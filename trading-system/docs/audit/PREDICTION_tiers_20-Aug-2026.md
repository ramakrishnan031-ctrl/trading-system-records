# PREDICTION — TIER THRESHOLDS 62/61 + MULTIPLIERS 0.85/0.75 (extract, INSTALL ⑥)

**Frozen 2026-08-20, ~08:50 IST, ⛔ BEFORE the gate result was known and ⛔ BEFORE any push.**
Unit: **`7297be7ec7f35699d4aea4a67e6d9642a84d25ea`** on `feat/tier-thresholds-extract-20aug`,
parent **`08b462ba175d904e8723ed34a13c956f0dd33679`** — `origin/main` measured **twice** at
08:22 IST (PC `git ls-remote` wire protocol + a raw `cat` of the VM bare repo's
`refs/heads/main`, no git binary). Worktree `…/scratchpad/tiers-work`.

⚠️ **BASE-STALENESS CLAUSE.** Frozen against `08b462b`. **If `origin/main` moves before the
push, this prediction MUST be re-frozen** — ⛔ do not push against a prediction written for a
different base. ⭐ Re-measure at the push window; ⛔ never from this banner.

> ## 🔑 **THIS UNIT HAS A REAL PRESENCE SIGNATURE *AND* A REAL BEHAVIOURAL ONE — and both have controls that have held for ten consecutive trading days.**
> ⛔ That is the opposite of its sibling `n907`, which is `NOT TESTED` by construction.

---

## §A — WHAT IS BEING INSTALLED, AND WHAT IT IS NOT

**Four values, two files, ⛔ no source file.**

| file | key | from | to |
|---|---|---|---|
| `config/scoring_weights.yaml` | `high_score_threshold` | **80** | **62** |
| `config/scoring_weights.yaml` | `medium_score_threshold` | **65** | **61** |
| `config/system_config.yaml` | `position_sizing.tier_multipliers.MEDIUM` | **0.70** | **0.85** |
| `config/system_config.yaml` | `position_sizing.tier_multipliers.LOW` | **0.50** | **0.75** |

⛔ **IT IS NOT** `3cf3729` — that commit does not apply to this base (two of its four files are
absent at `08b462b`, and its `delivery_tier_multipliers` hunk targets a block that does not
exist here). ⛔ **NOT** `65b7196`'s allocation model · ⛔ no `.py` · ⛔ **no DB migration** ·
⛔ no schema · ⛔ no `max_qty` · ⛔ no value cap · ⛔ no loss limit · ⛔ no concentration cap ·
⛔ `min_pass_score` is UNTOUCHED at 60, so **the entry gate does not move — only the SIZE of a
signal that already passed.**

## §B — THE PRESENCE SIGNATURES, AND THEIR CONTROLS

⭐ **A presence signature must be an artifact that could not exist before the change.** This
unit has three, and each control was measured **before** the change could fire.

| id | signature | control, measured 2026-08-20 before any push |
|---|---|---|
| **S1** | the 08:15 boot logs `position_sizing.mode` with `tier_weights:{"HIGH":1.0,"MEDIUM":0.85,"LOW":0.75}` (`main.py:2523-2531`, `_tw = ps_cfg.tier_multipliers`) | today's boot logged **`{"HIGH":1.0,"MEDIUM":0.7,"LOW":0.5}`** at `08:15:36.064` |
| **S2** | a **new `config_snapshots` row** for `2026-08-21` whose `config_hash` ≠ `79932bde50fe…` | 🔑 **the last TEN snapshots — `2026-08-07` → `2026-08-20`, ids 28-37 — all carry the IDENTICAL hash `79932bde50fe10831bd50f09cc0211e11dd89ea4c9c97337ee325580bfe66c4d`.** Ten trading days, one hash ⇒ any move is unambiguous |
| **S3** | a `trades` row with **`tier_weight_applied` ∈ {0.75, 0.85, 1.0}** (`position_sizer.py:492/:532` → `order_manager.py:224/:256`) | 🔑 **those three values have NEVER appeared in the table.** Every valued row since `2026-06-22`: **`0.5` ×604** and **`0.7` ×1** (11-Aug, one trade). n=605 |

⭐ **S3 is the strong one:** it is not "a number changed", it is **a value the system has never
once produced in its entire recorded history**.

## §C — 🔑 THE INERT-VS-WORKING DISCRIMINATOR

🔴 **The card's question, asked and answered by measurement: does the changed value have a live
path that can exercise it in the window? — YES, end-to-end, on the deployed tree.**

```
config/scoring_weights.yaml  →  app_config.scoring
      →  main.py:2881  QualityScorer(weights=app_config.scoring)
      →  quality_scorer.py:122-131   high_thr / med_thr  →  tier = HIGH|MEDIUM|LOW
config/system_config.yaml    →  app_config.system.position_sizing
      →  main.py:2506-2510  PositionSizer(tier_multipliers={HIGH,MEDIUM,LOW})
      →  position_sizer.py:467  tier_mult = self._tier_multipliers.get(score_tier, 1.0)
      →  position_sizer.py:471  effective_mult = tier_mult * perf_weight  →  qty
      →  position_sizer.py:492  breakdown["tier_weight_applied"]  →  order_manager.py:256  →  trades
```

⭐ Corroborated **live** by today's own boot line and by 605 `trades` rows carrying the value.
⛔ **This is not "the key exists in a yaml".**

⚠️ **A TRAP DEFUSED IN ADVANCE.** The resolved config carries these key NAMES in **two** places:
`.scoring.high_score_threshold` (**the live path**) and `.system.v3_chain.high_score_threshold`
(**dormant** — the V3 chain is DEFAULT-OFF). This unit changes **only** `.scoring`. ⇒ after the
push, `.system.v3_chain` will still read **80/65**, and ⛔ **that is correct, not a failed
deploy.** `3cf3729` did not touch it either, and `config_loader.py:1225`'s v3 ordering check
still needs `80 > 65 > 60`.

## §D — 🔑 THE CALL

**On the first 08:15 boot after the push (expected `2026-08-21`):**

1. **S1 fires** — `tier_weights:{"HIGH":1.0,"MEDIUM":0.85,"LOW":0.75}`.
2. **S2 fires** — a `config_snapshots` row for `2026-08-21` with a hash ≠ `79932bde50fe…`.
3. **The boot does NOT fail.** `62 > 61 > 60` satisfies `config_auditor` `B5_..._live`
   (`Severity.BLOCK`) and `config_loader.py:2046`; `TierMultiplierModeCheck` only reports.
4. **S3 fires on the first entry of the day**, and 🔴 **`tier_weight_applied` is NEVER `0.5`
   again** on any trade sized under this config.

**Expected distribution of S3**, from 2,681 screener rows with `score ≥ 60` over the last 60
days: **≈72.8 % at `0.75`** (score 60), **≈0.5 % at `0.85`** (score 61), **≈26.8 % at `1.0`**
(scores 62-65). ⭐ Most first-trades should read **`0.75`**; a `1.0` is expected within days.

**EXPOSURE, the honest headline:** mean tier multiplier **0.50082 → 0.81740 = `+63.21 %`**
across those 2,681 rows. 🔴 **ON BOTH BOOKS** — see §F.

## §E — FALSIFIERS, each independently scoreable

| id | fires if | measured by |
|---|---|---|
| **T1** | after the push, `origin/main` ≠ `7297be7…` on either independent measure | VM bare ref `cat` + PC `ls-remote` |
| **T2** | either changed file differs PC vs VM by md5 | `md5sum`, PC side **from the ref's blobs** |
| **T3** | the VM deployed tree shows tracked drift vs the new HEAD | 🔴 `GIT_INDEX_FILE` temp-index **+ `update-index --refresh`** — see §G |
| **T4** | 🔴 the 08:15 boot **fails or hard-kills** | `systemctl show`, `system_<date>.log` |
| **T5** | the boot logs `tier_weights` still `0.7/0.5` | ⇒ the config was not read; the unit is **INERT** |
| **T6** | the `2026-08-21` `config_snapshots` row carries hash `79932bde50fe…` unchanged | ⇒ same as T5, from a second, persisted source |
| **T7** | 🔴 a trade is sized with `tier_weight_applied = 0.5` under the new config | ⇒ the sizer did not receive the values |
| **T8** | ⛔ a boot-time `CONFIG_UNACCESSED` warning newly lists `scoring.high_score_threshold` or `position_sizing.tier_multipliers` | ⇒ configured-and-inert |
| **T9** | 🔴 a `CapitalInvariantViolation`, a bucket `avail < 0`, or a `HARD_KILL` traceable to a larger position | `fm_ledger`, `system_<date>.log` |

⭐ **`NOT TESTED` is available for S3 alone** — if no entry fills on 21-Aug, S1 · S2 · T4-T6
still score, and S3 defers to the next trading day. ⛔ **`NOT TESTED` is NOT available for S1 or
S2** — the boot happens whether or not the market cooperates.
⭐ **`CANNOT DETERMINE` is available** if the service does not boot for an unrelated reason.

## §F — 🔴 THE SIDE-EFFECT ITS OWN AUTHOR DID NOT INTEND — **IT MOVES THE DELIVERY BOOK TOO**

`3cf3729`'s message says *"INTRADAY position sizes will rise"* and calls its delivery line
**"INERT BY CONSTRUCTION"**. ⭐ **True on `65b7196`'s tree. ⛔ FALSE on this base**, and the
difference is measured, not argued:

- `08b462b:config/scoring_weights.yaml` contains **zero** delivery keys (`grep delivery` → empty).
- `08b462b:config/system_config.yaml` has **no `delivery_tier_multipliers` block** at all.
- `08b462b:capital/position_sizer.py` holds **exactly one** multiplier dict —
  `self._tier_multipliers` (`:155`, `:445`, `:467`) — with **no delivery branch**.

⇒ 🔑 **there is no two-pipeline split on the deployed tree; delivery and intraday share one
threshold pair and one multiplier dict.** Delivery is **live** today: `delivery_enabled: true`,
`force_intraday_only: false`, `delivery_active: true`, and three positional strategies in
`will_trade`. ⇒ **delivery position sizes rise by the same +63 % class.**
⛔ **This is recorded in advance so it cannot later be discovered as a surprise.**

**M-C2 coupling (`N11-23`), re-derived under the multipliers this unit ships:**
`positional_bucket_pct 0.30 ÷ max_open_delivery_positions 3 = 0.10` = `max_concentration_pct
0.10`, **exactly**; this unit changes none of the three ⇒ **the identity HOLDS.** The tier
multiplier is applied **AFTER** `min(risk, capital, conc)` (`position_sizer.py:216-220`), so
raising it moves size **up toward** the 10 %-of-total cap and **never past it**. Identity holds
**and** positions move up ⇒ ⭐ **M-C2's reach SHRINKS**; at full size `3 × 10 % = 30 %` = the
entire positional bucket, so the 3-slot cap is self-enforcing. ⛔ **M-C2 is NOT implemented.**

## §G — 🔴 A FALSIFIER'S OWN INSTRUMENT WAS BROKEN, AND IT WAS FIXED BEFORE USE

**T3 (and `n907`'s `P3`) name the `GIT_INDEX_FILE` temp-index method.** Measured today on the
VM, against a tree known to be identical:

| method | result |
|---|---|
| `read-tree <sha>` → `diff-files` | 🔴 **1,309 files reported MODIFIED — a FALSE POSITIVE** (a fresh index carries no stat data) |
| `read-tree <sha>` → **`update-index --refresh -q`** → `diff-files` | ✅ **0** |
| independent control: `md5sum` of 6 tracked files vs their blobs at `08b462b` | ✅ **6/6 MATCH** |

⇒ ⛔ **As written, T3 would have fired falsely tonight.** ⭐ The `update-index --refresh` step is
now part of the method. 📌 *A red check needs its method verified — and this one was red for a
reason that had nothing to do with the tree.*

## §H — THE CEILING, STATED IN ADVANCE

⭐ The highest status reachable the morning after the push is **`DEPLOYED` + S1 · S2 confirmed**.
**`VERIFIED LIVE` requires S3** — a real trade carrying a multiplier the system has never
emitted. ⛔ Until an entry fills under the new config, the correct label is **`DEPLOYED, effect
NOT TESTED`**, ⛔ never *"working"*.
⛔ A day with no entry scores **`NOT TESTED` for S3** — ⛔ never a pass.

## §I — WHAT THIS PREDICTION DOES NOT CLAIM

⛔ It does **not** claim the new values are correct — they were calibrated by `3cf3729`'s author
against `65b7196`'s allocation model, which is **not deployed**. This unit lands them on the
**older** sizer. ⛔ It does not claim the +63 % is safe; it states it so the decision is Rama's.
⛔ It does not claim anything about `65b7196`, `7d1fd4e`, F6, controlplane or the GUI.
⛔ It makes **no** claim about `n907`, which is a separate unit with a separate gate and a
separate verdict — ⭐ **if one fails the other is neither cancelled nor rolled back.**

<!-- FROZEN-BOUNDARY — everything ABOVE this line is FROZEN. ⛔ No edit above it, especially if a call turns out wrong. Addenda go BELOW, appended only, each with its own timestamp. -->

## ADDENDA (append-only, below the boundary)

## ADDENDUM 1 — **GATED TWICE · REBASED TO `b80354c` FOR THE §8(D) ORDER · AND 🔴 THE GATE IS VACUOUS W.R.T. THE VALUES, PROVEN BY PLANTING.**
Added **2026-08-20 ~09:40 IST**, ⛔ **BEFORE any push.** ⛔ No edit above the boundary.
⛔ Nothing pushed, started, migrated or run on the VM.

### A · ⭐ THE BASE HELD — ⛔ NO RE-FREEZE OWED FOR THE CALLS
`origin/main` re-measured **two independent ways** at 08:22 (PC `ls-remote` + raw `cat` of the VM
bare ref) = **`08b462ba175d904e8723ed34a13c956f0dd33679`**, the freeze-time base. ⇒ every call in
§B–§F above stands. ⚠️ **The SHA moves (see §C); the CALLS do not.**

### B · 🧪 THE GATE — FOUR FULL RUNS, AND THE ARITHMETIC DECOMPOSES
Identical staging on all four: system Python **3.11.9**, pytest **9.0.3**, ⛔ no venv,
`config/instruments.csv` planted (md5 `a7b07623909e051cb624ad157cee1671`), `python3` shim,
**Git Bash**, raw rc **from pytest itself** by redirect (⛔ never a pipe).

| SHA | contains | rc | failed | passed | skipped | elapsed |
|---|---|---|---|---|---|---|
| `08b462b` | — (base) | **1** | 7 | 5,646 | 4 | 897.92 s |
| `d896968` | n907 | **1** | 7 | **5,654** | 4 | 917.59 s |
| `7297be7` | **tiers** (sibling) | **1** | 7 | **5,646** | 4 | 893.43 s |
| `b80354c` | n907 + **tiers** (SHIPPED) | **1** | 7 | **5,654** | 4 | 927.03 s |

- ✅ **`comm` BOTH directions, `b80354c` vs its parent `d896968`: 0 NEW · 0 disappeared · 7 common.**
  **Failure MESSAGES identical too**, ⛔ not just ids.
- ✅ Same for the sibling `7297be7` vs `08b462b`: **0 / 0 / 7**, messages identical.
- ✅ Tree fingerprint `d41d8cd98f00b204e9800998ecf8427e` **IDENTICAL at start AND end** of all four.
- ⭐ **CROSS-CHECK: `passed = 5,646 + 8 × (n907 present)`** across four independent runs. The `+8`
  is n907's own test file; **tiers contributes exactly `+0`, on BOTH bases.**
- 🏷️ **WORDING:** *no new failures — 7 known remain; 0 did not reproduce; raw rc retained.*
  ⛔ NEVER *"the gate passed"*, ⛔ NEVER *"set-identical"*.

### C · 🔑 THE SHIPPED SHA IS **`b80354c240b79177c62fefacb31d4884bb0464f0`**, ⛔ NOT `7297be7`
🔴 **WHY — A CONSTRAINT NEITHER THE CARD NOR THIS PREDICTION ANTICIPATED.** `d896968` (n907) and
`7297be7` (tiers) are **siblings**: both parented on `08b462b`, neither containing the other.
`git push --dry-run` with an explicit refspec calls **each** a clean fast-forward **on its own**
(`08b462b..d896968` rc 0 · `08b462b..7297be7` rc 0) — ⭐ **which is precisely how this trap gets
past a per-unit check.** The first push moves `origin/main`; the second is then **1 ahead / 1
behind** ⇒ **non-FF**, and ⛔ `--force` is prohibited.

✅ **RESOLVED IN DAYLIGHT, ⛔ not at 19:00.** §8(D) already fixes the order (**n907 first**), so
tiers was rebased onto `d896968`:
- **content proven identical to the sibling:** `range-diff 08b462b..7297be7 d896968..b80354c` →
  **`1: 7297be7 = 1: b80354c`**, and `patch-id --stable` **identical** on both
  (`f3d8297cb494b470f5476619d841f3a7af16dbf1`). Clean cherry-pick, ⛔ no conflict.
- **ancestry proven clean at `b80354c`:** `c39e799` · `9fdfe41` · `4f91784` · `071169b` ·
  `bfd6b5f` · `43f73b1` · `7649cd8` · `65b7196` · `3cf3729` · `7d1fd4e` · `5cdd7e9` — **all
  FALSE**; ⭐ with an **expected-TRUE control** (`d896968` **IS** an ancestor) proving the check
  could have been TRUE.
- **1 ahead of `d896968`, 0 behind.**

⛔ **THE VERDICTS REMAIN INDEPENDENT.** If n907 is refused, tiers keeps its sibling SHA `7297be7`,
which is separately gated above. ⛔ Neither unit's failure cancels or rolls back the other.
⚠️ **`T1` now reads against `b80354c`**, and `origin/main` must be re-measured **again** after the
first push — the second install's comparand is not the first's.

### D · 🔴 **THE GATE IS VACUOUS WITH RESPECT TO THE VALUES — PROVEN BY PLANTING, ⛔ NOT ASSUMED**
🔑 **Passed went `5,646 → 5,646`: ZERO test-count delta.** `3cf3729`'s own two test files were
dropped (absent at base, §A), so **nothing arrived to cover the change.** ⛔ That is consistent
with *"the suite does not exercise this at all"*, so a count-based non-vacuity claim is
unavailable. **Two deliberate regressions were planted into a throwaway worktree to find out
what, if anything, guards these values:**

| | plant | result |
|---|---|---|
| **control** | the unit's real values `62/61/0.85/0.75` | `rc=0` · **271 passed** |
| **P-1** | 🔴 a **WRONG VALUE**: `tier_multipliers.MEDIUM 0.85 → 0.99` (structurally valid) | 🔴 `rc=0` · **271 passed — byte-identical to control. NOTHING CAUGHT IT.** |
| **P-2** | a **BROKEN ORDERING**: `high_score_threshold 62 → 59` (`59 > 61` false) | ✅ `rc=1` · **5 failed / 47 errors** — `test_config_auditor` ×2 · `test_diary4_tier_multiplier` · `test_preflight` · `test_preflight_config_rest` |

⇒ 🔑 **THE SUITE GUARDS THE *STRUCTURE* OF THE TIER CONFIG AND PLACES ZERO CONSTRAINT ON THE
*VALUES*.** P-2 proves the ordering guard is real and fires hard — so the green is ⛔ not vacuous
in general. P-1 proves that **within a valid ordering, any multiplier passes**; the suite cannot
tell `0.85` from `0.99`.

⇒ 🔴 **THIS UNIT SHIPS A `+63.21 %` EXPOSURE CHANGE THAT NO TEST CONSTRAINS.** The only checks on
those numbers are the pydantic ordering validator (which passes) and human judgement.
⛔ **A reader seeing only *"7F / 5,646P, 0 new"* would take more comfort from this gate than it
can give.** ⭐ That is recorded here so the comfort is not taken.
✅ Config **restored and verified byte-identical** after both plants
(`b16c32b67c51151d8274e42153f20691` / `e147d5cb825712fadd593cf2cd033685`, `git status` clean).

### E · ✅ NON-VACUITY THAT **IS** AVAILABLE — THE CHANGE REACHES THE LOADER
`load_all(config/)` run on both trees, ⛔ not inferred from the yaml:

| key | base `08b462b` | unit |
|---|---|---|
| `scoring.min_pass_score` | 60 | **60** — untouched ✓ |
| `scoring.medium_score_threshold` | 65 | **61** |
| `scoring.high_score_threshold` | 80 | **62** |
| `system.position_sizing.tier_multipliers` H/M/L | 1.0 / **0.7** / **0.5** | 1.0 / **0.85** / **0.75** |
| `system.v3_chain.medium` / `.high` | 65 / 80 | **65 / 80** — dormant, ⭐ **correctly unchanged** |

⇒ ✅ the change is real and reaches the resolved config; ✅ `load_all()` **succeeds**, so the
ordering validators accept `62 > 61 > 60` and **the boot will not fail on config validation**;
✅ **§C's trap is confirmed in advance** — `v3_chain` stays at `80/65` and ⛔ that is NOT a failed
deploy.

### F · ⛔ WHAT THIS ADDENDUM DOES NOT DO
⛔ It does not change any call above the boundary. ⛔ It does not claim the values are correct —
§I already says they were calibrated against `65b7196`'s allocation model, which is **not
deployed**, and §D now adds that **no test would notice if they were wrong**. ⛔ It does not
lift the requirement for Rama's quoted go. ⛔ It makes no claim about `n907`.

## ADDENDUM 2 — **RAMA'S RULING: `HOLD`. + THE BAND CHECK ON THE TRADE RECORD, A THRESHOLDS-ONLY VARIANT MEASURED, AND A TRANSCRIPTION SLIP CORRECTED.**
Added **2026-08-20 ~10:05 IST**. ⛔ No edit above the boundary. ⛔ **MEASUREMENT ONLY — nothing
built, gated, committed, amended, deleted or deployed for this addendum.** ⭐ `b80354c` and
`7297be7` stand exactly as built (both `cat-file -t` = `commit`; branch and tag resolve).

### A · 🏷️ THE RULING — **`tiers` IS `HELD`, ⛔ NOT REFUSED**
**Rama, 20-Aug:** *"n907 GO tonight, tiers HOLD pending a clean measurement."* ⇒ this prediction
**does not score tomorrow**; its window opens on the first 08:15 boot after whatever variant is
eventually authorised. ⛔ **`NOT TESTED` by deferral, ⛔ never a pass.**
⚠️ **If a DIFFERENT variant ships (see §D), this prediction is frozen for the WRONG UNIT and
MUST be re-frozen** — its §A names four value changes; a thresholds-only unit changes **two**.

### B · 🔑 THE BAND-INVERSION CHECK, RUN AGAINST THE **TRADE RECORD** — ⛔ NOT THE SCREENER ROWS
**Why it was asked:** the register's `E-1` cites *band inversion* as one of three converging
lines on the entries; the concern raised was that Shape A′ gives **×1.00** to scores **62-65**,
the sub-band reported anti-predictive. ⭐ **Measured directly rather than reasoned about.**

**Base: 263 closed trades** (`trades ⋈ screener_results` on `signal_id`; status
`CLOSED`/`CLOSED_MANUAL`, `net_pnl` NOT NULL, `risk_amount > 0`), **`2026-06-17 → 2026-08-19`**.

| band | A′ gives | n | win % | total P&L | avg R | pooled R |
|---|---|---|---|---|---|---|
| **62-65** | ×1.00 | 48 | **43.8 %** | **+₹2.77** | −0.0996 | **+0.0123** |
| **60** | ×0.75 | 180 | **40.0 %** | **−₹171.10** | −0.1417 | −0.1489 |
| <60 (closed era) | — | 35 | 34.3 % | −₹21.71 | −0.1622 | −0.1084 |

⇒ ⭐ **Within the 60-65 operating band, the HIGHER score performed BETTER on every measure.**
The *"it sizes up the losers"* concern is **NOT supported by the realised record.**
✅ **REGIME CHECK — it could have gone the other way:** both bands span the same window
(60: `17-Jun→19-Aug`; 62-65: `22-Jun→19-Aug`) ⇒ ⛔ not two different periods compared.

🔴 **AND IT ESTABLISHES NOTHING POSITIVE. `z = +0.470`** on 21/48 vs 72/180 (pooled p = 40.8 %)
⇒ ⛔ **NOT distinguishable at 95 %**; 62-65 would need **≥ 27/48 (56.2 %)** wins to reach `z > 1.96`.
⚠️ **AND IT IS FRAGILE:** for 62-65, **avg R is NEGATIVE (−0.0996) while pooled R is POSITIVE
(+0.0123)** ⇒ the positive total is carried by a few **larger-risk** trades, ⛔ not by a broadly
better band.

🔑🔑 **THE SCOPE LIMIT THAT MATTERS MOST — THE TRADE RECORD *CANNOT* TEST BAND INVERSION.**
**Scores 50-54 have ZERO trades. ⛔ Not few — zero.** They sit below `min_pass_score: 60` and were
never traded. ⇒ **the inversion's BEST band exists only in screener/shadow rows**, and the
realised record is **structurally incapable** of confirming or refuting that half.
⚠️ **The two populations also disagree on the band they CAN both see:** the trade record puts
**60-65 at 40.8 % win / −0.1328 avg R (n=228)** against the inversion's **31 % / −0.27 R**. Same
band, different basis, materially different numbers. ⛔ **That gap is unexplained and must be
before either figure is leaned on.**
⛔ **BAND INVERSION CAVEATS, STATED: one regime · ~2 months · no forward confirmation. ⛔ It is
NOT settled, and ⛔ today's measurement does NOT settle it.**

### C · ⚠️ A TRANSCRIPTION SLIP CORRECTED — **THE DEPLOYED TRIPLE IS `1.0 / 0.70 / 0.50`**
The routing instruction carried **`0.70/0.70/0.70`**. ⛔ Wrong, and ⛔ **not cosmetic.**
**Measured THREE independent ways, all agreeing:**

| source | value |
|---|---|
| deployed `config/system_config.yaml` on the VM | `HIGH 1.0 · MEDIUM 0.70 · LOW 0.50` |
| the **running process's own** 08:15 boot emission | `tier_weights:{"HIGH":1.0,"MEDIUM":0.7,"LOW":0.5}` |
| the resolved `config_snapshots` row persisted at boot (id 37) | `{"HIGH":1.0,"LOW":0.5,"MEDIUM":0.7}` |

🔑 **WHY THE SLIP MATTERS: a FLAT triple is a DIFFERENT POLICY, ⛔ not a rounding difference.**
`0.70/0.70/0.70` ⇒ **HIGH/LOW spread `1.0000×` = TIERING SWITCHED OFF ENTIRELY** (mean `0.70000`,
`+39.77 %` vs today). ⭐ That is precisely the *"configured, started, inert"* class
[[tier_mapping_measured_09aug]] already names — measuring the slip would have measured a policy
nobody proposed.

### D · 📊 **THE THRESHOLDS-ONLY VARIANT, MEASURED — ⛔ NOT BUILT**
Thresholds **62/61**, `tier_multipliers` left at the **DEPLOYED** `1.0/0.70/0.50`.
Same **2,681** screener rows, score ≥ 60, last 60 days.

| variant | mean multiplier | HIGH/LOW spread | vs today |
|---|---|---|---|
| **TODAY** — thr 80/65, mult 1.0/0.70/0.50 | **0.50082** | **2.0000×** | — |
| **THRESHOLDS-ONLY** — thr 62/61, mult UNCHANGED | **0.63480** | **2.0000×** | **+26.75 %** |
| **SHAPE A′** — thr 62/61, mult 1.0/0.85/0.75 | **0.81740** | **1.3333×** | **+63.21 %** |
| *(routing-file slip 0.70/0.70/0.70, for the record)* | *0.70000* | *1.0000×* | *+39.77 %* |

| score | n | share | today | thr-only | Δ | A′ | Δ |
|---|---|---|---|---|---|---|---|
| **60** | 1,951 | **72.77 %** | 0.50 | **0.50** | 🟢 **+0.0 %** | 0.75 | +50.0 % |
| 61 | 12 | 0.45 % | 0.50 | 0.70 | +40.0 % | 0.85 | +70.0 % |
| 62 | 526 | 19.62 % | 0.50 | 1.00 | +100.0 % | 1.00 | +100.0 % |
| 63 | 4 | 0.15 % | 0.50 | 1.00 | +100.0 % | 1.00 | +100.0 % |
| 64 | 177 | 6.60 % | 0.50 | 1.00 | +100.0 % | 1.00 | +100.0 % |
| 65 | 11 | 0.41 % | 0.70 | 1.00 | +42.9 % | 1.00 | +42.9 % |

**THREE THINGS THE NUMBERS SAY:**
1. ⭐ **THRESHOLDS-ONLY PRESERVES DISCRIMINATION; A′ COMPRESSES IT.** Deployed spread `2.00×`;
   thresholds-only keeps it **exactly `2.00×`**; A′ flattens to **`1.33×`**. ⇒ **A′ does not merely
   raise size — it reduces the tiering's power to separate.** That is a POLICY change riding
   along with the fix.
2. ⭐ **THRESHOLDS-ONLY IS THE SEPARABLE CHANGE — the DEFECT fix without the POLICY change.** The
   measured defect is that HIGH at 80 was **unreachable** against a ceiling of 65 (max score = 65
   across 118,250 rows in 60 days). Thresholds-only repairs exactly that. ⛔ A′ also moves what a
   tier is WORTH — the half **no test constrains** (ADDENDUM 1 §D) and the half **calibrated
   against `65b7196`'s undeployed allocation model** (§I).
3. 📊 **It delivers `42.3 %` of A′'s increase and leaves `72.77 %` of the population UNTOUCHED.**
   Score 60 — the band that lost **₹171.10** over 180 closed trades — does **not move at all**.
   The whole increase lands on scores 62-65 (**26.37 %** of rows).

⚠️ **AND THAT LAST POINT CUTS BOTH WAYS — ⛔ stated, not resolved.** On the **trade record** (§B)
62-65 measured *better*, so concentrating there is favourable. On the **Band Inversion**
hypothesis 62-65 is the anti-predictive band, so concentrating there is worse. 🔑 **The two
sources disagree, and thresholds-only makes the bet MORE concentrated, ⛔ not less;** A′ spreads
it across both bands. ⛔ **No recommendation is made here between them — the disagreement in §B
is unresolved and that is the honest state.**

**UNCHANGED UNDER EITHER VARIANT:** ⭐ the **ceiling**. `max_concentration_pct 0.10 ×
₹10,609.10 = ₹1,060.91`; largest position **ever** taken = **₹963.30** (265 filled trades).
`tier_mult` applies **after** `min(risk, capital, conc)` (`position_sizer.py:216-220`) ⇒ **typical
size rises TOWARD the ceiling; ⛔ the ceiling does NOT move.** · validator holds (`62 > 61 > 60`)
· ⇒ still **BOTH BOOKS** — one `tier_multipliers` dict, no two-pipeline split on this base (§F).

### E · ⭐ **SEQUENCING — RECORDED SO TOMORROW DOES NOT RE-DERIVE IT**
🔑 **`b80354c` WAS BUILT ON TOP OF `d896968`, SO n907 LANDING TONIGHT COSTS TIERS NOTHING.**
**Measured:** `b80354c^` **==** `d896968` · `merge-base --is-ancestor d896968 b80354c` = **YES** ·
**1 ahead / 0 behind**. ⇒ **once `origin/main` = `d896968`, `b80354c` is STILL a clean
fast-forward. ⛔ NOTHING needs rebuilding, rebasing or re-gating when tiers is decided.**
⭐ Its gate (ADDENDUM 1 §B) was run **against `d896968` as the baseline** — i.e. against exactly
the tree that will be `origin/main` after tonight. ⛔ The gate does **not** go stale tonight.
⚠️ **BUT:** if the eventual ruling is **thresholds-only** (§D), that is a **different unit** —
new SHA, new gate, re-frozen prediction. `b80354c` is the Shape-A′ candidate only.
📌 `7297be7` (the sibling, parented on `08b462b`) is retained **unchanged** as the fallback for
the case where n907 does **not** ship.

### F · ⛔ WHAT THIS ADDENDUM DOES NOT DO
⛔ No edit above the boundary. ⛔ It does not score this prediction. ⛔ It does not build, gate,
commit, amend or delete anything. ⛔ It does not recommend a variant. ⛔ It does not settle Band
Inversion, and ⛔ does not treat today's trade-record numbers as settling it. ⛔ It makes no claim
about `n907`, which proceeds on its own gate and its own verdict.
