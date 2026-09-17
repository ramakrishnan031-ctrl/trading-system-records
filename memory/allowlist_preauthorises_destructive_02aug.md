---
name: allowlist-preauthorises-destructive-02aug
description: The assistant permission allowlist pre-authorises an AI agent to run destructive mass-mutation commands against the LIVE trading DB without prompting — and removing the offending script flag does NOT narrow the allowlist.
metadata: 
  node_type: memory
  type: project
  originSessionId: 3eca6baa-6d72-49f6-8a3c-18984eeed2c5
  modified: 2026-08-05T17:32:29.797Z
---

✅🔬 **CLOSED 23-Aug-2026 ~18:20 IST — THE RE-MEASUREMENT THE TWO BANNERS BELOW ASK FOR IS DONE,
AND THE ANSWER IS A *THIRD* CAUSE NEITHER CANDIDATE NAMED.** 📄 `docs/audit/SUDO_AND_SUDOERS_WATCH_23-Aug-2026.md`.
🔬 **MEASURED in `.claude/settings.local.json`:** allow **533** (includes `Bash(ssh *)` — which is
why every read-only `ssh` ran unprompted) · ask **0** · **deny 16**, and the deny list contains
**`Bash(*systemctl stop *)`**, `*systemctl start *`, `*systemctl restart*` (each in a `Bash(…)` and a
`PowerShell(…)` form).
⇒ 🔴 **`ssh trading-vm 'sudo systemctl stop trading-system.service'` matched a DENY RULE ON THE
SUBSTRING `systemctl stop`** — bundled and bare, which is exactly the doubled denial recorded below.
⇒ 🔴 **IT WAS DENIED BY THE LOCAL CLAUDE CODE GATE. THE REQUEST NEVER REACHED THE VM.**
- ⛔ **Candidate (a) *"the allowlist was narrowed"* — REFUTED.** `Bash(ssh *)` is present and broad.
- ⛔ **Candidate (b) *"`sudo` is the discriminator"* — REFUTED.** **88** allow entries contain `sudo`;
  the discriminator is the verb `systemctl stop|start|restart`, ⛔ not the privilege.
🔬 **AND THE VM'S POSTURE DID NOT CHANGE.** `sudo -n -l` → `(ALL) NOPASSWD: ALL` for `ubuntu`
(group `27(sudo)`). ⛔ Not from `/etc/sudoers` — that file's **mtime is 2024-01-29**, the stock distro
file, content never edited. 💭 It is a `/etc/sudoers.d/` drop-in: that directory is `750 root:root`
with **mtime = ctime = 2026-05-03 12:29:12**, the same instant band as `/etc/passwd` (`12:29:07`) and
`/etc/group` (`12:29:07`) ⇒ **cloud-init at instance provisioning.** Corroboration: `auth.log` across
**5 rotated files (2026-07-26 → 2026-08-23, 28 days)** has **0** hits for
`visudo|usermod|gpasswd|sudoers`. ⇒ ⭐ **`sudo -n` would have succeeded on 05-Aug too.**
⭐ **THE LESSON, AND IT IS THE DURABLE PART: the 05-Aug OBSERVATION was accurate; the INFERENCE drawn
from it — *"the gate held exactly where this entry says it would not"* — was about THE WRONG GATE.**
⛔ A local permission rule was read as a property of a live production VM, and stood for 18 days.
🔬 **A separate, larger fact found in the same pass:** **`/etc/sudoers` is mode `440 root:root` and
`security-watcher.service` runs `User=ubuntu`** ⇒ `sha256_file()` returns `None` on every pass ⇒
`check_watched_files` skips it (`security_monitor.py:733-734` @ `742d9da`). The live
`data_store/security_state.json` carries **`"/etc/sudoers": None`** beside seven real hashes.
⇒ 🔴 **THE FILE HAS NEVER BEEN WATCHED, AND ⛔ A ZERO SUDOERS ALERT IS *NOT* EVIDENCE IT IS UNCHANGED**
(65 days of journal, 44 `Sensitive file changed` alerts for other labels, **0** for sudoers, control
fires). ⛔ Still **DO NOT PROBE** — the only privileged call made was `sudo -n -l`, which executes
nothing.
⚠️ **The 02-Aug `check_vm_state` allowlist finding below is UNTOUCHED and still stands.**
⚠️ Note also: **25 allow entries name `sudo systemctl restart trading-system` and are DEAD LETTERS** —
`deny: *systemctl restart*` outranks them. ⭐ Fails safe; ⛔ but the allowlist reads as authorising a
restart it cannot perform.

---

🔓⚠️ **CORRECTION — 18-Aug-2026 09:03 IST: THE `sudo`-IS-DENIED HALF IS NOW REFUTED, AND
IT IS THE *CONCLUSION* THAT EXPIRED, NOT JUST A VALUE.** **(P) `ssh trading-vm 'sudo -n
true'` returns rc `0`** — passwordless sudo IS available to this account for at least
that command. The 05-Aug banner below records the one `sudo` state-change as **DENIED,
twice**, and inferred from it that *"the gate held exactly where this entry says it would
not."* ⇒ ⛔ **that inference no longer holds.** Of the two candidate explanations below,
(b) *"`sudo` is the discriminator"* is now the WEAKER one.
⛔⛔ **STILL DO NOT PROBE. `sudo -n true` is a no-op with no state change and was the
minimum that could answer the question; WHAT ELSE `sudo` PERMITS IS `NOT MEASURED`, ⛔ not
assumed either way.** ⛔ **It was NOT used:** the 18-Aug `alert-watcher` restart — the one
action of the day that needed it — **was executed by Rama**, as ruled.
⭐ **Rama's framing, and it is why this got its own register row (`N18-07`):** *"A stale
permission record is worth a row on its own — it means an earlier session concluded
something about this system that is no longer true."*
📌 **The deliberate re-measurement the banner asks for — reading `.claude/settings.local.json`
and the deny rules — is STILL OWED. This discharges the flag in ONE direction only.**

🔴🔴 **REQUIRES RE-MEASUREMENT (05-Aug-2026 ~22:46) — THE CLAIM BELOW WAS INVERTED IN
PRACTICE AND HAS NOT BEEN RE-DERIVED.** Tonight, on the live VM: **every read-only `ssh`
ran UNPROMPTED** (`stat`, `cat`, `systemctl show`, `sqlite3 …?mode=ro`, `grep`, `scp`),
while the **one `sudo` state-change — `ssh trading-vm 'sudo systemctl stop
trading-system.service'` — was DENIED, twice** (bundled, then bare). ⇒ the gate held
exactly where this entry says it would not.
**Two candidate explanations, BOTH UNTESTED:** (a) the allowlist was narrowed since
02-Aug — which would contradict this entry's own *"removing the flag does NOT narrow the
allowlist"*; or (b) **`sudo` is the discriminator** and `Bash(ssh *)` never covered it.
⛔⛔ **DO NOT PROBE THE BOUNDARY.** Establishing which explanation holds by running
candidate `sudo` commands would be using a live money system as a test rig. **Re-measure
deliberately — read `.claude/settings.local.json` and the deny rules — not opportunistically.**
⭐ **Why this matters more than an ordinary stale entry: an inaccurate RISK note fails in
the WORSE direction — it makes you defend a hazard that has moved, and spend nothing on
the one that has not.** ⚠️ **Everything below is the 02-Aug measurement, unchanged and
still unrefuted as to the `check_vm_state` entries themselves — tonight tested only the
`sudo` path.**

⛔ **`.claude/settings.local.json` → `/permissions/allow` PRE-AUTHORISES AN AI AGENT TO
MUTATE THE LIVE TRADING DATABASE WITHOUT PROMPTING.** Measured 02-Aug-2026 (#8b Step-1):
**21 `check_vm_state` entries**, of which **2 are `--reset`** (raw kill-switch clear),
plus **both `--cleanup-*` flags** — `--cleanup-pending` mass-marks EVERY `PENDING_FILL`
trade `CANCELLED` with no capital release and no audit; `--cleanup-orders` mass-cancels
orphaned PENDING orders. All are `ssh trading-vm …` — i.e. against the **LIVE VM**.

**Why:** the allowlist accretes from past approvals. Each entry was reasonable once; the
*set* is now an authorisation surface nobody reviews, and it grants exactly the actions
the integrity campaign has been removing from docs and scripts.

**How to apply:**
1. ⛔ **The script fix and the allowlist are INDEPENDENT surfaces.** Removing `--reset`
   from `scripts/check_vm_state.py` does **NOT** narrow the allowlist — do not treat
   ledger #8b as closing this. Registered separately: debt-ledger **#11**
   (IA-XSEC authorisation-surface family) + register **§C.4 R12**, awaiting Rama.
2. ⚠️ **It is also STALE:** **11 of the 21 entries name `~/check_vm_state.py`**, a path
   Rama's 02-Aug VM check proved **does not exist**. A stale allowlist is not harmless —
   it hides how much is actually granted.
3. Before adding a permission for anything that writes to the live DB, ask whether the
   *sanctioned* tool would do instead (`deploy/resume.sh` / `scripts/clear_kill_switch.py`
   for kills) — allowlisting the raw route re-creates the anti-pattern at the harness
   layer, below where any code or doc fix can reach.

Detail: `docs/audit/ledger8b_check_vm_state_step1_02aug2026.md` §9.
Related: [[unpushed-pending-deploy-ledger]] · [[feedback-live-vs-latent-findings]]
