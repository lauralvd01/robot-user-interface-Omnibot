import { writable } from "svelte/store";

    export const selectedTriangle = writable({ id: null, color: "#494949" }); //définition d'un emplacement par son id et sa couleur

    // Définition des listes de triangles et de trapèzes

    // x goes ascending from left to right, y goes ascending from top to bottom
    export const triangles = [
        {
            id: 7,
            x1: 250,
            y1: 113.4,
            x2: 200,
            y2: 200,
            x3: 150,
            y3: 113.4,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 8,
            x1: 300,
            y1: 200,
            x2: 200,
            y2: 200,
            x3: 250,
            y3: 113.4,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 9,
            x1: 250,
            y1: 286.61,
            x2: 200,
            y2: 200,
            x3: 300,
            y3: 200,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 10,
            x1: 150,
            y1: 286.61,
            x2: 200,
            y2: 200,
            x3: 250,
            y3: 286.61,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 11,
            x1: 100,
            y1: 200,
            x2: 200,
            y2: 200,
            x3: 150,
            y3: 286.61,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 12,
            x1: 150,
            y1: 113.4,
            x2: 200,
            y2: 200,
            x3: 100,
            y3: 200,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
    ];

    // x goes ascending from left to right, y goes ascending from top to bottom
    export const trapezes = [
        {
            id: 1,
            x1: 275, // Coin supérieur droit
            y1: 70.1,
            x2: 125, // Coin supérieur gauche
            y2: 70.1,
            x3: 150, // Coin inférieur gauche
            y3: 113.4,
            x4: 250, // Coin inférieur droit
            y4: 113.4,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 2,
            x1: 350, // Coin supérieur droit
            y1: 200,
            x2: 275, // Coin supérieur gauche
            y2: 70.1,
            x3: 250, // Coin inférieur gauche
            y3: 113.4,
            x4: 300, // Coin inférieur droit
            y4: 200,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 3,
            x1: 275,
            y1: 329.91,
            x2: 350,
            y2: 200,
            x3: 300,
            y3: 200,
            x4: 250,
            y4: 286.61,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 4,
            x1: 125,
            y1: 329.91,
            x2: 275,
            y2: 329.91,
            x3: 250,
            y3: 286.61,
            x4: 150,
            y4: 286.61,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 5,
            x1: 50,
            y1: 200,
            x2: 125,
            y2: 329.91,
            x3: 150,
            y3: 286.61,
            x4: 100,
            y4: 200,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 6,
            x1: 125,
            y1: 70.1,
            x2: 50,
            y2: 200,
            x3: 100,
            y3: 200,
            x4: 150,
            y4: 113.4,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
    ];

    export const centers = [
        { id: 1, x: 200, y: 91.75 },
        { id: 2, x: 293.75, y: 145.875 },
        { id: 3, x: 293.75, y: 254.63 },
        { id: 4, x: 200, y: 308.76 },
        { id: 5, x: 106.25, y: 254.63 },
        { id: 6, x: 106.25, y: 145.875 },
        { id: 7, x: 200, y: 142.26 },
        { id: 8, x: 250, y: 171.13 },
        { id: 9, x: 250, y: 228.86 },
        { id: 10, x: 200, y: 257.73 },
        { id: 11, x: 150, y: 228.86 },
        { id: 12, x: 150, y: 171.13 },
    ];

    // Fonction permettant de dessiner des triangles équilatéraux
    export function drawEquilateralTriangle(ctx, x1, y1, x2, y2, x3, y3) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.lineTo(x3, y3);
        ctx.closePath();
        ctx.stroke();
        ctx.fill();
    }

    // Fonction pour dessiner un trapèze
    export function drawTrapeze(ctx, x1, y1, x2, y2, x3, y3, x4, y4) {
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
    export function isPointInTriangle(px, py, { x1, y1, x2, y2, x3, y3 }) {
        const area =
            0.5 * (-y2 * x3 + y1 * (-x2 + x3) + x1 * (y2 - y3) + x2 * y3);
        const s =
            (1 / (2 * area)) *
            (y1 * x3 - x1 * y3 + (y3 - y1) * px + (x1 - x3) * py);
        const t =
            (1 / (2 * area)) *
            (x1 * y2 - y1 * x2 + (y1 - y2) * px + (x2 - x1) * py);
        const u = 1 - s - t;
        return s >= 0 && t >= 0 && u >= 0;
    }

    // Fonction pour vérifier si un point est dans un trapèze
    export function isPointInTrapeze(
        px,
        py,
        { x1, y1, x2, y2, x3, y3, x4, y4 },
    ) {
        function sign(x1, y1, x2, y2, x, y) {
            return (x1 - x) * (y2 - y) - (x2 - x) * (y1 - y);
        }

        let d1, d2, d3, d4;
        d1 = sign(px, py, x1, y1, x2, y2);
        d2 = sign(px, py, x2, y2, x3, y3);
        d3 = sign(px, py, x3, y3, x4, y4);
        d4 = sign(px, py, x4, y4, x1, y1);

        const has_neg = d1 < 0 || d2 < 0 || d3 < 0 || d4 < 0;
        const has_pos = d1 > 0 || d2 > 0 || d3 > 0 || d4 > 0;

        return !(has_neg && has_pos);
    }

    //import des images
    import pictoIntelligence from "../src/lib/images/picto_intelligence.svg";
    import picto_energie from "../src/lib/images/picto_energie.svg";
    import picto_mobilite from "../src/lib/images/picto_mobilite.svg";
    import picto_stockage from "../src/lib/images/picto_stockage_energie.svg";
    import picto_capteur from "../src/lib/images/picto_capteur.svg";

    export const functionalityImages = {
        "Stockage d'energie": picto_stockage,
        "Production d'energie": picto_energie,
        "Mobilite": picto_mobilite,
        "Capteur": picto_capteur,
        "Processeur": pictoIntelligence,
        "Reseau": pictoIntelligence,
    };

    export const triangleTitle = writable({
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

    export const triangleData = writable({
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


    export const triangleImages = writable({
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

export const wheels_count = writable(0);