import streamlit as st
import time
import auth
import laporan_nastar

# Tambahkan admin default jika belum ada
auth.add_admin("admin", "password123")

def login_page():
    st.set_page_config(page_title="Dark Login", page_icon="🌑", layout="centered")
    
    # Custom CSS untuk dark theme
    st.markdown("""
        <style>
            /* Background dark */
            .stApp {
                background-color: #1a1a1a;
                min-height: 100vh;
            }
            
            /* Card container */
            .dark-card {
                background: #2d2d2d;
                border-radius: 12px;
                padding: 2.5rem;
                border: 1px solid #3d3d3d;
                box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
                margin: 2rem 0;
            }
            
            /* Input field styling */
            .stTextInput>div>div>input {
                background-color: #333333;
                border: 1px solid #4d4d4d !important;
                color: #ffffff;
                border-radius: 8px;
                padding: 12px;
                transition: all 0.3s ease;
            }
            
            .stTextInput>div>div>input:focus {
                border-color: #4a90e2 !important;
                box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
            }
            
            /* Label text styling */
            .stTextInput label, .stPassword label {
                color: #cccccc !important;
                font-weight: 500;
            }
            
            /* Button styling */
            .stButton>button {
                width: 100%;
                background: #4a90e2;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-weight: 600;
                transition: all 0.2s ease;
                margin-top: 1.5rem;
            }
            
            .stButton>button:hover {
                background: #357abd;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }
            
            /* Title styling */
            .dark-title {
                text-align: center;
                color: #ffffff;
                margin-bottom: 2rem;
                font-size: 1.8rem;
                font-weight: 700;
            }
            
            /* Error message styling */
            .dark-error {
                background: #4a1f1f;
                color: #ff6b6b;
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid #5f2a2a;
                margin-top: 1.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            /* Footer styling */
            .dark-footer {
                text-align: center;
                color: #666666;
                margin-top: 2rem;
                font-size: 0.9rem;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown(
                """
                <div class="dark-card">
                    <div class="dark-title">
                        🔒 Secure Access
                    </div>
                """, 
                unsafe_allow_html=True
            )
            
            with st.form("login_form", clear_on_submit=True):
                username = st.text_input(
                    "Username",
                    placeholder="Enter admin username",
                    key="dark_username"
                )
                
                password = st.text_input(
                    "Password", 
                    placeholder="••••••••",
                    type="password",
                    key="dark_password"
                )
                
                login_button = st.form_submit_button("Authenticate")
                
                if login_button:
                    with st.spinner("Verifying credentials..."):
                        time.sleep(0.5)
                        if auth.login(username, password):
                            st.session_state["logged_in"] = True
                            st.success("Access granted! Redirecting...")
                            time.sleep(0.8)
                            st.rerun()
                        else:
                            st.markdown(
                                """<div class="dark-error">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">
                                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                                    </svg>
                                    Invalid credentials
                                </div>""", 
                                unsafe_allow_html=True
                            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Footer
            st.markdown(
                """
                <div class="dark-footer">
                    © 2024 Secure System | v2.0.1
                </div>
                """, 
                unsafe_allow_html=True
            )

# Cek status login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    laporan_nastar.main()
else:
    login_page()