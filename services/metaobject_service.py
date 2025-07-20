from typing import Dict, List, Optional, Any
from services.shopify_api import shopify_api, ShopifyAPIError

class MetaobjectService:
    """
    Service for handling Shopify metaobjects and their references
    """
    
    def __init__(self):
        self.api = shopify_api
        self._metaobject_cache = {}
        self._definition_cache = {}
    
    def get_smartphone_metafield_references(self, smartphone_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get metaobject references for smartphone metafields
        
        Args:
            smartphone_data: Dictionary with smartphone field values
            
        Returns:
            Dictionary mapping metafield keys to metaobject global IDs and types
        """
        references = {}
        
        # Actual metaobject IDs from your Shopify store
        metaobject_mappings = {
            'sim_carriers': {
                'type': 'list.metaobject_reference',  # List type based on metafield definition
                'values': {
                    'SIM Free': 'gid://shopify/Metaobject/116965343381',
                    'Rakuten Mobile (-)': 'gid://shopify/Metaobject/116971733141',
                    'Softbank (-)': 'gid://shopify/Metaobject/116971765909',
                    'Docomo (-)': 'gid://shopify/Metaobject/116971798677',
                    'AU (-)': 'gid://shopify/Metaobject/116971831445'
                }
            },
            'product_rank': {
                'type': 'metaobject_reference',  # One entry
                'values': {
                    'BNIB': 'gid://shopify/Metaobject/117057519765',
                    'BNOB': 'gid://shopify/Metaobject/117057650837',
                    'BNWB': 'gid://shopify/Metaobject/117057880213',
                    'S+': 'gid://shopify/Metaobject/117058142357',
                    'S': 'gid://shopify/Metaobject/117058240661',
                    'A+': 'gid://shopify/Metaobject/117058273429',
                    'A': 'gid://shopify/Metaobject/117058338965'
                }
            },
            'product_inclusions': {
                'type': 'list.metaobject_reference',  # List type based on error
                'values': {
                    'Full set cable': 'gid://shopify/Metaobject/116985528469',
                    'Bonus charger': 'gid://shopify/Metaobject/116985725077',
                    'Bonus adapter': 'gid://shopify/Metaobject/116986216597',
                    'Bonus anti gores': 'gid://shopify/Metaobject/116986314901',
                    'Bonus softcase': 'gid://shopify/Metaobject/116986347669',
                    'Bukan box bawaan': 'gid://shopify/Metaobject/116986445973',
                    'With box': 'gid://shopify/Metaobject/116986642581',
                    'No box': 'gid://shopify/Metaobject/116986708117',
                    'Full set (charger)': 'gid://shopify/Metaobject/117085601941',
                    'Phone, Charger': 'gid://shopify/Metaobject/117085601941',  # Map to Full set
                    'Phone only': 'gid://shopify/Metaobject/116986708117'  # Map to No box
                }
            }
        }
        
        # Map smartphone fields to metaobject IDs
        for field_key, value in smartphone_data.items():
            print(f"DEBUG: Processing field {field_key} with value: {value}")
            if not value or field_key not in metaobject_mappings:
                print(f"DEBUG: Skipping {field_key} - empty value or not in mappings")
                continue
            
            field_mapping = metaobject_mappings[field_key]
            field_type = field_mapping['type']
            field_values = field_mapping['values']
            
            # Handle list vs single values based on field type and input data
            if field_type == 'list.metaobject_reference':
                # For list metaobject references, collect all valid IDs
                metaobject_ids = []
                
                if isinstance(value, list):
                    # Handle actual lists
                    for item in value:
                        item_id = field_values.get(item.strip())
                        if item_id:
                            metaobject_ids.append(item_id)
                else:
                    # Handle single values that should become lists
                    # Clean the value (remove parentheses and extra text for sim_carriers)
                    clean_value = value
                    if field_key == 'sim_carriers':
                        # Handle format like "Softbank (-)" -> "Softbank"
                        clean_value = value.split('(')[0].strip()
                    
                    item_id = field_values.get(clean_value)
                    if item_id:
                        metaobject_ids.append(item_id)
                
                if metaobject_ids:
                    print(f"DEBUG: Generated list reference for {field_key}: {metaobject_ids}")
                    references[field_key] = {
                        'id': metaobject_ids,  # Always a list for list.metaobject_reference
                        'type': field_type
                    }
                else:
                    print(f"DEBUG: No metaobject IDs found for {field_key}")
            else:
                # Handle single values for non-list fields
                if isinstance(value, list):
                    # For non-list fields that receive list data, take first item
                    value = value[0] if len(value) == 1 else ', '.join(value)
                
                # Look up metaobject ID
                metaobject_id = field_values.get(value)
                
                if metaobject_id:
                    print(f"DEBUG: Generated single reference for {field_key}: {metaobject_id}")
                    references[field_key] = {
                        'id': metaobject_id,
                        'type': field_type
                    }
                else:
                    print(f"DEBUG: No metaobject ID found for {field_key} with value: {value}")
        
        return references
    
    def get_ram_metafield_reference(self, ram_size: str) -> Optional[Dict[str, Any]]:
        """
        Get metafield reference for RAM size using correct metaobject GIDs
        """
        # Correct RAM mappings from Shopify API
        ram_mappings = {
            '3GB': 'gid://shopify/Metaobject/127463915669',
            '4GB': 'gid://shopify/Metaobject/127584206997',
            '6GB': 'gid://shopify/Metaobject/127584239765',
            '8GB': 'gid://shopify/Metaobject/127584272533',
            '12GB': 'gid://shopify/Metaobject/127584305301',
            '16GB': 'gid://shopify/Metaobject/127584370837',
        }
        
        metaobject_id = ram_mappings.get(ram_size)
        if metaobject_id:
            return {
                'id': metaobject_id,
                'type': 'list.metaobject_reference'  # Based on error message pattern
            }
        return None
    
    def get_minus_metafield_reference(self, minus_items: List[str]) -> Optional[Dict[str, Any]]:
        """
        Get metafield reference for minus/issues using correct metaobject GIDs
        """
        if not minus_items:
            return None
        
        # Join multiple issues or use single issue
        minus_text = ', '.join(minus_items) if isinstance(minus_items, list) else minus_items
        
        # Correct minus mappings from Shopify API
        minus_mappings = {
            'White spot': 'gid://shopify/Metaobject/125916905621',
            'Shadow': 'gid://shopify/Metaobject/125917266069',
            'Dead Pixel': 'gid://shopify/Metaobject/125922050197',
            'Speaker pecah': 'gid://shopify/Metaobject/125922508949',
            'Battery service': 'gid://shopify/Metaobject/125932535957',
            # Add some mappings for common variations
            'Minor scratches on back': 'gid://shopify/Metaobject/125916905621',  # Map to White spot
            'Screen scratches': 'gid://shopify/Metaobject/125916905621',  # Map to White spot
            'Battery issue': 'gid://shopify/Metaobject/125932535957',  # Map to Battery service
            'Screen burn-in': 'gid://shopify/Metaobject/125917266069',  # Map to Shadow
        }
        
        # Try to find exact match first
        metaobject_id = minus_mappings.get(minus_text)
        
        # If no exact match, try individual items (for list input)
        if not metaobject_id and isinstance(minus_items, list):
            for item in minus_items:
                metaobject_id = minus_mappings.get(item.strip())
                if metaobject_id:
                    break
        
        if metaobject_id:
            return {
                'id': metaobject_id,
                'type': 'metaobject_reference'  # Single reference based on error patterns
            }
        return None

# Global service instance
metaobject_service = MetaobjectService()