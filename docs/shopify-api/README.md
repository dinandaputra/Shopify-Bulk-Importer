# Shopify API Reference for Bulk Importer

This directory contains comprehensive Shopify API documentation extracted and organized for the MyByte Shopify Bulk Importer project.

## Files Overview

### Core API Documentation
- **`product-rest-structure.md`** - Complete REST API product structure with real examples from your store
- **`product-graphql.md`** - GraphQL Product API documentation including mutations and queries
- **`metafields-rest.md`** - REST API metafields documentation with examples and use cases
- **`metaobject-graphql.md`** - GraphQL Metaobject API for managing custom data definitions

## Quick Reference

### Your Store Details
- **Store**: myByte International (jufbtk-ut.myshopify.com)
- **Currency**: JPY (Japanese Yen)
- **Location**: Japan (GMT+09:00)
- **API Version**: 2025-07

### Your Metaobject Definitions
1. **Cosmetic condition** (gid://shopify/MetaobjectDefinition/7936508053)
2. **SIM card capability** (gid://shopify/MetaobjectDefinition/7936540821)
3. **Operating system** (gid://shopify/MetaobjectDefinition/7936573589)
4. **Color** (gid://shopify/MetaobjectDefinition/7936606357)
5. **Subscription type** (gid://shopify/MetaobjectDefinition/7936639125)

### API Access Scopes Configured
- `read_products` / `write_products`
- `read_metaobjects` / `write_metaobjects`
- `read_metaobject_definitions` / `write_metaobject_definitions`
- `read_inventory` / `write_inventory`
- `read_product_listings` / `write_product_listings`
- `read_price_rules` / `write_price_rules`

## Key Implementation Notes

### REST vs GraphQL
- **Products**: Use REST API for CRUD operations
- **Metaobjects**: Use GraphQL API (REST endpoints deprecated)
- **Metafields**: Use REST API for attaching custom data to products

### Metafield Patterns
- **Shopify namespace**: `shopify.color` for official color references
- **Custom namespace**: `custom.*` for custom metafields
- **Metaobject references**: Use full GID format `gid://shopify/Metaobject/{id}`

### Currency & Pricing
- All prices stored as strings in JPY
- Example: `"2500"` = ¥2,500
- No decimal places for JPY currency

### Inventory Management
- Set `inventory_management: "shopify"` for stock tracking
- Use `inventory_policy: "deny"` to prevent overselling
- Japan timezone: All timestamps include `+09:00`

## Testing Commands

### Test API Connection
```bash
export $(cat .env | grep -v ^# | xargs) && python3 -c "
from services.shopify_api import shopify_api
shop_info = shopify_api.test_connection()
print(f'Connected to: {shop_info[\"shop\"][\"name\"]}')
"
```

### Test Product Creation
```bash
export $(cat .env | grep -v ^# | xargs) && python3 -c "
from services.shopify_api import shopify_api
product = shopify_api.create_product({
    'title': 'Test Product',
    'status': 'draft',
    'published': False
})
print(f'Created product ID: {product[\"product\"][\"id\"]}')
"
```

This documentation is tailored specifically for your MyByte International store and bulk importer requirements.