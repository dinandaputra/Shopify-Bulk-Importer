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
        Parse template string back to component data
        
        Args:
            template: Template string to parse
            
        Returns:
            Dict with parsed component data or None if parsing fails
        """
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
    
    def _find_model_data(self, model_key: str, spec_parts: List[str], color: str) -> Optional[Dict]:
        """
        Find original model data by matching template components
        
        Args:
            model_key: Full model name
            spec_parts: List of abbreviated spec components [cpu, ram, vga, display, storage]
            color: Color name
            
        Returns:
            Dict with original model data or None if not found
        """
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