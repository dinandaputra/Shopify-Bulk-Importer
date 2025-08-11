"""
Product data repository for data access abstraction.

This repository provides methods for accessing product specification data
with support for brand-specific data loading and caching. Implements the
data access layer for the laptop scalability refactor.
"""

import json
import os
import glob
from typing import Dict, List, Optional
from functools import lru_cache


class ProductDataRepository:
    """
    Repository for product specification data access.
    
    Provides caching and unified access to brand-specific product data
    stored in JSON files. Supports both individual brand access and
    bulk operations for the laptop scalability system.
    """
    
    def __init__(self):
        """Initialize repository with base path for product data."""
        self.laptop_path = "data/products/laptops/"
        self._cache = {}
    
    def get_brand_data(self, brand: str) -> Dict:
        """
        Load data for specific brand.
        
        Args:
            brand: Brand name (case-insensitive, e.g., "ASUS", "Dell", "HP")
            
        Returns:
            Dictionary containing brand data with models and configurations
            
        Raises:
            FileNotFoundError: If brand data file doesn't exist
            json.JSONDecodeError: If JSON file is invalid
        """
        filename = f"{brand.lower()}.json"
        cache_key = f"brand_{brand.lower()}"
        
        if cache_key not in self._cache:
            file_path = os.path.join(self.laptop_path, filename)
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Brand data file not found: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self._cache[cache_key] = json.load(f)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Invalid JSON in {file_path}: {str(e)}", e.doc, e.pos)
        
        return self._cache[cache_key]
    
    def get_all_brands(self) -> List[str]:
        """
        Get list of available brands.
        
        Returns:
            Sorted list of brand names available in the system
        """
        if not os.path.exists(self.laptop_path):
            return []
        
        files = glob.glob(os.path.join(self.laptop_path, "*.json"))
        brands = []
        
        for file_path in files:
            filename = os.path.basename(file_path)
            # Skip index files and other non-brand files
            if filename not in ["brands_index.json", "template_cache.json"]:
                brand_name = filename.replace('.json', '').title()
                brands.append(brand_name)
        
        return sorted(brands)
    
    def get_all_models(self) -> Dict[str, Dict]:
        """
        Load all laptop models from all brands.
        
        Returns:
            Dictionary mapping model keys to model specifications
            from all available brands
        """
        cache_key = "all_models"
        
        if cache_key not in self._cache:
            all_models = {}
            
            for brand in self.get_all_brands():
                try:
                    brand_data = self.get_brand_data(brand)
                    models = brand_data.get("models", {})
                    all_models.update(models)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Warning: Could not load data for brand {brand}: {e}")
                    continue
            
            self._cache[cache_key] = all_models
        
        return self._cache[cache_key]
    
    def get_models_by_brand(self, brand: str) -> Dict[str, Dict]:
        """
        Get all models for a specific brand.
        
        Args:
            brand: Brand name
            
        Returns:
            Dictionary mapping model keys to model specifications for the brand
        """
        try:
            brand_data = self.get_brand_data(brand)
            return brand_data.get("models", {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def get_model_data(self, model_key: str, brand: Optional[str] = None) -> Optional[Dict]:
        """
        Get data for a specific model.
        
        Args:
            model_key: Model key to search for
            brand: Optional brand name to limit search
            
        Returns:
            Model data dictionary if found, None otherwise
        """
        if brand:
            models = self.get_models_by_brand(brand)
            return models.get(model_key)
        else:
            all_models = self.get_all_models()
            return all_models.get(model_key)
    
    def search_models(self, search_term: str, brand: Optional[str] = None) -> List[str]:
        """
        Search for models containing the search term.
        
        Args:
            search_term: Term to search for in model keys
            brand: Optional brand name to limit search
            
        Returns:
            List of model keys matching the search term
        """
        if brand:
            models = self.get_models_by_brand(brand)
        else:
            models = self.get_all_models()
        
        search_term_lower = search_term.lower()
        matching_models = []
        
        for model_key in models.keys():
            if search_term_lower in model_key.lower():
                matching_models.append(model_key)
        
        return sorted(matching_models)
    
    def get_brand_count(self) -> int:
        """
        Get total number of available brands.
        
        Returns:
            Number of brands in the system
        """
        return len(self.get_all_brands())
    
    def get_model_count(self, brand: Optional[str] = None) -> int:
        """
        Get total number of models.
        
        Args:
            brand: Optional brand name to limit count
            
        Returns:
            Number of models (total or for specific brand)
        """
        if brand:
            models = self.get_models_by_brand(brand)
            return len(models)
        else:
            all_models = self.get_all_models()
            return len(all_models)
    
    def get_configuration_count(self, brand: Optional[str] = None) -> int:
        """
        Get total number of configurations across all models.
        
        Args:
            brand: Optional brand name to limit count
            
        Returns:
            Total number of configurations
        """
        if brand:
            models = self.get_models_by_brand(brand)
        else:
            models = self.get_all_models()
        
        total_configs = 0
        for model_data in models.values():
            configurations = model_data.get("configurations", [])
            total_configs += len(configurations)
        
        return total_configs
    
    def validate_brand_data(self, brand: str) -> Dict[str, List[str]]:
        """
        Validate brand data for completeness and consistency.
        
        Args:
            brand: Brand name to validate
            
        Returns:
            Dictionary with validation results and any issues found
        """
        validation_results = {
            "errors": [],
            "warnings": [],
            "model_count": 0,
            "config_count": 0
        }
        
        try:
            brand_data = self.get_brand_data(brand)
            models = brand_data.get("models", {})
            validation_results["model_count"] = len(models)
            
            required_config_fields = [
                "cpu", "ram", "vga", "gpu", "display", "storage",
                "os", "keyboard_layout", "keyboard_backlight"
            ]
            
            for model_key, model_data in models.items():
                if "configurations" not in model_data:
                    validation_results["errors"].append(f"Model {model_key} missing configurations")
                    continue
                
                if "colors" not in model_data:
                    validation_results["warnings"].append(f"Model {model_key} missing colors")
                
                configs = model_data.get("configurations", [])
                validation_results["config_count"] += len(configs)
                
                for i, config in enumerate(configs):
                    for field in required_config_fields:
                        if field not in config or not config[field]:
                            validation_results["warnings"].append(
                                f"Model {model_key} config {i} missing/empty {field}"
                            )
        
        except Exception as e:
            validation_results["errors"].append(f"Failed to validate brand {brand}: {e}")
        
        return validation_results
    
    def clear_cache(self) -> None:
        """Clear the internal cache to force reload of data."""
        self._cache.clear()
    
    def get_cache_info(self) -> Dict[str, int]:
        """
        Get information about cached data.
        
        Returns:
            Dictionary with cache keys and sizes
        """
        cache_info = {}
        for key, data in self._cache.items():
            if isinstance(data, dict):
                cache_info[key] = len(data)
            else:
                cache_info[key] = 1
        return cache_info
    
    def refresh_cache(self) -> None:
        """Refresh cache by clearing and reloading all models."""
        self.clear_cache()
        # Force reload
        self.get_all_models()
    
    def get_all_models_legacy_format(self) -> Dict[str, Dict]:
        """
        Convert current laptop data to expected format for template parsing
        
        This method adapts the new JSON-based data format to work with
        the template parsing system that expects a simpler structure.
        
        Returns:
            Dict with model_key as key and model data as value in legacy format
        """
        all_models = {}
        
        try:
            # Load data from all brands
            for brand in self.get_all_brands():
                try:
                    brand_data = self.get_brand_data(brand)
                    models = brand_data.get("models", {})
                    
                    for model_key, model_data in models.items():
                        # Get configurations (should be a list in new format)
                        configurations = model_data.get("configurations", [])
                        
                        # For template parsing, include ALL configurations
                        if configurations:
                            # Transform to expected structure for template parsing
                            all_models[model_key] = {
                                "configurations": configurations,  # Include all configurations
                                "colors": model_data.get("colors", ["Black"]),  # Default color if missing
                                "brand": brand,
                                # Include first config fields at top level for backward compatibility
                                **configurations[0]
                            }
                        
                except Exception as e:
                    print(f"Warning: Error loading brand {brand}: {e}")
                    continue
            
            print(f"📊 Loaded {len(all_models)} laptop models from {len(self.get_all_brands())} brands for template parsing")
            return all_models
            
        except Exception as e:
            print(f"❌ Error loading laptop models: {e}")
            return {}