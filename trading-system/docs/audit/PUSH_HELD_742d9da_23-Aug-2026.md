# PUSH — SCOPE SETTLED, **HELD ON OPS ②** · 23-Aug-2026 (Sun), evening

**Governed by** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
🏷️ **⛔ NOT PUSHED · ⛔ NOT DEPLOYED · `origin/main` = `4568385` (as last measured).**

---

## THE TWO GATES

| gate | status |
|---|---|
| **§2 — scope** | ✅ **SETTLED. 👤 Rama, 23-Aug: `742d9da`, 8 commits.** ⛔ NOT `a4a5cef` — NI-5 stays the third unit |
| **§3 — OPS ②** | 🔴 **OPEN. 👤 Rama: *"Not yet — I'll run it first."*** ⛔ **THE PUSH IS HELD UNTIL HE CONFIRMS IT LANDED** |

⇒ ⛔ **No push tonight until OPS ② is applied and its three evidences are collected.**

## WHAT `742d9da` IS — 🔬 measured, ⛔ not carried from any card

`4568385 ⊂ d00e574 ⊂ 742d9da ⊂ a4a5cef`, all clean fast-forwards. **8 commits:**

```
d00e574  fix(sizing): item 1 -- delivery risk config is explicit; the silent fallback is gone
940a572  test(config): job 1 -- the delivery-setting sweep found nothing to fill, pinned
4928941  fix(sizing): NI-1 -- the SL-direction guard raised KeyError instead of warning
c146eb7  fix(auditor): NI-2 -- C2 compared the ceilings without the multiplier between them
5a7dbf6  docs(risk):  NI-3 -- the delivery count caps are LIVE; the "inert" clause was stale
6ad328e  fix(config): NI-4 -- the last two delivery keys stop defaulting silently
4c495d0  docs(snapshot): NI-6 -- the first post-deploy config_hash change is CORRECT
742d9da  test(rename): NI-7 -- the file stopped testing a scaffold on 22-Aug; the name did not
```

⚠️ **CORRECTION TO THE CARD'S COMPOSITION:** it listed *"F1 + NI-1/2/3/4/6/**7/8** + the
job-1 test"*. 🔬 **There is no NI-8 commit** — `NI-8` is *"the memory line budget · DONE"*,
a memory-file task outside the repo. The count is still 8; the composition was wrong.
⛔ `NI-5` is absent by design (third unit).

## STATIC PRE-FLIGHT — done now because it cannot change; ⛔ NOT a substitute for V-1…V-6

| check | result |
|---|---|
| **V-4** forbidden ancestry | ✅ `65b7196` **NOT** in ancestry · `3dff752` (the register, on `main`) **NOT** in ancestry · `c39e799` (F6) **NOT** in ancestry |
| **V-4** positive control | ✅ **fires** — `d00e574` *is* correctly detected inside `742d9da`, so the test is not vacuous |
| **V-3** F6 **CONTENT**, ⛔ not ancestry (the `N9-07` lesson) | ✅ `orders/cnc_gtt_monitor.py` at `742d9da` is **BYTE-IDENTICAL** to deployed `4568385` ⇒ the push carries **ZERO** F6 substance |
| **V-3** positive control | ✅ **fires** — `c39e799`'s own version differs from deployed by **326** lines, so the comparison can see F6 when it is there |

⭐ Both zeros are load-bearing **only** because both controls fired.

## 🔴 STILL TO RUN IMMEDIATELY BEFORE THE PUSH — ⛔ nothing above substitutes

⚠️ **`origin/main` must be resolved AT GATE TIME.** A SHA measured hours earlier passes and
tells you nothing.

- **V-1** `origin/main` **two independent ways** — VM bare-repo ref **and** `git ls-remote`.
  ⛔ The cached local `refs/remotes/origin/main` is **NOT** a second measure. Must equal
  `45683859a0a05f466189ac5bc98f9a9f089f98d3`.
- **V-2** `git push --dry-run origin <full-40>:refs/heads/main` → must show `..`
  (fast-forward), ⛔ no `+`, ⛔ no forced update.
- **V-5** 🔬 **SERVICE BEFORE-IMAGE** — `trading-system`, `alert-watcher`, `gui-dashboard`,
  `token-watcher`: `MainPID` + `NRestarts` + timestamp. ⚠️ Capture **after** OPS ② and
  **before** the push, or the *"did the hook restart anything"* check is unscoreable.
- **V-6** 🔬 the **M-5 pre-deploy search**, on the VM, with the **poisoned-gate-corrected
  signature**:
  ```
  signals.status='PLACEMENT_FAILED' AND reason LIKE '%unhandled%msg%'
  logs: "Unhandled exception in pipeline" + "Attempt to overwrite 'msg' in LogRecord"
  ```
  🔴 ⛔ **DO NOT search `sl_direction_warning` — it returns ZERO BY CONSTRUCTION**
  (pre-NI-1 that call *raised* instead of logging). State the width. ⚠️ Does not block;
  ⭐ after this deploy the artifact **flips form permanently**.

**THE PUSH:** explicit **full 40-char** refspec only —
`git push origin 742d9dab5234682d40d2c538fce1b777a42b30e1:refs/heads/main`
⛔ **NEVER** `git push origin main` · ⛔ `--force` · ⛔ amend · ⛔ push the register ·
⛔ push `a4a5cef`.

## AFTER — FILE/CONFIG LEVEL ONLY

`origin/main` == pushed SHA, two ways · register + `65b7196` still absent · PC==VM per
changed file **and state whether that check was NON-VACUOUS** (they must have differed
before) · deployed-tree drift via the **corrected** `GIT_INDEX_FILE` recipe **with
`update-index --refresh`** (⛔ the uncorrected form reports 1,309 phantom files) · crontab
md5 vs `b8276da7` / 46 job lines (⚠️ a seventh *"AUTO-INSTALLED from canonical"* with
unchanged content ⇒ ⭐ **record, ⛔ never repair**) · the four services vs V-5 ·
⭐ re-confirm `RestartPreventExitStatus=3 4 5` still in force.

⛔ **DO NOT start the service · no `--resume` · no SOFT_KILL clearing · no runtime
verification.**
🏷️ **CEILING: `DEPLOYED`. ⛔ NEVER `VERIFIED LIVE`.**
⭐ **Monday 24-Aug 08:15 is the first execution. F1 is fail-closed on the boot path —
👤 Rama should be awake for it.** ⛔ **REVERT if a VALID config is rejected.**

## ⚠️ WHAT GOES IN WITH IT — stated so it is not a surprise Monday

- **NI-1 is money-path by REACH** — `LATENT`, ⛔ not live (an inverted LONG SL is
  structurally underivable), ⛔ does not block. But if one ever reaches `calculate()`,
  nothing between PS10 and `fm.reserve` stops it.
- **F1 + NI-4 make exit 5 routinely reachable** — which is exactly why OPS ② goes first.
- **8 commits in one deployment ⇒ ⛔ no controlled attribution.** 👤 Chosen knowingly.
