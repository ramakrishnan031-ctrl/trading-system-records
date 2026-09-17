"""Generate the force_qty DELIVER and ROLLBACK command files for the testing VM from the Gate 4 guarded-write
template (SYSTEM_MAP line quoted in the build record), plus SANDBOX variants that differ ONLY in the transport
(`ssh -o BatchMode=yes trading-sbx '...'` -> `bash -c '...'`) and the cd target. Refuses to overwrite. ASCII only."""
import hashlib
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = "/d/Projects/_preservation"
BUILD = f"{P}/FORCE_QTY_BUILD_17-Sep-2026__worktree-bytes_captured_2026-09-17T1859IST"
NEWCFG = f"{P}/TWIN_system_config_FORCE-QTY_md5-12d79b2a__built-validated_2026-09-17T1902IST.yaml"
OLDCFG = f"{P}/TWIN_system_config_POST-SR-SHADOW_md5-4eab1ae5__preserved_2026-09-16T0208IST.yaml"
WT = "D:/Projects/wt-sr-shadow-15sep"
VMROOT = "/home/ubuntu/systems/trading-system"

FILES = [  # delivery order: loader -> sizer -> main -> config
    ("core/config_loader.py", "5b27302483de514ec3117442267609f3", "2030714e78d55b0a8a4ea8db58a987ae",
     f"cat {BUILD}/core/config_loader.py", f"git -C {WT} show e7bf477:core/config_loader.py"),
    ("capital/position_sizer.py", "a9775db87f1d2c74d01966e615bfc97b", "b2b27684244691d2fdcd15eae7d97837",
     f"cat {BUILD}/capital/position_sizer.py", f"git -C {WT} show e7bf477:capital/position_sizer.py"),
    ("main.py", "5aacc1b8028682405834b7dd6238ab5a", "277b07028d5e265aab74ce026787ecc8",
     f"cat {BUILD}/main.py", f"git -C {WT} show e7bf477:main.py"),
    ("config/system_config.yaml", "4eab1ae5a9716059431b55a210e917c9", "12d79b2a03a4becd989baae56078e058",
     f"cat {NEWCFG}", f"cat {OLDCFG}"),
]


def md5_of(cmd):
    return hashlib.md5(subprocess.run(["C:/Program Files/Git/usr/bin/bash.exe", "-c", cmd], capture_output=True, check=True).stdout).hexdigest()


# the sources must produce exactly the bytes the guards expect
for f, old, new, src_new, src_old in FILES:
    assert md5_of(src_new) == new, (f, "new source")
    assert md5_of(src_old) == old, (f, "old source")


def guarded(src, f, want_old, want_new, root, transport):
    body = (f'cd {root} && cur=$({{ md5sum < {f}; }} 2>/dev/null | cut -c1-32); '
            f'if [ "$cur" = "{want_new}" ]; then cat > /dev/null; echo "ALREADY_DONE {f}"; exit 0; fi; '
            f'if [ "$cur" != "{want_old}" ]; then cat > /dev/null; echo "REFUSED_DRIFT {f} have=${{cur:-NONE}} want={want_old}"; exit 1; fi; '
            f'cat > {f}.tmp && [ "$(md5sum < {f}.tmp | cut -c1-32)" = "{want_new}" ] && chmod --reference={f} {f}.tmp '
            f'&& mv -- {f}.tmp {f} && echo "WROTE {f}" || {{ rm -f -- {f}.tmp; echo "REFUSED_WRITE {f}"; exit 1; }}')
    assert "'" not in body
    return f"{src} | {transport} '{body}'"


def build(root, transport):
    deliver = [guarded(sn, f, o, n, root, transport) for f, o, n, sn, so in FILES]
    rollback = [guarded(so, f, n, o, root, transport) for f, o, n, sn, so in reversed(FILES)]
    return " && \\\n".join(deliver) + "\n", " && \\\n".join(rollback) + "\n"


real_d, real_r = build(VMROOT, "ssh -o BatchMode=yes trading-sbx")
sb_root = (HERE / "sandbox_vm").as_posix()
sb_d, sb_r = build(sb_root, "bash -c")
assert real_d.replace("ssh -o BatchMode=yes trading-sbx", "bash -c").replace(VMROOT, sb_root) == sb_d
assert real_r.replace("ssh -o BatchMode=yes trading-sbx", "bash -c").replace(VMROOT, sb_root) == sb_r
for name, text in (("DELIVER_forceqty_testing-vm.sh", real_d), ("ROLLBACK_forceqty_testing-vm.sh", real_r),
                   ("SANDBOX_deliver.sh", sb_d), ("SANDBOX_rollback.sh", sb_r)):
    with open(HERE / name, "x", encoding="ascii", newline="\n") as fh:
        fh.write(text)
    print(name, len(text.encode()), "B md5", hashlib.md5(text.encode()).hexdigest())
