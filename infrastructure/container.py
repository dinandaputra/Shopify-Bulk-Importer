"""
Dependency injection container for managing service dependencies.

This module provides a simple but effective dependency injection container
that manages service registration, resolution, and lifecycle.
"""

from typing import TypeVar, Type, Dict, Any, Optional, Callable, Union, List
from abc import ABC, abstractmethod
import inspect
import logging


T = TypeVar('T')


class Container(ABC):
    """
    Abstract dependency injection container interface.
    
    This interface defines the contract that all DI containers must follow.
    """
    
    @abstractmethod
    def register(self, interface: Type[T], implementation: Type[T], singleton: bool = True) -> None:
        """
        Register a service implementation.
        
        Args:
            interface: The interface or abstract class
            implementation: The concrete implementation
            singleton: Whether to create single instance
        """
        pass
    
    @abstractmethod
    def register_factory(self, interface: Type[T], factory: Callable[[], T], singleton: bool = True) -> None:
        """
        Register a factory function.
        
        Args:
            interface: The interface to register
            factory: Factory function that creates instances
            singleton: Whether to cache the created instance
        """
        pass
    
    @abstractmethod
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """
        Register a specific instance.
        
        Args:
            interface: The interface to register
            instance: The instance to use
        """
        pass
    
    @abstractmethod
    def resolve(self, interface: Type[T]) -> T:
        """
        Resolve a service instance.
        
        Args:
            interface: The interface to resolve
            
        Returns:
            Instance of the requested service
            
        Raises:
            ValueError: If no registration found
        """
        pass
    
    @abstractmethod
    def has_registration(self, interface: Type[T]) -> bool:
        """
        Check if an interface has a registration.
        
        Args:
            interface: The interface to check
            
        Returns:
            True if registered
        """
        pass


class SimpleContainer(Container):
    """
    Simple dependency injection container implementation.
    
    This container supports constructor injection, factory functions,
    and singleton management.
    """
    
    def __init__(self):
        """Initialize the container."""
        self._services: Dict[Type, Type] = {}
        self._factories: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}
        self._singleton_flags: Dict[Type, bool] = {}
        self._logger = logging.getLogger(__name__)
    
    def register(self, interface: Type[T], implementation: Type[T], singleton: bool = True) -> None:
        """
        Register a service implementation.
        
        Args:
            interface: The interface or abstract class
            implementation: The concrete implementation
            singleton: Whether to create single instance
        """
        self._logger.debug(f"Registering {implementation.__name__} for {interface.__name__}")
        self._services[interface] = implementation
        self._singleton_flags[interface] = singleton
    
    def register_factory(self, interface: Type[T], factory: Callable[[], T], singleton: bool = True) -> None:
        """
        Register a factory function.
        
        Args:
            interface: The interface to register
            factory: Factory function that creates instances
            singleton: Whether to cache the created instance
        """
        self._logger.debug(f"Registering factory for {interface.__name__}")
        self._factories[interface] = factory
        self._singleton_flags[interface] = singleton
    
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """
        Register a specific instance.
        
        Args:
            interface: The interface to register
            instance: The instance to use
        """
        self._logger.debug(f"Registering instance for {interface.__name__}")
        self._singletons[interface] = instance
        self._singleton_flags[interface] = True
    
    def resolve(self, interface: Type[T]) -> T:
        """
        Resolve a service instance.
        
        Args:
            interface: The interface to resolve
            
        Returns:
            Instance of the requested service
            
        Raises:
            ValueError: If no registration found
        """
        self._logger.debug(f"Resolving {interface.__name__}")
        
        # Check if already created singleton
        if interface in self._singletons:
            self._logger.debug(f"Returning cached singleton for {interface.__name__}")
            return self._singletons[interface]
        
        # Check factory registration
        if interface in self._factories:
            instance = self._create_from_factory(interface)
            if self._singleton_flags.get(interface, True):
                self._singletons[interface] = instance
            return instance
        
        # Check service registration
        if interface in self._services:
            instance = self._create_from_service(interface)
            if self._singleton_flags.get(interface, True):
                self._singletons[interface] = instance
            return instance
        
        # Try to resolve the concrete type directly
        if not inspect.isabstract(interface):
            try:
                instance = self._create_instance(interface)
                return instance
            except Exception:
                pass
        
        raise ValueError(f"No registration found for {interface.__name__}")
    
    def has_registration(self, interface: Type[T]) -> bool:
        """
        Check if an interface has a registration.
        
        Args:
            interface: The interface to check
            
        Returns:
            True if registered
        """
        return (interface in self._services or 
                interface in self._factories or 
                interface in self._singletons)
    
    def _create_from_factory(self, interface: Type[T]) -> T:
        """
        Create instance using factory function.
        
        Args:
            interface: The interface type
            
        Returns:
            Created instance
        """
        factory = self._factories[interface]
        self._logger.debug(f"Creating {interface.__name__} from factory")
        return factory()
    
    def _create_from_service(self, interface: Type[T]) -> T:
        """
        Create instance from service registration.
        
        Args:
            interface: The interface type
            
        Returns:
            Created instance
        """
        implementation = self._services[interface]
        self._logger.debug(f"Creating {implementation.__name__} for {interface.__name__}")
        return self._create_instance(implementation)
    
    def _create_instance(self, implementation: Type[T]) -> T:
        """
        Create instance with dependency injection.
        
        Args:
            implementation: The implementation class
            
        Returns:
            Created instance with injected dependencies
        """
        # Get constructor signature
        signature = inspect.signature(implementation.__init__)
        params = {}
        
        for param_name, param in signature.parameters.items():
            if param_name == 'self':
                continue
            
            # Get parameter type annotation
            param_type = param.annotation
            
            # Skip if no type annotation
            if param_type == inspect.Parameter.empty:
                # Use default if available
                if param.default != inspect.Parameter.empty:
                    params[param_name] = param.default
                continue
            
            # Try to resolve the parameter
            try:
                if self.has_registration(param_type):
                    params[param_name] = self.resolve(param_type)
                elif param.default != inspect.Parameter.empty:
                    params[param_name] = param.default
                else:
                    # Try to create instance if it's a concrete type
                    if not inspect.isabstract(param_type):
                        params[param_name] = self.resolve(param_type)
            except Exception as e:
                self._logger.warning(
                    f"Failed to resolve {param_name} of type {param_type} "
                    f"for {implementation.__name__}: {str(e)}"
                )
                if param.default == inspect.Parameter.empty:
                    raise
        
        return implementation(**params)
    
    def clear(self) -> None:
        """Clear all registrations and cached instances."""
        self._services.clear()
        self._factories.clear()
        self._singletons.clear()
        self._singleton_flags.clear()
    
    def get_registrations(self) -> Dict[str, List[str]]:
        """
        Get summary of all registrations.
        
        Returns:
            Dictionary with registration information
        """
        return {
            "services": [f"{k.__name__} -> {v.__name__}" for k, v in self._services.items()],
            "factories": [k.__name__ for k in self._factories.keys()],
            "singletons": [k.__name__ for k in self._singletons.keys()]
        }


# Global container instance
_container: Optional[SimpleContainer] = None


def get_container() -> SimpleContainer:
    """
    Get the global container instance.
    
    Returns:
        The global container
    """
    global _container
    if _container is None:
        _container = SimpleContainer()
    return _container


def configure_container() -> SimpleContainer:
    """
    Configure the dependency injection container with all services.
    
    Returns:
        Configured container instance
    """
    container = get_container()
    
    # Clear any existing registrations
    container.clear()
    
    # Register infrastructure services
    from services.shopify_api import ShopifyAPIClient
    container.register_factory(
        ShopifyAPIClient,
        lambda: ShopifyAPIClient(),
        singleton=True
    )
    
    # Register repositories
    from repositories.interfaces.product_repository import ProductRepository
    from repositories.interfaces.metaobject_repository import MetaobjectRepository
    from repositories.shopify_product_repository import ShopifyProductRepository
    from repositories.shopify_metaobject_repository import ShopifyMetaobjectRepository
    
    container.register(ProductRepository, ShopifyProductRepository)
    container.register(MetaobjectRepository, ShopifyMetaobjectRepository)
    
    # Register domain services
    from domain.services.product_domain_service import ProductDomainService
    from domain.services.metafield_domain_service import MetafieldDomainService
    
    container.register_instance(ProductDomainService, ProductDomainService())
    container.register_instance(MetafieldDomainService, MetafieldDomainService())
    
    # Register mappers
    from infrastructure.mappers.product_mapper import ProductMapper
    container.register_instance(ProductMapper, ProductMapper())
    
    return container