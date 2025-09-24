# Update Metaobject Scripts

Scripts for updating existing metaobjects in Shopify.

## Purpose

Update scripts help with:
- Bulk value updates
- Fixing typos or incorrect mappings
- Adding new fields to existing metaobjects
- Migrating metaobject structures

## Common Update Operations

### Bulk Value Updates
Update multiple metaobjects at once:

```python
def bulk_update_metaobjects(updates):
    """Update multiple metaobjects in a single operation"""
    mutation = """
    mutation metaobjectUpdate($id: ID!, $metaobject: MetaobjectUpdateInput!) {
        metaobjectUpdate(id: $id, metaobject: $metaobject) {
            metaobject {
                id
                displayName
            }
            userErrors {
                field
                message
            }
        }
    }
    """
    # Process updates...
```

### Field Updates
Add or modify fields on existing metaobjects:

```python
def update_metaobject_fields(metaobject_id, field_updates):
    """Update specific fields on a metaobject"""
    # Build field update payload
    # Execute update mutation
```

### Display Name Corrections
Fix typos in metaobject display names:

```python
def fix_display_names(corrections):
    """Fix typos in metaobject display names"""
    # corrections = {"old_name": "new_name"}
    for old_name, new_name in corrections.items():
        # Find metaobject by old name
        # Update to new name
```

## Safety Measures

### Dry Run Mode
Always test updates before applying:

```python
def update_metaobjects(updates, dry_run=True):
    if dry_run:
        print("DRY RUN - No changes will be made")
        for update in updates:
            print(f"Would update: {update}")
    else:
        # Perform actual updates
```

### Backup Before Updates
Create backups of current state:

```python
def backup_metaobjects(definition_type):
    """Export current metaobject state before updates"""
    # Query all metaobjects
    # Save to timestamped file
    # Return backup filename
```

### Validation
Validate updates before applying:

```python
def validate_updates(updates):
    """Validate update data before applying"""
    # Check required fields
    # Verify metaobject exists
    # Validate field types
    # Return validation errors
```

## Update Patterns

### Incremental Updates
Update in small batches to minimize risk:

```python
BATCH_SIZE = 10

for i in range(0, len(updates), BATCH_SIZE):
    batch = updates[i:i+BATCH_SIZE]
    process_batch(batch)
    time.sleep(1)  # Rate limiting
```

### Rollback Support
Keep track of changes for rollback:

```python
def update_with_rollback(updates):
    rollback_data = []
    
    for update in updates:
        # Save current state
        current = get_current_state(update['id'])
        rollback_data.append(current)
        
        # Apply update
        apply_update(update)
    
    # Save rollback data
    save_rollback_data(rollback_data)
```

## Best Practices

1. **Always backup first** - Export current state before updates
2. **Use dry run mode** - Test updates before applying
3. **Update in batches** - Don't update everything at once
4. **Log all changes** - Keep audit trail of updates
5. **Validate data** - Ensure updates are valid before applying
6. **Handle errors gracefully** - Don't stop on first error
7. **Implement rollback** - Be able to undo changes

## Error Handling

```python
def safe_update(metaobject_id, updates):
    try:
        result = api.update_metaobject(metaobject_id, updates)
        if result.get('userErrors'):
            log_error(f"Update failed: {result['userErrors']}")
            return False
        log_success(f"Updated: {metaobject_id}")
        return True
    except Exception as e:
        log_error(f"Exception updating {metaobject_id}: {str(e)}")
        return False
```