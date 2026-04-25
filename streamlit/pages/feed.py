import streamlit as st
from utils.logger import get_logger, is_debug_enabled

from canvas import canvas

import requests as rq

logger = get_logger(__name__)


def feed_page():
    """Feed page - social feed display"""
    if is_debug_enabled():
        logger.debug("Feed page loaded - user viewing feed")
    
    logger.info("User accessing feed page")

    st.header("Skrunklies Feed")

    posts = get_posts()
    st.divider()
    for id in range(len(posts)):
        canvas(data={"isEditor": False, "scn": posts[id]["skrunkle"]}, key=f"canvas{id}")
        st.write(f"by {posts[id]['user']}")
        st.divider()


@st.cache_data(ttl=60) #time in seconds
def get_posts(): 
    url = st.secrets.get("API_HOST", "http://localhost:8000")
    try:
        response = rq.get(f"{url}/v0/post/all")
        if response.status_code in (200, 201):
            return response.json()
        else:
            st.error(f"Failed to fetch feed. API returned status code {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Failed to fetch feed: {str(e)}")
        st.error(f"Failed to fetch feed: {e}")
