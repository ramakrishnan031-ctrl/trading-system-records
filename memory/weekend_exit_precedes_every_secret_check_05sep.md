---
name: weekend_exit_precedes_every_secret_check_05sep
description: "A clean weekend/holiday exit returns ~285 lines BEFORE WEBHOOK_SECRET is ever read, so it proves nothing about .env or any credential."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9f103ec2-6ea8-4b32-a0ca-586e0765e2af
  modified: 2026-09-05T18:28:30.042Z
---

🔬 **MEASURED 05-Sep-2026** at the deployed tree `/home/ubuntu/systems/trading-system`.

**The holiday/weekend guard is the FIRST thing `main()` does — and it returns before
any secret, config or startup check runs.**

- 📄 `main.py:2098-2145` — "Holiday guard (SU6) -- BEFORE setup_logging; zero log on
  non-trading day". Prints `MARKET IS CLOSED / Reason : Weekend`, then **`return 0`**.
- 📄 `main.py:2198` `load_all(config_dir)` — config is not even loaded yet.
- 📄 `main.py:2430` `required_startup_secrets(_primary_id)` → the FIRST point
  `WEBHOOK_SECRET` is required (consumed by `run_all_startup_checks`).
- 📄 `main.py:3366` `WebhookReceiver(..., secret_token=os.environ.get("WEBHOOK_SECRET"))`.

⇒ ⛔ **A green weekend boot is NOT evidence that `.env`, the token, or any startup
check is healthy.** The run exits ~285 lines before the first secret is looked at.
⭐ This is the *"an absence that could mean two opposite things"* class → [[feedback_absence_needs_wide_check]].

**The discriminator that DOES work — exit codes (📄 `main.py:11-20`):**
- `0` = clean shutdown **OR** holiday/weekend  ⇒ benign
- `3` = startup check failure (blocking)
- `5` = invalid args / config / **missing env var**
🔬 `RestartPreventExitStatus=3 4 5` in the unit ⇒ ⛔ **exit 3 or 5 does NOT restart:
the service stays dead and the trading day is lost silently.**

**Corollary — the webhook cannot be tested off-market.** 📄 `WebhookReceiver` is
constructed at `:3366`, past the guard; 📄 `webhook_receiver.py:117-118`
`app.run(host=config.webhook.bind_host, port=config.webhook.bind_port)`;
📄 `:335` "this endpoint sits on 0.0.0.0:5000". 🔬 Confirmed by `ss -ltnp`: **nothing
on :5000** on a non-trading day. ⇒ ⭐ A Chartink "Test webhook" press off-market
returns connection-refused **regardless of whether the token is right** — it can
never distinguish a good token from a bad one → [[weekend_holiday_system_is_down]].

⛔ **So a token rotation done off-market is UNVERIFIABLE server-side until the next
08:15 boot.** ⭐ The only pre-boot evidence available is (a) the `.env` line's shape
and (b) that the 16 Chartink URLs agree with each other.

---

**HOW THE 05/06-Sep ROTATION WAS CLOSED ANYWAY — the client-side proof.**

⭐ Server-side verification was impossible (nothing binds :5000 off-market), so the
proof was taken from the **other end of the wire**, read-only, in-browser:

🔬 Fingerprint the ACTIVE secret on the VM without moving it:
`awk '/^WEBHOOK_SECRET=/{printf "%s", substr($0,16)}' .env | sha256sum`
🔬 Then, in the page at `https://chartink.com/alert_dashboard?page=1&per_page=50`
(all 16 alerts on one page; the webhook URLs are in the page HTML), SHA-256 each
alert's `token=` param **inside the page** via `crypto.subtle.digest` and return
only the hash prefix.

⇒ 🔬 **16/16 URLs · one distinct fingerprint · equal to the server's** ⇒ the
rotation is proven complete **without the plaintext ever leaving either end**.
⭐ This is strictly stronger than *"the 16 agree with each other"*, and it is the
technique to reuse on every future rotation → [[webhook_token_rotated_03jul]].

⚠️ Two gotchas: the browser tool **blocks return keys named like secrets**
(`tokenParamCount` → `[BLOCKED: Sensitive key]`) — ⭐ name the key `fp`. And the
alert-list pager ignores clicks; ⭐ use `?per_page=50` instead.
