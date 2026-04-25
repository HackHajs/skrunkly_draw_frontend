import streamlit as st
from utils.auth import require_login
from utils.logger import get_logger, is_debug_enabled

logger = get_logger(__name__)


def settings_page():
    """Settings page - user settings and preferences"""
    require_login("Feed")

    if is_debug_enabled():
        logger.debug("Settings page loaded - user viewing settings")
    
    logger.info("User accessing settings page")

    st.header("Settings")

    st.divider()
    st.subheader("Account Settings")
    st.write("Change your account settings here (coming soon)")

    st.divider()
    st.subheader("Privacy Settings")
    st.write("Manage your privacy preferences (coming soon)")

    st.divider()
    st.subheader("Notification Settings")
    st.write("Configure notification preferences (coming soon)")
