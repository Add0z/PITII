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

def show_orders_page():
    """Displays the user's order history."""
    logo_bytes = get_image_bytes("images/logoFull.jpg")
    if logo_bytes:
        st.sidebar.image(logo_bytes, use_container_width=True)
        
    st.sidebar.write(f"Welcome, {st.session_state['user_info'].name}!")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
        
    st.title("My Orders")
    
    user_id = st.session_state['user_info'].id
    orders = db.get_orders_by_user(user_id)

    if not orders:
        st.warning("You have no past orders.")
        return

    for order in orders:
        with st.expander(f"Order #{order.id} - {order.order_date} - Status: {order.status}"):
            items = db.get_order_items(order.id)
            for item in items:
                product = db.get_product_by_id(item.product_id)
                if product:
                    st.write(f"• {product.name} - Quantity: {item.quantity}")
            st.write(f"**Total: ${order.total_price:.2f}**")
            
            if order.status == "Pending":
                if st.button("Cancel Order", key=f"cancel_{order.id}"):
                    if db.cancel_order(order.id):
                        st.success("Order cancelled successfully.")
                        st.rerun()
                    else:
                        st.error("Could not cancel the order. It may have already been shipped.")

# --- Main Execution ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to view your orders.")
    st.stop()

show_orders_page()
