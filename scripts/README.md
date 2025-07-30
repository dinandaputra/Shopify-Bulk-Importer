# Scripts Directory

This directory contains utility scripts organized by functionality.

## Directory Structure

```
scripts/
├── metaobjects/           # Shopify metaobject management
│   ├── create/           # Scripts to create metaobjects
│   ├── query/            # Scripts to query metaobjects
│   ├── update/           # Scripts to update metaobjects
│   └── analyze/          # Scripts to analyze metaobjects
├── utilities/            # General utility scripts
│   ├── data_migration/   # Data migration scripts
│   ├── bulk_operations/  # Bulk operation scripts
│   └── reporting/        # Reporting and analytics
└── one_time/            # Scripts run once and archived
```

## Metaobject Scripts

### Create Scripts
- `create_laptop_metaobjects_final.py`: Creates laptop-related metaobjects
- `laptop_metaobject_data.py`: Data definitions for laptop metaobjects

### Query Scripts
- `laptop_metaobject_definitions_mapping.py`: Maps laptop specifications to metaobject IDs

## Utility Scripts

### General Utilities
- `verify_black_color_fix.py`: Validates color metafield mappings

## Usage Guidelines

1. **Test First**: Always test scripts on development store before production
2. **Backup**: Ensure you have backups before running destructive operations  
3. **Rate Limits**: Be mindful of Shopify API rate limits
4. **Documentation**: Each script should include usage instructions

## Running Scripts

Most scripts require environment variables to be set:

```bash
export SHOPIFY_ACCESS_TOKEN="your_token"
export SHOPIFY_SHOP_DOMAIN="your-shop.myshopify.com"
export SHOPIFY_API_KEY="your_api_key"
export SHOPIFY_API_SECRET="your_api_secret"
```

Then run from the project root:
```bash
python scripts/metaobjects/create/create_laptop_metaobjects_final.py
```

## Contributing

When adding new scripts:
1. Choose the appropriate subdirectory
2. Include clear docstring with usage instructions
3. Handle errors gracefully
4. Log important operations
5. Update this README if adding new categories