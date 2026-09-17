# SANDBOX BUILD PROPOSAL — Oracle Cloud aarch64 mirror of the live trading system

**Status: PROPOSAL ONLY. Nothing has been created. This stops and waits for approval.**

**Evidence provenance:** all ten investigated dimensions were judged **PARTLY_WRONG** by the adversarial verifier — none SOUND, none UNSOUND. Every figure below is the *corrected* version. Where a correction changed a decision, it is marked `[CORRECTED]`.

---

## 1. THE INSTANCE SPEC

| Field | Decided value | Basis |
|---|---|---|
| **Shape** | `VM.Standard.A1.Flex` | Exact production shape (IMDS: shapeConfig ocpus 2.0, memoryInGBs 12.0) |
| **Architecture** | **aarch64 / arm64** (Ampere Neoverse-N1) | Mandatory. Production venv contains 9 aarch64-only `.so` files; x86 is forbidden |
| **OCPU** | 2 | Exact production match |
| **RAM** | 12 GB | Exact production match (MemTotal 12,213,676 kB) |
| **Swap** | 0 (do not create) | Production is 0; `/etc/fstab` has no swap entry — structural, not accidental |
| **Boot volume** | **60 GB** — see conflict callout below | Oracle: a custom size must be *strictly larger than* 50 GB |
| **Boot volume tier** | Balanced (10 VPU, default) | Production's tier not measurable; default is the safe match |
| **Image** | `Canonical-Ubuntu-24.04-aarch64-2026.07.17-0` | Newest published catalogue build |
| **Image OCID** | `ocid1.image.oc1.ap-mumbai-1.aaaaaaaamtc6jgk5qnf36vkudldlyn3fhmngilbepfgxdir3v3hlujs2gcbq` | Verified against docs.oracle.com |
| **NOT the image** | Any `-Minimal-` variant; production's own image OCID `...rcggq2ehi...` | Production is the FULL server image (`build.info: build_name: server`). Its source image matches **no** published build (2026.02.28-0, 2026.04.30-1, 2026.06.29-0, 2026.07.17-0) — it launched 03-May from a build since withdrawn. Do not plan on pasting it |
| **Always Free eligible** | **NO** | Production already consumes 100% of the tenancy's Always Free A1 allowance (1,500 OCPU-hr + 9,000 GB-hr/mo = exactly 2 OCPU / 12 GB, halved 15-Jun-2026) |
| **Tenancy** | Existing tenancy, upgraded to **Pay As You Go** | A second Always Free tenancy violates one-account-per-person and risks suspension of the account running live trading |
| **Region** | `ap-mumbai-1` | Home region. Always Free block volumes must be created in the home region; the tenancy has only this one |
| **Availability domain** | `kveW:AP-MUMBAI-1-AD-1` | The only AD in ap-mumbai-1 |
| **Fault domain** | **Leave unspecified** | Lets OCI pick any of 3 — the only capacity mitigation available (there is no second AD) |
| **Instance display name** | `trading-sandbox` | Production's is literally `trading-system`; the marker guard depends on the difference |
| **OS hostname** | `trading-sandbox` | `socket.gethostname()` at `alerts/critical.py:105` is the **only** machine stamp in any alert payload |
| **VCN** | **NEW**: `vcn-sandbox`, CIDR `10.1.0.0/16` | Separate VCN. **No peering to production's VCN**, ever |
| **Subnet** | Public regional, `10.1.0.0/24` | |
| **Internet gateway** | Yes, route `0.0.0.0/0 → IGW` | Needed for apt/pip and SSH |
| **Public IPv4** | Ephemeral, assigned | SSH only |
| **Security-list ingress** | **TCP 22 from `<operator public IP>/32` ONLY** | Delete the default `0.0.0.0/0:22` rule. No 5000. No 5010. No 8500. No ICMP from anywhere |
| **Security-list egress** | Allow all (initially) | Required for apt/pip; may be tightened after Phase 3 |
| **Host iptables** | Default-DROP INPUT except `lo`, ESTABLISHED/RELATED, and tcp/22 from operator IP | Persist with `netfilter-persistent save`. **Never** run `deploy/install_vm_services.sh` — it inserts an *unrestricted* tcp/5000 ACCEPT at INPUT position 5 and persists it |
| **Webhook bind** | `127.0.0.1:5010` | `config/system_config.yaml:328` `bind_host` and `:335` `bind_port`. Required Pydantic field, `extra="forbid"` — a one-line YAML edit is complete and sufficient |
| **SSH keypair** | **NEW** ed25519, passphrase-protected, `trading-sandbox` | Never production's key. SSH alias `trading-sandbox` (production is `trading-vm`) |
| **Tailscale** | **NOT INSTALLED** | `[CORRECTED]` Production's `iptables INPUT` rule **1** is `ts-input`, containing `-A ts-input -i tailscale0 -j ACCEPT` — an unconditional accept for every packet on the tailnet interface. Joining the same tailnet grants the sandbox **unrestricted L3 access to every listening port on production**, including 0.0.0.0:5000. The source-IP rule bounds only the public interface |
| **OCI Cloud Agent plugins** | **All three DISABLED at launch**: Custom Logs Monitoring, Compute Instance Monitoring, **Cloud Guard Workload Protection** | `[CORRECTED]` — three enabled, not two. Otherwise sandbox logs and Cloud Guard findings land in the production tenancy's Logging/Cloud Guard |
| **Cron** | **Zero entries.** `crontab -r` on first boot, asserted | Nothing in the repo self-installs cron on boot; the only crontab *write* in the entire tree is the post-receive hook |
| **unattended-upgrades** | Disabled | Production has run it 138 times and has ~38 packages behind at any moment; a sandbox must not drift |
| **journald** | `SystemMaxUse=500M` | Production's is a bare `[Journal]` stanza and reached 3.16 GiB |

### CONFLICT WITH THE OPERATOR'S 50 GB PREFERENCE

**50 GB is not selectable as a custom boot-volume size.** Oracle's own rule (docs.oracle.com, Block/Concepts/bootvolumes.htm, verbatim): *"the custom boot volume size must be larger than the image's default boot volume size or 50 GB, whichever is higher"* — **larger than**, not ≥. Oracle's Always Free page additionally contradicts itself on the default (47 GB in the Compute section, 50 GB in the Block Volume section); the real default is unknown until the launch dialog displays it.

Your options:

- **Accept the image default** (47 or 50, whatever the dialog shows) — workable, and the closest thing to "50 GB".
- **Set 60 GB** — **recommended.** Sufficiency, measured: OS footprint ~4.6 GiB excluding journald; sandbox payload 1.23 GB; `data_store/backups` (14 GB) explicitly **not** copied; no cron, so no nightly backup regrowth. Steady state ≈ 8–10 GiB used of ~57 GiB usable ≈ 17%. Ten snapshots at 749 MiB = 7.3 GiB more. `scripts/disk_monitor.py` warns at 75% and criticals at 86% — 60 GB stays far below both.

47 GB would also work. It is 60 GB only because the snapshot store plus its (currently unreclaimed) trash tier is the one thing that grows without bound.

**Storage-allowance consequence:** production 100 GB + sandbox 60 GB = 160 GB of the 200 GB Always Free block allowance, leaving 40 GB and five *shared* volume-backup slots. `[CORRECTED]` The "100 GB free" figure in the source investigation was one instance's own `lsblk`, not a tenancy inventory — it is an **upper bound**, unverified. **The Console's Block Volumes + Boot Volumes + Backups pages must be read before launch** (see §6.2).

---

## 2. COST AND ELIGIBILITY STATEMENT

**Not free forever. Not free during a trial. Billed — with an unresolved band.**

### Why it cannot be Always Free
Oracle halved the Always Free Ampere A1 allowance effective **15-Jun-2026**, with no announcement, and terminated over-limit instances on or after 18-Aug-2026. The allowance is now **1,500 OCPU-hours + 9,000 GB-hours per month**, which is exactly 2 OCPUs and 12 GB run continuously. Production (measured via IMDS: 2.0 OCPU, 12.0 GB) consumes **100% of it**. There is zero free-tier A1 headroom for a second instance. Creating a second free tenancy is prohibited (one account per person) and can trigger suspension of the account running live trading.

Incidental correction: production was already at 2 OCPU / 12 GB on **09-Jun-2026** (`/var/log/dmesg.4.gz`: `smp: Brought up 1 node, 2 CPUs` / `Memory: 12098708K/12582912K available`), six days *before* the halving. Oracle's cut did not pin it to the ceiling; it was there by choice.

### The cost band

Ampere A1 list price: **$0.01/OCPU-hour + $0.0015/GB-hour** → 2 OCPU + 12 GB = **$0.038/hour**.

| Scenario | Monthly cost |
|---|---|
| **If PAYG keeps the same 1,500/9,000 free allowance** (docs.oracle.com: *"All tenancies get the first 1,500 OCPU hours…"*) — production consumes 1,440 OCPU-hr in a 30-day month, 1,488 in a 31-day month, leaving **30 free sandbox-hours** (30-day), **6** (31-day), **78** (February) | Drill-only at ~20 h/month: **$0.00** (30-day) to **$0.53** (31-day). Left on 24/7: **$27.36** (30-day) / **$28.27** (31-day) |
| **If Oracle Support's reading holds** — InfoQ (2026-07), citing Support on 22-Jun-2026: the new limits apply only to free-tier accounts, and PAYG may retain the original **4 OCPU / 24 GB** at no cost | **$0.00** at any duty cycle |

**The band is $0.00 – $28.27/month and it is genuinely UNRESOLVED.** Oracle's documentation and Oracle's own support agents contradict each other. Resolve it with a written Support answer, or by running one billed hour and reading the cost report. Do not put a single number in a plan before then.

**Boot volume:** 60 GB is **free** if it fits inside the unused portion of the 200 GB Always Free block allowance (which also covers paid tenancies). If it does not fit, list price is $0.0255/GB-month + $0.0017/VPU/GB-month; at 10 VPU that is $0.0425/GB-month → **$2.55/month** for 60 GB. Worst case total: **$30.82/month at 24/7**, or **~$2.55/month drill-only**.

**Billing control — do this BEFORE upgrading:** the PAYG upgrade permanently removes the hard billing stop from the tenancy that runs live trading. Set a **Budget with an alert at $10/month** and **compartment quotas** capping A1 at 4 OCPU / 24 GB and block storage at 200 GB, first.

**Stop the sandbox from the Console/API between drills, never with an OS shutdown.** Verbatim from docs.oracle.com: *"Stopping an instance pauses billing… Shutting down an instance using the instance's OS does not stop billing for that instance."* Boot-volume storage bills regardless.

**The alternative if PAYG is refused:** a third-party ARM64 VPS (AWS Graviton `t4g`, Hetzner `CAX`, Scaleway `COPARM1`) provides genuine aarch64 Ubuntu 24.04 for a few dollars a month with **zero coupling** to the tenancy that runs live trading — a strictly smaller blast radius than a PAYG upgrade on the production account. Co-location in ap-mumbai-1 matters for broker latency in *production*; a replay-only sandbox does not need it. Exact pricing is not verified here and must be checked. The x86 `E2.1.Micro` fallback is **not** an option — architecture mismatch is forbidden, and one E2 at 47–50 GB would also consume half the remaining block allowance.

---

## 3. TOP RISKS, RANKED

### R1 — CREDENTIAL: the full live Zerodha credential set is already in plaintext on production, world-readable
`/home/ubuntu/.gemini` is 1.2 GB / 502 `.db` files. Scanning it with the real (non-placeholder) `.env` values found the complete live set across **28 distinct files**: both real Zerodha API keys, both API secrets, both 32-char base32 TOTP seeds, `ZERODHA_PASSWORD`, `TELEGRAM_BOT_TOKEN`, and the channel IDs. Extension breakdown: 22 `.env`, 4 `.jsonl`, 1 `.db`, 1 `.db-wal`. Modes **0644/0664** — group- and other-readable — versus the real `.env` at 0600.

**Mitigation (independent of the sandbox, and overdue):** rotate now — both Zerodha API secrets, both TOTP seeds, the account password, and the Telegram bot token. Exclude `/home/ubuntu/.gemini` **entirely** from any copy; the previously proposed `**/*.db` glob covers 2 of 28 files.

### R2 — CREDENTIAL: a live broker access token sits in `data_store/session/` on every trading day
`data_store/session/zerodha_token.json` (`main.py:134`, `deploy/token_watcher.sh:20`) holds a live Zerodha `access_token` from 08:15 until the `0 5 * * *` cron deletes it the next morning. It was invisible to the weekend inventory that produced the exclusion list.

**Mitigation:** exclude `data_store/session/` as a **directory**, not by filename. That also excludes `gui_secret_key` (64 B Flask session key — a copied one lets a production session cookie authenticate against the sandbox).

### R3 — PRODUCTION: the sandbox becomes a second autonomous live trader
Copying `.env` plus the systemd units arms a second live trader on the same broker account. `trading-system.service` is `ExecStart=… main.py --mode live`, `WantedBy=multi-user.target`. `token-watcher.service` runs as **root**, `Restart=always`, and exists to auto-start trading on a fresh token — and it starts `trading-system.service` **by name**. Inference, not measured: a Kite login from the sandbox would very likely invalidate production's access token, killing a production trading day.

**Mitigation:** fresh `.env` with **no** Zerodha credentials at all (§4, Phase 4.4); install units **disabled** and **sbx-prefixed**; do **not** install `token-watcher` or `security-watcher`; add a boot-time refusal — if `/etc/trading-sandbox` exists and any `ZERODHA_TOTP*`/`ZERODHA_PASSWORD*` is set, exit non-zero. `main.py:2377` `is_paper = (args.mode == 'paper')` — one argv string — is otherwise the entire barrier.

### R4 — PRODUCTION: a `git push` from the sandbox rewrites the live tree and the live crontab
The bare repo's `post-receive` (md5 `b7166732f1a4cbb70e7e1d2b984e3f88`, byte-identical to the repo copy) does `git --work-tree=/home/ubuntu/systems/trading-system --git-dir=/home/ubuntu/trading-system.git checkout -f main` and then `crontab deploy/cron/trading-system.cron`. The live crontab has **46** command lines; the canonical file has **45** — the extra is `41 7 7 9 * /home/ubuntu/preserved/2026-09-04_cnc_off/revert_delivery.sh`, the operator's dated one-shot. This exact failure already occurred on 04-Sep. (The crontab install is *conditional* on a `generate_crontab.py --generate | diff -q` guard passing; the `checkout -f` is not.)

**Mitigation:** seed the sandbox by **tarball, not `git clone`**. A clone sets `origin` to the production bare repo and any later push fires the hook. If a clone is used anyway, `git remote remove origin` is the *very next command*, verified by `git remote -v` printing nothing.

### R5 — PRODUCTION/CREDENTIAL: the tailnet is an open door (see spec row)
`ts-input` is INPUT rule 1 on production and accepts everything on `tailscale0`. **The sandbox must not join the production tailnet.** If tailnet reachability is genuinely needed, use a separate tailnet or an explicit ACL denying sandbox→trading-system, and verify it — do not rely on the source-IP rule, which bounds only the public interface.

### R6 — CREDENTIAL: identifiers and account data already committed to `main`
`docs/incident/2026-09-03_ANANTRAJ_broker_book.json` **is tracked on refs/heads/main** (contradicting the project note calling it untracked) and contains `account_id` and `placed_by` 51 times each — a real broker client identifier, on the deployed branch. Separately, `ops_dashboard/backend/config/gui_config.local.yaml` (untracked, 0600) holds a live `password_hash` and `totp_secret`, **and both were rendered into a verifier's tool output during this investigation**.

**Mitigation:** rotate the ops-dashboard password and TOTP seed. Scrub `placed_by`/`account_id` from any derived fixture — and understand that this does *not* remove what is already in git history; whether to rewrite history is the operator's call.

### R7 — PRODUCTION: the copy method itself can corrupt or contaminate
All five live DBs are `journal_mode=wal`. A `cp`/`rsync`/`tar` of a `.db` without its `-wal` yields a stale or torn image. `sqlite3 <path> ".backup <out>"` (bare form) opens the source **read-write**, and all three live DBs are writable by the deploying user. And `?mode=ro` still creates `-shm`/`-wal` sidecars beside a WAL-header file — which is precisely what happened during this investigation: **at least 5 new sidecar files were written into production's `data_store/backups/` at 01:48 and 3 more in `data/` at 01:54 on 06-Sep**, under a strictly-read-only mandate. `/tmp/tracked_py.txt` (26,242 B, mode **664**, world-readable) is also still present.

**Mitigation:** `sqlite3 'file:<src>?immutable=1' ".backup <dst>"` for the extraction, taken while the trading service is stopped; `?immutable=1` for every read. Disclose and clean the stray sidecars and `/tmp/tracked_py.txt` before the build. Note the extraction writes ~750 MB onto production's filesystem (71 GB free) — that is a production write and needs explicit authorisation.

### R8 — PRODUCTION: paper mode does NOT silence alerts, and the mail carries a production subject tag
`config/system_config.yaml:377` `telegram_alerts_in_paper_mode: true` — a `--mode paper` sandbox with a copied `.env` messages the real channel, and `deploy/token_watcher.sh:79-88` sends Telegram *outside* the app entirely. Email: `:440` (SMTP **login username**), `:448` (from), `:450` (to) all hardcode `pythonsystemalerts@gmail.com` and are **not** env-driven. `[CORRECTED]` `:440` was omitted from the earlier isolation list — omitting it means the sandbox authenticates *as* the production alert mailbox even after from/to are changed. And `scripts/preflight/report.py:197` / `scripts/cron_report_render.py:174` build the **email subject tag** `[LFL836]`, whose stated purpose is operator mail filtering — sandbox noise would land inside the live-alert filter. The tag appears at ~20 sites, not the ~8 previously counted.

**Mitigation:** Telegram `enabled: false`; rewrite `:440/:448/:450`; rewrite every `[LFL836]` tag to `[SANDBOX]` (enumerate with `git grep -n LFL836`, treat the count as unbounded until re-run at the sandbox SHA).

### R9 — PRODUCTION: preflight's auto-fix shells `sudo -n systemctl start` on named units
`scripts/preflight/checks/services.py:44-46, :85-87`. The tuple is `[CORRECTED]` **alert-watcher.service, token-watcher.service, security-watcher.service, cron, fail2ban, auditd** — three of the six are un-renameable OS daemons. On a shared host this starts production services; on the sandbox it starts **cron**, whose absence is the whole point. `ubuntu` has `(ALL) NOPASSWD: ALL`.

**Mitigation:** do not run preflight on the sandbox until the check list is explicitly re-scoped. This is also a decisive argument for a **separate instance**, not a second tree on the production VM.

### R10 — CORPUS DECAY: the broker-error corpus is expiring on two clocks
Four of eight broker failure classes exist **only** in `logs/system_*.log`, kept at 7 files per family (`scripts/output_retention.py:86`) ≈ 7 trading days: cancel-in-progress, MIS-blocked-for-SYMBOL, DataException 502, ReadTimeout. `[CORRECTED]` The DB half is **not** durable either — `scripts/db_retention.py:68` prunes `reconciliation_log` on a rolling **180-day** window, nightly, with backups keeping only 14 days behind it. Hard deadlines from 06-Sep-2026: the 325 June market-protection rows and 579 tick-size rows delete around **12–13 Dec 2026**; the sole 01-Jul tag-length row (id 7761) around **28-Dec-2026**.

**Mitigation:** rescue **both halves now**, before the sandbox exists — one grep over the 7 retained logs and one query over `reconciliation_log`, frozen to `tests/fixtures/broker_corpus/observed_errors.jsonl`. This is the only item on this list that gets worse by waiting.

### R11 — LIVE DEFECT surfaced by this investigation (not a sandbox risk — a production one)
`requests.exceptions.ReadTimeout` is **not** a subclass of `TimeoutError`, and `kiteconnect.exceptions.DataException.__mro__` is `(DataException, KiteException, Exception)` — not `GeneralException`. Both therefore match **no branch** of `_translate_kite_exception` (`broker/zerodha_adapter.py:274-330`) and fall through to a generic `BrokerError`. Proven in production: `logs/system_2026-09-03.log:64847` and `:64909` carry `exc_type: "BrokerError"` for a ReadTimeout on api.kite.trade. Consequence: `orders/order_reconciler.py::_classify_broker_error` returns `STATE_UNKNOWN` only for `isinstance(exc, BrokerTimeoutError)` — so the **only timeout class ever observed in production** is classified `RETRYABLE`. A read-timed-out *placement* would be retried blind: exactly the double-sell hazard `STATE_UNKNOWN` exists to prevent.

**Mitigation:** this is a pre-build-review-gate item for the operator, not something the harness should quietly fix. It is also the single strongest argument for building the harness at all.

### R12 — CAPACITY: the instance may simply not launch
`ap-mumbai-1` has exactly **one** availability domain, so Oracle's own first-line "out of host capacity" mitigation — try a different AD — does not exist. Capacity reservations are barred to Free Tier (available on PAYG, but billed at 85% even when unused). Production proves capacity existed on 03-May-2026; that is not evidence for today.

**Mitigation:** leave fault domain unspecified; retry over hours/days; if the drill schedule is time-critical, budget for a PAYG capacity reservation.

### R13 — IDLE RECLAMATION
Verbatim from the Always Free page: an instance is idle if, over any 7-day window, **all three** hold — 95th-percentile CPU <20%, network <20%, memory <20% (A1 only). A drill-only sandbox trips all three by construction. The PAYG exemption is **community-reported only**; no docs.oracle.com sentence exempts paid accounts.

**Mitigation:** design the sandbox to survive reclamation — reproducible rebuild from this document plus the corpus tarball, nothing unique living only there. Do not rely on an undocumented exemption.

---

## 4. THE BUILD SEQUENCE

### PHASE 0 — Before anything is created (operator actions; no build)

| # | Action |
|---|---|
| 0.1 | **Read the tenancy type** in the OCI Console (Billing & Cost Management / account-type banner). Not measurable from the VM — `command -v oci` → not found, `~/.oci/config` absent. Every cost figure hangs on this |
| 0.2 | **Read the Block Storage inventory** (Storage → Block Volumes + Boot Volumes + Backups, home region). Record GB in use and whether a backup policy is enabled on production's boot volume. The "100 GB free" figure is an unverified upper bound |
| 0.3 | **Set a Budget ($10/mo alert) and compartment quotas (A1 ≤ 4 OCPU / 24 GB; block ≤ 200 GB) BEFORE upgrading to PAYG** |
| 0.4 | Get a **written Oracle Support answer** on whether PAYG retains the 4 OCPU / 24 GB free A1 allowance — or accept the $0–$28.27 band |
| 0.5 | **Rotate the R1 credentials** (both Zerodha API secrets, both TOTP seeds, account password, Telegram bot token) and the R6 ops-dashboard password_hash + totp_secret. Independent of the sandbox |
| 0.6 | **Clean the read-only violations** left on production: `/tmp/tracked_py.txt` and the stray `-wal`/`-shm` sidecars in `data_store/backups/` and `data/` from 06-Sep 01:48–01:55 |
| 0.7 | **Rescue the broker corpus** (R10) — both halves, to `tests/fixtures/broker_corpus/observed_errors.jsonl` |
| 0.8 | **Authorise (or refuse) the one production write the build needs**: a ~750 MB `.backup` extraction onto production's filesystem |

### PHASE 1 — Provision (does not touch production)

1. `ssh-keygen -t ed25519 -f ~/.ssh/trading-sandbox -C trading-sandbox` (passphrase-protected, on the operator's PC).
2. Create VCN `vcn-sandbox` `10.1.0.0/16`; public subnet `10.1.0.0/24`; internet gateway; route `0.0.0.0/0 → IGW`.
3. Security list: **delete** the default `0.0.0.0/0:22` rule; add TCP 22 from `<operator IP>/32`. Egress allow-all.
4. Launch: name `trading-sandbox`, A1.Flex 2/12, image `2026.07.17-0` aarch64, boot volume **60 GB**, subnet as above, ephemeral public IPv4, paste the **new** public key, **disable all three Cloud Agent plugins**, leave fault domain unspecified.
5. First boot: record `uname -r`. `[CORRECTED]` The first-boot kernel is a **third unknown value** — the April image baked 6.17.0-1010, not the then-current head, so a July image bakes something that is neither production's running 1018 nor its staged 1020. Record the delta; it converges on 1020 only after `apt upgrade` **and** a reboot.

### PHASE 2 — Host baseline

6. `sudo hostnamectl set-hostname trading-sandbox`; `sudo timedatectl set-timezone Asia/Kolkata`; `export TZ=Asia/Kolkata` in every unit file (four `date.today()` sites read the local TZ).
7. `echo SANDBOX | sudo tee /etc/trading-sandbox` — the marker every sandbox script guards on.
8. `sudo crontab -r; crontab -r`; assert `crontab -l` → "no crontab".
9. Freeze drift: `printf 'APT::Periodic::Update-Package-Lists "0";\nAPT::Periodic::Unattended-Upgrade "0";\n' | sudo tee /etc/apt/apt.conf.d/20auto-upgrades`.
10. `SystemMaxUse=500M` in `/etc/systemd/journald.conf`; restart journald.
11. **Pin Python BEFORE installing anything.** `[CORRECTED]` **Eight** packages carry `3.12.3-1ubuntu0.15`, not four: `python3.12`, `python3.12-minimal`, `python3.12-dev`, `python3.12-venv`, `libpython3.12-stdlib`, `libpython3.12-minimal`, `libpython3.12t64`, `libpython3.12-dev`. Installing `python3.12-dev` unpinned silently resolves the whole family to 0.16 and *reverses* a four-package pin. Write `/etc/apt/preferences.d/python312` pinning `python3.12*` and `libpython3.12*` to `3.12.3-1ubuntu0.15` at Pin-Priority 1001. Verify: `dpkg-query -W -f='${Package} ${Version}\n' 'python3.12*' 'libpython3.12*'` → **eight lines, all 0.15**. (`python3.12-venv` comes from **universe** — ensure it is enabled.)
12. Install: `git tree net-tools curl sqlite3 apt-transport-https ca-certificates gnupg iptables-persistent stress-ng fail2ban auditd audispd-plugins build-essential python3-dev python3.12-dev libssl-dev zlib1g-dev`. **Do not install:** `ufw`, `npm`, `nginx`, `certbot`, `python3.11`, `libffi-dev`, `unified-monitoring-agent` (the Cloud Agent installs it itself), `tailscale`.
13. Node 20 from NodeSource (arm64, deb822, pin 600) **only if ops_dashboard is in scope** — Ubuntu's `nodejs` is 18.19.1, the wrong major.
14. iptables default-DROP INPUT except `lo`/ESTABLISHED/tcp-22-from-operator; `netfilter-persistent save`.

### PHASE 3 — Code and environment (no credentials yet)

15. **Seed by tarball** to `/home/ubuntu/sandbox/trading-system` (deliberately *not* `/home/ubuntu/systems/trading-system`). If a clone is used, `git remote remove origin` immediately, verified.
16. **Rebuild both venvs from requirements — never copy.** `[CORRECTED]` A second venv exists and was omitted from every prior inventory: `gui-dashboard.service` ExecStart is `…/ops_dashboard/venv/bin/python`, a separate 32 MB / 17-package venv, gitignored. The main venv is aarch64-native (9 `.so` files), `pyvenv.cfg` pins `/home/ubuntu/systems/venv`, and every console-script shebang is absolute — copying it leaves every entry point broken. Baseline is **51 distributions**, not 53 (53 is a `pip list | wc -l` header artifact).
17. `config/instruments.csv`: gitignored, absent from the bare repo, 77,437 B / 2,229 lines, regenerated daily by the 09:00 cron **from the Kite API**. Since the sandbox has no Kite credentials, take a **one-way file copy** (a data copy, not a credential copy). Without it: `core/instrument_cache.py:104-116` raises `ConfigMissingError`, and `check_instrument_cache_size` (min_rows=1000) blocks boot.
18. Config edits (sandbox copy only): `system_config.yaml` `:328`→`127.0.0.1`, `:335`→`5010`, `:345` worker_count→`1`, `:375` telegram→`false`, `:429` email_fallback→`false`, `:440/:448/:450`→sandbox mailbox, broker_limits `jitter_sec`→`0`. Leave `allocator_mode: shadow` and `v3_hardgate_mode: shadow` — already non-binding. `accounts.csv`: exactly one `is_primary=TRUE`; any `enabled` row needs `paper_capital > 0`.
19. Rewrite every `[LFL836]` alert-tag site to `[SANDBOX]`.
20. systemd units: install as `sbx-*`, **disabled**, each with `SyslogIdentifier=sbx-<name>` — including `cron-watchdog` and `gui-dashboard`, which production leaves untagged (their journal lines read only `python`). **Do not install** `token-watcher` (root, starts `trading-system.service` by name) or `security-watcher` (`config/security.yaml:126-134` watches **absolute production paths** — it would hash and alert on production's files regardless of where the sandbox tree lives). `[CORRECTED]` Nine unit files exist on production, not eight; the ninth is `trading-system.service.bak-23aug2026`, a stale divergent copy of the live-trading unit — do not carry it.
21. Regenerate, never copy: `data_store/session/gui_secret_key` (app.py mints it on first boot when absent) and `ops_dashboard/backend/config/gui_config.local.yaml` (new `password_hash`, new `totp_secret`).

### PHASE 4 — Credentials (fresh, minimal)

22. Author a **new** `.env`, mode 0600. **Not from `.env.example`** — it documents 20 of the 27 real keys, omitting `ZERODHA_USER_ID`, `ZERODHA_PASSWORD`, `ALERT_SMTP_PASSWORD`, `ALERT_EMAIL_USER/_PASSWORD/_TO`, `GEMINI_BIN`.
23. Four boot-blocking keys: `ZERODHA_API_KEY_<primary>`, `ZERODHA_API_SECRET_<primary>` (f-string-suffixed from `accounts.csv`, `main.py:228-229`), `TELEGRAM_BOT_TOKEN`, `WEBHOOK_SECRET` (64 hex, `secrets.token_hex(32)`). The check is falsy (`if not os.environ.get(key)`), so unset and blank both abort cleanly with `missing_secrets`.
24. **Zerodha login credentials — omit all five.** `[CORRECTED]` This is the single most dangerous item and the earlier "cheap safe default" recommendation did **not** escape it. Production sets only the **generic** `ZERODHA_USER_ID` (len 6) / `ZERODHA_PASSWORD` (len 12); **no suffixed pair exists for any account**, LFL836 included. `scripts/auto_refresh_token.py:349-353` resolves suffixed-then-generic, so *any* account_id choice falls through to the generic pair. And nothing compares the broker-returned user to the configured account: `save_token(account_id=account.account_id, …)` stamps the *config* value into the token record, and `is_token_valid()` then compares that self-written field against the same config value. The one place a broker `user_id` is read (`scripts/preflight/checks/broker.py:317-319`) only **prints** it. A wrong-user login is silent and self-certifying. **Decision: the sandbox is replay-only. No login credentials, no `token-watcher`, no `auto_refresh_token`.** If a token is ever needed, hand-place the file.
25. Use **DR6114** as the account_id label with a **new** Kite Connect app registered against it. Do not reuse production's app key (shared rate-limit bucket, shared postback URL).
26. Telegram: new bot + new private channel, or leave `TELEGRAM_CHANNEL_PRIMARY` unset. Note it is **not** boot-blocking — unset means the engine boots green and drops every alert with only a per-send WARNING (`alerts/telegram_notifier.py:622-627`) while the 08:30/09:14/09:15 preflight phases fail CRITICAL.
27. SMTP: either set a real sandbox app password or **do not install alert-watcher**. `[CORRECTED]` Absent and blank are **identical** — `core/config_loader.py:902-903` is `os.environ.get(self.password_env, "")`, so both raise `ValueError` and the unit fails to start. There is no absent-vs-blank distinction.
28. Structural paper enforcement: boot-time refusal if `/etc/trading-sandbox` exists and any Zerodha login secret is set.

### PHASE 5 — Corpus extraction (the one production write)

29. Take it with the trading service **stopped** (after 17:35 IST, or a weekend).
30. `sqlite3 'file:/home/ubuntu/systems/trading-system/data_store/trading_system.db?immutable=1' ".backup /tmp/corpus.db"`; same for `analytics.db`. **Never** bare `sqlite3 <path>` (read-write). **Never** `cp` (WAL, torn image).
31. `scp` to the sandbox as `corpus.db` / `corpus_candles.db`, mounted **separately** from the sandbox's own live DB. The harness only reads them, only via `?immutable=1`, and never opens the sandbox's live DB.
32. Also copy: `data_store/v3/*.jsonl` (96,210,703 B — **UNREGENERABLE**, read-only), `data_store/candles/*.csv` (10,799,476 B), `config/instruments.csv`.
33. **Hard exclusions:** `data_store/backups/` (14 GB), `data_store/session/` (whole directory), `/home/ubuntu/.gemini` (whole directory), `~/.ssh`, `~/.cache`, `~/.npm`, `~/tools`, `~/preserved`, `.env` and `.env.bak-*`, `data_store/security/` and `security_state.json` (SSH fingerprints / host baselines — a sandbox must re-baseline or every check fires falsely), `logs/`, both venvs.
34. Post-copy scrub, **inside the sandbox corpus only**:
    ```sql
    UPDATE config_snapshots SET account_id = 'SANDBOX';
    UPDATE session          SET account_id = 'SANDBOX';
    UPDATE config_snapshots SET config_json = json_set(config_json,
             '$.system.alerts.smtp.username','sandbox@example.invalid');
    UPDATE webhook_audit    SET source_ip = '0.0.0.0';
    ```
    The `config_json` edit invalidates `config_hash` **by design** — expect a `CONFIG_DIFF` event on first boot. That is correct, not drift.

### PHASE 6–7 — Harness and snapshot tooling
See §5.

### PHASE 8 — Acceptance gate (each a single command; all must pass before the sandbox is declared usable)

```
systemctl list-units 'sbx-*'            # returns the installed set
systemctl list-units 'trading-*'        # returns 0
crontab -l                              # "no crontab for ubuntu"
ss -lntp                                # only 0.0.0.0:22 and 127.0.0.1:5010 (+8090/8510 if GUI in scope)
git -C /home/ubuntu/sandbox/trading-system remote -v     # prints nothing
hostname                                # trading-sandbox
grep -cE 'ZERODHA_(TOTP|PASSWORD|USER_ID)' .env          # 0
ls data_store/session/zerodha_token.json                 # no such file
which tailscale; ip link show tailscale0                 # both absent
dpkg-query -W -f='${Package} ${Version}\n' 'python3.12*' 'libpython3.12*'   # 8 lines, all 0.15
sudo iptables -S INPUT                  # no :5000 rule, no tailscale0 ACCEPT
```

---

## 5. THE REPLAY HARNESS DESIGN

### 5A — Signal replay (HTTP into the real receiver)

**Corpus reality.** 58 trading days exist (2026-06-12 … 2026-09-04; 223,484 `webhook_audit` rows, 208,946 `signals`, 62,068 reconstructible POSTs, 173,592 `screener_results`). But the **oracle-valid corpus is ≈34 days**, being the intersection of: `config_snapshots` (full resolved AppConfig JSON + sha256 per day, **47 dates from 2026-07-02**, nothing before), complete screener coverage, and `analytics.db` candles (54 days; missing 06-12, 06-15, 06-16, 06-17, 06-18). Advertise 34, not 58.

`[CORRECTED]` Screener coverage is 83.1% corpus-wide (35,354 signals have no screener row), but the gap is **fully accounted for**: `REJECTED_STRATEGY_CONTROL` 23,481 + `REJECTED_STRATEGY_CIRCUIT_BREAKER` 7,705 + `REJECTED_SHADOW_INNING_ACTIVE` 4,168 = 35,354 exactly. Coverage of everything that *reached the screener* is **100%**. On heavy strategy-control days (2026-08-03: 61% rejected) the oracle for those signals is a rejection status, not a score.

**POST reconstruction.** Keyed on `(scanner, received_at)` — proven lossless **globally**: zero groups with more than one distinct payload across all 208,946 rows; zero `received_at` values mapping to more than one scanner.

```sql
SELECT scanner, received_at, MIN(webhook_payload) AS body, COUNT(*) AS prod_accepted
FROM signals
WHERE received_at >= :day || 'T00:00' AND received_at < :next || 'T00:00'
GROUP BY scanner, received_at ORDER BY received_at;
```

**Request shape.** `POST http://127.0.0.1:5010/webhook/<scanner>`, `Content-Type: application/json`, body = the stored bytes **verbatim** (never re-serialised). Auth: default to **HMAC** — `X-Webhook-Signature: sha256=<hmac_sha256(secret, body_bytes)>` — with `require_hmac: true` in the sandbox so the token param is off. Secret from env, never a CLI arg.

**Redaction.** Only `webhook_url` was redacted, and the receiver never parses it. The delta is a measured constant, `len(scanner) + 101`, with **zero variance** across four sampled days. Optional `--restore-url` makes `payload_size_bytes` byte-match; purely cosmetic. Credential safety confirmed independently: zero unredacted rows across all 208,946, zero rows containing `token=`, exactly one redaction per payload, and the earliest redacted row *is* the earliest row — no pre-sanitiser window.

**Timing.** Schedule POST *i* at `t0 + (received_at_i − received_at_0)`. `received_at` is stamped inside the request (`webhook_receiver.py:641`), has microsecond resolution and zero collisions. Use absolute monotonic deadlines and a small worker pool so the sub-millisecond bursts arrive concurrently (min gap 200 µs; 12 gaps under 1 ms; 1,012 under 100 ms). `[CORRECTED]` Peak is **24 POSTs in any 60 s sliding window**, not 12 (12 was a calendar-minute bucketing artifact).

**Rate limit — do not disable it.** `[CORRECTED]` Simulating the 60-token / 5.0-per-second bucket over all 3,523 real 02-Sep timestamps compressed by *S*: `S=1,2,4,8,16` → **zero 429s**. First 429s at `S=31` (134), `S=32` (206), `S=64` (1,723). The earlier "8× drains the burst in ~22 s" claim is false; 8× and 16× are entirely safe.

### Determinism blockers and how each is handled

| # | Blocker | Location | Handling |
|---|---|---|---|
| 1 | `now_ist()` has no seam — 203 call sites, 39 modules | `core/time_authority.py:94-99`; `configure()` takes thresholds/callbacks only | **Patch `core.time_authority.datetime`.** `[CORRECTED]` This is the one seam that works. `now_ist` resolves the name `datetime` from time_authority's own module globals **at call time**, so swapping that attribute re-clocks all 203 sites — including the **31 modules** that do module-scope `from core.time_authority import now_ist` (order_placer, fund_manager, kill_switch, webhook_receiver, signal_processor, zerodha_adapter, …). Rebinding `now_ist` itself reaches **none** of those 31; the earlier plan called out only `step_executor` as the exception when it is one of 31 instances of the rule |
| 2 | **`check_ntp_sync` blocks the boot** | `utils/startup_checks.py:506-545` | `[NEW — not in the original plan]` Makes a live UDP/123 call to `pool.ntp.org` at every boot; drift ≥ `block_sec=5.0` is a **BLOCKING failure**. A virtual clock set days back = ~176,000 s drift. Either inject `ntp_fetcher_fn` (the parameter exists at `:512`, "injectable for tests") to return virtual time, **or** run fully offline — the exception path at `:533-545` returns `passed=True, skipped=True`. Decide before first boot |
| 3 | Holiday filename chosen at **module import** | `core/config_loader.py:2411`, inside the module-level `_CONFIG_FILES` tuple | Only `nse_holidays_2026.yaml` is committed. **Pin every virtual date to 2026.** Late patching appears to work then picks the wrong file at a year boundary |
| 4 | `EntryThrottle` gates on `time.monotonic`, constructed **without** its `clock=` seam | `signals/entry_throttle.py:40-52`; `signals/signal_processor.py:229-235` | Pass `clock=` from the virtual clock. **Do not zero** the config (`system_config.yaml:350-353`: 20 s min-gap, 3-per-60 s burst, 300 s per-symbol) — that removes a real live gate and gives a green replay of a system that no longer has it. Every reject path also releases the capital reservation, so capital state diverges too |
| 5 | ~89 other `time.monotonic` sites, 6 `perf_counter`, 9 raw wall-clock reads | `entry_gate.py:383-404`, `step_executor.py:159`, `mis_autosquareoff.py:383-393`, `eod_squareoff.py:308`, `candle_store.py:242`, `cron_heartbeat.py:136-141` | Triage before claiming the monotonic surface is patched — it is not a one-module job. `[CORRECTED]` **libfaketime is a live option**, not a dead end: it is packaged for arm64 (noble/universe 0.9.10-2.1) and intercepts `CLOCK_MONOTONIC` **by default** (it ships `FAKETIME_DONT_FAKE_MONOTONIC` as the opt-out). Prefer in-process patching for control and observability; keep LD_PRELOAD as the fallback |
| 6 | `step_timeout_sec` hardcoded 5.0 s | `screening/step_executor.py:53`; `main.py:3234-3237` constructs `StepExecutor` **without** it | `[CORRECTED]` A **code** change, not config — there is no such YAML key. A step that times out scores NEUTRAL, so a slow sandbox produces different scores from identical inputs. Add the constructor arg at `main.py:3234` or raise the default |
| 7 | 5 worker threads race on capital and position slots | `signal_processor.py:277-280`; `system_config.yaml:345` | Set `worker_count: 1` (validator allows 1). Accept that the replay then no longer exercises the in-flight/TOCTOU contention path |
| 8 | uuid4 IDs; the ranker's final tiebreak is a random UUID | `core/ids.py:52/57/66`; `allocation/ranker.py:16-19` | `triggered_at` is stamped to the whole minute — **208,946 of 208,946** rows have `seconds == '00'` — so `triggered_epoch` ties en masse and `str(signal_id)` decides. Replace with a seeded counter derived from the corpus row. (The module docstring claiming "fully deterministic / replayable, no clock or random reads" is actively misleading) |
| 9 | Unseeded `random.uniform` 429-backoff jitter | `broker/zerodha_adapter.py:1984-1987` | `jitter_sec: 0` in the sandbox broker-limits, or seed `random` |
| 10 | `triggered_at` re-anchors to the sandbox date | `signals/webhook_receiver.py:604-611` | Two mutually exclusive failures without a virtual clock: persisted `triggered_at` → **100% EXPIRED** (age vs `expiry_sec: 600`); raw payload → the receiver re-stamps with today's date. **All 208,946 stored payloads are time-only** (0 full-date, 0 null), so with the clock set to each POST's arrival moment the receiver stamps the correct historical date *by construction* and the defect self-heals. Use `--anchor original` + controlled clock for oracle runs; `--anchor now` for iteration only — it shifts the scored `time_of_day` step and is **not** score-neutral (magnitude unmeasured) |
| 11 | `UNIQUE(fingerprint, fingerprint_date)` makes run 2 a silent no-op | `webhook_receiver.py:916-960` | Truncate `signals`/`screener_results`/`webhook_audit`/`trades`/`orders`/`gate_state` between runs (via the snapshot tool), or advance the virtual date. **Assert accepted-count > 0** and compare per-POST against `prod_accepted` — a green "all 200 OK" run can have inserted nothing |
| 12 | Pre-parse 403/503 gates | `webhook_receiver.py:536` (kill switch), `:544` (queue ≥240), `:551` (entry window 10:00–15:00) | With the virtual clock inside the window these behave as production did. Kill switch must be inactive. Do not widen the window unless replaying outside it deliberately |
| 13 | Config drift silently invalidates the oracle | `config_snapshots` | 47 dated snapshots (2026-07-02 … 2026-09-04). Pin the sandbox to the replayed day's snapshot. **Days before 02-Jul are not oracle-valid** |
| 14 | **`excluded_symbols` is LIVE, not empty** | `system_config.yaml:131-136`; gate at `webhook_receiver.py:673-679` | `[CORRECTED]` Five entries: E2E, GVPIL, BIRLACABLE, SHANKARA, MCLEODRUSS. The gate appends `REJECTED_EXCLUDED_SYMBOL` and inserts **no signals row**, so it is a further source of "unreconstructible" slots. The earlier claim that this gate is inert is false and would send a builder hunting accept-count divergence in the harness |
| 15 | Symbol aliases applied at the edge, before any DB write | `webhook_receiver.py:665`; `config/symbol_aliases.yaml` | `[CORRECTED]` **2** entries (`TVSSCS→TVSSRICHAK`, `SIGMAADV→SIGMAADV-BE`), not 3. The replay inherits the *sandbox's* map — pin it to the replayed day |

**What the corpus does NOT reproduce (scope the determinism claim honestly):**
- **Step 0**, the MIS learned blocklist (`screening/secondary_screener.py:138-160`), runs **before** the quote fetch and is runtime state accumulated from broker HTTP 400s. Not in the corpus.
- Throttle / sizing / daily-limit rejections: on 02-Sep, `REJECTED_ENTRY_THROTTLED` 17, `REJECTED_SIZING_CONCENTRATION` 17, `REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT` 8. No quote snapshot reproduces these.
- The DUPLICATE path (1,514 all-duplicate POSTs/day) and the out-of-window 403 path (649/day). `[CORRECTED]` `webhook_audit` stores **no rejection reason**, so the 1,514 are an unrecorded mix of DUPLICATE / EXPIRED / IN_PROCESS / INVALID / EXCLUDED. Omission is behaviour-neutral for the TTLCache only (cachetools 7.1.2 `__contains__` provably does not extend TTL); it is **not** neutral for `IN_PROCESS`, which is concurrency-dependent — dropping those POSTs removes exactly the contention that produced them.
- **Four of the ten scoring steps are constant by construction today**: `volume_surge` 0.0 and `atr_filter` 0.0 (154,726 of 154,726), `rsi_range` 0.5 and `sector_strength` 0.5 — starved by the hardcoded `None`s at `secondary_screener.py:411-415`. That makes replay easy now and **invalidates every baseline** the day anyone populates `atr`/`rsi`/`sector`/`avg_volume_20d`. Pin the baseline to the deployed SHA and record that 40% of the rubric is inert.

**The fake market-data provider.** `[CORRECTED]` **Key on `signal_id`**, not `(symbol, minute)`. `screener_results` has **no `symbol` column** (join through `signals`), and under a `(symbol, minute)` key **12,582 of 151,812 buckets (8.3%)** hold two or more distinct snapshots — the provider would inject the very nondeterminism it exists to remove. Reserve `(symbol, minute)` only for the paths with no signal_id (entry_gate pullback polling, the FIX-067 re-anchor re-fetch), and document a tie-break rule. Return `None` for the 192 empty snapshots on 02-Sep so `SKIPPED_QUOTE_UNAVAILABLE` is exercised faithfully.

The snapshot is a 1:1 invertible image of the broker `Quote` for the **screener's ten fields only** (`ltp, bid, ask, volume, upper_circuit, lower_circuit, vwap, open, day_high, day_low`; `circuit_state` derived; the rest hardcoded `None`). `[CORRECTED]` There are **7 production `quote_fn` wirings**, not 6 — `main.py:2978/3033/3133/3252/3575/3798` plus `orders/order_reconciler.py:279` — and the non-screener ones read more of the `Quote`. **Stub the adapter, not the call sites**; enumerating call sites is the wrong safety primitive, and the earlier enumeration already missed one. Post-entry exit polling uses `analytics.db` candles (1,563,963 1-min bars, 54 days, 1,268 symbols, 97.7% symbol coverage on 02-Sep).

**First test case — corrected oracle.** Replay 02-Sep whole-day. Expected: **1,359 POSTs, 13,601 symbol slots, 3,831 ACCEPTED, 3,831 screener rows**. `[CORRECTED]` The trade oracle is **4 PROCESSED + 3 PLACEMENT_FAILED**, not "7 trades" — MODISONLTD 10:00, COALINDIA 10:05 and MODISONLTD 10:06 were broker rejections that a stub cannot reproduce, so an assertion on "7" fires on every run. Only the POST/accepted/screener-row counts are stub-independent. Also note the plan's own `--anchor now` default is not score-neutral, so oracle runs must use `--anchor original` with a controlled clock.

**Harness safety interlocks (non-negotiable):** refuse any target not resolving to 127.0.0.1; require `/etc/trading-sandbox`; open the corpus only with `?immutable=1`; refuse the production host under any spelling; `--dry-run` prints method/URL/redacted-headers/body and POSTs nothing. Treat `webhook_payload` as opaque bytes — no eval, no f-string interpolation, no shell interpolation.

### 5B — Broker-response replay

**Seam — zero production change.** `ZerodhaAdapter(kite_client=ReplayKiteClient(), paper_mode=False)`. `broker/zerodha_adapter.py:342` (`kite_client: Any,  # KiteConnect or mock`), stored `:383`. Verified chokepoint: **no module under `orders/` imports kiteconnect**; 23 `self._kite` references, all in the adapter. Production wiring (`main.py:2383`) is untouched.

**Paper mode CANNOT be used for this** — three independent reasons:
1. `place_order` short-circuits at `:573-584` and returns **before** `:604 self._kite.place_order`, so a fake client is never consulted.
2. `get_order_history`'s paper branch (`:1127-1149`) returns exactly **one** synthetic entry with `rejection_reason=''` — structurally incapable of a rejection message or the 4-then-7 cancel-lag ladder.
3. `get_quote_raw` returns `{}` unconditionally in paper (`:1769-1777`), which **silently disables** the slippage guard (`order_placer.py:1106-1107`), the price-drift top-up (`:1200-1201`) and the liquidity/spread gate (`:4065-4100`). **A paper sandbox replays a strictly more permissive system than live.** Implement `get_quote_raw` for the sandbox or the replay cannot reproduce any decision those three guards blocked.

`tests/integration/conftest.py` builds the whole system with `kite_client=None, paper_mode=True` — reusing that fixture yields a **green test that never touched the rejection path**. Do **not** add an env-var hook inside `main.py:_build_kite_client` (`:381-390`): a live boot with a stray env var would then trade against a fake broker while believing it is live. Construct the adapter directly, and make the fake refuse to construct if `ZERODHA_ACCESS_TOKEN` is set.

**ReplayKiteClient surface — 16 methods:** `place_order, place_gtt, modify_gtt, get_gtt, get_gtts, delete_gtt, holdings, cancel_order, modify_order, order_history, positions, margins, order_margins, quote, trades, orders`. Omit `reqsession` — the date-header hook (`:1286-1297`) early-returns when it is absent, explicitly for mocks. Optionally expose `GTT_TYPE_OCO` (read via `getattr` with a `"two-leg"` default).

Each method is script-driven by a per-call-index list of `{return | raise}`, where `raise` names a **kiteconnect exception class** and a verbatim message, so `_translate_kite_exception` (`:274-330`) does the real translation and fixtures get genuine `OrderRejectedError` / `BrokerTimeoutError` / `BrokerRateLimit429Error` objects. The existing in-tree precedent (`tests/integration/test_fix190_incident_replay.py`) constructs `OrderRejectedError` directly with a message only — bypassing the translator — which is exactly why raising through it is the better design.

**Corpus (rescue immediately — see R10):**

| Source | Content | Decay |
|---|---|---|
| `reconciliation_log.action_taken` | 915 rows; **5 raw strings / 4 messages** `[CORRECTED]` — tick-size 0.05 (579, 16-Jun only), market-protection **two disjoint clusters** (325 rows 15–16 Jun at len 115; 8 rows 03-Sep at len 116 with a trailing `)`), MIS-till-3:12-PM (2, 27-Aug), Invalid-tags (1, 01-Jul, id 7761). The trailing `)` is on **9 of 915** rows, not all | Rolling **180 days**; June clusters gone ~12–13 Dec 2026, 01-Jul row ~28-Dec-2026; backups keep only 14 days |
| `logs/system_*.log` | 21 adapter ERRORs / **7 classes** across 7 retained days. **4 classes have no DB copy at all**: cancel-in-progress, MIS-blocked-for-SYMBOL, DataException 502, ReadTimeout | 7 files per family ≈ 7 trading days |
| `docs/incident/2026-09-03_ANANTRAJ_broker_book.json` (tracked on main) | 30 raw Kite orders × **36 keys** `[CORRECTED]`, 16 trades × 13 keys, three complete 7-entry order histories | Permanent (but see R6 on the embedded identifiers) |

**The three named incidents:**

| Incident | Fidelity | Fixture |
|---|---|---|
| **03-Sep, 8× market-protection rejection** | Full | `reconciliation_log` ids 7907–7914; 8 adapter ERROR lines at 15:10:17.585 … 15:12:09.404 with full `exc_traceback`. `[CORRECTED]` Span is **111.819 s**; both `docs/incident/…ANANTRAJ.md:339` and `tests/unit/test_t2_broker_error_classification.py:4` say "111.4 s" and are wrong. Script `place_order` to raise `InputException(msg)` on every call; assert `_classify_broker_error` → TERMINAL and the caller escalates **once**, not 8 times in 111.819 s |
| **1.115 s cancel lag** | Full — the only fixture with raw payloads | `order_history_260903170310434` ladder: `[PUT ORDER REQ RECEIVED, VALIDATION PENDING, OPEN PENDING, OPEN, CANCEL PENDING, CANCELLED, CANCELLED]`. Serve `entries[:4]` on call 1 (ends on `OPEN` → correctly non-terminal) and all 7 on call 2; `…432` returns 7 always. **`[CORRECTED]` There is NO clock seam** — `_verify_cancelled` (`orders/mis_autosquareoff.py:919-956`) uses real `time.monotonic` and `time.sleep`. Either accept ~1.25 s real wall time (5 polls × 0.25 s inside the 5.0 s deadline) or shrink the module constants at `:106-107`, which the code comment invites. Also `[CORRECTED]`: the 1.115 s is the interval between mis_autosquareoff's verdict (15:07:04.601) and **order_placer's unrelated poll** (15:07:05.716) — not "the next verification poll". It still proves the broker was terminal by then |
| **01-Jul tag-length** | Message-level only (logs rotated in July) | `reconciliation_log` id 7761. A **regression pin on a shipped fix**: `broker/zerodha_adapter.py:601-603` calls `truncate_tag_for_broker` unconditionally before `:604`. Assert the guard means it never fires |

**Write these three tests first, in this order:**
1. **The cancel-lag replay** — the only fixture that pins a timing bug and the only one with raw payloads.
2. **A `market_protection` gap test, written as EXPECTED-FAIL.** `place_order`'s kwargs (`:604-613`) carry no `market_protection`; all 30 orders in the book show `market_protection = 0`; F4 is unshipped. A *passing* assertion of current behaviour would **pin the bug**.
3. **A table-driven classification test** looping over the rescued JSONL, replacing the hand-written constants at `tests/unit/test_t2_broker_error_classification.py:44-46`, so a newly-rescued class must be explicitly triaged into TERMINAL / RETRYABLE / STATE_UNKNOWN. `_TERMINAL_REJECTION_PATTERNS` is deliberately one entry long — "add from a rejection someone has actually seen" — so this extends an allow-list, not a taxonomy.

**And surface R11 as a finding, not a fixture detail.** The ReadTimeout/DataException translation gap is the strongest justification for the whole harness, and it is a live production defect requiring the pre-build review gate.

### 5C — Snapshot / restore (the iteration loop)

**In-guest, not OCI volumes.** `sqlite3 'file:<db>?immutable=1' ".backup"` + `tar --zstd`. Payload **749 MiB**, create **~12 s**, verified restore **~40 s** (write throughput unmeasured — could be ~60 s on a 10-VPU Balanced tier). Reject OCI backup/clone for the loop: five backup slots **tenancy-wide, shared with production DR**; restore creates a *new* volume; attach requires a **stopped** instance; clone back-fill up to 30 minutes; clones of an attached source serialise. Take exactly **one** OCI boot-volume backup after the sandbox is built and scrubbed, as the cold "the box is unbootable" tier — never on a schedule. ZFS/LVM are unavailable (no `zfs`/`zpool`, no VG, root is `/dev/sda1` ext4 with no `shared_blocks` → no reflink). btrfs-on-loopback is a documented Stage 2, not a Stage 1.

**Corrections that must be carried into the tooling:**
- `[CORRECTED]` **A `.backup` image is `journal_mode=WAL`, not `delete`** — header bytes 18/19 = `[2,2]` on all 48 production backup files. The "delete" reading is an **artifact of `immutable=1` itself**. So: drop the "flip it back to WAL after restore" step, and drop the `[ "$jm" = delete ]` guard, which under `immutable=1` **always** returns "delete" and therefore can never fire — a green check that could not have been red.
- `[CORRECTED]` **Any** open of a WAL-header DB creates `-wal`/`-shm` — including `mode=ro` and `PRAGMA query_only=ON`. Only `immutable=1` is clean. This is also why the "production defect" reported earlier (something converting the newest daily backup to WAL) is almost certainly the investigation's own footprint, not a bug.
- `[CORRECTED]` `.sha3sum`'s observed default digest is **sha3-224** despite the help text claiming sha3-256. Pin `--sha3-256` explicitly everywhere.
- `snap-prove` **has no hostname guard** as delivered — it checks only `/etc/trading-sandbox`, hardcodes the **production** path, stops `trading-system`, and `DELETE`s from `signals`/`orders` (`foreign_keys=0`, so those deletes execute unimpeded against 208,946 / 1,332 rows). `ubuntu` has `NOPASSWD: ALL`. **Add the full guard (marker + hostname + explicit ROOT refusal) before installing either script anywhere.**
- **Reclaim the trash tier.** Restore renames ~863 MB of live state into `$TRASH` per run and nothing ever deletes it; `snap prune` enumerates only `$STORE` and is dry-run by default. ~1.6 GB permanent per drill ≈ 83 GB/year against 72 GB free. Add trash retention and put `snap prune --apply` in the schedule.
- **Do not schedule the drill Sunday 03:05.** All 90 `STARTUP` rows on record fall on weekdays — **zero on Saturday, zero on Sunday** — and the system is down by design in SOFT_KILL off-market. The `G3` service-proof gate, the thing that makes the whole drill non-vacuous, would fail every single week.
- Add `trap 'sudo systemctl start cron || true' ERR EXIT` — as delivered, a mid-restore failure leaves cron stopped.
- Keep the mutation-witness (`G1`) and negative-control (`G2`) design. They are the reason a green drill cannot be produced by a no-op, and they are the strongest part of the original proposal.

---

## 6. WHAT REMAINS GENUINELY UNKNOWN

### Operator must decide or look up

| # | Question | How to resolve | What it changes |
|---|---|---|---|
| 6.1 | **Is the tenancy Always Free or already PAYG?** | OCI Console → Billing & Cost Management / account-type banner. **Not measurable from the VM** (`command -v oci` → not found, `~/.oci/config` absent) | Every cost figure; the entire go/no-go |
| 6.2 | **How much of the 200 GB block allowance actually remains?** Is a backup policy enabled on production's boot volume? | Console → Storage → Block Volumes + Boot Volumes + Backups (home region) | Whether the 60 GB boot volume is free or $2.55/month; whether the 5 backup slots are already partly consumed |
| 6.3 | **Does PAYG retain the 4 OCPU / 24 GB free A1 allowance?** | Written Oracle Support answer, or run one billed hour and read the cost report | **$0.00 vs ~$28.27/month.** Docs and Support contradict each other in writing |
| 6.4 | **Is a PAYG upgrade acceptable on the tenancy that runs live trading?** | Operator judgement | It permanently removes the hard billing stop. Alternative: third-party ARM64 VPS (Graviton t4g / Hetzner CAX / Scaleway COPARM1) — genuine aarch64, zero tenancy coupling, strictly lower blast radius, exact pricing unverified |
| 6.5 | **Boot volume: 60 GB or the image default?** | Read the default off the launch dialog (47 or 50 — the docs contradict themselves) | 50 exactly is **not selectable** as a custom size |
| 6.6 | **Is `ops_dashboard` in scope?** | Operator | If no: drop the second venv, `gui_config.local.yaml`, `gui_secret_key`, Node 20, ports 8500/8090 entirely. Simpler and safer |
| 6.7 | **Does the sandbox need headless token refresh?** | Operator | Recommended **no**. If yes, the whole R3/§4.24 login hazard returns and the plan needs a fifth guard |
| 6.8 | **Which Kite Connect app?** | Register a new one against DR6114 | `.env` holds real-looking DR6114 credentials (16/32/32) — deliberately unread, so whether they belong to a distinct live app or are stale is unknown. **Do not assume; register new** |
| 6.9 | **Full 462 MB corpus or a scrubbed subset?** | Operator | Barely changes snapshot size (~750 MiB either way); decides whether snapshots are themselves sensitive artifacts needing 0600 and sync exclusion |
| 6.10 | **Rotation of the R1 `/home/ubuntu/.gemini` exposure** | Operator | Independent of the sandbox and overdue |

### Only resolvable by trying

| # | Question | Test |
|---|---|---|
| 6.11 | **Is A1.Flex capacity obtainable in ap-mumbai-1 today?** | The only test is a real LaunchInstance attempt. Oracle publishes no per-region capacity status. One AD, so no AD fallback; capacity reservations barred on Free Tier. Production proves capacity existed on 03-May-2026 — not evidence for today |
| 6.12 | **What kernel does `2026.07.17-0` first-boot?** | `uname -r` at first boot. It is neither 1018 (prod running) nor 1020 (prod staged) — the April image baked 1010, so a July image bakes a third value. Record the delta |
| 6.13 | **Boot-volume WRITE throughput** | `dd if=/dev/zero of=… bs=1M count=2000 conv=fsync` on day one. Read is 69.0 MB/s cold on production; write was never measurable (production writes forbidden). The ~40 s restore estimate assumes write ≈ read |
| 6.14 | **Does PAYG exempt instances from idle reclamation?** | Unknowable from docs — every exemption claim is community-sourced. Design for reclamation instead |
| 6.15 | **Magnitude of the `--anchor now` score divergence** | Measure on the sandbox: replay one day both ways and diff `step_results`. The `time_of_day` step is scored (0.5 in the INDOCO example) and re-anchoring shifts it. Until measured, `--anchor now` is iteration-only |
| 6.16 | **Can a weekend boot write a `STARTUP` row at all?** | Try one on the sandbox. Determines whether the snapshot drill's `G3` gate can ever pass off-market |
| 6.17 | **Would a Kite login from the sandbox invalidate production's access token?** | **Do not test this.** It is INFERENCE, and it is the reason to give the sandbox no login credentials rather than to run the experiment |
| 6.18 | **Does the Console's "My images → Image OCID" field accept a platform-image OCID?** | Untested. Moot if you use the catalogue build `2026.07.17-0`, which is the plan of record |
| 6.19 | **What is the environment-qualified test baseline at the deployed SHA?** | Establish it on the sandbox before adding any fixture: record interpreter, `PYTHONPATH`, cwd and invocation beside the count. Running pytest on production was correctly refused. A count without its environment is not a baseline |

---

**Nothing in this proposal has been created. Approve, amend, or reject — then Phase 0 begins with the OCI Console reads, not with a launch.**