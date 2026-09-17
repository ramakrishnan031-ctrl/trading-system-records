# -*- coding: utf-8 -*-
"""WINDOW VALIDATOR -- a PRECONDITION gate, run BEFORE any comparison.

Usage:  validate_window.py boot|eod <whole-day application log .jsonl>

Amendment 19 s1: the guard is EXACTLY ONE on both markers, not ">= 1".
    0 markers -> the boot never reached its terminator          -> WINDOW_INVALID
    1 marker  -> a single unambiguous window                    -> WINDOW_OK
    2 markers -> two boots/shutdowns in one day                 -> WINDOW_INVALID
A ">= 1" guard PASSES the 2-marker case, and two windows break every
multiplicity check: E1.1/E1.2 are each predicted exactly once, and the
whole-day rows (drain error, any new CRITICAL) would span two process
lifetimes attributed to one deployment. The awk also exits at the FIRST
terminator, so the boot window would silently be boot #1 while the whole-day
checks covered both -- two windows with two different meanings of "today".

Amendment 19 s3: when the window is invalid the FIRST finding is
WINDOW_INVALID, NEVER a normalizer residual. A huge residual list produced by
a malformed window must not be read as the primary failure.

Exit codes (a PRECONDITION verdict -- distinct from the normalizer's
tool-health rc, which is never a deployment verdict):
    0  WINDOW_OK
    3  WINDOW_INVALID
    2  input unusable
"""
import json, sys

SPECS = {
    # kind: (start marker, [end markers], source refs at e7bf477)
    "boot": ("Trading System v",
             ["effect_telemetry: composition OK", "effect_telemetry composition assertion FAILED"],
             "start main.py:2188 / end core/effect_telemetry.py:190|:197 via main.py:4277"),
    "eod": ("Shutdown initiated",
            ["Shutdown complete"],
            "start main.py:1631 / end main.py:1839 -- sr_shadow.stop() at main.py:1705 lies between them"),
}

if len(sys.argv) != 3 or sys.argv[1] not in SPECS:
    print("usage: validate_window.py boot|eod <whole-day .jsonl>")
    sys.exit(2)

kind, path = sys.argv[1], sys.argv[2]
start_key, end_keys, prov = SPECS[kind]

starts, ends, bad, total = [], [], 0, 0
for i, ln in enumerate(open(path, encoding="utf-8"), 1):
    ln = ln.strip()
    if not ln:
        continue
    total += 1
    try:
        msg = json.loads(ln).get("msg", "")
    except Exception:
        bad += 1
        continue
    if msg.startswith(start_key):
        starts.append(i)
    for k in end_keys:
        if msg.startswith(k):
            ends.append(i)
            break

print("WINDOW VALIDATOR  kind=%s  file=%s" % (kind, path))
print("  provenance: %s" % prov)
print("  start marker %-34r count=%d at lines %s" % (start_key, len(starts), starts or "-"))
print("  end marker(s) %-33r count=%d at lines %s" % ("|".join(end_keys), len(ends), ends or "-"))
if bad:
    print("  unparseable lines: %d of %d" % (bad, total))

fail = []
if len(starts) != 1:
    fail.append("start marker count is %d, must be EXACTLY 1 (0 = window never opened; "
                ">=2 = two %s events in one day)" % (len(starts), kind))
if len(ends) != 1:
    if len(ends) == 0:
        fail.append("end marker count is 0 -- the %s NEVER REACHED ITS TERMINATOR. That is "
                    "ITSELF THE FINDING; the window would otherwise run to end of file and the "
                    "comparison would produce enormous residuals that look like a normalizer "
                    "or window fault." % kind)
    else:
        fail.append("end marker count is %d, must be EXACTLY 1 -- two windows in one day break "
                    "EVERY multiplicity check. NOTE: a '>= 1' guard would have PASSED this."
                    % len(ends))
if len(starts) == 1 and len(ends) == 1 and ends[0] <= starts[0]:
    fail.append("the end marker (line %d) does not occur AFTER the start marker (line %d)"
                % (ends[0], starts[0]))

print()
if fail:
    print("*** WINDOW_INVALID ***")
    for f in fail:
        print("  - %s" % f)
    print("\n  >>> THE FIRST FINDING IS **WINDOW_INVALID**, never NORMALIZER_RESIDUAL.")
    print("  >>> Do NOT run the comparison and then interpret the residuals. STOP and report.")
    sys.exit(3)

print("WINDOW_OK  lines %d..%d  (%d events in window)" % (starts[0], ends[0], ends[0] - starts[0] + 1))
sys.exit(0)
