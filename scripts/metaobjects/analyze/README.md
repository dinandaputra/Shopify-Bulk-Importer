# Analyze Metaobject Scripts

Scripts for analyzing metaobject usage, finding gaps, and generating reports.

## Purpose

These scripts help identify:
- Missing metaobject mappings
- Unused metaobjects
- Frequency of metaobject usage
- Gaps between product data and available metaobjects

## Common Analysis Tasks

### Gap Analysis
Identify products that reference non-existent metaobjects:

```python
def analyze_missing_mappings():
    """Find all missing metaobject references in products"""
    # 1. Load product data
    # 2. Extract metaobject references
    # 3. Check against existing metaobjects
    # 4. Report missing entries
```

### Usage Frequency Analysis
Determine which metaobjects are most/least used:

```python
def analyze_usage_frequency():
    """Count metaobject usage across all products"""
    # 1. Query all products
    # 2. Count metaobject references
    # 3. Generate frequency report
```

### Cross-Reference Analysis
Compare template definitions with existing metaobjects:

```python
def cross_reference_templates():
    """Compare product templates with Shopify metaobjects"""
    # 1. Load template definitions
    # 2. Query Shopify metaobjects
    # 3. Identify gaps
    # 4. Generate creation scripts
```

## Report Generation

Analysis scripts should generate reports in multiple formats:

### Human-Readable Markdown
```markdown
# Missing Metaobjects Report

## Summary
- Total missing: 45
- Categories affected: 3
- Most common missing: "Intel Core i7-13700H"

## Details by Category
### Processors (25 missing)
- Intel Core i7-13700H (5 occurrences)
- AMD Ryzen 7 7840HS (3 occurrences)
...
```

### Machine-Readable JSON
```json
{
    "summary": {
        "total_missing": 45,
        "categories": ["processor", "graphics", "display"]
    },
    "missing_entries": {
        "processor": {
            "Intel Core i7-13700H": {
                "count": 5,
                "first_seen": "2025-07-28",
                "products": ["laptop-123", "laptop-456"]
            }
        }
    }
}
```

### Actionable Scripts
Generate scripts to create missing metaobjects:

```python
# generated_create_missing.py
MISSING_METAOBJECTS = {
    "laptop_processor": [
        {"display_name": "Intel Core i7-13700H", "type": "processor"},
        {"display_name": "AMD Ryzen 7 7840HS", "type": "processor"}
    ]
}
```

## Best Practices

1. **Run regularly** - Schedule weekly/monthly analysis
2. **Track trends** - Monitor growth in missing entries
3. **Automate fixes** - Generate scripts for common issues
4. **Alert on thresholds** - Notify when missing entries exceed limits
5. **Version reports** - Keep historical data for comparison

## Integration with Logging

These scripts should integrate with the missing metaobjects logger:

```python
from config.laptop_metafield_mapping_enhanced import missing_logger

# Use existing log data
report = missing_logger.get_report()

# Analyze patterns
trends = analyze_trends(report)
```