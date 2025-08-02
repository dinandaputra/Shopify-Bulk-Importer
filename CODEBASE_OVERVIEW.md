# Codebase Overview

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

## Architecture Overview (Phase 4 Clean Architecture)

### Clean Architecture Structure
Following Clean Architecture principles with clear separation of concerns:

#### Domain Layer (`domain/`)
- **entities/**: Rich domain entities with business logic
  - **product.py**: Abstract product base class
  - **smartphone.py**: Smartphone entity with business rules
  - **laptop.py**: Laptop entity with business rules
- **services/**: Domain services for complex business logic
  - **product_domain_service.py**: Product-related business operations
  - **metafield_domain_service.py**: Metafield mapping and validation
- **value_objects/**: Immutable domain concepts
  - **price.py**: Price with currency handling
  - **metafield.py**: Metafield data validation

#### Infrastructure Layer (`infrastructure/`)
- **container.py**: Dependency injection container
- **exceptions.py**: Custom exception hierarchy
- **error_handler.py**: Centralized error processing
- **mappers/**: Data conversion utilities

#### Repository Layer (`repositories/`)
- **interfaces/**: Abstract repository contracts
- **shopify_product_repository.py**: Shopify product data access
- **shopify_metaobject_repository.py**: Shopify metaobject operations

#### Application Layer
- **services/enhanced_product_service.py**: Clean architecture service with backward compatibility
- **Original services/**: Legacy services (maintained for compatibility)

#### Presentation Layer
- **streamlit_app.py**: Main entry point with navigation and session management
- **pages/**: Streamlit pages for different product categories
- **models/**: Pydantic models (maintained for backward compatibility)

### Key Services
- **shopify_api.py**: Core Shopify API client with authentication and error handling
- **product_service.py**: Product creation orchestration with metafield management
- **metaobject_service.py**: Handles Shopify metaobject reference mapping
- **export_service.py**: CSV export functionality for fallback workflows
- **validation_service.py**: Business rule validation
- **image_service.py**: Image upload and management with Shopify CDN
- **laptop_metafield_service.py**: Laptop-specific metafield processing

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

### Product Configuration
- Products default to draft status (`published: false`)
- Tax disabled (`taxable: false`)
- Inventory tracking enabled (`inventory_management: shopify`)
- Category set to "Mobile & Smart Phones" in product data (not metafield)

### Session Management
- Maximum 10 products per session to prevent memory issues
- Session state persists across page reloads
- Clear session functionality available in sidebar

### Store Configuration (myByte International)
- **Domain**: jufbtk-ut.myshopify.com
- **Currency**: JPY (no decimals)
- **Timezone**: Japan GMT+09:00  
- **API Version**: 2025-07

## Product Support

### Smartphone Products
- 5/6 metafields working: product_rank, product_inclusions, ram_size, minus, sim_carriers (via variants)
- SIM carrier variants: Supports 1-5 variants (SIM Free, Softbank, Docomo, AU, Rakuten Mobile)
- Inventory properly tracked and distributed across selected variants
- iPhone template system with smart auto-fill capabilities

### Laptop Products
- Full laptop product entry system with templates
- Comprehensive metafield mapping for CPU, RAM, GPU, Display, Storage, OS, Keyboard
- Enhanced logging system for missing metaobject entries
- Smart component detection from templates

## Important Files

### Core Configuration
- **config/shopify_config.py**: API configuration and validation
- **config/master_data.py**: Centralized product templates and data
- **config/laptop_metafield_mapping_enhanced.py**: Enhanced laptop metafield mapping with logging

### Models
- **models/smartphone.py**: Smartphone data model with metafield definitions
- **models/laptop.py**: Laptop data model with specifications

### Services
- **services/product_service.py**: Main product creation logic
- **services/shopify_api.py**: Core Shopify API integration
- **services/laptop_metafield_service.py**: Laptop metafield processing

### Pages
- **pages/smartphone_entry.py**: Smartphone product entry UI
- **pages/laptop_entry.py**: Laptop product entry UI

### Testing & Scripts
- **verify_variant_metafields.py**: Test script to verify variant metafield linking works ✅
- **test_fixed_variant_linking.py**: Working test for variant-to-metafield automation ✅
- **scripts/**: Organized by function (metaobjects/, utilities/, one_time/)

## Current Development Status

### ✅ Completed Systems
- **Phase 1**: Codebase restructuring and documentation
- **Phase 2**: Configuration management consolidation
- **Phase 3**: Scripts and utilities organization
- **Phase 4**: Clean architecture implementation
- **Phase 5**: AI Agent System implementation
- **Laptop Product Entry**: Full system with templates and metafield mapping
- **Variant Metafield Linking**: Working GraphQL metafieldsSet mutation

### 🚧 In Progress
- **iPhone Template System Enhancement**: 90% complete, Phase 3 ready
- **Option-to-Metafield Linking**: Research alternative approaches

### 🎯 Next Goals
- Image upload functionality for iPhone templates
- Inline session editing capabilities
- Performance optimizations

## Documentation References

For detailed technical implementation, see **TECHNICAL_REFERENCE.md**
For AI agent instructions, see **CLAUDE.md**