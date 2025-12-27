"""
Laptop Metaobject Definition Mapping

This file maps the screenshot metafields to their corresponding metaobject definition IDs
from laptop_metafields.py. These are the definitions where we need to add new metaobject entries.
"""

# Screenshot Field -> Metafield Key -> Metaobject Definition ID
LAPTOP_METAOBJECT_DEFINITIONS = {
    # From screenshot -> config/laptop_metafields.py
    "Color": {
        "field_key": "color",
        "metafield_name": "Color",
        "definition_id": "gid://shopify/MetaobjectDefinition/7936606357",
        "namespace": "shopify",
        "key": "color-pattern"
    },
    
    "01 Processor": {
        "field_key": "processor", 
        "metafield_name": "01 Processor",
        "definition_id": "gid://shopify/MetaobjectDefinition/10078486677",
        "namespace": "custom",
        "key": "01_processor"
    },
    
    "02 RAM": {
        "field_key": "ram",
        "metafield_name": "02 RAM", 
        "definition_id": None,  # Text field, not metaobject reference
        "namespace": "custom",
        "key": "02_ram"
    },
    
    "03 Graphics": {
        "field_key": "graphics",
        "metafield_name": "03 Graphics",
        "definition_id": "gid://shopify/MetaobjectDefinition/10078617749",
        "namespace": "custom", 
        "key": "03_graphics"
    },
    
    "04 Display": {
        "field_key": "display",
        "metafield_name": "04 Display",
        "definition_id": "gid://shopify/MetaobjectDefinition/10078388373",
        "namespace": "custom",
        "key": "04_display"
    },
    
    "05 Storage": {
        "field_key": "storage",
        "metafield_name": "05 Storage", 
        "definition_id": "gid://shopify/MetaobjectDefinition/10097983637",
        "namespace": "custom",
        "key": "05_storage"
    },
    
    "06 VGA": {
        "field_key": "vga",
        "metafield_name": "06 VGA",
        "definition_id": "gid://shopify/MetaobjectDefinition/10078650517",
        "namespace": "custom",
        "key": "06_vga"
    },
    
    "07 OS": {
        "field_key": "operating_system",
        "metafield_name": "07 OS",
        "definition_id": "gid://shopify/MetaobjectDefinition/10827989141",
        "namespace": "custom",
        "key": "07_os"
    },
    
    "08 Kelengkapan": {
        "field_key": "kelengkapan",
        "metafield_name": "08 Kelengkapan",
        "definition_id": "gid://shopify/MetaobjectDefinition/10098049173",
        "namespace": "custom",
        "key": "08_kelengkapan"
    },
    
    "09 Rank": {
        "field_key": "rank",
        "metafield_name": "09 Rank",
        "definition_id": "gid://shopify/MetaobjectDefinition/10098147477",
        "namespace": "custom",
        "key": "09_rank"
    },
    
    "10 Keyboard Layout": {
        "field_key": "keyboard_layout",
        "metafield_name": "10 Keyboard Layout",
        "definition_id": "gid://shopify/MetaobjectDefinition/10097819797",
        "namespace": "custom",
        "key": "10_keyboard_layout"
    },
    
    "11 Keyboard Backlight": {
        "field_key": "keyboard_backlight", 
        "metafield_name": "11 Keyboard Backlight",
        "definition_id": "gid://shopify/MetaobjectDefinition/10097787029",
        "namespace": "custom",
        "key": "11_keyboard_backlight"
    },
    
    "Minus": {
        "field_key": "minus",
        "metafield_name": "Minus",
        "definition_id": "gid://shopify/MetaobjectDefinition/10847748245",
        "namespace": "custom",
        "key": "minus"
    }
}

# Extract just the metaobject definition IDs that need new entries
METAOBJECT_DEFINITIONS_TO_POPULATE = {
    "processor": "gid://shopify/MetaobjectDefinition/10078486677",
    "graphics": "gid://shopify/MetaobjectDefinition/10078617749", 
    "display": "gid://shopify/MetaobjectDefinition/10078388373",
    "storage": "gid://shopify/MetaobjectDefinition/10097983637",
    "vga": "gid://shopify/MetaobjectDefinition/10078650517",
    "operating_system": "gid://shopify/MetaobjectDefinition/10827989141",
    "kelengkapan": "gid://shopify/MetaobjectDefinition/10098049173",
    "rank": "gid://shopify/MetaobjectDefinition/10098147477", 
    "keyboard_layout": "gid://shopify/MetaobjectDefinition/10097819797",
    "keyboard_backlight": "gid://shopify/MetaobjectDefinition/10097787029",
    "color": "gid://shopify/MetaobjectDefinition/7936606357",
    "minus": "gid://shopify/MetaobjectDefinition/10847748245"
}

def get_definition_id(field_key: str) -> str:
    """Get metaobject definition ID for a field key"""
    return METAOBJECT_DEFINITIONS_TO_POPULATE.get(field_key)

def get_all_definition_ids() -> list:
    """Get all metaobject definition IDs that need to be populated"""
    return list(METAOBJECT_DEFINITIONS_TO_POPULATE.values())