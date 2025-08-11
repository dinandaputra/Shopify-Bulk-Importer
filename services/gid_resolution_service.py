"""
Comprehensive GID Resolution Service for Laptop Component Mapping

This service handles the complete GID resolution process for missing laptop components
by querying Shopify's GraphQL API with intelligent search strategies.

Author: Shopify API Developer (Claude Code Sub-Agent System)
Date: 2025-08-06
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from services.shopify_api import ShopifyAPIClient, ShopifyAPIError


@dataclass
class ComponentSearchResult:
    """Result of a component GID search"""
    component_name: str
    component_type: str
    found: bool
    gid: Optional[str] = None
    shopify_display_name: Optional[str] = None
    search_attempts: List[str] = field(default_factory=list)
    search_method: Optional[str] = None


@dataclass
class GIDResolutionResults:
    """Complete results of GID resolution process"""
    total_components_processed: int
    components_found: int
    components_not_found: int
    success_rate_percent: float
    processing_time_seconds: float
    api_calls_made: int
    resolved_components: Dict[str, Dict[str, ComponentSearchResult]] = field(default_factory=dict)
    not_found_components: Dict[str, List[str]] = field(default_factory=dict)


class GIDResolutionService:
    """
    Comprehensive service for resolving missing component GIDs from Shopify API
    
    This service implements intelligent search strategies to find metaobjects
    for laptop components across VGA, Graphics, Displays, and Storage types.
    """
    
    def __init__(self, shopify_client: ShopifyAPIClient = None):
        """Initialize the GID Resolution Service"""
        self.api = shopify_client or ShopifyAPIClient()
        self.api_calls_made = 0
        self.processing_start_time = None
        
        # Component type to metaobject type mapping for Shopify queries
        self.metaobject_type_mapping = {
            "vga": "dedicated_graphics",
            "graphics": "integrated_graphics", 
            "displays": "display_laptop",
            "storage": "storage_laptop"
        }
        
        # Search strategy configurations for different component types
        self.search_strategies = {
            "vga": self._generate_vga_search_variations,
            "graphics": self._generate_graphics_search_variations,
            "displays": self._generate_display_search_variations,
            "storage": self._generate_storage_search_variations
        }
    
    def resolve_missing_gids(self, missing_components: Dict[str, List[str]]) -> GIDResolutionResults:
        """
        Resolve GIDs for all missing components using comprehensive search strategies
        
        Args:
            missing_components: Dictionary mapping component type to list of missing component names
            
        Returns:
            GIDResolutionResults with complete resolution status
        """
        self.processing_start_time = time.time()
        self.api_calls_made = 0
        
        results = GIDResolutionResults(
            total_components_processed=sum(len(components) for components in missing_components.values()),
            components_found=0,
            components_not_found=0,
            success_rate_percent=0.0,
            processing_time_seconds=0.0,
            api_calls_made=0
        )
        
        print(f"🔍 Starting GID resolution for {results.total_components_processed} missing components...")
        
        # Process each component type
        for component_type, components in missing_components.items():
            if not components:
                continue
                
            print(f"\n📋 Processing {len(components)} {component_type} components...")
            
            # Initialize results structure for this component type
            results.resolved_components[component_type] = {}
            results.not_found_components[component_type] = []
            
            # Process each component
            for component_name in components:
                print(f"  🔎 Searching for: {component_name}")
                
                search_result = self._search_component(component_name, component_type)
                
                if search_result.found:
                    results.resolved_components[component_type][component_name] = search_result
                    results.components_found += 1
                    print(f"    ✅ Found: {search_result.gid}")
                else:
                    results.not_found_components[component_type].append(component_name)
                    results.components_not_found += 1
                    print(f"    ❌ Not found after {len(search_result.search_attempts)} attempts")
                
                # Rate limiting between searches
                time.sleep(0.5)
        
        # Calculate final metrics
        processing_time = time.time() - self.processing_start_time
        results.processing_time_seconds = round(processing_time, 2)
        results.api_calls_made = self.api_calls_made
        
        if results.total_components_processed > 0:
            results.success_rate_percent = round(
                (results.components_found / results.total_components_processed) * 100, 2
            )
        
        print(f"\n📊 GID Resolution Complete:")
        print(f"   • Total processed: {results.total_components_processed}")
        print(f"   • Found: {results.components_found}")
        print(f"   • Not found: {results.components_not_found}")
        print(f"   • Success rate: {results.success_rate_percent}%")
        print(f"   • Processing time: {results.processing_time_seconds}s")
        print(f"   • API calls made: {results.api_calls_made}")
        
        return results
    
    def _search_component(self, component_name: str, component_type: str) -> ComponentSearchResult:
        """
        Search for a specific component using intelligent search strategies
        
        Args:
            component_name: Name of the component to search for
            component_type: Type of component (vga, graphics, displays, storage)
            
        Returns:
            ComponentSearchResult with search outcome
        """
        search_result = ComponentSearchResult(
            component_name=component_name,
            component_type=component_type,
            found=False
        )
        
        # Get metaobject type for Shopify query
        metaobject_type = self.metaobject_type_mapping.get(component_type)
        if not metaobject_type:
            print(f"    ⚠️ Unknown component type: {component_type}")
            return search_result
        
        # Generate search variations using appropriate strategy
        search_strategy = self.search_strategies.get(component_type)
        if not search_strategy:
            print(f"    ⚠️ No search strategy for component type: {component_type}")
            return search_result
        
        search_variations = search_strategy(component_name)
        search_result.search_attempts = search_variations
        
        # Try each search variation
        for search_term in search_variations:
            try:
                metaobjects = self._query_metaobjects_by_type(metaobject_type, search_term)
                
                if metaobjects:
                    # Found at least one match - take the first one
                    metaobject = metaobjects[0]
                    search_result.found = True
                    search_result.gid = metaobject['id']
                    search_result.shopify_display_name = metaobject.get('displayName', '')
                    search_result.search_method = f"Search term: '{search_term}'"
                    break
                    
            except ShopifyAPIError as e:
                print(f"    ⚠️ API error searching '{search_term}': {e}")
                continue
            except Exception as e:
                print(f"    ⚠️ Unexpected error searching '{search_term}': {e}")
                continue
        
        return search_result
    
    def _query_metaobjects_by_type(self, metaobject_type: str, search_term: str) -> List[Dict[str, Any]]:
        """
        Query Shopify for metaobjects of specific type matching search term
        
        Args:
            metaobject_type: Shopify metaobject type to query
            search_term: Term to search for in metaobject names
            
        Returns:
            List of matching metaobjects
        """
        query = """
        query GetMetaobjects($type: String!, $first: Int!, $query: String) {
          metaobjects(type: $type, first: $first, query: $query) {
            nodes {
              id
              type
              displayName
              handle
              fields {
                key
                value
              }
            }
          }
        }
        """
        
        variables = {
            "type": metaobject_type,
            "first": 50,  # Reasonable limit for searches
            "query": f"displayName:*{search_term}*"
        }
        
        try:
            response = self.api._make_graphql_request(query, variables)
            self.api_calls_made += 1
            
            metaobjects = response.get('data', {}).get('metaobjects', {}).get('nodes', [])
            return metaobjects
            
        except Exception as e:
            print(f"    ⚠️ GraphQL query failed for {metaobject_type} with '{search_term}': {e}")
            raise ShopifyAPIError(f"Failed to query metaobjects: {e}")
    
    # Search strategy generators for different component types
    
    def _generate_vga_search_variations(self, component_name: str) -> List[str]:
        """Generate search variations for VGA/GPU components"""
        variations = []
        
        # Original name
        variations.append(component_name)
        
        # Common GPU name transformations
        if "NVIDIA GeForce" in component_name:
            # Try without NVIDIA GeForce prefix
            clean_name = component_name.replace("NVIDIA GeForce ", "")
            variations.append(clean_name)
            
            # Try with just the model number
            if "RTX" in clean_name or "GTX" in clean_name:
                # Extract RTX/GTX + number part
                parts = clean_name.split()
                if len(parts) >= 2:
                    model_part = f"{parts[0]} {parts[1]}"  # e.g., "RTX 4060"
                    variations.append(model_part)
        
        # Try without memory specifications
        if "GB" in component_name or "gb" in component_name:
            no_memory = component_name.split("GB")[0].split("gb")[0].strip()
            if no_memory != component_name:
                variations.append(no_memory)
        
        # Try abbreviated forms
        if "Ti" in component_name:
            variations.append(component_name.replace(" Ti ", " Ti"))
        
        return variations
    
    def _generate_graphics_search_variations(self, component_name: str) -> List[str]:
        """Generate search variations for integrated graphics components"""
        variations = []
        
        # Original name
        variations.append(component_name)
        
        # Intel graphics variations
        if "Intel" in component_name:
            # Try without "Intel " prefix
            clean_name = component_name.replace("Intel ", "")
            variations.append(clean_name)
            
            # Try different Intel graphics naming
            if "UHD Graphics" in component_name:
                # Try with number if present
                if "770" in component_name:
                    variations.extend(["UHD Graphics 770", "Intel UHD 770", "UHD 770"])
        
        # AMD graphics variations  
        if "AMD" in component_name:
            # Try without "AMD " prefix
            clean_name = component_name.replace("AMD ", "")
            variations.append(clean_name)
            
            if "Radeon" in component_name:
                # Try different Radeon naming patterns
                variations.extend(["Radeon Graphics", "AMD Radeon"])
                if "680M" in component_name:
                    variations.extend(["Radeon 680M", "680M Graphics"])
        
        return variations
    
    def _generate_display_search_variations(self, component_name: str) -> List[str]:
        """Generate search variations for display components"""
        variations = []
        
        # Original name
        variations.append(component_name)
        
        # Common display transformations
        # Handle refresh rate variations
        if "Hz)" in component_name:
            # Try with different parenthesis formats
            no_parens = component_name.replace("(", "").replace(")", "")
            variations.append(no_parens)
            
            # Extract refresh rate
            if "144Hz" in component_name:
                variations.extend(["144Hz", "144 Hz", "144hz"])
            elif "120Hz" in component_name:
                variations.extend(["120Hz", "120 Hz", "120hz"])
            elif "165Hz" in component_name:
                variations.extend(["165Hz", "165 Hz", "165hz"])
            elif "240Hz" in component_name:
                variations.extend(["240Hz", "240 Hz", "240hz"])
            elif "300Hz" in component_name:
                variations.extend(["300Hz", "300 Hz", "300hz"])
        
        # Screen size variations
        if "15-inch" in component_name:
            variations.append(component_name.replace("15-inch", "15.6-inch"))
        elif "17.3-inch" in component_name:
            variations.extend([
                component_name.replace("17.3-inch", "17.3"),
                component_name.replace("17.3-inch", "17\"")
            ])
        elif "14-inch" in component_name:
            variations.append(component_name.replace("14-inch", "14\""))
        
        # Resolution variations
        if "FHD" in component_name:
            variations.extend([
                component_name.replace("FHD", "Full HD"),
                component_name.replace("FHD", "1920x1080")
            ])
        elif "4K UHD" in component_name:
            variations.extend([
                component_name.replace("4K UHD", "4K"),
                component_name.replace("4K UHD", "UHD")
            ])
        elif "QHD" in component_name:
            variations.extend([
                component_name.replace("QHD", "Quad HD"),
                component_name.replace("QHD", "2560x1440")
            ])
        
        return variations
    
    def _generate_storage_search_variations(self, component_name: str) -> List[str]:
        """Generate search variations for storage components"""
        variations = []
        
        # Original name
        variations.append(component_name)
        
        # Storage capacity variations
        if "TB" in component_name:
            if "2TB" in component_name:
                variations.extend([
                    "2TB SSD",
                    "2 TB SSD", 
                    "2TB Solid State Drive",
                    "2000GB SSD",
                    "2048GB SSD"
                ])
        
        # Try without specific technology
        if "SSD" in component_name:
            base_capacity = component_name.replace("SSD", "").strip()
            variations.extend([
                f"{base_capacity} Solid State Drive",
                f"{base_capacity} Storage"
            ])
        
        return variations
    
    def save_results_to_file(self, results: GIDResolutionResults, output_path: Path) -> None:
        """
        Save GID resolution results to JSON file
        
        Args:
            results: GID resolution results to save
            output_path: Path to save results file
        """
        # Convert results to JSON-serializable format
        results_dict = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "script_version": "1.0.0",
                "total_components_processed": results.total_components_processed,
                "components_found": results.components_found,
                "components_not_found": results.components_not_found,
                "success_rate_percent": results.success_rate_percent,
                "processing_time_seconds": results.processing_time_seconds,
                "api_calls_made": results.api_calls_made
            },
            "summary_by_type": {},
            "resolved_components": {},
            "not_found_components": results.not_found_components,
            "search_details": []
        }
        
        # Build summary by type and search details
        for component_type, components in results.resolved_components.items():
            total = len(components) + len(results.not_found_components.get(component_type, []))
            found = len(components)
            not_found = len(results.not_found_components.get(component_type, []))
            
            results_dict["summary_by_type"][component_type] = {
                "total": total,
                "found": found,
                "not_found": not_found,
                "success_rate": round((found / total * 100) if total > 0 else 0, 2)
            }
            
            # Convert resolved components to simple dict format
            results_dict["resolved_components"][component_type] = {}
            for comp_name, search_result in components.items():
                results_dict["resolved_components"][component_type][comp_name] = {
                    "gid": search_result.gid,
                    "shopify_display_name": search_result.shopify_display_name
                }
                
                # Add search details
                results_dict["search_details"].append({
                    "component_name": search_result.component_name,
                    "component_type": search_result.component_type,
                    "found": search_result.found,
                    "gid": search_result.gid,
                    "shopify_display_name": search_result.shopify_display_name,
                    "search_attempts": search_result.search_attempts,
                    "search_method": search_result.search_method
                })
        
        # Add not found components to search details
        for component_type, components in results.not_found_components.items():
            for comp_name in components:
                results_dict["search_details"].append({
                    "component_name": comp_name,
                    "component_type": component_type,
                    "found": False,
                    "gid": None,
                    "shopify_display_name": None,
                    "search_attempts": [],  # Would need to store this from search process
                    "search_method": None
                })
        
        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 GID resolution results saved to: {output_path}")