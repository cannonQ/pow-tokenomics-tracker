#!/usr/bin/env python3
"""
Generate comparison matrix across all projects with vesting schedules.

Usage:
    python generate_comparison_matrix.py

Reads all allocations/*/vesting-schedule.json files and generates:
    allocations/comparison-matrix.json

The comparison matrix extracts key milestones (TGE, 6mo, 12mo, 18mo, 24mo, 36mo, 48mo)
for easy cross-project comparison.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def load_vesting_schedule(project_path: Path) -> Dict[str, Any]:
    """Load a project's vesting schedule JSON."""
    vesting_file = project_path / 'vesting-schedule.json'

    if not vesting_file.exists():
        return None

    with open(vesting_file, 'r') as f:
        return json.load(f)


def load_emission_schedule(project_path: Path) -> Dict[str, Any]:
    """Load a project's emission schedule JSON."""
    emission_file = project_path / 'emission-schedule.json'

    if not emission_file.exists():
        return None

    with open(emission_file, 'r') as f:
        return json.load(f)


def extract_milestones(allocation_data: Dict[str, Any], milestone_months: List[int], is_emission: bool = False) -> Dict[str, Any]:
    """Extract milestone data at specific months."""
    milestones = {}
    monthly_schedule = allocation_data.get('monthly_schedule', [])

    # Create lookup by month
    month_lookup = {entry['month']: entry for entry in monthly_schedule}

    # Determine which keys to use based on type
    if is_emission:
        pct_key = 'cumulative_pct_of_total'
    else:
        pct_key = 'cumulative_pct_of_genesis'

    for milestone_month in milestone_months:
        if milestone_month in month_lookup:
            entry = month_lookup[milestone_month]
            key = f"month_{milestone_month}" if milestone_month > 0 else "tge"
            milestones[key] = {
                'liquid_pct': entry['total'].get(pct_key, entry['total'].get('cumulative_pct_of_genesis', 0)),
                'liquid_tokens': entry['total']['cumulative_tokens'],
                'date': entry['date']
            }

            # Add tier breakdown
            tier_breakdown = {}
            for tier, agg in entry['tier_aggregates'].items():
                tier_breakdown[tier] = {
                    'pct': agg['cumulative_pct_of_tier'],
                    'tokens': agg['cumulative_tokens']
                }

            milestones[key]['tier_breakdown'] = tier_breakdown

    return milestones


def calculate_unlock_rate(allocation_data: Dict[str, Any], start_month: int, end_month: int, is_emission: bool = False) -> float:
    """Calculate average monthly unlock rate between two months."""
    monthly_schedule = allocation_data.get('monthly_schedule', [])
    month_lookup = {entry['month']: entry for entry in monthly_schedule}

    if start_month not in month_lookup or end_month not in month_lookup:
        return 0.0

    # Determine which key to use
    pct_key = 'cumulative_pct_of_total' if is_emission else 'cumulative_pct_of_genesis'

    start_pct = month_lookup[start_month]['total'].get(pct_key, month_lookup[start_month]['total'].get('cumulative_pct_of_genesis', 0))
    end_pct = month_lookup[end_month]['total'].get(pct_key, month_lookup[end_month]['total'].get('cumulative_pct_of_genesis', 0))

    months_diff = end_month - start_month
    if months_diff == 0:
        return 0.0

    return round((end_pct - start_pct) / months_diff, 2)


def find_full_unlock_month(allocation_data: Dict[str, Any], is_emission: bool = False) -> Dict[str, Any]:
    """Find when vesting/emission is fully complete (100%)."""
    monthly_schedule = allocation_data.get('monthly_schedule', [])

    # Determine which key to use
    pct_key = 'cumulative_pct_of_total' if is_emission else 'cumulative_pct_of_genesis'

    for entry in reversed(monthly_schedule):
        pct = entry['total'].get(pct_key, entry['total'].get('cumulative_pct_of_genesis', 0))
        if pct >= 99.9:
            return {
                'month': entry['month'],
                'date': entry['date']
            }

    # If not fully complete, return last entry
    if monthly_schedule:
        last_entry = monthly_schedule[-1]
        pct = last_entry['total'].get(pct_key, last_entry['total'].get('cumulative_pct_of_genesis', 0))
        return {
            'month': last_entry['month'],
            'date': last_entry['date'],
            'note': f"Not fully complete - only {pct}% released"
        }

    return None


def load_genesis_summary(project_path: Path) -> Dict[str, Any]:
    """Load summary info from genesis.json."""
    genesis_file = project_path / 'genesis.json'

    if not genesis_file.exists():
        return {}

    with open(genesis_file, 'r') as f:
        data = json.load(f)

    return {
        'has_premine': data.get('has_premine', False),
        'total_genesis_allocation_pct': data.get('total_genesis_allocation_pct', 0),
        'genesis_date': data.get('genesis_date', ''),
        'has_dev_tax': data.get('has_dev_tax', False)
    }


def generate_comparison_matrix(allocations_dir: Path) -> Dict[str, Any]:
    """Generate comparison matrix from all projects."""
    projects = []

    # Find all project directories
    for project_dir in sorted(allocations_dir.iterdir()):
        if not project_dir.is_dir():
            continue

        project_name = project_dir.name

        # Load genesis summary
        genesis_summary = load_genesis_summary(project_dir)

        # Load both vesting and emission schedules
        vesting_data = load_vesting_schedule(project_dir)
        emission_data = load_emission_schedule(project_dir)

        # Check if project has allocation data
        if not vesting_data and not emission_data:
            # No allocation schedule - check if it's because no premine
            if not genesis_summary.get('has_premine', False):
                projects.append({
                    'name': project_name,
                    'has_premine': False,
                    'allocation_type': 'fair_launch_only',
                    'note': 'No genesis allocation - 100% mining/staking distribution'
                })
            continue

        # Determine which schedule to use for milestone extraction
        # Prefer vesting if both exist, otherwise use emission
        primary_data = vesting_data if vesting_data else emission_data
        is_emission = primary_data == emission_data

        # Extract data
        milestone_months = [0, 6, 12, 18, 24, 36, 48]
        milestones = extract_milestones(primary_data, milestone_months, is_emission=is_emission)

        # Calculate metrics
        unlock_rate_year_1 = calculate_unlock_rate(primary_data, 0, 12, is_emission=is_emission)
        unlock_rate_year_2 = calculate_unlock_rate(primary_data, 12, 24, is_emission=is_emission)

        full_unlock = find_full_unlock_month(primary_data, is_emission=is_emission)

        # Determine allocation type
        allocation_type = 'time_locked_vesting'
        if emission_data and not vesting_data:
            allocation_type = 'emission_based'
        elif vesting_data and emission_data:
            allocation_type = 'hybrid'

        project_entry = {
            'name': project_name,
            'has_premine': True,
            'allocation_type': allocation_type,
            'genesis_date': primary_data.get('genesis_date', ''),
            'total_genesis_allocation_tokens': primary_data.get('total_genesis_allocation_tokens', primary_data.get('total_emission_tokens', 0)),
            'total_genesis_allocation_pct': genesis_summary.get('total_genesis_allocation_pct', 0),
            'tier_composition': {
                tier: totals
                for tier, totals in primary_data.get('tier_totals', {}).items()
            },
            'milestones': milestones,
            'unlock_metrics': {
                'avg_monthly_unlock_rate_year_1_pct': unlock_rate_year_1,
                'avg_monthly_unlock_rate_year_2_pct': unlock_rate_year_2,
                'full_unlock_month': full_unlock['month'] if full_unlock else None,
                'full_unlock_date': full_unlock['date'] if full_unlock else None
            }
        }

        if full_unlock and 'note' in full_unlock:
            project_entry['unlock_metrics']['note'] = full_unlock['note']

        projects.append(project_entry)

    return {
        'generated_date': datetime.now().strftime('%Y-%m-%d'),
        'description': 'Cross-project comparison of genesis allocations and vesting schedules',
        'milestone_columns': ['tge', 'month_6', 'month_12', 'month_18', 'month_24', 'month_36', 'month_48'],
        'projects': projects
    }


def main():
    # Find allocations directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    allocations_dir = repo_root / 'allocations'

    if not allocations_dir.exists():
        print(f"Error: Allocations directory not found: {allocations_dir}")
        sys.exit(1)

    print(f"✓ Scanning projects in: {allocations_dir}")

    # Generate comparison matrix
    comparison_data = generate_comparison_matrix(allocations_dir)

    project_count = len(comparison_data['projects'])
    premine_count = sum(1 for p in comparison_data['projects'] if p.get('has_premine', False))

    print(f"✓ Found {project_count} projects ({premine_count} with premines)")

    # Write output
    output_path = allocations_dir / 'comparison-matrix.json'
    with open(output_path, 'w') as f:
        json.dump(comparison_data, f, indent=2)

    print(f"✓ Generated: {output_path}")

    # Print summary table
    print(f"\nSummary:")
    print(f"  {'Project':<20} {'Genesis %':<12} {'TGE %':<10} {'12mo %':<10} {'24mo %':<10} {'Full Unlock':<15}")
    print(f"  {'-'*20} {'-'*12} {'-'*10} {'-'*10} {'-'*10} {'-'*15}")

    for project in comparison_data['projects']:
        if not project.get('has_premine', False):
            print(f"  {project['name']:<20} {'0%':<12} {'-':<10} {'-':<10} {'-':<10} {'N/A (mining)':<15}")
            continue

        genesis_pct = project.get('total_genesis_allocation_pct', 0)
        tge_pct = project.get('milestones', {}).get('tge', {}).get('liquid_pct', 0)
        mo12_pct = project.get('milestones', {}).get('month_12', {}).get('liquid_pct', 0)
        mo24_pct = project.get('milestones', {}).get('month_24', {}).get('liquid_pct', 0)
        full_unlock_month = project.get('unlock_metrics', {}).get('full_unlock_month', '?')

        print(f"  {project['name']:<20} {genesis_pct:<11.1f}% {tge_pct:<9.1f}% {mo12_pct:<9.1f}% {mo24_pct:<9.1f}% {f'{full_unlock_month} months':<15}")


if __name__ == '__main__':
    main()
