import streamlit as st
from models.laptop import LaptopProduct
from config.master_data import (
    PRODUCT_RANKS, MINUS_OPTIONS,
    get_laptop_template_suggestions, extract_info_from_template,
    get_collections_for_brand, detect_template_brand
)
from config.laptop_inclusions import LAPTOP_INCLUSION_LABELS
from config.laptop_metafields import LAPTOP_FIELD_ORDER
from utils.handle_generator import preview_handle, generate_handle
from services.export_service import export_to_csv
from services.product_service import product_service
from services.image_service import image_service
from pydantic import ValidationError

def clean_stale_image_references():
    """Clean up stale image references from session state"""
    if not hasattr(st.session_state, 'product_images'):
        return
    
    handles_to_clean = []
    for handle, images in st.session_state.product_images.items():
        valid_images = []
        for img in images:
            try:
                if hasattr(img, 'seek') and hasattr(img, 'read'):
                    img.seek(0)
                    test_read = img.read(1)
                    img.seek(0)  # Reset to beginning
                    if test_read:
                        valid_images.append(img)
            except:
                continue  # Skip invalid images
        
        if valid_images:
            st.session_state.product_images[handle] = valid_images
        else:
            handles_to_clean.append(handle)
    
    # Remove handles with no valid images
    for handle in handles_to_clean:
        del st.session_state.product_images[handle]

def laptop_entry_page():
    """Laptop entry page with laptop template selector"""
    st.header("💻 Laptop Entry")
    
    # Clean up any stale image references first
    clean_stale_image_references()
    
    # Initialize session state
    if "products" not in st.session_state:
        st.session_state.products = []
    
    if "product_images" not in st.session_state:
        st.session_state.product_images = {}
    
    # Check session limit
    if len(st.session_state.products) >= 10:
        st.error("Session limit reached (10 products). Please create products or clear session to continue.")
        return
    
    # Template Selection Section
    st.subheader("🔍 Select Laptop Template")
    
    # Search for laptop templates
    search_term = st.text_input(
        "Search laptops by brand, specs, or model:", 
        placeholder="e.g., 'asus i7 16gb', 'dell rtx 4060', 'hp gaming'",
        help="Search by any combination of brand, CPU, RAM, GPU, or model"
    )
    
    # Get template suggestions
    template_options = []
    if search_term:
        try:
            template_options = get_laptop_template_suggestions(search_term)
            if not template_options:
                st.warning(f"No laptops found matching '{search_term}'. Try different keywords.")
        except Exception as e:
            st.error(f"Error searching templates: {str(e)}")
            template_options = []
    else:
        try:
            template_options = get_laptop_template_suggestions()[:50]  # Show first 50 by default
        except Exception as e:
            st.error(f"Error loading templates: {str(e)}")
            template_options = []
    
    # Template selector
    selected_template = None
    if template_options:
        st.success(f"Found {len(template_options)} matching laptops")
        selected_template = st.selectbox(
            "Choose laptop configuration:",
            [""] + template_options,
            help="Select a laptop template to auto-fill specifications"
        )
    elif search_term:
        st.info("Enter a search term above to find laptop templates")
    else:
        st.info("Loading default templates...")
        # Show a few default options even when no search
        try:
            default_templates = get_laptop_template_suggestions()[:10]
            if default_templates:
                selected_template = st.selectbox(
                    "Choose laptop configuration (showing first 10):",
                    [""] + default_templates,
                    help="Select a laptop template to auto-fill specifications"
                )
        except Exception as e:
            st.error(f"Error loading default templates: {str(e)}")
    
    # Extract template information if selected
    template_info = {}
    if selected_template:
        template_info = extract_info_from_template(selected_template)
        if template_info:
            st.success(f"✓ Template selected: {template_info.get('title', 'Unknown')}")
            
            # Display template details
            with st.expander("📋 Template Details"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Specifications:**")
                    for key in ['cpu', 'ram', 'gpu', 'display', 'storage']:
                        if key in template_info:
                            st.write(f"• {key.upper()}: {template_info[key]}")
                
                with col2:
                    st.write("**Details:**")
                    for key in ['brand', 'color', 'vga', 'os']:
                        if key in template_info:
                            st.write(f"• {key.title()}: {template_info[key]}")
    
    st.divider()
    
    # Product Entry Form
    st.subheader("📝 Product Details")
    
    with st.form("laptop_entry_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Required fields
            st.markdown("**Required Fields**")
            
            title = st.text_input(
                "Product Title*",
                value=template_info.get('title', ''),
                help="Auto-generated from template or enter manually"
            )
            
            price = st.number_input(
                "Price (JPY)*", 
                min_value=0, 
                step=1000,
                help="Price in Japanese Yen"
            )
            
            rank = st.selectbox(
                "Product Rank*",
                PRODUCT_RANKS,
                help="Condition ranking from A to BNIB"
            )
            
            # Template-filled specifications
            st.markdown("**Specifications** (Auto-filled from template)")
            
            cpu = st.text_input(
                "Processor",
                value=template_info.get('cpu', ''),
                help="CPU specification from template"
            )
            
            ram = st.text_input(
                "RAM",
                value=template_info.get('ram', ''),
                help="Memory specification from template"
            )
            
            gpu = st.text_input(
                "Graphics",
                value=template_info.get('gpu', ''),
                help="GPU specification from template"
            )
        
        with col2:
            # More specifications
            st.markdown("**Additional Specifications**")
            
            display = st.text_input(
                "Display",
                value=template_info.get('display', ''),
                help="Display specification from template"
            )
            
            storage = st.text_input(
                "Storage",
                value=template_info.get('storage', ''),
                help="Storage specification from template"
            )
            
            color = st.text_input(
                "Color",
                value=template_info.get('color', ''),
                help="Laptop color/finish"
            )
            
            # Optional fields
            st.markdown("**Optional Fields**")
            
            inclusions = st.multiselect(
                "Product Inclusions",
                LAPTOP_INCLUSION_LABELS,
                help="What's included with the laptop"
            )
            
            minus_issues = st.multiselect(
                "Issues/Defects",
                MINUS_OPTIONS,
                help="Any known issues or defects"
            )
            
            # Collections (auto-assigned but editable)
            default_collections = template_info.get('collections', ['All Products', 'Laptop'])
            collections = st.multiselect(
                "Collections",
                ['All Products', 'Laptop', 'Gaming', 'Business', 'ASUS', 'Dell', 'HP', 'Lenovo', 'MSI'],
                default=default_collections,
                help="Shopify collections for this product"
            )
        
        # Submit button
        submit_button = st.form_submit_button(
            "Add to Session", 
            type="primary",
            use_container_width=True
        )
        
        if submit_button:
            # Validate required fields
            if not title or not price or not rank:
                st.error("Please fill in all required fields (Title, Price, Rank)")
                st.stop()
            
            try:
                # Generate handle
                brand = template_info.get('brand', 'Laptop')
                model = template_info.get('model', title.split()[0] if title else 'Unknown')
                specs = f"{cpu}-{ram}".replace(' ', '') if cpu and ram else 'specs'
                handle = generate_handle(title)
                
                # Create laptop product
                laptop_data = {
                    'title': title,
                    'brand': brand,
                    'model': model,
                    'price': price,
                    'handle': handle,
                    'collections': collections,
                    'rank': rank,
                    'cpu': cpu,
                    'ram': ram,
                    'gpu': gpu,
                    'display': display,
                    'storage': storage,
                    'color': color,
                    'vga': template_info.get('vga', ''),
                    'os': template_info.get('os', 'Windows 11'),
                    'keyboard_layout': template_info.get('keyboard_layout', 'US'),
                    'keyboard_backlight': template_info.get('keyboard_backlight', 'Yes'),
                    'inclusions': inclusions,
                    'minus': minus_issues,
                    'metafield_mappings': template_info.get('metafield_mappings', {})
                }
                
                # Validate with Pydantic model
                laptop_product = LaptopProduct(**laptop_data)
                
                # Add to session
                st.session_state.products.append(laptop_product.model_dump())
                
                st.success(f"✅ Laptop added to session: {title}")
                st.rerun()
                
            except ValidationError as e:
                st.error(f"Validation error: {str(e)}")
            except Exception as e:
                st.error(f"Error creating laptop: {str(e)}")
    
    # Session Management
    if st.session_state.products:
        st.divider()
        st.subheader("📦 Current Session")
        
        # Display products in session
        for i, product in enumerate(st.session_state.products):
            with st.expander(f"Product {i+1}: {product.get('title', 'Unknown')}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Brand:** {product.get('brand', 'N/A')}")
                    st.write(f"**Price:** ¥{product.get('price', 0):,}")
                    st.write(f"**Rank:** {product.get('rank', 'N/A')}")
                    if product.get('cpu') and product.get('ram'):
                        st.write(f"**Specs:** {product.get('cpu')} / {product.get('ram')}")
                
                with col2:
                    st.write(f"**Handle:** {product.get('handle', 'N/A')}")
                    st.write(f"**Collections:** {len(product.get('collections', []))}")
                
                with col3:
                    if st.button(f"Remove", key=f"remove_{i}"):
                        st.session_state.products.pop(i)
                        st.rerun()
        
        # Session actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export to CSV", use_container_width=True):
                try:
                    csv_data = export_to_csv(st.session_state.products)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name="laptop_products.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Export failed: {str(e)}")
        
        with col2:
            if st.button("🛍️ Create in Shopify", use_container_width=True):
                try:
                    success_count = 0
                    error_count = 0
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, product in enumerate(st.session_state.products):
                        status_text.text(f"Creating product {i+1}/{len(st.session_state.products)}")
                        
                        try:
                            # Create laptop product using the service
                            result = product_service.create_laptop_product(LaptopProduct(**product))
                            
                            if result.get('success'):
                                success_count += 1
                            else:
                                raise Exception(result.get('error', 'Unknown error'))
                            
                        except Exception as e:
                            st.error(f"Failed to create {product.get('title', 'Unknown')}: {str(e)}")
                            error_count += 1
                        
                        progress_bar.progress((i + 1) / len(st.session_state.products))
                    
                    if success_count > 0:
                        st.success(f"✅ Created {success_count} products successfully!")
                    if error_count > 0:
                        st.warning(f"⚠️ {error_count} products failed to create")
                    
                    # Clear session after successful creation
                    if success_count > 0:
                        st.session_state.products = []
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Bulk creation failed: {str(e)}")
        
        with col3:
            if st.button("🗑️ Clear Session", use_container_width=True):
                st.session_state.products = []
                st.rerun()

if __name__ == "__main__":
    laptop_entry_page()