#!/usr/bin/env python3
"""
Create Laptop Metaobjects - Final Working Version

This script creates metaobjects for laptop specifications using the correct
type strings and field names extracted from your Shopify store.
"""

import os
import json
from typing import Dict, List, Optional

# Load environment variables manually  
def load_env_file():
    """Load environment variables from .env file"""
    env_path = '/home/dinanda/Documents/Shopify-Bulk-Importer/.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

# Load environment variables before importing services
load_env_file()

from services.shopify_api import ShopifyAPIClient

# CORRECTED METAOBJECT TYPE STRINGS (from actual Shopify store)
LAPTOP_METAOBJECT_TYPES = {
    "processor": "processor",
    "graphics": "integrated_graphics", 
    "vga": "dedicated_graphics",
    "display": "display_laptop",
    "storage": "storage_laptop",
    "os": "os_laptop",
    "keyboard_layout": "keyboard_layout",
    "laptop_rank": "product_rank_laptop",
    "laptop_inclusions": "product_inclusion_laptop",
    "laptop_minus": "minus",
}

# Sample metaobjects to create
SAMPLE_METAOBJECTS_TO_CREATE = {
    "processor": [
        {"handle": "i7-13700h", "label": "Intel Core i7-13700H (20 CPUs), ~2.4GHz"},
        {"handle": "ryzen-7-6800h", "label": "AMD Ryzen 7 6800H (16 CPUs), ~3.2GHz"},
        {"handle": "apple-m3", "label": "Apple M3 8-Core CPU"},
        {"handle": "i9-13900k", "label": "Intel Core i9-13900K (24 CPUs), ~3.0GHz"},
        {"handle": "apple-m3-pro", "label": "Apple M3 Pro 12-Core CPU"}
    ],
    "graphics": [
        {"handle": "intel-iris-xe-g7", "label": "Intel Iris Xe Graphics G7 96EUs"},
        {"handle": "amd-radeon-680m", "label": "AMD Radeon 680M Graphics"},
        {"handle": "intel-uhd-graphics-770", "label": "Intel UHD Graphics 770"},
        {"handle": "apple-m3-gpu", "label": "Apple M3 10-Core GPU"}
    ],
    "vga": [
        {"handle": "rtx-4060", "label": "NVIDIA GeForce RTX 4060 8GB"},
        {"handle": "rtx-4070", "label": "NVIDIA GeForce RTX 4070 12GB"},
        {"handle": "rtx-4080", "label": "NVIDIA GeForce RTX 4080 16GB"},
        {"handle": "rtx-4060-ti", "label": "NVIDIA GeForce RTX 4060 Ti 16GB"}
    ],
    "display": [
        {"handle": "14-2k-90hz", "label": "14-inch 2K (90Hz)"},
        {"handle": "16-4k-60hz", "label": "16-inch 4K (60Hz)"},
        {"handle": "13-4k-60hz", "label": "13-inch 4K (60Hz)"},
        {"handle": "15-qhd-165hz", "label": "15-inch QHD (165Hz)"},
        {"handle": "17-fhd-144hz", "label": "17-inch FHD (144Hz)"}
    ],
    "storage": [
        {"handle": "2tb-ssd", "label": "2TB SSD"},
        {"handle": "1tb-ssd-1tb-hdd", "label": "1TB SSD + 1TB HDD Hybrid"},
        {"handle": "4tb-ssd", "label": "4TB SSD"},
        {"handle": "2tb-ssd-2tb-hdd", "label": "2TB SSD + 2TB HDD"}
    ],
    "os": [
        {"handle": "windows-11-pro", "label": "Windows 11 Pro"},
        {"handle": "ubuntu-22-04", "label": "Ubuntu 22.04 LTS"},
        {"handle": "macos-sonoma-14", "label": "macOS Sonoma 14"},
        {"handle": "windows-11-home", "label": "Windows 11 Home"}
    ],
    "laptop_rank": [
        {"handle": "excellent", "label": "Excellent"},
        {"handle": "very-good", "label": "Very Good"},
        {"handle": "good", "label": "Good"}
    ],
    "laptop_inclusions": [
        {"handle": "unit-charger-bonus", "label": "Unit + Charger + Bonus"},
        {"handle": "unit-original-box", "label": "Unit + Original Box"},
        {"handle": "unit-only", "label": "Unit Only"}
    ],
    "laptop_minus": [
        {"handle": "minor-scratches", "label": "Minor scratches"},
        {"handle": "keyboard-wear", "label": "Keyboard wear"},
        {"handle": "battery-degraded", "label": "Battery degradation"}
    ]
}

def create_metaobject(api_client: ShopifyAPIClient, type_string: str, handle: str, label: str) -> Optional[Dict]:
    """
    Create a single metaobject using GraphQL with correct field structure
    
    Args:
        api_client: Shopify API client instance
        type_string: Metaobject type string (e.g., "processor")
        handle: Unique handle for the metaobject
        label: Display label for the metaobject
        
    Returns:
        Created metaobject data or None if failed
    """
    
    mutation = """
    mutation createMetaobject($metaobject: MetaobjectCreateInput!) {
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
                code
            }
        }
    }
    """
    
    # Use correct field structure - all metaobjects use "label" field
    fields = [
        {"key": "label", "value": label}
    ]
    
    variables = {
        "metaobject": {
            "type": type_string,
            "handle": handle,
            "fields": fields
        }
    }
    
    try:
        response = api_client.graphql_request(mutation, variables)
        
        # Check for errors
        user_errors = response.get('data', {}).get('metaobjectCreate', {}).get('userErrors', [])
        if user_errors:
            print(f"❌ Error creating {handle}: {user_errors}")
            return None
        
        # Return created metaobject
        metaobject = response.get('data', {}).get('metaobjectCreate', {}).get('metaobject', {})
        if metaobject:
            print(f"✅ Created: {metaobject.get('displayName', label)} (ID: {metaobject.get('id', 'N/A')})")
        
        return metaobject
        
    except Exception as e:
        print(f"❌ Failed to create {handle}: {e}")
        return None

def main():
    """Main function to create sample laptop metaobjects"""
    
    # Initialize API client
    api_client = ShopifyAPIClient()
    
    # Test API connection
    try:
        shop_info = api_client.test_connection()
        print(f"✅ Connected to Shopify store: {shop_info['shop']['name']}")
    except Exception as e:
        print(f"❌ Failed to connect to Shopify API: {e}")
        return
    
    print(f"\n🚀 Creating sample laptop metaobjects using correct type strings...")
    
    # Track creation results
    creation_results = {}
    total_created = 0
    total_failed = 0
    
    # Create metaobjects for each category
    for category, metaobjects_list in SAMPLE_METAOBJECTS_TO_CREATE.items():
        print(f"\n📂 Creating {category.upper()} metaobjects:")
        print("=" * 50)
        
        type_string = LAPTOP_METAOBJECT_TYPES.get(category)
        if not type_string:
            print(f"❌ No type string found for category: {category}")
            continue
        
        print(f"🏷️  Using type: {type_string}")
        category_results = []
        
        for metaobject_data in metaobjects_list:
            handle = metaobject_data["handle"]
            label = metaobject_data["label"]
            
            print(f"🔧 Creating: {label}")
            
            created_metaobject = create_metaobject(
                api_client, 
                type_string, 
                handle, 
                label
            )
            
            if created_metaobject:
                category_results.append({
                    "handle": handle,
                    "label": label,
                    "id": created_metaobject.get('id'),
                    "success": True
                })
                total_created += 1
            else:
                category_results.append({
                    "handle": handle,
                    "label": label,
                    "id": None,
                    "success": False
                })
                total_failed += 1
        
        creation_results[category] = category_results
    
    # Print summary
    print(f"\n📊 CREATION SUMMARY:")
    print("=" * 60)
    print(f"✅ Successfully created: {total_created} metaobjects")
    print(f"❌ Failed to create: {total_failed} metaobjects")
    print(f"📈 Success rate: {(total_created/(total_created+total_failed)*100):.1f}%" if (total_created+total_failed) > 0 else "N/A")
    
    # Save results to file
    from datetime import datetime
    results = {
        'creation_timestamp': datetime.now().isoformat(),
        'shop_domain': api_client.config.SHOP_DOMAIN,
        'type_strings_used': LAPTOP_METAOBJECT_TYPES,
        'creation_results': creation_results,
        'summary': {
            'total_created': total_created,
            'total_failed': total_failed,
            'success_rate': (total_created/(total_created+total_failed)*100) if (total_created+total_failed) > 0 else 0
        }
    }
    
    output_file = '/home/dinanda/Documents/Shopify-Bulk-Importer/laptop_metaobjects_final_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    if total_created > 0:
        print(f"\n🎉 Successfully created {total_created} new laptop metaobjects!")
        print("You can now use these in your laptop product creation.")
        print("\n🔧 Next steps:")
        print("1. Update config/laptop_metafield_mapping_actual.py with new GIDs")
        print("2. Test laptop product creation with new metaobjects")
    
    if total_failed > 0:
        print(f"\n⚠️  {total_failed} metaobjects failed to create. Check the errors above.")

if __name__ == "__main__":
    main()