"""
Samsung Galaxy specifications database (2021 and above) with model, storage, RAM, color, 5G, and box inclusion info.
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class GalaxySpec:
    """Samsung Galaxy model specification"""
    model: str
    year: int
    has_5g: bool
    storage_options: List[str]
    ram_options: List[str]
    colors: List[str]
    product_inclusions: List[str]
    series: str

# Samsung Galaxy specifications database (2021+)
GALAXY_SPECS: Dict[str, GalaxySpec] = {
    # S Series 2025
    "Galaxy S25": GalaxySpec(
        model="Galaxy S25",
        year=2025,
        has_5g=True,
        storage_options=["128GB", "256GB", "512GB"],
        ram_options=["12GB"],
        colors=["Icy Blue", "Navy", "Silver Shadow"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S25"
    ),
    "Galaxy S25+": GalaxySpec(
        model="Galaxy S25+",
        year=2025,
        has_5g=True,
        storage_options=["256GB", "512GB"],
        ram_options=["12GB"],
        colors=["Icy Blue", "Navy", "Silver Shadow"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S25+"
    ),
    "Galaxy S25 Ultra": GalaxySpec(
        model="Galaxy S25 Ultra",
        year=2025,
        has_5g=True,
        storage_options=["256GB", "512GB", "1TB"],
        ram_options=["12GB"],
        colors=["Titanium Silver Blue", "Titanium Black", "Titanium White Silver", "Titanium Gray"],
        product_inclusions=["USB-C cable", "No adapter", "S Pen"],
        series="S25 Ultra"
    ),
    
    # S Series 2024
    "Galaxy S24": GalaxySpec(
        model="Galaxy S24",
        year=2024,
        has_5g=True,
        storage_options=["128GB", "256GB", "512GB"],
        ram_options=["8GB"],
        colors=["Onyx Black", "Marble Grey", "Cobalt Violet"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S24"
    ),
    "Galaxy S24 Ultra": GalaxySpec(
        model="Galaxy S24 Ultra",
        year=2024,
        has_5g=True,
        storage_options=["256GB", "512GB", "1TB"],
        ram_options=["12GB"],
        colors=["Titanium Black", "Titanium Gray", "Titanium Violet"],
        product_inclusions=["USB-C cable", "No adapter", "S Pen"],
        series="S24 Ultra"
    ),
    "Galaxy S24 FE": GalaxySpec(
        model="Galaxy S24 FE",
        year=2024,
        has_5g=True,
        storage_options=["128GB", "256GB", "512GB"],
        ram_options=["8GB"],
        colors=["Blue", "Graphite", "Gray", "Mint", "Yellow"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S24 FE"
    ),
    
    # S Series 2023
    "Galaxy S23": GalaxySpec(
        model="Galaxy S23",
        year=2023,
        has_5g=True,
        storage_options=["128GB", "256GB", "512GB"],
        ram_options=["8GB"],
        colors=["Phantom Black", "Cream", "Green", "Lavender", "Graphite", "Lime"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S23"
    ),
    "Galaxy S23+": GalaxySpec(
        model="Galaxy S23+",
        year=2023,
        has_5g=True,
        storage_options=["256GB", "512GB"],
        ram_options=["8GB"],
        colors=["Phantom Black", "Green", "Cream", "Lavender", "Graphite", "Sky Blue", "Lime"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S23+"
    ),
    "Galaxy S23 Ultra": GalaxySpec(
        model="Galaxy S23 Ultra",
        year=2023,
        has_5g=True,
        storage_options=["256GB", "512GB", "1TB"],
        ram_options=["8GB", "12GB"],
        colors=["Phantom Black", "Green", "Cream", "Lavender", "Graphite", "Sky Blue", "Lime", "Red", "BMW M Edition"],
        product_inclusions=["USB-C cable", "No adapter", "S Pen"],
        series="S23 Ultra"
    ),
    "Galaxy S23 FE": GalaxySpec(
        model="Galaxy S23 FE",
        year=2023,
        has_5g=True,
        storage_options=["128GB", "256GB"],
        ram_options=["8GB"],
        colors=["Mint", "Graphite", "Cream", "Purple", "Indigo", "Tangerine"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S23 FE"
    ),
    
    # S Series 2022
    "Galaxy S22": GalaxySpec(
        model="Galaxy S22",
        year=2022,
        has_5g=True,
        storage_options=["128GB", "256GB"],
        ram_options=["8GB"],
        colors=["Phantom Black", "White", "Pink Gold", "Green", "Graphite", "Sky Blue", "Violet", "Cream", "Bora Purple"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S22"
    ),
    "Galaxy S22+": GalaxySpec(
        model="Galaxy S22+",
        year=2022,
        has_5g=True,
        storage_options=["128GB", "256GB"],
        ram_options=["8GB"],
        colors=["Phantom Black", "White", "Pink Gold", "Green", "Graphite", "Sky Blue", "Violet", "Cream", "Bora Purple"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S22+"
    ),
    "Galaxy S22 Ultra": GalaxySpec(
        model="Galaxy S22 Ultra",
        year=2022,
        has_5g=True,
        storage_options=["128GB", "256GB", "512GB", "1TB"],
        ram_options=["8GB", "12GB"],
        colors=["Phantom Black", "White", "Burgundy", "Green", "Graphite", "Red", "Sky Blue", "Bora Purple"],
        product_inclusions=["USB-C cable", "No adapter", "S Pen"],
        series="S22 Ultra"
    ),
    
    # S Series 2021
    "Galaxy S21": GalaxySpec(
        model="Galaxy S21",
        year=2021,
        has_5g=True,
        storage_options=["128GB", "256GB"],
        ram_options=["8GB"],
        colors=["Phantom Gray", "Phantom White", "Phantom Violet", "Phantom Pink"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S21"
    ),
    "Galaxy S21+": GalaxySpec(
        model="Galaxy S21+",
        year=2021,
        has_5g=True,
        storage_options=["128GB", "256GB"],
        ram_options=["8GB"],
        colors=["Phantom Silver", "Phantom Black", "Phantom Violet"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S21+"
    ),
    "Galaxy S21 Ultra": GalaxySpec(
        model="Galaxy S21 Ultra",
        year=2021,
        has_5g=True,
        storage_options=["128GB", "256GB", "512GB"],
        ram_options=["12GB"],
        colors=["Phantom Black", "Phantom Silver", "Phantom Navy"],
        product_inclusions=["USB-C cable", "No adapter", "S Pen"],
        series="S21 Ultra"
    ),
    "Galaxy S21 FE": GalaxySpec(
        model="Galaxy S21 FE",
        year=2022,
        has_5g=True,
        storage_options=["128GB", "256GB"],
        ram_options=["6GB", "8GB"],
        colors=["White", "Graphite", "Lavender", "Olive"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="S21 FE"
    ),
    
    # A Series (Available in Japan)
    "Galaxy A55": GalaxySpec(
        model="Galaxy A55",
        year=2024,
        has_5g=True,
        storage_options=["128GB", "256GB"],
        ram_options=["8GB"],
        colors=["Awesome Navy", "Awesome Iceblue"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="A55"
    ),
    
    # Z Series (Foldables) 2025
    "Galaxy Z Fold7": GalaxySpec(
        model="Galaxy Z Fold7",
        year=2025,
        has_5g=True,
        storage_options=["256GB", "512GB", "1TB"],
        ram_options=["12GB"],
        colors=["Blue Shadow", "Silver Shadow", "Jet Black"],
        product_inclusions=["USB-C cable", "No adapter", "S Pen"],
        series="Z Fold7"
    ),
    "Galaxy Z Flip7": GalaxySpec(
        model="Galaxy Z Flip7",
        year=2025,
        has_5g=True,
        storage_options=["256GB", "512GB"],
        ram_options=["12GB"],
        colors=["Blue Shadow", "Jet Black"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="Z Flip7"
    ),
    
    # Z Series (Foldables) 2024
    "Galaxy Z Fold6": GalaxySpec(
        model="Galaxy Z Fold6",
        year=2024,
        has_5g=True,
        storage_options=["256GB", "512GB", "1TB"],
        ram_options=["12GB"],
        colors=["Navy", "Silver Shadow", "Pink", "Black", "White"],
        product_inclusions=["USB-C cable", "No adapter", "S Pen"],
        series="Z Fold6"
    ),
    "Galaxy Z Flip6": GalaxySpec(
        model="Galaxy Z Flip6",
        year=2024,
        has_5g=True,
        storage_options=["256GB", "512GB"],
        ram_options=["12GB"],
        colors=["Yellow", "Silver Shadow", "Mint", "Blue", "Black", "White", "Peach"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="Z Flip6"
    ),
    
    # Z Series (Foldables) 2023
    "Galaxy Z Fold5": GalaxySpec(
        model="Galaxy Z Fold5",
        year=2023,
        has_5g=True,
        storage_options=["256GB", "512GB", "1TB"],
        ram_options=["12GB"],
        colors=["Icy Blue", "Phantom Black", "Cream", "Gray", "Blue"],
        product_inclusions=["USB-C cable", "No adapter", "S Pen"],
        series="Z Fold5"
    ),
    "Galaxy Z Flip5": GalaxySpec(
        model="Galaxy Z Flip5",
        year=2023,
        has_5g=True,
        storage_options=["256GB", "512GB"],
        ram_options=["8GB"],
        colors=["Mint", "Graphite", "Cream", "Lavender", "Gray", "Blue", "Green", "Yellow"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="Z Flip5"
    ),
    
    # Z Series (Foldables) 2022
    "Galaxy Z Fold4": GalaxySpec(
        model="Galaxy Z Fold4",
        year=2022,
        has_5g=True,
        storage_options=["256GB", "512GB", "1TB"],
        ram_options=["12GB"],
        colors=["Graygreen", "Phantom Black", "Beige", "Burgundy"],
        product_inclusions=["USB-C cable", "No adapter", "S Pen"],
        series="Z Fold4"
    ),
    "Galaxy Z Flip4": GalaxySpec(
        model="Galaxy Z Flip4",
        year=2022,
        has_5g=True,
        storage_options=["128GB", "256GB", "512GB"],
        ram_options=["8GB"],
        colors=["Bora Purple", "Graphite", "Pink Gold", "Blue", "Yellow", "White"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="Z Flip4"
    ),
    
    # Z Series (Foldables) 2021
    "Galaxy Z Fold3": GalaxySpec(
        model="Galaxy Z Fold3",
        year=2021,
        has_5g=True,
        storage_options=["256GB", "512GB"],
        ram_options=["12GB"],
        colors=["Phantom Black", "Phantom Green", "Phantom Silver"],
        product_inclusions=["USB-C cable", "No adapter", "S Pen"],
        series="Z Fold3"
    ),
    "Galaxy Z Flip3": GalaxySpec(
        model="Galaxy Z Flip3",
        year=2021,
        has_5g=True,
        storage_options=["128GB", "256GB"],
        ram_options=["8GB"],
        colors=["Cream", "Green", "Lavender", "Phantom Black", "Gray", "White", "Pink", "Blue"],
        product_inclusions=["USB-C cable", "No adapter"],
        series="Z Flip3"
    ),
}

def get_galaxy_spec(model: str) -> GalaxySpec:
    """Get Samsung Galaxy specifications for a specific model"""
    return GALAXY_SPECS.get(model)

def is_5g_capable(model: str) -> bool:
    """Check if Samsung Galaxy model supports 5G"""
    spec = get_galaxy_spec(model)
    return spec.has_5g if spec else False

def get_valid_storage_options(model: str) -> List[str]:
    """Get valid storage options for Samsung Galaxy model"""
    spec = get_galaxy_spec(model)
    return spec.storage_options if spec else []

def get_valid_ram_options(model: str) -> List[str]:
    """Get valid RAM options for Samsung Galaxy model"""
    spec = get_galaxy_spec(model)
    return spec.ram_options if spec else []

def get_valid_colors(model: str) -> List[str]:
    """Get valid color options for Samsung Galaxy model"""
    spec = get_galaxy_spec(model)
    return spec.colors if spec else []

def get_product_inclusions(model: str) -> List[str]:
    """Get product inclusions for Samsung Galaxy model"""
    spec = get_galaxy_spec(model)
    return spec.product_inclusions if spec else []

def get_all_models() -> List[str]:
    """Get list of all Samsung Galaxy models"""
    return list(GALAXY_SPECS.keys())

def get_models_by_series(series: str) -> List[str]:
    """Get all models in a specific Samsung Galaxy series"""
    return [model for model, spec in GALAXY_SPECS.items() if spec.series == series]

def get_all_series() -> List[str]:
    """Get list of all Samsung Galaxy series"""
    series_list = list(set(spec.series for spec in GALAXY_SPECS.values()))
    return sorted(series_list, key=lambda s: GALAXY_SPECS[get_models_by_series(s)[0]].year, reverse=True)

# Template generation functions for Galaxy products

def format_ram_storage(model: str, ram: str, storage: str) -> str:
    """Format RAM/Storage based on available RAM options
    
    Returns:
        - "8GB/256GB" if model has multiple RAM options
        - "256GB" if model has only one RAM option
    """
    spec = get_galaxy_spec(model)
    if not spec:
        return storage
    
    # Ensure proper formatting (handle both GB and TB)
    ram_clean = ram if ram.endswith('GB') else ram + 'GB'
    
    if storage.endswith('TB'):
        storage_clean = storage
    elif storage.endswith('GB'):
        storage_clean = storage  
    else:
        storage_clean = storage + 'GB'
    
    if len(spec.ram_options) > 1:
        return f"{ram_clean}/{storage_clean}"
    else:
        return storage_clean

def get_default_ram(model: str) -> str:
    """Get default RAM size for a Galaxy model (highest available)"""
    spec = get_galaxy_spec(model)
    if not spec or not spec.ram_options:
        return "8GB"  # Default fallback
    
    # Return highest RAM option as default
    ram_values = [int(ram.replace('GB', '')) for ram in spec.ram_options]
    max_ram = max(ram_values)
    return f"{max_ram}GB"

def generate_galaxy_template(model: str, storage: str, ram: str, color: str, inclusion_preset: str) -> str:
    """Generate Galaxy template: 'Galaxy S24 Ultra 12/256 [Titanium Black] [No Box]'"""
    ram_storage = format_ram_storage(model, ram, storage)
    return f"{model} {ram_storage} [{color}] [{inclusion_preset}]"

def parse_galaxy_template(template: str) -> Dict[str, str]:
    """Parse Galaxy template to extract components
    
    Args:
        template: "Galaxy S24 Ultra 12/256 [Titanium Black] [No Box]"
        
    Returns:
        Dict with model, storage, ram, color, inclusion_preset
    """
    import re
    
    # Pattern to match Galaxy template format
    pattern = r'^(Galaxy\s+[\w\s+]+?)\s+(\d+(?:GB)?(?:/\d+(?:GB)?)?)\s+\[([^\]]+)\]\s+\[([^\]]+)\]$'
    match = re.match(pattern, template.strip())
    
    if not match:
        return {}
    
    model = match.group(1).strip()
    ram_storage = match.group(2).strip()
    color = match.group(3).strip()
    inclusion_preset = match.group(4).strip()
    
    # Parse RAM/Storage
    if '/' in ram_storage:
        # Format: "8GB/256GB" or "12/256" -> RAM: 8GB, Storage: 256GB
        ram_part, storage_part = ram_storage.split('/')
        ram = f"{ram_part}GB" if not ram_part.endswith('GB') else ram_part
        storage = f"{storage_part}GB" if not storage_part.endswith('GB') else storage_part
    else:
        # Format: "256GB" or "256" -> Single storage, get default RAM
        storage = f"{ram_storage}GB" if not ram_storage.endswith('GB') else ram_storage
        ram = get_default_ram(model)
    
    return {
        'model': model,
        'storage': storage,
        'ram': ram,
        'color': color,
        'inclusion_preset': inclusion_preset
    }

def generate_product_title(model: str, storage: str, sim_type: str = "SIM Free") -> str:
    """Generate Samsung product title: 'Samsung Galaxy S24 Ultra 5G 256GB (SIM Free)'"""
    # Add 5G designation for supported models
    has_5g = is_5g_capable(model)
    connectivity = " 5G" if has_5g else ""
    
    return f"Samsung {model}{connectivity} {storage} ({sim_type})"

def validate_galaxy_combination(model: str, storage: str, ram: str, color: str) -> bool:
    """Validate if the Galaxy model/storage/RAM/color combination is valid"""
    spec = get_galaxy_spec(model)
    if not spec:
        return False
    
    return (
        storage in spec.storage_options and
        ram in spec.ram_options and
        color in spec.colors
    )

def generate_all_galaxy_templates() -> List[str]:
    """Generate all valid Galaxy templates with inclusion presets"""
    templates = []
    
    # Common inclusion presets for Galaxy products
    inclusion_presets = [
        "No box",
        "With box", 
        "Full set cable",
        "Full set (charger)"
    ]
    
    for model, spec in GALAXY_SPECS.items():
        for storage in spec.storage_options:
            for ram in spec.ram_options:
                for color in spec.colors:
                    for preset in inclusion_presets:
                        template = generate_galaxy_template(model, storage, ram, color, preset)
                        templates.append(template)
    
    return sorted(templates)

def search_galaxy_templates(search_term: str) -> List[str]:
    """Search Galaxy templates by term with enhanced matching for RAM/Storage patterns"""
    if not search_term:
        return generate_all_galaxy_templates()
    
    all_templates = generate_all_galaxy_templates()
    search_lower = search_term.lower()
    
    # Enhanced search: normalize search term to handle "12 256" format
    import re
    
    # Extract RAM/Storage pattern like "12 256" and convert to searchable formats
    ram_storage_pattern = re.search(r'(\d+)\s+(\d+)', search_term)
    
    matching_templates = []
    
    for template in all_templates:
        template_lower = template.lower()
        
        # Basic text matching
        if search_lower in template_lower:
            matching_templates.append(template)
            continue
            
        # Enhanced RAM/Storage matching
        if ram_storage_pattern:
            ram_val = ram_storage_pattern.group(1)
            storage_val = ram_storage_pattern.group(2)
            
            # Check for various RAM/Storage formats in template:
            # "12GB/256GB", "12/256", "256GB" (single RAM)
            patterns_to_check = [
                f"{ram_val}gb/{storage_val}gb",
                f"{ram_val}/{storage_val}",
                f"{storage_val}gb"  # For single RAM models
            ]
            
            if any(pattern in template_lower for pattern in patterns_to_check):
                matching_templates.append(template)
    
    return matching_templates

def get_galaxy_templates_by_series(series: str) -> List[str]:
    """Get Galaxy templates filtered by series"""
    models_in_series = get_models_by_series(series)
    templates = []
    
    inclusion_presets = ["No box", "With box", "Full set cable", "Full set (charger)"]
    
    for model in models_in_series:
        spec = get_galaxy_spec(model)
        if spec:
            for storage in spec.storage_options:
                for ram in spec.ram_options:
                    for color in spec.colors:
                        for preset in inclusion_presets:
                            template = generate_galaxy_template(model, storage, ram, color, preset)
                            templates.append(template)
    
    return sorted(templates) 