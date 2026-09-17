---
name: instance-lock-flake-mechanism-27jul
description: "The test_instance_lock flake is NOT 'PC-env/Windows' — it is a 120-second orphan child process this test class spawns and fails to reap. Corrects four ledger entries that recorded the wrong cause."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9cadf64c-e510-4d81-a606-31dcc47fea07
  modified: 2026-07-27T03:09:44.626Z
---

**⛔ NEVER label the `test_instance_lock` failures "PC-env", "Windows flake", or "an external
process". That was recorded as fact for nine days and is wrong.** Found 27-Jul by source reading only
(no suite run). Full analysis: `docs/audit/instance_lock_flake_mechanism_27jul2026.md` (⛔ deliberately
UNCOMMITTED on 27-Jul — the Monday card asserts 24 commits; commit it after the push).

## The mechanism

`_holder_process()` (`tests/unit/test_instance_lock.py:39-58`) spawns a real child that takes the
machine-global lock and then **`time.sleep(120)`**. It is a bare `Popen` — no job object, no `atexit`,
no session fixture — so **it is not killed when pytest dies**. Any run that ends without reaping one
leaves a **live process holding `%TEMP%\trading-system.lock` for up to two minutes**. The next
invocation inside that window is refused, naming a PID that is **alive and different every run**.
That is the entire symptom. The racing parties are this class's own children across overlapping runs.

⭐ **Self-amplifying:** the `assert line == "ACQUIRED"` at `:57` fires **before `return proc`**, so the
caller never binds `holder` and the `finally: _reap(holder)` never runs — a poisoned run leaks another
child.

⭐ **Why the count wobbles 2/1/2 on an unchanged tree:** it depends only on wall-clock spacing between
invocations. There is also **no `pytest.ini`/`pyproject.toml`/`setup.cfg`/`tox.ini` anywhere in the
repo** ⇒ no ordering pin at all. [[feedback-no-fixed-test-baseline]]

## Three more test-side defects found with it

- **Hardcoded port collision 59996:** `test_instance_lock.py:280` asserts it AVAILABLE;
  `test_phase17_batch3.py:67` **binds+listens** on it. That module isolated its *own* ports (`:34-36`)
  and then used bare 59996–59999 anyway.
- **`test_phase17_batch3.py::test_fix081` is a second holder with NO cleanup** — the file has no
  classes, no fixtures, no teardown, no try/finally. A raise between `:71` and `:84` leaks the lock
  *and* the socket for the rest of the process.
- **The suite breaks the invariant it also asserts:** `instance_lock.py:35-39` says the lock file is
  never unlinked, and `test_release_leaves_the_file_in_place` asserts it — yet
  `test_instance_lock.py:181` and `test_phase17_batch3.py:70` both unlink it. On Linux that is the
  **false-pass** direction (two holders, two inodes, guard silently absent).

## Ledger corrections

- ❌ `live_seed_mc1_wired_18jul2026.md:286` — "naming PID 8708, **which is not running**" reads a field
  `instance_lock.py:22-24` documents as **informational only**; a dead PID there is BY DESIGN
  (`test_succeeds_when_stale_lock_dead_pid` writes `999999999`). "Names a different PID than the
  spawned one" is the **specification**, not a symptom. [[feedback-verify-the-finding-premise]]
- ❌ same — "PC-only, all pass on the VM": not a platform property; the VM just never overlapped two
  invocations. This label is what closed the investigation.
- ❌ `p1_health_require_hmac_done_17jul2026.md:117` — "Windows concurrent-process / file-lock flake".
- ⚠️ `capital_snapshot_redirect_25jul2026.md:128` — conclusion (not attributable) stands, label wrong.
- ✅ `clock_dependency_class_26jul2026.md:204-209` — closest, and **the "never run suites in parallel"
  rule is sound — but incomplete**: the 120 s orphan makes *sequential* runs contend when merely close
  together. Following that rule alone will not stop the flake.
- ✅ **REFUTED cleanly:** `test_main.py` is NOT a contender — `:312-313` `MagicMock`s both
  `acquire_instance_lock` and `release_instance_lock`.

## LATENT production finding — do not stop for it

`utils/instance_lock.py:176` sets `_lock_fd = fd` **without closing the previous fd**; a leaked fd
still holds the kernel lock. **Unreachable in production** — `main.py:1801` calls acquire exactly
once inside a `try/finally` releasing at `:1808`. ⇒ LATENT: document + pin, do not fix now.
[[feedback-live-vs-latent-findings]]

## Fix — designed, NOT applied

Test-only and contained, but unverifiable without running the suite ⇒ deferred to an evening.
(1) child blocks on stdin instead of `sleep(120)` so it dies with its parent; (2) reap on the refusal
path; (3) monkeypatch `il._LOCK_FILE` to `tmp_path` in a session fixture — `tests/conftest.py`'s
`_isolate_real_sentinels` is the in-tree precedent; (4) own port + `try/finally` for `test_fix081`,
and drop both test-side `unlink()`s.
⛔ **Never weaken `test_p1` or the two `test_p2` restart tests** — two instances trading one book
double every order, and a guard that wrongly refuses a start is its own outage. **The flake is in the
fixture, never in the property.**
