import streamlit as st
from data import database as db
from data.data_models import Order
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

def show_checkout_page():
    """Displays the checkout page with order summary and a fake payment form."""
    logo_bytes = get_image_bytes("images/logoFull.jpg")
    if logo_bytes:
        st.sidebar.image(logo_bytes, use_container_width=True)
        
    st.sidebar.write(f"Welcome, {st.session_state['user_info'].name}!")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
        
    st.title("Checkout")

    if 'cart' not in st.session_state or not st.session_state['cart']:
        st.warning("Your cart is empty. Add items to your cart to proceed to checkout.")
        st.stop()

    cart_items = st.session_state['cart']
    total_price = 0

    st.subheader("Order Summary")
    for item in cart_items:
        product = db.get_product_by_id(item['product_id'])
        if product:
            st.write(f"- {product.name} (Quantity: {item['quantity']})")
            total_price += product.price * item['quantity']
    
    st.markdown("---")
    st.write(f"### Total: ${total_price:.2f}")
    st.markdown("---")

    st.subheader("Payment Information (Simulation)")
    with st.form("payment_form"):
        st.text_input("Cardholder Name", "John Doe")
        st.text_input("Card Number", "1234-5678-9012-3456")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Expiry Date (MM/YY)", "12/25")
        with col2:
            st.text_input("CVV", "***", type="password")
        
        payment_methods = db.get_store_settings().get('payment_methods', [])
        st.selectbox("Payment Method", payment_methods)

        submitted = st.form_submit_button("Pay Now")
        if submitted:
            user_id = st.session_state['user_info'].id
            new_order = Order(user_id=user_id, total_price=total_price, status="Pending")
            db.create_order(new_order, cart_items)
            
            st.session_state['cart'] = []
            
            st.success("Order placed successfully! Thank you for your purchase.")
            st.balloons()
            
            st.switch_page("pages/04_My_Orders.py")

# --- Main Execution ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to proceed to checkout.")
    st.stop()

show_checkout_page()
