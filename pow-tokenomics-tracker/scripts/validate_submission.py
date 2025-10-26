#!/usr/bin/env python3
"""
PoW Tokenomics Tracker - Submission Validator
Validates project and genesis JSON files before submission
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class ValidationError(Exception):
    """Custom exception for validation failures"""
    pass


class Validator:
    def __init__(self, project_name):
        self.project_name = project_name
        self.errors = []
        self.warnings = []
        self.project_data = None
        self.genesis_data = None
        
    def validate_all(self):
        """Run all validation checks"""
        print(f"🔍 Validating {self.project_name}...\n")
        
        try:
            # Load and validate project file
            self.load_project_file()
            self.validate_project_structure()
            self.validate_supply_math()
            self.validate_emission_math()
            self.validate_dates()
            self.validate_urls()
            
            # Load and validate genesis file if needed
            if self.project_data.get('has_premine'):
                self.load_genesis_file()
                self.validate_genesis_structure()
                self.validate_allocation_math()
                self.validate_vesting_logic()
            
            # Check for comment fields
            self.check_for_comments()
            
            # Print results
            self.print_results()
            
            return len(self.errors) == 0
            
        except Exception as e:
            print(f"❌ Fatal error: {str(e)}\n")
            return False
    
    def load_project_file(self):
        """Load and parse project JSON file"""
        project_path = Path(f"data/projects/{self.project_name}.json")
        
        if not project_path.exists():
            raise ValidationError(
                f"Project file not found: {project_path}\n"
                f"Expected location: data/projects/{self.project_name}.json"
            )
        
        try:
            with open(project_path, 'r') as f:
                self.project_data = json.load(f)
            print(f"✅ Loaded project file: {project_path}")
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in project file: {str(e)}")
    
    def load_genesis_file(self):
        """Load and parse genesis JSON file"""
        genesis_path = Path(f"allocations/{self.project_name}/genesis.json")
        
        if not genesis_path.exists():
            self.errors.append(
                f"Genesis file missing: {genesis_path}\n"
                f"  → Project has has_premine=true but no genesis file found\n"
                f"  → Create: allocations/{self.project_name}/genesis.json"
            )
            return
        
        try:
            with open(genesis_path, 'r') as f:
                self.genesis_data = json.load(f)
            print(f"✅ Loaded genesis file: {genesis_path}")
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in genesis file: {str(e)}")
    
    def validate_project_structure(self):
        """Check required fields in project file"""
        required_fields = [
            'project', 'ticker', 'consensus', 'launch_date',
            'has_premine', 'supply', 'emission', 'data_sources'
        ]
        
        for field in required_fields:
            if field not in self.project_data:
                self.errors.append(f"Missing required field: {field}")
        
        # Check nested required fields
        if 'supply' in self.project_data:
            supply_required = ['max_supply', 'current_supply', 'pct_mined']
            for field in supply_required:
                if field not in self.project_data['supply']:
                    self.errors.append(f"Missing required field: supply.{field}")
        
        if 'emission' in self.project_data:
            emission_required = ['current_block_reward', 'block_time_seconds', 'daily_emission']
            for field in emission_required:
                if field not in self.project_data['emission']:
                    self.errors.append(f"Missing required field: emission.{field}")
        
        # Check data sources
        if 'data_sources' in self.project_data:
            sources = self.project_data['data_sources']
            if not sources.get('official_docs'):
                self.warnings.append("No official_docs provided in data_sources")
            if not sources.get('block_explorer'):
                self.warnings.append("No block_explorer provided in data_sources")
    
    def validate_supply_math(self):
        """Validate supply calculations"""
        supply = self.project_data.get('supply', {})
        
        max_supply = supply.get('max_supply')
        current_supply = supply.get('current_supply')
        pct_mined = supply.get('pct_mined')
        emission_remaining = supply.get('emission_remaining')
        
        # Skip if max_supply is null (unlimited)
        if max_supply is None:
            if pct_mined is not None:
                self.warnings.append(
                    "pct_mined should be null if max_supply is null (unlimited supply)"
                )
            return
        
        # Check pct_mined calculation
        if current_supply and max_supply and pct_mined:
            calculated_pct = (current_supply / max_supply) * 100
            if abs(calculated_pct - pct_mined) > 0.1:  # Allow 0.1% tolerance
                self.errors.append(
                    f"pct_mined incorrect: {pct_mined}% (should be {calculated_pct:.2f}%)\n"
                    f"  → Formula: (current_supply / max_supply) * 100"
                )
        
        # Check emission_remaining calculation
        if max_supply and current_supply and emission_remaining:
            calculated_remaining = max_supply - current_supply
            if abs(calculated_remaining - emission_remaining) > 1:  # Allow 1 token tolerance
                self.errors.append(
                    f"emission_remaining incorrect: {emission_remaining} "
                    f"(should be {calculated_remaining:.0f})\n"
                    f"  → Formula: max_supply - current_supply"
                )
    
    def validate_emission_math(self):
        """Validate emission calculations"""
        emission = self.project_data.get('emission', {})
        supply = self.project_data.get('supply', {})
        
        block_reward = emission.get('current_block_reward')
        block_time = emission.get('block_time_seconds')
        daily_emission = emission.get('daily_emission')
        annual_inflation = emission.get('annual_inflation_pct')
        current_supply = supply.get('current_supply')
        
        # Check daily_emission calculation
        if block_reward and block_time and daily_emission:
            calculated_daily = (86400 / block_time) * block_reward
            if abs(calculated_daily - daily_emission) > 1:  # Allow 1 token tolerance
                self.errors.append(
                    f"daily_emission incorrect: {daily_emission} "
                    f"(should be ~{calculated_daily:.0f})\n"
                    f"  → Formula: (86400 / block_time_seconds) * current_block_reward"
                )
        
        # Check annual_inflation_pct calculation
        if daily_emission and current_supply and annual_inflation:
            calculated_inflation = (daily_emission * 365 / current_supply) * 100
            if abs(calculated_inflation - annual_inflation) > 0.1:  # Allow 0.1% tolerance
                self.errors.append(
                    f"annual_inflation_pct incorrect: {annual_inflation}% "
                    f"(should be ~{calculated_inflation:.2f}%)\n"
                    f"  → Formula: (daily_emission * 365 / current_supply) * 100"
                )
    
    def validate_dates(self):
        """Validate date formats"""
        date_fields = [
            ('launch_date', self.project_data),
            ('last_updated', self.project_data),
        ]
        
        if self.genesis_data:
            date_fields.append(('genesis_date', self.genesis_data))
        
        for field_name, data in date_fields:
            if field_name in data:
                date_str = data[field_name]
                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    self.errors.append(
                        f"Invalid date format for {field_name}: {date_str}\n"
                        f"  → Must be YYYY-MM-DD format (e.g., 2023-01-15)"
                    )
        
        # Warn if data is old
        if 'last_updated' in self.project_data:
            last_updated = datetime.strptime(self.project_data['last_updated'], '%Y-%m-%d')
            days_old = (datetime.now() - last_updated).days
            if days_old > 30:
                self.warnings.append(
                    f"Data is {days_old} days old (last_updated: {self.project_data['last_updated']})\n"
                    f"  → Consider refreshing with current data"
                )
    
    def validate_urls(self):
        """Check URL formats in data_sources"""
        if 'data_sources' not in self.project_data:
            return
        
        sources = self.project_data['data_sources']
        url_fields = ['official_docs', 'block_explorer', 'market_data', 'mining_data']
        
        for field in url_fields:
            if field in sources:
                urls = sources[field]
                if not isinstance(urls, list):
                    self.errors.append(f"data_sources.{field} must be a list")
                    continue
                
                for url in urls:
                    if not url.startswith(('http://', 'https://')):
                        self.errors.append(
                            f"Invalid URL in data_sources.{field}: {url}\n"
                            f"  → URLs must start with http:// or https://"
                        )
    
    def validate_genesis_structure(self):
        """Check required fields in genesis file"""
        if not self.genesis_data:
            return
        
        required_fields = [
            'project', 'has_premine', 'genesis_date',
            'total_genesis_allocation_pct', 'allocation_tiers'
        ]
        
        for field in required_fields:
            if field not in self.genesis_data:
                self.errors.append(f"Genesis file missing required field: {field}")
        
        # Check project name matches
        if self.genesis_data.get('project') != self.project_name:
            self.errors.append(
                f"Project name mismatch:\n"
                f"  → Main file: {self.project_name}\n"
                f"  → Genesis file: {self.genesis_data.get('project')}"
            )
    
    def validate_allocation_math(self):
        """Validate allocation percentages sum correctly"""
        if not self.genesis_data or 'allocation_tiers' not in self.genesis_data:
            return
        
        tiers = self.genesis_data['allocation_tiers']
        total_pct = 0
        
        # Sum all tier totals
        tier_names = [
            'tier_1_profit_seeking',
            'tier_2_entity_controlled',
            'tier_3_community',
            'tier_4_liquidity'
        ]
        
        for tier_name in tier_names:
            if tier_name in tiers and 'total_pct' in tiers[tier_name]:
                tier_pct = tiers[tier_name]['total_pct']
                total_pct += tier_pct
                
                # Validate tier total matches bucket sum
                if 'buckets' in tiers[tier_name]:
                    bucket_sum = sum(b['pct'] for b in tiers[tier_name]['buckets'] if 'pct' in b)
                    if abs(bucket_sum - tier_pct) > 0.1:
                        self.errors.append(
                            f"Tier {tier_name} total mismatch:\n"
                            f"  → Declared total: {tier_pct}%\n"
                            f"  → Bucket sum: {bucket_sum}%"
                        )
        
        # Check total allocation matches
        declared_total = self.genesis_data.get('total_genesis_allocation_pct', 0)
        if abs(total_pct - declared_total) > 0.1:
            self.errors.append(
                f"Total allocation mismatch:\n"
                f"  → Declared: {declared_total}%\n"
                f"  → Tier sum: {total_pct}%"
            )
        
        # Check allocation + mining = 100%
        mining_pct = self.genesis_data.get('available_for_mining_genesis_pct', 0)
        total_with_mining = declared_total + mining_pct
        
        if abs(total_with_mining - 100) > 0.1:
            self.errors.append(
                f"Total allocation + mining must equal 100%:\n"
                f"  → Genesis allocation: {declared_total}%\n"
                f"  → Mining allocation: {mining_pct}%\n"
                f"  → Total: {total_with_mining}% (should be 100%)"
            )
    
    def validate_vesting_logic(self):
        """Check vesting schedule logic"""
        if not self.genesis_data:
            return
        
        # Check each tier's buckets
        tiers = self.genesis_data.get('allocation_tiers', {})
        for tier_name, tier_data in tiers.items():
            if 'buckets' not in tier_data:
                continue
            
            for bucket in tier_data['buckets']:
                # TGE unlock shouldn't exceed 100%
                tge_unlock = bucket.get('tge_unlock_pct', 0)
                if tge_unlock > 100:
                    self.errors.append(
                        f"Bucket '{bucket.get('name')}' has tge_unlock_pct > 100%: {tge_unlock}%"
                    )
                
                # If cliff exists, should be < vesting period
                cliff = bucket.get('cliff_months', 0)
                vesting = bucket.get('vesting_months')
                if vesting and cliff > vesting:
                    self.warnings.append(
                        f"Bucket '{bucket.get('name')}': cliff ({cliff}mo) exceeds vesting ({vesting}mo)"
                    )
    
    def check_for_comments(self):
        """Check if template comment fields are still present"""
        def has_comment_keys(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key.startswith('_comment'):
                        self.errors.append(
                            f"Template comment field still present: {path}.{key}\n"
                            f"  → Delete all lines starting with '_comment' before submitting"
                        )
                    has_comment_keys(value, f"{path}.{key}" if path else key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    has_comment_keys(item, f"{path}[{i}]")
        
        if self.project_data:
            has_comment_keys(self.project_data, "project")
        if self.genesis_data:
            has_comment_keys(self.genesis_data, "genesis")
    
    def print_results(self):
        """Print validation results"""
        print("\n" + "="*60)
        
        if self.errors:
            print(f"❌ VALIDATION FAILED - {len(self.errors)} error(s) found:\n")
            for i, error in enumerate(self.errors, 1):
                print(f"{i}. {error}\n")
        else:
            print("✅ VALIDATION PASSED - No errors found!\n")
        
        if self.warnings:
            print(f"⚠️  {len(self.warnings)} warning(s):\n")
            for i, warning in enumerate(self.warnings, 1):
                print(f"{i}. {warning}\n")
        
        print("="*60)
        
        if not self.errors:
            print("\n🎉 Your submission looks good!")
            print("   Next step: Commit and create a Pull Request\n")
        else:
            print("\n❌ Please fix the errors above before submitting.")
            print("   Need help? Check CONTRIBUTING.md or open an issue.\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_submission.py <project-name>")
        print("\nExample:")
        print("  python validate_submission.py bitcoin")
        print("  python validate_submission.py example-coin")
        sys.exit(1)
    
    project_name = sys.argv[1]
    validator = Validator(project_name)
    
    success = validator.validate_all()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
