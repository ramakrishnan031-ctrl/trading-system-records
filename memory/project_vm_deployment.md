---
name: VM Deployment State (Oracle Cloud)
description: Oracle Cloud VM setup state, SSH config, deployment method for trading system
type: project
originSessionId: 214ee83f-3fa4-4b23-8f91-25eee5b7caac
---
VM setup complete through Step 1 (bootstrap + bare repo).

**Why:** Oracle Cloud Ampere ARM VM for reliable 24x7 trading system operation (replaces home PC prone to power outages).

**VM facts:**
- IP: 80.225.198.195, user: ubuntu, hostname: trading-system
- Ubuntu 24.04.4 LTS, aarch64, 12GB RAM, 67GB disk
- Python 3.14.3 via pyenv at ~/.pyenv
- Swap: 2GB configured, swappiness=10
- Timezone: Asia/Kolkata (IST, +0530)
- Bare repo: ~/trading-system.git (branch: main, NOT master)
- Checkout: ~/trading-system (post-receive hook auto-updates on push)

**SSH from PC:**
- Git Bash uses /usr/bin/ssh which can't reach Windows ssh-agent
- Must use /c/Windows/System32/OpenSSH/ssh.exe (Windows native)
- Key trading_vm_secure already loaded in Windows OpenSSH Agent service
- Git configured: core.sshCommand = /c/Windows/System32/OpenSSH/ssh.exe
- SSH alias `trading-vm` configured in C:\Users\rama\.ssh\config
- Push command: GIT_SSH="/c/Windows/System32/OpenSSH/ssh.exe" git push vm main

**How to apply:** For all future SSH commands to VM from Bash tool, always use /c/Windows/System32/OpenSSH/ssh.exe. For git push, prefix with GIT_SSH env var or rely on core.sshCommand config.

**Gitignore additions made:**
- `env` (credentials file without dot prefix — real API keys)
- `.claude/settings.local.json`
- `memory/`, `mempalace.yaml`, `CLAUDE_md_and_explanations.txt`
- `.gitattributes` added: `* text=auto eol=lf` for LF on Linux

**Next steps:** Steps 2–4a COMPLETE as of 18-Apr-2026. See project_deployment_status.md for full current state. Monday 20-Apr = first paper session.
