#!/usr/bin/env python3
"""
Query SIM carrier metaobject IDs from Shopify GraphQL API
Run this once to get the IDs and add them to metaobject_service.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.shopify_api import shopify_api

def get_sim_carrier_metaobjects():
    """Query SIM carrier metaobjects from Shopify"""
    # First, let's see what metaobject definitions exist
    definitions_query = """
    query GetMetaobjectDefinitions {
      metaobjectDefinitions(first: 10) {
        edges {
          node {
            id
            type
            name
          }
        }
      }
    }
    """
    
    print("First, checking what metaobject definitions exist...")
    try:
        result = shopify_api._make_graphql_request(definitions_query)
        if 'data' in result and 'metaobjectDefinitions' in result['data']:
            definitions = result['data']['metaobjectDefinitions']['edges']
            print(f"Found {len(definitions)} metaobject definitions:")
            for edge in definitions:
                node = edge['node']
                print(f"  Type: {node['type']}, Name: {node['name']}, ID: {node['id']}")
        else:
            print("Error getting definitions:", result)
    except Exception as e:
        print(f"Error querying definitions: {e}")
    
    # Now try the SIM carriers query with the correct type
    query = """
    query GetSIMCarrierMetaobjects {
      metaobjects(type: "sim_carrier", first: 10) {
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
    
    try:
        print("Querying SIM carrier metaobjects...")
        result = shopify_api._make_graphql_request(query)
        
        if 'data' in result and 'metaobjects' in result['data']:
            metaobjects = result['data']['metaobjects']['edges']
            
            print(f"Found {len(metaobjects)} SIM carrier metaobjects:")
            print("\n# SIM Carriers metaobject mapping:")
            
            mappings = {}
            for edge in metaobjects:
                node = edge['node']
                metaobject_id = node['id']
                display_name = node['displayName']
                handle = node['handle']
                
                print(f"'{display_name}': '{metaobject_id}',  # handle: {handle}")
                mappings[display_name] = metaobject_id
            
            print(f"\nPython dict format:")
            print("sim_carrier_mappings = {")
            for name, gid in mappings.items():
                print(f"    '{name}': '{gid}',")
            print("}")
            
            return mappings
        else:
            print("No metaobjects found or error in query")
            print("Response:", result)
            return None
            
    except Exception as e:
        print(f"Error querying metaobjects: {e}")
        return None

if __name__ == "__main__":
    get_sim_carrier_metaobjects()