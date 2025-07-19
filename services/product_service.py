from typing import Dict, List, Optional, Any
from models.smartphone import SmartphoneProduct
from services.shopify_api import shopify_api, ShopifyAPIError
from services.metaobject_service import metaobject_service

class ProductService:
    """
    Service for creating and managing products via Shopify API
    """
    
    def __init__(self):
        self.api = shopify_api
        self.metaobject_service = metaobject_service
    
    def create_smartphone_product(self, smartphone: SmartphoneProduct) -> Dict[str, Any]:
        """
        Create a smartphone product in Shopify with all metafields
        
        Args:
            smartphone: SmartphoneProduct instance
            
        Returns:
            Dictionary with creation result
        """
        try:
            # Step 1: Create the basic product
            product_data = self._build_product_data(smartphone)
            
            # Create the product
            response = self.api.create_product(product_data)
            
            if not response.get('product'):
                return {
                    'success': False,
                    'error': 'Failed to create product',
                    'response': response
                }
            
            created_product = response['product']
            product_id = created_product['id']
            
            # Step 2: Set product category using GraphQL
            category_result = None
            try:
                category_result = self.api.update_product_category(
                    product_id, 
                    "gid://shopify/TaxonomyCategory/el-4-8-5"  # Mobile & Smart Phones category
                )
            except Exception as e:
                print(f"Warning: Failed to set product category: {str(e)}")
            
            # Step 3: Add metafields
            metafield_results = self._add_smartphone_metafields(product_id, smartphone)
            
            return {
                'success': True,
                'product_id': product_id,
                'product': created_product,
                'metafields': metafield_results,
                'category_update': category_result
            }
            
        except ShopifyAPIError as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': e.status_code,
                'response': e.response
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def _build_product_data(self, smartphone: SmartphoneProduct) -> Dict[str, Any]:
        """
        Build the product data for Shopify API
        """
        # Build the main product object
        product_data = {
            'title': smartphone.title,
            'body_html': '',
            'vendor': smartphone.vendor,
            'product_type': '',  # Keep product type empty - category will be set via GraphQL
            'tags': smartphone.tags,
            'published': smartphone.published.lower() == 'true',
            'status': 'draft' if smartphone.published.lower() == 'false' else 'active',
            'handle': smartphone.handle,
            'variants': [
                {
                    'title': 'Default Title',
                    'price': str(smartphone.price),
                    'sku': '',
                    'inventory_quantity': smartphone.quantity,
                    'inventory_management': 'shopify',
                    'inventory_policy': 'deny',
                    'barcode': '',
                    'taxable': False,
                    'weight': 0,
                    'weight_unit': 'g'
                }
            ]
        }
        
        return product_data
    
    def _add_smartphone_metafields(self, product_id: int, smartphone: SmartphoneProduct) -> List[Dict]:
        """
        Add metafields to the created product
        """
        results = []
        
        # Note: Category is now set in the product data, not as a metafield
        # This should trigger the metafield forms to appear in Shopify admin
        
        # Get metaobject references for smartphone data
        # Note: Color uses shopify namespace, not custom namespace
        smartphone_data = {
            'sim_carriers': smartphone.sim_carriers,
            'product_rank': smartphone.product_rank,
            'product_inclusions': smartphone.product_inclusions
        }
        
        # Handle metaobject references with correct types
        references = self.metaobject_service.get_smartphone_metafield_references(smartphone_data)
        
        for field_key, metafield_info in references.items():
            try:
                metaobject_id = metafield_info['id']
                field_type = metafield_info['type']
                
                # Format value based on type
                if field_type == 'list.metaobject_reference':
                    field_value = [metaobject_id]  # Wrap in array for list type
                else:
                    field_value = metaobject_id
                
                metafield_result = self.api.create_product_metafield(
                    product_id,
                    {
                        'namespace': 'custom',
                        'key': field_key,
                        'value': field_value,
                        'type': field_type
                    }
                )
                results.append({
                    'field': field_key,
                    'success': True,
                    'result': metafield_result
                })
            except Exception as e:
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
                    else:
                        ram_value = ram_reference['id']
                    
                    ram_result = self.api.create_product_metafield(
                        product_id,
                        {
                            'namespace': 'custom',
                            'key': 'ram_size',
                            'value': ram_value,
                            'type': ram_reference['type']
                        }
                    )
                    results.append({
                        'field': 'ram_size',
                        'success': True,
                        'result': ram_result
                    })
                except Exception as e:
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
                    minus_result = self.api.create_product_metafield(
                        product_id,
                        {
                            'namespace': 'custom',
                            'key': 'minus',
                            'value': minus_reference['id'],
                            'type': minus_reference['type']
                        }
                    )
                    results.append({
                        'field': 'minus',
                        'success': True,
                        'result': minus_result
                    })
                except Exception as e:
                    results.append({
                        'field': 'minus',
                        'success': False,
                        'error': str(e)
                    })
        
        # Handle color (uses shopify namespace)
        if smartphone.color:
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
                    color_result = self.api.create_product_metafield(
                        product_id,
                        {
                            'namespace': 'shopify',
                            'key': 'color-pattern',
                            'value': [color_id],  # List type
                            'type': 'list.metaobject_reference'
                        }
                    )
                    results.append({
                        'field': 'color',
                        'success': True,
                        'result': color_result
                    })
                except Exception as e:
                    results.append({
                        'field': 'color',
                        'success': False,
                        'error': str(e)
                    })
        
        return results
    
    def upload_multiple_products(self, smartphones: List[SmartphoneProduct]) -> Dict[str, Any]:
        """
        Upload multiple smartphone products
        
        Args:
            smartphones: List of SmartphoneProduct instances
            
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

# Global service instance
product_service = ProductService()