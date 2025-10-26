## New Project Submission: [Project Name]

**Project:** [e.g., Bitcoin, Kaspa, Example Coin]  
**Ticker:** [e.g., BTC, KAS, EXC]  
**Launch Type:** [Fair Launch / Premine / ICO / IEO]  
**Premine:** [Yes X% / No]

---

### 📊 Key Findings

**Allocation Summary:**
- Mining/Staking: X%
- Team: X%
- Investors: X%
- Foundation/Treasury: X%
- Community: X%

**Notable Points:**
- [e.g., "Investors paid $0.01, current price $0.50 = 50x ROI"]
- [e.g., "Miner parity in 4.3 years (Feb 2030)"]
- [e.g., "Only 2 out of 15 investors disclosed"]
- [e.g., "Suspected insider mining in first 3 months"]

---

### ✅ Data Sources Checklist

Please check ALL sources you've used:

#### Official Sources
- [ ] Official tokenomics document: [URL]
- [ ] Whitepaper: [URL]
- [ ] Project blog/announcements: [URL]
- [ ] Official GitHub repository: [URL]

#### Blockchain Verification
- [ ] Block explorer stats: [URL]
- [ ] Token contract address: [Address + Explorer URL]
- [ ] Vesting contract address (if applicable): [Address + Explorer URL]
- [ ] Genesis block verification: [URL]

#### Market Data
- [ ] CoinGecko: [URL]
- [ ] CoinMarketCap: [URL]
- [ ] DEX aggregator (if applicable): [URL]

#### Investor/Funding Information
- [ ] VC portfolio pages: [List VCs + URLs]
- [ ] Crunchbase: [URL]
- [ ] Funding announcements: [URLs]
- [ ] Press releases: [URLs]

#### Community Research (if applicable)
- [ ] Third-party analysis: [URL]
- [ ] On-chain investigations: [URL]
- [ ] Community discussions: [URL]

**Note:** If any data is "suspected" or unverified, clearly label it as such in the JSON.

---

### ✅ Validation Checklist

Before submitting, confirm you've completed:

#### Technical Validation
- [ ] Ran `python scripts/validate_submission.py [project-name]` successfully
- [ ] All percentages sum to 100%
- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] JSON files have no syntax errors
- [ ] Removed all `_INSTRUCTIONS`, `_NOTE`, and comment blocks from JSON

#### Data Quality
- [ ] All required fields (marked ⚠️) are filled in
- [ ] Supply calculations are correct (pct_mined matches current/max)
- [ ] Vesting schedules match official documentation
- [ ] Mining/staking costs calculated with sources
- [ ] Market data is recent (within last 7 days)

#### Transparency & Sourcing
- [ ] Every claim has a source URL in the `sources` section
- [ ] Known investor names listed individually
- [ ] Unknown/undisclosed investors counted and noted
- [ ] "Community" funds properly categorized (Foundation vs truly community-controlled)
- [ ] Any suspected insider activity labeled as unverified

#### Project-Specific
- [ ] For Fair Launch: Confirmed no premine/founder allocation
- [ ] For Premine: All allocation tiers properly categorized
- [ ] For Suspected Insiders: Evidence listed, confidence level stated, counterarguments included
- [ ] For Hybrid: Both mining and staking data included

---

### 🔍 Notable Concerns or Disputes

**Are there any known controversies about this project's tokenomics?**
- [ ] No known controversies
- [ ] Yes, see details below:

[If yes, describe:]
- Issue: [e.g., "Team claims fair launch but on-chain data suggests otherwise"]
- Evidence: [Links to analysis, on-chain data, etc.]
- Team Response: [Link to official response if available]
- Your Assessment: [Your judgment with reasoning]

---

### 📝 Additional Context

**Why did you add this project?**
[e.g., "Requested by community", "Noticed missing from tracker", "Found interesting tokenomics pattern"]

**Any special challenges in gathering data?**
[e.g., "Vesting contract not verified on Etherscan", "Team deleted original tokenomics doc", "Conflicting information from multiple sources"]

**Confidence in your data (1-5):**
- [ ] 1 - Low confidence, limited sources
- [ ] 2 - Some uncertainty, missing key details  
- [ ] 3 - Moderate confidence, most data verified
- [ ] 4 - High confidence, well-documented
- [ ] 5 - Very high confidence, all data verified on-chain

---

### 🎯 Comparison to Bitcoin (Fair Launch Baseline)

How does this project compare to Bitcoin's fair launch?

**Similarities:**
- [e.g., "No premine", "Pure PoW", "Public launch"]

**Differences:**
- [e.g., "66.7% premine vs Bitcoin's 0%", "VCs got 50x ROI vs Bitcoin's equal opportunity mining", "Miners won't achieve parity until 2030 vs Bitcoin's day 1"]

---

### 📎 Files Changed

Please list all files added or modified:

```
data/projects/[project-name].json
allocations/[project-name]/genesis.json
allocations/[project-name]/insiders/[any-additional-files].json
mining-data/[project-name]/[any-csv-files].csv
```

---

### 🙋 Questions for Reviewers

**Do you need feedback on any specific aspects?**
- [ ] Categorization of allocations (is my tier assignment correct?)
- [ ] Suspected insider mining claims (is my evidence sufficient?)
- [ ] Source quality (are my sources credible enough?)
- [ ] Calculation accuracy (did I calculate parity correctly?)
- [ ] Other: [Specify]

---

### 📜 Contributor Statement

By submitting this PR, I confirm that:

- [ ] All data is sourced and cited
- [ ] I have no financial interest in this project (or disclosed below)
- [ ] I have not been compensated by the project team
- [ ] I am not attempting to manipulate perception through selective data
- [ ] I understand this data will be public and may be used for research/analysis

**Financial Disclosure (if applicable):**
[e.g., "I hold 1000 tokens of this project" or "No holdings"]

---

### 🚀 Ready for Review

- [ ] I have completed all checklists above
- [ ] I have reviewed my submission for accuracy
- [ ] I am ready for maintainer review

---

**Thank you for contributing to crypto transparency!** 🙏

Maintainers will review your submission and may request changes or additional sources.
