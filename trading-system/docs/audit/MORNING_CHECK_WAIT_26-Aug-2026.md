# MORNING CHECK WAIT — 26-Aug-2026 · PC-only, zero VM blast radius

**Change: `deploy/zerodha_morning.ps1` wait lengthened 15s → 45s.** ⛔ `token_watcher.sh` on the VM was NOT touched — the 30s poll interval is unchanged. ⛔ Nothing pushed; this file is PC-side and outside the deploy path.

---

## 1 — EXISTING STATE

**Anti-duplication check, done before reading or editing anything:** `zerodha_morning.ps1` exists in **7 locations** on this PC:

| location | md5 |
|---|---|
| `D:/Projects/trading-system` (ROOT) | `841a376fea5f4d7ff4a729717433690f` |
| `D:/Projects/trading-system-controlplane` | `841a376fea5f4d7ff4a729717433690f` |
| `D:/Projects/trading-system-gui09` | `841a376fea5f4d7ff4a729717433690f` |
| `D:/Projects/trading-system-main` | `841a376fea5f4d7ff4a729717433690f` |
| `D:/Projects/trading-system-n907` | `841a376fea5f4d7ff4a729717433690f` |
| `D:/Projects/trading-system-tiers` | `841a376fea5f4d7ff4a729717433690f` |

⚠️ **These are not independent scripts that could disagree with each other** — they are byte-identical git-worktree checkouts of the same file, present because each of the five other unpushed units (FILE 2 M10: `tiers`, `controlplane`, `main`, `gui09`, plus `n907`) lives in its own worktree, and a worktree checks out the *entire* tree. `PATHS.md` and `docs/SYSTEM_MAP.md` name no canonical path for this script, and a `schtasks` sweep found **no Windows Scheduled Task** referencing any of them — it is run manually, and the only sensible invocation point is the ROOT project directory. **⇒ Only the ROOT copy was edited.** The five sibling copies now diverge until their unit is refitted (M10); that refit should carry this one-line change forward rather than re-derive it.

**File read end-to-end** (`deploy/zerodha_morning.ps1`, 104 lines before edit). The wait value appears **three times**, tied to one mechanism:

* Header comment, `:10` — `#   4. Wait 15 seconds for the VM token-watcher to detect it`
* Display text, `:76` — `Write-Host "[..] Waiting 15s for VM to detect new token..."`
* The actual value, `:77` — `Start-Sleep -Seconds 15`

⛔ **No retry loop exists anywhere in the file** — a straight-line script: check token → (login if needed) → SCP → wait once → check once → report.

---

## 2 — ROOT CAUSE

The stated premise — token_watcher polls every 30s, the script waits 15s — was **confirmed from source, not assumed**: `token_watcher.sh:22` on the VM reads `SLEEP_SEC="${SLEEP_SEC:-30}"` (the `LONG_SLEEP=300` at `:23` is a distinct back-off path for HALT/startup-fail cases, not the normal cadence). The PC's SCP write and the VM's poll loop are **not synchronised** — the moment the token lands on the VM can fall anywhere in token_watcher's 30s cycle, so in the worst case up to just under 30s can elapse before token_watcher even notices the new file, before it can issue `systemctl start` and before that reaches `active`. A 15s wait therefore samples `systemctl is-active` **before** a full poll cycle has necessarily turned even once, so on a genuinely healthy morning the check can read the service as not-yet-active and report RED — the script was faster than the thing it was measuring. Lengthening to 45s guarantees the wait spans one full 30s cycle plus a 15s margin for the subsequent `systemctl start` → `active` transition and the SSH round-trip, without touching the VM-side interval that is the actual source of the delay.

---

## 3 — THE CHANGE

```diff
--- a/deploy/zerodha_morning.ps1
+++ b/deploy/zerodha_morning.ps1
@@ -7,7 +7,7 @@
 #   1. Check if zerodha_token.json exists and is not expired (created today)
 #   2. If expired or missing -> run zerodha_login.py (opens browser for TOTP)
 #   3. SCP the fresh token file to the VM
-#   4. Wait 15 seconds for the VM token-watcher to detect it
+#   4. Wait 45 seconds for the VM token-watcher to detect it (30s poll + 15s margin)
 #   5. SSH to verify the trading-system systemd service is active
 #   6. Report success or failure with next steps

@@ -73,8 +73,10 @@ if ($LASTEXITCODE -ne 0) {
 Write-Host "[OK] Token copied to VM." -ForegroundColor Green

 # Step 4: Wait for VM token-watcher
-Write-Host "[..] Waiting 15s for VM to detect new token..."
-Start-Sleep -Seconds 15
+# VM poll interval is 30s (token_watcher.sh:22, SLEEP_SEC=30); 45s covers one
+# full poll cycle plus a 15s margin, so a healthy morning no longer reads RED.
+Write-Host "[..] Waiting 45s for VM to detect new token (30s poll + 15s margin)..."
+Start-Sleep -Seconds 45

 # Step 5: Check service status
 Write-Host "[..] Checking VM service status..."
```

No second wait was added and no existing wait was stacked (none existed to stack). ⛔ `token_watcher.sh` was not opened for editing. ⛔ No file under `/home/ubuntu/systems/trading-system/` was touched.

**Push status:** `deploy/zerodha_morning.ps1` is tracked in the repo (root worktree, branch `feat/delivery-config-split`). The edit is a local, unpushed change — no push authority exists today, and none is claimed.

---

## 4 — VERIFICATION

**V1 — re-read end-to-end after the edit.** The changed line now reads, at its new position:

```
79:	Start-Sleep -Seconds 45
```
(shifted from `:77` to `:79` by the two comment lines inserted above it at `:76-77`.) Header comment now reads `:10` *"Wait 45 seconds for the VM token-watcher to detect it (30s poll + 15s margin)"*; display text now reads `:78` *"Waiting 45s for VM to detect new token (30s poll + 15s margin)..."*. All three occurrences of the wait value are consistent.

**V2 — run against live VM state.** ⚠️ **Scoped, not the full script.** Running `zerodha_morning.ps1` unmodified would exercise Step 3 (`scp` overwriting the VM's live token file) and, on any token-check anomaly, a real browser TOTP login — both real actions against a VM that is live-trading right now, and both pre-existing, unrelated to today's change. Per the file's own PARITY FIXATION instruction ("if it writes anything to the VM, STOP and report"), that write is disclosed at §"parity" below rather than exercised. Instead, the exact changed mechanism was mirrored:

```powershell
Start-Sleep -Seconds 45
$ServiceStatus = ssh trading-vm "systemctl is-active trading-system" 2>$null
```
**Result: `ServiceStatus='active'`, elapsed `46.2609616` seconds.** (45s sleep + ~1.26s SSH round-trip.)

**V3 — diff confirms nothing else changed.** Shown in full at §3 above — two hunks, both confined to the wait value and its accompanying comment/display text.

**V4 — stated plainly: this is a smoke test, not proof.** The service was already `active` for hours at the moment of this test (boot proven at 08:15 today, per FILE 1/FILE 2 of this session); `systemctl is-active` would have returned `active` under a 15s wait, a 45s wait, or no wait at all, because there was no cold-boot race to lose. **The mechanism this change fixes only contends during a genuine cold boot**, when token_watcher must both *detect* a brand-new token and *start* the service from a stopped state. **The real proof is tomorrow's 08:15 (27-Aug-2026) run.**

---

## 5 — PARITY / BLAST-RADIUS DISCLOSURE

The two elements that changed — the wait (`Start-Sleep`, purely local) and the check that follows it (`ssh … systemctl is-active`, read-only) — are both confirmed non-writing against the VM. ⚠️ **The script as a whole is not purely read-only**: Step 3 performs `scp $TokenFile $VMTokenDest`, writing `data_store/session/zerodha_token.json` on the VM. This write **pre-exists** this change, was not modified, and was not exercised in V2's smoke test (which started after Step 3 in the script's own sequence). Flagged here rather than silently run or silently omitted.

---

## 6 — WHAT WAS NOT DONE

* The five sibling worktree copies (`tiers`, `controlplane`, `main`, `gui09`, `n907`) were **not** edited — in scope only for the ROOT worktree today; each owes this same one-line change at its own refit (M10).
* `token_watcher.sh` and the VM's 30s poll interval were **not** touched.
* No push was made; no push authority exists today.
* The full `zerodha_morning.ps1` (including its SCP write and potential login flow) was **not** run end-to-end against the live VM — only the changed wait+check was smoke-tested.
* Tomorrow's 08:15 boot has **not** happened yet — the fix is unverified against the actual race condition it addresses.
