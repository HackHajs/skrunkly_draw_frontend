import streamlit as st

from utils.logger import get_logger

logger = get_logger(__name__)

_REPLY_CACHE_PREFIXES = ("replies_cache", "reply_cache")


def invalidate_app_caches(source: str = "unknown") -> int:
    """Invalidate Streamlit caches used by feed/profile/reply views."""
    st.cache_data.clear()

    cleared_reply_cache_keys = 0
    for key in list(st.session_state.keys()):
        if key.startswith(_REPLY_CACHE_PREFIXES):
            del st.session_state[key]
            cleared_reply_cache_keys += 1

    logger.info(
        f"App cache invalidated from {source}; cleared {cleared_reply_cache_keys} reply cache key(s)"
    )
    return cleared_reply_cache_keys
