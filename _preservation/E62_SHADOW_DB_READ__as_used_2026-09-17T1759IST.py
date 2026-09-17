"""E6.2 read of the preserved 17-Sep shadow DB copies (captured 17:58 IST, md5-verified against the VM).
Never opens a preserved file: byte-copies to two scratch working dirs first (refuses if they exist).
A = immutable=1 on main file (SQLite does NOT read the WAL under immutable) -- the false-zero comparison.
B = normal open of main+WAL copy (WAL recovered) -- the measurement.
ASCII stdout only."""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

P = Path("D:/Projects/_preservation")
STEM = "SR_SHADOW_DB_trading-sbx__post-1605_17-Sep-2026__captured_2026-09-17T1758IST__FILE_"
WANT = {"sr_shadow.db": "7fa6dbc83b3408dbb8c57433b518b421", "sr_shadow.db-wal": "e420327f089ecfd34484dd5c0776bba8"}
CRONLOG = P / "EVALUATOR_CRONLOG_trading-sbx__post-1605_17-Sep-2026__captured_2026-09-17T1751IST.log"
HERE = Path(__file__).resolve().parent


def p(*a):
    print(" ".join(str(x) for x in a).encode("ascii", "backslashreplace").decode("ascii"))


def md5(b):
    return hashlib.md5(b).hexdigest()


src = {}
for name, want in WANT.items():
    b = (P / (STEM + name + ".copy")).read_bytes()
    assert md5(b) == want, ("preserved copy drifted", name)
    src[name] = b
assert md5(CRONLOG.read_bytes()) == "d0e7d4a378957f53a4817a8bf38df5cd", "cron log copy drifted"

wa, wb = HERE / "work_immutable", HERE / "work_wal"
for d in (wa, wb):
    d.mkdir(exist_ok=False)
(wa / "sr_shadow.db").write_bytes(src["sr_shadow.db"])
(wa / "sr_shadow.db-wal").write_bytes(src["sr_shadow.db-wal"])
(wb / "sr_shadow.db").write_bytes(src["sr_shadow.db"])
(wb / "sr_shadow.db-wal").write_bytes(src["sr_shadow.db-wal"])
p("python", sys.version.split()[0], "sqlite", sqlite3.sqlite_version)

Q_TABLES = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"


def counts(con, label):
    tabs = [r[0] for r in con.execute(Q_TABLES)]
    out = {t: con.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0] for t in tabs}
    p(label, "tables+rowcounts", out)
    return out


ca = sqlite3.connect((wa / "sr_shadow.db").as_uri() + "?immutable=1", uri=True)
a = counts(ca, "A_IMMUTABLE")
a_runs = ca.execute("SELECT rowid, run_at, target_date, length(stats_json) FROM evaluation_runs ORDER BY rowid").fetchall() if "evaluation_runs" in a else None
p("A_IMMUTABLE evaluation_runs rows", a_runs)
ca.close()

cb = sqlite3.connect(str(wb / "sr_shadow.db"))
p("B_WAL journal_mode", cb.execute("PRAGMA journal_mode").fetchone()[0])
b = counts(cb, "B_WAL")
for (name, sql) in cb.execute("SELECT name, sql FROM sqlite_master WHERE type IN ('table','index') ORDER BY type, name"):
    p("SCHEMA", name, "|", " ".join((sql or "").split()))
runs = cb.execute("SELECT rowid, run_at, target_date, length(stats_json) FROM evaluation_runs ORDER BY rowid").fetchall()
p("B_WAL evaluation_runs rows", runs)
grp = cb.execute("SELECT target_date, count(*) FROM evaluation_runs GROUP BY target_date ORDER BY target_date").fetchall()
p("B_WAL evaluation_runs by target_date", grp)
exact = cb.execute("SELECT count(*) FROM evaluation_runs WHERE target_date = ?", ("2026-09-17",)).fetchone()[0]
neg = cb.execute("SELECT count(*) FROM evaluation_runs WHERE target_date = ?", ("2026-09-18",)).fetchone()[0]
p("B_WAL exact-literal 2026-09-17 =", exact, "| group value =", dict(grp).get("2026-09-17"), "| NEG control 2026-09-18 =", neg)

log_obj = json.loads(CRONLOG.read_text(encoding="utf-8").strip())
for rowid, run_at, td, n in runs:
    if td != "2026-09-17":
        continue
    sj = json.loads(cb.execute("SELECT stats_json FROM evaluation_runs WHERE rowid=?", (rowid,)).fetchone()[0])
    p("ROW", rowid, "run_at", run_at, "stats keys", sorted(sj.keys()) if isinstance(sj, dict) else type(sj).__name__)
    p("  equals cron-log whole object:", sj == log_obj)
    p("  equals cron-log['statistics']:", sj == log_obj.get("statistics"))
    if isinstance(sj, dict):
        for k in sorted(set(sj) | set(log_obj)):
            if sj.get(k) != log_obj.get(k):
                p("  DIFF key", k, "| db:", json.dumps(sj.get(k), sort_keys=True)[:300], "| log:", json.dumps(log_obj.get(k), sort_keys=True)[:300])
cb.close()
p("DELTA rowcounts B_WAL minus A_IMMUTABLE", {t: b[t] - a.get(t, 0) for t in b})
