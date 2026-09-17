# TWO JOBS — JOB 1 (fill every empty delivery setting) · JOB 2 (NI-1 … NI-8)

**Build report.** 22-Aug-2026 (Saturday) evening, IST.
**Card:** VS CODE CLAUDE, "TWO JOBS, NOTHING ELSE", issued 16:30 IST.
**Governed by:** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).

🏷️ **STATUS: `BUILT · GATED · ⛔ UNPUSHED · ⛔ UNDEPLOYED · ⛔ NOT VERIFIED LIVE`.**
⛔ **PUSHED: NO.** ⛔ **DEPLOYED: NO.** Deploy needs Rama's separate quoted word.

🔴 **TWO ITEMS STOPPED SHORT ON PURPOSE AND NEED HIS WORD — NI-5 (its own tripwire
fired) and the JOB 1 headline. Both are in §0 and §5.**

---

## §D — EVIDENCE LINE

| item | measured value |
|---|---|
| **Deployed SHA** | `45683859a0a05f466189ac5bc98f9a9f089f98d3` (`origin/main`), measured with `git rev-parse origin/main` |
| **BASE for this pass** | **`d00e574323a0b19cf0f98c3fca65031925d027cc`** — fix item 1, whose parent is `4568385` (verified: `git rev-parse d00e574^` → `4568385`). ⛔ Confirmed by measurement, ⛔ not assumed from the card |
| **Build worktree** | `scratchpad/j2-work`, branch **`fix/delivery-fill-and-ni-22aug`**, 7 commits ahead of `d00e574`, **8 ahead of `origin/main`**, 0 behind |
| **Gate base worktree** | `scratchpad/j2-base`, detached at `d00e574` |
| **Branch CONTENT, not name** | `d00e574` is an ancestor of this branch, so deploying this head ships item 1 as well. `fix/delivery-config-independence-22aug` still points at `d00e574` and is **untouched** — item 1's gated unit is preserved exactly as the ledger records it |
| **Root worktree** | ⛔ **UNTOUCHED.** Still `feat/delivery-config-split` `6d24a83`; `docs/MASTER_PENDING_01-Aug-2026.md` still uncommitted and intact. Only new untracked files were added under `docs/audit/` |
| **Out of scope, and not read** | ⛔ Rama's uploaded config · ⛔ `65b7196` · ⛔ `feat/delivery-config-split`'s content · ⛔ the allocation model · ⛔ the "PLANNING BASIS". Left as evidence, ⛔ not revived, ⛔ not deleted |
| **Frozen prediction** | `docs/audit/PREDICTION_job1_ni_22-Aug-2026.md`, **8,170 B**, md5 **`6a56833191e6e7a7799717be8a969c6f`**, hashed BEFORE the first line was written |

---

## §0a — 🔴 THE OPEN PROVENANCE QUESTION, AND WHAT I DID **NOT** TREAT THE CARD AS

The deploy ledger's top block, written **22-Aug ~15:3x**, records a tripped provenance
gate and this line verbatim:

> 🔴 **RAMA MUST DECIDE BEFORE ANY MORE EFFORT:** ① does `FIX-F1` (`d00e574`) stand, or
> does `65b7196` supersede it? ② is `FIX-F2a` a new build or the REVIVAL of `65b7196`?
> ③ `65b7196` carries a **SCHEMA change** …

**This card was issued at 16:30 — after that block — and it scopes the work: base on
`d00e574`, and `65b7196` / `feat/delivery-config-split` / the allocation model are
explicitly OUT OF SCOPE, "not revived, not merged, not read, not deleted."** I built to
that instruction, and nothing in this pass touched any of them.

⛔ **I am NOT recording that as Rama's ruling on ①, ② or ③.** A card does not speak for
Rama (`WC-PATTERN #7`). Those three questions stay **OPEN** in the ledger. What is true
and measurable is narrower: this pass extends `d00e574`, changes nothing about
`65b7196`, and carries **no schema change of any kind** — so it forecloses none of the
three answers. If ① is later answered *"`65b7196` supersedes it"*, these seven commits
come off with `d00e574` and cost nothing extra.

---

## §0 — 🔴 THE HEADLINE: JOB 1 FILLS NOTHING, AND THAT IS THE FINDING

**The sweep found ZERO delivery-scoped settings that are `null`, absent, or unset.
All 13 that can exist are already written explicitly with a value.**
`config/system_config.yaml` therefore carries **no JOB 1 edit at all** — the only
change to that file in this whole pass is NI-3's comment block.

**Why the sweep is closed rather than best-effort.** All 64 pydantic models in
`core/config_loader.py` declare `extra="forbid"` — measured, with a control proving
an unknown key is rejected. So the set of *possible* config keys **is** the schema
field set, and walking the schema across every file in `_CONFIG_FILES` enumerates
every delivery-scoped setting that can exist. There is no "and maybe others" tail.

**🔴 The trap this finding avoided, stated plainly.** Two delivery-scoped keys look
like fill candidates because their schema defaults were silent:
`max_open_delivery_positions` (3) and `max_daily_delivery_trades` (5). Their
INTRADAY twins are **5** and **10**. Executing "write the intraday value of the same
setting" on them would have moved two **live risk limits — 3→5 and 5→10** — loosening
the delivery book's slot cap and daily cap on real money. The card's own tripwire
covers it exactly: *"IF A FILLED VALUE CHANGES A COMPUTED QUANTITY, IT CAME FROM THE
WRONG PLACE."* They were **not filled**. Their silent schema defaults are a different
defect and are fixed as **NI-4**, values untouched.

⚠️ **The alternative reading, listed and left alone as J-3 requires.** "Delivery-scoped"
could instead be read as *any* sizing/risk setting that governs the delivery book —
which would mean inventing delivery twins for `min_qty_threshold`, `min_tick_size`,
`max_single_order_qty`, `lot_skew_rejection_threshold`, `max_consecutive_losses`,
`price_drift_threshold`, `sector_unknown_alert_pct` and the tier multipliers. **⛔ Not
done**, because J-5 forbids it — *"do not add a key the live code has no consumer
for"* — and each would need a NEW consumer in the sizer or the gate, which is new
logic and not behaviour-neutral. **If that was the intent, say so and it becomes its
own unit.**

---

## §1 — JOB 1 TABLE: EVERY DELIVERY-SCOPED SETTING THAT CAN EXIST

Discovered by walking the schema, not by trusting any list — including the card's.

⚠️ **`M3` — every `file:line` below is measured at the BASE `d00e574` and holds only
there.** NI-3 added comment lines, so at the unit head `742d9da` the two `risk_engine`
sites are `:544` and `:632`.

| # | key | intraday counterpart | intraday value | delivery BEFORE | delivery AFTER | live code reads it | changes a computed quantity |
|---|---|---|---|---|---|---|---|
| 1 | `position_sizing.delivery_risk_per_trade_pct` | `risk_per_trade_pct` | 0.01 | **0.01** | 0.01 *(no change)* | ✅ `position_sizer.py:357` → `:438` | **NO** |
| 2 | `position_sizing.delivery_max_concentration_pct` | `max_concentration_pct` | 0.10 | **0.10** | 0.10 *(no change)* | ✅ `position_sizer.py:359` → `:480` | **NO** |
| 3 | `position_sizing.delivery_max_position_value_pct` | `max_position_value_pct` | 0.40 | **0.40** | 0.40 *(no change)* | ✅ `position_sizer.py:361` → `:636` | **NO** |
| 4 | `risk.delivery_max_sector_exposure_pct` | `max_sector_exposure_pct` | 0.40 | **0.40** | 0.40 *(no change)* | ✅ `risk_engine` gate 8 | **NO** |
| 5 | `risk.delivery_daily_loss_limit_pct` | `daily_loss_limit_pct` | 0.03 | **0.03** | 0.03 *(no change)* | ✅ `risk_engine` gate 7 | **NO** |
| 6 | `risk.max_open_delivery_positions` | `max_open_positions` | **5** | **3** | **3** *(⛔ NOT filled)* | ✅ `risk_engine.py:538` | **NO** — filling it would have made it **5** |
| 7 | `risk.max_daily_delivery_trades` | `max_daily_trades` | **10** | **5** | **5** *(⛔ NOT filled)* | ✅ `risk_engine.py:622` | **NO** — filling it would have made it **10** |
| 8 | `capital.positional_bucket_pct` | `intraday_bucket_pct` | 0.70 | **0.30** | 0.30 *(no change)* | ✅ `fund_manager` | **NO** — a complementary pair, ⛔ not a twin; they must sum to 1 |
| 9 | `capital.gtt_sl_limit_offset_pct` | `sl_limit_offset_pct` | **0.005** | **0.03** | **0.03** *(⛔ NOT filled)* | ✅ `orders/cnc_gtt.py:74` | **NO** — deliberately 6× WIDER so an overnight gap-down still fills |
| 10 | `capital.leverage_map.DELIVERY` | `leverage_map.INTRADAY` | **5.0** | **1.0** | **1.0** *(⛔ NOT filled)* | ✅ `fund_manager.py:267` | **NO** — CNC has no leverage; a broker fact, not a policy |
| 11 | `delivery_enabled` | `force_intraday_only` | false | **true** | true *(no change)* | ✅ `zerodha_adapter.py:558` | **OUT of J-3** — a boolean feature switch |
| 12 | `broker_costs zerodha.stt_cnc_pct` | `stt_sell_pct` | **0.025** | **0.1** | **0.1** *(⛔ NOT filled)* | ✅ `cost_calculator.py:169` | **OUT of J-3** — a statutory tax rate, not sizing or risk |
| 13 | `broker_costs zerodha.stamp_duty_cnc_buy_pct` | `stamp_duty_mis_buy_pct` | **0.003** | **0.015** | **0.015** *(⛔ NOT filled)* | ✅ `cost_calculator.py` | **OUT of J-3** — statutory |

**Every row: "changes a computed quantity" = NO.** Rows 6, 7, 9, 10, 12, 13 are the
ones where filling from intraday would have changed one, which is why they were not
filled. Rows 1–5 were already set to the intraday value by fix item 1.

**Pinned as a property, not a snapshot.** `tests/unit/test_delivery_config_inventory.py`
asserts that **no** delivery-scoped setting is absent or null, that the discovery is
non-vacuous (≥13 fields, ≥2 files, ≥4 sections), that `extra="forbid"` really closes
the key universe (with a rejection control), and that the inventory equals a **named**
recorded set — so a NEW delivery key added to the schema and forgotten in the YAML
turns it red and says WHICH key. Three parametrised controls delete and null a real
key to prove the checker complains. Verified once more from outside the suite:
nulling `delivery_risk_per_trade_pct` in the actual YAML (byte-level, binary mode)
turns the property test **RED**; the file was restored **md5-identical**.

---

## §2 — J-4: KEYS WITH NO INTRADAY COUNTERPART

**None.** Every one of the 13 has a counterpart, so J-4's stop condition never fired.

Two are worth naming anyway, because their counterpart exists but is **deliberately a
different number** — copying it would have been the wrong act:

- **`capital.gtt_sl_limit_offset_pct` = 0.03** vs `sl_limit_offset_pct` = 0.005. A CNC
  OCO-GTT stop rests 3% below its trigger *on purpose*, so an overnight gap-down still
  fills within the floor. The 0.5% intraday offset would leave it resting unfilled.
- **`capital.leverage_map.DELIVERY` = 1.0** vs `INTRADAY` = 5.0. CNC carries no
  leverage. This is a broker fact.

---

## §3 — JOB 2, ITEM BY ITEM

### 🔴 NI-1 — the warning that crashed instead of warning · **FIXED** · `4928941`

| | |
|---|---|
| **file:line** | `capital/position_sizer.py:328` and `:334` **at `d00e574`** (the card's `:278`/`:284` are the `4568385` numbers — `M3`: line numbers hold only at their measured SHA) |
| **the defect** | both PS10 sites passed `"msg"` in the payload handed to `_warn`, which does `self._log.warning(msg, extra=extra)`. `"msg"` is a reserved `LogRecord` attribute, so `makeRecord` raises `KeyError`. **Proven by experiment on the base tree, ⛔ not by reading:** a BUY with `sl > entry` raises `KeyError: "Attempt to overwrite 'msg' in LogRecord"` out of `calculate()` |
| **the fix** | `"msg"` → `"detail"` at both sites — one word each. Plus a comment at `_warn` recording the constraint so the next payload cannot reintroduce it |
| **the test** | `tests/unit/test_position_sizer.py` — BUY and SELL through a **REAL `logging.Logger`** with a handler that keeps the `LogRecord` objects; asserts the record carries `detail`, `side`, `entry`, `sl`, and that it **formats** (the failure mode was inside record construction). Plus a **control** that feeds the OLD `"msg"` payload to the same real logger and requires it to still raise. Plus an **AST class sweep** of the whole file for any reserved attribute name, with the reserved set **derived from a live `LogRecord`** rather than hard-coded, and an assertion that it inspected ≥2 payload dicts so it cannot pass by finding nothing |
| **🔴 measured both ways** | on the BASE tree the three new tests **FAIL** and the sweep names both sites — `position_sizer.py:328 -> 'msg'`, `:334 -> 'msg'` — while **the two old tests PASS**. That is the card's point demonstrated, not asserted: `_MockLogger.warning` appends to a list and never builds a `LogRecord`, so a fake logger cannot see a logging bug. Base worktree restored clean afterwards |

### 🟠 NI-2 — the consistency check that ignored a multiplier · **FIXED** · `c146eb7`

| | |
|---|---|
| **file:line** | `core/config_auditor.py:414` (base numbering) — the C2 ladder check |
| **the defect** | it compared `max_position_value_pct <= max_concentration_pct` directly. The tier/perf multiplier is applied **after** the concentration constraint (`tiered_qty = floor(raw_qty × effective_mult)`, then clamped to `raw_qty × 2`), so the routine ceiling is `max_concentration_pct × the largest multiplier sizing can produce`. A config could pass C2 while the backstop bound on **routine** sizing — the exact condition C2 exists to prevent |
| **the fix** | C2 evaluates the effective ceiling. The multiplier is **derived** — `max(tier weights) × max_multiplier`, clamped by the sizer's own hard 2× tiered-qty ceiling — so raising a tier weight or `max_multiplier` moves the check with it. The finding's metrics now carry `max_effective_multiplier` and `effective_concentration_ceiling` |
| **⛔ not touched** | the multiplier's own policy. `perf_weight` is still unwired (`main.py` builds `SignalProcessor` with no `perf_weights`, so `.get(name, 1.0)` always returns 1.0). That is why the effective ceiling is 1.0 in practice today, and it is deliberately left exactly as it was |
| **the test** | three, all with **multiplier ≠ 1**: (a) the `conc 0.25 / posv 0.40` config the old check passed — C2 now fires, and the test asserts the OLD comparison's silence as an explicit premise; (b) the same conc/posv with `max_multiplier=1.0` — C2 stays silent, proving the multiplier term is live rather than a `2` baked in; (c) the shipped config stays silent with the margin asserted. The pre-existing C2 test passes unchanged |
| **behaviour-neutral on the live config** | measured: `0.10 × 2.0 = 0.20` vs a `0.40` backstop — a 2× margin. `audit_app_config()` on the real config still returns **verdict PASS with zero C-group findings** |
| **measured both ways** | on the base tree the multiplier test FAILS and the other two PASS |

### 🟡 NI-3 — comments that misdescribed live behaviour · **FIXED** · `5a7dbf6`

**The card named three sites. A sweep found SIX.**

| site | named by the card? |
|---|---|
| `config/system_config.yaml:214-215` | ✅ (×2) |
| `capital/risk_engine.py` OPEN_POSITIONS / DAILY_TRADES | ✅ (×2) |
| `core/config_loader.py` `RiskConfig` | ⭐ found |
| `core/state_store.py` — on the two COUNT QUERIES that feed the caps, claiming both "return 0" | ⭐ found — **the one that matters most of the six** |
| `tests/unit/test_phase3_delivery_caps_conditional_capital.py` header | ⭐ found |

**⛔ Deliberately NOT touched, and why.** `docs/SYSTEM_MAP.md` carries the same wording
in its 25/26-Jun entries — it is a **DATED changelog** and those entries were TRUE when
written; rewriting a dated record to match today would falsify the history, a worse
defect than the one being fixed. And `orders/cnc_gtt_monitor.py:26` /
`scripts/t2_cnc_gtt_realtest.py:5` say *"delivery_enabled stays false"* about the **GTT
lifecycle phase**, not about these caps — same claim family, different subject, **reported
as still open** rather than quietly swept in.

**The replacement does not quote the old wording.** A stale claim quoted in place still
reads as current, and it would defeat any sweep that looks for it. The exact old text is
in the commit diff, which is what a diff is for.

**🔴 NO LOGIC CHANGED — measured, not asserted.** `config/system_config.yaml` parses to
an **IDENTICAL object** base vs this tree; `capital/risk_engine.py`, `core/config_loader.py`
and `core/state_store.py` are **AST-IDENTICAL** to base (pure `#` comment edits); and a
control renaming one method proves the AST comparison can go red.

**The test** (`tests/unit/test_ni3_delivery_count_caps_are_live.py`) checks the claim
family is gone from all six sites, runs the identical matcher over the **pre-NI-3
wording** as a control so the sweep cannot pass by failing to recognise the claim,
asserts the antecedent really is false in the shipped config (if `force_intraday_only`
is ever set back to true this goes RED — correct, because the new comments say ENFORCED),
and links "ENFORCED" to the wired branch without duplicating the behavioural proof that
already exists in `test_phase3_delivery_caps_conditional_capital.py`.

### 🟡 NI-4 — the two remaining silent delivery defaults · **FIXED** · `6ad328e`

| | |
|---|---|
| **file:line** | `core/config_loader.py:555-556` at `d00e574` (the card's `:536-537` are the `4568385` numbers) |
| **the defect** | `max_open_delivery_positions: int = 3` / `max_daily_delivery_trades: int = 5`. Delete either from the YAML and the system **BOOTED on the hardcoded number** instead of refusing — the same class item 1 removed for its five keys |
| **the fix** | both become `Optional[int]` with **no default**, plus a dedicated validator that rejects `None`. Split out of `_validate_positive_int` on purpose: a shared validator would report *"must be >= 1"* for a missing key, which says nothing about the fallback |
| **⛔ values unchanged** | 3 and 5 stay. **This is where JOB 1 would have done damage** — see §0 |
| **measured end-to-end**, through the line the boot actually logs | `\| risk.max_open_delivery_positions: Field required` · `\| risk.max_daily_delivery_trades: Value error, delivery count cap must be set explicitly to an integer >= 1; it does NOT fall back to a built-in default` · a 0 still gives `>= 1`. Path: `load_all` → `ConfigSchemaError` → `main._config_error_detail` → CRITICAL → **exit 5** |
| **the test** | 10 assertions incl. a **control** that an untouched copy of `config/` still loads (so the rejections are the schema's doing, not an artifact of copying), a separate `no_silent_3_or_5` assertion (*"it raised"* and *"it did not silently default"* are different claims and only the second is the defect), and the shipped values pinned as tighter than their intraday twins |
| **measured both ways** | 6 of the 10 FAIL on the base tree, one of them literally reporting `max_open_delivery_positions silently defaulted to 3` |
| **overlap with JOB 1** | ⭐ **Yes, and it was done ONCE.** JOB 1's sweep surfaced these two; JOB 1 correctly filled nothing (their values are right), NI-4 fixed the schema. ⛔ Not fixed twice |

### ⚠️ NI-5 — unsafe position-sizer constructor defaults · **🔴 STOPPED, NOT SHIPPED**

**Built in full, then REVERTED, because the card's own tripwire fired.** See §5.

### ⚪ NI-6 — the config-hash change is correct · **RECORDED** · `4c495d0`

Nothing fixed. The reason is recorded at
`core/config_snapshotter._resolve_config_dict` — the function that decides what gets
hashed — so it is where someone will look.

**Two independent reasons, both MEASURED:**

1. Item 1 made five delivery keys explicit, so the dumped config gains five fields. A
   real config change, correctly recorded.
2. ⭐ **The one that will catch someone out:** `AppConfig` carries `file_hashes` — the
   sha256 of each config file's **RAW BYTES** — and that dict is **inside** the hashed
   payload. So a **COMMENT-ONLY** edit moves `config_hash` while every VALUE is
   unchanged. Measured: NI-3 in this same pass edited only comments; the canonical JSON
   stayed **16,206 bytes**, every value was identical, and `config_hash` went
   `4bed2598…` → `1b163ca4…`.

⇒ **THE RULE:** a `config_hash` change is evidence that a config **FILE** changed. It is
⛔ **NOT** evidence that a config **VALUE** changed. To answer *"did a value move?"*, diff
`config_json` — ⛔ never the hash.

Pinned by `tests/unit/test_ni6_config_hash_change_is_expected.py`, which asserts the
mechanism (if `file_hashes` ever leaves the payload the note is wrong and the test says
so), reproduces the comment-only case end-to-end on a copied config, and confirms the
five item-1 keys are in the snapshot. Executable code in `config_snapshotter.py` is
**AST-identical** to base with docstrings stripped, control-verified.

### ⚪ NI-7 — the stale filename · **RENAMED** · `742d9da`

`tests/unit/test_position_sizer_delivery_scaffold.py` → `..._delivery_contract.py`.
**A pure rename:** md5 `460b07c00cd8fa9c97491748c989f713` before and after, git reports
`rename … (100%)`, **0 insertions / 0 deletions**, the 5 tests pass unchanged.

⚠️ **Reported, not fixed:** the file's own docstring still opens with the OLD path on
line 2, and its parenthetical still says the stale name was *"recorded, not silently
renamed"* — both now stale. Left alone deliberately: any content edit breaks the 100%
similarity, and a provably-nothing-but-a-rename diff is the one reviewable at a glance.
Three docs also name the old path — `docs/SYSTEM_MAP.md`,
`docs/v3/V3_STEP5_RISK_SIZING_GAPMAP.md`, `PATHS.md` — all **dated** entries recording
what V3 Step 5 built on 12-Jul, when that WAS the path. Same reasoning as NI-3's
SYSTEM_MAP decision.

### 🧠 NI-8 — the memory line budget · **DONE**

**80 lines over budget → 0.** Measured with the recorded control itself, in **BYTES**:

```
LC_ALL=C awk 'length>(index($0,"🔝")?450:300){print FILENAME" "FNR": "length}' MEMORY*.md
```

⚠️ **A measurement correction worth stating:** my first inventory counted **characters**
and reported 73. The recorded control counts **bytes** (`LC_ALL=C`), and the header says
`≤300 B`. Emoji are 4 bytes each, so the character count understated it. Re-measured in
bytes: **80**, matching the control exactly — `ARCHIVE 57 · BOARD 22 · REFERENCE 1`,
`MEMORY.md` clean.

**Fixed by RELOCATING, ⛔ never by raising the cap.** For each line the **ORIGINAL was
appended VERBATIM** to its topic file under a dated heading *before* the index line was
trimmed, so the pass is lossless by construction. 34 new topic files were created where
no target existed; the index lines keep their tags, their headline and their link.

| check | result |
|---|---|
| the recorded control | prints **NOTHING** (was 80 lines) |
| the control can still go red | ✅ a planted 600 B line is detected |
| index line counts | **unchanged** — 123 / 162 / 46 / 208. Nothing added, nothing deleted |
| total bytes across the memory dir | **grew** 4,297,356 → 4,342,399 — relocation, not deletion |
| **every one of the 80 original lines still present VERBATIM somewhere in the corpus** | ✅ **80 checked, 0 missing** |
| backup | the whole memory dir was copied before the pass |

`MEMORY.md` itself was **not touched** — it was already clean, and adding 34 pointer
lines to it would have worked against the very budget being satisfied. The relocated
lines are reachable from the BOARD/ARCHIVE lines that now link them.

---

## §4 — ISSUES FOUND EN ROUTE (⛔ none fixed; all reported)

**NI-9 — `RiskEngine.__init__` still defaults the two delivery COUNT caps.**
`capital/risk_engine.py:160-161` keeps `max_open_delivery_positions: int = 3` /
`max_daily_delivery_trades: int = 5`. NI-4 closes the **config** half completely (a
missing YAML key now refuses at boot), but a RiskEngine built **outside** the config
path still gets a silent 3/5 — and `RiskEngine`'s own docstring says it *"takes NO
defaults"*, so it contradicts itself on exactly these two. Unreachable in production
(one construction site, `main.py`, wired from now-required config). **Measured cost to
close it the way item 1 closed its five: 2 test files** —
`tests/unit/test_delivery_config_independence.py:251` and
`tests/unit/test_risk_engine.py:181` are the only RiskEngine sites that gate a
positional entry without passing the caps. ⛔ Not done: one fix per commit, and the card
scoped NI-4 to the schema.

**NI-10 — NI-5 would make the config auditor's group-F guard vacuous.** See §5.

**NI-11 — C2 has no delivery pair.** `core/config_auditor.py`'s C2 ladder checks only
the global `max_concentration_pct` / `max_position_value_pct`. Since item 1 there is a
delivery pair with identical semantics, and **C2 does not check it at all**. NI-2 fixed
the multiplier as the card specified; adding a delivery arm is *adding a check*, not
fixing one. ⛔ Not done.

**NI-12 — two more "delivery_enabled stays false" claims, different subject.**
`orders/cnc_gtt_monitor.py:26` and `scripts/t2_cnc_gtt_realtest.py:5`. Same stale-claim
family as NI-3 but about the GTT lifecycle phase, not the count caps. ⛔ Not touched.

**NI-13 — the renamed test file's own docstring is now stale.** See NI-7.

**⭐ RECORDED, ⛔ NOT FIXED, as the card instructs — `sl_gap_buffer_pct` means PERCENT
while every other `_pct` in `system_config.yaml` means a FRACTION.**
`signals/signal_processor.py:1715` divides it by 100, so `0.3` means 0.3%. Four
strategy YAMLs carry it (`gap_fade_long/short`, `gap_go_long/short`) and it is live
09:15–09:30. Setting it to `30` intending 30% would give a 30× wider stop. ⚠️ Note the
same convention split exists in `config/broker_costs.yaml`, whose header says so
explicitly: *"All `_pct` fields are PERCENTAGES (e.g. 0.03 means 0.03%)"*. ⛔ Not fixed.

**A process note on my own work.** My first null-sweep script printed *"NULL-VALUED
KEYS: 0"* — because it **defined** the walker and never **called** it. A vacuous check
that would have produced the right answer for the wrong reason. It was caught by
cross-checking against a grep that found two nulls, then rewritten with a control that
forces a known key to null and requires the sweep to report it. `V5`.

---

## §5 — 🔴 NI-5: BUILT, MEASURED, THEN STOPPED. RAMA'S CALL.

**The card's tripwire:** *"you measured ~20 test sites. If the diff exceeds that, or
reaches beyond position_sizer and its tests, ⛔ STOP and report."*
**And:** *"If a test fails because the system encodes a DELIBERATE POLICY rather than a
bug, ⛔ STOP and report."*

**Both fired. NI-5 is reverted and is NOT in any commit.**

### What was built (and is preserved)

The classification the card asked for, made explicitly rather than by deleting
everything:

| class | parameters | reasoning |
|---|---|---|
| **SAFETY-CRITICAL POLICY** — loses its default | `risk_per_trade_pct` (0.01) · `max_concentration_pct` (0.10) · `max_position_value_pct` (0.40) | these three multiply capital into a number of shares. A silent value sizes REAL MONEY on a number nobody chose |
| **LEGITIMATE PROGRAMMING** — default kept | `min_qty_threshold` · `tier_multipliers` · `logger` · `instrument_cache` · `lot_skew_rejection_threshold` · `min_tick_size` · `max_single_order_qty` · `broker_adapter` · `enabled` · `flat_value_rs` · `delivery_*` | **none of these can ENLARGE a position.** They are a 1-share floor, tick/skew guards, a sanity cap, optional collaborators, a mode switch already guarded by its own raise, and item 1's delivery knobs whose `None` is a hard error on use |

### The diff, against the tripwire

| measure | value | verdict |
|---|---|---|
| `PositionSizer(...)` construction sites in the tree | **20** (AST-measured; **0 positional**, so re-ordering a parameter is safe) | matches the card's "~20" |
| sites needing an edit | **15**, in **8 files** | within budget |
| total diff | **10 files, 216 insertions, 11 deletions** | within budget |
| files outside `position_sizer` + its tests | **0** | ✅ inside the tripwire |
| **but** — files that MUST also change for the suite to be green | **2**: `core/config_auditor.py` + `tests/unit/test_config_auditor.py` | 🔴 **TRIPWIRE** |

### 🔴 Why it cannot be finished inside its own scope

`core/config_auditor.py` has a **group F, "stale-default guard"**, whose entire purpose
is to check that `PositionSizer.__init__`'s **default** for `max_position_value_pct`
still matches config. Remove the default and:

- group F hits `if default is inspect.Parameter.empty: continue` and **silently skips**
  that row;
- `test_config_auditor.py::TestGroupFStaleDefault::test_diverging_position_cap_default_warns`
  **FAILS** — correctly. It is not a broken test; it is a test noticing that its subject
  no longer exists;
- worse, group F's PASS message would still read *"component defaults match config
  intent (position-value cap + daily-loss pct)"* while having checked neither for the
  position-value cap — **NI-5 would CREATE a tautological check**, the `V5` class.

⛔ I did not silently reinterpret that deliberate policy as a defect, and I did not
ship a red test or a vacuous green one.

### The two ways forward — ⛔ I have not chosen

| | option | what it costs |
|---|---|---|
| **(a)** | **Extend NI-5's scope by two files.** Remove the three defaults, and in the same commit make group F's skip explicit and correct its PASS message so it names only what it actually checked; update the one group-F test. | +2 files beyond the tripwire, ~15 lines. Gives the full fix and leaves no vacuous check. **This is what I would do on your word.** |
| **(b)** | **Narrow NI-5** to `risk_per_trade_pct` and `max_concentration_pct` only, leaving `max_position_value_pct` defaulted so group F keeps working. | Stays inside the tripwire, but leaves the **catastrophic-loss backstop** as the one policy limit that still has a silent default — the least defensible one to leave. |

**Preserved, so either is one command away:**
`docs/audit/NI5_STOPPED_22-Aug-2026.patch`, **19,032 B**, md5 `e1bce4ac3583e2ff0f1f8c37c794fc7f` (untracked, alongside the other audit artifacts; a copy also sits in the session scratchpad).
The work tree was reverted and re-verified: clean at `742d9da`, and the touched suites
run **114 passed**.

---

## §6 — COMMITS

| # | hash | one line |
|---|---|---|
| 1 | `940a572` | `test(config): job 1 -- the delivery-setting sweep found nothing to fill, pinned` |
| 2 | `4928941` | `fix(sizing): NI-1 -- the SL-direction guard raised KeyError instead of warning` |
| 3 | `c146eb7` | `fix(auditor): NI-2 -- C2 compared the ceilings without the multiplier between them` |
| 4 | `5a7dbf6` | `docs(risk): NI-3 -- the delivery count caps are LIVE; the "inert" clause was stale` |
| 5 | `6ad328e` | `fix(config): NI-4 -- the last two delivery keys stop defaulting silently` |
| 6 | `4c495d0` | `docs(snapshot): NI-6 -- the first post-deploy config_hash change is CORRECT` |
| 7 | `742d9da` | `test(rename): NI-7 -- the file stopped testing a scaffold on 22-Aug; the name did not` |

**One commit per item, each independently reversible.** NI-5 has no commit (§5). NI-8
is outside the repo (mempalace files).

---

## §7 — GATE

### The exact command

```bash
python -m pytest tests/unit tests/integration -q > "$SP/${name}.out.txt" 2>&1
echo $? > "$SP/${name}.rc.txt"
```

⭐ **rc read from pytest ITSELF via file redirection** — ⛔ never `| tail; echo $?`, which
captures `tail`'s code and has produced a false `rc=0` on this campaign before.
⛔ `run_tests.py` was not used: the full tree `load_dotenv()`s the real `.env`.

### Environment — the launcher is part of the gate

| | |
|---|---|
| launcher | **Git Bash** — ⛔ never PowerShell |
| `python` | `/c/python311/python` → **Python 3.11.9** (both sides) |
| `python3` | the session **shim** (a copy of `python.exe`) → **Python 3.11.9**, ⛔ NOT the WindowsApps stub |
| `PATH` form | **POSIX `/c/...`** — a drive-letter colon splits a colon-separated PATH |
| pytest | **9.0.3** (both sides) |
| `config/instruments.csv` | planted into BOTH trees with `cp -p`, md5 `a7b07623909e051cb624ad157cee1671` — identical on both, ⛔ never `write_text` |
| `venv/` | absent in both fresh worktrees; `pick_python()` falls through to bare `python`, which here resolves to the real `C:\python311\python.exe`. **Identical on both sides** |
| ordering | **STRICTLY SEQUENTIAL** — `test_instance_lock` holds a machine-global lock |
| clock | both runs the same Saturday evening, 15 minutes apart |
| dirty | **0** on both sides, recorded at run time |

⚠️ **DISCLOSED, ⛔ not hidden — the FIRST launch died before it started.** Its shim
pre-check used the **Windows `C:/…`** PATH form; the drive-letter colon split `PATH`, so
`command -v python3` resolved to the WindowsApps stub and the script exited 49. **No
pytest ran, so no partial result exists.** The launcher itself already used the POSIX
form; the check around it did not. Fixed and relaunched from scratch.

⚠️ **Also disclosed:** an earlier **scouting** run of `tests/unit` alone (before the gate,
to find fixtures needing NI-4's keys) showed **3 extra `test_t4_deploy_preflight`
failures**. They are absent from both gate sides because that run had no `python3` shim
on PATH. ⛔ No number from that run is used anywhere here.

### 🔴 RAW PYTEST TAILS, BOTH SIDES

**BASE — `j2-base`, HEAD `d00e574323a0b19cf0f98c3fca65031925d027cc`, `dirty=0`, 19:59:24 → 20:15:16:**

```
FAILED tests/unit/test_closure_source_contract.py::test_no_module_restates_the_vocabulary_literals
FAILED tests/unit/test_fix181.py::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active
FAILED tests/unit/test_main.py::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret
FAILED tests/unit/test_main.py::TestContinueFromGate::test_price_hit_calls_placer_with_correct_prices
FAILED tests/unit/test_main.py::TestContinueFromGate::test_no_placer_releases_reservation_and_updates_status
FAILED tests/unit/test_main.py::TestContinueFromGate::test_stats_placed_incremented_on_success
FAILED tests/unit/test_phase17_batch2.py::test_fix077_flask_max_content_length
7 failed, 5715 passed, 4 skipped, 281 warnings in 946.90s (0:15:46)
```

`RAW_PYTEST_RC=1`

**UNIT — `j2-work`, HEAD `742d9dab5234682d40d2c538fce1b777a42b30e1`, `dirty=0`, 20:15:16 → 20:30:19:**

```
FAILED tests/unit/test_closure_source_contract.py::test_no_module_restates_the_vocabulary_literals
FAILED tests/unit/test_fix181.py::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active
FAILED tests/unit/test_main.py::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret
FAILED tests/unit/test_main.py::TestContinueFromGate::test_price_hit_calls_placer_with_correct_prices
FAILED tests/unit/test_main.py::TestContinueFromGate::test_no_placer_releases_reservation_and_updates_status
FAILED tests/unit/test_main.py::TestContinueFromGate::test_stats_placed_incremented_on_success
FAILED tests/unit/test_phase17_batch2.py::test_fix077_flask_max_content_length
7 failed, 5751 passed, 4 skipped, 281 warnings in 897.94s (0:14:57)
```

`RAW_PYTEST_RC=1`. 🏷️ Per `N12-16` `<RULE · BINDING>`: **a non-zero rc alone does NOT
fail the gate; an UNATTRIBUTED failure does.** All seven are attributed below.

### ID-level two-way differential — ⛔ ID-LEVEL ONLY, per `N20-19`

```
comm -13  (NEW on UNIT)           -> EMPTY  (0)
comm -23  (DISAPPEARED from BASE) -> EMPTY  (0)
comm -12  (COMMON)                -> 7
```

⛔ **No `failmsgs` artefact was produced at all** — `N20-19` records that a
"messages identical" claim on `pytest -q` output is vacuous, so nothing here can later
be mistaken for message-level evidence.

### ⭐ The harness is proven before the comparison is trusted

The base run of `d00e574` reproduces **item 1's own recorded UNIT measurement of
`d00e574`** — recorded there as `rc 1 · 7F / 5,715P / 4S` — measured here as
**`rc 1 · 7F / 5,715P / 4S`**. A base that did not reproduce the recorded baseline
would be a broken harness, not a finding. The 7 are the campaign's enumerated standing
set: `test_closure_source_contract` ×1 · `test_fix181` ×1 · `test_main` ×4 ·
`test_phase17_batch2` ×1 — identical name-for-name on both sides.

### The passed-count delta decomposes by arithmetic, ⛔ not waved through

`5,751 − 5,715 = +36`, and:

| source | collected |
|---|---|
| `tests/unit/test_delivery_config_inventory.py` (JOB 1, new) | **+8** |
| `tests/unit/test_ni3_delivery_count_caps_are_live.py` (new) | **+8** |
| `tests/unit/test_ni4_delivery_count_caps_required.py` (new) | **+10** |
| `tests/unit/test_ni6_config_hash_change_is_expected.py` (new) | **+3** |
| `tests/unit/test_position_sizer.py` 43 → 47 (NI-1) | **+4** |
| `tests/unit/test_config_auditor.py` 52 → 55 (NI-2) | **+3** |
| the NI-7 rename, 5 → 5 | **0** |
| | **= +36** ✓ |

⇒ **no test silently disappeared and none was silently added.**

### 🔴 BEHAVIOUR-NEUTRALITY — the card's own acceptance test, measured

A grid of **252 sizing computations** — 4 intents × 3 score tiers × 7 prices
(37 · 100 · 395.55 · 437.20 · 1058.70 · 1064.56 · 2500) × 3 stop distances — plus every
loaded sizing/risk/capital config value, plus the three recorded CNC risk-leg anchors
(CLSEL 18 · MANINDS 7 · KRONOX 25), dumped as canonical JSON on each tree:

```
j2-base -> 156,140 B      j2-work -> 156,140 B      diff -> IDENTICAL
```

Every `qty`, `margin_required`, `risk_amount`, `bucket`, `constraint` and every
`breakdown` field is the same number on both sides.

⭐ **And the comparison is proven able to go red:** planting **exactly the change JOB 1
would have made** — `max_open_delivery_positions: 3 → 5` — makes the diff fire
immediately. The config was then restored **md5-identical** and the work tree
re-verified clean.

### Frozen prediction, scored — ⛔ including the two that were WRONG

| | | |
|---|---|---|
| **P-1** | JOB 1 is behaviour-neutral because it is empty | ✅ **CONFIRMED** — JOB 1's commit touches one test file; the YAML's only change in the pass is NI-3's comment block |
| **P-2** | NI-1: two words, and the OLD tests cannot see it | ✅ **CONFIRMED** — measured both ways; the old two pass on the broken tree |
| **P-3** | NI-2: C2 is algebraically silent on the multiplier; zero new findings on the live config | ✅ **CONFIRMED** |
| **P-4** | NI-3 is comments only, and there are **FOUR** copies | ⚠️ **SPLIT — one half CONFIRMED, one half WRONG.** "No executable line" is ✅ CONFIRMED (parsed-object and AST identity, control-verified). **"FOUR" is WRONG — there are SIX.** I predicted the `config_loader` copy and missed `state_store` (the one on the count queries themselves) and the test-file header. ⛔ An undercount is still a wrong call and is scored as one |
| **P-5** | NI-4 behaviour-neutral; missing/null rejects naming the key | ✅ **CONFIRMED** |
| **P-6** | NI-5's diff stays inside the tripwire | ⚠️ **MEASUREMENTS CONFIRMED, CONCLUSION WRONG.** 20 sites / 0 positional / 15 edits / 8 files all held exactly. But the conclusion "stays inside the tripwire" did **not**: completing NI-5 requires `core/config_auditor.py` + its test, which the prediction did not anticipate. **The item was STOPPED, not shipped** (§5) |
| **P-7** | NI-7 is a pure R100 rename | ✅ **CONFIRMED** — md5 identical, `rename (100%)`, 0/0 lines |
| **P-8** | gate set-equality at ID level | ✅ **CONFIRMED** — 0 NEW / 0 DISAPPEARED, delta decomposes to +36 |
| **P-9** | nothing in the pass moves a computed quantity | ✅ **CONFIRMED** — 252-point grid byte-identical, with a control |

---

## §8 — STILL OPEN — ⛔ NONE OF THESE WAS TOUCHED

| item | status |
|---|---|
| **OPS ① — a systemd `OnFailure=` unit** | 🔴 **STILL OPEN, QUEUED.** Catches *every* boot failure and crash, not just this one. Needs a new unit file installed on the VM **by Rama** |
| **OPS ② — add `5` to `RestartPreventExitStatus`** | 🔴 **STILL OPEN, QUEUED.** One word in the unit file. ⚠️ **Weigh this before deploying:** the fail-closed behaviour approved for item 1 is *"the system refuses to start"*. What the unit file does today is *"the system refuses to start, ten times a minute, until someone notices."* ⭐ It also repairs `token_watcher`'s exit-code branches, because the service would settle in `failed` instead of cycling through `activating` |
| **The boot-path alert wiring** (option 1 — alert naming the exact key before `return 5`) | 🔴 **STILL OPEN, QUEUED.** ⛔ Not built in this pass |
| **The alert guard** — `token_watcher`'s `clear_alert_flags()` deletes the once-per-day flag on `active`/`activating`, so the guard is defeated during exactly the crash-loop it was written for | 🔴 **STILL OPEN.** ⛔ Not touched |
| **The exit-5 restart loop** | 🔴 **STILL OPEN** (= OPS ②) |
| **F2 / F2a / F2b / F2c** | 🔴 **STILL OPEN.** ⛔ Not read, ⛔ not started |
| **The MIS 3.5× decision** | 🔴 **HELD**, exactly as it was. ⛔ Not revisited, ⛔ not implied by anything here |
| **Segment-capital basis · ATR · S6 · strategy YAMLs · GUI** | ⛔ untouched — 0 strategy YAML files changed, verified by diff |
| **NI-5** | 🔴 **STOPPED — awaiting Rama's word** (§5) |
| **NI-9 · NI-11 · NI-12 · NI-13 · `sl_gap_buffer_pct`** | 🔴 **REPORTED, NOT FIXED** (§4) |

⚠️ **This pass must not be read as having closed any of the above.**

---

## §9 — LIMITS OBSERVED

⛔ **NOT DEPLOYED.** ⛔ **NOT PUSHED.** ⛔ No `sudo`. ⛔ No VM contact. ⛔ No paper run
offered as evidence — paper nets by SYMBOL while live Kite nets per (SYMBOL, PRODUCT),
so a paper drill of a delivery change is vacuously green.

⛔ No percentage, cap, count, multiplier or rupee value changed anywhere.
⛔ No strategy YAML touched (0 files). ⛔ No tier value touched. ⛔ No basis change.
⛔ No guard removed. ⛔ Rama's uploaded config not read. ⛔ `65b7196` /
`feat/delivery-config-split` not read, not merged, not deleted — left as evidence.
⛔ The root worktree was not switched and `MASTER_PENDING_01-Aug-2026.md` is intact.

---

# ADDENDUM — 22-Aug evening, after the pass was accepted

## §10 — THE TWO READINGS ARE NOT THE SAME · THE PARAMETER-PARITY LIST

Rama said two things. They are different questions and only one of them is answered.

| | reading | status |
|---|---|---|
| **A** | *"if empty then fill the same numbers from Intraday"* | ✅ **ANSWERED. ZERO found, nothing filled.** All 13 delivery-scoped settings that can exist are already explicit and non-null |
| **B** | *"Intraday config settings/parameters = Delivery settings parameters"* | ⚠️ **NOT ANSWERED — and it is a different thing.** This is **PARAMETER PARITY**: delivery having a *twin for every intraday sizing parameter*. Some intraday parameters have **no delivery counterpart at all** |

🔴 **Reading B is ⛔ NOT a config fill and ⛔ NOT behaviour-neutral.** Every new key needs a
**runtime consumer** — a branch in `position_sizer` or `risk_engine` that reads the delivery
key on a positional entry. That is a build, with its own gate and its own blast radius.
⛔ **Nothing below was created.** The list is here so the decision can be made with it in view.

### Measured: 31 global parameters across `position_sizing` / `risk` / `capital`; **7** have a delivery twin

#### 🔴 GROUP 1 — no twin, and **READ ON THE DELIVERY PATH TODAY**. A twin here WOULD change delivery behaviour.

Measured against the bucket split at `position_sizer.py:338` (`d00e574`): every one of
these is read **after** it, unconditionally, so it applies to **both books**.

| parameter | shipped | read at | note |
|---|---|---|---|
| `position_sizing.min_tick_size` | `0.05` | `:411` | rejects a sub-tick SL |
| `position_sizing.max_single_order_qty` | `10000` | `:443` | sanity cap on qty |
| `position_sizing.tier_multipliers` | `HIGH 1.0 / MEDIUM 0.70 / LOW 0.50` | `:502`, `:524` | ⚠️ **ONE dict serves BOTH books** — a tier change already moves delivery |
| `position_sizing.lot_skew_rejection_threshold` | `0.25` | `:617` | rejects on lot skew |
| `position_sizing.min_qty_threshold` | `1` | `:681` | the 1-share floor |
| `risk.max_consecutive_losses` | `4` | `risk_engine` gate | ⚠️ **deliberately shared** — recorded as such in F1's `RE18` |

#### ⚪ GROUP 2 — no twin, and **NO PRODUCTION READER AT ALL**. A twin would be a key nothing reads (J-5 forbids).

| parameter | shipped | only reader |
|---|---|---|
| `position_sizing.min_multiplier` | `0.5` | `ops_dashboard` display |
| `position_sizing.max_multiplier` | `2.0` | `ops_dashboard` display — ⭐ **plus `config_auditor`'s C2 as of NI-2, which is its first non-display use** |

#### ⚪ GROUP 3 — no twin, but **not sizing**: order/exit/observability path

| parameter | shipped | reader |
|---|---|---|
| `capital.slm_margin_buffer_pct` | `0.05` | `fund_manager.py:341` — SL-M margin |
| `capital.emergency_exit_buffer_pct` | `0.01` | `kill_switch.py:254` — ⚠️ HARD_KILL flattens only MIS/CO, so in effect intraday-only |
| `risk.price_drift_threshold` | `0.005` | `order_placer.py:1207` — pre-placement margin top-up |
| `risk.sector_unknown_alert_pct` | `0.20` | `order_placer.py:640` — data-quality alert |
| `position_sizing.flat_value_rs` | `null` | mode-gated; the flat-sizing mode is OFF (`enabled: true`) |

#### ✅ GROUP 4 — LOOK like they have no twin, but they DO (differently named)

⚠️ A naive `delivery_`-prefix sweep reports these as gaps. They are not — and filling them
would be the same class of mistake as the count caps.

| intraday | its delivery counterpart | note |
|---|---|---|
| `capital.intraday_bucket_pct` `0.70` | `capital.positional_bucket_pct` `0.30` | a complementary pair; they must sum to 1 |
| `capital.sl_limit_offset_pct` `0.005` | `capital.gtt_sl_limit_offset_pct` `0.03` | deliberately **6× wider** for an overnight gap |
| `capital.leverage_map.INTRADAY` `5.0` | `capital.leverage_map.DELIVERY` `1.0` | CNC has no leverage — a broker fact |

#### ⛔ OUT of J-3 scope entirely (non-numeric)

`position_sizing.dynamic_by_winrate` · `position_sizing.enabled` ·
`risk.one_trade_per_symbol_direction_per_day` · `risk.daily_loss_include_unrealized` ·
`risk.sector_cap_mode` · `capital.conditional_allocation_enabled`

### ⭐ The honest summary for the decision

**Six numeric parameters (Group 1) genuinely govern the delivery book today with no
delivery-scoped key of their own.** Two of them are already flagged elsewhere in the
campaign: `tier_multipliers` (one dict, both books) and `max_consecutive_losses`
(deliberately shared). Groups 2–4 should ⛔ **not** be given twins — they would be keys with
no consumer, non-sizing knobs, or twins that already exist under another name.

⛔ **None of this was created. ⛔ No key was added. ⛔ No consumer was written.**
