"""
Product repository interface for Shopify product data access.

This module defines the contract for product-related data operations,
extending the base repository with product-specific functionality.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from .base import Repository


class ProductRepository(Repository[Dict[str, Any]], ABC):
    """
    Interface for product data access operations.
    
    This repository extends the base repository interface with
    product-specific operations for creating, updating, and
    managing products in Shopify.
    """
    
    @abstractmethod
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new product in Shopify.
        
        Args:
            product_data: Dictionary containing product information
            
        Returns:
            Created product data including generated ID and fields
            
        Raises:
            ProductCreationException: If product creation fails
            ValidationException: If product data is invalid
        """
        pass
    
    @abstractmethod
    async def update_product(self, product_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing product in Shopify.
        
        Args:
            product_id: The Shopify product ID
            updates: Dictionary of fields to update
            
        Returns:
            Updated product data
            
        Raises:
            ProductUpdateException: If update fails
            ProductNotFoundException: If product doesn't exist
        """
        pass
    
    @abstractmethod
    async def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a product by its Shopify ID.
        
        Args:
            product_id: The Shopify product ID
            
        Returns:
            Product data if found, None otherwise
            
        Raises:
            ProductRetrievalException: If retrieval fails
        """
        pass
    
    @abstractmethod
    async def assign_metafields(self, product_id: str, metafields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assign metafields to a product.
        
        Args:
            product_id: The Shopify product ID
            metafields: List of metafield data to assign
            
        Returns:
            Result of metafield assignment operation
            
        Raises:
            MetafieldAssignmentException: If assignment fails
        """
        pass
    
    @abstractmethod
    async def assign_variant_metafields(self, variant_metafields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assign metafields to product variants.
        
        Args:
            variant_metafields: List of variant metafield data
            
        Returns:
            Result of variant metafield assignment
            
        Raises:
            MetafieldAssignmentException: If assignment fails
        """
        pass
    
    @abstractmethod
    async def get_products_by_collection(self, collection_id: str, 
                                       limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve products belonging to a specific collection.
        
        Args:
            collection_id: The Shopify collection ID
            limit: Maximum number of products to return
            
        Returns:
            List of products in the collection
            
        Raises:
            ProductRetrievalException: If retrieval fails
        """
        pass
    
    @abstractmethod
    async def search_products(self, query: str, filters: Optional[Dict[str, Any]] = None,
                            limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search for products based on query and filters.
        
        Args:
            query: Search query string
            filters: Additional filter criteria
            limit: Maximum number of results
            
        Returns:
            List of products matching the search criteria
            
        Raises:
            ProductSearchException: If search fails
        """
        pass
    
    @abstractmethod
    async def bulk_create_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create multiple products in a single operation.
        
        Args:
            products: List of product data dictionaries
            
        Returns:
            List of created products
            
        Raises:
            BulkOperationException: If bulk creation fails
        """
        pass
    
    @abstractmethod
    async def archive_product(self, product_id: str) -> bool:
        """
        Archive a product (soft delete).
        
        Args:
            product_id: The Shopify product ID
            
        Returns:
            True if archived successfully
            
        Raises:
            ProductArchiveException: If archiving fails
        """
        pass