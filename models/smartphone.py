from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class SmartphoneProduct(BaseModel):
    # Core fields
    title: str = Field(..., min_length=1, description="Product title")
    brand: str = Field(..., min_length=1, description="Brand name")
    model: Optional[str] = Field(None, description="Model name (optional - auto-extracted from templates)")
    storage: Optional[str] = Field(None, description="Storage capacity (auto-extracted from templates)")
    price: float = Field(..., gt=0, description="Price in JPY")
    quantity: int = Field(1, ge=1, description="Quantity")
    
    # Image fields (new)
    image_urls: Optional[List[str]] = Field(None, description="List of image URLs to upload")
    
    # New fields for enhanced template system
    collections: Optional[List[str]] = Field(None, description="Shopify collections to assign product to")
    sales_channels: List[str] = Field(["online_store", "pos", "shop"], description="Sales channels where product should be available")
    color_metafield_gid: Optional[str] = Field(None, description="Shopify color metaobject GID")
    template: Optional[str] = Field(None, description="Source template used for product creation")
    
    # Metafields (exact Shopify metaobject names)
    color: Optional[str] = Field(None, description="Color")
    sim_carrier_variants: Optional[List[str]] = Field(None, description="Available SIM carrier variants for this device")
    minus: Optional[List[str]] = Field(None, description="Issues/problems with the product")
    product_inclusions: Optional[List[str]] = Field(None, description="What's included with the product")
    product_rank: Optional[str] = Field(None, description="Product condition rank")
    ram_size: Optional[str] = Field(None, description="RAM size")
    
    # Auto-generated fields
    handle: Optional[str] = Field(None, description="Auto-generated product handle")
    vendor: str = Field("myByte International", description="Vendor name")
    tags: str = Field("smartphone", description="Product tags")
    published: str = Field("TRUE", description="Published status")
    
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
        return v.strip()
    
    @validator('model')
    def validate_model(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Model cannot be empty')
        return v.strip()
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_csv_row(self) -> dict:
        """Convert to CSV row format for Shopify export"""
        return {
            "Handle": self.handle or "",
            "Title": self.title,
            "Body HTML": "",
            "Vendor": self.vendor,
            "Type": "",
            "Tags": self.tags,
            "Published": self.published,
            "Product Category": "Mobile & Smart Phones",
            "Taxable": "FALSE",
            "Variant SKU": "",
            "Variant Inventory Qty": self.quantity,
            "Variant Inventory Tracker": "shopify",
            "Variant Price": self.price,
            "Variant Barcode": "",
            "Color (product.metafields.custom.color)": self.color or "",
            "SIM Carriers (product.metafields.custom.sim_carriers)": ", ".join(self.sim_carrier_variants) if self.sim_carrier_variants else "",
            "Minus (product.metafields.custom.minus)": ", ".join(self.minus) if self.minus else "",
            "Product Inclusions (product.metafields.custom.product_inclusions)": ", ".join(self.product_inclusions) if self.product_inclusions else "",
            "Product Rank (product.metafields.custom.product_rank)": self.product_rank or "",
            "RAM Size (product.metafields.custom.ram_size)": self.ram_size or "",
        }
    
    def get_display_model_storage(self) -> str:
        """Get display string for model and storage combination"""
        if self.model and self.storage:
            return f"{self.model} {self.storage}"
        elif self.model:
            return self.model
        elif self.storage:
            return self.storage
        else:
            return "N/A"
    
    def to_api_data(self) -> dict:
        """Convert to format suitable for Shopify API upload"""
        return {
            'handle': self.handle,
            'title': self.title,
            'vendor': self.vendor,
            'tags': self.tags,
            'published': self.published,
            'price': self.price,
            'quantity': self.quantity,
            'color': self.color,
            'sim_carrier_variants': self.sim_carrier_variants,
            'minus': self.minus,
            'product_inclusions': self.product_inclusions,
            'product_rank': self.product_rank,
            'ram_size': self.ram_size,
            'image_urls': self.image_urls,
            'created_at': self.created_at
        }
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }