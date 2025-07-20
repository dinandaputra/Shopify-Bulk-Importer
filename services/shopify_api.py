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
    
    def update_product_option_with_metafield(self, product_id: int, option_name: str, option_values: List[str], metafield_definition_id: str) -> dict:
        """
        Update a product's option to connect with a metafield definition using GraphQL
        
        Args:
            product_id: Shopify product ID
            option_name: Name of the option (e.g., "SIM Carriers")
            option_values: List of option values
            metafield_definition_id: GID of the metafield definition to connect to
            
        Returns:
            Updated product data
        """
        query = """
        mutation UpdateProductOption($product: ProductUpdateInput!) {
          productUpdate(product: $product) {
            product {
              id
              title
              options {
                id
                name
                values
                optionValues {
                  id
                  name
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
        
        # Build the options input - Shopify automatically connects when name matches metafield
        options_input = [
            {
                "name": option_name,
                "values": option_values
            }
        ]
        
        variables = {
            "product": {
                "id": f"gid://shopify/Product/{product_id}",
                "options": options_input
            }
        }
        
        return self._make_graphql_request(query, variables)
    
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
    
    def connect_variant_option_to_metafield(self, product_id: int, option_name: str, metafield_namespace: str, metafield_key: str) -> dict:
        """
        Connect a product variant option to an existing metafield definition
        
        Args:
            product_id: Product ID
            option_name: Name of the variant option
            metafield_namespace: Metafield namespace (e.g., 'custom')
            metafield_key: Metafield key (e.g., 'sim_carriers')
            
        Returns:
            API response
        """
        # Use productUpdate to update the entire product with linked metafield options
        mutation = """
        mutation productUpdate($input: ProductInput!) {
          productUpdate(input: $input) {
            product {
              id
              options {
                id
                name
                linkedMetafield {
                  namespace
                  key
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
        
        # First get the current product options
        get_product_query = """
        query getProduct($id: ID!) {
          product(id: $id) {
            options {
              id
              name
              values
            }
          }
        }
        """
        
        product_result = self._make_graphql_request(get_product_query, {
            "id": f"gid://shopify/Product/{product_id}"
        })
        
        if not product_result.get('data', {}).get('product', {}).get('options'):
            return {'error': 'Could not find product options'}
        
        # Build the options array with the linked metafield for the matching option
        options = []
        for option in product_result['data']['product']['options']:
            if option['name'] == option_name:
                # Add linkedMetafield to this option
                options.append({
                    'name': option['name'],
                    'values': option['values'],
                    'linkedMetafield': {
                        'namespace': metafield_namespace,
                        'key': metafield_key
                    }
                })
            else:
                # Keep other options as-is
                options.append({
                    'name': option['name'],
                    'values': option['values']
                })
        
        variables = {
            "input": {
                "id": f"gid://shopify/Product/{product_id}",
                "options": options
            }
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
        endpoint = f"admin/api/{self.config.API_VERSION}/products/{product_id}.json"
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
        endpoint = f"admin/api/{self.config.API_VERSION}/variants/{variant_id}.json"
        payload = {'variant': variant_data}
        response = self._make_request('PUT', endpoint, payload)
        return response

# Global API client instance
shopify_api = ShopifyAPIClient()