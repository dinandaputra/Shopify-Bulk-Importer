# Architecture Decision Records (ADRs)

This document tracks all significant architectural decisions made during the Shopify Bulk Importer development.

## ADR-001: Clean Architecture Implementation

**Date**: 2025-07-31
**Status**: ✅ Accepted and Implemented
**Decision Maker**: Code Quality Architect

### Context
The codebase lacked clear separation of concerns, with business logic mixed with infrastructure code. This made testing difficult and changes risky.

### Decision
Implement Clean Architecture with the following layers:
- **Domain Layer**: Business entities and rules
- **Repository Layer**: Data access abstractions
- **Infrastructure Layer**: External service implementations
- **Application Layer**: Use cases and services

### Consequences
**Positive:**
- Improved testability through dependency injection
- Clear separation of business logic from infrastructure
- Enhanced maintainability and extensibility
- Better error handling consistency

**Negative:**
- Initial complexity increase
- Temporary duplication during migration
- Learning curve for new patterns

### Implementation
- Created domain entities (SmartphoneEntity, LaptopEntity)
- Implemented repository pattern with Shopify implementations
- Added dependency injection container
- Enhanced error handling system

---

## ADR-002: Variant Metafield System Protection

**Date**: 2025-07-28
**Status**: ✅ Accepted and Protected
**Decision Maker**: Shopify API Developer

### Context
The variant metafield linking system was successfully implemented after significant effort. It uses GraphQL metafieldsSet mutations to link individual variants to specific metaobjects.

### Decision
Protect the working variant metafield system from modification:
- `services/shopify_api.py:assign_metafields_to_variants()` method
- GraphQL metafieldsSet mutation implementation
- JSON array format for list.metaobject_reference

### Rationale
- System is working correctly (verified with live products)
- Complex implementation that took significant effort to perfect
- Critical for SIM carrier variant functionality
- Breaking this would impact core product features

### Implementation
- Added protection warnings in documentation
- Created test scripts to verify functionality
- Documented the working implementation pattern

---

## ADR-003: Configuration Consolidation Strategy

**Date**: 2025-07-30
**Status**: ✅ Accepted and Implemented
**Decision Maker**: Code Quality Architect

### Context
Multiple duplicate configuration files caused confusion and maintenance overhead. Four versions of laptop metafield mapping existed with unclear purposes.

### Decision
Consolidate duplicate configurations while maintaining backward compatibility:
- Keep essential files with clear purposes
- Archive duplicate/outdated files
- Create compatibility layers where needed
- Document file purposes clearly

### Implementation
- Reduced laptop metafield files from 6 to 3 authoritative files
- Moved duplicates to `archive/config/`
- Created compatibility layer for imports
- Enhanced processor extraction logic

---

## ADR-004: AI Agent System Architecture

**Date**: 2025-08-02
**Status**: ✅ Accepted and In Progress
**Decision Maker**: Product Strategy Advisor + Code Quality Architect

### Context
Need for structured AI agent workflow to improve development efficiency and maintain consistent quality across sessions.

### Decision
Implement AI Agent System with:
- **Specialized Agent Roles**: 4 distinct agent types with clear responsibilities
- **Context Preservation**: Structured handoff between sessions
- **Workflow Templates**: Standardized processes for common tasks
- **Quality Gates**: Checklists and patterns for consistency

### Agent Roles
1. **Code Quality Architect**: Architecture, testing, performance
2. **Shopify API Developer**: API integration, metaobjects
3. **Web Research Specialist**: Research, documentation
4. **Product Strategy Advisor**: Features, UX, business logic

### Implementation Structure
```
.ai/
├── agents/           # Agent role definitions
├── context/          # State preservation
├── workflows/        # Process templates
├── patterns/         # Code patterns
└── checklists/       # Quality gates
```

### Benefits
- Improved development consistency
- Better context preservation between sessions
- Clear responsibility delegation
- Standardized quality processes

---

## ADR-005: Shopify API Strategy

**Date**: 2025-07-22
**Status**: ✅ Accepted and Implemented
**Decision Maker**: Shopify API Developer

### Context
Need to balance REST and GraphQL usage for optimal performance and functionality.

### Decision
Use hybrid API approach:
- **REST API**: Simple CRUD operations, product creation
- **GraphQL API**: Complex queries, metafield operations, bulk updates
- **Rate Limit Management**: Exponential backoff with monitoring
- **Error Handling**: Standardized error response processing

### Rationale
- REST is simpler for basic operations
- GraphQL is more efficient for complex data fetching
- Proper rate limiting prevents API blocks
- Consistent error handling improves reliability

### Implementation
- Enhanced `services/shopify_api.py` with hybrid approach
- Implemented rate limit monitoring
- Created standardized error handling patterns
- Added comprehensive logging

---

## ADR-006: Metafield Management Strategy

**Date**: 2025-07-25
**Status**: ✅ Accepted and Implemented
**Decision Maker**: Shopify API Developer

### Context
Metafield creation required consistent approach across different product types and complex reference management.

### Decision
Implement tiered metafield strategy:
- **Product-level metafields**: For general product attributes
- **Variant-level metafields**: For variant-specific attributes (e.g., SIM carriers)
- **Metaobject references**: Use GID format with JSON arrays
- **Graceful fallback**: Continue operation if metafield creation fails

### Implementation
- Created separate services for different product types
- Implemented missing entry logging for tracking unmapped values
- Used JSON array format for list.metaobject_reference types
- Added comprehensive error handling

---

## ADR-007: Testing Strategy

**Date**: 2025-07-30
**Status**: ✅ Accepted and Implemented
**Decision Maker**: Code Quality Architect

### Context
Tests were scattered in root directory with unclear organization and insufficient coverage.

### Decision
Implement comprehensive testing strategy:
- **Test Organization**: Separate unit, integration, and E2E tests
- **Coverage Targets**: >80% for critical paths
- **Test Types**: Model validation, service logic, API integration
- **Continuous Testing**: Run tests before commits

### Implementation
```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Component interaction tests
├── e2e/           # Full workflow tests
└── fixtures/      # Test data and mocks
```

### Tools
- **pytest**: Primary testing framework
- **Mock**: For API integration testing
- **Fixtures**: Reusable test data

---

## ADR-008: Dependency Injection Strategy

**Date**: 2025-07-31
**Status**: ✅ Accepted and Implemented
**Decision Maker**: Code Quality Architect

### Context
Tight coupling between components made testing difficult and changes risky.

### Decision
Implement lightweight dependency injection:
- **Constructor Injection**: Primary injection method
- **Interface-based Design**: Abstract dependencies
- **Container Management**: Simple DI container
- **Backward Compatibility**: Gradual migration approach

### Implementation
- Created `infrastructure/container.py`
- Defined repository interfaces
- Implemented constructor injection in services
- Maintained backward compatibility during transition

---

## ADR-009: Laptop vs Smartphone Metafield Type Strategy

**Date**: 2025-08-03
**Status**: ✅ Accepted and Implemented
**Decision Maker**: Shopify API Developer

### Context
Critical metafield type mismatches were discovered for laptop products:
1. Color metafield failing with `'metaobject_reference' must be consistent with the definition's type: 'list.metaobject_reference'`
2. VGA and Graphics metafields not populating correctly due to data mapping issues

### Problem Analysis
- **Smartphones**: Use color as a variant option (single metaobject_reference)
- **Laptops**: Use color only as product description (requires list.metaobject_reference)
- **GPU Fields**: Confusion between integrated vs dedicated graphics mapping

### Decision
Implement product-specific metafield type handling:
- **Smartphone Color**: Maintain single `metaobject_reference` for variant usage (PROTECTED - DO NOT CHANGE)
- **Laptop Color**: Use `list.metaobject_reference` with JSON array format for product-level metafields
- **GPU Field Separation**: Distinct handling for VGA (dedicated) vs Graphics (integrated)
- **Enhanced Lookup**: Support abbreviated GPU names (RTX 4060 → NVIDIA GeForce RTX 4060 8GB)

### Implementation Details

#### Color Metafield Type Fix
```python
# Laptop-specific color handling
if field_name == 'color':
    gid = get_metaobject_gid(field_name, value)
    if gid:
        metafields[config['key']] = {
            'namespace': config['namespace'],
            'key': config['key'],
            'type': 'list.metaobject_reference',  # Array for laptops
            'value': json.dumps([gid])  # JSON array format
        }
```

#### GPU Field Separation
```python
# Data mapping correction
laptop_data = {
    'graphics': laptop.integrated_graphics,  # 03 Graphics metafield
    'vga': laptop.gpu,                       # 06 VGA metafield
}
```

#### Enhanced VGA Lookup
```python
# Handle abbreviated GPU names
if value and 'RTX' in value and 'NVIDIA' not in value:
    for full_name, gid in DEDICATED_GRAPHICS_MAPPING.items():
        if value in full_name:
            return gid
```

### Rationale
- **Product Specificity**: Different product types have different metafield requirements
- **Shopify Compliance**: Must match exact metafield definition types in Shopify
- **Data Integrity**: Separate fields for integrated vs dedicated graphics prevent confusion
- **User Experience**: Enhanced lookup supports abbreviated names commonly used in templates

### Consequences
**Positive:**
- All laptop metafields now populate correctly (color, VGA, graphics)
- Clear separation between smartphone and laptop metafield handling
- Enhanced GPU lookup supports user-friendly abbreviated names
- Smartphone functionality completely protected and untouched

**Negative:**
- Increased complexity in metafield handling logic
- Product-specific code paths require careful maintenance
- Different type handling for same metafield name across products

### Files Modified
- `config/laptop_metafield_mapping_actual.py`: Color type and VGA lookup fixes
- `config/laptop_metafield_mapping_enhanced.py`: Abbreviated GPU name handling  
- `services/product_service.py`: GPU field mapping corrections

### Testing Results
- ✅ Color metafield: `["gid://shopify/Metaobject/131501392021"]` (JSON array)
- ✅ VGA metafield: `gid://shopify/Metaobject/131302916245` (RTX 4060)
- ✅ Graphics metafield: `gid://shopify/Metaobject/117180858517` (Intel UHD Graphics)
- ✅ Smartphone verification: Color logic completely untouched

---

## Decision Review Process

### Monthly Review
- Review all active ADRs
- Assess implementation success
- Update status where needed
- Archive superseded decisions

### Decision Criteria
1. **Impact**: How significant is the change?
2. **Reversibility**: Can we easily revert if needed?
3. **Complexity**: Implementation and maintenance effort
4. **Risk**: Potential for breaking existing functionality
5. **Value**: Business and technical benefits

### Documentation Standards
Each ADR must include:
- **Context**: Why the decision was needed
- **Decision**: What was decided
- **Rationale**: Why this approach was chosen
- **Consequences**: Expected positive and negative outcomes
- **Implementation**: How it was executed
- **Status**: Current implementation status

---

**Last Updated**: 2025-08-03
**Next Review**: 2025-09-03
**Document Owner**: Code Quality Architect