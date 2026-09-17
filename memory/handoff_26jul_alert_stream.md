---
name: handoff-26jul-alert-stream
description: "The 26-Jul alert-stream batch is CLOSED — the one owed check is RUN and PASSED. Current state: T2/Slice-2.5 re-validated against 388 commits of main drift and CANARY-READY, awaiting Rama + market hours. Two order/kill-path decisions still Rama's."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4ce1013a-db92-4899-ac6c-796dd439a76e
  modified: 2026-07-26T09:52:18.018Z
---

**Alert-stream batch DEPLOYED `e808595`, CODE LEDGER EMPTY. ✅ The one owed check is DONE (26-Jul ~09:20).**

## ✅ §A4 CONFIRMATION — RUN AND PASSED (nothing owed from this batch any more)

**The SSH-key alert has stopped.** Evidence, strongest first:
- `data_store/security/last_run.json` @ `09:17:25` — `clean: true`, **`findings_count: 0`**, `persistent: []`
  (and it carries the new §B `persistent`/`persistent_count` keys ⇒ the presence ledger is live).
- **Newest sentinel of ANY kind = `25-Jul 21:46:45`** — the last SSH-key one. Zero sentinels written since
  the fix; the `03:46:45` eligible re-fire window passed silently.

⚠️ **The count criterion I wrote in the old handoff ("still 37") was WRONG — it read 33, and 33 is correct.**
The `sentinel_retention` cron (02:05 daily, `-mtime +7`, on `*.delivered` only) ran `02:05:01 rc=0` and
deleted 17-Jul's four 6-hourly sentinels. Oldest survivor `18-Jul 03:27:09`, just past the 18-Jul 02:05
cutoff — arithmetic exact. Lesson recorded as a sibling in [[feedback-no-fixed-test-baseline]]:
**never make a COUNT the pass criterion for a population under retention.**

## ▶️ T2 / SLICE 2.5 — RE-VALIDATED 26-Jul, CANARY-READY

Branch **`fix-t2-repair-07jul`@`854112b`** (3 commits, LOCAL/UNPUSHED **by design** — live-validation-gated,
same convention the ledger used for `e4-w10-pnl-contract`; this is NOT a ledger leak).

**The risk was drift:** the branch was last validated **10-Jul**, and main has moved **388 commits** since its
base `eb75731`. Drift against main's signatures is what broke this script twice (3 signature drifts on 07-Jul;
the MARKET→LIMIT broker rejection on 10-Jul). Re-checked against a **true post-merge tree** (a scratch worktree
at current main with the 3 branch files overlaid — NOT the branch's own tree, which would test 07-Jul modules):

- main **never touched** the 3 branch files ⇒ **0 merge conflicts**.
- Dependencies that DID move: `core/config_loader.py` **12** commits, `core/state_store.py` **13**.
  `orders/price_math.py` + `orders/cnc_gtt.py` + `broker/rate_limiter.py` + `broker/order_state_machine.py`: **0**.
- `py_compile` clean · **import-smoke builds the adapter** (drifts #1/#2 still fixed; `load_all` survived the
  12 config commits) · **20/20 tests pass**.
- **`--dry-run` exit 0 and NOT vacuous** — throwaway DB built to **v44** (was v41 in July), FK chain seeded
  `signals`→`trades`, and the **`gtt_state` row landed**: `gtt_id=9000000000001, IDEA, SELL, qty=1,
  sl 97.0/94.05, tgt 105.0/104.45`, ACTIVE→CANCELLED on cleanup; analytics sibling isolated in the subdir.
- ⭐ **The P11 migration guard does NOT block it.** `StateStore(db_path)` passes no `allow_migrate=`, so it
  defaults **False** — but the refusal gate is `old_version is not None and old_version < EXPECTED`, and a
  brand-new file has `old_version = None` (`state_store.py:397` says so explicitly). Fresh build, no refusal,
  no CRITICAL sentinel. **Verified by execution, not by reading.**
- **No app importer** on current main ⇒ operator-only, as before.
- ⭐ **The VM canary copy is byte-identical to what I validated**: `/home/ubuntu/t2_proof_run/t2_cnc_gtt_realtest.py`
  sha256 **`a5779420d652c606…`** == the branch file. Monday's canary runs exactly this code. (The *deployed*
  tree still holds the old pre-repair script `23aca731…` — correct, the branch is unpushed.)

⚠️ **A quiet dry-run console is normal on a PC worktree** — progress goes through `get_logger` to `logs/`,
which a fresh worktree lacks. Read the **artifact** (throwaway DB `gtt_state` row), not the console.

### ⭐⭐ CORRECTION (26-Jul, from the ledger): T2's SAME-DAY LEG ALREADY PASSED LIVE

**"Canary-ready" understated it.** The live same-day canary **PASSED 10-Jul 14:26–14:41 IST with
REAL orders on FOUR symbols** — IDEA/JIOFIN/NTPC/ONGC each: BUY LIMIT accepted+filled → real
OCO-GTT (`327073639`/`327076809`/`327077052`/`327077301`) ACTIVE+verified → same-day SELL filled →
GTT deleted; ended flat, all holdings/GTTs NONE, ~₹0.2 total cost.

**⏳ The ONLY remaining T2 leg is `--arm-overnight`** — the DDPI/holdings-sell proof. A same-day
square is a *day position* with **no demat debit**, so DDPI is still UNPROVEN. Needs a **Mon→Tue
pair**, supervised both ends. Then the merge decision.

⚠️ **I misread live `gtt_state = 0` as "the GTT lifecycle never ran."** Wrong — T2 writes to an
isolated throwaway store **by design**. The zero means *the live service* has never placed a GTT,
which is a different and still-true claim. **Don't repeat that inference.**

## 🔴 RAMA'S DECISIONS — one now BUILT, one still open

1. 🔴 **OPEN — CHECK1's external-close label.** ⭐ Investigated 26-Jul, and it is **NOT cosmetic**:
   CHECK1 races our own exit path, wins, and the INFO **"TARGET HIT" alert is never sent** — a false
   CRITICAL replaces it (`order_placer.py:2374` early return). Not a missing check: the check exists
   and its result is discarded; plus the label is written 30 lines before the evidence is gathered.
   Full analysis + how a TRUE external close stays visible:
   `docs/audit/check1_external_close_26jul2026.md`. Overlaps **W8** (`trades.closure_source`) —
   **separable fixes, one shared vocabulary.** [[rms-manual-close-is-mislabel-26jul]]
2. ✅ **BUILT 26-Jul — the routine 15:15 SOFT_KILL CRITICALs.** `soft_kill` now routes at WARNING
   when `_is_scheduled_reason(reason)`, CRITICAL otherwise. Reuses `SCHEDULED_KILL_REASONS`, which
   `auto_clear_scheduled_kill()` already trusts for the *bigger* decision (unattended resume at
   08:15). Emergency kills proven un-swallowable by planting one real reason from **every**
   emergency caller; FIX-191's own email-fallback test stays green. Not silent: still alerts, and
   the 15:15 event keeps its dedicated WARNING from `main.py:699`.

## ✅ 26-Jul LATER — PAPER PRODUCT FIXED (`08d300b`), and it un-blinded TWO mechanisms

`zerodha_adapter.py:2165` hardcoded every PAPER position to `product="MIS"`. Fixed `f7eedd3` — the
book now reflects the order's product, which `_paper_place_order` had already stored on the same
record (`:1985`). ⭐ **Live was ALWAYS correct**; the change is **doubly unreachable in LIVE**
(`if self._paper:` at `:573` + the ZA16a guard at `:2054`), so Monday's boot cannot execute it.

**What it unblocks:** the EOD6/FIX-015 CNC exemption **and H-5's HARD_KILL sweep intent** (a CNC
swept as MIS opens a **naked short**). Both were "covered" by tests that hand-build
`Position(product="CNC")` — true assertions that prove the CONSUMER and bypass the FEED.
⇒ **"paper-proven", the stated delivery gate, could not prove the one thing it had to.**

⚠️ **Still NOT paper-modellable:** the overnight position→holding TRANSITION. `_paper_holdings` has
one writer (`seed_paper_holding`). Paper gets a carry's END STATE, never the transition ⇒ the
**Mon→Tue live pair is irreducible**, not conventional.

**Also landed:** `check1_w8_design_26jul2026.md` (⛔ design only, 6 open Qs for ChatGPT) ·
`slice25_never_run_pieces_26jul2026.md` (the 7 classified; top first-run risk = **conditional capital
allocation**, untested and the only one touching intraday capital).

⭐ **The register was corrected** — it claimed "nothing unpushed / no `hold-*` branches", which missed
the T2 branch **because it isn't named `hold-*`**. A held branch with a different prefix reads as
"nothing held".

## 📖 26-Jul LATEST — CHECK1+W8: §A LANDED, §B/§C/§D HELD WITH REASONS

✅ **§A `bc19aab` — the canonical closure vocabulary.** `core/closure_source.py` (code
single-source, mirroring how `core/constants.py` holds `PRODUCT_TO_INTENT`) +
`docs/closure_source_contract.md`. **15 tests**, incl. a **tree-wide scan forbidding any third
literal restatement** — proven non-vacuous by planting a copy in `core/constants.py` (RED, named
the file:line) and stripping the contradiction rule (RED); both restored md5-identical.
⭐ Two axes: `closure_source` (WHO) vs `exit_mechanism` (HOW) — a GTT leg is an SL/TGT by REASON.
⚠️ **Contradiction ⇒ CRITICAL, not a tie.** Precedence orders SILENT sources; it never overrules
one that SPOKE.

⛔ **§B/§C/§D HELD — `docs/audit/check1_w8_build_order_26jul2026.md`. Two reasons, both real:**

1. ⭐ **§0's own argument defeats §B.** §0 made the deferral default-0 to keep Monday readable.
   **§B cannot be defaulted off** — `closure_source`/`exit_mechanism` are new `trades` columns, and
   this schema **rebuilds `trades`** to add columns (`MIGRATION_TABLES[34]`/`[35]` precedent).
   ⇒ v45 rebuilds the live capital-bearing table at **Mon 08:15**, and a failed migration raises
   out of `StateStore` init ⇒ **the service does not start.** No flag makes that a no-op.
2. ⚠️ **§0.3's separation FAILS literally.** At bound 0 there is no deferral ⇒ CHECK1 still wins,
   `close_trade` still raises, `order_placer:2374` still returns ⇒ the literal "TARGET HIT" cannot
   fire. ⭐ **Fix: CHECK1 emits the INFO itself** from the same evidence (bound 0 ⇒ reconciler
   alerts, timing unchanged; bound >0 ⇒ order_placer alerts). Exactly one alert either way. **Build
   it that way or §C without §D leaves the alert deleted — which F1 forbids.**

▶️ **Ready to build next, in order:** §B (v45 + writers — ⭐ note `order_manager.close_trade` is the
ONE central finalizer and already takes a validated `exit_reason`, so derive there, not in 5 places;
`MANUAL_CLOSE` is the ambiguous one) → §C (D1+D2+classifier, **claim THEN cancel**) → §D (bound,
expiry log, CHECK1's INFO). **Do §B after Monday is observed clean.**

## 🔧 26-Jul FINAL — CHECK1+W8: §A·§B·§C BUILT, §D NOT. Branch `hold-check1-w8-26jul`, UNPUSHED.

4 commits: `77b8b04` §B (v45 + writer) · `10c02ae` classifier (component) · `2f8fd87` §C (wiring).
▶️ **TRIGGER unchanged: push after Mon 27-Jul is observed CLEAN** ⇒ Tuesday's boot takes the
migration as a single variable. If Monday isn't clean, it waits again.

**§C = D1 + D2 + classifier + 1.4.** ⭐ **D1 plumbed the answer rather than rewriting the check** —
`_cancel_orphaned_orders_for_trade` already classified the refusal correctly; its answer died in an
`int` the mid-fill branch never incremented. Now `OrphanLegOutcome(cancelled, mid_fill, ambiguous,
read_failed)` — and a failed lookup is `read_failed`, not a silent 0. ⭐ **The third discarded signal
is plumbed:** `_resolve_exit_price` fetched `get_trades()` (rows carry `order_id`) and kept only
`average_price`; an optional collector threads it out without changing the return type its other
caller needs.

⚠️ **§D NOT BUILT.** With 1.4 landed the good alert is no longer deleted, so §C stands alone; §D
adds the capital-*timing* fix only. **§0's rule is satisfied: §C shipped WITH 4.4.**

⚠️ **§3.1 ANSWERED — PAPER'S CLASSIFICATION IS WEAKER THAN LIVE'S.** `get_trades()` returns `[]` in
paper ⇒ **rungs 1–2 permanently unreachable; every paper suppression rests on rung 3 alone**, and
**the broker-vs-local contradiction rule can NEVER fire in paper.** Rung 3 exists precisely for this.
Bounded for Slice 2.5 only because FIX-183's prepass excludes a carried CNC before CHECK1 sees it.
**§3.2:** the 6 no-leg rows still reach CRITICAL — tested two ways (no legs; legs present none filled).

## 📌 STATE

- **PC == origin == VM bare == VM tree == `e808595`**, working tree clean; crontab byte-identical
  `892c9d0c…`; trading service `inactive`, `NRestarts=0`, start still Fri 24-Jul 08:15:27.
- **§B is LIVE** since the push (`security-watcher` = oneshot + `RestartSec=60`), verified running clean.
- ⚠️ 13F was THIS PC/shell's number — take a fresh same-shell BASE next time [[feedback-no-fixed-test-baseline]].
- **Monday 27-Jul 08:15** carries the previously-owed items on `docs/MONDAY_27-JUL_CARD.txt`.
