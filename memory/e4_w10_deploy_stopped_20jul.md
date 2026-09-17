---
name: e4-w10-deploy-stopped-20jul
description: "E4/W10 deploy attempted 20-Jul with Rama's Option-A approval and STOPPED at the regression gate — merge was 0-conflict but 3 Q9 detectors fire, and the blocker is that the M-C1 live-seed safety argument must be re-derived."
metadata: 
  node_type: memory
  type: project
  originSessionId: d010c6e6-1e94-4ed6-9e89-609c3f52dda7
  modified: 2026-07-20T15:33:18.796Z
---

**E4/W10 DEPLOY ATTEMPTED 20-Jul-2026 AND STOPPED AT THE GATE. NOT DEPLOYED, never pushed.**
`PC == origin == VM bare == 80fbe86`; VM artifacts byte-identical; the E4 code is absent from the
VM tree; branch `e4-w10-pnl-contract` untouched at `ad34ee4`. Report:
`docs/audit/e4_w10_deploy_stopped_20jul2026.md`.

**The merge was flawless — ZERO conflicts**, including `main.py`, `PATHS.md`, `SYSTEM_MAP.md` (the
three the runbook predicted would conflict). Verified first that 0 commits landed on main since base
`4c148fb` for any of the five capital-path files. Reproduce with `git merge --no-ff e4-w10-pnl-contract`.

**⚠️ The historical "14-failure baseline" is UNUSABLE on the PC as currently configured** — `bash`
resolves to the **WSL stub** (`WindowsApps\bash.exe`), so `shutil.which("bash")` succeeds and ~20
bash-subprocess tests (`test_fix065_market_hours_guard` ×17, `test_t4_deploy_preflight` ×3) **run and
fail instead of skipping**. Plus the set is already clock/calendar dependent. **⇒ take a fresh BASE run
in the same window and diff the SETS; never compare to a historical absolute.**

| | BASE `80fbe86` | MERGE `abad483` |
|---|---|---|
| failed | 33 | 36 |
| xfailed | 1 | 0 |
| collected | 5001 | 5021 (+20) |

**`comm` merge-only = 3, base-only = 0.** All three are E4/W10 detectors added to main on **18-Jul,
AFTER the branch was cut on 17-Jul** — the branch could not have updated them, and the runbook
(19-Jul) predicted only "collected rises, failures stay at 14".

**⭐ THE BLOCKER is not a test edit.** `test_the_reader_is_a_different_quantity_and_is_not_involved`
encodes the safety argument for the **M-C1 live-seed cancellation**: it was argued safe *because* the
daily-loss reader (`SUM(pnl_delta) − SUM(costs)`) was a **different quantity** from the carryover (raw
`pnl_delta`). Post-fix both are `SUM(pnl_delta)` — **the same quantity**, so the premise is void. The
cancellation itself is **not** broken (`test_the_carryover_equals_exactly_what_phase_2_re_applies`
still passes); what must be re-derived is *why it is safe*. **Capital-path reasoning — needs its own
review before the retry.** The other two are deliberate flips (a `strict=True` xfail that XPASSes by
design, and the `−Σcosts` discrepancy pin).

**Runbook inaccuracies found (3):** `broker/cost_calculator.py` is **not new** (299→353; the +54 is
exact, the *function* is new) · the new test file has **20** tests, not 19 · "81 commits behind" is now 94.

**Checklist A3 was NOT flipped** (E4/W10 did not ship ⇒ Option-B stays correct) but **was fixed for a
separate defect: it was VACUOUS** — comparing `RESET_PNL.amount` (**always 0.0**) against an
`expected_reset` computed over *all* rows including the RESET row itself (**also 0.0**), i.e.
`0.0 == 0.0`. Now compares `pnl_delta`, excludes the RESET row, and is pre-armed with `18.29`, the
value that becomes correct the day this ships. [[feedback-verify-rc-not-output]]

Measured pre-deploy signature (Option-B holds exactly): 07-14 `17.58` · 07-15 `0.83` · 07-20 **`19.61`**
= −(Σδ−Σc). Post-deploy it must become −Σδ = **18.29**, differing by exactly Σcosts = 1.32.
Backup kept: `data_store/backups/pre_deploy_e4_w10_20260720.db` (`quick_check=ok`).
Related: [[e4-w10-done-17jul]] [[e4-w10-outcome-impact-19jul]] [[q9-live-seed-mc1-wired-19jul]]
