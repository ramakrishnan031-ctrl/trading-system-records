---
name: paper_mode_requires_webhook_secret_06sep
description: "Paper mode requires WEBHOOK_SECRET despite a test asserting it must not — recorded for batch 2, not fixed"
metadata: 
  node_type: memory
  type: project
  originSessionId: c47eb4bf-3dba-4631-885e-af1d917d4a27
  modified: 2026-09-06T09:58:11.034Z
---

🔬 **PAPER MODE CURRENTLY REQUIRES `WEBHOOK_SECRET`, AND A TEST SAYS IT MUST NOT.**
`tests/unit/test_main.py::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret`
fails with `assert 'WEBHOOK_SECRET' not in ['ZERODHA_API_KEY_LFL836',
'ZERODHA_API_SECRET_LFL836', 'TELEGRAM_BOT_TOKEN', 'WEBHOOK_SECRET']`.
🔬 Measured 06-Sep-2026 on the sandbox at SHA `20061b6`, Python 3.12.3, TZ IST.

**Why:** ⭐ The test's *name* states the design intent and the code violates it — so
this is a real defect, ⛔ not an environment artefact. ⭐ Classified
environment-independent: the assertion compares a list of required env-var names
and never touches the filesystem, network or clock, so it fails identically
anywhere at this SHA.

**How to apply:** ⛔ **RECORD, DO NOT FIX — batch 2, pre-build review gate**
(👤 Rama, 06-Sep). ⭐ It is the **third** independent blocker on ever booting the
sandbox, alongside the weekend guard (`holiday_guard.py:92` returns before reading
any holiday file when `weekday() >= 5`) and the absent
`data_store/session/zerodha_token.json` that paper's quote_provider reads.
⭐ Of the three, this one is solvable **without DR6114**: a throwaway
`WEBHOOK_SECRET` is ⛔ not a credential — ⭐ it is a random string for the sandbox's
own loopback receiver on `127.0.0.1:5010`. ⛔ The token file is not solvable that
way. See [[sandbox_replica_built_06sep]].
