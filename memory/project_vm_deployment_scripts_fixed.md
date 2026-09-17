---
name: VM deployment scripts fixed (03-May-2026)
description: Updated IP to 161.118.188.171 and path to systems/trading-system in DEPLOYMENT.md + copy_token_to_vm.bat; commit 97b8b23
type: project
originSessionId: 00972e13-adf4-462d-8fa4-5507eac59da8
---
# VM Deployment Scripts Fixed — 03-May-2026

**Commit:** 97b8b23  
**Date:** 03-May-2026

## Changes

Updated deployment scripts and docs from old VM (129.154.253.244, path `/home/ubuntu/trading-system`) to new VM architecture:

- **IP:** 129.154.253.244 → **161.118.188.171**
- **Path:** `~/trading-system` → `~/systems/trading-system`

### Files Updated

1. **DEPLOYMENT.md** (9 changes)
   - 7 IP replacements
   - 2 path updates

2. **scripts/copy_token_to_vm.bat** (2 changes)
   - Line 10: scp destination path
   - Line 15: success message

## Verification

Deployed to VM via git push:
```
remote: Deploying main to /home/ubuntu/systems/trading-system...
remote: Deployment complete.
419c430..97b8b23  main -> main
```

Files verified on VM at `~/systems/trading-system/` show correct IP/path.

**Why:** Aligns all deployment scripts with locked VM architecture (project_vm_architecture_locked.md).

**How to apply:** These scripts are now production-ready for Monday morning token copy workflow.
