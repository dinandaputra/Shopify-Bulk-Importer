"""
Master data configuration for dropdown options and templates
"""

from typing import Dict, List
from config.iphone_specs import (
    get_all_series, get_templates_by_series, search_templates, 
    parse_template, generate_product_title as generate_iphone_title, get_color_metafield_gid,
    generate_all_templates as generate_all_iphone_templates
)
from config.galaxy_specs import (
    generate_all_galaxy_templates, search_galaxy_templates, parse_galaxy_template,
    generate_product_title as generate_galaxy_title, get_default_ram, 
    validate_galaxy_combination
)
from config.laptop_specs import (
    generate_all_laptop_templates, search_laptop_templates, parse_laptop_template,
    generate_product_title as generate_laptop_title, validate_laptop_combination,
    get_laptop_colors, get_laptop_configurations, expand_laptop_template_specs
)
from config.laptop_metafield_mapping_interim import (
    convert_laptop_specs_to_metafields, validate_laptop_metafield_mapping_interim as validate_laptop_metafields
)

# SIM Carriers (5 options)
SIM_CARRIERS = [
    "SIM Free",
    "Docomo (-)", 
    "AU (-)",
    "Softbank (-)",
    "Rakuten Mobile (-)"
]

# Product Rank (7 options)
PRODUCT_RANKS = [
    "A",      # Fair condition, visible screen marks
    "A+",     # Good condition, minor screen marks  
    "S",      # Excellent condition, no screen scratches
    "S+",     # Like new condition, very light usage
    "BNWB",   # Brand New Without Box
    "BNOB",   # Brand New Open Box
    "BNIB"    # Brand New In Box
]

# Product Inclusions (9 options, multi-select)
PRODUCT_INCLUSIONS = [
    "Bonus charger",
    "Bonus anti gores",
    "Bonus softcase", 
    "Bukan box bawaan",
    "With box",
    "No box",
    "Full set cable",
    "Full set (charger)",
    "Bonus adapter"
]

# Smart Inclusion Mapping - Pre-defined inclusion combinations
INCLUSION_MAPPINGS = {
    "Full set cable": ["Full set cable", "Bonus adapter", "Bonus softcase", "Bonus anti gores"],
    "Full set (charger)": ["Full set (charger)", "Bonus softcase", "Bonus anti gores"],
    "With box": ["With box", "Bonus charger", "Bonus softcase", "Bonus anti gores"],
    "No box": ["No box", "Bonus charger", "Bonus softcase", "Bonus anti gores"]
}

# Minus Options (5 options, multi-select)
MINUS_OPTIONS = [
    "Battery service",      # Need battery service
    "Speaker pecah",        # Speaker damaged/cracked
    "White spot",          # White spot on screen
    "Shadow",              # Screen burn-in present
    "Dead Pixel"           # Dead pixel on screen
]

# RAM Options (6 options)
RAM_OPTIONS = ["3GB", "4GB", "6GB", "8GB", "12GB", "16GB"]

# Common smartphone brands
COMMON_BRANDS = [
    "iPhone",
    "Samsung",
    "Google",
    "OnePlus",
    "Xiaomi",
    "Oppo",
    "Vivo",
    "Huawei",
    "Sony",
    "LG"
]

# Legacy title templates for non-iPhone devices
TITLE_TEMPLATES = {
    "samsung": [
        "Samsung Galaxy S24 Ultra {storage} (SIM Free)",
        "Samsung Galaxy S24+ {storage} (SIM Free)",
        "Samsung Galaxy S24 {storage} (SIM Free)",
        "Samsung Galaxy S23 Ultra {storage} (SIM Free)",
        "Samsung Galaxy S23+ {storage} (SIM Free)",
        "Samsung Galaxy S23 {storage} (SIM Free)",
        "Samsung Galaxy Note 20 Ultra {storage} (SIM Free)",
        "Samsung Galaxy Z Fold 5 {storage} (SIM Free)",
        "Samsung Galaxy Z Flip 5 {storage} (SIM Free)",
    ],
    "google": [
        "Google Pixel 8 Pro {storage} (SIM Free)",
        "Google Pixel 8 {storage} (SIM Free)",
        "Google Pixel 7 Pro {storage} (SIM Free)",
        "Google Pixel 7 {storage} (SIM Free)",
        "Google Pixel 6 Pro {storage} (SIM Free)",
        "Google Pixel 6 {storage} (SIM Free)",
    ]
}

# Common storage options
STORAGE_OPTIONS = ["64GB", "128GB", "256GB", "512GB", "1TB"]

def get_unified_template_suggestions(search_term: str = "") -> List[str]:
    """Get unified template suggestions for iPhone, Galaxy, and Laptop products"""
    # Get all product type templates
    iphone_templates = generate_all_iphone_templates()
    galaxy_templates = generate_all_galaxy_templates()
    laptop_templates = generate_all_laptop_templates()
    
    # Combine all templates
    all_templates = iphone_templates + galaxy_templates + laptop_templates
    
    if search_term:
        # Apply search filtering
        search_lower = search_term.lower()
        filtered_templates = [template for template in all_templates 
                            if search_lower in template.lower()]
        return filtered_templates[:100]  # Limit for performance
    else:
        return all_templates

def get_iphone_template_suggestions(search_term: str = "") -> List[str]:
    """Get iPhone template suggestions using comprehensive iPhone specs database with inclusion presets"""
    if search_term:
        # Search specific iPhone templates
        all_templates = generate_all_iphone_templates()
        search_lower = search_term.lower()
        filtered_templates = [template for template in all_templates 
                            if search_lower in template.lower()]
        return filtered_templates[:50]  # Limit to 50 suggestions for performance
    else:
        # Return all templates (will be used with search UI)
        return generate_all_iphone_templates()

def get_galaxy_template_suggestions(search_term: str = "") -> List[str]:
    """Get Galaxy template suggestions using comprehensive Galaxy specs database"""
    if search_term:
        return search_galaxy_templates(search_term)[:50]  # Limit for performance
    else:
        return generate_all_galaxy_templates()

def get_laptop_template_suggestions(search_term: str = "") -> List[str]:
    """Get Laptop template suggestions using comprehensive Laptop specs database"""
    if search_term:
        return search_laptop_templates(search_term)[:50]  # Limit for performance
    else:
        return generate_all_laptop_templates()

def get_title_suggestions(search_term: str) -> List[str]:
    """Get title suggestions based on search term (legacy function for non-iPhone)"""
    if not search_term:
        return []
    
    search_lower = search_term.lower()
    suggestions = []
    
    # Check if this is an iPhone search - use new system
    if "iphone" in search_lower:
        return get_iphone_template_suggestions(search_term)
    
    # Legacy system for non-iPhone devices
    for brand_key, templates in TITLE_TEMPLATES.items():
        if brand_key in search_lower or search_lower in brand_key:
            for template in templates:
                for storage in STORAGE_OPTIONS:
                    suggestions.append(template.format(storage=storage))
    
    return suggestions[:10]  # Limit to 10 suggestions

def extract_info_from_iphone_template(template: str) -> Dict[str, str]:
    """Extract comprehensive info from iPhone template using specs database
    
    Args:
        template: iPhone template like "iPhone 15 Pro Max 256GB [Desert Titanium] [No box]"
        
    Returns:
        Dict with model, storage, color, title, brand, collections, and inclusions info
    """
    parsed = parse_template(template)
    if not parsed:
        return {}
    
    model = parsed.get('model', '')
    storage = parsed.get('storage', '')
    color = parsed.get('color', '')
    inclusion_preset = parsed.get('inclusion_preset', '')
    
    # Generate product title with correct 5G logic
    product_title = generate_iphone_title(model, storage, "SIM Free")
    
    # Get color metafield GID
    color_gid = get_color_metafield_gid(color)
    
    # Get inclusions from preset if available
    product_inclusions = []
    if inclusion_preset and inclusion_preset in INCLUSION_MAPPINGS:
        product_inclusions = INCLUSION_MAPPINGS[inclusion_preset]
    
    result = {
        'title': product_title,
        'brand': 'iPhone',
        'model': model,
        'storage': storage,
        'color': color,
        'color_metafield_gid': color_gid,
        'collections': ['All Products', 'iPhone'],  # Auto-assigned collections
        'template': template
    }
    
    # Add inclusions if preset was found
    if product_inclusions:
        result['product_inclusions'] = product_inclusions
        result['inclusion_preset'] = inclusion_preset
    
    return result

def extract_info_from_galaxy_template(template: str) -> Dict[str, str]:
    """Extract comprehensive info from Galaxy template using specs database
    
    Args:
        template: Galaxy template like "Galaxy S24 Ultra 12/256 [Titanium Black] [No box]"
        
    Returns:
        Dict with model, storage, ram, color, title, brand, collections, and inclusions info
    """
    parsed = parse_galaxy_template(template)
    if not parsed:
        return {}
    
    model = parsed.get('model', '')
    storage = parsed.get('storage', '')
    ram = parsed.get('ram', '')
    color = parsed.get('color', '')
    inclusion_preset = parsed.get('inclusion_preset', '')
    
    # Generate product title with correct 5G logic
    product_title = generate_galaxy_title(model, storage, "SIM Free")
    
    # Get inclusions from preset if available
    product_inclusions = []
    if inclusion_preset and inclusion_preset in INCLUSION_MAPPINGS:
        product_inclusions = INCLUSION_MAPPINGS[inclusion_preset]
    
    result = {
        'title': product_title,
        'brand': 'Samsung',
        'model': model,
        'storage': storage,
        'ram': ram,  # Auto-fill RAM for Galaxy products
        'color': color,
        'collections': ['All Products', 'Samsung', 'Android'],  # Auto-assigned collections
        'template': template
    }
    
    # Add inclusions if preset was found
    if product_inclusions:
        result['product_inclusions'] = product_inclusions
        result['inclusion_preset'] = inclusion_preset
    
    return result

def extract_info_from_laptop_template(template: str) -> Dict[str, str]:
    """Extract comprehensive info from Laptop template using specs database
    
    Args:
        template: Laptop template like "ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB] [Graphite Black]"
        
    Returns:
        Dict with model, cpu, ram, gpu, display, storage, color, title, brand, collections info
    """
    parsed = parse_laptop_template(template)
    if not parsed:
        return {}
    
    model = parsed.get('model', '')
    cpu = parsed.get('cpu', '')
    ram = parsed.get('ram', '')
    gpu = parsed.get('gpu', '')
    display = parsed.get('display', '')
    storage = parsed.get('storage', '')
    color = parsed.get('color', '')
    brand = parsed.get('brand', '')
    
    # Generate product title
    product_title = generate_laptop_title(model, cpu, ram)
    
    # Convert specs to metafield GIDs
    metafield_mappings = convert_laptop_specs_to_metafields(parsed)
    
    # Expand specifications to include full names for display
    expanded_info = expand_laptop_template_specs(parsed)
    
    result = {
        'title': product_title,
        'brand': brand,
        'model': model,
        'cpu': cpu,
        'ram': ram,
        'gpu': gpu,
        'display': display,
        'storage': storage,
        'color': color,
        'vga': parsed.get('vga', ''),
        'os': parsed.get('os', 'Windows 11'),
        'keyboard_layout': parsed.get('keyboard_layout', 'US'),
        'keyboard_backlight': parsed.get('keyboard_backlight', 'Yes'),
        'collections': ['All Products', 'Laptop', brand],  # Auto-assigned collections
        'template': template,
        'category': parsed.get('category', 'Gaming'),
        'metafield_mappings': metafield_mappings,  # Add metafield GID mappings
        # Add full component names for display
        'cpu_full': expanded_info.get('cpu_full', cpu),
        'ram_full': expanded_info.get('ram_full', ram),
        'gpu_full': expanded_info.get('gpu_full', gpu),
        'display_full': expanded_info.get('display_full', display),
        'storage_full': expanded_info.get('storage_full', storage)
    }
    
    return result

def extract_info_from_template(template: str) -> Dict[str, str]:
    """Extract info from template (supports iPhone, Galaxy, Laptop, and legacy systems)"""
    # Check if this is an iPhone template format
    if "iPhone" in template and "[" in template and "]" in template:
        return extract_info_from_iphone_template(template)
    
    # Check if this is a Galaxy template format
    if "Galaxy" in template and "[" in template and "]" in template:
        return extract_info_from_galaxy_template(template)
    
    # Check if this is a Laptop template format (has CPU specs like "i7-" or "Ryzen")
    if "[" in template and "]" in template and ("i7-" in template or "i5-" in template or "Ryzen" in template):
        return extract_info_from_laptop_template(template)
    
    # Legacy extraction logic for non-templated devices
    info = {
        "brand": "",
        "model": "",
        "storage": ""
    }
    
    if "iPhone" in template:
        info["brand"] = "iPhone"
        parts = template.split()
        if len(parts) >= 3:
            info["model"] = " ".join(parts[1:3])  # e.g., "15 Pro"
    elif "Samsung" in template:
        info["brand"] = "Samsung"
        if "Galaxy" in template:
            parts = template.split("Galaxy ")[1].split(" (")[0]
            info["model"] = f"Galaxy {parts.split(' ')[0]}"  # e.g., "Galaxy S24"
    elif "Google" in template:
        info["brand"] = "Google"
        if "Pixel" in template:
            parts = template.split("Pixel ")[1].split(" (")[0]
            info["model"] = f"Pixel {parts.split(' ')[0]}"  # e.g., "Pixel 8"
    
    # Extract storage
    for storage in STORAGE_OPTIONS:
        if storage in template:
            info["storage"] = storage
            break
    
    return info

# New functions for enhanced template system
def get_inclusion_mapping_options() -> List[str]:
    """Get available inclusion mapping options"""
    return list(INCLUSION_MAPPINGS.keys())

def get_inclusions_for_mapping(mapping_key: str) -> List[str]:
    """Get inclusions for a specific mapping key"""
    return INCLUSION_MAPPINGS.get(mapping_key, [])

def apply_inclusion_mapping(current_inclusions: List[str], mapping_key: str) -> List[str]:
    """Apply inclusion mapping to current selections (additive)
    
    Args:
        current_inclusions: Currently selected inclusions
        mapping_key: Inclusion mapping to apply
        
    Returns:
        Updated inclusions list (removes duplicates)
    """
    if not mapping_key or mapping_key not in INCLUSION_MAPPINGS:
        return current_inclusions
    
    new_inclusions = INCLUSION_MAPPINGS[mapping_key]
    combined = list(current_inclusions) + new_inclusions
    
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for item in combined:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result

def get_collections_for_brand(brand: str) -> List[str]:
    """Get auto-assigned collections for a brand"""
    collections = ['All Products']  # Always include
    
    if brand == 'iPhone':
        collections.append('iPhone')
    elif brand in ['Samsung', 'Google', 'OnePlus', 'Xiaomi', 'Oppo', 'Vivo', 'Huawei', 'Sony', 'LG']:
        collections.extend(['Android', brand])
    elif brand in ['ASUS', 'Dell', 'HP', 'Lenovo', 'MSI', 'Acer', 'Apple']:
        collections.extend(['Laptop', brand])
    
    return collections

def detect_template_brand(template: str) -> str:
    """Detect brand from template string"""
    if "iPhone" in template:
        return "iPhone"
    elif "Galaxy" in template:
        return "Samsung"
    elif "Pixel" in template:
        return "Google"
    elif "ASUS" in template:
        return "ASUS"
    elif "Dell" in template:
        return "Dell"
    elif "HP" in template:
        return "HP"
    elif "Lenovo" in template:
        return "Lenovo"
    elif "MSI" in template:
        return "MSI"
    else:
        return "Unknown"