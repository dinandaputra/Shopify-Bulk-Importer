#!/usr/bin/env python3
"""
Complete Phase 2 Workflow Runner for Laptop Component Mapping Plan

This master script runs the complete Phase 2 workflow for GID Resolution & Mapping Updates.
It orchestrates all the individual scripts to provide a seamless end-to-end experience.

Workflow:
1. Run GID resolution for unmapped components
2. Update mapping files with resolved GIDs  
3. Generate missing Shopify entries report
4. Provide comprehensive summary and next steps

Author: Shopify API Developer (Claude Code Sub-Agent System)
Version: 1.0.0
Date: 2025-08-06
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scripts/metaobjects/phase2_complete.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_script(script_path: str, script_name: str) -> tuple[bool, int]:
    """
    Run a Python script and return success status and exit code
    
    Args:
        script_path: Path to the script to run
        script_name: Display name for logging
        
    Returns:
        Tuple of (success: bool, exit_code: int)
    """
    logger.info(f"Running {script_name}...")
    logger.info(f"Script: {script_path}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.stdout:
            logger.info(f"{script_name} output:\n{result.stdout}")
        
        if result.stderr:
            logger.warning(f"{script_name} errors:\n{result.stderr}")
        
        if result.returncode == 0:
            logger.info(f"✓ {script_name} completed successfully")
            return True, result.returncode
        else:
            logger.error(f"✗ {script_name} failed with exit code: {result.returncode}")
            return False, result.returncode
            
    except subprocess.TimeoutExpired:
        logger.error(f"✗ {script_name} timed out after 5 minutes")
        return False, -1
    except Exception as e:
        logger.error(f"✗ Error running {script_name}: {e}")
        return False, -2

def check_prerequisites() -> bool:
    """
    Check if all prerequisites are met for Phase 2
    
    Returns:
        True if all prerequisites are met, False otherwise
    """
    logger.info("Checking prerequisites...")
    
    # Check if Phase 1 output exists
    phase1_file = Path("data/analysis/unmapped_components.json")
    if not phase1_file.exists():
        logger.error(f"Phase 1 output file not found: {phase1_file}")
        logger.error("Please run Phase 1 analysis first: python scripts/analysis/analyze_laptop_components.py")
        return False
    
    # Check if required directories exist
    required_dirs = [
        Path("data/metaobjects"),
        Path("scripts/metaobjects")
    ]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            logger.error(f"Required directory not found: {dir_path}")
            return False
    
    # Check if required scripts exist
    required_scripts = [
        Path("scripts/metaobjects/resolve_missing_gids.py"),
        Path("scripts/metaobjects/batch_update_mappings.py"),
        Path("scripts/metaobjects/generate_missing_report.py")
    ]
    
    for script_path in required_scripts:
        if not script_path.exists():
            logger.error(f"Required script not found: {script_path}")
            return False
    
    logger.info("✓ All prerequisites met")
    return True

def generate_summary_report() -> None:
    """
    Generate a comprehensive summary report of Phase 2 results
    """
    logger.info("Generating Phase 2 summary report...")
    
    try:
        # Read results from individual scripts
        import json
        
        # GID resolution results
        gid_results_file = Path("data/analysis/gid_resolution_results.json")
        if gid_results_file.exists():
            with open(gid_results_file, 'r', encoding='utf-8') as f:
                gid_results = json.load(f)
        else:
            gid_results = {}
        
        # Generate summary report
        summary_report = []
        summary_report.append("# Phase 2 Complete Workflow Summary Report\n\n")
        summary_report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        summary_report.append(f"**Workflow Version**: 1.0.0\n\n")
        
        summary_report.append("## Phase 2: GID Resolution & Mapping Updates - COMPLETE\n\n")
        
        if gid_results.get('metadata'):
            metadata = gid_results['metadata']
            summary_report.append("### GID Resolution Results\n\n")
            summary_report.append(f"- **Total Components Processed**: {metadata.get('total_components_processed', 0)}\n")
            summary_report.append(f"- **Components Found**: {metadata.get('components_found', 0)}\n")
            summary_report.append(f"- **Components Not Found**: {metadata.get('components_not_found', 0)}\n")
            summary_report.append(f"- **Success Rate**: {metadata.get('success_rate_percent', 0):.1f}%\n")
            summary_report.append(f"- **Processing Time**: {metadata.get('processing_time_seconds', 0):.2f} seconds\n")
            summary_report.append(f"- **API Calls Made**: {metadata.get('api_calls_made', 0)}\n\n")
        
        # Component type breakdown
        if gid_results.get('summary_by_type'):
            summary_report.append("### Component Type Breakdown\n\n")
            summary_report.append("| Component Type | Total | Found | Success Rate |\n")
            summary_report.append("|---------------|--------|-------|---------------|\n")
            
            for component_type, stats in gid_results['summary_by_type'].items():
                total = stats.get('total', 0)
                found = stats.get('found', 0)
                success_rate = stats.get('success_rate', 0)
                summary_report.append(f"| {component_type.title()} | {total} | {found} | {success_rate:.1f}% |\n")
            
            summary_report.append("\n")
        
        # Files generated
        summary_report.append("### Files Generated\n\n")
        
        generated_files = [
            ("data/analysis/gid_resolution_results.json", "Complete GID resolution results"),
            ("data/analysis/missing_shopify_entries.md", "Missing components report"),
            ("data/analysis/mapping_update_report.md", "Mapping update summary"),
            ("scripts/metaobjects/gid_resolution.log", "GID resolution process log"),
            ("scripts/metaobjects/batch_update_mappings.log", "Mapping update process log"),
            ("scripts/metaobjects/phase2_complete.log", "Complete workflow log")
        ]
        
        for file_path, description in generated_files:
            path = Path(file_path)
            if path.exists():
                size = path.stat().st_size / 1024
                summary_report.append(f"- **{path.name}**: {description} ({size:.1f} KB)\n")
        
        summary_report.append("\n")
        
        # Next steps
        summary_report.append("## Next Steps\n\n")
        summary_report.append("### Immediate Actions\n\n")
        summary_report.append("1. **Review Missing Components Report**: Check `data/analysis/missing_shopify_entries.md`\n")
        summary_report.append("2. **Create Missing Metaobjects**: Use Shopify Admin to create missing metaobjects\n")
        summary_report.append("3. **Re-run GID Resolution**: After creating metaobjects, run Phase 2 again to resolve more components\n")
        summary_report.append("4. **Test Laptop Product Creation**: Validate updated mappings work correctly\n\n")
        
        summary_report.append("### Phase 3 Preparation\n\n")
        summary_report.append("1. **Comprehensive Testing**: Validate all mapping updates\n")
        summary_report.append("2. **Product Creation Testing**: Test laptop product creation with new mappings\n")
        summary_report.append("3. **End-to-End Validation**: Complete workflow testing\n")
        summary_report.append("4. **Documentation Updates**: Update project documentation\n\n")
        
        # Performance insights
        summary_report.append("## Performance Insights\n\n")
        if gid_results.get('metadata'):
            api_calls = metadata.get('api_calls_made', 0)
            processing_time = metadata.get('processing_time_seconds', 0)
            if processing_time > 0:
                avg_call_time = processing_time / api_calls if api_calls > 0 else 0
                summary_report.append(f"- **Average API Call Time**: {avg_call_time:.2f} seconds\n")
                summary_report.append(f"- **Components per Second**: {metadata.get('total_components_processed', 0) / processing_time:.2f}\n")
        
        summary_report.append("\n---\n\n")
        summary_report.append("*This summary was generated automatically by the Phase 2 complete workflow runner.*\n")
        
        # Save summary report
        summary_file = Path("data/analysis/phase2_complete_summary.md")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(''.join(summary_report))
        
        logger.info(f"Phase 2 summary report generated: {summary_file}")
        
    except Exception as e:
        logger.error(f"Failed to generate summary report: {e}")

def main():
    """
    Main function to run the complete Phase 2 workflow
    """
    start_time = datetime.now()
    
    logger.info("=" * 80)
    logger.info("LAPTOP COMPONENT MAPPING PLAN - PHASE 2 COMPLETE WORKFLOW")
    logger.info("=" * 80)
    logger.info(f"Workflow started at: {start_time.isoformat()}")
    
    # Check prerequisites
    if not check_prerequisites():
        logger.error("Prerequisites not met - aborting Phase 2 workflow")
        return 1
    
    # Phase 2 workflow steps
    workflow_steps = [
        ("scripts/metaobjects/resolve_missing_gids.py", "GID Resolution"),
        ("scripts/metaobjects/batch_update_mappings.py", "Mapping Updates"), 
        ("scripts/metaobjects/generate_missing_report.py", "Missing Components Report")
    ]
    
    # Execute workflow steps
    total_steps = len(workflow_steps)
    completed_steps = 0
    
    for step_num, (script_path, step_name) in enumerate(workflow_steps, 1):
        logger.info(f"\n{'=' * 60}")
        logger.info(f"PHASE 2 STEP {step_num}/{total_steps}: {step_name.upper()}")
        logger.info(f"{'=' * 60}")
        
        success, exit_code = run_script(script_path, step_name)
        
        if success:
            completed_steps += 1
            logger.info(f"✓ Step {step_num} completed successfully")
        else:
            logger.error(f"✗ Step {step_num} failed - aborting workflow")
            logger.error(f"Check logs for detailed error information")
            return exit_code
        
        # Brief pause between steps
        if step_num < total_steps:
            logger.info("Proceeding to next step...")
    
    # Generate summary report
    logger.info(f"\n{'=' * 60}")
    logger.info("GENERATING PHASE 2 SUMMARY REPORT")
    logger.info(f"{'=' * 60}")
    
    generate_summary_report()
    
    # Final summary
    end_time = datetime.now()
    total_time = end_time - start_time
    
    logger.info(f"\n{'=' * 80}")
    logger.info("PHASE 2 COMPLETE WORKFLOW FINISHED!")
    logger.info(f"{'=' * 80}")
    logger.info(f"Workflow completed at: {end_time.isoformat()}")
    logger.info(f"Total processing time: {total_time.total_seconds():.2f} seconds")
    logger.info(f"Steps completed: {completed_steps}/{total_steps}")
    
    if completed_steps == total_steps:
        logger.info("✓ Phase 2 workflow completed successfully!")
        logger.info("\nGenerated Reports:")
        logger.info("- data/analysis/gid_resolution_results.json")
        logger.info("- data/analysis/missing_shopify_entries.md") 
        logger.info("- data/analysis/mapping_update_report.md")
        logger.info("- data/analysis/phase2_complete_summary.md")
        logger.info("\nNext: Review missing components report and create metaobjects in Shopify Admin")
        return 0
    else:
        logger.error("✗ Phase 2 workflow failed!")
        logger.error("Check individual step logs for detailed error information")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)