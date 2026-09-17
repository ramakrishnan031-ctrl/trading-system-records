# PHASE A — RE-VERIFICATION AND CLOSURE
## READ-ONLY · 05-Sep-2026 · **PHASE A CLOSED**

**Repo SHA:** `6d24a83` · **VM:** `trading-vm` · 8 agents, 283 tool calls, all four sections
adversarially re-derived by an independent agent that did not see the original scripts.

| Section | Verdict | Adversarial |
|---|---|---|
| §1.1 — did `pullback_wait_enabled` ever change? | **VERIFIED** | upheld (MINOR) |
| §2 — SL-fraction distribution + stale-cohort delta | **VERIFIED** | upheld (MATERIAL) |
| §2.1 — quote freshness | **VERIFIED** | upheld (MATERIAL) |
| §1 — webhook token mechanism | **VERIFIED** | upheld (MINOR) |

**Zero sections refuted.** Nothing was modified: no code, config, YAML, scanner, commit, push or
restart; `pullback_wait_enabled` was neither flipped nor edited; the webhook secret was never printed,
echoed or rotated.

---

# §1.1 — VERIFIED · four of five probes with passing controls

The standing rule — *a search that cannot go red is not evidence* — was applied to every null.

| Probe | Corpus actually walked | Target | Positive control | Verdict |
|---|---|---|---|---|
| **1** config_snapshots | 48 rows, 741,306 chars | `pullback_wait_enabled` → **0/48** | all 9 top-level keys → **48/48**; `sl_pct`/`min_score`/`entry_offset_pct` → 0/48; `file_hashes` covers 8 top-level YAMLs, **no strategy YAML** | **NULL + CONTROL PASSED** |
| **2** local git pickaxe | 1,739 commits, 21 touching `config/strategies/*.yaml` | 2 commits ever; **16 `+` lines, ZERO `−` lines, ever** | `entry_end_time` **56 `+` / 40 `−`** (real edits, e.g. `−"13:30"` → `+"15:20"`), `sl_pct` 22/6, `min_score` 34/18 | **NULL + CONTROL PASSED** — the pickaxe demonstrably detects a value *edit*, not merely file creation |
| **3** VM bare repo | **1,272 commits** on `main` since 01-Jun (tip `20061b6`) | **6 distinct `config/strategies` trees**, all enumerated file-by-file; identical per-file map on all 15 shared files | same code on varying keys: `tgt_risk_reward` → **3** distinct maps, `min_score` → 3, `enabled` → 3, `max_positions` → 2 | **NULL + CONTROL PASSED** |
| **4** 31 deployed SHAs | 157,875 records parsed, 0 unparseable | 1 signature | `tgt_risk_reward`, `min_score`, `enabled`, `entry_end_time` **also each give exactly 1** | **NULL + CONTROL FAILED → per-key null WITHDRAWN** |
| **5** runtime attribution | 7 log files, 263 distinct FIX-067 events, 94 `trade_created` events | 0 TRUE-cohort attributions | **43/51 perfect partition, zero crossover** | **PASSED AND NON-TAUTOLOGICAL** |

## Probe 4 — the control failed, and that is reported rather than smoothed over

The cause is a **degenerate corpus**: `git rev-parse <sha>:config/strategies` returns the *same tree
object* `1534438c…` for all 31 deployed SHAs, so no key *can* vary there and no control could pass.

The per-key null is withdrawn. It is replaced by a **stronger, self-validating, content-addressed
fact**: all 16 strategy YAMLs are **byte-identical at every deployed SHA** across 13-Jul → 04-Sep.
The same code is shown non-blind by probe 3, where it returned 2–3 distinct maps.

**Extension — the one real hole in a git-only argument, now closed.** Git records what was *pushed*;
the runtime reads the *deployed working tree*, which is hand-editable. MEASURED: 13 of 16 deployed
YAMLs have mtime `2026-07-13 18:33` and md5-match git. The other 3 (the positional strategies) have
mtime `2026-09-04 10:41` and differ from git by **exactly one line each** — `enabled: true` →
`enabled: false  # TEMP 04-Sep-2026 ONLY … REVERT MON 07-Sep`. Their `pullback_wait_enabled: false`
matches git. **The out-of-band edit channel is real, was exercised, and did not touch the flag.**

## Probe 5 — the tautology check, stated because this is the named failure class

The FIX-067 log line carries a **symbol, not a strategy**, and its branch runs only when the flag is
False. So "0 events attributed to a TRUE-cohort strategy" via a naive grep **would be a tautology**.
The test was therefore inverted to one that could have come out the other way: each `trade_created`
record carries `signal_id` → `signals.strategy` (ground truth). Of 94 placements in the corpus:

* **43 preceded by a FIX-067 line — all 43 FALSE-cohort**
* **51 not preceded — all 51 TRUE-cohort**
* Zero crossover; identical at a 10 s and 30 s window.

**The method examined 51 genuine TRUE-cohort placements by the same code path and could have found a
preceding FIX-067 for any of them. It found none.**

A secondary fuzzy join was separately controlled: run against the 94 ground-truth events it produced
48 unique attributions, **48 of 48 correct**, and **24 named a TRUE-cohort strategy** — proving the
join is not blind to the TRUE cohort. Run against the 263 FIX-067 events it produced 93 unique
attributions, **all FALSE-cohort**, and of 170 ambiguous sets **none is all-TRUE**.

⇒ **NO natural experiment exists. The strategy-identity confound stands. No causal claim is made.**

---

# §2 — VERIFIED · and Part 2 lands on a hard, controlled NULL

## Part 1 — nothing moved

All 17 D2 statistics reproduce **to the last reported digit** (N=234; median 0.0460, P90 0.1871,
P95 0.3185; adverse >25% = 8/234 = 3.42%; symmetry 104/101/29, sign test p=0.889), from an
independent re-derivation with its own SQL, inversion and percentile code.

**Two facts derived that were not supplied, and that corroborate the prior population definition:**

* The **N=234 boundary is real and has a cause**: FRESH trades with `created_at >= 2026-07-08` number
  exactly 234. Commit `3f4587f` (07-Jul) is the Wave-5 FIX-067 D1 plumbing fix.
* **Before it, delta is exactly 0.000000 on 83/83 trades** (2026-06-24 → 07-07) — the fresh branch
  silently fell back to stale, exactly as the code comment at HEAD `signal_processor.py:961-971` says.

## Part 2 — the stale cohort is NOT measurable at 1-minute resolution

The proposal was that the stale cohort's delta could be recovered against a pre-placement reference.
**Measured, it cannot.** The reason is structural:

* Chartink fires the webhook **on a 1-minute bar close**, and **648/648 trades place inside the very
  next bar** (median 1.9–2.9 s after receipt).
* Therefore **R1 — the close of the bar strictly before the placement bar — *is* the trigger price
  itself**: identical to the tick in **82.8% of trades in BOTH cohorts**.
* Recovery against the known-true logged delta: **R1 recovers 0.065x; R2 (placement-bar open)
  recovers 0.324x.**

The side-by-side table was produced in full, but the STALE figures (R1 mean 0.0082, R2 mean 0.0294 of
stop) are **floors, not the quantity**, and on the same basis the two cohorts are statistically
indistinguishable (Mann-Whitney **p=0.94** / **p=0.70**) — which is what a floor-vs-floor comparison
must produce and is therefore not evidence of similarity either.

**What IS newly established:** both cohorts have the **same pipeline-latency structure** — bar-lag 0
for 100% of both, STALE if anything marginally faster. That makes the FRESH D2 distribution the best
available estimate for the STALE cohort, and it is now a *reasoned* extrapolation rather than an
unexamined one.

⇒ **A cleaner delta is still not a causal claim.** The treatment remains perfectly collinear with
strategy identity. **Measured delta ≠ measured harm.** No outcome regression was run.

---

# §2.1 — VERIFIED · the two kinds of fresh, separated

| Kind | Status | Basis |
|---|---|---|
| **APPLICATION-FRESH** — the adapter makes a new call rather than returning a memoised value | **DEMONSTRATED** | `_quote_fn` is an unwrapped bound method reaching `kite.quote()` over HTTP; no memoisation on the path; **0 of 37,628 logged calls completed in under 10 ms** |
| **BROKER-MARKET-FRESH** — the returned tick is the latest traded price at the exchange | **NOT DEMONSTRABLE** | Kite returns `timestamp` and `last_trade_time`; kiteconnect 5.1.0 parses both into datetimes; **the adapter silently drops both** and sets `Quote.ts = now_ist()` — the local wall clock |

⇒ This is a **data-observability gap, not evidence that quotes are stale.** Broker-side quote age is
unrecoverable for every historical trade, **in both directions** — it cannot be used to argue quotes
were fresh either. It is not converted into a trading rule here, and no change is recommended.

## Two numbers moved

1. **"zero-move median day volume 3.2x lower, 711k vs 2.28M"** — reproduced **once the definition is
   pinned**, but the prior *wording* was wrong for the number it carried. Read literally ("day volume"
   = all 375 bars) it gives **1,281,521 vs 7,792,188, ratio 6.08x** — and that reading is
   **look-ahead-tainted**, since it sums bars that had not traded when the quote was taken. The prior
   figure was in fact cumulative volume **up to the decision minute**: re-running that way gives
   **709,947 vs 2,307,218, ratio 3.25x**, matching to rounding. The conclusion (zero-move cases are
   genuinely illiquid, not cache hits) is unchanged; the label was wrong.
2. A parser-control was added: the log-duration measurement now reports its matched pattern and a
   non-zero N, so "no fast calls" cannot be an artefact of a parser matching nothing.

---

# §1 — WEBHOOK TOKEN MECHANISM · VERIFIED, with two material additions

Every orchestrator claim re-derived. **One shared 64-character bearer token in the URL query string,
constant-time compared, no HMAC, no IP allow-list, no anti-replay, on plain HTTP bound to
`0.0.0.0:5000`, reached directly from the public internet** (223,481 audited POSTs; `remote_addr` is
the true peer, so nothing proxies it). **Tailscale + HTTPS covers only the GUI on `127.0.0.1:8500` —
the webhook does not share that path.**

| Property | Finding | Reader |
|---|---|---|
| Comparison | **Constant-time** `_hmac.compare_digest` — not `==` | `webhook_receiver.py` auth decision |
| `require_hmac` (deployed) | **`false`** ⇒ the `?token=` param IS the live auth surface | deployed `system_config.yaml:336` |
| Bind | `0.0.0.0` at `:328`; its own comment says the bind "relies on `require_hmac=true` plus firewall restrictions" — **precondition not met** | deployed `:328-335` |
| Scope | **One shared secret**, 64 chars, env `WEBHOOK_SECRET` — not per-scanner | `main.py:3083` (HEAD) / `:3373` (deployed) |
| Rotation | **Requires a restart** — read once at startup, config is load-once (`core/config_loader.py:38`, "Does not support hot reload") | — |
| Push safety | **`.env` is gitignored and untracked ⇒ a push cannot revert the token** | `.gitignore:6` |
| Rate limit | Per-IP token bucket, burst 60, refill 5/s → 429 | `:463-473` |

## Addition 1 — the deployed receiver is NOT HEAD

The deployed `webhook_receiver.py` is the **pre-two-pipeline-split file (45-line diff)**. Consequence:
the **live edge enforces a hard 600 s signal-age gate**, whereas HEAD `6d24a83` would compute
`expiry=None` — i.e. **no edge age gate at all**. Anyone reasoning about the live auth surface from
HEAD is reading the wrong file.

## Addition 2 — the 300 s dedup is NOT anti-replay, and a replay is accepted

`dedup_window_seconds: 300` is **duplicate-SIGNAL dedup**, keyed on `(symbol, scanner)` plus
`sha256(scanner|symbol|epoch_bucket(triggered_at))`. It is not auth replay protection.

**And it fails as replay protection for a specific measured reason:** Chartink's `triggered_at` is
**time-only** (`"2:59 pm"` — measured in the stored payload), so the receiver **re-dates it to today**.
⇒ **A captured POST replayed at the same wall-clock time on a later day is accepted as fresh.**

## Blast radius — bounded, and measured

A leaked token buys the ability to **inject an arbitrary Chartink-shaped signal**. It does **not** buy
a chosen price, a chosen size, or an unbounded number of orders. The full gate chain from accepted
POST to live order, in execution order:

| # | Gate |
|---|---|
| 1–3 | shutdown flag → 503 · per-IP bucket → 429 · **AUTH → 401** |
| 4–5 | unknown scanner → 404 (only the 16 mapped names) · `eod` type → watchlist only, **structurally never enqueued** |
| 6–8 | kill switch → 403 · queue backpressure (300 × 0.80) → 503 · **entry window 10:00–15:00 IST, trading days only** → 403 |
| 9–10 | JSON shape / `scan_name` must match the path / numeric casts → 400 · `excluded_symbols` |
| 11 | **age > 600 s → EXPIRED** · in-flight claim · TTLCache duplicate · DB UNIQUE |
| 13–14 | processor re-checks kill switch, window, age · `scan_webhook_map` → strategy |
| 15 | **`strategy_will_trade` — 12 of 16 currently `enabled: true`; the 3 positional/CNC + pb01 are `false` ⇒ a leaked token cannot open a delivery/overnight position today** |
| 16–17 | per-strategy entry window (narrower) · strategy circuit breaker |
| 18 | **secondary screener — live market data, scored against `min_pass_score: 60`** (which independently rejects 91.92% of real signals) |
| 19 | sizer: `max_single_order_qty 10000`, `max_concentration_pct 0.10`, `max_position_value_pct 0.40` |
| 20 | `RiskEngine.approve` — 10 checks: kill switch, sizing, capital, open positions, … |

## Rotation — the risk list

Rotation is a **coordinated change across 16 Chartink alerts and the system**, and a half-done
rotation fails **silently**: an alert left on the old token gets a 401 and simply goes quiet. That
failure mode is already on this week's record — *"nothing traded" is not a quiet day.*

Two things must be re-checked after the restart that a rotation requires, because the deploy
post-receive hook runs `checkout -f main` **and** replaces the whole crontab:
* the **3 TEMP-disabled delivery YAMLs** (currently `enabled: false`, owed a revert Mon 07-Sep)
* the **Monday cron entry**

The token itself is safe from that hook — `.env` is untracked.

---

# PHASE A IS CLOSED

All three re-verifications reproduce with passing controls; the one failed control is reported,
its null withdrawn, and replaced by a stronger measurement. Nothing was modified.

**What Phase A did not establish, restated:**
1. Any causal harm from stale pricing — no natural experiment exists; the confound is total.
2. The STALE cohort's true staleness — **not merely unlogged but unmeasurable at 1-minute resolution**.
3. Broker-side quote age — supplied by Kite, discarded by the adapter, unrecoverable in both directions.
4. Whether the Chartink RANGE BREAKOUT scanners were ever edited — only their current state was read.

**No Phase B has begun. No recommendations are made. Rama authorises Phase B separately.**

*Still outstanding and unrelated: the `/controls` AFTER liveness read and its bracket verdict.*
