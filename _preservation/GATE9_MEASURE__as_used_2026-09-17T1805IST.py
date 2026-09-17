"""Gate 9 -- MEASUREMENT ONLY -- on a fresh scratch copy of the preserved 17-Sep shadow DB (main + WAL, md5-asserted).
Every number carries n, window, source. No tuning, no attribution. Recomputes the per-variant/per-decision
outcome counts from shadow_rows and compares them with the stored run's stats_json. ASCII stdout."""
import collections
import hashlib
import json
import sqlite3
from pathlib import Path

P = Path("D:/Projects/_preservation")
STEM = "SR_SHADOW_DB_trading-sbx__post-1605_17-Sep-2026__captured_2026-09-17T1758IST__FILE_"
WANT = {"sr_shadow.db": "7fa6dbc83b3408dbb8c57433b518b421", "sr_shadow.db-wal": "e420327f089ecfd34484dd5c0776bba8"}
W = Path(__file__).resolve().parent / "work_gate9"


def p(*a):
    print(" ".join(str(x) for x in a).encode("ascii", "backslashreplace").decode("ascii"))


W.mkdir(exist_ok=False)
for name, want in WANT.items():
    b = (P / (STEM + name + ".copy")).read_bytes()
    assert hashlib.md5(b).hexdigest() == want, name
    (W / name).write_bytes(b)
con = sqlite3.connect(str(W / "sr_shadow.db"))
con.row_factory = sqlite3.Row
rows = [dict(r) for r in con.execute("SELECT * FROM shadow_rows")]
spool = [dict(r) for r in con.execute("SELECT signal_id, captured_at, status, attempts, last_error, updated_at FROM spool")]
run = con.execute("SELECT run_id, run_at, target_date, stats_json FROM evaluation_runs").fetchall()
assert len(run) == 1
stats = json.loads(run[0]["stats_json"])["statistics"]
SRC = "source: _preservation SR_SHADOW_DB ...T1758IST copies (VM sr_shadow.db + WAL, md5 7fa6dbc8.../e420327f...), scratch copy"
p(SRC)

p("---- n / window ----")
p("shadow_rows n =", len(rows), "| spool n =", len(spool), "| evaluation_runs n =", len(run), "run_at", run[0]["run_at"], "target", run[0]["target_date"])
C = collections.Counter
p("date:", dict(C(r["date"] for r in rows)), "| mode:", dict(C(r["mode"] for r in rows)))
for col in ("time_ist", "signal_timestamp_used", "captured_at", "decided_at", "evaluated_at"):
    vals = sorted(str(r[col]) for r in rows if r[col] is not None)
    p(f"{col}: non-null {len(vals)} of {len(rows)} | min {vals[0] if vals else None} | max {vals[-1] if vals else None}")
sp_c = sorted(str(s["captured_at"]) for s in spool)
p("spool captured_at: min", sp_c[0], "| max", sp_c[-1], "| status", dict(C(s["status"] for s in spool)),
  "| attempts by status", dict(C((s["status"], s["attempts"]) for s in spool)))
p("spool FAILED last_error (first 110 chars, counted):", dict(C((s["last_error"] or "")[:110] for s in spool if s["status"] == "FAILED")))
ids_rows, ids_done = {r["signal_id"] for r in rows}, {s["signal_id"] for s in spool if s["status"] == "DONE"}
p("shadow_rows signal_ids == spool DONE signal_ids ->", ids_rows == ids_done, "| rows-not-in-DONE", len(ids_rows - ids_done), "| DONE-not-in-rows", len(ids_done - ids_rows))

p("---- the two P counts (R-C) ----")
p("rows_with_trustworthy_p (p_provenance_available truthy) =", sum(1 for r in rows if r["p_provenance_available"]),
  "| p_provenance_available values", dict(C(r["p_provenance_available"] for r in rows)))
und = [r for r in rows if r["contract_formula_undefined_fields"] not in (None, "", "[]")]
p("rows_with_contract_formula_undefined_fields =", len(und), "| distinct values (first 160 chars):",
  dict(C(str(r["contract_formula_undefined_fields"])[:160] for r in und)))

p("---- decisions and outcomes, per variant (R-B: split per decision) ----")
p("shadow_decision:", dict(C(r["shadow_decision"] for r in rows)), "| decision_agreement_flag:", dict(C(r["decision_agreement_flag"] for r in rows)))
p("admission_status:", dict(C(r["admission_status"] for r in rows)), "| data_unavailable_sub_reason (decision-level):", dict(C(r["data_unavailable_sub_reason"] for r in rows)))
p("confirmation_status:", dict(C(r["confirmation_status"] for r in rows)), "| invariant_violation_flag:", dict(C(r["invariant_violation_flag"] for r in rows)))
for v in ("strict", "recency"):
    tab = C((r[v + "_decision"], r[v + "_outcome"], r[v + "_outcome_sub_reason"]) for r in rows)
    for k, n in sorted(tab.items(), key=lambda kv: (-kv[1], str(kv[0]))):
        p(f"  {v}: decision={k[0]} outcome={k[1]} sub={k[2]} -> {n}")
    p(f"  {v}: reject_code:", dict(C(r[v + "_reject_code"] for r in rows)))
    nullst = C((r[v + "_decision"], r[v + "_stop_v1"] is None, r[v + "_target"] is None) for r in rows if r[v + "_outcome"] is None)
    p(f"  {v}: rows with outcome NULL, by (decision, stop_v1 IS NULL, target IS NULL):", dict(nullst))
    # recompute the stored bucket the way the numbers are defined (non-null outcomes only, per decision)
    elig = [r for r in rows if not r["invariant_violation_flag"]]
    for d in sorted({str(r[v + "_decision"]) for r in elig if r[v + "_outcome"] is not None}):
        oc = C(r[v + "_outcome"] for r in elig if str(r[v + "_decision"]) == d and r[v + "_outcome"] is not None)
        st = stats["variants"][v]["by_decision"].get(d, {})
        mine = {"target_hit": oc.get("TARGET_HIT", 0), "stop_hit": oc.get("STOP_HIT", 0), "time_close": oc.get("TIME_CLOSE", 0),
                "ambiguous_same_bar": oc.get("AMBIGUOUS_SAME_BAR", 0), "counterfactual_entry_invalid": oc.get("COUNTERFACTUAL_ENTRY_INVALID", 0)}
        stored = {k: st.get(k) for k in mine}
        p(f"  {v}: by_decision[{d}] outcome counts from rows {dict(oc)} | recomputed == stored ->", mine == stored, "| stored", stored)
con.close()
