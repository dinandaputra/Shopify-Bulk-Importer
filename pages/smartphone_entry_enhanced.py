import streamlit as st
from models.smartphone import SmartphoneProduct
from config.master_data import (
    SIM_CARRIERS, PRODUCT_RANKS, PRODUCT_INCLUSIONS, 
    MINUS_OPTIONS, RAM_OPTIONS, COMMON_BRANDS,
    get_iphone_template_suggestions, extract_info_from_template,
    get_collections_for_brand
)
from utils.handle_generator import preview_handle, generate_handle
from services.export_service import export_to_csv
from services.product_service import product_service
from pydantic import ValidationError

def smartphone_entry_page():
    """Simplified smartphone entry page with single template selector"""
    st.header("📱 Smartphone Entry - Simplified")
    
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
        st.subheader("📋 Product Information")
        
        # TOP SECTION: Single Template Selector
        st.markdown("### 🔍 Select iPhone Template")
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # Single searchable template selector
            all_templates = get_iphone_template_suggestions()
            
            selected_template = st.selectbox(
                "Search and select iPhone template:",
                [""] + all_templates,
                format_func=lambda x: x if x else "Type to search templates...",
                key="template_selector",
                help="Type part of iPhone model to filter (e.g., 'iPhone 15 Pro')"
            )
            
            # Auto-fill when template is selected - use on_change callback approach
            if selected_template and selected_template != "":
                # Check if template changed
                if st.session_state.get('current_template') != selected_template:
                    extracted_info = extract_info_from_template(selected_template)
                    if extracted_info:
                        # Update form data immediately
                        st.session_state.form_data.update(extracted_info)
                        st.session_state.current_template = selected_template
                
                # Show current template info
                if selected_template == st.session_state.get('current_template', ''):
                    extracted_info = extract_info_from_template(selected_template)
                    if extracted_info:
                        # Show success message with extracted info
                        st.success(f"✅ **{extracted_info.get('title', selected_template)}**")
                        
                        # Show quick preview of extracted info
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.caption(f"📱 {extracted_info.get('model', 'N/A')} {extracted_info.get('storage', '')}")
                        with col_b:
                            st.caption(f"🎨 {extracted_info.get('color', 'N/A')}")
                        with col_c:
                            inclusion_preset = extracted_info.get('inclusion_preset', '')
                            if inclusion_preset:
                                st.caption(f"📦 {inclusion_preset}")
        
        with col2:
            st.markdown("##### Quick Tips")
            st.caption("💡 Type to search")
            st.caption("⚡ Auto-fills all fields")
            st.caption("✏️ All fields editable")
        
        st.divider()
        
        # MIDDLE SECTION: Essential User Input
        st.markdown("### ✏️ Essential Information (User Input)")
        col1, col2 = st.columns(2)
        
        with col1:
            # Price - required
            price = st.number_input(
                "Price (JPY) *",
                min_value=0.0,
                value=st.session_state.form_data.get("price", 0.0),
                step=100.0,
                format="%.0f"
            )
            
            # Product Rank - required  
            product_rank = st.selectbox(
                "Product Rank *",
                options=[""] + PRODUCT_RANKS,
                index=0,
                help="Device condition rating"
            )
            
            # SIM Carrier variants - required
            sim_carrier_variants = st.multiselect(
                "Available SIM Carrier Variants *",
                options=SIM_CARRIERS,
                help="Select which SIM carrier variants are available"
            )
        
        with col2:
            # RAM Size - optional
            ram_size = st.selectbox(
                "RAM Size",
                options=[""] + RAM_OPTIONS,
                index=0
            )
            
            # Issues/Problems - optional
            minus = st.multiselect(
                "Issues/Problems",
                options=MINUS_OPTIONS,
                default=[],
                help="Any device issues or defects"
            )
        
        st.divider()
        
        # BOTTOM SECTION: Auto-Populated Editable Fields
        st.markdown("### 📝 Auto-Populated Fields (Editable)")
        col1, col2 = st.columns(2)
        
        with col1:
            # Title - auto-filled but editable
            title_input = st.text_input(
                "Product Title *",
                value=st.session_state.form_data.get("title", ""),
                placeholder="Auto-generated from template"
            )
            
            # Brand - auto-filled but editable
            brand = st.selectbox(
                "Brand *",
                options=COMMON_BRANDS,
                index=COMMON_BRANDS.index(st.session_state.form_data.get("brand", "iPhone")) if st.session_state.form_data.get("brand") in COMMON_BRANDS else 0
            )
            
            # Color - auto-filled but editable
            color = st.text_input(
                "Color",
                value=st.session_state.form_data.get("color", ""),
                placeholder="Auto-extracted from template"
            )
        
        with col2:
            # Collections - auto-assigned but editable
            if brand:
                auto_collections = get_collections_for_brand(brand)
                st.session_state.form_data["collections"] = auto_collections
            
            collections_display = st.text_input(
                "Collections (Auto-assigned)",
                value=", ".join(st.session_state.form_data.get("collections", [])),
                help="Automatically assigned, editable if needed"
            )
            
            # Inclusions - auto-filled from template but editable
            default_inclusions = st.session_state.form_data.get("product_inclusions", [])
            inclusions = st.multiselect(
                "Product Inclusions",
                options=PRODUCT_INCLUSIONS,
                default=default_inclusions,
                help="Auto-selected from template, modify as needed"
            )
        
        # Handle preview
        if title_input:
            handle_preview = preview_handle(title_input)
            st.caption(f"🔗 Handle: `{handle_preview}`")
        
        st.divider()
        
        # Form submission
        submitted = st.form_submit_button("🚀 Add Product to Session", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            errors = []
            
            if not title_input or title_input.strip() == "":
                errors.append("Product title is required")
            
            if not brand:
                errors.append("Brand is required")
            
            if price <= 0:
                errors.append("Price must be greater than 0")
                
            if not product_rank:
                errors.append("Product rank is required")
                
            if not sim_carrier_variants:
                errors.append("At least one SIM carrier variant must be selected")
            
            # Show errors
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
                return
            
            # Create product
            try:
                # Parse collections from display field if edited
                if collections_display:
                    parsed_collections = [c.strip() for c in collections_display.split(",") if c.strip()]
                else:
                    parsed_collections = st.session_state.form_data.get("collections", ["All Products"])
                
                product_data = {
                    "title": title_input.strip(),
                    "brand": brand,
                    "model": st.session_state.form_data.get("model"),  # From template
                    "storage": st.session_state.form_data.get("storage"),  # From template  
                    "price": price,
                    "color": color.strip() if color else None,
                    "sim_carrier_variants": sim_carrier_variants,
                    "product_rank": product_rank,
                    "ram_size": ram_size if ram_size else None,
                    "product_inclusions": inclusions if inclusions else None,
                    "minus": minus if minus else None,
                    "collections": parsed_collections,
                    "sales_channels": ["online_store", "pos", "shop"],
                    "color_metafield_gid": st.session_state.form_data.get("color_metafield_gid"),
                    "template": st.session_state.form_data.get("template", "")
                }
                
                # Generate handle
                handle = generate_handle(title_input.strip())
                product_data["handle"] = handle
                
                # Create product instance
                product = SmartphoneProduct(**product_data)
                
                # Add to session
                st.session_state.products.append(product)
                
                # Show success message before clearing
                st.success(f"✅ Product added! Handle: `{handle}`")
                template_used = st.session_state.form_data.get("template", "")
                if template_used:
                    st.success(f"🎯 Template: `{template_used}`")
                
                # Clear form data
                st.session_state.form_data = {}
                if "current_template" in st.session_state:
                    del st.session_state.current_template
                    
                st.rerun()
                
            except ValidationError as e:
                st.error(f"❌ Validation error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Show current products in session (enhanced display)
    if st.session_state.products:
        st.divider()
        st.subheader("📦 Products in Current Session")
        
        for i, product in enumerate(st.session_state.products):
            with st.expander(f"{i+1}. {product.title} - ¥{product.price:,.0f}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Brand**: {product.brand}")
                    st.write(f"**Model**: {product.get_display_model_storage()}")
                    st.write(f"**Price**: ¥{product.price:,.0f}")
                    st.write(f"**Handle**: `{product.handle}`")
                
                with col2:
                    st.write(f"**Rank**: {product.product_rank or 'N/A'}")
                    st.write(f"**Color**: {product.color or 'N/A'}")
                    st.write(f"**RAM**: {product.ram_size or 'N/A'}")
                    st.write(f"**SIM Variants**: {', '.join(product.sim_carrier_variants) if product.sim_carrier_variants else 'N/A'}")
                
                with col3:
                    st.write(f"**Collections**: {', '.join(product.collections) if product.collections else 'N/A'}")
                    st.write(f"**Inclusions**: {', '.join(product.product_inclusions) if product.product_inclusions else 'None'}")
                    st.write(f"**Issues**: {', '.join(product.minus) if product.minus else 'None'}")
                    if product.template:
                        st.write(f"**Template**: {product.template}")
                
                # Action buttons
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"📝 Edit", key=f"edit_{i}"):
                        st.info("🚧 Inline editing coming in Phase 3!")
                with col_btn2:
                    if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                        st.session_state.products.pop(i)
                        st.rerun()
        
        # Session actions
        st.divider()
        st.markdown("### 📤 Session Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Clear All Products", type="secondary", use_container_width=True):
                st.session_state.products = []
                st.rerun()
        
        with col2:
            if st.button("📥 Export to CSV", type="primary", use_container_width=True):
                try:
                    csv_data = export_to_csv(st.session_state.products)
                    
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
                    filename = f"mybyte-smartphones-enhanced-{timestamp}.csv"
                    
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv_data,
                        file_name=filename,
                        mime="text/csv",
                        type="primary"
                    )
                    
                    st.success(f"✅ CSV ready for download! ({len(st.session_state.products)} products)")
                    
                except Exception as e:
                    st.error(f"❌ Export error: {str(e)}")
        
        with col3:
            if st.button("🚀 Upload to Shopify", type="primary", use_container_width=True):
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Uploading products to Shopify...")
                    
                    result = product_service.upload_multiple_products(st.session_state.products)
                    
                    progress_bar.progress(100)
                    
                    # Show results
                    if result['successful'] > 0:
                        st.success(f"✅ Successfully uploaded {result['successful']} of {result['total']} products!")
                        
                        with st.expander("📋 View uploaded products"):
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
                        
                        with st.expander("❌ View failed products"):
                            for product_result in result['products']:
                                if not product_result['result']['success']:
                                    product = product_result['smartphone']
                                    error = product_result['result']['error']
                                    st.write(f"❌ {product.title}: {error}")
                    
                except Exception as e:
                    st.error(f"❌ Upload error: {str(e)}")
    
    else:
        st.info("📝 No products in current session. Use the form above to add products with the enhanced template system!")