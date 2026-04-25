"""
Authentication helper module for Supabase.
"""

import streamlit as st
from supabase_client import (
    signup_with_email,
    login_with_email,
    logout as supabase_logout,
    get_current_user,
)
from .logger import get_logger, log_auth_event, log_session_change, log_redirect

logger = get_logger(__name__)


def signup(email: str, password: str) -> dict:
    log_auth_event("Signup attempt", email)
    try:
        response = signup_with_email(email, password)
        user = response.user if hasattr(response, "user") else response.get("user")
        log_auth_event("Signup successful", email, "success")
        
        return {
            "success": True,
            "user": user,
            "error": None,
        }
    except Exception as e:
        error_message = str(e)
        log_auth_event("Signup failed", email, "error")
        return {
            "success": False,
            "user": None,
            "error": error_message,
        }


def login(email: str, password: str) -> dict:
    log_auth_event("Login attempt", email)
    try:
        response = login_with_email(email, password)
        user = response.user if hasattr(response, "user") else response.get("user")
        session = response.session if hasattr(response, "session") else response.get("session")
        
        if session and hasattr(session, "access_token"):
            access_token = session.access_token
        elif isinstance(session, dict):
            access_token = session.get("access_token")
        else:
            access_token = None
        
        st.session_state.access_token = access_token
        st.session_state.user = user
        log_session_change("access_token", "***token***")
        log_session_change("user", email)
        log_auth_event("Login successful", email, "success")
        
        return {
            "success": True,
            "user": user,
            "error": None,
            "session": session,
        }
    except Exception as e:
        error_message = str(e)
        log_auth_event("Login failed", email, "error")
        return {
            "success": False,
            "user": None,
            "error": error_message,
            "session": None,
        }


def logout() -> None:
    user_email = None
    if "user" in st.session_state and st.session_state.user:
        user = st.session_state.user
        if hasattr(user, 'email'):
            user_email = user.email
        elif isinstance(user, dict):
            user_email = user.get('email')
    
    log_auth_event("Logout initiated", user_email)
    try:
        supabase_logout()
    except Exception:
        pass
    
    if "access_token" in st.session_state:
        del st.session_state.access_token
    if "user" in st.session_state:
        del st.session_state.user
    
    log_auth_event("Logout completed", user_email, "success")


def get_user() -> dict | None:
    try:
        logger.debug("Attempting to retrieve current user from Supabase")
        user = get_current_user()
        if user:
            logger.debug("User retrieved successfully")
        else:
            logger.debug("No user found")
        return user
    except Exception as e:
        logger.debug(f"Error retrieving user: {str(e)}")
        return None


def verify_session() -> bool:
    logger.debug("Verifying session state")
    if "access_token" in st.session_state and st.session_state.access_token:
        logger.debug("Session verified via access_token")
        return True
    
    try:
        user = get_current_user()
        if user:
            logger.debug("Session verified via Supabase")
            return True
        else:
            logger.debug("Session verification failed - no user found")
            return False
    except Exception as e:
        logger.debug(f"Session verification error: {str(e)}")
        return False


def require_login(redirect_page: str = "Feed") -> bool:
    logger.debug(f"Checking login requirement (redirect_page: {redirect_page})")
    if st.session_state.get("is_logged_in"):
        logger.debug("User already logged in, access granted")
        st.switch_page("pages/1_feed.py")
        return False
    else:
        logger.debug("User not logged in, access denied - redirecting to Feed")
        return True


def require_logout(redirect_page: str = "Feed") -> bool:
    logger.debug(f"Checking logout requirement (redirect_page: {redirect_page})")
    if not st.session_state.get("is_logged_in"):
        logger.debug("User not logged in, access granted to auth page")
        st.switch_page("pages/1_feed.py")
        return False
    else:
        logger.debug("User already logged in, redirecting from auth page to Feed")
    return True
