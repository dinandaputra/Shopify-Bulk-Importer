"""
Full Laptop Metafield Mapping with Detailed Names as Keys

This mapping uses the full detailed component names as keys for proper form integration.
Based on laptop_metafield_mapping_complete.py but with restructured keys.

Creation date: 2025-07-28
"""

from typing import Dict, Optional

# Import from complete mapping for processors/graphics/vga
from config.laptop_metafield_mapping_complete import (
    PROCESSOR_METAOBJECTS,
    GRAPHICS_METAOBJECTS,
    VGA_METAOBJECTS
)

# Import other mappings from actual mapping file
from config.laptop_metafield_mapping_actual import (
    DISPLAY_METAOBJECTS,
    STORAGE_METAOBJECTS,
    OS_METAOBJECTS,
    KEYBOARD_LAYOUT_METAOBJECTS,
    LAPTOP_RANK_METAOBJECTS,
    LAPTOP_INCLUSION_METAOBJECTS,
    LAPTOP_MINUS_METAOBJECTS
)

# Build reverse mappings for processors with full names as keys
PROCESSOR_FULL_NAME_MAPPING = {
    # Intel Core i9 Series
    "Intel Core i9-13980HX (32 CPUs), ~3.0GHz": "gid://shopify/Metaobject/131306291349",
    "Intel Core i9-13950HX (32 CPUs), ~3.0GHz": "gid://shopify/Metaobject/131306324117",
    "Intel Core i9-12950HX (24 CPUs), ~2.3GHz": "gid://shopify/Metaobject/131306356885",
    "Intel Core i9-12900HX (24 CPUs), ~2.3GHz": "gid://shopify/Metaobject/131306389653",
    "Intel Core i9-12900HK (20 CPUs), ~2.5GHz": "gid://shopify/Metaobject/131306422421",
    "Intel Core i9-12900H (20 CPUs), ~2.5GHz": "gid://shopify/Metaobject/131306455189",
    "Intel Core i9-11980HK (16 CPUs), ~2.6GHz": "gid://shopify/Metaobject/131306487957",
    "Intel Core i9-11950H (16 CPUs), ~2.6GHz": "gid://shopify/Metaobject/131306520725",
    "Intel Core i9-11900H (16 CPUs), ~2.6GHz": "gid://shopify/Metaobject/125935124629",
    "Intel Core i9-10980HK (16 CPUs), ~2.4GHz": "gid://shopify/Metaobject/131306553493",
    "Intel Core i9-10885H (16 CPUs), ~2.4GHz": "gid://shopify/Metaobject/131306586261",
    "Intel Core i9-9980HK (16 CPUs), ~2.4GHz": "gid://shopify/Metaobject/131306619029",
    "Intel Core i9-8950HK (12 CPUs), ~2.9GHz": "gid://shopify/Metaobject/131306651797",
    "Intel Core i9 8-Core 2.3 GHz": "gid://shopify/Metaobject/125796843669",
    
    # Intel Core i7 Series
    "Intel Core i7-13700HX (24 CPUs), ~2.1GHz": "gid://shopify/Metaobject/131306684565",
    "Intel Core i7-13700H (20 CPUs), ~2.4GHz": "gid://shopify/Metaobject/131306717333",
    "Intel Core i7-12800HX (20 CPUs), ~2.0GHz": "gid://shopify/Metaobject/131306750101",
    "Intel Core i7-12700H (20 CPUs), ~2.3GHz": "gid://shopify/Metaobject/131306782869",
    "Intel Core i7-12650H (16 CPUs), ~2.3GHz": "gid://shopify/Metaobject/117180924053",
    "Intel Core i7-11800H (16 CPUs), ~2.3GHz": "gid://shopify/Metaobject/131306815637",
    "Intel Core i7-11700H (16 CPUs), ~2.3GHz": "gid://shopify/Metaobject/131306848405",
    "Intel Core i7-11370H (8 CPUs), ~3.3GHz": "gid://shopify/Metaobject/131307896981",  # Add if created
    "Intel Core i7-10750H (12 CPUs), ~2.6GHz": "gid://shopify/Metaobject/125922246805",
    "Intel Core i7-10700H (16 CPUs), ~2.6GHz": "gid://shopify/Metaobject/131306881173",
    "Intel Core i7-9750H (12 CPUs), ~2.6GHz": "gid://shopify/Metaobject/131306913941",
    "Intel Core i7-8750H (12 CPUs), ~2.2GHz": "gid://shopify/Metaobject/131306946709",
    "Intel Core i7 6-Core 2.6 GHz": "gid://shopify/Metaobject/125798940821",
    "Intel Core i7 Quad-Core 2.8 GHz": "gid://shopify/Metaobject/125801791637",
    "Intel Core i7 Quad-Core 2.2GHz": "gid://shopify/Metaobject/118603219093",
    
    # Intel Core i5 Series
    "Intel Core i5-13500H (18 CPUs), ~2.6GHz": "gid://shopify/Metaobject/131306979477",
    "Intel Core i5-12500H (16 CPUs), ~2.5GHz": "gid://shopify/Metaobject/131307012245",
    "Intel Core i5-12450H (12 CPUs), ~2.0GHz": "gid://shopify/Metaobject/125933682837",
    "Intel Core i5-11400H (12 CPUs), ~2.7GHz": "gid://shopify/Metaobject/131307045013",
    "Intel Core i5-10300H (8 CPUs), ~2.5GHz": "gid://shopify/Metaobject/125803036821",
    "Intel Core i5-10200H, (8CPU)~2.4GHz": "gid://shopify/Metaobject/117533278357",
    "Intel Core i5-9300H (8 CPUs), ~2.4GHz": "gid://shopify/Metaobject/131307077781",
    "Intel Core i5-8300H (8 CPUs), ~2.3GHz": "gid://shopify/Metaobject/131307110549",
    "Intel Core i5-8265U (8 CPUs), ~1.8GHz": "gid://shopify/Metaobject/125933486229",
    "Intel Core i5-1135G7 @ 2.40GHz": "gid://shopify/Metaobject/125934796949",
    "Intel Core i5-1035G1 (8 CPUs), ~1.2GHz": "gid://shopify/Metaobject/125935779989",
    "Intel Core i5 7200U CPU @2.5GHz": "gid://shopify/Metaobject/125788291221",
    "Intel Core i5 Dual-Core 2.3 GHz": "gid://shopify/Metaobject/125795434645",
    "Intel Core i5 Dual-Core 1.6 GHz": "gid://shopify/Metaobject/125802119317",
    "Intel Core i5 Quad-Core 2.4GHz": "gid://shopify/Metaobject/131307831445",
    "Intel Core i5 Quad-Core 2.0GHz": "gid://shopify/Metaobject/131307864213",
    
    # AMD Ryzen Series
    "AMD Ryzen 9 8945HS (16 CPUs), ~4.0GHz": "gid://shopify/Metaobject/131307143317",
    "AMD Ryzen 9 7945HX (32 CPUs), ~2.5GHz": "gid://shopify/Metaobject/131307176085",
    "AMD Ryzen 9 6900HX (16 CPUs), ~3.3GHz": "gid://shopify/Metaobject/131307208853",
    "AMD Ryzen 9 5900HX (16 CPUs), ~3.3GHz": "gid://shopify/Metaobject/131307241621",
    "AMD Ryzen 9 5900HS (16 CPUs), ~3.3GHz": "gid://shopify/Metaobject/125921984661",
    "AMD Ryzen 7 8845HS (16 CPUs), ~3.8GHz": "gid://shopify/Metaobject/131307274389",
    "AMD Ryzen 7 7840HS (16 CPUs), ~3.8GHz": "gid://shopify/Metaobject/131307339925",
    "AMD Ryzen 7 7735HS (16 CPUs), ~3.2GHz": "gid://shopify/Metaobject/131307372693",
    "AMD Ryzen 7 6800H (16 CPUs), ~3.2GHz": "gid://shopify/Metaobject/131307405461",
    "AMD Ryzen 7 5800H (16 CPUs), ~3.2GHz": "gid://shopify/Metaobject/125803659413",
    "AMD Ryzen 7 4800HS (16 CPUs), ~2.9GHz": "gid://shopify/Metaobject/125803430037",
    "AMD Ryzen 7 4800H (16 CPUs), ~2.9GHz": "gid://shopify/Metaobject/131307438229",
    "AMD Ryzen 5 7640HS (12 CPUs), ~4.3GHz": "gid://shopify/Metaobject/131307470997",
    "AMD Ryzen 5 6600H (12 CPUs), ~3.3GHz": "gid://shopify/Metaobject/131307503765",
    "AMD Ryzen 5 5600H (12 CPUs), ~3.3GHz": "gid://shopify/Metaobject/131307536533",
    "AMD Ryzen 5 4600H (12 CPUs), ~3.0GHz": "gid://shopify/Metaobject/131307569301",
    
    # Apple Silicon
    "Apple M3 Max Chip": "gid://shopify/Metaobject/131307602069",
    "Apple M3 Pro Chip": "gid://shopify/Metaobject/131307634837",
    "Apple M3 Chip": "gid://shopify/Metaobject/131307667605",
    "Apple M2 Chip": "gid://shopify/Metaobject/125799628949",
    "Apple M1 Ultra Chip": "gid://shopify/Metaobject/131307700373",
    "Apple M1 Max Chip": "gid://shopify/Metaobject/131307733141",
    "Apple M1 Pro Chip": "gid://shopify/Metaobject/131307765909",
    "Apple M1 Chip": "gid://shopify/Metaobject/131307798677",
}

# GRAPHICS (Integrated Graphics) Full Name Mapping
GRAPHICS_FULL_NAME_MAPPING = {
    # Intel Integrated Graphics
    "Intel Iris Xe Graphics": "gid://shopify/Metaobject/125934829717",
    "Intel UHD Graphics": "gid://shopify/Metaobject/117180858517",
    "Intel UHD Graphics 630": "gid://shopify/Metaobject/125796810901",
    "Intel UHD Graphics Family": "gid://shopify/Metaobject/125935190165",
    "Intel UHD Graphics 617": "gid://shopify/Metaobject/125936795797",
    "Intel Iris Plus Graphics": "gid://shopify/Metaobject/131307896981",
    "Intel Iris Plus 645": "gid://shopify/Metaobject/125802479765",
    "Intel Iris Plus 650": "gid://shopify/Metaobject/125802578069",
    "Intel Iris Plus 640": "gid://shopify/Metaobject/125795369109",
    "Intel Iris Pro": "gid://shopify/Metaobject/118603317397",
    "Intel Iris Graphics 540": "gid://shopify/Metaobject/125936697493",
    "Intel HD Graphics 620": "gid://shopify/Metaobject/125788225685",
    "Intel HD Graphics 630": "gid://shopify/Metaobject/125801726101",
    "Intel HD Graphics 6000": "gid://shopify/Metaobject/125802086549",
    "Intel HD Graphics 5000": "gid://shopify/Metaobject/125802250389",
    "Intel HD Graphics 515": "gid://shopify/Metaobject/125936599189",
    "Intel HD Graphics 530": "gid://shopify/Metaobject/131307929749",
    
    # AMD Integrated Graphics
    "AMD Radeon Graphics": "gid://shopify/Metaobject/125803397269",
    "AMD Radeon 780M Graphics": "gid://shopify/Metaobject/131307962517",
    "AMD Radeon 680M Graphics": "gid://shopify/Metaobject/131307995285",
    "AMD Radeon Vega 8 Graphics": "gid://shopify/Metaobject/131308028053",
    "AMD Radeon Vega 7 Graphics": "gid://shopify/Metaobject/131308060821",
    "AMD Radeon Vega 6 Graphics": "gid://shopify/Metaobject/131308093589",
    
    # Apple Integrated Graphics
    "Apple GPU (M3 Max)": "gid://shopify/Metaobject/131308126357",
    "Apple GPU (M3 Pro)": "gid://shopify/Metaobject/131308159125",
    "Apple GPU (M3)": "gid://shopify/Metaobject/131308191893",
    "Apple GPU (M2 Ultra)": "gid://shopify/Metaobject/131308224661",
    "Apple GPU (M2 Max)": "gid://shopify/Metaobject/131308257429",
    "Apple GPU (M2 Pro)": "gid://shopify/Metaobject/131308290197",
    "Apple GPU (M2)": "gid://shopify/Metaobject/131308322965",
    "Apple GPU (M1 Ultra)": "gid://shopify/Metaobject/131308355733",
    "Apple GPU (M1 Max)": "gid://shopify/Metaobject/131308388501",
    "Apple GPU (M1 Pro)": "gid://shopify/Metaobject/131308421269",
    "Apple GPU (M1)": "gid://shopify/Metaobject/131308454037",
}

# VGA (Dedicated Graphics) Full Name Mapping
VGA_FULL_NAME_MAPPING = {
    # NVIDIA RTX 40 Series
    "NVIDIA GeForce RTX 4090 16GB": "gid://shopify/Metaobject/131308387477",
    "NVIDIA GeForce RTX 4080 16GB": "gid://shopify/Metaobject/131308420245",
    "NVIDIA GeForce RTX 4070 Ti 12GB": "gid://shopify/Metaobject/131308453013",
    "NVIDIA GeForce RTX 4070 12GB": "gid://shopify/Metaobject/131308485781",
    "NVIDIA GeForce RTX 4060 8GB": "gid://shopify/Metaobject/131302916245",
    "NVIDIA GeForce RTX 4050 6GB": "gid://shopify/Metaobject/117180891285",
    
    # NVIDIA RTX 30 Series  
    "NVIDIA GeForce RTX 3080 Ti 12GB": "gid://shopify/Metaobject/131308551317",
    "NVIDIA GeForce RTX 3080 10GB": "gid://shopify/Metaobject/131308584085",
    "NVIDIA GeForce RTX 3070 Ti 8GB": "gid://shopify/Metaobject/131308616853",
    "NVIDIA GeForce RTX 3070 8GB": "gid://shopify/Metaobject/131308649621",
    "NVIDIA GeForce RTX 3060 6GB": "gid://shopify/Metaobject/117533343893",
    "NVIDIA GeForce RTX 3050 Ti 4GB": "gid://shopify/Metaobject/125935386773",
    "NVIDIA GeForce RTX 3050 4GB": "gid://shopify/Metaobject/125933813909",
    
    # NVIDIA RTX 20 Series
    "NVIDIA GeForce RTX 2080 8GB": "gid://shopify/Metaobject/131308682389",
    "NVIDIA GeForce RTX 2070 8GB": "gid://shopify/Metaobject/131308715157",
    "NVIDIA GeForce RTX 2060 6GB": "gid://shopify/Metaobject/125922410645",
    
    # AMD Radeon
    "AMD Radeon RX 7900 XTX 24GB": "gid://shopify/Metaobject/131308747925",
    "AMD Radeon RX 7600M XT 8GB": "gid://shopify/Metaobject/131308780693",
    "AMD Radeon RX 6800M 12GB": "gid://shopify/Metaobject/131308813461",
    "AMD Radeon RX 6700M 10GB": "gid://shopify/Metaobject/131308846229",
    "AMD Radeon RX 6600M 8GB": "gid://shopify/Metaobject/131308878997",
    "AMD Radeon Pro 5500M 4GB": "gid://shopify/Metaobject/125796876437",
    "AMD Radeon Pro 5300M 4GB": "gid://shopify/Metaobject/125798908053",
    "Radeon Pro 555 2GB": "gid://shopify/Metaobject/125799891093",
}

# Enhanced lookup function with full name support
def get_metaobject_gid_full(field_name: str, value: str) -> Optional[str]:
    """
    Get metaobject GID with support for full detailed names
    
    Args:
        field_name: The metafield name (e.g., 'processor', 'vga', 'graphics')
        value: The full detailed value (e.g., 'Intel Core i7-11370H (8 CPUs), ~3.3GHz')
        
    Returns:
        Metaobject GID if found, None otherwise
    """
    # Map field names to appropriate full name mappings
    full_name_mappings = {
        'processor': PROCESSOR_FULL_NAME_MAPPING,
        'graphics': GRAPHICS_FULL_NAME_MAPPING,
        'vga': VGA_FULL_NAME_MAPPING,
        # Add more mappings as needed
    }
    
    # First try exact match with full name mapping
    if field_name in full_name_mappings:
        if value in full_name_mappings[field_name]:
            return full_name_mappings[field_name][value]
    
    # Fall back to original abbreviated key lookup
    original_mappings = {
        'processor': PROCESSOR_METAOBJECTS,
        'graphics': GRAPHICS_METAOBJECTS,
        'vga': VGA_METAOBJECTS,
        'display': DISPLAY_METAOBJECTS,
        'storage': STORAGE_METAOBJECTS,
        'os': OS_METAOBJECTS,
        'keyboard_layout': KEYBOARD_LAYOUT_METAOBJECTS,
        'rank': LAPTOP_RANK_METAOBJECTS,
        'inclusions': LAPTOP_INCLUSION_METAOBJECTS,
        'minus': LAPTOP_MINUS_METAOBJECTS,
    }
    
    if field_name in original_mappings:
        mapping = original_mappings[field_name]
        
        # Try extracting abbreviated form from the full value
        # For processors: extract "i7-11370H" from "Intel Core i7-11370H (8 CPUs), ~3.3GHz"
        if field_name == 'processor' and 'Intel Core' in value:
            parts = value.split()
            if len(parts) >= 3:
                abbreviated = parts[2].split('(')[0].strip()
                if abbreviated in mapping:
                    return mapping[abbreviated]
        
        # For VGA: extract "RTX 3070" from "NVIDIA GeForce RTX 3070 8GB"
        if field_name == 'vga' and ('RTX' in value or 'GTX' in value):
            if 'RTX' in value:
                rtx_part = value.split('RTX')[1].split()[0]
                abbreviated = f"RTX {rtx_part}"
                if abbreviated in mapping:
                    return mapping[abbreviated]
        
        # For Display: handle different formats
        if field_name == 'display':
            # Try to match "15-inch FHD (144Hz)" to "15 FHD 144Hz"
            if '15-inch FHD (144Hz)' in value:
                return mapping.get('15 FHD 144Hz')
            elif '15.6-inch FHD (144Hz)' in value:
                return mapping.get('15.6 FHD 144Hz')
            elif '15-inch FHD (240Hz)' in value:
                return mapping.get('15 FHD 240Hz')
            elif '15-inch FHD (300Hz)' in value:
                return mapping.get('15 FHD 300Hz')
            elif '15-inch FHD (60Hz)' in value:
                return mapping.get('15 FHD 60Hz')
            elif '15-inch HD (60Hz)' in value:
                return mapping.get('15 HD 60Hz')
            elif '14-inch FHD (144Hz)' in value:
                return mapping.get('14 FHD 144Hz')
            elif '13-inch FHD (60Hz) Touch Screen' in value:
                return mapping.get('13 FHD Touch')
            elif '13.4 Inch FHD (120Hz) Touchscreen' in value:
                return mapping.get('13.4 FHD 120Hz Touch')
            # Retina displays
            elif '16-inch Retina' in value:
                return mapping.get('16 Retina')
            elif '15.4-inch Retina' in value:
                return mapping.get('15.4 Retina')
            elif '15-inch Retina' in value:
                return mapping.get('15 Retina')
            elif '13.6-inch Retina' in value:
                return mapping.get('13.6 Retina')
            elif '13.3-inch Retina' in value:
                return mapping.get('13.3 Retina')
            elif '13-inch Retina' in value:
                return mapping.get('13 Retina')
            elif '12-inch Retina' in value:
                return mapping.get('12 Retina')
            # Basic displays
            elif '13-inch' in value:
                return mapping.get('13 inch')
            elif '11-inch' in value:
                return mapping.get('11 inch')
        
        # Try partial matching as last resort
        for key, gid in mapping.items():
            if key.lower() in value.lower() or value.lower() in key.lower():
                return gid
    
    return None