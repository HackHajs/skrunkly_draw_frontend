import streamlit as st
from utils.auth import require_login

require_login("Feed")

st.header("My Profile")

user = st.session_state.get("user")
email = "Not available"

if user:
    if hasattr(user, 'email'):
        email = user.email
    elif isinstance(user, dict) and 'email' in user:
        email = user['email']

st.write(f"**Email:** {email}")
st.write("**Username:** (stored in session)")

st.divider()
st.subheader("Profile Information")
st.write("Edit your profile information here (coming soon)")
