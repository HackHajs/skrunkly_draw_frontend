"""
Supabase client module for authentication and database operations.
Provides helper functions to interact with Supabase authentication and database.
"""

import streamlit as st
from supabase import create_client, Client


def get_supabase_client() -> Client:
    """
    Initialize and return a Supabase client instance.
    Retrieves credentials from Streamlit secrets (SUPABASE_URL and SUPABASE_ANON_KEY).
    
    Returns:
        Client: Authenticated Supabase client
        
    Raises:
        KeyError: If SUPABASE_URL or SUPABASE_ANON_KEY are not found in st.secrets
    """
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(supabase_url, supabase_key)


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
    client = get_supabase_client()
    response = client.auth.sign_up({"email": email, "password": password})
    return response


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
    client = get_supabase_client()
    response = client.auth.sign_in_with_password({"email": email, "password": password})
    return response


def logout() -> None:
    """
    Log out the current user by clearing the session.
    Clears auth token from Streamlit session state.
    """
    client = get_supabase_client()
    client.auth.sign_out()


def get_current_user() -> dict | None:
    """
    Get the currently authenticated user's information.
    
    Returns:
        dict: User information if authenticated, None otherwise
    """
    client = get_supabase_client()
    try:
        user = client.auth.get_user()
        return user
    except Exception:
        return None
