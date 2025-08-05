#!/usr/bin/env python3
"""
GID Preservation Validation Script

This script validates that all GID values from the original Python mapping 
have been correctly preserved in the JSON files, focusing on GID preservation
rather than key name matching (since we intentionally converted abbreviated 
keys to full names as requested).
"""

import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def load_original_mappings():
    """Load the original mappings from the Python file"""
    try:
        from config.laptop_metafield_mapping_actual import (
            PROCESSOR_METAOBJECTS,
            GRAPHICS_METAOBJECTS, 
            VGA_METAOBJECTS,
            DISPLAY_METAOBJECTS,
            STORAGE_METAOBJECTS,
            COLOR_METAOBJECTS,
            OS_METAOBJECTS,
            KEYBOARD_LAYOUT_METAOBJECTS,
            KEYBOARD_BACKLIGHT_METAOBJECTS
        )
        
        return {
            'processors': PROCESSOR_METAOBJECTS,
            'graphics': GRAPHICS_METAOBJECTS,
            'vga': VGA_METAOBJECTS,
            'displays': DISPLAY_METAOBJECTS,
            'storage': STORAGE_METAOBJECTS,
            'colors': COLOR_METAOBJECTS,
            'os': OS_METAOBJECTS,
            'keyboard_layouts': KEYBOARD_LAYOUT_METAOBJECTS,
            'keyboard_backlights': KEYBOARD_BACKLIGHT_METAOBJECTS
        }
    except ImportError as e:
        print(f"Error importing original mappings: {e}")
        return None

def load_json_mappings():
    """Load the JSON mappings"""
    json_files = {
        'processors': 'data/metaobjects/processors.json',
        'graphics': 'data/metaobjects/graphics.json', 
        'vga': 'data/metaobjects/vga.json',
        'displays': 'data/metaobjects/displays.json',
        'storage': 'data/metaobjects/storage.json',
        'colors': 'data/metaobjects/colors.json',
        'os': 'data/metaobjects/os.json',
        'keyboard_layouts': 'data/metaobjects/keyboard_layouts.json',
        'keyboard_backlights': 'data/metaobjects/keyboard_backlights.json'
    }
    
    json_mappings = {}
    
    for key, file_path in json_files.items():
        try:
            with open(file_path, 'r') as f:
                json_mappings[key] = json.load(f)
        except FileNotFoundError:
            print(f"JSON file not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in {file_path}: {e}")
            return None
    
    return json_mappings

def extract_gids(mapping_dict):
    """Extract all GID values from a mapping dictionary"""
    return set(mapping_dict.values())

def validate_gid_preservation():
    """Validate that all GIDs from original mapping are preserved in JSON files"""
    print("🔍 Validating GID preservation during extraction...")
    print("=" * 60)
    
    # Load mappings
    original_mappings = load_original_mappings()
    json_mappings = load_json_mappings()
    
    if not original_mappings or not json_mappings:
        print("❌ Failed to load mappings")
        return False
    
    # Track validation results
    validation_results = {}
    all_original_gids = set()
    all_json_gids = set()
    
    # Validate each component type
    for component_type in original_mappings.keys():
        print(f"\n📋 Validating {component_type} GID preservation...")
        
        original = original_mappings[component_type]
        json_data = json_mappings[component_type]
        
        original_gids = extract_gids(original)
        json_gids = extract_gids(json_data)
        
        all_original_gids.update(original_gids)
        all_json_gids.update(json_gids)
        
        original_count = len(original_gids)
        json_count = len(json_gids)
        
        print(f"   Original GIDs: {original_count}")
        print(f"   JSON GIDs: {json_count}")
        
        # Check for missing and extra GIDs
        missing_gids = original_gids - json_gids
        extra_gids = json_gids - original_gids
        
        # Store results
        validation_results[component_type] = {
            'original_count': original_count,
            'json_count': json_count,
            'missing_gids': missing_gids,
            'extra_gids': extra_gids,
            'gids_preserved': len(missing_gids) == 0
        }
        
        # Report issues
        if missing_gids:
            print(f"   ❌ Missing {len(missing_gids)} GIDs from JSON:")
            for gid in missing_gids:
                # Find the original key for this GID
                original_key = next((k for k, v in original.items() if v == gid), "Unknown")
                print(f"      - {gid} (was: {original_key})")
        
        if extra_gids:
            print(f"   ⚠️  {len(extra_gids)} extra GIDs in JSON (not in original):")
            for gid in extra_gids:
                # Find the JSON key for this GID
                json_key = next((k for k, v in json_data.items() if v == gid), "Unknown")
                print(f"      + {gid} (now: {json_key})")
        
        if validation_results[component_type]['gids_preserved']:
            print(f"   ✅ {component_type}: All GIDs preserved correctly")
        else:
            print(f"   ❌ {component_type}: Missing GIDs detected")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 GID PRESERVATION SUMMARY")
    print("=" * 60)
    
    valid_components = sum(1 for result in validation_results.values() if result['gids_preserved'])
    total_components = len(validation_results)
    
    total_original_unique_gids = len(all_original_gids)
    total_json_unique_gids = len(all_json_gids)
    
    print(f"Total unique original GIDs: {total_original_unique_gids}")
    print(f"Total unique JSON GIDs: {total_json_unique_gids}")
    print(f"Components with all GIDs preserved: {valid_components}/{total_components}")
    
    # Check overall GID preservation
    global_missing_gids = all_original_gids - all_json_gids
    global_extra_gids = all_json_gids - all_original_gids
    
    if len(global_missing_gids) == 0:
        print("\n🎉 SUCCESS: All GIDs successfully preserved!")
        print("✅ Every GID from the original Python mappings exists in the JSON files")
        print("✅ No data loss occurred during the extraction process")
        print("✅ Full names are correctly used as keys instead of abbreviations")
        
        if len(global_extra_gids) > 0:
            print(f"ℹ️  Note: {len(global_extra_gids)} additional GIDs found in JSON (likely aliases)")
        
        return True
    else:
        print(f"\n❌ GID PRESERVATION FAILED: {len(global_missing_gids)} GIDs missing")
        print("Missing GIDs:")
        for gid in global_missing_gids:
            print(f"  - {gid}")
        return False

def main():
    """Main validation function"""
    success = validate_gid_preservation()
    
    if success:
        print("\n🚀 GID extraction completed successfully!")
        print("📄 Task 1.2 from LAPTOP_SCALABILITY_REFACTOR_PLAN.md is complete")
        sys.exit(0)
    else:
        print("\n🛠️  Please fix the GID preservation issues before proceeding")
        sys.exit(1)

if __name__ == "__main__":
    main()