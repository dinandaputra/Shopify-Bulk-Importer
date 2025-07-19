import os
from typing import Optional

class ShopifyConfig:
    """
    Configuration class for Shopify API credentials
    """
    
    def __init__(self):
        # API credentials (should be environment variables)
        self.API_KEY = os.getenv("SHOPIFY_API_KEY", "")
        self.API_SECRET = os.getenv("SHOPIFY_API_SECRET", "")
        self.ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
        self.SHOP_DOMAIN = os.getenv("SHOPIFY_SHOP_DOMAIN", "")
        
        # API settings
        self.API_VERSION = "2024-01"
        self.RATE_LIMIT_DELAY = 0.5  # seconds between API calls
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate that all required configuration is present"""
        required_fields = [
            ("API_KEY", self.API_KEY),
            ("API_SECRET", self.API_SECRET),
            ("ACCESS_TOKEN", self.ACCESS_TOKEN),
            ("SHOP_DOMAIN", self.SHOP_DOMAIN)
        ]
        
        for field_name, field_value in required_fields:
            if not field_value:
                raise ValueError(f"Missing required configuration: {field_name}")
    
    @property
    def shop_url(self) -> str:
        """Get the full shop URL"""
        return f"https://{self.SHOP_DOMAIN}"
    
    @property
    def api_url(self) -> str:
        """Get the API base URL"""
        return f"https://{self.SHOP_DOMAIN}/admin/api/{self.API_VERSION}"
    
    def get_auth_headers(self) -> dict:
        """Get authentication headers for API requests"""
        return {
            "X-Shopify-Access-Token": self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }
    
    def __repr__(self):
        return f"ShopifyConfig(shop_domain='{self.SHOP_DOMAIN}', api_version='{self.API_VERSION}')"

# Global config instance
shopify_config = ShopifyConfig()