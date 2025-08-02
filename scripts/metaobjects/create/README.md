# Create Metaobject Scripts

Scripts for creating new metaobjects in Shopify.

## Available Scripts

### create_laptop_metaobjects_final.py
Creates all laptop-related metaobjects (processors, graphics cards, displays, etc.) in Shopify.

**Usage:**
```bash
python scripts/metaobjects/create/create_laptop_metaobjects_final.py
```

**Features:**
- Creates metaobjects for all laptop components
- Supports dry-run mode for testing
- Handles rate limiting automatically
- Generates creation report

### laptop_metaobject_data.py
Data definitions for laptop metaobjects. This is imported by the creation script.

**Contains:**
- Processor definitions (Intel, AMD, Apple)
- Graphics card definitions (NVIDIA, AMD, Intel)
- Display specifications
- Storage options
- RAM configurations

## Creating New Metaobject Scripts

When creating scripts for new product categories:

1. **Define the data structure** in a separate data file
2. **Use GraphQL mutations** for efficiency
3. **Include validation** to prevent duplicates
4. **Log all operations** with timestamps
5. **Handle errors gracefully** with clear messages

## Example Template

```python
#!/usr/bin/env python3
"""
Create [Category] Metaobjects

This script creates metaobjects for [category] products.
"""

import os
from services.shopify_api import ShopifyAPI
from [category]_metaobject_data import METAOBJECT_DATA

def create_metaobjects():
    api = ShopifyAPI()
    
    for definition_type, entries in METAOBJECT_DATA.items():
        print(f"Creating {definition_type} metaobjects...")
        
        for entry in entries:
            try:
                # Create metaobject
                result = api.create_metaobject(definition_type, entry)
                print(f"✅ Created: {entry['display_name']}")
            except Exception as e:
                print(f"❌ Failed: {entry['display_name']} - {str(e)}")

if __name__ == "__main__":
    create_metaobjects()
```

## Notes

- Always check if metaobjects already exist before creating
- Some metaobjects (like colors) may require manual creation in Shopify Admin
- Keep data files versioned for rollback capability