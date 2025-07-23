# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Shopify Bulk Importer is a Streamlit-based web application for MyByte International that helps staff efficiently input used electronics data and create products directly in Shopify via API integration. The app replaces manual CSV import workflows and includes metafield management for product attributes.

## Common Commands

### Running the Application
```bash
streamlit run streamlit_app.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables Required
```bash
export SHOPIFY_ACCESS_TOKEN="your_token_here"
export SHOPIFY_API_KEY="your_api_key_here"
export SHOPIFY_API_SECRET="your_api_secret_here"
export SHOPIFY_SHOP_DOMAIN="your-shop.myshopify.com"
```

## Architecture Overview

### Core Application Structure
- **streamlit_app.py**: Main entry point with navigation and session management
- **pages/**: Streamlit pages for different product categories (currently smartphone_entry.py)
- **models/**: Pydantic models for data validation (smartphone.py)
- **services/**: Business logic and external API integrations
- **config/**: Configuration management including Shopify API settings
- **utils/**: Utility functions like handle generation
- **database/**: Session state and counter management

### Key Services
- **shopify_api.py**: Core Shopify API client with authentication and error handling
- **product_service.py**: Product creation orchestration with metafield management
- **metaobject_service.py**: Handles Shopify metaobject reference mapping
- **export_service.py**: CSV export functionality for fallback workflows
- **validation_service.py**: Business rule validation

### Data Flow
1. User enters product data via Streamlit forms
2. Data validated using Pydantic models with business rules
3. Products created directly in Shopify via REST API
4. Metafields attached using metaobject references
5. Session manages multiple products before batch operations

## Key Implementation Details

### Handle Generation
- Format: `{brand}-{model}-{specs}-{YYMMDD}-{counter}`
- Daily counters reset automatically
- Handles stored in `handle_counter.json` for persistence

### Metafield Management
- Uses actual Shopify metaobject IDs for references
- 5/6 metafields working: product_rank, product_inclusions, ram_size, minus, sim_carriers (via variants)
- Color metafield disabled (requires metafield definition setup in admin)
- Supports both single and list metaobject references with JSON string formatting
- Graceful error handling when metafield creation fails

### Product Configuration
- Products default to draft status (`published: false`)
- Tax disabled (`taxable: false`)
- Inventory tracking enabled (`inventory_management: shopify`)
- Category set to "Mobile & Smart Phones" in product data (not metafield)

### Session Management
- Maximum 10 products per session to prevent memory issues
- Session state persists across page reloads
- Clear session functionality available in sidebar

### SIM Carrier Variants (WORKING)
- Staff select which SIM carrier variants are available per device
- Supports 1-5 variants: SIM Free, Softbank (-), Docomo (-), AU (-), Rakuten Mobile (-)
- Inventory properly tracked and distributed evenly across selected variants
- Creates product options automatically based on selected carriers
- Examples:
  - Product A: ["SIM Free"] → Creates 1 variant with full inventory
  - Product B: ["SIM Free", "Softbank (-)"] → Creates 2 variants with split inventory  
  - Product C: ["Softbank (-)"] → Creates 1 variant with full inventory

## Development Notes

### API Integration Status (Updated July 22, 2025) ✅ WORKING IMPLEMENTATION
- **✅ FULLY WORKING**: Direct variant-to-metafield linking using GraphQL metafieldsSet mutation
- **✅ FIXED**: Product creation with SIM carrier variants using GraphQL productSet
- **✅ FIXED**: Inventory management - products have correct tracked inventory levels
- **✅ WORKING**: 4/6 metafields via API: ram_size, minus (working), product_rank, product_inclusions
- **✅ WORKING**: Each SIM carrier variant individually linked to its specific metaobject
- **✅ WORKING**: Error handling with detailed logging and GraphQL error reporting
- **✅ WORKING**: Rate limiting and proper API authentication

### 🎯 WORKING VARIANT METAFIELD IMPLEMENTATION (DO NOT MODIFY)

#### Shopify Admin Setup Required:
1. **Product-level metafield**: `custom.sim_carriers` (type: list.metaobject_reference)
2. **Variant-level metafield**: `custom.sim_carrier` (type: list.metaobject_reference) ⭐ KEY REQUIREMENT

#### Working Code Structure:
- **services/shopify_api.py**: `assign_metafields_to_variants()` method using metafieldsSet mutation
- **services/product_service.py**: Post-creation variant metafield assignment
- **Test verification**: `verify_variant_metafields.py` script confirms each variant has correct metafield

#### Proven Working Example:
- **Product ID**: 8843114479765
- **URL**: https://jufbtk-ut.myshopify.com/admin/products/8843114479765
- **Status**: All 3 variants successfully linked to individual metaobjects
- **Verification**: GraphQL query confirms metafields exist on each variant

#### Key Technical Details:
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

### 🎯 Next Goal: Option-to-Metafield Linking
- **Current**: Variants linked to metafields ✅
- **Desired**: Option "SIM Carriers" linked to metafield (removes "Connect metafield" button)
- **Challenge**: GraphQL productSet linkedMetafield has API conflicts
- **Approach**: Research option-specific mutations or alternative linking methods

### Data Validation
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

## Recent Progress (July 22, 2025) ✅ VARIANT LINKING SUCCESS

### Issues Fully Resolved
1. **❌→✅ VARIANT METAFIELD LINKING**: Each variant individually linked to specific metaobject via GraphQL metafieldsSet
2. **❌→✅ API AUTOMATION**: No manual clicking required - fully automated variant-to-metafield connection
3. **❌→✅ METAFIELD DEFINITIONS**: Required variant-level metafield definition `custom.sim_carrier` created in admin
4. **❌→✅ JSON FORMATTING**: Correct `list.metaobject_reference` format with JSON array values
5. **❌→✅ VERIFICATION**: GraphQL query confirms all variant metafields successfully created

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

### Store-Specific Configuration (myByte International)
- **Domain**: jufbtk-ut.myshopify.com
- **Currency**: JPY (no decimals)
- **Timezone**: Japan GMT+09:00  
- **API Version**: 2025-07

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

## Current Development Projects

### 🚧 iPhone Template System Enhancement (90% Complete)
**Status**: Phase 1 & 2 Mostly Complete - UI Issue in Progress  
**PRD**: `iphone_template_system_prd.md` - Complete specifications and implementation plan  
**Goal**: Streamline iPhone product entry with smart templates, auto-fill, and 70% time reduction  

#### ✅ **Key Features Implemented:**
- **Smart Templates**: "iPhone 15 Pro Max 256GB [Desert Titanium]" → Auto-generated title with 5G logic
- **Comprehensive iPhone Database**: All models from iPhone XR/XS to iPhone 16 with accurate colors/storage
- **Smart Inclusion Mapping**: "Full set cable" → Auto-selects [Full set cable, Bonus adapter, Bonus softcase, Bonus anti gores]
- **Simplified Form**: Remove Model/Storage fields, streamline to 2 required fields (Price, Rank)
- **Auto Collections**: "All Products" + "iPhone" automatically assigned and editable
- **Image Upload**: Drag & drop with Shopify CDN integration
- **Inline Session Editing**: Click-to-edit products in session list

#### 🚧 **Current Status & Next Steps:**
- **✅ Phase 1**: iPhone specs database + enhanced templates *(COMPLETE)*
- **🚧 Phase 2**: Simplified form interface + collections management *(90% complete - UI issue)*  
- **⏳ Phase 3**: Image upload + inline editing features *(PENDING)*
- **⏳ Phase 4**: Performance optimizations + sales channel integration *(PENDING)*

#### 🚨 **Current Issue:**
**Template Auto-Fill UI**: Templates only apply when pressing Enter in search field, not immediately on dropdown selection. Needs debugging of Streamlit session state and form refresh behavior.

#### CRITICAL: Preserve Current Working Systems
- **DO NOT MODIFY** existing variant metafield system (`services/shopify_api.py:assign_metafields_to_variants()`)
- **Maintain compatibility** with current SIM carrier variant workflow
- **Preserve** all existing API integrations and error handling

## Important Files

- **iphone_template_system_prd.md**: iPhone Template System - Complete PRD and implementation plan 📋
- **PROJECT_CONTEXT_SUMMARY.md**: Detailed session history and current status
- **prd.md**: Complete product requirements and user stories
- **config/shopify_config.py**: API configuration and validation
- **services/product_service.py**: Main product creation logic
- **models/smartphone.py**: Data model with all metafield definitions
- **verify_variant_metafields.py**: Test script to verify variant metafield linking works ✅
- **test_fixed_variant_linking.py**: Working test for variant-to-metafield automation ✅