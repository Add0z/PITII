import streamlit as st

def apply_styles():
    """
    Applies custom CSS styles to the Streamlit app.
    """
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Nunito:wght@400;700&display=swap');

            /* --- Main Colors --- */
            :root {
                --primary-color: #D988B9; /* Soft Pink */
                --secondary-color: #B9A2D9; /* Lavender */
                --background-color: #FDF4F5; /* Creamy White */
                --text-color: #5C3D2E; /* Chocolate Brown */
                --accent-color: #E7CBA9; /* Light Gold */
            }

            /* --- General Styling --- */
            body, .stApp {
                background-color: var(--background-color);
                color: var(--text-color);
                font-family: 'Nunito', sans-serif;
            }

            /* --- Titles and Headers --- */
            h1, h2, h3 {
                font-family: 'Pacifico', cursive;
                color: var(--primary-color);
            }
            h1 { /* Specific rule for h1 to change its color */
                color: var(--secondary-color);
            }

            /* --- Buttons --- */
            .stButton > button {
                background-color: var(--primary-color);
                color: white; /* Changed to white */
                border-radius: 20px;
                border: none;
                padding: 10px 20px;
                transition: background-color 0.3s;
            }
            .stButton > button:hover {
                background-color: var(--secondary-color);
            }
            
            /* --- Form Submit Buttons (Login/Sign Up) --- */
            .stForm button {
                background-color: #5D9A95 !important;
                color: white !important;
                border-radius: 20px !important;
                border: none !important;
                padding: 10px 20px !important;
            }
            
            .stForm button:hover {
                background-color: #4A7B77 !important;
            }
            
            button[data-testid="baseButton-primary"] {
                background-color: #5D9A95 !important;
                color: white !important;
            }
            
            button[data-testid="baseButton-primary"]:hover {
                background-color: #4A7B77 !important;
            }

            /* --- Tabs --- */
            div[role="tablist"] {
                justify-content: center;
            }

            button[data-baseweb="tab"] {
                background-color: beige !important;
                color: var(--text-color) !important;
                border-radius: 5px 5px 0 0;
            }

            button[data-baseweb="tab"]:hover {
                background-color: var(--accent-color) !important;
                color: var(--text-color) !important;
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                background-color: var(--primary-color) !important;
                color: var(--secondary-color) !important;
            }

            /* --- Sidebar --- */
            [data-testid="stSidebar"] {
                background-color: #5D9A95 !important;
            }
            [data-testid="stSidebar"] .st-emotion-cache-1v0mbdj, [data-testid="stSidebar"] .st-emotion-cache-1kyxreq {
                color: var(--text-color);
            }

            /* --- Product Cards --- */
            .st-emotion-cache-0 {
                color: var(--text-color);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }

            /* Remove top padding/margin from st.image components within product cards */
            .st-emotion-cache-0 [data-testid="stImage"] {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            .st-emotion-cache-0 [data-testid="stImage"] > div:first-child {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            
            /* --- Expander (for admin and orders) */
            .st-emotion-cache-p5msec {
                border: 1px solid var(--accent-color);
                border-radius: 10px;
                background-color: white;
            }
            .st-emotion-cache-p5msec summary {
                font-weight: bold;
                color: var(--primary-color);
            }
            
            .stNumberInput input {
                background-color: #9FD3C4 !important;
                border-color: #79BFA0 !important;
            }
            
            .stNumberInput button {
                background-color: #79BFA0 !important;
                color: white !important; /* Ensure button text is readable */
            }
            /* --- Alert/Warning/Info Boxes --- */
            .stAlert p {
                color: var(--text-color) !important;
            }

            /* --- Form & Input Labels --- */
            label {
                color: #000000 !important;
            }
            
            .stTextInput label, .stTextInput > label {
                color: #000000 !important;
            }

            /* Remove focus outline from text inputs */
            .stTextInput input:focus {
                outline: none !important;
                box-shadow: none !important;
            }

            /* Style for st.text_input boxes */
            .stTextInput input {
                background-color: #79BFA0 !important;
                border: 1px solid white !important; /* Added white border */
                color: white !important; /* Ensure text is readable */
            }

            /* Style for "Press enter to submit the form" text */
            .stForm small {
                color: white !important;
            }
            
            /* Style for the eye button on password input */
            .stTextInput button {
                background-color: #9FD3C4 !important;
                border: none !important;
            }
            
            .stTextInput button:hover {
                background-color: #79BFA0 !important;
                
            }
            
            [data-testid="StyledFullScreenButton"] {
                background-color: #9FD3C4 !important;
            }
            
            div[data-baseweb="input"] button {
                background-color: #9FD3C4 !important;
            }
            
            /* Remove the black area next to the eye button */
            .stTextInput > div > div {
                background-color: #79BFA0 !important;
            }
            
            /* Ensure the entire input container has the correct background */
            div[data-baseweb="input"] {
                background-color: #79BFA0 !important;
            }

        </style>
    """, unsafe_allow_html=True)
