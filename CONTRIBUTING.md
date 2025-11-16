# Contributing to PoW Tokenomics Tracker

## Table of Contents
1. [Philosophy: Why We Do This](#philosophy)
2. [Getting Started](#getting-started)
3. [Data Requirements](#data-requirements)
4. [Step-by-Step Instructions](#instructions)
5. [Special Cases](#special-cases)
6. [Quality Standards](#quality-standards)
7. [After You Submit](#after-submission)

---

## Philosophy: Show Data, Let Users Judge {#philosophy}

We don't create synthetic "fairness scores" because they hide manipulation and are easily gamed.

Instead, we show:
- **Raw allocation numbers** - Can't hide premine dominance
- **Circulating composition** - Who controls liquid supply today
- **Vesting schedules** - When insiders unlock tokens
- **Transparency gaps** - What data is missing or unverifiable

**Your job:** Provide accurate, verifiable data
**User's job:** Judge fairness themselves

---

## Getting Started {#getting-started}

### What You'll Need

**Tools:**
- Git/GitHub account
- Text editor (VS Code, Sublime, etc.)
- Python 3.7+ (optional, for validation)

**Data sources:**
- Block explorer for the chain
- Official project documentation
- Funding announcements (Medium, Twitter, Crunchbase)
- CoinGecko/CoinMarketCap for market data

**Time commitment:**
- Simple project: 15-30 minutes
- Complex project: 1-2 hours (if researching investor allocations)

### File Structure Overview
```
data/projects/yourproject.json          ← Always required
allocations/yourproject/genesis.json    ← Only if has_premine=true
```

**Rule:** One file for fair launches, two files for premined projects

---

## Data Requirements {#data-requirements}

### Must-Have Fields

**Basic Info:**
- `project` - Lowercase, no spaces (e.g., "bitcoin", "kadena")
- `ticker` - Uppercase symbol (e.g., "BTC", "KDA")
- `launch_date` - YYYY-MM-DD format
- `consensus` - PoW, PoS, Hybrid, or DPoS
- `has_premine` - true/false

**Supply Data:**
- `max_supply` - Total cap (use `null` if unlimited)
- `current_supply` - Mined/minted to date
- `pct_mined` - Percentage of max already issued

**Emission Data:**
- `current_block_reward` - Tokens per block now
- `block_time_seconds` - Average time between blocks
- `daily_emission` - Tokens created per day
- `annual_inflation_pct` - Yearly inflation rate

**Market Data:**
- `current_price_usd` - Current price
- `fdmc` - Fully diluted market cap
- `circulating_mcap` - Circulating market cap

**Critical:**
- `data_sources` - URLs for every claim (block explorer, docs, announcements)

### Genesis Allocation (If Premine Exists)

Required in `allocations/yourproject/genesis.json`:

**Allocation Tiers:**
- **Tier 1: Profit-Seeking** (VCs, team with direct profit motive)
- **Tier 2: Entity-Controlled** (Foundation, treasury, dev company)
- **Tier 3: Community** (Airdrops, public sales)
- **Tier 4: Liquidity** (DEX/CEX market making)

For each tier bucket:
- Percentage of supply
- Absolute token count
- Cost per token (what insiders paid)
- Vesting schedule (months, cliff, TGE unlock %)
- Known investors (name, allocation if disclosed)

---

## Step-by-Step Instructions {#instructions}

### Path A: Fair Launch Project (No Premine)

**Step 1: Copy template**
```bash
cp templates/project-template.json data/projects/bitcoin.json
```

**Step 2: Fill required fields**

Open in editor. For each field:
1. Read the `_comment_fieldname` explanation
2. Find the data from sources
3. Fill in the value
4. Delete the comment line

**Example:**
```json
{
  "max_supply": 21000000,
  "_comment_max_supply": "Maximum possible supply. Use null if unlimited.",
  
  // Becomes:
  
  "max_supply": 21000000,
}
```

**Step 3: Set key flags**
```json
{
  "has_premine": false,
  "premine": null,
  "genesis_allocation": null,
  "launch_type": "fair"
}
```

**Step 4: Add data sources**
```json
{
  "data_sources": {
    "official_docs": [
      "https://bitcoin.org/bitcoin.pdf",
      "https://github.com/bitcoin/bitcoin"
    ],
    "block_explorer": [
      "https://blockchain.com",
      "https://blockchair.com/bitcoin"
    ],
    "market_data": [
      "https://www.coingecko.com/en/coins/bitcoin"
    ]
  }
}
```

**Step 5: Delete ALL `_comment` lines**

Search for `"_comment` and delete every line containing it.

**Step 6: Validate**
```bash
python scripts/validate_submission.py bitcoin
```

Fix any errors reported.

**Step 7: Submit PR**
```bash
git add data/projects/bitcoin.json
git commit -m "Add Bitcoin tokenomics data"
git push origin main
```

Create PR on GitHub.

---

### Path B: Premined Project

**Step 1: Copy both templates**
```bash
cp templates/project-template.json data/projects/yourproject.json
mkdir -p allocations/yourproject
cp templates/genesis-template.json allocations/yourproject/genesis.json
```

**Step 2: Fill main project file**

Same as Path A, but set:
```json
{
  "has_premine": true,
  "launch_type": "premine", // or "ico" or "private_sale"
}
```

**Step 3: Fill genesis allocation file**

**Break down the premine by tier:**
```json
{
  "total_genesis_allocation_pct": 33.0,
  
  "allocation_tiers": {
    "tier_1_profit_seeking": {
      "total_pct": 20.0,
      "buckets": [
        {
          "name": "Seed Round 1",
          "pct": 15.0,
          "absolute_tokens": 15000000,
          "cost_per_token_usd": 0.01,
          "vesting_months": 24,
          "cliff_months": 6,
          "investors": {
            "known": [
              {"name": "Polychain Capital", "pct_of_round": "unknown"}
            ],
            "unknown_count": 12,
            "total_investors": 13
          }
        }
      ]
    }
  }
}
```

**Step 4: Handle unknowns**

When investor info isn't disclosed:
```json
"investors": {
  "known": [
    {"name": "Binance Labs", "pct_of_round": 40, "tokens": 4760000}
  ],
  "unknown_count": 8,
  "total_investors": 9,
  "notes": "Only Binance Labs disclosed; 8 others unknown"
}
```

**Step 5: Add vesting waterfall**

Monthly unlock schedule:
```json
"vesting_waterfall": [
  {
    "month": 0,
    "unlock_tokens": 9100000,
    "pct_of_premine": 27.6,
    "source": "TGE unlocks (multiple buckets)"
  },
  {
    "month": 6,
    "unlock_tokens": 4500000,
    "pct_of_premine": 13.6,
    "source": "Seed 1 cliff"
  }
]
```

**Step 6: Validate both files**
```bash
python scripts/validate_submission.py yourproject
```

**Step 7: Submit PR with both files**
```bash
git add data/projects/yourproject.json allocations/yourproject/genesis.json
git commit -m "Add YourProject tokenomics data"
git push origin main
```

---

## Special Cases {#special-cases}

### Case 1: Suspected Insider Mining (Kaspa-style)

When you suspect unfair mining but can't prove it:
```json
"suspected_insider_mining": {
  "enabled": true,
  "timeframe": "2021-11 to 2022-02",
  "estimated_pct_of_supply": 3.0,
  "evidence": [
    "Hashrate spike to 1.2 TH/s in week 1 despite no public ASIC availability",
    "Single address accumulated 450M tokens in first 3 months",
    "Network hashrate dropped 60% after month 4 (suspected rented hashrate)"
  ],
  "verifiable": false,
  "source_investigations": [
    "https://link-to-community-analysis"
  ]
}
```

**Rules:**
- Only use if you have specific evidence
- Link to analyses, not rumors
- Set `verifiable: false` unless proven with on-chain clustering
- Don't make accusations without backing data

### Case 2: Dev Tax / Block Reward Split (Zcash-style)

When protocol takes % of each block:
```json
"dev_tax": {
  "type": "block_reward_split",
  "pct_of_block_reward": 20,
  "duration_blocks": 1051200,
  "recipient": "0x123...",
  "notes": "20% of each block to founder reward address for first 4 years"
}
```

### Case 3: Treasury Emission (Ergo-style)

When mining rewards are split (not a premine):
```json
"has_premine": false,
"has_treasury_emission": true,

"treasury_emission": {
  "total_pct_of_supply": 4.43,
  "mechanism": "block_reward_percentage",
  "percentage_of_blocks": 10,
  "duration_start": "2019-07-01",
  "duration_end": "2022-01-01",
  "status": "completed"
}
```

### Case 4: Missing Blockchain Data (Kaspa-style)

When transaction records are missing:
```json
"blockchain_data_complete": false,
"missing_data": {
  "period": "2021-11-07 to 2022-05-08",
  "pct_of_supply_affected": 27.0,
  "reason": "No full nodes exist with complete transaction history",
  "impact": "Cannot verify distribution claims for first 6 months"
}
```

### Case 5: Unknown Investors

When most investors aren't disclosed:
```json
"investors": {
  "known": [
    {"name": "Polychain Capital", "pct_of_round": "unknown", "tokens": "unknown"}
  ],
  "unknown_count": 24,
  "total_investors": 25,
  "notes": "Announcement stated '25 investors including Polychain' - individual allocations not disclosed"
}
```

**Key:** Be honest about what you don't know. Use `"unknown"` strings and `unknown_count` fields.

---

## Quality Standards {#quality-standards}

### Required for Approval ✅

**1. Verifiable Sources**
Every claim must have a URL:
- Block explorers for supply/emission data
- Official docs for tokenomics design
- Funding announcements for investor info
- On-chain contracts for vesting (if available)

❌ **Rejected:** "Supply is 100M according to team Discord"
✅ **Approved:** "Supply is 100M per block explorer: https://..."

**2. Current Data**
- Data should be <30 days old
- Include `last_updated: "2025-11-16"` field
- Stale PRs may be closed (can reopen with fresh data)

**3. Accurate Math**
Validator checks:
- Allocation percentages sum to 100%
- Supply calculations are consistent
- Emission math is correct
- No impossible vesting schedules

**4. Neutral Tone**
- Stick to facts, not opinions
- OK: "Team received 10% with 2-year vesting"
- NOT OK: "Team greedily took 10% with short vesting"
- Use `notes` field for factual context

### Nice-to-Have 🎯

- Complete investor disclosure (names and amounts)
- On-chain contract addresses for verification
- Historical context in notes field
- Multiple source cross-referencing
- Transparency assessment

---

## Where to Find Data

### Supply & Emission Data

**Block Explorers:**
- Bitcoin: blockchain.com, blockchair.com
- Ethereum: etherscan.io
- Other chains: Search "[project] block explorer"

**What to collect:**
- Current supply (total mined/minted)
- Max supply (from code or docs)
- Current block reward
- Average block time (last 1000 blocks)

### Mining/Staking Data

**Mining (PoW):**
- WhatToMine.com - profitability, difficulty
- MiningPoolStats - pool distribution
- Project's own explorer - hashrate

**Staking (PoS):**
- Staking explorers (e.g., beaconcha.in for Ethereum)
- Validator lists
- Staking participation rates

### Market Data

**Price & Market Cap:**
- CoinGecko (API available)
- CoinMarketCap
- LiveCoinWatch
- DEX aggregators (if not on CEXs)

### Investor & Allocation Data

**Funding Announcements:**
- Project Medium blog
- Project Twitter
- Crunchbase
- TechCrunch articles
- VC firm announcements

**Vesting Information:**
- Project tokenomics docs
- Etherscan (if vesting contracts on Ethereum)
- Project's own block explorer
- Community analyses

**Red flags when sources are scarce:**
- No public investor list → Note in `unknown_count`
- Vague percentages → Use `"unknown"` for specifics
- Missing vesting details → Document in transparency notes

---

## Calculating Derived Fields

Some fields aren't directly available - you calculate them:

### Daily Emission
```javascript
daily_emission = (86400 seconds / block_time_seconds) * current_block_reward

Example (Bitcoin):
= (86400 / 600) * 6.25
= 144 * 6.25
= 900 BTC/day
```

### Annual Inflation
```javascript
annual_inflation_pct = (daily_emission * 365 / current_supply) * 100

Example (Bitcoin):
= (900 * 365 / 19562000) * 100
= 1.68%
```

### Percentage Mined
```javascript
pct_mined = (current_supply / max_supply) * 100

Example (Bitcoin):
= (19562000 / 21000000) * 100
= 93.15%
```

### Market Caps
```javascript
fdmc = current_price_usd * max_supply
circulating_mcap = current_price_usd * current_supply

Example (Bitcoin at $67,500):
fdmc = 67500 * 21000000 = $1,417,500,000,000
circulating_mcap = 67500 * 19562000 = $1,320,435,000,000
```

### Token Velocity
```javascript
token_velocity = daily_volume / circulating_mcap

Example (Bitcoin with $28.5B daily volume):
= 28500000000 / 1320435000000
= 0.022 (2.2% daily turnover)
```

---

## Common Mistakes ❌

### 1. Leaving Template Comments

❌ **Wrong:**
```json
{
  "max_supply": 21000000,
  "_comment_max_supply": "Maximum possible supply. Use null if unlimited."
}
```

✅ **Right:**
```json
{
  "max_supply": 21000000
}
```

**Fix:** Search for `"_comment` and delete every matching line.

### 2. Percentages Don't Sum to 100%

❌ **Wrong:**
```json
"tier_1_profit_seeking": {"total_pct": 33.5},
"tier_2_entity_controlled": {"total_pct": 39.4},
"tier_3_community": {"total_pct": 23.0}
// Total: 95.9% (missing 4.1%!)
```

✅ **Right:**
```json
"tier_1_profit_seeking": {"total_pct": 33.5},
"tier_2_entity_controlled": {"total_pct": 39.4},
"tier_3_community": {"total_pct": 23.0},
"tier_4_liquidity": {"total_pct": 4.1}
// Total: 100%
```

### 3. No Data Sources

❌ **Wrong:**
```json
{
  "current_supply": 19562000,
  "data_sources": {}
}
```

✅ **Right:**
```json
{
  "current_supply": 19562000,
  "data_sources": {
    "block_explorer": ["https://blockchain.com/explorer"]
  }
}
```

### 4. Wrong Date Format

❌ **Wrong:**
```json
"launch_date": "11/7/2021"  // Month/Day/Year
"launch_date": "7-Nov-2021" // Text month
```

✅ **Right:**
```json
"launch_date": "2021-11-07"  // YYYY-MM-DD
```

### 5. Outdated Information

❌ **Wrong:**
```json
{
  "current_supply": 19000000,  // From 6 months ago
  "last_updated": "2025-05-01"
}
```

✅ **Right:**
```json
{
  "current_supply": 19562000,  // Fresh data
  "last_updated": "2025-11-16"
}
```

---

## After You Submit {#after-submission}

### Review Process

**1. Auto-checks run** (if configured)
- JSON syntax validation
- Required field verification
- Basic math checks

**2. Community review** (typically 1-3 days)
- Maintainers verify data sources
- Check calculations
- Cross-reference claims with blockchain

**3. Feedback or approval**
- ✅ Approved → Merged! Goes live on tracker
- 🔄 Changes needed → Comments on what to fix

**4. Updates**

Data gets stale! To update existing projects:
```bash
# Edit the file(s)
# Update last_updated date
# Add note about what changed

git add data/projects/yourproject.json
git commit -m "Update YourProject - Nov 2025 data refresh"
git push
```

### What Makes a PR Merge-Worthy

**Fast-track approval:**
- All required fields complete
- Multiple sources cited
- Math validated
- Current data (<7 days old)
- Clean JSON (no comments left)
- Follows existing patterns

**Needs revision:**
- Missing sources
- Math errors
- Template comments still present
- Vague or marketing language
- Stale data (>30 days)

**Rejected:**
- Duplicate submission
- Spam/joke submission
- Malicious data
- Unverifiable claims without disclosure

---

## Examples

### Example 1: Bitcoin (Fair Launch)

See `examples/bitcoin-example.json`:
- No premine (has_premine: false)
- No genesis file needed
- Clean, simple structure
- Multiple sources cited

### Example 2: Example Coin (66.7% Premine)

See `examples/example-coin.json` and `examples/example-coin-genesis.json`:
- Complex tier breakdown
- Partial investor disclosure (some known, some unknown)
- Detailed vesting schedule
- Transparency notes included

### Example 3: Updating Existing Project
```bash
# 1. Edit data/projects/kadena.json
# Update current_supply, current_price_usd, fdmc
# Change last_updated to today

# 2. Commit
git commit -m "Update Kadena - Nov 2025 supply and market data"

# 3. In PR description, explain:
"Updated Kadena data to reflect current supply (Nov 16, 2025):
- Current supply: 254M → 267M KDA
- FDMC: $1.8B → $1.6B
- Sources: kadena.io/explorer, coingecko.com"
```

---

## Getting Help

**Question about data format?**
→ Check `examples/` directory for patterns

**Can't find specific data?**
→ Use `null` or `"unknown"` and note in transparency section

**Validation errors?**
→ Read the error message - it usually tells you exactly what's wrong

**Still stuck?**
→ Open an [Issue](../../issues) with `question` label
→ Include: project name, what you're trying to find, where you've looked

**Found a bug in templates?**
→ Open an issue or submit a fix PR!

---

## Thank You

By contributing accurate tokenomics data, you help:
- 🔍 **Miners** understand if projects are fair
- 💰 **Investors** see insider allocations
- 📊 **Researchers** analyze PoW economics
- 🗳️ **Community** make informed decisions

Every contribution brings more transparency to crypto.

**Let's make PoW tokenomics transparent together.** 🚀
