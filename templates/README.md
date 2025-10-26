# Templates Directory

This directory contains template files for contributing project data.

## Files

### `project-template.json`
**Use for:** Every project submission  
**Purpose:** Core project data (supply, emissions, mining, market data)  
**Required:** Yes, always

### `genesis-template.json`
**Use for:** Projects with premine/ICO/presale  
**Purpose:** Genesis allocation breakdown, investor details, vesting schedules  
**Required:** Only if `has_premine: true`

## How to Use

1. **Copy** the appropriate template(s)
2. **Rename** to your project name (lowercase, no spaces)
3. **Fill in** all fields (use `null` for unknown)
4. **Delete** all lines starting with `_comment`
5. **Validate** (optional): `python scripts/validate_submission.py yourproject`
6. **Submit** PR

## Template Features

### Inline Documentation
Every field has a `_comment_fieldname` explaining:
- What the field means
- Expected format/values
- Where to find the data
- Example values

### Smart Defaults
Templates include:
- Common values pre-filled (adjust for your project)
- Calculation formulas in comments
- Links to relevant tools/explorers

### Validation-Ready
Templates are structured to pass validation:
- Correct JSON syntax
- All required fields present
- Proper nesting structure
- Valid date formats

## Examples

**Fair launch project (Bitcoin-style):**
```bash
cp templates/project-template.json data/projects/bitcoin.json
# Edit bitcoin.json
# Set has_premine: false
# No genesis file needed!
```

**Premined project:**
```bash
cp templates/project-template.json data/projects/example-coin.json
mkdir -p allocations/example-coin
cp templates/genesis-template.json allocations/example-coin/genesis.json
# Edit both files
# Set has_premine: true
```

## Need Help?

- 📖 Full guide: [CONTRIBUTING.md](../CONTRIBUTING.md)
- 🚀 Quick start: [QUICK_START.md](../QUICK_START.md)
- ❓ Questions: Open an issue

## Philosophy

These templates follow the **DefiLlama approach**:
- Simple, copy-paste workflow
- No fancy tools required
- Git-native contribution
- Community-driven verification

Just fill in the data, submit a PR, and we'll verify it together!
