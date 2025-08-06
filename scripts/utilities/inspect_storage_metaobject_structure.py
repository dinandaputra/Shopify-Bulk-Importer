#!/usr/bin/env python3
"""
Inspect the structure of existing storage metaobjects to understand the field schema.

Author: Shopify API Developer (Claude Code Sub-Agent System)
Version: 1.0.0
Date: 2025-08-06
"""

import sys
import os
import json
from typing import Dict, Any, List

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.shopify_api import ShopifyAPIClient, ShopifyAPIError

def inspect_storage_metaobject_structure():
    """Inspect the structure of existing storage metaobjects"""
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
                        type
                        fields {
                            key
                            value
                            type
                        }
                    }
                }
            }
        }
        """
        
        result = api_client._make_graphql_request(query, {"first": 10})
        edges = result.get("data", {}).get("metaobjects", {}).get("edges", [])
        metaobjects = [edge["node"] for edge in edges]
        
        print("="*80)
        print("STORAGE METAOBJECT STRUCTURE ANALYSIS")
        print("="*80)
        
        if not metaobjects:
            print("No storage metaobjects found")
            return {}
        
        print(f"Found {len(metaobjects)} storage metaobjects")
        
        # Analyze field structure
        field_analysis = {}
        
        for i, metaobject in enumerate(metaobjects):
            print(f"\n📋 Metaobject {i+1}: '{metaobject['displayName']}'")
            print(f"   GID: {metaobject['id']}")
            print(f"   Handle: {metaobject['handle']}")
            print(f"   Type: {metaobject['type']}")
            print(f"   Fields ({len(metaobject.get('fields', []))}):")
            
            for field in metaobject.get('fields', []):
                key = field.get('key', 'unknown')
                value = field.get('value', '')
                field_type = field.get('type', 'unknown')
                
                print(f"     - {key}: '{value}' (type: {field_type})")
                
                # Track field usage
                if key not in field_analysis:
                    field_analysis[key] = {
                        'count': 0,
                        'type': field_type,
                        'sample_values': []
                    }
                
                field_analysis[key]['count'] += 1
                if value not in field_analysis[key]['sample_values']:
                    field_analysis[key]['sample_values'].append(value)
        
        # Summary of field structure
        print(f"\n" + "="*80)
        print("FIELD STRUCTURE SUMMARY")
        print("="*80)
        
        for field_key, info in field_analysis.items():
            print(f"\n🔑 Field: '{field_key}'")
            print(f"   Type: {info['type']}")
            print(f"   Usage: {info['count']}/{len(metaobjects)} metaobjects")
            print(f"   Sample values: {info['sample_values'][:3]}")
            if len(info['sample_values']) > 3:
                print(f"   ... and {len(info['sample_values']) - 3} more")
        
        return field_analysis
        
    except Exception as e:
        print(f"✗ Error inspecting storage metaobjects: {e}")
        return {}

def get_metaobject_definition():
    """Get the metaobject definition for storage type"""
    try:
        api_client = ShopifyAPIClient()
        
        query = """
        query getMetaobjectDefinition($type: String!) {
            metaobjectDefinition(type: $type) {
                id
                name
                type
                displayNameKey
                fieldDefinitions {
                    key
                    name
                    type {
                        name
                    }
                    required
                    description
                    validations {
                        name
                        value
                    }
                }
            }
        }
        """
        
        result = api_client._make_graphql_request(query, {"type": "storage"})
        definition = result.get("data", {}).get("metaobjectDefinition")
        
        if definition:
            print(f"\n" + "="*80)
            print("STORAGE METAOBJECT DEFINITION")
            print("="*80)
            
            print(f"Definition ID: {definition['id']}")
            print(f"Name: {definition['name']}")
            print(f"Type: {definition['type']}")
            print(f"Display Name Key: {definition['displayNameKey']}")
            
            field_definitions = definition.get('fieldDefinitions', [])
            print(f"\nField Definitions ({len(field_definitions)}):")
            
            for field_def in field_definitions:
                key = field_def.get('key', 'unknown')
                name = field_def.get('name', 'unknown')
                field_type = field_def.get('type', {}).get('name', 'unknown')
                required = field_def.get('required', False)
                description = field_def.get('description', '')
                
                print(f"\n  📝 {key} ({name})")
                print(f"     Type: {field_type}")
                print(f"     Required: {required}")
                if description:
                    print(f"     Description: {description}")
                
                validations = field_def.get('validations', [])
                if validations:
                    print(f"     Validations:")
                    for validation in validations:
                        print(f"       - {validation['name']}: {validation['value']}")
            
            return definition
        else:
            print("⚠️  No metaobject definition found for 'storage' type")
            return None
            
    except Exception as e:
        print(f"✗ Error getting metaobject definition: {e}")
        return None

def main():
    """Main function to inspect storage metaobject structure"""
    print("STORAGE METAOBJECT STRUCTURE INSPECTION")
    
    # Step 1: Inspect existing metaobjects
    field_analysis = inspect_storage_metaobject_structure()
    
    # Step 2: Get metaobject definition
    definition = get_metaobject_definition()
    
    # Recommendations
    print(f"\n" + "="*80)
    print("RECOMMENDATIONS FOR CREATING 2TB SSD")
    print("="*80)
    
    if definition and definition.get('fieldDefinitions'):
        print("✓ Found metaobject definition - use these field keys:")
        for field_def in definition['fieldDefinitions']:
            key = field_def['key']
            required = field_def.get('required', False)
            field_type = field_def.get('type', {}).get('name', 'unknown')
            status = "REQUIRED" if required else "optional"
            print(f"   - {key} ({field_type}) [{status}]")
    elif field_analysis:
        print("⚠️  No definition found, but based on existing metaobjects:")
        for field_key, info in field_analysis.items():
            print(f"   - Use field key: '{field_key}' (type: {info['type']})")
    else:
        print("❌ Could not determine field structure")
    
    return bool(field_analysis or definition)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)