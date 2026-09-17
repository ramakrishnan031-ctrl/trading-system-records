PRE-REGISTERED PREDICTION -- 17-Sep-2026 18:00 IST CRON-DRIFT RUN -- testing VM trading-sbx (130.210.13.114)
==========================================================================================================

STATUS : PREDICTION. NOT AN OBSERVATION. Written 17-Sep-2026 ~10:03 IST, before the 18:00 run.
         Plain ASCII on purpose: it can be printed on any console without an encoding crash.
         DO NOT EDIT. Its size and md5 are recorded in docs/SYSTEM_MAP.md
         (RESULT-CRON-DRIFT-1800-PREDICTION-FROZEN-17SEP2026), in PATHS.md and in the
         current manifest. The classification of the 18:00 output is written ELSEWHERE,
         quoting the OBSERVED bytes, never copying a line from this file. A miss is
         recorded as a miss. This file contains no observed result for 17-Sep 18:00.
SOURCE : the 17-Sep card "BOTH CORRECTIONS ACCEPTED - FREEZE THE 18:00 PREDICTION BEFORE
         18:00 - GATE 9", section 2.
AUTHOR : Part A = the card author (verbatim). Parts B and C = VS Code Claude, from code
         and records read before 18:00.


------------------------------------------------------------------------------
PART A -- THE CARD'S PREDICTION, VERBATIM (em dashes rendered as "--"; nothing else changed)
------------------------------------------------------------------------------

    EXPECTED CRITICALs tonight from cron drift:
      1. standing -- 5 missing gemini_* jobs (pre-existing, predates today)
      2. expected -- hand-added evaluator line absent from cron_registry.yaml

    ANY CRITICAL THAT IS NEITHER OF THESE IS A GENUINE NEW CRITICAL
    and is investigated, not absorbed into "expected drift noise".


------------------------------------------------------------------------------
PART B -- THE SAME PREDICTION, RESOLVED TO IDENTITIES, SINKS AND UNITS
------------------------------------------------------------------------------

B0. PREMISES. If any of these differs when the 18:00 output is classified, the premise
    changed: record that, and do not reinterpret the prediction around it.
    - the run   : crontab line 136
                  0 18 * * 1-5 cd /home/ubuntu/systems/trading-system && set -a && . ./.env && set +a && PYTHONPATH=. /home/ubuntu/systems/venv/bin/python scripts/check_cron_drift.py >> logs/cron-drift-check.log 2>&1
    - live crontab (user ubuntu, `crontab -l`): 151 lines, md5 d0b9a184da7dc8aeea507f7dc80d7073
                  (read 17-Sep 09:54:15 and again ~10:00; same md5 as 09:17:02 and 09:21:33)
    - VM config/cron_registry.yaml   : 27,116 B, md5 ae9b22a15e69ca786c718c9c893a3ca4
                  (= the 970aabf blob except 4 lines: --account LFL836 -> VBB097; 0 lines contain "sr_shadow")
    - VM scripts/check_cron_drift.py : 11,396 B, md5 3d43f51c1b92b2d697389bcdd735c01a
                  (= the 970aabf blob 0bb75e4afefea9a2249a9443314a54e8 with CRLF line endings:
                   `diff --strip-trailing-cr` = 0 lines; control without the strip = differs)
    - VM scripts/generate_crontab.py : md5 564adf9c1cb9da9c8754f255bca6cfbd (= the 970aabf blob)
    - VM core/logger.py              : md5 24fe535dd6f410bcb1c52c31a5f266aa (= the 970aabf blob)

B1. SINKS -- where the 18:00 result can and cannot be observed (by origin)

    S1  logs/cron-drift-check.log on the VM -- stdout of print(msg), via the cron redirect.
        THE COUNTED POPULATION for this prediction.
        Pre-18:00 state: 12,347 B, 248 lines, mtime 2026-09-16 18:00:02.631433374 +0530,
        md5 a35fd44ba983b3ccf6b964d27e018ccb -- identical before and after the copy; preserved as
        _preservation/CRON_DRIFT_CHECK_LOG_trading-sbx__pre-1800_17-Sep-2026__captured_2026-09-17T1000IST.log
        Tonight's population = the bytes AFTER the first 12,347, valid only while those
        first 12,347 bytes still hash to a35fd44ba983b3ccf6b964d27e018ccb.

    S2  Telegram -- notifier.send_alert(msg, level="CRITICAL") (check_cron_drift.py:203-208).
        A sink, NOT counted here: the channel is not read from this machine.

    S3  logs/system_2026-09-17.log -- the E4.10 whole-day population.
        PREDICTED TO RECEIVE NOTHING FROM THE 18:00 RUN.
        Code: the process attaches no log handler. get_logger() attaches none
        (core/logger.py:266-270); handlers are attached only inside setup_logging(), whose only
        non-test caller is main.py:2178. Searched core/, alerts/, utils/, scripts/cron_officer.py,
        scripts/generate_crontab.py in the 970aabf and e7bf477 trees: no module-level handler
        setup; the one lazy import (cron_officer.py:525 -> scripts/output_retention.py) configures
        logging only inside main() (:277), and to stderr. Transitive imports beyond those were not
        enumerated -- the 16-Sep measurement below covers the real process.
        Its one INFO line (check_cron_drift.result, :198) therefore has no handler; WARNING+ would
        reach stderr, i.e. S1, never S3.
        Measured, 16-Sep: the 18:00 run happened (S1 mtime 18:00:02.631) while
        logs/system_2026-09-16.log was last written 17:35:05.546 ("Shutdown complete") at
        16,798,379 B -- the Gate 2 baseline size -- with 0 lines containing "check_cron_drift" and
        0 containing "CRON INTEGRITY" (15-Sep: 0 and 0). Positive control, same grep on the same
        file: "Shutdown complete" = 1.
        => The 18:00 drift CRITICAL is predicted NOT to be part of E4.10's CRITICAL count, whether
           the full-day log is captured before or after 18:00.

    S4  cron_heartbeat row "check_cron_drift" (record_heartbeat, :216-221) -- completion
        evidence only; not counted.

B2. THE PREDICTED S1 BLOCK, if B0 holds

    - EXACTLY ONE header line, severity CRITICAL:
          [VBB097] CRON INTEGRITY CRITICAL
    - the section  <U+1F534> ENABLED in registry, ABSENT from live crontab (CRITICAL):
      with EXACTLY these five items, in this order:
          - gemini_premarket_brief (08:55 Mon-Fri)
          - gemini_log_review (16:20 Mon-Fri)
          - gemini_trade_coach (16:40 Mon-Fri)
          - gemini_data_integrity_check (17:00 Mon-Fri)
          - gemini_weekly_patterns (18:00 Sunday)
      = IDENTITY 1 (card item 1). The same five, in the same order, as each of the last five
        CRITICAL blocks in S1 (the last dated 16-Sep 18:00:02 by the file's mtime; the earlier
        four are undated -- position is an ordering fact, not a date).
    - NO section "Live crontab line no longer parses (CRITICAL):"     (unparseable = 0)
    - NO section "Personal-tooling job absent from live (WARN):"       (absent_warn = 0)
    - NEW versus 16-Sep, the section
          <U+1F195> Live job NOT in registry <U+2014> RAN_UNVERIFIED (needs registry entry + contract):
      with EXACTLY ONE item, the evaluator line (crontab line 151):
          - 5 16 * * 1-5 cd /home/ubuntu/systems/trading-system && set -a && . ./.env && set +a && PYTHONPATH=. /home/ubuntu/systems/venv/bin/python scripts/sr_shadow_evaluate.py >> logs/cron-sr-shadow-evaluate.log 2>&1
      = IDENTITY 2 (card item 2) -- BUT CLASSED RAN_UNVERIFIED, WHICH THE CODE CALLS
        INFORMATIONAL. IT IS NOT A CRITICAL-CLASS ITEM AND DOES NOT MAKE THE BLOCK CRITICAL.
        Code: a live line that parses and resolves to a job name absent from the registry goes
        to `unregistered`; has_critical = absent_critical or unparseable
        (check_cron_drift.py:93-95, :114-121). The line parses (env_wrapper python, log_target
        ">> logs/cron-sr-shadow-evaluate.log 2>&1", no marker) and resolves to
        "sr_shadow_evaluate"; the comment line 150 is skipped (_command_lines skips "#").
        Contrast in S1's own history (earlier undated blocks, account tag LFL836, origin not
        established): a hand-added "41 7 7 9 * .../revert_delivery.sh" line was reported under
        this same RAN_UNVERIFIED heading, and those blocks' headers read CRON INTEGRITY WARNING.
    - the section  <U+23F0> Monitored, due-today jobs with NO heartbeat in 24h:
      CONTENT NOT PREDICTED -- it depends on heartbeat rows and markers at 18:00.
      WARNING class by code: it can never raise the block to CRITICAL (_build_alert :146-150).
      For reference only, not a prediction: across S1's last five CRITICAL blocks this section
      held 3, 4, 5, 5 and 5 items (16-Sep: evidence_backup, gemini_premarket_brief,
      gemini_log_review, gemini_trade_coach, gemini_data_integrity_check).
    - section order, by code (_build_alert :152-166): CRITICAL-absent, then RAN_UNVERIFIED,
      then heartbeat.

B3. HOW B2 WAS DERIVED -- so the derivation can itself be audited
    The VM's own ContentDrift / content_drift() definitions were lifted by `ast` from the VM
    copy (check_cron_drift.py was NOT imported: its module level calls load_dotenv and imports
    the state store) and executed on the PC against md5-asserted copies of the VM registry and
    the VM `crontab -l`, with generate_crontab.py at the 970aabf blob:
        REAL      absent_critical 5 (the five above) | absent_warn 0 | unregistered 1 (the
                  evaluator line) | unparseable 0 | has_critical True
    Red-capable controls -- same code, same inputs, ONE mutation each:
        A  the check_cron_drift line removed      -> absent_critical 6 (adds check_cron_drift)
        B  the evaluator line made unparseable    -> unregistered 0, unparseable 1 (CRITICAL class)
        C  the evaluator added to a scratch registry copy -> unregistered 0
    => detection reaches; the CRITICAL branch is reachable and the real line does not take it;
       the evaluator line is the ONLY unregistered line.


------------------------------------------------------------------------------
PART C -- HOW THE 18:00 OUTPUT IS SCORED (fixed before the observation)
------------------------------------------------------------------------------

C1. UNITS -- stated before counting, never merged, never summed across populations:
    U1  header lines "CRON INTEGRITY <SEVERITY>" in tonight's S1 bytes
    U2  CRITICAL-class items = item lines under a heading ending "(CRITICAL):"
    U3  RAN_UNVERIFIED items
    U4  heartbeat-miss items (WARNING class)
    E4.10's CRITICAL set (S3, set-difference against the 16-Sep baseline, per the frozen
    Gate 7/8 method) is a DIFFERENT population and is never added to U1 or U2.

C2. CLASSIFICATION
    U2 item named one of the five in B2       -> IDENTITY 1: standing / pre-existing
    U2 item with any other name, or ANY
    "no longer parses" item                   -> GENUINE NEW CRITICAL: investigated, not absorbed
    U3 item = the evaluator line in B2        -> IDENTITY 2: expected / predicted; not a defect
                                                 (deliberate temporary measurement infrastructure)
    U3 item that is anything else             -> UNPREDICTED: recorded and investigated
    a header line whose severity is not CRITICAL, or more than one header line
                                              -> a MISS of B2: recorded, not explained away

C3. SCORING -- the two predictions are scored SEPARATELY; neither is edited
    Part A item 1 : HIT if U2 lists the five gemini_* names.
    Part A item 2 : scored on two properties, reported separately --
                    (i) the evaluator line is reported;  (ii) it is reported AS A CRITICAL.
                    Part B predicts (i) YES and (ii) NO.
    Part B        : HIT or MISS per bullet of B2, and per sink claim of B1 (S3 especially).

C4. WORDING -- card section 2, the harder direction. Per population, with its unit:
    "N CRITICALs observed; M classified as pre-existing/expected per the 17-Sep pre-18:00
     prediction; K unexplained."
    Never "no CRITICALs". A classification annotates an observation; it never deletes one.

C5. NON-OBSERVATION -- if S1 has gained no bytes after the 18:00 run should have completed,
    the result is "18:00 drift run NOT OBSERVED -- execution not proven" (manifest Amendment 22
    section 2). Never "no CRITICAL".

C6. OUT OF SCOPE, stated now so that it cannot be explained after the fact --
    cron_officer --eod-summary (crontab line 139, 18:50) also compares the registry with the
    live crontab. Its severity logic was NOT read for this prediction. Any CRITICAL it emits is
    recorded as UNPREDICTED-REPORTER, and its items are classified by IDENTITY 1 / IDENTITY 2 as
    in C2; anything else is a genuine new CRITICAL.

C7. FALSIFIER FOR B1-S3 -- B1-S3 is a MISS if logs/system_2026-09-17.log gains any byte after
    its "Shutdown complete" line by the time the 18:00 run has completed, or contains any line
    with "check_cron_drift" or "CRON INTEGRITY".

END OF PREDICTION
