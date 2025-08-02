# Bulk Operations Scripts

Scripts for performing bulk operations on products, inventory, and other Shopify resources.

## Purpose

Bulk operation scripts help with:
- Mass product updates
- Inventory adjustments across multiple products
- Price changes for collections
- Bulk metafield assignments
- Collection management

## Common Bulk Operations

### Bulk Product Updates
Update multiple products efficiently:

```python
def bulk_update_products(updates):
    """Update multiple products using GraphQL bulk operations"""
    mutation = """
    mutation productUpdate($input: ProductInput!) {
        productUpdate(input: $input) {
            product {
                id
                title
                status
            }
            userErrors {
                field
                message
            }
        }
    }
    """
    
    results = {'success': 0, 'failed': 0}
    
    for update in updates:
        try:
            result = api.execute_graphql(mutation, {'input': update})
            if result['data']['productUpdate']['userErrors']:
                results['failed'] += 1
            else:
                results['success'] += 1
        except Exception as e:
            results['failed'] += 1
            
    return results
```

### Bulk Inventory Adjustments
Adjust inventory for multiple locations:

```python
def bulk_adjust_inventory(adjustments):
    """Adjust inventory levels in bulk"""
    mutation = """
    mutation inventoryAdjustQuantities($input: InventoryAdjustQuantitiesInput!) {
        inventoryAdjustQuantities(input: $input) {
            inventoryAdjustmentGroup {
                createdAt
                reason
                changes {
                    name
                    delta
                }
            }
            userErrors {
                field
                message
            }
        }
    }
    """
    # Process adjustments...
```

### Bulk Price Updates
Update prices for entire collections:

```python
def update_collection_prices(collection_id, price_adjustment):
    """Update all product prices in a collection"""
    # 1. Get all products in collection
    products = api.get_collection_products(collection_id)
    
    # 2. Calculate new prices
    updates = []
    for product in products:
        for variant in product['variants']:
            new_price = calculate_new_price(
                variant['price'], 
                price_adjustment
            )
            updates.append({
                'id': variant['id'],
                'price': new_price
            })
    
    # 3. Apply updates in batches
    return bulk_update_variants(updates)
```

## Bulk Operation Patterns

### Batching
Process items in batches to respect rate limits:

```python
def process_in_batches(items, batch_size=50):
    """Process items in batches"""
    total = len(items)
    
    for i in range(0, total, batch_size):
        batch = items[i:i+batch_size]
        
        print(f"Processing batch {i//batch_size + 1} of {total//batch_size + 1}")
        process_batch(batch)
        
        # Rate limit pause
        time.sleep(1)
```

### Progress Tracking
Show progress for long operations:

```python
from tqdm import tqdm

def bulk_operation_with_progress(items):
    """Show progress bar for bulk operations"""
    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }
    
    with tqdm(total=len(items), desc="Processing") as pbar:
        for item in items:
            try:
                result = process_item(item)
                results['success'].append(result)
            except Exception as e:
                results['failed'].append({
                    'item': item,
                    'error': str(e)
                })
            
            pbar.update(1)
    
    return results
```

### Parallel Processing
Use threading for independent operations:

```python
from concurrent.futures import ThreadPoolExecutor
import threading

rate_limit_lock = threading.Lock()

def parallel_bulk_operation(items, max_workers=5):
    """Process items in parallel with rate limiting"""
    
    def process_with_rate_limit(item):
        with rate_limit_lock:
            # Ensure rate limiting
            time.sleep(0.2)
        
        return process_item(item)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_with_rate_limit, items))
    
    return results
```

## Safety Measures

### Dry Run Mode
Test operations before executing:

```python
def bulk_operation(items, dry_run=True):
    """Bulk operation with dry run support"""
    if dry_run:
        print("DRY RUN MODE - No changes will be made")
        
        for item in items[:5]:  # Show sample
            print(f"Would process: {item}")
        
        print(f"... and {len(items)-5} more items")
        return
    
    # Actual processing
    return process_items(items)
```

### Validation
Validate data before bulk operations:

```python
def validate_bulk_data(items):
    """Validate items before bulk processing"""
    errors = []
    
    for i, item in enumerate(items):
        item_errors = validate_item(item)
        if item_errors:
            errors.append({
                'index': i,
                'item': item,
                'errors': item_errors
            })
    
    if errors:
        print(f"Validation failed for {len(errors)} items")
        return False, errors
    
    return True, []
```

### Rollback Support
Track changes for potential rollback:

```python
class BulkOperationWithRollback:
    def __init__(self):
        self.changes = []
    
    def execute(self, operations):
        """Execute operations with rollback tracking"""
        for op in operations:
            # Save current state
            current = self.get_current_state(op['id'])
            
            try:
                # Apply change
                result = self.apply_change(op)
                
                # Track for rollback
                self.changes.append({
                    'id': op['id'],
                    'before': current,
                    'after': result
                })
            except Exception as e:
                # Rollback previous changes
                self.rollback()
                raise
    
    def rollback(self):
        """Rollback all changes"""
        for change in reversed(self.changes):
            self.apply_change({
                'id': change['id'],
                'data': change['before']
            })
```

## Best Practices

1. **Always validate first** - Check data before processing
2. **Use batching** - Don't overload the API
3. **Implement progress tracking** - Show operation status
4. **Log everything** - Keep detailed operation logs
5. **Test with small batches** - Verify logic before full run
6. **Handle partial failures** - Don't stop on first error
7. **Provide rollback** - Be able to undo changes
8. **Use GraphQL for efficiency** - Minimize API calls

## Example: Complete Bulk Price Update

```python
#!/usr/bin/env python3
"""
Bulk update prices for products in a collection
"""

import os
import sys
from datetime import datetime
from services.shopify_api import ShopifyAPI

def bulk_update_collection_prices(collection_handle, adjustment_percent):
    """Update all prices in a collection by percentage"""
    
    api = ShopifyAPI()
    
    # Get collection
    collection = api.get_collection_by_handle(collection_handle)
    if not collection:
        print(f"Collection '{collection_handle}' not found")
        return
    
    # Get products
    products = api.get_collection_products(collection['id'])
    print(f"Found {len(products)} products in collection")
    
    # Prepare updates
    updates = []
    for product in products:
        for variant in product['variants']:
            old_price = float(variant['price'])
            new_price = old_price * (1 + adjustment_percent / 100)
            
            updates.append({
                'id': variant['id'],
                'old_price': old_price,
                'new_price': new_price
            })
    
    # Confirm
    print(f"Will update {len(updates)} variants")
    sample = updates[:3]
    for update in sample:
        print(f"  {update['old_price']} → {update['new_price']}")
    
    if input("Continue? (y/n): ").lower() != 'y':
        print("Cancelled")
        return
    
    # Execute updates
    success = 0
    failed = 0
    
    for update in updates:
        try:
            api.update_variant_price(update['id'], update['new_price'])
            success += 1
        except Exception as e:
            print(f"Failed to update variant {update['id']}: {e}")
            failed += 1
    
    # Report
    print(f"\nCompleted:")
    print(f"  Success: {success}")
    print(f"  Failed: {failed}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: bulk_price_update.py <collection_handle> <adjustment_percent>")
        sys.exit(1)
    
    bulk_update_collection_prices(sys.argv[1], float(sys.argv[2]))
```