import streamlit as st
from utils.auth import require_login
from supabase_client import update_user_metadata
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
    
    with st.expander("Change Username", expanded=True):
        new_username = st.text_input("New Username", placeholder="Enter your new username")
        if st.button("Update Username"):
            if new_username:
                try:
                    with st.spinner("Updating..."):
                        response = update_user_metadata({"username": new_username})
                        
                        # Update session state with the fresh user object
                        if hasattr(response, "user") and response.user:
                            st.session_state.user = response.user
                        elif isinstance(response, dict) and response.get("user"):
                            st.session_state.user = response["user"]
                        else:
                            # Fallback if no fresh object returned, attempt manual override but log it
                            logger.warning("No user returned from update, falling back to manual assignment")
                            if hasattr(st.session_state.user, "user_metadata"):
                                if st.session_state.user.user_metadata is None:
                                    st.session_state.user.user_metadata = {}
                                st.session_state.user.user_metadata["username"] = new_username
                            elif isinstance(st.session_state.user, dict):
                                if "user_metadata" not in st.session_state.user or st.session_state.user["user_metadata"] is None:
                                    st.session_state.user["user_metadata"] = {}
                                st.session_state.user["user_metadata"]["username"] = new_username
                            
                        st.success("Username updated successfully!")
                except Exception as e:
                    st.error(f"Failed to update username: {str(e)}")
            else:
                st.warning("Please enter a valid username.")

    st.write("Change your other account settings here (coming soon)")

    st.divider()
    st.subheader("Privacy Settings")
    st.write("Manage your privacy preferences (coming soon)")

    st.divider()
    st.subheader("Notification Settings")
    st.write("Configure notification preferences (coming soon)")
