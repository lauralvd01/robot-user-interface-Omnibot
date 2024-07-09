<script>
    import { onMount } from "svelte";
    import {selectedTriangle} from './store';

    let canvas;
    const size = 80; 

    function drawEquilateralTriangle(ctx, x1, y1, x2, y2, x3, y3) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.lineTo(x3, y3);
        ctx.closePath();
        ctx.stroke();
        ctx.fill();
        canvas.addEventListener('click', function(event) {
      const { offsetX, offsetY } = event;
      if (ctx.isPointInPath(offsetX, offsetY)) {
        selectedTriangle.set(slot); 
      }
    });
    }

    onMount(() => {
        const ctx = canvas.getContext("2d");

        ctx.fillStyle = "#494949"; 
        ctx.strokeStyle = "#000000"; 

        const triangles = [
            { x1: 125, y1: 329.91, x2: 200, y2: 200, x3: 275, y3: 329.91 }, //slot id 1
            { x1: 275, y1: 329.91, x2: 200, y2: 200, x3: 350, y3: 200 }, //slot id 2
            { x1: 350, y1: 200, x2: 200, y2: 200, x3: 275, y3: 70.1 }, //slot id 3
            { x1: 275, y1: 70.1, x2: 200, y2: 200, x3: 125, y3: 70.1 }, //slot id 4
            { x1: 125, y1: 70.1, x2: 200, y2: 200, x3: 50, y3: 200 }, //slot id 5
            { x1: 50, y1: 200, x2: 200, y2: 200, x3: 125, y3: 329.91 }, //slot id 6
            { x1: 150, y1: 286.61, x2: 200, y2: 200, x3: 250, y3: 286.61 }, //slot id 7
            { x1: 250, y1: 286.61, x2: 200, y2: 200, x3: 300, y3: 200 }, //slot id 8
            { x1: 300, y1: 200, x2: 200, y2: 200, x3: 250, y3: 113.4 }, //slot id 9
            { x1: 250, y1: 113.4, x2: 200, y2: 200, x3: 150, y3: 113.4 }, //slot id 10
            { x1: 150, y1: 113.4, x2: 200, y2: 200, x3: 100, y3: 200 }, //Slot id 11
            { x1: 100, y1: 200, x2: 200, y2: 200, x3: 150, y3: 286.61 } //slot id 12
        ];

        for (const triangle of triangles) {
            drawEquilateralTriangle(ctx, triangle.x1, triangle.y1, triangle.x2, triangle.y2, triangle.x3, triangle.y3);
        }
    });
</script>


<div class="canvas-container">
    <canvas bind:this={canvas} width="400" height="400"></canvas>
</div>


<style>
    canvas {
        display: block;
        margin: auto;
        z-index: 1;
    }
    .canvas-container{
        position:relative;
        width:800px;
        height: 500px;
        background-image: url('$lib/images/fond_omnibot.svg')no-repeat center top;
        background-size:contain ;
        background-position: top;
        z-index:-1;
    }
</style>
