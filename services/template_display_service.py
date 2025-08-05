import re
from typing import Dict, List, Tuple


class TemplateDisplayService:
    """
    Service for converting full component names to template-friendly abbreviations
    and generating template strings in the format:
    "ASUS TUF F15 FX507ZV4 [i7-12700H/16GB/RTX 4060/144Hz/512GB SSD] [Graphite Black]"
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
        """
        Generate template string for a specific configuration
        
        Args:
            model_key: Full model name (e.g., "ASUS TUF F15 FX507ZV4")
            config: Configuration dict with cpu, ram, vga, display, storage
            color: Color name
            
        Returns:
            Template string in format: "Model [cpu/ram/vga/display/storage] [color]"
        """
        components = [
            self.abbreviate_for_template(config["cpu"], "cpu"),
            config["ram"],  # Already simple: "16GB"
            self.abbreviate_for_template(config["vga"], "vga"),
            self.abbreviate_for_template(config["display"], "display"),
            config["storage"]  # Already simple: "512GB SSD"
        ]
        
        spec_string = "/".join(components)
        return f"{model_key} [{spec_string}] [{color}]"
    
    def clear_cache(self):
        """Clear the abbreviation cache - useful for testing or memory management"""
        self._abbreviation_cache.clear()
    
    def get_cache_size(self) -> int:
        """Get current cache size - useful for monitoring"""
        return len(self._abbreviation_cache)