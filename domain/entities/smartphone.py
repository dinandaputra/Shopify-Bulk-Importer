"""
Smartphone entity for the domain layer.

This module defines the smartphone product entity with specific
attributes and business rules for smartphone products.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from domain.entities.product import Product


@dataclass
class SmartphoneEntity(Product):
    """
    Domain entity for smartphone products.
    
    This class extends the base Product with smartphone-specific
    attributes and business logic.
    """
    
    # Smartphone-specific attributes
    brand: str = ""
    model: Optional[str] = None
    storage: Optional[str] = None
    color: Optional[str] = None
    
    # Technical specifications
    ram_size: Optional[str] = None
    network_type: Optional[str] = "5G"
    
    # Product metadata
    product_rank: Optional[str] = None
    product_inclusions: List[str] = field(default_factory=list)
    minus: List[str] = field(default_factory=list)
    
    # SIM carrier options
    sim_carrier_variants: List[str] = field(default_factory=list)
    
    # Cosmetic condition
    cosmetic_condition: Optional[str] = None
    
    def get_product_type(self) -> str:
        """Return the product type identifier."""
        return "smartphone"
    
    def validate_business_rules(self) -> List[str]:
        """
        Validate smartphone-specific business rules.
        
        Returns:
            List of validation error messages
        """
        errors = self.validate_common_rules()
        
        # Brand validation
        if not self.brand:
            errors.append("Brand is required for smartphones")
        
        # Price validation for smartphones
        if self.price < 1000:
            errors.append("Smartphone price must be at least ¥1000")
        
        # Product rank validation
        if not self.product_rank:
            errors.append("Product rank is required for smartphones")
        elif self.product_rank not in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "J"]:
            errors.append(f"Invalid product rank: {self.product_rank}")
        
        # SIM carrier validation
        if self.sim_carrier_variants:
            valid_carriers = [
                "SIM Free", 
                "Softbank (-)", 
                "Docomo (-)", 
                "AU (-)", 
                "Rakuten Mobile (-)"
            ]
            for carrier in self.sim_carrier_variants:
                if carrier not in valid_carriers:
                    errors.append(f"Invalid SIM carrier: {carrier}")
            
            if len(self.sim_carrier_variants) > 5:
                errors.append("Maximum 5 SIM carrier variants allowed")
        
        # Collection validation
        if not self.collections:
            errors.append("At least one collection is required")
        
        return errors
    
    def get_full_title(self) -> str:
        """
        Generate the full product title.
        
        Returns:
            Complete product title with all specifications
        """
        title_parts = [self.brand]
        
        if self.model:
            title_parts.append(self.model)
        
        if self.storage:
            title_parts.append(self.storage)
        
        if self.color:
            title_parts.append(f"[{self.color}]")
        
        # Add network type for newer models
        if self.model and any(keyword in self.model for keyword in ["12", "13", "14", "15", "16"]):
            title_parts.append(self.network_type)
        
        return " ".join(title_parts)
    
    def calculate_variant_inventory(self) -> List[tuple[str, int]]:
        """
        Calculate inventory distribution across SIM carrier variants.
        
        Returns:
            List of tuples (carrier_name, inventory_quantity)
        """
        if not self.sim_carrier_variants:
            return [("Default", self.quantity)]
        
        variant_count = len(self.sim_carrier_variants)
        base_quantity = self.quantity // variant_count
        remainder = self.quantity % variant_count
        
        variants = []
        for i, carrier in enumerate(self.sim_carrier_variants):
            quantity = base_quantity
            if i < remainder:
                quantity += 1
            variants.append((carrier, quantity))
        
        return variants
    
    def add_inclusion(self, inclusion: str) -> None:
        """
        Add a product inclusion.
        
        Args:
            inclusion: Inclusion to add
        """
        if inclusion and inclusion not in self.product_inclusions:
            self.product_inclusions.append(inclusion)
    
    def remove_inclusion(self, inclusion: str) -> None:
        """
        Remove a product inclusion.
        
        Args:
            inclusion: Inclusion to remove
        """
        if inclusion in self.product_inclusions:
            self.product_inclusions.remove(inclusion)
    
    def add_minus(self, minus_item: str) -> None:
        """
        Add a minus (missing item).
        
        Args:
            minus_item: Missing item to add
        """
        if minus_item and minus_item not in self.minus:
            self.minus.append(minus_item)
    
    def remove_minus(self, minus_item: str) -> None:
        """
        Remove a minus (missing item).
        
        Args:
            minus_item: Missing item to remove
        """
        if minus_item in self.minus:
            self.minus.remove(minus_item)
    
    def get_condition_score(self) -> int:
        """
        Get numeric score based on product rank.
        
        Returns:
            Numeric score (1-10) based on rank
        """
        rank_scores = {
            "A": 10, "A-": 9,
            "B+": 8, "B": 7, "B-": 6,
            "C+": 5, "C": 4, "C-": 3,
            "J": 1
        }
        return rank_scores.get(self.product_rank, 0)
    
    def is_premium_condition(self) -> bool:
        """
        Check if product is in premium condition.
        
        Returns:
            True if rank is A or A-
        """
        return self.product_rank in ["A", "A-"]
    
    def to_dict(self) -> dict:
        """
        Convert smartphone entity to dictionary.
        
        Returns:
            Dictionary representation of the smartphone
        """
        base_dict = super().to_dict()
        base_dict.update({
            'brand': self.brand,
            'model': self.model,
            'storage': self.storage,
            'color': self.color,
            'ram_size': self.ram_size,
            'network_type': self.network_type,
            'product_rank': self.product_rank,
            'product_inclusions': self.product_inclusions,
            'minus': self.minus,
            'sim_carrier_variants': self.sim_carrier_variants,
            'cosmetic_condition': self.cosmetic_condition,
            'full_title': self.get_full_title(),
            'condition_score': self.get_condition_score(),
            'is_premium': self.is_premium_condition()
        })
        return base_dict