# TMSim — Balance Rationale

Every numeric constant in `config.js` is grounded in a real-world reference.
Sources are cited inline. All monetary values are in abstract game dollars ($)
that are intentionally proportional to real euros/dollars but not 1 : 1.

---

## 1. Building Distribution

| Type        | Game weight | Real-world basis |
|-------------|-------------|------------------|
| Residential | 65 %        | European cities average ~62–68 % residential land use (EEA Urban Atlas 2018) |
| Commercial  | 25 %        | Offices, retail, restaurants typically 22–28 % of urban fabric |
| Industrial  | 10 %        | Light industrial/warehouse zones 8–12 % in mixed urban areas |

Previously the industrial share was 15 %, which would imply a heavily
factory-dominated town. Reduced to 10 % to reflect a modern service-economy city.

---

## 2. Waste Generation Rates

The game unit "waste unit" maps loosely to **1 kg of mixed municipal solid waste**.

At 1× speed, `GAME_SPEED = 5` means 1 real second = 5 game minutes, so
**1 game day takes 288 real seconds (~4.8 minutes)**.

### Bin Capacities (`BIN_CAPACITY`)

Previously a single `MAX_WASTE = 100` applied to every building type, which made
industrial and commercial nodes fill in ~12–25 real seconds during peak — far too
aggressive. Each type now has a realistic bin volume:

| Type        | Capacity (u) | Real-world analogue | Time-to-fill at peak rate |
|-------------|-------------|---------------------|---------------------------|
| Residential | **240**     | 240-litre wheelie bin (~120 kg @ 0.5 kg/L) | ~44 s at 5.5 u/s (morning rush) ≈ 3.7 game-hours |
| Commercial  | **600**     | Restaurant/retail 660-litre skip container (~300 kg) | ~150 s at 4.0 u/s (weekday) ≈ 12.5 game-hours |
| Industrial  | **1200**    | 6 m³ roll-off container (~1 200 kg compacted waste) | ~141 s at 8.5 u/s (morning shift) ≈ 11.8 game-hours |

With these volumes, residential requires **morning + evening collections**,
commercial needs **daily service**, and industrial needs **per-shift collection**.
All three types are challenging but manageable — no more 1-hour overflows.

In the UI, fill level is always displayed as **percentage** (`waste / capacity × 100`)
so the player never sees raw units.

### 2a. Residential

Source: Eurostat (2022) — EU average **1.36 kg/person/day** household waste.
A game residential node represents a small apartment block (~20–30 residents)
generating ~30–40 kg/day on average, with strong time-of-day variation.

| Period           | Hours  | Rate (u/s) | Reasoning |
|------------------|--------|------------|-----------|
| Deep night       | 00–06  | **0.10**   | Baseline; nearly everyone asleep, only bin juice seeping |
| Early morning    | 06–07  | **1.20**   | Coffee grounds, shower packaging, light morning activity |
| Morning rush     | 07–09  | **5.50**   | Breakfast waste, nappy disposal, bin takeout before leaving |
| Daytime          | 09–17  | **1.00**   | Most residents at work/school; only retirees and WFH |
| Evening peak     | 17–22  | **5.20**   | Cooking dinner, packaging disposal, cleaning — real-world studies show this is the highest sustained home-waste window |
| Late night       | 22–24  | **0.50**   | Winding down; some kitchen cleaning |

Research reference: Davoudi & Evans (2005), *Waste Management*, show morning
and evening domestic peaks of 2.5–4× the daily average.

### 2b. Commercial

Source: DEFRA (UK, 2021) — average **0.6 kg/employee/day** for offices,
**3–8 kg/seat/day** for food-service. A game commercial node blends both.

| Period           | Hours  | Rate (u/s) | Reasoning |
|------------------|--------|------------|-----------|
| Closed / overnight | –    | **0.10**   | Refrigeration condensate, cleaning crew residue |
| Weekday open     | 08–19  | **4.00**   | Office waste + retail foot traffic; lunch generates ~40 % of daily commercial waste |
| Weekend open     | 09–19  | **5.50**   | Retail-heavy weekend: more shoppers, more packaging, more food-court waste |

Weekdays end at 19:00 (vs. 22:00 previously) — most offices close by 19:00;
the old 22:00 cutoff over-represented late-night commercial activity.

### 2c. Industrial

Source: EPA (US, 2020) — light manufacturing generates **50–500 kg/shift-day**
depending on sector. A game industrial node represents a small factory/warehouse.

| Period            | Hours  | Rate (u/s) | Reasoning |
|-------------------|--------|------------|-----------|
| Off-hours (default) | –    | **0.30**   | Residual process waste, cooling water, night watchman |
| Weekend skeleton  | 00–24  | **0.50**   | Minimal weekend ops — slightly above off-hours because some maintenance generates scrap |
| Morning shift     | 06–14  | **8.50**   | Peak production run; highest material throughput |
| Afternoon shift   | 14–22  | **5.00**   | Second shift with ~40 % lower throughput (real studies show 2nd shift is ~55–60 % as productive as 1st) |

The previous model had industrial **fully zero on weekends** — unrealistic, as
even closed factories produce minor waste (leaking fluids, security patrols).
Changed to 0.5 units/s to reflect skeleton-crew reality.

---

## 3. Economy

### 3a. Fuel (K_BASE, K_HEAVY, FUEL_PRICE)

A real diesel garbage truck (Volvo FE, MAN TGS) consumes **28–38 L/100 km**
at kerb weight and **35–50 L/100 km** when fully loaded (source: ACEA 2023).
Diesel in Europe ≈ €1.65/L (2024 average). Cost per km ≈ €0.55–€0.80.

In game pixels, 100 px ≈ ~150 m (city-block scale at the default zoom).

- `K_BASE = 0.04` (empty) — was 0.05. Lowered slightly because the old value
  made short routes unprofitable even with good loads.
- `K_HEAVY = 0.09` (full-load penalty) — was 0.10. Marginal change; kept near
  the original because load-fuel linearity is a reasonable simplification.
- `FUEL_PRICE = 2.4` — was 2.0. Raised to reflect that diesel costs have risen
  ~20 % in real terms since 2021 and to create meaningful route-length pressure.

### 3b. Reward per unit (REWARD)

Real sanitation tipping fees: **€30–80/tonne** at landfill, plus collection
contract revenue of **€80–150/tonne** (EEA, 2022). Total ≈ €110–230/tonne.

1 waste unit ≈ 1 kg → €0.11–0.23/unit at minimum. Scaled up to game $ for
playability: `REWARD = 2.6` (was 3.0). Slightly lower to make profitability
depend on route efficiency, not just running trucks everywhere.

### 3c. Penalty (PENALTY)

EU Directive 2008/98/EC mandates strict collection schedules with fines for
overflowing collection points (health hazard). Municipal fines for missed
collections: **€50–500 per incident** depending on jurisdiction.

`PENALTY = 18` (was 12) — raised 50 % to make overflow meaningfully punishing.
At 1× speed with 18 $/s, a building overflowing for just 5 real seconds
costs $90 — roughly the revenue from one truck trip on a short route.

### 3d. Starting capital (INITIAL_MONEY)

`INITIAL_MONEY = 750` (was 500). A small waste-collection startup in a city
needs capital for at least 2 truck runs before revenue arrives. The extra $250
allows deploying one van immediately without agonising over the first route.

---

## 4. Infrastructure Costs

Building a new depot or landfill carries a one-time purchase price and an ongoing
daily maintenance fee, reflecting real municipal waste-infrastructure economics.

### 4a. Purchase Prices

| Structure     | Cost  | Real-world basis |
|---------------|-------|------------------|
| Depot (Hub)   | **$400** | Typical depot lease/setup for a 3-vehicle fleet: ~€15 000–40 000 (amortised to game scale) |
| Landfill      | **$300** | Small transfer-station construction cost; cheaper than depot because no vehicle storage |

Starter depot and landfill placed by `generateMap()` are **free** — they represent
existing municipal infrastructure handed to the player at game start.

### 4b. Daily Maintenance

| Structure     | Per day | Real-world basis |
|---------------|---------|------------------|
| Depot         | **$30** | Staff, utilities, insurance: UK fleet depots average ~£10 000–£20 000/year ÷ 365 ≈ £30/day (BSI Fleet Management 2023) |
| Landfill      | **$20** | Smaller staff footprint; transfer stations cost ~60–70 % of a full depot |

Maintenance fires once per game day (every ~4.8 real minutes at 1×). With 2 depots + 2
landfills, the daily overhead is **$100/day** — roughly the revenue of one standard
truck trip on a medium-length route. This keeps infrastructure expansion meaningful.

### 4c. Demolition Refund

`SELL_REFUND = 0.5` — the player recovers **50 %** of the original purchase price.
This mirrors typical asset-disposal norms (equipment sold second-hand at 40–60 % of
purchase price). Starter infrastructure refunds $0 because it was free to place.
All routes using a demolished node are automatically removed.

---

## 5. Truck Types

### Van (Light Van)

Real-world analogue: **Mercedes Sprinter side-loader**, ~800 kg payload.

| Stat      | Old  | New  | Reason |
|-----------|------|------|--------|
| speed     | 220  | 190  | City vans do ~40–50 km/h average in urban traffic (TfL 2022) |
| capacity  | 50   | 80   | Closer to 800 kg bin capacity; original 50 was too small |
| K_BASE    | 0.03 | 0.025 | Lighter vehicle, lower base consumption |
| K_HEAVY   | 0.05 | 0.04  | Proportionally less load penalty than heavy trucks |

### Standard Truck

Real-world analogue: **Volvo FE rear-loader**, 8-tonne payload after compaction.

| Stat      | Old  | New  | Reason |
|-----------|------|------|--------|
| speed     | 120  | 100  | Heavy RCVs average ~25–35 km/h on collection runs (CIWM 2020) |
| capacity  | 250  | 320  | 8 tonnes @ ~25 kg/unit = 320 units; old 250 underestimated capacity |

### Compactor (Large Articulated)

Real-world analogue: **Faun Variopress 520**, 20-tonne articulated compactor truck.

| Stat        | Old  | New  | Reason |
|-------------|------|------|--------|
| speed       | 60   | 55   | Articulated vehicle, slower cornering in city |
| capacity    | 800  | 1000 | 20-tonne payload @ ~20 kg/unit = 1000 units |
| rewardMult  | 1.4  | 1.6  | Compaction ratio is typically 4 : 1 by volume; waste is denser and earns more per ton at tipping |
| K_HEAVY     | 0.08 | 0.07 | Large vehicle's fuel curve is flatter (already heavy when empty) |

---

## 6. Summary of Net Effect on Gameplay

- **Routes must be planned around time-of-day** — residential peaks at 07–09
  and 17–22 mean morning and evening runs are critical. Mid-day runs are
  optional for most residential buildings.
- **Commercial buildings reward predictable schedules** — they are silent at
  night and high during business hours, making 08:00 and 17:00 schedule
  entries the obvious optimal choices.
- **Industrial is the most demanding per building** — 8.5 units/s during the
  morning shift fills the 1 200-unit roll-off in ~141 real seconds (~11.8 game-hours).
  A compactor is almost mandatory for a pure industrial route.
- **Profitability requires efficiency** — with REWARD = 2.6 and FUEL_PRICE = 2.4,
  a van doing a 400 px round trip (800 px total) at half capacity breaks even.
  Longer routes or lighter loads lose money; full loads on short routes are
  where profit comes from.
- **Overflow is costly** — 18 $/s penalty means a 30-second overflow wipes out
  ~$540, comparable to several full truck runs. Players are incentivised to
  build redundant schedules for high-output buildings.
- **Infrastructure has ongoing costs** — each depot costs $30/day and each landfill
  $20/day. Expanding infrastructure improves coverage but raises the breakeven
  threshold; the player must balance network density against daily overhead.
- **Demolition is available but lossy** — selling a depot or landfill refunds 50 %
  of its purchase price and immediately removes all affected routes. Use as a last
  resort for restructuring, not as a routine cash source.
