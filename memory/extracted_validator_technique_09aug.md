---
name: extracted-validator-technique-09aug
description: "TECHNIQUE — extract a stdlib-only validator/auditor from a git ref and RUN it against two configs. Cheap, read-only, no .env/DB/network, and it refutes claims that reading the code cannot."
metadata: 
  node_type: memory
  type: reference
  originSessionId: d9595f8a-8cb4-47fd-9b87-a97e7c891339
  modified: 2026-08-09T05:24:17.908Z
---

# 🔬 **EXTRACT THE VALIDATOR AND RUN IT — ⛔ READING THE CODE WOULD NOT HAVE CAUGHT IT**

**09-Aug-2026.** The claim *"this warning fires every morning"* was refuted in minutes by **running** the real check, not by reading it. ⭐ Rama asked for the technique to be pinned because it is **reusable and cheap**.

## THE RECIPE

1. **Check the module's imports first.** `sed -n '1,60p' <file> | grep '^import\|^from'` — if it is **stdlib-only at module level**, it loads standalone: ⛔ **no `.env`, no DB, no network, no `load_dotenv()`** *(the trap in [[feedback-no-fixed-test-baseline]])*. `core/config_auditor.py` is: `enum`, `dataclasses`, `typing`.
2. **Take BOTH sides from the REFS, ⛔ not the worktree:** `git show origin/main:core/config_auditor.py > deployed.py` · `cp core/config_auditor.py built.py`, and the same for the config. ⭐ **The worktree and the deployed ref are DIFFERENT OBJECTS** — the same discipline as GO/NO-GO line 9b.
3. **Load by path** (`importlib.util.spec_from_file_location`) so both versions coexist in one process under different names.
4. **Feed real config through `yaml.safe_load` + `SimpleNamespace`** — ⛔ never hand-typed values; transcription is its own error class.
5. **Run the 2×2** (old code × old config · new code × new config, and the crosses if the question needs them) and **print the findings verbatim**.
6. ⭐ **Anti-vacuity, ⛔ not optional:** a green is evidence ONLY if it could have been red. Here run A returned `[PASS] C_ok` and run B returned two `WARN`s **on the same harness** — that is what makes A's silence mean something. [[feedback-verify-rc-not-output]]

## WHY IT BEATS READING

- ⭐ It evaluates **guards you would skim** — C5b's whole arm is gated on `d_rpt is not None`, and the deployed value is `null`, so the check does not merely pass, **it does not run at all.**
- ⭐ It applies the **real config**, so a threshold nobody restated correctly (`0.03 × 2` vs `0.03 × 0.70 × 2`) cannot hide.
- ⭐ It answers *"what does the VM do TODAY"* separately from *"what will it do after the deploy"* — the exact distinction that drifted in [[feedback-tense-drift-09aug]].
- ⛔ **Scope limit:** this proves what the CODE computes from a CONFIG. It is ⛔ NOT a live-system observation and must never be labelled `VERIFIED LIVE` [[feedback-status-label-rule-27jul]].

**Applies to:** any pure-function check — config auditors, pydantic validators, severity maps, threshold/gate helpers. ⛔ **Not** to anything touching `state_store`, a broker adapter, or a DB path *(and ⛔ never `scripts/*.py --db <copy>` — it writes to the LIVE DB before parsing `--db`)*.

See also [[c5-c5b-risk-pct-card03-09aug]] · [[pc-test-env-hygiene]] · [[tautological-check-class-05aug]]
