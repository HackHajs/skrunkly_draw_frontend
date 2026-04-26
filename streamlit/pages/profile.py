import streamlit as st
from utils.auth import require_login
from utils.logger import get_logger, is_debug_enabled

import requests as rq

logger = get_logger(__name__)


@st.cache_data(ttl=600) #10 minutes
def get_user(uuid):
    url = st.secrets.get("API_HOST", "http://localhost:8000")
    try:
        response = rq.get(f"{url}/v0/user?id={uuid}")
        if response.status_code in (200, 201):
            return response.json()
        else:
            return None
    except Exception as e:
        logger.error(f"Failed to fetch user: {str(e)}")
        st.error(f"Failed to fetch user: {e}")


def profile_page():
    """Profile page - user profile display and editing"""
    require_login("Feed")

    if is_debug_enabled():
        logger.debug("Profile page loaded - user viewing profile")
    
    logger.info("User accessing profile page")

    st.header("My Profile")

    user = st.session_state.get("user")

    email = "Not available"
    portfolio = ""

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

    user_2 = get_user(user.id)
    if user_2 != None:
        username = user_2["name"]
        portfolio = user_2["link"]


    st.write(f"**Email:** {email}")

    new_name = st.text_input("**Username:**", placeholder=username)
    new_porto = st.text_input("**Portfolio:**", placeholder=portfolio)


    st.button("Update Profile", key="upd_profile", on_click=lambda:upd_profile(new_name if new_name else username, new_porto))

    st.divider()

def upd_profile(new_name, new_porto):
    data = {"name": new_name }
    if new_porto: data["link"] = new_porto

    url = st.secrets.get("API_HOST", "http://localhost:8000")
    token = st.session_state.get("access_token", "")

    try:
        response = rq.put(f"{url}/v0/user", json=data, 
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        )

        if response.status_code in (200, 201):
            st.toast("Successfully updated profile!")
        else:
            st.error(f"Failed to update. API returned status code {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Failed to update profile: {str(e)}")
        st.error(f"Failed to update profile: {e}")