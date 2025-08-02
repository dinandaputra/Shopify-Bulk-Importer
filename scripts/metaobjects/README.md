# Metaobject Scripts

This directory contains scripts for managing Shopify metaobjects.

## Directory Structure

- **create/** - Scripts to create new metaobjects in Shopify
- **query/** - Scripts to query and search existing metaobjects
- **update/** - Scripts to update metaobject values
- **analyze/** - Scripts to analyze metaobject usage and find gaps

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