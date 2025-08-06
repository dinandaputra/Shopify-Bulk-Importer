#!/usr/bin/env python3
"""
Phase 3 Comprehensive Validation Master Script

This script orchestrates all Phase 3 testing components to provide complete validation
of the laptop component mapping system. It runs all validation tests in sequence and
generates a comprehensive summary report.

Part of the Laptop Component Mapping Plan Phase 3: Comprehensive Testing & Validation.

Features:
- Runs all 4 validation scripts in optimal order
- Handles dependencies between tests
- Generates unified summary report
- Provides actionable recommendations
- Tracks overall system readiness for production
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

class Phase3ValidationOrchestrator:
    """Orchestrates all Phase 3 validation tests."""
    
    def __init__(self, verbose: bool = False):
        """
        Initialize orchestrator.
        
        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.script_dir = Path(__file__).parent
        self.results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "script_version": "1.0.0",
                "phase": "Phase 3: Comprehensive Testing & Validation",
                "total_validation_scripts": 4
            },
            "summary": {
                "overall_success": False,
                "scripts_passed": 0,
                "scripts_failed": 0,
                "critical_issues": 0,
                "production_ready": False,
                "overall_score": 0.0
            },
            "script_results": [],
            "consolidated_recommendations": [],
            "system_assessment": {}
        }
        
        # Define validation scripts in execution order
        self.validation_scripts = [
            {
                "name": "Component Mapping Validation",
                "script": "validate_component_mapping.py",
                "description": "Validates all laptop components have proper metaobject mappings",
                "critical": True,
                "dependencies": []
            },
            {
                "name": "Shopify Entry Verification", 
                "script": "verify_shopify_entries.py",
                "description": "Verifies all GIDs exist and are accessible in Shopify",
                "critical": True,
                "dependencies": ["validate_component_mapping.py"]
            },
            {
                "name": "Product Creation Testing",
                "script": "test_laptop_product_creation.py",
                "description": "Tests complete laptop product creation with metafields",
                "critical": True,
                "dependencies": ["validate_component_mapping.py", "verify_shopify_entries.py"]
            },
            {
                "name": "End-to-End Integration Testing",
                "script": "test_e2e_integration.py",
                "description": "Tests complete workflow from selection to Shopify upload",
                "critical": False,
                "dependencies": []
            }
        ]
    
    def log(self, message: str, level: str = "INFO") -> None:
        """
        Log message with timestamp.
        
        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "SUCCESS": "✅"
        }.get(level, "ℹ️")
        
        print(f"[{timestamp}] {prefix} {message}")
        
        if self.verbose and level in ["WARNING", "ERROR"]:
            print(f"    Detail: {message}")
    
    def run_validation_script(self, script_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single validation script.
        
        Args:
            script_info: Script information dictionary
            
        Returns:
            dict: Script execution result
        """
        script_name = script_info["script"]
        script_path = self.script_dir / script_name
        
        result = {
            "script_name": script_name,
            "display_name": script_info["name"],
            "description": script_info["description"],
            "critical": script_info["critical"],
            "success": False,
            "exit_code": None,
            "execution_time": 0.0,
            "output": "",
            "error": "",
            "results_file": None,
            "recommendations": []
        }
        
        if not script_path.exists():
            result["error"] = f"Script not found: {script_path}"
            self.log(f"Script not found: {script_name}", "ERROR")
            return result
        
        self.log(f"Running {script_info['name']}...")
        
        start_time = time.time()
        
        try:
            # Run the script
            process = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            result["exit_code"] = process.returncode
            result["output"] = process.stdout
            result["error"] = process.stderr
            result["success"] = process.returncode == 0
            result["execution_time"] = time.time() - start_time
            
            if result["success"]:
                self.log(f"{script_info['name']} completed successfully", "SUCCESS")
            else:
                self.log(f"{script_info['name']} failed with exit code {process.returncode}", "ERROR")
                if self.verbose and process.stderr:
                    self.log(f"Error output: {process.stderr[:500]}...", "ERROR")
            
            # Try to find generated results file
            possible_files = [
                "data/analysis/component_mapping_validation.json",
                "data/analysis/shopify_gid_verification.json", 
                "data/analysis/laptop_product_creation_test.json",
                "data/analysis/e2e_integration_test.json"
            ]
            
            for file_path in possible_files:
                if script_name in file_path or any(word in file_path for word in script_name.replace('.py', '').split('_')):
                    full_path = Path(file_path)
                    if full_path.exists():
                        result["results_file"] = str(full_path)
                        
                        # Try to extract key metrics from results file
                        try:
                            with open(full_path, 'r') as f:
                                script_results = json.load(f)
                            
                            # Extract recommendations if available
                            if "recommendations" in script_results:
                                result["recommendations"] = script_results["recommendations"]
                                
                            # Extract score or success metrics
                            if "summary" in script_results:
                                summary = script_results["summary"]
                                if "validation_score" in summary:
                                    result["score"] = summary["validation_score"]
                                elif "success_rate" in summary:
                                    result["score"] = summary["success_rate"]
                                    
                        except Exception as e:
                            self.log(f"Could not parse results file {full_path}: {e}", "WARNING")
                        
                        break
            
        except subprocess.TimeoutExpired:
            result["error"] = "Script execution timed out after 10 minutes"
            result["exit_code"] = -1
            self.log(f"{script_info['name']} timed out", "ERROR")
            
        except Exception as e:
            result["error"] = str(e)
            result["exit_code"] = -1
            self.log(f"{script_info['name']} crashed: {e}", "ERROR")
        
        return result
    
    def consolidate_recommendations(self) -> None:
        """Consolidate recommendations from all scripts."""
        all_recommendations = []
        priority_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        for script_result in self.results["script_results"]:
            for rec in script_result.get("recommendations", []):
                all_recommendations.append({
                    "source_script": script_result["display_name"],
                    "priority": rec.get("priority", "medium"),
                    "category": rec.get("category", "general"),
                    "title": rec.get("title", ""),
                    "description": rec.get("description", ""),
                    "action": rec.get("action", "")
                })
                
                priority = rec.get("priority", "medium")
                if priority in priority_counts:
                    priority_counts[priority] += 1
        
        # Sort by priority (critical -> high -> medium -> low)
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        all_recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        self.results["consolidated_recommendations"] = all_recommendations
        self.results["recommendation_summary"] = priority_counts
    
    def assess_system_readiness(self) -> None:
        """Assess overall system readiness for production."""
        assessment = {
            "component_mapping_ready": False,
            "shopify_integration_ready": False,
            "product_creation_ready": False,
            "workflow_integration_ready": False,
            "overall_readiness_score": 0.0,
            "production_blockers": [],
            "minor_issues": [],
            "recommendations_by_priority": {}
        }
        
        # Analyze script results
        for script_result in self.results["script_results"]:
            script_name = script_result["script_name"]
            
            if "validate_component_mapping" in script_name:
                assessment["component_mapping_ready"] = script_result["success"] and script_result.get("score", 0) >= 80
                if not assessment["component_mapping_ready"]:
                    assessment["production_blockers"].append("Component mapping validation failed or score too low")
                    
            elif "verify_shopify_entries" in script_name:
                assessment["shopify_integration_ready"] = script_result["success"] and script_result.get("score", 0) >= 90
                if not assessment["shopify_integration_ready"]:
                    assessment["production_blockers"].append("Shopify GID verification failed or success rate too low")
                    
            elif "test_laptop_product_creation" in script_name:
                assessment["product_creation_ready"] = script_result["success"] and script_result.get("score", 0) >= 80
                if not assessment["product_creation_ready"]:
                    assessment["production_blockers"].append("Product creation testing failed or success rate too low")
                    
            elif "test_e2e_integration" in script_name:
                assessment["workflow_integration_ready"] = script_result["success"] and script_result.get("score", 0) >= 75
                if not assessment["workflow_integration_ready"]:
                    assessment["minor_issues"].append("E2E integration tests have issues")
        
        # Calculate overall readiness score
        critical_systems = [
            assessment["component_mapping_ready"],
            assessment["shopify_integration_ready"], 
            assessment["product_creation_ready"]
        ]
        
        workflow_weight = 0.7 if assessment["workflow_integration_ready"] else 0.3
        critical_weight = sum(critical_systems) / len(critical_systems)
        
        assessment["overall_readiness_score"] = (critical_weight * 0.8 + workflow_weight * 0.2) * 100
        
        # Group recommendations by priority
        for rec in self.results["consolidated_recommendations"]:
            priority = rec["priority"]
            if priority not in assessment["recommendations_by_priority"]:
                assessment["recommendations_by_priority"][priority] = []
            assessment["recommendations_by_priority"][priority].append(rec)
        
        self.results["system_assessment"] = assessment
        
        # Update summary
        self.results["summary"]["production_ready"] = (
            len(assessment["production_blockers"]) == 0 and 
            assessment["overall_readiness_score"] >= 80
        )
        self.results["summary"]["critical_issues"] = len(assessment["production_blockers"])
        self.results["summary"]["overall_score"] = assessment["overall_readiness_score"]
    
    def generate_summary_report(self, output_dir: str = "data/analysis") -> str:
        """
        Generate comprehensive summary report.
        
        Args:
            output_dir: Directory to save report
            
        Returns:
            str: Path to saved markdown report
        """
        os.makedirs(output_dir, exist_ok=True)
        
        metadata = self.results["metadata"]
        summary = self.results["summary"]
        assessment = self.results["system_assessment"]
        
        report_lines = [
            "# Phase 3: Comprehensive Testing & Validation Report",
            f"**Generated**: {metadata['timestamp']}",
            f"**Script Version**: {metadata['script_version']}",
            f"**Overall Score**: {summary['overall_score']:.1f}/100",
            f"**Production Ready**: {'✅ YES' if summary['production_ready'] else '❌ NO'}",
            "",
            "## Executive Summary",
            "",
            f"- **Total Validation Scripts**: {metadata['total_validation_scripts']}",
            f"- **Scripts Passed**: {summary['scripts_passed']}/{metadata['total_validation_scripts']}",
            f"- **Scripts Failed**: {summary['scripts_failed']}",
            f"- **Critical Issues**: {summary['critical_issues']}",
            f"- **Overall Readiness Score**: {assessment['overall_readiness_score']:.1f}%",
            ""
        ]
        
        # System Readiness Assessment
        report_lines.extend([
            "## System Readiness Assessment",
            "",
            f"- **Component Mapping**: {'✅ Ready' if assessment['component_mapping_ready'] else '❌ Not Ready'}",
            f"- **Shopify Integration**: {'✅ Ready' if assessment['shopify_integration_ready'] else '❌ Not Ready'}",
            f"- **Product Creation**: {'✅ Ready' if assessment['product_creation_ready'] else '❌ Not Ready'}",
            f"- **Workflow Integration**: {'✅ Ready' if assessment['workflow_integration_ready'] else '⚠️ Issues'}",
            ""
        ])
        
        # Production Blockers
        if assessment["production_blockers"]:
            report_lines.extend([
                "## 🔴 Production Blockers",
                "",
                "These critical issues must be resolved before production deployment:",
                ""
            ])
            for blocker in assessment["production_blockers"]:
                report_lines.append(f"- {blocker}")
            report_lines.append("")
        
        # Script Results
        report_lines.extend([
            "## Validation Script Results",
            ""
        ])
        
        for script_result in self.results["script_results"]:
            status_emoji = "✅" if script_result["success"] else "❌"
            critical_badge = " 🔴 CRITICAL" if script_result["critical"] else ""
            
            report_lines.extend([
                f"### {status_emoji} {script_result['display_name']}{critical_badge}",
                f"**Description**: {script_result['description']}",
                f"**Success**: {script_result['success']}",
                f"**Execution Time**: {script_result['execution_time']:.2f}s",
                ""
            ])
            
            if "score" in script_result:
                report_lines.append(f"**Score**: {script_result['score']:.1f}%")
                report_lines.append("")
            
            if script_result["results_file"]:
                report_lines.append(f"**Results File**: `{script_result['results_file']}`")
                report_lines.append("")
            
            if not script_result["success"] and script_result["error"]:
                report_lines.extend([
                    "**Error**:",
                    f"```",
                    script_result["error"][:500] + ("..." if len(script_result["error"]) > 500 else ""),
                    f"```",
                    ""
                ])
        
        # Consolidated Recommendations
        if self.results["consolidated_recommendations"]:
            report_lines.extend([
                "## Recommendations",
                ""
            ])
            
            for priority in ["critical", "high", "medium", "low"]:
                priority_recs = [r for r in self.results["consolidated_recommendations"] if r["priority"] == priority]
                if not priority_recs:
                    continue
                    
                priority_emoji = {"critical": "🔴", "high": "🟡", "medium": "🟠", "low": "🟢"}[priority]
                report_lines.extend([
                    f"### {priority_emoji} {priority.title()} Priority ({len(priority_recs)} items)",
                    ""
                ])
                
                for rec in priority_recs:
                    report_lines.extend([
                        f"#### {rec['title']}",
                        f"**Source**: {rec['source_script']}",
                        f"**Category**: {rec['category'].replace('_', ' ').title()}",
                        f"**Description**: {rec['description']}",
                        f"**Action**: {rec['action']}",
                        ""
                    ])
        
        # Next Steps
        report_lines.extend([
            "## Next Steps",
            ""
        ])
        
        if summary["production_ready"]:
            report_lines.extend([
                "🎉 **System is ready for production deployment!**",
                "",
                "1. ✅ All critical validation tests passed",
                "2. ✅ Component mappings are complete and valid",
                "3. ✅ Shopify integration is working correctly",
                "4. ✅ Product creation workflow is functional",
                "",
                "**Recommended Actions**:",
                "- Deploy to production environment",
                "- Schedule regular validation runs (weekly)",
                "- Monitor system performance in production",
                "- Address any low-priority recommendations as time permits",
                ""
            ])
        else:
            report_lines.extend([
                "⚠️ **System is NOT ready for production deployment**",
                "",
                "**Critical Issues to Address**:",
                ""
            ])
            
            for blocker in assessment["production_blockers"]:
                report_lines.append(f"1. {blocker}")
            
            report_lines.extend([
                "",
                "**Recommended Actions**:",
                "1. Address all production blockers listed above",
                "2. Re-run Phase 3 validation after fixes",
                "3. Ensure all critical tests pass with high scores",
                "4. Review and implement high-priority recommendations",
                ""
            ])
        
        report_lines.extend([
            "## Files Generated",
            "",
            "This validation run generated the following files:",
            ""
        ])
        
        for script_result in self.results["script_results"]:
            if script_result["results_file"]:
                report_lines.append(f"- **{script_result['display_name']}**: `{script_result['results_file']}`")
        
        report_lines.extend([
            f"- **Phase 3 Summary**: `{output_dir}/phase3_validation_summary.json`",
            f"- **This Report**: `{output_dir}/phase3_comprehensive_validation_report.md`",
            ""
        ])
        
        report_lines.extend([
            "---",
            "",
            "*This report was generated by the Phase 3 Comprehensive Validation orchestrator.*",
            "*For questions or issues, refer to the project documentation.*"
        ])
        
        # Save markdown report
        md_file = os.path.join(output_dir, "phase3_comprehensive_validation_report.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        return md_file
    
    def save_summary(self, output_dir: str = "data/analysis") -> str:
        """
        Save validation summary to JSON file.
        
        Args:
            output_dir: Directory to save summary
            
        Returns:
            str: Path to saved file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        json_file = os.path.join(output_dir, "phase3_validation_summary.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
        
        return json_file
    
    def run_validation(self) -> Dict[str, Any]:
        """
        Run complete Phase 3 validation.
        
        Returns:
            dict: Complete validation results
        """
        start_time = time.time()
        
        print("🧪 Starting Phase 3: Comprehensive Testing & Validation")
        print("=" * 70)
        print(f"   Running {len(self.validation_scripts)} validation scripts...")
        print()
        
        # Run each validation script
        for i, script_info in enumerate(self.validation_scripts, 1):
            print(f"📋 Script {i}/{len(self.validation_scripts)}: {script_info['name']}")
            print(f"   Description: {script_info['description']}")
            
            # Check dependencies
            missing_deps = []
            for dep in script_info.get("dependencies", []):
                dep_passed = any(
                    r["script_name"] == dep and r["success"] 
                    for r in self.results["script_results"]
                )
                if not dep_passed:
                    missing_deps.append(dep)
            
            if missing_deps:
                self.log(f"Skipping {script_info['name']} due to failed dependencies: {missing_deps}", "WARNING")
                result = {
                    "script_name": script_info["script"],
                    "display_name": script_info["name"],
                    "description": script_info["description"],
                    "critical": script_info["critical"],
                    "success": False,
                    "exit_code": -2,
                    "execution_time": 0.0,
                    "error": f"Dependencies failed: {missing_deps}",
                    "results_file": None,
                    "recommendations": []
                }
                self.results["script_results"].append(result)
                self.results["summary"]["scripts_failed"] += 1
                continue
            
            # Run the script
            result = self.run_validation_script(script_info)
            self.results["script_results"].append(result)
            
            # Update counters
            if result["success"]:
                self.results["summary"]["scripts_passed"] += 1
            else:
                self.results["summary"]["scripts_failed"] += 1
                
            print()  # Blank line between scripts
        
        # Consolidate recommendations
        self.log("Consolidating recommendations from all scripts...")
        self.consolidate_recommendations()
        
        # Assess system readiness
        self.log("Assessing overall system readiness...")
        self.assess_system_readiness()
        
        # Generate reports
        self.log("Generating comprehensive reports...")
        json_file = self.save_summary()
        md_file = self.generate_summary_report()
        
        # Update final results
        self.results["summary"]["overall_success"] = self.results["summary"]["production_ready"]
        self.results["metadata"]["total_processing_time"] = time.time() - start_time
        
        # Final summary
        summary = self.results["summary"]
        assessment = self.results["system_assessment"]
        
        print("=" * 70)
        print(f"✅ Phase 3 Validation Complete!")
        print(f"   Overall Score: {summary['overall_score']:.1f}/100")
        print(f"   Scripts Passed: {summary['scripts_passed']}/{len(self.validation_scripts)}")
        print(f"   Production Ready: {'✅ YES' if summary['production_ready'] else '❌ NO'}")
        
        if summary["critical_issues"] > 0:
            print(f"   🔴 Critical Issues: {summary['critical_issues']}")
        
        print()
        print(f"📄 Summary Report: {md_file}")
        print(f"📊 JSON Results: {json_file}")
        
        return self.results

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Run Phase 3 comprehensive validation of laptop component mapping system"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="data/analysis",
        help="Output directory for reports (default: data/analysis)"
    )
    
    args = parser.parse_args()
    
    try:
        orchestrator = Phase3ValidationOrchestrator(verbose=args.verbose)
        results = orchestrator.run_validation()
        
        # Exit with appropriate code
        if results["summary"]["production_ready"]:
            print("\n🎉 System is production ready!")
            sys.exit(0)
        elif results["summary"]["critical_issues"] > 0:
            print("\n💥 Critical issues prevent production deployment")
            sys.exit(2)
        elif results["summary"]["scripts_failed"] > 0:
            print("\n⚠️ Some validation tests failed")
            sys.exit(1)
        else:
            print("\n✅ All validation tests passed")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Validation orchestrator failed: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()