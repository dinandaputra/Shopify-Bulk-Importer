#!/usr/bin/env python3
"""
API Testing Script for Shopify Bulk Importer
Keep this file for repeated testing - don't delete after tests
"""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.smartphone import SmartphoneProduct
from services.product_service import product_service

def test_sim_carriers_metafield_connection():
    """Test if SIM Carriers variant option connects to metafield properly"""
    print("=== Testing SIM Carriers Metafield Connection ===")
    
    # Create test smartphone with multiple SIM carrier variants
    test_smartphone = SmartphoneProduct(
        title="Test iPhone 15 - SIM Carriers Test",
        brand="Apple",
        model="iPhone 15",
        vendor="Apple",
        price=120000,
        quantity=4,
        tags="test, api, sim-carriers",
        published="false",  # Keep as draft
        handle=f"test-iphone-15-sim-test-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        color="Black",
        ram_size="8GB",
        sim_carrier_variants=["SIM Free", "Softbank (-)"],  # Test with 2 variants
        product_rank="A",
        product_inclusions=["Full set cable"],
        minus=["No minus"]
    )
    
    print(f"Creating test product: {test_smartphone.title}")
    print(f"SIM Carrier Variants: {test_smartphone.sim_carrier_variants}")
    
    # Create the product
    result = product_service.create_smartphone_product(test_smartphone)
    
    if result['success']:
        product_id = result['product_id']
        print(f"✅ Product created successfully!")
        print(f"Product ID: {product_id}")
        print(f"Shopify Admin URL: https://jufbtk-ut.myshopify.com/admin/products/{product_id}")
        
        # Check variants
        created_product = result['product']
        if 'variants' in created_product:
            print(f"\nVariants created: {len(created_product['variants'])}")
            for i, variant in enumerate(created_product['variants']):
                print(f"  Variant {i+1}: {variant.get('title', 'N/A')} - option1: {variant.get('option1', 'N/A')}")
        
        # Check options
        if 'options' in created_product:
            print(f"\nProduct options:")
            for option in created_product['options']:
                print(f"  Name: {option.get('name')} - Values: {option.get('values')}")
        
        print(f"\nMetafield results:")
        for metafield in result.get('metafields', []):
            print(f"  {metafield['field']}: {'✅' if metafield['success'] else '❌'}")
            if not metafield['success']:
                print(f"    Error: {metafield.get('error')}")
        
        return product_id
    else:
        print(f"❌ Product creation failed: {result.get('error')}")
        return None

def test_single_sim_carrier():
    """Test with single SIM carrier variant"""
    print("\n=== Testing Single SIM Carrier Variant ===")
    
    test_smartphone = SmartphoneProduct(
        title="Test iPhone 14 - Single SIM Test",
        brand="Apple",
        model="iPhone 14",
        vendor="Apple", 
        price=110000,
        quantity=2,
        tags="test, api, single-sim",
        published="false",
        handle=f"test-iphone-14-single-sim-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        color="Blue",
        ram_size="6GB",
        sim_carrier_variants=["Docomo (-)"],  # Test with 1 variant
        product_rank="B",
        product_inclusions=["With box"],
        minus=["Minor scratches"]
    )
    
    print(f"Creating test product: {test_smartphone.title}")
    print(f"SIM Carrier Variants: {test_smartphone.sim_carrier_variants}")
    
    result = product_service.create_smartphone_product(test_smartphone)
    
    if result['success']:
        product_id = result['product_id']
        print(f"✅ Single variant product created!")
        print(f"Product ID: {product_id}")
        print(f"Shopify Admin URL: https://jufbtk-ut.myshopify.com/admin/products/{product_id}")
        return product_id
    else:
        print(f"❌ Single variant creation failed: {result.get('error')}")
        return None

def test_graphql_linked_metafields():
    """Test GraphQL-based product creation with linked metafields"""
    print("\n=== Testing GraphQL Linked Metafields (NEW APPROACH) ===")
    
    test_smartphone = SmartphoneProduct(
        title="Test iPhone 16 - GraphQL Linked Metafields",
        brand="Apple",
        model="iPhone 16",
        vendor="Apple",
        price=150000,
        quantity=6,
        tags="test, api, graphql, linked-metafields",
        published="false",
        handle=f"test-iphone-16-graphql-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        color="Pacific Blue",
        ram_size="8GB",
        sim_carrier_variants=["SIM Free", "Softbank (-)", "Docomo (-)"],  # Test with 3 variants
        product_rank="A",
        product_inclusions=["Full set cable"],
        minus=["No minus"]
    )
    
    print(f"Creating test product with GraphQL: {test_smartphone.title}")
    print(f"SIM Carrier Variants: {test_smartphone.sim_carrier_variants}")
    
    # Create the product using the new GraphQL method
    result = product_service.create_smartphone_product_with_linked_metafields(test_smartphone)
    
    if result['success']:
        product_id = result['product_id']
        print(f"✅ GraphQL product created successfully!")
        print(f"Product ID: {product_id}")
        print(f"Shopify Admin URL: https://jufbtk-ut.myshopify.com/admin/products/{product_id}")
        
        # Check product structure
        created_product = result['product']
        print(f"\nGraphQL Product Structure:")
        print(f"  Title: {created_product.get('title')}")
        print(f"  Status: {created_product.get('status')}")
        
        # Check options with linked metafields
        if 'options' in created_product:
            print(f"\nProduct Options (should be linked to metafields):")
            for option in created_product['options']:
                linked = option.get('linkedMetafield')
                print(f"  Name: {option.get('name')}")
                if linked:
                    print(f"    ✅ Linked to metafield: {linked['namespace']}.{linked['key']}")
                else:
                    print(f"    ❌ Not linked to metafield")
                
                # Check option values
                option_values = option.get('optionValues', [])
                print(f"    Values ({len(option_values)}):")
                for value in option_values:
                    linked_value = value.get('linkedMetafieldValue')
                    print(f"      - {value.get('name')}: {linked_value or 'No linked value'}")
        
        # Check variants
        if 'variants' in created_product and 'nodes' in created_product['variants']:
            variants = created_product['variants']['nodes']
            print(f"\nVariants created: {len(variants)}")
            for i, variant in enumerate(variants):
                print(f"  Variant {i+1}: {variant.get('title')}")
                selected_options = variant.get('selectedOptions', [])
                for option in selected_options:
                    print(f"    {option.get('name')}: {option.get('value')}")
        
        # Check metafield results
        print(f"\nNon-variant metafield results:")
        for metafield in result.get('metafields', []):
            print(f"  {metafield['field']}: {'✅' if metafield['success'] else '❌'}")
            if not metafield['success']:
                print(f"    Error: {metafield.get('error')}")
        
        return product_id
    else:
        print(f"❌ GraphQL product creation failed: {result.get('error')}")
        if 'response' in result:
            print(f"Response: {result['response']}")
        return None

if __name__ == "__main__":
    print("Starting API tests for SIM Carriers metafield connection...")
    
    # Test 1: Multiple SIM carriers (OLD REST API approach)
    product_id_1 = test_sim_carriers_metafield_connection()
    
    # Test 2: Single SIM carrier (OLD REST API approach)
    product_id_2 = test_single_sim_carrier()
    
    # Test 3: GraphQL with linked metafields (NEW approach)
    product_id_3 = test_graphql_linked_metafields()
    
    print(f"\n=== Test Summary ===")
    print(f"Multi-variant REST test: {'✅' if product_id_1 else '❌'}")
    print(f"Single-variant REST test: {'✅' if product_id_2 else '❌'}")
    print(f"GraphQL linked metafields test: {'✅' if product_id_3 else '❌'}")
    
    if product_id_1 or product_id_2 or product_id_3:
        print(f"\n📋 Next Steps:")
        print(f"1. Check the products in Shopify admin")
        print(f"2. Compare REST vs GraphQL approaches")
        print(f"3. Verify GraphQL product shows dropdown instead of 'add another value'")
        print(f"4. Confirm variant-metafield synchronization in GraphQL product")