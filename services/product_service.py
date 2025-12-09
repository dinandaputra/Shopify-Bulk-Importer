from typing import Dict, List, Optional, Any, Tuple
import json
from datetime import datetime
from collections import defaultdict
from models.smartphone import SmartphoneProduct
from models.laptop import LaptopProduct
from services.shopify_api import shopify_api, ShopifyAPIError
from services.metaobject_service import metaobject_service
from services.collection_service import collection_service
from services.laptop_metafield_service import laptop_metafield_service
from config.iphone_specs import IPHONE_COLOR_GIDS
from config.laptop_metafields import LAPTOP_METAFIELDS, ADDITIONAL_METAFIELDS
import re

class ProductService:
    """
    Service for creating and managing products via Shopify API
    """
    
    def __init__(self):
        self.api = shopify_api
        self.metaobject_service = metaobject_service
        self.collection_service = collection_service
    
    def create_smartphone_product(self, smartphone: SmartphoneProduct) -> Dict[str, Any]:
        """
        Create a smartphone product in Shopify with all metafields
        Uses GraphQL productSet for proper variant-metafield linking
        
        Args:
            smartphone: SmartphoneProduct instance
            
        Returns:
            Dictionary with creation result
        """
        # Use the GraphQL method that properly links variants to metafields
        return self.create_smartphone_product_with_linked_metafields(smartphone)
    
    def _build_product_data(self, smartphone: SmartphoneProduct) -> Dict[str, Any]:
        """
        Build the product data for Shopify REST API (deprecated - use GraphQL method)
        This method is kept for backward compatibility but is no longer used
        """
        # This method is deprecated - the create_smartphone_product method now uses GraphQL
        raise NotImplementedError("This method is deprecated. Use create_smartphone_product_with_linked_metafields instead.")
    
    def _add_smartphone_metafields(self, product_id: int, smartphone: SmartphoneProduct) -> List[Dict]:
        """
        Add metafields to the created product
        """
        results = []
        
        # Note: Category is now set in the product data, not as a metafield
        # This should trigger the metafield forms to appear in Shopify admin
        
        # Get metaobject references for smartphone data
        # (SIM carriers are now handled by linked variants, not metafields)
        smartphone_data = {
            'product_rank': smartphone.product_rank,
            'product_inclusions': smartphone.product_inclusions
        }
        
        # Handle metaobject references with correct types
        references = self.metaobject_service.get_smartphone_metafield_references(smartphone_data)
        
        print(f"DEBUG: Input smartphone_data: {smartphone_data}")
        print(f"DEBUG: Generated references: {references}")
        
        for field_key, metafield_info in references.items():
            try:
                metaobject_id = metafield_info['id']
                field_type = metafield_info['type']
                
                # Format value based on type
                if field_type == 'list.metaobject_reference':
                    # For list types, Shopify expects a JSON string representation
                    if isinstance(metaobject_id, list):
                        field_value = metaobject_id
                    else:
                        field_value = [metaobject_id]
                    # Convert to JSON string for Shopify API
                    field_value = json.dumps(field_value)
                else:
                    field_value = metaobject_id
                
                print(f"DEBUG: Creating metafield - key: {field_key}, value: {field_value}, type: {field_type}")
                
                metafield_result = self.api.create_product_metafield(
                    product_id,
                    {
                        'namespace': 'custom',
                        'key': field_key,
                        'value': field_value,
                        'type': field_type
                    }
                )
                
                print(f"DEBUG: Metafield result for {field_key}: {metafield_result}")
                
                results.append({
                    'field': field_key,
                    'success': True,
                    'result': metafield_result
                })
            except Exception as e:
                print(f"ERROR: Failed to create metafield {field_key}: {str(e)}")
                results.append({
                    'field': field_key,
                    'success': False,
                    'error': str(e)
                })
        
        # Handle RAM size
        if smartphone.ram_size:
            ram_reference = self.metaobject_service.get_ram_metafield_reference(smartphone.ram_size)
            if ram_reference:
                try:
                    # Format value based on type
                    if ram_reference['type'] == 'list.metaobject_reference':
                        ram_value = [ram_reference['id']]  # Wrap in array for list type
                        # Convert to JSON string for Shopify API
                        ram_value = json.dumps(ram_value)
                    else:
                        ram_value = ram_reference['id']
                    
                    print(f"DEBUG: Creating RAM metafield - value: {ram_value}, type: {ram_reference['type']}")
                    
                    ram_result = self.api.create_product_metafield(
                        product_id,
                        {
                            'namespace': 'custom',
                            'key': 'ram_size',
                            'value': ram_value,
                            'type': ram_reference['type']
                        }
                    )
                    
                    print(f"DEBUG: RAM metafield result: {ram_result}")
                    
                    results.append({
                        'field': 'ram_size',
                        'success': True,
                        'result': ram_result
                    })
                except Exception as e:
                    print(f"ERROR: Failed to create RAM metafield: {str(e)}")
                    results.append({
                        'field': 'ram_size',
                        'success': False,
                        'error': str(e)
                    })
        
        # Handle minus/issues
        if smartphone.minus:
            minus_reference = self.metaobject_service.get_minus_metafield_reference(smartphone.minus)
            if minus_reference:
                try:
                    print(f"DEBUG: Creating minus metafield - value: {minus_reference['id']}, type: {minus_reference['type']}")
                    
                    minus_result = self.api.create_product_metafield(
                        product_id,
                        {
                            'namespace': 'custom',
                            'key': 'minus',
                            'value': minus_reference['id'],
                            'type': minus_reference['type']
                        }
                    )
                    
                    print(f"DEBUG: Minus metafield result: {minus_result}")
                    
                    results.append({
                        'field': 'minus',
                        'success': True,
                        'result': minus_result
                    })
                except Exception as e:
                    print(f"ERROR: Failed to create minus metafield: {str(e)}")
                    results.append({
                        'field': 'minus',
                        'success': False,
                        'error': str(e)
                    })
        
        # Create the product-level color metafield that Shopify uses as a variant option
        if smartphone.color:
            print(f"DEBUG: Creating color metafield for '{smartphone.color}'")
            color_id = IPHONE_COLOR_GIDS.get(smartphone.color)
            if color_id:
                try:
                    color_result = self.api.create_product_metafield(
                        product_id,
                        {
                            'namespace': 'shopify',
                            'key': 'color-pattern',
                            'value': color_id,
                            'type': 'metaobject_reference'
                        }
                    )
                    print(f"DEBUG: Color metafield result: {color_result}")
                    results.append({
                        'field': 'color',
                        'success': True,
                        'result': color_result
                    })
                except Exception as e:
                    print(f"ERROR: Failed to create color metafield: {str(e)}")
                    results.append({
                        'field': 'color',
                        'success': False,
                        'error': str(e)
                    })
            else:
                print(f"WARNING: No color mapping found for: {smartphone.color}")
                results.append({
                    'field': 'color',
                    'success': False,
                    'error': f'No mapping found for color: {smartphone.color}'
                })
        
        return results
    
    def upload_multiple_products(self, smartphones: List[SmartphoneProduct], product_images: Dict[str, List] = None) -> Dict[str, Any]:
        """
        Upload multiple smartphone products with optional image uploads
        
        Args:
            smartphones: List of SmartphoneProduct instances
            product_images: Dictionary mapping product handles to lists of uploaded files
            
        Returns:
            Dictionary with batch upload results
        """
        results = {
            'total': len(smartphones),
            'successful': 0,
            'failed': 0,
            'products': []
        }
        
        for i, smartphone in enumerate(smartphones):
            print(f"Uploading product {i+1}/{len(smartphones)}: {smartphone.title}")
            
            result = self.create_smartphone_product(smartphone)
            
            if result['success']:
                results['successful'] += 1
                print(f"✅ Successfully created: {smartphone.title}")
                
                # Handle image upload if images exist for this product
                from services.image_service import image_service
                product_id = result.get('product_id')
                has_files = product_images and smartphone.handle in product_images
                has_urls = smartphone.image_urls and len(smartphone.image_urls) > 0
                
                if product_id and (has_files or has_urls):
                    uploaded_files = product_images[smartphone.handle] if has_files else None
                    image_urls = smartphone.image_urls if has_urls else None
                    
                    total_images = (len(uploaded_files) if uploaded_files else 0) + (len(image_urls) if image_urls else 0)
                    print(f"📸 Uploading {total_images} image(s) for {smartphone.title}")
                    
                    image_success = image_service.handle_combined_upload(
                        product_id, 
                        uploaded_files=uploaded_files,
                        image_urls=image_urls
                    )
                    
                    if image_success:
                        result['images_uploaded'] = total_images
                    else:
                        result['image_upload_partial'] = True
                    
            else:
                results['failed'] += 1
                print(f"❌ Failed to create: {smartphone.title} - {result.get('error', 'Unknown error')}")
            
            results['products'].append({
                'smartphone': smartphone,
                'result': result
            })
            
            # Small delay to respect rate limits
            import time
            time.sleep(0.5)
        
        return results
    
    def upload_multiple_laptops(self, laptops: List[LaptopProduct], product_images: Dict[str, List] = None) -> Dict[str, Any]:
        """
        Upload multiple laptop products with optional image uploads
        
        Args:
            laptops: List of LaptopProduct instances
            product_images: Dictionary mapping product handles to lists of uploaded files
            
        Returns:
            Dictionary with batch upload results
        """
        results = {
            'total': len(laptops),
            'successful': 0,
            'failed': 0,
            'success_count': 0,
            'failed_count': 0,
            'products': [],
            'results': []
        }
        
        for i, laptop in enumerate(laptops):
            print(f"Uploading product {i+1}/{len(laptops)}: {laptop.title}")
            
            result = self.create_laptop_product(laptop)
            
            if result['success']:
                results['successful'] += 1
                results['success_count'] += 1
                print(f"✅ Successfully created: {laptop.title}")
                
                # Handle image upload if images exist for this product
                from services.image_service import image_service
                product_id = result.get('product_id')
                has_files = product_images and laptop.handle in product_images
                has_urls = laptop.image_urls and len(laptop.image_urls) > 0
                
                if product_id and (has_files or has_urls):
                    uploaded_files = product_images[laptop.handle] if has_files else None
                    image_urls = laptop.image_urls if has_urls else None
                    
                    total_images = (len(uploaded_files) if uploaded_files else 0) + (len(image_urls) if image_urls else 0)
                    print(f"📸 Uploading {total_images} image(s) for {laptop.title}")
                    
                    image_success = image_service.handle_combined_upload(
                        product_id, 
                        uploaded_files=uploaded_files,
                        image_urls=image_urls
                    )
                    
                    if image_success:
                        result['images_uploaded'] = total_images
                    else:
                        result['image_upload_partial'] = True
                    
            else:
                results['failed'] += 1
                results['failed_count'] += 1
                print(f"❌ Failed to create: {laptop.title} - {result.get('error', 'Unknown error')}")
            
            results['products'].append({
                'laptop': laptop,
                'result': result
            })
            
            # Also add to results array for compatibility with laptop UI
            result_dict = result.copy()
            result_dict['title'] = laptop.title
            results['results'].append(result_dict)
            
            
            # Small delay to respect rate limits
            import time
            time.sleep(0.5)
        
        return results
    
    def create_smartphone_product_with_linked_metafields(self, smartphone: SmartphoneProduct) -> Dict[str, Any]:
        """
        Create a smartphone product using GraphQL with linked metafields for SIM carriers
        
        Args:
            smartphone: SmartphoneProduct instance
            
        Returns:
            Dictionary with creation result
        """
        try:
            # Build GraphQL product data with linked metafields
            product_data = self._build_graphql_product_data(smartphone)
            
            # Create the product using GraphQL
            response = self.api.create_product_with_linked_metafields(product_data)
            
            if response.get('data') and response['data'].get('productSet'):
                result = response['data']['productSet']
                
                if result.get('userErrors') and len(result['userErrors']) > 0:
                    return {
                        'success': False,
                        'error': f"GraphQL errors: {result['userErrors']}",
                        'response': response
                    }
                
                created_product = result.get('product')
                if not created_product:
                    return {
                        'success': False,
                        'error': 'No product returned from GraphQL mutation',
                        'response': response
                    }
                
                # Extract product ID from GraphQL ID
                product_gid = created_product['id']
                product_id = int(product_gid.split('/')[-1])
                
                # Set product category using existing GraphQL method
                category_result = None
                try:
                    category_result = self.api.update_product_category(
                        product_id, 
                        "gid://shopify/TaxonomyCategory/el-4-8-5"  # Mobile & Smart Phones category
                    )
                except Exception as e:
                    print(f"Warning: Failed to set product category: {str(e)}")
                
                # Add remaining metafields (non-variant ones) using REST API
                metafield_results = self._add_non_variant_metafields(product_id, smartphone)
                
                # Link the "Color" option to the shopify.color-pattern metafield (removes "Connect metafield" button)
                color_option_link_result = None
                if smartphone.color:
                    try:
                        # Import the color GIDs mapping
                        from config.iphone_specs import IPHONE_COLOR_GIDS
                        
                        # Validate that the color exists in our mapping
                        if smartphone.color not in IPHONE_COLOR_GIDS:
                            print(f"WARNING: Color '{smartphone.color}' not found in IPHONE_COLOR_GIDS mapping")
                            # Still attempt to link - the option values will be created but not linked to metaobjects
                        
                        color_option_link_result = self.api.link_product_option_to_metafield(
                            product_id,
                            "Color",
                            "shopify",  # Note: shopify namespace, not custom
                            "color-pattern",  # Note: hyphen, not underscore
                            IPHONE_COLOR_GIDS  # Pass the color mappings
                        )
                        print(f"DEBUG: Color option-to-metafield link result: {color_option_link_result}")
                    except Exception as e:
                        print(f"WARNING: Failed to link Color option to metafield: {str(e)}")
                        color_option_link_result = {'error': str(e)}
                
                # Link the "SIM Carriers" option to the metafield (removes "Connect metafield" button)
                option_link_result = None
                if smartphone.sim_carrier_variants and len(smartphone.sim_carrier_variants) > 0:
                    try:
                        # Get SIM carrier mappings for option values
                        sim_carrier_mappings = self.metaobject_service.get_sim_carrier_metaobject_gids()
                        
                        option_link_result = self.api.link_product_option_to_metafield(
                            product_id, 
                            "SIM Carriers", 
                            "custom", 
                            "sim_carriers",
                            sim_carrier_mappings  # Pass the option value mappings
                        )
                        print(f"DEBUG: Option-to-metafield link result: {option_link_result}")
                    except Exception as e:
                        print(f"WARNING: Failed to link option to metafield: {str(e)}")
                        option_link_result = {'error': str(e)}

                # Assign metafields directly to variants (working implementation)
                variant_metafield_result = None
                if smartphone.sim_carrier_variants and len(smartphone.sim_carrier_variants) > 0:
                    try:
                        # Get variant GIDs from the created product
                        variants = created_product.get('variants', {}).get('nodes', [])
                        sim_carrier_mappings = self.metaobject_service.get_sim_carrier_metaobject_gids()
                        
                        # Build variant metafield data
                        variant_metafield_data = []
                        for i, variant in enumerate(variants):
                            if i < len(smartphone.sim_carrier_variants):
                                carrier_name = smartphone.sim_carrier_variants[i]
                                metaobject_gid = sim_carrier_mappings.get(carrier_name)
                                
                                if metaobject_gid:
                                    variant_metafield_data.append({
                                        'variant_gid': variant['id'],  # Already a GID
                                        'metaobject_gid': metaobject_gid,
                                        'namespace': 'custom',
                                        'key': 'sim_carrier'  # Match the variant metafield definition (singular)
                                    })
                        
                        if variant_metafield_data:
                            variant_metafield_result = self.api.assign_metafields_to_variants(variant_metafield_data)
                            print(f"DEBUG: Direct variant metafield assignment result: {variant_metafield_result}")
                        else:
                            print(f"WARNING: No variant metafield data to assign")
                            
                    except Exception as e:
                        print(f"WARNING: Failed to assign variant metafields: {str(e)}")
                        variant_metafield_result = {'error': str(e)}
                
                # Assign product to collections (new feature)
                collection_result = None
                if smartphone.collections:
                    try:
                        collection_result = self.collection_service.add_product_to_collections(
                            product_id, smartphone.collections
                        )
                        print(f"DEBUG: Collection assignment result: {collection_result}")
                        
                        if collection_result['successful'] > 0:
                            print(f"SUCCESS: Added product to {collection_result['successful']} collections")
                        if collection_result['failed'] > 0:
                            print(f"WARNING: Failed to add product to {collection_result['failed']} collections")
                            
                    except Exception as e:
                        print(f"WARNING: Failed to assign collections: {str(e)}")
                        collection_result = {'error': str(e)}
                
                # Assign product to sales channels
                sales_channel_result = None
                if smartphone.sales_channels:
                    try:
                        sales_channel_result = self._assign_to_sales_channels(
                            product_id, smartphone.sales_channels
                        )
                        print(f"DEBUG: Sales channel assignment result: {sales_channel_result}")
                        
                        if sales_channel_result.get('successful', 0) > 0:
                            print(f"SUCCESS: Added product to {sales_channel_result['successful']} sales channels")
                        if sales_channel_result.get('failed', 0) > 0:
                            print(f"WARNING: Failed to add product to {sales_channel_result['failed']} sales channels")
                            
                    except Exception as e:
                        print(f"WARNING: Failed to assign sales channels: {str(e)}")
                        sales_channel_result = {'error': str(e)}
                else:
                    sales_channel_result = {
                        'success': False,
                        'message': 'No sales channels specified'
                    }
                
                return {
                    'success': True,
                    'product_id': product_id,
                    'product': created_product,
                    'metafields': metafield_results,
                    'option_link': option_link_result,
                    'color_option_link': color_option_link_result,
                    'variant_metafields': variant_metafield_result,
                    'category_update': category_result,
                    'collections': collection_result,
                    'sales_channels': sales_channel_result,
                    'graphql_response': response
                }
                
            else:
                return {
                    'success': False,
                    'error': 'Invalid GraphQL response structure',
                    'response': response
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def _build_graphql_product_data(self, smartphone: SmartphoneProduct) -> Dict[str, Any]:
        """
        Build GraphQL product data with linked metafields for SIM carriers
        """
        # Get the primary location ID for inventory
        primary_location_id = self._get_primary_location_id()
        
        sim_carriers = smartphone.sim_carrier_variants or []
        
        # If no SIM carriers selected, create a basic product without options
        if not sim_carriers:
            return self._build_simple_product_data(smartphone)
        
        # Build variant data with linked metafield values
        variants = []
        quantity_per_variant = smartphone.quantity // len(sim_carriers) if len(sim_carriers) > 0 else smartphone.quantity
        remaining_quantity = smartphone.quantity % len(sim_carriers) if len(sim_carriers) > 0 else 0
        
        # Get SIM carrier metaobject GIDs dynamically
        try:
            sim_carrier_mappings = self.metaobject_service.get_sim_carrier_metaobject_gids()
            print(f"DEBUG: Dynamic SIM carrier mappings: {sim_carrier_mappings}")
        except Exception as e:
            print(f"WARNING: Failed to fetch dynamic GIDs, using fallback: {str(e)}")
            # Fallback to hardcoded mappings if dynamic lookup fails
            sim_carrier_mappings = {
                'SIM Free': 'gid://shopify/Metaobject/116965343381',
                'Rakuten Mobile (-)': 'gid://shopify/Metaobject/116971733141',
                'Softbank (-)': 'gid://shopify/Metaobject/116971765909',
                'Docomo (-)': 'gid://shopify/Metaobject/116971798677',
                'AU (-)': 'gid://shopify/Metaobject/116971831445'
            }
        
        for i, carrier in enumerate(sim_carriers):
            # Give extra quantity to first variant if there's remainder
            variant_quantity = quantity_per_variant + (1 if i == 0 and remaining_quantity > 0 else 0)
            
            # Build option values - include color if present
            option_values = []
            
            # Add color option value if product has color
            if smartphone.color:
                option_values.append({
                    'optionName': 'Color',
                    'name': smartphone.color
                })
            
            # Add SIM carrier option value
            option_values.append({
                'optionName': 'SIM Carriers',
                'name': carrier  # This will be matched against displayName in metaobjects
            })
            
            # All variants in this method have option values (since we filtered out no-SIM-carrier case)
            variant = {
                'optionValues': option_values,
                'price': str(smartphone.price),
                'inventoryItem': {
                    'tracked': True
                },
                'inventoryQuantities': [
                    {
                        'locationId': primary_location_id,
                        'name': 'available',
                        'quantity': variant_quantity
                    }
                ],
                'taxable': False
            }
            variants.append(variant)
        
        # Build the main product data using correct Shopify productSet structure
        product_data = {
            'title': smartphone.title,
            'descriptionHtml': '',
            'vendor': smartphone.vendor,
            'productType': '',
            'tags': smartphone.tags.split(', ') if smartphone.tags else [],
            'status': 'DRAFT' if smartphone.published.lower() == 'false' else 'ACTIVE',
            'handle': smartphone.handle,
            'category': 'gid://shopify/TaxonomyCategory/el-4-8-5',  # Mobile & Smart Phones category
            'variants': variants
        }
        
        # Add productOptions with standard values first (will link metafield post-creation)
        # The 2025-07 GraphQL API has conflicts with linkedMetafield + values in productSet
        product_options = []
        
        # Add Color as first option if product has a color
        if smartphone.color:
            product_options.append({
                'name': 'Color',
                'position': 1,
                'values': [{'name': smartphone.color}]
            })
        
        # Add SIM Carriers as second option if applicable
        if sim_carriers and sim_carriers[0] != 'Default Title':
            product_options.append({
                'name': 'SIM Carriers',
                'position': 2 if smartphone.color else 1,
                'values': [{'name': carrier} for carrier in sim_carriers]
            })
        
        if product_options:
            product_data['productOptions'] = product_options
            print(f"DEBUG: Added standard productOptions (linkedMetafield will be added post-creation)")
            print(f"DEBUG: Values: {sim_carriers}")
            print(f"DEBUG: Will link to metafield custom.sim_carriers after product creation")
        
        return product_data
    
    def _build_simple_product_data(self, smartphone: SmartphoneProduct) -> Dict[str, Any]:
        """
        Build simple product data without SIM carrier variants but may have color option
        """
        primary_location_id = self._get_primary_location_id()
        
        # Build variant - if color exists, include option value
        variant_data = {
            'price': str(smartphone.price),
            'inventoryItem': {
                'tracked': True
            },
            'inventoryQuantities': [
                {
                    'locationId': primary_location_id,
                    'name': 'available',
                    'quantity': smartphone.quantity
                }
            ],
            'taxable': False
        }
        
        # Add color option value if present
        if smartphone.color:
            variant_data['optionValues'] = [{
                'optionName': 'Color',
                'name': smartphone.color
            }]
        
        # Build the main product data
        product_data = {
            'title': smartphone.title,
            'descriptionHtml': '',
            'vendor': smartphone.vendor,
            'productType': '',
            'tags': smartphone.tags.split(', ') if smartphone.tags else [],
            'status': 'DRAFT' if smartphone.published.lower() == 'false' else 'ACTIVE',
            'handle': smartphone.handle,
            'variants': [variant_data]
        }
        
        # Add Color as product option if present
        if smartphone.color:
            product_data['productOptions'] = [{
                'name': 'Color',
                'position': 1,
                'values': [{'name': smartphone.color}]
            }]
        
        return product_data
    
    def _add_non_variant_metafields(self, product_id: int, smartphone: SmartphoneProduct) -> List[Dict]:
        """
        Add metafields that are not connected to variants (product_rank, product_inclusions, etc.)
        """
        results = []
        
        # Get metaobject references for non-variant smartphone data 
        # (SIM carriers are now handled by linked variants, not metafields)
        smartphone_data = {
            'product_rank': smartphone.product_rank,
            'product_inclusions': smartphone.product_inclusions
        }
        
        # Handle metaobject references with correct types
        references = self.metaobject_service.get_smartphone_metafield_references(smartphone_data)
        
        print(f"DEBUG: Input smartphone_data (non-variant): {smartphone_data}")
        print(f"DEBUG: Generated references (non-variant): {references}")
        
        for field_key, metafield_info in references.items():
            try:
                metaobject_id = metafield_info['id']
                field_type = metafield_info['type']
                
                # Format value based on type
                if field_type == 'list.metaobject_reference':
                    if isinstance(metaobject_id, list):
                        field_value = metaobject_id
                    else:
                        field_value = [metaobject_id]
                    field_value = json.dumps(field_value)
                else:
                    field_value = metaobject_id
                
                print(f"DEBUG: Creating non-variant metafield - key: {field_key}, value: {field_value}, type: {field_type}")
                
                metafield_result = self.api.create_product_metafield(
                    product_id,
                    {
                        'namespace': 'custom',
                        'key': field_key,
                        'value': field_value,
                        'type': field_type
                    }
                )
                
                print(f"DEBUG: Non-variant metafield result for {field_key}: {metafield_result}")
                
                results.append({
                    'field': field_key,
                    'success': True,
                    'result': metafield_result
                })
            except Exception as e:
                print(f"ERROR: Failed to create non-variant metafield {field_key}: {str(e)}")
                results.append({
                    'field': field_key,
                    'success': False,
                    'error': str(e)
                })
        
        # Handle RAM size
        if smartphone.ram_size:
            ram_reference = self.metaobject_service.get_ram_metafield_reference(smartphone.ram_size)
            if ram_reference:
                try:
                    if ram_reference['type'] == 'list.metaobject_reference':
                        ram_value = [ram_reference['id']]
                        ram_value = json.dumps(ram_value)
                    else:
                        ram_value = ram_reference['id']
                    
                    print(f"DEBUG: Creating RAM metafield - value: {ram_value}, type: {ram_reference['type']}")
                    
                    ram_result = self.api.create_product_metafield(
                        product_id,
                        {
                            'namespace': 'custom',
                            'key': 'ram_size',
                            'value': ram_value,
                            'type': ram_reference['type']
                        }
                    )
                    
                    print(f"DEBUG: RAM metafield result: {ram_result}")
                    
                    results.append({
                        'field': 'ram_size',
                        'success': True,
                        'result': ram_result
                    })
                except Exception as e:
                    print(f"ERROR: Failed to create RAM metafield: {str(e)}")
                    results.append({
                        'field': 'ram_size',
                        'success': False,
                        'error': str(e)
                    })
        
        # Handle minus/issues
        if smartphone.minus:
            minus_reference = self.metaobject_service.get_minus_metafield_reference(smartphone.minus)
            if minus_reference:
                try:
                    print(f"DEBUG: Creating minus metafield - value: {minus_reference['id']}, type: {minus_reference['type']}")
                    
                    minus_result = self.api.create_product_metafield(
                        product_id,
                        {
                            'namespace': 'custom',
                            'key': 'minus',
                            'value': minus_reference['id'],
                            'type': minus_reference['type']
                        }
                    )
                    
                    print(f"DEBUG: Minus metafield result: {minus_result}")
                    
                    results.append({
                        'field': 'minus',
                        'success': True,
                        'result': minus_result
                    })
                except Exception as e:
                    print(f"ERROR: Failed to create minus metafield: {str(e)}")
                    results.append({
                        'field': 'minus',
                        'success': False,
                        'error': str(e)
                    })
        
        return results
    
    def _update_variant_inventory(self, product_id: int, smartphone: SmartphoneProduct) -> List[Dict]:
        """
        Update inventory for product variants after creation using REST API
        """
        results = []
        
        try:
            # Get the created product to find variant IDs
            product_response = self.api.get_product(product_id)
            if not product_response.get('product'):
                return [{'error': 'Could not fetch created product for inventory update'}]
            
            variants = product_response['product'].get('variants', [])
            sim_carriers = smartphone.sim_carrier_variants or ['Default Title']
            
            # Calculate inventory per variant
            quantity_per_variant = smartphone.quantity // len(sim_carriers)
            remaining_quantity = smartphone.quantity % len(sim_carriers)
            
            for i, variant in enumerate(variants):
                # Give extra quantity to first variant if there's remainder
                variant_quantity = quantity_per_variant + (1 if i == 0 and remaining_quantity > 0 else 0)
                
                try:
                    # Update variant with inventory settings
                    variant_update = {
                        'inventory_quantity': variant_quantity,
                        'inventory_management': 'shopify',
                        'inventory_policy': 'deny'
                    }
                    
                    update_response = self.api.update_variant(variant['id'], variant_update)
                    
                    results.append({
                        'variant_id': variant['id'],
                        'variant_title': variant.get('title', 'Default Title'),
                        'inventory_set': variant_quantity,
                        'success': True,
                        'response': update_response
                    })
                    
                except Exception as e:
                    results.append({
                        'variant_id': variant['id'],
                        'variant_title': variant.get('title', 'Default Title'),
                        'success': False,
                        'error': str(e)
                    })
            
        except Exception as e:
            results.append({
                'error': f'Failed to update variant inventory: {str(e)}'
            })
        
        return results
    
    def _get_primary_location_id(self) -> str:
        """
        Get the primary location ID for inventory tracking
        """
        try:
            # Get shop info which includes primary_location_id
            response = self.api.test_connection()
            if response and response.get('shop', {}).get('primary_location_id'):
                location_id = response['shop']['primary_location_id']
                return f"gid://shopify/Location/{location_id}"
        except:
            pass
        
        # Fallback - use the known primary location for this store
        return "gid://shopify/Location/79305801877"
    
    def create_laptop_product(self, laptop: LaptopProduct) -> Dict[str, Any]:
        """
        Create a laptop product in Shopify with all metafields
        
        Args:
            laptop: LaptopProduct instance
            
        Returns:
            Dictionary with creation result
        """
        try:
            # Build laptop product data
            product_data = self._build_laptop_product_data(laptop)
            
            # Create the product using basic REST API
            response = self.api.create_product(product_data)
            
            if response.get('product'):
                created_product = response['product']
                product_id = created_product['id']
                
                # Set product category - try multiple laptop category possibilities
                category_result = None
                laptop_category_ids = [
                    "gid://shopify/TaxonomyCategory/el-6-6",    # Laptops (confirmed working)
                ]
                
                for i, category_id in enumerate(laptop_category_ids):
                    try:
                        print(f"DEBUG: Attempting laptop category #{i+1}: {category_id}")
                        
                        category_result = self.api.update_product_category(product_id, category_id)
                        
                        # Check for success (no userErrors)
                        if (category_result.get('data', {}).get('productUpdate', {}).get('userErrors') == [] or 
                            not category_result.get('data', {}).get('productUpdate', {}).get('userErrors')):
                            print(f"SUCCESS: Laptop category set to: {category_id}")
                            break
                        else:
                            errors = category_result['data']['productUpdate']['userErrors']
                            print(f"DEBUG: Category {category_id} failed: {errors}")
                            
                    except Exception as e:
                        print(f"DEBUG: Category {category_id} exception: {str(e)}")
                        continue
                
                if not category_result or category_result.get('error'):
                    print(f"WARNING: All laptop category attempts failed")
                    category_result = {'error': 'All category attempts failed'}
                
                # Add laptop metafields using the dedicated service
                metafield_results = self._add_laptop_metafields_with_service(product_id, laptop)
                
                # Note: Laptops don't use color as a variant option, only as a product metafield
                # Color is handled in _add_laptop_metafields_with_service
                
                # Assign product to collections
                collection_result = None
                if laptop.collections:
                    try:
                        collection_result = self.collection_service.add_product_to_collections(
                            product_id, laptop.collections
                        )
                        print(f"DEBUG: Collection assignment result: {collection_result}")
                        
                        if collection_result['successful'] > 0:
                            print(f"SUCCESS: Added product to {collection_result['successful']} collections")
                        if collection_result['failed'] > 0:
                            print(f"WARNING: Failed to add product to {collection_result['failed']} collections")
                            
                    except Exception as e:
                        print(f"WARNING: Failed to assign collections: {str(e)}")
                        collection_result = {'error': str(e)}
                
                # Assign product to sales channels
                sales_channel_result = None
                if laptop.sales_channels:
                    try:
                        sales_channel_result = self._assign_to_sales_channels(
                            product_id, laptop.sales_channels
                        )
                        print(f"DEBUG: Sales channel assignment result: {sales_channel_result}")
                        
                        if sales_channel_result.get('successful', 0) > 0:
                            print(f"SUCCESS: Added product to {sales_channel_result['successful']} sales channels")
                        if sales_channel_result.get('failed', 0) > 0:
                            print(f"WARNING: Failed to add product to {sales_channel_result['failed']} sales channels")
                            
                    except Exception as e:
                        print(f"WARNING: Failed to assign sales channels: {str(e)}")
                        sales_channel_result = {'error': str(e)}
                
                return {
                    'success': True,
                    'product_id': product_id,
                    'product': created_product,
                    'metafields': metafield_results,
                    'category_update': category_result,
                    'collections': collection_result,
                    'sales_channels': sales_channel_result
                }
                
            else:
                return {
                    'success': False,
                    'error': 'Failed to create laptop product',
                    'response': response
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def _build_laptop_product_data(self, laptop: LaptopProduct) -> Dict[str, Any]:
        """
        Build laptop product data for Shopify REST API
        """
        # Build the main product data
        product_data = {
            'title': laptop.title,
            'body_html': '',
            'vendor': laptop.vendor,
            'product_type': 'Laptop',
            'tags': laptop.tags,
            'published': laptop.published.lower() == 'true',
            'handle': laptop.handle,
            'variants': [
                {
                    'price': str(laptop.price),
                    'inventory_quantity': laptop.quantity,
                    'inventory_management': 'shopify',
                    'inventory_policy': 'deny',
                    'taxable': False
                }
            ]
        }
        
        return product_data
    
    def _add_laptop_metafields_with_service(self, product_id: int, laptop: LaptopProduct) -> Dict[str, Any]:
        """
        Add laptop-specific metafields using actual metaobject GID mappings
        Uses real metaobject GIDs fetched from Shopify store
        """
        try:
            from repositories.metaobject_repository import MetaobjectRepository
            
            print(f"DEBUG: Creating laptop metafields using new repository system")
            
            # Initialize metaobject repository
            metaobject_repo = MetaobjectRepository()
            
            # Convert laptop data to metafield mappings using repository
            laptop_data = {
                'color': laptop.color,
                'cpu': laptop.cpu,
                'ram': laptop.ram,
                'gpu': laptop.integrated_graphics,  # Integrated graphics
                'display': laptop.display,
                'storage': laptop.storage,
                'vga': laptop.gpu,   # Dedicated graphics cards
                'os': laptop.os,
                'keyboard_layout': laptop.keyboard_layout,
                'keyboard_backlight': laptop.keyboard_backlight,
                'product_rank': laptop.rank,  # 09 Rank
                'product_inclusions': laptop.inclusions,  # 08 Kelengkapan
                'minus': laptop.minus  # Minus/Issues
            }
            
            metafield_mappings = self._convert_laptop_data_to_metafields_with_repo(laptop_data, metaobject_repo)
            print(f"DEBUG: Generated {len(metafield_mappings)} metafield mappings")
            
            results = []
            
            # Process each metafield mapping (these are complete metafield data structures)
            for field_key, metafield_data in metafield_mappings.items():
                if not metafield_data or not metafield_data.get('value'):
                    continue
                    
                try:
                    result = self.api.create_product_metafield(product_id, metafield_data)
                    print(f"DEBUG: Created {field_key} metafield: {metafield_data['value']}")
                    results.append({'field': field_key, 'success': True, 'result': result})
                        
                except Exception as e:
                    print(f"ERROR: Failed to create {field_key} metafield: {str(e)}")
                    results.append({'field': field_key, 'success': False, 'error': str(e)})
            
            successful = len([r for r in results if r.get('success')])
            failed = len([r for r in results if not r.get('success') and not r.get('skipped')])
            skipped = len([r for r in results if r.get('skipped')])
            
            print(f"DEBUG: Metafield creation complete - {successful} successful, {failed} failed, {skipped} skipped")
            
            return {
                'success': successful > 0,  # Success if at least one metafield was created
                'created_metafields': results,
                'successful': successful,
                'failed': failed,
                'skipped': skipped,
                'message': f'Created {successful} metafields using new repository system.'
            }
            
        except Exception as e:
            print(f"ERROR: Failed to create laptop metafields: {str(e)}")
            return {
                'success': False,
                'errors': [str(e)],
                'created_metafields': []
            }
    
    def _convert_laptop_data_to_metafields_with_repo(self, laptop_data: Dict[str, str], metaobject_repo) -> Dict[str, Dict]:
        """
        Convert laptop data to metafields using the repository system
        
        Args:
            laptop_data: Dictionary of laptop field data
            metaobject_repo: MetaobjectRepository instance
            
        Returns:
            Dictionary of metafield data structures ready for API
        """
        metafield_mappings = {}
        
        # Map each component to its metafield data
        component_mappings = [
            ('cpu', 'processor', 'custom', '01_processor', 'metaobject_reference'),
            ('ram', None, 'custom', '02_ram', 'single_line_text_field'),
            ('gpu', 'graphics', 'custom', '03_graphics', 'metaobject_reference'),
            ('display', 'display', 'custom', '04_display', 'metaobject_reference'),
            ('storage', 'storage', 'custom', '05_storage', 'metaobject_reference'),
            ('vga', 'vga', 'custom', '06_vga', 'metaobject_reference'),
            ('os', 'os', 'custom', '07_os', 'metaobject_reference'),
            ('keyboard_layout', 'keyboard_layout', 'custom', '10_keyboard_layout', 'metaobject_reference'),
            ('keyboard_backlight', 'keyboard_backlight', 'custom', '11_keyboard_backlight', 'metaobject_reference'),
            ('color', 'color', 'custom', 'color', 'metaobject_reference')
        ]
        
        for field_key, repo_key, namespace, metafield_key, field_type in component_mappings:
            value = laptop_data.get(field_key)
            if not value:
                continue
                
            if field_type == 'metaobject_reference' and repo_key:
                # Get GID from repository
                gid = metaobject_repo.get_gid(repo_key, value)
                if gid:
                    # Special handling for color field - needs JSON array format for laptops
                    if field_key == 'color':
                        metafield_mappings[field_key] = {
                            'namespace': namespace,
                            'key': metafield_key,
                            'value': json.dumps([gid]),
                            'type': 'list.metaobject_reference'
                        }
                    else:
                        metafield_mappings[field_key] = {
                            'namespace': namespace,
                            'key': metafield_key,
                            'value': gid,
                            'type': field_type
                        }
            elif field_type == 'single_line_text_field':
                # Direct text value
                metafield_mappings[field_key] = {
                    'namespace': namespace,
                    'key': metafield_key,
                    'value': value,
                    'type': field_type
                }
        
        return metafield_mappings
    
    def _build_laptop_metafield_data(self, field_name: str, field_value) -> Optional[Dict[str, Any]]:
        """
        Build metafield data structure for laptop fields
        
        Args:
            field_name: Internal field name (e.g., 'product_rank', 'processor')
            field_value: Field value (text or GID or list of GIDs)
            
        Returns:
            Metafield data dictionary for Shopify API
        """
        # Define metafield key mappings
        metafield_keys = {
            'product_rank': '09_rank',
            'product_inclusions': '08_kelengkapan', 
            'minus': '12_minus',
            'ram': '02_ram',
            'processor': '01_processor',
            'graphics': '03_graphics',
            'display': '04_display',
            'storage': '05_storage',
            'vga': '06_vga',
            'operating_system': '07_os',
            'keyboard_layout': '10_keyboard_layout',
            'keyboard_backlight': '11_keyboard_backlight'
        }
        
        key = metafield_keys.get(field_name)
        if not key:
            print(f"WARNING: No metafield key defined for field '{field_name}'")
            return None
        
        # Determine metafield type and value based on field type
        if field_name in ['product_rank', 'minus']:
            # Single metaobject reference
            if isinstance(field_value, str) and field_value.startswith('gid://shopify/Metaobject/'):
                return {
                    'namespace': 'custom',
                    'key': key,
                    'type': 'metaobject_reference',
                    'value': field_value
                }
        elif field_name == 'product_inclusions':
            # List metaobject reference
            if isinstance(field_value, list):
                gids = [gid for gid in field_value if isinstance(gid, str) and gid.startswith('gid://shopify/Metaobject/')]
                if gids:
                    return {
                        'namespace': 'custom',
                        'key': key,
                        'type': 'list.metaobject_reference',
                        'value': json.dumps(gids)  # JSON array format
                    }
        else:
            # Text fields (processor, graphics, display, storage, etc.)
            if isinstance(field_value, str) and field_value.strip():
                return {
                    'namespace': 'custom',
                    'key': key,
                    'type': 'single_line_text_field',
                    'value': field_value.strip()
                }
        
        print(f"DEBUG: Could not build metafield data for {field_name}: {field_value}")
        return None
    
    def _assign_to_sales_channels(self, product_id: int, sales_channels: List[str]) -> Dict[str, Any]:
        """
        Assign product to specific sales channels using GraphQL publications
        
        Args:
            product_id: Shopify product ID
            sales_channels: List of sales channel names (e.g., ['online_store', 'pos', 'shop'])
            
        Returns:
            Dictionary with assignment results
        """
        try:
            # Discover available publications first
            publications_result = self.api.discover_publications()
            
            if not publications_result.get('success'):
                return {
                    'successful': 0,
                    'failed': len(sales_channels),
                    'error': f"Failed to discover publications: {publications_result.get('error')}"
                }
            
            publication_map = publications_result['publication_map']
            print(f"DEBUG: Available publications: {list(publication_map.keys())}")
            
            # Map sales channel input aliases to Shopify publication names (lowercased)
            channel_mapping = {
                'online_store': 'online store',
                'online store': 'online store',
                'online': 'online store',

                'pos': 'point of sale',
                'point of sale': 'point of sale',
                'point_of_sale': 'point of sale',

                'shop': 'shop',

                # Facebook & Instagram aliases
                'facebook': 'facebook & instagram',
                'instagram': 'facebook & instagram',
                'facebook_instagram': 'facebook & instagram',
                'facebook & instagram': 'facebook & instagram',

                # Google & YouTube aliases
                'google': 'google & youtube',
                'youtube': 'google & youtube',
                'google_youtube': 'google & youtube',
                'google & youtube': 'google & youtube',

                # TikTok
                'tiktok': 'tiktok'
            }
            
            results = []
            successful = 0
            failed = 0
            
            for channel in sales_channels:
                # Normalize input: trim, lower, replace underscores/dashes with spaces
                normalized = re.sub(r'[_\-]+', ' ', (channel or '').strip().lower())

                # Try direct mapping
                publication_name = channel_mapping.get(normalized)

                # Fallback heuristics for common inputs
                if not publication_name:
                    if 'facebook' in normalized or 'instagram' in normalized:
                        publication_name = 'facebook & instagram'
                    elif 'google' in normalized or 'youtube' in normalized:
                        publication_name = 'google & youtube'
                    elif 'tiktok' in normalized or 'tik tok' in normalized:
                        publication_name = 'tiktok'
                    else:
                        publication_name = None

                if not publication_name:
                    print(f"WARNING: Unknown sales channel '{channel}', skipping")
                    failed += 1
                    results.append({
                        'channel': channel,
                        'success': False,
                        'error': f'Unknown sales channel: {channel}'
                    })
                    continue

                # Find the publication by name (publication_map keys are lowercased names)
                publication_info = publication_map.get(publication_name)
                if not publication_info:
                    print(f"WARNING: Publication '{publication_name}' not found in store")
                    failed += 1
                    results.append({
                        'channel': channel,
                        'publication_name': publication_name,
                        'success': False,
                        'error': f'Publication not found: {publication_name}'
                    })
                    continue

                publication_id = publication_info['id']

                try:
                    print(f"DEBUG: Publishing to {publication_info['name']} ({publication_id})")
                    
                    # Use GraphQL to publish product to this specific channel
                    result = self.api.publish_product_to_channel(product_id, publication_id)
                    
                    if result.get('success', False):
                        successful += 1
                        results.append({
                            'channel': channel,
                            'publication_name': publication_info['name'],
                            'publication_id': publication_id,
                            'success': True,
                            'message': f'Successfully published to {publication_info["name"]}'
                        })
                        print(f"SUCCESS: Published to {publication_info['name']}")
                    else:
                        failed += 1
                        results.append({
                            'channel': channel,
                            'publication_name': publication_info['name'],
                            'publication_id': publication_id,
                            'success': False,
                            'error': result.get('error', 'Unknown error')
                        })
                        print(f"FAILED: Could not publish to {publication_info['name']}: {result.get('error')}")
                        
                except Exception as e:
                    failed += 1
                    results.append({
                        'channel': channel,
                        'publication_name': publication_name,
                        'success': False,
                        'error': str(e)
                    })
                    print(f"ERROR: Exception publishing to {publication_name}: {str(e)}")
            
            return {
                'successful': successful,
                'failed': failed,
                'results': results
            }
            
        except Exception as e:
            print(f"ERROR: Failed to assign sales channels: {str(e)}")
            return {
                'successful': 0,
                'failed': len(sales_channels),
                'error': str(e)
            }
    
    def convert_laptop_data_to_metafields_enhanced(self, laptop_data: Dict[str, Any]) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, List[str]]]:
        """
        Enhanced conversion with detailed logging of missing entries using MetaobjectRepository
        
        This replaces the legacy function from config/laptop_metafield_mapping_enhanced.py
        and uses the new repository pattern for metaobject GID lookup.
        
        Args:
            laptop_data: Dictionary containing laptop specification data
            
        Returns:
            Tuple[metafields_dict, missing_entries_dict]: 
                - metafields_dict: Successfully mapped metafields
                - missing_entries_dict: Missing entries organized by field
        """
        
        metafields = {}
        missing_entries = defaultdict(list)
        
        # Get metafield configurations
        all_metafields = {**LAPTOP_METAFIELDS, **ADDITIONAL_METAFIELDS}
        
        # Product context for logging
        product_context = {
            'product_title': laptop_data.get('title', 'Unknown'),
            'brand': laptop_data.get('brand', 'Unknown'),
            'model': laptop_data.get('model', 'Unknown'),
            'timestamp': datetime.now().isoformat()
        }
        
        # Try to import and use the MetaobjectRepository
        try:
            from repositories.metaobject_repository import MetaobjectRepository
            metaobject_repo = MetaobjectRepository()
        except ImportError:
            # Repository not available - return error
            return {}, {"error": "MetaobjectRepository not available"}
        
        # Process each laptop data field
        for field_name, value in laptop_data.items():
            if not value:  # Skip empty values
                continue
            
            # Get metafield configuration with special mappings for laptop fields
            metafield_config = None
            
            # Map field names to metafield config keys
            field_to_config_map = {
                'product_rank': 'rank',
                'product_inclusions': 'kelengkapan',
                'minus': 'minus'
            }
            
            # First check if there's a direct mapping
            config_key_to_use = field_to_config_map.get(field_name, field_name)
            
            for config_key, config in all_metafields.items():
                if config_key == config_key_to_use or config_key == field_name or config.key.endswith(field_name):
                    metafield_config = config
                    break
            
            if not metafield_config:
                continue  # Skip fields without metafield definitions
            
            # Handle different metafield types
            if field_name == 'ram':
                # RAM is a text field, not a metaobject reference
                metafields[metafield_config.key] = {
                    'namespace': metafield_config.namespace,
                    'key': metafield_config.key,
                    'type': metafield_config.type.value,
                    'value': str(value)
                }
                
            elif 'metaobject' in metafield_config.type.value:
                # Handle metaobject reference fields using MetaobjectRepository
                
                # Map field names to repository component types (using singular forms as expected by MetaobjectRepository)
                field_to_component_map = {
                    'processor': 'processor',
                    'cpu': 'processor', 
                    'graphics': 'graphics',
                    'gpu': 'graphics',
                    'integrated_graphics': 'graphics',
                    'display': 'display',
                    'storage': 'storage',
                    'vga': 'vga',
                    'os': 'os',
                    'operating_system': 'os',
                    'keyboard_layout': 'keyboard_layout',
                    'keyboard_backlight': 'keyboard_backlight',
                    'color': 'color',
                    'product_rank': 'product_rank_laptop',
                    'product_inclusions': 'product_inclusion_laptop',
                    'inclusions': 'product_inclusion_laptop',
                    'minus': 'minus'
                }
                
                component_type = field_to_component_map.get(field_name)
                if component_type:
                    
                    if field_name == 'product_rank':
                        # Handle single metaobject reference for product_rank
                        gid = metaobject_repo.get_gid(component_type, value)
                        if gid:
                            metafields[metafield_config.key] = {
                                'namespace': metafield_config.namespace,
                                'key': metafield_config.key,
                                'type': 'metaobject_reference',  # Single reference
                                'value': gid
                            }
                        else:
                            missing_entries[field_name].append(value)
                    elif field_name in ['product_inclusions', 'inclusions', 'minus']:
                        # Handle list fields - map each value and create list of GIDs
                        if isinstance(value, list) and value:
                            gids = []
                            for item in value:
                                gid = metaobject_repo.get_gid(component_type, item)
                                if gid:
                                    gids.append(gid)
                                else:
                                    missing_entries[field_name].append(item)
                            
                            if gids:
                                metafields[metafield_config.key] = {
                                    'namespace': metafield_config.namespace,
                                    'key': metaffield_config.key,
                                    'type': 'list.metaobject_reference',  # List type for multi-select
                                    'value': json.dumps(gids)  # JSON encode the list
                                }
                        elif value:  # Single value provided as string
                            gid = metaobject_repo.get_gid(component_type, value)
                            if gid:
                                metafields[metafield_config.key] = {
                                    'namespace': metafield_config.namespace,
                                    'key': metafield_config.key,
                                    'type': 'list.metaobject_reference',
                                    'value': json.dumps([gid])  # Still a list but with single item
                                }
                            else:
                                missing_entries[field_name].append(value)
                    else:
                        # Handle single metaobject reference fields
                        gid = metaobject_repo.get_gid(component_type, value)
                        
                        if gid:
                            # Special handling for color field - needs JSON array format for laptops
                            if field_name == 'color':
                                metafields[metafield_config.key] = {
                                    'namespace': metafield_config.namespace,
                                    'key': metafield_config.key,
                                    'type': 'list.metaobject_reference',  # Override to list type for laptops
                                    'value': json.dumps([gid])
                                }
                            else:
                                metafields[metafield_config.key] = {
                                    'namespace': metafield_config.namespace,
                                    'key': metafield_config.key,
                                    'type': metafield_config.type.value,
                                    'value': gid
                                }
                        else:
                            missing_entries[field_name].append(value)
        
        return metafields, dict(missing_entries)

# Global service instance
product_service = ProductService()
