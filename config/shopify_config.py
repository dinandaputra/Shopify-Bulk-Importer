import os
from typing import Optional

class ShopifyConfig:
    """
    Configuration class for Shopify API credentials
    """
    
    def __init__(self):
        # Auto-load environment variables from .env file (local development)
        # Or from Streamlit secrets (cloud deployment)
        try:
            import streamlit as st
            # Check if running in Streamlit Cloud with secrets
            if hasattr(st, 'secrets') and 'SHOPIFY_API_KEY' in st.secrets:
                # Use Streamlit secrets
                self.API_KEY = st.secrets.get("SHOPIFY_API_KEY", "")
                self.API_SECRET = st.secrets.get("SHOPIFY_API_SECRET", "")
                self.ACCESS_TOKEN = st.secrets.get("SHOPIFY_ACCESS_TOKEN", "")
                self.SHOP_DOMAIN = st.secrets.get("SHOPIFY_SHOP_DOMAIN", "")
                # API settings
                self.API_VERSION = st.secrets.get("SHOPIFY_API_VERSION", "2025-07")
                self.RATE_LIMIT_DELAY = float(st.secrets.get("RATE_LIMIT_DELAY", "0.5"))
                self.SESSION_LIMIT = int(st.secrets.get("SESSION_LIMIT", "25"))
                # Validate configuration
                self._validate_config()
            else:
                # Fall back to environment variables
                self._load_from_env()
        except ImportError:
            # Streamlit not available, use environment variables
            self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables or .env file"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            # dotenv not available, continue with system environment variables
            pass
        
        # API credentials from environment variables
        self.API_KEY = os.getenv("SHOPIFY_API_KEY", "")
        self.API_SECRET = os.getenv("SHOPIFY_API_SECRET", "")
        self.ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
        self.SHOP_DOMAIN = os.getenv("SHOPIFY_SHOP_DOMAIN", "")
        
        # API settings
        self.API_VERSION = "2025-07"
        self.RATE_LIMIT_DELAY = 0.5  # seconds between API calls
        self.SESSION_LIMIT = int(os.getenv("SESSION_LIMIT", "25"))
        
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