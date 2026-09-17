---
name: sandbox_replica_built_06sep
description: "The trading-system sandbox replica — address, access, what is verified, and what remains unproven"
metadata: 
  node_type: memory
  type: project
  originSessionId: c47eb4bf-3dba-4631-885e-af1d917d4a27
  modified: 2026-09-06T11:08:21.775Z
---

🟢🗿 **SANDBOX REPLICA BUILT AND VERIFIED 06-Sep-2026.** ⭐ `trading-system-sandbox`
· 🔬 `161.118.168.162` · ⭐ `ssh trading-sbx` (key `C:/Users/rama/.ssh/trading-system-sandbox.key`)
· ⭐ Ubuntu 24.04.4 aarch64 · ⭐ Python 3.12.3 · ⭐ SQLite 3.45.1 · ⭐ systemd 255 ·
⭐ 2 OCPU/12 GB · ⭐ 60 GB boot · ⭐ TZ `Asia/Kolkata`.

🔴 **IT IS A SEPARATE ORACLE TENANCY, ⛔ not just a separate VCN** — 🔬 sandbox
`ocid1.tenancy…s7tzjfo6oamofu2xynjf5xs4gadbj35dx7wzjdth2mo5w5jj6oia`, production
`…vmabgwcuwp4lodzkjp6atwj6fdgbckwo4njafrr4x2okspttkhta`. ⭐ The sandbox tenancy
holds **one** instance and **one** boot volume; ⭐ 60 GB of the 200 GB Always Free.

**Why:** ⭐ 👤 Rama wanted a pure duplicate of production at SHA `20061b6` to test
against without touching the live book. ⭐ Deliberate exclusions: ⛔ no `.gemini`,
⛔ no `.claude` (⭐ plaintext creds for 5 accounts — see
[[gemini_dir_holds_every_live_credential_06sep]]), ⛔ no Tailscale (⭐ production's
`iptables` rule 1 accepts everything on `tailscale0`), ⛔ no installed cron,
⛔ no live `.env`.

**How to apply:**
⭐ · 🔬 **VERIFIED:** code at `20061b6` · 10 requirements pins exact · webhook
  `127.0.0.1:5010` (⭐ parsed, ⛔ not grepped) · 7 systemd units installed, ⭐ all
  disabled · ⭐ 15 GB data copied, ⭐ **both DBs byte-identical to production** ·
  ⭐ gate **18F/6051P** · ⭐ snapshot **and restore both proven** (⭐ restored volume
  mounted, ⭐ `trading_system.db` md5 matched live) · ⭐ backup
  `sbx-restore-drill-06sep2026` retained.
⭐ · ⛔ **UNPROVEN: `main.py` has never executed there.** ⭐ Three independent
  blockers: 🔬 `holiday_guard.py:92` returns before reading any file when
  `weekday() >= 5` (⛔ unbypassable on a weekend) · ⛔ no
  `data_store/session/zerodha_token.json` (⭐ paper's quote_provider reads it) ·
  ⭐ [[paper_mode_requires_webhook_secret_06sep]].
⭐ · 🔬 **The 18F breakdown:** ⭐ 10 = the gemini exclusion **working** (⛔ no binary)
  · ⭐ 1 = ordering flake (⭐ passes standalone) · ⭐ 7 non-gemini, ⛔ NOT root-caused.
  ⭐ Recorded gate at `20061b6` is **10F/6054P/5S** ⇒ ⭐ they *may* be a subset.
  ⛔ That is a hypothesis — ⭐ settle it by comparing the **names**, ⛔ never by a
  gate run on production.
⭐ · ⭐ **OCI is now scriptable:** `~/.oci/config` written (⭐ user OCID, fingerprint,
  tenancy, region; ⭐ key `~/.ssh/oracle_api_private.pem`). ⛔ No console needed.
⚠️ · 🔬 **The OCI console renders broken in this Chrome:** a drawer sticks at
  `transform: translateX(1920px)`, parking dialogs off-viewport ⇒ ⭐ clicks land
  nowhere and captures look "tiled". ⭐ Override that transform and it works.
  ⛔ It is not a screenshot artefact.
