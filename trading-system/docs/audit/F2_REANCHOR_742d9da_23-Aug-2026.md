# F2 — RE-ANCHOR AT `742d9da` · 23-Aug-2026

**Governed by** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`). Applies **M3**: *line numbers
hold ONLY at their measured SHA.*

`F2_SEGMENT_CAPITAL_INVENTORY_22-Aug-2026.md` measured **22 unique `file:line`
references** at **`4568385`**. `origin/main` is now **`742d9da`**.
⛔ **No number below is carried — every one was re-measured or proven by byte-identity.**

---

## A · 13 REFERENCES HOLD — ⭐ PROVEN, ⛔ NOT ASSUMED

Their files are **byte-identical** between `4568385` and `742d9da` (md5 compared), so the
line numbers cannot have moved. ⭐ This is a re-measurement, not an assumption.

| file | refs that hold |
|---|---|
| `capital/fund_manager.py` | `337-338` · `445-477` · `521` · `1347` · `1411` · `2311-2335` · `2391` |
| `orders/order_reconciler.py` | `3683-3702` |
| `ops_dashboard/backend/api/risk_capital.py` | `32` |
| `ops_dashboard/backend/services/operations.py` | `60-61` |
| `reports/daily_trade_review.py` | `1237-1240` |
| `scripts/system_manager.py` | `262` · `295` |

## B · 7 REFERENCES MOVED — line shift only, anchor text unchanged

Re-measured by locating each old anchor line's **exact text** in the new tree.

| reference | `4568385` | **`742d9da`** | Δ | anchor |
|---|---|---|---|---|
| `position_sizer.py` | 316 | **373** | +57 | `margin_pct = self._broker_adapter.get_live_margin_pc…` |
| `position_sizer.py` | 381 | **438** | +57 | `risk_rs = total_capital * eff_risk_pct` |
| `position_sizer.py` | 418 | **475** | +57 | `margin_per_share = effective_entry_price / leverage` |
| `position_sizer.py` | 419-421 | **476-…** | +57 | `qty_by_capital = (` |
| `position_sizer.py` | 423-425 | **480-…** | +57 | `qty_by_concentration = int(math.floor(` |
| `position_sizer.py` | 585 | **649** | +64 | `max_position_value = eff_max_position_value_pct * to…` |
| `state_store.py` | 856-877 | **860-…** | +4 | `def sector_exposure(` |

## C · 🔴 2 REFERENCES DID **NOT** MERELY MOVE — THEIR OPERAND CHANGED

⭐ These read as **GONE** on an exact-text match, and that is the finding: F1 rewrote them.

| | `4568385` | **`742d9da`** |
|---|---|---|
| daily loss | `:593` `limit = **self._daily_loss_pct** * snap.total` | `:672` `limit = **eff_daily_loss_pct** * snap.total` |
| sector cap | `:638` `if projected > **self._max_sector_pct** * snap.total:` | `:717` `if projected > **eff_max_sector_pct** * snap.total:` |
| (telemetry twins) | `:652` · `:661` | `:731` · `:740` |

**What changed and why it matters to F2** — `risk_engine.py:322-328` @ `742d9da`:

```python
if <delivery>:
    eff_daily_loss_pct  = self._require_delivery(self._delivery_daily_loss_pct,  "delivery_daily_loss_limit_pct")
    eff_max_sector_pct  = self._require_delivery(self._delivery_max_sector_pct,  "delivery_max_sector_exposure_pct")
else:
    eff_daily_loss_pct  = self._daily_loss_pct
    eff_max_sector_pct  = self._max_sector_pct
```

⇒ 🔴 **F2's inventory described ONE percentage per limit. There are now TWO — book-scoped —
resolved through an `eff_*` indirection F1 introduced.** ⛔ Any F2 edit that rewrites *"the
line that multiplies the pct by `snap.total`"* would now silently cover **both books**, or
**miss one**, depending on where it lands.

⭐ **BUT F2'S CORE FINDING SURVIVES INTACT, and this is the important half:** the
**multiplicand is still `snap.total` — real cash — in both branches.** F1 scoped the
*percentage* per book; it did **not** move either limit onto segment capital. ⇒ **F2's
premise stands; only its surface has doubled.**

---

## ⚠️ WHAT THIS RE-ANCHOR DOES **NOT** COVER

⛔ It re-anchors **line references only**. It does ⛔ **not** re-verify F2's *rupee figures*
(`₹1,058.70` / `₹3,705.45` / `₹317.61` / `R = ₹10,587.00`) — those derive from live capital
on a measured day and expire on their own schedule, ⛔ not on a SHA.
⛔ It does not re-run F2's `segment_capital(bucket)` reasoning.
⭐ Anyone using a rupee figure from that inventory must re-derive it, ⛔ not carry it.
