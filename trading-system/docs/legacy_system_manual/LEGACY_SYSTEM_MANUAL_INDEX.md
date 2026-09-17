# LEGACY TRADING SYSTEM — END-TO-END MANUAL · INDEX

> **The system is DEAD / REFERENCE ONLY** — 👤 Rama, card-relayed, dated 17-Sep-2026. This manual describes the system **as it was**. It is ⛔ not a repair plan: a defect found while writing is registered in **chapter 22**, and no fix, proposed fix or schedule appears anywhere.
> Opened 18-Sep-2026 00:1x IST. **25 chapters**; chapter 24 is the cross-reference index and covers all 25.

---

## 1. Evidence basis (every chapter header repeats its own)

| Class | What | Notes |
|---|---|---|
| 🔬 **PRIMARY — inspected** | the PC worktree `D:/Projects/wt-sr-shadow-15sep` = commit **`e7bf477`** + the uncommitted **`force_qty`** change set | byte-equivalent to the **TESTING VM** as delivered 17-Sep-2026 19:31:34–40 (`core/config_loader.py` `2030714e…` · `capital/position_sizer.py` `b2b27684…` · `main.py` `277b0702…` · the twin's `config/system_config.yaml` `12d79b2a…`). ⚠️ Three files are modified in the working tree, so line numbers hold for the files **as read**, not for `e7bf477` alone |
| 📄 **RECORD-DERIVED** | `trading-system-sbx-snapshot/_machine/` — the installed systemd units (8), the real `crontab -l` (42 active), the armed `post-receive` hook; `_preservation/` captures; `docs/audit/` (441 files); `docs/SYSTEM_MAP.md` (80 sections); the deploy ledger; git at `970aabf` for production-side code | captured from the testing VM 17-Sep-2026 20:06 IST. A record is evidence of what was **recorded**, at its own date |
| ⛔ **NOT READ** | **PRODUCTION** `161.118.187.249` and its bare repo | every production statement is **RECORD-DERIVED** or **NOT ESTABLISHED**. ⛔ No chapter implies production was inspected. The measured divergences ride as **Appendix 01-A** |

## 2. Scope, measured 18-Sep 00:0x IST

| Population | Count | Source / method |
|---|---:|---|
| files in the worktree (excl. `.git` `.venv` `__pycache__` `.pytest_cache` `node_modules`) | **1,465** | `os.walk` |
| `.py` modules · physical lines | **757** · **289,044** | `os.walk` + `splitlines` |
| non-test `.py` modules | **344** | 757 − 413 test modules |
| **runtime set** — statically import-reachable from `main` + the **38** `.py` named in `config/cron_registry.yaml` | **200** modules · **92,168** lines | AST import walk, package `__init__` included |
| outside the runtime set | **557** (tests **413** · `ops_dashboard` **93** · other **51**) | same walk |
| `config/` files · YAML · strategy YAMLs | **52** · **31** · **16** | `os.walk`; `config/strategies/` |
| configuration files the loader actually loads | **8** | `_CONFIG_FILES`, `core/config_loader.py:2536` |
| `config/cron_registry.yaml` | **27,116** B · **767** lines · **47** jobs | `wc -l`; YAML parse (corrected from 768 — an earlier count of mine added one for the trailing newline) |
| database tables | **45** main · **3** analytics · **4** shadow | `core/schema.sql`, `core/analytics_schema.sql`, and a byte-copy of `sr_shadow.db` **with its WAL** |
| tests | **451** files (`tests/unit` **363** · `tests/integration` **17**) | `os.walk` |
| sbx snapshot: committed · repo-only artifacts · VM tree · excluded-and-named | **1,418** · **13** · **1,405** · **3,916** | `git ls-files`; the manifest's own totals |

**Method limits, stated once.** Reachability is **static import reachability**, not observed execution; the three dynamic-import sites are named in chapter 02 §2.1. `exec(` and `eval(` do not occur in any of the 344 non-test modules (controls: `import ` = 3,008; an impossible token = 0).

## 3. The 25 chapters

| # | Chapter | Group | Status | Pages | Evidence date | Unresolved |
|---|---|---|---|---:|---|---|
| 01 | System overview (+ Appendix 01-A, the divergences) | 1 | ✅ **WRITTEN** | 6.4 | 18-Sep | production state; which mode each instance booted; the twin's own `accounts.csv` contents |
| 02 | Repository and file map | 1 | ✅ **WRITTEN** | 244.7 | 18-Sep | runtime truth vs import reachability; 24 config-key and 13 table tokens dropped rather than guessed |
| 03 | Startup, runtime and scheduler (+ 03-A, the schedule tables) | 1 | ✅ **WRITTEN** | 11.2 + 3.9 | 18-Sep | who installs the crontab; the SQL behind three boot calls; delivery at EOD; the pre-receive guard's existence |
| 04 | Market data and data sources | 2 | ⏸ NOT STARTED | — | — | — |
| 05 | Signals and strategies | 2 | ⏸ NOT STARTED | — | — | 15+ pages required: all 16 strategies, full condition sets |
| 06 | Filtering and trade decision | 2 | ⏸ NOT STARTED | — | — | — |
| 07 | Technical analysis and S&R | 2 | ⏸ NOT STARTED | — | — | shadow only; the capture defect is chapter 22 material |
| 08 | Entry price and R:R | 2 | ⏸ NOT STARTED | — | — | 15+ pages required; absorbs the T1–T14 evidence pass, T2/T3 first |
| 09 | Risk and capital allocation | 2 | ⏸ NOT STARTED | — | — | `force_qty` is part of the twin's basis and was never verified live |
| 10 | Order processing and management | 2 | ⏸ NOT STARTED | — | — | — |
| 11 | Position management | 2 | ⏸ NOT STARTED | — | — | — |
| 12 | Exits | 2 | ⏸ NOT STARTED | — | — | — |
| 13 | Reconciliation and broker state | 3 | ⏸ NOT STARTED | — | — | — |
| 14 | Alerts, notifications, monitoring | 3 | ⏸ NOT STARTED | — | — | forwarding must be proven, not inferred |
| 15 | Reports, audit, evidence, logging | 3 | ⏸ NOT STARTED | — | — | — |
| 16 | Database and storage | 3 | ⏸ NOT STARTED | — | — | read only from byte-copies, main **+ WAL** |
| 17 | Configuration | 3 | ⏸ NOT STARTED | — | — | 15+ pages required: key by key across 31 YAMLs; production values record-derived |
| 18 | Security, credentials, deployment | 3 | ⏸ NOT STARTED | — | — | ⛔ WHERE and WHAT CLASS only — ⛔ never a value |
| 19 | Testing and validation | 3 | ⏸ NOT STARTED | — | — | ⛔ no coverage claim from a test count |
| 20 | Failure recovery and runbook | 3 | ⏸ NOT STARTED | — | — | — |
| 21 | End-to-end walkthrough | 4 | ⏸ NOT STARTED | — | — | 15+ pages required; **written last on purpose** — every contradiction it exposes is a finding |
| 22 | Known issues and evidence register | 4 | ⏸ NOT STARTED | — | — | the only home for every defect; its raw input is already parked (§5) |
| 23 | Legacy lessons | 4 | ⏸ NOT STARTED | — | — | ⛔ not a V2 design |
| 24 | Index / cross-reference | 4 | ⏸ NOT STARTED | — | — | covers all 25 chapters |
| 25 | Ops dashboard and GUI | 4 | ⏸ NOT STARTED | — | — | 93 modules · 40,722 lines · its own installed unit, which exists in no repository file |

**Written so far: 3 chapters + 2 appendices ≈ 270 pages.** Writing order (card §4, ⛔ not chapter-number order): **G1** 01·02·03 → **G2** 04–12 → **G3** 13–20 → **G4** 21·22·23·24·25.

## 4. Evidence format every chapter follows

1. **Header:** subject · evidence basis (tree, commit, machine) · evidence date · what it deliberately excludes.
2. **The trace,** per component: `SOURCE → INPUT → PROCESS → VALIDATION → OUTPUT → STORAGE → NEXT COMPONENT`.
3. **Labels, never blended:** **FACT** · **UNKNOWN / NOT ESTABLISHED** · **INTERPRETATION** · **HISTORICAL** · **KNOWN DEFECT**.
4. **Formulas as the actual expression from the code**, with `file:line` — never a prose description of what it probably does. Code lines are distinguished from log or output lines.
5. **Paper vs live** wherever behaviour differs — never one described and the other assumed.
6. **Every number carries its population, window and source.** Every zero carries a positive control run with the same flags and locale.
7. **A closing "what this chapter could not establish".**
8. **Cross-references** to the chapter that owns each neighbouring fact.

⭐ **On the KNOWN DEFECT label.** The register of defects is chapter 22 and nowhere else, and no fix is proposed anywhere. Where a defect is load-bearing for understanding a sequence, the chapter states the fact under the **KNOWN DEFECT** label and says it is registered in 22; it argues no remedy. Everything else is parked (§5) for 22 to triage.

## 5. Working data (⛔ not chapters)

`_working/` beside this index, so the evidence outlives the session that produced it:

| File | What it is |
|---|---|
| `_parked_for_ch22.md` | **743 parked observations** with file, line and the text of that line: 4 verified by the author, 682 from the per-module passes, 57 from the sequence traces. ⛔ None is a confirmed defect until chapter 22 examines it |
| `graph.json` | the deterministic module dataset: every module's path, lines, importers, imports, classes, functions, config-key and table literals, log-call counts, and the runtime-set flag |
| `entries_verified.json` | the 200 per-module research entries after every anchor was resolved against the file |
| `boot_verified.json` | the 6 sequence traces, 480 steps, each with its verdict |
| `resolve_stats.json`, `resolve_drops.json` | the anchoring accounting and every dropped claim with its reason |

## 6. Verification accounting so far

| Anchor class | Claims | Anchored | Dropped | Agent's own line exact |
|---|---:|---:|---:|---:|
| Symbols (class / function / method) | 1,689 | 1,687 | 2 | 1,663 (98%) |
| Config keys | 691 | 667 | 24 | 613 (89%) |
| Database tables | 308 | 295 | 13 | 247 (80%) |
| Sequence steps (quoted line vs the file) | 480 | 480 | 0 | 480 (**100%**) |

**Corrections the author made against the research passes**, each re-derived from the code: the cron registry is **767** lines, not 768 (my own earlier count added one); the startup aggregator runs **15** checks, not 16 (17 exist in the module, two are not called); the `kiteconnect`-exclusivity claim in `broker/zerodha_adapter.py`'s own docstring is false for the tree (**17** import sites in **15** files) and is recorded as such in chapter 02 and parked for 22.

## 7. Unresolved / awaiting

| # | Item | State |
|---|---|---|
| U1 | the governing spec `INSTRUCTION_TO_WEB_CLAUDE_DEAD_SYSTEM_COMPLETE_BOOKLET_MANUALS.txt` never reached the session and is not on the PC | ⭐ **no longer blocking** — 👤 Rama's instruction is to write against the card; a reconciliation pass follows if the spec arrives |
| U2 | production access | ⏸ **answered:** no yes has arrived, so 02, 17 and 18 are testing-VM-only with production RECORD-DERIVED / NOT ESTABLISHED. ⛔ Not to be asked again |
| U3 | `ops_dashboard/` | ⭐ **answered:** in scope, as its own **chapter 25** |
| U4 | the VM file-count discrepancy | ✅ **resolved:** 1,405 tree files + 3,916 excluded = **5,321**; the earlier 3,939 predates 23 CSVs moving into the repo (3,939 − 23 = 3,916). ⚠️ A **one-file** residue against a live `find` of 5,322 is unexplained and recorded in Appendix 01-A |
| U5 | the CRLF-only difference on 23 files | ⚠️ cause still **UNRESOLVED**, carried from 17-Sep |

## 8. Push and record discipline

- Chapters live here and are pushed **per chapter or small batch** to `trading-system-records` — ⛔ never weeks unpushed.
- ⚠️ On the **first push**, that repo's `SNAPSHOT_MANIFEST.md` must be amended: it excludes `docs/` outside `docs/audit/`.
- `PATHS.md` carries pointers; `docs/SYSTEM_MAP.md` carries a **POINTER ONLY**.
- ⛔ No secret values in any chapter, at any time. These files go to GitHub.

## 9. Execution metadata

| Pass | Model | Effort | Notes |
|---|---|---|---|
| Index opened, 18-Sep 00:1x IST | `claude-opus-5[1m]` | `ultracode` | 👤 Rama's setting governs and supersedes the cards' "Low" |
| Group 1 written, 18-Sep 00:3x–02:xx IST | `claude-opus-5[1m]` | `ultracode` | 36 research agents (4.58 M agent tokens, 0 errors) for evidence; **every file written and every citation re-verified by the author**, per the 11-Sep lesson that a subagent must never be handed final assembly |
