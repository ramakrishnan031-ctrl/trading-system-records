# -*- coding: utf-8 -*-
"""Normalizer implementing the FROZEN ruleset R1-R3 (Amendment 13 s3).

Usage:  normalize.py <a.jsonl> <b.jsonl>
Emits the normalized multiset difference both ways. Comparison only --
the raw .jsonl files remain the evidence of record (Amendment 14 s4).
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


a_path, b_path = sys.argv[1], sys.argv[2]
A, abad = load(a_path)
B, bbad = load(b_path)
ca, cb = collections.Counter(A), collections.Counter(B)

print("A = %s : %d events (%d unparseable)" % (a_path, len(A), abad))
print("B = %s : %d events (%d unparseable)" % (b_path, len(B), bbad))
print("distinct A=%d  B=%d" % (len(ca), len(cb)))

only_a = ca - cb
only_b = cb - ca
print("\n--- ONLY IN A (%d event-instances, %d distinct) ---" % (sum(only_a.values()), len(only_a)))
for (lvl, lg, msg), n in sorted(only_a.items(), key=lambda kv: (-kv[1], str(kv[0]))):
    print("  x%d  [%s] %s | %s" % (n, lvl, lg, msg[:150]))
print("\n--- ONLY IN B (%d event-instances, %d distinct) ---" % (sum(only_b.values()), len(only_b)))
for (lvl, lg, msg), n in sorted(only_b.items(), key=lambda kv: (-kv[1], str(kv[0]))):
    print("  x%d  [%s] %s | %s" % (n, lvl, lg, msg[:150]))

print("\nNOISE FLOOR: %d event-instances differ between two NO-CHANGE boots."
      % (sum(only_a.values()) + sum(only_b.values())))
