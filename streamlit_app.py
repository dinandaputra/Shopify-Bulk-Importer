import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.smartphone_entry import smartphone_entry_page
from pages.laptop_entry import laptop_entry_page

def main():
    st.set_page_config(
        page_title="MyByte Shopify Product Manager",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📱 MyByte Shopify Product Manager")
    st.markdown("### Streamlined product entry for used electronics")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Product Categories")
        
        # Category selection
        category = st.selectbox(
            "Select Category:",
            ["📱 Smartphones", "💻 Laptops"],
            help="Choose product category to manage"
        )
        
        st.divider()
        
        st.header("Session Stats")
        if "products" not in st.session_state:
            st.session_state.products = []
        
        st.metric("Products in Session", len(st.session_state.products))
        st.metric("Session Limit", f"{len(st.session_state.products)}/10")
        
        if len(st.session_state.products) > 0:
            if st.button("Clear Session", type="secondary"):
                st.session_state.products = []
                st.rerun()
    
    # Main content - load appropriate page based on category
    if category == "📱 Smartphones":
        smartphone_entry_page()
    elif category == "💻 Laptops":
        laptop_entry_page()

if __name__ == "__main__":
    main()