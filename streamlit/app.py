import streamlit as st

from auth_callback import handle_callback
from auth_config import get_cached_config
from auth_helpers import (
    build_authorize_url,
    generate_nonce,
    generate_pkce_challenge,
    generate_state,
)

st.set_page_config(
    page_title="Skrunkly Draw",
    page_icon="✏️",
)


def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "id_token" not in st.session_state:
        st.session_state.id_token = None
    if "email" not in st.session_state:
        st.session_state.email = None


def handle_login_click():
    try:
        config = get_cached_config()
        pkce = generate_pkce_challenge()
        state = generate_state()
        nonce = generate_nonce()

        # Store in session for callback validation
        st.session_state.auth_code_verifier = pkce.code_verifier
        st.session_state.auth_state = state
        st.session_state.auth_nonce = nonce

        authorize_url = build_authorize_url(
            config, state, nonce, pkce.code_challenge
        )

        # Provide clickable link to Auth0
        st.session_state.login_url = authorize_url
    except Exception as e:
        st.error(f"Failed to initiate login: {str(e)}")


def handle_logout():
    st.session_state.authenticated = False
    st.session_state.id_token = None
    st.session_state.email = None
    st.query_params.clear()
    st.rerun()


init_session_state()

# Handle callback from Auth0
callback_result = handle_callback()
if callback_result:
    st.session_state.authenticated = True
    st.session_state.id_token = callback_result["id_token"]
    st.session_state.email = callback_result["email"]
    # Clear query params after successful auth
    st.query_params.clear()

# Header with auth status
col1, col2 = st.columns([3, 1])
with col1:
    st.write("# Welcome to Skrunkly Draw!")
with col2:
    if st.session_state.authenticated:
        st.write(f"**{st.session_state.email}**")
    else:
        st.write("Not logged in")

# Auth buttons in sidebar
with st.sidebar:
    st.write("## Authentication")
    if st.session_state.authenticated:
        st.success(f"Logged in as: {st.session_state.email}")
        if st.button("Logout"):
            handle_logout()
    else:
        if st.button("Login with Auth0"):
            handle_login_click()
        if "login_url" in st.session_state and st.session_state.login_url:
            st.link_button(
                "Click here to complete login",
                st.session_state.login_url,
            )

if st.session_state.authenticated:
    st.info(f"Welcome {st.session_state.email}! You are successfully authenticated.")
else:
    st.write("Click the **Login with Auth0** button in the sidebar to get started.")
