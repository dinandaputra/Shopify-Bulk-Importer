# Smartphone Entry Guide

This guide walks you through the process of creating smartphone products in the Shopify Bulk Importer.

## Overview

The smartphone entry system is designed to streamline the process of adding used smartphones to your Shopify store. With intelligent templates and automatic field population, you can create products in under 2 minutes.

## Getting Started

1. Launch the application: `streamlit run streamlit_app.py`
2. Navigate to "Smartphone Entry" from the sidebar
3. Choose between manual entry or template selection

## Using Templates

### Available Templates

The system includes pre-configured templates for:
- **iPhone Models**: All models from iPhone XR/XS to iPhone 16 series
- **Samsung Galaxy**: S series, Note series, A series
- **Other Brands**: Oppo, Xiaomi, Google Pixel, etc.

### Template Selection Process

1. **Select a Template**: Choose from the dropdown menu
   - Example: "iPhone 15 Pro Max 256GB [Desert Titanium]"

2. **Auto-Population**: The following fields are automatically filled:
   - Brand (e.g., "Apple")
   - Model (e.g., "iPhone 15 Pro Max")
   - Storage (e.g., "256GB")
   - Color (e.g., "Desert Titanium")
   - Title (e.g., "Apple iPhone 15 Pro Max (5G) 256GB [Desert Titanium]")

3. **5G Detection**: The system automatically adds "(5G)" to compatible models:
   - iPhone 12 and later
   - Samsung Galaxy S20 and later
   - Other 5G-capable devices

## Manual Entry Fields

### Required Fields

1. **Title**: Product display name
   - Auto-generated from template or manually entered
   - Format: "[Brand] [Model] (5G) [Storage] [Color]"

2. **Price (JPY)**: Product price in Japanese Yen
   - No decimal places required
   - Example: 150000 for ¥150,000

3. **Product Rank**: Condition rating
   - A: Excellent condition
   - B: Good condition
   - C: Fair condition
   - D: Poor condition

### Optional Fields

1. **Condition Description**: Detailed condition notes
   - Describe any scratches, dents, or issues
   - Mention what's been replaced or repaired

2. **RAM Size**: Memory capacity
   - 4GB, 6GB, 8GB, 12GB, 16GB

3. **Minus Points**: Cosmetic or functional issues
   - Light scratches
   - Deep scratches
   - Dents
   - Battery issues
   - Screen issues

4. **Product Inclusions**: What's included
   - Full set cable (auto-selects related items)
   - Original box
   - Manual book
   - Bonus adapter
   - Bonus softcase
   - Bonus anti gores

5. **Collections**: Product categories
   - Default: "All Products" + brand collection
   - Automatically set based on brand
   - Can be customized

## SIM Carrier Variants

### Understanding Variants

Each smartphone can have multiple SIM carrier variants:
- **SIM Free**: Unlocked, works with any carrier
- **Softbank (-)**: Locked to Softbank
- **Docomo (-)**: Locked to Docomo
- **AU (-)**: Locked to AU
- **Rakuten Mobile (-)**: Locked to Rakuten

### How to Select Variants

1. Check the boxes for available variants
2. At least one variant must be selected
3. Inventory is automatically distributed evenly

### Examples

- **Single Variant**: Only "SIM Free" → 1 variant with full inventory
- **Two Variants**: "SIM Free" + "Softbank (-)" → 2 variants, 50% inventory each
- **All Variants**: All 5 options → 5 variants, 20% inventory each

## Smart Inclusions Mapping

The system uses intelligent mapping for inclusions:

### Full Set Cable
When you select "Full set cable", it automatically includes:
- Full set cable
- Bonus adapter
- Bonus softcase
- Bonus anti gores

This saves time and ensures consistency.

## Image Upload

### Supported Formats
- JPG/JPEG
- PNG
- WebP
- GIF

### Upload Process
1. Click "Upload Images" or drag & drop
2. Multiple images can be uploaded
3. Images are automatically uploaded to Shopify CDN
4. First image becomes the main product image

### Best Practices
- Use high-quality images (1000x1000px or larger)
- Show the product from multiple angles
- Include images of any damage or wear
- Maximum 10 images per product

## Creating the Product

### Pre-Creation Checklist
- ✓ All required fields filled
- ✓ Price is positive number
- ✓ At least one SIM variant selected
- ✓ Product rank selected
- ✓ Images uploaded (optional but recommended)

### Creation Process
1. Click "Create Product in Shopify"
2. Wait for API response (2-5 seconds)
3. Success message appears with product details
4. Product is added to session list

### What Happens Behind the Scenes
1. Product created in Shopify (draft status)
2. Variants created based on SIM selections
3. Inventory distributed across variants
4. Metafields assigned (rank, inclusions, RAM, etc.)
5. Images uploaded and attached
6. Collections assigned

## Session Management

### Session Features
- View all products created in current session
- Maximum 10 products per session
- Edit products before final submission
- Export session to CSV

### Session Actions
- **Clear Session**: Remove all products and start fresh
- **Export CSV**: Download session as CSV file
- **View in Shopify**: Links to products in admin

## Troubleshooting

### Common Issues

#### "Product creation failed"
- Check all required fields are filled
- Verify price is a positive number
- Ensure at least one SIM variant is selected

#### "Metafield assignment failed"
- Non-critical error, product still created
- Check Shopify admin for metafield definitions
- Contact support if persistent

#### "Image upload failed"
- Check image format is supported
- Verify file size < 20MB
- Try uploading fewer images

#### "Session full"
- Maximum 10 products reached
- Clear session or export and start new

### Tips for Efficiency

1. **Use Templates**: 70% faster than manual entry
2. **Prepare Images**: Have them ready before starting
3. **Batch Similar Products**: Group by brand/model
4. **Use Keyboard Shortcuts**: Tab through fields
5. **Check Session Regularly**: Don't lose work

## Advanced Features

### Bulk Operations
- Select multiple products in session
- Apply changes to all selected
- Bulk export or delete

### Custom Templates
Contact development team to add new templates for frequently used models

### API Integration
Products are created via Shopify REST API with GraphQL for metafields

## Best Practices

1. **Accurate Descriptions**: Be honest about condition
2. **Consistent Ranking**: Use the same criteria for all products
3. **Complete Information**: Fill all relevant fields
4. **Quality Images**: Show actual product condition
5. **Regular Saves**: Export session periodically

## FAQ

**Q: Can I edit a product after creation?**
A: Yes, click on the product in session list to edit before final submission

**Q: What happens to products in draft status?**
A: They remain hidden from customers until published in Shopify admin

**Q: Can I import multiple products at once?**
A: Currently one at a time, but session supports up to 10 products

**Q: How do I delete a product?**
A: Remove from session or delete directly in Shopify admin

**Q: Can I save templates?**
A: System templates are pre-configured, contact support for additions

## Getting Help

- Check error messages for specific issues
- Review this guide for feature details
- Contact support team for technical issues
- Submit feature requests via GitHub