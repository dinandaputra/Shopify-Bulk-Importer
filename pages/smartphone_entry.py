import streamlit as st
from models.smartphone import SmartphoneProduct
from config.master_data import (
    SIM_CARRIERS, PRODUCT_RANKS, PRODUCT_INCLUSIONS, 
    MINUS_OPTIONS, RAM_OPTIONS, COMMON_BRANDS,
    get_unified_template_suggestions, extract_info_from_template,
    get_collections_for_brand, detect_template_brand
)
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

def smartphone_entry_page():
    """Smartphone entry page with iPhone template selector"""
    st.header("📱 Smartphone Entry")
    
    # Clean up any stale image references first
    clean_stale_image_references()
    
    # Initialize session state
    if "products" not in st.session_state:
        st.session_state.products = []
    
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}
    
    # Check session limit
    if len(st.session_state.products) >= 10:
        st.error("⚠️ Session limit reached (10 products). Please export current products before adding more.")
        return
    
    # TOP SECTION: Unified Template Selector (outside form for immediate updates)
    st.subheader("📋 Product Information")
    st.markdown("### 🔍 Select Product Template")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Unified searchable template selector
        all_templates = get_unified_template_suggestions()
        
        # Template selection callback
        def on_template_change():
            selected = st.session_state.template_selector
            if selected and selected != "":
                extracted_info = extract_info_from_template(selected)
                if extracted_info:
                    # Update form data immediately
                    st.session_state.form_data.update(extracted_info)
                    st.session_state.current_template = selected
        
        selected_template = st.selectbox(
            "Search and select product template:",
            [""] + all_templates,
            format_func=lambda x: x if x else "Type to search templates...",
            key="template_selector",
            help="Type part of iPhone/Galaxy model to filter (e.g., 'iPhone 15 Pro', 'Galaxy S24')",
            on_change=on_template_change
        )
        
        # Show current template info if selected
        if selected_template and selected_template != "":
            extracted_info = extract_info_from_template(selected_template)
            if extracted_info:
                brand = detect_template_brand(selected_template)
                brand_emoji = "📱" if brand == "iPhone" else "🤖" if brand == "Samsung" else "📱"
                
                # Show success message with extracted info
                st.success(f"✅ **{extracted_info.get('title', selected_template)}**")
                
                # Show quick preview of extracted info
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    model_info = f"{extracted_info.get('model', 'N/A')} {extracted_info.get('storage', '')}"
                    if extracted_info.get('ram'):  # Show RAM for Galaxy products
                        model_info += f" ({extracted_info.get('ram')})"
                    st.caption(f"{brand_emoji} {model_info}")
                with col_b:
                    st.caption(f"🎨 {extracted_info.get('color', 'N/A')}")
                with col_c:
                    inclusion_preset = extracted_info.get('inclusion_preset', '')
                    if inclusion_preset:
                        st.caption(f"📦 {inclusion_preset}")
    
    with col2:
        st.markdown("##### Quick Tips")
        st.caption("💡 Type to search")
        st.caption("📱 iPhone & 🤖 Galaxy")
        st.caption("⚡ Auto-fills all fields")
        st.caption("✏️ All fields editable")
    
    st.divider()
    
    # Form container (starts with form fields only)
    with st.form("smartphone_form", clear_on_submit=True):
        
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
                format="%.0f",
                key="price_input"
            )
            
            # Product Rank - required  
            product_rank = st.selectbox(
                "Product Rank *",
                options=[""] + PRODUCT_RANKS,
                index=0 if not st.session_state.form_data.get("product_rank") else 
                      PRODUCT_RANKS.index(st.session_state.form_data.get("product_rank")) + 1
                      if st.session_state.form_data.get("product_rank") in PRODUCT_RANKS else 0,
                help="Device condition rating",
                key="product_rank_input"
            )
            
            # SIM Carrier variants - required
            sim_carrier_variants = st.multiselect(
                "Available SIM Carrier Variants *",
                options=SIM_CARRIERS,
                default=st.session_state.form_data.get('sim_carrier_variants', []),
                help="Select which SIM carrier variants are available",
                key="sim_carrier_variants_input"
            )
        
        with col2:
            # RAM Size - auto-filled for Galaxy, optional for iPhone
            ram_auto_filled = st.session_state.form_data.get("ram")
            ram_size = st.selectbox(
                "RAM Size" + (" (Auto-filled)" if ram_auto_filled else ""),
                options=[""] + RAM_OPTIONS,
                index=0 if not st.session_state.form_data.get("ram") else 
                      RAM_OPTIONS.index(st.session_state.form_data.get("ram")) + 1
                      if st.session_state.form_data.get("ram") in RAM_OPTIONS else 0,
                help="Auto-filled for Galaxy products from template",
                key="ram_size_input"
            )
            
            # Issues/Problems - optional
            minus = st.multiselect(
                "Issues/Problems",
                options=MINUS_OPTIONS,
                default=[],
                help="Any device issues or defects",
                key="minus_input"
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
                placeholder="Auto-generated from template",
                key="title_input"
            )
            
            # Brand - auto-filled but editable
            brand = st.selectbox(
                "Brand *",
                options=COMMON_BRANDS,
                index=COMMON_BRANDS.index(st.session_state.form_data.get("brand", "iPhone")) if st.session_state.form_data.get("brand") in COMMON_BRANDS else 0,
                key="brand_input"
            )
            
            # Color - auto-filled but editable
            color = st.text_input(
                "Color",
                value=st.session_state.form_data.get("color", ""),
                placeholder="Auto-extracted from template",
                key="color_input"
            )
        
        with col2:
            # Collections - auto-assigned but editable
            if brand:
                auto_collections = get_collections_for_brand(brand)
                st.session_state.form_data["collections"] = auto_collections
            
            collections_display = st.text_input(
                "Collections (Auto-assigned)",
                value=", ".join(st.session_state.form_data.get("collections", [])),
                help="Automatically assigned, editable if needed",
                key="collections_input"
            )
            
            # Inclusions - auto-filled from template but editable
            default_inclusions = st.session_state.form_data.get("product_inclusions", [])
            inclusions = st.multiselect(
                "Product Inclusions",
                options=PRODUCT_INCLUSIONS,
                default=default_inclusions,
                help="Auto-selected from template, modify as needed",
                key="inclusions_input"
            )
        
        # Handle preview
        if title_input:
            handle_preview = preview_handle(title_input)
            st.caption(f"🔗 Handle: `{handle_preview}`")
        
        st.divider()
        
        # Image upload section
        uploaded_files = image_service.render_image_upload_interface("form")
        
        # Image preview with delete functionality
        active_images = []
        if uploaded_files:
            active_images = image_service.render_image_preview(uploaded_files, "form")
        
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
                    "ram_size": ram_size if ram_size else st.session_state.form_data.get("ram"),  # Use form input or auto-filled
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
                
                # Store uploaded images for this product (if any)
                if active_images:
                    if "product_images" not in st.session_state:
                        st.session_state.product_images = {}
                    # Store images with product handle as key
                    st.session_state.product_images[handle] = active_images
                
                # Add to session
                st.session_state.products.append(product)
                
                # Show success message before clearing
                st.success(f"✅ Product added! Handle: `{handle}`")
                template_used = st.session_state.form_data.get("template", "")
                if template_used:
                    st.success(f"🎯 Template: `{template_used}`")
                
                # Clear form data and reset all form fields
                st.session_state.form_data = {}
                
                # Clear template-related session state
                if "current_template" in st.session_state:
                    del st.session_state.current_template
                if "template_selector" in st.session_state:
                    del st.session_state.template_selector
                
                # Clear all form field keys to reset them completely
                form_keys = [
                    "price_input", "product_rank_input", "sim_carrier_variants_input",
                    "ram_size_input", "minus_input", "title_input", "brand_input", 
                    "color_input", "collections_input", "inclusions_input", "image_upload_form"
                ]
                for key in form_keys:
                    if key in st.session_state:
                        del st.session_state[key]
                
                # Image-related session state will be automatically cleared by reset counter
                
                # Increment reset counter to force file uploader reset
                if "form_reset_counter" not in st.session_state:
                    st.session_state.form_reset_counter = 0
                st.session_state.form_reset_counter += 1
                
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
                    
                    # Show image count and preview (read-only in main session view)
                    if hasattr(st.session_state, 'product_images') and product.handle in st.session_state.product_images:
                        current_images = st.session_state.product_images[product.handle]
                        image_count = len(current_images)
                        st.write(f"**Images**: 📸 {image_count} image(s)")
                        
                        # Display images in a grid (read-only preview)
                        if image_count > 0:
                            st.markdown("**Product Images:**")
                            img_cols = st.columns(min(image_count, 3))
                            
                            for img_idx, img_file in enumerate(current_images):
                                with img_cols[img_idx % 3]:
                                    try:
                                        # Check if file is still valid before displaying
                                        if hasattr(img_file, 'seek') and hasattr(img_file, 'read'):
                                            img_file.seek(0)
                                            # Try to read a small portion to validate the file
                                            current_pos = img_file.tell()
                                            test_read = img_file.read(1)
                                            img_file.seek(current_pos)
                                            
                                            if test_read:  # File is readable
                                                st.image(img_file, caption=img_file.name, width=80)
                                            else:
                                                st.warning(f"⚠️ Image unavailable: {img_file.name}")
                                        else:
                                            st.warning(f"⚠️ Invalid image reference: {getattr(img_file, 'name', 'Unknown')}")
                                        
                                    except Exception as e:
                                        st.warning(f"⚠️ Cannot display: {getattr(img_file, 'name', 'Unknown')}")
                    else:
                        st.write(f"**Images**: No images")
                    
                    if product.template:
                        st.write(f"**Template**: {product.template}")
                
                # Inline editing form
                if st.session_state.get(f"editing_product_{i}", False):
                    st.divider()
                    st.markdown("**✏️ Edit Product**")
                    
                    # Image management section (OUTSIDE the form to allow buttons)
                    st.markdown("**📸 Product Images**")
                    
                    # Show current images if any
                    current_images = []
                    if hasattr(st.session_state, 'product_images') and product.handle in st.session_state.product_images:
                        current_images = st.session_state.product_images[product.handle]
                    
                    if current_images:
                        st.markdown("**Current Images:**")
                        
                        # Track which images to remove (only initialize once per editing session)
                        images_to_remove_key = f"images_to_remove_edit_{i}"
                        if images_to_remove_key not in st.session_state:
                            st.session_state[images_to_remove_key] = set()
                        
                        images_to_remove = st.session_state[images_to_remove_key]
                        images_to_keep = []
                        
                        # Create columns for images that are NOT marked for removal
                        active_images = [(idx, img) for idx, img in enumerate(current_images) if idx not in images_to_remove]
                        
                        if active_images:
                            img_cols = st.columns(min(len(active_images), 4))
                            
                            for display_idx, (original_idx, img_file) in enumerate(active_images):
                                with img_cols[display_idx % 4]:
                                    try:
                                        # Check if file is still valid before displaying
                                        if hasattr(img_file, 'seek') and hasattr(img_file, 'read'):
                                            img_file.seek(0)
                                            # Try to read a small portion to validate the file
                                            current_pos = img_file.tell()
                                            test_read = img_file.read(1)
                                            img_file.seek(current_pos)
                                            
                                            if test_read:  # File is readable
                                                st.image(img_file, caption=img_file.name, width=120)
                                                
                                                # X delete button (now outside form, so this works)
                                                if st.button(
                                                    "❌", 
                                                    key=f"delete_img_edit_{i}_{original_idx}",
                                                    help=f"Remove {img_file.name}",
                                                    use_container_width=False
                                                ):
                                                    # Mark image for removal
                                                    st.session_state[images_to_remove_key].add(original_idx)
                                                    st.rerun()
                                                
                                                # Add to keep list
                                                images_to_keep.append(img_file)
                                            else:
                                                st.warning(f"⚠️ Image unavailable: {img_file.name}")
                                                # Still show delete button for stale references
                                                if st.button(
                                                    "🗑️ Remove Stale", 
                                                    key=f"delete_stale_edit_{i}_{original_idx}",
                                                    help=f"Remove invalid reference: {img_file.name}",
                                                    use_container_width=False
                                                ):
                                                    st.session_state[images_to_remove_key].add(original_idx)
                                                    st.rerun()
                                        else:
                                            st.warning(f"⚠️ Invalid image reference: {getattr(img_file, 'name', 'Unknown')}")
                                            # Show delete button for invalid references
                                            if st.button(
                                                "🗑️ Remove Invalid", 
                                                key=f"delete_invalid_edit_{i}_{original_idx}",
                                                help=f"Remove invalid reference",
                                                use_container_width=False
                                            ):
                                                st.session_state[images_to_remove_key].add(original_idx)
                                                st.rerun()
                                        
                                    except Exception as e:
                                        st.warning(f"⚠️ Cannot display: {getattr(img_file, 'name', 'Unknown')}")
                                        # Show delete button for error cases
                                        if st.button(
                                            "🗑️ Remove Error", 
                                            key=f"delete_error_edit_{i}_{original_idx}",
                                            help=f"Remove problematic reference",
                                            use_container_width=False
                                        ):
                                            st.session_state[images_to_remove_key].add(original_idx)
                                            st.rerun()
                        
                        if not images_to_keep and current_images:
                            st.info("All current images marked for removal")
                        elif len(images_to_keep) < len(current_images):
                            removed_count = len(current_images) - len(images_to_keep)
                            st.warning(f"{removed_count} image(s) marked for removal")
                    else:
                        images_to_keep = []
                        st.info("No current images")
                    
                    # Upload new images section (also outside the form)
                    st.markdown("**Add New Images:**")
                    
                    # Use dynamic key for edit form to enable clearing
                    if f"edit_reset_counter_{i}" not in st.session_state:
                        st.session_state[f"edit_reset_counter_{i}"] = 0
                    
                    edit_key = f"edit_{i}_{st.session_state[f'edit_reset_counter_{i}']}"
                    new_uploaded_files = image_service.render_image_upload_interface(edit_key)
                    
                    # Preview new images
                    new_active_images = []
                    if new_uploaded_files:
                        new_active_images = image_service.render_image_preview(new_uploaded_files, edit_key)
                    
                    # Combine kept current images and new images
                    all_images = images_to_keep + new_active_images
                    
                    if all_images:
                        st.success(f"Total images for this product: {len(all_images)}")
                    
                    st.divider()
                    
                    # Now the actual form for other product data
                    with st.form(f"edit_form_{i}"):
                        edit_col1, edit_col2 = st.columns(2)
                        
                        with edit_col1:
                            # Editable title
                            new_title = st.text_input("Title", value=product.title, key=f"edit_title_{i}")
                            
                            # Editable price
                            new_price = st.number_input("Price (JPY)", value=float(product.price), min_value=0.0, step=100.0, key=f"edit_price_{i}")
                            
                            # Editable product rank
                            current_rank_index = PRODUCT_RANKS.index(product.product_rank) if product.product_rank in PRODUCT_RANKS else 0
                            new_product_rank = st.selectbox("Product Rank", PRODUCT_RANKS, index=current_rank_index, key=f"edit_rank_{i}")
                            
                            # Editable SIM carrier variants
                            new_sim_carriers = st.multiselect("SIM Carrier Variants", SIM_CARRIERS, default=product.sim_carrier_variants or [], key=f"edit_sim_{i}")
                        
                        with edit_col2:
                            # Editable color
                            new_color = st.text_input("Color", value=product.color or "", key=f"edit_color_{i}")
                            
                            # Editable RAM size
                            current_ram_index = RAM_OPTIONS.index(product.ram_size) if product.ram_size and product.ram_size in RAM_OPTIONS else 0
                            new_ram = st.selectbox("RAM Size", [""] + RAM_OPTIONS, index=0 if not product.ram_size else RAM_OPTIONS.index(product.ram_size) + 1, key=f"edit_ram_{i}")
                            
                            # Editable inclusions
                            new_inclusions = st.multiselect("Product Inclusions", PRODUCT_INCLUSIONS, default=product.product_inclusions or [], key=f"edit_inclusions_{i}")
                            
                            # Editable minus/issues
                            new_minus = st.multiselect("Issues/Problems", MINUS_OPTIONS, default=product.minus or [], key=f"edit_minus_{i}")
                        
                        # Edit form buttons
                        edit_col_btn1, edit_col_btn2 = st.columns(2)
                        with edit_col_btn1:
                            save_clicked = st.form_submit_button("💾 Save Changes", type="primary")
                        with edit_col_btn2:
                            cancel_clicked = st.form_submit_button("❌ Cancel", type="secondary")
                        
                        if save_clicked:
                            # Validation
                            if not new_title.strip():
                                st.error("Title cannot be empty")
                            elif new_price <= 0:
                                st.error("Price must be greater than 0")
                            elif not new_product_rank:
                                st.error("Product rank is required")
                            elif not new_sim_carriers:
                                st.error("At least one SIM carrier variant must be selected")
                            else:
                                # Update the product in session
                                updated_data = {
                                    "title": new_title.strip(),
                                    "brand": product.brand,  # Keep original brand
                                    "model": product.model,  # Keep original model
                                    "storage": product.storage,  # Keep original storage
                                    "price": new_price,
                                    "color": new_color.strip() if new_color else None,
                                    "sim_carrier_variants": new_sim_carriers,
                                    "product_rank": new_product_rank,
                                    "ram_size": new_ram if new_ram else None,
                                    "product_inclusions": new_inclusions if new_inclusions else None,
                                    "minus": new_minus if new_minus else None,
                                    "collections": product.collections,  # Keep original collections
                                    "sales_channels": product.sales_channels,  # Keep original sales channels
                                    "color_metafield_gid": product.color_metafield_gid,  # Keep original metafield
                                    "template": product.template,  # Keep original template
                                }
                                
                                # Generate new handle if title changed
                                if new_title.strip() != product.title:
                                    new_handle = generate_handle(new_title.strip())
                                    updated_data["handle"] = new_handle
                                    
                                    # Update images dictionary key if handle changed
                                    if hasattr(st.session_state, 'product_images') and product.handle in st.session_state.product_images:
                                        st.session_state.product_images[new_handle] = st.session_state.product_images.pop(product.handle)
                                else:
                                    updated_data["handle"] = product.handle
                                
                                try:
                                    # Create updated product instance
                                    updated_product = SmartphoneProduct(**updated_data)
                                    
                                    # Replace in session
                                    st.session_state.products[i] = updated_product
                                    
                                    # Update images in session
                                    if all_images:
                                        if "product_images" not in st.session_state:
                                            st.session_state.product_images = {}
                                        st.session_state.product_images[updated_data["handle"]] = all_images
                                    else:
                                        # Remove images if none selected
                                        if hasattr(st.session_state, 'product_images') and updated_data["handle"] in st.session_state.product_images:
                                            del st.session_state.product_images[updated_data["handle"]]
                                    
                                    # Clear editing state
                                    if f"editing_product_{i}" in st.session_state:
                                        del st.session_state[f"editing_product_{i}"]
                                    
                                    # Clear edit-specific image state
                                    keys_to_clear = [key for key in st.session_state.keys() if key.startswith(f"images_to_keep_edit_{i}_")]
                                    for key in keys_to_clear:
                                        del st.session_state[key]
                                    
                                    # Clear removal tracking state
                                    images_to_remove_key = f"images_to_remove_edit_{i}"
                                    if images_to_remove_key in st.session_state:
                                        del st.session_state[images_to_remove_key]
                                    
                                    # Increment edit reset counter to clear image upload interface
                                    if f"edit_reset_counter_{i}" in st.session_state:
                                        st.session_state[f"edit_reset_counter_{i}"] += 1
                                    
                                    st.success(f"✅ Product updated: {new_title}")
                                    if all_images:
                                        st.success(f"📸 Images updated: {len(all_images)} image(s)")
                                    
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Update error: {str(e)}")
                        
                        if cancel_clicked:
                            # Clear editing state
                            if f"editing_product_{i}" in st.session_state:
                                del st.session_state[f"editing_product_{i}"]
                            
                            # Clear edit-specific image state
                            keys_to_clear = [key for key in st.session_state.keys() if key.startswith(f"images_to_keep_edit_{i}_")]
                            for key in keys_to_clear:
                                del st.session_state[key]
                            
                            # Clear removal tracking state
                            images_to_remove_key = f"images_to_remove_edit_{i}"
                            if images_to_remove_key in st.session_state:
                                del st.session_state[images_to_remove_key]
                            
                            # Increment edit reset counter to clear image upload interface
                            if f"edit_reset_counter_{i}" in st.session_state:
                                st.session_state[f"edit_reset_counter_{i}"] += 1
                            
                            st.rerun()
                
                # Action buttons
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"📝 Edit", key=f"edit_{i}"):
                        st.session_state[f"editing_product_{i}"] = True
                        st.rerun()
                with col_btn2:
                    if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                        removed_product = st.session_state.products.pop(i)
                        # Remove associated images
                        if hasattr(st.session_state, 'product_images') and removed_product.handle in st.session_state.product_images:
                            del st.session_state.product_images[removed_product.handle]
                        
                        # Clean up any image-related session state for this product
                        keys_to_clean = [
                            f"images_to_remove_edit_{i}",
                            f"editing_product_{i}",
                            f"edit_reset_counter_{i}"
                        ]
                        for key in keys_to_clean:
                            if key in st.session_state:
                                del st.session_state[key]
                        
                        st.rerun()
        
        # Session actions
        st.divider()
        st.markdown("### 📤 Session Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Clear All Products", type="secondary", use_container_width=True):
                st.session_state.products = []
                # Clear product images as well
                if hasattr(st.session_state, 'product_images'):
                    st.session_state.product_images = {}
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
                    
                    # Pass product images if they exist
                    product_images = getattr(st.session_state, 'product_images', {})
                    result = product_service.upload_multiple_products(st.session_state.products, product_images)
                    
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
                            # Clear product images as well
                            if hasattr(st.session_state, 'product_images'):
                                st.session_state.product_images = {}
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