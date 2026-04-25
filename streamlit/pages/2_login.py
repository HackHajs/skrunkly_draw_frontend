import streamlit as st
from utils.auth import login

st.header("Log In")

email = st.text_input("Email", placeholder="your@email.com")
password = st.text_input("Password", type="password")

if st.button("Log In", type="primary"):
    if not email or not password:
        st.error("Please enter both email and password")
    else:
        with st.spinner("Logging in..."):
            try:
                response = login(email, password)
                
                if response["success"]:
                    st.session_state.is_logged_in = True
                    st.session_state.user = response["user"]
                    st.success(f"Welcome back, {email}!")
                    st.rerun()
                else:
                    st.error(f"Login failed: {response['error']}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
