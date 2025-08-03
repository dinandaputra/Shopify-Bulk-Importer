from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime

class LaptopProduct(BaseModel):
    # Core fields
    title: str = Field(..., min_length=1, description="Product title")
    brand: str = Field(..., min_length=1, description="Brand name (ASUS, Dell, HP, etc.)")
    model: Optional[str] = Field(None, description="Model name (auto-extracted from templates)")
    price: float = Field(..., gt=0, description="Price in JPY")
    quantity: int = Field(1, ge=1, description="Quantity")
    
    # Laptop-specific specifications
    cpu: Optional[str] = Field(None, description="Processor/CPU specification")
    ram: Optional[str] = Field(None, description="RAM/Memory size")
    gpu: Optional[str] = Field(None, description="Dedicated graphics card/GPU (VGA)")
    integrated_graphics: Optional[str] = Field(None, description="Integrated graphics (from CPU)")
    display: Optional[str] = Field(None, description="Display specification")
    storage: Optional[str] = Field(None, description="Storage capacity and type")
    vga: Optional[str] = Field(None, description="VGA/external display capability (legacy field)")
    os: Optional[str] = Field("Windows 11", description="Operating system")
    keyboard_layout: Optional[str] = Field("US", description="Keyboard layout")
    keyboard_backlight: Optional[str] = Field("Yes", description="Keyboard backlight capability")
    
    # Product details
    collections: Optional[List[str]] = Field(None, description="Shopify collections to assign product to")
    sales_channels: List[str] = Field(["online_store", "pos", "shop"], description="Sales channels where product should be available")
    color: Optional[str] = Field(None, description="Laptop color/finish")
    template: Optional[str] = Field(None, description="Source template used for product creation")
    
    # Metafields for laptop category
    rank: Optional[str] = Field(None, description="Product condition rank (A, A+, S, S+, BNWB, BNOB, BNIB)")
    inclusions: Optional[List[str]] = Field(None, description="What's included with the laptop")
    minus: Optional[List[str]] = Field(None, description="Issues/problems with the laptop")
    
    # Metafield mappings (GIDs for Shopify API)
    metafield_mappings: Optional[Dict[str, str]] = Field(None, description="Shopify metafield GID mappings")
    
    # Auto-generated fields
    handle: Optional[str] = Field(None, description="Auto-generated product handle")
    vendor: str = Field("myByte International", description="Vendor name")
    tags: str = Field("laptop", description="Product tags")
    published: str = Field("TRUE", description="Published status")
    category: Optional[str] = Field("Gaming", description="Laptop category")
    
    # Timestamps
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v
    
    @validator('title')
    def validate_title(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('brand')
    def validate_brand(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Brand cannot be empty')
        valid_brands = ['ASUS', 'Dell', 'HP', 'Lenovo', 'MSI', 'Acer', 'Apple', 'Samsung', 'LG']
        if v not in valid_brands:
            # Allow any brand but warn in logs
            pass
        return v.strip()
    
    @validator('rank')
    def validate_rank(cls, v):
        if v is not None:
            valid_ranks = ['A', 'A+', 'S', 'S+', 'BNWB', 'BNOB', 'BNIB']
            if v not in valid_ranks:
                raise ValueError(f'Rank must be one of: {", ".join(valid_ranks)}')
        return v
    
    @validator('ram')
    def validate_ram(cls, v):
        if v is not None:
            valid_ram = ['8GB', '16GB', '32GB', '64GB', '128GB']
            # Allow other values but warn
            if v not in valid_ram:
                # Custom RAM sizes are allowed
                pass
        return v
    
    @validator('os')
    def validate_os(cls, v):
        if v is not None:
            valid_os = ['Windows 11', 'Windows 10', 'Linux', 'Chrome OS', 'macOS']
            # Allow other values but warn  
            if v not in valid_os:
                pass
        return v
    
    @validator('collections')
    def validate_collections(cls, v):
        if v is not None:
            # Ensure 'All Products' is always included
            if 'All Products' not in v:
                v.append('All Products')
            # Ensure 'Laptop' is included for laptop products
            if 'Laptop' not in v:
                v.append('Laptop')
        else:
            v = ['All Products', 'Laptop']
        return v
    
    @validator('metafield_mappings')
    def validate_metafield_mappings(cls, v):
        if v is not None:
            # Validate that GIDs are properly formatted
            for field, gid in v.items():
                if gid and not gid.startswith('gid://shopify/'):
                    # This might be a placeholder or manual entry
                    pass
        return v
    
    def get_display_summary(self) -> str:
        """Get a one-line summary of laptop specifications"""
        specs = []
        if self.cpu:
            specs.append(self.cpu)
        if self.ram:
            specs.append(self.ram)
        if self.gpu:
            specs.append(f"VGA: {self.gpu}")
        if self.integrated_graphics:
            specs.append(f"iGPU: {self.integrated_graphics}")
        if self.storage:
            specs.append(self.storage)
        
        return " | ".join(specs) if specs else "No specs available"
    
    def get_shopify_handle(self) -> str:
        """Generate Shopify-compatible handle"""
        if self.handle:
            return self.handle
        
        # Generate from title if handle not set
        import re
        handle = self.title.lower()
        handle = re.sub(r'[^a-z0-9\s-]', '', handle)
        handle = re.sub(r'\s+', '-', handle.strip())
        handle = re.sub(r'-+', '-', handle)
        return handle.strip('-')
    
    def get_metafield_count(self) -> int:
        """Get count of mapped metafields"""
        return len(self.metafield_mappings) if self.metafield_mappings else 0
    
    def is_template_based(self) -> bool:
        """Check if product was created from a template"""
        return bool(self.template)
    
    def get_missing_specs(self) -> List[str]:
        """Get list of missing core specifications"""
        missing = []
        core_specs = ['cpu', 'ram', 'gpu', 'integrated_graphics', 'display', 'storage']
        
        for spec in core_specs:
            if not getattr(self, spec):
                missing.append(spec)
        
        return missing
    
    class Config:
        # Allow extra fields for flexibility
        extra = "forbid"
        # Use enum values for validation
        use_enum_values = True
        # Validate on assignment
        validate_assignment = True