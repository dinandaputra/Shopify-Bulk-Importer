import streamlit as st
from models.laptop import LaptopProduct
from config.master_data import (
    PRODUCT_RANKS, MINUS_OPTIONS,
    get_collections_for_brand, detect_template_brand
)
from services.template_cache_service import TemplateCacheService
from services.component_dropdown_service import ComponentDropdownService
from services.template_display_service import TemplateDisplayService
from services.validation_service import (
    missing_logger,
    get_missing_entries_report,
    clear_session_data
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

@st.cache_resource
def get_template_service():
    """Initialize template cache service (cached for performance)"""
    return TemplateCacheService()

@st.cache_resource
def get_dropdown_service():
    """Initialize component dropdown service (cached for performance)"""
    return ComponentDropdownService()

def laptop_entry_page():
    """Laptop entry page with laptop template selector and enhanced logging"""
    st.header("💻 Laptop Entry")
    
    # Initialize services
    template_service = get_template_service()
    
    try:
        dropdown_service = get_dropdown_service()
    except Exception as e:
        st.error(f"Error initializing dropdown service: {str(e)}")
        st.error("Falling back to text inputs. Please check metaobject data files.")
        return
    
    # Auto-regenerate cache if needed (runs on app start)
    if template_service.needs_regeneration():
        with st.spinner("Updating laptop templates..."):
            template_service.regenerate_cache()
    
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
            # Load all templates using the new service
            all_laptop_templates = template_service.get_all_templates()
            
            if not all_laptop_templates:
                st.warning("No laptop templates available. Please check data configuration.")
                all_laptop_templates = []
            
            # Template selection callback with comprehensive error handling
            def on_laptop_template_change():
                selected = st.session_state.laptop_template_selector
                if selected and selected != "":
                    print(f"🔍 Template selected: {selected}")
                    
                    try:
                        extracted_info = template_service.parse_template(selected)
                        if extracted_info:
                            print(f"✅ Template parsed successfully: {len(extracted_info)} fields")
                            
                            # Initialize session state if needed
                            if 'laptop_form_data' not in st.session_state:
                                st.session_state.laptop_form_data = {}
                            
                            # Update session state with parsed data
                            st.session_state.laptop_form_data.update(extracted_info)
                            st.session_state.current_laptop_template = selected
                            
                            # Show success message
                            st.success(f"✅ Template loaded: {extracted_info.get('title', 'Laptop')}")
                        else:
                            print("❌ Template parsing failed")
                            st.error(f"Failed to parse template: {selected}")
                            st.error("Please try selecting a different template or contact support.")
                            
                    except Exception as e:
                        print(f"❌ Error in template parsing: {e}")
                        st.error(f"Error processing template: {str(e)}")
                        st.error("Please try refreshing the page or selecting a different template.")
            
            selected_template = st.selectbox(
                "Search and select laptop template:",
                [""] + all_laptop_templates,
                format_func=lambda x: x if x else "Type to search laptop templates...",
                key="laptop_template_selector",
                help="Type part of laptop brand, model, or specs to filter (e.g., 'ASUS i7', 'Dell RTX 4060', 'HP Gaming')",
                on_change=on_laptop_template_change
            )
            
            # Show current template info if selected with better error handling
            if selected_template and selected_template != "":
                try:
                    extracted_info = template_service.parse_template(selected_template)
                    if extracted_info:
                        brand = extracted_info.get('brand', 'Laptop')
                        brand_emoji = "💻" if brand == "ASUS" else "🖥️" if brand == "Dell" else "⚡" if brand == "HP" else "💻"
                        
                        # Show success message with extracted info
                        st.success(f"✅ **{extracted_info.get('title', selected_template)}**")
                        
                        # Show quick preview of extracted specs with null checks
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            cpu_info = extracted_info.get('cpu', 'N/A')
                            if extracted_info.get('ram'):
                                cpu_info += f" / {extracted_info.get('ram')}"
                            st.caption(f"{brand_emoji} {cpu_info[:30]}...'" if len(cpu_info) > 30 else f"{brand_emoji} {cpu_info}")
                        with col_b:
                            gpu_info = extracted_info.get('gpu') or extracted_info.get('vga', 'N/A')
                            st.caption(f"🎮 {gpu_info[:20]}...'" if len(gpu_info) > 20 else f"🎮 {gpu_info}")
                        with col_c:
                            storage_info = extracted_info.get('storage', 'N/A')
                            st.caption(f"💾 {storage_info}")
                    else:
                        st.warning("⚠️ Template selected but could not be parsed. Form fields may be empty.")
                except Exception as e:
                    st.error(f"Error displaying template info: {str(e)}")
            
        except Exception as e:
            st.error(f"Error loading laptop templates: {str(e)}")
            st.error("Falling back to manual entry mode.")
            
            # Fallback to empty template selector
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
    
    # Initialize form reset counter for image uploads
    if "form_reset_counter" not in st.session_state:
        st.session_state.form_reset_counter = 0
    
    with st.form("laptop_entry_form"):
        st.divider()
        
        # Image upload section (inside form like smartphone implementation)
        st.markdown("### 📸 Product Images")
        uploaded_files = image_service.render_image_upload_interface("form")
        
        # Image preview with delete functionality
        active_images = []
        if uploaded_files:
            active_images = image_service.render_image_preview(uploaded_files, "form")
        
        st.divider()
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
            
            # CPU/Processor searchable dropdown
            cpu_options = dropdown_service.get_processor_options()
            cpu_template_value = template_info.get('cpu_full', template_info.get('cpu', ''))
            cpu_index = dropdown_service.find_dropdown_index(cpu_options, cpu_template_value)

            cpu_selection = st.selectbox(
                "Processor",
                options=cpu_options,
                format_func=lambda x: x[1],  # Show display name
                index=cpu_index,
                help="Select processor or choose 'Other/Custom processor...' for manual entry",
                key="laptop_cpu_dropdown"
            )
            cpu = cpu_selection[0]  # Get the value

            # Handle custom input
            if cpu == "CUSTOM":
                cpu = st.text_input(
                    "Enter custom processor:", 
                    value=cpu_template_value,
                    help="Enter processor specification manually",
                    key="cpu_custom"
                )
            
            # RAM simple selectbox
            ram_options = dropdown_service.get_ram_options()
            ram_template_value = template_info.get('ram_full', template_info.get('ram', ''))
            ram_index = dropdown_service.find_simple_dropdown_index(ram_options, ram_template_value)

            ram = st.selectbox(
                "RAM",
                options=ram_options,
                index=ram_index,
                help="Select RAM size from common options",
                key="laptop_ram_dropdown"
            )
            
            # VGA/Dedicated Graphics searchable dropdown
            vga_options = dropdown_service.get_vga_options()
            vga_template_value = template_info.get('vga', '')
            vga_index = dropdown_service.find_dropdown_index(vga_options, vga_template_value)

            vga_selection = st.selectbox(
                "VGA",
                options=vga_options,
                format_func=lambda x: x[1],  # Show display name
                index=vga_index,
                help="Select dedicated graphics card or choose 'Other/Custom VGA...' for manual entry",
                key="laptop_vga_dropdown"
            )
            gpu = vga_selection[0]  # Get the value

            # Handle custom input
            if gpu == "CUSTOM":
                gpu = st.text_input(
                    "Enter custom VGA:", 
                    value=vga_template_value,
                    help="Enter dedicated graphics specification manually",
                    key="vga_custom"
                )
            
            # Integrated Graphics searchable dropdown
            graphics_options = dropdown_service.get_graphics_options()
            graphics_template_value = template_info.get('gpu', '')
            graphics_index = dropdown_service.find_dropdown_index(graphics_options, graphics_template_value)

            graphics_selection = st.selectbox(
                "Integrated Graphics",
                options=graphics_options,
                format_func=lambda x: x[1],  # Show display name
                index=graphics_index,
                help="Select integrated graphics or choose 'Other/Custom graphics...' for manual entry",
                key="laptop_graphics_dropdown"
            )
            integrated_gpu = graphics_selection[0]  # Get the value

            # Handle custom input
            if integrated_gpu == "CUSTOM":
                integrated_gpu = st.text_input(
                    "Enter custom integrated graphics:", 
                    value=graphics_template_value,
                    help="Enter integrated graphics specification manually",
                    key="graphics_custom"
                )
        
        with col2:
            # More specifications
            st.markdown("**Additional Specifications**")
            
            # Display searchable dropdown
            display_options = dropdown_service.get_display_options()
            display_template_value = template_info.get('display_full', template_info.get('display', ''))
            display_index = dropdown_service.find_dropdown_index(display_options, display_template_value)

            display_selection = st.selectbox(
                "Display",
                options=display_options,
                format_func=lambda x: x[1],  # Show display name
                index=display_index,
                help="Select display specification or choose 'Other/Custom display...' for manual entry",
                key="laptop_display_dropdown"
            )
            display = display_selection[0]  # Get the value

            # Handle custom input
            if display == "CUSTOM":
                display = st.text_input(
                    "Enter custom display:", 
                    value=display_template_value,
                    help="Enter display specification manually",
                    key="display_custom"
                )
            
            # Storage searchable dropdown
            storage_options = dropdown_service.get_storage_options()
            storage_template_value = template_info.get('storage_full', template_info.get('storage', ''))
            storage_index = dropdown_service.find_dropdown_index(storage_options, storage_template_value)

            storage_selection = st.selectbox(
                "Storage",
                options=storage_options,
                format_func=lambda x: x[1],  # Show display name
                index=storage_index,
                help="Select storage specification or choose 'Other/Custom storage...' for manual entry",
                key="laptop_storage_dropdown"
            )
            storage = storage_selection[0]  # Get the value

            # Handle custom input
            if storage == "CUSTOM":
                storage = st.text_input(
                    "Enter custom storage:", 
                    value=storage_template_value,
                    help="Enter storage specification manually",
                    key="storage_custom"
                )
            
            # Color searchable dropdown
            color_options = dropdown_service.get_color_options()
            color_template_value = template_info.get('color', '')
            color_index = dropdown_service.find_dropdown_index(color_options, color_template_value)

            color_selection = st.selectbox(
                "Color",
                options=color_options,
                format_func=lambda x: x[1],  # Show display name
                index=color_index,
                help="Select color/finish or choose 'Other/Custom color...' for manual entry",
                key="laptop_color_dropdown"
            )
            color = color_selection[0]  # Get the value

            # Handle custom input
            if color == "CUSTOM":
                color = st.text_input(
                    "Enter custom color:", 
                    value=color_template_value,
                    help="Enter color/finish specification manually",
                    key="color_custom"
                )
            
            # Keyboard Backlight dropdown
            keyboard_backlight_options = dropdown_service.get_keyboard_backlight_options()
            keyboard_backlight_template_value = template_info.get('keyboard_backlight', 'Yes')
            keyboard_backlight_index = dropdown_service.find_dropdown_index(keyboard_backlight_options, keyboard_backlight_template_value)

            keyboard_backlight_selection = st.selectbox(
                "Keyboard Backlight",
                options=keyboard_backlight_options,
                format_func=lambda x: x[1],  # Show display name
                index=keyboard_backlight_index,
                help="Select keyboard backlight type",
                key="laptop_keyboard_backlight_dropdown"
            )
            keyboard_backlight = keyboard_backlight_selection[0]  # Get the value
            
            # Optional fields
            st.markdown("**Optional Fields**")
            
            # OS dropdown
            os_options = dropdown_service.get_os_options()
            os_template_value = template_info.get('os', 'Windows 11')
            os_index = dropdown_service.find_dropdown_index(os_options, os_template_value)

            os_selection = st.selectbox(
                "Operating System",
                options=os_options,
                format_func=lambda x: x[1],  # Show display name
                index=os_index,
                help="Select operating system",
                key="laptop_os_dropdown"
            )
            operating_system = os_selection[0]  # Get the value

            # Keyboard Layout dropdown
            keyboard_layout_options = dropdown_service.get_keyboard_layout_options()
            keyboard_layout_template_value = template_info.get('keyboard_layout', 'US')
            keyboard_layout_index = dropdown_service.find_dropdown_index(keyboard_layout_options, keyboard_layout_template_value)

            keyboard_layout_selection = st.selectbox(
                "Keyboard Layout",
                options=keyboard_layout_options,
                format_func=lambda x: x[1],  # Show display name
                index=keyboard_layout_index,
                help="Select keyboard layout type",
                key="laptop_keyboard_layout_dropdown"
            )
            keyboard_layout = keyboard_layout_selection[0]  # Get the value
            
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
                    'operating_system': operating_system,
                    'keyboard_layout': keyboard_layout,
                    'keyboard_backlight': keyboard_backlight,
                    'inclusions': inclusions,
                    'minus': minus_issues,
                    'metafield_mappings': template_info.get('metafield_mappings', {})
                }
                
                # Check for missing metaobjects using enhanced logging
                metafields, missing_entries = product_service.convert_laptop_data_to_metafields_enhanced(laptop_data)
                
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
                validation_data['gpu'] = validation_data.pop('vga', '')  # Dedicated graphics (VGA field) → gpu
                validation_data['integrated_graphics'] = validation_data.pop('graphics', '')  # Integrated graphics → integrated_graphics
                validation_data['os'] = validation_data.pop('operating_system', '')
                
                laptop_product = LaptopProduct(**validation_data)
                
                # Store uploaded images for this product (if any) - simplified approach like smartphone
                
                # Store uploaded images directly (simplified like smartphone entry)
                if active_images:
                    if "product_images" not in st.session_state:
                        st.session_state.product_images = {}
                    # Store images with product handle as key
                    st.session_state.product_images[handle] = active_images
                
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
                    "laptop_cpu_dropdown", "cpu_custom", "laptop_ram_dropdown", 
                    "laptop_vga_dropdown", "vga_custom", "laptop_graphics_dropdown", "graphics_custom",
                    "laptop_display_dropdown", "display_custom", "laptop_storage_dropdown", "storage_custom",
                    "laptop_color_dropdown", "color_custom", "laptop_keyboard_backlight_dropdown",
                    "laptop_os_dropdown", "laptop_keyboard_layout_dropdown",
                    "laptop_inclusions_input", "laptop_minus_input", "laptop_collections_input"
                ]
                for key in laptop_form_keys:
                    if key in st.session_state:
                        del st.session_state[key]
                
                # Clear all form field keys to reset them completely (including image upload)
                laptop_form_keys.append("image_upload_form")
                
                # Increment reset counter to force file uploader reset
                if "form_reset_counter" not in st.session_state:
                    st.session_state.form_reset_counter = 0
                st.session_state.form_reset_counter += 1
                
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
                    
                    # Show image count and preview (read-only in main session view)
                    if hasattr(st.session_state, 'product_images') and product.get('handle') in st.session_state.product_images:
                        current_images = st.session_state.product_images[product.get('handle')]
                        image_count = len(current_images)
                        st.write(f"**Images**: 📸 {image_count} image(s)")
                        
                        # Display images in a grid (read-only preview)
                        if image_count > 0:
                            st.markdown("**Product Images:**")
                            img_cols = st.columns(min(image_count, 3))
                            
                            for img_idx, img_file in enumerate(current_images):
                                with img_cols[img_idx % 3]:
                                    try:
                                        img_file.seek(0)
                                        st.image(
                                            img_file,
                                            caption=f"Image {img_idx + 1}",
                                            width=100
                                        )
                                    except:
                                        st.error(f"Cannot display image {img_idx + 1}")
                    else:
                        st.write(f"**Images**: 📸 0 image(s)")
                
                with col3:
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
                            if hasattr(st.session_state, 'product_images') and removed_product.get('handle') in st.session_state.product_images:
                                del st.session_state.product_images[removed_product.get('handle')]
                            st.rerun()
                
                # Show missing metafields details if any
                if missing_count > 0:
                    with st.expander("⚠️ Missing Metafields Details"):
                        for field_name, values in product['missing_metafields'].items():
                            field_display = field_name.replace('_', ' ').title()
                            st.write(f"**{field_display}:** {', '.join(values)}")
                
                # Edit mode
                if st.session_state.get(f"editing_product_{i}", False):
                    st.markdown("---")
                    st.subheader(f"✏️ Edit Product {i+1}")
                    
                    # Show current images if any
                    current_images = []
                    if hasattr(st.session_state, 'product_images') and product.get('handle') in st.session_state.product_images:
                        current_images = st.session_state.product_images[product.get('handle')]
                    
                    if current_images:
                        st.markdown("**Current Images:**")
                        
                        # Track which images to remove (only initialize once per editing session)
                        images_to_remove_key = f"images_to_remove_edit_{i}"
                        if images_to_remove_key not in st.session_state:
                            st.session_state[images_to_remove_key] = set()
                        
                        images_to_remove = st.session_state[images_to_remove_key]
                        
                        # Display current images with delete options
                        img_cols = st.columns(min(len(current_images), 4))
                        for img_idx, img_file in enumerate(current_images):
                            if img_idx not in images_to_remove:
                                with img_cols[img_idx % 4]:
                                    try:
                                        img_file.seek(0)
                                        st.image(img_file, caption=f"Image {img_idx + 1}", width=120)
                                        if st.button(f"🗑️ Remove", key=f"remove_img_edit_{i}_{img_idx}"):
                                            st.session_state[images_to_remove_key].add(img_idx)
                                            st.rerun()
                                    except:
                                        st.error(f"Cannot display image {img_idx + 1}")
                        
                        # Prepare images to keep
                        images_to_keep = [img for idx, img in enumerate(current_images) if idx not in images_to_remove]
                    else:
                        images_to_keep = []
                    
                    # Upload new images (simplified approach)
                    st.markdown("**Upload New Images:**")
                    new_uploaded_files = image_service.render_image_upload_interface(f"edit_{i}")
                    
                    # Preview new images
                    new_active_images = []
                    if new_uploaded_files:
                        new_active_images = image_service.render_image_preview(new_uploaded_files, f"edit_{i}")
                    
                    # Combine kept current images and new images
                    all_images = images_to_keep + new_active_images
                    
                    if all_images:
                        st.success(f"Total images for this product: {len(all_images)}")
                    
                    st.divider()
                    
                    # Edit form for product data
                    with st.form(f"edit_form_{i}"):
                        # Editable fields
                        new_title = st.text_input("Product Title", value=product.get('title', ''), key=f"edit_title_{i}")
                        new_price = st.number_input("Price (¥)", value=float(product.get('price', 0)), min_value=0.0, step=100.0, key=f"edit_price_{i}")
                        new_rank = st.selectbox("Product Rank", options=[1, 2, 3, 4, 5], index=int(product.get('rank', 1)) - 1, key=f"edit_rank_{i}")
                        
                        # Editable collections
                        new_collections = st.multiselect(
                            "Collections",
                            ['All Products', 'Laptop', 'Gaming', 'Business', 'ASUS', 'Dell', 'HP', 'Lenovo', 'MSI'],
                            default=product.get('collections', []),
                            key=f"edit_collections_{i}"
                        )
                        
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
                            else:
                                try:
                                    # Update product data
                                    updated_data = product.copy()
                                    updated_data["title"] = new_title.strip()
                                    updated_data["price"] = new_price
                                    updated_data["rank"] = new_rank
                                    updated_data["collections"] = new_collections
                                    
                                    # Generate new handle if title changed
                                    if new_title.strip() != product.get('title', ''):
                                        # generate_handle already imported at top
                                        new_handle = generate_handle(new_title.strip())
                                        updated_data["handle"] = new_handle
                                        
                                        # Update images dictionary key if handle changed
                                        if hasattr(st.session_state, 'product_images') and product.get('handle') in st.session_state.product_images:
                                            st.session_state.product_images[new_handle] = st.session_state.product_images.pop(product.get('handle'))
                                    
                                    # Update images
                                    if all_images:
                                        st.session_state.product_images[updated_data["handle"]] = all_images
                                    elif updated_data["handle"] in st.session_state.product_images:
                                        # Remove images if none left
                                        del st.session_state.product_images[updated_data["handle"]]
                                    
                                    # Update product in session
                                    st.session_state.products[i] = updated_data
                                    
                                    # Clear edit state
                                    st.session_state[f"editing_product_{i}"] = False
                                    if images_to_remove_key in st.session_state:
                                        del st.session_state[images_to_remove_key]
                                    
                                    st.success("✅ Product updated successfully!")
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"Error updating product: {str(e)}")
                        
                        if cancel_clicked:
                            # Clear edit state
                            st.session_state[f"editing_product_{i}"] = False
                            if images_to_remove_key in st.session_state:
                                del st.session_state[images_to_remove_key]
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
                    # Prepare laptop products list
                    laptop_products = []
                    for product in st.session_state.products:
                        # Filter out extra fields that aren't part of LaptopProduct model
                        product_data = {k: v for k, v in product.items() 
                                      if k not in ['missing_metafields', 'available_metafields']}
                        laptop_products.append(LaptopProduct(**product_data))
                    
                    # Get product images from session state (if any)
                    product_images = getattr(st.session_state, 'product_images', {})
                    
                    
                    # Use bulk upload method with integrated image handling
                    with st.spinner("Creating laptops in Shopify..."):
                        results = product_service.upload_multiple_laptops(laptop_products, product_images)
                    
                    # Show results
                    success_count = results.get('success_count', 0)
                    failed_count = results.get('failed_count', 0)
                    
                    if success_count > 0:
                        st.success(f"✅ Created {success_count} laptops successfully!")
                        
                        # Check for partial image uploads
                        for result in results.get('results', []):
                            if result.get('success') and result.get('image_upload_partial'):
                                st.warning(f"⚠️ Some images failed for {result.get('title', 'Unknown laptop')}")
                    
                    if failed_count > 0:
                        st.error(f"❌ {failed_count} laptops failed to create")
                        
                        # Show specific errors
                        for result in results.get('results', []):
                            if not result.get('success'):
                                st.error(f"• {result.get('title', 'Unknown')}: {result.get('error', 'Unknown error')}")
                    
                    # Clear session after successful creation
                    if success_count > 0:
                        st.session_state.products = []
                        # Clear associated images
                        if hasattr(st.session_state, 'product_images'):
                            st.session_state.product_images = {}
                        clear_session_data()  # Clear enhanced logging session data
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Bulk creation failed: {str(e)}")
        
        with col3:
            if st.button("🗑️ Clear Session", use_container_width=True):
                st.session_state.products = []
                # Clear associated images
                if hasattr(st.session_state, 'product_images'):
                    st.session_state.product_images = {}
                st.rerun()

if __name__ == "__main__":
    laptop_entry_page()