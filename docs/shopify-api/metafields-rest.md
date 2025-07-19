# Shopify REST API Metafields Documentation

## Overview
Metafields allow storing additional custom data for products, variants, customers, orders, and other resources.

## Metafield Structure

### Core Fields
- `id`: Unique metafield identifier
- `namespace`: Groups related metafields (e.g., "custom", "shopify")
- `key`: Metafield identifier within namespace
- `value`: The actual data stored
- `type`: Data type (metaobject_reference, single_line_text_field, etc.)
- `description`: Optional description
- `owner_id`: ID of resource this metafield belongs to
- `owner_resource`: Type of resource (product, variant, customer, etc.)
- `created_at`: Creation timestamp
- `updated_at`: Last modification timestamp
- `admin_graphql_api_id`: GraphQL API identifier

## Common Metafield Types

### Metaobject Reference
```json
{
  "type": "metaobject_reference",
  "value": "gid://shopify/Metaobject/117057880213"
}
```

### Text Fields
```json
{
  "type": "single_line_text_field",
  "value": "Some text value"
}
```

### Number Fields
```json
{
  "type": "number_integer",
  "value": "42"
}
```

### List References
```json
{
  "type": "list.metaobject_reference",
  "value": "[\"gid://shopify/Metaobject/123\", \"gid://shopify/Metaobject/456\"]"
}
```

## REST API Endpoints

### Get Product Metafields
```
GET /admin/api/2025-07/products/{product_id}/metafields.json
```

### Create Product Metafield
```
POST /admin/api/2025-07/products/{product_id}/metafields.json
```

### Update Product Metafield
```
PUT /admin/api/2025-07/products/{product_id}/metafields/{metafield_id}.json
```

### Delete Product Metafield
```
DELETE /admin/api/2025-07/products/{product_id}/metafields/{metafield_id}.json
```

## Example Create Request

```json
{
  "metafield": {
    "namespace": "custom",
    "key": "color",
    "type": "metaobject_reference",
    "value": "gid://shopify/Metaobject/123456789"
  }
}
```

## Key Implementation Notes

### Namespaces
- `custom`: For custom metafields
- `shopify`: For Shopify-managed metafields (like colors)
- Custom namespaces: Can create your own

### Metaobject References
- Use full GID format: `gid://shopify/Metaobject/{id}`
- For lists: JSON array of GIDs as string
- References must point to existing metaobjects

### Error Handling
- Invalid metaobject references will fail
- Namespace/key combinations must be unique per resource
- Type mismatches will be rejected

## Common Use Cases for Products
- **Color**: `shopify.color` → metaobject reference
- **Storage**: `custom.storage` → metaobject reference  
- **Condition**: `custom.condition` → metaobject reference
- **Specifications**: `custom.specs` → text or number fields
- **Categories**: `custom.category` → metaobject reference