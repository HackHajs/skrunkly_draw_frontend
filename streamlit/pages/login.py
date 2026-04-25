import streamlit as st
from utils.auth import login, require_logout
from utils.logger import get_logger, is_debug_enabled, log_error

logger = get_logger(__name__)


def login_page():
    """Login page"""
    require_logout("Feed")

    if is_debug_enabled():
        logger.debug("Login page loaded")

    st.header("Log In")

    email = st.text_input("Email", placeholder="your@email.com")
    password = st.text_input("Password", type="password")

    if st.button("Log In", type="primary"):
        if not email or not password:
            logger.warning("Login attempt with missing credentials")
            st.error("Please enter both email and password")
        else:
            with st.spinner("Logging in..."):
                try:
                    logger.debug(f"Attempting login for {email}")
                    response = login(email, password)

                    if response["success"]:
                        st.session_state.is_logged_in = True
                        st.session_state.user = response["user"]
                        logger.info(f"Login successful for {email}")
                        st.success(f"Welcome back, {email}!")
                        st.rerun()
                    else:
                        logger.warning(f"Login failed for {email}: {response['error']}")
                        st.error(f"Login failed: {response['error']}")
                except Exception as e:
                    log_error("LOGIN_PAGE", f"Login error for {email}", e)
                    st.error(f"Connection error: {str(e)}")
