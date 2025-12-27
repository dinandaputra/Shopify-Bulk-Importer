"""
Metafield value object for representing Shopify metafields.

This module defines an immutable value object for handling metafield
data with proper validation.
"""

from dataclasses import dataclass
from typing import Any, Optional
import json


@dataclass(frozen=True)
class Metafield:
    """
    Value object for representing metafields.
    
    This immutable class ensures metafield data is always valid and
    provides methods for converting to Shopify format.
    """
    
    namespace: str
    key: str
    value: Any
    type: str
    owner_id: Optional[str] = None
    
    def __post_init__(self):
        """Validate metafield after initialization."""
        # Validate namespace
        if not self.namespace:
            raise ValueError("Namespace is required")
        if len(self.namespace) > 255:
            raise ValueError("Namespace must be 255 characters or less")
        
        # Validate key
        if not self.key:
            raise ValueError("Key is required")
        if len(self.key) > 64:
            raise ValueError("Key must be 64 characters or less")
        
        # Validate type
        valid_types = [
            "single_line_text_field",
            "multi_line_text_field", 
            "number_integer",
            "number_decimal",
            "boolean",
            "json",
            "date",
            "date_time",
            "metaobject_reference",
            "list.metaobject_reference",
            "list.single_line_text_field",
            "list.number_integer",
            "url",
            "color",
            "file_reference",
            "list.file_reference"
        ]
        
        if self.type not in valid_types:
            raise ValueError(f"Invalid metafield type: {self.type}")
        
        # Validate value based on type
        self._validate_value()
    
    def _validate_value(self):
        """Validate value based on metafield type."""
        if self.value is None:
            return
        
        # Number validations
        if self.type == "number_integer":
            if not isinstance(self.value, int):
                try:
                    int(self.value)
                except (ValueError, TypeError):
                    raise ValueError(f"Value must be an integer for type {self.type}")
        
        elif self.type == "number_decimal":
            if not isinstance(self.value, (int, float)):
                try:
                    float(self.value)
                except (ValueError, TypeError):
                    raise ValueError(f"Value must be a number for type {self.type}")
        
        # Boolean validation
        elif self.type == "boolean":
            if not isinstance(self.value, bool):
                raise ValueError(f"Value must be a boolean for type {self.type}")
        
        # List validations
        elif self.type.startswith("list."):
            if not isinstance(self.value, list):
                raise ValueError(f"Value must be a list for type {self.type}")
        
        # Reference validations
        elif "reference" in self.type:
            if self.type == "metaobject_reference":
                if not isinstance(self.value, str) or not self.value.startswith("gid://"):
                    raise ValueError("Metaobject reference must be a GID string")
            elif self.type == "list.metaobject_reference":
                if not isinstance(self.value, list):
                    raise ValueError("List metaobject reference must be a list")
                for item in self.value:
                    if not isinstance(item, str) or not item.startswith("gid://"):
                        raise ValueError("All items in list must be GID strings")
    
    def to_shopify_format(self) -> dict:
        """
        Convert to Shopify API format.
        
        Returns:
            Dictionary in Shopify metafield format
        """
        shopify_format = {
            "namespace": self.namespace,
            "key": self.key,
            "type": self.type
        }
        
        # Format value based on type
        if self.type == "json" or self.type.startswith("list."):
            # JSON and list types need to be JSON strings
            if isinstance(self.value, str):
                shopify_format["value"] = self.value
            else:
                shopify_format["value"] = json.dumps(self.value)
        else:
            shopify_format["value"] = str(self.value)
        
        # Add owner ID if present
        if self.owner_id:
            shopify_format["ownerId"] = self.owner_id
        
        return shopify_format
    
    def with_owner(self, owner_id: str) -> 'Metafield':
        """
        Create a new Metafield with the specified owner ID.
        
        Args:
            owner_id: The owner ID (e.g., product or variant GID)
            
        Returns:
            New Metafield instance with owner ID
        """
        return Metafield(
            namespace=self.namespace,
            key=self.key,
            value=self.value,
            type=self.type,
            owner_id=owner_id
        )
    
    def is_reference_type(self) -> bool:
        """
        Check if this is a reference type metafield.
        
        Returns:
            True if metafield is a reference type
        """
        return "reference" in self.type
    
    def is_list_type(self) -> bool:
        """
        Check if this is a list type metafield.
        
        Returns:
            True if metafield is a list type
        """
        return self.type.startswith("list.")
    
    def get_display_value(self) -> str:
        """
        Get a human-readable display value.
        
        Returns:
            Formatted display value
        """
        if self.type == "boolean":
            return "Yes" if self.value else "No"
        elif self.type == "list.metaobject_reference":
            return f"{len(self.value)} references" if self.value else "No references"
        elif isinstance(self.value, list):
            return f"{len(self.value)} items"
        else:
            return str(self.value)
    
    def __str__(self) -> str:
        """String representation of the metafield."""
        return f"{self.namespace}.{self.key}: {self.get_display_value()}"
    
    def __repr__(self) -> str:
        """Developer representation of the metafield."""
        return (f"Metafield(namespace='{self.namespace}', key='{self.key}', "
                f"value={repr(self.value)}, type='{self.type}')")
    
    def to_dict(self) -> dict:
        """
        Convert metafield to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "namespace": self.namespace,
            "key": self.key,
            "value": self.value,
            "type": self.type,
            "owner_id": self.owner_id,
            "display_value": self.get_display_value()
        }