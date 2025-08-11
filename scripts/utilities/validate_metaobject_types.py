#!/usr/bin/env python3
"""
Metaobject Types Validation Script

This script validates what metaobject types exist in Shopify and provides
detailed analysis of why the GID resolution returned 0 results.

Author: Shopify API Developer (Claude Code Sub-Agent System)
Date: 2025-08-06
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.shopify_api import ShopifyAPIClient, ShopifyAPIError


def query_all_metaobject_definitions(api_client: ShopifyAPIClient) -> dict:
    """Query all metaobject definitions to see what types exist in Shopify"""
    
    query = """
    query GetAllMetaobjectDefinitions {
      metaobjectDefinitions(first: 50) {
        nodes {
          id
          type
          name
          description
          displayNameKey
          fieldDefinitions {
            key
            name
            type {
              name
            }
          }
        }
      }
    }
    """
    
    try:
        response = api_client._make_graphql_request(query)
        return response
    except Exception as e:
        print(f"❌ Failed to query metaobject definitions: {e}")
        return {"data": {"metaobjectDefinitions": {"nodes": []}}}


def query_metaobjects_by_type(api_client: ShopifyAPIClient, metaobject_type: str) -> dict:
    """Query metaobjects of a specific type to see what exists"""
    
    query = """
    query GetMetaobjectsByType($type: String!, $first: Int!) {
      metaobjects(type: $type, first: $first) {
        nodes {
          id
          type
          displayName
          handle
          fields {
            key
            value
          }
        }
      }
    }
    """
    
    variables = {
        "type": metaobject_type,
        "first": 20
    }
    
    try:
        response = api_client._make_graphql_request(query, variables)
        return response
    except Exception as e:
        print(f"❌ Failed to query metaobjects for type {metaobject_type}: {e}")
        return {"data": {"metaobjects": {"nodes": []}}}


def main():
    """Main validation function"""
    print("🔍 Validating Metaobject Types in Shopify")
    print("=" * 50)
    
    try:
        api_client = ShopifyAPIClient()
        print("✅ Shopify API client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Shopify API client: {e}")
        return 1
    
    # Step 1: Query all metaobject definitions
    print("\n📋 Querying all metaobject definitions...")
    definitions_response = query_all_metaobject_definitions(api_client)
    
    definitions = definitions_response.get('data', {}).get('metaobjectDefinitions', {}).get('nodes', [])
    
    print(f"Found {len(definitions)} metaobject definitions:")
    
    existing_types = set()
    for definition in definitions:
        print(f"  • {definition['type']} - {definition['name']}")
        existing_types.add(definition['type'])
    
    # Step 2: Check if our target types exist
    target_types = ["laptop_vga", "laptop_graphics", "laptop_displays", "laptop_storage"]
    
    print(f"\n🎯 Checking target metaobject types...")
    missing_types = []
    
    for target_type in target_types:
        if target_type in existing_types:
            print(f"  ✅ {target_type} - EXISTS")
            
            # Query some examples
            examples_response = query_metaobjects_by_type(api_client, target_type)
            examples = examples_response.get('data', {}).get('metaobjects', {}).get('nodes', [])
            print(f"     Found {len(examples)} metaobjects of this type")
            
            for example in examples[:3]:  # Show first 3 examples
                print(f"       - {example.get('displayName', 'No display name')}")
                
        else:
            print(f"  ❌ {target_type} - MISSING")
            missing_types.append(target_type)
    
    # Step 3: Check existing working types
    print(f"\n🔍 Checking existing working metaobject types...")
    working_types = ["processors", "colors", "keyboard_backlights", "keyboard_layouts", "os"]
    
    for working_type in working_types:
        if working_type in existing_types:
            print(f"  ✅ {working_type} - EXISTS (working)")
            
            # Query some examples
            examples_response = query_metaobjects_by_type(api_client, working_type)
            examples = examples_response.get('data', {}).get('metaobjects', {}).get('nodes', [])
            print(f"     Found {len(examples)} metaobjects")
            
        else:
            print(f"  ❌ {working_type} - MISSING (should exist)")
    
    # Step 4: Generate report
    print(f"\n📊 VALIDATION REPORT")
    print("=" * 30)
    
    if missing_types:
        print(f"🔴 MISSING METAOBJECT TYPES ({len(missing_types)}):")
        for missing_type in missing_types:
            print(f"   • {missing_type}")
        
        print(f"\n💡 EXPLANATION:")
        print(f"   The GID resolution script returned 0 results because the metaobject")
        print(f"   types for VGA, Graphics, Displays, and Storage don't exist in Shopify yet.")
        print(f"   ")
        print(f"   These types need to be created in Shopify Admin first:")
        print(f"   1. Go to Shopify Admin > Settings > Custom Data")
        print(f"   2. Create metaobject definitions for: {', '.join(missing_types)}")
        print(f"   3. Add the required fields for each type")
        print(f"   4. Create individual metaobjects for each component")
        print(f"   5. Re-run the GID resolution script")
        
    else:
        print(f"✅ ALL TARGET METAOBJECT TYPES EXIST")
        print(f"   The metaobject types exist but no individual metaobjects were found")
        print(f"   matching the search terms. This suggests the metaobjects need to be")
        print(f"   created manually or the search terms need adjustment.")
    
    # Step 5: Save validation results
    validation_results = {
        "timestamp": datetime.now().isoformat(),
        "total_definitions_found": len(definitions),
        "existing_types": list(existing_types),
        "target_types": target_types,
        "missing_target_types": missing_types,
        "working_types_status": {
            wt: wt in existing_types for wt in working_types
        },
        "all_definitions": [
            {
                "type": d['type'],
                "name": d['name'],
                "description": d.get('description', ''),
                "field_count": len(d.get('fieldDefinitions', []))
            }
            for d in definitions
        ]
    }
    
    results_file = Path(__file__).parent.parent.parent / "data" / "analysis" / "metaobject_types_validation.json"
    
    try:
        results_file.parent.mkdir(parents=True, exist_ok=True)
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(validation_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Validation results saved to: {results_file}")
        
    except Exception as e:
        print(f"⚠️ Failed to save validation results: {e}")
    
    print(f"\n✅ Metaobject types validation completed!")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)