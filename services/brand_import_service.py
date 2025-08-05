import csv
import json
import os
from typing import Dict, List, Optional
from repositories.product_data_repository import ProductDataRepository


class BrandImportService:
    """
    Service for importing laptop models from CSV files and converting them
    to brand JSON format. Enables bulk addition of new laptop models
    and brands to the system.
    """
    
    def __init__(self):
        self.product_repo = ProductDataRepository()
        self.laptop_path = "data/products/laptops/"
    
    def import_from_csv(self, csv_path: str, brand_name: str) -> Dict:
        """
        Import laptop models from CSV file
        
        Args:
            csv_path: Path to CSV file with laptop data
            brand_name: Name of the brand (e.g., "HP", "ASUS")
            
        Returns:
            Dict with brand data in the expected JSON format
            
        Expected CSV format:
            model_key, display_name, series, year, category, cpu, ram, vga, gpu, 
            display, storage, os, keyboard_layout, keyboard_backlight, colors
        """
        models = {}
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            required_fields = ['model_key', 'cpu', 'ram', 'vga', 'gpu', 'display', 'storage', 'colors']
            
            for row_num, row in enumerate(reader, start=2):  # Start from 2 to account for header
                # Validate required fields
                missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
                if missing_fields:
                    print(f"Warning: Row {row_num} missing required fields: {missing_fields}")
                    continue
                
                model_key = row['model_key'].strip()
                
                if not model_key:
                    print(f"Warning: Row {row_num} has empty model_key, skipping")
                    continue
                
                # Parse colors (pipe-separated: "Color1|Color2|Color3")
                colors_str = row['colors'].strip()
                colors = [color.strip() for color in colors_str.split('|') if color.strip()]
                
                if not colors:
                    print(f"Warning: Row {row_num} has no colors, using default")
                    colors = ["Black"]
                
                models[model_key] = {
                    "display_name": row.get('display_name', '').strip() or model_key,
                    "series": row.get('series', '').strip() or "Standard",
                    "year": self._parse_year(row.get('year', '')),
                    "category": row.get('category', '').strip() or "Laptop",
                    "configurations": [{
                        "cpu": row['cpu'].strip(),
                        "ram": row['ram'].strip(),
                        "vga": row['vga'].strip(),
                        "gpu": row['gpu'].strip(),
                        "display": row['display'].strip(),
                        "storage": row['storage'].strip(),
                        "os": row.get('os', '').strip() or "Windows 11",
                        "keyboard_layout": row.get('keyboard_layout', '').strip() or "US - International Keyboard",
                        "keyboard_backlight": row.get('keyboard_backlight', '').strip() or "Backlit"
                    }],
                    "colors": colors
                }
        
        if not models:
            raise ValueError("No valid models found in CSV file")
        
        return {
            "brand": brand_name,
            "models": models
        }
    
    def _parse_year(self, year_str: str) -> int:
        """
        Parse year from string, with fallback to current year
        
        Args:
            year_str: Year as string
            
        Returns:
            Year as integer
        """
        try:
            year = int(year_str.strip()) if year_str.strip() else 2023
            # Validate reasonable year range
            if year < 2010 or year > 2030:
                print(f"Warning: Year {year} seems unreasonable, using 2023")
                return 2023
            return year
        except ValueError:
            print(f"Warning: Invalid year '{year_str}', using 2023")
            return 2023
    
    def save_brand_data(self, brand_name: str, brand_data: Dict) -> str:
        """
        Save brand data to JSON file
        
        Args:
            brand_name: Name of the brand
            brand_data: Brand data dict to save
            
        Returns:
            Path to the saved file
        """
        os.makedirs(self.laptop_path, exist_ok=True)
        filename = f"{self.laptop_path}{brand_name.lower()}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(brand_data, f, indent=2, ensure_ascii=False)
        
        model_count = len(brand_data['models'])
        print(f"✅ Saved {model_count} models for {brand_name} to {filename}")
        
        return filename
    
    def import_and_save(self, csv_path: str, brand_name: str) -> str:
        """
        Import from CSV and save to JSON in one operation
        
        Args:
            csv_path: Path to CSV file
            brand_name: Name of the brand
            
        Returns:
            Path to the saved JSON file
        """
        brand_data = self.import_from_csv(csv_path, brand_name)
        filename = self.save_brand_data(brand_name, brand_data)
        return filename
    
    def validate_csv_format(self, csv_path: str) -> Dict:
        """
        Validate CSV file format and report any issues
        
        Args:
            csv_path: Path to CSV file to validate
            
        Returns:
            Dict with validation results
        """
        validation_result = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "row_count": 0,
            "valid_rows": 0
        }
        
        if not os.path.exists(csv_path):
            validation_result["errors"].append(f"File not found: {csv_path}")
            return validation_result
        
        required_fields = ['model_key', 'cpu', 'ram', 'vga', 'gpu', 'display', 'storage', 'colors']
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Check if all required columns exist
                missing_columns = [field for field in required_fields if field not in reader.fieldnames]
                if missing_columns:
                    validation_result["errors"].append(f"Missing required columns: {missing_columns}")
                    return validation_result
                
                valid_rows = 0
                for row_num, row in enumerate(reader, start=2):
                    validation_result["row_count"] = row_num - 1
                    
                    # Check for missing required data
                    missing_data = [field for field in required_fields if not row.get(field, '').strip()]
                    if missing_data:
                        validation_result["warnings"].append(f"Row {row_num}: Missing data in {missing_data}")
                        continue
                    
                    # Validate year
                    year_str = row.get('year', '').strip()
                    if year_str:
                        try:
                            year = int(year_str)
                            if year < 2010 or year > 2030:
                                validation_result["warnings"].append(f"Row {row_num}: Unusual year {year}")
                        except ValueError:
                            validation_result["warnings"].append(f"Row {row_num}: Invalid year '{year_str}'")
                    
                    # Validate colors format
                    colors = row.get('colors', '').strip()
                    if '|' not in colors and len(colors) > 50:  # Likely not pipe-separated
                        validation_result["warnings"].append(f"Row {row_num}: Colors might not be pipe-separated")
                    
                    valid_rows += 1
                
                validation_result["valid_rows"] = valid_rows
                validation_result["valid"] = valid_rows > 0
                
        except Exception as e:
            validation_result["errors"].append(f"Error reading CSV: {str(e)}")
        
        return validation_result
    
    def get_existing_brands(self) -> List[str]:
        """
        Get list of existing brands in the system
        
        Returns:
            List of brand names
        """
        return self.product_repo.get_all_brands()
    
    def merge_with_existing_brand(self, brand_name: str, new_models: Dict) -> Dict:
        """
        Merge new models with existing brand data
        
        Args:
            brand_name: Name of existing brand
            new_models: Dict of new models to add
            
        Returns:
            Merged brand data
        """
        try:
            existing_data = self.product_repo.get_brand_data(brand_name)
            existing_models = existing_data.get("models", {})
            
            # Check for model key conflicts
            conflicts = set(existing_models.keys()) & set(new_models.keys())
            if conflicts:
                print(f"Warning: Model key conflicts detected: {conflicts}")
                print("New models will override existing ones with same keys")
            
            # Merge models
            merged_models = {**existing_models, **new_models}
            
            return {
                "brand": brand_name,
                "models": merged_models
            }
            
        except Exception as e:
            print(f"Brand {brand_name} not found, creating new brand data")
            return {
                "brand": brand_name,
                "models": new_models
            }
    
    def create_sample_csv(self, output_path: str):
        """
        Create a sample CSV file with proper format
        
        Args:
            output_path: Path where to create the sample CSV
        """
        sample_data = [
            {
                "model_key": "Sample Laptop Pro 15",
                "display_name": "Laptop Pro 15",
                "series": "Pro Series",
                "year": "2023",
                "category": "Professional",
                "cpu": "Intel Core i7-12700H (20 CPUs), ~2.3GHz",
                "ram": "16GB",
                "vga": "NVIDIA GeForce RTX 4060 8GB",
                "gpu": "Intel Iris Xe Graphics",
                "display": "15.6\" FHD 144Hz",
                "storage": "512GB SSD",
                "os": "Windows 11",
                "keyboard_layout": "US - International Keyboard",
                "keyboard_backlight": "RGB Backlight",
                "colors": "Space Gray|Silver|Gold"
            }
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = sample_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sample_data)
        
        print(f"✅ Sample CSV created at {output_path}")