---
name: gui-redesign-screen01-login-08jul
description: "GUI redesign Screen 01 (Login) — BUILT + DEPLOYED + LIVE-VERIFIED 08-Jul ~21:54 IST. Corrected a wrong task premise (no hero existed), presentation-only, inline-SVG hero to avoid the auth guard."
metadata: 
  node_type: memory
  type: project
  originSessionId: 7691c8b3-1f80-4cdd-92c2-a4ebcf10749d
---

**DEPLOYED + LIVE-VERIFIED (08-Jul ~21:54 IST, off-market).** Screen 01 (Login)
merged to `main` (merge commit `9815786`, `--no-ff`, carrying `main`'s HEAD
forward from `7338e08` — this push ALSO shipped the schema-version fail-fast
`0b816dc`/`7338e08`, which was standalone-safe and already tested; see
`schema_version_failfast_08jul`). Pushed `origin/main` `005c007..9815786`;
VM bare-repo HEAD confirmed `9815786`; `gui-dashboard.service` restarted
(fresh `ActiveEnterTimestamp`, `active/running`, `Result=success`) — trading
stack unit states verified IDENTICAL before/after (untouched). Tailscale
serve intact (`/` → `127.0.0.1:8500`). **curl-grep live proof:** HTTP 200 at
`https://trading-system.tail1cdc6d.ts.net/login`, body contains
`.login-hero`, `.login-hero svg`, the inline-SVG comment, and the mobile
hide-hero rule — the NEW design is genuinely serving (the pre-deploy
`login.html` on the VM, mtime `Jul 5 00:55`, had zero redesign markup,
confirming this was genuinely undeployed, not a browser-cache issue).
Pre-push regression: 354/354 `ops_dashboard` tests green (run inside the
isolated `.venv` — a same-session run under system Python false-failed 1
test, `test_c_venv_has_no_kiteconnect`, purely from using the wrong
interpreter; not a real issue).

Screen 01 (Login) of the one-screen-at-a-time ops_dashboard GUI redesign was
BUILT: branch `gui-redesign-login-08jul`@`3537632` (+ doc-sync `28925da`),
off `main`@`271d24f`, then merged onto the current `main` (which had since
advanced via PUSH-1 + the fail-fast).

**Key correction to the instruction file's premise:** the task assumed the
deployed `/login` already implemented most of the spec (hero chip+eagle
etc.) and this was a small polish pass. Investigation (full `git log --all`
+ `git grep --all eagle` across every branch) proved the opposite — the
actual `ops_dashboard/frontend/templates/login.html` was a plain centered
card with **no hero pane at all**. `gui/01. Login-Screen.png` (paired with
the `.txt` spec) is a **target mockup**, not a screenshot of a live screen —
this repo's own history confirms that content never existed anywhere.

**Why this matters going forward:** the `gui/*.txt` + `gui/*.png` pairs for
the other 20 screens are almost certainly the same pattern (target mockup +
spec, not "already partially built"). Don't trust an instruction file's
"current state" framing without verifying against the actual template/git
history first — re-verify per screen.

**How to apply:** a real technical constraint surfaced that will recur for
every future screen with custom illustration/imagery: `backend/app.py`'s
`before_request` guard applies `login_required` to **all** routes including
`/static/*` (only `auth.login_get`/`auth.login_post` are exempt). Any art
needed on the pre-auth login screen must be inline (SVG/data-URI), never a
separate static file — otherwise it 404s for an unauthenticated visitor.
Other screens are post-auth so this constraint is Login-specific, but keep
it in mind if any other pre-auth surface gets added later.

Result: 40/55 hero/card desktop split, mobile ≤780px hides hero, inline SVG
chip+heraldic-eagle (4-side pins, neon glow, no CDN/external asset — CDN
grep gate passes since inline SVG has no `http://`/`https://`, note the
`xmlns` attribute on inline `<svg>` must be OMITTED in HTML5 or it trips the
gate's naive substring scan), field placeholders, footer shield icon,
two-tone title, Inter/IBM Plex Sans typography. Zero backend/route/API/auth
diff (confirmed via `git diff --stat -- ops_dashboard/backend` = empty).
354/354 tests pass. Gap doc: `ops_dashboard/docs/redesign/01_login_gap.md`.

**Status:** LIVE at `https://trading-system.tail1cdc6d.ts.net/login`; awaiting
Rama's browser sign-off (hard-refresh Ctrl+Shift+R to bypass any stale local
cache of the old page) before Screen 02 (Dashboard) starts.
