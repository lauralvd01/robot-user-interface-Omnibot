<script>
    import { onMount } from "svelte";
    import {
        selectedTriangle,
        triangles,
        trapezes,
        centers,
        drawEquilateralTriangle,
        drawTrapeze,
        isPointInTriangle,
        isPointInTrapeze,
    } from "./store"; // Importer le store

    let canvas; // Initialisation du canvas
    let hoveredShape = null;

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
                ctx.fillStyle = "#494949"; // Couleur par défaut
            }
            drawEquilateralTriangle(
                ctx,
                triangle.x1,
                triangle.y1,
                triangle.x2,
                triangle.y2,
                triangle.x3,
                triangle.y3,
            );
        }

        // Dessiner tous les trapèzes
        for (const trapeze of trapezes) {
            if (trapeze.id === hoveredShape) {
                ctx.fillStyle = trapeze.hoverColor; // Couleur lorsque survolé
            } else if (trapeze.id === $selectedTriangle.id) {
                ctx.fillStyle = $selectedTriangle.color; // Couleur lorsque sélectionné
            } else {
                ctx.fillStyle = "#494949"; // Couleur par défaut
            }
            drawTrapeze(
                ctx,
                trapeze.x1,
                trapeze.y1,
                trapeze.x2,
                trapeze.y2,
                trapeze.x3,
                trapeze.y3,
                trapeze.x4,
                trapeze.y4,
            );
        }

        // Draw white circles in the middle of each triangle and each trapeze that are connected to a module
        for (const center of centers) {
            if ($triangleImages[center.id] !== null) {
                // Check if there is a module connected on this slot and draw a white circle with the image in the middle
                const image = document.getElementById(center.id);
                ctx.fillStyle = "white";
                ctx.beginPath();
                ctx.arc(center.x, center.y, 18, 0, 2 * Math.PI);
                ctx.fill();
                ctx.drawImage(image, center.x - 15, center.y - 15, 30, 30);
            }
        }
    }

    // Runs when the Omnibot component is mounted
    onMount(() => {
        // console.log("onMount triggered");

        if (!canvas) {
            console.error("Canvas not initialized");
            return;
        }

        const ctx = canvas.getContext("2d");
        if (!ctx) {
            console.error("Failed to get canvas context");
            return;
        }

        // console.log("Canvas and context initialized");

        // Gestion des événements sur le canvas
        canvas.addEventListener("click", (event) => {
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
                selectedTriangle.set({
                    id: clickedTriangleId,
                    color: triangles.find((t) => t.id === clickedTriangleId)
                        .clickColor,
                });
            } else if (clickedTrapezeID !== null) {
                selectedTriangle.set({
                    id: clickedTrapezeID,
                    color: trapezes.find((t) => t.id === clickedTrapezeID)
                        .clickColor,
                });
            } else {
                selectedTriangle.set({ id: null, color: "#494949" });
            }

            redrawCanvas(); // Redessiner après la sélection
        });

        // Gestion de l'événement de survol sur le canvas
        canvas.addEventListener("mousemove", (event) => {
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
                hoveredShape =
                    hoveredTriangleId !== null
                        ? hoveredTriangleId
                        : hoveredTrapezeId;
            } else {
                hoveredShape = null;
            }

            // Redessiner le canvas avec les nouvelles couleurs des triangles et trapèzes survolés
            redrawCanvas();
        });

        // Gestion de l'événement de sortie du canvas
        canvas.addEventListener("mouseout", () => {
            // Réinitialisation de la couleur du store
            hoveredShape = null;
            // Redessiner le canvas avec les couleurs de base
            redrawCanvas();
        });

        // Appel initial pour dessiner le canvas avec les formes par défaut
        redrawCanvas();
    });

    // Get connected_modules from parent component and update triangles and trapezes info accordingly
    import { connected_modules } from "./data_store";
    import {
        triangleTitle,
        triangleData,
        triangleImages,
        functionalityImages,
    } from "./store";

    function updateCanvasInfo(connected_modules) {
        if (connected_modules.length === 0) {
            // Reset the store
            triangleTitle.set({
        1: null,
        2: null,
        3: null,
        4: null,
        5: null,
        6: null,
        7: null,
        8: null,
        9: null,
        10: null,
        11: null,
        12: null
    });
            triangleData.set({
        1: null,
        2: null,
        3: null,
        4: null,
        5: null,
        6: null,
        7: null,
        8: null,
        9: null,
        10: null,
        11: null,
        12: null
    });
            triangleImages.set({
        1: null,
        2: null,
        3: null,
        4: null,
        5: null,
        6: null,
        7: null,
        8: null,
        9: null,
        10: null,
        11: null,
        12: null
    });
            return;
        }
        for (let index = 0; index < connected_modules.length; index++) {
            const module = connected_modules[index];

            if (module.module_id !== null && module.module_id !== 32) {
                $triangleTitle[index + 1] = module.name;
                $triangleData[index + 1] = {"slot_id": index+1, ...module};
                    // `Module id : ${module.module_id}, Fonction : ${module.functionality !== null ? module.functionality : "Aucune"}, Caractéristiques : ${module.characteristics.length > 0 ? module.characteristics.join(", ") : "Aucune"}`;
                $triangleImages[index + 1] =
                    module.functionality !== null
                        ? functionalityImages[module.functionality]
                        : null;
            } else {
                $triangleTitle[index + 1] = "Emplacement vide";
                $triangleData[index + 1] = "Aucun module connecté";
                $triangleImages[index + 1] = null;
            }
        }
    }

    // Redraw the canvas when at least one img component is mounted and the image loaded
    function updateCanvasWhenLoaded(img_node) {
        img_node.addEventListener("load", () => {
            redrawCanvas();
            return {};
        });
    }

    $: connected_modules && updateCanvasInfo($connected_modules);
</script>

<div class="canvas-container">
    <div style="display: none;">
        {#each Object.entries($triangleImages) as [id, image]}
            {#if image !== null}
                <img
                    {id}
                    src={image}
                    alt={`Image for slot ${id}`}
                    width="10px"
                    height="10px"
                    use:updateCanvasWhenLoaded
                />
            {/if}
        {/each}
        {#if $connected_modules.length === 0}
            <img
                src={"./src/lib/images/logo_omnibot.svg"}
                alt={"Default image"}
                width="10px"
                height="10px"
                use:updateCanvasWhenLoaded
            />
        {/if}
    </div>
    <canvas bind:this={canvas} width="400" height="400" autoclear={true}
    ></canvas>
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
