import streamlit as st

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
