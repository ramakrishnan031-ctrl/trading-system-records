---
name: ssh-key-rebaseline-28jun
description: "28-Jun SSH key rotation was LEGITIMATE (Rama, DrHT9→uDRN8 SHA256:uDRN8…GKduk); security_monitor baseline updated + NEW durable approve_ssh_keys re-baseline command. Never re-flag as compromise."
metadata: 
  node_type: memory
  type: project
  originSessionId: af71af35-f911-422b-b85c-400ba1b0d5cf
---

**28-Jun-2026 SSH key rotation = LEGITIMATE (Rama), NOT a compromise — NEVER re-flag it as one.** Rama rotated SSH keys ~09:37–09:41 IST from his Airtel/Tamil-Nadu IP **223.237.190.224** (verified India, no VPN/proxy/Tor). A transient 2nd key (XrYwY…) was his and was removed. The ONE authorized key now:
**`SHA256:uDRN8BJTmfNGFfCLofbnXkIGtWF6qTtrREQrQJGKduk`** (ED25519 `oracle-vm-2026`).

**Why the CRITICAL flood:** `scripts/security_monitor.py` `check_authorized_keys` baseline (`config/security.yaml:expected_key_fingerprint`) was the OLD `SHA256:DrHT9VviCBFmeg+RBwO3wZhw+EwzhjRD/G2ceKntEqM` (19-Jun audit) → live uDRN8 ≠ baseline → "UNEXPECTED SSH KEY" CRITICAL each 6h realert window.

**FIX (DEPLOYED `033ae58`, 28-Jun):**
- **Part A:** committed `config/security.yaml` baseline DrHT9→uDRN8 — AFTER a hard safety gate that independently verified the live `~/.ssh/authorized_keys` has EXACTLY ONE key == uDRN8 (auto-trusting nothing). Alerts CLEARED: `security_monitor --report` → "No findings".
- **Part B (root cause = static git-tracked baseline that every deploy `checkout -f` reverts):** durable OPERATOR OVERRIDE **`data_store/security/ssh_key_baseline.json`** (NOT git-tracked → survives deploys), overlaid by `security_monitor.apply_operator_ssh_baseline` (wins when present; `check_authorized_keys` now LIST-aware for multi-key rotations). NEW command **`scripts/approve_ssh_keys.py`** — operator-run ONLY (never monitor-triggered): shows live keys + diff vs baseline; `--apply` writes the override + re-seeds `security_state.json` + ALWAYS Telegrams (a re-baseline can NEVER be silent). Override written + Telegram sent 28-Jun.

**★ FUTURE SSH KEY ROTATION PROCEDURE:** after ANY legitimate rotation, run `python scripts/approve_ssh_keys.py --apply` on the VM — no config edit, no deploy needed (the override is durable; the committed `config/security.yaml` default is just a fallback). Tests: +5 in `test_security_monitor.py` (42 pass). Related: [[monday-29jun-schedule]] (the same `checkout -f` clobber lesson), [[feedback_ssh_automation]].
