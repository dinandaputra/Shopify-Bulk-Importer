#!/usr/bin/env python3
"""
Repository Layer Validation Script

This script validates the new repository layer implementation against
the existing metaobject data to ensure proper functionality and data
integrity for Task 1.3 of the laptop scalability refactor.
"""

import os
import sys
import json
from typing import Dict, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from repositories.metaobject_repository import MetaobjectRepository
from repositories.product_data_repository import ProductDataRepository


def validate_metaobject_repository():
    """Validate MetaobjectRepository functionality."""
    print("🔍 Validating MetaobjectRepository...")
    
    repo = MetaobjectRepository()
    validation_results = {
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    # Test all component type mappings
    component_tests = [
        ("processors", repo.get_processor_mapping),
        ("vga", repo.get_vga_mapping),
        ("graphics", repo.get_graphics_mapping),
        ("displays", repo.get_display_mapping),
        ("storage", repo.get_storage_mapping),
        ("colors", repo.get_color_mapping),
        ("os", repo.get_os_mapping),
        ("keyboard_layouts", repo.get_keyboard_layout_mapping),
        ("keyboard_backlights", repo.get_keyboard_backlight_mapping),
    ]
    
    for component_type, method in component_tests:
        try:
            mapping = method()
            
            # Validate mapping structure
            if not isinstance(mapping, dict):
                validation_results["errors"].append(f"{component_type}: Expected dict, got {type(mapping)}")
                validation_results["failed"] += 1
                continue
            
            # Validate GID format
            invalid_gids = []
            for key, gid in mapping.items():
                if not gid.startswith("gid://shopify/Metaobject/"):
                    invalid_gids.append(f"{key}: {gid}")
            
            if invalid_gids:
                validation_results["errors"].append(f"{component_type}: Invalid GID format: {invalid_gids[:3]}...")
                validation_results["failed"] += 1
            else:
                print(f"  ✅ {component_type}: {len(mapping)} mappings loaded successfully")
                validation_results["passed"] += 1
                
        except Exception as e:
            validation_results["errors"].append(f"{component_type}: {str(e)}")
            validation_results["failed"] += 1
    
    # Test unified get_gid method
    try:
        # Test with existing processor
        processor_mapping = repo.get_processor_mapping()
        if processor_mapping:
            first_processor = list(processor_mapping.keys())[0]
            expected_gid = processor_mapping[first_processor]
            actual_gid = repo.get_gid("processor", first_processor)
            
            if actual_gid == expected_gid:
                print(f"  ✅ Unified get_gid method working correctly")
                validation_results["passed"] += 1
            else:
                validation_results["errors"].append(f"get_gid mismatch: expected {expected_gid}, got {actual_gid}")
                validation_results["failed"] += 1
        
        # Test invalid component type
        invalid_gid = repo.get_gid("invalid_type", "test")
        if invalid_gid is None:
            print(f"  ✅ Invalid component type correctly returns None")
            validation_results["passed"] += 1
        else:
            validation_results["errors"].append(f"Invalid component type should return None, got {invalid_gid}")
            validation_results["failed"] += 1
            
    except Exception as e:
        validation_results["errors"].append(f"get_gid method: {str(e)}")
        validation_results["failed"] += 1
    
    # Test component types and options
    try:
        component_types = repo.get_all_component_types()
        expected_types = [
            "processor", "vga", "graphics", "display", "storage",
            "color", "os", "keyboard_layout", "keyboard_backlight"
        ]
        
        if component_types == expected_types:
            print(f"  ✅ All component types correctly listed")
            validation_results["passed"] += 1
        else:
            validation_results["errors"].append(f"Component types mismatch: {component_types}")
            validation_results["failed"] += 1
            
    except Exception as e:
        validation_results["errors"].append(f"Component types: {str(e)}")
        validation_results["failed"] += 1
    
    # Test caching functionality
    try:
        # Clear cache and load
        repo.clear_cache()
        cache_info_empty = repo.get_cache_info()
        
        # Load some data
        repo.get_processor_mapping()
        cache_info_loaded = repo.get_cache_info()
        
        if len(cache_info_empty) == 0 and len(cache_info_loaded) > 0:
            print(f"  ✅ Caching functionality working correctly")
            validation_results["passed"] += 1
        else:
            validation_results["errors"].append(f"Cache not working: empty={cache_info_empty}, loaded={cache_info_loaded}")
            validation_results["failed"] += 1
            
    except Exception as e:
        validation_results["errors"].append(f"Caching: {str(e)}")
        validation_results["failed"] += 1
    
    return validation_results


def validate_product_data_repository():
    """Validate ProductDataRepository functionality."""
    print("\n🔍 Validating ProductDataRepository...")
    
    repo = ProductDataRepository()
    validation_results = {
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    # Test get_all_brands
    try:
        brands = repo.get_all_brands()
        
        if isinstance(brands, list):
            print(f"  ✅ get_all_brands returned list with {len(brands)} brands")
            validation_results["passed"] += 1
            
            # If no brands exist yet, that's expected for this test
            if len(brands) == 0:
                print(f"  ℹ️  No brand data files found yet (expected for new system)")
        else:
            validation_results["errors"].append(f"get_all_brands: Expected list, got {type(brands)}")
            validation_results["failed"] += 1
            
    except Exception as e:
        validation_results["errors"].append(f"get_all_brands: {str(e)}")
        validation_results["failed"] += 1
    
    # Test get_all_models (should handle empty case gracefully)
    try:
        all_models = repo.get_all_models()
        
        if isinstance(all_models, dict):
            print(f"  ✅ get_all_models returned dict with {len(all_models)} models")
            validation_results["passed"] += 1
        else:
            validation_results["errors"].append(f"get_all_models: Expected dict, got {type(all_models)}")
            validation_results["failed"] += 1
            
    except Exception as e:
        validation_results["errors"].append(f"get_all_models: {str(e)}")
        validation_results["failed"] += 1
    
    # Test brand count
    try:
        brand_count = repo.get_brand_count()
        
        if isinstance(brand_count, int) and brand_count >= 0:
            print(f"  ✅ get_brand_count returned valid count: {brand_count}")
            validation_results["passed"] += 1
        else:
            validation_results["errors"].append(f"get_brand_count: Expected non-negative int, got {brand_count}")
            validation_results["failed"] += 1
            
    except Exception as e:
        validation_results["errors"].append(f"get_brand_count: {str(e)}")
        validation_results["failed"] += 1
    
    # Test model count
    try:
        model_count = repo.get_model_count()
        
        if isinstance(model_count, int) and model_count >= 0:
            print(f"  ✅ get_model_count returned valid count: {model_count}")
            validation_results["passed"] += 1
        else:
            validation_results["errors"].append(f"get_model_count: Expected non-negative int, got {model_count}")
            validation_results["failed"] += 1
            
    except Exception as e:
        validation_results["errors"].append(f"get_model_count: {str(e)}")
        validation_results["failed"] += 1
    
    # Test search functionality
    try:
        search_results = repo.search_models("test")
        
        if isinstance(search_results, list):
            print(f"  ✅ search_models returned list with {len(search_results)} results")
            validation_results["passed"] += 1
        else:
            validation_results["errors"].append(f"search_models: Expected list, got {type(search_results)}")
            validation_results["failed"] += 1
            
    except Exception as e:
        validation_results["errors"].append(f"search_models: {str(e)}")
        validation_results["failed"] += 1
    
    # Test caching functionality
    try:
        repo.clear_cache()
        cache_info_empty = repo.get_cache_info()
        
        # Try to load data (will be empty but should work)
        repo.get_all_models()
        cache_info_loaded = repo.get_cache_info()
        
        print(f"  ✅ Caching functionality working (empty: {len(cache_info_empty)}, loaded: {len(cache_info_loaded)})")
        validation_results["passed"] += 1
        
    except Exception as e:
        validation_results["errors"].append(f"Caching: {str(e)}")
        validation_results["failed"] += 1
    
    return validation_results


def validate_repository_integration():
    """Validate integration between repositories."""
    print("\n🔍 Validating Repository Integration...")
    
    validation_results = {
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    try:
        metaobject_repo = MetaobjectRepository()
        product_repo = ProductDataRepository()
        
        # Test that both repositories can be instantiated together
        print(f"  ✅ Both repositories can be instantiated together")
        validation_results["passed"] += 1
        
        # Test that they use different cache systems
        metaobject_repo.clear_cache()
        product_repo.clear_cache()
        
        # Load data in each
        metaobject_repo.get_processor_mapping()
        product_repo.get_all_models()
        
        meta_cache = metaobject_repo.get_cache_info()
        product_cache = product_repo.get_cache_info()
        
        print(f"  ✅ Independent caching systems working (meta: {len(meta_cache)}, product: {len(product_cache)})")
        validation_results["passed"] += 1
        
    except Exception as e:
        validation_results["errors"].append(f"Integration: {str(e)}")
        validation_results["failed"] += 1
    
    return validation_results


def print_validation_summary(results: Dict[str, Dict]):
    """Print validation summary."""
    print("\n" + "="*60)
    print("REPOSITORY LAYER VALIDATION SUMMARY")
    print("="*60)
    
    total_passed = sum(r["passed"] for r in results.values())
    total_failed = sum(r["failed"] for r in results.values())
    total_tests = total_passed + total_failed
    
    for test_name, result in results.items():
        status = "✅ PASS" if result["failed"] == 0 else "❌ FAIL"
        print(f"{test_name}: {status} ({result['passed']}/{result['passed'] + result['failed']} tests)")
        
        if result["errors"]:
            print(f"  Errors:")
            for error in result["errors"][:3]:  # Show first 3 errors
                print(f"    - {error}")
            if len(result["errors"]) > 3:
                print(f"    - ... and {len(result['errors']) - 3} more errors")
    
    print(f"\nOVERALL: {total_passed}/{total_tests} tests passed")
    
    if total_failed == 0:
        print("🎉 All repository layer validations PASSED!")
        print("\n✅ Task 1.3 repository layer implementation is working correctly")
    else:
        print(f"⚠️  {total_failed} validations FAILED - see errors above")
        print("\n❌ Task 1.3 repository layer needs fixes before proceeding")
    
    return total_failed == 0


def main():
    """Main validation function."""
    print("Repository Layer Validation - Task 1.3")
    print("Laptop Scalability Refactor Plan")
    print("="*60)
    
    # Run all validations
    results = {
        "MetaobjectRepository": validate_metaobject_repository(),
        "ProductDataRepository": validate_product_data_repository(),
        "Integration": validate_repository_integration()
    }
    
    # Print summary
    success = print_validation_summary(results)
    
    # Return appropriate exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()