# Metaobject Scripts

This directory contains scripts for managing Shopify metaobjects, including the **Phase 2** automated GID resolution and mapping update system.

## Directory Structure

- **create/** - Scripts to create new metaobjects in Shopify
- **query/** - Scripts to query and search existing metaobjects
- **update/** - Scripts to update metaobject values
- **analyze/** - Scripts to analyze metaobject usage and find gaps

## Phase 2: GID Resolution & Mapping Updates (NEW)

### Core Phase 2 Scripts

- **`resolve_missing_gids.py`** - Main GID resolution script for unmapped components
- **`batch_update_mappings.py`** - Automated JSON mapping file updater with backup system
- **`generate_missing_report.py`** - Missing Shopify entries report generator
- **`run_phase2_complete.py`** - Master workflow orchestrator for complete Phase 2

### Quick Start Phase 2

```bash
# Run complete Phase 2 workflow
python scripts/metaobjects/run_phase2_complete.py
```

This automated workflow:
1. Resolves GIDs for unmapped laptop components
2. Updates mapping files with found GIDs
3. Generates missing components report
4. Creates comprehensive backup and validation system

### Phase 2 Features
- **GraphQL Integration**: Efficient metaobject queries
- **Smart Component Matching**: Multiple search variations
- **Automatic Backup System**: Timestamped backups before updates
- **Rate Limiting**: Shopify API rate limit handling
- **Comprehensive Reporting**: Missing components with priority classification

## Common Use Cases

### Creating New Metaobjects
When adding support for new product categories (e.g., laptops, tablets), use the create scripts to bulk-create required metaobjects.

### Querying Metaobjects
Use query scripts to:
- Find metaobject GIDs by display name
- Export metaobject data for documentation
- Verify metaobject definitions exist

### Updating Metaobjects
Update scripts help with:
- Bulk value updates
- Fixing typos or incorrect mappings
- Adding new fields to existing metaobjects

### Analyzing Metaobjects
Analysis scripts help identify:
- Missing metaobject mappings
- Unused metaobjects
- Frequency of metaobject usage

## Best Practices

1. **Always test in development** before running on production
2. **Use GraphQL for bulk operations** to minimize API calls
3. **Log all operations** for audit trail
4. **Handle rate limits** gracefully with retries
5. **Backup before destructive operations**

## Required Environment Variables

```bash
export SHOPIFY_ACCESS_TOKEN="your_token"
export SHOPIFY_SHOP_DOMAIN="your-shop.myshopify.com"
export SHOPIFY_API_KEY="your_api_key"
export SHOPIFY_API_SECRET="your_api_secret"
```