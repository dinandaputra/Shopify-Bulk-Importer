#!/usr/bin/env python3
"""
Laptop Component Analysis Script - Phase 1

Analyzes all laptop specifications from data/products/laptops/, extracts components,
cross-references with existing metaobject mappings, and identifies unmapped components
for Phase 2 GID resolution.

Usage:
    python scripts/analysis/analyze_laptop_components.py

Output:
    - data/analysis/unmapped_components.json (machine-readable)
    - data/analysis/unmapped_components.md (human-readable report)
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Set, Any, Optional
from pathlib import Path
from collections import defaultdict, Counter

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from repositories.metaobject_repository import MetaobjectRepository
    from repositories.product_data_repository import ProductDataRepository
except ImportError as e:
    print(f"Error importing repositories: {e}")
    print("Please ensure you're running from the project root directory")
    sys.exit(1)


class ComponentAnalysisResult:
    """Data class for analysis results."""
    
    def __init__(self):
        self.extracted_components: Dict[str, Set[str]] = defaultdict(set)
        self.existing_mappings: Dict[str, Dict[str, str]] = {}
        self.unmapped_components: Dict[str, List[str]] = defaultdict(list)
        self.component_frequency: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.source_models: Dict[str, List[str]] = defaultdict(list)  # Track which models use which components
        self.statistics = {
            'total_models': 0,
            'total_configurations': 0,
            'analysis_timestamp': datetime.now().isoformat(),
            'script_version': '1.0.0'
        }


class LaptopComponentAnalyzer:
    """
    Main analyzer class for laptop component analysis.
    
    Extracts components from all laptop JSON files, cross-references with
    existing metaobject mappings, and generates comprehensive unmapped reports.
    """
    
    # Component field mapping from laptop JSON to metaobject type
    COMPONENT_FIELD_MAPPING = {
        'cpu': 'processors',
        'vga': 'vga', 
        'gpu': 'graphics',           # Integrated graphics
        'display': 'displays',
        'storage': 'storage',
        'os': 'os',
        'keyboard_layout': 'keyboard_layouts',
        'keyboard_backlight': 'keyboard_backlights'
    }
    
    def __init__(self):
        """Initialize analyzer with repository dependencies."""
        try:
            self.metaobject_repo = MetaobjectRepository()
            self.product_repo = ProductDataRepository()
            print("✅ Repositories initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing repositories: {e}")
            raise
    
    def analyze_components(self) -> ComponentAnalysisResult:
        """
        Main analysis method.
        
        Returns:
            ComponentAnalysisResult with all extracted components and mapping analysis
        """
        print("🔍 Starting laptop component analysis...")
        result = ComponentAnalysisResult()
        
        # Step 1: Extract components from all laptop data
        print("📊 Step 1: Extracting components from laptop JSON files...")
        self._extract_components_from_laptops(result)
        
        # Step 2: Load existing metaobject mappings
        print("🗂️  Step 2: Loading existing metaobject mappings...")
        self._load_existing_mappings(result)
        
        # Step 3: Cross-reference and identify unmapped
        print("🔄 Step 3: Cross-referencing components with mappings...")
        self._cross_reference_components(result)
        
        # Step 4: Generate statistics
        print("📈 Step 4: Generating analysis statistics...")
        self._generate_statistics(result)
        
        print("✅ Component analysis completed successfully!")
        return result
    
    def _extract_components_from_laptops(self, result: ComponentAnalysisResult):
        """Extract all components from laptop JSON files."""
        try:
            all_brands = self.product_repo.get_all_brands()
            print(f"📁 Found {len(all_brands)} laptop brands to analyze")
            
            for brand in all_brands:
                print(f"  🔍 Analyzing {brand} laptops...")
                try:
                    brand_data = self.product_repo.get_brand_data(brand)
                    self._extract_components_from_brand_data(brand, brand_data, result)
                except Exception as e:
                    print(f"  ⚠️  Warning: Error processing {brand}: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error during component extraction: {e}")
            raise
    
    def _extract_components_from_brand_data(self, brand: str, brand_data: Dict, result: ComponentAnalysisResult):
        """Extract components from a single brand's data."""
        models_processed = 0
        configurations_processed = 0
        
        # Handle JSON structure: brand_data has 'models' key containing the actual model data
        models_data = brand_data.get('models', {})
        
        for model_name, model_info in models_data.items():
            models_processed += 1
            configurations = model_info.get('configurations', [])
            
            for config in configurations:
                configurations_processed += 1
                
                # Extract each component type
                for json_field, metaobject_type in self.COMPONENT_FIELD_MAPPING.items():
                    component_value = config.get(json_field)
                    
                    if component_value and component_value.strip():
                        # Normalize component name (strip whitespace)
                        normalized_value = component_value.strip()
                        
                        # Add to extracted components
                        result.extracted_components[metaobject_type].add(normalized_value)
                        
                        # Track frequency
                        result.component_frequency[metaobject_type][normalized_value] += 1
                        
                        # Track source models
                        source_key = f"{brand} {model_name}"
                        result.source_models[f"{metaobject_type}:{normalized_value}"].append(source_key)
        
        print(f"    ✅ {brand}: {models_processed} models, {configurations_processed} configurations")
        result.statistics['total_models'] += models_processed
        result.statistics['total_configurations'] += configurations_processed
    
    def _load_existing_mappings(self, result: ComponentAnalysisResult):
        """Load all existing metaobject mappings."""
        mapping_methods = {
            'processors': self.metaobject_repo.get_processor_mapping,
            'vga': self.metaobject_repo.get_vga_mapping,
            'graphics': self.metaobject_repo.get_graphics_mapping,
            'displays': self.metaobject_repo.get_display_mapping,
            'storage': self.metaobject_repo.get_storage_mapping,
            'os': self.metaobject_repo.get_os_mapping,
            'keyboard_layouts': self.metaobject_repo.get_keyboard_layout_mapping,
            'keyboard_backlights': self.metaobject_repo.get_keyboard_backlight_mapping
        }
        
        total_mappings = 0
        for component_type, method in mapping_methods.items():
            try:
                mappings = method()
                result.existing_mappings[component_type] = mappings
                mapping_count = len(mappings)
                total_mappings += mapping_count
                print(f"  📋 {component_type}: {mapping_count} existing mappings")
            except Exception as e:
                print(f"  ⚠️  Warning: Error loading {component_type} mappings: {e}")
                result.existing_mappings[component_type] = {}
        
        print(f"  ✅ Total existing mappings loaded: {total_mappings}")
    
    def _cross_reference_components(self, result: ComponentAnalysisResult):
        """Cross-reference extracted components with existing mappings."""
        total_extracted = 0
        total_unmapped = 0
        
        for component_type, extracted_components in result.extracted_components.items():
            existing_mapping = result.existing_mappings.get(component_type, {})
            
            extracted_count = len(extracted_components)
            total_extracted += extracted_count
            
            # Find unmapped components
            unmapped = []
            for component in extracted_components:
                if component not in existing_mapping:
                    unmapped.append(component)
            
            result.unmapped_components[component_type] = unmapped
            unmapped_count = len(unmapped)
            total_unmapped += unmapped_count
            
            mapped_count = extracted_count - unmapped_count
            print(f"  📊 {component_type}: {extracted_count} total, {mapped_count} mapped, {unmapped_count} unmapped")
        
        print(f"  ✅ Total: {total_extracted} components, {total_unmapped} unmapped ({total_unmapped/total_extracted*100:.1f}%)")
    
    def _generate_statistics(self, result: ComponentAnalysisResult):
        """Generate comprehensive analysis statistics."""
        result.statistics.update({
            'total_extracted_components': sum(len(components) for components in result.extracted_components.values()),
            'total_unmapped_components': sum(len(unmapped) for unmapped in result.unmapped_components.values()),
            'component_type_breakdown': {
                component_type: {
                    'extracted': len(result.extracted_components[component_type]),
                    'mapped': len(result.existing_mappings.get(component_type, {})),
                    'unmapped': len(result.unmapped_components[component_type])
                }
                for component_type in self.COMPONENT_FIELD_MAPPING.values()
            }
        })
    
    def save_results(self, result: ComponentAnalysisResult, output_dir: str = "data/analysis"):
        """
        Save analysis results to JSON and Markdown files.
        
        Args:
            result: Analysis results to save
            output_dir: Output directory path
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON data (machine-readable)
        json_path = os.path.join(output_dir, "unmapped_components.json")
        self._save_json_results(result, json_path)
        
        # Save Markdown report (human-readable)
        md_path = os.path.join(output_dir, "unmapped_components.md")
        self._save_markdown_report(result, md_path)
        
        print(f"📄 Results saved:")
        print(f"  📊 JSON data: {json_path}")
        print(f"  📝 Report: {md_path}")
    
    def _save_json_results(self, result: ComponentAnalysisResult, file_path: str):
        """Save results as JSON for machine processing."""
        # Convert sets to lists for JSON serialization
        json_data = {
            'metadata': result.statistics,
            'extracted_components': {
                component_type: list(components) 
                for component_type, components in result.extracted_components.items()
            },
            'existing_mappings': result.existing_mappings,
            'unmapped_components': dict(result.unmapped_components),
            'component_frequency': {
                component_type: dict(freq_dict)
                for component_type, freq_dict in result.component_frequency.items()
            },
            'source_models': dict(result.source_models)
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    def _save_markdown_report(self, result: ComponentAnalysisResult, file_path: str):
        """Generate comprehensive Markdown report."""
        total_unmapped = result.statistics['total_unmapped_components']
        total_extracted = result.statistics['total_extracted_components']
        unmapped_percentage = (total_unmapped / total_extracted * 100) if total_extracted > 0 else 0
        
        md_content = f"""# Laptop Component Mapping Analysis Report

**Generated**: {result.statistics['analysis_timestamp']}  
**Script Version**: {result.statistics['script_version']}  
**Analysis Scope**: {result.statistics['total_models']} laptop models, {result.statistics['total_configurations']} configurations

## Executive Summary

- **📊 Total Components Extracted**: {total_extracted}
- **✅ Already Mapped**: {total_extracted - total_unmapped} ({100 - unmapped_percentage:.1f}%)
- **❌ Missing Mappings**: {total_unmapped} ({unmapped_percentage:.1f}%)

## Missing Components by Type

"""
        
        # Add unmapped components by type
        for component_type in sorted(result.unmapped_components.keys()):
            unmapped = result.unmapped_components[component_type]
            if not unmapped:
                continue
                
            md_content += f"\n### {component_type.title()} ({len(unmapped)} missing)\n\n"
            
            for component in sorted(unmapped):
                # Get frequency and source models
                frequency = result.component_frequency[component_type].get(component, 0)
                sources = result.source_models.get(f"{component_type}:{component}", [])
                source_list = ", ".join(sources[:3])  # Show first 3 sources
                if len(sources) > 3:
                    source_list += f" (+{len(sources) - 3} more)"
                
                md_content += f"- **{component}**\n"
                md_content += f"  - Frequency: {frequency} configurations\n"
                md_content += f"  - Found in: {source_list}\n\n"
        
        # Add component type breakdown
        md_content += "\n## Component Type Analysis\n\n| Component Type | Extracted | Mapped | Unmapped | Coverage |\n"
        md_content += "|---|---|---|---|---|\n"
        
        for component_type, stats in result.statistics['component_type_breakdown'].items():
            extracted = stats['extracted']
            mapped = stats['mapped']  # existing mapping count
            unmapped = stats['unmapped']
            actually_mapped = extracted - unmapped
            coverage = (actually_mapped / extracted * 100) if extracted > 0 else 0
            
            md_content += f"| {component_type.title()} | {extracted} | {actually_mapped} | {unmapped} | {coverage:.1f}% |\n"
        
        # Add next steps
        md_content += f"""
## Next Steps for Phase 2

### High Priority (Frequent Components)
"""
        
        # Find most frequent unmapped components
        frequent_unmapped = []
        for component_type, unmapped_list in result.unmapped_components.items():
            for component in unmapped_list:
                frequency = result.component_frequency[component_type].get(component, 0)
                if frequency >= 2:  # Used in 2+ configurations
                    frequent_unmapped.append((component_type, component, frequency))
        
        # Sort by frequency
        frequent_unmapped.sort(key=lambda x: x[2], reverse=True)
        
        for component_type, component, frequency in frequent_unmapped[:10]:  # Top 10
            md_content += f"- **{component}** ({component_type}) - {frequency} configurations\n"
        
        md_content += """
### Phase 2 GID Resolution Plan

1. **Query Shopify** for each unmapped component using GraphQL
2. **Extract GIDs** for found components and update JSON mappings
3. **Document missing entries** that need manual creation in Shopify
4. **Generate updated mappings** for Phase 3 validation

### Technical Implementation

- Use `scripts/metaobjects/resolve_missing_gids.py` (to be created)
- Target GraphQL metaobjects query with component type filtering
- Update corresponding JSON files in `data/metaobjects/`
- Generate `missing_shopify_entries.md` for manual action

---

**Analysis completed successfully** ✅  
**Ready for Phase 2 GID Resolution** 🚀
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)


def main():
    """Main execution function."""
    print("🚀 Laptop Component Analysis - Phase 1")
    print("=" * 50)
    
    try:
        # Initialize analyzer
        analyzer = LaptopComponentAnalyzer()
        
        # Run analysis
        result = analyzer.analyze_components()
        
        # Save results
        analyzer.save_results(result)
        
        print("\n" + "=" * 50)
        print("✅ Phase 1 Analysis Complete!")
        print(f"📊 Found {result.statistics['total_unmapped_components']} unmapped components")
        print(f"📁 Results saved to data/analysis/")
        print(f"🚀 Ready for Phase 2: GID Resolution")
        
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        print("Please check error details above and try again.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())