---
name: ct-day6-retests
description: "Day 6 retest results (11-Jun-2026): CT032 PASS, CT083 PASS, CT084 PASS, CT085 PASS_WITH_RISK"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8b860701-6391-4408-be2a-86ea2bdeaf60
---

## Day 6 Retests (2026-06-11)

| CT | Title | Result | Evidence |
|---|---|---|---|
| CT032 | Signal while position open | PASS | UNICHEMLAB SHORT → REJECTED_CONTRARY_POSITION; SBIN re-entry → REJECTED_SHADOW_INNING_ACTIVE |
| CT083 | Max open positions | PASS | Set max_open_positions=2, 3 signals REJECTED_OPEN_POSITIONS (including natural signal). Historically: 8756 rejections |
| CT084 | Max daily trades | PASS | Set max_daily_trades=20, 52 trades today → REJECTED_DAILY_TRADES immediately. Historically: 2086 rejections |
| CT085 | Max consecutive losses | PASS_WITH_RISK | Not directly retested today (need to engineer 4 consecutive losses). Historically: 16 firings, last on 10-Jun-2026 |

**Paper mode challenges:** Signal injection at non-LTP prices causes immediate SL_HIT (SL calculated from trigger price, entry fills at LTP). Future CT083 testing should use natural signals or exact-LTP injection.

Related: [[ct-day6-blockers-reset]]
