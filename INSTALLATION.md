# Installation Guide

This guide provides detailed instructions for setting up the Shopify Bulk Importer application.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Shopify Partner account or store with API access
- Basic command line knowledge

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/shopify-bulk-importer.git
cd shopify-bulk-importer
```

### 2. Set Up Python Virtual Environment

It's recommended to use a virtual environment to avoid dependency conflicts:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

With your virtual environment activated:
```bash
pip install -r requirements.txt
```

This will install:
- streamlit>=1.28.0
- pandas>=2.0.0
- pydantic>=2.0.0
- shopifyapi>=12.0.0
- requests>=2.28.0
- python-dateutil>=2.8.0
- python-dotenv>=0.19.0

### 4. Shopify API Credentials

#### Getting Your Credentials

1. Log in to your Shopify admin panel
2. Go to Settings → Apps and sales channels
3. Click "Develop apps" (you may need to enable this)
4. Create a new app or use an existing one
5. Configure API scopes:
   - `read_products`
   - `write_products`
   - `read_inventory`
   - `write_inventory`
   - `read_metaobjects`
   - `write_metaobjects`
6. Install the app to generate credentials

#### Setting Environment Variables

Create a `.env` file in the project root:

```env
SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SHOPIFY_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SHOPIFY_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SHOPIFY_SHOP_DOMAIN=your-shop.myshopify.com
```

**Alternative: Export as shell variables:**
```bash
export SHOPIFY_ACCESS_TOKEN="shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export SHOPIFY_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export SHOPIFY_API_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export SHOPIFY_SHOP_DOMAIN="your-shop.myshopify.com"
```

### 5. Verify Installation

Test your setup:
```bash
streamlit run streamlit_app.py
```

The application should start and be accessible at `http://localhost:8501`

### 6. Configure Shopify Store

Ensure your Shopify store has the required metafield definitions:

1. **Product-level metafields:**
   - `custom.product_rank` (single_line_text_field)
   - `custom.product_inclusions` (list.metaobject_reference)
   - `custom.ram_size` (single_line_text_field)
   - `custom.minus` (single_line_text_field)

2. **Variant-level metafields:**
   - `custom.sim_carrier` (list.metaobject_reference)

3. **Metaobject definitions required:**
   - Cosmetic condition
   - SIM card capability
   - Operating system
   - Color
   - Subscription type

## Troubleshooting

### Common Issues

#### ImportError: No module named 'streamlit'
- Ensure your virtual environment is activated
- Run `pip install -r requirements.txt` again

#### Shopify API Authentication Failed
- Verify your access token starts with `shpat_`
- Check the token hasn't expired
- Ensure all required API scopes are granted

#### Cannot Connect to Shopify Store
- Verify SHOPIFY_SHOP_DOMAIN includes `.myshopify.com`
- Check your internet connection
- Ensure the store is active and accessible

#### Missing Metafield Errors
- Create required metafield definitions in Shopify admin
- Check the namespace and key match exactly
- Verify metaobject definitions exist

### Getting Help

If you encounter issues:
1. Check the error message in the terminal
2. Review logs in the `logs/` directory
3. Consult the README.md troubleshooting section
4. Create an issue on GitHub with detailed error information

## Next Steps

After successful installation:
1. Read the README.md for usage instructions
2. Review ARCHITECTURE.md to understand the system
3. Check the guides in `docs/guides/` for specific workflows
4. Start creating products!

## Updating

To update to the latest version:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

Always check CHANGELOG.md for breaking changes before updating.