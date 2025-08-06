import re
from typing import Dict, List, Tuple


# Standardized component naming - abbreviated to detailed format mapping
STANDARDIZED_COMPONENTS = {
    "cpu": {
        # Intel processors (abbreviated -> detailed format matching Shopify metaobjects)
        "i7-12700H": "Intel Core i7-12700H (16 CPUs), ~2.3GHz",
        "i7-12650H": "Intel Core i7-12650H (16 CPUs), ~2.3GHz", 
        "i5-12500H": "Intel Core i5-12500H (12 CPUs), ~3.1GHz",
        "i5-11400H": "Intel Core i5-11400H (12 CPUs), ~2.7GHz",
        "i7-11800H": "Intel Core i7-11800H (16 CPUs), ~2.3GHz",
        "i9-12900H": "Intel Core i9-12900H (20 CPUs), ~2.5GHz",
        "i7-13700H": "Intel Core i7-13700H (20 CPUs), ~2.4GHz",
        "i9-13900H": "Intel Core i9-13900H (20 CPUs), ~2.6GHz",
        "i5-13500H": "Intel Core i5-13500H (16 CPUs), ~2.6GHz",
        "i7-14700HX": "Intel Core i7-14700HX (20 CPUs), ~2.1GHz",
        "i9-14900HX": "Intel Core i9-14900HX (24 CPUs), ~2.2GHz",
        "i7-9750H": "Intel Core i7-9750H (12 CPUs), ~2.6GHz",
        "i5-10300H": "Intel Core i5-10300H (8 CPUs), ~2.5GHz",
        "i7-10750H": "Intel Core i7-10750H (12 CPUs), ~2.6GHz",
        "i7-11370H": "Intel Core i7-11370H (8 CPUs), ~3.3GHz",
        "i9-11900H": "Intel Core i9-11900H (16 CPUs), ~2.5GHz",
        
        # AMD processors
        "Ryzen 7 5800H": "AMD Ryzen 7 5800H (16 CPUs), ~3.2GHz",
        "Ryzen 5 5600H": "AMD Ryzen 5 5600H (12 CPUs), ~3.3GHz",
        "Ryzen 7 6800H": "AMD Ryzen 7 6800H (16 CPUs), ~3.2GHz",
        "Ryzen 9 5900HX": "AMD Ryzen 9 5900HX (16 CPUs), ~3.3GHz",
        "Ryzen 7 4800H": "AMD Ryzen 7 4800H (16 CPUs), ~2.9GHz",
        "Ryzen 5 4600H": "AMD Ryzen 5 4600H (12 CPUs), ~3.0GHz",
        "Ryzen 9 6900HX": "AMD Ryzen 9 6900HX (16 CPUs), ~3.3GHz",
        "Ryzen 7 7735HS": "AMD Ryzen 7 7735HS (16 CPUs), ~3.2GHz",
        "Ryzen 9 7940HS": "AMD Ryzen 9 7940HS (16 CPUs), ~4.0GHz",
        "Ryzen 9 8945HS": "AMD Ryzen 9 8945HS (16 CPUs), ~4.0GHz",
        "Ryzen 7 7040": "AMD Ryzen 7 7040 (16 CPUs), ~3.8GHz",
    },
    
    "ram": {
        "8GB": "8GB DDR4",
        "16GB": "16GB DDR4", 
        "32GB": "32GB DDR4",
        "64GB": "64GB DDR4"
    },
    
    "gpu": {
        # NVIDIA RTX 40 series (abbreviated -> detailed format)
        "RTX 4090": "NVIDIA GeForce RTX 4090 16GB",
        "RTX 4080": "NVIDIA GeForce RTX 4080 16GB",
        "RTX 4070": "NVIDIA GeForce RTX 4070 12GB",
        "RTX 4060": "NVIDIA GeForce RTX 4060 8GB",
        "RTX 4050": "NVIDIA GeForce RTX 4050 6GB",
        
        # NVIDIA RTX 30 series
        "RTX 3080": "NVIDIA GeForce RTX 3080 10GB",
        "RTX 3070": "NVIDIA GeForce RTX 3070 8GB",
        "RTX 3060": "NVIDIA GeForce RTX 3060 6GB",
        "RTX 3050": "NVIDIA GeForce RTX 3050 4GB",
        "RTX 3080 Ti": "NVIDIA GeForce RTX 3080 Ti 12GB",
        "RTX 3070 Ti": "NVIDIA GeForce RTX 3070 Ti 8GB",
        
        # NVIDIA RTX 20 series
        "RTX 2070": "NVIDIA GeForce RTX 2070 8GB",
        "RTX 2080": "NVIDIA GeForce RTX 2080 8GB",
        "RTX 2060": "NVIDIA GeForce RTX 2060 6GB",
        
        # NVIDIA GTX series
        "GTX 1650": "NVIDIA GeForce GTX 1650 4GB",
        "GTX 1650 Ti": "NVIDIA GeForce GTX 1650 Ti 4GB",
        "GTX 1660 Ti": "NVIDIA GeForce GTX 1660 Ti 6GB",
        
        # AMD graphics
        "RX 6600M": "AMD Radeon RX 6600M 8GB",
        "RX 6700M": "AMD Radeon RX 6700M 10GB",
        
        # Integrated graphics (these will map to graphics field)
        "Integrated": "Intel Iris Xe Graphics",
        "Intel UHD": "Intel UHD Graphics",
        "Intel Iris Xe": "Intel Iris Xe Graphics",
        "AMD Radeon": "AMD Radeon Graphics",
        "Apple GPU": "Apple GPU (M1)",
    },
    
    "display": {
        # Abbreviated -> detailed format matching Shopify metaobjects
        "144Hz": "15-inch FHD (144Hz)",
        "120Hz": "15-inch FHD (120Hz)", 
        "60Hz": "15-inch FHD (60Hz)",
        "17.3 144Hz": "17.3-inch FHD (144Hz)",
        "14 60Hz": "14-inch FHD (60Hz)",
        "13.3 60Hz": "13.3-inch FHD (60Hz)",
        "4K": "15-inch 4K UHD (60Hz)",
        "QHD 165Hz": "15-inch QHD (165Hz)",
        "165Hz": "15-inch FHD (165Hz)",
        "17.3 165Hz": "17.3-inch FHD (165Hz)",
        "14 QHD 120Hz": "14-inch QHD (120Hz)",
        "240Hz": "15-inch FHD (240Hz)",
        "17.3 240Hz": "17.3-inch FHD (240Hz)",
        "QHD 240Hz": "15-inch QHD (240Hz)",
        "300Hz": "15-inch FHD (300Hz)",
        "14 OLED 120Hz": "14-inch OLED (120Hz)",
        "16 OLED 240Hz": "16-inch OLED (240Hz)",
    },
    
    "storage": {
        # Abbreviated -> detailed format matching Shopify metaobjects
        "256GB": "256GB SSD",
        "512GB": "512GB SSD", 
        "1TB": "1TB SSD",
        "2TB": "2TB SSD",
        "1TB+256GB": "1TB HDD + 256GB SSD",
    }
}


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
    
    def get_abbreviated_component_name(self, component_type: str, detailed_name: str) -> str:
        """
        Convert detailed component name back to abbreviated name for metafield processing
        
        This is a reverse lookup function that finds the abbreviated name from 
        a detailed name using the STANDARDIZED_COMPONENTS mapping.
        
        Args:
            component_type: Type of component ('cpu', 'gpu', 'display', 'storage', 'ram')
            detailed_name: Detailed name like 'Intel Core i7-11370H (8 CPUs), ~3.3GHz'
            
        Returns:
            Abbreviated name like 'i7-11370H' for metafield lookup
        """
        if component_type not in STANDARDIZED_COMPONENTS:
            return detailed_name
        
        # Reverse lookup: find abbreviated name from detailed name
        for abbreviated, detailed in STANDARDIZED_COMPONENTS[component_type].items():
            if detailed == detailed_name:
                return abbreviated
        
        return detailed_name