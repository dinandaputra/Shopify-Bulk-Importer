"""
Laptop Metafield Mapping System with Actual GIDs

This mapping system uses the actual metaobject GIDs from your Shopify store
to properly link laptop specifications to their metafield references.
"""

from typing import Dict, List, Optional, Any
import json

# Actual metaobject GID mappings fetched from Shopify store
PROCESSOR_METAOBJECTS = {
    "i7-12650H": "gid://shopify/Metaobject/117180924053",  # Intel Core i7-12650H (16 CPUs), ~2.3GHz
    "i5-10200H": "gid://shopify/Metaobject/117533278357",  # Intel Core i5-10200H, (8CPU)~2.4GHz
    "i7 Quad-Core": "gid://shopify/Metaobject/118603219093",  # Intel Core i7 Quad-Core 2.2GHz
    "i5-7200U": "gid://shopify/Metaobject/125788291221",  # Intel Core i5 7200U CPU @2.5GHz
    "i5 Dual-Core": "gid://shopify/Metaobject/125795434645",  # Intel Core i5 Dual-Core 2.3 GHz
    "i9 8-Core": "gid://shopify/Metaobject/125796843669",  # Intel Core i9 8-Core 2.3 GHz
    "i7 6-Core": "gid://shopify/Metaobject/125798940821",  # Intel Core i7 6-Core 2.6 GHz
    "Apple M2": "gid://shopify/Metaobject/125799628949",  # Apple M2 Chip
    "i7-2.8GHz": "gid://shopify/Metaobject/125801791637",  # Intel Core i7 Quad-Core 2.8 GHz
    "i5-1.6GHz": "gid://shopify/Metaobject/125802119317",  # Intel Core i5 Dual-Core 1.6 GHz
    "i5-10300H": "gid://shopify/Metaobject/125803036821",  # Intel Core i5-10300H (8 CPUs), ~2.5GHz
    "Ryzen 7 4800HS": "gid://shopify/Metaobject/125803430037",  # AMD Ryzen 7 4800HS (16 CPUs), ~2.9GHz
    "Ryzen 7 5800H": "gid://shopify/Metaobject/125803659413",  # AMD Ryzen 7 5800H (16 CPUs), ~3.2GHz
    "Ryzen 9 5900HS": "gid://shopify/Metaobject/125921984661",  # AMD Ryzen 9 5900HS (16 CPUs), ~3.3GHz
    "i7-10750H": "gid://shopify/Metaobject/125922246805",  # Intel Core i7 10750H (12 CPUs), ~2.6GHz
    "i5-8265U": "gid://shopify/Metaobject/125933486229",  # Intel Core i5-8265U (8 CPUs), ~1.8GHz
    "i5-12450H": "gid://shopify/Metaobject/125933682837",  # Intel Core i5-12450H (12 CPUs), ~2.0GHz
    "i5-1135G7": "gid://shopify/Metaobject/125934796949",  # Intel Core i5-1135G7 @ 2.40GHz
    "i9-11900H": "gid://shopify/Metaobject/125935124629",  # Intel Core i9-11900H (16 CPUs), ~2.6GHz
    "i5-1035G1": "gid://shopify/Metaobject/125935779989",  # Intel Core i5-1035G1 (8 CPUs), ~1.2GHz
}

GRAPHICS_METAOBJECTS = {
    "Intel UHD Graphics": "gid://shopify/Metaobject/117180858517",
    "Intel Iris Pro": "gid://shopify/Metaobject/118603317397",
    "Intel HD Graphics 620": "gid://shopify/Metaobject/125788225685",
    "Intel Iris Plus 640": "gid://shopify/Metaobject/125795369109",
    "Intel UHD Graphics 630": "gid://shopify/Metaobject/125796810901",
    "Intel HD Graphics 630": "gid://shopify/Metaobject/125801726101",
    "Intel HD Graphics 6000": "gid://shopify/Metaobject/125802086549",
    "Intel HD Graphics 5000": "gid://shopify/Metaobject/125802250389",
    "Intel Iris Plus 645": "gid://shopify/Metaobject/125802479765",
    "Intel Iris Plus 650": "gid://shopify/Metaobject/125802578069",
    "Radeon Graphics": "gid://shopify/Metaobject/125803397269",
    "Intel Iris Xe Graphics": "gid://shopify/Metaobject/125934829717",
    "Intel UHD Graphics Family": "gid://shopify/Metaobject/125935190165",
    "Intel HD Graphics 515": "gid://shopify/Metaobject/125936599189",
    "Intel Iris Graphics 540": "gid://shopify/Metaobject/125936697493",
    "Intel UHD Graphics 617": "gid://shopify/Metaobject/125936795797",
}

VGA_METAOBJECTS = {
    "RTX 4050": "gid://shopify/Metaobject/117180891285",  # NVIDIA GeForce RTX 4050 6GB
    "RTX 3060": "gid://shopify/Metaobject/117533343893",  # NVIDIA GeForce RTX 3060 6GB
    "Radeon Pro 5500M": "gid://shopify/Metaobject/125796876437",  # AMD Radeon Pro 5500M 4 GB
    "Radeon Pro 5300M": "gid://shopify/Metaobject/125798908053",  # AMD Radeon Pro 5300M 4 GB
    "Radeon Pro 555": "gid://shopify/Metaobject/125799891093",  # Radeon Pro 555 2 GB
    "RTX 2060": "gid://shopify/Metaobject/125922410645",  # NVIDIA GeForce RTX 2060 6 GB
    "RTX 3050": "gid://shopify/Metaobject/125933813909",  # NVIDIA GeForce RTX 3050 4 GB
    "RTX 3050 Ti": "gid://shopify/Metaobject/125935386773",  # NVIDIA GeForce RTX 3050 Ti 4GB
}

DISPLAY_METAOBJECTS = {
    "15.6 FHD 144Hz": "gid://shopify/Metaobject/117180760213",  # 15.6-inch FHD (144Hz)
    "15 FHD 144Hz": "gid://shopify/Metaobject/117533442197",  # 15-inch FHD 144Hz
    "15 Retina": "gid://shopify/Metaobject/118603120789",  # 15-inch Retina
    "13.4 FHD 120Hz Touch": "gid://shopify/Metaobject/119138222229",  # 13.4 Inch FHD (120Hz) Touchscreen
    "15 FHD 60Hz": "gid://shopify/Metaobject/125794517141",  # 15-inch FHD (60Hz)
    "13 Retina": "gid://shopify/Metaobject/125795336341",  # 13-inch Retina
    "16 Retina": "gid://shopify/Metaobject/125796778133",  # 16-inch Retina
    "13.6 Retina": "gid://shopify/Metaobject/125799596181",  # 13.6-inch Retina
    "15.4 Retina": "gid://shopify/Metaobject/125799923861",  # 15.4-inch Retina
    "13 inch": "gid://shopify/Metaobject/125802053781",  # 13-inch
    "11 inch": "gid://shopify/Metaobject/125802217621",  # 11-inch
    "13.3 Retina": "gid://shopify/Metaobject/125802348693",  # 13.3-inch Retina
    "15 FHD 240Hz": "gid://shopify/Metaobject/125803331733",  # 15-inch FHD (240Hz)
    "15 FHD 300Hz": "gid://shopify/Metaobject/125922312341",  # 15-inch FHD (300Hz)
    "13 FHD Touch": "gid://shopify/Metaobject/125933617301",  # 13-inch FHD (60Hz) Touch Screen
    "14 FHD 144Hz": "gid://shopify/Metaobject/125935354005",  # 14-inch FHD (144Hz)
    "15 HD 60Hz": "gid://shopify/Metaobject/125935911061",  # 15-inch HD (60Hz)
    "12 Retina": "gid://shopify/Metaobject/125936631957",  # 12-inch Retina
}

STORAGE_METAOBJECTS = {
    "512GB SSD": "gid://shopify/Metaobject/117265825941",
    "256GB SSD": "gid://shopify/Metaobject/117530034325",
    "128GB SSD": "gid://shopify/Metaobject/125795467413",
    "1TB SSD": "gid://shopify/Metaobject/125797826709",
    "500GB SSD + 1TB HDD": "gid://shopify/Metaobject/125922345109",
    "256GB SSD + 512GB HDD": "gid://shopify/Metaobject/125936009365",
}

OS_METAOBJECTS = {
    "macOS Sequoia": "gid://shopify/Metaobject/125803364501",
    "macOS Ventura": "gid://shopify/Metaobject/125803462805",
    "macOS Monterey": "gid://shopify/Metaobject/125803495573",
    "macOS Big Sur": "gid://shopify/Metaobject/125803528341",
    "Windows 11": "gid://shopify/Metaobject/125803626645",
    "macOS Sonoma": "gid://shopify/Metaobject/125936828565",
}

KEYBOARD_LAYOUT_METAOBJECTS = {
    "US": "gid://shopify/Metaobject/117265563797",  # US - International Keyboard
    "Japanese": "gid://shopify/Metaobject/117265596565",  # Japanese - JIS Keyboard
}

# Laptop-specific metaobject mappings
LAPTOP_RANK_METAOBJECTS = {
    "BNIB": "gid://shopify/Metaobject/117266186389",
    "BNOB": "gid://shopify/Metaobject/117266219157",
    "BNWB": "gid://shopify/Metaobject/117266251925",
    "S+": "gid://shopify/Metaobject/117266284693",
    "S": "gid://shopify/Metaobject/117266317461",
    "A+": "gid://shopify/Metaobject/117266350229",
    "A": "gid://shopify/Metaobject/117266382997",
}

LAPTOP_INCLUSION_METAOBJECTS = {
    "Full set": "gid://shopify/Metaobject/117265989781",
    "With box": "gid://shopify/Metaobject/117266022549",
    "Unit + Charger original": "gid://shopify/Metaobject/117266055317",
    "Unit + Bonus charger": "gid://shopify/Metaobject/117268873365",
}

LAPTOP_MINUS_METAOBJECTS = {
    "White spot": "gid://shopify/Metaobject/125916905621",
    "Shadow": "gid://shopify/Metaobject/125917266069",
    "Dead Pixel": "gid://shopify/Metaobject/125922050197",
    "Speaker pecah": "gid://shopify/Metaobject/125922508949",
    "Battery service": "gid://shopify/Metaobject/125932535957",
}

def get_metaobject_gid(field_name: str, value: str) -> Optional[str]:
    """Get metaobject GID for a given field and value"""
    
    # Try using the enhanced mapping first
    try:
        from config.laptop_metafield_mapping_full import get_metaobject_gid_full
        result = get_metaobject_gid_full(field_name, value)
        if result:
            return result
    except ImportError:
        pass
    
    # Handle laptop-specific metaobjects
    if field_name == "rank" and value in LAPTOP_RANK_METAOBJECTS:
        return LAPTOP_RANK_METAOBJECTS[value]
    
    if field_name == "inclusions" and value in LAPTOP_INCLUSION_METAOBJECTS:
        return LAPTOP_INCLUSION_METAOBJECTS[value]
    
    if field_name == "minus" and value in LAPTOP_MINUS_METAOBJECTS:
        return LAPTOP_MINUS_METAOBJECTS[value]
    
    # Handle laptop-specific metaobjects
    mappings = {
        "processor": PROCESSOR_METAOBJECTS,
        "graphics": GRAPHICS_METAOBJECTS,
        "vga": VGA_METAOBJECTS,
        "display": DISPLAY_METAOBJECTS,
        "storage": STORAGE_METAOBJECTS,
        "os": OS_METAOBJECTS,
        "keyboard_layout": KEYBOARD_LAYOUT_METAOBJECTS,
    }
    
    if field_name in mappings:
        # Try exact match first
        if value in mappings[field_name]:
            return mappings[field_name][value]
        
        # For Display: handle format conversions
        if field_name == 'display':
            # Try to match "15-inch FHD (144Hz)" to "15 FHD 144Hz"
            if '15-inch FHD (144Hz)' in value and '15 FHD 144Hz' in mappings[field_name]:
                return mappings[field_name]['15 FHD 144Hz']
            elif '15.6-inch FHD (144Hz)' in value and '15.6 FHD 144Hz' in mappings[field_name]:
                return mappings[field_name]['15.6 FHD 144Hz']
            elif '15-inch FHD (240Hz)' in value and '15 FHD 240Hz' in mappings[field_name]:
                return mappings[field_name]['15 FHD 240Hz']
            elif '15-inch FHD (300Hz)' in value and '15 FHD 300Hz' in mappings[field_name]:
                return mappings[field_name]['15 FHD 300Hz']
            elif '15-inch FHD (60Hz)' in value and '15 FHD 60Hz' in mappings[field_name]:
                return mappings[field_name]['15 FHD 60Hz']
            elif '15-inch HD (60Hz)' in value and '15 HD 60Hz' in mappings[field_name]:
                return mappings[field_name]['15 HD 60Hz']
            elif '14-inch FHD (144Hz)' in value and '14 FHD 144Hz' in mappings[field_name]:
                return mappings[field_name]['14 FHD 144Hz']
        
        # Try partial matches
        for key, gid in mappings[field_name].items():
            if key.lower() in value.lower() or value.lower() in key.lower():
                return gid
    
    return None

def convert_laptop_data_to_metafields(laptop_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Convert laptop data to metafield format using actual metaobject GIDs
    
    Args:
        laptop_data: Dictionary with laptop specifications
        
    Returns:
        Dict mapping metafield keys to complete metafield data structures
    """
    metafields = {}
    
    # Define metafield configurations - all laptop metafields from Shopify
    metafield_configs = {
        'processor': {'namespace': 'custom', 'key': '01_processor', 'type': 'metaobject_reference'},
        'ram': {'namespace': 'custom', 'key': '02_ram', 'type': 'single_line_text_field'},  # Text field
        'graphics': {'namespace': 'custom', 'key': '03_graphics', 'type': 'metaobject_reference'},
        'display': {'namespace': 'custom', 'key': '04_display', 'type': 'metaobject_reference'},
        'storage': {'namespace': 'custom', 'key': '05_storage', 'type': 'metaobject_reference'},
        'vga': {'namespace': 'custom', 'key': '06_vga', 'type': 'metaobject_reference'},
        'os': {'namespace': 'custom', 'key': '07_os', 'type': 'metaobject_reference'},
        'inclusions': {'namespace': 'custom', 'key': '08_kelengkapan', 'type': 'metaobject_reference'},  # Laptop inclusions
        'rank': {'namespace': 'custom', 'key': '09_rank', 'type': 'metaobject_reference'},  # Laptop rank
        'keyboard_layout': {'namespace': 'custom', 'key': '10_keyboard_layout', 'type': 'metaobject_reference'},
        'minus': {'namespace': 'custom', 'key': 'minus', 'type': 'metaobject_reference'}  # Shared with smartphones
    }
    
    for field_name, config in metafield_configs.items():
        if field_name not in laptop_data or not laptop_data[field_name]:
            continue
        
        value = laptop_data[field_name]
        
        # Handle RAM as text field
        if field_name == 'ram':
            metafields[config['key']] = {
                'namespace': config['namespace'],
                'key': config['key'],
                'type': config['type'],
                'value': str(value)
            }
            continue
        
        # Handle metaobject references
        if 'metaobject' in config['type']:
            # For inclusions and minus, handle potential list values but take only first item
            # since they're defined as single metaobject references in Shopify
            if field_name in ['inclusions', 'minus']:
                # Handle list values from UI multiselect by taking first item
                actual_value = value[0] if isinstance(value, list) and value else value
                if actual_value:
                    gid = get_metaobject_gid(field_name, actual_value)
                    if gid:
                        metafields[config['key']] = {
                            'namespace': config['namespace'],
                            'key': config['key'],
                            'type': config['type'],
                            'value': gid
                        }
            else:
                # Single metaobject reference
                gid = get_metaobject_gid(field_name, value)
                if gid:
                    metafields[config['key']] = {
                        'namespace': config['namespace'],
                        'key': config['key'],
                        'type': config['type'],
                        'value': gid
                    }
    
    return metafields

def find_best_match(value: str, field_name: str) -> Optional[str]:
    """Find the best matching metaobject for a given value"""
    
    # Try to find exact or partial match
    gid = get_metaobject_gid(field_name, value)
    if gid:
        return gid
    
    # For VGA/Graphics cards, check if it's integrated graphics
    if field_name in ['vga', 'graphics'] and 'integrated' in value.lower():
        # Return the integrated graphics option from graphics
        return GRAPHICS_METAOBJECTS.get("Intel UHD Graphics")
    
    return None