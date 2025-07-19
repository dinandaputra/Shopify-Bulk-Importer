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
        # Fixed based on error messages - some fields need list.metaobject_reference
        metaobject_mappings = {
            'sim_carriers': {
                'type': 'list.metaobject_reference',  # List type based on error
                'values': {
                    'SIM Free': 'gid://shopify/Metaobject/116965343381',
                    'Rakuten Mobile': 'gid://shopify/Metaobject/116971733141',
                    'Softbank': 'gid://shopify/Metaobject/116971765909',
                    'Docomo': 'gid://shopify/Metaobject/116971798677',
                    'AU': 'gid://shopify/Metaobject/116971831445'
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
            if not value or field_key not in metaobject_mappings:
                continue
            
            field_mapping = metaobject_mappings[field_key]
            field_type = field_mapping['type']
            field_values = field_mapping['values']
            
            # Handle list values (like minus, product_inclusions)
            if isinstance(value, list):
                value = ', '.join(value)
            
            # Look up metaobject ID
            metaobject_id = field_values.get(value)
            
            if metaobject_id:
                references[field_key] = {
                    'id': metaobject_id,
                    'type': field_type
                }
        
        return references
    
    def get_ram_metafield_reference(self, ram_size: str) -> Optional[Dict[str, Any]]:
        """
        Get metafield reference for RAM size
        Note: RAM metafields need to be mapped to existing metaobjects
        For now, we'll use a default mapping
        """
        # Default RAM mapping - you may need to adjust these based on your actual RAM metaobjects
        ram_mappings = {
            '4GB': 'gid://shopify/Metaobject/117265825941',  # Use existing ID from test
            '6GB': 'gid://shopify/Metaobject/117265825941',  
            '8GB': 'gid://shopify/Metaobject/117265825941',
            '16GB': 'gid://shopify/Metaobject/117265825941',
            '32GB': 'gid://shopify/Metaobject/117265825941',
        }
        
        metaobject_id = ram_mappings.get(ram_size)
        if metaobject_id:
            return {
                'id': metaobject_id,
                'type': 'list.metaobject_reference'  # Changed based on error message
            }
        return None
    
    def get_minus_metafield_reference(self, minus_items: List[str]) -> Optional[Dict[str, Any]]:
        """
        Get metafield reference for minus/issues
        Note: This needs to be mapped to your actual minus metaobjects
        """
        if not minus_items:
            return None
        
        # For now, use a default mapping - you may need to create these metaobjects
        # or map to existing ones
        minus_text = ', '.join(minus_items)
        
        # Default minus mapping - adjust based on your actual minus metaobjects
        minus_mappings = {
            'Minor scratches on back': 'gid://shopify/Metaobject/117266317461',
            'Screen scratches': 'gid://shopify/Metaobject/117266317461',
            'Battery issue': 'gid://shopify/Metaobject/117266317461',
            'No issues': 'gid://shopify/Metaobject/117266317461'
        }
        
        # Try to find a match or use default
        metaobject_id = minus_mappings.get(minus_text, minus_mappings.get('No issues'))
        
        if metaobject_id:
            return {
                'id': metaobject_id,
                'type': 'metaobject_reference'  # Based on your screenshots
            }
        return None

# Global service instance
metaobject_service = MetaobjectService()