---
name: bk1-long-short-scanner-17jul
description: "BK-1 DONE (read-only) — the \"58% short\" premise is INVERTED; the closed book is 91% LONG, loss concentrated in intraday longs. D2 data package. Report bc35a62 UNPUSHED."
metadata: 
  node_type: memory
  type: project
  originSessionId: 26214a92-ac1b-4507-998c-ca000415a4c5
---

# BK-1 — LONG/SHORT + per-scanner analysis — DONE 17-Jul (READ-ONLY, D2 input)

Report `docs/audit/bk1_long_short_scanner_analysis_17jul2026.md`, commit **`bc35a62` UNPUSHED**
(docs-only). sqlite3 `-readonly` on the live DB; nothing changed. Feeds Rama's **D2** + a Web
Claude PROPOSE thesis. **Book = `CLOSED`+`CLOSED_MANUAL`, qty_filled>0 = 155 trades, 15-Jun→16-Jul,
23 trading days.** (`analytics.db` has NO trades table — book is in `trading_system.db`.)

## ⭐ THE PREMISE WAS INVERTED (verify-the-finding again — [[feedback-verify-the-finding-premise]])
The instruction's "the book is heavily short (58% short)" is **FALSE**. The executed closed book is
**91% LONG (141) / 9% SHORT (14)**. No DB population is 58% short (all-status 20%, FAILED 32%, closed
9%). The LONG dominance is a **scanner-mix artifact**: long scanners fire ~4× more (289 vs 72
trade-rows), amplified by **short orders filling at only 19% vs 49% for longs**.

## Direction (the reliable finding is NOT "shorts beat longs")
- **LONG n=141 (reliable):** WR 36.9%, gross −0.075R, **net −0.150R**, cost 0.076R, +1.33/−1.02 win/loss R.
- **SHORT n=14 (⚠️ too small):** WR 64.3%, net **+0.298R** — the 14 shorts PROP the book UP (without them −103R not −75R).
- **Cleaner cut: the loss is INTRADAY LONGs** (−0.239R, n=108). **Positional longs +0.136R (n=33)** and shorts were both net positive. Longs win as big as they lose — the problem is FREQUENCY (69 SL-hits vs 44 TGT-hits).

## Keep/kill DATA (ranked by net-R contribution; small-sample, one regime — NOT a verdict)
Only 3 scanners clear n≥24; 7 of 11 are n<10.
- **Biggest drain (only reliable loser): `vwap_bounce_long` −12.1R, n=35, net −0.346R, highest cost/R 0.112.** KILL/redesign candidate.
- Losers: `gap_fade_long` −5.22R(n8) · `gap_go_long` −5.09R(n13) · `open_low_breakout_long` −4.19R(n28) · `positional_swing_long` −1.66R(n10) · `gap_fade_short` −0.4R(n6).
- Best: `positional_sector_rotation` +4.46R(n19) · `first_pullback_short` +3.73R(n5⚠️) · `positional_momentum_long` +1.7R(n4⚠️) · `first_pullback_long` +1.03R(n24, cost knife-edge) · `vwap_rejection_short` +0.55R(n3⚠️).
- **⭐ NONE is "cost-killed" — every net-negative scanner is negative on GROSS too ⇒ negative-EDGE, not cost. Cost tuning can't save them.** The ONLY cost-marginal one is `first_pullback_long` (gross +0.10 → net +0.045). This nuances the book-wide "costs dominate" story: at book level costs turn ~breakeven gross into a net loss, but the WORST scanners are bad on gross alone.

## What the data CANNOT answer
- **Regime confound UNRESOLVED — the DB has NO index/NIFTY candles** (token 256265 = 0 rows in analytics.db). Weekly long net-R was +4.8/−6.4/+3.8/−13.8/−9.5 (worst in July W27-W28), *consistent* with a July long-headwind, but unconfirmable. Counter-evidence it's not PURELY regime: winning & losing long scanners **overlap in time** (positional_sector_rotation + vwap_bounce_long both ran 06-17→mid-Jul) ⇒ scanner-quality is real.
- SHORTs (n=14) + 7/11 scanners (n<10) too small for any per-cell verdict. One regime, 23 days, no forward confirmation.
- **NET understated on 36 CLOSED_MANUAL trades** (charges=0, the RMS costs=0.0 path [[capital-operational-note]]) — cost-imputed variant shown in the report; the direction gap survives it.

## For D2 / next
Data-supported (n≥24): `vwap_bounce_long` KILL/redesign · `open_low_breakout_long`/`gap_go_long` KILL/redesign candidates · `first_pullback_long` WATCH/tune (cost-marginal). Everything else n-too-small. **This UNBLOCKS part of D2** (the long/short + keep/kill empirical sub-questions) and feeds **M-S4** (dead scorer, gated on D2). Rama decides the keep/kill list; Web Claude may draft a PROPOSE thesis from this.

Related: [[feedback-verify-the-finding-premise]] · [[capital-operational-note]] · [[e4-w10-done-17jul]] (the pnl_delta=NET fix — relevant to how net is measured)
