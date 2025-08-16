"""
iPhone specifications database with complete model, storage, and color information.
Used for template generation and validation.
"""

from typing import Dict, List, NamedTuple
from dataclasses import dataclass

# iPhone Color GID Mappings - Updated with actual Shopify metaobject GIDs
IPHONE_COLOR_GIDS = {
    "Black": "gid://shopify/Metaobject/108876857493",
    "White": "gid://shopify/Metaobject/126394368149",
    "Blue": "gid://shopify/Metaobject/111343370389", 
    "Green": "gid://shopify/Metaobject/111343435925",
    "Space Gray": "gid://shopify/Metaobject/125795303573",
    "Silver": "gid://shopify/Metaobject/118603284629",
    "Gold": "gid://shopify/Metaobject/111343403157",
    "Pacific Blue": "gid://shopify/Metaobject/126233608341",
    "Graphite": "gid://shopify/Metaobject/127395233941",
    "Sierra Blue": "gid://shopify/Metaobject/127395135637",
    "Midnight": "gid://shopify/Metaobject/125799497877",
    "Starlight": "gid://shopify/Metaobject/127394644117",
    "Space Black": "gid://shopify/Metaobject/126919508117",
    "Midnight Green": "gid://shopify/Metaobject/127395266709",
    "Black Titanium": "gid://shopify/Metaobject/118601613461",
    "White Titanium": "gid://shopify/Metaobject/118601580693",
    "Natural Titanium": "gid://shopify/Metaobject/118601449621",
    "Desert Titanium": "gid://shopify/Metaobject/118601547925",
    "Blue Titanium": "gid://shopify/Metaobject/126415896725",
    "(PRODUCT)RED": "gid://shopify/Metaobject/127394676885",
    "Pink": "gid://shopify/Metaobject/126394400917",
    "Yellow": "gid://shopify/Metaobject/111476342933",
    "Purple": "gid://shopify/Metaobject/127394709653",
    "Coral": "gid://shopify/Metaobject/126394400917",
    "Deep Purple": "gid://shopify/Metaobject/126919573653",
    "Red": "gid://shopify/Metaobject/127394676885",
    "Teal": "gid://shopify/Metaobject/126393909397",
    "Ultramarine": "gid://shopify/Metaobject/126394073237",
}

@dataclass
class iPhoneSpec:
    """iPhone model specification"""
    model: str
    storage_options: List[str]
    colors: List[str]
    has_5g: bool
    series: str
    year: int

# Complete iPhone specifications database
IPHONE_SPECS: Dict[str, iPhoneSpec] = {
    # iPhone 16 Series (2024) - All support 5G
    "iPhone 16": iPhoneSpec(
        model="iPhone 16",
        storage_options=["128GB", "256GB", "512GB"],
        colors=["Black", "White", "Pink", "Teal", "Ultramarine"],
        has_5g=True,
        series="iPhone 16",
        year=2024
    ),
    "iPhone 16 Plus": iPhoneSpec(
        model="iPhone 16 Plus",
        storage_options=["128GB", "256GB", "512GB"],
        colors=["Black", "White", "Pink", "Teal", "Ultramarine"],
        has_5g=True,
        series="iPhone 16",
        year=2024
    ),
    "iPhone 16 Pro": iPhoneSpec(
        model="iPhone 16 Pro",
        storage_options=["128GB", "256GB", "512GB", "1TB"],
        colors=["Black Titanium", "White Titanium", "Natural Titanium", "Desert Titanium"],
        has_5g=True,
        series="iPhone 16",
        year=2024
    ),
    "iPhone 16 Pro Max": iPhoneSpec(
        model="iPhone 16 Pro Max",
        storage_options=["256GB", "512GB", "1TB"],  # No 128GB option
        colors=["Black Titanium", "White Titanium", "Natural Titanium", "Desert Titanium"],
        has_5g=True,
        series="iPhone 16",
        year=2024
    ),
    
    # iPhone 15 Series (2023) - All support 5G
    "iPhone 15": iPhoneSpec(
        model="iPhone 15",
        storage_options=["128GB", "256GB", "512GB"],
        colors=["Black", "Blue", "Green", "Yellow", "Pink"],
        has_5g=True,
        series="iPhone 15",
        year=2023
    ),
    "iPhone 15 Plus": iPhoneSpec(
        model="iPhone 15 Plus",
        storage_options=["128GB", "256GB", "512GB"],
        colors=["Black", "Blue", "Green", "Yellow", "Pink"],
        has_5g=True,
        series="iPhone 15",
        year=2023
    ),
    "iPhone 15 Pro": iPhoneSpec(
        model="iPhone 15 Pro",
        storage_options=["128GB", "256GB", "512GB", "1TB"],
        colors=["Black Titanium", "White Titanium", "Blue Titanium", "Natural Titanium"],
        has_5g=True,
        series="iPhone 15",
        year=2023
    ),
    "iPhone 15 Pro Max": iPhoneSpec(
        model="iPhone 15 Pro Max",
        storage_options=["256GB", "512GB", "1TB"],  # No 128GB option
        colors=["Black Titanium", "White Titanium", "Blue Titanium", "Natural Titanium"],
        has_5g=True,
        series="iPhone 15",
        year=2023
    ),
    
    # iPhone 14 Series (2022) - All support 5G
    "iPhone 14": iPhoneSpec(
        model="iPhone 14",
        storage_options=["128GB", "256GB", "512GB"],
        colors=["Blue", "Purple", "Midnight", "Starlight", "(PRODUCT)RED"],
        has_5g=True,
        series="iPhone 14",
        year=2022
    ),
    "iPhone 14 Plus": iPhoneSpec(
        model="iPhone 14 Plus",
        storage_options=["128GB", "256GB", "512GB"],
        colors=["Blue", "Purple", "Midnight", "Starlight", "(PRODUCT)RED"],
        has_5g=True,
        series="iPhone 14",
        year=2022
    ),
    "iPhone 14 Pro": iPhoneSpec(
        model="iPhone 14 Pro",
        storage_options=["128GB", "256GB", "512GB", "1TB"],
        colors=["Deep Purple", "Gold", "Silver", "Space Black"],
        has_5g=True,
        series="iPhone 14",
        year=2022
    ),
    "iPhone 14 Pro Max": iPhoneSpec(
        model="iPhone 14 Pro Max",
        storage_options=["128GB", "256GB", "512GB", "1TB"],
        colors=["Deep Purple", "Gold", "Silver", "Space Black"],
        has_5g=True,
        series="iPhone 14",
        year=2022
    ),
    
    # iPhone 13 Series (2021) - All support 5G
    "iPhone 13 mini": iPhoneSpec(
        model="iPhone 13 mini",
        storage_options=["128GB", "256GB", "512GB"],
        colors=["Pink", "Blue", "Midnight", "Starlight", "(PRODUCT)RED"],
        has_5g=True,
        series="iPhone 13",
        year=2021
    ),
    "iPhone 13": iPhoneSpec(
        model="iPhone 13",
        storage_options=["128GB", "256GB", "512GB"],
        colors=["Pink", "Blue", "Midnight", "Starlight", "(PRODUCT)RED"],
        has_5g=True,
        series="iPhone 13",
        year=2021
    ),
    "iPhone 13 Pro": iPhoneSpec(
        model="iPhone 13 Pro",
        storage_options=["128GB", "256GB", "512GB", "1TB"],
        colors=["Sierra Blue", "Gold", "Silver", "Graphite"],
        has_5g=True,
        series="iPhone 13",
        year=2021
    ),
    "iPhone 13 Pro Max": iPhoneSpec(
        model="iPhone 13 Pro Max",
        storage_options=["128GB", "256GB", "512GB", "1TB"],
        colors=["Sierra Blue", "Gold", "Silver", "Graphite"],
        has_5g=True,
        series="iPhone 13",
        year=2021
    ),
    
    # iPhone 12 Series (2020) - All support 5G (First 5G iPhones)
    "iPhone 12 mini": iPhoneSpec(
        model="iPhone 12 mini",
        storage_options=["64GB", "128GB", "256GB"],
        colors=["Black", "White", "Red", "Green", "Blue", "Purple"],
        has_5g=True,
        series="iPhone 12",
        year=2020
    ),
    "iPhone 12": iPhoneSpec(
        model="iPhone 12",
        storage_options=["64GB", "128GB", "256GB"],
        colors=["Black", "White", "Red", "Green", "Blue", "Purple"],
        has_5g=True,
        series="iPhone 12",
        year=2020
    ),
    "iPhone 12 Pro": iPhoneSpec(
        model="iPhone 12 Pro",
        storage_options=["128GB", "256GB", "512GB"],
        colors=["Graphite", "Silver", "Gold", "Pacific Blue"],
        has_5g=True,
        series="iPhone 12",
        year=2020
    ),
    "iPhone 12 Pro Max": iPhoneSpec(
        model="iPhone 12 Pro Max",
        storage_options=["128GB", "256GB", "512GB"],
        colors=["Graphite", "Silver", "Gold", "Pacific Blue"],
        has_5g=True,
        series="iPhone 12",
        year=2020
    ),
    
    # iPhone 11 Series (2019) - NO 5G support (Last 4G-only iPhones)
    "iPhone 11": iPhoneSpec(
        model="iPhone 11",
        storage_options=["64GB", "128GB", "256GB"],
        colors=["Black", "Green", "Yellow", "Purple", "White", "(PRODUCT)RED"],
        has_5g=False,
        series="iPhone 11",
        year=2019
    ),
    "iPhone 11 Pro": iPhoneSpec(
        model="iPhone 11 Pro",
        storage_options=["64GB", "256GB", "512GB"],  # No 128GB option
        colors=["Midnight Green", "Space Gray", "Silver", "Gold"],
        has_5g=False,
        series="iPhone 11",
        year=2019
    ),
    "iPhone 11 Pro Max": iPhoneSpec(
        model="iPhone 11 Pro Max",
        storage_options=["64GB", "256GB", "512GB"],  # No 128GB option
        colors=["Midnight Green", "Space Gray", "Silver", "Gold"],
        has_5g=False,
        series="iPhone 11",
        year=2019
    ),
    
    # Legacy Models (Pre-2019) - NO 5G support
    "iPhone XS": iPhoneSpec(
        model="iPhone XS",
        storage_options=["64GB", "256GB", "512GB"],
        colors=["Space Gray", "Silver", "Gold"],
        has_5g=False,
        series="iPhone XS",
        year=2018
    ),
    "iPhone XS Max": iPhoneSpec(
        model="iPhone XS Max",
        storage_options=["64GB", "256GB", "512GB"],
        colors=["Space Gray", "Silver", "Gold"],
        has_5g=False,
        series="iPhone XS",
        year=2018
    ),
    "iPhone XR": iPhoneSpec(
        model="iPhone XR",
        storage_options=["64GB", "128GB", "256GB"],
        colors=["Black", "White", "Red", "Yellow", "Blue", "Coral"],
        has_5g=False,
        series="iPhone XR",
        year=2018
    )
}

def get_iphone_spec(model: str) -> iPhoneSpec:
    """Get iPhone specifications for a specific model"""
    return IPHONE_SPECS.get(model)

def is_5g_capable(model: str) -> bool:
    """Check if iPhone model supports 5G"""
    spec = get_iphone_spec(model)
    return spec.has_5g if spec else False

def get_valid_storage_options(model: str) -> List[str]:
    """Get valid storage options for iPhone model"""
    spec = get_iphone_spec(model)
    return spec.storage_options if spec else []

def get_valid_colors(model: str) -> List[str]:
    """Get valid color options for iPhone model"""
    spec = get_iphone_spec(model)
    return spec.colors if spec else []

def validate_combination(model: str, storage: str, color: str) -> bool:
    """Validate if model/storage/color combination is valid"""
    spec = get_iphone_spec(model)
    if not spec:
        return False
    
    return (storage in spec.storage_options and 
            color in spec.colors)

def get_all_models() -> List[str]:
    """Get list of all iPhone models"""
    return list(IPHONE_SPECS.keys())

def get_models_by_series(series: str) -> List[str]:
    """Get all models in a specific iPhone series"""
    return [model for model, spec in IPHONE_SPECS.items() 
            if spec.series == series]

def get_all_series() -> List[str]:
    """Get list of all iPhone series"""
    series_list = list(set(spec.series for spec in IPHONE_SPECS.values()))
    # Sort by year (newest first)
    return sorted(series_list, 
                 key=lambda s: IPHONE_SPECS[get_models_by_series(s)[0]].year, 
                 reverse=True)

def generate_all_templates() -> List[str]:
    """Generate all valid iPhone templates with correct inclusion presets"""
    templates = []
    
    for model, spec in IPHONE_SPECS.items():
        # Get appropriate inclusion presets for this model
        inclusion_presets = get_inclusion_presets_for_model(model)
        
        for storage in spec.storage_options:
            for color in spec.colors:
                for inclusion in inclusion_presets:
                    template = f"{model} {storage} [{color}] [{inclusion}]"
                    templates.append(template)
    return sorted(templates)

def parse_template(template: str) -> Dict[str, str]:
    """Parse iPhone template to extract model, storage, color, and inclusion preset
    
    Args:
        template: Format like "iPhone 15 Pro Max 256GB [Desert Titanium] [No box]"
        
    Returns:
        Dict with 'model', 'storage', 'color', 'inclusion_preset' keys
    """
    try:
        # Count brackets to determine format
        bracket_count = template.count('[')
        
        if bracket_count == 0:
            return {}
        elif bracket_count == 1:
            # Legacy format: "iPhone 15 Pro Max 256GB [Desert Titanium]"
            if '[' not in template or ']' not in template:
                return {}
            
            main_part, color_part = template.split('[', 1)
            color = color_part.rstrip(']').strip()
            inclusion_preset = ""
        else:
            # New format: "iPhone 15 Pro Max 256GB [Desert Titanium] [No box]"
            # Use regex to properly extract bracketed content
            import re
            bracket_pattern = r'\[([^\]]+)\]'
            matches = re.findall(bracket_pattern, template)
            
            if len(matches) < 2:
                return {}
            
            main_part = re.sub(bracket_pattern, '', template).strip()
            color = matches[0].strip()
            inclusion_preset = matches[1].strip()
        
        # Extract storage (last part before the first bracket)
        main_parts = main_part.strip().split()
        if not main_parts:
            return {}
        
        # Find storage (should be like "256GB")
        storage = None
        storage_index = -1
        for i, part in enumerate(main_parts):
            if part.endswith('GB') or part.endswith('TB'):
                storage = part
                storage_index = i
                break
        
        if storage is None:
            return {}
        
        # Model is everything before the storage
        model_parts = main_parts[:storage_index]
        model = ' '.join(model_parts)
        
        result = {
            'model': model,
            'storage': storage, 
            'color': color
        }
        
        if inclusion_preset:
            result['inclusion_preset'] = inclusion_preset
        
        return result
    except Exception:
        return {}

def generate_product_title(model: str, storage: str, sim_variant: str = "SIM Free") -> str:
    """Generate product title with correct 5G designation
    
    Args:
        model: iPhone model (e.g., "iPhone 15 Pro Max")
        storage: Storage capacity (e.g., "256GB")
        sim_variant: SIM variant type (default: "SIM Free")
        
    Returns:
        Complete product title with 5G if supported
    """
    spec = get_iphone_spec(model)
    if not spec:
        return f"{model} {storage} ({sim_variant})"
    
    # Add 5G for iPhone 12 and newer
    if spec.has_5g:
        return f"{model} 5G {storage} ({sim_variant})"
    else:
        return f"{model} {storage} ({sim_variant})"

# Template search and filtering functions
def search_templates(search_term: str) -> List[str]:
    """Search templates by model name"""
    if not search_term:
        return generate_all_templates()
    
    search_lower = search_term.lower()
    templates = generate_all_templates()
    
    return [template for template in templates 
            if search_lower in template.lower()]

def get_templates_by_series(series: str) -> List[str]:
    """Get all templates for a specific iPhone series"""
    models = get_models_by_series(series)
    templates = []
    
    for model in models:
        spec = IPHONE_SPECS[model]
        inclusion_presets = get_inclusion_presets_for_model(model)
        
        for storage in spec.storage_options:
            for color in spec.colors:
                for inclusion in inclusion_presets:
                    template = f"{model} {storage} [{color}] [{inclusion}]"
                    templates.append(template)
    
    return sorted(templates)

# Color mapping for metafields (to be populated with actual Shopify metaobject GIDs)
COLOR_METAFIELD_MAPPINGS = {
    # iPhone Standard Colors - Updated with correct GIDs from colors.json
    'Black': 'gid://shopify/Metaobject/108876857493',
    'White': 'gid://shopify/Metaobject/126394368149', 
    'Pink': 'gid://shopify/Metaobject/126394400917',
    'Teal': 'gid://shopify/Metaobject/126393909397',
    'Ultramarine': 'gid://shopify/Metaobject/126394073237',
    
    # Titanium Colors (Pro Models) - Updated with correct GIDs
    'Black Titanium': 'gid://shopify/Metaobject/118601613461',
    'White Titanium': 'gid://shopify/Metaobject/118601580693',
    'Natural Titanium': 'gid://shopify/Metaobject/118601449621',
    'Desert Titanium': 'gid://shopify/Metaobject/118601547925',
    'Blue Titanium': 'gid://shopify/Metaobject/126415896725',
    
    # Standard Colors - Updated with correct GIDs
    'Blue': 'gid://shopify/Metaobject/111343370389',
    'Green': 'gid://shopify/Metaobject/111343435925',
    'Yellow': 'gid://shopify/Metaobject/111476342933',
    'Purple': 'gid://shopify/Metaobject/127394709653',
    'Midnight': 'gid://shopify/Metaobject/125799497877',
    'Starlight': 'gid://shopify/Metaobject/127394644117',
    '(PRODUCT)RED': 'gid://shopify/Metaobject/127394676885',
    'Red': 'gid://shopify/Metaobject/127394676885',
    
    # Pro Colors - Updated with correct GIDs
    'Deep Purple': 'gid://shopify/Metaobject/126919573653',
    'Gold': 'gid://shopify/Metaobject/111343403157',
    'Silver': 'gid://shopify/Metaobject/118603284629',
    'Space Black': 'gid://shopify/Metaobject/126919508117',
    'Sierra Blue': 'gid://shopify/Metaobject/127395135637',
    'Graphite': 'gid://shopify/Metaobject/127395233941',
    'Pacific Blue': 'gid://shopify/Metaobject/126233608341',
    
    # iPhone 11 and older colors - Updated with correct GIDs
    'Midnight Green': 'gid://shopify/Metaobject/127395266709',
    'Space Gray': 'gid://shopify/Metaobject/125795303573',
    'Coral': 'gid://shopify/Metaobject/126394400917'
}

def get_color_metafield_gid(color: str) -> str:
    """Get Shopify metaobject GID for color"""
    return COLOR_METAFIELD_MAPPINGS.get(color, '')

def get_inclusion_presets_for_model(model: str) -> List[str]:
    """Get appropriate inclusion presets for iPhone model based on charger inclusion history
    
    iPhone 11 and older: Included charger (Full set charger available)
    iPhone 12 and newer: No charger included (only Full set cable available)
    """
    spec = get_iphone_spec(model)
    if not spec:
        return ["No box", "With box"]
    
    # iPhone 12 (2020) was first to exclude charger
    if spec.year >= 2020 and model != "iPhone 11":  # iPhone 11 is 2019
        # iPhone 12+ only get cable option since no charger included
        return ["No box", "With box", "Full set cable"]
    else:
        # iPhone 11 and older get charger option since charger was included
        return ["No box", "With box", "Full set cable", "Full set (charger)"]