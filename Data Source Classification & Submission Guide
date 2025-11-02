# Data Source Classification & Submission Guide

*For contributors to the PoW Tokenomics Tracker*

---

## Overview

This tracker presents **data with source attribution**, not grades or scores. Every data point must clearly indicate where it came from so users can judge credibility themselves.

**Core principle:** Show the data, show the source, let users judge fairness.

---

## 1. Four Source Types

### 🔗 On-Chain
**What it is:** Data extracted directly from blockchain state.

**Examples:**
- Genesis block allocations
- Current block reward  
- Total mined supply
- Transaction history
- Vesting contract code

**Why it matters:** Anyone can verify by running a node or checking block explorers.

**How to use:** Provide links to 2+ block explorers showing the same data.

---

### 📄 Documented
**What it is:** Information in official protocol documentation.

**Examples:**
- Emission schedule (in protocol code)
- Max supply (in consensus rules)
- Launch date (genesis timestamp)
- Team announcements (timestamped blog posts)
- Investor press releases

**Why it matters:** Can be independently located and reviewed, but not necessarily on-chain.

**How to use:** Link to GitHub code, archived announcements, or official documentation.

---

### 💬 Project Claims
**What it is:** Information stated by the project without independent verification.

**Examples:**
- "We raised $8M"
- "15 investors participated"  
- "Team holds 10%"
- Vesting schedules without contracts

**Why it matters:** Cannot independently verify - users decide whether to trust it.

**How to use:** Link to the team's statement, clearly mark as unverified.

---

### ❓ Unknown / Missing
**What it is:** Data doesn't exist, is lost, or we're showing speculation.

**Examples:**
- Missing blockchain data
- Undisclosed information
- Speculation based on circumstantial evidence
- Community estimates

**Why it matters:** Users should know when data is absent or speculative.

**How to use:** Explicitly state what's missing and why verification is impossible.

---

## 2. Visual Indicators

### Icons

**🔗 On-Chain**
```
Usage: "Max supply: 21M 🔗"
Tooltip: "Source: On-chain data (verifiable via block explorer)"
```

**📄 Documented**  
```
Usage: "Launch: Nov 7, 2021 📄"
Tooltip: "Source: Protocol documentation"
```

**💬 Project Claims**
```
Usage: "Raised: $8M 💬"
Tooltip: "Source: Project statement (unverified)"
```

**❓ Unknown**
```
Usage: "Investor allocations: Not disclosed ❓"
Tooltip: "Data not available"
```

### In Tables
```markdown
| Metric              | Value    | Source        |
|---------------------|----------|---------------|
| Max Supply          | 1B       | 🔗 On-Chain   |
| Emission Schedule   | Declining| 📄 Documented |
| ICO Amount Raised   | $8M      | 💬 Claimed    |
| Individual Investors| Unknown  | ❓ Missing    |
```

---

## 3. Handling Conflicting Information

**When sources disagree, show all sources without picking a winner** (unless blockchain contradicts documentation—blockchain wins).

### Template for Conflicts
```markdown
🚨 CONFLICTING INFORMATION

Max supply:
- 🔗 Blockchain shows: 1.5B tokens mined
- 📄 Whitepaper states: 1B max supply  
- Note: Discrepancy unresolved. Blockchain data reflects current state; 
  documentation may be outdated.
```

### When to Show Ranges
```markdown
Circulating supply: 500-550M 🔗
- Explorer A: 500M
- Explorer B: 550M
- Note: Difference likely due to varying "circulating" definitions
```

---

## 4. Documenting Missing Information

Create a prominent section showing what cannot be verified:
```markdown
## ⚠️ Missing Information

**Allocation Details:**
- Individual investor names and amounts (Project disclosed "80 contributors" 
  but no breakdown)
- Team member wallet addresses (Claimed 10% allocation but addresses not public)
- Vesting contract addresses (No smart contracts to verify claimed vesting)

**Historical Data:**
- Transaction records Nov 2021 - May 2022 (Blockchain data not available)
- Early mining distribution (Period covers 7.8B KAS - 27% of supply)

**Financial Details:**
- SEC filings (None found for U.S. investors)
- Individual VC investment amounts (Only total $8M disclosed)
```

**Rules:**
- State what's missing specifically
- Explain why it cannot be verified
- Do NOT speculate about motives ("team is hiding...") ❌
- Do NOT editorialize ("suspiciously absent...") ❌

---

## 5. Labeling Speculation & Analysis

When presenting estimates or analytical conclusions:
```markdown
## 🔍 Analysis & Estimates

**The following are estimates, not verified facts:**

**Suspected Insider Mining:**
- **Basis:** Network hashrate reached 1.2 TH/s in first week despite no ASIC 
  availability
- **Evidence:** [Hashrate charts], [Launch timeline analysis]
- **Estimate:** 1-6B KAS (3.5-21% of supply) may have been mined with 
  informational advantage
- **Confidence:** Speculative - based on circumstantial evidence
```

**Rules:**
- Always show your reasoning
- Never present speculative numbers as facts
- Separate speculation from verified data
- Use 🔍 icon consistently for analytical sections

---

## 6. Source Attribution Rules

### For Every Data Point, Answer:

1. **Where did this number come from?**
2. **Can someone else verify it?**
3. **If sources conflict, what do they each say?**

### Good Examples

✅ **Good:**
```markdown
ICO raised: $8M 💬
Source: Team announcement (Sept 2021) [link]
Note: No SEC filing found, no investor confirmations
```

✅ **Good:**
```markdown
Daily emission: 33,091 ALPH 🔗
Source: Calculated from block reward (0.18 ALPH) × blocks/day (172,800)
Verified: [Block explorer link]
```

### Bad Examples

❌ **Bad:**
```markdown
ICO raised: $8M ✓ VERIFIED
```
→ Don't add editorial judgment ("verified")

❌ **Bad:**
```markdown
Team allocation: 10%
```
→ No source indicated. Reader doesn't know if this is on-chain, documented, or claimed.

---

## 7. Page Structure Template

Every project page should follow this structure:
```markdown
# [Project Name] Tokenomics Analysis

## Data Sources Overview

This page uses the following source types:

🔗 **On-Chain** - Verifiable via blockchain  
📄 **Documented** - In protocol code/official docs  
💬 **Project Claims** - Team statements (unverified)  
❓ **Unknown** - Data not available

**Source Breakdown:**
- 🔗 On-chain: 15 metrics
- 📄 Documented: 8 metrics
- 💬 Unverified claims: 5 metrics
- ❓ Missing data: 6 metrics

*Users should independently verify any claims important to their decisions.*

---

## Core Metrics

### Supply & Emission
- **Max Supply:** 21M 🔗 [[Source](link)]
- **Current Supply:** 19.5M 🔗 [[Explorer](link)]
- **Daily Emission:** 900 BTC 🔗 [[Calculation](link)]
- **Annual Inflation:** 1.74% 📄 [[Formula](link)]

### Genesis Allocation  
- **Total Premine:** 0% 🔗 [[Genesis block](link)]
- **Team Allocation:** 0% 🔗
- **Investor Allocation:** 0% 🔗
- **Public Mining:** 100% 🔗

### Fundraising
- **Total Raised:** $0 (no ICO) 🔗
- **Presale Price:** N/A
- **Investor Count:** 0 🔗

---

## 🔗 On-Chain Verified Data

[List all blockchain-verifiable metrics with explorer links]

---

## 📄 Protocol Documented Data

[List all data from code/docs with GitHub/doc links]

---

## 💬 Project Claims (Unverified)

[List all team statements that cannot be independently verified]

---

## ⚠️ Missing Information

[List all undisclosed or unavailable data]

---

## 🔍 Analysis & Estimates  

[Clearly labeled speculation and calculations]

---

## 🚨 Conflicting Information

[Document any discrepancies between sources]

---

**Last Updated:** [Date]  
**Contributor:** [Name]  
**Data Sources:** [Number] total citations
```

---

## 8. Contributor Checklist

Before submitting, verify:

### ✅ Source Attribution

- [ ] Every number has a source icon (🔗📄💬❓)
- [ ] 🔗 On-chain data includes block explorer links (2+ explorers if possible)
- [ ] 📄 Documented data includes GitHub/whitepaper links
- [ ] 💬 Project claims include announcement links and "unverified" note
- [ ] ❓ Unknown items explain why data is unavailable

### ✅ Conflict Handling

- [ ] Listed all conflicting sources when they disagree
- [ ] Did NOT pick a winner (unless blockchain contradicts docs)
- [ ] Explained possible reasons for discrepancies
- [ ] Used 🚨 icon for major conflicts

### ✅ Missing Information Section

- [ ] Listed all data that couldn't be found
- [ ] Did NOT speculate about WHY it's missing
- [ ] Specified what evidence would fill the gap
- [ ] Used ⚠️ icon for this section

### ✅ Speculation & Analysis

- [ ] Marked all estimates with 🔍 icon
- [ ] Showed reasoning/calculation for estimates
- [ ] Clearly separated from verified facts
- [ ] Included confidence level ("speculative," "estimated," etc.)

### ✅ No Editorial Language

- [ ] Did NOT use words like "verified" ✓ or "reliable" or "trustworthy"
- [ ] Did NOT use judgmental language ("only claims," "merely," "suspiciously")
- [ ] Did NOT editorialize about team motives
- [ ] Stuck to factual source attribution

### ✅ Links & Citations

- [ ] All URLs are functional
- [ ] Used archive links for announcements (archive.org)
- [ ] Block explorer links point to specific txs/addresses/blocks
- [ ] GitHub links reference specific commits or files (not just main page)

### ✅ Calculations Shown

- [ ] All derived metrics show their formula
- [ ] Parity timelines show calculation method
- [ ] ROI calculations show all inputs (entry price, current price, inflation)
- [ ] Mining cost estimates show assumptions (hardware, electricity rate)

---

## 9. Common Mistakes to Avoid

### ❌ Don't Add Subjective Judgments

**Wrong:**
```markdown
Max supply: 21M ✓ VERIFIED AND TRUSTWORTHY
```

**Right:**
```markdown
Max supply: 21M 🔗
Source: Bitcoin consensus rules [GitHub link]
```

---

### ❌ Don't Editorialize About Missing Data

**Wrong:**
```markdown
Team allocation: Unknown (suspiciously, the team refuses to disclose this)
```

**Right:**
```markdown
Team allocation: Not disclosed ❓
Note: Project documentation does not provide team wallet addresses
```

---

### ❌ Don't Present Speculation as Fact

**Wrong:**
```markdown
Insider mining: 3% of supply
```

**Right:**
```markdown
Suspected insider mining: 1-6% of supply 🔍
Basis: Hashrate patterns during low public awareness period
Confidence: Speculative
[Link to analysis]
```

---

### ❌ Don't Pick Winners in Conflicts (Usually)

**Wrong:**
```markdown
Max supply: 1.5B (whitepaper is outdated and wrong)
```

**Right:**
```markdown
🚨 CONFLICTING INFORMATION
Max supply:
- 🔗 Blockchain: 1.5B tokens mined
- 📄 Whitepaper: 1B stated as max
Note: Blockchain reflects current state; documentation may need updating
```

**Exception:** When blockchain contradicts documentation, blockchain wins:
```markdown
Max supply: 1.5B 🔗 (actual mined supply)
Note: Whitepaper claims 1B 📄, but blockchain has exceeded this
```

---

## 10. Quick Reference

### What Goes Where?

| Data Type | Source Icon | Link Required | Notes |
|-----------|-------------|---------------|-------|
| Genesis allocation | 🔗 | Yes - explorer | Check 2+ explorers |
| Block reward | 🔗 | Yes - explorer | Current reward |
| Emission schedule | 📄 | Yes - GitHub | Protocol code |
| Max supply | 📄 | Yes - GitHub | Consensus rules |
| ICO raised | 💬 | Yes - announcement | Mark unverified |
| Team claims | 💬 | Yes - blog/tweet | Mark unverified |
| Missing data | ❓ | No | Explain why missing |
| Speculation | 🔍 | Yes - methodology | Show reasoning |

---

### When in Doubt

1. **Blockchain vs documentation?** → Blockchain wins
2. **Can't verify a claim?** → Mark as 💬 Project Claims
3. **Data missing?** → Use ❓ and explain why
4. **Making an estimate?** → Use 🔍 and show calculation
5. **Sources disagree?** → Show all sources with 🚨

---

## 11. Examples of Complete Entries

### Example 1: Bitcoin (High Transparency)
```markdown
## Supply Metrics

- **Max Supply:** 21,000,000 BTC 🔗 [[Consensus rules](link)]
- **Current Supply:** 19,562,000 BTC 🔗 [[Blockchain.com](link)] [[Blockchair](link)]
- **Emission Remaining:** 1,438,000 BTC 🔗 (21M - 19.562M)
- **Annual Inflation:** 1.74% 📄 [[Calculation](link)]

## Genesis Allocation

- **Total Premine:** 0% 🔗 [[Genesis block](link)]
- **Team Allocation:** 0% 🔗
- **Investor Allocation:** 0% 🔗
- **Fair Launch:** Yes 🔗 (All supply from mining)

## ⚠️ Missing Information

None. Bitcoin has complete transparency from genesis.

## 🔍 Analysis

**Satoshi's Holdings:** ~1.1M BTC estimated 🔍
- Basis: Block pattern analysis of early mining
- Method: Attributed blocks from 2009 with similar patterns
- Confidence: Community consensus estimate
- [Analysis by Sergio Lerner](link)
```

---

### Example 2: Kaspa (Moderate Transparency with Gaps)
```markdown
## Supply Metrics

- **Max Supply:** 28,704,026,601 KAS 📄 [[Protocol code](link)]
- **Current Supply:** 26,850,000,000 KAS 🔗 [[KaspaExplorer](link)]
- **Circulating Supply:** 26,850,000,000 KAS 🔗 (No lockups)

## Genesis Allocation

- **Total Premine:** 0% 🔗 [[Genesis block](link)]
- **Development Mining:** 700-850M KAS 💬 [[Team wiki](link)]
  - Team claims this amount was mined using rented cloud infrastructure
  - Period: Nov 2021 - May 2022
  - Recipients: Polychain Capital investors, ex-DAGLabs employees
  - Cannot verify on-chain (transaction data missing)

## Fundraising

- **Total Raised:** $8M 💬 [[Team wiki](link)]
  - Lead: Polychain Capital
  - Additional: Accomplice, Genesis Mining
  - Individual amounts: Not disclosed ❓
  - SEC filings: None found ❓

## ⚠️ Missing Information

**Transaction History:**
- Nov 2021 - May 2022 records unavailable ❓
- Affects 7.8B KAS (27% of max supply)
- No full nodes exist with complete history
- Impossible to verify distribution during this period

**Investor Details:**
- Individual investor allocations ❓
- Individual VC investment amounts ❓  
- Token purchase prices ❓
- Vesting terms ❓

## 🔍 Suspected Issues

**Missing Blockchain Data:**
- **Period:** Nov 2021 - May 2022 (6 months)
- **Impact:** 7.8B KAS mined (27% of supply) cannot be audited
- **Status:** Data permanently unavailable per community investigations
- **Evidence:** [[Forum thread](link)] [[Developer Discord](link)]

**Suspected Insider Mining:**
- **Estimate:** 1-6B KAS (3.5-21% of supply) may involve informational advantage
- **Basis:** High hashrate in first weeks despite limited public awareness
- **Evidence:** [[Hashrate analysis](link)]
- **Confidence:** Speculative
```

---

## 12. Final Reminders

**The goal of this tracker is transparency, not judgment.**

✅ **DO:**
- Show sources clearly
- Document missing information
- Present conflicts without resolution
- Mark speculation explicitly
- Link to primary sources

❌ **DON'T:**
- Grade projects (A/B/C)
- Call data "verified" or "trustworthy"
- Editorialize about team motives
- Present speculation as fact
- Hide data gaps

**Remember:** Your job is to show the data and its provenance. The user's job is to judge whether they trust it.

---

**Questions?** Open an issue on GitHub.

**Contributing?** Submit a PR following this guide. All submissions reviewed for source attribution quality.
