# Quick Start: Add a Project in 10 Minutes

## Prerequisites
- GitHub account
- Basic JSON editing skills
- Project data ready

## 3 Steps to Contribute

### Step 1: Copy the Right Template (30 seconds)

**Fair launch (no premine)?**
```bash
cp templates/project-template.json data/projects/yourproject.json
```

**Has premine/ICO?**
```bash
cp templates/project-template.json data/projects/yourproject.json
mkdir -p allocations/yourproject
cp templates/genesis-template.json allocations/yourproject/genesis.json
```

### Step 2: Fill in the Data (8 minutes)

**Critical fields table:**
| Field | Where to Find | Example |
|-------|---------------|---------|
| `ticker` | Official docs | "BTC" |
| `launch_date` | Block explorer | "2009-01-03" |
| `current_supply` | Block explorer | 19562000 |
| `max_supply` | Whitepaper | 21000000 |
| `current_block_reward` | Block explorer | 6.25 |
| `block_time_seconds` | Block explorer average | 600 |
| `current_price_usd` | CoinGecko | 67500 |

**Quick calculations:**
```javascript
daily_emission = (86400 / block_time_seconds) * current_block_reward
annual_inflation_pct = (daily_emission * 365 / current_supply) * 100
fdmc = current_price_usd * max_supply
```

**CRITICAL:** Delete all lines starting with `_comment` before submitting!

### Step 3: Validate & Submit (90 seconds)
```bash
# Optional validation
python scripts/validate_submission.py yourproject

# Commit and push
git add data/projects/yourproject.json
git commit -m "Add [Project Name] tokenomics"
git push origin main
```

Create PR on GitHub. Done!

## Data Source Shortcuts

| Data Type | Best Sources |
|-----------|--------------|
| Supply/emission | Blockchain.com, Blockchair, project explorer |
| Price/market cap | CoinGecko, CoinMarketCap |
| Mining stats | WhatToMine, Minerstat |
| Investor info | Crunchbase, project blog, Twitter |
| Vesting | Project docs, Etherscan (if on-chain) |

## Common Mistakes (5-Second Checklist)

- [ ] Deleted all `_comment` lines?
- [ ] Provided data sources for each claim?
- [ ] Percentages sum to 100%?
- [ ] Dates in YYYY-MM-DD format?
- [ ] Data less than 30 days old?

## Need More Detail?

→ Read [CONTRIBUTING.md](CONTRIBUTING.md) for comprehensive guide

## Stuck?

→ Check [examples/](examples/) for completed submissions
→ Open an [Issue](../../issues) with `question` label
