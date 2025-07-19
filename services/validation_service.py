from typing import List, Dict, Any
from models.smartphone import SmartphoneProduct
from pydantic import ValidationError

class ValidationResult:
    """Holds validation results with errors and warnings"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.is_valid: bool = True
    
    def add_error(self, message: str):
        """Add an error message"""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """Add a warning message"""
        self.warnings.append(message)
    
    def has_errors(self) -> bool:
        """Check if there are any errors"""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings"""
        return len(self.warnings) > 0

def validate_smartphone_data(form_data: Dict[str, Any]) -> ValidationResult:
    """
    Validate smartphone form data before creating product
    
    Args:
        form_data: Dictionary containing form field values
        
    Returns:
        ValidationResult with errors and warnings
    """
    result = ValidationResult()
    
    # Required field validation
    if not form_data.get("title") or str(form_data.get("title")).strip() == "":
        result.add_error("Title is required")
    
    if not form_data.get("brand"):
        result.add_error("Brand is required")
    
    if not form_data.get("model") or str(form_data.get("model")).strip() == "":
        result.add_error("Model is required")
    
    # Price validation
    try:
        price = float(form_data.get("price", 0))
        if price <= 0:
            result.add_error("Price must be greater than 0")
    except (ValueError, TypeError):
        result.add_error("Price must be a valid number")
    
    # Business rule warnings (don't block submission)
    if not form_data.get("sim_carriers"):
        result.add_warning("SIM Carriers not selected (recommended for better searchability)")
    
    if not form_data.get("product_rank"):
        result.add_warning("Product Rank not selected (helps customers understand condition)")
    
    # Data format validation
    title = form_data.get("title")
    if title and len(str(title).strip()) > 255:
        result.add_error("Title too long (maximum 255 characters)")
    
    # Multi-select validation
    inclusions = form_data.get("product_inclusions", [])
    if inclusions and not isinstance(inclusions, list):
        result.add_error("Product inclusions must be a list")
    
    minus = form_data.get("minus", [])
    if minus and not isinstance(minus, list):
        result.add_error("Minus options must be a list")
    
    return result

def validate_product_model(product_data: Dict[str, Any]) -> ValidationResult:
    """
    Validate using Pydantic model
    
    Args:
        product_data: Dictionary containing product data
        
    Returns:
        ValidationResult with model validation results
    """
    result = ValidationResult()
    
    try:
        # Try to create product instance
        SmartphoneProduct(**product_data)
    except ValidationError as e:
        for error in e.errors():
            field = error.get("loc", ["unknown"])[0]
            message = error.get("msg", "Invalid value")
            result.add_error(f"{field}: {message}")
    except Exception as e:
        result.add_error(f"Validation error: {str(e)}")
    
    return result

def validate_csv_export(products: List[SmartphoneProduct]) -> ValidationResult:
    """
    Validate products before CSV export
    
    Args:
        products: List of SmartphoneProduct instances
        
    Returns:
        ValidationResult with export validation results
    """
    result = ValidationResult()
    
    if not products:
        result.add_error("No products to export")
        return result
    
    # Check for duplicate handles (shouldn't happen with daily counter)
    handles = [p.handle for p in products if p.handle]
    if len(handles) != len(set(handles)):
        result.add_warning("Duplicate handles detected (may cause import issues)")
    
    # Validate each product
    for i, product in enumerate(products):
        try:
            # Ensure all required fields are present
            if not product.title:
                result.add_error(f"Product {i+1}: Missing title")
            
            if not product.handle:
                result.add_error(f"Product {i+1}: Missing handle")
            
            if product.price <= 0:
                result.add_error(f"Product {i+1}: Invalid price")
            
            # Test CSV row generation
            product.to_csv_row()
            
        except Exception as e:
            result.add_error(f"Product {i+1}: Export error - {str(e)}")
    
    return result