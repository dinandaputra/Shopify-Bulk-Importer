import pandas as pd
from io import StringIO
from typing import List
from models.smartphone import SmartphoneProduct
from services.validation_service import validate_csv_export

def export_to_csv(products: List[SmartphoneProduct]) -> str:
    """
    Export products to Shopify-compatible CSV format
    
    Args:
        products: List of SmartphoneProduct instances
        
    Returns:
        CSV string ready for download
        
    Raises:
        ValueError: If validation fails
    """
    # Validate before export
    validation_result = validate_csv_export(products)
    
    if validation_result.has_errors():
        error_msg = "Export validation failed:\n" + "\n".join(validation_result.errors)
        raise ValueError(error_msg)
    
    # Define CSV column headers (exact Shopify format)
    csv_headers = [
        "Handle",
        "Title", 
        "Body HTML",
        "Vendor",
        "Type",
        "Tags",
        "Published",
        "Product Category",
        "Taxable",
        "Variant SKU",
        "Variant Inventory Qty",
        "Variant Inventory Tracker",
        "Variant Price",
        "Variant Barcode",
        "Color (product.metafields.custom.color)",
        "SIM Carriers (product.metafields.custom.sim_carriers)",
        "Minus (product.metafields.custom.minus)",
        "Product Inclusions (product.metafields.custom.product_inclusions)",
        "Product Rank (product.metafields.custom.product_rank)",
        "RAM Size (product.metafields.custom.ram_size)"
    ]
    
    # Convert products to CSV rows
    csv_rows = []
    for product in products:
        csv_row = product.to_csv_row()
        csv_rows.append(csv_row)
    
    # Create DataFrame
    df = pd.DataFrame(csv_rows, columns=csv_headers)
    
    # Convert to CSV string
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_string = csv_buffer.getvalue()
    
    return csv_string

def generate_filename(product_count: int) -> str:
    """
    Generate a filename for CSV export
    
    Args:
        product_count: Number of products in the export
        
    Returns:
        Filename string
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return f"mybyte-smartphones-{timestamp}-{product_count}products.csv"

def export_summary(products: List[SmartphoneProduct]) -> dict:
    """
    Generate export summary statistics
    
    Args:
        products: List of SmartphoneProduct instances
        
    Returns:
        Dictionary with export statistics
    """
    if not products:
        return {
            "total_products": 0,
            "total_value": 0,
            "brands": {},
            "avg_price": 0
        }
    
    # Calculate statistics
    total_products = len(products)
    total_value = sum(p.price for p in products)
    avg_price = total_value / total_products if total_products > 0 else 0
    
    # Brand breakdown
    brands = {}
    for product in products:
        brand = product.brand
        if brand not in brands:
            brands[brand] = {"count": 0, "value": 0}
        brands[brand]["count"] += 1
        brands[brand]["value"] += product.price
    
    return {
        "total_products": total_products,
        "total_value": total_value,
        "brands": brands,
        "avg_price": avg_price
    }

def validate_shopify_import(csv_string: str) -> dict:
    """
    Validate CSV format for Shopify import
    
    Args:
        csv_string: CSV content as string
        
    Returns:
        Dictionary with validation results
    """
    try:
        # Read CSV back to validate structure
        df = pd.read_csv(StringIO(csv_string))
        
        # Check required columns
        required_columns = ["Handle", "Title", "Vendor", "Published", "Variant Price"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return {
                "valid": False,
                "errors": [f"Missing required columns: {', '.join(missing_columns)}"]
            }
        
        # Check for empty handles
        empty_handles = df["Handle"].isna().sum()
        if empty_handles > 0:
            return {
                "valid": False,
                "errors": [f"{empty_handles} products have empty handles"]
            }
        
        # Check for invalid prices
        invalid_prices = df["Variant Price"].isna().sum() + (df["Variant Price"] <= 0).sum()
        if invalid_prices > 0:
            return {
                "valid": False,
                "errors": [f"{invalid_prices} products have invalid prices"]
            }
        
        return {
            "valid": True,
            "row_count": len(df),
            "column_count": len(df.columns)
        }
        
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"CSV validation error: {str(e)}"]
        }