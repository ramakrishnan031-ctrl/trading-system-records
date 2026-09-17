# FROZEN PREDICTION — FIX ITEM 1 · MIS/GTT CONFIG INDEPENDENCE + KILL THE SILENT FALLBACK

**Written:** 22-Aug-2026 (Saturday), IST — **BEFORE any line of the build was written.**
**Card:** VS CODE CLAUDE BUILD CARD, FIX ITEM 1, issued 05:00 IST 22-Aug-2026.
**Governed by:** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
**Base, MEASURED at freeze time, not recalled:**
`git ls-remote origin refs/heads/main` -> `45683859a0a05f466189ac5bc98f9a9f089f98d3`.
**Build worktree:** `scratchpad/item1-work`, branch `fix/delivery-config-independence-22aug`, off `4568385`.
**Gate base worktree:** `scratchpad/item1-base`, detached at `4568385`.

**Status of the unit at freeze time:** `NOT BUILT · NOT GATED · NOT PUSHED · NOT DEPLOYED · NOT VERIFIED LIVE`.

---

## 0 · WHAT THIS UNIT IS PREDICTED TO DO

Five delivery-scoped risk keys become **explicit and required**; the positional
(delivery) sizing/gating path stops inheriting the intraday (global) value when its
own key is absent. Every new value is set to **today's effective value**, so the
prediction is that **no measured quantity moves**.

| key | today's EFFECTIVE value (inherited) | value written by this build |
|---|---|---|
| `position_sizing.delivery_risk_per_trade_pct` | 0.01 (from `risk_per_trade_pct`) | 0.01 |
| `position_sizing.delivery_max_position_value_pct` | 0.40 (from `max_position_value_pct`) | 0.40 |
| `position_sizing.delivery_max_concentration_pct` | 0.10 (from `max_concentration_pct`) | 0.10 |
| `risk.delivery_max_sector_exposure_pct` | 0.40 (from `max_sector_exposure_pct`) | 0.40 |
| `risk.delivery_daily_loss_limit_pct` | 0.03 (from `daily_loss_limit_pct`) | 0.03 |

---

## 1 · PREDICTIONS WITH EXPLICIT FALSIFIERS

### P-1 — BEHAVIOUR NEUTRALITY (the acceptance test, B-3)

**Predicted:** every sizing quantity computed for a DELIVERY (positional) entry is
**bit-identical** before and after, because each new key equals the value that was
being inherited. The three recorded CNC risk legs reproduce exactly:
`CLSEL 105.87/5.78 -> 18` · `MANINDS 105.87/14.46 -> 7` · `KRONOX 105.87/4.11 -> 25`.

**FALSIFIER:** any one of `qty_by_risk`, `qty_by_concentration`, `qty_by_capital`,
`raw_qty`, `tiered_qty`, `final_qty`, `margin_required`, `risk_amount`, `constraint`
differing between base and unit on the same inputs. **A single differing integer
falsifies the build, not the test.**

### P-2 — INTRADAY UNTOUCHED (T-6)

**Predicted:** the MIS/INTRADAY path is byte-identical. `bucket == "intraday"` never
reads any `delivery_*` key. 231 of 266 entries are MIS LONG; none may move.

**FALSIFIER:** any intraday sizing quantity changing, OR any `delivery_*` symbol
appearing on a code path reachable with `bucket == "intraday"`.

### P-3 — THE FALLBACK IS GONE (B-4, T-3, T-4)

**Predicted:** there is **no expression anywhere** that substitutes a global value for
an absent/NULL delivery value. A missing key and a NULL key each **reject at startup**,
naming the key, via main.py's existing `_config_error_detail` -> `_log.critical("Config
load failed: ...")` -> `return 5`.

**FALSIFIER:** (a) a grep finding any surviving `delivery_X if ... is not None else
global_X` shape; (b) a config with the key removed booting; (c) a config with the key
`null` booting; (d) the boot log not naming the offending key; (e) the failure arriving
as a WARNING rather than a non-zero exit.

### P-4 — INDEPENDENCE, BOTH DIRECTIONS (T-2)

**Predicted:** changing a global (MIS) key moves **no** delivery limit, and changing a
delivery key moves **no** intraday limit. Asserted in both directions.

**FALSIFIER:** either direction leaking. **Named exclusion, stated in advance so its
absence is not read as a pass:** `capital/fund_manager.py`'s post-close daily-loss
circuit breaker stays GLOBAL by design (one account-wide realized P&L exists; there is
no per-book P&L attribution to split it with). The delivery daily-loss key scopes the
**pre-trade gate only**. If this build is later read as having made daily loss fully
book-independent, that reading is wrong.

### P-5 — THE STALE COMMENT IS GONE (B-5)

**Predicted:** the assertion that the delivery path "is never taken live" / "these are
never read" survives in **zero** places. It exists in three at `4568385`:
`core/config_loader.py:318-322`, `capital/position_sizer.py:296-299` (and ctor note
`:143-146`), `config/system_config.yaml:185-189`.

**FALSIFIER:** any surviving text claiming delivery is never live, never read, or INERT.

### P-6 — THE :596/:609 REPORTING TRAP FIRES THE MOMENT THIS BUILD LANDS

**Predicted, and it is a defect this build CREATES if left alone:**
`position_sizer.py:585` enforces `eff_max_position_value_pct` while `:596` and `:609`
report `self._max_position_value_pct` (the GLOBAL). Today they are equal, which is why
nothing is visibly broken. **Populating the delivery key is exactly the event that
separates them.** This build must make both report the ENFORCED value.

**FALSIFIER:** a delivery rejection whose CRITICAL log or reason string states a
percentage that was not the one enforced.

### P-7 — §5's OPERATIONAL RISK — A VALID CONFIG MUST NEVER TRIP THE NEW REJECTION

**This is the named falsifier the card demands.** After this ships, the boot path can
**refuse to start** on a config mistake. **Monday's 08:15 boot is UNATTENDED.** A false
rejection = no boot, no entries, a lost trading day — the same cost as the 10-Aug
HARD_KILL day.

**Predicted:** the shipped `config/system_config.yaml` loads cleanly, every time, and
the rejection path is reachable ONLY by removing or nulling a key.

**FALSIFIER (any one):** `load_all(Path("config"))` raising on the shipped config; the
full test suite showing a new config-load failure; a valid-but-differently-ordered or
differently-commented config being rejected; the rejection firing on a key that IS
present and IS a number.

**REVERT TRIGGER, stated in advance:** if a VALID config is ever rejected, the unit is
REVERTED — not tuned, not loosened, not exception-scoped.

### P-8 — GATE SET-EQUALITY, NOT COUNT-EQUALITY

**Predicted:** `pytest tests/unit tests/integration` run from **Git Bash** on both trees
in the same environment, same day, sequentially (never concurrently — `test_instance_lock`
holds a machine-global lock), yields **0 NEW failures and 0 disappeared failures** by
`comm` in BOTH directions, and identical failure MESSAGES for common failures.

**FALSIFIER:** any failure id present on one side and not the other that is not
explained by an experiment, not by a label.

---

## 2 · WHAT THIS PREDICTION DOES **NOT** CLAIM

- **A paper-mode pass is NOT evidence here, and this is said in advance.** Paper nets
  by SYMBOL; live Kite nets per `(SYMBOL, PRODUCT)`. A paper drill of a delivery
  product-semantics change is vacuously green. No paper result will be offered as proof.
- No claim about the VM's on-disk tree. The base is proven by `git ls-remote`
  measurement only; the deployed working tree was NOT read (service down, Saturday,
  no VM op owed).
- No claim that `delivery_max_position_value_pct` can ever bind. It is measured
  UNREACHABLE (cap 40% of TOTAL vs a positional bucket of 30% of TOTAL; concentration
  binds at 10% first). It is populated to satisfy the no-fallback rule and is recorded
  as inert. **The choice among the three §4 options is RAMA's and is NOT taken here.**
- No claim about `VERIFIED LIVE`. Nothing is pushed. Nothing is deployed. The first
  execution of any of this would be a future 08:15 boot that has not been authorised.

---

## 3 · SCORING RULE

Each of P-1 .. P-8 is scored **CONFIRMED / REFUTED / NOT TESTED** separately.
They are never collapsed into one green. A falsifier whose window has not arrived is
`NOT TESTED`, never a pass.
