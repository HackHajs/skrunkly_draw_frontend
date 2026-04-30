import streamlit as st
from utils.auth import verify_session, get_user
from utils.cache import invalidate_app_caches
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
    page_icon="favicon.gif",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        div[data-baseweb="select"] > div {
            background-color: transparent !important;
            border-color: transparent !important;
        }

        div[data-testid="stMainBlockContainer"] {
            max-width: 1080px;
            padding: 3.5rem 2rem 2rem;
            margin: 0 auto;
        }

        div[data-testid="stVerticalBlock"] {
            gap: .35rem;
        }

        hr {
            margin: 1em 0em;
        }

        .st-key-auth-nav-mobile,
        .st-key-guest-nav-mobile {
            display: none;
        }

        @media (max-width: 640px) {
            div[data-testid="stMainBlockContainer"] {
                padding: 1.5rem 0.75rem 1.5rem;
                max-width: 100%;
            }

            div[data-testid="stVerticalBlock"] {
                gap: .1rem;
            }

            div[data-testid="stButton"] > button {
                min-height: 2.5rem;
            }

            .st-key-auth-nav-desktop,
            .st-key-guest-nav-desktop {
                display: none !important;
            }

            .st-key-auth-nav-mobile,
            .st-key-guest-nav-mobile {
                display: block !important;
            }
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
if "user_menu_selection_desktop" not in st.session_state:
    st.session_state.user_menu_selection_desktop = None
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
    st.session_state.user_menu_selection_desktop = None
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

def switch_page(param):
    st.switch_page(draw_pg, query_params=param)


def clear_caches_from_menu():
    cleared_reply_cache_keys = invalidate_app_caches(source="user_menu")
    st.toast("Cache invalidated successfully!", icon="🧹")
    if is_debug_enabled():
        log_event(
            "Cache invalidated",
            source="user_menu",
            cleared_reply_cache_keys=cleared_reply_cache_keys,
            logged_in=True,
        )


def handle_user_selection(selected, username, previous_selection):
    if selected == f"{username}":
        return
    if selected == "Profile":
        if is_debug_enabled():
            log_event("User navigated", page="profile", logged_in=True)
        st.switch_page(profile_pg)
    elif selected == "Settings":
        if is_debug_enabled():
            log_event("User navigated", page="settings", logged_in=True)
        st.switch_page(settings_pg)
    elif selected == "Invalidate cache":
        if previous_selection != selected:
            clear_caches_from_menu()
    elif selected == "Logout":
        if is_debug_enabled():
            log_event("User logout", page="logout", logged_in=True)
        logout()


def render_user_menu():
    """Render user profile dropdown menu"""
    if st.session_state.is_logged_in:
        username = get_user_display_name()
        menu_options = [f"{username}", "Profile", "Settings", "Invalidate cache", "Logout"]
        previous_selection_desktop = st.session_state.get("user_menu_selection_desktop")

        with st.container(key="auth-nav-desktop"):
            nav_col, menu_col = st.columns([3, 2], gap="medium")
            with nav_col:
                col1, col2, col3 = st.columns([1, 1, 1], gap="small")
                with col1:
                    if st.button("Draw", use_container_width=True, key="btn_auth_draw_desktop"):
                        if is_debug_enabled():
                            log_event("User navigated", page="draw", logged_in=True)
                        st.switch_page(draw_pg)
                with col2:
                    if st.button("Feed", use_container_width=True, key="btn_auth_feed_desktop"):
                        if is_debug_enabled():
                            log_event("User navigated", page="feed", logged_in=True)
                        st.switch_page(feed_pg)
                with col3:
                    if st.button("Discover", use_container_width=True, key="btn_auth_discover_desktop"):
                        if is_debug_enabled():
                            log_event("User navigated", page="discover", logged_in=True)
                        st.switch_page(discover_pg)
            with menu_col:
                selected_desktop = st.selectbox(
                    label="User Menu",
                    options=menu_options,
                    key="user_menu_desktop",
                    label_visibility="collapsed",
                )

            st.session_state.user_menu_selection_desktop = selected_desktop
            handle_user_selection(selected_desktop, username, previous_selection_desktop)

        with st.container(key="auth-nav-mobile"):
            col1, col2, col3 = st.columns([1, 1, 1], gap="small")

            with col1:
                if st.button("Draw", use_container_width=True, key="btn_auth_draw"):
                    if is_debug_enabled():
                        log_event("User navigated", page="draw", logged_in=True)
                    st.switch_page(draw_pg)
            with col2:
                if st.button("Feed", use_container_width=True, key="btn_auth_feed"):
                    if is_debug_enabled():
                        log_event("User navigated", page="feed", logged_in=True)
                    st.switch_page(feed_pg)
            with col3:
                if st.button("Discover", use_container_width=True, key="btn_auth_discover"):
                    if is_debug_enabled():
                        log_event("User navigated", page="discover", logged_in=True)
                    st.switch_page(discover_pg)

            selected_mobile = st.selectbox(
                label="User Menu",
                options=menu_options,
                key="user_menu",
                label_visibility="collapsed",
            )

            previous_selection_mobile = st.session_state.get("user_menu_selection")
            st.session_state.user_menu_selection = selected_mobile
            handle_user_selection(selected_mobile, username, previous_selection_mobile)
            
    else:
        with st.container(key="guest-nav-desktop"):
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="small")

            with col1:
                if st.button("Feed", use_container_width=True, key="btn_anon_feed_desktop"):
                    if is_debug_enabled():
                        log_event("User navigated", page="feed", logged_in=False)
                    st.switch_page(feed_pg)
            with col2:
                if st.button("Discover", use_container_width=True, key="btn_anon_discover_desktop"):
                    if is_debug_enabled():
                        log_event("User navigated", page="discover", logged_in=False)
                    st.switch_page(discover_pg)
            with col3:
                if st.button("Log In", use_container_width=True, key="btn_anon_login_desktop"):
                    if is_debug_enabled():
                        log_event("User navigated", page="login", logged_in=False)
                    st.switch_page(login_pg)
            with col4:
                if st.button("Sign Up", use_container_width=True, key="btn_anon_signup_desktop"):
                    if is_debug_enabled():
                        log_event("User navigated", page="signup", logged_in=False)
                    st.switch_page(signup_pg)

        with st.container(key="guest-nav-mobile"):
            top_left, top_right = st.columns([1, 1], gap="small")
            bottom_left, bottom_right = st.columns([1, 1], gap="small")
            
            with top_left:
                if st.button("Feed", use_container_width=True, key="btn_anon_feed"):
                    if is_debug_enabled():
                        log_event("User navigated", page="feed", logged_in=False)
                    st.switch_page(feed_pg)
            with top_right:
                if st.button("Discover", use_container_width=True, key="btn_anon_discover"):
                    if is_debug_enabled():
                        log_event("User navigated", page="discover", logged_in=False)
                    st.switch_page(discover_pg)
            with bottom_left:
                if st.button("Log In", use_container_width=True, key="btn_anon_login"):
                    if is_debug_enabled():
                        log_event("User navigated", page="login", logged_in=False)
                    st.switch_page(login_pg)
            with bottom_right:
                if st.button("Sign Up", use_container_width=True, key="btn_anon_signup"):
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
