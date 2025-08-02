# Technical Reference

## API Integration Status (Updated July 28, 2025) ✅ WORKING IMPLEMENTATION

- **✅ FULLY WORKING**: Direct variant-to-metafield linking using GraphQL metafieldsSet mutation
- **✅ FIXED**: Product creation with SIM carrier variants using GraphQL productSet
- **✅ FIXED**: Inventory management - products have correct tracked inventory levels
- **✅ WORKING**: 4/6 metafields via API: ram_size, minus (working), product_rank, product_inclusions
- **✅ WORKING**: Each SIM carrier variant individually linked to its specific metaobject
- **✅ WORKING**: Error handling with detailed logging and GraphQL error reporting
- **✅ WORKING**: Rate limiting and proper API authentication

## 🎯 WORKING VARIANT METAFIELD IMPLEMENTATION (DO NOT MODIFY)

### Shopify Admin Setup Required:
1. **Product-level metafield**: `custom.sim_carriers` (type: list.metaobject_reference)
2. **Variant-level metafield**: `custom.sim_carrier` (type: list.metaobject_reference) ⭐ KEY REQUIREMENT

### Working Code Structure:
- **services/shopify_api.py**: `assign_metafields_to_variants()` method using metafieldsSet mutation
- **services/product_service.py**: Post-creation variant metafield assignment
- **Test verification**: `verify_variant_metafields.py` script confirms each variant has correct metafield

### Proven Working Example:
- **Product ID**: 8843114479765
- **URL**: https://jufbtk-ut.myshopify.com/admin/products/8843114479765
- **Status**: All 3 variants successfully linked to individual metaobjects
- **Verification**: GraphQL query confirms metafields exist on each variant

### Key Technical Details:
```python
# Working GraphQL mutation structure
mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id, key, namespace, value, ownerType, createdAt
    }
    userErrors { field, message }
  }
}

# Working metafield data format
{
  "ownerId": "gid://shopify/ProductVariant/123",
  "namespace": "custom", 
  "key": "sim_carrier",
  "value": '["gid://shopify/Metaobject/456"]',  # JSON array format
  "type": "list.metaobject_reference"
}
```

### Key Breakthrough: MetafieldsSet Mutation
```python
# Final working implementation
def assign_metafields_to_variants(self, variant_metafield_data):
    mutation = """mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {...}"""
    # Each variant gets individual metafield with its specific metaobject GID
```

### ROLLBACK INSTRUCTIONS
If option-to-metafield linking attempts fail, revert to current working state:
1. Keep `services/shopify_api.py:assign_metafields_to_variants()` method  
2. Keep `services/product_service.py` post-creation variant assignment logic
3. Use `verify_variant_metafields.py` to confirm variant linking still works
4. Test with product creation to ensure variant metafields remain functional

## Metafield Management

### Smartphone Metafields
- Uses actual Shopify metaobject IDs for references
- 5/6 metafields working: product_rank, product_inclusions, ram_size, minus, sim_carriers (via variants)
- Color metafield disabled (requires metafield definition setup in admin)
- Supports both single and list metaobject references with JSON string formatting
- Graceful error handling when metafield creation fails

### Laptop Metafields
- **CPU**: Processor specifications mapped to metaobjects
- **RAM**: Memory size options (4GB, 8GB, 16GB, 32GB, 64GB)
- **GPU**: Graphics card specifications
- **Display**: Screen size and resolution
- **Storage**: SSD/HDD capacity and type
- **OS**: Operating system (Windows 11, Windows 10, etc.)
- **Keyboard**: Layout and backlight options
- **Missing Entry Logging**: Automatic detection and logging of unmapped values

### SIM Carrier Variants (WORKING)
- Staff select which SIM carrier variants are available per device
- Supports 1-5 variants: SIM Free, Softbank (-), Docomo (-), AU (-), Rakuten Mobile (-)
- Inventory properly tracked and distributed evenly across selected variants
- Creates product options automatically based on selected carriers
- Examples:
  - Product A: ["SIM Free"] → Creates 1 variant with full inventory
  - Product B: ["SIM Free", "Softbank (-)"] → Creates 2 variants with split inventory  
  - Product C: ["Softbank (-)"] → Creates 1 variant with full inventory

## 🎯 Next Goal: Option-to-Metafield Linking
- **Current**: Variants linked to metafields ✅
- **Desired**: Option "SIM Carriers" linked to metafield (removes "Connect metafield" button)
- **Challenge**: GraphQL productSet linkedMetafield has API conflicts
- **Approach**: Research option-specific mutations or alternative linking methods

## Data Validation
- Required fields: title, brand, model, price
- SIM carrier variants optional but recommended for proper variant creation
- Price must be positive (validated in JPY)
- Multi-select fields (inclusions, minus, sim_carrier_variants) supported
- Automatic handle generation with date/counter system

### Testing & Verification
- Test products via product_service.create_smartphone_product()
- **Live Example**: https://jufbtk-ut.myshopify.com/admin/products/8842615423125
- Verify inventory tracking in Shopify admin products section
- Check variant creation and inventory distribution
- Metafields appear in product admin (working: ram_size, minus)

## API Documentation & Reference

### ALWAYS Use Documentation Before API Work
When working with Shopify APIs, you MUST consult documentation in this order:

1. **Local Store-Specific Docs** (PRIORITY 1 - Check first)
   - **`docs/shopify-api/README.md`**: Store-specific overview with your metaobject IDs
   - **`docs/shopify-api/product-rest-structure.md`**: Real product structure from your store
   - **`docs/shopify-api/metafields-rest.md`**: REST metafields with working examples
   - **`docs/shopify-api/metaobject-graphql.md`**: GraphQL metaobject operations
   - **`docs/shopify-api/product-graphql.md`**: GraphQL product operations

2. **Shopify Dev MCP** (PRIORITY 2 - For official/latest docs)
   - Configured at `~/.cursor/mcp.json` as `shopify-dev-mcp`
   - Use for official API schemas and new feature discovery
   - Always current with latest Shopify API changes

### Your Metaobject Definitions (Use these exact GIDs)
- **Cosmetic condition**: `gid://shopify/MetaobjectDefinition/7936508053`
- **SIM card capability**: `gid://shopify/MetaobjectDefinition/7936540821`
- **Operating system**: `gid://shopify/MetaobjectDefinition/7936573589`
- **Color**: `gid://shopify/MetaobjectDefinition/7936606357`
- **Subscription type**: `gid://shopify/MetaobjectDefinition/7936639125`

### Documentation Workflow
1. **Before any API change**: Read relevant local docs first
2. **For new features**: Check Shopify Dev MCP for latest API additions
3. **For debugging**: Reference both local examples and official MCP schemas
4. **Never guess**: Always verify API structure against documentation

## 📚 Adding New Laptop Models Guide

### Overview
This guide documents the reusable method for adding new laptop models from different brands to the system. The process involves analyzing existing metaobjects, creating missing ones, and testing the implementation.

### Step 1: Analyze Existing Metaobjects
Use the Shopify API to query and document all laptop-related metaobjects:

```python
# Run the analysis script
python scripts/analyze_laptop_metaobjects.py
```

This will generate a report at `/reports/laptop_metaobjects_analysis.json` containing:
- All metaobject definitions and their GIDs
- Existing entries for each metaobject type
- Statistics on coverage

### Step 2: Add New Laptop Templates
Add new laptop models to `config/master_data.py`:

```python
LAPTOP_TEMPLATES = {
    "Brand Model [CPU/RAM/GPU/Display/Storage] [Color]": {
        "brand": "Brand",
        "model": "Model",
        "cpu": "CPU-Model",
        "ram": "XGB",
        "gpu": "GPU-Model",
        "display": "Size RefreshHz",
        "storage": "XXXGB",
        "os": "Windows 11",
        "keyboard_layout": "US",
        "keyboard_backlight": "Yes/RGB/White",
        "color": "Color Name"
    }
}
```

### Step 3: Cross-Reference and Find Gaps
Run the gap analysis to identify missing metaobjects:

```python
# This script compares templates with existing Shopify metaobjects
python scripts/cross_reference_laptop_metaobjects.py
```

Reports generated:
- `/reports/laptop_missing_metaobjects_report.md` - Human-readable gap analysis
- `/reports/laptop_missing_metaobjects_summary.json` - Structured data
- `/scripts/missing_laptop_metaobjects/` - JSON files for each category

### Step 4: Create Missing Metaobjects
Use the automated script to create missing metaobjects in Shopify:

```python
# Create all missing metaobjects
python scripts/missing_laptop_metaobjects/create_missing_metaobjects_graphql.py

# Or create by category
python scripts/missing_laptop_metaobjects/create_missing_metaobjects_graphql.py --category processor
python scripts/missing_laptop_metaobjects/create_missing_metaobjects_graphql.py --category graphics
python scripts/missing_laptop_metaobjects/create_missing_metaobjects_graphql.py --category display
```

**Note**: Color metaobjects require manual creation in Shopify Admin due to taxonomy requirements.

### Step 5: Update Metafield Mappings
If needed, update the mapping in `config/laptop_metafield_mapping_enhanced.py`:

```python
LAPTOP_METAFIELD_MAPPING = {
    "processor": {
        "New CPU Model": "gid://shopify/Metaobject/XXXXX",
        # Add new processor mappings
    },
    "graphics": {
        "New GPU Model": "gid://shopify/Metaobject/XXXXX",
        # Add new graphics mappings
    }
    # Add other mappings as needed
}
```

### Step 6: Test the Implementation
Run the comprehensive test suite:

```python
# Test core functionality without API
python test_laptop_core_functionality.py

# Test with Shopify API (requires credentials)
python test_laptop_product_creation.py

# Test specific templates
python test_laptop_product_creation.py --template "Your New Template Name"
```

### Step 7: Monitor Missing Entries
The system automatically logs missing metaobject mappings:

```bash
# Check the missing entries log
cat logs/missing_metaobjects.json
```

This file tracks:
- Missing metaobject values
- Frequency of missing entries
- Context (which products tried to use them)

### Important Files for Laptop Management

#### Configuration Files
- `config/laptop_specs.py` - Database of laptop models and configurations
- `config/laptop_metafield_mapping_enhanced.py` - Metaobject GID mappings
- `config/laptop_inclusions.py` - Laptop-specific inclusion options

#### Scripts
- `scripts/analyze_laptop_metaobjects.py` - Analyze existing metaobjects
- `scripts/cross_reference_laptop_metaobjects.py` - Find missing entries
- `scripts/missing_laptop_metaobjects/create_missing_metaobjects_graphql.py` - Create metaobjects

#### Reports
- `/reports/laptop_metaobjects_analysis.json` - Current metaobject inventory
- `/reports/laptop_missing_metaobjects_report.md` - Gap analysis
- `/logs/missing_metaobjects.json` - Runtime missing entry tracking

### Metaobject Naming Conventions

When creating new metaobjects, follow these formats:

1. **Processors**: `"Brand Model (X CPUs), ~Clock GHz"`
   - Example: `"Intel Core i7-14700HX (24 CPUs), ~2.1GHz"`

2. **Graphics**: `"Brand Model XGB"`
   - Example: `"NVIDIA GeForce RTX 4060 8GB"`

3. **Display**: `"Size-inch Resolution (RefreshHz)"`
   - Example: `"15.6-inch FHD (144Hz)"`

4. **Storage**: `"Capacity Type"`
   - Example: `"512GB SSD"`

5. **RAM**: `"XGB"`
   - Example: `"16GB"`

### Troubleshooting

1. **Metaobject Creation Fails**
   - Check API credentials are set correctly
   - Verify metaobject definition IDs match your store
   - Check GraphQL error messages in logs

2. **Templates Not Mapping**
   - Check `logs/missing_metaobjects.json` for unmapped values
   - Verify naming format matches expected pattern
   - Run gap analysis to identify missing entries

3. **Product Creation Errors**
   - Enable debug logging in `services/laptop_metafield_service.py`
   - Check Shopify API response for specific errors
   - Verify all required metaobject types exist

### Best Practices

1. **Always run gap analysis** before adding new laptop brands
2. **Create metaobjects in batches** to avoid rate limits
3. **Test with one product** before bulk creation
4. **Monitor missing entries log** regularly
5. **Document new brand specifications** in laptop_specs.py
6. **Follow naming conventions** for consistency

## Recent Development Progress

### July 28, 2025 - Laptop Product Support
- **✅ COMPLETED**: Full laptop product entry system with templates
- **✅ ADDED**: Comprehensive laptop metafield mapping system
- **✅ IMPLEMENTED**: Enhanced logging for missing metaobject entries
- **✅ CREATED**: Laptop-specific inclusions and specifications
- **✅ INTEGRATED**: Laptop templates with auto-population

### July 22, 2025 - ✅ VARIANT LINKING SUCCESS

### Issues Fully Resolved
1. **❌→✅ VARIANT METAFIELD LINKING**: Each variant individually linked to specific metaobject via GraphQL metafieldsSet
2. **❌→✅ API AUTOMATION**: No manual clicking required - fully automated variant-to-metafield connection
3. **❌→✅ METAFIELD DEFINITIONS**: Required variant-level metafield definition `custom.sim_carrier` created in admin
4. **❌→✅ JSON FORMATTING**: Correct `list.metaobject_reference` format with JSON array values
5. **❌→✅ VERIFICATION**: GraphQL query confirms all variant metafields successfully created

## Development History

### ✅ Phase 2 Configuration Management - COMPLETED (2025-07-30)

#### **Goal Achieved**
Successfully consolidated duplicate configuration files and created single source of truth for each configuration type.

#### **Implementation Results**
- **✅ Configuration Consolidation**: Reduced laptop metafield files from 6 → 3 authoritative files
- **✅ Archive Organization**: 3 duplicate files moved to `archive/config/`
- **✅ Import Chain Integrity**: All imports validated and working correctly
- **✅ Processor Regression Fixed**: Resolved missing processor metaobject lookup issue
- **✅ Missing Entries Cleanup**: Cleaned stale entries from logging system
- **✅ Functionality Preserved**: Zero regressions in smartphone or laptop functionality

#### **Configuration Structure**
```
config/
├── laptop_metafield_mapping_enhanced.py     # UI layer (Streamlit)
├── laptop_metafield_mapping_actual.py       # Backend layer (Product Service)  
├── laptop_metafield_mapping.py              # Compatibility layer
├── laptop_metafields.py                     # Schema definitions
├── dedicated_graphics_mapping.py            # Graphics metaobject mapping
└── color_metaobject_mapping.py              # Color metaobject mapping

archive/config/
├── laptop_metafield_mapping_complete.py     # Archived: Large comprehensive mapping
├── laptop_metafield_mapping_full.py         # Archived: Full name mapping 
└── dedicated_graphics_mapping_clean_*.py    # Archived: Timestamped duplicate
```

#### **Technical Achievements**
- **Enhanced Processor Extraction**: Supports Intel, AMD, and Apple processor name formats
- **Self-Contained Enhanced Version**: No external dependencies on archived files
- **Missing Entry Logging**: Comprehensive tracking and cleanup of unmapped values
- **45 Additional Processors**: Added missing processor mappings from archived complete version
- **Backward Compatibility**: All existing imports continue to work seamlessly

#### **Validation Results**
- ✅ All 4 laptop metafield files serve clear, distinct purposes
- ✅ 8/8 processor extraction patterns working correctly
- ✅ Streamlit core functionality validated
- ✅ Backend integration tested and functional  
- ✅ Missing entry logging system operational
- ✅ Zero regressions detected in comprehensive testing

#### **Files Modified**
- **`config/laptop_metafield_mapping_actual.py`** - Added 45 missing processor mappings
- **`config/laptop_metafield_mapping_enhanced.py`** - Fixed processor extraction logic, made self-contained
- **`config/laptop_metafield_mapping.py`** - Created compatibility layer
- **`logs/missing_metaobjects.json`** - Cleaned fixed processor entries (15→11 missing values)

**Status**: ✅ **COMPLETE** - Ready for Phase 3 (Scripts Organization)

---

## Documentation Navigation

- **CLAUDE.md** - AI Agent System Framework and behavior instructions
- **CODEBASE_OVERVIEW.md** - Project context, architecture, and current status
- **TECHNICAL_REFERENCE.md** (this file) - Implementation details and development guides