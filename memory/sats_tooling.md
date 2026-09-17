---
name: sats-tooling
description: "SATS static-analysis tooling (Bandit + Semgrep) — PC-only, manual on-demand .bat scan scripts under sats\\"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0732f4c1-94e3-4fd5-aa1c-b47d2ff1ed94
---

Static analysis (SAST) for the trading system lives in `D:\Projects\trading-system\sats\`
— **PC-only, git-ignored, never deploys to the VM**. Two pre-installed isolated venvs hold
the scanners; **do NOT modify / activate / reinstall them**:
- Bandit **1.9.4** → `sats\bandit-env\Scripts\bandit.exe`
- Semgrep **1.167.0** → `sats\semgrep-env\Scripts\semgrep.exe`

**On-demand manual scans only** (no pre-commit hooks, no automation) — double-click:
- `sats\scripts\scan_bandit.bat`
- `sats\scripts\scan_semgrep.bat`

Each scans the repo root, **excludes `venv,sats,.git`**, writes a timestamped report to
`sats\reports\{bandit,semgrep}_<yyyyMMdd_HHmmss>.txt`, and echoes it to the console. Both
`.bat`s use `chcp 65001`, a locale-independent PowerShell timestamp (`Get-Date -Format
yyyyMMdd_HHmmss`), auto-create `reports\`, and run the tool ONCE (`-o`/`--output` → `type`).
Semgrep rulesets = `p/python` + `p/security-audit` (login-free; first run downloads from the
registry — needs internet once — cached after). Bandit reports all severities — add `-ll` to
filter to medium+ if noisy.

**Bandit `-x` uses absolute paths** (`...\venv,...\sats,...\.git`) on purpose: `bandit/core/
manager.py` tests each exclude token both as an fnmatch glob AND as a path substring, and
existing dirs get `\*` appended — absolute paths match via both branches regardless of the
`.bat`'s working dir, and won't catch the project's own root `scripts\`/`reports\`.

**Windows UTF-8 (critical):** both `.bat`s set `PYTHONUTF8=1`. Without it Semgrep AND Bandit
**crash** with `UnicodeEncodeError` writing the `--output`/`-o` report on this PC — Python defaults
to cp1252 for file writes and findings contain non-ASCII (em-dashes, box chars, code snippets).
`chcp 65001` only sets the CONSOLE code page; it does NOT fix Python file writes. (Found 22-Jun when
the first real scan crashed.)

**Semgrep baseline:** `sats\semgrep_baseline.txt` pins a commit (currently `65439ff`); when present,
`scan_semgrep.bat` adds `--baseline-commit <hash>` and runs from the repo root, so only findings NEW
since that commit show. It is git-diff-aware — it evaluates only files COMMITTED-changed since the
baseline (uncommitted edits aren't scanned until committed). Delete the file for a full scan. This is
the chosen way to silence reviewed false positives — NOT scattered `# nosemgrep`. See [[sats_triage_22jun]].

Created 22-Jun-2026 (VS Code Claude), updated same day with the PYTHONUTF8 + baseline facts. Also
recorded in SYSTEM_MAP.md (PC Paths → SATS + Changelog) and PATHS.md. Related: [[task_4_system_map]].
