---
name: fix2-shell-dir-awaiting-rama-13aug
description: The trading-system-fix2 shell directory is not deleted, awaiting Rama
metadata:
  type: project
---


## Index line relocated from `MEMORY_BOARD.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 556 B (budget 450 B). The index now carries a hook and this link.

- 🗑️⏸️🔝 **`D:/Projects/trading-system-fix2` SHELL — ⏸️ **NOT DELETED, AWAITING RAMA**: his `rmdir` REFUSED (*"Not a directory"*, exit 1) because `venv` is a **DANGLING SYMLINK** → the removed `trading-system-capcarry/venv` (born 10-Aug 13:23:42).** ⭐ **The command's own guard stopped it — *"the protection is in the command, not in my authorisation."*** 📌 **The correct fail-safe shape for a symlink is plain `rm` (⛔ no flags) — ⛔ NOT substituted on my own authority.** ⚪ 0 files, 8.0K; no `.git`, de-registered already.
