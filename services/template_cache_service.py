import json
import os
import glob
from datetime import datetime
from typing import List, Dict, Optional
from repositories.product_data_repository import ProductDataRepository
from services.template_display_service import TemplateDisplayService


class TemplateCacheService:
    """
    Service for auto-generating template cache with file persistence.
    Generates all laptop templates from data/products/laptops/ JSON files
    and caches them in data/cache/template_cache.json with metadata.
    Auto-regenerates cache when source files are newer than cache.
    """
    
    def __init__(self):
        self.cache_file = "data/cache/template_cache.json"
        self.source_dir = "data/products/laptops/"
        self.product_repo = ProductDataRepository()
        self.display_service = TemplateDisplayService()
    
    def get_all_templates(self) -> List[str]:
        """
        Get all laptop templates, regenerating cache if needed
        
        Returns:
            List of template strings sorted alphabetically
        """
        if self.needs_regeneration():
            self.regenerate_cache()
        
        return self._load_cached_templates()
    
    def needs_regeneration(self) -> bool:
        """
        Check if template cache needs to be regenerated
        
        Returns:
            True if cache is missing or source files are newer than cache
        """
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
        """
        Generate templates for a specific brand
        
        Args:
            brand: Brand name (e.g., "ASUS", "Dell")
            
        Returns:
            List of template strings for this brand
        """
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
        """
        Load templates from cache file
        
        Returns:
            List of cached template strings
        """
        with open(self.cache_file, 'r') as f:
            cache_data = json.load(f)
        
        return cache_data["templates"]
    
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
                print(f"  CPU: {result['cpu'][:50]}...'" if result['cpu'] else "  CPU: (empty)")
                print(f"  VGA: {result['vga'][:50]}...'" if result['vga'] else "  VGA: (empty)")
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
            all_models = self.product_repo.get_all_models_legacy_format()
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
            return {"exists": False}
        
        with open(self.cache_file, 'r') as f:
            cache_data = json.load(f)
        
        return {
            "exists": True,
            "generated_at": cache_data.get("generated_at"),
            "total_templates": cache_data.get("total_templates"),
            "version": cache_data.get("version"),
            "file_size": os.path.getsize(self.cache_file),
            "needs_regeneration": self.needs_regeneration()
        }
    
    def clear_cache(self):
        """Remove the cache file - useful for testing or forced regeneration"""
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
            print("🗑️ Cache file removed")