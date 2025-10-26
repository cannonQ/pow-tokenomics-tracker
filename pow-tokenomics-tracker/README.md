# PoW Tokenomics Tracker - Contribution System

**Simple, DefiLlama-style contribution workflow:** Just add a file, submit a PR.

---

## For Contributors

### 🚀 Quick Start (3 steps)

1. **Copy template** → Fill it in → Delete comment lines
2. **Commit** to your fork
3. **Submit PR** (template auto-loads)

That's it! See [QUICK_START.md](QUICK_START.md) for details.

### 📚 Resources

| Document | Use When |
|----------|----------|
| [QUICK_START.md](QUICK_START.md) | You want to submit fast (3-min guide) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | You want detailed instructions |
| [templates/](templates/) | You need the JSON templates |
| [examples/](examples/) | You want to see completed submissions |
| [scripts/validate_submission.py](scripts/validate_submission.py) | You want to check your work |

---

## File Structure

```
pow-tokenomics-tracker/
│
├── templates/                    ← START HERE
│   ├── project-template.json     (Copy this for every project)
│   ├── genesis-template.json     (Copy only if premine)
│   └── README.md
│
├── examples/                     ← STUDY THESE
│   ├── bitcoin-example.json      (Fair launch example)
│   ├── example-coin.json         (Premine example)
│   ├── example-coin-genesis.json
│   └── README.md
│
├── data/projects/                ← PUT YOUR PROJECT HERE
│   └── yourproject.json
│
├── allocations/                  ← PUT GENESIS DATA HERE (if needed)
│   └── yourproject/
│       └── genesis.json
│
├── scripts/
│   └── validate_submission.py    ← RUN THIS BEFORE PR (optional)
│
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md  (Auto-loads when you submit)
│
├── QUICK_START.md                ← 3-minute guide
└── CONTRIBUTING.md               ← Detailed guide
```

---

## Submission Workflow

### For Fair Launch Projects (No Premine)

```bash
# 1. Copy template
cp templates/project-template.json data/projects/yourproject.json

# 2. Edit file (see examples/bitcoin-example.json)
# - Fill in all fields
# - Delete all _comment lines
# - Add data sources

# 3. Validate (optional)
python scripts/validate_submission.py yourproject

# 4. Commit & PR
git add data/projects/yourproject.json
git commit -m "Add yourproject tokenomics"
git push origin main
# Create PR on GitHub
```

### For Premined Projects

```bash
# 1. Copy templates
cp templates/project-template.json data/projects/yourproject.json
mkdir -p allocations/yourproject
cp templates/genesis-template.json allocations/yourproject/genesis.json

# 2. Edit both files (see examples/example-coin*)
# - Fill in all fields
# - Delete all _comment lines
# - Break down premine by tier

# 3. Validate
python scripts/validate_submission.py yourproject

# 4. Commit & PR
git add data/projects/yourproject.json allocations/yourproject/genesis.json
git commit -m "Add yourproject tokenomics"
git push origin main
# Create PR on GitHub
```

---

## What the Validator Checks

Run `python scripts/validate_submission.py yourproject` to check:

✅ Valid JSON syntax  
✅ Required fields present  
✅ Math correct (supply, emissions, percentages)  
✅ Dates formatted properly  
✅ URLs valid  
✅ No template comments left in  
✅ Allocations sum to 100%  
✅ Vesting logic makes sense  

**Optional but recommended!** Helps catch errors before PR.

---

## PR Review Process

1. **You submit** → PR auto-opens with template
2. **Auto-checks run** (JSON validation)
3. **Community reviews** (1-3 days)
   - Verify data sources
   - Check calculations
   - Cross-reference claims
4. **Merged or feedback** given
5. **Goes live** on tracker!

---

## Data Quality Standards

### ✅ Required for Approval

- **Verifiable sources** for every claim
- **Current data** (<30 days old)
- **Accurate math** (we'll verify)
- **Neutral tone** (facts, not marketing)

### 🎯 Nice to Have

- Complete investor disclosure
- On-chain contract addresses
- Historical context in notes
- Multiple source verification

---

## Philosophy: Show Data, Let Users Judge

We **don't** create synthetic "fairness scores" because:
- They hide manipulation
- They're gameable
- Users can't verify them

We **do** show:
- Raw allocation numbers
- Miner parity timelines
- Cost economics
- Transparency gaps

**The data speaks for itself.**

---

## Examples to Learn From

### Bitcoin (Fair Launch)
```json
{
  "project": "bitcoin",
  "has_premine": false,
  "launch_type": "fair",
  ...
}
```
👉 No genesis file needed!

### Example Coin (66.7% Premine)
```json
// Main file
{
  "project": "example-coin",
  "has_premine": true,
  ...
}

// allocations/example-coin/genesis.json
{
  "total_genesis_allocation_pct": 66.7,
  "allocation_tiers": {
    "tier_1_profit_seeking": {...},
    "tier_2_entity_controlled": {...}
  }
}
```
👉 Both files required!

See full examples in `examples/` directory.

---

## Common Mistakes

❌ Leaving `_comment` fields in JSON  
❌ No data sources provided  
❌ Percentages don't sum to 100%  
❌ Wrong date format (use YYYY-MM-DD)  
❌ Outdated data (>30 days)  
❌ Missing genesis file when has_premine=true  

**Tip:** Study the examples first!

---

## Getting Help

**Have questions?**

1. Check [CONTRIBUTING.md](CONTRIBUTING.md) - comprehensive guide
2. Look at [examples/](examples/) - real submissions
3. Open an [Issue](../../issues) - we'll help!

**Found a bug in the templates or docs?**
- Open an issue or submit a fix PR

---

## For Project Maintainers

### Updating Existing Projects

Data gets stale! To update:

```bash
# 1. Edit the existing file(s)
# 2. Update last_updated date
# 3. Add note about what changed

git add data/projects/yourproject.json
git commit -m "Update yourproject - Q4 2025 data"
git push origin main
# Create PR with "Update" in title
```

### Responding to PRs

If your project is submitted and you want to clarify:
- Comment on the PR with corrections
- Provide sources for accurate data
- Keep it factual and professional

---

## Why Contribute?

By adding accurate tokenomics data, you help:

🔍 **Miners** - understand if a project is fair  
💰 **Investors** - see insider allocations  
📊 **Researchers** - analyze PoW economics  
🏗️ **Community** - make informed decisions  

**Every contribution brings more transparency to crypto.**

---

## Thank You! 🙏

This project only works because of contributors like you.

Whether you're adding Bitcoin or a new project nobody's heard of, **your contribution matters**.

**Let's make PoW tokenomics transparent together.** 🚀

---

## Quick Links

- 🚀 [Quick Start](QUICK_START.md) - 3-minute guide
- 📖 [Contributing Guide](CONTRIBUTING.md) - detailed instructions
- 📝 [Templates](templates/) - copy these
- 💡 [Examples](examples/) - study these
- 🔧 [Validator](scripts/validate_submission.py) - check your work
- ❓ [Issues](../../issues) - get help

**Ready? Go to [QUICK_START.md](QUICK_START.md) and start contributing!**
