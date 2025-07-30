"""
Enhanced Laptop Metafield Mapping System with Comprehensive Logging

This module provides enhanced laptop metafield mapping with comprehensive logging
for missing metaobject entries. It detects, logs, and reports missing entries
to improve user experience and system maintenance.

Features:
- Missing metaobject detection and logging
- Frequency tracking for popular missing entries
- User feedback integration for Streamlit UI
- Admin reporting capabilities
- Automated script generation for batch updates

Author: myByte International
Generated: July 2025
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from collections import defaultdict

from config.laptop_metafields import LAPTOP_METAFIELDS, ADDITIONAL_METAFIELDS

# Import the clean dedicated_graphics mapping
try:
    from config.dedicated_graphics_mapping import DEDICATED_GRAPHICS_MAPPING
except ImportError:
    DEDICATED_GRAPHICS_MAPPING = {}

@dataclass
class MissingMetaobjectEntry:
    """Represents a missing metaobject entry with tracking info"""
    field_name: str
    value: str
    frequency: int
    first_seen: str
    last_seen: str
    context: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

class MissingMetaobjectLogger:
    """Handles logging and tracking of missing metaobject entries"""
    
    def __init__(self, log_file_path: str = "logs/missing_metaobjects.json"):
        """Initialize logger with configurable log file path"""
        self.log_file = Path(log_file_path)
        self.log_file.parent.mkdir(exist_ok=True)
        self.missing_entries: Dict[str, Dict[str, MissingMetaobjectEntry]] = {}
        self.session_missing: List[Dict] = []  # Track missing entries for current session
        self._load_existing_log()
        
        # Setup Python logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('MissingMetaobjectLogger')
    
    def _load_existing_log(self):
        """Load existing missing entries from log file"""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert loaded data back to MissingMetaobjectEntry objects
                for field_name, entries in data.get('entries', {}).items():
                    self.missing_entries[field_name] = {}
                    for value, entry_data in entries.items():
                        self.missing_entries[field_name][value] = MissingMetaobjectEntry(
                            field_name=entry_data['field_name'],
                            value=entry_data['value'],
                            frequency=entry_data['frequency'],
                            first_seen=entry_data['first_seen'],
                            last_seen=entry_data['last_seen'],
                            context=entry_data.get('context', {})
                        )
        except Exception as e:
            self.logger.warning(f"Could not load existing log: {e}")
            self.missing_entries = {}
    
    def log_missing_entry(self, field_name: str, value: str, context: Dict[str, Any] = None):
        """Log a missing metaobject entry with context and frequency tracking"""
        
        if context is None:
            context = {}
        
        timestamp = datetime.now().isoformat()
        
        # Initialize field if not exists
        if field_name not in self.missing_entries:
            self.missing_entries[field_name] = {}
        
        # Update or create entry
        if value in self.missing_entries[field_name]:
            # Update existing entry
            entry = self.missing_entries[field_name][value]
            entry.frequency += 1
            entry.last_seen = timestamp
            entry.context.update(context)
        else:
            # Create new entry
            entry = MissingMetaobjectEntry(
                field_name=field_name,
                value=value,
                frequency=1,
                first_seen=timestamp,
                last_seen=timestamp,
                context=context
            )
            self.missing_entries[field_name][value] = entry
        
        # Add to session tracking
        self.session_missing.append({
            'field_name': field_name,
            'value': value,
            'timestamp': timestamp,
            'context': context
        })
        
        # Save to file
        self._save_log()
        
        # Log to console/file logger
        self.logger.warning(
            f"Missing metaobject: {field_name}='{value}' "
            f"(frequency: {entry.frequency}, context: {context})"
        )
    
    def _save_log(self):
        """Save current log state to file"""
        try:
            # Convert to serializable format
            serializable_data = {
                'last_updated': datetime.now().isoformat(),
                'total_missing_fields': len(self.missing_entries),
                'total_missing_values': sum(len(entries) for entries in self.missing_entries.values()),
                'entries': {}
            }
            
            for field_name, entries in self.missing_entries.items():
                serializable_data['entries'][field_name] = {}
                for value, entry in entries.items():
                    serializable_data['entries'][field_name][value] = entry.to_dict()
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Failed to save log: {e}")
    
    def get_missing_summary(self) -> Dict[str, List[Dict]]:
        """Get summary of missing entries by category"""
        summary = {}
        
        for field_name, entries in self.missing_entries.items():
            summary[field_name] = []
            
            # Sort by frequency (descending) then by last seen (descending)
            sorted_entries = sorted(
                entries.values(),
                key=lambda x: (x.frequency, x.last_seen),
                reverse=True
            )
            
            for entry in sorted_entries:
                summary[field_name].append({
                    'value': entry.value,
                    'frequency': entry.frequency,
                    'first_seen': entry.first_seen,
                    'last_seen': entry.last_seen,
                    'context': entry.context
                })
        
        return summary
    
    def get_session_missing(self) -> List[Dict]:
        """Get missing entries from current session"""
        return self.session_missing
    
    def clear_session_missing(self):
        """Clear session missing entries (called after successful product creation)"""
        self.session_missing = []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about missing entries"""
        total_fields = len(self.missing_entries)
        total_values = sum(len(entries) for entries in self.missing_entries.values())
        total_frequency = sum(
            entry.frequency 
            for entries in self.missing_entries.values() 
            for entry in entries.values()
        )
        
        # Most frequent missing entries across all fields
        all_entries = [
            entry for entries in self.missing_entries.values() 
            for entry in entries.values()
        ]
        most_frequent = sorted(all_entries, key=lambda x: x.frequency, reverse=True)[:10]
        
        # Field-wise statistics
        field_stats = {}
        for field_name, entries in self.missing_entries.items():
            field_total_frequency = sum(entry.frequency for entry in entries.values())
            field_stats[field_name] = {
                'unique_values': len(entries),
                'total_frequency': field_total_frequency,
                'most_frequent': max(entries.values(), key=lambda x: x.frequency).value if entries else None
            }
        
        return {
            'total_fields': total_fields,
            'total_unique_values': total_values,
            'total_frequency': total_frequency,
            'most_frequent_overall': [
                {'value': entry.value, 'field': entry.field_name, 'frequency': entry.frequency}
                for entry in most_frequent
            ],
            'field_statistics': field_stats,
            'log_file_path': str(self.log_file),
            'last_updated': datetime.now().isoformat()
        }
    
    def generate_creation_script(self, field_name: str, limit: int = 20) -> str:
        """Generate metaobject creation script for missing entries"""
        
        if field_name not in self.missing_entries:
            return ""
        
        entries = self.missing_entries[field_name]
        
        # Sort by frequency and take top entries
        sorted_entries = sorted(
            entries.values(),
            key=lambda x: x.frequency,
            reverse=True
        )[:limit]
        
        script_content = f'''#!/usr/bin/env python3
"""
Auto-generated Metaobject Creation Script for {field_name}
Generated on: {datetime.now().isoformat()}
Top {len(sorted_entries)} missing entries by frequency

This script creates metaobjects for the most frequently requested
{field_name} values that are currently missing from Shopify.
"""

# Missing {field_name.upper()} entries (sorted by frequency)
{field_name.upper()}_MISSING_DATA = [
'''
        
        for entry in sorted_entries:
            handle = entry.value.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('/', '-').replace(',', '')
            script_content += f'''    {{
        "display_name": "{entry.value}",
        "handle": "{handle}",
        "fields": {{
            "label": "{entry.value}"
        }},
        "frequency": {entry.frequency},
        "context": {json.dumps(entry.context, indent=8)}
    }},
'''
        
        script_content += f''']

# Use this data with create_laptop_metaobjects.py
# Definition ID for {field_name}: {self._get_definition_id_for_field(field_name)}

if __name__ == "__main__":
    print(f"Generated {len(sorted_entries)} {field_name} entries")
    print(f"Total frequency: {sum(entry.frequency for entry in sorted_entries)}")
    print("Use with MetaobjectBatchCreator.batch_create_category()")
'''
        
        return script_content
    
    def _get_definition_id_for_field(self, field_name: str) -> Optional[str]:
        """Get metaobject definition ID for a field"""
        field_mapping = {
            'processor': 'gid://shopify/MetaobjectDefinition/10078486677',
            'graphics': 'gid://shopify/MetaobjectDefinition/10078617749',
            'vga': 'gid://shopify/MetaobjectDefinition/10078650517',
            'display': 'gid://shopify/MetaobjectDefinition/10078388373',
            'storage': 'gid://shopify/MetaobjectDefinition/10097983637',
            'operating_system': 'gid://shopify/MetaobjectDefinition/10827989141',
            'keyboard_layout': 'gid://shopify/MetaobjectDefinition/10097819797',
            'color': 'gid://shopify/MetaobjectDefinition/7936606357',  # Color metaobject definition
        }
        return field_mapping.get(field_name)

# Global logger instance
missing_logger = MissingMetaobjectLogger()

# Import existing mapping functions from actual mapping (working version)
from config.laptop_metafield_mapping_actual import (
    get_metaobject_gid,
    PROCESSOR_METAOBJECTS,
    GRAPHICS_METAOBJECTS,
    VGA_METAOBJECTS,
    DISPLAY_METAOBJECTS,
    STORAGE_METAOBJECTS,
    OS_METAOBJECTS,
    KEYBOARD_LAYOUT_METAOBJECTS,
    LAPTOP_RANK_METAOBJECTS,
    LAPTOP_INCLUSION_METAOBJECTS,
    LAPTOP_MINUS_METAOBJECTS,
    COLOR_METAOBJECTS
)

# Enhanced lookup function with fallback to actual mapping
def get_metaobject_gid_full(field_name: str, value: str) -> Optional[str]:
    """
    Get metaobject GID with enhanced lookup that falls back to actual mapping
    """
    # First try the actual mapping function
    result = get_metaobject_gid(field_name, value)
    if result:
        return result
    
    # Enhanced processor name extraction for templates
    if field_name == 'processor':
        mappings = PROCESSOR_METAOBJECTS
        
        # Extract abbreviated form from full processor name
        # "Intel Core i7-12700H (16 CPUs), ~2.3GHz" → "i7-12700H"
        if 'Intel Core' in value:
            parts = value.split()
            if len(parts) >= 3:
                abbreviated = parts[2].split('(')[0].strip()
                if abbreviated in mappings:
                    return mappings[abbreviated]
        
        # Handle AMD processors: "AMD Ryzen 7 4800HS (16 CPUs), ~2.9GHz" → "Ryzen 7 4800HS"
        elif 'AMD Ryzen' in value:
            # Extract "Ryzen 7 4800HS" from "AMD Ryzen 7 4800HS (16 CPUs), ~2.9GHz"
            if '(' in value:
                ryzen_part = value.split('(')[0].strip()  # "AMD Ryzen 7 4800HS"
                abbreviated = ryzen_part.replace('AMD ', '')  # "Ryzen 7 4800HS"
                if abbreviated in mappings:
                    return mappings[abbreviated]
        
        # Handle Apple processors: "Apple M2 Chip" → "Apple M2"
        elif 'Apple M' in value:
            apple_part = value.replace(' Chip', '').strip()  # "Apple M2"
            if apple_part in mappings:
                return mappings[apple_part]
    
    # Enhanced display matching for templates
    elif field_name == 'display':
        mappings = DISPLAY_METAOBJECTS
        # Try to match "15-inch FHD (144Hz)" to "15 FHD 144Hz"
        if '15-inch FHD (144Hz)' in value:
            return mappings.get('15 FHD 144Hz')
        elif '15.6-inch FHD (144Hz)' in value:
            return mappings.get('15.6 FHD 144Hz')
        elif '15-inch FHD (240Hz)' in value:
            return mappings.get('15 FHD 240Hz')
        elif '15-inch FHD (300Hz)' in value:
            return mappings.get('15 FHD 300Hz')
        elif '15-inch FHD (60Hz)' in value:
            return mappings.get('15 FHD 60Hz')
        elif '15-inch HD (60Hz)' in value:
            return mappings.get('15 HD 60Hz')
        elif '14-inch FHD (144Hz)' in value:
            return mappings.get('14 FHD 144Hz')
        elif '13-inch FHD (60Hz) Touch Screen' in value:
            return mappings.get('13 FHD Touch')
        elif '13.4 Inch FHD (120Hz) Touchscreen' in value:
            return mappings.get('13.4 FHD 120Hz Touch')
        # Retina displays
        elif '16-inch Retina' in value:
            return mappings.get('16 Retina')
        elif '15.4-inch Retina' in value:
            return mappings.get('15.4 Retina')
        elif '15-inch Retina' in value:
            return mappings.get('15 Retina')
        elif '13.6-inch Retina' in value:
            return mappings.get('13.6 Retina')
        elif '13.3-inch Retina' in value:
            return mappings.get('13.3 Retina')
        elif '13-inch Retina' in value:
            return mappings.get('13 Retina')
        elif '12-inch Retina' in value:
            return mappings.get('12 Retina')
        # Basic displays
        elif '13-inch' in value:
            return mappings.get('13 inch')
        elif '11-inch' in value:
            return mappings.get('11 inch')
    
    return None

# Define lookup functions that delegate to the full mapping
def get_processor_metafield_gid(value: str) -> Optional[str]:
    return get_metaobject_gid_full('processor', value)

def get_graphics_metafield_gid(value: str) -> Optional[str]:
    # First try the clean dedicated_graphics mapping
    if value in DEDICATED_GRAPHICS_MAPPING:
        return DEDICATED_GRAPHICS_MAPPING[value]
    # Fallback to full mapping
    return get_metaobject_gid_full('graphics', value)

def get_display_metafield_gid(value: str) -> Optional[str]:
    return get_metaobject_gid_full('display', value)

def get_storage_metafield_gid(value: str) -> Optional[str]:
    return get_metaobject_gid_full('storage', value)

def get_vga_metafield_gid(value: str) -> Optional[str]:
    # First try the clean dedicated_graphics mapping (VGA and graphics share the same metaobjects)
    if value in DEDICATED_GRAPHICS_MAPPING:
        return DEDICATED_GRAPHICS_MAPPING[value]
    # Fallback to full mapping
    return get_metaobject_gid_full('vga', value)

def get_os_metafield_gid(value: str) -> Optional[str]:
    return get_metaobject_gid_full('os', value)

def get_keyboard_layout_metafield_gid(value: str) -> Optional[str]:
    return get_metaobject_gid_full('keyboard_layout', value)

def get_keyboard_backlight_metafield_gid(value: str) -> Optional[str]:
    # Keyboard backlight doesn't have metaobjects, return None
    return None

def get_color_metafield_gid(value: str) -> Optional[str]:
    # Use imported color mappings from actual mapping file
    return COLOR_METAOBJECTS.get(value)

def get_metaobject_gid_enhanced(field_name: str, value: str, context: Dict[str, Any] = None) -> Tuple[Optional[str], bool]:
    """
    Enhanced metaobject GID lookup with comprehensive logging
    
    Args:
        field_name: The metafield name (e.g., 'processor', 'graphics')
        value: The value to look up (e.g., 'Intel Core i7-12700H')
        context: Additional context for logging (e.g., product info)
        
    Returns:
        Tuple[Optional[str], bool]: (GID or None, found flag)
    """
    
    if context is None:
        context = {}
    
    # Mapping of field names to lookup functions
    lookup_functions = {
        'processor': get_processor_metafield_gid,
        'graphics': get_graphics_metafield_gid,
        'display': get_display_metafield_gid,
        'storage': get_storage_metafield_gid,
        'vga': get_vga_metafield_gid,
        'operating_system': get_os_metafield_gid,
        'keyboard_layout': get_keyboard_layout_metafield_gid,
        'keyboard_backlight': get_keyboard_backlight_metafield_gid,
        'color': get_color_metafield_gid,
    }
    
    # Try full name lookup first with the new mapping
    gid = get_metaobject_gid_full(field_name, value)
    if gid:
        return gid, True
    
    # Try existing lookup as fallback
    lookup_func = lookup_functions.get(field_name)
    if lookup_func:
        gid = lookup_func(value)
        if gid and not gid.startswith('PLACEHOLDER'):
            return gid, True
    
    # If not found, log as missing
    missing_logger.log_missing_entry(field_name, value, context)
    return None, False

def convert_laptop_data_to_metafields_enhanced(laptop_data: Dict[str, Any]) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, List[str]]]:
    """
    Enhanced conversion with detailed logging of missing entries
    
    Args:
        laptop_data: Dictionary containing laptop specification data
        
    Returns:
        Tuple[metafields_dict, missing_entries_dict]: 
            - metafields_dict: Successfully mapped metafields
            - missing_entries_dict: Missing entries organized by field
    """
    
    metafields = {}
    missing_entries = defaultdict(list)
    
    # Get metafield configurations
    all_metafields = {**LAPTOP_METAFIELDS, **ADDITIONAL_METAFIELDS}
    
    # Product context for logging
    product_context = {
        'product_title': laptop_data.get('title', 'Unknown'),
        'brand': laptop_data.get('brand', 'Unknown'),
        'model': laptop_data.get('model', 'Unknown'),
        'timestamp': datetime.now().isoformat()
    }
    
    # Process each laptop data field
    for field_name, value in laptop_data.items():
        if not value:  # Skip empty values
            continue
            
        # Get metafield configuration
        metafield_config = None
        for config_key, config in all_metafields.items():
            if config_key == field_name or config.key.endswith(field_name):
                metafield_config = config
                break
        
        if not metafield_config:
            continue  # Skip fields without metafield definitions
        
        # Handle different metafield types
        if field_name == 'ram':
            # RAM is a text field, not a metaobject reference
            metafields[metafield_config.key] = {
                'namespace': metafield_config.namespace,
                'key': metafield_config.key,
                'type': metafield_config.type.value,
                'value': str(value)
            }
            
        elif 'metaobject' in metafield_config.type.value:
            # Handle metaobject reference fields
            
            if field_name in ['inclusions', 'minus', 'kelengkapan']:
                # Handle list fields (take first value if list)
                actual_value = value[0] if isinstance(value, list) and value else value
                if actual_value:
                    gid, found = get_metaobject_gid_enhanced(
                        field_name, 
                        actual_value, 
                        product_context
                    )
                    
                    if found:
                        metafields[metafield_config.key] = {
                            'namespace': metafield_config.namespace,
                            'key': metafield_config.key,
                            'type': metafield_config.type.value,
                            'value': gid
                        }
                    else:
                        missing_entries[field_name].append(actual_value)
            else:
                # Handle single metaobject reference fields
                gid, found = get_metaobject_gid_enhanced(
                    field_name, 
                    value, 
                    product_context
                )
                
                if found:
                    metafields[metafield_config.key] = {
                        'namespace': metafield_config.namespace,
                        'key': metafield_config.key,
                        'type': metafield_config.type.value,
                        'value': gid
                    }
                else:
                    missing_entries[field_name].append(value)
    
    return metafields, dict(missing_entries)

def get_missing_entries_report() -> Dict[str, Any]:
    """Get comprehensive report of all missing entries"""
    
    return {
        'summary': missing_logger.get_missing_summary(),
        'statistics': missing_logger.get_statistics(),
        'session_missing': missing_logger.get_session_missing()
    }

def clear_session_data():
    """Clear session-specific missing data"""
    missing_logger.clear_session_missing()

def generate_batch_update_scripts(output_dir: str = "scripts/missing_metaobjects") -> List[str]:
    """Generate batch update scripts for all missing metaobject categories"""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    generated_scripts = []
    
    for field_name in missing_logger.missing_entries.keys():
        script_content = missing_logger.generate_creation_script(field_name)
        if script_content:
            script_file = output_path / f"create_missing_{field_name}_metaobjects.py"
            
            try:
                with open(script_file, 'w', encoding='utf-8') as f:
                    f.write(script_content)
                
                generated_scripts.append(str(script_file))
                
            except Exception as e:
                missing_logger.logger.error(f"Failed to generate script for {field_name}: {e}")
    
    return generated_scripts

# Validation and utility functions
def validate_enhanced_logging() -> Dict[str, bool]:
    """Validate that enhanced logging system is working correctly"""
    
    test_results = {}
    
    try:
        # Test logging functionality
        test_context = {'test': True, 'timestamp': datetime.now().isoformat()}
        missing_logger.log_missing_entry('test_field', 'test_value', test_context)
        test_results['logging_works'] = True
    except Exception as e:
        missing_logger.logger.error(f"Logging test failed: {e}")
        test_results['logging_works'] = False
    
    try:
        # Test file I/O
        test_results['file_io_works'] = missing_logger.log_file.exists()
    except Exception:
        test_results['file_io_works'] = False
    
    try:
        # Test metafield conversion
        test_data = {'processor': 'Test Processor', 'ram': '16GB'}
        metafields, missing = convert_laptop_data_to_metafields_enhanced(test_data)
        test_results['conversion_works'] = True
    except Exception as e:
        missing_logger.logger.error(f"Conversion test failed: {e}")
        test_results['conversion_works'] = False
    
    return test_results

if __name__ == "__main__":
    # Run validation tests when executed directly
    print("🔍 Enhanced Laptop Metafield Mapping System")
    print("=" * 50)
    
    validation_results = validate_enhanced_logging()
    
    print("🧪 Validation Results:")
    for test_name, result in validation_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\\n📊 Current Statistics:")
    stats = missing_logger.get_statistics()
    print(f"   Missing fields: {stats['total_fields']}")
    print(f"   Missing values: {stats['total_unique_values']}")
    print(f"   Total frequency: {stats['total_frequency']}")
    print(f"   Log file: {stats['log_file_path']}")