# SECTION E + THE F2 INVENTORY — 27-Aug-2026 (Thu)

**FILE 13 execution record.** Model: Claude Opus 5 (1M), reasoning MAX for §4.
🔬 MEASURED unless labelled otherwise · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S.

⛔ Nothing was pushed. ⛔ No service was started, restarted or stopped by me.
⛔ No order, no GTT. ⛔ No F2 implementation. ⛔ No revert-trigger change.
⛔ The `feat/delivery-config-split` working tree was never touched — every §4
figure is read from git objects.

---

## 0 — PRESERVATION FIRST (FILE 13 §4, mandatory before any branch work)

🔬 **`deploy/zerodha_morning.ps1` IS PRESERVED.** Done before any git command
that could reach the branch.

| copy | path | sha256 |
|---|---|---|
| working tree (unchanged) | `deploy/zerodha_morning.ps1` | `321c0e30…0b9d74b4` |
| preserved #1 | `C:\Users\rama\.claude\preserved\zerodha_morning.ps1.PRESERVED_27Aug2026` | `321c0e30…0b9d74b4` |
| preserved #2 | session scratchpad `preserved/` | `321c0e30…0b9d74b4` |

All three identical, 3,793 B, mtime 26-Aug 11:06. ⛔ Not committed, ⛔ not pushed.
Both copies live OUTSIDE the repo, so no branch operation can reach them.

---

## 1 — STATE LABELS AT THE TOP OF THIS SESSION

- **F2** — EXISTS · NOT DEPLOYED · **CORRECTNESS UNKNOWN (never measured live)**.
- The 48-commit branch is **SOURCE MATERIAL**, ⛔ not a deployment candidate.
- 🔬 `origin/main` resolved BY MEASUREMENT at session time = **`bc9a9f5`**
  (⛔ not taken from a card).
- 🔬 Rollback TREE stays `75e637c`. TREE ≠ `origin/main` is INTENTIONAL.

---

## 2 — THE THREE-WAY DELTA VOCABULARY — ADOPTED, ⛔ NOTHING REFACTORED

Adopted in this document, in logs and in evidence tables from here on:
`capital_delta_rupees` (₹) · `margin_residual_rupees` (₹) ·
`quantity_delta_shares` (shares). ⛔ No existing code was renamed tonight.

🔴 **THE ARMED REVERT TRIGGER REMAINS DISARMED BY POLICY.** ⛔ No revert may be
EXECUTED on its signal until the path is traced end-to-end
(trigger → owning function → input fields → **unit and semantic meaning** →
callers → downstream action → reversal consequence) and classified A/B/C/D/E.
✅ **TRACED 27-Aug ~10:0x** — 📄 `REVERT_TRIGGER_TRACE_27-Aug-2026.md`. Quantity = class **B**; the RULE = class **E**. ⛔ It STAYS DISARMED: class E + fail-safe C-3 both say escalate, ⛔ not adjudicate.

---

## 3 — SECTION E · THE 27-Aug 08:15 BOOT

⭐ Measured in order, ⛔ not reordered. Two clocks checked first:
🔬 PC `08:05:00` vs VM `08:05:02` — **in sync, ≤2 s**, so every timestamp below
is comparable.

### E-1 — Service / process state ✅ **PASS**
| | before (08:02:28 IST) | after |
|---|---|---|
| `trading-system` | `inactive` / `dead` | 🔬 **`active` / `running`** |
| `ExecMainStartTimestamp` | Wed 26-Aug 08:15:18 | 🔬 **Thu 27-Aug 08:15:15 IST** |
| `ExecMainPID` | 402677 (exited 26-Aug 17:35:05) | 🔬 **492196** |
| `NRestarts` | 0 | 🔬 **0** — ⛔ no restart loop |
| `token-watcher` | `active` since 28-Jul 06:02:38 | unchanged |

⭐ **The precondition hazard was checked FIRST and did not apply:** the standing
kill was `SOFT_KILL / circuit_breaker_force_close_15:15`, triggered
**26-Aug 15:15:01.600633** — a **PRIOR-DAY scheduled** kill, ⛔ not a manual stop.
⇒ ⛔ I did not `start`/`restart` anything; the automatic chain was left to run.

### E-2 — 🔴 TOKEN FRESHNESS FIRST ✅ **PASS**
🔬 At 08:02 the token was **ABSENT** — correct: `0 5 * * *` deletes it
(`data_store/session/` mtime = 27-Aug 05:00).
🔬 **Token written 08:15:02.023669803 +0530, 257 bytes** — the VM cron
`15 8 * * 1-5 … scripts/auto_refresh_token.py` fired on time.
⚠️ 🔬 **CORRECTION TO A STANDING ASSUMPTION:** the automatic morning path is
**entirely VM-side** (cron → `auto_refresh_token.py` → `token_watcher.sh`).
The PC script is an **operator tool**, not part of the automatic chain, and
🔬 **there is no Windows scheduled task for it** (checked the full non-Microsoft
task list).

### E-3 — Boot occurrence ✅ **PASS — and this is `bc9a9f5`'s FIRST RUN**
🔬 Full chain, timestamped:

| # | event | time (IST) | Δ |
|---|---|---|---|
| 1 | token written by cron | `08:15:02.023` | — |
| 2 | `token_watcher`: *"Fresh token detected … Starting trading-system.service."* | `08:15:15` | +12.98 s |
| 3 | `systemctl start` issued | `08:15:15` | +0 s |
| 4 | `ExecMainStartTimestamp` | `08:15:15` | +0 s |
| 5 | `KILL_AUTO_CLEARED` — `event_id 3796` | `08:15:16.538` | +1.5 s |
| 6 | **`STARTUP` — `event_id 3797`, scenario `COLD`** | **`08:15:27.356`** | **+12.4 s after (4)** |
| 7 | `is-active` = `active` | `08:15:17` (3 s poll granularity) | — |

✅ **STARTUP row is AFTER `ExecMainStartTimestamp`** (08:15:27.356 > 08:15:15).
✅ **L-1 satisfied — ⛔ it is NOT an earlier same-day row.** 🔬 Today's
`system_events` contains **exactly two** rows: `3796` KILL_AUTO_CLEARED and
`3797` STARTUP. `event_id` is monotonic against yesterday's STARTUP (`3794`).
✅ Kill switch auto-cleared exactly as predicted: `previous_state SOFT_KILL`,
`classification "scheduled"`, `cleared_via "clear_stale_state"`.
🔬 Boot health: **0 ERROR**, **2 WARNING**, **1 CRITICAL** — and the CRITICAL is
the known expected alarm (`kill_switch`, 08:15:16.535, *"KILL SWITCH ACTIVE AT
STARTUP"*), fired **3 ms before** the auto-clear that resolved it.
🔬 Live schema version = **45**; ⛔ no migration ran today.

⚠️ **RECORDED, ⛔ NOT CHASED (M-2):** that CRITICAL's text says *"operator must
call `resume()` to clear"*, which was **already untrue 3 ms later**. 🏷️ LATENT,
message-accuracy only; it did not change any decision.

### E-4 — Bounded search for *"NO strategy resolver was supplied"* ⚪ **UNPROVEN (0 hits, and 0 is not proof)**
🔬 **0 hits on three independent surfaces:** today's `system_2026-08-27.log`
(84 lines / 13,871 B) · every file in `logs/` modified today · `journalctl -u
trading-system --since 08:15:00`.
🔬 **Positive controls, stated so the zero means something:** the log is readable
and grep-able (`wc -l` = 84). ⚠️ **But the bare phrase `strategy resolver` also
returns 0**, so this search cannot distinguish *"the CRITICAL did not fire"* from
*"this phrase never appears in this file at all"*.
⇒ 🔴 **ABSENCE DOES NOT PROVE THE FEATURE LIVE.** The book is flat, so the
resolver path was very likely never exercised. ⛔ Recorded as UNPROVEN.

### E-5 — `get_holdings` at boot ✅ **PASS (boot leg)** · `carry` at 09:15 ✅ **PASS (see §7)**
🔬 `zerodha_adapter get_holdings` — `call_start 08:15:24.659`,
`call_end 08:15:24.672`, `duration_ms 13`, **`result_summary "0 holdings"`**.
✅ **Matches the FROZEN expectation: ZERO.** The book closed flat on 26-Aug.
⛔ **`carry=0` is NOT carry correctness** — it is one flat-book observation.
✅ **The 09:15 leg is now MEASURED — §7.** `carry 0.0` at `09:15:00.049`, on four
independent surfaces. ⚠️ It was `⏳ pending` here only because this section was
written at 08:32, before the window arrived; the PC died at ~09:15 and §7 was
recovered VM-side at 09:23. ⛔ The §7 evidence is the 09:15 **capital sync**, ⛔ not
`preflight --phase C` — phase C tests SIGNALS, ⛔ it carries no carry figure.

### E-6 — The 45 s morning check ⚪ **UNPROVEN — DELIBERATELY NOT RUN**
🔴 **I did not run `zerodha_morning.ps1`, and running it would have been unsafe.**
Three measured reasons:
1. 🔬 The PC-side token `data_store\session\zerodha_token.json` is **265 B, mtime
   21-Jun-2026 12:47**. The script's step 1 would read it as expired and run
   `scripts\zerodha_login.py --account LFL836`.
2. 🔴 **A fresh Zerodha login mints a new access token and can invalidate the one
   the LIVE session is currently holding.** The service went active at 08:15:17
   and is trading today. ⛔ That risk is not worth a test.
3. 🔬 The script is **interactive**: it ends in `Read-Host "Press Enter to close"`
   and, on failure, `Start-Process ssh`. With stdin at the null device it cannot
   complete non-interactively.

⭐ **But the fix's PREMISE was measured today, and it holds:** token written
`08:15:02.023` → watcher detected `08:15:15` = **12.98 s**, inside a **30 s**
poll cycle (`token_watcher.sh:22 SLEEP_SEC=30`). ⇒ an operator push lands
uniformly in [0, 30) s plus ~2 s to reach `active`, so a **15 s** wait is a
coin-flip and **45 s** covers the whole cycle. **The 45 s value is correct.**
🔴 ⚠️ **AND TODAY COULD NOT HAVE GONE RED ANYWAY** — at 12.98 s even the old 15 s
wait would have read GREEN. ⇒ **today was never a discriminating test of this
fix**, whatever had been run. 👤 A real test needs Rama to run the script himself
on a morning where he pushes the token.

### E-7 — Rollback TREE ✅ **PRECONDITION NOW MET — 👤 the act is Rama's**
E-3 proves `bc9a9f5` boots: `STARTUP 3797 COLD` at 08:15:27.356, 0 ERROR,
kill auto-cleared, holdings call clean, service `active` with `NRestarts=0`.
⇒ The TREE **may now be considered** for `75e637c` → `bc9a9f5`.
⛔ **I have not advanced it.** A green gate is never authorisation, and neither a
card nor a reviewer may speak for Rama.

### E-8 — CHECK 1 / 2a / 2b / four-reading / G3 T+1 ✅ **CORRECTLY NOT RUN**
🔬 Book is flat (`0 holdings`). ⛔ Not run against a flat book, ⛔ no carry
manufactured.

> 🔴 **BOOT PROOF ≠ FEATURE PROOF.** Everything above proves the deployed service
> starts and reaches its running lifecycle state. ⛔ It proves nothing about F2
> correctness, resolver correctness, carry correctness, capital reconciliation,
> G3, or the safety of any undeployed branch.

---

## 4 — THE F2 INVENTORY (measurement only; ⛔ no decision, ⛔ no code)

### The ten answers

**1. Exact F2 branch HEAD**
🔬 `6d24a831d114ee63e719de130f0779161c7288fe` — 2026-08-09 01:50:42 +0530 —
*"docs(gate): 9a resolved by swapping primary and cross-check; the gate freezes"*.

**2. Merge-base with current `origin/main`**
🔬 `645728dd5bf57fe9cc4f3a1f6de248685d17b9cc` — 2026-08-07 18:16:58 +0530.
🔬 `git rev-list --left-right --count` = **48 ahead / 81 behind**.
⚠️ **The ledger says 77 behind. 81 is correct today** — Batch A's four commits
(`ae6c344`, `ce29d49`, `272d1d4`, `bc9a9f5`) landed on 26-Aug after that figure
was written. ⭐ The behind-count moves whenever main moves; re-measure at use,
⛔ never quote it from a card.

**3. The 48 commits** — all dated 07-Aug…09-Aug-2026. By class:

*Five commits carry effectively all the code:*

| SHA | subject | files | +/− |
|---|---|---|---|
| `c39e799` | fix(delivery): F6 — exit identity, not exit quantity | 8 | +1,864 / −21 |
| `12348ec` | feat(pipelines): delivery and intraday become two independent books | 15 | +2,024 / −139 |
| `aa364e2` | refactor(config)!: the caps become `intraday_max_*` — D1 phase A | 13 | breaking rename |
| `247b983` | feat(governor): the loss limit cuts off one book, not the system | 3 | +563 / −71 |
| `65b7196` | feat(sizing): the allocation model — the stop moves the money, not the size | 30 | +2,577 / −848 |

*plus* `a5ae50d` (three gate-found defects), `9fdfe41` (bash/WSL-stub test guard),
`e0c83da` (auditor C5 test). **The remaining ~40 are docs/records** —
`docs(map,paths)`, `docs(gate)`, `docs(governance)`, decision cards, a register pass.

**4. How many files changed, and which**
🔬 **102 files, +12,168 / −1,107** (`git diff --shortstat 645728d 6d24a83`).

🔴 ⚠️ **THE LEDGER'S "2,122 insertions / 1,025 deletions across 12 files" IS NOT
REPRODUCIBLE.** Search width stated — eight measures tried:

| measure | result |
|---|---|
| three-dot merge-base → branch | **102 / +12,168 / −1,107** |
| two-dot `bc9a9f5..6d24a83` | 171 / +12,855 / −21,049 |
| vs the old `origin/main` `75e637c` | 168 / +12,855 / −19,788 |
| working tree vs HEAD (uncommitted) | 10 / +1,104 / −44 |
| code only, excl. docs+tests | 21 / +2,621 / −408 |
| `capital/ core/` only | 10 / +1,777 / −317 |
| `capital/ core/ orders/ signals/` | 15 / +2,256 / −347 |
| modified-only, non-doc non-test | 20 / +2,201 / −408 |

⛔ **None yields 12 / 2,122 / 1,025.** ⇒ The correct figure for *"what this branch
adds over the shared ancestor"* is **102 files / +12,168 / −1,107**, and the branch
is **~8.5× larger in file count** than the ledger records.
🔴 **Do not plan the work off the old number.**

**5. Which changed files are ALREADY represented in current main**
🔬 **ZERO by content.** Not one of the 102 has a byte-identical twin in `bc9a9f5`.

| class | count | meaning |
|---|---|---|
| **COLLISION** | **34** (31 code/config + 3 docs) | changed on BOTH sides since the merge-base |
| **BRANCH-ONLY** | **68** | main has not touched them since the merge-base |
| **CONVERGED** | **0** | no branch change already landed identically on main |

⭐ But *"represented"* also means **re-implemented in substance** — and there it is
**not** zero. See **P-A**.

**6. Which changes are genuinely NEW** — the 68 branch-only files:
- **16 production code/config** — `capital/pipeline_policy.py` (**420 lines, wholly
  new**), `allocation/portfolio_allocator.py`, `config/scoring_weights.yaml`,
  `core/market_windows.py`, `core/migrations.py`, `orders/order_manager.py`,
  `screening/quality_scorer.py`, `screening/secondary_screener.py`,
  `signals/webhook_receiver.py`, `scripts/preflight/checks/config_integrity.py`,
  `scripts/system_manager.py`, `reports/daily_trade_review.py`, 3 ops_dashboard
  services + `controls.html`
- **30 tests** — `test_f6_delivery_exit_predicate.py` (820),
  `test_two_pipeline_split.py` (655), `test_order_sizing_allocation.py` (501),
  `test_pipeline_loss_governor.py` (342), `test_schema_v46_sizing_audit.py` (218),
  `test_intraday_cap_rename.py` (141), …
- **22 docs**

**7. Duplicate implementations of the same resolver / pipeline / config / guard?**
🔬 **NO — and this is the branch's strongest structural property.**
There is **ONE** policy object (`PipelinePolicy`, a frozen dataclass) and **ONE**
resolver (`resolve_pipeline_policy`), built once at `main.py:2438` and injected as
`policy_provider=` into **five** subsystems (`main.py:2495, 2623, 2683, 3025, 3291`).
Each consumer holds a `_policy_for(...)` that delegates to that provider and falls
back to an **explicit, logged** pre-split shim when it is absent.
`pipeline_policy.py:2` states it: *"THE ONE authoritative resolver for two-pipeline
policy."*
⇒ **Two policies, one mechanism.** ⛔ Not a forked pipeline.

**8. 🔴 Does it introduce a second trading book / capital pool / governor / lifecycle path?**

| dimension | verdict | evidence |
|---|---|---|
| **Second trading BOOK** | **YES — BY DESIGN. That IS F2's requirement**, ⛔ not a defect | `12348ec`; expressed as policy, ⛔ not as a duplicated code path (Q7) |
| **Second capital POOL** | 🔬 **NO — RULED OUT** | The 70/30 buckets **already exist on deployed main**: `fund_manager.py:285/300/338/368/373/478/481`, `system_config.yaml:144-145`, with a sum-to-1.0 assertion at `:324`. The branch adds per-bucket **policy resolution**, ⛔ not a new pool. `capital_base_value()` is *always* the bucket — *"Neither pipeline may borrow from the other"* |
| **Second GOVERNOR** | 🔬 **NO — RULED OUT** | `247b983` is ONE loop over buckets reading ONE limit source. Its own docstring: *"⛔ There is deliberately no second loss calculation anywhere in this module… One limit, two enforcement points, ONE source."* Unwired it logs a WARNING and stays on the pre-split GLOBAL base |
| **Second LIFECYCLE path** | 🔬 **NO for F2** | The branch adds per-book *admission windows* (`delivery_entry_start/end`, `delivery_expiry_sec`) — policy, not lifecycle. The one real lifecycle change on this branch is **F6 (`c39e799`)**, a delivery-**exit** predicate — a **separate register item that merely shares the branch** |

🔬 **A NEW CAPABILITY the branch supplies that main does not have:**
`core/state_store.get_daily_realized_net_pnl_for_bucket(today, bucket)` —
**branch-only, ABSENT on `bc9a9f5`**. This matters because main's own F1 comment
says the post-close circuit breaker *"stays GLOBAL — one account-wide realized P&L
exists and **there is no per-book attribution to split it with**."*
⭐ That is true **of main**. The branch **creates** that attribution.
⛔ Not a contradiction — a real capability gap the branch closes.

**9. Config / schema / memory / documentation changes required**
- 🔴 **BREAKING config rename (`aa364e2`, D1 phase A)** — `max_open_positions` →
  `intraday_max_open_positions`, `max_daily_trades` → `intraday_max_daily_trades`.
  Touches config + `pipeline_policy` + `risk_engine` + `config_auditor` +
  `config_loader` + `schema.sql` + `state_store` + `main.py` + **4 ops_dashboard
  files** + `docs/locked_decisions.yaml`. ⛔ **D1: NO PARTIAL DEPLOY.**
- 🔴 **SCHEMA v45 → v46, a `trades` REBUILD.** 8 new sizing-audit columns
  (`qty_by_allocation`, `qty_by_segment_capital`, `qty_by_broker_margin`,
  `qty_by_max_position_value`, `qty_by_max_qty`, `planning_basis_rs`,
  `capital_per_trade_allocation`, `risk_budget_per_trade`); `qty_by_risk` and
  `qty_by_capital` **RETIRED, ⛔ not reused** (pre-v46 rows keep their true values).
  🔬 The live DB measured **v45** this morning. ⚠️ An evening schema push buys a
  night of CRITICALs — the migration lands only at the next OFF-MARKET boot.
- 🔴 **`binding_constraint` vocabulary is a DIRECT, SAME-LINE COLLISION.**
  MAIN (`e39655a`, BUG-NI18) *appends* `multiplier` to the old vocabulary; the
  BRANCH *replaces* the vocabulary with `allocation | segment_capital |
  broker_margin | max_position_value | concentration | max_qty | flat`.
  ⭐ Note **why** main needed `multiplier`: to name the case where the tier/perf
  multiplier lifted qty above the tightest rung — **the very defect the branch's
  model removes by construction** (see P-B).
- **New config surface** — `delivery_entry_start` / `delivery_entry_end`,
  `delivery_expiry_sec` (null = *no expiry*, ⛔ NOT a fallback), delivery tier
  multipliers, `delivery_max_*`, `delivery_max_single_order_qty`,
  `config/scoring_weights.yaml`, `docs/locked_decisions.yaml`.
- **Docs** — `docs/campaign_practices.md` (611 lines) and the decision cards live
  on this branch and are **not** on main.

**10. Can the useful part be extracted as a small, reviewable change?**
🔬 **Partly — and the separation is measurable.**
- ✅ **F6 (`c39e799`) IS cleanly extractable.** 8 files, +1,864/−21, and its
  heaviest file `orders/cnc_gtt_monitor.py` (+326 on the branch) has taken only
  **+3/−1** on main since the merge-base. Its substance is **not** on main.
  ⚠️ It is a *delivery-exit* item, ⛔ **not** F2.
- ✅ `capital/pipeline_policy.py` (420 lines) transplants as a new file with
  **zero** collisions.
- ⛔ **The F2 core is NOT cleanly extractable** — every consumer of that new file
  is a collision file main has since repaired. See P-C.

---

### The three frozen predictions — scored

**P-A — *"F1 vs `feat(pipelines)` may be the same work done twice"* → 🟡 HELD IN PART.**

🔬 Main's F1 = `d00e574` (*"delivery risk config is explicit; the silent fallback
is gone"*), `6ad328e` (NI-4), `a056768` (NI-9). Main's config now reads: *"each key
is REQUIRED… A missing or null value is REJECTED at config load — the boot logs the
key name at CRITICAL and exits 5. There is NO inheritance from the intraday keys."*
The branch says the same thing: *"⛔ NULL NO LONGER MEANS 'fall back to the
global'… a null here is a STARTUP VALIDATION ERROR."*
⇒ ✅ **The fail-closed delivery-config contract IS duplicated work.**

⛔ **But the genuinely-new subset does NOT shrink sharply**, because the two builds
disagree on the values *and the model*:

| key | MAIN (F1, DEPLOYED, behaviour-neutral by construction) | BRANCH (F2) |
|---|---|---|
| `delivery_risk_per_trade_pct` | `0.01` (= global today) | `0.02`, **⛔ INERT for sizing** |
| `delivery_max_concentration_pct` | `0.10` | `0.20` **of the delivery basis** |
| `delivery_max_position_value_pct` | `0.40`, **REJECTS** | `0.25`, **TRIMS** |
| `max_concentration_pct` (intraday) | `0.10` of TOTAL | `0.20` **of the planning basis** |
| `max_position_value_pct` (intraday) | `0.40` of TOTAL, REJECTS | `0.25` of basis, **TRIMS** |
| `risk_per_trade_pct` (intraday) | a live sizing input | **⛔ INERT for sizing** |

⇒ 📄 F1 is *config independence, behaviour-neutral*. The branch is *config
independence **plus** a different sizing model that deliberately changes the
INTRADAY book*. ⭐ **They are the same work only in the fail-closed dimension.**

**P-B — *"NI-16's blocker may already be resolved on the branch"* → 🟢 HELD.**

🔬 BRANCH `capital/position_sizer.py:574-575`:
`effective_mult = min(1.0, effective_mult_unclamped)` then
`allocation = base_allocation * effective_mult`. The multiplier lives **inside**
the allocation and can only ever REDUCE it.
🔬 MAIN `capital/position_sizer.py:545`:
`effective_mult = tier_mult * max(0.0, perf_weight)` — **no `min(1.0, …)`, and no
allocation for a ceiling to be *of*.**
⇒ NI-16 is **structurally resolved on the branch** and remains LIVE-but-LATENT on
main (`perf_weight ≡ 1.0` today).
⇒ ✅ **NI-16 moves BLOCKED → QUEUED.** ⛔ Not built, per FILE 13.

**P-C — *"main's commits may have reverted or superseded branch work"* → 🟢 HELD, and it is THE cost driver.**

🔬 Of main's **81** commits since the merge-base, **19** touch `ops_dashboard/`
(the GUI track). The rest include an NI-series landing squarely inside the
branch's own files:

| collision file | main commits | main +/− | what they are |
|---|---|---|---|
| `capital/position_sizer.py` | **5** | +187/−42 | NI-5, **NI-17**, **NI-18**, NI-1, item-1 — all sizing defect fixes |
| `main.py` | **5** | +393/−29 | EOD lifecycle ×2, NI-12, item-1, alerts PHASE 1 |
| `core/config_auditor.py` | **4** | +134/−15 | NI-5, NI-11, NI-12, NI-2 |
| `core/state_store.py` | **4** | +102/−7 | TICK 2 *"gate 1 becomes pipeline-scoped"*, EOD lifecycle, NI-3 |
| `capital/risk_engine.py` | **3** | +116/−16 | NI-9, NI-3, item-1 |
| `core/config_loader.py` | **3** | +102/−20 | NI-4, NI-3, item-1 |
| `capital/fund_manager.py` | **1** | +156/−12 | *"a carried delivery position is not a claim on today's cash"* |
| `ops_dashboard/backend/readers/db_reader.py` | **11** | +1,338/−14 | the GUI track |

⇒ 🔴 **Taking the branch's version of these files wholesale would REVERT NI-1,
NI-2, NI-4, NI-5, NI-9, NI-11, NI-12, NI-17, NI-18, TICK 2's pipeline-scoped
gate 1, the EOD-lifecycle fixes and `63caa52`.**
⭐ A 21-day-stale branch is not merely stale here — it is **actively wrong in
exactly the files it must change.**
🔬 **Plus one rename/modify conflict:** main renamed
`tests/unit/test_position_sizer_delivery_scaffold.py` →
`test_position_sizer_delivery_contract.py` (`742d9da`, R100); the branch modifies
the **old** path (+74/−34).

---

### 🔴 TWO FINDINGS THE TEN QUESTIONS DID NOT ASK FOR

**FINDING 1 — the branch's own headline regression guard is VACUOUS.**
`test_12_mis_sizing_is_byte_identical` calls itself *"⛔ THE REGRESSION LINE OF THE
WHOLE BUILD"*. At branch HEAD it asserts `p.sizing_base(total) == total`.
🔬 **`sizing_base` is dead code:** `position_sizer.py:404` — *"⛔ `pol.sizing_base`
is NO LONGER READ"* — and a whole-tree grep finds its only remaining callers are
that one test file. The live basis is `pol.planning_basis(total, planning_leverage)`.
Its other assertions compare the resolver's fields to **the config's own fields** —
and those config values changed (`0.10 → 0.20`, `0.40 → 0.25`).
⇒ 🔴 **The test cannot go red when MIS sizing changes.** ⚠️ Exactly the shape
already on the RULES list: *a green check is evidence only if it could have been
red*. 🏷️ **LATENT** (branch undeployed) ⇒ recorded, ⛔ not fixed.

**FINDING 2 — the allocation model implements a ruling Rama has HELD.**
🔬 On the branch, MIS plans against
`intraday_bucket (0.70) × leverage_map.INTRADAY (5.0)` = **3.5 × total capital**,
replacing today's *total capital* base. (`leverage_map.INTRADAY: 5.0` measured on
`bc9a9f5`.)
📄 The ledger records **"F2a's MIS 3.5× is HELD"**, and records the refusal that
produced it: *"the argument is that the answer is DERIVABLE from Rama's stated
architecture ⇒ ⛔ **DERIVABLE IS NOT DECIDED**."*
⇒ 🔴 **The branch cannot be deployed as-is without executing a decision Rama has
explicitly not taken.** 👤 **His to rule — ⛔ not a build detail.**
⭐ The branch's author flagged it himself, in `pipeline_policy.sizing_base`:
*"A DELIBERATE ASYMMETRY, AND IT IS THE ONE JUDGEMENT CALL IN THIS BUILD —
recorded here rather than buried in the sizer, because it is Rama's to overrule and
it must be findable."* ⭐ It was findable. ⛔ It is still unruled.

---

### THREE OPTIONS, WITH MEASURED COSTS — ⛔ NO CHOICE MADE

**OPTION A — extract a clean subset.**
- ✅ Cheap and real for **F6 (`c39e799`)**: 8 files, +1,864/−21, main has moved
  only +3/−1 in its heaviest file. ⛔ **But F6 is not F2.**
- ✅ `capital/pipeline_policy.py` (420 lines) lands as a new file with **zero**
  collisions.
- ⛔ **Its five consumers do not.** Wiring it means re-applying branch work onto
  `position_sizer.py` (5 main commits), `main.py` (5), `config_auditor.py` (4),
  `state_store.py` (4), `risk_engine.py` (3), `config_loader.py` (3),
  `fund_manager.py` (1) **without reverting the NI-series**.
- ⛔ Cannot be done without also taking the **breaking `intraday_max_*` rename**
  (D1: no partial deploy) **and schema v46**.
- 💭 Cost shape: **1 clean new file + 31 code/config collision files** — ~10 core
  files hand-merged against main's repairs, ~11 ops_dashboard rename touch-points
  (1–3 lines each on the branch side, but main has rewritten those files heavily),
  plus a rename/modify conflict.

**OPTION B — reimplement F2 against current main.**
- ⭐ `pipeline_policy.py` becomes a **specification you can read** — 420 fully
  commented lines with its judgement calls labelled — rather than a patch to land.
- ⭐ The branch's **30 test files are the acceptance suite**, and they already
  cover **all seven behavioural criteria**:

  | criterion | test |
  |---|---|
  | A runs while B is stopped | `test_intraday_limit_reached_blocks_MIS_and_leaves_DELIVERY_trading` |
  | B runs while A is stopped | `test_delivery_limit_reached_blocks_DELIVERY_and_leaves_MIS_trading` |
  | own config each | `test_01`, `test_02`, `test_03`, `test_03b`, `test_03c` |
  | own capital / reservation each | `test_05`, `test_05b`, `test_05c` |
  | own limits and counters each | `test_04`, `test_06`, `test_06b`, `test_07`, `test_07b` |
  | a halt in one does NOT halt the other | `test_intraday_governor_cannot_flatten_delivery`, `test_a_failed_close_does_not_take_the_other_book_down`, `test_both_limits_reached_blocks_both_independently` |
  | shared infra ≠ a single global stop | `test_the_governor_NEVER_arms_the_kill_switch`, `test_HARD_KILL_keeps_its_global_semantics` |

- ⛔ Cost: rewriting ~2,600 lines of production code across ~21 files.
- ✅ Keeps every NI-series fix; ⛔ zero rename/modify conflicts.
- ✅ Lets FINDING 1's vacuous guard be replaced by a real one, and lets FINDING 2
  reach Rama **before** any code depends on the answer.

**OPTION C — F2 is obsolete / already superseded.**
🔬 **REFUTED BY MEASUREMENT.** Main has **no** `pipeline_policy.py`, **no**
`allocation_divisor`, **no** `min(1.0, …)` clamp, **no**
`get_daily_realized_net_pnl_for_bucket`, and **no** per-book loss governor.
⭐ Only the *fail-closed config* half was superseded, by F1.
**The two-book split itself is not on main in any form.**

👤 **Rama decides.** ⛔ I have not chosen, and *"48 commits exist"* must not
dictate the method.

---

### F2 ACCEPTANCE GATE — state after this session

| box | state |
|---|---|
| branch identity | ✅ MEASURED |
| merge-base | ✅ MEASURED |
| 48-commit list | ✅ MEASURED |
| aggregate diff | ✅ MEASURED — ⚠️ and it corrects the ledger |
| duplicate / superseded functionality identified | ✅ MEASURED (P-A, P-C) |
| 🔴 second-book / second-capital-pool risk RULED OUT | ✅ **RULED OUT** (Q8) |
| config / schema impact | ✅ MEASURED |
| integration path chosen | ⛔ **OPEN — 👤 Rama's** |
| tests defined | 🟡 the branch's suite covers all seven criteria — ⚠️ FINDING 1 must be repaired first |
| implementation passes · commit · VM deploy · post-deploy evidence | ⛔ NOT STARTED |

---

## 5 — WHAT THE WINDOW ALLOWED

### 5.1 — K-1 🔴 **THE EXPECTATION IS REFUTED. K-1 DOES NOT CLOSE — IT OPENS.**

**The question** (ledger + `EOD_CARRY_SEQUENCE_26-27-Aug-2026.md:1931`): *does the
system deduct charges from bucket capital DURING the session, at trade close,
while the broker has not yet debited them?* 👤 Rama's contract-note fact: the
broker settles CNC/MIS charges **out of market**, that midnight or the next day.
📄 FILE 13 §5.1 predicted **"expected to CLOSE"**.

🔬 **ANSWER: YES. Measured twice — in the deployed code, and in the live ledger.**

**(a) The deployed code** — `capital/fund_manager.py` @ `bc9a9f5`, `release_used`:
```
pnl = gross_pnl - costs                          # net of charges
self._bucket_add_avail(bucket, margin + pnl)     # ← charges leave BUCKET AVAIL
self._total += pnl                               # ← charges leave _total
```
⭐ Read from the **code body**, ⛔ not only the docstring — though the docstring
states the same contract outright: *"pnl_delta := gross_pnl − costs, and that same
NET number is what is credited to bucket avail and to `_total`."*

**(b) The live ledger — the exact ₹1.15 K-1 asked to trace:**

| ledger_id | ts | bucket | margin_delta | pnl_delta | **costs** | bal_before | bal_after |
|---|---|---|---|---|---|---|---|
| **11499** | **2026-08-26T15:19:53.319488+05:30** | **positional** | −454.48 | −6.57 | **1.15** | 2,715.98 | **3,163.89** |

🔬 Arithmetic closes exactly: `2,715.98 + 454.48 + (−6.57) = 3,163.89`.
⇒ **WHEN:** at trade close, 15:19:53 — mid-session, ~4 min after the 15:15
circuit-close. **WHERE:** `positional` bucket `avail`, and `_total`.
⇒ **DID IT REDUCE AVAILABLE CAPACITY INTRADAY?** ✅ **YES** — `balance_after` is
₹1.15 below what a gross-P&L credit would have left.

🔬 **Whole-day magnitude, 26-Aug** — six `RELEASE_USED` rows, `costs` =
1.34 + 0.57 + 1.09 + 1.46 + 0.46 + 1.15 = **₹6.07** removed from bucket `avail`
during the session, against a day-start capital of **₹10,567.60** (`INIT`,
`ledger_id 11411`, 08:15:26). **= 0.057 % of total capital.** Positional-only
charges were ₹3.95 on a ~₹3,170 bucket = **0.125 % of that bucket**.

⇒ 👤 By Rama's own stated rule — *"IF YES ⇒ each pipeline's intraday capacity is
UNDERSTATED and later trades are UNDER-SIZED — a CORE SIZING EFFECT"* — **K-1
stays OPEN as a core sizing item.** 🏷️ **PREDICTION FAILED, recorded as failed.**

⚠️ **Two things this does ⛔ NOT establish, stated so the finding is not over-read:**
1. **Whether it is a DEFECT is a design ruling, ⛔ not a measurement.** The broker
   *will* take that money at midnight, so deducting at close is **conservative** —
   it understates capacity now and matches reality later. Whether "capacity" means
   *what the broker would honour this second* or *economically committed capital*
   is 👤 **Rama's to rule.**
2. **Whether the understatement ever CHANGED a size is not measured.** Deployed
   sizing takes `min(risk, capital, concentration)`; this only bites when the
   **capital** rung binds. ⛔ I did not measure how often it binds.
⛔ Nothing was fixed, tuned or changed — report only, per the standing instruction.

### 5.2 — The uncommitted audit files: 🔬 **69 untracked, ⛔ not 62 — and the pattern settles it**

🔬 `git status` shows **69** untracked entries: **63** under `docs/audit/`, 2 under
`docs/decisions/`, `alerts/delivery.py`, `exp.xlsx`, 2 under `tests/unit/`.

🔴 **FIRST, THE CORRECTION THE INSTRUCTION WARNED ABOUT — ⛔ these are NOT missing fixes:**
🔬 `alerts/delivery.py` and `tests/unit/test_alert_delivery_contract.py` are
**TRACKED ON `origin/main`** and **PRESENT ON THE VM** (`alerts/delivery.py`,
5,960 B, 17-Aug 19:06). They read as *untracked* only because the ROOT working
tree sits on `feat/delivery-config-split` (09-Aug), which predates the Phase-0
alert-contract commit. ⭐ **A file's status is relative to the branch you are
standing on** — this is a stale-branch artifact, ⛔ not a gap.

**THE PATTERN, named instead of listing 63:** `docs/audit/` is by campaign
practice the **dated-record space** (*"Reports → `docs/audit/`"*). 🔬 **All 63
carry a date stamp in the name** (58 as `_DD-MMM-YYYY`, the other 5 as
`_DD-MMM-YYYY_evening` / `_0046` / `capture_10aug2026/` / `gate_20aug2026/`), and
**17 are `PREDICTION_*`** — written-before / scored-after records, historical by
definition. ⇒ **HISTORICAL is correct by construction for 61 of 63.**

**THE OPERATIVE LIST — 🔬 two files, and it is short by measurement, not by assertion.**
Screened by *executable-command density* (`sudo|ssh|systemctl|git|sqlite3|grep|journalctl|cd /home`)
and cross-checked against the VM's 235 `docs/audit/` entries:

| file | cmd-lines | on VM? | class |
|---|---|---|---|
| `ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md` | 16 | ✅ **YES**, 49,703 B, 26-Aug 19:28 | OPERATIVE — ✅ **already remediated** |
| `RUNBOOK_n907_install_20-Aug-2026.md` | 12 | ❌ absent | **OPERATIVE** (procedure; its own install is done — value is as the next refit's template) |
| `OPS2_HANDOVER_RAMA_23-Aug-2026.md` | 13 | ❌ absent | **OPERATIVE** (handover to Rama, carries commands) |
| `MORNING_CHECK_WAIT_26-Aug-2026.md` | **0** | ❌ absent | HISTORICAL — reasoning behind the 45 s change, ⛔ not a procedure |

🔬 **Of the 63, exactly 2 are on the VM; 61 are absent.** ⛔ Nothing pushed, per
instruction. 👤 The only actionable residue is whether the **two** operative files
above should join `ROLLBACK_AND_ATTENDANCE` on the VM.

### 5.3 — F9 SOURCE-OF-TRUTH (P7) — 🔬 **REACHED AND ANSWERED A–F. ⛔ No mechanism built.**

🔴 **THE HEADLINE, AND IT IS NOT WHAT THE QUESTION EXPECTED: there are TWO sector
consumers with TWO DIFFERENT SOURCES, and only one of them is wired.**

| path | reads | today's value | mode |
|---|---|---|---|
| **SCORE** — `screening/step_executor.py:331 _step_6_sector_strength` | `md.get("sector")` | 🔬 **hard-wired `None` ⇒ a CONSTANT `0.5`** | **LIVE** |
| **RISK** — `capital/risk_engine.py` via `sector_lookup_fn` | `instrument_cache.sector()` → the real CSV | 🔬 **93.6 % `UNKNOWN`** | `sector_cap_mode: observe` (log-only) |

⛔ **Never conflate them.** The `observe` safety covers **only** the RISK cap. The
SCORE path is live today and unaffected by `sector_cap_mode`.

**A — every reader of sector/instruments data** (deployed `bc9a9f5`, code only):
`core/instrument_cache.py` is **THE single loader** (`InstrumentCache.load`), and
`.sector()` has exactly **three** production callers —
`capital/risk_engine.py:136`, `main.py:2905`, `orders/order_placer.py:721`.
Other instruments.csv readers: `main.py:2438` (boot load),
`scripts/preflight/checks/broker.py:217` (mtime freshness),
`scripts/sr_level_export.py`, `scripts/find_symbol_aliases.py`.
⚠️ **`step_executor` is NOT among them** — the score path never touches the cache.

**B — every writer / import path:** exactly one — `scripts/refresh_instruments.py`
(*"Build instruments.csv from three authoritative sources"*: NSE security master +
sector indices + Kite API; RI13 `--csv`, default `config/instruments.csv`), run by
cron `0 9 * * 1-5`. Plus `InstrumentCache.reload(path)` (FIX-092 event).
⇒ ⭐ **There is no second import path, and no second sector-mapping mechanism to build.**

**C — is `config/instruments.csv` authoritative, generated, stale, test-only?**
🔬 **GENERATED, and authoritative at runtime.** `.gitignore:39` lists it ⇒ ⛔ never
in a clone or a fresh worktree (**this is the same file that produces the 26
phantom gate failures**). Production copy measured: **77,460 B, 2,228 rows,
mtime 2026-08-26 09:00:02** — yesterday's cron.

**D — how production obtains `data_store/instruments.csv`**
🔴 🔬 **THE QUESTION'S PREMISE IS FALSE. `data_store/instruments.csv` DOES NOT
EXIST.** A whole-tree `find` (excluding `venv/`) returns **exactly one** file:
`config/instruments.csv`. ⛔ There is no `data_store` copy to obtain.

**E — does a fresh deployment expect a bootstrap load?**
🔬 **YES, and it FAILS CLOSED — ⛔ it does not degrade silently.** `main.py:2436-2446`
pre-loads inside a `try`, and the comment states the contract: *file missing →
`check_config_files_present` blocks with `missing_config_files`; present but corrupt
→ blocks with `instrument_cache_too_small`.* ⇒ A fresh deploy that boots before its
first 09:00 refresh **is blocked, loudly.** ✅ Correct behaviour.

**F — what *"config-driven placeholder"* meant** — 🔬 **NEITHER of the two offered
readings.** Source of truth found: `docs/locked_decisions.yaml:2892` —
*"`step_6_sector_strength`: sector present -> 1.0; missing -> 0.5 (placeholder for
v2.1)"*. It is a **SCORING stand-in**, ⛔ not a versioned mapping that SUPPLEMENTS
the source and ⛔ not a mechanism that SELECTS/CONTROLS it.
🔬 The deployed body is verbatim:
```python
def _step_6_sector_strength(self, signal, md, thr, direction) -> float:
    """Placeholder: 1.0 if sector provided, 0.5 if missing."""
    sector = md.get("sector")
    return 1.0 if sector else 0.5
```
🔴 **And its input is hard-coded `None`.** Chain verified end-to-end:
`_build_market_data(quote)` (`secondary_screener.py:378`) returns the dict at `:395`
containing **`"sector": None`** at `:413` — with the comment *"Still not in Kite
quote API; would need instruments cache"* — assigned at `:182`, passed as
`market_data=` at `:444`, read by `_step_6` as `md.get("sector")`.
⇒ 🔬 **`sector_strength` returns `0.5` for EVERY symbol, on EVERY signal.** It is a
**10-point step** (`scoring_weights.yaml:16`, weight `8.0` at `system_config.yaml:526`)
with **ZERO discriminating power** — it awards exactly half its points to every
candidate and can never separate two signals.
⚠️ ⭐ **I nearly reported a 93.6 %/6.4 % scoring skew.** The premise failed on
inspection: the score path does not read the CSV at all. 🏷️ Recorded because the
near-miss is the lesson — *verify the finding's premise.*
⚠️ `tests/unit/test_forward_shadow.py:32/37` asserts **both** branches (`1.0` and
`0.5`) from synthetic data, so the suite looks healthy while production can only
ever take one branch.

⇒ 👤 **A design choice IS still genuinely required, and it is now a precise one:**
should the score path be wired to `instrument_cache.sector()` (the source that
already exists), or should step 6 be retired? ⛔ I did not build either.
🔴 `sector_cap_mode` **STAYS `observe`** — untouched.

### 5.4 — P2 F6: one bounded check only (⛔ the lifecycle work itself NOT started)

🔬 **`c39e799` is NOT an ancestor of `bc9a9f5`** ⇒ **F6 is BUILT and NOT DEPLOYED**,
confirming the standing memory entry rather than assuming it.
🔬 `orders/cnc_gtt_monitor.py`: **737 lines deployed vs 1,029 on the branch (+292)**.
⇒ This is the same measurement that makes F6 the cleanest OPTION-A candidate (§4 Q10).
⛔ The F6 lifecycle investigation itself was **not** started.

### 5.5 — NOT REACHED
- **P3 F6-leg · P4 F4 observability · P5 F11 · P6 S6** — ⛔ not started.
⭐ The window went to Section E and the F2 inventory, which FILE 13 ordered first
and second. ⛔ No non-core reporting consumed a core-fix window.

---

## 6 — MEMORY UPDATES · AND WHAT I DID NOT MEASURE

### What I did NOT measure — plainly
1. ✅ **RESOLVED — the armed revert trigger IS NOW TRACED end-to-end**
   (📄 `REVERT_TRIGGER_TRACE_27-Aug-2026.md`): quantity **B**, rule **E**,
   🔬 `carry>0` met on **0 of 9,289** samples ⇒ never evaluable.
   ⛔ It remains **DISARMED BY POLICY**; ⛔ no revert may be executed on its signal.
2. **E-4 cannot prove the resolver fix is live.** 0 hits on three surfaces, but
   the phrase `strategy resolver` returns 0 too, so the search cannot distinguish
   *"did not fire"* from *"never appears here"*. The flat book means the path was
   very likely never exercised.
3. **E-6 was not exercised.** The 45 s morning check was deliberately not run
   (a fresh login could invalidate the live session token; the script is
   interactive). ⭐ Its premise was confirmed by measurement instead — and today
   could not have gone red at 15 s either, so today was never a discriminating test.
4. **Whether K-1's understatement ever changed a position size** — the `capital`
   rung's binding frequency is unmeasured.
5. **The branch was never built or run.** Every §4 figure is a git/static read.
   ⛔ No branch test was executed; F2's correctness remains UNKNOWN.
6. **F9, P2–P6** — not started.
7. ✅ **RESOLVED — the 09:15 `carry` leg of E-5 is MEASURED in §7** (`carry 0.0`,
   27-Aug 09:23 IST, read-only from the VM after the PC power-down).
   ⛔ It remains a **flat-book** observation — ⛔ not carry correctness.

### Memory updates — before / after bytes

| file | before | after | Δ | what went in |
|---|---|---|---|---|
| `MEMORY.md` | 9,297 | **9,500** | +203 | RESUME → the proven boot; F2 line re-measured (48/**81**, 102 files); ONE hot line for the HELD MIS ×3.5 |
| `MEMORY_HAZARDS.md` | 17,496 | **18,645** | +1,149 | K-1's capital-path invariant · the HELD MIS ×3.5 DO-NOT · the F2 inventory figures |
| `MEMORY_RULES.md` | 9,375 | **10,160** | +785 | *a guard on a superseded method guards nothing* (Tests) · *untracked is branch-relative* (Method) |
| `MEMORY_BOARD.md` | 50,645 | **52,391** | +1,746 | the four items awaiting Rama: F2's three options · K-1 OPEN · NI-16 → QUEUED · E-7 · the two operative files |
| `UNPUSHED_PENDING_DEPLOY_LEDGER.md` | 1,450,922 | **1,455,084** | +4,162 | new top block: the timestamped boot chain, the E-6 reasoning, **the correction to this ledger's own F2 figures**, both findings, K-1 |
| `docs/audit/SECTION_E_AND_F2_INVENTORY_27-Aug-2026.md` | — | this file | new | the same record, in the repo |

🔬 **Both memory guards re-run and CLEAN after the edits:**
`wc -c MEMORY.md` = **9,500 < 24,000** ✅ ·
`LC_ALL=C awk 'length>(index($0,"🔝")?450:300)' MEMORY*.md` **prints nothing** ✅
(it caught four over-length lines on the first pass; all four were trimmed).

⛔ Superseded ledger text was **retained, not deleted** — the new top block
corrects the 77-behind and 12-file figures in place above them.



---

## 7 — THE 09:15 `carry` LEG OF E-5 — 🔬 **MEASURED 27-Aug 09:23 IST**

> ⚠️ **WHY THIS SECTION IS SEPARATE AND LATE.** §6 item 7 forward-referenced a §7
> that did not exist: at 08:32 the 09:15 window had not yet arrived, so the leg was
> left `⏳ pending`. 🔬 **The PC powered down at ~09:15 and rebooted 09:17:46**
> (`LastBootUpTime`), destroying the session before §7 could be written.
> ⭐ **The VM was never affected** — `ExecMainPID 492196` / `NRestarts=0` /
> `ExecMainStartTimestamp Thu 27-Aug 08:15:15` are **unchanged**, so this is the
> SAME uninterrupted run E-3 proved, ⛔ not a re-boot. The measurement was
> therefore recoverable in full from VM-side artifacts, ⛔ nothing re-run,
> ⛔ nothing manufactured.

### E-5, second leg ✅ **PASS — `carry` IS ZERO, AND IT IS LOGGED EXPLICITLY**

🔬 The value is a named field, ⛔ not an inference from absence:

```
{"ts":"2026-08-27T09:15:00.049+05:30","level":"INFO","logger":"fund_manager",
 "msg":"fund_manager.sync_from_broker",
 "broker_cash":10544.5,"carry":0.0,"new_total":10544.5,"old_total":10544.5}
```

| # | artifact | time (IST) | value |
|---|---|---|---|
| 1 | `get_margins` (the sync's input) | `09:15:00.000` → `.045` | 44 ms |
| 2 | **`fund_manager.sync_from_broker`** | **`09:15:00.049`** | **`carry 0.0`** · `broker_cash 10544.5` · `old_total 10544.5` → `new_total 10544.5` |
| 3 | `main: market_open_margin_sync` — *"capital re-synced at 09:15"* | `09:15:00.049` | **`delta 0.0`** · `old 10544.5` → `new 10544.5` |
| 4 | **`fm_ledger 11501`** `SYNC` / bucket `both` | `09:15:00.046783` | `10544.50 → 10544.50`, `margin_delta 0.0` · `pnl_delta 0.0` · `costs 0.0` · reason *"broker sync: 10544.50 -> 10544.50"* |
| 5 | **`get_holdings` (2nd call of the day)** | `09:15:00.803` → `.819` | 15 ms, **`result_summary "0 holdings"`** |

✅ **FROZEN EXPECTATION MET: ZERO.** Measured on **four independent surfaces** —
the fund_manager log field, the `main` sync line, the persisted `fm_ledger` row and
a fresh broker `get_holdings` — ⛔ not one reading repeated.
✅ In the §2 vocabulary: **`capital_delta_rupees` = ₹0.00** at the 09:15 sync.
⛔ **`carry = 0` IS STILL NOT CARRY CORRECTNESS.** The book was flat all night, so
the carry path was never asked to carry anything. ⭐ This is a **second flat-book
observation**, ⛔ not evidence the delivery-carry logic works.

### Session health at the time of measurement (09:23–09:25 IST)

| check | 🔬 measured |
|---|---|
| `ActiveState` / `SubState` | `active` / `running` |
| `ExecMainPID` · `NRestarts` | **492196** · **0** — ⛔ no restart, ⛔ not a re-boot |
| `ExecMainStartTimestamp` | `Thu 27-Aug 08:15:15 IST` — identical to E-3 |
| today's log | 1,223 lines · **0 ERROR** · **1 CRITICAL** · **2 WARNING** |
| the 1 CRITICAL | `08:15:16.535` `kill_switch` — the **known** startup alarm, resolved by the auto-clear **3 ms later**. ⛔ Unchanged since 08:32; ⛔ no new CRITICAL |
| `system_events` today | **still exactly two rows** — `3796` KILL_AUTO_CLEARED · `3797` STARTUP. ⛔ Nothing fired in the 70 min since |
| `kill_switch_state` | `INACTIVE` — `auto_clear_stale`, `main.auto_clear_stale` |
| open positions · trades today | **0** · **0** |
| service liveness | last log line `09:25:19.602` — polling normally |

🔬 **The two WARNINGs, now named** (§3 counted them; ⛔ it did not enumerate them):
1. `08:15:16.539` `kill_switch` — the auto-clear itself. **Expected.**
2. `08:15:27.355` `core.config_validator` — **`CONFIG_UNACCESSED: 388 config keys
   never read`**. 🏷️ RECORDED, ⛔ **NOT CHASED (M-2)** — it is a boot-time
   coverage report, not a fault, and it changed no decision today.
   ⚠️ 💭 It is worth a bounded look **later** only because a two-book split adds
   config surface, and an unread key is exactly how a delivery key goes inert.

### The three cron preflight phases — ⛔ none of these existed at 08:32

| phase | mark rc | completed | verdict |
|---|---|---|---|
| A (`08:30`) | **0** | `08:30:03` | ⚠️ `READY_WITH_WARNINGS` — 49 ✅ / **0 🔴** / 2 ⚠️ / 1 ⏭ (52) |
| B (`09:14`) | **0** | `09:14:02` | ✅ **`READY`** — 8 ✅ / **0 🔴** / 0 ⚠️ / 1 ⏭ (9) |
| **C (`09:15`, `--watch-sec 285`)** | **0** | **`09:19:47`** | ⚠️ `READY_WITH_WARNINGS` — 2 ✅ / **0 🔴** / 1 ⚠️ (3) |

🔬 **Phase C's single WARN is `signals_arrived` — *"no signals received yet"*.**
⭐ **That is EXPECTED, ⛔ not a fault:** preflight A measured
`trading_hours.entry_start=10:00 [LAUNCH-PHASE]`, and phase C closed at 09:19:47 —
**40 minutes before entries open.** ⛔ Do not read it as a webhook defect; the same
run proved `webhook_responsive` ✅ and `webhook_backpressure` ✅ `queue 0`.
🔬 Corroborating state from A/B: `kill switch INACTIVE` · `no open positions at
start` · `no resting/active orders` · `no trades stuck in EXITING` ·
`schema v45 OK` (⛔ still not v46) · `capital deployed 0.0%` (`margin_used ₹0`) ·
`vm_ip_unchanged` · `db_writable`.
⚠️ A's 2 WARNs: `kite_instruments_fresh` (*"instruments from last trading day
2026-08-26; today's 09:00 refresh pending"* — A runs 08:30, the refresh cron is
`0 9`, ⇒ **structural, expected**) and `long_strategies_enabled` (a standing
review note, ⛔ not new).

### ⚠️ ONE OBSERVATION RECORDED, ⛔ NOT CHASED, ⛔ NOT A DEFECT CLAIM

🔬 Day-start capital moved **₹10,567.60 (26-Aug `INIT`, `ledger_id 11411`) →
₹10,544.50 (27-Aug `INIT`, `ledger_id 11500`, `08:15:24.467`) = −₹23.10.**
🔬 Yesterday's local realized was `RESET_PNL` *"previous pnl=−18.79"* (`11498`,
`15:17:02`) **plus** trade `11499`'s `pnl_delta −6.57` (`15:19:53`) = **−₹25.36**.
⇒ residual **₹2.26**.

🔴 **⛔ THIS IS NOT PRESENTED AS A DISCREPANCY.** Both `INIT` figures are broker-
sourced, so this is a broker-to-broker day-over-day read, ⛔ **not** the forbidden
`_total` vs broker-net comparison. ⭐ A residual of this shape is exactly what
**K-1 (§5.1)** predicts: the broker settles CNC/MIS charges **out of market**, so
overnight settlement and the local intraday net are ⛔ not required to agree to the
paisa on any single day.
⚠️ 💭 **Also recorded, ⛔ not chased:** trade `11499` closed at `15:19:53` — **2 min
51 s AFTER** the `RESET_PNL` at `15:17:02`. 💭 An EOD reset preceding a same-day
trade close is an **ordering question worth a bounded check**, ⛔ not a finding:
I did ⛔ **not** measure where that −6.57 landed. 🏷️ **UNPROVEN.**
⛔ Nothing was tuned, changed or "reconciled". ⭐ **It goes on the board as a
question, ⛔ not on the ledger as a fault.**

### What §7 changes — and what it does ⛔ NOT change

- ✅ **E-5 is now COMPLETE: both legs PASS.** §3's `⏳ pending` is discharged, and
  §6 item 7 is closed.
- ⛔ **E-4 is still UNPROVEN** — nothing here touches the resolver question.
- ⛔ **E-6 is still UNPROVEN** — the 45 s morning check was still not run, and
  ⚠️ today remains a **non-discriminating** day for it (12.98 s ≪ 15 s).
- ⛔ **E-7 is still 👤 RAMA'S** — the TREE was ⛔ NOT advanced. A second clean
  reading is still ⛔ not authorisation.
- ⛔ **§4 is untouched.** ⛔ No F2 decision, ⛔ no branch operation, ⛔ no push.
  🔬 The `feat/delivery-config-split` working tree was ⛔ **never** touched, and
  `deploy/zerodha_morning.ps1` remains preserved (§0) — the power-down did ⛔ not
  reach it: both copies live outside the repo.
- 🔴 **BOOT PROOF ≠ FEATURE PROOF still stands.** A clean 09:15 sync on a flat book
  proves the sync path runs. ⛔ It proves nothing about F2, the resolver, carry
  correctness, G3, or the armed revert trigger — which remains **DISARMED BY
  POLICY and UNTRACED.**

⛔ **Read-only throughout.** No service was started/stopped/restarted, no order, no
GTT, no push, no write of any kind to the VM. Every figure above is a `sqlite3
-readonly` query, a log read, or `systemctl show`.
