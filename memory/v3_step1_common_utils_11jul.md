---
name: v3_step1_common_utils_11jul
description: "V3 Step 1 — two NEW pure helpers (ATR + timeframe-resample) built in core/candle_math.py; unit-tested, NOT wired, BUILT-but-UNPUSHED"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c01370e-a523-42ed-bcb4-b17cc03d4987
---

**V3 Shared-Engine — Step 1 Common Utilities (11-Jul-2026). BUILT + UNIT-TESTED, NOT wired, BUILT-but-UNPUSHED (Rama pushes off-market).** Follows Phase-0 [[v3_phase0_investigation_11jul]]. Delivered the two genuinely-NEW pure helpers the gap analysis flagged; the rest of "Common Utilities" is existing pure helpers REUSED as-is (no move/rewrite — churn-free).

**New file `core/candle_math.py`** (domain-agnostic, layer-1, pure, mode-agnostic):
- `true_range_series(candles) -> list[float]`: TR_t = max(H-L, |H-prevC|, |L-prevC|); first candle TR = H-L (degenerate, EXCLUDED from atr).
- `atr(candles, period, method="wilder"|"sma") -> float|None`: Wilder smoothing (default; seed=SMA of first `period` real TRs then `(atr*(p-1)+TR)/p`) or SMA of last `period` real TRs. Requires `period+1` candles → fewer returns **None** (never fabricated). `period` is a PARAMETER (no baked default). Raises ValueError on period<=0 / bad method. Fills the Phase-0 gap (ATR was only consumed pre-computed; ATR-SL/TGT unimplemented→FIXED_PCT fallback).
- `resample(base_candles, target_tf, session_bounds) -> ResampleResult`: base→higher TF (int minutes | "day"/"daily"). O=first/H=max/L=min/C=last/V=sum, ts=bucket START; buckets anchored to each date's **session open via INJECTED `session_bounds`** (tuple or date->(open,close) callable; NEVER hardcodes 09:15; no cross-day merge; pre-open/after-hours excluded). `ResampleResult(bars, partial_bucket_starts, empty_bucket_starts)` + `.partial_last` property — empty buckets flagged not fabricated; session-tail partial bar (e.g. NSE 375min→15min tail on 30m grid) emitted from data present + flagged, never padded.

**Placement/anti-dup decision (R2/R3):** `core/candle_math.py` chosen (NOT `orders/price_math.py`=order math, NOT `sr_detector/`=S&R-specific). REUSES the ONE shared `Candle` type (`sr_detector/models.py`) — no parallel candle type. Key subtlety: `sr_detector/__init__.py` eagerly imports detector+fetch (which import core), so a module-level `from sr_detector.models import Candle` in core would be a layer inversion + heavy-init trigger. SOLVED: `atr`/`true_range_series` need no project import (duck-type on `.high/.low/.close`); only `resample` constructs Candle, via a **function-local** `from sr_detector.models import Candle` — the exact `# local import avoids cycle` pattern already in `core/market_windows.py:283`. **Verified: importing `core.candle_math` does NOT load `sr_detector` (sys.modules check); sr_detector loads only when resample() runs.**

**Verification:** `tests/unit/test_candle_math.py` 26 tests ALL PASS (hand-computed TR=[2,2,2,4,2], Wilder atr=22/9, SMA atr=8/3, insufficient→None, determinism, invalid-param raises; resample OHLCV/alignment/partial/empty/no-cross-day/pre-post-hours/daily/tz-preserve/MarketWindows-bounds/shared-Candle-type). sr_detector regression 64 pass. Main `tests/` collects 4448 clean (the `pyotp` collect error is PRE-EXISTING, ops_dashboard's isolated venv only — unrelated). **git: only `core/candle_math.py` + test NEW; ZERO existing code files modified → nothing wired, no live behaviour change, paper==live by construction.**

**Ledger:** BUILT-but-UNPUSHED on `main` working tree (no branch created yet; Rama pushes off-market). Docs updated: `docs/SYSTEM_MAP.md` (V3 Common Utilities substrate catalog), PATHS.md, this memory, UNPUSHED_PENDING_DEPLOY_LEDGER. **NEXT = Step 2 (03.01 S&R Detection) after Web Claude + ChatGPT review.**
