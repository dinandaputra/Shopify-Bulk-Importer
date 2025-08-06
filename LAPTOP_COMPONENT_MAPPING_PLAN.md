# LAPTOP COMPONENT MAPPING ANALYSIS & GID RESOLUTION PLAN

## Overview
Comprehensive plan untuk menganalisis spesifikasi laptop di `data/products/laptops/`, mencocokkan dengan mapping komponen di `data/metaobjects/`, mengidentifikasi komponen yang belum dimapping, dan melakukan GID resolution untuk komponen yang missing.

## Phase 1: Component Analysis & Unmapped Identification (1-2 hari)

### 1.1 Create Analysis Script
- **File**: `scripts/analysis/analyze_laptop_components.py`
- **Purpose**: Parse semua file laptop JSON dan extract komponen specs
- **Output**: `data/analysis/unmapped_components.json`

### 1.2 Component Extraction Logic
```python
# Extract components dari setiap laptop configuration:
- CPU/Processor dari field "cpu"
- VGA dari field "vga" 
- GPU dari field "gpu"
- Display dari field "display"
- Storage dari field "storage"
- OS dari field "os"
- Keyboard Layout dari field "keyboard_layout"
- Keyboard Backlight dari field "keyboard_backlight"
```

### 1.3 Cross-Reference dengan Metaobjects
- Compare extracted components dengan existing mappings di:
  - `data/metaobjects/processors.json`
  - `data/metaobjects/vga.json`
  - `data/metaobjects/graphics.json`
  - `data/metaobjects/displays.json`
  - `data/metaobjects/storage.json`
  - `data/metaobjects/os.json`
  - `data/metaobjects/keyboard_layouts.json`
  - `data/metaobjects/keyboard_backlights.json`

### 1.4 Generate Unmapped Report
- **Output**: `data/analysis/unmapped_components.md`
- **Format**: Categorized list dengan contoh:
```markdown
## Missing VGA Components
- NVIDIA GeForce RTX 4060 8GB (found in: ASUS TUF F15 FX507ZV4)
- AMD Radeon RX 6600M (found in: Dell G15 5520)

## Missing Processors
- Intel Core i7-12700H (16 CPUs), ~2.3GHz (found in: ASUS TUF F15 FX507ZV4)
```

## Phase 2: GID Resolution & Mapping Updates (2-3 hari)

### 2.1 Create GID Resolution Script
- **File**: `scripts/metaobjects/resolve_missing_gids.py`
- **Purpose**: Query Shopify untuk setiap unmapped component
- **Reference**: Gunakan screenshots di `scripts/metaobjects/` folder sebagai panduan struktur metaobject

### 2.2 GraphQL Query Implementation
```python
# Untuk setiap missing component:
# 1. Query berdasarkan type (vga, processor, etc.)
# 2. Search by label/display_name
# 3. Extract GID jika ditemukan
# 4. Update corresponding JSON file
```

### 2.3 Automated Mapping Updates
- Update file JSON di `data/metaobjects/` dengan GID baru
- Create backup sebelum update
- Generate summary report

### 2.4 Handle Missing Shopify Entries
- **Output**: `data/analysis/missing_shopify_entries.md`
- List komponen yang tidak ditemukan di Shopify untuk manual creation

## Phase 3: Comprehensive Testing & Validation (2-3 hari)

### 3.1 Component Mapping Validation
- **Script**: `scripts/testing/validate_component_mapping.py`
- **Tests**:
  1. Verify semua laptop components ada mapping
  2. Validate GID format dan accessibility
  3. Check for duplicate mappings

### 3.2 Shopify Entry Verification
- **Script**: `scripts/testing/verify_shopify_entries.py`
- **Purpose**: Query Shopify untuk verify semua GID masih valid
- **Output**: `data/analysis/invalid_gids_report.md`

### 3.3 Product Creation Testing
- **Script**: `scripts/testing/test_laptop_product_creation.py`
- **Tests**:
  1. Create test laptop product dengan complete specifications
  2. Verify semua metafield terisi correctly
  3. Validate product visibility di Shopify admin
  4. Test dengan berbagai laptop models (ASUS, Dell, HP, Lenovo, MSI)

### 3.4 End-to-End Integration Test
- Test complete workflow dari laptop selection → product creation → Shopify upload
- Verify UI dropdown populations
- Check error handling untuk missing components

## File Structure Output

```
data/analysis/
├── unmapped_components.json          # Raw data unmapped components
├── unmapped_components.md            # Human-readable report
├── missing_shopify_entries.md        # Components tidak ada di Shopify
├── invalid_gids_report.md            # GID yang tidak valid
└── component_mapping_summary.md      # Final summary report

scripts/analysis/
├── analyze_laptop_components.py      # Phase 1 main script
└── generate_mapping_report.py        # Report generation

scripts/metaobjects/
├── resolve_missing_gids.py           # Phase 2 main script
└── batch_update_mappings.py          # Batch update JSON files

scripts/testing/
├── validate_component_mapping.py     # Phase 3 validation
├── verify_shopify_entries.py         # GID verification  
└── test_laptop_product_creation.py   # E2E testing
```

## Example Component Analysis Flow

### Step 1: Extract dari Laptop JSON
```json
// data/products/laptops/asus.json
{
  "ASUS TUF F15 FX507ZV4": {
    "configurations": [{
      "cpu": "Intel Core i7-12700H (16 CPUs), ~2.3GHz",
      "vga": "NVIDIA GeForce RTX 4060 8GB",
      "gpu": "Intel Iris Xe Graphics",
      "display": "15-inch FHD (144Hz)",
      "storage": "512GB SSD",
      "os": "Windows 11",
      "keyboard_layout": "US - International Keyboard", 
      "keyboard_backlight": "RGB Backlight"
    }]
  }
}
```

### Step 2: Check Against Existing Mappings
```json
// data/metaobjects/vga.json (current)
{
  "NVIDIA GeForce RTX 4050 6GB": "gid://shopify/Metaobject/117180891285",
  "NVIDIA GeForce RTX 3060 6GB": "gid://shopify/Metaobject/117533343893"
  // Missing: "NVIDIA GeForce RTX 4060 8GB"
}
```

### Step 3: Generate Unmapped Report
```markdown
## Missing VGA Components
- NVIDIA GeForce RTX 4060 8GB
  - Found in: ASUS TUF F15 FX507ZV4
  - Frequency: 3 laptop models
  - Action: Query Shopify for GID
```

## GraphQL Query Examples

### Query Metaobjects by Type
```graphql
query getVGAMetaobjects($type: String!, $first: Int!) {
  metaobjects(type: $type, first: $first) {
    nodes {
      id
      handle
      displayName
      fields {
        key
        value
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Search Specific Component
```graphql
query searchComponent($type: String!, $query: String!) {
  metaobjects(type: $type, first: 10, query: $query) {
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
  }
}
```

## Success Criteria

### Phase 1 Complete When:
- ✅ All laptop specs extracted dan categorized
- ✅ Unmapped components identified dan documented
- ✅ Clear list of missing mappings generated

### Phase 2 Complete When:
- ✅ All resolvable GIDs fetched dari Shopify
- ✅ JSON mapping files updated dengan new GIDs
- ✅ Missing Shopify entries documented untuk manual action

### Phase 3 Complete When:
- ✅ 100% laptop components have valid GID mappings
- ✅ Test product creation succeeds dengan complete metafields
- ✅ All integration tests passing
- ✅ Documentation updated dengan new mappings

## Risk Mitigation
- **Backup**: Create backup semua JSON files sebelum update
- **Rollback**: Implement rollback mechanism jika ada error
- **Rate Limiting**: Handle Shopify API rate limits dengan proper delays
- **Error Handling**: Graceful handling untuk network/API errors

## Reference Files
- Screenshots: `scripts/metaobjects/` folder
- Current mappings: `data/metaobjects/*.json`
- Laptop data: `data/products/laptops/*.json`
- Project context: `CODEBASE_STATE.md`, `WORK_LOG.md`

## Implementation Notes
- Use existing `ShopifyAPIClient` from `services/shopify_api.py`
- Follow project patterns dari `services/metaobject_service.py`
- Maintain backward compatibility dengan existing mapping system
- Log all changes untuk audit trail