"""
Metafield domain service for metafield-related business logic.

This module contains domain services that handle metafield mapping
and validation logic.
"""

from typing import List, Dict, Any, Optional
import json
from domain.entities.product import Product
from domain.entities.smartphone import SmartphoneEntity
from domain.entities.laptop import LaptopEntity
from domain.value_objects.metafield import Metafield


class MetafieldDomainService:
    """
    Domain service for metafield-related business logic.
    
    This service handles the mapping of product properties to metafields
    and validates metafield constraints.
    """
    
    def map_product_to_metafields(self, product: Product) -> List[Metafield]:
        """
        Map product properties to metafields.
        
        Args:
            product: Product entity
            
        Returns:
            List of Metafield value objects
        """
        if isinstance(product, SmartphoneEntity):
            return self._map_smartphone_metafields(product)
        elif isinstance(product, LaptopEntity):
            return self._map_laptop_metafields(product)
        else:
            return self._map_generic_metafields(product)
    
    def _map_smartphone_metafields(self, smartphone: SmartphoneEntity) -> List[Metafield]:
        """
        Map smartphone-specific properties to metafields.
        
        Args:
            smartphone: Smartphone entity
            
        Returns:
            List of metafields
        """
        metafields = []
        
        # Product rank metafield (required)
        if smartphone.product_rank:
            metafields.append(Metafield(
                namespace="custom",
                key="product_rank",
                value=f"gid://shopify/Metaobject/{smartphone.product_rank}",
                type="metaobject_reference"
            ))
        
        # Product inclusions metafield
        if smartphone.product_inclusions:
            inclusion_gids = [f"gid://shopify/Metaobject/{inc}" for inc in smartphone.product_inclusions]
            metafields.append(Metafield(
                namespace="custom",
                key="product_inclusions",
                value=inclusion_gids,
                type="list.metaobject_reference"
            ))
        
        # RAM size metafield
        if smartphone.ram_size:
            metafields.append(Metafield(
                namespace="custom",
                key="ram_size",
                value=f"gid://shopify/Metaobject/{smartphone.ram_size}",
                type="metaobject_reference"
            ))
        
        # Minus (missing items) metafield
        if smartphone.minus:
            minus_gids = [f"gid://shopify/Metaobject/{item}" for item in smartphone.minus]
            metafields.append(Metafield(
                namespace="custom",
                key="minus",
                value=minus_gids,
                type="list.metaobject_reference"
            ))
        
        # Cosmetic condition metafield
        if smartphone.cosmetic_condition:
            metafields.append(Metafield(
                namespace="custom",
                key="cosmetic_condition",
                value=f"gid://shopify/Metaobject/{smartphone.cosmetic_condition}",
                type="metaobject_reference"
            ))
        
        return metafields
    
    def _map_laptop_metafields(self, laptop: LaptopEntity) -> List[Metafield]:
        """
        Map laptop-specific properties to metafields.
        
        Args:
            laptop: Laptop entity
            
        Returns:
            List of metafields
        """
        metafields = []
        
        # Product rank metafield
        if laptop.rank:
            metafields.append(Metafield(
                namespace="custom",
                key="product_rank",
                value=f"gid://shopify/Metaobject/{laptop.rank}",
                type="metaobject_reference"
            ))
        
        # CPU metafield
        if laptop.cpu:
            metafields.append(Metafield(
                namespace="custom",
                key="processor",
                value=f"gid://shopify/Metaobject/{laptop.cpu}",
                type="metaobject_reference"
            ))
        
        # RAM metafield
        if laptop.ram:
            metafields.append(Metafield(
                namespace="custom",
                key="memory",
                value=f"gid://shopify/Metaobject/{laptop.ram}",
                type="metaobject_reference"
            ))
        
        # GPU metafield
        if laptop.gpu:
            metafields.append(Metafield(
                namespace="custom",
                key="graphics",
                value=f"gid://shopify/Metaobject/{laptop.gpu}",
                type="metaobject_reference"
            ))
        
        # Display metafield
        if laptop.display:
            metafields.append(Metafield(
                namespace="custom",
                key="display",
                value=f"gid://shopify/Metaobject/{laptop.display}",
                type="metaobject_reference"
            ))
        
        # Storage metafield
        if laptop.storage:
            metafields.append(Metafield(
                namespace="custom",
                key="storage",
                value=f"gid://shopify/Metaobject/{laptop.storage}",
                type="metaobject_reference"
            ))
        
        # OS metafield
        if laptop.os:
            metafields.append(Metafield(
                namespace="custom",
                key="operating_system",
                value=f"gid://shopify/Metaobject/{laptop.os}",
                type="metaobject_reference"
            ))
        
        # Inclusions metafield
        if laptop.inclusions:
            inclusion_gids = [f"gid://shopify/Metaobject/{inc}" for inc in laptop.inclusions]
            metafields.append(Metafield(
                namespace="custom",
                key="product_inclusions",
                value=inclusion_gids,
                type="list.metaobject_reference"
            ))
        
        # Minus metafield
        if laptop.minus:
            minus_gids = [f"gid://shopify/Metaobject/{item}" for item in laptop.minus]
            metafields.append(Metafield(
                namespace="custom",
                key="minus",
                value=minus_gids,
                type="list.metaobject_reference"
            ))
        
        return metafields
    
    def _map_generic_metafields(self, product: Product) -> List[Metafield]:
        """
        Map generic product properties to metafields.
        
        Args:
            product: Generic product entity
            
        Returns:
            List of metafields
        """
        metafields = []
        
        # Add any generic metafields that apply to all products
        # Currently no generic metafields defined
        
        return metafields
    
    def validate_metafield_constraints(self, metafields: List[Metafield]) -> List[str]:
        """
        Validate metafield business constraints.
        
        Args:
            metafields: List of metafields to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check for duplicate keys within same namespace
        namespace_keys = {}
        for mf in metafields:
            key = f"{mf.namespace}.{mf.key}"
            if key in namespace_keys:
                errors.append(f"Duplicate metafield key: {key}")
            namespace_keys[key] = True
        
        # Validate required metafields
        # Currently product_rank is soft-required for smartphones/laptops
        
        # Validate metafield value constraints
        for mf in metafields:
            if mf.is_reference_type() and mf.value:
                # Validate GID format
                if mf.type == "metaobject_reference":
                    if not isinstance(mf.value, str) or not mf.value.startswith("gid://shopify/Metaobject/"):
                        errors.append(f"Invalid metaobject reference format for {mf.key}")
                elif mf.type == "list.metaobject_reference":
                    if isinstance(mf.value, list):
                        for item in mf.value:
                            if not isinstance(item, str) or not item.startswith("gid://shopify/Metaobject/"):
                                errors.append(f"Invalid metaobject reference in list for {mf.key}")
        
        return errors
    
    def map_variant_metafields(self, variant_id: str, carrier_name: str, 
                             carrier_gid: str) -> Metafield:
        """
        Create metafield for a product variant.
        
        Args:
            variant_id: Shopify variant ID
            carrier_name: SIM carrier name
            carrier_gid: Metaobject GID for the carrier
            
        Returns:
            Metafield for the variant
        """
        return Metafield(
            namespace="custom",
            key="sim_carrier",
            value=[carrier_gid],  # List format required
            type="list.metaobject_reference",
            owner_id=f"gid://shopify/ProductVariant/{variant_id}"
        )
    
    def group_metafields_by_owner(self, metafields: List[Metafield]) -> Dict[str, List[Metafield]]:
        """
        Group metafields by their owner ID.
        
        Args:
            metafields: List of metafields
            
        Returns:
            Dictionary mapping owner IDs to their metafields
        """
        grouped = {}
        
        for mf in metafields:
            owner = mf.owner_id or "product"
            if owner not in grouped:
                grouped[owner] = []
            grouped[owner].append(mf)
        
        return grouped
    
    def merge_metafields(self, existing: List[Metafield], 
                        new: List[Metafield]) -> List[Metafield]:
        """
        Merge new metafields with existing ones, updating duplicates.
        
        Args:
            existing: List of existing metafields
            new: List of new metafields
            
        Returns:
            Merged list of metafields
        """
        # Create lookup by namespace.key
        merged = {f"{mf.namespace}.{mf.key}": mf for mf in existing}
        
        # Add or update with new metafields
        for mf in new:
            key = f"{mf.namespace}.{mf.key}"
            merged[key] = mf
        
        return list(merged.values())