import streamlit as st
from utils.logger import get_logger, is_debug_enabled

logger = get_logger(__name__)


def discover_page():
    """Discover page - public content discovery"""
    if is_debug_enabled():
        logger.debug("Discover page loaded - user browsing discovery")
    
    logger.info("User accessing discover page")

    st.header("Discover")
    st.write("Explore content.")
