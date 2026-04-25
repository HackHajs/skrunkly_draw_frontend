import streamlit as st
from utils.logger import get_logger, is_debug_enabled

logger = get_logger(__name__)


def feed_page():
    """Feed page - social feed display"""
    if is_debug_enabled():
        logger.debug("Feed page loaded - user viewing feed")
    
    logger.info("User accessing feed page")

    st.header("Skrunklies Feed")

    st.info("Featured Post 1")
    st.write("Check out this amazing post!")
    
    st.info("Featured Post 2")
    st.write("Another creative piece by the skrunk")
    
    st.info("Featured Post 3")
    st.write("Discover more great skrunksl")
