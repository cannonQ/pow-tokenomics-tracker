# Quick Reference: Adding a Project

**Too busy to read CONTRIBUTING.md? Here's the ultra-quick version:**

---

## 3-Minute Setup

### 1. Copy Template(s)

**Fair launch (no premine):**
```bash
cp templates/project-template.json data/projects/yourproject.json
```

**Has premine:**
```bash
cp templates/project-template.json data/projects/yourproject.json
cp templates/genesis-template.json allocations/yourproject/genesis.json
```

### 2. Fill Required Fields

**In `data/projects/yourproject.json`:**
- `project` - lowercase name (bitcoin, kaspa)
- `ticker` - BTC, KAS, etc.
- `launch_date` - YYYY-MM-DD
- `supply.max_supply` - total cap (or null)
- `supply.current_supply` - mined so far
- `emission.current_block_reward` - current reward
- `emission.block_time_seconds` - avg block time
- `data_sources` - MUST provide URLs

**In `allocations/yourproject/genesis.json` (if premine):**
- `total_genesis_allocation_pct` - % premined
- Break down in `allocation_tiers`
- List known investors
- Add vesting schedules

### 3. Delete Comments

Remove ALL lines starting with `_comment` before submitting!

### 4. Submit PR

Done! We'll review and merge.

---

## Where to Find Data

| Need | Where to Look |
|------|--------------|
| Supply | Block explorer |
| Block reward | Block explorer (recent blocks) |
| Block time | Block explorer (average) |
| Hashrate | Mining pools, WhatToMine |
| Price | CoinGecko, Livecoinwatch |
| VCs | Medium, Twitter, CrunchBase |

---

## Quick Calculations

```javascript
// Daily emission
daily_emission = (86400 / block_time) * block_reward

// % mined
pct_mined = (current_supply / max_supply) * 100

// Annual inflation
annual_inflation = (daily_emission * 365 / current_supply) * 100

// FDMC
fdmc = price * max_supply
```

---

## Common Mistakes

❌ Leaving `_comment` fields in JSON  
❌ Percentages don't sum to 100%  
❌ No data sources provided  
❌ Wrong date format (use YYYY-MM-DD)  
❌ Outdated data (>30 days old)

---

## Need Help?

1. Check examples: `data/projects/bitcoin.json`
2. Read full guide: `CONTRIBUTING.md`
3. Open an issue with `question` label

**That's it!** Thanks for contributing! 🚀
