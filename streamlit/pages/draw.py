import streamlit as st
from utils.auth import require_login
from utils.logger import get_logger, is_debug_enabled

import requests as rq

from canvas import canvas 

logger = get_logger(__name__)


def draw_page():
    """Draw page - interactive drawing canvas"""
    require_login("Feed")

    if is_debug_enabled():
        logger.debug("Draw page loaded - user accessing drawing canvas")
    
    logger.info("User accessing draw page")


    scn = {
        "palette": ["#FF0000", "#9F9F00", "#00FF00", "#009F9F", "#0000FF", "#9F009F", "#7F7F7F", "#CFCFCF"],
        "strokes": []
    }

    if "id" in st.query_params:
        from pages.feed import get_post
        p = get_post(st.query_params.id)
        if p:
            scn = p["skrunkle"]


    result = canvas(data={"isEditor": True, "scn": scn})

    if result:
        make_post(result, st.query_params.id if "id" in st.query_params else None)

def make_post(scn, id):
    url = st.secrets.get("API_HOST", "http://localhost:8000")
    token = st.session_state.get("access_token", "")
    
    data = {"mature": False, "skrunkle": scn["commit"]}
    if id:
        data["reply"] = {"parent": id, "on_feed": False}
    try:
        response = rq.post(
            f"{url}/v0/post",
            json=data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        )
        if response.status_code in (200, 201):
            st.toast("Drawing published successfully!")
        else:
            st.error(f"Failed to publish. API returned status code {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Failed to publish post: {str(e)}")
        st.error(f"Failed to publish drawing: {e}")
