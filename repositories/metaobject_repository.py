"""
Metaobject repository for data access abstraction.

This repository provides methods for accessing metaobject GID mappings
with caching to avoid repeated file reads. Implements the data access
layer for the laptop scalability refactor.
"""

import json
import os
from typing import Dict, Optional, List
from functools import lru_cache


class MetaobjectRepository:
    """
    Repository for metaobject GID mappings data access.
    
    Provides caching and unified access to all component type mappings
    stored in JSON files. Supports both individual component access
    and bulk operations for the laptop scalability system.
    """
    
    def __init__(self):
        """Initialize repository with base path for metaobject data."""
        self.base_path = "data/metaobjects/"
        self._cache = {}
    
    def get_processor_mapping(self) -> Dict[str, str]:
        """
        Get processor metaobject GID mappings.
        
        Returns:
            Dictionary mapping processor full names to their GIDs
        """
        return self._load_mapping("processors.json")
    
    def get_vga_mapping(self) -> Dict[str, str]:
        """
        Get VGA (dedicated graphics) metaobject GID mappings.
        
        Returns:
            Dictionary mapping VGA full names to their GIDs
        """
        return self._load_mapping("vga.json")
    
    def get_graphics_mapping(self) -> Dict[str, str]:
        """
        Get integrated graphics metaobject GID mappings.
        
        Returns:
            Dictionary mapping graphics full names to their GIDs
        """
        return self._load_mapping("graphics.json")
    
    def get_display_mapping(self) -> Dict[str, str]:
        """
        Get display metaobject GID mappings.
        
        Returns:
            Dictionary mapping display full names to their GIDs
        """
        return self._load_mapping("displays.json")
    
    def get_storage_mapping(self) -> Dict[str, str]:
        """
        Get storage metaobject GID mappings.
        
        Returns:
            Dictionary mapping storage full names to their GIDs
        """
        return self._load_mapping("storage.json")
    
    def get_color_mapping(self) -> Dict[str, str]:
        """
        Get color metaobject GID mappings.
        
        Returns:
            Dictionary mapping color full names to their GIDs
        """
        return self._load_mapping("colors.json")
    
    def get_os_mapping(self) -> Dict[str, str]:
        """
        Get operating system metaobject GID mappings.
        
        Returns:
            Dictionary mapping OS full names to their GIDs
        """
        return self._load_mapping("os.json")
    
    def get_keyboard_layout_mapping(self) -> Dict[str, str]:
        """
        Get keyboard layout metaobject GID mappings.
        
        Returns:
            Dictionary mapping keyboard layout full names to their GIDs
        """
        return self._load_mapping("keyboard_layouts.json")
    
    def get_keyboard_backlight_mapping(self) -> Dict[str, str]:
        """
        Get keyboard backlight metaobject GID mappings.
        
        Returns:
            Dictionary mapping keyboard backlight full names to their GIDs
        """
        return self._load_mapping("keyboard_backlights.json")
    
    def get_product_rank_laptop_mapping(self) -> Dict[str, str]:
        """
        Get product rank (laptop) metaobject GID mappings.
        
        Returns:
            Dictionary mapping product rank names to their GIDs
        """
        return self._load_mapping("product_rank_laptop.json")
    
    def get_product_inclusion_laptop_mapping(self) -> Dict[str, str]:
        """
        Get product inclusion (laptop) metaobject GID mappings.
        
        Returns:
            Dictionary mapping product inclusion names to their GIDs
        """
        return self._load_mapping("product_inclusion_laptop.json")
    
    def get_minus_mapping(self) -> Dict[str, str]:
        """
        Get minus/issues metaobject GID mappings.
        
        Returns:
            Dictionary mapping minus/issue names to their GIDs
        """
        return self._load_mapping("minus.json")
    
    def get_gid(self, component_type: str, full_name: str) -> Optional[str]:
        """
        Get GID for component by type and full name (unified lookup).
        
        Args:
            component_type: Type of component (processor, vga, graphics, etc.)
            full_name: Full component name as it appears in data
            
        Returns:
            GID string if found, None otherwise
        """
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
            "product_rank_laptop": self.get_product_rank_laptop_mapping,
            "product_inclusion_laptop": self.get_product_inclusion_laptop_mapping,
            "minus": self.get_minus_mapping,
        }
        
        if component_type in mapping_methods:
            mapping = mapping_methods[component_type]()
            return mapping.get(full_name)
        
        return None
    
    def get_all_component_types(self) -> List[str]:
        """
        Get list of all available component types.
        
        Returns:
            List of component type names
        """
        return [
            "processor", "vga", "graphics", "display", "storage",
            "color", "os", "keyboard_layout", "keyboard_backlight",
            "product_rank_laptop", "product_inclusion_laptop", "minus"
        ]
    
    def get_component_options(self, component_type: str) -> List[str]:
        """
        Get all available options for a specific component type.
        
        Args:
            component_type: Type of component
            
        Returns:
            Sorted list of available component full names
        """
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
            "product_rank_laptop": self.get_product_rank_laptop_mapping,
            "product_inclusion_laptop": self.get_product_inclusion_laptop_mapping,
            "minus": self.get_minus_mapping,
        }
        
        if component_type in mapping_methods:
            try:
                mapping = mapping_methods[component_type]()
                return sorted(mapping.keys())
            except (FileNotFoundError, json.JSONDecodeError):
                return []
        
        return []
    
    def _load_mapping(self, filename: str) -> Dict[str, str]:
        """
        Load mapping from JSON file with caching.
        
        Args:
            filename: Name of the JSON mapping file
            
        Returns:
            Dictionary mapping full names to GIDs
            
        Raises:
            FileNotFoundError: If mapping file doesn't exist
            json.JSONDecodeError: If JSON file is invalid
        """
        if filename not in self._cache:
            file_path = os.path.join(self.base_path, filename)
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Metaobject mapping file not found: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self._cache[filename] = json.load(f)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Invalid JSON in {file_path}: {str(e)}", e.doc, e.pos)
        
        return self._cache[filename]
    
    def clear_cache(self) -> None:
        """Clear the internal cache to force reload of mappings."""
        self._cache.clear()
    
    def get_cache_info(self) -> Dict[str, int]:
        """
        Get information about cached mappings.
        
        Returns:
            Dictionary with filename keys and count values
        """
        return {filename: len(mapping) for filename, mapping in self._cache.items()}