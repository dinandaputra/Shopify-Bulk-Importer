from typing import Dict, List, Optional, Any
import json
from models.smartphone import SmartphoneProduct
from services.shopify_api import shopify_api, ShopifyAPIError
from services.metaobject_service import metaobject_service
from services.collection_service import collection_service

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
        
        # Handle color (DISABLED - requires metafield definition with key 'color')
        # TODO: Create a metafield definition in Shopify admin with key 'color' for this to work
        if False and smartphone.color:  # Temporarily disabled
            color_mappings = {
                'Pacific Blue': 'gid://shopify/Metaobject/126233608341',
                'Black': 'gid://shopify/Metaobject/108876857493',
                'Blue': 'gid://shopify/Metaobject/111343370389',
                'Silver': 'gid://shopify/Metaobject/118603284629',
                'Gold': 'gid://shopify/Metaobject/111343403157',
                'Space Gray': 'gid://shopify/Metaobject/125795303573',
                'Natural Titanium': 'gid://shopify/Metaobject/118601449621'
            }
            
            color_id = color_mappings.get(smartphone.color)
            if color_id:
                try:
                    # Convert to JSON string for Shopify API
                    color_value = json.dumps([color_id])
                    
                    print(f"DEBUG: Creating color metafield - value: {color_value}, type: list.metaobject_reference")
                    
                    # Try the standard color namespace and key based on error message
                    # Error said: requires metafield definition with key: color
                    # Let's try custom namespace with color key
                    color_result = self.api.create_product_metafield(
                        product_id,
                        {
                            'namespace': 'custom',  # Changed from 'shopify' to 'custom'
                            'key': 'color',
                            'value': color_value,  # JSON string for list type
                            'type': 'list.metaobject_reference'
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
                if product_images and smartphone.handle in product_images:
                    from services.image_service import image_service
                    product_id = result.get('product_id')
                    uploaded_files = product_images[smartphone.handle]
                    
                    if product_id and uploaded_files:
                        print(f"📸 Uploading {len(uploaded_files)} image(s) for {smartphone.title}")
                        image_success = image_service.handle_post_creation_upload(product_id, uploaded_files)
                        if image_success:
                            result['images_uploaded'] = len(uploaded_files)
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
            
            # Build option value - Shopify will auto-link via linkedMetafield
            option_value = {
                'optionName': 'SIM Carriers',
                'name': carrier  # This will be matched against displayName in metaobjects
            }
            
            # All variants in this method have option values (since we filtered out no-SIM-carrier case)
            variant = {
                'optionValues': [option_value],
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
        if sim_carriers and sim_carriers[0] != 'Default Title':
            product_data['productOptions'] = [
                {
                    'name': 'SIM Carriers',
                    'position': 1,
                    'values': [{'name': carrier} for carrier in sim_carriers]
                }
            ]
            print(f"DEBUG: Added standard productOptions (linkedMetafield will be added post-creation)")
            print(f"DEBUG: Values: {sim_carriers}")
            print(f"DEBUG: Will link to metafield custom.sim_carriers after product creation")
        
        return product_data
    
    def _build_simple_product_data(self, smartphone: SmartphoneProduct) -> Dict[str, Any]:
        """
        Build simple product data without variants/options for products without SIM carriers
        """
        primary_location_id = self._get_primary_location_id()
        
        # Single variant for the entire quantity
        variant = {
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
        
        # Build the main product data
        product_data = {
            'title': smartphone.title,
            'descriptionHtml': '',
            'vendor': smartphone.vendor,
            'productType': '',
            'tags': smartphone.tags.split(', ') if smartphone.tags else [],
            'status': 'DRAFT' if smartphone.published.lower() == 'false' else 'ACTIVE',
            'handle': smartphone.handle,
            'variants': [variant]
        }
        
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
            
            # Map sales channel names to publication names
            channel_mapping = {
                'online_store': 'online store',
                'pos': 'point of sale', 
                'shop': 'shop'
            }
            
            results = []
            successful = 0
            failed = 0
            
            for channel in sales_channels:
                publication_name = channel_mapping.get(channel.lower())
                if not publication_name:
                    print(f"WARNING: Unknown sales channel '{channel}', skipping")
                    failed += 1
                    results.append({
                        'channel': channel,
                        'success': False,
                        'error': f'Unknown sales channel: {channel}'
                    })
                    continue
                
                # Find the publication by name
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

# Global service instance
product_service = ProductService()