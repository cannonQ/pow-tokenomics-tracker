# Data Fields Manifest — What To Find

This is the single source of truth for **what data a project needs** and **where to find it**.
It is written for agents: the `/acquire-project` skill and its research subagents read this file to
decide which fields are required, which are conditional, and which sources to search.

Field **names and structure are authoritative** — they mirror `templates/project-template.json` and
`templates/genesis-template.json` exactly, so output drops straight into the repo and passes
`scripts/validate_submission.py`.

> **Derived fields are never researched.** Anything tagged `[DERIVED]` is computed by
> `scripts/compute_derived.py` from other fields. Subagents must leave them out; the orchestrator
> fills them at CP4.

---

## 1. Conditional matrix — which files & blocks apply

Classify the project first (consensus + `launch_type`), then include only what applies.

| launch_type / flag | `data/projects/<p>.json` | `allocations/<p>/genesis.json` | vesting CSV | extra blocks to fill |
|---|---|---|---|---|
| `fair` | ✅ always | — | — | — |
| `fair_with_suspicion` | ✅ | ✅ (forensic only) | — | `suspected_insider_mining`, often `blockchain_data_complete=false` + `missing_data` |
| `premine` / `ico` / `private_sale` | ✅ (`has_premine=true`) | ✅ | ✅ if any bucket vests | `allocation_tiers`, `vesting_waterfall` |
| `has_treasury_emission=true` (e.g. Ergo) | ✅ (`has_premine=false`) | ✅ (`has_emission_allocation=true`) | emission CSV | `treasury_emission` |
| `dev_tax` present (e.g. Zcash-style) | ✅ | ✅ | — | `dev_tax` |

File-generation helpers (reuse, do not hand-write JSON for these):
- vesting CSV → JSON: `scripts/csv_to_vesting_json.py`
- emission CSV → JSON: `scripts/csv_to_emission_json.py`

---

## 2. Field catalog by group

Each field lists: **where to look** and **example search queries**. Every researched value must come
back with a `source_url` and a `confidence` (high/med/low). Use `null` or `"unknown"` + a `notes`
reason when no source can be found — never guess.

### Group: identity  → owned by orchestrator (CP1)
| field | source | example query |
|---|---|---|
| `project`, `ticker` | CoinGecko, official site | `<name> coingecko`, `<name> ticker symbol` |
| `consensus`, `algorithm` | whitepaper, official docs | `<name> consensus algorithm whitepaper` |
| `launch_date` | block explorer (genesis block), docs | `<name> mainnet launch date`, `<name> genesis block date` |
| `launch_type`, `has_premine` | whitepaper, tokenomics docs | `<name> premine`, `<name> token distribution genesis` |

### Group: supply  → `supply-emission-researcher`
| field | source | example query |
|---|---|---|
| `max_supply` (null if uncapped) | whitepaper, official docs | `<name> max supply cap` |
| `current_supply` | project block explorer | `<name> circulating supply explorer` |
| `pct_mined` `[DERIVED]` | — | — |
| `emission_remaining` `[DERIVED]` | — | — |

### Group: emission  → `supply-emission-researcher`
| field | source | example query |
|---|---|---|
| `current_block_reward` (include dev tax) | block explorer, docs | `<name> current block reward` |
| `block_time_seconds` | block explorer (avg of last ~1000 blocks) | `<name> average block time` |
| `halving_schedule[]` | whitepaper, docs | `<name> halving schedule emission curve` |
| `daily_emission` `[DERIVED]` | — | — |
| `annual_inflation_pct` `[DERIVED]` | — | — |

> **No `mining` group.** The consuming site renders Supply / Emission / Investors / Analysis / Market
> only — there is no Mining tab, and "miner parity" is computed client-side from
> `daily_emission`, `max_supply`, `launch_date`, and `total_genesis_allocation_pct` (all already
> collected elsewhere). Do **not** research hashrate, difficulty, ASIC-resistance, cost-to-mine, or
> pool distribution — none of it is displayed.

### Group: market_data  → `market-data-researcher`
| field | source | example query |
|---|---|---|
| `current_price_usd` | CoinGecko, CMC | `<name> price` |
| `daily_volume` | CoinGecko, CMC | `<name> 24h trading volume` |
| `fdmc` `[DERIVED]`, `circulating_mcap` `[DERIVED]`, `token_velocity` `[DERIVED]` | — | — |

### Group: data_sources  → assembled by orchestrator
Aggregate every `source_url` the subagents returned into the
`official_docs / block_explorer / market_data` lists (and `funding_data` if applicable for premined
projects). Validator requires real URLs.

### Group: genesis allocation_tiers  → `allocation-researcher` (premine/ICO only)
For each tier (`tier_1_profit_seeking`, `tier_2_entity_controlled`, `tier_3_community`,
`tier_4_liquidity`) and each bucket: `name`, `pct`, `absolute_tokens`, `cost_per_token_usd`, `date`,
`vesting_months`, `cliff_months`, `tge_unlock_pct`, and `investors{known[], unknown_count,
total_investors, notes}`. Build `vesting_waterfall[]` (months 0..N) — emit as a CSV for
`csv_to_vesting_json.py` rather than hand-writing.
- sources: Medium funding announcements, Crunchbase, project tokenomics docs, Etherscan vesting
  contracts, CoinGecko.
- queries: `<name> seed round investors`, `<name> tokenomics vesting schedule`, `<name> raised funding`,
  `<name> foundation treasury allocation`.
- **Honesty rule:** disclose only what's sourced. Use `unknown_count` + `"unknown"` for undisclosed
  investors/amounts.

### Group: special-case blocks  → `forensics-researcher`
| block | when | source / query |
|---|---|---|
| `suspected_insider_mining` | early-advantage suspicion | community analyses, on-chain clustering: `<name> insider mining controversy`. Set `verifiable:false` unless on-chain-proven; link analyses, not rumors. |
| `blockchain_data_complete=false` + `missing_data` | early node/tx history missing | `<name> missing blockchain history early blocks` |
| `dev_tax` | ongoing block-reward cut to team | `<name> dev tax founder reward block reward split` |
| `treasury_emission` | block-reward % to treasury (Ergo-style) | `<name> treasury emission block reward percentage` |

---

## 3. Source priority (tie-breaking during CP3 review)
1. **On-chain / block explorer** for supply, emission, addresses (most authoritative).
2. **Whitepaper / official docs** for design constants (max supply, halving curve, tokenomics).
3. **CoinGecko / CMC** for price, volume, market caps.
4. **Medium / Crunchbase / Twitter** for investor & funding info — corroborate with ≥2 where possible.
5. **Community analyses / on-chain investigations** for forensic & red-flag claims — link the
   analysis, set `verifiable:false` unless on-chain-proven.

When two sources conflict, prefer the higher-priority one and record the discrepancy in `notes`.
