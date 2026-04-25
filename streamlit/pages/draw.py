import streamlit as st
from utils.auth import require_login
from utils.logger import get_logger, is_debug_enabled

logger = get_logger(__name__)


def draw_page():
    """Draw page - interactive drawing canvas"""
    require_login("Feed")

    if is_debug_enabled():
        logger.debug("Draw page loaded - user accessing drawing canvas")

    st.header("Draw")
    
    logger.info("User accessing draw page")

    canvas_html = """
<style>
    .canvas {
        height: 100%;
        aspect-ratio: 1;
        image-rendering: pixelated;
        background-color: #03070F;
        cursor: none;
        display: block;
        margin: 0 auto;
        max-width: 100%;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
</style>

<canvas class="canvas" width="512" height="512"></canvas>

<script>
const canvas = document.getElementsByClassName("canvas")[0];
const ctx = canvas.getContext("2d");

ctx.fillStyle = "#FFFFFF"
let cursor_size = 3

let cursor = [0,0,0]

let pallete = ["#0000FF", "#00FF00", "#FF0000", "#FFFFFF"];
let strokes = [];
let stroke = [];

let undoBuffer = [];

let color = 0;
ctx.lineWidth = cursor_size;

function clamp(num, min, max) {
  return num <= min 
    ? min 
    : num >= max 
      ? max 
      : num
}

function drawStroke(s) {
    ctx.strokeStyle = pallete[s.color]

    dx = Math.random() - .5
    dy = Math.random() - .5

    ctx.beginPath();
    ctx.moveTo(s.points[0][0] + dx, s.points[0][1] + dy);
    for (let p = 1; p < s.points.length; p++) {
        dx = clamp(7/8 * dx + (Math.random() - .5) / 4, -.5, .5)
        dy = clamp(7/8 * dy + (Math.random() - .5) / 4, -.5, .5)

        ctx.lineTo(s.points[p][0] + dx, s.points[p][1] + dy);
    }
    ctx.stroke();
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let s = 0; s < strokes.length; s++) {
        drawStroke(strokes[s])
    }
    if (stroke.length > 1) {
        drawStroke({color: color, points: stroke});
    } 

    if (cursor[2] != 0) {
        c = cursor_size * cursor[2]
    } else {
        c = cursor_size * .5
    }

    ctx.fillRect(cursor[0] - c, cursor[1] - c, c * 2, c * 2);
}

setInterval(draw, 100);

function point(evt) {
    return [
        Math.floor(evt.offsetX * ctx.canvas.width / ctx.canvas.clientWidth),
        Math.floor(evt.offsetY * ctx.canvas.height / ctx.canvas.clientHeight), 
        evt.pressure
    ];
}

function move(evt) {
    cursor = point(evt)
    if (evt.pressure > 0) {
        l = stroke[stroke.length-1]
        if ((cursor[0] - l[0])**2 + (cursor[1] - l[1])**2 >= 1) {
            stroke.push(cursor);
        }
    } else if (stroke.length > 1) {
        strokes.push({color: color, points: stroke});
        stroke = []
        undoBuffer = []
    } else {
        stroke = []
    }
}

function down(evt) {
    stroke.push(point(evt));
}

function keypress(evt) {
    if (evt.ctrlKey && evt.key == "z") {
        if (strokes.length > 0) {
            undoBuffer.push(strokes.pop());
        }
    }
    else if (evt.ctrlKey && evt.key == "Z") {
        if (undoBuffer.length > 0) {
            strokes.push(undoBuffer.pop());
        }
    }
    else if (evt.code == "Space") {
        color = (color + 1) % pallete.length;
    }
}

canvas.addEventListener("pointermove", move)
canvas.addEventListener("pointerdown", down)
document.addEventListener("keyup", keypress)
</script>
"""

    st.components.v1.html(canvas_html, height=550)
