# Vesting Schedule Guide

This guide explains how to create a vesting schedule for a project with genesis allocations (premine/ICO/presale).

## Overview

The vesting schedule tracks **when genesis allocations unlock over time**, enabling cross-project comparison of sell pressure from insiders, VCs, team, and treasury.

### Key Concepts

- **Genesis allocation**: Tokens allocated at launch (before any mining/staking)
- **Vesting**: Gradual release of locked tokens over time
- **Cliff**: Period where 0% unlocks, then vesting begins
- **TGE unlock**: Percentage immediately liquid at Token Generation Event (genesis)
- **Bucket**: Individual allocation (e.g., "Seed Round 1", "Team Allocation")
- **Tier**: Category of allocation (Tier 1 = VCs/Team, Tier 2 = Treasury, etc.)

---

## Step 1: Gather Data from genesis.json

Before creating the vesting schedule, you need the bucket-level data from `genesis.json`:

```json
"allocation_tiers": {
  "tier_1_profit_seeking": {
    "buckets": [
      {
        "name": "Seed Round 1",
        "absolute_tokens": 50000000,
        "vesting_months": 24,
        "cliff_months": 6,
        "tge_unlock_pct": 0
      }
    ]
  }
}
```

Extract for each bucket:
- ✅ `name` (must match exactly)
- ✅ `absolute_tokens` (total allocation)
- ✅ `vesting_months` (total vesting duration)
- ✅ `cliff_months` (months before first unlock)
- ✅ `tge_unlock_pct` (% liquid at genesis)

---

## Step 2: Calculate Monthly Unlocks

### Linear Vesting (Most Common)

**Example:** 50M tokens, 24-month linear vesting, 6-month cliff, 0% TGE

```
Months 0-5:   Unlock = 0  (cliff)
Months 6-29:  Unlock = 50M / 24 = 2,083,333 per month
Month 30+:    Unlock = 0  (vesting complete)
```

**Cumulative tracking:**
- Month 0: Cumulative = 0
- Month 6: Cumulative = 2,083,333 (4.17%)
- Month 12: Cumulative = 14,583,333 (29.17%)
- Month 30: Cumulative = 50,000,000 (100%)

---

### Quarterly Vesting

**Example:** 80M tokens, 24-month quarterly vesting, 0-month cliff, 0% TGE

```
Quarters:     8 total (every 3 months)
Per quarter:  80M / 8 = 10M

Month 0:      0
Month 3:      10M   (Q1)
Month 6:      10M   (Q2)
Month 9:      10M   (Q3)
Month 12:     10M   (Q4)
...
Month 24:     10M   (Q8, complete)
```

**Important:** Show ALL months, not just quarters. Months 1, 2, 4, 5, etc. have 0 unlocks.

---

### TGE Unlock + Linear Vesting

**Example:** 100M tokens, 10% TGE unlock, 18-month linear vesting, 3-month cliff

```
Month 0:      10M  (10% TGE unlock)
Months 1-2:   0    (cliff)
Month 3:      5M   (90M remaining / 18 months = 5M/month)
Month 4:      5M
...
Month 20:     5M   (final vest, 100M total = 100%)
```

**Cumulative:**
- Month 0: 10M (10%)
- Month 3: 15M (15%)
- Month 20: 100M (100%)

---

### Block Reward Vesting (Advanced)

**Example:** 30M tokens released via block rewards over 30 months at varying rates

```
Phase 1 (Months 0-24):  7.5 tokens/block
Phase 2 (Months 25-27): 4.5 tokens/block
Phase 3 (Months 28-30): 1.5 tokens/block

Calculation:
- Blocks per month = 1,440 blocks/day × 30 days = 43,200 blocks
- Phase 1 monthly: 7.5 × 43,200 = 324,000 tokens
- Phase 2 monthly: 4.5 × 43,200 = 194,400 tokens
- Phase 3 monthly: 1.5 × 43,200 = 64,800 tokens
```

**CSV entries:**
```
Months 1-24:  unlock_tokens = 324,000
Months 25-27: unlock_tokens = 194,400
Months 28-30: unlock_tokens = 64,800
```

---

## Step 3: Fill Out the CSV

### CSV Structure

```csv
month,date,tier,bucket_name,unlock_tokens,unlock_pct_of_bucket,cumulative_tokens,cumulative_pct_of_bucket,notes
```

### Column Definitions

| Column | Description | Example |
|--------|-------------|---------|
| `month` | Months since genesis (0 = genesis) | `0`, `1`, `12`, `24` |
| `date` | Actual date (genesis_date + month) | `2021-11-08` |
| `tier` | Tier from genesis.json | `tier_1_profit_seeking` |
| `bucket_name` | **Exact** name from genesis.json | `Seed Round 1` |
| `unlock_tokens` | **New** tokens unlocking THIS month | `2083333` |
| `unlock_pct_of_bucket` | % of THIS bucket unlocking | `4.17` |
| `cumulative_tokens` | **Total** unlocked UP TO this month | `14583333` |
| `cumulative_pct_of_bucket` | Cumulative % of THIS bucket | `29.17` |
| `notes` | Human-readable description | `Q4 linear vesting` |

---

### Important Rules

#### 1. Bucket Names Must Match Exactly

❌ **WRONG:**
```csv
month,date,tier,bucket_name,...
0,2021-11-08,tier_1_profit_seeking,Seed Round,...  ← Missing "1"
```

✅ **CORRECT:**
```csv
month,date,tier,bucket_name,...
0,2021-11-08,tier_1_profit_seeking,Seed Round 1,...  ← Exact match
```

The converter script validates bucket names against `genesis.json`.

---

#### 2. Include One Row Per Bucket Per Month

If a project has 3 buckets and tracks 48 months:
- **Total rows:** 3 buckets × 48 months = **144 rows**

Example month with 2 buckets:
```csv
month,date,tier,bucket_name,unlock_tokens,...
12,2022-11-08,tier_1_profit_seeking,Private Sale,10000000,...
12,2022-11-08,tier_2_entity_controlled,Treasury,5000000,...
```

---

#### 3. Skip Tiers with 0 Buckets

If Tier 3 and Tier 4 have no buckets, **do not include rows for them**.

❌ **WRONG:**
```csv
0,2021-11-08,tier_3_community,N/A,0,...
0,2021-11-08,tier_4_liquidity,N/A,0,...
```

✅ **CORRECT:** Skip entirely.

---

#### 4. Cumulative Must Equal 100% at Final Month

The validator checks that `cumulative_pct_of_bucket` reaches 100.00% (±0.1% tolerance) at the final month.

❌ **WRONG:**
```csv
60,2026-11-08,tier_1_profit_seeking,Seed Round 1,0,0.00,48000000,96.00,...  ← Only 96%!
```

✅ **CORRECT:**
```csv
60,2026-11-08,tier_1_profit_seeking,Seed Round 1,2000000,4.00,50000000,100.00,...  ← 100%
```

---

#### 5. Date Calculation

Dates must be **genesis_date + month offset**.

If genesis is `2021-11-08`:
- Month 0: `2021-11-08`
- Month 1: `2021-12-08`
- Month 12: `2022-11-08`
- Month 24: `2023-11-08`

**Excel formula:**
```excel
=DATE(YEAR($B$2), MONTH($B$2) + A2, DAY($B$2))
```
Where `$B$2` is genesis date and `A2` is month number.

---

## Step 4: Example - Complete Workflow

### Project: ExampleCoin

**From genesis.json:**
```json
{
  "project": "examplecoin",
  "genesis_date": "2023-01-01",
  "allocation_tiers": {
    "tier_1_profit_seeking": {
      "buckets": [
        {
          "name": "Seed Round",
          "absolute_tokens": 20000000,
          "vesting_months": 12,
          "cliff_months": 0,
          "tge_unlock_pct": 10
        }
      ]
    },
    "tier_2_entity_controlled": {
      "buckets": [
        {
          "name": "Treasury",
          "absolute_tokens": 30000000,
          "vesting_months": 24,
          "cliff_months": 6,
          "tge_unlock_pct": 0
        }
      ]
    }
  }
}
```

---

### Calculations

**Seed Round:**
- TGE: 10% × 20M = 2M (month 0)
- Remaining: 90% × 20M = 18M
- Monthly unlock: 18M / 12 = 1.5M

| Month | Unlock | Cumulative | % |
|-------|--------|------------|---|
| 0 | 2M | 2M | 10% |
| 1 | 1.5M | 3.5M | 17.5% |
| 2 | 1.5M | 5M | 25% |
| ... | ... | ... | ... |
| 12 | 1.5M | 20M | 100% |

**Treasury:**
- TGE: 0%
- Cliff: 6 months (months 0-5 = 0 unlock)
- Monthly unlock: 30M / 24 = 1.25M (months 6-29)

| Month | Unlock | Cumulative | % |
|-------|--------|------------|---|
| 0 | 0 | 0 | 0% |
| 1-5 | 0 | 0 | 0% |
| 6 | 1.25M | 1.25M | 4.17% |
| 7 | 1.25M | 2.5M | 8.33% |
| ... | ... | ... | ... |
| 29 | 1.25M | 30M | 100% |

---

### CSV Output (first 10 rows)

```csv
month,date,tier,bucket_name,unlock_tokens,unlock_pct_of_bucket,cumulative_tokens,cumulative_pct_of_bucket,notes
0,2023-01-01,tier_1_profit_seeking,Seed Round,2000000,10.00,2000000,10.00,TGE unlock 10%
0,2023-01-01,tier_2_entity_controlled,Treasury,0,0.00,0,0.00,Genesis - 6 month cliff
1,2023-02-01,tier_1_profit_seeking,Seed Round,1500000,7.50,3500000,17.50,Linear vesting begins
1,2023-02-01,tier_2_entity_controlled,Treasury,0,0.00,0,0.00,Cliff ongoing
2,2023-03-01,tier_1_profit_seeking,Seed Round,1500000,7.50,5000000,25.00,Linear vesting
2,2023-03-01,tier_2_entity_controlled,Treasury,0,0.00,0,0.00,Cliff ongoing
3,2023-04-01,tier_1_profit_seeking,Seed Round,1500000,7.50,6500000,32.50,Linear vesting
3,2023-04-01,tier_2_entity_controlled,Treasury,0,0.00,0,0.00,Cliff ongoing
...
```

---

## Step 5: Validate and Convert

### Run the Converter

```bash
python scripts/csv_to_vesting_json.py allocations/examplecoin/vesting-schedule.csv
```

### Success Output

```
✓ Loaded genesis.json: allocations/examplecoin/genesis.json
✓ Parsing CSV: allocations/examplecoin/vesting-schedule.csv
✓ Parsed 60 rows
✓ Validating data...
✓ All validations passed
✓ Converting to JSON...
✓ Generated: allocations/examplecoin/vesting-schedule.json

Summary:
  Project: examplecoin
  Total genesis allocation: 50,000,000 tokens
  Vesting period: 29 months
  Final unlock: 2025-06-01
```

---

### Common Validation Errors

#### Error: Bucket name not found

```
✗ Row 5: Bucket name 'Seed' not found in genesis.json tier 'tier_1_profit_seeking'.
Valid names: Seed Round
```

**Fix:** Use exact bucket name from genesis.json.

---

#### Error: Cumulative never decreases

```
✗ Row 15: Cumulative decreased from 10000000 to 9500000 for tier_1_profit_seeking::Seed Round
```

**Fix:** Check your cumulative calculation. It should never go down.

---

#### Error: Final cumulative not 100%

```
✗ Final cumulative for tier_1_profit_seeking::Seed Round is 95.5%, expected 100%
```

**Fix:** Extend vesting schedule or recalculate monthly amounts. Cumulative must reach 100%.

---

## Step 6: Generate Comparison Matrix

After adding vesting schedules for multiple projects:

```bash
python scripts/generate_comparison_matrix.py
```

Output:
```
✓ Found 3 projects (2 with premines)
✓ Generated: allocations/comparison-matrix.json

Summary:
  Project              Genesis %    TGE %      12mo %     24mo %     Full Unlock
  -------------------- ------------ ---------- ---------- ---------- ---------------
  alephium             14.0       % 0.0      % 31.2     % 70.4     % 81 months
  examplecoin          50.0       % 5.0      % 35.0     % 100.0    % 29 months
  kaspa                0%           -          -          -          N/A (mining)
```

---

## Common Vesting Patterns

### Pattern 1: Fair Launch (No Premine)

**Example:** Kaspa, Bitcoin

- ❌ No vesting schedule needed
- ✅ Set `has_premine: false` in genesis.json
- ✅ Skip vesting-schedule.csv entirely

---

### Pattern 2: VC-Heavy Launch

**Example:** Typical ICO project

```
Tier 1 (70%):  Seed, Private, Strategic rounds
  - 10% TGE unlock
  - 6-month cliff
  - 18-24 month linear vesting

Tier 2 (20%):  Team, Advisors
  - 0% TGE unlock
  - 12-month cliff
  - 36-48 month linear vesting

Tier 3 (10%):  Community airdrop
  - 100% TGE unlock (immediately liquid)
```

---

### Pattern 3: Fair Launch with Small Treasury

**Example:** Ergo

```
Tier 2 (4.43%):  Foundation treasury
  - 0% TGE unlock
  - Released via block rewards over 30 months
  - No Tier 1 (no VCs/team allocation)

Tier 3 (0.51%):  Community pre-sale
  - 100% TGE unlock (small, accredited investors)
```

---

### Pattern 4: Quarterly with Long Cliffs

**Example:** Alephium

```
Tier 1 (7.95%):  Private sale
  - 0% TGE unlock
  - 0-month cliff
  - Quarterly vesting over 24 months (8 quarters)

Tier 2 (6%):  Treasury + Ecosystem
  - 0% TGE unlock
  - 12-48 month cliffs (different per bucket)
  - Quarterly vesting after cliff
```

---

## Troubleshooting

### Q: My project has 100% TGE unlock for one bucket. How do I represent this?

**A:** Show month 0 with 100% unlock, then stop tracking that bucket:

```csv
month,date,tier,bucket_name,unlock_tokens,unlock_pct_of_bucket,cumulative_tokens,cumulative_pct_of_bucket,notes
0,2023-01-01,tier_3_community,Airdrop,5000000,100.00,5000000,100.00,Immediate unlock at TGE
```

No need to include months 1, 2, 3, etc. for this bucket (it's fully unlocked).

---

### Q: The vesting schedule in the whitepaper is vague. What should I do?

**A:** Make reasonable assumptions and document them in the `notes` column:

```csv
notes
Assumes linear vesting - whitepaper did not specify
```

Add transparency note in genesis.json:
```json
"transparency_notes": [
  "Vesting schedule estimated from whitepaper; exact unlock dates not disclosed"
]
```

---

### Q: Can I include months beyond 60?

**A:** Yes! The CSV supports any number of months. Some projects have 10-year vesting (120 months).

---

### Q: What if a bucket has a cliff longer than the vesting period?

**A:** This happens with "release after X years" allocations:

```json
{
  "name": "Long-term Reserve",
  "absolute_tokens": 10000000,
  "vesting_months": 0,
  "cliff_months": 60,
  "tge_unlock_pct": 0
}
```

**CSV:**
```csv
month,date,tier,bucket_name,unlock_tokens,unlock_pct_of_bucket,cumulative_tokens,cumulative_pct_of_bucket,notes
0,2023-01-01,tier_2_entity_controlled,Long-term Reserve,0,0.00,0,0.00,60-month cliff begins
...
59,2027-12-01,tier_2_entity_controlled,Long-term Reserve,0,0.00,0,0.00,Cliff ongoing
60,2028-01-01,tier_2_entity_controlled,Long-term Reserve,10000000,100.00,10000000,100.00,Cliff ends - immediate 100% unlock
```

---

## Best Practices

### ✅ DO:
- Use exact bucket names from genesis.json
- Include ALL months (even those with 0 unlocks)
- Double-check cumulative percentages reach 100%
- Add detailed notes for complex vesting patterns
- Validate with the converter script before submitting

### ❌ DON'T:
- Guess unlock schedules - cite sources in genesis.json
- Round cumulative percentages excessively (use 2 decimals)
- Skip months (e.g., show only quarters) - include all months
- Include tiers with 0 buckets
- Forget to run the validation script

---

## Need Help?

- **Examples:** See `allocations/alephium/vesting-schedule.csv`
- **Template:** Use `templates/vesting-schedule-template.csv`
- **Converter:** `scripts/csv_to_vesting_json.py --help`
- **Issues:** https://github.com/anthropics/claude-code/issues
