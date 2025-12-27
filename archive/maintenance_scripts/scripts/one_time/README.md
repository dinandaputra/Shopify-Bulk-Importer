# One-Time Scripts

This directory contains scripts that are run once and then archived.

## Purpose

One-time scripts are used for:
- Initial data setup
- One-off migrations
- Temporary fixes
- Data cleanup tasks
- System initialization

## Guidelines

### When to Use This Directory
Place scripts here when they:
1. Will only be run once
2. Are tied to a specific date/event
3. Fix a temporary issue
4. Perform initial setup

### Naming Convention
Use descriptive names with dates:
```
YYYYMMDD_description_of_task.py
```

Examples:
- `20250730_initial_metaobject_creation.py`
- `20250815_fix_duplicate_skus.py`
- `20250901_migrate_legacy_products.py`

### Documentation Requirements
Each script MUST include:
```python
#!/usr/bin/env python3
"""
One-Time Script: [Brief Description]

Purpose: [Detailed explanation of why this script exists]
Date: [YYYY-MM-DD]
Author: [Name/Team]
Ticket/Issue: [Reference number if applicable]

This script will:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Usage:
    python scripts/one_time/YYYYMMDD_script_name.py [options]

IMPORTANT: This script should only be run once. Running it multiple times
may cause [describe potential issues].
"""
```

### Before Running
1. **Backup data** if the script modifies anything
2. **Test in development** environment first
3. **Document the run** in the script header
4. **Get approval** if required by your team

### After Running
Add a completion note to the script:
```python
"""
EXECUTION LOG:
- Date: 2025-07-30
- Executed by: [Name]
- Environment: Production
- Result: Success - processed 1,234 items
- Notes: [Any relevant information]
"""
```

## Archival Process

### When to Archive
Scripts should remain here for:
- 30 days after execution
- Until the next major release
- Until confirmed no rollback needed

### How to Archive
1. Ensure script has execution log
2. Move to `archive/scripts/one_time/`
3. Update any documentation references

## Examples

### Initial Setup Script
```python
#!/usr/bin/env python3
"""
One-Time Script: Initial Shopify Metaobject Setup

Purpose: Create all required metaobject definitions for the new product system
Date: 2025-07-30
Author: Development Team
Ticket: SHOP-123

This script will:
1. Create metaobject definitions
2. Populate initial metaobject entries
3. Verify creation success

Usage:
    python scripts/one_time/20250730_initial_metaobject_setup.py

IMPORTANT: This script should only be run once during initial setup.
Running multiple times will attempt to create duplicate definitions.
"""

import os
from services.shopify_api import ShopifyAPI

def main():
    print("Starting initial metaobject setup...")
    
    api = ShopifyAPI()
    
    # Create definitions
    definitions = [
        {
            'type': 'laptop_processor',
            'name': 'Laptop Processor',
            'fields': [...]
        },
        # More definitions...
    ]
    
    for definition in definitions:
        try:
            result = api.create_metaobject_definition(definition)
            print(f"✅ Created: {definition['name']}")
        except Exception as e:
            print(f"❌ Failed: {definition['name']} - {e}")
    
    print("Setup complete!")

if __name__ == "__main__":
    if input("This will create metaobjects. Continue? (y/n): ").lower() != 'y':
        print("Cancelled")
    else:
        main()

"""
EXECUTION LOG:
- Date: 2025-07-30 14:30 PST
- Executed by: John Doe
- Environment: Production
- Result: Success - created 5 definitions
- Notes: All metaobject definitions created successfully
"""
```

### Data Fix Script
```python
#!/usr/bin/env python3
"""
One-Time Script: Fix Duplicate SKUs

Purpose: Remove duplicate SKUs that were created due to import bug
Date: 2025-08-15
Author: Support Team
Ticket: BUG-456

This script will:
1. Identify all duplicate SKUs
2. Rename duplicates with suffix
3. Generate report of changes

Usage:
    python scripts/one_time/20250815_fix_duplicate_skus.py [--dry-run]

IMPORTANT: This modifies product data. Ensure you have a backup.
"""

def fix_duplicate_skus(dry_run=True):
    # Implementation...
    pass

if __name__ == "__main__":
    import sys
    dry_run = '--dry-run' in sys.argv
    
    if dry_run:
        print("DRY RUN MODE - No changes will be made")
    
    fix_duplicate_skus(dry_run)
```

## Safety Checklist

Before running any one-time script:

- [ ] Tested in development environment
- [ ] Data backed up (if applicable)
- [ ] Script reviewed by another developer
- [ ] Dry-run mode tested (if available)
- [ ] Rollback plan documented
- [ ] Stakeholders notified
- [ ] Execution window scheduled

## Common Patterns

### Confirmation Prompt
```python
def confirm_execution():
    print("This script will make the following changes:")
    print("- Change 1")
    print("- Change 2")
    
    response = input("\nContinue? (yes/no): ")
    return response.lower() == 'yes'

if __name__ == "__main__":
    if not confirm_execution():
        print("Execution cancelled")
        sys.exit(0)
```

### Progress Tracking
```python
def process_with_progress(items):
    total = len(items)
    
    for i, item in enumerate(items):
        print(f"Processing {i+1}/{total}: {item['name']}")
        process_item(item)
        
        if (i + 1) % 100 == 0:
            print(f"Checkpoint: {i+1} items processed")
```

### Rollback Support
```python
def execute_with_rollback():
    changes = []
    
    try:
        # Make changes and track them
        for item in items:
            old_state = get_state(item)
            new_state = apply_change(item)
            changes.append((item, old_state, new_state))
            
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Rolling back changes...")
        
        for item, old_state, _ in reversed(changes):
            restore_state(item, old_state)
        
        raise
```

## Archive Directory

Scripts older than 30 days should be moved to:
```
archive/scripts/one_time/
├── 2025/
│   ├── 07/
│   │   └── 20250701_archived_script.py
│   └── 08/
│       └── 20250815_another_script.py
```

This keeps the active directory clean while preserving historical scripts.