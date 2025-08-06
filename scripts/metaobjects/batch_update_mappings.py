#!/usr/bin/env python3
"""
Batch Update Mappings Script for Laptop Component Mapping Plan Phase 2

This script automatically updates JSON metaobject mapping files with resolved GIDs
from the GID resolution process. It includes comprehensive backup systems and 
validation to ensure data integrity.

Author: Shopify API Developer (Claude Code Sub-Agent System)  
Version: 1.0.0
Date: 2025-08-06
"""

import json
import os
import sys
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scripts/metaobjects/batch_update_mappings.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MappingUpdater:
    """
    Main class for batch updating metaobject mapping JSON files
    """
    
    def __init__(self):
        """Initialize the mapping updater with file paths and configuration"""
        self.metaobject_dir = Path("data/metaobjects")
        self.backup_dir = Path("data/metaobjects/backups")
        self.results_file = Path("data/analysis/gid_resolution_results.json")
        
        # Mapping file configurations
        self.mapping_files = {
            'processors': 'processors.json',
            'vga': 'vga.json', 
            'graphics': 'graphics.json',
            'displays': 'displays.json',
            'storage': 'storage.json',
            'os': 'os.json',
            'keyboard_layouts': 'keyboard_layouts.json',
            'keyboard_backlights': 'keyboard_backlights.json'
        }
        
        # Update statistics
        self.update_stats = {
            'files_processed': 0,
            'files_updated': 0,
            'entries_added': 0,
            'files_backed_up': 0,
            'errors': 0,
            'backup_created': None
        }
        
        logger.info("Mapping updater initialized successfully")
    
    def create_backup_directory(self) -> Path:
        """
        Create a timestamped backup directory for all mapping files
        
        Returns:
            Path to the created backup directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"batch_update_{timestamp}"
        
        try:
            backup_path.mkdir(parents=True, exist_ok=True)
            self.update_stats['backup_created'] = backup_path
            logger.info(f"Created backup directory: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create backup directory: {e}")
            raise
    
    def backup_mapping_file(self, file_path: Path, backup_dir: Path) -> bool:
        """
        Create a backup of a single mapping file
        
        Args:
            file_path: Path to the original mapping file
            backup_dir: Directory to store the backup
            
        Returns:
            True if backup was successful, False otherwise
        """
        if not file_path.exists():
            logger.warning(f"Mapping file does not exist, skipping backup: {file_path}")
            return False
        
        try:
            backup_file = backup_dir / file_path.name
            shutil.copy2(file_path, backup_file)
            
            # Verify backup
            if backup_file.exists() and backup_file.stat().st_size == file_path.stat().st_size:
                logger.debug(f"✓ Backed up: {file_path.name}")
                self.update_stats['files_backed_up'] += 1
                return True
            else:
                logger.error(f"✗ Backup verification failed: {file_path.name}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to backup {file_path}: {e}")
            return False
    
    def backup_all_mappings(self, backup_dir: Path) -> bool:
        """
        Create backups of all mapping files before updates
        
        Args:
            backup_dir: Directory to store backups
            
        Returns:
            True if all backups were successful, False otherwise
        """
        logger.info("Creating backups of all mapping files...")
        
        backup_success = True
        
        for component_type, filename in self.mapping_files.items():
            file_path = self.metaobject_dir / filename
            
            if not self.backup_mapping_file(file_path, backup_dir):
                backup_success = False
        
        # Also backup the GID resolution results
        if self.results_file.exists():
            self.backup_mapping_file(self.results_file, backup_dir)
        
        if backup_success:
            logger.info(f"✓ All mapping files backed up successfully to: {backup_dir}")
        else:
            logger.warning("⚠ Some backup operations failed - check logs for details")
        
        return backup_success
    
    def load_gid_resolution_results(self) -> Dict[str, Any]:
        """
        Load the GID resolution results from the resolver script
        
        Returns:
            Dictionary containing resolution results
            
        Raises:
            FileNotFoundError: If results file is not found
            json.JSONDecodeError: If results file contains invalid JSON
        """
        try:
            with open(self.results_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            logger.info(f"Loaded GID resolution results from: {self.results_file}")
            logger.info(f"Components found: {results['metadata']['components_found']}")
            logger.info(f"Components not found: {results['metadata']['components_not_found']}")
            
            return results
            
        except FileNotFoundError:
            logger.error(f"GID resolution results file not found: {self.results_file}")
            logger.error("Please run the GID resolution script first: python scripts/metaobjects/resolve_missing_gids.py")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in results file: {e}")
            raise
    
    def load_existing_mapping(self, file_path: Path) -> Dict[str, str]:
        """
        Load an existing metaobject mapping file
        
        Args:
            file_path: Path to the mapping JSON file
            
        Returns:
            Dictionary containing existing mappings
        """
        try:
            if not file_path.exists():
                logger.info(f"Creating new mapping file: {file_path}")
                return {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            
            logger.debug(f"Loaded existing mapping: {file_path.name} ({len(mapping)} entries)")
            return mapping
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in mapping file {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load mapping file {file_path}: {e}")
            raise
    
    def update_mapping_file(self, component_type: str, resolved_components: Dict[str, Dict]) -> Tuple[bool, int]:
        """
        Update a single mapping file with resolved GIDs
        
        Args:
            component_type: Type of components (e.g., 'processors', 'vga')
            resolved_components: Dictionary of resolved components with GIDs
            
        Returns:
            Tuple of (success: bool, entries_added: int)
        """
        if component_type not in self.mapping_files:
            logger.error(f"Unknown component type: {component_type}")
            return False, 0
        
        filename = self.mapping_files[component_type]
        file_path = self.metaobject_dir / filename
        
        try:
            # Load existing mapping
            existing_mapping = self.load_existing_mapping(file_path)
            original_count = len(existing_mapping)
            
            # Add new resolved components
            entries_added = 0
            for component_name, component_data in resolved_components.items():
                gid = component_data['gid']
                shopify_name = component_data.get('shopify_display_name', component_name)
                
                if component_name not in existing_mapping:
                    existing_mapping[component_name] = gid
                    entries_added += 1
                    logger.info(f"  + Added: {component_name} → {gid}")
                else:
                    logger.debug(f"  = Exists: {component_name}")
            
            # Only write file if changes were made
            if entries_added > 0:
                # Sort mappings alphabetically for consistent output
                sorted_mapping = dict(sorted(existing_mapping.items()))
                
                # Write updated mapping
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(sorted_mapping, f, indent=2, ensure_ascii=False)
                
                new_count = len(sorted_mapping)
                logger.info(f"✓ Updated {filename}: {original_count} → {new_count} entries (+{entries_added})")
                self.update_stats['files_updated'] += 1
                
            else:
                logger.info(f"○ No updates needed for {filename}")
            
            self.update_stats['files_processed'] += 1
            self.update_stats['entries_added'] += entries_added
            
            return True, entries_added
            
        except Exception as e:
            logger.error(f"Failed to update mapping file {filename}: {e}")
            self.update_stats['errors'] += 1
            return False, 0
    
    def validate_updated_mappings(self) -> bool:
        """
        Validate all updated mapping files for JSON format and consistency
        
        Returns:
            True if all files are valid, False otherwise
        """
        logger.info("Validating updated mapping files...")
        
        validation_success = True
        
        for component_type, filename in self.mapping_files.items():
            file_path = self.metaobject_dir / filename
            
            if not file_path.exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    mapping = json.load(f)
                
                # Validate GID format
                invalid_gids = []
                for component_name, gid in mapping.items():
                    if not isinstance(gid, str) or not gid.startswith("gid://shopify/Metaobject/"):
                        invalid_gids.append(f"{component_name}: {gid}")
                
                if invalid_gids:
                    logger.error(f"Invalid GIDs found in {filename}:")
                    for invalid_gid in invalid_gids:
                        logger.error(f"  - {invalid_gid}")
                    validation_success = False
                else:
                    logger.debug(f"✓ Valid: {filename} ({len(mapping)} entries)")
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON validation failed for {filename}: {e}")
                validation_success = False
            except Exception as e:
                logger.error(f"Validation error for {filename}: {e}")
                validation_success = False
        
        if validation_success:
            logger.info("✓ All updated mapping files passed validation")
        else:
            logger.error("✗ Some mapping files failed validation - check logs for details")
        
        return validation_success
    
    def rollback_updates(self, backup_dir: Path) -> bool:
        """
        Rollback all updates by restoring from backup
        
        Args:
            backup_dir: Directory containing backup files
            
        Returns:
            True if rollback was successful, False otherwise
        """
        logger.warning("Rolling back all updates from backup...")
        
        rollback_success = True
        
        for component_type, filename in self.mapping_files.items():
            backup_file = backup_dir / filename
            target_file = self.metaobject_dir / filename
            
            if backup_file.exists():
                try:
                    shutil.copy2(backup_file, target_file)
                    logger.info(f"✓ Restored: {filename}")
                except Exception as e:
                    logger.error(f"Failed to restore {filename}: {e}")
                    rollback_success = False
            else:
                logger.warning(f"No backup found for {filename}")
        
        if rollback_success:
            logger.info("✓ Rollback completed successfully")
        else:
            logger.error("✗ Rollback failed - manual intervention may be required")
        
        return rollback_success
    
    def update_all_mappings(self) -> bool:
        """
        Update all mapping files with resolved GIDs
        
        Returns:
            True if all updates were successful, False otherwise
        """
        logger.info("Starting batch update of all mapping files...")
        
        try:
            # Create backup directory
            backup_dir = self.create_backup_directory()
            
            # Create backups of all mapping files
            if not self.backup_all_mappings(backup_dir):
                logger.error("Backup creation failed - aborting update process")
                return False
            
            # Load GID resolution results
            resolution_results = self.load_gid_resolution_results()
            resolved_components = resolution_results.get('resolved_components', {})
            
            if not resolved_components:
                logger.warning("No resolved components found - nothing to update")
                return True
            
            # Update each component type
            update_success = True
            
            for component_type, components in resolved_components.items():
                logger.info(f"\n--- Updating {component_type} mappings ---")
                
                success, entries_added = self.update_mapping_file(component_type, components)
                
                if not success:
                    update_success = False
                    logger.error(f"Failed to update {component_type} mappings")
            
            # Validate all updated files
            if update_success:
                validation_success = self.validate_updated_mappings()
                if not validation_success:
                    logger.error("Validation failed - rolling back updates...")
                    self.rollback_updates(backup_dir)
                    return False
            else:
                logger.error("Some updates failed - rolling back all changes...")
                self.rollback_updates(backup_dir)
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Critical error during batch update: {e}")
            if 'backup_dir' in locals():
                self.rollback_updates(backup_dir)
            return False
    
    def generate_update_report(self) -> None:
        """
        Generate a summary report of the batch update process
        """
        report_file = Path("data/analysis/mapping_update_report.md")
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# Mapping Update Report\n\n")
                f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Script Version**: 1.0.0\n\n")
                
                f.write("## Update Summary\n\n")
                f.write(f"- **Files Processed**: {self.update_stats['files_processed']}\n")
                f.write(f"- **Files Updated**: {self.update_stats['files_updated']}\n")
                f.write(f"- **New Entries Added**: {self.update_stats['entries_added']}\n")
                f.write(f"- **Files Backed Up**: {self.update_stats['files_backed_up']}\n")
                f.write(f"- **Errors**: {self.update_stats['errors']}\n\n")
                
                if self.update_stats['backup_created']:
                    f.write(f"## Backup Location\n\n")
                    f.write(f"All original files backed up to:\n")
                    f.write(f"```\n{self.update_stats['backup_created']}\n```\n\n")
                
                f.write("## Files Updated\n\n")
                for component_type, filename in self.mapping_files.items():
                    file_path = self.metaobject_dir / filename
                    if file_path.exists():
                        try:
                            with open(file_path, 'r', encoding='utf-8') as mapping_file:
                                mapping = json.load(mapping_file)
                            f.write(f"- **{filename}**: {len(mapping)} entries\n")
                        except Exception:
                            f.write(f"- **{filename}**: (read error)\n")
                
                f.write("\n## Next Steps\n\n")
                f.write("1. Review updated mapping files in `data/metaobjects/`\n")
                f.write("2. Test laptop product creation with new mappings\n")
                f.write("3. Generate missing Shopify entries report if needed\n")
                f.write("4. Clean up backup files after validation\n")
            
            logger.info(f"Update report generated: {report_file}")
            
        except Exception as e:
            logger.error(f"Failed to generate update report: {e}")

def main():
    """
    Main function to run the batch mapping update process
    """
    logger.info("="*60)
    logger.info("BATCH MAPPING UPDATE - PHASE 2")
    logger.info("="*60)
    logger.info(f"Script started at: {datetime.now().isoformat()}")
    
    try:
        # Initialize updater
        updater = MappingUpdater()
        
        # Update all mapping files
        success = updater.update_all_mappings()
        
        # Generate report
        updater.generate_update_report()
        
        if success:
            logger.info("\n" + "="*60)
            logger.info("BATCH MAPPING UPDATE COMPLETED SUCCESSFULLY!")
            logger.info("="*60)
            logger.info(f"Files processed: {updater.update_stats['files_processed']}")
            logger.info(f"Files updated: {updater.update_stats['files_updated']}")
            logger.info(f"New entries added: {updater.update_stats['entries_added']}")
            logger.info("Check update report: data/analysis/mapping_update_report.md")
            return 0
        else:
            logger.error("\n" + "="*60)
            logger.error("BATCH MAPPING UPDATE FAILED!")
            logger.error("="*60)
            logger.error("Check logs for detailed error information")
            return 1
            
    except Exception as e:
        logger.error(f"Critical error in batch update process: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)