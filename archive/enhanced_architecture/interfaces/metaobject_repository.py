"""
Metaobject repository interface for Shopify metaobject data access.

This module defines the contract for metaobject-related data operations,
providing methods for querying, creating, and managing metaobjects.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class MetaobjectRepository(ABC):
    """
    Interface for metaobject data access operations.
    
    This repository defines operations for managing Shopify metaobjects,
    which are used to store structured data like product attributes,
    cosmetic conditions, SIM carriers, etc.
    """
    
    @abstractmethod
    async def get_metaobject_gids(self, metaobject_type: str) -> Dict[str, str]:
        """
        Get metaobject GID mappings for a specific type.
        
        Args:
            metaobject_type: The type of metaobject (e.g., 'cosmetic_condition', 'sim_carrier')
            
        Returns:
            Dictionary mapping metaobject values to their GIDs
            
        Raises:
            MetaobjectRetrievalException: If retrieval fails
        """
        pass
    
    @abstractmethod
    async def create_metaobject(self, metaobject_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new metaobject in Shopify.
        
        Args:
            metaobject_data: Dictionary containing metaobject information
            
        Returns:
            Created metaobject data including GID
            
        Raises:
            MetaobjectCreationException: If creation fails
            ValidationException: If metaobject data is invalid
        """
        pass
    
    @abstractmethod
    async def query_metaobjects(self, query: str) -> List[Dict[str, Any]]:
        """
        Query metaobjects using GraphQL.
        
        Args:
            query: GraphQL query string
            
        Returns:
            List of metaobjects matching the query
            
        Raises:
            GraphQLQueryException: If query fails
        """
        pass
    
    @abstractmethod
    async def get_metaobject_by_gid(self, gid: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific metaobject by its GID.
        
        Args:
            gid: The Global ID of the metaobject
            
        Returns:
            Metaobject data if found, None otherwise
            
        Raises:
            MetaobjectRetrievalException: If retrieval fails
        """
        pass
    
    @abstractmethod
    async def update_metaobject(self, gid: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing metaobject.
        
        Args:
            gid: The Global ID of the metaobject
            updates: Dictionary of fields to update
            
        Returns:
            Updated metaobject data
            
        Raises:
            MetaobjectUpdateException: If update fails
            MetaobjectNotFoundException: If metaobject doesn't exist
        """
        pass
    
    @abstractmethod
    async def get_metaobject_definitions(self) -> List[Dict[str, Any]]:
        """
        Get all metaobject definitions for the store.
        
        Returns:
            List of metaobject definition data
            
        Raises:
            MetaobjectRetrievalException: If retrieval fails
        """
        pass
    
    @abstractmethod
    async def get_metaobjects_by_definition(self, definition_id: str, 
                                          limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all metaobjects for a specific definition.
        
        Args:
            definition_id: The metaobject definition ID
            limit: Maximum number of results
            
        Returns:
            List of metaobjects for the definition
            
        Raises:
            MetaobjectRetrievalException: If retrieval fails
        """
        pass
    
    @abstractmethod
    async def bulk_create_metaobjects(self, metaobjects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create multiple metaobjects in a single operation.
        
        Args:
            metaobjects: List of metaobject data dictionaries
            
        Returns:
            List of created metaobjects
            
        Raises:
            BulkOperationException: If bulk creation fails
        """
        pass
    
    @abstractmethod
    async def find_metaobject_by_value(self, definition_type: str, field_key: str, 
                                     value: str) -> Optional[Dict[str, Any]]:
        """
        Find a metaobject by a specific field value.
        
        Args:
            definition_type: The metaobject definition type
            field_key: The field to search by
            value: The value to search for
            
        Returns:
            Metaobject if found, None otherwise
            
        Raises:
            MetaobjectSearchException: If search fails
        """
        pass