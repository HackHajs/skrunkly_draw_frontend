import streamlit as st
from utils.auth import verify_session, get_user
from utils.logger import get_logger, is_debug_enabled, log_event
from pages.feed import feed_page
from pages.login import login_page
from pages.signup import signup_page
from pages.discover import discover_page
from pages.draw import draw_page
from pages.profile import profile_page
from pages.settings import settings_page

logger = get_logger(__name__)

feed_pg = st.Page(feed_page, title="Feed")
login_pg = st.Page(login_page, title="Log In")
signup_pg = st.Page(signup_page, title="Sign Up")
discover_pg = st.Page(discover_page, title="Discover")
draw_pg = st.Page(draw_page, title="Draw")
profile_pg = st.Page(profile_page, title="Profile")
settings_pg = st.Page(settings_page, title="Settings")


st.set_page_config(
    page_title="Skrunkly Draw",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        div[data-baseweb="select"] > div {
            background-color: transparent !important;
            border-color: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
    if is_debug_enabled():
        logger.debug("Session initialized: is_logged_in = False")
if "user" not in st.session_state:
    st.session_state.user = None
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_menu_selection" not in st.session_state:
    st.session_state.user_menu_selection = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "feed"


def restore_session():
    """Restore user session on page load if tokens exist"""
    logger.debug("restore_session() called")
    if st.session_state.get("access_token") and not st.session_state.get("is_logged_in"):
        logger.debug("Access token found but is_logged_in is False, attempting to restore session")
        # User has a token but session state says not logged in - restore
        user = get_user()
        if user:
            st.session_state.is_logged_in = True
            st.session_state.user = user
            logger.info("Session restored successfully from access_token")
        else:
            logger.warning("Access token present but user not found - clearing token")
            st.session_state.access_token = None
    else:
        logger.debug(f"Session state: access_token={bool(st.session_state.get('access_token'))}, is_logged_in={st.session_state.get('is_logged_in')}")


def logout():
    logger.debug("logout() initiated by user")
    user_email = None
    if st.session_state.user:
        if hasattr(st.session_state.user, 'email'):
            user_email = st.session_state.user.email
        elif isinstance(st.session_state.user, dict) and 'email' in st.session_state.user:
            user_email = st.session_state.user['email']
    
    st.session_state.is_logged_in = False
    st.session_state.user = None
    st.session_state.access_token = None
    st.session_state.user_menu_selection = None
    logger.info(f"User logged out: {user_email if user_email else 'unknown'}")
    st.rerun()


def get_user_display_name() -> str:
    """Extract user display name from user object metadata or email"""
    if st.session_state.user:
        user = st.session_state.user
        
        # Check metadata for custom username first
        if hasattr(user, 'user_metadata'):
            metadata = user.user_metadata
            if metadata and 'username' in metadata:
                return metadata['username']
        elif isinstance(user, dict) and 'user_metadata' in user:
            metadata = user['user_metadata']
            if metadata and 'username' in metadata:
                return metadata['username']

        # Try to get email first, then fall back
        if hasattr(user, 'email'):
            return user.email.split('@')[0]
        elif isinstance(user, dict) and 'email' in user:
            return user['email'].split('@')[0]
    return "User"


def render_user_menu():
    """Render user profile dropdown menu"""
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="large")

    with col1:
        if st.session_state.is_logged_in:
            if st.button("Draw", use_container_width=True):
                if is_debug_enabled():
                    log_event("User navigated", page="draw", logged_in=st.session_state.is_logged_in)
                st.switch_page(draw_pg)
    with col2:
        st.write("**Button 1**")
    with col3:
        st.write("**Button 2**")
    with col4:
        if st.session_state.is_logged_in:
            username = get_user_display_name()
            menu_options = [f"{username}", "Profile", "Settings", "Logout"]
            
            selected = st.selectbox(
                label="User Menu",
                options=menu_options,
                key="user_menu",
                label_visibility="collapsed",
            )
            if selected == f"{username}":
                print("Yippe")
            elif selected == "Profile":
                if is_debug_enabled():
                    log_event("User navigated", page="profile", logged_in=True)
                st.switch_page(profile_pg)
            elif selected == "Settings":
                if is_debug_enabled():
                    log_event("User navigated", page="settings", logged_in=True)
                st.switch_page(settings_pg)
            elif selected == "Logout":
                if is_debug_enabled():
                    log_event("User logout", page="logout", logged_in=True)
                logout()
        else:
            login_col, signup_col = st.columns(2)
            with login_col:
                if st.button("Log In", use_container_width=True):
                    if is_debug_enabled():
                        log_event("User navigated", page="login", logged_in=False)
                    st.switch_page(login_pg)
            with signup_col:
                if st.button("Sign Up", use_container_width=True):
                    if is_debug_enabled():
                        log_event("User navigated", page="signup", logged_in=False)
                    st.switch_page(signup_pg)


restore_session()

if is_debug_enabled():
    if st.session_state.is_logged_in:
        logger.debug(f"User logged in: {st.session_state.user}")
    else:
        logger.debug("User not logged in - showing public pages")

# Define navigation pages based on login status
if st.session_state.is_logged_in:
    pages = {
        "Pages": [feed_pg, discover_pg, draw_pg],
        "Account": [profile_pg, settings_pg]
    }
    if is_debug_enabled():
        logger.debug("Navigation pages for logged-in user: feed, discover, draw, profile, settings")
else:
    pages = {
        "Pages": [feed_pg, discover_pg],
        "Account": [login_pg, signup_pg]
    }
    if is_debug_enabled():
        logger.debug("Navigation pages for logged-out user: feed, discover, login, signup")

# Single st.navigation() call with pages list
page = st.navigation(pages, position="hidden")

if is_debug_enabled():
    logger.debug(f"Page being rendered: {page.title}")

render_user_menu()

st.divider()

page.run()
