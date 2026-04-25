import streamlit as st
from canvas import canvas 

st.header("Draw")

canvas(data={"isEditor": True, "scn": 
{
    "palette": ["#FF0000", "#9F9F00", "#00FF00", "#009F9F", "#0000FF", "#9F009F", "#7F7F7F", "#CFCFCF"],
    "strokes": []
}},
    on_commit_change = lambda:print("beep") #TODO
)