# Data Migration Scripts

Scripts for migrating data between different systems and formats.

## Purpose

Data migration scripts handle:
- Import from legacy systems
- Export to different formats
- Data transformation and cleaning
- Format conversions (CSV, JSON, XML)
- Database migrations

## Common Migration Tasks

### CSV Import
Import products from CSV files:

```python
def import_products_from_csv(csv_file):
    """Import products from CSV file"""
    import csv
    
    products = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            product = {
                'title': row['Product Title'],
                'vendor': row['Brand'],
                'product_type': row['Category'],
                'tags': row['Tags'].split(','),
                'variants': [{
                    'price': row['Price'],
                    'sku': row['SKU'],
                    'inventory_quantity': int(row['Stock'])
                }]
            }
            products.append(product)
    
    return products
```

### JSON Export
Export products to JSON format:

```python
def export_products_to_json(products, output_file):
    """Export products to JSON file"""
    import json
    
    export_data = {
        'export_date': datetime.now().isoformat(),
        'total_products': len(products),
        'products': products
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {len(products)} products to {output_file}")
```

### Data Transformation
Transform data between different schemas:

```python
def transform_legacy_to_shopify(legacy_product):
    """Transform legacy product format to Shopify format"""
    
    # Map legacy fields to Shopify fields
    shopify_product = {
        'title': legacy_product['name'],
        'body_html': legacy_product['description'],
        'vendor': legacy_product['manufacturer'],
        'product_type': map_category(legacy_product['category_id']),
        'tags': extract_tags(legacy_product),
        'variants': transform_variants(legacy_product['variations']),
        'images': transform_images(legacy_product['photos']),
        'metafields': extract_metafields(legacy_product)
    }
    
    return shopify_product

def map_category(legacy_category_id):
    """Map legacy category IDs to Shopify product types"""
    category_map = {
        '1': 'Electronics',
        '2': 'Computers',
        '3': 'Mobile Phones',
        # ... more mappings
    }
    return category_map.get(legacy_category_id, 'Other')
```

## Migration Patterns

### Incremental Migration
Migrate data in chunks:

```python
def incremental_migration(source_data, chunk_size=100):
    """Migrate data incrementally"""
    
    # Track progress
    migration_state = load_migration_state()
    start_index = migration_state.get('last_processed', 0)
    
    total = len(source_data)
    
    for i in range(start_index, total, chunk_size):
        chunk = source_data[i:i+chunk_size]
        
        try:
            # Process chunk
            migrated = process_chunk(chunk)
            
            # Save to destination
            save_to_destination(migrated)
            
            # Update state
            migration_state['last_processed'] = i + len(chunk)
            save_migration_state(migration_state)
            
            print(f"Processed {i+len(chunk)}/{total} items")
            
        except Exception as e:
            print(f"Error at index {i}: {e}")
            break
```

### Data Validation
Validate data during migration:

```python
def validate_migrated_data(source, migrated):
    """Validate migrated data against source"""
    
    validation_report = {
        'total_source': len(source),
        'total_migrated': len(migrated),
        'missing_items': [],
        'data_mismatches': []
    }
    
    # Check for missing items
    source_ids = {item['id'] for item in source}
    migrated_ids = {item['source_id'] for item in migrated}
    
    missing = source_ids - migrated_ids
    validation_report['missing_items'] = list(missing)
    
    # Check data integrity
    for source_item in source:
        migrated_item = find_migrated_item(migrated, source_item['id'])
        
        if migrated_item:
            mismatches = compare_items(source_item, migrated_item)
            if mismatches:
                validation_report['data_mismatches'].append({
                    'id': source_item['id'],
                    'mismatches': mismatches
                })
    
    return validation_report
```

### Rollback Support
Implement migration rollback:

```python
class MigrationWithRollback:
    def __init__(self, source_system, destination_system):
        self.source = source_system
        self.destination = destination_system
        self.migrated_ids = []
    
    def migrate(self, items):
        """Migrate items with rollback support"""
        try:
            for item in items:
                # Transform data
                transformed = self.transform(item)
                
                # Save to destination
                result = self.destination.create(transformed)
                
                # Track for rollback
                self.migrated_ids.append(result['id'])
                
        except Exception as e:
            print(f"Migration failed: {e}")
            self.rollback()
            raise
    
    def rollback(self):
        """Remove migrated items"""
        print("Rolling back migration...")
        
        for item_id in reversed(self.migrated_ids):
            try:
                self.destination.delete(item_id)
                print(f"Rolled back: {item_id}")
            except Exception as e:
                print(f"Failed to rollback {item_id}: {e}")
```

## Data Cleaning

### Standardize Data
Clean and standardize during migration:

```python
def clean_product_data(product):
    """Clean and standardize product data"""
    
    # Trim whitespace
    product['title'] = product['title'].strip()
    
    # Standardize case
    product['vendor'] = product['vendor'].title()
    
    # Clean HTML
    product['body_html'] = clean_html(product['body_html'])
    
    # Remove duplicates from tags
    product['tags'] = list(set(product['tags']))
    
    # Validate and fix prices
    for variant in product['variants']:
        variant['price'] = str(abs(float(variant['price'])))
    
    # Remove empty fields
    product = {k: v for k, v in product.items() if v}
    
    return product
```

### Handle Encoding Issues
Deal with character encoding:

```python
def fix_encoding(text):
    """Fix common encoding issues"""
    
    # Common replacements
    replacements = {
        'â€™': "'",
        'â€œ': '"',
        'â€': '"',
        'â€"': '-',
        'â€¦': '...'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Try to decode/encode to fix issues
    try:
        text = text.encode('latin-1').decode('utf-8')
    except:
        pass
    
    return text
```

## Best Practices

1. **Always backup** - Keep source data intact
2. **Validate thoroughly** - Check data integrity
3. **Use transactions** - Ensure atomicity where possible
4. **Log everything** - Track what was migrated
5. **Test with samples** - Verify logic with small datasets
6. **Handle duplicates** - Decide on duplicate strategy
7. **Map relationships** - Preserve data relationships
8. **Clean as you go** - Fix data quality issues

## Example: Complete CSV to Shopify Migration

```python
#!/usr/bin/env python3
"""
Migrate products from CSV to Shopify
"""

import csv
import json
from datetime import datetime
from services.shopify_api import ShopifyAPI

class CSVToShopifyMigration:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.api = ShopifyAPI()
        self.results = {
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }
    
    def run(self):
        """Execute the migration"""
        print(f"Starting migration from {self.csv_file}")
        
        # Load and validate data
        products = self.load_csv()
        print(f"Loaded {len(products)} products")
        
        # Validate
        valid_products = self.validate_products(products)
        print(f"Valid products: {len(valid_products)}")
        
        # Migrate
        self.migrate_products(valid_products)
        
        # Report
        self.generate_report()
    
    def load_csv(self):
        """Load products from CSV"""
        products = []
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    product = self.transform_row(row)
                    products.append(product)
                except Exception as e:
                    self.results['errors'].append({
                        'row': row,
                        'error': str(e)
                    })
        
        return products
    
    def transform_row(self, row):
        """Transform CSV row to Shopify product"""
        return {
            'title': row['Product Name'],
            'body_html': row['Description'],
            'vendor': row['Brand'],
            'product_type': row['Category'],
            'tags': [tag.strip() for tag in row['Tags'].split(',')],
            'published': row['Status'] == 'Active',
            'variants': [{
                'price': row['Price'],
                'sku': row['SKU'],
                'inventory_quantity': int(row['Stock']),
                'inventory_management': 'shopify'
            }]
        }
    
    def validate_products(self, products):
        """Validate products before migration"""
        valid = []
        
        for product in products:
            errors = []
            
            # Required fields
            if not product.get('title'):
                errors.append('Missing title')
            
            if not product.get('variants'):
                errors.append('No variants')
            
            # Validate price
            for variant in product.get('variants', []):
                try:
                    float(variant['price'])
                except:
                    errors.append('Invalid price')
            
            if errors:
                self.results['skipped'] += 1
                self.results['errors'].append({
                    'product': product.get('title', 'Unknown'),
                    'errors': errors
                })
            else:
                valid.append(product)
        
        return valid
    
    def migrate_products(self, products):
        """Migrate products to Shopify"""
        for i, product in enumerate(products):
            try:
                print(f"Migrating {i+1}/{len(products)}: {product['title']}")
                
                result = self.api.create_product(product)
                
                if result:
                    self.results['success'] += 1
                else:
                    self.results['failed'] += 1
                    
            except Exception as e:
                self.results['failed'] += 1
                self.results['errors'].append({
                    'product': product['title'],
                    'error': str(e)
                })
            
            # Rate limiting
            if (i + 1) % 10 == 0:
                time.sleep(1)
    
    def generate_report(self):
        """Generate migration report"""
        print("\n=== Migration Report ===")
        print(f"Success: {self.results['success']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Skipped: {self.results['skipped']}")
        
        if self.results['errors']:
            print(f"\nErrors ({len(self.results['errors'])}):")
            for error in self.results['errors'][:5]:
                print(f"  - {error}")
        
        # Save detailed report
        report_file = f"migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nDetailed report saved to: {report_file}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: csv_migration.py <csv_file>")
        sys.exit(1)
    
    migration = CSVToShopifyMigration(sys.argv[1])
    migration.run()
```