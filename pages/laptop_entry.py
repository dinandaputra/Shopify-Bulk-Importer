import streamlit as st
from models.laptop import LaptopProduct
from config.master_data import (
    PRODUCT_RANKS, MINUS_OPTIONS,
    get_laptop_template_suggestions, extract_info_from_template,
    get_collections_for_brand, detect_template_brand
)
from config.laptop_specs import get_abbreviated_component_name
from config.laptop_inclusions import LAPTOP_INCLUSION_LABELS
from config.laptop_metafields import LAPTOP_FIELD_ORDER
from config.laptop_metafield_mapping_enhanced import (
    convert_laptop_data_to_metafields_enhanced,
    missing_logger,
    get_missing_entries_report,
    clear_session_data
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

def laptop_entry_page():
    """Laptop entry page with laptop template selector and enhanced logging"""
    st.header("💻 Laptop Entry")
    
    # Sidebar: Missing Metaobjects Report
    with st.sidebar:
        st.subheader("📊 Missing Metaobjects Report")
        
        # Get current missing entries report
        report = get_missing_entries_report()
        stats = report.get('statistics', {})
        
        # Show summary statistics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Missing Fields", stats.get('total_fields', 0))
        with col2:
            st.metric("Missing Values", stats.get('total_unique_values', 0))
        
        st.metric("Total Frequency", stats.get('total_frequency', 0))
        
        # Show session missing entries
        session_missing = report.get('session_missing', [])
        if session_missing:
            st.write("**This Session:**")
            st.write(f"🔍 {len(session_missing)} missing entries detected")
            
            with st.expander("View Session Missing"):
                for entry in session_missing[-5:]:  # Show last 5
                    field = entry['field_name'].replace('_', ' ').title()
                    st.write(f"• **{field}**: {entry['value']}")
        
        # Show most frequent missing overall
        most_frequent = stats.get('most_frequent_overall', [])[:3]
        if most_frequent:
            st.write("**Most Frequent Missing:**")
            for entry in most_frequent:
                field = entry['field'].replace('_', ' ').title()
                st.write(f"• **{field}**: {entry['value']} ({entry['frequency']}x)")
        
        # Link to admin report
        if st.button("📋 View Full Report", use_container_width=True):
            st.info("Navigate to Admin → Missing Metaobjects Report for detailed analysis")
    
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
    
    # Template Selection Section - Unified Fuzzy Search Pattern
    st.subheader("🔍 Select Laptop Template")
    st.markdown("### 🔍 Product Information")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Unified searchable template selector - load all templates for fuzzy search
        try:
            all_laptop_templates = get_laptop_template_suggestions()
            
            # Template selection callback for immediate updates
            def on_laptop_template_change():
                selected = st.session_state.laptop_template_selector
                if selected and selected != "":
                    extracted_info = extract_info_from_template(selected)
                    if extracted_info:
                        # Update session state immediately like smartphone entry
                        if 'laptop_form_data' not in st.session_state:
                            st.session_state.laptop_form_data = {}
                        st.session_state.laptop_form_data.update(extracted_info)
                        st.session_state.current_laptop_template = selected
            
            selected_template = st.selectbox(
                "Search and select laptop template:",
                [""] + all_laptop_templates,
                format_func=lambda x: x if x else "Type to search laptop templates...",
                key="laptop_template_selector",
                help="Type part of laptop brand, model, or specs to filter (e.g., 'ASUS i7', 'Dell RTX 4060', 'HP Gaming')",
                on_change=on_laptop_template_change
            )
            
            # Show current template info if selected - similar to smartphone pattern
            if selected_template and selected_template != "":
                extracted_info = extract_info_from_template(selected_template)
                if extracted_info:
                    brand = extracted_info.get('brand', 'Laptop')
                    brand_emoji = "💻" if brand == "ASUS" else "🖥️" if brand == "Dell" else "⚡" if brand == "HP" else "💻"
                    
                    # Show success message with extracted info
                    st.success(f"✅ **{extracted_info.get('title', selected_template)}**")
                    
                    # Show quick preview of extracted specs
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        cpu_info = extracted_info.get('cpu', 'N/A')
                        if extracted_info.get('ram'):
                            cpu_info += f" / {extracted_info.get('ram')}"
                        st.caption(f"{brand_emoji} {cpu_info}")
                    with col_b:
                        gpu_info = extracted_info.get('gpu') or extracted_info.get('integrated_graphics', 'N/A')
                        st.caption(f"🎮 {gpu_info}")
                    with col_c:
                        storage_info = extracted_info.get('storage', 'N/A')
                        st.caption(f"💾 {storage_info}")
            
        except Exception as e:
            st.error(f"Error loading laptop templates: {str(e)}")
            # Fallback to empty template list
            selected_template = st.selectbox(
                "Search and select laptop template:",
                [""],
                help="Template loading failed - you can still create products manually"
            )
    
    with col2:
        st.markdown("##### Quick Tips")
        st.caption("💡 Type to search")
        st.caption("💻 All laptop brands")
        st.caption("⚡ Auto-fills all fields")
        st.caption("✏️ All fields editable")
    
    # Initialize laptop form data if not exists
    if 'laptop_form_data' not in st.session_state:
        st.session_state.laptop_form_data = {}
    
    # Extract template information from session state
    template_info = st.session_state.laptop_form_data
    
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
                help="Auto-generated from template or enter manually",
                key="laptop_title_input"
            )
            
            price = st.number_input(
                "Price (JPY)*", 
                min_value=0, 
                step=1000,
                help="Price in Japanese Yen",
                key="laptop_price_input"
            )
            
            rank = st.selectbox(
                "Product Rank*",
                [""] + PRODUCT_RANKS,
                help="Condition ranking from A to BNIB",
                key="laptop_rank_input"
            )
            
            # Template-filled specifications
            st.markdown("**Specifications** (Auto-filled from template)")
            
            cpu = st.text_input(
                "Processor",
                value=template_info.get('cpu_full', template_info.get('cpu', '')),
                help="CPU specification from template",
                key="laptop_cpu_input"
            )
            
            ram = st.text_input(
                "RAM",
                value=template_info.get('ram_full', template_info.get('ram', '')),
                help="Memory specification from template",
                key="laptop_ram_input"
            )
            
            gpu = st.text_input(
                "VGA",
                value=template_info.get('gpu_full', ''),
                help="Dedicated graphics card (VGA) specification",
                key="laptop_gpu_input"
            )
            
            # Integrated Graphics field (also connects to 03 Graphics metafield)
            integrated_gpu = st.text_input(
                "Integrated Graphics", 
                value=template_info.get('integrated_graphics', ''),
                help="Integrated graphics specification (auto-detected from CPU)",
                key="laptop_integrated_gpu_input"
            )
        
        with col2:
            # More specifications
            st.markdown("**Additional Specifications**")
            
            display = st.text_input(
                "Display",
                value=template_info.get('display_full', template_info.get('display', '')),
                help="Display specification from template",
                key="laptop_display_input"
            )
            
            storage = st.text_input(
                "Storage",
                value=template_info.get('storage_full', template_info.get('storage', '')),
                help="Storage specification from template",
                key="laptop_storage_input"
            )
            
            color = st.text_input(
                "Color",
                value=template_info.get('color', ''),
                help="Laptop color/finish",
                key="laptop_color_input"
            )
            
            # Optional fields
            st.markdown("**Optional Fields**")
            
            inclusions = st.multiselect(
                "Product Inclusions",
                LAPTOP_INCLUSION_LABELS,
                default=template_info.get('inclusions', []),
                help="What's included with the laptop",
                key="laptop_inclusions_input"
            )
            
            minus_issues = st.multiselect(
                "Issues/Defects",
                MINUS_OPTIONS,
                help="Any known issues or defects",
                key="laptop_minus_input"
            )
            
            # Collections (auto-assigned but editable)
            default_collections = template_info.get('collections', ['All Products', 'Laptop'])
            collections = st.multiselect(
                "Collections",
                ['All Products', 'Laptop', 'Gaming', 'Business', 'ASUS', 'Dell', 'HP', 'Lenovo', 'MSI'],
                default=default_collections,
                help="Shopify collections for this product",
                key="laptop_collections_input"
            )
        
        # Submit button
        submit_button = st.form_submit_button(
            "Add to Session", 
            type="primary",
            use_container_width=True
        )
        
        if submit_button:
            # Validate required fields
            if not title or title.strip() == "":
                st.error("❌ Product title is required")
                st.stop()
            
            if price <= 0:
                st.error("❌ Price must be greater than 0")
                st.stop()
                
            if not rank:
                st.error("❌ Product rank is required")
                st.stop()
            
            try:
                # Generate handle
                brand = template_info.get('brand', 'Laptop')
                model = template_info.get('model', title.split()[0] if title else 'Unknown')
                specs = f"{cpu}-{ram}".replace(' ', '') if cpu and ram else 'specs'
                handle = generate_handle(title)
                
                # Create laptop product data - use full detailed names for metafield processing
                laptop_data = {
                    'title': title,
                    'brand': brand,
                    'model': model,
                    'price': price,
                    'handle': handle,
                    'collections': collections,
                    'rank': rank,
                    'processor': cpu,  # Use full detailed name for metafield processing
                    'ram': ram,
                    'vga': gpu,   # VGA field for dedicated graphics cards
                    'graphics': integrated_gpu,  # Graphics field for integrated graphics
                    'display': display,
                    'storage': storage,
                    'color': color,
                    'operating_system': template_info.get('os', 'Windows 11'),
                    'keyboard_layout': template_info.get('keyboard_layout', 'US'),
                    'keyboard_backlight': template_info.get('keyboard_backlight', 'Yes'),
                    'inclusions': inclusions,
                    'minus': minus_issues,
                    'metafield_mappings': template_info.get('metafield_mappings', {})
                }
                
                # Check for missing metaobjects using enhanced logging
                metafields, missing_entries = convert_laptop_data_to_metafields_enhanced(laptop_data)
                
                # Show warnings for missing metaobject entries
                if missing_entries:
                    st.warning("⚠️ Some specifications don't have metaobject entries yet:")
                    
                    missing_details = []
                    for field_name, values in missing_entries.items():
                        field_display = field_name.replace('_', ' ').title()
                        missing_details.append(f"**{field_display}**: {', '.join(values)}")
                    
                    for detail in missing_details:
                        st.write(f"  • {detail}")
                    
                    with st.expander("📝 What this means"):
                        st.info("""
                        **Impact on your product:**
                        - These specifications will be saved as text until proper metaobject entries are created
                        - Product will be created successfully but may have limited filtering/search capabilities in Shopify
                        - Missing entries are automatically logged for the next batch update
                        
                        **Next steps:**
                        - You can proceed with product creation - it will work fine
                        - Missing entries will be included in the next batch metaobject update
                        - Check the admin panel for reports on frequently missing entries
                        """)
                    
                    # Allow user to proceed or cancel
                    proceed_anyway = st.checkbox(
                        "Proceed anyway (specifications will be saved as text)",
                        help="Product will be created successfully with text specifications"
                    )
                    
                    if not proceed_anyway:
                        st.info("Please check the checkbox above to proceed with product creation.")
                        st.stop()
                
                # Validate with Pydantic model (convert back to original field names for validation)
                validation_data = laptop_data.copy()
                validation_data['cpu'] = validation_data.pop('processor', '')
                validation_data['gpu'] = validation_data.pop('graphics', '')
                validation_data['os'] = validation_data.pop('operating_system', '')
                
                laptop_product = LaptopProduct(**validation_data)
                
                # Add to session with enhanced metafield info
                session_product = laptop_product.model_dump()
                session_product['missing_metafields'] = missing_entries
                session_product['available_metafields'] = len(metafields)
                
                st.session_state.products.append(session_product)
                
                # Show success message with metafield info
                success_msg = f"✅ Laptop added to session: {title}"
                if missing_entries:
                    missing_count = sum(len(values) for values in missing_entries.values())
                    success_msg += f" (⚠️ {missing_count} missing metafields logged)"
                
                st.success(success_msg)
                template_used = st.session_state.laptop_form_data.get("template", selected_template)
                if template_used:
                    st.success(f"🎯 Template: `{template_used}`")
                
                # Clear form data and reset all form fields like smartphone entry
                st.session_state.laptop_form_data = {}
                
                # Clear template-related session state
                if "current_laptop_template" in st.session_state:
                    del st.session_state.current_laptop_template
                if "laptop_template_selector" in st.session_state:
                    del st.session_state.laptop_template_selector
                
                # Clear all form field keys to reset them completely
                laptop_form_keys = [
                    "laptop_title_input", "laptop_price_input", "laptop_rank_input",
                    "laptop_cpu_input", "laptop_ram_input", "laptop_gpu_input", 
                    "laptop_integrated_gpu_input", "laptop_display_input", "laptop_storage_input",
                    "laptop_color_input", "laptop_inclusions_input", "laptop_minus_input", 
                    "laptop_collections_input"
                ]
                for key in laptop_form_keys:
                    if key in st.session_state:
                        del st.session_state[key]
                
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
            # Show missing metafield indicator in title
            missing_count = 0
            if 'missing_metafields' in product:
                missing_count = sum(len(values) for values in product['missing_metafields'].values())
            
            title_suffix = f" ⚠️ ({missing_count} missing)" if missing_count > 0 else ""
            
            with st.expander(f"Product {i+1}: {product.get('title', 'Unknown')}{title_suffix}"):
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
                    
                    # Show metafield status
                    available_count = product.get('available_metafields', 0)
                    st.write(f"**Metafields:** {available_count} available")
                    if missing_count > 0:
                        st.write(f"**Missing:** {missing_count} metafields")
                
                with col3:
                    if st.button(f"Remove", key=f"remove_{i}"):
                        st.session_state.products.pop(i)
                        st.rerun()
                
                # Show missing metafields details if any
                if missing_count > 0:
                    with st.expander("⚠️ Missing Metafields Details"):
                        for field_name, values in product['missing_metafields'].items():
                            field_display = field_name.replace('_', ' ').title()
                            st.write(f"**{field_display}:** {', '.join(values)}")
        
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
                            # Filter out extra fields that aren't part of LaptopProduct model
                            product_data = {k: v for k, v in product.items() 
                                          if k not in ['missing_metafields', 'available_metafields']}
                            
                            # Create laptop product using the service
                            result = product_service.create_laptop_product(LaptopProduct(**product_data))
                            
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
                        clear_session_data()  # Clear enhanced logging session data
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Bulk creation failed: {str(e)}")
        
        with col3:
            if st.button("🗑️ Clear Session", use_container_width=True):
                st.session_state.products = []
                st.rerun()

if __name__ == "__main__":
    laptop_entry_page()