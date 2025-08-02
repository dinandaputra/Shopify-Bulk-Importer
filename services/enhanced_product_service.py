"""
Enhanced product service using Phase 4 architecture improvements.

This service provides a backward-compatible interface while using the new
repository pattern, domain entities, and dependency injection.
"""

from typing import Dict, Any, List, Optional
import logging
from models.smartphone import SmartphoneProduct
from models.laptop import LaptopProduct
from domain.entities.smartphone import SmartphoneEntity
from domain.entities.laptop import LaptopEntity
from domain.services.product_domain_service import ProductDomainService
from domain.services.metafield_domain_service import MetafieldDomainService
from repositories.interfaces.product_repository import ProductRepository
from repositories.interfaces.metaobject_repository import MetaobjectRepository
from infrastructure.container import get_container
from infrastructure.error_handler import ErrorHandler, ErrorContext
from infrastructure.mappers.product_mapper import ProductMapper
from infrastructure.exceptions import *


class EnhancedProductService:
    """
    Enhanced product service using clean architecture patterns.
    
    This service provides the same interface as the original ProductService
    but uses the new architecture components internally.
    """
    
    def __init__(self):
        """Initialize the enhanced product service."""
        self.container = get_container()
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler(self.logger)
        
        # Resolve dependencies
        self._product_repo = self.container.resolve(ProductRepository)
        self._metaobject_repo = self.container.resolve(MetaobjectRepository)
        self._product_domain_service = self.container.resolve(ProductDomainService)
        self._metafield_domain_service = self.container.resolve(MetafieldDomainService)
        self._mapper = self.container.resolve(ProductMapper)
    
    def create_smartphone_product(self, smartphone: SmartphoneProduct) -> Dict[str, Any]:
        """
        Create a smartphone product using the new architecture.
        
        Args:
            smartphone: Pydantic smartphone model (for backward compatibility)
            
        Returns:
            Product creation result
        """
        context = ErrorContext("create_smartphone_product")
        
        try:
            # Convert Pydantic model to domain entity
            smartphone_entity = self._convert_to_smartphone_entity(smartphone)
            
            # Generate product handle
            handle = self._product_domain_service.generate_product_handle(smartphone_entity)
            
            # Create base product data
            product_data = self._prepare_product_data(smartphone_entity, handle)
            
            # Create product in Shopify
            created_product = self._product_repo.create_product(product_data)
            
            # Process metafields
            metafields_result = self._process_metafields(smartphone_entity, created_product)
            
            # Process variant metafields if SIM carriers are specified
            variant_result = self._process_variant_metafields(
                smartphone_entity, created_product
            )
            
            return {
                "success": True,
                "product": created_product,
                "metafields": metafields_result,
                "variants": variant_result,
                "handle": handle
            }
            
        except Exception as e:
            error_response = self.error_handler.handle_error(e, context)
            return error_response
    
    def create_laptop_product(self, laptop: LaptopProduct) -> Dict[str, Any]:
        """
        Create a laptop product using the new architecture.
        
        Args:
            laptop: Pydantic laptop model (for backward compatibility)
            
        Returns:
            Product creation result
        """
        context = ErrorContext("create_laptop_product")
        
        try:
            # Convert Pydantic model to domain entity
            laptop_entity = self._convert_to_laptop_entity(laptop)
            
            # Generate product handle
            handle = self._product_domain_service.generate_product_handle(laptop_entity)
            
            # Create base product data
            product_data = self._prepare_product_data(laptop_entity, handle)
            
            # Create product in Shopify
            created_product = self._product_repo.create_product(product_data)
            
            # Process metafields
            metafields_result = self._process_metafields(laptop_entity, created_product)
            
            return {
                "success": True,
                "product": created_product,
                "metafields": metafields_result,
                "handle": handle
            }
            
        except Exception as e:
            error_response = self.error_handler.handle_error(e, context)
            return error_response
    
    def _convert_to_smartphone_entity(self, smartphone: SmartphoneProduct) -> SmartphoneEntity:
        """
        Convert Pydantic SmartphoneProduct to domain entity.
        
        Args:
            smartphone: Pydantic model
            
        Returns:
            Domain entity
        """
        return SmartphoneEntity(
            title=smartphone.title,
            price=float(smartphone.price),
            quantity=smartphone.quantity,
            brand=smartphone.brand,
            model=smartphone.model,
            storage=smartphone.storage,
            color=smartphone.color,
            ram_size=smartphone.ram_size,
            product_rank=smartphone.product_rank,
            product_inclusions=smartphone.product_inclusions or [],
            minus=smartphone.minus or [],
            sim_carrier_variants=smartphone.sim_carrier_variants or [],
            collections=smartphone.collections or ["All Products"],
            sales_channels=smartphone.sales_channels or ["Online Store"],
            published=smartphone.published,
            taxable=False  # As per existing business rules
        )
    
    def _convert_to_laptop_entity(self, laptop: LaptopProduct) -> LaptopEntity:
        """
        Convert Pydantic LaptopProduct to domain entity.
        
        Args:
            laptop: Pydantic model
            
        Returns:
            Domain entity
        """
        return LaptopEntity(
            title=laptop.title,
            price=float(laptop.price),
            quantity=laptop.quantity,
            brand=laptop.brand,
            model=laptop.model,
            cpu=laptop.cpu,
            ram=laptop.ram,
            gpu=laptop.gpu,
            display=laptop.display,
            storage=laptop.storage,
            os=laptop.os or "Windows 11",
            keyboard_layout=laptop.keyboard_layout or "US",
            keyboard_backlight=laptop.keyboard_backlight,
            color=laptop.color,
            rank=laptop.rank,
            inclusions=laptop.inclusions or [],
            minus=laptop.minus or [],
            collections=laptop.collections or ["All Products", "Laptop"],
            sales_channels=laptop.sales_channels or ["Online Store"],
            published=laptop.published,
            taxable=False
        )
    
    def _prepare_product_data(self, product_entity, handle: str) -> Dict[str, Any]:
        """
        Prepare product data for Shopify API.
        
        Args:
            product_entity: Domain product entity
            handle: Generated product handle
            
        Returns:
            Product data dictionary
        """
        # Convert entity to dictionary
        product_dict = product_entity.to_dict()
        product_dict["handle"] = handle
        
        # Use mapper to convert to Shopify format
        return self._mapper.to_shopify_format(product_dict)
    
    def _process_metafields(self, product_entity, created_product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process product metafields.
        
        Args:
            product_entity: Domain product entity
            created_product: Created product data
            
        Returns:
            Metafields processing result
        """
        try:
            # Map entity to metafields
            metafields = self._metafield_domain_service.map_product_to_metafields(product_entity)
            
            if not metafields:
                return {"success": True, "message": "No metafields to process"}
            
            # Validate metafields
            validation_errors = self._metafield_domain_service.validate_metafield_constraints(metafields)
            if validation_errors:
                self.logger.warning(f"Metafield validation warnings: {validation_errors}")
            
            # Convert to Shopify format
            shopify_metafields = self._mapper.map_metafields_to_shopify([mf.to_dict() for mf in metafields])
            
            # Add product ID to metafields
            product_id = created_product.get("id")
            for mf in shopify_metafields:
                mf["ownerId"] = f"gid://shopify/Product/{product_id}"
            
            # Assign metafields
            result = self._product_repo.assign_metafields(product_id, shopify_metafields)
            
            return {
                "success": True,
                "metafields_count": len(metafields),
                "validation_warnings": validation_errors,
                "result": result
            }
            
        except Exception as e:
            self.logger.error(f"Metafield processing failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "metafields_count": 0
            }
    
    def _process_variant_metafields(self, smartphone_entity: SmartphoneEntity, 
                                  created_product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process variant metafields for SIM carriers.
        
        Args:
            smartphone_entity: Smartphone domain entity
            created_product: Created product data
            
        Returns:
            Variant metafields processing result
        """
        try:
            if not smartphone_entity.sim_carrier_variants:
                return {"success": True, "message": "No variant metafields to process"}
            
            # Get product variants
            variants = created_product.get("variants", [])
            if not variants:
                return {"success": False, "error": "No variants found in created product"}
            
            # Get SIM carrier metaobject mappings
            carrier_mappings = self._metaobject_repo.get_metaobject_gids("sim_carrier")
            
            # Create variant metafields
            variant_metafields = []
            for i, variant in enumerate(variants):
                if i < len(smartphone_entity.sim_carrier_variants):
                    carrier_name = smartphone_entity.sim_carrier_variants[i]
                    carrier_gid = carrier_mappings.get(carrier_name)
                    
                    if carrier_gid:
                        metafield = self._metafield_domain_service.map_variant_metafields(
                            variant.get("id"),
                            carrier_name,
                            carrier_gid
                        )
                        variant_metafields.append(metafield.to_shopify_format())
            
            if variant_metafields:
                # Assign variant metafields
                result = self._product_repo.assign_variant_metafields(variant_metafields)
                
                return {
                    "success": True,
                    "variant_metafields_count": len(variant_metafields),
                    "result": result
                }
            else:
                return {
                    "success": False,
                    "error": "No valid carrier mappings found"
                }
                
        except Exception as e:
            self.logger.error(f"Variant metafield processing failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "variant_metafields_count": 0
            }
    
    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """
        Get product by ID.
        
        Args:
            product_id: Shopify product ID
            
        Returns:
            Product data or error
        """
        context = ErrorContext("get_product_by_id")
        context.add_data("product_id", product_id)
        
        try:
            product = self._product_repo.get_product(product_id)
            
            if product:
                return {"success": True, "product": product}
            else:
                return {"success": False, "error": "Product not found"}
                
        except Exception as e:
            error_response = self.error_handler.handle_error(e, context)
            return error_response
    
    def update_product(self, product_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update product.
        
        Args:
            product_id: Shopify product ID
            updates: Fields to update
            
        Returns:
            Update result
        """
        context = ErrorContext("update_product")
        context.add_data("product_id", product_id)
        
        try:
            updated_product = self._product_repo.update_product(product_id, updates)
            
            return {
                "success": True,
                "product": updated_product
            }
            
        except Exception as e:
            error_response = self.error_handler.handle_error(e, context)
            return error_response