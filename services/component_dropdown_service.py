from typing import List, Tuple, Dict, Optional
from repositories.metaobject_repository import MetaobjectRepository


class ComponentDropdownService:
    """
    Service for populating searchable dropdowns with component options.
    Supports all components: processors, VGA, graphics, displays, storage, 
    colors, OS, keyboard layouts/backlights.
    Includes "CUSTOM" options for user input and helper methods for finding dropdown indices.
    """
    
    def __init__(self):
        self.metaobject_repo = MetaobjectRepository()
    
    def get_processor_options(self) -> List[Tuple[str, str]]:
        """
        Get processor dropdown options as (value, display_name) tuples
        
        Returns:
            List of tuples with processor options including empty and custom options
        """
        mapping = self.metaobject_repo.get_processor_mapping()
        options = [("", "Select processor...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))  # Full name as both value and display
        
        # Add custom option
        options.append(("CUSTOM", "Other/Custom processor..."))
        return options
    
    def get_ram_options(self) -> List[str]:
        """
        Get common RAM options
        
        Returns:
            List of RAM options with empty option first
        """
        return ["", "8GB", "16GB", "32GB", "64GB"]
    
    def get_vga_options(self) -> List[Tuple[str, str]]:
        """
        Get VGA (dedicated graphics) dropdown options
        
        Returns:
            List of tuples with VGA options including empty and custom options
        """
        mapping = self.metaobject_repo.get_vga_mapping()
        options = [("", "Select dedicated graphics...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        options.append(("CUSTOM", "Other/Custom VGA..."))
        return options
    
    def get_graphics_options(self) -> List[Tuple[str, str]]:
        """
        Get integrated graphics dropdown options
        
        Returns:
            List of tuples with integrated graphics options including empty and custom options
        """
        mapping = self.metaobject_repo.get_graphics_mapping()
        options = [("", "Select integrated graphics...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        options.append(("CUSTOM", "Other/Custom graphics..."))
        return options
    
    def get_display_options(self) -> List[Tuple[str, str]]:
        """
        Get display dropdown options
        
        Returns:
            List of tuples with display options including empty and custom options
        """
        mapping = self.metaobject_repo.get_display_mapping()
        options = [("", "Select display...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        options.append(("CUSTOM", "Other/Custom display..."))
        return options
    
    def get_storage_options(self) -> List[Tuple[str, str]]:
        """
        Get storage dropdown options
        
        Returns:
            List of tuples with storage options including empty and custom options
        """
        mapping = self.metaobject_repo.get_storage_mapping()
        options = [("", "Select storage...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        options.append(("CUSTOM", "Other/Custom storage..."))
        return options
    
    def get_color_options(self) -> List[Tuple[str, str]]:
        """
        Get color dropdown options
        
        Returns:
            List of tuples with color options including empty and custom options
        """
        mapping = self.metaobject_repo.get_color_mapping()
        options = [("", "Select color...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        options.append(("CUSTOM", "Other/Custom color..."))
        return options
    
    def get_os_options(self) -> List[Tuple[str, str]]:
        """
        Get OS dropdown options
        
        Returns:
            List of tuples with OS options including empty option
        """
        mapping = self.metaobject_repo.get_os_mapping()
        options = [("", "Select OS...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        return options
    
    def get_keyboard_layout_options(self) -> List[Tuple[str, str]]:
        """
        Get keyboard layout dropdown options
        
        Returns:
            List of tuples with keyboard layout options including empty option
        """
        mapping = self.metaobject_repo.get_keyboard_layout_mapping()
        options = [("", "Select keyboard layout...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        return options
    
    def get_keyboard_backlight_options(self) -> List[Tuple[str, str]]:
        """
        Get keyboard backlight dropdown options
        
        Returns:
            List of tuples with keyboard backlight options including empty option
        """
        mapping = self.metaobject_repo.get_keyboard_backlight_mapping()
        options = [("", "Select backlight type...")]
        
        for full_name in sorted(mapping.keys()):
            options.append((full_name, full_name))
        
        return options
    
    def find_dropdown_index(self, options: List[Tuple[str, str]], value: str) -> int:
        """
        Find the index of a value in dropdown options
        
        Args:
            options: List of (value, display) tuples
            value: Value to find
            
        Returns:
            Index of the value in options, or 0 if not found
        """
        for i, (option_value, _) in enumerate(options):
            if option_value == value:
                return i
        return 0  # Default to first option if not found
    
    def find_simple_dropdown_index(self, options: List[str], value: str) -> int:
        """
        Find the index of a value in simple dropdown options (for RAM)
        
        Args:
            options: List of string options
            value: Value to find
            
        Returns:
            Index of the value in options, or 0 if not found
        """
        try:
            return options.index(value)
        except ValueError:
            return 0  # Default to first option if not found
    
    def get_component_options(self, component_type: str) -> List[Tuple[str, str]]:
        """
        Get dropdown options for any component type
        
        Args:
            component_type: Type of component (processor, vga, graphics, etc.)
            
        Returns:
            List of tuples with component options
            
        Raises:
            ValueError: If component_type is not supported
        """
        component_methods = {
            "processor": self.get_processor_options,
            "vga": self.get_vga_options,
            "graphics": self.get_graphics_options,
            "display": self.get_display_options,
            "storage": self.get_storage_options,
            "color": self.get_color_options,
            "os": self.get_os_options,
            "keyboard_layout": self.get_keyboard_layout_options,
            "keyboard_backlight": self.get_keyboard_backlight_options,
        }
        
        if component_type not in component_methods:
            raise ValueError(f"Unsupported component type: {component_type}")
        
        return component_methods[component_type]()
    
    def get_all_component_counts(self) -> Dict[str, int]:
        """
        Get count of available options for each component type
        
        Returns:
            Dict with component types as keys and option counts as values
        """
        counts = {}
        
        try:
            counts["processors"] = len(self.metaobject_repo.get_processor_mapping())
            counts["vga"] = len(self.metaobject_repo.get_vga_mapping())
            counts["graphics"] = len(self.metaobject_repo.get_graphics_mapping())
            counts["displays"] = len(self.metaobject_repo.get_display_mapping())
            counts["storage"] = len(self.metaobject_repo.get_storage_mapping())
            counts["colors"] = len(self.metaobject_repo.get_color_mapping())
            counts["os"] = len(self.metaobject_repo.get_os_mapping())
            counts["keyboard_layouts"] = len(self.metaobject_repo.get_keyboard_layout_mapping())
            counts["keyboard_backlights"] = len(self.metaobject_repo.get_keyboard_backlight_mapping())
            counts["ram_options"] = len(self.get_ram_options()) - 1  # Exclude empty option
        except Exception as e:
            print(f"Error getting component counts: {e}")
            counts["error"] = str(e)
        
        return counts