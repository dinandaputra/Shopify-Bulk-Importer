# Shopify Bulk Importer

A Streamlit-based web application for MyByte International that streamlines the process of creating used electronics products in Shopify. This tool replaces manual CSV workflows and reduces data entry time by 50%.

## Overview

The Shopify Bulk Importer enables staff to efficiently input product data for used electronics (smartphones and laptops) and create products directly in Shopify via API integration. The application includes intelligent templates, automated metafield management, and robust data validation.

## Features

- **Direct Shopify Integration**: Create products instantly via REST/GraphQL APIs
- **Smart Product Templates**: Pre-defined templates with auto-population for iPhones and laptops
- **Metafield Management**: Automated metafield creation with metaobject references
- **Unique Handle Generation**: Auto-generates handles in format `{brand}-{model}-{specs}-{YYMMDD}-{counter}`
- **Real-time Validation**: Business rule validation with clear error messages
- **Multi-variant Support**: SIM carrier variants for smartphones with inventory distribution
- **Session Management**: Batch process up to 10 products per session
- **CSV Export**: Fallback option for manual Shopify import

## Tech Stack

- **Framework**: Streamlit (>=1.28.0)
- **Language**: Python 3.x
- **Data Validation**: Pydantic (>=2.0.0)
- **Data Processing**: Pandas (>=2.0.0)
- **API Integration**: ShopifyAPI (>=12.0.0)
- **HTTP Requests**: Requests (>=2.28.0)
- **Date Utilities**: python-dateutil (>=2.8.0)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shopify-bulk-importer.git
cd shopify-bulk-importer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export SHOPIFY_ACCESS_TOKEN="your_token_here"
export SHOPIFY_API_KEY="your_api_key_here"
export SHOPIFY_API_SECRET="your_api_secret_here"
export SHOPIFY_SHOP_DOMAIN="your-shop.myshopify.com"
```

Or create a `.env` file:
```env
SHOPIFY_ACCESS_TOKEN=your_token_here
SHOPIFY_API_KEY=your_api_key_here
SHOPIFY_API_SECRET=your_api_secret_here
SHOPIFY_SHOP_DOMAIN=your-shop.myshopify.com
```

## Quick Start

1. Run the Streamlit application:
```bash
streamlit run streamlit_app.py
```

2. Navigate to `http://localhost:8501` in your browser

3. Choose a product category (Smartphone or Laptop)

4. Fill in the product details or select a template

5. Click "Create in Shopify" to create the product directly

## Product Categories

### Smartphones
- **Supported Brands**: iPhone, Samsung Galaxy, Oppo, and more
- **Templates**: Pre-configured for all iPhone models (XR/XS to iPhone 16)
- **SIM Variants**: SIM Free, Softbank (-), Docomo (-), AU (-), Rakuten Mobile (-)
- **Metafields**: Product rank, inclusions, RAM size, cosmetic condition

### Laptops
- **Supported Brands**: ASUS, Dell, HP, Lenovo, Apple, MSI, Acer
- **Specifications**: CPU, RAM, GPU, Display, Storage, OS, Keyboard
- **Templates**: Popular models with auto-populated specs
- **Inclusions**: Power adapter, laptop bag, mouse options

## Project Structure

```
shopify-bulk-importer/
├── streamlit_app.py          # Main application entry point
├── pages/                    # Streamlit pages
│   ├── smartphone_entry.py   # Smartphone product entry
│   └── laptop_entry.py       # Laptop product entry
├── models/                   # Pydantic data models
│   ├── smartphone.py         # Smartphone validation
│   └── laptop.py            # Laptop validation
├── services/                 # Business logic
│   ├── shopify_api.py       # Core Shopify API client
│   ├── product_service.py   # Product creation orchestration
│   └── ...                  # Other service modules
├── config/                   # Configuration files
│   ├── master_data.py       # Product templates
│   ├── shopify_config.py    # API configuration
│   └── ...                  # Metafield mappings
└── utils/                    # Utility functions
```

## Configuration

### Shopify Store Settings
- **Store**: jufbtk-ut.myshopify.com
- **Currency**: JPY (Japanese Yen)
- **API Version**: 2025-07
- **Default Status**: Draft
- **Inventory**: Tracked by Shopify

### Handle Format
Handles are automatically generated with daily counters:
```
{brand}-{model}-{specs}-{YYMMDD}-{counter}
```
Example: `apple-iphone-15-pro-max-256gb-250730-001`

## Common Commands

```bash
# Run the application
streamlit run streamlit_app.py

# Install dependencies
pip install -r requirements.txt

# Run tests (when available)
python -m pytest tests/

# Check code quality
python -m black .
python -m flake8 .
```

## Troubleshooting

### API Connection Issues
- Verify all environment variables are set correctly
- Check your Shopify access token has necessary permissions
- Ensure the shop domain includes `.myshopify.com`

### Metafield Errors
- Confirm metafield definitions exist in Shopify admin
- Check metaobject IDs match your store's configuration
- Review logs in `logs/missing_metaobjects.json`

### Product Creation Failures
- Verify required fields are filled (title, brand, model, price)
- Check for rate limiting (wait 1-2 seconds between requests)
- Review error messages in the Streamlit interface

### Session Issues
- Clear session if you hit the 10-product limit
- Use the "Clear Session" button in the sidebar
- Refresh the page if the UI becomes unresponsive

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure all tests pass and follow the existing code style.

## Support

For issues, questions, or feature requests:
- Check existing GitHub issues
- Create a new issue with detailed information
- Contact the development team

## License

This project is proprietary software owned by MyByte International. All rights reserved.

## Acknowledgments

- Shopify API team for excellent documentation
- Streamlit team for the intuitive web framework
- All contributors who have helped improve this tool