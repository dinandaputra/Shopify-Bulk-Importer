"""
Laptop Metafield Configuration

This module contains the complete laptop metafield schema mapping between
the UI fields and Shopify API metafield definitions.

Generated from API verification on 2025-07-26.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class MetafieldType(Enum):
    """Metafield types used for laptop products"""
    METAOBJECT_REFERENCE = "metaobject_reference"
    LIST_METAOBJECT_REFERENCE = "list.metaobject_reference"
    SINGLE_LINE_TEXT = "single_line_text_field"
    LIST_SINGLE_LINE_TEXT = "list.single_line_text_field"

@dataclass
class LaptopMetafieldDefinition:
    """Definition of a laptop metafield"""
    id: str
    name: str
    namespace: str
    key: str
    type: MetafieldType
    category: str
    description: str = ""
    metaobject_definition_id: Optional[str] = None
    choices: Optional[List[str]] = None
    validations: Optional[List[Dict]] = None

# Laptop Metafield Definitions (from API verification)
LAPTOP_METAFIELDS = {
    # Core Laptop Specification Fields
    "processor": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144543219861",
        name="01 Processor",
        namespace="custom",
        key="01_processor",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Laptop processor/CPU specification",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10078486677"
    ),
    
    "ram": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144547676309",
        name="02 RAM",
        namespace="custom",
        key="02_ram",
        type=MetafieldType.SINGLE_LINE_TEXT,
        category="TEXT",
        description="Laptop RAM/memory size",
        choices=["3GB", "4GB", "6GB", "8GB", "12GB", "16GB", "18GB", "24GB", "32GB", "64GB", "128GB"]
    ),
    
    "graphics": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144543776917",
        name="03 Graphics",
        namespace="custom",
        key="03_graphics",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Laptop graphics card/GPU specification",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10078617749"
    ),
    
    "display": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144543809685",
        name="04 Display",
        namespace="custom",
        key="04_display",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Laptop display/screen specification",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10078388373"
    ),
    
    "storage": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144543842453",
        name="05 Storage",
        namespace="custom",
        key="05_storage",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Laptop storage type and capacity",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10097983637"
    ),
    
    "vga": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144543875221",
        name="06 VGA",
        namespace="custom",
        key="06_vga",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Laptop VGA/external graphics capability",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10078650517"
    ),
    
    "operating_system": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144543907989",
        name="07 OS",
        namespace="custom",
        key="07_os",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Laptop operating system",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10827989141"
    ),
    
    "keyboard_layout": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144544006293",
        name="10 Keyboard Layout",
        namespace="custom",
        key="10_keyboard_layout",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Laptop keyboard layout (e.g., Japanese, US)",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10097819797"
    ),
    
    "keyboard_backlight": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144544235669",
        name="11 Keyboard Backlight",
        namespace="custom",
        key="11_keyboard_backlight",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Laptop keyboard backlight capability",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10097787029"
    ),
    
    # Laptop-specific metafields that were missing from initial verification
    "kelengkapan": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144543940757",
        name="08 Kelengkapan",
        namespace="custom",
        key="08_kelengkapan",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Laptop accessories and inclusions",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10098049173"
    ),
    
    "rank": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144543973525",
        name="09 Rank",
        namespace="custom",
        key="09_rank",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Laptop condition rank",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10098147477"
    ),
}

# Additional metafields that may be useful for laptops
ADDITIONAL_METAFIELDS = {
    # Existing storage metafield (general)
    "storage_general": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/138277879957",
        name="Storage",
        namespace="custom",
        key="storage",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="General storage metafield",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10099556501"
    ),
    
    # Operating system (Shopify official)
    "os_shopify": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/87965761685",
        name="Operating system",
        namespace="shopify",
        key="operating-system",
        type=MetafieldType.LIST_METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Defines the system software a device uses, such as iOS or ChromeOS",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/7936573589"
    ),
    
    # RAM for smart gadgets (alternative)
    "ram_smart_gadget": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/146059985045",
        name="RAM (Smart Gadget)",
        namespace="custom",
        key="ram_size",
        type=MetafieldType.LIST_METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="RAM metafield for smart gadgets",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10970890389"
    ),
    
    # Shared metafields with smartphones
    "color": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/87965663381",
        name="Color",
        namespace="shopify",
        key="color-pattern",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Product color/pattern",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/7936606357"
    ),
    
    "minus": LaptopMetafieldDefinition(
        id="gid://shopify/MetafieldDefinition/144724394133",
        name="Minus",
        namespace="custom",
        key="minus",
        type=MetafieldType.METAOBJECT_REFERENCE,
        category="REFERENCE",
        description="Product condition issues or defects",
        metaobject_definition_id="gid://shopify/MetaobjectDefinition/10847748245"
    ),
}

# All laptop metafields are now properly defined above
# Color and Minus are shared with smartphones (same metafield definitions)
# Kelengkapan and Rank are laptop-specific metafields

# Laptop field order for UI (matching screenshot)
LAPTOP_FIELD_ORDER = [
    "color",                # 🔗 Shared with smartphones
    "processor",            # ✅ Available
    "ram",                  # ✅ Available
    "graphics",             # ✅ Available
    "display",              # ✅ Available
    "storage",              # ✅ Available
    "vga",                  # ✅ Available
    "operating_system",     # ✅ Available
    "kelengkapan",          # 📋 custom.08_kelengkapan
    "rank",                 # 📋 custom.09_rank
    "keyboard_layout",      # ✅ Available
    "keyboard_backlight",   # ✅ Available
    "minus",                # 🔗 Shared with smartphones
]

def get_laptop_metafield(field_name: str) -> Optional[LaptopMetafieldDefinition]:
    """Get laptop metafield definition by field name"""
    return LAPTOP_METAFIELDS.get(field_name) or ADDITIONAL_METAFIELDS.get(field_name)

def get_all_laptop_metafields() -> Dict[str, LaptopMetafieldDefinition]:
    """Get all laptop metafield definitions"""
    return {**LAPTOP_METAFIELDS, **ADDITIONAL_METAFIELDS}

def get_metafield_by_key(namespace: str, key: str) -> Optional[LaptopMetafieldDefinition]:
    """Get metafield definition by namespace and key"""
    all_metafields = get_all_laptop_metafields()
    for metafield in all_metafields.values():
        if metafield.namespace == namespace and metafield.key == key:
            return metafield
    return None

def get_required_metaobject_definitions() -> List[str]:
    """Get list of all required metaobject definition IDs for laptops"""
    all_metafields = get_all_laptop_metafields()
    metaobject_ids = []
    
    for metafield in all_metafields.values():
        if metafield.metaobject_definition_id:
            metaobject_ids.append(metafield.metaobject_definition_id)
    
    return list(set(metaobject_ids))  # Remove duplicates

def format_metafield_value(field_name: str, value: str) -> str:
    """Format metafield value according to its type"""
    metafield = get_laptop_metafield(field_name)
    if not metafield:
        return value
    
    if metafield.type in [MetafieldType.METAOBJECT_REFERENCE]:
        # Single metaobject reference
        if not value.startswith("gid://"):
            return f"gid://shopify/Metaobject/{value}"
        return value
    
    elif metafield.type in [MetafieldType.LIST_METAOBJECT_REFERENCE]:
        # List of metaobject references as JSON string
        if isinstance(value, list):
            gids = [f"gid://shopify/Metaobject/{v}" if not v.startswith("gid://") else v for v in value]
            return str(gids).replace("'", '"')
        return value
    
    else:
        # Text fields
        return str(value)

# Mapping from screenshot field names to metafield keys
FIELD_NAME_MAPPING = {
    "Color": "color",                           # 🔗 Shared with smartphones
    "01 Processor": "processor",                # ✅ custom.01_processor
    "02 RAM": "ram",                           # ✅ custom.02_ram
    "03 Graphics": "graphics",                 # ✅ custom.03_graphics
    "04 Display": "display",                   # ✅ custom.04_display
    "05 Storage": "storage",                   # ✅ custom.05_storage
    "06 VGA": "vga",                          # ✅ custom.06_vga
    "07 OS": "operating_system",              # ✅ custom.07_os
    "08 Kelengkapan": "kelengkapan",          # 📋 custom.08_kelengkapan
    "09 Rank": "rank",                        # 📋 custom.09_rank
    "10 Keyboard Layout": "keyboard_layout",   # ✅ custom.10_keyboard_layout
    "11 Keyboard Backlight": "keyboard_backlight", # ✅ custom.11_keyboard_backlight
    "Minus": "minus",                         # 🔗 Shared with smartphones
}