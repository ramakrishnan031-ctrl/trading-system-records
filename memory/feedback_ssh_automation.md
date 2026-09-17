---
name: SSH key passwordless for VM automation
description: trading_vm_secure key has no passphrase; Claude Code handles all VM operations
type: feedback
originSessionId: d5bd2391-ce3d-4d13-8c5f-cd1d20f63b64
---
SSH key `~/.ssh/trading_vm_secure` is now passwordless (passphrase removed 2026-04-28).

**Why:** Enables Claude Code to automate VM operations (git push, service restart, log tailing) without interactive prompts.

**How to apply:**
- Use `ssh trading-vm "<command>"` directly from Bash tool
- Git push: `GIT_SSH_COMMAND="ssh -i ~/.ssh/trading_vm_secure" git push vm main`
- All VM deployment/monitoring operations can be automated
