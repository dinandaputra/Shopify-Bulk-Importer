import re
from datetime import datetime
from database.handle_counter import handle_counter

def generate_handle(title: str) -> str:
    """
    Generate a unique handle for a product
    Format: {brand}-{model}-{specs}-{YYMMDD}-{counter}
    Example: iphone-15-pro-128gb-250715-001
    """
    # Clean the title
    handle_base = title.lower()
    
    # Remove special characters and replace spaces with hyphens
    handle_base = re.sub(r'[^\w\s-]', '', handle_base)
    handle_base = re.sub(r'\s+', '-', handle_base)
    handle_base = re.sub(r'-+', '-', handle_base)
    handle_base = handle_base.strip('-')
    
    # Get today's date in YYMMDD format
    today = datetime.now().strftime("%y%m%d")
    
    # Get next counter for today
    counter = handle_counter.get_next_counter()
    
    # Format counter with zero padding
    counter_str = f"{counter:03d}"
    
    # Combine all parts
    handle = f"{handle_base}-{today}-{counter_str}"
    
    return handle

def preview_handle(title: str) -> str:
    """
    Preview what the handle would look like without incrementing counter
    """
    if not title:
        return ""
    
    # Clean the title
    handle_base = title.lower()
    
    # Remove special characters and replace spaces with hyphens
    handle_base = re.sub(r'[^\w\s-]', '', handle_base)
    handle_base = re.sub(r'\s+', '-', handle_base)
    handle_base = re.sub(r'-+', '-', handle_base)
    handle_base = handle_base.strip('-')
    
    # Get today's date in YYMMDD format
    today = datetime.now().strftime("%y%m%d")
    
    # Get next counter (without incrementing)
    next_counter = handle_counter.get_current_counter() + 1
    counter_str = f"{next_counter:03d}"
    
    # Combine all parts
    handle = f"{handle_base}-{today}-{counter_str}"
    
    return handle