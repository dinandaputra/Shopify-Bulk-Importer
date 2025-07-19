# Shopify REST API Product Structure

## Core Product Fields

### Product Level
- `id`: Unique product identifier
- `title`: Product name displayed to customers
- `body_html`: Product description (HTML)
- `vendor`: Name of product's vendor
- `product_type`: Product category/type
- `handle`: URL handle (auto-generated from title)
- `status`: Product status (active, draft, archived)
- `published_at`: Publication timestamp
- `published_scope`: Visibility scope (global, web)
- `tags`: Comma-separated tags
- `template_suffix`: Theme template override
- `created_at`: Creation timestamp
- `updated_at`: Last modification timestamp
- `admin_graphql_api_id`: GraphQL API identifier

### Product Variants
Each product has `variants` array containing:
- `id`: Variant unique identifier
- `product_id`: Parent product ID
- `title`: Variant title
- `price`: Price as string
- `compare_at_price`: Original price for discounts
- `position`: Display order
- `inventory_policy`: How to handle out-of-stock (deny/continue)
- `option1`, `option2`, `option3`: Variant option values
- `taxable`: Whether variant is taxable
- `barcode`: Product barcode
- `sku`: Stock keeping unit
- `weight`: Product weight
- `weight_unit`: Unit of weight (kg, g, lb, oz)
- `grams`: Weight in grams
- `inventory_management`: Who manages inventory (shopify/manual/null)
- `inventory_quantity`: Current stock level
- `requires_shipping`: Whether variant needs shipping
- `fulfillment_service`: Who fulfills orders (manual/third-party)

### Product Options
- `options` array defines variant option types:
  - `id`: Option ID
  - `name`: Option name (e.g., "Size", "Color")
  - `position`: Display order
  - `values`: Array of possible values

### Product Images
- `images` array contains product media:
  - `id`: Image ID
  - `src`: Image URL
  - `alt`: Alt text
  - `position`: Display order
  - `width`, `height`: Image dimensions
  - `variant_ids`: Which variants use this image
- `image`: Primary product image (same structure as images[0])

## REST API Endpoints

### Create Product
```
POST /admin/api/2025-07/products.json
```

### Get Products
```
GET /admin/api/2025-07/products.json
```

### Get Single Product
```
GET /admin/api/2025-07/products/{product_id}.json
```

### Update Product
```
PUT /admin/api/2025-07/products/{product_id}.json
```

### Delete Product
```
DELETE /admin/api/2025-07/products/{product_id}.json
```

## Key Notes for Implementation
- Prices are stored as strings, not numbers
- All timestamps include timezone (+09:00 for Japan store)
- Currency is JPY for this store
- Inventory management set to "shopify" for stock tracking
- Products can have multiple variants with different options
- Images are stored separately but linked to variants