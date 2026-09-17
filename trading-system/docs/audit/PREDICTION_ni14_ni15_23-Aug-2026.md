# FROZEN PREDICTION — NI-14 + NI-15 L1 · 23-Aug-2026, written BEFORE the build

**Base:** 🔬 `origin/main` = `2f67bb849633eb7844dc46570d2b31f8a8604e97`.
Governed by `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
**Authorisation:** 👤 Rama routed the decision to ChatGPT (*"Answer web claude, so web claude will
finish remainin 2/3 N** fix"*) → ruled **YES NI-14 · YES NI-15 L1 · NO NI-16**.
🏷️ **Delegated answer on a routed question** — ⛔ not ChatGPT acting unilaterally (`WC-PATTERN #8`),
⛔ not Rama's own words. ⚠️ Scope = presentation semantics + an already-approved watcher fix;
⛔ it does **not** extend to capital, risk, sizing, orders or MIS ×3.5.

---

## N-1 · 🔬 THE ACTUAL SEVERITY VOCABULARY — MEASURED, ⛔ NOT ASSUMED

⚠️ **The card's suspicion was right: there are TWO vocabularies.**

| layer | vocabulary | source |
|---|---|---|
| **source-native** (security_monitor) | `CRITICAL · WARNING · INFO` | `security_monitor.py` |
| **tower** | `CRITICAL > HIGH > MEDIUM > LOW > INFO` | `severity.py:TOWER_SCALE`, `RANK` |

```python
TOWER_SCALE = ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO")
RANK = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "INFO": 0}
SECURITY_MAP = {"CRITICAL": "CRITICAL", "WARNING": "MEDIUM", "INFO": "INFO"}
CONFIG_MAP   = {"BLOCK": "CRITICAL", "WARN": "HIGH", "INFO": "INFO", "PASS": "INFO"}
```

⇒ 🔴 **A native security `WARNING` never appears as the string `"WARNING"` inside the aggregator —
it arrives as tower `MEDIUM`.** ⛔ Any implementation keying on the literal `"WARNING"` would be
dead code.

### ⇒ THE RULING, MAPPED ONTO THE REAL VOCABULARY

| 👤 ruling | 🔬 implementation |
|---|---|
| CRITICAL present → RED | any finding with tower severity `CRITICAL` → `"critical"` |
| WARNING present → AMBER | any finding with `RANK[sev] > RANK["INFO"]` → `"warn"` (covers `HIGH`, `MEDIUM`, **and `LOW`**) |
| INFO only → GREEN | all findings `INFO` → `"ok"` |
| zero findings → GREEN | → `"ok"` |

⚠️ **`LOW` is a judgement call and is stated, ⛔ not hidden:** `LOW` is **not** `INFO`, and the
security adapter emits `LOW` for *"last_run.json unreadable"* — a real condition. ⇒ **`LOW` → AMBER.**
⭐ Driven off `RANK`, ⛔ not a hardcoded list, so it follows the one reviewable vocabulary.

---

## N-2 · 🔬 BOTH PINNED FIELDS — LOCATED, AND A THIRD SITE FOUND

| # | site | current code | reachable-`ok`? |
|---|---|---|---|
| **1a** | `aggregator.py:88-89` **security** | `"critical" if any CRITICAL else "warn" if findings else "ok"` | 🔴 **no** — INFO-only pins `warn` |
| **1b** | `aggregator.py:137-138` **cron** | *identical expression* | ⚠️ same shape |
| **2** | `aggregator.py:259` | `"status": "OK_WITH_FINDINGS" if detected else "OK"` | 🔴 **no** — `detected` includes INFO |

🔬 **Site 1b is behaviour-identical under the new rule, and that is MEASURED, ⛔ not assumed:** the
cron adapter emits only `HIGH` and `MEDIUM` findings (grep of its `Finding(` severities: `HIGH` ×2,
`MEDIUM` ×1, **zero INFO**) ⇒ under both old and new derivations it yields `warn`.
⇒ ⭐ Fixing it via the shared helper is **correct-by-construction with zero behaviour change**,
⛔ not scope creep.

🔬 Site 2's fix is natural because `counts` (line ~236) is already computed over
`("CRITICAL","HIGH","MEDIUM","LOW")` — **INFO is already excluded** ⇒ `OK_WITH_FINDINGS` iff
`sum(counts.values()) > 0`.

---

## THE PREDICTIONS, WITH FALSIFIERS

### P-1 · NI-14 · the live security panel flips `warn` → `ok`
🔬 Today's live `last_run.json`: `clean:false, findings_count:1, max_severity:"INFO"` ⇒ one INFO
finding ⇒ **old = `warn`, new = `ok`.**
**FALSIFIER:** the adapter still returns `warn` on an INFO-only findings list ⇒ the fix missed.

### P-2 · ⛔ THE FINDING INVENTORY IS UNCHANGED (N-3)
INFO findings still **counted**, still in `detected`, still entering `open_severities`,
`health.score_and_band` and the push path. ⭐ **Only the STATUS derivation changes.**
**FALSIFIER:** `findings_total`, `counts`, or `open_severities` differ for the same input ⇒ STOP.
⚠️ An INFO finding becoming invisible would be **worse than the defect being fixed**.

### P-3 · cron status is bit-identical
**FALSIFIER:** any cron test changes result ⇒ the helper is wrong.

### P-4 · NI-15 L1 · the baseline survives a `None`
🔬 Defect: `:732 hashes[path] = cur` runs **before** `:733 if cur is None: continue`.
After the fix: `HASH_A → gone → HASH_B` **alerts** (prev survives as `HASH_A`).
**FALSIFIER:** the recreate-with-different-content case stays silent ⇒ the fix is cosmetic.

### P-5 · the identical-content case — 🏷️ CONTRACT STATED IN ADVANCE
`HASH_A → gone → HASH_A` ⇒ **NO alert.** ⭐ The check is a **content**-integrity check; content is
unchanged. ⛔ The vanish itself is not alerted — that would be a NEW alert type, ⛔ outside L1.
⭐ The `unreadable/missing` state IS recorded, per the invariant.
**FALSIFIER:** if the contract is later judged to require an alert here, this is the line to revisit.

### P-6 · ⛔ NI-15 L1 DOES **NOT** CLOSE THE SUDOERS GAP
🔬 `/etc/sudoers` is `440 root:root`, watcher runs `User=ubuntu` ⇒ still unreadable, still skipped.
⭐ **L1 makes the skip NON-DESTRUCTIVE; ⛔ it does not make the file visible.** That is L2, ⛔ not
authorised.
**FALSIFIER:** any claim that NI-15 closes sudoers ⇒ false.

### P-7 · the gate
Base `2f67bb8` must reproduce **`7F / 5,797P / 4S`** — ⭐ the NEW baseline, ⛔ not the old 5,751.
Head = same 7 failures, id-level identical, plus the new tests.
**FALSIFIER:** base ≠ 7F/5,797P/4S ⇒ the harness is wrong, ⛔ not the code.

### P-8 · ⭐ EVERY NEW TEST MUST FAIL PRE-FIX
⛔ A test that passes on both trees proves nothing (`V5`, the tautological-check class).
**FALSIFIER:** any new test green on `2f67bb8` ⇒ it is not a test, ⛔ rewrite it.

---

## ⛔ OUT OF SCOPE, EXPLICITLY

⛔ NI-16 (blocked on F2 — the clamp limits a trade to ONE ALLOCATION and the deployed system
computes none) · ⛔ `root_probe_spike_threshold` (👤 400 stays) · ⛔ F13 legs L2–L4 · ⛔ D-1b as a
wider redesign · ⛔ D-3 · ⛔ MIS ×3.5 · ⛔ any change to the finding inventory.
