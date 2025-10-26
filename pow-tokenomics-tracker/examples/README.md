# Examples Directory

These are **real, complete examples** showing what properly filled-out submissions look like.

## Files

### Fair Launch Example (No Premine)
- `bitcoin-example.json` - Complete Bitcoin data (fair launch)
- **Key features:**
  - No premine/ICO
  - All `_comment` fields removed
  - Complete emission schedule
  - Multiple data sources cited
  - Mining economics included

### Premined Project Example
- `example-coin.json` - Main project file (66.7% premine)
- `example-coin-genesis.json` - Genesis allocation breakdown
- **Key features:**
  - Complex allocation tiers
  - Known + unknown investors
  - Vesting waterfall
  - Transparency notes

## How to Use These Examples

### 1. Study Before You Start
Look at these examples to understand:
- What a complete submission looks like
- How to structure allocations
- What level of detail to provide
- How to cite sources

### 2. Reference While Filling
Keep these open while working on your submission:
- Check field formats
- See how to handle unknowns
- Understand tier breakdowns
- Get citation examples

### 3. Compare Before Submitting
Before you submit, compare your work to these:
- ✅ All comments removed?
- ✅ Similar level of detail?
- ✅ Sources provided?
- ✅ Math checks out?

## Key Differences Between Examples

| Aspect | Bitcoin | Example Coin |
|--------|---------|--------------|
| Launch Type | Fair | Premine |
| Genesis File | ❌ Not needed | ✅ Required |
| Investor Info | None | Detailed tiers |
| Transparency | 100% | ~12% (3/25 disclosed) |
| Vesting | None | Complex schedule |

## What Makes These Good Examples

### Bitcoin Example Shows:
✅ Fair launch = simple structure  
✅ No genesis file needed  
✅ Clear emission schedule  
✅ Multiple data source types  
✅ Concise but complete  

### Example Coin Shows:
✅ Complex premine handling  
✅ Tiered allocation system  
✅ Known vs unknown investors  
✅ Vesting waterfall  
✅ Transparency notes  
✅ How to handle incomplete data  

## Common Patterns

### Handling Unknown Investors
```json
"investors": {
  "known": [
    {"name": "Known VC", "pct_of_round": "unknown"}
  ],
  "unknown_count": 13,
  "total_investors": 15,
  "notes": "Only 2 of 15 disclosed"
}
```

### Multiple Data Sources
```json
"data_sources": {
  "official_docs": ["URL1", "URL2"],
  "block_explorer": ["URL1"],
  "market_data": ["URL1", "URL2"]
}
```

### Vesting Cliffs
```json
{
  "vesting_months": 24,
  "cliff_months": 6,
  "tge_unlock_pct": 0
}
```

## Your Turn!

1. **Copy** the appropriate template from `templates/`
2. **Reference** these examples while filling it out
3. **Match** the level of detail and structure
4. **Submit** your PR!

Need help? Check [CONTRIBUTING.md](../CONTRIBUTING.md) or [QUICK_START.md](../QUICK_START.md)
