#!/usr/bin/env python3
"""
Update storage.json mappings with correct current Shopify metaobject data.
Create backup of old file before updating.

Author: Shopify API Developer (Claude Code Sub-Agent System)
Version: 1.0.0
Date: 2025-08-06
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any
import shutil

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.shopify_api import ShopifyAPIClient, ShopifyAPIError

def backup_current_storage_file():
    """Create a backup of the current storage.json file"""
    storage_file = "data/metaobjects/storage.json"
    backup_dir = "data/metaobjects/backups"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/storage_backup_{timestamp}.json"
    
    try:
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copy the current file to backup
        if os.path.exists(storage_file):
            shutil.copy2(storage_file, backup_file)
            print(f"✓ Created backup: {backup_file}")
            return backup_file
        else:
            print(f"⚠️  No existing storage.json file to backup")
            return None
    except Exception as e:
        print(f"✗ Failed to create backup: {e}")
        return None

def get_shopify_storage_metaobjects():
    """Get all current storage metaobjects from Shopify"""
    try:
        api_client = ShopifyAPIClient()
        
        query = """
        query getStorageMetaobjects($first: Int!) {
            metaobjects(type: "storage", first: $first) {
                edges {
                    node {
                        id
                        handle
                        displayName
                        fields {
                            key
                            value
                        }
                    }
                }
            }
        }
        """
        
        result = api_client._make_graphql_request(query, {"first": 250})
        edges = result.get("data", {}).get("metaobjects", {}).get("edges", [])
        metaobjects = [edge["node"] for edge in edges]
        
        print(f"✓ Retrieved {len(metaobjects)} storage metaobjects from Shopify")
        return metaobjects
        
    except Exception as e:
        print(f"✗ Failed to retrieve Shopify storage metaobjects: {e}")
        return []

def create_updated_mappings(shopify_metaobjects):
    """Create updated storage mappings based on current Shopify data"""
    print("\n" + "="*80)
    print("CREATING UPDATED STORAGE MAPPINGS")
    print("="*80)
    
    updated_mappings = {}
    
    print(f"\nProcessing {len(shopify_metaobjects)} Shopify storage metaobjects:")
    
    for metaobject in sorted(shopify_metaobjects, key=lambda x: x["displayName"]):
        display_name = metaobject["displayName"]
        gid = metaobject["id"]
        handle = metaobject["handle"]
        
        # For storage components, we might want to add "SSD" suffix for consistency
        # but let's keep the exact Shopify display names for accuracy
        mapping_key = display_name
        
        updated_mappings[mapping_key] = gid
        
        print(f"  ✓ '{mapping_key}' → {gid}")
    
    print(f"\n✓ Created {len(updated_mappings)} updated mappings")
    return updated_mappings

def save_updated_mappings(updated_mappings):
    """Save the updated mappings to storage.json"""
    storage_file = "data/metaobjects/storage.json"
    
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(storage_file), exist_ok=True)
        
        # Save updated mappings
        with open(storage_file, 'w', encoding='utf-8') as f:
            json.dump(updated_mappings, f, indent=2, ensure_ascii=False)
        
        file_size = os.path.getsize(storage_file) / 1024
        print(f"✓ Updated storage.json saved ({file_size:.1f} KB)")
        print(f"✓ File location: {storage_file}")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to save updated mappings: {e}")
        return False

def validate_updated_file():
    """Validate the updated storage.json file"""
    storage_file = "data/metaobjects/storage.json"
    
    try:
        with open(storage_file, 'r', encoding='utf-8') as f:
            mappings = json.load(f)
        
        print(f"\n✓ Validation: File contains {len(mappings)} mappings")
        
        # Check GID format
        valid_gids = 0
        for name, gid in mappings.items():
            if gid.startswith("gid://shopify/Metaobject/"):
                valid_gids += 1
            else:
                print(f"⚠️  Invalid GID format: {name} → {gid}")
        
        print(f"✓ Validation: {valid_gids}/{len(mappings)} GIDs have correct format")
        
        return valid_gids == len(mappings)
        
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False

def main():
    """Main function to update storage mappings"""
    print("="*80)
    print("STORAGE MAPPINGS UPDATE")
    print("="*80)
    print(f"Started at: {datetime.now().isoformat()}")
    
    # Step 1: Create backup
    print("\n1. Creating backup of current storage.json...")
    backup_file = backup_current_storage_file()
    
    # Step 2: Get current Shopify data
    print("\n2. Retrieving current Shopify storage metaobjects...")
    shopify_metaobjects = get_shopify_storage_metaobjects()
    
    if not shopify_metaobjects:
        print("❌ Cannot proceed without Shopify data")
        return False
    
    # Step 3: Create updated mappings
    print("\n3. Creating updated mappings...")
    updated_mappings = create_updated_mappings(shopify_metaobjects)
    
    # Step 4: Save updated mappings
    print("\n4. Saving updated mappings...")
    success = save_updated_mappings(updated_mappings)
    
    if not success:
        print("❌ Failed to save updated mappings")
        return False
    
    # Step 5: Validate updated file
    print("\n5. Validating updated file...")
    valid = validate_updated_file()
    
    # Final summary
    print("\n" + "="*80)
    print("UPDATE SUMMARY")
    print("="*80)
    
    if valid:
        print("✅ Storage mappings successfully updated!")
        print(f"✓ Backup created: {backup_file}")
        print(f"✓ Updated mappings: {len(updated_mappings)} entries")
        print("✓ All GIDs validated")
        
        print(f"\nNext steps:")
        print("1. Re-run GID resolution to test with updated mappings")
        print("2. Consider creating '2TB SSD' metaobject in Shopify if needed")
        
        return True
    else:
        print("❌ Update completed but validation failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)