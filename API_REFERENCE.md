# API Reference

This document provides a comprehensive reference for all APIs and services used in the Shopify Bulk Importer application.

## Table of Contents

1. [Shopify API Integration](#shopify-api-integration)
2. [Service APIs](#service-apis)
3. [Model Schemas](#model-schemas)
4. [Configuration APIs](#configuration-apis)
5. [Utility Functions](#utility-functions)

## Shopify API Integration

### ShopifyAPI Class

Location: `services/shopify_api.py`

The main class for interacting with Shopify's REST and GraphQL APIs.

#### Initialization

```python
api = ShopifyAPI()
```

Environment variables required:
- `SHOPIFY_ACCESS_TOKEN`
- `SHOPIFY_SHOP_DOMAIN`
- `SHOPIFY_API_KEY`
- `SHOPIFY_API_SECRET`

#### Methods

##### create_product(product_data: dict) -> dict

Creates a product using Shopify REST API.

```python
product_data = {
    "title": "iPhone 15 Pro Max 256GB",
    "vendor": "Apple",
    "product_type": "Mobile & Smart Phones",
    "variants": [{
        "option1": "SIM Free",
        "price": "150000",
        "inventory_quantity": 1
    }]
}
result = api.create_product(product_data)
```

**Returns**: Product object with ID, variants, and handle

##### create_product_with_graphql(product_input: dict) -> dict

Creates a product using GraphQL productSet mutation.

```python
product_input = {
    "title": "Laptop Model",
    "productType": "Electronics",
    "vendor": "Brand",
    "variants": [...]
}
result = api.create_product_with_graphql(product_input)
```

##### assign_metafields_to_product(product_id: str, metafields: list) -> dict

Assigns metafields to a product.

```python
metafields = [{
    "namespace": "custom",
    "key": "product_rank",
    "value": "A",
    "type": "single_line_text_field"
}]
api.assign_metafields_to_product("gid://shopify/Product/123", metafields)
```

##### assign_metafields_to_variants(variant_metafield_data: list) -> dict

Assigns metafields to product variants.

```python
variant_data = [{
    "variant_id": "gid://shopify/ProductVariant/123",
    "metafield": {
        "namespace": "custom",
        "key": "sim_carrier",
        "value": '["gid://shopify/Metaobject/456"]',
        "type": "list.metaobject_reference"
    }
}]
api.assign_metafields_to_variants(variant_data)
```

##### upload_image(image_url: str) -> dict

Uploads an image to Shopify CDN.

```python
result = api.upload_image("https://example.com/image.jpg")
# Returns: {"url": "https://cdn.shopify.com/..."}
```

## Service APIs

### ProductService

Location: `services/product_service.py`

High-level service for product creation workflow.

#### create_smartphone_product(smartphone_data: Smartphone) -> dict

Creates a smartphone product with all metafields and variants.

```python
from models.smartphone import SmartphoneProduct

smartphone = SmartphoneProduct(
    title="iPhone 15 Pro Max 256GB",
    brand="Apple",
    model="iPhone 15 Pro Max",
    storage="256GB",
    color="Blue Titanium",
    price=150000,
    product_rank="A",
    sim_carrier_variants=["SIM Free", "Softbank (-)"]
)

result = ProductService.create_smartphone_product(smartphone)
```

#### create_laptop_product(laptop_data: Laptop) -> dict

Creates a laptop product with specifications and metafields.

```python
from models.laptop import LaptopProduct

laptop = LaptopProduct(
    title="ASUS ROG Strix G16",
    brand="ASUS",
    model="ROG Strix G16",
    price=180000,
    cpu="Intel Core i7-13700H",
    ram="16GB",
    storage="512GB SSD"
)

result = ProductService.create_laptop_product(laptop)
```

### MetaobjectService

Location: `services/metaobject_service.py`

Handles metaobject lookups and reference management.

#### get_metaobject_gid(metaobject_type: str, value: str) -> str

Retrieves the GID for a metaobject value.

```python
gid = MetaobjectService.get_metaobject_gid("color", "Space Black")
# Returns: "gid://shopify/Metaobject/123456"
```

#### query_metaobjects_by_type(type_id: str) -> list

Queries all metaobjects of a specific type.

```python
colors = MetaobjectService.query_metaobjects_by_type(
    "gid://shopify/MetaobjectDefinition/7936606357"
)
```

### ValidationService

Location: `services/validation_service.py`

Business rule validation beyond model constraints.

#### validate_product_data(product_data: dict) -> tuple[bool, list[str]]

Validates product data against business rules.

```python
is_valid, errors = ValidationService.validate_product_data({
    "title": "Product Name",
    "price": 100000,
    "inventory_quantity": 1
})
```

### ImageService

Location: `services/image_service.py`

Handles image upload and management.

#### upload_product_images(images: list) -> list[dict]

Uploads multiple images to Shopify CDN.

```python
images = [image_file_1, image_file_2]
uploaded = ImageService.upload_product_images(images)
# Returns: [{"url": "https://cdn.shopify.com/..."}, ...]
```

### ExportService

Location: `services/export_service.py`

CSV export functionality for manual import fallback.

#### export_products_to_csv(products: list[dict]) -> str

Exports products to CSV format.

```python
csv_path = ExportService.export_products_to_csv(session_products)
# Returns: "exports/products_20250730_123456.csv"
```

## Model Schemas

### Smartphone Model

Location: `models/smartphone.py`

```python
class Smartphone(BaseModel):
    title: str
    brand: str
    model: str
    storage: Optional[str]
    color: Optional[str]
    price: float = Field(gt=0)
    inventory_quantity: int = Field(default=1, ge=0)
    product_rank: str
    condition_description: Optional[str]
    ram_size: Optional[str]
    minus: Optional[List[str]]
    product_inclusions: Optional[List[str]]
    sim_carrier_variants: List[str] = Field(default=["SIM Free"])
    collections: List[str] = Field(default=["All Products"])
    images: Optional[List[str]]
```

### Laptop Model

Location: `models/laptop.py`

```python
class Laptop(BaseModel):
    title: str
    brand: str
    model: str
    price: float = Field(gt=0)
    inventory_quantity: int = Field(default=1, ge=0)
    product_rank: str
    condition_description: Optional[str]
    cpu: Optional[str]
    ram: Optional[str]
    gpu: Optional[str]
    display: Optional[str]
    storage: Optional[str]
    os: Optional[str]
    keyboard_layout: Optional[str]
    keyboard_backlight: Optional[str]
    color: Optional[str]
    product_inclusions: Optional[List[str]]
    collections: List[str] = Field(default=["All Products"])
    images: Optional[List[str]]
```

## Configuration APIs

### ShopifyConfig

Location: `config/shopify_config.py`

```python
class ShopifyConfig:
    ACCESS_TOKEN: str
    SHOP_DOMAIN: str
    API_KEY: str
    API_SECRET: str
    API_VERSION: str = "2025-07"
    
    @classmethod
    def validate(cls) -> bool:
        """Validates all required configuration is present"""
```

### MasterData

Location: `config/master_data.py`

```python
# Product templates
SMARTPHONE_TEMPLATES = {
    "iPhone 15 Pro Max 256GB [Blue Titanium]": {...},
    "Samsung Galaxy S24 Ultra 512GB [Titanium Gray]": {...}
}

LAPTOP_TEMPLATES = {
    "ASUS ROG Strix G16 [i7/16GB/RTX4060/16inch/512GB]": {...}
}

# Metaobject mappings
METAOBJECT_DEFINITIONS = {
    "cosmetic_condition": "gid://shopify/MetaobjectDefinition/7936508053",
    "sim_card_capability": "gid://shopify/MetaobjectDefinition/7936540821",
    "operating_system": "gid://shopify/MetaobjectDefinition/7936573589",
    "color": "gid://shopify/MetaobjectDefinition/7936606357",
    "subscription_type": "gid://shopify/MetaobjectDefinition/7936639125"
}
```

## Utility Functions

### Handle Generator

Location: `utils/handle_generator.py`

#### generate_handle(brand: str, model: str, specs: str) -> str

Generates a unique handle with daily counter.

```python
handle = generate_handle("apple", "iphone-15-pro-max", "256gb")
# Returns: "apple-iphone-15-pro-max-256gb-250730-001"
```

#### reset_daily_counter() -> None

Resets the daily counter (automatically called when date changes).

```python
reset_daily_counter()
```

### Date Utilities

#### get_current_date() -> str

Returns current date in YYMMDD format.

```python
date = get_current_date()
# Returns: "250730"
```

## GraphQL Queries and Mutations

### Product Creation (GraphQL)

```graphql
mutation productSet($input: ProductSetInput!) {
  productSet(input: $input) {
    product {
      id
      title
      handle
      variants(first: 10) {
        edges {
          node {
            id
            title
            price
          }
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
```

### Metafield Assignment

```graphql
mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
    }
    userErrors {
      field
      message
    }
  }
}
```

### Metaobject Query

```graphql
query getMetaobjects($type: String!) {
  metaobjects(type: $type, first: 250) {
    edges {
      node {
        id
        displayName
        fields {
          key
          value
        }
      }
    }
  }
}
```

## Error Handling

All API methods follow consistent error handling:

```python
try:
    result = api.create_product(data)
except ShopifyAPIError as e:
    # Handle Shopify-specific errors
    print(f"API Error: {e.message}")
except ValidationError as e:
    # Handle validation errors
    print(f"Validation Error: {e.errors()}")
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected Error: {str(e)}")
```

## Rate Limiting

The Shopify API client implements automatic rate limiting:
- REST API: 2 requests per second
- GraphQL API: Calculated cost-based throttling
- Automatic retry with exponential backoff

## Response Formats

### Successful Product Creation

```json
{
  "success": true,
  "product": {
    "id": "gid://shopify/Product/123456",
    "title": "iPhone 15 Pro Max 256GB",
    "handle": "apple-iphone-15-pro-max-256gb-250730-001",
    "variants": [...]
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Product creation failed",
  "details": {
    "field": "title",
    "message": "Title is required"
  }
}
```

## Testing

Example test cases for API methods:

```python
def test_create_product():
    api = ShopifyAPI()
    result = api.create_product({
        "title": "Test Product",
        "vendor": "Test Brand"
    })
    assert result["success"] == True
    assert "id" in result["product"]
```

This API reference provides the foundation for understanding and using the Shopify Bulk Importer's programmatic interfaces.