# F6 — BUILD CONTRACT + RUNNING BUILD LOG

**08-Aug-2026 · Opus 5 · authorised by DECISION CARD 01 (Rama, 07-Aug ~22:5x IST)**

> **AUTHORISATION, QUOTED VERBATIM (G1 rule — no quote block, no action):**
> > *"If we can move onto production please proceed"* — Rama, 07-Aug-2026 ~22:5x IST,
> > preceded by *"If we are ready to build now? then lets proceed"*.
>
> **SCOPE OF THAT SENTENCE:** ✅ BUILD F6 · ✅ the `CONTRARY_POSITION` one-line comment ·
> ✅ the `expected_alarms` fold.
> ⛔ **NOT AUTHORISED: DEPLOY. PUSH. Cancelling `330944932`. Touching MANINFRA. Any config flip.**
> Deploy is its own decision and gets its own card when the build and the full regression are green.

**Start state, measured:** PowerShell `Get-Date` = `2026-08-08 09:34:10` IST (Saturday) ·
`git status --porcelain` **empty** · `HEAD = 763b0f2` · **ahead 18** (docs-only, held).
Service **down** since 07-Aug 18:36:48 by Rama's manual stop. Both GTTs untouched.

---

## 1 · ASSUMPTIONS FROZEN

Stated so drift is detectable. Each carries how it was established.

| # | assumption | basis |
|---|---|---|
| A1 | `orders/cnc_gtt_monitor.py:464` `held[sym] = held.get(sym,0) + abs(int(qty))` is the defect | **(S)** read at HEAD this session, line-exact |
| A2 | `held == 0` (`:487`) is the **sole** door to `_finalize_gtt_exit` | **(S)** the ladder at `:486-523`, read in full |
| A3 | **Two** consumers read the same `held` — the F6 re-protect (`:489`) and auto-recreate (`:513`) | **(S)** design §1.2, re-verified at HEAD |
| A4 | `fm_ledger.reservation_id` **already exists as a column** (`core/schema.sql:528`) | **(S)** schema read this session |
| A5 | `trades.reservation_id` exists and resolves rid from trade_id | **(S)** `state_store.get_entry_commit_margin:2567-2572` |
| A6 | `system_events` is **never pruned** — absent from `DEFAULT_RETENTION` (`scripts/db_retention.py:63-70`) | **(S)** read this session |
| A7 | `reconcile()` has exactly two call sites, both on the reconciler's single poll thread (`order_reconciler.py:426` startup, `:676` cadence) | **(S)** grep, whole repo, `venv`+`tests` excluded |
| A8 | CHECK1's delivery skip is fed by `get_active_gtt_states()` — **`status='ACTIVE'` only** (`order_reconciler.py:855-863`) | **(S)** read this session |
| A9 | Paper nets by **symbol**; live Kite nets per **(symbol, product)** | memory `paper_cannot_exercise_class_26jul` |
| A10 | The golden reference trace (design §4, ASKAUTOLTD 06-Aug 10:47:46) must still pass afterwards | design §4 |

⚠️ **A11 — carried as UNVERIFIED, not as fact:** design §3's transient window (both endpoints
disagreeing mid-settlement) has **never been sampled**. The build treats it as *possible*; no
regression case can prove it exists.

---

## 2 · ACCEPTED DESIGN — D-1 + D-2 + D-3

⛔ **D-1 alone is a rejection criterion and this build does not offer it alone.**

**D-1 — the settled book is authoritative; a same-day CNC position is a *delta*.**
`held(sym) = holdings(sym) + max(0, cnc_position_qty(sym))`. Only a **LONG** delta is shares not
yet in the settled book. A **SHORT** delta is a sale `holdings()` has already applied — adding it
double-counts. Satisfies constraints 1, 2, 3, 6.

**D-2 — a processed exit becomes a recorded one-way fact, and BOTH consumers read it.**
🔑 **CHOSEN MARKER: the `gtt_state` rows for a trade whose `status` is `TRIGGERED`.**
Written at **OBSERVATION** (the instant the broker reports the GTT triggered), by a **conditional
UPDATE** (`… WHERE gtt_id=? AND status='ACTIVE'`) so exactly-once is enforced by SQLite, not by a
read-then-write. Structured (`trade_id` is indexed), durable, never un-set, never pruned.
`COUNT(*)` over it is the number of observed exits for that trade, and **re-protect is admitted
only on the first**. Both consumers consult it: the F6 branch *and* auto-recreate.

**D-3 — `reservation_id` onto `RELEASE_USED`, plus the second independent release path.**
`release_used` resolves the rid from `trades.reservation_id` and stamps it on the ledger row
(the column already exists — **no DDL**). The second release path is a new reconciler check that
closes an `OPEN` delivery trade whose broker position **and** holding are both absent across N
consecutive cycles — Invariant A's structural answer.

### 2.1 · The two "PROPOSED, NOT CHOSEN" items — CHOSEN NOW

**§12.1's split (a) LIFECYCLE / (b) AUDITABILITY — CHOSEN: build them TOGETHER, in this build.**
*Reason:* the split existed only because 06-Aug was an evening with a deploy deadline, and D-3 was
read as a schema change. Both premises are gone — there is no deploy in this card, and D-3 needs
no DDL (A4/A5). Splitting now would cost the one thing the split was meant to buy (a smaller blast
radius) while paying its full price twice: two regression runs over the same capital path, and a
window in which `_check7`'s latent false negative stays armed with F6 already changed underneath it.

**§14.4's `D-3 BEFORE PHASE E` ordering — CHOSEN: ADOPT as a hard ordering constraint, discharged
by this build.** *Reason:* D-3 lands here, so the constraint is satisfied rather than carried. The
rule stays written down (`docs/04_db_schema_reference.md` already carries it) because it is a
statement about any future change that queries closed reservations, not about this one.

### 2.2 · 🔴 THE DESIGN'S "D-2 ⇒ SCHEMA" CONCLUSION IS SUPERSEDED — and here is exactly why

Design **§12.3.1** concluded *"D-2 requires a new persisted marker ⇒ schema."* That conclusion was
**correct about `gtt_state.status` as it is written today and wrong as a general claim**, and the
difference is the whole of D-2:

- §12.3.1 measured that `status` is written **by the handler, recording what it DID** — `CLEANED`
  by the gated function, `TRIGGERED` by the failure branch — and correctly concluded that a marker
  written by the gated function cannot guard that gate.
- **D-2 changes the write discipline, not the column.** `TRIGGERED` becomes written at
  **observation**, before any branch decides anything, by a conditional UPDATE that cannot run
  twice. It then records **what was SEEN**, which is precisely what §12.3.1 said the column could
  not express — because nothing had ever written it that way.

⭐ **Changing when a value is written is not DDL.** The two consequences are a widened working set
and a widened CHECK1 skip, both **queries**. ⇒ **No schema change, and the card's prohibition and
the design's requirement are both satisfied.** ⛔ Recorded here rather than silently: a superseded
conclusion left standing is how the next reader re-derives the block.

---

## 3 · EXCLUDED SCOPE — explicitly

- ⛔ The **ATULAUTO** and **DIFFNKG** phantom rows are **NOT hand-closed**. No raw DB write.
- ⛔ **NO schema change.** No `schema_version` bump, no DDL, no migration entry.
- ⛔ **NO GTT cancelled** — `330944932` and `330856765` are untouched. MANINFRA is Monday's control.
- ⛔ The `abs()`-on-signed-quantity class at the **other sites is NAMED, not fixed** (§ log below).
- ⛔ **NO deploy, NO push.** No config flip. No service start/restart.
- ⛔ `_check_stuck_exiting`'s unguarded delivery path (memory `check1_skip_guards_3of4_05aug`) is
  **named, not fixed** — it is a CHECK1 defect, not an F6 one, and fixing it here would break
  one-fix-per-commit.

---

## 4 · ROLLBACK TRIGGER — the exact observation that stops or reverts

⛔ **Carried from the queue, not re-derived.**

**STOP THE BUILD (do not continue to the gate) if:**
1. the corrected BL-3 test **does not go RED on old code** — design §13.2: *if a corrected fixture
   does not go red, the correction is wrong*;
2. the T+1 regression case (case 3) **does not go RED on old code** — constraint 5;
3. the golden reference trace (§4 / case 1+2, same-day round trip) **regresses** — that would be
   breaking the common case to fix the rare one (constraint 6).

**REVERT THE CHANGE if, after the build:**
4. `pytest tests/unit tests/integration` shows **any NEW failure** outside the 9 enumerated in
   `docs/audit/rulings_1_2_verification_07aug2026.md` §8.12 — set-compare, ⛔ never count-compare;
5. any regression case shows a **duplicate side effect** — a second ledger row, a second GTT, **or a
   second alert**. ⛔ *"No side effects" includes notifications.*

**The revert is `git revert` of the build commits.** Nothing is deployed, so no VM action exists.

---

## 5 · REGRESSION LIST — 9 cases + the BL-3 fix

**Gate:** `pytest tests/unit tests/integration` — ⛔ **never** `run_tests.py`, ⛔ **never through a
pipe** (`D5.1`: capture `PYTEST_RC` into a variable and read it back separately).

| # | case | RED-first on old code? | 🧪 can PAPER exercise it? |
|---|---|---|---|
| **3.1** | **BL-3 fixture is vacuous** — `test_state_store.py:1944` inserts a `RELEASE_USED` row **with** a `reservation_id`, a shape production has produced **0 of 220** times | ✅ **REQUIRED — fix and run on OLD code FIRST** | n/a — store-level |
| 1 | same-day CNC **buy** (+1) still counts as held | ❌ no (must stay green) | ✅ yes |
| 2 | same-day CNC **sell** (−1) does **not** count as held | ✅ **yes** | ⚠️ **VACUOUS in paper** — paper nets by *symbol*, so it cannot present a `-1` CNC row beside a `holdings()` entry (A9) |
| 3 | **T+1 exit** — `holdings()=0`, CNC `positions()=−1` | ✅ **yes — constraint 5** | ⛔ **PAPER CANNOT EXERCISE** — no T+1 settlement exists in paper |
| 4 | **repeated monitor execution** after a successful exit | ✅ yes (would have caught the loop) | ✅ yes |
| 5 | **service restart** after a successful exit | ✅ yes (would have caught the phantom) | ⚠️ **PARTIAL** — restart is exercisable; the CNC re-reservation it races is not (R-4) |
| 6 | **operator cancels a system GTT** while the monitor runs | ❌ characterises current behaviour | ✅ yes (injected) |
| 7 | **STEADY STATE** — ten consecutive cycles after a release | ✅ yes | ✅ yes |
| 8 | **COMBINED** — restart immediately after release, then multiple cycles | ✅ yes | ⚠️ **PARTIAL**, as case 5 |
| 9 | **SPANS MIDNIGHT** — (i) continuous, (ii) restart; injected `now_fn`, scratch DB only | ❌ pins the clock/boot split | ⚠️ **PARTIAL** — the clock roll is exercisable; the delivery carry across the boundary is live-only |

⛔ **A vacuously-green paper drill is labelled as such and is NOT counted as a pass.** Cases 2, 3
are the ones where that matters: they are written against injected broker state, so they run in the
unit suite regardless of mode — but **no paper run proves them**.

---
---

# RUNNING BUILD LOG

*One file. Findings are logged here and batched — ⛔ they do not spawn a card, a review round, or
a document.*

## L0 · 08-Aug 09:3x — contract frozen; coding starts
Nothing deployed, nothing pushed, service still down, both GTTs untouched.

## L1 · Step 3.1 — the BL-3 test fixed FIRST, and it went RED on the old code ✅

⛔ **Ordering honoured: no production line was written before this passed.**

The vacuity was **not** in the reader. Design §13's inversion holds — `sum_fm_ledger_margin_delta`
is correct and **the DATA violates its contract** — so the fix moves the assertion onto the
**WRITER**, where it can actually fail. Three tests added to `test_fund_manager.py`:

| test | RED on old code | measured failure |
|---|---|---|
| `test_bl3_release_used_writer_stamps_reservation_id` | ✅ | `RELEASE_USED must carry reservation_id='753d0fd77d6742a9', got None` |
| `test_bl3_release_used_ledger_chain_nets_to_zero_by_reservation_id` | ✅ | `assert 5000.0 == 0.0` — the released reservation reports its **entire** margin as still held, exactly the **689.41341** measured on ASKAUTOLTD in production |
| `test_bl3_release_used_without_trade_id_degrades_not_raises` | ❌ by design | pins DEGRADE-not-BLOCK: a release must never be refused, the position is already realised at the broker |

⚠️ **One thing had to be fixed before the RED was even legible:** a failed assert skipped
`store.close()`, so Windows reported a tempdir `PermissionError` **on top of** the real failure.
`store.close()` moved into a `finally`. ⭐ **A RED you cannot read is not evidence.**

`test_state_store.py`'s original test is kept as a **reader** test with its scope stated in the
docstring, and a new `..._blind_to_unkeyed_release_used` characterises the blindness at production
shape — so "fixing the reader" can never be mistaken for the fix.

## L2 · The build, as landed

| file | change |
|---|---|
| `orders/cnc_gtt_monitor.py` | **D-1** `max(0, int(qty))` at the CNC-positions leg · **D-2** observation marker + the ladder rewritten around it + the auto-recreate guard (constraint 4) · **Invariant A** the second release path · M2 scoped to ACTIVE · the orphan sweep scoped to ACTIVE |
| `core/state_store.py` | `get_reconcilable_gtt_states` · `mark_gtt_state_triggered` (conditional UPDATE) · `count_observed_gtt_exits` · `clean_gtt_states_for_trade` · `get_reservation_id_for_trade` · **the one-way guard inside `set_gtt_state_status`** |
| `capital/fund_manager.py` | **D-3** `release_used` stamps `reservation_id`, resolved via `trades.reservation_id`, degrading to NULL + WARN |
| `orders/order_reconciler.py` | CHECK1's delivery skip moved onto the same working set |
| `capital/risk_engine.py` | the authorised `CONTRARY_POSITION` one-line comment (activation condition, at the source) |
| `docs/expected_alarms.md` | the authorised fold — new §11, the service-down-with-a-carry weekend |

### 🔴 THREE SEAMS FOUND BY TRACING, each of which would have been a live defect

1. **M2 would have SOFT-KILLED the system on the ordinary partial-fill path.** Widening the
   working set to ACTIVE+TRIGGERED means a normal re-protect leaves a trade with one TRIGGERED
   row **and** one ACTIVE row — and M2 rejects *">1 ACTIVE GTT for one trade"* with a SOFT_KILL.
   Scoped to ACTIVE rows. Pinned by `test_m2_soft_kill_is_not_tripped_by_a_normal_reprotect`.
2. **CHECK1's delivery skip would have DISARMED MID-EXIT.** It reads `get_active_gtt_states()`.
   Once TRIGGERED became durable, a trade mid-exit would have had no ACTIVE row, the skip would
   have released it, and CHECK1 could mis-mark a live delivery trade `CLOSED_MANUAL`. Both now
   read **one** classifier. Pinned by `test_check1_delivery_skip_and_monitor_share_one_working_set`.
3. **The orphan sweep would have read a TRIGGERED row as healthy protection.** Its contract is
   *"a system GTT we believe is FINISHED yet still live at the broker"*. Scoped to ACTIVE rows.

### 📌 TWO DECISIONS TAKEN AT THE CODE, recorded because neither is obvious

**(a) The D-2 marker is keyed on the TRADE, not the gtt_id.** Every re-protect mints a **new**
gtt_id, and on 06-Aug each replacement fired again within ~15 minutes — so a per-row marker would
have been fresh on every cycle and bounded nothing. `test_case7b` runs ten cycles with a
permanently-wrong holding and asserts **≤1** live GTT placed and that the alerting **stops**.

**(b) The second release path books NO exit price and NO P&L.** `_resolve_exit_price` falls
through *today's* broker trade book → LTP → entry proxy, and for a stranded trade rung 1 always
misses, so it would book a live quote for an unrelated moment straight into the daily-loss reader
and the expectancy corpus. ⭐ **A gap is a loss; a fabricated number is a corruption, and the
corruption is undetectable later.** It releases the capital (unambiguous — the margin reverses
from the persisted COMMIT row, not from any price), leaves `exit_price`/`net_pnl` NULL, writes
`pnl_delta = 0.0` exactly, and raises a CRITICAL naming the trade for manual correction.
🏷️ This does **not** retire design cost 5 — §15.0 states no branch of F6 avoids it. It refuses to
make it worse.

## L3 · §3.3 — the `abs()`-on-quantity class, NAMED not fixed

⚠️ **THE CARD SAYS "the other 5 sites". THE MEASURED COUNT IS 11, and the honest answer is that
NONE of them is F6's class.** Recorded as measured rather than forced to the expected number.
**Width:** whole repo, all `*.py`, `venv`/`sats`/`tests` excluded.

**F6's class is not "abs() on a quantity" — it is "two overlapping sources ADDED as though
disjoint".** `abs()` was the instance; the addition was the defect. On that test:

| site | verdict |
|---|---|
| `structure_exit_manager.py:428` | ✅ **no-op** — `abs()` on `trades.qty_filled`, a LOCAL column that is never negative |
| `kill_switch.py:1281` · `order_reconciler.py:3120` | ✅ **correct** — `abs(qty) > 0` / `== 0` is a *presence* test, and a short IS a position |
| `eod_squareoff.py:1487` · `:1525` · `order_reconciler.py:2185` · `:2291` | ✅ **correct** — magnitude used to SIZE a flatten order, which is what you want in both directions |
| `eod_squareoff.py:1079` · `:1613` | ⚠️ **adjacent, not the class** — dict comprehensions keyed by symbol: a second product for the same symbol **overwrites** rather than adds. Not F6 (no double-count), but it is the same *(symbol, product)* blindness paper cannot exercise |
| 🔴 `order_reconciler.py:2968` · `structure_exit_manager.py:631` | ⚠️ **NAMED — a genuinely related hazard.** Both take the magnitude of a **signed net position** and use it as *"how much is held"* to gate a SELL. A SHORT position would read as held, and selling into it would DEEPEN the short. Both are LONG-only paths today, so it is **LATENT, not live** |

⛔ **Not fixed here** — one fix per commit, and expanding a live-capital change beyond its
evidence is exactly what the design's rejection criterion is about.

## L4 · Also named, NOT fixed (found while tracing; ⛔ not chased)

- `order_reconciler._check_stuck_exiting` remains **unguarded** by the delivery skip — a CHECK1
  defect, not an F6 one.
- `closure_source` / `exit_mechanism` are still **empty** on a `GTT_EXIT` close (design §4
  recorded this and did not chase it; unchanged).
- `drift_handler.py:17`'s docstring still says the escalating set is *"`{"fund_manager"}`"* —
  **one** member — while the frozenset at `:66-70` has **three**. Doc/code divergence on a
  kill-path gate, already filed.

## L5 · 🔴 GATE FINDING — **THE REGRESSION RESULT DEPENDS ON WHICH SHELL LAUNCHES IT**

**The first full run came back `PYTEST_RC=1`, `29 failed / 5562 passed / 4 skipped` in 882.42 s,
against a written-down baseline of NINE.** ⛔ Twenty extra failures on a capital-path change is a
stop-and-diagnose, not a shrug — so it was diagnosed rather than labelled.

**SET-COMPARE FIRST (⛔ never a count-compare).** All **nine** §8.12 baseline failures were present
and unchanged. The extra twenty were **two entire families, neither of which appears in the
baseline at all**: `test_fix065_market_hours_guard.py` (17) and `test_t4_deploy_preflight.py` (3).

**ATTRIBUTION, BY EXPERIMENT rather than by prior.** The production changes were stashed
(`core/state_store.py`, `capital/fund_manager.py`, `orders/cnc_gtt_monitor.py`,
`orders/order_reconciler.py`, `capital/risk_engine.py`) and the two families re-run:

| | result |
|---|---|
| with the F6 changes | **20 failed, 10 passed** |
| with the F6 changes **removed** | **20 failed, 10 passed** — and the FAILED sets compare **IDENTICAL**, line for line |

⇒ structurally impossible for the change to have caused them. ⭐ **And "not mine" is not a
diagnosis, so the cause was found too:**

```
E  assert ('REJECT' in "W\x00i\x00n\x00d\x00o\x00w\x00s\x00 \x00S\x00u\x00b\x00s\x00y\x00s...
                       '<Distro>' to install.
```

Both families **shell out to `bash`**. The UTF-16LE interleaving and the *"'&lt;Distro&gt;' to
install"* text are **WSL's app-execution alias** answering instead of a shell — the scripts never
ran at all, and the tests asserted against WSL's error message.

| launcher | `bash` resolves to | those two families |
|---|---|---|
| **PowerShell** | `C:\Users\rama\AppData\Local\Microsoft\WindowsApps\bash.exe` (WSL alias, no distro installed) | **20 failed, 10 passed** |
| **Git Bash** | `/usr/bin/bash` | ✅ **30 passed** |

🔑 **THE RULE THIS ADDS TO THE GATE: run `pytest tests/unit tests/integration` FROM GIT BASH.** The
07-Aug baseline of 9 was produced from Git Bash; running the identical command from PowerShell
silently manufactures **20 phantom failures** with no hint that a shell resolution is the cause.
⛔ A gate whose answer changes with the launcher is not a gate until the launcher is part of it —
and the failure mode is the dangerous direction only by luck: this time it added noise, but the
same mechanism could just as easily have made a real failure look like the known set.
⚠️ ⛔ **This does NOT retire the 9** — they are unchanged, and none of them is environmental.

## L6 · ✅ THE GATE — re-run from Git Bash, and the set is EXACTLY the baseline

> ### 🏷️ **REPORTING CONVENTION — ⛔ NEVER WRITE "GATE GREEN" BESIDE `RC=1`.**
> ⭐ A production gate reporting a **non-zero exit code** next to the word GREEN will
> eventually be misread by someone in a hurry, and the person in a hurry is exactly who is
> reading it at 18:15 on a deploy evening. **The correct phrasing, used from here on:**
> **`REGRESSION ACCEPTED — zero NEW failures; 9 known baseline failures; RC=1 by baseline
> convention.`** ⛔ *Accepted* is a judgement with its basis attached; *green* is a colour.

```
PYTEST_RC=1     <- expected: the 9 known baseline failures. NOT "green".
9 failed, 5582 passed, 4 skipped, 281 warnings in 887.79s (0:14:47)
```
**⇒ REGRESSION ACCEPTED — zero NEW failures; 9 known baseline failures; RC=1 by convention.**

⛔ `PYTEST_RC` captured into a variable and read back separately (`D5.1`) — ⛔ never through a pipe.
⛔ `pytest tests/unit tests/integration`, ⛔ never `run_tests.py`.

**TRUE SET-COMPARE against `rulings_1_2_verification_07aug2026.md` §8.12 — all nine present, and
NOTHING ELSE:**

| # | the nine | today |
|---|---|---|
| 1 | `test_closure_source_contract::test_no_module_restates_the_vocabulary_literals` | ✅ present |
| 2 | `test_fix181::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active` | ✅ present |
| 3-4 | `test_instance_lock::p1` · `::p2` | ✅ present |
| 5-8 | `test_main::TestBl15WebhookSecretRequired…` · `TestContinueFromGate` ×3 | ✅ present |
| 9 | `test_phase17_batch2::test_fix077_flask_max_content_length` | ✅ present |

⇒ 🟢 **ZERO NEW FAILURES.** Rollback triggers **4** (a new failure outside the nine) and **5**
(a duplicate ledger row, GTT **or alert**) are **NOT** met.

### ⭐ AND THE PASS COUNT RECONCILES EXACTLY — an independent check, not a restatement

**5557 (07-Aug) + 25 = 5582 (today)**, and the 25 decompose with no remainder:
**21** (`test_f6_delivery_exit_predicate.py`) + **3** (BL-3 writer tests in `test_fund_manager.py`)
+ **1** (`..._blind_to_unkeyed_release_used` in `test_state_store.py`) = **25**.
⭐ This is the check that would have caught a test silently vanishing — a set-compare on FAILURES
says nothing about a test that stopped being collected.

⚠️ **ANTI-VACUITY, stated because a green gate is only evidence if it could have been red:** these
21 were run against the PRE-FIX code with the production changes stashed, and **17 of the 21 went
RED**, case 3 failing with `['recreated:ATULAUTO'] != ['gtt_exit:ATULAUTO']` — the defect
reproduced exactly. The 4 that stayed green there are the must-not-regress guards (same-day buy,
operator cancel with the holding intact, M2, and the golden reference trace).

## L7 · 🔒 STATUS, LABELLED — and what is explicitly NOT true yet

🏷️ **`<BUILT>` — ⛔ NOT DEPLOYED, ⛔ NOT PUSHED, ⛔ NOT VERIFIED LIVE.**
Deploy is a separate decision and gets its own card.

⛔ **THE §15.2 RETIREMENT CHECKLIST IS UNTOUCHED, AND ALL FIVE CRITERIA REMAIN UNMET.** Every one
of them requires an **observed live evening**, which a local build cannot produce:

| # | criterion | why it is still open |
|---|---|---|
| 1 | the service self-exits at 17:35 with a carry open | needs an observed evening, ⛔ not a source read |
| 2 | the boot dependency removed or re-justified | untouched by this build |
| 3 | Friday's three-way measurement still converges | needs live broker truth |
| 4 | the obligation formally closed in HOT memory | ⛔ nothing struck |
| 5 | the restart hazard eliminated | untouched |

⇒ 🔴 **THE NIGHTLY MANUAL STOP IS STILL OWED, EVERY TRADING NIGHT.** A missed one still costs a
full trading day, silently, and a missed **Friday** still costs **Monday**. ⭐ Nothing in this
build changes that until it is deployed AND an evening is observed.

## L8 · 🔁 GATE RE-RUN AFTER THE `conftest.py` GUARD — ⛔ because it runs in EVERY session

**A change to `conftest.py` is not a test change, it is a change to every test run** — so the
full gate was re-run rather than reasoned about.

```
PYTEST_RC=1
9 failed, 5582 passed, 4 skipped, 281 warnings in 878.27s (0:14:38)
```
**⇒ REGRESSION ACCEPTED — zero NEW failures; 9 known baseline failures; RC=1 by convention.**

⭐ **BYTE-FOR-BYTE THE SAME OUTCOME AS THE PRE-GUARD RUN** — the same nine names, the same
`5582 / 4`. ⇒ **the guard is provably INERT on a supported launcher**, which is the property it
had to have: it must change *whether* the suite runs, ⛔ never *what it reports*.

**And it was proven in the other direction too, which is the half that matters:**

| launcher | result |
|---|---|
| PowerShell (`bash` → the WindowsApps WSL stub) | **exit 4 — a pytest USAGE error**, with the offending path printed. ⭐ Deliberately not exit 1: a *usage* error can never be mistaken for a test failure |
| Git Bash (`bash` → `/usr/bin/bash`) | **51 passed**, including both formerly-phantom families |
| `TS_ALLOW_UNSUPPORTED_SHELL=1` | runs, for someone who knowingly accepts a partial, non-comparable run |
