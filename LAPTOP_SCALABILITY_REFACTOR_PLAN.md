# Laptop Model Scalability Refactor - Implementation Plan

## Executive Summary
This comprehensive plan refactors the current monolithic laptop specification system into a scalable, data-driven architecture with clean separation of concerns, searchable dropdowns, and auto-generated template caching.

## Current vs Target State

### Current Issues
- **laptop_specs.py**: 1,892 lines with 40+ models hardcoded
- **Mixed concerns**: Config folder contains data, logic, and mappings
- **Manual maintenance**: Adding new models requires extensive coding
- **Text inputs**: Prone to typos and inconsistent data
- **Complex dependencies**: 33+ files with circular imports

### Target Benefits
- **Add new brand**: 2-3 days → 30 minutes (95% reduction)
- **Add new model**: 30-60 minutes → 2-3 minutes (90% reduction)
- **Zero typos**: Searchable dropdowns with validated data
- **Clean architecture**: Proper separation of config/data/services
- **Auto-generated cache**: Fast performance with file persistence

## Final Architecture Structure

```
Shopify-Bulk-Importer/
├── config/                           # ONLY configuration files
│   └── shopify_config.py            # API keys, settings (NO CHANGES)
│
├── data/                            # [NEW] All static data & mappings
│   ├── metaobjects/                 # Shopify metaobject GID mappings
│   │   ├── processors.json          # "Intel Core i7-12700H..." : "gid://..."
│   │   ├── graphics.json            # Integrated graphics mappings
│   │   ├── vga.json                 # Dedicated graphics mappings
│   │   ├── displays.json            # Display mappings
│   │   ├── storage.json             # Storage mappings
│   │   ├── colors.json              # Color mappings
│   │   ├── os.json                  # OS mappings
│   │   ├── keyboard_layouts.json    # "US - International Keyboard", etc.
│   │   └── keyboard_backlights.json # "RGB Backlight", "Non-backlit", etc.
│   ├── products/                    # Product specifications
│   │   ├── laptops/                 # Split by brand
│   │   │   ├── asus.json           # ASUS models only
│   │   │   ├── dell.json           # Dell models only
│   │   │   ├── hp.json             # HP models only
│   │   │   └── brands_index.json   # Brand file mappings
│   │   ├── iphone.json             # iPhone specifications (moved)
│   │   └── galaxy.json             # Galaxy specifications (moved)
│   └── cache/                       # Generated cache files
│       └── template_cache.json      # Auto-generated templates
│
├── services/                        # Business logic layer
│   ├── template_cache_service.py    # [NEW] Template generation & caching
│   ├── component_dropdown_service.py # [NEW] Dropdown population
│   ├── brand_import_service.py      # [NEW] CSV to JSON import
│   └── [existing services...]
│
├── repositories/                    # Data access layer
│   ├── metaobject_repository.py    # [NEW] Metaobject data access
│   └── product_data_repository.py  # [NEW] Product data access
│
└── archive/                        # Deprecated files after migration
    └── config/
        ├── laptop_specs.py         # [MOVE HERE after Phase 3]
        ├── laptop_metafield_mapping*.py
        └── [other deprecated files]
```

## Data Format Specifications

### Template Format (NO CHANGES - PERFECT)
```
"ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB SSD] [Graphite Black]"
```
- **Template includes**: CPU/RAM/VGA/Display/Storage + Color
- **Template excludes**: OS, keyboard layout, keyboard backlight (form fields only)

### Laptop Model Data Structure
```json
// data/products/laptops/asus.json
{
  "brand": "ASUS",
  "models": {
    "ASUS TUF F15 FX507ZV4": {
      "display_name": "TUF Gaming F15",
      "series": "TUF Gaming",
      "year": 2023,
      "category": "Gaming",
      "configurations": [
        {
          "cpu": "Intel Core i7-12700H (20 CPUs), ~2.3GHz",
          "ram": "16GB",
          "vga": "NVIDIA GeForce RTX 4060 8GB",
          "gpu": "Intel Iris Xe Graphics",
          "display": "15.6\" FHD 144Hz",
          "storage": "512GB SSD",
          "os": "Windows 11",
          "keyboard_layout": "US - International Keyboard",
          "keyboard_backlight": "RGB Backlight"
        }
      ],
      "colors": ["Graphite Black", "Eclipse Gray"]
    }
  }
}
```

### Metaobject Mapping Structure
```json
// data/metaobjects/processors.json
{
  "Intel Core i7-12700H (20 CPUs), ~2.3GHz": "gid://shopify/Metaobject/131306782869",
  "AMD Ryzen 7 4800HS (16 CPUs), ~2.9GHz": "gid://shopify/Metaobject/131307438229"
}
```

## Phase 1: Foundation Setup (Day 1 - 4 hours)

### Task 1.1: Create Directory Structure (30 min)
**Agent**: code-quality-architect
**Goal**: Set up clean architecture folders

**Actions**:
1. Create `data/` directory with all subdirectories
2. Create `data/metaobjects/`, `data/products/laptops/`, `data/cache/`
3. Create `services/`, `repositories/` if needed
4. Create placeholder README files

**Validation**:
```bash
# Verify directory structure exists
ls -la data/metaobjects/
ls -la data/products/laptops/
ls -la data/cache/
```

### Task 1.2: Extract Metaobject GID Mappings (2 hours)
**Agent**: shopify-api-developer
**Goal**: Convert Python dict mappings to JSON files with full names as keys

**Source Files**:
- `config/laptop_metafield_mapping_actual.py`

**Create Files**:
- `data/metaobjects/processors.json`
- `data/metaobjects/graphics.json` (integrated)
- `data/metaobjects/vga.json` (dedicated)
- `data/metaobjects/displays.json`
- `data/metaobjects/storage.json`
- `data/metaobjects/colors.json`
- `data/metaobjects/os.json`
- `data/metaobjects/keyboard_layouts.json`
- `data/metaobjects/keyboard_backlights.json`

**Important**: Use FULL NAMES as keys (no abbreviations):
```json
// ✅ Correct
"Intel Core i7-12700H (20 CPUs), ~2.3GHz": "gid://shopify/Metaobject/131306782869"

// ❌ Wrong
"i7-12700H": "gid://shopify/Metaobject/131306782869"
```

**Validation**:
```python
# Test that all original GIDs are preserved
import json
with open('data/metaobjects/processors.json') as f:
    processors = json.load(f)
assert len(processors) >= 70  # Should have 70+ processors
assert "Intel Core i7-12700H (20 CPUs), ~2.3GHz" in processors
```

### Task 1.3: Create Repository Layer (1 hour)
**Agent**: code-quality-architect
**Goal**: Data access abstraction

**Create**: `repositories/metaobject_repository.py`
```python
import json
import glob
from typing import Dict, Optional, List

class MetaobjectRepository:
    def __init__(self):
        self.base_path = "data/metaobjects/"
        self._cache = {}
    
    def get_processor_mapping(self) -> Dict[str, str]:
        return self._load_mapping("processors.json")
    
    def get_vga_mapping(self) -> Dict[str, str]:
        return self._load_mapping("vga.json")
    
    def get_graphics_mapping(self) -> Dict[str, str]:
        return self._load_mapping("graphics.json")
    
    def get_display_mapping(self) -> Dict[str, str]:
        return self._load_mapping("displays.json")
    
    def get_storage_mapping(self) -> Dict[str, str]:
        return self._load_mapping("storage.json")
    
    def get_color_mapping(self) -> Dict[str, str]:
        return self._load_mapping("colors.json")
    
    def get_os_mapping(self) -> Dict[str, str]:
        return self._load_mapping("os.json")
    
    def get_keyboard_layout_mapping(self) -> Dict[str, str]:
        return self._load_mapping("keyboard_layouts.json")
    
    def get_keyboard_backlight_mapping(self) -> Dict[str, str]:
        return self._load_mapping("keyboard_backlights.json")
    
    def get_gid(self, component_type: str, full_name: str) -> Optional[str]:
        """Get GID for component by type and full name"""
        mapping_methods = {
            "processor": self.get_processor_mapping,
            "vga": self.get_vga_mapping,
            "graphics": self.get_graphics_mapping,
            "display": self.get_display_mapping,
            "storage": self.get_storage_mapping,
            "color": self.get_color_mapping,
            "os": self.get_os_mapping,
            "keyboard_layout": self.get_keyboard_layout_mapping,
            "keyboard_backlight": self.get_keyboard_backlight_mapping,
        }
        
        if component_type in mapping_methods:
            mapping = mapping_methods[component_type]()
            return mapping.get(full_name)
        
        return None
    
    def _load_mapping(self, filename: str) -> Dict[str, str]:
        if filename not in self._cache:
            with open(f"{self.base_path}{filename}", 'r') as f:
                self._cache[filename] = json.load(f)
        return self._cache[filename]
```

**Create**: `repositories/product_data_repository.py`
```python
import json
import glob
from typing import Dict, List

class ProductDataRepository:
    def __init__(self):
        self.laptop_path = "data/products/laptops/"
    
    def get_brand_data(self, brand: str) -> Dict:
        """Load data for specific brand"""
        filename = f"{brand.lower()}.json"
        with open(f"{self.laptop_path}{filename}", 'r') as f:
            return json.load(f)
    
    def get_all_brands(self) -> List[str]:
        """Get list of available brands"""
        files = glob.glob(f"{self.laptop_path}*.json")
        brands = []
        for file in files:
            if "brands_index.json" not in file:
                brand_name = file.split('/')[-1].replace('.json', '').title()
                brands.append(brand_name)
        return sorted(brands)
    
    def get_all_models(self) -> Dict[str, Dict]:
        """Load all laptop models from all brands"""
        all_models = {}
        for brand in self.get_all_brands():
            brand_data = self.get_brand_data(brand)
            all_models.update(brand_data.get("models", {}))
        return all_models
```

### Task 1.4: Extract Laptop Model Data (1.5 hours)
**Agent**: code-quality-architect
**Goal**: Convert laptop_specs.py to per-brand JSON files

**Source**: `config/laptop_specs.py` (LAPTOP_SPECS dict)

**Create Files**:
- `data/products/laptops/asus.json`
- `data/products/laptops/dell.json`
- `data/products/laptops/hp.json`
- `data/products/laptops/msi.json`
- `data/products/laptops/brands_index.json`

**Example output for asus.json**:
```json
{
  "brand": "ASUS",
  "models": {
    "ASUS TUF F15 FX507ZV4": {
      "display_name": "TUF Gaming F15",
      "series": "TUF Gaming",
      "year": 2023,
      "category": "Gaming",
      "configurations": [
        {
          "cpu": "Intel Core i7-12700H (20 CPUs), ~2.3GHz",
          "ram": "16GB",
          "vga": "NVIDIA GeForce RTX 4060 8GB",
          "gpu": "Intel Iris Xe Graphics",
          "display": "15.6\" FHD 144Hz",
          "storage": "512GB SSD",
          "os": "Windows 11",
          "keyboard_layout": "US - International Keyboard",
          "keyboard_backlight": "RGB Backlight"
        }
      ],
      "colors": ["Graphite Black", "Eclipse Gray"]
    }
  }
}
```

**Validation**:
```python
# Verify data integrity
import json
with open('data/products/laptops/asus.json') as f:
    asus_data = json.load(f)

# Check model count matches original
assert len(asus_data['models']) >= 30  # ASUS has 30+ models

# Check data completeness
for model_key, model_data in asus_data['models'].items():
    assert 'configurations' in model_data
    assert 'colors' in model_data
    assert len(model_data['configurations']) > 0
```

## Phase 2: Service Layer Implementation (Day 2 - 6 hours)

### Task 2.1: Create Template Display Service (2 hours)
**Agent**: code-quality-architect
**Goal**: Smart abbreviation service for template generation

**Create**: `services/template_display_service.py`
```python
import re
from typing import Dict, List, Tuple

class TemplateDisplayService:
    def __init__(self):
        self._abbreviation_cache = {}
    
    def abbreviate_for_template(self, full_name: str, component_type: str) -> str:
        """Convert full component name to template-friendly abbreviation"""
        cache_key = f"{component_type}:{full_name}"
        
        if cache_key not in self._abbreviation_cache:
            self._abbreviation_cache[cache_key] = self._calculate_abbreviation(full_name, component_type)
        
        return self._abbreviation_cache[cache_key]
    
    def _calculate_abbreviation(self, full_name: str, component_type: str) -> str:
        """Calculate abbreviation based on component type"""
        if component_type == "cpu":
            # "Intel Core i7-12700H (20 CPUs), ~2.3GHz" → "i7-12700H"
            if "Intel Core" in full_name:
                match = re.search(r'Intel Core (i\d+-\w+)', full_name)
                return match.group(1) if match else full_name
            elif "AMD Ryzen" in full_name:
                # "AMD Ryzen 7 4800HS (16 CPUs), ~2.9GHz" → "Ryzen 7 4800HS"
                match = re.search(r'AMD (Ryzen \d+ \w+)', full_name)
                return match.group(1) if match else full_name
            elif "Apple" in full_name:
                # "Apple M2 Chip" → "Apple M2"
                return full_name.replace(" Chip", "")
        
        elif component_type == "vga":
            # "NVIDIA GeForce RTX 4060 8GB" → "RTX 4060"
            if "RTX" in full_name:
                match = re.search(r'RTX (\d+)', full_name)
                return f"RTX {match.group(1)}" if match else full_name
            elif "GTX" in full_name:
                match = re.search(r'GTX (\d+)', full_name)
                return f"GTX {match.group(1)}" if match else full_name
            elif "Radeon" in full_name:
                # Extract model number
                match = re.search(r'Radeon.*?(\w+\s*\w*M?)', full_name)
                return match.group(1) if match else full_name
        
        elif component_type == "display":
            # "15.6\" FHD 144Hz" → "144Hz"
            # "13.3-inch Retina" → "Retina"
            if "Hz" in full_name:
                match = re.search(r'(\d+Hz)', full_name)
                return match.group(1) if match else full_name
            elif "Retina" in full_name:
                return "Retina"
            else:
                # Fallback: extract resolution or size
                return full_name
        
        elif component_type in ["ram", "storage", "os"]:
            # These are already simple enough for templates
            return full_name
        
        return full_name
    
    def generate_template_string(self, model_key: str, config: Dict, color: str) -> str:
        """Generate template string for a specific configuration"""
        components = [
            self.abbreviate_for_template(config["cpu"], "cpu"),
            config["ram"],  # Already simple: "16GB"
            self.abbreviate_for_template(config["vga"], "vga"),
            self.abbreviate_for_template(config["display"], "display"),
            config["storage"]  # Already simple: "512GB SSD"
        ]
        
        spec_string = "/".join(components)
        return f"{model_key} [{spec_string}] [{color}]"
```

### Task 2.2: Create Template Cache Service (2 hours)
**Agent**: code-quality-architect
**Goal**: Auto-generating template cache with file persistence

**Create**: `services/template_cache_service.py`
```python
import json
import os
import glob
from datetime import datetime
from typing import List, Dict
from repositories.product_data_repository import ProductDataRepository
from services.template_display_service import TemplateDisplayService

class TemplateCacheService:
    def __init__(self):
        self.cache_file = "data/cache/template_cache.json"
        self.source_dir = "data/products/laptops/"
        self.product_repo = ProductDataRepository()
        self.display_service = TemplateDisplayService()
    
    def get_all_templates(self) -> List[str]:
        """Get all laptop templates, regenerating cache if needed"""
        if self.needs_regeneration():
            self.regenerate_cache()
        
        return self._load_cached_templates()
    
    def needs_regeneration(self) -> bool:
        """Check if template cache needs to be regenerated"""
        if not os.path.exists(self.cache_file):
            return True
        
        cache_time = os.path.getmtime(self.cache_file)
        
        # Check if any source file is newer than cache
        for brand_file in glob.glob(f"{self.source_dir}*.json"):
            if os.path.getmtime(brand_file) > cache_time:
                return True
        
        return False
    
    def regenerate_cache(self):
        """Generate all templates and save to cache file"""
        print("🔄 Regenerating template cache...")
        
        templates = []
        template_metadata = {}
        
        # Generate templates for each brand
        for brand in self.product_repo.get_all_brands():
            brand_templates = self._generate_brand_templates(brand)
            templates.extend(brand_templates)
        
        # Sort templates
        templates = sorted(templates)
        
        # Save to cache
        cache_data = {
            "generated_at": datetime.now().isoformat(),
            "total_templates": len(templates),
            "templates": templates,
            "version": "1.0",
            "source_files": glob.glob(f"{self.source_dir}*.json")
        }
        
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        print(f"✅ Generated {len(templates)} templates")
    
    def _generate_brand_templates(self, brand: str) -> List[str]:
        """Generate templates for a specific brand"""
        templates = []
        brand_data = self.product_repo.get_brand_data(brand)
        
        for model_key, model_spec in brand_data["models"].items():
            for config in model_spec["configurations"]:
                for color in model_spec["colors"]:
                    template = self.display_service.generate_template_string(
                        model_key, config, color
                    )
                    templates.append(template)
        
        return templates
    
    def _load_cached_templates(self) -> List[str]:
        """Load templates from cache file"""
        with open(self.cache_file, 'r') as f:
            cache_data = json.load(f)
        
        return cache_data["templates"]
    
    def parse_template(self, template: str) -> Dict[str, str]:
        """Parse template string back to component data"""
        try:
            # Extract model name (everything before first bracket)
            model_match = template.split('[')[0].strip()
            
            # Extract spec string (between first brackets)
            spec_start = template.find('[') + 1
            spec_end = template.find(']', spec_start)
            spec_string = template[spec_start:spec_end]
            
            # Extract color (between second brackets)
            color_start = template.find('[', spec_end) + 1
            color_end = template.find(']', color_start)
            color = template[color_start:color_end]
            
            # Parse spec components
            spec_parts = spec_string.split('/')
            if len(spec_parts) != 5:
                return None
            
            # Find the original model data to get full component names
            model_data = self._find_model_data(model_match, spec_parts, color)
            
            if model_data:
                return {
                    'model': model_match,
                    'brand': model_data['brand'],
                    'cpu': model_data['cpu'],
                    'ram': model_data['ram'],
                    'vga': model_data['vga'],
                    'gpu': model_data['gpu'],
                    'display': model_data['display'],
                    'storage': model_data['storage'],
                    'color': color,
                    'os': model_data['os'],
                    'keyboard_layout': model_data['keyboard_layout'],
                    'keyboard_backlight': model_data['keyboard_backlight'],
                    'template': template
                }
            
        except Exception as e:
            print(f"Error parsing template: {template}, Error: {e}")
            return None
    
    def _find_model_data(self, model_key: str, spec_parts: List[str], color: str) -> Dict:
        """Find original model data by matching template components"""
        all_models = self.product_repo.get_all_models()
        
        if model_key not in all_models:
            return None
        
        model_spec = all_models[model_key]
        
        # Find matching configuration
        for config in model_spec["configurations"]:
            # Check if this config matches the abbreviated spec
            if (self.display_service.abbreviate_for_template(config["cpu"], "cpu") == spec_parts[0] and
                config["ram"] == spec_parts[1] and
                self.display_service.abbreviate_for_template(config["vga"], "vga") == spec_parts[2] and
                self.display_service.abbreviate_for_template(config["display"], "display") == spec_parts[3] and
                config["storage"] == spec_parts[4] and
                color in model_spec["colors"]):
                
                return {
                    'brand': model_spec.get('brand', 'Unknown'),
                    **config
                }
        
        return None
```

### Task 2.3: Create Component Dropdown Service (1.5 hours)
**Agent**: ux-design-specialist
**Goal**: Populate searchable dropdowns with component options

**Create**: `services/component_dropdown_service.py`
```python
from typing import List, Tuple, Dict, Optional
from repositories.metaobject_repository import MetaobjectRepository

class ComponentDropdownService:
    def __init__(self):
        self.metaobject_repo = MetaobjectRepository()
    
    def get_processor_options(self) -> List[Tuple[str, str]]:
        """Get processor dropdown options as (value, display_name) tuples"""
        mapping = self.metaobject_repo.get_processor_mapping()
        options = [("", "Select processor...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))  # Full name as both value and display
        
        # Add custom option
        options.append(("CUSTOM", "Other/Custom processor..."))
        return options
    
    def get_ram_options(self) -> List[str]:
        """Get common RAM options"""
        return ["", "8GB", "16GB", "32GB", "64GB"]
    
    def get_vga_options(self) -> List[Tuple[str, str]]:
        """Get VGA (dedicated graphics) dropdown options"""
        mapping = self.metaobject_repo.get_vga_mapping()
        options = [("", "Select dedicated graphics...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        options.append(("CUSTOM", "Other/Custom VGA..."))
        return options
    
    def get_graphics_options(self) -> List[Tuple[str, str]]:
        """Get integrated graphics dropdown options"""
        mapping = self.metaobject_repo.get_graphics_mapping()
        options = [("", "Select integrated graphics...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        options.append(("CUSTOM", "Other/Custom graphics..."))
        return options
    
    def get_display_options(self) -> List[Tuple[str, str]]:
        """Get display dropdown options"""
        mapping = self.metaobject_repo.get_display_mapping()
        options = [("", "Select display...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        options.append(("CUSTOM", "Other/Custom display..."))
        return options
    
    def get_storage_options(self) -> List[Tuple[str, str]]:
        """Get storage dropdown options"""
        mapping = self.metaobject_repo.get_storage_mapping()
        options = [("", "Select storage...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        options.append(("CUSTOM", "Other/Custom storage..."))
        return options
    
    def get_color_options(self) -> List[Tuple[str, str]]:
        """Get color dropdown options"""
        mapping = self.metaobject_repo.get_color_mapping()
        options = [("", "Select color...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        options.append(("CUSTOM", "Other/Custom color..."))
        return options
    
    def get_os_options(self) -> List[Tuple[str, str]]:
        """Get OS dropdown options"""
        mapping = self.metaobject_repo.get_os_mapping()
        options = [("", "Select OS...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        return options
    
    def get_keyboard_layout_options(self) -> List[Tuple[str, str]]:
        """Get keyboard layout dropdown options"""
        mapping = self.metaobject_repo.get_keyboard_layout_mapping()
        options = [("", "Select keyboard layout...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        return options
    
    def get_keyboard_backlight_options(self) -> List[Tuple[str, str]]:
        """Get keyboard backlight dropdown options"""
        mapping = self.metaobject_repo.get_keyboard_backlight_mapping()
        options = [("", "Select backlight type...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        return options
    
    def find_dropdown_index(self, options: List[Tuple[str, str]], value: str) -> int:
        """Find the index of a value in dropdown options"""
        for i, (option_value, _) in enumerate(options):
            if option_value == value:
                return i
        return 0  # Default to first option if not found
```

### Task 2.4: Create Brand Import Service (30 minutes)
**Agent**: product-strategy-advisor
**Goal**: Enable CSV import for bulk model addition

**Create**: `services/brand_import_service.py`
```python
import csv
import json
from typing import Dict, List
from repositories.product_data_repository import ProductDataRepository

class BrandImportService:
    def __init__(self):
        self.product_repo = ProductDataRepository()
    
    def import_from_csv(self, csv_path: str, brand_name: str) -> Dict:
        """Import laptop models from CSV file"""
        models = {}
        
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                model_key = row['model_key']  # e.g., "HP Pavilion 15"
                
                models[model_key] = {
                    "display_name": row.get('display_name', ''),
                    "series": row.get('series', ''),
                    "year": int(row.get('year', 2023)),
                    "category": row.get('category', 'Laptop'),
                    "configurations": [{
                        "cpu": row['cpu'],
                        "ram": row['ram'],
                        "vga": row['vga'],
                        "gpu": row['gpu'],
                        "display": row['display'],
                        "storage": row['storage'],
                        "os": row.get('os', 'Windows 11'),
                        "keyboard_layout": row.get('keyboard_layout', 'US - International Keyboard'),
                        "keyboard_backlight": row.get('keyboard_backlight', 'Backlit')
                    }],
                    "colors": row['colors'].split('|')  # "Color1|Color2|Color3"
                }
        
        return {
            "brand": brand_name,
            "models": models
        }
    
    def save_brand_data(self, brand_name: str, brand_data: Dict):
        """Save brand data to JSON file"""
        filename = f"data/products/laptops/{brand_name.lower()}.json"
        
        with open(filename, 'w') as f:
            json.dump(brand_data, f, indent=2)
        
        print(f"✅ Saved {len(brand_data['models'])} models for {brand_name}")
```

## Phase 3: UI Implementation (Day 3 - 4 hours)

### Task 3.1: Update Template Loading (1 hour)
**Agent**: ux-design-specialist
**Goal**: Replace template loading with new cache service

**Update**: `pages/laptop_entry.py`

**Changes needed**:
```python
# OLD CODE (to be replaced)
from config.laptop_specs import generate_all_laptop_templates, parse_laptop_template

# NEW CODE
from services.template_cache_service import TemplateCacheService
import streamlit as st

# Initialize service
@st.cache_resource
def get_template_service():
    return TemplateCacheService()

# In the main function
def main():
    template_service = get_template_service()
    
    # Auto-regenerate cache if needed (runs on app start)
    if template_service.needs_regeneration():
        with st.spinner("Updating laptop templates..."):
            template_service.regenerate_cache()
    
    # Load templates
    all_templates = template_service.get_all_templates()
    
    # Template selection (no changes to UI)
    selected_template = st.selectbox(
        "Search and select laptop template:",
        [""] + all_templates,
        format_func=lambda x: x if x else "Type to search laptop templates...",
        key="laptop_template_selector"
    )
    
    # Parse template (updated method)
    if selected_template:
        template_info = template_service.parse_template(selected_template)
        # template_info now contains full component names
```

### Task 3.2: Implement Searchable Dropdowns (2.5 hours)
**Agent**: ux-design-specialist
**Goal**: Replace text inputs with searchable dropdowns

**Update**: `pages/laptop_entry.py` - Replace all component text inputs

**Changes needed**:
```python
from services.component_dropdown_service import ComponentDropdownService

# Initialize dropdown service
@st.cache_resource
def get_dropdown_service():
    return ComponentDropdownService()

# In the form section, replace:

# OLD: CPU text input
cpu = st.text_input("Processor", value=template_info.get('cpu', ''))

# NEW: CPU searchable dropdown
dropdown_service = get_dropdown_service()
cpu_options = dropdown_service.get_processor_options()
cpu_index = dropdown_service.find_dropdown_index(cpu_options, template_info.get('cpu', ''))

cpu_selection = st.selectbox(
    "Processor",
    options=cpu_options,
    format_func=lambda x: x[1],  # Show display name
    index=cpu_index,
    key="laptop_cpu_dropdown"
)
cpu = cpu_selection[0]  # Get the value

# Handle custom input
if cpu == "CUSTOM":
    cpu = st.text_input("Enter custom processor:", key="cpu_custom")

# Apply same pattern to all components:
# - RAM (simple selectbox with predefined options)
# - VGA (searchable dropdown)
# - Integrated Graphics (searchable dropdown)  
# - Display (searchable dropdown)
# - Storage (searchable dropdown)
# - Color (searchable dropdown)
# - OS (dropdown)
# - Keyboard Layout (dropdown)
# - Keyboard Backlight (dropdown)
```

**Detailed implementation for each field**:
```python
# RAM - Simple dropdown with common options
ram_options = dropdown_service.get_ram_options()
ram_index = ram_options.index(template_info.get('ram', '')) if template_info.get('ram', '') in ram_options else 0
ram = st.selectbox("RAM", options=ram_options, index=ram_index, key="laptop_ram_dropdown")

# VGA - Searchable dropdown
vga_options = dropdown_service.get_vga_options()
vga_index = dropdown_service.find_dropdown_index(vga_options, template_info.get('vga', ''))
vga_selection = st.selectbox("VGA (dedicated graphics)", options=vga_options, format_func=lambda x: x[1], index=vga_index, key="laptop_vga_dropdown")
vga = vga_selection[0]
if vga == "CUSTOM":
    vga = st.text_input("Enter custom VGA:", key="vga_custom")

# Integrated Graphics - Searchable dropdown
gpu_options = dropdown_service.get_graphics_options()
gpu_index = dropdown_service.find_dropdown_index(gpu_options, template_info.get('gpu', ''))
gpu_selection = st.selectbox("Integrated Graphics", options=gpu_options, format_func=lambda x: x[1], index=gpu_index, key="laptop_gpu_dropdown")
gpu = gpu_selection[0]
if gpu == "CUSTOM":
    gpu = st.text_input("Enter custom integrated graphics:", key="gpu_custom")

# Continue for all other components...
```

### Task 3.3: Update Master Data Integration (30 minutes)
**Agent**: shopify-api-developer
**Goal**: Update master_data.py to use new services

**Update**: `config/master_data.py`

**Changes needed**:
```python
# OLD CODE (to be replaced)
from config.laptop_specs import generate_all_laptop_templates
from config.iphone_specs import get_all_iphone_models
from config.galaxy_specs import get_all_galaxy_models

# NEW CODE
from services.template_cache_service import TemplateCacheService
import json

def get_all_laptop_templates():
    """Get all laptop templates from cache service"""
    service = TemplateCacheService()
    return service.get_all_templates()

def get_all_iphone_models():
    """Load iPhone models from JSON"""
    with open('data/products/iphone.json', 'r') as f:
        data = json.load(f)
    return list(data.keys())

def get_all_galaxy_models():
    """Load Galaxy models from JSON"""
    with open('data/products/galaxy.json', 'r') as f:
        data = json.load(f)
    return list(data.keys())

# Update any other references to old config files
```

## Phase 4: Dependency Updates (Day 3 - 2 hours)

### Task 4.1: Update Service Layer Dependencies (1 hour)
**Agent**: shopify-api-developer
**Goal**: Update imports in service files

**Files to update**:
- `services/product_service.py`
- `services/laptop_metafield_service.py`
- `services/shopify_api.py`

**Changes needed**:
```python
# In services/product_service.py
# OLD
from config.laptop_metafield_mapping_actual import convert_laptop_data_to_metafields

# NEW  
from repositories.metaobject_repository import MetaobjectRepository

class ProductService:
    def __init__(self):
        self.metaobject_repo = MetaobjectRepository()
    
    def convert_laptop_data_to_metafields(self, laptop_data):
        """Updated method using repository"""
        metafields = []
        
        # Use repository to get GIDs
        processor_gid = self.metaobject_repo.get_gid("processor", laptop_data.get("cpu"))
        if processor_gid:
            metafields.append({
                "namespace": "laptop",
                "key": "processor", 
                "value": processor_gid,
                "type": "metaobject_reference"
            })
        
        # Apply same pattern for all components
        return metafields
```

### Task 4.2: Update Test Files (30 minutes)
**Agent**: test-coverage-specialist
**Goal**: Update import paths in test files

**Script approach** - Create automated update script:
```python
# scripts/update_test_imports.py
import os
import re

def update_imports_in_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Define replacement patterns
    replacements = {
        r'from config\.laptop_specs import': 'from services.template_cache_service import TemplateCacheService',
        r'from config\.laptop_metafield_mapping import': 'from repositories.metaobject_repository import MetaobjectRepository',
        r'from config\.laptop_metafield_mapping_enhanced import': 'from repositories.metaobject_repository import MetaobjectRepository',
        r'from config\.laptop_metafield_mapping_actual import': 'from repositories.metaobject_repository import MetaobjectRepository',
    }
    
    for old_pattern, new_import in replacements.items():
        content = re.sub(old_pattern, new_import, content)
    
    with open(file_path, 'w') as f:
        f.write(content)

# Find and update all test files
for root, dirs, files in os.walk('tests/'):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            update_imports_in_file(file_path)
```

### Task 4.3: Update Admin Tools (30 minutes)
**Agent**: shopify-api-developer
**Goal**: Update admin tools to use new architecture

**Update**: `admin/missing_metaobjects_report.py`

**Changes needed**:
```python
# OLD
from config.laptop_metafield_mapping_enhanced import missing_logger, get_missing_entries_report

# NEW
from repositories.metaobject_repository import MetaobjectRepository

def generate_missing_report():
    repo = MetaobjectRepository()
    
    # Check for missing mappings across all component types
    missing_components = []
    
    # This logic will need to be adapted based on how you want to track missing components
    # Could read from logs or scan data files for unmapped components
    
    return missing_components
```

## Phase 5: File Cleanup & Documentation (Day 3 - 1 hour)

### Task 5.1: Archive Old Files (30 minutes)
**Agent**: code-quality-architect
**Goal**: Move deprecated files to archive

**Actions**:
1. Create `archive/config/` directory
2. Move old files with timestamp:
   - `config/laptop_specs.py` → `archive/config/laptop_specs_20241204.py`
   - `config/laptop_metafield_mapping.py` → `archive/config/laptop_metafield_mapping_20241204.py`
   - `config/laptop_metafield_mapping_enhanced.py` → `archive/config/laptop_metafield_mapping_enhanced_20241204.py`
   - `config/laptop_metafield_mapping_actual.py` → `archive/config/laptop_metafield_mapping_actual_20241204.py`
   - `config/color_metaobject_mapping.py` → `archive/config/color_metaobject_mapping_20241204.py`
   - `config/dedicated_graphics_mapping.py` → `archive/config/dedicated_graphics_mapping_20241204.py`

3. Update `.gitignore` if needed
4. Create `archive/README.md` explaining archived files

### Task 5.2: Create Documentation (30 minutes)
**Agent**: ux-design-specialist
**Goal**: User guides for new system

**Create**: `docs/ADDING_LAPTOP_MODELS.md`
```markdown
# Adding Laptop Models - Quick Guide

## Adding a Single Model

1. Open the appropriate brand file: `data/products/laptops/asus.json`
2. Add new model under "models":
```json
"NEW MODEL KEY": {
  "display_name": "Model Display Name",
  "series": "Series Name",
  "year": 2024,
  "category": "Gaming",
  "configurations": [{
    "cpu": "Intel Core i7-14700H (20 CPUs), ~2.4GHz",
    "ram": "16GB",
    "vga": "NVIDIA GeForce RTX 4070 8GB",
    "gpu": "Intel Iris Xe Graphics",
    "display": "15.6\" FHD 144Hz",
    "storage": "1TB SSD",
    "os": "Windows 11",
    "keyboard_layout": "US - International Keyboard",
    "keyboard_backlight": "RGB Backlight"
  }],
  "colors": ["Black", "Silver"]
}
```
3. Restart app - templates auto-regenerate!

## Adding New Brand via CSV

1. Create CSV with columns: model_key, display_name, series, year, cpu, ram, vga, gpu, display, storage, colors
2. Use BrandImportService:
```python
from services.brand_import_service import BrandImportService

service = BrandImportService()
brand_data = service.import_from_csv("new_brand.csv", "BrandName")
service.save_brand_data("BrandName", brand_data)
```

## Adding New Components

If you need a component not in dropdowns:
1. Add to appropriate JSON in `data/metaobjects/`
2. Add GID mapping in Shopify
3. Component automatically appears in dropdown
```

## Testing Strategy

### Phase 1 Testing
```python
# Test repository loading
repo = MetaobjectRepository()
processors = repo.get_processor_mapping()
assert len(processors) >= 70
assert "Intel Core i7-12700H (20 CPUs), ~2.3GHz" in processors

# Test product data loading  
product_repo = ProductDataRepository()
brands = product_repo.get_all_brands()
assert "ASUS" in brands
asus_data = product_repo.get_brand_data("ASUS")
assert len(asus_data["models"]) >= 30
```

### Phase 2 Testing
```python
# Test template generation
template_service = TemplateCacheService()
templates = template_service.get_all_templates()
assert len(templates) >= 200
assert "ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB SSD] [Graphite Black]" in templates

# Test template parsing
parsed = template_service.parse_template("ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB SSD] [Graphite Black]")
assert parsed["cpu"] == "Intel Core i7-12700H (20 CPUs), ~2.3GHz"
assert parsed["ram"] == "16GB"
```

### Phase 3 Testing
```python
# Test dropdown service
dropdown_service = ComponentDropdownService()
cpu_options = dropdown_service.get_processor_options()
assert len(cpu_options) >= 70
assert ("Intel Core i7-12700H (20 CPUs), ~2.3GHz", "Intel Core i7-12700H (20 CPUs), ~2.3GHz") in cpu_options
```

### Integration Testing
1. Template selection works
2. Form fields populate correctly
3. Product creation succeeds
4. All metafields map to correct GIDs
5. No data loss compared to old system

## Rollback Plan

If issues arise:
1. Restore files from `archive/config/`
2. Revert import changes
3. Remove new directories
4. System returns to original state

## Success Criteria

✅ Add new brand: 30 minutes (vs 2-3 days)
✅ Add new model: 2-3 minutes (vs 30-60 minutes)  
✅ Zero typos in component selection
✅ Clean architecture with proper separation
✅ All existing functionality preserved
✅ Performance maintained or improved
✅ 33+ files updated without breaking changes

This comprehensive plan ensures a smooth migration to the new scalable architecture while maintaining all existing functionality and improving the development experience significantly.

## Phase 6: GID Resolution Optimization (Future Session - 4 hours)

**Status**: Phase 4 completed successfully with 78% GID resolution rate (7 out of 9 component types fully resolved). Phase 6 addresses the remaining gaps to achieve 95%+ coverage.

**Current GID Resolution Analysis**:
- ✅ **processors.json**: 69+ entries, excellent coverage
- ✅ **graphics.json**: 17 entries, good coverage  
- ✅ **colors.json**: 27 entries, excellent coverage
- ✅ **displays.json**: 19 entries, adequate coverage (some format inconsistencies)
- ✅ **storage.json**: 6 entries, basic coverage (missing combinations)
- ✅ **os.json**: 7 entries, adequate coverage
- ✅ **keyboard_layouts.json**: 2 entries, sufficient coverage
- ❌ **vga.json**: Only 8 entries, major gap identified (critical priority)
- ❌ **RAM**: Currently hardcoded strings, not using metaobject system

### Task 6.1: Expand VGA Mappings (Critical Priority - 1.5 hours)
**Agent**: shopify-api-developer
**Goal**: Address the major VGA coverage gap from 8 to 50+ entries

**Current VGA entries** (only 8):
- NVIDIA GeForce GTX 1650 4GB
- NVIDIA GeForce RTX 3050 4GB  
- NVIDIA GeForce RTX 3060 6GB
- NVIDIA GeForce RTX 4050 6GB
- NVIDIA GeForce RTX 4060 8GB
- NVIDIA GeForce RTX 4070 8GB
- AMD Radeon RX 6500M 4GB
- AMD Radeon RX 6600M 8GB

**Missing VGA components identified**:
- RTX 4080/4090 series (high-end gaming)
- GTX 1660 Ti/1660 Super (mid-range legacy)  
- RTX 3070/3080 series (previous gen high-end)
- AMD RX 6700M/6800M series (AMD alternatives)
- RTX 4060 Ti variations
- Mobile workstation graphics (Quadro/FirePro)

**Actions**:
1. **Create missing VGA metaobjects in Shopify**:
   ```json
   // Target additions for data/metaobjects/vga.json
   {
     "NVIDIA GeForce RTX 4080 12GB": "gid://shopify/Metaobject/[NEW_GID]",
     "NVIDIA GeForce RTX 4090 16GB": "gid://shopify/Metaobject/[NEW_GID]",
     "NVIDIA GeForce GTX 1660 Ti 6GB": "gid://shopify/Metaobject/[NEW_GID]",
     "NVIDIA GeForce RTX 3070 8GB": "gid://shopify/Metaobject/[NEW_GID]",
     "NVIDIA GeForce RTX 3080 10GB": "gid://shopify/Metaobject/[NEW_GID]",
     "AMD Radeon RX 6700M 10GB": "gid://shopify/Metaobject/[NEW_GID]",
     "AMD Radeon RX 6800M 12GB": "gid://shopify/Metaobject/[NEW_GID]",
     "NVIDIA GeForce RTX 4060 Ti 8GB": "gid://shopify/Metaobject/[NEW_GID]",
     "NVIDIA GeForce RTX 4060 Ti 16GB": "gid://shopify/Metaobject/[NEW_GID]"
   }
   ```

2. **Priority order for VGA additions**:
   - RTX 4080/4090 (current flagship)
   - RTX 3070/3080 (common in existing inventory)
   - GTX 1660 Ti (popular mid-range legacy)
   - AMD RX 6700M/6800M (AMD competition)

**Validation**:
```python
# Test expanded VGA coverage
repo = MetaobjectRepository()
vga_mapping = repo.get_vga_mapping()
assert len(vga_mapping) >= 25  # Target 25+ VGA entries
assert "NVIDIA GeForce RTX 4080 12GB" in vga_mapping
```

### Task 6.2: Implement RAM as Metaobject System (High Priority - 1 hour)
**Agent**: shopify-api-developer  
**Goal**: Convert RAM from hardcoded strings to metaobject references

**Current Issue**: RAM uses simple strings ("8GB", "16GB") instead of metaobject GIDs like other components.

**Actions**:
1. **Create RAM metaobjects in Shopify**:
   ```json
   // Create data/metaobjects/ram.json
   {
     "8GB": "gid://shopify/Metaobject/[NEW_GID]",
     "16GB": "gid://shopify/Metaobject/[NEW_GID]", 
     "32GB": "gid://shopify/Metaobject/[NEW_GID]",
     "64GB": "gid://shopify/Metaobject/[NEW_GID]",
     "8GB DDR4": "gid://shopify/Metaobject/[NEW_GID]",
     "16GB DDR4": "gid://shopify/Metaobject/[NEW_GID]",
     "32GB DDR4": "gid://shopify/Metaobject/[NEW_GID]",
     "8GB DDR5": "gid://shopify/Metaobject/[NEW_GID]",
     "16GB DDR5": "gid://shopify/Metaobject/[NEW_GID]",
     "32GB DDR5": "gid://shopify/Metaobject/[NEW_GID]"
   }
   ```

2. **Update MetaobjectRepository**:
   ```python
   # Add to repositories/metaobject_repository.py
   def get_ram_mapping(self) -> Dict[str, str]:
       return self._load_mapping("ram.json")
   ```

3. **Update ComponentDropdownService**:
   ```python
   # Replace hardcoded RAM options with metaobject-backed dropdown
   def get_ram_options(self) -> List[Tuple[str, str]]:
       mapping = self.metaobject_repo.get_ram_mapping()
       options = [("", "Select RAM...")]
       
       for full_name in sorted(mapping.keys()):
           options.append((full_name, full_name))
       
       options.append(("CUSTOM", "Other/Custom RAM..."))
       return options
   ```

**Validation**:
```python
# Test RAM metaobject integration
repo = MetaobjectRepository()
ram_mapping = repo.get_ram_mapping()
assert len(ram_mapping) >= 10  # DDR4/DDR5 variations
assert "16GB DDR5" in ram_mapping
```

### Task 6.3: Expand Storage Combinations (Medium Priority - 45 minutes)
**Agent**: shopify-api-developer
**Goal**: Add missing storage configurations for comprehensive coverage

**Current storage.json** (only 6 entries):
- 256GB SSD, 512GB SSD, 1TB SSD, 2TB SSD, 1TB HDD, 512GB SSD + 1TB HDD

**Missing combinations identified**:
- 128GB SSD (budget laptops)
- 4TB SSD (high-end workstations)  
- 256GB SSD + 1TB HDD (hybrid configs)
- 512GB SSD + 2TB HDD (common hybrid)
- NVMe vs SATA specifications
- Multiple drive configurations

**Actions**:
1. **Add missing storage metaobjects**:
   ```json
   // Additions to data/metaobjects/storage.json
   {
     "128GB SSD": "gid://shopify/Metaobject/[NEW_GID]",
     "4TB SSD": "gid://shopify/Metaobject/[NEW_GID]",
     "256GB SSD + 1TB HDD": "gid://shopify/Metaobject/[NEW_GID]",
     "512GB SSD + 2TB HDD": "gid://shopify/Metaobject/[NEW_GID]",
     "1TB NVMe SSD": "gid://shopify/Metaobject/[NEW_GID]",
     "2TB NVMe SSD": "gid://shopify/Metaobject/[NEW_GID]"
   }
   ```

**Target**: Expand from 6 to 15+ storage combinations

### Task 6.4: Standardize CPU Format Variations (Medium Priority - 30 minutes)
**Agent**: shopify-api-developer
**Goal**: Resolve CPU naming inconsistencies in processors.json

**Current issues identified**:
- Some entries: "Intel Core i7-12700H (20 CPUs), ~2.3GHz"
- Others: "Intel Core i5-1240P"
- Missing standardized format for Apple Silicon
- AMD format variations

**Actions**:
1. **Standardize CPU naming convention**:
   ```json
   // Standardized format examples
   {
     "Intel Core i7-12700H (20 CPUs), ~2.3GHz": "existing_gid",
     "Intel Core i5-1240P (16 CPUs), ~1.7GHz": "new_gid",
     "Apple M2 Chip (8-core CPU)": "new_gid", 
     "AMD Ryzen 7 6800H (16 CPUs), ~3.2GHz": "new_gid"
   }
   ```

2. **Create mapping for common format variations** to handle legacy data

### Task 6.5: Fix Display Format Inconsistencies (Low Priority - 30 minutes)
**Agent**: ux-design-specialist
**Goal**: Standardize display naming in displays.json

**Current issues**:
- Mix of formats: "15.6\" FHD 144Hz" vs "13.3-inch Retina"
- Inconsistent refresh rate notation
- Missing common resolutions

**Actions**:
1. **Standardize display format**: [Size] [Resolution] [Refresh Rate]
2. **Add missing common displays**:
   - "14\" FHD 60Hz"
   - "17.3\" FHD 144Hz" 
   - "15.6\" 4K 60Hz"

### Task 6.6: Create Missing Metaobject Analysis Tool (Support Task - 30 minutes)
**Agent**: code-quality-architect
**Goal**: Automated tool to identify missing GID mappings

**Create**: `admin/metaobject_gap_analyzer.py`
```python
import json
from repositories.metaobject_repository import MetaobjectRepository
from repositories.product_data_repository import ProductDataRepository

class MetaobjectGapAnalyzer:
    def __init__(self):
        self.metaobject_repo = MetaobjectRepository()
        self.product_repo = ProductDataRepository()
    
    def analyze_coverage_gaps(self) -> dict:
        """Analyze GID resolution gaps across all components"""
        gaps = {}
        all_models = self.product_repo.get_all_models()
        
        # Track unique component values used in product data
        used_components = {
            'cpu': set(), 'vga': set(), 'display': set(), 
            'storage': set(), 'ram': set(), 'gpu': set()
        }
        
        # Collect all used component values
        for model_data in all_models.values():
            for config in model_data.get('configurations', []):
                for component_type in used_components.keys():
                    if component_type in config:
                        used_components[component_type].add(config[component_type])
        
        # Check coverage for each component type
        for component_type, used_values in used_components.items():
            mapping_method = getattr(self.metaobject_repo, f'get_{component_type}_mapping', None)
            if mapping_method:
                available_mappings = mapping_method()
                missing = used_values - set(available_mappings.keys())
                gaps[component_type] = {
                    'total_used': len(used_values),
                    'mapped': len(used_values) - len(missing),
                    'missing': list(missing),
                    'coverage_percent': ((len(used_values) - len(missing)) / len(used_values)) * 100
                }
        
        return gaps
    
    def generate_missing_metaobjects_script(self, gaps: dict) -> str:
        """Generate GraphQL script to create missing metaobjects"""
        script = "# Missing Metaobject Creation Script\n\n"
        
        for component_type, gap_data in gaps.items():
            if gap_data['missing']:
                script += f"## {component_type.upper()} Missing Entries:\n"
                for missing_item in gap_data['missing']:
                    script += f"# TODO: Create metaobject for '{missing_item}'\n"
                script += "\n"
        
        return script

def main():
    analyzer = MetaobjectGapAnalyzer()
    gaps = analyzer.analyze_coverage_gaps()
    
    print("=== METAOBJECT COVERAGE ANALYSIS ===")
    total_coverage = 0
    
    for component_type, gap_data in gaps.items():
        coverage = gap_data['coverage_percent']  
        total_coverage += coverage
        print(f"{component_type.upper()}: {coverage:.1f}% ({gap_data['mapped']}/{gap_data['total_used']})")
        
        if gap_data['missing']:
            print(f"  Missing: {', '.join(gap_data['missing'][:3])}{'...' if len(gap_data['missing']) > 3 else ''}")
    
    overall_coverage = total_coverage / len(gaps)
    print(f"\nOVERALL GID RESOLUTION: {overall_coverage:.1f}%")
    
    # Generate missing items script
    script = analyzer.generate_missing_metaobjects_script(gaps)
    with open('admin/missing_metaobjects_todo.txt', 'w') as f:
        f.write(script)
    
    print(f"Missing items script saved to: admin/missing_metaobjects_todo.txt")

if __name__ == "__main__":
    main()
```

### Task 6.7: Update Repository Architecture for RAM (Technical Task - 15 minutes)
**Agent**: code-quality-architect
**Goal**: Ensure RAM metaobject integration is properly included in repository architecture

**Actions**:
1. Update `get_gid()` method in MetaobjectRepository to include RAM
2. Update component dropdown service method mappings
3. Update product service metafield conversion to handle RAM as metaobject reference

**Validation**:
```python
# Test complete architecture integration
repo = MetaobjectRepository()
ram_gid = repo.get_gid("ram", "16GB DDR5")
assert ram_gid is not None
assert ram_gid.startswith("gid://shopify/Metaobject/")
```

### Phase 6 Success Criteria

**Target GID Resolution**: 95%+ (up from current 78%)

**Expected improvements**:
- ✅ VGA coverage: 8 → 25+ entries (300% increase)
- ✅ RAM system: String → Metaobject references (new capability)
- ✅ Storage coverage: 6 → 15+ entries (150% increase)  
- ✅ CPU standardization: Consistent naming convention
- ✅ Display standardization: Unified format
- ✅ Gap analysis tool: Automated coverage monitoring
- ✅ Overall GID resolution: 78% → 95%+

**Implementation Priority**:
1. **Critical**: VGA expansion (biggest impact on GID resolution)
2. **High**: RAM metaobject system (architectural completion)
3. **Medium**: Storage expansion + CPU standardization
4. **Low**: Display standardization + analysis tool

**Estimated Time**: 4 hours total
**Expected Outcome**: Near-complete GID resolution with systematic gap monitoring