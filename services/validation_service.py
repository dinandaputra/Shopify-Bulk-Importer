import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from collections import defaultdict
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


@dataclass
class MissingMetaobjectEntry:
    """Represents a missing metaobject entry with tracking info"""
    field_name: str
    value: str
    frequency: int
    first_seen: str
    last_seen: str
    context: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


class MissingMetaobjectLogger:
    """
    Handles logging and tracking of missing metaobject entries
    
    This class was migrated from config/laptop_metafield_mapping_enhanced.py
    to provide centralized missing entry tracking functionality.
    """
    
    def __init__(self, log_file_path: str = "logs/missing_metaobjects.json"):
        """Initialize logger with configurable log file path"""
        self.log_file = Path(log_file_path)
        self.log_file.parent.mkdir(exist_ok=True)
        self.missing_entries: Dict[str, Dict[str, MissingMetaobjectEntry]] = {}
        self.session_missing: List[Dict] = []  # Track missing entries for current session
        self._load_existing_log()
        
        # Setup Python logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('MissingMetaobjectLogger')
    
    def _load_existing_log(self):
        """Load existing missing entries from log file"""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert loaded data back to MissingMetaobjectEntry objects
                for field_name, entries in data.get('entries', {}).items():
                    self.missing_entries[field_name] = {}
                    for value, entry_data in entries.items():
                        self.missing_entries[field_name][value] = MissingMetaobjectEntry(
                            field_name=entry_data['field_name'],
                            value=entry_data['value'],
                            frequency=entry_data['frequency'],
                            first_seen=entry_data['first_seen'],
                            last_seen=entry_data['last_seen'],
                            context=entry_data.get('context', {})
                        )
        except Exception as e:
            self.logger.warning(f"Could not load existing log: {e}")
            self.missing_entries = {}
    
    def log_missing_entry(self, field_name: str, value: str, context: Dict[str, Any] = None):
        """Log a missing metaobject entry with context and frequency tracking"""
        
        if context is None:
            context = {}
        
        timestamp = datetime.now().isoformat()
        
        # Initialize field if not exists
        if field_name not in self.missing_entries:
            self.missing_entries[field_name] = {}
        
        # Update or create entry
        if value in self.missing_entries[field_name]:
            # Update existing entry
            entry = self.missing_entries[field_name][value]
            entry.frequency += 1
            entry.last_seen = timestamp
            entry.context.update(context)
        else:
            # Create new entry
            entry = MissingMetaobjectEntry(
                field_name=field_name,
                value=value,
                frequency=1,
                first_seen=timestamp,
                last_seen=timestamp,
                context=context
            )
            self.missing_entries[field_name][value] = entry
        
        # Add to session tracking
        self.session_missing.append({
            'field_name': field_name,
            'value': value,
            'timestamp': timestamp,
            'context': context
        })
        
        # Save to file
        self._save_log()
        
        # Log to console/file logger
        self.logger.warning(
            f"Missing metaobject: {field_name}='{value}' "
            f"(frequency: {entry.frequency}, context: {context})"
        )
    
    def _save_log(self):
        """Save current log state to file"""
        try:
            # Convert to serializable format
            serializable_data = {
                'last_updated': datetime.now().isoformat(),
                'total_missing_fields': len(self.missing_entries),
                'total_missing_values': sum(len(entries) for entries in self.missing_entries.values()),
                'entries': {}
            }
            
            for field_name, entries in self.missing_entries.items():
                serializable_data['entries'][field_name] = {}
                for value, entry in entries.items():
                    serializable_data['entries'][field_name][value] = entry.to_dict()
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Failed to save log: {e}")
    
    def get_missing_summary(self) -> Dict[str, Any]:
        """Get summary of all missing entries"""
        summary = {}
        
        for field_name, entries in self.missing_entries.items():
            field_summary = {
                'total_values': len(entries),
                'total_frequency': sum(entry.frequency for entry in entries.values()),
                'most_common': [],
                'recent_entries': []
            }
            
            # Get most common missing values (top 5)
            sorted_entries = sorted(
                entries.values(),
                key=lambda x: x.frequency,
                reverse=True
            )
            field_summary['most_common'] = [
                {'value': entry.value, 'frequency': entry.frequency}
                for entry in sorted_entries[:5]
            ]
            
            # Get recent entries (last 5)
            recent_entries = sorted(
                entries.values(),
                key=lambda x: x.last_seen,
                reverse=True
            )
            field_summary['recent_entries'] = [
                {'value': entry.value, 'last_seen': entry.last_seen, 'frequency': entry.frequency}
                for entry in recent_entries[:5]
            ]
            
            summary[field_name] = field_summary
        
        return summary
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistical information about missing entries"""
        total_fields = len(self.missing_entries)
        total_unique_values = sum(len(entries) for entries in self.missing_entries.values())
        total_frequency = sum(
            sum(entry.frequency for entry in entries.values())
            for entries in self.missing_entries.values()
        )
        
        return {
            'total_fields': total_fields,
            'total_unique_values': total_unique_values,
            'total_frequency': total_frequency,
            'log_file_path': str(self.log_file),
            'log_file_exists': self.log_file.exists(),
            'session_missing_count': len(self.session_missing)
        }
    
    def get_session_missing(self) -> List[Dict]:
        """Get missing entries for current session"""
        return self.session_missing.copy()
    
    def clear_session_missing(self):
        """Clear session-specific missing data"""
        self.session_missing.clear()
        self.logger.info("Cleared session missing data")


# Global instances for backward compatibility with legacy imports
missing_logger = MissingMetaobjectLogger()

def get_missing_entries_report() -> Dict[str, Any]:
    """Get comprehensive report of all missing entries (legacy compatibility function)"""
    return {
        'summary': missing_logger.get_missing_summary(),
        'statistics': missing_logger.get_statistics(),
        'session_missing': missing_logger.get_session_missing()
    }

def clear_session_data():
    """Clear session-specific missing data (legacy compatibility function)"""
    missing_logger.clear_session_missing()