import streamlit as st

st.header("Draw")

js_folder_path = "../canvas"
iframe_html = f"""
<iframe
    src="{js_folder_path}/canvas.html"
    width="100%"
    height="600"
    frameborder="0"
    style="border: 1px solid #ddd; border-radius: 4px;">
</iframe>
"""
st.components.v1.html(iframe_html, height=620)
