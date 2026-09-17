# -*- coding: utf-8 -*-
"""Gate 7/8 per-event row extractor -- READ-ONLY over LOCAL captures. Writes nothing.

Usage: gate78_rows.py <baseline whole-day app log> <17-Sep whole-day app log (captured)>

Every row reports observed multiplicity + raw line refs (line numbers are 1-based in the
WHOLE-DAY file named). Boot window = the prediction's semantic delimiters, applied exactly
as its awk does: first 'Trading System v.* starting' through the first
'composition OK|composition assertion FAILED' at/after it. The normalizer's norm_msg (R3)
is imported from the FROZEN normalizer text, not re-typed, so E1.1's <PATH> rule is the
frozen one.
"""
import io, json, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
FROZEN_NORMALIZER = "D:/Projects/_preservation/normalize_bootlog__frozen_v3_2026-09-16T1138IST.py"

# Pull R3 + norm_msg out of the frozen file WITHOUT executing its top-level comparison code.
src = open(FROZEN_NORMALIZER, encoding="utf-8").read()
start = src.index("R3 = [")
end = src.index("def load(path):")
ns = {"re": re}
exec(compile(src[start:end], FROZEN_NORMALIZER, "exec"), ns)
norm_msg = ns["norm_msg"]


def read(path):
    rows, bad = [], []
    for i, ln in enumerate(open(path, encoding="utf-8"), 1):
        s = ln.strip()
        if not s:
            continue
        try:
            d = json.loads(s)
        except Exception:
            bad.append(i)
            continue
        rows.append((i, d.get("ts", ""), d.get("level"), d.get("logger"), d.get("msg", "") or "", d))
    return rows, bad


def boot_window(rows):
    out, on = [], False
    for r in rows:
        if not on and re.search(r"Trading System v.* starting", r[4]):
            on = True
        if on:
            out.append(r)
            if re.search(r"composition OK|composition assertion FAILED", r[4]):
                break
    return out


def refs(rs, n=6):
    return ", ".join("L%d@%s" % (r[0], r[1][11:23]) for r in rs[:n]) + (" …" if len(rs) > n else "") if rs else "-"


base_path, day_path = sys.argv[1], sys.argv[2]
B_rows, B_bad = read(base_path)
T_rows, T_bad = read(day_path)
Bw, Tw = boot_window(B_rows), boot_window(T_rows)

print("INPUTS")
print("  baseline whole-day : %s  events=%d unparseable=%d" % (base_path, len(B_rows), len(B_bad)))
print("  17-Sep whole-day   : %s  events=%d unparseable=%d %s" % (day_path, len(T_rows), len(T_bad), T_bad[:10]))
print("  17-Sep last event ts (capture horizon): %s" % (T_rows[-1][1] if T_rows else "-"))
print("  boot window: baseline L%s..L%s (%d events) | 17-Sep L%s..L%s (%d events)" % (
    Bw[0][0] if Bw else "-", Bw[-1][0] if Bw else "-", len(Bw),
    Tw[0][0] if Tw else "-", Tw[-1][0] if Tw else "-", len(Tw)))

E11 = "sr_shadow: worker started (contract=v1.3 schema=1 db=<PATH>/sr_shadow.db)"
E12 = "sr_shadow: ENABLED and started (mode=LIVE, log-only)"


def sel(rows, pred):
    return [r for r in rows if pred(r)]


print("\nE-1  (BOOT WINDOW, app log; FULL normalized msg; multiplicity exactly 1)")
e11 = sel(Tw, lambda r: r[3] == "sr_shadow" and r[2] == "INFO" and norm_msg(r[4]) == E11)
e11_any = sel(Tw, lambda r: "worker started" in r[4])
e12 = sel(Tw, lambda r: r[3] == "main" and r[2] == "INFO" and r[4] == E12)
e12_frag = sel(Tw, lambda r: r[4].startswith("sr_shadow: ENABLED and started"))
enabled_frag_all = sel(Tw, lambda r: "ENABLED and started" in r[4])
print("  E1.1 exact(logger=sr_shadow,INFO,full-norm-msg) : %d  %s" % (len(e11), refs(e11)))
for r in e11:
    print("       raw msg: %s" % r[4])
print("       (diagnostic, NOT the test) any 'worker started' in window: %d  %s" % (len(e11_any), refs(e11_any)))
print("  E1.2 exact(logger=main,INFO,full msg)           : %d  %s" % (len(e12), refs(e12)))
print("       (diagnostic, NOT the test) msg startswith 'sr_shadow: ENABLED and started': %d  %s" % (len(e12_frag), refs(e12_frag)))
for r in e12_frag:
    print("       raw: [%s] %s | %s" % (r[2], r[3], r[4]))
print("       (diagnostic, the substring trap) any 'ENABLED and started' in window: %d  %s" % (len(enabled_frag_all), refs(enabled_frag_all)))
for r in enabled_frag_all:
    print("         - [%s] %s | %s" % (r[2], r[3], r[4]))
if len(e11) == 1 and len(e12) == 1:
    print("  ORDER E1.1 before E1.2: %s (L%d vs L%d)" % ("YES" if e11[0][0] < e12[0][0] else "NO", e11[0][0], e12[0][0]))
else:
    print("  ORDER: not evaluable (multiplicity not 1/1)")

print("\nE-2.3 composition (BOOT WINDOW end marker)")
for label, w in (("baseline", Bw), ("17-Sep", Tw)):
    c = sel(w, lambda r: "composition OK" in r[4] or "composition assertion FAILED" in r[4])
    for r in c:
        print("  %-8s L%d %s [%s] %s | %s" % (label, r[0], r[1][11:23], r[2], r[3], r[4][:200]))
    if not c:
        print("  %-8s NO end marker in window" % label)

print("\nE-2.4 config-bearing boot lines (context; the YAML md5 is read on the VM separately)")
for label, w in (("baseline", Bw), ("17-Sep", Tw)):
    for r in sel(w, lambda r: r[4].startswith("Config loaded") or r[4].startswith("config_snapshotter")):
        print("  %-8s L%d %s | %s" % (label, r[0], r[1][11:23], r[4][:220]))

print("\nE-4 MUST BE ABSENT (app log)")
e46w = sel(Tw, lambda r: r[4].startswith("sr_shadow wiring failed"))
e46d = sel(T_rows, lambda r: r[4].startswith("sr_shadow wiring failed"))
e47w = sel(Tw, lambda r: "composition assertion FAILED" in r[4])
e47d = sel(T_rows, lambda r: "composition assertion FAILED" in r[4])
e48d = sel(T_rows, lambda r: r[4].startswith("sr_shadow: drain error="))
e49d = sel(T_rows, lambda r: "stop_invariant_violated" in r[4])
print("  E4.6 'sr_shadow wiring failed'   boot window=%d %s | whole-day-so-far=%d %s" % (len(e46w), refs(e46w), len(e46d), refs(e46d)))
print("  E4.7 'composition assertion FAILED' boot window=%d %s | whole-day-so-far=%d %s" % (len(e47w), refs(e47w), len(e47d), refs(e47d)))
print("  E4.8 'sr_shadow: drain error='   whole-day-so-far=%d %s" % (len(e48d), refs(e48d)))
print("  E4.9 'stop_invariant_violated'   (EOD window; not yet open) whole-day-so-far=%d %s" % (len(e49d), refs(e49d)))
bc = {(r[3], norm_msg(r[4])) for r in B_rows if r[2] == "CRITICAL"}
tc = sel(T_rows, lambda r: r[2] == "CRITICAL")
new_crit = [r for r in tc if (r[3], norm_msg(r[4])) not in bc]
print("  E4.10 CRITICAL so far today: %d total; NEW vs baseline set (logger + R3-normalized msg): %d" % (len(tc), len(new_crit)))
for r in tc:
    tag = "NEW" if r in new_crit else "in-baseline-set"
    print("       [%s] L%d %s %s | %s" % (tag, r[0], r[1][11:23], r[3], r[4][:230]))
print("  baseline CRITICAL set size (distinct logger+norm msg): %d" % len(bc))

print("\nE-5")
k = "sr_detector/retest enabled but no market-data kite handle"
print("  E5.11 kite-handle WARNING boot window: baseline=%d 17-Sep=%d %s" % (
    len(sel(Bw, lambda r: r[4].startswith(k))), len(sel(Tw, lambda r: r[4].startswith(k))), refs(sel(Tw, lambda r: r[4].startswith(k)))))
rt = ("sr_shadow capture failed for", "sr_shadow.capture_failed", "sr_shadow.capture_duplicate", "sr_shadow.process_failed")
for key in rt:
    w = sel(Tw, lambda r, key=key: r[4].startswith(key))
    d = sel(T_rows, lambda r, key=key: r[4].startswith(key))
    print("  E5.12 %-30s boot window=%d | whole-day-so-far=%d %s" % (key, len(w), len(d), refs(d)))

print("\nOTHER BOOT-WINDOW FACTS (context, not predicted rows)")
for r in sel(Tw, lambda r: r[4] == "strategy_control.summary"):
    d = r[5]
    print("  L%d strategy_control.summary will_trade_count=%s wont_trade=%s trade_type=%s force_intraday_only=%s" % (
        r[0], d.get("will_trade_count"), d.get("wont_trade"), d.get("trade_type"), d.get("force_intraday_only")))
    print("       will_trade=%s" % d.get("will_trade"))
lv = {}
for r in Tw:
    lv[r[2]] = lv.get(r[2], 0) + 1
print("  17-Sep boot window level counts: %s" % lv)
lvb = {}
for r in Bw:
    lvb[r[2]] = lvb.get(r[2], 0) + 1
print("  baseline boot window level counts: %s" % lvb)
for r in sel(Tw, lambda r: r[2] in ("ERROR", "CRITICAL", "WARNING")):
    print("    17-Sep window [%s] L%d %s %s | %s" % (r[2], r[0], r[1][11:23], r[3], r[4][:200]))
st = sel(T_rows, lambda r: re.search(r"Trading System v.* starting", r[4]))
print("  'Trading System v… starting' whole-day-so-far count: %d %s" % (len(st), refs(st)))
