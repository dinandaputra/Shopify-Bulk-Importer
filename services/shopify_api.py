import requests
import json
import time
from typing import Dict, List, Optional, Any, Union
from config.shopify_config import shopify_config

class ShopifyAPIError(Exception):
    """Custom exception for Shopify API errors"""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class ShopifyAPIClient:
    """
    Main Shopify API client for handling all API operations
    """
    
    def __init__(self):
        self.config = shopify_config
        self.session = requests.Session()
        self.session.headers.update(self.config.get_auth_headers())
    
    def _make_request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        """
        Make a request to the Shopify API with error handling and rate limiting
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., 'products.json')
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            ShopifyAPIError: If the request fails
        """
        url = f"{self.config.api_url}/{endpoint}"
        
        try:
            # Rate limiting
            time.sleep(self.config.RATE_LIMIT_DELAY)
            
            # Make the request
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params
            )
            
            # Check for success
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 429:
                # Rate limit exceeded
                raise ShopifyAPIError(
                    "Rate limit exceeded. Please try again later.",
                    status_code=response.status_code
                )
            else:
                # Other error
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('errors', {})
                raise ShopifyAPIError(
                    f"API request failed: {error_msg}",
                    status_code=response.status_code,
                    response=error_data
                )
                
        except requests.exceptions.RequestException as e:
            raise ShopifyAPIError(f"Network error: {str(e)}")
    
    def test_connection(self) -> dict:
        """
        Test the API connection by getting shop information
        
        Returns:
            Shop information dictionary
        """
        return self._make_request('GET', 'shop.json')
    
    def get_product(self, product_id: int) -> dict:
        """Get a single product by ID"""
        return self._make_request('GET', f'products/{product_id}.json')
    
    def get_products(self, limit: int = 50, params: dict = None) -> dict:
        """Get a list of products"""
        query_params = {'limit': limit}
        if params:
            query_params.update(params)
        return self._make_request('GET', 'products.json', params=query_params)
    
    def create_product(self, product_data: dict) -> dict:
        """
        Create a new product
        
        Args:
            product_data: Product data dictionary
            
        Returns:
            Created product data
        """
        return self._make_request('POST', 'products.json', data={'product': product_data})
    
    def update_product(self, product_id: int, product_data: dict) -> dict:
        """Update an existing product"""
        return self._make_request('PUT', f'products/{product_id}.json', data={'product': product_data})
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        try:
            self._make_request('DELETE', f'products/{product_id}.json')
            return True
        except ShopifyAPIError:
            return False
    
    def get_metaobjects(self, type_name: str = None) -> dict:
        """Get metaobjects, optionally filtered by type"""
        params = {'type': type_name} if type_name else {}
        return self._make_request('GET', 'metaobjects.json', params=params)
    
    def get_metaobject(self, metaobject_id: int) -> dict:
        """Get a single metaobject by ID"""
        return self._make_request('GET', f'metaobjects/{metaobject_id}.json')
    
    def create_metaobject(self, metaobject_data: dict) -> dict:
        """Create a new metaobject"""
        return self._make_request('POST', 'metaobjects.json', data={'metaobject': metaobject_data})
    
    def get_metaobject_definitions(self) -> dict:
        """Get all metaobject definitions"""
        return self._make_request('GET', 'metaobject_definitions.json')
    
    def get_product_metafields(self, product_id: int) -> dict:
        """Get metafields for a specific product"""
        return self._make_request('GET', f'products/{product_id}/metafields.json')
    
    def create_product_metafield(self, product_id: int, metafield_data: dict) -> dict:
        """Create a metafield for a product"""
        return self._make_request('POST', f'products/{product_id}/metafields.json', data={'metafield': metafield_data})
    
    def update_product_metafield(self, product_id: int, metafield_id: int, metafield_data: dict) -> dict:
        """Update a product metafield"""
        return self._make_request('PUT', f'products/{product_id}/metafields/{metafield_id}.json', data={'metafield': metafield_data})
    
    def _make_graphql_request(self, query: str, variables: dict = None) -> dict:
        """
        Make a GraphQL request to Shopify API
        
        Args:
            query: GraphQL query or mutation string
            variables: Optional variables for the query
            
        Returns:
            Response data as dictionary
            
        Raises:
            ShopifyAPIError: If the request fails
        """
        url = f"https://{self.config.SHOP_DOMAIN}/admin/api/{self.config.API_VERSION}/graphql.json"
        
        payload = {
            'query': query
        }
        if variables:
            payload['variables'] = variables
            
        try:
            # Rate limiting
            time.sleep(self.config.RATE_LIMIT_DELAY)
            
            # Make the request
            response = self.session.post(
                url=url,
                json=payload,
                headers={
                    'Content-Type': 'application/json',
                    'X-Shopify-Access-Token': self.config.ACCESS_TOKEN
                }
            )
            
            # Check for success
            if response.status_code in [200, 201]:
                result = response.json()
                
                # Check for GraphQL errors
                if 'errors' in result:
                    raise ShopifyAPIError(
                        f"GraphQL errors: {result['errors']}",
                        status_code=response.status_code,
                        response=result
                    )
                
                return result
            else:
                error_data = response.json() if response.text else {}
                raise ShopifyAPIError(
                    f"GraphQL request failed: {error_data}",
                    status_code=response.status_code,
                    response=error_data
                )
                
        except requests.exceptions.RequestException as e:
            raise ShopifyAPIError(f"Network error: {str(e)}")
    
    def graphql_request(self, query: str, variables: dict = None) -> dict:
        """
        Public method for making GraphQL requests
        
        Args:
            query: GraphQL query or mutation string
            variables: Optional variables for the query
            
        Returns:
            Response data as dictionary
        """
        return self._make_graphql_request(query, variables)
    
    def update_product_category(self, product_id: int, taxonomy_category_id: str) -> dict:
        """
        Update a product's category using GraphQL
        
        Args:
            product_id: Shopify product ID
            taxonomy_category_id: Taxonomy category ID (e.g., "gid://shopify/TaxonomyCategory/5173")
            
        Returns:
            Updated product data
        """
        query = """
        mutation UpdateProductCategory($product: ProductUpdateInput!) {
          productUpdate(product: $product) {
            product {
              id
              title
              category {
                id
                name
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
            "product": {
                "id": f"gid://shopify/Product/{product_id}",
                "category": taxonomy_category_id
            }
        }
        
        return self._make_graphql_request(query, variables)
    
    def link_product_option_to_metafield(self, product_id: int, option_name: str, metafield_namespace: str, metafield_key: str, option_value_mappings: dict = None) -> dict:
        """
        Link a product's existing option to a metafield definition using productOptionUpdate
        
        Args:
            product_id: Shopify product ID
            option_name: Name of the option (e.g., "SIM Carriers") 
            metafield_namespace: Namespace of the metafield (e.g., "custom")
            metafield_key: Key of the metafield (e.g., "sim_carriers")
            option_value_mappings: Dict mapping option value names to metaobject GIDs
            
        Returns:
            Updated product data with linked option
        """
        # First, get the product to find the option ID
        product_query = """
        query GetProductOptions($id: ID!) {
          product(id: $id) {
            id
            title
            options {
              id
              name
              position
              values
            }
          }
        }
        """
        
        product_variables = {
            "id": f"gid://shopify/Product/{product_id}"
        }
        
        product_response = self._make_graphql_request(product_query, product_variables)
        
        if not product_response.get('data', {}).get('product'):
            raise ShopifyAPIError("Could not fetch product data for option linking")
        
        # Find the option ID for the specified option name
        product = product_response['data']['product']
        target_option = None
        
        for option in product.get('options', []):
            if option['name'] == option_name:
                target_option = option
                break
        
        if not target_option:
            raise ShopifyAPIError(f"Option '{option_name}' not found in product")
        
        # Now update the option with linkedMetafield using the correct mutation
        update_mutation = """
        mutation ProductOptionUpdate($productId: ID!, $option: OptionUpdateInput!, $optionValuesToUpdate: [OptionValueUpdateInput!]) {
          productOptionUpdate(productId: $productId, option: $option, optionValuesToUpdate: $optionValuesToUpdate) {
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
            }
            userErrors {
              field
              message
              code
            }
          }
        }
        """
        
        # Build option values with their metafield mappings
        option_values_to_update = []
        if option_value_mappings:
            for option_value in target_option.get('values', []):
                metaobject_gid = option_value_mappings.get(option_value)
                if metaobject_gid:
                    # Find the option value ID from the option structure
                    # We need to get the full option values with IDs
                    pass  # Will be handled below
        
        # Get option values with IDs from another query first
        option_values_query = """
        query GetOptionValues($id: ID!) {
          product(id: $id) {
            options {
              id
              name
              optionValues {
                id
                name
              }
            }
          }
        }
        """
        
        option_values_response = self._make_graphql_request(option_values_query, {
            "id": f"gid://shopify/Product/{product_id}"
        })
        
        # Build optionValuesToUpdate array
        if option_value_mappings:
            product_data = option_values_response.get('data', {}).get('product', {})
            for option in product_data.get('options', []):
                if option['id'] == target_option['id']:
                    for option_value in option.get('optionValues', []):
                        value_name = option_value['name']
                        metaobject_gid = option_value_mappings.get(value_name)
                        if metaobject_gid:
                            option_values_to_update.append({
                                "id": option_value['id'],
                                "linkedMetafieldValue": metaobject_gid
                            })
                    break
        
        update_variables = {
            "productId": f"gid://shopify/Product/{product_id}",
            "option": {
                "id": target_option['id'],
                "linkedMetafield": {
                    "namespace": metafield_namespace,
                    "key": metafield_key
                }
            }
        }
        
        # Add option values if we have mappings
        if option_values_to_update:
            update_variables["optionValuesToUpdate"] = option_values_to_update
        
        return self._make_graphql_request(update_mutation, update_variables)
    
    def get_taxonomy_categories(self) -> dict:
        """
        Get available taxonomy categories to find the correct category ID
        
        Returns:
            Available taxonomy categories
        """
        query = """
        query GetTaxonomyCategories {
          taxonomy {
            categories(search: "mobile", first: 50) {
              nodes {
                id
                name
                fullName
                level
                isLeaf
                isRoot
              }
            }
          }
        }
        """
        
        return self._make_graphql_request(query)
    
    def create_product_with_linked_metafields(self, product_data: dict) -> dict:
        """
        Create a product using GraphQL productSet with linked metafields for variants
        
        Args:
            product_data: Product data including linked metafield options
            
        Returns:
            GraphQL response
        """
        mutation = """
        mutation productSet($input: ProductSetInput!) {
          productSet(input: $input) {
            product {
              id
              title
              handle
              status
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
                  price
                  inventoryQuantity
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
        
        variables = {
            "input": product_data
        }
        
        return self._make_graphql_request(mutation, variables)
    
    def assign_metafields_to_variants(self, variant_metafield_data: List[dict]) -> dict:
        """
        Directly assign metafields to variants using metafieldsSet mutation
        
        Args:
            variant_metafield_data: List of dicts with variant_gid, metaobject_gid, namespace, key
            
        Returns:
            GraphQL response
        """
        mutation = """
        mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
          metafieldsSet(metafields: $metafields) {
            metafields {
              id
              key
              namespace
              value
              ownerType
              createdAt
            }
            userErrors {
              field
              message
            }
          }
        }
        """
        
        # Build metafields array for all variants
        metafields_input = []
        for data in variant_metafield_data:
            metafields_input.append({
                "ownerId": data['variant_gid'],
                "namespace": data['namespace'],
                "key": data['key'],
                "value": f'["{data["metaobject_gid"]}"]',  # JSON array format for list type
                "type": "list.metaobject_reference"
            })
        
        variables = {
            "metafields": metafields_input
        }
        
        return self._make_graphql_request(mutation, variables)
    
    
    def get_product(self, product_id: int) -> dict:
        """
        Get product details via REST API
        
        Args:
            product_id: Product ID
            
        Returns:
            Product data
        """
        endpoint = f"products/{product_id}.json"
        response = self._make_request('GET', endpoint)
        return response
    
    def update_variant(self, variant_id: int, variant_data: dict) -> dict:
        """
        Update variant via REST API
        
        Args:
            variant_id: Variant ID
            variant_data: Variant update data
            
        Returns:
            Updated variant data
        """
        endpoint = f"variants/{variant_id}.json"
        payload = {'variant': variant_data}
        response = self._make_request('PUT', endpoint, payload)
        return response
    
    def create_variant_metafield(self, variant_id: int, metafield_data: dict) -> dict:
        """
        Create a metafield for a specific variant via REST API
        
        Args:
            variant_id: Variant ID
            metafield_data: Metafield data (namespace, key, value, type)
            
        Returns:
            Created metafield data
        """
        endpoint = f"variants/{variant_id}/metafields.json"
        payload = {'metafield': metafield_data}
        response = self._make_request('POST', endpoint, payload)
        return response
    
    def update_variants_with_sim_carrier_metafields(self, product_id: int, sim_carrier_mappings: dict, variants_data: List[dict]) -> List[dict]:
        """
        Update existing product variants with SIM carrier metafields
        
        Args:
            product_id: Product ID
            sim_carrier_mappings: Dict mapping carrier names to metaobject GIDs
            variants_data: List of variant data with carrier names
            
        Returns:
            List of metafield creation results
        """
        results = []
        
        try:
            # Get the created product to access variant IDs
            product_response = self.get_product(product_id)
            if not product_response.get('product'):
                return [{'error': 'Could not fetch product for variant metafield update'}]
            
            variants = product_response['product'].get('variants', [])
            
            for i, variant in enumerate(variants):
                if i < len(variants_data):
                    carrier_name = variants_data[i].get('carrier_name')
                    metaobject_gid = sim_carrier_mappings.get(carrier_name)
                    
                    if metaobject_gid:
                        try:
                            metafield_result = self.create_variant_metafield(
                                variant['id'],
                                {
                                    'namespace': 'custom',
                                    'key': 'sim_carriers',  # Match the metafield definition key
                                    'value': metaobject_gid,
                                    'type': 'metaobject_reference'
                                }
                            )
                            
                            results.append({
                                'variant_id': variant['id'],
                                'variant_title': variant.get('title', 'Default Title'),
                                'carrier_name': carrier_name,
                                'metaobject_gid': metaobject_gid,
                                'success': True,
                                'result': metafield_result
                            })
                            
                        except Exception as e:
                            results.append({
                                'variant_id': variant['id'],
                                'variant_title': variant.get('title', 'Default Title'),
                                'carrier_name': carrier_name,
                                'success': False,
                                'error': str(e)
                            })
                    else:
                        results.append({
                            'variant_id': variant['id'],
                            'variant_title': variant.get('title', 'Default Title'),
                            'carrier_name': carrier_name,
                            'success': False,
                            'error': f'No metaobject GID found for carrier: {carrier_name}'
                        })
        
        except Exception as e:
            results.append({
                'error': f'Failed to update variant metafields: {str(e)}'
            })
        
        return results
    
    def discover_publications(self) -> Dict[str, Any]:
        """
        Discover available publications/sales channels for the store
        
        Returns:
            Dictionary with available publications
        """
        query = """
        query getPublications {
          publications(first: 10) {
            nodes {
              id
              name
              supportsFuturePublishing
            }
          }
        }
        """
        
        try:
            response = self._make_graphql_request(query, {})
            
            if response.get('data') and response['data'].get('publications'):
                publications = response['data']['publications']['nodes']
                
                # Create a mapping for easy access
                publication_map = {}
                for pub in publications:
                    pub_name = pub.get('name', '').lower()
                    publication_map[pub_name] = {
                        'id': pub.get('id'),
                        'name': pub.get('name'),
                        'supports_future': pub.get('supportsFuturePublishing', False)
                    }
                
                return {
                    'success': True,
                    'publications': publications,
                    'publication_map': publication_map
                }
            else:
                return {
                    'success': False,
                    'error': 'No publications found in response',
                    'response': response
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def publish_product_to_channel(self, product_id: int, channel_gid: str) -> Dict[str, Any]:
        """
        Publish a product to a sales channel using GraphQL
        
        Args:
            product_id: Shopify product ID
            channel_gid: Sales channel GID (e.g., "gid://shopify/Channel/1")
            
        Returns:
            Dictionary with publication result
        """
        try:
            product_gid = f"gid://shopify/Product/{product_id}"
            
            mutation = """
            mutation publishablePublish($id: ID!, $input: [PublicationInput!]!) {
              publishablePublish(id: $id, input: $input) {
                publishable {
                  publicationCount
                }
                userErrors {
                  field
                  message
                }
              }
            }
            """
            
            variables = {
                "id": product_gid,
                "input": [
                    {
                        "publicationId": channel_gid
                    }
                ]
            }
            
            response = self._make_graphql_request(mutation, variables)
            
            if response.get('data') and response['data'].get('publishablePublish'):
                result = response['data']['publishablePublish']
                
                if result.get('userErrors') and len(result['userErrors']) > 0:
                    return {
                        'success': False,
                        'error': f"GraphQL errors: {result['userErrors']}",
                        'response': response
                    }
                
                return {
                    'success': True,
                    'result': result,
                    'response': response
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
                'error': f'Failed to publish product to channel: {str(e)}'
            }

# Global API client instance
shopify_api = ShopifyAPIClient()