---
name: trade-review-may-11
description: May 11 live trading collapse - LONG strategies failing vs SHORT working
metadata: 
  node_type: memory
  type: project
  originSessionId: 9aefa85b-0188-4017-b867-0390152cb3f2
---

## Trade Review Findings: May 11, 2026

**Performance divergence**:
- LONG strategies: 13% win rate (FAILING)
- SHORT strategies: 58% win rate (WORKING)

**Root cause hypothesis**: Scanner quality issue suspected.
- System went LIVE on May 11 with Rs 25K micro capital
- Day 1 saw unexplained double-release issue (since FIXED in commit 4ef614e)
- Performance analysis revealed directional bias

**Why**: Possible causes:
1. Chartink scanner configuration not validated for LONG setups
2. Market regime shift (bearish day) → LONG signals poor quality
3. Entry/exit parameters need direction-specific tuning
4. Scanner "momentum break" may work better for SHORT in current volatility

**How to apply**:
- Before next LONG trade acceptance: audit scanner hit rate vs market direction
- Consider direction-aware min_pass_score threshold (P18 scoring)
- Review May 11 signals in Sheet 1: compare LONG vs SHORT "Algo Score" distribution
- Post-scanner validation: add market-regime filter (bullish/bearish/sideways)
