import streamlit as st
from utils.auth import signup, login, require_logout
from utils.logger import get_logger, is_debug_enabled, log_error

logger = get_logger(__name__)


def signup_page():
    """Signup page"""
    require_logout("Feed")

    if is_debug_enabled():
        logger.debug("Signup page loaded")

    st.header("Sign Up")
    st.write("Create a new account.")

    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up", type="primary"):
        if not email or not username or not password or not confirm_password:
            logger.warning("Signup attempt with missing fields")
            st.error("Please fill in all fields")
        elif password != confirm_password:
            logger.warning(f"Signup attempt with mismatched passwords for {email}")
            st.error("Passwords do not match")
        else:
            try:
                logger.debug(f"Attempting signup for {email}")
                signup_response = signup(email, password)

                if signup_response["success"]:
                    logger.debug(f"Signup successful for {email}, attempting auto-login")
                    # Now log them in
                    login_response = login(email, password)

                    if login_response["success"]:
                        st.session_state.is_logged_in = True
                        st.session_state.username = username
                        logger.info(f"Signup and login successful for {email}")
                        st.success("Account created and logged in!")
                        st.rerun()
                    else:
                        logger.warning(f"Signup successful but login failed for {email}: {login_response['error']}")
                        if login_response['error'] == "Email not confirmed":
                            st.warn("You have received an email with a link to verify the email address. Please verify it and then log in.")
                        else:
                            st.error(f"Signup successful but login failed: {login_response['error']}")
                else:
                    logger.warning(f"Signup failed for {email}: {signup_response['error']}")
                    st.error(f"Signup failed: {signup_response['error']}")
            except Exception as e:
                log_error("SIGNUP_PAGE", f"Signup error for {email}", e)
                st.error(f"An unexpected error occurred: {str(e)}")
