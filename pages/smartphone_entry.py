import streamlit as st
from models.smartphone import SmartphoneProduct
from config.master_data import (
    SIM_CARRIERS, PRODUCT_RANKS, PRODUCT_INCLUSIONS, 
    MINUS_OPTIONS, RAM_OPTIONS, COMMON_BRANDS,
    get_title_suggestions, extract_info_from_template
)
from utils.handle_generator import preview_handle, generate_handle
from services.export_service import export_to_csv
from services.product_service import product_service
from pydantic import ValidationError

def smartphone_entry_page():
    """Main smartphone entry page"""
    st.header("📱 Smartphone Entry")
    
    # Initialize session state
    if "products" not in st.session_state:
        st.session_state.products = []
    
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}
    
    # Check session limit
    if len(st.session_state.products) >= 10:
        st.error("⚠️ Session limit reached (10 products). Please export current products before adding more.")
        return
    
    # Form container
    with st.form("smartphone_form", clear_on_submit=False):
        st.subheader("Product Information")
        
        # Title section with templates
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Title input with suggestions  
            title_input = st.text_input(
                "Product Title *",
                value=st.session_state.form_data.get("title", ""),
                placeholder="Start typing (e.g., iPhone 15 Pro) or select from suggestions below",
                key="title_input"
            )
        
        with col2:
            use_template = st.checkbox("Use Template", value=False)
        
        # Template selection callback
        def on_template_change():
            selected = st.session_state.template_select
            if selected != "Custom title":
                # Auto-fill form data from template
                extracted_info = extract_info_from_template(selected)
                st.session_state.form_data.update(extracted_info)
                st.session_state.form_data['title'] = selected
        
        # Title suggestions
        if title_input and len(title_input) > 2:
            suggestions = get_title_suggestions(title_input)
            if suggestions:
                st.write("**Suggestions:**")
                selected_template = st.selectbox(
                    "Select a template or continue with custom title",
                    ["Custom title"] + suggestions,
                    key="template_select",
                    on_change=on_template_change
                )
                
                # Apply template immediately if selected
                if selected_template != "Custom title" and selected_template != st.session_state.form_data.get('title', ''):
                    title_input = selected_template
                    # Auto-fill form data from template
                    extracted_info = extract_info_from_template(selected_template)
                    st.session_state.form_data.update(extracted_info)
                    st.session_state.form_data['title'] = selected_template
        
        # Two-column layout for main form
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Basic Information**")
            
            brand = st.selectbox(
                "Brand *",
                options=[""] + COMMON_BRANDS,
                index=0 if not st.session_state.form_data.get("brand") else 
                      COMMON_BRANDS.index(st.session_state.form_data.get("brand")) + 1
                      if st.session_state.form_data.get("brand") in COMMON_BRANDS else 0,
                key="brand_select"
            )
            
            model = st.text_input(
                "Model *",
                value=st.session_state.form_data.get("model", ""),
                placeholder="e.g., 15 Pro",
                key="model_input"
            )
            
            storage = st.text_input(
                "Storage",
                value=st.session_state.form_data.get("storage", ""),
                placeholder="e.g., 128GB",
                key="storage_input"
            )
            
            price = st.number_input(
                "Price (JPY) *",
                min_value=0.0,
                value=st.session_state.form_data.get("price", 0.0),
                step=100.0,
                format="%.0f"
            )
            
            color = st.text_input(
                "Color",
                value=st.session_state.form_data.get("color", ""),
                placeholder="e.g., Space Gray",
                key="color_input"
            )
        
        with col2:
            st.write("**Product Details**")
            
            sim_carrier_variants = st.multiselect(
                "Available SIM Carrier Variants *",
                options=SIM_CARRIERS,
                help="Select which SIM carrier variants are available for this specific device"
            )
            
            product_rank = st.selectbox(
                "Product Rank",
                options=[""] + PRODUCT_RANKS,
                index=0
            )
            
            ram_size = st.selectbox(
                "RAM Size",
                options=[""] + RAM_OPTIONS,
                index=0
            )
            
            # Multi-select fields
            st.write("**Inclusions** (multi-select)")
            # Use pre-selected inclusions from template if available
            default_inclusions = st.session_state.form_data.get('product_inclusions', [])
            inclusions = st.multiselect(
                "What's included?",
                options=PRODUCT_INCLUSIONS,
                default=default_inclusions
            )
            
            st.write("**Issues/Minus** (multi-select)")
            minus = st.multiselect(
                "Any issues?",
                options=MINUS_OPTIONS,
                default=[]
            )
        
        # Handle preview
        if title_input:
            handle_preview = preview_handle(title_input)
            st.info(f"**Generated Handle:** `{handle_preview}`")
        
        # Form submission
        submitted = st.form_submit_button("Add Product to Session", type="primary")
        
        if submitted:
            # Validate required fields
            errors = []
            warnings = []
            
            if not title_input or title_input.strip() == "":
                errors.append("Title is required")
            
            if not brand:
                errors.append("Brand is required")
            
            if not model or model.strip() == "":
                errors.append("Model is required")
            
            if price <= 0:
                errors.append("Price must be greater than 0")
            
            # SIM Carrier variants validation (required)
            if not sim_carrier_variants:
                errors.append("At least one SIM Carrier Variant must be selected")
            
            # Show errors and warnings
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
                return
            
            if warnings:
                for warning in warnings:
                    st.warning(f"⚠️ {warning}")
            
            # Create product
            try:
                product_data = {
                    "title": title_input.strip(),
                    "brand": brand,
                    "model": model.strip(),
                    "storage": storage.strip() if storage else None,
                    "price": price,
                    "color": color.strip() if color else None,
                    "sim_carrier_variants": sim_carrier_variants,
                    "product_rank": product_rank if product_rank else None,
                    "ram_size": ram_size if ram_size else None,
                    "product_inclusions": inclusions if inclusions else None,
                    "minus": minus if minus else None,
                    # Collections and sales channels from template or defaults
                    "collections": st.session_state.form_data.get('collections', ['All Products', 'iPhone'] if brand == 'iPhone' else ['All Products']),
                    "sales_channels": st.session_state.form_data.get('sales_channels', ["online_store", "pos", "shop"]),
                }
                
                # Generate handle
                handle = generate_handle(title_input.strip())
                product_data["handle"] = handle
                
                # Create product instance
                product = SmartphoneProduct(**product_data)
                
                # Add to session
                st.session_state.products.append(product)
                
                # Clear form data
                st.session_state.form_data = {}
                
                st.success(f"✅ Product added! Handle: `{handle}`")
                st.rerun()
                
            except ValidationError as e:
                st.error(f"❌ Validation error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Show current products in session
    if st.session_state.products:
        st.divider()
        st.subheader("Products in Current Session")
        
        for i, product in enumerate(st.session_state.products):
            with st.expander(f"{i+1}. {product.title} - ¥{product.price:,.0f}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Brand:** {product.brand}")
                    st.write(f"**Model:** {product.model}")
                    st.write(f"**Storage:** {product.storage or 'N/A'}")
                    st.write(f"**Price:** ¥{product.price:,.0f}")
                    st.write(f"**Handle:** `{product.handle}`")
                
                with col2:
                    st.write(f"**SIM Carrier Variants:** {', '.join(product.sim_carrier_variants) if product.sim_carrier_variants else 'N/A'}")
                    st.write(f"**Rank:** {product.product_rank or 'N/A'}")
                    st.write(f"**RAM:** {product.ram_size or 'N/A'}")
                    st.write(f"**Inclusions:** {', '.join(product.product_inclusions) if product.product_inclusions else 'N/A'}")
                    st.write(f"**Issues:** {', '.join(product.minus) if product.minus else 'None'}")
                
                if st.button(f"Remove", key=f"remove_{i}"):
                    st.session_state.products.pop(i)
                    st.rerun()
        
        # Export and Upload buttons
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔄 Clear All Products", type="secondary"):
                st.session_state.products = []
                st.rerun()
        
        with col2:
            if st.button("📥 Export to CSV", type="primary"):
                try:
                    csv_data = export_to_csv(st.session_state.products)
                    
                    # Generate filename
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
                    filename = f"mybyte-smartphones-{timestamp}.csv"
                    
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=filename,
                        mime="text/csv",
                        type="primary"
                    )
                    
                    st.success(f"✅ CSV ready for download! ({len(st.session_state.products)} products)")
                    
                except Exception as e:
                    st.error(f"❌ Export error: {str(e)}")
        
        with col3:
            if st.button("🚀 Upload to Shopify", type="primary"):
                try:
                    # Show upload progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Upload products
                    status_text.text("Uploading products to Shopify...")
                    
                    result = product_service.upload_multiple_products(st.session_state.products)
                    
                    progress_bar.progress(100)
                    
                    # Show results
                    if result['successful'] > 0:
                        st.success(f"✅ Successfully uploaded {result['successful']} of {result['total']} products!")
                        
                        # Show successful products
                        with st.expander("View uploaded products"):
                            for product_result in result['products']:
                                if product_result['result']['success']:
                                    product = product_result['smartphone']
                                    product_id = product_result['result']['product_id']
                                    st.write(f"✅ {product.title} - [View in Shopify](https://jufbtk-ut.myshopify.com/admin/products/{product_id})")
                        
                        # Clear session after successful upload
                        if result['failed'] == 0:
                            st.session_state.products = []
                            st.rerun()
                    
                    if result['failed'] > 0:
                        st.error(f"❌ Failed to upload {result['failed']} products")
                        
                        # Show failed products
                        with st.expander("View failed products"):
                            for product_result in result['products']:
                                if not product_result['result']['success']:
                                    product = product_result['smartphone']
                                    error = product_result['result']['error']
                                    st.write(f"❌ {product.title}: {error}")
                    
                except Exception as e:
                    st.error(f"❌ Upload error: {str(e)}")
    
    else:
        st.info("No products in current session. Add products using the form above.")