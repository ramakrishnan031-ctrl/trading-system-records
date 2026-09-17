"""Evidence capture around the UNMODIFIED scripts/sr_corp_action_spotcheck.py.

Runs the script's own main() with the card's exact argv. Wraps the two broker
methods on the kite object the script builds, so the one instruments() call and
the one historical_data() call are recorded, not repeated. Writes nothing.
Deployment-card amendment §5 fields: first/last session date, sessions before
and on/after the ex-date, instrument token, and every field of the matching
instrument record.
"""
import importlib.util
import sys
import traceback
from datetime import date, datetime

SCRIPT = sys.argv[1] if len(sys.argv) > 1 else "scripts/sr_corp_action_spotcheck.py"
ARGV = ["--symbol", "V2RETAIL", "--around", "2026-03-25", "--window", "20"]
SYMBOL = "V2RETAIL"
EX_DATE = date(2026, 3, 25)

spec = importlib.util.spec_from_file_location("sr_corp_action_spotcheck", SCRIPT)
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)

cap = {"instruments_calls": 0, "historical_calls": 0, "matches": None, "hist_kwargs": None, "rows": None}
_orig_build = sc._build_kite


def _build():
    k = _orig_build()
    if k is None:
        return None
    inst, hist = k.instruments, k.historical_data

    def instruments(*a, **kw):
        cap["instruments_calls"] += 1
        rows = inst(*a, **kw)
        cap["matches"] = [dict(r) for r in rows if r.get("tradingsymbol") == SYMBOL]
        return rows

    def historical_data(*a, **kw):
        cap["historical_calls"] += 1
        cap["hist_kwargs"] = {"args": [str(x) for x in a], **{key: str(v) for key, v in kw.items()}}
        rows = hist(*a, **kw)
        cap["rows"] = rows
        return rows

    k.instruments, k.historical_data = instruments, historical_data
    return k


sc._build_kite = _build

print("=== SCRIPT OUTPUT: sr_corp_action_spotcheck.main(%r) ===" % (ARGV,), flush=True)
rc = None
try:
    rc = sc.main(ARGV)
except BaseException:  # the evidence below must print even if the script dies after the call
    print("SCRIPT RAISED:", flush=True)
    traceback.print_exc(file=sys.stdout)
print("=== SCRIPT rc=%r ===" % (rc,), flush=True)

print("=== CAPTURED EVIDENCE ===")
print("broker calls: instruments=%d historical_data=%d" % (cap["instruments_calls"], cap["historical_calls"]))
print("instrument records with tradingsymbol=%s: %s" % (SYMBOL, "NONE CAPTURED" if cap["matches"] is None else len(cap["matches"])))
for m in cap["matches"] or []:
    print("  record:", {key: (str(v) if isinstance(v, (date, datetime)) else v) for key, v in sorted(m.items())})
print("historical_data request:", cap["hist_kwargs"])
rows = cap["rows"]
if rows is None:
    print("rows: NONE CAPTURED")
else:
    def _d(r):
        v = r["date"]
        return v.date() if isinstance(v, datetime) else v
    dates = [_d(r) for r in rows]
    print("rows returned: %d" % len(rows))
    if rows:
        print("first session: %s" % min(dates))
        print("last session : %s" % max(dates))
    print("sessions BEFORE %s: %d" % (EX_DATE, sum(1 for d in dates if d < EX_DATE)))
    print("sessions ON/AFTER %s: %d" % (EX_DATE, sum(1 for d in dates if d >= EX_DATE)))
    print("duplicate dates: %d" % (len(dates) - len(set(dates))))
    print("date        open      high      low       close     volume")
    for r in rows:
        print("%s  %-9s %-9s %-9s %-9s %s" % (_d(r), r.get("open"), r.get("high"), r.get("low"), r.get("close"), r.get("volume")))
print("=== END ===")
