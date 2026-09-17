---
name: feedback-live-vs-latent-findings
description: "STOP-AND-REPORT is calibrated by REACHABILITY, not by whether the words match the trigger phrase. LIVE (can fire under current production config) => STOP. LATENT (cannot fire today, but the config holds the trigger or one wiring change arms it) => CONTINUE, document prominently, PIN IT WITH A TEST THAT FAILS THE MOMENT IT BECOMES REACHABLE, escalate."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 53e59a7c-edb5-400e-9b3e-6d5981ddd5a2
  modified: 2026-07-18T15:19:22.500Z
---

**⭐ JUDGE A FINDING BY REACHABILITY, NOT BY WHETHER IT MATCHES THE TRIGGER PHRASE.**
Ruling given 18-Jul-2026, after Q9 batch 4 raised it as an open judgement call.

    LIVE finding    = it CAN fire under CURRENT production config
                      -> ⛔ STOP AND REPORT. Highest-severity class on the capital path.
    LATENT finding  = it cannot fire today, but the config already contains the trigger, or
                      ONE wiring change would arm it
                      -> ✅ CONTINUE. Document prominently, **PIN IT WITH A TEST THAT FAILS
                         THE MOMENT IT BECOMES REACHABLE**, and escalate in the report.

**THE REFERENCE EXAMPLE (LATENT):** `capital/position_sizer.py:506`'s
`max(1, min(tiered_qty, raw_qty * 2))` ceiling lets any effective multiplier > 1 produce **2× the
tightest clamp arm** — 20% of capital against a 10% concentration cap, which the 40% position-value
cap cannot catch, while the stored `binding_constraint` still reads `'concentration'`. It matches
§1's *"a cap that can be exceeded"* **word for word**, yet it **cannot fire**: `perf_weight` is
pinned at 1.0 by four independent mechanisms (written only at `signal_processor.py:198` from a
constructor kwarg · **no setter** · `main.py` never passes it · `PerformanceAllocator` never
constructed) and 298/298 production trades confirm it at runtime. **Continuing was correct** —
halting would have left sizing at ZERO wired coverage, the larger risk by far.
[[q9-batch4-sizing-reachability-18jul]]

**Why:** the substance of stop-and-report is *escalation with evidence*, not *stopping*. Batch 4
delivered the substance without stopping — documented in §4.2, pinned by a test that fails if
`PerformanceAllocator(` is ever constructed or `perf_weights=` ever passed, and escalated for D1.
That is the behaviour the rule exists to produce.

**How to apply:**
1. When a finding matches a stop-trigger, **do not stop yet — first ask "can this fire TODAY?"**
   Enumerate the mechanisms that prevent it and verify EACH against current code + config
   ([[feedback-verify-the-finding-premise]]); runtime-confirm against production data where it
   exists. Four independent mechanisms is a strong verdict; one is not.
2. **LIVE ⇒ stop immediately.** Do not keep building on a capital path that can misbehave now.
3. **LATENT ⇒ continue, but you owe three things:** prominent documentation, a **pin** (a test
   that goes red the moment reachability changes — a guard test, not a comment), and escalation.
4. **Say plainly which classification you chose and why**, so the reader can overrule it. A
   judgement call presented as a fact is the thing to avoid.
5. Sibling of [[q9-batch4-sizing-reachability-18jul]]'s **"WIRED IS NOT REACHABLE"** and Q9's
   **"CONFIGURED IS NOT COVERED"** — all three say the same thing: *reachability is the question,
   not the presence of the shape.*

Applied again in batch 5: `rehydrate_from_open_trades()` is **not idempotent within one instance**
(`initialize()` has an H-4 double-call guard; rehydrate has none), which reads like a capital bug —
but it has ONE call site (`main.py:2286`), no retry loop, and a restart is a new process. **LATENT
⇒ documented + pinned by a test asserting the single call site.** [[q9-batch5-post-restart-18jul]]
