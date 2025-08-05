#!/usr/bin/env python3
"""
Validation script to ensure all GID values from the original Python mapping
have been correctly preserved in the JSON files.
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

def create_reverse_mapping(mapping_dict):
    """Create a reverse mapping from GID to name for comparison"""
    return {v: k for k, v in mapping_dict.items()}

def validate_mappings():
    """Validate that all GIDs from original mapping are preserved in JSON files"""
    print("🔍 Validating metaobject GID extraction...")
    print("=" * 60)
    
    # Load mappings
    original_mappings = load_original_mappings()
    json_mappings = load_json_mappings()
    
    if not original_mappings or not json_mappings:
        print("❌ Failed to load mappings")
        return False
    
    # Track validation results
    validation_results = {}
    total_original_gids = 0
    total_json_gids = 0
    
    # Validate each component type
    for component_type in original_mappings.keys():
        print(f"\n📋 Validating {component_type}...")
        
        original = original_mappings[component_type]
        json_data = json_mappings[component_type]
        
        original_count = len(original)
        json_count = len(json_data)
        
        total_original_gids += original_count
        total_json_gids += json_count
        
        print(f"   Original entries: {original_count}")
        print(f"   JSON entries: {json_count}")
        
        # Create reverse mappings for comparison
        original_gid_to_name = create_reverse_mapping(original)
        json_gid_to_name = create_reverse_mapping(json_data)
        
        # Check for missing GIDs
        missing_gids = set(original_gid_to_name.keys()) - set(json_gid_to_name.keys())
        extra_gids = set(json_gid_to_name.keys()) - set(original_gid_to_name.keys())
        
        # Check for name mismatches (same GID, different name)
        name_mismatches = []
        for gid in original_gid_to_name:
            if gid in json_gid_to_name:
                original_name = original_gid_to_name[gid]
                json_name = json_gid_to_name[gid]
                if original_name != json_name:
                    name_mismatches.append((gid, original_name, json_name))
        
        # Store results
        validation_results[component_type] = {
            'original_count': original_count,
            'json_count': json_count,
            'missing_gids': missing_gids,
            'extra_gids': extra_gids,
            'name_mismatches': name_mismatches,
            'valid': len(missing_gids) == 0 and len(extra_gids) == 0 and len(name_mismatches) == 0
        }
        
        # Report issues
        if missing_gids:
            print(f"   ❌ Missing {len(missing_gids)} GIDs:")
            for gid in missing_gids:
                print(f"      - {gid} ({original_gid_to_name[gid]})")
        
        if extra_gids:
            print(f"   ⚠️  Extra {len(extra_gids)} GIDs:")
            for gid in extra_gids:
                print(f"      + {gid} ({json_gid_to_name[gid]})")
        
        if name_mismatches:
            print(f"   ⚠️  {len(name_mismatches)} name mismatches:")
            for gid, orig_name, json_name in name_mismatches:
                print(f"      {gid}: '{orig_name}' → '{json_name}'")
        
        if validation_results[component_type]['valid']:
            print(f"   ✅ {component_type}: All GIDs preserved correctly")
        else:
            print(f"   ❌ {component_type}: Issues found")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    valid_components = sum(1 for result in validation_results.values() if result['valid'])
    total_components = len(validation_results)
    
    print(f"Total original GIDs: {total_original_gids}")
    print(f"Total JSON GIDs: {total_json_gids}")
    print(f"Valid components: {valid_components}/{total_components}")
    
    if valid_components == total_components:
        print("\n🎉 SUCCESS: All metaobject GIDs successfully extracted and preserved!")
        print("✅ All JSON files contain the exact same GID mappings as the original Python file")
        print("✅ Full names are used as keys (no abbreviations)")
        print("✅ Data integrity maintained throughout the extraction process")
        return True
    else:
        print(f"\n❌ VALIDATION FAILED: {total_components - valid_components} components have issues")
        print("Please review the issues above and correct the JSON files")
        return False

def main():
    """Main validation function"""
    success = validate_mappings()
    
    if success:
        print("\n🚀 Ready for next phase of laptop scalability refactor!")
        sys.exit(0)
    else:
        print("\n🛠️  Please fix the validation issues before proceeding")
        sys.exit(1)

if __name__ == "__main__":
    main()