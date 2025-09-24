"""
Laptop entity for the domain layer.

This module defines the laptop product entity with specific
attributes and business rules for laptop products.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from domain.entities.product import Product


@dataclass
class LaptopEntity(Product):
    """
    Domain entity for laptop products.
    
    This class extends the base Product with laptop-specific
    attributes and business logic.
    """
    
    # Laptop-specific attributes
    brand: str = ""
    model: str = ""
    
    # Technical specifications
    cpu: str = ""
    ram: str = ""
    gpu: Optional[str] = None
    display: str = ""
    storage: str = ""
    os: str = "Windows 11"
    
    # Keyboard specifications
    keyboard_layout: str = "US"
    keyboard_backlight: Optional[str] = None
    
    # Physical attributes
    color: Optional[str] = None
    weight: Optional[float] = None  # in kg
    
    # Product metadata
    rank: Optional[str] = None
    inclusions: List[str] = field(default_factory=list)
    minus: List[str] = field(default_factory=list)
    
    # Additional features
    webcam: Optional[str] = None
    battery_life: Optional[str] = None
    ports: List[str] = field(default_factory=list)
    
    def get_product_type(self) -> str:
        """Return the product type identifier."""
        return "laptop"
    
    def validate_business_rules(self) -> List[str]:
        """
        Validate laptop-specific business rules.
        
        Returns:
            List of validation error messages
        """
        errors = self.validate_common_rules()
        
        # Brand and model validation
        if not self.brand:
            errors.append("Brand is required for laptops")
        if not self.model:
            errors.append("Model is required for laptops")
        
        # Price validation for laptops
        if self.price < 5000:
            errors.append("Laptop price must be at least ¥5000")
        
        # Technical specification validation
        if not self.cpu:
            errors.append("CPU specification is required")
        if not self.ram:
            errors.append("RAM specification is required")
        if not self.display:
            errors.append("Display specification is required")
        if not self.storage:
            errors.append("Storage specification is required")
        
        # RAM validation
        valid_ram_sizes = ["4GB", "8GB", "12GB", "16GB", "24GB", "32GB", "48GB", "64GB"]
        if self.ram and self.ram not in valid_ram_sizes:
            errors.append(f"Invalid RAM size: {self.ram}")
        
        # OS validation
        valid_os = ["Windows 11", "Windows 10", "macOS", "Ubuntu", "Chrome OS"]
        if self.os and self.os not in valid_os:
            errors.append(f"Invalid operating system: {self.os}")
        
        # Keyboard layout validation
        valid_layouts = ["US", "UK", "JIS", "German", "French", "Spanish"]
        if self.keyboard_layout and self.keyboard_layout not in valid_layouts:
            errors.append(f"Invalid keyboard layout: {self.keyboard_layout}")
        
        # Collection validation
        if not self.collections:
            errors.append("At least one collection is required")
        
        return errors
    
    def get_full_title(self) -> str:
        """
        Generate the full product title.
        
        Returns:
            Complete product title with specifications
        """
        title_parts = [self.brand, self.model]
        
        # Add key specifications
        spec_parts = []
        if self.cpu:
            spec_parts.append(self.cpu)
        if self.ram:
            spec_parts.append(self.ram)
        if self.gpu:
            spec_parts.append(self.gpu)
        if self.display:
            spec_parts.append(self.display)
        if self.storage:
            spec_parts.append(self.storage)
        
        if spec_parts:
            title_parts.append(f"[{'/'.join(spec_parts)}]")
        
        if self.color:
            title_parts.append(f"[{self.color}]")
        
        return " ".join(title_parts)
    
    def get_performance_tier(self) -> str:
        """
        Determine performance tier based on specifications.
        
        Returns:
            Performance tier (Entry, Mid-Range, High-End, Gaming, Workstation)
        """
        # Simple heuristic based on RAM and GPU
        ram_gb = int(self.ram.replace("GB", "")) if self.ram else 0
        has_dedicated_gpu = bool(self.gpu and "Intel" not in self.gpu)
        
        if ram_gb >= 32 and has_dedicated_gpu:
            return "Workstation"
        elif ram_gb >= 16 and has_dedicated_gpu and "RTX" in (self.gpu or ""):
            return "Gaming"
        elif ram_gb >= 16:
            return "High-End"
        elif ram_gb >= 8:
            return "Mid-Range"
        else:
            return "Entry"
    
    def add_inclusion(self, inclusion: str) -> None:
        """
        Add a product inclusion.
        
        Args:
            inclusion: Inclusion to add
        """
        if inclusion and inclusion not in self.inclusions:
            self.inclusions.append(inclusion)
    
    def remove_inclusion(self, inclusion: str) -> None:
        """
        Remove a product inclusion.
        
        Args:
            inclusion: Inclusion to remove
        """
        if inclusion in self.inclusions:
            self.inclusions.remove(inclusion)
    
    def add_minus(self, minus_item: str) -> None:
        """
        Add a minus (missing item).
        
        Args:
            minus_item: Missing item to add
        """
        if minus_item and minus_item not in self.minus:
            self.minus.append(minus_item)
    
    def remove_minus(self, minus_item: str) -> None:
        """
        Remove a minus (missing item).
        
        Args:
            minus_item: Missing item to remove
        """
        if minus_item in self.minus:
            self.minus.remove(minus_item)
    
    def add_port(self, port: str) -> None:
        """
        Add a port specification.
        
        Args:
            port: Port type to add
        """
        if port and port not in self.ports:
            self.ports.append(port)
    
    def is_gaming_laptop(self) -> bool:
        """
        Check if laptop is suitable for gaming.
        
        Returns:
            True if has dedicated GPU with gaming capabilities
        """
        gaming_keywords = ["RTX", "GTX", "Radeon", "Arc"]
        return any(keyword in (self.gpu or "") for keyword in gaming_keywords)
    
    def is_ultrabook(self) -> bool:
        """
        Check if laptop qualifies as an ultrabook.
        
        Returns:
            True if weight < 1.5kg and has SSD storage
        """
        is_lightweight = self.weight and self.weight < 1.5
        has_ssd = "SSD" in (self.storage or "")
        return is_lightweight and has_ssd
    
    def get_storage_type(self) -> str:
        """
        Extract storage type from storage specification.
        
        Returns:
            Storage type (SSD, HDD, Hybrid, Unknown)
        """
        if not self.storage:
            return "Unknown"
        elif "SSD" in self.storage:
            return "SSD"
        elif "HDD" in self.storage:
            return "HDD"
        elif "SSD" in self.storage and "HDD" in self.storage:
            return "Hybrid"
        else:
            return "Unknown"
    
    def to_dict(self) -> dict:
        """
        Convert laptop entity to dictionary.
        
        Returns:
            Dictionary representation of the laptop
        """
        base_dict = super().to_dict()
        base_dict.update({
            'brand': self.brand,
            'model': self.model,
            'cpu': self.cpu,
            'ram': self.ram,
            'gpu': self.gpu,
            'display': self.display,
            'storage': self.storage,
            'os': self.os,
            'keyboard_layout': self.keyboard_layout,
            'keyboard_backlight': self.keyboard_backlight,
            'color': self.color,
            'weight': self.weight,
            'rank': self.rank,
            'inclusions': self.inclusions,
            'minus': self.minus,
            'webcam': self.webcam,
            'battery_life': self.battery_life,
            'ports': self.ports,
            'full_title': self.get_full_title(),
            'performance_tier': self.get_performance_tier(),
            'is_gaming': self.is_gaming_laptop(),
            'is_ultrabook': self.is_ultrabook(),
            'storage_type': self.get_storage_type()
        })
        return base_dict