#!/usr/bin/env python3
"""
Component Mapping Validation Script - Phase 3.1

This script validates that all laptop components have proper mappings and GID format validation.
Part of the Laptop Component Mapping Plan Phase 3: Comprehensive Testing & Validation.

Features:
- Validates all laptop components have metaobject mappings
- Checks GID format and accessibility
- Detects duplicate mappings
- Generates comprehensive validation reports
"""

import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from collections import defaultdict

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from repositories.metaobject_repository import MetaobjectRepository
from repositories.product_data_repository import ProductDataRepository

class ComponentMappingValidator:
    """Validates laptop component mappings for completeness and correctness."""
    
    def __init__(self):
        """Initialize validator with repository dependencies."""
        self.metaobject_repo = MetaobjectRepository()
        self.product_data_repo = ProductDataRepository()
        self.validation_results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "script_version": "1.0.0",
                "validation_categories": 8
            },
            "summary": {
                "total_components": 0,
                "mapped_components": 0,
                "unmapped_components": 0,
                "duplicate_mappings": 0,
                "invalid_gids": 0,
                "validation_score": 0.0
            },
            "component_analysis": {},
            "gid_validation": {
                "valid_gids": [],
                "invalid_gids": [],
                "duplicate_gids": []
            },
            "mapping_issues": [],
            "recommendations": []
        }
        
    def validate_gid_format(self, gid: str) -> bool:
        """
        Validate Shopify GID format.
        
        Args:
            gid: Global ID string to validate
            
        Returns:
            bool: True if GID format is valid
        """
        if not gid or not isinstance(gid, str):
            return False
            
        # Shopify GID format: gid://shopify/Metaobject/{id}
        pattern = r'^gid://shopify/Metaobject/\d+$'
        return bool(re.match(pattern, gid))
    
    def extract_all_laptop_components(self) -> Dict[str, Set[str]]:
        """
        Extract all unique components from laptop data files.
        
        Returns:
            dict: Component types mapped to sets of component names
        """
        components_by_type = defaultdict(set)
        
        try:
            # Get all laptop brands
            all_brands = self.product_data_repo.get_all_brands()
            
            for brand in all_brands:
                brand_data = self.product_data_repo.get_brand_data(brand)
                
                for model_name, model_data in brand_data.get("models", {}).items():
                    configurations = model_data.get("configurations", [])
                    
                    for config in configurations:
                        # Extract components based on field mapping
                        component_fields = {
                            "processors": config.get("cpu"),
                            "vga": config.get("vga"), 
                            "graphics": config.get("gpu"),
                            "displays": config.get("display"),
                            "storage": config.get("storage"),
                            "os": config.get("os"),
                            "keyboard_layouts": config.get("keyboard_layout"),
                            "keyboard_backlights": config.get("keyboard_backlight")
                        }
                        
                        for component_type, component_value in component_fields.items():
                            if component_value and component_value.strip():
                                components_by_type[component_type].add(component_value.strip())
                                
        except Exception as e:
            self.validation_results["mapping_issues"].append({
                "type": "extraction_error",
                "message": f"Failed to extract laptop components: {str(e)}",
                "severity": "high"
            })
            
        return {k: v for k, v in components_by_type.items()}
    
    def validate_component_mappings(self, components_by_type: Dict[str, Set[str]]) -> None:
        """
        Validate that all components have proper mappings.
        
        Args:
            components_by_type: Components organized by type
        """
        total_components = 0
        mapped_components = 0
        
        for component_type, components in components_by_type.items():
            total_components += len(components)
            
            # Get metaobject mappings for this component type
            try:
                if hasattr(self.metaobject_repo, f'get_{component_type}'):
                    mappings = getattr(self.metaobject_repo, f'get_{component_type}')()
                else:
                    mappings = {}
                    
                mapped_count = 0
                unmapped_count = 0
                unmapped_components = []
                
                for component in components:
                    if component in mappings:
                        mapped_count += 1
                        mapped_components += 1
                    else:
                        unmapped_count += 1
                        unmapped_components.append(component)
                
                # Store component type analysis
                self.validation_results["component_analysis"][component_type] = {
                    "total_components": len(components),
                    "mapped_components": mapped_count,
                    "unmapped_components": unmapped_count,
                    "mapping_percentage": (mapped_count / len(components) * 100) if components else 0,
                    "unmapped_list": unmapped_components,
                    "metaobject_count": len(mappings)
                }
                
                # Add issues for unmapped components
                if unmapped_components:
                    self.validation_results["mapping_issues"].append({
                        "type": "unmapped_components",
                        "component_type": component_type,
                        "count": unmapped_count,
                        "components": unmapped_components,
                        "severity": "medium" if unmapped_count > 5 else "low"
                    })
                    
            except Exception as e:
                self.validation_results["mapping_issues"].append({
                    "type": "mapping_access_error",
                    "component_type": component_type,
                    "message": f"Failed to access mappings: {str(e)}",
                    "severity": "high"
                })
        
        # Update summary
        self.validation_results["summary"]["total_components"] = total_components
        self.validation_results["summary"]["mapped_components"] = mapped_components
        self.validation_results["summary"]["unmapped_components"] = total_components - mapped_components
    
    def validate_gid_formats(self) -> None:
        """Validate all GID formats in metaobject mappings."""
        all_gids = []
        gid_to_component = {}
        
        # Collect all GIDs from all component types
        component_types = [
            "processors", "vga", "graphics", "displays", 
            "storage", "colors", "os", "keyboard_layouts", "keyboard_backlights"
        ]
        
        for component_type in component_types:
            try:
                if hasattr(self.metaobject_repo, f'get_{component_type}'):
                    mappings = getattr(self.metaobject_repo, f'get_{component_type}')()
                    
                    for component_name, gid in mappings.items():
                        all_gids.append(gid)
                        
                        # Track GID to component for duplicate detection
                        if gid in gid_to_component:
                            gid_to_component[gid].append(f"{component_type}:{component_name}")
                        else:
                            gid_to_component[gid] = [f"{component_type}:{component_name}"]
                        
                        # Validate GID format
                        if self.validate_gid_format(gid):
                            self.validation_results["gid_validation"]["valid_gids"].append({
                                "gid": gid,
                                "component_type": component_type,
                                "component_name": component_name
                            })
                        else:
                            self.validation_results["gid_validation"]["invalid_gids"].append({
                                "gid": gid,
                                "component_type": component_type,
                                "component_name": component_name,
                                "issue": "invalid_format"
                            })
                            
            except Exception as e:
                self.validation_results["mapping_issues"].append({
                    "type": "gid_validation_error",
                    "component_type": component_type,
                    "message": f"Failed to validate GIDs: {str(e)}",
                    "severity": "medium"
                })
        
        # Check for duplicate GIDs
        for gid, components in gid_to_component.items():
            if len(components) > 1:
                self.validation_results["gid_validation"]["duplicate_gids"].append({
                    "gid": gid,
                    "components": components,
                    "count": len(components)
                })
        
        # Update summary
        self.validation_results["summary"]["duplicate_mappings"] = len(self.validation_results["gid_validation"]["duplicate_gids"])
        self.validation_results["summary"]["invalid_gids"] = len(self.validation_results["gid_validation"]["invalid_gids"])
    
    def calculate_validation_score(self) -> None:
        """Calculate overall validation score."""
        summary = self.validation_results["summary"]
        
        # Base score from mapping completeness
        mapping_score = 0
        if summary["total_components"] > 0:
            mapping_score = (summary["mapped_components"] / summary["total_components"]) * 100
        
        # Penalties for issues
        penalty = 0
        penalty += summary["duplicate_mappings"] * 2  # 2 points per duplicate
        penalty += summary["invalid_gids"] * 5        # 5 points per invalid GID
        
        # Issue severity penalties
        for issue in self.validation_results["mapping_issues"]:
            if issue["severity"] == "high":
                penalty += 10
            elif issue["severity"] == "medium":
                penalty += 5
            elif issue["severity"] == "low":
                penalty += 2
        
        # Final score (0-100)
        final_score = max(0, mapping_score - penalty)
        self.validation_results["summary"]["validation_score"] = round(final_score, 2)
    
    def generate_recommendations(self) -> None:
        """Generate actionable recommendations based on validation results."""
        recommendations = []
        summary = self.validation_results["summary"]
        
        # Mapping completeness recommendations
        if summary["unmapped_components"] > 0:
            recommendations.append({
                "priority": "high",
                "category": "mapping_completeness",
                "title": f"Resolve {summary['unmapped_components']} unmapped components",
                "description": "Run GID resolution scripts to find missing metaobjects in Shopify",
                "action": "Execute scripts/metaobjects/resolve_missing_gids.py"
            })
        
        # GID format recommendations
        if summary["invalid_gids"] > 0:
            recommendations.append({
                "priority": "high",
                "category": "data_integrity",
                "title": f"Fix {summary['invalid_gids']} invalid GID formats",
                "description": "Invalid GIDs will cause API failures during product creation",
                "action": "Review and correct GID formats in metaobject mapping files"
            })
        
        # Duplicate GID recommendations
        if summary["duplicate_mappings"] > 0:
            recommendations.append({
                "priority": "medium", 
                "category": "data_consistency",
                "title": f"Resolve {summary['duplicate_mappings']} duplicate GID mappings",
                "description": "Multiple components mapped to same GID can cause unexpected behavior",
                "action": "Review component mappings and ensure unique GID assignments"
            })
        
        # Performance recommendations
        if summary["validation_score"] < 80:
            recommendations.append({
                "priority": "medium",
                "category": "system_health",
                "title": f"Improve validation score from {summary['validation_score']}%",
                "description": "Low validation scores indicate system reliability issues",
                "action": "Address high-priority mapping and GID issues first"
            })
        
        # Success recommendations
        if summary["validation_score"] >= 95:
            recommendations.append({
                "priority": "low",
                "category": "maintenance",
                "title": "System validation excellent - continue monitoring",
                "description": "Maintain current mapping quality with regular validation",
                "action": "Schedule weekly validation runs to catch drift early"
            })
        
        self.validation_results["recommendations"] = recommendations
    
    def save_results(self, output_dir: str = "data/analysis") -> str:
        """
        Save validation results to file.
        
        Args:
            output_dir: Directory to save results
            
        Returns:
            str: Path to saved file
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON results
        json_file = os.path.join(output_dir, "component_mapping_validation.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, ensure_ascii=False)
        
        return json_file
    
    def generate_markdown_report(self, output_dir: str = "data/analysis") -> str:
        """
        Generate markdown validation report.
        
        Args:
            output_dir: Directory to save report
            
        Returns:
            str: Path to saved markdown file
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        summary = self.validation_results["summary"]
        metadata = self.validation_results["metadata"]
        
        report_lines = [
            "# Component Mapping Validation Report",
            f"**Generated**: {metadata['timestamp']}",
            f"**Script Version**: {metadata['script_version']}",
            f"**Validation Score**: {summary['validation_score']}/100",
            "",
            "## Executive Summary",
            "",
            f"- **Total Components**: {summary['total_components']}",
            f"- **Mapped Components**: {summary['mapped_components']} ({(summary['mapped_components']/summary['total_components']*100):.1f}%)" if summary['total_components'] > 0 else "- **Mapped Components**: 0 (0.0%)",
            f"- **Unmapped Components**: {summary['unmapped_components']}",
            f"- **Invalid GIDs**: {summary['invalid_gids']}",
            f"- **Duplicate Mappings**: {summary['duplicate_mappings']}",
            "",
            "## Component Type Analysis",
            ""
        ]
        
        # Component type breakdown
        for component_type, analysis in self.validation_results["component_analysis"].items():
            status_emoji = "✅" if analysis["mapping_percentage"] >= 90 else "⚠️" if analysis["mapping_percentage"] >= 70 else "❌"
            report_lines.extend([
                f"### {component_type.title()} {status_emoji}",
                "",
                f"- **Total Components**: {analysis['total_components']}",
                f"- **Mapped**: {analysis['mapped_components']} ({analysis['mapping_percentage']:.1f}%)",
                f"- **Unmapped**: {analysis['unmapped_components']}",
                f"- **Metaobjects Available**: {analysis['metaobject_count']}",
                ""
            ])
            
            if analysis["unmapped_list"]:
                report_lines.extend([
                    "**Unmapped Components:**",
                    ""
                ])
                for component in analysis["unmapped_list"]:
                    report_lines.append(f"- {component}")
                report_lines.append("")
        
        # GID Validation Results
        report_lines.extend([
            "## GID Validation Results",
            "",
            f"- **Valid GIDs**: {len(self.validation_results['gid_validation']['valid_gids'])}",
            f"- **Invalid GIDs**: {len(self.validation_results['gid_validation']['invalid_gids'])}",
            f"- **Duplicate GIDs**: {len(self.validation_results['gid_validation']['duplicate_gids'])}",
            ""
        ])
        
        # Invalid GIDs
        if self.validation_results["gid_validation"]["invalid_gids"]:
            report_lines.extend([
                "### Invalid GIDs ❌",
                ""
            ])
            for invalid in self.validation_results["gid_validation"]["invalid_gids"]:
                report_lines.append(f"- **{invalid['component_type']}**: {invalid['component_name']} → `{invalid['gid']}` ({invalid['issue']})")
            report_lines.append("")
        
        # Duplicate GIDs
        if self.validation_results["gid_validation"]["duplicate_gids"]:
            report_lines.extend([
                "### Duplicate GIDs ⚠️",
                ""
            ])
            for duplicate in self.validation_results["gid_validation"]["duplicate_gids"]:
                report_lines.append(f"- **GID**: `{duplicate['gid']}`")
                report_lines.append(f"  - Components: {', '.join(duplicate['components'])}")
            report_lines.append("")
        
        # Issues
        if self.validation_results["mapping_issues"]:
            report_lines.extend([
                "## Issues Detected",
                ""
            ])
            
            for issue in self.validation_results["mapping_issues"]:
                severity_emoji = "🔴" if issue["severity"] == "high" else "🟡" if issue["severity"] == "medium" else "🟢"
                report_lines.append(f"### {severity_emoji} {issue.get('type', 'Unknown Issue').replace('_', ' ').title()}")
                
                if "component_type" in issue:
                    report_lines.append(f"**Component Type**: {issue['component_type']}")
                if "count" in issue:
                    report_lines.append(f"**Count**: {issue['count']}")
                if "message" in issue:
                    report_lines.append(f"**Message**: {issue['message']}")
                
                report_lines.append("")
        
        # Recommendations
        if self.validation_results["recommendations"]:
            report_lines.extend([
                "## Recommendations",
                ""
            ])
            
            for rec in self.validation_results["recommendations"]:
                priority_emoji = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
                report_lines.extend([
                    f"### {priority_emoji} {rec['title']}",
                    f"**Priority**: {rec['priority'].title()}",
                    f"**Category**: {rec['category'].replace('_', ' ').title()}",
                    f"**Description**: {rec['description']}",
                    f"**Action**: `{rec['action']}`",
                    ""
                ])
        
        report_lines.extend([
            "---",
            "",
            "*This report was generated by the Component Mapping Validation script.*",
            "*For questions or issues, refer to the project documentation.*"
        ])
        
        # Save markdown report
        md_file = os.path.join(output_dir, "component_mapping_validation.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        return md_file
    
    def run_validation(self) -> Dict[str, Any]:
        """
        Run complete component mapping validation.
        
        Returns:
            dict: Validation results
        """
        print("🔍 Starting Component Mapping Validation...")
        print("=" * 60)
        
        # Step 1: Extract all components
        print("1. Extracting laptop components...")
        components_by_type = self.extract_all_laptop_components()
        total_components = sum(len(components) for components in components_by_type.values())
        print(f"   ✅ Found {total_components} unique components across {len(components_by_type)} types")
        
        # Step 2: Validate component mappings
        print("2. Validating component mappings...")
        self.validate_component_mappings(components_by_type)
        mapped_count = self.validation_results["summary"]["mapped_components"]
        print(f"   ✅ {mapped_count}/{total_components} components have mappings ({mapped_count/total_components*100:.1f}%)")
        
        # Step 3: Validate GID formats
        print("3. Validating GID formats...")
        self.validate_gid_formats()
        valid_gids = len(self.validation_results["gid_validation"]["valid_gids"])
        invalid_gids = self.validation_results["summary"]["invalid_gids"]
        print(f"   ✅ {valid_gids} valid GIDs, {invalid_gids} invalid GIDs")
        
        # Step 4: Calculate validation score
        print("4. Calculating validation score...")
        self.calculate_validation_score()
        score = self.validation_results["summary"]["validation_score"]
        print(f"   ✅ Validation Score: {score}/100")
        
        # Step 5: Generate recommendations
        print("5. Generating recommendations...")
        self.generate_recommendations()
        rec_count = len(self.validation_results["recommendations"])
        print(f"   ✅ Generated {rec_count} recommendations")
        
        # Step 6: Save results
        print("6. Saving validation results...")
        json_file = self.save_results()
        md_file = self.generate_markdown_report()
        print(f"   ✅ JSON results: {json_file}")
        print(f"   ✅ Markdown report: {md_file}")
        
        print("=" * 60)
        print(f"✅ Validation Complete! Score: {score}/100")
        
        return self.validation_results

def main():
    """Main execution function."""
    try:
        validator = ComponentMappingValidator()
        results = validator.run_validation()
        
        # Exit with appropriate code based on validation score
        score = results["summary"]["validation_score"]
        if score >= 90:
            print("🎉 Excellent validation score - system ready for production!")
            sys.exit(0)
        elif score >= 70:
            print("⚠️  Good validation score - minor issues to address")
            sys.exit(0)
        else:
            print("❌ Low validation score - significant issues need attention")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Validation failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()