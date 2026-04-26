import streamlit as st
from utils.logger import get_logger, is_debug_enabled

from pages.draw import draw_page
from pages.profile import get_user
from canvas import canvas

import requests as rq

logger = get_logger(__name__)
draw_pg = st.Page(draw_page, title="Draw")

st.cache_data.clear()

def feed_page():
    """Feed page - social feed display"""
    if is_debug_enabled():
        logger.debug("Feed page loaded - user viewing feed")
    
    logger.info("User accessing feed page")

    st.header("Skrunklies Feed")
    st.divider()
    if "id" in st.query_params:
        posts = get_thread(st.query_params.id)        
    else:
        posts = get_posts()
    
    for id in range(len(posts)):
        post(posts[id], not "id" in st.query_params)

    if "id" in st.query_params:
        if st.button("Add Reply"):
            st.switch_page(draw_pg, query_params={"id": st.query_params.id})

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


@st.cache_data(ttl=60) #time in seconds
def get_thread(id): 
    url = st.secrets.get("API_HOST", "http://localhost:8000")

    main = get_post(id)

    try:
        response = rq.get(f"{url}/v0/post/replies?id={id}")
        if response.status_code in (200, 201):
            return [main] + response.json()
        else:
            st.error(f"Failed to fetch feed. API returned status code {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Failed to fetch feed: {str(e)}")
        st.error(f"Failed to fetch feed: {e}")
    return []

@st.cache_data(ttl=600) #time in seconds
def get_post(id):
    url = st.secrets.get("API_HOST", "http://localhost:8000")
    try:
        response = rq.get(f"{url}/v0/post?id={id}",
                    headers={"Content-Type": "application/json"},
                    json={"id": id})
        if response.status_code in (200, 201):
            return response.json()
        else:
            st.error(f"Failed to fetch feed. API returned status code {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Failed to fetch feed: {str(e)}")
        st.error(f"Failed to fetch feed: {e}")
    return None


def post(post, show_replies):
    canvas(data={"isEditor": False, "scn": post["skrunkle"]}, key=f"canvas{post["_id"]}")
    u = get_user(post["user"])
    st.write(f"by {u['name'] if u else 'anon'}")
    if show_replies:
        st.button("replies", on_click=lambda: set_query(post["_id"]), key=f"button{post["_id"]}")
    st.divider()

def set_query(id):
    st.query_params["id"] = id
