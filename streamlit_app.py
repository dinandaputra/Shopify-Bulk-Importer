import streamlit as st
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.smartphone_entry import smartphone_entry_page

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
        st.header("Session Stats")
        if "products" not in st.session_state:
            st.session_state.products = []
        
        st.metric("Products in Session", len(st.session_state.products))
        st.metric("Session Limit", f"{len(st.session_state.products)}/10")
        
        if len(st.session_state.products) > 0:
            if st.button("Clear Session", type="secondary"):
                st.session_state.products = []
                st.rerun()
                
        st.divider()
        st.caption("💡 Future categories (Laptop, etc.) will be added as needed")
    
    # Main content - directly load smartphone entry
    smartphone_entry_page()

if __name__ == "__main__":
    main()