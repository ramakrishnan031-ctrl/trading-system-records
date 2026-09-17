# FILE 19 — BUILD RECORD · 27-Aug-2026 EVENING

🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S · 🏷️ VACUOUS / NOT EXERCISED.

🔬 **Step 0, measured:** `origin/main` = **`bc9a9f5`** = **VM bare HEAD** ·
service **`inactive`** (self-exited 17:35:04, `Result=success`) · market closed.
⛔ **ROOT (`feat/delivery-config-split` @ `6d24a83`) was never touched** — all work
in isolated worktrees off `bc9a9f5`, with the gitignored `config/instruments.csv`
seeded into both (else 26 phantom failures).

---

## 1 — TODAY'S RECORD · A–G, EXACT WORDING

| # | label | record |
|---|---|---|
| **A** | 🔴 **PROCESS MISS — mine** | *"FILE 18's time-critical C-1 notice was not delivered before its deadline."* Issued 12:15 for 15:00/15:10/15:15/15:25/17:25–17:45; received **18:20**. ⛔ Not softened. **Structural fix, ⛔ not "be faster":** a file whose value expires at a clock time must carry its **DEADLINE IN ITS FILENAME OR FIRST LINE**, and a time-critical notice must reach 👤 Rama **in the chat reply**, ⛔ never only inside a `.txt` that depends on transport |
| **B** | **SYSTEM OUTCOME** | *"The candidate independently exited via GTT legs; no carry existed at close."* ⚠️ ⛔ **NOTICE MISSED ≠ CARRY LOST BY THE MISS** — JINDALSAW **12:46:55**, OAL **14:33:41**, both before the ~15:00 deadline ⇒ nothing left to decide at 15:00 |
| **C** | **EOD** | *"27-Aug again exercised only the flat/trivial self-exit arm."* `17:35:00.002 eod_self_exit … flat (0 active positions)` · `ExecMainExitTimestamp 17:35:04` · `Result=success` · `NRestarts=0` · SHUTDOWN **3798**. ✅ **FLAT EOD SELF-EXIT = OBSERVED.** 🔴 ⛔ **CNC-ONLY DISCRIMINATING CASE = NOT EXERCISED.** ⚠️ **3 × flat ≠ 1 × discriminating** |
| **D** | **CARRY TESTS** | *"All carry-dependent tests remain NOT EXERCISED / OWED."* OWED-2 · CHECK 1 · CHECK 2a · **CHECK 2b = NOT COMPUTABLE** (⭐ correctly not manufactured — a flat-book reading removes the carried-capital component it measures) · four-reading series · three-cause discriminator · G3's owed settled-CNC `used` · **cause ④ = INFERENCE** · **revert trigger `carry > 0` = still 0 of 9,289** |
| **E** | **T+1** | *"F6 T+1 remains NOT EXERCISED."* ⛔ Today's intraday GTT exits are ⛔ not T+1 evidence. ⛔ The F6 fix did **not** fail — there was no eligible carry to run it against |
| **F** | **STARTUP** | *"COLD→CRASH classification sequence observed and parked; no scope change tonight."* → §2 P-1 |
| **G** | **U3** | *"722-row persisted leverage baseline captured; executable post-fix neutrality proof still required."* MIS **503 @ 5.0** · CNC **84 @ 1.0**, `min == max` · 135 NULL-product EXCLUDED. 🔴 ⛔ A historical query over unchanged rows is **not** a post-fix proof ⇒ ⭐ **an executable oracle was built instead (§4)** |

⭐ **EVIDENCE WORDING HELD:** *"System records show all CNC positions exited via
`GTT_EXIT`."* ⛔ Not converted into a broker-confirmed claim. ⛔ Broker audit data
was **not** independently checked.
⭐ **GOVERNING PRINCIPLE RECORDED:** ⛔ *do not turn absence of the qualifying
condition into evidence about that condition's behaviour.* No carry ⇒ no carry
proof — ⛔ not a pass, ⛔ not a fail, ⛔ not a simulation.

---

## 2 — TWO PARKED FINDINGS

**P-1 · COLD IS UNREACHABLE — 🏷️ OBSERVED BEHAVIOUR / PARKED ARCHITECTURAL HAZARD.**
🔬 `08:15:16.540 startup_scenario=COLD` → `.555 CRASH` →
`08:15:24.421 run_all_startup_checks: OK scenario=CRASH`. Same pair 26-Aug.
⇒ 🔴 **If CRASH always wins at 08:15, the COLD arm has never run in production** —
an **F11-family unreachable path**, ⛔ not a labelling oddity. ⚠️ Corollary: CRASH
normally does MORE recovery work, so **the system runs crash-recovery every
morning as its normal path** — probably harmless if idempotent, ⛔ never
questioned. ⛔ **No scenario logic changed tonight.**

**P-2 · THE CLEANEST CNC SAMPLE YET — 🏷️ RECORDED, ⛔ NOT ANALYSED.**
👤 Rama confirms nothing manual closed. 🔬 **Three CNC round trips, all
system-entered and system-exited:** RAMRAT (→10:45:29), JINDALSAW
(10:01:23→12:46:55), OAL (10:14:21→14:33:41) — ⛔ zero operator involvement,
unlike 26-Aug's 20MICRONS contamination. ⭐ **The first uncontaminated CNC
lifecycle sample.** ⛔ **DEFECT B stays PARKED — NON-CORE**; ⛔ no exit-price
analysis opened. ⭐ Only CORE use is **F4 (CNC fill rate)** — 🔬 **3 CNC entries
filled today** — ⚠️ and F4 is blocked on observability that is ⛔ not built.
⭐ Count recorded. ⛔ Nothing analysed.

---

## 3 — UNIT 1 · F6-LEG · ✅ BUILT · commit `b5d6c8b`

### The 8-file classification (done FIRST, as required)

| file | in `c39e799` | class | taken? |
|---|---|---|---|
| `orders/cnc_gtt_monitor.py` | +310/−16 | 🔴 **REQUIRED — the F6-leg hunk only** | ✅ the one line + rationale |
| `core/state_store.py` | +114/−4 | SUPPORTING **of the wider F6 redesign** — 5 new GTT-state methods (`get_reconcilable_gtt_states`, `mark_gtt_state_triggered`, `count_observed_gtt_exits`, `get_reservation_id_for_trade`, `clean_gtt_states_for_trade`) | ⛔ **NOT taken** |
| `capital/fund_manager.py` | +44/−0 | SUPPORTING — `_resolve_release_reservation_id` (F6 **D-3**) | ⛔ **NOT taken** |
| `orders/order_reconciler.py` | +8/−1 | COUPLED to TRIGGERED-durability (`get_active_gtt_states` → `get_reconcilable_gtt_states`); its own comment: *"⛔ The two MUST move together"* | ⛔ **NOT taken** |
| `tests/unit/test_f6_delivery_exit_predicate.py` | +820 | acceptance suite **for the redesign** | ⛔ not taken; a **new** targeted suite written instead |
| `tests/unit/test_fund_manager.py` | +143 | supporting the D-3 change | ⛔ not taken |
| `tests/unit/test_state_store.py` | +64 | supporting the 5 methods | ⛔ not taken |
| `docs/audit/f6_build_08aug2026.md` | +361 | **COLLATERAL** — a dated record | ⛔ not taken |

🔴 **WHY ONLY ONE HUNK — measured, ⛔ not preference.** `_finalize_gtt_exit`
**already exists on deployed main** (`cnc_gtt_monitor.py:528`) and is already
reachable from three sites (`:490`, `:510`, `:512`). The `abs()` at `:466` is the
**only** thing making `held == 0` unreachable on T+1. ⇒ The fix **restores
reachability of an existing working path**; it needs none of the new machinery.
⚠️ Taking any of the three untraced files wholesale would have **deleted main's
work** — `vsMAIN` measured: `fund_manager.py` **+56/−156**, `state_store.py`
**+121/−106**, `order_reconciler.py` **+21/−157**.
⭐ The rest of `c39e799` is the **separate F6 item**, ⛔ not F6-leg.

### The change
```python
-  held[sym] = held.get(sym, 0) + abs(int(qty))
+  held[sym] = held.get(sym, 0) + max(0, int(qty))
```
🔴 **THE TRAP, pinned by test:** deleting `abs()` is **also wrong** — the signed
sum gives `−1`, likewise `!= 0`; and it additionally **clamps a genuine remainder
away** (holdings 1 + position −1 = 0), routing a real partial fill to the
clean-exit path. Only `max(0, …)` is correct.

### Red-capability — 🔬 MUTATION VERIFIED
| mutation | result |
|---|---|
| restore `abs(int(qty))` | 🔴 **5 of 8 fail** |
| delete `abs()` → raw signed sum | 🔴 **5 of 8 fail** |
| correct `max(0, int(qty))` | ✅ **8 pass** |

⚠️ 🏷️ **NOT EXERCISED: the T+1 arm.** ⛔ A unit test is not a live T+1 exercise.

---

## 4 — UNIT 3 · 🔴 SPLIT ON THE STANDING STOP CONDITION

🔬 **Blast radius measured BEFORE writing code — and it triggered B-1's stop rule:**

| group | files | sites |
|---|---|---|
| **A** — real `FundManager(` with **no** `leverage_map` (U3-c) | **8** | 17 |
| **B** — incomplete / invalid-intent maps (U3-e) | **6** | ~9 |
| **TOTAL** | 🔴 **14** | ~26 |

⇒ Predicted **≥8**; actual **14** — a **75% overrun** = *"substantially beyond"*.
⇒ ⭐ **STOPPED AND REASSESSED, per instruction.**

🔬 **The separation that made a safe subset possible:** `LeverageMapConfig` is
referenced **only** in `core/config_loader.py` — nowhere else, not even tests —
and only **one** test file builds its own `capital:` yaml block. ⇒ The validation
half is separable at a cost of **1 existing test file**.

> ✅ **SHIPPED — UNIT 3a (validation):** the entire capital protection.
> ⏸️ **DEFERRED — UNIT 3b (source hardening):** U3-c + U3-e. Both guard **latent,
> currently-unreachable** paths — `main.py` always supplies the map, and only MIS
> and CNC occur in production. 🏷️ **Recorded as owed, ⛔ not silently dropped.**

### UNIT 3a · ✅ BUILT · commit `52ccb4f`
- `leverage_safety` block (`min_allowed 1.0`, `max_allowed 10.0`) — **REQUIRED,
  self-validating, no default**
- `ABSOLUTE_MAX_LEVERAGE = 20.0` (code) — config ⛔ cannot widen its own bound
- All four intents: present · finite · bounded ⇒ **CRITICAL + load failure**
- **DELIVERY pinned to exactly `1.0`**
- NaN / ±Inf rejected **explicitly** — 🔬 a bounds check alone accepts NaN
  (`nan < 1.0` and `nan > 10.0` are both False; pinned by `test_14b`)
- 🔬 Shipped values **UNCHANGED**: `5.0 / 6.0 / 1.0 / 5.0`, safety `1.0 … 10.0`

### 🔴 THE EXECUTABLE NEUTRALITY ORACLE (FILE 19 condition 4)
⛔ **Not** a re-query of unchanged rows. ⭐ The suite **executes the real
`required_margin()`** with the **real config-loaded map** against **12 real
production triples** `(qty, entry_target_price, margin_reserved)` and requires
equality. Non-circular: `margin_reserved` was persisted independently at reserve
time and is not derived from the other two.
🔬 Corroborated across the whole persisted population: implied leverage is
**exactly 5.0 on 503 MIS rows** and **exactly 1.0 on 84 CNC rows**, `min == max`.

### Red-capability — 🔬 MUTATION VERIFIED
| neutered protection | failures |
|---|---|
| DELIVERY pin | 🔴 1 |
| explicit finite check | 🔴 4 |
| map-vs-safety bounds | 🔴 5 |
| governance self-validation | 🔴 2 |
| **all restored** | ✅ **40 pass** |

---

## 5 — UNIT 2 · F11 · ⛔ **UNTOUCHED** (a valid outcome, and the reason is measured)

🔬 Reader-surface scan before any edit:

| key | production `.py` refs | yaml files | config_loader | schema.sql |
|---|---|---|---|---|
| `order_protocol` | 🔴 **100** | 19 | 0 | **3** |
| `sl_atr_multiplier` | 2 | 🔴 **17** | 0 | 0 |
| `delivery_max_position_value` | 10 | 1 | 2 | 0 |
| `dynamic_by_winrate` | 3 | 1 | 1 | 0 |

⇒ A bounded 7-step no-live-reader proof (definition → validation → loading →
runtime read → indirect access → tests/docs → removal) **does not complete in this
window** for `order_protocol` (100 references, and it is also a live `trades`
column) or `sl_atr_multiplier` (17 strategy yamls).
⇒ ⛔ **Nothing removed. Removing a key on partial evidence is forbidden.**
⭐ This is *"the proof did not complete"*, ⛔ **not** *"I ran out of time"*.

---

## 6 — WHAT WAS ⛔ NOT MEASURED
1. ⛔ **No live T+1.** UNIT 1's T+1 arm has no production evidence and cannot get
   any without a real carry.
2. ⛔ **Broker audit data was not checked** — the GTT_EXIT claim rests on system
   records only.
3. ⛔ **UNIT 3b is unbuilt and untested** — the latent duplicate and the silent
   `.get(intent, 1.0)` fallback both remain exactly as they are on `bc9a9f5`.
4. ⛔ **`COVER_ORDER` / `BRACKET_ORDER` remain NOT EXERCISED** — zero production
   rows; their values are validated but never applied.
5. ⛔ **The 135 NULL-product rows** are excluded from every per-intent figure —
   the standing `trades.product` schema hazard.
6. ⛔ **P-1 (COLD unreachable) was not investigated** and no scenario logic was
   touched.
