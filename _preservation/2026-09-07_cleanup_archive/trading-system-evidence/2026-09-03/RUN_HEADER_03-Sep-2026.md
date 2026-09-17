# RUN HEADER — GUI deployed-instance sweep, 03-Sep-2026

⭐ **ONE file, ⛔ not two.** 👤 FILE 114 §3: the header spans **two sources** — the
VM knows the process, the browser knows the render. ⭐ Split across two files,
nobody can prove in four days' time that the measurements came from the
restarted process. ⭐ Bound here.

🔴 ⚠️ **THE BINDING IS MANUAL AND IT IS THE WEAK LINK.** ⛔ Nothing in the snippet
can verify which process served it. ⭐ The only protection is **SEQUENCE**:
⭐ confirm the new PID → ⭐ **then** hand over the snippet.
⛔ **Never the reverse** — ⭐ a pre-restart run would look perfect and be void, and
⛔ no later inspection could tell the difference.

---

## A · VM SIDE — 🔬 measured by me over SSH

### A1. PRE-restart state (🔬 measured 03-Sep 12:36:25 IST)
| field | value |
|---|---|
| `gui-dashboard` MainPID | **1019239** |
| `gui-dashboard` start | **Wed 2026-09-02 06:19:53 IST** |
| `gui-dashboard` NRestarts | 0 · ActiveState active |
| bare `refs/heads/main` | **`2d084364b830aca83b6d5cd3f2db21100372f446`** |
| deployed work-tree vs that tree | **0** differing tracked files |
| `trading-system` (must stay untouched) | MainPID **1101999**, start **Thu 2026-09-03 08:15:29 IST**, NRestarts 0 |

⭐ Deploy checkout of `ops_dashboard/` was **02-Sep 23:39:55** ⇒ ⭐ every one of
the **29** changed backend modules postdates PID 1019239's start by **17h20m**.

### A2. POST-restart state — 🟢 **STEP B PASSED** (🔬 measured 03-Sep 13:08:55 IST)
| field | value | gate |
|---|---|---|
| `gui-dashboard` MainPID | **1119981** | ✅ ≠ 1019239 |
| `gui-dashboard` start | **Thu 2026-09-03 13:08:20 IST** | ✅ ≠ Wed 06:19:53 |
| NRestarts · state | 0 · active/running | ✅ clean start, ⛔ no restart loop |
| serving? | 🔬 `/login` **200** (151,803 B) · `/` **302 → /login** | ✅ |
| `trading-system` | **1101999** · Thu 03-Sep **08:15:29** · NRestarts **0** | ✅ **UNTOUCHED** |
| bare `refs/heads/main` | `2d084364b830aca83b6d5cd3f2db21100372f446` | ✅ unchanged |
| deployed tree vs that tree | **0** differing tracked files | ✅ |

🔴 **THE DECISIVE FACT:** 🔬 `services/controls.py` and `readers/control_client.py`
carry mtime **02-Sep 23:39:55**; 🔬 the process started **03-Sep 13:08:20** —
**13h28m later**. ⇒ ⭐ By CPython import semantics this process holds the
**deployed** modules, including the two that **did not exist at `39292d3`**.
⇒ ⭐ And the Jinja cache is **empty**, so every render is a first render off the
deployed tree — ⭐ which is what makes the browse evidence at all.

⭐ **Sequence honoured: PID confirmed FIRST, snippet handed over SECOND.**

---

## B · BROWSER SIDE — from the snippet's own output

| field | value |
|---|---|
| instrument | `gui_sweep_snippet.js` (hash in `SHA256SUMS.txt`) |
| origin | ⏸ from the run |
| browser version | ⏸ from the run |
| host `devicePixelRatio` | ⏸ from the run (⭐ irrelevant to the numbers — the iframe box is the surface, and `innerWidth === requested` is **asserted**) |
| measured viewports | **1920×1080** and **1440×900**, set on the iframe |
| `AUTHENTICATED` | ⏸ ⭐ proven by the run itself (C0), ⛔ not assumed |
| `SELFTEST` | ⏸ must read **PASS** or the run is void |
| C1 DEPLOYED-S02 verdict | ⏸ `COMPARABLE` / `HEIGHT ONLY` / `MORE THAN THE HEIGHT MOVED` |
| C1 magnitudes | ⏸ `Δh = __px · scrollbar = __px · ratio __×` |
| `INTEGRITY` | ⏸ any `⛔LOGINPAGE` / `⛔UNFOCUSED` / error rows |
| scope | ⏸ `STOP_AFTER_C2` true (C0–C2) or false (full) |

⚠️ **Vocabulary note:** the Round-3 instrument does **not** emit
`SCROLLBAR-PLAUSIBLE`. ⭐ That label was removed because a scrollbar is
**certain** at `h=1212` vs a 1080 viewport, which made the opposing branch
algebraically unreachable. ⭐ The verdict now splits on **what moved**, and the
**magnitudes** carry the diagnosis. ⛔ Do not record a label the instrument
cannot produce.

⚠️ **Known hazard in the instrument, ⛔ recorded, ⛔ not fixed today:** the
`window.__GUI_SWEEP_CFG` hook can also override `ROUTES`, `S02_EXPECT`,
`S02_ROUTE` and `VIEWPORTS`. ⭐ The *"TEST CONFIG ACTIVE"* banner only prints when
the caller volunteers `__present: true` ⇒ ⛔ a measurement-affecting override
could run **silently**. ⭐ Using the hook for `STOP_AFTER_C2` alone is scope-only
and safe. ⭐ A future revision should make the banner fire automatically on any
measurement-affecting key. ⛔ Not changed mid-handover — the shipped hash was
already independently verified.

---

## C · ⛔ PROBES TESTED AND REJECTED — ⭐ recorded so they are not re-derived

⭐ 👤 FILE 114 §3: recording what was **tested and rejected** is worth as much as
the result.

1. **`/static/*` md5 comparison** — ⛔ **VACUOUS.**
   🔬 `/static/style.css` and `/static/components.js` returned the **identical**
   md5 `280c34c2ab9b438cdc708195624414bf`, 199 B — 🔬 because both are auth-gated
   and returned the **302 redirect body** (`loc=/login`), ⛔ not the assets.
   ⇒ ⭐ It could not distinguish new from old. ⭐ Cited, then withdrawn.
2. **New-route liveness probe** — ⛔ **VACUOUS.**
   ⭐ Since `services/controls.py` is a **wholly new file** (ABSENT at `39292d3`),
   hitting a `2d08436`-only route looked like a credential-free backend test.
   🔬 `/api/controls-summary` (**both** builds), `/api/analytics/slippage`
   (**new only**) and `/api/definitely-not-a-route-xyz` (**neither**) **all
   return `401`** — ⭐ auth answers before routing resolves.
   ⇒ 🔴 ⭐ **No credential-free backend-liveness probe exists.** ⭐ Killed by its own
   negative control **before** it produced a number.
3. ⇒ ⭐ **The PID + start-time check IS the instrument** for deploy-liveness, and
   ⭐ it is sufficient: ⭐ CPython imports a module once per process, ⭐ so a process
   started after **02-Sep 23:39:55** holds the deployed modules.

---

## D · RESULTS — ⏸ written as taken, in three LABELLED tiers

⛔ **Never "Δ = 0 everywhere"** — ⭐ there is no complete *everywhere* to compare
to → `the_gui_delta_has_no_comparand`.

- **TIER 1 — CORROBORATION (new instrument), ⛔ NOT Δ.** ⭐ Presence and order of
  magnitude only. ⭐ **S14: overflow PRESENT and ~tens ⇒ PASS**; ⛔ absent ⇒
  investigate the measurement, ⛔ do not celebrate. ⭐ Plus S17, S16, S06, S07.
- **TIER 2 — Δ vs a STALE 19-Aug baseline** (1920 only, 3 metrics, different
  instrument). ⭐ **Drift EXPECTED on the 7 freeze screens**
  (S11·S16·S17·S18·S19·S20·S21) — ⭐ report, ⛔ interpret nothing.
  ⭐ Each remaining screen carries its **churn figure**.

  🔴 **COUNT — ⛔ keep these two apart, ⛔ never merge them:**
  | | |
  |---|---|
  | the **historical campaign** | **22 screens** approved; **21** of them table-bearing (⭐ S01 has no table) |
  | the **19-Aug baseline table** | **22 rows**, S01 included (h=1080 · ovf=no · <13px=**2**) |
  | **this sweep** | 🔬 **21 routes** — ⭐ the 22 **minus S01** |
  ⭐ **Why S01 is excluded:** ⭐ `/login` is the unauthenticated standalone page;
  ⭐ inside an authenticated session it ⛔ does not render, and a route that
  redirects would be flagged `⛔LOGINPAGE`. ⇒ ⭐ It is measured by 👤 Rama's eye,
  ⛔ not by this instrument.
  ⇒ ⛔ **Never write "22 screens verified" from a 21-route sweep.**
- **TIER 3 — FIRST MEASUREMENT, ⛔ no baseline exists.** ⭐ All clipped-cell
  counts, and 1440×900 for every screen but four. ⛔ Never call these a Δ.

⭐ Wording for the gap, 👤 FILE 113 §4: *"the historical campaign validation is
**not independently reproducible** from the repository today."*
⛔ **NOT** *"the campaign was invalid"*; ⛔ **NOT** *"the measurements were false."*
