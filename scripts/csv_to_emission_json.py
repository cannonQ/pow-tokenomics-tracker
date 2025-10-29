#!/usr/bin/env python3
"""
Convert emission schedule CSV to JSON format with validation.

Usage:
    python csv_to_emission_json.py <csv_file_path> [genesis_json_path]

Example:
    python csv_to_emission_json.py allocations/ergo/emission-schedule.csv allocations/ergo/genesis.json
"""

import csv
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any


def load_genesis_json(genesis_path: Path) -> Dict[str, Any]:
    """Load genesis.json for validation."""
    if not genesis_path.exists():
        return {}

    with open(genesis_path, 'r') as f:
        return json.load(f)


def extract_bucket_names_from_genesis(genesis_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Extract bucket names from genesis.json allocation_tiers."""
    bucket_names = defaultdict(list)

    if 'allocation_tiers' not in genesis_data:
        return bucket_names

    for tier_name, tier_data in genesis_data['allocation_tiers'].items():
        if 'buckets' in tier_data and isinstance(tier_data['buckets'], list):
            for bucket in tier_data['buckets']:
                if 'name' in bucket:
                    bucket_names[tier_name].append(bucket['name'])

    return bucket_names


def validate_emission_mechanism(genesis_data: Dict[str, Any], bucket_name: str, tier: str) -> bool:
    """Check if bucket has allocation_mechanism set to block_reward_emission."""
    if 'allocation_tiers' not in genesis_data:
        return True  # Skip validation if no tiers

    tier_data = genesis_data['allocation_tiers'].get(tier, {})
    buckets = tier_data.get('buckets', [])

    for bucket in buckets:
        if bucket.get('name') == bucket_name:
            mechanism = bucket.get('allocation_mechanism', '')
            if mechanism and mechanism != 'block_reward_emission':
                return False

    return True


def validate_csv_data(rows: List[Dict], genesis_data: Dict[str, Any]) -> List[str]:
    """Validate CSV data and return list of errors."""
    errors = []

    # Extract bucket names from genesis if available
    valid_bucket_names = extract_bucket_names_from_genesis(genesis_data)

    # Track cumulative by bucket
    prev_cumulative = defaultdict(lambda: 0.0)

    for i, row in enumerate(rows, start=2):  # +2 for header and 0-indexing
        month = int(row['month'])
        tier = row['tier']
        bucket_name = row['bucket_name']
        emission_tokens = float(row['emission_tokens'])
        cumulative_tokens = float(row['cumulative_tokens'])
        cumulative_pct = float(row['cumulative_pct_of_bucket'])

        bucket_key = f"{tier}::{bucket_name}"

        # Validation 1: No negative emissions
        if emission_tokens < 0:
            errors.append(f"Row {i}: Negative emission_tokens ({emission_tokens}) for {bucket_key}")

        # Validation 2: Cumulative never decreases
        if cumulative_tokens < prev_cumulative[bucket_key]:
            errors.append(
                f"Row {i}: Cumulative decreased from {prev_cumulative[bucket_key]} to {cumulative_tokens} for {bucket_key}"
            )

        prev_cumulative[bucket_key] = cumulative_tokens

        # Validation 3: Check bucket names exist in genesis.json (if provided)
        if valid_bucket_names and tier in valid_bucket_names:
            if bucket_name not in valid_bucket_names[tier]:
                errors.append(
                    f"Row {i}: Bucket name '{bucket_name}' not found in genesis.json tier '{tier}'. "
                    f"Valid names: {', '.join(valid_bucket_names[tier])}"
                )

        # Validation 4: Check allocation_mechanism is block_reward_emission
        if genesis_data and not validate_emission_mechanism(genesis_data, bucket_name, tier):
            errors.append(
                f"Row {i}: Bucket '{bucket_name}' in genesis.json should have "
                f"allocation_mechanism='block_reward_emission' for emission schedules"
            )

    # Validation 5: Check final cumulative is 100% for each bucket
    final_month = max(int(row['month']) for row in rows)
    final_rows = [row for row in rows if int(row['month']) == final_month]

    for row in final_rows:
        bucket_key = f"{row['tier']}::{row['bucket_name']}"
        final_pct = float(row['cumulative_pct_of_bucket'])

        # Allow some tolerance for rounding (99.9% - 100.1%)
        if final_pct < 99.9 or final_pct > 100.1:
            if final_pct > 0:  # Only warn if there were actual emissions
                errors.append(
                    f"Final cumulative for {bucket_key} is {final_pct}%, expected 100%"
                )

    return errors


def parse_csv(csv_path: Path) -> List[Dict]:
    """Parse CSV file and return list of row dictionaries."""
    rows = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip comment lines
            if row.get('month', '').startswith('#'):
                continue
            rows.append(row)

    return rows


def convert_to_json(rows: List[Dict], genesis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert CSV rows to JSON format."""

    # Group by month
    months_data = defaultdict(list)
    for row in rows:
        month = int(row['month'])
        months_data[month].append(row)

    # Calculate tier totals from CSV
    tier_bucket_totals = defaultdict(lambda: defaultdict(float))
    for row in rows:
        tier = row['tier']
        bucket = row['bucket_name']
        # Find the maximum cumulative for this bucket (= total allocation)
        cumulative = float(row['cumulative_tokens'])
        tier_bucket_totals[tier][bucket] = max(tier_bucket_totals[tier][bucket], cumulative)

    # Calculate tier totals
    tier_totals_calc = {}
    total_emission_tokens = 0
    for tier, buckets in tier_bucket_totals.items():
        tier_total = sum(buckets.values())
        tier_totals_calc[tier] = {
            'tokens': tier_total
        }
        total_emission_tokens += tier_total

    # Build monthly schedule
    monthly_schedule = []

    for month in sorted(months_data.keys()):
        month_rows = months_data[month]

        # Get the date from first row (should be same for all rows in month)
        date = month_rows[0]['date']

        # Build buckets array
        buckets = []
        tier_aggregates = defaultdict(lambda: {'emission_tokens': 0, 'cumulative_tokens': 0})

        for row in month_rows:
            tier = row['tier']
            bucket_name = row['bucket_name']
            emission_tokens = float(row['emission_tokens'])
            emission_pct = float(row['emission_pct_of_bucket'])
            cumulative_tokens = float(row['cumulative_tokens'])
            cumulative_pct = float(row['cumulative_pct_of_bucket'])
            notes = row.get('notes', '')

            buckets.append({
                'tier': tier,
                'bucket_name': bucket_name,
                'emission_tokens': int(emission_tokens),
                'emission_pct_of_bucket': round(emission_pct, 2),
                'cumulative_tokens': int(cumulative_tokens),
                'cumulative_pct_of_bucket': round(cumulative_pct, 2),
                'notes': notes
            })

            # Aggregate by tier
            tier_aggregates[tier]['emission_tokens'] += emission_tokens
            tier_aggregates[tier]['cumulative_tokens'] = max(
                tier_aggregates[tier]['cumulative_tokens'],
                cumulative_tokens
            )

        # Calculate tier percentages
        for tier in tier_aggregates:
            tier_total = tier_totals_calc.get(tier, {}).get('tokens', 1)
            tier_aggregates[tier]['cumulative_pct_of_tier'] = round(
                (tier_aggregates[tier]['cumulative_tokens'] / tier_total * 100) if tier_total > 0 else 0,
                2
            )

        # Calculate total
        total_emission = sum(tier_aggregates[t]['emission_tokens'] for t in tier_aggregates)
        total_cumulative = sum(tier_aggregates[t]['cumulative_tokens'] for t in tier_aggregates)
        total_cumulative_pct = round(
            (total_cumulative / total_emission_tokens * 100) if total_emission_tokens > 0 else 0,
            2
        )

        monthly_schedule.append({
            'month': month,
            'date': date,
            'buckets': buckets,
            'tier_aggregates': {
                tier: {
                    'emission_tokens': int(agg['emission_tokens']),
                    'cumulative_tokens': int(agg['cumulative_tokens']),
                    'cumulative_pct_of_tier': agg['cumulative_pct_of_tier']
                }
                for tier, agg in tier_aggregates.items()
            },
            'total': {
                'emission_tokens': int(total_emission),
                'cumulative_tokens': int(total_cumulative),
                'cumulative_pct_of_total': total_cumulative_pct
            }
        })

    # Generate milestone summary
    milestones = {}
    milestone_months = [0, 6, 12, 18, 24, 36, 48]

    for milestone_month in milestone_months:
        if milestone_month in months_data:
            month_entry = next(m for m in monthly_schedule if m['month'] == milestone_month)
            key = f"at_genesis" if milestone_month == 0 else f"at_month_{milestone_month}"
            milestones[key] = {
                'month': milestone_month,
                'date': month_entry['date'],
                'emitted_pct_of_total': month_entry['total']['cumulative_pct_of_total'],
                'emitted_tokens': month_entry['total']['cumulative_tokens']
            }

    # Find full emission milestone
    final_month_entry = monthly_schedule[-1]
    if final_month_entry['total']['cumulative_pct_of_total'] >= 99.9:
        milestones['at_completion'] = {
            'month': final_month_entry['month'],
            'date': final_month_entry['date'],
            'emitted_pct_of_total': 100.0,
            'emitted_tokens': final_month_entry['total']['cumulative_tokens']
        }

    # Build tier_totals for output
    tier_totals_output = {}
    for tier, data in tier_totals_calc.items():
        tier_totals_output[tier] = {
            'tokens': int(data['tokens']),
            'pct_of_total_emission': round((data['tokens'] / total_emission_tokens * 100) if total_emission_tokens > 0 else 0, 2)
        }

    # Extract project info from genesis or use defaults
    project_name = genesis_data.get('project', 'unknown')
    genesis_date = genesis_data.get('genesis_date', rows[0]['date'] if rows else 'unknown')

    return {
        'project': project_name,
        'genesis_date': genesis_date,
        'allocation_type': 'emission_based',
        'total_emission_tokens': int(total_emission_tokens),
        'tier_totals': tier_totals_output,
        'monthly_schedule': monthly_schedule,
        'milestone_summary': milestones
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python csv_to_emission_json.py <csv_file_path> [genesis_json_path]")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    genesis_path = Path(sys.argv[2]) if len(sys.argv) > 2 else csv_path.parent / 'genesis.json'

    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)

    # Load genesis.json if available
    genesis_data = load_genesis_json(genesis_path) if genesis_path.exists() else {}

    if genesis_data:
        print(f"✓ Loaded genesis.json: {genesis_path}")
    else:
        print(f"⚠ Genesis.json not found: {genesis_path} (validation will be limited)")

    # Parse CSV
    print(f"✓ Parsing CSV: {csv_path}")
    rows = parse_csv(csv_path)

    if not rows:
        print("Error: CSV file is empty or invalid")
        sys.exit(1)

    print(f"✓ Parsed {len(rows)} rows")

    # Validate
    print("✓ Validating data...")
    errors = validate_csv_data(rows, genesis_data)

    if errors:
        print(f"\n✗ Validation failed with {len(errors)} error(s):\n")
        for error in errors:
            print(f"  • {error}")
        print("\nFix the errors in your CSV and re-run.")
        sys.exit(1)

    print("✓ All validations passed")

    # Convert to JSON
    print("✓ Converting to JSON...")
    json_data = convert_to_json(rows, genesis_data)

    # Write output
    output_path = csv_path.with_suffix('.json')
    with open(output_path, 'w') as f:
        json.dump(json_data, f, indent=2)

    print(f"✓ Generated: {output_path}")

    # Print summary
    total_tokens = json_data['total_emission_tokens']
    final_month = json_data['monthly_schedule'][-1]
    print(f"\nSummary:")
    print(f"  Project: {json_data['project']}")
    print(f"  Total emissions: {total_tokens:,} tokens")
    print(f"  Emission period: {final_month['month']} months")
    print(f"  Final emission: {final_month['date']}")


if __name__ == '__main__':
    main()
