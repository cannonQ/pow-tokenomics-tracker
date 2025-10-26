# Contributing to PoW Tokenomics Tracker

**Welcome!** This guide will help you add or update project data. It's designed to be simple - just like adding a token to DefiLlama.

---

## Quick Start (5 steps)

1. **Fork** this repository
2. **Copy** the template and fill it in
3. **Validate** your data (optional but recommended)
4. **Commit** to your fork
5. **Submit** a Pull Request

That's it! No complex setup needed.

---

## Step-by-Step Instructions

### 1. Choose Your Template

**For fair launch projects (no premine):**
- Copy `templates/project-template.json`
- Fill in all fields
- Set `has_premine: false`
- Set `genesis_allocation: null`

**For projects with premine/ICO/presale:**
- Copy `templates/project-template.json` AND `templates/genesis-template.json`
- Fill in both files
- Set `has_premine: true` in main project file

---

### 2. Where to Put Your Files

```
data/projects/[yourproject].json          ← Main project data
allocations/[yourproject]/genesis.json    ← Only if has_premine=true
```

**Example for Bitcoin:**
```
data/projects/bitcoin.json
# No genesis.json needed - fair launch!
```

**Example for a premined project:**
```
data/projects/example-coin.json
allocations/example-coin/genesis.json
```

---

### 3. Filling in the Template

#### A. Required Fields (Must Have)

**Main Project File:**
- `project` - Lowercase name (e.g., "bitcoin")
- `ticker` - Symbol (e.g., "BTC")
- `launch_date` - YYYY-MM-DD format
- `consensus` - PoW, PoS, Hybrid, or DPoS
- `supply.max_supply` - Use `null` if unlimited
- `supply.current_supply` - Get from block explorer
- `emission.current_block_reward` - Current reward per block
- `emission.block_time_seconds` - Average block time
- `data_sources` - **CRITICAL!** Must provide sources

**Genesis File (if premine exists):**
- `total_genesis_allocation_pct` - Total % premined
- `allocation_tiers` - Break down by investor/team/foundation
- `investors.known` - List known VCs/investors
- `vesting_months` - Vesting schedule for each bucket

#### B. Where to Find Data

| Data Point | Where to Look |
|------------|---------------|
| Max Supply | Whitepaper, GitHub README, block explorer |
| Current Supply | Block explorer (Blockchain.com, Blockchair, etc.) |
| Block Reward | Block explorer - check recent blocks |
| Block Time | Block explorer - average over last 1000 blocks |
| Hashrate | Mining pools, WhatToMine, CoinWarz |
| Difficulty | Block explorer |
| Price/FDMC | CoinGecko, CoinMarketCap |
| Investor Info | Medium announcements, Twitter, CrunchBase |
| Vesting | Blockchain (if on-chain), official docs |

#### C. Calculating Fields

Some fields require simple math. Here's how:

```javascript
// Daily emission
daily_emission = (86400 / block_time_seconds) * current_block_reward

// Annual inflation
annual_inflation_pct = (daily_emission * 365 / current_supply) * 100

// % mined
pct_mined = (current_supply / max_supply) * 100

// FDMC (Fully Diluted Market Cap)
fdmc = current_price_usd * max_supply

// Circulating Market Cap
circulating_mcap = current_price_usd * current_supply

// Token Velocity
token_velocity = daily_volume / circulating_mcap
```

#### D. Handling Unknown Data

**Use `null` for truly unknown values:**
```json
"max_supply": null,  // ✅ Good - unlimited supply
"unknown_count": 12, // ✅ Good - we know there are unknowns
```

**Use "unknown" string for counts:**
```json
"pct_of_round": "unknown",  // ✅ Good - not disclosed
```

**Use empty arrays if section not applicable:**
```json
"halving_schedule": [],  // ✅ Good - no halvings
```

---

### 4. Special Cases

#### A. Fair Launch with Suspected Insider Mining

If you believe there was unfair early mining (like Kaspa claims), use the `suspected_insider_mining` section in `genesis-template.json`:

```json
"suspected_insider_mining": {
  "enabled": true,
  "timeframe": "2021-11 to 2022-02",
  "estimated_pct_of_supply": 3.0,
  "evidence": [
    "Hashrate spike week 1 despite no public hardware",
    "Single whale address: 450M tokens in 3 months"
  ],
  "verifiable": false,
  "source_investigations": [
    "https://link-to-analysis"
  ]
}
```

**IMPORTANT:** 
- Only use this if you have specific evidence
- Link to analyses, not just rumors
- Mark `verifiable: false` unless proven with on-chain clustering

#### B. Dev Tax / Block Reward Split

If the project takes a % of each block (Zcash-style):

```json
"dev_tax": {
  "type": "block_reward_split",
  "pct_of_block_reward": 20,
  "duration_blocks": 1051200,
  "recipient": "0x123...",
  "notes": "20% of each block for first 2 years"
}
```

#### C. Unknown Investors

When investor lists are incomplete:

```json
"investors": {
  "known": [
    {"name": "Polychain Capital", "pct_of_round": "unknown"},
    {"name": "Binance Labs", "pct_of_round": 40, "tokens": 4760000}
  ],
  "unknown_count": 8,
  "total_investors": 10,
  "notes": "Only 2/10 investors disclosed publicly"
}
```

---

### 5. Validate Your Submission (Optional)

Before submitting, you can validate your JSON:

```bash
# Install Python requirements
pip install jsonschema

# Run validator
python scripts/validate_submission.py yourproject
```

**What it checks:**
- ✅ Valid JSON syntax
- ✅ All required fields present
- ✅ Percentages sum to 100%
- ✅ Dates in correct format
- ✅ URLs are properly formatted
- ✅ Math checks out (supply, emissions)

Don't have Python? **No problem!** Just submit your PR and reviewers will validate it.

---

### 6. Submit Your Pull Request

1. **Commit your files:**
```bash
git add data/projects/yourproject.json
git add allocations/yourproject/genesis.json  # if applicable
git commit -m "Add [Project Name] tokenomics data"
git push origin main
```

2. **Create PR on GitHub**
   - Click "New Pull Request"
   - Fill out the PR template (auto-loads)
   - Submit!

3. **PR will be reviewed for:**
   - Data accuracy
   - Source verification
   - Proper formatting
   - No duplicate projects

---

## Data Quality Standards

### Must-Haves for Approval ✅

1. **Verifiable Sources**
   - Every data point must have a source
   - Use official docs, block explorers, or archived announcements
   - No "trust me bro" submissions

2. **Current Data**
   - Data should be <30 days old
   - Add `last_updated` date
   - Outdated PRs may be closed (you can reopen with fresh data)

3. **Accurate Math**
   - Supply calculations must be correct
   - Percentages must sum to 100%
   - Emission calculations must match block explorer

4. **Neutral Tone**
   - Stick to facts, not opinions
   - It's OK to note controversies in `notes` field
   - Use `suspected_insider_mining` section appropriately

### Nice-to-Haves 🎯

1. **Complete Investor List**
   - The more disclosed, the better
   - Note when information is incomplete

2. **On-Chain Verification**
   - Vesting contract addresses
   - Token contract address
   - Multisig addresses

3. **Historical Context**
   - Notable events in `notes`
   - Controversy documentation

---

## Common Mistakes to Avoid ❌

1. **Leaving `_comment` fields in JSON**
   - Delete ALL lines starting with `_comment`
   - They're just instructions for you

2. **Wrong percentage calculations**
   - Always verify percentages sum to 100%
   - Double-check tier totals vs bucket totals

3. **Mixing up supply types**
   - `max_supply` = ultimate cap (21M for Bitcoin)
   - `current_supply` = mined so far (19.5M for Bitcoin)
   - `circulating_supply` = actively traded

4. **Missing data sources**
   - **Every claim needs a source**
   - Link to official docs, explorers, announcements

5. **Outdated information**
   - Mining difficulty changes constantly
   - Price/market cap changes daily
   - Note your data collection date

---

## Need Help?

**Questions about:**
- **Data format?** → Check existing projects in `data/projects/`
- **Finding data?** → See "Where to Find Data" section above
- **Validation errors?** → Read error message, check formatting
- **Project already exists?** → Submit an update PR instead

**Still stuck?**
- Open an [Issue](../../issues) with your question
- Tag with `question` label
- We'll help you get it sorted!

---

## What Happens After You Submit?

1. **Auto-checks run** (if set up)
   - JSON syntax validation
   - Basic field checking

2. **Community review** (1-3 days typically)
   - Data verification
   - Source checking
   - Math validation

3. **Approval or feedback**
   - If approved: Merged! 🎉
   - If changes needed: We'll comment on what to fix

4. **Your data goes live**
   - Shows up on website
   - Available in comparison tools
   - Helps the community!

---

## Updating Existing Projects

**To update existing data:**

1. Edit the project file directly
2. Update `last_updated` field
3. Add note explaining what changed
4. Submit PR with clear title: "Update [Project] - [what changed]"

**Example:**
```
Title: Update Bitcoin - Q4 2025 hashrate and difficulty
Description: Updated current_supply, hashrate, and difficulty to reflect Q4 2025 data.
```

---

## Philosophy: Show Data, Let Users Judge

We don't create synthetic "fairness scores" because:
- They hide the actual data
- They're easily gamed
- Users can't verify them

Instead, we show:
- **Raw allocation numbers**
- **Miner parity timelines**
- **Cost disadvantages**
- **Transparency gaps**

Let the data speak for itself.

---

## Examples to Learn From

**Fair Launch:**
- See: `data/projects/bitcoin.json`
- Notice: `has_premine: false`, no genesis file needed

**Clean Premine:**
- See: `data/projects/ethereum.json` (if added)
- Notice: Full investor disclosure, on-chain vesting

**Suspected Issues:**
- See: `data/projects/kaspa.json` (if added)
- Notice: `suspected_insider_mining` section with evidence

---

## Thank You! 🙏

By contributing accurate data, you're helping miners, investors, and the broader crypto community make informed decisions.

Every contribution matters - whether it's adding a new project or fixing a typo!

**Let's bring transparency to PoW tokenomics together.**
