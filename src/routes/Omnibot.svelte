<script>
    import { onMount } from "svelte";
    import { selectedTriangle } from './store'; // Importer le store

    let canvas; // Initialisation du canvas

    // Fonction permettant de dessiner des triangles équilatéraux
    function drawEquilateralTriangle(ctx, x1, y1, x2, y2, x3, y3) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.lineTo(x3, y3);
        ctx.closePath();
        ctx.stroke();
        ctx.fill();
    }

    function drawTrapeze(ctx, x1, y1, x2, y2, x3, y3, x4, y4) {
    ctx.beginPath();
    ctx.moveTo(x1, y1); // Coin supérieur gauche
    ctx.lineTo(x2, y2); // Coin supérieur droit
    ctx.lineTo(x3, y3); // Coin inférieur droit
    ctx.lineTo(x4, y4); // Coin inférieur gauche
    ctx.closePath();
    ctx.stroke();
    ctx.fill();
    }

    // Fonction pour vérifier si un point est dans un triangle
    function isPointInTriangle(px, py, { x1, y1, x2, y2, x3, y3 }) {
        const area = 0.5 * (-y2 * x3 + y1 * (-x2 + x3) + x1 * (y2 - y3) + x2 * y3);
        const s = 1 / (2 * area) * (y1 * x3 - x1 * y3 + (y3 - y1) * px + (x1 - x3) * py);
        const t = 1 / (2 * area) * (x1 * y2 - y1 * x2 + (y1 - y2) * px + (x2 - x1) * py);
        const u = 1 - s - t;
        console.log(`s: ${s}, t: ${t}, u: ${u}`);
        return s >= 0 && t >= 0 && u >= 0;
    }

    function isPointInTrapeze(px, py, { x1, y1, x2, y2, x3, y3, x4, y4 }) {
    // Vérification à l'aide de la méthode du produit vectoriel
    function sign(x1, y1, x2, y2, x, y) {
        return (x1 - x) * (y2 - y) - (x2 - x) * (y1 - y);
    }

    let d1, d2, d3, d4;
    d1 = sign(px, py, x1, y1, x2, y2);
    d2 = sign(px, py, x2, y2, x3, y3);
    d3 = sign(px, py, x3, y3, x4, y4);
    d4 = sign(px, py, x4, y4, x1, y1);

    const has_neg = (d1 < 0) || (d2 < 0) || (d3 < 0) || (d4 < 0);
    const has_pos = (d1 > 0) || (d2 > 0) || (d3 > 0) || (d4 > 0);

    return !(has_neg && has_pos);
}

    onMount(() => {
        console.log("onMount triggered");
        if (!canvas) {
            console.error("Canvas not initialized");
            return;
        }

        const ctx = canvas.getContext("2d");
        if (!ctx) {
            console.error("Failed to get canvas context");
            return;
        }

        console.log("Canvas and context initialized");

        if (canvas) {
            canvas.addEventListener('click', () => {
                console.log('Canvas clicked directly');
            });
        } else {
            console.error("Canvas not initialized");
        }

        ctx.fillStyle = "#494949"; 
        ctx.strokeStyle = "#000000"; 
        const trapezes = [
            { id: 1, x1: 275, y1: 70.1, x2: 125, y2: 70.1, x3: 150, y3: 113.4, x4: 250, y4: 113.4 },
            { id: 2, x1: 350, y1: 200, x2: 275, y2: 70.1, x3: 250, y3: 113.4, x4: 300, y4: 200 },
            { id: 3, x1: 275, y1: 329.91, x2: 350, y2: 200, x3: 300, y3: 200, x4: 250, y4: 286.61 },
            { id: 4, x1: 125, y1: 329.91, x2: 275, y2: 329.91, x3: 250, y3: 286.61, x4:150, y4: 286.61 },
            { id: 5, x1: 50, y1: 200, x2: 125, y2: 329.91, x3: 150, y3: 286.61, x4: 100, y4: 200 },
            { id: 6, x1: 125, y1: 70.1, x2: 50, y2: 200, x3: 100, y3: 200, x4: 150, y4: 113.4  }
        ]
        // Liste des coordonnées des sommets de tous les triangles formant l'Omnibot
        const triangles = [
            { id: 7, x1: 250, y1: 113.4, x2: 200, y2: 200, x3: 150, y3: 113.4 },
            { id: 8, x1: 300, y1: 200, x2: 200, y2: 200, x3: 250, y3: 113.4 },
            { id: 9, x1: 250, y1: 286.61, x2: 200, y2: 200, x3: 300, y3: 200 },
            { id: 10, x1: 150, y1: 286.61, x2: 200, y2: 200, x3: 250, y3: 286.61 },
            { id: 11, x1: 100, y1: 200, x2: 200, y2: 200, x3: 150, y3: 286.61 },         
            { id: 12, x1: 150, y1: 113.4, x2: 200, y2: 200, x3: 100, y3: 200 } 
        ];

        // Boucle permettant de tracer tous les triangles
        for (const triangle of triangles) {
            ctx.fillStyle = triangle.id === $selectedTriangle.id ? $selectedTriangle.color : '#494949';
            drawEquilateralTriangle(ctx, triangle.x1, triangle.y1, triangle.x2, triangle.y2, triangle.x3, triangle.y3);
        }

        for (const trapeze of trapezes){
            ctx.fillStyle = trapeze.id === $selectedTriangle.id ? $selectedTriangle.color : '#494949';
            drawTrapeze(ctx, trapeze.x1, trapeze.y1, trapeze.x2, trapeze.y2, trapeze.x3, trapeze.y3, trapeze.x4, trapeze.y4)
        }

        // Event listener pour les clics sur le canvas
        canvas.addEventListener('click', (event) => {
            console.log("Canvas clicked"); // Log pour vérifier si l'événement est détecté
            const rect = canvas.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            console.log(`Clicked at: ${x}, ${y}`); // Ajout du log

            let clickedTriangleId = null;
            for (const triangle of triangles) {
                if (isPointInTriangle(x, y, triangle) ) {
                    clickedTriangleId = triangle.id;
                    break;
                }
            }

            let clickedTrapezeID = null;
            for(const trapeze of trapezes){
                if (isPointInTrapeze(x,y,trapeze)) {
                    clickedTrapezeID = trapeze.id;
                    break
                }
            }

            if (clickedTriangleId !== null) {
                console.log(`Clicked on triangle ID: ${clickedTriangleId}`); // Ajout du log
                selectedTriangle.set({id:clickedTriangleId, color: '#ff0000'});
            } else if (clickedTrapezeID !== null){
                console.log(`Clicked on trapeze ID: ${clickedTrapezeID}`);
                selectedTriangle.set({id:clickedTrapezeID, color: '#ff0000'});
            }else {
                selectedTriangle.set({id:null, color: '#ff0000'})
                console.log("Clicked outside Omnibot"); // Log si le clic n'était sur aucun triangle
            }
           
        });
    });
</script>

<div class="canvas-container">
    <canvas bind:this={canvas} width="400" height="400"></canvas> <!-- Création du canvas 400x400px -->
</div>

<style>
    canvas {
        display: block;
        margin: auto;
        z-index: 10;
        cursor: pointer; /* Ajoute un pointeur pour indiquer que le canvas est cliquable */
        
        
    }
    .canvas-container {
        position: relative;
        width: 800px;
        height: 500px;
        z-index: 1;
    }

    
</style>
