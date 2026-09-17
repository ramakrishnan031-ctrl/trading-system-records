"""Classify the 17-Sep 18:00 drift block (S1) against the FROZEN prediction's Part C.
Locale discipline: Python on bytes/str, ASCII anchors only, no grep; every count cross-checked at the byte level;
a positive control on the preserved pre-18:00 log; mutation controls that must FLIP the verdict. ASCII stdout."""
import hashlib
from pathlib import Path

P = Path("D:/Projects/_preservation")
BLOCK = P / "CRON_DRIFT_1800_APPENDED_BLOCK_17-Sep-2026__after_byte_12347__captured_2026-09-17T1800IST.log"
PRE = P / "CRON_DRIFT_CHECK_LOG_trading-sbx__pre-1800_17-Sep-2026__captured_2026-09-17T1000IST.log"
PRED = P / "CRON_DRIFT_1800_PREDICTION_17-Sep-2026__pre-registered_2026-09-17T1003IST.md"
FIVE = ["gemini_premarket_brief (08:55 Mon-Fri)", "gemini_log_review (16:20 Mon-Fri)",
        "gemini_trade_coach (16:40 Mon-Fri)", "gemini_data_integrity_check (17:00 Mon-Fri)",
        "gemini_weekly_patterns (18:00 Sunday)"]
FIVE_NAMES = [x.split(" (")[0] for x in FIVE]
EVAL = ("5 16 * * 1-5 cd /home/ubuntu/systems/trading-system && set -a && . ./.env && set +a && PYTHONPATH=. "
        "/home/ubuntu/systems/venv/bin/python scripts/sr_shadow_evaluate.py >> logs/cron-sr-shadow-evaluate.log 2>&1")


def p(*a):
    print(" ".join(str(x) for x in a).encode("ascii", "backslashreplace").decode("ascii"))


def md5(b):
    return hashlib.md5(b).hexdigest()


def section_kind(ln):
    if ln.endswith("ENABLED in registry, ABSENT from live crontab (CRITICAL):"):
        return "ABSENT_CRITICAL"
    if ln.endswith("Live crontab line no longer parses (CRITICAL):"):
        return "UNPARSEABLE"
    if ln.endswith("Personal-tooling job absent from live (WARN):"):
        return "ABSENT_WARN"
    if "Live job NOT in registry" in ln and ln.endswith("RAN_UNVERIFIED (needs registry entry + contract):"):
        return "UNREGISTERED"
    if ln.endswith("Monitored, due-today jobs with NO heartbeat in 24h:"):
        return "HEARTBEAT"
    if ln.endswith("(CRITICAL):"):
        return "UNKNOWN_CRITICAL_HEADING"
    return None


def parse(text):
    """-> list of blocks; each block = dict(header, severity, sections=[(kind, heading, [items])]); plus stray lines."""
    blocks, stray = [], []
    cur = None
    for n, ln in enumerate(text.split("\n")[:-1] if text.endswith("\n") else text.split("\n"), 1):
        parts = ln.split(" ")
        if (len(parts) == 4 and parts[0].startswith("[") and parts[0].endswith("]") and parts[1] == "CRON"
                and parts[2] == "INTEGRITY" and parts[3].isascii() and parts[3].isalpha() and parts[3].isupper()):
            cur = {"line": n, "header": ln, "tag": parts[0], "severity": parts[3], "sections": []}
            blocks.append(cur)
            continue
        k = section_kind(ln)
        if k is not None:
            if cur is None:
                stray.append((n, "HEADING_WITHOUT_HEADER", ln))
                continue
            cur["sections"].append([k, ln, []])
            continue
        if ln.startswith("   - "):
            if cur is None or not cur["sections"]:
                stray.append((n, "ITEM_WITHOUT_SECTION", ln))
                continue
            cur["sections"][-1][2].append(ln[len("   - "):])
            continue
        stray.append((n, "UNRECOGNISED", ln))
    return blocks, stray


def classify(blocks, stray):
    v = {"U1_headers": [(b["header"], b["severity"]) for b in blocks], "IDENTITY1": [], "GENUINE_NEW": [],
         "IDENTITY2": [], "UNPREDICTED_U3": [], "U4": [], "ABSENT_WARN": [], "MISS": [], "stray": stray}
    if len(blocks) != 1:
        v["MISS"].append(f"header line count {len(blocks)} != 1")
    for b in blocks:
        if b["severity"] != "CRITICAL":
            v["MISS"].append(f"header severity {b['severity']}")
        if b["header"] != "[VBB097] CRON INTEGRITY CRITICAL":
            v["MISS"].append("header text differs from B2")
        for kind, heading, items in b["sections"]:
            for it in items:
                if kind == "ABSENT_CRITICAL":
                    (v["IDENTITY1"] if it.split(" (")[0] in FIVE_NAMES else v["GENUINE_NEW"]).append(it)
                elif kind in ("UNPARSEABLE", "UNKNOWN_CRITICAL_HEADING"):
                    v["GENUINE_NEW"].append(f"[{kind}] {it}")
                elif kind == "UNREGISTERED":
                    (v["IDENTITY2"] if it == EVAL else v["UNPREDICTED_U3"]).append(it)
                elif kind == "HEARTBEAT":
                    v["U4"].append(it)
                elif kind == "ABSENT_WARN":
                    v["ABSENT_WARN"].append(it)
    return v


def score(blocks, v):
    s = {}
    b = blocks[0] if len(blocks) == 1 else None
    kinds = [k for k, _, _ in b["sections"]] if b else []
    items = {k: it for k, _, it in b["sections"]} if b else {}
    s["B2.1 exactly one header, CRITICAL, text as predicted"] = bool(b) and b["header"] == "[VBB097] CRON INTEGRITY CRITICAL"
    s["B2.2 CRITICAL-absent section = the five, in order"] = items.get("ABSENT_CRITICAL") == FIVE and kinds.count("ABSENT_CRITICAL") == 1
    s["B2.3 no 'no longer parses' section"] = "UNPARSEABLE" not in kinds
    s["B2.4 no 'Personal-tooling ... (WARN)' section"] = "ABSENT_WARN" not in kinds
    s["B2.5 RAN_UNVERIFIED section = exactly the evaluator line"] = items.get("UNREGISTERED") == [EVAL] and kinds.count("UNREGISTERED") == 1
    order = [k for k in kinds if k in ("ABSENT_CRITICAL", "UNREGISTERED", "HEARTBEAT")]
    s["B2.7 order CRITICAL-absent, RAN_UNVERIFIED, heartbeat"] = order == [k for k in ("ABSENT_CRITICAL", "UNREGISTERED", "HEARTBEAT") if k in order] and "UNKNOWN_CRITICAL_HEADING" not in kinds
    s["A1 U2 lists the five gemini_* names"] = sorted(x.split(" (")[0] for x in v["IDENTITY1"]) == sorted(FIVE_NAMES)
    eval_crit = any(it == EVAL for bb in blocks for k, _, its in bb["sections"] if k in ("ABSENT_CRITICAL", "UNPARSEABLE", "UNKNOWN_CRITICAL_HEADING") for it in its)
    eval_any = any(it == EVAL for bb in blocks for _, _, its in bb["sections"] for it in its)
    s["A2(i) evaluator line reported"] = eval_any
    s["A2(ii) evaluator line reported AS A CRITICAL"] = eval_crit
    return s


def verdict_line(v):
    return (f"U1={len(v['U1_headers'])}{[h[1] for h in v['U1_headers']]} U2: IDENTITY1={len(v['IDENTITY1'])} GENUINE_NEW={len(v['GENUINE_NEW'])} "
            f"U3: IDENTITY2={len(v['IDENTITY2'])} UNPREDICTED={len(v['UNPREDICTED_U3'])} U4={len(v['U4'])} "
            f"ABSENT_WARN={len(v['ABSENT_WARN'])} MISS={len(v['MISS'])} stray={len(v['stray'])}")


# ---- premises
assert md5(PRED.read_bytes()) == "b31802e4a210a830e188df2424216e33", "FROZEN PREDICTION CHANGED"
raw = BLOCK.read_bytes()
assert len(raw) == 921 and md5(raw) == "35ab0fb21826c0f8f37ae30092245591", "block drifted"
text = raw.decode("utf-8", errors="strict")
p("PREMISES frozen prediction md5 b31802e4... unchanged; block 921 B md5 35ab0fb2...; strict UTF-8 decode OK; CR", raw.count(b"\r"),
  "; ends with LF", raw.endswith(b"\n"), "; LF count", raw.count(b"\n"))

p("---- OBSERVED BLOCK, line by line (non-ASCII shown as escapes) ----")
for n, ln in enumerate(text.split("\n")[:-1], 1):
    p(f"{n:02d}|{ln}")

blocks, stray = parse(text)
v = classify(blocks, stray)
p("---- REAL ----")
p("VERDICT", verdict_line(v))
for k in ("U1_headers", "IDENTITY1", "GENUINE_NEW", "IDENTITY2", "UNPREDICTED_U3", "U4", "ABSENT_WARN", "MISS", "stray"):
    p(" ", k, v[k])
for b in blocks:
    for kind, heading, items in b["sections"]:
        p("  SECTION", kind, "| heading codepoints before ASCII text:", [f"U+{ord(c):04X}" for c in heading if ord(c) > 127], "| items", len(items))
sc = score(blocks, v)
for k, val in sc.items():
    p("  SCORE", k, "->", "HIT" if val else "MISS")

# ---- byte-level cross-counts (independent of the parser)
bc = {"CRON INTEGRITY": raw.count(b"CRON INTEGRITY"), "(CRITICAL):\\n": raw.count(b"(CRITICAL):\n"),
      "RAN_UNVERIFIED": raw.count(b"RAN_UNVERIFIED"), "NO heartbeat in 24h:\\n": raw.count(b"NO heartbeat in 24h:\n"),
      "items '\\n   - '": raw.count(b"\n   - ") + (1 if raw.startswith(b"   - ") else 0), "no longer parses": raw.count(b"no longer parses"),
      "(WARN):": raw.count(b"(WARN):"), "sr_shadow_evaluate.py": raw.count(b"sr_shadow_evaluate.py"), "gemini_": raw.count(b"gemini_")}
n_items = sum(len(it) for b in blocks for _, _, it in b["sections"])
p("BYTECOUNT", bc)
p("CROSSCHECK U1 parser", len(blocks), "== bytes", bc["CRON INTEGRITY"], "->", len(blocks) == bc["CRON INTEGRITY"],
  "| items parser", n_items, "== bytes", bc["items '\\n   - '"], "->", n_items == bc["items '\\n   - '"],
  "| CRITICAL headings parser", sum(1 for b in blocks for k, _, _ in b["sections"] if k in ("ABSENT_CRITICAL", "UNPARSEABLE", "UNKNOWN_CRITICAL_HEADING")),
  "== bytes", bc["(CRITICAL):\\n"])

# ---- positive control: the same parser on the preserved pre-18:00 log
pre = PRE.read_bytes()
assert md5(pre) == "a35fd44ba983b3ccf6b964d27e018ccb"
pb, ps = parse(pre.decode("utf-8"))
last = pb[-1]
p("---- POSITIVE CONTROL (pre-18:00 log, 12,347 B) ----")
p("  headers parsed", len(pb), "== bytes 'CRON INTEGRITY'", pre.count(b"CRON INTEGRITY"), "| severities", sorted({b["severity"] for b in pb}),
  "| stray lines", len(ps), "kinds", sorted({s[1] for s in ps}))
p("  LAST block (16-Sep 18:00 by mtime):", last["header"], [(k, it) for k, _, it in last["sections"]])
p("  LAST block CRITICAL-absent == the five in order ->", dict((k, it) for k, _, it in last["sections"]).get("ABSENT_CRITICAL") == FIVE,
  "| RAN_UNVERIFIED items in last block:", sum(len(it) for k, _, it in last["sections"] if k == "UNREGISTERED"))

# ---- mutation controls: each MUST change the verdict
p("---- MUTATION CONTROLS (each must flip) ----")
base = verdict_line(v)
L = text.split("\n")
i_crit = next(i for i, ln in enumerate(L) if ln.endswith("(CRITICAL):"))
i_unreg = next(i for i, ln in enumerate(L) if "RAN_UNVERIFIED" in ln)
i_eval = next(i for i, ln in enumerate(L) if ln == "   - " + EVAL)
i_hdr = next(i for i, ln in enumerate(L) if "CRON INTEGRITY" in ln)
muts = {
    "M1 extra item under CRITICAL-absent": L[:i_crit + 1] + ["   - fake_new_job (01:00 daily)"] + L[i_crit + 1:],
    "M2 header severity WARNING": L[:i_hdr] + [L[i_hdr].replace("CRITICAL", "WARNING")] + L[i_hdr + 1:],
    "M3 duplicated header line": L[:i_hdr + 1] + [L[i_hdr]] + L[i_hdr + 1:],
    "M4 add an unparseable section": L[:i_unreg] + ["\U0001f534 Live crontab line no longer parses (CRITICAL):", "   - junk line"] + L[i_unreg:],
    "M5 second RAN_UNVERIFIED item": L[:i_eval + 1] + ["   - 1 2 * * * /bin/true"] + L[i_eval + 1:],
    "M6 evaluator line altered by one char": L[:i_eval] + [L[i_eval].replace("5 16 ", "6 16 ", 1)] + L[i_eval + 1:],
    "M7 one gemini item removed": L[:i_crit + 1] + L[i_crit + 2:],
    "M8 evaluator line moved under CRITICAL-absent": L[:i_crit + 1] + ["   - " + EVAL] + [x for j, x in enumerate(L[i_crit + 1:], i_crit + 1) if j != i_eval],
}
for name, ml in muts.items():
    mt = "\n".join(ml)
    mb, ms = parse(mt)
    mv = classify(mb, ms)
    msc = score(mb, mv) if len(mb) == 1 else {"(no single block)": False}
    flipped = verdict_line(mv) != base or msc != sc
    changed = sorted(k for k in sc if msc.get(k) != sc[k])
    p(f"  {name}: FLIPPED={flipped} | {verdict_line(mv)} | score keys changed: {changed}")
