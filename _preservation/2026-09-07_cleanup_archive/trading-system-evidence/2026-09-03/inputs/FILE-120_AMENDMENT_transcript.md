# TRANSCRIPT — FILE 120 (03-Sep-2026), AMENDMENT TO FILE 118

🔴 **PROVENANCE: this is a TRANSCRIPT of the FILE 120 text as received in the
session, ⛔ NOT a copy of an original `.txt`** — no such file exists on this
machine (see `README_PROVENANCE.md`). ⛔ Do not cite this as the original.

---

```
================================================================================
FILE 120 - AMENDMENT TO FILE 118 · FRESH-LIVENESS GATE · PROVENANCE CLOSURE
================================================================================
ISSUED            : 03-Sep-2026 (Thu) IST
MODEL REQUIRED    : Claude Opus 4.6+ · REASONING: HIGH
                    (the post-run ingest in FILE 118 §5 is still ahead and is
                     the heavy part; do NOT downgrade to Sonnet for any part)

PERMANENT FIXATION (Rama protocol #4)
  Read current state -> establish root cause -> modify the EXISTING file. No
  parallel files. FILE 114 §3 stands: ONE run header, not two. The `inputs/`
  files you already wrote are the existing files - amend them, do not re-create
  them under new names.

PARITY FIXATION (Rama protocol #5)
  Investigate before acting. Every value written to the record must be measured
  by a command whose output you captured. Nothing here touches the engine, so
  paper/live parity is not in scope for this file.

MEMORY UPDATE PATHS (mandatory, §6 of this file - do not skip)
  · mempalace (repo)
  · ~/doc/SYSTEM_MAP.md
  · PATHS.md
  · UNPUSHED_PENDING_DEPLOY_LEDGER

SCOPE OF THIS FILE
  FILE 118 REMAINS IN FORCE IN FULL, except at the four points amended in §3
  below. Nothing in the instrument, the scope hook, the gates, the failure
  branches, the §7 conclusion wording, the §8 TREE-advance order or the §9
  memory directive is changed. Do NOT reopen instrument design.

================================================================================
1 - YOUR FILE 118 §2 EXECUTION: REVIEWED IN FULL, ACCEPTED
================================================================================
The five files you wrote were read and checked here, not taken on report.

  · line counts as you stated them: README_PROVENANCE 47 · FILE117_COVERING_NOTE
    48 · FILE-116 transcript 105 · FILE-118 transcript 447 · PRERUN_CHECKS 67.
    All five match. No inflation.
  · the FILE-118 transcript was diffed against the file I issued: 425 lines
    against 425 lines, and every difference is character transliteration
    (em-dash -> hyphen, ellipsis -> three dots, one emoji dropped). No line added,
    no line removed, no clause altered. It is a faithful transcript.
  · §2.1 verified independently here as well: RUN_HEADER computes to
    91f3924932d4619d9acabab338dfdfd0aa58ba10b19cca4b25b423fdad784551, the value
    the manifest carries. Two independent computations now agree.

1.1 - MY ERROR, NOT YOURS: FILE 118 §2.2 WAS UNEXECUTABLE AS WRITTEN
---------------------------------------------------------------------
I instructed you to copy three named `.txt` files into `inputs/`. I never
established that those files existed on that machine. They do not - they exist
as chat-side artifacts on Rama's side. I asserted a filesystem shape without
measuring it, which is the exact failure mode my own standing rules name.

You searched `D:\Projects` and `C:\Users\rama\{Downloads,Desktop,Documents,
OneDrive}` by exact name, by `RAMA_*` / `Reply_to_*` / `*SCOPE-FLAG*` /
`*PRE-RUN*`, and by every `*.txt` modified since 01-Sep; the only hits belonged
to `mcx_data_storage`. You then refused to fabricate a copy and filed labelled
transcripts with a provenance README instead.

  => That is the correct behaviour and it is recorded as correct. A search that
    could have gone red and did is evidence; a copy invented to satisfy an
    instruction would have poisoned the folder permanently.
  => Keep `README_PROVENANCE.md` and the two transcript provenance headers
    exactly as written. Never rename a transcript to look like an original.

1.2 - THE FILE 117 QUESTION IS ALREADY SETTLED BY MEASUREMENT, NOT BY FILE 117
-------------------------------------------------------------------------------
You surfaced the fact that matters: this session's own tests already answered
the control-flow question empirically, before FILE 117 existed.

  · G3 (`STOP_AFTER_C2: true` via the CFG hook) measured S17 and then did NOT
    measure the following route.
  · G4 (`false`) measured it.
  => The mechanism was SHOWN to stop. That is stronger than any reading of the
    source, mine or ChatGPT's.

  => AMEND `FILE117_COVERING_NOTE.md`: promote the G3/G4 measurement to the
    PRIMARY basis for the "no defect" ruling, and demote both FILE 117 §1 and
    FILE 118 §1.2 to concurring readings. The ruling must not depend on a
    document the folder does not contain.
  => Keep the provenance limit paragraph verbatim. Do not describe the note as
    an independent review of FILE 117 - it is not one, and it must never read
    as one.

================================================================================
2 - THE CHRONOLOGY POINT (ChatGPT FILE 119 §4): RESOLVED, WITH THE REASON
================================================================================
ChatGPT flagged your §2.4 liveness timestamp of 13:50:42 IST as possibly
future-dated, on the ground that its own conversation clock read earlier.

That ground does not hold, and the record should say why rather than carry an
unresolved suspicion:

  · A comparison between ChatGPT's session clock and the PC's clock is a
    CROSS-CLOCK comparison. It establishes nothing about either. Two clocks
    disagreeing is not evidence that one measurement was back-dated.
  · Within the PC's own clock the figure is self-consistent. Operands:
        liveness read      13:50:42
        turn footer        "done 1:51 PM"        => 13:51:00
        gap                18 s
        turn length        "Churned for 4m 47s"  => implied start 13:46:13
        13:46:13 <= 13:50:42 <= 13:51:00         => inside the turn window
    Self-consistent, not independently corroborated - same clock produced both
    figures. That is the honest characterisation and it is enough here.

  => VERDICT: no back-dating is indicated. Do not correct, adjust or re-label
    the 13:50:42 figure. It stands exactly as measured.

BUT ChatGPT'S REMEDY IS RIGHT ANYWAY, FOR A DIFFERENT AND BETTER REASON.
The problem is not that 13:50:42 might be false. The problem is that it is
GETTING OLDER. FILE 118 §2.4 required the liveness read to be the LAST action
before handover. It was - and then a full review round happened after it. The
freshness that made it a binding has been spent by the elapsed time, and more
will be spent before Rama actually pastes.

  => The binding is re-established by RE-MEASURING, never by arguing about a
    timestamp. §3.1 makes that a gate.

================================================================================
3 - THE FOUR AMENDMENTS TO FILE 118
================================================================================

3.1 - NEW GATE · FRESH LIVENESS READ IMMEDIATELY BEFORE THE PASTE
------------------------------------------------------------------
Run this again, read-only, no sudo, as the last VM action before Rama pastes -
regardless of the 13:50:42 read already on file:

  systemctl show gui-dashboard  --property=MainPID,ActiveState,NRestarts,ExecMainStartTimestamp
  systemctl show trading-system --property=MainPID,ActiveState,NRestarts,ExecMainStartTimestamp

  Required:
    gui-dashboard  MainPID 1119981 · NRestarts 0 · active · start 03-Sep 13:08:20
    trading-system MainPID 1101999 · NRestarts 0 · active · start 03-Sep 08:15:29

  If gui-dashboard's PID has changed -> STOP. STEP B must be re-established
  before any run; the VM<->browser binding cannot be repaired after the fact.
  If trading-system's PID has changed -> STOP and investigate. Do not restart
  it, do not touch it, under any condition.

  Append the new reading to the EXISTING `PRERUN_CHECKS_03-Sep-2026.md` as a
  second dated block. Do not overwrite the 13:50:42 block - both readings
  stay, so the elapsed gap is visible on the record.

3.2 - NEW RECORD REQUIREMENT · BOTH TIMESTAMPS, GAP VISIBLE
------------------------------------------------------------
The post-run results record must carry, side by side:
  · the timestamp of the final liveness read (§3.1)
  · the run's own start time as printed by the instrument
  · the interval between them, stated plainly

  Do not invent a tolerance for that interval. There is no measured basis for
  one. The record's job is to make the gap visible and auditable, not to
  pronounce it acceptable.

3.3 - AMENDED · FILE 118 §5.6 MANIFEST REGENERATION
----------------------------------------------------
FILE 118 §5.6 said "add the §2.2 / §2.3 input files to the regenerated
manifest." The §2.2 files were never created because they could not be. Replace
that clause with:

  At the post-run regeneration, build SHA256SUMS.txt by COMPUTING IT FROM WHAT
  IS ACTUALLY ON DISK at that moment - never from any list written in an
  instruction file, including this one. Expected to include, at minimum:
    gui_sweep_snippet.js · INSTRUMENT_VALIDATION_03-Sep-2026.md ·
    RUN_HEADER_03-Sep-2026.md · inputs/README_PROVENANCE.md ·
    inputs/FILE117_COVERING_NOTE.md · inputs/FILE-116_SCOPE-FLAG_transcript.md ·
    inputs/FILE-118_PRE-RUN-CLEARANCE_transcript.md ·
    inputs/PRERUN_CHECKS_03-Sep-2026.md · plus any originals Rama has dropped in
    by then · plus the results record itself if it is complete at that point.
  Regenerate ONCE, after the single authorised RUN_HEADER edit. Not before
  the browser run. Not twice.
  Record old and new RUN_HEADER hashes and restate the snippet hash as
  UNCHANGED at 743a7d46..., exactly as FILE 118 §5.6 already requires.

3.4 - AMENDED · THE INPUT SET IS NOW FIVE ARTIFACTS, NOT THREE
---------------------------------------------------------------
The round's artifact set is FILE 116 · FILE 117 · FILE 118 · FILE 119 · FILE 120.
Only Rama can supply the originals; they are chat-side, not on that machine.

  => File a transcript of FILE 119 (ChatGPT's pre-run clearance review) and of
    FILE 120 (this file) into `inputs/`, with the same provenance headers you
    used for 116 and 118.
  => Update the `README_PROVENANCE.md` table to cover all five, showing for each
    whether the folder holds an ORIGINAL or a TRANSCRIPT.
  => When Rama drops the real `.txt` originals in, update the table to show them
    as originals - but do not delete the history of their absence. The record
    of what was missing and when is itself evidence.
  => This is OWED, POST-RUN. It does not block the browser run, and nothing
    manifest-listed may be touched to solve it before the run.

================================================================================
4 - WHAT IS UNCHANGED AND STILL BINDING (do not re-derive, do not relitigate)
================================================================================
  · Instrument FROZEN at 743a7d46.... Do not edit line 53. Do not edit any byte.
  · Scope selected ONLY by: window.__GUI_SWEEP_CFG = { STOP_AFTER_C2: true };
  · No ROUTES / VIEWPORTS / S02_EXPECT / S02_ROUTE overrides. No __present:true.
  · Do not regenerate the manifest before the run. Three OK lines is the pass
    condition; a bare hash string is not what `sha256sum -c` prints.
  · C0 is a hard gate: AUTHENTICATED = TRUE and SELFTEST = PASS, or the route
    results are VOID and S02/S17 are not interpreted at all.
  · C1 vocabulary: COMPARABLE / HEIGHT ONLY / MORE THAN THE HEIGHT MOVED.
    SCROLLBAR-PLAUSIBLE does not exist. No invented tolerance.
  · S14 is a full-sweep TIER-1 control. Not a C0-C2 criterion, not a failure
    if absent, not reportable as passed.
  · Tiers 1/2/3 -> "NOT MEASURED - scope STOP_AFTER_C2 = true".
  · The only acceptable clean conclusion, verbatim:
      "Live deployment verification completed at C2; S02 and S17 verified;
       Tier-2/Tier-3 sweep not measured."
    never "sweep complete" · never "22-screen GUI verified" · never "all 21
    table-bearing screens verified" · never "delta = 0 everywhere".
  · Counts stay apart: campaign 22 screens (21 table-bearing) · 19-Aug baseline
    22 rows · this sweep 21 routes S02-S22.
  · Ingest order FILE 118 §5.1-5.7 unchanged. Verbatim output first, redact only
    token-shaped strings and note each redaction.
  · TREE advance 39292d3 -> 2d08436: record -> report -> THEN separately advance ->
    STOP. Never on a failed or void C0-C2. Never folded into the run turn.
  · Do not touch trading-system. Do not put any credential, TOTP, cookie or
    token into any file, log or report.

================================================================================
5 - EXECUTION ORDER FROM HERE
================================================================================
  5.1  amend FILE117_COVERING_NOTE.md  (§1.2 - G3/G4 promoted)
  5.2  file FILE 119 + FILE 120 transcripts, update README table (§3.4)
  5.3  FRESH liveness read, appended as a 2nd block   (§3.1)  <- LAST
  5.4  report READY to Rama, <=5 lines, carrying the NEW timestamp
  --------------- Rama executes the browser run (FILE 118 §4) ---------
  5.5  ingest per FILE 118 §5.1-5.5, gates per §6
  5.6  single RUN_HEADER edit, then ONE manifest regeneration (§3.3)
  5.7  results record, incl. both timestamps and the gap      (§3.2)
  5.8  report per FILE 118 §10
  5.9  ONLY THEN, separately: TREE advance 39292d3 -> 2d08436 -> STOP
  5.10 memory + ledger (§6 below) - last, and never skipped

  5.3 must be the last VM action before the paste. If anything intervenes
  between 5.3 and the paste, run 5.3 again. Re-measuring is cheap; a broken
  binding is unrecoverable.

================================================================================
6 - MEMORY AND LEDGER · MANDATORY · DO NOT SKIP
================================================================================
Everything FILE 118 §9 requires still applies, PLUS these, added this round:

  mempalace
    · RULE (new, standing): never instruct or accept a file COPY whose existence
      on the target machine has not been measured. Search first, report the
      search space, and file a labelled transcript rather than fabricate an
      original. Absence recorded is evidence; absence papered over is not.
    · RULE (new, standing): a cross-clock comparison is not evidence of
      back-dating. Freshness of a VM<->browser binding is established by
      RE-MEASURING immediately before handover, never by arguing about a
      timestamp. Both readings stay on the record so the gap stays visible.
    · RULE (new, standing): a manifest is computed from disk at regeneration
      time, never transcribed from a list in an instruction file.
    · FACT: the STOP_AFTER_C2 short-scope mechanism is settled EMPIRICALLY by
      this session's G3 (stopped after S17) and G4 (continued) - not by any
      reading of the source. FILE 117 §1 and FILE 118 §1.2 concur; neither is
      the basis.
    · FACT: FILE 118 §2.2 was issued unexecutable by Web Claude; VS Code
      correctly refused to fabricate and filed labelled transcripts instead.
    · OPEN: provenance gap - the five round originals are chat-side only; owed
      into `inputs/` by Rama, post-run, non-blocking.

  ~/doc/SYSTEM_MAP.md · PATHS.md · UNPUSHED_PENDING_DEPLOY_LEDGER
    · as FILE 118 §9, plus `inputs/` recorded in PATHS.md, plus the provenance
      gap and the CFG-hook hardening item carried OPEN in the ledger.
    · Carry the standing nightly engine-stop obligation forward every session
      until F6 lands. A missed Friday stop costs Monday's entries.

Do not report any memory path as updated unless you performed and verified
the write. Claiming a memory update you did not make is the one failure that
corrupts every future session.

================================================================================
7 - REPORT-BACK
================================================================================
PRE-RUN, <=5 lines: (a) covering note amended · (b) FILE 119/120 filed + README
updated · (c) FRESH liveness PID/NRestarts/state and its timestamp · (d) engine
unchanged · (e) the scope line to paste, then the file unchanged.
POST-RUN: exactly as FILE 118 §10.

a cross-clock disagreement != back-dating
a transcript != the original
a quotation != the document
a stale binding != a broken one - but only re-measuring tells you which
an unmeasured tier != a passed tier

================================================================================
END OF FILE 120
================================================================================
```

---

## Execution note attached at filing time
- ⭐ §5.1 done — `FILE117_COVERING_NOTE.md` amended: **G3/G4 promoted to PRIMARY
  basis**; FILE 117 §1 and FILE 118 §1.2 demoted to **concurring readings**;
  ⭐ provenance-limit paragraph kept verbatim; ⭐ an explicit *"this is not an
  independent review of FILE 117"* clause added.
- 🔴 §5.2 **partially executable only** — ⛔ **FILE 119 does not exist on this
  machine and was never read here.** ⭐ A transcript of it is impossible.
  📄 `FILE119_ABSENT.md` records the absence in its place.
