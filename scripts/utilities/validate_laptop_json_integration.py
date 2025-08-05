#!/usr/bin/env python3
"""
Validate Laptop JSON Integration with Repository Layer

This script validates that the newly created per-brand JSON files integrate correctly
with the existing ProductDataRepository and can be used for laptop data access.

Task 1.4 Validation: Test repository integration
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import repository and test existing laptop data access
try:
    from repositories.product_data_repository import ProductDataRepository
    print("✅ Successfully imported ProductDataRepository")
except ImportError as e:
    print(f"❌ Failed to import ProductDataRepository: {e}")
    sys.exit(1)

def test_repository_integration():
    """Test integration with repository layer"""
    print("\n🧪 Testing Repository Integration")
    print("=" * 50)
    
    # Initialize repository
    try:
        repo = ProductDataRepository()
        print("✅ ProductDataRepository initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize repository: {e}")
        return False
    
    # Test loading all brands
    try:
        all_brands = repo.get_all_brands()
        print(f"✅ Loaded {len(all_brands)} brands: {all_brands}")
    except Exception as e:
        print(f"❌ Failed to load all brands: {e}")
        return False
    
    # Test loading specific brand data (ASUS should have 34+ models)
    try:
        asus_data = repo.get_brand_data("ASUS")
        if asus_data:
            model_count = len(asus_data.get("models", {}))
            print(f"✅ ASUS data loaded: {model_count} models")
            
            if model_count >= 30:
                print("✅ ASUS model count validation passed (30+ models)")
            else:
                print(f"❌ ASUS model count validation failed: {model_count} < 30")
                return False
        else:
            print("❌ Failed to load ASUS data")
            return False
    except Exception as e:
        print(f"❌ Failed to load ASUS data: {e}")
        return False
    
    # Test loading all models
    try:
        all_models = repo.get_all_models()
        total_models = len(all_models)
        print(f"✅ Loaded {total_models} total models")
        
        if total_models >= 38:  # Should have exactly 38 models based on extraction
            print("✅ Total model count validation passed")
        else:
            print(f"❌ Total model count validation failed: {total_models} < 38")
            return False
    except Exception as e:
        print(f"❌ Failed to load all models: {e}")
        return False
    
    # Test model search functionality
    try:
        search_results = repo.search_models("TUF Gaming", brand="ASUS")
        print(f"✅ Search for 'TUF Gaming' in ASUS: {len(search_results)} results")
        
        if len(search_results) > 0:
            print("✅ Search functionality working")
        else:
            print("⚠️  Search returned no results - this might be expected")
    except Exception as e:
        print(f"❌ Search functionality failed: {e}")
        return False
    
    # Test model counting
    try:
        total_count = repo.get_model_count()
        brand_counts = {brand: repo.get_model_count(brand) for brand in all_brands}
        
        print(f"✅ Total model count: {total_count}")
        print("✅ Brand model counts:")
        for brand, count in brand_counts.items():
            print(f"   {brand}: {count} models")
        
        # Verify counts match
        sum_brand_counts = sum(brand_counts.values())
        if total_count == sum_brand_counts:
            print("✅ Model count consistency validated")
        else:
            print(f"❌ Model count inconsistency: total={total_count}, sum={sum_brand_counts}")
            return False
            
    except Exception as e:
        print(f"❌ Model counting failed: {e}")
        return False
    
    return True

def test_data_structure_validation():
    """Test that the JSON data structure matches expected format"""
    print("\n📋 Testing Data Structure")
    print("=" * 50)
    
    try:
        repo = ProductDataRepository()
        
        # Get sample model data and validate structure
        asus_data = repo.get_brand_data("ASUS")
        if not asus_data or "models" not in asus_data:
            print("❌ ASUS data structure invalid")
            return False
        
        # Test first model structure
        first_model_key = list(asus_data["models"].keys())[0]
        first_model = asus_data["models"][first_model_key]
        
        # Required fields
        required_fields = ["display_name", "series", "year", "category", "configurations", "colors"]
        for field in required_fields:
            if field not in first_model:
                print(f"❌ Missing required field: {field}")
                return False
        
        print("✅ All required model fields present")
        
        # Test configuration structure
        if not first_model["configurations"]:
            print("❌ No configurations found")
            return False
        
        first_config = first_model["configurations"][0]
        config_fields = ["cpu", "ram", "vga", "gpu", "display", "storage", "os", "keyboard_layout", "keyboard_backlight"]
        for field in config_fields:
            if field not in first_config:
                print(f"❌ Missing configuration field: {field}")
                return False
        
        print("✅ All required configuration fields present")
        
        # Test that component names are full (not abbreviated)
        cpu = first_config["cpu"]
        if "Intel Core" not in cpu and "AMD Ryzen" not in cpu:
            print(f"❌ CPU name appears abbreviated: {cpu}")
            return False
        
        print("✅ CPU names are in full format")
        
        # Test VGA field contains full GPU names when not empty
        vga = first_config["vga"]
        if vga and ("NVIDIA GeForce" not in vga and "AMD Radeon" not in vga):
            print(f"❌ VGA name appears abbreviated: {vga}")
            return False
        
        if vga:
            print("✅ VGA names are in full format")
        else:
            print("✅ VGA field correctly empty for integrated-only system")
        
        return True
        
    except Exception as e:
        print(f"❌ Data structure validation failed: {e}")
        return False

def main():
    """Main validation process"""
    print("🔍 Laptop JSON Integration Validation")
    print("Task 1.4: Validate repository integration with extracted JSON files")
    print("=" * 70)
    
    # Test repository integration
    integration_success = test_repository_integration()
    
    # Test data structure validation
    structure_success = test_data_structure_validation()
    
    # Overall validation result
    print("\n" + "=" * 70)
    if integration_success and structure_success:
        print("✅ ALL VALIDATIONS PASSED")
        print("🎉 Task 1.4 validation successful!")
        print("📁 Per-brand JSON files are ready for use with repository layer")
    else:
        print("❌ VALIDATION FAILED")
        print("🔍 Check errors above and fix issues before proceeding")
    
    return integration_success and structure_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)