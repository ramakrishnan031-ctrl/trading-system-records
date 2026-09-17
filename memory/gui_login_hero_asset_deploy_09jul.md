---
name: gui-login-hero-asset-deploy-09jul
description: "GUI Screen-01 Login hero swapped to a photorealistic chip+eagle WebP (base64-inlined, mix-blend-mode:lighten), deployed e0b26b7 09-Jul; first cycle of the centralized assets-library workflow + reusable pre-auth/blend techniques."
metadata: 
  node_type: memory
  type: project
  originSessionId: d2a118eb-0a38-47ce-9184-d58b65b01f01
---

**GUI Screen-01 (Login) hero asset — BUILT + DEPLOYED `e0b26b7` (09-Jul ~22:2x IST, off-market).** First cycle of Rama's centralized **assets-library workflow**: ① screen spec (`gui/NN. *.txt`+`.png` target mockup) → ② Asset Requirement Spec (9 fields/asset; report only genuinely-missing) → ③ ChatGPT generates → ④ Rama places in `ops_dashboard/assets/<cat>/<screen>/` → ⑤ implement referencing assets → ⑥ Rama live review → next. **ONE screen at a time; explicit approval between; never redraw/placeholder/invent assets; reuse first.**

**Shipped:** replaced the hand-authored inline-SVG chip+eagle in `login.html` with the approved **photorealistic chip+eagle** — base64-inlined **800×800 WebP, 106 KB file / 142 KB b64** (`data:image/webp`). Presentation-only; card/fields/footer/mobile-hide + all routes/backend/auth/config untouched. 354/354 ops_dashboard tests pass; verified via headless-Edge render of the real template + live `curl`.

**Reusable constraints/techniques (apply to future screens):**
- **Login is the ONE pre-auth screen → assets MUST be inlined, never referenced as files.** `backend/app.py` gates ALL routes incl `/static/*` behind login (`_LOGIN_EXEMPT={auth.login_get,auth.login_post}`); a `/static/` or `/assets/` URL 302s to /login pre-auth. Screens 02–22 are authed → file references are fine there.
- **Matte-black-bg raster + `mix-blend-mode: lighten`** over the panel's dark radial-gradient+PCB-grid = seamless: it drops the pure-black bg (no rectangle seam) while leaving bright pixels pixel-faithful (more faithful than `screen`, which brightens). `isolation:isolate` on the pane scopes the blend. **A WHITE-bg asset CANNOT be composited this way** — blend modes only cleanly drop a *black* bg over a dark backdrop; a white bg required an asset regen.
- **Asset QA gate before embedding:** measure bytes + corner pixels. Delivered v1 = 2 MB + WHITE bg (regen → matte black); v2 still 1.77 MB/1254px → I produced the optimized derivative (Rama authorized "visually-lossless ≤150 KB"). Target **base64 ≤150 KB** (not just file). Master `login-chip-eagle.png` (1.77 MB) + `login-chip-eagle.web.webp` (106 KB, the inlined one) both committed under `assets/illustrations/login/`.

**Deploy mechanics (gui-dashboard):** `git push origin main` → bare-repo post-receive checkout (INSTALL.md §0: **hook starts NOTHING**) → manual `ssh trading-vm 'sudo systemctl restart gui-dashboard'` (passwordless sudo OK). Verify via loopback: `curl 127.0.0.1:8500/login` (200 + new-hero grep), root 302→/login. Live URL: https://trading-system.tail1cdc6d.ts.net/login. **Awaiting Rama live review before Screen 02.** [[gui_redesign_screen01_login_08jul]] [[project_vm_architecture_locked]]

**Production asset policy (`bcf5aae`, 09-Jul — applies to ALL future screens):** git/production ships **ONLY the optimized asset** (`login-chip-eagle.web.webp`); raw editable **masters stay LOCAL-only**. Enforced: `git rm --cached` the 1.77 MB master (kept on PC, git-ignored) + removed from the VM working tree; `ops_dashboard/.gitignore` ignores `assets/**/*.png|jpg|jpeg` (force-add only if a raster is genuinely the final production asset). login.html references only the committed `.web.webp` (runtime uses the inline base64 data URI — no file dependency on either). **Every future screen: commit only the optimized `.web.webp`/`.svg`, never the master.**

**Aside flagged 09-Jul:** PC `TZ=Asia/Kolkata date` read ~5.5 h BEHIND the VM (16:47 vs 22:20 IST); VM is authoritative (daily TOTP works) → **PC clock likely ~5.5 h slow** (git commit timestamps skew; check PC NTP). Non-blocking; both agreed off-market.
