# Laptop Entry Guide

This guide provides comprehensive instructions for creating laptop products in the Shopify Bulk Importer.

## Overview

The laptop entry system streamlines the process of adding used laptops to your Shopify store. With detailed specification templates and automatic metafield mapping, you can create complete product listings quickly and accurately.

## Getting Started

1. Launch the application: `streamlit run streamlit_app.py`
2. Navigate to "Laptop Entry" from the sidebar
3. Choose between manual entry or template selection

## Using Templates

### Available Brands and Models

The system includes templates for major laptop brands:
- **ASUS**: ROG, TUF Gaming, VivoBook, ZenBook series
- **Dell**: XPS, Inspiron, Latitude, Precision series
- **HP**: Pavilion, Envy, Omen, EliteBook series
- **Lenovo**: ThinkPad, IdeaPad, Legion, Yoga series
- **Apple**: MacBook Air, MacBook Pro (Intel and M-series)
- **MSI**: Gaming and Creator series
- **Acer**: Aspire, Predator, Swift series

### Template Format

Templates follow this naming convention:
```
[Brand] [Model] [CPU/RAM/GPU/Display/Storage] [Color]
```

Example:
```
ASUS ROG Strix G16 [i7-13700H/16GB/RTX4060/16inch/1TB] [Eclipse Gray]
```

### Auto-Population from Templates

When you select a template, these fields are automatically filled:
- Brand (e.g., "ASUS")
- Model (e.g., "ROG Strix G16")
- CPU (e.g., "Intel Core i7-13700H")
- RAM (e.g., "16GB")
- GPU (e.g., "NVIDIA GeForce RTX 4060")
- Display (e.g., "16-inch FHD (144Hz)")
- Storage (e.g., "1TB SSD")
- Color (e.g., "Eclipse Gray")

## Manual Entry Fields

### Required Fields

1. **Title**: Product display name
   - Auto-generated from specifications
   - Format: "[Brand] [Model] [Key Specs]"
   - Can be manually edited

2. **Brand**: Manufacturer name
   - Select from dropdown
   - Determines collection assignment

3. **Model**: Specific model name
   - Include series and model number
   - Example: "ROG Strix G16 2023"

4. **Price (JPY)**: Product price
   - Japanese Yen without decimals
   - Example: 180000 for ¥180,000

5. **Product Rank**: Condition rating
   - A: Like new
   - B: Excellent
   - C: Good
   - D: Fair

### Specification Fields

#### CPU (Processor)
- Full processor name with generation
- Examples:
  - "Intel Core i7-13700H"
  - "AMD Ryzen 7 7840HS"
  - "Apple M2 Pro"

#### RAM (Memory)
- Capacity in GB
- Options: 4GB, 8GB, 16GB, 32GB, 64GB
- Include type if relevant (DDR4/DDR5)

#### GPU (Graphics)
- Full graphics card name
- Examples:
  - "NVIDIA GeForce RTX 4060"
  - "Intel Iris Xe Graphics"
  - "AMD Radeon RX 6700M"

#### Display
- Size and specifications
- Format: "[Size]-inch [Resolution] ([Refresh Rate])"
- Examples:
  - "15.6-inch FHD (144Hz)"
  - "14-inch QHD (60Hz)"
  - "16-inch 4K (120Hz)"

#### Storage
- Type and capacity
- Examples:
  - "512GB SSD"
  - "1TB SSD + 1TB HDD"
  - "256GB NVMe SSD"

#### Operating System
- Current OS installed
- Options:
  - Windows 11 (Home/Pro)
  - Windows 10 (Home/Pro)
  - macOS Ventura/Sonoma
  - No OS

#### Keyboard
- **Layout**: US, UK, Japanese
- **Backlight**: None, White, RGB

### Optional Fields

1. **Condition Description**
   - Detailed condition notes
   - Mention any defects or replacements
   - Note upgrade history

2. **Color**
   - Laptop color/finish
   - Must match predefined options

3. **Product Inclusions**
   - Power adapter (original/compatible)
   - Laptop bag
   - Mouse (wireless/wired)
   - Additional accessories

4. **Collections**
   - Auto-assigned: "All Products" + brand
   - Can add custom collections

## Specification Templates

### Gaming Laptops
Typically include:
- High-performance CPU (i7/i9, Ryzen 7/9)
- Dedicated GPU (RTX 3060 or better)
- 144Hz+ display
- 16GB+ RAM
- RGB keyboard

### Business Laptops
Usually feature:
- Efficient CPU (i5/i7, Ryzen 5/7)
- Integrated or entry-level GPU
- Standard 60Hz display
- 8-16GB RAM
- Professional design

### Creative Workstations
Often have:
- Powerful CPU (i9, Xeon, Ryzen 9)
- Professional GPU (RTX A-series, Quadro)
- High-resolution display (4K)
- 32GB+ RAM
- Color-accurate screen

## Metafield Mapping

### How It Works

The system automatically maps specifications to Shopify metaobjects:

1. **Processor Metafields**
   - Maps CPU model to processor metaobject
   - Example: "Intel Core i7-13700H" → GID reference

2. **Graphics Metafields**
   - Maps GPU to graphics metaobject
   - Handles both integrated and dedicated GPUs

3. **Display Metafields**
   - Maps display specs to display metaobject
   - Includes size, resolution, refresh rate

4. **Other Metafields**
   - RAM size (text field)
   - Storage (text field)
   - OS (metaobject reference)

### Missing Metaobject Handling

If a specification doesn't have a metaobject:
1. System logs it to `logs/missing_metaobjects.json`
2. Product is still created successfully
3. Admin can create missing metaobject later

## Creating the Product

### Pre-Creation Checklist
- ✓ All required fields completed
- ✓ Specifications make sense together
- ✓ Price is reasonable for specs
- ✓ Condition accurately described

### Creation Process
1. Review all entered information
2. Click "Create Product in Shopify"
3. System validates data
4. Creates product with variants
5. Assigns all metafields
6. Uploads images if provided

### Behind the Scenes
1. Product created in draft status
2. Single variant created (unlike smartphones)
3. Specifications mapped to metafields
4. Collections automatically assigned
5. Images processed and attached

## Best Practices

### Accurate Specifications
- Verify CPU model exactly
- Include GPU memory (e.g., "8GB")
- Specify display technology (IPS, OLED)
- Note storage type (SSD vs HDD)

### Condition Assessment
- Check all ports functionality
- Test keyboard and trackpad
- Verify battery health
- Note any cosmetic damage
- Test display for dead pixels

### Pricing Guidelines
Consider:
- Original retail price
- Current market value
- Specification tier
- Condition rating
- Included accessories

## Common Issues and Solutions

### "Metaobject not found"
- Non-critical warning
- Product still created
- Check logs for missing mappings
- Contact admin to add metaobject

### "Invalid specifications"
- Verify CPU/GPU names are correct
- Check RAM is from valid options
- Ensure display format is correct

### "Template not loading"
- Refresh the page
- Check template selection
- Verify template exists in system

## Tips for Efficiency

1. **Use Templates**: 80% faster than manual entry
2. **Batch by Brand**: Process similar laptops together
3. **Prepare Specs**: Have system information ready
4. **Standard Descriptions**: Create condition templates
5. **Quick Keys**: Use Tab to navigate fields

## Advanced Features

### Bulk Specification Entry
- Copy specifications from spreadsheet
- System parses and fills fields
- Verify before submission

### Custom Metafield Mapping
- Add new processor/GPU models
- Contact development for additions
- Automatic learning from logs

### Integration Features
- Direct to Shopify draft products
- Metafield assignment via GraphQL
- Inventory tracking enabled

## Specification Reference

### CPU Naming Conventions
- **Intel**: "Intel Core [i5/i7/i9]-[Generation][Suffix]"
- **AMD**: "AMD Ryzen [5/7/9] [Generation]"
- **Apple**: "Apple [M1/M2/M3] [Pro/Max/Ultra]"

### GPU Categories
- **Integrated**: Intel Iris, AMD Radeon Graphics
- **Entry Gaming**: GTX 1650, RTX 3050
- **Mid Gaming**: RTX 3060, RTX 4060
- **High-End**: RTX 4070+, RX 7900
- **Professional**: RTX A-series, Quadro

### Display Standards
- **HD**: 1366x768
- **FHD**: 1920x1080 (Most common)
- **QHD**: 2560x1440
- **4K**: 3840x2160
- **Refresh**: 60Hz (standard), 120Hz, 144Hz, 165Hz

## FAQ

**Q: How do I add a laptop model not in templates?**
A: Use manual entry and fill all specification fields

**Q: Can I edit specifications after creation?**
A: Yes, in the session list before final submission

**Q: What if my GPU isn't in the list?**
A: Enter it manually, system will log for future addition

**Q: How are laptops different from smartphones?**
A: Single variant, more detailed specs, different metafields

**Q: Can I import laptop specs from other sources?**
A: Currently manual entry only, API import planned

## Getting Help

- Review specification formats in this guide
- Check logs for metaobject mapping issues
- Contact support for template additions
- Submit feature requests via GitHub

## Appendix: Common Laptop Specifications

### Storage Combinations
- Single SSD: "512GB SSD", "1TB SSD"
- Dual drives: "256GB SSD + 1TB HDD"
- High-end: "2TB NVMe SSD"

### RAM Configurations
- Budget: 4GB, 8GB
- Standard: 16GB
- Professional: 32GB, 64GB

### Display Technologies
- TN: Fast, lower quality
- IPS: Better colors, common
- OLED: Best quality, expensive
- Mini-LED: High-end option