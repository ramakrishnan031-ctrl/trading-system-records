---
name: post_rotation_creds_02jul
description: "02-Jul credential rotation sync — VM+PC .env updated from credentials.xlsx, Phase-1 token-gen PASS, GO for security-batch deploy (no values)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 567e201a-8ff2-4882-b687-0f55318fab0f
---

Post-rotation credential sync (02-Jul-2026, off-market ~18:50 IST). NO credential values recorded here.

**What rotated (6 of the 8 synced values changed):** `ZERODHA_API_SECRET_LFL836`, `ZERODHA_TOTP_LFL836`, `ZERODHA_API_SECRET_DR6114`, `ZERODHA_TOTP_DR6114`, `TELEGRAM_BOT_TOKEN`, `WEBHOOK_SECRET`. **Did NOT change:** both `ZERODHA_API_KEY_*` (Zerodha keeps the app key), the Kite `ZERODHA_PASSWORD`, `ZERODHA_USER_ID` (=LFL836) — verified identical by hash, so no password sync was needed.

**Synced BOTH sides** from `credentials.xlsx` (Sheet1: only LFL836 + DR6114 rows present; other 3 accounts D351962/ZA004/ZA005 are disabled placeholders): PC `.env` (20 vars) + VM `/home/ubuntu/systems/trading-system/.env` (24 vars — extras: `GEMINI_BIN`, `ALERT_SMTP_PASSWORD`, `ZERODHA_USER_ID`, `ZERODHA_PASSWORD`). Line-preserving replace, all other vars byte-identical, PC↔VM 8 values SHA-parity confirmed. VM backup left at `.env.pre-rotation-02jul.bak` (0600, dead old creds — remove after deploy is stable). Patch transferred over SSH stdin only (never on VM disk).

**xlsx handling:** `credentials.xlsx` added to `.gitignore` (C-1 scanner doesn't scan .xlsx → gitignore+deletion are the controls); confirmed never committed / not in history. As of this run it is STILL PRESENT on the PC — **Rama must delete it** (it also holds the Kite password, which is not in `.env`). `.gitignore` change is uncommitted (PC working tree) — commit it eventually for permanent protection.

**Scrub result:** none of the 6 rotated secrets leak anywhere in the tree. Pre-existing finding (NOT caused by rotation, low sev): the live LFL836 **api_key** (unchanged) is hardcoded at `scripts/fetch_daily_candles.py:30`, `scripts/gemini_data_integrity_check.py:45`, `scripts/reconstruct_excursions.py` (+3 `docs/web_claude/*.txt`). api_key alone can't auth without the secret (which is NOT hardcoded). Recommend moving to `os.environ` later; not deploy-blocking. Placeholder collisions in `.env.example`/`test_secret_scan.py`/audit doc are benign.

**Data-entry flag:** LFL836 and DR6114 have an IDENTICAL TOTP seed in the sheet (same hash). Moot for the gate (DR6114 disabled), but if DR6114 is ever enabled its TOTP will likely fail — verify the seed was not copy-pasted.

**Phase-1 gate = PASS** → satisfies the deploy runbook's Phase 1. Token-gen (`scripts/auto_refresh_token.py --token-path <temp>`) exit 0 on live LFL836 (validated new api_secret via exchange + new TOTP via 2FA + password/user_id via login); ran against a TEMP path + it was 18:5x (outside token-watcher's 08:00–16:00 window) so the live trader was NOT started; canonical token untouched; temp token shredded. New bot token valid (`getMe` ok, `@Trade_sysbot`). `WEBHOOK_SECRET` present len 64 (C-2 both modes).

**DEPLOY EXECUTED & VERIFIED** (Rama chose "Opus executes now", off-market ~19:10 IST). Fast-forward `git push origin HEAD:main` `59f83b5..9becf8c` (the 5-commit stack `7bc3367·d922007·99bd4c4·340109d·9becf8c`; C-1 secret scanner + C-2 webhook lockdown + A-1/E-1 naked-orphan recovery). Post-receive checked out main + AUTO-INSTALLED crontab (regen==canonical). Verified: bare HEAD==worktree HEAD==9becf8c, no tracked-file drift, crontab==canonical AND zero-drops vs pre-deploy, 16 changed .py py_compile clean, trading-system left INACTIVE + token-watcher active. DB+crontab backed up at `/home/ubuntu/backups/pre_deploy_02jul_securitybatch/`. Local main ff'd to 9becf8c. **NOT started tonight** — new code (incl. A-1/E-1 first live boot) takes effect at tomorrow 03-Jul 08:15 headless boot, which also auto-clears today's prior-day SOFT_KILL (`circuit_breaker_force_close_15:15`). Pending: Rama deletes credentials.xlsx; commit the .gitignore hardening; remove VM `.env.pre-rotation-02jul.bak` once stable. See [[a1_e1_orphan_fix_impl_02jul]], [[c2_webhook_lockdown_02jul]], [[c1_secret_remediation_02jul]].
