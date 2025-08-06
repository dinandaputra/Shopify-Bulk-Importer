#!/usr/bin/env python3
"""
Standardize Keyboard Backlight Values Script

Updates all laptop JSON files to use standardized keyboard backlight values:
- "Non-backlit" - For no backlight
- "RGB Backlight" - For RGB backlight (keep as is)
- "Backlit" - For any colored backlight (White, Blue, Green, Red, etc.)

Usage:
    python scripts/utilities/standardize_keyboard_backlight.py
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class KeyboardBacklightStandardizer:
    """Standardizes keyboard backlight values across all laptop JSON files."""
    
    # Mapping from current values to standardized values
    STANDARDIZATION_MAP = {
        "RGB Backlight": "RGB Backlight",  # Keep as is
        "White Backlight": "Backlit",
        "Blue Backlight": "Backlit", 
        "Green Backlight": "Backlit",
        "Red Backlight": "Backlit",
        "Yes": "Backlit",  # Generic backlight
        "No": "Non-backlit",  # No backlight
        # Add more mappings as needed
    }
    
    def __init__(self):
        self.laptop_dir = "data/products/laptops/"
        self.changes_made = []
        self.files_processed = 0
        self.values_updated = 0
    
    def standardize_all_files(self):
        """Process all laptop JSON files."""
        print("🔧 Starting keyboard backlight standardization...")
        
        # Get all JSON files in laptops directory
        json_files = [f for f in os.listdir(self.laptop_dir) if f.endswith('.json')]
        
        print(f"📁 Found {len(json_files)} laptop files to process")
        
        for filename in json_files:
            if filename == 'brands_index.json':
                continue  # Skip index file
                
            file_path = os.path.join(self.laptop_dir, filename)
            self._process_file(file_path, filename)
        
        self._print_summary()
    
    def _process_file(self, file_path: str, filename: str):
        """Process a single laptop JSON file."""
        try:
            # Read original file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            original_data = json.dumps(data)
            changes_in_file = 0
            
            # Process models
            models = data.get('models', {})
            for model_name, model_info in models.items():
                configurations = model_info.get('configurations', [])
                
                for i, config in enumerate(configurations):
                    original_value = config.get('keyboard_backlight', '')
                    
                    if original_value in self.STANDARDIZATION_MAP:
                        new_value = self.STANDARDIZATION_MAP[original_value]
                        
                        if original_value != new_value:
                            config['keyboard_backlight'] = new_value
                            changes_in_file += 1
                            self.values_updated += 1
                            
                            self.changes_made.append({
                                'file': filename,
                                'model': model_name,
                                'config_index': i,
                                'original': original_value,
                                'updated': new_value
                            })
                    elif original_value:  # Non-empty value not in map
                        print(f"  ⚠️  Warning: Unknown keyboard_backlight value '{original_value}' in {filename}:{model_name}")
            
            # Save file if changes were made
            if changes_in_file > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"  ✅ {filename}: {changes_in_file} values updated")
            else:
                print(f"  📋 {filename}: No changes needed")
            
            self.files_processed += 1
            
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")
    
    def _print_summary(self):
        """Print comprehensive summary of changes."""
        print("\n" + "="*60)
        print("📊 STANDARDIZATION SUMMARY")
        print("="*60)
        
        print(f"📁 Files Processed: {self.files_processed}")
        print(f"🔧 Values Updated: {self.values_updated}")
        
        if self.changes_made:
            print(f"\n📋 DETAILED CHANGES ({len(self.changes_made)} total):")
            
            # Group changes by transformation type
            transformations = {}
            for change in self.changes_made:
                key = f"{change['original']} → {change['updated']}"
                if key not in transformations:
                    transformations[key] = []
                transformations[key].append(change)
            
            for transformation, changes in transformations.items():
                print(f"\n  🔄 {transformation} ({len(changes)} instances):")
                for change in changes[:5]:  # Show first 5 examples
                    print(f"    - {change['file']}:{change['model']}")
                if len(changes) > 5:
                    print(f"    - ... and {len(changes) - 5} more")
        
        print(f"\n✅ Standardization complete!")
        print(f"📋 All keyboard backlight values now use: Non-backlit, RGB Backlight, Backlit")
    
    def validate_standardization(self):
        """Validate that all values are now standardized."""
        print("\n🔍 Validating standardization...")
        
        valid_values = {"Non-backlit", "RGB Backlight", "Backlit"}
        issues_found = []
        
        json_files = [f for f in os.listdir(self.laptop_dir) if f.endswith('.json')]
        
        for filename in json_files:
            if filename == 'brands_index.json':
                continue
                
            file_path = os.path.join(self.laptop_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                models = data.get('models', {})
                for model_name, model_info in models.items():
                    configurations = model_info.get('configurations', [])
                    
                    for i, config in enumerate(configurations):
                        value = config.get('keyboard_backlight', '')
                        
                        if value and value not in valid_values:
                            issues_found.append({
                                'file': filename,
                                'model': model_name,
                                'config_index': i,
                                'invalid_value': value
                            })
            
            except Exception as e:
                print(f"  ❌ Error validating {filename}: {e}")
        
        if issues_found:
            print(f"  ❌ Found {len(issues_found)} invalid values:")
            for issue in issues_found:
                print(f"    - {issue['file']}:{issue['model']} = '{issue['invalid_value']}'")
            return False
        else:
            print("  ✅ All keyboard backlight values are now standardized!")
            return True


def main():
    """Main execution function."""
    print("🚀 Keyboard Backlight Standardization")
    print("=" * 50)
    
    try:
        standardizer = KeyboardBacklightStandardizer()
        
        # Step 1: Standardize all files
        standardizer.standardize_all_files()
        
        # Step 2: Validate results
        standardizer.validate_standardization()
        
        print("\n" + "=" * 50)
        print("✅ Keyboard Backlight Standardization Complete!")
        print("📋 Ready for updated component analysis")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Standardization failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())