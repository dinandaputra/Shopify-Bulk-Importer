#!/usr/bin/env python3
"""
Query Keyboard Backlight Metaobjects

This script queries the Shopify store to fetch all existing keyboard backlight metaobjects
and identifies which entries are missing, specifically looking for "RGB".
"""

import sys
import os
from dotenv import load_dotenv

# Change to project root directory
project_root = os.path.join(os.path.dirname(__file__), '../..')
os.chdir(project_root)
sys.path.append(project_root)

# Load environment variables
load_dotenv()

from services.shopify_api import ShopifyAPIClient
from pprint import pprint

def query_keyboard_backlight_metaobjects():
    """Query all keyboard backlight metaobjects from Shopify store"""
    
    api = ShopifyAPIClient()
    
    # Definition ID for keyboard backlight from the mapping
    keyboard_backlight_definition_id = "gid://shopify/MetaobjectDefinition/10097787029"
    
    print("🔍 Querying Keyboard Backlight Metaobjects...")
    print(f"Definition ID: {keyboard_backlight_definition_id}")
    print("-" * 60)
    
    # GraphQL query to fetch all metaobjects for keyboard backlight definition
    query = """
    query getKeyboardBacklightMetaobjects($type: String!, $first: Int!) {
        metaobjects(type: $type, first: $first) {
            nodes {
                id
                handle
                displayName
                fields {
                    key
                    value
                }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
    """
    
    variables = {
        "type": "keyboard_backlight",
        "first": 50
    }
    
    try:
        response = api.graphql_request(query, variables)
        
        if 'errors' in response:
            print("❌ GraphQL Errors:")
            for error in response['errors']:
                print(f"   - {error['message']}")
            return None
        
        metaobjects = response['data']['metaobjects']['nodes']
        
        print(f"✅ Found {len(metaobjects)} keyboard backlight metaobjects:")
        print()
        
        existing_values = []
        for metaobject in metaobjects:
            display_name = metaobject['displayName']
            handle = metaobject['handle']
            gid = metaobject['id']
            
            print(f"🔘 {display_name}")
            print(f"   Handle: {handle}")
            print(f"   GID: {gid}")
            
            # Get label field value
            for field in metaobject['fields']:
                if field['key'] == 'label':
                    print(f"   Label: {field['value']}")
                    existing_values.append(field['value'])
                    break
            print()
        
        # Check for missing "RGB" value
        print("-" * 60)
        print("📋 Analysis:")
        
        # Values we expect based on templates
        expected_values = ["RGB", "White", "Blue", "Green", "Red", "Yes"]
        
        print(f"Expected values: {expected_values}")
        print(f"Existing values: {existing_values}")
        
        missing_values = [value for value in expected_values if value not in existing_values]
        
        if missing_values:
            print(f"❌ Missing values: {missing_values}")
            
            if "RGB" in missing_values:
                print()
                print("🎯 CONFIRMED: 'RGB' metaobject entry is missing!")
                print("   This explains the 'Some specifications don't have metaobject entries yet: • Keyboard Backlight: RGB' warning")
        else:
            print("✅ All expected values are present")
        
        return {
            'existing_metaobjects': metaobjects,
            'existing_values': existing_values,
            'missing_values': missing_values
        }
        
    except Exception as e:
        print(f"❌ Error querying metaobjects: {e}")
        return None

def create_missing_rgb_metaobject():
    """Create the missing RGB keyboard backlight metaobject"""
    
    api = ShopifyAPIClient()
    
    # Create the RGB metaobject
    create_mutation = """
    mutation createMetaobject($metaobject: MetaobjectCreateInput!) {
        metaobjectCreate(metaobject: $metaobject) {
            metaobject {
                id
                handle
                displayName
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
            "type": "gid://shopify/MetaobjectDefinition/10097787029",
            "handle": "rgb",
            "fields": [
                {
                    "key": "label",
                    "value": "RGB"
                }
            ]
        }
    }
    
    print("🛠️ Creating missing 'RGB' keyboard backlight metaobject...")
    print(f"Definition: gid://shopify/MetaobjectDefinition/10097787029")
    print(f"Handle: rgb")
    print(f"Label: RGB")
    print()
    
    try:
        response = api.graphql_request(create_mutation, variables)
        
        if 'errors' in response:
            print("❌ GraphQL Errors:")
            for error in response['errors']:
                print(f"   - {error['message']}")
            return None
        
        result = response['data']['metaobjectCreate']
        
        if result['userErrors']:
            print("❌ User Errors:")
            for error in result['userErrors']:
                print(f"   - {error['field']}: {error['message']}")
            return None
        
        metaobject = result['metaobject']
        print("✅ Successfully created RGB keyboard backlight metaobject!")
        print(f"   ID: {metaobject['id']}")
        print(f"   Handle: {metaobject['handle']}")
        print(f"   Display Name: {metaobject['displayName']}")
        
        # Get the label field
        for field in metaobject['fields']:
            if field['key'] == 'label':
                print(f"   Label: {field['value']}")
                break
        
        return metaobject['id']
        
    except Exception as e:
        print(f"❌ Error creating metaobject: {e}")
        return None

if __name__ == "__main__":
    print("🔍 Keyboard Backlight Metaobject Analysis")
    print("=" * 60)
    
    # First, query existing metaobjects
    result = query_keyboard_backlight_metaobjects()
    
    if result and "RGB" in result.get('missing_values', []):
        print("\n" + "=" * 60)
        print("🛠️ Creating Missing RGB Metaobject")
        print("=" * 60)
        
        rgb_gid = create_missing_rgb_metaobject()
        
        if rgb_gid:
            print("\n" + "=" * 60)
            print("✅ SUCCESS: RGB metaobject created!")
            print("🔄 Re-querying to verify...")
            print("=" * 60)
            
            # Verify by re-querying
            verification_result = query_keyboard_backlight_metaobjects()
            
            if verification_result and "RGB" not in verification_result.get('missing_values', []):
                print("\n🎉 VERIFICATION SUCCESSFUL: RGB metaobject is now available!")
                print("💡 Next step: Update the keyboard backlight mapping to include the new GID")
            else:
                print("\n❌ VERIFICATION FAILED: RGB metaobject still missing")
        else:
            print("\n❌ FAILED: Could not create RGB metaobject")