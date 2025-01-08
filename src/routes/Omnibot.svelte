<script>
    import { onMount } from "svelte";
    import { selectedTriangle } from './store'; // Importer le store

    let canvas; // Initialisation du canvas
    let selectedShape = null;
    let hoveredShape = null;

    // Définition des listes de triangles et de trapèzes
    const triangles = [
        { id: 7, x1: 250, y1: 113.4, x2: 200, y2: 200, x3: 150, y3: 113.4, hoverColor: '#696761',clickColor: '#FF662E' },
        { id: 8, x1: 300, y1: 200, x2: 200, y2: 200, x3: 250, y3: 113.4, hoverColor: '#696761',clickColor: '#FF662E' },
        { id: 9, x1: 250, y1: 286.61, x2: 200, y2: 200, x3: 300, y3: 200, hoverColor: '#696761',clickColor: '#FF662E' },
        { id: 10, x1: 150, y1: 286.61, x2: 200, y2: 200, x3: 250, y3: 286.61, hoverColor: '#696761',clickColor: '#FF662E' },
        { id: 11, x1: 100, y1: 200, x2: 200, y2: 200, x3: 150, y3: 286.61, hoverColor: '#696761',clickColor: '#FF662E' },
        { id: 12, x1: 150, y1: 113.4, x2: 200, y2: 200, x3: 100, y3: 200, hoverColor: '#696761',clickColor: '#FF662E' }
    ];

    const trapezes = [
        { id: 1, x1: 275, y1: 70.1, x2: 125, y2: 70.1, x3: 150, y3: 113.4, x4: 250, y4: 113.4, hoverColor: '#696761',clickColor: '#FF662E' },
        { id: 2, x1: 350, y1: 200, x2: 275, y2: 70.1, x3: 250, y3: 113.4, x4: 300, y4: 200, hoverColor: '#696761',clickColor: '#FF662E' },
        { id: 3, x1: 275, y1: 329.91, x2: 350, y2: 200, x3: 300, y3: 200, x4: 250, y4: 286.61, hoverColor: '#696761' ,clickColor: '#FF662E'},
        { id: 4, x1: 125, y1: 329.91, x2: 275, y2: 329.91, x3: 250, y3: 286.61, x4: 150, y4: 286.61, hoverColor: '#696761',clickColor: '#FF662E' },
        { id: 5, x1: 50, y1: 200, x2: 125, y2: 329.91, x3: 150, y3: 286.61, x4: 100, y4: 200, hoverColor: '#696761',clickColor: '#FF662E' },
        { id: 6, x1: 125, y1: 70.1, x2: 50, y2: 200, x3: 100, y3: 200, x4: 150, y4: 113.4, hoverColor: '#696761',clickColor: '#FF662E' }
    ];


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


    // Fonction pour dessiner un trapèze
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
        return s >= 0 && t >= 0 && u >= 0;
    }


    // Fonction pour vérifier si un point est dans un trapèze
    function isPointInTrapeze(px, py, { x1, y1, x2, y2, x3, y3, x4, y4 }) {
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


    // Fonction pour redessiner le canvas avec les formes et les couleurs actuelles
    function redrawCanvas() {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Effacer le canvas

    // Dessiner tous les triangles
    for (const triangle of triangles) {
        if (triangle.id === hoveredShape) {
            ctx.fillStyle = triangle.hoverColor; // Couleur lorsque survolé
        } else if (triangle.id === $selectedTriangle.id) {
            ctx.fillStyle = $selectedTriangle.color; // Couleur lorsque sélectionné
        } else {
            ctx.fillStyle = '#494949'; // Couleur par défaut
        }
        drawEquilateralTriangle(ctx, triangle.x1, triangle.y1, triangle.x2, triangle.y2, triangle.x3, triangle.y3);
    }

    // Dessiner tous les trapèzes
    for (const trapeze of trapezes) {
        if (trapeze.id === hoveredShape) {
            ctx.fillStyle = trapeze.hoverColor; // Couleur lorsque survolé
        } else if (trapeze.id === $selectedTriangle.id) {
            ctx.fillStyle = $selectedTriangle.color; // Couleur lorsque sélectionné
        } else {
            ctx.fillStyle = '#494949'; // Couleur par défaut
        }
        drawTrapeze(ctx, trapeze.x1, trapeze.y1, trapeze.x2, trapeze.y2, trapeze.x3, trapeze.y3, trapeze.x4, trapeze.y4);
    }
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

        // Gestion des événements sur le canvas
        canvas.addEventListener('click', (event) => {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        let clickedTriangleId = null;
        for (const triangle of triangles) {
            if (isPointInTriangle(x, y, triangle)) {
                clickedTriangleId = triangle.id;
                break;
            }
        }

        let clickedTrapezeID = null;
        for (const trapeze of trapezes) {
            if (isPointInTrapeze(x, y, trapeze)) {
                clickedTrapezeID = trapeze.id;
                break;
            }
        }

        if (clickedTriangleId !== null) {
            selectedTriangle.set({ id: clickedTriangleId, color: triangles.find(t => t.id === clickedTriangleId).clickColor });
        } else if (clickedTrapezeID !== null) {
            selectedTriangle.set({ id: clickedTrapezeID, color: trapezes.find(t => t.id === clickedTrapezeID).clickColor });
        } else {
            selectedTriangle.set({ id: null, color: '#494949' });
        }

        redrawCanvas(); // Redessiner après la sélection
    });


           
    // Gestion de l'événement de survol sur le canvas
    canvas.addEventListener('mousemove', (event) => {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        let hoveredTriangleId = null;
        let hoveredTrapezeId = null;

        // Vérifier si la souris survole un triangle
        for (const triangle of triangles) {
            if (isPointInTriangle(x, y, triangle)) {
                hoveredTriangleId = triangle.id;
                break;
            }
        }

        // Vérifier si la souris survole un trapèze
        for (const trapeze of trapezes) {
            if (isPointInTrapeze(x, y, trapeze)) {
                hoveredTrapezeId = trapeze.id;
                break;
            }
        }

        // Mettre à jour l'état local pour le survol
        if (hoveredTriangleId !== null || hoveredTrapezeId !== null) {
            hoveredShape = hoveredTriangleId !== null ? hoveredTriangleId : hoveredTrapezeId;
        } else {
            hoveredShape = null;
        }

        // Redessiner le canvas avec les nouvelles couleurs des triangles et trapèzes survolés
        redrawCanvas();
    });

    // Gestion de l'événement de sortie du canvas
    canvas.addEventListener('mouseout', () => {
        // Réinitialisation de la couleur du store
        hoveredShape = null;
        // Redessiner le canvas avec les couleurs de base
        redrawCanvas();
    });

        // Appel initial pour dessiner le canvas avec les formes par défaut
        redrawCanvas();
    });

</script>

<div class="canvas-container">
    <canvas bind:this={canvas} width="400" height="400"></canvas>
</div>

<style>
    canvas {
        display: block;
        margin: auto;
        z-index: 10;
        cursor: pointer;
    }

    .canvas-container {
        position: relative;
        z-index: 1;
    }
</style>
