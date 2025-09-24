#!/usr/bin/env python3
"""
Update Test Imports Script - Phase 4.2
Automated script to update import paths in test files for laptop scalability refactor.
"""

import os
import re
import glob
from typing import List, Tuple

def update_imports_in_file(file_path: str) -> Tuple[bool, List[str]]:
    """
    Update imports in a single file
    
    Args:
        file_path: Path to the file to update
        
    Returns:
        Tuple of (changed, list_of_changes)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return False, [f"Error reading file: {str(e)}"]
    
    content = original_content
    changes = []
    
    # Define replacement patterns
    replacements = [
        # Laptop specs imports
        (r'from config\.laptop_specs import', 'from services.template_cache_service import TemplateCacheService'),
        
        # Laptop metafield mapping imports
        (r'from config\.laptop_metafield_mapping import', 'from repositories.metaobject_repository import MetaobjectRepository'),
        (r'from config\.laptop_metafield_mapping_enhanced import', 'from repositories.metaobject_repository import MetaobjectRepository'),
        (r'from config\.laptop_metafield_mapping_actual import', 'from repositories.metaobject_repository import MetaobjectRepository'),
        
        # Specific function imports that need updating
        (r'TemplateCacheService().get_all_templates', 'TemplateCacheService().get_all_templates'),
        (r'TemplateCacheService().parse_template', 'TemplateCacheService().parse_template'),
        (r'MetaobjectRepository().get_gid', 'MetaobjectRepository().get_gid'),
        
        # Update test function calls
        (r'MetaobjectRepository().get_gid\(([^)]+)\)', r'# Updated to use MetaobjectRepository - MetaobjectRepository().get_gid(\1)'),
    ]
    
    for pattern, replacement in replacements:
        old_content = content
        content = re.sub(pattern, replacement, content)
        if content != old_content:
            changes.append(f"Updated: {pattern} -> {replacement}")
    
    # Write back if changes were made
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes
        except Exception as e:
            return False, [f"Error writing file: {str(e)}"]
    
    return False, []

def update_all_test_files() -> None:
    """Update all test files in the project"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Find all Python test files
    test_patterns = [
        'tests/**/*.py',
        'test_*.py',
        '*_test.py',
        '**/*test*.py'
    ]
    
    all_test_files = set()
    for pattern in test_patterns:
        test_files = glob.glob(os.path.join(base_dir, pattern), recursive=True)
        all_test_files.update(test_files)
    
    print(f"Found {len(all_test_files)} potential test files")
    
    total_updated = 0
    total_changes = 0
    
    for file_path in sorted(all_test_files):
        # Skip if file doesn't exist or is not a Python file
        if not os.path.exists(file_path) or not file_path.endswith('.py'):
            continue
            
        print(f"\nProcessing: {os.path.relpath(file_path, base_dir)}")
        
        changed, changes = update_imports_in_file(file_path)
        
        if changed:
            total_updated += 1
            total_changes += len(changes)
            print(f"  ✅ Updated {len(changes)} imports:")
            for change in changes:
                print(f"    - {change}")
        else:
            print("  ⏭️  No updates needed")
    
    print(f"\n🎉 Summary:")
    print(f"Files updated: {total_updated}")
    print(f"Total changes: {total_changes}")
    
    if total_updated == 0:
        print("✨ All test files are already up to date!")

if __name__ == "__main__":
    print("🔧 Updating test file imports for Phase 4.2...")
    update_all_test_files()
    print("\n✅ Test import update complete!")