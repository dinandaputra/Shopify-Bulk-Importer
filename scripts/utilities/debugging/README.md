# Debugging Scripts

Scripts for debugging, verification, and troubleshooting.

## Available Scripts

### verify_black_color_fix.py
Verifies that the black color metafield mapping is working correctly.

**Usage:**
```bash
python scripts/utilities/debugging/verify_black_color_fix.py
```

**Purpose:**
- Tests color metafield creation
- Verifies black color mapping specifically
- Validates metaobject references

## Common Debugging Tasks

### Data Validation
Verify data integrity and consistency:

```python
def validate_product_data(product):
    """Validate product data structure"""
    errors = []
    
    # Required fields
    if not product.get('title'):
        errors.append("Missing title")
    
    # Data types
    if not isinstance(product.get('price'), (int, float)):
        errors.append("Invalid price type")
    
    # Business rules
    if product.get('price', 0) < 0:
        errors.append("Negative price")
    
    return errors
```

### API Response Debugging
Debug Shopify API responses:

```python
def debug_api_response(response):
    """Print detailed API response information"""
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Body: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code >= 400:
        print("ERROR DETAILS:")
        error_data = response.json()
        if 'errors' in error_data:
            for error in error_data['errors']:
                print(f"  - {error}")
```

### Configuration Verification
Verify environment and configuration:

```python
def verify_configuration():
    """Check all required configuration is present"""
    required_vars = [
        'SHOPIFY_ACCESS_TOKEN',
        'SHOPIFY_SHOP_DOMAIN',
        'SHOPIFY_API_KEY',
        'SHOPIFY_API_SECRET'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"Missing environment variables: {missing}")
        return False
    
    print("Configuration verified ✅")
    return True
```

### Metafield Debugging
Debug metafield creation and references:

```python
def debug_metafield_creation(product_id):
    """Debug metafield creation for a product"""
    # Get product with metafields
    product = api.get_product(product_id, include_metafields=True)
    
    print(f"Product: {product['title']}")
    print(f"Metafields: {len(product.get('metafields', []))}")
    
    for metafield in product.get('metafields', []):
        print(f"\nMetafield: {metafield['namespace']}.{metafield['key']}")
        print(f"  Type: {metafield['type']}")
        print(f"  Value: {metafield['value']}")
```

## Debugging Patterns

### Verbose Logging
Enable detailed logging for troubleshooting:

```python
import logging

def setup_debug_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Also log HTTP requests
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1
```

### State Inspection
Inspect application state at key points:

```python
def inspect_state(checkpoint_name, **kwargs):
    """Log state at debugging checkpoint"""
    print(f"\n=== CHECKPOINT: {checkpoint_name} ===")
    for key, value in kwargs.items():
        print(f"{key}: {value}")
    print("=" * 40)
```

### Error Reproduction
Create minimal test cases:

```python
def reproduce_error():
    """Minimal code to reproduce an error"""
    try:
        # Minimal setup
        api = ShopifyAPI()
        
        # Reproduce issue
        result = api.problematic_operation()
        
    except Exception as e:
        print(f"Error reproduced: {type(e).__name__}")
        print(f"Message: {str(e)}")
        import traceback
        traceback.print_exc()
```

## Best Practices

1. **Isolate Issues** - Create minimal reproducible examples
2. **Use Logging** - Don't rely on print statements in production
3. **Check Assumptions** - Verify data types and structures
4. **Document Findings** - Record what you discover
5. **Clean Up** - Remove debug code before committing

## Common Issues and Solutions

### Rate Limiting
```python
# Check rate limit headers
print(f"Rate limit: {response.headers.get('X-Shopify-Shop-Api-Call-Limit')}")
```

### Invalid Metaobject References
```python
# Verify metaobject exists
metaobject = api.get_metaobject(metaobject_id)
if not metaobject:
    print(f"Metaobject {metaobject_id} not found!")
```

### JSON Parsing Errors
```python
# Handle malformed JSON
try:
    data = json.loads(json_string)
except json.JSONDecodeError as e:
    print(f"JSON error at position {e.pos}: {e.msg}")
    print(f"Problem area: {json_string[max(0, e.pos-20):e.pos+20]}")
```