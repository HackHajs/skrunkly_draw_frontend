
const canvas = document.getElementsByClassName("canvas")[0];
const ctx = canvas.getContext("2d");

const palette = document.getElementsByClassName("color");
const cursor_size = document.getElementsByClassName("size")[0];

ctx.fillStyle = "#FFFFFF"
ctx.lineCap = "round"

let cursor = [0,0,0]

// let palette = ["#0000FF", "#00FF00", "#FF0000", "#FFFFFF"];
let strokes = [];
let stroke = [];

let undoBuffer = [];

let color = 0;

function clamp(num, min, max) {
  return num <= min 
    ? min 
    : num >= max 
      ? max 
      : num
}


function drawStroke(s) {
    ctx.strokeStyle = palette[s.color].value;

    dx = Math.random() - .5
    dy = Math.random() - .5

    // ctx.lineWidth = s.points[0][2];
    ctx.beginPath();
    ctx.moveTo(s.points[0][0] + dx, s.points[0][1] + dy);
    for (let p = 1; p < s.points.length; p++) {
        dx = clamp(7/8 * dx + (Math.random() - .5) / 4, -.5, .5)
        dy = clamp(7/8 * dy + (Math.random() - .5) / 4, -.5, .5)
        ctx.lineWidth = s.points[p][2];
        ctx.lineTo(s.points[p][0] + dx, s.points[p][1] + dy);
        ctx.stroke();
        ctx.beginPath()
        ctx.moveTo(s.points[p][0] + dx, s.points[p][1] + dy);
    }
}

function draw() {
    ctx.clearRect(0, 0, 128, 128);

    for (let s = 0; s < strokes.length; s++) {
        drawStroke(strokes[s])
    }
    if (stroke.length > 1) {
        drawStroke({color: color, points: stroke});
    } 

    if (cursor[2] != 0) {
        c = cursor[2]
    } else {
        c = cursor_size.value * .5
    }

    ctx.strokeStyle = "#FFF"
    ctx.beginPath();
    ctx.lineWidth = 1;
    ctx.arc(cursor[0], cursor[1], c, 0, 2*Math.PI);
    ctx.stroke();
    // ctx.fillRect(cursor[0] - c, cursor[1] - c, c * 2, c * 2);
}

setInterval(draw, 100);

function point(evt) {
    return [
        Math.floor(evt.offsetX * ctx.canvas.width / ctx.canvas.clientWidth),
        Math.floor(evt.offsetY * ctx.canvas.height / ctx.canvas.clientHeight), 
        evt.pressure * cursor_size.value
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
        color = (color + 1) % palette.length;
    }
}


canvas.addEventListener("pointermove", move)
canvas.addEventListener("pointerdown", down)
document.addEventListener("keyup", keypress)

// colors = document.getElementsByClassName("color")
for (let e = 0; e < palette.length; e++) {
    palette[e].addEventListener("pointerdown", function (evt) {
        s = document.getElementsByClassName("selected")[0]
        if (s == evt.target){
            evt.target.disabled = false;
        } else {
            s.disabled = true;
            s.classList.remove("selected");
            evt.target.classList.add("selected");
            color = e;
        }
    })
} 

