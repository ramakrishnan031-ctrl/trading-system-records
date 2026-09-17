---
name: tick4-blocked-on-sizing-deploy-09aug
description: VERIFIED - Tick 4 cannot run until the sizing build is deployed. On main, risk_per_trade_pct is a LIVE sizing input and no allocation-model symbol exists, so there is nothing to repoint the checks to.
metadata:
  node_type: memory
  type: project
---

# 🔴⏸️ **TICK 4 — `DECIDED · BLOCKED ON THE SIZING BUILD BEING DEPLOYED`**

⛔ **⛔ NOT "decided, not built"** — that reads as *available*, and it is not. **It is blocked by a DEPLOY that has not happened, ⛔ not by a decision: Rama already decided it.**

## ✅ VERIFIED, ⛔ NOT INHERITED — and the evidence is stronger than the hypothesis
Tick 4 = *"repoint the three morning checks to the AUTHORITATIVE SIZING MODEL, prove them, then retire `risk_per_trade_pct`."* **(P) on `main`:**
- 🔴 **`risk_per_trade_pct` is a LIVE SIZING INPUT**, not inert: `risk_per_trade_rs = total_capital * risk_per_trade_pct` → `qty_by_risk = floor(risk_per_trade_rs / sl_distance)`, and `qty_by_risk` is one of the three candidates in `min(qty_by_risk, qty_by_capital, qty_by_concentration)`. A `"RISK"` `binding_constraint` value exists.
- **C3/C4/C5 read it** (`rpt = ps.risk_per_trade_pct`).
- ⭐⭐ **ZERO allocation-model symbols exist on `main`** — `grep -cE 'planning_basis|capital_per_trade_allocation|max_daily_trades'` over `main`'s `position_sizer.py` returns **0**.

⇒ **On `main` there is literally NOTHING to repoint the checks TO, and retiring the key would BREAK SIZING.**

## ⭐ THE SHARPER FRAMING
**On `main`, C3/C4/C5 are not stale at all — they correctly describe live behaviour.** The premise *"the three checks are wrong"* is a property of the **UNDEPLOYED** tree only. ⇒ **Tick 4's problem statement does not yet hold in production**, which is a stronger statement than "blocked on a deploy" and explains why neither base works:
- **off `main`** ⇒ ⛔ repoints live checks to a model production does not run;
- **off the sizing branch** ⇒ ⛔ entangles it with schema v46 and it can never deploy separately.

## 📌 WHAT UNBLOCKS IT
**The sizing build going live.** ⛔ Nothing else — no decision, no card, no measurement. ⭐ The moment it is deployed, Tick 4 becomes an ordinary build off the then-current `main`.
⚠️ **And `N9-01`'s ordering still governs when it does run: rebase the checks FIRST, prove the replacement, retire the key LAST** — so C5's real ₹525 finding is never left unwatched by a retirement.

See also [[c5-c5b-risk-pct-card03-09aug]] · [[tick1-threshold-base-mixup-09aug]] · [[two-pipeline-split-08aug]]
