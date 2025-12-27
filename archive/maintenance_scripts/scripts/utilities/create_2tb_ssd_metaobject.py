#!/usr/bin/env python3
"""
Create a 2TB SSD metaobject in Shopify since it's needed but doesn't exist.

Author: Shopify API Developer (Claude Code Sub-Agent System)
Version: 1.0.0
Date: 2025-08-06
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.shopify_api import ShopifyAPIClient, ShopifyAPIError

def check_existing_2tb_ssd():
    """Check if 2TB SSD already exists"""
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
                    }
                }
            }
        }
        """
        
        result = api_client._make_graphql_request(query, {"first": 250})
        edges = result.get("data", {}).get("metaobjects", {}).get("edges", [])
        metaobjects = [edge["node"] for edge in edges]
        
        # Check for 2TB variants
        for metaobject in metaobjects:
            display_name = metaobject["displayName"].lower()
            if "2tb" in display_name or "2 tb" in display_name:
                print(f"⚠️  Found existing 2TB storage: '{metaobject['displayName']}' → {metaobject['id']}")
                return metaobject
        
        print("✓ No existing 2TB SSD found - safe to create")
        return None
        
    except Exception as e:
        print(f"✗ Error checking existing 2TB SSD: {e}")
        return None

def create_2tb_ssd_metaobject():
    """Create a 2TB SSD metaobject in Shopify"""
    try:
        api_client = ShopifyAPIClient()
        
        # GraphQL mutation to create metaobject
        mutation = """
        mutation metaobjectCreate($metaobject: MetaobjectCreateInput!) {
            metaobjectCreate(metaobject: $metaobject) {
                metaobject {
                    id
                    handle
                    displayName
                    type
                    fields {
                        key
                        value
                    }
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        variables = {
            "metaobject": {
                "type": "storage",
                "handle": "2tb-ssd",  # URL-friendly handle
                "fields": [
                    {
                        "key": "label",
                        "value": "2TB SSD"
                    }
                ]
            }
        }
        
        print("Creating 2TB SSD metaobject...")
        result = api_client._make_graphql_request(mutation, variables)
        
        # Check for errors
        user_errors = result.get("data", {}).get("metaobjectCreate", {}).get("userErrors", [])
        if user_errors:
            print("✗ Failed to create 2TB SSD metaobject:")
            for error in user_errors:
                print(f"   {error['field']}: {error['message']}")
            return None
        
        # Get the created metaobject
        metaobject = result.get("data", {}).get("metaobjectCreate", {}).get("metaobject")
        if metaobject:
            print(f"✅ Successfully created 2TB SSD metaobject!")
            print(f"   Display Name: {metaobject['displayName']}")
            print(f"   GID: {metaobject['id']}")
            print(f"   Handle: {metaobject['handle']}")
            return metaobject
        else:
            print("✗ Failed to create metaobject - no data returned")
            return None
            
    except Exception as e:
        print(f"✗ Error creating 2TB SSD metaobject: {e}")
        return None

def update_storage_json_with_2tb_ssd(metaobject):
    """Update storage.json with the new 2TB SSD metaobject"""
    storage_file = "data/metaobjects/storage.json"
    
    try:
        # Load current mappings
        with open(storage_file, 'r', encoding='utf-8') as f:
            mappings = json.load(f)
        
        # Add the new 2TB SSD mapping
        display_name = metaobject["displayName"]
        gid = metaobject["id"]
        
        mappings[display_name] = gid
        
        # Save updated mappings
        with open(storage_file, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Added '{display_name}' → {gid} to storage.json")
        print(f"✓ storage.json now contains {len(mappings)} mappings")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to update storage.json: {e}")
        return False

def main():
    """Main function to create 2TB SSD metaobject"""
    print("="*80)
    print("CREATE 2TB SSD METAOBJECT")
    print("="*80)
    print(f"Started at: {datetime.now().isoformat()}")
    
    # Step 1: Check if 2TB SSD already exists
    print("\n1. Checking for existing 2TB SSD metaobject...")
    existing = check_existing_2tb_ssd()
    
    if existing:
        print("⚠️  2TB storage already exists - updating storage.json instead")
        success = update_storage_json_with_2tb_ssd(existing)
        return success
    
    # Step 2: Create 2TB SSD metaobject
    print("\n2. Creating 2TB SSD metaobject in Shopify...")
    metaobject = create_2tb_ssd_metaobject()
    
    if not metaobject:
        print("❌ Failed to create 2TB SSD metaobject")
        return False
    
    # Step 3: Update storage.json
    print("\n3. Updating storage.json with new 2TB SSD...")
    success = update_storage_json_with_2tb_ssd(metaobject)
    
    # Final summary
    print("\n" + "="*80)
    print("CREATION SUMMARY")
    print("="*80)
    
    if success:
        print("✅ 2TB SSD metaobject successfully created!")
        print(f"✓ Shopify metaobject: {metaobject['displayName']} → {metaobject['id']}")
        print("✓ storage.json updated")
        
        print(f"\nNext steps:")
        print("1. Re-run GID resolution to test with new metaobject")
        print("2. Update missing entries report")
        
        return True
    else:
        print("❌ Creation completed but storage.json update failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)