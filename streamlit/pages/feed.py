import streamlit as st
from utils.logger import get_logger, is_debug_enabled

logger = get_logger(__name__)


def feed_page():
    """Feed page - social feed display"""
    if is_debug_enabled():
        logger.debug("Feed page loaded - user viewing feed")
    
    logger.info("User accessing feed page")

    st.header("Skrunklies Feed")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Featured Post 1")
        st.write("Check out this amazing post!")
    with col2:
        st.info("Featured Post 2")
        st.write("Another creative piece by the skrunk")
    with col3:
        st.info("Featured Post 3")
        st.write("Discover more great skrunksl")
