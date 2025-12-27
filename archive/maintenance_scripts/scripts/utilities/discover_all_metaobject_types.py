#!/usr/bin/env python3
"""
Metaobject Type Discovery Script

This script discovers ALL metaobject types (definitions) in Shopify to identify
the correct type names for laptop component mapping.

Author: Shopify API Developer (Claude Code Sub-Agent System)
Created: 2025-08-06
Purpose: Complete metaobject type discovery for laptop component mapping
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.shopify_api import ShopifyAPIClient, ShopifyAPIError

class MetaobjectTypeDiscovery:
    """Discovers all metaobject types in Shopify"""
    
    def __init__(self):
        """Initialize the discovery service"""
        self.client = ShopifyAPIClient()
        self.discovered_types = {}
        
    def discover_all_metaobject_definitions(self) -> Dict[str, Dict]:
        """
        Discover all metaobject definitions in Shopify
        
        Returns:
            Dictionary mapping type name to definition details
        """
        print("🔍 Discovering ALL metaobject definitions in Shopify...")
        
        # GraphQL query to get all metaobject definitions
        query = """
        query getMetaobjectDefinitions($first: Int!, $after: String) {
            metaobjectDefinitions(first: $first, after: $after) {
                edges {
                    node {
                        id
                        type
                        name
                        description
                        fieldDefinitions {
                            key
                            name
                            type {
                                name
                            }
                        }
                    }
                    cursor
                }
                pageInfo {
                    hasNextPage
                    hasPreviousPage
                }
            }
        }
        """
        
        definitions = {}
        has_next_page = True
        cursor = None
        
        try:
            while has_next_page:
                variables = {"first": 50}
                if cursor:
                    variables["after"] = cursor
                    
                print(f"📡 Fetching definitions (cursor: {cursor or 'start'})...")
                result = self.client.graphql_request(query, variables)
                
                # Check for GraphQL errors
                if "errors" in result:
                    print(f"❌ GraphQL errors: {result['errors']}")
                    break
                    
                data = result.get("data", {}).get("metaobjectDefinitions", {})
                edges = data.get("edges", [])
                
                for edge in edges:
                    definition = edge["node"]
                    type_name = definition["type"]
                    
                    definitions[type_name] = {
                        "id": definition["id"],
                        "type": type_name,
                        "name": definition["name"],
                        "description": definition.get("description", ""),
                        "field_definitions": [
                            {
                                "key": field["key"],
                                "name": field["name"],
                                "type": field["type"]["name"]
                            }
                            for field in definition.get("fieldDefinitions", [])
                        ]
                    }
                    
                    print(f"✅ Found definition: {type_name} ({definition['name']})")
                
                # Update pagination
                page_info = data.get("pageInfo", {})
                has_next_page = page_info.get("hasNextPage", False)
                
                if edges:
                    cursor = edges[-1]["cursor"]
                else:
                    has_next_page = False
                    
        except ShopifyAPIError as e:
            print(f"❌ Failed to discover metaobject definitions: {e}")
            return {}
            
        print(f"✅ Discovered {len(definitions)} metaobject definitions")
        return definitions
    
    def count_metaobjects_by_type(self, type_name: str) -> int:
        """
        Count total metaobjects for a specific type
        
        Args:
            type_name: The metaobject type name
            
        Returns:
            Total count of metaobjects for this type
        """
        query = """
        query countMetaobjects($type: String!, $first: Int!) {
            metaobjects(type: $type, first: $first) {
                edges {
                    node {
                        id
                    }
                }
                pageInfo {
                    hasNextPage
                }
            }
        }
        """
        
        total_count = 0
        has_next_page = True
        cursor = None
        
        try:
            while has_next_page:
                variables = {"type": type_name, "first": 250}
                if cursor:
                    variables["after"] = cursor
                    
                result = self.client.graphql_request(query, variables)
                
                if "errors" in result:
                    print(f"❌ Error counting {type_name}: {result['errors']}")
                    return 0
                    
                data = result.get("data", {}).get("metaobjects", {})
                edges = data.get("edges", [])
                
                total_count += len(edges)
                
                # Update pagination
                page_info = data.get("pageInfo", {})
                has_next_page = page_info.get("hasNextPage", False)
                
                if edges:
                    cursor = edges[-1]["cursor"] if "cursor" in edges[-1] else None
                else:
                    has_next_page = False
                    
        except ShopifyAPIError as e:
            print(f"❌ Failed to count metaobjects for {type_name}: {e}")
            return 0
            
        return total_count
    
    def analyze_laptop_component_types(self, definitions: Dict[str, Dict]) -> Dict[str, List[str]]:
        """
        Analyze definitions to identify laptop component types
        
        Args:
            definitions: All discovered metaobject definitions
            
        Returns:
            Dictionary mapping component categories to potential type names
        """
        print("🧠 Analyzing definitions for laptop component types...")
        
        component_analysis = {
            "processors": [],
            "vga_graphics": [],
            "integrated_graphics": [],
            "displays": [],
            "storage": [],
            "colors": [],
            "os": [],
            "keyboard_layouts": [],
            "keyboard_backlights": []
        }
        
        # Keywords to look for in type names and descriptions
        keywords = {
            "processors": ["processor", "cpu", "chip", "intel", "amd", "apple"],
            "vga_graphics": ["dedicated", "gpu", "graphics", "nvidia", "radeon", "vga"],
            "integrated_graphics": ["integrated", "graphics", "intel", "amd"],
            "displays": ["display", "screen", "monitor", "resolution"],
            "storage": ["storage", "ssd", "hdd", "disk", "drive"],
            "colors": ["color", "colour"],
            "os": ["os", "operating", "system", "windows", "macos"],
            "keyboard_layouts": ["keyboard", "layout"],
            "keyboard_backlights": ["backlight", "backlit", "rgb"]
        }
        
        for type_name, definition in definitions.items():
            name = definition["name"].lower()
            description = definition["description"].lower()
            type_lower = type_name.lower()
            
            # Check each component category
            for category, category_keywords in keywords.items():
                for keyword in category_keywords:
                    if (keyword in type_lower or 
                        keyword in name or 
                        keyword in description):
                        
                        if type_name not in component_analysis[category]:
                            component_analysis[category].append(type_name)
                        break
        
        # Print analysis results
        for category, types in component_analysis.items():
            if types:
                print(f"📋 {category.upper()}: {', '.join(types)}")
            else:
                print(f"❌ {category.upper()}: No matching types found")
                
        return component_analysis
    
    def generate_discovery_report(self, definitions: Dict[str, Dict], 
                                component_analysis: Dict[str, List[str]]) -> Dict:
        """
        Generate comprehensive discovery report
        
        Args:
            definitions: All discovered metaobject definitions
            component_analysis: Component type analysis results
            
        Returns:
            Complete discovery report
        """
        print("📊 Generating comprehensive discovery report...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_definitions": len(definitions),
            "definitions": definitions,
            "component_analysis": component_analysis,
            "type_counts": {},
            "recommendations": {}
        }
        
        # Count metaobjects for each type
        print("🔢 Counting metaobjects for each type...")
        for type_name in definitions.keys():
            count = self.count_metaobjects_by_type(type_name)
            report["type_counts"][type_name] = count
            print(f"📊 {type_name}: {count} entries")
        
        # Generate recommendations
        recommendations = {}
        
        # Expected targets from user requirements
        targets = {
            "processors": 186,
            "vga_graphics": 41,
            "integrated_graphics": 75,
            "displays": "unknown",
            "storage": "unknown"
        }
        
        for category, types in component_analysis.items():
            category_recs = []
            
            if not types:
                category_recs.append(f"❌ No metaobject types found for {category}")
                category_recs.append(f"⚠️ May need to create metaobject definition in Shopify Admin")
            else:
                # Find the type with the most entries (likely the correct one)
                best_type = None
                best_count = 0
                
                for type_name in types:
                    count = report["type_counts"].get(type_name, 0)
                    if count > best_count:
                        best_count = count
                        best_type = type_name
                
                if best_type:
                    category_recs.append(f"✅ Recommended type: {best_type} ({best_count} entries)")
                    
                    # Check against targets
                    if category in targets and isinstance(targets[category], int):
                        target = targets[category]
                        if best_count >= target:
                            category_recs.append(f"🎯 Meets target: {best_count} >= {target}")
                        else:
                            category_recs.append(f"⚠️ Below target: {best_count} < {target}")
                
                # List all alternatives
                if len(types) > 1:
                    alternatives = [t for t in types if t != best_type]
                    category_recs.append(f"🔄 Alternatives: {', '.join(alternatives)}")
            
            recommendations[category] = category_recs
        
        report["recommendations"] = recommendations
        
        return report
    
    def run_complete_discovery(self) -> str:
        """
        Run complete metaobject type discovery process
        
        Returns:
            Path to the generated report file
        """
        print("🚀 Starting complete metaobject type discovery...")
        print("=" * 80)
        
        # Step 1: Discover all definitions
        definitions = self.discover_all_metaobject_definitions()
        if not definitions:
            print("❌ No metaobject definitions found!")
            return ""
        
        print("\n" + "=" * 80)
        
        # Step 2: Analyze for laptop components
        component_analysis = self.analyze_laptop_component_types(definitions)
        
        print("\n" + "=" * 80)
        
        # Step 3: Generate report
        report = self.generate_discovery_report(definitions, component_analysis)
        
        # Step 4: Save report
        report_path = f"data/analysis/metaobject_type_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Discovery report saved to: {report_path}")
        
        # Print summary
        print("\n" + "🎯 DISCOVERY SUMMARY" + "\n" + "=" * 80)
        print(f"📊 Total metaobject definitions: {len(definitions)}")
        print(f"📁 Report file: {report_path}")
        
        print("\n🏷️ RECOMMENDED METAOBJECT TYPES:")
        for category, recs in report["recommendations"].items():
            print(f"\n{category.upper()}:")
            for rec in recs:
                print(f"  {rec}")
        
        print("\n" + "=" * 80)
        print("✅ Complete metaobject type discovery finished!")
        
        return report_path

def main():
    """Main execution function"""
    try:
        discovery = MetaobjectTypeDiscovery()
        report_path = discovery.run_complete_discovery()
        
        if report_path:
            print(f"\n🎉 SUCCESS: Discovery complete! Report saved to: {report_path}")
            return 0
        else:
            print("\n❌ FAILED: Discovery could not be completed")
            return 1
            
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)