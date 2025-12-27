#!/usr/bin/env python3
"""
Complete GID Resolution Script for Laptop Component Mapping

This script completes the Phase 6 GID resolution by fetching missing GIDs 
for all remaining unmapped laptop components (VGA, Graphics, Displays, Storage).

Based on the analysis files, this script targets:
- VGA (16 components): RTX 3050 Ti, RTX 4070 12GB, RTX 2070 8GB, etc.
- Graphics (3 components): AMD Radeon Graphics, AMD Radeon 680M Graphics, Intel UHD Graphics 770
- Displays (12 components): 15-inch 4K UHD (60Hz), 17.3 300Hz, etc.
- Storage (1 component): 2TB SSD

Author: Shopify API Developer (Claude Code Sub-Agent System)
Date: 2025-08-06
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.gid_resolution_service import GIDResolutionService, GIDResolutionResults
from services.shopify_api import ShopifyAPIClient, ShopifyAPIError


class JSONMappingUpdater:
    """Service to update JSON mapping files with new GIDs using backup system"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.metaobjects_dir = self.project_root / "data" / "metaobjects"
        self.backups_dir = self.metaobjects_dir / "backups"
    
    def create_backup(self) -> Path:
        """Create timestamped backup of all current mapping files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backups_dir / f"gid_resolution_backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📦 Creating backup in: {backup_dir}")
        
        # Backup all JSON mapping files
        mapping_files = ["vga.json", "graphics.json", "displays.json", "storage.json"]
        
        for filename in mapping_files:
            source_file = self.metaobjects_dir / filename
            if source_file.exists():
                backup_file = backup_dir / filename
                backup_file.write_text(source_file.read_text(encoding='utf-8'))
                print(f"  ✅ Backed up: {filename}")
        
        return backup_dir
    
    def update_mapping_files(self, results: GIDResolutionResults) -> Dict[str, int]:
        """
        Update JSON mapping files with newly found GIDs
        
        Args:
            results: GID resolution results containing new mappings
            
        Returns:
            Dictionary with count of updates per file
        """
        update_counts = {}
        
        for component_type, components in results.resolved_components.items():
            if not components:
                continue
            
            # Map component type to JSON filename
            filename_mapping = {
                "vga": "vga.json",
                "graphics": "graphics.json", 
                "displays": "displays.json",
                "storage": "storage.json"
            }
            
            filename = filename_mapping.get(component_type)
            if not filename:
                print(f"⚠️ Unknown component type for file mapping: {component_type}")
                continue
            
            # Load existing mappings
            mapping_file = self.metaobjects_dir / filename
            try:
                if mapping_file.exists():
                    with open(mapping_file, 'r', encoding='utf-8') as f:
                        existing_mappings = json.load(f)
                else:
                    existing_mappings = {}
                    print(f"  ℹ️ Creating new mapping file: {filename}")
                
                # Add new mappings
                updates_made = 0
                for comp_name, search_result in components.items():
                    if comp_name not in existing_mappings:
                        existing_mappings[comp_name] = search_result.gid
                        updates_made += 1
                        print(f"  ➕ Added: {comp_name} -> {search_result.gid}")
                    else:
                        print(f"  ⚠️ Skipped existing: {comp_name}")
                
                # Save updated mappings
                if updates_made > 0:
                    with open(mapping_file, 'w', encoding='utf-8') as f:
                        json.dump(existing_mappings, f, indent=2, ensure_ascii=False)
                    
                    update_counts[filename] = updates_made
                    print(f"  💾 Updated {filename} with {updates_made} new mappings")
                else:
                    update_counts[filename] = 0
                    print(f"  ✅ No updates needed for {filename}")
                
            except Exception as e:
                print(f"  ❌ Error updating {filename}: {e}")
                update_counts[filename] = -1
        
        return update_counts
    
    def validate_updates(self, results: GIDResolutionResults) -> bool:
        """
        Validate that all updates were successful
        
        Args:
            results: GID resolution results to validate
            
        Returns:
            True if all updates are valid, False otherwise
        """
        print("🔍 Validating JSON mapping updates...")
        
        validation_passed = True
        
        for component_type, components in results.resolved_components.items():
            filename_mapping = {
                "vga": "vga.json",
                "graphics": "graphics.json",
                "displays": "displays.json", 
                "storage": "storage.json"
            }
            
            filename = filename_mapping.get(component_type)
            if not filename:
                continue
            
            mapping_file = self.metaobjects_dir / filename
            
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    current_mappings = json.load(f)
                
                # Check each resolved component is in the file
                for comp_name, search_result in components.items():
                    if comp_name not in current_mappings:
                        print(f"  ❌ Missing from {filename}: {comp_name}")
                        validation_passed = False
                    elif current_mappings[comp_name] != search_result.gid:
                        print(f"  ❌ GID mismatch in {filename} for {comp_name}")
                        print(f"      Expected: {search_result.gid}")
                        print(f"      Found: {current_mappings[comp_name]}")
                        validation_passed = False
                    else:
                        print(f"  ✅ Validated: {comp_name} in {filename}")
                
            except Exception as e:
                print(f"  ❌ Error validating {filename}: {e}")
                validation_passed = False
        
        return validation_passed


def main():
    """Main execution function for complete GID resolution"""
    print("🚀 Starting Complete GID Resolution for Laptop Components")
    print("=" * 70)
    
    # Initialize services
    try:
        shopify_client = ShopifyAPIClient()
        gid_service = GIDResolutionService(shopify_client)
        json_updater = JSONMappingUpdater()
        
        print("✅ Services initialized successfully")
        
    except Exception as e:
        print(f"❌ Failed to initialize services: {e}")
        return 1
    
    # Define missing components based on analysis results
    missing_components = {
        "vga": [
            "RTX 3050 Ti",
            "NVIDIA GeForce RTX 4070 12GB",
            "NVIDIA GeForce RTX 2070 8GB",
            "NVIDIA GeForce RTX 2080 8GB",
            "NVIDIA GeForce RTX 4090 16GB",
            "NVIDIA GeForce RTX 3080 10GB",
            "NVIDIA GeForce RTX 2060 6GB",
            "NVIDIA GeForce GTX 1650 Ti 4GB",
            "NVIDIA GeForce RTX 4080 16GB",
            "NVIDIA GeForce RTX 3050 4GB",
            "NVIDIA GeForce RTX 3070 8GB",
            "NVIDIA GeForce GTX 1660 Ti 6GB",
            "NVIDIA GeForce RTX 3070 Ti 8GB",
            "NVIDIA GeForce RTX 3080 Ti 12GB",
            "NVIDIA GeForce GTX 1650 4GB",
            "NVIDIA GeForce RTX 4060 8GB"
        ],
        "graphics": [
            "AMD Radeon Graphics",
            "AMD Radeon 680M Graphics",
            "Intel UHD Graphics 770"
        ],
        "displays": [
            "15-inch 4K UHD (60Hz)",
            "17.3 300Hz",
            "16-inch OLED (240Hz)",
            "15-inch FHD (120Hz)",
            "17.3-inch FHD (240Hz)",
            "17.3 120Hz",
            "15-inch QHD (165Hz)",
            "14-inch QHD (120Hz)",
            "15-inch FHD (165Hz)",
            "17.3-inch FHD (144Hz)",
            "15-inch FHD (144Hz)",
            "17.3-inch FHD (165Hz)"
        ],
        "storage": [
            "2TB SSD"
        ]
    }
    
    print(f"📋 Components to resolve:")
    for comp_type, components in missing_components.items():
        print(f"  • {comp_type.upper()}: {len(components)} components")
    
    # Step 1: Create backup of current mappings
    try:
        backup_dir = json_updater.create_backup()
        print(f"✅ Backup created successfully: {backup_dir}")
        
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return 1
    
    # Step 2: Resolve missing GIDs
    try:
        print(f"\n🔍 Starting GID resolution...")
        results = gid_service.resolve_missing_gids(missing_components)
        
        print(f"✅ GID resolution completed")
        
    except Exception as e:
        print(f"❌ Failed to resolve GIDs: {e}")
        return 1
    
    # Step 3: Update JSON mapping files
    try:
        print(f"\n📝 Updating JSON mapping files...")
        update_counts = json_updater.update_mapping_files(results)
        
        total_updates = sum(count for count in update_counts.values() if count > 0)
        print(f"✅ JSON files updated with {total_updates} new mappings")
        
        # Display update summary
        for filename, count in update_counts.items():
            if count > 0:
                print(f"  • {filename}: {count} new mappings")
            elif count == 0:
                print(f"  • {filename}: No updates needed")
            else:
                print(f"  • {filename}: Update failed")
        
    except Exception as e:
        print(f"❌ Failed to update JSON files: {e}")
        return 1
    
    # Step 4: Validate updates
    try:
        print(f"\n🔍 Validating updates...")
        validation_passed = json_updater.validate_updates(results)
        
        if validation_passed:
            print(f"✅ All updates validated successfully")
        else:
            print(f"❌ Validation failed - check output above")
            return 1
        
    except Exception as e:
        print(f"❌ Failed to validate updates: {e}")
        return 1
    
    # Step 5: Save detailed results
    try:
        results_file = Path(__file__).parent.parent.parent / "data" / "analysis" / "complete_gid_resolution_results.json"
        gid_service.save_results_to_file(results, results_file)
        
    except Exception as e:
        print(f"⚠️ Failed to save results file: {e}")
        # Don't return error for this - it's not critical
    
    # Step 6: Generate final report
    print(f"\n📊 FINAL REPORT")
    print("=" * 50)
    print(f"✅ GID Resolution Status:")
    print(f"   • Total components processed: {results.total_components_processed}")
    print(f"   • Successfully found: {results.components_found}")
    print(f"   • Not found: {results.components_not_found}")
    print(f"   • Success rate: {results.success_rate_percent}%")
    print(f"   • Processing time: {results.processing_time_seconds}s")
    print(f"   • API calls made: {results.api_calls_made}")
    
    print(f"\n📂 Updated Files:")
    for filename, count in update_counts.items():
        if count > 0:
            print(f"   • {filename}: +{count} new GID mappings")
    
    if results.components_not_found > 0:
        print(f"\n🔴 Components still needing manual creation in Shopify:")
        for comp_type, not_found_list in results.not_found_components.items():
            if not_found_list:
                print(f"   • {comp_type.upper()}: {', '.join(not_found_list)}")
    
    print(f"\n✅ Complete GID Resolution finished successfully!")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)