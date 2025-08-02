"""
Repository pattern implementation for Shopify Bulk Importer.

This module provides abstract interfaces and concrete implementations
for data access operations, following the repository pattern to abstract
away infrastructure concerns from the domain layer.
"""

from .interfaces.base import Repository
from .interfaces.product_repository import ProductRepository
from .interfaces.metaobject_repository import MetaobjectRepository

__all__ = [
    'Repository',
    'ProductRepository',
    'MetaobjectRepository',
]