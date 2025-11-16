import streamlit as st
from data import database as db
from styles.styling import apply_styles
import os

apply_styles()

def get_image_bytes(image_path):
    """Reads an image file and returns its bytes."""
    try:
        abs_path = os.path.abspath(image_path)
        with open(abs_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None

def remove_from_cart(item_index):
    """Removes an item from the shopping cart."""
    if 0 <= item_index < len(st.session_state['cart']):
        st.session_state['cart'].pop(item_index)

def show_cart_page():
    """Displays the shopping cart contents and checkout button."""
    logo_bytes = get_image_bytes("images/logoFull.jpg")
    if logo_bytes:
        st.sidebar.image(logo_bytes, use_container_width=True)
        
    st.sidebar.write(f"Welcome, {st.session_state['user_info'].name}!")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
        
    st.title("Your Shopping Cart")
    
    if 'cart' not in st.session_state or not st.session_state['cart']:
        st.warning("Your cart is empty.")
        st.stop()

    total_price = 0
    
    st.markdown("---")
    
    for i, item in enumerate(st.session_state['cart']):
        product = db.get_product_by_id(item['product_id'])
        if product:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if product.image_url:
                    image_bytes = get_image_bytes(product.image_url)
                    if image_bytes:
                        st.image(image_bytes, width=100)
                else:
                    st.image("https://via.placeholder.com/100", width=100)

            with col2:
                st.subheader(product.name)
                st.write(f"Quantity: {item['quantity']}")
                st.write(f"Price per unit: ${product.price:.2f}")

            with col3:
                st.write(f"**Total: ${product.price * item['quantity']:.2f}**")
                if st.button("Remove", key=f"remove_{i}"):
                    remove_from_cart(i)
                    st.rerun()
            
            total_price += product.price * item['quantity']
            st.markdown("---")
    
    st.markdown(f"<h3 style='text-align: right;'>Grand Total: ${total_price:.2f}</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            .st-emotion-cache-7ym5gk {
                display: flex;
                justify-content: flex-end;
            }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("Proceed to Checkout"):
        st.switch_page("pages/03_Checkout.py")

# --- Main Execution ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to view your cart.")
    st.stop()

show_cart_page()
