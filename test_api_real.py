#!/usr/bin/env python3
"""
Test the fixed SIM carrier implementation with real Shopify API calls
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.smartphone import SmartphoneProduct
from services.product_service import product_service
from services.shopify_api import shopify_api

def test_api_connection():
    """Test API connection first"""
    print("Testing Shopify API connection...")
    try:
        shop_info = shopify_api.test_connection()
        if shop_info and shop_info.get('shop'):
            print(f"✅ Connected to: {shop_info['shop']['name']}")
            print(f"Domain: {shop_info['shop']['domain']}")
            return True
        else:
            print("❌ Failed to connect to Shopify")
            return False
    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False

def test_create_product_with_sim_carriers():
    """Test creating a product with SIM carrier variants via API"""
    
    # Create test product data
    smartphone_data = {
        'title': 'API Test iPhone 14 - SIM Carrier Fix',
        'brand': 'Apple',
        'model': 'iPhone 14',
        'storage': '128GB',
        'price': 89000,
        'quantity': 6,
        'handle': 'api-test-iphone-basic-inventory-test',
        'tags': 'API test, iPhone, SIM carrier fix',
        'published': 'false',  # Keep as draft for testing
        'sim_carrier_variants': ['SIM Free', 'Docomo (-)'],  # Test 2 variants
        'product_rank': 'Rank A',
        'product_inclusions': ['Original box', 'Lightning cable'],
        'ram_size': '6GB',
        'minus': ['Minor scratches on back']
    }
    
    print("\n" + "="*60)
    print("TESTING: Creating Product with SIM Carrier Variants")
    print("="*60)
    
    print(f"Product: {smartphone_data['title']}")
    print(f"SIM Carriers: {smartphone_data['sim_carrier_variants']}")
    print(f"Total Quantity: {smartphone_data['quantity']} (2 per variant)")
    print(f"Price: ¥{smartphone_data['price']:,}")
    
    try:
        # Create smartphone instance
        smartphone = SmartphoneProduct(**smartphone_data)
        print(f"\n✅ Smartphone model validation passed")
        
        # Create the product via API
        print(f"\n🚀 Creating product via Shopify API...")
        result = product_service.create_smartphone_product(smartphone)
        
        if result['success']:
            print(f"\n✅ SUCCESS: Product created!")
            print(f"Product ID: {result['product_id']}")
            
            # Extract and display product info
            product = result['product']
            print(f"\nProduct Details:")
            print(f"  Title: {product['title']}")
            print(f"  Handle: {product['handle']}")
            print(f"  Status: {product['status']}")
            
            # Check product options (linked metafield)
            if product.get('options'):
                print(f"\n✅ Product Options:")
                for option in product['options']:
                    linked = option.get('linkedMetafield')
                    print(f"  - {option['name']}")
                    if linked:
                        print(f"    ✅ Linked to metafield: {linked['namespace']}.{linked['key']}")
                        
                        # Check option values with linked metaobjects
                        if option.get('optionValues'):
                            print(f"    Option Values:")
                            for value in option['optionValues']:
                                linked_value = value.get('linkedMetafieldValue')
                                print(f"      - {value['name']}: {linked_value or 'No linked value'}")
                    else:
                        print(f"    ❌ Not linked to metafield")
            else:
                print(f"\n❌ No product options found")
            
            # Check variants
            if product.get('variants', {}).get('nodes'):
                print(f"\n✅ Variants ({len(product['variants']['nodes'])}):")
                total_inventory = 0
                for i, variant in enumerate(product['variants']['nodes'], 1):
                    inventory = variant.get('inventoryQuantity', 0)
                    total_inventory += inventory
                    print(f"  {i}. {variant['title']}")
                    print(f"     Price: ¥{variant['price']}")
                    print(f"     Inventory: {inventory}")
                    
                    # Check selected options (should show SIM carrier)
                    if variant.get('selectedOptions'):
                        for option in variant['selectedOptions']:
                            print(f"     {option['name']}: {option['value']}")
                
                print(f"\nTotal inventory: {total_inventory} (expected: {smartphone_data['quantity']})")
                if total_inventory == smartphone_data['quantity']:
                    print("✅ Inventory distribution correct")
                else:
                    print("❌ Inventory distribution incorrect")
            else:
                print(f"\n❌ No variants found")
            
            # Check metafields created
            if result.get('metafields'):
                print(f"\n✅ Metafields Created:")
                for metafield in result['metafields']:
                    if metafield['success']:
                        print(f"  ✅ {metafield['field']}")
                    else:
                        print(f"  ❌ {metafield['field']}: {metafield['error']}")
            
            # Check inventory updates
            if result.get('inventory_updates'):
                print(f"\n📦 Inventory Updates:")
                for inventory in result['inventory_updates']:
                    if inventory.get('success'):
                        print(f"  ✅ {inventory['variant_title']}: {inventory['inventory_set']} units")
                    else:
                        print(f"  ❌ {inventory.get('variant_title', 'Unknown')}: {inventory.get('error', 'Unknown error')}")
            
            # Show admin URL
            print(f"\n🔗 Shopify Admin URL:")
            print(f"https://jufbtk-ut.myshopify.com/admin/products/{result['product_id']}")
            
            return result['product_id']
            
        else:
            print(f"\n❌ FAILED: {result['error']}")
            if result.get('response'):
                print(f"API Response: {result['response']}")
            return None
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test API connection first
    if test_api_connection():
        # If connection works, test product creation
        product_id = test_create_product_with_sim_carriers()
        
        if product_id:
            print(f"\n" + "="*60)
            print(f"✅ TEST SUCCESSFUL!")
            print(f"Product ID: {product_id}")
            print(f"✅ SIM carrier variants should now be properly linked to metafields")
            print(f"="*60)
        else:
            print(f"\n" + "="*60)
            print(f"❌ TEST FAILED!")
            print(f"❌ Check the error messages above")
            print(f"="*60)
    else:
        print("❌ Cannot proceed without API connection")