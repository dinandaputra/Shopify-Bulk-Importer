"""
Base repository interface for all repository implementations.

This module defines the generic repository interface that provides
common CRUD operations for all entity types.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any

T = TypeVar('T')


class Repository(Generic[T], ABC):
    """
    Base repository interface providing generic CRUD operations.
    
    This abstract class defines the contract that all repository
    implementations must follow, ensuring consistent data access
    patterns across the application.
    """
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """
        Create a new entity in the data store.
        
        Args:
            entity: The entity to create
            
        Returns:
            The created entity with any generated fields (e.g., ID)
            
        Raises:
            RepositoryException: If creation fails
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Retrieve an entity by its unique identifier.
        
        Args:
            entity_id: The unique identifier of the entity
            
        Returns:
            The entity if found, None otherwise
            
        Raises:
            RepositoryException: If retrieval fails
        """
        pass
    
    @abstractmethod
    async def update(self, entity: T) -> T:
        """
        Update an existing entity in the data store.
        
        Args:
            entity: The entity with updated values
            
        Returns:
            The updated entity
            
        Raises:
            RepositoryException: If update fails
            EntityNotFoundException: If entity doesn't exist
        """
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """
        Delete an entity from the data store.
        
        Args:
            entity_id: The unique identifier of the entity to delete
            
        Returns:
            True if deletion was successful, False otherwise
            
        Raises:
            RepositoryException: If deletion fails
        """
        pass
    
    @abstractmethod
    async def find_all(self, filters: Optional[Dict[str, Any]] = None, 
                      limit: Optional[int] = None, 
                      offset: Optional[int] = None) -> List[T]:
        """
        Find all entities matching the given filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            limit: Maximum number of results to return
            offset: Number of results to skip
            
        Returns:
            List of entities matching the criteria
            
        Raises:
            RepositoryException: If query fails
        """
        pass
    
    @abstractmethod
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count entities matching the given filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            Number of entities matching the criteria
            
        Raises:
            RepositoryException: If count operation fails
        """
        pass
    
    @abstractmethod
    async def exists(self, entity_id: str) -> bool:
        """
        Check if an entity exists in the data store.
        
        Args:
            entity_id: The unique identifier of the entity
            
        Returns:
            True if entity exists, False otherwise
            
        Raises:
            RepositoryException: If existence check fails
        """
        pass