#!/usr/bin/env python3
"""
Extract Laptop Model Data from config/laptop_specs.py to Per-Brand JSON Files

This script extracts laptop model data from the LAPTOP_SPECS dictionary in config/laptop_specs.py
and converts it to per-brand JSON files with the required structure for the laptop scalability refactor.

Task 1.4 from LAPTOP_SCALABILITY_REFACTOR_PLAN.md

Output Files:
- data/products/laptops/asus.json
- data/products/laptops/dell.json  
- data/products/laptops/hp.json
- data/products/laptops/lenovo.json
- data/products/laptops/msi.json
- data/products/laptops/brands_index.json

JSON Structure:
{
  "brand": "ASUS",
  "models": {
    "MODEL_KEY": {
      "display_name": "Display Name",
      "series": "Series Name", 
      "year": 2023,
      "category": "Gaming",
      "configurations": [{
        "cpu": "Full CPU name",
        "ram": "16GB DDR4",
        "vga": "Full VGA name", 
        "gpu": "Full GPU name",
        "display": "Full display name",
        "storage": "512GB SSD",
        "os": "Windows 11",
        "keyboard_layout": "US - International Keyboard",
        "keyboard_backlight": "RGB Backlight"
      }],
      "colors": ["Color1", "Color2"]
    }
  }
}

Requirements:
- Use FULL component names (not abbreviations) to match metaobject mappings
- Preserve all existing laptop model data
- Group models by brand accurately
- Handle multiple configurations per model
- Ensure all colors are preserved
- Add metadata fields (display_name, series, year, category)
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import laptop specs data
from config.laptop_specs import LAPTOP_SPECS, STANDARDIZED_COMPONENTS, CPU_TO_INTEGRATED_GRAPHICS

def expand_component_to_full_name(component_type: str, abbreviated_name: str) -> str:
    """Convert abbreviated component name to full name for metaobject matching"""
    if component_type in STANDARDIZED_COMPONENTS:
        return STANDARDIZED_COMPONENTS[component_type].get(abbreviated_name, abbreviated_name)
    return abbreviated_name

def get_integrated_graphics_for_cpu(cpu: str) -> str:
    """Get integrated graphics for a CPU using the mapping"""
    return CPU_TO_INTEGRATED_GRAPHICS.get(cpu, "")

def convert_laptop_configuration(config, cpu_abbreviated: str) -> Dict[str, Any]:
    """Convert LaptopConfiguration to JSON format with full component names"""
    
    # Get full component names using standardized mappings
    cpu_full = expand_component_to_full_name('cpu', cpu_abbreviated)
    ram_full = expand_component_to_full_name('ram', config.ram)
    storage_full = expand_component_to_full_name('storage', config.storage)
    display_full = expand_component_to_full_name('display', config.display)
    
    # Handle GPU vs integrated graphics properly
    gpu_full = expand_component_to_full_name('gpu', config.gpu)
    
    # Determine if this is integrated or dedicated graphics
    integrated_keywords = ['Intel Iris', 'Intel UHD', 'Intel HD', 'AMD Radeon Graphics', 'Apple GPU', 'Integrated']
    is_integrated_gpu = any(keyword in gpu_full for keyword in integrated_keywords)
    
    if is_integrated_gpu:
        # If GPU field contains integrated graphics, use it for gpu field and clear vga
        vga_full = ""
        gpu_final = gpu_full
        integrated_graphics = gpu_full
    else:
        # If GPU field contains dedicated graphics, use it for vga field and detect integrated graphics from CPU
        vga_full = gpu_full
        gpu_final = get_integrated_graphics_for_cpu(cpu_abbreviated) or "Intel UHD Graphics"
        integrated_graphics = gpu_final
    
    # Format keyboard layout and backlight to match expected format
    keyboard_layout_formatted = config.keyboard_layout
    if keyboard_layout_formatted == "US":
        keyboard_layout_formatted = "US - International Keyboard"
    
    keyboard_backlight_formatted = config.keyboard_backlight
    if keyboard_backlight_formatted == "RGB":
        keyboard_backlight_formatted = "RGB Backlight"
    elif keyboard_backlight_formatted == "Yes":
        keyboard_backlight_formatted = "Backlit"
    elif keyboard_backlight_formatted == "No":
        keyboard_backlight_formatted = "Non-backlit"
    elif keyboard_backlight_formatted in ["White", "Blue", "Green", "Red"]:
        keyboard_backlight_formatted = f"{keyboard_backlight_formatted} Backlight"
    
    return {
        "cpu": cpu_full,
        "ram": ram_full,
        "vga": vga_full,  # Dedicated graphics (RTX 4060, etc.) or empty for integrated-only
        "gpu": gpu_final,  # Integrated graphics or the actual GPU for integrated-only systems
        "display": display_full,
        "storage": storage_full,
        "os": config.os,
        "keyboard_layout": keyboard_layout_formatted,
        "keyboard_backlight": keyboard_backlight_formatted
    }

def convert_laptop_spec_to_json(model_key: str, spec) -> Dict[str, Any]:
    """Convert LaptopSpec to JSON format"""
    
    # Generate display name from model (remove brand prefix for cleaner display)
    display_name = spec.model
    if spec.base_model != model_key:
        # If base_model differs from key, use it for more specificity
        display_name = spec.base_model.replace(f"{spec.brand} ", "")
    
    # Convert all configurations
    configurations = []
    for config in spec.configurations:
        config_json = convert_laptop_configuration(config, config.cpu)
        configurations.append(config_json)
    
    return {
        "display_name": display_name,
        "series": spec.series,
        "year": spec.year,
        "category": spec.category,
        "configurations": configurations,
        "colors": spec.colors
    }

def extract_laptop_data_by_brand() -> Dict[str, Dict[str, Any]]:
    """Extract and group laptop data by brand"""
    
    brands_data = defaultdict(lambda: {"brand": "", "models": {}})
    
    for model_key, spec in LAPTOP_SPECS.items():
        brand = spec.brand
        
        # Set brand name if not set
        if not brands_data[brand]["brand"]:
            brands_data[brand]["brand"] = brand
        
        # Convert spec to JSON format
        model_json = convert_laptop_spec_to_json(model_key, spec)
        brands_data[brand]["models"][model_key] = model_json
    
    return dict(brands_data)

def save_brand_files(brands_data: Dict[str, Dict[str, Any]], output_dir: Path) -> None:
    """Save per-brand JSON files"""
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    brand_mapping = {
        "ASUS": "asus.json",
        "Dell": "dell.json", 
        "HP": "hp.json",
        "Lenovo": "lenovo.json",
        "MSI": "msi.json"
    }
    
    for brand, filename in brand_mapping.items():
        if brand in brands_data:
            file_path = output_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(brands_data[brand], f, indent=2, ensure_ascii=False)
            print(f"✅ Created {filename} with {len(brands_data[brand]['models'])} models")
        else:
            print(f"⚠️  No data found for brand: {brand}")

def create_brands_index(brands_data: Dict[str, Dict[str, Any]], output_dir: Path) -> None:
    """Create brands_index.json for brand enumeration"""
    
    brands_index = {
        "brands": []
    }
    
    for brand, data in brands_data.items():
        model_count = len(data["models"])
        brands_index["brands"].append({
            "name": brand,
            "model_count": model_count,
            "filename": f"{brand.lower()}.json"
        })
    
    # Sort brands alphabetically
    brands_index["brands"].sort(key=lambda x: x["name"])
    
    index_file = output_dir / "brands_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(brands_index, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created brands_index.json with {len(brands_index['brands'])} brands")

def validate_extraction(brands_data: Dict[str, Dict[str, Any]]) -> None:
    """Validate the extracted data for completeness and integrity"""
    
    print("\n📊 Data Extraction Validation:")
    print("=" * 50)
    
    total_models = len(LAPTOP_SPECS)
    extracted_models = 0
    
    for brand, data in brands_data.items():
        model_count = len(data["models"])
        extracted_models += model_count
        
        # Count configurations and colors
        total_configs = 0
        total_colors = 0
        
        for model_key, model_data in data["models"].items():
            total_configs += len(model_data["configurations"])
            total_colors += len(model_data["colors"])
        
        print(f"{brand:8} | {model_count:2} models | {total_configs:2} configs | {total_colors:2} colors")
    
    print("=" * 50)
    print(f"Total models in source: {total_models}")
    print(f"Total models extracted: {extracted_models}")
    print(f"Data integrity: {'✅ PASS' if total_models == extracted_models else '❌ FAIL'}")
    
    # Validate ASUS model count (should be 30+ as per requirements)
    if "ASUS" in brands_data:
        asus_count = len(brands_data["ASUS"]["models"])
        print(f"ASUS models: {asus_count} {'✅ PASS' if asus_count >= 30 else '❌ FAIL (should be 30+)'}")
    
    # Check for required metadata fields
    sample_errors = []
    for brand, data in brands_data.items():
        for model_key, model_data in data["models"].items():
            # Check required fields
            required_fields = ["display_name", "series", "year", "category", "configurations", "colors"]
            for field in required_fields:
                if field not in model_data:
                    sample_errors.append(f"{brand} {model_key} missing {field}")
                    break
            
            # Check configuration fields
            if model_data.get("configurations"):
                config = model_data["configurations"][0]
                config_fields = ["cpu", "ram", "vga", "gpu", "display", "storage", "os", "keyboard_layout", "keyboard_backlight"]
                for field in config_fields:
                    if field not in config:
                        sample_errors.append(f"{brand} {model_key} config missing {field}")
                        break
            
            if len(sample_errors) >= 3:  # Limit error output
                break
        if len(sample_errors) >= 3:
            break
    
    if sample_errors:
        print("\n❌ Sample validation errors:")
        for error in sample_errors[:3]:
            print(f"  - {error}")
    else:
        print("\n✅ All required fields present")

def main():
    """Main extraction process"""
    print("🚀 Starting Laptop Model Data Extraction")
    print("Task 1.4: Extract laptop model data to per-brand JSON files")
    print("=" * 60)
    
    # Define output directory
    output_dir = project_root / "data" / "products" / "laptops"
    
    # Extract data by brand
    print("\n📋 Extracting laptop data by brand...")
    brands_data = extract_laptop_data_by_brand()
    
    # Save brand files
    print("\n💾 Saving per-brand JSON files...")
    save_brand_files(brands_data, output_dir)
    
    # Create brands index
    print("\n📚 Creating brands index...")
    create_brands_index(brands_data, output_dir)
    
    # Validate extraction
    validate_extraction(brands_data)
    
    print(f"\n✅ Task 1.4 Complete!")
    print(f"📁 Output directory: {output_dir}")
    print(f"📄 Files created:")
    for brand in brands_data.keys():
        print(f"   - {brand.lower()}.json")
    print(f"   - brands_index.json")

if __name__ == "__main__":
    main()