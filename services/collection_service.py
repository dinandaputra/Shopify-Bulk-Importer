"""
Collection service for managing Shopify collections
"""

from typing import Dict, List, Optional, Any
import json
from services.shopify_api import shopify_api, ShopifyAPIError

class CollectionService:
    """
    Service for managing Shopify collections
    """
    
    def __init__(self):
        self.api = shopify_api
        self._collections_cache = None
        
    def get_all_collections(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """Get all Shopify collections
        
        Args:
            force_refresh: Force refresh the cache
            
        Returns:
            List of collection dictionaries
        """
        if self._collections_cache is None or force_refresh:
            try:
                # Fetch all collections via REST API
                response = self.api._make_request('GET', 'custom_collections.json')
                if response and 'custom_collections' in response:
                    self._collections_cache = response['custom_collections']
                else:
                    self._collections_cache = []
                    
            except ShopifyAPIError as e:
                print(f"ERROR: Failed to fetch collections: {str(e)}")
                self._collections_cache = []
        
        return self._collections_cache or []
    
    def get_collection_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Get collection by title
        
        Args:
            title: Collection title to search for
            
        Returns:
            Collection dict if found, None otherwise
        """
        collections = self.get_all_collections()
        for collection in collections:
            if collection.get('title', '').lower() == title.lower():
                return collection
        return None
    
    def get_collection_id_by_title(self, title: str) -> Optional[int]:
        """Get collection ID by title
        
        Args:
            title: Collection title to search for
            
        Returns:
            Collection ID if found, None otherwise
        """
        collection = self.get_collection_by_title(title)
        return collection.get('id') if collection else None
    
    def create_collection_if_not_exists(self, title: str, description: str = "") -> Dict[str, Any]:
        """Create collection if it doesn't exist
        
        Args:
            title: Collection title
            description: Collection description
            
        Returns:
            Dictionary with creation result
        """
        try:
            # Check if collection already exists
            existing_collection = self.get_collection_by_title(title)
            if existing_collection:
                return {
                    'success': True,
                    'collection_id': existing_collection['id'],
                    'title': title,
                    'existed': True,
                    'message': f'Collection "{title}" already exists'
                }
            
            # Create new collection
            collection_data = {
                'custom_collection': {
                    'title': title,
                    'body_html': description,
                    'collection_type': 'manual'
                }
            }
            
            response = self.api._make_request('POST', 'custom_collections.json', data=collection_data)
            
            if response and 'custom_collection' in response:
                created_collection = response['custom_collection']
                
                # Clear cache to force refresh
                self._collections_cache = None
                
                return {
                    'success': True,
                    'collection_id': created_collection['id'],
                    'title': title,
                    'existed': False,
                    'message': f'Collection "{title}" created successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'Invalid response from Shopify API'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to create collection: {str(e)}'
            }
    
    def add_product_to_collections(self, product_id: int, collection_titles: List[str]) -> Dict[str, Any]:
        """Add product to multiple collections
        
        Args:
            product_id: Shopify product ID
            collection_titles: List of collection titles to add product to
            
        Returns:
            Dictionary with assignment results
        """
        results = {
            'product_id': product_id,
            'total_collections': len(collection_titles),
            'successful': 0,
            'failed': 0,
            'details': []
        }
        
        for title in collection_titles:
            try:
                # Ensure collection exists
                creation_result = self.create_collection_if_not_exists(title)
                
                if not creation_result['success']:
                    results['failed'] += 1
                    results['details'].append({
                        'collection': title,
                        'success': False,
                        'error': creation_result['error']
                    })
                    continue
                
                collection_id = creation_result['collection_id']
                
                # Add product to collection using GraphQL (more reliable)
                success = self._add_product_to_collection_graphql(product_id, collection_id)
                
                if success:
                    results['successful'] += 1
                    results['details'].append({
                        'collection': title,
                        'collection_id': collection_id,
                        'success': True,
                        'message': f'Product added to "{title}" collection'
                    })
                else:
                    results['failed'] += 1
                    results['details'].append({
                        'collection': title,
                        'collection_id': collection_id,
                        'success': False,
                        'error': 'Failed to add product to collection'
                    })
                    
            except Exception as e:
                results['failed'] += 1
                results['details'].append({
                    'collection': title,
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def _add_product_to_collection_graphql(self, product_id: int, collection_id: int) -> bool:
        """Add product to collection using GraphQL
        
        Args:
            product_id: Shopify product ID
            collection_id: Shopify collection ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            mutation = """
            mutation collectionAddProducts($id: ID!, $productIds: [ID!]!) {
                collectionAddProducts(id: $id, productIds: $productIds) {
                    collection {
                        id
                        title
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
            """
            
            variables = {
                'id': f"gid://shopify/Collection/{collection_id}",
                'productIds': [f"gid://shopify/Product/{product_id}"]
            }
            
            response = self.api.graphql_request(mutation, variables)
            
            if response and response.get('data') and response['data'].get('collectionAddProducts'):
                result = response['data']['collectionAddProducts']
                
                # Check for errors
                if result.get('userErrors') and len(result['userErrors']) > 0:
                    print(f"WARNING: Collection assignment errors: {result['userErrors']}")
                    return False
                
                return True
            else:
                print(f"ERROR: Invalid GraphQL response for collection assignment: {response}")
                return False
                
        except Exception as e:
            print(f"ERROR: Failed to add product to collection via GraphQL: {str(e)}")
            return False
    
    def get_recommended_collections(self, brand: str) -> List[str]:
        """Get recommended collections for a brand
        
        Args:
            brand: Product brand
            
        Returns:
            List of recommended collection titles
        """
        collections = ['All Products']  # Always include
        
        if brand == 'iPhone':
            collections.append('iPhone')
            # Could add more specific collections like 'iPhone Pro', 'iPhone Mini' based on model
        elif brand in ['Samsung', 'Google', 'OnePlus', 'Xiaomi', 'Oppo', 'Vivo', 'Huawei', 'Sony', 'LG']:
            collections.extend(['Android', brand])
            # Could add more specific collections like 'Samsung Galaxy', 'Google Pixel'
        
        return collections
    
    def validate_collections_exist(self, collection_titles: List[str]) -> Dict[str, bool]:
        """Check which collections exist
        
        Args:
            collection_titles: List of collection titles to check
            
        Returns:
            Dictionary mapping collection title to existence status
        """
        results = {}
        collections = self.get_all_collections()
        existing_titles = {c.get('title', '').lower(): c.get('title', '') for c in collections}
        
        for title in collection_titles:
            title_lower = title.lower()
            results[title] = title_lower in existing_titles
        
        return results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics
        
        Returns:
            Dictionary with collection statistics
        """
        collections = self.get_all_collections()
        
        return {
            'total_collections': len(collections),
            'collection_titles': [c.get('title', 'Untitled') for c in collections],
            'automated_collections': [
                'All Products', 'iPhone', 'Android', 
                'Samsung', 'Google', 'OnePlus', 'Xiaomi'
            ]
        }

# Global service instance
collection_service = CollectionService()