import streamlit as st
from utils.auth import require_login
from utils.cache import invalidate_app_caches
from utils.gif_export import GifExportError, export_scene_to_gif
from utils.logger import get_logger, is_debug_enabled

import hashlib
import json
import requests as rq
from datetime import datetime, timezone

from canvas import canvas 

logger = get_logger(__name__)
GIF_EXPORT_STATE_KEY = "drawing_gif_export"


def _build_publish_key(commit, parent_id):
    payload = json.dumps(commit, sort_keys=True, separators=(",", ":"))
    payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"{parent_id or 'root'}:{payload_hash}"


def draw_page():
    """Draw page - interactive drawing canvas"""
    require_login("Feed")
    st.session_state.setdefault("published_post_keys", set())
    st.session_state.setdefault("publishing_post_keys", set())
    st.session_state.setdefault(GIF_EXPORT_STATE_KEY, None)

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


    result = canvas(data={"isEditor": True, "scn": scn}, key="draw_canvas")

    if result and "commit" in result:
        make_post(result, st.query_params.id if "id" in st.query_params else None)
    if result and "export" in result:
        prepare_gif_export(result["export"])

    gif_export = st.session_state.get(GIF_EXPORT_STATE_KEY)
    if gif_export:
        st.download_button(
            "Download GIF",
            data=gif_export["bytes"],
            file_name=gif_export["file_name"],
            mime="image/gif",
            use_container_width=True,
            key="download-drawing-gif",
        )


def prepare_gif_export(scene):
    try:
        gif_bytes = export_scene_to_gif(scene)
    except GifExportError as export_error:
        st.session_state[GIF_EXPORT_STATE_KEY] = None
        st.warning(str(export_error))
        return
    except Exception as export_error:
        st.session_state[GIF_EXPORT_STATE_KEY] = None
        logger.error(f"Failed to export GIF: {str(export_error)}")
        st.error("Failed to export GIF. Please try again.")
        return

    file_name = f"skrunkly-drawing-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.gif"
    st.session_state[GIF_EXPORT_STATE_KEY] = {"bytes": gif_bytes, "file_name": file_name}
    st.success("GIF export is ready.")

def make_post(scn, id):
    publish_key = _build_publish_key(scn["commit"], id)
    published_post_keys = st.session_state.setdefault("published_post_keys", set())
    publishing_post_keys = st.session_state.setdefault("publishing_post_keys", set())

    if publish_key in published_post_keys or publish_key in publishing_post_keys:
        if is_debug_enabled():
            logger.debug("Duplicate publish prevented for current drawing")
        return

    publishing_post_keys.add(publish_key)

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
            published_post_keys.add(publish_key)
            publishing_post_keys.discard(publish_key)
            invalidate_app_caches(source="publish_success")
            st.toast("Drawing published successfully!")
            from pages.feed import feed_page
            feed_pg = st.Page(feed_page, title="Feed")
            st.switch_page(feed_pg, query_params={})
        else:
            publishing_post_keys.discard(publish_key)
            st.error(f"Failed to publish. API returned status code {response.status_code}: {response.text}")
    except Exception as e:
        publishing_post_keys.discard(publish_key)
        logger.error(f"Failed to publish post: {str(e)}")
        st.error(f"Failed to publish drawing: {e}")
