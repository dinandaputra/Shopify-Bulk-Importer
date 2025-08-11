#!/usr/bin/env python3
"""
Standardize laptop component names to match Shopify metaobject formats.
This ensures consistency between product definitions and metaobject lookups.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComponentNameStandardizer:
    """Standardizes component names to match Shopify metaobject formats."""
    
    def __init__(self):
        self.base_path = Path("/home/dinanda/Documents/Shopify-Bulk-Importer")
        self.metaobjects_path = self.base_path / "data" / "metaobjects"
        self.products_path = self.base_path / "data" / "products" / "laptops"
        
        # Load all metaobject names for validation
        self.metaobject_names = self._load_metaobject_names()
        
        # Track changes for reporting
        self.changes_made = []
    
    def _load_metaobject_names(self) -> Dict[str, set]:
        """Load all metaobject names from JSON files."""
        metaobject_names = {}
        
        files_to_load = [
            'processors.json',
            'storage.json',
            'displays.json',
            'graphics.json',
            'vga.json',
            'os.json',
            'keyboard_layouts.json',
            'keyboard_backlights.json',
            'colors.json'
        ]
        
        for filename in files_to_load:
            filepath = self.metaobjects_path / filename
            if filepath.exists():
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    category = filename.replace('.json', '')
                    metaobject_names[category] = set(data.keys())
                    logger.info(f"Loaded {len(data)} {category} metaobject names")
        
        return metaobject_names
    
    def find_correct_metaobject_name(self, value: str, category: str) -> str:
        """Find the correct metaobject name for a given value."""
        if category not in self.metaobject_names:
            return value
        
        valid_names = self.metaobject_names[category]
        
        # Direct match
        if value in valid_names:
            return value
        
        # Case-insensitive match
        for valid_name in valid_names:
            if value.lower() == valid_name.lower():
                return valid_name
        
        # Partial match - find the best match
        value_lower = value.lower()
        for valid_name in valid_names:
            valid_lower = valid_name.lower()
            
            # Check if the core components match
            if self._components_match(value_lower, valid_lower):
                return valid_name
        
        # No match found, return original
        logger.warning(f"No match found for {category}: {value}")
        return value
    
    def _components_match(self, value1: str, value2: str) -> bool:
        """Check if two component names are essentially the same."""
        # Remove common variations
        value1 = value1.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        value2 = value2.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Check for substring match
        return value1 in value2 or value2 in value1
    
    def standardize_configuration(self, config: Dict[str, Any], model_name: str) -> Dict[str, Any]:
        """Standardize component names in a configuration."""
        field_mappings = {
            'cpu': 'processors',
            'storage': 'storage',
            'display': 'displays',
            'gpu': 'graphics',
            'vga': 'vga',
            'os': 'os',
            'keyboard_layout': 'keyboard_layouts',
            'keyboard_backlight': 'keyboard_backlights'
        }
        
        standardized_config = {}
        
        for field, value in config.items():
            if field in field_mappings:
                category = field_mappings[field]
                original_value = value
                
                # Find the correct metaobject name
                correct_name = self.find_correct_metaobject_name(value, category)
                
                if correct_name != original_value:
                    self.changes_made.append({
                        'model': model_name,
                        'field': field,
                        'original': original_value,
                        'standardized': correct_name
                    })
                    logger.info(f"Changed {field}: '{original_value}' -> '{correct_name}'")
                
                standardized_config[field] = correct_name
            else:
                standardized_config[field] = value
        
        return standardized_config
    
    def process_laptop_file(self, filepath: Path) -> None:
        """Process a single laptop JSON file."""
        logger.info(f"Processing {filepath.name}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        modified = False
        
        if 'models' in data:
            for model_id, model_data in data['models'].items():
                if 'configurations' in model_data:
                    for i, config in enumerate(model_data['configurations']):
                        standardized = self.standardize_configuration(
                            config, 
                            f"{data.get('brand', 'Unknown')} {model_id}"
                        )
                        if standardized != config:
                            model_data['configurations'][i] = standardized
                            modified = True
                
                # Also standardize colors if present
                if 'colors' in model_data:
                    standardized_colors = []
                    for color in model_data['colors']:
                        correct_color = self.find_correct_metaobject_name(color, 'colors')
                        if correct_color != color:
                            self.changes_made.append({
                                'model': f"{data.get('brand', 'Unknown')} {model_id}",
                                'field': 'color',
                                'original': color,
                                'standardized': correct_color
                            })
                            logger.info(f"Changed color: '{color}' -> '{correct_color}'")
                        standardized_colors.append(correct_color)
                    
                    if standardized_colors != model_data['colors']:
                        model_data['colors'] = standardized_colors
                        modified = True
        
        if modified:
            # Create backup
            backup_path = filepath.with_suffix('.json.backup')
            if not backup_path.exists():
                with open(backup_path, 'w') as f:
                    with open(filepath, 'r') as original:
                        f.write(original.read())
                logger.info(f"Created backup: {backup_path.name}")
            
            # Write updated data
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Updated {filepath.name}")
    
    def run(self) -> None:
        """Process all laptop JSON files."""
        logger.info("Starting component name standardization")
        
        # Process each laptop brand file
        laptop_files = list(self.products_path.glob("*.json"))
        laptop_files = [f for f in laptop_files if f.name != 'brands_index.json']
        
        for filepath in laptop_files:
            self.process_laptop_file(filepath)
        
        # Generate report
        self.generate_report()
    
    def generate_report(self) -> None:
        """Generate a report of all changes made."""
        report_path = self.base_path / "data" / "analysis" / "component_name_standardization_report.json"
        report_path.parent.mkdir(exist_ok=True)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_changes': len(self.changes_made),
            'changes_by_field': {},
            'all_changes': self.changes_made
        }
        
        # Group changes by field
        for change in self.changes_made:
            field = change['field']
            if field not in report['changes_by_field']:
                report['changes_by_field'][field] = []
            report['changes_by_field'][field].append(change)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report generated: {report_path}")
        logger.info(f"Total changes made: {len(self.changes_made)}")
        
        # Print summary
        print("\n=== Component Name Standardization Summary ===")
        print(f"Total changes: {len(self.changes_made)}")
        for field, changes in report['changes_by_field'].items():
            print(f"  {field}: {len(changes)} changes")


if __name__ == "__main__":
    standardizer = ComponentNameStandardizer()
    standardizer.run()