#!/usr/bin/env python3
"""
Create Missing Keyboard Backlight Color Metaobjects

This script creates the missing keyboard backlight metaobjects for specific colors
that are used in laptop templates: White, Blue, Green, Red.
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

def create_keyboard_backlight_metaobjects():
    """Create missing keyboard backlight color metaobjects"""
    
    api = ShopifyAPIClient()
    
    # Colors that are missing from the current keyboard backlight metaobjects
    missing_colors = [
        {"label": "White", "handle": "white"},
        {"label": "Blue", "handle": "blue"},
        {"label": "Green", "handle": "green"},
        {"label": "Red", "handle": "red"}
    ]
    
    definition_id = "gid://shopify/MetaobjectDefinition/10097787029"
    
    print("🛠️ Creating Missing Keyboard Backlight Color Metaobjects")
    print("=" * 60)
    print(f"Definition ID: {definition_id}")
    print(f"Creating {len(missing_colors)} color metaobjects...")
    print()
    
    created_metaobjects = []
    
    for color_data in missing_colors:
        label = color_data["label"]
        handle = color_data["handle"]
        
        print(f"🔨 Creating '{label}' keyboard backlight metaobject...")
        
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
                "type": "keyboard_backlight",  # Use the type handle, not the GID
                "handle": handle,
                "fields": [
                    {
                        "key": "label",
                        "value": label
                    }
                ]
            }
        }
        
        try:
            response = api.graphql_request(create_mutation, variables)
            
            if 'errors' in response:
                print(f"❌ GraphQL Errors for {label}:")
                for error in response['errors']:
                    print(f"   - {error['message']}")
                continue
            
            result = response['data']['metaobjectCreate']
            
            if result['userErrors']:
                print(f"❌ User Errors for {label}:")
                for error in result['userErrors']:
                    print(f"   - {error['field']}: {error['message']}")
                continue
            
            metaobject = result['metaobject']
            print(f"✅ Successfully created '{label}' keyboard backlight metaobject!")
            print(f"   ID: {metaobject['id']}")
            print(f"   Handle: {metaobject['handle']}")
            print(f"   Display Name: {metaobject['displayName']}")
            
            # Get the label field
            for field in metaobject['fields']:
                if field['key'] == 'label':
                    print(f"   Label: {field['value']}")
                    break
            
            created_metaobjects.append({
                'label': label,
                'gid': metaobject['id'],
                'handle': metaobject['handle']
            })
            print()
            
        except Exception as e:
            print(f"❌ Error creating {label} metaobject: {e}")
            print()
    
    # Generate the updated mapping
    print("=" * 60)
    print("🔄 Updated Keyboard Backlight Mapping")
    print("=" * 60)
    
    if created_metaobjects:
        print("Add these entries to KEYBOARD_BACKLIGHT_METAOBJECTS in laptop_metafield_mapping_actual.py:")
        print()
        
        for created in created_metaobjects:
            print(f'    "{created["label"]}": "{created["gid"]}",  # {created["label"]} keyboard backlight')
        
        print("\n📋 Complete mapping should include:")
        print("```python")
        print("KEYBOARD_BACKLIGHT_METAOBJECTS = {")
        print('    "Backlit": "gid://shopify/Metaobject/117265465493",')
        print('    "RGB Backlight": "gid://shopify/Metaobject/117265629333",')
        print('    "Non-backlit": "gid://shopify/Metaobject/117265662101",')
        
        for created in created_metaobjects:
            print(f'    "{created["label"]}": "{created["gid"]}",')
        
        print('    # Map common template values to existing metaobjects')
        print('    "RGB": "gid://shopify/Metaobject/117265629333",  # Map "RGB" to "RGB Backlight"')
        print('    "Yes": "gid://shopify/Metaobject/117265465493",  # Map "Yes" to "Backlit"')
        print('    "No": "gid://shopify/Metaobject/117265662101",   # Map "No" to "Non-backlit"')
        print("}")
        print("```")
        
    else:
        print("❌ No metaobjects were created successfully.")
    
    return created_metaobjects

if __name__ == "__main__":
    created = create_keyboard_backlight_metaobjects()
    
    if created:
        print(f"\n🎉 SUCCESS: Created {len(created)} keyboard backlight metaobjects!")
        print("💡 Next step: Update the mapping in laptop_metafield_mapping_actual.py with the new GIDs")
    else:
        print("\n❌ FAILED: No metaobjects were created")