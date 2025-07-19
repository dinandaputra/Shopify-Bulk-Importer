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
- Color metafields use `shopify` namespace, others use `custom`
- Supports both single and list metaobject references
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

## Development Notes

### API Integration Status
- Direct Shopify product creation is working (services/product_service.py:44)
- Metafield API calls may fail but forms still appear in Shopify admin
- Error handling includes detailed logging for debugging API issues
- Rate limiting implemented (0.5s delay between calls)

### Data Validation
- Required fields: title, price
- Price must be positive
- Multi-select fields (inclusions, minus) supported
- SIM carrier recommendations (warnings, not errors)

### Testing
- Test products via product_service.create_smartphone_product()
- Verify uploads at https://your-shop.myshopify.com/admin/products/
- Check metafield forms appear even if API calls fail

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