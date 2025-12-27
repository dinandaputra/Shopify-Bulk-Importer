"""
Product domain service for complex business logic.

This module contains domain services that handle business logic
spanning multiple entities or requiring complex calculations.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from domain.entities.product import Product
from domain.entities.smartphone import SmartphoneEntity
from domain.entities.laptop import LaptopEntity
from domain.value_objects.price import Price
from domain.value_objects.metafield import Metafield
# from utils.handle_generator import generate_handle  # TODO: Fix import when needed


class ProductDomainService:
    """
    Domain service for product-related business logic.
    
    This service handles complex operations that don't belong to a single
    entity but are part of the domain logic.
    """
    
    def calculate_variant_inventory(self, total_quantity: int, variant_count: int) -> List[int]:
        """
        Calculate inventory distribution across variants.
        
        Args:
            total_quantity: Total inventory available
            variant_count: Number of variants to distribute to
            
        Returns:
            List of inventory quantities per variant
        """
        if variant_count <= 0:
            raise ValueError("Variant count must be positive")
        
        if total_quantity < 0:
            raise ValueError("Total quantity cannot be negative")
        
        # Calculate base quantity per variant
        base_quantity = total_quantity // variant_count
        remainder = total_quantity % variant_count
        
        # Distribute inventory
        quantities = [base_quantity] * variant_count
        
        # Distribute remainder to first variants
        for i in range(remainder):
            quantities[i] += 1
        
        return quantities
    
    def generate_product_handle(self, product: Product) -> str:
        """
        Generate unique product handle.
        
        Args:
            product: Product entity
            
        Returns:
            Generated handle string
        """
        # Simple handle generation for now
        import re
        from datetime import datetime
        
        if isinstance(product, SmartphoneEntity):
            parts = [product.brand, product.model or product.title]
            if product.storage:
                parts.append(product.storage)
        elif isinstance(product, LaptopEntity):
            parts = [product.brand, product.model]
            if product.cpu:
                parts.append(product.cpu.split()[0])  # First word of CPU
        else:
            parts = [product.vendor, product.title]
        
        # Create handle from parts
        handle_base = "-".join(parts).lower()
        handle_base = re.sub(r'[^a-z0-9-]', '-', handle_base)
        handle_base = re.sub(r'-+', '-', handle_base).strip('-')
        
        # Add date for uniqueness
        date_suffix = datetime.now().strftime("%y%m%d")
        return f"{handle_base}-{date_suffix}"
    
    def validate_price_rules(self, price: Price, product_type: str) -> List[str]:
        """
        Validate price against business rules.
        
        Args:
            price: Price value object
            product_type: Type of product
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Define minimum prices by product type
        min_prices = {
            "smartphone": 1000,
            "laptop": 5000,
            "tablet": 2000,
            "accessory": 100
        }
        
        min_price = min_prices.get(product_type, 0)
        
        if price.amount < min_price:
            errors.append(
                f"{product_type.capitalize()} price must be at least {Price(min_price, price.currency).formatted}"
            )
        
        # Maximum price validation
        if price.amount > 999999999:
            errors.append("Price exceeds maximum allowed value")
        
        return errors
    
    def calculate_discount(self, original_price: float, sale_price: float) -> Dict[str, Any]:
        """
        Calculate discount information.
        
        Args:
            original_price: Original product price
            sale_price: Sale price
            
        Returns:
            Dictionary with discount information
        """
        if original_price <= 0:
            raise ValueError("Original price must be positive")
        
        if sale_price < 0:
            raise ValueError("Sale price cannot be negative")
        
        if sale_price > original_price:
            raise ValueError("Sale price cannot exceed original price")
        
        discount_amount = original_price - sale_price
        discount_percentage = (discount_amount / original_price) * 100
        
        return {
            "original_price": original_price,
            "sale_price": sale_price,
            "discount_amount": discount_amount,
            "discount_percentage": round(discount_percentage, 2),
            "is_on_sale": sale_price < original_price
        }
    
    def determine_shipping_requirements(self, product: Product) -> Dict[str, Any]:
        """
        Determine shipping requirements based on product.
        
        Args:
            product: Product entity
            
        Returns:
            Dictionary with shipping requirements
        """
        shipping_info = {
            "requires_shipping": product.requires_shipping,
            "weight": None,
            "dimensions": None,
            "shipping_class": "standard",
            "fragile": False
        }
        
        # Laptop-specific shipping
        if isinstance(product, LaptopEntity):
            shipping_info.update({
                "weight": product.weight or 2.5,  # Default 2.5kg
                "shipping_class": "electronics",
                "fragile": True,
                "requires_insurance": product.price > 50000
            })
        
        # Smartphone-specific shipping
        elif isinstance(product, SmartphoneEntity):
            shipping_info.update({
                "weight": 0.3,  # Average smartphone weight
                "shipping_class": "electronics",
                "fragile": True,
                "requires_insurance": product.price > 30000
            })
        
        return shipping_info
    
    def calculate_profit_margin(self, cost: float, selling_price: float) -> Dict[str, float]:
        """
        Calculate profit margin for a product.
        
        Args:
            cost: Product cost
            selling_price: Selling price
            
        Returns:
            Dictionary with margin calculations
        """
        if cost < 0:
            raise ValueError("Cost cannot be negative")
        
        if selling_price <= 0:
            raise ValueError("Selling price must be positive")
        
        profit = selling_price - cost
        margin_percentage = (profit / selling_price) * 100 if selling_price > 0 else 0
        markup_percentage = (profit / cost) * 100 if cost > 0 else float('inf')
        
        return {
            "cost": cost,
            "selling_price": selling_price,
            "profit": profit,
            "margin_percentage": round(margin_percentage, 2),
            "markup_percentage": round(markup_percentage, 2)
        }
    
    def suggest_related_products(self, product: Product, all_products: List[Product]) -> List[Product]:
        """
        Suggest related products based on current product.
        
        Args:
            product: Current product
            all_products: List of all available products
            
        Returns:
            List of suggested related products
        """
        related = []
        
        for other in all_products:
            if other.id == product.id:
                continue
            
            # Same brand products
            if hasattr(product, 'brand') and hasattr(other, 'brand'):
                if product.brand == other.brand:
                    related.append(other)
                    continue
            
            # Similar price range (within 20%)
            price_diff_percentage = abs(product.price - other.price) / product.price
            if price_diff_percentage <= 0.2:
                related.append(other)
                continue
            
            # Same product type
            if product.get_product_type() == other.get_product_type():
                related.append(other)
        
        # Limit to top 10 related products
        return related[:10]
    
    def validate_inventory_rules(self, product: Product) -> List[str]:
        """
        Validate inventory-related business rules.
        
        Args:
            product: Product entity
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check minimum stock levels
        if product.inventory_tracked and product.quantity < 0:
            errors.append("Inventory quantity cannot be negative")
        
        # Check variant inventory consistency
        if isinstance(product, SmartphoneEntity) and product.sim_carrier_variants:
            variant_inventory = product.calculate_variant_inventory()
            total_variant_qty = sum(qty for _, qty in variant_inventory)
            
            if total_variant_qty != product.quantity:
                errors.append("Variant inventory total doesn't match product quantity")
        
        return errors