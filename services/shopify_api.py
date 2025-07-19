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

# Global API client instance
shopify_api = ShopifyAPIClient()