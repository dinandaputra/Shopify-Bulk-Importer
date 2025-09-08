# Changelog

All notable changes to the Shopify Bulk Importer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Phase 5 AI Agent System Implementation (planned)

### Changed
- TBD

### Fixed
- TBD

## [2.0.0] - 2025-07-31

### Added
- **Phase 4 Architecture Improvements completed** - Major architectural overhaul
- **Clean Architecture implementation** with clear separation of concerns
- **Repository Pattern** with abstract interfaces and Shopify implementations
- **Domain Layer** with rich entities (SmartphoneEntity, LaptopEntity) and business logic
- **Value Objects** for Price and Metafield with immutability and validation
- **Dependency Injection Container** with constructor injection and service lifecycle management
- **Centralized Error Handling System** with custom exception hierarchy
- **Enhanced Product Service** maintaining backward compatibility while using new architecture
- **Comprehensive integration tests** for all architectural components
- **Architecture documentation** (ARCHITECTURE.md) with detailed system design
- **Architectural Decision Record** (ADR-001) documenting clean architecture adoption

### Changed
- Restructured codebase following clean architecture principles
- Separated business logic from infrastructure concerns
- Improved testability with dependency injection and repository pattern
- Enhanced error handling with consistent error processing across all layers
- Updated project structure with domain/, repositories/, and infrastructure/ directories

### Fixed
- Import issues in domain services and infrastructure components
- Async/await compatibility between repository interfaces and implementations
- Type hints and proper error handling throughout the system

### Tested
- All 7 functionality tests passing (imports, domain layer, DI, API, services, error handling)
- Successfully created test products with full metafield support
- Verified backward compatibility with existing Streamlit UI
- Confirmed zero regressions in existing functionality

## [1.5.0] - 2025-07-30

### Added
- Phase 3 Scripts & Utilities Organization completed
- Complete scripts directory structure with logical organization
- 8 comprehensive README files for all script categories
- Script organization by function: metaobjects/, utilities/, one_time/
- Usage examples and best practices documentation for each category
- Safety guidelines and naming conventions for script development
- Future-ready structure with clear patterns for new scripts

### Changed
- Moved 4 existing scripts to appropriate organized directories
- Updated import paths for moved scripts (verify_black_color_fix.py)
- Enhanced scripts/README.md with comprehensive usage documentation
- Reorganized debugging scripts into utilities/debugging/ subdirectory

### Fixed  
- Fixed relative import paths for moved scripts
- Ensured all script imports work correctly from new locations
- Verified all moved scripts maintain full functionality

### Tested
- Comprehensive testing of all moved scripts
- Verified smartphone product creation (ID: 8852465123477)
- Verified laptop product creation (ID: 8852466040981)
- Confirmed all metafields working correctly
- Validated Streamlit app functionality unchanged

## [1.4.0] - 2025-07-30

### Added
- Phase 2 Configuration Management completed
- Enhanced processor name extraction for Intel, AMD, and Apple processors
- Compatibility layer for backward compatibility (`laptop_metafield_mapping.py`)
- 45 additional processor mappings restored from archived complete mapping
- Comprehensive validation testing for all configuration changes

### Changed
- Consolidated laptop metafield mapping files from 6 → 3 authoritative files
- Moved duplicate configuration files to `archive/config/` directory
- Enhanced mapping system made self-contained (no external dependencies)
- Missing entries logging system cleaned up (15→11 missing values)

### Fixed
- **CRITICAL**: Processor metaobject lookup regression that caused "Some specifications don't have metaobject entries yet" warnings
- Missing processor mappings including `i7-11370H` and `i7-12700H`
- Broken processor name extraction logic for template integration
- Stale missing entries in logging system persisting after fixes

### Technical Details
- `config/laptop_metafield_mapping_enhanced.py`: UI layer with comprehensive logging
- `config/laptop_metafield_mapping_actual.py`: Backend layer with core GID mappings  
- `config/laptop_metafield_mapping.py`: Compatibility layer redirecting to enhanced version
- All import chains validated and regression tested
- Zero functionality regressions in smartphone or laptop product creation

## [1.3.0] - 2025-07-30

### Added
- **Phase 1 Restructuring Complete**: Comprehensive codebase organization
- Complete project documentation suite:
  - Comprehensive README.md with project overview, features, installation
  - INSTALLATION.md with detailed setup instructions
  - ARCHITECTURE.md documenting system design and components
  - API_REFERENCE.md with complete API documentation  
  - CONTRIBUTING.md with development guidelines
  - CHANGELOG.md tracking project history
- User guides:
  - `docs/guides/smartphone_entry.md` - Complete smartphone entry workflow
  - `docs/guides/laptop_entry.md` - Detailed laptop product creation guide
- Organized test structure:
  - `tests/unit/` - Unit tests for individual components
  - `tests/integration/` - Integration tests with external services
  - `tests/e2e/` - End-to-end workflow tests
  - `tests/fixtures/` - Test data and mocks
- Organized scripts structure:
  - `scripts/metaobjects/` - Shopify metaobject management scripts
  - `scripts/utilities/` - General utility scripts
  - `scripts/one_time/` - One-time migration scripts
- Project archive for non-essential files

### Changed
- **Root directory cleanup**: Reduced from 40+ files to 12 essential files
- **Test organization**: Moved all test files from root to appropriate subdirectories
- **Script organization**: Moved utility scripts to structured directories
- **Documentation structure**: Centralized all documentation under `docs/`
- **File organization**: Clear separation of concerns with proper directory structure

### Fixed
- Import path issues after file reorganization
- Documentation class name references (SmartphoneProduct, LaptopProduct)
- Project structure chaos - now follows clean architecture principles

## [1.2.0] - 2025-07-28

### Added
- Full laptop product entry system with intelligent templates
- Comprehensive laptop metafield mapping for specifications
- Enhanced logging system for missing metaobject entries
- Laptop-specific inclusions (power adapter, laptop bag, mouse)
- Automatic field population from laptop templates
- Support for laptop brands: ASUS, Dell, HP, Lenovo, Apple, MSI, Acer

### Changed
- Updated master_data.py with extensive laptop templates
- Enhanced metafield service to handle laptop specifications

### Fixed
- Laptop color metafield mapping issues
- Missing metaobject detection and logging

## [1.1.0] - 2025-07-22

### Added
- GraphQL metafieldsSet mutation for variant-to-metafield linking
- Automated variant metafield assignment post-product creation
- Verification script for variant metafields
- Test suite for variant linking functionality

### Changed
- Migrated from manual to automated variant metafield assignment
- Updated product creation workflow to include automatic metafield linking

### Fixed
- Variant metafield linking now works without manual intervention
- Each SIM carrier variant correctly linked to its metaobject
- JSON formatting for list.metaobject_reference type

## [1.0.0] - 2025-07-15

### Added
- Initial release of Shopify Bulk Importer
- Streamlit-based web interface
- Smartphone product entry with templates
- Direct Shopify API integration (REST + GraphQL)
- SIM carrier variant support with inventory distribution
- Metafield management for product attributes
- Handle generation with daily counters
- Session management for batch operations
- CSV export fallback functionality
- Real-time data validation with Pydantic

### Features
- iPhone template system with all models from XR/XS to iPhone 16
- Smart inclusion mapping (e.g., "Full set cable" auto-selects related items)
- Automatic 5G detection for compatible iPhone models
- Image upload support with Shopify CDN integration
- Business rule validation
- Error handling and user-friendly messages

### Known Issues
- Color metafield requires manual setup in Shopify admin
- Option-to-metafield linking not yet implemented
- Some metafields require metaobject definitions in store

## [0.9.0] - 2025-06-30 (Beta)

### Added
- Basic product creation functionality
- Simple Streamlit interface
- REST API integration with Shopify

### Changed
- Switched from CSV-based to API-based approach

### Fixed
- Authentication issues with Shopify API
- Product validation errors

## [0.5.0] - 2025-06-01 (Alpha)

### Added
- Initial proof of concept
- CSV generation for manual import
- Basic product data validation

### Known Issues
- Manual process still required
- No direct API integration
- Limited to smartphones only

---

## Version History Summary

- **1.2.0** - Laptop support and enhanced metafield mapping
- **1.1.0** - Automated variant metafield linking
- **1.0.0** - First stable release with smartphone support
- **0.9.0** - Beta with basic API integration
- **0.5.0** - Alpha with CSV generation only

## Upgrade Guide

### From 1.1.0 to 1.2.0
1. No breaking changes
2. Update dependencies: `pip install -r requirements.txt`
3. New laptop templates available immediately
4. Check logs/missing_metaobjects.json for any missing mappings

### From 1.0.0 to 1.1.0
1. Ensure variant-level metafield `custom.sim_carrier` exists in Shopify admin
2. Update ShopifyAPI service to latest version
3. Test variant creation to verify metafield linking works

### From 0.x to 1.0.0
1. Complete reinstall recommended
2. New environment variables required
3. Metafield definitions must be created in Shopify admin
4. Update all import paths due to restructured codebase

## Deprecation Notices

### Version 2.0.0 (Planned)
- CSV export functionality will be moved to a plugin
- Direct file uploads will replace URL-based image handling
- Legacy smartphone model format will be deprecated

### Version 1.3.0 (Upcoming)
- Old laptop metafield mapping files will be consolidated
- Manual variant metafield assignment methods will be removed

## Security Updates

### Version 1.1.0
- Updated requests library to patch security vulnerability
- Enhanced API token handling to prevent exposure

### Version 1.0.0
- Implemented secure environment variable handling
- Added input sanitization for all user inputs

---

For detailed migration guides and breaking changes, see the [Migration Guide](docs/migration.md).