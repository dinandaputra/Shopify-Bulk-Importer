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
        }
        return field_mapping.get(field_name)

# Global logger instance
missing_logger = MissingMetaobjectLogger()

# Import existing mapping functions (these should be replaced with actual mappings)
try:
    from config.laptop_metafield_mapping_full import get_metaobject_gid_full
    from config.laptop_metafield_mapping import (
        get_processor_metafield_gid,
        get_graphics_metafield_gid,
        get_display_metafield_gid,
        get_storage_metafield_gid,
        get_vga_metafield_gid,
        get_os_metafield_gid,
        get_keyboard_layout_metafield_gid,
        get_keyboard_backlight_metafield_gid,
        get_color_metafield_gid
    )
except ImportError:
    # Fallback functions if mapping module not available
    def get_metaobject_gid_full(field_name: str, value: str) -> Optional[str]:
        return None
    def get_processor_metafield_gid(value: str) -> Optional[str]:
        return None
    def get_graphics_metafield_gid(value: str) -> Optional[str]:
        return None
    def get_display_metafield_gid(value: str) -> Optional[str]:
        return None
    def get_storage_metafield_gid(value: str) -> Optional[str]:
        return None
    def get_vga_metafield_gid(value: str) -> Optional[str]:
        return None
    def get_os_metafield_gid(value: str) -> Optional[str]:
        return None
    def get_keyboard_layout_metafield_gid(value: str) -> Optional[str]:
        return None
    def get_keyboard_backlight_metafield_gid(value: str) -> Optional[str]:
        return None
    def get_color_metafield_gid(value: str) -> Optional[str]:
        return None

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