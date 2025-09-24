#!/usr/bin/env python3
"""
Color Metaobject Discrepancy Investigation Script

This script investigates the conflict between iPhone 11 Pro Max color mappings:
- iphone_specs.py maps "Midnight Green" to GID 127395266709
- colors.json maps "Alpine Green" to GID 127395266709

We'll fetch the actual metaobject from Shopify to determine the correct color name.
"""

import sys
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.shopify_api import ShopifyAPIClient, ShopifyAPIError

def fetch_metaobject_by_gid(client: ShopifyAPIClient, gid: str) -> dict:
    """
    Fetch a specific metaobject by its GID using GraphQL

    Args:
        client: ShopifyAPIClient instance
        gid: The GID of the metaobject to fetch

    Returns:
        Metaobject data dictionary
    """
    query = """
    query getMetaobject($id: ID!) {
        metaobject(id: $id) {
            id
            type
            displayName
            handle
            fields {
                key
                value
                type
                ... on MetaobjectFieldSingleLineTextField {
                    value
                }
                ... on MetaobjectFieldMultiLineTextField {
                    value
                }
                ... on MetaobjectFieldFileReference {
                    reference {
                        ... on MediaImage {
                            id
                            alt
                            url
                        }
                    }
                }
            }
        }
    }
    """

    variables = {
        "id": gid
    }

    try:
        response = client.graphql_request(query, variables)
        return response.get('data', {}).get('metaobject')
    except ShopifyAPIError as e:
        print(f"❌ Error fetching metaobject {gid}: {e}")
        return None

def search_color_metaobjects(client: ShopifyAPIClient, search_term: str = "green") -> list:
    """
    Search for color metaobjects containing a specific term

    Args:
        client: ShopifyAPIClient instance
        search_term: Term to search for in color names

    Returns:
        List of matching metaobjects
    """
    query = """
    query searchMetaobjects($type: String!, $first: Int!) {
        metaobjects(type: $type, first: $first) {
            edges {
                node {
                    id
                    displayName
                    handle
                    fields {
                        key
                        value
                    }
                }
            }
        }
    }
    """

    # Assuming color metaobjects are of type "color" (common convention)
    variables = {
        "type": "color",
        "first": 250
    }

    try:
        response = client.graphql_request(query, variables)
        metaobjects = response.get('data', {}).get('metaobjects', {}).get('edges', [])

        # Filter for metaobjects containing the search term
        matching_objects = []
        for edge in metaobjects:
            node = edge['node']
            if search_term.lower() in node.get('displayName', '').lower():
                matching_objects.append(node)

        return matching_objects
    except ShopifyAPIError as e:
        print(f"❌ Error searching color metaobjects: {e}")
        return []

def main():
    print("🔍 Color Metaobject Discrepancy Investigation")
    print("=" * 50)

    # Initialize API client
    try:
        client = ShopifyAPIClient()
        print("✅ Shopify API client initialized")

        # Test connection
        shop_info = client.test_connection()
        shop_name = shop_info.get('shop', {}).get('name', 'Unknown')
        print(f"✅ Connected to shop: {shop_name}")

    except Exception as e:
        print(f"❌ Failed to initialize API client: {e}")
        return

    print("\n📋 Investigation Details:")
    print("• Conflicted GID: gid://shopify/Metaobject/127395266709")
    print("• iphone_specs.py maps this to: 'Midnight Green'")
    print("• colors.json maps this to: 'Alpine Green'")
    print("• iPhone 11 Pro Max should have 'Midnight Green' as valid color")

    # Step 1: Fetch the specific metaobject
    print("\n🔍 Step 1: Fetching metaobject with conflicted GID...")
    target_gid = "gid://shopify/Metaobject/127395266709"
    metaobject_data = fetch_metaobject_by_gid(client, target_gid)

    if metaobject_data:
        print("✅ Metaobject found!")
        print(f"   • ID: {metaobject_data.get('id')}")
        print(f"   • Type: {metaobject_data.get('type')}")
        print(f"   • Display Name: {metaobject_data.get('displayName')}")
        print(f"   • Handle: {metaobject_data.get('handle')}")

        # Extract field data
        fields = metaobject_data.get('fields', [])
        if fields:
            print("   • Fields:")
            for field in fields:
                print(f"     - {field.get('key')}: {field.get('value')} (type: {field.get('type')})")

        # Determine the actual color name
        actual_color_name = metaobject_data.get('displayName')
        print(f"\n📝 ACTUAL COLOR NAME: '{actual_color_name}'")

    else:
        print("❌ Metaobject not found or error occurred")
        return

    # Step 2: Search for similar green colors
    print("\n🔍 Step 2: Searching for other 'green' color metaobjects...")
    green_colors = search_color_metaobjects(client, "green")

    if green_colors:
        print(f"✅ Found {len(green_colors)} green color metaobjects:")
        for color in green_colors:
            gid_short = color['id'].split('/')[-1]
            print(f"   • {color.get('displayName')} = gid://shopify/Metaobject/{gid_short}")
            print(f"     Handle: {color.get('handle')}")
    else:
        print("❌ No green color metaobjects found")

    # Step 3: Analysis and recommendations
    print("\n📊 ANALYSIS & RECOMMENDATIONS:")
    print("=" * 50)

    if metaobject_data:
        actual_name = metaobject_data.get('displayName', '').strip()

        if actual_name:
            print(f"✅ The metaobject GID 127395266709 actually represents: '{actual_name}'")

            # Determine which mapping is correct
            if actual_name.lower() == "midnight green":
                print("✅ CORRECT MAPPING: iphone_specs.py is correct")
                print("❌ INCORRECT MAPPING: colors.json should be updated")
                print(f"🔧 RECOMMENDATION: Update colors.json to map 'Alpine Green' to a different GID")

            elif actual_name.lower() == "alpine green":
                print("❌ INCORRECT MAPPING: iphone_specs.py should be updated")
                print("✅ CORRECT MAPPING: colors.json is correct")
                print(f"🔧 RECOMMENDATION: Update iphone_specs.py to map 'Midnight Green' to a different GID")

            else:
                print(f"⚠️  UNEXPECTED: The metaobject is actually '{actual_name}'")
                print("🔧 RECOMMENDATION: Both mappings may need to be updated")

            # Look for the missing color in the search results
            if green_colors:
                print("\n🔍 Checking for the missing color in available green metaobjects:")
                for color in green_colors:
                    color_name = color.get('displayName', '').strip()
                    if actual_name.lower() == "midnight green" and color_name.lower() == "alpine green":
                        gid_short = color['id'].split('/')[-1]
                        print(f"✅ Found Alpine Green: gid://shopify/Metaobject/{gid_short}")
                    elif actual_name.lower() == "alpine green" and color_name.lower() == "midnight green":
                        gid_short = color['id'].split('/')[-1]
                        print(f"✅ Found Midnight Green: gid://shopify/Metaobject/{gid_short}")

    print("\n✅ Investigation complete!")

if __name__ == "__main__":
    main()