# Template Parsing Fix - Focused Implementation Plan

## 🎯 **Executive Summary**
This plan focuses specifically on fixing the template field population issue by implementing the minimum viable components from the LAPTOP_SCALABILITY_REFACTOR_PLAN.md needed to resolve template parsing failures.

## 🔍 **Problem Analysis**

### **Root Cause**
- Template parsing in `services/template_cache_service.py` fails to convert abbreviated components back to full names
- `_find_model_data()` method cannot reliably match abbreviated specs with original JSON data
- Form fields in `pages/laptop_entry.py` expect full component names but receive None or incomplete data

### **Current Failure Pattern**
```python
# Current broken flow:
template = "ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB SSD] [Graphite Black]"
template_info = template_service.parse_template(template)
# Returns: None or incomplete data
# Result: Form fields remain empty
```

### **Expected Success Pattern**
```python
# Fixed flow should return:
template_info = {
    'cpu': 'Intel Core i7-12700H (16 CPUs), ~2.3GHz',    # FULL NAME
    'vga': 'NVIDIA GeForce RTX 4060 8GB',                # FULL NAME  
    'display': '15.6" FHD 144Hz',                         # FULL NAME
    'storage': '512GB SSD',                               # FULL NAME
    'color': 'Graphite Black'                             # COLOR
}
# Result: All form fields populate correctly
```

## 🚀 **Implementation Strategy**

### **Phase 1: Core Template Parsing Fix (2-3 hours)**

#### **Task 1.1: Create Template Display Service (30 minutes)**
**Goal**: Implement reliable abbreviation logic for template components

**File**: `services/template_display_service.py`

```python
import re
from typing import Dict

class TemplateDisplayService:
    """
    Service for converting full component names to template-friendly abbreviations
    and generating template strings with consistent patterns
    """
    
    def __init__(self):
        self._abbreviation_cache = {}
    
    def abbreviate_for_template(self, full_name: str, component_type: str) -> str:
        """
        Convert full component name to template-friendly abbreviation
        
        Args:
            full_name: Full component name (e.g., "Intel Core i7-12700H (20 CPUs), ~2.3GHz")
            component_type: Type of component (cpu, vga, display, ram, storage)
            
        Returns:
            Abbreviated name for template display (e.g., "i7-12700H")
        """
        cache_key = f"{component_type}:{full_name}"
        
        if cache_key not in self._abbreviation_cache:
            self._abbreviation_cache[cache_key] = self._calculate_abbreviation(full_name, component_type)
        
        return self._abbreviation_cache[cache_key]
    
    def _calculate_abbreviation(self, full_name: str, component_type: str) -> str:
        """Calculate abbreviation based on component type with robust error handling"""
        try:
            if component_type == "cpu":
                # "Intel Core i7-12700H (20 CPUs), ~2.3GHz" → "i7-12700H"
                if "Intel Core" in full_name:
                    match = re.search(r'Intel Core (i\d+-\w+)', full_name)
                    return match.group(1) if match else full_name
                elif "AMD Ryzen" in full_name:
                    # "AMD Ryzen 7 4800H (16 CPUs), ~2.9GHz" → "Ryzen 7 4800H"
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
                    # Extract model number from AMD cards
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
                    # Fallback: return as-is for unusual displays
                    return full_name
            
            elif component_type in ["ram", "storage"]:
                # These are already simple enough for templates
                return full_name
            
            return full_name
            
        except Exception as e:
            print(f"Warning: Error abbreviating {component_type} '{full_name}': {e}")
            return full_name  # Fallback to original name
    
    def generate_template_string(self, model_key: str, config: Dict, color: str) -> str:
        """
        Generate template string for a specific configuration
        
        Args:
            model_key: Full model name (e.g., "ASUS TUF F15 FX507ZV4")
            config: Configuration dict with cpu, ram, vga, display, storage
            color: Color name
            
        Returns:
            Template string in format: "Model [cpu/ram/vga/display/storage] [color]"
        """
        try:
            components = [
                self.abbreviate_for_template(config.get("cpu", ""), "cpu"),
                config.get("ram", ""),  # Already simple: "16GB"
                self.abbreviate_for_template(config.get("vga", ""), "vga"),
                self.abbreviate_for_template(config.get("display", ""), "display"),
                config.get("storage", "")  # Already simple: "512GB SSD"
            ]
            
            spec_string = "/".join(components)
            return f"{model_key} [{spec_string}] [{color}]"
        except Exception as e:
            print(f"Error generating template for {model_key}: {e}")
            return f"{model_key} [Error] [{color}]"
    
    def clear_cache(self):
        """Clear the abbreviation cache - useful for testing or memory management"""
        self._abbreviation_cache.clear()
```

**Validation**:
```python
# Test abbreviation logic
service = TemplateDisplayService()
assert service.abbreviate_for_template("Intel Core i7-12700H (16 CPUs), ~2.3GHz", "cpu") == "i7-12700H"
assert service.abbreviate_for_template("NVIDIA GeForce RTX 4060 8GB", "vga") == "RTX 4060"
```

---

#### **Task 1.2: Create Product Data Repository (30 minutes)**
**Goal**: Provide data access for template parsing using current laptop specs

**File**: `repositories/product_data_repository.py`

```python
import json
from typing import Dict, List
from config.laptop_specs import LAPTOP_SPECS  # Use existing data temporarily

class ProductDataRepository:
    """
    Repository for accessing laptop product data
    Currently uses existing LAPTOP_SPECS data with format adaptation
    """
    
    def __init__(self):
        self.laptop_data = LAPTOP_SPECS
    
    def get_all_models(self) -> Dict[str, Dict]:
        """
        Convert current laptop specs to expected format for template parsing
        
        Returns:
            Dict with model_key as key and model data as value
        """
        all_models = {}
        
        try:
            for brand, models in self.laptop_data.items():
                for model_key, model_data in models.items():
                    # Transform to expected structure
                    all_models[model_key] = {
                        "configurations": [model_data],  # Wrap single config in array
                        "colors": model_data.get("colors", ["Black"]),  # Default color if missing
                        "brand": brand
                    }
            
            print(f"📊 Loaded {len(all_models)} laptop models from {len(self.laptop_data)} brands")
            return all_models
            
        except Exception as e:
            print(f"❌ Error loading laptop models: {e}")
            return {}
    
    def get_brand_data(self, brand: str) -> Dict:
        """
        Get data for specific brand (for future expansion)
        
        Args:
            brand: Brand name (e.g., "ASUS")
            
        Returns:
            Brand data dict
        """
        return self.laptop_data.get(brand, {})
    
    def get_all_brands(self) -> List[str]:
        """Get list of available brands"""
        return list(self.laptop_data.keys())
    
    def validate_data_integrity(self) -> Dict[str, int]:
        """
        Validate current laptop data integrity
        
        Returns:
            Dict with validation statistics
        """
        stats = {
            "total_brands": 0,
            "total_models": 0,
            "models_with_colors": 0,
            "models_missing_cpu": 0,
            "models_missing_vga": 0
        }
        
        try:
            for brand, models in self.laptop_data.items():
                stats["total_brands"] += 1
                for model_key, model_data in models.items():
                    stats["total_models"] += 1
                    
                    if model_data.get("colors"):
                        stats["models_with_colors"] += 1
                    if not model_data.get("cpu"):
                        stats["models_missing_cpu"] += 1
                    if not model_data.get("vga"):
                        stats["models_missing_vga"] += 1
            
            print(f"📈 Data integrity: {stats}")
            return stats
            
        except Exception as e:
            print(f"❌ Error validating data: {e}")
            return stats
```

**Validation**:
```python
# Test repository functionality
repo = ProductDataRepository()
models = repo.get_all_models()
assert len(models) > 0, "Should load laptop models"
assert "ASUS TUF F15 FX507ZV4" in models, "Should contain known model"
```

---

#### **Task 1.3: Create Fixed Template Cache Service (1 hour)**
**Goal**: Implement robust template parsing that returns full component names

**File**: `services/template_cache_service.py`

```python
import os
import json
from typing import List, Dict, Optional
from repositories.product_data_repository import ProductDataRepository
from services.template_display_service import TemplateDisplayService

class TemplateCacheService:
    """
    Service for auto-generating template cache with file persistence.
    Fixed version that properly parses templates back to full component names.
    """
    
    def __init__(self):
        self.product_repo = ProductDataRepository()
        self.display_service = TemplateDisplayService()
        self.cache_file = "data/cache/template_cache.json"
        
        # Ensure cache directory exists
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
    
    def get_all_templates(self) -> List[str]:
        """
        Get all laptop templates, using cache if available or generating from current data
        
        Returns:
            List of template strings sorted alphabetically
        """
        try:
            # Try to load existing template cache first
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                return cache_data.get("templates", [])
        except Exception as e:
            print(f"Warning: Could not load template cache: {e}")
        
        # Fallback: use current template generation if available
        try:
            from config.laptop_specs import generate_all_laptop_templates
            templates = generate_all_laptop_templates()
            print(f"📋 Loaded {len(templates)} templates from legacy system")
            return templates
        except ImportError as e:
            print(f"Warning: Could not import legacy templates: {e}")
            return []
    
    def parse_template(self, template: str) -> Optional[Dict[str, str]]:
        """
        Parse template string back to component data with comprehensive error handling
        
        Args:
            template: Template string to parse
            
        Returns:
            Dict with parsed component data or None if parsing fails
        """
        if not template or template == "":
            return None
            
        try:
            print(f"🔍 Parsing template: {template}")
            
            # Extract model name (everything before first bracket)
            if '[' not in template:
                print(f"❌ Invalid template format: no brackets found")
                return None
                
            model_match = template.split('[')[0].strip()
            
            # Extract spec string (between first brackets)
            spec_start = template.find('[') + 1
            spec_end = template.find(']', spec_start)
            if spec_start == 0 or spec_end == -1:
                print(f"❌ Invalid template format: malformed brackets")
                return None
                
            spec_string = template[spec_start:spec_end]
            
            # Extract color (between second brackets)
            color_start = template.find('[', spec_end) + 1
            color_end = template.find(']', color_start)
            if color_start == 0 or color_end == -1:
                print(f"❌ Invalid template format: missing color brackets")
                return None
                
            color = template[color_start:color_end]
            
            # Parse spec components
            spec_parts = spec_string.split('/')
            if len(spec_parts) != 5:
                print(f"❌ Invalid spec format: expected 5 parts (cpu/ram/vga/display/storage), got {len(spec_parts)}: {spec_parts}")
                return None
            
            print(f"📋 Extracted components:")
            print(f"  Model: {model_match}")
            print(f"  Spec parts: {spec_parts}")
            print(f"  Color: {color}")
            
            # Find the original model data
            model_data = self._find_model_data(model_match, spec_parts, color)
            
            if model_data:
                # Construct comprehensive result with both abbreviated and full names
                result = {
                    'model': model_match,
                    'brand': model_data.get('brand', 'Unknown'),
                    'title': model_match,  # For form title field
                    
                    # CPU fields (both abbreviated and full)
                    'cpu': model_data.get('cpu', ''),
                    'cpu_full': model_data.get('cpu', ''),
                    
                    # RAM fields (keep as-is since it's already simple)
                    'ram': spec_parts[1],
                    'ram_full': spec_parts[1],
                    
                    # VGA/GPU fields (dedicated graphics)
                    'vga': model_data.get('vga', ''),
                    'gpu': model_data.get('gpu', model_data.get('integrated_graphics', '')),
                    'gpu_full': model_data.get('gpu', model_data.get('integrated_graphics', '')),
                    
                    # Display fields
                    'display': model_data.get('display', ''),
                    'display_full': model_data.get('display', ''),
                    
                    # Storage fields (keep as-is since it's already simple)
                    'storage': spec_parts[4],
                    'storage_full': spec_parts[4],
                    
                    # Color and other fields
                    'color': color,
                    'os': model_data.get('os', 'Windows 11'),
                    'keyboard_layout': model_data.get('keyboard_layout', 'US - International Keyboard'),
                    'keyboard_backlight': model_data.get('keyboard_backlight', 'Yes'),
                    
                    # Keep original template for reference
                    'template': template
                }
                
                print(f"✅ Successfully parsed template: {len([k for k, v in result.items() if v])} fields populated")
                print(f"  CPU: {result['cpu'][:50]}..." if result['cpu'] else "  CPU: (empty)")
                print(f"  VGA: {result['vga'][:50]}..." if result['vga'] else "  VGA: (empty)")
                return result
            else:
                print(f"❌ Could not find model data for: {model_match}")
                return None
            
        except Exception as e:
            print(f"❌ Error parsing template: {template}")
            print(f"   Error details: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _find_model_data(self, model_key: str, spec_parts: List[str], color: str) -> Optional[Dict]:
        """
        Find original model data by matching template components with robust matching
        
        Args:
            model_key: Full model name
            spec_parts: List of abbreviated spec components [cpu, ram, vga, display, storage]
            color: Color name
            
        Returns:
            Dict with original model data or None if not found
        """
        try:
            all_models = self.product_repo.get_all_models()
            print(f"🔍 Looking for model: {model_key}")
            print(f"🔍 Available models: {len(all_models)} total")
            
            if model_key not in all_models:
                # Try fuzzy matching for slight variations
                similar_models = [m for m in all_models.keys() if model_key in m or m in model_key]
                if similar_models:
                    print(f"❓ Exact model not found, similar models: {similar_models[:3]}")
                else:
                    print(f"❌ Model not found in data: {model_key}")
                return None
            
            model_spec = all_models[model_key]
            print(f"✅ Found model in data")
            
            # Find matching configuration
            configurations = model_spec.get("configurations", [])
            print(f"🔍 Checking {len(configurations)} configurations")
            
            for i, config in enumerate(configurations):
                print(f"🔍 Configuration {i+1}:")
                
                # Component matching with detailed logging
                cpu_match = self._component_matches("cpu", config.get("cpu", ""), spec_parts[0])
                ram_match = config.get("ram", "") == spec_parts[1]
                vga_match = self._component_matches("vga", config.get("vga", ""), spec_parts[2])
                display_match = self._component_matches("display", config.get("display", ""), spec_parts[3])
                storage_match = config.get("storage", "") == spec_parts[4]
                color_match = color in model_spec.get("colors", [])
                
                print(f"  ✓ CPU: {cpu_match} ({config.get('cpu', '')[:30]}... vs {spec_parts[0]})")
                print(f"  ✓ RAM: {ram_match} ({config.get('ram', '')} vs {spec_parts[1]})")
                print(f"  ✓ VGA: {vga_match} ({config.get('vga', '')[:30]}... vs {spec_parts[2]})")
                print(f"  ✓ Display: {display_match} ({config.get('display', '')[:30]}... vs {spec_parts[3]})")
                print(f"  ✓ Storage: {storage_match} ({config.get('storage', '')} vs {spec_parts[4]})")
                print(f"  ✓ Color: {color_match} ({color} in {model_spec.get('colors', [])})")
                
                # Check if all components match
                all_match = cpu_match and ram_match and vga_match and display_match and storage_match and color_match
                match_count = sum([cpu_match, ram_match, vga_match, display_match, storage_match, color_match])
                
                print(f"  📊 Match score: {match_count}/6")
                
                if all_match:
                    print("✅ Perfect match found!")
                    return {
                        'brand': model_spec.get('brand', 'Unknown'),
                        **config
                    }
                elif match_count >= 4:  # Allow partial matches for flexibility
                    print(f"⚠️ Partial match found ({match_count}/6), using anyway")
                    return {
                        'brand': model_spec.get('brand', 'Unknown'),
                        **config
                    }
            
            print("❌ No matching configuration found")
            return None
            
        except Exception as e:
            print(f"❌ Error in _find_model_data: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _component_matches(self, component_type: str, full_component: str, abbreviated: str) -> bool:
        """
        Check if abbreviated component matches full component with error handling
        
        Args:
            component_type: Type of component (cpu, vga, display)
            full_component: Full component name from data
            abbreviated: Abbreviated component from template
            
        Returns:
            True if components match, False otherwise
        """
        try:
            if not full_component or not abbreviated:
                return False
                
            calculated_abbrev = self.display_service.abbreviate_for_template(full_component, component_type)
            matches = calculated_abbrev == abbreviated
            
            if not matches and component_type in ["cpu", "vga", "display"]:
                # Try alternative matching patterns for flexibility
                if component_type == "cpu":
                    # Alternative CPU matching patterns
                    matches = (abbreviated in full_component or 
                              full_component.replace("Intel Core ", "").startswith(abbreviated))
                elif component_type == "vga":
                    # Alternative VGA matching patterns
                    matches = abbreviated in full_component
                elif component_type == "display":
                    # Alternative display matching patterns
                    matches = abbreviated in full_component or full_component in abbreviated
            
            return matches
            
        except Exception as e:
            print(f"❌ Error matching {component_type}: {e}")
            return False
    
    def get_cache_info(self) -> Dict:
        """
        Get information about the current cache
        
        Returns:
            Dict with cache metadata
        """
        if not os.path.exists(self.cache_file):
            return {"exists": False, "message": "Cache file not found"}
        
        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
            
            return {
                "exists": True,
                "generated_at": cache_data.get("generated_at"),
                "total_templates": cache_data.get("total_templates"),
                "version": cache_data.get("version"),
                "file_size": os.path.getsize(self.cache_file)
            }
        except Exception as e:
            return {"exists": True, "error": str(e)}
    
    def clear_cache(self):
        """Remove the cache file - useful for testing or forced regeneration"""
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
            print("🗑️ Cache file removed")
```

**Validation**:
```python
# Test template parsing
service = TemplateCacheService()
templates = service.get_all_templates()
assert len(templates) > 0, "Should load templates"

# Test parsing a known template
test_template = "ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB SSD] [Graphite Black]"
result = service.parse_template(test_template)
assert result is not None, "Should parse template successfully"
assert result['cpu'] != '', "CPU should be populated"
assert "Intel Core" in result['cpu'], "Should return full CPU name"
```

---

#### **Task 1.4: Update UI Template Loading (30 minutes)**
**Goal**: Use new template service in laptop entry page with proper error handling

**File**: `pages/laptop_entry.py`

**Changes needed in the template selection section (around line 135-200):**

```python
# Add imports at the top of the file
from services.template_cache_service import TemplateCacheService

# Replace the template service initialization
@st.cache_resource
def get_template_service():
    """Initialize template cache service with error handling"""
    try:
        return TemplateCacheService()
    except Exception as e:
        st.error(f"Error initializing template service: {str(e)}")
        return None

# In the template selection section, replace the existing code:

# Template Selection Section - Updated with proper error handling
st.subheader("🔍 Select Laptop Template")
st.markdown("### 🔍 Product Information")
col1, col2 = st.columns([4, 1])

with col1:
    # Initialize template service with error handling
    template_service = get_template_service()
    
    if template_service is None:
        st.error("Template service unavailable. Please check system configuration.")
        st.stop()
    
    try:
        # Load all templates using the new service
        all_laptop_templates = template_service.get_all_templates()
        
        if not all_laptop_templates:
            st.warning("No laptop templates available. Please check data configuration.")
            all_laptop_templates = []
        
        # Template selection callback with comprehensive error handling
        def on_laptop_template_change():
            selected = st.session_state.laptop_template_selector
            if selected and selected != "":
                print(f"🔍 Template selected: {selected}")
                
                try:
                    extracted_info = template_service.parse_template(selected)
                    if extracted_info:
                        print(f"✅ Template parsed successfully: {len(extracted_info)} fields")
                        
                        # Initialize session state if needed
                        if 'laptop_form_data' not in st.session_state:
                            st.session_state.laptop_form_data = {}
                        
                        # Update session state with parsed data
                        st.session_state.laptop_form_data.update(extracted_info)
                        st.session_state.current_laptop_template = selected
                        
                        # Show success message
                        st.success(f"✅ Template loaded: {extracted_info.get('title', 'Laptop')}")
                    else:
                        print("❌ Template parsing failed")
                        st.error(f"Failed to parse template: {selected}")
                        st.error("Please try selecting a different template or contact support.")
                        
                except Exception as e:
                    print(f"❌ Error in template parsing: {e}")
                    st.error(f"Error processing template: {str(e)}")
                    st.error("Please try refreshing the page or selecting a different template.")
        
        # Template selector with improved error handling
        selected_template = st.selectbox(
            "Search and select laptop template:",
            [""] + all_laptop_templates,
            format_func=lambda x: x if x else "Type to search laptop templates...",
            key="laptop_template_selector",
            help="Type part of laptop brand, model, or specs to filter (e.g., 'ASUS i7', 'Dell RTX 4060', 'HP Gaming')",
            on_change=on_laptop_template_change
        )
        
        # Show current template info if selected with better error handling
        if selected_template and selected_template != "":
            try:
                extracted_info = template_service.parse_template(selected_template)
                if extracted_info:
                    brand = extracted_info.get('brand', 'Laptop')
                    brand_emoji = "💻" if brand == "ASUS" else "🖥️" if brand == "Dell" else "⚡" if brand == "HP" else "💻"
                    
                    # Show success message with extracted info
                    st.success(f"✅ **{extracted_info.get('title', selected_template)}**")
                    
                    # Show quick preview of extracted specs with null checks
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        cpu_info = extracted_info.get('cpu', 'N/A')
                        if extracted_info.get('ram'):
                            cpu_info += f" / {extracted_info.get('ram')}"
                        st.caption(f"{brand_emoji} {cpu_info[:30]}..." if len(cpu_info) > 30 else f"{brand_emoji} {cpu_info}")
                    with col_b:
                        gpu_info = extracted_info.get('gpu') or extracted_info.get('vga', 'N/A')
                        st.caption(f"🎮 {gpu_info[:20]}..." if len(gpu_info) > 20 else f"🎮 {gpu_info}")
                    with col_c:
                        storage_info = extracted_info.get('storage', 'N/A')
                        st.caption(f"💾 {storage_info}")
                else:
                    st.warning("⚠️ Template selected but could not be parsed. Form fields may be empty.")
            except Exception as e:
                st.error(f"Error displaying template info: {str(e)}")
        
    except Exception as e:
        st.error(f"Error loading laptop templates: {str(e)}")
        st.error("Falling back to manual entry mode.")
        
        # Fallback to empty template selector
        selected_template = st.selectbox(
            "Search and select laptop template:",
            [""],
            help="Template loading failed - you can still create products manually"
        )

with col2:
    # Keep existing quick tips
    st.markdown("##### Quick Tips")
    st.caption("💡 Type to search")
    st.caption("💻 All laptop brands")
    st.caption("⚡ Auto-fills all fields")
    st.caption("✏️ All fields editable")
    st.caption("🔧 Manual entry if needed")
```

---

### **Phase 2: Testing & Validation (30 minutes)**

#### **Task 2.1: Create Template Parsing Test**
**Goal**: Verify template parsing works correctly

**File**: `tests/test_template_parsing_fix.py`

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.template_cache_service import TemplateCacheService
from services.template_display_service import TemplateDisplayService
from repositories.product_data_repository import ProductDataRepository

def test_template_parsing():
    """Test that templates parse correctly and return full component names"""
    print("🧪 Testing template parsing functionality...")
    
    service = TemplateCacheService()
    
    # Test with a known template
    test_template = "ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB SSD] [Graphite Black]"
    print(f"Testing template: {test_template}")
    
    result = service.parse_template(test_template)
    
    # Basic validation
    assert result is not None, "Template parsing should not return None"
    print("✅ Template parsing returned data")
    
    # Field validation
    assert result.get('cpu', '') != '', "CPU field should be populated"
    assert result.get('vga', '') != '', "VGA field should be populated" 
    assert result.get('display', '') != '', "Display field should be populated"
    print("✅ Core fields are populated")
    
    # Content validation - ensure we got full names, not abbreviations
    cpu = result.get('cpu', '')
    vga = result.get('vga', '')
    
    assert len(cpu) > 10, f"CPU should be full name, not abbreviation. Got: {cpu}"
    assert "Intel Core" in cpu or "AMD Ryzen" in cpu, f"CPU should contain full manufacturer name. Got: {cpu}"
    
    assert len(vga) > 10, f"VGA should be full name, not abbreviation. Got: {vga}"
    assert "NVIDIA GeForce" in vga or "AMD Radeon" in vga, f"VGA should contain full manufacturer name. Got: {vga}"
    
    print("✅ Full component names verified")
    
    # Print results for manual verification
    print("\n📋 Parsed template results:")
    for key, value in result.items():
        if key not in ['template']:  # Skip the original template
            print(f"  {key}: {value}")
    
    print("✅ Template parsing test passed!")
    return True

def test_abbreviation_service():
    """Test abbreviation logic works correctly"""
    print("\n🧪 Testing abbreviation service...")
    
    service = TemplateDisplayService()
    
    # Test CPU abbreviation
    test_cases = [
        {
            'full': "Intel Core i7-12700H (16 CPUs), ~2.3GHz",
            'type': "cpu",
            'expected': "i7-12700H"
        },
        {
            'full': "NVIDIA GeForce RTX 4060 8GB",
            'type': "vga",
            'expected': "RTX 4060"
        },
        {
            'full': "AMD Ryzen 7 4800H (16 CPUs), ~2.9GHz",
            'type': "cpu",
            'expected': "Ryzen 7 4800H"
        },
        {
            'full': "15.6\" FHD 144Hz",
            'type': "display",
            'expected': "144Hz"
        }
    ]
    
    for case in test_cases:
        result = service.abbreviate_for_template(case['full'], case['type'])
        print(f"  {case['type']}: '{case['full']}' → '{result}'")
        assert result == case['expected'], f"Expected '{case['expected']}', got '{result}'"
    
    print("✅ Abbreviation service test passed!")
    return True

def test_product_data_repository():
    """Test product data repository functionality"""
    print("\n🧪 Testing product data repository...")
    
    repo = ProductDataRepository()
    
    # Test data loading
    models = repo.get_all_models()
    assert len(models) > 0, "Repository should load laptop models"
    print(f"✅ Loaded {len(models)} models")
    
    # Test specific model exists
    test_model = "ASUS TUF F15 FX507ZV4"
    assert test_model in models, f"Should contain test model: {test_model}"
    print(f"✅ Found test model: {test_model}")
    
    # Test model structure
    model_data = models[test_model]
    assert "configurations" in model_data, "Model should have configurations"
    assert "colors" in model_data, "Model should have colors"
    assert "brand" in model_data, "Model should have brand"
    print("✅ Model structure validated")
    
    # Validate data integrity
    stats = repo.validate_data_integrity()
    print(f"📊 Data integrity stats: {stats}")
    
    print("✅ Product data repository test passed!")
    return True

def test_full_integration():
    """Test the complete flow from template selection to field population"""
    print("\n🧪 Testing full integration flow...")
    
    # Initialize all services
    template_service = TemplateCacheService()
    
    # Get available templates
    templates = template_service.get_all_templates()
    assert len(templates) > 0, "Should have available templates"
    print(f"✅ Found {len(templates)} available templates")
    
    # Test parsing multiple templates
    test_count = min(5, len(templates))  # Test first 5 templates
    successful_parses = 0
    
    for i in range(test_count):
        template = templates[i]
        result = template_service.parse_template(template)
        
        if result:
            successful_parses += 1
            print(f"  ✅ Parsed: {template[:50]}...")
        else:
            print(f"  ❌ Failed: {template[:50]}...")
    
    success_rate = (successful_parses / test_count) * 100
    print(f"📊 Parse success rate: {success_rate:.1f}% ({successful_parses}/{test_count})")
    
    # We expect at least 80% success rate
    assert success_rate >= 80, f"Parse success rate too low: {success_rate:.1f}%"
    
    print("✅ Full integration test passed!")
    return True

def run_all_tests():
    """Run all template parsing tests"""
    print("🚀 Starting Template Parsing Fix Tests")
    print("=" * 50)
    
    try:
        test_abbreviation_service()
        test_product_data_repository()
        test_template_parsing()
        test_full_integration()
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! Template parsing fix is working correctly.")
        print("✅ Ready for production use")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    if not success:
        sys.exit(1)
```

**Run with**:
```bash
cd /home/dinanda/Documents/Shopify-Bulk-Importer
python tests/test_template_parsing_fix.py
```

---

## 🎯 **Implementation Checklist**

### **Pre-Implementation Setup**
- [ ] Create `services/` directory if it doesn't exist
- [ ] Create `repositories/` directory if it doesn't exist  
- [ ] Create `tests/` directory if it doesn't exist
- [ ] Create `data/cache/` directory if it doesn't exist

### **Phase 1: Core Implementation**
- [ ] Create `services/template_display_service.py` with abbreviation logic
- [ ] Create `repositories/product_data_repository.py` with data access
- [ ] Create `services/template_cache_service.py` with fixed parsing
- [ ] Update `pages/laptop_entry.py` template loading section
- [ ] Test basic template loading and parsing

### **Phase 2: Validation**  
- [ ] Create `tests/test_template_parsing_fix.py` with comprehensive tests
- [ ] Run tests and verify all pass
- [ ] Manual test template selection in UI
- [ ] Verify form fields populate correctly
- [ ] Check console logs for any errors

### **Phase 3: Production Validation**
- [ ] Test with multiple laptop templates
- [ ] Verify different brands work (ASUS, Dell, HP, etc.)
- [ ] Test error handling with malformed templates
- [ ] Confirm no regressions in existing functionality

---

## 🚨 **Expected Results**

### **Before Fix**
```python
# User selects template
template = "ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB SSD] [Graphite Black]"
parsed = template_service.parse_template(template)
# Result: None or incomplete data
# Form fields: Empty or unpopulated
```

### **After Fix**  
```python
# User selects same template
template = "ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB SSD] [Graphite Black]"
parsed = template_service.parse_template(template)
# Result: Complete dict with full component names
{
    'cpu': 'Intel Core i7-12700H (16 CPUs), ~2.3GHz',    # ✅ FULL NAME
    'vga': 'NVIDIA GeForce RTX 4060 8GB',                # ✅ FULL NAME
    'display': '15.6" FHD 144Hz',                         # ✅ FULL NAME
    'storage': '512GB SSD',                               # ✅ POPULATED
    'color': 'Graphite Black',                            # ✅ POPULATED
    'ram': '16GB',                                        # ✅ POPULATED
    # ... all other fields populated
}
# Form fields: All populated with correct full component names
```

### **UI Experience**
- **Before**: User selects template → Form remains empty → Frustration
- **After**: User selects template → All fields populate instantly → Success message

---

## 🔧 **Troubleshooting Guide**

### **Common Issues & Solutions**

#### **Issue**: Templates not loading
```python
# Check template service initialization
template_service = get_template_service()
if template_service is None:
    # Check import errors or data file issues
```

#### **Issue**: Template parsing returns None
```python
# Enable debug logging in parse_template method
# Check console output for detailed error messages
# Verify template format matches expected pattern
```

#### **Issue**: Form fields still empty after template selection
```python
# Verify template parsing returns data
# Check session state updates in on_laptop_template_change
# Ensure form field mapping uses correct keys
```

#### **Issue**: CPU/VGA fields show abbreviations instead of full names
```python
# Check _find_model_data method for proper data return
# Verify original laptop specs data contains full names
# Test abbreviation service matching logic
```

---

## 📈 **Success Metrics**

1. **Template Parse Success Rate**: >90% of templates parse successfully
2. **Field Population Rate**: >95% of form fields populate when template selected
3. **Full Name Display**: CPU and VGA fields show full manufacturer names
4. **Error Rate**: <5% of template selections result in errors
5. **User Experience**: Template selection immediately populates form fields

---

## 🔄 **Rollback Plan**

If issues occur after implementation:

1. **Keep backup of original files**:
   ```bash
   cp pages/laptop_entry.py pages/laptop_entry.py.backup
   ```

2. **Quick rollback**:
   - Remove new service files
   - Restore original `laptop_entry.py`
   - Clear any new cache files

3. **Verify system returns to previous state**

---

## 🚀 **Next Steps**

After successful implementation of this fix:

1. **Monitor template parsing success rates**
2. **Gather user feedback on form field population**
3. **Consider implementing full LAPTOP_SCALABILITY_REFACTOR_PLAN.md**
4. **Add more comprehensive error handling**
5. **Optimize performance for large template lists**

---

## 📞 **Support Information**

- **Implementation Time**: 2-3 hours
- **Testing Time**: 30 minutes
- **Skills Required**: Python, Streamlit, basic debugging
- **Dependencies**: Existing laptop_specs data structure
- **Risk Level**: Low (focused fix with rollback plan)

This comprehensive plan ensures the template field population issue is resolved efficiently while maintaining system stability and providing clear validation steps.