---
name: scripts/preflight_scanner_check.py built and locked (PF1-PF8)
description: Standalone CLI pre-flight scanner check; thin wrapper around check_scanner_connectivity(); 17 tests
type: project
originSessionId: 657b84bc-8102-4180-b1a5-946a01b3f62f
---
Module: scripts/preflight_scanner_check.py (PF1-PF8)
New tests: 17 (test_preflight_scanner.py)
Running total: 1128

**Design:**
- Thin wrapper around `utils.startup_checks.check_scanner_connectivity()` — no duplicate HTTP logic (PF6)
- `_make_capturing_fetcher(snippets, timeout_override)` wraps `requests.get`, captures body snippets keyed by URL for --verbose display without re-fetching
- CLI: `--config PATH`, `--verbose`, `--timeout N`; exit 0=all OK, 1=any failure

**Cross-module:** utils.startup_checks (reuse check_scanner_connectivity)

Running total after both M35+M36: 1178

**Why:** Operator pre-market sanity check that all 15 Chartink scanners are reachable before starting main.py.
**How to apply:** Keep as thin wrapper; all scanner logic lives in startup_checks.
