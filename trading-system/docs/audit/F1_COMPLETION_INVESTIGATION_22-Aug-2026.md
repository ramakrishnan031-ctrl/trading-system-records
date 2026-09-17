# F1 COMPLETION — INVESTIGATION

**22-Aug-2026, 14:15 card.** Everything measured at `4568385` (deployed) unless a line says `d00e574` (built). No code, no config edit, no test written, nothing pushed. `R` = **₹10,587.00**, the measured live capital.

---

# Q1 — WHY A GLOBAL `risk_per_trade` WHEN EVERY STRATEGY OWNS ITS SL

## A · The formula, with the code

```
signal_processor.py:1669   sl_price   = entry × (1 − sl_pct)        ← STRATEGY owns sl_pct
position_sizer.py:349      sl_distance = |entry − sl_price| = entry × sl_pct
position_sizer.py:381      risk_rs     = total_capital × risk_per_trade_pct   ← CONFIG owns this
position_sizer.py:382      qty_by_risk = floor(risk_rs / sl_distance)
```

In one line:

```
qty_by_risk = floor( capital × risk_pct  /  (entry × sl_pct) )
```

The strategy's number is in the **denominator**. The config's number is in the **numerator**. They multiply through, they don't compete.

## B · What each one is

- **`sl_pct` (strategy) = WHERE the stop sits.** A price distance. It says "get out if it moves 1% against me."
- **`risk_per_trade_pct` (config) = HOW MUCH may be lost.** A rupee budget. It says "whatever happens, ₹105.87."

A stop tells you the exit price. It tells you nothing about how many shares to buy. The budget divided by the stop distance is what turns one into the other.

## C · What happens if the global is removed

Two possible readings, both worked:

- **If `risk_rs` is zeroed** → `qty_by_risk = 0` → `raw_qty = min(0, …) = 0` → **every trade rejected.** The system stops trading.
- **If the rung is dropped** → `raw_qty = min(qty_by_capital, qty_by_concentration)`.

**For the second reading, the honest answer is: today, nothing changes.**

The risk rung binds only when it is the smallest of the three. Algebraically:

```
qty_by_risk < qty_by_concentration
⟺ risk_pct / sl_pct < conc_pct
⟺ sl_pct > risk_pct / conc_pct = 0.01 / 0.10 = 10%
```

**The risk budget binds if and only if the stop is wider than 10%.** Run on the real deployed sizer:

| stop | sl distance | qty_by_risk | qty_by_conc | qty_by_capital | what binds | final qty |
|---|---|---|---|---|---|---|
| 1% | ₹1.00 | 105 | 10 | 370 | CONCENTRATION | 10 |
| 5% | ₹5.00 | 21 | 10 | 370 | CONCENTRATION | 10 |
| **10%** | ₹10.00 | **10** | **10** | 370 | RISK (tie) | 10 |
| 15% | ₹15.00 | 7 | 10 | 370 | **RISK** | 7 |
| 20% | ₹20.00 | 5 | 10 | 370 | **RISK** | 5 |

**The widest stop any strategy is allowed to take is `sl_max_pct` = 5% intraday, 8% positional.** Both are below 10%. That is why `position_sizer.py:434` carries the comment *"the risk-per-trade term actually bound a size — algebraically never today"*, and why the record shows **zero `REJECTED_SIZING_RISK`** and `binding_constraint = concentration` on every measured trade.

### The three CNC trades — and this answer needs no entry prices

All three delivery trades ran a positional strategy, and all three positional strategies carry `sl_pct: 0.02`. At a 2% stop:

```
qty_by_risk / qty_by_concentration = (risk_pct / sl_pct) / conc_pct = (0.01/0.02)/0.10 = 5.0
```

So the risk rung sat at **5× the concentration rung** on all three. Using the recorded risk quantities:

| trade | sl distance | qty_by_risk (recorded) | qty_by_conc = ⌊21.174 / sl_dist⌋ | binds |
|---|---|---|---|---|
| CLSEL | 5.78 | 18 | **3** | CONCENTRATION |
| MANINDS | 14.46 | 7 | **1** | CONCENTRATION |
| KRONOX | 4.11 | 25 | **5** | CONCENTRATION |

**Removing the risk budget would not have changed one share on any of the three.**

⚠️ **But "it never binds today" is not "it does nothing".** It is a backstop with a precise trigger: a stop wider than 10%. Today `sl_max_pct` prevents any strategy reaching that. Remove the budget and the only thing standing between you and an unbounded loss-per-trade is `sl_max_pct` — one number in sixteen files, instead of two independent limits.

## D · The question behind the question — sizing with no risk budget at all

Two stocks, both at ₹100, same rupees deployed (concentration cap, ₹1,058.70 → 10 shares each):

| | stop | shares | rupees deployed | **loss if stopped** |
|---|---|---|---|---|
| Stock A | 1% | 10 | ₹1,000 | **₹10** |
| Stock B | 10% | 10 | ₹1,000 | **₹100** |
| Stock C | 20% | 10 | ₹1,000 | **₹200** |

**Same money in. Twenty times the loss out.** Position value tells you what you spent. It tells you nothing about what you can lose.

With the risk budget in place, Stock C is cut to 5 shares and loses ₹100 — the budget, not the price. **That is the whole answer: the budget makes the loss the same regardless of how wide the stop is. Without it, the loss scales with the stop width and nothing caps it.**

## E · Would a per-strategy risk budget be coherent? (description only — not a proposal)

Yes, it would be coherent. It would mean each strategy carries its own rupee budget instead of sharing one: a high-conviction strategy could risk ₹200 a trade while a weaker one risks ₹50, and the stop width would still divide it.

Two things would have to come with it, stated so the shape is honest:

1. **A portfolio ceiling.** Today one number times `max_open_positions` gives the worst case: 5 × 1% = 5% of capital at risk at once, against a 3% daily loss limit. The config auditor's `C5` check already warns when `risk_pct × max_open > 2 × daily_loss`. With sixteen different budgets that check has to become a sum over whatever combination is open, which is a different kind of check.
2. **A decision about who owns the number.** Today the strategy owns the stop and the config owns the budget, and they are separately reviewable. Merging both into the strategy file means one file can change both, and a wider stop plus a bigger budget compounds.

⛔ Not proposed, not designed, not to be built.

---

# Q2 — EVERY SETTING THAT AFFECTS ORDER SIZE OR CAPITAL

`%` = a fraction, computed against a base. `INR` / `count` = an absolute, used as-is. Timing settings excluded as asked.

### The ones that decide quantity

| setting | MIS | GTT | unit | what it limits | read at | binds today? | ₹ at R = 10,587 |
|---|---|---|---|---|---|---|---|
| **`max_concentration_pct`** | 0.10 | 0.10 *(`d00e574` `delivery_max_concentration_pct`; at `4568385` **no delivery key — it borrowed MIS's**)* | % | notional in one symbol | `position_sizer.py:423-425` | 🔴 **YES — this is the one that decides. Concentration bound 15 of 15 trades** | **₹1,058.70 per scrip** |
| `risk_per_trade_pct` | 0.01 | 0.01 *(`d00e574`; `null` at `4568385`)* | % | rupees at risk per trade | `:381` | **NO** — needs a stop wider than 10%; max allowed is 5% / 8% | ₹105.87 |
| `max_position_value_pct` | 0.40 | 0.40 *(`d00e574`; `null` at `4568385`)* | % | notional backstop | `:585` | **NO** — 4× above the concentration ceiling | ₹4,234.80 |
| `leverage_map` | INTRADAY 5.0 · CO 6.0 · BO 5.0 | DELIVERY 1.0 | multiple | margin per share = price ÷ leverage | `:313` static, `:316` **live broker margin overrides it** | **YES** — sets `qty_by_capital` | MIS margin ₹20/share at ₹100; GTT ₹100 |
| `intraday_bucket_pct` / `positional_bucket_pct` | 0.70 | 0.30 | % | the purse each book may spend | `fund_manager.py:2334-2335` | **YES** — caps `qty_by_capital` | MIS ₹7,410.90 · GTT ₹3,176.10 |
| `tier_multipliers` | HIGH 1.0 · MED 0.70 · LOW 0.50 | same | multiple | scales the winning rung | `position_sizer.py:524` | **YES** whenever the tier is MEDIUM or LOW | −30% / −50% |
| `min_multiplier` / `max_multiplier` | 0.5 / 2.0 | same | multiple | performance weight bounds | `:527` | ⛔ **NO — INERT.** `perf_weights` is never passed to `SignalProcessor`, so the weight is always 1.0 | — |
| `dynamic_by_winrate` | true | true | bool | — | `main.py:2532` **log line only** | ⛔ **NO — gates nothing** | — |
| `entry_offset_pct` *(per strategy)* | 0.001 | 0.002 | % | raises the price margin is charged on | `position_sizer.py:417` | **YES**, marginally | +0.1% / +0.2% margin |
| `sl_gap_buffer_pct` *(4 gap strategies)* | 0.3 | — | ⚠️ **PERCENT, not a fraction** — the code divides by 100 (`signal_processor.py:1715`) | widens the stop 09:15–09:30 → smaller qty | `:1709-1720` | **YES**, in that window only | a 1% stop becomes 1.297% ⇒ ~23% fewer shares on the risk rung |

### The ones that reject rather than size

| setting | MIS | GTT | unit | effect | read at | binds today? |
|---|---|---|---|---|---|---|
| `max_open_positions` | 5 | 5 *(portfolio-wide, counts delivery too)* | count | 🔴 **the real ceiling**: 5 × ₹1,058.70 = **₹5,293.50 max deployed** | `risk_engine.py` OPEN_POSITIONS | **YES** |
| `max_daily_trades` | 10 | — | count | entries per day | DAILY_TRADES | rarely |
| `max_open_delivery_positions` | — | 3 | count | concurrent CNC | `risk_engine.py:469` | ⚠️ hit exactly 3-of-3 once, 12-Aug |
| `max_daily_delivery_trades` | — | 5 | count | CNC entries/day | `:553` | no |
| `max_concurrent_positions` *(per strategy)* | 2 (nine) · 3 (four) | 2 (all three) | count | per-strategy cap | gate layer | sometimes |
| `max_consecutive_losses` | 4 | 4 *(shared, no delivery twin)* | count | halts entries | CONSECUTIVE_LOSSES | rarely |
| `max_sector_exposure_pct` | 0.40 | 0.40 *(`d00e574`; **no key** at `4568385`)* | % | margin per sector | `risk_engine.py:638` | ⛔ **NO** — `sector_cap_mode: observe`, logs only | ₹4,234.80 |
| `daily_loss_limit_pct` | 0.03 | 0.03 *(`d00e574`; **no key** at `4568385`)* | % | day loss, **three enforcement points** | `risk_engine.py:593` · `fund_manager.py:1347` · `system_manager.py:262` | not yet | ₹317.61 |
| `min_qty_threshold` | 1 | 1 | count | reject below | `position_sizer.py:616` | at tiny sizes |
| `max_single_order_qty` | 10000 | 10000 | count | explosion guard | `:386` | never |
| **`min_tick_size`** | **0.05** | **0.05** | 🔴 **INR — absolute** | reject if stop distance < 5 paise | `:354` | never at current prices |
| `lot_skew_rejection_threshold` | 0.25 | 0.25 | % | lot-rounding skew | `:560` | **never** — `lot_size = 1` for equity, so the check is skipped |
| `min_depth_qty` | 500 | 500 | count | order-book depth gate | entry gate | sometimes |
| `min_effective_rr` | 1.0 | 1.0 | ratio | abort if R:R < 1 after slippage | entry gate | sometimes |

### The ones that move rupees without changing quantity

| setting | value | unit | effect |
|---|---|---|---|
| `slm_margin_buffer_pct` | 0.05 | % | 5% extra margin **reserved** for an SL-M leg — reduces what is left for the next trade |
| `sl_limit_offset_pct` | 0.005 | % | MIS stop-limit offset — affects fill price, not size |
| `gtt_sl_limit_offset_pct` | 0.03 | % | GTT stop-limit offset (deeper, for overnight gaps) |
| `emergency_exit_buffer_pct` | 0.01 | % | marketable-limit band on kill exits |
| `flat_value_rs` | **absent** | 🔴 **INR** | the alternative sizing mode. `position_sizing.enabled: true`, so it is off. If ever turned on it would be an absolute rupee figure per order |
| `conditional_allocation_enabled` | false | bool | if true, the 70/30 split changes with which books are active |

### 🔴 The one-line answer to "which one decides"

**Concentration.** `0.10 × R = ₹1,058.70 per scrip`, and with `max_open_positions: 5` the whole system can deploy at most **₹5,293.50** — about **14%** of what the MIS bucket could actually support at 5× leverage. Risk-per-trade and position-value never get a vote; sector and daily-loss are switched to observe or not yet reached.

---

# Q3 — CAN THE CONFIG-REJECTION SEND TELEGRAM AND EMAIL?

## The short answer, up front

**Yes. Both. And there is already a working example of exactly this in the boot path.** There is no chicken-and-egg — I expected one and it isn't there.

**But I found something else while tracing it, and it matters more than the alert.**

## 🔴 The thing I did not expect — systemd will restart it every 10 seconds, forever

`deploy/systemd/trading-system.service`:

```
Restart=on-failure
RestartSec=10
RestartPreventExitStatus=3 4
```

**Exit 5 is not in that list.** The unit's own comments explain that 3 and 4 were added *"otherwise systemd hammer-restarts on the same SOFT_KILL; 18-Jun crash-loop"* — the exact problem — but exit 5 was never added.

So a rejected config does not stop the system cleanly. It restarts every 10 seconds, fails identically, and writes another CRITICAL line each time.

`token_watcher.sh` then adds a second restarter: exit 5 falls into its `1|2|*)` branch (`:168`), which restarts up to `MAX_CRASH_PER_HOUR = 3` per hour and then sends a Telegram. Two independent things are restarting the same failing service.

⚠️ **This is pre-existing** — exit 5 exists at `4568385` today. What F1 changes is how *reachable* it becomes: five new required keys are five new ways to land on it. **F1 does not create the crash-loop; it makes the door to it much wider.**

⛔ What I have **not** measured: whether systemd's default start-rate limiter eventually gives up. That depends on `DefaultStartLimitIntervalSec` / `Burst` on the VM, which I did not read. With `RestartSec=10` and the usual defaults (5 starts per 10s), one start every 10 seconds stays under the limit — so my expectation is that it loops indefinitely, but **that is reasoning, not a measurement.**

## A · What is initialised at the moment of rejection

```
main.py:1839   setup_logging(Path("logs"))      ← logging is up
main.py:1840   _log = get_logger("main")
main.py:1844   acquire_instance_lock()
main.py:1849   → _main_locked(args, config_dir)
main.py:1859        app_config = load_all(config_dir)   ← FAILS HERE
main.py:1861        _log.critical("Config load failed: …")
main.py:1862        return 5
```

Logging is fully initialised. The notifier is **not yet constructed** — but nothing stops it being constructed at that point.

## B · The chicken-and-egg — it does not exist

I checked whether the notifier's credentials come from the config that just failed. **They do not.**

- `TelegramNotifier.from_env` (`alerts/telegram_notifier.py:288-289`) reads **`TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHANNEL_PRIMARY` from environment variables**.
- The service gets them from `EnvironmentFile=/home/ubuntu/systems/trading-system/.env` — a different file entirely.
- The only config it touches is the on/off switch, `_read_telegram_enabled` (`:81-102`), which uses raw `yaml.safe_load` — **not the schema** — and its own docstring says *"FAIL-OPEN: any error (missing file, parse error, missing key) returns True."*

And a schema rejection is not a parse failure: the YAML still parses fine, it just fails validation. The switch reads correctly either way.

**⇒ The notifier works at the exact moment the config is rejected.**

## The precedent — this has already been built once

`main.py:285` — **`_alert_invalid_strategy_configs`**. Its docstring:

> *"Fire ONE loud Telegram + email alert naming every strategy YAML that failed to load/validate … Called from the startup-checks abort path BEFORE the boot returns. The boot STILL fails — a broken strategy set must not run — but this tells Rama LOUDLY and specifically WHY the system won't start, naming each file + reason instead of burying it in one log line."*

Written 18-Jul-2026 for a *different* config-abort path. It uses `TelegramNotifier.from_env` for Telegram and `write_critical_sentinel` for the email — the sentinel is a `.flag` file the separate long-running **alert-watcher** service picks up and emails, so the email survives the trading service dying.

**The pattern you want already exists, is deployed, and works. It just isn't wired to this branch.**

## C · What notices today

| | does it notice? |
|---|---|
| **systemd** | restarts every 10s; writes journal entries; ⛔ sends nothing |
| **`token_watcher.sh`** | ✅ **eventually yes.** After 3 restarts in an hour it calls `alert_once_per_day crash …` → `send_telegram` → *"trading-system crashing (exit 5); restart backoff limit reached. Manual check needed."* |
| ⚠️ but | `clear_alert_flags()` (`:141`) deletes the once-per-day flag whenever the state reads `active` or `activating` — which a restart loop passes through constantly. So the once-per-day guard is defeated and the message may repeat |
| ⚠️ and | the message names **exit 5**, not which key was wrong. You would learn the system is down, not why |
| **alert-watcher** | ⛔ only reacts to sentinel files. It sends nothing unless the boot path writes one |
| **trading-watchman** | ⛔ `BindsTo=trading-system.service` — it stops when trading-system stops |
| **the EOD / morning messages** | their absence, which is a silence |

**⇒ It is not pure silence today, but the alert is late, generic, and repeats.** You would get *"crashing, manual check needed"* after roughly half an hour, with no key name.

## D · What it would take — options, not a choice

| option | what it catches | blast radius |
|---|---|---|
| **1 · Alert from inside the boot path** before `return 5` | **only this failure**, but names the exact key | Smallest. Copies `_alert_invalid_strategy_configs` almost verbatim. Touches `main.py` `_main_locked` only. Proven to work — no config dependency |
| **2 · systemd `OnFailure=`** unit | ⭐ **every** boot failure, and every crash | Needs a new unit file installed on the VM by you. Catches exits this and every future build can produce |
| **3 · Add `5` to `RestartPreventExitStatus`** | stops the loop; doesn't alert by itself | One word in the unit file. ⭐ **Also makes `token_watcher`'s existing exit-code branches work properly**, because the service settles in `failed` instead of cycling through `activating` |
| **4 · A heartbeat that alarms on absence** | ⭐ **every** way the system can fail to run, including ones nobody has thought of | Largest. A separate watcher, external if it is to survive the box |

⭐ **Options 2 and 4 catch far more than this one failure.** Option 1 catches only this, but gives the one thing the others cannot: **the name of the key that was wrong.**

⭐ **Option 3 is worth noticing on its own** — it is one word, it stops a crash-loop, and it repairs an existing mechanism rather than adding one.

## E · Is this F1 work?

**Honest answer: option 1 is arguably F1; options 2, 3 and 4 are not.**

- **Option 1** fires *because of* F1's new rejection, sits in the same function, and is meaningless without F1. If the alert is meant to name the missing delivery key, that string only exists in F1. **A case can be made either way, and it is yours to make.**
- **Options 2 and 3** are **systemd unit files on the VM**. Not Python, not in the gate, deployed by a different mechanism, and they change behaviour for **every** exit code — including ones unrelated to delivery config. That is a different unit.
- **Option 4** is a new service. Clearly separate.

⚠️ **And one thing you should weigh regardless of scope:** if F1 ships without option 3, a config typo produces an infinite restart loop rather than a clean stop. **The fail-closed behaviour you approved is "the system refuses to start". What the unit file actually does today is "the system refuses to start, ten times a minute, until someone notices."** Those are not the same thing, and the difference is one word in a file F1 does not touch.

---

# Q4 — NI-1 … NI-8

## 🔴 NI-4 first, because it is the one that matters

**NI-4 is the same bug F1 just fixed, on two keys F1 did not touch. Leaving it means F1 fixed half of its own defect class.**

`core/config_loader.py:536-537`:

```python
max_open_delivery_positions: int = 3
max_daily_delivery_trades: int = 5
```

These are delivery-scoped risk limits with **silent defaults**. Delete them from `system_config.yaml` and the system boots happily on a hardcoded 3 and 5 — exactly what `delivery_risk_per_trade_pct: null` did before F1, in the same file, for the same book. F1 made five delivery keys required and left these two optional.

**Cost today:** zero, because both keys are present with their intended values. It is a trap, not a live defect.
**Fix:** remove ` = 3` and ` = 5`, add them to the existing validator list. **Two lines.**
**Blast radius:** `tests/unit/test_phase3_delivery_caps_conditional_capital.py` already covers these caps and passes both explicitly, so it would not break. Anything constructing a `RiskConfig` without them would — and F1's gate already found and fixed that class of fixture.
**Can it join F1?** ✅ **YES.** Same file, same block, same schema pattern, same rejection path, same test. If Monday goes wrong you cannot distinguish it from F1 — but that is precisely because **it is the same change**, so the distinction has no diagnostic value.

## The rest

### NI-1 — the SL-direction warning raises instead of warning

**What it is.** When a signal arrives with the stop on the wrong side (a BUY whose stop is *above* the entry), the sizer is supposed to log a warning and carry on. Instead it crashes. The dictionary of extra detail it hands to the logger contains a key called `"msg"`, and Python's logging library reserves that name — it refuses and raises `KeyError`. **The warning destroys itself.**

**Where.** `capital/position_sizer.py:278` and `:284`.

**How found.** Measured. I ran a BUY with the stop above entry against the `4568385` tree and it raised.

**What it costs today — measured, not estimated: nothing, and it cannot fire.** All three production callers are in `signal_processor.py` (`:1001`, `:1940`, `:2262`). The stop is always computed as `entry × (1 − sl_pct)` for a LONG (`:1669`), with `sl_pct` forced positive by the schema; the bounds clamp at `:1684-1703` rebuilds it on the same side; the gap buffer at `:1718` multiplies it down, still below entry. And `side` is derived as `"BUY" if direction in ("LONG","BUY")`. **A BUY's stop is structurally always below entry.** The condition has never occurred and cannot occur from any current path.

⚠️ **The part worth your attention is the test, not the bug.** There are two tests for exactly this path — `test_sl_wrong_side_buy_logs_warning` and `test_sl_wrong_side_sell_logs_warning` — and **both pass**. They pass because they use a fake logger (`test_position_sizer.py:69-88`) whose `warning()` just appends to a list and never builds a real log record. **The defect is fully covered by tests that cannot see it.**

**Fix.** One word at each site: `"msg"` → `"detail"`. Two lines.
**Blast radius.** The two tests would need a real logger, or an assertion on the dict's keys. Nothing else reads those fields.
**Can it join F1?** ⚠️ **YES, but as its own commit.** Same file as F1, so if Monday goes wrong you could not attribute a `position_sizer` problem to one or the other from the outside — but a separate commit makes it a one-command revert.
**New test needed.** One that uses a real `logging.Logger` and asserts the warning is emitted rather than raised — a test that could have gone red.

### NI-2 — the config auditor's ladder check is missing a factor

**What it is.** A startup audit warns if the catastrophic-loss cap (40%) is set tighter than the routine concentration cap (10%), because then the emergency backstop would fire on normal trades. The check compares the two percentages directly — but the actual notional can be multiplied by the tier and performance weights, up to 2×. So `conc 25%` with `posval 40%` passes the check while the real ceiling is 50%, above the backstop.

**Where.** `core/config_auditor.py:414`.
**How found.** Reasoned from the formula, then confirmed against `max_multiplier: 2.0` in config.
**Cost today.** None. The multiplier is stuck at 1.0 because performance weights are never wired in (see NI-5's neighbour finding), and the shipped values are 10/40.
**Fix.** Widen the comparison to include the multiplier, and add the delivery pair the check does not look at at all. ~5 lines.
**Blast radius.** `test_config_auditor.py:293` asserts the current behaviour and would need updating. The auditor runs at boot and only warns.
**Can it join F1?** ⛔ **NO — its own unit.** Different file, different subsystem, and it changes what a boot-time audit says. Perfectly attributable on its own, so there is no reason to hide it inside F1.

### NI-3 — comments that say "inert" about something that is live

**What it is.** Three places say the delivery count caps are *"inert while `force_intraday_only=true`"*. That flag is `false`. The sentence is technically true — "inert while X" when X is false says nothing — but it reads as "don't worry about these".

**Where.** `config/system_config.yaml:214-215`, `capital/risk_engine.py:534` and `:620`.
**How found.** Measured (the flag's value) plus reading.
**Cost today.** Cosmetic — but it is the same reading hazard that hid the original defect for weeks.
**Fix.** Reword three comments. ~6 lines, no behaviour.
**Blast radius.** None. Comments only.
**Can it join F1?** ✅ **YES.** Comment-only changes cannot cause a Monday problem, so attribution is not at stake.

### NI-5 — the sizer's constructor defaults every limit

**What it is.** `PositionSizer` can be built with no risk settings at all and will quietly use 1%, 10% and 40%. `RiskEngine`'s own docstring forbids exactly this for itself — *"RiskEngine takes NO defaults — all caps are required, so a component built without config fails fast rather than running loose."* **The two classes disagree about the same principle.**

**Where.** `capital/position_sizer.py:128-139`.
**How found.** Measured while doing F1.
**Cost today.** None in production — the sizer is built at one site, `main.py:2501`, from validated config. It matters only if new code ever constructs one.
**Fix.** Remove five defaults, update every construction site. **Nine sites in `test_position_sizer.py` alone**, ~20 across the suite.
**Blast radius.** Large-ish and entirely in tests, but it is the same class of churn F1 already absorbed.
**Can it join F1?** ⛔ **NO — its own unit.** Not because it is risky, but because it is a wide mechanical edit across many test files. Mixed into F1 it would make F1's diff much harder to read, and reviewing F1 is the thing protecting Monday.

### NI-6 — the config snapshot hash will change

**What it is.** The system takes a daily fingerprint of the config. Five new keys means a new fingerprint on the first day after F1 deploys. **This is correct behaviour recording a real change**, not drift.
**Where.** `core/config_snapshotter.py`.
**How found.** Measured.
**Cost.** None. Flagged only so nobody reads it as an anomaly.
**Fix.** None needed.
**Can it join F1?** n/a — nothing to build.

### NI-7 — a test file whose name no longer matches its contents

**What it is.** `test_position_sizer_delivery_scaffold.py` used to prove the fallback worked. F1 inverted its assertions to prove the fallback is gone. The word "scaffold" in the filename is now wrong.
**Where.** `tests/unit/test_position_sizer_delivery_scaffold.py`.
**How found.** Deliberate — kept the name so the reversed contract stays traceable, rather than renaming mid-gate and turning the diff into a delete-plus-add.
**Cost.** Cosmetic.
**Fix.** `git mv` plus one import-free rename. 1 line.
**Can it join F1?** ⛔ **NO, and not for safety reasons** — a rename inside the unit being gated makes the gate's own diff harder to read. Do it in any later batch.

### NI-8 — memory files over their line-length budget

**What it is.** The memory palace has a self-check for line length. It currently reports **80 over-budget lines** — measured, not estimated: `MEMORY_BOARD.md` 22, `MEMORY_REFERENCE.md` 1, `MEMORY_ARCHIVE_2026H1.md` 57. `MEMORY.md` itself is clean.
**Where.** Outside the repository entirely.
**How found.** Measured by running the check.
**Cost.** None to the trading system. It is housekeeping.
**Fix.** A compaction pass.
**Can it join F1?** ⛔ **NO — it is not code and not in the repo.**

## The grouping

**The criterion is not size. It is: if Monday goes wrong, can you tell which change caused it?**

| | items | why |
|---|---|---|
| ✅ **SAFE TO BUNDLE INTO F1** | **NI-4** (2 lines) · **NI-3** (comments) | NI-4 is literally the same change on two more keys — same file, same schema block, same rejection path. NI-3 is comments and cannot cause a fault |
| ⚠️ **SAFE BUT ITS OWN COMMIT INSIDE F1** | **NI-1** (2 words) | Same file as F1, so external attribution is impossible either way — but a separate commit makes it a one-command revert. Needs one real-logger test |
| ⛔ **MUST BE ITS OWN UNIT** | **NI-2** · **NI-5** | Different subsystems, cleanly attributable on their own. NI-5 also carries ~20 test edits that would drown F1's diff |
| ⛔ **NOTHING TO BUILD** | **NI-6** · **NI-7** · **NI-8** | A correct behaviour, a rename, and housekeeping outside the repo |

## What F1's gate would need if NI-4, NI-3 and NI-1 were bundled

| for | new test |
|---|---|
| **NI-4** | remove `max_open_delivery_positions` from the config → **startup rejects, naming the key**; same for `max_daily_delivery_trades`; and a valid config still boots. Mirrors F1's existing T-3/T-4 exactly — the parametrised list simply grows from five keys to seven |
| **NI-1** | size a BUY with the stop above entry using a **real `logging.Logger`** → the warning is emitted, no exception. ⭐ It must be a real logger: the two existing tests pass with a fake one and prove nothing |
| **NI-3** | none — the existing comment-sweep test already fails on any surviving false claim, and it goes red at the base tree, so it is not vacuous |

---

# FOUND EN ROUTE

**1 · `sl_gap_buffer_pct` means percent, while every other `_pct` key means a fraction.**
`signal_processor.py:1715` divides it by 100. So `0.3` means 0.3%, not 30%. Everywhere else in the system `0.3` would mean 30%. Four strategies carry it (`gap_fade_long/short`, `gap_go_long/short`) and it is live during 09:15–09:30. Set it to `30` intending 30% and you would get a 30× wider stop. ⛔ Not touched.

**2 · The gap buffer is applied after the bounds check.**
The comment at `:1707` says so deliberately. It means the final stop can exceed `sl_max_pct`. At current values (0.3% on a 1% stop → 1.297%, against a 5% max) it does not. ⛔ Not touched.

**3 · The `token_watcher` once-per-day alert flag is cleared by a restart loop.**
`clear_alert_flags()` runs on `active` or `activating` (`:140-141`). A crash-loop passes through `activating` repeatedly, deleting the flag, so the "once per day" guard does not hold during exactly the scenario it was written for. ⛔ Not touched.
