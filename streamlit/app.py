import streamlit as st
from utils.auth import verify_session, get_user


st.set_page_config(
    page_title="Skrunkly Draw",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    [data-testid="stIconMaterial"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "access_token" not in st.session_state:
    st.session_state.access_token = None


def restore_session():
    """Restore user session on page load if tokens exist"""
    if st.session_state.get("access_token") and not st.session_state.get("is_logged_in"):
        # User has a token but session state says not logged in - restore
        user = get_user()
        if user:
            st.session_state.is_logged_in = True
            st.session_state.user = user


def logout():
    st.session_state.is_logged_in = False
    st.session_state.user = None
    st.session_state.access_token = None
    st.rerun()


restore_session()

feed_page = st.Page("pages/1_feed.py", title="Feed")
discover_page = st.Page("pages/4_discover.py", title="Discover")
draw_page = st.Page("pages/5_draw.py", title="Draw")
login_page = st.Page("pages/2_login.py", title="Log In")
signup_page = st.Page("pages/3_signup.py", title="Sign Up")

if st.session_state.is_logged_in:
    nav_pages = [feed_page, discover_page, draw_page]
else:
    nav_pages = [feed_page, discover_page, login_page, signup_page]

page = st.navigation(nav_pages)

# Top navigation bar
col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="large")
with col1:
    if st.button("Draw", use_container_width=True):
        st.switch_page(draw_page)
with col2:
    st.write("**Button 1**")
with col3:
    st.write("**Button 2**")
with col4:
    if st.session_state.is_logged_in:
        if st.button("Logout", use_container_width=True):
            logout()
    else:
        if st.button("Login", use_container_width=True):
            st.switch_page(login_page)


st.divider()

page.run()