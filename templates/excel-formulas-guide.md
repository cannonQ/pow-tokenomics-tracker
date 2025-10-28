# Excel Formulas Guide for Vesting Schedule

When using Excel/Google Sheets to fill out the vesting schedule, these formulas can automate calculations and reduce errors.

## Setup

1. Open `vesting-schedule-template.csv` in Excel/Google Sheets
2. Set up a **parameters section** at the top (before the data table)
3. Apply formulas below to automate calculations

---

## Parameter Setup (Add to top of sheet)

```
Row 1: Project Name: [Your Project]
Row 2: Genesis Date: 2023-01-01
Row 3:
Row 4: Bucket Parameters:
Row 5: Tier | Bucket Name | Total Tokens | Vesting Months | Cliff Months | TGE Unlock %
Row 6: tier_1_profit_seeking | Seed Round | 20000000 | 12 | 0 | 10
Row 7: tier_2_entity_controlled | Treasury | 30000000 | 24 | 6 | 0
Row 8:
Row 9: (Start data table here)
```

---

## Column Formulas

Assume your data table starts at **Row 10** with headers in Row 9.

### Column A: `month`
**Manual entry** (0, 1, 2, 3, ...)

Or use auto-fill:
```excel
A10: 0
A11: =A10+1
(Drag down)
```

---

### Column B: `date`
**Formula:** Add months to genesis date

```excel
B10: =DATE(YEAR($B$2), MONTH($B$2) + A10, DAY($B$2))
```

**Explanation:**
- `$B$2` = Genesis date (absolute reference)
- `A10` = Month number
- Formula adds months to genesis date

**Example:**
- Genesis: `2023-01-01`
- Month 0: `2023-01-01`
- Month 1: `2023-02-01`
- Month 12: `2024-01-01`

---

### Column C: `tier`
**Manual entry** - copy down for each bucket

---

### Column D: `bucket_name`
**Manual entry** - copy down for each bucket

---

### Column E: `unlock_tokens`
**Formula:** Depends on vesting pattern

#### For Linear Vesting:

Set up helper columns (hide these later):
```
Column J: cliff_months (lookup from parameters)
Column K: vesting_months (lookup from parameters)
Column L: total_tokens (lookup from parameters)
Column M: tge_pct (lookup from parameters)
```

**Unlock formula:**
```excel
E10: =IF(A10=0,
    L10 * M10 / 100,  // TGE unlock
    IF(A10 < J10,
        0,  // During cliff
        IF(A10 <= J10 + K10,
            (L10 * (1 - M10/100)) / K10,  // Linear vesting
            0  // After vesting complete
        )
    )
)
```

#### For Quarterly Vesting:

```excel
E10: =IF(A10=0,
    L10 * M10 / 100,  // TGE unlock
    IF(A10 < J10,
        0,  // During cliff
        IF(MOD(A10 - J10, 3) = 0,  // Every 3 months after cliff
            (L10 * (1 - M10/100)) / (K10/3),  // Quarterly amount
            0
        )
    )
)
```

---

### Column F: `unlock_pct_of_bucket`
**Formula:** Percentage of bucket unlocking this month

```excel
F10: =(E10 / L10) * 100
```

Round to 2 decimals:
```excel
F10: =ROUND((E10 / L10) * 100, 2)
```

---

### Column G: `cumulative_tokens`
**Formula:** Sum of all unlocks up to this month for this bucket

```excel
G10: =SUMIFS($E$10:E10, $D$10:D10, D10)
```

**Explanation:**
- Sums `unlock_tokens` (column E)
- From row 10 to current row
- Only for rows matching current `bucket_name`

**Example:** For "Seed Round" at month 12:
- Sums all months 0-12 where bucket_name = "Seed Round"

---

### Column H: `cumulative_pct_of_bucket`
**Formula:** Cumulative percentage of bucket

```excel
H10: =ROUND((G10 / L10) * 100, 2)
```

---

### Column I: `notes`
**Manual entry** - describe the unlock

---

## Complete Example Setup

### Parameters Section (Rows 1-8)

```
| A | B | C | D |
|---|---|---|---|
| Project: | ExampleCoin | | |
| Genesis Date: | 2023-01-01 | | |
| | | | |
| Bucket Parameters: | | | |
| Tier | Bucket | Total Tokens | Vesting Mo | Cliff Mo | TGE % |
| tier_1_profit_seeking | Seed Round | 20000000 | 12 | 0 | 10 |
| tier_2_entity_controlled | Treasury | 30000000 | 24 | 6 | 0 |
```

### Data Table (Rows 10+)

With formulas applied:

```
| A (month) | B (date) | C (tier) | D (bucket) | E (unlock) | F (pct) | G (cum) | H (cum_pct) | I (notes) |
|-----------|----------|----------|------------|------------|---------|---------|-------------|-----------|
| 0 | =DATE(...) | tier_1 | Seed Round | =IF(...) | =ROUND(...) | =SUMIFS(...) | =ROUND(...) | TGE 10% |
| 0 | =DATE(...) | tier_2 | Treasury | =IF(...) | =ROUND(...) | =SUMIFS(...) | =ROUND(...) | Cliff 6mo |
| 1 | =DATE(...) | tier_1 | Seed Round | =IF(...) | =ROUND(...) | =SUMIFS(...) | =ROUND(...) | Linear vest |
| 1 | =DATE(...) | tier_2 | Treasury | =IF(...) | =ROUND(...) | =SUMIFS(...) | =ROUND(...) | Cliff ongoing |
```

---

## VLOOKUP for Parameters

To avoid manual entry, use VLOOKUP to fetch bucket parameters:

### Setup Named Range
1. Select rows 6-7 (bucket parameters)
2. Name it: `BucketParams`

### Formulas with VLOOKUP

```excel
// Column J: cliff_months
J10: =VLOOKUP(D10, BucketParams, 5, FALSE)

// Column K: vesting_months
K10: =VLOOKUP(D10, BucketParams, 4, FALSE)

// Column L: total_tokens
L10: =VLOOKUP(D10, BucketParams, 3, FALSE)

// Column M: tge_pct
M10: =VLOOKUP(D10, BucketParams, 6, FALSE)
```

Now column E's unlock formula automatically references the correct bucket!

---

## Validation Checks

Add these at the bottom of your sheet to catch errors:

### Check 1: Each Bucket Reaches 100%

```excel
// Find last row for each bucket and check cumulative
=IF(
  MAX(IF($D$10:$D$1000="Seed Round", $H$10:$H$1000)) < 99.9,
  "ERROR: Seed Round not 100%",
  "OK"
)
```

### Check 2: No Negative Unlocks

```excel
=IF(
  COUNTIF($E$10:$E$1000, "<0") > 0,
  "ERROR: Negative unlocks found",
  "OK"
)
```

### Check 3: Cumulative Never Decreases

```excel
// Add helper column checking if cumulative < previous cumulative for same bucket
```

---

## Export to CSV

Before running the converter script:

1. **Delete parameter rows** (rows 1-8)
2. **Delete helper columns** (J, K, L, M)
3. **Copy values only** (remove formulas):
   - Select all data
   - Copy
   - Paste Special > Values
4. **Save As CSV:**
   - File > Save As
   - Format: CSV (Comma delimited)
   - Name: `vesting-schedule.csv`

---

## Google Sheets Differences

Most formulas work identically. Key differences:

### Date Formula
```
// Excel
=DATE(YEAR($B$2), MONTH($B$2) + A10, DAY($B$2))

// Google Sheets (same)
=DATE(YEAR($B$2), MONTH($B$2) + A10, DAY($B$2))
```

### SUMIFS
```
// Excel & Google Sheets (same)
=SUMIFS($E$10:E10, $D$10:D10, D10)
```

---

## Tips & Tricks

### Tip 1: Conditional Formatting for Errors

Highlight cells where cumulative > 100%:
```
Format > Conditional Formatting
Formula: =H10 > 100
Format: Red fill
```

### Tip 2: Freeze Panes

Freeze header row so columns stay visible:
```
View > Freeze Panes > Freeze Top Row
```

### Tip 3: Auto-Fill for Multiple Buckets

1. Fill formulas for month 0 for all buckets
2. Select entire row (all buckets)
3. Drag down to auto-fill months 1, 2, 3, ...

### Tip 4: Quick Month Generation

Generate 60 months instantly:
```
A10: 0
A11: =A10+1
Select A10:A11, drag down to A69 (60 months)
```

---

## Common Formula Errors

### #REF! Error
**Cause:** Reference to deleted row/column
**Fix:** Check absolute references ($B$2) are correct

### #VALUE! Error
**Cause:** Text in numeric column
**Fix:** Ensure total_tokens, vesting_months are numbers, not text

### #DIV/0! Error
**Cause:** Division by zero (e.g., total_tokens = 0)
**Fix:** Add IF check: `=IF(L10=0, 0, E10/L10)`

### Wrong Cumulative Total
**Cause:** SUMIFS range includes other buckets
**Fix:** Ensure criteria `$D$10:D10, D10` matches exact bucket name

---

## Example Files

- **Simple CSV:** `templates/vesting-schedule-template.csv`
- **Filled Example:** `allocations/alephium/vesting-schedule.csv`
- **Documentation:** `docs/vesting-schedule-guide.md`

---

## Need Help?

Formula not working? Check:
1. Are parameter cells formatted as numbers? (Right-click > Format Cells)
2. Are bucket names spelled exactly the same in parameters and data table?
3. Did you use absolute references ($B$2) where needed?
4. Did you copy formulas down correctly (select cell, double-click bottom-right corner)?

For more help: https://github.com/anthropics/claude-code/issues
