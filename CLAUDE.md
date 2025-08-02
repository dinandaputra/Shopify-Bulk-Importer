# CLAUDE.md

This file provides **MANDATORY** guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🤖 MANDATORY: AI Agent System Framework

**CRITICAL**: Every new session MUST use the comprehensive AI Agent System. This is not optional.

### 📋 SESSION STARTUP PROTOCOL (MANDATORY)

#### 1. REQUIRED READING - Session Start Checklist
**Before any work begins, agents MUST read these files in order:**

1. **`.ai/context/CODEBASE_STATE.md`** - Current system status and architecture overview
2. **`.ai/context/WORK_LOG.md`** - Recent development work and progress  
3. **`.ai/context/KNOWN_ISSUES.md`** - Active issues and blockers
4. **`.ai/agents/GENERAL_RULES.md`** - Core principles and protected systems
5. **Relevant agent role file** from `.ai/agents/` based on task type:
   - `code-quality-architect.md` - Architecture, testing, performance
   - `shopify-api-developer.md` - API integration, metaobjects  
   - `web-research-specialist.md` - Research, documentation, product specs
   - `product-strategy-advisor.md` - Features, UX, business logic

#### 2. MANDATORY QUALITY GATES
**Every task MUST follow these quality checkpoints:**

1. **PRE-CODING**: Read `.ai/checklists/PRE_CODING.md` before starting work
2. **PRE-COMMIT**: Read `.ai/checklists/PRE_COMMIT.md` before committing
3. **CODE REVIEW**: Use `.ai/checklists/CODE_REVIEW.md` for all reviews

#### 3. REQUIRED PROGRESS LOGGING
**Agents MUST update these files during work:**

- **`.ai/context/WORK_LOG.md`** - Log all significant work completed (MANDATORY - update at end of session)
- **`.ai/context/CODEBASE_STATE.md`** - Update when major changes made
- **`.ai/context/KNOWN_ISSUES.md`** - Log new issues discovered
- **`.ai/context/ARCHITECTURE_DECISIONS.md`** - Document architectural decisions

#### 4. WORKFLOW SELECTION (MANDATORY)
**Choose appropriate workflow based on task type:**

- **New Features**: Follow `.ai/workflows/feature_implementation.md`
- **Bug Fixes**: Follow `.ai/workflows/bug_fixing.md`  
- **Code Changes**: Follow `.ai/workflows/code_review.md`

#### 5. PATTERN APPLICATION (MANDATORY)
**Use established patterns from:**

- **`.ai/patterns/api_patterns.md`** - For Shopify API work
- **`.ai/patterns/ui_patterns.md`** - For Streamlit UI development
- **`.ai/patterns/testing_patterns.md`** - For all testing work

### 🎯 AGENT SELECTION GUIDE (MANDATORY)

**Task Type → Required Agent(s):**

- **Architecture Changes** → Code Quality Architect
- **API Integration** → Shopify API Developer  
- **Technology Research** → Web Research Specialist
- **Product Research** → Web Research Specialist
- **Market Analysis** → Web Research Specialist + Product Strategy Advisor
- **UX/Workflow** → Product Strategy Advisor
- **Bug Investigation** → Domain Specialist + Code Quality Architect
- **Performance Issues** → Code Quality Architect + Shopify API Developer
- **Documentation** → Web Research Specialist + Domain Expert
- **Template Creation** → Web Research Specialist + Product Strategy Advisor

### ⚠️ CRITICAL PROTECTED SYSTEMS (DO NOT MODIFY)

**ONLY Shopify API Developer can modify these systems:**

1. **Variant Metafield System** - `services/shopify_api.py:assign_metafields_to_variants()`
2. **SIM Carrier Variants** - Working 1-5 variant creation logic
3. **GraphQL Mutations** - All working GraphQL metafield operations

### 📚 COMPLETE UTILIZATION GUIDE

**For comprehensive guidance, always reference:**
- **`.ai/AGENT_UTILIZATION_GUIDE.md`** - Complete 1,200+ line guide with examples, scenarios, and best practices

### 🔄 SESSION HANDOFF TEMPLATE (MANDATORY)

**When ending a session, MUST provide:**

```markdown
## Session Handoff Summary
### Agent: [Current Agent Role]
### Work Completed:
- [Task 1] - Status and outcome
- [Task 2] - Status and outcome

### Files Modified:
- [List all changed files]

### Next Steps:
1. [High priority task]
2. [Medium priority task]

### Important Notes:
- [Any constraints or considerations]
- [Dependencies identified]
- [Issues encountered]
```

---

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

## Architecture Overview (Updated - Phase 4 Clean Architecture)

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
- **laptop_metafield_service.py**: Laptop-specific metafield processing (NEW)

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

#### Smartphone Metafields
- Uses actual Shopify metaobject IDs for references
- 5/6 metafields working: product_rank, product_inclusions, ram_size, minus, sim_carriers (via variants)
- Color metafield disabled (requires metafield definition setup in admin)
- Supports both single and list metaobject references with JSON string formatting
- Graceful error handling when metafield creation fails

#### Laptop Metafields (NEW)
- **CPU**: Processor specifications mapped to metaobjects
- **RAM**: Memory size options (4GB, 8GB, 16GB, 32GB, 64GB)
- **GPU**: Graphics card specifications
- **Display**: Screen size and resolution
- **Storage**: SSD/HDD capacity and type
- **OS**: Operating system (Windows 11, Windows 10, etc.)
- **Keyboard**: Layout and backlight options
- **Missing Entry Logging**: Automatic detection and logging of unmapped values

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

### API Integration Status (Updated July 28, 2025) ✅ WORKING IMPLEMENTATION
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

## Recent Progress

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

### 🎉 Phase 1 Codebase Restructuring (COMPLETED - 2025-07-30)
**Status**: Fully Implemented and Tested  
**Goal**: Establish project foundation with comprehensive documentation and organized file structure  

#### ✅ **Completed Features:**
- **Complete Documentation Suite**: README.md, INSTALLATION.md, ARCHITECTURE.md, API_REFERENCE.md, CONTRIBUTING.md, CHANGELOG.md
- **User Guides**: Detailed smartphone and laptop entry guides in docs/guides/
- **Organized Test Structure**: tests/unit/, tests/integration/, tests/e2e/, tests/fixtures/
- **Organized Scripts Structure**: scripts/metaobjects/, scripts/utilities/, scripts/one_time/
- **Root Directory Cleanup**: Reduced from 40+ files to 12 essential files
- **Archive Organization**: Non-essential files moved to archive/ directory
- **Functionality Preservation**: All core functionality tested and working (8/8 tests passed)

#### 🔧 **Technical Implementation:**
- All test files moved from root to appropriate subdirectories
- Utility scripts organized by function (metaobjects, utilities, one-time)
- Import paths verified and working correctly
- Documentation class names corrected (SmartphoneProduct, LaptopProduct)
- Clean project structure following architectural best practices

### 🎉 Phase 2 Configuration Management (COMPLETED - 2025-07-30)
**Status**: Fully Implemented and Tested  
**Goal**: Consolidate duplicate configuration files and create single source of truth  

#### ✅ **Completed Features:**
- **Configuration Consolidation**: Reduced laptop metafield files from 6 → 3 authoritative files
- **Archive Organization**: 3 duplicate files moved to `archive/config/`
- **Import Chain Integrity**: All imports validated and working correctly
- **Processor Regression Fixed**: Resolved missing processor metaobject lookup issue
- **Missing Entries Cleanup**: Cleaned stale entries from logging system
- **Functionality Preservation**: Zero regressions in smartphone or laptop functionality

#### 🔧 **Technical Implementation:**
- Enhanced processor extraction supporting Intel, AMD, and Apple formats
- Self-contained enhanced version with no external dependencies
- 45 additional processors added from archived complete version
- Backward compatibility maintained for all existing imports  

### 🎉 Phase 3 Scripts & Utilities Organization (COMPLETED - 2025-07-30)
**Status**: Fully Implemented and Tested  
**Goal**: Create logical script organization and separate utilities from one-time scripts  

#### ✅ **Completed Features:**
- **Complete Directory Structure**: Created organized scripts/ hierarchy with metaobjects/, utilities/, and one_time/ subdirectories
- **Script Organization**: Moved 4 existing scripts to appropriate categories (create/, query/, debugging/)
- **Comprehensive Documentation**: Created 8 README files covering all script categories with usage examples and best practices
- **Import Path Updates**: Fixed relative import paths for moved scripts, all imports working correctly
- **Testing Verified**: All moved scripts tested and working (verify_black_color_fix.py, laptop metaobject data imports)
- **Future-Ready Structure**: Established patterns for new scripts with clear naming conventions

#### 🔧 **Technical Implementation:**
- Scripts organized by function: metaobjects/, utilities/, one_time/
- Each directory has comprehensive README with usage patterns
- Import paths updated for new locations
- All existing functionality preserved and tested
- Clear naming conventions and safety guidelines established

### 🎉 Laptop Product Entry System (COMPLETED)
**Status**: Fully Implemented and Operational  
**Goal**: Support laptop product entry with intelligent templates and metafield mapping  

#### ✅ **Features Implemented:**
- **Laptop Templates**: Pre-defined templates for popular laptop models (ASUS, Dell, HP, etc.)
- **Smart Component Detection**: Extracts CPU, RAM, GPU, Display, Storage from templates
- **Comprehensive Metafield Mapping**: Maps laptop specifications to Shopify metaobjects
- **Enhanced Logging System**: Tracks missing metaobject entries for future improvements
- **Laptop-Specific Inclusions**: Power adapter, laptop bag, mouse options
- **Automatic Field Population**: Templates auto-fill specifications when selected
- **Image Management**: Full image upload support for laptop products

#### 🔧 **Technical Implementation:**
- **models/laptop.py**: Pydantic model with laptop-specific fields
- **pages/laptop_entry.py**: Streamlit UI for laptop product entry
- **config/laptop_specs.py**: Laptop specifications database
- **config/laptop_metafield_mapping_enhanced.py**: Missing entry detection with logging
- **services/laptop_metafield_service.py**: Metafield processing for laptops

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
- **✅ Phase 2**: Simplified form interface + collections management *(COMPLETE)*  
- **🚧 Phase 3**: Image upload + inline editing features *(READY TO START)*
- **⏳ Phase 4**: Performance optimizations + sales channel integration *(PENDING)*

#### ✅ **Phase 2 Status - COMPLETED (July 23, 2025):**
- **✅ Template Auto-Fill**: Fixed - templates now apply immediately on dropdown selection
- **✅ Form Interface**: Streamlined to 2 required fields (Price, Product Rank) + SIM carriers
- **✅ Auto Collections**: "All Products" + brand collections automatically assigned and editable
- **✅ Session Management**: Enhanced product display with action buttons
- **✅ Template Integration**: Full template extraction with smart inclusion mapping working
- **✅ Form Validation**: Comprehensive validation with clear error messages

#### 🎯 **Phase 3 Ready to Implement:**
**Next Goals**: Image upload functionality and inline session editing for enhanced user workflow

#### CRITICAL: Preserve Current Working Systems
- **DO NOT MODIFY** existing variant metafield system (`services/shopify_api.py:assign_metafields_to_variants()`)
- **Maintain compatibility** with current SIM carrier variant workflow
- **Preserve** all existing API integrations and error handling

### 🎉 Phase 4 Architecture Improvements (COMPLETED - 2025-07-31)
**Status**: Fully Implemented and Tested  
**Goal**: Implement clean architecture patterns and improve testability  

#### ✅ **Completed Features:**
- **Repository Pattern**: Abstract data access with Shopify implementations
- **Domain Layer**: Rich entities with business logic (SmartphoneEntity, LaptopEntity)
- **Dependency Injection**: Lightweight container with constructor injection
- **Error Handling System**: Centralized exception hierarchy and processing
- **Value Objects**: Immutable Price and Metafield objects
- **Enhanced Services**: Backward-compatible services using clean architecture
- **Comprehensive Testing**: Integration tests validating all components
- **Documentation**: Complete architecture guide and ADR

#### 🔧 **Technical Implementation:**
- Clean Architecture with clear layer separation
- Repository Pattern abstracting Shopify API access
- Domain entities with encapsulated business rules
- Value objects for immutable domain concepts
- DI container for service lifecycle management
- Custom exception hierarchy for better error handling
- Enhanced services maintaining backward compatibility

#### 📊 **Architecture Benefits:**
- **Improved Testability**: Domain logic testable in isolation
- **Enhanced Maintainability**: Clear separation of concerns
- **Better Extensibility**: Easy addition of new product types
- **Backward Compatibility**: Zero breaking changes
- **Error Consistency**: Standardized error handling across layers

### 🎉 Phase 5: AI Agent System Implementation (COMPLETED - 2025-08-02)
**Status**: Fully Implemented and Operational
**Goal**: Create structured AI agent workflow system  
**Focus**: Agent framework, context preservation, workflow automation  
**Duration**: 4-5 days (Completed in 1 day)

#### ✅ **Completed Features:**
- **Complete AI Agent Framework**: Created .ai/ directory with 19 files across 7 subdirectories
- **4 Specialized Agent Roles**: Code Quality Architect, Shopify API Developer, Web Research Specialist, Product Strategy Advisor
- **Context Preservation System**: 5 comprehensive state tracking files for seamless session handoffs
- **Workflow Templates**: 3 standardized processes (feature implementation, bug fixing, code review)
- **Pattern Libraries**: 3 code pattern guides (API, UI, testing)
- **Quality Checklists**: 3 mandatory quality gates (PRE_CODING, PRE_COMMIT, CODE_REVIEW)
- **Comprehensive Utilization Guide**: Complete documentation for using the AI agent system
- **Web Research Specialist Enhancement**: Added product specification research capabilities

#### 🔧 **Technical Implementation:**
- **Agent Framework**: Structured role definitions with clear decision authority
- **Context Preservation**: CODEBASE_STATE.md, WORK_LOG.md, ARCHITECTURE_DECISIONS.md, KNOWN_ISSUES.md, TECHNICAL_DEBT.md
- **Multi-Agent Coordination**: Handoff protocols and collaboration guidelines
- **Quality Assurance**: Systematic quality gates and review processes
- **Product Research**: Japan market expertise for smartphones and laptops
- **Template Creation**: Automated product template generation and validation

#### 📊 **System Benefits:**
- **Specialized Expertise**: Each agent focuses on their domain of strength
- **Quality Consistency**: Standardized workflows and mandatory quality gates
- **Context Continuity**: Seamless handoffs between sessions with comprehensive state tracking
- **Risk Mitigation**: Protected systems awareness and quality checkpoints
- **Knowledge Sharing**: Centralized patterns and best practices
- **Product Intelligence**: Market research and competitive analysis capabilities

#### 🎯 **Web Research Specialist Enhancement (NEW):**
- **Product Specification Research**: Comprehensive smartphone and laptop research for Japan market
- **Market Intelligence**: Carrier ecosystems (Docomo, Softbank, AU, Rakuten Mobile), pricing analysis
- **Template Creation**: Automated product template generation with specification validation
- **Research Methodologies**: Structured approach with quality standards and cross-referencing
- **Japan Market Sources**: Official manufacturers, carriers, retailers, review platforms

## Important Files

### Documentation
- **iphone_template_system_prd.md**: iPhone Template System - Complete PRD and implementation plan 📋
- **PROJECT_CONTEXT_SUMMARY.md**: Detailed session history and current status
- **prd.md**: Complete product requirements and user stories

### Core Configuration
- **config/shopify_config.py**: API configuration and validation
- **config/master_data.py**: Centralized product templates and data
- **config/laptop_metafield_mapping_enhanced.py**: Enhanced laptop metafield mapping with logging

### Models
- **models/smartphone.py**: Smartphone data model with metafield definitions
- **models/laptop.py**: Laptop data model with specifications (NEW)

### Services
- **services/product_service.py**: Main product creation logic
- **services/shopify_api.py**: Core Shopify API integration
- **services/laptop_metafield_service.py**: Laptop metafield processing (NEW)

### Pages
- **pages/smartphone_entry.py**: Smartphone product entry UI
- **pages/laptop_entry.py**: Laptop product entry UI (NEW)

### Testing & Scripts
- **verify_variant_metafields.py**: Test script to verify variant metafield linking works ✅
- **test_fixed_variant_linking.py**: Working test for variant-to-metafield automation ✅
- **create_laptop_metaobjects_final.py**: Script to create laptop metaobjects (NEW)
- **laptop_metaobject_data.py**: Laptop metaobject data definitions (NEW)

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

## ✅ Phase 2 Configuration Management - COMPLETED (2025-07-30)

### **Goal Achieved**
Successfully consolidated duplicate configuration files and created single source of truth for each configuration type.

### **Implementation Results**
- **✅ Configuration Consolidation**: Reduced laptop metafield files from 6 → 3 authoritative files
- **✅ Archive Organization**: 3 duplicate files moved to `archive/config/`
- **✅ Import Chain Integrity**: All imports validated and working correctly
- **✅ Processor Regression Fixed**: Resolved missing processor metaobject lookup issue
- **✅ Missing Entries Cleanup**: Cleaned stale entries from logging system
- **✅ Functionality Preserved**: Zero regressions in smartphone or laptop functionality

### **Configuration Structure**
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

### **Technical Achievements**
- **Enhanced Processor Extraction**: Supports Intel, AMD, and Apple processor name formats
- **Self-Contained Enhanced Version**: No external dependencies on archived files
- **Missing Entry Logging**: Comprehensive tracking and cleanup of unmapped values
- **45 Additional Processors**: Added missing processor mappings from archived complete version
- **Backward Compatibility**: All existing imports continue to work seamlessly

### **Validation Results**
- ✅ All 4 laptop metafield files serve clear, distinct purposes
- ✅ 8/8 processor extraction patterns working correctly
- ✅ Streamlit core functionality validated
- ✅ Backend integration tested and functional  
- ✅ Missing entry logging system operational
- ✅ Zero regressions detected in comprehensive testing

### **Files Modified**
- **`config/laptop_metafield_mapping_actual.py`** - Added 45 missing processor mappings
- **`config/laptop_metafield_mapping_enhanced.py`** - Fixed processor extraction logic, made self-contained
- **`config/laptop_metafield_mapping.py`** - Created compatibility layer
- **`logs/missing_metaobjects.json`** - Cleaned fixed processor entries (15→11 missing values)

**Status**: ✅ **COMPLETE** - Ready for Phase 3 (Scripts Organization)

---

## 🚨 FINAL REMINDER: MANDATORY AI AGENT SYSTEM

**Every new session MUST:**

1. **START** by reading the 5 required context files
2. **IDENTIFY** appropriate agent role(s) for the task
3. **FOLLOW** established workflows and patterns
4. **USE** mandatory quality gates (PRE-CODING, PRE-COMMIT, CODE_REVIEW)
5. **LOG** progress in WORK_LOG.md at session end
6. **PROTECT** critical systems (variant metafields, SIM carrier variants)
7. **REFERENCE** `.ai/AGENT_UTILIZATION_GUIDE.md` for comprehensive guidance

**No exceptions. This framework ensures:**
- ✅ Consistent quality and standards
- ✅ Context preservation across sessions  
- ✅ Protection of working systems
- ✅ Efficient collaboration
- ✅ Knowledge sharing and documentation

**The AI Agent System is now the ONLY approved way to work on this project.**