import streamlit as st
from utils.auth import require_login
from utils.logger import get_logger, is_debug_enabled

logger = get_logger(__name__)


def profile_page():
    """Profile page - user profile display and editing"""
    require_login("Feed")

    if is_debug_enabled():
        logger.debug("Profile page loaded - user viewing profile")
    
    logger.info("User accessing profile page")

    st.header("My Profile")

    user = st.session_state.get("user")
    email = "Not available"

    if user:
        if hasattr(user, 'email'):
            email = user.email
            username = email.split('@')[0]
        elif isinstance(user, dict) and 'email' in user:
            email = user['email']
            username = email.split('@')[0]
        else:
            username = "User"
            
        if hasattr(user, 'user_metadata') and user.user_metadata and 'username' in user.user_metadata:
            username = user.user_metadata['username']
        elif isinstance(user, dict) and 'user_metadata' in user and user['user_metadata'] and 'username' in user['user_metadata']:
            username = user['user_metadata']['username']
        logger.debug(f"User profile accessed: {email}")
    else:
        username = "Guest"

    st.write(f"**Email:** {email}")
    st.write(f"**Username:** {username}")

    st.divider()
    st.subheader("Profile Information")
    st.write("Edit your profile information here (coming soon)")
