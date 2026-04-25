import streamlit as st
from utils.auth import require_login

require_login("Feed")

st.header("Settings")

st.divider()
st.subheader("Account Settings")
st.write("Change your account settings here (coming soon)")

st.divider()
st.subheader("Privacy Settings")
st.write("Manage your privacy preferences (coming soon)")

st.divider()
st.subheader("Notification Settings")
st.write("Configure notification preferences (coming soon)")
