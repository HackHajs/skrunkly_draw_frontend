
import streamlit as st

with open("canvas/canvas.js") as file:
    js = file.read()
    

canvas = st.components.v2.component(
    "skrunkle_editor",
    html="""    
        <div class="editor">
        <div class="bar">
            <input class="color selected" type="color" value="#FF0000"/>
            <input class="color"          type="color" value="#9F9F00" disabled/>
            <input class="color"          type="color" value="#00FF00" disabled/>
            <input class="color"          type="color" value="#009F9F" disabled/>
            <input class="color"          type="color" value="#0000FF" disabled/>
            <input class="color"          type="color" value="#9F009F" disabled/>
            <input class="color"          type="color" value="#7F7F7F" disabled/>
            <input class="color"          type="color" value="#CFCFCF" disabled/>

            <div class="spacer"></div>

            <input class="size" type="range" min="1" max="32" value="8" oninput="this.nextElementSibling.innerHTML = this.value"/>
            <p class="sizelabel">8</p>
            <button>Publish</button>
        </div>
        <canvas class="canvas" width="128" height="128"></canvas>
        </div>""",

    css="""
        .editor {
            display: flex;
            flex-direction: column;
            align-items: stretch;
            height: 100vh;
            width: calc(100vh - 50px);
        }

        .bar {
            display: flex;
            background-color: var(--st-background-color);
            height: 50px;
            align-items: center;
        }

        .color {
            border-radius: var(--st-button-radius);
            height: 35px;
            width: 35px;
            margin: 5px;
            background-color: var(--st-background-color);
        }
        .selected {
            background-color: var(--st-primary-color);
        }

        .spacer {flex-grow: 100;}

        .sizeLabel {
            width: 25px;
            color: var(--st-text-color);
        }

        button {
            border-radius: var(--st-button-radius)
        }

        .canvas {
            height: calc(100% - 50px);
            aspect-ratio: 1;
        
            image-rendering: pixelated;
            background-color: #03070F;
            cursor: none;
        }
    """,
    js=js,
)