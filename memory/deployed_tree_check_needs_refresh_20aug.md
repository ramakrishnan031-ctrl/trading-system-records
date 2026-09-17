---
name: deployed-tree-check-needs-refresh-20aug
description: The GIT_INDEX_FILE deployed-tree drift check reports EVERY tracked file modified unless update-index --refresh runs between read-tree and diff-files.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3bdb2912-ae06-4bd6-bc2f-4df54526afca
  modified: 2026-08-20T03:23:08.907Z
---

**Measured 20-Aug-2026 on the VM, against a tree PROVEN identical.** The deployed-tree
drift check named in Gate E2 — and in the falsifiers of both the `n907` (`P3`) and
`tiers` (`T3`) predictions — is **wrong as written**:

| method | result |
|---|---|
| `read-tree <sha>` → `diff-files` | 🔴 **1,309 files reported MODIFIED — FALSE POSITIVE** |
| `read-tree <sha>` → **`update-index --refresh -q`** → `diff-files` | ✅ **0** |
| independent control: `md5sum` 6 tracked files vs their blobs at the sha | ✅ **6/6 MATCH** |

**Why:** `read-tree` populates a fresh index with **no stat data**. `diff-files`
compares worktree stat info against the index, so with every entry's stat blank it
calls every file modified. `update-index --refresh` fills the stat data in (re-hashing
where stat disagrees), which is what makes the subsequent `diff-files` meaningful.

**How to apply — the corrected recipe, all three commands sharing one `GIT_INDEX_FILE`:**

```
export GIT_INDEX_FILE=/tmp/idx_probe && rm -f /tmp/idx_probe
G="--git-dir=/home/ubuntu/trading-system.git --work-tree=/home/ubuntu/systems/trading-system"
git $G read-tree <sha>
git $G update-index --refresh -q          # <-- THE MISSING STEP
git $G diff-files --name-status           # empty == no tracked drift
rm -f /tmp/idx_probe
```

⛔ **Never report the un-refreshed output as drift.** ⭐ Always pair it with the
independent `md5sum`-vs-blob control on a few files — two methods that agree beat one
that cannot be wrong in a way you would notice.

🔑 This is a concrete instance of [[probe_method_must_be_verified_14aug]] and
[[feedback_verify_rc_not_output]]: **a red check needs its method verified before the
redness is believed** — here the check was red for a reason with nothing to do with the
tree, and on a deploy night it would have produced a false DEFER (or, worse, a hunt for
drift that does not exist). See also [[feedback_no_fixed_test_baseline]].

## Index line relocated from `MEMORY_REFERENCE.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 372 B (budget 300 B). The index now carries a hook and this link.

- 🔴 **[Deployed-tree drift check needs `update-index --refresh`](deployed_tree_check_needs_refresh_20aug.md)** — `read-tree`→`diff-files` alone called **1,309 files modified on an IDENTICAL tree** (fresh index has no stat data). Gate E2 / `n907 P3` / `tiers T3` all name this method. ⛔ Never report the un-refreshed output as drift; pair it with `md5sum`-vs-blob.
