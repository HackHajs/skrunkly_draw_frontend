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
            <button>Publish!</button>
        </div>
        <canvas class="canvas" width="128" height="128"></canvas>
        </div>""",

    css="""
        .editor {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: min(100%, 40rem);
            margin: 0 auto;
        }

        .bar {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-start;
            gap: 0.25rem;
            background-color: var(--st-background-color);
            min-height: 50px;
            width: 100%;
            align-items: center;
            padding: 0.25rem;
            box-sizing: border-box;
        }

        .color {
            border-radius: var(--st-button-radius);

            height: 35px;
            width: 35px;
            margin: 0;
            padding: 1px;
            border-color: var(--st-background-color);
            background-color: var(--st-background-color);
        }
        .selected {
            transform: translateY(10px);
            margin: 8px 4px 0;
            padding: 1px;
            border-color: var(--st-primary-color);
            background-color: var(--st-primary-color);
        }

        .spacer {flex-grow: 100;}

        .size {
            width: 7.5rem;
        }

        .sizelabel {
            width: 25px;
            color: var(--st-text-color);
            margin: 0;
        }

        button {
            font-size: 1rem;
            margin: 0 0 0 auto;
            padding: 0.35rem 0.75rem;
            border-radius: var(--st-button-radius);
        }

        .canvas {
            width: 100%;
            aspect-ratio: 1;
            image-rendering: pixelated;
            background-color: #03070F;
            touch-action: none;
            display: block;
        }

        @media (max-width: 640px) {
            .bar {
                justify-content: center;
            }

            .spacer {
                display: none;
            }

            .color {
                height: 30px;
                width: 30px;
            }

            .selected {
                transform: none;
                margin: 0;
            }

            .size {
                width: 6.5rem;
            }

            button {
                margin-left: 0;
            }
        }
    """,
    js=js,
)
