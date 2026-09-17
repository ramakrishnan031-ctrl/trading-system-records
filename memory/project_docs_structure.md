---
name: docs/web_claude/ folder structure
description: Authoritative 7-folder layout of docs/web_claude/ as of 18-Apr-2026 reorganization
type: project
originSessionId: f0372d08-5082-4fd3-945d-64733fe3796b
---
docs/web_claude/ now has 7 top-level folders (00–06). Folders 05_deployment and 06_live_operations added on 18-Apr-2026. See docs/web_claude/README.md for authoritative folder map.

**Why:** Web Claude reorganized loose chat-history step files into a permanent docs structure so VS Code Claude and future sessions can always locate instructions by path.

**How to apply:** When referencing deployment steps, fixes, or live ops playbooks, use the paths below — do NOT guess old loose filenames.

## Folder map

| Folder | Contents |
|--------|----------|
| 00_source_documents/ | g1_to_g10_summary, locked_decisions.yaml, v2_design_spec.md |
| 01_module_instructions/ | 32 module build specs (M11–M41) |
| 02_phase_instructions/ | 7 phase instruction files (Phase B/G/H/I etc.) |
| 03_audit_responses/ | 7 audit response files |
| 04_post_build_ops/ | 5 post-build ops files (task1–3, pending items) |
| 05_deployment/ | 5 deployment step files + fixes/ subfolder |
| 05_deployment/fixes/ | 4 fix instruction files (fix1–fix4) |
| 06_live_operations/ | 4 operations files (overview + 3 playbooks) |

## Key paths in 05_deployment/
- `00_deployment_overview.md`
- `step2_cleanup_env_files.txt`
- `step2_vm_venv_and_first_run.txt`
- `step3_systemd_and_firewall.txt`
- `step4a_systemd_restart_test.txt`
- `fixes/fix1_weekend_test_bug.txt`
- `fixes/fix2_scan_webhook_schema.txt`
- `fixes/fix3_holidays_schema_audit.txt`
- `fixes/fix4_requirements_split.txt`

## Key paths in 06_live_operations/
- `00_operations_overview.md`
- `monday_paper_playbook.docx`
- `monday_commands_runbook.docx`
- `paper_to_live_transition_plan.docx`

Total file count: 68 files (verified 18-Apr-2026).
