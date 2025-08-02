# Streamlit UI Patterns

This document establishes standardized patterns for building consistent, user-friendly interfaces using Streamlit in the Shopify Bulk Importer application.

## Overview

**Purpose**: Standardized Streamlit UI patterns and components
**Scope**: All user interface implementations
**Maintainer**: Product Strategy Advisor

## Core UI Principles

### 1. User-Centric Design
Design interfaces that prioritize user workflow efficiency and error prevention.

### 2. Consistency
Maintain consistent patterns across all pages and components.

### 3. Progressive Disclosure
Show essential information first, provide details on demand.

### 4. Error Prevention
Design interfaces that prevent errors rather than just handling them.

### 5. Responsive Feedback
Provide immediate feedback for all user actions.

## Page Structure Patterns

### Standard Page Layout
```python
import streamlit as st
from typing import Optional

def render_page_header(title: str, description: Optional[str] = None):
    """Standard page header pattern."""
    st.title(title)
    if description:
        st.markdown(f"*{description}*")
    st.divider()

def render_page_footer():
    """Standard page footer pattern."""
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<div style='text-align: center; color: gray; font-size: 12px;'>"
            "MyByte International - Shopify Bulk Importer"
            "</div>", 
            unsafe_allow_html=True
        )

def create_standard_page(title: str, description: str = None):
    """Standard page wrapper with consistent layout."""
    render_page_header(title, description)
    
    # Page content goes here
    yield
    
    render_page_footer()

# Usage
def smartphone_entry_page():
    with create_standard_page("Smartphone Product Entry", "Add new smartphone products to Shopify"):
        # Page content here
        pass
```

### Navigation Pattern
```python
def render_sidebar_navigation():
    """Consistent sidebar navigation."""
    with st.sidebar:
        st.title("🛍️ Product Entry")
        
        # Main navigation
        page = st.selectbox(
            "Select Product Type",
            ["Smartphone", "Laptop", "Tablet", "Accessories"],
            key="product_type_nav"
        )
        
        st.divider()
        
        # Session info
        if "products_in_session" in st.session_state:
            product_count = len(st.session_state.products_in_session)
            st.metric("Products in Session", product_count, delta=None)
        
        # Quick actions
        st.subheader("Quick Actions")
        if st.button("📤 Export Session", use_container_width=True):
            export_session_products()
        
        if st.button("🗑️ Clear Session", use_container_width=True):
            clear_session_products()
        
        return page
```

## Form Patterns

### Standard Form Structure
```python
def create_product_form(product_type: str) -> Optional[Dict]:
    """Standard product form pattern."""
    
    with st.form(key=f"{product_type}_form", clear_on_submit=True):
        st.subheader(f"📱 {product_type} Details")
        
        # Required fields section
        st.markdown("**Required Information**")
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input(
                "Product Title*",
                placeholder="Enter product title",
                help="This will be displayed in your Shopify store"
            )
        
        with col2:
            price = st.number_input(
                "Price (JPY)*",
                min_value=0,
                step=100,
                help="Product price in Japanese Yen"
            )
        
        # Optional fields section (collapsed by default)
        with st.expander("📋 Additional Details", expanded=False):
            description = st.text_area(
                "Product Description",
                placeholder="Enter detailed product description",
                height=100
            )
        
        # Form submission
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button(
                "➕ Add Product",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            # Validation
            if not title or not price:
                st.error("Please fill in all required fields marked with *")
                return None
            
            # Return form data
            return {
                "title": title,
                "price": price,
                "description": description
            }
    
    return None
```

### Template Selection Pattern
```python
def create_template_selector(templates: Dict[str, Dict]) -> Optional[str]:
    """Template selection with preview pattern."""
    
    st.subheader("📋 Quick Templates")
    
    # Template selection
    template_names = ["None (Manual Entry)"] + list(templates.keys())
    selected_template = st.selectbox(
        "Choose a template to auto-fill form",
        template_names,
        key="template_selector"
    )
    
    if selected_template != "None (Manual Entry)":
        template_data = templates[selected_template]
        
        # Template preview
        with st.expander("👀 Template Preview", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Product Info:**")
                st.write(f"• Brand: {template_data.get('brand', 'N/A')}")
                st.write(f"• Model: {template_data.get('model', 'N/A')}")
                st.write(f"• Storage: {template_data.get('storage', 'N/A')}")
            
            with col2:
                st.markdown("**Specifications:**")
                st.write(f"• RAM: {template_data.get('ram', 'N/A')}")
                st.write(f"• Color: {template_data.get('color', 'N/A')}")
        
        if st.button("✨ Apply Template", use_container_width=True):
            # Apply template to form fields
            for key, value in template_data.items():
                st.session_state[f"form_{key}"] = value
            st.success("Template applied! Form fields have been auto-filled.")
            st.rerun()
    
    return selected_template if selected_template != "None (Manual Entry)" else None
```

### Multi-Select Pattern
```python
def create_multi_select_field(
    label: str,
    options: List[str],
    key: str,
    default: List[str] = None,
    help_text: str = None
) -> List[str]:
    """Standardized multi-select field with chips display."""
    
    selected = st.multiselect(
        label,
        options,
        default=default or [],
        key=key,
        help=help_text
    )
    
    # Display selected items as chips
    if selected:
        chips_html = ""
        for item in selected:
            chips_html += f"""
            <span style="
                background-color: #e1f5fe;
                color: #01579b;
                padding: 2px 8px;
                margin: 2px;
                border-radius: 12px;
                font-size: 12px;
                display: inline-block;
            ">{item}</span>
            """
        
        st.markdown(
            f"<div style='margin-top: 5px;'>Selected: {chips_html}</div>",
            unsafe_allow_html=True
        )
    
    return selected
```

## Data Display Patterns

### Product Session Display
```python
def display_session_products():
    """Display products in current session with actions."""
    
    if "products_in_session" not in st.session_state:
        st.session_state.products_in_session = []
    
    products = st.session_state.products_in_session
    
    if not products:
        st.info("📝 No products in current session. Add products using the form above.")
        return
    
    st.subheader(f"📦 Session Products ({len(products)})")
    
    for i, product in enumerate(products):
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{product['title']}**")
                st.caption(f"Price: ¥{product['price']:,}")
            
            with col2:
                st.markdown(f"Brand: {product.get('brand', 'N/A')}")
                st.caption(f"Model: {product.get('model', 'N/A')}")
            
            with col3:
                if st.button("✏️", key=f"edit_{i}", help="Edit product"):
                    edit_product_in_session(i)
            
            with col4:
                if st.button("🗑️", key=f"delete_{i}", help="Remove product"):
                    remove_product_from_session(i)
                    st.rerun()
        
        st.divider()
```

### Status Display Pattern
```python
def display_operation_status(status: str, message: str, details: Optional[Dict] = None):
    """Standardized status display pattern."""
    
    status_config = {
        "success": {"icon": "✅", "color": "green", "container": st.success},
        "warning": {"icon": "⚠️", "color": "orange", "container": st.warning},
        "error": {"icon": "❌", "color": "red", "container": st.error},
        "info": {"icon": "ℹ️", "color": "blue", "container": st.info}
    }
    
    config = status_config.get(status, status_config["info"])
    
    # Main status message
    config["container"](f"{config['icon']} {message}")
    
    # Additional details if provided
    if details:
        with st.expander("📋 Details", expanded=False):
            for key, value in details.items():
                st.write(f"**{key}:** {value}")
```

### Progress Indicator Pattern
```python
def show_progress_indicator(current: int, total: int, operation: str):
    """Standardized progress indicator."""
    
    progress_percentage = current / total if total > 0 else 0
    
    # Progress bar
    progress_bar = st.progress(progress_percentage)
    
    # Progress text
    st.caption(f"{operation}: {current}/{total} ({progress_percentage:.0%})")
    
    return progress_bar
```

## Input Validation Patterns

### Real-time Validation
```python
def validate_product_title(title: str) -> tuple[bool, str]:
    """Validate product title with real-time feedback."""
    
    if not title:
        return False, "Title is required"
    
    if len(title) < 3:
        return False, "Title must be at least 3 characters"
    
    if len(title) > 100:
        return False, "Title must be less than 100 characters"
    
    # Check for special characters
    import re
    if not re.match(r'^[a-zA-Z0-9\s\-\[\]()]+$', title):
        return False, "Title contains invalid characters"
    
    return True, "Valid title"

def create_validated_text_input(
    label: str,
    key: str,
    validator: callable,
    placeholder: str = "",
    help_text: str = None
):
    """Text input with real-time validation."""
    
    value = st.text_input(
        label,
        placeholder=placeholder,
        key=key,
        help=help_text
    )
    
    if value:
        is_valid, message = validator(value)
        if is_valid:
            st.success(message)
        else:
            st.error(message)
        
        return value, is_valid
    
    return value, True  # Empty is initially valid
```

### Form Validation Summary
```python
def display_validation_summary(validation_results: Dict[str, tuple[bool, str]]):
    """Display form validation summary."""
    
    valid_fields = []
    invalid_fields = []
    
    for field, (is_valid, message) in validation_results.items():
        if is_valid:
            valid_fields.append(field)
        else:
            invalid_fields.append((field, message))
    
    if invalid_fields:
        st.error("Please fix the following issues:")
        for field, message in invalid_fields:
            st.write(f"• **{field}**: {message}")
        return False
    else:
        st.success(f"All {len(valid_fields)} fields are valid!")
        return True
```

## Modal and Dialog Patterns

### Confirmation Dialog
```python
def show_confirmation_dialog(
    title: str,
    message: str,
    confirm_text: str = "Confirm",
    cancel_text: str = "Cancel"
) -> Optional[bool]:
    """Standardized confirmation dialog."""
    
    if f"show_dialog_{title}" not in st.session_state:
        st.session_state[f"show_dialog_{title}"] = False
    
    if st.session_state[f"show_dialog_{title}"]:
        with st.container():
            st.warning(f"**{title}**")
            st.write(message)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button(cancel_text, key=f"cancel_{title}"):
                    st.session_state[f"show_dialog_{title}"] = False
                    st.rerun()
            
            with col3:
                if st.button(confirm_text, key=f"confirm_{title}", type="primary"):
                    st.session_state[f"show_dialog_{title}"] = False
                    return True
        
        return None  # Dialog is showing, no decision yet
    
    return False  # Dialog not showing

# Usage
def delete_all_products():
    if st.button("🗑️ Clear All Products"):
        st.session_state["show_dialog_clear_products"] = True
        st.rerun()
    
    result = show_confirmation_dialog(
        "Clear All Products",
        "Are you sure you want to remove all products from the session? This action cannot be undone.",
        "Clear All",
        "Keep Products"
    )
    
    if result:
        st.session_state.products_in_session = []
        st.success("All products cleared from session.")
        st.rerun()
```

## Error Handling Patterns

### User-Friendly Error Display
```python
def display_user_error(error: Exception, context: str = ""):
    """Display user-friendly error messages."""
    
    error_type = type(error).__name__
    error_message = str(error)
    
    # Map technical errors to user-friendly messages
    user_messages = {
        "ValidationError": "Please check your input data for errors",
        "ShopifyAPIError": "There was a problem connecting to Shopify",
        "RateLimitError": "Please wait a moment before trying again",
        "AuthenticationError": "Please check your Shopify credentials",
        "NetworkError": "Please check your internet connection"
    }
    
    user_message = user_messages.get(error_type, "An unexpected error occurred")
    
    st.error(f"**{user_message}**")
    
    with st.expander("🔧 Technical Details", expanded=False):
        st.code(f"Error Type: {error_type}")
        st.code(f"Message: {error_message}")
        if context:
            st.code(f"Context: {context}")
        
        st.caption("Please share these details with support if the problem persists.")
```

### Loading States
```python
import time
from contextlib import contextmanager

@contextmanager
def show_loading(message: str = "Processing..."):
    """Context manager for loading states."""
    
    placeholder = st.empty()
    
    with placeholder.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info(f"⏳ {message}")
    
    try:
        yield placeholder
    finally:
        placeholder.empty()

# Usage
def create_product_with_loading(product_data):
    with show_loading("Creating product in Shopify..."):
        time.sleep(1)  # Simulate API call
        result = create_product(product_data)
    
    st.success("Product created successfully!")
    return result
```

## Mobile Responsiveness Patterns

### Mobile-Friendly Layouts
```python
def create_responsive_columns(*ratios):
    """Create responsive columns that stack on mobile."""
    
    # Use single column layout on mobile
    if st.session_state.get("mobile_view", False):
        return [st.container() for _ in ratios]
    else:
        return st.columns(ratios)

def detect_mobile():
    """Detect mobile viewport (simplified)."""
    # In a real implementation, you might use JavaScript injection
    # For now, provide a toggle for testing
    mobile_toggle = st.sidebar.checkbox("📱 Mobile View", key="mobile_view")
    return mobile_toggle
```

### Touch-Friendly Controls
```python
def create_touch_friendly_button(
    label: str,
    key: str,
    button_type: str = "secondary",
    full_width: bool = True
) -> bool:
    """Create touch-friendly buttons with adequate spacing."""
    
    # Add spacing for touch targets
    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
    
    return st.button(
        label,
        key=key,
        type=button_type,
        use_container_width=full_width
    )
```

## Accessibility Patterns

### Screen Reader Support
```python
def create_accessible_form_field(
    field_type: str,
    label: str,
    key: str,
    required: bool = False,
    help_text: str = None,
    **kwargs
):
    """Create form fields with proper accessibility attributes."""
    
    # Add required indicator
    if required:
        label += " *"
    
    # Add help text for screen readers
    if help_text:
        full_help = f"{help_text}. {'' if not required else 'This field is required.'}"
    else:
        full_help = "This field is required." if required else None
    
    field_functions = {
        "text": st.text_input,
        "number": st.number_input,
        "select": st.selectbox,
        "multiselect": st.multiselect,
        "textarea": st.text_area
    }
    
    field_function = field_functions.get(field_type, st.text_input)
    
    return field_function(
        label,
        key=key,
        help=full_help,
        **kwargs
    )
```

## Common UI Anti-patterns to Avoid

### ❌ Inconsistent Layouts
```python
# Don't mix different column layouts randomly
col1, col2 = st.columns(2)  # Page 1
col1, col2, col3 = st.columns(3)  # Page 2 - inconsistent
```

### ❌ Poor Error Messages
```python
# Don't show technical errors to users
st.error("ValidationError: field 'title' required")  # Too technical
```

### ❌ No Loading States
```python
# Don't leave users wondering if something is happening
result = slow_api_call()  # No feedback during wait
```

### ❌ Inconsistent Button Styles
```python
# Don't mix button types randomly
st.button("Save", type="primary")  # Page 1
st.button("Save")  # Page 2 - inconsistent styling
```

### ❌ Poor Form Organization
```python
# Don't mix required and optional fields randomly
title = st.text_input("Title")  # Required
description = st.text_area("Description")  # Optional
price = st.number_input("Price")  # Required - poor grouping
```

---

**Pattern Version**: 1.0.0
**Last Updated**: 2025-08-02
**Next Review**: 2025-09-02
**Maintainer**: Product Strategy Advisor