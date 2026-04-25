

function clamp(num, min, max) {
  return num <= min 
    ? min 
    : num >= max 
      ? max 
      : num
}


let scenes = [];


function drawStroke(ctx, stroke) {
    let dx = Math.random() - .5
    let dy = Math.random() - .5

    ctx.beginPath();
    ctx.moveTo(stroke[0][0] + dx, stroke[0][1] + dy);
    for (let p = 1; p < stroke.length; p++) {
        dx = clamp(7/8 * dx + (Math.random() - .5) / 4, -.5, .5)
        dy = clamp(7/8 * dy + (Math.random() - .5) / 4, -.5, .5)
        ctx.lineWidth = stroke[p][2];
        ctx.lineTo(stroke[p][0] + dx, stroke[p][1] + dy);
        ctx.stroke();
        ctx.beginPath()
        ctx.moveTo(stroke[p][0] + dx, stroke[p][1] + dy);
    }
}

function draw(ctx, scn) {
    ctx.clearRect(0, 0, 128, 128);
    
    for (let s = 0; s < scn.strokes.length; s++) {
        ctx.strokeStyle = scn.palette[scn.strokes[s].color].value
        drawStroke(ctx, scn.strokes[s].shape)
    }

    if ("stroke" in scn && scn.stroke.length > 1) {
        ctx.strokeStyle = scn.palette[scn.activeColor].value
        drawStroke(ctx, scn.stroke);
    } 

    if ("cursor" in scn) {
        // ctx.strokeStyle = "#FFF";
        ctx.strokeStyle = scn.palette[scn.activeColor].value
        ctx.beginPath();
        ctx.lineWidth = 1;
        ctx.arc(scn.cursor[0], scn.cursor[1], scn.cursor[2], 0, 2*Math.PI);
        ctx.stroke(); 
    }
}

function frame() {
    for (let i=0; i < scenes.length; i++) {
        draw(scenes[i][0], scenes[i][1]);
    }
}

setInterval(frame, 100);

function point(ctx, size, evt) {
    

    return [
        Math.floor(evt.offsetX * ctx.canvas.width / ctx.canvas.clientWidth),
        Math.floor(evt.offsetY * ctx.canvas.height / ctx.canvas.clientHeight), 
        evt.pressure == 0 ? .5 * size : evt.pressure * size
    ];
}

function compile(scn) {
    let out = {}
    out.palette = []
    for (let i=0; i<8; i++){
        out.palette.push(scn.palette[i].value)
    }
    out.strokes = scn.strokes
    out.bg_color = "#03070F";
    return out
}

export default function({setTriggerValue, parentElement, data}) {
    let canvas = parentElement.querySelector("canvas");
    let ctx = canvas.getContext("2d");
    let cursor_size = parentElement.querySelector(".size")
    ctx.lineCap = "round"

    let scn = data.scn;


    let p = parentElement.querySelectorAll(".color");
    for (let i = 0; i < 8; i++) {
        p[i].value = scn.palette[i];
        scn.palette[i] = p[i];
    }
    

    if (data.isEditor) {
        scn.activeColor = 0;
        scn.stroke = [];
        scn.cursor = [0,0,0]
    
        for (let i = 0; i<8; i++) {
            scn.palette[i].addEventListener("pointerdown", function (evt) {
                let s = parentElement.querySelector(".selected")
                if (s == evt.target){
                    evt.target.disabled = false;
                } else {
                    s.disabled = true;
                    s.classList.remove("selected");
                    evt.target.classList.add("selected");
                    scn.activeColor = i;
                }
            })
        }

        scn.undoBuffer = [];
        canvas.addEventListener("pointerdown", evt => {
            scn.stroke.push(point(ctx, cursor_size.value, evt));
        })
        canvas.addEventListener("pointermove", evt => {
            scn.cursor = point(ctx, cursor_size.value, evt);
            if (evt.pressure > 0) {
                let l = scn.stroke[scn.stroke.length-1];
                if ((scn.cursor[0] - l[0])**2 + (scn.cursor[1] - l[1])**2 >= 1) {
                    scn.stroke.push(scn.cursor);
                }
            } else if (scn.stroke.length > 1) {
                scn.strokes.push({color: scn.activeColor, shape: scn.stroke});
                scn.stroke = []
                scn.undoBuffer = []
            } else {
                scn.stroke = []
            }
        })

        document.addEventListener("keyup", evt => {
            if (evt.ctrlKey && evt.key == "z") {
                if (scn.strokes.length > 0) {
                    scn.undoBuffer.push(scn.strokes.pop());
                }
            }

            else if (evt.ctrlKey && evt.key == "Z") {
                if (scn.undoBuffer.length > 0) {
                    scn.strokes.push(scn.undoBuffer.pop());
                }
            }
        })

    } else {
        let bar = parentElement.querySelector(".bar");
        bar.style.display = "none";
        canvas.style.height = "100%";
    }
    
    scenes.push([ctx, data.scn]);

    parentElement.querySelector("button").addEventListener("click", () => {
        setTriggerValue("commit", compile(scn));
    });

}