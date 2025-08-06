#!/usr/bin/env python3
"""
Generate Missing Shopify Entries Report for Laptop Component Mapping Plan Phase 2

This script generates a comprehensive report of laptop components that were not found
in Shopify during the GID resolution process. The report provides actionable information
for manually creating these metaobjects in Shopify Admin.

Author: Shopify API Developer (Claude Code Sub-Agent System)
Version: 1.0.0
Date: 2025-08-06
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_gid_resolution_results(results_file: str = "data/analysis/gid_resolution_results.json") -> Dict[str, Any]:
    """
    Load the GID resolution results
    
    Args:
        results_file: Path to the GID resolution results file
        
    Returns:
        Dictionary containing resolution results
    """
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        logger.info(f"Loaded GID resolution results from: {results_file}")
        return results
    except FileNotFoundError:
        logger.error(f"GID resolution results file not found: {results_file}")
        logger.error("Please run the GID resolution script first")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in results file: {e}")
        raise

def load_unmapped_components(unmapped_file: str = "data/analysis/unmapped_components.json") -> Dict[str, Any]:
    """
    Load the original unmapped components data for frequency information
    
    Args:
        unmapped_file: Path to the unmapped components file
        
    Returns:
        Dictionary containing unmapped components data
    """
    try:
        with open(unmapped_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded unmapped components data from: {unmapped_file}")
        return data
    except FileNotFoundError:
        logger.error(f"Unmapped components file not found: {unmapped_file}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in unmapped components file: {e}")
        raise

def get_metaobject_type_info() -> Dict[str, Dict]:
    """
    Get metaobject type information and field structures for Shopify Admin
    
    Returns:
        Dictionary with metaobject type information
    """
    return {
        'processor': {
            'display_name': 'Processor',
            'shopify_type': 'processor',
            'fields': [
                {'key': 'name', 'type': 'single_line_text_field', 'required': True},
                {'key': 'brand', 'type': 'single_line_text_field', 'required': False},
                {'key': 'cores', 'type': 'number_integer', 'required': False},
                {'key': 'base_frequency', 'type': 'single_line_text_field', 'required': False}
            ],
            'description': 'CPU processors for laptops'
        },
        'vga': {
            'display_name': 'VGA Graphics Card',
            'shopify_type': 'vga',
            'fields': [
                {'key': 'name', 'type': 'single_line_text_field', 'required': True},
                {'key': 'brand', 'type': 'single_line_text_field', 'required': False},
                {'key': 'memory_size', 'type': 'single_line_text_field', 'required': False},
                {'key': 'memory_type', 'type': 'single_line_text_field', 'required': False}
            ],
            'description': 'Dedicated graphics cards for laptops'
        },
        'graphics': {
            'display_name': 'Integrated Graphics',
            'shopify_type': 'graphics',
            'fields': [
                {'key': 'name', 'type': 'single_line_text_field', 'required': True},
                {'key': 'brand', 'type': 'single_line_text_field', 'required': False}
            ],
            'description': 'Integrated graphics processors'
        },
        'display': {
            'display_name': 'Display',
            'shopify_type': 'display',
            'fields': [
                {'key': 'name', 'type': 'single_line_text_field', 'required': True},
                {'key': 'size', 'type': 'single_line_text_field', 'required': False},
                {'key': 'resolution', 'type': 'single_line_text_field', 'required': False},
                {'key': 'refresh_rate', 'type': 'single_line_text_field', 'required': False},
                {'key': 'panel_type', 'type': 'single_line_text_field', 'required': False}
            ],
            'description': 'Laptop display specifications'
        },
        'storage': {
            'display_name': 'Storage',
            'shopify_type': 'storage',
            'fields': [
                {'key': 'name', 'type': 'single_line_text_field', 'required': True},
                {'key': 'capacity', 'type': 'single_line_text_field', 'required': False},
                {'key': 'type', 'type': 'single_line_text_field', 'required': False},
                {'key': 'interface', 'type': 'single_line_text_field', 'required': False}
            ],
            'description': 'Storage devices and configurations'
        },
        'operating_system': {
            'display_name': 'Operating System',
            'shopify_type': 'operating_system',
            'fields': [
                {'key': 'name', 'type': 'single_line_text_field', 'required': True},
                {'key': 'version', 'type': 'single_line_text_field', 'required': False},
                {'key': 'edition', 'type': 'single_line_text_field', 'required': False}
            ],
            'description': 'Operating systems for laptops'
        },
        'keyboard_layout': {
            'display_name': 'Keyboard Layout',
            'shopify_type': 'keyboard_layout',
            'fields': [
                {'key': 'name', 'type': 'single_line_text_field', 'required': True},
                {'key': 'language', 'type': 'single_line_text_field', 'required': False},
                {'key': 'region', 'type': 'single_line_text_field', 'required': False}
            ],
            'description': 'Keyboard layouts and languages'
        },
        'keyboard_backlight': {
            'display_name': 'Keyboard Backlight',
            'shopify_type': 'keyboard_backlight',
            'fields': [
                {'key': 'name', 'type': 'single_line_text_field', 'required': True},
                {'key': 'type', 'type': 'single_line_text_field', 'required': False},
                {'key': 'colors', 'type': 'single_line_text_field', 'required': False}
            ],
            'description': 'Keyboard backlight configurations'
        }
    }

def generate_missing_report(results: Dict[str, Any], unmapped_data: Dict[str, Any]) -> str:
    """
    Generate a comprehensive markdown report of missing Shopify entries
    
    Args:
        results: GID resolution results
        unmapped_data: Original unmapped components data
        
    Returns:
        Markdown report content
    """
    not_found_components = results.get('not_found_components', {})
    component_frequency = unmapped_data.get('component_frequency', {})
    source_models = unmapped_data.get('source_models', {})
    metaobject_types = get_metaobject_type_info()
    
    # Map component types to Shopify types
    type_mapping = {
        'processors': 'processor',
        'vga': 'vga', 
        'graphics': 'graphics',
        'displays': 'display',
        'storage': 'storage',
        'os': 'operating_system',
        'keyboard_layouts': 'keyboard_layout',
        'keyboard_backlights': 'keyboard_backlight'
    }
    
    report = []
    report.append("# Missing Shopify Metaobject Entries Report\n")
    report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**Script Version**: 1.0.0\n")
    report.append(f"**Total Missing Components**: {sum(len(components) for components in not_found_components.values())}\n\n")
    
    report.append("## Summary\n\n")
    report.append("This report lists laptop components that were not found in Shopify during the GID resolution process. ")
    report.append("These metaobjects need to be manually created in the Shopify Admin before they can be used in product creation.\n\n")
    
    # Summary table
    report.append("| Component Type | Missing Count | Priority |\n")
    report.append("|---------------|---------------|----------|\n")
    
    priority_map = {'high': 0, 'medium': 0, 'low': 0}
    
    for component_type, components in not_found_components.items():
        if not components:
            continue
            
        missing_count = len(components)
        
        # Calculate priority based on frequency of usage
        total_frequency = 0
        for component in components:
            freq_key = f"{component_type}:{component}"
            frequency = component_frequency.get(component_type, {}).get(component, 0)
            total_frequency += frequency
        
        avg_frequency = total_frequency / missing_count if missing_count > 0 else 0
        
        if avg_frequency >= 5:
            priority = "🔴 High"
            priority_map['high'] += missing_count
        elif avg_frequency >= 2:
            priority = "🟡 Medium"
            priority_map['medium'] += missing_count
        else:
            priority = "🟢 Low"
            priority_map['low'] += missing_count
        
        report.append(f"| {component_type.title()} | {missing_count} | {priority} |\n")
    
    report.append(f"\n**Priority Distribution**: {priority_map['high']} High, {priority_map['medium']} Medium, {priority_map['low']} Low\n\n")
    
    # Detailed sections for each component type
    for component_type, components in not_found_components.items():
        if not components:
            continue
        
        shopify_type = type_mapping.get(component_type, component_type)
        type_info = metaobject_types.get(shopify_type, {})
        
        report.append(f"## {component_type.title().replace('_', ' ')} ({len(components)} missing)\n\n")
        
        if type_info:
            report.append(f"**Shopify Metaobject Type**: `{type_info['shopify_type']}`\n")
            report.append(f"**Description**: {type_info['description']}\n\n")
        
        # Sort components by frequency (most used first)
        components_with_freq = []
        for component in components:
            frequency = component_frequency.get(component_type, {}).get(component, 0)
            components_with_freq.append((component, frequency))
        
        components_with_freq.sort(key=lambda x: x[1], reverse=True)
        
        report.append("### Components to Create\n\n")
        
        for component, frequency in components_with_freq:
            priority_icon = "🔴" if frequency >= 5 else "🟡" if frequency >= 2 else "🟢"
            report.append(f"{priority_icon} **{component}**\n")
            report.append(f"   - Frequency: {frequency} laptop configurations\n")
            
            # Find source models
            source_key = f"{component_type}:{component}"
            if source_key in source_models:
                models = source_models[source_key][:3]  # Show first 3 models
                report.append(f"   - Found in: {', '.join(models)}")
                if len(source_models[source_key]) > 3:
                    report.append(f" (+{len(source_models[source_key]) - 3} more)")
                report.append("\n")
            
            report.append("\n")
        
        # Shopify Admin instructions
        report.append("### Shopify Admin Creation Steps\n\n")
        report.append("1. Go to **Settings > Custom data > Metaobjects**\n")
        report.append(f"2. Find or create metaobject definition: `{shopify_type}`\n")
        report.append("3. For each component above, click **Add entry**\n")
        report.append("4. Fill in the required fields:\n")
        
        if type_info and 'fields' in type_info:
            for field in type_info['fields']:
                required_text = " **(required)**" if field.get('required') else ""
                report.append(f"   - **{field['key']}**: {field['type']}{required_text}\n")
        
        report.append("5. Save each entry and note the generated GID\n\n")
        
        report.append("---\n\n")
    
    # Implementation guidance
    report.append("## Implementation Guidance\n\n")
    report.append("### Priority Recommendations\n\n")
    report.append("1. **🔴 High Priority**: Components used in 5+ laptop configurations - create these first\n")
    report.append("2. **🟡 Medium Priority**: Components used in 2-4 configurations - create after high priority\n")
    report.append("3. **🟢 Low Priority**: Components used in 1 configuration - create as needed\n\n")
    
    report.append("### Batch Creation Tips\n\n")
    report.append("- Create components in priority order to maximize immediate impact\n")
    report.append("- Use consistent naming conventions matching the component names listed above\n")
    report.append("- Keep track of generated GIDs for future mapping updates\n")
    report.append("- Test product creation with new metaobjects before proceeding to next priority level\n\n")
    
    report.append("### After Creation\n\n")
    report.append("1. Run the GID resolution script again to find newly created components\n")
    report.append("2. Update mapping files using the batch update script\n")
    report.append("3. Test laptop product creation with updated mappings\n")
    report.append("4. Regenerate this report to track progress\n\n")
    
    # Footer
    report.append("---\n\n")
    report.append("*This report was generated automatically by the Laptop Component Mapping Plan Phase 2 scripts.*\n")
    report.append("*For questions or issues, refer to the project documentation or logs.*\n")
    
    return ''.join(report)

def main():
    """
    Main function to generate the missing Shopify entries report
    """
    logger.info("="*60)
    logger.info("MISSING SHOPIFY ENTRIES REPORT GENERATION")
    logger.info("="*60)
    
    try:
        # Load data
        logger.info("Loading GID resolution results...")
        results = load_gid_resolution_results()
        
        logger.info("Loading unmapped components data...")
        unmapped_data = load_unmapped_components()
        
        # Generate report
        logger.info("Generating missing entries report...")
        report_content = generate_missing_report(results, unmapped_data)
        
        # Save report
        output_file = Path("data/analysis/missing_shopify_entries.md")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Report statistics
        not_found_components = results.get('not_found_components', {})
        total_missing = sum(len(components) for components in not_found_components.values())
        
        logger.info("="*60)
        logger.info("MISSING ENTRIES REPORT GENERATED SUCCESSFULLY!")
        logger.info("="*60)
        logger.info(f"Report saved to: {output_file}")
        logger.info(f"Total missing components: {total_missing}")
        logger.info(f"Component types affected: {len([t for t, c in not_found_components.items() if c])}")
        logger.info(f"Report size: {output_file.stat().st_size / 1024:.1f} KB")
        
        return 0
        
    except Exception as e:
        logger.error(f"Critical error generating missing entries report: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)