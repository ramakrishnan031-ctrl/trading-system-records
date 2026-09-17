# -*- coding: utf-8 -*-
"""Normalizer for the APPLICATION LOG ONLY -- frozen ruleset R1/R3 (Amd 13 s3, 15 s2).

Usage:  normalize.py <a.jsonl> <b.jsonl>

SCOPE (Amendment 15 s2 -- sink authority is by ORIGIN, not by level):
  * This tool compares APPLICATION-EMITTED events, and the application log
    (logs/system_<DATE>.log, JSON lines) is their AUTHORITATIVE sink, ALWAYS.
    It carries INFO+, so a level flip never changes what it holds.
  * The journal's copy of an application event is a stdout DUPLICATE whose
    presence depends on level -- it must NEVER be used for comparison.
  * SYSTEMD / UNIT LIFECYCLE events (Started/Stopped/Main process exited/
    restarts) are authoritative in the JOURNAL and are compared separately;
    the application log cannot carry them, because the app never emitted them.

MISUSE GUARD: journal text is not JSON. If a file does not parse as JSON lines
this exits non-zero rather than silently producing a garbage diff -- pointing
this tool at the journal is the mistake the origin rule exists to prevent.

Comparison only -- the raw files remain the evidence of record (Amd 14 s4).
"""
import collections, json, re, sys

# R3 -- each rule justified by CODE, not by "it differed".
# R3.1-R3.3 predicted from the sr_shadow diff; R3.4-R3.8 added 16-Sep ~10:50
# from the 15-Sep vs 16-Sep calibration (Amendment 14 s3a), which empirically
# enumerated every date-bearing boot message -- which is what makes TARGETED
# date rules complete for the boot window rather than a blanket date wildcard.
R3 = [
    # R3.1 runtime-resolved store path -- sr_shadow/runner.py:152 logs self._store.path
    (re.compile(r"(sr_shadow: worker started \(contract=\S+ schema=\S+ db=).*?(/sr_shadow\.db\))"), r"\1<PATH>\2"),
    # R3.2 session-dependent counters -- runner.py:158 json.dumps(self.counters)/history.stats
    (re.compile(r"(sr_shadow: worker stopped counters=).*?( history=).*$"), r"\1<JSON>\2<JSON>"),
    # R3.3 interpolated symbol -- signals/signal_processor.py:649
    (re.compile(r"(sr_shadow capture failed for ).*?(:)"), r"\1<SYMBOL>\2"),
    # R3.4 live disk measurement -- utils/startup_checks.py:1242 logs shutil.disk_usage free
    (re.compile(r"(check_disk_space: OK free=)[0-9.]+(GB)"), r"\1<GB>\2"),
    # R3.5 snapshot_date -- core/config_snapshotter.py:184
    (re.compile(r"(config_snapshotter: resolved config for )\d{4}-\d{2}-\d{2}"), r"\1<DATE>"),
    # R3.6 DB-assigned new_id + snapshot_date -- core/config_snapshotter.py:214
    (re.compile(r"(config_snapshotter: wrote config snapshot id=)\d+( for )\d{4}-\d{2}-\d{2}"), r"\1<ID>\2<DATE>"),
    # R3.7 prev/today session dates -- utils/startup_checks.py:296
    (re.compile(r"(startup_scenario=COLD: new day \(prev=)\d{4}-\d{2}-\d{2}(, today=)\d{4}-\d{2}-\d{2}"),
     r"\1<DATE>\2<DATE>"),
    # R3.8 triggered_date + today -- capital/kill_switch.py:360. reason/by are EVIDENCE, kept.
    (re.compile(r"(Kill switch auto-cleared: prior \S+ from )\d{4}-\d{2}-\d{2}"), r"\1<DATE>"),
    (re.compile(r"(-- new day )\d{4}-\d{2}-\d{2}( starts clean)"), r"\1<DATE>\2"),
]


def norm_msg(msg):
    for pat, rep in R3:
        msg = pat.sub(rep, msg)
    return msg


def load(path):
    """R1: key = (level, logger, normalized msg). R1.2 drops ts only."""
    events = []
    bad = 0
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        try:
            d = json.loads(ln)
        except Exception:
            bad += 1
            continue
        events.append((d.get("level"), d.get("logger"), norm_msg(d.get("msg", ""))))
    return events, bad


BANNER = """\
================================================================================
 THIS TOOL'S EXIT CODE CARRIES NO VERDICT.  (Amendment 16 s1)
 It reports DIFFERENCES between two event streams. It knows NOTHING about the
 predicted deployment events.
   * On a CHANGE pair (17-Sep vs 16-Sep) the rc is INVERTED: a CORRECT
     deployment emits new events -> unrecognised families -> rc 1.  A
     deployment where the manager NEVER STARTED emits nothing -> no difference
     -> rc 0.  DEMONSTRATED 16-Sep: correct=4 unrecognised/rc 1, failed=0/rc 0.
   * An event absent from BOTH sides produces NO difference, so this tool is
     STRUCTURALLY BLIND to a MISSING expected event -- which is the E-1 failure
     mode the prediction exists to catch.
 Presence, multiplicity and order are tested ONLY by the per-event Gate 7/8
 table. The Gate 7/8 record has NO FIELD for this tool's pass/fail -- only for
 its residual list.
================================================================================"""
print(BANNER)

a_path, b_path = sys.argv[1], sys.argv[2]
A, abad = load(a_path)
B, bbad = load(b_path)
ca, cb = collections.Counter(A), collections.Counter(B)

print("A = %s : %d events (%d unparseable)" % (a_path, len(A), abad))
print("B = %s : %d events (%d unparseable)" % (b_path, len(B), bbad))
print("distinct A=%d  B=%d" % (len(ca), len(cb)))

# MISUSE GUARD (Amendment 15 s2): the application log is JSON lines. Journal text
# is not. Refuse rather than emit a garbage diff.
for path, ok, bad in ((a_path, len(A), abad), (b_path, len(B), bbad)):
    if bad:
        total = ok + bad
        print("\n*** UNPARSEABLE LINES in %s: %d of %d ***" % (path, bad, total))
        if bad * 2 >= total:
            print("*** REFUSED: this is not a JSON application log. The journal is NOT")
            print("*** comparable with this tool -- systemd lifecycle events are compared")
            print("*** separately, and the journal's copy of an application event is a")
            print("*** level-dependent stdout duplicate. See ruleset R2. ***")
            sys.exit(2)

only_a = ca - cb
only_b = cb - ca
print("\n--- ONLY IN A (%d event-instances, %d distinct) ---" % (sum(only_a.values()), len(only_a)))
for (lvl, lg, msg), n in sorted(only_a.items(), key=lambda kv: (-kv[1], str(kv[0]))):
    print("  x%d  [%s] %s | %s" % (n, lvl, lg, msg[:150]))
print("\n--- ONLY IN B (%d event-instances, %d distinct) ---" % (sum(only_b.values()), len(only_b)))
for (lvl, lg, msg), n in sorted(only_b.items(), key=lambda kv: (-kv[1], str(kv[0]))):
    print("  x%d  [%s] %s | %s" % (n, lvl, lg, msg[:150]))

# Amendment 15 s1: report by FAMILY IDENTITY. A count must never travel as a budget.
# Amendment 16 s2: the match is ANCHORED -- logger must match AND msg must START
# with the key. Fragment matching here would silently absorb a genuinely new event
# whose text merely CONTAINS a known key (e.g. a new error about the NTP check)
# into a known family -- a FALSE GREEN, which is silent. R1.5 forbids fragment
# matching for event identity; the classifier must be held to the same rule.
KNOWN_FAMILIES = [
    ("check_ntp_sync", "main", "NTP outcome varies; it flips INFO<->WARNING"),
    ("email_fallback.sent", "telegram_notifier", "telegram email fallback fires or does not"),
]


def family_of(logger, msg):
    for key, lg, _ in KNOWN_FAMILIES:
        if logger == lg and msg.startswith(key):
            return key
    return None


resid = list(only_a.elements()) + list(only_b.elements())
known = collections.Counter(f for f in (family_of(lg, m) for _, lg, m in resid) if f)
unknown = [(lvl, lg, m) for (lvl, lg, m) in resid if family_of(lg, m) is None]

print("\n=== RESIDUAL, BY FAMILY (Amendment 15 s1) ===")
print("  RECOGNITION IS BY FAMILY IDENTITY, NEVER BY COUNT.")
print("  Ten instances of a known family is ordinary. ONE instance of a new family is NOT.")
for key, lg, why in KNOWN_FAMILIES:
    print("    KNOWN-VARIANCE  %-22s x%-3d  [logger=%s]  (%s)" % (key, known.get(key, 0), lg, why))
print("    UNRECOGNISED FAMILIES: %d" % len(unknown))
for lvl, lg, m in unknown:
    print("      >>> %s | %s | %s" % (lvl, lg, m[:120]))
print("\n  Observed residual sample: %d event-instances across this comparison." % len(resid))
print("  NOT a false-positive rate -- no denominator, no distribution over")
print("  repeated no-deployment boots. RECORD THE RESIDUAL LIST, NOT THIS rc.")

# Amendment 16 s3: the application log is machine-written JSON. ANY unparseable
# line in it is itself an anomaly to adjudicate, not a rounding error -- and
# silently dropping it from a comparison whose purpose is to notice MISSING
# events is exactly the wrong failure. The 50% rule above catches "you pointed
# this at the journal"; this catches "this file is partly corrupt".
if abad or bbad:
    print("\n  *** FINDING: %d unparseable line(s) were DROPPED from this comparison."
          % (abad + bbad))
    print("  *** The application log is machine-written JSON; an unparseable line is")
    print("  *** an anomaly to adjudicate. Record it in the Gate 7/8 table. ***")

print("\n" + BANNER)
sys.exit(1 if (unknown or abad or bbad) else 0)
