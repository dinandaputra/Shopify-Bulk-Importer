#!/usr/bin/env python3
"""
GID Resolution Script for Laptop Component Mapping Plan Phase 2

This script queries Shopify metaobjects to resolve missing GIDs for unmapped laptop components.
It follows the patterns established in the project for API usage and error handling.

Author: Shopify API Developer (Claude Code Sub-Agent System)
Version: 1.0.0
Date: 2025-08-06
"""

import json
import time
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.shopify_api import ShopifyAPIClient, ShopifyAPIError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scripts/metaobjects/gid_resolution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ComponentSearchResult:
    """Result of a component search in Shopify"""
    component_name: str
    component_type: str
    gid: Optional[str] = None
    shopify_display_name: Optional[str] = None
    found: bool = False
    search_attempts: List[str] = None
    
    def __post_init__(self):
        if self.search_attempts is None:
            self.search_attempts = []

@dataclass
class ResolutionSummary:
    """Summary of the GID resolution process"""
    total_components: int = 0
    found_components: int = 0
    not_found_components: int = 0
    errors: int = 0
    processing_time: float = 0.0
    results_by_type: Dict[str, Dict] = None
    
    def __post_init__(self):
        if self.results_by_type is None:
            self.results_by_type = {}

class GIDResolver:
    """
    Main class for resolving GIDs for unmapped laptop components
    """
    
    def __init__(self):
        """Initialize the GID resolver with API client and configuration"""
        self.api_client = ShopifyAPIClient()
        self.metaobject_type_mappings = {
            'processors': 'processor',
            'vga': 'vga',
            'graphics': 'graphics',
            'displays': 'display',
            'storage': 'storage',
            'os': 'operating_system',
            'keyboard_layouts': 'keyboard_layout',
            'keyboard_backlights': 'keyboard_backlight'
        }
        
        # Rate limiting settings
        self.api_delay = 0.5  # Seconds between API calls
        self.batch_delay = 2.0  # Seconds between batches
        self.max_retries = 3
        
        # Results tracking
        self.search_results: List[ComponentSearchResult] = []
        self.api_calls_made = 0
        
        logger.info("GID Resolver initialized successfully")
    
    def load_unmapped_components(self, file_path: str = "data/analysis/unmapped_components.json") -> Dict[str, Any]:
        """
        Load the unmapped components data from Phase 1 analysis
        
        Args:
            file_path: Path to the unmapped components JSON file
            
        Returns:
            Dictionary containing unmapped components data
            
        Raises:
            FileNotFoundError: If the unmapped components file is not found
            json.JSONDecodeError: If the file contains invalid JSON
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Loaded unmapped components data from {file_path}")
            logger.info(f"Total unmapped components: {data['metadata']['total_unmapped_components']}")
            
            return data
        except FileNotFoundError:
            logger.error(f"Unmapped components file not found: {file_path}")
            logger.error("Please run Phase 1 analysis first: python scripts/analysis/analyze_laptop_components.py")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in unmapped components file: {e}")
            raise
    
    def query_metaobjects_by_type(self, metaobject_type: str, limit: int = 250) -> List[Dict[str, Any]]:
        """
        Query Shopify for all metaobjects of a specific type using GraphQL
        
        Args:
            metaobject_type: The type of metaobjects to query (e.g., 'processor', 'vga')
            limit: Maximum number of results to return
            
        Returns:
            List of metaobject dictionaries with id, handle, displayName, and fields
            
        Raises:
            ShopifyAPIError: If the GraphQL query fails
        """
        query = """
        query getMetaobjectsByType($type: String!, $first: Int!) {
            metaobjects(type: $type, first: $first) {
                edges {
                    node {
                        id
                        handle
                        displayName
                        fields {
                            key
                            value
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        """
        
        variables = {
            "type": metaobject_type,
            "first": limit
        }
        
        try:
            # Add API call tracking and rate limiting
            self.api_calls_made += 1
            time.sleep(self.api_delay)
            
            logger.info(f"Querying Shopify for metaobjects of type: {metaobject_type}")
            result = self.api_client._make_graphql_request(query, variables)
            
            # Extract metaobjects from GraphQL response
            edges = result.get("data", {}).get("metaobjects", {}).get("edges", [])
            metaobjects = [edge["node"] for edge in edges]
            
            logger.info(f"Found {len(metaobjects)} metaobjects of type {metaobject_type}")
            return metaobjects
            
        except Exception as e:
            logger.error(f"Failed to query metaobjects of type {metaobject_type}: {e}")
            raise ShopifyAPIError(f"Could not query metaobjects: {e}") from e
    
    def search_component_in_metaobjects(self, component_name: str, metaobjects: List[Dict], component_type: str) -> ComponentSearchResult:
        """
        Search for a specific component in a list of metaobjects
        
        Args:
            component_name: Name of the component to search for
            metaobjects: List of metaobject dictionaries from Shopify
            component_type: Type of component (for logging)
            
        Returns:
            ComponentSearchResult with search results and GID if found
        """
        result = ComponentSearchResult(
            component_name=component_name,
            component_type=component_type
        )
        
        # Generate search variations
        search_variations = self._generate_search_variations(component_name)
        result.search_attempts = search_variations
        
        logger.debug(f"Searching for {component_name} with {len(search_variations)} variations")
        
        # Search through metaobjects
        for metaobject in metaobjects:
            display_name = metaobject.get("displayName", "")
            
            # Try exact match first
            if display_name == component_name:
                result.gid = metaobject["id"]
                result.shopify_display_name = display_name
                result.found = True
                logger.info(f"✓ EXACT MATCH: {component_name} → {result.gid}")
                break
            
            # Try partial matches with variations
            for variation in search_variations:
                if self._is_component_match(variation.lower(), display_name.lower()):
                    result.gid = metaobject["id"]
                    result.shopify_display_name = display_name
                    result.found = True
                    logger.info(f"✓ VARIATION MATCH: {component_name} → {display_name} → {result.gid}")
                    break
            
            if result.found:
                break
        
        if not result.found:
            logger.warning(f"✗ NOT FOUND: {component_name} (tried {len(search_variations)} variations)")
        
        return result
    
    def _generate_search_variations(self, component_name: str) -> List[str]:
        """
        Generate search variations for a component name to improve matching
        
        Args:
            component_name: Original component name
            
        Returns:
            List of search variations to try
        """
        variations = [component_name]
        
        # For processors - handle different CPU name formats
        if "CPU" in component_name or "Core" in component_name or "Ryzen" in component_name:
            # Remove frequency info: "(16 CPUs), ~2.3GHz" → ""
            clean_name = component_name.split(" (")[0] if " (" in component_name else component_name
            variations.append(clean_name)
            
            # Add frequency variations
            if "~" in component_name:
                freq_part = component_name.split("~")[1].split("GHz")[0] if "~" in component_name else ""
                if freq_part:
                    freq_variations = [f"{clean_name} @ {freq_part.strip()}GHz", f"{clean_name} {freq_part.strip()}GHz"]
                    variations.extend(freq_variations)
        
        # For graphics cards - handle abbreviated names
        if "RTX" in component_name or "GTX" in component_name:
            # Handle abbreviated forms: "RTX 3050 Ti" → "NVIDIA GeForce RTX 3050 Ti 4GB"
            if not component_name.startswith("NVIDIA"):
                variations.append(f"NVIDIA GeForce {component_name}")
                variations.append(f"NVIDIA {component_name}")
            
            # Add memory size variations for incomplete names
            if "GB" not in component_name:
                for memory in ["4GB", "6GB", "8GB", "12GB", "16GB"]:
                    variations.append(f"{component_name} {memory}")
                    if not component_name.startswith("NVIDIA"):
                        variations.append(f"NVIDIA GeForce {component_name} {memory}")
        
        # For displays - handle different formats
        if "inch" in component_name or "Hz" in component_name:
            # Normalize display formats
            if "FHD" in component_name:
                variations.append(component_name.replace("FHD", "Full HD"))
                variations.append(component_name.replace("FHD", "1080p"))
            if "QHD" in component_name:
                variations.append(component_name.replace("QHD", "2K"))
                variations.append(component_name.replace("QHD", "1440p"))
            if "4K UHD" in component_name:
                variations.append(component_name.replace("4K UHD", "4K"))
                variations.append(component_name.replace("4K UHD", "Ultra HD"))
        
        # For storage - handle different formats
        if "SSD" in component_name or "HDD" in component_name:
            variations.append(component_name.replace("SSD", "Solid State Drive"))
            variations.append(component_name.replace("HDD", "Hard Drive"))
        
        # Remove duplicates and empty strings
        variations = list(set([v for v in variations if v.strip()]))
        
        return variations
    
    def _is_component_match(self, search_term: str, metaobject_name: str) -> bool:
        """
        Determine if a search term matches a metaobject name
        
        Args:
            search_term: Search term (lowercase)
            metaobject_name: Metaobject display name (lowercase)
            
        Returns:
            True if the terms match, False otherwise
        """
        # Exact match
        if search_term == metaobject_name:
            return True
        
        # Contains match for longer names
        if len(search_term) > 10 and search_term in metaobject_name:
            return True
        
        # For processors - match key components
        if any(cpu in search_term for cpu in ["intel core", "amd ryzen"]):
            # Extract key parts for CPU matching
            search_parts = search_term.replace("(", "").replace(")", "").split()
            metaobject_parts = metaobject_name.replace("(", "").replace(")", "").split()
            
            # Look for matching model numbers and generation
            for part in search_parts:
                if part.startswith("i") and part[1:].isdigit():  # Intel Core i7, i9, etc.
                    if part in metaobject_parts:
                        # Check if processor generation matches
                        for search_part in search_parts:
                            if "-" in search_part and search_part in metaobject_parts:
                                return True
                
                if "ryzen" in search_term and part.isdigit() and len(part) == 1:  # Ryzen 5, 7, 9
                    if part in metaobject_parts and "ryzen" in metaobject_name:
                        return True
        
        return False
    
    def resolve_components_for_type(self, component_type: str, components: List[str]) -> List[ComponentSearchResult]:
        """
        Resolve GIDs for all components of a specific type
        
        Args:
            component_type: Type of components (e.g., 'processors', 'vga')
            components: List of component names to resolve
            
        Returns:
            List of ComponentSearchResult objects
        """
        results = []
        
        if not components:
            logger.info(f"No unmapped components found for type: {component_type}")
            return results
        
        logger.info(f"\n=== Resolving {len(components)} {component_type} components ===")
        
        # Get the Shopify metaobject type
        shopify_type = self.metaobject_type_mappings.get(component_type)
        if not shopify_type:
            logger.error(f"Unknown component type: {component_type}")
            return results
        
        try:
            # Query Shopify for all metaobjects of this type
            metaobjects = self.query_metaobjects_by_type(shopify_type)
            
            if not metaobjects:
                logger.warning(f"No metaobjects found in Shopify for type: {shopify_type}")
                return results
            
            # Search for each component
            for component_name in components:
                try:
                    result = self.search_component_in_metaobjects(component_name, metaobjects, component_type)
                    results.append(result)
                    
                    # Small delay between searches
                    time.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Error searching for component {component_name}: {e}")
                    error_result = ComponentSearchResult(
                        component_name=component_name,
                        component_type=component_type,
                        found=False
                    )
                    results.append(error_result)
            
            logger.info(f"Completed {component_type}: {sum(1 for r in results if r.found)}/{len(results)} found")
            
        except Exception as e:
            logger.error(f"Failed to resolve {component_type} components: {e}")
            # Create error results for all components
            for component_name in components:
                error_result = ComponentSearchResult(
                    component_name=component_name,
                    component_type=component_type,
                    found=False
                )
                results.append(error_result)
        
        return results
    
    def resolve_all_unmapped_components(self, unmapped_data: Dict[str, Any]) -> ResolutionSummary:
        """
        Resolve GIDs for all unmapped components across all types
        
        Args:
            unmapped_data: Dictionary containing unmapped components data
            
        Returns:
            ResolutionSummary with complete results
        """
        start_time = time.time()
        summary = ResolutionSummary()
        
        logger.info("Starting GID resolution for all unmapped components...")
        logger.info(f"Total unmapped components: {unmapped_data['metadata']['total_unmapped_components']}")
        
        unmapped_components = unmapped_data.get("unmapped_components", {})
        
        # Process each component type
        for component_type, components in unmapped_components.items():
            if not components:
                continue
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing {component_type.upper()}")
            logger.info(f"{'='*60}")
            
            # Resolve components for this type
            type_results = self.resolve_components_for_type(component_type, components)
            self.search_results.extend(type_results)
            
            # Update summary
            found_count = sum(1 for r in type_results if r.found)
            not_found_count = len(type_results) - found_count
            
            summary.results_by_type[component_type] = {
                "total": len(components),
                "found": found_count,
                "not_found": not_found_count,
                "success_rate": (found_count / len(components) * 100) if components else 0
            }
            
            summary.total_components += len(components)
            summary.found_components += found_count
            summary.not_found_components += not_found_count
            
            # Add delay between component types to respect rate limits
            if component_type != list(unmapped_components.keys())[-1]:  # Not the last type
                logger.info(f"Waiting {self.batch_delay}s before processing next type...")
                time.sleep(self.batch_delay)
        
        summary.processing_time = time.time() - start_time
        
        logger.info(f"\n{'='*60}")
        logger.info("GID RESOLUTION COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Total components processed: {summary.total_components}")
        logger.info(f"Successfully resolved: {summary.found_components}")
        logger.info(f"Not found in Shopify: {summary.not_found_components}")
        logger.info(f"Success rate: {(summary.found_components / summary.total_components * 100):.1f}%")
        logger.info(f"Processing time: {summary.processing_time:.2f} seconds")
        logger.info(f"API calls made: {self.api_calls_made}")
        
        return summary
    
    def save_results(self, summary: ResolutionSummary, output_file: str = "data/analysis/gid_resolution_results.json") -> None:
        """
        Save the GID resolution results to a JSON file
        
        Args:
            summary: ResolutionSummary object with complete results
            output_file: Path to output JSON file
        """
        # Prepare results data
        results_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "script_version": "1.0.0",
                "total_components_processed": summary.total_components,
                "components_found": summary.found_components,
                "components_not_found": summary.not_found_components,
                "success_rate_percent": round((summary.found_components / summary.total_components * 100), 2) if summary.total_components > 0 else 0,
                "processing_time_seconds": round(summary.processing_time, 2),
                "api_calls_made": self.api_calls_made
            },
            "summary_by_type": summary.results_by_type,
            "resolved_components": {},
            "not_found_components": {},
            "search_details": []
        }
        
        # Organize results by type
        for result in self.search_results:
            component_type = result.component_type
            
            if result.found:
                if component_type not in results_data["resolved_components"]:
                    results_data["resolved_components"][component_type] = {}
                
                results_data["resolved_components"][component_type][result.component_name] = {
                    "gid": result.gid,
                    "shopify_display_name": result.shopify_display_name
                }
            else:
                if component_type not in results_data["not_found_components"]:
                    results_data["not_found_components"][component_type] = []
                
                results_data["not_found_components"][component_type].append(result.component_name)
            
            # Add search details
            results_data["search_details"].append({
                "component_name": result.component_name,
                "component_type": result.component_type,
                "found": result.found,
                "gid": result.gid,
                "shopify_display_name": result.shopify_display_name,
                "search_attempts": result.search_attempts
            })
        
        # Save to file
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to: {output_file}")
            logger.info(f"File size: {os.path.getsize(output_file) / 1024:.1f} KB")
            
        except Exception as e:
            logger.error(f"Failed to save results to {output_file}: {e}")
            raise

def main():
    """
    Main function to run the GID resolution process
    """
    logger.info("="*60)
    logger.info("LAPTOP COMPONENT GID RESOLUTION - PHASE 2")
    logger.info("="*60)
    logger.info(f"Script started at: {datetime.now().isoformat()}")
    
    try:
        # Initialize resolver
        resolver = GIDResolver()
        
        # Load unmapped components from Phase 1
        unmapped_data = resolver.load_unmapped_components()
        
        # Resolve all unmapped components
        summary = resolver.resolve_all_unmapped_components(unmapped_data)
        
        # Save results
        resolver.save_results(summary)
        
        logger.info("\n" + "="*60)
        logger.info("PHASE 2 GID RESOLUTION COMPLETED SUCCESSFULLY!")
        logger.info("="*60)
        logger.info(f"Check results in: data/analysis/gid_resolution_results.json")
        logger.info(f"Check logs in: scripts/metaobjects/gid_resolution.log")
        
        return 0
        
    except Exception as e:
        logger.error(f"Critical error in GID resolution process: {e}")
        logger.error("Phase 2 GID resolution failed!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)