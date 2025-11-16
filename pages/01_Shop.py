import streamlit as st
from data import database as db
from data.data_models import Product
from styles.styling import apply_styles
import os

apply_styles()

# --- Helper Functions ---
def get_image_bytes(image_path):
    """Reads an image file and returns its bytes."""
    try:
        abs_path = os.path.abspath(image_path)
        with open(abs_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None

def add_to_cart(product, quantity):
    """Adds a product to the shopping cart in the session state."""
    # Backend validation for quantity
    if not isinstance(quantity, int) or quantity <= 0:
        st.error("Quantity must be a positive number.")
        return

    cart_item = {'product_id': product.id, 'quantity': quantity}
    
    for item in st.session_state['cart']:
        if item['product_id'] == product.id:
            item['quantity'] += quantity
            return
            
    st.session_state['cart'].append(cart_item)

# --- Page Implementation ---
def show_shop_page():
    """Displays the main shop page with product listings."""
    logo_bytes = get_image_bytes("images/logoFull.jpg")
    if logo_bytes:
        st.sidebar.image(logo_bytes, use_container_width=True)
        
    st.sidebar.write(f"Welcome, {st.session_state['user_info'].name}!")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
        
    st.title("Cupcake Vitrine")
    
    flavors = ["All"] + db.get_flavors()
    selected_flavor = st.sidebar.selectbox("Filter by Flavor", flavors)
    
    products = db.get_all_products(flavor_filter=selected_flavor)
    
    if not products:
        st.warning("No products available for the selected filter.")
        return

    cols = st.columns(3)
    for i, product in enumerate(products):
        with cols[i % 3]:
            with st.container():
                st.markdown('<div class="st-emotion-cache-0">', unsafe_allow_html=True)
                if product.image_url:
                    image_bytes = get_image_bytes(product.image_url)
                    if image_bytes:
                        st.image(image_bytes, caption=product.name)
                    else:
                        st.image("https://via.placeholder.com/150", caption=f"{product.name}")
                        st.warning(f"Image not found at: {os.path.abspath(product.image_url)}")
                else:
                    st.image("https://via.placeholder.com/150", caption=product.name)
                
                st.subheader(product.name)
                st.write(f"**Price:** ${product.price:.2f}")
                quantity = st.number_input("Quantity", min_value=1, max_value=product.stock, value=1, step=1, key=f"qty_{product.id}")
                if st.button("Add to Cart", key=f"add_{product.id}"):
                    add_to_cart(product, quantity)
                    st.success(f"Added {quantity} of {product.name} to cart!")
                st.markdown('</div>', unsafe_allow_html=True)

# --- Main Execution ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to access the shop.")
    st.stop()

show_shop_page()
