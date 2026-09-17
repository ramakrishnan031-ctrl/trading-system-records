---
name: project-crash-test-tools
description: All 12 crash test tools built and verified (05-Jun-2026); tests/crash_test/ directory; ready for Day 1 scenarios Jun 8
metadata: 
  node_type: memory
  type: project
  originSessionId: 176bf475-8dfe-4ee1-9083-166c16486ac8
---

All 12 crash test tools built and verified on 2026-06-05.
Location: tests/crash_test/ (PC) — needs SCP to VM.

**Why:** Infrastructure for Jun 8-12 crash test (5-day certification).
**How to apply:** Use these tools during crash test execution. Each tool is standalone CLI.

## Tools

| # | File | Verified | Notes |
|---|------|----------|-------|
| - | ct_utils.py | PASS | Shared utilities: DB, IST, Telegram, HTTP |
| 1 | invariant_checker.py | PASS | 8 invariants (A-H); `--full`/`--quick`/`--invariant X` |
| 2 | signal_injector.py | PASS | 6 modes: single/burst/flood/malformed/expired/duplicate; `--dry-run` |
| 3 | state_inspector.py | PASS | `--snapshot`/`--diff`/`--live` |
| 4 | network_controller.py | PASS | Linux/iptables only; Windows shows SKIPPED gracefully |
| 5 | scenario_runner.py | PASS | YAML-driven; `--dry-run`; master tracker skip logic |
| 6 | crash_test_reporter.py | PASS | Day/all aggregation; Telegram summary; markdown report |
| 7 | cleanup.py | PASS | `--soft`/`--hard`/`--nuclear`; safety gates for open positions |
| 8 | idempotency_tester.py | PASS | `--scenario X --runs N`; drift detection |
| 9 | exactly_once_verifier.py | PASS | 7 operation checks; `--date today`/`--window`/`--full` |
| 10 | state_machine_validator.py | PASS | orders/trades/signals transition validation |
| 11 | forensic_reconstructor.py | PASS | `--source db`/`--source logs`; broker deferred to Monday |
| 12 | resource_monitor.py | PASS | `--live`/`--start`/`--stop`/`--report`; needs psutil on VM |

## Sample scenario
- tests/crash_test/scenarios/ct001.yaml — CT001 Happy Path (day 1 sample)

## Known PC-only limitations
- resource_monitor: returns -1 metrics without psutil (VM has psutil)
- network_controller: Linux-only (shows graceful skip on Windows)
- invariant A: FAIL on local DB (no capital_snapshot row — expected; VM DB has it)

## Next steps
- SCP to VM: `scp -r tests/crash_test/ trading_vm:~/systems/trading-system/tests/`
- Create remaining scenario YAMLs for Day 1 (36 scenarios)
- Verify psutil installed on VM: `pip show psutil`
