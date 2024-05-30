<script>
    import { onMount } from "svelte";

    let canvas;
    const size = 80; 

    function drawEquilateralTriangle(ctx, x, y, size, angle) {
        ctx.beginPath();
        for (let i = 0; i < 3; i++) {
            ctx.lineTo(
                x + size * Math.cos(angle + (i * 2 * Math.PI) / 3),
                y + size * Math.sin(angle + (i * 2 * Math.PI) / 3)
            );
        }
        ctx.closePath();
        ctx.stroke();
        ctx.fill();
    }

    function drawHexagonWithTriangles(ctx, x, y, size) {
        const angleStep = Math.PI / 3; // 60 degrés en radians
        for (let i = 0; i < 6; i++) {
            const angle = i * angleStep;
            const triangleCenterX = x + size * Math.cos(angle);
            const triangleCenterY = y + size * Math.sin(angle);
            drawEquilateralTriangle(ctx, triangleCenterX, triangleCenterY, size, angle + Math.PI / 6);
        }
    }

    onMount(() => {
        const ctx = canvas.getContext("2d");
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;

        ctx.fillStyle = "#A1CEE1"; 
        ctx.strokeStyle = "#000000"; 
        drawHexagonWithTriangles(ctx, centerX, centerY, size);
    });
</script>

<canvas bind:this={canvas} width="400" height="400"></canvas>

<style>
    canvas {
        display: block;
        margin: auto;
    }
</style>
