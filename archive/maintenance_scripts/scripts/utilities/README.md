# Utility Scripts

General utility scripts for various operational tasks.

## Directory Structure

- **data_migration/** - Scripts for migrating data between systems
- **bulk_operations/** - Scripts for bulk product/inventory operations
- **reporting/** - Scripts for generating reports and analytics
- **debugging/** - Scripts for debugging and verification

## Purpose

These scripts handle tasks that don't fit into the metaobject category but are essential for store operations.

## Categories

### Data Migration
- Import/export between different formats
- Legacy system migrations
- Data transformation scripts

### Bulk Operations
- Bulk product updates
- Inventory adjustments
- Price updates
- Collection management

### Reporting
- Sales analytics
- Inventory reports
- Product performance metrics
- Missing data reports

### Debugging
- Data validation scripts
- Consistency checks
- API response debugging
- Configuration verification

## Best Practices

1. **Modular Design** - Keep scripts focused on single tasks
2. **Reusable Functions** - Extract common operations
3. **Clear Documentation** - Include usage examples
4. **Error Handling** - Graceful failure with clear messages
5. **Logging** - Track all operations for audit

## Common Patterns

### Configuration Loading
```python
def load_config():
    """Load configuration from environment"""
    return {
        'shop_domain': os.getenv('SHOPIFY_SHOP_DOMAIN'),
        'access_token': os.getenv('SHOPIFY_ACCESS_TOKEN')
    }
```

### Progress Tracking
```python
from tqdm import tqdm

def process_items(items):
    for item in tqdm(items, desc="Processing"):
        process_single_item(item)
```

### Result Reporting
```python
def generate_report(results):
    """Generate summary report of operations"""
    print(f"Processed: {results['total']}")
    print(f"Success: {results['success']}")
    print(f"Failed: {results['failed']}")
```