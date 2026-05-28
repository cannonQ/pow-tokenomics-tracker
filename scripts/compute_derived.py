#!/usr/bin/env python3
"""
PoW Tokenomics Tracker - Derived Field Calculator

Computes the fields that are derived from other fields, so acquisition agents
never do arithmetic by hand. These are the same formulas validate_submission.py
checks, so running this BEFORE the validator means the math gate always passes
when the underlying source data is right.

Derived fields:
  supply.pct_mined            = (current_supply / max_supply) * 100
  supply.emission_remaining   = max_supply - current_supply
  emission.daily_emission     = (86400 / block_time_seconds) * current_block_reward
  emission.annual_inflation_pct = (daily_emission * 365 / current_supply) * 100
  market_data.fdmc            = current_price_usd * max_supply
  market_data.circulating_mcap = current_price_usd * current_supply
  market_data.token_velocity  = daily_volume / circulating_mcap

Usage:
  python scripts/compute_derived.py <project>            # write fields back into the file
  python scripts/compute_derived.py <project> --check    # report diffs, write nothing (exit 1 if drift)
"""

import json
import sys
from pathlib import Path


def _round(value, ndigits):
    """Round, but keep clean integers as ints for whole-token fields."""
    if value is None:
        return None
    if ndigits == 0:
        return int(round(value))
    return round(value, ndigits)


def compute(project_data):
    """Return a dict of {dotted.path: computed_value} for every derivable field
    whose inputs are present. Missing inputs (e.g. null max_supply) are skipped."""
    supply = project_data.get("supply", {}) or {}
    emission = project_data.get("emission", {}) or {}
    market = project_data.get("market_data", {}) or {}

    max_supply = supply.get("max_supply")
    current_supply = supply.get("current_supply")
    block_reward = emission.get("current_block_reward")
    block_time = emission.get("block_time_seconds")
    price = market.get("current_price_usd")
    daily_volume = market.get("daily_volume")

    out = {}

    # Supply
    if max_supply not in (None, 0) and current_supply is not None:
        out["supply.pct_mined"] = _round((current_supply / max_supply) * 100, 2)
        out["supply.emission_remaining"] = _round(max_supply - current_supply, 0)

    # Emission
    daily_emission = None
    if block_time not in (None, 0) and block_reward is not None:
        daily_emission = (86400 / block_time) * block_reward
        out["emission.daily_emission"] = _round(daily_emission, 2)
    if daily_emission is not None and current_supply not in (None, 0):
        out["emission.annual_inflation_pct"] = _round(
            (daily_emission * 365 / current_supply) * 100, 2
        )

    # Market data
    circulating_mcap = None
    if price is not None and max_supply is not None:
        out["market_data.fdmc"] = _round(price * max_supply, 0)
    if price is not None and current_supply is not None:
        circulating_mcap = price * current_supply
        out["market_data.circulating_mcap"] = _round(circulating_mcap, 0)
    if daily_volume is not None and circulating_mcap not in (None, 0):
        out["market_data.token_velocity"] = _round(daily_volume / circulating_mcap, 4)

    return out


def apply_to(project_data, computed):
    """Write computed values into the nested dict in place."""
    for dotted, value in computed.items():
        section, field = dotted.split(".", 1)
        project_data.setdefault(section, {})[field] = value


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_only = "--check" in sys.argv

    if not args:
        print("Usage: python scripts/compute_derived.py <project> [--check]")
        sys.exit(1)

    project = args[0]
    path = Path(f"data/projects/{project}.json")
    if not path.exists():
        print(f"Project file not found: {path}")
        sys.exit(1)

    with open(path) as f:
        data = json.load(f)

    computed = compute(data)

    if check_only:
        drift = []
        for dotted, value in computed.items():
            section, field = dotted.split(".", 1)
            existing = (data.get(section) or {}).get(field)
            if existing != value:
                drift.append((dotted, existing, value))
        if drift:
            print(f"DRIFT in {project}: {len(drift)} derived field(s) differ\n")
            for dotted, existing, value in drift:
                print(f"  {dotted}: file={existing}  computed={value}")
            sys.exit(1)
        print(f"OK: all {len(computed)} derived fields in {project} match.")
        sys.exit(0)

    apply_to(data, computed)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"Computed {len(computed)} derived field(s) for {project}:")
    for dotted, value in computed.items():
        print(f"  {dotted} = {value}")


if __name__ == "__main__":
    main()
