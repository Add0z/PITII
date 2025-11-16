import streamlit as st
from data import database as db
from data.data_models import User
from styles.styling import (apply_styles)
import os

# --- Page Configuration and Global Setup ---
st.set_page_config(page_title="Cupcake Store", layout="wide")
apply_styles()
db.create_tables()

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# --- Helper to get image bytes ---
def get_image_bytes(image_path):
    try:
        abs_path = os.path.abspath(image_path)
        with open(abs_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None

# --- Authentication Views ---
def show_login_view():
    """Displays the login and signup forms."""
    logo_bytes = get_image_bytes("images/logoFull.jpg")
    if logo_bytes:
        _, col2, _ = st.columns([1.7, 2, 1])
        with col2:
            st.image(logo_bytes, width=400)

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login", use_container_width=True):
                    user = db.get_user_by_email(email)
                    if user and user.password == db.hash_password(password):
                        if user.status == 'active':
                            st.session_state['logged_in'] = True
                            st.session_state['user_info'] = user
                            st.rerun()
                        else:
                            st.error("This account is inactive or blocked.")
                    else:
                        st.error("Invalid email or password.")

    with signup_tab:
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            with st.form("signup_form", clear_on_submit=True):
                name = st.text_input("Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Sign Up", use_container_width=True):
                    if db.get_user_by_email(email):
                        st.error("This email is already registered.")
                    else:
                        new_user = User(name=name, email=email, password=password, status='active')
                        db.add_user(new_user)
                        st.success("Account created successfully! Please log in.")

# --- Main Application Router ---
def main():
    """The main function that runs the Streamlit app."""
    if not st.session_state['logged_in']:
        show_login_view()
    else:
        # If logged in, show sidebar with small logo and switch to shop
        logo_bytes = get_image_bytes("images/logoFull.jpg")
        if logo_bytes:
            st.sidebar.image(logo_bytes, use_container_width=True)
        
        st.sidebar.write(f"Welcome, {st.session_state['user_info'].name}!")
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.switch_page("pages/01_Shop.py")

if __name__ == "__main__":
    main()
