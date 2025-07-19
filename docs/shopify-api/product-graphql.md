# Shopify GraphQL Product API Documentation

## Overview
- **Access Scope Required**: `read_products`
- **Represents**: Goods and services merchants offer to customers
- **Supports**: Product variants, media, collections, inventory, pricing, publication status

## Key Product Object Fields

### Core Fields
- `title`: Product name displayed to customers
- `description`: Product description  
- `vendor`: Name of product's vendor
- `priceRangeV2`: Minimum and maximum product prices
- `variants`: List of product variants
- `options`: Product configuration options (size, color, etc.)
- `status`: Controls product visibility across sales channels

### Metafield Support
- `metafield`: Custom fields for additional product information
- `metafields`: Connection to multiple custom fields

## Key Mutations

### Product Management
1. **`productCreate`**: Create new products
2. **`productUpdate`**: Modify existing product details
3. **`productDuplicate`**: Duplicate an existing product

### Product Options
4. **`productOptionsCreate`**: Add product options
5. **`productOptionsDelete`**: Remove product options  
6. **`productOptionsReorder`**: Change option display order

## Usage Notes
- Products support comprehensive data management within Shopify's GraphQL Admin API
- Metafields allow custom product attributes beyond standard fields
- Product variants enable size/color/option variations
- Status field controls visibility across different sales channels