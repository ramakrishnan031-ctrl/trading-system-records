# MUTATION AND FAILURE-ID EVIDENCE — 28-Aug-2026

Saved verbatim so a future reader diffs against a LIST, not a hash. The
fingerprint alone cannot discriminate between baselines: it hashes the sorted
failure IDs, and the standing ten are identical across all three gates below.
The PASS COUNT is the discriminator.

---

## 1 — EXACT FAILURE-ID LISTS, PER GATE

### effff24 (pushed baseline)

    SHA         effff24b8d3c5cec025d4ded60d030a5dca2e239
    totals      10 failed, 5956 passed, 4 skipped, 281 warnings in 1018.73s (0:16:58)
    fingerprint 46c38a3eee03d34be8defedba73421c803c6ba42e05375a8968632e4cb118f0b
    count       10

     1. tests/unit/test_closure_source_contract.py::test_no_module_restates_the_vocabulary_literals
     2. tests/unit/test_fix181.py::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active
     3. tests/unit/test_main.py::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret
     4. tests/unit/test_main.py::TestContinueFromGate::test_no_placer_releases_reservation_and_updates_status
     5. tests/unit/test_main.py::TestContinueFromGate::test_price_hit_calls_placer_with_correct_prices
     6. tests/unit/test_main.py::TestContinueFromGate::test_stats_placed_incremented_on_success
     7. tests/unit/test_phase17_batch2.py::test_fix077_flask_max_content_length
     8. tests/unit/test_t4_deploy_preflight.py::test_check_tz_fails_on_broken_utc_form
     9. tests/unit/test_t4_deploy_preflight.py::test_check_tz_passes_on_agreement
    10. tests/unit/test_t4_deploy_preflight.py::test_ist_now_emits_valid_ist

### 38de90f (COMMIT 1 extraction)

    SHA         38de90fd4dbc4d8b3c009fa63e84ab2ad0dc1a6b
    totals      10 failed, 5956 passed, 4 skipped, 281 warnings in 992.37s (0:16:32)
    fingerprint 46c38a3eee03d34be8defedba73421c803c6ba42e05375a8968632e4cb118f0b
    count       10

     1. tests/unit/test_closure_source_contract.py::test_no_module_restates_the_vocabulary_literals
     2. tests/unit/test_fix181.py::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active
     3. tests/unit/test_main.py::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret
     4. tests/unit/test_main.py::TestContinueFromGate::test_no_placer_releases_reservation_and_updates_status
     5. tests/unit/test_main.py::TestContinueFromGate::test_price_hit_calls_placer_with_correct_prices
     6. tests/unit/test_main.py::TestContinueFromGate::test_stats_placed_incremented_on_success
     7. tests/unit/test_phase17_batch2.py::test_fix077_flask_max_content_length
     8. tests/unit/test_t4_deploy_preflight.py::test_check_tz_fails_on_broken_utc_form
     9. tests/unit/test_t4_deploy_preflight.py::test_check_tz_passes_on_agreement
    10. tests/unit/test_t4_deploy_preflight.py::test_ist_now_emits_valid_ist

### 22a143f (COMMIT 2 F)

    SHA         22a143f6021597cf882d0d89ae6382b46b9b6292
    totals      10 failed, 5985 passed, 4 skipped, 281 warnings in 1064.64s (0:17:44)
    fingerprint 46c38a3eee03d34be8defedba73421c803c6ba42e05375a8968632e4cb118f0b
    count       10

     1. tests/unit/test_closure_source_contract.py::test_no_module_restates_the_vocabulary_literals
     2. tests/unit/test_fix181.py::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active
     3. tests/unit/test_main.py::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret
     4. tests/unit/test_main.py::TestContinueFromGate::test_no_placer_releases_reservation_and_updates_status
     5. tests/unit/test_main.py::TestContinueFromGate::test_price_hit_calls_placer_with_correct_prices
     6. tests/unit/test_main.py::TestContinueFromGate::test_stats_placed_incremented_on_success
     7. tests/unit/test_phase17_batch2.py::test_fix077_flask_max_content_length
     8. tests/unit/test_t4_deploy_preflight.py::test_check_tz_fails_on_broken_utc_form
     9. tests/unit/test_t4_deploy_preflight.py::test_check_tz_passes_on_agreement
    10. tests/unit/test_t4_deploy_preflight.py::test_ist_now_emits_valid_ist

### SET COMPARISON (comm), not by eye

    COMMIT 1 vs effff24 : NEW=[] MASKED=[]
    COMMIT 2 vs effff24 : NEW=[] MASKED=[]
    identical to baseline: COMMIT 1 = True · COMMIT 2 = True

    Three of the ten (test_t4_deploy_preflight) are the known venv-less
    environment artefact. The label does NOT remove them from the standing set;
    they are inside every fingerprint above.

---

## 2 — F MUTATIONS — THE EXACT NINE

Each names an observed unsafe EVENT, not "goes RED".

```
MUTATION                                     RESULT               UNSAFE EVENT IT WOULD ALLOW
======================================================================================================================
TEST C  F imports the orchestrator          RED                  F coupled to the orchestrator
TEST D  the instance-sharing refactor becomes possible RED                  lifecycle coupling reintroduced
PARTIAL treated as success                   RED                  a half-delivered incident reads as OK
one channel's failure skips the other        RED                  evidence erased by the other channel's failure
send awaited instead of bounded              RED                  F itself causes a DEADLINE_BREACH
timeout dropped silently                     RED                  a dead transport reads green
self-test becomes a health latch             RED                  stale 08:15 PASS reads as 15:07 cover
pre-pass hardcoded to 15:05                  RED                  F drifts when the cutoff moves
a CRITICAL branch unwired                    RED                  that incident is invisible
======================================================================================================================
ALL MUTATIONS RED: True
restored md5 check: OK
TREE CLEAN AFTER RUN: yes
```

## 3 — ORCHESTRATOR MUTATIONS — TWELVE, re-run at 22a143f from a clean tree

The count is **TWELVE**, not fourteen. Fourteen conflated this twelve-entry
harness with two one-off mutations run separately for the GTT-separation test;
those two were real and RED, but they are not in this table and must not be
counted into it.

```
MUTATION                                         FILE PATCHED               TEST                                 RESULT
============================================================================================================================
MIS_PRODUCT -> CNC                               mis_autosquareoff.py       test_product_boundary_mis_only_cnc   RED
MIS_PRODUCT -> CO                                mis_autosquareoff.py       test_co_position_produces_zero_ord   RED
product predicate widened to {MIS,CNC}           mis_autosquareoff.py       test_only_exact_mis_is_eligible      RED
_product_of defaults absent product to MIS       mis_autosquareoff.py       test_12_missing_product_excluded_i   RED
qty != 0  ->  qty > 0                            mis_autosquareoff.py       test_short_position_closes_with_a_   RED
drop cancel-before-exit guard                    mis_autosquareoff.py       test_cancel_failure_blocks_the_exi   RED
remove R-2 max(0,...) floor                      mis_autosquareoff.py       test_a1_grace_floor_never_negative   RED
remove R-2 cap entirely                          mis_autosquareoff.py       test_21_grace_capped_when_pass_1_i   RED
PASS 2 reads the general limit_grace_sec         mis_autosquareoff.py       test_pass_2_order_type_is_market_n   RED
shared fired flag instead of per-pass            mis_autosquareoff.py       test_27_per_pass_flags_pass_2_stil   RED
drop the margin >= poll_interval floor           mis_squareoff_timing.py    test_28_margin_below_poll_interval   RED
query failure returns [] instead of raising      mis_autosquareoff.py       test_query_failure_is_never_flat     RED
============================================================================================================================
MUTATIONS RUN: 12   RED: 12
ALL MUTATIONS RED: True
TREE CLEAN AFTER RUN: yes
```

### The ANCHOR-MISSING row, and what it cost

An earlier re-run of this table returned **eleven RED and one ANCHOR-MISSING**
-- `drop the margin >= poll_interval floor` -- and its own footer read
`ALL MUTATIONS RED: False`. ANCHOR-MISSING is **not RED**: it means the harness
never mutated anything, so it is not evidence of anything. That row was
nonetheless reported as though the set were all-RED. It was not.

**Cause: tooling, not a defect in the code.** COMMIT 1 (38de90f) moved
`MisSquareoffTiming.build()` out of `orders/mis_autosquareoff.py` into
`core/mis_squareoff_timing.py`. The harness still patched the orchestrator, so
the anchor could not match. Determined by measurement, not inference:

    grep -c 'if margin_sec < poll_interval_sec:' orders/mis_autosquareoff.py -> 0
    grep -rn 'margin_sec < poll_interval_sec'    core/ -> core/mis_squareoff_timing.py:129
    build(margin_sec=4, poll_interval_sec=5)     -> MisSquareoffConfigError raised

The validation is exactly where it was designed to be and still fails closed;
only its FILE changed. The harness now records the file it patched per row, so
this cannot recur silently.

### A second defect the fix exposed: a CONTAMINATED BASELINE

Fixing the anchor surfaced a different row as ANCHOR-MISSING
(`shared fired flag instead of per-pass`). `git status` showed
`orders/mis_autosquareoff.py` **modified**: line 233 read `PASS_1` where the
shipped file reads `PASS_2`. That is mutation #10, still applied to disk.

An intermediate edit of the harness crashed with `ValueError: too many values
to unpack` **at** the newly-5-tuple entry #11 -- after iterations 1..10 had each
written their mutation to disk, and before the single end-of-loop restore could
run. The file stayed mutated. Every subsequent row was then measured against a
file that was already wrong, so a RED could have come from the standing
mutation rather than the intended one. **That entire run was discarded.**

Three changes, so it cannot happen again:

* restore is now **per mutation**, not once at the end, with an `assert` that
  the file came back byte-identical;
* `git status --porcelain` is checked **before and after** every run -- a dirty
  tree refuses to run rather than producing contaminated RED;
* the table prints the file each mutation patched.

The table above was produced after `git checkout --` restored the file and
`git diff --quiet HEAD` confirmed it identical to 22a143f.

---

## 4 — TEST B: THE REAL REFACTOR RUN AS THE MUTATION

Not "add an unused parameter" -- the actual thing a developer would do:
*"both build the same timing object, so build it once and pass it in."*
The mutation ACCEPTS the parameter AND HONOURS it, then a caller passes the
orchestrator's own instance.

```
==============================================================================
MUTATION APPLIED: F now accepts AND honours an injected timing instance
==============================================================================

[1] TEST B under the mutation : RED
     E       AssertionError: F accepts injectable timing/orchestrator state ['timing'] -- the instance-sharing refactor is now possible
     E       assert not {'timing'}
     tests\unit\test_mis_squareoff_notifier.py:256: AssertionError
    failing assertion: E       AssertionError: F accepts injectable timing/orchestrator state ['timing'] -- the instance-sharing refactor is now possible

[2] passing the orchestrator's instance, WITH the mutation:
     INJECTED_OK True

MUTATION REVERTED: OK

[3] the same injection, WITHOUT the mutation (shipped code):
     REJECTED MisSquareoffNotifier.__init__() got an unexpected keyword argument 'timing'

[4] TEST B on restored shipped code : GREEN
```

### What this establishes, and its one limit

* TEST B goes **RED** under the real refactor.
* Under the mutation the coupling is genuinely achieved: `f.timing is
  orch_timing` -> **True**. Not hypothetical.
* On shipped code the same injection is **impossible**: TypeError, unexpected
  keyword argument 'timing'.

* LIMIT, stated plainly: the assertion that fires is the SIGNATURE check
  ("no parameter exists through which a prebuilt timing can be injected"),
  NOT the identity assertion. `f.timing is not orch_timing` still cannot fail
  from inside TEST B, because TEST B does not pass a timing -- F builds its
  own. The identity line documents intent; the SIGNATURE line is what carries
  the red-capability. Both are kept: the first states the invariant, the
  second enforces it.

---

## 5 — WAS THE COMMIT 2 GATE INSIDE THE CONTAMINATION WINDOW? NO.

The gate tests the WORKING TREE, so a gate that overlapped the dirty span
would be void exactly as the mutation run was. Settled by timestamps AND by
re-measurement -- not by argument.

    22a143f committed         21:59:08
    gate STARTED             ~22:00:33   (22:18:17 minus its own 1064.64s)
    gate FINISHED             22:18:17   <- mtime of gate_commit2.txt
    contaminating crash      ~23:0x      (this session, 46 min later)

Two independent lines agree:

* **Structural.** The crash was `ValueError: too many values to unpack
  (expected 4)`, raised by the 5-tuple harness entry. That 5-tuple did not
  exist until the anchor fix was written tonight, so the crash was NOT
  REACHABLE at 22:00. A failure mode that does not yet exist cannot have fired.
* **Empirical.** The prior run's own table records
  `shared fired flag -> RED`, which requires the `PASS_2` anchor to have
  matched -- i.e. the file was shipped-clean when that run began -- and that
  run completed its restore.

### The decisive check: the gate re-run from a verified-clean tree

    tree                git status --porcelain EMPTY, HEAD 22a143f, before AND after

    RECORDED 22:18:17   10 failed, 5985 passed, 4 skipped   in 1064.64s
    RE-RUN   clean      10 failed, 5985 passed, 4 skipped   in  906.13s

    fingerprint RECORDED 46c38a3eee03d34be8defedba73421c803c6ba42e05375a8968632e4cb118f0b
    fingerprint RE-RUN   46c38a3eee03d34be8defedba73421c803c6ba42e05375a8968632e4cb118f0b

    NEW    (re-run minus recorded) : EMPTY
    MASKED (recorded minus re-run) : EMPTY

Identical failure set, identical fingerprint, identical pass count.
**The 5,985 gate stands. It was NOT inside the contamination window.**

Note the pass count is what discriminates here, not the fingerprint: the
standing ten are identical across every gate in this document, so the hash
alone could not have told these runs apart.
