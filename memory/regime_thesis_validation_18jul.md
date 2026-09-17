---
name: regime-thesis-validation-18jul
description: "18-Jul Q10 — BLOCKED on a stale Kite token (Rama must refresh), but the verdict is already determinable: NOT DETERMINABLE at n=23, because the sample ceiling is the TRADE side (21/15/11 days per control cell) not the index side. Backfill cannot fix it; ~2.2 months more data needed for a LARGE effect only."
metadata: 
  node_type: memory
  type: project
  originSessionId: b9e84959-b70c-4ce6-9521-3db6f6dd3fee
---

**📉🔬 Q10 REGIME THESIS VALIDATION — 18-Jul-2026. BLOCKED on the token; VERDICT NONETHELESS.**
Report `docs/audit/regime_thesis_validation_18jul2026.md`. Docs-only, **UNPUSHED**. Nothing changed:
no backfill, no code, no flag, no schema; all DB access `mode=ro`.

**🔴 §2 STOP — NO VALID KITE TOKEN (RAMA ACTION OWED).** VM `data_store/session/zerodha_token.json`
**absent**; session dir mtime `Jul 18 05:00` = the documented 05:00 delete cron; `token_cleanup.done`
18-Jul 05:00; **the 08:15 TOTP refresh does NOT run on a non-trading day** (latest preflight marks are
17-Jul). PC copy dated **21-Jun 12:47** ⇒ ~4 weeks stale (Kite tokens die the next morning).
⇒ `kite.historical_data` unusable ⇒ the backfill could not run. **I deliberately did NOT run
`scripts/auto_refresh_token.py`** — it handles live credentials + the TOTP seed and §2 reserves the
refresh for Rama. No workaround attempted.

**⭐⭐ THE REAL FINDING — I expected the blocker to be the missing index data; IT ISN'T. The sample
ceiling is the TRADE side, not the index side, so the backfill CANNOT rescue the statistics.**
The controlled question needs trading DAYS per bucket; the book has 23 days total:
| cell | trades | **days** | per bucket (3) |
|---|---|---|---|
| LONG/INTRADAY | 108 | **21** | **~7** |
| LONG/POSITIONAL | 33 | **15** | **~5** |
| SHORT/INTRADAY | 14 | **11** | **~3.7 anecdotal** |
**Every cell is single-digit BEFORE the analysis starts** ⇒ **VERDICT: NOT DETERMINABLE at n=23**,
stated with confidence because it does not depend on the missing data.

**⚠️ THE BETA TRAP (why the controls are decisive):** the book is **91% LONG** (141/155) and the bleed
is in **intraday longs** (108 trades, **−25.57R**, 36.1% win). With a 91%-long book, *"Bull mornings did
better"* IS the null — **market beta, not a ranking edge**. Only the WITHIN-cell test (same
strategy+direction: do Bull mornings beat Bear mornings?) separates them — and that is exactly the test
with ~7/~5/~4 days per bucket. **The control that makes the question meaningful is the control that
makes it statistically empty here.**

**📏 POWER (grounded in observed variance, not a rule of thumb).** LONG/INTRADAY daily P&L: 21 days,
mean **−5.42**/day, **σ=13.54**. `n_per_group = 2σ²(1.96+0.84)²/Δ²` (80% power, α=0.05):
**LARGE (1.0σ) → 16 days/bucket = 47 trading days ≈ 2.2 months** · MODERATE (0.5σ) → 63/bucket = 188 days
≈ 9 months · SMALL (0.25σ) → 251/bucket ≈ 36 months. ⇒ **only a LARGE effect is detectable on a
realistic horizon (~2.2 months). If the edge is subtle, this book cannot prove it in any useful
timeframe** — a Rama decision, not a computable one.

**✅ PIPELINE PROVEN ON REAL DATA (so only breadth is missing):** 2026-07-16, NIFTY 256265, 375 1-min
candles (09:15:00→15:29:00); the **09:15–09:59 window = 45 bars**; open 24142.10 → close 24128.10 ⇒
**morning move −0.058%**. Steps (b) terciles + (c) cross-tabs are then mechanical.
**Trades side fully computed already** (no index data needed) and it **independently reproduces BK-1**:
LONG/INTRADAY 108 / −113.8 / 36.1% / −25.57R · LONG/POSITIONAL 33 / +10.4 / +4.50R ·
SHORT/INTRADAY 14 / +28.6 / 64.3% / +3.87R · TOTAL 155 / −74.8.

**📅 The 23 days needing backfill** (authoritative, from the closed book): 15-19 Jun · 22-25 Jun ·
29-30 Jun · 1-3 Jul · 6-10 Jul · 13-16 Jul. (26-Jun absent = no trades; 17-Jul = 0 trades, the S4
outage.) **Coverage today: NIFTY = 1 day only (16-Jul, 375 rows) ⇒ 22 of 23 missing.**
**One command when the token is live** (proven, data-only, idempotent `INSERT OR IGNORE`, `_fetch_indices`
first + fail-safe): `PYTHONPATH=. python3 scripts/fetch_daily_candles.py --backfill --from 2026-06-15
--to 2026-07-16` — fresh `analytics.db` backup first; then verify 23 days landed, 0 stock rows changed,
integrity ok. **The tercile % bands are the ONE deliverable that genuinely needs the backfill** (I have
n=1 observed move and refused to invent bands from it).

**RECOMMENDATION:** (1) refresh the token and **run the backfill anyway** — cheap, proven, it is the
Phase 3 calibration asset, yields the real bands, and **starts the clock** so every future session
accumulates an observation; (2) **do NOT build Phase 1 expecting this test to bless it** — the thesis is
**unvalidated and not validatable on this book for ~2+ months, and only if the effect is large**;
(3) if built anyway, build it explicitly as a **hypothesis under measurement** (shadow-only, logged
daily, verdict deferred) — a legitimate but *conscious* choice.

**⚠️🔴 STANDING WARNING (unchanged, restate every time):** **do NOT flip `regime.enabled`** while the
V3/F1 shadow soak is accumulating — the V3 chain consumes regime via `gate_extreme` + `regime_fraction`
(**8/40 Context**); flipping mid-soak changes the score distribution and makes pre/post shadow rows
**non-comparable**. [[regime-phase1-investigation-18jul]]

**📌 RECORDED FOR THE FUTURE PHASE 1 DESIGN (ChatGPT's recommendation — NOT built):** the opening-regime
calc should be a **configurable PLUG-IN inside the existing `regime/` module** (never parallel):
**configurable opening window** (default 09:15–09:59) · **tunable thresholds** · **pluggable additional
regime algorithms** · **VERSIONED regime logic** so variants can be compared on the same logged history.
**Versioning matters most given the finding above** — if the verdict needs months of data, every logged
row must record WHICH algorithm version produced it.

Related: [[regime-phase1-investigation-18jul]] (the 3 inverted premises + the wiring warning) ·
[[regime-phase0-17jul]] (the ingestion this backfills) · [[bk1-long-short-scanner-17jul]] (the 91%-long
book this reproduces) · [[token-workflow-confirmed-21jun]] (05:00 delete → 08:15 refresh, weekday-only).

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 648 B (budget 450 B). The index now carries a hook and this link.

- 📉🔬🔝 **[Q10 REGIME THESIS — NOT DETERMINABLE 18-Jul](regime_thesis_validation_18jul.md)** — **🔴 RAMA: refresh the Kite token** (VM token absent; 08:15 TOTP doesn't fire on a non-trading day; I did NOT run it — credentials are Rama's) ⇒ backfill blocked, **Part B NOT started**. **⭐ But the ceiling is the TRADE side, not the index side — the backfill CANNOT rescue it:** 21/15/11 days per control cell. **Beta trap:** 91%-long book ⇒ "Bull mornings did better" IS the null. **Power (σ=13.54): LARGE effect ≈ 2.2 months; MODERATE ≈ 9.** Pipeline proven (16-Jul, 45 bars, −0.058%). [[regime-thesis-validation-18jul]]
