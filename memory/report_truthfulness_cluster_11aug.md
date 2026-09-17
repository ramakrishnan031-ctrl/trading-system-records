---
name: report-truthfulness-cluster-11aug
description: "11-Aug-2026 measured cluster: reconcile_positions exit 2 means MISMATCH-FOUND but is rendered FAILED; watchman/flow_trace generators are not scheduled at all so the EOD MISSING line is meaningless; the EOD SUMMARY SOFT_KILL line is a hardcoded string that contradicts its own readiness block. Plus the Web Claude framing call that was WRONG."
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-11T04:47:44.559Z
  originSessionId: 8ed4c442-48ea-4d03-8a20-48adca6b269d
---

# 11-Aug-2026 — THREE MEASURED REPORT-TRUTHFULNESS DEFECTS + ONE WRONG CALL

> ## ⭐ **THE STANDING PATTERN, THIRD AND FOURTH INSTANCE THIS WEEK: THE DEFECT IS IN WHAT THE SYSTEM *CLAIMS*, ⛔ NOT IN WHAT IT *DOES*.**

⛔ **All four are `<MEASURED · REPORTED · NOT FIXED>`.** ⛔ No code, config or schedule was touched.

---

## ① 🔴 `reconcile_positions` — **`exit 2` IS A SUCCESSFUL DETECTION, RENDERED AS `FAILED`**

**(P) `scripts/reconcile_positions.py:428-434` @ `645728d`:**
```python
has_mismatch = any(r["status"] not in ("OK", "ERROR") for r in results)
has_error    = any(r["status"] == "ERROR" for r in results)
if has_mismatch: return 2      # ← the reconciler WORKED and found a real discrepancy
if has_error:    return 1      # ← a genuine error
return 0
```
**(P) `_cron_main:437-450` maps EVERY non-zero rc to the single label `FAILED`** ⇒ *"your DB disagrees with the broker about real positions"* and *"I crashed"* print **identically** in the EOD.

🔍 **WIDTH OF THE BACKWARD HUNT, STATED: table `cron_heartbeat`, `job_name='reconcile_positions'`, ALL 40 ROWS = the job's ENTIRE recorded history, `2026-06-19` → `2026-08-10`.** ⛔ No narrower window. Tally **33 SUCCESS · 6 FAILED · 1 SKIPPED**.

| date | rc | meaning | `eod_broker_reconcile` same day |
|---|---|---|---|
| 19-Jun | **1** | genuine error | — |
| 29-Jul | 2 | mismatch | ISSUES: IOB, MSUMI, SJVN, SOUTHBANK, TRIDENT |
| 31-Jul | 2 | mismatch | ISSUES: same 5 |
| 06-Aug | 2 | mismatch | ISSUES: ATULAUTO |
| **07-Aug** | 2 | mismatch | **ISSUES: DIFFNKG** |
| **10-Aug** | 2 | mismatch | **ISSUES: DIFFNKG, MANINFRA** |

⭐⭐ **EXACTLY ONE genuine error in the job's whole life. Every `exit 2` day matches an independent `ISSUES` day — two separate mechanisms, perfect correlation.**

> ## 🔑 **⇒ "WOULD A *PASSING* `reconcile_positions` HAVE FLAGGED DIFFNKG/MANINFRA?" CARRIES A FALSE PREMISE. A pass means nothing was wrong. IT FLAGGED DIFFNKG ON 07-Aug AT 15:45 — TWO TRADING DAYS BEFORE the 11-Aug exit — AND BOTH ROWS ON 10-Aug. THE DETECTION FIRED CORRECTLY AND ON TIME; THE *LABEL* BURIED IT.**

⚠️ **It had NOT run on 11-Aug as of ~10:30** — 0 rows for that date; scheduled `15:45 Mon-Fri`.
🧪 **PARITY: a CRON/REPORT path — SHARED, mode-independent** (takes no trading decision).

---

## ② 🔴 `watchman` / `flow_trace` — **THE GENERATORS ARE NOT SCHEDULED AT ALL**

⛔ **THE HYPOTHESIS *"the generator is gated on the service being alive"* IS REFUTED. ⭐ It was measured, ⛔ not inherited — precisely because the cron chain had already been proven independent of the service.**

**(P) `crontab -l | grep -ci "watchman\|flow_trace"` = `0`.** **(P) ZERO `cron_heartbeat` rows for either, ever.**
**(P) `scripts/system_manager.py:409-410` `_check()`s for `watchman_{day}.md` / `trace_{day}.md` UNCONDITIONALLY every EOD; `_check` (`:395-401`) is a plain exists/size/mtime test with NO gate of any kind.**
**(P) Last artefacts: `watchman_2026-07-21.md` (21 days stale) · `trace_2026-06-22.md` (50 days stale).**

> ## ⇒ ⭐ **WORSE THAN THE HYPOTHESIS: it is not that HARD_KILL days lose their forensic record — ⛔ EVERY day loses it, and the EOD has asserted MISSING every single day for WEEKS. The line says NOTHING about the service.**

🔴 **This IS the already-owed Rama item *"`watchman`/`flow_trace`: retire the CHECK or the producer"* — now MEASURED rather than suspected.**

---

## ③ 🔴 THE EOD `SUMMARY` LINE IS A **HARDCODED STRING** THAT CONTRADICTS ITS OWN READINESS BLOCK

**(P) `scripts/system_manager.py:886,900` — `generate_full_report`:**
```python
reasons = [r.soft_kill_reason for r in results if r.soft_kill_reason]
if reasons:
    lines.append("🚫 SOFT_KILL triggered for tomorrow — manual deploy/resume.sh required")
```
It fires on **any** non-empty reason and ⛔ **NEVER consults the readiness verdict.** On 10-Aug the setter was **`:597` `"HARD_KILL currently active"`**, while `TOMORROW READINESS` (`:725-729`) had already printed *"auto-clears it (HEADLESS GUARANTEE). No action needed; ⛔ do NOT run deploy/resume.sh for this."* **The two blocks are computed independently and never reconciled.**

🔑 **THREE defects in ONE line:** ① it hardcodes **`SOFT_KILL`** while `:597` set a **HARD_KILL** reason — ⛔ the static string can NEVER name the real state ② it demands `resume.sh` in the EXACT case readiness forbids it ③ **SIX setters** (`:235 :249 :266 :282 :442 :597`) all print this same SOFT_KILL sentence, including *DB integrity failed* and *position cap exceeded* — ⛔ **none of which is a SOFT_KILL. The mislabel is SYSTEMATIC, not specific to the kill check.**
⭐ **CAN IT EVER BE RIGHT? Only by coincidence** — when the kill happens to be same-day-dated AND genuinely SOFT_KILL. ⛔ **Its correctness is unconditional on the facts it asserts.**
⚠️ **11-Aug PROVED the readiness block right and the SUMMARY wrong: the boot auto-cleared at `08:15:52` and no `resume.sh` was run.** ⛔ **The SUMMARY is the line a tired reader acts on at 18:45.**

---

## ④ 🏷️ **A WEB-CLAUDE FRAMING CALL, RECORDED AS *WRONG* — same corpus and format as the frozen predictions**

📜 **The midday card was headed *"THE RUNNING CODE IS NOT THE AUDITED CODE (LIVE, NOW)"*.** ⛔ **The premise was stronger than the evidence supports, and Rama accepted the correction on the record.**
**(P) zero trading-path readers** — `registered_direction()` has **ZERO callers** (width: whole tree, all `*.py`, minus `venv/` and `tests/`); `load_registry()` has **exactly ONE non-test caller and it is the WRITER** (`strategy_registry_officer.py:224`). **(P) `docs/expected_alarms.md:422` already names this exact alarm and `:432` gives the discriminator — *escalate if the diff names any file OTHER than this one* — which the diff does NOT trip.**

> ## ⭐⭐ **THE LESSON, AND IT IS THE SAME ONE AGAIN: THE PREDICTION WRITTEN *BEFORE* THE FACT HELD; THE FRAMING CONSTRUCTED *AFTER* THE FACT OVERSTATED.** ⛔ **Do not bury it.**

📌 **CORRECT WORDING, VERBATIM, ⛔ use this and nothing else:**
> **"Live configuration-file drift exists; measured code-path analysis shows no current trading behavioural effect."**

⛔⛔ **NEVER write *"the deployed tree is identical to audited code"* — it is byte-different from `645728d` (VM blob `41a14df1…` vs `b03f4ed0…`) and the GOVERNANCE finding survives.**

---

## ⑤ 📎 TWO DOCUMENTATION DEFECTS FOUND IN THE SAME SWEEP — ⛔ RECORDED SEPARATELY ON PURPOSE

⭐ **Kept apart so a future reviewer who "repairs" the harmless runtime drift cannot accidentally close the real one.**
- **D1 `claim-vs-code`** — `docs/audit/signal_mortality_census_19jul2026.md:390` claims *"Directions are taken from `config/strategy_direction_registry.yaml`"*. ⛔ **Refuted by the caller measurement above.**
- **D2 `self-erasing-invariant`** — `scripts/strategy_registry_officer.py` writes via a PyYAML round-trip that **STRIPS THE 25-LINE HEADER**. ⭐ **That header was the ONLY in-repo statement of the *"nothing reads direction from here"* invariant** ⇒ 🔑 **the officer's own write destroys the documentation that justifies the officer being harmless.**

## ⑥ 💱 **THE EOD RISK REPORTER AND THE LIVE SIZER READ CAPITAL FROM TWO DIFFERENT SOURCES**

**(P) `_day_capital` (`scripts/system_manager.py:148`) → `store.get_day_opening_capital(day)` = the `fm_ledger` **INIT row only**, label `"fm_ledger"` (`:157`); fallback `accounts.csv` `paper_capital` (`:160-165`).** **(P) the live sizer reads `total_capital = snap.total` (`capital/position_sizer.py:293`) from FundManager.**
⇒ ⚠️ **A mid-day payin or a `SYNC` delta NEVER reaches the EOD risk envelope.** ⛔ **Only safe while written down — DANGEROUS the moment an operator reads the EOD envelope as describing what the sizer actually used.**
✅ **`₹210` on 10-Aug was a correct read of a seed that DEATH froze** (INIT written 08:15 pre-payin, service hard-killed 08:15:25, nothing re-based it). ⛔ **The reader is SOUND; it governed the REPORT, ⛔ never the TRADING.**

[[feedback-never-classify-by-free-text]] [[feedback-absence-needs-wide-check]] [[tautological-check-class-05aug]] [[capital-vocabulary]] [[feedback-status-label-rule-27jul]]

---

## ⑦ 🔴 **THE 60-SECOND CNC SELF-CANCEL — THE REAL DELIVERY BOTTLENECK, FOUND 11-Aug**

> ## 📌 **RECORD IT IN THESE WORDS, ⛔ AND NEVER AS A "qty-0 SIZING FAILURE":**
> **"`qty_planned` > 0; `qty_filled` = 0 because the LIMIT order remained unfilled and was cancelled after ~60 s. No `rejection_reason` was written."**

⭐ **THE SIZER WORKED.** FUSION `qty_by_risk 24` / `qty_by_capital 14` / `qty_by_concentration` **4 ← binds** → tier `0.70` → **`qty_planned 2`**, margin `₹434.29` · ROLEXRINGS `31` / `19` / **`6` ← binds** → tier `0.50` → **`qty_planned 3`**, margin `₹499.94`. **(P) `risk_engine.approve … intent=DELIVERY approved=True failed_check=none`.**

**(P) THE TIMEOUT: `broker/order_monitor.py:1076` (OM7) — *"If order has been open longer than `fill_timeout_sec`, cancel it."* Config key **`fill_timeout_sec: 60`** at `config/system_config.yaml:141`, validated `>= 5` at `core/config_loader.py:261-265`, wired at `main.py:2648`.** ⛔ **A CONFIG KEY, ⛔ not a literal — and it is PRODUCT-BLIND.**
⚠️ **`limit_grace_sec: 120` is NOT related — it belongs to `orders/eod_squareoff.py` (the EOD LIMIT→MARKET promotion). ⭐ A suspected 60-vs-120 conflict was CHECKED AND REFUTED, ⛔ not asserted.**

> ## 🔑🔑 **IT IS PRODUCT-BLIND BUT NOT PRODUCT-NEUTRAL — CNC IS PRESSED AGAINST THE WALL.**
> 🔍 **WIDTH: whole `orders` table, `leg='ENTRY' AND placed_at IS NOT NULL`, **442 rows**, `2026-06-15` → `2026-08-11`.**
> **CNC `COMPLETE` avg time-to-fill `35.34 s` (min `5.41`, max **`59.70`**) vs MIS `16.05 s` (min `0.21`, max `60.05`).** ⇒ ⭐⭐ **THE SLOWEST SUCCESSFUL CNC FILL IN ALL HISTORY CLEARED THE 60 s CANCEL BY `0.30 s`.**
> **CANCEL RATES: CNC `10/15` = `66.7 %` · MIS `200/427` = `46.8 %`.**

🔴 **`rejection_reason` IS EMPTY on both cancelled orders, and no writer populates it on the OM7 timeout path** *(width: `rejection_reason` across `orders/` + `core/` — the only hit is a DOCSTRING at `orders/entry_engine.py:55`)*. ⇒ ⛔ **SILENCE IS THE FINDING.** ⭐ **Same family as the concentration rejection, which DOES record its reason and all three operands — one path records, the other does not.**

✅ **CAPITAL IS RELEASED — ⛔ NO LEAK, and this was the live-money question:** `RESERVE 456.004164` `10:02:15.467` → `RELEASE` `10:03:18.155` (**2 ms** after the broker cancel) · `RESERVE 524.935026` `10:11:14.907` → `RELEASE` `10:12:19.388` (**1.5 ms** after). **The positional bucket returns to EXACTLY `₹3,193.68` = `0.30 × 10,645.60` after every pair.**
⚠️ **FILED, ⛔ NOT CHASED: the reservation carries a ~5 % buffer over `trades.margin_reserved` (`1.05` on both), and `fm_ledger.trade_id` is EMPTY on RESERVE/RELEASE rows ⇒ reservations are NOT linked to their trade — these were matched by timestamp + amount.**

⛔⛔ **FIX 1 `2e1f109` IS NOT THE CAUSE AND ⛔ TONIGHT'S INSTALL MUST NOT BE JUSTIFIED BY THESE TWO FAILURES** — `qty_by_capital` was **14** and **19** against binding concentration **4** and **6**, so capital was NEVER binding. ⭐ **Tonight is scheduled maintenance; it unblocks nothing in delivery.**
⭐ **AND THE *"configured, started and inert"* HYPOTHESIS IS REFUTED: 5 of 15 CNC entries COMPLETED (05, 06, 07-Aug) — delivery FILLS SOMETIMES.** ⛔ Not a universal CNC success rate; the population is named.
🧪 **PARITY: sizing path SHARED (`position_sizer.py`, ZERO `is_paper` refs). ORDER-CANCELLATION PARITY = `CANNOT DETERMINE` — ⛔ not traced, and ⛔ "not traced" is NEVER written as "shared".**

---

## ⑧ 🏷️ **METHOD CORPUS — FOUR ENTRIES, ⛔ NONE SOFTENED, BOTH DIRECTIONS KEPT**

1. **Web Claude WRONG** — midday §1 headed *"the running code is not the audited code"*; the premise was stronger than the evidence, and it was measured down.
2. **VS Code Claude (me) WRONG** — concluded `MASTER_REGISTER.md` did not exist, from a root worktree **parked on `feat/delivery-config-split` where `main`'s files are not checked out**, while the card had named the file twice. ⭐ **Fourth instance this week of *the thing visible is not the thing that governs*.**
3. **Web Claude WRONG AGAIN, SAME DAY** — the follow-up card's §2 premise said *"the sizer produced qty 0"*. ⛔ **It did not — `qty_planned` was 2 and 3.** ⭐ **Recorded even though the investigation it triggered was the day's best finding: a useful consequence does not make a premise true.**
4. ⭐⭐ **A CORRECTION CAN ITSELF BE THE ERROR.** The ledger's *"correction"* on `feat/delivery-config-split` (*"six doc files… a docs-freshness question"*) **softened a TRUE warning back into the trap**; measurement restored it (11 files, `3cf3729` NOT an ancestor, OLD tier values). ⛔ **Keep the original warning, the correction AND the refutation all three visible.**

📌 **REGISTER LOCATION — THE TRAP THAT CAUSED ENTRY 2, RECORDED SO IT DOES NOT RECUR:** 🔑 **THE FINAL REGISTER IS `D:\Projects\trading-system-main\docs\MASTER_REGISTER.md`** *(committed on `main`; `:3` = "THIS FILE WINS")*. ⛔ **IT WILL NEVER APPEAR IN `D:\Projects\trading-system\docs\` while the root is parked off `main`.** ⛔ **DO NOT copy it into the root** (`:34` forbids it) · ⛔ **DO NOT create `master_pending.md`** (`:9` — *"UNDATED BY DESIGN. Dated filenames produced the chain."*). ⭐ **`MASTER_PENDING_01-Aug-2026.md` is a MERGED HISTORICAL SOURCE, ⛔ not the register.**
🗄️ **PRESERVATION: the 10-Aug copy (`4e132b3a…`) was written to a SESSION SCRATCHPAD and is GONE — the directory survives and is EMPTY.** ✅ **Re-preserved 11-Aug ~11:27 IST at `D:\Projects\_preservation\MASTER_PENDING_01-Aug-2026__preserved_2026-08-11T1145IST.md` (`sha256 1aba53f3…`, 410,494 B), verified OUTSIDE every git worktree and every scratchpad.** ⛔ **A SESSION TEMP DIR IS NOT A PRESERVATION LOCATION — measured, not assumed.**

## Index line relocated from `MEMORY_BOARD.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 656 B (budget 450 B). The index now carries a hook and this link.

- 📢🔴🔝 **[11-Aug CLUSTER — THREE MEASURED REPORT-TRUTHFULNESS DEFECTS + ONE WRONG CALL, `<MEASURED · NOT FIXED>`](report_truthfulness_cluster_11aug.md)** — 🔑 **`reconcile_positions` `exit 2` MEANS *mismatch FOUND* and is rendered `FAILED`** *(width: all 40 `cron_heartbeat` rows, 19-Jun→10-Aug; ⭐ **it flagged DIFFNKG on 07-Aug, two trading days early — the label buried it**)* · **`watchman`/`flow_trace` have ZERO crontab entries ⇒ the "service-alive gate" hypothesis is REFUTED and EVERY day loses the record** · **the EOD `SOFT_KILL` SUMMARY is a HARDCODED string contradicting its own readiness block, fired by SIX setters.**
