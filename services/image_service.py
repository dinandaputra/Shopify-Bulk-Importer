import requests
import base64
import os
import time
from typing import List, Dict, Optional, Union
from services.shopify_api import ShopifyAPIClient, ShopifyAPIError
import streamlit as st

class ImageUploadError(Exception):
    """Custom exception for image upload errors"""
    pass

class ImageService:
    """
    Service for handling image uploads to Shopify CDN
    Supports drag & drop, multiple images, and graceful error handling
    """
    
    def __init__(self):
        self.shopify_client = ShopifyAPIClient()
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        self.max_file_size = 10 * 1024 * 1024  # 10MB limit
    
    def validate_image(self, uploaded_file) -> bool:
        """
        Validate uploaded image file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not uploaded_file:
            return False
            
        # Check file extension
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension not in self.supported_formats:
            st.error(f"Unsupported file format: {file_extension}. Supported formats: {', '.join(self.supported_formats)}")
            return False
            
        # Check file size
        if uploaded_file.size > self.max_file_size:
            st.error(f"File too large: {uploaded_file.size / (1024*1024):.1f}MB. Maximum size: {self.max_file_size / (1024*1024)}MB")
            return False
            
        return True
    
    def encode_image_to_base64(self, uploaded_file) -> str:
        """
        Convert uploaded file to base64 for Shopify API
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            str: Base64 encoded image data
        """
        try:
            # Reset file pointer
            uploaded_file.seek(0)
            image_data = uploaded_file.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            return encoded_image
        except Exception as e:
            raise ImageUploadError(f"Failed to encode image: {str(e)}")
    
    def generate_image_filename(self, product_handle: str, image_index: int = 0) -> str:
        """
        Generate standardized filename for product images
        
        Args:
            product_handle: Product handle for naming
            image_index: Index for multiple images (0 for single image)
            
        Returns:
            str: Generated filename
        """
        if image_index == 0:
            return f"{product_handle}"
        else:
            return f"{product_handle}_{image_index + 1}"
    
    def upload_image_to_shopify(self, product_id: str, uploaded_file, position: int = 1) -> Dict:
        """
        Upload single image to Shopify product
        
        Args:
            product_id: Shopify product ID
            uploaded_file: Streamlit uploaded file object
            position: Image position in product gallery
            
        Returns:
            dict: Shopify image response data
            
        Raises:
            ImageUploadError: If upload fails
        """
        try:
            # Validate image
            if not self.validate_image(uploaded_file):
                raise ImageUploadError("Image validation failed")
            
            # Encode image to base64
            encoded_image = self.encode_image_to_base64(uploaded_file)
            
            # Prepare image data for Shopify API
            image_data = {
                "image": {
                    "attachment": encoded_image,
                    "filename": uploaded_file.name,
                    "position": position
                }
            }
            
            # Upload to Shopify
            endpoint = f"products/{product_id}/images.json"
            response = self.shopify_client._make_request("POST", endpoint, data=image_data)
            
            return response.get('image', {})
            
        except ShopifyAPIError as e:
            raise ImageUploadError(f"Shopify API error: {str(e)}")
        except Exception as e:
            raise ImageUploadError(f"Image upload failed: {str(e)}")
    
    def upload_multiple_images(self, product_id: str, uploaded_files: List, progress_callback=None) -> List[Dict]:
        """
        Upload multiple images to Shopify product
        
        Args:
            product_id: Shopify product ID
            uploaded_files: List of Streamlit uploaded file objects
            progress_callback: Optional callback for progress updates
            
        Returns:
            list: List of uploaded image data
        """
        uploaded_images = []
        failed_uploads = []
        
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                # Update progress if callback provided
                if progress_callback:
                    progress_callback(i + 1, len(uploaded_files), uploaded_file.name)
                
                # Upload image
                image_data = self.upload_image_to_shopify(product_id, uploaded_file, position=i + 1)
                uploaded_images.append(image_data)
                
                # Small delay between uploads to respect rate limits
                if i < len(uploaded_files) - 1:
                    time.sleep(0.5)
                    
            except ImageUploadError as e:
                failed_uploads.append({
                    'filename': uploaded_file.name,
                    'error': str(e)
                })
                continue
        
        # Report results
        if uploaded_images:
            st.success(f"Successfully uploaded {len(uploaded_images)} image(s)")
        
        if failed_uploads:
            st.warning(f"Failed to upload {len(failed_uploads)} image(s):")
            for failure in failed_uploads:
                st.error(f"- {failure['filename']}: {failure['error']}")
        
        return uploaded_images
    
    def delete_product_image(self, product_id: str, image_id: str) -> bool:
        """
        Delete image from Shopify product
        
        Args:
            product_id: Shopify product ID
            image_id: Shopify image ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            endpoint = f"products/{product_id}/images/{image_id}.json"
            self.shopify_client._make_request("DELETE", endpoint)
            return True
        except ShopifyAPIError as e:
            st.error(f"Failed to delete image: {str(e)}")
            return False
    
    def get_product_images(self, product_id: str) -> List[Dict]:
        """
        Get all images for a product
        
        Args:
            product_id: Shopify product ID
            
        Returns:
            list: List of product images
        """
        try:
            endpoint = f"products/{product_id}/images.json"
            response = self.shopify_client._make_request("GET", endpoint)
            return response.get('images', [])
        except ShopifyAPIError as e:
            st.error(f"Failed to fetch product images: {str(e)}")
            return []
    
    def render_image_upload_interface(self, key_suffix: str = "") -> List:
        """
        Render drag & drop image upload interface
        
        Args:
            key_suffix: Unique suffix for widget keys
            
        Returns:
            list: List of uploaded files
        """
        st.subheader("📸 Product Images")
        
        # Instructions
        st.markdown("""
        **Upload product images (optional but recommended)**
        - Drag & drop files or click to browse
        - Supported formats: JPG, PNG, WebP, GIF
        - Maximum size: 10MB per image
        - Multiple images supported
        """)
        
        # Generate dynamic key based on session state to force reset
        if "form_reset_counter" not in st.session_state:
            st.session_state.form_reset_counter = 0
        
        dynamic_key = f"image_upload_{key_suffix}_{st.session_state.form_reset_counter}"
        
        # File uploader with drag & drop
        uploaded_files = st.file_uploader(
            "Choose image files",
            type=['jpg', 'jpeg', 'png', 'webp', 'gif'],
            accept_multiple_files=True,
            key=dynamic_key,
            help="Drag and drop image files here, or click to browse"
        )
        
        return uploaded_files if uploaded_files else []
    
    def render_image_preview(self, uploaded_files: List, key_suffix: str = "") -> List:
        """
        Render image preview thumbnails with delete option
        
        Args:
            uploaded_files: List of uploaded file objects
            key_suffix: Unique suffix for widget keys
            
        Returns:
            list: Updated list of uploaded files after any deletions
        """
        if not uploaded_files:
            return []
        
        st.subheader("🖼️ Image Preview")
        
        # Use session state to track which images to keep (with dynamic counter)
        if "form_reset_counter" not in st.session_state:
            st.session_state.form_reset_counter = 0
        
        dynamic_key = f"images_to_keep_{key_suffix}_{st.session_state.form_reset_counter}"
        
        if dynamic_key not in st.session_state:
            st.session_state[dynamic_key] = list(range(len(uploaded_files)))
        
        images_to_keep = st.session_state[dynamic_key]
        
        # Display images in columns
        active_files = [uploaded_files[i] for i in images_to_keep if i < len(uploaded_files)]
        
        if not active_files:
            st.info("No images selected. Upload images above to see preview.")
            return []
        
        cols = st.columns(min(len(active_files), 4))
        
        for idx, file_index in enumerate([i for i in images_to_keep if i < len(uploaded_files)]):
            uploaded_file = uploaded_files[file_index]
            with cols[idx % 4]:
                try:
                    # Reset file pointer and display image
                    uploaded_file.seek(0)
                    st.image(
                        uploaded_file,
                        caption=f"{uploaded_file.name} ({uploaded_file.size / 1024:.1f}KB)",
                        width=150
                    )
                    
                    # Delete button for each image
                    if st.button(f"🗑️ Remove", key=f"remove_img_{key_suffix}_{st.session_state.form_reset_counter}_{file_index}"):
                        # Remove this image from the keep list
                        st.session_state[dynamic_key] = [
                            i for i in images_to_keep if i != file_index
                        ]
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Cannot preview {uploaded_file.name}: {str(e)}")
        
        return active_files
    
    def handle_post_creation_upload(self, product_id: str, uploaded_files: List) -> bool:
        """
        Handle image upload after product creation with progress tracking
        
        Args:
            product_id: Shopify product ID
            uploaded_files: List of uploaded file objects
            
        Returns:
            bool: True if all uploads successful or no images, False if some failed
        """
        if not uploaded_files:
            return True
        
        st.info(f"Uploading {len(uploaded_files)} image(s) to Shopify...")
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def progress_callback(current: int, total: int, filename: str):
            progress = current / total
            progress_bar.progress(progress)
            status_text.text(f"Uploading image {current}/{total}: {filename}")
        
        try:
            # Upload images
            uploaded_images = self.upload_multiple_images(
                product_id, 
                uploaded_files, 
                progress_callback
            )
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Return success status
            return len(uploaded_images) == len(uploaded_files)
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Image upload error: {str(e)}")
            return False

# Initialize global image service instance
image_service = ImageService()