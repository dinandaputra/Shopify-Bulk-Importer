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

### API Integration Status (Updated July 2025)
- **✅ FIXED**: Direct Shopify product creation using GraphQL productSet mutation
- **✅ FIXED**: SIM carrier variants with proper inventory tracking and distribution
- **✅ FIXED**: Inventory management - products now have correct tracked inventory levels
- **✅ WORKING**: 4/6 metafields via API: ram_size, minus (working), product_rank, product_inclusions (mapping needs update)
- **⚠️ PARTIAL**: SIM carriers create variants but metafield linking needs Shopify admin setup
- **❌ DISABLED**: Color metafield (requires metafield definition setup in admin)
- **✅ WORKING**: Error handling with detailed logging and GraphQL error reporting
- **✅ WORKING**: Rate limiting and proper API authentication

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

## Recent Progress (July 20, 2025)

### Issues Fixed
1. **❌→✅ INVENTORY TRACKING**: Fixed major inventory issue where products had 0 inventory and weren't tracked
2. **❌→✅ VARIANT CREATION**: SIM carrier variants now create properly with correct inventory distribution  
3. **❌→✅ GRAPHQL IMPLEMENTATION**: Migrated from broken REST approach to working GraphQL productSet
4. **❌→✅ LOCATION HANDLING**: Automatic primary location detection for inventory management
5. **❌→✅ TRACKING STATUS**: Products now have `tracked: true` for proper inventory management

### Current Status
- **WORKING**: Core SIM carrier variant functionality with proper inventory
- **WORKING**: Product creation, variants, inventory tracking, basic metafields
- **PARTIAL**: Metafield linking (variants work but not connected to metafields yet - requires admin setup)
- **NEXT**: Complete metafield linking would require Shopify admin metafield definition configuration

### Key Files Modified
- `services/product_service.py`: Complete rewrite of product creation using GraphQL
- `services/shopify_api.py`: Added GraphQL productSet support and inventory methods  
- Cleaned up test files and unused implementations

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

## Important Files

- **PROJECT_CONTEXT_SUMMARY.md**: Detailed session history and current status
- **prd.md**: Complete product requirements and user stories
- **config/shopify_config.py**: API configuration and validation
- **services/product_service.py**: Main product creation logic
- **models/smartphone.py**: Data model with all metafield definitions