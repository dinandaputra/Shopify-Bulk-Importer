"""
Master data configuration for dropdown options and templates
"""

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

# Title templates for quick entry
TITLE_TEMPLATES = {
    "iphone": [
        "iPhone 15 Pro Max {storage} (SIM Free)",
        "iPhone 15 Pro {storage} (SIM Free)",
        "iPhone 15 {storage} (SIM Free)",
        "iPhone 14 Pro Max {storage} (SIM Free)",
        "iPhone 14 Pro {storage} (SIM Free)",
        "iPhone 14 {storage} (SIM Free)",
        "iPhone 13 Pro Max {storage} (SIM Free)",
        "iPhone 13 Pro {storage} (SIM Free)",
        "iPhone 13 {storage} (SIM Free)",
        "iPhone 12 Pro Max {storage} (SIM Free)",
        "iPhone 12 Pro {storage} (SIM Free)",
        "iPhone 12 {storage} (SIM Free)",
    ],
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

def get_title_suggestions(search_term: str) -> list:
    """Get title suggestions based on search term"""
    if not search_term:
        return []
    
    search_lower = search_term.lower()
    suggestions = []
    
    for brand_key, templates in TITLE_TEMPLATES.items():
        if brand_key in search_lower or search_lower in brand_key:
            for template in templates:
                for storage in STORAGE_OPTIONS:
                    suggestions.append(template.format(storage=storage))
    
    return suggestions[:10]  # Limit to 10 suggestions

def extract_info_from_template(title: str) -> dict:
    """Extract brand, model, storage from title template"""
    info = {
        "brand": "",
        "model": "",
        "storage": ""
    }
    
    # Simple extraction logic
    if "iPhone" in title:
        info["brand"] = "iPhone"
        parts = title.split()
        if len(parts) >= 3:
            info["model"] = " ".join(parts[1:3])  # e.g., "15 Pro"
    elif "Samsung" in title:
        info["brand"] = "Samsung"
        if "Galaxy" in title:
            parts = title.split("Galaxy ")[1].split(" (")[0]
            info["model"] = f"Galaxy {parts.split(' ')[0]}"  # e.g., "Galaxy S24"
    elif "Google" in title:
        info["brand"] = "Google"
        if "Pixel" in title:
            parts = title.split("Pixel ")[1].split(" (")[0]
            info["model"] = f"Pixel {parts.split(' ')[0]}"  # e.g., "Pixel 8"
    
    # Extract storage
    for storage in STORAGE_OPTIONS:
        if storage in title:
            info["storage"] = storage
            break
    
    return info