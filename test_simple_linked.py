#!/usr/bin/env python3
"""
Simple test for metafield-linked variants following Shopify docs exactly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.shopify_api import shopify_api

def test_simple_linked_metafield():
    """Test creating a product with linked metafield exactly as shown in Shopify docs"""
    
    # Simple productSet mutation following the documentation
    mutation = """
    mutation productSet($input: ProductSetInput!) {
      productSet(input: $input) {
        product {
          id
          title
          options {
            id
            name
            linkedMetafield {
              namespace
              key
            }
            optionValues {
              id
              name
              linkedMetafieldValue
            }
          }
          variants(first: 10) {
            nodes {
              id
              title
              selectedOptions {
                name
                value
              }
            }
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    
    # Test data - with minimal variants using linkedMetafieldValue
    variables = {
        "input": {
            "title": "Simple Test Product - Metafield Linked",
            "status": "DRAFT",
            "productOptions": [
                {
                    "name": "SIM Carriers",
                    "linkedMetafield": {
                        "namespace": "custom",
                        "key": "sim_carriers"
                    }
                }
            ],
            "variants": [
                {
                    "optionValues": [
                        {
                            "optionName": "SIM Carriers",
                            "name": "SIM Free",
                            "linkedMetafieldValue": "gid://shopify/Metaobject/116965343381"
                        }
                    ],
                    "price": "100000"
                },
                {
                    "optionValues": [
                        {
                            "optionName": "SIM Carriers", 
                            "name": "Docomo (-)",
                            "linkedMetafieldValue": "gid://shopify/Metaobject/116971798677"
                        }
                    ],
                    "price": "100000"
                }
            ]
        }
    }
    
    print("Testing simple metafield-linked product creation...")
    print("Following Shopify docs exactly...")
    
    try:
        result = shopify_api._make_graphql_request(mutation, variables)
        
        print(f"GraphQL Response: {result}")
        
        if result.get('data') and result['data'].get('productSet'):
            product_set = result['data']['productSet']
            
            if product_set.get('userErrors'):
                print(f"❌ User Errors: {product_set['userErrors']}")
                return None
            
            if product_set.get('product'):
                product = product_set['product']
                print(f"✅ Product created: {product['id']}")
                print(f"Title: {product['title']}")
                
                # Check options
                if product.get('options'):
                    print(f"\nOptions:")
                    for option in product['options']:
                        linked = option.get('linkedMetafield')
                        print(f"  Name: {option['name']}")
                        if linked:
                            print(f"    ✅ Linked to: {linked['namespace']}.{linked['key']}")
                        else:
                            print(f"    ❌ Not linked")
                
                # Extract product ID
                product_gid = product['id']
                product_id = int(product_gid.split('/')[-1])
                print(f"\nProduct ID: {product_id}")
                print(f"Shopify Admin URL: https://jufbtk-ut.myshopify.com/admin/products/{product_id}")
                
                return product_id
            else:
                print("❌ No product returned")
                return None
        else:
            print(f"❌ Invalid response: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def check_metafield_definitions():
    """Check what metafield definitions exist for products"""
    query = """
    query {
      metafieldDefinitions(ownerType: PRODUCT, first: 20) {
        edges {
          node {
            id
            namespace
            key
            name
            type {
              name
            }
            validations {
              name
              value
            }
          }
        }
      }
    }
    """
    
    print("Checking metafield definitions...")
    result = shopify_api._make_graphql_request(query)
    
    if result.get('data', {}).get('metafieldDefinitions'):
        definitions = result['data']['metafieldDefinitions']['edges']
        print(f"Found {len(definitions)} metafield definitions:")
        
        for edge in definitions:
            node = edge['node']
            print(f"  - {node['namespace']}.{node['key']}: {node['name']} (type: {node['type']['name']})")
            if node.get('validations'):
                print(f"    Validations: {node['validations']}")
        
        # Look for sim_carriers specifically
        sim_carriers_def = None
        for edge in definitions:
            node = edge['node']
            if node['namespace'] == 'custom' and node['key'] == 'sim_carriers':
                sim_carriers_def = node
                break
        
        if sim_carriers_def:
            print(f"\n✅ Found SIM Carriers definition:")
            print(f"   ID: {sim_carriers_def['id']}")
            print(f"   Type: {sim_carriers_def['type']['name']}")
            print(f"   Validations: {sim_carriers_def.get('validations', 'None')}")
            return sim_carriers_def
        else:
            print(f"\n❌ No custom.sim_carriers metafield definition found!")
            return None
    else:
        print(f"Error getting metafield definitions: {result}")
        return None

if __name__ == "__main__":
    # First check what metafield definitions exist
    check_metafield_definitions()
    
    print("\n" + "="*50 + "\n")
    
    # Then try to create the product
    test_simple_linked_metafield()