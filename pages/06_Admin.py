import streamlit as st
from data import database as db
from data.data_models import Product, User
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

def show_product_management():
    st.header("Product Management")
    
    with st.expander("Add New Product"):
        with st.form("add_product_form", clear_on_submit=True):
            name = st.text_input("Name")
            description = st.text_area("Description")
            price = st.number_input("Price", min_value=0.0, format="%.2f")
            stock = st.number_input("Stock", min_value=0)
            flavor = st.text_input("Flavor")
            image_url = st.text_input("Image URL", placeholder="e.g., images/my_cupcake.jpg.png")
            
            submitted = st.form_submit_button("Add Product")
            if submitted:
                new_product = Product(name=name, description=description, price=price, stock=stock, flavor=flavor, image_url=image_url)
                db.add_product(new_product)
                st.success("Product added successfully!")
                st.rerun()

    st.subheader("Existing Products")
    products = db.get_all_products()
    for product in products:
        with st.expander(f"Edit: {product.name}"):
            with st.form(f"edit_form_{product.id}"):
                name = st.text_input("Name", value=product.name, key=f"name_{product.id}")
                description = st.text_area("Description", value=product.description, key=f"desc_{product.id}")
                price = st.number_input("Price", value=product.price, key=f"price_{product.id}", format="%.2f")
                stock = st.number_input("Stock", value=product.stock, key=f"stock_{product.id}")
                flavor = st.text_input("Flavor", value=product.flavor, key=f"flavor_{product.id}")
                image_url = st.text_input("Image URL", value=product.image_url, key=f"image_url_{product.id}")
                
                if st.form_submit_button("Update"):
                    updated_product = Product(id=product.id, name=name, description=description, price=price, stock=stock, flavor=flavor, image_url=image_url)
                    db.update_product(updated_product)
                    st.success("Product updated!")
                    st.rerun()

        if st.button("Delete", key=f"delete_{product.id}"):
            db.delete_product(product.id)
            st.success("Product deleted!")
            st.rerun()

def show_order_management():
    st.header("Order Management")
    orders = db.get_all_orders()

    if not orders:
        st.warning("No orders found.")
        return

    for order in orders:
        with st.expander(f"Order #{order.id} - User ID: {order.user_id} - Status: {order.status}"):
            items = db.get_order_items(order.id)
            for item in items:
                product = db.get_product_by_id(item.product_id)
                st.write(f"• {product.name} (Qty: {item.quantity})")
            st.write(f"**Total: ${order.total_price:.2f}**")
            
            status_options = ["Pending", "Shipped", "Delivered", "Cancelled"]
            current_status_index = status_options.index(order.status) if order.status in status_options else 0
            new_status = st.selectbox(
                "Update Status", status_options, index=current_status_index, key=f"status_{order.id}"
            )
            if st.button("Update Status", key=f"update_status_{order.id}"):
                db.update_order_status(order.id, new_status)
                st.success("Order status updated!")
                st.rerun()

def show_user_management():
    st.header("User Management")
    users = db.get_all_users()

    for user in users:
        st.write(f"**{user.name}** ({user.email}) - ID: {user.id}")
        is_admin = st.checkbox("Is Admin?", value=user.is_admin, key=f"admin_{user.id}")
        if st.button("Update Role", key=f"update_role_{user.id}"):
            db.update_user_admin_status(user.id, is_admin)
            st.success(f"User {user.name}'s role updated.")
            st.rerun()
        st.markdown("---")

def show_stock_management():
    st.header("Stock Management")
    products = db.get_all_products()
    for product in products:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**{product.name}**")
        with col2:
            new_stock = st.number_input("Current Stock", value=product.stock, min_value=0, key=f"stock_level_{product.id}")
        with col3:
            if st.button("Update Stock", key=f"update_stock_{product.id}"):
                db.set_product_stock(product.id, new_stock)
                st.success(f"{product.name} stock updated to {new_stock}.")
                st.rerun()

def show_store_settings():
    st.header("Store Settings")
    settings = db.get_store_settings()
    
    st.subheader("Payment Methods")
    payment_methods = settings.get('payment_methods', [])
    methods_text = "\n".join(payment_methods)
    
    new_methods_text = st.text_area("Edit Payment Methods (one per line)", value=methods_text, height=150)
    if st.button("Update Payment Methods"):
        new_methods = [line.strip() for line in new_methods_text.split("\n") if line.strip()]
        db.update_store_setting('payment_methods', new_methods)
        st.success("Payment methods updated.")
        st.rerun()

def show_admin_page():
    """The main container for all admin-related functionalities."""
    logo_bytes = get_image_bytes("images/logoFull.jpg")
    if logo_bytes:
        st.sidebar.image(logo_bytes, use_container_width=True)
        
    st.sidebar.write(f"Welcome, {st.session_state['user_info'].name}!")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
        
    st.title("Admin Dashboard")
    
    admin_pages = {
        "Product Management": show_product_management,
        "Order Management": show_order_management,
        "User Management": show_user_management,
        "Stock Management": show_stock_management,
        "Store Settings": show_store_settings,
    }
    
    selection = st.sidebar.radio("Admin Menu", list(admin_pages.keys()))
    
    page_to_show = admin_pages[selection]
    page_to_show()

# --- Main Execution ---
if 'logged_in' not in st.session_state or not st.session_state.get('logged_in'):
    st.warning("You must be logged in to access this page.")
    st.stop()
if not st.session_state.get('user_info').is_admin:
    st.error("You do not have permission to access this page.")
    st.stop()

show_admin_page()
