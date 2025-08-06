# Testing Scripts - Phase 3: Comprehensive Testing & Validation

This directory contains the comprehensive testing suite for Phase 3 of the Laptop Component Mapping Plan. These scripts validate the entire laptop component mapping system to ensure production readiness.

## 📋 Overview

Phase 3 testing provides complete validation of:
- Component mapping completeness and accuracy
- Shopify GID validity and accessibility  
- Product creation workflows with metafields
- End-to-end integration testing
- Error handling and system reliability

## 🧪 Test Scripts

### 1. Component Mapping Validation
**File**: `validate_component_mapping.py`
**Purpose**: Validates all laptop components have proper metaobject mappings

**Features**:
- Extracts all components from laptop data files
- Validates GID format and accessibility
- Checks for duplicate mappings
- Generates validation score and comprehensive report

**Usage**:
```bash
python validate_component_mapping.py
```

**Outputs**:
- `data/analysis/component_mapping_validation.json`
- `data/analysis/component_mapping_validation.md`

### 2. Shopify Entry Verification
**File**: `verify_shopify_entries.py`  
**Purpose**: Queries Shopify to verify all GIDs are still valid

**Features**:
- GraphQL queries to verify GID existence
- Detects orphaned or deleted metaobjects
- Validates GID accessibility and structure
- Generates invalid GIDs report

**Usage**:
```bash
python verify_shopify_entries.py
```

**Outputs**:
- `data/analysis/shopify_gid_verification.json`
- `data/analysis/invalid_gids_report.md`

### 3. Product Creation Testing
**File**: `test_laptop_product_creation.py`
**Purpose**: Tests complete laptop product creation with metafields

**Features**:
- Tests with various laptop models (ASUS, Dell, HP, Lenovo, MSI)
- Validates metafield population and accuracy
- Dry run and live testing modes
- Cleanup functionality for test products

**Usage**:
```bash
# Dry run (recommended)
python test_laptop_product_creation.py

# Live test (creates actual products)
python test_laptop_product_creation.py --live

# Live test with cleanup
python test_laptop_product_creation.py --live --cleanup
```

**Outputs**:
- `data/analysis/laptop_product_creation_test.json`
- `data/analysis/laptop_product_creation_test.md`

### 4. End-to-End Integration Testing
**File**: `test_e2e_integration.py`
**Purpose**: Tests complete workflow from selection to Shopify upload

**Features**:
- Template selection workflow testing
- Dropdown population validation
- Metafield mapping workflow verification
- Product creation workflow testing
- Error handling and edge cases
- Data integrity validation
- Performance testing

**Usage**:
```bash
python test_e2e_integration.py
```

**Outputs**:
- `data/analysis/e2e_integration_test.json`
- `data/analysis/e2e_integration_test.md`

## 🎯 Master Validation Script

### Phase 3 Comprehensive Validation
**File**: `run_phase3_comprehensive_validation.py`
**Purpose**: Orchestrates all validation tests and generates unified report

**Features**:
- Runs all 4 validation scripts in optimal order
- Handles dependencies between tests
- Consolidates recommendations
- Assesses overall system readiness
- Generates comprehensive summary report

**Usage**:
```bash
# Standard validation
python run_phase3_comprehensive_validation.py

# Verbose output
python run_phase3_comprehensive_validation.py --verbose

# Custom output directory
python run_phase3_comprehensive_validation.py --output-dir custom/path
```

**Outputs**:
- `data/analysis/phase3_validation_summary.json`
- `data/analysis/phase3_comprehensive_validation_report.md`

## 📊 Test Execution Order

The master script runs tests in this optimal order:

1. **Component Mapping Validation** (Critical)
   - Foundation validation for all other tests
   - Ensures mapping completeness before Shopify queries

2. **Shopify Entry Verification** (Critical)  
   - Depends on: Component Mapping Validation
   - Verifies GIDs exist before product creation tests

3. **Product Creation Testing** (Critical)
   - Depends on: Component Mapping + Shopify Verification
   - Tests actual product creation workflow

4. **End-to-End Integration Testing** (Important)
   - Independent validation of complete workflows
   - Can run regardless of other test results

## 🎯 Success Criteria

### Production Readiness Requirements

For the system to be marked as **production ready**, all of the following must be met:

- ✅ Component Mapping Validation: Score ≥ 80%
- ✅ Shopify Entry Verification: Success rate ≥ 90% 
- ✅ Product Creation Testing: Success rate ≥ 80%
- ✅ End-to-End Integration: Success rate ≥ 75%
- ✅ No critical issues detected

### Score Interpretations

**Validation Scores**:
- **90-100%**: Excellent - Production ready
- **80-89%**: Good - Minor issues to address
- **70-79%**: Fair - Several issues need attention  
- **Below 70%**: Poor - Significant problems requiring fixes

**Critical vs Non-Critical Tests**:
- **Critical Tests**: Must pass for production deployment
- **Non-Critical Tests**: Important for quality but don't block production

## 🔧 Development & Debugging

### Running Individual Tests

Each test script can be run independently for debugging:

```bash
# Test specific component mapping
python validate_component_mapping.py

# Test Shopify connectivity
python verify_shopify_entries.py

# Test product creation (dry run)
python test_laptop_product_creation.py

# Test workflows
python test_e2e_integration.py
```

### Verbose Output

Use `--verbose` flag with the master script for detailed debugging information:

```bash
python run_phase3_comprehensive_validation.py --verbose
```

### Test Data Location

All test results are saved to:
- **JSON Data**: `data/analysis/*.json` (machine-readable)
- **Reports**: `data/analysis/*.md` (human-readable)

### Common Issues & Troubleshooting

**Issue**: "No templates loaded from cache"
- **Solution**: Run template cache regeneration first
- **Command**: Check `services/template_cache_service.py`

**Issue**: "GraphQL error: authentication"  
- **Solution**: Verify Shopify API credentials in `.env`
- **Check**: `SHOPIFY_ACCESS_TOKEN` and `SHOPIFY_SHOP_DOMAIN`

**Issue**: "Component mapping not found"
- **Solution**: Run Phase 2 GID resolution first
- **Command**: `python scripts/metaobjects/run_phase2_complete.py`

**Issue**: Script timeout (10 minutes)
- **Solution**: Check network connectivity and API rate limits
- **Note**: Large datasets may require increased timeout

## 📈 Integration with CI/CD

These tests are designed for integration with continuous integration:

### Exit Codes
- `0`: All tests passed, production ready
- `1`: Some tests failed, issues need attention  
- `2`: Critical failures, production blocked
- `130`: User interruption (Ctrl+C)

### Example CI Integration
```yaml
# Example GitHub Actions workflow
- name: Run Phase 3 Validation
  run: |
    python scripts/testing/run_phase3_comprehensive_validation.py
    
- name: Upload Test Reports
  uses: actions/upload-artifact@v3
  with:
    name: phase3-validation-reports
    path: data/analysis/phase3_*
```

## 🔄 Regular Maintenance

### Recommended Schedule

- **Daily**: Run master validation during development
- **Weekly**: Run full validation in staging environment
- **Before Production Deployment**: Always run complete validation
- **After Metaobject Changes**: Run Shopify verification

### Monitoring

Track these key metrics over time:
- Component mapping completeness percentage
- Shopify GID success rate
- Product creation success rate
- Overall system readiness score

## 📚 Related Documentation

- **Phase 1**: `scripts/analysis/README.md` - Component analysis
- **Phase 2**: `scripts/metaobjects/README.md` - GID resolution
- **Main Plan**: `LAPTOP_COMPONENT_MAPPING_PLAN.md` - Complete project plan
- **Architecture**: `docs/ARCHITECTURE.md` - System architecture
- **API Patterns**: `.ai/patterns/testing_patterns.md` - Testing patterns

---

## 🎯 Quick Start

**For first-time validation**:
```bash
# Run complete Phase 3 validation
python scripts/testing/run_phase3_comprehensive_validation.py --verbose

# Review the generated report
open data/analysis/phase3_comprehensive_validation_report.md
```

**For ongoing validation**:
```bash
# Quick validation check
python scripts/testing/run_phase3_comprehensive_validation.py

# Review summary for any critical issues
grep -E "(Production Ready|Critical Issues)" data/analysis/phase3_comprehensive_validation_report.md
```

This comprehensive testing suite ensures the laptop component mapping system is production-ready and maintains high quality standards throughout development and deployment.