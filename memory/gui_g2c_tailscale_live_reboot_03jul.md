---
name: gui_g2c_tailscale_live_reboot_03jul
description: E3 Tailscale access LIVE + E4 reboot drill PASS (03-Jul) — ops dashboard reachable at https://trading-system.tail1cdc6d.ts.net (tailnet-only); Tailscale serve CLI syntax changed
metadata: 
  node_type: memory
  type: project
  originSessionId: 9fe7c775-fb70-4094-bcaf-e66df45399c5
---

**E3 Tailscale LIVE + E4 reboot drill (03-Jul-2026 ~22:15–22:21 IST, off-market).** Access-layer only — trading stack UNTOUCHED at every step (`trading-system` unit stayed `inactive` throughout, correct off-market).

**Access facts (LIVE):**
- VM host = `trading-system`; Tailscale machine = `trading-system`; tailnet = `tail1cdc6d.ts.net`; tailnet IP = `100.74.84.44`. Rama's phone `moto-g96-5g` (`100.85.45.94`) also on the tailnet.
- **URL → https://trading-system.tail1cdc6d.ts.net** — `tailscale serve`, **tailnet-only (NOT funnel)** → `http://127.0.0.1:8500`.
- Path: browser/phone (Rama's tailnet) → HTTPS (Let's Encrypt via tailscaled) → `100.74.84.44:443` → loopback → `gui-dashboard` `127.0.0.1:8500` (read-only DBs).
- **Listener proof:** 8500 stays `127.0.0.1`-only; `:443` bound to `100.74.84.44` + tailnet IPv6 (`fd7a:115c:a1e0::…`) — **zero `0.0.0.0` public listener added.** (Pre-existing `rpcbind 0.0.0.0:111` is unrelated — flagged for a later VM-hardening pass, NOT touched.)
- Night access confirmed: 22:15 IST `curl` → HTTP 302 → /login (time-lock is copy-gate-only, does not block access).

**⚠️ Tailscale CLI CHANGED (record for future serve/funnel work):** the old positional form `tailscale serve --bg https / http://127.0.0.1:8500` (as written in INSTALL.md §5 pre-E3) is **REMOVED** on the current Tailscale version — it errors and prints the replacement. Working form:
```
sudo tailscale serve --bg http://127.0.0.1:8500      # one-arg = HTTPS:443 / → target
```
Correctly STOPPED on the error and got Rama's explicit approval before running the new form (outward-facing change). INSTALL.md §5 updated to the new syntax + a full "Access — LIVE" block (facts, diagram, recovery/rebuild, SSH-tunnel fallback).

**E4 reboot drill = CLEAN PASS (no findings).** `sudo systemctl reboot` → new boot `2026-07-03 22:20:54` (back ~20s). All units returned to baseline: `gui-dashboard` ACTIVE, `token-watcher` active, `alert-watcher`/`security-watcher` `activating` (their steady baseline — NOT a fault), `cron-watchdog` inactive/static (timer), `tailscaled` active. `trading-system` stayed INACTIVE (correct — token-watcher only starts it in 08:00–16:00 on a fresh token; next live boot Mon 06-Jul 08:15). **`tailscale serve` persisted across reboot** (still proxying), 8500 loopback-only, :443 tailnet-IP-only, URL → 302 /login.

**Docs updated + committed (off-market):** `ops_dashboard/deployment/INSTALL.md` §5 (new CLI + Access-LIVE + recovery/SSH-fallback), `docs/SYSTEM_MAP.md` (E3 + E4 blockquote under the GUI section), `PATHS.md` (line-6 GUI block: live URL + E3/E4 done).

**SSH-tunnel fallback caveat (documented):** `ssh -L 8500:127.0.0.1:8500 ubuntu@161.118.187.249` reaches the port, but `session_cookie_secure: true` means login over plain http through the tunnel won't persist the cookie — Tailscale HTTPS is the only supported interactive path; tunnel = reach-the-port/health only.

**Pending (Rama's manual confirmations, handed over — not blocking deploy state):** install Tailscale on PC+phone (sign in `ramakrishnan031@gmail.com`), open URL + login + bookmark; negative test (phone Tailscale OFF on mobile data → URL must NOT load); post-reboot bookmark refresh.

State after this: **fully deployed + accessible.** Mon 06-Jul 08:15 boot activates A-2 + B-1(shadow); soak S1–S8 Mon–Wed per the locked contract. See [[deploy_a2_b1_gui_03jul]], [[gui_g2c_deploy_prep_03jul]], [[gui_readiness_g3_0_03jul]], [[project_vm_architecture_locked]].
