"""
Supabase client module for authentication and database operations.
Provides helper functions to interact with Supabase authentication and database.
"""

import streamlit as st
from supabase import create_client, Client
from utils.logger import get_logger, log_error, log_auth_event

logger = get_logger(__name__)


def get_supabase_client() -> Client:
    """
    Initialize and return a Supabase client instance.
    Retrieves credentials from Streamlit secrets (SUPABASE_URL and SUPABASE_ANON_KEY).
    
    Returns:
        Client: Authenticated Supabase client
        
    Raises:
        KeyError: If SUPABASE_URL or SUPABASE_ANON_KEY are not found in st.secrets
    """
    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_ANON_KEY"]
        client = create_client(supabase_url, supabase_key)
        logger.debug("Supabase client initialized successfully")
        return client
    except KeyError as e:
        logger.error(f"Missing Supabase secret: {str(e)}")
        raise
    except Exception as e:
        log_error("SUPABASE", "Failed to initialize Supabase client", e)
        raise


def signup_with_email(email: str, password: str) -> dict:
    """
    Sign up a new user with email and password.
    
    Args:
        email: User's email address
        password: User's password
        
    Returns:
        dict: Response containing user information and session data
        
    Raises:
        Exception: If signup fails (invalid email, weak password, email already exists, etc.)
    """
    try:
        logger.debug(f"Attempting signup for email: {email}")
        client = get_supabase_client()
        response = client.auth.sign_up({"email": email, "password": password})
        logger.info(f"Signup successful for email: {email}")
        return response
    except Exception as e:
        log_error("SUPABASE_SIGNUP", f"Signup failed for {email}", e)
        raise


def login_with_email(email: str, password: str) -> dict:
    """
    Log in a user with email and password.
    
    Args:
        email: User's email address
        password: User's password
        
    Returns:
        dict: Response containing user information and session data
        
    Raises:
        Exception: If login fails (invalid credentials, user not found, etc.)
    """
    try:
        logger.debug(f"Attempting login for email: {email}")
        client = get_supabase_client()
        response = client.auth.sign_in_with_password({"email": email, "password": password})
        logger.info(f"Login successful for email: {email}")
        return response
    except Exception as e:
        log_error("SUPABASE_LOGIN", f"Login failed for {email}", e)
        raise


def logout() -> None:
    """
    Log out the current user by clearing the session.
    Clears auth token from Streamlit session state.
    """
    try:
        logger.debug("Attempting logout from Supabase")
        client = get_supabase_client()
        client.auth.sign_out()
        logger.info("Logout successful")
    except Exception as e:
        log_error("SUPABASE_LOGOUT", "Logout failed", e)


def update_user_metadata(metadata: dict):
    """
    Update the authenticated user's metadata (e.g. username).
    """
    try:
        logger.debug("Attempting to update user metadata")
        client = get_supabase_client()
        response = client.auth.update_user({"data": metadata})
        logger.info("User metadata updated successfully")
        return response
    except Exception as e:
        log_error("SUPABASE_UPDATE", "Failed to update user metadata", e)
        raise


def get_current_user() -> dict | None:
    """
    Get the currently authenticated user's information.
    
    Returns:
        dict: User information if authenticated, None otherwise
    """
    try:
        logger.debug("Fetching current user from Supabase")
        client = get_supabase_client()
        user = client.auth.get_user()
        if user:
            logger.debug(f"Current user retrieved: {user.id if hasattr(user, 'id') else 'unknown'}")
        else:
            logger.debug("No authenticated user found")
        return user
    except Exception as e:
        logger.debug(f"Failed to get current user: {str(e)}")
        return None
