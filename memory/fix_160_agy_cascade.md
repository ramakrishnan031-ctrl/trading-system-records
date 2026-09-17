---
name: fix-160-agy-cascade
description: "FIX-160 deployed 10-Jun-2026 — AGY model cascade with tier-based model assignment, quota fallback, GEMINI_BIN path resolution"
metadata: 
  node_type: memory
  type: project
  originSessionId: 07bf868a-1840-48e8-8b38-78ff37db426e
---

FIX-160: AGY model cascade deployed 10-Jun-2026.

- Tier 1 (deep analysis — trade coach, CEO, auditor, weekly, integrity): Claude Sonnet 4.6 → Gemini Pro High → Gemini Pro Low
- Tier 2 (routine — watchman, log review, cron): Gemini Flash Low → Medium → High → Pro Low
- Premarket brief: custom cascade starting at Flash Medium
- Forbidden: Opus, GPT-OSS never used in AGY scripts
- Default agy model (settings.json): Gemini 3.5 Flash (Low)
- GEMINI_BIN=/home/ubuntu/tools/antigravity/agy set in VM .env
- All 6 gemini scripts use shared `scripts/agy_runner.py` — no more direct subprocess calls
- FIX-160b: `--dangerously-skip-permissions` flag added (default on) to prevent interactive prompts blocking cron/systemd
- 26 tests pass; 2851 full suite pass

**Why:** Claude Opus was default model burning entire shared Claude+GPT pool on every AGY call. Routine tasks don't need Opus quality.

**How to apply:** When adding new AGY scripts, import from `scripts.agy_runner` and use appropriate tier. Never call agy subprocess directly. See [[feedback-paper-live-parity]] for deployment checklist.
