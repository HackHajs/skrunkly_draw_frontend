import streamlit as st
from utils.auth import signup, login

st.header("Sign Up")
st.write("Create a new account.")

email = st.text_input("Email")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Sign Up", type="primary"):
    if not email or not username or not password or not confirm_password:
        st.error("Please fill in all fields")
    elif password != confirm_password:
        st.error("Passwords do not match")
    else:
        signup_response = signup(email, password)
        
        if signup_response["success"]:
            # Now log them in
            login_response = login(email, password)
            
            if login_response["success"]:
                st.session_state.is_logged_in = True
                st.session_state.username = username
                st.success("Account created and logged in!")
                st.rerun()
            else:
                st.error(f"Signup successful but login failed: {login_response['error']}")
        else:
            st.error(f"Signup failed: {signup_response['error']}")
