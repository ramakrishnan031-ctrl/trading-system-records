---
name: fix2-preflight-capital-checks-10aug
description: "FIX 2 BUILT (13df9cd, branch fix/preflight-capital-coherence off the DEPLOYED 645728d, UNPUSHED): capital_deployment had NO predicate at all and passed 432.3%; the bound used is the capital identity the system already enforces, so no number was invented. kite_funds_available was STOPPED — adequacy needs a threshold policy does not define."
metadata: 
  node_type: memory
  type: project
  originSessionId: 55f762b9-1f1c-4ab4-b80b-c1b50da706f7
  modified: 2026-08-10T09:13:47.492Z
---

**`<BUILT · TESTED · ⛔ NOT PUSHED · ⛔ NOT DEPLOYED>`**
Branch **`fix/preflight-capital-coherence`** off the **DEPLOYED** ref `645728d`, **seventh
worktree** `D:\Projects\trading-system-fix2`. 🔴 `git worktree remove` when done.
🔑 **TIP = `4bd8a42` (docs-only). THE CODE IS TWO COMMITS: `13df9cd` `capital_deployment` +
`ee3ff49` the `₹2,000` floor.** *(Docs-only proven both times by an EMPTY
`git diff <code>..HEAD -- '*.py' '*.yaml' '*.sql'`.)* ⛔ **A push pushes the TIP — quote `4bd8a42`
when pushing, `13df9cd`/`ee3ff49` when talking about behaviour.**
⚠️ **PROVENANCE (`G1`): the card's `start Fix 2` was an AUTO-FILL, ⛔ not Rama** — it proceeds
because Rama said *"start to fix"* and the card itself authorised the scope. **Recorded, not assumed.**

---

## ① `capital_deployment` — ✅ **BUILT**

**⛔ IT HAD NO PREDICATE AT ALL** — ⛔ not a threshold set too loosely: **every reachable path below
the div-0 guard returned `self._passed()`**, so it could not have gone non-green for ANY input.
🔴 **It printed `capital deployed 432.3%` and PASSED, on the same 08:15 boot the capital invariant
HARD-KILLED.** [[tautological-check-class-05aug]]

### ⭐⭐ **AND `432.3 %` IS NOT A DEPLOYMENT LEVEL — IT IS TWO OPERANDS ON DIFFERENT BASES**
| operand | source | what it is |
|---|---|---|
| **denominator** `opening` | first `INIT` `fm_ledger` row | **broker CASH** *(`fund_manager.py:468-476` writes `broker_balance` verbatim)* |
| **numerator** `margin_used` | `SUM(trades.margin_reserved)` over `OPEN/PARTIAL/EXITING` | **includes a CARRY whose money is already in stock** |

⚠️ **AND FIX 1 DOES NOT CHANGE THIS READING** — Fix 1 lifts `_total` **in memory only** and writes no
ledger row for the carry ⇒ the `INIT` row still holds CASH and this check would still print `432.3 %`
on the same day. ⭐ **The two fixes are genuinely independent.** Same class as
[[tick1-threshold-base-mixup-09aug]]: **every percentage carries its base or it is not a number.**

### 🔑 **NO NUMBER WAS INVENTED — the bound is the identity ALREADY ENFORCED**
`if used > opening → _warn`. Buckets partition ONE total (`0.70 + 0.30 = 1.0`) and `_check_invariant`
holds `avail+reserved+used == cash_floor` all non-negative (INV6) ⇒ **deployed margin can NEVER exceed
the capital it was reserved from**, so `used > opening` is reachable **only via a carry**. **The bound
is 100 %, and 100 % is the sum of the split.**
⛔ **`portfolio_allocator.max_portfolio_deployment_pct` is the ONLY key in the tree with the right
shape and it is `null` = INERT in a `shadow`-mode component — ⛔ NOT treated as an authored ceiling.**

🔒 **SEVERITY UNCHANGED — the 25-Jul ruling is INTACT:** still `Criticality.WARN`, and
**`report.py:44-51` makes `is_blocking` = `FAIL` **AND** `CRITICAL`** ⇒ a WARN can never block a run or
make it CRITICAL. ⭐ **What changed is ONLY that the check CAN now be non-green.**

⛔ **NOT DONE, NAMED: the denominator is STILL CASH.** Correcting it means re-deriving Fix 1's carry
rule **inside preflight = a SECOND site for one semantic**, the exact defect Fix 1 removed — and it
needs a product split `trades` cannot answer *(⛔ no `trades.product` column;
[[schema-product-is-on-orders-05aug]])*. **The operands are printed WITH their bases instead.**

---

## ②b ✅ **ANSWERED AND BUILT SAME DAY — `₹2,000` (`ee3ff49`)**

📜 **RAMA, 10-Aug-2026, QUOTED — ⛔ the quote IS the authorisation:** *"minimum broker cash: Rs 2k or
your opinion, but avoid spending time on it — no much of setting x or y amount when other config
settings are master."*

> ## 🔑 **SEVERITY MEASURED *BEFORE* SETTING IT — ⛔ IT DOES NOT BLOCK THE SYSTEM.**
> **`Criticality.CRITICAL` sets how LOUD a failure is, ⛔ not whether anything stops.**
> **`report.py:44-51`'s `is_blocking` rolls up the *REPORT*; ⛔ NOTHING in the boot chain reads the
> preflight sentinel** — `main.py:3637-3641` is the ONLY touchpoint and it **launches a missed phase
> DETACHED, in a try/except, and never reads a result** *(its own comment: "never blocks startup")*;
> **`Criticality`'s docstring says "ALERT-ONLY — never blocks trading".**
> 🔍 **WIDTH for the absence: every `.sh`/`.yaml`/`.service`/`.timer` in the tree — the only preflight
> references are the THREE cron entries that RUN the orchestrator.**
> ⇒ ⭐ **A post-sweep morning is reported LOUDLY and STILL STARTS. The card's worry does not hold.**

⏰ **AND IT COULD NOT HAVE SAVED 10-Aug: phase A is the `08:30` cron — FIFTEEN MINUTES AFTER the 08:15
boot had already hard-killed.** Under the floor today's phase A would have added a **THIRD** FAIL to a
run **already** `CRITICAL_FAILURE` *(`kill_switch_state`, `open_positions_at_start`)* — ⭐ **but it
would have been the FIRST check to name the CAUSE instead of a consequence.** ⛔ **It fixes neither
the invariant defect nor the ceiling, and must not be used to explain or soften either.**

🗂️ **HOME: `config/preflight.yaml`, ⛔ DELIBERATELY NOT in `AppConfig`'s `_CONFIG_FILES`.** Every
AppConfig model is **`extra="forbid"`**, so a key in `system_config.yaml` would need a pydantic field
**the trading app never reads** — and the campaign already DELETED one such set (`live_test_*`) as
misleading dead config. ⭐ **Same precedent as `config/security.yaml`: preflight is a SEPARATE process
and owns its own thresholds.** ⇒ **editing it CANNOT break the boot**, and a missing/unreadable file
**DEGRADES to the in-code default** *(its absence is an ENVIRONMENT condition)*
[[failfast-vs-degrade-discriminator-27jul]].
⚠️ **This does NOT overturn *"no rupee capital value exists in config"*** [[capital-vocabulary]] —
⭐ **it is a preflight STARTUP FLOOR in a file the app does not load, ⛔ not a capital value, ⛔ not a
sizing input, ⛔ not an allocation.**
🧪 **PARITY PINNED, ⛔ not asserted: `ctx.is_paper` returns `SKIPPED` on the FIRST line, before any
broker call ⇒ paper can NEVER reach either predicate.** 📏 **Pre-fix `2F/17P` · post-fix `19P` · all
preflight suites `179P`.** ⭐ **The liveness wording is UNCHANGED — `cash ≤ 0` still says *"no funds
available"*, so "empty" and "small" stay distinguishable (a guard pins it).**

---

## ② `kite_funds_available` — 🔴 **THE STOP AS IT STOOD BEFORE RAMA ANSWERED (retained: it is why the answer was asked for)**

⭐ **⛔ NOT tautological in the strict sense — it CAN go red** (`cash ≤ 0` fails). Its defect is
narrower and exactly as the card names it: **a LIVENESS check on the field, ⛔ not an ADEQUACY check on
the amount.** It saw `net = 209.80 > 0.0` and passed while the account could not cover a `907.02` book.

🔍 **(P) ABSENCE ESTABLISHED WITH ITS WIDTH** *([[feedback-absence-needs-wide-check]])*: every key in
`config/` (recursive) matching `cash|fund|balance|capital|minimum` outside the known sizing
percentages ⇒ **the only hit is the `capital:` header**; every non-test `.py` for
`MIN_CASH|MINIMUM_CASH|CASH_FLOOR_MIN|MIN_CAPITAL|MIN_BALANCE|min_funds` ⇒ **the only hit is
`EXPECTED_MIN_CASH` itself.**

⛔ **AND THE DERIVATIONS DO NOT SURVIVE:** `cash ≥ used + reserved` is **WRONG after Fix 1** *(a carry
makes cash legitimately LOWER than `used` ⇒ a false alarm EVERY morning a position is held — the exact
class Fix 1 removed)* · `cash + carry ≥ used + reserved` is **tautological by construction** ·
*"enough for the smallest tradable position"* is **not derivable** · `fund_manager_balance` already
asks the whole-account version.

> ## 🔴 **THE MISSING DECISION, FOR RAMA: *HOW MUCH BROKER CASH IS TOO LITTLE TO BEGIN A TRADING DAY?***
> **TWO CONTROL *FORMS*, ⛔ not two values of one:** ① an **absolute rupee floor** *(a ₹10k-era figure
> that rots — two absolutes were already retired for this)* ② a **capital-relative floor** *(permanent
> by construction, consistent with `daily_loss_limit_pct` / `max_position_value_pct` /
> `max_concentration_pct`, all deliberately moved to this form)*.
> ⛔⛔ **NO VALUE PROPOSED AND NONE MAY BE INFERRED** — [[feedback-unsourced-promoted-by-repetition-09aug]].
> **The check is UNCHANGED meanwhile.**

---

## ③ 🧪 TESTS — RED-FIRST, AND ONE SELF-CAUGHT REPEAT

**3 RED pre-fix:** the live 10-Aug shape *(`opening 209.80`, legs `446.106 + 460.91632`)* · the 100 %
boundary *(`1000.01` warns, exactly `1000.00` passes)* · the base-naming wording.
**6 GREEN ON BOTH TREES** *(controls)*. 📏 **Pre-fix `3F/14P` · post-fix `17P` · all preflight suites
`175P`.**
📏📏 **FINAL FULL GATE on `ee3ff49`, Git Bash, tree clean: `PYTEST_RC=1` · **9F / 5,566P / 4S** ·
866.48 s.** ✅ **SET-IDENTICAL to the nine ids recorded AT `645728d` — 0 new, 0 disappeared.**
⭐ **Arithmetic DECOMPOSES, ⛔ not merely adds up: `5,557 + 5 + 4 = 5,566`, verified as
`test_preflight_engine.py` 12 → 17 and `test_preflight_broker.py` 15 → 19 test defs.**
*(The interim gate at `13df9cd`, before the ₹2,000 floor, was `9F / 5,562P / 4S` · 871.91 s — also
set-identical. Both recorded; the later one supersedes.)*
⚠️ **SELF-CAUGHT: the "ordinary carried book" guard FIRST also asserted the new wording ⇒ red on the
old tree for a COSMETIC reason ⇒ it had stopped being a two-tree control.** Split into its own
post-fix-only test. ⭐ **The SAME defect found in Fix 1's test file the same day —
[[feedback-carry-the-countermeasure-09aug]] earned again.**

🛠️ **PROVISIONING TRAP, DIAGNOSED ⛔ NOT LABELLED:** a NEW worktree fails `kite_instruments_fresh`
because **`config/instruments.csv` is GITIGNORED (`.gitignore:39`)** — copy it in. ⛔ **Not a
regression, and *"known PC-env"* would have been the wrong answer** [[pc-test-env-hygiene]].

⛔ **NOT TOUCHED:** `max_open_delivery_positions` · the 3-slot ceiling · any new % or ₹ limit · the
book-growth problem (**Fix 3**) · `fund_manager.py` (Fix 1 FROZEN) · the sizing split · F6.
📄 **Record `docs/audit/fix2_preflight_capital_checks_10aug2026.md`.**
