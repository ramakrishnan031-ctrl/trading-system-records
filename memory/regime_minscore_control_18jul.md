---
name: regime-minscore-control-18jul
description: "18-Jul Part A — per-day active min_pass_score reconstructed. config_snapshots is authoritative but only from 02-Jul (12 of 23 book days UNDETERMINABLE). 6 days at 60, 4 at 55, 1 split. The control leaves ~1-2 days per cell, hardening the NOT-DETERMINABLE verdict. ACTIONABLE: freeze min_pass_score while data accumulates."
metadata: 
  node_type: memory
  type: project
  originSessionId: b9e84959-b70c-4ce6-9521-3db6f6dd3fee
---

**📉🔬 Q10 PART A — PER-DAY ACTIVE MIN-SCORE CONTROL. Done 18-Jul-2026 (READ-ONLY, no token).**
Report `docs/audit/regime_thesis_minscore_control_18jul2026.md`. Docs-only, **UNPUSHED**. `mode=ro`
throughout; nothing changed. **Part B NOT started** (needs Rama's token refresh + confirmation).

**A1 — AUTHORITATIVE SOURCE = `config_snapshots`** (full resolved `AppConfig` written at EVERY boot —
`main.py:2099`, writer `core/config_snapshotter.py:141-190`, schema `core/schema.sql:1459-1470`, v41);
field `scoring.min_pass_score`. **⚠️ It only starts 02-Jul ⇒ covers 11 of the 23 book days.**
**Second, INDEPENDENT source: `signals.status = REJECTED_SCORE_<n>`** — the score of every
screen-rejected signal ⇒ a rejection recorded at 55–59 PROVES the threshold is 60. Exists only from
09-Jul (before that, volume was 3–463/day with **no score-bearing status at all**; from 09-Jul it
jumps to ~7,800/day and the statuses appear). **The two agree PERFECTLY on all 6 overlapping days.**
**Strategy-level overrides: all 16 YAMLs `min_score: 0`, none ever non-zero in the window ⇒ the
GLOBAL value governs universally (no override confound).**

**⚠️⭐ GIT DATES ARE NOT SAFE — PROVEN, not assumed.** `config_snapshots` shows **06-Jul had TWO boots:
08:15:22 → min=60, then 11:20:12 → min=55** — but the commit that lowers it (`8a3e0b7`) is dated
**06-Jul 20:24, NINE HOURS AFTER it was already live on the VM. THE VM CONFIG CAN LEAD GIT.** Naive
commit-date→effective-date inference would have mis-dated it. (Second rule, also confirmed: config is
**loaded ONCE at boot**, so `61ae9cc` 10-Jul 10:04→60 did NOT affect 10-Jul, which still ran 55; 60
first appears at the **13-Jul** boot.) ⇒ **the June days are NOT inferable from git and were NOT guessed.**

**A2 — THE 23-DAY DISTRIBUTION: 6 days @ min=60 · 4 @ min=55 · 1 MIXED · 12 UNDETERMINED.**
* **60** (authoritative): 02, 03, 13, 14, 15, 16-Jul
* **55** (authoritative): 07, 08, 09, 10-Jul
* **SPLIT DAY 06-Jul**: 60 until 11:20:12, then 55
* **UNDETERMINED (12 = more than half the book)**: 15,16,17,18,19,22,23,24,25,29,30-Jun + 01-Jul.
  (git *suggests* 55 from 16-Jun and 60 from 19-Jun — recorded as a HYPOTHESIS ONLY, not a finding.)
**⇒ Rama's belief CONFIRMED: the book ran at both 55 and 60.**

**A3 — THE CONTROL KILLS IT (answer: NO cell survives, not remotely).** Cells (trades/days):
min=60 → LONG/INTRADAY 38/**6d**, SHORT/INTRADAY 5/3d, LONG/POSITIONAL 3/2d ·
min=55 → LONG/INTRADAY 25/**4d**, LONG/POSITIONAL 8/4d, SHORT/INTRADAY 3/2d ·
06-Jul mixed 8/1d · undetermined 65/12d (unusable). *(46+36+8+65=155 ✓; 6+4+1+12=23 ✓)*
**After the FULL control set (direction × horizon × min-score × 3 regime buckets): days per bucket =
LONG/INTRADAY 2.0 (min60) / 1.3 (min55) · LONG/POSITIONAL 0.7 / 1.3 · SHORT/INTRADAY 1.0 / 0.7.**
**⇒ ~1–2 DAYS PER CELL. Not weak statistics — effectively ONE OBSERVATION per cell.** A controlled
Bull-vs-Bear comparison would be comparing single days to single days.
**Second damage:** the 12 undetermined days are **June, the BETTER period** (LONG/POSITIONAL +48.0/+6.34R
vs −0.75R in July@60) ⇒ dropping them biases what remains toward the worse July stretch — **their loss
is not statistically neutral.**

**A4 — SIDE FINDING (observational ONLY, for D3/min_pass): the lower threshold looks worse.**
min=60: 6 days, 46 trades, −49.8, **win 45.7%**, sumR −6.39, **R/trade −0.139** ·
min=55: 4 days, 36 trades, −83.9, **win 33.3%**, sumR −11.89, **R/trade −0.330** (**~2.4× worse**).
Directionally what you'd expect (a lower bar admits weaker signals) **but 6 days vs 4, both loss-making,
and the groups are DIFFERENT CALENDAR WEEKS ⇒ fully confounded. An observation, not evidence.**

**⭐⭐ THE ONE ACTIONABLE OUTPUT: FREEZE `min_pass_score` WHILE DATA ACCUMULATES.** The ~2.2-month
estimate for detecting a LARGE effect assumes a **single** threshold throughout; **every mid-window
change re-fragments the sample and resets the clock** for the affected group. If the regime feature is
to be measurable at all, the threshold must stop moving. (Going forward `config_snapshots` makes every
day self-documenting, so this reconstruction problem is **historical only** and will not recur.)

**NET EFFECT ON Q10: the verdict is UNCHANGED and HARDENED** — "NOT DETERMINABLE at n=23" becomes
"not determinable, and the properly-controlled cells hold ~1–2 days each". [[regime-thesis-validation-18jul]]
**Part B still worth running when the token is live** (backfill + the tercile bands = the Phase 3
calibration asset, and it starts the clock) — but it cannot deliver a verdict.

**⚠️🔴 STANDING WARNING (restate every time): do NOT flip `regime.enabled`** during the V3/F1 shadow
soak — the V3 chain scores **8/40 Context** from regime (`gate_extreme` + `regime_fraction`); flipping
mid-soak changes the score distribution and makes pre/post shadow rows **non-comparable**.
[[regime-phase1-investigation-18jul]]

**📌 FUTURE PHASE 1 DESIGN (recorded, NOT built):** a **configurable PLUG-IN inside the existing
`regime/` module** — configurable window (default 09:15–09:59) · tunable thresholds · pluggable
algorithms · **VERSIONED regime logic** so each logged row records which algorithm version produced it
(critical when the verdict needs months of data). **The raw ingredients now accumulate automatically**
(Phase 0's 15:40 cron stores index candles daily; trades are recorded) ⇒ **the clock runs with NO new code.**

Related: [[regime-thesis-validation-18jul]] · [[regime-phase1-investigation-18jul]] ·
[[regime-phase0-17jul]] · [[bk1-long-short-scanner-17jul]].

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 716 B (budget 450 B). The index now carries a hook and this link.

- 📉🔬🔝 **[Q10 PART A — MIN-SCORE CONTROL 18-Jul](regime_minscore_control_18jul.md)** — per-day active `min_pass_score` reconstructed: **`config_snapshots` authoritative but starts 02-Jul ⇒ 12 of 23 book days UNDETERMINABLE** (not guessed). **6 days @60 · 4 @55 · 1 split (06-Jul)** ⇒ Rama's 55/60 belief confirmed. **⚠️ git dates PROVEN unsafe** (06-Jul was live at 11:20; commit stamped 20:24 ⇒ the VM leads git). **A3: the full control set leaves ~1–2 days per cell ⇒ NO cell clears n<10 — the NOT-DETERMINABLE verdict HARDENS.** A4 (observational): min=55 days worse (win 33.3% vs 45.7%). **⭐ ACTIONABLE: FREEZE `min_pass_score` while measuring.** [[regime-minscore-control-18jul]]
