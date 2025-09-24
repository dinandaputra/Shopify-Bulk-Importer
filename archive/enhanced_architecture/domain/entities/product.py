"""
Base product entity for the domain layer.

This module defines the abstract base class for all product types,
containing common attributes and business logic.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Product(ABC):
    """
    Base product entity containing common attributes for all product types.
    
    This abstract class defines the core structure and behavior that all
    product types must implement.
    """
    
    # Core attributes
    title: str
    price: float
    quantity: int
    vendor: str = "MyByte International"
    
    # Optional attributes
    id: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    published: bool = False
    taxable: bool = False
    requires_shipping: bool = True
    inventory_tracked: bool = True
    
    # Collections and channels
    collections: List[str] = field(default_factory=list)
    sales_channels: List[str] = field(default_factory=list)
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # SEO fields
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    
    def __post_init__(self):
        """Validate product after initialization."""
        validation_errors = self.validate_business_rules()
        if validation_errors:
            raise ValueError(f"Product validation failed: {'; '.join(validation_errors)}")
    
    @abstractmethod
    def get_product_type(self) -> str:
        """
        Get the product type identifier.
        
        Returns:
            String identifier for the product type (e.g., 'smartphone', 'laptop')
        """
        pass
    
    @abstractmethod
    def validate_business_rules(self) -> List[str]:
        """
        Validate product-specific business rules.
        
        Returns:
            List of validation error messages, empty if valid
        """
        pass
    
    def validate_common_rules(self) -> List[str]:
        """
        Validate common business rules for all products.
        
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Title validation
        if not self.title or not self.title.strip():
            errors.append("Product title is required")
        elif len(self.title) > 255:
            errors.append("Product title must be 255 characters or less")
        
        # Price validation
        if self.price < 0:
            errors.append("Product price cannot be negative")
        elif self.price > 999999999:
            errors.append("Product price exceeds maximum allowed value")
        
        # Quantity validation
        if self.quantity < 0:
            errors.append("Product quantity cannot be negative")
        
        # Vendor validation
        if not self.vendor or not self.vendor.strip():
            errors.append("Vendor is required")
        
        return errors
    
    def add_tag(self, tag: str) -> None:
        """
        Add a tag to the product.
        
        Args:
            tag: Tag to add
        """
        if tag and tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """
        Remove a tag from the product.
        
        Args:
            tag: Tag to remove
        """
        if tag in self.tags:
            self.tags.remove(tag)
    
    def add_to_collection(self, collection: str) -> None:
        """
        Add product to a collection.
        
        Args:
            collection: Collection name
        """
        if collection and collection not in self.collections:
            self.collections.append(collection)
    
    def remove_from_collection(self, collection: str) -> None:
        """
        Remove product from a collection.
        
        Args:
            collection: Collection name
        """
        if collection in self.collections:
            self.collections.remove(collection)
    
    def publish_to_channel(self, channel: str) -> None:
        """
        Publish product to a sales channel.
        
        Args:
            channel: Sales channel name
        """
        if channel and channel not in self.sales_channels:
            self.sales_channels.append(channel)
    
    def unpublish_from_channel(self, channel: str) -> None:
        """
        Unpublish product from a sales channel.
        
        Args:
            channel: Sales channel name
        """
        if channel in self.sales_channels:
            self.sales_channels.remove(channel)
    
    def calculate_tax(self, tax_rate: float) -> float:
        """
        Calculate tax amount for the product.
        
        Args:
            tax_rate: Tax rate as decimal (e.g., 0.10 for 10%)
            
        Returns:
            Tax amount
        """
        if not self.taxable:
            return 0.0
        return self.price * tax_rate
    
    def update_inventory(self, quantity_change: int) -> None:
        """
        Update product inventory.
        
        Args:
            quantity_change: Positive to add, negative to subtract
        """
        new_quantity = self.quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Inventory cannot be negative")
        self.quantity = new_quantity
    
    def is_in_stock(self) -> bool:
        """
        Check if product is in stock.
        
        Returns:
            True if quantity > 0
        """
        return self.quantity > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert product to dictionary representation.
        
        Returns:
            Dictionary representation of the product
        """
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'quantity': self.quantity,
            'vendor': self.vendor,
            'description': self.description,
            'tags': self.tags,
            'published': self.published,
            'taxable': self.taxable,
            'requires_shipping': self.requires_shipping,
            'inventory_tracked': self.inventory_tracked,
            'collections': self.collections,
            'sales_channels': self.sales_channels,
            'product_type': self.get_product_type(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'seo_title': self.seo_title,
            'seo_description': self.seo_description
        }