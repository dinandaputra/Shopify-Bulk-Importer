"""Color metaobject mapping for Shopify products"""

# Generated from Shopify metaobjects
# This file contains all available color metaobjects with their GIDs and properties

COLOR_METAOBJECT_MAPPING = {
    "acid-green": {
        "gid": "gid://shopify/Metaobject/131501064341",
        "displayName": "Acid Green",
        "label": "Acid Green",
        "hex": "#77DD77"
    },
    "asus-blue": {
        "gid": "gid://shopify/Metaobject/131501097109",
        "displayName": "Asus Blue",
        "label": "Asus Blue",
        "hex": "#0078D4"
    },
    "bonfire-black": {
        "gid": "gid://shopify/Metaobject/131501129877",
        "displayName": "Bonfire Black",
        "label": "Bonfire Black",
        "hex": "#1C1C1C"
    },
    "brushed-metal": {
        "gid": "gid://shopify/Metaobject/131501162645",
        "displayName": "Brushed Metal",
        "label": "Brushed Metal",
        "hex": "#C0C0C0"
    },
    "cool-silver": {
        "gid": "gid://shopify/Metaobject/131501195413",
        "displayName": "Cool Silver",
        "label": "Cool Silver",
        "hex": "#D3D3D3"
    },
    "dark-shadow-gray": {
        "gid": "gid://shopify/Metaobject/131501228181",
        "displayName": "Dark Shadow Gray",
        "label": "Dark Shadow Gray",
        "hex": "#4A4A4A"
    },
    "eclipse-gray": {
        "gid": "gid://shopify/Metaobject/131501260949",
        "displayName": "Eclipse Gray",
        "label": "Eclipse Gray",
        "hex": "#666666"
    },
    "electro-punk": {
        "gid": "gid://shopify/Metaobject/131501293717",
        "displayName": "Electro Punk",
        "label": "Electro Punk",
        "hex": "#FF1493"
    },
    "fortress-gray": {
        "gid": "gid://shopify/Metaobject/131501326485",
        "displayName": "Fortress Gray",
        "label": "Fortress Gray",
        "hex": "#808080"
    },
    "glacier-blue": {
        "gid": "gid://shopify/Metaobject/131501359253",
        "displayName": "Glacier Blue",
        "label": "Glacier Blue",
        "hex": "#B0E0E6"
    },
    "graphite-black": {
        "gid": "gid://shopify/Metaobject/131501392021",
        "displayName": "Graphite Black",
        "label": "Graphite Black",
        "hex": "#2F4F4F"
    },
    "gun-metal": {
        "gid": "gid://shopify/Metaobject/131501424789",
        "displayName": "Gun Metal",
        "label": "Gun Metal",
        "hex": "#2C3539"
    },
    "jaeger-gray": {
        "gid": "gid://shopify/Metaobject/131501457557",
        "displayName": "Jaeger Gray",
        "label": "Jaeger Gray",
        "hex": "#5A5A5A"
    },
    "mecha-gray": {
        "gid": "gid://shopify/Metaobject/131501490325",
        "displayName": "Mecha Gray",
        "label": "Mecha Gray",
        "hex": "#696969"
    },
    "metallic-hairline": {
        "gid": "gid://shopify/Metaobject/131501523093",
        "displayName": "Metallic Hairline",
        "label": "Metallic Hairline",
        "hex": "#E5E5E5"
    },
    "moonlight-white": {
        "gid": "gid://shopify/Metaobject/131501555861",
        "displayName": "Moonlight White",
        "label": "Moonlight White",
        "hex": "#F8F8FF"
    },
    "off-black": {
        "gid": "gid://shopify/Metaobject/131501588629",
        "displayName": "Off Black",
        "label": "Off Black",
        "hex": "#313131"
    },
    "original-black": {
        "gid": "gid://shopify/Metaobject/131501621397",
        "displayName": "Original Black",
        "label": "Original Black",
        "hex": "#000000"
    },
    "phantom-blue": {
        "gid": "gid://shopify/Metaobject/131501654165",
        "displayName": "Phantom Blue",
        "label": "Phantom Blue",
        "hex": "#191970"
    },
    "platinum-white": {
        "gid": "gid://shopify/Metaobject/131501686933",
        "displayName": "Platinum White",
        "label": "Platinum White",
        "hex": "#FAFAFA"
    },
    "quiet-blue": {
        "gid": "gid://shopify/Metaobject/131501719701",
        "displayName": "Quiet Blue",
        "label": "Quiet Blue",
        "hex": "#4682B4"
    },
    "shadow-black": {
        "gid": "gid://shopify/Metaobject/131501752469",
        "displayName": "Shadow Black",
        "label": "Shadow Black",
        "hex": "#1A1A1A"
    },
    "specter-green": {
        "gid": "gid://shopify/Metaobject/131501785237",
        "displayName": "Specter Green",
        "label": "Specter Green",
        "hex": "#00FF00"
    },
    "starry-black": {
        "gid": "gid://shopify/Metaobject/131501818005",
        "displayName": "Starry Black",
        "label": "Starry Black",
        "hex": "#191919"
    },
    "stealth-black": {
        "gid": "gid://shopify/Metaobject/131501850773",
        "displayName": "Stealth Black",
        "label": "Stealth Black",
        "hex": "#0A0A0A"
    },
    "volt-green": {
        "gid": "gid://shopify/Metaobject/131501883541",
        "displayName": "Volt Green",
        "label": "Volt Green",
        "hex": "#CEFF00"
    }
}

# Helper function to get color GID by handle
def get_color_gid(handle: str) -> str:
    """Get the Shopify GID for a color by its handle"""
    color = COLOR_METAOBJECT_MAPPING.get(handle)
    return color['gid'] if color else None

# Helper function to get color by display name (case-insensitive)
def get_color_by_name(name: str) -> dict:
    """Get color data by display name (case-insensitive)"""
    name_lower = name.lower()
    for handle, color in COLOR_METAOBJECT_MAPPING.items():
        if color['displayName'].lower() == name_lower:
            return {"handle": handle, **color}
    return None

# List of all available color handles
AVAILABLE_COLOR_HANDLES = list(COLOR_METAOBJECT_MAPPING.keys())

# List of all available color names
AVAILABLE_COLOR_NAMES = [color['displayName'] for color in COLOR_METAOBJECT_MAPPING.values()]

# Color groups for UI organization
COLOR_GROUPS = {
    "Black": ["bonfire-black", "graphite-black", "off-black", "original-black", "shadow-black", "starry-black", "stealth-black"],
    "Gray": ["dark-shadow-gray", "eclipse-gray", "fortress-gray", "gun-metal", "jaeger-gray", "mecha-gray"],
    "White": ["moonlight-white", "platinum-white"],
    "Silver": ["brushed-metal", "cool-silver", "metallic-hairline"],
    "Blue": ["asus-blue", "glacier-blue", "phantom-blue", "quiet-blue"],
    "Green": ["acid-green", "specter-green", "volt-green"],
    "Other": ["electro-punk"]
}