import streamlit as st
from data import database as db
from data.data_models import User
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

def show_profile_page():
    """Allows a user to update their profile information."""
    logo_bytes = get_image_bytes("images/logoFull.jpg")
    if logo_bytes:
        st.sidebar.image(logo_bytes, use_container_width=True)
        
    st.sidebar.write(f"Welcome, {st.session_state['user_info'].name}!")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
        
    st.header("Update Profile")
    
    user = st.session_state['user_info']
    
    with st.form("profile_form"):
        name = st.text_input("Name", value=user.name)
        email = st.text_input("Email", value=user.email)
        password = st.text_input("New Password (leave blank to keep current)", type="password")
        
        submitted = st.form_submit_button("Update")
        if submitted:
            updated_user = User(id=user.id, name=name, email=email, password=password, is_admin=user.is_admin)
            db.update_user(updated_user)
            st.session_state['user_info'] = db.get_user_by_email(email)
            st.success("Profile updated successfully!")
            st.rerun()

# --- Main Execution ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to view your profile.")
    st.stop()

show_profile_page()
