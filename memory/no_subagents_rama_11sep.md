---
name: no-subagents-rama-11sep
description: "RESCINDED 11-Sep-2026 (same day) -- Rama's 15:10 no-subagents rule was based on a misreading (he thought the findings were lost); subagents are fine again. Kept as a record of the real failure mode to watch for."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6e6242ba-8eb1-4017-b077-360f22940d0a
  modified: 2026-09-11T12:34:04.201Z
---

⚠️ **RESCINDED, same day.** Rama's 15:10 instruction (below) was written believing the four research agents' findings had been lost/gone; they had not -- the findings files were safe on disk the whole time, and only the fifth (drafting) agent's output was cut off. Once he re-read the text and saw that, he withdrew the rule: *"So please forgive me and ignore my instruction to not to use agents hereafter"* (11-Sep, same day). ⛔ Do NOT treat "no subagents" as a standing rule any more.

**What actually happened, for future reference (this part still holds):** subagents cannot save/write report files -- a drafting agent given that job will return truncated text instead of a saved artifact. Never hand final-document assembly to a subagent; assemble/write the deliverable yourself even when research was parallelized. Parallel research agents themselves were not the problem.

**Original 15:10 text, kept for context:** *"Then why the hell he's initiating 4 agents at a time, So much api burned non-sensely, Next time tell him to not use any agents, instead he himself let work on it, No worries about time consumption for me, Fuck around >6L-7L tokens burned already uselessly shit"* -- prompted by 4 research agents (397,862 + 440,259 + 302,368 + 408,058 tokens) plus a 5th drafting agent (234,784 tokens, 29m50s) that could not write its report file and returned truncated text. ~1.78M tokens total for that pass.

**How to apply now:** subagents are usable again for research/parallelism as normal. The one durable lesson: don't delegate final report/file assembly to a subagent -- do that step yourself.
