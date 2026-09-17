"""Offline, read-only: run the testing VM's OWN content_drift() on the VM's OWN inputs.

Inputs are local copies fetched read-only from trading-sbx; md5 asserted before use.
No VM contact, no DB, no .env, no broker. check_cron_drift.py is NOT imported (its
module level calls load_dotenv and imports the state store); the two definitions are
lifted from the VM copy with ast and executed against generate_crontab's helpers.
Stdout is ASCII only; the full result goes to a UTF-8 file.
"""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

S = Path(__file__).resolve().parent
EXPECT = {
    "blob970_generate_crontab.py": "564adf9c1cb9da9c8754f255bca6cfbd",   # = VM md5
    "scripts_check_cron_drift.py": "3d43f51c1b92b2d697389bcdd735c01a",   # VM copy (CRLF)
    "config_cron_registry.yaml": "ae9b22a15e69ca786c718c9c893a3ca4",     # VM copy
    "vm_crontab_live.txt": "d0b9a184da7dc8aeea507f7dc80d7073",           # VM crontab -l
}
for name, want in EXPECT.items():
    have = hashlib.md5((S / name).read_bytes()).hexdigest()
    assert have == want, f"INPUT DRIFT {name}: have {have} want {want}"
print("inputs: 4/4 md5 match")

spec = importlib.util.spec_from_file_location("gen970", S / "blob970_generate_crontab.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

src = (S / "scripts_check_cron_drift.py").read_text(encoding="utf-8")
tree = ast.parse(src)
wanted = {"ContentDrift", "content_drift"}
nodes = [n for n in tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name in wanted]
assert {n.name for n in nodes} == wanted, "definitions not found in the VM copy"
ns = {
    "__name__": "lifted",
    "Path": Path,
    "load_jobs": gen.load_jobs, "parse": gen.parse, "compose": gen.compose,
    "_command_lines": gen._command_lines, "resolve_job_name": gen.resolve_job_name,
}
exec(compile("from __future__ import annotations\n", "<future>", "exec"), ns)
exec(compile(ast.Module(body=nodes, type_ignores=[]), "check_cron_drift.py(VM,lifted)", "exec"), ns)
content_drift = ns["content_drift"]

reg = S / "config_cron_registry.yaml"
live = (S / "vm_crontab_live.txt").read_text(encoding="utf-8")


def run(registry_path, crontab_text):
    cd = content_drift(registry_path, crontab_text)
    return {
        "absent_critical": list(cd.absent_critical),
        "absent_warn": list(cd.absent_warn),
        "unregistered": list(cd.unregistered),
        "unparseable": list(cd.unparseable),
        "has_critical": cd.has_critical,
        "has_any": cd.has_any,
    }


result = {"REAL": run(reg, live)}

# CONTROL A -- a registered, enabled job's line removed => it must appear in absent_critical
lines = live.splitlines(keepends=True)
drop = [i for i, ln in enumerate(lines) if "scripts/check_cron_drift.py" in ln and not ln.startswith("#")]
assert len(drop) == 1, drop
ctl_a = "".join(ln for i, ln in enumerate(lines) if i != drop[0])
result["CONTROL_A_drop_check_cron_drift_line"] = run(reg, ctl_a)

# CONTROL B -- the evaluator line made unparseable (double space after the minute field)
ev = [i for i, ln in enumerate(lines) if "scripts/sr_shadow_evaluate.py" in ln and not ln.startswith("#")]
assert len(ev) == 1, ev
ctl_b_lines = list(lines)
ctl_b_lines[ev[0]] = ctl_b_lines[ev[0]].replace("5 16 ", "5  16 ", 1)
result["CONTROL_B_evaluator_line_unparseable"] = run(reg, "".join(ctl_b_lines))

# CONTROL C -- the evaluator registered (scratch registry copy) => it must leave `unregistered`
import yaml  # noqa: E402
data = yaml.safe_load(reg.read_text(encoding="utf-8"))
f = gen.parse(lines[ev[0]].rstrip("\n"))
data2 = copy.deepcopy(data)
data2["jobs"]["sr_shadow_evaluate"] = {
    "enabled": True, "cron_expression": f["cron_expression"], "env_wrapper": f["env_wrapper"],
    "command": f["command"], "log_target": f["log_target"],
}
reg_c = S / "CONTROL_C_registry_scratch.yaml"
reg_c.write_text(yaml.safe_dump(data2, sort_keys=False), encoding="utf-8")
result["CONTROL_C_evaluator_registered"] = run(reg_c, live)

out = S / "content_drift_offline_result.json"
out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

for k, r in result.items():
    print(f"{k}: has_critical={r['has_critical']} absent_critical={len(r['absent_critical'])} "
          f"absent_warn={len(r['absent_warn'])} unregistered={len(r['unregistered'])} "
          f"unparseable={len(r['unparseable'])}")
    print("   absent_critical:", ",".join(r["absent_critical"]).encode("ascii", "replace").decode())
    for u in r["unregistered"] + r["unparseable"]:
        print("   line:", u[:60].encode("ascii", "replace").decode(), "...", u[-45:].encode("ascii", "replace").decode())
print("wrote", out.name, out.stat().st_size, "B")
