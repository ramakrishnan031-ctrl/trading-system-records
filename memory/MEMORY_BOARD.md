# Memory — OPEN WORK BOARD

**⭐ Read this before starting any batch.** Split out of `MEMORY.md` on **25-Jul-2026** — every line below is **VERBATIM**, nothing summarised.
Hazards/DO-NOTs stay **HOT** in **[`MEMORY.md`](MEMORY.md)** · stable facts in **[`MEMORY_REFERENCE.md`](MEMORY_REFERENCE.md)** · closed work in **[archive](MEMORY_ARCHIVE_2026H1.md)**. Same byte budget applies.

## 11-Sep-2026 (Fri) 02:52 — ⏸ RUN THESE IF THE SCHEDULED JOBS DID NOT FIRE · ⛔ NOTHING PUSHED · ⏸ RESUME HERE

- ⏸ **08:20 prod runtime check** → `memory/fallback_instructions/FALLBACK_11-Sep-2026_0820_PRODUCTION_RUNTIME_CHECK.txt`
- ⏸ **15:13 capture of the 15:03 exercise** → `memory/fallback_instructions/FALLBACK_11-Sep-2026_1513_BLOCK_A_EXERCISE_CAPTURE.txt`
  (⚠️ SAME DAY ONLY -- the broker's order book is daily.)
  ⭐ READ WITH the 11:15 file (delivered 11:11:58): production holds BSOFT SHORT ⇒ its exit is a BUY -- the 1.5 % /
  2.5 % band was chosen from a SELL-side table (BUY "consistently milder"): a BUY success ⛔ proves nothing for SELL.
  Attribute every exit by broker order id -- ⛔ never by exit_reason / closure_source (wrong both ways, S11-R22).
  ⭐ AND the 12:20 file (delivered 12:17:10): NAME the outcome -- (a) cancel OK → protected MARKET → filled ·
  (b) → rejected/partial · (c) cancel REFUSED → no exit (CANCEL_FAILED; a failed restore = S11-R8, not new) ·
  (d) closed on its own leg before 15:03 · (e) per source: cancel accepted while the leg FILLED → verify counts
  COMPLETE as settled → the MARKET still goes out. Only (a)/(b)/(e) exercise the MARKET path. The capture drops
  colon-format lines -- also dump the window: ssh trading-vm 'grep -h "T15:0"
  /home/ubuntu/systems/trading-system/logs/system_2026-09-11.log | grep -E "mis_autosq|mis_squareoff|CRITICAL"'

- ⏸ **10:12 TWIN Batch 1 watch #1** → `memory/fallback_instructions/FALLBACK_11-Sep-2026_1012_B1_TWIN_TRAFFIC_WATCH_1.txt`
- ⏸ **10:47 TWIN Batch 1 watch #2** → `memory/fallback_instructions/FALLBACK_11-Sep-2026_1047_B1_TWIN_TRAFFIC_WATCH_2.txt`
- ⏸ **15:16 the TWIN's own 15:03 capture** → `memory/fallback_instructions/FALLBACK_11-Sep-2026_1516_TWIN_BLOCK_A_EXERCISE_CAPTURE.txt`
  (the 09:35 file §3/§4, delivered 09:33:04 -- TESTING VM only; SAME DAY ONLY; VBB097's evidence, never production's.)
- ⏸ **14:50 BOTH VMs -- the MIS book from the BROKER, before 15:03** → `memory/fallback_instructions/FALLBACK_11-Sep-2026_1450_MIS_BROKER_READ_BOTH_VMS.txt`
  (the 10:45 file §1.1, delivered 10:44:45 -- read-only; alert Rama if any MIS is open; ⛔ never act on a position.)
- ⚠️ Session jobs `31f68404` (08:20) · `37d2a662` (14:50) · `0bf5092c` (15:13) · `97e80a55` (15:16) are a CONVENIENCE --
  they die with the session. `343596b7` (10:12) + `40669337` (10:47) were deleted when I ran those watches myself.
  Each fallback first checks HERE for its RESULT- marker, so a job that DID fire is never run twice.
  👤 09:35 file: "The session jobs are convenience. The files are the mechanism."
- 🔬 §1 (02:35 file): "12:45" was ⛔ NOT a typo -- the authorising file's header reads `ISSUED : 12:45 IST`; it
  reached the session at **12:39:52**; the removal ran **12:43:27**, REPLACE **12:43:37** ⇒ authorisation first,
  by 3 min 45 s. The header stamp is the inaccurate time. ⛔ Not 21:45 (= the CLOSE-SIX file). Annotated, not rewritten.
- 📋 §2: register ~~N 246 → 262~~ ⛔ **N = 304 BY COUNT (06:05, below)** -- S11-R5..R14 (10 items the record called "registered") + S11-R15..R20 (6 carried
  only in OPEN lists). Every candidate's only prior hit was the S11 "surfaced" paragraph -- 0 real rows.
- 🗺️ §4: WORKING SYSTEM_MAP.md current (17 of 17 ledger entries 09-11 Sep); COMMITTED copy stale since 02-Sep
  (`7d4970a`); one BOARD-only 09-Sep section (consent screen / ~~prod email dead since 07-Sep~~) reached neither.
  ✅ **CORRECTED 11-Sep-2026 11:21 -- "prod email dead" was STALE:** RESTORED 09-Sep, proven by contrast 64 s apart
  (12:21:30 `via TELEGRAM fallback` vs 12:22:34 plain `-> .delivered` -- RULES); a real sentinel by email 12:58:37.
  🔬 Re-measured today on production: degraded marker ABSENT, SMTP auth fails 0, and 09:20:30 / 10:00:33 / 10:25:36
  delivered with NO fallback tag. I repeated the stale note in the 10:47 report; the 11:15 file caught it.

- ⛔ Sequence: 08:20 → 15:03 observation → §1 + §2 → final review → Batch 1 → twin (direct copy) → review → prod.

## 13-Sep-2026 (Sun) 16:4x — 🧱 SECONDARY CONTEXT PHASE E BUILT · ⛔ UNPUSHED · ⏸ STOPPED FOR REVIEW

- 🧱 Same branch, tip `25807e3`. Zones + five checks + outcome contract. Report `docs/audit/SECONDARY_CONTEXT_PHASE_E_BUILD_13-Sep-2026.md`.
- 🔬 Gate 7F/6,576P/5S, failure set identical to `3143e55`, both comm empty. Mutations 105/105 RED. Full entry -> [[unpushed-pending-deploy-ledger]].
- ⭐ With every Rama number unset the engine measures everything and renders NO verdict — the state shadow needs.
- ⏸ NEW for Rama: the FORCE of a RECENT OBSTACLE against room is unspecified ⇒ 4b withholds and records both ratios. Clear air unchanged.
- ⚠️ Adversarial review (30 agents) found 7 real defects pre-gate; the mutation harness then caught a vacuous test of my own.

## 13-Sep-2026 (Sun) 14:3x — 🧱 SECONDARY CONTEXT PHASE D BUILT · ⛔ UNPUSHED · ⏸ STOPPED FOR REVIEW

- 🧱 Same branch, tip `3143e55` (A+B+C `932b1ed` accepted). Report `docs/audit/SECONDARY_CONTEXT_PHASE_D_BUILD_13-Sep-2026.md`.
- 🔬 Gate 7F/6,505P/5S, failure set identical to `932b1ed`, both comm empty. Mutations 74/74 RED. Full entry -> [[unpushed-pending-deploy-ledger]].
- ⏸ Open for review: pullback "reaction" reading · AT-the-level = no change · all checks REQUIRED · QUALIFIER meaning · 4a reject-name conflict. ⛔ CLEAR_AIR verdict = Rama's.
- ⛔ Monday scanner-III clear-air measurement NOT RUN; Batch 1 08:15/08:20 first; only on Rama's go.

## 13-Sep-2026 (Sun) 12:5x — 🧱 SECONDARY CONTEXT A+B+C BUILT · ⛔ UNPUSHED · ⏸ STOPPED FOR REVIEW

- 🧱 Branch `feat/secondary-context-abc-13sep` tip `932b1ed` (worktree `D:/Projects/wt-secctx-13sep`). Report `docs/audit/SECONDARY_CONTEXT_ABC_BUILD_13-Sep-2026.md`.
- 🔬 Gate 7F/6,438P/5S vs base 7F/6,218P/5S, failure set identical, both comm empty. Mutations 47/47 RED. Full entry → [[unpushed-pending-deploy-ledger]].
- ⏸ Next: Rama reviews. ⛔ Token checks (RAYMOND, payload, staleness, forming bar, EMA20, VWAP systematic) NOT RUN; Monday Batch 1 first.

## 13-Sep-2026 (Sun) — ⏸ SECONDARY FILTER v2: PRE-BUILD REVIEW DONE · ⛔ NOTHING BUILT · AWAITING RAMA

- 📄 Spec = `C:/Users/rama/Downloads/discussions/SECONDARY_FILTER_FROZEN_DESIGN_v2_12-Sep-2026.txt` (PROPOSAL, COMPLETE_RECORD, v1 = history only).
- 🔬 Base `970aabf` = origin/main (ls-remote 13-Sep); read in clean worktree `D:/Projects/wt-evidence-10sep`. Basis: SIGNAL_TO_ORDER_FLOW + VWAP_EMA_DATA_SEMANTICS (12-Sep).
- ⚠️ File 2 names a card `FOR_VSCODE_CLAUDE ... IMPLEMENT_PHASES_ABC` ("A-C in flight") -- not in the folder, no branch/worktree/commit. Asked Rama.
- ⏸ Asked: confirm one-shot lock (reverses 05-Sep contract §5 WATCHING) · daily-store location (rec: own sqlite file) · shadow async (rec) vs sync · 9 open check definitions.
- 🔬 v2 corrections sent: I/XV = 10 identical conditions (not 9) · EMA "prev" = fixed D-1 base, never the previous minute · circuit boundary per book · XVI never reaches the path.
- ⛔ Token-dependent checks (§10 items 6-9, RAYMOND weekly) need a live token: Mon after 08:15, Rama's call.

## 12-Sep-2026 (Sat) ~00:00 — ✅ RESULT-D11-SIGNAL-TO-ORDER-12SEP2026 · WHAT HAPPENS INSIDE (the 23:10 file) — ONE REPORT, ASSEMBLED BY ME

- 📄 Report: `docs/audit/SIGNAL_TO_ORDER_FLOW_12-Sep-2026.md` (untracked). Evidence: `docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/`
  (36 files, sha256 in MANIFEST; every command and output verbatim). First line: on 11-Sep, 21,005 stock-alerts → 3,807 signals → 81 passed
  → 21 at the broker → 6 filled.
- 🔴 After 10:15 the score reaches 60 ONLY if `spread_check` = 1 (≤ 0.005 %, the unit mismatch). 0 of 156,680 such rows have ever passed;
  2,950 of 3,992 passes came from 10:00–10:14. The code's exact expression reproduces 175,019 of 175,019 stored scores.
- 🔴 The receiver keeps one (symbol, scanner) per 300 s; 81.9 % of alerts die there, and those statuses are response-only (stored nowhere).
  The entry price sent is also stored nowhere (`orders.price` NULL on 769 of 769). The placer's drift top-up can move the entry to the raw
  LTP (once in 8 days). The target is recomputed from the fill and clamped to the circuit band (RAYMOND: R:R 0.33).
- 📋 Unwired: `rate_limiter` (FIX-007), `perf_weights`, the liquidity check, `price_drift_threshold`, heartbeats, `pipeline_timeout_sec`.
  YAMLs: 565 key instances, 37 distinct — 208 never consulted, 162 neutralised; only 6 keys both differ and decide.
- ⛔ The 22:45 file's Task 1 (lateness) and Task 2 (data availability) were DEFERRED by the 23:10 file and not done. No recommendation,
  design or keep/modify/add/delete. Nothing changed on either VM.
- ⏸ NEXT: Monday 08:15 Batch 1 load and the 08:20 proof come FIRST; then 👤 Rama decides from the report.

## 11-Sep-2026 (Fri) 17:46 — ✅ RESULT-CONTRACT-S11S12-11SEP2026 · THE CONTRACT §11/§12 REPORT, ASSEMBLED BY ME — NO AGENTS

- 📄 `docs/audit/CONTRACT_S11_S12_REPORT_11-Sep-2026.md` (untracked). First line: §11.7 — WEEKLY IS NEVER FETCHED,
  in either book ⇒ §3 is a BUILD. Order as the 15:10 file set: §1 · §11.7 · §11.8 · §11.1-§11.4 · §11.5-§11.6 · §12
  · unmeasured · disagreements · conflicts. Evidence (30 files, sha256): `docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/`.
- 🔴 287.80 WAS INVISIBLE FOR THREE REASONS: (1) no weekly data — `config_loader.py:1246`, `system_config.yaml:510`;
  (2) the 180-day window — `system_config.yaml:511`, `fetch.py:123-125`; (3) printed 13:52, still inside the last bar
  at 14:09 — `pivots.py:42`. §3 fixes only (1); the 400-day [A] fixes (2), so it is load-bearing; nothing fixes (3)
  ⇒ the contract's central example would still fail after §3 is built.
- ⚖️ 3.3: the five-bar exclusion is DELIBERATE — SR-P2 under "Locked Design Decisions", `pivots.py:14-15` ⇒ Rama's
  "287.80 was the ceiling" vs the detector's design is a judgement question, not a defect. ⛔ pivots.py unchanged.
- 📊 SCORER: 2 steps dead at 0 (25) + 2 pinned at half (10 lost) = 35 unreachable ⇒ ceiling 65
  (`quality_scorer.py:16-19`); the source corrects the 15:10 file's "four dead = 40". Six usable values 60-65: 4,301 of
  173,756 rows (2.48 %); HIGH 80 unreachable; MEDIUM only at 65 (15 rows); INDOCO 62 vs 60 via spread_check; §8's
  sensitivity curve has six points above the pass mark.
- ✏️ CONTRACT FACTS CORRECTED: INDOCO entry 276.83, not ~281.48 (the 14:43:33 capture price); the stop hit the SAME
  day (1-min low 270.55 at 15:05; exit 271.02 GTT_EXIT 15:19:08); KOTAKBANK never a system trade ⇒ S11-R26, the corpus
  question. 12,069 in-window 403s ⇒ S11-R27. Both registered 15:14; N 311.
- ⛔ No recommendation, threshold or design; §10 stays blocked; nothing changed on either VM. Checked after drafting:
  a script cross-check against the findings + my own `git show 970aabf` re-read, 15:36-15:38.
- ⏸ NEXT: 👤 Rama decides from the report.

## 11-Sep-2026 (Fri) 15:24 — ✅ RESULT-1516-TWIN-11SEP2026 · THE TWIN'S 15:03: NOT EXERCISED -- OUTCOME (d) · BATCH 1 SILENT

- 🔬 TWIN BLOCK A, EVENT (log): PASS_1 15:03:04.106 mis_candidates=0 → "PASS_1: FLAT"; PASS_2 15:06:04.130
  mis_candidates=0 → "PASS_2: FLAT"; 0 EXIT_SUBMITTED. Lifecycle 15:02-15:12: 4 squareoff lines, 0 CRITICAL /
  ERROR, 0 sentinels.
- 🔬 BROKER (15:16:24): MOBIKWIK, SUNTV, RAYMOND all net 0; 0 squareoff orders. RAYMOND was NEW after the 14:50
  snapshot: MIS BUY 1 @ 1000.15 260911170817593 at 14:53:42 → its own TGT 260911170818450 at 14:59:32 @ 1004.10;
  SL 260911170818449 CANCELLED 14:59:34 -- 3.5 min before PASS_1.
- ⛔ ⇒ outcome (d): every MIS position closed on its own leg before 15:03 → NOT EXERCISED (never PASS, never CLEAN).
  The 14:50 snapshot was flat and a position still opened and closed before 15:03 -- a snapshot is not a
  prediction.
- 🟢 TWIN BATCH 1 (the recorder, a separate stream): 5,618 rows (P3 5,468 · P2 127 · P1 23), all COMPLETE;
  fingerprint 5,618 / 5,618 == the disk (d6c049a3…); failure ledger NONE; no [EVIDENCE] sentinel; 0 evidence log
  lines -- SILENT.
- 📋 The twin log's CRITICAL 3 / ERROR 8 since the restart are not the observer: the 15:15:00 circuit-breaker
  force-close → SOFT_KILL (3 lines); the 10:25 drift (S11-R23); the 10:32 cancel race (S11-R24); broker "MIS
  orders are currently blocked" for SESHAPAPER (11:14) and MAFANG (14:59).
- ⏸ NEXT: the contract §11/§12 report, assembled by me in the main thread.

## 11-Sep-2026 (Fri) 15:14 — ✅ RESULT-1513-11SEP2026 · PRODUCTION'S 15:03: NOT EXERCISED -- OUTCOME (d), BOTH PASSES FOUND 0 MIS

- 🔬 EVENT (from the log, not the capture time): PASS_1 15:03:00.335 MIS_AUTO_SQUAREOFF_SCAN mis_candidates=0 →
  "PASS_1: FLAT"; PASS_2 15:06:00.364 mis_candidates=0 → "PASS_2: FLAT"; 0 EXIT_SUBMITTED. Lifecycle 15:02-15:12:
  4 squareoff lines, 0 CRITICAL / ERROR, 0 sentinels.
- 🔬 BROKER (captured 15:13:12): MIS day book BSOFT / MOBIKWIK / NIITMTS / SUNTV all net 0; 0 squareoff orders. Each
  closed on its OWN leg, by broker order id: BSOFT SL 260911170248165 11:40:19 · MOBIKWIK SL 260911170281572
  10:25:43 · NIITMTS SL 260911170633355 13:20:53 · SUNTV TGT 260911170272882 10:32:11.
- ⛔ ⇒ outcome (d): every MIS position closed on its own leg before 15:03 → NOT EXERCISED (never PASS, never CLEAN).
  Block A's protected MARKET did not run on production today; the BUY-side question does not arise. NIITMTS
  (13:18:14) came from the unchanged process, not the 13:17:55 push.
- 🧪 Run with PYTHONDONTWRITEBYTECODE=1: Monday's evidence_contract .pyc baseline is still ABSENT after the capture.
  The session job 0bf5092c was deleted before I ran it, so it cannot run twice.
- ⏸ NEXT: the twin's 15:03 at 15:16 (`97e80a55` → run by me) · then the contract report.

## 11-Sep-2026 (Fri) 14:51 — ✅ RESULT-1450-MIS-BROKER-11SEP2026 · PRE-EXERCISE SNAPSHOT: BOTH VMs FLAT IN MIS AT THE BROKER · ⏸ 15:13 / 15:16

- 🔬 Broker 14:50:18 (twin) / 14:50:20 (production), broker_mis_read.py, read-only. TESTING VM: 0 MIS open (MOBIKWIK
  + SUNTV closed by their own legs this morning). PRODUCTION: 0 MIS open -- BSOFT closed 11:40:19 (own SL);
  NIITMTS a NEW round trip: BUY 2 @ 233.85 13:18:14, its own SL sold 2 @ 230.62 13:20:53, TGT cancelled 13:20:56
  (P&L -6.46).
- 🔬 0 non-zero net positions of any product on either machine; each local DB agrees (0 live). NIITMTS entered 19 s
  after the 13:17:55 push -- by the unchanged d3ee69d process (PID 2298907), not by the push.
- ⏸ A SNAPSHOT, not a prediction: both 15:03 passes should find nothing (NOT EXERCISED) unless a new MIS entry fills
  before entries close. No push sent -- the rule alerts only on an open MIS position.
- ⏸ NEXT: 15:13 production capture `0bf5092c` · 15:16 twin `97e80a55` -- each + the lifecycle dump.

## 11-Sep-2026 (Fri) 13:20 — 🚀 BATCH 1 PUSHED TO PRODUCTION 13:17:59 · FILES ONLY, ⛔ NO RESTART · SPLIT STATE UNTIL MON 08:15

- 👤 On Rama's own word, typed 13:15:07: "push now [Books already flatten now]". Gate re-measured 13:16 (not
  carried): origin/main d3ee69d, fast-forward to 970aabf (0 behind / 16 ahead), exactly the 10 files, production 0
  tracked modifications, crontab == canonical 148.
- 🚀 git push origin 970aabf:refs/heads/main at 13:17:55 → d3ee69d..970aabf; the hook: checkout -f main + "crontab
  AUTO-INSTALLED from canonical". origin/main = 970aabf (ls-remote 13:17:59).
- ✅ On disk 13:18: 0 tracked modifications; all ten files == the 970aabf blobs (md5); crontab 148 → 151, md5
  1dd8c62f, evidence_backup at lines 27-28 (10 1 * * *); config load_all OK, 8 files; arm LFL836 →
  data_store/evidence/signal_evidence_LFL836_<date>.jsonl; retention prunes only reports/output + logs.
- ⛔ NO RESTART: MainPID 2298907, started 08:15:20, NRestarts 0 -- unchanged across the push. SPLIT STATE: production
  runs d3ee69d CODE with 970aabf FILES on disk until Monday 08:15 (Python does not reload a running process).
  Harmless; written down, not discovered.
- 🧪 Monday's proof, prepared: core/__pycache__/evidence_contract.cpython-312.pyc ABSENT at 13:18 (re-checked after
  my own checks, which wrote no bytecode), and nothing that runs before the boot imports it (backup_evidence /
  output_retention / generate_crontab are stdlib-only).
- 📊 TRADING VM · Batch 1: COMMITTED ✅ · PUSHED ✅ 13:17:59 · DEPLOYED (files) ✅ · RUNNING ⛔ (old code until Mon
  08:15) · RUNTIME-PROVEN ⛔ (Mon 08:20) · TRAFFIC-TESTED ⛔ · REVIEWED ⛔ · LIVE-PROVEN ⛔.
- ⏸ NEXT: 14:50 snapshot `37d2a662` · 15:13 production · 15:16 twin · Monday 08:20: prove the load.

## 11-Sep-2026 (Fri) 13:02 — ⏸ THE 13:00 FILE: PUSH STILL HELD (RAMA QUOTED, NOT TYPED HERE) · BSOFT LABEL CORRECT · ⛔ CRONTAB WARNING

- ⏸ The 13:00 file (delivered 12:59:05) quotes Rama at 12:42: "Additional Info: If its possible deploy/push Batch-1
  to trading vm also now, subject to your discretion - FYI books are flat now". Its own §1.3: unless he types
  "push now" himself, hold. 🔬 Transcript: no Rama-typed message since 12:40 (only the 12:42:36 and 12:59:05 files)
  ⇒ HELD, asked him directly. origin/main still d3ee69d.
- 🔬 §3 BSOFT's local record (read 12:45:46): CLOSED / SL_HIT / OWN_SL -- correct on all three vs the broker (own SL
  260911170248165, 11:40:19). ⇒ S11-R22 is CONDITIONAL: today 2 of 5 own-leg closures were stored MANUAL (prod
  MOBIKWIK, twin SUNTV); closure_source was right in 5 of 5.
- ⚠️ §4 THE CRONTABS DIVERGE BY DESIGN: production 148 now → 151 after the push (the canonical adds the
  evidence_backup comment + job + blank); the twin 149 (the job line appended by hand at 09:07, no comment). Same
  logical job, different counts, for a reason.
- ⛔ THE TWIN MUST NEVER RECEIVE THE CANONICAL CRONTAB (nor a push): it would repoint refresh_instruments +
  reconcile_positions from --account VBB097 to LFL836 (PRODUCTION's account) and re-enable the 5 gemini_* jobs
  Rama disabled 09-Sep. Twin 149 vs canonical 151 = 18 lines: not drift.
- ⏸ NEXT: Rama's own word on the push · 14:50 snapshot `37d2a662` · 15:13 production · 15:16 twin.

## 11-Sep-2026 (Fri) 12:51 — 🎯 THE 12:45 FILE: BSOFT CLOSED ON ITS OWN STOP · BATCH 1 PUSH READY, ⏸ HELD FOR RAMA'S WORD · S11-R25

- 🔬 §1 BROKER 12:45: BSOFT closed by its OWN SL -- order 260911170248165 TRIGGER PENDING from 10:00:48, filled 1 @
  278.60 at 11:40:19; the TGT 260911170248170 CANCELLED 11:40:20. Both VMs flat in MIS. ⇒ (d); today's 15:03
  almost certainly NOT EXERCISED, and (e) cannot occur unless a new MIS opens.
- ✅ Push preconditions, all measured: d3ee69d is 970aabf's ancestor (0 behind / 16 ahead; push --dry-run =
  fast-forward) ⇒ no rebase; exactly the twin's 10 files; production: 0 tracked modifications, the 4 new paths
  absent, crontab == canonical (148, md5 4a3e46cc).
- ✅ The hook (md5 b7166732): checkout -f + install the canonical crontab ONLY if generate(registry) == canonical; ⛔
  no restart. My PC run differed only by CR bytes (Windows stdout); CR-stripped, 0 lines differ at both SHAs ⇒ it
  installs 151 lines (md5 1dd8c62f) on production.
- ⏸ The push is the reviewer's recommendation, ⛔ not Rama's word -- HELD. On his go: git push origin
  970aabf:refs/heads/main, ⛔ no restart; then crontab 148 → 151, hashes, arm LFL836, retention; the split state
  (d3ee69d code, 970aabf files) recorded until Monday 08:15.
- 🔴 Registered S11-R25 (N 308 → 309): outcome (e) -- the same race is in 3b15bbf / 20061b6 (:612, :946), whose
  unprotected MARKET (:636) the broker refuses via the API. Block A did not create the race; it removed the
  accidental protection hiding it. ⛔ Not fixed.
- ⏸ NEXT: Rama's word on the push · 14:50 PRE-EXERCISE SNAPSHOT `37d2a662` · 15:13 production · 15:16 twin.

## 11-Sep-2026 (Fri) 12:26 — 🔬 THE 12:20 FILE CHECKED AGAINST d3ee69d: FIVE 15:03 OUTCOMES, NOT FOUR · ⏸ 14:50

- 🔬 orders/mis_autosquareoff.py @ d3ee69d: PASS_1 cancels each resting leg read from the LOCAL store (:815-839),
  verifies at the broker only if cancel_ok and resting (:841-842), and on not cancel_ok restores, emits a
  CANCEL_FAILED CRITICAL and submits NO exit (:846-857) -- the file's 1.1 holds.
- ⚠️ (e), possible per source, not observed: _verify_cancelled counts COMPLETE as settled (:1204) and PASS_1 does not
  re-read the position before placing (:869) ⇒ a cancel ACCEPTED as the leg fills lets the protected MARKET go out
  against a closed position -- a reversed position PASS_2 then sees.
- ⚠️ 1.2 holds only conditionally: the loop stops at the first refused cancel (:835). If the SL was cancelled first
  and the TGT's cancel is refused for a reason other than filling, the stop is gone and the restore cannot replace
  it (S11-R8, side='') ⇒ naked on the stop side.
- 📣 The CRITICAL names its state (:1320): MIS AUTO-SQUAREOFF — CANCEL_FAILED (no exit attempted) vs — EXIT_REJECTED
  (place_order raised, :907). An asynchronous broker REJECT after EXIT_SUBMITTED shows as a REJECTED order + a
  later MIS_REMAINS / PASS_2.
- 🧰 The capture's filter drops Block A's colon-format lines and its RESTORE FAILED lines ⇒ lifecycle_1503.py
  (read-only, either VM) dumps every 15:02-15:12 squareoff line, CRITICAL, order-path line and sentinel; run
  beside each capture. Tested on 10-Sep's window, both VMs.
- 📡 The alert path, measured by that test on production's 10-Sep window: the EXIT_REJECTED and MIS_REMAINS CRITICALs
  reached F as BOTH_ACCEPTED (email 3.2 / 3.1 s), while _emit's second, direct notifier call failed both times
  ("notifier failed for …"). ⇒ Rama's 15:03 alert comes via F. Not investigated.
- 🎯 Stakes (broker 10:55): BSOFT 1 share short @ 275.80, SL trigger 278.55 / limit 279.95 ⇒ Rs 2.75 to the trigger,
  at most Rs 4.15 at the limit. Observed calmly; ⛔ no rule relaxed.
- ⏸ NEXT: 14:50 PRE-EXERCISE SNAPSHOT `37d2a662` · 15:13 production · 15:16 twin -- each + the lifecycle dump.

## 11-Sep-2026 (Fri) 11:21 — 🏷️ THE 11:15 FILE: TAG KEPT · EMAIL NOTE CORRECTED · 3 ROWS REGISTERED · ⏸ 14:50 BSOFT

- 🏷️ Tag keep/register-16jul → e7a6d7089232 (lightweight, LOCAL ONLY -- 0 on origin), holding e7a6d70 + 55c1a98 + the
  16-Jul register blob 9e8d7d31. fsck (refs only, reflogs ignored): 611 unreachable before, all three listed → 600
  after, none ⇒ gc can no longer remove them. Working tree untouched.
- 📧 The "prod email dead since 07-Sep" note above is struck and corrected: restored 09-Sep, and today 3 of 3
  production sentinels delivered with no fallback tag. Telegram never stopped. If BSOFT's exit fails, Rama is
  alerted within seconds.
- 🎯 15:03 is PRODUCTION's: BSOFT short 1 @ 275.80 (broker 10:55). Its exit would be a BUY -- the band was chosen
  SELL-side, so a BUY success ⛔ proves nothing for SELL. ⛔ Nobody touches BSOFT. Most likely a leg fills first =
  NOT EXERCISED.
- 📋 Registered, N 305 → 308: S11-R22 closure attribution wrong in BOTH directions (ORCHPHARMA 09-Sep false OWN_SL;
  today own fills stored MANUAL); S11-R23 the drift delta is an exact operand difference; S11-R24 cancel-vs-fill
  race on a resting leg. None investigated.
- ⏱️ fsync tail as a rate: 3 of 2,700 over 10 ms (worst 28.5) × production's median 4,484 signals/day × 1.136 rows
  each ≈ 6 stalls >10 ms a day ON THE TRADING THREAD (95%: ~1-17), ~2 over 20 ms. ⛔ S11-R19 stays OPEN; ⛔ no
  redesign.
- ⏸ NEXT: 14:50 BSOFT from the BROKER, both VMs `37d2a662` · 15:13 production `0bf5092c` · 15:16 twin `97e80a55`.

## 11-Sep-2026 (Fri) 11:02 — 🟢 RESULT-1047-B1TWIN-11SEP2026 · TWIN WATCH #2: 276 ROWS, 276 COMPLETE, 243/243 COVERED · ⚠️ PROD HOLDS BSOFT MIS · ⏸ 14:50

- 🔬 Run 10:51:02-10:52:36 by me -- the 10:45 file (delivered 10:44:45) + 👤 Rama: "So run everything as much as
  possible as per your opinion"; job 40669337 deleted before the run. Batch 1 checks on the TESTING VM; broker
  reads on both VMs at 10:55 (read-only).
- 🟢 Rows 276 (P3 243 · P2 27 · P1 6), 10:00:07.50 → 10:50:08.51; COMPLETE 276/276; missing 0/0; fingerprint 276/276
  == d6c049a3…; 243 signals = 243 signal_ids, 0 without a row, 0 orphans; P2 27/27 · P3 243/243 · P1 6 →
  PROCESSED.
- 🔇 Observer silent: no failure ledger, 0 failure lines. Today's 3rd sentinel is the reconciler's capital drift
  (10:25:26), and the log's ERROR 2 / Traceback 1 are the reconciler + adapter -- none is the observer.
- 📊 §4.3 at 243 signals: P3 on 100% of signals (88.0% of rows), P2 on 11.1% (27: throttle 12, direction limit 11,
  duplicate 4 -- all after screening), P1 2.5%. At 35 signals: P3 100%, P2 60%. The ~69% is not reproduced; every
  capture point fires.
- ⏱️ §4.2 fsync tail at loadavg 0.00: n=600 max 28.5 ms (>10 ms: 28.5, 15.9); n=1500 max 13.0 ms. With 10:12: 3
  stalls >10 ms in 2,700 samples, 1 >20 ms -- the volume's own tail, present at idle. ⛔ S11-R19 stays OPEN.
- 💼 §1.1 BROKER 10:55: TWIN flat in MIS -- MOBIKWIK closed by its own SL 10:25:43, SUNTV by its own TGT 10:32:15 ⇒
  neither is Block A. ⚠️ PRODUCTION holds BSOFT MIS SHORT 1 @ 275.8 with SL (BUY trig 278.55) + TGT (BUY 271.7)
  resting ⇒ if open at 15:03, PRODUCTION's Block A runs for real.
- ⚠️ Exit mislabel on BOTH machines: twin SUNTV and production MOBIKWIK are CLOSED_MANUAL / exit_reason MANUAL while
  closure_source says OWN_TGT / OWN_SL and the broker shows the system's own order filling. Production has no
  Batch 1 ⇒ pre-existing. Captures: attribute by broker order id.
- 🧾 §3 ledger annotated, not rewritten: 0c74860 → d31759f and 9625b7d → afefccb (both SHIPPED), b80354c → 7297be7,
  a5779420 UNVERIFIABLE. e7a6d70 + 55c1a98 still at gc risk -- one command keeps both: git tag keep/register-16jul
  e7a6d70. ⛔ Not run -- 👤 Rama's word.
- ⏸ NEXT: 14:50 broker read, both VMs `37d2a662` · 15:13 production `0bf5092c` · 15:16 twin `97e80a55`.

## 11-Sep-2026 (Fri) 10:17 — 🟢 RESULT-1012-B1TWIN-11SEP2026 · TWIN BATCH 1 WATCH #1: 62 ROWS, 62 COMPLETE, 62 AGREE, SILENT · ⏸ 10:47

- 🔬 Run 10:12:32-10:13:02 by me on 👤 Rama's "continue with the 10:12 watch" (precheck 0); the session job 343596b7
  had not fired and was deleted after the run, so the watch cannot run twice. TESTING VM only, read-only;
  production untouched.
- 🟢 Rows 62: P3_SCREEN 35 · P2_REJECT 21 · P1_ACCEPT 6 (10:00:07.50 → 10:12:08.52). record_status COMPLETE 62 of 62;
  missing required 0, optional 0; arm VBB097; contract 1. code_fingerprint 62 of 62 == the disk recompute
  d6c049a3… (110 files).
- 🟢 Rows vs traffic: 35 signals since the restart = 35 signal_ids in the rows; 0 signals without a row; 0 orphan
  rows. Agreement: P2 21/21 = signals.status · P3 35/35 = screener_results.status · P1 6 → PROCESSED 6.
- ⚠️ P3 recorded 35 of 35 signals (100%), not the ~69% predicted: every P2 reject in the window (throttle 12,
  direction limit 6, duplicate 3) was screened first. Score rejections (8) are recorded once, at P3 only -- a
  question for the review, not a finding.
- 📊 Mix vs 10-Sep, same clock window: 35 signals vs 124; every status today belongs to a family seen on 10-Sep
  (throttle · direction limit · duplicate · processed · score, the number being the score). A comparison, not a
  counterfactual proof.
- 🔇 Observer silent: no failure ledger · 0 capture-failure / not-built log lines · CRITICAL 0 · ERROR 0 · Traceback
  0; today's 2 sentinels are the routine Phase C + Cron Briefing.
- ⏱️ fsync under the twin's real load (loadavg 0.02): mean 2.03 ms · p99 2.71 · max 4.81 · 0 over 5 ms (n=600); no
  fsync 0.064 ms. From the rows: busiest second 6 rows; smallest gap between two consecutive rows 3.22 ms (2 of 77
  under 5 ms). ⛔ S11-R19 stays OPEN (light load, one box, a proxy).
- 💼 Open at 10:15 (local DB; broker not queried): RAYMOND + SMSPHARMA CNC with ACTIVE GTTs; SUNTV + MOBIKWIK MIS
  with SL + TGT open. ⭐ Two MIS positions ⇒ the twin's 15:03 pass may be EXERCISED today unless SL/TGT closes them
  first.
- ⏸ NEXT: watch #2 at 10:47 `40669337` · 15:13 production `0bf5092c` · 15:16 twin `97e80a55`.

## 11-Sep-2026 (Fri) 10:07 — 📋 THE 09:35 FILE §1-§5: ⛔ BATCH 1 NOT PUSHED · LEDGER VERIFIED CLAIM BY CLAIM · EIGHT STATES · ⏸ 10:12

- 🔬 §1 -- 👤 Rama's "all pushes as per unpush ledger succeeded" does NOT hold for Batch 1: 970aabf / 305ed3c are in 0
  of the 9 live origin heads (ls-remote 10:03:24), 0 remote-tracking refs, the branch has no upstream; the twin's
  bare /home/ubuntu/trading-system.git is 20061b6 and 970aabf is not even an object there. It reached the twin by
  direct copy only.
- 🔬 §1.3 -- every ledger push claim tested against the live origin/main d3ee69d: 153 confirmed; the hot index's 26
  push claims confirmed one by one; 22 scan flags read line by line = 0 false push claims; the 40 ids the ledger
  calls unpushed are still unpushed (never pushed -- "all succeeded" does not cover them).
- ⚠️ STALE: "SHADOWTRACKER DISABLE IS HELD" (0c74860) and "M-A2 IS HELD" (9625b7d) -- both hold branches are gone and
  both changes are IN origin/main, patch-identical, as d31759f ("AUTHORISED and pushed") and afefccb. The HELD
  lines were never cleared.
- ⚠️ UNREFERENCED: e7a6d70 + 55c1a98 (16-Jul docs commits) -- no branch or tag holds them and no equivalent exists in
  origin/main or local main; gc may delete them. b80354c likewise, but its change lives on as 7297be7. "SHA
  a5779420" is not an object here. ⛔ Nothing tagged or fixed -- 👤 Rama's call.
- 📊 §2 eight states (COMMITTED · PUSHED · COPIED/DEPLOYED · RUNNING · RUNTIME-PROVEN · TRAFFIC-TESTED · REVIEWED ·
  LIVE-PROVEN): TRADING VM Block A ✅✅✅✅✅⛔⛔⛔ · TRADING VM Batch 1 ✅⛔⛔⛔⛔⛔⛔⛔ · TESTING VM Block A ✅ ⛔(file copy) ✅✅✅
  ⛔(10-Sep 15:03 FLAT = NOT EXERCISED) ⛔⛔ · TESTING VM Batch 1 ✅ ⛔(never) ✅✅✅ ⏳(first rows 10:00) ⛔⛔. Table +
  evidence: the ledger.
- 📄 §3 the 10:12 / 10:47 twin watches are fallback files now (scripts embedded verbatim, extracted and compared
  equal to the sources) and on the fallback list above. §4 the twin's own 15:03: twin_1516_capture.py (production
  v3 + 8 labelled substitutions -- host + labels only), job 97e80a55 at 15:16 + its fallback.
- ⏱️ §5 the fsync bench now reports the tail (p99 · max · five worst · counts >5/10/20 ms). ⛔ The 2.10 ms idle bench
  does NOT close S11-R19 -- OPEN; the under-load figures come at 10:12.
- 🟢 Traffic started with the 10:00 window: at 10:00:08 the twin had 4 signals and 4 P3_SCREEN rows, all 4 agreeing
  with screener_results. Before 10:00: 124 webhooks, all 403 -- zero rows were correct (the directory is created
  by the first row).
- ⏸ NEXT: 10:12 watch `343596b7` · 10:47 `40669337` · 15:13 production `0bf5092c` · 15:16 twin `97e80a55`.

## 11-Sep-2026 (Fri) 09:23 — 🟢 BATCH 1 COPIED + RUNNING ON THE TESTING VM ONLY · ⛔ NOT ON THE TRADING VM · ⏸ 10:00 WATCH

- 👤 Rama's ruling (the 08:55 file, delivered 08:55:53): deploy Batch 1 to the TESTING VM today, restart it, review
  the result. ⛔ Production got nothing -- no copy, no push, no restart.
- 📦 DIRECT COPY, never a push (the twin's bare stays 20061b6): 10 files -- 5 COPY (the twin's copy == d3ee69d), 1
  DELTA (config/cron_registry.yaml +15 lines; its 4 VBB097 lines kept -- a straight copy would have repointed
  refresh_instruments + reconcile_positions at LFL836), 4 NEW. md5 both sides OK, CR 0, 664 ubuntu:ubuntu. Backups
  ~/preserved/batch1_backup_20260911_090741.
- ⏰ Crontab 148 → 149: exactly the evidence_backup job line (01:10 daily), diff = 1 line; the canonical file ⛔ NOT
  installed.
- 🔁 Restart: denied to me by the permission layer; 👤 Rama ran it 09:16:44 (PID 212449). Flat at 09:09:20 (a fresh
  broker read).
- 🧪 LOADED, by experiment: core/__pycache__/evidence_contract.cpython-312.pyc -- ABSENT at 09:02 and 09:09 --
  written 09:16:53 by the new boot; header == the deployed source. STARTUP ev 3850 WARM 09:16:56. Since the start:
  Config loaded 1 · CRITICAL 0 · ERROR 0 · Traceback 0.
- 🏷️ The arm resolves to VBB097 on the twin (not LFL836); data_store/evidence/ appears with the first row. Retention
  excludes it.
- ⏱️ fsync on the twin's disk, pre-open (load 0.11): mean 2.10 ms · p99 2.73 · max 16.4 (n=300); 0.065 ms without
  fsync. Under load: after 10:00.
- 🔧 Two instrument slips of mine, caught, nothing changed: a Git Bash path rewrite stopped install.sh at line 8
  (rebuilt -- the script now derives its staging dir); my verify read log timestamps one character late (fixed).
- ⏸ NEXT: after 10:00 -- rows per P1 / P2 / P3, record_status, fsync under load, outcomes vs yesterday,
  a silent failure path. The 15:13 production capture is unchanged (job `0bf5092c`).

## 11-Sep-2026 (Fri) 08:43 — INPUT 3.5 RE-RUN RECORDED · 3.5 PASS · ESTABLISHED · ⏸ 15:13 NEXT

- 🧪 3.5 (verbatim): PASS -- ConfigSchemaError, error_count=2, on exactly the two Block A keys
  (eod_squareoff.mis_pass_1_market_protection_percent and eod_squareoff.mis_pass_2_market_protection_percent, both
  extra_forbidden)
- ⚖️ COMBINED (verbatim): Host gate PASS and inputs 3.1-3.4, 3.6-3.12 PASS (the 08:20 record) + input 3.5 PASS (this record) => Block A's
  RUNTIME is ESTABLISHED on production -- and it is NOT live-proven: ESTABLISHED says the right code is running
  with the right values, and NOTHING about whether a protected MARKET order actually executes at the broker. That
  is 15:13's question, and only a real exit can answer it.
- 📄 NEW record `docs/audit/BOOT_PROOF_BLOCK_A_d3ee69d_11-Sep-2026__INPUT_3.5_RERUN.md` (sha256 8342ee7c36a93d2f…,
  raw f41db86c72cd1aa2…) cites the 08:20 record (f76f313c99e913a2…, raw 82b2c694dcb1701e…); ⛔ the 08:20 record is
  untouched and stays NOT ESTABLISHED as the truth of 08:20.
- 🔧 Producer: the 08:20 script + ONE line (register the old loader in sys.modules before exec); sha256
  642b45fa3d018922… (08:20: 82e39df6…). Nothing else changed.
- 📌 08:35 §5 registered, ⛔ not chased: 5.1 main.py's .pyc mismatch is expected (the entry script is never cached) --
  REFERENCE; 5.2 the token-refresh log silent since 08-Sep -- register row S11-R21 (N 304 → 305); 5.3 my check's
  two label slips (characters printed as 'bytes'; the heartbeat time column not found) -- fix when the script is
  next touched, ⛔ not now.
- ⏸ NEXT: 15:13 capture (job `0bf5092c`, else the fallback above) → final review → twin by direct
  copy → review → prod. ⛔ No push · no Batch 1 on either VM · no restart · no repair.

## 11-Sep-2026 (Fri) 08:25 — 08:20 PRODUCTION CHECK RECORDED · P5 / T2 · COMPLETE · ⏸ 15:13 NEXT

- 🚦 TRIAGE (verbatim): P5 / T2 -- service active, today's process; REQUIRED EVIDENCE MISSING -- FAIL: none ; NOT EXECUTED: 3.5.
  Production is running: a records gap, not an emergency.
- 🧾 RESULT-0820-11SEP2026 · VERDICT (verbatim): NOT ESTABLISHED -- host gate: PASS ; FAIL: none ; NOT EXECUTED: 3.5. Do NOT restart, do NOT repair.
- 🖥️ SERVICE / KILL SWITCH (verbatim): active, process started Fri Sep 11 08:15:19 2026 | KILL SWITCH: INACTIVE at 2026-09-11T08:15:21.050806+05:30 by
  main.auto_clear_stale
- 👁️ WITNESS (verbatim): AGREE
- 🔬 Host gate: PASS  hostname=trading-system · run 2026-09-11 08:20:33 IST · by session job 31f68404 (08:20) ·
  COMPLETE. Inputs 3.1-3.12: 3.1 PASS · 3.2 PASS · 3.3 PASS · 3.4 PASS · 3.5 NOT EXECUTED · 3.6 PASS · 3.7 PASS ·
  3.8 PASS · 3.9 PASS · 3.10 PASS · 3.11 PASS · 3.12 PASS.
- 📄 Evidence record `docs/audit/BOOT_PROOF_BLOCK_A_d3ee69d_11-Sep-2026.md` (sha256 f76f313c99e913a2…, raw sidecar
  82b2c694dcb1701e…) -- never edited after creation; a correction is a NEW record citing its path and both hashes.
- 🧭 Reading: P5/T2 -- production is RUNNING NORMALLY: the 08:15 boot fired (STARTUP ev 3842 COLD, written after the process
  start), the kill switch was auto-cleared by main.auto_clear_stale at 08:15:21 (the witness AGREES), the token is
  dated 08:15:01 today, the book is flat, 0 orders. Verdict NOT ESTABLISHED only because input 3.5 did NOT
  EXECUTE: the old loader stopped on PydanticUserError before schema validation, and a proxy is never a pass.
  PC-ONLY reproduction (not production evidence): the check's method, an unregistered ModuleType, reproduces that
  PydanticUserError exactly; registered in sys.modules, the same 3b15bbf loader refuses today's d3ee69d YAML with
  ConfigSchemaError, error_count=2, both extra_forbidden on the two Block A keys. So the gap is in the instrument,
  not in production (inference). Closing 3.5 needs a corrected read-only production run, recorded as a NEW record
  citing this one -- awaiting review; nothing was re-run.
- ⏸ NEXT: 15:13 capture (job `0bf5092c`, else the fallback above) → final review → twin by direct
  copy → review → prod. ⛔ No push · no Batch 1 on either VM · no restart · no repair.

## 11-Sep-2026 (Fri) 06:05 — §1 RESOLVED BY AUTHOR STATEMENT · 🔴 REGISTER N = 304 BY COUNT, ⛔ NOT 262 · ⏸ 08:20 NEXT

- 👤 §1, recorded per the 05:30 file §1.4 VERBATIM (⛔ never strengthen it): "The 09-Sep instruction file's ISSUED
  header reads 12:45 IST." · "That header is author-typed, approximate, and in this instance later than the file's
  real delivery time." · "Delivery to the session at 12:39:52 is the authorisation event, because delivery and
  authorisation are the same act in this workflow." · "The removal at 12:43:37 followed authorisation by 3 min 45 s."
  · "Source of the header's meaning: Web Claude, who authored it. Not inferred from the transcript."
- ⭐ §1.5 STANDING RULE now in RULES: an ISSUED header is NEVER evidence of chronology. 🔬 This file too: header
  `05:30`, delivered **05:28:02**. ⛔ §1.6: crontab untouched · no restore · no re-run · `970aabf`'s message not rewritten.
- 🔴 §2.2 COUNTED, NOT CARRIED: **N = 304** = 233 base + N9 27 + N10 11 + N11 4 + S7 9 + S11 20. The 07-Sep pass
  restarted from 233 (the figure the register's RESUME header still shows) and skipped the 42 rows of the 09/10/11-Aug
  passes; my 242 → 246 → 262 carried it on uncounted. ⭐ Every row is present -- only the tally was wrong.
- 🔴 The register that GOVERNS per that file's own 11-Aug note is `docs/MASTER_REGISTER.md` ("THIS FILE WINS"): 🔬 only
  on local `main` (`3dff752`, 22-Aug), ⛔ not on origin/main, 0 S7 / 0 S11 rows; `D:/Projects/trading-system-main` is gone.
  ⇒ all 29 rows since 22-Aug live only in the historical file. 👤 Which file is the register is Rama's call.
- 📋 §2.3: S11-R5..R20 now have 6 columns -- source fact · current status · evidence · next decision · owner. Every
  status reads OPEN; none reads resolved. R18 keeps "never defined" and "830,107 bytes measured 11-Sep 02:49" apart.
- 🔧 06:09: both fallbacks REVISED (v2, v1 kept in claude-ev10sep): the precheck is now a MECHANICAL marker grep on this
  BOARD (each file's §2: 0 ⇒ run, 1+ ⇒ already recorded); the 08:20 script also reports kiteconnect `__file__` +
  `__version__`, positions, kill switch and today's orders. 🔬 Its twin dry run (06:07, read-only, no broker) caught a
  v1 defect: `kiteconnect.__version__` is the SUBMODULE there; the string is one level down (5.1.0). Fixed before use.
- 🛑 06:35 file (delivered **06:30:55**; its header says 06:35 -- a third ISSUED instance): ChatGPT's two "critical
  findings" were the TWIN dry run read as production. Stand down: nothing hunted on the twin, repaired, pushed, restarted.
- 🔧 06:39: scripts + fallbacks v3 -- host guard (production = `trading-system`, twin = `trading-system-sandbox`),
  the 12-input PASS / FAIL / NOT EXECUTED verdict, 3.12 `d3ee69d` in the bare repo; 15:13: 5 fill classes, pass by id.
- 🧾 06:50 file (delivered **06:49:38**): the 08:20 result becomes an IMMUTABLE evidence record --
  `docs/audit/BOOT_PROOF_BLOCK_A_d3ee69d_11-Sep-2026.md` + `.raw.txt`: raw output verbatim, SHA-256s, read-only, never
  overwritten; a later finding is a NEW record. 🚦 TRIAGE printed first: T1 normal · T2 evidence gap (trading) ·
  T3 not trading · T4 boot failed (rollback to 3b15bbf = RAMA'S CALL) · T5 yesterday's process · T6 kill switch on.
- 🧭 07:20 file (delivered **07:19:47**): ONE triage code by explicit precedence -- P0 wrong host · P1/T4 boot failed
  · P2/T3 no boot (TOKEN or UNKNOWN; the token is checked first) · P3/T5 yesterday's process (not an outage) ·
  P4/T6 kill switch (not "not trading") · P5/T2 evidence gap · P6/T1 established. The kill switch is an
  independent witness to the boot. The writer saves the raw output FIRST and records PARTIAL output; the
  record is never edited after creation. Host gate + inputs 3.1-3.12, never "thirteen".
- ⏸ NEXT: 08:20 check (job `31f68404`, else the fallback above) → 15:13 capture → final review → twin by direct copy →
  review → prod. ⛔ No push · no Batch 1 on either VM · no crontab change.

## 11-Sep-2026 (Fri) 02:05 — 🟢 CLOSE-SIX §1-§4 CLOSED · TIP `970aabf` · ⛔ UNPUSHED · ⏸ RESUME HERE

- ⏸ Supersedes the 21:5x PAUSED resume point below. `feat/evidence-contract-10sep` in `D:/Projects/wt-evidence-10sep`:
  `305ed3c` + `e1952e4` (§3) + `056905b` (§1+§2) + `970aabf` (empty CHECKPOINT). Clean, **0 remote refs**, on NEITHER VM.
- 🔬 §4 EXPLAINED, ⛔ nothing touched: the twin's 149→148 is **09-Sep 12:43:37** -- session `455ded6a` removed ONLY the
  spent `41 7 7 9 * …revert_delivery.sh`, under the §1.3 ruling of the file stamped `ISSUED 12:45` (delivered **12:39:52**) + report item 5 ("testing VM likewise").
  Backup `~/preserved/crontab.bak.20260909-pre-line149-removal.txt` md5 `d005d6eb…` == the 08-Sep install, byte-exact.
  14:15:14 = the recorded gemini disable (148→148). ⚠️ That session recorded the twin removal NOWHERE -- gap closed.
- 🔬 §1 MEASURED FIRST (prod, read-only, 12-Jun..10-Sep): **48,934** P2 rejects, symbol/strategy bad **0 / 0**;
  44,766 bound + **4,168** pre-lookup (all SHADOW_INNING_ACTIVE) via the scanner; getattr sites + QUEUE_FULL **0 rows**;
  logs 01-10 Sep **4,222** reject lines == the DB's P2 rows for those days. ⇒ FAIL is cheap: P2 identity now REQUIRED.
- 🔴 QUEUE_FULL's capture had inherited the dispatcher's literal `"unknown"` (id + symbol) -- an invented identity
  that would pass as present. Fixed (reads the tuple); the contract now refuses a placeholder identity outright.
- 🟢 §2: per-point REQUIRED / OPTIONAL / N-A table (P3 per verdict shape); N/A absent ⇒ COMPLETE; score 0 / tier LOW
  placeholders → `na_supplied`. Normal P1 / P2 / P3 read **COMPLETE** through the REAL pipeline and the REAL screener.
- 🟢 §3 wording only: output_retention + cron_registry say SAME-DISK; AST-identical; crontab byte-identical.
- 🟢 Gate **7F / 6218P / 5S**, RC=1, failure-set sha16 `1855d12c70394465` (== baseline), both `comm` EMPTY, **+115 == the 115 tests of test_evidence_contract.py**.
- 🟢 Mutations **18 of 18 RED as expected, every file restored byte-exact**.
- 🔴🧪 **THE GATE RECIPE WENT BLIND:** `FORCE_COLOR=3` here ANSI-wraps every `FAILED` line, so `grep '^FAILED '` read
  **0** (sha16 `e3b0c442…` = the empty file). ANSI-stripped: **7**, `1855d12c…` == 10-Sep. Both runs stripped alike.
- 📋 Register S11-R1..R4 (N 242→246): off-box backup (O-5) · 12,016 post-sizing P2 rejects lose sizing context ·
  QUEUE_FULL `"unknown"` fallback (latent) · the dormant resumes carry no trigger time.
- ⏸ NEXT: 08:20 prod check (`claude-ev10sep/prod_0820_check.py`, read-only) · 15:03 capture ONLY if MIS held ·
  Batch 1 → twin by direct copy after review, ⛔ never a push.

## 10-Sep-2026 (Thu) 21:5x — ⏸ PAUSED (power-down) BEFORE "CLOSE SIX ITEMS" · ⛔ NO CODE CHANGED · RESUME HERE

- 📄 The instruction file (21:45, *"CLOSE SIX ITEMS. STILL NO PUSH."*) is saved verbatim as
  `Downloads/FOR_VSCODE_CLAUDE_10-Sep-2026_CLOSE_SIX_ITEMS.txt`. §1-§4 = the work; §5 = 11-Sep gates; §6 = out.
- ✅ Done before the pause: READ-ONLY reads only. 🔬 worktree clean at `305ed3c`, nothing staged, no background job.
- 🔬 §1 facts: `allocator_mode: "shadow"` ⇒ the two `getattr(candidate,"symbol",None)` sites (admit_prepared,
  reject_prepared) are ENFORCE-only and have never run in production. Gate resume dormant (no `EntryGate.add()`
  caller); retest off. The receiver rejects unknown scanners (`webhook_receiver.py:551`). `signals` carries
  `symbol`/`scanner`/`strategy` NOT NULL + `trigger_price` ⇒ identity is knowable per row. ⏸ NEXT: measure P2 on
  production, read-only: P2 = REJECTED* whose status is NOT a screener verdict for that signal_id (J-1: a signal
  can have several `screener_results` rows); by check, pre/post the strategy lookup in `_process_one`.
- 🔬 §2 facts: P3 shapes = PASSED · REJECTED_SCORE_n · step/gate rejects · SKIPPED_*. `rejected_step` is None for
  PASSED and score rejects. Skips and several rejects carry PLACEHOLDER `score=0` / `tier="LOW"` -- not real scores.
- ⚠️ §4 lead: the BOARD's 09-Sep "CRONTAB 149 → 148" is PRODUCTION (2× LFL836, the 09-Sep push) -- ⛔ NOT the twin.
  Twin: 149 at 08-Sep 22:08, already 148 at the 09-Sep sweep -- STILL UNEXPLAINED. ⛔ [11-Sep: EXPLAINED — see CLOSE-SIX.] Next: the twin's syslog
  `(ubuntu) REPLACE` events after 08-Sep 22:08:41, and memory for the 09-Sep twin copy of `3b15bbf`. ⛔ Fix nothing.
- ⏸ ORDER ON RESUME: if it is 11-Sep morning, §5.1 (08:20 production check, `extra="forbid"`) comes FIRST. Then
  §4 (read-only) → §1 measure → §1 fix + tests → §2 table + tests → §3 wording (prove AST-identical) → gate +
  mutations → CHECKPOINT commits → memory → report. 15:03: capture only if production holds MIS; ⛔ never manufacture.

## 10-Sep-2026 (Thu) 21:xx — 🔎 CHECKPOINT RE-CHECKED · 🟢 TIP `305ed3c` · ⛔ UNPUSHED · ⏸ RESUME HERE

- 👤 Rama: *"re-check>re-do if required"* -- the 19:xx checkpoint may have been a lower model. ⭐ Re-checked
  against the SOURCE, not the hand-off: **8 defects + 3 gaps fixed in 8 commits + an empty CHECKPOINT tip**.
- 🔴 **THE §6.7 SENTINEL COULD NEVER FIRE IN PRODUCTION** -- main.py's sink omitted `TelegramNotifier.send`'s
  REQUIRED `source_module` => TypeError, swallowed. Every test used a FAKE sink. Fixed `ea0e506` + a REAL-notifier test.
- 🔴 `reanchored` True on 100 % of P1 rows (`23d2be7`) · QUEUE_FULL reject uncaptured, no-bypass test blind (`853a3a1`)
  · §6.7 persist never built + silent payload failures (`d646347`) · P3 lost on a DB failure (`02d1e3f`).
- 🔴 The backup could destroy the last good copy, and it is SAME-DISK (never off-box) -- fixed and stated (`4608b83`).
- 🟢 Gate **7F / 6172P / 5S**, RC=1, failure-set sha16 `1855d12c70394465` (== baseline), both `comm` EMPTY, **+69 exact** · **20 mutations as expected** (19 RED + M19b GREEN by design), all restored byte-exact.
- 🔬 Batch 1 ABSENT on production AND the Testing VM (files + crontab measured 21:1x); branch has 0 remote refs.
- ⛔ **CORRECTION to the 19:xx entry below:** its "status line frozen" held in MEMORY only -- 🔬 **0 of 4** commit
  messages carried it. It is now in every re-check commit + the tip.
- ⏸ **NEXT, IN ORDER:** (1) **08:20** prod runtime check (`extra="forbid"`). (2) **15:03** MIS capture only if held --
  ⛔ never manufacture. (3) P2 identity. (4) fsync-on-trading-thread ruling (PC 2.18 ms mean). (5) PARTIAL is
  near-universal. (6) off-box backup. (7) Batch 1 -> Testing VM by **direct copy**, ⛔ never a push.

## 10-Sep-2026 (Thu) 19:xx — 🟢 BATCH-1 **CHECKPOINT COMMITTED** · ⛔ UNPUSHED · ⏸ **PAUSED — RESUME HERE**

- ⚠️ **STATUS LINE, VERBATIM:** *"Block A is validated by unit, differential and twin evidence and is now
  authorised for supervised production exercise."* ⛔ NEVER "live-proven". **Testing VM: Block A only, since
  13:42:47. Batch 1: NOT deployed to either VM.**
- 🟢📍 **RESUME POINT:** `D:/Projects/wt-evidence-10sep`, `feat/evidence-contract-10sep`, **4 commits**
  (`d2aa35d` · `8d27fdb` · `28ec9df` · `99342e0`) off `d3ee69d`, tree **clean**, **0 remote refs**.
  Gate **7F/6152P**, sha256 `1855d12c70394465`, both `comm` EMPTY, **+49 exact**. **7 mutations RED.**
- ✅ **FOUR GAPS CLOSED:** cron entry registered · manifest frozen at **110** · **P3 identity mandatory
  (missing ⇒ FAILED + sentinel)** · status line frozen. ⛔ **[21:xx: the status line was in NO commit (0 of 4),
  and that sentinel could never fire in production -- both fixed; see the 21:xx entry above.]**
- 🔴📄 **THE CRON "GAP" WAS PYTHON TEXT MODE — THIRD TIME THIS CLASS HAS BITTEN.**
  `generate_crontab.py`'s **stdout** emits CRLF on Windows; `.gitattributes` pins canonical to LF ⇒ a naive
  `--generate | diff - canonical` says **all 148 lines differ** while content is identical. ⭐ Use **`--out`**
  (ASCII+LF) or normalise. Same family as the MEMORY.md CRLF incident.
- ⭐🧪 **109 vs 110 SETTLED = 110.** 109 predated `core/evidence_contract.py`, which is inside the set.
  Frozen in a committed manifest + a drift test, so `code_fingerprint`'s MEANING cannot change silently.
- ⏸🔴 **NEXT SESSION, IN ORDER:** (1) **08:20** production runtime verification — it is currently **old
  code with new files on disk**; use the `extra="forbid"` experiment, ⛔ not PID age. (2) **15:03** capture IF
  production holds an MIS position — ⛔ never manufacture one. (3) P2 identity tightening. (4) Batch 1 →
  Testing VM **by direct copy**, ⛔ never a push. (5) check9 + EOD phase-2 still UNPROTECTED.

## 10-Sep-2026 (Thu) NIGHT — 🟢 BLOCK A ON PRODUCTION · 🟢 EVIDENCE CONTRACT BUILT · ⏸ 08:20 TOMORROW

- 🟢🚀 **BLOCK A PUSHED: `3b15bbf` → `d3ee69d`**, explicit refspec, all four gates green
  (**0 of 1432 files modified**, config identical to base and keeping **production's own mailbox**,
  crontab **148 → 148**). Hook: *"crontab AUTO-INSTALLED from canonical."*
- ⚠️⏸ **NOT RESTARTED, DELIBERATELY.** PID 2206465 from **08:15:21**, files mtime **16:19:37** ⇒ **old code,
  new files** until the ~17:35 self-exit. Harmless (market closed) — ⛔ but recorded, not assumed.
  ⭐ **Block A first RUNS tomorrow 08:15.** ⛔ It is **NOT live-proven** — no protected MARKET has executed anywhere.
- ⭐🗂️ **§4 REVERT TRAP CLOSED:** the Batch-1 branch was based on `3b15bbf`; pushing from there would have
  **silently reverted Block A off production**. Rebased onto `d3ee69d`, baseline re-established **7F/6103P**.
- 🟢📐 **EVIDENCE CONTRACT BUILT.** P1 + **all FIVE** terminal reject paths + P3; the no-bypass invariant is
  enforced by a **source-parsing test**, ⛔ not a comment. Fingerprint = sha256 over a **named 110-file artefact
  set**, ⛔ no git ref. Arm **in the filename**. `step_statuses` finally persisted.
- 🔴🧪 **THE GATE CAUGHT THE FORBIDDEN CLASS IN MY OWN OBSERVER** — `self._evidence` read OUTSIDE the `try`
  made a reject path raise, i.e. **the observer changed a decision outcome**. Fixed: every lookup inside the
  guard, payload made a **callable**. ⇒ ⭐ **an observer must have NOTHING outside its guard — not the
  attribute lookup, not the payload build.**
- ⚠️🧪 **AND MY FIRST MUTATION FOR THAT REGRESSION CAME BACK GREEN** — it left the lookup inside the `try`,
  so it never reproduced the defect. ⇒ ⭐ **check that a mutation fails for the RIGHT reason**; a GREEN
  mutation may mean the mutation is wrong, not that the test is vacuous.
- 🟢 Gate **7F/6143P**, sha256 unchanged, both `comm` EMPTY, **+40 exact**. **6 mutations RED**, all restored.
- 🔴⏸ **ONE §6.8 STEP BLOCKED:** `backup_evidence.py` is written and tested but **not scheduled** —
  🔬 `generate_crontab.py --generate != canonical` **ON THE PC** (it matches on production), so a registry
  change cannot be validated here and a drift would freeze the crontab at the next push.
- ⛔ Batch 1 **not pushed**, 0 commits. ⛔ No production change beyond the authorised push.

## 10-Sep-2026 (Thu) EVENING — 🟢 BLOCK A COMMITTED · 🔴 IDEA FAILED AGAIN · 📐 BATCH-1 SPEC

- 🟢📦 **BLOCK A COMMITTED LOCALLY:** `8f9afe0` · `5f75c9b` · `1955ae1` (+ `d3ee69d` audit). Tree clean.
  ⛔ **NOT PUSHED** — `origin/main` `3b15bbf`, **0 refs** on the remote. ⏸ Production deploy is with ChatGPT.
- 🔴📉 **PRODUCTION FAILED AGAIN — IDEA 15:03:01, second in two days.** 👤 Rama closed it by hand ~15:05.
  📄 `docs/audit/MIS_SQUAREOFF_REJECTION_IDEA_10-Sep-2026.md`.
- ⭐ **PASS_2 DID fire** (15:06:04, found flat). ⛔ Do NOT read that as "PASS_2 works" — it has still never
  exited anything.
- ⭐ **NO kill-switch trip, and "not adopted" did NOT suppress CHECK 9.** CHECK 9 iterates LOCAL rows and
  🔬 IDEA has **0 local trades and 0 local orders on any date** ⇒ no input. Same root cause, ⛔ not causation.
- 🔴 **A SECOND RESTORE FAILURE MODE:** no local trade ⇒ no SL row to read. ⛔ **Fixing the `state_store`
  SELECT alone leaves this broken**, and it is reachable only on OPERATOR positions — so a fix validated on
  system trades exercises it **not at all**.
- 🔴 **TWO SUBSYSTEMS DISAGREED 12 s APART** — the reconciler declined to adopt IDEA, the squareoff exited it
  anyway, because eligibility comes from the broker position alone. Registered, ⛔ not fixed.
- 📐🟢 **BATCH-1 WORKTREE UP:** `wt-evidence-10sep` @ `3b15bbf`, baseline **EXACT 7F/6063P**, sha256
  `1855d12c70394465`, both `comm` empty. ⚠️ inherited `PYTHONPATH` was the primary tree AGAIN — overridden.
- 🔴📐 **FOUR CORRECTIONS TO THE BATCH-1 BRIEF:** P2 is **6 handlers (4 terminal)**, ⛔ not one — capturing
  at `:1081` alone loses the gate and retest resumes · P3 is a funnel for **every** verdict and is **68.99 %**,
  ⛔ not ~63 % · much of the field set **already persists**, but **`step_statuses` is computed and thrown away**
  · the lying fingerprint is `forward_shadow_record.py:71-72` falling back to the **bare repo**.
- ⭐ §3.6: pruning exclusion has an exact precedent; 🔴 **the backup half does not exist** (cron backs up only
  the two SQLite DBs). ⭐ §3.8: `primary_account_tag()` exists but reaches **neither** capture point.

## 10-Sep-2026 (Thu) ROUND 8 — 🟢 **BLOCK A PROVEN LIVE ON THE TWIN** · ⭐ THE WARNING WAS snapd's

- 🟢⏱️ **THE RESTART LANDED.** PID **157694**, start **13:42:47**, vs Block-A mtime **13:32:57** ⇒ the
  process is newer than the code. Both of Rama's restarts landed (`Config loaded` at 13:42:24 **and** 13:42:48);
  `run_all_startup_checks: OK ... warnings=[]`; **0 CRITICAL since 13:42**. ⛔ No further restart. ⛔ No daemon-reload.
- ⭐📦 **`NRestarts=0` DOES NOT MEAN "no restarts happened"** — it is the AUTO-restart counter and a manual
  `systemctl restart` resets it. ⛔ Never read it as a tally of deliberate restarts.
- ⭐🔧 **THE systemd "unit changed" WARNING IS snapd's, 8 HOURS OLDER THAN THE DEPLOY.** Only
  `/etc/systemd/system/snap-snapd-27740.mount` (05:26:31 today) was written; it bumped the DIRECTORY mtime.
  `trading-system.service` is 2026-08-23, `watchman.conf` 2026-06-11. ⛔ Block A wrote nothing under /etc/systemd.
- ⭐🧪 **PROOF TECHNIQUE WORTH KEEPING: an `extra="forbid"` schema turns "which code is loaded?" into an
  EXPERIMENT.** The OLD `config_loader` **rejects** today's YAML (`ValidationError: 2 validation errors`), so a
  process that completed config load cannot be old. ⭐ Corroborated by `.pyc` headers (source mtime+size, all MATCH).
- ⭐📧 **LIVE PROOF THE CONFIG DELTA-APPLY HELD:** the boot self-test email went to
  **`sandboxpythonsystemalerts@gmail.com`**, ⛔ not production's mailbox.
- ⚠️ **A SECOND `or []` AT `_restore_protection_inner:999` — ⛔ NOT the same defect.** That path deliberately
  fails towards placing (*"a duplicate stop is bounded, no stop is not"*), so `None` and an exception act
  identically; only the **attribution** differs (`already=False` vs `PROTECTION_UNKNOWN`). ⛔ Out of scope, untouched.
- ⭐ **15:03 TODAY: the twin runs Block-A code, production runs the old unprotected path.** Both flat at 13:55
  ⇒ likely **no live exercise**, which is a complete result. ⛔ No synthetic trade.

## 10-Sep-2026 (Thu) ROUND 7 — 🟢 **BLOCK A ON THE TWIN, 12/12** · 🔴 NOT LIVE · ⏸ RESTART IS 👤 RAMA'S

- 🟢📦 **DEPLOYED BY FILE COPY** (👤 Rama 13:31, book flat). 5 files copied — **all md5-identical both
  sides** — + `config/system_config.yaml` **DELTA-APPLIED**. Backups at
  `/home/ubuntu/backups/blockA-20260910-133225/`, each verified against what it replaced.
- ⚠️🔴 **THE DEVIATION THAT SAVED PRODUCTION'S MAILBOX:** the twin's `system_config.yaml` is hand-modified
  (3 lines → `sandboxpythonsystemalerts@gmail.com`). A straight copy would have repointed the twin's alerts at
  **production's** mailbox. ⭐ Delta-applied instead; 3 sandbox refs intact, 0 production refs, 2 keys present.
- 🟢🧪 **12/12 VALIDATED ON THE TWIN'S OWN PYTHON 3.12.3** (⛔ not the PC's 3.11.9): boot path · config
  **1.5/2.5 exactly** · wire body carries them and `0.015` is absent · `None` omits · **40/40 tests** · band in
  the audit record AND the log · **0 orders / 0 trades since deployment**, **0 MARKET orders ever**.
- ⭐📦 **THE TWO-DIST kiteconnect TRAP IS PC-ONLY** — the twin enumerates **ONE** (5.1.0), and
  `check_sdk_version` passes there. ⛔ Do not generalise the trap to the twin or production.
- 🔴⏸ **THE CODE IS NOT LIVE.** Service started **08:15:26**; the new file's mtime is **13:32:57** — the
  running process holds the OLD modules. ⇒ **today's 15:03 runs the OLD unprotected path unless
  `sudo systemctl restart trading-system` is run on `trading-sbx`.** ⛔ Not restarted by me — not in the
  authorised action list, and the standing rule is to hand over the command. ⭐ Pre-flight green: kill switch
  INACTIVE (auto-cleared 08:15:26), 0 open trades, boot-path checks pass.
- ⛔ **No push. No production. No broker order.** ⛔ Block A only — Block B, check9 and the EOD fallback untouched.

## 10-Sep-2026 (Thu) ROUND 5 — 🟢 **BLOCK A BUILT + GATE-CLEAN** · ⛔ UNPUSHED · ⏸ REVIEW OWED

- 🟢🛠️ **BUILT on `fix/market-protection-10sep` @ `3b15bbf`** — 5 files +367/−3, plus a new 38-test file.
  ⚠️ **LABEL: BUILT + GATE-CLEAN. ⛔ NOT DEPLOYED, ⛔ NOT VERIFIED LIVE.** ⛔ 0 commits, ⛔ nothing pushed.
- 👤 **BANDS ARE RAMA'S: PASS_1 = 1.5, PASS_2 = 2.5 (PERCENT).** ⚠️ Historical coverage, ⛔ not a guaranteed fill.
- 🟢🧪 **GATE DIFFERENTIALLY CLEAN:** 7F/**6101P** vs baseline 7F/6063P, failure sha256 **identical**
  `1855d12c70394465`, `comm -13` and `comm -23` BOTH empty, **+38 decomposes exactly**. `RAW_PYTEST_RC=1`.
  ⭐ **Non-vacuity PROVEN BY MUTATION** (3 mutations → 3/9/7 RED, all files restored byte-exact).
- ⚠️⚠️ **THE UNITS TRAP IS GUARDED THREE WAYS** — `_percent` naming · config-load refusal at BOOT · adapter
  chokepoint re-check. 🔬 `0.015` REFUSED. ⭐ The decisive test asserts the **form-encoded wire body**.
- 🔴⚠️ **§1.4: THE ADAPTER FIXES ONE PATH, ⛔ NOT THREE.** ⏸ **STILL BROKEN:** check9's emergency MARKET
  exit (`order_reconciler.py:3078`) and eod_squareoff's phase-2 MARKET fallback (`:1663`). Fixable, ⛔ not fixed.
- 🔴⏸ **BLOCK B REMAINS AN ACCEPTED, VISIBLE COST:** a *successful* MIS squareoff may now be classified
  **EXTERNAL_UNATTRIBUTED** — the inverse of ORCHPHARMA. 👤 Rama's accepted trade for shipping fast.
- ⛔ **NEXT: review → twin → production.** ⛔ No push. ⛔ No broker order. ⛔ No production test.

## 10-Sep-2026 (Thu) ROUND 4 — ⭐ SPECIFICATION DELIVERED · 🔴 THE ROW IS NOT FREE · ⏸ REVIEW OWED

- ⭐⚖️ **ANSWER: TWO FIXES, ONE ARTEFACT, PLUS A THIRD REQUIREMENT** — the row must be **TRACKED**, not just
  written. `order_monitor.track()` → EventBus → `order_manager` is the only thing that advances an `orders`
  row to COMPLETE, and `mis_autosquareoff` takes ⛔ **no** order_manager / order_monitor / event bus today.
- 🔴💥 **WRITING THE ROW CHANGES CHECK 9.** FIX-155's guard (`order_reconciler.py:2887-2891`) already keys on
  `leg='EOD' AND order_type='MARKET' AND status IN (PENDING,SUBMITTED,OPEN)`. ⭐ Correct while the exit is live;
  🔴 **latches forever and silently disables CHECK 9's emergency exit if the status is never advanced.**
  ⇒ ⛔ the claim *"no unrelated flow changes"* cannot be made.
- ⭐🏷️ **`'EOD'` IS THE RIGHT LEG — no migration, no classifier change.** Distinguish by **`leg_index`**
  (`eod_squareoff` already uses 0 = primary, **1 = residual sweep**; no CHECK on the column).
  🔴 ⛔ **NOT by tag — the `orders` table has NO tag column.**
- ⭐🔍 **THE `trade_id` BLOCKER DISSOLVES.** `get_open_intraday_positions()` already resolves it with no
  resting leg; 🔬 `(symbol, direction)` unique — **0 same-direction overlaps all-time**, 0 open trades now.
  ⚠️ Rests on **config** `one_trade_per_symbol_direction_per_day: true`, ⛔ not a schema constraint.
- ⛔🔁 **TAG-CORRELATION REUSE IS LARGER** and returns a broker dict, ⛔ never the local row the classifier
  reads — and *"entry+SL+TGT share that tag"* makes an exit-side query structurally AMBIGUOUS.
- 🔴🧪 **THE TWIN CAN NEVER PROVE THE PARTIAL PATH.** A protection-converted partial needs price to move
  outside the band during execution — ⛔ not commandable. ⭐ Unit-only forever; `FakeAdapter`'s existing
  **`after=`** already expresses it. ⭐ Stated now, ⛔ not discovered at the gate.
- 🔴📊 **A SECOND DEAD FILL-FIELD:** `update_order_status` writes `qty_filled`, yet **668 COMPLETE rows, 668
  with `filled_at`, 0 with `qty_filled>0`**. ⭐ `trades.qty_filled` IS alive (365/366) — ⛔ don't generalise.
- 🔴📦 **`check_sdk_version` reads METADATA, not the import** (`utils/startup_checks.py:1338`, wired `:1626`)
  while TWO kiteconnect dists are installed. ⭐ Pin from `__file__` + `__version__`. ⛔ No package change.
- ⏸ **THE SPECIFICATION IS FOR REVIEW.** ⛔ Nothing built. ⛔ Zero commits.

## 10-Sep-2026 (Thu) ROUND 3 — 🔴 INVERSE DEFECT CONFIRMED · ⭐ VERDICT: **TWO ITEMS, ONE ARTEFACT**

- 🔴🔁 **THE INVERSE DEFECT IS REAL.** A *successful* MIS auto-squareoff would be logged
  **`EXTERNAL_UNATTRIBUTED` at CRITICAL** — the exact mirror of ORCHPHARMA's false `OWN_SL`. ⭐ The filled
  order's broker id **is** collected; ⛔ there is no local leg to bind it to.
  ⇒ ⛔ **Fixing the exit without this swaps a false positive for a false negative.**
- ⭐⚖️ **VERDICT FOR THE IMPLEMENTATION PLAN: TWO ITEMS SHARING ONE ARTEFACT.** CANCEL needs only an
  in-pass handle. ATTRIBUTION needs persistence + `trade_id` + an accepted leg, and hits the `orders.leg`
  **CHECK constraint** (`schema.sql:322` ⇒ migration), the `SL/TGT/EOD`-only classifier map, and 🔴 **a
  `trade_id` that is unavailable exactly when `resting` is empty — the naked case.**
- 🔴🏷️ **THE EXIT TAG CANNOT TELL THE PASSES APART** — `"mis_autosq_pass_1"` is 17 chars, truncated to
  16 ⇒ **both passes send `"mis_autosq_pass_"`.** ⭐ It survives to the broker and comes back on
  `get_all_orders()`; ⛔ `get_open_orders()` drops the tag entirely.
- ⭐🔎 **`get_open_orders()` ALREADY sees a triggerless residual** — the `trigger_price > 0` filter is in the
  CALLER (`_restore_protection_inner:743`), ⛔ not the query. ⇒ ⛔ **nothing needs broadening in the restore
  filter.** `get_all_orders()` is the smallest query that both sees AND attributes.
- 🔴☠️ **DEAD MACHINERY, recorded so it is not mistaken for working:**
  `MisState.EXIT_PARTIALLY_FILLED` declared, **never assigned** (0 refs) ·
  `_retry_remaining_mis_positions` defined, **never called** (0 call sites).
- ⭐🛑 **THE REFUSAL SEMANTICS ALREADY EXIST** — `:617-626` refuses to submit, restores, emits CRITICAL and
  skips **that symbol only**. ⭐ What is missing is the **trigger**, ⛔ not the behaviour.
- ⚠️ **I CORRECTED TWO OF MY OWN CLAIMS THIS ROUND:** the protected-MARKET wording (now
  *"protected execution range … may leave unfilled quantity open"*), and my "three `INSERT INTO orders` sites"
  — it is **SEVEN**; my grep missed `INSERT OR IGNORE`. ⭐ Conclusion unchanged and stronger.
- ⛔ **NOTHING BUILT. ZERO COMMITS.**

## 10-Sep-2026 (Thu) ROUND 2 — 🟢 COVERAGE TABLE · 🔴 PARTIAL-FILL BLIND SPOT · ⏸ STILL 👤 RAMA'S CALL

- 🟢📊 **COVERAGE TABLE DELIVERED** (bands 0.5-5.0 % as measurement bins, PASS_1 vs PASS_2, inside /
  exceeding / coverage %, exact n, full query definition). ⛔ **No band recommended — by design.**
  ⭐ The decisive line: **PASS_1 reaches zero exceedances at 3.0 %; PASS_2 still has 2 at 4.0 % and only reaches
  zero at 5.0 %.** p99.9 **2.170 % vs 3.613 %**. ⇒ "materially different" is MEASURED.
  ⭐ n = **1,647**/pass (all traded symbols) and **289**/pass (MIS-held). SELL-only table; 🔬 the book is
  **275 LONG / 41 SHORT**, and the BUY tail is milder at every band ⇒ a SELL-chosen band covers BUY too.
- 🔴🧩 **THE PARTIAL-FILL BLIND SPOT IS REAL AND STRUCTURAL** —
  [[partial_fill_residue_is_invisible_to_the_cancel_step_10sep]]. ⭐ PASS_2 re-derives qty from a fresh
  `get_positions()` (🟢 correct), ⚠️ **but that is necessary and NOT sufficient**: the resting remainder is
  never cancelled, so both can fill. ⭐ **Latent today** (0 MARKET rows ever) — ⛔ the `market_protection`
  repair is what arms it. ⇒ ⏸ **must be in the implementation spec.**
- ⏸👤 **STILL OWED: RAMA'S 7 CHOICES**, four of them the band values. ⛔ Nothing may be built first.
- ⏸ **STILL OWED: the `check1_mid_fill_defer_sec` policy decision.** Still **0.0 (OFF)**. ⛔ Not changed,
  ⛔ not recommended, ⛔ and explicitly not lost.
- ⏸📄 **FOLLOW-UP RECORDED — THE UNCOMMITTED PRIMARY-TREE CONTENT.** 🔬 Measured: `PATHS.md` **279,596 B**
  + `docs/SYSTEM_MAP.md` **319,578 B** = **599,174 B (~585 KiB)**, only **8,830 B** of it mine from today;
  **+1,478 / −44 lines across 10 modified tracked files**. ⇒ reconcile deliberately AFTER this batch boundary.
  🔴 **AND THE TRAP INSIDE IT:** HEAD's blobs are **pure LF**, the working copies **pure CRLF** (rewritten before
  this session) ⇒ committing as-is rewrites EVERY line ending and makes the diff unreviewable. ⭐ Decide the
  line endings explicitly as part of that reconciliation.
- ⭐ **PIN AT THE IMPLEMENTATION GATE (carried):** two `kiteconnect` dist-info dirs (5.1.0 **and** 5.2.0) while
  the import is 5.1.0. ⛔ Do not change packages — pin and document the ACTUAL import origin. Same provenance
  family as the testing VM's stale git stamp.
- ⛔ **NOTHING BUILT. ZERO COMMITS. Production not touched this round** beyond one read-only SQL.

## 10-Sep-2026 (Thu) MEASURE-ONLY — 🟢 WORKTREE + BASELINE · 🟢 3 MEASUREMENTS · ⏸ 7 CHOICES OWED FROM 👤 RAMA

- 🟢🗂️ **DEDICATED WORKTREE STOOD UP:** `fix/market-protection-10sep` @ `3b15bbf` in
  `D:/Projects/wt-mktprot-10sep`. **ZERO commits.** ⭐ Seeded `config/instruments.csv` (cp, md5
  `a7b07623909e051cb624ad157cee1671`), `data_store/`, and a `--system-site-packages` **venv**;
  ⛔ `.env` deliberately NOT seeded.
- 🔴⚠️ **THE INHERITED `PYTHONPATH` WAS `D:\Projects\trading-system` — THE PRIMARY TREE.**
  ⭐ That is the exact 02-Sep false-RED mechanism, live in this session's shell. It was **overridden
  explicitly** to the tree under test and recorded beside the count. ⛔ Never inherit it.
- 🟢🧪 **BASELINE: 7 failed / 6063 passed / 5 skipped, `RAW_PYTEST_RC=1`**, failure sha256
  `1855d12c70394465`, 1223.75 s, started 09:52:59 IST. ⚠️ **The instruction's standing 10F/6054P is pinned to
  `20061b6`, not to our base** — at `3b15bbf` the recorded comparand is **10F/6060P**, and 7F/6063P decomposes
  **exactly**: −3F/+3P, all three `test_t4_deploy_preflight`, which the venv repairs (**proven: that file alone
  = 9 passed in 0.63 s**). ⭐ The remaining 7 ARE the 17-Aug `6fa8a1c` named set. ⇒ 🟢 the tree reproduces
  the baseline in a **cleaner** environment. ⛔ **Never compare this tree against 10F again — its baseline is 7F.**
- 🟢📏 **M1 (band):** measured and reported as a DISTRIBUTION;
  ⛔ **no percentage recommended, by design** — [[squareoff_window_protection_band_measured_10sep]].
  ⭐ The single most decision-relevant number: **PASS_2's minute (15:06) has a materially fatter tail than
  PASS_1's (15:03)** — p99.9 **3.612 %** vs **2.170 %**. ⇒ "two passes, materially different" is now *measured*.
- 🟢🔎 **M2 (closure):** the vocabulary already contains `EXTERNAL_UNATTRIBUTED` ⇒ ⛔ no new enum.
  The false `OWN_SL` is **precedence rung 4** — [[mid_fill_rung_manufactures_own_sl_10sep]].
- 🟢⚙️ **M3 (`-1`):** `-1` and a number marshal **identically**; the SDK validates **nothing**
  (`999`, `-7`, `0`, `2.5` all reach the wire) ⇒ ⭐ one mechanism serves both passes, ⛔ and the bounds check
  is ours — [[no_order_path_can_send_market_09sep]].
- 🔴📅 **A THIRD INCIDENT SURFACED: 07-Sep V2RETAIL**, never written down. Same shape as ANANTRAJ and
  ORCHPHARMA — but ⭐ **the system's own EOD aggressive LIMIT rescued it at 15:17:07 with no human**, and ⭐ its
  closure_source is **CORRECT** (`EXTERNAL_UNATTRIBUTED`), which is what exonerates the classifier.
- ⏸👤 **OWED — RAMA'S 7 CHOICES, four of them the market-protection values.** ⛔ **NO implementation may
  begin before they arrive.** The evidence he asked for is now on record; the choice is his and ChatGPT reviews it.
- ⏸ **OWED — a decision on `check1_mid_fill_defer_sec`.** ⭐ It is the guard that was built for exactly this
  failure and it is set to **0.0 (OFF)** in production. ⛔ Not changed by me; ⛔ not recommended by me.
- ⛔ **NOTHING BUILT, NOTHING PUSHED, NO ORDER PLACED.** Production was touched **read-only** only.

## 09-Sep-2026 (Wed) STEP-1 SURVEY — Batch-1 fixation, READ-ONLY at `3b15bbf`

- 🔴 **(A) THERE IS NO LIVE `L3` GATE — the name does not exist here.** 🔬 Every
  `L3` match is an unrelated decision-id (`OPL3`, `RL3`, `L3` log-routing
  `core/logger.py:14`, `CL3`). ⭐ **R:R NEVER REJECTS**: `hard_gate.py:1-8` — the
  V3 gates (confirm/pullback/R:R/HTF/extreme) are *"PLAYBOOK-shadow scope… NEVER
  reject a live order"*. 🔬 `scoring_weights.yaml:39` `v3_hardgate_mode:"shadow"`;
  `system_config.yaml:562` `v3_chain_mode:"shadow"` (LOG-ONLY).
  ⛔ **Never write "L3" into a card again.**
- 🔴🔴 **(B) `_broken_zone` IS NOT A LIVE ADMISSION INPUT — it runs ONLY on
  already-PLACED trades.** 🔬 `sr_detector/flags.py:125`; reaches the processor
  solely via `_sr_observe` (`signal_processor.py:508`) called at **`:1406`, AFTER
  `place()` and AFTER status=PROCESSED** — *"non-gating observer"*. ⇒ ⭐ rejected
  signals (3,824 of 3,852 on 08-Sep) NEVER have it computed. **B1.6's axis changes.**
- 🔴 **(C) `signal_id` IS MACHINE-LOCAL — the two arms cannot join on it.**
  🔬 `core/ids.py:50` zero-arg UUID4, minted per machine at
  `webhook_receiver.py:957`. 🔬 15:04:30 IST, both sides in ONE instant:
  prod 5,948 / sbx 5,301, **INTERSECTION 0**. ⭐ Only natural key
  `symbol|strategy|triggered_at` — UNIQUE within each machine, intersecting **833**.
  ⛔ Chartink's payload carries NO event id; `webhook_audit` shares none with `signals`.
- ✅ **(D) THE 36.6% IS NOT A LEAK.** 🔬 318 of 336 predate the recorder (13-Jul);
  the other 18 are today, pending 18:15. Every completed day 13-Jul→08-Sep is
  **missing=0**. ⛔ Nothing to design against.
- ⭐ **§1.2 — NO SINGLE POINT. THREE ARE NEEDED:** ① ACCEPT — just before
  `place()` at `signal_processor.py:1300` (everything IS in scope). ② PIPELINE
  REJECT — one handler `:1081` catching **61 raise sites**, ⚠️ but what is BOUND
  varies by how far the signal travelled. ③ SCREENER REJECT —
  `secondary_screener._persist:596`, never raises; ⭐ **the LARGEST population
  (`REJECTED_SCORE_*` ~63%)**.
- ⚠️ **THE ENTRY PRICE IS NOT ONE VALUE.** `_derive_prices(trigger_price)` `:922`,
  then **M-S1 re-anchors on a live LTP at `:989-991`** (momentum only `:973`;
  stale fallback on quote failure). ⭐ **The pre-anchor value does NOT survive.**
  `tgt_price` computed later still `:1245`. Only `trigger_price` survives.
- 🔬 **PERSISTED AT DECISION TIME: ONLY `signals.status` + `rejection_reason`.**
  Score, tier, step_results, market_data_snapshot, prices, sizing are in-memory
  only, reconstructed at 18:15. Vocabulary = the `signals` CHECK: 20 enumerated
  + 5 GLOB families; 51 distinct in use.
- 🔴 **§8 — A FAILING RECORD WRITE IS SWALLOWED TODAY.** `_process_one_safe:372`
  catches all; the fallback `update_signal_status` sits in a NESTED try/except
  that also swallows ⇒ one ERROR line, record silently lost. ⭐ Two never-block
  patterns exist (`_sr_observe:531-556`, `v3_chain.observe:1025-1032`) — both
  **log-only**, ⛔ neither wired to `alerts/critical.py::write_critical_sentinel`.
- 🔬 **STORAGE — OPPOSITE EXPOSURES.** `data_store/v3/*.jsonl` is **never-deleted**
  (`output_retention.py:54-55`) but ⛔ **NOT backed up**. A SQLite table IS backed
  up nightly but falls under `db_retention.py:63-70` (90-365d DELETE).
  🔬 579.7 B/row ⇒ **532 MB/yr** at 3,850/day.
- 🔬 **ACCOUNT IDENTITY DOES NOT REACH THE RECORD LAYER** — 0 account columns in
  `signals`/`trades`, 0 acct/host keys in a forward-shadow row. AR12's tag reaches
  alerts/preflight only.
- ⭐ **§5.2 SEPARATION IS NATURALLY AVAILABLE:** the 18:15 recorder is append-only,
  auto-rolls on `_METHOD_VERSION` bump (`forward_shadow_record.py:37-41`), reads
  only its OWN OUT_PATH (`:159-167`). ⚠️ One coupling: writing signal-time evidence
  into the SAME file would be consumed by its `seen` set. `sim_R` needs the day's
  completed candle path ⇒ ⛔ cannot be computed at signal time.
- ⏸ **GAPS STATED, NOT FILLED:** no latency-budget constant at the admission point ·
  ATR timeframe inside `_step_3_atr_filter:271` not traced · per-step weight VALUES
  not enumerated (file + rescale fns named).

## 09-Sep-2026 (Wed) FINAL SWEEP — 🧹 testing VM de-noised

- ✅ **PREFLIGHT IP BASELINE FIXED (testing VM only).** 🔬
  `data_store/preflight/last_known_ip.txt` held **`161.118.187.249`** —
  PRODUCTION's IP, written **2026-06-22**, inherited by the clone — vs an actual
  `130.210.13.114` ⇒ `VmIpUnchangedCheck` raised a **CRITICAL twice a day**
  (Phase A 08:30, Phase B 09:14). Now correct. 🔬 Verified by running the class:
  **PASS** *"public IP unchanged"*; ⭐ non-vacuous — a bogus baseline still FAILs.
  ⛔ **Production's baseline UNTOUCHED — its IP genuinely has not changed.**
- ⚠️ **REGISTERED, ⛔ NOT FIXED:** `VmIpUnchangedCheck` names the **Kite
  dev-console IP allowlist** as the cause but ⛔ **never contacts Kite** — it only
  diffs `ifconfig.me` against a local file. ⭐ A check that asserts a remote cause
  it never tested is a defect in its own right.
- ✅ **FIVE `gemini_*` CRON JOBS COMMENTED OUT, testing VM** (⛔ commented, not
  deleted). 🔬 lines **148 → 148**, **active commands 45 → 40**, active
  `gemini_*` **0**, diff = exactly those 5. ⭐ **`forward_shadow_record` 18:15
  STILL ACTIVE**; `fetch_daily_candles`, `reconstruct_excursions`,
  `system_manager` all still active. ⛔ Production's five untouched.
- 🔬 **INHERITED-STATE SWEEP** (data_store/ + config/, excluding DBs and logs):
  only live-state hit was `preflight/today.json` `"account": "LFL836"` — ⭐ dated
  and **self-correcting** at tomorrow's 08:30 run (AR12 live there ⇒ VBB097).
  ⛔ **LEFT ALONE** — editing it would rewrite what the system actually emitted.
  All else dated history (`critical_alert_*`, `cron_audit/*21-Jun*`,
  `crontab_backups/*`); `trading-system.service` is the shared unit name, benign.
  ⛔ Databases untouched per 👤 Rama.
- ✅ **ORPHAN GTT `335374217` (GRAPHITE) GONE — CLOSED, STRUCK FROM THE REGISTER.**
  🔬 Broker: absent from the GTT list entirely. ⭐ Real check — **ORPHAN GTTs = 0**:
  the one active GTT `335441167` MONQ50 has a position behind it (qty 2).

## 09-Sep-2026 (Wed) Q6 — 🧊 THE BATCH-1 GATE MEASURED · ⚰️ mempalace RETIRED

- 🧊🔴 **Q6 ANSWER: NO. The forward-shadow record does ⛔ NOT contain what B1.6
  needs ⇒ ⭐ the clock starts when the contract ships, ⛔ not in July.** Measured
  read-only at `3b15bbf`. Corpus = `data_store/v3/forward_shadow_fs-v1.jsonl`,
  **168,290 rows**, 40 dates, 13-Jul → 08-Sep, `method_version=fs-v1` throughout.
- 🔴 **ABSENT, all five:** `_broken_zone` · ATR (+timeframe) · the L3 inputs the
  decision consumed · signal-time entry/reference price · S&R level identity+value.
  🔬 The schema is a **FIXED 20 keys in ALL 168,290 rows** — no variation, nothing
  added over time ⇒ ⭐ they were never captured at any point, not merely dropped.
- ⭐🔴 **EVERYTHING PRESENT IS A RECOMPUTATION, ⛔ NOT A SIGNAL-TIME CAPTURE.**
  🔬 `computed_at − ts`: min **3.28 h** · median **5.17 h** · max **13.66 h**, and
  **168,290 of 168,290 (100.00%)** computed >1 h after the signal. ⇒ it is an
  **18:15 batch reconstruction**; every field reflects 18:15 state, not 10:00.
- ✅ **PRESENT:** `side`/`strategy`/`symbol` · `ts` (the TRUE signal time) ·
  fingerprints `git_commit` + `scoring_weights_sha` + `system_config_sha` +
  `method_version` · `decision` **100%** · `reject_reason` **100%** · `sim_R` **96.42%**.
- 🔴 **`realized_pnl` ON 222 OF 168,290 = 0.132% — ONE ROW IN 758.** ⭐ A corpus of
  decisions with **simulated** outcomes and almost no **realized** ones is a
  DIFFERENT OBJECT from what the re-plan assumed, and it is the first thing the
  design round must reckon with. Daily realized: 08-Sep 5 · 07-Sep 9 · 03-Sep 8.
- ✅ **JOINABLE, PERFECTLY** — key `signal_id`: 🔬 **168,290/168,290 = 100.000%**,
  **zero orphans**, and the fabricated-id control **failed to join** (⭐ non-vacuous).
  ⚠️ But 🔬 **335 of 916 trades (36.6%) have NO forward-shadow row at all.**
- 🔬 **FUNNEL, 08-Sep (complete day):** 2,499 requests → 3,852 signals rows →
  **3,852** forward-shadow rows → **3,852** decisions → **19 trades** → **5 realized**.
  ⭐ Stage 4→5→6 is **1:1, losing nothing**. ⇒ ⭐ **the yield that sets the B1.6
  calendar is ~3,850 decisions/day producing FIVE realized outcomes.**
- 🔴 **PB01 IS ⛔ NOT INERT — a LIVE analysis path nobody has examined.**
  `pb01_watchlist` feeds `v3_chain/pb01_entry.py::Pb01EntryStage`, polling
  09:20-11:00 for a 5-min retest. 🔬 **ZERO order-placing call sites**; 812 rows
  transitioning (SKIPPED_GAP 353 · CONSUMED 197 · EXPIRED_WINDOW 129 ·
  INVALIDATED 102 · PENDING 31). ⏸ **REGISTERED, ⛔ not investigated.**
- ⚠️ 🔬 **`REJECTED_SCORE_59` = 32,283 rows** — the population T7's 59.5/60
  boundary would admit. ⛔ **NUMBER RECORDED, ⛔ NOT ACTED ON.** T1-forward,
  T5-forward and T7 stay FROZEN.
- 🔬 **The feed is LIVE, ⛔ not inert:** last write **08-Sep 18:16:24 rc=0**, cron
  `15 18 * * 1-5` present in the live 148-line crontab, unbroken runs 03/04/07/08-Sep.
- ⚰️ **mempalace RETIRED (👤 Rama, 09-Sep).** Directive now **THREE** targets:
  `docs/SYSTEM_MAP.md` · `PATHS.md` · `UNPUSHED_PENDING_DEPLOY_LEDGER`. 🔬 Cause:
  Smart App Control blocks the unsigned `_pydantic_core` DLL at **LOAD** time;
  keeping it = SAC **off permanently**. ⛔ **The backfill question dies with it —
  it is NOT an owed item and must not resurface.**

## 09-Sep-2026 (Wed) DEPLOYED — 🟢 `20061b6` → **`3b15bbf`** PUSHED TO PRODUCTION

- 🟢🚀 **PUSHED 13:0x on 👤 Rama's "push now" ruling** (⛔ not my 15:35 advice — his
  call, and my own measurement supported it). 🔬 `20061b6..3b15bbf`, **explicit
  refspec** `3b15bbf…:refs/heads/main`, fast-forward, 4 commits, 23 files, **all
  `.py`**. 🔬 Post-push all three agree: PC `origin/main` == VM bare HEAD ==
  **`3b15bbf`**, deployed-tree drift **0**.
- ⭐ **WHY A LIVE-SESSION PUSH WAS SAFE — measured, ⛔ not assumed:** the armed hook
  does **`checkout -f`** + a conditional `crontab` install and **NOTHING ELSE** —
  ⛔ no service restart, ⛔ no unit files, ⛔ untracked files (`.env`, `data_store/`,
  `logs/`) untouched. ⇒ ⭐ **the running process keeps its in-memory code; Python
  does not reload.** 🔬 `trading-system ActiveEnterTimestamp=08:15:23`,
  `NRestarts=0` **before and after** the push.
- 🔬 **PRE-CHECKS, ALL RE-MEASURED AT PUSH TIME:** book flat **per the BROKER**
  (net 0 / day 0 / holdings 0) — ⚠️ the LOCAL `trades` row still said `OPEN` for
  GRAPHITE, ⭐ **the broker is the authority and local lagged**; tracked
  modifications on target **0**; fast-forward **YES** via `merge-base --is-ancestor`.
- ⚠️ 🔴 **ONE ACTIVE ORPHAN GTT LEFT: id `335374217` GRAPHITE, triggers
  `[845.55, 888.65]`, with NO underlying position.** 👤 Rama flagged it; ⛔ not
  actioned by me.
- 🟢 **CRONTAB 149 → 148**, and 🔬 the removed line is exactly the spent
  `41 7 7 9 * …revert_delivery.sh`; live now **IDENTICAL** to canonical, 2×
  `--account LFL836` intact. ⭐ Checked the one-shot was genuinely spent before
  letting it go: it fired **07-Sep 07:41:01**, `revert.log` = *"REVERTED OK — all
  3 assert enabled: true"*, and all three delivery YAMLs read `enabled: true`.
- ⭐🔑 **THE PARITY CHECK THAT MATTERED, AND IT IS NON-VACUOUS:** on production's
  real `accounts.csv` → `primary_account_tag()` = **`LFL836`** (⛔ not VBB097);
  every label renders `[LFL836]` / `[LFL836-BAN]`; `primary_api_key_env()` =
  **`ZERODHA_API_KEY_LFL836`** and the value **== `os.environ[...]`** exactly.
  ⭐ Control: the SAME code on a VBB097 csv returns `VBB097` ⇒ the check could
  have failed.
- 🔬 **WHEN THE NEW CODE BITES — confirmed, ⛔ not assumed. (a)** Cron spawns FRESH
  python ⇒ **new code immediately from disk**; all 5 credential-fix scripts show
  `LFL836 literals=0` ⇒ ⭐ `forward_shadow_record` gets the fix at **18:15 tonight
  with no restart**. **(b)** The long-running service keeps OLD code until
  tomorrow's 08:15 boot — ⭐ harmless, since all three fixes it carries are
  **no-ops on production**: 🔬 today's webhook traffic = **2356× 200 / 386× 403 /
  400 count = ZERO**, and scanner names arrive UNPREFIXED ⇒ nothing to strip.
- ✅ **PROD EMAIL CONFIRMED STILL GOOD POST-PUSH:** backoff
  `{"consecutive_auth_fails": 0, "last_fail_iso": null}`, degraded marker ABSENT,
  and 🔬 an unprompted REAL sentinel delivered **12:58:37 `-> .delivered`** with
  ⛔ no `via TELEGRAM fallback` tag.
- 🧠 **mempalace RESOLVED — it was a live PyPI package all along (3.9.0).**
  ⚠️ Installed into an **ISOLATED venv** (`C:/Users/rama/.mempalace-venv`), ⛔ NOT
  the gate interpreter: 🔬 a shared install would pull 55 packages and **upgrade
  `click` 8.3.3→8.5.0 and `typing-extensions` 4.15.0→4.16.0**, invalidating the
  very baseline measured today. 🔬 `C:\python311` verified unchanged after.
  `.claude.json` repointed. ⏸ **Needs a Claude Code restart to connect.**
- ⏸ **STILL OWED:** the receiver log-redaction fix (`:490` logs `raw_body`) ·
  the orphan GTT · mempalace backfill (3 days, ~30-45 min once it connects) ·
  `nse_holidays_2027.yaml` · `.gemini` rotation.

## 09-Sep-2026 (Wed) CLOSE — 🟢 SIGNALS FLOWING · 🟢 PROD EMAIL RESTORED · ⛔ NOTHING PUSHED

- 🟢🌐 **THE TESTING VM IS TAKING SIGNALS.** 👤 Rama ruled the `scan_name`
  mismatch be fixed in the RECEIVER (⭐ he cannot drop the column in the Chartink
  UI) — ⚠️ **an explicit override of the Batch-1 freeze, on the signal path,
  recorded as his call.** `_strip_account_prefix()` strips a leading
  `<AR12 tag><- or _>` from the NORMALISED body scan_name before the WR4 compare.
  ⭐ **Config-driven** (`primary_account_tag()`), ⛔ never a literal; prod's tag is
  LFL836 which no alert carries ⇒ **no-op there**. ⭐ **PREFIX ONLY** — a genuine
  mismatch still 400s, and `UNKNOWN` (AR12's read-failure fallback) is explicitly
  NOT strippable.
- 🔬 **THE TRANSITION, MEASURED:** 12:29:06 all **400 / 0 accepted** → restart
  12:29:47 → 12:30:07 **13 scanners ALL 200**, `signals_accepted=56`,
  `signals_rejected=115`, and 🔬 **56 rows in `signals`** — ⭐ the accounting
  closes exactly. Gate **DIFFERENTIALLY CLEAN**: 10F/**6060P** vs baseline
  10F/6054P, failure sha256 identical `46c38a3eee03d34b`, both `comm` empty, and
  ⭐ the **+6 decomposes exactly** into the 6 named WR4b tests.
- ⭐ **THE 6 TESTS ARE NON-VACUOUS BY MEASUREMENT:** with the strip neutralised,
  the 2 asserting NEW behaviour **FAIL** and the 3 asserting PRESERVED behaviour
  still pass ⇒ 2 prove the fix, 3 guard against weakening it.
- 🟢📧 **PRODUCTION EMAIL RESTORED — AND THE CREDENTIAL ALONE DID NOT DO IT.**
  🔴 A **persisted SMTP backoff survived the restart** (see the RULES entry):
  n=11 ⇒ 30-min cap ⇒ SMTP never attempted, first sentinel went Telegram-fallback
  and was marked `.delivered`. ⭐ Cleared via the code's OWN `_reset_smtp_state()`,
  then proved by CONTRAST 64 s apart. 🔬 `alert_watcher_degraded.json` **deleted by
  the successful send** — the marker the canary/Officer read. 🔬 Canary's own
  `check_email_path()` (login-only, never sends) → `ok=True`.
  ⇒ ⭐ 08:20 canary passes tomorrow, ⛔ and it never depended on the restart.
- 🔑 **LEAK CLOSED.** 🔬 The new secret leaked 12:20:06→**12:29:06** only (130/file)
  — it stopped at the restart because ⭐ **only the 400 branch logs `raw_body`**
  (`:490`, the sole such call). 🔬 DB occurrences **0** throughout —
  `_sanitize_payload_for_storage` protects STORAGE; the LOG path does not.
  ⏸ **RECEIVER LOG-REDACTION FIX STILL OWED** — ⛔ not done today.
- ✅ **ALSO SHIPPED TO THE TESTING VM ONLY (all differentially clean):** the AR12
  label fix (16 files) and the AR12b credential-env fix (6 files:
  `forward_shadow_record` first, done well before its 18:15 run). 🔬 On the VM:
  `api_key_env=ZERODHA_API_KEY_VBB097`, key resolves, `_ACCOUNT=VBB097`,
  **0 `LFL836` literals**; `alert-watcher` restarted 12:30:17 ⇒ `_ACCOUNT_TAG=VBB097`.
- ⛔ **NOTHING PUSHED.** All of it sits on `fix/account-tag-from-registry-09sep`
  off `20061b6` in a worktree; ⭐ the F2 branch was NEVER checked out. Production
  received `.env` + an `alert-watcher` restart and nothing else.
  ⏸ **Push + a production deploy of all four fixes remain OWED, 👤 Rama's call.**
- ⚠️ **EVERY SERVICE RESTART TODAY WAS DENIED TO ME by the permission layer**
  (prod `alert-watcher`, sandbox `trading-system` x2, sandbox `alert-watcher`).
  ⭐ Hand Rama the exact command; ⛔ do not engineer a workaround.

## 09-Sep-2026 (Wed) MIDDAY — 🟢 TOKEN + LABELS DONE · 🔴 CHARTINK 400 · 🔑 SECRET ROTATED

- 🟢🔑 **ITEM 1 CLOSED.** 👤 Rama granted the Kite consent; `auto_refresh_token.py`
  **rc=0**. 🔬 Token 11:15:03.479 (`account_id=VBB097`, **0x LFL836**) ->
  `token_watcher` logged *"Fresh token detected ... Starting"* at **11:15:05**,
  i.e. **2 s**, inside its 30 s poll — ⭐ started BY ITSELF, ⛔ not by hand.
  `NRestarts=0`, `Result=success`. 🔬 Broker `k.profile()` -> **`user_id=VBB097`**.
- ⚠️ **`/health` AND `/metrics` ARE ON :8080, ⛔ NOT :5000.** 🔬 :5000 is the
  webhook receiver (401 on an unauthenticated GET — ⭐ correct, ⛔ not a fault);
  :8080 is `scripts/healthcheck_server.py`, loopback-only by design (C-3).
  🔬 :8080 `/health` **200** · `/metrics` **200** · `/metrics/prometheus` **200**.
  ⛔ I probed the wrong port first and briefly called it a failure.
- 🟢🌐 **3.3 PROVEN, AND IT PROVED ITSELF** — 60 s after startup, REAL Chartink
  traffic from `23.106.53.213` wrote `webhook_audit` rows. OCI ingress -> host
  iptables -> app -> DB all confirmed by live traffic, ⛔ no synthetic POST needed
  (⭐ I could not have sent one: ingress admits only Chartink's IP).
- 🔴 **BUT ZERO SIGNALS ENTER — every post 400s.** 🔬 `webhook_receiver.py:590`
  `if body_scan_name is not None:` then `:591` requires
  `scan_name.lower().replace(" ","_") == <path>`. Chartink's alerts carry a
  **`VBB097-` prefix** => `vbb097-gap_fade_short` vs path `gap_fade_short` => 400,
  `signals_accepted=0`, before any parsing. ⭐ **REMEDY = REMOVE the `scan_name`
  column** — `:590` is the skip-branch and `:578` requires only
  `stocks/trigger_prices/triggered_at`. ⛔ NOT a rename (collides with prod).
  ⛔ Do NOT make the receiver strip a prefix — signal path, Batch 1 frozen.
- 🔑 **SANDBOX `WEBHOOK_SECRET` ROTATED** (old `b61b4cccf9eb` -> new
  `2f89bbe80e44`, hashes only). ⚠️ **SPLIT STATE: `.env` has the new one, the
  RUNNING process still has the old** — ⛔ my `systemctl restart` was DENIED by
  the permission layer (both `trading-system` and `alert-watcher`). ⏸ 👤 Rama's.
  📄 `C:/Users/rama/Downloads/CHARTINK_UPDATE_09-Sep-2026.txt` — restart cmd,
  the scan_name instruction, new secret, **16 URLs** taken from
  `config/scan_webhook_map.yaml` (⭐ NOT from observed traffic — `range_breakout_*`
  have never posted and would have been missed).
- 🔴📜 **THE 400 BRANCH LOGS `raw_body` VERBATIM AND CHARTINK ECHOES THE TOKEN.**
  🔬 Exactly ONE `raw_body=` call — `:490`, inside the 400 path; auth failures log
  NOTHING. => ⭐ **the RESTART alone stops the leak** (old token -> 401, no body
  logged), before Chartink is touched. 🔬 Purged 169/file, inodes preserved (live
  fds), ⛔ but it re-accumulated **65 in 4 min ~ 13/min/file** — ⭐ purging before
  the root cause stops is futile. 🔬 DB occurrences **0** —
  `_sanitize_payload_for_storage` protects STORAGE; the LOG path is unprotected.
  ⏸ Receiver fix OWED, ⛔ not today.
- 🟢🏷️ **LABEL FIX DEPLOYED — TESTING VM ONLY, VERIFIED LIVE.** 🔬 Gate
  **DIFFERENTIALLY CLEAN**: baseline 10F/6054P vs changed 10F/6054P, failure-set
  sha256 **identical `46c38a3eee03d34b`**, `comm -13` and `comm -23` BOTH empty.
  16 files md5-verified on the VM; live tree renders `[VBB097]` everywhere.
  ⏸ `alert-watcher` restart owed (it caches `_ACCOUNT_TAG` at import).
- ⏸ 🔴 **PRODUCTION EMAIL STILL DOWN — THE APP PASSWORD VALUE NEVER ARRIVED.**
  🔬 Only the app NAME reached me (`Output-trading system.txt:128`,
  *"LFL836-trading-system-prod"*). ⛔ Not guessed, ⛔ not hunted for. ⏸ 👤 owed.

## 09-Sep-2026 (Wed) MORNING — 🔴 TESTING VM BLOCKED ON A **CONSENT SCREEN** · 🔴 PROD EMAIL DEAD SINCE **07-Sep**

- 🔴🔑 **THE 08:15 TOKEN FAILURE IS ⛔ NOT THE IP ALLOWLIST AND ⛔ NOT THE
  API KEY — IT IS A ONE-TIME KITE CONNECT AUTHORISATION THAT HAS NEVER BEEN
  GRANTED.** 🔬 Traced hop by hop (read-only, no token written): `/api/login`
  **200 status=success** · `/api/twofa` **200 status=success** ⇒ ⭐ credentials
  and TOTP are GOOD. Then hop 0 `connect/login` **302** → hop 1
  `connect/finish` **302** → hop 2 **`connect/authorize` 200 HTML** (a Vue
  shell; the production code reads no body, hence the bare *"request_token not
  found (HTTP 200, hop 2)"*).
- ⭐ **THE DECISIVE READ — the authorize screen's own backing API**
  `GET /api/connect/session?api_key=…&sess_id=…` → **200**:
  `app.name="trading-sandbox"` · `app_id=301057` · `user_id="VBB097"` ·
  **`"trusted": false`** · `redirect_url="http://127.0.0.1"` · a 4-item
  permission list. ⇒ 🔴 **Kite is showing the CONSENT screen and waiting for a
  human.** ⭐ On production the same code works headlessly because LFL836
  granted this consent long ago — `connect/finish` then 302s straight to the
  redirect URL carrying `request_token`.
- ⏸ 👤 **OWED FROM RAMA — ONE BROWSER ACTION:** open
  `kite.zerodha.com/connect/login?v=3&api_key=<VBB097 app key>`, log in as
  **VBB097**, click **Authorize** once. ⛔ I did ⛔ NOT click it — granting API
  permissions on a trading account is his act, not mine. ⭐ The page was left
  open in Chrome, verified showing *"Login to trading-sandbox"* / **VBB097**.
- ⭐ **`redirect_url = http://127.0.0.1` IS ⛔ NOT A DEFECT — DO NOT "FIX" IT.**
  The browser will land on a dead page after Authorize; that is fine, the grant
  is recorded server-side. And `_fetch_request_token` reads the token from the
  **Location header** before ever fetching that URL (its own comment says so).
- ⚠️ 🔬 **THE PREFLIGHT IP CLAIM IS A HYPOTHESIS, ⛔ NOT A MEASUREMENT** — see
  the RULES entry. Its sandbox baseline file holds **production's** IP
  `161.118.187.249` (written **22-Jun**, inherited by the disk clone) vs actual
  `130.210.13.114`. ⛔ Nothing on either VM can read what IP the Kite console
  has registered; that lives only in the dev console.
- ✅🌐 **OCI INGRESS FOR TCP 5000 NOW EXISTS — the 08-Sep blocker is CLEARED.**
  🔬 Read read-only via the OCI SDK, DEFAULT profile, after proving the profile's
  tenancy actually contains `trading-system-sandbox` (public IP match): subnet
  `subnet-20260906-1032`, **1 security list, 0 NSGs**, ingress rule 4 =
  **TCP dport 5000 from `23.106.53.213/32`** — ⭐ exactly the recommended source,
  matching host `iptables` INPUT rule 5. ⛔ 3.3 (an external POST proving 200 +
  a `webhook_audit` row) is **NOT YET DONE** — nothing binds :5000 because the
  service is down for want of the token.
- 🔴📧 **PRODUCTION EMAIL HAS BEEN DEAD SINCE 07-Sep, ⛔ NOT 08-Sep — THE
  INSTRUCTION FILE'S PREMISE IS WRONG AND THE SOURCE WINS.** 🔬 The canary is a
  once-a-day 08:20 check, so it could only show 08-Sep. The **alert-watcher
  loop** caught it far earlier: last good email **07-Sep 09:20:11**
  (`…091947_0010252b.flag -> .delivered`, no fallback tag); first failure
  **07-Sep 15:03:15**. ⇒ ⭐ It **PREDATES** the 08-Sep credential work ⇒ an
  INDEPENDENT defect, and 4.5 fires.
- 🔬 **`.env` IS UNCHANGED SINCE 05-Sep 23:14:31 and the value is a well-formed
  16-char app password ⇒ THE STORED CREDENTIAL DID NOT CHANGE; GOOGLE STOPPED
  ACCEPTING IT.** Account = **`pythonsystemalerts@gmail.com`** (both USER and
  TO) — ⛔ **NOT** the sandbox account `sandboxpythonsystemalerts@gmail.com`.
  ⚠️ `ALERT_SMTP_PASSWORD` and `ALERT_EMAIL_PASSWORD` hold the **SAME** value
  (measured), so ⛔ I **cannot** distinguish *app password revoked* from
  *account password changed* from the VM — that discriminator lives only in the
  Google account's App-passwords page. ⭐ Either way the remedy is identical.
- ⭐ **4.4 ANSWERED — APPLYING THE NEW PASSWORD DOES ⛔ NOT REQUIRE RESTARTING
  TRADING.** 🔬 `smtplib` appears in exactly **two** runtime senders,
  `scripts/alert_watcher.py` and `scripts/monitoring_canary.py`; **`main.py`
  never sends email** (it writes sentinels). `alert-watcher.service` has
  `BindsTo=` and `PartOf=` **EMPTY** ⇒ independent of `trading-system`. ⇒
  edit `.env` + **`systemctl restart alert-watcher`** ONLY. Cron senders pick
  it up on their next run with no restart at all.
- ⏸ 👤 **OWED FROM RAMA:** regenerate the Gmail app password for
  `pythonsystemalerts@gmail.com`; I update `.env` and restart **alert-watcher
  only**, at a moment he chooses.

## 08-Sep-2026 (Tue) 22:26 — 🟢 REBOOTED, SEVEN UP · 🔴 CHARTINK CANNOT REACH :5000

- 🟢 **THE REBOOT PROVED THE MACHINE COMES UP ALONE** (starting the units
  by hand would not have). 🔬 boot_id `eaa7b5f2…` → `1a7f2baf…`, boot
  **22:26:13**; **all seven now carry a populated `ActiveEnterTimestamp`**
  (22:26:22–23) — the field that was **EMPTY** before. 🔬
  `is-system-running` = **running**, **0 failed**. cron **active, 149 lines,
  2× VBB097 / 0× LFL836**. TZ **Asia/Kolkata**, NTP synced.
- 🔴🌐 **BLOCKING — THE OCI SECURITY LIST HAS NO INGRESS RULE FOR TCP
  5000.** 🔬 Read-only via OCI SDK, **DEFAULT** profile (🔬 its tenancy ==
  the sandbox instance's; the **PRODUCTION** profile does NOT match and was
  refused): **1 security list, 0 NSGs, ingress = TCP 22 + ICMP ONLY**.
  ⇒ 🔴 **all 16 Chartink alerts point at `130.210.13.114:5000` and every
  packet is dropped before it reaches the host.**
  ⏸ 👤 **FIX OWED — add ingress TCP 5000, ⭐ source `23.106.53.213/32`,
  ⛔ NOT `0.0.0.0/0`.** ⛔ Not taken — an internet-facing port is Rama's call.
  ⚠️ Until then the failure is **SILENT**: nothing alerts on traffic that
  never arrived.
- 🔬 **Proven in three layers:** app **GOOD** (real receiver + real secret
  → `/health` **200**; wrong token → **401**, so it could have gone the other
  way) · host firewall **CORRECT** (`iptables` admits :5000 from
  **`23.106.53.213/32` only**) · 🔴 **the cloud layer is the block** — with my
  own IP temporarily allowed the external connect **STILL timed out**.
  ⛔ Temp rule removed; 🔬 my IP now appears **0** times.
- ⭐ **Three units not `active`, ALL BY DESIGN:** `trading-system` **exited 0**
  — *"Outside service START window [08:00-18:15 IST]"* (FIX-189) ⇒ ⛔ nothing
  binds :5000 overnight · `trading-watchman` `BindsTo` it · `security-watcher`
  is a **60 s heartbeat** whose unit file says *"NRestarts is NORMAL"*.
- ✅ 🔴 **MY ALERT-CHANNEL CLAIM IS WITHDRAWN — IT WAS WRONG.** 🔬 Settled
  by **sending**: Telegram **`@sandbox_py_bot`** → channel **`sandbox_system`**
  (id `<TELEGRAM_CHANNEL_ID_REDACTED>`, PRIMARY *and* SECONDARY), `success=True`; email
  **`sandboxpythonsystemalerts@gmail.com`** → itself, through the system's own
  sentinel → alert-watcher path (🔬 `Delivered … -> .delivered` 22:46:36).
  ⇒ ⛔ **nothing production-side. CLOSED.** ⭐ An inference from key names is
  ⛔ **not** evidence — an empirical pass outranks it.
- ⚠️ **`?token=` is logged by the DEV server** — my probe's werkzeug log
  caught the secret (**shredded**). ⭐ The real system uses **`waitress`** and
  does **not** log URLs. ⚠️ The value did reach this session's transcript
  — ⏸ 👤 rotate if it is shared with production.
- 🔬 **Zero side effects:** `webhook_audit` 229,346 → **229,346**; `signals`
  219,361 → **219,361**; firewall byte-restored; `claude-*` units cleared.
- ⏸ 👤 **Line 149 ruling still owed** — inert until **07-Sep-2027**.



## 08-Sep-2026 (Tue) — 🟢 TESTING-VM CRONTAB LIVE · 🔴 THE SEVEN ARE ENABLED BUT NOT RUNNING

- 🟢 **CRONTAB INSTALLED AND LIVE on `130.210.13.114`, 22:08:41 IST**,
  👤 on Rama's typed instruction. 🔬 rc=0 · **149 lines** · md5
  staged==installed · syslog `(ubuntu) REPLACE` · `cron` **active+enabled**.
  🔬 **2 `--account` refs, BOTH `VBB097`; `LFL836` = 0.** ⛔ No push ·
  ⛔ production untouched.
- 🔬 **149 = 148 canonical + 1 appended.** `diff` vs the repo canonical is
  **exactly 3 deltas**: lines 70/94 `LFL836`→`VBB097`, and line 149
  `41 7 7 9 * …/revert_delivery.sh` — ⚠️ a clone-inherited production line,
  date **07-Sep 07:41 already past** ⇒ next fire **07-Sep-2027**. ⛔ Left in
  place (removal breaks the instructed 149). ⏸ 👤 **Keep or drop?**
- 🔴⏰ **THE DECIDING ITEM FOR TOMORROW — START THE SEVEN UNITS (or
  reboot) BEFORE 08:15.** 🔬 All seven `enabled` but **never run this boot**:
  `systemctl enable …` ran **14:26:14**, *after* the **13:02:40** boot, and
  ⛔ **`enable` is not `start`**. Proof ×4: `journalctl -b -u <each>` = **No
  entries** · `ActiveEnterTimestamp` **empty** · `ConditionResult=no` ·
  **no reboot scheduled**. ⇒ 🔴 **`token-watcher` is not polling, so a
  valid 08:15 token starts NOTHING — and it fails SILENTLY.**
  ⭐ `kill_switch_state` = **INACTIVE** (auto-cleared 08-Sep 08:15:19) ⇒
  ⛔ no manual stop standing. ⛔ **Not done by me — a start is Rama's call.**
- ✅ **Parked production token DELETED** —
  `/root/zerodha_token.json.removed-08Sep2026`, proven **1× `LFL836` /
  0× `VBB097`** before `rm`; 🔬 a filesystem-wide `find` now returns
  **nothing**. ✅ Live token path clear + writable.
- 🔬 **`paper_capital=10000` and `capital_share_pct=1` are BOTH INERT here**
  — the unit runs `main.py --mode live`; the live seed is `compute_live_seed()`
  off **broker margins** (`main.py:2074`). `paper_capital`'s only live effect is
  **AR11 `> 0`** validation; `capital_share_pct` is read **only when
  `len(enabled) > 1`**. ⛔ The ₹10,000 match is a **coincidence, not a
  wiring**. ⏸ 👤 Reported, unchanged, as instructed.
- ⛔ **[WITHDRAWN 08-Sep 22:46 — DISPROVEN BY MEASUREMENT.]**
  ~~ALERT-CHANNEL COLLISION (💭 inference):~~ only the
  Zerodha keys were swapped; `TELEGRAM_*` / `ALERT_EMAIL_*` look like
  **production's**. ⇒ tomorrow's `Token refresh FAILED for VBB097`
  **CRITICAL** would land in production's channel. ⭐ The account name
  distinguishes it; ⛔ the hostname does not appear in the message.
- ⚠️ **Cosmetic, manual-VM-act:** `trading-system.service` still comments
  *"primary account (LFL836)"*. ⛔ No functional effect (selection is
  `is_primary` in `accounts.csv` = **VBB097**).
- 🔴 **mempalace STILL DOWN** — `CONNECTION_CLOSED` again this session.
  ⏸ The reinstate-or-retire ruling from 07-Sep is **still owed**.




## 06-Sep-2026 (Sun) — 🔴 SANDBOX PROPOSED, ⛔ NOTHING CREATED · ⏸ 4 DECISIONS OWED

- ⛔ **NOTHING WAS CREATED IN OCI.** ⭐ No instance, no VCN, no key, no payment
  change. ⭐ Production untouched. ⏸ The build STOPS until 👤 Rama answers §2.
- 📄 **THE FULL PROPOSAL IS SAVED: `docs/audit/SANDBOX_PREFLIGHT_06-Sep-2026.md`**
  (62 KB, untracked). 🔬 10 dimensions × adversarial verify, 21 agents, 2.7M
  tokens — ⛔ **do not re-derive it.** ⭐ All 10 came back `PARTLY_WRONG`; the file
  already carries the corrected figures, marked `[CORRECTED]`.
- 🔬 **MEASURED, and it overturns the agents' central premise:** the sandbox
  tenancy **`ramakkrishnan031`** (double-k) is a **SEPARATE** tenancy from
  production — different OCID, and AD prefix **`WIBD:`** vs production's
  **`kveW:`** (AD prefixes are tenancy-scoped). ⭐ It is **Pay As You Go, card on
  file, 0 instances, 0 volumes**. ⇒ ⭐ Its Always Free allowance is untouched and
  🔴 **production's tenancy is never modified at all** — ⛔ no PAYG upgrade, ⛔ no
  billing-stop removal. ⭐ That was the synthesis's largest risk; it evaporates.
- 🔬 **ALWAYS FREE A1 WAS HALVED 15-Jun-2026** → **1,500 OCPU-h + 9,000 GB-h/mo**
  = **750 instance-hours** at 2 OCPU/12 GB. ⛔ The old 4 OCPU/24 GB figure is dead.
  ⇒ ⭐ A 31-day month is 744 h ⇒ **$0.00 even at 24/7**, ⚠️ but only **6 h/month**
  of margin — ⛔ a second instance or any oversizing bills immediately.
- ⚠️ 🔬 **50 GB is NOT selectable** — Oracle requires a custom boot volume
  *strictly larger than* 50 GB. ⭐ Proposed **60 GB**; the image default (47/50)
  also works. ⏸ 👤 Rama's call.
- ⏸ **THE 4 DECISIONS OWED:** ⭐ (1) boot volume 60 GB vs image default ·
  (2) is `ops_dashboard` in scope · (3) authorise the **one** production write —
  a ~750 MB `sqlite3 …?immutable=1 ".backup"` extraction with the service
  stopped · (4) the `.gemini` rotation first? → [[gemini_dir_holds_every_live_credential_06sep]]
- 🔴 ⏰ **TIME-CRITICAL, ⛔ independent of the sandbox — RESCUE THE BROKER CORPUS.**
  🔬 4 of 8 broker-failure classes exist **ONLY** in `logs/system_*.log`
  (~7 trading days retained); the DB half prunes on a rolling **180 days**
  (`scripts/db_retention.py:68`). ⭐ The June market-protection rows delete
  **~12-13 Dec 2026**, the 01-Jul tag-length row (id 7761) **~28-Dec-2026**.
  ⇒ ⭐ One grep + one query → `tests/fixtures/broker_corpus/observed_errors.jsonl`.
  ⛔ **This is the only item that gets worse by waiting.**
- 🔴 **A LIVE MONEY-PATH DEFECT SURFACED (R11) — pre-build review gate, ⛔ not a
  quiet fix.** 🔬 `requests.exceptions.ReadTimeout` is **not** a subclass of
  `TimeoutError`, and `DataException.__mro__` excludes `GeneralException` ⇒ both
  match **no branch** of `_translate_kite_exception`
  (`broker/zerodha_adapter.py:274-330`) and fall through to generic `BrokerError`.
  📄 Proven live: `logs/system_2026-09-03.log:64847`. ⇒ 🔴 `_classify_broker_error`
  returns `STATE_UNKNOWN` only for `BrokerTimeoutError`, so **the only timeout
  class ever seen in production is classified RETRYABLE** — ⛔ a read-timed-out
  *placement* would be retried blind. ⭐ Exactly the double-sell hazard
  `STATE_UNKNOWN` exists to prevent.
- ⚠️ ⏸ **MY OWN FOOTPRINT, OWED CLEANUP (a production write, so not done):**
  🔬 `/tmp/tracked_py.txt` (26,242 B, mode 664) and ~12 SQLite `-wal`/`-shm`
  sidecars written 01:48-02:02 into `data_store/backups/` and `data/`.
  ⭐ **No DB content altered** — every stray `-wal` is 0 bytes. ⭐ Cause: **any**
  open of a WAL-mode DB creates sidecars, ⛔ including `mode=ro`; ⭐ only
  `immutable=1` is clean → carry that into every future read.

## 03-Sep-2026 (Thu) FINAL — ✅ DIVERGENCE 2 FIXED `18dd6cc` · ⏸ DIV 1 DEFERRED

- ✅ **`18dd6cc`** — F1 idempotency is now **SIDE-SCOPED**: `symbol +
  transaction_type + trigger>0`, ⭐ the **same predicate shape as the June
  RAMCOIND fix**, ⭐ reused ⛔ not reimplemented. ⭐ `exit_side` from the SL leg ⇒
  side-symmetric. 🔬 **RED-proof:** old predicate ⇒ `protected=True` ⇒ skip ⇒ **no
  stop**; new ⇒ `False` ⇒ restore placed. ⭐ 4 side tests + PROTECTION_UNKNOWN.
- ⏸ 🔴 **DIVERGENCE 1 DEFERRED — ⛔ a trade-off, ⛔ not a bug.** ⭐ `_fill_map` is
  **local** state ⇒ ⭐ as a *decision input* it would **re-open Div 2** by another
  route. ⭐ Duplicate = 🔬 ~₹13.50 **with** a backstop; ⭐ skipped restore = **full
  tail**. ⇒ ⭐ Proceed-on-unknown stays. ⭐ Added **visibility only**:
  `PROTECTION_UNKNOWN` log, ⭐ distinct from a clean *"no SL found"*.
  ⏸ ⭐ F3 may admit `_fill_map` as **corroboration** (broker-acked `order_id`,
  symbol **AND** side, bounded recency). ⛔ Never a bare presence check.
- ⚠️ **WORDING:** ⭐ the **₹10-20** Friday figure is an **order-of-magnitude
  estimate** (🔬 n=1 RAMCOIND ₹13.50 + assumed 2 % move), ⛔ **NOT a bound** — ⭐ and
  the remediating branch has **never fired in production**.
- ✅ **FULL GATE (⛔ not inherited — money-path): 10F/6037P → 10F/6042P, failure
  sets byte-identical, Δ +5 passed.** ⭐ *"zero new failures; the existing 10
  unchanged."*
- ✅ **PUSHED `ce7cea7..18dd6cc`** (⭐ `389d527` PATHS note rode along, as 👤 FILE 137
  §4 suggested). 🔬 PC = VM bare = deployed tree, **0** differing files.
  🔬 Side-scoped check + `PROTECTION_UNKNOWN` verified present on the VM;
  🔬 schedule still 15:03 / 15:06 / 15:09. ⭐ Engine inactive at 00:09 — ⭐ it boots
  **08:15 today** and will run this code.

## 03-Sep-2026 (Thu) CLOSED — 🔴 DUPLICATE-SL × 3 IN NINE DAYS · ⭐ F1 GAPS NAMED

- 🔬 **Recurrence: IRFC 17-Jun · NIACL 22-Jun · RAMCOIND 25-Jun** — 3 in 9 days,
  none since. 🔬 RAMCOIND: both SLs filled **10:12:49 @ 334.00** ⇒ **−1 naked
  short**, ⛔ **disowned as a human order** (*"no local trade"*), ~**₹13.50**.
- 🔬 **What closed it:** Layer 1(a) `_G5B_SETTLING_WINDOW_SEC=10.0` — ⭐ a **TIMING**
  fix for a ~40 ms TOCTOU race ⇒ 🔴 ⛔ **does NOTHING for F1** (F1's missing row is
  **permanent**). ⭐ Layer 1(b) `_already_has_live_sl()` — **broker-authoritative**;
  ⭐ **that** is the shape F1 copies.
- 🔴 **TWO DIVERGENCES IN MY F1 (mine, ⏸ ledger, ⛔ not changed tonight):**
  1. ⛔ **No second source on a failed read.** 🔬 June falls back to
     `order_placer._fill_map` before concluding *"no SL"*; ⭐ F1 just proceeds.
     ⭐ The fallback already exists in the codebase.
  2. ⚠️ **Looser match** — 🔬 June: `symbol + exit_side + trigger>0`; F1:
     `symbol + trigger>0`. ⇒ ⭐ An opposite-side trigger order would read as
     *"protected"* ⇒ 🔴 **F1 would skip a genuine restore** — ⛔ wrong direction.
- 🔬 **Layer 3: UNTRIGGERED, ⛔ not proven dead.** `SYSTEM_OVERSELL` = **0** in
  retained logs, ⭐ BUT its container runs — **4 × `CHECK2 INFLIGHT_ORPHAN` on 4
  separate days** + daily reconcile cycles. ⇒ ⭐ Better than the 4 *"built yet
  inert"* components (⛔ those had no containing activity), ⛔ but **not proven**.
  ⭐ Say *"container proven live; branch unobserved"* — ⛔ never *"Layer 3 works."*
- ⭐ **Friday residual quantified: ~₹10-20 per occurrence**, needing **two
  simultaneous** broker failures — ⭐ vs **no stop at all**, which is 03-Sep.
- ⏸ ⭐ `389d527` (PATHS branch note) stays **local**; 👤 FILE 137 §4 suggests carrying
  it on the **next intentional code push (F3)**, ⛔ not standalone. 👤 Rama's call.

## 03-Sep-2026 (Thu) LATE-2 — ⭐ `ce7cea7` DOCS PUSHED · ⭐ GATE INHERITED

- ⭐ **Tip `ce7cea7`** (docs-only on STOP A `5455ced`). 🔬 PC = VM = origin, 0
  differing files. ⚠️ It landed **after** 👤 Rama typed *"reverse"* — ⭐ reported
  plainly, ⛔ not left to pass. ⏸ 👤 Leave-vs-revert: ⛔ **no decision given**;
  ⭐ left in place, ⛔ NOT reverted. ⛔ Never force-push over a deployed SHA —
  ⭐ `git revert` or nothing.
- ⭐ **GATE = INHERITED from `5455ced`**, ⛔ never *"passed at ce7cea7"*. 🔬 Proof:
  `git diff --name-only 5455ced..ce7cea7` = **3 paths, all `docs/**` `.md`/`.json`**,
  3058 insertions / 0 deletions; ⭐ the negative filter (anything NOT docs/md/json)
  returns **empty**.
  ⭐ **RULE (new, narrow):** a commit whose diff touches **only** `docs/**`
  non-executable files may **inherit** the previous gate result, ⭐ proven by diff
  and ⭐ labelled *inherited*. ⛔ Any other path ⇒ re-run the gate.
- 🔬 **RAMCOIND PRECEDENT FOUND — it is real and it is exact.** 📄
  `docs/audit/orphan_adoption_22jul2026.md:132`: **25-Jun-2026 10:13, qty −1 @
  334.00** — a duplicate SELL leg filled ⇒ **naked short**, and the system
  **disowned it as a human order** (*"no local trade — not managed by system"*)
  ⭐ because there was no local row. ⭐ `_detect_system_oversell` (Layer 3, "RAMCOIND
  fix") was written in response.
  ⇒ 🟢 ⭐ **GOOD NEWS for F1: Layer 3 reads the `trades` table, ⛔ NOT `orders`**
  (`order_reconciler:1892`, lookback **300 s**), ⭐ so unlike the dedupe net it does
  **not** depend on the row `mis_autosquareoff` never writes ⇒ ⭐ an F1 duplicate
  that double-filled **would** be caught and flattened as `SYSTEM_OVERSELL`/CRITICAL.
  ⚠️ ⭐ But Layer 3 is **remediation after both fills**, ⛔ not prevention. ⭐ Layer 2
  (prevention) still cannot see an F1 order. ⇒ ⭐ **F3 remains the real fix.**
- ⏸ **`389d527` PATHS.md branch-safety note — committed LOCALLY, ⛔ NOT pushed**
  (👤 FILE 136 §8: *nothing else pushed*). ⭐ PC is **1 commit ahead** of origin.
- ⛔ **`_restore_protection` untouched** since the gate. ⛔ Nothing else pushed.

## 03-Sep-2026 (Thu) LATE — ⏰ FRIDAY WATCH 15:03-15:09 · 🔴 3 OPEN ITEMS

- ⏰ 👤 **FRIDAY 04-Sep: MIS ON, watch 15:03-15:09** (⛔ NOT 15:07-15:17 — moved).
  ⭐ Expect **2-3 CRITICALs**: cancel → exit **still rejected** (⛔ F4 not shipped)
  → **F1 restores the stop**. ⭐ That is the system working. ⛔ Rama does NOT flatten
  by hand unless an alert says the **restore itself** failed. ⭐ Naked window is now
  **seconds**, ⛔ not the ~2m20s of 03-Sep. ⭐ Then EOD 15:17 / broker 15:12 (CAS).
- 🔴 **F1's DUPLICATE-SL RISK IS NOT CONTAINED — named + accepted for Friday.**
  🔬 `_check_duplicate_exits` (`order_reconciler:3472`) reads the **LOCAL** orders
  table; 🔬 `mis_autosquareoff` **persists nothing** ⇒ ⛔ an F1-placed SL is
  **invisible** to the dedupe net. ⭐ Reachable when `cancel_order` is rejected AND
  `get_open_orders()` fails ⇒ two SLs ⇒ 📄 the RAMCOIND naked-short outcome.
  ⭐ Accepted: a duplicate stop beats none at 1-share size, and it needs BOTH
  failures. ⇒ 🔴 ⭐ **F3 (persistence) fixes this too** — ⭐ raises F3's priority.
  ⛔ There is no broker-side OCO (software LIMIT_TRIPLE only).
- 🔴 ⛔ **RULE CORRECTED: 15:10 and 15:12 are NOT concurrent** — 🔬 15:10 (03-Aug
  launch) was **superseded** by 15:12 (10-Aug). ⇒ ⛔ *"use the earlier of two
  published figures"* is **WRONG** (it fails if a broker moves a deadline
  earlier). ⭐ **NEW RULE: hold a stated cushion below the CURRENT published
  deadline and RE-VERIFY on a schedule.** ⭐ 15:09 unaffected (3 min below 15:12).
  🔴 ⏸ **STANDING: re-verify Zerodha timings MONTHLY** — 🔬 changed twice in a month.

## 03-Sep-2026 (Thu) LATE — 🟢 STOP A PUSHED `5455ced` · ⭐ NEW SCHEDULE LIVE

- ✅ **PUSHED `80091ce..5455ced`.** 🔬 PC = VM bare = deployed tree, **0** differing
  files. 🔬 Gate: **10F/6021P → 10F/6037P**, ⭐ failure sets **byte-identical** ⇒
  Δ **+16 passed / 0 new failures**. ⭐ Engine inactive. ⛔ MIS not enabled by me.
- 🔬 **LIVE SCHEDULE (verified on the VM): `mis_squareoff_cutoff 15:09`,
  offsets `6m`/`3m` ⇒ PASS_1 **15:03** · PASS_2 **15:06**.** 👤 Rama's objective:
  two complete checks finishing 1 min before Zerodha's earliest action.
  🔴 ⭐ **RULE: ⛔ never design to the LATER of two conflicting broker deadlines**
  (📄 Zerodha publishes CAS **15:12** on the support page and **15:10** in the
  03-Aug post). ⚠️ COST: ~16 min of holding given up on non-CAS (15:25).
- ⭐ **F2** `_verify_cancelled` → bounded **5 s** poll (was ONE at +27-53 ms;
  terminal at +1.115 s). ⭐ 5 s is a **schedule budget**, ⛔ not an n=1 tolerance.
- 🔴 ⭐ **F1** `_restore_protection` restores the SL on **every** failure path,
  with its own parameters, idempotent, symbol-scoped. ⛔ TGT not restored.
- ⚠️ 🔴 **I broke my own "never raises" contract; the EXISTING suite caught it**
  (`KeyError` on a row without `leg`, **inside an already-failing path** ⇒ would
  have masked the failure and skipped its alert). ⭐ Fixed via `_row_get` + outer
  guard, ⭐ both pinned by tests. ⇒ ⭐ RULE: a helper inside a failure path must be
  **proven** unable to raise, ⛔ not documented as such.
- ⚠️ 4 existing tests updated for the right reason: `placed == []` would now pass
  a version that leaves the position **naked**. ⇒ two-sided property asserted.
- ⛔ **NOT shipped: F4 payload (MARKET → marketable LIMIT).** ⭐ Blocked on F3
  (`mis_autosquareoff` persists NOTHING + static tag). ⭐ This is **STOP A**, ⛔ not C.
  🔬 `test_fix181::test_inflight_orphan_flattened_when_kill_active` is STILL in
  the 10 — ⭐ correct: it expects LIMIT and F4 did not ship.
- ⏸ **Stale comments** naming 15:07/15:10 remain in `core/mis_squareoff_timing.py`
  (docstring invariant), `main.py:3292`, `alerts/mis_squareoff_notifier.py:32/35/183`,
  `config/system_config.yaml:52`. 🔬 Comment-only, ⛔ zero behaviour. ⏸ Owed.

## 03-Sep-2026 (Thu) NIGHT — 🟢 PUSHED `80091ce` · 🔴 PASS_2 IS THE FATAL STEP

- ✅ **C0 TREE `39292d3` → `2d08436`** 👤 on Rama's Option-1 line. ✅ **PUSHED
  `2d08436..80091ce`**; 🔬 PC=VM bare=deployed tree, **0** differing files; hook
  re-installed crontab. ⛔ MIS NOT enabled. ⭐ Engine inactive.
- 🔴 **PASS_2 IS THE FATAL STEP, ⛔ NOT PASS_1** — 🔬 02-Sep COALINDIA: PASS_1 failed
  ⇒ G5b recovered in **13 s** ⇒ closed externally ⇒ PASS_2 **FLAT** ⇒ ⛔ no incident.
  🔬 03-Sep ANANTRAJ: survived **2 m 59 s** to PASS_2, which cancelled the
  **recovery** SL ⇒ G5b blocked ⇒ CHECK9 ⇒ 8 rejections. ⇒ ⭐ Minimal intervention
  is **disable PASS_2**; ⛔ no config route exists ⇒ ⭐ code ⇒ sandbox.
- 🔴 **`mis_autosquareoff` PERSISTS NOTHING but DOES submit** (`:541`
  `_adapter.place_order`, tag `mis_autosq_*`; only store call is a READ `:500`).
  ⇒ ⭐ `PASS_2_EXIT_PROTOCOL="MARKET"` is **LIVE config**, ⛔ not dead. ⇒ 🔴 a
  submitted exit is **invisible** to the local store ⇒ CHECK9/G5b could place a
  **second sell**. ⇒ ⭐ **C6 ships ONLY with `mis_autosquareoff` persistence** —
  ⛔ C5 does not cover it (position still open while an unfilled exit rests).
- 🔬 **MIS is a near-certainty, ⛔ not a risk:** module shipped 28-Aug (~5 trading
  days); a position was open at a pass on **2**; **both failed**; 3/3, 0 exits.
  ⇒ ⭐ Enabling MIS = **scheduling a manual intervention** at **15:07-15:17**.
- ⛔ ⭐ Moving `entry_end` earlier would NOT help — 🔬 ANANTRAJ entered **10:01:33**.
- ⏸ **GUI closure: step 1 done** (🔬 pre-render 21:44:50 — MainPID **1119981**,
  start 13:08:20, NRestarts 0, `/controls` 302→/login unauth). ⏸ Awaiting 👤 Rama's
  click, then the post-render bracket read.

## 03-Sep-2026 (Thu) NIGHT — 🟢 T1 + T2 BUILT & COMMITTED · ⏸ PUSH PENDING

- 🔧 **Build tree = `D:/Projects/trading-system-gui09`**, branch
  **`fix/exit-path-t1-t2-03sep`** off `2d08436`. ⚠️ ⛔ NOT `D:/Projects/trading-system`
  (that is the 98-dirty `feat/delivery-config-split` tree — ⛔ never build there).
- 🚨 **TWO ENV TRAPS HIT AND HANDLED:** 🔬 inherited **`PYTHONPATH=D:\Projects\
  trading-system`** points at the dirty tree ⇒ ⭐ **every gate run uses
  `env -u PYTHONPATH`**, ⛔ or you get a false RED. 🔬 `data_store/instruments.csv`
  is **MISSING from every local tree** (`data_store/` is gitignored) ⇒ ⭐ absolute
  counts are meaningless locally; ⭐ compare **Δ against the same-env baseline**.
- 🔬 **BASELINE @ `2d08436`, env recorded:** Python **3.11.9**, cwd gui09,
  `PYTHONPATH` unset, `pytest tests/unit tests/integration -q` ⇒
  **10F / 6007P / 5S in 905.96s** — ⭐ matches the recorded fingerprint exactly.
- ✅ **T1 `cc2aeae`** — `MISSING_EXITS` gets its own alert body (no exit order /
  NOT managed to SL/TGT / manual flattening may be required). ⭐ New **branch**,
  ⛔ not a rewrite. 12 tests pass. ⭐ String + branch only, ⛔ zero execution effect.
- ✅ **T2 `80091ce`** — `_classify_broker_error`: TERMINAL / STATE_UNKNOWN /
  RETRYABLE, ⭐ allow-list **one entry**, ⭐ unrecognised stays RETRYABLE (pinned).
  ⭐ Blocks re-attempts + escalates once. 9 tests pass. ⭐ Fewer orders, louder alerts.
- 🔴 **WHY THE 8 RETRIES HAPPENED (code-level root cause):** 🔬 FIX-155's guard
  looks for an `orders` row with `order_type='MARKET'` — ⛔ a **rejected order
  persists no row**, so the guard could never fire.
- 🔴 **§5.1 SETTLED — ⛔ NO CONTRADICTION.** 📄 Zerodha: **CAS 3:12 · non-CAS 3:25
  · F&O 3:26**. ⇒ ⭐ config `15:12` = the **CAS** time, **correct**; ⭐ the 15:17 EOD
  pass beats **non-CAS 15:25** — ⭐ why 27/27 worked. ⚠️ 🔴 **NEW RISK: a CAS stock is
  broker-squared at 15:12, BEFORE the 15:17 pass** (₹50+GST), and 📄 ⛔ **no fresh
  MIS order can be placed after the cutoff** ⇒ the exit path is *closed*, not slow.
- ⛔ **KILLED:** 🔬 the 27 EOD orders are **21 SELL + 6 BUY** ⇒ ⭐ the BUY branch HAS
  run; 🔬 `marketable_limit_price` **does** invert per side; 🔬 history has **40 BUY
  SL / 38 BUY TGT / 39 filled SHORTs** ⇒ ⛔ the short side is **not** untested.
- ⚠️ 🔬 **A pre-existing RED test already asserts the fix:** `test_fix181::
  test_inflight_orphan_flattened_when_kill_active` expects `LIMIT`, gets `MARKET`.
  ⭐ In the baseline 10F; 🔬 proven pre-existing by stashing T2.
- ✅ **GATE CLEAN, Δ0 FAILURES.** 🔬 baseline `2d08436` **10F/6007P/5S** vs
  T1+T2 `80091ce` **10F/6021P/5S** — 🔬 **failure sets byte-identical** (`diff`
  empty) ⇒ ⭐ Δ = **+14 passed, 0 new failures** (= 5 T1 + 9 T2). ⚠️ `rc=1` reflects
  the **pre-existing 10**, ⛔ not a regression. 🔬 `push --dry-run` = clean FF
  `2d08436..80091ce`. 🔬 Diff is exactly **4 files** (2 source + 2 test).
- 🔴🚨 **§3.1 ANSWERED — CHECK9 IS PRODUCT-BLIND IN PRACTICE. ⛔ DISABLING MIS DOES
  NOT KEEP THE REPAIRED EXIT PATH OUT OF LIVE.**
  🔬 `order_reconciler.py:869` excludes trades via `get_active_gtt_states()`, which
  is `SELECT * FROM gtt_state WHERE status='ACTIVE'` — ⭐ i.e. **keyed on an ACTIVE
  GTT, ⛔ NOT on product**. 🔬 The live DB has **ZERO ACTIVE rows** (CLEANED 37,
  EXPIRED 1, TRIGGERED 4) ⇒ ⭐ `delivery_trade_ids` is **EMPTY** ⇒ ⛔ CHECK9
  currently excludes **nothing**. 🔬 And **72 of 109** historical CNC trades have
  **no `gtt_state` row at all**.
  ⚠️ 🔬 Worse: the read is wrapped in a bare `except` that sets `_delivery_rows=[]`
  ⇒ ⭐ a failed GTT read makes **every** delivery trade eligible.
  ⇒ 🔴 ⭐ **A CNC position without an ACTIVE GTT can be declared naked by CHECK9 and
  have the emergency exit fired at it.** ⇒ ⭐ C5 (human-race guard) is **not
  optional** — it is the only thing between the repaired payload and a live CNC
  position, which is exactly why 👤 FILE 130 orders C5 **before** C6.
  ⭐ Partial guard already present: 🔬 the naked-confirm re-reads `get_positions()`
  and returns False if flat. ⛔ Not a full pre-submit guard.
  ⛔ No `trades.product` column exists — ⛔ do not add one tonight.
- ⏸ 👤 **BLOCKED ON RAMA — ⛔ NOTHING PUSHED:** (1) the **TREE advance**
  `39292d3 → 2d08436` — 👤 FILE 129 §3.4 itself says *"needs one explicit line;
  ask, do not infer"*, ⭐ and it numbers TREE as **commit 0, before the push**;
  (2) the **GUI `/controls` closure** click (⛔ FILE 124 not in this session).
  ⭐ Push is ONE command once (1) is answered. ⛔ I did not reorder his sequence.

## 03-Sep-2026 (Thu) 🔴 **INCIDENT — NO WORKING FORCED EXIT** (TOP OF THE DEBT LEDGER)

- 💀 **ANANTRAJ naked position.** 🔬 MIS squareoff cancelled SL+TGT
  (`success=True` 15:07:04.5) then refused to exit on a **15 ms** confirmation
  poll ⇒ NAKED. Recovery SL placed 15:07:16; PASS_2 repeated it 15:10:03.
  🔬 Emergency fallback **REJECTED 8×**. 👤 Rama closed by hand 15:12:25.
  🔬 Exposure ≈ **11.5 s + 2 m 22 s**; loss **₹2.13** — ⭐ luck (trigger 620.08
  never hit), ⛔ not design. 📄 `docs/incident/2026-09-03_naked_position_ANANTRAJ.md`
- 🔴 **D1 — raw `order_type="MARKET"` is rejected by Zerodha, always.**
  🔬 `order_reconciler.py:~2996`. ⭐ The correct code (`marketable_limit_price` +
  LIMIT) sits **~680 lines above in the SAME file** (~2317). 🔬 Constraint known
  since the **10-Jul canary**; 🔬 this path also failed 01-Jul (tag length) ⇒
  **2nd production rejection, symptom-only fixes.** 🔬 `mis_autosquareoff.py:71/546`
  use MARKET for BOTH passes ⇒ ⭐ two independent reasons it could not auto-exit.
  ⇒ ⛔ **Every MARKET call site is UNPROVEN in live.**
- 🔴 **D2 — `_verify_cancelled` (`mis_autosquareoff.py:565-579`) polls ONCE, no
  retry.** 🔬 Orders read terminal **1.1 s later**. ⚠️ ⛔ **CORRECTION:** it DOES
  re-read the broker — ⭐ the defect is **TIMING**, ⛔ not source-of-truth.
  🔴 Cancels are sent BEFORE verification ⇒ a miss leaves protection destroyed.
- 🔴 **D4 (NEW, ⛔ not in FILE 125) — the trade row LIES.** 🔬 `exit_reason=MANUAL`
  + `status=CLOSED_MANUAL` but `closure_source=**OWN_SL**`, `exits_verified=1`.
  🔬 All 3 protective orders `CANCELLED`, `qty_filled=0` ⇒ ⛔ no SL ever filled.
  ⇒ ⭐ A post-trade review sees a normal SL exit and investigates nothing.
- ⭐ D3 — the `MISSING_EXITS` SOFT_KILL body says *"Intraday positions: managed to
  SL/TGT/EOD"* — ⛔ false by construction on that kill.
- 🔬 **Flat at broker CONFIRMED** (`0 positions` sustained to 16:31). 🔬 Schedule is
  CORRECT (cutoff 15:12 −5m/−2m; `entry_end` **15:00** since T5 29-Jun) ⇒ ⛔ the
  "15:15" in the record is STALE. 🔬 `trading-watchman` exited **cleanly**
  (status 0) ⇒ ⛔ NOT causally linked; ⚠️ but a market-hours monitor that exits at
  boot is a **separate** fault.
- ⏸ 👤 **RAMA'S CALL FOR FRIDAY:** (a) trade with MIS disabled, or (b) trade MIS
  knowing the manual flatten is the live safety net and watch 15:07-15:12.
  ⛔ Not VS Code's decision. ⛔ No fix overnight.
- ✅ **BROKER BOOK PULLED** (4 read-only GETs; token expired 04-Sep 05:00 ⇒ ⭐ last
  chance). 📄 `docs/incident/2026-09-03_ANANTRAJ_broker_book.json` `6b76425e…`
  - ✅ 🔬 `…7099` **CANCELLED at the exchange 15:10:03** ⇒ ⭐ naked was REAL,
    ⭐ CHECK9's detector **CORRECT**, ⛔ no 6th defect.
  - 🔴 🔬 Flattened by **`260903171167107` SELL MARKET COMPLETE 628.05 @15:12:11,
    `tag=None`** ⇒ 👤 Rama's manual close. ⇒ 🔴 ⭐ **A MARKET order FILLED from the
    UI** — Kite adds protection in the UI, ⛔ refuses it via API. ⭐ Exposure
    **≈2m20s** (ends at the FILL 15:12:11, ⛔ not the 15:12:25 observation).
  - 🔴 🔬 **MIS SQUAREOFF EXIT HAS NEVER EXECUTED** — all 27 EOD orders ever are
    26@15:17 + 1@10:00, **all LIMIT**; **0** in 15:07-15:12. ⭐ 3rd "built yet inert".
  - 🔴 🔬 **G5b never re-fired = SOURCE-OF-TRUTH SPLIT** (⛔ not SOFT_KILL): it is
    gated on the **LOCAL** `get_sl_order_for_trade()`, whose row stayed
    non-terminal until **15:17:04** ⇒ ⛔ G5b was never called. ⭐ System believed
    naked (broker) + protected (local) at once.
  - 🔬 SHAs: running code **IS `2d08436`** (Δ0); ⛔ TREE `39292d3` is NOT it ⇒
    ⭐ **the TREE advance is now a prerequisite of the exit-path fix.**
- 🔴 ⚠️ **I ALMOST FILED A VACUOUS SYSTEMIC FINDING.** 🔬 "74 of 74 OWN_SL with no
  SL fill" was **incapable of another answer** — `qty_filled>0` and
  `avg_fill_price>0` are **0 across all 1315 orders** (dead columns).
  🔬 Re-run on `status='COMPLETE'` ⇒ **1** (ANANTRAJ) ⇒ ⭐ **D4 is NARROW**;
  ⛔ the exit-attribution corpus is **NOT** contaminated.
- **D5:** 🔬 8 identical rejections / 111.4 s ⇒ ⛔ no retryable-vs-terminal
  classification. ⭐ Validation errors are permanent ⇒ escalate, ⛔ never loop.
- ✅ **ROUND 3 — MEASUREMENT CLOSED. ⭐ 3 of 👤 Rama's own hypotheses KILLED:**
  - ⛔ §4.1 neither the `rc_recovery_sl` tag nor `pending_quantity` — 🔬 the latter
    is in **0 files**; the row has the correct `trade_id`. ⭐ Real cause: **nothing
    polls a non-entry order between placement and a terminal-parent sweep**
    (row swept 15:17:04).
  - ⛔ §4.2 "four manual interventions" FALSE — 🔬 3 are **GTT_EXIT** (broker GTT
    engine places untagged orders) ⇒ ⛔ *"untagged ⇒ manual"* fails. ⭐ D4 NARROW.
  - 🔬 §4.3 `orders WHERE order_type='MARKET'` = **0 of 1315** ⇒ ⭐ the system has
    **never recorded placing** a MARKET order.
  - ⛔ §4.4 D6 is data-hygiene, ⛔ NOT live — 🔬 `trades.qty_filled` **335/844
    populated**; 🔬 **0 of 286 refs** read the dead `orders.*` columns.
  - 🔬 §4.5 **exactly 2 defect sites**: `mis_autosquareoff` (⛔ no
    `marketable_limit_price` import at all) + `order_reconciler` check9 (~3000).
    ⚠️ Residual: every converting site falls back to raw MARKET with no LTP ⇒
    ⭐ **"no quote" = "no exit", silently.**
- 🔴 **DOUBLE-SELL RISK:** 🔬 last emergency attempt 15:12:09 vs 👤 Rama's fill
  15:12:11 = **2 s**. ⇒ ⭐ **The exit was safe only because it was broken.** ⭐ Any
  fix MUST re-read the broker position immediately before submitting.
- 🟢 **ROUND 4 DESIGN WRITTEN** 📄 `docs/design/2026-09-03_exit_path_design.md`
  - 🔴 **A WORKING MIS BACKSTOP EXISTS:** 🔬 `OWN_EOD` = **27 closures, ALL MIS**,
    `leg='EOD'` orders **27/27 LIMIT + COMPLETE** ⇒ ⭐ the **15:17 eod_squareoff
    works because it uses LIMIT** — ⭐ the proven shape to copy. ⇒ ⭐ **Real exposure
    window = 15:07 → 15:17.** ⚠️ 🔬 4 MIS positions closed there via
    `EXTERNAL_UNATTRIBUTED` ⇒ ⛔ **broker-cutoff vs manual is NOT determinable.**
  - 🔴 **THE DB TELLS A FALSE STORY:** 🔬 rejected orders leave **no row**
    (`order_type='MARKET'` 0 of 1315 despite 8 attempts) ⇒ ⭐ the DB reports
    ANANTRAJ as a *clean verified SL exit*. ⇒ ⭐ **Persist rejected orders = commit
    1**; ⛔ without it no fix is provable.
  - ⭐ **O3 (👤 Rama's): `modify_order` the resting SL into the exit** — ⛔ both
    replacement orderings have a hole (zero protection vs 🔬 **3 resting sells on a
    qty-1 long**). 🔬 Kite DOES list `order_type` as modifiable ⇒ plausible; ⛔ but
    SL→LIMIT, the SELL-SL trigger rule and rate limits are **all UNSTATED** ⇒
    ⛔ needs a live drill, ⛔ not adoptable on docs.
  - ⚠️ **`order_monitor` = 5th "built yet inert"** (🔬 1 log line/day); ⭐ the design
    **routes around** it ⇒ ⛔ other local-state consumers stay stale. ⏸ Not fixed.
  - ⭐ Commit order: **0 TREE advance (prereq) → 1 rejected-order persistence →
    2 state contract → 3 G5b + STATE-UNKNOWN → 4 error classification →
    5 pre-submit broker re-read → 6 payload (O3 or shared LIMIT) → 7 hygiene.**
    🔴 ⛔ Never 6 before 5.

## 03-Sep-2026 (Thu) — 🟢 BOOT PROVEN ON `2d08436` · ⏸ TREE + RESTART OWED

- 🟢 **THE 08:15 BOOT HAPPENED AND IS CLEAN.** 🔬 `STARTUP` **ev 3814**
  `scenario=COLD` @ `08:15:41.796` — **after** `ExecMainStartTimestamp`
  `08:15:29` ⇒ ⭐ written live by THIS process. `NRestarts=0`, MainPID
  **1101999**. ⭐ Sequence 3801 → 3805 → 3808 → 3811 → **3814**.
- 🟢 **Token refresh SUCCEEDED** — `data_store/session/zerodha_token.json`
  written **08:15:02.051**, before the start. ⭐ The silent-failure item is GREEN.
- 🟢 **Startup checks OK, `warnings=[]`** — config 8 files, holidays 2026/15,
  NTP drift 0.002s, kiteconnect 5.1.0, disk 71.8 GB.
  ⭐ The single CRITICAL is the prior `SOFT_KILL` auto-clearing for the new day.
- 🔬 **The code that booted IS `2d08436`:** bare `refs/heads/main` = `2d08436`,
  ref last written **02-Sep 23:59:54** — ⭐ BEFORE the 08:15:29 start, so it
  cannot have moved under the boot — and the deployed work-tree differs from
  that tree by **0** tracked files.
- ⭐ ⇒ **TREE-ADVANCE `39292d3` → `2d08436` IS NOW ELIGIBLE.** ⏸ 👤 Rama's
  separate numbered reversible act. ⛔ NOT taken. ⛔ It proves nothing new
  about trading — 🔬 engine code is byte-identical to `39292d3`.
- 🔬 **Session healthy at 11:00:** 17197 INFO / 45 WARN / 2 ERROR / 1 CRITICAL.
  ⭐ The 2 ERRORs are ONE event — a **slippage rejection** (ANTELOPUS 10:00:30,
  ₹3.25 > ₹2.57 tol). ⭐ That is the guard refusing a bad fill, ⛔ not a defect.
  ⭐ Record it as **a red-capable guard that went red correctly** (👤 FILE 110).
- 🔴 **CORRECTION — ⛔ the GUI is NOT "serving old templates"; it is MIXED.**
  🔬 `/login` serves the **NEW** build (3 `2d08436`-only markers, with a
  positive control that could have failed). 🔬 Flask 3.1.3, `auto_reload=False`
  ⇒ Jinja caches at FIRST RENDER ⇒ ⛔ stale-vs-new is per-template and depends
  on browsing history. 🔬 But **29/29** backend `.py` postdate the process ⇒
  ⭐ all backend modules ARE pre-deploy. → [[gui_after_deploy_is_mixed_not_old_03sep]]
- ⚠️ **My own static-asset md5 check was VACUOUS** — `/static/*` is auth-gated
  and returned the 302 redirect body for both files. ⛔ Discarded, ⛔ not cited.
- ⏸ 🔴 **STEP B GATE NOT PASSED @ 11:21** — `gui-dashboard` is **still MainPID
  1019239 / Wed 06:19:53**, `NRestarts=0`. ⇒ ⭐ The restart (👤 step A) has NOT
  happened, so browser verification (C) + its record (D) are **VOID** and were
  ⛔ NOT attempted. ⭐ Engine untouched: `trading-system` still 1101999 @ 08:15:29.
- 🔴 **`services/controls.py` + `readers/control_client.py` are WHOLLY NEW
  files** — 🔬 ABSENT at `39292d3`, EXIST at `2d08436` (+496 lines, 0 deletions).
  ⇒ ⭐ The running GUI has **no such module** — ⛔ not stale, **missing**.
  ⭐ That is why 👤 FILE 110 puts **S17 first** after the restart.
- ⚠️ **A 2nd vacuous instrument, caught BEFORE citing.** 🔬 A `2d08436`-only
  route probe cannot work: `/api/controls-summary` (both), `/api/analytics/
  slippage` (new-only) and a route in **NEITHER** build **all return 401** —
  auth answers before routing. ⇒ ⛔ **No credential-free backend probe exists.**
  ⭐ The **PID + start-time check IS the instrument.** ⛔ Do not re-derive it.
- ⭐ **RULE ADOPTED (👤 FILE 110 §1): under `auto_reload=False` a rendered screen
  evidences the deployed tree ONLY IF the process started after the deploy.**
  ⇒ ⭐ Order: restart ⇒ confirm NEW PID ⇒ **then** browse. ⛔ A browse before the
  PID check looks identical to a silently-failed restart.
- 🔴 **THE Δ ASKED FOR IN 👤 FILE 111 §1 HAS NO COMPARAND.** 🔬 The **only**
  capture index on **any** branch is `docs/audit/approval_final_19aug/INDEX.md`
  (`be41d3c`, **19-Aug**): 22 screens, **1920 only**, 3 metrics (`h`/`OVF`/
  `<13px`) — ⛔ no 1440 column, ⛔ no clipped-cell column. ⚠️ The global table
  rule (`63a3946`+`0bbe127`) landed **02-Sep** and moves **33 headings** ⇒ ⭐ a
  drift vs 19-Aug is EXPECTED, ⛔ not a defect. ⚠️ `style.css:2017`'s "29 routes"
  is a **static CSS** audit, ⛔ NOT a rendered sweep.
  ⇒ ⭐ Report step C in **3 labelled tiers** — TRUE Δ (S14 `+9`/`+67` + S17/S16/
  S06/S07) · Δ-vs-stale (19-Aug 1920) · FIRST MEASUREMENT (all clipped-cell,
  1440 for the rest). ⛔ Never claim "Δ=0 everywhere".
  ⭐ The sweep BECOMES the missing baseline ⇒ ⭐ commit it (FILE 109 §1, one
  layer down: the acceptance NUMBERS, ⛔ not the procedure).
  → [[the_gui_delta_has_no_comparand_03sep]]
- 🔬 **§3 LOOKUP DONE — height drift EXPECTED on 7** (S11·S16·S17·S18·S19·S20·
  S21: the 15 freeze wraps, 🔬 `tbl-freeze`=0 at `be41d3c`); ⭐ **should HOLD on
  the other 15.** 🔴 ⭐ **S02 Dashboard is the CLEAN environmental probe** —
  🔬 `dashboard.html` **unchanged** `be41d3c..2d08436`, no freeze, only a
  `text-align` rule reaches it. ⇒ ⭐ **Predict `h=1212 · OVF=no · <13px=0`;
  any deviation is ENVIRONMENTAL.** ⭐ A prediction that can fail.
- ✅ **THE INSTRUMENT IS BUILT AND VALIDATED — ⏸ waiting only on the restart.**
  📄 `D:/Projects/trading-system-evidence/2026-09-03/gui_sweep_snippet.js`
  (sha256 `743a7d46…`, post-FILE-115) + `INSTRUMENT_VALIDATION` + `RUN_HEADER`
  + `SHA256SUMS` (all `-c` verified).
  ⭐ **ROUND 2 (👤 FILE 114) — 3 holes closed, each re-validated:**
  ⭐ **§1 scrollbar:** DEPLOYED-S02's `h=1212` > 1080 vp ⇒ a scrollbar is
  CERTAIN ⇒ it narrows `cw`, which REFLOWS and moves `h` — ⛔ and 19-Aug never
  recorded `cw`. ⭐ C1 now classifies: 🔬 T3 (sbar **0**) ⇒ `UNEXPLAINED`;
  🔬 T4 (sbar **23**) ⇒ `SCROLLBAR-PLAUSIBLE` + *"NOT RESOLVABLE"*. ⭐ Both halt;
  👤 Rama decides. ⛔ Never stop on `h` alone.
  ⭐ **§2 focus:** 🔬 T5 on a genuinely backgrounded tab ⇒ **3 rows `⛔UNFOCUSED`**
  + INTEGRITY; 🔬 T6 stubbed-focused ⇒ **0**. ⚠️ ⭐ Round-1 runs were THEMSELVES
  unfocused — ⭐ that is why they took 4 s/route. ⛔ An instruction to a human
  mid-run is ⛔ not a control.
  ⭐ **§3 binding:** one `RUN_HEADER` carries BOTH halves (VM PID + browser).
  ⚠️ 🔴 ⭐ The binding is MANUAL ⇒ ⭐ protection is SEQUENCE: **PID first, snippet
  second.** ⛔ A pre-restart run looks perfect and is void, undetectably.
  ⭐ It also records the 2 REJECTED probes so they are ⛔ not re-derived.
  ⚠️ ⭐ **SYNTHETIC-S02 (h=1080/916) ≠ DEPLOYED-S02 (h=1212)** — ⛔ never read the
  validation's numbers as production expectations.
  🔴 ⭐ **ROUND 3 (👤 FILE 115) — γ FOUND IN MY OWN GATE.** ⭐ Round 2 classified on
  *"is a scrollbar present?"* — ⚠️ but `h=1212` > 1080 vp ⇒ `sbar>0` **ALWAYS** ⇒
  ⛔ the strong branch was **algebraically unreachable for the only screen it was
  built for**. ⭐ T3 reached it only because the synthetic page FIT its viewport.
  ⭐ **FIX, ⛔ no threshold:** verdict now splits on **what moved** (height-only vs
  more-than-height, ⭐ reachable either way) and **prints magnitudes**:
  `Δh=804px · sbar=23px · ratio 35.0×`. 🔬 **G2 proves it: `MORE THAN THE HEIGHT
  MOVED` fires WITH sbar=23** ⇒ ⭐ branch reachable under the real screen's
  permanent condition.
  ⭐ **Scope:** `STOP_AFTER_C2` — 🔬 G3 stops after S17, G4 continues; both print
  `══ COMPLETE ANSWER REACHED (C2) ══`. ⭐ C0-C2 answers the deployment question
  in <1 min; ⛔ the rest is baseline-building. ⚠️ If stopped early the record says
  *"deployment verified at C2; Tiers 2/3 not measured"* — ⛔ never *"complete"*.
  🟢 **STEP B PASSED 03-Sep 13:08:55** — `gui-dashboard` **1119981** @ Thu
  **13:08:20**, NRestarts 0, serving (`/login` 200). ⭐ Engine UNTOUCHED
  (1101999 / 08:15:29 / 0). 🔬 `controls.py` mtime 02-Sep **23:39:55** vs start
  **13:08:20** ⇒ ⭐ **13h28m later** ⇒ the process holds the DEPLOYED modules and
  the Jinja cache is EMPTY. ⭐ Sequence honoured: PID first, snippet second.
  🔴 ⛔ **21 ROUTES ≠ 22 SCREENS.** 🔬 The instrument carries **21** (S02-S22);
  ⭐ S01 `/login` is excluded — it ⛔ does not render inside an authenticated
  session. ⭐ Campaign = 22 approved / 21 table-bearing; ⭐ 19-Aug baseline table =
  22 rows. ⇒ ⛔ **Never write "22 screens verified" from a 21-route sweep.**
  ⚠️ ⭐ **Scope via the CFG hook, ⛔ never by editing the file** — ⭐ an edit breaks
  the hash 👤 Rama was told to verify. ⭐ `window.__GUI_SWEEP_CFG =
  { STOP_AFTER_C2: true };` pasted FIRST, then the file unchanged.
  ⚠️ **Known, ⛔ unfixed:** that hook also overrides `ROUTES`/`S02_EXPECT`/
  `VIEWPORTS`, and the *"TEST CONFIG ACTIVE"* banner only fires on a voluntary
  `__present` ⇒ ⛔ a measurement-affecting override could run silently. ⭐ Fix in
  a future revision; ⛔ not changed mid-handover.
  🔴 ⛔ **The 23px is NOT a production scrollbar width** — ⭐ Round-1/2 numbers were
  taken UNFOCUSED, the very condition the new control rejects. ⭐ Conclusions
  (binary) stand; ⛔ their NUMBERS are not load-bearing.
  ⭐ 👤 Rama pastes it in his **authenticated** dashboard console ⇒ ⛔ NO credential
  moves anywhere. 🔬 Validated on a synthetic origin, Chrome 152:
  ⭐ SELFTEST fires all 3 detectors and goes quiet; ⭐ **the S02 gate HALTED on a
  wrong expectation (Δ h=-98919) and PASSED on the right one** — ⭐ both
  directions; ⭐ `/login.html` caught as **`auth=false ⛔LOGINPAGE`** ⇒ ⭐ the auth
  hole is CLOSED; 🔬 host **dpr 0.667** yet every row `cw=1920`/`1440` ⇒ ⭐ DPR
  trap defeated in practice. ⚠️ **Keep the tab FOCUSED** — background throttling
  ⇒ ~4 s/route (~3 min total). ⚠️ 2 bugs found and fixed by the test itself.
- 🔴 ⏸ **BLOCKER FOR C: the authed sweep is ⛔ NOT autonomous.** 🔬 username +
  password + **TOTP** (`pyotp`), 🔬 **5 failures ⇒ 15-min lockout** — ⛔ never
  guess, ⭐ it would lock 👤 Rama out mid-session. 🔬 `local_dev.auto_login` needs
  `OPS_DASHBOARD_LOCAL_DEV=1`; 🔬 the VM unit's `Environment=` is **empty by
  design** ⇒ ⛔ do NOT set it. ⭐ Cleanest: 👤 Rama hands over a **session
  cookie** after logging in once. ⭐ His call.
- ⏸ **Post-restart check order (👤 FILE 110 §3), to run when B passes:** S17
  first (new backend module) · a freeze-pane screen · a header-alignment screen
  · then **S14 — ⚠️ EXPECT the +67 overflow; ⭐ its presence is a PASS.**
  🔴 ⛔ **If S14 looks fixed, the check itself is wrong** — ⭐ it is the negative
  control for the whole verification. ⭐ Static assets: hard-refresh, authed.

## 02-Sep-2026 (Wed) — 🟢 GUI CAMPAIGN MERGED + PUSHED · ⏸ RESTART OWED

- 🟢 **PUSHED.** `origin/main` `39292d3` → `686df1c` (merge) → `7d4970a` → **`2d08436`** (record + TREE note). 🔬 Re-measured 03-Sep 00:3x after a power-cut: origin/main = VM bare = VM deployed tree (**0** differing tracked files, compared via a throwaway `GIT_INDEX_FILE`).
  🔬 origin/main = VM bare = VM deployed work-tree, three independent measurements.
  🔬 Both suites Δ0 with **identical failure SETS**: gate 10F/6007P/5S, GUI 1F/2171P.
  🔬 Outside `ops_dashboard/` + `docs/` the diff is only `PATHS.md` + `UNPUSHED_LEDGER.md`;
  across every engine path it is **EMPTY** ⇒ ⭐ byte-identical trading code at 08:15.
- ⏸ 👤 **RAMA OWES: `sudo systemctl restart gui-dashboard`.** 🔬 The hook has
  **zero** `systemctl` references (measured on the LIVE VM hook); the unit is still
  MainPID **1019239** from **06:19:53** with no file-watching ⇒ ⛔ serving OLD
  templates. ⛔ Until then the push looks like it did nothing.
  🔴 **SUPERSEDED 03-Sep: *"serving OLD templates"* is MEASURED FALSE** — the
  state is **MIXED**, and the real staleness is the **29 backend modules**.
  ⭐ The restart is still owed, for a sharper reason. ⭐ See the 03-Sep entry.
- ⏸ **Browser verification of the 21 refitted screens** — blocked on that restart.
  🔴 ⛔ **NO screen is `VERIFIED LIVE`**; every approval to date was a LOCAL render.
  ⭐ Acceptance wording once confirmed: *"22-screen GUI campaign complete; **21**
  table-bearing screens refitted and validated; integrated onto main; deployed;
  `gui-dashboard` restarted and verified."* ⛔ S01 is not a table screen.
- 🗿 **TREE STAYS `39292d3`.** ⛔ `2d08436` (the DEPLOYED tip) has never booted — ⭐ a push is
  ⛔ not a boot. TREE-eligible after the **03-Sep 08:15** boot, as a separate
  numbered reversible act. ⛔ Not tonight.
  🟢 **CONDITION MET 03-Sep 08:15** (ev 3814). ⭐ Now ELIGIBLE, ⏸ 👤 still owed.
- ⚠️ **DUE, one command, ⛔ not tonight: RENAME local `main`** in
  `D:/Projects/trading-system-main` (`3dff752`, 90 ahead / 94 behind) so a default
  `git push origin main` has nothing to resolve. ⛔ Do not delete the worktree —
  the 90 docs commits are unexamined. → [[stale_local_main_is_a_push_trap_02sep]]
- ⛔ **F2-CORE `587b306` STILL UNPUSHED** (`feat/f2-core-30aug`, on no remote).
  ⭐ Now recorded in the REPO ledger, not only in memory. ⚠️ RE-GATE on resume.
- ⛔ **Untouched and still owed:** S14 overflow · S08 sub-13px headers · S17's two
  truth defects · S05/S04 unbounded tables · R3/R4/R10 · the 36 left/center
  residuals (32 on non-campaign routes) · the `kiteconnect` isolation test.

## 30-Aug-2026 (Sun) — ⭐ 9 READY & HELD · ⛔ F2-CORE HELD (OPTION 2)

- 🏁✅🔝 **GUI TRACK: 🟢 **22 of 22 APPROVED, ⛔ 0 QUALIFIED, ⛔ 0 PENDING** (02-Sep).** 👤 S16 `b776cc8` · 👤 S06 sighting `92b927c` · 👤 S07 re-approval `7f6d999` — ⭐ the last two were **RENDER-ONLY**, 🔬 `git status`=0 either side. 📄 Entries 33-35
- ⏸📐🔝 **THE GLOBAL TABLE RULE IS NOW **DUE** — ⛔ no blocker left.** 📄 It was deferred *until all 22 are done*, and they are (02-Sep). ⚠️ ⭐ It touches EVERY screen ⇒ ⛔ not a render-only change; ⭐ it needs its own design → review → build pass.
- 🔴🖥️🔝 **S17 SAYS *"the config has no delivery variant"* OVER **Max Trades 10 / Max Positions 5** — 🔬 FALSE.** `max_open_delivery_positions: 3` and `max_daily_delivery_trades: 5` gate every delivery entry. ⏸ ⛔ UNTOUCHED (the S16 card forbade it). 📄 Entry 33
- ⚠️🖥️ **S17 rider — its `_limits` looked for a `delivery_` PREFIX; ⭐ those two keys use an INFIX.** ⛔ Its *Min Eligible Score* reads `v3_chain.min_pass_score`, 📄 a seed the config labels NON-GATING — same 60, ⛔ wrong source. 👤 Rama's call.
- 🔬⚖️🔝 **THE CONFIG SPLITS **NINE** PARAMETERS PER BOOK, ⛔ NOT THREE** — 🔬 measured 02-Sep from the ENFORCERS at `39292d3`. ⭐ `risk_engine.py:557-560`/`:655-660` **BRANCH on `bucket == "positional"`** ⇒ a delivery entry NEVER reads `max_open_positions`/`max_daily_trades`.
- ⛔⚖️ **NINE rider — the YAML holds EXACTLY 7 `delivery`-scoped keys** (+ capital split + leverage map = 9). ⛔ `max_consecutive_losses`, `min_pass_score`, `max_single_order_qty`, `price_drift_threshold` are GLOBAL — ⛔ never give them a Delivery column.
- 🖥️🔬🔝 **⛔ *"S10 is the FIRST drag application; 13 templates still owe it"* IS STALE.** 🔬 Measured at HEAD: **16 of 30** screen templates use `colDragMixin` (`static/components.js:95`) ⭐ and **all 16** iterate `cols` inside `<tbody>` ⇒ **16/16 genuinely move DATA**, ⛔ 0 header-only. ⭐ The 14 non-users appear to be screens with no reorderable table.
- 🖥️📍🔝 **gui09 = `feat/screen10-slippage-analytics` @ **`7f6d999`**, CLEAN, ⛔ UNPUSHED.** 🔬 **119 ahead** of `origin/main` `39292d3`. ⚠️ 🔴 **⛔ NO screen is `VERIFIED LIVE`** — every approval was a LOCAL review render; ⛔ none was ever seen on the VM. 📄 Entries 33-35
- ⚠️🧾🔝 **⛔ *"the CORRECTION is unchanged"* AND *"the FILE is unchanged"* ARE DIFFERENT CLAIMS.** 🔬 I wrote *"Build `b47e148` UNCHANGED"* for S06; the diff was **22 lines** — `efeb0b7` had refactored its DRAG, ⭐ the very thing the separator depends on. ⭐ **Check the FILE**, ⛔ never infer it from the commit that made the fix. 📄 Entry 34 rider
- ✅🖥️🔝 **THE gui09 REFIT IS STILL FREE — 🔬 RE-CONFIRMED 30-Aug: ZERO COLLISIONS.** 135 gui09 files vs 68 main files since merge-base `6fa8a1c` (14-Aug), **0 overlap**; 🔬 main touched `ops_dashboard/` in **0** files, gui09 in **87**. ⇒ ⭐ A rebase, ⛔ not a merge fight. ⚠️ It only grows more behind with every main push.

- ▶️🔴🔝 **THE 18:00 WINDOW PROCEDURE IS PERSISTED + PATCHED — [WINDOW_PROCEDURE_30-Aug-2026.md](WINDOW_PROCEDURE_30-Aug-2026.md)** (sha256 `82ab69c1df7907b4…`). ⭐ FILE 63 + FILE 64: `git -C $CAND` scoping, STEP 0 worktree pinning, absolute `--git-dir`, STEP 6 records, W-1…W-5. ⚠️ ⭐ Written because the 18:03 timer is **session-only** and mempalace is **down**.
- ⛔🚫🔝 **WITHDRAWN COMMANDS — ⛔ do NOT run these if an old card is re-read.** ⛔ FILE 58 §4 / FILE 59 §4·§6 **V-3** (`cd /home/ubuntu/systems/trading-system && git rev-parse HEAD`) — 🔬 that dir has **no `.git`**; it returns *"not a git repository"* and reads as a FAILED DEPLOY. ⭐ Use the bare/work-tree form. ⛔ FILE 58 **D-F** withdrawn. ⛔ `~/doc/SYSTEM_MAP.md` does not exist.

- ✅🔔🔝 **D-AA / Z-1 — ⛔ NO FALSE CRITICAL AT MON 16:05.** 🔬 At `39292d3` `daily_report` carries **BOTH** `monitored: false` **AND** `enabled: false`. ⭐ The 3-commit arc retired it AND un-monitored it together, so the officer never expects a heartbeat from it. ⚠️ ⭐ Standing rule anyway: **retiring a job and un-monitoring it are TWO SEPARATE ACTS** — ⛔ removing a cron line does not remove an expectation.
- ✅⏱️🔝 **D-AA / Z-2 — ⛔ THE PUSH RAISES NO "MISSING" ALERT TONIGHT.** 🔬 The officer's EOD runs **18:50 Mon–Fri** (`50 18 * * 1-5`) ⇒ ⛔ it does NOT run Sunday. `expected_heartbeat_jobs(..., before_time=now)` only expects a job once its time has passed. ⇒ ⭐ `output_retention` (02:10, `cadence: daily`, `critical: false`) runs **before** the first officer pass that expects it (Mon 18:50) ⇒ ⭐ classified COMPLETED.
- ✅🐍🔝 **D-AB / Z-3 — THE 02:10 LINE CAN EXECUTE; ⭐ proven by jobs already running.** 🔬 `/home/ubuntu/systems/venv/bin/python` exists (symlink → python3, **3.12.3**); 🔬 **31** live crontab lines use the **byte-identical** prologue+interpreter, incl. the 09:20 briefing that runs daily. ⇒ ⛔ No shape difference. ⭐ Rule: a new cron line's interpreter+prologue must match lines proven to run.
- ⚠️🐍🔝 **D-AB rider — the CONCRETE version delta behind W-1's caveat: 🔬 VM Python **3.12.3** vs PC **3.11.9**.** ⇒ ⭐ That is the only remaining theoretical source of a PC-vs-VM generator difference. ⛔ Do NOT close it by running the generator on the VM. ⭐ The hook's own output + post-push `crontab -l` are the decisive evidence.
- 🔴🧾🔝 **D-AC — A GROUPED COUNT IS NOT AN INVENTORY, ⭐ and it hid a gap through TWO review rounds.** 🔬 I first wrote *"10 weekly_patterns + **4** crash-test files + **12** dirs = 26"*; the truth is **10 + 5 + 11 = 26**. ⚠️ ⭐ **TWO COMPENSATING ERRORS cancelled to the correct total** — undercounted `crash_test` files by 1 (`full_report_2026-06-11.md` is a `.md`, not a "data file") and overcounted dirs by 1.
- ⭐🧾🔝 **D-AC rider — the literal porcelain is preserved** at `scratchpad/f2core/VM_PORCELAIN_LITERAL.txt`, sha256 `c0de46827b5e492099183640bd87bb8800b235c3be08f82d5308e6f65a2571c3` (35 lines = 1 tracked M + 34 untracked). ⇒ ⭐ **Preserve raw tool output whenever the SET matters, ⛔ not a summary of it.**
- ⚠️📜🔝 **D-AD — `logs/cron-output-retention.log` grows WITHOUT rotation** and is excluded from retention by its own `cron-*` never-touch name. ⭐ Small permanent accumulation; ⛔ not tonight's work. ⚠️ ⭐ Note the shape: **the reaper's own log is the one thing the reaper will never reap.**
- ⭐🏷️🔝 **W-4 WORDING — ⛔ do not generalise the Wednesday prediction.** ⭐ It applies to the **five REGULAR** one-per-trading-day families (`system_`, `debug_`, `trades_`, `reconciler_`, `daily_trade_review_report_`) reaching 8 vs keep-7 on **Wed 02-Sep**. ⚠️ ⭐ `alert_watcher_` is IRREGULAR (18/26/29-Aug) ⇒ ⭐ treat by its ACTUAL future rate. ⭐ `MAX_DELETE=25` is a CAP, ⛔ not evidence deletions stay small.
- ⭐🏷️🔝 **W-5 WORDING — ⛔ never write "the job is healthy".** ⭐ Write: *"application status is SUCCESS and exit code is 0 **despite** the 12 intentional REFUSED entries."* ⛔ An implementation status is ⛔ not a system-health claim. ⛔ **exit 0 ≠ healthy.**

- ✅🗑️🔝 **D-U — THE 02:10 JOB *DOES* DELETE: the generated cron line CARRIES `--apply`.** 🔬 Verbatim @`39292d3`: `… python scripts/output_retention.py --apply >> logs/cron-output-retention.log …`. ⭐ Cap **25**/run (`DEFAULT_MAX_DELETE`), `monitored: true`. ⇒ ⭐ *"the retention job goes live Monday"* is **TRUE**.
- ⭐📅🔝 **D-U rider — FIRST NON-ZERO DELETION IS ⭐ WED 02-Sep-2026 02:10**, ⛔ not Monday. 🔬 Rate MEASURED (⛔ not assumed): `system_/debug_/trades_/reconciler_/daily_trade_review_report_` each hold exactly the 6 latest trading days ⇒ **1/family/trading-day**. Mon 6→keep · Tue 7→keep · **Wed 8 ⇒ deletes the 21-Aug member.** ⚠️ `alert_watcher_` is IRREGULAR (18, 26, 29-Aug only).
- ✅🔔🔝 **D-U rider 2 — ⛔ THE 02:10 JOB WILL *NOT* PAGE NIGHTLY.** 🔬 The 12 refusals log at **WARNING** but ⛔ do NOT set status; `status` stays `SUCCESS` ⇒ 🔬 **exit code 0** (`return 0 if status == "SUCCESS" else 1`) and the heartbeat records SUCCESS. ⇒ ⭐ A healthy zero-delete first run is ⛔ NOT seen as a failure. ⭐ Only `>cap` or an exception sets FAILED/exit 1.
- ⭐🧾🔝 **D-Y — THE 34 UNTRACKED, LITERALLY: 2 config `.bak` + 5 docs + 26 `reports/*` + 1 `select` = 34 ✅.** 🔬 **11 collapsed DIRECTORIES** (⛔ not 12 as the card said): `reports/` × archive_prereconstruct · briefing · coach · crash_test/{resources,results,snapshots} · daily_review · flow_trace · integrity · log_review · watchman.
- 🔴🧾🔝 **D-Y rider — ⛔ NONE of the 34 sits inside `reports/output/` OR `logs/`.** 🔬 Measured. ⇒ ⭐ The retention scopes contain **ZERO** untracked entries, so the dirty tree and the reaper do ⛔ not interact at all.
- 🔴📄🔝 **D-Z — ⛔ CORRECTION TO MY OWN R-1.5: THE 15:20–15:30 F EVIDENCE COPY IS **NOT AUTOMATED**.** 🔬 No cron entry, no code path writes an "evidence" artifact — ⭐ it is a **manual Rama step**. ⇒ ⛔ *"it's a `system_*` file"* was an INFERENCE from the phrase "F evidence", ⛔ not a measurement. ⭐ Its family membership is whatever Rama names it.
- ⚠️📄🔝 **D-Z rider — what each naming choice costs.** ⭐ Outside `logs/`+`reports/output/` ⇒ ⭐ out of scope entirely (safest). ⭐ Inside `logs/` matching no family ⇒ **REFUSED** (safe, but a permanent nightly WARNING). ⭐ Inside `logs/` matching `system_*.log` **with** a date ⇒ joins the family as the NEWEST ⇒ kept. ⛔ Undated inside a family ⇒ REFUSED forever.
- ⚠️🔢🔝 **D-V — ⛔ LINE COUNT IS NOT EVIDENCE.** 🔬 Live crontab **148** lines; canonical **148**. The push ADDS the 02:10 line and REMOVES the 16:05 line ⇒ **148 → 148**. ⇒ ⛔ Never verify a crontab by count, by canonical md5, or by the hook's own claim. ⭐ Read the **named lines** out of `crontab -l`. ⭐ Generalise: ⛔ aggregate equality never proves set equality.
- ⚠️🗂️🔝 **D-W — ORPHANED FAMILY, permanent.** 🔬 The 6 retired `daily_report_2026-08-*.xlsx` match **no** family since `bee9755` dropped it ⇒ ⭐ REFUSED every run, forever, ⛔ never cleaned by any job. ⭐ A small bounded accumulation (6 files) — ⛔ recorded, ⛔ not a defect to fix.
- ⭐🏷️🔝 **W-1 WORDING — ⛔ never write "the generator is host-independent".** ⭐ Write: **structurally** host-independent *from the inspected source* (paths hardcoded `:42-44`; no hostname/locale/timestamp/`sorted()`), ⛔ **but PC-vs-VM byte equality was NOT directly measured** (running it on the VM is forbidden). ⭐ The decisive evidence is the hook's output + post-push `crontab -l`.
- ⭐🏷️🔝 **W-2 WORDING — ⛔ never write "the reaper cannot delete".** ⭐ Write: the **measured FIRST-RUN delete-set is zero**, and the implementation carries explicit scope+containment protections. ⚠️ ⭐ Future accumulation WILL produce a non-zero set; ⭐ the guarantee is **containment**, ⛔ not never-deleting.

- ⭐🖥️🔝 **D-P — THE DEPLOY MODEL, ⭐ measured once so it never costs another card.** Bare `/home/ubuntu/trading-system.git` + `--work-tree=/home/ubuntu/systems/trading-system`; ⛔ **the target has NO `.git`**; hook runs `checkout -f` as user **`ubuntu`** and installs **ubuntu's** crontab. ⇒ ⭐ EVERY VM SHA/status check uses `git --git-dir=… --work-tree=… …`.
- ✅🗑️🔝 **D-S — THE 02:10 RETENTION FIRST RUN DELETES **ZERO** FILES.** 🔬 Enumerated by running the REAL `build_plan` against the VM's actual 83 filenames: every family is at/under keep-7 (`daily_trade_review_report_*` 6 · `system_*` 6 · `debug_*` 6 · `trades_*` 6 · `reconciler_*` 6 · `alert_watcher_*` 3). ⭐ 12 files REFUSED (kept + logged): the 6 retired `daily_report_*.xlsx` + 6 undated `*.log`.
- ⭐🛡️🔝 **D-S rider — the reaper CANNOT escape its two roots.** 🔬 `SCOPES` = only `reports/output` + `logs`, explicit globs, `iterdir()` **non-recursive**, `_assert_inside()` realpath-asserts, symlinks refused. ⛔ Cannot reach `config/`, the repo, or evidence. ⭐ An undated file matching a family is **REFUSED**, ⛔ never deleted and ⛔ never takes a keep slot.
- ⭐📅 **D-S rider 2 — Monday's F evidence survives Tuesday's 02:10.** 🔬 `system_*` is 6 today; Monday adds 1 ⇒ 7 = keep ⇒ 0 deleted. ⭐ Even at 8 the OLDEST (21-Aug) goes, ⛔ never the newest. ⭐ Standing rule: **enumerate a deleting job's FIRST run before it runs unattended.**
- 🔴📁🔝 **D-Q — THE VM DEPLOY TREE IS DIRTY AND `checkout -f` DOES NOT CLEAN IT.** 🔬 1 tracked mod (byte-identical, `1cbf91a8…`) + **34 untracked** that ⛔ **ALL SURVIVE** the deploy. ⇒ ⛔ **`forced checkout` ≠ `clean deployed tree`** — ⛔ never write "the VM tree is clean" from a green V-3.
- ⚠️📁🔝 **D-Q rider — THE 2 CONFIG `.bak` FILES ARE INERT, ⭐ BUT ONLY BY ACCIDENT OF NAMING.** 🔬 3 sites glob `config/*.yaml` (`utils/startup_checks.py:1477` ⚠️ **runs at 08:15 boot** · `scripts/preflight/checks/config_integrity.py:85` · `system_manager.py:509`). ⭐ `…yaml.bak.2026…` does ⛔ NOT match `*.yaml`. 🔴 **`system_config.bak.yaml` WOULD.** ⇒ ⛔ **never name a backup so it ends in `.yaml`.**
- ✅⏰🔝 **D-R — THE CRON INSTALL IS CONDITIONAL, ⭐ and the condition is host-independent.** 🔬 `generate_crontab.py` hardcodes `PROJ`/`VENV_PY` as **absolute constants** (`:42-44`) — ⛔ NOT derived from `_ROOT` — so PC and VM emit identical bytes. ⭐ Success string: `post-receive: crontab AUTO-INSTALLED from canonical.` ⛔ Failure: `post-receive: WARNING canonical != generate(registry) … crontab NOT installed.`
- ⭐🔬🔝 **S-3 — ⛔ A CARD'S CONCRETE COMMAND AGAINST AN UNMEASURED TARGET IS A QUESTION, ⛔ NOT AN INSTRUCTION.** 🔬 Twice in two cards: D-F asserted a `PATHS.md` defect never read; V-3 assumed a `.git` that does not exist and would have read as a FAILED DEPLOY at the window. ⇒ ⭐ **Measure the target, then correct the command.** ⛔ A card never outranks a measurement.
- ⭐🏷️🔝 **A-2 WORDING RULE — ⛔ NEVER WRITE "all pre-checks passed" OR "N-1 passed".** 🔬 N-1 FOUND A DIRTY TREE; only the narrower safety question passed. ⇒ ⭐ Always write **what passed AND what was found**, side by side. ⛔ A green V-3 must never be allowed to erase the N-1 finding.
- 🔴🔌🔝 **D-M — mempalace RETRY DONE 30-Aug ~11:50: ⛔ STILL `CONNECTION_CLOSED`.** 🔬 No `mempalace` tool resolves. ⇒ ⭐ **The whole 30-Aug set (D-A…D-T, S-1, S-2, S-3) lives ONLY in these files.** ⏸ Replication to mempalace is **OWED** and must be carried to the TOP of the next session. ⛔ Never let an outage silently swallow a day's findings.

- 🔴🖥️🔝 **D-I — THE VM WORKING TREE IS DIRTY, AND `checkout -f` SILENTLY DISCARDS IT.** 🔬 `M config/system_config.yaml` (the 29-Aug out-of-band email edit) + **34 untracked**. ⭐ The hook runs `git --work-tree=… checkout -f` ⇒ ⛔ tracked edits are overwritten with NO warning. ⛔ **No VM-side edits — every change reaches the VM through the bare repo.**
- ✅🔬 **D-I rider — the 29-Aug edit is SAFE to overwrite, 🔬 re-measured 30-Aug (⛔ not trusted from the ledger).** md5 of the VM's live `system_config.yaml` = md5 of the `39292d3` blob = **`1cbf91a8afbe1e9de8251e21b5b759f8`** ⇒ ⭐ `checkout -f` is a genuine **no-op** for that file.
- 🔴🛠️🔝 **⛔ `V-3` AS WRITTEN IN FILE 58/59 IS NOT MEASURABLE.** 🔬 `/home/ubuntu/systems/trading-system` has **NO `.git`** — it is a `--work-tree` deploy, so `cd $D && git rev-parse HEAD` returns *"not a git repository"*.
- 🔴🔬🔝 **⛔ AND THAT "CORRECT FORM" WAS STILL NOT A CONTENT CHECK.** 🔬 03-Sep: `--work-tree=<EMPTY dir> rev-parse HEAD` printed `2d08436` — `rev-parse` reads the ref from `--git-dir` ⇒ ⛔ V-2 and V-3 were ONE measurement. ⭐ **REPLACEMENT:** `read-tree HEAD` into `GIT_INDEX_FILE=$(mktemp)`, then `status --porcelain -uno | wc -l` ⇒ **0**. 🔬 Self-tested: 0 real, **1427** empty.
- ✅⏰🔝 **D-J ANSWERED — THE CRONTAB *IS* REPO-DRIVEN, INSTALLED BY THE POST-RECEIVE HOOK ITSELF.** ⭐ It installs `deploy/cron/trading-system.cron`, ⛔ but ONLY if that file matches `scripts/generate_crontab.py --generate`; otherwise it prints a WARNING and installs **NOTHING**. 🔬 Verified identical at `39292d3` (md5 `4a3e46cc717c77e0209267b7832d0cc0`).
- ⚠️🪟🔝 **D-J rider — ⛔ NEVER RUN THAT COMPARISON ON WINDOWS WITHOUT NORMALISING.** 🔬 `generate_crontab.py` emits **CRLF** on Windows ⇒ `diff` reports **all 148 lines changed** and looks like "the hook will refuse". ⭐ The committed blob has **0 CR bytes**; ⭐ compare with `tr -d '
'` or against `git show`. ⚠️ A near-miss false finding.
- ✅⏰🔝 **Monday's crontab, 🔬 measured both sides.** BEFORE (live now): **0** `output_retention` lines · `daily_report` **still at 16:05**. AFTER the push: 02:10 `output_retention` line **PRESENT** ⇒ arms · the `daily_report` 16:05 **LINE IS GONE** from canonical ⇒ ⭐ the line DISAPPEARS (⛔ it does not linger and self-disable) · `daily_trade_review` stays 16:07.
- ⚠️📧🔝 **D-N/N-3 — ⛔ NO LOG EVIDENCE OF ANY SEND TO THE NEW ADDRESS.** 🔬 `pythonsystemalerts` hits in logs = **0**; `ramakrishnan031` = **0**; no send/failure markers. ⭐ **The logs do not record recipients AT ALL**, so silence is uninformative in BOTH directions — ⛔ it is neither confirmation nor refutation. 👤 The only evidence is Rama's 29-Aug inbox confirmation.
- ⭐🏷️🔝 **D-O — WORDING, ADOPTED: ⛔ never write "F2-CORE is gate-clean".** ⭐ Write: **regression-gate clean** against the 30-Aug baseline; ⛔ **architectural acceptance INCOMPLETE** (criterion 7 partial). ⭐ Three states named separately from now on: **regression-clean** · **architecturally accepted** · **authorised for release**. ⭐ F2-CORE is the 1st, ⛔ not the 2nd, ⛔ therefore not the 3rd.
- ⚠️🤖 **D-N — G1 PATTERN STRENGTH: 9 recorded auto-filled-prompt occurrences, 2 of which IMPERSONATED Rama's ruling.** ⭐ Count it as evidence for the standing rule: ⛔ **no quote = no authority.** ⭐ A fired timer is a CLOCK, ⛔ never an authority.

- ✅🚀🔝 **PUSHED 30-Aug ~19:5x — `origin/main` `effff24` → `39292d3` (the 9).** 👤 Rama's 11:24 PUSH-AUTH (`PUSH_AUTH.txt` `bfae638f…`); gate `85826ac6…`, record `9faa7858…`. 🔬 V-1..V-4 all `39292d3` **incl. the DEPLOYED TREE**; V-5 F2-CORE ⛔ not an ancestor; V-6 `587b306` intact, 0 remote refs. ⛔ **SERVICE NOT STARTED.** 🔴 **Mon 08:15 = first run.**
- 🔴🧠🔝 **mempalace STILL DOWN — RETRIED ONCE AT SESSION END 30-Aug, still unreachable** (tools not exposed; `CONNECTION_CLOSED` all session). ⇒ ⭐ **The WHOLE 30-Aug record is SINGLE-COPY in these files.** ⛔ Never invent a replacement mechanism. ⭐ Carry the outage **and the full owed replication set** to the TOP of the next session.
- ⚠️🧾🔝 **MASTER_REGISTER — a PATH/ROOT MISMATCH, ⛔ NOT a missing file.** 🔬 Absent from **every branch in the project graph**. 👤 Rama: it lives at `D:/Projects/trading-system-main/docs/` — **outside that tree**, in a clone **85 behind** `effff24`. ⛔ Not interchangeable. ⚠️ Its 231 items were compiled there ⇒ CONTENTS may be stale. ⛔ Nothing done tonight.
- ✅🗑️🔝 **X-2 RE-MEASURED 20:4x — the 02:10 first-run delete-set is STILL 0** (dry-run; every family under KEEP=7). 🔬 The 35th untracked entry = **`reports/weekly_patterns/patterns_2026-08-30.md`** @18:00:19, written by cron `gemini_weekly_patterns [0 18 * * 0]` — ⛔ **NOT in scope**. ⚠️ 12 files *refused: no family*, incl. 6 `daily_report_*.xlsx` ⇒ orphaned from retention. ⛔ Not chased.
- ⏸📄🔝 **OWED (deferred by the procedure itself): `docs/SYSTEM_MAP.md` + `PATHS.md` corrections for the MAIN lineage** — ⛔ still not written; the S11/S12/S13 blocks went to the **gui09** branch only. ⭐ Carry to the next commit window.
- ✅⏰🔝 **HOOK = INSTALL, and V-9 PROVES IT TOOK.** 🔬 *`post-receive: crontab AUTO-INSTALLED from canonical.`* ⇒ `output_retention` **02:10 PRESENT, `--apply` visible** · `daily_report` **ABSENT** · `daily_trade_review` **16:07 unchanged**. ⚠️ **148-TRAP: 148 → 148** ⇒ ⛔ the count proves NOTHING; the greps do. 📄 `PUSH_COMPLETION…txt` `1b85a396…`
- ⚠️🗑️🔝 **V-10 — THE VM TREE IS DIRTY AND STAYS DIRTY.** 🔬 MEASURED **35** untracked, ⛔ **not the recorded 34** (most likely today's `patterns_2026-08-30.md`); ⛔ reported, ⛔ NOT cleaned. 🔬 **0 modified / 0 deleted TRACKED** ⇒ the deploy overwrote tracked content cleanly and the dirt is untracked-only, surviving `checkout -f`. ⛔ **A green V-3 does NOT make this tree clean** (W-3) — both stand together.
- 🗿🔴🔝 **F2-CORE IS BUILT, GATE-CLEAN, AND ⛔ HELD UNPUSHED at `587b306` on `feat/f2-core-30aug`** (7 commits + its ledger commit, 17 ahead of `effff24`). 👤 **OPTION 2 ruling:** ⛔ six of seven criteria ⇒ ⛔ not done ⇒ ⛔ does not ship. ⛔ Do NOT delete/squash/rebase that branch.
- ⚠️🧪🔝 **⛔ F2-CORE'S GATE RESULT DOES NOT SURVIVE A SHA CHANGE.** 🔬 Clean vs the 30-Aug baseline (fingerprint `46c38a3e…`, 10F/6029P/5S). ⭐ Whenever it is resumed — rebase, refit or new base — ⭐ **RE-GATE from a fresh baseline.** ⛔ Never quote today's numbers for tomorrow's tree.
- 🔴🧾🔝 **⛔ ENTRY 22 EXISTS ONLY ON THE HELD BRANCH.** 🔬 `grep 'Entry 22' UNPUSHED_LEDGER.md` = **0** on `39292d3`, **1** on `587b306`. ⇒ ⭐ a session reading the ledger from pushed main will ⛔ NOT see the 7 held commits. ⭐ **That is why the held-unit facts are duplicated HERE.**
- 🔴🛑🔝 **D-A — CRITERION 7 / CHANNEL 4 UNPROVEN: a daily-loss breach is a GLOBAL stop.** `_make_daily_loss_cb` → `EodSquareoff.fire_now()` (closes **ALL** positions) → global `soft_kill`; `KillSwitch.is_active(intent)` is scoped by INTENT, ⛔ never by pipeline. ⛔ Needs `kill_switch.py` + EOD ⇒ own design + fresh gate.
- ⛔🛑🔝 **D-A rider: ⛔ UNTIL IT LANDS, NO artifact, alert, doc or commit may claim the two books are independent.** ⭐ Design it WITH the standing SOFT_KILL defect (scheduled 15:15 breaker kills vs emergency kills not distinguished; `clear_stale_state()` clears only previous-day kills) — ⭐ same kill path, or fix 2 reopens fix 1.
- 🔴📊🔝 **D-B — `SECTOR_EXPOSURE` IS STILL CROSS-PIPELINE, and it is a MAIN-LINE finding (⛔ it does not go away because F2-CORE is held).** 🔬 The limit pct is per-book but `state_store.sector_exposure()` sums ALL products and the base is `pct × snap.total`. ⭐ Inert ONLY because `sector_cap_mode: observe` ⇒ ⛔ **`observe → enforce` IS BLOCKED until scoped per book.**
- ⚠️🧪🔝 **D-C — THE GATE INSTRUMENT IS NOT FULLY DETERMINISTIC.** 🔬 `test_signal_processor.py::test_b5_no_shadow_tracker_wired_proceeds` went 4F/421P → 5F/420P → 4F/421P across identical re-runs. Repro: the 6-file subset (risk_engine, fund_manager, state_store, config_loader, signal_processor, main). ⛔ Polluting test NOT identified.
- ⚠️↩️ **D-D — ROLLBACK TREE `52ccb4f` is now far behind what the VM will boot.** ⛔ NOT advanced today. ⭐ Re-prove it after Monday's boot evidence lands. ⛔ A push is not a boot.
- 🔴🗺️🔝 **D-E/D-F CORRECTED BY MEASUREMENT — ⛔ the card's premise was FALSE.** 🔬 `PATHS.md:242` records `| Local repo | D:/Projects/trading-system |`; the string `trading-system-main` appears in **0** lines of PATHS.md and SYSTEM_MAP.md. ⛔ So PATHS.md does NOT record a stale main. ⭐ The real defect is below.
- 🔴📍🔝 **⛔ `D:/Projects/trading-system` (what PATHS.md calls "Local repo") IS NOT THE WORKING LINE** — 🔬 it is `feat/delivery-config-split` @ `6d24a83` with **98 dirty files** (the F2-SIZING tree). ⛔ NEVER build or gate there. ⭐ Read-only via `git show`. ⏸ PATHS.md correction OWED (frozen tree tonight).
- ⚠️📍 **⛔ `D:/Projects/trading-system-main` IS A STALE DIVERGENT `main`** — 🔬 `3dff752`, **90 ahead / 85 behind** `effff24`. ⭐ A trap by OMISSION: it is recorded nowhere, so a session that finds it assumes it is main. ⛔ It is not.
- ⭐📍🔝 **THE ACTUAL WORKING LINE 30-Aug** = the `mis-work` worktree (`fix/mis-autosquareoff-28aug`) under a *prior session's* scratchpad, plus `f2core-work` (`feat/f2-core-30aug`) under this one. ⚠️ ⛔ Scratchpad worktrees are session-scoped — ⭐ resolve with `git worktree list`, ⛔ never from a remembered path.
- ⏸🗂️🔝 **D-G — carried forward, named and UNTOUCHED:** F2-SIZING (⚠️ ~7× on the only binding rung, 708/708 concentration) · the `intraday_max_*` rename · **OPEN-1** (`one_trade_per_symbol_direction_per_day`) · `config_auditor`'s G1 is intraday-only and ⛔ does not audit `delivery_entry_end`.
- 🔴🌙 **D-H — F6 REMAINS UNFIXED** (`cnc_gtt_monitor.py:482`, `abs(int(qty))`). ⇒ ⭐ The standing obligation continues: 👤 **Rama stops the service every trading night, ⛔ or there is no 08:15 boot next morning.**
- ⚠️🔌 **`mempalace` MCP SERVER FAILED TO CONNECT this session (CONNECTION_CLOSED).** ⛔ Not "unconfigured" — a connection failure. ⇒ ⭐ every §7 memory update landed in THESE files instead. ⏸ Replicate to mempalace when it is back.
- ⚠️📄 **FILE 58 named `~/doc/SYSTEM_MAP.md`; 🔬 that path DOES NOT EXIST.** ⭐ The file is `docs/SYSTEM_MAP.md` **inside the repo** (663 KB). ⛔ Do not create the phantom path.

## 27-Aug-2026 — ✅ FILE 14: D-1…D-9 TAKEN · V-1…V-4 MEASURED · BUILD GATED TO 17:45

- 🖥️✅🔝 **GUI TRACK: ALL 22 SCREENS BUILT.** ⚠️ ⛔ **SUPERSEDED — the live count is the GUI TRACK line at the top of this board.** ⛔ PUSHED = NO, DEPLOYED = NO.
- 🔧✅🔝 **COLUMN REORDER IS NOW ONE IMPLEMENTATION (`efeb0b7`): 29 copies → 1.** `colDragMixin()` in `static/components.js` (drag + `initCols`/`saveCols`/`resetCols`). ⭐ `Object.assign` puts page members LAST, so the 15 existing screens keep their own overrides and are unchanged.
- ⚠️🖥️ **DRAG RULE IS ONLY PARTLY APPLIED — S10 is the FIRST application; 13 templates still owe it.** ⚠️ Wiring is not enough: a table with POSITIONAL `<td>`s moves the LABEL and leaves the DATA — both `<thead>` and `<tbody>` must iterate the same live `cols`.
- 🔴📏 **⛔ NEITHER S09 NOR S10 IS "VERIFIED LIVE".** S09 approved on **seeded demo** data, S10 on a **stale REAL VM snapshot**. ⭐ Composition/alignment confirmed; ⛔ populated PRODUCTION behaviour is not.
- ⚠️🚦 **S10's amber/red slippage status path is LIVE BUT NEVER EXERCISED** — 🔬 real slippage is ~₹0.00–0.02, **100% within limit**, 0 near, 0 exceeded.
- 🎨✅ **S09 APPROVED 27-Aug ~21:5x (supersedes 24-Aug).** 🔧 `292a750` rebuilt both heatmaps as the artwork's **two-row matrix** (`Net P&L (₹)` label, uncoloured label row, one coloured value row, tint on the VALUE cell only); `ade92cc` records it.
- ⚠️🧪🔝 **🔴 THE S09 APPROVAL RESTS ON DEMO DATA, ⛔ NOT PRODUCTION.** 🔬 The local `data_store/trading_system.db` holds **0 closed trades** (last written 03-Aug), so the render used **75 seeded demo trades**. ⭐ Composition/colour/alignment are confirmed; ⛔ the populated PRODUCTION appearance is **NOT** confirmed. ⛔ Do not upgrade this to "verified live".
- ✅🧹 **DEMO-DB HYGIENE HELD:** 🔬 the `gui_config.local.yaml` pointer was reverted **byte-identically** (that file forbids leaving one), the demo DB lives **outside the repo**, and the real DB's mtime is **unchanged at 03-Aug 16:08** ⇒ never opened for writing.
- 🔧✅ **THE gui09 "REFIT" IS ESSENTIALLY FREE — 🔬 ZERO COLLISIONS, WHOLE TREE.** 83 ahead / 37 behind `52ccb4f`, merge-base `6fa8a1c` (14-Aug); 132 gui09 files vs 65 main files, **0 overlap**. ⚠️ Not FF-able only because it is behind ⇒ a rebase, ⛔ not a merge fight.
- ⚠️📍 **CORRECTION:** the F2-era note *"19 of main's commits touch ops_dashboard"* is dated **07→14-Aug**, BEFORE gui09's merge-base ⇒ already in its base. 🔬 main touched `ops_dashboard/` in **0** of the 37 commits since. ⛔ Not refit cost for gui09.

- 🗺️✅🔝 **F2 — DECIDED (D-3/D-4). ⛔ NO LONGER AWAITING RAMA.** **F2-CORE SHIPS** via **OPTION B** (reimplement vs current main); ⏸ **F2-SIZING DEFERRED** (allocation model, cap rewrite, `risk_per_trade` inert). ↩️ SIZING is QUEUED, ⛔ not discarded. 📄 `FILE14_DECISIONS_AND_V1-V4_27-Aug-2026.md`
  - 🔬 **V-2/V-3 collapsed the surface: 19 code/config collisions → 7 for F2-CORE** + new `pipeline_policy.py` (0 collisions). ✅ ⛔ NO schema v46 (SIZING owns all `+28/−5`; RENAME's touch is ONE comment). ✅ ⛔ NO `intraday_max_*` rename (PIPE refs it in **0** production files).
  - ⚠️ **⛔ RISK IS NOT ZERO — prediction FAILED on that clause:** the 7 CORE files still carry **19 main commits, +957/−100** (`main.py` 5 · `state_store` 4 · `risk_engine` 3 · `config_loader` 3). ✅ But `position_sizer.py` (5) + `config_auditor.py` (4) + `db_reader.py` (11) DROP OUT.
- 💸✅🔝 **K-1 — CLOSED COMPLETELY (D-5 + V-4). ⛔ NOT a defect.** 🔬 `binding_constraint` = `concentration` on **708/708** trades; `capital` binds on **0**; **0** rows where `qty_by_capital ≤ qty_by_concentration`; **min margin 1.75×**, mean **37×**. ⇒ ₹6.07/day (0.057%) cannot have changed any size. ⭐ Deducting at close is CONSERVATIVE AND CORRECT.
- 🧮✅ **NI-16 — BLOCKED → QUEUED.** 🔬 The branch resolves it structurally: `position_sizer.py:574` `min(1.0, effective_mult_unclamped)` inside the allocation; main has no clamp and no allocation. ⛔ NOT built.
- 🚦✅ **E-7 — D-1 TAKEN 27-Aug ~11:00: the ROLLBACK TREE IS NOW `bc9a9f5`** (was `75e637c`), on E-3's boot proof. ↩️ Reversible in one line. 🔴 ⛔ Do NOT advance it again to tonight's push SHA — a push is not a boot; the 28-Aug 08:15 boot is.
- 📄✅ **D-9 TAKEN — the TWO operative audit files SHIP tonight:** `RUNBOOK_n907_install_20-Aug-2026.md` + `OPS2_HANDOVER_RAMA_23-Aug-2026.md`. ⛔ The other 61 stay off — dated records, HISTORICAL by construction.
- 🔨✅🔝 **UNIT 1 METHOD DECIDED BY V-1 = EXTRACT `c39e799`, ⛔ NOT a fresh build.** 🔬 It already contains the F6-leg fix, and main moved only **+3/−1** in `cnc_gtt_monitor.py`. ⚠️ Its T+1 arm stays **NOT EXERCISED** until a real carry — ⛔ do not claim it.
- 🛑🐛🔝 **⛔ THE OBVIOUS F6-leg FIX IS WRONG — DO NOT "JUST DELETE THE `abs()`".** 🔬 Correct is `held[sym] += max(0, int(qty))`, ⛔ NOT the signed sum: `c39e799` says *"Deleting abs() does not fix it either: the signed sum gives -1"*, which also fails the `held == 0` door to `_finalize_gtt_exit`.
- ⚠️📋 **⛔ EXTRACTION IS NOT ONE FILE:** `c39e799` is **8 files, +1,864/−21** — `cnc_gtt_monitor.py` +326, `state_store.py` +118, `fund_manager.py` +44, `order_reconciler.py` +9, plus 3 test files. 🔬 Only the monitor's change was traced end-to-end; the other 7 are UNTRACED.
- ⚡✅🔝 **UNIT 3 (leverage) COLLAPSES TO VALIDATION-ONLY — 👤 Rama's ask is ALREADY IMPLEMENTED.** ⛔ U3-a NO-OP (`DELIVERY: 1.0` exists) · ⛔ U3-b NO-OP (one intent-generic multiply already covers it). ✅ **U3-d is the entire value**: bounds + all 4 intents + CRITICAL/exit 5. 📄 `FILE15_L1-L5_LEVERAGE_27-Aug-2026.md`
- ⚖️⏸ **👤 RAMA TO CONFIRM — the U3-d leverage ceiling: propose `1.0 ≤ lev ≤ 10.0`.** ⭐ `10.0` is **not invented**: it is the bound G2 already uses (`config_auditor.py:697 if value > 10`), so it adds no new number and clears `COVER_ORDER: 6.0`. ⛔ NOT adopted silently.
- 🐛❓ **LATENT LEVERAGE GAP ① (⛔ unreachable today, ⛔ not fixed):** `fund_manager.py:312-318` substitutes a **hardcoded duplicate** of the config map when `leverage_map is None` ⇒ silent drift the day config changes.
- 🐛❓ **LATENT LEVERAGE GAP ②:** `position_sizer.py:183` ⛔ does NOT validate map completeness (FundManager `:319-322` does) ⇒ `.get(intent, 1.0)` would size an unknown intent at **1×** instead of failing.
- 🧊🔒🔝 **U3 PREDICTION FROZEN 27-Aug ~11:4x, BEFORE ANY CODE.** ⭐ With the current map ALL SEVEN hold (values · intent→value · inputs · **calculated capital/margin** · downstream sizing · persisted audit · Live=Paper); ⇒ **ONLY an invalid config produces a new outcome: BOOT FAILURE.** 📄 `FILE16_UNIT3_SCOPE_FROZEN_27-Aug-2026.md`
- ⚖️⏸ **👤 RAMA — OPEN: the ABSOLUTE code bound `leverage_safety.max_allowed` may never exceed.** ⏸ Until set, the two-block structure is **DEFERRED**; a hardcoded `1.0 ≤ lev ≤ 10.0` applies ⇒ ⚠️ a future 12× WOULD need code.
- ⚠️🧪 **U3-c IS NOT A 6-LINE DELETION — ≥8 TEST FILES NEED EDITS IN THE SAME COMMIT.**
  - 🔬 The **6** that build the REAL `FundManager` with no `leverage_map`: `test_double_release` · `test_fund_manager_edges` · `test_gate8_sector_toctou` · `test_h7_strategy_cap_toctou` · `test_phase19_batch2`×5 · `test_order_reconciler:2106`.
- 🐛🔴 **FINDING — `"POSITIONAL"` IS NOT A VALID INTENT** yet sits in 2 test leverage maps (`test_fix133_dynamic_sizing:36` · `test_mc6_zero_multiplier_skip:46`). ⭐ Invisible because `.get(intent, 1.0)` absorbs it — **Direction 3 in the wild.**
- 📏✅🔝 **U3 NEUTRALITY BASELINE MEASURED 27-Aug ~11:5x — `implied_lev = qty_planned × entry_target_price / margin_reserved`.** 🔬 **MIS: 495 rows, min=max=5.0000. CNC: 79 rows, min=max=1.0000.** Zero variance ⇒ the configured map IS what production applied. ⭐ Post-U3 acceptance = **EQUALITY**; any row off 5.0/1.0 is RED. 📄 `FILE17_..._27-Aug-2026.md`
- ⚠️🕑 **⛔ RE-CAPTURE THAT BASELINE AFTER MARKET CLOSE** — the population is still growing (708 @10:30 → 709 @11:5x). ⛔ Do NOT reuse the 11:5x numbers as the post-close baseline.
- ⚠️🕳️ **19% OF THE POPULATION IS PRODUCT-BLIND:** 🔬 **135 of 709** rows have NO `orders.leg='ENTRY'` row ⇒ `product NULL` ⇒ excluded from per-intent attribution. ⭐ The standing `trades.product` schema hazard, firing on real data.
- 🏷️❓ **`COVER_ORDER` / `BRACKET_ORDER` leverage = NOT EXERCISED** — 🔬 zero production rows. Their `6.0`/`5.0` are validated but never applied. ⛔ Do not report them as proven.
- 🌑❌🔝 **27-Aug CARRY CANDIDATE DIED ON ITS OWN — ⛔ NOT a decision, ⛔ not a miss.** 🔬 JINDALSAW exited **12:46:55** and OAL **14:33:41**, both `GTT_EXIT`, i.e. **before the ~15:00 C-1 deadline** ⇒ at 15:00 there was nothing to decide. ⚠️ Same shape as 24-Aug (BALUFORGE/KAMATHOTEL).
- 🚦❓ **EOD GATE TOOK THE TRIVIAL ARM AGAIN — 3rd consecutive flat close (25/26/27-Aug).** 📄 `17:35:00.002 eod_self_exit: past 17:35 IST and flat (0 active positions)`. ⇒ 🔴 **The DISCRIMINATING CNC-only case is STILL NOT EXERCISED.**
- 🏷️ **ALL CARRY-BLOCKED TESTS = NOT EXERCISED — NO CARRY CANDIDATE:** OWED-2 · CHECK 1/2a/2b · four-reading series · three-cause discriminator · G3's owed settled-CNC `used` · revert-trigger precondition (**0** samples) · cause ④ · F6-leg T+1 arm. ⭐ Re-armed.
- 📏✅ **§5 POST-CLOSE NEUTRALITY BASELINE (final population 722):** 🔬 **MIS 503 rows min=max=5.0 · CNC 84 rows min=max=1.0 · 135 NULL-product EXCLUDED.** ⭐ Use THIS as tonight's pre-fix baseline, ⛔ not the 11:5x numbers.
- ✅🧪🔝 **BOTH FROZEN PREDICTIONS SCORED 27-Aug.** ✅ **NEUTRALITY = HELD** — all 7 clauses; executable oracle reproduced **12 real production triples** exactly, differential gate **0 new failures** across 5,896 tests. ⚠️ **WORK SIZE = HELD AS WORDED but the estimate UNDERSTATED by 75%** (predicted ≥8, measured **14**) — that overrun is what triggered the split.
- ⏸🔧 **UNIT 3b OWED (U3-c + U3-e):** remove `fund_manager.py:312-318`'s hardcoded default; replace `.get(intent, 1.0)` with a strict lookup. 🔬 Cost **14 test files / ~26 sites**. ⚠️ Both guard LATENT paths — main.py always supplies the map, and only MIS/CNC occur in production.
- ⏸🔧 **UNIT 3b OWED (U3-c + U3-e):** remove `fund_manager.py:312-318`'s hardcoded default; replace `.get(intent, 1.0)` with a strict lookup. 🔬 Cost **14 test files / ~26 sites**. ⚠️ Both guard LATENT paths only.
- ⏸📋 **UNIT 2 (F11) UNTOUCHED — the PROOF did not complete, ⛔ not "no time".** 🔬 `order_protocol` **100** prod refs + **3 in schema.sql** (a live `trades` column) · `sl_atr_multiplier` **17** yamls. ⛔ No key removed on partial evidence.
- ⏱️✅ **E-5 CLOSED — the 09:15 leg was RECOVERED VM-side 27-Aug 09:23 after the PC died ~09:15.** 🔬 `carry 0.0` @`09:15:00.049` on 4 surfaces (fund_manager field · `main` `delta 0.0` · `fm_ledger 11501` · `get_holdings` *0 holdings*). ⛔ flat book ≠ carry correctness. → §7
- ⚙️❓ **`CONFIG_UNACCESSED: 388 config keys never read`** — boot WARNING `08:15:27.355`, `core.config_validator`. 🏷️ RECORDED, ⛔ **NOT CHASED**. ⚠️ Bounded look later: a two-book split ADDS config surface, and an unread key is how a delivery key goes INERT.
- 🌙❓ **EOD ORDERING QUESTION — ⛔ UNPROVEN, ⛔ not a fault.** 🔬 Trade `11499` closed `15:19:53`, **2m51s AFTER** `RESET_PNL` `11498` `15:17:02`. 💭 Where did its `pnl_delta −6.57` land? ⛔ I did NOT measure. ⭐ Bounded check, pairs with K-1.
- ⚖️⏸ **REVERT TRIGGER — 👤 RAMA: it is SIGN-BLIND, and a free discriminator exists.** 🔬 Causes ①②③ drive the residual **POSITIVE**; NEW cause ④ (carry staleness) drives it **NEGATIVE**. ⭐ A sign in the wording separates them at zero cost. ⛔ I did NOT reword it.
- 🧮❓ **NEW CAUSE ④ — CARRY IS A FIXED SNAPSHOT, NEVER DECREMENTED.** 🔬 `_positional_carry` has 2 writes @`bc9a9f5`: `fund_manager.py:486` + `:1832`; `_intraday_carry` is permanently `0.0` (`:1831`). 💭 A carried CNC that exits leaves `held_today` understated. 🏷️ **UNPROVEN LIVE.**
- ⚠️🔗 **₹/SHARES COLLISION ON ONE EVENT CLASS — RECORDED, ⛔ NOT CHASED.** 🔬 `CapitalDriftDetected.delta` is RUPEES from G3 CHECK 1 (`:3695`) and SHARES from CHECK 5 (`:2566`). 📄 `drift_handler.py:18-24` names it. ⛔ Does NOT reach the revert trigger. Other consumers unaudited.

- 🗳️🚀🔝 **🔴 `D-4` PUSH SCOPE IS THE HIGHEST-VALUE OPEN ITEM.** 🔬 **CORRECTED 25-Aug 22:5x — `fix/ni-batch-23aug` `b397806` IS AN ANCESTOR OF `origin/main` `75e637c` ⇒ IT IS PUSHED; nothing waits on it.**
  - ⚠️ Superseded text, retained: *"SEVEN COMMITTED NI FIXES WAIT ON IT ALONE (`fix/ni-batch-23aug` b397806, 8 commits, gate clean)"* — stale since 24-Aug (N-4).
  - ⭐ What DOES still wait: `tiers` `7d1fd4e` · `controlplane` `5cdd7e9` · `gui09` `725ede9` (carries `S07` `66fc82e`) · `main` `3dff752` — all now owing REFIT vs `75e637c`.
  - Then **D-1b** status logic (⭐ pairs with F14: *"may this control STOP anything?"*) · **D-3** `tier_multipliers`.
  - 👤 D-1a keep 400 CLOSED · D-2 → `F13 · POST-COMPROMISE DETECTION` (L1 ✅APPROVED, L2/L3 ⛔NOT AUTH) · NI-15 **BLOCKED→F13-L1/L2**.

- 🧠✂️🔝 **23-Aug — `MEMORY.md` auto-load: **856 chars over** the ~24,985-char cap. ⚠️ 📄 evidence is FIRST-PERSON (harness: *"Only part of it was loaded"*); ⛔ transcript cannot re-verify. 🔴 **A-3: there is NO memory check at all — 0 hits for `MEMORY.md` in scripts/.claude/settings.** 👤 **M-3 UNCHOSEN** — (c) reorder + (d) trim clears it, ZERO demotion.** 📄 `TRUNCATION_CLAIM_ADJUDICATED_23-Aug-2026.md`.
- 🆓👁️🔝 **`F14 · CONTROLS THAT FIRE AND ARE IGNORED` OPENED 23-Aug — ⭐ distinct from F11 (*cannot fire*); ⛔ NO CODE FIXES F14.** Seeds 🔬 (card’s own seed STRUCK — non-existent): **F14-1** the 10-Aug memory-budget note, correct, read past **13 days** · **F14-2** crontab *"AUTO-INSTALLED"* ×**7**, canonical diff **0 lines** · **F14-3** `NRestarts=`**72,687**. ⛔ **SWEEP RECORDED, NOT RUN.**

## Relocated from the hot index (08-Aug compaction) — status/open work, VERBATIM
*Moved to keep `MEMORY.md` under its read limit. ⛔ The DO-NOT halves STAYED in HOT; only status and open-work detail came here. Nothing summarised.*
- 🧺✅🔝 **[T2 ARMED 29-Jul — 5 CNC HELD OVERNIGHT](t2_arm_result_29jul.md)** — ✅ DDPI VERIFIED 26-Jun. 🔇 exit code is the only signal. 🐚 Git Bash. ⚠️ Also [[slice25-execution-plan-27jul]] (an 'Orphan GTT' WARNING is EXPECTED) · [[t2-btst-close-defer-30jul]] (a BTST close cannot test DDPI).
- ✅🏷️🔝 **[`RMS/MANUAL CLOSE` — v45 VERIFIED LIVE + BACKFILL RUN](rms_manual_close_is_mislabel_26jul.md)** — 35 written, **SIX NULL**. ⚠️ has **no operand on the delivery path** (`GTT_EXIT` carries it).
- 👁️⚠️🔝 **[HEARTBEAT SEMANTICS — DEPLOYED 25-Jul](silent_failure_gaps_25jul.md)** — ⭐ a MISSING `forward_shadow_record` HB on a trading day now means **DEAD**, not "quiet". ⚠️ `pb01_capture` records **`queued=`, NOT captured** ⇒ the row COUNT is the only proof.
- 🔁⛔ **[A CHECK6 REDESIGN MUST NAME #2b + #2c-R](ledger3_design_registration_03aug.md)** — its 3-cycle FIX-B is the ONLY thing bounding both, and ⛔ **neither item's code mentions CHECK6.**
- 🔴 **RAMA-ACTIONS owed — STILL OWED:** ✅ offsite backup DONE 27-Jul · ⛔ **SSH→Tailscale REFUSED — PHONE OFF the tailnet ⇒ closing :22 voids the emergency runbook** · **2FA seed → Fri 7/Sat 8-Aug**. [[operator-backup-ssh-27jul]]
- 🔴⏰ **COMMIT NSE's PUBLISHED `nse_holidays_2027.yaml` BEFORE 31-Dec-2026** — the first 08:15 boot of 2027 does NOT start. ⛔ **NEVER invent the dates.** ✅ It EMAILS you from 15-Dec (`cbcad2c`).
- 🔴 **D1–D4** (⚠️ D1 carries a corrected claim and is BLOCKED by the sector-cap gap) · `require_hmac` → **KEEP FALSE**, REFUSED 20-Jul · arm `pre-receive`? → **NOT as-is**
- 🧺 **T2 basket: ASM/GSM status is the ONE item only Rama can check** (not exposed by the Kite API).

- 🗜️🔴🔝 **OWED RAMA — `MEMORY.md` is `~21 KB` vs a `17.1 KB` target (re-checked 10-Aug close) and ⛔ I STOPPED SHORT ON PURPOSE.** Only 2 entries were relocatable under the file's own rule; **the other 68 are ALL hazard/DO-NOT/invariant/rule.** ⭐ **Hitting the number means DEMOTING HAZARDS — his call.** *(24.4 KB read limit: still loads.)*

## Relocated from the hot index (10-Aug compaction) — status/measurement, VERBATIM
*Moved under the file's OWN placement rule (build STATUS and a MEASUREMENT are not hazards). ⛔ Nothing summarised, nothing deleted.*
- ✅📐🔝 **[TIER 75/85/100 — ✅ BUILT+GATED 10-Aug `3cf3729` on `feat/tier-multipliers-61-62`, ⛔ UNPUSHED](tier_test_phase_built_09aug.md)** — 🟢 **Rama DROPPED `max_qty 3`** ⇒ the blocker is gone and only **3** tests moved, exactly as measured. ⛔ **OFF `65b7196`, ⛔ NOT `645728d` (the split tests/keys DO NOT EXIST there).** ⭐ **THE LAST BUILD.**
- 📐🔴🔝 **[TIER MAPPING — ⛔ *"DELIVERY IS UNCHANGED"* IS TRUE **ONLY ON `65b7196`'s TREE** (re-measured 20-Aug)](tier_mapping_measured_09aug.md)** — on **DEPLOYED `main` the `delivery_tier_multipliers` KEY IS ABSENT ⇒ delivery falls on the INTRADAY family**, so a tier change moves **BOTH** books. ⛔ `3cf3729`'s *"INERT BY CONSTRUCTION"* tag describes ITS tree. → [[no-two-pipeline-split-deployed-20aug]]

## 20-Aug-2026 — RULED: `n907` GO TONIGHT · `tiers` HELD PENDING A CLEAN MEASUREMENT
- 🚦❌🔝 **[⛔ SUPERSEDED 20-Aug 21:01 — THE “CLEAN FF” CLAIM IS **WRONG**](n907_cherrypick_breaks_tiers_ff_20aug.md)** — n907 shipped as the CHERRY-PICK **`4568385`**, ⛔ NOT `d896968`, so `b80354c` (tiers) sits on a parent **NOT on `main`** ⇒ ⛔ **NO LONGER A FAST-FORWARD; tiers needs a REFIT onto `4568385` + a FULL re-gate.** ⭐ Ruling stands: **thresholds-only**.
- 🧮🔴🔝 **⛔ THE SIBLING TRAP THAT PASSES A PER-UNIT CHECK: two units both parented on one base each `--dry-run` as a clean FF *alone*; the first push makes the second `1 ahead / 1 behind`.** ⭐ Always test the SECOND against the FIRST's SHA, ⛔ never against today's `origin/main`.
- 📐⚖️🔝 **[tiers — THREE VARIANTS MEASURED over 2,681 rows (score ≥60, 60 d). ⛔ NO recommendation made; the two evidence sources disagree](tiers_three_variants_measured_20aug.md)** — TODAY `0.50082` **2.00×** · **THRESHOLDS-ONLY** `0.63480` **2.00×** **+26.75 %** · **SHAPE A′** `0.81740` **1.33×** **+63.21 %**. ⛔ Band Inversion is ⛔ NOT settled — scores 50-54 have ZERO trades.
- ⚠️🔢 **A ROUTING SLIP CAUGHT: `0.70/0.70/0.70` is NOT the deployed triple.** Deployed = **`1.0/0.70/0.50`**, measured 3 ways. ⛔ A FLAT triple = spread **1.00× = TIERING OFF ENTIRELY** — a different policy, ⛔ not a rounding slip. [[tier_mapping_measured_09aug]]
- 🧪🔴🔝 **⛔ THE tiers GATE IS VACUOUS W.R.T. THE VALUES — PROVEN BY PLANTING, ⛔ not assumed.** Planting `MEDIUM 0.85 → 0.99` ⇒ `rc=0`, **271 passed, byte-identical to control**. Planting a broken ordering (`high 62 → 59`) ⇒ `rc=1`, **5F / 47 errors**. ⇒ the suite guards the tier config's **STRUCTURE** and places **ZERO constraint on the VALUES**. ⛔ A green gate here carries far less weight than it looks like it does.
- 💰⭐ **THE BOUND (the reassuring half): `max_concentration_pct 0.10 × ₹10,609.10 = ₹1,060.91`; largest position EVER taken = ₹963.30 (265 fills).** `tier_mult` applies **AFTER** `min(risk, capital, conc)` ⇒ ⭐ **typical size rises TOWARD the ceiling; ⛔ the ceiling does NOT move.**
- 🧊📌 **[Frozen 20-Aug — the prediction files, their hashes, ADDENDUM 13 scored](frozen_predictions_20aug.md)** — ② **CORROBORATED**, first `G3` delta **₹0.00** ⇒ DEFECT A is **per-session**, ⛔ NOT closed. ⛔ Both UNTRACKED in the root worktree.
- 📏 **[HISTORICAL — ⛔ base is now `4568385`] [Gate base `08b462b` = rc 1 · 7F / 5,646P / 4S](gate_base_08b462b_historical_20aug.md)** — ⭐ the 7 are **set-identical name-for-name to the 17-Aug `6fa8a1c` baseline**, so the harness is proven, ⛔ not assumed.
- 🔔⏳🔝 **RELOCATED FROM THE HOT PIN 20-Aug (⛔ not dropped — the pin now carries n907): ALERTS ⑤ `f62db55` = `DEPLOYED · LOADED IN BOTH PROCESSES · ⛔ NOT VERIFIED LIVE`.** 🔴 **`alert_send_caller` = 0 across every file under `logs/`** ⇒ ⛔ *“alerts live”* is NOT written. ⭐ Rung ③ needs a REAL SMTP failure with pending sentinels — ⛔ none induced. [[alert-delivery-contract-phase0-09aug]]

## Decisions & open threads
- 🕳️🔴 **F12 · THE ALREADY-BUILT ANSWER — ⛔ OPENED, ⛔ NOT STARTED.** ⭐ TWICE in one day a thing treated as UNBUILT existed in a built, tested, NEVER-DEPLOYED tree — both found BY ACCIDENT. 🔴 The cost is **a SECOND solution to one problem**. ⚠️ F12 ≠ F11.
- 🧮🔴 **NI-16 IS A PRECONDITION ON WIRING `PerformanceAllocator` (`N9-10`)** — unfixed it breaches CONCENTRATION **and** the RISK BUDGET on every HIGH trade, silently. ⚠️ `N9-10` may already lock the clamp, but it sits on `65b7196`, ⛔ unread. [[min-rule-multiplier-after-cap-22aug]]
- 🕳️🔴 **F11 · INERT-CONTROL SWEEP — ⛔ OPENED, ⛔ NOT STARTED.** ⭐ 9+ instances of ONE shape: *a control that exists, runs, reports healthy, constrains NOTHING* (`N20-48`). ⛔ Finding them one at a time, by accident, is no longer the method. → [[exit5-restart-loop-unbounded-22aug]]
- 🗓️🕳️ **[⛔ NEVER TRUST *"grep today's `alert_watcher` log"* — THE NAME IS FIXED AT PROCESS START AND `--loop` OUTLIVES IT](alert_watcher_log_name_frozen_18aug.md)** `<MEASURED · LATENT · ⛔ NOT FIXED>` 🔴 OWED: rotate on date change. `N18-06`
- 💀🔴🔝 **[A ⛔ **LIVE** HAZARD, 14-Aug — A PAYOUT / SETTLEMENT SWEEP LANDING WHILE POSITIONS ARE OUTSTANDING CAN HARD-KILL **BOTH** BOOKS **TODAY**](payout_sweep_hard_kill_hazard_14aug.md)** `<MEASURED · NOT FIXED>` — `fund_manager.py:2391` → `_handle_invariant_violation`. ⚠️ **Fix 1 repaired ONLY the BOOT-time version ⇒ the MID-SESSION one is UNREPAIRED.** `N14-09`
- 🧮⏭️🔝 **[CAPITAL RECOMPUTATION — ⛔ DEFERRED ON RAMA'S WORD, ⛔ nothing built 14-Aug](capital_recomputation_deferred_14aug.md)** — ✅ **Δ source RESOLVED = ① broker-attributed** (`utilised.payout` &c). ⛔ the `net − last_known_net` fallback is RETRACTED. 🔴 **It is a SCHEMA MIGRATION ⇒ ⛔ never an evening push.** `N14-10`
- ⏳🔮🔝 **[FIX 2 SCORED 14-Aug — TWO HALVES STILL OPEN, ⛔ recorded as `NOT YET DETERMINABLE`, ⛔ never as a pass](fix2_scored_14aug.md)** — ① P6's ENTRIES half (window had not opened at report time) · ② P7's SECOND half (registry re-divergence at the 16:22 officer run). 📌 **Both are FREE measurements at the next EOD pass — ⛔ neither needs a change.**
- 🔍🔴🔝 **[⛔ A **RED** CHECK IS EVIDENCE ONLY ONCE ITS METHOD IS VERIFIED — NEW RULE, 14-Aug](probe_method_must_be_verified_14aug.md)** — ⭐ the mirror of *"a green check is evidence only if it could have been red"*, and it was MISSING. **THREE mis-specified probes fired in one morning.** ⛔ **Ask *"could this probe have found the thing?"* BEFORE reporting any absence.**
- 🚨🔴🔝 **[⛔⛔ NEVER `rm -rf` ON ANY PATH UNDER `D:/Projects/` — FOUR **LIVE** venv SYMLINKS POINT INTO THE SHARED OBJECT STORE (13-Aug, MEASURED)](venv_symlinks_shared_object_store_13aug.md)** — ⭐ **USE SHAPES THAT REFUSE: `rmdir` for a directory; plain `rm` (⛔ no `-r`, ⛔ no `-f`) for a symlink.** [[gate-worktree-venv-hazards]]
- 🗑️⏸️🔝 **[`D:/Projects/trading-system-fix2` SHELL — ⏸️ **NOT DELETED, AWAITING RAMA**](fix2_shell_dir_awaiting_rama_13aug.md)** — his `rmdir` REFUSED because `venv` is a **DANGLING SYMLINK**. ⭐ **The command's own guard stopped it — *"the protection is in the command, not in my authorisation."*** ⛔ Plain `rm` NOT substituted on my own authority.
- 🗂️✅🔝 **[WORKTREE AUDIT 13-Aug — ✅ CLOSED: RAMA AUTHORISED **ONLY** `trading-system-fix2`](worktree_audit_13aug.md)** — ⚠️ **`git worktree remove` is ⛔ NOT ATOMIC ON WINDOWS** ⇒ an orphaned shell dir remains. ⚠️⚠️ **CORRECTED 14-Aug — ⛔ THE `gui04` CLAUSE IS DEAD ON BOTH HALVES.** Worktrees now **7**. [[install-collision-map-10aug]]
- 🪤🔴🔝 **[`trading-system-alertfix` IS A LIVE TRAP, ⛔ NOT MERELY A KEEP (Rama, 13-Aug)](alertfix_worktree_is_a_trap_13aug.md)** — `fix/alert-remediation` `bfd6b5f` is a STRICT ANCESTOR of the deployable `fix/alert-phase2-watcher` `071169b`, **ONE COMMIT SHORT** ⇒ ⛔ pushing it OMITS the availability fix. ⇒ FIVE pending units, ⛔ not six.
- 🧨⚠️🔝 **[⛔ NOT A NEW RULE — THE **SECOND** INSTANCE OF *"a green check is evidence ONLY if it could have been red"* (Rama, 13-Aug)](rev_list_exclude_all_false_green_13aug.md)** — ⭐ NEW: **THE FIRST APPLICATION TO A DESTRUCTIVE OPERATION, WHERE A FALSE GREEN HAS NO ROLLBACK.** `--exclude=` never applied to `--all`. [[feedback-verify-rc-not-output]]
- 🧮🔴🔝 **[M-C2 — DELIVERY CAP TOCTOU IS `LIVE (REACHABLE)`, ⛔ NOT LATENT](mc2_delivery_cap_toctou_live.md)** `<MEASURED · NOT FIXED · NOT DESIGNED>` — ⭐ **SLOT-CAP defect, ⛔ NOT capital** — bounded at `₹3,193.68`; reach 6–7 vs a cap of 3. 🔑 **PARITY IS THE DEFECT: intraday has FIX-018 + Bug E, delivery has neither.**
- 💀🔢🔝 **[⛔ THE *"IDLE ₹6,900 — ONE SWITCH"* FRAMING IS DEAD, ⛔ do not revive it](inert_by_arithmetic_label_11aug.md)** — the figures have NO base, **and `conditional_allocation_enabled` is a NO-OP at `trade_type: BOTH` — both branches return `(0.70, 0.30)`.** ⭐ **NEW LABEL: `INERT BY ARITHMETIC`** — reader present, branch reachable, branches identical.
- 🔗📐🔝 **[HIDDEN COUPLING — A PRECONDITION ON INSTALL ⑥, ⛔ NOT AN INVESTIGATION](hidden_coupling_bucket_slot_concentration.md)** — `0.30 ÷ 3 = 0.10` makes `positional_bucket_pct ÷ max_open_delivery_positions` EQUAL `max_concentration_pct` exactly. ⭐ At MAX size the slot cap self-enforces through capital; **M-C2 bites only BELOW the concentration ceiling.**
- 📢🔴🔝 **[11-Aug CLUSTER — THREE MEASURED REPORT-TRUTHFULNESS DEFECTS + ONE WRONG CALL, `<MEASURED · NOT FIXED>`](report_truthfulness_cluster_11aug.md)** — 🔑 **`reconcile_positions` `exit 2` MEANS *mismatch FOUND* and is rendered `FAILED`** · **`watchman`/`flow_trace` have ZERO crontab entries** · **the EOD `SOFT_KILL` SUMMARY is a HARDCODED string.**
- 🧮🔴🔝 **[CONCENTRATION IS THE BINDING CONSTRAINT, AND IT HAS A LIVE CEILING](concentration_binding_ceiling_11aug.md)** — base `₹10,645.60` @ 11-Aug: `10 %` ⇒ `₹1,064.56` ⇒ ⛔ ANY symbol priced above it sizes to ZERO. ✅ **NOT silent** — `constraint="CONCENTRATION"` + all three operands. 🧪 PARITY: path SHARED.
- 📐⚠️🔝 **[M3 CORRECTION — ⛔ ATTACH THE SHA OR THE LINE DESCRIBES CODE THAT IS NOT RUNNING](m3_attach_the_sha_correction.md)** — the sizing divisor `max_daily_trades` belongs to the UNPUSHED `65b7196`. ⛔ **The DEPLOYED `645728d` has NO divisor — `qty_by_capital = floor(avail_bucket ÷ margin_per_share)` over the WHOLE bucket.** [[stated-vs-configured-limits-09aug]]
- 🗺️✅🔝 **[INSTALL MAP COMPLETE 10-Aug — TEN live branches (⛔ `main` has NO worktree), 6 installs + 5 refits (3 SUBSTANTIVE), ~2 WEEKS baseline](install_collision_map_10aug.md)** — ⛔ **NO FURTHER INSTALL-MAP WORK; no rebase until the evening it is needed.** 🔴 **OWED RAMA: the calendar** *(the refits are not in his week)*.
- 🔔✅🔝 **10-Aug CLOSE — ⭐⭐ THE BUILD QUEUE IS EMPTY; `3cf3729` (tiers) WAS THE LAST THING TO WRITE.** 🔑 **Fix 3 + alert phases 3-5 are GATED ON MEASUREMENTS A HALTED SYSTEM CANNOT TAKE** ⇒ **INSTALLS ONLY from here, ONE PER EVENING, each with its own trading day.** 🗓️ **ORDER: ⓪ score BOTH predictions → Fix 1 ALONE → Fix 2 → registry split → F6 → Tick 2 → sizing.**
- ✅🗂️🔝 **10-Aug CLOSE — THREE OF THE FOURTEEN CLOSED, ⛔ DO NOT REWORK: item 1 = NO-OP (`max_qty` absent from `645728d`/`main`/`0337378`; commented `10` in `65b7196` — the `3` NEVER SHIPPED) · item 2 = DONE `0337378` ⚠️ **NOW BLOCKED by the 07-vs-10-Aug contradiction** · OPEN-2 = FOUND, ⛔ not a ghost.** ✅ **Item 6 BUILT+GATED `cf16554`.** [[item6-registry-daily-critical-10aug]] [[same-day-reentry-contradiction-10aug]]
- 🟢🧮🔝 **VALUE-CAP THREAD — ✅ CLOSED 10-Aug, RAMA: *CHANGE NOTHING*. ⛔ NOTHING EDITED, no new key, no test touched.** ✅ **Delivery cap VERIFIED `0.25 × ₹3,000 = ₹750` > the `₹500` allocation.** 🔴 **And intraday ALREADY has one — `0.25 × ₹35,000 = ₹8,750` > `₹5,833` — so the SAME test gives the SAME answer.** [[value-cap-card-stopped-10aug]]
- 🔑📐🔝 **WHY IT CLOSED — `₹6,000` COULD NEVER BIND: `position_sizer.py:586-589` reduces to `qty = floor(allocation ÷ price)` (the stop CANCELS) and `effective_mult` is clamped `≤1.0` ⇒ `qty × price ≤ ₹5,833.33` AT ANY PRICE, ANY STOP, ANY TIER.** ⛔ **An inert ceiling, ⛔ not a backstop.** [[value-cap-card-stopped-10aug]]
- 🚫🗝️🔝 **⭐ THE GUARD DID ITS JOB — AN ABSOLUTE ₹ POSITION-VALUE KEY IS A *GUARDED DELETED KEY*: `config_auditor.py:347-352` raises `B2_max_position_value_rs_resurrected` — *"BUILD 1 replaced it with the capital-relative `max_position_value_pct`. Remove the Rs key."*** ⚠️ **Preflight `B_single_source` asserts the same. ⛔ A different NAME would EVADE a guard built for this.** [[value-cap-card-stopped-10aug]]
- ⏹️🔴🔝 **SIZING TEST-CONTRACT SPLIT — RESUME REFUSED A THIRD TIME, 10-Aug close. ⛔ ITS PREMISE (*"nothing about it needs a decision"*) IS REFUTED BY TODAY'S OWN RECORD: authorised for **5** tests, **12** are red, **8 OUTSIDE the authorisation**, and the (A)/(B) choice was MEASURED AND DELIBERATELY NOT TAKEN.** 🔑 **ONE LINE FROM RAMA UNBLOCKS IT — ⛔ nothing else does.** [[tier-test-phase-built-09aug]]
- 🔍✅🔝 **VERIFIED 10-Aug close — the twice-reverted config IS still clean: both `max_qty` lines are COMMENTED (`system_config.yaml:230,261`), and every line the working tree adds over `65b7196` is a comment.** ⛔ **No live `max_qty` key exists in any build — the `3` is a PROPOSAL, ⛔ not shipped.** [[stated-vs-configured-limits-09aug]]
- 📐🔒🔝 **ORDER SIZING = ALLOCATION MODEL — `FROZEN · COMMITTED LOCALLY `65b7196` · NOT PUSHED`. ⛔ A commit is NOT permission to deploy.** 🚦 **GO/NO-GO is now NINE lines — line 9 proves the pushed ref excludes the sizing branch (it carries schema v46).**
- 🔴❓🔝 **THREE AWAIT RAMA — ⛔ RECORD, DO NOT RESOLVE:** ① **C5 is a CLASSIFICATION, not a number** — if simultaneous-exposure ceiling and daily realised stop are DELIBERATELY different controls, nothing changes; ⛔ do not touch `5`/`1%`/`2.10%` ② **the sizing NUMERATOR — ask *"what fraction of your money on ONE trade?"*, ⛔ not our vocabulary** ③ Monday's `margins()` read. [[two-pipeline-split-08aug]]
- 🗂️🔴🔝 **DEPLOYABLE ALERT REF = `fix/alert-phase2-watcher` (contains P0+P1+P2); ⛔ `fix/alert-remediation` is P0+P1 ONLY and pushing it OMITS the availability fix.** ✅ Only sizing is v46. 🗓️ Sequence: MON F6 · TUE eve alerts · WED eve sizing · THU eve Tick 2 · FRI eve N9-07 — Rama's call.** [[branch-inventory-deploy-sequence-09aug]]
- 🃏🔑🔝 **CARD 04 REPLACES CARD 03 — the question is *WHAT THRESHOLD SHOULD C5 REPRESENT?*, ⛔ not *delete the key?* 🔴 SUBSTANCE: `₹525` vs a `₹210` daily stop = ~2.5×, REALISED-based ⇒ it cannot get in front. ⛔ A slot cut alone does NOT fix it (3 = ₹262.50). ⛔ WE PROPOSE NO NUMBER.** [[c5-c5b-risk-pct-card03-09aug]]
- 🔬📅🔝 **MONDAY §3.6b ADDED — the `margins()` capture: 4 readings (before entry · after entry · after SL · after TGT), SAME symbol+qty, hashed.** ⛔ **AFTER E1-E7 scoring. ⛔ NO natural delivery entry ⇒ IT DOES NOT HAPPEN — `NOT MEASURED` is VALID; ⛔ never manufacture a trade.** ⛔ *"Position-reducing needs no margin"* stays **(I)** until the numbers exist. ⚠️ LIVE-ONLY — paper never calls `margins()`.
- 🛑✅🔝 **PIPELINE LOSS GOVERNOR `<BUILT 08-Aug>` — ⛔ IT IS NO LONGER A KILL, AND THAT IS THE WHOLE FIX.** The gate already blocks the breached book ⇒ **NO NEW STATE**: survives restart by construction, clears at the DAY boundary, ⛔ NOT `SOFT_KILL`'s boot-bound clearing. ⛔ **kill_switch stays PRODUCT-BLIND (35 callers).** Delivery breach closes NOTHING (Q4). [[loss-governor-scope-08aug]]
- 🏷️✅🔝 **D1 DONE `<BUILT 08-Aug>`: `intraday_max_open_positions`/`intraday_max_daily_trades`, 43 files, NO aliases** *(old key ⇒ loud startup error)*. ⭐ **`capacity.py` needed the COUNT, not the label.** 🔴 **OWED RAMA: `qty = capital-per-scrip ÷ SL points` differs from the code ~140× at ₹10k — NAME THE NUMERATOR (risk budget vs deployable) before any sizing build.** [[capital-vocabulary]]
- 🔴🛑🔝 **THE SPLIT SEPARATED THE COUNTERS, ⛔ NOT THE *ACTION*: a daily-loss breach still fires a SYSTEM-WIDE `soft_kill` ⇒ an INTRADAY loss STOPS DELIVERY and vice versa.** ⭐ **TWO actions, TWO scopes — the CLOSE is already MIS/CO-only (EOD6); only the KILL is wrong.** ⛔ **The fix is NOT a product-aware kill switch (35 callers) — its own build.** [[loss-governor-scope-08aug]]
- ⚖️✅🔝 **SETTLED — ChatGPT §C (*"anchor the daily gate to the first FILLED entry"*): ⛔ DO NOT IMPLEMENT.** Its precondition FAILED (nothing filled) **and its substantive ask is ALREADY SATISFIED — `_EXECUTED_TRADE_STATUSES` CONTAINS `CLOSED`+`CLOSED_MANUAL`, so a filled-then-flat trade DOES consume the day.** ⛔ Implementing it changes nothing except pulling `FAILED` in = FIX-181 REVERSED. [[pncinfra-double-entry-08aug]]
- 🟢🔎🔝 **PNCINFRA 06-Aug "double entry" — NO DEFECT, NO GATE HOLE. ⛔ THE PREMISE FAILED: NEITHER ORDER FILLED** (3 attempts, all `FAILED`, ENTRY orders `CANCELLED` qty_filled=0 — the alert prints the PLACEMENT price). ⭐ **Gate 1 fired 19× that day; `FAILED` is excluded BY FIX-181 ON PURPOSE.** ✅ **Corpus scan 0 since 03-Aug vs CONTROL 4 before ⇒ OPEN-1 evidence STANDS.** [[pncinfra-double-entry-08aug]]
- 🔴📉 **FILED, ⛔ NOT CHASED: 49 `FAILED` + 10 `REJECTED` vs 24 EXECUTED since 03-Aug — two-thirds of trade rows never opened exposure.** A FILL-RATE question, ⛔ not a gate question; needs its own measurement. [[pncinfra-double-entry-08aug]]
- 🧭🔴🔝 **TWO-PIPELINE SPLIT `<BUILT 08-Aug · branch feat/delivery-config-split>` — ⛔ NOT DEPLOYED, ⛔ NOT with F6.** ⭐⭐ **SEPARATING THE LIMITS IS THE EASY HALF — A SHARED COUNTER WITH TWO LIMITS READING IT IS STILL A SHARED LIMIT** (4 couplings, 1 in memory). 🔴 **DELIVERY SIZE ×1.5-1.8 = REAL EXPOSURE RISE.** 🔴 **OWED: rename/labels for 9 global readers.** [[two-pipeline-split-08aug]]
- 🎯🔴🔝 **F6 `<AUTHORISED 08-Aug · c39e799 · NO-GO 10-Aug>` — ⛔ NOT DEPLOYED. Gate 3+6 FAILED: the 10-Aug boot HARD_KILLED ~60 s BEFORE `cnc_gtt_monitor` ran ⇒ F6's first live execution would sit behind a gate that can PREVENT it running at all.** ⭐ The window recurs nightly; the first-live observation does not. ⛔ **The nightly stop STILL stands.** [[delivery-book-ceiling-10aug]]
- 🧮✅🔝 **FIX 1 `<BUILT · REBASED ONTO THE DEPLOYED `645728d` · `63caa52`+`2e1f109` · ⛔ UNPUSHED>` — a carried delivery position was counted TWICE when re-basing from broker cash.** ✅ **Rebase CLEAN; `range-diff` `=` on both ⇒ patches unaltered** (pre-rebase tip tagged `fix1-prerebase-10aug`). ⭐⭐ **IT IS F6's PRECONDITION, ⛔ not F6's competitor.** [[fix1-carried-position-accounting-10aug]]
- 💸✅🔝 **ANSWERED 10-Aug — the `₹8,773.78` WAS THE SEBI QUARTERLY SETTLEMENT.** ⛔ Not a loss, not a withdrawal. ⭐ **SCHEDULED + RECURRING ⇒ the conditional resolves: "Monday-after HARD_KILL on a carried CNC" IS a schedule.** ✅ Pinned by tests A + H/H2 (both paths, to ₹0 cash). [[delivery-book-ceiling-10aug]]
- 🟢🔬🔝 **FIX 2 `<BUILT · tip `ee3ff49` · off the DEPLOYED `645728d` · ⛔ UNPUSHED>` — BOTH checks now done.** `capital_deployment` had **NO predicate** (`432.3 %` PASSED); ⛔ **NO NUMBER INVENTED** — the bound is the capital identity. ✅ **`kite_funds_available` = Rama's `₹2,000`, in `config/preflight.yaml` (⛔ NOT in `AppConfig`).** [[fix2-preflight-capital-checks-10aug]]
- ⚠️🔑🔝 **THE `₹2,000` FLOOR DOES **NOT** BLOCK THE SYSTEM — MEASURED BEFORE IT WAS SET.** ⛔ **Nothing in the boot chain reads the preflight sentinel**; `Criticality` = how LOUD, ⛔ not whether anything stops. ⏰ ⛔ **Phase A is the 08:30 cron ⇒ 15 min AFTER the 08:15 boot — it could NOT have saved 10-Aug.** [[fix2-preflight-capital-checks-10aug]]
- ✅🔮🔝 **ANSWERED — RAMA'S POSITIONS SCREEN IS EMPTY ⇒ `held = 0+0 = 0` ⇒ (A) DETERMINED as an INPUT state, both `_gather` terms measured pre-boot.** ⚠️ **Limits: broker UI ⛔ not API · the code reads `raw["net"]` (`zerodha_adapter.py:1228-1239`), Rama's gloss names DAY · taken ~14:00, boot is 08:15.** ⛔ **NOT evidence the code RAN (A).** [[diffnkg-prediction-11aug]]
- 🏷️🔴🔝 **MY OWN ERROR, RECORDED: MANINFRA's `₹661–685` forecast used TODAY'S `fm_ledger` INIT (`209.80`, a pre-payin DAILY SEED) as a proxy for TOMORROW'S live `margins().net`.** ⛔ **Worse than a stale seed — DIFFNKG's file `:133`, written HOURS EARLIER THE SAME NIGHT, already had `₹10,209.80`.** ⭐ **Not re-derived: NOT LOOKED UP.** [[capital-vocabulary]]
- 🔬📡🔝 **API MEASUREMENT SUPERSEDES BOTH SCREENSHOTS — `reconcile_positions` `15:45:02.715`: `DIFFNKG broker=0` · `MANINFRA broker=−4`.** ⭐ It reads `positions()` ONLY = **exactly `_gather:464`.** ⇒ ✅ DIFFNKG both terms 0 by API; 🔴 **MANINFRA's `−4` IS REAL — if it survives to 08:15, `held=4`.** ⛔ **15:45 ≠ 08:15; the CLOSE call stands.** [[maninfra-prediction-11aug]]
- 🔴🔫🔝 **MANINFRA'S GTT WAS EXECUTED **BROKER-SIDE** TODAY — ⛔ NOT by the system, which was dead since `08:15:25`.** ⭐ **Its row can reach branch 1 (`bg` listed `triggered`) where DIFFNKG cannot** ⇒ 🚨 **`_reprotect` has NO `in_hours` gate ⇒ a real SELL GTT for 4 shares AT 08:15, ⛔ NO warning window.** ⭐ CALL = **CLOSES**, MODERATE. [[maninfra-prediction-11aug]]
- 🗓️🔴🔝 **TOMORROW, THIS ORDER, BOTH ROWS, NOTHING BEFORE IT:** ① did the boot REACH the monitor *(if not ⇒ BOTH `NOT TESTED`)* ② per row, which branch — **by the frozen signature tables, ⛔ never by narrative** ③ capture exit_price · status · P&L · `CLEANED` · `RELEASE_USED` ④ 🔑 **score *"P&L TOO FAVOURABLE"* SEPARATELY** ⑤ then the deploy. [[maninfra-prediction-11aug]]
- 🔴🧮🔝 **NEW OPEN — THE SWEEP STILL KILLS THROUGH THE *INTRADAY* BUCKET (Fix 1 is positional-only).** MEASURED: same-day restart kills above **58.8 % of the intraday bucket** — ⛔ but ONLY IF broker `net` excludes blocked intraday margin. ⭐ **§3.6b `margins()` is the whole decision.** LATENT. [[fix1-carried-position-accounting-10aug]]
- 📜⚠️ **`G11` IS NOT IN `docs/campaign_practices.md`** — (P) 0 hits; it landed in memory/MAP/PATHS only, while HOT advertises *"G1-G11"*. 🔴 **OWED: transcribe from `reversibility_two_claims_08aug.md`.** ⭐ `G12` IS in.
- ⚖️🔴🔝 **OWED RAMA (07-Aug, after rulings 1+2):** ① ⛔ **the config flip `one_trade_per_symbol_direction_per_day: true→false` — Ruling 2's WHOLE loosening, NOT authorised** ② does *"immediately eligible again"* govern the **300 s `per_symbol_cooldown_sec`** too? ③ retire `CONTRARY_POSITION` (**0** fires in 109,254) or keep it a documented no-op? ⛔ **F6 FIRST — it is Ruling 2's prerequisite.** [[rulings-1-2-taken-07aug]]
- 📐🔴 **(E) 07-Aug: FIRED once (§3.5 — tier HALVED MANINFRA 8→4, 1st live; scope corrected, tier+G2 rise). 2nd reopen REFUSED: 492/492 concentration UNIQUE min, 0 ties — register CONFIRMED.** ⛔ Card's 18/9/9-tie NOT in the DB. Impl FROZEN. → sizing_thread_conclusions §3.5-3.6
- 🚀✅🔝 **06-Aug CLOSED — STOP EXECUTED 20:32:19 (clean, MEASURED) · PUSHED `b54b5c9`, 98 commits · `ahead 0` · PC==VM by md5.** ⭐ **Regression gate ran as SETS: base-only 27 (the push FIXES them), merge-only 1 = a PROVEN pre-existing flake.** ⛔ **G1 #8 filed: a correct auto-fill beside a real ruling.** [[daily-resets-clock-bound-06aug]]
- 🔴 **OWED RAMA (06-Aug):** ① twin-retirement ruling (`risk_per_trade_pct`·`max_position_value_pct`) ② `watchman`/`flow_trace`: retire the CHECK or the producer ③ classification-leakage + integrity gate ④ **F6 cost #7 — P&L understated by more than its own value.** ⛔ Sizing FROZEN
- 🏷️🔎 **⛔ FILE, DO NOT CHASE — [the 06-Aug 08:15 boot self-labelled `startup_scenario=CRASH` after a CLEAN stop](startup_scenario_crash_mislabel_06aug.md).** ⚠️ Mechanism INFERRED; whether `CRASH` alters boot recovery is UNVERIFIED.
- ⏰🔀🔝 **PREDICTED TUE 18:00 — a `CRON INTEGRITY WARNING` naming the 4 claude heartbeats. EXPECTED, ⛔ not an incident.** Live crontab 0 claude (removed ~02:12); VM registry @`4149263` still declares them ⇒ absent-from-live. ⭐ **WARNING not CRITICAL only because `personal_tooling: true` — `check_cron_drift.py:123-127`; that flag is LOAD-BEARING.** Clears when `71f331b` rides the flip push (49→45 jobs).
- ✅🏷️🔝 **15:15 PAIR FIXED `4149263` (Rama ruled, rides the flip push) — ⛔ TWO WRONG PRESCRIPTIONS REMAIN, both CODE, NOT authorised:** (a) `Naked untracked position` **false 5/5 — a GTT-blind DETECTOR (IA-P5-06), not a wording fix**; (b) `STRATEGY PAUSED` *"rest of today"* vs `strategy_governor.py:42` in-memory. Warned meanwhile in `expected_alarms.md` §6a/§6d.
- 🎯✅🔝 **LEDGER #2 (BUY-DAY FILTER) `<BUILT>` `43043a2`+`2e606ec` — CNC SURVIVES HARD_KILL (Q4); NULL/NRML flatten+CRITICAL; ONE vocab source; NEW-set EMPTY.** 🔴 **OWED: the THIRD-SITE ruling — reconciler CHECK2 flattens under kill, product-blind (CNC-unreachable pre-flip): #2b Mon-eve or carry-pilot blocker** + D1–D3 + the slot. Record `docs/audit/buyday_filter_build_01aug2026.md`.
- 🛠️✅🔝 **LEDGER #1 — `<BUILT — STOP RESOLVED `4959111`>`, ⛔ NOT DEPLOYED/PUSHED; 🔴 OWED: the DEPLOY SLOT** (Mon-eve-with-flip vs Tue-eve→Wed). ⏳ **MON pre-deploy: PC-paper composition boot (B2 must PASS clean) + calm regression confirm** (3 isolation-passing flips, known-flaky consec-losses family — record §6a). `docs/audit/effect_telemetry_phaseB_build_01aug2026.md`.
- 🏁✅🔝 **[REGISTER — ✅ **PHASE 1 COMPLETE** on `main` (`1bde728`; DOCS-ONLY, F6 code SHA `9fdfe41` untouched). ALL FOUR sources merged; **333 rows / 291 merged**](register_rebuild_plan_10aug.md)** — ⛔ **labelled `STATUSES UNVERIFIED`, ⛔ NEVER "complete"; Phase 2 NOT started.** 🔴 **FINDING 7: the 15 `X` items fell out of the chain at 28-Jul and were in NO later edition.**
- 📋⭐🔝 **THE WORKING REGISTER IS `docs/MASTER_PENDING_01-Aug-2026.md`** — ⭐ **N = 271** *(10-Aug pass, +11 rows `N10-01`…`N10-11`; `260 + 11`)*. 🔴 **SIX row candidates STILL await Rama — if admitted `271 → 277`. ⛔ N is GOVERNED.** ⚠️ **N10-11 records that ~85 % of rows carry NO status.** ⛔ 28/30-Jul masters SUPERSEDED-but-RETAINED — where they disagree, THEY WIN.
- 🏁🔎 **INTEGRITY AUDIT 2026 — ✅ COMPLETE, 16 phases, local `4603b75`** → `docs/audit/integrity_audit_2026.md` (4,593 lines). **VERDICT: well-built, NOT yet profitable (R1); dominant risk = nothing verifies a declared thing has EFFECT.** ⛔ FIX CAMPAIGN separate, filter-FIRST.
- 📅⚠️🔝 **THU 30-JUL SLOT — SETTLED: tonight is `fix-tests`+S4+`214a878`+docs; `fix-symdir` is FRI eve → MON boot (calendar §6). ONE boot variable (S4).** ✅ §7.1 gate **PROCEED** — #16a inert by TWO conditions (`delivery_enabled:false` AND `force_intraday_only:true`). 🔴 **AWAITS RAMA: the calendar rejected "evening before a carried-CNC sale" as THE WORST SLOT — that is now TONIGHT.** ⭐ Counter: S4 REMOVES a halt.
- 🔗⚠️ **THE T2 CLOSE SHARES THE DEPLOYED CODE** — `load_all()` (`t2_cnc_gtt_realtest.py:157`) runs the config auditor + `raise_if_blocked()` (`config_loader.py:1790`). ⇒ **"independent of the service" ≠ "independent of the push."** Re-rehearse after a push (omit confirm ⇒ EXIT=2).
- 🔄📐 **RECONCILIATION DESIGN DOC DONE, NOTHING BUILT** (`docs/audit/reconciliation_redesign_design_30jul2026.txt`). ⭐ **NOT a 4-Aug blocker** — but **step 1 (scope `reconcile_positions` to intraday) ships WITH the flip**, else a daily false CRITICAL. 🔴 **AWAITS RAMA Q1-Q5.**
- 🔒📉 **ROOT-PROBE ALERT — 400/hr sits INSIDE the noise (p95 413, MAX ever 516) ⇒ ~1.6 alerts/day BY DESIGN** [`ssh_root_probe_audit_30jul.md`]. 🔴 **AWAITS RAMA:** invariants (base rate 0/50d) + an `sshd -T` drift watch; or single-IP >250/hr. ⛔ **NOT 600.**
- 📅⭐🔝 **THURSDAY SLOT RE-COUNTED 28-Jul — the overload was FRIDAY** (calendar §6; `45e0133` UNPUSHED). `fix-tests-27jul` = **ZERO non-test files**; **#16a INERT** (`delivery_enabled=false`) ⇒ **Fri boot = ONE live change (S4)**. ⭐ #16a only ADDS a boot refusal, S4 only REMOVES one — opposite signs ⇒ no separate boot needed. 🔴 **AWAITS RAMA: move audit trail `214a878` Fri→Thu** (2 files, no schema; delay cost PERMANENT).
- ✅🔐🔝 **CREDENTIALS ROTATED + WIRED 25-Jul (Rama rotated; I wired): `TELEGRAM_BOT_TOKEN` + `ZERODHA_TOTP_LFL836` on BOTH VM and PC.** Telegram VERIFIED live (`getMe` ok, Trade_sysbot, no message sent); TOTP verified **offline only** — ⚠️ **broker acceptance UNPROVEN until Mon 08:15.** `.env` 600, exactly 2 keys changed (68/68). ⛔ `WEBHOOK_SECRET` untouched.
- ✅🛡️ **rpcbind DISABLED 25-Jul** — both `.socket` AND `.service`; `:111` silent, both inactive+disabled. Rollback `systemctl enable --now rpcbind.socket`. **PC `.env` ACL fixed** (was world-readable ⇒ owner-only, still readable).
- 🗑️✅ **`predeploy-*`: ACCIDENT (no code creates it) AND pure DUPLICATION** — oldest backup **12-Jul**, series 12→19 unbroken, 2 surviving `pre_*` from 17-Jul itself ⇒ deleting loses nothing, ~764 MB. ⚠️ renaming to `pre_*` = DELETE in disguise.
- 🔐⚡🔝 **SECURITY ITEMS NOW EXECUTABLE — [`security_items_scoped_25jul2026.md`]** (verified, not assumed): **rpcbind SAFE to disable** (`rpcinfo -p` = only portmapper, 0 nfs mounts) ⚠️ **must disable `.socket` AND `.service`** · **Telegram rotation needs NO mid-week restart — do it while the service is DOWN** (cron re-reads `.env`; the service holds it from boot); verify with `getMe`, never a test alert.
- 🔴🕐 **2FA seed MOVE — DEFERRED 27-Jul, STILL OWED.** ⛔ NOT 31-Jul/1-Aug — that made Mon 3-Aug a credential day and 3-Aug belongs to the delivery sequence. Rule: FRI-EVE/SAT, and the FOLLOWING Monday must not be a Slice-2.5 step. Next **Fri 7/Sat 8-Aug**, fallback 14/15-Aug.
- 📏✅🔝 **KILL-PERSIST NOW MEASURED (`a98d15e`)** — `_persist_state` times itself and WARNs ≥1.0s. ⭐ It sits INSIDE `self._lock`, which `is_active()` also takes ⇒ a slow persist stalls the **last-mile order check**, not just `/health`. ⛔ `busy_timeout` UNCHANGED, write stays in the lock (KS9 persist-first is deliberate). Wrap proven non-vacuous by PLANTING.
- 👁️⚠️ **THE SIBLING PATTERN to built-and-never-run: code that RUNS CONSTANTLY and was never MEASURED.** Ask BOTH of anything load-bearing: *has it run?* AND *has it been measured?* A thing can be alive, correct, exercised daily — and still unobserved.
- 🤖 **WATCHMAN: NOT SCHEDULED, never has been** (11 manual runs). ⛔ **Do NOT 'tighten the prompt'** — 2 such rules already exist and are ignored; the mandated `[HH:MM:SS]` format IS the confabulation pressure. **If ever put on cron, post-hoc timestamp verification FIRST.**
- 📣⚠️ **SECONDARY TG CHANNEL NEVER BOUGHT REDUNDANCY** — ONE host, differs only by `chat_id` ⇒ an outage takes BOTH; a hung endpoint leaves it **NEVER ATTEMPTED**. ⭐ **Real redundancy = `ALERT_EMAIL_*` — ABSENT from VM `.env` ⇒ email fallback INERT.**
- ⛔🚨🔝 **`halt.sh` DOES NOT EXIST — it was a hypothetical in an F2 report.** VERIFIED absent from repo, repo HISTORY, VM and PATH. ⚠️ `deploy/resume.sh` DOES exist with no counterpart — the asymmetry INVITES the wrong assumption. **THE ONLY HALT: `ssh trading-vm sudo systemctl stop trading-system`** — it stops entries AND exit management, incl. the 15:17 EOD squareoff.
- ✅🛑 **F2 DROPPED (Rama, 25-Jul) — not deferred.** ⛔ **The 'cheap CLI' is NOT cheap:** separate process + MEMORY-authoritative kill state ⇒ **writing the DB halts NOTHING**; signalling re-enters KS4's RLock mid-operation.
- 📧✅🔝 **OUT-OF-BAND ALERT PATH VERIFIED IN PRODUCTION 25-Jul** — sentinel 21:15:28 → `Delivered` 21:15:58. `alert_watcher` is a LIVE systemd service (up 16-Jul, no `--dry-run`); **`.delivered` is earned** (`future.result()` raises first). ⛔ The notifier's OWN `ALERT_EMAIL_*` fallback is INERT — and it is the one that reads `enabled: true`.
- ✅🔔🔝 **ALL FIVE ALERT-STREAM ITEMS CLOSED 26-Jul (`67df233`·`324be50`·`1bb8809`·`5fc7928`)** — SSH re-baselined (Rama 00:24) + committed fallback fixed · re-alert loop rebuilt on PRESENCE · §C premise **measured & largely REFUTED** · §D answered. `docs/audit/alert_stream_fixes_26jul2026.md`. [[realert-presence-ledger-26jul]]
- 📉🔝 **NOISE RATIO CORRECTED BY MEASUREMENT — the '24 scheduled CRITICALs' was an overcount of the CHANNEL, not the EMAIL.** All 85 sentinels re-rendered through `_build_email`: **16 already say INFO/⚠️**, incl. all 6 `System Manager EOD — clean` (`[LFL836] INFO — …`). ⛔ Nothing downgraded — that would be a change against the evidence.
- ✅⚖️🔝 **CHECK1's label — ANSWERED `CLASSIFY`, and it was ALREADY SHIPPED (v45, 27-Jul 18:17) two hours before the package asking for it was written.** Doc archived → `docs/audit/check1_external_close_decision_27jul2026.md`. ⭐ Candidates are **3, not 6** (SULA/AGARIND predate leg recording; GICRE's ENTRY was CANCELLED). 🔴 **ONLY the `closure_source` backfill is still open.** [[rms-manual-close-is-mislabel-26jul]]
- ⚠️🧯 **LATENT, pinned not fixed: `alert_watcher._build_email` INFERS `CRITICAL` when `context.severity` is absent.** Harmless today; it is how a future scheduled report joins the stream. `test_scheduled_report_severity.py` goes RED if it does.
- 📉⚠️ **SCREENER SCORE IS 45/100 CONSTANT** — 4/10 steps hardcoded `None` (vol+atr→0.0 = 25pts; rsi+sector→0.5 = +10) ⇒ **max ACHIEVABLE score 65**, pass band [60,65]. ⭐ **`min_pass=60` AND tiers calibrated against this instrument** — populating inputs re-tunes gate+tiers+knobs.
- 🛑🔝 **F2 — RECOMMEND: DO NOT BUILD NOW; re-scope as "operator halt semantics"** [`f2_auth_separation_25jul2026.md`]. 5 probes: 1 smaller, 4 bigger. ⭐ Benefit was *halt without SSH*, but a signed body forces a helper script ⇒ real gesture is `ssh ./halt.sh` = `systemctl stop`. Gain is **semantic, not ergonomic**. Cheapest path skips HTTP: a VM **CLI**. ⛔ report, not a decision.
- 🧵✅ **`threads=1` NOT deliberate (unexamined default); raising it is SAFE** [`healthcheck_threads_25jul2026.md`]. In the file's BIRTH commit, uncommented. **No hidden dependency:** `state_store` per-thread, `get_runtime_metrics` lock-guarded + copies, others read-only. ⛔ not changed.
- ⏱️⚠️🔝 **The 30s `busy_timeout` blocks `is_active()` — the LAST-MILE ORDER CHECK, not just `/health`** [`kill_persist_busy_timeout_25jul2026.md`]. `soft_kill` holds `self._lock` across `_persist_state`. **Ceiling never hit** (0 SQLITE_BUSY / 25 kills) but ⚠️ **UNINSTRUMENTED** ⇒ "never ≥30s" proven, "never blocked" NOT.
- 🎛️🔝 **F2's BLOCKER IS NOT AUTH — [`f2_surface_recheck_25jul2026.md`]:** the `:8080` app has **no reference to the live `KillSwitch`** (reads the DB) and `is_active()` returns `self._state` with **no runtime re-read** ⇒ **a route writing the DB row halts NOTHING.** ⚠️ `/health` HMACs `b""` ⇒ its signature is **replayable** — a control route must not copy it. ⚠️ waitress `threads=1`.
- ⚖️ **F2's auto-clear question COLLIDES with Rama's 2026-06-20 HEADLESS GUARANTEE** (`clear_stale_state`: every prior-day kill clears, safety net moved to the EOD report). An operator-halt exemption **REVISES that decision** — argue it as one. Hook exists: `SCHEDULED_KILL_REASONS`.
- ✅🔒🔝 **ALL THREE OWED CALLS ANSWERED 25-Jul + DEPLOYED `488e7e3`:** ShadowTracker **OFF** (`d31759f`; 141 rows stay, marked VOID) · M-A2 deadline **30s→8s, configurable** (`488e7e3`) · **TICK FEED STAYS DORMANT — a DECISION with a reopen trigger** (live-safety dependency, or post-M-S4 exits re-derivation; ⛔ nothing earlier). [[dormant-tick-candle-path-25jul]]
- ✅⏱️🔝 **M-A2 + E1 SHIPPED 25-Jul `cb4c256`; the F2 override covered those TWO items only — gate NORMAL again.** ✅ **A5 ANSWERED: 30 s → 8 s, configurable (`488e7e3`)** — hung endpoint now **[5.0, 1.0] = 8.0 s**; healthy sends untouched. ⚠️ **budget is SHARED across channels — enabling `TELEGRAM_CHANNEL_SECONDARY` doubles the ladder to ~52 s; decide the two together.**
- ❓🔴 **§C `trade_review.txt` — AWAITS RAMA: there is NO such file.** Closest match `candle_data_*.csv` is a **live SOURCE** for the 16:05 report (X3-blocked). Meant `reports/system_manager/<date>.txt`? [[silent-failure-gaps-25jul]]
- 🗳️🔝 **[DECISIONS BOARD → `docs/decisions/00_INDEX.md`](decision_packages_19jul.md)** — **11 items, 10 OPEN** (#09 CLOSED 25-Jul): E4/W10·D1·D2·D3·D4·PerfAlloc(06)·Regime(07)·Freeze(08)·Throttle(10)·🆕**KillLadder(11, 28-Jul — absolute Rs vs ~9.87k: HARD 25.3%, ⛔ do NOT re-tune)**. 2 DECIDABLE NOW (01·08); 11 needs ONE unblocked measurement. [[decision-readiness-triage-19jul]]
- 🔐✅ **[C6 DONE 25-Jul `e8ec604` — auth collapsed to ONE `_authenticate()`](c6_auth_collapse_25jul.md)** — byte-identical; 4 divergences kept (⭐ the EOD early return); RED-first by PLANTING 5/5. **Unblocks F2** (design NOT started). [[c6-auth-collapse-25jul]]
- 🗂️✅ **WAVE-7 TRIAGED** (`wave7_nine_investigation_22jul2026.md`): 45→34 closed · **Tier A EMPTY** (M-O5 deployed 22-Jul `4585bd2`) · 4 inert · 6 ordinary · **M-C2/O4/O7 arm IFF delivery; M-O4 inert (system-only)**. Pushed.
- 🔧✅ **[FIXATION BATCH 24-Jul — DEPLOYED `bc75406`](fixation_batch_24jul_handoff.md)** — M-K2 + §E + F1(CLOSED) + docs SHIPPED; 16:10 verify PASSED; backup clear EXECUTED (76 files/4.73GB). **ONLY §B `capital_snapshot` (boot-gate) remains.** ❌ daily-report DOES heartbeat (19; 25-Jul).
- 🗑️✅ **PRUNE #09 CLOSED 25-Jul `2fadf3a` = Option A, leave as-is, NO code** (2,667 rows vs ~9.9 MB/day is noise). ⚠️ Kept from the refused design: the naive Option-B diff makes the 15:50 job a **permanent no-op** (`EXPIRED`/`DUPLICATE` are NEVER persisted). [[prune-09-design-20jul]]
- 🔐 **2FA seed→VM-only RUNBOOK — written, NOT executed, weekend-only (20-Jul)** — seed hash-identical PC+VM. ⚠️ re-enrol is **ONE-WAY** (no rollback). Path A (delete PC copy, no rotation) = zero risk. `docs/decisions/RUNBOOK_2fa_seed_vm_only.md`. [[token-workflow-confirmed-21jun]]
- 🗄️✅ **DONE/DEPLOYED → [archive](MEMORY_ARCHIVE_2026H1.md)** (links relocated 25-Jul). ⚠️ RAMA: `cleanup.py --live` REMOVED — return as a `scripts/` tool? 6 destructive CTs UNBLOCKED, NOT RUN.
- 🔒🔎 **[AB-910 Ops+Sec audit](ab910_ops_security_audit_16jul.md)** — 5 HIGH, no CRITICAL. OPEN: §2.2 `market_day_only` decorative on 20/25 · §1.2 · §2.1. [[ab910-ops-security-audit-16jul]]
- 🗂️ **BUCKET BOARD (17-Jul):** decision items → the DECISIONS BOARD above · **D** own-run D2 CT-harness (`ct_utils.py:63` LIVE DB); BK-1 ✅ [[bk1-long-short-scanner-17jul]] · **G** ✅ Mon 20-Jul · F1 enforce (Rama) · HARD_KILL = M-C8 · **H** X8 · W1 · **I** T2 · S&R V1.

## Recent Operations — deferred / archive pointers
> 🗄️ **ALL ≤17-Jul Operations → [archive](MEMORY_ARCHIVE_2026H1.md)**: 15/16-Jul blocks · Build History · Crash Tests · 13–14 Jul · ≤09-Jul (Wave-6, PUSH-1, Wave-5, full-repo audit) · V3 Steps 1-10b BUILT+DEPLOYED (`277d63e`). FIRST LIVE HARD_KILL still M-C8's test.
- ★ Deferred (OPEN): **S&R V1 calibration** (data-gated) [[sr_v1_calibration_deferred_30jun]] · **C-2 webhook Ph3** = Rama [[c2_webhook_lockdown_02jul]]
- ★🔝 **SLICE 2.5 DECOMPOSED 26-Jul → `docs/audit/slice25_decomposition_26jul2026.md`** — 16 pieces: **4 PROVEN LIVE 10-Jul**, 2 already correct, **7 never-run (all in the live service)**, 2 not started. ⭐ **T2's same-day leg PASSED; only `--arm-overnight` DDPI left.** ⛔ branch `854112b` UNPUSHED **by design** — do not push/delete. [[handoff-26jul-alert-stream]]
- ✅🩹🔝 **SLICE 2.5's PAPER BLOCKER FIXED 26-Jul `f7eedd3`** — the paper book now reflects the ORDER's product (it was hardcoded `"MIS"`). ⭐ Un-blinded **TWO** mechanisms, paper-only: EOD6/FIX-015 CNC exemption **and H-5's HARD_KILL sweep intent** (a CNC swept as MIS = naked short). Live was always correct. RED-first 8/11, MIS proven unchanged first.
- 🗂️🔝 **SLICE 2.5's 7 NEVER-RUN PIECES CLASSIFIED → `slice25_never_run_pieces_26jul2026.md`** — none "never wired"; 4 loop over an EMPTY collection, 2 have a cold branch, 1 config-gated. ⭐ **Top first-run risk = conditional capital allocation** (untested AND the only one touching intraday capital). ⚠️ Paper can't model the overnight position→holding TRANSITION ⇒ Mon→Tue pair irreducible.
- 📖🔝 **CLOSURE VOCABULARY IS CANONICAL — `core/closure_source.py` + `docs/closure_source_contract.md` (`bc19aab`)** — ⛔ **never restate the literals; a test scans the whole tree.** 2 axes (`closure_source` WHO · `exit_mechanism` HOW). ⚠️ **Contradiction ⇒ CRITICAL, NOT a tie** — precedence orders SILENT sources, never overrules one that SPOKE.
- ✅🔓🔝 **§B/§C/§D of CHECK1+W8 — THE HOLD IS LIFTED AND ALL THREE SHIPPED in v45 (`bc19aab`·`77b8b04`·`10c02ae`·`2f8fd87`·`81f9372`).** ⭐ The §0.3 finding survived the build: at bound 0 `order_placer:2374` still returns, so **CHECK1 emits the INFO itself** — that is what let §C ship without §D. ⚠️ v45 REBUILDS live `trades` at the **28-Jul 08:15** boot; a failed migration blocks the boot.
- 📐🔝 **CHECK1+W8 DESIGN WRITTEN FOR CHATGPT → `docs/audit/check1_w8_design_26jul2026.md`** (⛔ design only, no code). First principle: **suppress only on POSITIVE evidence, never on absence.** 3 defects addressed separately; ⭐ **deferral (not attribution) is what restores the deleted INFO "TARGET HIT"**. W8 vocabulary defined ONCE. **B6 = NO, FIX-183's prepass is still required.** 6 open Qs.

## Relocated from the hot index (27-Jul compaction) — OPEN WORK, verbatim
- 🎨 **[GUI workflow](feedback_gui_redesign_workflow.md) — FOLLOW VERBATIM; its `## Status` names the current screen.** ✅ S08+S09 approved 24-Aug. ⛔ Suite green (2,080) BEFORE the commit. ⛔ **Scanner is dropped app-wide (Rama, 24-Aug)** — it overrides the artwork.
- 🔎 **P3-s14 loop tail** — same defect shape at `webhook_receiver.py:875` (`fetch_one` inside `except IntegrityError` escapes with both claims held); recorded not widened. [[p3s14-done-17jul]]
- 🔬❓ **[W10 workarounds still needed? (23-Jul §D)](w10_workaround_still_needed_23jul.md)** — QUESTION not finding; the double-subtract that justified avoiding the reader is now fixed. Reader-by-reader (recon block STILL must avoid it: RESET_PNL). NOT acted. [[e4-w10-done-17jul]]
- **X3-retirement** (`daily_report` + `fetch_daily_candles`) — BLOCKED on W1 + a Candles/Capital keep-or-lose decision. [[batch3-done-17jul]]
- **S5-tail** — per-job functional criteria for the **7 jobs reading reconciliation/CAPITAL state**; 27 are execution-only. Decide each, never bulk. [[s1s3s5-done-17jul]]

## ⬇️ MOVED FROM HOT (`MEMORY.md`) 28-Jul-2026 — status/open-work, per the placement rule
*The DO-NOTs stayed in HOT; only status and open-work detail came here.*
- 🔁📉 **[SENCO 27-Jul re-entry = POLICY GAP, not a defect](senco_double_entry_27jul.md)** — a continuous ~5-min signal stream held back only by the position guard. ⛔ **Cooldown NOT evidence-backed: n=3** ⇒ the 3-Aug rule WILL bind. ⭐ **Real finding: FIRST entries n=181, win 40.3%.**
- 🆕 **CAREFUL-LOOP fallout — RECORDED not fixed (a):** 3 `event_type` sites · `Rejected (Sizing/Capital)` label · `build_taxonomy_map --config-dir` · wave-7 · W9 webhook-drop · 403-POST count (~338k). [[signal-mortality-census-19jul]] [[q9-batch4-sizing-reachability-18jul]]
- 🆕 **CAREFUL-LOOP fallout — RECORDED not fixed (b):** `position_sizer.py:506` 2× ceiling (latent) · **`eod_cleanup` FK crash 15-Jul, no heartbeat (#09)** · Rs 0.29 SL. [[consecutive-losses-gate-wired-19jul]] [[q9-batch5-post-restart-18jul]]
- ✅ **[S4 BOOT OUTAGE — follow-up ANSWERED 27-Jul: DEGRADE + out-of-band CRITICAL](s4_boot_outage_17jul.md)** — built on `fix-boot-27jul`, UNPUSHED (Thu 30-Jul). [[failfast-vs-degrade-discriminator-27jul]]
- 🧪 **[`test_instance_lock` = a 120s ORPHAN CHILD this class spawns — NOT 'PC-env'](instance_lock_flake_mechanism_27jul.md)** — bare `Popen`, unreaped ⇒ a LIVE holder PID differing each run. ⛔ 'no parallel suites' is sound but INCOMPLETE. Fix queued on `fix-tests-27jul`.
- 🔁🛑 **[NO REDUNDANT WATCHERS (26-Jul)](feedback_no_redundant_watchers.md)** — `run_in_background` **re-invokes on exit**; an `until`-loop waiting on it is waste. ⛔ Kill any watcher **in the turn its result lands**; verify with `Get-Process` (git-bash `ps` can't see Windows procs).
- 🔕⏰ **[No self-wakeups for time-gated pushes](feedback_no_push_wakeups.md)** — an armed wakeup fails SILENTLY if the session is down (no alert, no trace). Instruction-file handoff instead. Proven 23-Jul. [[no-push-wakeups]]
- ▶️ **[26-Jul handoff](handoff_26jul_alert_stream.md)** — §A4 DONE+PASSED; superseded by the 28-Jul handoff in HOT.

## Added 06-Sep-2026 — sandbox replica build
- 🟢🗿 **[SANDBOX REPLICA BUILT + VERIFIED](sandbox_replica_built_06sep.md)** — `ssh trading-sbx` · **a separate Oracle TENANCY**, not just a separate VCN · snapshot **and restore both proven** · gate 18F/6051P (10 = the gemini exclusion working) · ⛔ **`main.py` has never executed
  there** (3 blockers). ⭐ `~/.oci/config` now written ⇒ OCI is scriptable, ⛔ no console.
- 🔬🐛 **[Paper mode requires `WEBHOOK_SECRET` though a test asserts it must not](paper_mode_requires_webhook_secret_06sep.md)** — `test_main.py::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret` fails at `20061b6`; environment-independent. ⛔ **RECORD, DO NOT
  FIX — batch 2.** ⭐ Third blocker on booting the sandbox, but the only one solvable without DR6114 (a throwaway secret is ⛔ not a credential).
