---
name: alert-phase2-n907-09aug
description: Phase 2 (alert_watcher propagation, 071169b) and N9-07 (forward-shadow encoding, 7649cd8) built, gated and committed on their own branches. Tick 4 is BLOCKED on the sizing deploy, verified.
metadata:
  node_type: memory
  type: project
---

# 🔧 PHASE 2 + N9-07 — `<BUILT · TESTED · COMMITTED · NOT PUSHED · NOT DEPLOYED>`

## 🔴 PHASE 2 — `071169b` on `fix/alert-phase2-watcher`
⚠️ **BASE IS `fix/alert-remediation`, ⛔ NOT `main` — a DELIBERATE deviation from the card, stated rather than silent.** Phase 2 uses Phase 0's `alerts/delivery.py`, which exists only on that branch; branching off `main` would have required a **second copy of the delivery contract on a second branch** — exactly the "second mechanism" the contract forbids. ⭐ Still its own branch, own commit, own gate.
⚠️ **DIFFERENT SHAPE FROM PHASES 0/1, and that is the point: those added a record to an EXISTING swallow. Here there was NO swallow** — the send was unguarded — **so the fix STOPS THE PROPAGATION *and* records.** `send_alert_recorded` does both and returns exactly the delivered boolean the loop needs.
🔴🔴 **THE SWEEP'S CLASSIFICATION IS CORRECTED: this is not merely "observability".** `run_once` is called **UNGUARDED** from `run_loop` and from `main()` (whose `try` has only a `finally`), so an escaping `notifier.send` **killed the long-lived `--loop` watcher and exited non-zero — RE-CREATING the 10s systemd crash-loop that the file's own closing comment names as the original fault.** ⭐ Sentinels still persist so nothing is lost, but **the availability of the alert path itself was at stake.**
⭐ **Second defect closed by the same change: one raising sentinel used to abort every remaining sentinel in the pass.**
✅ RED-first **8F/3P → 11P**; the 3 pre-existing passes are MUST-NOT-CHANGE GUARDS. **GATE `PYTEST_RC=1` · 9F / 5,618P / 4S · 890 s — `NO NEW FAILURES`, 0 new, none missing; arithmetic closes exactly (5,607 + 11 = 5,618).**
⚠️ **PARITY: ⛔ NO paper coverage claimed. A CRON path, its own process, reading no mode flag ⇒ MODE-INDEPENDENT**, which is a different statement, and a test pins that no mode token appears in the module.

## 📄 N9-07 — `7649cd8` on `fix/n907-forward-shadow-encoding` (off `main`)
⚠️ **The register named ONE site (`:47`); the file had TWO** — `:47` (scoring weights) and `:102` (the access-token JSON). Both encoded. ⛔ **`read_bytes()` in `_provenance` left alone and pinned by a test** — hashing must see bytes, and a blanket sweep would have corrupted the provenance stamp.
🔑 **REACHABILITY MEASURED, ⛔ not assumed: `config/scoring_weights.yaml` carries **51 non-ASCII bytes** of 5,013, and this is a CRON job** — a cron environment with `LANG` unset resolves the default to ASCII, where the first read raises and the job produces nothing that day. ⛔ **This is OPEN-1's evidence instrument and its output CANNOT BE REGENERATED**, so a missed day is a permanent hole that may never be filled *(a gap is a loss; a manufactured day is a CORRUPTION)*.
⛔ **THE RECORDER WAS NEVER RUN.** "Prove it still runs" honoured as narrowly as it can honestly be meant: the CHANGED paths are exercised directly (`_weights()`, the token read), never `main()`. **An AST test pins that the suite calls no entry point**, and `_METHOD_VERSION`/`OUT_PATH` are pinned by a must-not-change guard.
⭐ **ANTI-VACUITY, both halves:** one test asserts the YAML really contains non-ASCII (else the fix guards nothing); another reads it as ASCII and requires it to **RAISE**, then requires `_weights()` to succeed.
✅ RED-first **3F/5P → 8P** *(an earlier draft of the never-invoked test was SELF-REFERENTIAL — it scanned its own source for the names in its own assertion — and was replaced with the AST check before the RED was read)*. **GATE `PYTEST_RC=1` · 9F / 5,590P / 4S · 1269 s — `NO NEW FAILURES`; arithmetic closes exactly (5,582 + 8 = 5,590).** The longer wall-clock is overlap with another branch's gate, ⛔ not a slowdown.

## 🗂️ FIVE WORKTREES, FIVE BRANCHES, ⛔ NONE PUSHED
`trading-system` *(sizing, uncommitted funds-short + docs)* · `-alertfix` `bfd6b5f` · `-tick2` `43f73b1` · `-p2` `071169b` · `-n907` `7649cd8`. 🔴 **Rama: `git worktree remove` each when done — every commit lives in the main repo's `.git` and survives removal.**

See also [[alert-delivery-contract-phase0-09aug]] · [[alert-delivery-sweep-09aug]] · [[feedback-carry-the-countermeasure-09aug]] · [[tick4-blocked-on-sizing-deploy-09aug]]
