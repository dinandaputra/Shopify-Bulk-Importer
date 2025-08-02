"""
Shopify implementation of the product repository interface.

This module provides concrete implementation of product data access
operations using the Shopify API.
"""

from typing import List, Dict, Any, Optional
import logging
from repositories.interfaces.product_repository import ProductRepository
from services.shopify_api import ShopifyAPIClient
from infrastructure.exceptions import (
    ProductCreationException,
    ProductUpdateException,
    ProductNotFoundException,
    ProductRetrievalException,
    MetafieldAssignmentException,
    BulkOperationException,
    ProductArchiveException
)


class ShopifyProductRepository(ProductRepository):
    """
    Shopify implementation of product repository.
    
    This class provides concrete implementation of product data access
    operations using the Shopify REST and GraphQL APIs.
    """
    
    def __init__(self, api_client: ShopifyAPIClient):
        """
        Initialize the repository with a Shopify API client.
        
        Args:
            api_client: The Shopify API client instance
        """
        self._api_client = api_client
        self._logger = logging.getLogger(__name__)
    
    async def create(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new entity (delegates to create_product)."""
        return await self.create_product(entity)
    
    async def get_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity by ID (delegates to get_product)."""
        return await self.get_product(entity_id)
    
    async def update(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Update entity (delegates to update_product)."""
        product_id = entity.get('id')
        if not product_id:
            raise ProductUpdateException("Product ID is required for update")
        return await self.update_product(product_id, entity)
    
    async def delete(self, entity_id: str) -> bool:
        """Delete entity (delegates to archive_product for soft delete)."""
        return await self.archive_product(entity_id)
    
    async def find_all(self, filters: Optional[Dict[str, Any]] = None, 
                      limit: Optional[int] = None, 
                      offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find all products matching filters."""
        try:
            # Convert to sync call as current API is synchronous
            # In future, this can be made truly async
            query = filters.get('query', '') if filters else ''
            return await self.search_products(query, filters, limit)
        except Exception as e:
            raise ProductRetrievalException(f"Failed to find products: {str(e)}")
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count products matching filters."""
        products = await self.find_all(filters)
        return len(products)
    
    async def exists(self, entity_id: str) -> bool:
        """Check if product exists."""
        product = await self.get_product(entity_id)
        return product is not None
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new product in Shopify.
        
        Args:
            product_data: Product information dictionary
            
        Returns:
            Created product data
            
        Raises:
            ProductCreationException: If creation fails
        """
        try:
            # Convert async to sync for now (current API is synchronous)
            result = self._api_client.create_product(product_data)
            if result.get('success'):
                return result['product']
            else:
                raise ProductCreationException(
                    f"Product creation failed: {result.get('error', 'Unknown error')}"
                )
        except Exception as e:
            self._logger.error(f"Product creation error: {str(e)}")
            raise ProductCreationException(f"Failed to create product: {str(e)}")
    
    async def update_product(self, product_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing product.
        
        Args:
            product_id: Shopify product ID
            updates: Fields to update
            
        Returns:
            Updated product data
            
        Raises:
            ProductUpdateException: If update fails
            ProductNotFoundException: If product not found
        """
        try:
            # Check if product exists
            existing = await self.get_product(product_id)
            if not existing:
                raise ProductNotFoundException(f"Product {product_id} not found")
            
            # Perform update (convert to sync call)
            result = self._api_client.update_product(product_id, updates)
            if result.get('success'):
                return result['product']
            else:
                raise ProductUpdateException(
                    f"Product update failed: {result.get('error', 'Unknown error')}"
                )
        except ProductNotFoundException:
            raise
        except Exception as e:
            self._logger.error(f"Product update error: {str(e)}")
            raise ProductUpdateException(f"Failed to update product: {str(e)}")
    
    async def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a product by ID.
        
        Args:
            product_id: Shopify product ID
            
        Returns:
            Product data if found, None otherwise
            
        Raises:
            ProductRetrievalException: If retrieval fails
        """
        try:
            # Convert to sync call
            result = self._api_client.get_product(product_id)
            if result.get('success'):
                return result.get('product')
            return None
        except Exception as e:
            self._logger.error(f"Product retrieval error: {str(e)}")
            raise ProductRetrievalException(f"Failed to retrieve product: {str(e)}")
    
    async def assign_metafields(self, product_id: str, metafields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assign metafields to a product.
        
        Args:
            product_id: Shopify product ID
            metafields: List of metafield data
            
        Returns:
            Assignment result
            
        Raises:
            MetafieldAssignmentException: If assignment fails
        """
        try:
            # Format metafields for product
            formatted_metafields = []
            for metafield in metafields:
                formatted_metafields.append({
                    'ownerId': f'gid://shopify/Product/{product_id}',
                    'namespace': metafield.get('namespace', 'custom'),
                    'key': metafield['key'],
                    'value': metafield['value'],
                    'type': metafield.get('type', 'single_line_text_field')
                })
            
            # Call API to assign metafields
            result = self._api_client.assign_metafields_to_variants(formatted_metafields)
            if not result.get('success'):
                raise MetafieldAssignmentException(
                    f"Metafield assignment failed: {result.get('error', 'Unknown error')}"
                )
            return result
        except Exception as e:
            self._logger.error(f"Metafield assignment error: {str(e)}")
            raise MetafieldAssignmentException(f"Failed to assign metafields: {str(e)}")
    
    async def assign_variant_metafields(self, variant_metafields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assign metafields to variants.
        
        Args:
            variant_metafields: List of variant metafield data
            
        Returns:
            Assignment result
            
        Raises:
            MetafieldAssignmentException: If assignment fails
        """
        try:
            result = self._api_client.assign_metafields_to_variants(variant_metafields)
            if not result.get('success'):
                raise MetafieldAssignmentException(
                    f"Variant metafield assignment failed: {result.get('error', 'Unknown error')}"
                )
            return result
        except Exception as e:
            self._logger.error(f"Variant metafield assignment error: {str(e)}")
            raise MetafieldAssignmentException(f"Failed to assign variant metafields: {str(e)}")
    
    async def get_products_by_collection(self, collection_id: str, 
                                       limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get products in a collection.
        
        Args:
            collection_id: Shopify collection ID
            limit: Maximum products to return
            
        Returns:
            List of products in collection
            
        Raises:
            ProductRetrievalException: If retrieval fails
        """
        try:
            # This would need to be implemented in the API client
            # For now, return empty list
            self._logger.warning(f"get_products_by_collection not fully implemented")
            return []
        except Exception as e:
            self._logger.error(f"Collection products retrieval error: {str(e)}")
            raise ProductRetrievalException(f"Failed to get products by collection: {str(e)}")
    
    async def search_products(self, query: str, filters: Optional[Dict[str, Any]] = None,
                            limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search for products.
        
        Args:
            query: Search query
            filters: Additional filters
            limit: Maximum results
            
        Returns:
            List of matching products
            
        Raises:
            ProductRetrievalException: If search fails
        """
        try:
            # This would need to be implemented in the API client
            # For now, return empty list
            self._logger.warning(f"search_products not fully implemented")
            return []
        except Exception as e:
            self._logger.error(f"Product search error: {str(e)}")
            raise ProductRetrievalException(f"Failed to search products: {str(e)}")
    
    async def bulk_create_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create multiple products.
        
        Args:
            products: List of product data
            
        Returns:
            List of created products
            
        Raises:
            BulkOperationException: If bulk creation fails
        """
        created_products = []
        errors = []
        
        for i, product_data in enumerate(products):
            try:
                created = await self.create_product(product_data)
                created_products.append(created)
            except Exception as e:
                errors.append(f"Product {i}: {str(e)}")
        
        if errors:
            raise BulkOperationException(
                f"Bulk creation partially failed. Created {len(created_products)}/{len(products)}. "
                f"Errors: {'; '.join(errors)}"
            )
        
        return created_products
    
    async def archive_product(self, product_id: str) -> bool:
        """
        Archive a product (soft delete).
        
        Args:
            product_id: Shopify product ID
            
        Returns:
            True if archived successfully
            
        Raises:
            ProductArchiveException: If archiving fails
        """
        try:
            # Set product status to archived
            updates = {'status': 'archived'}
            result = await self.update_product(product_id, updates)
            return result is not None
        except Exception as e:
            self._logger.error(f"Product archive error: {str(e)}")
            raise ProductArchiveException(f"Failed to archive product: {str(e)}")