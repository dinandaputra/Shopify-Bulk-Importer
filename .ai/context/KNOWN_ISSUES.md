# Known Issues & Technical Debt

This document tracks all known issues, bugs, technical debt, and areas needing attention in the Shopify Bulk Importer project.

**Last Updated**: 2025-08-02
**Review Frequency**: Weekly
**Next Review**: 2025-08-09

## Critical Issues (High Priority) 🔴

### None Currently Identified ✅
All critical functionality is working as expected.

---

## Minor Issues (Medium Priority) 🟡

### Issue #1: Color Metafield Disabled
**Status**: 🟡 Known Limitation
**Impact**: Medium - One metafield type unavailable
**Affected Components**: Smartphone and laptop product creation

#### Description
Color metafield is currently disabled in smartphone and laptop product creation due to required metafield definition setup in Shopify Admin.

#### Technical Details
- **File**: `config/smartphone_metafield_mapping.py`
- **Workaround**: Color metafield creation commented out
- **Root Cause**: Requires manual metafield definition creation in Shopify Admin

#### Resolution Plan
1. Create color metafield definition in Shopify Admin
2. Test metafield creation functionality
3. Re-enable color metafield in mapping
4. Update documentation

**Assigned To**: Shopify API Developer
**Target Timeline**: Next quarter

### Issue #2: Option-to-Metafield Linking Missing
**Status**: 🟡 Enhancement Opportunity
**Impact**: Medium - Manual "Connect metafield" button visible in admin
**Affected Components**: SIM carrier product options

#### Description
While variant-to-metafield linking works perfectly, the option "SIM Carriers" is not automatically linked to its metafield, requiring manual connection in admin.

#### Technical Details
- **Current State**: Variants linked to metafields ✅
- **Missing**: Option linked to metafield
- **Impact**: "Connect metafield" button appears in admin UI
- **Challenge**: GraphQL productSet linkedMetafield has API conflicts

#### Resolution Plan
1. Research option-specific GraphQL mutations
2. Investigate alternative linking methods
3. Test option metafield linking
4. Implement if viable solution found

**Assigned To**: Shopify API Developer
**Target Timeline**: Future enhancement

### Issue #3: Missing Metaobject Entries
**Status**: 🟡 Data Completeness
**Impact**: Low - Graceful degradation for unmapped values
**Affected Components**: Laptop metafield mapping

#### Description
11 laptop specification values are not mapped to Shopify metaobjects, causing graceful failures during metafield creation.

#### Current Missing Entries
```json
{
  "processor": ["Intel Core i3-1115G4 (4 CPUs), ~3.0GHz", "AMD Ryzen 5 5500U (12 CPUs), ~2.1GHz"],
  "graphics": ["AMD Radeon Graphics"],
  "display": ["13.3-inch FHD", "14-inch FHD"],
  "storage": ["256GB SSD", "1TB HDD"],
  "operating_system": ["Windows 10 Home", "Windows 11 Pro"],
  "keyboard_layout": ["JIS", "AZERTY"]
}
```

**Note**: ✅ **Keyboard Backlight entries resolved** - All keyboard backlight values (RGB, Yes, No, White, Blue, Green, Red) now have complete metaobject mappings and working pipeline.

#### Resolution Plan
1. Create missing metaobjects in Shopify Admin
2. Update metafield mapping configurations
3. Test metafield creation for missing entries
4. Clear resolved entries from missing log

**Assigned To**: Shopify API Developer
**Target Timeline**: Next sprint

---

## Technical Debt (Low Priority) 🟢

### Debt #1: Legacy Service Compatibility
**Status**: 🟢 Managed Technical Debt
**Impact**: Low - Code maintenance overhead
**Affected Components**: Service layer architecture

#### Description
Maintaining both legacy services and new clean architecture services during transition period creates some code duplication.

#### Technical Details
- **Legacy Services**: Original service implementations
- **Enhanced Services**: Clean architecture implementations
- **Compatibility Layer**: Wrapper functions for backward compatibility
- **Migration**: Gradual transition approach

#### Management Strategy
- All new features use enhanced services
- Legacy services maintained for existing functionality
- Gradual migration of existing code to enhanced services
- Full migration planned for Phase 6

**Timeline**: Phase 6 (Testing & QA)

### Debt #2: Test Coverage Gaps
**Status**: 🟢 Continuous Improvement
**Impact**: Low - Risk mitigation
**Affected Components**: Testing infrastructure

#### Description
While core functionality is well-tested, some edge cases and new architecture components need expanded test coverage.

#### Current Coverage
- **Unit Tests**: 8/8 passing ✅
- **Integration Tests**: Core API flows covered ✅
- **E2E Tests**: Manual workflow validation ✅
- **Performance Tests**: Basic profiling only

#### Improvement Plan
- Expand unit test coverage for new domain entities
- Add integration tests for enhanced services
- Implement automated E2E testing
- Add performance benchmarking

**Target**: >80% coverage for critical paths
**Timeline**: Phase 6 (Testing & QA)

### Debt #3: Documentation Drift
**Status**: 🟢 Ongoing Maintenance
**Impact**: Low - Developer experience
**Affected Components**: Internal documentation

#### Description
Some internal documentation may lag behind rapid development changes, particularly for newly implemented clean architecture.

#### Areas Needing Attention
- Internal API documentation for enhanced services
- Code comments in complex business logic
- Developer onboarding for new architecture
- Troubleshooting guides for new patterns

#### Management Strategy
- Weekly documentation review and updates
- Documentation updates included in Definition of Done
- Automated documentation generation where possible
- Regular documentation audits

**Timeline**: Ongoing maintenance

---

## Monitoring & Prevention

### Issue Tracking Process

#### Detection Methods
1. **Automated Testing**: Continuous test suite execution
2. **Error Logging**: Comprehensive error tracking and analysis
3. **Performance Monitoring**: Response time and resource usage tracking
4. **User Feedback**: Regular check-ins with MyByte International staff
5. **Code Reviews**: Quality gates before changes

#### Escalation Criteria
- **Critical**: System unavailable or data corruption
- **High**: Core functionality broken or security issue
- **Medium**: Feature degradation or user workflow impact
- **Low**: Minor bugs or enhancement opportunities

#### Resolution SLA
- **Critical**: Immediate response, 4-hour resolution target
- **High**: Same-day response, 24-hour resolution target
- **Medium**: 3-day response, 1-week resolution target
- **Low**: Weekly review, quarterly resolution target

### Prevention Strategies

#### Code Quality Gates
- Comprehensive test coverage before deployment
- Code review for all changes
- Performance benchmarking for new features
- Security review for API changes

#### Monitoring Systems
- Error rate monitoring with alerts
- Performance degradation detection
- API rate limit monitoring
- User workflow completion tracking

#### Knowledge Management
- Document all issues and resolutions
- Maintain troubleshooting runbooks
- Share lessons learned across team
- Regular postmortem sessions for major issues

---

## Historical Issues (Resolved) ✅

### Resolved #1: Variant Metafield Linking Failure
**Resolved**: 2025-07-28
**Resolution**: Implemented GraphQL metafieldsSet mutation with proper JSON formatting

#### Original Problem
Variants were not being automatically linked to their metafields, requiring manual admin intervention.

#### Solution Implemented
- Used GraphQL metafieldsSet mutation instead of REST API
- Implemented proper JSON array format for list.metaobject_reference
- Added comprehensive error handling and logging
- Created test scripts to verify functionality

#### Prevention Measures
- Protected working implementation from modification
- Created comprehensive test suite
- Documented implementation patterns
- Added monitoring for variant metafield creation

### Resolved #2: Configuration File Chaos
**Resolved**: 2025-07-30
**Resolution**: Consolidated duplicate files and created single source of truth

#### Original Problem
Multiple versions of configuration files caused confusion and maintenance overhead.

#### Solution Implemented
- Analyzed all duplicate files and identified authoritative versions
- Moved outdated files to archive directory
- Created compatibility layers for backward compatibility
- Enhanced processor extraction logic
- Documented file purposes clearly

#### Prevention Measures
- Established clear naming conventions
- Created file purpose documentation
- Implemented regular configuration audits
- Added guidelines for new configuration files

### Resolved #3: Root Directory Clutter
**Resolved**: 2025-07-30
**Resolution**: Organized files into logical directory structure

#### Original Problem
40+ files in root directory made navigation and maintenance difficult.

#### Solution Implemented
- Created organized directory structure (tests/, scripts/, docs/)
- Moved all files to appropriate locations
- Updated import paths and verified functionality
- Created comprehensive documentation structure

#### Prevention Measures
- Established clear directory organization guidelines
- Added file placement rules to coding standards
- Regular directory structure audits
- Clear guidelines for new file creation

### Resolved #4: Keyboard Backlight Metafield System Missing
**Resolved**: 2025-08-03
**Resolution**: Complete UI field and metaobject system implementation with data pipeline fix

#### Original Problem
- "Keyboard Backlight" field missing from laptop entry UI despite backend infrastructure
- "11 Keyboard Backlight" metafield showing empty in Shopify products
- "Keyboard Backlight: RGB" missing metaobject entry warnings blocking uploads

#### Solution Implemented
**Multi-Agent Resolution:**
- **UX Design**: Added "Keyboard Backlight" text input field to laptop entry UI with template integration
- **Shopify API**: Created 4 missing keyboard backlight color metaobjects (White/Blue/Green/Red)
- **Critical Fix**: Added missing `keyboard_backlight` field to laptop_data dictionary in services/product_service.py
- **Complete Mapping**: Fixed get_keyboard_backlight_metafield_gid() function and added comprehensive value mapping

#### Technical Changes
- Files: pages/laptop_entry.py, config/laptop_metafield_mapping_*.py, services/product_service.py
- Metaobjects: 4 new keyboard backlight entries created in Shopify with GID mappings
- Pipeline: Complete UI → laptop model → metafield conversion → Shopify "11 Keyboard Backlight" metafield

#### Prevention Measures
- Complete pipeline testing for all template values (RGB/Yes/No/White/Blue/Green/Red)
- Protected systems verification (smartphone logic untouched)
- Data flow validation from UI input to final Shopify metafield
- Comprehensive commit with multi-agent collaboration documentation

---

**Document Maintainer**: All AI Agents (Collaborative)
**Update Process**: Add new issues as discovered, update resolution status
**Review Process**: Weekly review of all open issues and technical debt