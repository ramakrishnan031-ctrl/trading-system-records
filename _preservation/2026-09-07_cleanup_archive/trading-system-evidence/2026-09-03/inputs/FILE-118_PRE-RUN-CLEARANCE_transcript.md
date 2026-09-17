# TRANSCRIPT — FILE 118 (03-Sep-2026), PRE-RUN CLEARANCE · POST-RUN INGEST · C0–C2

🔴 **PROVENANCE: this is a TRANSCRIPT of the FILE 118 text as received in the
session, ⛔ NOT a copy of `RAMA_03-Sep-2026_FILE-118_PRE-RUN-CLEARANCE.txt`** —
that file does not exist on this machine (see `README_PROVENANCE.md`). ⛔ Do not
cite this as the original artifact.

---

```
================================================================================
FILE 118 — PRE-RUN CLEARANCE · POST-RUN INGEST PROTOCOL · C0–C2
================================================================================
ISSUED            : 03-Sep-2026 (Thu) IST
MODEL REQUIRED    : Claude Opus 4.6+ · REASONING: HIGH
                    (record integrity + hash custody + failure-branch logic;
                     do NOT downgrade to Sonnet for any part of this file)

PERMANENT FIXATION (Rama protocol #4)
  Before adding or modifying ANY operational file (.py / .md / .json / db /
  config / evidence artifact): read the current state -> establish the root
  cause of the change -> modify the EXISTING file. Do not create a parallel
  file. FILE 114 §3 stands: ONE run header, not two.

PARITY FIXATION (Rama protocol #5)
  Investigate before acting. Every claim written into the evidence record must
  be a MEASURED value from the actual console output or from a command you
  ran. No expected value is ever written as if it were observed. Paper/live
  parity is not in scope for this file - nothing here touches the engine.

MEMORY UPDATE PATHS (mandatory, §9 of this file - do not skip)
  · mempalace (repo)
  · ~/doc/SYSTEM_MAP.md
  · PATHS.md
  · UNPUSHED_PENDING_DEPLOY_LEDGER

================================================================================
0 - STATE ON RECEIPT OF THIS FILE
================================================================================
Received and reviewed in full: FILE 116, your reply (Output-trading_system),
the corrected RUN_HEADER_03-Sep-2026.md, SHA256SUMS.txt, and ChatGPT's
FILE 117 reply.

FACTS ON RECORD (source shown; nothing below is inferred):
  · gui-dashboard  : PID 1119981 · start Thu 03-Sep 13:08:20 IST · NRestarts 0
                     · active/running                    [RUN_HEADER §A2]
  · previous       : PID 1019239 · start Wed 02-Sep 06:19:53 IST
  · trading-system : PID 1101999 · start Thu 03-Sep 08:15:29 IST · NRestarts 0
                     · UNTOUCHED and must stay untouched [RUN_HEADER §A2]
  · bare refs/heads/main = 2d084364b830aca83b6d5cd3f2db21100372f446
  · deployed work-tree vs that tree = 0 differing tracked files
  · controls.py / control_client.py mtime 02-Sep 23:39:55; process start
    03-Sep 13:08:20 -> 13h28m25s later. CPython imports once per process =>
    this process holds the deployed modules.
  · instrument     : gui_sweep_snippet.js
                     743a7d461f8a171e228fd8d9d2ffce1fe0c59642f8408569ad3ff80fb10bec93
                     UNCHANGED, byte-identical, hash independently verified.
  · route table    : 21 routes (S02-S22, S01 absent)
  · S02_EXPECT     : { h: 1212, ovf: false, sub13: 0 } · historical cw NOT recorded

STATUS: STEP B = PASS · HASH = PASS · RECORD CORRECTIONS = PASS ·
        INSTRUMENT = READY · SCOPE HOOK = READY.
The only missing evidence is the actual console output.

================================================================================
1 - FOUR FINDINGS THIS ROUND
================================================================================

1.1 - MANIFEST CURRENCY: CHECKED AND CLEARED (measured, not assumed)
------------------------------------------------------------------
The risk was real and specific: you EDITED RUN_HEADER_03-Sep-2026.md (+19 / -1
lines) after SHA256SUMS.txt was quoted. If the manifest had been generated
BEFORE that edit, step 1 of the run (`sha256sum -c SHA256SUMS.txt`) would print
a FAILED line and Rama would be staring at a verification failure seconds
before pasting.

It was verified, not assumed. SHA-256 of the corrected RUN_HEADER as it stands:

  computed : 91f3924932d4619d9acabab338dfdfd0aa58ba10b19cca4b25b423fdad784551
  manifest : 91f3924932d4619d9acabab338dfdfd0aa58ba10b19cca4b25b423fdad784551
  VERDICT  : MATCH

=> The manifest was regenerated AFTER the corrections. It is current. Nothing to
fix. Recorded here so this is not re-raised, and so the discipline is on file:
an edited artifact invalidates any manifest written before the edit, every
time. This one happened to be clean.

  NOTE: this check covers the RUN_HEADER line only. The snippet line was
  independently verified by you. INSTRUMENT_VALIDATION_03-Sep-2026.md has not
  been independently checked by anyone in this cycle - `sha256sum -c` covers it
  at run time. All three lines must read OK.

1.2 - FILE 117 (ChatGPT) IS INTERNALLY CONTRADICTORY - ANNOTATE ON FILING
--------------------------------------------------------------------------
The document's TITLE and PREAMBLE assert a defect:
  "CRITICAL STOP_AFTER_C2 CONTROL-FLOW FINDING"
  "...the advertised STOP_AFTER_C2=true short run does NOT actually stop the
   sweep at C2."

Its own §1 then WITHDRAWS that assertion in full:
  "...the `break` targets the enclosing ROUTES loop, not the viewport loop... the
   short-scope mechanism is structurally valid. My earlier concern about an
   inner-loop break would be incorrect for this exact uploaded file; it does
   not apply."

The preamble is stale text from an earlier draft. The OPERATIVE RULING is §1
onward: NO DEFECT · NO SNIPPET MODIFICATION · SCOPE HOOK IS CORRECT.

  => File FILE 117 VERBATIM. Do not edit ChatGPT's artifact.
  => Write a SEPARATE covering note beside it recording that the title/preamble
    is superseded by its own §1, and that the operative ruling is "no defect".
  => Reason this matters: an evidence folder that contains a headline claiming a
    critical instrument defect, filed without annotation, will be read in four
    days' time as an unresolved defect. The annotation is the record's defence.

1.3 - S14 IS WITHDRAWN FROM THE C0-C2 SCOPE (correction to FILE 116 §3)
------------------------------------------------------------------------
FILE 116 §3 carried: "Expect and do not misread: S14 overflow PRESENT = PASS."
That expectation belongs to the FULL sweep. ChatGPT §13 is correct and FILE 116
is corrected here: with STOP_AFTER_C2 = true the run answers C0 -> C1 (S02) ->
C2 (S17) and breaks. S14 is a TIER-1 corroboration control for the full sweep.

  => S14 is NOT a criterion for this run.
  => Do NOT invent it as a C2 requirement.
  => Do NOT report its absence as a failure.
  => If the short run's output happens to contain an S14 row at all, record it
    as observed data and gate nothing on it.
  => The S14 negative control is deferred to the later full sweep, where
    "overflow PRESENT and ~tens" remains the PASS condition.

1.4 - WHAT `sha256sum -c` ACTUALLY PRINTS (correction to FILE 116 §3 step 1)
-----------------------------------------------------------------------------
FILE 116 wrote "-> must read 743a7d46...". That is wrong about the output shape.
`sha256sum -c SHA256SUMS.txt` prints one line PER FILE:

  gui_sweep_snippet.js: OK
  INSTRUMENT_VALIDATION_03-Sep-2026.md: OK
  RUN_HEADER_03-Sep-2026.md: OK

  => THREE "OK" lines is the pass condition. Any "FAILED" line => STOP, do not
    run, report which file failed. The bare hash string is not what appears.

================================================================================
2 - PRE-RUN TASKS · DO THESE NOW · READ-ONLY, NOTHING HASHED MAY CHANGE
================================================================================
GOVERNING RULE FOR §2: the three manifest-listed files are FROZEN until the
console output arrives. Any edit to any of them re-opens the verify-then-edit
contradiction FILE 116 caught. Freeze them. All §2 work happens OUTSIDE them.

TASK 2.1 - Verify the manifest on disk (read-only)
  cd D:\Projects\trading-system-evidence\2026-09-03
  sha256sum -c SHA256SUMS.txt
  Expected: three OK lines (§1.4). Capture the verbatim output to a scratch
  note - NOT into any manifest-listed file.
  If any line reads FAILED -> STOP. Do not hand over. Report the failing file.

TASK 2.2 - File the round's inputs (additive only)
  Create D:\Projects\trading-system-evidence\2026-09-03\inputs\ if absent, and
  copy in, unmodified:
    · RAMA_03-Sep-2026_FILE-116_SCOPE-FLAG.txt
    · Reply_to_Web_Claude_FILE117_Scope_Control_Final_03Sep2026.txt
    · RAMA_03-Sep-2026_FILE-118_PRE-RUN-CLEARANCE.txt   (this file)
  Anti-duplication check first: if any already exists, verify it is identical
  and do not write a second copy under a new name.

TASK 2.3 - Write the FILE 117 covering note
  New file: inputs\FILE117_COVERING_NOTE.md
  Contents (short, factual, no editorialising):
    · what the title/preamble claims
    · what §1 rules
    · which one is operative (§1)
    · consequence: no snippet modification; scope hook stands
  Do NOT add these two files to SHA256SUMS.txt yet. The manifest is
  regenerated ONCE, post-run, in §5.6.

TASK 2.4 - Confirm liveness immediately before handover (read-only, no sudo)
  systemctl show gui-dashboard  --property=MainPID,ActiveState,NRestarts,ExecMainStartTimestamp
  systemctl show trading-system --property=MainPID,ActiveState,NRestarts,ExecMainStartTimestamp
  Gates:
    gui-dashboard  MainPID must still be 1119981 · NRestarts 0 · active
    trading-system MainPID must still be 1101999 · NRestarts 0 · active
  If gui-dashboard's PID has changed, STEP B must be re-established before the
  run - the sequence (PID confirmed FIRST, snippet SECOND) is the only binding
  between the VM evidence and the browser evidence, and it cannot be repaired
  after the fact.
  Do not restart, reload, stop or touch trading-system under any condition.

TASK 2.5 - Report READY to Rama in five lines or fewer
  Lines: manifest 3xOK · gui PID + NRestarts · engine PID unchanged · scope
  line to paste · "paste the file unchanged". Nothing else.

================================================================================
3 - PROHIBITIONS FOR THIS ROUND
================================================================================
Do not edit gui_sweep_snippet.js. Not line 53, not anything. It is hash-
   verified and the CFG hook already gives the short scope.
Do not edit RUN_HEADER_03-Sep-2026.md before the run (§2 governing rule).
Do not add `__present: true`. Not needed for a scope-only run.
Do not pass ROUTES, VIEWPORTS, S02_EXPECT or S02_ROUTE through the CFG hook.
   Those are measurement-definition overrides and they can run SILENTLY -
   that hazard is recorded and is exactly why the hook stays scope-only.
Do not open another instrument-design cycle. ChatGPT §20 is explicit: only a
   real defect surfaced by the real run reopens design.
Do not touch the engine service.
Do not write password, TOTP, session cookie or bearer token into any file,
   any log, or any report. If the console output contains a token-shaped
   string, redact it in the record and say so.
Do not combine the TREE advance with the browser run (§8).

================================================================================
4 - THE RUN · RAMA EXECUTES · YOU DO NOT
================================================================================
  1  cd D:\Projects\trading-system-evidence\2026-09-03
     sha256sum -c SHA256SUMS.txt          -> three OK lines
  2  log in to the dashboard normally; land on a real dashboard page on the
     dashboard's OWN origin
  3  keep that tab visible and FOCUSED
  4  DevTools -> Console, paste this line ALONE and press Enter:

         window.__GUI_SWEEP_CFG = { STOP_AFTER_C2: true };

  5  then paste gui_sweep_snippet.js UNCHANGED
  6  KEEP THE TAB FOCUSED until it prints END
  7  copy the COMPLETE console output back (also retained in window.__GUI_SWEEP)

  For the full sweep instead: paste the file alone, no CFG line. The default of
  STOP_AFTER_C2 is already false.

ASCII - EXECUTION SHAPE UNDER STOP_AFTER_C2 = true
  +--------------------------------------------------------------+
  | C0   AUTHENTICATED + SELFTEST                                |
  |  |                                                            |
  |  +- FAIL ---------------------------> VOID the run, stop     |
  |  v                                                            |
  | C1   S02 @1920x1080 -> @1440x900                             |
  |  |                                                            |
  |  +- MORE THAN THE HEIGHT MOVED -----> instrument halts, stop |
  |  v                                                            |
  | C2   S17 @1920x1080 -> @1440x900                             |
  |  |                                                            |
  |  v   break outer ROUTES loop                                 |
  | INTEGRITY summary -> END                                     |
  +--------------------------------------------------------------+
  Verified by ChatGPT against the uploaded file: the `break` sits AFTER the
  inner viewport loop closes, so it targets the ROUTES loop. Structurally sound.

================================================================================
5 - POST-RUN INGEST · ON RECEIPT OF THE CONSOLE OUTPUT
================================================================================
Work strictly in this order. Do not skip a step, do not batch them.

5.1  Paste the console output into the record VERBATIM and UNABRIDGED first,
     before interpreting anything. Redact only token-shaped strings, and note
     each redaction.

5.2  C0 GATE - hard.
       AUTHENTICATED must read TRUE.
       SELFTEST must read PASS.
     Either one failing => the route results are VOID. Do not interpret S02 or
     S17. Report the failure and stop.

5.3  C1 - S02 @1920x1080. Record every field the instrument printed:
       h · sw · cw · scrollbarPx · OVF · sub13 · clipped · authentication ·
       focus/visibility · settle status · verdict · magnitudes
     Historical reference: h = 1212 · ovf = false · sub13 = 0 · cw NOT RECORDED.
     Verdict vocabulary - the ONLY three the Round-3 instrument emits:
       COMPARABLE / HEIGHT ONLY / MORE THAN THE HEIGHT MOVED
     SCROLLBAR-PLAUSIBLE does not exist. Never write it.
     If HEIGHT ONLY, the recorded wording is exactly:
       "the deviation is plausibly associated with client-width / scrollbar
        reflow but is not fully resolvable against the historical record
        because historical cw was not recorded."
     If MORE THAN THE HEIGHT MOVED, the instrument halts by design - stop,
     record, report. Do not continue to C2.
     Do not invent a tolerance. Use the printed magnitudes.

5.4  C2 - S17, only if C1 permits continuation. S17 is the deployment-specific
     check: the relevant backend modules were ABSENT at 39292d3 and PRESENT in
     the deployed tree, so a clean S17 under PID 1119981 is the evidence that
     the restarted GUI is serving the refitted path. Record all fields as 5.3.

5.5  INTEGRITY - record every LOGINPAGE / UNFOCUSED / error row. If any is
     present, it is reported, not smoothed over.

5.6  Fill RUN_HEADER_03-Sep-2026.md in ONE edit (the header is unfrozen only
     now). Required:
       §B  every pending marker replaced by a measured value: origin · browser
           version · DPR · requested vs measured viewport · AUTHENTICATED ·
           SELFTEST · C1 verdict · C1 magnitudes · INTEGRITY · scope flag
       §B  scope row must read: STOP_AFTER_C2 = true (C0-C2)
       §D  TIER 1 / TIER 2 / TIER 3 must each be marked
           "NOT MEASURED - scope STOP_AFTER_C2 = true"
           and a line added: "S14 is a TIER-1 control of the full sweep and is
           not a criterion of this run."
     Then regenerate SHA256SUMS.txt ONCE, and record inside the results file:
       old RUN_HEADER hash 91f3924932d4619d9acabab338dfdfd0aa58ba10b19cca4b25b423fdad784551
       new RUN_HEADER hash <computed>
       reason: post-run results entry, authorised
       gui_sweep_snippet.js hash UNCHANGED at 743a7d46... - restate explicitly
     Add the §2.2 / §2.3 input files to the regenerated manifest at this point.

5.7  Write the results record to D:\Projects\trading-system-evidence\2026-09-03\
     containing, at minimum:
       run timestamp (IST) · gui-dashboard PID + start · trading-system PID +
       start (unchanged) · deployed tree reference 2d084364... · 0 differing
       tracked files · instrument SHA-256 · origin · browser version · DPR ·
       requested and measured viewport · AUTHENTICATED · SELFTEST · S02 result ·
       S17 result · INTEGRITY · exact scope flag · complete console output
     Never record an expected value as if it were observed.

================================================================================
6 - GATES AND FAILURE BRANCHES
================================================================================
  SELFTEST fail            -> VOID · stop · investigate
  AUTHENTICATED fail       -> VOID · stop · investigate
  S02 halts                -> stop · record magnitudes · report
  S17 fail                 -> stop · record · report
  INTEGRITY suspect row    -> stop · record · report
  gui PID != 1119981 pre-run-> STEP B re-establish before any run

Do not continue into the remaining routes to "see if the rest is fine". A
deployment failure buried under 19 more routes is a deployment failure you have
made harder to find. The purpose of this run is one question: is the restarted
GUI serving the deployed tree.

================================================================================
7 - THE ONLY ACCEPTABLE CONCLUSION WORDING ON A CLEAN C0-C2
================================================================================
  "Live deployment verification completed at C2; S02 and S17 verified;
   Tier-2/Tier-3 sweep not measured."

never "sweep complete"
never "22-screen GUI verified"
never "all 21 table-bearing screens verified"
never "full visual revalidation"
never "delta = 0 everywhere" - there is no complete everywhere to compare to

COUNTS - keep apart, never merge:
  historical campaign   : 22 screens approved, 21 table-bearing (S01 has no table)
  19-Aug baseline table : 22 rows, S01 included (h=1080 · ovf=no · <13px=2)
  this sweep            : 21 routes, S02-S22, S01 excluded
Wording for the historical gap (FILE 113 §4): "the historical campaign
validation is not independently reproducible from the repository today."
NOT "the campaign was invalid" · NOT "the measurements were false."

================================================================================
8 - TREE ADVANCE · SEPARATE ACT · AFTER RECORD AND REPORT
================================================================================
Order is fixed and not negotiable:
   record  ->  report to Rama  ->  THEN, separately, TREE advance
   39292d3 -> 2d08436  ->  STOP.
Do not fold the advance into the browser-run turn.
Do not advance on a failed or void C0-C2.
Authorisation note: the TREE advance to 2d08436 is contingent on a clean C0-C2.
If C0-C2 is not clean, the advance does not happen and is re-requested from
Rama in his own words.

================================================================================
9 - MEMORY AND LEDGER UPDATE · MANDATORY · DO NOT SKIP
================================================================================
Update ALL FOUR at the end of this round:

  mempalace
    · STEP B closed: gui-dashboard PID 1119981 · 03-Sep 13:08:20 · NRestarts 0
    · stale-process blocker closed
    · instrument gui_sweep_snippet.js frozen at 743a7d46...; scope selected via
      window.__GUI_SWEEP_CFG = { STOP_AFTER_C2: true } - CFG hook is scope-only
    · KNOWN HAZARD (open, not fixed): CFG hook can override ROUTES /
      S02_EXPECT / S02_ROUTE / VIEWPORTS silently; "TEST CONFIG ACTIVE" banner
      only fires when the caller volunteers __present: true. Future revision:
      make any measurement-affecting override self-announce or be rejected in
      production mode.
    · RULE (new, standing): editing any artifact invalidates a manifest written
      before the edit. Regenerate and re-issue, or do not edit. Verify-then-edit
      is not verification.
    · RULE (new, standing): a scope flag changes WHAT WAS MEASURED, therefore
      every unmeasured tier must be labelled NOT MEASURED in the record, never
      left blank and never inferred.
    · S14 is a full-sweep TIER-1 control, not a C0-C2 criterion.
    · FILE 117 title/preamble superseded by its own §1: no STOP_AFTER_C2 defect.

  ~/doc/SYSTEM_MAP.md
    · gui-dashboard service: current PID/start, deployed tree 2d084364...,
      0 differing tracked files, controls.py + control_client.py present in the
      deployed tree and absent at 39292d3.

  PATHS.md
    · D:\Projects\trading-system-evidence\2026-09-03\  (evidence root)
    · D:\Projects\trading-system-evidence\2026-09-03\inputs\  (round inputs)

  UNPUSHED_PENDING_DEPLOY_LEDGER
    · TREE advance 39292d3 -> 2d08436 - PENDING, contingent on clean C0-C2
    · CFG-hook hardening - OPEN, deferred, not scheduled
    · Tier-2 / Tier-3 full sweep - NOT MEASURED, outstanding
    · STANDING NIGHTLY OBLIGATION (until F6 lands): the engine service is
      stopped manually by Rama each trading night. Carry it in the ledger every
      session; a missed Friday stop costs Monday's entries.

Read the ledger at session start and before every off-market push window.

================================================================================
10 - REPORT-BACK FORMAT
================================================================================
PRE-RUN  : five lines or fewer (§2.5).
POST-RUN : (a) C0 verdict · (b) C1 S02 verdict + magnitudes · (c) C2 S17
           verdict · (d) INTEGRITY rows · (e) the §7 conclusion sentence,
           verbatim, or the failure branch taken · (f) files written ·
           (g) old and new RUN_HEADER hashes · (h) memory paths updated.
No prose beyond that. Every number quoted must be traceable to the pasted
console output or to a command whose output you captured.

================================================================================
IMPLEMENTATION ORDER · DEPENDENCIES
================================================================================
  §2.1 manifest verify        -> blocks everything
  §2.2 file inputs            -> independent, additive
  §2.3 covering note          -> depends on §2.2
  §2.4 liveness confirm       -> must be the LAST thing before handover
  §2.5 report READY           -> depends on §2.1 + §2.4
  [ Rama executes §4 ]
  §5.1-5.5 ingest and gate    -> depends on the console output existing
  §5.6 header + manifest      -> depends on §5.1-5.5 complete
  §5.7 results record         -> depends on §5.6
  §8   TREE advance           -> depends on §5.7 AND a clean C0-C2 AND report sent
  §9   memory + ledger        -> last, and never skipped

verifying a hash then editing the file != verification
a default != the recommended scope
21 routes != 22 screens
a stale preamble != a ruling
an unmeasured tier != a passed tier

================================================================================
END OF FILE 118
================================================================================
```

---

## Execution note attached at filing time
- 🔬 **§2.1 result:** three `: OK` lines, `rc=0`. 🔬 RUN_HEADER computed
  independently as `91f39249…` — **matches** FILE 118 §1.1.
- 🔴 **§2.2 could not be executed as written** — 🔬 none of the three named
  `.txt` files exists on this machine. ⭐ Transcripts filed instead, labelled.
  📄 `README_PROVENANCE.md`.
- 🔴 **§2.3 written, but FILE 117 itself is ABSENT** and was never read here;
  ⭐ the note is sourced only from FILE 118 §1.2's quotations.
