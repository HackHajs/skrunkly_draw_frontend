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


def signup(email: str, password: str) -> dict:
    """
    Sign up a new user with email and password.
    
    Args:
        email: User's email address
        password: User's password
        
    Returns:
        dict with keys:
            - success (bool): Whether signup was successful
            - user (dict or None): User information if successful
            - error (str or None): Error message if failed
    """
    try:
        response = signup_with_email(email, password)
        user = response.user if hasattr(response, "user") else response.get("user")
        
        return {
            "success": True,
            "user": user,
            "error": None,
        }
    except Exception as e:
        error_message = str(e)
        return {
            "success": False,
            "user": None,
            "error": error_message,
        }


def login(email: str, password: str) -> dict:
    """
    Log in a user with email and password.
    
    Args:
        email: User's email address
        password: User's password
        
    Returns:
        dict with keys:
            - success (bool): Whether login was successful
            - user (dict or None): User information if successful
            - error (str or None): Error message if failed
            - session (dict or None): Session data with access token
    """
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
        
        return {
            "success": True,
            "user": user,
            "error": None,
            "session": session,
        }
    except Exception as e:
        error_message = str(e)
        return {
            "success": False,
            "user": None,
            "error": error_message,
            "session": None,
        }


def logout() -> None:
    """
    Log out the current user and clear session state.
    Clears stored session tokens and user information.
    """
    try:
        supabase_logout()
    except Exception:
        pass
    
    if "access_token" in st.session_state:
        del st.session_state.access_token
    if "user" in st.session_state:
        del st.session_state.user


def get_user() -> dict | None:
    """
    Get the currently authenticated user's information.
    
    Returns:
        dict: User information if authenticated, None otherwise
    """
    try:
        user = get_current_user()
        return user
    except Exception:
        return None


def verify_session() -> bool:
    """
    Check if a valid session exists.
    Checks both st.session_state and by querying the current user.
    
    Returns:
        bool: True if user is authenticated, False otherwise
    """
    if "access_token" in st.session_state and st.session_state.access_token:
        return True
    
    try:
        user = get_current_user()
        return user is not None
    except Exception:
        return False
