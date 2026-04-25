import streamlit as st
from utils.auth import require_login
from utils.logger import get_logger, is_debug_enabled

from canvas import canvas 

logger = get_logger(__name__)


def draw_page():
    """Draw page - interactive drawing canvas"""
    require_login("Feed")

    if is_debug_enabled():
        logger.debug("Draw page loaded - user accessing drawing canvas")

    st.header("Draw")
    
    logger.info("User accessing draw page")


    canvas(data={"isEditor": True, "scn": 
    {
        "palette": ["#FF0000", "#9F9F00", "#00FF00", "#009F9F", "#0000FF", "#9F009F", "#7F7F7F", "#CFCFCF"],
        "strokes": []
    }},
        on_commit_change = lambda:print("beep") #TODO
    )
