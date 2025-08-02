"""
Product mapper for converting between domain entities and Shopify API formats.

This module provides mapping functionality to convert domain product entities
to and from Shopify API formats.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class ProductMapper:
    """
    Maps between domain product entities and Shopify API formats.
    
    This mapper handles the conversion of product data between the clean
    domain representation and the Shopify-specific API format.
    """
    
    def to_shopify_format(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert domain product entity to Shopify API format.
        
        Args:
            product: Domain product entity
            
        Returns:
            Shopify-formatted product data
        """
        shopify_product = {
            "title": product.get("title"),
            "vendor": product.get("vendor", "MyByte International"),
            "product_type": product.get("product_type", "Electronics"),
            "published": product.get("published", False),
            "tags": product.get("tags", []),
            "status": "draft" if not product.get("published") else "active"
        }
        
        # Add body HTML if description is provided
        if product.get("description"):
            shopify_product["body_html"] = product["description"]
        
        # Handle pricing
        if product.get("price"):
            shopify_product["variants"] = [{
                "price": str(product["price"]),
                "inventory_quantity": product.get("quantity", 0),
                "inventory_management": "shopify",
                "fulfillment_service": "manual",
                "requires_shipping": True
            }]
        
        # Handle product-specific fields based on type
        product_type = product.get("product_type_identifier")
        if product_type == "smartphone":
            shopify_product = self._map_smartphone_fields(product, shopify_product)
        elif product_type == "laptop":
            shopify_product = self._map_laptop_fields(product, shopify_product)
        
        return {"product": shopify_product}
    
    def _map_smartphone_fields(self, product: Dict[str, Any], 
                              shopify_product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map smartphone-specific fields.
        
        Args:
            product: Domain product entity
            shopify_product: Shopify product being built
            
        Returns:
            Updated Shopify product data
        """
        # Handle SIM carrier variants
        sim_carriers = product.get("sim_carrier_variants", [])
        if sim_carriers:
            # Create variants for each SIM carrier
            base_variant = shopify_product["variants"][0]
            variants = []
            
            # Calculate inventory per variant
            total_inventory = base_variant.get("inventory_quantity", 0)
            inventory_per_variant = total_inventory // len(sim_carriers)
            remainder = total_inventory % len(sim_carriers)
            
            for i, carrier in enumerate(sim_carriers):
                variant = base_variant.copy()
                variant["option1"] = carrier
                variant["inventory_quantity"] = inventory_per_variant
                
                # Distribute remainder to first variants
                if i < remainder:
                    variant["inventory_quantity"] += 1
                
                variants.append(variant)
            
            shopify_product["variants"] = variants
            shopify_product["options"] = [{
                "name": "SIM Carriers",
                "values": sim_carriers
            }]
        
        # Add smartphone-specific tags
        if product.get("brand"):
            shopify_product["tags"].append(product["brand"])
        if product.get("model"):
            shopify_product["tags"].append(product["model"])
        
        return shopify_product
    
    def _map_laptop_fields(self, product: Dict[str, Any], 
                          shopify_product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map laptop-specific fields.
        
        Args:
            product: Domain product entity
            shopify_product: Shopify product being built
            
        Returns:
            Updated Shopify product data
        """
        # Add laptop-specific tags
        if product.get("cpu"):
            shopify_product["tags"].append(f"CPU:{product['cpu']}")
        if product.get("ram"):
            shopify_product["tags"].append(f"RAM:{product['ram']}")
        if product.get("storage"):
            shopify_product["tags"].append(f"Storage:{product['storage']}")
        
        return shopify_product
    
    def from_shopify_format(self, shopify_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Shopify API response to domain product entity.
        
        Args:
            shopify_data: Shopify API product data
            
        Returns:
            Domain product entity
        """
        product = shopify_data.get("product", shopify_data)
        
        domain_product = {
            "id": str(product.get("id")),
            "title": product.get("title"),
            "vendor": product.get("vendor"),
            "product_type": product.get("product_type"),
            "published": product.get("status") == "active",
            "tags": product.get("tags", []),
            "created_at": product.get("created_at"),
            "updated_at": product.get("updated_at")
        }
        
        # Extract description from body HTML
        if product.get("body_html"):
            domain_product["description"] = product["body_html"]
        
        # Handle variants and pricing
        variants = product.get("variants", [])
        if variants:
            # For single variant products, extract price and inventory
            if len(variants) == 1:
                variant = variants[0]
                domain_product["price"] = float(variant.get("price", 0))
                domain_product["quantity"] = variant.get("inventory_quantity", 0)
            else:
                # For multi-variant products, store variant data
                domain_product["variants"] = []
                total_quantity = 0
                
                for variant in variants:
                    domain_product["variants"].append({
                        "id": str(variant.get("id")),
                        "title": variant.get("title"),
                        "price": float(variant.get("price", 0)),
                        "quantity": variant.get("inventory_quantity", 0),
                        "option1": variant.get("option1"),
                        "option2": variant.get("option2"),
                        "option3": variant.get("option3")
                    })
                    total_quantity += variant.get("inventory_quantity", 0)
                
                domain_product["quantity"] = total_quantity
                
                # Extract options
                if product.get("options"):
                    domain_product["options"] = product["options"]
        
        return domain_product
    
    def map_metafields_to_shopify(self, metafields: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Map domain metafields to Shopify format.
        
        Args:
            metafields: List of domain metafield objects
            
        Returns:
            List of Shopify-formatted metafields
        """
        shopify_metafields = []
        
        for metafield in metafields:
            shopify_metafield = {
                "namespace": metafield.get("namespace", "custom"),
                "key": metafield["key"],
                "type": metafield.get("type", "single_line_text_field")
            }
            
            # Handle value formatting based on type
            value = metafield["value"]
            if metafield.get("type") == "list.metaobject_reference":
                # Ensure value is JSON array format
                if isinstance(value, list):
                    shopify_metafield["value"] = json.dumps(value)
                else:
                    shopify_metafield["value"] = value
            else:
                shopify_metafield["value"] = str(value)
            
            # Add owner ID if provided
            if metafield.get("owner_id"):
                shopify_metafield["ownerId"] = metafield["owner_id"]
            
            shopify_metafields.append(shopify_metafield)
        
        return shopify_metafields