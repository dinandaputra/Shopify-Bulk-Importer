"""
Laptop Metafield Service

This service handles laptop-specific metafield operations including:
- Metafield value formatting and validation
- Metaobject reference lookups
- Laptop metafield creation and updates
- Integration with existing smartphone metafield patterns
"""

import json
from typing import Dict, List, Optional, Any, Union
from config.laptop_metafields import (
    LAPTOP_METAFIELDS,
    ADDITIONAL_METAFIELDS,
    FIELD_NAME_MAPPING,
    get_laptop_metafield,
    format_metafield_value,
    MetafieldType,
    LaptopMetafieldDefinition
)
from services.shopify_api import shopify_api, ShopifyAPIError

class LaptopMetafieldService:
    """Service for managing laptop metafields"""
    
    def __init__(self):
        self.api_client = shopify_api
        self._metaobject_cache = {}
    
    def get_available_metafields(self) -> Dict[str, LaptopMetafieldDefinition]:
        """Get all available laptop metafields"""
        return {**LAPTOP_METAFIELDS, **ADDITIONAL_METAFIELDS}
    
    def get_missing_metafields(self) -> List[str]:
        """Get list of metafields that are missing and need to be created"""
        # All metafields are now properly defined, so return empty list
        return []
    
    def validate_laptop_data(self, laptop_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate laptop data against metafield definitions
        
        Args:
            laptop_data: Dictionary of laptop field data
            
        Returns:
            Dictionary with validation results and formatted values
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "formatted_data": {},
            "metafield_data": {}
        }
        
        for field_name, value in laptop_data.items():
            if not value:  # Skip empty values
                continue
                
            # Map UI field name to internal field name
            internal_field = FIELD_NAME_MAPPING.get(field_name, field_name.lower())
            metafield = get_laptop_metafield(internal_field)
            
            if not metafield:
                validation_result["errors"].append(
                    f"Unknown metafield for field '{field_name}'"
                )
                validation_result["valid"] = False
                continue
            
            # Validate field value
            validation_error = self._validate_field_value(metafield, value)
            if validation_error:
                validation_result["errors"].append(
                    f"Field '{field_name}': {validation_error}"
                )
                validation_result["valid"] = False
                continue
            
            # Format value for Shopify API
            formatted_value = format_metafield_value(internal_field, value)
            validation_result["formatted_data"][field_name] = formatted_value
            
            # Prepare metafield data for API
            validation_result["metafield_data"][internal_field] = {
                "namespace": metafield.namespace,
                "key": metafield.key,
                "type": metafield.type.value,
                "value": formatted_value
            }
        
        return validation_result
    
    def _validate_field_value(self, metafield: LaptopMetafieldDefinition, value: Any) -> Optional[str]:
        """Validate a single field value against its metafield definition"""
        
        # Check choices for text fields
        if metafield.choices and metafield.type == MetafieldType.SINGLE_LINE_TEXT:
            if str(value) not in metafield.choices:
                return f"Invalid choice. Must be one of: {', '.join(metafield.choices)}"
        
        # Validate metaobject references
        if metafield.type in [MetafieldType.METAOBJECT_REFERENCE, MetafieldType.LIST_METAOBJECT_REFERENCE]:
            if not self._is_valid_metaobject_reference(value, metafield.metaobject_definition_id):
                return f"Invalid metaobject reference for {metafield.name}"
        
        return None
    
    def _is_valid_metaobject_reference(self, value: Any, metaobject_def_id: str) -> bool:
        """Check if a metaobject reference is valid"""
        # For now, just check format. In production, you might want to verify
        # the metaobject actually exists and belongs to the correct definition
        if isinstance(value, str):
            return value.startswith("gid://shopify/Metaobject/") or value.isdigit()
        elif isinstance(value, list):
            return all(
                (isinstance(v, str) and (v.startswith("gid://shopify/Metaobject/") or v.isdigit()))
                for v in value
            )
        return False
    
    def create_laptop_metafields(self, product_id: int, laptop_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create metafields for a laptop product
        
        Args:
            product_id: Shopify product ID
            laptop_data: Dictionary of laptop field data
            
        Returns:
            Dictionary with creation results
        """
        validation_result = self.validate_laptop_data(laptop_data)
        
        if not validation_result["valid"]:
            return {
                "success": False,
                "errors": validation_result["errors"],
                "warnings": validation_result["warnings"]
            }
        
        created_metafields = []
        errors = []
        
        for field_name, metafield_data in validation_result["metafield_data"].items():
            try:
                result = self.api_client.create_product_metafield(product_id, metafield_data)
                created_metafields.append({
                    "field": field_name,
                    "metafield_id": result["metafield"]["id"],
                    "value": metafield_data["value"]
                })
            except ShopifyAPIError as e:
                errors.append(f"Failed to create metafield for {field_name}: {str(e)}")
        
        return {
            "success": len(errors) == 0,
            "created_metafields": created_metafields,
            "errors": errors,
            "warnings": validation_result["warnings"]
        }
    
    def get_metaobject_options(self, metafield_name: str) -> List[Dict[str, str]]:
        """
        Get available metaobject options for a given metafield
        
        Args:
            metafield_name: Internal metafield name (e.g., 'processor', 'graphics')
            
        Returns:
            List of metaobject options with id, handle, and display_name
        """
        metafield = get_laptop_metafield(metafield_name)
        if not metafield or not metafield.metaobject_definition_id:
            return []
        
        # Use cache to avoid repeated API calls
        cache_key = metafield.metaobject_definition_id
        if cache_key in self._metaobject_cache:
            return self._metaobject_cache[cache_key]
        
        try:
            # Query metaobjects for this definition
            query = f"""
            query GetMetaobjects {{
              metaobjects(type: "{metafield.metaobject_definition_id}", first: 100) {{
                edges {{
                  node {{
                    id
                    handle
                    displayName
                    fields {{
                      key
                      value
                    }}
                  }}
                }}
              }}
            }}
            """
            
            result = self.api_client._make_graphql_request(query)
            
            if 'data' in result and 'metaobjects' in result['data']:
                metaobjects = result['data']['metaobjects']['edges']
                options = []
                
                for edge in metaobjects:
                    node = edge['node']
                    options.append({
                        'id': node['id'],
                        'handle': node['handle'],
                        'display_name': node['displayName'] or node['handle'],
                        'fields': {field['key']: field['value'] for field in node.get('fields', [])}
                    })
                
                # Cache the result
                self._metaobject_cache[cache_key] = options
                return options
        
        except Exception as e:
            print(f"Failed to fetch metaobject options for {metafield_name}: {e}")
        
        return []
    
    def get_laptop_form_config(self) -> Dict[str, Any]:
        """
        Get form configuration for laptop entry interface
        
        Returns:
            Dictionary with form field configurations
        """
        form_config = {
            "fields": {},
            "field_order": [],
            "missing_fields": []  # All metafields are now available
        }
        
        available_metafields = self.get_available_metafields()
        
        for ui_field_name, internal_field in FIELD_NAME_MAPPING.items():
            metafield = available_metafields.get(internal_field)
            
            field_config = {
                "label": ui_field_name,
                "internal_name": internal_field,
                "required": False,  # Could be configured per field
                "available": metafield is not None
            }
            
            if metafield:
                field_config.update({
                    "type": metafield.type.value,
                    "category": metafield.category,
                    "description": metafield.description,
                    "namespace": metafield.namespace,
                    "key": metafield.key
                })
                
                # Add choices for text fields
                if metafield.choices:
                    field_config["choices"] = metafield.choices
                
                # Add metaobject options for reference fields
                if metafield.type in [MetafieldType.METAOBJECT_REFERENCE, MetafieldType.LIST_METAOBJECT_REFERENCE]:
                    field_config["options"] = self.get_metaobject_options(internal_field)
            
            form_config["fields"][ui_field_name] = field_config
            form_config["field_order"].append(ui_field_name)
        
        return form_config
    
    def get_ram_choices(self) -> List[str]:
        """Get available RAM choices for laptops"""
        metafield = get_laptop_metafield("ram")
        if metafield and metafield.choices:
            return metafield.choices
        return ["8GB", "16GB", "32GB", "64GB"]  # Fallback choices

# Create a singleton instance for easy importing
laptop_metafield_service = LaptopMetafieldService()